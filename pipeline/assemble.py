"""Narration track, loudness, mux and subtitles from the locked timing (stdlib + ffmpeg).

- The narration track has exactly the video's length (frames / fps); each beat's
  measured audio is placed at its scheduled start, silence elsewhere.
- Loudness: two-pass ffmpeg loudnorm (linear) to LOUDNESS_TARGET, true peak TRUE_PEAK.
- Subtitles: sentence-level SRT from measured sentence spans (no invented word timings).
- QA: A/V duration drift <= 1 frame, loudness within +/-1 LU, true peak, SRT sanity.
"""
import json
import re
import subprocess
import wave
from pathlib import Path

from integrations import audio_probe

LOUDNESS_TARGET = -16.0   # LUFS integrated (speech-led; YouTube normalises down to about -14)
TRUE_PEAK = -1.5          # dBTP
LRA = 11.0
SUB_LINE_CHARS = 42


def _ffmpeg(*args):
    return subprocess.run([audio_probe._bin("ffmpeg"), "-hide_banner", *map(str, args)], capture_output=True, text=True)


def build_narration_track(project_dir, timing, out_path, shot_ids=None):
    """Place beat audio at scheduled times. shot_ids limits to a contiguous subset (smoke test),
    with times re-based to the first selected shot."""
    p = Path(project_dir)
    fps = timing["fps"]
    shots = [s for s in timing["shots"] if shot_ids is None or s["id"] in shot_ids]
    if not shots:
        raise ValueError("no shots selected")
    origin = shots[0]["start_frame"]
    frames = sum(s["frames"] for s in shots)
    beats = [b for b in timing["beats"] if b["shot"] in {s["id"] for s in shots}]
    params, buf = None, None
    for beat in beats:
        with wave.open(str(p / beat["audio_file"]), "rb") as w:
            if params is None:
                params = (w.getnchannels(), w.getsampwidth(), w.getframerate())
                if params[2] % fps:
                    raise ValueError(f"sample rate {params[2]} is not a multiple of {fps} fps")
                buf = bytearray(frames * (params[2] // fps) * params[0] * params[1])
            elif (w.getnchannels(), w.getsampwidth(), w.getframerate()) != params:
                raise ValueError(f"{beat['audio_file']}: audio format differs")
            data = w.readframes(w.getnframes())
        bytes_per = params[0] * params[1]
        start = int(round((beat["start_seconds"] - origin / fps) * params[2])) * bytes_per
        if start < 0 or start + len(data) > len(buf):
            raise ValueError(f"beat {beat['id']} does not fit inside its shot(s)")
        if any(buf[start:start + len(data)]):
            raise ValueError(f"beat {beat['id']} overlaps another beat")
        buf[start:start + len(data)] = data
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(out_path), "wb") as w:
        w.setnchannels(params[0])
        w.setsampwidth(params[1])
        w.setframerate(params[2])
        w.writeframes(bytes(buf))
    return {"path": str(out_path), "frames": frames, "seconds": frames / fps, "beats": [b["id"] for b in beats],
            "origin_frame": origin}


def loudnorm(src, dst, sample_rate=48000):
    first = _ffmpeg("-i", src, "-af", f"loudnorm=I={LOUDNESS_TARGET}:TP={TRUE_PEAK}:LRA={LRA}:print_format=json",
                    "-f", "null", "-")
    m = re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", first.stderr, re.S)
    if first.returncode != 0 or not m:
        raise RuntimeError(f"loudnorm measure failed: {first.stderr[-300:]}")
    meas = json.loads(m.group(0))
    second = _ffmpeg("-y", "-i", src, "-af",
                     f"loudnorm=I={LOUDNESS_TARGET}:TP={TRUE_PEAK}:LRA={LRA}:measured_I={meas['input_i']}:"
                     f"measured_TP={meas['input_tp']}:measured_LRA={meas['input_lra']}:"
                     f"measured_thresh={meas['input_thresh']}:offset={meas['target_offset']}:linear=true",
                     "-ar", sample_rate, "-c:a", "pcm_s16le", dst)
    if second.returncode != 0:
        raise RuntimeError(f"loudnorm apply failed: {second.stderr[-300:]}")
    return meas


def ebur128(path):
    out = _ffmpeg("-nostats", "-i", path, "-af", "ebur128=peak=true", "-f", "null", "-")
    i = re.findall(r"I:\s*(-?[\d.]+) LUFS", out.stderr)
    tp = re.findall(r"Peak:\s*(-?[\d.]+|-inf) dBFS", out.stderr)
    if not i:
        raise RuntimeError("ebur128 measurement failed")
    return {"integrated_lufs": float(i[-1]), "true_peak_dbtp": float(tp[-1]) if tp and tp[-1] != "-inf" else None}


def mux(video, audio, out):
    r = _ffmpeg("-y", "-i", video, "-i", audio, "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy",
                "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", out)
    if r.returncode != 0:
        raise RuntimeError(f"mux failed: {r.stderr[-300:]}")


def _srt_time(t):
    ms = int(round(t * 1000))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def _wrap(text, width=SUB_LINE_CHARS):
    """One line if it fits, else two balanced lines (split minimising the longer line)."""
    text = " ".join(text.split())
    if len(text) <= width:
        return text
    spaces = [i for i, ch in enumerate(text) if ch == " "]
    best = min(spaces, key=lambda i: max(len(text[:i]), len(text[i + 1:])))
    return text[:best] + "\n" + text[best + 1:]


def write_srt(timing, out, shot_ids=None, origin_seconds=0.0):
    """Sentence-level subtitles from measured sentence spans."""
    entries = []
    for beat in timing["beats"]:
        if shot_ids is not None and beat["shot"] not in shot_ids:
            continue
        for s in beat["sentences"]:
            entries.append((s["start"] - origin_seconds, s["end"] - origin_seconds, s["text"]))
    lines = []
    for i, (a, b, text) in enumerate(entries, 1):
        lines += [str(i), f"{_srt_time(a)} --> {_srt_time(b)}", _wrap(text), ""]
    Path(out).write_text("\n".join(lines), encoding="utf-8")
    return entries


def check_srt(entries, duration):
    problems, last = [], 0.0
    for a, b, text in entries:
        if not (0 <= a < b <= duration + 1e-6):
            problems.append(f"subtitle {text[:30]!r} at {a:.2f}-{b:.2f}s is outside 0-{duration:.2f}s")
        if a < last - 1e-6:
            problems.append(f"subtitle {text[:30]!r} overlaps the previous one")
        last = b
    return problems


def assemble(project_dir, video, out_mp4, shot_ids=None, log=print):
    """Build narration track (+loudnorm), mux with `video`, write SRT, verify; returns a report."""
    p = Path(project_dir)
    timing = json.loads((p / "script/timing.json").read_text())
    tag = "full" if shot_ids is None else "_".join(shot_ids)
    raw = p / "audio" / f"narration_track_{tag}.wav"
    track = build_narration_track(p, timing, raw, shot_ids)
    mixed = p / "audio" / f"narration_mix_{tag}.wav"
    measured_in = loudnorm(raw, mixed)
    out_mp4 = Path(out_mp4)
    out_mp4.parent.mkdir(parents=True, exist_ok=True)
    mux(video, mixed, out_mp4)
    srt = out_mp4.with_suffix(".en.srt")
    entries = write_srt(timing, srt, shot_ids, track["origin_frame"] / timing["fps"])

    probe = json.loads(subprocess.run(
        [audio_probe._bin("ffprobe"), "-v", "error", "-count_frames", "-show_entries",
         "stream=codec_type,codec_name,nb_read_frames,duration,sample_rate,width,height:format=duration",
         "-of", "json", str(out_mp4)], capture_output=True, text=True, check=True).stdout)
    streams = {s["codec_type"]: s for s in probe["streams"]}
    fps = timing["fps"]
    problems = []
    v, a = streams.get("video"), streams.get("audio")
    if not v or not a:
        problems.append("output must have one video and one audio stream")
    else:
        if int(v["nb_read_frames"]) != track["frames"]:
            problems.append(f"video has {v['nb_read_frames']} frames, timing says {track['frames']}")
        drift = abs(float(a["duration"]) - track["seconds"])
        if drift > 1.0 / fps + 0.03:  # AAC priming/padding is < 25 ms
            problems.append(f"audio/video drift {drift * 1000:.0f} ms exceeds one frame")
    loud = ebur128(out_mp4)
    if abs(loud["integrated_lufs"] - LOUDNESS_TARGET) > 1.0:
        problems.append(f"integrated loudness {loud['integrated_lufs']} LUFS is not {LOUDNESS_TARGET} +/- 1")
    if loud["true_peak_dbtp"] is not None and loud["true_peak_dbtp"] > -1.0:
        problems.append(f"true peak {loud['true_peak_dbtp']} dBTP exceeds -1.0")
    problems += check_srt(entries, track["seconds"])
    report = {"output": str(out_mp4), "subtitles": str(srt), "narration_track": str(mixed), "shots": shot_ids or "all",
              "frames": track["frames"], "seconds": track["seconds"],
              "video": v, "audio": a, "loudness_before": {"I": measured_in["input_i"], "TP": measured_in["input_tp"]},
              "loudness_after": loud, "subtitle_entries": len(entries), "problems": problems}
    for line in (f"  {out_mp4.name}: {track['frames']} frames, {track['seconds']:.3f}s",
                 f"  loudness {loud['integrated_lufs']} LUFS, true peak {loud['true_peak_dbtp']} dBTP",
                 f"  subtitles: {len(entries)} sentence cues -> {srt.name}"):
        log(line)
    return report
