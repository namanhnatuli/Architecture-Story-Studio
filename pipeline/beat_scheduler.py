"""Narration-first scheduling (pure Python, no bpy, no audio decoding).

Inputs: measured beat audio (audio/narration_manifest.json), pacing
(script/narration.json) and the authoring storyboard (storyboard.template.json).
Outputs: script/timing.json (frame-exact timing manifest) and the generated
storyboard/storyboard.json the Blender engine renders.

Rules
- A shot's length = lead-in + its beats (with gaps) + tail, rounded UP to whole
  frames; extended (never shortened) when its animation needs longer. Narration
  is never stretched to fit pictures.
- Animation times may be anchors relative to the shot start:
  "@B3.s1+0.4" (beat B3, sentence 1 start, +0.4 s), "@B3" / "@B3.start", "@B3.end".
- Every narration beat belongs to exactly one shot, in narration order.
"""
import copy
import hashlib
import json
import math
import re
from pathlib import Path

from engine import motion, templates

ANCHOR = re.compile(r"^@(?P<beat>[A-Za-z0-9_]+)(?:\.(?P<part>s\d+|start|end))?(?P<offset>[+-]\d+(?:\.\d+)?)?$")


class ScheduleError(ValueError):
    pass


def _ceil_frames(seconds, fps):
    return int(math.ceil(round(seconds * fps, 6)))


def _resolve(value, beat_local, where):
    """Replace anchor strings (recursively) by seconds relative to the shot start."""
    if isinstance(value, dict):
        return {k: _resolve(v, beat_local, f"{where}.{k}") for k, v in value.items()}
    if isinstance(value, list):
        return [_resolve(v, beat_local, f"{where}[{i}]") for i, v in enumerate(value)]
    if not (isinstance(value, str) and value.startswith("@")):
        return value
    m = ANCHOR.match(value)
    if not m:
        raise ScheduleError(f"{where}: bad anchor {value!r} (use @B1, @B1.s0+0.3, @B1.end)")
    beat = beat_local.get(m.group("beat"))
    if beat is None:
        raise ScheduleError(f"{where}: anchor {value!r} names a beat that is not in this shot")
    part = m.group("part") or "start"
    if part == "start":
        t = beat["start"]
    elif part == "end":
        t = beat["start"] + beat["duration"]
    else:
        idx = int(part[1:])
        if idx >= len(beat["sentences"]):
            raise ScheduleError(f"{where}: {value!r} — beat has {len(beat['sentences'])} sentences")
        t = beat["start"] + beat["sentences"][idx]["start"]
    return round(t + float(m.group("offset") or 0.0), 6)


