"""M7 long-form review documents, generated from the project files (stdlib only):

  review/EVIDENCE_MATRIX.md             claim -> sources/locators -> sentences -> on-screen use
  review/EDITORIAL_APPROVAL_PACKAGE.md  everything the owner must approve, sentence by sentence
  review/YOUTUBE_DESCRIPTION.md         DRAFT description: chapters (timestamps), sources, credits
  qa/VISUAL_VARIETY.md                  visual kinds per chapter, runs, shot lengths

  python3 tools/longform_reports.py --project why-bridges-look-different [--preset review]

Nothing here approves anything: statuses are copied from the records, never raised."""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from pipeline import chapters as CH  # noqa: E402


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def tc(seconds):
    s = int(seconds)
    return f"{s // 60}:{s % 60:02d}"


def _load(p):
    return {"sources": read(p / "research/sources.json"), "narration": read(p / "script/narration.json"),
            "beats": read(p / "script/visual_beats.json"), "timing": read(p / "script/timing.json"),
            "story": read(p / "storyboard/storyboard.json"), "assets": read(p / "assets/manifest.json"),
            "chapters": read(CH.path(p))}


def sentence_times(d):
    """{"B03.s1": (start, end)} in film seconds."""
    out = {}
    for b in d["timing"]["beats"]:
        base = b["start_seconds"] - b["sentences"][0]["rel_start"] if b["sentences"] else b["start_seconds"]
        for s in b["sentences"]:
            out[f"{b['id']}.s{s['index']}"] = (base + s["rel_start"], base + s["rel_end"])
    return out


def on_screen(d):
    """claim id -> on-screen uses (annotation ids with text; card element texts of beats citing it)."""
    uses = {}
    for b in d["beats"]["beats"]:
        for a in b.get("annotations", []):
            if a.get("claim_id"):
                uses.setdefault(a["claim_id"], []).append(f"{a['id']} ({a['type']}{': ' + a['text'] if a.get('text') else ''})")
    return uses


def evidence_matrix(p, d):
    claims = d["sources"]["claims"]
    used = {}
    for b in d["narration"]["beats"]:
        for c in b["claim_ids"]:
            used.setdefault(c, []).append(b["id"])
    screen = on_screen(d)
    lines = ["# Ma trận bằng chứng: Why Bridges Don't All Look the Same (M7)", "",
             "Sinh tự động bởi `tools/longform_reports.py` từ `research/sources.json`, `script/narration.json` và "
             "`script/visual_beats.json`. Mọi trích dẫn đã được khớp nguyên văn với văn bản nguồn tải về "
             "(`research/build_sources.py`). **Chưa claim nào được duyệt biên tập.**", "",
             f"- Nguồn: {len(d['sources']['sources'])}. Claim: {len(claims)}. Claim được lời dẫn dùng: {len(used)}.", "",
             "| Claim | Nội dung (tiếng Anh, như trong registry) | Nguồn · vị trí | Beat dùng | Trên màn hình | Trạng thái |",
             "|---|---|---|---|---|---|"]
    for c in claims:
        where = "; ".join(f"{e['source_id']} · {e['locator']}" for e in c["evidence"])
        lines.append(f"| {c['id']} | {c['text']} | {where} | {', '.join(used.get(c['id'], [])) or '— (không dùng)'} | "
                     f"{'; '.join(screen.get(c['id'], [])) or '—'} | {c['review_status']} |")
    lines += ["", "## Nguồn", ""]
    for s in d["sources"]["sources"]:
        lines.append(f"- **{s['id']}**: {s['title']}. {s.get('publisher', '')}. {s.get('edition', '')}. {s.get('url', '')} "
                     f"(truy cập {s.get('accessed', '?')}). {s.get('verification', '')}")
    out = p / "review" / "EVIDENCE_MATRIX.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out


