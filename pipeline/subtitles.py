"""Phrase-level subtitles from measured audio (stdlib only; Whisper runs out of process).

Text always comes from the script (official spellings such as "Babergh" kept);
timing comes from the audio:
  - sentence start/end: the measured TTS segment spans (script/timing.json);
  - cue boundaries inside a sentence: Whisper word timestamps on that sentence's
    own audio (`align`), matched to the script words, then moved to the quietest
    10 ms frame near the word boundary in the real waveform.
A boundary is only placed between two script words that were both matched to
recognised words; nothing is interpolated from character counts. A sentence with
no usable alignment becomes one sentence-level cue (and the QA report says so).
"""
import array
import json
import math
import re
import wave
from pathlib import Path

from pipeline import asr_check

LINE_MAX = 42          # hard limit per line
LINE_TARGET = (32, 42)  # preferred line length when a cue needs two lines
MAX_LINES = 2
MIN_CUE = 1.0          # seconds (QA warns below, fails below FAIL_MIN_CUE)
FAIL_MIN_CUE = 0.7
MAX_CUE = 7.0
CPS_WARN, CPS_FAIL = 17.0, 21.0
LEAD_OUT = 0.25        # seconds a sentence-final cue may linger into the following pause
MIN_GAP = 2 / 24       # two frames between consecutive cues
GOOD_BREAK_AFTER = (",", ";", ":", "—", ".", "?", "!")
GOOD_BREAK_BEFORE = {"and", "but", "as", "or", "that", "which", "depending", "from", "between", "in", "with",
                     "because", "while", "where", "when", "than", "at"}
ALIGN_MODEL = "openai/whisper-large-v3-turbo"


# ---------------------------------------------------------------- alignment (Whisper words)
def align_project(project_dir, log=print):
    """Add Whisper word timestamps to every current sentence segment that lacks them."""
    from pipeline.audio_manifest import AudioManifest
    manifest = AudioManifest(project_dir)
    current = {s["cache_key"] for b in manifest.data.get("beats", {}).values() for s in b["sentences"]}
    todo = [r for k, r in manifest.data["segments"].items() if k in current
            and (r.get("alignment") or {}).get("segment_sha256") != r["sha256"]]
    if todo:
        results = asr_check.transcribe([Path(project_dir) / r["file"] for r in todo], words=True)
        for rec, res in zip(todo, results):
            rec["alignment"] = {"model": ALIGN_MODEL, "method": "whisper word timestamps (cross-attention DTW)",
                                "segment_sha256": rec["sha256"], "heard": res["text"], "words": res["words"]}
            log(f"ALIGNED {rec['beat_id']}.s{rec['sentence_index']}: {len(res['words'])} words")
        manifest.save()
    return len(todo)


def _tokens(text, aliases=None):
    toks = asr_check.normalize(text)
    return [aliases.get(t, t) for t in toks] if aliases else toks


def match_words(script_words, asr_words, aliases=None):
    """Per script word: (start, end) from the recognised words it matched, else None.
    Token-level edit-distance alignment after the WER normalisation (numbers, hyphens)."""
    a = [(i, t) for i, w in enumerate(script_words) for t in _tokens(w, aliases)]
    b = [(j, t) for j, w in enumerate(asr_words) for t in _tokens(w["text"], aliases)]
    n, m = len(a), len(b)
    cost = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        cost[i][0] = i
    for j in range(m + 1):
        cost[0][j] = j
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            cost[i][j] = min(cost[i - 1][j] + 1, cost[i][j - 1] + 1,
                             cost[i - 1][j - 1] + (0 if a[i - 1][1] == b[j - 1][1] else 1))
    pairs, i, j = [], n, m
    while i and j:
        if cost[i][j] == cost[i - 1][j - 1] + (0 if a[i - 1][1] == b[j - 1][1] else 1):
            if a[i - 1][1] == b[j - 1][1]:
                pairs.append((a[i - 1][0], b[j - 1][0]))
            i, j = i - 1, j - 1
        elif cost[i][j] == cost[i - 1][j] + 1:
            i -= 1
        else:
            j -= 1
    times = [None] * len(script_words)
    for si, aj in pairs:
        w = asr_words[aj]
        if w.get("start") is None or w.get("end") is None:
            continue
        s, e = times[si] or (w["start"], w["end"])
        times[si] = (min(s, w["start"]), max(e, w["end"]))
    return times