def _animation_min_frames(shot, states, fps):
    """Smallest frame count for which the shot's template plans without a timing error."""
    if shot.get("visual_type", "BLENDER_3D") != "BLENDER_3D":
        return 1
    lo, hi = 2, 24 * 600
    probe = dict(shot)

    def fits(n):
        probe["duration_seconds"] = n / fps
        if isinstance(probe.get("animation"), dict) and "duration_seconds" in probe["animation"]:
            probe["animation"] = dict(probe["animation"], duration_seconds=n / fps)
        try:
            templates.plan_shot(probe, states, fps, templates.placeholder_slots(probe, states))
            return True
        except motion.PlanError as e:
            if "timing needs" in str(e) or "after the last frame" in str(e) or "before the shot does" in str(e):
                return False
            raise ScheduleError(str(e)) from None
    if not fits(hi):
        raise ScheduleError(f"{shot['id']}: animation does not fit even in {hi / fps:.0f}s")
    while lo < hi:
        mid = (lo + hi) // 2
        if fits(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo


def _graphic_min_frames(shot, fps):
    g = shot.get("graphic") or {}
    last = max([e.get("appear", 0.0) for e in g.get("elements", [])] or [0.0])
    return _ceil_frames(last + float(g.get("fade_seconds", 0.4)) + 0.5, fps)


def schedule(narration, manifest, template, states, fps):
    pacing = narration["pacing"]
    lead, tail = pacing["beat_lead_in_seconds"], pacing["beat_tail_seconds"]
    beats_audio = manifest.get("beats") or {}
    order = [b["id"] for b in narration["beats"]]
    missing = [b for b in order if b not in beats_audio]
    if missing:
        raise ScheduleError(f"no measured audio for beats {missing}; run `narrate` first")
    claims_of = {b["id"]: b.get("claim_ids", []) for b in narration["beats"]}
    text_of = {b["id"]: " ".join(b["sentences"]) for b in narration["beats"]}

    used = [b for s in template["shots"] for b in s.get("beat_ids", [])]
    if used != order:
        raise ScheduleError(f"shots must cover every beat exactly once, in narration order: got {used}, expected {order}")

    shots_out, timing_shots, timing_beats = [], [], []
    start_frame = 0
    for tshot in template["shots"]:
        sid = tshot["id"]
        beat_local, t = {}, lead
        for i, bid in enumerate(tshot["beat_ids"]):
            if i:
                t += tail + lead
            a = beats_audio[bid]
            beat_local[bid] = {"start": t, "duration": a["duration"], "sentences": a["sentences"]}
            t += a["duration"]
        narration_seconds = t + tail
        shot = copy.deepcopy(tshot)
        for key in ("animation", "graphic"):
            if key in shot:
                shot[key] = _resolve(shot[key], beat_local, f"{sid}.{key}")
        shot["narration"] = " ".join(text_of[b] for b in tshot["beat_ids"])
        shot["claim_ids"] = sorted({c for b in tshot["beat_ids"] for c in claims_of[b]})
        n_narr = _ceil_frames(narration_seconds, fps)
        n_anim = (_graphic_min_frames(shot, fps) if shot.get("visual_type") == "MOTION_GRAPHICS"
                  else _animation_min_frames(shot, states, fps))
        frames = max(n_narr, n_anim)
        shot["start_seconds"] = start_frame / fps
        shot["duration_seconds"] = frames / fps
        if isinstance(shot.get("animation"), dict) and "duration_seconds" in shot["animation"]:
            shot["animation"]["duration_seconds"] = frames / fps
        shots_out.append(shot)
        shot_beats = []
        for bid in tshot["beat_ids"]:
            b = beat_local[bid]
            absolute = start_frame / fps + b["start"]
            entry = {"id": bid, "shot": sid, "audio_file": beats_audio[bid]["file"],
                     "audio_sha256": beats_audio[bid]["sha256"], "start_seconds": round(absolute, 6),
                     "duration": b["duration"],
                     "sentences": [{"index": s["index"], "text": s["text"],
                                    "start": round(absolute + s["start"], 6), "end": round(absolute + s["end"], 6)}
                                   for s in b["sentences"]]}
            shot_beats.append(entry)
            timing_beats.append(entry)
        timing_shots.append({"id": sid, "start_frame": start_frame, "frames": frames,
                             "start_seconds": start_frame / fps, "duration_seconds": frames / fps,
                             "narration_seconds": round(narration_seconds, 6),
                             "animation_min_seconds": round(n_anim / fps, 6),
                             "extended_by_animation": n_anim > n_narr, "beat_ids": tshot["beat_ids"]})
        start_frame += frames

    key_stills = []
    for still in template.get("key_stills", []):
        s = dict(still)
        if isinstance(s.get("time_seconds"), str):
            tshot = next(x for x in template["shots"] if x["id"] == s["shot"])
            local, t = {}, lead
            for i, bid in enumerate(tshot["beat_ids"]):
                if i:
                    t += tail + lead
                a = beats_audio[bid]
                local[bid] = {"start": t, "duration": a["duration"], "sentences": a["sentences"]}
                t += a["duration"]
            s["time_seconds"] = _resolve(s["time_seconds"], local, f"key_stills.{s['id']}")
        key_stills.append(s)

    total_frames = start_frame
    storyboard = {"generated_by": "pipeline/beat_scheduler.py — do not edit; edit storyboard.template.json",
                  "key_stills": key_stills, "shots": shots_out}
    timing = {"fps": fps, "total_frames": total_frames, "total_seconds": total_frames / fps,
              "pacing": pacing, "shots": timing_shots, "beats": timing_beats}
    return storyboard, timing


def content_hash(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def run(project_dir, lock=True):
    """Schedule the project from files; write timing.json + storyboard.json (+ project duration)."""
    from pipeline import narration as nar
    p = Path(project_dir)
    project = json.loads((p / "project.json").read_text())
    narration = nar.load(p)
    manifest = json.loads((p / "audio/narration_manifest.json").read_text())
    template = json.loads((p / "storyboard/storyboard.template.json").read_text())
    states = json.loads((p / "storyboard/states.json").read_text())
    if manifest.get("narration_sha256") != nar.narration_hash(narration):
        raise ScheduleError("narration.json changed since the audio was generated; run `narrate` again")
    storyboard, timing = schedule(narration, manifest, template, states, int(project["fps"]))
    sentence_records = [r for r in manifest["segments"].values() if r.get("role") == "sentence"]
    current = {s["cache_key"] for b in manifest["beats"].values() for s in b["sentences"]}
    asr = [r.get("asr", {}).get("pass") for r in sentence_records if r["cache_key"] in current]
    timing["locked"] = bool(lock and asr and all(asr))
    timing["lock_basis"] = {"narration_sha256": manifest["narration_sha256"],
                            "beat_audio_sha256": {b: v["sha256"] for b, v in manifest["beats"].items()},
                            "asr_checked_sentences": len(asr), "asr_all_pass": bool(asr) and all(asr)}
    timing["storyboard_sha256"] = content_hash(storyboard)
    (p / "script/timing.json").write_text(json.dumps(timing, indent=2, ensure_ascii=False) + "\n")
    (p / "storyboard/storyboard.json").write_text(json.dumps(storyboard, indent=2, ensure_ascii=False) + "\n")
    project["duration_seconds"] = timing["total_seconds"]
    project["audio_timing_locked"] = timing["locked"]
    (p / "project.json").write_text(json.dumps(project, indent=2, ensure_ascii=False) + "\n")
    return timing
