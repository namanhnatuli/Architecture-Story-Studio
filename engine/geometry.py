"""Procedural house geometry. Run only inside Blender's embedded Python."""
import math
import bpy


def make_collection(name):
    col = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(col)
    return col


def put_in_collection(obj, collection):
    for old in list(obj.users_collection):
        old.objects.unlink(obj)
    collection.objects.link(obj)


def annotate(obj, component_id, role, variant_id="shared"):
    obj["component_id"] = component_id
    obj["variant_id"] = variant_id
    obj["role"] = role
    return obj


def cube(name, location, dimensions, material, collection, component_id, role, variant_id="shared", bevel=0.015):
    bpy.ops.mesh.primitive_cube_add(size=1, location=location)
    obj = bpy.context.object
    obj.name = name
    # Cube geometry dimension is set by edit-free object scale to support keyed movement.
    obj.dimensions = dimensions
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if material:
        obj.data.materials.append(material)
    if bevel:
        mod = obj.modifiers.new(name="Soft architectural edge", type="BEVEL")
        mod.width = bevel
        mod.segments = 2
        norm = obj.modifiers.new(name="Weighted normals", type="WEIGHTED_NORMAL")
        if hasattr(norm, "keep_sharp"):
            norm.keep_sharp = True
    put_in_collection(obj, collection)
    return annotate(obj, component_id, role, variant_id)


def triangular_gable(name, y, width, z_base, rise, material, collection, variant_id):
    verts = [(-width/2, y, z_base), (width/2, y, z_base), (0, y, z_base + rise)]
    mesh = bpy.data.meshes.new(f"{name}_mesh")
    mesh.from_pydata(verts, [], [(0, 1, 2)])
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    collection.objects.link(obj)
    obj.data.materials.append(material)
    solid = obj.modifiers.new(name="Gable thickness", type="SOLIDIFY")
    solid.thickness = 0.06
    return annotate(obj, name, "roof_gable", variant_id)


def build_base(materials):
    shared = make_collection("00_SHARED")
    w, d, h = 4.6, 3.2, 2.55
    objs = []
    objs.append(cube("ground", (0, 0, -0.52), (14, 13, .18), materials["ground"], shared, "ground", "terrain", bevel=0.05))
    objs.append(cube("foundation", (0, 0, -0.20), (w+.32, d+.32, .36), materials["stone"], shared, "foundation", "foundation"))
    objs.append(cube("floor", (0, 0, .015), (w, d, .10), materials["wood"], shared, "floor", "floor"))
    for side, x in [("left", -w/2), ("right", w/2)]:
        objs.append(cube(f"wall_{side}", (x, 0, h/2), (.17, d, h), materials["plaster"], shared, f"wall_{side}", "wall"))
    for side, y in [("front", -d/2), ("back", d/2)]:
        objs.append(cube(f"wall_{side}", (0, y, h/2), (w, .17, h), materials["plaster"], shared, f"wall_{side}", "wall"))
    objs.append(cube("door", (-.8, -d/2-.095, .94), (.83, .065, 1.88), materials["wood"], shared, "door", "door"))
    objs.append(cube("door_handle", (-.47, -d/2-.15, .92), (.075, .04, .075), materials["metal"], shared, "door_handle", "detail"))
    # Fixed windows: left/right of door on the front elevation.
    for n, x in [("right", 1.05), ("left", -1.82)]:
        objs.append(cube(f"window_{n}", (x, -d/2-.100, 1.62), (.66, .06, .79), materials["window"], shared, f"window_{n}", "window"))
        objs.append(cube(f"window_{n}_frame_h", (x, -d/2-.141, 1.62), (.70, .06, .065), materials["wood"], shared, f"window_{n}_frame_h", "detail"))
        objs.append(cube(f"window_{n}_frame_v", (x, -d/2-.143, 1.62), (.065, .06, .83), materials["wood"], shared, f"window_{n}_frame_v", "detail"))
    return {"width": w, "depth": d, "wall_height": h}, objs


def build_roof(variant, dims, materials):
    variant_id = variant["id"]
    collection = make_collection(f"10_{variant_id.upper()}")
    width, depth, wall_height = dims["width"], dims["depth"], dims["wall_height"]
    angle = math.radians(float(variant["roof_pitch_degrees"]))
    run = width/2 + 0.07
    rise = run * math.tan(angle)
    slope_length = run / math.cos(angle)
    roof_mat = materials[variant["color_key"]]
    objs = []
    for side, sign in [("left", -1), ("right", 1)]:
        x = sign * run/2
        z = wall_height + rise/2 + .02
        obj = cube(f"{variant_id}_{side}_panel", (x, 0, z),
                   (slope_length+.12, depth+.42, .105), roof_mat, collection,
                   f"{variant_id}_{side}_panel", "roof_panel", variant_id, bevel=.018)
        obj.rotation_euler[1] = sign * angle
        objs.append(obj)
    for side, y in [("front", -depth/2+.065), ("back", depth/2-.065)]:
        gable = triangular_gable(f"{variant_id}_{side}_gable", y, width, wall_height, rise,
                                 materials["plaster"], collection, variant_id)
        objs.append(gable)
    return objs
