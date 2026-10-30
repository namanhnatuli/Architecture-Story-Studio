"""Offline structural checks using stdlib only; distinguishes demo gate vs publish gate."""
import json
from pathlib import Path

from engine import motion, spec, templates  # pure-Python modules, no bpy

APPROVED_CLAIM = {"EDITORIALLY_APPROVED", "verified"}   # "verified": v0.1 ledger vocabulary
SOURCE_CHECKED_CLAIM = {"SOURCE_VERIFIED", "EDITORIALLY_APPROVED", "verified"}
GRAPHIC_KINDS = ("text", "arrow", "rect", "line", "circle", "polygon", "image")   # M7: shapes + archival images
EXTERNAL_LICENSE_FIELDS = ("source_url", "creator", "license", "attribution", "usage_restrictions", "acquired",
                           "local_path", "intended_use", "modifications", "status")


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
    if project.get("mode") not in ("prototype", "production", "documentary"):
        errors.append("project.mode invalid")
    if project.get("mode") == "documentary" or project.get("chapters"):   # M7 long-form: chapters are required
        from pipeline import chapters as CH
        narration_path = base / "script/narration.json"
        if not project.get("chapters"):
            errors.append("documentary mode needs project.chapters (script/chapters.json)")
        elif narration_path.is_file():
            beats_path = base / "script/visual_beats.json"
            errors += [f"chapters: {e}" for e in CH.validate(
                CH.load(base), json.loads(narration_path.read_text(encoding="utf-8")),
                json.loads(beats_path.read_text(encoding="utf-8")) if beats_path.is_file() else None)]
    profile = project.get("production_profile")
    if profile is not None:   # M5.5: explicit, validated production profiles (pipeline/gates.py)
        from pipeline.gates import PROFILES
        if profile not in PROFILES:
            errors.append(f"production_profile must be one of {', '.join(PROFILES)}")
        if profile == "TECHNICAL_SILENT_PREVIEW" and any(
                (base / rel).exists() for rel in ("script/narration.json", "audio/narration_manifest.json")):
            errors.append("production_profile TECHNICAL_SILENT_PREVIEW but the project has narration "
                          "(script/narration.json or audio/): a narrated project is NARRATED_INTERNAL_REVIEW or "
                          "PUBLICATION_CANDIDATE, its audio gates cannot be switched off")
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
            elif claim_map[ref].get("review_status") == "REJECTED":
                errors.append(f"{sid}: uses REJECTED claim {ref}")
        if shot.get("visual_type", "BLENDER_3D") == "MOTION_GRAPHICS":
            errors.extend(f"{sid}: {e}" for e in validate_graphic(shot.get("graphic"), b, base, assets))
        for field in ("from_state", "to_state"):
            v = shot.get(field)
            if v is not None and v not in variant_ids:
                errors.append(f"{sid}: unknown variant {v}")
        if shot.get("cut_from_previous", "match") not in ("match", "hard"):
            errors.append(f"{sid}: cut_from_previous must be 'match' or 'hard'")
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
            if shot.get("visual_type", "BLENDER_3D") != "BLENDER_3D":
                continue  # 2D cards / archival media are not planned by the 3D templates
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
            card = next((s for s in shots if s.get("id") == still.get("shot")
                         and s.get("visual_type") == "MOTION_GRAPHICS"), None)
            if card is not None:
                try:
                    templates.key_still_frame(card, float(still.get("time_seconds")), fps)
                except (motion.PlanError, TypeError, ValueError) as e:
                    errors.append(f"key still {kid}: {e}")
                continue
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
    _narr = base / "script/narration.json"
    narration_revision = ((read_json(_narr).get("revision") or {}).get("version")) if _narr.exists() else None
    for claim in sources.get("claims", []):
        cid, status = claim.get("id"), claim.get("review_status")
        for ref in claim.get("source_ids", []):
            if ref not in source_map:
                errors.append(f"Claim {cid} references missing source {ref}")
        if status in SOURCE_CHECKED_CLAIM and not claim.get("source_ids"):
            errors.append(f"Verified claim {cid} needs source IDs")
        if status in ("SOURCE_VERIFIED", "EDITORIALLY_APPROVED"):
            evidence = claim.get("evidence") or []
            for ref in claim.get("source_ids", []):
                ev = [e for e in evidence if e.get("source_id") == ref]
                if not ev or not all(e.get("locator") and e.get("excerpt") for e in ev):
                    errors.append(f"Claim {cid}: {status} needs a locator and an excerpt for {ref}")
                if not (source_map.get(ref) or {}).get("url"):
                    errors.append(f"Claim {cid}: source {ref} has no url")
        if status == "EDITORIALLY_APPROVED":  # a human record, tied to the narration wording it approved
            record = claim.get("editorial_approval") or {}
            missing = [k for k in ("approved_by", "approved_on", "narration_revision") if not record.get(k)]
            if missing:
                errors.append(f"Claim {cid}: EDITORIALLY_APPROVED needs editorial_approval.{', '.join(missing)} "
                              "(recorded by the human reviewer; see review/EDITORIAL_APPROVAL_PACKAGE.md)")
            elif narration_revision and record["narration_revision"] != narration_revision:
                errors.append(f"Claim {cid}: approval is for narration {record['narration_revision']!r}, but the "
                              f"narration is now {narration_revision!r} (re-review the changed wording)")
        if status == "REJECTED":
            continue
        if status not in APPROVED_CLAIM:
            warnings.append(f"Claim {cid} not verified — demo only" if status in ("provisional", "contested", None)
                            else f"Claim {cid} is {status}, not editorially approved — internal preview only")

    # M3 narration + timing lock (only when the project has a narration script).
    narration_path = base / "script/narration.json"
    narration = read_json(narration_path) if narration_path.exists() else None
    registry = lexicon = None
    if narration is not None:
        from pipeline import narration as nar
        from integrations.tts import providers
        from pipeline import pronunciation as pron
        registry = providers.load_registry()
        errors.extend(f"tts_providers: {e}" for e in providers.validate_registry(registry))
        lexicon = pron.load(base)
        errors.extend(f"narration: {e}" for e in nar.validate(narration, sources, registry, lexicon, base.name))
        order = [b.get("id") for b in narration.get("beats", [])]
        covered = []
        for s in shots:   # M5/M6 planned projects: one beat may span several consecutive shots
            for bid in s.get("beat_ids", []):
                if not covered or covered[-1] != bid or len(s.get("beat_ids", [])) > 1:
                    covered.append(bid)
        if covered != order:
            errors.append(f"shots must cover every narration beat exactly once, in order (shots {covered}, beats {order})")
        timing_path = base / "script/timing.json"
        if timing_path.exists():
            errors.extend(validate_timing(read_json(timing_path), narration, story, fps, duration, lexicon))
        elif project.get("audio_timing_locked"):
            errors.append("audio_timing_locked is true but script/timing.json is missing")

    for asset in assets.get("assets", []):
        if asset.get("status") != "approved":
            warnings.append(f"Asset {asset.get('id')} rights pending")
        if asset.get("origin") != "procedural" and not asset.get("source_url"):
            errors.append(f"External asset {asset.get('id')} missing source_url")
        if asset.get("origin") == "external":   # M7: archival imagery needs the full rights record
            missing = [k for k in EXTERNAL_LICENSE_FIELDS if not asset.get(k)]
            if missing:
                errors.append(f"External asset {asset.get('id')} rights record lacks {', '.join(missing)}")
            elif not (base / asset["local_path"]).is_file():
                errors.append(f"External asset {asset.get('id')}: {asset['local_path']} not found")

    if final:
        if not project.get("audio_timing_locked"):
            errors.append("FINAL gate: audio timing not locked")
        used = used_claim_ids(base, narration, story)   # M7: what the film actually says or shows
        checked = [c for c in sources.get("claims", []) if not used or c.get("id") in used]
        unapproved = sorted(c.get("id") for c in checked if c.get("review_status") not in APPROVED_CLAIM | {"REJECTED"})
        if unapproved:
            errors.append("FINAL gate: unverified claims used in the film (claims must be EDITORIALLY_APPROVED): "
                          + ", ".join(unapproved[:8]))
        missing = sorted(used - {c.get("id") for c in sources.get("claims", [])})
        if missing:
            errors.append("FINAL gate: the film uses claims missing from the registry: " + ", ".join(missing))
        if narration is not None:
            status = ((narration.get("voice") or {}).get("license") or {}).get("status")
            if status != "APPROVED":
                errors.append(f"FINAL gate: narration voice licence is {status!r}, not APPROVED")
            errors.extend(f"FINAL gate: {e}" for e in publication_audio_errors(base, narration, registry, lexicon))
        if any(asset.get("status") != "approved" for asset in assets.get("assets", [])):
            errors.append("FINAL gate: unapproved assets")
        if project.get("factual_review") != "verified":
            errors.append("FINAL gate: factual_review is not verified")
    return errors, warnings


