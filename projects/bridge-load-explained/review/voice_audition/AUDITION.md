# Thử giọng Kokoro-82M (M6)

- Model: `hexgrad/Kokoro-82M` revision `f3ff3571791e…`, tham số speed 1.0, seed 0, lang_code `b` (Anh–Anh). Sinh cục bộ, offline.
- Đo lúc 2026-10-29T04:56:48Z bằng `tools/voice_audition.py`.
- Đoạn thử (lấy từ kịch bản pilot, có thuật ngữ kỹ thuật):
  - B2.s1: "The deck is carried by the superstructure, the part of the bridge that spans the gap."
  - B5.s0: "The curve turns the downward load into thrust along the arch, pressing the stones together."
  - B6.s2: "Each span here is a simple span, so under a downward load its top chord is squeezed and its bottom chord is stretched."

| Giọng | VOICES.md (target / thời lượng huấn luyện / tổng) | Tốc độ (wpm) | WER lớn nhất | Chênh mức âm giữa các câu (dB) | Mức trung bình (dB) | File nghe |
|---|---|---|---|---|---|---|
| `bf_emma` | B / HH hours / **B-** | 182.5 | 0.087 | 0.2 | -24.1, -24.3, -24.1 | `review/voice_audition/bf_emma.m4a` |
| `bm_george` | B / MM minutes / **C** | 161.0 | 0.087 | 0.1 | -24.8, -24.7, -24.7 | `review/voice_audition/bm_george.m4a` |
| `bm_fable` | B / MM minutes / **C** | 180.3 | 0.087 | 0.4 | -27.0, -27.1, -27.4 | `review/voice_audition/bm_fable.m4a` |
| `bm_daniel` | C / MM minutes / **D** | 185.1 | 0.087 | 0.2 | -24.6, -24.6, -24.4 | `review/voice_audition/bm_daniel.m4a` |

## ASR nghe được gì

- `bf_emma`: "The deck is carried by the superstructure, the part of the bridge that spans the gap." (WER 0.000) / "The curve turns the downward load into thrust along the arch, pressing the stones together." (WER 0.000) / "Each span here is a simple span, so under a downward load its top cord is squeezed and its bottom cord is stretched." (WER 0.087)
- `bm_george`: "The deck is carried by the superstructure, the part of the bridge that spans the gap." (WER 0.000) / "The curve turns the downward load into thrust along the arch, pressing the stones together." (WER 0.000) / "Each span here is a simple span, so under a downward load, its top cord is squeezed and its bottom cord is stretched." (WER 0.087)
- `bm_fable`: "The deck is carried by the superstructure, the part of the bridge that spans the gap." (WER 0.000) / "The curve turns the downward load into thrust along the arch, pressing the stones together." (WER 0.000) / "Each span here is a simple span, so under a downward load its top cord is squeezed and its bottom cord is stretched." (WER 0.087)
- `bm_daniel`: "The deck is carried by the superstructure, the part of the bridge that spans the gap." (WER 0.000) / "The curve turns the downward load into thrust along the arch, pressing the stones together." (WER 0.000) / "Each span here is a simple span, so under a downward load its top cord is squeezed and its bottom cord is stretched." (WER 0.087)

## Kết luận kỹ thuật (không phải quyết định chọn giọng)

- Quy tắc xếp hạng (chỉ dựa trên số đo): VOICES.md overall grade, then max ASR WER, then |wpm - 160|, then level spread.
- Giọng mặc định kỹ thuật tạm thời trước khi người dùng chọn: `bf_emma`.
- **Người dùng đã chọn giọng kênh `bm_george` (2026-10-29).** Ghi trong `script/narration.json` → `voice.selection`. Lời dẫn pilot đã được sinh lại bằng giọng này (143.4 wpm cho toàn bài).
- ASR chỉ chứng minh câu nghe rõ, không chứng minh giọng hay hay phát âm đúng. Thứ hạng không thay cho việc nghe bằng tai.
- Chọn giọng không phải là cấp quyền: `voice.license.status` vẫn là `LICENSE_REVIEW_REQUIRED`, provider vẫn là `PENDING_REVIEW`.
- Quyền xuất bản của Kokoro là một bước riêng: `docs/licensing/KOKORO_LICENSE_AUDIT.md` (§5).
