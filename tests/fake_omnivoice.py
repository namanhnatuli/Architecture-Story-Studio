"""A stdlib fake of the OmniVoice Gradio API used by the adapter tests (no model, no network).

Mirrors the real contract inspected on 2026-10-27 (labels, enums, SSE flow, file URLs).
`FakeOmniVoice.mode` switches failure behaviour per test.
"""
import json
import math
import socket
import struct
import threading
import time
import wave
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from io import BytesIO

GENERATION = [
    {"label": "Inference Steps", "parameter_has_default": True, "parameter_default": 32, "type": {"type": "number"}},
    {"label": "Guidance Scale (CFG)", "parameter_has_default": True, "parameter_default": 2.0, "type": {"type": "number"}},
    {"label": "Denoise", "parameter_has_default": True, "parameter_default": True, "type": {"type": "boolean"}},
    {"label": "Speed", "parameter_has_default": True, "parameter_default": 1.0, "type": {"type": "number"}},
    {"label": "Duration (seconds)", "parameter_has_default": False, "type": {"type": "number"}},
    {"label": "Preprocess Prompt", "parameter_has_default": True, "parameter_default": True, "type": {"type": "boolean"}},
    {"label": "Postprocess Output", "parameter_has_default": True, "parameter_default": True, "type": {"type": "boolean"}},
]
TEXT = {"label": "Text to Synthesize / 待合成文本", "parameter_has_default": False, "type": {"type": "string"}}
LANG = {"label": "Language (optional) / 语种 (可选)", "parameter_has_default": True, "parameter_default": "Auto",
        "type": {"type": "string", "enum": ["Auto", "English", "Vietnamese"]}}


def enum(label, options):
    return {"label": label, "parameter_has_default": True, "parameter_default": "Auto",
            "type": {"type": "string", "enum": ["Auto"] + options}}


INFO = {"named_endpoints": {
    "/_clone_fn": {"parameters": [TEXT, LANG,
                                  {"label": "Reference Audio / 参考音频", "parameter_has_default": False, "type": {"type": "object"}},
                                  {"label": "Reference Text (optional) / 参考音频文本（可选）", "parameter_has_default": False, "type": {"type": "string"}},
                                  {"label": "Instruct", "parameter_has_default": False, "type": {"type": "string"}}] + GENERATION,
                   "returns": [{"label": "Output Audio"}, {"label": "Status"}]},
    "/_design_fn": {"parameters": [TEXT, LANG] + GENERATION + [
        enum("Gender / 性别", ["Male / 男", "Female / 女"]),
        enum("Age / 年龄", ["Young Adult / 青年", "Middle-aged / 中年"]),
        enum("Pitch / 音调", ["Low Pitch / 低音调", "Moderate Pitch / 中音调"]),
        enum("Style / 风格", ["Whisper / 耳语"]),
        enum("English Accent / 英文口音", ["American Accent / 美式口音", "British Accent / 英国口音"]),
        enum("Chinese Dialect / 中文方言", ["Sichuan Dialect / 四川话"])],
        "returns": [{"label": "Output Audio"}, {"label": "Status"}]},
}, "unnamed_endpoints": {}}


def wav_bytes(seconds=2.0, amplitude=0.3, rate=24000):
    buf = BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        frames = int(seconds * rate)
        w.writeframes(b"".join(struct.pack("<h", int(32767 * amplitude * math.sin(2 * math.pi * 220 * i / rate)))
                               for i in range(frames)))
    return buf.getvalue()


class FakeOmniVoice:
    def __init__(self):
        self.mode = "ok"
        self.calls = []          # (endpoint, data) per generation request
        self.uploads = 0
        fake = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass

            def _send(self, code, body, ctype="application/json"):
                self.send_response(code)
                self.send_header("Content-Type", ctype)
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def do_GET(self):
                if self.path == "/gradio_api/info":
                    if fake.mode == "bad_json":
                        return self._send(200, b"<html>not json</html>", "text/html")
                    info = json.loads(json.dumps(INFO))
                    if fake.mode == "contract_changed":
                        info["named_endpoints"]["/_design_fn"]["parameters"] = [TEXT, LANG] + GENERATION
                    return self._send(200, json.dumps(info).encode())
                if self.path.startswith("/gradio_api/call/"):
                    if fake.mode == "slow":
                        time.sleep(3)
                    self.send_response(200)
                    self.send_header("Content-Type", "text/event-stream")
                    self.end_headers()
                    if fake.mode == "error_event":
                        events = "event: error\ndata: null\n\n"
                    else:
                        status = "Error: RuntimeError: boom" if fake.mode == "bad_status" else "Done."
                        url = f"http://127.0.0.1:{fake.port}/gradio_api/file=/tmp/fake/audio.wav"
                        payload = [{"path": "/tmp/fake/audio.wav", "url": url, "meta": {"_type": "gradio.FileData"}}, status]
                        events = f"event: heartbeat\ndata: null\n\nevent: complete\ndata: {json.dumps(payload)}\n\n"
                    self.wfile.write(events.encode())
                    return None
                if self.path.startswith("/gradio_api/file="):
                    amplitude = 0.0 if fake.mode == "silent" else 0.3
                    return self._send(200, wav_bytes(amplitude=amplitude), "audio/wav")
                return self._send(404, b"{}")

            def do_POST(self):
                length = int(self.headers.get("Content-Length", 0))
                body = self.rfile.read(length)
                if self.path == "/gradio_api/upload":
                    fake.uploads += 1
                    return self._send(200, json.dumps(["/tmp/fake/upload/ref.wav"]).encode())
                if self.path.startswith("/gradio_api/call/"):
                    fake.calls.append((self.path.rsplit("/", 1)[-1], json.loads(body)["data"]))
                    if fake.mode == "no_event_id":
                        return self._send(200, b"{}")
                    return self._send(200, json.dumps({"event_id": "abc123"}).encode())
                return self._send(404, b"{}")

        self.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.port = self.server.server_address[1]
        self.url = f"http://127.0.0.1:{self.port}"
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)

    def __enter__(self):
        self.thread.start()
        return self

    def __exit__(self, *exc):
        self.server.shutdown()
        self.server.server_close()


def unused_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]
