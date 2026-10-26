"""Lighting, material and camera for visual consistency."""
import math
import bpy
from mathutils import Vector
from engine.geometry import make_collection


def hex_to_rgba(color):
    text = color.lstrip("#")
    if len(text) != 6:
        raise ValueError(f"Expected #RRGGBB: {color}")
    rgb = tuple(int(text[i:i+2], 16)/255.0 for i in (0, 2, 4))
    # Convert sRGB HEX into linear Blender scene RGB to preserve chosen palette.
    def to_linear(v):
        return v / 12.92 if v <= 0.04045 else ((v + 0.055)/1.055)**2.4
    return (*[to_linear(v) for v in rgb], 1.0)


def make_material(name, color, roughness=0.72, metallic=0.0):
    material = bpy.data.materials.new(name)
    material.use_nodes = True
    bsdf = material.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = hex_to_rgba(color)
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    material.diffuse_color = hex_to_rgba(color)
    return material


def make_materials(style):
    p = style["palette"]
    return {
        "ground": make_material("Ground", p["ground"]),
        "stone": make_material("Foundation stone", p["limestone"]),
        "plaster": make_material("Warm plaster", p["plaster"]),
        "wood": make_material("Wood", p["wood"]),
        "window": make_material("Stylized glass", "#6B9AA5", roughness=0.27),
        "metal": make_material("Metal detail", "#7C7C78", roughness=0.35, metallic=0.55),
        "roof_variant_a": make_material("Roof A graphite", p["roof_variant_a"]),
        "roof_variant_b": make_material("Roof B terracotta", p["roof_variant_b"]),
    }


def build_camera_and_lights(style):
    col = make_collection("90_CAMERA_LIGHTS")
    camera_data = bpy.data.cameras.new("Locked 3-4 Orthographic")
    camera = bpy.data.objects.new("Camera_3_4_LOCKED", camera_data)
    col.objects.link(camera)
    camera.location = (7.7, -9.9, 7.5)
    target = Vector((0, 0, 1.6))
    direction = target - camera.location
    camera.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
    camera_data.type = "ORTHO"
    camera_data.ortho_scale = 10.1
    bpy.context.scene.camera = camera

    def area(name, loc, power, size):
        light_data = bpy.data.lights.new(name, type="AREA")
        light_data.energy = power
        light_data.shape = "DISK"
        light_data.size = size
        obj = bpy.data.objects.new(name, light_data)
        col.objects.link(obj)
        obj.location = loc
        obj.rotation_euler = (target - obj.location).to_track_quat("-Z", "Y").to_euler()
    area("Key softbox", (0, -6, 9), 1300, 7)
    area("Fill softbox", (5, 3, 6), 750, 6)

    world = bpy.data.worlds.new("Soft neutral world")
    world.use_nodes = True
    bg = world.node_tree.nodes.get("Background")
    bg.inputs["Color"].default_value = hex_to_rgba(style["background_color"])
    bg.inputs["Strength"].default_value = 0.6
    bpy.context.scene.world = world


def configure_render(preset, project):
    scene = bpy.context.scene
    engine = preset.get("engine", "EEVEE")
    if engine == "EEVEE":
        # Blender 5.0 renamed the identifier. 4.5 uses BLENDER_EEVEE_NEXT.
        scene.render.engine = "BLENDER_EEVEE" if bpy.app.version >= (5, 0, 0) else "BLENDER_EEVEE_NEXT"
    else:
        scene.render.engine = engine
    scene.render.resolution_x = int(preset["width"])
    scene.render.resolution_y = int(preset["height"])
    scene.render.resolution_percentage = 100
    scene.render.fps = int(project["fps"])
    scene.frame_start = 1
    scene.frame_end = round(float(project["duration_seconds"])*int(project["fps"]))
    scene.render.film_transparent = False
    if hasattr(scene.render.image_settings, "media_type"):
        scene.render.image_settings.media_type = "IMAGE"
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGBA"
    scene.render.image_settings.color_depth = "8"
    try:
        scene.view_settings.view_transform = "AgX"
    except Exception:
        pass
    scene.render.use_file_extension = True
