"""Content-addressed TTS cache + narration audio manifest (stdlib only).

A segment is reused when an identical request was generated before: same
provider/adapter, model + revision, voice id + identity (reference clip by content
hash), *spoken* text (after pronunciation overrides), generation parameters and
rights class. Regeneration is explicit (--regenerate).

Version 1 keys (M3) had no model id, voice id or rights class. A v1 record is
adopted into v2 only for an INTERNAL_PREVIEW_ONLY run whose spoken text equals the
written text (narration.py), so M3 takes are preserved but can never become
publication audio.
"""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

MANIFEST_VERSION = 2


def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _digest(payload):
    return hashlib.sha256(json.dumps(payload, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def cache_key(provider, adapter_version, model, model_revision, spoken_text, voice_id, voice_identity, params,
              rights_class, source_identity=None):
    payload = {"v": 2, "provider": provider, "adapter": adapter_version, "model": model,
               "model_revision": model_revision, "text": spoken_text.strip(), "voice_id": voice_id,
               "voice": voice_identity, "params": params, "rights_class": rights_class}
    if source_identity is not None:
        payload["source"] = source_identity
    return _digest(payload)


def legacy_cache_key_v1(provider, adapter_version, model_revision, text, voice_identity, params):
    """The M3 (manifest v1) key, used only to adopt existing preview takes."""
    return _digest({"v": 1, "provider": provider, "adapter": adapter_version, "model_revision": model_revision,
                    "text": text.strip(), "voice": voice_identity, "params": params})


class AudioManifest:
    def __init__(self, project_dir):
        self.project_dir = Path(project_dir)
        self.path = self.project_dir / "audio" / "narration_manifest.json"
        if self.path.is_file():
            self.data = json.loads(self.path.read_text(encoding="utf-8"))
            self.data["version"] = MANIFEST_VERSION
        else:
            self.data = {"version": MANIFEST_VERSION, "voice": {}, "segments": {}, "beats": {}}

    def rel(self, path):
        return str(Path(path).resolve().relative_to(self.project_dir.resolve()))

    def lookup(self, key):
        """A cached segment record, only if its file still exists with the recorded hash."""
        rec = self.data["segments"].get(key)
        if not rec:
            return None
        f = self.project_dir / rec["file"]
        if not f.is_file() or sha256_file(f) != rec["sha256"]:
            return None
        return rec

    def adopt(self, legacy_key, key, extra):
        """Re-key a valid v1 record under its v2 key (same file, same audio); None if absent/invalid."""
        rec = self.lookup(legacy_key)
        if not rec:
            return None
        rec = dict(rec, **extra, cache_key=key, legacy_cache_key=legacy_key)
        del self.data["segments"][legacy_key]
        self.data["segments"][key] = rec
        return rec

    def store(self, key, record):
        record = dict(record, cache_key=key, sha256=sha256_file(self.project_dir / record["file"]),
                      stored_utc=datetime.now(timezone.utc).isoformat())
        self.data["segments"][key] = record
        return record

    def save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self.data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
