"""Write concept/VISUAL_STORYBOARD.md from the script and the audio lock (stdlib only).

    python3 projects/floating-city-design-challenge/concept/build_storyboard.py

One shot per beat (SHnn = Bnn) at the script-review stage. Narration and claims come from script/narration.json and
script/visual_beats.json (written by script/story.py); durations from script/timing.json once `lock-audio` has run
(otherwise from words at 2.3 words per second, marked "est."). The visual fields below are the Studio's plan for each
shot; feasibility classes follow the concept brief (section 15).
"""
import json
import re
from pathlib import Path

P = Path(__file__).resolve().parents[1]
FAM = {"A": "môi trường biển", "B": "phao", "C": "mối nối", "D": "neo", "E": "nhà", "F": "hạ tầng", "K": "card 2D"}
R, AD, GP, NEW, EXT = "REUSE_EXISTING", "ADAPT_EXISTING", "GENERATE_PROCEDURAL", "CREATE_SMALL_NEW_CAPABILITY", "EXTERNAL_DEPENDENCY_REQUIRED"

# beat: (viewer question, family, camera, animation, what it reveals, annotation, render cost, confidence, limitation, class)
SHOTS = {
    "B01": ("Đây là gì?", "A,B,E,F", "Aerial cao, đẩy chậm", "HOLD + PUSH_IN", "Lời hứa: một thành phố", "NOTE 'Illustrative design'", "H", "H", "Cảnh lớn; cần instancing", GP),
    "B02": ("Thiết kế được không?", "A,B,E,F", "Aerial, tiếp B01", "HOLD", "Bài toán được đặt ra", "—", "H", "H", "Dùng chung cảnh B01", R),
    "B03": ("Đã có ai làm chưa?", "K", "2D", "CARD theo từ", "Ranh giới đã xây và đề xuất", "'built' / 'proposed 2022' / 'status checked Nov 2026: OCEANIX news page, BIG project page'", "L", "M", "Ảnh Schoonschip chờ quyết định giấy phép; tạm dùng sơ đồ", R),
    "B04": ("Thành phố gồm những gì?", "A–F", "Three-quarter, lùi nhẹ", "SEQUENCE: FADE_OUT theo nhóm", "Thành phố là chồng hệ thống", "tên từng hệ khi nó biến mất", "H", "H", "—", GP),
    "B05": ("Bê tông nổi được à?", "A,B", "Mặt cắt ngang", "SIDE_BY_SIDE; REVEAL", "Hình dạng quyết định", "'same volume of concrete'", "M", "H", "Không hoạt ảnh 'chìm dần'", GP),
    "B06": ("Vì sao nổi?", "A,B,E", "Mặt cắt chính diện (prototype P1)", "HOLD_HIGHLIGHT", "Khối nước bị chiếm chỗ", "'displaced water'", "M", "H", "Cần tham số mặt cắt", NEW),
    "B07": ("Ngoài đời thì sao?", "K", "2D", "CARD", "Cỡ người thật", "'two builders' figures: 340–350 t'", "L", "H", "Sơ đồ, chưa có ảnh", R),
    "B08": ("Cái gì nặng nhất?", "B,E", "Three-quarter", "EXPLODE + thanh 2D", "Bất ngờ: thân phao hơn nửa", "'illustrative'", "M", "H", "—", GP),
    "B09": ("Thêm tải thì sao?", "B,E", "Cận thước mớn nước (P2b, P6)", "REPLACE + SINK (mới)", "Tải làm phao chìm", "thước 1 m; mạn khô 1,04 → 0,71 m", "M", "H", "33 cm không thấy ở khung rộng (P2)", NEW),
    "B10": ("Sửa thế nào?", "B", "Cùng camera B09", "REVEAL phần thân thêm + RISE (mới)", "Lần sửa có lý do", "mạn khô 0,71 → 1,15 m; '+4% concrete'", "M", "H", "Cùng nhánh với B09 (một tải)", NEW),
    "B11": ("Có lật không?", "B", "Ngang, three-quarter thấp", "HOLD + nghiêng nhỏ (TILT, mới)", "Nghiêng ít ≠ đứng yên trong sóng", "'illustrative'", "L", "H", "Không ký hiệu G, B, M", NEW),
    "B12": ("Nhân bản được không?", "B,E", "Three-quarter", "ASSEMBLE_IN", "Khu hình thành", "—", "M", "H", "—", GP),
    "B13": ("Sao không nối cứng?", "B,C,E", "Mặt đứng", "HIGHLIGHT_REPLACE_HIGHLIGHT", "Chênh cao độ → cầu có khớp (một lựa chọn)", "'floating independently'", "M", "H", "Không tô đỏ, không vẽ gãy", GP),
    "B14": ("Mối nối trông ra sao?", "C,F", "Cận", "CLOSEUP_HIGHLIGHT", "Khe, cầu có khớp, đường hạ tầng mềm", "'conceptual geometry'", "M", "H", "Không chọn cơ cấu cụ thể", GP),
    "B15": ("Bao nhiêu phao?", "K", "2D mặt bằng", "CARD, chấm hiện dần", "Quy mô mối nối", "'illustrative'; 40 m² = 30 + 10", "L", "H", "—", R),
    "B16": ("To hay nhiều?", "K", "2D mặt bằng cùng tỉ lệ", "CARD", "Đánh đổi; chọn 60 m", "khối lượng mỗi phao; 'not an optimum'", "L", "H", "—", R),
    "B17": ("Sóng thì sao?", "A,B,C", "Three-quarter thấp", "CONCEPT_MOTION (mới)", "Khe co giãn", "'Conceptual motion visualization — not a hydrodynamic simulation'", "M", "M", "Biên độ không mang nghĩa", NEW),
    "B18": ("Người ở có thấy?", "K,E", "2D + cận nhà", "CARD", "Chuyển động là chuyện con người", "nguồn: Yale E360, 2021", "L", "H", "—", R),
    "B19": ("Phao lớn thì sao?", "K", "2D mặt cắt", "CARD, đường cong vẽ dần", "Bài toán mở", "'exaggerated, conceptual'", "L", "M", "Không có số", R),
    "B20": ("Giảm sóng thế nào?", "K", "2D bản đồ sơ đồ", "CARD", "Địa điểm là thiết kế", "'limited fetch'", "L", "H", "Không gắn địa danh thật", R),
    "B21": ("Bố cục ra sao?", "A–F", "Top → three-quarter", "SEQUENCE", "Tổ chức theo chuyển động", "'reduces waves — does not remove storm risk'", "H", "H", "—", GP),
    "B22": ("Cái gì giữ nó?", "A,D", "Three-quarter thấp (P4)", "SEQUENCE: nước 2 bước, HIGHLIGHT cọc", "Hệ neo vô hình", "—", "H", "H", "Phải thấy mặt nước trước khi mờ", AD),
    "B23": ("Triều lên thì sao?", "B,D,F", "Mặt đứng", "SEQUENCE + RISE/SINK (mới)", "Vì sao cầu có khớp", "'2 m range, assumed'", "M", "H", "—", NEW),
    "B24": ("Xa bờ hơn?", "A,D", "Dưới nước, ngang", "REPLACE (cọc → dây)", "Neo theo độ sâu", "'Conceptual mooring — not sized'", "H", "H", "Độ võng dây chỉ là hình vẽ; tương phản dây (P5)", GP),
    "B25": ("Đã là thành phố chưa?", "E,F", "Three-quarter", "SEQUENCE: GHOST nhà", "Nửa còn lại của thành phố", "—", "H", "H", "—", GP),
    "B26": ("Tự cung tự cấp?", "K", "2D", "CARD", "'Floating ≠ off-grid'", "—", "L", "H", "—", R),
    "B27": ("Nước thải đi đâu?", "F", "Cận một phao", "CLOSEUP_HIGHLIGHT", "Phụ thuộc vào bờ", "—", "M", "H", "—", GP),
    "B28": ("Cấp cứu, đi lại?", "F", "Three-quarter", "SEQUENCE: HIGHLIGHT 3 mục", "Mọi dịch vụ nối bờ", "—", "H", "H", "Không khẳng định đạt quy chuẩn", GP),
    "B29": ("Ra khơi được không?", "A,B", "3D biển mở, aerial thấp", "HOLD", "Bắt đầu phản thực tế", "'Counterfactual'", "M", "H", "Site biển mở mới", GP),
    "B30": ("Đê và neo còn đủ?", "A,D", "Cùng cảnh, xuống dưới nước", "SEQUENCE + CONCEPT_MOTION (sóng dài)", "Sóng dài; dây dài ra", "nhãn chuyển động khái niệm", "H", "H", "—", NEW),
    "B31": ("Còn nối bờ được?", "F", "Cùng cảnh", "HOLD_HIGHLIGHT", "Liên kết dài và lộ hơn", "—", "M", "H", "—", GP),
    "B32": ("Nếu phải tự chủ?", "K", "2D", "CARD", "Một điều kiện thêm, không mặc định", "'one concept study's estimate'", "L", "H", "—", R),
    "B33": ("Thiết kế khác ra sao?", "B", "3D cạnh nhau", "SIDE_BY_SIDE", "Một loại thân khác", "'concept study (2026)'", "M", "H", "Biến thể phao bán chìm (sơ đồ)", GP),
    "B34": ("Bảo trì?", "B", "Cận thân phao", "CLOSEUP_HIGHLIGHT", "Chi phí ẩn", "'no dedicated standards yet'", "L", "H", "Không vẽ hư hỏng", GP),
    "B35": ("Sinh thái?", "A", "Dưới nước", "HOLD (bóng EEVEE)", "Tác động vô hình", "—", "M", "M", "Không mô phỏng ánh sáng", AD),
    "B36": ("Ai dùng mặt nước?", "E,F", "Three-quarter", "SIDE_BY_SIDE 2 biến thể", "Câu hỏi phi kỹ thuật", "—", "M", "H", "—", GP),
    "B37": ("Bao nhiêu tiền?", "K", "2D", "CARD 2 cột", "Kết luận cân bằng", "'no reliable cost estimate for this design'", "L", "H", "—", R),
    "B38": ("Đi được bao xa?", "A–F", "DETAIL_THEN_OVERVIEW", "SIDE_BY_SIDE + nhãn", "So sánh cuối", "mỗi hệ một nhãn", "H", "H", "Phao 40 m cạnh quận khoảng 600 m: cần khung cận trước", GP),
    "B39": ("Kết luận 1?", "K", "2D", "CARD theo từ", "Đã có thật", "—", "L", "H", "—", R),
    "B40": ("Kết luận 2?", "K", "2D", "CARD theo từ", "Có thể, có điều kiện", "'checked: OCEANIX Busan, Nov 2026'", "L", "H", "—", R),
    "B41": ("Kết luận 3?", "K", "2D", "CARD theo từ", "Còn suy đoán", "—", "L", "H", "—", R),
    "B42": ("Phép tính chứng minh gì?", "A–F", "Aerial (dùng lại B01)", "HOLD + PUSH_IN", "Giới hạn của phép tính", "—", "H", "H", "Dùng lại cảnh B01", R),
    "B43": ("—", "K", "2D", "CARD icon tự vẽ", "Lời kêu gọi", "—", "L", "H", "—", R),
    "B44": ("—", "K", "2D", "CARD", "Ghi công, công bố giọng AI", "—", "L", "H", "—", R),
}