CHECKLIST = [
    "Lời dẫn: mỗi câu đúng với claim nó trích (xem cột trích dẫn nguồn).",
    "Chữ trên card: tiêu đề, nhãn, chú thích ảnh, thang nhịp và dòng thời gian.",
    "Ảnh lưu trữ: chọn ảnh, cách cắt viền phim, dòng ghi công (xem `review/RIGHTS_PROVENANCE.md`).",
    "Nhãn 'Illustrative model' trên các mô hình 3D đứng cạnh cầu có thật (B27, B29).",
    "Phát âm các tên mới (narration.voice.pronunciation_review.terms).",
    "Giọng: xác nhận quyết định cấp quyền Kokoro / bm_george ngày 2026-10-29 cũng áp dụng cho phim này "
    "(narration.voice.license.owner_confirmation_for_this_film = PENDING).",
]


def editorial_package(p, d):
    claims = {c["id"]: c for c in d["sources"]["claims"]}
    times = sentence_times(d)
    rev = d["narration"].get("revision") or {}
    lines = ["# Gói duyệt biên tập: \"Why Bridges Don't All Look the Same\" (M7, narration "
             f"`{rev.get('version')}`)", "",
             "> **Đang chờ duyệt.** Agent soạn gói này nhưng không tự duyệt claim, giọng hay phát âm. "
             "Tới khi chủ kênh duyệt, mọi bản dựng mang nhãn INTERNAL REVIEW.", "",
             "## Cần chủ kênh quyết định", ""]
    lines += [f"{i}. {x}" for i, x in enumerate(CHECKLIST, 1)]
    lines += ["", "Cách ghi quyết định giống M6: `research/sources.json` → `review_status: EDITORIALLY_APPROVED` + "
              "`editorial_approval {approved_by, approved_on, narration_revision}`; `project.json` → "
              "`factual_review: verified`; `narration.voice.pronunciation_review.status: CONFIRMED`.", "",
              "## Các điểm cần lưu ý (agent tự nêu)", "",
              "- Năm xây cầu Bollman ở Savage **không** được nói, vì các nguồn không thống nhất (ASCE chỉ chắc chắn về "
              "bằng sáng chế 1852; các hồ sơ khác ghi khoảng 1869). Phim chỉ nói 'patented in 1852'.",
              "- 'world's oldest stone railroad span still in service' được gán cho báo cáo năm 2005 ('A national report in "
              "2005 called it…'), không khẳng định cho hiện tại.",
              "- 'America's greatest stone arch' là lời của báo cáo NCHRP, được gán rõ ('What one report calls…').",
              "- Địa danh trong chú thích ảnh (Covington, Virginia; Corinne, Utah; Savage, Maryland) lấy từ tiêu đề hồ sơ "
              "HAER/LOC của chính bức ảnh.",
              "- Không có con số về nội lực, sức chịu tải, ứng suất, độ võng hay hệ số an toàn. Các nhịp (30 ft, 220 ft, "
              "gần 400 ft) là giá trị NCHRP nêu, vẽ đúng tỉ lệ với nhau.",
              "- Đánh dấu nén/kéo cụ thể chỉ có ở biên trên/biên dưới giàn đơn giản dưới tải hướng xuống (CLM_713); "
              "thanh bụng không được tô màu nén/kéo (CLM_714 chỉ nói 'một số').",
              "- Không trình bày ba loại cầu như một chuỗi tiến bộ: B02, B19, B33 nói rõ điều ngược lại.", "",
              "## Lời dẫn theo câu", ""]
    beats_by_chapter = {c["id"]: c for c in d["chapters"]["chapters"]}
    owner = {b: c for c in d["chapters"]["chapters"] for b in c["beat_ids"]}
    current = None
    for b in d["narration"]["beats"]:
        if owner[b["id"]]["id"] != current:
            current = owner[b["id"]]["id"]
            lines += ["", f"### {current} · {beats_by_chapter[current]['title']}", ""]
        lines.append(f"**{b['id']}** ({b['kind']}; claim: {', '.join(b['claim_ids']) or 'không, câu dẫn dắt'})")
        lines.append("")
        for i, s in enumerate(b["sentences"]):
            t0, _ = times.get(f"{b['id']}.s{i}", (0, 0))
            lines.append(f"- `{tc(t0)}` {s}")
        for cid in b["claim_ids"]:
            c = claims[cid]
            ex = " · ".join(f"{e['source_id']} {e['locator']}: \"{e['excerpt']}\"" for e in c["evidence"])
            lines.append(f"  - {cid}: {ex}" + (f" — giả định: {c['assumptions']}"
                                               if c.get("assumptions") and not c["assumptions"].startswith("None") else ""))
        lines.append("")
    plan = read(p / "storyboard/visual_plan.json")
    unsure = [r for r in (plan.get("consistency") or {}).get("rows", []) if r["verdict"] != "CONSISTENT"]
    lines += ["## Bộ kiểm nhất quán lời/hình: cần người duyệt xác nhận", ""]
    lines += [f"- {r['beat_id']}.s{r['sentence']} ({r['rule']}, {r['verdict']}): \"{r['text']}\" — {r['detail']}"
              for r in unsure] or ["- Không có."]
    lines += ["", "## Chữ trên card", ""]
    for s in d["story"]["shots"]:
        texts = [e["text"] for e in (s.get("graphic") or {}).get("elements", []) if e.get("kind") == "text"]
        if texts:
            lines.append(f"- **{s['id']}** ({', '.join(s['beat_ids'])}): " + " | ".join(texts))
    lines += ["", "## Chú thích trên cảnh 3D", ""]
    for b in d["beats"]["beats"]:
        for a in b.get("annotations", []):
            if a.get("text"):
                lines.append(f"- {b['beat_id']} `{a['id']}` {a['type']}: \"{a['text']}\"" +
                             (f" ({a['claim_id']})" if a.get("claim_id") else ""))
    lines += ["", "## Bản ghi sửa câu (ASR / tốc độ đọc)", ""]
    for e in rev.get("edits", []):
        lines.append(f"- {e['sentence']}: \"{e['draft']}\" → \"{e['m7-r1']}\" ({e['why']})")
    out = p / "review" / "EDITORIAL_APPROVAL_PACKAGE.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out


