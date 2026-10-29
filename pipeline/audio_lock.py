"""Audio-locked timing for planned (M5/M6) projects (pure Python, no audio decoding).

The M3 scheduler (pipeline/beat_scheduler.py) needs an authored storyboard template with
one shot per beat. Planned projects have several shots per beat, chosen by planner/ from
the *measured* narration, so the lock has two steps:

1. lock_beats  (`lock-audio`, after narrate + asr-check + align): script/timing.json with
   every beat's measured duration and sentence spans (relative to the beat audio), the
   pacing and the lock basis. `locked` only when every current sentence passed ASR and
   script/visual_beats.json narrates exactly the script's sentences (fail closed).
2. finalize    (`build-shots`, after the plan is compiled): the shots of the compiled
   storyboard (whole frames), each beat's audio placed at its window start + lead-in, the
   storyboard hash, the total; project.json gets the duration and audio_timing_locked.

A beat window is lead-in + measured speech + tail, rounded up to whole frames; the
planner never stretches or truncates narration to fit pictures (planner/timing.py).
"""
import hashlib
import json
import math
from pathlib import Path


class AudioLockError(ValueError):
    pass


def content_hash(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def beats_hash(timing):
    """What the visual plan depends on: beat durations, sentence spans and pacing."""
    return content_hash({"pacing": timing.get("pacing"),
                         "beats": [{"id": b["id"], "duration": b["duration"],
                                    "sentences": [[s.get("rel_start", s["start"]), s.get("rel_end", s["end"])]
                                                  for s in b.get("sentences", [])]}
                                   for b in timing.get("beats", [])]})


def _read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def lock_beats(project_dir):
    from pipeline import narration as nar, pronunciation as pron
    p = Path(project_dir)
    narration = nar.load(p)
    if narration is None:
        raise AudioLockError("script/narration.json missing")
    mpath = p / "audio/narration_manifest.json"
    if not mpath.is_file():
        raise AudioLockError("no measured narration; run `narrate` first")
    manifest = _read(mpath)
    if manifest.get("narration_sha256") != nar.narration_hash(narration, pron.load(p)):
        raise AudioLockError("narration.json changed since the audio was generated; run `narrate` again")
    problems = []
    beats_path = p / "script/visual_beats.json"
    if beats_path.is_file():
        visual = {b["beat_id"]: b for b in _read(beats_path)["beats"]}
        order = [b["id"] for b in narration["beats"]]
        if list(visual) != order:
            problems.append(f"visual_beats.json beats {list(visual)} differ from narration.json beats {order}")
        for b in narration["beats"]:
            text = " ".join(b["sentences"])
            if b["id"] in visual and visual[b["id"]]["narration"] != text:
                problems.append(f"{b['id']}: visual_beats narration differs from the narrated sentences")
    audio = manifest.get("beats") or {}
    beats = []
    for b in narration["beats"]:
        a = audio.get(b["id"])
        if a is None:
            raise AudioLockError(f"no measured audio for beat {b['id']}; run `narrate`")
        beats.append({"id": b["id"], "duration": a["duration"], "audio_file": a["file"], "audio_sha256": a["sha256"],
                      "sentences": [{"index": s["index"], "text": s["text"], "start": s["start"], "end": s["end"]}
                                    for s in a["sentences"]]})
    current = {s["cache_key"] for b in audio.values() for s in b["sentences"]}
    asr = [r.get("asr", {}).get("pass") for k, r in manifest["segments"].items()
           if r.get("role") == "sentence" and k in current]
    asr_ok = bool(asr) and len(asr) == len(current) and all(asr)
    if not asr_ok:
        problems.append("ASR check missing or failing for some sentences (run `asr-check`)")
    fps = int(_read(p / "project.json")["fps"])
    timing = {"schema": "timing/2", "mode": "PLANNED_AUDIO_LOCK", "stage": "BEATS_LOCKED", "fps": fps,
              "pacing": narration["pacing"], "locked": not problems, "problems": problems, "beats": beats,
              "lock_basis": {"narration_sha256": manifest["narration_sha256"],
                             "beat_audio_sha256": {b["id"]: b["audio_sha256"] for b in beats},
                             "asr_checked_sentences": len(asr), "asr_all_pass": asr_ok}}
    timing["beats_sha256"] = beats_hash(timing)
    (p / "script/timing.json").write_text(json.dumps(timing, indent=2, ensure_ascii=False) + "\n")
    project = _read(p / "project.json")
    project["audio_timing_locked"] = False    # set by finalize, once shots exist
    (p / "project.json").write_text(json.dumps(project, indent=2, ensure_ascii=False) + "\n")
    return timing


def window_frames(timing, beat, fps):
    pacing = timing["pacing"]
    seconds = pacing["beat_lead_in_seconds"] + beat["duration"] + pacing["beat_tail_seconds"]
    return int(math.ceil(seconds * fps - 1e-9))


def finalize(project_dir):
    """Shots + absolute beat/sentence times from the compiled storyboard (after build-shots)."""
    from pipeline import beat_scheduler
    p = Path(project_dir)
    timing = _read(p / "script/timing.json")
    if timing.get("mode") != "PLANNED_AUDIO_LOCK":
        raise AudioLockError("script/timing.json was not written by `lock-audio`")
    if not timing.get("locked"):
        raise AudioLockError("timing is not locked: " + "; ".join(timing.get("problems") or ["unknown"]))
    story = _read(p / "storyboard/storyboard.json")
    plan = _read(p / "storyboard/visual_plan.json")
    if plan.get("inputs", {}).get("timing_sha256") != timing["beats_sha256"]:
        raise AudioLockError("the visual plan was made from other beat timings; re-run plan-visuals")
    fps = timing["fps"]
    lead = timing["pacing"]["beat_lead_in_seconds"]
    shots, frame = [], 0
    for s in story["shots"]:
        n = int(round(s["duration_seconds"] * fps))
        shots.append({"id": s["id"], "start_frame": frame, "frames": n, "start_seconds": frame / fps,
                      "duration_seconds": n / fps, "beat_ids": list(s["beat_ids"])})
        frame += n
    beats = []
    for b in timing["beats"]:
        own = [s for s in shots if s["beat_ids"] == [b["id"]]]
        if not own:
            raise AudioLockError(f"beat {b['id']} has no shot in the storyboard")
        first, n = own[0], sum(s["frames"] for s in own)
        if n != window_frames(timing, b, fps):
            raise AudioLockError(f"beat {b['id']}: shots last {n} frames, the measured window is "
                                 f"{window_frames(timing, b, fps)} (plan and audio disagree)")
        start = first["start_seconds"] + lead
        beats.append(dict(b, shot=first["id"], shots=[s["id"] for s in own], start_seconds=round(start, 6),
                          sentences=[dict(x, start=round(start + x.get("rel_start", x["start"]), 6),
                                          end=round(start + x.get("rel_end", x["end"]), 6),
                                          rel_start=x.get("rel_start", x["start"]), rel_end=x.get("rel_end", x["end"]))
                                     for x in b["sentences"]]))   # idempotent: offsets are the measured spans
    timing.update(stage="SHOTS_SCHEDULED", shots=shots, beats=beats, total_frames=frame, total_seconds=frame / fps,
                  storyboard_sha256=beat_scheduler.content_hash(story), plan_sha256=story.get("plan_sha256"))
    (p / "script/timing.json").write_text(json.dumps(timing, indent=2, ensure_ascii=False) + "\n")
    project = _read(p / "project.json")
    project["duration_seconds"] = timing["total_seconds"]
    project["audio_timing_locked"] = True
    (p / "project.json").write_text(json.dumps(project, indent=2, ensure_ascii=False) + "\n")
    return timing


def check_consistency(timing):
    """Errors in a finalized manifest (independent re-derivation): contiguous whole-frame shots,
    beats inside their shots in order, sentences inside their beat, no overlaps."""
    errors = []
    fps = timing.get("fps")
    frame = 0
    for s in timing.get("shots", []):
        if s["start_frame"] != frame:
            errors.append(f"{s['id']}: starts at frame {s['start_frame']}, expected {frame} (gap or overlap)")
        if abs(s["duration_seconds"] * fps - s["frames"]) > 1e-6:
            errors.append(f"{s['id']}: duration is not {s['frames']} whole frames")
        frame = s["start_frame"] + s["frames"]
    if timing.get("total_frames") != frame:
        errors.append(f"total_frames {timing.get('total_frames')} differs from the shots ({frame})")
    by_id = {s["id"]: s for s in timing.get("shots", [])}
    end_prev = -1.0
    for b in timing.get("beats", []):
        own = [by_id[x] for x in b.get("shots", [b.get("shot")]) if x in by_id]
        if not own:
            errors.append(f"{b['id']}: unknown shots {b.get('shots')}")
            continue
        lo = own[0]["start_seconds"]
        hi = own[-1]["start_seconds"] + own[-1]["duration_seconds"]
        if b["start_seconds"] < lo - 1e-6 or b["start_seconds"] + b["duration"] > hi + 1e-6:
            errors.append(f"{b['id']}: audio {b['start_seconds']:.3f}-{b['start_seconds'] + b['duration']:.3f} s "
                          f"is outside its shots {lo:.3f}-{hi:.3f} s")
        if b["start_seconds"] < end_prev - 1e-6:
            errors.append(f"{b['id']}: overlaps the previous beat")
        end_prev = b["start_seconds"] + b["duration"]
        for x in b.get("sentences", []):
            if "rel_start" in x and abs(x["start"] - (b["start_seconds"] + x["rel_start"])) > 2e-6:
                errors.append(f"{b['id']}.s{x['index']}: absolute start differs from beat start + measured offset")
            if not (b["start_seconds"] - 1e-6 <= x["start"] <= x["end"] <= end_prev + 1e-6):
                errors.append(f"{b['id']}.s{x['index']}: sentence {x['start']:.3f}-{x['end']:.3f} s is outside its beat")
    return errors
