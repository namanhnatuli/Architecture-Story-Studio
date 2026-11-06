"""Materials, environment, camera and render settings for visual consistency (bpy)."""
import json
import math
from pathlib import Path

import bpy
from mathutils import Matrix, Vector

from engine import framing


def hex_to_rgba(color):
    text = color.lstrip("#")
    if len(text) != 6:
        raise ValueError(f"Expected #RRGGBB: {color}")
    rgb = tuple(int(text[i:i+2], 16)/255.0 for i in (0, 2, 4))
    # Convert sRGB HEX into linear Blender scene RGB to preserve chosen palette.
    def to_linear(v):
        return v / 12.92 if v <= 0.04045 else ((v + 0.055)/1.055)**2.4
    return (*[to_linear(v) for v in rgb], 1.0)


def _socket(sockets, identifier):
    return next(s for s in sockets if s.identifier == identifier)


def add_surface_detail(material, color, detail):
    """Subtle procedural variation: object-space noise scales the base colour and drives
    a bump. `stretch` elongates features (e.g. straw along the slope for thatch)."""
    nodes, links = material.node_tree.nodes, material.node_tree.links
    bsdf = nodes.get("Principled BSDF")
    coord = nodes.new("ShaderNodeTexCoord")
    mapping = nodes.new("ShaderNodeMapping")
    mapping.inputs["Scale"].default_value = tuple(detail.get("stretch", (1.0, 1.0, 1.0)))
    links.new(coord.outputs["Object"], mapping.inputs["Vector"])
    noise = nodes.new("ShaderNodeTexNoise")
    noise.inputs["Scale"].default_value = detail.get("scale", 8.0)
    noise.inputs["Detail"].default_value = detail.get("detail", 4.0)
    links.new(mapping.outputs["Vector"], noise.inputs["Vector"])
    span = nodes.new("ShaderNodeMapRange")
    span.inputs["To Min"].default_value = 1.0 - detail.get("variation", 0.08)
    span.inputs["To Max"].default_value = 1.0 + detail.get("variation", 0.08)
    links.new(noise.outputs["Fac"], span.inputs["Value"])
    tint = nodes.new("ShaderNodeMix")
    tint.data_type = "RGBA"
    tint.blend_type = "MULTIPLY"
    _socket(tint.inputs, "Factor_Float").default_value = 1.0
    _socket(tint.inputs, "A_Color").default_value = hex_to_rgba(color)
    links.new(span.outputs["Result"], _socket(tint.inputs, "B_Color"))
    links.new(_socket(tint.outputs, "Result_Color"), bsdf.inputs["Base Color"])
    links.new(_socket(tint.outputs, "Result_Color"), bsdf.inputs["Emission Color"])
    if detail.get("bump", 0.0) > 0:
        bump = nodes.new("ShaderNodeBump")
        bump.inputs["Strength"].default_value = detail["bump"]
        links.new(noise.outputs["Fac"], bump.inputs["Height"])
        links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])


def _math(nodes, links, op, a, b=None):
    node = nodes.new("ShaderNodeMath")
    node.operation = op
    for i, v in enumerate((a, b)):
        if v is None:
            continue
        if isinstance(v, (int, float)):
            node.inputs[i].default_value = v
        else:
            links.new(v, node.inputs[i])
    return node.outputs[0]


