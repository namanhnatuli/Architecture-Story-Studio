# SOP 02 — File contracts

Dùng file dữ liệu làm giao diện giữa AI và Blender; không truyền toàn bộ câu chuyện thành một prompt Blender mơ hồ.

- `project.json`: slug, title, language, mode, duration, fps, render preset. Bản demo có `mode=prototype`.
- `storyboard/storyboard.json`: shot list (`id`, start, duration, `visual_purpose`, narration, `claim_ids`, camera, transition). Một shot chỉ nên có một nhiệm vụ hình ảnh rõ ràng.
- `storyboard/states.json`: `shared_components`, `variants`, `transitions`; thành phần nào được giữ, xóa, lắp vào, và chuyển động bằng template gì.
- `research/sources.json`: source ledger chứa URL/tác giả/ngày truy cập/giấy phép khi có; `claims[]` có `source_ids`, `review_status`, `uncertainty`.
- `assets/manifest.json`: tên/nguồn/credit/license/usage/status. Tài sản tạo nội bộ có thể ghi `origin=procedural`.

## IDs
- Shot: `SC_001`...; source `SRC_001`...; claim `CLM_001`...; asset `AST_001`...; component `roof_A_left`...
- ID phải ổn định; thay tên hiển thị nhưng không tùy tiện thay ID nếu đã liên kết.

## Mô hình 3D
- Mỗi object chính mang custom props: `component_id`, `variant_id`, `role`.
- Shared component không được duplicate giữa variant A/B nếu không có lý do.
- **Tất cả biến thể cùng hệ tọa độ, tỷ lệ, ground plane, camera, ánh sáng**, trừ khi shot yêu cầu.
- `REPLACE_PARTS` chỉ tác động đến IDs liệt kê, không được vô tình di chuyển shared.

## Demo vs production
- Demo có thể chứa claim `provisional` và không có source xác minh — file phải ghi đây là minh họa kỹ thuật.
- Production phải có verified source-backed claims, asset rights và audio lock, nếu không validator final gate chặn.
- JSON Schema mô tả form trong `schemas/`, validator mã thuần Python trong `tools/validator.py` chạy structural checks mà không cần pip.

## M2 — states.json v2 và storyboard animation (2026-10-26)
- `states.json` có `schema_version: 2` và `base` (builder + kích thước). Mỗi variant có `builder` (mặc định `gable_roof`) và `components: [{id, role, layer}]`. Đây là **quyền sở hữu tường minh**: danh sách phải khớp đúng các part mà builder tạo ra (`engine/spec.py`), nếu không thì validator báo lỗi.
- `shared_components` chấp nhận component id hoặc tên group (`walls`, `windows`, `door`, `structure`…). Mọi part của base phải được bao phủ. `ground` được chấp nhận nhưng giờ thuộc về môi trường, không thuộc model.
- File v1 (không có `components` / `base`) vẫn hợp lệ: parts lấy từ builder. Điều này có test (`test_v1_states_and_single_replace_shot_still_validate`).
- Shot có thể có `animation` (config của template, xem SOP 05); `transition` phải bằng `animation.template`. Shot v0.1 không có `animation` dùng `transition` cùng các giá trị mặc định.
- `storyboard.json` có `key_stills: [{id, shot, time_seconds | marker}]`. `marker` lấy từ plan của template (ví dụ `exploded_hold`), nên still luôn rơi đúng khoảnh khắc cần xem dù timing có đổi.
- Tên object trong Blender: shot một-model dùng chính `component_id`; SIDE_BY_SIDE dùng `<state>.<component_id>`. Custom prop `component_id` luôn giữ ID ổn định.
- Thời lượng shot phải là số nguyên frame; tổng các shot phải bằng `project.duration_seconds`.

## M3 — project có lời dẫn (2026-10-27)
Xem `docs/m3/M3_PIPELINE.md`. Hợp đồng mới: `script/narration.json` (`schemas/narration.schema.json`), sổ bằng chứng v2 (`schemas/sources.schema.json`: `evidence[{source_id, locator, excerpt}]`, các trạng thái PROVISIONAL / SOURCE_VERIFIED / EDITORIALLY_APPROVED / REJECTED; `verified` của v0.1 vẫn được chấp nhận và tương đương EDITORIALLY_APPROVED), `storyboard.template.json` (có mốc neo) → `storyboard.json` (được sinh ra), `script/timing.json` (khóa: hash của narration, audio beat và storyboard). Shot có `beat_ids`; validator yêu cầu mỗi beat được bao phủ đúng một lần, theo thứ tự.

## M6 — khóa theo audio, chú thích, scene context (2026-10-29)
Xem `docs/m6/M6_ARCHITECTURE.md` và `docs/m6/ANNOTATION_STYLE_GUIDE.md`.
- `script/narration.json`: `voice.provider` có thể là `kokoro`, `mode: preset`, `voice: bf_emma`, tham số `speed/seed/lang_code`. `license.rights_class` phải trùng registry (`PENDING_REVIEW`).
- `script/timing.json` của dự án do planner lập kế hoạch: `schema: timing/2`, `mode: PLANNED_AUDIO_LOCK`.
  - Giai đoạn `BEATS_LOCKED` (do `lock-audio`): thời lượng beat, khoảng câu tương đối, lock basis.
  - Giai đoạn `SHOTS_SCHEDULED` (do `build-shots`): shot, mốc beat/câu tuyệt đối, `rel_start/rel_end`, `beats_sha256`, `storyboard_sha256`, `plan_sha256`.
  - Một beat có thể trải nhiều shot liên tiếp.
- `script/visual_beats.json`: `annotations[]`, `highlight_at_sentence`, `visual_repair_preference`, intent `EXPLAIN_LOAD_PATH`.
- Shot do planner sinh có thể có `annotations` (bố cục đã tính sẵn: `items[{id, type, appear, disappear, claim_id, anchors[{world, screen, point, component_ids}], elements[...]}]`, `reserved`, `style_sha256`) và `scene_context`. Animation HOLD có thể có `label_position: TOP`.
- `states.json` schema 3 (chỉ khi dự án có nhiều họ): `contexts{name: {building_type, base, shared_components}}`, mỗi variant có `context`. Dự án một họ giữ schema 2.
