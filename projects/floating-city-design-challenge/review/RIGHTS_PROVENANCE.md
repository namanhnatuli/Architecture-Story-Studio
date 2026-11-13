# Bản kê quyền và nguồn gốc: floating-city-design-challenge (narration c-r2, bản final 4K)

- **Ngày lập:** 2026-11-13, sau bản final 4K (`review/FINAL_4K.md`).
- **Người lập:** agent. Đây là bản kê, **không phải tư vấn pháp lý**.
- Phim này trước đây chưa có bản kê. Các thông tin dưới đây lấy từ hồ sơ của dự án.
- **Trạng thái duyệt:** theo `review/OWNER_APPROVALS.json`. Chủ kênh chưa duyệt bản mô tả YouTube đã sửa, và chưa ghi việc đăng phim.

| Thành phần | Nguồn gốc | Quyền / license | Trạng thái |
|---|---|---|---|
| Lời dẫn (126 câu, 44 beat) | Sinh cục bộ bằng Kokoro-82M (`hexgrad/Kokoro-82M` @ `f3ff3571`), giọng `am_michael`, `lang_code='a'`, speed 1.0, seed 0 | Apache-2.0. Kiểm toán ở `docs/licensing/KOKORO_LICENSE_AUDIT.md`; mục 5 còn những điểm mở mà chủ kênh đã chấp nhận | Chủ kênh duyệt giọng cho phim này (APP-VOICE, 2026-11-08). ASR đạt 126/126 |
| Phát âm | Không có mục ghi đè. Danh sách thuật ngữ cần nghe ở `review/PRONUNCIATION_REVIEW.md` | Của dự án | Chủ kênh chấp nhận audio hiện tại, kể cả "Schoonschip" (APP-PRONUNCIATION). Không ghi buổi nghe từng mục nào |
| Kịch bản | Agent viết từ các claim đã đối chiếu (`research/sources.json`: 16 nguồn, 64 claim, phim dùng 50) | Của dự án | 50 claim EDITORIALLY_APPROVED (APP-CLAIMS); 14 claim chỉ dùng cho nghiên cứu |
| Số liệu thiết kế | Tính toán ở mức concept của Studio (`analysis/RESULTS.md`, `concept/SCENARIO_CONTRACT.md`) | Của dự án | Ghi là ước tính của Studio, không phải thiết kế kỹ thuật được chứng nhận. Nói rõ trên hình và trong mô tả |
| Mô hình 3D, site vịnh, sơ đồ | Sinh thủ tục trong dự án (họ asset `floating`, site `bay`; `engine/`, `asset_library/`) | `generated_in_project` | Minh họa. Chuyển động của nước và các nền nổi là minh họa khái niệm, không phải mô phỏng thủy động lực học; có ghi chú trên hình |
| Ảnh chụp, bản vẽ của bên thứ ba | **Không có**. Schoonschip chỉ có sơ đồ do Studio vẽ; không dùng ảnh chụp công trình | — | — |
| Footage | **Không có** | — | — |
| Watermark kênh | `branding/concepts_20261107/A_watermark_burnin_640.png` (sha256 ghi trong `config/branding.json`) | Của kênh | Đốt vào hình ở góc dưới trái, rộng 14%, độ đậm 55% |
| Chữ trên hình | Font `<builtin>` của Blender | Như các phim trước: OFL-1.1 / Bitstream Vera | Chưa xác định file font cụ thể đứng sau `<builtin>` |
| Phụ đề (SRT + track mov_text) | Chép nguyên văn lời dẫn; thời điểm theo khoảng câu đã đo | Của dự án | 181 cue |
| Hiệu ứng âm thanh | 6 file từ Pixabay, chủ kênh tự tải; agent chọn từng đoạn bằng số đo. Trang nguồn, tác giả, ngày kiểm và sha256 ghi trong `audio/sound_plan.json` | Pixabay Content License: dùng trong video được, không bắt buộc ghi công, không được phân phối lại file đứng riêng. Vì vậy `sfx/pixabay/` không vào git | Chủ kênh duyệt SFX như FULL_V3 (APP-SOUND-FINAL). Agent không nghe được |
| Nhạc | **Không có** | — | — |
| ASR (chỉ dùng cho QA) | `openai/whisper-large-v3-turbo` cục bộ | MIT | Không nằm trong video |

## Mô tả YouTube
- Theo yêu cầu của chủ kênh (DEC-DESCRIPTION-CREDITS, 2026-11-13), mô tả **không ghi** dòng về lời dẫn hay dòng về SFX.
- **Giấy phép không bị ảnh hưởng:** Apache-2.0 không đòi ghi công cho audio sinh ra, và Pixabay Content License không bắt buộc ghi công.
- **Điều kiện duyệt giọng không còn áp cho phim này:** lần duyệt giọng (APP-VOICE) có điều kiện "nêu lời dẫn do AI tạo trong mô tả". Quyết định trên của chủ kênh bỏ điều kiện đó cho phim này.
- **Phần còn lại là việc của chủ kênh khi đăng:** cài đặt "nội dung đã chỉnh sửa hoặc tổng hợp" trên YouTube, và kiểm lại chính sách YouTube lúc đăng (mục 5, điểm 3 của bản kiểm toán).