def add_units(material, units):
    """Stylised roofing units: course joints along the slope and staggered vertical joints,
    drawn in the covering's object space (local x = along the slope, y = along the ridge).
    Rows start at the per-object attribute `ass_course_origin` (the eave edge), so they line
    up with the course ribs; each unit gets a slight random tone. Multiplies whatever
    currently feeds Base/Emission colour."""
    nodes, links = material.node_tree.nodes, material.node_tree.links
    bsdf = nodes.get("Principled BSDF")
    coord = nodes.new("ShaderNodeTexCoord")
    xyz = nodes.new("ShaderNodeSeparateXYZ")
    links.new(coord.outputs["Object"], xyz.inputs["Vector"])
    origin = nodes.new("ShaderNodeAttribute")
    origin.attribute_type, origin.attribute_name = "OBJECT", "ass_course_origin"
    m = lambda op, a, b=None: _math(nodes, links, op, a, b)
    course_axis, unit_axis = units.get("axes", ("X", "Y"))   # roofs: X along the slope; walls: ["Z", "X"]
    s = m("DIVIDE", m("SUBTRACT", xyz.outputs[course_axis], origin.outputs["Fac"]), float(units["course"]))
    row = m("FLOOR", s)
    fs = m("SUBTRACT", s, row)
    parity = m("FLOORED_MODULO", row, 2.0)
    t = m("ADD", m("DIVIDE", xyz.outputs[unit_axis], float(units["width"])), m("MULTIPLY", parity, 0.5))
    col = m("FLOOR", t)
    ft = m("SUBTRACT", t, col)
    jc = float(units["joint"]) / float(units["course"]) / 2
    jw = float(units["joint"]) / float(units["width"]) / 2
    near = lambda f, j: m("LESS_THAN", m("MINIMUM", f, m("SUBTRACT", 1.0, f)), j)
    mask = m("MAXIMUM", near(fs, jc), m("MULTIPLY", near(ft, jw), float(units.get("vertical", 1.0))))
    shade = m("SUBTRACT", 1.0, m("MULTIPLY", mask, 1.0 - float(units["joint_dark"])))
    cell = nodes.new("ShaderNodeCombineXYZ")
    links.new(row, cell.inputs["X"])
    links.new(col, cell.inputs["Y"])
    rnd = nodes.new("ShaderNodeTexWhiteNoise")
    rnd.noise_dimensions = "3D"
    links.new(cell.outputs["Vector"], rnd.inputs["Vector"])
    tone = m("ADD", 1.0 - float(units.get("tone", 0.06)), m("MULTIPLY", rnd.outputs["Value"],
                                                           2 * float(units.get("tone", 0.06))))
    factor = m("MULTIPLY", shade, tone)
    src = bsdf.inputs["Base Color"].links[0].from_socket if bsdf.inputs["Base Color"].is_linked else None
    mix = nodes.new("ShaderNodeMix")
    mix.data_type, mix.blend_type = "RGBA", "MULTIPLY"
    _socket(mix.inputs, "Factor_Float").default_value = 1.0
    if src is not None:
        links.new(src, _socket(mix.inputs, "A_Color"))
    else:
        _socket(mix.inputs, "A_Color").default_value = bsdf.inputs["Base Color"].default_value
    gray = nodes.new("ShaderNodeCombineColor")
    for ch in ("Red", "Green", "Blue"):
        links.new(factor, gray.inputs[ch])
    links.new(gray.outputs["Color"], _socket(mix.inputs, "B_Color"))
    links.new(_socket(mix.outputs, "Result_Color"), bsdf.inputs["Base Color"])
    links.new(_socket(mix.outputs, "Result_Color"), bsdf.inputs["Emission Color"])


