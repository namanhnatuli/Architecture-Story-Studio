"""Download extra Kokoro-82M voice files at the pinned revision and check them against the
SHA256 prefixes published in that revision's VOICES.md (M7 voice audition).

Run with the Kokoro interpreter (it has huggingface_hub):
  ~/Work/Projects/Kokoro/.venv/bin/python tools/kokoro_fetch_voices.py af_heart am_michael ...
Prints {voice: {path, sha256, voices_md_prefix, match}} as JSON. Downloading a voice does not
make it usable for narration: integrations/tts/kokoro.py only accepts audited voices.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

from huggingface_hub import hf_hub_download

REPO, REV = "hexgrad/Kokoro-82M", "f3ff3571791e39611d31c381e3a41a3af07b4987"


def main(voices):
    table = Path(hf_hub_download(repo_id=REPO, filename="VOICES.md", revision=REV)).read_text(encoding="utf-8")
    out = {}
    for v in voices:
        m = re.search(r"\|\s*\**" + re.escape(v).replace("_", r"\\?_") + r"\**\s*\|.*`([0-9a-f]{8})`", table)
        path = hf_hub_download(repo_id=REPO, filename=f"voices/{v}.pt", revision=REV)
        digest = hashlib.sha256(Path(path).read_bytes()).hexdigest()
        prefix = m.group(1) if m else None
        out[v] = {"path": path, "sha256": digest, "voices_md_prefix": prefix,
                  "match": bool(prefix) and digest.startswith(prefix)}
    print(json.dumps(out, indent=1))
    return all(x["match"] for x in out.values())


if __name__ == "__main__":
    sys.exit(0 if main(sys.argv[1:]) else 1)
