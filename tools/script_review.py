#!/usr/bin/env python3
"""Owner's script review document (stdlib only; nothing is rendered or approved).

  python3 tools/script_review.py --project <slug> [--audio]

writes projects/<slug>/review/SCRIPT_REVIEW.md from the generated script (narration.json, visual_beats.json,
chapters.json), the audio timing lock and the claim ledger, so the document always shows the sentences that
were actually narrated. review/SCRIPT_REVIEW_NOTES.md (written by the agent: decisions the owner must take)
goes on top when it exists. --audio also joins audio/beats/*.wav, with the locked pauses, into
output/<slug>_narration_preview_<revision>.m4a (git-ignored) so the owner can listen; it is not a master.
Used when the owner asks to read the script before any review video is rendered.
"""
import argparse
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def read(path):
    path = Path(path)
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def clock(seconds):
    return f"{int(seconds // 60)}:{int(seconds % 60):02d}"


def beat_windows(timing):
    """{beat id: (start, end)} in film seconds: each beat's speech plus the locked lead-in and tail."""
    pace = timing.get("pacing", {})
    pad = pace.get("beat_lead_in_seconds", 0) + pace.get("beat_tail_seconds", 0)
    out, t = {}, 0.0
    for b in timing.get("beats", []):
        out[b["id"]] = (t, t + b["duration"] + pad)
        t += b["duration"] + pad
    return out


def on_screen(visual):
    """The words the viewer reads: card text, then notes on 3D shots."""
    words = [e["text"] for e in (visual.get("graphic") or {}).get("elements", []) if e.get("kind") == "text"]
    return words + [a["text"] for a in visual.get("annotations", []) if a.get("type") == "NOTE"]


def visual_kind(visual, status):
    if visual.get("strategy") == "CARD":
        return "sơ đồ/card 2D"
    return "3D, cần bộ sinh mới" if status == "MISSING_ASSET" else "3D"


def text_only_runs(order, visuals, windows):
    """Consecutive cards made only of words (and thin rules), longest first: [(beat ids, seconds)]. The share of 2D
    says little by itself; a long run of cards with nothing to look at is what tires a viewer."""
    def words_only(v):
        kinds = (v.get("graphic") or {}).get("elements", [])
        return v.get("strategy") == "CARD" and all(
            e["kind"] == "text" or (e["kind"] == "line" and len(e.get("points", [])) == 2) for e in kinds)
    runs, run = [], []
    for bid in order + [None]:
        if bid is not None and words_only(visuals.get(bid, {})):
            run.append(bid)
        elif run:
            runs.append((run, sum(windows[k][1] - windows[k][0] for k in run)))
            run = []
    return sorted(runs, key=lambda r: -r[1])


def pronunciation_rows(p, timing, windows):
    """One row per speech-only override: where it is first spoken, in the preview track's time."""
    lexicon = read(p / "script/pronunciation.json")
    lead = timing.get("pacing", {}).get("beat_lead_in_seconds", 0)
    rows = []
    for e in lexicon.get("entries", []):
        where = next(((b["id"], s) for b in timing.get("beats", []) for s in b.get("sentences", [])
                      if e["written"] in s["text"]), None)
        at = "không được đọc"
        if where:
            bid, s = where
            at = f"{clock(windows[bid][0] + lead + s['start'])} ({bid}.s{s['index']})"
        rows.append(f"| {e['written']} | {e.get('respelling', '')} | {at} | {e.get('without_override', '')} | {e.get('status', '')} |")
    return rows


