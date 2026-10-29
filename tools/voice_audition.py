"""Kokoro voice audition (M6): the same narration passage in every audited British voice,
measured objectively, for a HUMAN listening decision.

  python3 tools/voice_audition.py --project bridge-load-explained

Writes review/voice_audition/<voice>.wav + .m4a (listening copies), metrics.json and
AUDITION.md. The agent ranks the voices on measured criteria only (VOICES.md grade, ASR
intelligibility, speaking rate, level consistency) and proposes a *provisional technical
default*; approving the channel voice is the user's decision, never recorded here.
"""
import argparse
import json
import re
import subprocess
import sys
import time
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from integrations import audio_probe  # noqa: E402
from integrations.tts import kokoro  # noqa: E402
from pipeline import asr_check  # noqa: E402
from pipeline.narration import join_wavs  # noqa: E402

PASSAGE = [("B2", 1), ("B5", 0), ("B6", 2)]   # technical terms: superstructure, thrust, chord
GRADE_ORDER = {g: k for k, g in enumerate(["A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "D-", "F"])}
TARGET_WPM = 160


def voices_md_rows():
    text = (kokoro.snapshot_dir() / "VOICES.md").read_text(encoding="utf-8")
    rows = {}
    for vid in kokoro.VOICE_SHA256:
        m = re.search(r"\|\s*" + vid + r"\s*\|[^|]*\|\s*([A-F][+-]?)\s*\|\s*([^|]+?)\s*\|\s*([A-F][+-]?)\s*\|", text)
        if m:
            rows[vid] = {"target_quality": m.group(1), "training_duration": m.group(2).replace("*", ""),
                         "overall_grade": m.group(3)}
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True)
    args = ap.parse_args()
    p = ROOT / "projects" / args.project
    narration = json.loads((p / "script/narration.json").read_text())
    beats = {b["id"]: b for b in narration["beats"]}
    sentences = [beats[b]["sentences"][k] for b, k in PASSAGE]
    out = p / "review" / "voice_audition"
    out.mkdir(parents=True, exist_ok=True)
    grades = voices_md_rows()
    worker = kokoro.KokoroWorker()
    rows = {}
    for vid in sorted(kokoro.VOICE_SHA256):
        errs = kokoro.verify_release(vid)
        if errs:
            raise SystemExit("; ".join(errs))
        items = [{"id": f"{vid}.s{k}", "text": s, "voice": vid, "speed": 1.0, "seed": 0,
                  "out": str(out / "parts" / f"{vid}.s{k}.wav")} for k, s in enumerate(sentences)]
        t0 = time.time()
        res = worker.run(items, "b")
        gen = time.time() - t0
        info = [audio_probe.validate_speech(i["out"], i["text"]) for i in items]
        joined = out / f"{vid}.wav"
        spans, total = join_wavs([i["out"] for i in items], narration["pacing"]["sentence_pause_seconds"], joined)
        subprocess.run([audio_probe._bin("ffmpeg"), "-y", "-loglevel", "error", "-i", str(joined), "-c:a", "aac",
                        "-b:a", "128k", str(out / f"{vid}.m4a")], check=True)
        heard = asr_check.transcribe([i["out"] for i in items])
        wers = [asr_check.wer(s, h["text"]) for s, h in zip(sentences, heard)]
        words = sum(len(s.split()) for s in sentences)
        speech = sum(r["duration"] for r in res)
        rows[vid] = {"voice_sha256": kokoro.VOICE_SHA256[vid], **grades.get(vid, {}),
                     "speech_seconds": round(speech, 3), "with_pauses_seconds": round(total, 3),
                     "wpm": round(words / speech * 60, 1),
                     "mean_db": [x["mean_db"] for x in info], "peak_db": [x["peak_db"] for x in info],
                     "level_spread_db": round(max(x["mean_db"] for x in info) - min(x["mean_db"] for x in info), 2),
                     "asr": [{"text": h["text"], "wer": round(w, 4)} for h, w in zip(heard, wers)],
                     "max_wer": round(max(wers), 4), "generation_seconds": round(gen, 2),
                     "files": {"wav": str(joined.relative_to(p)), "m4a": f"review/voice_audition/{vid}.m4a"}}
        print(f"{vid}: {rows[vid]['wpm']} wpm, max WER {rows[vid]['max_wer']}, spread {rows[vid]['level_spread_db']} dB, "
              f"grade {rows[vid].get('overall_grade')}")
    worker.close()

    def rank(v):
        r = rows[v]
        return (GRADE_ORDER.get(r.get("overall_grade"), 99), r["max_wer"], abs(r["wpm"] - TARGET_WPM),
                r["level_spread_db"], v)
    order = sorted(rows, key=rank)
    metrics = {"passage": [{"beat": b, "sentence": k, "text": s} for (b, k), s in zip(PASSAGE, sentences)],
               "params": {"speed": 1.0, "seed": 0, "lang_code": "b"}, "model_revision": kokoro.REVISION,
               "ranking_rule": "VOICES.md overall grade, then max ASR WER, then |wpm - 160|, then level spread",
               "ranking": order, "provisional_technical_default": order[0],
               "user_selection": narration["voice"].get("selection"), "voices": rows,
               "measured_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    (out / "metrics.json").write_text(json.dumps(metrics, indent=2, ensure_ascii=False) + "\n")
    write_md(out, metrics)
    print("WROTE", out / "AUDITION.md")


def write_md(out, m):
    lines = ["# Thử giọng Kokoro-82M (M6)", "",
             f"- Model: `hexgrad/Kokoro-82M` revision `{m['model_revision'][:12]}…`, tham số speed 1.0, seed 0, "
             "lang_code `b` (Anh–Anh). Sinh cục bộ, offline.",
             f"- Đo lúc {m['measured_utc']} bằng `tools/voice_audition.py`.",
             "- Đoạn thử (lấy từ kịch bản pilot, có thuật ngữ kỹ thuật):"]
    lines += [f"  - {x['beat']}.s{x['sentence']}: \"{x['text']}\"" for x in m["passage"]]
    lines += ["", "| Giọng | VOICES.md (target / thời lượng huấn luyện / tổng) | Tốc độ (wpm) | WER lớn nhất | "
              "Chênh mức âm giữa các câu (dB) | Mức trung bình (dB) | File nghe |", "|---|---|---|---|---|---|---|"]
    for v in m["ranking"]:
        r = m["voices"][v]
        lines.append(f"| `{v}` | {r.get('target_quality')} / {r.get('training_duration')} / **{r.get('overall_grade')}** | "
                     f"{r['wpm']} | {r['max_wer']:.3f} | {r['level_spread_db']} | "
                     f"{', '.join(str(x) for x in r['mean_db'])} | `{r['files']['m4a']}` |")
    lines += ["", "## ASR nghe được gì", ""]
    for v in m["ranking"]:
        lines.append(f"- `{v}`: " + " / ".join(f"\"{a['text']}\" (WER {a['wer']:.3f})" for a in m["voices"][v]["asr"]))
    lines += ["", "## Kết luận kỹ thuật (không phải quyết định chọn giọng)", "",
              f"- Quy tắc xếp hạng (chỉ dựa trên số đo): {m['ranking_rule']}.",
              f"- Giọng mặc định kỹ thuật tạm thời (theo số đo): `{m['provisional_technical_default']}`.",
              (f"- **Người dùng đã chọn giọng kênh `{m['user_selection']['voice']}` "
               f"({m['user_selection']['selected_on']}).** Ghi trong `script/narration.json` → `voice.selection`."
               if m.get("user_selection") else "- **Người dùng chưa chọn giọng kênh.**"),
              "- ASR chỉ chứng minh câu nghe rõ, không chứng minh giọng hay hay phát âm đúng. Thứ hạng không thay cho "
              "việc nghe bằng tai.",
              "- Chọn giọng không phải là cấp quyền: `voice.license.status` và hạng quyền provider không đổi. "
              "Agent không tự chọn giọng thay người dùng.",
              "- Quyền xuất bản của Kokoro là một bước riêng: `docs/licensing/KOKORO_LICENSE_AUDIT.md` (§5)."]
    (out / "AUDITION.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
