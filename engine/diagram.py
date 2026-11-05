"""2D card shots (visual_type MOTION_GRAPHICS): self-made schematics and archival images (bpy).

Elements are placed in card units (x, y in 0..1 of the frame width/height, origin
bottom-left), each fading in at its `appear` time and, optionally, out at `disappear`:

  text     position, text, size (frame-height fraction), align LEFT|CENTER|RIGHT, color,
           plate (a light plate behind the text, the annotation style)
  arrow    start, end, width, color
  rect     box [x0, y0, x1, y1], color (fill, optional), border, border_width, dash
  line     points [[x, y], ...], width, color, dash [dash, gap]
  circle   center, radius (frame-height fraction), color
  polygon  points, color (fill), border, border_width
  image    path (project-relative), asset (id in assets/manifest.json), box (fitted inside,
           aspect kept), crop [u0, v0, u1, v1] of the source, drift [dx, dy] over its display

M7 added rect/line/circle/polygon/image, `disappear` and text plates; text and arrows are
unchanged. Uses Blender's built-in font (no external font licence), flat emission colours
and the Standard view transform so colours match the palette. Fades and drifts reuse
motion.Plan and animate.apply_plan, so the Blender QA compares keys like any 3D shot.
"""
import math
from dataclasses import dataclass
from pathlib import Path

import bpy
from mathutils import Vector

from engine import animate, motion, templates
from engine import scene as scene_mod
from engine.geometry import make_collection

CARD_HEIGHT = 1.0  # world units; width = aspect
KINDS = ("text", "arrow", "rect", "line", "circle", "polygon", "image")
Z = {"image": 0.002, "rect": 0.003, "polygon": 0.004, "line": 0.006, "circle": 0.008, "plate": 0.009,
     "arrow": 0.01, "text": 0.01}


@dataclass
class CardContext:
    shot: dict
    cfg: dict
    scene: object
    plan: object
    fps: int
    frame_count: int
    objects: dict          # element id -> its main object
    render_objects: dict   # every animated object (plates, borders, camera, background)
    camera: object
    aspect: float
    helpers: dict = None   # element id -> helper objects (text plate, border)


def _flat_material(name, color):
    """Emission colour; ass_transparency (object attribute) mixes to fully transparent."""
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nodes, links = m.node_tree.nodes, m.node_tree.links
    nodes.clear()
    out = nodes.new("ShaderNodeOutputMaterial")
    emit = nodes.new("ShaderNodeEmission")
    emit.inputs["Color"].default_value = scene_mod.hex_to_rgba(color)
    emit.inputs["Strength"].default_value = 1.0
    clear = nodes.new("ShaderNodeBsdfTransparent")
    attr = nodes.new("ShaderNodeAttribute")
    attr.attribute_type, attr.attribute_name = "OBJECT", "ass_transparency"
    mix = nodes.new("ShaderNodeMixShader")
    links.new(attr.outputs["Fac"], mix.inputs["Fac"])
    links.new(emit.outputs["Emission"], mix.inputs[1])
    links.new(clear.outputs["BSDF"], mix.inputs[2])
    links.new(mix.outputs["Shader"], out.inputs["Surface"])
    if hasattr(m, "surface_render_method"):
        m.surface_render_method = "BLENDED"
    return m


def _image_material(name, image):
    """The image's own colours as emission (exact under the Standard view transform)."""
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nodes, links = m.node_tree.nodes, m.node_tree.links
    nodes.clear()
    out = nodes.new("ShaderNodeOutputMaterial")
    tex = nodes.new("ShaderNodeTexImage")
    tex.image = image
    tex.interpolation = "Linear"
    emit = nodes.new("ShaderNodeEmission")
    links.new(tex.outputs["Color"], emit.inputs["Color"])
    clear = nodes.new("ShaderNodeBsdfTransparent")
    attr = nodes.new("ShaderNodeAttribute")
    attr.attribute_type, attr.attribute_name = "OBJECT", "ass_transparency"
    mix = nodes.new("ShaderNodeMixShader")
    links.new(attr.outputs["Fac"], mix.inputs["Fac"])
    links.new(emit.outputs["Emission"], mix.inputs[1])
    links.new(clear.outputs["BSDF"], mix.inputs[2])
    links.new(mix.outputs["Shader"], out.inputs["Surface"])
    if hasattr(m, "surface_render_method"):
        m.surface_render_method = "BLENDED"
    return m


def _card_to_world(pt, aspect, z=0.0):
    return Vector(((pt[0] - 0.5) * aspect * CARD_HEIGHT, (pt[1] - 0.5) * CARD_HEIGHT, z))