def used_claim_ids(base, narration, story):
    """Claims the publication artifact uses: narration beats, visual beats (beat claims and annotation
    claims) and storyboard shots. Empty when the project records none (then every claim is checked)."""
    used = {c for b in (narration or {}).get("beats", []) for c in b.get("claim_ids", [])}
    beats_path = Path(base) / "script/visual_beats.json"
    if beats_path.is_file():
        vb = read_json(beats_path)
        for b in vb.get("beats", []):
            used |= set(b.get("claim_ids", []))
            used |= {a["claim_id"] for a in b.get("annotations", []) or [] if a.get("claim_id")}
    for s in (story or {}).get("shots", []):
        used |= set(s.get("claim_ids", []) or [])
    return used


def publication_audio_errors(base, narration, registry, lexicon):
    """Audio provenance for publication: every narrated segment must come from a PUBLICATION_CLEARED
    provider (by the record *and* the current registry) and every pronunciation override in use
    must be CONFIRMED by a human listener. Matching text/duration never substitutes for this."""
    from pipeline import pronunciation as pron
    errors = []
    manifest_path = base / "audio/narration_manifest.json"
    if not manifest_path.exists():
        return ["narration audio manifest missing"]
    manifest = read_json(manifest_path)
    segments = manifest.get("segments", {})
    providers_info = (registry or {}).get("providers", {})
    bad = {}
    for beat in manifest.get("beats", {}).values():
        for sentence in beat.get("sentences", []):
            rec = segments.get(sentence.get("cache_key")) or {}
            provider = rec.get("provider")
            current = (providers_info.get(provider) or {}).get("rights_class")
            if rec.get("rights_class") != "PUBLICATION_CLEARED" or current != "PUBLICATION_CLEARED":
                bad.setdefault((provider, rec.get("rights_class")), []).append(sentence.get("text", "")[:30])
    for (provider, rc), texts in bad.items():
        errors.append(f"{len(texts)} narration segment(s) from {provider} are {rc}, not PUBLICATION_CLEARED "
                      "(regenerate with a cleared provider: `narrate --purpose publication`)")
    provider = (narration.get("voice") or {}).get("provider")
    entries = {e["id"]: e for e in (lexicon or {}).get("entries", [])}
    for eid in pron.used_entries(narration, lexicon, provider):
        if entries[eid].get("status") != "CONFIRMED":
            errors.append(f"pronunciation {eid} ({entries[eid].get('written')}) is {entries[eid].get('status')}, "
                          "not CONFIRMED by a human listener")
    return errors


