"""Narration script -> validated, cached, measured beat audio (stdlib only).

script/narration.json defines beats (ordered sentences + claim IDs) and the voice.
Each sentence is synthesised separately (so sentence timings are exact), validated,
cached by content, then joined per beat with fixed pauses at the sample level.
Durations always come from the decoded audio, never from word counts.
"""
import json
import wave
from dataclasses import asdict, is_dataclass
from pathlib import Path

from integrations import audio_probe
from integrations.tts import omnivoice as ov
from integrations.tts import providers
from pipeline import pronunciation as pron
from pipeline.audio_manifest import AudioManifest, cache_key, legacy_cache_key_v1, sha256_file

BEAT_KINDS = ("framing", "fact", "interpretation")
MAX_TAKES = 3
LICENSE_STATUSES = ("APPROVED", "LICENSE_REVIEW_REQUIRED", "NOT_CLEARED", "REJECTED")
CLAIM_STATUSES = ("PROVISIONAL", "SOURCE_VERIFIED", "EDITORIALLY_APPROVED", "REJECTED",
                  "provisional", "verified", "contested")  # lower-case: v0.1 ledger values


def load(project_dir):
    path = Path(project_dir) / "script" / "narration.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else None


def voice_cleared(clearance, voice_id, project_id=None):
    """True when the provider clearance covers this voice: listed in voices_cleared, or approved by the
    owner for this project (clearance.voice_approvals, M7). No voices_cleared list = legacy clearance."""
    if clearance.get("voices_cleared") is None or voice_id in clearance["voices_cleared"]:
        return True
    return any(a.get("voice") == voice_id and (project_id is None or project_id in a.get("projects", []))
               for a in clearance.get("voice_approvals", []))


def validate(narration, sources, registry=None, lexicon=None, project_id=None):
    """Errors in narration.json against the claim ledger, the TTS rights registry and the
    pronunciation lexicon (empty list when valid). registry/lexicon checks run when given."""
    errors = []
    claims = {c.get("id"): c for c in (sources or {}).get("claims", [])}
    voice = narration.get("voice") or {}
    lic = voice.get("license") or {}
    if lic.get("status") not in LICENSE_STATUSES:
        errors.append(f"narration.voice.license.status must be one of {LICENSE_STATUSES} "
                      "(record the voice licensing review before generating narration)")
    if not lic.get("components"):
        errors.append("narration.voice.license.components is empty (list model/code/data licences)")
    if registry is not None:
        provider = voice.get("provider")
        info = (registry.get("providers") or {}).get(provider)
        if info is None:
            errors.append(f"narration.voice.provider {provider!r} is not in config/tts_providers.json")
        else:
            if lic.get("rights_class") != info.get("rights_class"):
                errors.append(f"narration.voice.license.rights_class {lic.get('rights_class')!r} disagrees with "
                              f"config/tts_providers.json ({provider}: {info.get('rights_class')!r})")
            if lic.get("status") == "APPROVED" and info.get("rights_class") != providers.PUBLICATION_CLEARED:
                errors.append(f"narration.voice.license.status is APPROVED but provider {provider} is "
                              f"{info.get('rights_class')}")
    if lic.get("status") == "APPROVED" and not (lic.get("approved_by") and lic.get("approved_on")):
        errors.append("narration.voice.license: APPROVED needs approved_by/approved_on (a named human reviewer)")
    cleared = ((registry or {}).get("providers", {}).get(voice.get("provider", "omnivoice")) or {}).get("clearance", {})
    if lic.get("status") == "APPROVED" and not voice_cleared(cleared, voice.get("voice"), project_id):
        errors.append(f"narration.voice.license: APPROVED but voice {voice.get('voice')!r} is not covered by the "
                      f"provider clearance {cleared.get('voices_cleared')} or an owner voice approval for "
                      f"{project_id or 'this project'} (the owner must extend it)")
    if lexicon is not None:
        errors.extend(pron.validate(lexicon))
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
    """OmniVoice VoiceSpec for `tts-check` (the generic path goes through providers.make_adapter)."""
    v = narration["voice"]
    if v.get("mode") == "clone":
        ref = v["reference"]
        return ov.VoiceSpec(mode="clone", language=v.get("language", "English"),
                            reference_audio=str(Path(project_dir) / ref["audio"]), reference_text=ref["text"])
    return ov.VoiceSpec(mode="design", language=v.get("language", "English"), design=v.get("design") or {})


