"""Stand-alone architecture asset scenes (bpy): multi-view previews, geometry QA on
evaluated meshes, reproducibility and build statistics (G4-B/C/E).

Runs headless via engine/render_scene.py --mode asset. No project is needed: the asset
is built on its own site (or the default river crossing) with the project lighting.
"""
import hashlib
import itertools
import json
import time
from pathlib import Path

import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree

from engine import geometry, shot_builder
from engine import scene as scene_mod
from engine.arch import assets, checks, realize, semantic

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SITE = "asset_library/architecture/sites/site_river_crossing_24.json"
VIEWS = {"three_quarter": "BRIDGE_THREE_QUARTER", "elevation": "ELEVATION", "top": "TOP",
         "exploded": "BRIDGE_THREE_QUARTER"}
# Designed interpenetration (framing, embedding); everything else must not overlap.
ALLOWED_INTERSECT = {frozenset(p) for p in (
    ("TRUSS_CHORD", "END_POST"), ("TRUSS_CHORD", "TRUSS_VERTICAL"), ("TRUSS_CHORD", "TRUSS_DIAGONAL"),
    ("END_POST", "TRUSS_DIAGONAL"), ("TRUSS_VERTICAL", "TRUSS_DIAGONAL"), ("TRUSS_CHORD", "FLOOR_BEAM"),
    ("TRUSS_CHORD", "BRACING"), ("END_POST", "FLOOR_BEAM"), ("JOINT", "TRUSS_CHORD"), ("JOINT", "END_POST"),
    ("JOINT", "TRUSS_VERTICAL"), ("JOINT", "TRUSS_DIAGONAL"), ("TRUSS_VERTICAL", "FLOOR_BEAM"),
    ("TRUSS_DIAGONAL", "FLOOR_BEAM"), ("DECK", "FLOOR_BEAM"),
)} | {frozenset(("WATER", t)) for t in semantic.SEMANTIC_TYPES}
CROPPED_VIEWS = ("elevation", "top")
TOUCH = 0.03
PENETRATION = 0.004   # m: a vertex this far inside another closed mesh is an intersection


def _penetration(tree, verts):
    """Deepest vertex of `verts` inside the closed mesh of `tree` (outward normals), metres."""
    deepest = 0.0
    for v in verts:
        loc, normal, _, _ = tree.find_nearest(v)
        if loc is not None:
            d = (v - loc).dot(normal)
            if d < -deepest:
                deepest = -d
    return deepest


def build(asset_path, style, preset, site_path=DEFAULT_SITE, exploded=False):
    """Clean scene with the site + asset. Returns (scene, objects, components, stats)."""
    t0 = time.perf_counter()
    shot_builder.purge_data()
    geometry.reset_mesh_cache()
    scene = bpy.context.scene
    data, _ = assets.load(asset_path)
    root = geometry.make_collection(f"ASSET_{data['asset_id']}", scene.collection)
    materials = scene_mod.make_materials(style)
    scene_mod.build_environment(scene, style, materials, geometry.make_collection("90_ENVIRONMENT", root))
    site = assets.plan_cached(site_path, "shared")
    comps = assets.plan_cached(asset_path, data["variant"])
    objs = realize.build_components(site + comps, materials, geometry.make_collection("00_MODEL", root),
                                    geometry._MESH_CACHE)
    if exploded:
        for cid, off in assets.explode_offsets(data, comps).items():
            obj = bpy.data.objects[cid]
            obj.location = tuple(a + b for a, b in zip(obj.location, off))
    bpy.context.view_layer.update()
    stats = {"build_seconds": round(time.perf_counter() - t0, 3), "objects": len(objs),
             "asset_objects": len(comps), "mesh_datablocks": len({o.data.name for o in objs}),
             "asset_mesh_datablocks": len({bpy.data.objects[c.id].data.name for c in comps})}
    return scene, {o.name: o for o in objs}, comps, stats