def make_material(name, color, roughness=0.72, metallic=0.0, glow_gain=1.0, render_method="DITHERED",
                  detail=None, units=None, tint_color=None):
    """Principled material driven per object by two custom properties:
    ass_highlight (0..1 self-coloured glow) and ass_transparency (0 opaque .. 1
    invisible). Missing properties read as 0."""
    material = bpy.data.materials.new(name)
    material.use_nodes = True
    nodes, links = material.node_tree.nodes, material.node_tree.links
    bsdf = nodes.get("Principled BSDF")
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Base Color"].default_value = hex_to_rgba(color)

    # Highlight = the part glowing in its own colour. No accent tint: mixing any other
    # hue shifted roof A (graphite) towards grey/beige and broke A/B colour identity.
    hl = nodes.new("ShaderNodeAttribute")
    hl.attribute_type, hl.attribute_name = "OBJECT", "ass_highlight"
    glow = nodes.new("ShaderNodeMath")
    glow.operation = "MULTIPLY"
    glow.inputs[1].default_value = glow_gain
    links.new(hl.outputs["Fac"], glow.inputs[0])
    bsdf.inputs["Emission Color"].default_value = hex_to_rgba(color)
    links.new(glow.outputs[0], bsdf.inputs["Emission Strength"])

    tr = nodes.new("ShaderNodeAttribute")
    tr.attribute_type, tr.attribute_name = "OBJECT", "ass_transparency"
    alpha = nodes.new("ShaderNodeMath")
    alpha.operation = "SUBTRACT"
    alpha.inputs[0].default_value = 1.0
    links.new(tr.outputs["Fac"], alpha.inputs[1])
    links.new(alpha.outputs[0], bsdf.inputs["Alpha"])
    if detail:
        add_surface_detail(material, color, detail)
    if units:
        add_units(material, units)
    if tint_color:
        # g-r5: a SEQUENCE highlight may colour the part instead of brightening it (ass_tint 0..1, default 0): the
        # surface turns towards the accent as the highlight rises, and the glow gives way by the same share. A light
        # stone glowing brighter on a light backdrop lost contrast (owner, g-r4 pilot review).
        tint = nodes.new("ShaderNodeAttribute")
        tint.attribute_type, tint.attribute_name = "OBJECT", "ass_tint"
        amount = nodes.new("ShaderNodeMath")
        amount.operation = "MULTIPLY"
        amount.use_clamp = True
        links.new(tint.outputs["Fac"], amount.inputs[0])
        links.new(hl.outputs["Fac"], amount.inputs[1])
        mix = nodes.new("ShaderNodeMix")
        mix.data_type = "RGBA"
        socket = lambda sockets, ident: next(x for x in sockets if x.identifier == ident)   # names repeat per type
        links.new(amount.outputs[0], socket(mix.inputs, "Factor_Float"))
        socket(mix.inputs, "A_Color").default_value = hex_to_rgba(color)
        socket(mix.inputs, "B_Color").default_value = hex_to_rgba(tint_color)
        base_in = bsdf.inputs["Base Color"]
        if base_in.is_linked:   # surface detail or units drive the base colour: tint what they produce
            src = base_in.links[0].from_socket
            links.new(src, socket(mix.inputs, "A_Color"))
        links.new(socket(mix.outputs, "Result_Color"), base_in)
        keep = nodes.new("ShaderNodeMath")   # glow x (1 - tint)
        keep.operation = "SUBTRACT"
        keep.inputs[0].default_value = 1.0
        links.new(tint.outputs["Fac"], keep.inputs[1])
        dim = nodes.new("ShaderNodeMath")
        dim.operation = "MULTIPLY"
        links.new(glow.outputs[0], dim.inputs[0])
        links.new(keep.outputs[0], dim.inputs[1])
        links.new(dim.outputs[0], bsdf.inputs["Emission Strength"])
    if hasattr(material, "surface_render_method"):
        material.surface_render_method = render_method
    if hasattr(material, "use_transparent_shadow"):
        material.use_transparent_shadow = True
    material.diffuse_color = hex_to_rgba(color)
    return material


MATERIAL_LIBRARY = Path(__file__).resolve().parents[1] / "asset_library" / "materials" / "stylized_materials.json"


