# Claude Code instructions

**MUST READ:** `AGENTS.md` (single source of truth), then `PROJECT_BRIEF.md` and `docs/01_PIPELINE.md` before modifying code or generating Blender scenes.

Use the exact same stages, safety restrictions, project schemas and validation gates as Codex. Do not bypass research, preview or license checks. `Blender MCP` is optional; Blender CLI is the reproducible execution path.

First reply when entering this repo: summarize detected Mac/Blender/FFmpeg environment, identify current project slug and propose the next smallest verifiable step. Never assume preview rendered unless the output exists.

## Làm một phim tài liệu mới (từ 2026-10-30)
- Chỉ cần chủ đề. Dán `prompts/NEW_DOCUMENTARY_AUTOPILOT.md` (thay `{{TOPIC}}`), rồi làm theo `docs/production/NEW_DOCUMENTARY_PLAYBOOK.md`. Mặc định nằm ở `config/production_defaults.json`; không hỏi lại ngôn ngữ, khung hình, độ dài, giọng hay preset.
- `python3 tools/episode.py new --topic "<chủ đề>"` tạo dự án. `python3 tools/episode.py status|next --project <slug>` suy ra giai đoạn từ chính các file; một phiên mới luôn bắt đầu bằng `status` và làm tiếp từ `NEXT:`.
- Dừng ở giai đoạn OWNER_APPROVAL: giao bản review nội bộ và gói duyệt, rồi chờ. Agent không bao giờ tự duyệt claim, giọng, phát âm hay xuất bản, và không ghi một buổi nghe chưa diễn ra.
- `projects/` chỉ chứa dự án đang làm. Phim tham chiếu: `projects/why-bridges-look-different/`. Các pilot cũ là fixture test ở `tests/fixtures/legacy_projects/` (chỉ đọc). Bản lưu trữ nằm ngoài repo (xem `docs/production/CLEANUP_REPORT.md`).
- Bản cuối 4K chỉ render sau khi chủ kênh duyệt, theo chương: `chapter --preset final_4k --release-frames`, rồi `final-assemble`, rồi `gates --preset final_4k`. Mỗi lúc một Blender.
