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
