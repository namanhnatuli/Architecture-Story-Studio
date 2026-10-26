# Báo cáo QA M2 — Engine biến đổi kiến trúc v1 (2026-10-26)

Môi trường: macOS 26.6.2, Apple M4 Pro, 24 GB · Blender 5.2.2 LTS · FFmpeg 9.0.1 · Python 3.14.6.
Phạm vi: pilot kỹ thuật. G1 (sự thật) vẫn **provisional**, G4 (timing narration) **chưa khóa**; final gate vẫn bị chặn đúng như thiết kế.

## 1. Trạng thái kết nối MCP
- Server `blender` đã đăng ký trong `.mcp.json` (mcp-for-blender 2.2.4, safe mode bật, telemetry tắt); `claude mcp list` báo `✓ Connected`.
- **Phiên Claude Code này không có tool MCP nào** (`get_addon_status`, `get_scene_info`, `execute_blender_code`, `look`): phiên khởi động trước khi file đăng ký được tạo. Tool search không tìm thấy tool Blender nào.
- Blender GUI đang chạy (pid 71601) nhưng **không có gì lắng nghe ở cổng 9876**; server của addon chưa được khởi động.
- Hệ quả: **không có bước kiểm tra hình ảnh qua MCP nào được thực hiện**. Mọi kiểm tra hình ảnh dưới đây làm trên ảnh render thật qua Blender CLI (Eevee, 640×360), được mở xem trực tiếp. Engine có chế độ `isolated=True` để sau này dùng MCP mà không đụng tới scene người dùng đang mở.

## 2. Các kiểm tra đã chạy
| Lệnh | Kết quả |
|---|---|
| `python3 tools/cli.py doctor` | Đã tìm thấy Blender 5.2.2 LTS, FFmpeg 9.0.1 |
| `python3 tools/cli.py validate` | PASS (cảnh báo: CLM_001 provisional) |
| `python3 -m unittest discover -s tests -v` | **43/43 OK**: 4 test contract v0.1, 28 test motion/framing, 10 test validator, 1 test tích hợp Blender |
| `python3 tools/cli.py check-blender` | **50/50 PASS** → `qa/blender_checks.json` |
| `python3 tools/cli.py still` | 5 key stills + still kiểu cũ, đều tồn tại và không rỗng |
| `python3 tools/cli.py preview` | 5 shot render xong, 6 MP4; media QA PASS → `qa/preview_media_report.json` |
| `python3 tools/cli.py final-gate` | Vẫn bị chặn đúng như mong đợi (claim chưa kiểm chứng, audio chưa khóa) |

Các số liệu chính đo trong Blender:
- Giá trị keyframe đã evaluate khớp planner Python thuần: sai số lớn nhất 5.3e-07 (SC_003, 14 object × 69 frame).
- REPLACE_PARTS: 7 phần bị gỡ (cuối shot là `hide_render`); 7 phần mới khớp đúng vị trí (sai số 1e-5). 15 object dùng chung không đổi trên mọi frame lấy mẫu.
- EXPLODED_VIEW: độ lệch lúc giữ là 1.60 / 0.80 / 0.50 m như cấu hình; trở về chính xác; 0 giao cắt mesh mới (bỏ qua 37 điểm tiếp xúc có sẵn khi nghỉ, ví dụ rafters ăn vào đỉnh tường).
- SIDE_BY_SIDE: transform local của phần dùng chung và kích thước giống hệt giữa hai slot; offset world đúng bằng offset của slot; khe giữa hai model theo trục màn hình 2.14 m; nội dung nằm trên dải nhãn 12% (điểm thấp nhất y = 0.190).
- Framing: lề tối thiểu 7% ở các shot tĩnh, 1.8% trong SC_003 (tấm phủ B lúc đang hạ xuống); camera không bao giờ có animation. SC_001–SC_004 dùng chung một camera (ortho 14.356), SC_005 có ortho 16.684.
- Build lại tái lập được: sha256 của mọi ma trận world, visibility và tham số shader trùng nhau giữa hai lần build, ở cả 5 shot.
- Media: 60 / 120 / 144 / 60 / 96 frame theo shot, tổng 480 frame = 20.000 s, h264 yuv420p 640×360 24 fps, 0 đoạn đen.

