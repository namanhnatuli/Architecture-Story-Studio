"""Narration script -> validated, cached, measured beat audio (stdlib only).

script/narration.json defines beats (ordered sentences + claim IDs) and the voice.
Each sentence is synthesised separately (so sentence timings are exact), validated,
cached by content, then joined per beat with fixed pauses at the sample level.
Durations always come from the decoded audio, never from word counts.
"""
import json
import wave
from pathlib import Path

from integrations import audio_probe
from integrations.tts import omnivoice as ov
from pipeline.audio_manifest import AudioManifest, cache_key, sha256_file

BEAT_KINDS = ("framing", "fact", "interpretation")
MAX_TAKES = 3
LICENSE_STATUSES = ("APPROVED", "LICENSE_REVIEW_REQUIRED", "REJECTED")
CLAIM_STATUSES = ("PROVISIONAL", "SOURCE_VERIFIED", "EDITORIALLY_APPROVED", "REJECTED",
                  "provisional", "verified", "contested")  # lower-case: v0.1 ledger values


def load(project_dir):
    path = Path(project_dir) / "script" / "narration.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else None


def validate(narration, sources):
    """Errors in narration.json against the claim ledger (empty list when valid)."""
    errors = []
    claims = {c.get("id"): c for c in (sources or {}).get("claims", [])}
    voice = narration.get("voice") or {}
    lic = voice.get("license") or {}
    if lic.get("status") not in LICENSE_STATUSES:
        errors.append(f"narration.voice.license.status must be one of {LICENSE_STATUSES} "
                      "(record the voice licensing review before generating narration)")
    if not lic.get("components"):
        errors.append("narration.voice.license.components is empty (list model/code/data licences)")
    if voice.get("mode") == "clone" and not (voice.get("reference") or {}).get("text"):
        errors.append("narration.voice.reference.text is required for clone mode")
    pacing = narration.get("pacing") or {}
    for key in ("sentence_pause_seconds", "beat_lead_in_seconds", "beat_tail_seconds"):
        value = pacing.get(key)
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not 0 <= value <= 3:
            errors.append(f"narration.pacing.{key} must be a number between 0 and 3")
    seen = set()
    for beat in narration.get("beats", []):
        bid = beat.get("id")
        if not bid or bid in seen:
            errors.append(f"beat id missing or duplicated: {bid!r}")
        seen.add(bid)
        if beat.get("kind") not in BEAT_KINDS:
            errors.append(f"{bid}: kind must be one of {BEAT_KINDS}")
        sentences = beat.get("sentences") or []
        if not sentences or any(not isinstance(s, str) or not s.strip() for s in sentences):
            errors.append(f"{bid}: needs at least one non-empty sentence")
        ids = beat.get("claim_ids") or []
        if beat.get("kind") in ("fact", "interpretation") and not ids:
            errors.append(f"{bid}: a {beat.get('kind')} beat must cite claim_ids")
        for cid in ids:
            claim = claims.get(cid)
            if claim is None:
                errors.append(f"{bid}: claim {cid} is not in research/sources.json")
            elif claim.get("review_status") == "REJECTED":
                errors.append(f"{bid}: claim {cid} is REJECTED and must not be narrated")
            elif claim.get("review_status") not in CLAIM_STATUSES:
                errors.append(f"{bid}: claim {cid} has unknown review_status {claim.get('review_status')!r}")
            elif not claim.get("source_ids"):
                errors.append(f"{bid}: claim {cid} has no source_ids")
    if not narration.get("beats"):
        errors.append("narration has no beats")
    return errors


def voice_spec(narration, project_dir):
    v = narration["voice"]
    if v.get("mode") == "clone":
        ref = v["reference"]
        return ov.VoiceSpec(mode="clone", language=v.get("language", "English"),
                            reference_audio=str(Path(project_dir) / ref["audio"]), reference_text=ref["text"])
    return ov.VoiceSpec(mode="design", language=v.get("language", "English"), design=v.get("design") or {})


def generation_params(narration):
    return ov.GenerationParams(**(narration["voice"].get("params") or {}))


def _segment(client, manifest, project_dir, text, voice, params, label, regenerate, log, extra):
    from dataclasses import asdict
    key = cache_key("omnivoice", ov.ADAPTER_VERSION, client.model_revision, text, voice.identity(), asdict(params))
    cached = None if regenerate else manifest.lookup(key)
    if cached:
        log(f"CACHED {label}: {cached['duration']:.2f}s")
        return cached
    out = Path(project_dir) / "audio" / "segments" / f"{key[:20]}.wav"
    for attempt in range(1, MAX_TAKES + 1):  # generation is stochastic: a rushed/garbled take gets a retake
        try:
            result = client.synthesize(text, voice, out, params)
            break
        except audio_probe.AudioValidationError as e:
            log(f"RETAKE {label} (take {attempt}/{MAX_TAKES} rejected: {e})")
            if attempt == MAX_TAKES:
                raise
    record = manifest.store(key, dict(extra, text=text, file=manifest.rel(out), duration=result.duration,
                                      sample_rate=result.sample_rate, channels=result.channels, codec=result.codec,
                                      mean_db=result.mean_db, peak_db=result.peak_db,
                                      words_per_second=result.words_per_second, params=asdict(params),
                                      endpoint=result.endpoint, elapsed_seconds=result.elapsed_seconds,
                                      takes=attempt, **result.metadata))
    manifest.save()  # persist every successful segment immediately (a later failure must not lose it)
    log(f"GENERATED {label}: {result.duration:.2f}s in {result.elapsed_seconds:.1f}s")
    return record


