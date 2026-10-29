"""Provider-independent narration interface + rights registry (stdlib only).

The narration pipeline (pipeline/narration.py) talks to a `NarrationAdapter`,
never to a concrete TTS client, so replacing the voice provider does not touch
the scheduler, the assembler or the gates. Every provider has a *rights class*
in config/tts_providers.json:

  INTERNAL_PREVIEW_ONLY  usable for internal timing/pacing previews only
  PENDING_REVIEW         not evaluated or not yet human-approved; not usable for publication
  PUBLICATION_CLEARED    a named human recorded the clearance (cleared_by/cleared_on/evidence)
  REJECTED               must not be used at all

The rights class is part of every audio cache key, so audio produced under one
class can never be served as audio of another (in particular, restricted
preview audio is never reused for publication because its text/duration match).
"""
import hashlib
import json
import shutil
from pathlib import Path

from integrations import audio_probe

ROOT = Path(__file__).resolve().parents[2]
REGISTRY_PATH = ROOT / "config" / "tts_providers.json"
RIGHTS_CLASSES = ("INTERNAL_PREVIEW_ONLY", "PENDING_REVIEW", "PUBLICATION_CLEARED", "REJECTED")
PURPOSES = ("internal_preview", "publication")
PUBLICATION_CLEARED = "PUBLICATION_CLEARED"


class RightsError(RuntimeError):
    """A provider/voice is not licensed for the requested purpose."""


def load_registry(path=None):
    return json.loads(Path(path or REGISTRY_PATH).read_text(encoding="utf-8"))


def validate_registry(registry):
    """Errors in the provider registry (empty when valid)."""
    errors = []
    providers = registry.get("providers") or {}
    if not providers:
        errors.append("tts_providers: no providers")
    for name, info in providers.items():
        rc = info.get("rights_class")
        if rc not in RIGHTS_CLASSES:
            errors.append(f"tts_providers.{name}: rights_class must be one of {RIGHTS_CLASSES}")
        if rc == PUBLICATION_CLEARED:
            clearance = info.get("clearance") or {}
            missing = [k for k in ("cleared_by", "cleared_on", "evidence") if not clearance.get(k)]
            if missing:
                errors.append(f"tts_providers.{name}: PUBLICATION_CLEARED needs a human clearance record "
                              f"(missing {', '.join(missing)})")
        if not info.get("license"):
            errors.append(f"tts_providers.{name}: record the licence terms (license)")
    for purpose, names in (registry.get("workflow") or {}).items():
        for name in names:
            if name not in providers:
                errors.append(f"tts_providers.workflow.{purpose}: unknown provider {name}")
            elif purpose == "publication" and providers[name].get("rights_class") != PUBLICATION_CLEARED:
                errors.append(f"tts_providers.workflow.publication lists {name}, which is "
                              f"{providers[name].get('rights_class')}, not {PUBLICATION_CLEARED}")
    return errors


def rights_class(provider, registry=None):
    registry = registry or load_registry()
    info = (registry.get("providers") or {}).get(provider)
    if info is None:
        raise RightsError(f"TTS provider {provider!r} is not in config/tts_providers.json")
    return info["rights_class"]


def check_purpose(provider, purpose, registry=None):
    """Raise RightsError unless `provider` may produce audio for `purpose`; returns its rights class."""
    if purpose not in PURPOSES:
        raise ValueError(f"purpose must be one of {PURPOSES}")
    rc = rights_class(provider, registry)
    if rc == "REJECTED":
        raise RightsError(f"TTS provider {provider} is REJECTED")
    if purpose == "publication" and rc != PUBLICATION_CLEARED:
        raise RightsError(f"TTS provider {provider} is {rc}: it cannot produce publication audio "
                          "(see docs/licensing/TTS_LICENSE_AUDIT.md)")
    return rc


class NarrationAdapter:
    """What the narration pipeline needs from a voice provider."""
    name = "abstract"
    adapter_version = "0"
    model = None
    model_revision = None

    def prepare(self, voice_cfg, project_dir, cached_segment, log):
        """Called once per run before any sentence (e.g. build a reference clip); returns a voice object."""
        raise NotImplementedError

    def voice_identity(self, voice):
        """JSON-able identity of the voice for cache keys (content hashes, not paths)."""
        raise NotImplementedError

    def params(self, voice_cfg):
        """JSON-able generation settings for cache keys."""
        return dict(voice_cfg.get("params") or {})

    def source_identity(self, segment_id, project_dir, voice=None):
        """Extra cache-key input per segment (e.g. the hash of a recorded take); None for generators."""
        return None

    def synthesize(self, text, voice, out_path, params, segment_id, project_dir):
        """Write speech for `text` to out_path and return an omnivoice.SynthesisResult-like object."""
        raise NotImplementedError


