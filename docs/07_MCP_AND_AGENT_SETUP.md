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

## M2.5 — Kiểm chứng MCP thật (2026-10-26)
- **Đã gọi thành công** `get_addon_status`, `get_scene_info`, `execute_blender_code` và `look` qua MCP server `mcp-for-blender==2.2.4` (server 1.30.0, addon 1.8, protocol 15, `up_to_date: true`; safe mode bật, telemetry tắt; mọi thư viện asset và generator đều tắt).
- Cách gọi: phiên Claude Code vẫn **chưa có tool MCP gốc** (phiên khởi động trước khi đăng ký server), nên tool được gọi bằng một client JSON-RPC/stdio nhỏ viết bằng stdlib. Client này khởi chạy chính server với env đã ghim. Blender dùng để kiểm tra là **một phiên bản GUI riêng** mở *bản sao* của `scenes/SC_00X.blend`, nên Blender người dùng đang mở không bị đụng tới. Cổng `127.0.0.1:9876` (chỉ loopback).
- Nguyên nhân cổng 9876 không lắng nghe trước đó: phiên bản Blender GUI của người dùng khởi động lúc 22:16:54, **trước khi** addon được cài và bật (22:19–22:20), nên chưa bao giờ nạp addon. Khởi động lại Blender là đủ.
- Mẹo `look`: chế độ `angles` mặc định tự đóng khung theo *mọi* object hiển thị, kể cả mặt sàn 160 m → luôn truyền `target=[...]`. `mode="frames"` + `view="camera"` + `frames=[...]` cho ra dải tiến trình qua camera của shot.
- Safe mode cho phép `open_mainfile` và `frame_set`, nhưng chặn `quit_blender` và mọi import ngoài bpy/bmesh/mathutils. Engine vẫn chạy qua CLI.

### ⚠️ Cấu hình scope local đang ghi đè cấu hình đã review
`claude mcp list` đang dùng server `blender` ở **scope local** (`uvx mcp-for-blender`, không ghim phiên bản, `env` rỗng → **không safe mode, telemetry bật, tự lên bản mới nhất**). Scope local được ưu tiên hơn `.mcp.json` của project. Server này được thêm ngoài các bước của agent (có thể do `uvx mcp-for-blender setup`). Agent **không tự sửa**. Nếu muốn dùng cấu hình đã review:
```bash
claude mcp remove blender -s local     # sau đó .mcp.json (ghim 2.2.4, safe mode) sẽ có hiệu lực
```

## M3 — Đã xử lý xung đột scope (2026-10-27)
- Trước khi sửa: cấu hình có hiệu lực là **scope local** `blender` (`uvx mcp-for-blender`, không ghim phiên bản, `env: {}` → không safe mode, telemetry bật). Đã sao lưu `~/.claude.json` thành `~/.claude.json.backup-m3-20261027-071823` (quyền 600).
- Đã chạy `claude mcp remove blender -s local`. Lệnh này **chỉ** gỡ mục của project này; project không có server local nào khác và không đụng tới scope user.
- Giờ có hiệu lực là **scope project** (`.mcp.json`): `mcp-for-blender==2.2.4` (phiên bản đã chạy được 30/30 lệnh ở M2.5), `BLENDER_MCP_SAFE_MODE=1`, `DISABLE_TELEMETRY=true`, `localhost:9876`.
- Đã kiểm chứng: `claude mcp get blender` → Project config, ✓ Connected; tool được gọi qua client stdio với đúng lệnh/env đó: `get_addon_status`, `get_scene_info`, `look`, `execute_blender_code` đều chạy được, và **safe mode chặn `import os`** ("Rejected by safe mode").
- Lần tới khi khởi động lại Claude Code, server project cần được phê duyệt một lần (`enabledMcpjsonServers` hiện đang rỗng).
