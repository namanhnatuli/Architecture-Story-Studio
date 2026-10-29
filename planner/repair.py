"""Visibility assessment and constrained visual repair of a drafted plan (M5.5).

Rule: every semantic target concept of a beat must read (planner/visibility.verdict) at an
explanatory frame of at least one of the beat's shots. When it does not, remedies are
evaluated offline on a copy of the shot, in the default preference order:

  1. REFRAME     camera_focus on the target (+ subtitle-safe band); same view direction
  2. SAFE_BAND   keep the subtitle band free on that shot (a band change splits its continuity group)
  3. ALT_CAMERA  another existing preset of the aspect class
  4. GHOST       the role groups covering the target turn see-through while it glows (HOLD)
  5. (planner)   the beat's next strategy (e.g. an exploded view), then manual review

Camera remedies that would break a match cut are skipped (reason recorded) unless the
problem is size/clipping, which only a closer framing can fix. The first remedy that
passes is written into the plan shot (never into a rendered scene) with every evaluated
candidate, so the decision is reproducible and reviewable.
"""
import copy

from planner import camera as CAM, visibility as VIS

REMEDIES = ("REFRAME", "SAFE_BAND", "ALT_CAMERA", "GHOST")


def assess_shot(ps, states, vcfg, presets, fps, pieces=()):
    """Rows for the shot's targets at its explanatory frames (+ frames, verification).
    pieces: concepts read as separate pieces (checked one by one in exploded views)."""
    scene = VIS.build_scene(ps["shot"], states, fps, presets)
    frames = VIS.evaluation_frames(scene)
    labels = VIS.explanatory_labels(scene)
    rows = []
    for lab in labels:
        for r in VIS.measure(scene, frames[lab], ps["semantic_targets"], vcfg):
            ok, ver, problems = VIS.verdict(r, vcfg, scene.template == "EXPLODED_VIEW" and r["concept"] in pieces)
            rows.append(dict(r, frame=frames[lab], label=lab, ok=ok, verification=ver, problems=problems))
    return scene, {"frames": frames, "explanatory": labels, "targets": rows}


def stored(assessment):
    """Plan copy of an assessment: top occluders only."""
    out = copy.deepcopy(assessment)
    for r in out["targets"]:
        if "occluders" in r:
            r["occluders"] = [{k: o[k] for k in ("id", "share")} for o in r["occluders"][:4]]
    return out


def _in_match_chain(plan_shots, i):
    nxt = plan_shots[i + 1] if i + 1 < len(plan_shots) else None
    return plan_shots[i]["cut_from_previous"] == "match" or (nxt is not None and nxt["cut_from_previous"] == "match")


def _row(assessment, concept):
    rows = [r for r in assessment["targets"] if r["concept"] == concept]
    return next((r for r in rows if r["ok"]), rows[0] if rows else None)


def _try(ps, states, vcfg, presets, fps, concept, change, pieces=()):
    trial = copy.deepcopy(ps)
    change(trial)
    try:
        _, a = assess_shot(trial, states, vcfg, presets, fps, pieces)
    except Exception as e:   # noqa: BLE001 - an engine refusal makes the remedy unusable
        return trial, None, f"engine rejects it: {e}"
    r = _row(a, concept)
    if r is None:
        return trial, None, "target not shown"
    return trial, r, (f"share {r['visible_share']:.2f}, core {r['core_area'] * 100:.2f}%, area "
                      f"{r['visible_area'] * 100:.2f}% -> " + ("PASS" if r["ok"] else ",".join(r["problems"])))


