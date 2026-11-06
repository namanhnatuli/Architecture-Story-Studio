"""Blender QA of M6 semantic annotations (bpy; excluded from the render-cache engine hash).

Per annotated shot, in the built scene:
- annotation_objects     every laid-out primitive was built (and nothing else)
- annotation_anchors     each anchor's world point projects onto its stored frame position under
                         the real camera, and a ray from the camera through it reaches one of the
                         anchor's own components first (see-through ghosted parts are skipped)
- annotation_layout      engine/annotation_layout.check with the REAL text widths: safe area,
                         subtitle zone, no overlapping texts, arrows (uniform length, LOAD down,
                         REACTION up), nothing outside the frame; text height >= min_text_px
- annotation_timing      invisible before `appear`, fully visible in the middle of its window,
                         invisible again after `disappear` (evaluated Blender values)
- captions_clear_of_subtitles  narrated projects: model captions stay above the subtitle zone
"""
import bpy
from mathutils import Vector

from engine import annotation_layout as AL, framing, motion


def _frame_xy(ctx, world):
    if ctx.cfg.get("template") == "SEQUENCE":   # the camera moves between views: project with it, at the current frame
        from bpy_extras.object_utils import world_to_camera_view
        c = world_to_camera_view(ctx.scene, ctx.camera, Vector(tuple(world)))
        return (c.x, c.y)
    sc = framing.frame_coords([tuple(world)], ctx.camera_fit, ctx.camera_basis, ctx.aspect)[0]
    return sc


def _first_hit(ctx, world, depsgraph, own):
    """Object hit first by a ray from the camera plane through `world`: the anchor's own
    components count even when ghosted; other see-through parts, annotations and captions
    are passed through."""
    fwd = Vector(ctx.camera_basis[2])
    origin = Vector(world) - fwd * 40.0
    for _ in range(12):
        hit, loc, _n, _i, obj, _m = ctx.scene.ray_cast(depsgraph, origin, fwd, distance=200.0)
        if not hit:
            return None
        if obj.name in own and not obj.hide_render:
            return obj
        if obj.hide_render or float(obj.get("ass_transparency", 0.0)) >= 0.5 \
                or obj.get("annotation_id") or obj.get("label_for"):
            origin = loc + fwd * 1e-3
            continue
        return obj
    return None


