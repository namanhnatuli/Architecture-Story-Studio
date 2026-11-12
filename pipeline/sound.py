"""Sound effects under the narration: synthesised in the project, or recorded files a project lists with their licence.

A SEQUENCE shot lists `sound_cues` (planner: the moment each arriving stone part lands). This module turns cues into
a mono track at the narration's sample rate, mixed under the narration before loudness normalisation.

Design rules (config/sound_design.json):
- one short sound per visible event (a stone set in place), never a bed of music;
- quiet: each sound's peak sits a fixed number of dB under the narration's peak, and nothing plays while a word is
  spoken unless the mix is checked by ASR (tools/excerpt.py compares Whisper on the clean and the mixed narration);
- deterministic: the same cue, kind and seed give the same samples, so a re-render is bit-identical.

Recorded sounds (owner request, 2026-11-12): a project may add `audio/sound_plan.json` (schema sound_plan/1):
- `sources`: each file with its sha256, page, artist, licence and the day the licence was checked; a missing or
  replaced file stops the mix;
- `kinds`: a stretch of a source (trim_start, seconds, fades), its level relative to the other sounds, and `align`
  ("onset": the stretch starts at the cue, as the synthesised sounds; "peak": its loudest moment falls on the cue);
- `replace`: storyboard cue kinds played by a recorded kind instead (STONE -> a recorded thud);
- `cues`: extra one-shots anchored to a storyboard step (shot, step index, its `do`, start or end, offset), so they
  follow the picture if its timing changes, without touching the shot (sounds never invalidate a render);
- `chapter_cues`: one kind on every cut into a chapter after the first;
- `beds`: a short ambience under one shot (from, to: seconds, "end" or a view's arrival), its RMS
  `bed_under_narration_db` under the narration's speech RMS, faded in and out. Only where the subject is the sound
  itself (water moving the platforms), never under the whole film.

An agent cannot listen: whether these sounds help or tire the viewer is the owner's call.
"""
import hashlib
import json
import math
import random
import shutil
import struct
import subprocess
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLAN_FILE = "audio/sound_plan.json"
PLAN_SCHEMA = "sound_plan/1"
SOURCE_FIELDS = ("file", "sha256", "page", "artist", "license", "license_url", "checked_on")


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


def load_plan(p):
    """A project's recorded sounds and extra cues (audio/sound_plan.json), or None."""
    path = Path(p) / PLAN_FILE
    return json.loads(path.read_text()) if path.is_file() else None


def check_plan(plan, root=ROOT):
    """Problems with a sound plan: unknown schema, a source without its licence record, missing or replaced (sha256),
    a kind without a source, a replacement or cue naming an unknown kind."""
    problems = []
    if plan.get("schema") != PLAN_SCHEMA:
        problems.append(f"sound plan schema {plan.get('schema')!r}, expected {PLAN_SCHEMA}")
    sources, kinds = plan.get("sources") or {}, plan.get("kinds") or {}
    synth_kinds = load_design()["kinds"]
    for sid, src in sources.items():
        missing = [k for k in SOURCE_FIELDS if not src.get(k)]
        if missing:
            problems.append(f"sound source {sid}: no {', '.join(missing)}")
            continue
        f = Path(root) / src["file"]
        if not f.is_file():
            problems.append(f"sound source {sid}: {src['file']} is missing")
        elif hashlib.sha256(f.read_bytes()).hexdigest() != src["sha256"]:
            problems.append(f"sound source {sid}: {src['file']} is not the recorded file (sha256)")
    for name, k in kinds.items():
        if name in synth_kinds:
            problems.append(f"recorded kind {name} has the name of a synthesised kind (use 'replace')")
        if k.get("source") not in sources:
            problems.append(f"recorded kind {name}: unknown source {k.get('source')!r}")
        if not k.get("seconds") or k["seconds"] <= 0:
            problems.append(f"recorded kind {name}: seconds must be > 0")
    for old, new in (plan.get("replace") or {}).items():
        if old not in synth_kinds or new not in kinds:
            problems.append(f"replace {old} -> {new}: {old} must be synthesised and {new} recorded")
    named = [c.get("kind") for c in plan.get("cues") or []] + [b.get("kind") for b in plan.get("beds") or []]
    if plan.get("chapter_cues"):
        named.append(plan["chapter_cues"].get("kind"))
    problems += [f"sound plan names unknown kind {k!r}" for k in named if k not in kinds]
    problems += [f"bed kind {b['kind']} is not a bed" for b in plan.get("beds") or [] if not kinds.get(b.get("kind"), {}).get("bed")]
    return problems


