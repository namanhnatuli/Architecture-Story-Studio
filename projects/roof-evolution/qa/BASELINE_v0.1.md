# Baseline v0.1 — trước khi bắt đầu M2 (2026-10-26)

Môi trường: macOS 26.6.2, Apple M4 Pro, 24 GB, Blender 5.2.2 LTS, FFmpeg 9.0.1, Python 3.14.6.

| Kiểm tra | Lệnh | Kết quả |
|---|---|---|
| Môi trường | `python3 tools/cli.py doctor` | Đã tìm thấy Blender + FFmpeg |
| G0 | `python3 tools/cli.py validate` | PASS (cảnh báo: CLM_001 provisional) |
| Unit tests | `python3 -m unittest discover -s tests` | 4/4 OK |
| Still | `python3 tools/cli.py still` | PNG 640×360 tại frame 130 (mái B), đã xem ảnh |
| Preview | `python3 tools/cli.py preview` | 144 frame, h264 640×360, 24 fps, 6.000 s, 0 frame đen |

Các file đã lưu trữ (bản sao, để so sánh với M2): `qa/baseline_v0_1/roof_evolution_still.png`,
`qa/baseline_v0_1/roof_evolution_preview.mp4`, `qa/baseline_v0_1/contact_sheet_preview.png`.

Baseline đã có bản sửa framing camera hôm nay (đỉnh mái B bị cắt; xem CHANGELOG 0.1.1).

## Các giới hạn đã biết của v0.1 mà M2 cần xử lý
- Một entry point duy nhất, timeline 6 s cố định; không có khái niệm shot/template; `keyframe_replace_parts` gắn chặt với pilot.
- Các tấm mái rời đi bị thu nhỏ còn 1% (spec M2: không được thu nhỏ về 0 nếu gây artifact).
- Mái chỉ gồm 2 tấm phủ + 2 tường hồi tam giác; không có cấu kiện kết cấu nào để làm exploded view.
- Ánh sáng là area light nhắm vào gốc tọa độ, nên sẽ không đồng đều nếu đặt các model cạnh nhau.
- Mép tấm nền đất 14×13 m lộ ra trong khung hình.
- Kết nối Blender MCP: server đã đăng ký trong `.mcp.json`, nhưng phiên Claude Code hiện tại khởi động trước khi đăng ký nên không có tool MCP; addon trong Blender GUI chưa lắng nghe ở cổng 9876.
