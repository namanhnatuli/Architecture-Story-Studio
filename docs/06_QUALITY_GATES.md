# SOP 06 — Quality Assurance

| Gate | Kiểm tra | Bắt buộc trước |
|---|---|---|
| G0 | Schema, IDs, timings, file references | Dựng geometry |
| G1 | Claim với source, nguồn đáng tin cậy, uncertainty | Narration final |
| G2 | Still A/mid/B, graybox, tỉ lệ, camera, silhouettes | Render preview |
| G3 | Frame sequence đầy đủ, không frame đen, không popping, camera giữ nguyên | Render final |
| G4 | TTS cues đã lock, scene length khớp audio | Final assembly |
| G5 | Rights, factual QA, audio peak, codecs, transcript/captions | Xuất bản |

## Tự động được
- Đọc JSON, ID duy nhất, source refs hiện hữu, timeline không overlap sai, duration hợp lệ.
- Check command existence, stdout/stderr, file exist, frame count (preview), ffprobe stream metadata, file size.
- Render 3 ảnh still tại đầu/giữa/cuối; lưu contact sheet nếu tích hợp công cụ.

## Cần review người/AI
- Có đúng bộ phận khác nhau? Mái mới có gắn vào đúng khung? Màu dễ phân biệt?
- Narration giải thích 'vì sao' chứ không chỉ 'điều gì'? Dữ kiện có nguồn thật?
- Thiết kế theo niên đại/vùng có bị phóng đại hoặc trộn lẫn văn hóa?
- Motion không gây hiểu lầm về cơ chế thi công ngoài đời?

## Khi fail
Nêu severity, affected scene_id, evidence (frame#, log), đề xuất fix, tái chạy đúng scene. Không đánh dấu pass bằng cách tự xóa cảnh lỗi.