def library_materials(kw, path=MATERIAL_LIBRARY):
    """M4 shared material library (procedural only), keyed like the asset components."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return {key: make_material(m["name"], m["color"], roughness=m.get("roughness", 0.72),
                               metallic=m.get("metallic", 0.0), detail=m.get("detail"), units=m.get("units"), **kw)
            for key, m in data["materials"].items()}


def make_materials(style):
    p = style["palette"]
    m = style.get("materials", {})
    kw = {"glow_gain": m.get("highlight_glow_gain", 1.0),
          "render_method": m.get("transparency_render_method", "DITHERED"),
          "tint_color": p.get("highlight")}
    u = m.get("covering_units", {})
    return {
        "ground": make_material("Ground", p["ground"], roughness=0.9, **kw),
        "stone": make_material("Foundation stone", p["limestone"], **kw),
        "plaster": make_material("Warm plaster", p["plaster"], **kw),
        "wood": make_material("Wood", p["wood"], roughness=0.6, **kw),
        "window": make_material("Stylized glass", "#6B9AA5", roughness=0.27, **kw),
        "metal": make_material("Metal detail", "#7C7C78", roughness=0.35, metallic=0.55, **kw),
        "roof_variant_a": make_material("Roof A graphite", p["roof_variant_a"], **kw),
        "roof_variant_b": make_material("Roof B terracotta", p["roof_variant_b"], **kw),
        # M3 coverings (illustrative appearance, not material science)
        "thatch": make_material("Thatch (longstraw, illustrative)", p.get("thatch", "#B8975A"), roughness=0.95,
                                detail={"scale": 6.0, "stretch": (1.0, 18.0, 18.0), "variation": 0.14, "bump": 0.25},
                                **kw),
        # Unit sizes are stylised (see geometry.COVERING_STYLES); joints must stay readable at 640x360.
        "roof_tile": make_material("Plain clay tile (illustrative)", p.get("roof_tile", "#B1593E"), roughness=0.75,
                                   detail={"scale": 14.0, "variation": 0.07, "bump": 0.05},
                                   units=u.get("plain_tile"), **kw),
        "roof_slate": make_material("Slate (illustrative)", p.get("roof_slate", "#4F5A64"), roughness=0.45,
                                    detail={"scale": 10.0, "variation": 0.05, "bump": 0.03},
                                    units=u.get("slate"), **kw),
        **library_materials(kw),
    }


def _sun(name, collection, source, energy, angle_degrees, shadow=True):
    data = bpy.data.lights.new(name, type="SUN")
    data.energy = energy
    data.angle = math.radians(angle_degrees)
    data.use_shadow = shadow
    obj = bpy.data.objects.new(name, data)
    collection.objects.link(obj)
    # A sun shines along its local -Z; point that away from the source direction.
    obj.rotation_euler = (-Vector(source)).normalized().to_track_quat("-Z", "Y").to_euler()
    return obj


def build_environment(scene, style, materials, collection):
    """Large ground plane + position-independent sun lighting + soft world fill.

    Suns (not area lights aimed at the origin) keep lighting identical for models
    placed anywhere, which SIDE_BY_SIDE comparisons rely on.
    """
    light = style.get("lighting", {})
    # foundation underside rests on the ground; M8: half-size 1 km, so the wide stacked comparisons of the
    # 72 m long-span models never show the plane's edge (it was 160 m)
    size, z = 1000.0, -0.38
    mesh = bpy.data.meshes.new("ground_mesh")
    mesh.from_pydata([(-size, -size, z), (size, -size, z), (size, size, z), (-size, size, z)], [], [(0, 1, 2, 3)])
    mesh.update()
    ground = bpy.data.objects.new("ground", mesh)
    ground["component_id"], ground["role"], ground["variant_id"] = "ground", "terrain", "environment"
    ground.data.materials.append(materials["ground"])
    collection.objects.link(ground)
    _sun("Key sun", collection, light.get("key_direction", (0.33, -1.0, 1.3)),
         light.get("key_strength", 3.0), light.get("key_angle_degrees", 8.0))
    _sun("Fill sun", collection, light.get("fill_direction", (0.9, 0.55, 0.45)),
         light.get("fill_strength", 0.8), 20.0, shadow=False)
    world = bpy.data.worlds.new("Soft neutral world")
    world.use_nodes = True
    bg = world.node_tree.nodes.get("Background")
    bg.inputs["Color"].default_value = hex_to_rgba(style["background_color"])
    bg.inputs["Strength"].default_value = light.get("world_strength", 0.6)
    scene.world = world
    return ground


def show_backdrop_to_camera(scene, color):
    """A camera below the ground plane sees the world directly: give camera rays a flat backdrop colour, while the
    world keeps lighting the model exactly as in every other shot."""
    tree = scene.world.node_tree
    output = next(n for n in tree.nodes if n.type == "OUTPUT_WORLD")
    lit = next(n for n in tree.nodes if n.type == "BACKGROUND")
    path = tree.nodes.new("ShaderNodeLightPath")
    seen = tree.nodes.new("ShaderNodeBackground")
    seen.inputs["Color"].default_value = hex_to_rgba(color)
    seen.inputs["Strength"].default_value = 1.0
    mix = tree.nodes.new("ShaderNodeMixShader")
    tree.links.new(path.outputs["Is Camera Ray"], mix.inputs[0])
    tree.links.new(lit.outputs[0], mix.inputs[1])
    tree.links.new(seen.outputs[0], mix.inputs[2])
    tree.links.new(mix.outputs[0], output.inputs["Surface"])


def apply_from_below(scene, style, cam_preset, objects):
    """Presets for a camera below the ground plane (CATHEDRAL_FROM_BELOW): no ground plane, a flat backdrop, and no
    parts whose undersides would fill the frame. Hidden parts still count for the framing, which is computed earlier."""
    if not cam_preset.get("hide_ground"):
        return
    if "ground" in bpy.data.objects:
        bpy.data.objects["ground"].hide_render = True
    show_backdrop_to_camera(scene, cam_preset.get("backdrop", style["background_color"]))
    for obj in objects:
        if obj.get("role") in cam_preset.get("hide_roles", ()):
            obj.hide_render = obj.hide_viewport = True
            obj["hidden_by_camera"] = True
    under = cam_preset.get("under_light")
    if under:   # the undersides the camera looks at: a shadowless sun from below (vault surfaces read as light stone)
        collection = next(iter(bpy.data.objects["Key sun"].users_collection))
        _sun("Under fill sun", collection, under["direction"], under["strength"], 30.0, shadow=False)


def camera_preset(style, name):
    presets = style.get("camera", {}).get("presets", {})
    if name not in presets:
        raise ValueError(f"unknown camera preset '{name}' (known: {', '.join(sorted(presets))})")
    return presets[name]


def build_camera(scene, collection, preset, points, aspect, bottom_band=0.0):
    """Locked orthographic camera: direction from the preset, position/scale fitted to points."""
    basis = framing.camera_basis(preset["azimuth_degrees"], preset["elevation_degrees"])
    fit = framing.fit_ortho(points, basis, aspect, preset.get("margin", 0.07), bottom_band)
    data = bpy.data.cameras.new("Locked orthographic")
    data.type = "ORTHO"
    data.ortho_scale = fit["ortho_scale"]
    data.clip_start, data.clip_end = fit["clip_start"], fit["clip_end"]
    camera = bpy.data.objects.new("Camera_LOCKED", data)
    collection.objects.link(camera)
    r, u, f = basis
    loc = fit["location"]
    camera.matrix_world = Matrix((
        (r[0], u[0], -f[0], loc[0]),
        (r[1], u[1], -f[1], loc[1]),
        (r[2], u[2], -f[2], loc[2]),
        (0.0, 0.0, 0.0, 1.0)))
    scene.camera = camera
    return camera, fit, basis


def configure_render(scene, preset, fps, frame_count, style=None):
    engine = preset.get("engine", "EEVEE")
    if engine == "EEVEE":
        # Blender 5.0 renamed the identifier. 4.5 uses BLENDER_EEVEE_NEXT.
        scene.render.engine = "BLENDER_EEVEE" if bpy.app.version >= (5, 0, 0) else "BLENDER_EEVEE_NEXT"
    else:
        scene.render.engine = engine
    scene.render.resolution_x = int(preset["width"])
    scene.render.resolution_y = int(preset["height"])
    scene.render.resolution_percentage = 100
    scene.render.fps = int(fps)
    scene.frame_start = 1
    scene.frame_end = int(frame_count)
    if "samples" in preset and hasattr(scene.eevee, "taa_render_samples"):
        scene.eevee.taa_render_samples = int(preset["samples"])
    scene.render.film_transparent = False
    if hasattr(scene.render.image_settings, "media_type"):
        scene.render.image_settings.media_type = "IMAGE"
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGB"
    scene.render.image_settings.color_depth = "8"
    style = style or {}
    cm = style.get("color_management", {})
    try:
        scene.view_settings.view_transform = cm.get("view_transform", "AgX")
        scene.view_settings.look = cm.get("look", "None")
        scene.view_settings.exposure = float(cm.get("exposure", 0.0))
    except Exception as e:  # missing OCIO names must not abort a render; log it
        print(f"[WARN] color management: {e}")
    ev = style.get("eevee", {})
    for key in ("use_raytracing", "use_fast_gi", "shadow_ray_count", "shadow_step_count"):
        if key in ev and hasattr(scene.eevee, key):
            setattr(scene.eevee, key, ev[key])
    if "samples" not in preset and "samples" in ev:
        scene.eevee.taa_render_samples = int(ev["samples"])
    scene.render.use_file_extension = True
