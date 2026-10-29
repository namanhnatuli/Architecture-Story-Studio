"""Kokoro-82M narration adapter (M6; stdlib only on this side).

Local inference through tools/kokoro_tts.py running under the *isolated* Kokoro
interpreter (env KOKORO_PYTHON, default ~/Work/Projects/Kokoro/.venv/bin/python;
installation and licences: docs/licensing/KOKORO_LICENSE_AUDIT.md). The worker is a
child process spoken to over stdin/stdout JSON lines for one `narrate` run: no network
server, Hugging Face offline, CPU.

Pinned release (official repo hexgrad/Kokoro-82M):
  revision f3ff3571791e39611d31c381e3a41a3af07b4987, kokoro-v1_0.pth SHA256 496dba11…
  (equals the model-card hash). The model and the selected voice file are hashed
  before generation; a mismatch stops generation.

Cache identity (pipeline/audio_manifest.cache_key): provider, adapter version, model,
model revision, spoken text, voice id, voice identity (voice file SHA256 + language),
generation params (speed, seed, lang_code) and the rights class - so Kokoro audio can
never be served for OmniVoice audio or vice versa.
"""
import atexit
import hashlib
import json
import os
import subprocess
import time
from pathlib import Path

from integrations import audio_probe
from integrations.tts.providers import NarrationAdapter

ROOT = Path(__file__).resolve().parents[2]
ADAPTER_VERSION = "1.0"
REPO = "hexgrad/Kokoro-82M"
REVISION = "f3ff3571791e39611d31c381e3a41a3af07b4987"
MODEL_FILE = "kokoro-v1_0.pth"
MODEL_SHA256 = "496dba118d1a58f5f3db2efc88dbdc216e0483fc89fe6e47ee1f2c53f18ad1e4"
CONFIG_SHA256 = "5abb01e2403b072bf03d04fde160443e209d7a0dad49a423be15196b9b43c17f"
VOICE_SHA256 = {   # VOICES.md prefixes verified on 2026-10-28
    "bf_emma": "d0a423deabf4a52b4f49318c51742c54e21bb89bbbe9a12141e7758ddb5da701",
    "bm_fable": "d44935f3135257a9064df99f007fc1342ff1aa767552b4a4fa4c3b2e6e59079c",
    "bm_george": "f1bc812213dc59774769e5c80004b13eeb79bd78130b11b2d7f934542dab811b",
    "bm_daniel": "fc3fce4e9c12ed4dbc8fa9680cfe51ee190a96444ce7c3ad647549a30823fc5d",
}
DEFAULT_PARAMS = {"speed": 1.0, "seed": 0, "lang_code": "b"}


class KokoroError(RuntimeError):
    pass


class KokoroUnavailable(KokoroError):
    pass


def kokoro_python():
    return os.environ.get("KOKORO_PYTHON", str(Path.home() / "Work/Projects/Kokoro/.venv/bin/python"))


def snapshot_dir():
    hub = Path(os.environ.get("HF_HUB_CACHE", Path.home() / ".cache/huggingface/hub"))
    return hub / "models--hexgrad--Kokoro-82M" / "snapshots" / REVISION


def sha256(path, cache={}):
    path = Path(path)
    key = (str(path), path.stat().st_mtime_ns, path.stat().st_size)
    if key not in cache:
        h = hashlib.sha256()
        with path.open("rb") as f:
            for block in iter(lambda: f.read(1 << 20), b""):
                h.update(block)
        cache[key] = h.hexdigest()
    return cache[key]


def verify_release(voice_id):
    """Errors if the pinned files are missing or differ from the audited hashes."""
    snap = snapshot_dir()
    errors = []
    for rel, want in ((MODEL_FILE, MODEL_SHA256), ("config.json", CONFIG_SHA256),
                      (f"voices/{voice_id}.pt", VOICE_SHA256.get(voice_id))):
        p = snap / rel
        if want is None:
            errors.append(f"voice {voice_id!r} is not in the audited voice list {sorted(VOICE_SHA256)}")
        elif not p.is_file():
            errors.append(f"{p} missing (download the pinned revision, docs/licensing/KOKORO_LICENSE_AUDIT.md)")
        elif sha256(p) != want:
            errors.append(f"{rel}: SHA256 {sha256(p)[:12]}… differs from the audited {want[:12]}…")
    if not Path(kokoro_python()).is_file():
        errors.append(f"Kokoro interpreter not found: {kokoro_python()} (set KOKORO_PYTHON)")
    return errors