def _mesh_object(name, verts, faces, collection, uvs=None):
    mesh = bpy.data.meshes.new(f"{name}_mesh")
    mesh.from_pydata(verts, [], faces)
    if uvs is not None:
        layer = mesh.uv_layers.new(name="UVMap")
        for poly in mesh.polygons:
            for li in poly.loop_indices:
                layer.data[li].uv = uvs[mesh.loops[li].vertex_index]
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    collection.objects.link(obj)
    return obj


def _quads(points, width, aspect, z, closed=False, dash=None):
    """Quads (world coords) along a polyline in card units; width in frame-height units."""
    pts = [_card_to_world(p, aspect) for p in points]
    if closed:
        pts.append(pts[0])
    segs = list(zip(pts, pts[1:]))
    if dash:
        d, g = dash[0] * CARD_HEIGHT, dash[1] * CARD_HEIGHT
        out, pos, on = [], 0.0, True
        for a, b in segs:
            seg = (b - a).length
            t = 0.0
            while t < seg - 1e-9:
                step = (d if on else g) - pos
                t1 = min(seg, t + step)
                if on:
                    out.append((a.lerp(b, t / seg), a.lerp(b, t1 / seg)))
                pos += t1 - t
                if pos >= (d if on else g) - 1e-9:
                    pos, on = 0.0, not on
                t = t1
        segs = out
    verts, faces = [], []
    h = width * CARD_HEIGHT / 2
    for a, b in segs:
        dvec = b - a
        n = Vector((-dvec.y, dvec.x, 0.0))
        if n.length < 1e-9:
            continue
        n = n.normalized() * h
        k = len(verts)
        verts += [tuple(a + n), tuple(b + n), tuple(b - n), tuple(a - n)]
        faces.append((k, k + 1, k + 2, k + 3))
    return [(v[0], v[1], z) for v in verts], faces


def _text(element, aspect, collection):
    curve = bpy.data.curves.new(f"{element['id']}_text", type="FONT")
    curve.body = element["text"]
    curve.size = float(element.get("size", 0.04)) * CARD_HEIGHT
    curve.align_x = element.get("align", "CENTER")
    curve.align_y = "CENTER"
    obj = bpy.data.objects.new(element["id"], curve)
    obj.location = _card_to_world(element["position"], aspect, Z["text"])
    collection.objects.link(obj)
    return obj


def _arrow(element, aspect, collection):
    a, b = _card_to_world(element["start"], aspect), _card_to_world(element["end"], aspect)
    d = (b - a)
    length = d.length
    w = float(element.get("width", 0.008)) * CARD_HEIGHT
    head = min(length * 0.3, w * 4.5)
    # Local frame: x along the arrow, starting at 0.
    verts = [(0, -w / 2, 0), (length - head, -w / 2, 0), (length - head, w / 2, 0), (0, w / 2, 0),
             (length - head, -w * 1.8, 0), (length, 0, 0), (length - head, w * 1.8, 0)]
    faces = [(0, 1, 2, 3), (4, 5, 6)]
    mesh = bpy.data.meshes.new(f"{element['id']}_mesh")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(element["id"], mesh)
    obj.location = (a.x, a.y, Z["arrow"])
    obj.rotation_euler = (0, 0, math.atan2(d.y, d.x))
    collection.objects.link(obj)
    return obj


def _rect(element, aspect, collection):
    box = element["box"]
    a, b = _card_to_world(box[:2], aspect), _card_to_world(box[2:], aspect)
    z = Z["rect"] + 0.0005 * float(element.get("layer", 0))
    if element.get("color"):
        return _mesh_object(element["id"], [(a.x, a.y, z), (b.x, a.y, z), (b.x, b.y, z), (a.x, b.y, z)],
                            [(0, 1, 2, 3)], collection)
    pts = [[box[0], box[1]], [box[2], box[1]], [box[2], box[3]], [box[0], box[3]]]
    verts, faces = _quads(pts, float(element.get("border_width", 0.004)), aspect, z, closed=True,
                          dash=element.get("dash"))
    return _mesh_object(element["id"], verts, faces, collection)


def _line(element, aspect, collection):
    z = Z["line"] + 0.0005 * float(element.get("layer", 0))
    verts, faces = _quads(element["points"], float(element.get("width", 0.005)), aspect, z,
                          dash=element.get("dash"))
    return _mesh_object(element["id"], verts, faces, collection)


def _circle(element, aspect, collection):
    c = _card_to_world(element["center"], aspect)
    r = float(element.get("radius", 0.01)) * CARD_HEIGHT
    z = Z["circle"] + 0.0005 * float(element.get("layer", 0))
    verts = [(c.x, c.y, z)] + [(c.x + r * math.cos(2 * math.pi * k / 24), c.y + r * math.sin(2 * math.pi * k / 24), z)
                               for k in range(24)]
    faces = [(0, 1 + k, 1 + (k + 1) % 24) for k in range(24)]
    return _mesh_object(element["id"], verts, faces, collection)


