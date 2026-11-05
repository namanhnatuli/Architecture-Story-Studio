"""Beat timing for planning: PROVISIONAL estimates or AUDIO_LOCKED measured windows, and
minimum template durations computed by the real motion planner (never guessed)."""
import json
import math
import re
from pathlib import Path

from engine import motion, templates
from planner import beats as B


class TimingError(ValueError):
    pass


def frames(seconds, fps):
    return int(math.ceil(seconds * fps - 1e-9))


def beat_windows(doc, project_dir, cfg):
    """{beat_id: (seconds, source)} for every beat."""
    if doc["timing_mode"] == "PROVISIONAL":
        return {b["beat_id"]: (B.provisional_seconds(b, cfg), "PROVISIONAL") for b in doc["beats"]}
    path = Path(project_dir) / "script" / "timing.json"
    if not path.is_file():
        raise TimingError("timing_mode AUDIO_LOCKED needs script/timing.json (measured narration, M3 `schedule`)")
    timing = json.loads(path.read_text())
    if not timing.get("locked"):
        raise TimingError("script/timing.json is not locked (ASR/measurement incomplete): cannot plan AUDIO_LOCKED")
    pacing = timing.get("pacing") or {}
    lead, tail = pacing.get("beat_lead_in_seconds", 0.0), pacing.get("beat_tail_seconds", 0.0)
    measured = {b["id"]: b["duration"] for b in timing.get("beats", [])}
    missing = [b["beat_id"] for b in doc["beats"] if b["beat_id"] not in measured]
    if missing:
        raise TimingError(f"AUDIO_LOCKED: no measured audio for beats {missing}")
    return {b["beat_id"]: (lead + measured[b["beat_id"]] + tail, "AUDIO_LOCKED") for b in doc["beats"]}


def split_sentences(narration):
    """Sentences of a beat's narration text (the narration script splits the same way)."""
    import re
    return [s for s in re.split(r"(?<=[.?!])\s+", narration.strip()) if s]


def sentence_offsets(doc, project_dir, cfg):
    """{beat_id: [(start, end), ...]}: each sentence's span in seconds from the start of its
    beat window. AUDIO_LOCKED: measured (lead-in + sentence span in the beat audio);
    PROVISIONAL: word-proportional estimate inside the estimated window."""
    out = {}
    if doc["timing_mode"] == "AUDIO_LOCKED":
        timing = json.loads((Path(project_dir) / "script" / "timing.json").read_text())
        lead = (timing.get("pacing") or {}).get("beat_lead_in_seconds", 0.0)
        for b in timing.get("beats", []):
            out[b["id"]] = [(round(lead + s.get("rel_start", s["start"]), 6), round(lead + s.get("rel_end", s["end"]), 6))
                            for s in b.get("sentences", [])]
        return out
    for b in doc["beats"]:
        sentences = split_sentences(b["narration"])
        words = [len(s.split()) for s in sentences]
        total = B.provisional_seconds(b, cfg)
        pad = cfg["provisional_padding_seconds"] / 2
        speech = max(total - 2 * pad, 0.1)
        t, spans = pad, []
        for w in words:
            d = speech * w / max(sum(words), 1)
            spans.append((round(t, 6), round(t + d, 6)))
            t += d
        out[b["beat_id"]] = spans
    return out


def norm_word(text):
    return re.sub(r"[^a-z0-9']", "", text.lower().replace("’", "'"))


def word_offsets(doc, project_dir):
    """M7: {beat_id: [[(word, start, end), ...] per sentence]}: Whisper word timestamps of the
    current narration (audio/narration_manifest.json alignment), in seconds from the start of the
    beat window like sentence_offsets. AUDIO_LOCKED only; empty when nothing is aligned."""
    if doc["timing_mode"] != "AUDIO_LOCKED":
        return {}
    p = Path(project_dir)
    mpath = p / "audio" / "narration_manifest.json"
    if not mpath.is_file():
        return {}
    timing = json.loads((p / "script" / "timing.json").read_text())
    manifest = json.loads(mpath.read_text())
    lead = (timing.get("pacing") or {}).get("beat_lead_in_seconds", 0.0)
    out = {}
    for b in timing.get("beats", []):
        current = (manifest.get("beats", {}).get(b["id"]) or {}).get("sentences", [])
        rows = []
        for s, cur in zip(b.get("sentences", []), current):
            seg = manifest.get("segments", {}).get(cur.get("cache_key")) or {}
            align = seg.get("alignment") or {}
            base = lead + s.get("rel_start", s["start"])
            rows.append([(norm_word(w["text"]), round(base + w["start"], 6), round(base + w["end"], 6))
                         for w in align.get("words", [])] if align.get("segment_sha256") == seg.get("sha256") else [])
        out[b["id"]] = rows
    return out


def plans(shot, states, fps):
    """True if the storyboard shot plans without a timing error."""
    try:
        templates.plan_shot(shot, states, fps, templates.placeholder_slots(shot, states))
        return True
    except motion.PlanError as e:
        msg = str(e)
        if any(k in msg for k in ("timing needs", "after the last frame", "before the shot does",
                                  "must finish before the last frame", "TOO_SHORT")):
            return False
        raise


def min_frames(make_shot, states, fps, limit_seconds=120):
    """Smallest frame count n for which make_shot(n) builds and plans (binary search)."""
    def ok(n):
        try:
            shot = make_shot(n)
        except TooShort:
            return False
        return plans(shot, states, fps)
    hi = limit_seconds * fps
    if not ok(hi):
        raise TimingError("the visual does not fit even in 120 s")
    lo = 2
    while lo < hi:
        mid = (lo + hi) // 2
        if ok(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo


class TooShort(ValueError):
    """A config builder cannot keep its minimum holds within the duration."""
