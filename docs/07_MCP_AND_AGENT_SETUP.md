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

## Cấu hình đã cài trên máy (2026-10-26)
- Package: `mcp-for-blender==2.2.4` (repo `ahujasid/mcp-for-blender`, trước đây `blender-mcp`). Đã review: socket addon bind `localhost:9876`, **không có xác thực**; `execute_blender_code` chạy Python tùy ý; addon **tự bật server khi mở Blender GUI** (tắt trong tab sidebar *MCP for Blender* nếu không dùng).
- Claude Code: `.mcp.json` ở project root (scope project, không ghi vào config user). Env: `DISABLE_TELEMETRY=true`, `BLENDER_MCP_SAFE_MODE=1` (chặn đọc/ghi file trực tiếp, subprocess, network trong script).
- Không dùng `uvx mcp-for-blender setup` / `@latest` / `update`: chúng tự sửa mọi client và nâng version chưa review. Nâng cấp = review diff mới rồi đổi version ghim.
- Không bật các tích hợp tải asset (Poly Haven, Sketchfab, Poly Pizza, Hyper3D, Meshy, Hunyuan3D) khi chưa kiểm tra license và ghi vào asset manifest.
- Codex: dùng cùng command/env (xem `.mcp.json`) theo tài liệu client Codex đang cài.

## Dùng MCP với engine M2 (chỉ để quan sát; sinh output vẫn qua CLI)
- Dựng một shot trong scene **riêng biệt**, không xóa file đang mở:
  ```python
  import sys; sys.path.insert(0, "<project root>")
  from engine import shot_builder
  ctx = shot_builder.build_shot("<project root>/projects/roof-evolution", "SC_003", isolated=True)
  ctx.scene.frame_set(ctx.plan.markers["middle"])
  ```
  `isolated=True` tạo scene `ASS_<shot>` và chuyển cửa sổ sang scene đó. Chế độ CLI mặc định thì làm rỗng file (chỉ an toàn khi chạy headless).
- Lệnh trên có `sys.path` / import cục bộ: safe mode có thể chặn. Khi đó **không tắt safe mode**; dùng `python3 tools/cli.py still|shot|check-blender` (mọi thao tác ghi file đều đi qua CLI).
- Trạng thái 2026-10-26: phiên Claude Code của milestone M2 khởi động trước khi đăng ký `.mcp.json`, nên **không có tool MCP nào**. Addon trong Blender GUI cũng chưa lắng nghe ở cổng 9876. Toàn bộ QA hình ảnh của M2 làm trên ảnh render thật qua CLI, **không** dùng `look` của MCP.
