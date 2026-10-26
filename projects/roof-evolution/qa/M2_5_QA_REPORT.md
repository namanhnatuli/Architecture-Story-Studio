# Báo cáo QA M2.5 — Ổn định hóa (2026-10-26/27)

Môi trường: macOS 26.6.2 · Apple M4 Pro 24 GB · Blender 5.2.2 LTS · FFmpeg 9.0.1 · Python 3.14.6.
Baseline: commit `75487d3` (tag `m2-baseline`). Kiểm tra qua MCP: xem `MCP_QA_REPORT.md`.

## 1. Các lỗi M2 đã sửa
| # | Lỗi | Bằng chứng trước khi sửa | Cách sửa | Kiểm chứng sau khi sửa |
|---|---|---|---|---|
| 1 | Rafters xuyên tường / joists | MCP xray (SC_002 f1, SC_003 f84); kiểm tra mới **FAIL ở cả 5 shot** trên geometry M2 | Cắt đầu dưới rafters 1 mm trên đỉnh tường (`geometry.box_object(clip_below_z)`) | `structure_clear_of_shared_at_rest` PASS ở 5/5 shot; MCP xray sạch; số điểm tiếp xúc khi nghỉ trong exploded view 37 → 33 |
| 2 | Highlight làm mái A mất màu | MCP SC_005 f47; render | Highlight = tự phát sáng bằng chính màu của phần đó (bỏ pha màu nhấn) | Render 960×540 + MCP f60: mái A vẫn graphite |
| 3 | Ánh sáng phẳng | So sánh L0 (hiện tại) | So 4 biến thể ở 960×540 (L0–L3), chọn L3: nắng trước-trái & cao, fill 0.3, world 0.4, AgX Medium High Contrast, ray tracing, cạnh vát smooth | Mặt trước sáng / mặt bên tối, bóng ngắn không chạm model bên cạnh, cạnh vát bắt sáng |
| 4 | Nhiễu dithering khi mờ dần | MCP SC_003 f84 (nhiễu giấy nhám); crop 960×540 | Twin BLENDED chỉ hiển thị khi đang mờ dần (`motion.split_fades`) | Crop mượt; SSIM tại điểm cắt = 1.0; `fade_twins_exclusive` PASS |
| 5 | Cắt cứng SC_004 → SC_005 | Contact sheet M2 | `SIDE_BY_SIDE.intro` (camera lùi ra, model đứng yên) | SSIM tại điểm cắt 0.99961 (960) / 0.99965 (640); `intro_matches_single_model_camera` PASS |
| 6 | `PACKAGE_MANIFEST.sha256` lỗi thời (v0.1) | `manifest --check`: 23 file thay đổi, 16 file mới | `python3 tools/cli.py manifest` từ `git ls-files` | `manifest --check` PASS (chạy trước commit) |
| 7 | 144 frame v0.1 + `.blend` cũ | `renders/preview/frame_*.png` | Nén không mất dữ liệu → `qa/baseline_v0_1/v0_1_preview_frames.tar.gz` (đã kiểm 144/144 checksum) → xóa bản rời; `.blend` được chuyển vào `qa/baseline_v0_1/` | Thư mục `renders/preview/` chỉ còn thư mục shot |

## 2. Các phương án đã so sánh
| Vấn đề | Phương án | Kết quả | Chọn |
|---|---|---|---|
| Ánh sáng | L0 hiện tại · L1 tương phản (cùng hướng nắng) · L2 nắng trước-trái · L3 = L2 với nắng cao hơn | L1 vẫn phẳng; L2 bóng đổ gần tới nhà B; L3 khối rõ + bóng ngắn | **L3** |
| Trong suốt | Dithered 64 mẫu · dithered 128 mẫu (×1.7 thời gian) · BLENDED cho mọi object · twin BLENDED chỉ khi đang mờ | 64/128 vẫn nhiễu; BLENDED cho mọi object đổi shading phần đặc → giật ở điểm cắt (SSIM 0.992) | **Twin** |
| Chuyển cảnh SC_004 → SC_005 | Cắt cứng (M2) · dissolve FFmpeg 0.75 s · camera lùi ra (intro) | Ở giữa dissolve có 3 "bóng ma" nhà chồng nhau, mất định hướng; intro giữ nhà B đúng chỗ, A hiện dần | **Intro** |

## 3. Kiểm tra hồi quy
| Kiểm tra | Kết quả |
|---|---|
| `python3 tools/cli.py validate` | PASS |
| `python3 -m unittest discover -s tests -v` | **49/49 OK** (43 test M2 + 6 mới: fade twins ×3, intro ×2, validator intro ×1) |
| `python3 tools/cli.py check-blender` | **58/58 PASS** (REPLACE_PARTS, EXPLODED_VIEW, SIDE_BY_SIDE, HOLD; transform ổn định; phần dùng chung giữ nguyên; framing; không thiếu object; tái lập) |
| Preview 640×360 | 48/120/144/60/108 frame = 480 frame, 20.000 s, 0 đoạn đen; điểm cắt SSIM 1.0 / 1.0 / 1.0 / 0.99965 |
| Review 960×540 | 480 frame, 20.000 s, 0 đoạn đen; điểm cắt SSIM 1.0 / 1.0 / 1.0 / 0.99961 |
| Hồi quy được phát hiện và sửa trong M2.5 | (a) test "phần dùng chung không bao giờ animate" fail khi có intro → siết lại: transform của phần dùng chung vẫn bị cấm, chỉ cho phép độ trong suốt ở các slot khác của intro; (b) `repeatable_build` fail ở SC_003/SC_005 → nguyên nhân là `matrix_world` cũ của object ẩn, chữ ký giờ chỉ băm những gì được render; (c) framing của SC_005 trong intro → dải nhãn chỉ áp sau khi camera đứng yên |

## 4. Hiệu năng (M4 Pro)
| Preset | Thời gian render (5 shot) | s/frame |
|---|---|---|
| 640×360 | ≈ 3.5 phút (cộng 29 s do máy ngủ ở SC_002) | 0.38–0.63 |
| 960×540 | 9.3 phút | 0.76–1.40 |

Sự cố: lần render 640 đầu tiên mất 19 phút vì **macOS tự ngủ khi idle** (`pmset -g log`: "Entering Sleep state due to 'Idle Sleep'" lúc 23:32:49; SC_003 frame 28 mất 911 s). Render lại SC_003: 73 s, không đứng. Đã khắc phục: CLI chạy Blender dưới `caffeinate -i`; bản render review sau đó không có frame nào quá 3 s.

## 5. Giới hạn còn lại
- Tấm phủ mái vẫn ăn 4–7.5 cm vào mép ngoài đỉnh tường khi nghỉ (bị chính tấm phủ đặc che; không có camera nào thấy). Kiểm tra mới chỉ áp cho rafters / ridge beam.
- Trong intro, twin của nhà A trông trong suốt như kính (thấy được cấu kiện bên trong) — cách hiện dần này được chấp nhận.
- Ảnh `look` của MCP là viewport, không phải bản render cuối; MCP chưa có tool gốc trong phiên Claude Code này.
- Chưa kiểm tra trên Blender 4.5 LTS. Không có audio.
