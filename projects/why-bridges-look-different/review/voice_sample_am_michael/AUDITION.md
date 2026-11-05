# Thử giọng Kokoro-82M

- Model: `hexgrad/Kokoro-82M` revision `f3ff3571791e…`, tham số speed 1.0, seed 0, lang_code a (af_/am_) or b (bf_/bm_). Sinh cục bộ, offline.
- Giọng có dấu ✗ ở cột "Dùng cho lời dẫn" chỉ để nghe thử: pipeline lời dẫn từ chối chúng, và quyền xuất bản ngày 2026-10-29 chưa áp dụng cho chúng.
- Đo lúc 2026-10-30T14:13:44Z bằng `tools/voice_audition.py`.
- Đoạn thử (lấy từ kịch bản pilot, có thuật ngữ kỹ thuật):
  - B04.s1: "The superstructure is the part that spans the gap, including the deck."
  - B10.s1: "It is built from wedge-shaped stones called voussoirs, with a keystone at the crown."
  - B13.s1: "While a stone arch is being built, a temporary timber frame called falsework holds the stones in place."
  - B26.s1: "Built of roughly twelve thousand granite blocks, it carries the railway over Gwynns Falls on an eighty foot arch."
  - B28.s2: "This timber trestle near Corinne, Utah, was built in 1872 by the Central Pacific Railroad."
  - B30.s1: "The Bollman truss, patented in 1852, was one of the first designs to use iron in all of its essential structural parts."

| Giọng | Giọng đọc | Dùng cho lời dẫn | VOICES.md (target / thời lượng huấn luyện / tổng) | Tốc độ (wpm) | WER lớn nhất | Chênh mức âm giữa các câu (dB) | File nghe |
|---|---|---|---|---|---|---|---|
| `am_michael` | American English, nam | ✓ | B / H hours / **C+** | 136.1 | 0.105 | 0.5 | `review/voice_sample_am_michael/am_michael.m4a` |

## ASR nghe được gì

- `am_michael`: "The superstructure is the part that spans the gap, including the deck." (WER 0.000) / "It is built from wedge-shaped stones called voossoirs with a keystone at the crown." (WER 0.067) / "While a stone arch is being built, a temporary timber frame called falsework holds the stones in place." (WER 0.000) / "Built of roughly 12,000 granite blocks, it carries the railway over Gwyn's Falls on an 80-foot arch." (WER 0.105) / "This timber trestle near Kareen, Utah, was built in 1872 by the Central Pacific Railroad." (WER 0.067) / "The Bauman Truss, patented in 1852, was one of the first designs to use iron in all of its essential structural parts." (WER 0.045)

## Kết luận kỹ thuật (không phải quyết định chọn giọng)

- Quy tắc xếp hạng (chỉ dựa trên số đo): VOICES.md overall grade, then max ASR WER, then |wpm - 160|, then level spread.
- Giọng mặc định kỹ thuật tạm thời (theo số đo): `am_michael`.
- **Người dùng đã chọn giọng kênh `am_michael` (2026-10-30).** Ghi trong `script/narration.json` → `voice.selection`.
- ASR chỉ chứng minh câu nghe rõ, không chứng minh giọng hay hay phát âm đúng. Thứ hạng không thay cho việc nghe bằng tai.
- Chọn giọng không phải là cấp quyền: `voice.license.status` và hạng quyền provider không đổi. Agent không tự chọn giọng thay người dùng.
- Quyền xuất bản của Kokoro là một bước riêng: `docs/licensing/KOKORO_LICENSE_AUDIT.md` (§5).
