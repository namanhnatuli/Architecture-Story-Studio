# SOP 07 — Codex/Claude + Blender MCP (optional)

## Phương án khuyến nghị
- **Coding:** Codex hoặc Claude Code, mở project root, đọc AGENTS.md.
- **Reproducible execution:** `python3 tools/cli.py ...` gọi Blender ở background; KHÔNG cần MCP.
- **Interactive inspection:** Khi cần AI mở Blender, xem scene và sửa bằng mệnh lệnh, cân nhắc MCP chính thức của Blender: https://www.blender.org/lab/mcp-server/

## Checklist trước khi bật MCP
1. Kiểm tra phiên bản Blender và tài liệu MCP tương thích, kiểm tra nguồn addon.
2. Đọc khả năng thực thi Python trực tiếp qua MCP; không coi kết nối là sandbox.
3. Làm trên project thử, lưu backup, hạn chế quyền truy cập tài khoản/thư mục cá nhân.
4. Bind server về loopback/local nếu addon cho phép, không expose public internet.
5. Thử một lệnh vô hại `list objects` hoặc tạo 1 cube, tuyệt đối không chạy mã tải từ nguồn ngẫu nhiên.
6. Để AI thay đổi code trong repo và render qua CLI cho batch; MCP chỉ giúp quan sát và sửa cục bộ.

## Quy ước AI giao tiếp
- Input: project slug + JSON spec, không prompt mơ hồ 1 câu để tự bịa kiến trúc.
- Output: code diff, command, created files, validation report, warnings.
- Lỗi: đọc trace, sửa module nhỏ nhất, tạo preview có thể tái hiện.

## Khác biệt Codex / Claude
`AGENTS.md` là nguồn hướng dẫn chung; `CLAUDE.md` trỏ đến nó. Không xây 2 kiến trúc khác nhau. Mỗi công cụ dùng MCP config theo tài liệu client bản đang cài (không chép blind install snippets nếu chưa xác nhận plugin/version).
