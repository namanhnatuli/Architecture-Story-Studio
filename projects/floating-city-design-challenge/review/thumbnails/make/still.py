"""Render one clean still from a shot scene: annotations hidden, optional camera override.
Usage: Blender -b scenes/SC_xxx.blend --python still.py -- spec.json   (one entry of specs.json, "out" made absolute)
spec: {"out": path, "frame": int, "res": [w, h], "cam": null | {"from": [x,y,z], "to": [x,y,z], "lens": mm},
       "bbox": true}  (the .blend on disk is never saved)"""
import bpy, json, sys
from mathutils import Vector

spec = json.loads(open(sys.argv[sys.argv.index("--") + 1]).read())
sc = bpy.context.scene
sc.frame_set(int(spec["frame"]))
for col in bpy.data.collections:
    if col.name.startswith("85_ANNOTATIONS"):
        col.hide_render = True
        for o in col.all_objects:
            o.hide_render = True
for o in sc.objects:
    if o.name.startswith("ANN_"):
        o.hide_render = True
for col in bpy.data.collections:   # whole collections: an object's own hide_render may be animated
    if any(h in col.name for h in spec.get("hide", [])):
        col.hide_render = True
if spec.get("bbox"):
    lo, hi = Vector((1e9,) * 3), Vector((-1e9,) * 3)
    for o in sc.objects:
        if o.type != "MESH" or o.hide_render:
            continue
        name = (o.users_collection[0].name if o.users_collection else "")
        if name.startswith("90_ENVIRONMENT") or "water" in name:
            continue
        for c in o.bound_box:
            w = o.matrix_world @ Vector(c)
            lo = Vector(map(min, lo, w)); hi = Vector(map(max, hi, w))
    print("BBOX", [round(v, 1) for v in lo], [round(v, 1) for v in hi])
    cam = sc.camera
    print("CAM", [round(v, 1) for v in cam.matrix_world.translation], "lens", cam.data.lens, "clip", cam.data.clip_start, cam.data.clip_end)
c = spec.get("cam")
if c:
    data = bpy.data.cameras.new("ThumbCam")
    data.lens = c.get("lens", 35)
    if c.get("ortho"):
        data.type = "ORTHO"
        data.ortho_scale = c["ortho"]
    data.clip_start, data.clip_end = c.get("clip", [1.0, 30000.0])
    cam = bpy.data.objects.new("ThumbCam", data)
    sc.collection.objects.link(cam)
    cam.location = Vector(c["from"])
    d = Vector(c["to"]) - cam.location
    cam.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
    sc.camera = cam
sc.render.resolution_x, sc.render.resolution_y = spec["res"]
sc.render.resolution_percentage = 100
sc.render.image_settings.file_format = "PNG"
if spec.get("transparent"):
    sc.render.film_transparent = True
    sc.render.image_settings.color_mode = "RGBA"
sc.render.filepath = spec["out"]
bpy.ops.render.render(write_still=True)
print("WROTE", spec["out"])
