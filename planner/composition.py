"""Adaptive comparison composition (M5.5): measure candidate layouts offline and pick
the clearest one that the narrative allows.

Every candidate is evaluated with the engine's own layout and camera maths (the offline
scene of planner/visibility.py): per model screen box, pixels per metre at the reference
(small-screen) resolution, the projected size of the model's typical member ("detail":
median of the smallest extent of its own components), overlap, clipping, label room and
scale. All simultaneous layouts and SEQUENTIAL_COMPARISON (one model at a time under one
shared locked camera) keep a COMMON real-world scale; nothing is normalised per model.
"""
import statistics

from engine import framing
from planner import visibility as VIS

LAYOUTS = ("SIDE_BY_SIDE_STACK", "SIDE_BY_SIDE_ROW", "SEQUENTIAL_COMPARISON")


def _detail_m(scene, slot):
    """Median of the smallest bounding extent of the model's own components (metres)."""
    dims = []
    for n, p in scene.parts.items():
        if p.slot != slot or n in scene.hidden or p.id in scene.shared:
            continue
        pts = VIS._verts(p)
        dims.append(min(max(q[i] for q in pts) - min(q[i] for q in pts) for i in range(3)))
    return statistics.median(dims) if dims else 0.0


def _boxes(scene):
    """{slot: (x0, x1, y0, y1)} frame-space boxes of what each slot shows."""
    out = {}
    for slot in scene.offsets:
        pts = [q for n, p in scene.parts.items() if p.slot == slot and n not in scene.hidden
               for q in VIS._verts(p, offset=scene.offsets[slot])]
        sc = framing.frame_coords(pts, scene.fit, scene.basis, scene.aspect)
        out[slot] = (min(x for x, _ in sc), max(x for x, _ in sc), min(y for _, y in sc), max(y for _, y in sc))
    return out


def measure_layout(scene, cfg, labels=True):
    """Readability metrics of one built comparison scene (SIDE_BY_SIDE or a single-model shot)."""
    w_px, h_px = cfg["reference_resolution"]
    px_per_m = w_px / scene.fit["ortho_scale"]
    boxes = _boxes(scene)
    models = {}
    for slot, (x0, x1, y0, y1) in boxes.items():
        d = _detail_m(scene, slot)
        models[slot] = {"width": round(x1 - x0, 4), "height": round(y1 - y0, 4),
                        "occupancy": round((x1 - x0) * (y1 - y0), 4), "width_px": round((x1 - x0) * w_px, 1),
                        "detail_m": round(d, 3), "detail_px": round(d * px_per_m, 2),
                        "clipped": x0 < -1e-6 or x1 > 1 + 1e-6 or y0 < -1e-6 or y1 > 1 + 1e-6,
                        "in_label_band": y0 < scene.band - 1e-6}
    overlap = 0.0
    slots = list(boxes)
    for i, a in enumerate(slots):
        for b in slots[i + 1:]:
            A, B = boxes[a], boxes[b]
            ix = max(0.0, min(A[1], B[1]) - max(A[0], B[0]))
            iy = max(0.0, min(A[3], B[3]) - max(A[2], B[2]))
            small = min((A[1] - A[0]) * (A[3] - A[2]), (B[1] - B[0]) * (B[3] - B[2]))
            overlap = max(overlap, ix * iy / small if small else 0.0)
    label_clash = False
    if labels and scene.template == "SIDE_BY_SIDE" and scene.shot["animation"].get("layout") == "STACK":
        size = cfg["label_size"]          # STACK captions sit under each row (engine/shot_builder.build_labels)
        rows = sorted(boxes.values(), key=lambda b: -b[3])
        for upper, lower in zip(rows, rows[1:]):
            if upper[2] - 1.4 * size < lower[3]:
                label_clash = True
    return {"px_per_m": round(px_per_m, 2), "models": models, "overlap": round(overlap, 4),
            "label_clash": label_clash, "scale": "COMMON",
            "min_detail_px": min(m["detail_px"] for m in models.values()),
            "min_width": min(m["width"] for m in models.values())}