def decode(path, sr, start=0.0, seconds=None, highpass_hz=None):
    """Mono float samples (-1..1) of a stretch of an audio file at `sr`, through FFmpeg."""
    af = [f"atrim=start={start}" + (f":duration={seconds}" if seconds else ""), "asetpts=PTS-STARTPTS"]
    if highpass_hz:
        af.append(f"highpass=f={highpass_hz}")
    raw = subprocess.run([shutil.which("ffmpeg") or "ffmpeg", "-v", "error", "-i", str(path), "-af", ",".join(af),
                          "-ac", "1", "-ar", str(sr), "-f", "s16le", "-"], check=True, capture_output=True).stdout
    return [v / 32768 for v in struct.unpack(f"<{len(raw) // 2}h", raw)]


def _fade(x, sr, fade_in, fade_out):
    a, b = max(1, int(fade_in * sr)), max(1, int(fade_out * sr))
    for i in range(min(a, len(x))):
        x[i] *= i / a
    for i in range(min(b, len(x))):
        x[len(x) - 1 - i] *= i / b
    return x


def recorded(kind, plan, sr, root=ROOT):
    """Samples of a recorded kind: its stretch of the source, faded at both ends. A one-shot is scaled to peak 1.0
    (as the synthesised sounds); a bed keeps its level, set later against the narration."""
    k = plan["kinds"][kind]
    src = plan["sources"][k["source"]]
    x = decode(Path(root) / src["file"], sr, k.get("trim_start", 0.0), k["seconds"], k.get("highpass_hz"))
    if k.get("bed"):
        return x
    x = _fade(x, sr, k.get("fade_in", 0.005), k.get("fade_out", 0.03))
    peak = max((abs(v) for v in x), default=0.0) or 1.0
    return [v / peak for v in x]


def loudest_at(x, sr, window=0.02):
    """Sample index of the middle of the loudest `window` of x."""
    w = max(1, int(window * sr))
    best, at = -1.0, 0
    for i in range(0, max(1, len(x) - w + 1), w):
        e = sum(v * v for v in x[i:i + w])
        if e > best:
            best, at = e, i + w // 2
    return at


