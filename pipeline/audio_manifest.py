"""Content-addressed TTS cache + narration audio manifest (stdlib only).

A segment is reused when an identical request was generated before:
same provider/adapter, text, voice identity (reference clip by content hash),
generation parameters and model revision. Regeneration is explicit (--regenerate).
"""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

MANIFEST_VERSION = 1


def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def cache_key(provider, adapter_version, model_revision, text, voice_identity, params):
    payload = {"v": MANIFEST_VERSION, "provider": provider, "adapter": adapter_version,
               "model_revision": model_revision, "text": text.strip(), "voice": voice_identity, "params": params}
    return hashlib.sha256(json.dumps(payload, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


class AudioManifest:
    def __init__(self, project_dir):
        self.project_dir = Path(project_dir)
        self.path = self.project_dir / "audio" / "narration_manifest.json"
        if self.path.is_file():
            self.data = json.loads(self.path.read_text(encoding="utf-8"))
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

    def store(self, key, record):
        record = dict(record, cache_key=key, sha256=sha256_file(self.project_dir / record["file"]),
                      stored_utc=datetime.now(timezone.utc).isoformat())
        self.data["segments"][key] = record
        return record

    def save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self.data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
