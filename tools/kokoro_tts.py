"""Kokoro-82M inference worker (M6). Runs ONLY under the isolated Kokoro interpreter
(KOKORO_PYTHON, default ~/Work/Projects/Kokoro/.venv/bin/python), offline, on CPU:

  KOKORO_PYTHON tools/kokoro_tts.py <request.json>     (one batch)
  KOKORO_PYTHON tools/kokoro_tts.py --serve            (JSON lines on stdin/stdout, used by the adapter)

request: {"snapshot": <local HF snapshot dir>, "lang_code": "b", "threads": 4, "items": [
           {"id", "text", "voice", "speed", "seed", "out"}]}
Prints one line "KOKORO_JSON <results>" with, per item: duration, sample_rate, phonemes,
tokens, chunks, elapsed_seconds. Audio: 24 kHz mono 16-bit PCM WAV (the M3 pipeline format).
The weights and voices are loaded with torch.load(weights_only=True) by the official package.
"""
import json
import sys
import time
import wave
from pathlib import Path

import numpy as np
import torch
from kokoro import KModel, KPipeline

SAMPLE_RATE = 24000


class Engine:
    def __init__(self, snapshot, lang_code="b", threads=4):
        self.snap = Path(snapshot)
        torch.set_num_threads(int(threads))
        t0 = time.time()
        model = KModel(repo_id="hexgrad/Kokoro-82M", config=str(self.snap / "config.json"),
                       model=str(self.snap / "kokoro-v1_0.pth")).to("cpu").eval()
        self.pipe = KPipeline(lang_code=lang_code, repo_id="hexgrad/Kokoro-82M", model=model)
        self.load_seconds = round(time.time() - t0, 2)
        self.voices = {}

    def run(self, items):
        return [self.one(item) for item in items]

    def one(self, item):
        return _synthesize(self.pipe, self.voices, self.snap, item)


def main():
    if sys.argv[1:] == ["--serve"]:   # JSON lines over stdin/stdout (no network server)
        engine = None
        for line in sys.stdin:
            req = json.loads(line)
            try:
                if engine is None:
                    engine = Engine(req["snapshot"], req.get("lang_code", "b"), req.get("threads", 4))
                out = {"ok": True, "load_seconds": engine.load_seconds, "torch": torch.__version__,
                       "results": engine.run(req["items"])}
            except Exception as e:  # noqa: BLE001 - reported to the adapter, which raises
                out = {"ok": False, "error": f"{type(e).__name__}: {e}"}
            sys.stdout.write("KOKORO_JSON " + json.dumps(out) + "\n")
            sys.stdout.flush()
        return
    req = json.loads(Path(sys.argv[1]).read_text())
    engine = Engine(req["snapshot"], req.get("lang_code", "b"), req.get("threads", 4))
    print("KOKORO_JSON " + json.dumps({"load_seconds": engine.load_seconds, "torch": torch.__version__,
                                       "results": engine.run(req["items"])}))


def _synthesize(pipe, voices, snap, item):
    """One utterance -> WAV; the seed is set per item (the decoder draws noise)."""
    voice = voices.get(item["voice"])
    if voice is None:
        voice = voices[item["voice"]] = pipe.load_voice(str(Path(snap) / "voices" / f"{item['voice']}.pt"))
    t1 = time.time()
    torch.manual_seed(int(item.get("seed", 0)))   # the decoder draws noise: one seed per item = reproducible
    audio, phonemes, tokens = [], [], 0
    with torch.no_grad():
        for res in pipe(item["text"], voice=voice, speed=float(item.get("speed", 1.0)), split_pattern=None):
            if res.audio is None:
                continue
            audio.append(res.audio.detach().cpu().numpy())
            phonemes.append(res.phonemes)
            tokens += len(res.phonemes)
    if not audio:
        raise RuntimeError(f"{item['id']}: no audio produced")
    pcm = np.concatenate(audio)
    peak = float(np.max(np.abs(pcm))) if pcm.size else 0.0
    data = (np.clip(pcm, -1.0, 1.0) * 32767.0).round().astype("<i2").tobytes()
    out = Path(item["out"])
    out.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(out), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SAMPLE_RATE)
        w.writeframes(data)
    return {"id": item["id"], "out": str(out), "duration": len(pcm) / SAMPLE_RATE,
            "sample_rate": SAMPLE_RATE, "phonemes": " ".join(phonemes), "phoneme_chars": tokens,
            "chunks": len(audio), "peak": round(peak, 4), "elapsed_seconds": round(time.time() - t1, 3)}


if __name__ == "__main__":
    main()
