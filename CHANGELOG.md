# Changelog

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
