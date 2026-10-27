"""Blender objects from semantic components (bpy).

- One object per component, named by its stable id, tagged like every other model
  part (engine.geometry.annotate) plus semantic_type / material_key / mesh_signature.
- Components with identical local meshes and material share ONE mesh datablock
  (repeated voussoirs, bents, spans): instancing without realising anything.
- Bevels are modifiers (non-destructive); geometry stays regenerable from the spec.
- Objects are linked into one sub-collection per semantic group.
"""
import math

import bmesh
import bpy

from engine import geometry
from engine.arch import semantic

BEVEL_ANGLE = math.radians(35.0)   # curved facets (arches) stay unbevelled


def _mesh(comp, material, name):
    bm = bmesh.new()
    verts = [bm.verts.new(v) for v in comp.mesh["verts"]]
    for f in comp.mesh["faces"]:
        try:
            bm.faces.new([verts[i] for i in f])
        except ValueError:      # duplicate face: a generator bug, fail loudly
            bm.free()
            raise ValueError(f"{comp.id}: duplicate or degenerate face {f}")
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    mesh = bpy.data.meshes.new(name)
    bm.to_mesh(mesh)
    bm.free()
    mesh.materials.append(material)
    if comp.bevel:
        if hasattr(mesh, "shade_smooth"):
            mesh.shade_smooth()
        else:
            mesh.polygons.foreach_set("use_smooth", [True] * len(mesh.polygons))
    return mesh


def build_components(comps, materials, collection, mesh_cache=None):
    """Create objects for `comps` under `collection`; returns them in order."""
    cache = {} if mesh_cache is None else mesh_cache
    groups = {}
    objs = []
    for c in comps:
        if c.material not in materials:
            raise KeyError(f"{c.id}: material '{c.material}' is not in the material library")
        sig = semantic.mesh_signature(c.mesh, [c.material, c.bevel])
        mesh = cache.get(sig)
        if mesh is None:
            mesh = cache[sig] = _mesh(c, materials[c.material], f"{c.type.lower()}_{sig[:10]}")
        obj = bpy.data.objects.new(c.id, mesh)
        if obj.name != c.id:
            raise ValueError(f"object name collision for '{c.id}'")
        obj.location = c.location
        obj.rotation_euler = c.rotation
        group = c.group or c.type.lower()
        if group not in groups:
            groups[group] = geometry.make_collection(f"{collection.name}:{c.variant}:{group}", collection)
        groups[group].objects.link(obj)
        if c.bevel:
            mod = obj.modifiers.new(name="Soft architectural edge", type="BEVEL")
            mod.width = c.bevel
            mod.segments = 2
            mod.limit_method = "ANGLE"
            mod.angle_limit = BEVEL_ANGLE
            norm = obj.modifiers.new(name="Weighted normals", type="WEIGHTED_NORMAL")
            if hasattr(norm, "keep_sharp"):
                norm.keep_sharp = True
        geometry.annotate(obj, c.id, c.role, c.variant, group=group, layer=c.layer, hint=c.hint)
        obj["semantic_type"] = c.type
        obj["material_key"] = c.material
        obj["animation_roles"] = list(c.animation)
        obj["mesh_signature"] = sig
        if c.evidence:
            obj["evidence"] = c.evidence
        objs.append(obj)
    return objs
