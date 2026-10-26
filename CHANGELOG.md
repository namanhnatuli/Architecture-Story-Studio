# Changelog

## 0.2.5 — 2026-10-27 — M2.5: ổn định hóa, QA qua MCP, sẵn sàng cho M3
- **Git:** giữ nguyên commit `init` của người dùng; baseline M2 được commit (`75487d3`, tag `m2-baseline`); `.gitignore` bổ sung media QA, `.blend@`, file tạm, `.env*`, `.claude/settings.local.json`.
- **MCP:** gọi thật `get_addon_status`/`get_scene_info`/`execute_blender_code`/`look` qua stdio (21/21 lệnh trước khi sửa, kèm lượt kiểm tra lại sau khi sửa) trên một phiên bản Blender riêng mở bản sao của các scene. Đã xác định vì sao addon không lắng nghe (Blender mở trước khi addon được cài) và phát hiện cấu hình scope local ghi đè safe mode (chỉ ghi lại, không tự sửa).
- **Sửa #1 — rafters xuyên tường:** cắt đầu dưới rafters 1 mm trên đỉnh tường (`box_object(clip_below_z=…)`). Kiểm tra mới `structure_clear_of_shared_at_rest` FAIL trên geometry M2, PASS sau khi sửa.
- **Sửa #2 — highlight:** chỉ còn tự phát sáng bằng màu của chính phần đó (bỏ pha màu nhấn); mái A giữ màu graphite.
- **Sửa #3 — ánh sáng phẳng:** chọn L3 sau khi so 4 biến thể ở 960×540: nắng chính từ trước-trái và cao (bóng ngắn, không chạm model bên cạnh), fill 0.3, world 0.4, AgX `Medium High Contrast`, ray tracing Eevee, smooth shading + weighted normals cho cạnh vát (edge highlight). Mọi thông số nằm trong `config/visual_style.json`.
- **Sửa #4 — nhiễu dithering:** twin BLENDED chỉ hiển thị khi đang mờ dần (`motion.split_fades`). Frame tĩnh và điểm cắt không đổi; đã so sánh với dithered 64/128 mẫu và BLENDED cho mọi object.
- **Sửa #5 — cắt cứng SC_004 → SC_005:** `SIDE_BY_SIDE.intro` (camera lùi ra, model đứng yên). Đã so sánh với dissolve bằng FFmpeg. SC_001 2.0 s, SC_005 4.5 s, tổng vẫn 20.0 s.
- **Sửa #6 — manifest:** lệnh `python3 tools/cli.py manifest [--check]` tạo lại từ `git ls-files`.
- **Sửa #7 — frame v0.1:** 144 PNG được nén không mất dữ liệu (đã kiểm checksum) vào `qa/baseline_v0_1/v0_1_preview_frames.tar.gz` rồi mới xóa bản rời; file `.blend` của v0.1 được chuyển vào cùng thư mục.
- **QA:** 58 kiểm tra Blender (thêm structure/twins/intro; chữ ký tái lập chỉ băm những gì được render); media QA đo SSIM tại điểm cắt (`cut_from_previous`); 49 unit test. CLI chạy Blender dưới `caffeinate -i` (máy ngủ khi idle từng làm một frame đứng 15 phút).
- **Output review riêng:** `--preset review` ghi vào `output/stills_review/`, `output/shots_review/`, `*_review.mp4`; preview 640×360 giữ nguyên tên cũ.
- **M3:** kế hoạch + brief nghiên cứu + storyboard nháp trong `docs/m3/` (chưa sản xuất).

## 0.2.0 — 2026-10-26 — M2: Engine biến đổi trực quan tái sử dụng v1
- Template mới: `REPLACE_PARTS`, `EXPLODED_VIEW`, `SIDE_BY_SIDE`, `HOLD` (+ highlight), điều khiển hoàn toàn bằng `storyboard.json` → `animation`.
- Planning bằng Python thuần (`engine/motion.py`, `templates.py`, `spec.py`, `framing.py`), nên validator kiểm tra được timing, ownership và option ngay ở G0. Keyframe được ghi với interpolation tường minh (`engine/animate.py`, hỗ trợ cả slotted actions của 5.x).
- Builder có metadata: mái gable gồm tấm phủ, rafters, ridge beam, tường hồi; base có thêm ceiling joists. `states.json` v2 có quyền sở hữu tường minh (v1 vẫn tương thích).
- Mỗi shot là một scene độc lập (`engine/shot_builder.py`) với camera ortho khóa, fit theo hình học. Ánh sáng chuyển sang sun (không phụ thuộc vị trí); mặt đất liền khối.
- CLI: `still` (key stills), `preview` (render theo shot có cache + MP4 theo shot + MP4 đầy đủ + media QA + contact sheet / dải tiến trình), `shot`, `check-blender`. Gọi Blender với `--python-exit-code 1`.
- QA: `engine/qa_checks.py` (50 kiểm tra), 38 test offline mới + 1 test tích hợp Blender (tổng 43 cùng 4 test cũ).
- Pilot roof-evolution: 20 s, 5 shot. Đã sửa: dải nền ở mép trên (clip_end), highlight làm đổi tông màu, bóng đổ lên model bên cạnh, cấu kiện đặc bị khung cắt (2 trường hợp), móng nổi 5 cm.
- Loại bỏ: cơ chế thu nhỏ còn 1% của v0.1 (`engine/transform.py` được giữ lại làm tham khảo, đánh dấu DEPRECATED, không còn được import).

## 0.1.1 — 2026-10-26
- Pilot `roof-evolution` render lần đầu trên Mac thật: macOS 26.6.2, Apple M4 Pro 24 GB, Blender 5.2.2 LTS, FFmpeg 9.0.1, Python 3.14.6.
- Fix framing (`engine/scene.py`): đỉnh mái B (48°, ~5.2 m) bị cắt 19% ở mép trên, móng hụt 3% ở mép dưới. Camera giờ nhắm z=2.1 (đèn vẫn nhắm z=1.6), `ortho_scale` 10.1 → 14.0; đo bằng `world_to_camera_view` trên geometry thật: cả A và B có lề dọc ~6%.
- Preview 6 s / 144 frame / 640×360 render trong ~35 s; MP4 h264 yuv420p, không black frame.
- Cài MCP for Blender 2.2.4 (`ahujasid/mcp-for-blender`, commit `febcd90`, MIT) sau khi review mã: wheel PyPI khớp source, addon SHA-256 `8e193a24…7083`. Addon → `~/Library/Application Support/Blender/5.2/scripts/addons/blender_mcp.py` (đã enable). Server đăng ký ở `.mcp.json` (scope project), ghim version, `DISABLE_TELEMETRY=true`, `BLENDER_MCP_SAFE_MODE=1`, localhost:9876. Pipeline CLI dùng `--factory-startup` nên không nạp addon.

## 0.1 — 2026-10-22
- Chốt narrative-first architecture 3D pipeline.
- Tạo chính sách AI coding, workflow, JSON schemas, validation, Mac CLI, sample roof transitions.
- Thêm unit tests và tài liệu đầu vào cho Codex/Claude.
- MVP chưa được render bằng Blender thực tế trong môi trường đóng gói.