def frame_camera(scene, style, preset, view, objs):
    dg = bpy.context.evaluated_depsgraph_get()
    pts = [p for o in objs.values() for p in shot_builder.world_vertices(o, dg)]
    cam_preset = scene_mod.camera_preset(style, VIEWS[view])
    for cam in [o for o in bpy.data.objects if o.type == "CAMERA"]:
        bpy.data.objects.remove(cam)
    camera, fit, basis = scene_mod.build_camera(scene, scene.collection, cam_preset, pts,
                                                preset["width"] / preset["height"])
    scene.render.use_border = scene.render.use_crop_to_border = view in CROPPED_VIEWS
    if view in CROPPED_VIEWS:   # technical views: crop to the model (no empty sky / under-ground bands)
        from engine import framing
        coords = framing.frame_coords(pts, fit, basis, preset["width"] / preset["height"])
        m = 0.06
        xs, ys = [c[0] for c in coords], [c[1] for c in coords]
        scene.render.border_min_x, scene.render.border_max_x = max(0.0, min(xs) - m / 2), min(1.0, max(xs) + m / 2)
        scene.render.border_min_y, scene.render.border_max_y = max(0.0, min(ys) - m), min(1.0, max(ys) + m)
    return camera


def render_views(asset_path, style, preset, out_dir, views=("three_quarter", "elevation", "top", "exploded")):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    results = {}
    for view in views:
        scene, objs, comps, stats = build(asset_path, style, preset, exploded=(view == "exploded"))
        frame_camera(scene, style, preset, view, objs)
        scene_mod.configure_render(scene, preset, 24, 1, style)
        # Elevations look along the horizon: the sky would show the dim world background;
        # render it transparent and let the JPEG export put it on the ground colour.
        scene.render.film_transparent = view == "elevation"
        scene.render.image_settings.color_mode = "RGBA" if view == "elevation" else "RGB"
        if view == "elevation" and "ground" in bpy.data.objects:   # seen edge-on: adds only a horizon line
            bpy.data.objects["ground"].hide_render = True
        scene.frame_set(1)
        target = out_dir / f"{view}.png"
        scene.render.filepath = str(target)
        t0 = time.perf_counter()
        bpy.ops.render.render(write_still=True)
        results[view] = {"file": str(target), "render_seconds": round(time.perf_counter() - t0, 3),
                         "build_seconds": stats["build_seconds"]}
    return results


def _tree(obj, dg):
    ev = obj.evaluated_get(dg)
    mesh = ev.to_mesh()
    verts = [ev.matrix_world @ v.co for v in mesh.vertices]
    polys = [tuple(p.vertices) for p in mesh.polygons]
    ev.to_mesh_clear()
    return BVHTree.FromPolygons(verts, polys), verts


def _aabb(verts):
    return (tuple(min(v[i] for v in verts) for i in range(3)), tuple(max(v[i] for v in verts) for i in range(3)))


def _near(a, b, tol):
    return all(a[0][i] - tol <= b[1][i] and b[0][i] - tol <= a[1][i] for i in range(3))