def ensure_reference(client, narration, project_dir, manifest, regenerate=False, log=print):
    """Create the synthetic narrator reference clip (voice design), cached like any segment."""
    v = narration["voice"]
    if v.get("mode") != "clone":
        return None
    ref = v["reference"]
    made = ref.get("made_with") or {}
    design = ov.VoiceSpec(mode="design", language=v.get("language", "English"), design=made.get("design") or {})
    record = _segment(client, manifest, project_dir, ref["text"], design, ov.GenerationParams(),
                      "voice reference", regenerate, log,
                      {"role": "voice_reference", "voice_id": v.get("id")})
    target = Path(project_dir) / ref["audio"]
    target.parent.mkdir(parents=True, exist_ok=True)
    src = Path(project_dir) / record["file"]
    if not target.is_file() or sha256_file(target) != sha256_file(src):
        target.write_bytes(src.read_bytes())
    info = audio_probe.probe(target)
    if not 3.0 <= info["duration"] <= 10.0:
        raise audio_probe.AudioValidationError(f"voice reference is {info['duration']:.1f}s; OmniVoice recommends 3-10 s")
    manifest.data["voice"] = {"id": v.get("id"), "mode": "clone", "reference": ref["audio"],
                              "reference_sha256": sha256_file(target), "reference_duration": info["duration"],
                              "design": made.get("design"), "license_status": v["license"]["status"],
                              "provenance": ref.get("provenance")}
    return target


def join_wavs(parts, pause_seconds, out_path):
    """Concatenate same-format PCM WAVs with silence between them; returns sentence spans."""
    spans, frames, params = [], [], None
    cursor = 0
    for i, path in enumerate(parts):
        with wave.open(str(path), "rb") as w:
            p = (w.getnchannels(), w.getsampwidth(), w.getframerate())
            if params is None:
                params = p
            elif p != params:
                raise audio_probe.AudioValidationError(f"{path}: format {p} differs from {params}")
            data = w.readframes(w.getnframes())
            n = w.getnframes()
        if i:
            gap = int(round(pause_seconds * params[2]))
            frames.append(b"\x00" * gap * params[0] * params[1])
            cursor += gap
        spans.append((cursor / params[2], (cursor + n) / params[2]))
        frames.append(data)
        cursor += n
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(out_path), "wb") as w:
        w.setnchannels(params[0])
        w.setsampwidth(params[1])
        w.setframerate(params[2])
        w.writeframes(b"".join(frames))
    return spans, cursor / params[2]


def generate(project_dir, client=None, regenerate=False, log=print):
    """Synthesise every sentence (cached), build beat WAVs, record measured timings."""
    project_dir = Path(project_dir)
    narration = load(project_dir)
    sources = json.loads((project_dir / "research" / "sources.json").read_text(encoding="utf-8"))
    errors = validate(narration, sources)
    if errors:
        raise ValueError("narration.json invalid: " + "; ".join(errors))
    client = client or ov.OmniVoiceClient()
    manifest = AudioManifest(project_dir)
    ensure_reference(client, narration, project_dir, manifest, regenerate, log)
    voice, params = voice_spec(narration, project_dir), generation_params(narration)
    pause = narration["pacing"]["sentence_pause_seconds"]
    license_status = narration["voice"]["license"]["status"]
    beats = {}
    for beat in narration["beats"]:
        records = [_segment(client, manifest, project_dir, text, voice, params, f"{beat['id']}.s{i}", regenerate, log,
                            {"role": "sentence", "beat_id": beat["id"], "sentence_index": i,
                             "voice_id": narration["voice"].get("id"), "license_status": license_status})
                   for i, text in enumerate(beat["sentences"])]
        out = project_dir / "audio" / "beats" / f"{beat['id']}.wav"
        spans, joined = join_wavs([project_dir / r["file"] for r in records], pause, out)
        measured = audio_probe.probe(out)["duration"]
        if abs(measured - joined) > 0.002:
            raise audio_probe.AudioValidationError(f"{out}: ffprobe {measured:.4f}s vs joined {joined:.4f}s")
        beats[beat["id"]] = {"file": manifest.rel(out), "duration": measured, "sha256": sha256_file(out),
                             "sentence_pause_seconds": pause,
                             "sentences": [{"index": i, "text": r["text"], "start": round(s, 6), "end": round(e, 6),
                                            "cache_key": r["cache_key"]} for i, (r, (s, e)) in enumerate(zip(records, spans))]}
        log(f"BEAT {beat['id']}: {measured:.2f}s ({len(records)} sentences)")
    manifest.data["beats"] = beats
    manifest.data["narration_sha256"] = narration_hash(narration)
    manifest.save()
    return manifest.data


def narration_hash(narration):
    import hashlib
    core = {"voice": narration["voice"], "pacing": narration["pacing"],
            "beats": [{"id": b["id"], "sentences": b["sentences"]} for b in narration["beats"]]}
    return hashlib.sha256(json.dumps(core, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
