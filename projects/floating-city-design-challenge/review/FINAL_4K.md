# Bản cuối 4K (2026-11-13)

**Đầu vào:**
- Chủ kênh: "tôi duyệt bản này, hãy render bản final 4k" (2026-11-12).
- Câu trả lời của chủ kênh cho bốn câu hỏi của agent, ghi trong `review/OWNER_APPROVALS.json`:
  - **Hình:** hình FULL v3, giữ nguyên cả 6 điểm (`APP-PICTURE-FINAL`);
  - **Âm thanh:** có SFX như FULL_V3 (`APP-SOUND-FINAL`);
  - **Lời kêu gọi cuối phim:** đã duyệt (`APP-CTA`);
  - **Mô tả YouTube:** chủ kênh muốn sửa, nên **chưa duyệt**.

## File
| File | Nội dung |
|---|---|
| `output/floating_city_design_challenge_FINAL_4K_2160p.mp4` | 3840×2160, 24 fps, H.264 High (CRF 16, x264 slow), BT.709; AAC mono 48 kHz; 784,167 s (13:04,2), 18 820 frame; có watermark; 424 MB |
| `output/floating_city_design_challenge_FINAL_4K_2160p.en.srt` | 181 cue, giống hệt phụ đề FULL_V3 |
| `output/floating_city_design_challenge_audio_master_final_4k.wav` | âm thanh cuối, có SFX, đã chuẩn hóa |
| `output/floating_city_design_challenge_narration_master_clean_final_4k.wav` | chỉ lời dẫn, không SFX, để làm lại âm thanh nếu cần |
| `output/floating_city_design_challenge_FINAL_4K_2160p.sha256` | sha256 của 4 file trên |

- **sha256 của MP4:** `1e25fc2523538fe942f778b8f6d4e69eb7de160e36761d900b2fa52645aaaa19`.
- Các file này nằm ngoài git (`projects/*/output/**`).

## Render
- **Cách render:** theo từng chương (`chapter --preset final_4k --release-frames`), mỗi lúc một Blender, máy không ngủ (`caffeinate`).
- **Thời gian:** 19:47 → 03:57, tức 8 giờ 10 phút cho 44/44 shot. Ghép xong lúc 04:03.
- Giờ xong của từng chương ở `qa/perf/final_4k_wall.txt`.
- PNG của từng chương đã xóa sau khi bản trung gian của chương được kiểm. Đĩa còn 69 GB.

## QA
- **Gate cuối trước khi render** (`final-gate`): PASS.
  - Cảnh báo về 14 claim SOURCE_VERIFIED chỉ áp cho các claim nghiên cứu mà phim không dùng (đã kiểm bằng `used_claim_ids`).
  - Cả 50 claim phim dùng đều EDITORIALLY_APPROVED.
- **Âm thanh:**
  - **Bản trộn trước chuẩn hóa:** giống từng mẫu với bản FULL_V3 chủ kênh đã duyệt (18 820 000 mẫu, 0 mẫu khác).
  - **Track chỉ có lời dẫn:** giống từng mẫu với bản `_no_sfx` của FULL_V3.
  - **SFX:** 11 tiếng và 2 đoạn nền nước, đúng các mốc trong `qa/EDITORIAL_REVIEW_TIMECODED.md`; 0 mẫu bị cắt.
  - **Mức:** −16,4 LUFS, đỉnh thật −1,4 dBTP.
- **Hình:**
  - SSIM giữa bản 4K (thu về 720p) và FULL_V3, lấy 1 frame mỗi giây (784 frame): thấp nhất 0,970, trung bình 0,993.
  - Frame thấp nhất ở giây 20: toàn cảnh quận nhiều chi tiết nhỏ, nên khác nhau chủ yếu vì độ phân giải.
- **Media QA** (`qa/preview_media_report_final_4k.json`):
  - 18 820/18 820 frame; 0 lỗi giải mã; 0 đoạn đen;
  - thẻ màu BT.709; watermark ở góc dưới trái, độ đậm 55%;
  - 7 điểm nối giữa chương qua SSIM.
- **Xem bằng mắt:** ảnh 4K tại 0:20, 5:40 (cắt 1:1), 9:33,75 (B31) và 10:07,5 (B33).
  - Ảnh nét, không thấy banding.
  - B31: nước đục, không có lưới bóng.
  - B33: như v3, gồm cả góc mép bãi nước mà chủ kênh đã duyệt giữ nguyên.
- **QA phim dài:** 17/17 PASS ở `final_4k`.
- **Gate** (`gates --preset final_4k`): G0–G6, GL, GV đều PASS. Hồ sơ `PUBLICATION_CANDIDATE`, kết luận của gate: `PUBLICATION_READY`.
- **Test:** 494 PASS, kể cả các file gọi Blender, chạy sau khi render xong. sha256 của 4 file cuối kiểm lại khớp sau khi test.

## Gate không kiểm việc duyệt mô tả
- Gate kiểm claim, giọng, phát âm, quyền âm thanh, kỹ thuật và việc có `publication_metadata` (tiêu đề, mô tả, ngôn ngữ, ghi công).
- Gate **không** kiểm chủ kênh đã duyệt nội dung mô tả hay chưa. Phim cầu cũng vậy.
- Chủ kênh chưa duyệt mô tả, nên phim **chưa sẵn sàng đăng**. Đăng phim là việc của chủ kênh.
- **Sửa mô tả không cần render lại:** file MP4, phụ đề và âm thanh không đổi.
- **Lưu ý cho lần sửa:**
  - `tools/longform_reports.py` ghi đè `review/YOUTUBE_DESCRIPTION.md` mỗi khi bản sinh tự động ngắn hơn 5 000 ký tự (hiện 4 858).
  - Khi đưa bản chủ kênh sửa vào, phải giữ bản đó khỏi bị ghi đè.

## Chưa ghi
- Việc duyệt mô tả YouTube và câu công bố giọng AI.
- Việc đăng phim.
- Agent không nghe được; không ghi một buổi nghe nào.