def geometry_qa(objs):
    """Evaluated-mesh checks: connectivity (BVH distance <= TOUCH) from the ground, and
    intersections between parts that are not designed to interpenetrate."""
    dg = bpy.context.evaluated_depsgraph_get()
    data = {n: _tree(o, dg) for n, o in objs.items() if o.type == "MESH" and n != "ground"}
    boxes = {n: _aabb(v) for n, (_, v) in data.items()}
    types = {n: objs[n].get("semantic_type", "") for n in data}
    adjacency = {n: set() for n in data}
    overlaps = []
    for a, b in itertools.combinations(sorted(data), 2):
        if not _near(boxes[a], boxes[b], TOUCH):
            continue
        ta, tb = data[a][0], data[b][0]
        hit = bool(ta.overlap(tb))
        touching = hit or any(tb.find_nearest(v, TOUCH)[0] is not None for v in data[a][1]) or \
            any(ta.find_nearest(v, TOUCH)[0] is not None for v in data[b][1])
        if touching:
            adjacency[a].add(b)
            adjacency[b].add(a)
        if hit and frozenset((types[a], types[b])) not in ALLOWED_INTERSECT:
            depth = max(_penetration(tb, data[a][1]), _penetration(ta, data[b][1]))
            if depth > PENETRATION:      # coplanar contact also "overlaps" in a BVH; only real penetration counts
                overlaps.append(f"{a} x {b} ({depth * 1000:.0f} mm)")
    roots = [n for n in data if boxes[n][0][2] <= checks.GROUND_Z + TOUCH]
    seen, todo = set(roots), list(roots)
    while todo:
        cur = todo.pop()
        for nb in adjacency[cur] - seen:
            seen.add(nb)
            todo.append(nb)
    floating = sorted(set(data) - seen)
    return [("bvh_connected_to_ground", not floating, f"floating: {floating[:6]}" if floating else
             f"{len(data)} objects reach the ground through touching evaluated meshes (tolerance {TOUCH} m)"),
            ("bvh_no_unintended_intersections", not overlaps, "; ".join(overlaps[:6]) if overlaps else
             f"no part penetrates another by more than {PENETRATION * 1000:.0f} mm outside the designed "
             f"framing list ({len(ALLOWED_INTERSECT)} allowed type pairs)")]


def signature(objs):
    """Semantic structure + transforms + evaluated geometry, rounded (for build-twice checks)."""
    dg = bpy.context.evaluated_depsgraph_get()
    rows = []
    for n in sorted(objs):
        o = objs[n]
        if o.type != "MESH":
            continue
        verts = shot_builder.world_vertices(o, dg)
        rows.append([n, o.get("semantic_type"), o.get("material_key"), o.get("group"), o.get("assembly_layer"),
                     [round(v, 5) for v in o.location], [round(v, 6) for v in o.rotation_euler],
                     o.get("mesh_signature"), len(verts),
                     hashlib.sha256(json.dumps([[round(c, 4) for c in v] for v in verts]).encode()).hexdigest()])
    return hashlib.sha256(json.dumps(rows).encode()).hexdigest(), rows


def run_qa(asset_path, style, preset):
    """Build twice from a clean state, compare signatures, run BVH checks; returns a report."""
    data, _ = assets.load(asset_path)
    scene, objs, comps, stats1 = build(asset_path, style, preset)
    sig1, rows1 = signature(objs)
    results = geometry_qa(objs)
    dg = bpy.context.evaluated_depsgraph_get()
    stats1["evaluated_verts"] = sum(len(shot_builder.world_vertices(o, dg)) for o in objs.values() if o.type == "MESH")
    scene, objs, comps, stats2 = build(asset_path, style, preset)
    sig2, rows2 = signature(objs)
    diff = [r1[0] for r1, r2 in zip(rows1, rows2) if r1 != r2] + (["(object count)"] if len(rows1) != len(rows2) else [])
    results.append(("reproducible_build", sig1 == sig2, f"sha256 {sig1[:16]} twice" if sig1 == sig2 else f"differs: {diff[:6]}"))
    # semantic tags in Blender match the planned components exactly
    planned = {c.id: (c.type, c.material, c.group or c.type.lower(), c.layer) for c in comps}
    tagged = {n: (o.get("semantic_type"), o.get("material_key"), o.get("group"), o.get("assembly_layer"))
              for n, o in objs.items() if n in planned}
    mism = sorted(n for n in planned if tagged.get(n) != planned[n])
    results.append(("semantic_tags_match_plan", not mism and len(tagged) == len(planned),
                    f"mismatch {mism[:5]}" if mism else f"{len(planned)} objects tagged with type/material/group/layer"))
    return {"asset_id": data["asset_id"], "signature": sig1, "stats": stats1, "rebuild_stats": stats2,
            "results": [{"check": c, "status": "PASS" if ok else "FAIL", "detail": d} for c, ok, d in results]}