def resolve_plan(plan, story_shots, film_ids, ids, offsets, chapter_firsts):
    """(cues, beds, problems): the plan's extra one-shots, chapter cues and beds for the shots `ids` of an excerpt or
    of the film, at their times in it (`offsets`: each shot's start). A chapter cue sounds only on a real cut: the
    chapter's first shot and the film shot before it are both present."""
    by_id = {s["id"]: s for s in story_shots}
    pos = {s: i for i, s in enumerate(film_ids)}
    cues, beds, problems = [], [], []
    for c in plan.get("cues") or []:
        if c["shot"] not in ids:
            continue
        steps = (by_id[c["shot"]].get("animation") or {}).get("steps") or []
        if not 0 <= c["step"] < len(steps) or steps[c["step"]]["do"] != c["do"]:
            problems.append(f"sound cue {c['kind']} on {c['shot']} step {c['step']}: not a {c['do']} step")
            continue
        st = steps[c["step"]]
        t = st["start_seconds"] + (st.get("seconds") or 0.0) * (c.get("edge") == "end") + c.get("offset", 0.0)
        cues.append({"at_seconds": round(offsets[c["shot"]] + t, 4), "kind": c["kind"], "shot": c["shot"],
                     "step": c["step"], "plan": True})
    ch = plan.get("chapter_cues")
    for first in chapter_firsts if ch else []:
        before = film_ids[pos[first] - 1] if pos.get(first, 0) > 0 else None
        if first in ids and before in ids and ids.index(before) == ids.index(first) - 1:
            cues.append({"at_seconds": round(offsets[first] + ch.get("offset", 0.0), 4), "kind": ch["kind"],
                         "shot": first, "chapter": True, "plan": True})
    for b in plan.get("beds") or []:
        if b["shot"] not in ids:
            continue
        shot = by_id[b["shot"]]

        def when(v):
            if v == "end":
                return shot["duration_seconds"]
            if isinstance(v, dict):
                view = shot["animation"]["views"][v["view"]]
                return (view.get("start_seconds") or 0.0) + (view.get("move_seconds") or 0.0)
            return float(v)
        a, e = when(b.get("from", 0.0)), when(b.get("to", "end"))
        if e - a < b.get("fade_in", 1.0) + b.get("fade_out", 1.0):
            problems.append(f"sound bed on {b['shot']}: {e - a:.2f} s, shorter than its fades")
            continue
        beds.append({"from_seconds": round(offsets[b["shot"]] + a, 4), "to_seconds": round(offsets[b["shot"]] + e, 4),
                     "kind": b["kind"], "fade_in": b.get("fade_in", 1.0), "fade_out": b.get("fade_out", 1.0),
                     "shot": b["shot"]})
    return sorted(cues, key=lambda c: c["at_seconds"]), beds, problems


def film_plan_cues(p, plan, story_shots, timing, ids, offsets):
    """resolve_plan for the shots `ids` of project `p` (at `offsets`), the chapter starts taken from
    script/chapters.json: (cues, beds, problems)."""
    shot_of = {b["id"]: b["shot"] for b in timing["beats"]}
    chapters = json.loads((Path(p) / "script/chapters.json").read_text())["chapters"]
    firsts = [shot_of[c["beat_ids"][0]] for c in chapters[1:]]
    return resolve_plan(plan, story_shots, [s["id"] for s in story_shots], ids, offsets, firsts)


def final_effects(p, plan, raw, timing, story_shots, root=ROOT):
    """The whole film's sound effects under its narration track `raw` (mono WAV): the storyboard's cues and the
    plan's, as tools/excerpt.py mixes them for the full review cut. Writes <raw>_sfx.wav; returns (path, report)."""
    ch, sr, narration = read_wav(raw)
    if ch != 1:
        raise ValueError("mono narration expected")
    fps = timing["fps"]
    offsets = {s["id"]: s["start_frame"] / fps for s in timing["shots"]}
    ids = [s["id"] for s in story_shots]
    cues = sorted((dict(c, at_seconds=round(offsets[s["id"]] + c["at_seconds"], 4), shot=s["id"])
                   for s in story_shots for c in s.get("sound_cues") or []), key=lambda c: c["at_seconds"])
    extra, beds, problems = film_plan_cues(p, plan, story_shots, timing, ids, offsets)
    cues = sorted(cues + extra, key=lambda c: c["at_seconds"])
    mixed, report = mix_under(narration, cues, sr, plan=plan, beds=beds, root=root)
    if report["clipped_samples"]:
        problems.append(f"{report['clipped_samples']} clipped samples in the mix")
    out = Path(raw).with_name(Path(raw).stem + "_sfx.wav")
    write_wav(out, mixed, sr)
    return out, dict(report, sound_cues=cues, sound_beds=beds, problems=problems, plan=PLAN_FILE)


def speech_rms(narration, sr, window=0.05, floor_db=30.0):
    """RMS (int16 scale) of the narration where it speaks: 50 ms windows within floor_db of the loudest one."""
    w = max(1, int(window * sr))
    ms = [sum(v * v for v in narration[i:i + w]) / w for i in range(0, len(narration) - w + 1, w)]
    top = max(ms, default=0.0)
    if not top:
        return 0.0
    keep = [m for m in ms if m >= top * 10 ** (-floor_db / 10)]
    return math.sqrt(sum(keep) / len(keep))