def _point(pt):
    return isinstance(pt, list) and len(pt) == 2 and all(isinstance(v, (int, float)) and 0 <= v <= 1 for v in pt)


def validate_graphic(graphic, duration, base=None, assets=None):
    """2D card spec (MOTION_GRAPHICS shots): element ids, kinds, positions, timing and, for
    archival images (M7), the file and a complete rights record in assets/manifest.json."""
    errors = []
    if not isinstance(graphic, dict) or not graphic.get("elements"):
        return ["MOTION_GRAPHICS shot needs graphic.elements"]
    manifest = {a.get("id"): a for a in (assets or {}).get("assets", [])}
    ids = set()
    for e in graphic["elements"]:
        eid = e.get("id")
        if not eid or eid in ids:
            errors.append(f"graphic element id missing or duplicated: {eid!r}")
        ids.add(eid)
        kind = e.get("kind")
        if kind not in GRAPHIC_KINDS:
            errors.append(f"graphic {eid}: kind must be one of {GRAPHIC_KINDS}")
            continue
        if kind == "text":
            points = [e.get("position")]
        elif kind == "arrow":
            points = [e.get("start"), e.get("end")]
        elif kind in ("rect", "image"):
            box = e.get("box")
            points = [box[:2], box[2:]] if isinstance(box, list) and len(box) == 4 else [None]
            if points[0] and points[1] and (box[0] >= box[2] or box[1] >= box[3]):
                errors.append(f"graphic {eid}: box must be [x0, y0, x1, y1] with x0 < x1, y0 < y1")
        elif kind == "circle":
            points = [e.get("center")]
        else:
            points = e.get("points") if isinstance(e.get("points"), list) and len(e.get("points")) >= 2 else [None]
        for pt in points:
            if not _point(pt):
                errors.append(f"graphic {eid}: positions are [x, y] in 0..1 card units")
                break
        if kind == "text" and not e.get("text"):
            errors.append(f"graphic {eid}: empty text")
        if kind == "image":
            asset = manifest.get(e.get("asset"))
            if asset is None:
                errors.append(f"graphic {eid}: image asset {e.get('asset')!r} is not in assets/manifest.json "
                              "(no external image without a rights record)")
            else:
                missing = [k for k in EXTERNAL_LICENSE_FIELDS if not asset.get(k)]
                if missing:
                    errors.append(f"graphic {eid}: asset {asset['id']} rights record lacks {', '.join(missing)}")
                if asset.get("local_path") != e.get("path"):
                    errors.append(f"graphic {eid}: path {e.get('path')!r} differs from the asset's local_path")
            if base is not None and not (Path(base) / str(e.get("path"))).is_file():
                errors.append(f"graphic {eid}: image file {e.get('path')!r} not found")
            crop = e.get("crop", [0, 0, 1, 1])
            if not (isinstance(crop, list) and len(crop) == 4 and 0 <= crop[0] < crop[2] <= 1 and 0 <= crop[1] < crop[3] <= 1):
                errors.append(f"graphic {eid}: crop must be [u0, v0, u1, v1] inside 0..1")
        appear = e.get("appear", 0.0)
        if isinstance(appear, str) or "sentence" in e:
            errors.append(f"graphic {eid}: unresolved timing {e.get('sentence', appear)!r} (run plan-visuals / `schedule`)")
        elif isinstance(duration, (int, float)) and not 0 <= appear < duration:
            errors.append(f"graphic {eid}: appears at {appear}s, outside the shot")
        dis = e.get("disappear")
        if dis is not None and not (isinstance(dis, (int, float)) and appear < dis <= (duration or dis) + 1e-6):
            errors.append(f"graphic {eid}: disappear {dis!r} must be after appear and inside the shot")
    return errors