def youtube_description(p, d, manifest):
    sources = d["sources"]["sources"]
    photos = [a for a in d["assets"]["assets"] if a.get("origin") == "external"]
    lines = ["<!-- DRAFT: not for publication until the editorial approval package is approved. -->", "",
             f"# {d['narration']['title']}", "",
             "Why does one bridge rest on rows of timber posts, another leap the gap in stone curves, and a third "
             "become a lattice of iron or steel triangles? This documentary explains how beam, arch and truss bridges "
             "carry load, and how materials, sites, spans, budgets and builders shaped the bridges people built.", "",
             "Chapters", ""]
    for c in manifest["chapters"]:
        lines.append(f"{tc(c['start_seconds'])} {c['title']}")
    lines += ["", "Sources", ""]
    for s in sources:
        if not s["id"].startswith("SRC_HAER"):
            lines.append(f"- {s['title']}, {s.get('publisher', '')}" + (f" ({s['edition']})" if s.get("edition") else "")
                         + f". {s.get('url', '')}")
    lines += ["", "Archival photographs", ""]
    for a in photos:
        lines.append(f"- {a.get('title') or a['id']}: {a['attribution']}. {a['license']}. Original record: "
                     f"{a.get('original_record') or a['source_url']}")
    lines += ["", "Credits and disclosures", "",
              "- Narration: AI-generated voice (Kokoro-82M, Apache-2.0; voice bm_george).",
              "- 3D models and diagrams are illustrative visualisations made for this video, not engineering designs "
              "or reconstructions of the bridges shown in the photographs.",
              "- Force arrows show concepts, not calculated forces. No load capacities, stresses or safety factors are given.",
              "- Historic American Engineering Record (HAER), National Park Service; Library of Congress Prints & "
              "Photographs Division. Photographs are public-domain works of the U.S. Government.", ""]
    out = p / "review" / "YOUTUBE_DESCRIPTION.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out