def cue_track(cues, n_samples, sr, peak, design=None, plan=None, root=ROOT):
    """Float samples (int16 scale) with every cue [{"at_seconds", "kind"}] placed at its time, each sound scaled to
    `peak` x its kind's relative gain. A recorded kind (plan) plays its file; `replace` maps a synthesised kind to a
    recorded one. Cues are mixed additively; the result is checked against clipping by the caller."""
    design = design or load_design()
    rec = (plan or {}).get("kinds") or {}
    replace = (plan or {}).get("replace") or {}
    out = [0.0] * n_samples
    cache = {}
    for k, cue in enumerate(sorted(cues, key=lambda c: c["at_seconds"])):
        kind = replace.get(cue["kind"], cue["kind"])
        if kind in rec:
            key = (kind, 0)
            if key not in cache:
                cache[key] = recorded(kind, plan, sr, root)
            if rec[kind].get("align") == "peak":
                start = int(round(cue["at_seconds"] * sr)) - loudest_at(cache[key], sr)
            else:
                start = int(round((cue["at_seconds"] - design["lead_seconds"]) * sr))
            g = peak * 10 ** (rec[kind].get("relative_db", 0.0) / 20)
        else:
            key = (kind, k % design["variants"])
            if key not in cache:
                cache[key] = synth(kind, sr, key[1], design)
            start = int(round((cue["at_seconds"] - design["lead_seconds"]) * sr))
            g = peak * 10 ** (design["kinds"][kind]["relative_db"] / 20)
        for i, v in enumerate(cache[key]):
            j = start + i
            if 0 <= j < n_samples:
                out[j] += v * g
    return out


def bed_track(beds, n_samples, sr, level_rms, plan, root=ROOT):
    """Float samples (int16 scale) with each bed's stretch at RMS `level_rms`, faded in and out."""
    out = [0.0] * n_samples
    for b in beds:
        x = recorded(b["kind"], plan, sr, root)
        need = int(round((b["to_seconds"] - b["from_seconds"]) * sr))
        if len(x) < need:
            raise ValueError(f"bed {b['kind']} on {b['shot']}: its source stretch is {len(x) / sr:.2f} s, "
                             f"{need / sr:.2f} s needed")
        x = x[:need]
        r = math.sqrt(sum(v * v for v in x) / max(1, len(x))) or 1.0
        x = _fade([v * level_rms / r for v in x], sr, b["fade_in"], b["fade_out"])
        start = int(round(b["from_seconds"] * sr))
        for i, v in enumerate(x):
            j = start + i
            if 0 <= j < n_samples:
                out[j] += v
    return out


def mix_under(narration, cues, sr, design=None, plan=None, beds=(), root=ROOT):
    """(mixed int16 samples, report) for a mono narration track and its cues. Each sound peaks `under_narration_db`
    below the narration's peak; a bed's RMS sits the plan's `bed_under_narration_db` under the speech RMS."""
    design = design or load_design()
    n_peak = max((abs(v) for v in narration), default=0) or 1
    peak = n_peak * 10 ** (-design["under_narration_db"] / 20)
    fx = cue_track(cues, len(narration), sr, peak, design, plan, root)
    report = {"cues": len(cues), "narration_peak": n_peak, "effect_peak": round(max((abs(v) for v in fx), default=0), 1),
              "under_narration_db": design["under_narration_db"]}
    if beds:
        speech = speech_rms(narration, sr)
        level = speech * 10 ** (-plan["bed_under_narration_db"] / 20)
        bed = bed_track(beds, len(narration), sr, level, plan, root)
        fx = [a + b for a, b in zip(fx, bed)]
        report.update(beds=len(beds), bed_under_narration_db=plan["bed_under_narration_db"],
                      speech_rms=round(speech, 1), bed_rms=round(level, 1))
    mixed = [a + b for a, b in zip(narration, fx)]
    report["clipped_samples"] = sum(1 for v in mixed if abs(v) > 32767)
    return mixed, report
