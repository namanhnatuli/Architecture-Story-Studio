"""OmniVoice TTS adapter (stdlib only).

Talks to the *local* OmniVoice Gradio demo (``omnivoice-demo``), whose HTTP API
was inspected on 2026-10-27 (OmniVoice 0.1.5, gradio 6.15.2):

  GET  /gradio_api/info                        endpoint + parameter contract
  POST /gradio_api/upload                      multipart "files" -> server paths
  POST /gradio_api/call/<endpoint>  {"data"}   -> {"event_id"}
  GET  /gradio_api/call/<endpoint>/<event_id>  SSE: event: complete|error|heartbeat
  GET  /gradio_api/file=<path>                 generated WAV (int16, 24 kHz mono)

Endpoints: ``/_design_fn`` (voice design from attributes) and ``/_clone_fn``
(voice cloning from a reference clip). Generation errors come back as a
status string, not an HTTP error, so the status is checked explicitly.

Parameters are matched to the live contract by *label*, never by a hard-coded
position, so an OmniVoice upgrade that changes the form fails loudly
(OmniVoiceContractError) instead of sending wrong values.

Configuration (environment):
  OMNIVOICE_URL              default http://127.0.0.1:8001 (localhost only by default)
  OMNIVOICE_TIMEOUT          seconds per generation, default 300
  OMNIVOICE_RETRIES          connection retries, default 2
  OMNIVOICE_MODEL_REVISION   recorded in metadata/cache keys; default read from the
                             local Hugging Face cache refs if present, else "unknown"
"""
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path

from integrations import audio_probe

ADAPTER_VERSION = "1.0"
DEFAULT_URL = "http://127.0.0.1:8001"
SUCCESS_STATUS = "Done."


class OmniVoiceError(RuntimeError):
    """Base class for OmniVoice adapter errors."""


class OmniVoiceUnavailable(OmniVoiceError):
    """Service not reachable (not started, wrong URL/port)."""


class OmniVoiceProtocolError(OmniVoiceError):
    """Response did not match the documented Gradio protocol."""


class OmniVoiceContractError(OmniVoiceError):
    """The running OmniVoice form no longer matches what this adapter expects."""


class OmniVoiceGenerationError(OmniVoiceError):
    """OmniVoice reported a failed generation (error event or non-'Done.' status)."""


class OmniVoiceTimeout(OmniVoiceError):
    """Generation did not complete within the timeout."""


# Label (English part) -> adapter key.
LABEL_KEYS = {
    "Text to Synthesize": "text", "Language": "language", "Reference Audio": "ref_audio",
    "Reference Text": "ref_text", "Instruct": "instruct", "Inference Steps": "num_step",
    "Guidance Scale": "guidance_scale", "Denoise": "denoise", "Speed": "speed",
    "Duration": "duration", "Preprocess Prompt": "preprocess_prompt",
    "Postprocess Output": "postprocess_output", "Gender": "gender", "Age": "age",
    "Pitch": "pitch", "Style": "style", "English Accent": "accent", "Chinese Dialect": "dialect",
}
DESIGN_ATTRIBUTES = ("gender", "age", "pitch", "style", "accent", "dialect")


def _label_key(label):
    english = (label or "").split(" / ")[0].split(" (")[0].strip()
    return LABEL_KEYS.get(english)


def _english(option):
    return option.split(" / ")[0].strip()


@dataclass
class VoiceSpec:
    """A narrator voice. mode 'design': attributes only; 'clone': a reference clip
    (the studio uses a *synthetic* reference made with voice design, never a real
    person's recording)."""
    mode: str = "design"
    language: str = "English"
    design: dict = field(default_factory=dict)   # e.g. {"gender": "Male", "accent": "British Accent"}
    reference_audio: str = None
    reference_text: str = None
    instruct: str = None

    def identity(self):
        """Stable identity for cache keys (reference audio by content hash)."""
        data = asdict(self)
        if self.reference_audio:
            import hashlib
            data["reference_audio"] = hashlib.sha256(Path(self.reference_audio).read_bytes()).hexdigest()
        return data


@dataclass
class GenerationParams:
    num_step: int = 32
    guidance_scale: float = 2.0
    denoise: bool = True
    speed: float = 1.0
    preprocess_prompt: bool = True
    postprocess_output: bool = True
    # duration is deliberately not exposed: forcing a length distorts the voice.


@dataclass
class SynthesisResult:
    path: str
    duration: float
    sample_rate: int
    channels: int
    codec: str
    mean_db: float
    peak_db: float
    words_per_second: float
    status: str
    elapsed_seconds: float
    endpoint: str
    metadata: dict


def default_model_revision():
    env = os.environ.get("OMNIVOICE_MODEL_REVISION")
    if env:
        return env
    ref = Path.home() / ".cache/huggingface/hub/models--k2-fsa--OmniVoice/refs/main"
    try:
        return ref.read_text().strip() or "unknown"
    except OSError:
        return "unknown"