# ---------------------------------------------------------------- waveform check
def rms_frames(wav_path, hop=0.01):
    """RMS (dBFS) per `hop` seconds of a 16-bit PCM WAV."""
    with wave.open(str(wav_path), "rb") as w:
        rate, width, channels = w.getframerate(), w.getsampwidth(), w.getnchannels()
        data = array.array("h", w.readframes(w.getnframes()))
    if width != 2:
        raise ValueError(f"{wav_path}: expected 16-bit PCM")
    if channels > 1:
        data = data[::channels]
    step = max(1, int(rate * hop))
    out = []
    for k in range(0, len(data), step):
        chunk = data[k:k + step]
        power = sum(x * x for x in chunk) / max(1, len(chunk))
        out.append(20 * math.log10(math.sqrt(power) / 32768) if power > 0 else -120.0)
    return out, hop


def quietest(rms, hop, lo, hi):
    """(time, dB) of the quietest frame in [lo, hi] seconds."""
    a, b = max(0, int(lo / hop)), min(len(rms) - 1, int(math.ceil(hi / hop)))
    if b < a:
        k = min(len(rms) - 1, max(0, int(lo / hop)))
        return k * hop, rms[k]
    k = min(range(a, b + 1), key=lambda i: rms[i])
    return (k + 0.5) * hop, rms[k]


# ---------------------------------------------------------------- cue layout
def wrap(text, width=LINE_MAX):
    """One line if it fits, else the two-line split (<= width each) that prefers a
    punctuation/conjunction break and balanced lengths; None if impossible."""
    text = " ".join(text.split())
    if len(text) <= width:
        return [text]
    words = text.split(" ")
    best = None
    for k in range(1, len(words)):
        l1, l2 = " ".join(words[:k]), " ".join(words[k:])
        if len(l1) > width or len(l2) > width:
            continue
        # Break quality outweighs balance: never split e.g. "historic | roofs" when a comma break fits.
        score = abs(len(l1) - len(l2)) + (0 if l1.endswith(GOOD_BREAK_AFTER) else
                                           6 if words[k].lower() in GOOD_BREAK_BEFORE else 18)
        if best is None or score < best[0]:
            best = (score, [l1, l2])
    return best[1] if best else None


def _break_penalty(words, k):
    """Cost of a cue break after words[k]."""
    if words[k].endswith(GOOD_BREAK_AFTER):
        return 0.0
    if words[k + 1].lower().strip(",.;:") in GOOD_BREAK_BEFORE:
        return 0.6
    return 2.5


def segment(words, times, start, end):
    """Split one sentence into cues: list of (first, last) word indices. Breaks only
    between two aligned words; minimises cue count, reading-speed and break costs."""
    n = len(words)
    can_break = [k < n - 1 and times[k] is not None and times[k + 1] is not None for k in range(n)]

    def cue_cost(a, b):
        text = " ".join(words[a:b + 1])
        lines = wrap(text)
        if lines is None or len(lines) > MAX_LINES:
            return None
        t0 = start if a == 0 else (times[a - 1][1] + times[a][0]) / 2
        t1 = end if b == n - 1 else (times[b][1] + times[b + 1][0]) / 2
        d = max(1e-3, t1 - t0)
        cost = 1.0 + max(0.0, len(text) / d - CPS_WARN) * 0.6 + (6.0 if d < MIN_CUE else 0.0)
        cost += max(0.0, d - 6.0) * 2.0
        if len(lines) == 2:
            cost += 0.15 * sum(max(0, LINE_TARGET[0] - len(l)) for l in lines) / 4
        return cost

    best = [None] * (n + 1)   # best[i] = (cost, cuts) covering words[:i]
    best[0] = (0.0, [])
    for i in range(1, n + 1):
        if i < n and not can_break[i - 1]:  # a cue may only end where a break is allowed
            continue
        for a in range(0, i):
            if best[a] is None or (a > 0 and not can_break[a - 1]):
                continue
            c = cue_cost(a, i - 1)
            if c is None:
                continue
            total = best[a][0] + c + (_break_penalty(words, a - 1) if a > 0 else 0.0)
            if best[i] is None or total < best[i][0]:
                best[i] = (total, best[a][1] + [(a, i - 1)])
    return best[n][1] if best[n] else None


