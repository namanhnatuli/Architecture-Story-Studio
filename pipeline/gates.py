"""Gates G0-G6 + project status flags for narrated projects (stdlib only).

Status flags are separate on purpose: a technical PASS never implies publication.
  TECHNICALLY_VALIDATED     G0, G3, G4, G5 pass and every narrated sentence passed ASR
  EDITORIAL_REVIEW_PENDING  claims not all EDITORIALLY_APPROVED (with records), factual_review not
                            verified, or a pronunciation override not CONFIRMED by a listener
  TTS_RIGHTS_PENDING        narration audio not entirely PUBLICATION_CLEARED, or the voice licence
                            record is not APPROVED by a named person
  PUBLICATION_READY         all gates PASS and nothing pending (exclusive)
"""
import json
from pathlib import Path

from pipeline import narration as nar
from pipeline import pronunciation as pron

STATUSES = ("TECHNICALLY_VALIDATED", "EDITORIAL_REVIEW_PENDING", "TTS_RIGHTS_PENDING", "PUBLICATION_READY")
# M5.5 production profiles (project.json "production_profile"): what the output is FOR decides
# which gates apply. A technical preview is never publication authorization.
PROFILES = ("TECHNICAL_SILENT_PREVIEW", "NARRATED_INTERNAL_REVIEW", "PUBLICATION_CANDIDATE", "INTERNAL_NARRATED_PREVIEW")
DEFAULT_PROFILE = "NARRATED_INTERNAL_REVIEW"   # projects without a profile get the strict narrated gates
PUBLICATION_METADATA = ("title", "description", "language", "credits")


def _read(path):
    path = Path(path)
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else None


PROFILE_ALIASES = {"INTERNAL_NARRATED_PREVIEW": "NARRATED_INTERNAL_REVIEW"}   # M6 spec name of the same profile


def profile_of(project):
    profile = (project or {}).get("production_profile") or DEFAULT_PROFILE
    return PROFILE_ALIASES.get(profile, profile)


def plan_gate(p):
    """GV (M5.5): the visual execution plan validates and its coverage report is current."""
    plan_path = p / "storyboard/visual_plan.json"
    if not plan_path.is_file():
        return None
    from planner import compiler, validate
    plan = _read(plan_path)
    errors = validate.validate_plan(plan, p, engine_check=False)
    story = _read(p / "storyboard/storyboard.json") or {}
    if story.get("plan_sha256") != compiler.plan_hash(plan):
        errors.append("storyboard.json was not compiled from the current visual_plan.json (run build-shots)")
    cov = _read(p / "qa/visual_coverage.json")
    if not cov or cov.get("executable") != plan.get("executable"):
        errors.append("qa/visual_coverage.json missing or out of date (run plan-visuals)")
    return ("PASS" if not errors else "FAIL", errors[:5] or [
        f"visual plan valid: {len(plan['shots'])} shots, coverage "
        + ", ".join(f"{k} {v}" for k, v in sorted(_counts(c["status"] for c in plan["coverage"]).items()))])


def _counts(items):
    out = {}
    for i in items:
        out[i] = out.get(i, 0) + 1
    return out


def silent_media(p, m, b, preset):
    """G4 for silent previews: Blender QA + media QA + staleness from the actual render
    dependencies (storyboard totals, per-shot render-cache keys), never from audio timing."""
    from tools import render_cache
    from tools.cli import shots, expected_frames
    notes, ok = [], True
    if not b:
        return "FAIL", ["no Blender QA report"]
    notes.append(f"Blender QA {b['passed']}/{b['total']}")
    ok &= b["failed"] == 0
    if not m:
        return "FAIL", notes + ["media QA missing (run preview)"]
    if m.get("problems"):
        return "FAIL", notes + m["problems"][:3]
    current = shots(p)
    total = sum(expected_frames(p, s) for s in current)
    stale = []
    if m.get("expected_total_frames") != total:
        stale.append(f"rendered for {m.get('expected_total_frames')} frames, storyboard now has {total}")
    keys = m.get("render_keys")
    if keys is None:
        stale.append("media report predates M5.5 (no render keys): re-run preview")
    else:
        for s in current:
            now = render_cache.cache_key(render_cache.components(p, s, preset))
            if keys.get(s["id"]) != now:
                stale.append(f"{s['id']} changed since the media were encoded")
    if stale:
        return "FAIL", notes + ["media QA is stale: " + "; ".join(stale[:4])]
    notes.append(f"silent media QA PASS ({total} frames, {len(current)} shots, render keys current)")
    return ("PASS" if ok else "FAIL"), notes