class KokoroWorker:
    """One local child process (tools/kokoro_tts.py --serve) for a run."""

    def __init__(self, threads=4):
        self.threads = threads
        self.proc = None
        self.load_seconds = None

    def _start(self):
        env = dict(os.environ, HF_HUB_OFFLINE="1", TRANSFORMERS_OFFLINE="1", TOKENIZERS_PARALLELISM="false",
                   PYTHONWARNINGS="ignore")
        self.proc = subprocess.Popen([kokoro_python(), str(ROOT / "tools/kokoro_tts.py"), "--serve"],
                                     stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                                     text=True, env=env, cwd=str(ROOT))
        atexit.register(self.close)

    def run(self, items, lang_code):
        if self.proc is None:
            self._start()
        req = {"snapshot": str(snapshot_dir()), "lang_code": lang_code, "threads": self.threads, "items": items}
        self.proc.stdin.write(json.dumps(req) + "\n")
        self.proc.stdin.flush()
        while True:
            line = self.proc.stdout.readline()
            if not line:
                raise KokoroUnavailable("Kokoro worker exited (check KOKORO_PYTHON and the pinned snapshot)")
            if line.startswith("KOKORO_JSON "):
                out = json.loads(line[len("KOKORO_JSON "):])
                if not out.get("ok"):
                    raise KokoroError(out.get("error", "unknown Kokoro error"))
                self.load_seconds = out.get("load_seconds")
                return out["results"]

    def close(self):
        if self.proc and self.proc.poll() is None:
            self.proc.stdin.close()
            try:
                self.proc.wait(timeout=10)
            except subprocess.TimeoutExpired:
                self.proc.kill()
        self.proc = None


class KokoroAdapter(NarrationAdapter):
    name = "kokoro"
    adapter_version = ADAPTER_VERSION
    model = REPO
    model_revision = REVISION

    def __init__(self, worker=None):
        self.worker = worker or KokoroWorker()

    def prepare(self, voice_cfg, project_dir, cached_segment, log):
        vid = voice_cfg.get("voice") or voice_cfg.get("kokoro_voice")
        errors = verify_release(vid)
        if errors:
            raise KokoroUnavailable("; ".join(errors))
        return {"voice": vid, "voice_sha256": VOICE_SHA256[vid], "lang_code": self.params(voice_cfg)["lang_code"]}

    def voice_identity(self, voice):
        return {"voice": voice["voice"], "voice_sha256": voice["voice_sha256"], "model_sha256": MODEL_SHA256,
                "lang_code": voice["lang_code"]}

    def params(self, voice_cfg):
        out = dict(DEFAULT_PARAMS)
        out.update({k: v for k, v in (voice_cfg.get("params") or {}).items() if k in DEFAULT_PARAMS})
        return out

    def synthesize(self, text, voice, out_path, params, segment_id, project_dir):
        from integrations.tts.omnivoice import SynthesisResult
        t0 = time.time()
        res = self.worker.run([{"id": segment_id, "text": text, "voice": voice["voice"],
                                "speed": params["speed"], "seed": params["seed"], "out": str(out_path)}],
                              params["lang_code"])[0]
        info = audio_probe.validate_speech(out_path, text)
        if abs(info["duration"] - res["duration"]) > 0.005:
            raise KokoroError(f"{segment_id}: worker reported {res['duration']:.3f}s, file is {info['duration']:.3f}s")
        return SynthesisResult(path=str(out_path), duration=info["duration"], sample_rate=info["sample_rate"],
                               channels=info["channels"], codec=info["codec"], mean_db=info["mean_db"],
                               peak_db=info["peak_db"], words_per_second=info["words_per_second"], status="Done.",
                               elapsed_seconds=round(time.time() - t0, 3), endpoint="local:tools/kokoro_tts.py",
                               metadata={"provider": self.name, "adapter_version": self.adapter_version,
                                         "model": self.model, "model_revision": self.model_revision,
                                         "model_sha256": MODEL_SHA256, "voice": voice["voice"],
                                         "voice_sha256": voice["voice_sha256"], "phonemes": res["phonemes"],
                                         "lang_code": params["lang_code"]})