def build_cues(project_dir, timing, manifest, aliases=None, shot_ids=None, origin_seconds=0.0, total=None):
    """Cues [{start, end, lines, text, sentence, source, boundary}] for the whole timeline."""
    p = Path(project_dir)
    segments = manifest.get("segments", {})
    beat_keys = {b: {s["index"]: s["cache_key"] for s in v["sentences"]} for b, v in manifest.get("beats", {}).items()}
    cues = []
    for beat in timing["beats"]:
        if shot_ids is not None and beat["shot"] not in shot_ids:
            continue
        for s in beat["sentences"]:
            text = " ".join(s["text"].split())
            words = text.split(" ")
            t_start, t_end = s["start"] - origin_seconds, s["end"] - origin_seconds
            rec = segments.get(beat_keys.get(beat["id"], {}).get(s["index"]), {})
            align = rec.get("alignment")
            label = f"{beat['id']}.s{s['index']}"
            if not align or align.get("segment_sha256") != rec.get("sha256"):
                cues.append({"start": t_start, "end": t_end, "lines": wrap(text) or [text], "text": text,
                             "sentence": label, "source": "sentence span (no alignment)", "boundary": None})
                continue
            times = match_words(words, align["words"], aliases)
            spans = segment(words, times, 0.0, t_end - t_start)
            if not spans:
                cues.append({"start": t_start, "end": t_end, "lines": wrap(text) or [text], "text": text,
                             "sentence": label, "source": "sentence span (no valid split)", "boundary": None})
                continue
            rms, hop = rms_frames(p / rec["file"])
            edges = [(0.0, None)]
            for (a, b), _ in zip(spans, spans[1:]):
                w_end, w_next = times[b][1], times[b + 1][0]
                mid = (w_end + w_next) / 2
                at, db = quietest(rms, hop, max(times[b][0], mid - 0.15), min(times[b + 1][1], mid + 0.15))
                edges.append((at, {"after_word": words[b], "before_word": words[b + 1],
                                   "whisper_boundary": round(mid, 3), "placed_at": round(at, 3),
                                   "rms_db_at_boundary": round(db, 1)}))
            edges.append((t_end - t_start, None))
            for k, (a, b) in enumerate(spans):
                chunk = " ".join(words[a:b + 1])
                cues.append({"start": t_start + edges[k][0], "end": t_start + edges[k + 1][0],
                             "lines": wrap(chunk), "text": chunk, "sentence": label,
                             "source": "whisper word alignment + waveform" if len(spans) > 1 else "sentence span",
                             "boundary": edges[k + 1][1]})
    # Lead-out: a sentence's last cue may stay up to LEAD_OUT longer, inside the pause that
    # follows (never closer than MIN_GAP to the next cue): lowers reading speed, keeps sync.
    for k, c in enumerate(cues):
        last_of_sentence = k + 1 == len(cues) or cues[k + 1]["sentence"] != c["sentence"]
        if last_of_sentence:
            limit = cues[k + 1]["start"] - MIN_GAP if k + 1 < len(cues) else \
                min(c["end"] + LEAD_OUT, total if total is not None else c["end"] + LEAD_OUT)
            c["speech_end"] = c["end"]
            c["end"] = max(c["end"], min(c["end"] + LEAD_OUT, limit))
    return cues