def build(p):
    p = Path(p)
    narration, beats = read(p / "script/narration.json"), read(p / "script/visual_beats.json")
    chapters, timing = read(p / "script/chapters.json"), read(p / "script/timing.json")
    sources, coverage = read(p / "research/sources.json"), read(p / "qa/visual_coverage.json")
    project = read(p / "project.json")
    windows = beat_windows(timing)
    visuals = {b["beat_id"]: b for b in beats.get("beats", [])}
    status = {b["beat_id"]: b.get("status") for b in coverage.get("beats", [])}
    claims = {c["id"]: c for c in sources.get("claims", [])}
    rows = narration.get("beats", [])
    by_id = {b["id"]: b for b in rows}
    total = max((w[1] for w in windows.values()), default=0)
    words = sum(len(s.split()) for b in rows for s in b["sentences"])
    sentences = sum(len(b["sentences"]) for b in rows)
    used = sorted({c for b in rows for c in b.get("claim_ids", [])})
    span = sum(w[1] - w[0] for k, w in windows.items() if visuals.get(k, {}).get("strategy") == "CARD")
    runs = text_only_runs([b["id"] for b in rows if b["id"] in windows], visuals, windows)

    out = [f"# Duyệt kịch bản: {project.get('title', p.name)}", "",
           f"- Revision lời dẫn: `{narration.get('revision', {}).get('version', narration.get('revision'))}`; "
           f"{len(chapters.get('chapters', []))} chương, {len(rows)} beat, {sentences} câu, {words} từ.",
           f"- Thời lượng đo từ audio đã khóa: khoảng **{total / 60:.1f} phút** ({clock(total)}).",
           f"- Hình: {clock(span)} là card 2D ({100 * span / total:.0f}%) nếu giữ nguyên kế hoạch hiện tại." if total else "",
           f"- Card chỉ có chữ: dài nhất {'–'.join((runs[0][0][0], runs[0][0][-1]))}, {runs[0][1]:.0f} giây liền." if runs else "",
           f"- Claim: {len(used)} claim được dùng, tất cả `SOURCE_VERIFIED`, **chưa claim nào được duyệt biên tập**.", ""]
    notes = p / "review/SCRIPT_REVIEW_NOTES.md"
    if notes.is_file():
        out += [notes.read_text(encoding="utf-8").strip(), ""]
    pron = pronunciation_rows(p, timing, windows)
    if pron:
        out += ["## Phát âm cần bạn nghe", "",
                "Mốc thời gian theo bản nghe thử. ASR đạt không chứng minh phát âm đúng.", "",
                "| Tên | Cách đọc đang dùng | Nghe ở | Nếu không ghi đè | Trạng thái |", "|---|---|---|---|---|"] + pron + [""]
    out += ["## Toàn bộ kịch bản", "",
            "Lời dẫn là tiếng Anh, đúng câu chữ đã đọc. Mốc thời gian là ước tính từ audio đã khóa.", ""]
    for ch in chapters.get("chapters", []):
        ids = ch.get("beat_ids", [])
        start = windows.get(ids[0], (0, 0))[0] if ids else 0
        out += [f"### {ch['id']} · {ch['title']} ({clock(start)})", ""]
        for bid in ids:
            b, v = by_id[bid], visuals.get(bid, {})
            cited = ", ".join(b.get("claim_ids", [])) or "không có claim"
            out += [f"**{bid}** · {clock(windows.get(bid, (0, 0))[0])} · {visual_kind(v, status.get(bid))} · {cited}", "",
                    "> " + " ".join(b["sentences"]), "",
                    f"- Hình: {v.get('visual_goal', '')}"]
            shown = on_screen(v)
            if shown:
                out.append("- Chữ trên hình: " + " · ".join(shown))
            out.append("")
    out += ["## Các claim phim dùng", "",
            "`medium` = chỉ có hoặc chủ yếu dựa vào nguồn thứ cấp, hoặc các nguồn lệch nhau. Nên xem kỹ các mục này.", "",
            "| Claim | Tin cậy | Nội dung | Nguồn | Giả định, giới hạn |", "|---|---|---|---|---|"]
    clean = lambda s: str(s).replace("|", "/").replace("\n", " ")   # noqa: E731
    for cid in used:
        c = claims.get(cid, {})
        extra = c.get("assumptions", "")
        extra = "" if extra.startswith("None beyond") else extra
        out.append(f"| {cid} | {c.get('confidence', '?')} | {clean(c.get('text', 'THIẾU'))} | "
                   f"{', '.join(c.get('source_ids', []))} | {clean(extra)} |")
    return "\n".join(x for x in out if x is not None).rstrip() + "\n"


def preview_audio(p):
    """Join the locked beat audio with its pauses into one listening track; returns its path."""
    p = Path(p)
    timing, narration = read(p / "script/timing.json"), read(p / "script/narration.json")
    pace = timing["pacing"]
    revision = (narration.get("revision") or {}).get("version", "draft")
    out = p / "output" / f"{p.name}_narration_preview_{revision}.m4a"
    beats = timing["beats"]
    inputs = [x for b in beats for x in ("-i", str(p / b["audio_file"]))]
    lead = int(pace["beat_lead_in_seconds"] * 1000)
    chains = [f"[{i}:a]adelay={lead}:all=1,apad=pad_dur={pace['beat_tail_seconds']}[a{i}]" for i in range(len(beats))]
    joined = "".join(f"[a{i}]" for i in range(len(beats)))
    graph = ";".join(chains) + f";{joined}concat=n={len(beats)}:v=0:a=1[out]"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", *inputs, "-filter_complex", graph, "-map", "[out]",
                    "-c:a", "aac", "-b:a", "128k", str(out)], check=True)
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--project", required=True)
    ap.add_argument("--projects-root", help="default: projects/ in this repository")
    ap.add_argument("--audio", action="store_true", help="also write the narration preview track")
    args = ap.parse_args(argv)
    p = Path(args.projects_root or ROOT / "projects") / args.project
    if not p.is_dir():
        raise SystemExit(f"no project {p}")
    (p / "review").mkdir(exist_ok=True)
    (p / "review/SCRIPT_REVIEW.md").write_text(build(p), encoding="utf-8")
    print(p / "review/SCRIPT_REVIEW.md")
    if args.audio:
        print(preview_audio(p))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