def main():
    vb = json.loads((P / "script" / "visual_beats.json").read_text())
    ch = json.loads((P / "script" / "chapters.json").read_text())
    tpath = P / "script" / "timing.json"
    durations, source = {}, "est."
    if tpath.is_file():
        t = json.loads(tpath.read_text())
        pace = t.get("pacing", {})
        pad = pace.get("beat_lead_in_seconds", 0) + pace.get("beat_tail_seconds", 0)
        durations = {b["id"]: b["duration"] + pad for b in t.get("beats", []) if "duration" in b}
        source = "audio"
    beats = {b["beat_id"]: b for b in vb["beats"]}
    missing = sorted(set(beats) ^ set(SHOTS))
    if missing:
        raise SystemExit(f"storyboard and script disagree on beats: {missing}")
    rows = ["# Storyboard sơ bộ (revision c-r1)", "",
            "Sinh bởi `concept/build_storyboard.py` từ `script/visual_beats.json` (`script/story.py`) và "
            + ("`script/timing.json` (thời lượng đo từ audio)." if source == "audio" else "ước lượng 2,3 từ mỗi giây (chưa có audio).")
            + " Một shot cho mỗi beat ở giai đoạn đọc kịch bản (SHnn = Bnn). Sửa ở `story.py` hoặc bảng `SHOTS` trong script này, "
              "rồi chạy lại; không sửa tay tệp này.", "",
            "**Cột:**",
            "- **Fam** là họ asset: " + ", ".join(f"{k} {v}" for k, v in FAM.items()) + ".",
            "- **Cplx** là chi phí render (L/M/H); **Conf** là độ tin cậy của nội dung (H/M).",
            "- **Hạng** là hạng khả thi theo brief mục 15.", ""]
    total, by_class, d2, d3 = 0.0, {}, 0.0, 0.0
    for c in ch["chapters"]:
        rows += [f"## {c['id']}: {c['title']}", "",
                 "| Shot | Lời dẫn (rút gọn) | Câu hỏi | Claim | Fam | Camera | Hoạt ảnh | Lộ ra | Chú thích | Dài | Cplx | Conf | Giới hạn | Hạng |",
                 "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
        for bid in c["beat_ids"]:
            b = beats[bid]
            q, fam, cam, anim, rev, ann, cplx, conf, lim, cls = SHOTS[bid]
            words = len(b["narration"].split())
            dur = durations.get(bid, words / 2.3)
            total += dur
            by_class[cls] = by_class.get(cls, 0) + 1
            if fam == "K":
                d2 += dur
            else:
                d3 += dur
            text = b["narration"]
            short = text if len(text) <= 110 else text[:107].rsplit(" ", 1)[0] + "…"
            claims = ", ".join(x.replace("CLM_", "") for x in b.get("claim_ids", [])) or "—"
            rows.append(f"| SH{bid[1:]} | {short} | {q} | {claims} | {fam} | {cam} | {anim} | {rev} | {ann} | "
                        f"{dur:.0f} s{'' if source == 'audio' else ' est.'} | {cplx} | {conf} | {lim} | {cls} |")
        rows.append("")
    m, s = divmod(int(round(total)), 60)
    rows += ["## Tổng", "",
             f"- **Thời lượng:** {m}:{s:02d} ({'đo từ audio, gồm khoảng lặng đầu và cuối mỗi beat' if source == 'audio' else 'ước lượng'}).",
             f"- **3D:** {d3:.0f} s ({100 * d3 / total:.0f}%); **2D:** {d2:.0f} s ({100 * d2 / total:.0f}%).",
             "- **Theo hạng khả thi:** " + "; ".join(f"{k} {v}" for k, v in sorted(by_class.items())) + ".",
             "- **Chuỗi card 2D liền nhau dài nhất:** " + longest_card_run(ch, beats) + ".",
             "- **Aerial:** chỉ B01–B02 và B42 (dùng lại cùng cảnh).", ""]
    (P / "concept" / "VISUAL_STORYBOARD.md").write_text("\n".join(rows) + "\n", encoding="utf-8")
    print(f"WROTE concept/VISUAL_STORYBOARD.md: {len(beats)} shots, {m}:{s:02d} ({source}); {by_class}")


def longest_card_run(ch, beats):
    order = [bid for c in ch["chapters"] for bid in c["beat_ids"]]
    best, run, start, best_start = 0, 0, None, None
    for bid in order:
        if SHOTS[bid][1] == "K":
            run += 1
            start = start or bid
            if run > best:
                best, best_start, best_end = run, start, bid
        else:
            run, start = 0, None
    return f"{best} ({best_start}–{best_end})" if best else "0"


if __name__ == "__main__":
    main()