class _Run:
    """One `narrate` run: adapter + manifest + the rights/voice context that goes into every cache key."""

    def __init__(self, adapter, manifest, project_dir, rights_class, voice_id, regenerate, log):
        self.adapter, self.manifest, self.project_dir = adapter, manifest, Path(project_dir)
        self.rights_class, self.voice_id, self.regenerate, self.log = rights_class, voice_id, regenerate, log

    def segment(self, text, spoken, voice, params, label, segment_id, extra):
        a = self.adapter
        pd = asdict(params) if is_dataclass(params) else dict(params)
        identity = a.voice_identity(voice)
        key = cache_key(a.name, a.adapter_version, a.model, a.model_revision, spoken, self.voice_id, identity, pd,
                        self.rights_class, a.source_identity(segment_id, self.project_dir, voice))
        labels = dict(extra, text=text, spoken_text=spoken, voice_id=self.voice_id, rights_class=self.rights_class)
        if not self.regenerate:
            cached = self.manifest.lookup(key)
            if cached:
                self.log(f"CACHED {label}: {cached['duration']:.2f}s")
                return cached
            # M3 (v1) takes: same provider/model/voice/params/text, produced as preview audio.
            if (self.rights_class == "INTERNAL_PREVIEW_ONLY" and spoken == text and a.name == "omnivoice"):
                legacy = legacy_cache_key_v1(a.name, a.adapter_version, a.model_revision, text, identity, pd)
                adopted = self.manifest.adopt(legacy, key, labels)
                if adopted:
                    self.manifest.save()
                    self.log(f"CACHED {label}: {adopted['duration']:.2f}s (M3 take, re-keyed as {self.rights_class})")
                    return adopted
        out = self.project_dir / "audio" / "segments" / f"{key[:20]}.wav"
        for attempt in range(1, MAX_TAKES + 1):  # generation is stochastic: a rushed/garbled take gets a retake
            try:
                result = a.synthesize(spoken, voice, out, params, segment_id, self.project_dir)
                break
            except audio_probe.AudioValidationError as e:
                self.log(f"RETAKE {label} (take {attempt}/{MAX_TAKES} rejected: {e})")
                if attempt == MAX_TAKES:
                    raise
        record = self.manifest.store(key, dict(labels, file=self.manifest.rel(out), duration=result.duration,
                                               sample_rate=result.sample_rate, channels=result.channels,
                                               codec=result.codec, mean_db=result.mean_db, peak_db=result.peak_db,
                                               words_per_second=result.words_per_second, params=pd,
                                               endpoint=result.endpoint, elapsed_seconds=result.elapsed_seconds,
                                               takes=attempt, **result.metadata))
        self.manifest.save()  # persist every successful segment immediately (a later failure must not lose it)
        self.log(f"GENERATED {label}: {result.duration:.2f}s in {result.elapsed_seconds:.1f}s")
        return record


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


