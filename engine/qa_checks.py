"""Blender-side QA for transformation templates (bpy). Run headless:

  python3 tools/cli.py check-blender

Every check reads evaluated Blender data after scene.frame_set(); nothing is
assumed from the plan alone. Local (parent-space) values are compared with the
plan, world-space matrices with layout/framing expectations.
"""
import hashlib
import itertools
import math

import bpy
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector
from mathutils.bvhtree import BVHTree

from engine import framing, motion, shot_builder, spec, templates

TOL = 1e-4            # plan vs evaluated keyframe values
TRANSFORM_TOL = 1e-5  # exact landings / shared parts staying put
FRAME_MARGIN = 0.01   # opaque geometry must stay at least 1% inside the frame
STRUCTURAL_ROLES = {"rafters", "ridge_beam"}  # members that must not pass through shared parts at rest
HIGHLIGHT_MIN_VISIBLE = 0.25   # share of a highlighted set's silhouette not hidden behind other opaque parts
HIGHLIGHT_MIN_FRAME = 0.003    # and visible area as a share of the frame
HIGHLIGHT_MIN_CORE = 0.002     # or a compact visible face (config/visual_planning.json visibility.min_core_area)
RAY_GRID = (192, 108)          # one orthographic ray per 3.3 x 3.3 px at 640 x 360


class Report:
    def __init__(self):
        self.results = []

    def add(self, shot, check, ok, detail=""):
        self.results.append({"shot": shot, "check": check, "status": "PASS" if ok else "FAIL",
                             "detail": detail})
        return ok


def sample_frames(ctx):
    n = ctx.frame_count
    frames = {1, max(1, round(n * .25)), max(1, round(n * .5)), max(1, round(n * .75)), n}
    frames |= {f for f in ctx.plan.markers.values() if 1 <= f <= n}
    for name in ctx.plan.tracks:
        for channel in ctx.plan.channels(name):
            for key in ctx.plan.keys(name, channel):
                frames |= {f for f in (key.frame - 1, key.frame, key.frame + 1) if 1 <= f <= n}
    return sorted(frames)


def _close(a, b, tol):
    return all(abs(x - y) <= tol for x, y in zip(a, b))


def _blender_value(obj, channel):
    if channel == motion.LOC:
        return tuple(obj.location)
    if channel == motion.ROT:
        return tuple(obj.rotation_euler)
    if channel == motion.SCALE:
        return tuple(obj.scale)
    if channel == motion.HIDE:
        return (1.0 if obj.hide_render else 0.0,)
    if channel == motion.ORTHO:
        return (obj.data.ortho_scale,)
    return (float(obj[channel[2:-2]]),)


def _visible(obj):
    return not obj.hide_render and float(obj.get("ass_transparency", 0.0)) < 0.5


def _bvh(obj, depsgraph):
    ev = obj.evaluated_get(depsgraph)
    mesh = ev.to_mesh()
    try:
        verts = [ev.matrix_world @ v.co for v in mesh.vertices]
        polys = [tuple(p.vertices) for p in mesh.polygons]
    finally:
        ev.to_mesh_clear()
    return BVHTree.FromPolygons(verts, polys)


def _combined_bvh(objs, depsgraph):
    """One BVH over several objects (world space) and the owner name of every polygon."""
    verts, polys, owner = [], [], []
    for obj in objs:
        ev = obj.evaluated_get(depsgraph)
        mesh = ev.to_mesh()
        try:
            base = len(verts)
            verts += [ev.matrix_world @ v.co for v in mesh.vertices]
            for p in mesh.polygons:
                polys.append([base + i for i in p.vertices])
                owner.append(obj.name)
        finally:
            ev.to_mesh_clear()
    return BVHTree.FromPolygons(verts, polys), owner


def highlight_visibility(ctx, names, frame, with_core=False):
    """(visible share of the targets' silhouette, visible share of the frame): orthographic
    rays on a grid over the camera frame; a ray counts when the first opaque surface it
    meets belongs to a target. Parts at >= 50 % transparency (ghosted) do not occlude.
    with_core: also the compact visible area (visible rays whose 4 neighbours are visible
    too: not a sliver), the planner/visibility.verdict criterion (M5.5)."""
    ctx.scene.frame_set(frame)
    dg = bpy.context.evaluated_depsgraph_get()
    opaque = [o for o in ctx.render_objects.values() if o.type == "MESH" and _visible(o)]
    targets = [o for o in opaque if o.name in names]
    if not targets:
        return 0.0, 0.0
    every, owner = _combined_bvh(opaque, dg)
    only, _ = _combined_bvh(targets, dg)
    cam = ctx.camera
    direction = (cam.matrix_world.to_3x3() @ Vector((0.0, 0.0, -1.0))).normalized()
    corners = [Vector(c) for c in cam.data.view_frame(scene=ctx.scene)]
    x0, x1 = min(c.x for c in corners), max(c.x for c in corners)
    y0, y1 = min(c.y for c in corners), max(c.y for c in corners)
    nx, ny = RAY_GRID
    silhouette = seen = 0
    grid = set()
    for j in range(ny):
        for i in range(nx):
            origin = cam.matrix_world @ Vector((x0 + (i + 0.5) / nx * (x1 - x0), y0 + (j + 0.5) / ny * (y1 - y0), 0.0))
            if only.ray_cast(origin, direction)[0] is None:
                continue
            silhouette += 1
            idx = every.ray_cast(origin, direction)[2]
            if idx is not None and owner[idx] in names:
                seen += 1
                grid.add((i, j))
    if with_core:
        core = sum(1 for i, j in grid if {(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)} <= grid)
        return seen / max(silhouette, 1), seen / (nx * ny), core / (nx * ny)
    return seen / max(silhouette, 1), seen / (nx * ny)


def _overlaps(objs, depsgraph):
    trees = {o.name: _bvh(o, depsgraph) for o in objs}
    return {tuple(sorted((a, b))) for a, b in itertools.combinations(sorted(trees), 2)
            if trees[a].overlap(trees[b])}


