"""Procedural architectural components. Run only inside Blender's embedded Python.

Builders create the parts listed in engine/spec.py and tag every object with
stable metadata (component_id, variant_id, role, group, assembly_layer and an
optional explode_hint). Geometry knows nothing about animation; templates only
read that metadata and the rest transforms.
"""
import math

import bmesh
import bpy
from mathutils import Euler, Matrix, Vector

from engine import spec


def make_collection(name, parent):
    col = bpy.data.collections.new(name)
    parent.children.link(col)
    return col


def annotate(obj, component_id, role, variant_id="shared", group=None, layer=0, hint=None):
    obj["component_id"] = component_id
    obj["variant_id"] = variant_id
    obj["role"] = role
    obj["group"] = group or role
    obj["assembly_layer"] = int(layer)
    if hint is not None:
        obj["explode_hint"] = [float(v) for v in hint]
    # Per-object shader controls read by the materials (engine/scene.py); 0 = normal.
    obj["ass_transparency"] = 0.0
    obj["ass_highlight"] = 0.0
    return obj


def _finish(obj, material, collection, bevel):
    collection.objects.link(obj)
    if material:
        obj.data.materials.append(material)
    if bevel:
        # Smooth + weighted normals: big faces stay flat, bevels catch light (edge highlights).
        if hasattr(obj.data, "shade_smooth"):
            obj.data.shade_smooth()
        else:
            obj.data.polygons.foreach_set("use_smooth", [True] * len(obj.data.polygons))
        mod = obj.modifiers.new(name="Soft architectural edge", type="BEVEL")
        mod.width = bevel
        mod.segments = 2
        norm = obj.modifiers.new(name="Weighted normals", type="WEIGHTED_NORMAL")
        if hasattr(norm, "keep_sharp"):
            norm.keep_sharp = True
    return obj


def box_object(name, boxes, material, collection, location=(0, 0, 0), rotation=(0, 0, 0), bevel=0.015,
               clip_below_z=None):
    """One object made of axis-aligned boxes [(local centre, dimensions)], built without bpy.ops.

    clip_below_z trims everything below that world height and caps the cut, e.g. a
    rafter's seat cut where it bears on the wall top instead of sinking into it.
    """
    bm = bmesh.new()
    for center, dims in boxes:
        bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.LocRotScale(Vector(center), None, Vector(dims)))
    if clip_below_z is not None:
        to_local = Matrix.LocRotScale(Vector(location), Euler(rotation), None).inverted()
        bmesh.ops.bisect_plane(bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:],
                               plane_co=to_local @ Vector((0, 0, clip_below_z)),
                               plane_no=(to_local.to_3x3() @ Vector((0, 0, 1))).normalized(), clear_inner=True)
        bmesh.ops.holes_fill(bm, edges=bm.edges[:], sides=0)
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    mesh = bpy.data.meshes.new(f"{name}_mesh")
    bm.to_mesh(mesh)
    bm.free()
    obj = bpy.data.objects.new(name, mesh)
    obj.location = location
    obj.rotation_euler = rotation
    return _finish(obj, material, collection, bevel)


def triangle_object(name, width, rise, thickness, material, collection, location):
    """Gable infill: triangle (base on z=-rise/3, apex at 2*rise/3) solidified towards +Y."""
    verts = [(-width / 2, 0, -rise / 3), (width / 2, 0, -rise / 3), (0, 0, 2 * rise / 3)]
    mesh = bpy.data.meshes.new(f"{name}_mesh")
    mesh.from_pydata(verts, [], [(0, 1, 2)])
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    obj.location = location
    _finish(obj, material, collection, bevel=0)
    solid = obj.modifiers.new(name="Gable thickness", type="SOLIDIFY")
    solid.thickness = thickness
    return obj


# ---------------------------------------------------------------- base (shared)
def build_rectangular_house_base(params, materials, collection):
    w, d, h = params["width"], params["depth"], params["wall_height"]
    parts = {i: (role, group) for i, role, group in spec.BASE_BUILDERS["rectangular_house_base"]}
    objs = []

    def add(cid, boxes, material, location, bevel=0.015):
        obj = box_object(cid, boxes, material, collection, location=location, bevel=bevel)
        role, group = parts[cid]
        objs.append(annotate(obj, cid, role, group=group))

    add("foundation", [((0, 0, 0), (w + .32, d + .32, .36))], materials["stone"], (0, 0, -0.20))
    add("floor", [((0, 0, 0), (w, d, .10))], materials["wood"], (0, 0, .015))
    for side, x in (("left", -w / 2), ("right", w / 2)):
        add(f"wall_{side}", [((0, 0, 0), (.17, d, h))], materials["plaster"], (x, 0, h / 2))
    for side, y in (("front", -d / 2), ("back", d / 2)):
        add(f"wall_{side}", [((0, 0, 0), (w, .17, h))], materials["plaster"], (0, y, h / 2))
    add("door", [((0, 0, 0), (.83, .065, 1.88))], materials["wood"], (-.8, -d / 2 - .095, .94))
    add("door_handle", [((0, 0, 0), (.075, .04, .075))], materials["metal"], (-.47, -d / 2 - .15, .92))
    for n, x in (("right", 1.05), ("left", -1.82)):
        add(f"window_{n}", [((0, 0, 0), (.66, .06, .79))], materials["window"], (x, -d / 2 - .100, 1.62))
        add(f"window_{n}_frame_h", [((0, 0, 0), (.70, .06, .065))], materials["wood"], (x, -d / 2 - .141, 1.62))
        add(f"window_{n}_frame_v", [((0, 0, 0), (.065, .06, .83))], materials["wood"], (x, -d / 2 - .143, 1.62))
    # Ceiling joists tie the long walls; top flush with the wall top, ends embedded in the walls.
    ys = spec.rafter_positions(d, params["rafter_count"])
    add("ceiling_joists", [((0, y, 0), (w, .06, .12)) for y in ys], materials["wood"], (0, 0, h - .06), bevel=.006)
    return objs