def check(ctx, report, project, preset):
    sid = ctx.shot["id"]
    data = ctx.shot.get("annotations") or {}
    style = AL.load_style()
    # M6 narrated shots: planned against locked audio (subtitles at the bottom of the frame)
    narrated = (project.get("production_profile") or "") != "TECHNICAL_SILENT_PREVIEW" and \
        (ctx.shot.get("editorial") or {}).get("timing_mode") == "AUDIO_LOCKED"
    if ctx.labels and narrated:
        ctx.scene.frame_set(1)
        dg = bpy.context.evaluated_depsgraph_get()
        low = []
        for slot_id, label in ctx.labels.items():
            ys = [_frame_xy(ctx, label.matrix_world @ Vector(c))[1] for c in label.evaluated_get(dg).bound_box]
            if min(ys) < style["subtitle_zone"]:
                low.append(f"{slot_id} caption bottom {min(ys):.3f}")
        report.add(sid, "captions_clear_of_subtitles", not low, "; ".join(low) or
                   f"{len(ctx.labels)} caption(s) above the subtitle zone ({style['subtitle_zone']})")
    if not data:
        return
    items = data["items"]
    built = ctx.annotations or {}

    # objects
    problems = []
    for a in items:
        n_el = len(a["elements"]) + sum(1 for e in a["elements"] if e["kind"] == "plate")   # + plate borders
        got = len(built.get(a["id"], []))
        if got != n_el:
            problems.append(f"{a['id']}: {got} objects for {n_el} primitives")
    extra = sorted(set(built) - {a["id"] for a in items})
    if extra:
        problems.append(f"objects for unknown annotations {extra}")
    report.add(sid, "annotation_objects", not problems, "; ".join(problems[:6]) or
               f"{len(items)} annotations, {sum(len(v) for v in built.values())} objects")

    # anchors (projection + ray attachment) at the middle of each display window
    tol = style["qa"]["anchor_tolerance"]
    worst, bad, n = 0.0, [], 0
    names_of = {}
    for name, obj in ctx.objects.items():
        names_of.setdefault(obj["component_id"], set()).add(name)
    for name, twin in (ctx.fade_twins or {}).items():
        names_of.setdefault(ctx.objects[name]["component_id"], set()).add(twin.name)
    for a in items:
        if not a["anchors"]:
            continue
        f = max(1, min(ctx.frame_count, int(round((a["appear"] + a["disappear"]) / 2 * ctx.fps)) + 1))
        ctx.scene.frame_set(f)
        dg = bpy.context.evaluated_depsgraph_get()
        for x in a["anchors"]:
            n += 1
            sx, sy = _frame_xy(ctx, x["world"])
            err = max(abs(sx - x["screen"][0]), abs(sy - x["screen"][1]))
            worst = max(worst, err)
            if err > tol:
                bad.append(f"{a['id']}: projects {err:.4f} away from its stored position")
                continue
            own = set().union(*(names_of.get(c, set()) for c in x["component_ids"]))
            hit = _first_hit(ctx, x["world"], dg, own)
            if hit is None or hit.name not in own:
                bad.append(f"{a['id']} @{f}: ray reaches {hit.name if hit else 'nothing'}, not {sorted(x['component_ids'])[:2]}")
    report.add(sid, "annotation_anchors", not bad, "; ".join(bad[:6]) or
               f"{n} anchors attached to their own components; max projection error {worst:.4f}")

    # layout with real text widths
    ctx.scene.frame_set(1)
    dg = bpy.context.evaluated_depsgraph_get()
    width_of = {}
    for aid, pairs in (ctx.annotation_texts or {}).items():
        for k, (obj, e) in enumerate(pairs):
            xs = [_frame_xy(ctx, obj.matrix_world @ Vector(c))[0] for c in obj.evaluated_get(dg).bound_box]
            width_of[(aid, k)] = max(xs) - min(xs)
    reserved = [r["box"] for r in data.get("reserved", [])]
    problems = AL.check(items, style, ctx.aspect, text_extent=lambda aid, k: width_of.get((aid, k)),
                        caption_boxes=reserved)
    height = bpy.context.scene.render.resolution_y if False else ctx.scene.render.resolution_y
    px = min((e["size"] * height for a in items for e in a["elements"] if e["kind"] == "text"), default=None)
    if px is not None and px < style["qa"]["min_text_px"] and preset != "preview":
        problems.append(f"smallest text {px:.1f} px < {style['qa']['min_text_px']} px at {preset}")
    report.add(sid, "annotation_layout", not problems, "; ".join(problems[:6]) or
               f"{len(width_of)} texts fit their plates (real widths), safe area and subtitle zone respected, "
               f"arrows uniform; smallest text {px:.1f} px at {preset}" if px else "no text")

    # timing (evaluated transparency)
    bad = []
    for a in items:
        objs = built.get(a["id"], [])
        if not objs:
            continue
        probe = objs[0]
        f_in = int(round(a["appear"] * ctx.fps)) + 1
        f_out = int(round(a["disappear"] * ctx.fps))
        mid = max(1, min(ctx.frame_count, (f_in + f_out) // 2))
        checks = [(mid, 0.0)]
        if f_in > 1:
            checks.append((f_in - 1, 1.0))
        if f_out < ctx.frame_count:
            checks.append((min(ctx.frame_count, f_out + 1), 1.0))
        for f, want in checks:
            ctx.scene.frame_set(f)
            got = float(probe["ass_transparency"])
            if abs(got - want) > 1e-3:
                bad.append(f"{a['id']} @{f}: transparency {got:.3f}, expected {want}")
    report.add(sid, "annotation_timing", not bad, "; ".join(bad[:6]) or
               f"{len(items)} annotations hidden before/after and visible within their windows")
