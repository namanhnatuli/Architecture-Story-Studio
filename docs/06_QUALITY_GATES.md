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

## Kiểm tra tự động M2 (2026-10-26)
| Lệnh | Kiểm tra |
|---|---|
| `python3 tools/cli.py validate` (G0) | Ownership component, shared bao phủ toàn bộ base, template/option/easing/direction hợp lệ, **timing vừa shot** (planner chạy offline), marker của key still tồn tại |
| `python3 -m unittest discover -s tests -v` | Easing khớp Blender, start/end transform, stagger, thứ tự, framing/layout, thông báo lỗi validator, tương thích ngược v1; kèm test tích hợp Blender |
| `python3 tools/cli.py check-blender` | Trong Blender sau `frame_set()`: đủ component + parent, key đã evaluate = plan (≤1e-4), phần không animate đứng yên (world, ≤1e-5), không đổi scale, REPLACE khớp đúng vị trí cuối + visibility, EXPLODED về chính xác + **không có giao cắt mesh mới** (BVH), visibility cuối, framing, camera khóa, công thức chiếu khớp Blender, SIDE_BY_SIDE (transform local giống hệt / offset world đúng bằng slot / không chồng lấn), camera giống nhau giữa các shot, **build lại cho kết quả giống từng bit** (sha256) |
| `python3 tools/cli.py preview` | Đủ số frame mỗi shot, ffprobe (codec/kích thước/fps/số frame/thời lượng), blackdetect, contact sheet + dải tiến trình 0/25/50/75/100% cho từng shot |

**Quy tắc framing:** mọi hình học đặc hơn 50% (`ass_transparency < 0.5`) phải nằm trong khung với lề ≥ 1%. Cấu kiện chỉ được đi qua mép khung khi đang trong suốt ít nhất 50% (vào/ra khỏi khung).

Kết quả: `projects/<slug>/qa/blender_checks.json`, `qa/preview_media_report.json`, `qa/progress_<shot>.png`, `qa/contact_sheet_preview.png`. Các file này là bằng chứng; vẫn phải nhìn ảnh trước khi đánh dấu G2/G3 là PASS.

## Bổ sung M2.5 (2026-10-26)
| Kiểm tra | Bắt lỗi gì |
|---|---|
| `structure_clear_of_shared_at_rest` (Blender) | Rafters / ridge beam ở vị trí nghỉ xuyên vào tường hoặc joists. Đã chứng minh: **FAIL trên geometry M2, PASS sau khi sửa** |
| `fade_twins_exclusive` (Blender) | Twin blended hiển thị cùng lúc với bản gốc, hoặc hiển thị ở frame đầu/cuối của shot |
| `camera_locked` (Blender) | Camera chỉ được chuyển động trong intro của SIDE_BY_SIDE, khóa sau `intro_end` |
| `intro_matches_single_model_camera` (Blender) | Frame 1 của intro phải trùng camera single-model (ortho, hướng, vị trí trừ offset slot) |
| `repeatable_build` | Chỉ băm những gì được render. Object ẩn có `matrix_world` cũ (Blender không evaluate object ẩn khỏi viewport), nên chỉ băm cờ ẩn của chúng |
| Media QA `cuts` | SSIM giữa frame cuối shot N và frame đầu shot N+1 ≥ 0.98, trừ khi shot khai báo `cut_from_previous: "hard"` |
| `python3 tools/cli.py manifest --check` | `PACKAGE_MANIFEST.sha256` khớp với các file đang được git theo dõi |

Render dài trên macOS chạy dưới `caffeinate -i`: nếu không, máy tự ngủ khi idle sẽ làm một frame "đứng" 15 phút (đã quan sát ngày 2026-10-26, xác nhận qua `pmset -g log`).