# ---------------------------------------------------------------- gable roof (variant)
COVERING_T = 0.105   # roof covering thickness
RAFTER_T = 0.14      # rafter depth (perpendicular to the slope)
RAFTER_W = 0.06
RIDGE_W, RIDGE_H = 0.12, 0.18


def build_gable_roof(variant, params, materials, collection):
    vid = variant["id"]
    parts = {p["id"]: p for p in spec.variant_parts(variant)}
    w, d, h = params["width"], params["depth"], params["wall_height"]
    a = math.radians(float(variant["roof_pitch_degrees"]))
    run = w / 2 + 0.07
    rise = run * math.tan(a)
    slope_len = run / math.cos(a)
    ys = spec.rafter_positions(d, params["rafter_count"])
    roof_mat = materials[variant["color_key"]]
    objs = []

    def tag(obj, suffix, hint):
        part = parts[f"{vid}_{suffix}"]
        return annotate(obj, part["id"], part["role"], vid, group=part["role"], layer=part.get("layer", 0), hint=hint)

    # Rafter centre line sits just under the covering's underside.
    rafter_off = -COVERING_T / 2 + 0.02 * math.cos(a) - 0.003 - RAFTER_T / 2
    s_start = 0.02
    s_end = (run - 0.065 - RAFTER_T / 2 * math.sin(a) + rafter_off * math.sin(a)) / math.cos(a)
    for side, sign in (("left", -1), ("right", 1)):
        eave_x = sign * run
        sx, sz = -sign * math.cos(a), math.sin(a)   # slope direction, eave -> ridge
        nx, nz = sign * math.sin(a), math.cos(a)     # outward roof normal
        rotation = (0, sign * a, 0)
        center = (eave_x + sx * slope_len / 2, 0, h + sz * slope_len / 2 + 0.02)
        cover = box_object(f"{vid}_covering_{side}", [((0, 0, 0), (slope_len + .12, d + .42, COVERING_T))],
                           roof_mat, collection, location=center, rotation=rotation, bevel=.018)
        objs.append(tag(cover, f"covering_{side}", (nx, 0, nz)))
        s_mid, length = (s_start + s_end) / 2, s_end - s_start
        r_center = (eave_x + sx * s_mid + nx * rafter_off, 0, h + sz * s_mid + nz * rafter_off)
        # Seat cut 1 mm above the wall top: rafters bear on the walls, never sink into them.
        rafters = box_object(f"{vid}_rafters_{side}", [((0, y, 0), (length, RAFTER_W, RAFTER_T)) for y in ys],
                             materials["wood"], collection, location=r_center, rotation=rotation, bevel=.008,
                             clip_below_z=h + 0.001)
        objs.append(tag(rafters, f"rafters_{side}", (nx, 0, nz)))

    # Ridge beam: top touches the covering underside at the beam's edges.
    top = h + (run - RIDGE_W / 2) * math.tan(a) + 0.02 - (COVERING_T / 2) / math.cos(a) - 0.004
    ridge = box_object(f"{vid}_ridge_beam", [((0, 0, 0), (RIDGE_W, d - .32, RIDGE_H))], materials["wood"],
                       collection, location=(0, 0, top - RIDGE_H / 2), bevel=.008)
    objs.append(tag(ridge, "ridge_beam", (0, 0, 1)))

    for side, y, hint in (("front", -d / 2 + .065, (0, -1, 0)), ("back", d / 2 - .065, (0, 1, 0))):
        gable = triangle_object(f"{vid}_gable_{side}", w, rise, 0.06, materials["plaster"], collection,
                                (0, y, h + rise / 3))
        objs.append(tag(gable, f"gable_{side}", hint))
    return objs


BASE_BUILDER_FUNCS = {"rectangular_house_base": build_rectangular_house_base}
VARIANT_BUILDER_FUNCS = {"gable_roof": build_gable_roof}


def build_model(states, materials, collection, variant_ids):
    """Shared base + the given variants. Fails loudly if a builder and the spec disagree."""
    params = spec.base_params(states)
    objs = BASE_BUILDER_FUNCS[params["builder"]](params, materials, collection)
    variants = spec.variant_map(states)
    for vid in variant_ids:
        variant = variants[vid]
        builder = spec.variant_builder(variant)
        if builder not in VARIANT_BUILDER_FUNCS:
            raise ValueError(f"variant {vid}: no Blender builder for '{builder}'")
        objs += VARIANT_BUILDER_FUNCS[builder](variant, params, materials, collection)
    expected = [p["id"] for p in spec.base_parts(states)]
    for vid in variant_ids:
        expected += spec.variant_ids(states, vid)
    built = [o["component_id"] for o in objs]
    missing = sorted(set(expected) - set(built))
    extra = sorted(set(built) - set(expected))
    if missing or extra or len(built) != len(set(built)):
        raise ValueError(f"builders disagree with states.json: missing {missing}, unexpected {extra}")
    return objs
