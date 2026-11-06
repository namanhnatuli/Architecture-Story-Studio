"""Sound effects synthesised in the project (stdlib only): no recordings, no libraries, no licence to clear.

A SEQUENCE shot lists `sound_cues` (planner: the moment each arriving stone part lands). This module turns cues into
a mono track at the narration's sample rate, mixed under the narration before loudness normalisation.

Design rules (config/sound_design.json):
- one short sound per visible event (a stone set in place), never a bed of music or ambience;
- quiet: each sound's peak sits a fixed number of dB under the narration's peak, and nothing plays while a word is
  spoken unless the mix is checked by ASR (tools/excerpt.py compares Whisper on the clean and the mixed narration);
- deterministic: the same cue, kind and seed give the same samples, so a re-render is bit-identical.

An agent cannot listen: whether these sounds help or tire the viewer is the owner's call.
"""
import json
import math
import random
import struct
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load_design(root=ROOT):
    return json.loads((Path(root) / "config/sound_design.json").read_text())


def _damped(freq, decay, seconds, sr, start_freq=None, phase=0.0):
    """A sine whose pitch glides from start_freq to freq, with an exponential decay (seconds to 1/e)."""
    out, ph = [], phase
    n = int(seconds * sr)
    for i in range(n):
        t = i / sr
        f = freq if start_freq is None else freq + (start_freq - freq) * math.exp(-t / (decay * 0.6))
        ph += 2 * math.pi * f / sr
        out.append(math.sin(ph) * math.exp(-t / decay))
    return out


def _noise_burst(seconds, decay, sr, rng, lowpass_hz, highpass_hz):
    """White noise through a one-pole high-pass and low-pass (a band), exponentially decaying."""
    a_lp = math.exp(-2 * math.pi * lowpass_hz / sr)
    a_hp = math.exp(-2 * math.pi * highpass_hz / sr)
    lp = hp_in = hp_out = 0.0
    out = []
    for i in range(int(seconds * sr)):
        x = rng.uniform(-1.0, 1.0)
        lp = (1 - a_lp) * x + a_lp * lp
        hp_out = a_hp * (hp_out + lp - hp_in)
        hp_in = lp
        out.append(hp_out * math.exp(-i / sr / decay))
    return out


def synth(kind, sr, seed=0, design=None):
    """Samples (floats, peak 1.0) of one sound. kinds: STONE (a block set in place), STONE_HEAVY (a large one)."""
    d = (design or load_design())["kinds"][kind]
    rng = random.Random(f"{kind}:{seed}")
    n = int(d["seconds"] * sr)
    mix = [0.0] * n
    layers = [(_damped(d["thump_hz"], d["thump_decay"], d["seconds"], sr, start_freq=d["thump_start_hz"]), d["thump_gain"]),
              (_noise_burst(d["seconds"], d["click_decay"], sr, rng, d["click_lowpass_hz"], d["click_highpass_hz"]),
               d["click_gain"])]
    for f, decay, g in d["body"]:   # resonances of the stone itself
        layers.append((_damped(f * (1 + rng.uniform(-0.03, 0.03)), decay, d["seconds"], sr, phase=rng.uniform(0, 6.28)), g))
    for samples, gain in layers:
        for i, v in enumerate(samples[:n]):
            mix[i] += v * gain
    attack = max(1, int(0.002 * sr))   # no click from a hard start
    for i in range(min(attack, n)):
        mix[i] *= i / attack
    release = max(1, int(0.015 * sr))  # nor from a hard end
    for i in range(min(release, n)):
        mix[n - 1 - i] *= i / release
    peak = max(abs(v) for v in mix) or 1.0
    return [v / peak for v in mix]


def read_wav(path):
    with wave.open(str(path), "rb") as w:
        if w.getsampwidth() != 2:
            raise ValueError(f"{path}: 16-bit PCM expected")
        ch, sr, data = w.getnchannels(), w.getframerate(), w.readframes(w.getnframes())
    samples = struct.unpack(f"<{len(data) // 2}h", data)
    return ch, sr, list(samples)


def write_wav(path, samples, sr, ch=1):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    clipped = [max(-32768, min(32767, int(round(v)))) for v in samples]
    with wave.open(str(path), "wb") as w:
        w.setnchannels(ch)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(struct.pack(f"<{len(clipped)}h", *clipped))


def cue_track(cues, n_samples, sr, peak, design=None):
    """Float samples (int16 scale) with every cue [{"at_seconds", "kind"}] placed at its time, each sound scaled to
    `peak` x its kind's relative gain. Cues are mixed additively; the result is checked against clipping by the caller."""
    design = design or load_design()
    out = [0.0] * n_samples
    cache = {}
    for k, cue in enumerate(sorted(cues, key=lambda c: c["at_seconds"])):
        key = (cue["kind"], k % design["variants"])
        if key not in cache:
            cache[key] = synth(cue["kind"], sr, key[1], design)
        start = int(round((cue["at_seconds"] - design["lead_seconds"]) * sr))
        g = peak * 10 ** (design["kinds"][cue["kind"]]["relative_db"] / 20)
        for i, v in enumerate(cache[key]):
            j = start + i
            if 0 <= j < n_samples:
                out[j] += v * g
    return out


def mix_under(narration, cues, sr, design=None):
    """(mixed int16 samples, report) for a mono narration track and its cues. Each sound peaks `under_narration_db`
    below the narration's peak."""
    design = design or load_design()
    n_peak = max((abs(v) for v in narration), default=0) or 1
    peak = n_peak * 10 ** (-design["under_narration_db"] / 20)
    fx = cue_track(cues, len(narration), sr, peak, design)
    mixed = [a + b for a, b in zip(narration, fx)]
    over = sum(1 for v in mixed if abs(v) > 32767)
    return mixed, {"cues": len(cues), "narration_peak": n_peak, "effect_peak": round(max((abs(v) for v in fx), default=0), 1),
                   "under_narration_db": design["under_narration_db"], "clipped_samples": over}
