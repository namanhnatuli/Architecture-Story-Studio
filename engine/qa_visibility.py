"""Level 2 visibility verification in Blender (M5.5; QA only, not a render dependency).

  blender --background --factory-startup --python engine/qa_visibility.py -- --project <dir> --out <json>

For every single-model shot with explanatory targets (storyboard editorial.visibility_targets,
else the highlight components) and at the same evaluation frames as the planner's Level 1
estimate (start, 25/50/75 %, end, every plan marker): orthographic rays on a grid over the
locked camera's frame are cast against the *evaluated* meshes (bevels, seat cuts, real
transforms). A target sample is visible when the first opaque surface hit belongs to it.
Fade twins count as their original; objects at >= 50 % transparency (ghosted) do not occlude.
Per component (pieces), each component's own silhouette is cast separately.
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import bpy  # noqa: E402
from bpy_extras.object_utils import world_to_camera_view  # noqa: E402
from mathutils import Vector  # noqa: E402
from mathutils.bvhtree import BVHTree  # noqa: E402

from engine import shot_builder, templates  # noqa: E402


def _bvh(objs, dg):
    verts, polys, owner = [], [], []
    for obj in objs:
        ev = obj.evaluated_get(dg)
        mesh = ev.to_mesh()
        try:
            base = len(verts)
            verts += [ev.matrix_world @ v.co for v in mesh.vertices]
            for p in mesh.polygons:
                polys.append([base + i for i in p.vertices])
                owner.append(obj.get("fade_twin_of") or obj.name)
        finally:
            ev.to_mesh_clear()
    return BVHTree.FromPolygons(verts, polys), owner


def _opaque(obj):
    return obj.type == "MESH" and not obj.hide_render and float(obj.get("ass_transparency", 0.0)) < 0.5


def evaluation_frames(ctx):
    n = ctx.frame_count
    frames = {"start": 1, "q25": max(1, round(n * 0.25)), "mid": max(1, round(n * 0.5)),
              "q75": max(1, round(n * 0.75)), "end": n}
    for k, f in sorted(ctx.plan.markers.items()):
        if 1 <= f <= n:
            frames[k] = f
    return frames


def measure(ctx, frame, targets, grid, band):
    ctx.scene.frame_set(frame)
    dg = bpy.context.evaluated_depsgraph_get()
    opaque = [o for o in ctx.render_objects.values() if _opaque(o)]
    every, owner = _bvh(opaque, dg)
    cam = ctx.camera
    direction = (cam.matrix_world.to_3x3() @ Vector((0.0, 0.0, -1.0))).normalized()
    corners = [Vector(c) for c in cam.data.view_frame(scene=ctx.scene)]
    x0, x1 = min(c.x for c in corners), max(c.x for c in corners)
    y0, y1 = min(c.y for c in corners), max(c.y for c in corners)
    nx, ny = grid
    origins = [[cam.matrix_world @ Vector((x0 + (i + 0.5) / nx * (x1 - x0), y0 + (j + 0.5) / ny * (y1 - y0), 0.0))
                for i in range(nx)] for j in range(ny)]
    first = [[None] * nx for _ in range(ny)]
    for j in range(ny):
        for i in range(nx):
            idx = every.ray_cast(origins[j][i], direction)[2]
            first[j][i] = owner[idx] if idx is not None else None
    band_rows = int(round(band * ny))
    out = []
    for t in targets:
        names = {templates.object_name(templates.MAIN_SLOT, c) for c in t["component_ids"]}
        shown = [o for o in opaque if (o.get("fade_twin_of") or o.name) in names]
        if not shown:
            out.append({"concept": t["concept"], "shown": False})
            continue
        only, _ = _bvh(shown, dg)
        sil = vis = in_band = core = 0
        occ = {}
        hit = [[False] * nx for _ in range(ny)]
        for j in range(ny):
            for i in range(nx):
                if only.ray_cast(origins[j][i], direction)[2] is None:
                    continue
                sil += 1
                if first[j][i] in names:
                    vis += 1
                    hit[j][i] = True
                    in_band += j < band_rows
                else:
                    occ[first[j][i]] = occ.get(first[j][i], 0) + 1
        for j in range(1, ny - 1):
            for i in range(1, nx - 1):
                if first[j][i] in names and first[j - 1][i] in names and first[j + 1][i] in names and \
                        first[j][i - 1] in names and first[j][i + 1] in names:
                    core += 1
        comps = {}
        if t.get("pieces") and len({o.get("fade_twin_of") or o.name for o in shown}) > 1:
            for name in sorted({o.get("fade_twin_of") or o.name for o in shown}):
                alone, _ = _bvh([o for o in shown if (o.get("fade_twin_of") or o.name) == name], dg)
                s_own = seen = own_core = 0
                for j in range(ny):
                    for i in range(nx):
                        if first[j][i] == name:
                            seen += 1
                        if alone.ray_cast(origins[j][i], direction)[2] is not None:
                            s_own += 1
                for j in range(1, ny - 1):
                    for i in range(1, nx - 1):
                        if first[j][i] == name and first[j - 1][i] == name and first[j + 1][i] == name and \
                                first[j][i - 1] == name and first[j][i + 1] == name:
                            own_core += 1
                cid = ctx.objects[name]["component_id"]
                comps[cid] = {"samples": s_own, "visible_share": round(seen / s_own, 4) if s_own else 0.0,
                              "core_area": round(own_core / (nx * ny), 5)}
        pts = [world_to_camera_view(ctx.scene, cam, Vector(p)) for o in shown for p in shot_builder.world_vertices(o, dg)]
        outside = sum(1 for p in pts if not (0 <= p.x <= 1 and 0 <= p.y <= 1)) / len(pts) if pts else 0.0
        total = nx * ny
        out.append({"concept": t["concept"], "shown": True, "samples": sil, "projected_area": round(sil / total, 5),
                    "visible_area": round(vis / total, 5), "visible_share": round(vis / sil, 4) if sil else 0.0,
                    "core_area": round(core / total, 5), "safe_band_share": round(in_band / vis, 4) if vis else 0.0,
                    "outside_share": round(outside, 4), "geometry": "BLENDER",
                    "occluders": [{"id": ctx.objects[n]["component_id"] if n in ctx.objects else n, "samples": c}
                                  for n, c in sorted(((n, c) for n, c in occ.items() if n is not None),
                                                     key=lambda kv: (-kv[1], kv[0]))[:4]],
                    "components": comps})
    return out


def targets_of(shot):
    ed = shot.get("editorial") or {}
    if ed.get("visibility_targets"):
        return ed["visibility_targets"]
    h = (shot.get("animation") or {}).get("highlight") or {}
    if isinstance(h.get("components"), list):
        return [{"concept": "highlight", "component_ids": h["components"], "pieces": False}]
    return []


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True)
    ap.add_argument("--preset", default="preview")
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    cfg = json.loads((ROOT / "config/visual_planning.json").read_text())["visibility"]
    data = shot_builder.load_project(args.project, args.preset)
    result = {"blender": bpy.app.version_string, "grid": cfg["raster"], "shots": {}}
    for shot in data["story"]["shots"]:
        targets = targets_of(shot)
        if not targets or shot.get("visual_type") == "MOTION_GRAPHICS" or \
                templates.animation_config(shot)["template"] == "SIDE_BY_SIDE":
            continue
        ctx = shot_builder.build_shot(args.project, shot["id"], args.preset)
        frames = evaluation_frames(ctx)
        result["shots"][shot["id"]] = {"frames": frames, "rows": {
            label: measure(ctx, f, targets, cfg["raster"], cfg["subtitle_safe_band"]) for label, f in frames.items()}}
        print(f"[VISIBILITY] {shot['id']}: {len(targets)} target(s) x {len(frames)} frames", flush=True)
    Path(args.out).write_text(json.dumps(result, indent=1))
    print(f"[SUCCESS] measured visibility => {args.out}")


if __name__ == "__main__":
    main()
