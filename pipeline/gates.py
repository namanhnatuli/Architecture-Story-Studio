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


def _read(path):
    path = Path(path)
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else None


def evaluate(p, preset_suffix=""):
    """{"gates": {name: {status, notes}}, "statuses": [...], "verdict": str}."""
    from tools.validator import publication_audio_errors, validate_project
    from integrations.tts import providers
    p = Path(p)
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
        notes = [f"{sum(s == 'EDITORIALLY_APPROVED' for s in statuses.values())}/{len(used)} narrated claims "
                 "editorially approved (see review/EDITORIAL_APPROVAL_PACKAGE.md)",
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