def _storyboard_claims(p):
    story = _read(p / "storyboard/storyboard.json") or {}
    return sorted({c for s in story.get("shots", []) for c in s.get("claim_ids", [])})


def evaluate(p, preset_suffix=""):
    """{"gates": {name: {status, notes}}, "statuses": [...], "verdict": str, "profile": str}."""
    p = Path(p)
    project = _read(p / "project.json") or {}
    profile = profile_of(project)
    if profile == "TECHNICAL_SILENT_PREVIEW":
        return _evaluate_silent(p, project, preset_suffix)
    result = _evaluate_narrated(p, preset_suffix)
    result["profile"] = profile
    gv = plan_gate(p)
    if gv:
        result["gates"]["GV visual plan & coverage"] = {"status": gv[0], "notes": gv[1]}
    if profile == "PUBLICATION_CANDIDATE":
        meta = project.get("publication_metadata") or {}
        missing = [k for k in PUBLICATION_METADATA if not str(meta.get(k) or "").strip()]
        g6 = result["gates"]["G6 final publication readiness"]
        if missing:
            g6["status"] = "BLOCKED"
            g6["notes"] = [f"FINAL gate: publication metadata missing {missing}"] + [n for n in g6["notes"]
                                                                                   if n != "all gates pass"]
        if gv and gv[0] != "PASS":
            g6["status"] = "BLOCKED"
            g6["notes"].append("FINAL gate: visual plan does not validate")
        if g6["status"] != "PASS" and "PUBLICATION_READY" in result["statuses"]:
            result["statuses"] = ["TECHNICALLY_VALIDATED"]
            result["verdict"] = "PUBLICATION CANDIDATE — BLOCKED (" + "; ".join(g6["notes"][:2]) + ")"
    elif "PUBLICATION_READY" in result["statuses"]:
        # Every gate passed, but this profile is an internal review: publication needs the
        # PUBLICATION_CANDIDATE profile (and its metadata), never an implicit promotion.
        result["statuses"] = ["TECHNICALLY_VALIDATED"]
        result["verdict"] = ("INTERNAL REVIEW — ALL GATES PASS; set production_profile PUBLICATION_CANDIDATE "
                             "(with publication_metadata) to evaluate publication")
    return result


