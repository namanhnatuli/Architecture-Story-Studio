"""Transcribe WAV files with a locally cached Whisper model (offline).

Runs in an *external* Python that has transformers/torch (by default OmniVoice's
venv); Architecture Story Studio itself stays stdlib-only. Never downloads:
HF_HUB_OFFLINE=1 is set by the caller.

Usage: <python> tools/asr_whisper.py <model-id> <wav> [<wav> ...]  -> JSON on stdout
"""
import json
import sys
import warnings

warnings.filterwarnings("ignore")


def main():
    import soundfile as sf
    import torch
    from transformers import pipeline

    model_id, paths = sys.argv[1], sys.argv[2:]
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    asr = pipeline("automatic-speech-recognition", model=model_id, device=device, torch_dtype=torch.float16)
    results = []
    for path in paths:
        audio, sr = sf.read(path, dtype="float32")
        out = asr({"raw": audio, "sampling_rate": sr}, generate_kwargs={"task": "transcribe"}, return_language=True)
        chunks = out.get("chunks") or []
        language = chunks[0].get("language") if chunks else out.get("language")
        results.append({"path": path, "text": out["text"].strip(), "language": language})
    print("ASR_JSON " + json.dumps(results))


if __name__ == "__main__":
    main()