def _polygon(element, aspect, collection):
    z = Z["polygon"] + 0.0005 * float(element.get("layer", 0))
    pts = [_card_to_world(p, aspect) for p in element["points"]]
    return _mesh_object(element["id"], [(p.x, p.y, z) for p in pts], [tuple(range(len(pts)))], collection)


def image_box(element, size, aspect):
    """Fitted box (card units) of an image element: the cropped image inside `box`, aspect kept."""
    u0, v0, u1, v1 = element.get("crop", [0.0, 0.0, 1.0, 1.0])
    img_aspect = (size[0] * (u1 - u0)) / max(size[1] * (v1 - v0), 1)
    x0, y0, x1, y1 = element["box"]
    bw, bh = (x1 - x0) * aspect, (y1 - y0)
    if img_aspect > bw / bh:
        w, h = bw, bw / img_aspect
    else:
        w, h = bh * img_aspect, bh
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    return [cx - w / aspect / 2, cy - h / 2, cx + w / aspect / 2, cy + h / 2]


def _image(element, aspect, collection, project_dir):
    path = Path(project_dir) / element["path"]
    image = bpy.data.images.load(str(path), check_existing=True)
    box = image_box(element, image.size, aspect)
    a, b = _card_to_world(box[:2], aspect), _card_to_world(box[2:], aspect)
    u0, v0, u1, v1 = element.get("crop", [0.0, 0.0, 1.0, 1.0])
    z = Z["image"] + 0.0005 * float(element.get("layer", 0))
    obj = _mesh_object(element["id"], [(a.x, a.y, z), (b.x, a.y, z), (b.x, b.y, z), (a.x, b.y, z)], [(0, 1, 2, 3)],
                       collection, uvs=[(u0, v0), (u1, v0), (u1, v1), (u0, v1)])
    obj.data.materials.append(_image_material(f"{element['id']} image", image))
    obj["image_box"] = box
    return obj


def _plate(element, text_obj, aspect, collection, style):
    """Light plate behind a text element, sized from the real text extents."""
    bpy.context.view_layer.update()
    xs = [(text_obj.matrix_world @ Vector(c)).x for c in text_obj.bound_box]
    ys = [(text_obj.matrix_world @ Vector(c)).y for c in text_obj.bound_box]
    size = float(element.get("size", 0.04))
    pad = 0.35 * size * CARD_HEIGHT
    x0, x1 = min(xs) - pad, max(xs) + pad
    cy = text_obj.location.y
    y0, y1 = cy - size * CARD_HEIGHT * 0.52 - pad, cy + size * CARD_HEIGHT * 0.52 + pad
    z = Z["plate"]
    plate = _mesh_object(f"{element['id']}__plate", [(x0, y0, z), (x1, y0, z), (x1, y1, z), (x0, y1, z)],
                         [(0, 1, 2, 3)], collection)
    plate.data.materials.append(_flat_material(f"{element['id']} plate", style["plate"]))
    to_card = lambda x, y: [x / (aspect * CARD_HEIGHT) + 0.5, y / CARD_HEIGHT + 0.5]   # noqa: E731
    pts = [to_card(x0, y0), to_card(x1, y0), to_card(x1, y1), to_card(x0, y1)]
    verts, faces = _quads(pts, style["border_width"], aspect, z - 0.0004, closed=True)
    border = _mesh_object(f"{element['id']}__border", verts, faces, collection)
    border.data.materials.append(_flat_material(f"{element['id']} plate border", style["plate_border"]))
    plate["plate_box"] = pts[0] + pts[2]
    return [plate, border]


def _key_fades(plan, name, appear, disappear, fade, frames):
    f0, f1 = plan.frame(appear), plan.frame(appear + fade)
    if f0 <= 1:
        plan.key(name, motion.TRANSPARENCY, 1, 0.0)
    else:
        plan.key(name, motion.TRANSPARENCY, 1, 1.0)
        plan.key(name, motion.TRANSPARENCY, f0, 1.0, "SMOOTH")
        plan.key(name, motion.TRANSPARENCY, min(f1, frames), 0.0)
    if disappear is not None and plan.frame(disappear) < frames:
        g1 = plan.frame(disappear)
        g0 = max(min(f1, frames), plan.frame(disappear - fade))
        plan.key(name, motion.TRANSPARENCY, g0, 0.0, "SMOOTH")
        plan.key(name, motion.TRANSPARENCY, max(g1, g0 + 1), 1.0)
        plan.key(name, motion.TRANSPARENCY, frames, 1.0)
    else:
        plan.key(name, motion.TRANSPARENCY, frames, 0.0)


