"""Offline structural checks using stdlib only; distinguishes demo gate vs publish gate."""
import json
from pathlib import Path

from engine import motion, spec, templates  # pure-Python modules, no bpy


class ValidationError(Exception):
    pass


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def validate_project(project_dir, final=False):
    base = Path(project_dir)
    errors, warnings = [], []
    required = {
        "project": base / "project.json",
        "storyboard": base / "storyboard/storyboard.json",
        "states": base / "storyboard/states.json",
        "sources": base / "research/sources.json",
        "assets": base / "assets/manifest.json",
    }
    for name, path in required.items():
        if not path.exists():
            errors.append(f"Missing {name}: {path}")
    if errors:
        return errors, warnings

    data = {key: read_json(value) for key, value in required.items()}
    project = data["project"]
    story = data["storyboard"]
    states = data["states"]
    sources = data["sources"]
    assets = data["assets"]

    if project.get("slug") != base.name:
        errors.append("project.slug must match project folder name")
    if project.get("mode") not in ("prototype", "production"):
        errors.append("project.mode invalid")
    fps = project.get("fps")
    if type(fps) is not int or not (1 <= fps <= 120):
        errors.append("fps must be integer between 1 and 120")
    duration = project.get("duration_seconds")
    if not isinstance(duration, (int, float)) or duration <= 0:
        errors.append("duration_seconds must be > 0")
        duration = 0
    shots = story.get("shots", [])
    if not isinstance(shots, list) or not shots:
        errors.append("Storyboard must have a nonempty shots list")
        shots = []
    variant_ids = [v.get("id") for v in states.get("variants", [])]
    if len(variant_ids) != len(set(variant_ids)) or any(not x for x in variant_ids):
        errors.append("Variant IDs must be present and unique")
    claim_ids = [c.get("id") for c in sources.get("claims", [])]
    source_ids = [s.get("id") for s in sources.get("sources", [])]
    if len(claim_ids) != len(set(claim_ids)):
        errors.append("Claim IDs must be unique")
    if len(source_ids) != len(set(source_ids)):
        errors.append("Source IDs must be unique")
    claim_map = {c.get("id"): c for c in sources.get("claims", [])}
    source_map = {s.get("id"): s for s in sources.get("sources", [])}

    seen = set()
    last_end = 0
    for shot in shots:
        sid = shot.get("id", "(missing)")
        if sid in seen:
            errors.append(f"Duplicate shot ID: {sid}")
        seen.add(sid)
        if not shot.get("visual_purpose"):
            errors.append(f"{sid}: no visual_purpose")
        a = shot.get("start_seconds")
        b = shot.get("duration_seconds")
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)) or a < 0 or b <= 0:
            errors.append(f"{sid}: invalid start/duration")
            continue
        if a < last_end - 0.001:
            errors.append(f"{sid}: shot overlaps previous (unless explicit montage policy)")
        last_end = max(last_end, a+b)
        for ref in shot.get("claim_ids", []):
            if ref not in claim_map:
                errors.append(f"{sid}: nonexistent claim {ref}")
        for field in ("from_state", "to_state"):
            v = shot.get(field)
            if v is not None and v not in variant_ids:
                errors.append(f"{sid}: unknown variant {v}")
        if shot.get("transition") == "REPLACE_PARTS" and not (shot.get("from_state") and shot.get("to_state")):
            errors.append(f"{sid}: REPLACE_PARTS needs two states")
    if shots and abs(last_end - duration) > .01:
        errors.append(f"Storyboard end {last_end:g}s must match project duration {duration:g}s")

    for change in states.get("transitions", []):
        if change.get("from") not in variant_ids or change.get("to") not in variant_ids:
            errors.append("Transition references unknown variant")

    # Component ownership, template configs and timing, planned offline with placeholder geometry.
    state_errors = spec.validate_states(states)
    errors.extend(f"states.json: {e}" for e in state_errors)
    plans = {}
    if not state_errors and type(fps) is int and fps > 0:
        for shot in shots:
            try:
                plans[shot.get("id")] = (shot, templates.plan_shot(
                    shot, states, fps, templates.placeholder_slots(shot, states)))
            except (motion.PlanError, KeyError, TypeError, ValueError) as e:
                errors.append(str(e) if str(e).startswith(str(shot.get("id"))) else f"{shot.get('id')}: {e}")
        still_ids = set()
        for still in story.get("key_stills", []):
            kid = still.get("id")
            if not kid or kid in still_ids:
                errors.append(f"key still id missing or duplicated: {kid!r}")
            still_ids.add(kid)
            if still.get("shot") not in plans:
                errors.append(f"key still {kid}: unknown or invalid shot {still.get('shot')!r}")
                continue
            shot, plan = plans[still["shot"]]
            if "marker" in still:
                if still["marker"] not in plan.markers:
                    errors.append(f"key still {kid}: marker '{still['marker']}' not produced by "
                                  f"{templates.animation_config(shot)['template']} (markers: {sorted(plan.markers)})")
            else:
                try:
                    templates.key_still_frame(shot, float(still.get("time_seconds")), fps)
                except (motion.PlanError, TypeError, ValueError) as e:
                    errors.append(f"key still {kid}: {e}")
    for claim in sources.get("claims", []):
        for ref in claim.get("source_ids", []):
            if ref not in source_map:
                errors.append(f"Claim {claim.get('id')} references missing source {ref}")
        if claim.get("review_status") != "verified":
            warnings.append(f"Claim {claim.get('id')} not verified — demo only")
        elif not claim.get("source_ids"):
            errors.append(f"Verified claim {claim.get('id')} needs source IDs")

    for asset in assets.get("assets", []):
        if asset.get("status") != "approved":
            warnings.append(f"Asset {asset.get('id')} rights pending")
        if asset.get("origin") != "procedural" and not asset.get("source_url"):
            errors.append(f"External asset {asset.get('id')} missing source_url")

    if final:
        if not project.get("audio_timing_locked"):
            errors.append("FINAL gate: audio timing not locked")
        if any(claim.get("review_status") != "verified" for claim in sources.get("claims", [])):
            errors.append("FINAL gate: unverified claims")
        if any(asset.get("status") != "approved" for asset in assets.get("assets", [])):
            errors.append("FINAL gate: unapproved assets")
        if project.get("factual_review") != "verified":
            errors.append("FINAL gate: factual_review is not verified")
    return errors, warnings
