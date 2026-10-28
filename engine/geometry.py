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

from engine import house_layout, spec


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


def cylinder_object(name, radius, length, material, collection, location, segments=20, bevel=0.0):
    """Cylinder along the Y axis (ridge rolls, half-round ridge tiles)."""
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=segments, radius1=radius,
                          radius2=radius, depth=length, matrix=Matrix.Rotation(math.pi / 2, 4, "X"))
    mesh = bpy.data.meshes.new(f"{name}_mesh")
    bm.to_mesh(mesh)
    bm.free()
    obj = bpy.data.objects.new(name, mesh)
    obj.location = location
    _finish(obj, material, collection, bevel)
    if hasattr(obj.data, "shade_smooth"):
        obj.data.shade_smooth()
    return obj


def v_ridge_object(name, width, height, length, material, collection, location):
    """'V'-shaped ridge tile: a triangular prism along Y, apex up."""
    verts = []
    for y in (-length / 2, length / 2):
        verts += [(-width / 2, y, 0.0), (width / 2, y, 0.0), (0.0, y, height)]
    faces = [(0, 1, 2), (5, 4, 3), (0, 3, 4, 1), (1, 4, 5, 2), (2, 5, 3, 0)]
    mesh = bpy.data.meshes.new(f"{name}_mesh")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    obj.location = location
    return _finish(obj, material, collection, bevel=0.006)


# ---------------------------------------------------------------- base (shared)
def _box_part(part, material, collection):
    return box_object(part["id"], part["boxes"], material, collection, location=part["location"],
                      rotation=part["rotation"], bevel=part["bevel"], clip_below_z=part.get("clip_below_z"))


def build_rectangular_house_base(params, materials, collection):
    """Shared house base from engine/house_layout.py (numbers shared with the offline proxy)."""
    parts = {i: (role, group) for i, role, group in spec.BASE_BUILDERS["rectangular_house_base"]}
    objs = []
    for part in house_layout.house_base_layout(params):
        obj = _box_part(part, materials[part["material"]], collection)
        role, group = parts[part["id"]]
        objs.append(annotate(obj, part["id"], role, group=group))
    return objs


# ---------------------------------------------------------------- gable roof (variant)
COVERING_STYLES = house_layout.COVERING_STYLES   # re-exported (engine/scene.py documents unit sizes)


def build_gable_roof(variant, params, materials, collection):
    """One gable roof variant from engine/house_layout.py."""
    vid = variant["id"]
    parts = {p["id"]: p for p in spec.variant_parts(variant)}
    roof_mat = materials[variant["color_key"]]
    objs = []
    for part in house_layout.gable_roof_layout(variant, params):
        material = roof_mat if part["material"] == "roof" else materials[part["material"]]
        kind = part["kind"]
        if kind == "boxes":
            obj = _box_part(part, material, collection)
            if "course_origin" in part:   # local x of the eave edge: shader course joints start here
                obj["ass_course_origin"] = part["course_origin"]
        elif kind == "triangle":
            obj = triangle_object(part["id"], part["width"], part["rise"], part["thickness"], material, collection,
                                  part["location"])
        elif kind == "gable":
            obj = gable_object(part["id"], part["outline"], part["thickness"], material, collection,
                               part["location"][1])
        elif kind == "v_ridge":
            obj = v_ridge_object(part["id"], part["width"], part["height"], part["length"], material, collection,
                                 part["location"])
        else:
            obj = cylinder_object(part["id"], part["radius"], part["length"], material, collection, part["location"],
                                  segments=part["segments"], bevel=part["bevel"])
        p = parts[part["id"]]
        objs.append(annotate(obj, p["id"], p["role"], vid, group=p["role"], layer=p.get("layer", 0), hint=part["hint"]))
    return objs


def gable_object(name, outline, thickness, material, collection, y):
    """Gable infill (house_layout.gable_outline) solidified towards +Y."""
    mesh = bpy.data.meshes.new(f"{name}_mesh")
    mesh.from_pydata([(x, 0.0, z) for x, z in outline], [], [tuple(range(len(outline)))])
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    obj.location = (0.0, y, 0.0)
    _finish(obj, material, collection, bevel=0)
    solid = obj.modifiers.new(name="Gable thickness", type="SOLIDIFY")
    solid.thickness = thickness
    return obj


def build_asset_base(params, materials, collection):
    """M4: shared site from an architecture asset spec (engine/arch)."""
    from engine.arch import assets, realize
    return realize.build_components(assets.plan_cached(params["asset"], "shared"), materials, collection,
                                    _MESH_CACHE)


def build_asset_variant(variant, params, materials, collection):
    """M4: a variant from an architecture asset spec; with structure_from only its
    replaceable parts (the rest is inherited from the source variant)."""
    from engine.arch import assets, realize
    keep = {p["id"] for p in spec.builder_parts(variant)}
    comps = [c for c in assets.plan_cached(variant["asset"], variant["id"]) if c.id in keep]
    return realize.build_components(comps, materials, collection, _MESH_CACHE)


_MESH_CACHE = {}   # mesh signature -> bpy mesh; shared across the slots of one shot, reset per scene


def reset_mesh_cache():
    _MESH_CACHE.clear()


BASE_BUILDER_FUNCS = {"rectangular_house_base": build_rectangular_house_base, spec.ASSET_BUILDER: build_asset_base}
VARIANT_BUILDER_FUNCS = {"gable_roof": build_gable_roof, spec.ASSET_BUILDER: build_asset_variant,
                         "none": lambda variant, params, materials, collection: []}


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
