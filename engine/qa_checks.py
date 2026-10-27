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


def check_shot(ctx, states, report):
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
                if err > TOL and len(mismatches) < 5:
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

    # 4. No template ever scales a component (v0.1 shrank parts to 1%).
    scaled = []
    for f in frames:
        ctx.scene.frame_set(f)
        for n, obj in ctx.render_objects.items():
            if not _close(tuple(obj.matrix_world.to_scale()), (1.0, 1.0, 1.0), TRANSFORM_TOL):
                scaled.append(f"{n}@{f}")
    report.add(sid, "no_scale_change", not scaled, ", ".join(scaled[:5]) or "all world scales are 1.0")

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
        names = sorted(plan.tracks)
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
    actual_visible = {n for n, o in ctx.objects.items() if _visible(o)}
    report.add(sid, "final_visibility", actual_visible == expected_visible,
               f"missing {sorted(expected_visible - actual_visible)}, unexpected {sorted(actual_visible - expected_visible)}"
               if actual_visible != expected_visible else f"{len(actual_visible)} visible parts as expected")

    # 7. Framing: opaque geometry inside the frame (and above the label band) on every sampled frame.
    worst_margin, worst_at, bottom_min = 1.0, None, 1.0
    settle = plan.markers.get("intro_end", 1)
    ctx.scene.frame_set(settle)
    cam_matrix, cam_ortho = ctx.camera.matrix_world.copy(), ctx.camera.data.ortho_scale
    cam_moves = []
    for f in frames:
        ctx.scene.frame_set(f)
        dg = bpy.context.evaluated_depsgraph_get()
        if f >= settle and (ctx.camera.matrix_world != cam_matrix or ctx.camera.data.ortho_scale != cam_ortho):
            cam_moves.append(f)
        for n, obj in ctx.render_objects.items():
            if obj.type != "MESH" or not _visible(obj):
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
                if not twin.hide_render and (not orig.hide_render or f in (1, last)):
                    overlap.append(f"{name}@{f}")
        report.add(sid, "fade_twins_exclusive", not overlap, ", ".join(overlap[:5]) or
                   f"{len(ctx.fade_twins)} twins visible only mid-fade, never with their original or on frames 1/{last}")

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
        if ctx.labels:  # captions: right text, inside the label band, under their own model, no overlap
            ctx.scene.frame_set(1)
            dg = bpy.context.evaluated_depsgraph_get()
            issues, spans = [], []
            for slot_id, label in ctx.labels.items():
                if label.data.body != ctx.cfg["labels"][slot_id]:
                    issues.append(f"{slot_id}: text {label.data.body!r} differs from the storyboard")
                corners = [world_to_camera_view(ctx.scene, ctx.camera, label.matrix_world @ Vector(c))
                           for c in label.evaluated_get(dg).bound_box]
                xs, ys = [c.x for c in corners], [c.y for c in corners]
                stack = ctx.cfg.get("layout", "ROW") == "STACK"
                if min(xs) < FRAME_MARGIN or max(xs) > 1 - FRAME_MARGIN or min(ys) < 0.005 or \
                        (not stack and max(ys) > ctx.bottom_band):
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
    return frames


def check_card(ctx, report):
    """2D card shot: every element built, fades match the plan, camera static."""
    sid = ctx.shot["id"]
    expected = {e["id"] for e in ctx.shot["graphic"]["elements"]}
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
            want = ctx.plan.sample(name, motion.TRANSPARENCY, f)[0]
            got = float(ctx.objects[name]["ass_transparency"])
            worst = max(worst, abs(want - got))
            if abs(want - got) > TOL and len(bad) < 5:
                bad.append(f"{name}@{f}: plan {want} vs {got}")
    report.add(sid, "plan_matches_evaluated_keys", not bad,
               "; ".join(bad) or f"{len(ctx.plan.tracks)} elements x {len(frames)} frames, max error {worst:.2e}")
    report.add(sid, "camera_locked", not moved, "card camera never moves" if not moved else "card camera moved")
    ctx.scene.frame_set(ctx.frame_count)
    hidden = [n for n, o in ctx.objects.items() if float(o["ass_transparency"]) > 1e-6]
    report.add(sid, "final_visibility", not hidden, f"still transparent at the end: {hidden}" if hidden
               else "every element visible on the last frame")
    return frames


def run_all(project_dir, preset="preview"):
    data = shot_builder.load_project(project_dir, preset)
    states = data["states"]
    report = Report()
    cameras, signatures, intros = {}, {}, {}
    for shot in data["story"]["shots"]:
        sid = shot["id"]
        ctx = shot_builder.build_shot(project_dir, sid, preset)
        if shot.get("visual_type", "BLENDER_3D") == "MOTION_GRAPHICS":
            signatures[sid] = (check_card(ctx, report), None)
            signatures[sid] = (signatures[sid][0], signature(ctx, signatures[sid][0]))
            continue
        frames = check_shot(ctx, states, report)
        if ctx.cfg["template"] != "SIDE_BY_SIDE":
            cameras[sid] = ([v for r in ctx.camera.matrix_world for v in r], ctx.camera.data.ortho_scale)
        elif ctx.camera_keys:
            ctx.scene.frame_set(1)
            m = ctx.camera.matrix_world
            intros[sid] = ([m[r][c] for r in range(3) for c in range(3)], [m[r][3] for r in range(3)],
                           ctx.camera.data.ortho_scale, ctx.slot_offsets[ctx.cfg["intro"]["from_state"]])
        signatures[sid] = (frames, signature(ctx, frames))

    # One locked camera for every single-model shot: cuts between them are invisible.
    ref_id = next(iter(cameras), None)
    diffs = [sid for sid, (m, s) in cameras.items()
             if not (_close(m, cameras[ref_id][0], 1e-6) and abs(s - cameras[ref_id][1]) < 1e-6)]
    report.add("ALL", "camera_identical_across_single_model_shots", not diffs,
               f"differs: {diffs}" if diffs else f"{len(cameras)} shots share one camera")

    # A SIDE_BY_SIDE intro must open on exactly the single-model framing (seamless cut).
    for sid, (rot, loc, ortho, shift) in intros.items():
        if ref_id is None:
            break
        ref_m, ref_ortho = cameras[ref_id]
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
        ctx = shot_builder.build_shot(project_dir, sid, preset)
        frames, first = signatures[sid]
        report.add(sid, "repeatable_build", signature(ctx, frames) == first, f"sha256 {first[:16]}")

    passed = sum(r["status"] == "PASS" for r in report.results)
    return {"blender": bpy.app.version_string, "preset": preset,
            "summary": {"passed": passed, "failed": len(report.results) - passed, "total": len(report.results)},
            "results": report.results}