class OmniVoiceClient:
    def __init__(self, base_url=None, timeout=None, retries=None, model_revision=None):
        self.base_url = (base_url or os.environ.get("OMNIVOICE_URL") or DEFAULT_URL).rstrip("/")
        self.timeout = float(timeout if timeout is not None else os.environ.get("OMNIVOICE_TIMEOUT", 300))
        self.retries = int(retries if retries is not None else os.environ.get("OMNIVOICE_RETRIES", 2))
        self.model_revision = model_revision or default_model_revision()
        self._contract = None

    # ------------------------------------------------------------ HTTP helpers
    def _url(self, path):
        return f"{self.base_url}{path}"

    def _request(self, method, path, body=None, headers=None, timeout=10.0, retry=True):
        attempts = (self.retries + 1) if retry else 1
        last = None
        for attempt in range(attempts):
            req = urllib.request.Request(self._url(path), data=body, method=method, headers=headers or {})
            try:
                with urllib.request.urlopen(req, timeout=timeout) as resp:
                    return resp.read()
            except urllib.error.HTTPError as e:
                raise OmniVoiceProtocolError(f"{method} {path}: HTTP {e.code}") from None
            except (urllib.error.URLError, ConnectionError, TimeoutError, OSError) as e:
                last = e
                if attempt + 1 < attempts:
                    time.sleep(min(2.0 ** attempt, 4.0))
        raise OmniVoiceUnavailable(f"OmniVoice not reachable at {self.base_url} ({last}). "
                                   "Start it with: omnivoice-demo --ip 127.0.0.1 --port 8001 --no-asr")

    def _json(self, method, path, payload=None, timeout=10.0):
        body = json.dumps(payload).encode() if payload is not None else None
        raw = self._request(method, path, body, {"Content-Type": "application/json"} if body else None, timeout)
        try:
            return json.loads(raw)
        except (json.JSONDecodeError, UnicodeDecodeError):
            raise OmniVoiceProtocolError(f"{method} {path}: response is not JSON") from None

    # ------------------------------------------------------------ contract
    def contract(self, refresh=False):
        if self._contract is None or refresh:
            info = self._json("GET", "/gradio_api/info")
            endpoints = info.get("named_endpoints") if isinstance(info, dict) else None
            if not isinstance(endpoints, dict) or not endpoints:
                raise OmniVoiceProtocolError("/gradio_api/info has no named_endpoints")
            parsed = {}
            for name, ep in endpoints.items():
                params = []
                for p in ep.get("parameters", []):
                    params.append({"key": _label_key(p.get("label")), "label": p.get("label"),
                                   "enum": (p.get("type") or {}).get("enum"),
                                   "default": p.get("parameter_default") if p.get("parameter_has_default") else None})
                parsed[name] = params
            design = [n for n, ps in parsed.items() if {"text", "gender"} <= {p["key"] for p in ps}]
            clone = [n for n, ps in parsed.items() if {"text", "ref_audio"} <= {p["key"] for p in ps}]
            if not design or not clone:
                raise OmniVoiceContractError(f"expected a voice-design and a voice-clone endpoint, got {sorted(parsed)}")
            self._contract = {"design": design[0], "clone": clone[0], "params": parsed}
        return self._contract

    def health(self):
        """Reachable + contract understood. Returns a summary (no secrets)."""
        c = self.contract(refresh=True)
        langs = next(p["enum"] for p in c["params"][c["design"]] if p["key"] == "language")
        return {"ok": True, "url": self.base_url, "design_endpoint": c["design"], "clone_endpoint": c["clone"],
                "languages": len(langs or []), "english_supported": "English" in (langs or []),
                "model_revision": self.model_revision, "adapter_version": ADAPTER_VERSION}

    def voice_options(self):
        """Voice-design attribute options (English labels) from the live contract."""
        c = self.contract()
        return {p["key"]: [_english(o) for o in (p["enum"] or []) if o != "Auto"]
                for p in c["params"][c["design"]] if p["key"] in DESIGN_ATTRIBUTES}

    def validate_voice(self, spec):
        """List of problems with a VoiceSpec (empty when valid)."""
        problems = []
        c = self.contract()
        langs = next(p["enum"] for p in c["params"][c["design"]] if p["key"] == "language") or []
        if spec.language not in langs:
            problems.append(f"language '{spec.language}' not offered by OmniVoice")
        if spec.mode == "design":
            options = self.voice_options()
            for key, value in (spec.design or {}).items():
                if key not in options:
                    problems.append(f"unknown design attribute '{key}' (known: {sorted(options)})")
                elif value not in options[key]:
                    problems.append(f"design {key}='{value}' not in {options[key]}")
        elif spec.mode == "clone":
            if not spec.reference_audio or not Path(spec.reference_audio).is_file():
                problems.append(f"clone reference audio missing: {spec.reference_audio}")
            if not spec.reference_text:
                problems.append("clone reference_text is required (the server runs with --no-asr)")
        else:
            problems.append(f"unknown voice mode '{spec.mode}' (design or clone)")
        return problems

    # ------------------------------------------------------------ generation
    def _upload(self, path):
        boundary = uuid.uuid4().hex
        data = Path(path).read_bytes()
        body = (f"--{boundary}\r\nContent-Disposition: form-data; name=\"files\"; filename=\"{Path(path).name}\"\r\n"
                f"Content-Type: audio/wav\r\n\r\n").encode() + data + f"\r\n--{boundary}--\r\n".encode()
        raw = self._request("POST", "/gradio_api/upload", body,
                            {"Content-Type": f"multipart/form-data; boundary={boundary}"}, timeout=30)
        try:
            paths = json.loads(raw)
            return paths[0]
        except (json.JSONDecodeError, IndexError, KeyError, TypeError):
            raise OmniVoiceProtocolError("upload response did not contain a server path") from None

    def _build_data(self, endpoint, values):
        data = []
        for p in self.contract()["params"][endpoint]:
            key = p["key"]
            if key is None:
                raise OmniVoiceContractError(f"{endpoint}: unrecognised parameter '{p['label']}'")
            if key in DESIGN_ATTRIBUTES:
                wanted = values.get(key)
                if not wanted:
                    data.append("Auto")
                    continue
                match = [o for o in (p["enum"] or []) if _english(o) == wanted]
                if not match:
                    raise OmniVoiceContractError(f"{endpoint}: {key}='{wanted}' is not an option")
                data.append(match[0])
            else:
                data.append(values.get(key, p["default"]))
        return data

    def _wait(self, endpoint, event_id):
        """Read the SSE stream until complete/error; return the data payload."""
        req = urllib.request.Request(self._url(f"/gradio_api/call{endpoint}/{event_id}"))
        deadline = time.monotonic() + self.timeout
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                event = None
                for raw in resp:
                    if time.monotonic() > deadline:
                        raise OmniVoiceTimeout(f"generation exceeded {self.timeout:.0f}s")
                    line = raw.decode("utf-8", "replace").rstrip("\r\n")
                    if line.startswith("event:"):
                        event = line[6:].strip()
                    elif line.startswith("data:") and event in ("complete", "error"):
                        payload = line[5:].strip()
                        if event == "error":
                            raise OmniVoiceGenerationError(f"OmniVoice error event: {payload[:300]}")
                        try:
                            return json.loads(payload)
                        except json.JSONDecodeError:
                            raise OmniVoiceProtocolError("complete event data is not JSON") from None
        except (TimeoutError, OSError) as e:
            if isinstance(e, OmniVoiceError):
                raise
            raise OmniVoiceTimeout(f"no completion within {self.timeout:.0f}s ({e})") from None
        raise OmniVoiceProtocolError("SSE stream ended without a complete/error event")

    def synthesize(self, text, voice, out_path, params=None):
        """Generate speech for `text` into `out_path` (WAV) and validate it."""
        if not text or not text.strip():
            raise ValueError("text is empty")
        params = params or GenerationParams()
        problems = self.validate_voice(voice)
        if problems:
            raise OmniVoiceContractError("; ".join(problems))
        c = self.contract()
        values = dict(asdict(params), text=text.strip(), language=voice.language, duration=None)
        if voice.mode == "design":
            endpoint = c["design"]
            values.update(voice.design or {})
        else:
            endpoint = c["clone"]
            values.update(ref_text=voice.reference_text, instruct=voice.instruct or "",
                          ref_audio={"path": self._upload(voice.reference_audio),
                                     "orig_name": Path(voice.reference_audio).name,
                                     "meta": {"_type": "gradio.FileData"}})
        started = time.monotonic()
        submitted = self._json("POST", f"/gradio_api/call{endpoint}", {"data": self._build_data(endpoint, values)})
        event_id = submitted.get("event_id") if isinstance(submitted, dict) else None
        if not event_id:
            raise OmniVoiceProtocolError("call response has no event_id")
        result = self._wait(endpoint, event_id)
        if not isinstance(result, list) or len(result) < 2:
            raise OmniVoiceProtocolError(f"unexpected result shape: {str(result)[:200]}")
        audio, status = result[0], result[1]
        if status != SUCCESS_STATUS or not isinstance(audio, dict) or not audio.get("url"):
            raise OmniVoiceGenerationError(f"OmniVoice status: {status!r}")
        url = urllib.parse.urlsplit(audio["url"])
        out = Path(out_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(self._request("GET", url.path + ("?" + url.query if url.query else ""), timeout=60))
        info = audio_probe.validate_speech(out, text)
        return SynthesisResult(path=str(out), duration=info["duration"], sample_rate=info["sample_rate"],
                               channels=info["channels"], codec=info["codec"], mean_db=info["mean_db"],
                               peak_db=info["peak_db"], words_per_second=info["words_per_second"],
                               status=status, elapsed_seconds=round(time.monotonic() - started, 2),
                               endpoint=endpoint, metadata=self.metadata())

    def metadata(self):
        return {"provider": "omnivoice", "adapter_version": ADAPTER_VERSION, "url": self.base_url,
                "model": "k2-fsa/OmniVoice", "model_revision": self.model_revision}
