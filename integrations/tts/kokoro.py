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
# M7 listening test only: American English voices (lang_code "a"), SHA256 checked against the
# VOICES.md prefixes of the pinned revision on 2026-10-30 (tools/kokoro_fetch_voices.py). They are
# NOT audited narration voices: narration (verify_release) refuses them, and the publication
# clearance of 2026-10-29 does not cover them until the owner chooses one and the audit is updated.
AUDITION_VOICE_SHA256 = {
    "af_heart": "0ab5709b8ffab19bfd849cd11d98f75b60af7733253ad0d67b12382a102cb4ff",
    "af_alloy": "6d877149dd8b348fbad12e5845b7e43d975390e9f3b68a811d1d86168bef5aa3",
    "af_aoede": "c03bd1a4c3716c2d8eaa3d50022f62d5c31cfbd6e15933a00b17fefe13841cc4",
    "af_bella": "8cb64e02fcc8de0327a8e13817e49c76c945ecf0052ceac97d3081480e8e48d6",
    "af_jessica": "cdfdccb8cc975aa34ee6b89642963b0064237675de0e41a30ae64cc958dd4e87",
    "af_kore": "8bfbc512321c3db49dff984ac675fa5ac7eaed5a96cc31104d3a9080e179d69d",
    "af_nicole": "c5561808bcf5250fe8c5f5de32caf2d94f27e57e95befdb098c5c85991d4c5da",
    "af_nova": "e0233676ddc21908c37a1f102f6b88a59e4e5c1bd764983616eb9eda629dbcd2",
    "af_river": "e149459bd9c084416b74756b9bd3418256a8b839088abb07d463730c369dab8f",
    "af_sarah": "49bd364ea3be9eb3e9685e8f9a15448c4883112a7c0ff7ab139fa4088b08cef9",
    "af_sky": "c799548aed06e0cb0d655a85a01b48e7f10484d71663f9a3045a5b9362e8512c",
    "am_adam": "ced7e284aba12472891be1da3ab34db84cc05cc02b5889535796dbf2d8b0cb34",
    "am_echo": "8bcfdc852bc985fb45c396c561e571ffb9183930071f962f1b50df5c97b161e8",
    "am_eric": "ada66f0eefff34ec921b1d7474d7ac8bec00cd863c170f1c534916e9b8212aae",
    "am_fenrir": "98e507eca1db08230ae3b6232d59c10aec9630022d19accac4f5d12fcec3c37a",
    "am_liam": "c82550757ddb31308b97f30040dda8c2d609a9e2de6135848d0a948368138518",
    "am_michael": "9a443b79a4b22489a5b0ab7c651a0bcd1a30bef675c28333f06971abbd47bd37",
    "am_onyx": "e8452be16cd0f6da7b4579eaf7b1e4506e92524882053d86d72b96b9a7fed584",
    "am_puck": "dd1d8973f4ce4b7d8ae407c77a435f485dabc052081b80ea75c4f30b84f36223",
    "am_santa": "7f2f7582fa2b1f160e90aafe6d0b442a685e773608b6667e545d743b073e97a7",
}
DEFAULT_PARAMS = {"speed": 1.0, "seed": 0, "lang_code": "b"}


def verify_audition_voice(voice_id):
    """Errors unless voice_id is an audited or audition voice whose file matches its recorded hash."""
    want = VOICE_SHA256.get(voice_id) or AUDITION_VOICE_SHA256.get(voice_id)
    path = snapshot_dir() / "voices" / f"{voice_id}.pt"
    if want is None:
        return [f"voice {voice_id!r} is neither audited nor in the audition list"]
    if not path.is_file():
        return [f"{path} missing (tools/kokoro_fetch_voices.py)"]
    return [] if sha256(path) == want else [f"voices/{voice_id}.pt: SHA256 {sha256(path)[:12]}… differs from {want[:12]}…"]


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