class OmniVoiceAdapter(NarrationAdapter):
    """Local OmniVoice (rights class from the registry: INTERNAL_PREVIEW_ONLY at the 2026-10-27 audit)."""
    name = "omnivoice"

    def __init__(self, client=None):
        from integrations.tts import omnivoice as ov
        self.ov = ov
        self.client = client or ov.OmniVoiceClient()
        self.adapter_version = ov.ADAPTER_VERSION
        self.model = "k2-fsa/OmniVoice"
        self.model_revision = self.client.model_revision

    def prepare(self, voice_cfg, project_dir, cached_segment, log):
        ov = self.ov
        if voice_cfg.get("mode") != "clone":
            return ov.VoiceSpec(mode="design", language=voice_cfg.get("language", "English"),
                                design=voice_cfg.get("design") or {})
        ref = voice_cfg["reference"]
        made = ref.get("made_with") or {}
        design = ov.VoiceSpec(mode="design", language=voice_cfg.get("language", "English"),
                              design=made.get("design") or {})
        record = cached_segment(ref["text"], ref["text"], design, ov.GenerationParams(), "voice reference",
                                {"role": "voice_reference"})
        target = Path(project_dir) / ref["audio"]
        target.parent.mkdir(parents=True, exist_ok=True)
        src = Path(project_dir) / record["file"]
        if not target.is_file() or sha(target) != sha(src):
            target.write_bytes(src.read_bytes())
        info = audio_probe.probe(target)
        if not 3.0 <= info["duration"] <= 10.0:
            raise audio_probe.AudioValidationError(
                f"voice reference is {info['duration']:.1f}s; OmniVoice recommends 3-10 s")
        return ov.VoiceSpec(mode="clone", language=voice_cfg.get("language", "English"),
                            reference_audio=str(target), reference_text=ref["text"])

    def voice_identity(self, voice):
        return voice.identity()

    def params(self, voice_cfg):
        from dataclasses import asdict
        return asdict(self.ov.GenerationParams(**(voice_cfg.get("params") or {})))

    def synthesize(self, text, voice, out_path, params, segment_id, project_dir):
        gp = params if isinstance(params, self.ov.GenerationParams) else self.ov.GenerationParams(**params)
        return self.client.synthesize(text, voice, out_path, gp)


class RecordedNarrationAdapter(NarrationAdapter):
    """Human narration: one WAV per sentence at <recordings>/<segment_id>.wav (e.g. audio/recorded/B1.s0.wav).

    Nothing is synthesised; the take is validated (speech rate, level) like a TTS
    segment and copied into the cache, so scheduling and assembly are unchanged.
    """
    name = "human"
    adapter_version = "1.0"
    model = "human-recording"
    model_revision = "n/a"

    def prepare(self, voice_cfg, project_dir, cached_segment, log):
        folder = Path(project_dir) / voice_cfg.get("recordings", "audio/recorded")
        if not folder.is_dir():
            raise FileNotFoundError(f"recordings folder {folder} is missing")
        return {"id": voice_cfg.get("id"), "recordings": str(folder)}

    def voice_identity(self, voice):
        return {"id": voice["id"]}

    def _source(self, segment_id, project_dir, voice=None):
        folder = Path(voice["recordings"]) if voice else Path(project_dir) / "audio/recorded"
        return folder / f"{segment_id}.wav"

    def source_identity(self, segment_id, project_dir, voice=None):
        src = self._source(segment_id, project_dir, voice)
        return sha(src) if src.is_file() else None

    def synthesize(self, text, voice, out_path, params, segment_id, project_dir):
        from integrations.tts.omnivoice import SynthesisResult
        src = self._source(segment_id, project_dir, voice)
        if not src.is_file():
            raise FileNotFoundError(f"missing recorded take {src}")
        info = audio_probe.validate_speech(src, text)
        Path(out_path).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, out_path)
        return SynthesisResult(path=str(out_path), duration=info["duration"], sample_rate=info["sample_rate"],
                               channels=info["channels"], codec=info["codec"], mean_db=info["mean_db"],
                               peak_db=info["peak_db"], words_per_second=info["words_per_second"], status="recorded",
                               elapsed_seconds=0.0, endpoint="file",
                               metadata={"provider": self.name, "adapter_version": self.adapter_version,
                                         "model": self.model, "model_revision": self.model_revision,
                                         "source_file": src.name})


ADAPTERS = {"omnivoice": OmniVoiceAdapter, "human": RecordedNarrationAdapter}


def make_adapter(provider, client=None):
    if provider == "kokoro":   # imported lazily: integrations.tts.kokoro subclasses NarrationAdapter
        from integrations.tts.kokoro import KokoroAdapter
        return KokoroAdapter(client)
    if provider not in ADAPTERS:
        raise RightsError(f"no adapter implemented for TTS provider {provider!r} "
                          "(registry entry only; see docs/licensing/TTS_LICENSE_AUDIT.md)")
    return ADAPTERS[provider](client) if provider == "omnivoice" else ADAPTERS[provider]()


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()