def visual_variety(p, d, manifest, rows):
    shots = {s["id"]: s for s in d["story"]["shots"]}
    kinds = [CH.visual_kind(s) for s in d["story"]["shots"]]
    total = sum(s["duration_seconds"] for s in d["story"]["shots"])
    by_kind = {}
    for s, k in zip(d["story"]["shots"], kinds):
        by_kind[k] = by_kind.get(k, 0.0) + s["duration_seconds"]
    lines = ["# Kiểm tra đa dạng hình ảnh (M7)", "",
             "Sinh tự động bởi `tools/longform_reports.py`. Đây là số liệu cấu trúc; phần nhận xét của người xem nằm trong "
             "`qa/EDITORIAL_REVIEW_TIMECODED.md`.", "",
             f"- {len(shots)} shot, {total:.1f} s. Shot dài nhất {max(s['duration_seconds'] for s in shots.values()):.1f} s; "
             f"trung bình {total / len(shots):.1f} s.", "",
             "| Loại hình | Số shot | Thời lượng | Tỉ lệ |", "|---|---|---|---|"]
    for k in sorted(by_kind, key=lambda k: -by_kind[k]):
        lines.append(f"| {k} | {kinds.count(k)} | {by_kind[k]:.1f} s | {100 * by_kind[k] / total:.0f}% |")
    two_d = [k in ("PHOTO", "DIAGRAM", "TITLE") for k in kinds]
    run, best, t, best_t, start = 0, 0, 0.0, 0.0, None
    for flag, s in zip(two_d, d["story"]["shots"]):
        run, t = (run + 1, t + s["duration_seconds"]) if flag else (0, 0.0)
        if t > best_t:
            best, best_t, start = run, t, s["id"]
    lines += ["", f"- Đoạn 2D liên tục dài nhất: {best} shot, {best_t:.1f} s (kết thúc ở {start}).", "",
              "## Theo chương", "", "| Chương | Bắt đầu | Dài | Shot | Loại hình |", "|---|---|---|---|---|"]
    for c in manifest["chapters"]:
        lines.append(f"| {c['id']} {c['title']} | {tc(c['start_seconds'])} | {c['duration_seconds']:.0f} s | "
                     f"{len(c['shots'])} | {', '.join(f'{k} ×{n}' for k, n in c['visual_kinds'].items())} |")
    lines += ["", "## Từng shot", "", "| Shot | Beat | Loại | Dài | Cắt |", "|---|---|---|---|---|"]
    for s, k in zip(d["story"]["shots"], kinds):
        lines.append(f"| {s['id']} | {', '.join(s['beat_ids'])} | {k} | {s['duration_seconds']:.1f} s | "
                     f"{s.get('cut_from_previous', 'match')} |")
    plan = read(p / "storyboard/visual_plan.json")
    templates = {}
    for ps in plan["shots"]:
        templates[ps["template"]] = templates.get(ps["template"], 0) + 1
    moves = [s["id"] for s in d["story"]["shots"] if (s.get("animation") or {}).get("camera_move")]
    dense, t0 = [], 0.0
    for s in d["story"]["shots"]:
        appear = sorted(a["appear"] for a in (s.get("annotations") or {}).get("items", []) if a.get("type") != "TAG")
        for i in range(len(appear) - 2):
            if appear[i + 2] - appear[i] <= 1.5:
                dense.append(f"{s['id']} @{tc(t0 + appear[i])}")
                break
        t0 += s["duration_seconds"]
    small = []
    for ps in plan["shots"]:
        for t in (ps.get("visibility") or {}).get("targets", []):
            if t.get("shown") and (t.get("visible_area", 1.0) < 0.004 or t.get("visible_share", 1.0) < 0.35):
                small.append(f"{ps['shot_id']} {t['concept']} (visible area {t.get('visible_area', 0):.4f}, "
                             f"share {t.get('visible_share', 0):.2f})")
    vs = plan.get("visibility_summary") or {}
    lines += ["", "## Lặp lại, mật độ và kích thước mục tiêu", "",
              "- Template theo số shot: " + ", ".join(f"{k} ×{n}" for k, n in sorted(templates.items(), key=lambda x: -x[1])),
              f"- Push-in: {len(moves)} shot ({', '.join(moves)}), mỗi cái cách nhau ít nhất một chương, trừ B27/B29 "
              "(hai mô hình minh họa đứng cạnh ảnh thật).",
              "- Cụm chú thích dày (≥ 3 chú thích hiện trong 1,5 s): " + (", ".join(dense) or "không có"),
              "- Mục tiêu nhỏ hoặc bị che nhiều (diện tích thấy < 0,4% khung hoặc thấy < 35%): " + ("; ".join(small) or "không có"),
              f"- Tầm nhìn (planner L1): {vs.get('rows_passing')}/{vs.get('target_rows')} dòng mục tiêu đạt, "
              f"{vs.get('auto_repaired')} tự sửa, {vs.get('manual_review')} cần xem tay."]
    lines += ["", "## Kiểm tra phim dài (pipeline/chapters.py)", ""]
    lines += [f"- {r['status']} `{r['check']}`: {r['detail']}" for r in rows]
    out = p / "qa" / "VISUAL_VARIETY.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out