def validate_timing(timing, narration, story, fps, duration, lexicon=None):
    """The timing lock must match the current narration, storyboard and project duration."""
    from pipeline import beat_scheduler, narration as nar
    errors = []
    basis = timing.get("lock_basis") or {}
    if basis.get("narration_sha256") != nar.narration_hash(narration, lexicon):
        errors.append("timing lock is stale: narration.json changed since `narrate`/`schedule`")
    if timing.get("storyboard_sha256") != beat_scheduler.content_hash(story):
        errors.append("timing lock is stale: storyboard.json differs from the scheduled one (re-run `schedule`)")
    if timing.get("fps") != fps:
        errors.append("timing fps differs from project fps")
    if isinstance(duration, (int, float)) and abs(timing.get("total_seconds", -1) - duration) > 1e-6:
        errors.append("project duration differs from timing.json total")
    for s in timing.get("shots", []):
        if s.get("frames") != round(s.get("duration_seconds", 0) * fps):
            errors.append(f"{s.get('id')}: timing duration is not a whole number of frames")
    if timing.get("mode") == "PLANNED_AUDIO_LOCK":   # M6: lock-audio + build-shots (pipeline/audio_lock.py)
        from pipeline import audio_lock
        if timing.get("stage") != "SHOTS_SCHEDULED":
            errors.append("timing lock is stale: shots not scheduled yet (run build-shots after lock-audio)")
        elif timing.get("beats_sha256") != audio_lock.beats_hash(timing):
            errors.append("timing manifest is inconsistent: beat sentence spans differ from the locked audio")
        errors.extend(f"timing manifest: {e}" for e in audio_lock.check_consistency(timing))
    return errors

