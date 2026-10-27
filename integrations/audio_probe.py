"""Measured audio facts via ffprobe/ffmpeg (stdlib only). Never estimates from word counts."""
import json
import re
import shutil
import subprocess


class AudioValidationError(ValueError):
    """Audio file is missing, undecodable, silent or implausible."""


def _bin(name):
    path = shutil.which(name)
    if not path:
        raise AudioValidationError(f"{name} not found (brew install ffmpeg)")
    return path


def probe(path):
    """Codec, sample rate, channels and duration as decoded by ffprobe."""
    out = subprocess.run([_bin("ffprobe"), "-v", "error", "-select_streams", "a:0",
                          "-show_entries", "stream=codec_name,sample_rate,channels",
                          "-show_entries", "format=duration", "-of", "json", str(path)],
                         capture_output=True, text=True)
    if out.returncode != 0:
        raise AudioValidationError(f"ffprobe cannot decode {path}: {out.stderr.strip()[:200]}")
    data = json.loads(out.stdout or "{}")
    streams = data.get("streams") or []
    if not streams:
        raise AudioValidationError(f"{path} has no audio stream")
    s = streams[0]
    duration = (data.get("format") or {}).get("duration")
    if duration in (None, "N/A"):  # e.g. a WAV header with zero samples
        raise AudioValidationError(f"{path} has no decodable duration (empty audio?)")
    return {"codec": s.get("codec_name"), "sample_rate": int(s.get("sample_rate", 0)),
            "channels": int(s.get("channels", 0)), "duration": float(duration)}


def levels(path):
    """Mean and peak level in dBFS (ffmpeg volumedetect)."""
    out = subprocess.run([_bin("ffmpeg"), "-v", "info", "-nostats", "-i", str(path),
                          "-af", "volumedetect", "-f", "null", "-"], capture_output=True, text=True)
    mean = re.search(r"mean_volume:\s*(-?[\d.]+|-inf) dB", out.stderr)
    peak = re.search(r"max_volume:\s*(-?[\d.]+|-inf) dB", out.stderr)
    if not mean or not peak:
        raise AudioValidationError(f"could not measure levels of {path}")
    as_float = lambda m: float("-inf") if m.group(1) == "-inf" else float(m.group(1))
    return {"mean_db": as_float(mean), "peak_db": as_float(peak)}


def validate_speech(path, text, min_wps=1.5, max_wps=4.5, min_peak_db=-35.0):
    """Probe + levels + speech-rate sanity for one synthesized utterance.

    The rate bound catches truncated or runaway generations (e.g. 3 words in 10 s).
    """
    info = probe(path)
    info.update(levels(path))
    if info["duration"] < 0.2:
        raise AudioValidationError(f"{path}: duration {info['duration']:.2f}s is too short")
    if info["peak_db"] < min_peak_db:
        raise AudioValidationError(f"{path}: peak {info['peak_db']} dBFS, audio is (near) silent")
    words = len(re.findall(r"[A-Za-z0-9']+", text))
    info["words"] = words
    info["words_per_second"] = round(words / info["duration"], 3) if info["duration"] else 0.0
    if words >= 3 and not min_wps <= info["words_per_second"] <= max_wps:
        raise AudioValidationError(f"{path}: {info['words_per_second']} words/s is outside "
                                   f"{min_wps}-{max_wps}; generation is likely truncated or garbled")
    return info