def readable(metrics, cfg):
    """(ok, problems) for a measured layout."""
    problems = []
    if metrics["min_detail_px"] < cfg["min_detail_px"]:
        problems.append(f"members ~{metrics['min_detail_px']:.1f} px wide at "
                        f"{cfg['reference_resolution'][0]}x{cfg['reference_resolution'][1]} (< {cfg['min_detail_px']})")
    if metrics["min_width"] < cfg["min_model_width"]:
        problems.append(f"smallest model {metrics['min_width'] * 100:.0f}% of the frame width (< "
                        f"{cfg['min_model_width'] * 100:.0f}%)")
    if any(m["clipped"] for m in metrics["models"].values()):
        problems.append("a model is clipped by the frame")
    if any(m["in_label_band"] for m in metrics["models"].values()):
        problems.append("a model reaches into the label/subtitle band")
    if metrics["overlap"] > cfg["max_overlap"]:
        problems.append(f"models overlap on screen ({metrics['overlap'] * 100:.0f}%)")
    if metrics["label_clash"]:
        problems.append("captions collide with the next row")
    return not problems, problems


def comparison_shot(state_ids, layout, gap_ratio, label_band, camera, labels=None):
    """Synthetic SIDE_BY_SIDE shot used to measure a candidate layout."""
    anim = {"template": "SIDE_BY_SIDE", "states": list(state_ids), "layout": layout, "gap_ratio": gap_ratio,
            "label_band": label_band}
    if labels:
        anim["labels"] = labels
    return {"id": "CANDIDATE", "duration_seconds": 3.0, "visual_type": "BLENDER_3D", "transition": "SIDE_BY_SIDE",
            "camera": camera, "from_state": state_ids[0], "to_state": state_ids[-1], "animation": anim}


def single_shot(state_id, built, camera, band):
    """Synthetic single-model HOLD of a sequential comparison (shared build set = shared camera)."""
    return {"id": "CANDIDATE", "duration_seconds": 3.0, "visual_type": "BLENDER_3D", "transition": "HOLD",
            "camera": camera, "from_state": state_id, "to_state": state_id,
            "animation": {"template": "HOLD", "state": state_id}, "build_variants": list(built), "camera_safe_band": band}


def purpose_cfg(cfg, purpose):
    return dict(cfg, **cfg["purposes"][purpose])


def evaluate(states, state_ids, camera, cfg, purpose, presets, fps=24):
    """Every candidate simultaneous layout: [{layout, gap_ratio, label_band, ok, problems, metrics}]."""
    pc = purpose_cfg(cfg, purpose)
    rows = []
    for cand in cfg["candidates"]:
        shot = comparison_shot(state_ids, cand["layout"], cand["gap_ratio"], cand["label_band"], camera)
        try:
            scene = VIS.build_scene(shot, states, fps, presets)
        except ValueError as e:   # e.g. STACK needs an elevated camera
            rows.append(dict(cand, ok=False, problems=[str(e)], metrics=None))
            continue
        m = measure_layout(scene, cfg)
        ok, problems = readable(m, pc)
        rows.append(dict(cand, ok=ok, problems=problems, metrics=m))
    return rows


def best(rows):
    """Most readable passing candidate (largest smallest member, then largest smallest model,
    then candidate order), or None."""
    good = [(i, r) for i, r in enumerate(rows) if r["ok"]]
    if not good:
        return None
    return sorted(good, key=lambda ir: (-round(ir[1]["metrics"]["min_detail_px"], 1),
                                        -round(ir[1]["metrics"]["min_width"], 3), ir[0]))[0][1]


def evaluate_sequence(states, state_ids, built, camera, cfg, purpose, presets, fps=24):
    """One model per shot under the shared camera: [{state, ok, problems, metrics}]."""
    pc = purpose_cfg(cfg, purpose)
    rows = []
    for s in state_ids:
        scene = VIS.build_scene(single_shot(s, built, camera, cfg["sequence_caption_band"]), states, fps, presets)
        m = measure_layout(scene, cfg, labels=False)
        ok, problems = readable(m, pc)
        rows.append({"state": s, "ok": ok, "problems": problems, "metrics": m})
    return rows


def summary(rows):
    """Short text of evaluated candidates for explanations."""
    out = []
    for r in rows:
        name = f"{r['layout']} {r['gap_ratio']}" if "layout" in r else r["state"]
        out.append(f"{name}: " + ("readable" if r["ok"] else "; ".join(r["problems"])))
    return " | ".join(out)
