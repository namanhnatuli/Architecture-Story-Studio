# M5.5: production profile và gate theo mục đích

**Đủ điều kiện làm preview kỹ thuật không có nghĩa là được phép xuất bản.**

M5 dùng chung một bộ gate cho mọi dự án, mà bộ gate này được viết cho tập phim có lời dẫn (M3.5). Hệ quả là pilot không lời của M5 bị đánh FAIL ở G2/G3/G5 (không có audio) và G4 bị báo "stale" chỉ vì không có `script/timing.json`. M5.5 thêm một trường **bắt buộc khai báo rõ** trong `project.json` là `production_profile`. Profile quyết định gate nào áp dụng. Không có cờ bỏ qua chung nào.

## 1. Ba profile
| Profile | Mục đích | Bắt buộc | Không áp dụng | Kết luận cao nhất |
|---|---|---|---|---|
| `TECHNICAL_SILENT_PREVIEW` | Thử mô hình, template, kế hoạch hình ảnh, render | G0 (schema, asset); **GV** (visual plan hợp lệ, storyboard biên dịch từ đúng plan đó, báo cáo coverage còn hiện hành); G4 (QA Blender + media QA video không lời + không stale) | G2 (audio/TTS), G3 (khóa timing), G5 (lắp ghép, phụ đề): `NOT_APPLICABLE`, **không phải FAIL** | `TECHNICAL PREVIEW — VALID (silent); NOT FOR PUBLICATION`. G6 luôn `BLOCKED` |
| `NARRATED_INTERNAL_REVIEW` | Duyệt lời dẫn, đồng bộ audio, kể chuyện bằng hình | Toàn bộ gate M3.5 (không đổi): claim, timing đo được, audio, video, phụ đề, QA hình ảnh, ghi nhận quyền | — | `INTERNAL PREVIEW — …`. Kể cả khi mọi gate PASS, dự án **không** tự thành PUBLICATION_READY: phải chuyển sang PUBLICATION_CANDIDATE |
| `PUBLICATION_CANDIDATE` | Xét điều kiện phát hành YouTube | Mọi gate trên + G6 cuối: claim đã duyệt biên tập, quyền audio PUBLICATION_CLEARED, asset ngoài đã duyệt, script khóa, timing đo được, lắp ghép hợp lệ, QA nội dung + hình ảnh, **`publication_metadata`** (title, description, language, credits), visual plan hợp lệ (nếu có) | — | `PUBLICATION_READY` chỉ khi mọi điều kiện trên đạt |

Không khai báo profile thì mặc định là `NARRATED_INTERNAL_REVIEW` (đường gate nghiêm ngặt).

## 2. Chặn lạm dụng
- Validator (G0) từ chối profile lạ.
- Validator từ chối `TECHNICAL_SILENT_PREVIEW` nếu dự án có lời dẫn (`script/narration.json` hoặc `audio/`). Vì vậy không thể "tắt" gate audio của một tập phim có lời dẫn bằng cách đổi profile. Thử trên bản sao của Suffolk: G0 FAIL, không có TECHNICALLY_VALIDATED, kết luận NOT VALID (có test).
- Profile và `publication_metadata` không phải phụ thuộc render, nên đổi profile không làm render lại (có test).

## 3. Media QA cho video không lời (`tools/cli.py` `media_qa`, chạy trong `preview`)
Với mỗi MP4 (từng shot và toàn bộ), kiểm tra:
- số frame đúng như storyboard;
- độ phân giải bằng preset;
- fps, codec h264, yuv420p;
- thời lượng khớp với số frame;
- **đúng một luồng video và không có luồng audio**;
- **không có lỗi giải mã** (tính toàn vẹn của container và frame);
- không có đoạn đen;
- SSIM tại các cắt match.

Báo cáo ghi lại *video được render từ đâu*: ranh giới shot, `storyboard_sha256`, `plan_sha256` và khóa render-cache của từng shot.

**Stale được tính từ các phụ thuộc thật của profile.**
- Video không lời bị coi là stale khi tổng số frame đổi, hoặc khi khóa cache hiện tại của một shot khác khóa lúc encode.
- Một thay đổi thuần biên tập (lời giải thích, ghi chú) không làm stale.
- Gate của dự án có lời dẫn vẫn giữ luật M3.5: theo timing đã khóa.

Không bao giờ tạo một file timing audio giả cho dự án không lời.

## 4. Kết quả
| Dự án | Profile | Trạng thái | Kết luận |
|---|---|---|---|
| bridge-story-m5 | TECHNICAL_SILENT_PREVIEW | TECHNICALLY_VALIDATED · EDITORIAL_REVIEW_PENDING (G0/GV/G4 PASS; G2/G3/G5 NOT_APPLICABLE; G6 BLOCKED) | TECHNICAL PREVIEW — VALID (silent); NOT FOR PUBLICATION |
| suffolk-roofs | NARRATED_INTERNAL_REVIEW | TECHNICALLY_VALIDATED · EDITORIAL_REVIEW_PENDING · TTS_RIGHTS_PENDING (**không đổi**) | INTERNAL PREVIEW — NOT PUBLICATION-READY |
| roof-plan-m5, roof-evolution, bridge-structure-evolution | TECHNICAL_SILENT_PREVIEW | TECHNICALLY_VALIDATED (roof-evolution, bridge-structure-evolution thêm EDITORIAL_REVIEW_PENDING) | VALID (silent); NOT FOR PUBLICATION, sau khi render lại bằng engine M5.5. Trước đó video cũ được báo stale một cách đúng đắn |