## 3. Lỗi hình ảnh phát hiện và đã sửa
| # | Phát hiện (bằng chứng) | Nguyên nhân | Cách sửa (module) |
|---|---|---|---|
| 1 | Pilot v0.1: đỉnh mái B bị cắt 19% ở mép trên, móng hụt 3% (`baseline_v0_1`) | Camera đặt tay | Camera fit theo hình học thật (`framing.py`) |
| 2 | Dải nền xám ở mép trên mọi khung (still đầu tiên của M2) | `clip_end` chỉ tính từ model, sàn ở xa bị cắt | `clip_end ≥ 1000 m` (`framing.py`) |
| 3 | Highlight biến mái A graphite thành màu be ở shot so sánh | Pha 25% màu nhấn vào màu gốc | Highlight = phát sáng cùng màu + 10% màu nhấn (`scene.py`) |
| 4 | Bóng của nhà A đổ lên chân nhà B ở SIDE_BY_SIDE | Nắng chiếu chéo ngang khung hình | Nắng chính chiếu từ phía trước, bóng đổ ra sau (`visual_style.json`) |
| 5 | Tường hồi phía sau mái B đặc hơn 50% nhưng nằm ngoài khung 7% (SC_003 frame 62, phát hiện bởi `camera_framing`) | Rơi từ 4 m với EASE_OUT nên đã hiện rõ khi vẫn còn cao | Incoming distance 4.0 → 2.0 m, `fade_end` 0.55 → 0.75 (storyboard) |
| 6 | Tấm phủ A còn đặc hơn 50% nhưng lệch ra ngoài khung 1.7% (SC_003 frame 39) | Mờ dần bắt đầu quá muộn | `fade_start` 0.25 → 0.0, distance 3.5 → 3.0 m (storyboard) |
| 7 | v0.1 thu nhỏ các phần rời đi còn 1% | Thiết kế cũ | Bỏ hẳn; có check `no_scale_change` |
| 8 | Móng nổi 5 cm trên mặt đất (hình học v0.1) | Đỉnh tấm nền ở z = −0.43 | Mặt sàn đặt ở z = −0.38 (`scene.py`) |
| 9 | Lỗi timing báo thành "keyframe 173 outside frames" | Thông báo lỗi ở tầng thấp | Báo dạng "timing needs frame N … lengthen the shot" (`motion.py`, có test) |

## 4. Bằng chứng hình ảnh (đã mở xem)
- Still ban đầu: `output/stills/01_initial.png` (cũng là `output/roof_evolution_still.png`)
- Exploded view: `output/stills/02_exploded_hold.png`, `output/shots/SC_002.mp4`, `qa/progress_SC_002.png`
- Thay mái: `output/stills/03_replace_middle.png`, `output/shots/SC_003.mp4`, `qa/progress_SC_003.png`
- Lộ diện: `output/stills/04_reveal.png`, `qa/progress_SC_004.png`
- So sánh cạnh nhau: `output/stills/05_comparison.png`, `output/shots/SC_005.mp4`, `qa/progress_SC_005.png`
- Toàn bộ chuỗi: `output/roof_evolution_preview.mp4`, `qa/contact_sheet_preview.png` (mỗi giây một ô)

## 5. Giới hạn còn lại
- Ánh sáng/vật liệu ở mức greybox, còn hơi phẳng (độ tương phản giữa mặt trước và mặt bên thấp). Cần tinh chỉnh ở stage 8.
- Ở đỉnh highlight, mái A vẫn ngả nhẹ về xám. Chấp nhận được, nhưng nên xem lại khi chỉnh màu.
- Phần rời đi / phần mới đi qua giai đoạn trong suốt dạng dithered; ở 640×360 thấy nhiễu nhẹ, trên 960×540 chưa kiểm tra.
- Rafters ăn vào đỉnh tường khi ở vị trí nghỉ (không thấy được khi đã lắp đủ; hiện tại không có cấu kiện birdsmouth/top plate).
- Lần cắt từ SC_004 sang SC_005 là cắt cứng (camera fit khác); chưa có chuyển cảnh mềm.
- Chưa kiểm tra trên Blender 4.5 LTS. Chưa có preset review (960×540). Không có audio. Narration là placeholder.
- Không có kiểm tra hình ảnh qua MCP (xem mục 1).