def _evaluate_silent(p, project, preset_suffix):
    """TECHNICAL_SILENT_PREVIEW: plan, assets, Blender QA and silent media must pass; narration,
    TTS rights, timing lock and subtitles are NOT_APPLICABLE (not failures); never publishable."""
    from tools.validator import validate_project
    gates = {}
    errors, _ = validate_project(p)
    gates["G0 project & schema validation"] = ("PASS" if not errors else "FAIL", errors[:5] or ["validate passes"])
    gv = plan_gate(p)
    if gv:
        gates["GV visual plan & coverage"] = gv
    sources = _read(p / "research/sources.json") or {}
    claims = {c["id"]: c for c in sources.get("claims", [])}
    used = _storyboard_claims(p)
    statuses = {c: claims.get(c, {}).get("review_status") for c in used}
    unknown = [c for c in used if c not in claims]
    weak = [f"{c}: {s}" for c, s in statuses.items() if c in claims and s not in ("SOURCE_VERIFIED", "EDITORIALLY_APPROVED")]
    if unknown:
        g1 = ("FAIL", [f"claims not in research/sources.json: {unknown}"])
    elif weak:
        g1 = ("PENDING_EVIDENCE", weak + ["(a silent technical preview may show them; publication may not)"])
    elif all(s == "EDITORIALLY_APPROVED" for s in statuses.values()):
        g1 = ("PASS", [f"{len(used)} on-screen claims editorially approved"])
    else:
        g1 = ("PENDING_EDITORIAL", [f"{sum(s == 'EDITORIALLY_APPROVED' for s in statuses.values())}/{len(used)} "
                                    "on-screen claims editorially approved (source-verified only)"])
    gates["G1 evidence review"] = g1
    na = "NOT_APPLICABLE"
    gates["G2 narration audio & TTS rights"] = (na, ["silent technical preview: no narration audio"])
    gates["G3 narration timing lock"] = (na, ["silent technical preview: timing comes from the visual plan "
                                              f"({(_read(p / 'storyboard/visual_plan.json') or {}).get('timing_mode', 'storyboard')})"])
    preset = "preview" if not preset_suffix else preset_suffix.lstrip("_")
    b = (_read(p / "qa/blender_checks.json") or {}).get("summary")
    m = _read(p / "qa" / f"preview_media_report{preset_suffix}.json")
    gates["G4 Blender visual preview"] = silent_media(p, m, b, preset)
    gates["G5 media assembly & subtitles"] = (na, ["silent technical preview: no audio to assemble, no subtitles; "
                                                   "the silent MP4 is checked in G4"])
    gates["G6 final publication readiness"] = ("BLOCKED", ["profile TECHNICAL_SILENT_PREVIEW is a technical preview; "
                                                           "it is never publication-ready (no narration, no rights)"])
    technical = all(gates[g][0] == "PASS" for g in gates if g.startswith(("G0", "GV", "G4")))
    flags = (["TECHNICALLY_VALIDATED"] if technical else []) + (["EDITORIAL_REVIEW_PENDING"] if g1[0] != "PASS" else [])
    verdict = ("TECHNICAL PREVIEW — VALID (silent); NOT FOR PUBLICATION" if technical else
               "TECHNICAL PREVIEW — NOT VALID (" + "; ".join(g for g in gates if gates[g][0] == "FAIL"
                                                          and g.startswith(("G0", "GV", "G4"))) + ")")
    return {"verdict": verdict, "statuses": flags, "profile": "TECHNICAL_SILENT_PREVIEW",
            "gates": {k: {"status": v[0], "notes": v[1]} for k, v in gates.items()}}


