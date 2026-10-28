"""Narrative beat contract (schemas/narrative_beats.schema.json): load, validate, timing, evidence."""
import hashlib
import json
from pathlib import Path

from planner import intents

TIMING_MODES = ("PROVISIONAL", "AUDIO_LOCKED")
BEAT_KINDS = ("framing", "fact", "interpretation")
COMPLEXITY = ("LOW", "MEDIUM", "HIGH")
CLAIM_OK = ("SOURCE_VERIFIED", "EDITORIALLY_APPROVED", "verified")
RESTRICTIONS = ("INTERNAL_ONLY", "PUBLICATION_CANDIDATE")


def load(path):
    path = Path(path)
    return json.loads(path.read_text(encoding="utf-8"))


def content_hash(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def validate(doc, sources=None):
    """Errors in a narrative beats document (empty when valid)."""
    errors = []
    for key in ("schema", "project_id", "timing_mode", "beats", "publication"):
        if key not in doc:
            errors.append(f"beats: missing '{key}'")
    if errors:
        return errors
    if doc["timing_mode"] not in TIMING_MODES:
        errors.append(f"beats: timing_mode must be one of {TIMING_MODES}")
    if (doc["publication"] or {}).get("restriction") not in RESTRICTIONS:
        errors.append(f"beats: publication.restriction must be one of {RESTRICTIONS}")
    claims = {c["id"]: c for c in (sources or {}).get("claims", [])}
    seen = set()
    for b in doc["beats"]:
        bid = b.get("beat_id")
        where = f"beat {bid}"
        if not bid or bid in seen:
            errors.append(f"beat id missing or duplicated: {bid!r}")
        seen.add(bid)
        if not (b.get("narration") or "").strip():
            errors.append(f"{where}: narration is empty")
        if b.get("kind") not in BEAT_KINDS:
            errors.append(f"{where}: kind must be one of {BEAT_KINDS}")
        if b.get("narrative_intent") not in intents.INTENTS:
            errors.append(f"{where}: unsupported visual intent {b.get('narrative_intent')!r} "
                          f"(supported: {', '.join(intents.INTENTS)})")
        if not b.get("visual_goal"):
            errors.append(f"{where}: visual_goal is required (what the viewer must understand)")
        if b.get("expected_complexity", "MEDIUM") not in COMPLEXITY:
            errors.append(f"{where}: expected_complexity must be one of {COMPLEXITY}")
        if not isinstance(b.get("required_concepts"), list):
            errors.append(f"{where}: required_concepts must be a list")
        for cid in b.get("claim_ids", []):
            if sources is not None and cid not in claims:
                errors.append(f"{where}: claim {cid} is not in research/sources.json")
        if b.get("kind") in ("fact", "interpretation") and not b.get("claim_ids"):
            errors.append(f"{where}: a {b.get('kind')} beat must cite claim_ids")
        t = b.get("timing") or {}
        if t.get("estimated_seconds") is not None and (not isinstance(t["estimated_seconds"], (int, float))
                                                        or t["estimated_seconds"] <= 0):
            errors.append(f"{where}: timing.estimated_seconds must be a positive number")
    return errors


def evidence_status(beat, sources):
    """(status, detail): FRAMING (no claims needed), INTERNAL_PREVIEW (claims source-verified,
    not editorially approved), APPROVED, or EVIDENCE_BLOCKED (a claim lacks evidence)."""
    claims = {c["id"]: c for c in (sources or {}).get("claims", [])}
    ids = beat.get("claim_ids", [])
    if not ids:
        return "FRAMING", "no factual claim"
    missing = [c for c in ids if c not in claims]
    weak = [c for c in ids if c in claims and claims[c].get("review_status") not in CLAIM_OK]
    if missing or weak:
        return "EVIDENCE_BLOCKED", (f"unknown claims {missing}" if missing else "") + \
            (f"; claims without verified evidence {weak}" if weak else "")
    if all(claims[c].get("review_status") in ("EDITORIALLY_APPROVED", "verified") for c in ids):
        return "APPROVED", "all claims editorially approved"
    return "INTERNAL_PREVIEW", "claims source-verified, not editorially approved"


def provisional_seconds(beat, cfg):
    """Estimated beat duration (PROVISIONAL): explicit estimate, else words / rate + padding.
    An estimate of a beat's length only; never used as speech or word timestamps."""
    t = beat.get("timing") or {}
    if t.get("estimated_seconds"):
        return float(t["estimated_seconds"])
    words = len(beat["narration"].split())
    return words / cfg["provisional_words_per_second"] + cfg["provisional_padding_seconds"]
