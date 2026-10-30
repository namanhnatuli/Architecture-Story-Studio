#!/usr/bin/env python3
"""Pronunciation evidence for a lexicon entry: the same narrator voice says the word
in several spoken forms; clips + Whisper transcripts + a listening checklist go to
projects/<slug>/qa/pronunciation/. ASR output is indicative only; a person must
listen and record the decision in script/pronunciation.json (status/confirmed_by).

    python3 tools/pronunciation_test.py --project <slug> --entry PRON_001 --beat <beat id>

Built for the M3 OmniVoice pilot (suffolk-roofs, now a test fixture); the active films use
Kokoro and tools/longform_reports.py for their pronunciation review.
"""
import argparse
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from integrations.tts import providers  # noqa: E402
from pipeline import asr_check, narration as nar, pronunciation as pron  # noqa: E402
from pipeline.audio_manifest import AudioManifest  # noqa: E402


def variants_for(entry, sentence):
    """(id, description, spoken sentence) — baseline is the written word as the TTS reads it by default."""
    w = entry["written"]
    forms = [("V1_cmu", f"CMU phones {entry['speech']['omnivoice']}", entry["speech"]["omnivoice"])]
    forms += [(f"V{i}_respell", f"respelling {r!r}", r) for i, r in enumerate(entry.get("test_respellings", []), 2)]
    out = [(vid, desc, sentence.replace(w, form)) for vid, desc, form in forms]
    # Phones alone produce no audio in OmniVoice 0.1.5 (tested 2026-10-27), so the short test is a phrase.
    out += [(vid + "_phrase", desc + " (short phrase)", f"{form} District.") for vid, desc, form in forms[:1]]
    return out


def run(project, entry_id, beat_id, index, log=print):
    p = ROOT / "projects" / project
    narration = nar.load(p)
    lexicon = pron.load(p)
    entry = next(e for e in lexicon["entries"] if e["id"] == entry_id)
    sentence = next(b for b in narration["beats"] if b["id"] == beat_id)["sentences"][index]
    out_dir = p / "qa" / "pronunciation"
    out_dir.mkdir(parents=True, exist_ok=True)
    rights = providers.check_purpose(narration["voice"]["provider"], "internal_preview")
    adapter = providers.make_adapter(narration["voice"]["provider"])
    manifest = AudioManifest(p)

    if not (p / narration["voice"]["reference"]["audio"]).is_file():
        raise SystemExit("run `narrate` first: the narrator reference clip is needed")
    voice = nar.voice_spec(narration, p)  # same synthetic narrator voice as the narration
    params = adapter.params(narration["voice"])
    clips = []
    # Baseline: the M3 take (written word read by default), copied — never regenerated.
    m3 = next((r for r in manifest.data["segments"].values()
               if r.get("role") == "sentence" and r.get("beat_id") == beat_id and r.get("sentence_index") == index
               and r.get("spoken_text", r.get("text")) == sentence), None)
    if m3:
        dst = out_dir / f"{entry_id}_V0_baseline_m3.wav"
        shutil.copyfile(p / m3["file"], dst)
        clips.append({"id": "V0_baseline_m3", "description": "M3 take: written spelling read by default (no override)",
                      "spoken": sentence, "file": dst.name})
    for vid, desc, spoken in variants_for(entry, sentence):
        dst = out_dir / f"{entry_id}_{vid}.wav"
        result = adapter.synthesize(spoken, voice, dst, params, f"{entry_id}_{vid}", p)
        log(f"GENERATED {vid}: {result.duration:.2f}s  {spoken!r}")
        clips.append({"id": vid, "description": desc, "spoken": spoken, "file": dst.name,
                      "duration": result.duration})
    heard = asr_check.transcribe([out_dir / c["file"] for c in clips])
    for c, h in zip(clips, heard):
        c["asr_text"] = h["text"]
    report = {"entry": entry_id, "written": entry["written"], "target_ipa": entry["ipa"],
              "target_respelling": entry["respelling"], "sentence": sentence, "provider": adapter.name,
              "model_revision": adapter.model_revision, "rights_class": rights,
              "generated_utc": datetime.now(timezone.utc).isoformat(), "clips": clips,
              "asr_model": "openai/whisper-large-v3-turbo",
              "asr_caveat": "Whisper writes the nearest English spelling; it cannot confirm a pronunciation."}
    (out_dir / f"{entry_id}_report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    return report


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True)
    ap.add_argument("--entry", default="PRON_001")
    ap.add_argument("--beat", default="B1")
    ap.add_argument("--index", type=int, default=0)
    a = ap.parse_args()
    report = run(a.project, a.entry, a.beat, a.index)
    for c in report["clips"]:
        print(f"{c['id']:>16}: heard {c['asr_text']!r}")


if __name__ == "__main__":
    main()