def build_card(data, shot, preset_name, scene):
    style, preset = data["style"], data["preset"]
    fps = int(data["project"]["fps"])
    frames = templates.frame_count(shot, fps)
    graphic = shot["graphic"]
    aspect = preset["width"] / preset["height"]
    root = make_collection(f"ASS_{shot['id']}", scene.collection)
    bg = bpy.data.meshes.new("card_bg_mesh")
    s = 2.0
    bg.from_pydata([(-aspect * s, -s, 0), (aspect * s, -s, 0), (aspect * s, s, 0), (-aspect * s, s, 0)], [], [(0, 1, 2, 3)])
    bg.update()
    background = bpy.data.objects.new("card_background", bg)
    background.data.materials.append(_flat_material("Card background", graphic.get("background",
                                                                                   style["background_color"])))
    root.objects.link(background)

    from engine import annotation_layout
    ann = annotation_layout.load_style()
    plate_style = {"plate": ann["colors"]["plate"], "plate_border": ann["colors"]["plate_border"],
                   "border_width": ann["text"]["border"]}
    objects, helpers, plan = {}, {}, motion.Plan(fps, frames)
    fade = float(graphic.get("fade_seconds", 0.4))
    materials = {}
    for element in graphic["elements"]:
        kind = element["kind"]
        if kind == "text":
            obj = _text(element, aspect, root)
        elif kind == "arrow":
            obj = _arrow(element, aspect, root)
        elif kind == "image":
            obj = _image(element, aspect, root, data["dir"])
        else:
            obj = {"rect": _rect, "line": _line, "circle": _circle, "polygon": _polygon}[kind](element, aspect, root)
        if kind != "image":
            color = element.get("color") or (element.get("border") if kind == "rect" else None) or "#3C3A36"
            if color not in materials:
                materials[color] = _flat_material(f"Card colour {color}", color)
            obj.data.materials.append(materials[color])
        obj["ass_transparency"] = 0.0
        obj["card_element"] = element["id"]
        objects[obj.name] = obj
        extra = []
        if kind == "text" and element.get("plate"):
            extra = _plate(element, obj, aspect, root, plate_style)
        if kind == "polygon" and element.get("border"):
            verts, faces = _quads(element["points"], float(element.get("border_width", 0.003)), aspect,
                                  Z["polygon"] + 0.0003 + 0.0005 * float(element.get("layer", 0)), closed=True)
            b = _mesh_object(f"{element['id']}__border", verts, faces, root)
            b.data.materials.append(_flat_material(f"{element['id']} border", element["border"]))
            extra = [b]
        for e in extra:
            e["ass_transparency"] = 0.0
            e["card_element"] = element["id"]
        helpers[element["id"]] = extra
        appear = float(element.get("appear", 0.0))
        disappear = element.get("disappear")
        for o in [obj] + extra:
            _key_fades(plan, o.name, appear, float(disappear) if disappear is not None else None, fade, frames)
        drift = element.get("drift")
        if drift:   # slow pan of an image (or any element) while it is shown
            start = obj.location.copy()
            end = start + Vector((drift[0] * aspect * CARD_HEIGHT, drift[1] * CARD_HEIGHT, 0.0))
            f0 = max(1, plan.frame(appear))
            f1 = plan.frame(float(disappear)) if disappear is not None else frames
            plan.key(obj.name, motion.LOC, f0, tuple(start), "LINEAR")
            plan.key(obj.name, motion.LOC, max(f1, f0 + 1), tuple(end))
            if f0 > 1:
                plan.key(obj.name, motion.LOC, 1, tuple(start), "CONSTANT")
            if f1 < frames:
                plan.key(obj.name, motion.LOC, frames, tuple(end))
    plan.markers["middle"] = (frames + 1) // 2

    cam_data = bpy.data.cameras.new("Card camera")
    cam_data.type = "ORTHO"
    cam_data.ortho_scale = aspect * CARD_HEIGHT
    camera = bpy.data.objects.new("Camera_CARD", cam_data)
    camera.location = (0, 0, 5)
    root.objects.link(camera)
    scene.camera = camera
    world = bpy.data.worlds.new("Card world")
    scene.world = world

    render_objects = dict(objects, **{camera.name: camera, background.name: background})
    for extra in helpers.values():
        for o in extra:
            render_objects[o.name] = o
    animate.apply_plan(plan, render_objects)
    card_style = dict(style, color_management={"view_transform": "Standard", "look": "None", "exposure": 0.0})
    scene_mod.configure_render(scene, preset, fps, frames, card_style)
    scene.frame_set(1)
    return CardContext(shot=shot, cfg={"template": "CARD"}, scene=scene, plan=plan, fps=fps,
                       frame_count=frames, objects=objects, render_objects=render_objects,
                       camera=camera, aspect=aspect, helpers=helpers)
