"""Speech-only pronunciation overrides (stdlib only).

script/pronunciation.json maps a *written* word (kept as-is in narration,
subtitles, citations and metadata) to a provider-specific *spoken* form that is
sent to TTS only, e.g. "Babergh" -> OmniVoice "[B EY1 B AH0]" (CMU phones).

Rules:
- whole-word, case-sensitive replacement of listed words only (no global place-name rewriting);
- providers without a listed form get the written text unchanged;
- ASR checks map `asr_aliases` back to the written word, because Whisper cannot
  spell a pronunciation. An ASR pass is therefore NOT evidence that the
  pronunciation is right: an entry is only `CONFIRMED` after a named person
  listened to the evidence clips (status/confirmed_by), which the publication gate requires.
"""
import json
import re
from pathlib import Path

STATUSES = ("PENDING_LISTENING_REVIEW", "CONFIRMED", "REJECTED")


def load(project_dir):
    path = Path(project_dir) / "script" / "pronunciation.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {"entries": []}


def _pattern(word):
    return re.compile(r"(?<![\w-])" + re.escape(word) + r"(?![\w-])")


def spoken_text(text, lexicon, provider):
    """(text sent to TTS, ids of applied entries). Written text is never modified."""
    applied = []
    for entry in (lexicon or {}).get("entries", []):
        form = (entry.get("speech") or {}).get(provider)
        if not form or entry.get("status") == "REJECTED":
            continue
        new = _pattern(entry["written"]).sub(form, text)
        if new != text:
            applied.append(entry["id"])
            text = new
    return text, applied


def asr_aliases(lexicon):
    """{normalised alias word: normalised written word} for the WER check."""
    out = {}
    for entry in (lexicon or {}).get("entries", []):
        for alias in entry.get("asr_aliases", []):
            out[alias.lower()] = entry["written"].lower()
    return out


def validate(lexicon):
    errors, ids = [], set()
    for entry in (lexicon or {}).get("entries", []):
        eid = entry.get("id")
        if not eid or eid in ids:
            errors.append(f"pronunciation: id missing or duplicated: {eid!r}")
        ids.add(eid)
        if not entry.get("written") or not entry.get("speech"):
            errors.append(f"pronunciation {eid}: needs `written` and provider `speech` forms")
        if entry.get("status") not in STATUSES:
            errors.append(f"pronunciation {eid}: status must be one of {STATUSES}")
        if entry.get("status") == "CONFIRMED" and not (entry.get("confirmed_by") and entry.get("confirmed_on")):
            errors.append(f"pronunciation {eid}: CONFIRMED needs confirmed_by/confirmed_on (a human listener)")
        for provider, form in (entry.get("speech") or {}).items():
            if provider == "omnivoice" and form.startswith("[") and not re.fullmatch(r"\[[A-Z]+[012]?( [A-Z]+[012]?)*\]", form):
                errors.append(f"pronunciation {eid}: OmniVoice CMU form must be uppercase phones in brackets, got {form!r}")
    return errors


def used_entries(narration, lexicon, provider):
    """Entries that change at least one narrated sentence for this provider."""
    used = set()
    for beat in narration.get("beats", []):
        for sentence in beat.get("sentences", []):
            used.update(spoken_text(sentence, lexicon, provider)[1])
    return sorted(used)