def generate(project_dir, client=None, regenerate=False, log=print, purpose="internal_preview", registry=None):
    """Synthesise every sentence (cached), build beat WAVs, record measured timings.

    `client` may be a providers.NarrationAdapter or, for OmniVoice, an OmniVoiceClient.
    `purpose="publication"` refuses any provider whose rights class is not PUBLICATION_CLEARED.
    """
    project_dir = Path(project_dir)
    narration = load(project_dir)
    sources = json.loads((project_dir / "research" / "sources.json").read_text(encoding="utf-8"))
    registry = registry or providers.load_registry()
    lexicon = pron.load(project_dir)
    errors = validate(narration, sources, registry, lexicon, project_dir.name)
    if errors:
        raise ValueError("narration.json invalid: " + "; ".join(errors))
    v = narration["voice"]
    provider = v.get("provider", "omnivoice")
    rights = providers.check_purpose(provider, purpose, registry)
    adapter = client if isinstance(client, providers.NarrationAdapter) else providers.make_adapter(provider, client)
    manifest = AudioManifest(project_dir)
    run = _Run(adapter, manifest, project_dir, rights, v.get("id"), regenerate, log)
    voice = adapter.prepare(v, project_dir, lambda text, spoken, vo, params, label, extra:
                            run.segment(text, spoken, vo, params, label, "voice_reference", extra), log)
    params = adapter.params(v)
    pause = narration["pacing"]["sentence_pause_seconds"]
    manifest.data["voice"] = {"id": v.get("id"), "provider": provider, "mode": v.get("mode"),
                              "rights_class": rights, "license_status": v["license"]["status"],
                              "provenance": (v.get("reference") or {}).get("provenance")}
    if v.get("mode") == "clone":
        ref = project_dir / v["reference"]["audio"]
        manifest.data["voice"].update(reference=v["reference"]["audio"], reference_sha256=sha256_file(ref),
                                      reference_duration=audio_probe.probe(ref)["duration"],
                                      design=(v["reference"].get("made_with") or {}).get("design"))
    beats = {}
    for beat in narration["beats"]:
        records = []
        for i, text in enumerate(beat["sentences"]):
            spoken, applied = pron.spoken_text(text, lexicon, provider)
            seg_id = f"{beat['id']}.s{i}"
            records.append(run.segment(text, spoken, voice, params, seg_id, seg_id,
                                       {"role": "sentence", "beat_id": beat["id"], "sentence_index": i,
                                        "pronunciation": applied, "license_status": v["license"]["status"]}))
        out = project_dir / "audio" / "beats" / f"{beat['id']}.wav"
        spans, joined = join_wavs([project_dir / r["file"] for r in records], pause, out)
        measured = audio_probe.probe(out)["duration"]
        if abs(measured - joined) > 0.002:
            raise audio_probe.AudioValidationError(f"{out}: ffprobe {measured:.4f}s vs joined {joined:.4f}s")
        beats[beat["id"]] = {"file": manifest.rel(out), "duration": measured, "sha256": sha256_file(out),
                             "sentence_pause_seconds": pause,
                             "sentences": [{"index": i, "text": r["text"], "start": round(s, 6), "end": round(e, 6),
                                            "cache_key": r["cache_key"], "rights_class": r.get("rights_class")}
                                           for i, (r, (s, e)) in enumerate(zip(records, spans))]}
        log(f"BEAT {beat['id']}: {measured:.2f}s ({len(records)} sentences)")
    manifest.data["beats"] = beats
    manifest.data["rights"] = {"provider": provider, "rights_class": rights, "purpose": purpose,
                               "audit": registry["providers"][provider].get("audit",
                                                                            "docs/licensing/TTS_LICENSE_AUDIT.md")}
    manifest.data["narration_sha256"] = narration_hash(narration, lexicon)
    manifest.save()
    return manifest.data


NON_AUDIO_VOICE_KEYS = ("license", "pace_note", "selection", "pronunciation_review")   # M6: human review records


def narration_hash(narration, lexicon=None):
    """Hash of everything that changes the narration audio (licence records excluded; spoken forms included)."""
    import hashlib
    voice = {k: v for k, v in narration["voice"].items() if k not in NON_AUDIO_VOICE_KEYS}
    provider = voice.get("provider", "omnivoice")
    core = {"voice": voice, "pacing": narration["pacing"],
            "beats": [{"id": b["id"], "sentences": b["sentences"],
                       "spoken": [pron.spoken_text(t, lexicon, provider)[0] for t in b["sentences"]]}
                      for b in narration["beats"]]}
    return hashlib.sha256(json.dumps(core, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
