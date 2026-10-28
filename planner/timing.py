"""Beat timing for planning: PROVISIONAL estimates or AUDIO_LOCKED measured windows, and
minimum template durations computed by the real motion planner (never guessed)."""
import json
import math
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