def pronunciation_review(p, d):
    """review/PRONUNCIATION_REVIEW.md: where each new term is spoken, its audio file, the phonemes
    Kokoro used and what ASR heard - for the owner to listen to (nothing is confirmed here)."""
    import re
    manifest = read(p / "audio/narration_manifest.json")
    times = sentence_times(d)
    pr = d["narration"]["voice"].get("pronunciation_review") or {}
    lines = ["# Nghe lại phát âm (M7)", "",
             f"Trạng thái: **{pr.get('status', 'PENDING')}**. Agent không xác nhận phát âm. Chủ kênh nghe các đoạn dưới "
             "đây rồi ghi `narration.voice.pronunciation_review.status: CONFIRMED` (kèm `confirmed_by`, `confirmed_on`), "
             "hoặc ghi chữ cần đọc khác.", "",
             "| Thuật ngữ | Câu | Mốc trong phim | File audio | Âm vị Kokoro (cả câu) | ASR nghe thấy từ này? |",
             "|---|---|---|---|---|---|"]
    for term in pr.get("terms", []):
        pat = re.compile(r"\b" + re.escape(term.lower()), re.I)
        found = False
        for b in d["narration"]["beats"]:
            for i, t in enumerate(b["sentences"]):
                if not pat.search(t):
                    continue
                key = manifest["beats"][b["id"]]["sentences"][i]["cache_key"]
                seg = manifest["segments"][key]
                heard = (seg.get("asr") or {}).get("text", "")
                lines.append(f"| {term} | {b['id']}.s{i} | {tc(times[f'{b['id']}.s{i}'][0])} | `{seg['file']}` | "
                             f"`{seg.get('phonemes', '')}` | {'có' if pat.search(heard) else 'KHÔNG: ' + heard} |")
                found = True
                break
            if found:
                break
        if not found:
            lines.append(f"| {term} | — | — | — | — | không có trong lời dẫn |")
    out = p / "review" / "PRONUNCIATION_REVIEW.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True)
    ap.add_argument("--preset", default="review")
    args = ap.parse_args()
    p = ROOT / "projects" / args.project
    d = _load(p)
    rows, manifest = CH.longform_qa(p, args.preset)
    (p / "review").mkdir(exist_ok=True)
    for out in (evidence_matrix(p, d), editorial_package(p, d), youtube_description(p, d, manifest),
                visual_variety(p, d, manifest, rows), pronunciation_review(p, d)):
        print("WROTE:", out)


if __name__ == "__main__":
    main()