def signature(ctx, frames):
    """Hash of everything that is rendered: world matrices, visibility, shader controls.

    Hidden objects contribute only their hidden flag: Blender leaves matrix_world of
    objects excluded from the depsgraph (hide_viewport) stale, so hashing it would
    measure evaluation history instead of what reaches the image."""
    h = hashlib.sha256()
    for f in frames:
        ctx.scene.frame_set(f)
        for name in sorted(ctx.render_objects):
            obj = ctx.render_objects[name]
            if obj.type not in ("MESH", "FONT"):
                h.update(f"{f}:{name}:{[round(v, 6) for row in obj.matrix_world for v in row]}".encode())
                continue
            if obj.hide_render:
                h.update(f"{f}:{name}:hidden".encode())
                continue
            vals = [round(v, 6) for row in obj.matrix_world for v in row]
            vals += [int(obj.hide_render), round(float(obj.get("ass_transparency", 0.0)), 6),
                     round(float(obj.get("ass_highlight", 0.0)), 6)]
            h.update(f"{f}:{name}:{vals}".encode())
    return h.hexdigest()


def check_shot(ctx, states, report, project=None, preset="preview"):
    sid = ctx.shot["id"]
    template = ctx.cfg["template"]
    frames = sample_frames(ctx)
    plan = ctx.plan
    shared = set(spec.shared_ids(states))

    # 1. Component registration and ownership metadata.
    problems = []
    for slot_id, built, _ in templates.layout_slots(ctx.shot, states):
        expected = {p["id"]: ("shared", p["role"]) for p in spec.base_parts(states)}
        for vid in built:
            expected.update({p["id"]: (vid, p["role"]) for p in spec.variant_parts(spec.variant_map(states)[vid])})
        got = ctx.slots[slot_id]
        if set(got) != set(expected):
            problems.append(f"{slot_id}: missing {sorted(set(expected) - set(got))}, extra {sorted(set(got) - set(expected))}")
        for cid, obj in got.items():
            if cid in expected and (obj["variant_id"], obj["role"]) != expected[cid]:
                problems.append(f"{slot_id}.{cid}: owner/role {(obj['variant_id'], obj['role'])} != {expected[cid]}")
            if obj.parent is not ctx.slot_roots[slot_id]:
                problems.append(f"{slot_id}.{cid}: not parented to its slot root")
    report.add(sid, "components_registered", not problems,
               "; ".join(problems) or f"{sum(len(s) for s in ctx.slots.values())} components, ownership + parenting OK")

    # 2. Blender's evaluated keys equal the pure-Python plan at every sampled frame.
    worst, mismatches = 0.0, []
    rest_world = {}
    for f in frames:
        ctx.scene.frame_set(f)
        for name in plan.tracks:
            obj = ctx.render_objects[name]
            for channel in plan.channels(name):
                want, got = plan.sample(name, channel, f), _blender_value(obj, channel)
                err = max(abs(a - b) for a, b in zip(want, got))
                if channel == motion.HIDE:
                    err = 0.0 if (want[0] > 0.5) == (got[0] > 0.5) else 1.0
                worst = max(worst, err)
                if err > motion.Plan.key_tolerance(want, TOL) and len(mismatches) < 5:
                    mismatches.append(f"{name}{channel}@{f}: plan {want} vs blender {got}")
        if f == 1:
            rest_world = {n: o.matrix_world.copy() for n, o in ctx.objects.items()}
    report.add(sid, "plan_matches_evaluated_keys", not mismatches,
               "; ".join(mismatches) or f"{len(plan.tracks)} animated objects x {len(frames)} frames, max error {worst:.2e}")

    # 3. Everything the template does not animate stays exactly where it was (world space).
    static = [n for n in ctx.objects if n not in plan.tracks]
    moved = []
    for f in frames:
        ctx.scene.frame_set(f)
        for n in static:
            m = ctx.objects[n].matrix_world
            if not all(abs(a - b) <= TRANSFORM_TOL for r1, r2 in zip(m, rest_world[n]) for a, b in zip(r1, r2)):
                moved.append(f"{n}@{f}")
    shared_static = [n for n in static if ctx.objects[n]["component_id"] in shared]
    report.add(sid, "unanimated_parts_static", not moved,
               ", ".join(moved[:5]) or f"{len(static)} objects ({len(shared_static)} shared) unchanged on {len(frames)} frames")

    # 4. No template ever scales a component (v0.1 shrank parts to 1%). The M7 annotation rig of a
    # push-in shot is the one exception: it scales the screen-fixed overlays with the ortho scale
    # (verified separately by overlays_screen_fixed); model parts and the camera are still checked.
    rig = ctx.render_objects.get("ANN_RIG")
    riding = {n for n, o in ctx.render_objects.items() if rig is not None and (o is rig or o.parent is rig)}
    scaled = []
    for f in frames:
        ctx.scene.frame_set(f)
        for n, obj in ctx.render_objects.items():
            if n not in riding and not _close(tuple(obj.matrix_world.to_scale()), (1.0, 1.0, 1.0), TRANSFORM_TOL):
                scaled.append(f"{n}@{f}")
    report.add(sid, "no_scale_change", not scaled, ", ".join(scaled[:5]) or
               "all world scales are 1.0" + (f" ({len(riding)} push-in overlay objects excepted)" if riding else ""))

    # 4b. Structural members at rest bear on the shared structure, never pass through it
    #     (e.g. rafters sinking into the wall tops, visible whenever the covering is off).
    last = ctx.frame_count
    comps = ctx.components
    clashes, tested = set(), 0
    for f in (1, last):
        ctx.scene.frame_set(f)
        dg = bpy.context.evaluated_depsgraph_get()
        at_rest = [o for n, o in ctx.objects.items() if _visible(o)
                   and _close(tuple(o.location), comps[n].location, TRANSFORM_TOL)]
        members = [o for o in at_rest if o["role"] in STRUCTURAL_ROLES and o["variant_id"] != "shared"]
        base = [o for o in at_rest if o["variant_id"] == "shared"]
        tested += len(members)
        if members and base:
            trees = {o.name: _bvh(o, dg) for o in members + base}
            clashes |= {f"{m.name}x{b.name}" for m in members for b in base if trees[m.name].overlap(trees[b.name])}
    report.add(sid, "structure_clear_of_shared_at_rest", not clashes,
               ", ".join(sorted(clashes)) or f"{tested} member checks (roles {sorted(STRUCTURAL_ROLES)}), no intersection with shared parts")

    # 4b. Covering hides the structure: points sampled along every gable edge, and the top
    #     edge vertices of the walls, must have the slot's covering (or ridge cap) straight
    #     above them at rest. Catches thin coverings (slate) letting plaster show through,
    #     which M3 missed.
    pierced, sampled = [], 0
    for f in (1, last):
        ctx.scene.frame_set(f)
        dg = bpy.context.evaluated_depsgraph_get()
        for slot_id, parts in ctx.slots.items():
            at_rest = [o for o in parts.values() if _visible(o)
                       and _close(tuple(o.location), comps[o.name].location, TRANSFORM_TOL)]
            covers = [o for o in at_rest if o["role"] in spec.COVERING_ROLES]
            gables = [o for o in at_rest if o["role"] == "gable_wall"]
            walls = [o for o in at_rest if o["role"] == "wall"]
            if not covers or not (gables or walls):
                continue
            verts, polys = [], []
            for o in covers:
                ev = o.evaluated_get(dg)
                mesh = ev.to_mesh()
                base = len(verts)
                verts += [ev.matrix_world @ v.co for v in mesh.vertices]
                polys += [tuple(base + i for i in poly.vertices) for poly in mesh.polygons]
                ev.to_mesh_clear()
            tree = BVHTree.FromPolygons(verts, polys)
            for g in gables:
                ev = g.evaluated_get(dg)
                mesh = ev.to_mesh()
                pts = [ev.matrix_world @ v.co for v in mesh.vertices]
                for e in mesh.edges:
                    a, b = pts[e.vertices[0]], pts[e.vertices[1]]
                    for k in range(11):
                        q = a.lerp(b, k / 10)
                        sampled += 1
                        hit = tree.ray_cast(q + Vector((0, 0, 1e-5)), Vector((0, 0, 1)), 5.0)
                        if hit[0] is None:
                            pierced.append(f"{g.name}@{f}")
                            break
                ev.to_mesh_clear()
            for wall in walls:  # wall top vertices
                ev = wall.evaluated_get(dg)
                mesh = ev.to_mesh()
                pts = [ev.matrix_world @ v.co for v in mesh.vertices]
                top = max(q.z for q in pts)
                for q in (q for q in pts if q.z > top - 0.03):
                    sampled += 1
                    if tree.ray_cast(q + Vector((0, 0, 1e-5)), Vector((0, 0, 1)), 5.0)[0] is None:
                        pierced.append(f"{wall.name}@{f}")
                        break
                ev.to_mesh_clear()
    report.add(sid, "covering_hides_structure", not pierced,
               ", ".join(sorted(set(pierced))[:6]) or f"{sampled} gable-edge and wall-top samples, all under the covering")

    # 5. Template start/end states.
    if template == "REPLACE_PARTS":
        a, b = templates.replace_states(ctx.shot, ctx.cfg, states)
        out_ids, in_ids = templates.replace_sets(states, a, b)
        out_names = [templates.object_name("main", i) for i in out_ids]
        in_names = [templates.object_name("main", i) for i in in_ids]
        issues = []
        ctx.scene.frame_set(1)
        for n in out_names:
            o = ctx.objects[n]
            if not (_visible(o) and _close(tuple(o.location), comps[n].location, TRANSFORM_TOL)):
                issues.append(f"start: {n} not visible at rest")
        issues += [f"start: {n} visible" for n in in_names if _visible(ctx.objects[n])]
        ctx.scene.frame_set(last)
        for n in in_names:
            o = ctx.objects[n]
            if not (_close(tuple(o.location), comps[n].location, TRANSFORM_TOL)
                    and _close(tuple(o.rotation_euler), comps[n].rotation, TRANSFORM_TOL)):
                issues.append(f"end: {n} not exactly at its rest transform")
            if not _visible(o) or float(o["ass_transparency"]) != 0.0:
                issues.append(f"end: {n} not fully visible")
        issues += [f"end: {n} still rendered" for n in out_names if not ctx.objects[n].hide_render]
        report.add(sid, "replace_start_end_states", not issues, "; ".join(issues) or
                   f"{len(out_names)} parts removed, {len(in_names)} landed exactly (tol {TRANSFORM_TOL})")
    elif template == "EXPLODED_VIEW":
        names = sorted(n for n in plan.tracks if n in ctx.objects)   # model parts (not M6 annotation fades)
        issues = []
        ctx.scene.frame_set(plan.markers["exploded_hold"])
        dists = {n: math.dist(tuple(ctx.objects[n].location), comps[n].location) for n in names}
        issues += [f"{n} did not move at the exploded hold" for n, d in dists.items() if d < 0.05]
        ctx.scene.frame_set(last)
        issues += [f"{n} did not return exactly" for n in names
                   if not _close(tuple(ctx.objects[n].location), comps[n].location, TRANSFORM_TOL)]
        report.add(sid, "exploded_returns_exactly", not issues, "; ".join(issues) or
                   "hold offsets " + ", ".join(f"{n}={d:.2f}m" for n, d in sorted(dists.items())))
        # Explosion must not create intersections that do not already exist at rest.
        dg = bpy.context.evaluated_depsgraph_get()
        ctx.scene.frame_set(1)
        visible = [o for o in ctx.objects.values() if _visible(o)]
        rest_pairs = _overlaps(visible, dg)
        ctx.scene.frame_set(plan.markers["exploded_hold"])
        dg = bpy.context.evaluated_depsgraph_get()
        hold_pairs = {p for p in _overlaps(visible, dg) if p[0] in plan.tracks or p[1] in plan.tracks}
        new = sorted(hold_pairs - rest_pairs)
        report.add(sid, "exploded_no_new_intersections", not new,
                   ", ".join(f"{a}x{b}" for a, b in new) or f"0 new mesh intersections ({len(rest_pairs)} resting contacts ignored)")

    elif template == "SEQUENCE":   # every arriving part lands exactly on its rest transform, fully opaque
        issues, landed = [], 0
        for i, step in enumerate(motion.sequence_steps(ctx.cfg)):
            if step["do"] != "REVEAL":
                continue
            f_landed = plan.markers[f"reveal_{i}_landed"]
            ctx.scene.frame_set(f_landed)
            for cid in step["components"]:
                o = ctx.objects[templates.object_name("main", cid)]
                landed += 1
                # at rest, or where the shot's earlier MOVE steps put the part (a part may arrive on a platform that
                # has already sunk); the plan composes both, motion tests check the composition
                moved = any(st["do"] in motion.TRANSFORM_STEPS and cid in st["components"]
                            for st in motion.sequence_steps(ctx.cfg))
                target = plan.sample(o.name, motion.LOC, f_landed) if moved else comps[o.name].location
                if not (_visible(o) and _close(tuple(o.location), tuple(target), TRANSFORM_TOL)
                        and float(o.get("ass_transparency", 0.0)) == 0.0):
                    issues.append(f"step {i}: {o.name} not landed, opaque and visible")
            before = plan.frame(step["start_seconds"]) - 1   # the frame before its arrival starts
            if before >= 1:
                ctx.scene.frame_set(before)
                issues += [f"step {i}: {cid} visible before it arrives (frame {before})" for cid in step["components"]
                           if _visible(ctx.objects[templates.object_name("main", cid)])]
        report.add(sid, "sequence_arrivals_land", not issues, "; ".join(issues[:5]) or
                   f"{landed} arriving parts land exactly at rest or where the shot's moves put them (tol {TRANSFORM_TOL}), "
                   "unseen before they arrive")

    # 6. Final visibility is exactly the expected design.
    ctx.scene.frame_set(last)
    expected_visible = set()
    for slot_id, _, _ in templates.layout_slots(ctx.shot, states):
        if template == "REPLACE_PARTS":
            final_states = [templates.replace_states(ctx.shot, ctx.cfg, states)[1]]
        else:
            final_states = ctx.visible_variants[slot_id]
        ids = templates.visible_component_ids(states, final_states)
        expected_visible |= {templates.object_name(slot_id, i) for i in ids}
    # A camera below the ground plane hides these parts on purpose (camera preset hide_roles; engine/scene.py).
    expected_visible -= {n for n, o in ctx.objects.items() if o.get("hidden_by_camera")}
    if template == "SEQUENCE":   # parts the sequence fades out stay out (the plan says so, key by key)
        expected_visible -= {n for n in expected_visible if motion.HIDE in plan.channels(n)
                             and plan.sample(n, motion.HIDE, last)[0] > 0.5}
    actual_visible = {n for n, o in ctx.objects.items() if _visible(o)}
    report.add(sid, "final_visibility", actual_visible == expected_visible,
               f"missing {sorted(expected_visible - actual_visible)}, unexpected {sorted(actual_visible - expected_visible)}"
               if actual_visible != expected_visible else f"{len(actual_visible)} visible parts as expected")

    # 7. Framing: opaque geometry inside the frame (and above the label band) on every sampled frame.
    worst_margin, worst_at, bottom_min = 1.0, None, 1.0
    settle = plan.markers.get("intro_end", 1)
    pushing = "camera_move_end" in plan.markers   # M7 push-in: full framing is the first frame
    if template == "SEQUENCE":
        sequence_camera_checks(ctx, report, plan)
    ctx.scene.frame_set(settle)
    cam_matrix, cam_ortho = ctx.camera.matrix_world.copy(), ctx.camera.data.ortho_scale
    cam_moves = []
    for f in ([1] if pushing or template == "SEQUENCE" else frames):
        ctx.scene.frame_set(f)
        dg = bpy.context.evaluated_depsgraph_get()
        if f >= settle and (ctx.camera.matrix_world != cam_matrix or ctx.camera.data.ortho_scale != cam_ortho):
            cam_moves.append(f)
        focus = set(ctx.shot.get("camera_focus") or [])
        if template == "SEQUENCE":   # the opening view frames its focus; ghosts may leave the frame
            focus = set(motion.sequence_views(ctx.cfg)[0]["focus"] or [])
        for n, obj in ctx.render_objects.items():
            if obj.type != "MESH" or not _visible(obj):
                continue
            if template == "SEQUENCE" and (obj.get("annotation_id") or float(obj.get("ass_transparency", 0.0)) >= 0.5
                                           or obj.get("fade_twin_of")):
                continue
            if focus and obj.get("component_id") not in focus:   # close-up: only the framed parts
                continue
            for p in shot_builder.world_vertices(obj, dg):
                c = world_to_camera_view(ctx.scene, ctx.camera, Vector(p))
                m = min(c.x, 1 - c.x, c.y, 1 - c.y)
                if f >= settle:  # label band applies once the camera has settled
                    bottom_min = min(bottom_min, c.y)
                if m < worst_margin:
                    worst_margin, worst_at = m, f"{n}@{f}"
    ok = worst_margin >= FRAME_MARGIN and bottom_min >= ctx.bottom_band - 0.005
    report.add(sid, "camera_framing", ok,
               f"min margin {worst_margin:.3f} at {worst_at}; lowest point y={bottom_min:.3f} "
               f"(label band {ctx.bottom_band:.2f}); ortho_scale {ctx.camera.data.ortho_scale:.3f}")
    if template == "SEQUENCE":
        pass   # camera and overlays: sequence_camera_checks
    elif pushing:   # the move itself is verified key by key (plan_matches_evaluated_keys)
        ctx.scene.frame_set(ctx.frame_count)
        end_ortho = ctx.camera.data.ortho_scale
        ctx.scene.frame_set(1)
        ok_move = end_ortho < ctx.camera.data.ortho_scale and ctx.camera.matrix_world == cam_matrix
        report.add(sid, "camera_locked", ok_move,
                   f"push-in by design: starts on the locked framing, ortho {ctx.camera.data.ortho_scale:.3f} -> "
                   f"{end_ortho:.3f}" if ok_move else "push-in does not start on the locked framing")
        overlays = [o for objs in (ctx.annotations or {}).values() for o in objs]
        if overlays:   # M7: screen-fixed annotations must not drift or grow while the camera pushes in
            def frame_box(f):
                ctx.scene.frame_set(f)
                out = []
                for o in overlays:
                    pts = [world_to_camera_view(ctx.scene, ctx.camera, o.matrix_world @ Vector(c)) for c in o.bound_box]
                    out.append((min(p.x for p in pts), min(p.y for p in pts), max(p.x for p in pts), max(p.y for p in pts)))
                return out
            first, mid, last = frame_box(1), frame_box((ctx.frame_count + 1) // 2), frame_box(ctx.frame_count)
            drift = max(abs(a - b) for boxes in (mid, last) for p, q in zip(first, boxes) for a, b in zip(p, q))
            ctx.scene.frame_set(1)
            report.add(sid, "overlays_screen_fixed", drift < 1e-3,
                       f"{len(overlays)} annotation objects keep their frame position during the push-in "
                       f"(max drift {drift:.1e})" if drift < 1e-3 else f"annotations drift {drift:.4f} of the frame")
    else:
        report.add(sid, "camera_locked", not cam_moves,
                   (f"camera moves only during the intro (frames 1-{settle}), locked afterwards" if settle > 1
                    else "camera never moves") if not cam_moves else f"camera moved after frame {settle}: {cam_moves[:5]}")

    # 7b. Fade twins (blended transparency) render only mid-fade, never together with
    #     their opaque original, and never on the first/last frame (shot cuts).
    if ctx.fade_twins:
        overlap = []
        for f in frames:
            ctx.scene.frame_set(f)
            for name, twin in ctx.fade_twins.items():
                orig = ctx.objects[name]
                # a SEQUENCE ghost held across a cut renders blended on both sides of it (no pop); never with its original
                edge = f in (1, last) and not (template == "SEQUENCE" and _held(plan, name, f))
                if not twin.hide_render and (not orig.hide_render or edge):
                    overlap.append(f"{name}@{f}")
        report.add(sid, "fade_twins_exclusive", not overlap, ", ".join(overlap[:5]) or
                   f"{len(ctx.fade_twins)} twins visible only mid-fade, never with their original or on frames 1/{last}")

    # 7c. Highlighted parts can actually be seen (not hidden under other parts) at the peak
    #     of the glow: HOLD highlight and the exploded hold of EXPLODED_VIEW.
    if template == "SEQUENCE":   # every glow step, at its own peak, in the view the camera is in then
        rows = []
        for i, step in enumerate(motion.sequence_steps(ctx.cfg)):
            if step["do"] != "HIGHLIGHT":
                continue
            names = {templates.object_name(templates.MAIN_SLOT, c) for c in step["components"]}
            f = plan.markers[f"highlight_{i}_peak"]
            share, area, core = highlight_visibility(ctx, names, f, with_core=True)
            ok = (share >= HIGHLIGHT_MIN_VISIBLE or core >= HIGHLIGHT_MIN_CORE) and area >= HIGHLIGHT_MIN_FRAME
            rows.append((ok, f"step {i}@{f}: {share * 100:.0f}% visible, {area * 100:.2f}% of frame"))
        if rows:
            report.add(sid, "highlight_targets_visible", all(ok for ok, _ in rows),
                       "; ".join(d for ok, d in rows if not ok) or "; ".join(d for _, d in rows))
    h = ctx.cfg.get("highlight") or {}
    marker = {"HOLD": "highlight_peak", "EXPLODED_VIEW": "exploded_hold"}.get(template)
    if marker and isinstance(h.get("components"), list) and marker in plan.markers:
        names = {templates.object_name(templates.MAIN_SLOT, i) for i in h["components"]}
        share, area, core = highlight_visibility(ctx, names, plan.markers[marker], with_core=True)
        ghosts = h.get("ghost") or []
        # Same rule as the planner's Level 1 verdict: mostly unhidden, or a compact visible face
        # (an arch ring set in its spandrel shows only its face); a sliver is neither.
        reads = share >= HIGHLIGHT_MIN_VISIBLE or core >= HIGHLIGHT_MIN_CORE
        report.add(sid, "highlight_targets_visible", reads and area >= HIGHLIGHT_MIN_FRAME,
                   f"{share * 100:.0f}% of the highlighted silhouette visible, {area * 100:.2f}% of the frame, compact "
                   f"face {core * 100:.2f}% at frame {plan.markers[marker]}"
                   + (f"; {len(ghosts)} covering part(s) ghosted" if ghosts else "")
                   + ("" if reads else "; mostly hidden: ghost the covering parts, explode, or choose another camera"))

    # 8. The pure-Python framing maths agrees with Blender's projection (settled camera).
    ctx.scene.frame_set(settle)
    probe = [tuple(o.matrix_world.translation) for o in list(ctx.objects.values())[:8]]
    ours = framing.frame_coords(probe, ctx.camera_fit, ctx.camera_basis, ctx.aspect)
    theirs = [tuple(world_to_camera_view(ctx.scene, ctx.camera, Vector(p)))[:2] for p in probe]
    err = max(abs(a - b) for u, v in zip(ours, theirs) for a, b in zip(u, v))
    report.add(sid, "framing_math_matches_blender", err < 1e-5, f"max projection error {err:.2e}")

    # 9. SIDE_BY_SIDE: same scale, local vs world, no overlap.
    if template == "SIDE_BY_SIDE":
        ctx.scene.frame_set(last)  # every slot is shown at the end (an intro fades slots in from hidden)
        slots = list(ctx.slots)
        issues = []
        boxes = {}
        dg = bpy.context.evaluated_depsgraph_get()
        for s in slots:  # rendered parts only: hidden objects are not evaluated (stale matrix_world)
            pts = [p for o in ctx.slots[s].values() if _visible(o) for p in shot_builder.world_vertices(o, dg)]
            boxes[s] = (tuple(min(p[i] for p in pts) for i in range(3)), tuple(max(p[i] for p in pts) for i in range(3)))
        for s1, s2 in itertools.combinations(slots, 2):
            (lo1, hi1), (lo2, hi2) = boxes[s1], boxes[s2]
            if all(lo1[i] < hi2[i] and lo2[i] < hi1[i] for i in range(2)):
                issues.append(f"{s1} and {s2} footprints overlap")
            offset = [b - a for a, b in zip(ctx.slot_offsets[s1], ctx.slot_offsets[s2])]
            for cid in shared:
                o1, o2 = ctx.slots[s1][cid], ctx.slots[s2][cid]
                if not _close([v for r in o1.matrix_basis for v in r], [v for r in o2.matrix_basis for v in r], TRANSFORM_TOL):
                    issues.append(f"{cid}: local transform differs between slots")
                world_delta = [b - a for a, b in zip(o1.matrix_world.translation, o2.matrix_world.translation)]
                if not _close(world_delta, offset, TRANSFORM_TOL):
                    issues.append(f"{cid}: world offset {world_delta} != slot offset {offset}")
                if not _close(tuple(o1.dimensions), tuple(o2.dimensions), TRANSFORM_TOL):
                    issues.append(f"{cid}: dimensions differ between slots")
        gaps = []
        if ctx.cfg.get("layout", "ROW") == "STACK":   # rows on screen: first model on top, never overlapping
            up = ctx.camera_basis[1]
            rows = {s: [sum(c * a for c, a in zip(p, up)) for o in ctx.slots[s].values() if _visible(o)
                        for p in shot_builder.world_vertices(o, dg)] for s in slots}
            gaps = [min(rows[s1]) - max(rows[s2]) for s1, s2 in zip(slots, slots[1:])]
            issues += [f"screen rows overlap by {-g:.3f} m" for g in gaps if g <= 0]
        else:
            for s1, s2 in zip(slots, slots[1:]):
                (lo1, hi1), (lo2, hi2) = boxes[s1], boxes[s2]
                axis = ctx.camera_basis[0]
                span1 = [sum(c * a for c, a in zip(p, axis)) for p in (lo1, hi1, (lo1[0], hi1[1], 0), (hi1[0], lo1[1], 0))]
                span2 = [sum(c * a for c, a in zip(p, axis)) for p in (lo2, hi2, (lo2[0], hi2[1], 0), (hi2[0], lo2[1], 0))]
                gaps.append(min(span2) - max(span1))
            issues += [f"screen-axis gap {g:.3f} m is not positive" for g in gaps if g <= 0]
        report.add(sid, "side_by_side_layout", not issues, "; ".join(issues[:6]) or
                   f"{len(slots)} models, identical shared local transforms and dimensions, gaps "
                   + ", ".join(f"{g:.2f} m" for g in gaps))
    texts = (ctx.cfg.get("labels") if template == "SIDE_BY_SIDE" else
             ({templates.MAIN_SLOT: ctx.cfg["label"]} if template == "HOLD" and ctx.cfg.get("label") else None))
    if ctx.labels:  # captions: right text, inside the label band, under their own model, no overlap
        ctx.scene.frame_set(1)
        dg = bpy.context.evaluated_depsgraph_get()
        issues, spans = [], []
        for slot_id, label in ctx.labels.items():
            if label.data.body != texts[slot_id]:
                issues.append(f"{slot_id}: text {label.data.body!r} differs from the storyboard")
            corners = [world_to_camera_view(ctx.scene, ctx.camera, label.matrix_world @ Vector(c))
                       for c in label.evaluated_get(dg).bound_box]
            xs, ys = [c.x for c in corners], [c.y for c in corners]
            stack = ctx.cfg.get("layout", "ROW") == "STACK"
            top = ctx.cfg.get("label_position") == "TOP"   # M6 narrated: caption at the top of the frame
            if min(xs) < FRAME_MARGIN or max(xs) > 1 - FRAME_MARGIN or min(ys) < 0.005 or max(ys) > 0.995 or \
                    (not stack and not top and max(ys) > ctx.bottom_band) or (top and min(ys) < 0.5):
                issues.append(f"{slot_id}: label box x {min(xs):.3f}-{max(xs):.3f}, y {min(ys):.3f}-{max(ys):.3f} "
                              f"outside the frame/label band {ctx.bottom_band:.2f}")
            for other, parts in ctx.slots.items():   # never on top of a model (any slot)
                pts = [world_to_camera_view(ctx.scene, ctx.camera, Vector(q)) for o in parts.values()
                       if _visible(o) for q in shot_builder.world_vertices(o, dg)]
                if pts and min(xs) < max(q.x for q in pts) and max(xs) > min(q.x for q in pts) and \
                        min(ys) < max(q.y for q in pts) and max(ys) > min(q.y for q in pts):
                    issues.append(f"{slot_id}: label overlaps the {other} model on screen")
            model = [world_to_camera_view(ctx.scene, ctx.camera, Vector(p)).x
                     for o in ctx.slots[slot_id].values() if _visible(o) for p in shot_builder.world_vertices(o, dg)]
            towards_camera = ctx.camera.matrix_world.to_3x3() @ Vector((0, 0, 1))
            for c in label.evaluated_get(dg).bound_box:  # nothing between the caption and the camera
                hit = ctx.scene.ray_cast(dg, label.matrix_world @ Vector(c) + towards_camera * 0.01,
                                         towards_camera, distance=100.0)
                if hit[0]:
                    issues.append(f"{slot_id}: label hidden by {hit[4].name}")
                    break
            centre = (min(xs) + max(xs)) / 2
            if not min(model) <= centre <= max(model):
                issues.append(f"{slot_id}: label centre {centre:.3f} is not under its model")
            spans.append((min(xs), max(xs), min(ys), max(ys), slot_id))
        issues += [f"labels {a[4]} and {b[4]} overlap" for i, a in enumerate(spans) for b in spans[i + 1:]
                   if a[0] < b[1] and b[0] < a[1] and a[2] < b[3] and b[2] < a[3]]
        report.add(sid, "labels_in_band", not issues, "; ".join(issues) or
                   f"{len(ctx.labels)} captions inside the label band, centred under their models, no overlap")
    if ctx.shot.get("annotations") or ctx.cfg.get("label_position") == "TOP" or ctx.labels:
        from engine import qa_annotations   # M6
        qa_annotations.check(ctx, report, project, preset)
    return frames


def check_card(ctx, report):
    """2D card shot: every element built, fades/drifts match the plan, camera static, elements
    visible at the end unless they disappear on purpose, and (M7) the layout: text inside the
    title-safe area and, on narrated (audio-locked) cards, above the subtitle zone."""
    sid = ctx.shot["id"]
    elements = {e["id"]: e for e in ctx.shot["graphic"]["elements"]}
    expected = set(elements)
    built = set(ctx.objects)
    report.add(sid, "card_elements_built", expected == built,
               f"missing {sorted(expected - built)}" if expected != built else f"{len(built)} elements")
    frames = sample_frames(ctx)
    worst, bad = 0.0, []
    cam = ctx.camera.matrix_world.copy()
    moved = False
    for f in frames:
        ctx.scene.frame_set(f)
        moved |= ctx.camera.matrix_world != cam
        for name in ctx.plan.tracks:
            obj = ctx.render_objects[name]
            for channel in ctx.plan.channels(name):
                want, got = ctx.plan.sample(name, channel, f), _blender_value(obj, channel)
                err = max(abs(a - b) for a, b in zip(want, got))
                worst = max(worst, err)
                if err > motion.Plan.key_tolerance(want, TOL) and len(bad) < 5:
                    bad.append(f"{name}{channel}@{f}: plan {want} vs {got}")
    report.add(sid, "plan_matches_evaluated_keys", not bad,
               "; ".join(bad) or f"{len(ctx.plan.tracks)} objects x {len(frames)} frames, max error {worst:.2e}")
    report.add(sid, "camera_locked", not moved, "card camera never moves" if not moved else "card camera moved")
    ctx.scene.frame_set(ctx.frame_count)
    duration = ctx.frame_count / ctx.fps
    hidden = [n for n, o in ctx.objects.items() if float(o["ass_transparency"]) > 1e-6
              and not (elements[n].get("disappear") is not None and float(elements[n]["disappear"]) < duration)]
    lingering = [n for n, o in ctx.objects.items() if elements[n].get("disappear") is not None
                 and float(elements[n]["disappear"]) < duration and float(o["ass_transparency"]) < 1 - 1e-6]
    report.add(sid, "final_visibility", not hidden and not lingering,
               (f"still transparent at the end: {hidden}" if hidden else "") +
               (f" visible after disappearing: {lingering}" if lingering else "") or
               "every lasting element visible on the last frame; disappearing elements gone")
    from engine import annotation_layout
    style = annotation_layout.load_style()
    safe = style["safe_area"]
    narrated = (ctx.shot.get("editorial") or {}).get("timing_mode") == "AUDIO_LOCKED"
    dg = bpy.context.evaluated_depsgraph_get()
    issues = []

    def card_box(obj):
        pts = [obj.matrix_world @ Vector(c) for c in obj.evaluated_get(dg).bound_box]
        xs = [p.x / (ctx.aspect * diagram_height()) + 0.5 for p in pts]
        ys = [p.y / diagram_height() + 0.5 for p in pts]
        return min(xs), min(ys), max(xs), max(ys)
    text_boxes = {}
    for f in sorted({1, ctx.frame_count}):
        ctx.scene.frame_set(f)
        for name, obj in ctx.objects.items():
            e = elements[name]
            x0, y0, x1, y1 = card_box(obj)
            if e["kind"] == "text":
                boxes = [(x0, y0, x1, y1)] + [card_box(h) for h in (ctx.helpers or {}).get(name, [])]
                bx0, by0 = min(b[0] for b in boxes), min(b[1] for b in boxes)
                bx1, by1 = max(b[2] for b in boxes), max(b[3] for b in boxes)
                text_boxes.setdefault(name, []).append((bx0, by0, bx1, by1))
                if bx0 < safe["left"] - 1e-3 or bx1 > safe["right"] + 1e-3 or by1 > safe["top"] + 1e-3 or \
                        by0 < safe["bottom"] - 1e-3:
                    issues.append(f"{name}@{f}: text box x {bx0:.3f}-{bx1:.3f} y {by0:.3f}-{by1:.3f} outside the safe area")
                if narrated and by0 < style["subtitle_zone"] - 1e-3:
                    issues.append(f"{name}@{f}: text bottom {by0:.3f} in the subtitle zone ({style['subtitle_zone']})")
            elif e["kind"] == "image" and not e.get("stage") and (x0 < -1e-3 or x1 > 1 + 1e-3 or y0 < -1e-3 or y1 > 1 + 1e-3):
                issues.append(f"{name}@{f}: image outside the frame ({x0:.3f}, {y0:.3f}, {x1:.3f}, {y1:.3f})")
    # M7: two texts shown at the same time never overlap (plates included)
    def window(e):
        return float(e.get("appear", 0.0)), float(e["disappear"]) if e.get("disappear") is not None else duration
    names = sorted(text_boxes)
    for i, n1 in enumerate(names):
        for n2 in names[i + 1:]:
            (a0, a1), (b0, b1) = window(elements[n1]), window(elements[n2])
            if min(a1, b1) <= max(a0, b0):
                continue
            for p, q in zip(text_boxes[n1], text_boxes[n2]):
                w = min(p[2], q[2]) - max(p[0], q[0])
                h = min(p[3], q[3]) - max(p[1], q[1])
                if w > 2e-3 and h > 2e-3:
                    issues.append(f"texts {n1} and {n2} overlap ({w:.3f} x {h:.3f})")
                    break
    report.add(sid, "card_layout", not issues, "; ".join(issues[:5]) or
               f"{sum(1 for e in elements.values() if e['kind'] == 'text')} texts inside the safe area"
               + (" and above the subtitle zone" if narrated else "") + ", none overlapping; images inside the frame")
    return frames


def diagram_height():
    from engine import diagram
    return diagram.CARD_HEIGHT


def run_all(project_dir, preset="preview", only=None):
    """Blender QA of every shot (only: a list of shot ids, e.g. to check new shots before a long render)."""
    data = shot_builder.load_project(project_dir, preset)
    states = data["states"]
    report = Report()
    cameras, signatures, intros = {}, {}, {}
    for shot in data["story"]["shots"]:
        sid = shot["id"]
        if only and sid not in only:
            continue
        ctx = shot_builder.build_shot(project_dir, sid, preset)
        if shot.get("visual_type", "BLENDER_3D") == "MOTION_GRAPHICS":
            signatures[sid] = (check_card(ctx, report), None)
            signatures[sid] = (signatures[sid][0], signature(ctx, signatures[sid][0]))
            continue
        frames = check_shot(ctx, spec.shot_states(states, shot), report, data["project"], preset)
        ctx.scene.frame_set(1)   # the locked framing (a push-in starts on it)
        if ctx.cfg["template"] != "SIDE_BY_SIDE":
            opening = shot.get("camera_focus") or ((motion.sequence_views(ctx.cfg)[0]["focus"] or ())
                                                    if ctx.cfg["template"] == "SEQUENCE" else ())
            v0 = motion.sequence_views(ctx.cfg)[0] if ctx.cfg["template"] == "SEQUENCE" else {}
            # a SEQUENCE may open on its own view; its clearance (how far the camera stands off) moves the camera too
            turn = tuple(v0.get(k) for k in ("azimuth", "elevation", "margin", "clearance"))
            group = (shot.get("scene_context"), tuple(templates.layout_slots(shot, states)[0][1]), shot.get("camera"),
                     tuple(sorted(opening)), float(shot.get("camera_safe_band", 0.0)), turn)
            cameras[sid] = ([v for r in ctx.camera.matrix_world for v in r], ctx.camera.data.ortho_scale, group)
        elif ctx.camera_keys:
            ctx.scene.frame_set(1)
            m = ctx.camera.matrix_world
            intros[sid] = ([m[r][c] for r in range(3) for c in range(3)], [m[r][3] for r in range(3)],
                           ctx.camera.data.ortho_scale, ctx.slot_offsets[ctx.cfg["intro"]["from_state"]])
        signatures[sid] = (frames, signature(ctx, frames))

    # One locked camera for every single-model shot of a continuity group (same built
    # variants, preset, focus and safe band): cuts between them are invisible.
    groups = {}
    for sid, (m, s, key) in cameras.items():
        groups.setdefault(key, []).append((sid, m, s))
    diffs = [sid for members in groups.values() for sid, m, s in members
             if not (_close(m, members[0][1], 1e-6) and abs(s - members[0][2]) < 1e-6)]
    report.add("ALL", "camera_identical_across_single_model_shots", not diffs,
               f"differs: {diffs}" if diffs else
               f"{len(cameras)} shots in {len(groups)} continuity group(s), one locked camera per group")

    # A SIDE_BY_SIDE intro must open on exactly the single-model framing (seamless cut):
    # the camera of shots that build every variant, without focus or safe band.
    def everything(context):
        return tuple(spec.variant_map(spec.context_view(states, context) if context else states))
    ref_id = next((sid for sid, (m, s, key) in cameras.items()
                   if key[1] == everything(key[0]) and not key[3] and not key[4]),
                  next(iter(cameras), None))
    for sid, (rot, loc, ortho, shift) in intros.items():
        if ref_id is None:
            break
        ref_m, ref_ortho, _ = cameras[ref_id]
        ref_rot = [ref_m[r * 4 + c] for r in range(3) for c in range(3)]
        ref_loc = [ref_m[r * 4 + 3] for r in range(3)]
        ok = (_close(rot, ref_rot, 1e-6) and abs(ortho - ref_ortho) < 1e-6
              and _close([a - b for a, b in zip(loc, shift)], ref_loc, 1e-5))
        report.add(sid, "intro_matches_single_model_camera", ok,
                   f"frame 1 ortho {ortho:.4f} vs {ref_ortho:.4f}; location minus slot offset matches {ref_id}"
                   if ok else f"frame 1 camera differs from {ref_id}")

    # Rebuilding from the same files gives bit-identical transforms (no hidden state).
    for shot in data["story"]["shots"]:
        sid = shot["id"]
        if sid not in signatures:
            continue
        ctx = shot_builder.build_shot(project_dir, sid, preset)
        frames, first = signatures[sid]
        report.add(sid, "repeatable_build", signature(ctx, frames) == first, f"sha256 {first[:16]}")

    passed = sum(r["status"] == "PASS" for r in report.results)
    return {"blender": bpy.app.version_string, "preset": preset,
            "summary": {"passed": passed, "failed": len(report.results) - passed, "total": len(report.results)},
            "results": report.results}


def sequence_camera_checks(ctx, report, plan):
    """SEQUENCE: at every settled view the camera is exactly that view's fit, its focus parts sit inside the frame
    (and above the safe band), and the annotation overlays keep their frame positions through every move."""
    sid = ctx.shot["id"]
    views = motion.sequence_views(ctx.cfg)
    fits = ctx.camera_keys["views"]
    issues, worst = [], 1.0
    for k, (v, fit) in enumerate(zip(views, fits)):
        f = 1 if k == 0 else plan.markers[f"view_{k}_settled"]
        ctx.scene.frame_set(f)
        loc, ortho = tuple(ctx.camera.matrix_world.translation), ctx.camera.data.ortho_scale
        if not (_close(loc, tuple(fit["location"]), 1e-4) and abs(ortho - fit["ortho_scale"]) < 1e-4):
            issues.append(f"view {k}@{f}: camera at {loc}, ortho {ortho:.3f}; fit {fit['ortho_scale']:.3f}")
        if fit.get("rotation") is not None:   # g-r5: and looking exactly from the view's direction
            want = framing.basis_from_euler(fit["rotation"])[2]
            got = tuple(-x for x in ctx.camera.matrix_world.col[2][:3])
            if not _close(got, want, 1e-4):
                issues.append(f"view {k}@{f}: camera looks along {tuple(round(x, 4) for x in got)}, view wants "
                              f"{tuple(round(x, 4) for x in want)}")
        dg = bpy.context.evaluated_depsgraph_get()
        ids = set(v["focus"] or [])
        for n, obj in ctx.objects.items():
            if obj.type != "MESH" or not _visible(obj) or (ids and obj["component_id"] not in ids) \
                    or float(obj.get("ass_transparency", 0.0)) >= 0.5:
                continue
            for p in shot_builder.world_vertices(obj, dg):
                c = world_to_camera_view(ctx.scene, ctx.camera, Vector(p))
                m = min(c.x, 1 - c.x, c.y - ctx.bottom_band, 1 - c.y)
                if m < worst:
                    worst = m
                if m < FRAME_MARGIN and len(issues) < 6:
                    issues.append(f"view {k}@{f}: {n} at ({c.x:.3f}, {c.y:.3f})")
                    break
    report.add(sid, "sequence_views_framed", not issues, "; ".join(issues[:6]) or
               f"{len(views)} views: camera exactly on each fit when settled, focus parts inside the frame "
               f"(min margin {worst:.3f})")
    overlays = [o for objs in (ctx.annotations or {}).values() for o in objs]
    if overlays and len(views) > 1:
        def frame_box(f):
            ctx.scene.frame_set(f)
            out = []
            for o in overlays:
                pts = [world_to_camera_view(ctx.scene, ctx.camera, o.matrix_world @ Vector(c)) for c in o.bound_box]
                out.append((min(p.x for p in pts), min(p.y for p in pts), max(p.x for p in pts), max(p.y for p in pts)))
            return out
        probe = sorted({1, ctx.frame_count} | {plan.markers[f"view_{k}_settled"] for k in range(1, len(views))}
                       | {max(1, plan.frame(v["start_seconds"] + v["move_seconds"] / 2)) for v in views[1:]})
        first = frame_box(probe[0])
        drift = max(abs(a - b) for f in probe[1:] for p, q in zip(first, frame_box(f)) for a, b in zip(p, q))
        ctx.scene.frame_set(1)
        report.add(sid, "overlays_screen_fixed", drift < 1e-3,
                   f"{len(overlays)} annotation objects keep their frame position through {len(views) - 1} camera "
                   f"move(s) (max drift {drift:.1e})" if drift < 1e-3 else f"annotations drift {drift:.4f} of the frame")


def _held(plan, name, f):
    """SEQUENCE: the part's see-through value does not change at frame f (a ghost held over the shot's first or last
    frame), so the cut shows the same blended surface on both sides."""
    if motion.TRANSPARENCY not in plan.channels(name):
        return False
    g = 2 if f == 1 else f - 1
    return abs(plan.sample(name, motion.TRANSPARENCY, f)[0] - plan.sample(name, motion.TRANSPARENCY, g)[0]) < 1e-9