def _evaluate_narrated(p, preset_suffix=""):
    """NARRATED_INTERNAL_REVIEW / PUBLICATION_CANDIDATE (the M3.5 gates, unchanged)."""
    from tools.validator import publication_audio_errors, validate_project
    from integrations.tts import providers
    gates = {}
    errors, _ = validate_project(p)
    gates["G0 project & schema validation"] = ("PASS" if not errors else "FAIL", errors[:5] or ["validate passes"])

    sources = _read(p / "research/sources.json") or {}
    narration = nar.load(p) or {}
    project = _read(p / "project.json") or {}
    lexicon = pron.load(p)
    claims = {c["id"]: c for c in sources.get("claims", [])}
    used = sorted({c for b in narration.get("beats", []) for c in b.get("claim_ids", [])})
    statuses = {c: claims.get(c, {}).get("review_status") for c in used}
    provider = (narration.get("voice") or {}).get("provider")
    entries = {e["id"]: e for e in lexicon.get("entries", [])}
    pending_pron = [f"{eid} ({entries[eid]['written']}) {entries[eid].get('status')}"
                    for eid in pron.used_entries(narration, lexicon, provider)
                    if entries[eid].get("status") != "CONFIRMED"]
    if any(s in (None, "REJECTED", "PROVISIONAL", "provisional") for s in statuses.values()):
        g1 = ("FAIL", [f"{c}: {s}" for c, s in statuses.items() if s not in ("SOURCE_VERIFIED", "EDITORIALLY_APPROVED")])
    elif all(s == "EDITORIALLY_APPROVED" for s in statuses.values()) and project.get("factual_review") == "verified" \
            and not pending_pron:
        g1 = ("PASS", [f"{len(used)} claims editorially approved; factual_review verified; pronunciations confirmed"])
    else:
        package = (narration.get("revision") or {}).get("review_package") or "review/EDITORIAL_APPROVAL_PACKAGE.md"
        notes = [f"{sum(s == 'EDITORIALLY_APPROVED' for s in statuses.values())}/{len(used)} narrated claims "
                 f"editorially approved (see {package})",
                 f"factual_review: {project.get('factual_review')}"]
        notes += [f"pronunciation pending: {x}" for x in pending_pron]
        g1 = ("PENDING_EDITORIAL", notes)
    gates["G1 evidence, script & pronunciation review"] = g1

    manifest = _read(p / "audio/narration_manifest.json") or {}
    current = {s["cache_key"] for b in manifest.get("beats", {}).values() for s in b["sentences"]}
    recs = [r for k, r in manifest.get("segments", {}).items() if k in current]
    asr = [r.get("asr", {}).get("pass") for r in recs]
    tech_ok = bool(asr) and all(asr)
    registry = providers.load_registry()
    rights_errors = publication_audio_errors(p, narration, registry, {"entries": []})  # pronunciation is G1
    licence = ((narration.get("voice") or {}).get("license") or {}).get("status")
    rights_ok = not rights_errors and licence == "APPROVED"
    classes = sorted({r.get("rights_class") or "UNKNOWN" for r in recs})
    gates["G2 narration audio & TTS rights"] = (
        "PASS" if tech_ok and rights_ok else ("BLOCKED_RIGHTS" if tech_ok else "FAIL"),
        [f"{len(asr)} sentences generated + ASR-verified" if tech_ok else "ASR check missing/failing",
         f"provider {provider}: rights class {', '.join(classes) or 'n/a'}; voice licence {licence}"]
        + rights_errors[:2])

    timing = _read(p / "script/timing.json") or {}
    timing_errors = [e for e in errors if "timing" in e]
    gates["G3 narration timing lock"] = ("PASS" if timing.get("locked") and not timing_errors else "FAIL",
                                         [f"{timing.get('total_frames')} frames, locked={timing.get('locked')}"]
                                         + timing_errors)
    b = (_read(p / "qa/blender_checks.json") or {}).get("summary")
    m = _read(p / "qa" / f"preview_media_report{preset_suffix}.json")
    total = timing.get("total_frames")
    media_stale = bool(m) and m.get("expected_total_frames") != total
    g4_ok = bool(b) and b["failed"] == 0 and bool(m) and not m.get("problems") and not media_stale
    gates["G4 Blender visual preview"] = ("PASS" if g4_ok else "FAIL",
                                          [f"Blender QA {b['passed']}/{b['total']}" if b else "no Blender QA report",
                                           ("media QA is stale (rendered for a different timing)" if media_stale else
                                            "media QA PASS" if m and not m.get("problems") else "media QA missing/failing")])
    a = _read(p / "qa" / f"assembly_report{preset_suffix}.json")
    a_stale = bool(a) and a.get("frames") != total
    gates["G5 media assembly & subtitles"] = (
        "PASS" if a and not a["problems"] and not a_stale else "FAIL",
        ["assembly report is stale (assembled for a different timing)"] if a_stale else
        a["problems"] if a and a["problems"] else
        ([f"{a['frames']} frames, {a['loudness_after']['integrated_lufs']} LUFS, "
          f"{a.get('subtitle_entries')} subtitle cues"] if a else ["not assembled"]))
    final_errors, _ = validate_project(p, final=True)
    final_errors = [e for e in final_errors if e.startswith("FINAL gate")]
    others_pass = all(v[0] == "PASS" for v in gates.values())
    gates["G6 final publication readiness"] = ("PASS" if not final_errors and others_pass else "BLOCKED",
                                               final_errors or ["all gates pass"])

    flags = []
    technical = all(gates[g][0] == "PASS" for g in gates if g.startswith(("G0", "G3", "G4", "G5"))) and tech_ok
    if technical:
        flags.append("TECHNICALLY_VALIDATED")
    if g1[0] != "PASS":
        flags.append("EDITORIAL_REVIEW_PENDING")
    if not rights_ok:
        flags.append("TTS_RIGHTS_PENDING")
    if gates["G6 final publication readiness"][0] == "PASS" and technical and len(flags) == 1:
        flags = ["PUBLICATION_READY"]
    if flags == ["PUBLICATION_READY"]:
        verdict = "PUBLICATION_READY"
    else:
        why = [f for f in flags if f != "TECHNICALLY_VALIDATED"] or [final_errors[0] if final_errors else "a gate failed"]
        if not technical:
            why.insert(0, "NOT TECHNICALLY VALIDATED")
        verdict = "INTERNAL PREVIEW — NOT PUBLICATION-READY (" + "; ".join(why) + ")"
    return {"verdict": verdict, "statuses": flags,
            "gates": {k: {"status": v[0], "notes": v[1]} for k, v in gates.items()}}
