# Đánh giá sẵn sàng cho M4 (cuối M3.5, 2026-10-27)

**Kết luận: sẵn sàng về kỹ thuật, nhưng chưa nên bắt đầu M4 sản xuất video phát hành** cho đến khi xong 3 việc của con người (B1–B3). Agent **không** tự bắt đầu M4.

## Đã sẵn sàng
| Năng lực | Bằng chứng |
|---|---|
| Pipeline narration-first có cache audio tách theo hạng quyền | `pipeline/narration.py`, `audio_manifest.py` v2; 9/14 take được giữ qua lần sửa lời dẫn |
| Đổi provider TTS mà không viết lại scheduler | `integrations/tts/providers.py` (OmniVoice và giọng người thật); test chặn publication |
| Duyệt biên tập có hồ sơ, gắn với revision | gói duyệt, validator `editorial_approval` |
| Phụ đề căn theo audio thật | `pipeline/subtitles.py`, `qa/SUBTITLE_QA.md` (21 cue, dòng tối đa 41 ký tự) |
| Cache render đúng phụ thuộc | `tools/render_cache.py`, `cache-report` |
| QA Blender bắt được lỗi xuyên mái và nhãn bị che | 70/70 (suffolk), 63/63 (roof-evolution); có phép thử ngược |
| Gate tách trạng thái | `pipeline/gates.py` |

## Chặn (việc của con người)
- **B1. Duyệt biên tập:** 7 claim + câu chữ B1/B6 + chữ trên màn hình (`projects/suffolk-roofs/review/EDITORIAL_APPROVAL_PACKAGE.md`).
- **B2. Chọn đường lời dẫn để xuất bản:** Kokoro (cục bộ, Apache-2.0, cần nghe thử và xác nhận dữ liệu huấn luyện), Azure/Polly (trả phí, SSML IPA), hoặc giọng người thật. Xem `docs/licensing/TTS_LICENSE_AUDIT.md` §6.
- **B3. Nghe xác nhận phát âm "Babergh"** (`qa/pronunciation/PRONUNCIATION_TEST.md`).

## Rủi ro kỹ thuật còn lại (đưa vào backlog M4)
1. Provider xuất bản mới sẽ cho thời lượng khác → mọi shot được lên lịch và render lại; thời gian render preview khoảng 10 phút/75 s ở 640×360. Video 8–15 phút cần ước lượng chi phí render (lệnh `render-plan` trong kế hoạch M3).
2. Timestamp theo từ của Whisper là xấp xỉ (DTW). Ranh giới đã được đặt lại theo năng lượng audio, nhưng với giọng người thật nên kiểm tra lại `SUBTITLE_QA.md`.
3. Tốc độ đọc phụ đề có 7 cảnh báo (17–19.8 ký tự/giây) do tốc độ đọc lời dẫn khoảng 170 từ/phút. Nếu chọn giọng đọc chậm hơn, cảnh báo sẽ giảm.
4. Chưa kiểm tra trên Blender 4.5 LTS; chưa có nhạc nền hay hiệu ứng âm thanh; chưa có tiêu đề/end card.
5. Tiêu đề project rộng hơn bằng chứng (xem gói duyệt §3).
6. Kích thước viên ngói/slate là minh họa đã cường điệu (có ghi rõ trong gói duyệt §6).

## Đề xuất phạm vi M4 (để người dùng quyết định)
- **M4a:** tích hợp provider xuất bản đã chọn (adapter + test giả lập + clearance), rồi tạo lại pilot Suffolk để có bản đầu tiên `PUBLICATION_READY` ở 1080p.
- **M4b:** mở rộng sang video dài (8–15 phút): ước lượng chi phí render, render song song theo shot, thêm template nếu cần (TIMELINE/CUTAWAY trong backlog).
