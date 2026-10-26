"""Materials, environment, camera and render settings for visual consistency (bpy)."""
import math

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


def make_material(name, color, highlight="#D9A441", roughness=0.72, metallic=0.0):
    """Principled material driven per object by two custom properties:
    ass_highlight (0..1 tint towards the highlight colour) and
    ass_transparency (0 opaque .. 1 invisible). Missing properties read as 0."""
    material = bpy.data.materials.new(name)
    material.use_nodes = True
    nodes, links = material.node_tree.nodes, material.node_tree.links
    bsdf = nodes.get("Principled BSDF")
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic

    # Highlight keeps the part's own hue (A/B colour identity matters in comparisons):
    # a light tint towards the accent plus a self-coloured glow.
    hl = nodes.new("ShaderNodeAttribute")
    hl.attribute_type, hl.attribute_name = "OBJECT", "ass_highlight"
    tint = nodes.new("ShaderNodeMath")
    tint.operation = "MULTIPLY"
    tint.inputs[1].default_value = 0.1
    links.new(hl.outputs["Fac"], tint.inputs[0])
    mix = nodes.new("ShaderNodeMix")
    mix.data_type = "RGBA"
    _socket(mix.inputs, "A_Color").default_value = hex_to_rgba(color)
    _socket(mix.inputs, "B_Color").default_value = hex_to_rgba(highlight)
    links.new(tint.outputs[0], _socket(mix.inputs, "Factor_Float"))
    links.new(_socket(mix.outputs, "Result_Color"), bsdf.inputs["Base Color"])
    glow = nodes.new("ShaderNodeMath")
    glow.operation = "MULTIPLY"
    glow.inputs[1].default_value = 0.8
    links.new(hl.outputs["Fac"], glow.inputs[0])
    links.new(_socket(mix.outputs, "Result_Color"), bsdf.inputs["Emission Color"])
    links.new(glow.outputs[0], bsdf.inputs["Emission Strength"])

    tr = nodes.new("ShaderNodeAttribute")
    tr.attribute_type, tr.attribute_name = "OBJECT", "ass_transparency"
    alpha = nodes.new("ShaderNodeMath")
    alpha.operation = "SUBTRACT"
    alpha.inputs[0].default_value = 1.0
    links.new(tr.outputs["Fac"], alpha.inputs[1])
    links.new(alpha.outputs[0], bsdf.inputs["Alpha"])
    if hasattr(material, "surface_render_method"):
        material.surface_render_method = "DITHERED"
    if hasattr(material, "use_transparent_shadow"):
        material.use_transparent_shadow = True
    material.diffuse_color = hex_to_rgba(color)
    return material


def make_materials(style):
    p = style["palette"]
    hl = p.get("highlight", "#D9A441")
    return {
        "ground": make_material("Ground", p["ground"], hl, roughness=0.9),
        "stone": make_material("Foundation stone", p["limestone"], hl),
        "plaster": make_material("Warm plaster", p["plaster"], hl),
        "wood": make_material("Wood", p["wood"], hl, roughness=0.6),
        "window": make_material("Stylized glass", "#6B9AA5", hl, roughness=0.27),
        "metal": make_material("Metal detail", "#7C7C78", hl, roughness=0.35, metallic=0.55),
        "roof_variant_a": make_material("Roof A graphite", p["roof_variant_a"], hl),
        "roof_variant_b": make_material("Roof B terracotta", p["roof_variant_b"], hl),
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
    size, z = 160.0, -0.38  # foundation underside rests on the ground
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


def configure_render(scene, preset, fps, frame_count):
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
    try:
        scene.view_settings.view_transform = "AgX"
    except Exception:
        pass
    scene.render.use_file_extension = True
