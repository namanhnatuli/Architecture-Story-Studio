"""Intelligibility check of narration: Whisper transcript vs script text (word error rate).

The Whisper run uses an external interpreter (env OMNIVOICE_PYTHON, default
$OMNIVOICE_HOME/.venv/bin/python, OMNIVOICE_HOME default ~/Work/Projects/OmniVoice)
and a locally cached model (env ASR_MODEL, default openai/whisper-large-v3-turbo).
"""
import json
import os
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAX_WER = 0.15

_ONES = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen " \
        "sixteen seventeen eighteen nineteen".split()
_TENS = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()
_ORD = {"one": "first", "two": "second", "three": "third", "five": "fifth", "eight": "eighth",
        "nine": "ninth", "twelve": "twelfth"}


def number_words(n):
    if n < 20:
        return _ONES[n]
    if n < 100:
        return _TENS[n // 10] + ("" if n % 10 == 0 else " " + _ONES[n % 10])
    return str(n)


def ordinal_words(n):
    words = number_words(n).split()
    last = words[-1]
    words[-1] = _ORD.get(last, last[:-1] + "ieth" if last.endswith("y") else last + "th")
    return " ".join(words)


def normalize(text):
    text = text.lower().replace("-", " ").replace("’", "'")
    text = re.sub(r"\b(\d{1,2})(st|nd|rd|th)\b", lambda m: ordinal_words(int(m.group(1))), text)
    text = re.sub(r"\b(\d{1,2})\b", lambda m: number_words(int(m.group(1))), text)
    text = re.sub(r"(\d)\s*(°|º|ᵒ)", r"\1 degrees", text)
    return re.sub(r"[^a-z0-9' ]+", " ", text).split()


def wer(reference, hypothesis):
    ref, hyp = normalize(reference), normalize(hypothesis)
    prev = list(range(len(hyp) + 1))
    for i, r in enumerate(ref, 1):
        cur = [i] + [0] * len(hyp)
        for j, h in enumerate(hyp, 1):
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (r != h))
        prev = cur
    return prev[-1] / max(1, len(ref))


def external_python():
    explicit = os.environ.get("OMNIVOICE_PYTHON")
    if explicit:
        return explicit
    home = Path(os.environ.get("OMNIVOICE_HOME", Path.home() / "Work/Projects/OmniVoice"))
    return str(home / ".venv/bin/python")


def transcribe(paths):
    python = external_python()
    if not Path(python).is_file():
        raise FileNotFoundError(f"ASR interpreter not found: {python} (set OMNIVOICE_PYTHON)")
    env = dict(os.environ, HF_HUB_OFFLINE="1", TRANSFORMERS_VERBOSITY="error")
    out = subprocess.run([python, str(ROOT / "tools/asr_whisper.py"),
                          os.environ.get("ASR_MODEL", "openai/whisper-large-v3-turbo"), *map(str, paths)],
                         capture_output=True, text=True, env=env, timeout=1800)
    line = next((l for l in out.stdout.splitlines() if l.startswith("ASR_JSON ")), None)
    if out.returncode != 0 or line is None:
        raise RuntimeError(f"ASR failed ({out.returncode}): {out.stderr.strip()[-400:]}")
    return json.loads(line[len("ASR_JSON "):])


def check_project(project_dir, log=print):
    """Transcribe every narrated sentence; store results in the manifest; return failures."""
    from pipeline.audio_manifest import AudioManifest
    project_dir = Path(project_dir)
    manifest = AudioManifest(project_dir)
    records = [r for r in manifest.data["segments"].values() if r.get("role") == "sentence"]
    current = {s["cache_key"] for b in manifest.data.get("beats", {}).values() for s in b["sentences"]}
    records = [r for r in records if r["cache_key"] in current]
    results = transcribe([project_dir / r["file"] for r in records])
    failures = []
    for rec, res in zip(records, results):
        score = round(wer(rec["text"], res["text"]), 4)
        ok = score <= MAX_WER and (res.get("language") or "").lower() in ("english", "en")
        rec["asr"] = {"text": res["text"], "language": res.get("language"), "wer": score, "pass": ok,
                      "model": os.environ.get("ASR_MODEL", "openai/whisper-large-v3-turbo")}
        log(f"{'PASS' if ok else 'FAIL'} {rec['beat_id']}.s{rec['sentence_index']} WER {score:.3f} "
            f"lang={res.get('language')}")
        if not ok:
            failures.append(f"{rec['beat_id']}.s{rec['sentence_index']}: WER {score:.2f} / {res.get('language')} "
                            f"heard {res['text']!r}")
    manifest.save()
    return failures
