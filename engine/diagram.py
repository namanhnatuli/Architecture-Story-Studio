"""2D card shots (visual_type MOTION_GRAPHICS): self-made text + arrow schematics (bpy).

Deliberately minimal: elements are text or arrows placed in card units (x, y in
0..1, origin bottom-left), each fading in at its `appear` time. Uses Blender's
built-in font (no external font licence), flat emission colours and the
Standard view transform so colours match the palette. Fades reuse motion.Plan
and animate.apply_plan, so the Blender QA can compare keys like any 3D shot.
"""
import math
from dataclasses import dataclass

import bpy
from mathutils import Vector

from engine import animate, motion, templates
from engine import scene as scene_mod
from engine.geometry import make_collection

CARD_HEIGHT = 1.0  # world units; width = aspect


@dataclass
class CardContext:
    shot: dict
    cfg: dict
    scene: object
    plan: object
    fps: int
    frame_count: int
    objects: dict
    render_objects: dict
    camera: object
    aspect: float


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


def _card_to_world(pt, aspect, z=0.0):
    return Vector(((pt[0] - 0.5) * aspect * CARD_HEIGHT, (pt[1] - 0.5) * CARD_HEIGHT, z))


def _text(element, aspect, collection):
    curve = bpy.data.curves.new(f"{element['id']}_text", type="FONT")
    curve.body = element["text"]
    curve.size = float(element.get("size", 0.04)) * CARD_HEIGHT
    curve.align_x = element.get("align", "CENTER")
    curve.align_y = "CENTER"
    obj = bpy.data.objects.new(element["id"], curve)
    obj.location = _card_to_world(element["position"], aspect, 0.01)
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
    obj.location = (a.x, a.y, 0.01)
    obj.rotation_euler = (0, 0, math.atan2(d.y, d.x))
    collection.objects.link(obj)
    return obj


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
    background.data.materials.append(_flat_material("Card background", style["background_color"]))
    root.objects.link(background)

    objects, plan = {}, motion.Plan(fps, frames)
    fade = float(graphic.get("fade_seconds", 0.4))
    for element in graphic["elements"]:
        obj = (_text if element["kind"] == "text" else _arrow)(element, aspect, root)
        obj.data.materials.append(_flat_material(f"{element['id']} colour", element.get("color", "#3C3A36")))
        obj["ass_transparency"] = 0.0
        objects[obj.name] = obj
        appear = float(element.get("appear", 0.0))
        f0, f1 = plan.frame(appear), plan.frame(appear + fade)
        if f0 <= 1:
            plan.key(obj.name, motion.TRANSPARENCY, 1, 0.0)
        else:
            plan.key(obj.name, motion.TRANSPARENCY, 1, 1.0)
            plan.key(obj.name, motion.TRANSPARENCY, f0, 1.0, "SMOOTH")
            plan.key(obj.name, motion.TRANSPARENCY, min(f1, frames), 0.0)
        plan.key(obj.name, motion.TRANSPARENCY, frames, 0.0)
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

    animate.apply_plan(plan, objects)
    card_style = dict(style, color_management={"view_transform": "Standard", "look": "None", "exposure": 0.0})
    scene_mod.configure_render(scene, preset, fps, frames, card_style)
    scene.frame_set(1)
    render_objects = dict(objects, **{camera.name: camera, background.name: background})
    return CardContext(shot=shot, cfg={"template": "CARD"}, scene=scene, plan=plan, fps=fps,
                       frame_count=frames, objects=objects, render_objects=render_objects,
                       camera=camera, aspect=aspect)
