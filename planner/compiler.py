"""Visual execution plan -> the existing deterministic engine contract:
storyboard/states.json, storyboard/storyboard.json, project.json (+ assets manifest).
No planning decisions are made here; the compiler transcribes a validated plan and picks
the frame that represents each shot as a key still."""
import json
from pathlib import Path

from planner.planner import is_site_state

SHOT_KEYS = ("id", "duration_seconds", "visual_type", "transition", "camera", "from_state", "to_state",
             "animation", "graphic", "camera_focus", "camera_safe_band", "build_variants", "annotations",
             "scene_context")


def storyboard(plan):
    shots, stills = [], []
    for ps in plan["shots"]:
        src = ps["shot"]
        shot = {k: src[k] for k in SHOT_KEYS if k in src and src[k] is not None}
        shot["start_seconds"] = ps["timing"]["start_seconds"]
        if ps["cut_from_previous"] == "hard":
            shot["cut_from_previous"] = "hard"
        shot.update(beat_ids=src["beat_ids"], claim_ids=src["claim_ids"], narration=src["narration"],
                    visual_purpose=src["visual_purpose"],
                    editorial={"planned_by": f"planner {plan['planner_version']}", "beat_id": ps["beat_id"],
                               "visual_intent": ps["visual_intent"], "strategy": ps["strategy"],
                               "part": ps["part"], "evidence_status": ps["evidence_status"],
                               "semantic_targets": [t["concept"] for t in ps["semantic_targets"]],
                               "timing_mode": ps["timing"]["mode"]})
        if ps["semantic_targets"]:   # M5.5: what Level 2 (verify-visibility) measures, and the estimate
            shot["editorial"]["visibility_targets"] = [
                {"concept": t["concept"], "component_ids": t["component_ids"],
                 "pieces": t["concept"] in plan.get("pieces_concepts", [])} for t in ps["semantic_targets"]]
            shot["editorial"]["visibility_estimate"] = [
                {k: r.get(k) for k in ("concept", "label", "frame", "visible_share", "core_area", "visible_area", "ok")}
                for r in (ps.get("visibility") or {}).get("targets", [])]
        if ps.get("composition"):
            shot["editorial"]["composition"] = {k: v for k, v in ps["composition"].items() if k != "candidates"}
        if ps.get("repairs"):
            shot["editorial"]["repairs"] = ps["repairs"]
        shots.append(shot)
        marker = {"EXPLODED_VIEW": "exploded_hold", "REPLACE_PARTS": "middle"}.get(ps["template"])
        if ps["template"] == "REPLACE_PARTS" and is_site_state(ps["states"][0]):
            marker = "incoming_end"      # assembly into the empty site: "middle" would still be empty
        still = {"id": f"{ps['shot_id']}_{ps['beat_id']}_{ps['template'].lower()}", "shot": ps["shot_id"]}
        if marker:
            still["marker"] = marker
        else:
            still["time_seconds"] = round(min(ps["timing"]["duration_seconds"] * 0.55,
                                              ps["timing"]["duration_seconds"] - 1 / plan["fps"]), 4)
        stills.append(still)
    return {"generated_by": f"planner {plan['planner_version']} (tools/cli.py build-shots); edit "
                            "script/visual_beats.json and re-plan, not this file",
            "plan_sha256": plan_hash(plan), "key_stills": stills, "shots": shots}


def plan_hash(plan):
    import hashlib
    return hashlib.sha256(json.dumps(plan, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def compile_plan(plan, project_dir):
    """Write the engine files for an executable plan; returns written paths."""
    if not plan["executable"]:
        bad = [f"{c['beat_id']}: {c['status']}" + (f" ({c['annotation_failures']} annotation(s) failed)"
                                                    if c.get("annotation_failures") else "")
               for c in plan["coverage"] if c["status"] not in ("COVERED", "PARTIALLY_COVERED") or c.get("annotation_failures")]
        raise ValueError("plan is not executable (" + "; ".join(bad) + "); see qa/VISUAL_COVERAGE.md")
    p = Path(project_dir)
    (p / "storyboard").mkdir(parents=True, exist_ok=True)
    states_path, story_path, project_path = p / "storyboard/states.json", p / "storyboard/storyboard.json", p / "project.json"
    states_path.write_text(json.dumps(plan["states"], indent=2) + "\n")
    story_path.write_text(json.dumps(storyboard(plan), indent=2, ensure_ascii=False) + "\n")
    project = json.loads(project_path.read_text()) if project_path.is_file() else {}
    project.update(slug=p.name, title=plan.get("title") or p.name, mode=project.get("mode", "prototype"),
                   language=project.get("language", "en"), fps=plan["fps"], duration_seconds=plan["duration_seconds"],
                   render_preset=project.get("render_preset", "preview"),
                   factual_review=project.get("factual_review", "provisional"),
                   # the lock is set by M3 `schedule`; a PROVISIONAL plan always clears it (fail closed)
                   audio_timing_locked=plan["timing_mode"] == "AUDIO_LOCKED" and bool(project.get("audio_timing_locked")))
    project_path.write_text(json.dumps(project, indent=2) + "\n")
    manifest = p / "assets/manifest.json"
    if not manifest.is_file():
        manifest.parent.mkdir(parents=True, exist_ok=True)
        manifest.write_text(json.dumps({"assets": [{"id": "AST_001", "origin": "procedural",
                                                     "name": "Architecture assets resolved by planner/",
                                                     "license": "generated_in_project", "status": "approved",
                                                     "source_url": None, "credit": "Architecture Story Studio"}]},
                                       indent=2) + "\n")
    return [states_path, story_path, project_path]