def candidates(ps, row, scene, plan_shots, i, cfg, family):
    """[(remedy, change(shot) or None, skip reason)] in preference order."""
    vcfg = cfg["visibility"]
    if callable(family):   # M6 multi-family: the shot's own scene context
        family = family(ps)
    problems = set(row["problems"])
    ids = {i for t in ps["semantic_targets"] for i in t["component_ids"]}   # every target stays framed
    if ps["template"] == "EXPLODED_VIEW":   # and every moving part: an explode is never cut by the frame
        ids |= set(ps["shot"]["animation"].get("components") or [])
    ids = sorted(ids)
    chain = _in_match_chain(plan_shots, i)
    size = bool(problems & {"TOO_SMALL", "CLIPPED"})
    out = []

    def reframe(p):
        p["shot"]["camera_focus"] = sorted(ids)
        p["shot"]["camera_safe_band"] = vcfg["subtitle_safe_band"]
        p["camera"].update(mode="COMPONENT_CLOSEUP", focus=sorted(ids), safe_band=vcfg["subtitle_safe_band"])
    if ps["template"] == "SIDE_BY_SIDE":
        return out
    out.append(("REFRAME", reframe if (size or not chain) else None,
                None if (size or not chain) else f"would break the match cut with "
                                                 f"{'the previous' if ps['cut_from_previous'] == 'match' else 'the next'} shot"))
    if "SUBTITLE_SAFE_AREA" in problems:
        def band(p):
            p["shot"]["camera_safe_band"] = vcfg["subtitle_safe_band"]
            p["camera"]["safe_band"] = vcfg["subtitle_safe_band"]
        out.append(("SAFE_BAND", band, None))
    if "OCCLUDED" in problems:
        current = ps["shot"]["camera"]
        cams = cfg["aspect_classes"][CAM.aspect_class(cfg, family)]["camera"]
        alts = sorted({p for mode, p in cams.items() if mode != "COMPARISON"} - {current})
        for preset in alts:
            def alt(p, preset=preset):
                p["shot"]["camera"] = preset
                p["camera"]["preset"] = preset
            out.append((f"ALT_CAMERA:{preset}", None if chain else alt,
                        "would break the match-cut continuity (a different view direction)" if chain else None))
        if ps["template"] == "HOLD" and (ps["shot"]["animation"].get("highlight") or {}).get("components"):
            target_roles = {r for t in ps["semantic_targets"] for r in t["roles"]}
            by_role = {}
            for o in row["occluders"]:
                part = next((p for p in scene.parts.values() if p.id == o["id"]), None)
                if part is None or part.id in scene.shared or part.role in target_roles:
                    continue
                by_role[part.role] = by_role.get(part.role, 0) + o["samples"]
            ranked = [r for r, _ in sorted(by_role.items(), key=lambda kv: (-kv[1], kv[0]))]
            shown = [p for n, p in scene.parts.items() if n not in scene.hidden and p.id not in scene.shared]
            glow = set(ps["shot"]["animation"]["highlight"]["components"])
            for k in range(1, min(len(ranked), vcfg["max_ghost_role_groups"]) + 1):
                roles = set(ranked[:k])
                ghost = sorted(p.id for p in shown if p.role in roles and p.id not in glow)
                if not ghost:
                    continue

                def gh(p, ghost=ghost):
                    p["shot"]["animation"]["highlight"]["ghost"] = ghost
                    p["shot"]["animation"]["highlight"]["ghost_transparency"] = vcfg["ghost_transparency"]
                out.append((f"GHOST:{'+'.join(sorted(roles))}", gh, None))
    prefer = ps.get("repair_preference")
    if prefer:   # M6: a beat may prefer e.g. GHOST (keep the narrated view direction) over ALT_CAMERA
        rank = {name: k for k, name in enumerate(prefer)}
        out.sort(key=lambda c: rank.get(c[0].split(":")[0], len(prefer)))
    return out


def repair_plan(plan_shots, states_fn, continuity_fn, cfg, presets, fps, family, pieces=()):
    """Assess every shot with targets; repair beats whose concepts do not read anywhere.
    Returns (records, unresolved {beat_id: [concept rows]})."""
    vcfg = cfg["visibility"]
    repaired, failed = [], []
    for _ in range(3):      # camera repairs change continuity groups (and fits): re-assess
        failed = []
        states = states_fn()
        scenes, changed_camera = {}, False
        for ps in plan_shots:
            if ps["semantic_targets"] and ps["template"] in ("HOLD", "EXPLODED_VIEW", "REPLACE_PARTS"):
                scenes[ps["shot_id"]], a = assess_shot(ps, states, vcfg, presets, fps, pieces)
                ps["_assessment"] = a
        unresolved = {}
        beats = []
        for ps in plan_shots:
            if ps["beat_id"] not in beats:
                beats.append(ps["beat_id"])
        for bid in beats:
            shots = [(i, ps) for i, ps in enumerate(plan_shots) if ps["beat_id"] == bid and "_assessment" in ps]
            concepts = []
            for _, ps in shots:
                for t in ps["semantic_targets"]:
                    if t["concept"] not in concepts:
                        concepts.append(t["concept"])
            for concept in concepts:
                rows = [(i, ps, r) for i, ps in shots for r in ps["_assessment"]["targets"] if r["concept"] == concept]
                if any(r["ok"] for _, _, r in rows):
                    continue
                fixed = False
                for i, ps, r in rows:
                    tried = []
                    for remedy, change, skip in candidates(ps, r, scenes[ps["shot_id"]], plan_shots, i, cfg, family):
                        if change is None:
                            tried.append({"remedy": remedy, "result": "SKIPPED", "detail": skip})
                            continue
                        trial, tr, detail = _try(ps, states, vcfg, presets, fps, concept, change, pieces)
                        tried.append({"remedy": remedy, "result": "PASS" if tr and tr["ok"] else "FAIL", "detail": detail})
                        if tr and tr["ok"]:
                            ps["shot"], ps["camera"] = trial["shot"], trial["camera"]
                            changed_camera |= not remedy.startswith("GHOST")
                            repaired.append({"beat_id": bid, "shot_id": ps["shot_id"], "concept": concept,
                                             "problems": r["problems"], "frame": r["label"],
                                            "before": {k: r[k] for k in ("visible_share", "core_area", "visible_area")},
                                            "after": {k: tr[k] for k in ("visible_share", "core_area", "visible_area")},
                                            "evaluated": tried, "chosen": remedy})
                            fixed = True
                            break
                    if fixed:
                        break
                    failed.append({"beat_id": bid, "shot_id": ps["shot_id"], "concept": concept,
                                   "problems": r["problems"], "frame": r["label"],
                                   "before": {k: r[k] for k in ("visible_share", "core_area", "visible_area")},
                                   "evaluated": tried, "chosen": None})
                if not fixed:
                    unresolved.setdefault(bid, []).append(rows[0][2])
        if not changed_camera:
            break
        continuity_fn()
    for ps in plan_shots:     # final assessment of the repaired plan
        if "_assessment" in ps:
            _, a = assess_shot(ps, states_fn(), vcfg, presets, fps, pieces)
            ps["visibility"] = stored(a)
            del ps["_assessment"]
        else:
            ps["visibility"] = None
    return repaired + failed, unresolved