# ---------------------------------------------------------------- output + QA
def srt_time(t):
    ms = int(round(max(0.0, t) * 1000))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def write_srt(cues, out):
    lines = []
    for i, c in enumerate(cues, 1):
        lines += [str(i), f"{srt_time(c['start'])} --> {srt_time(c['end'])}", *c["lines"], ""]
    Path(out).write_text("\n".join(lines), encoding="utf-8")


def parse_srt(text):
    """[(start, end, [lines])] from SRT text (used by the QA to check the written file)."""
    out = []
    for block in re.split(r"\n\s*\n", text.strip()):
        rows = block.splitlines()
        if len(rows) < 3:
            continue
        m = re.match(r"(\d+):(\d+):(\d+),(\d+) --> (\d+):(\d+):(\d+),(\d+)", rows[1])
        if not m:
            raise ValueError(f"bad SRT timing line {rows[1]!r}")
        g = [int(x) for x in m.groups()]
        out.append((g[0] * 3600 + g[1] * 60 + g[2] + g[3] / 1000, g[4] * 3600 + g[5] * 60 + g[6] + g[7] / 1000, rows[2:]))
    return out


def qa(cues, duration, sentences):
    """(problems, warnings, stats). `sentences`: {label: script text} — cue text must rebuild it exactly."""
    problems, warnings = [], []
    last = 0.0
    for i, c in enumerate(cues, 1):
        d = c["end"] - c["start"]
        tag = f"cue {i} ({c['sentence']})"
        if not (0 <= c["start"] < c["end"] <= duration + 1e-6):
            problems.append(f"{tag}: {c['start']:.3f}-{c['end']:.3f}s outside 0-{duration:.3f}s")
        if c["start"] < last - 1e-6:
            problems.append(f"{tag}: overlaps the previous cue")
        last = c["end"]
        if not c["lines"] or len(c["lines"]) > MAX_LINES:
            problems.append(f"{tag}: {len(c['lines'] or [])} lines (max {MAX_LINES})")
        for line in c["lines"] or []:
            if len(line) > LINE_MAX:
                problems.append(f"{tag}: line of {len(line)} chars > {LINE_MAX}")
        cps = len(c["text"]) / d if d > 0 else 99
        if d < FAIL_MIN_CUE:
            problems.append(f"{tag}: {d:.2f}s on screen (< {FAIL_MIN_CUE}s)")
        elif d < MIN_CUE:
            warnings.append(f"{tag}: {d:.2f}s on screen (< {MIN_CUE}s)")
        if d > MAX_CUE:
            warnings.append(f"{tag}: {d:.2f}s on screen (> {MAX_CUE}s)")
        if cps > CPS_FAIL:
            problems.append(f"{tag}: {cps:.1f} characters/s (> {CPS_FAIL})")
        elif cps > CPS_WARN:
            warnings.append(f"{tag}: {cps:.1f} characters/s (> {CPS_WARN})")
    rebuilt = {}
    for c in cues:
        rebuilt.setdefault(c["sentence"], []).append(c["text"])
    for label, text in sentences.items():
        got = " ".join(rebuilt.get(label, []))
        if got != " ".join(text.split()):
            problems.append(f"{label}: cue text {got!r} does not rebuild the script sentence {text!r}")
    lengths = [len(l) for c in cues for l in c["lines"] or []]
    stats = {"cues": len(cues), "sentences": len(sentences), "max_line": max(lengths, default=0),
             "lines_over_42": sum(1 for n in lengths if n > LINE_MAX),
             "two_line_cues": sum(1 for c in cues if len(c["lines"] or []) == 2),
             "aligned_boundaries": sum(1 for c in cues if c["boundary"]),
             "sentence_fallbacks": sum(1 for c in cues if "no alignment" in c["source"] or "no valid" in c["source"]),
             "max_cps": round(max((len(c["text"]) / (c["end"] - c["start"]) for c in cues), default=0), 1)}
    return problems, warnings, stats
