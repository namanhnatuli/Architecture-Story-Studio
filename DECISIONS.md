# Locked product/engineering decisions (2026-10-22)

**Product choices**
- Audience: English-language YouTube, aim 8–15 minutes/video.
- Narration/story-first architecture history/design explainers. 3 formats: decision A→B due to constraints, architecture across time, regional comparison.
- 3D visuals: Clean Stylized Architectural / Technical Visualization; asset geometry separated into meaningful components.
- Transitions: DISASSEMBLE / REPLACE_PARTS / COMPARE / CUTAWAY / EXPLODED_VIEW; careful cause/effect visualizations.
- No required humans/characters/workers/machinery. Destruction is an occasional storytelling device, **not** the channel premise.
- No interactive web application as primary deliverable. Blender renders YouTube videos; Three.js is optional future tool, not MVP.

**Technical choices**
- Mac Apple Silicon M4, RAM 16 GB, creator is beginner.
- Blender + bpy + geometry/procedural modeling, Codex *or* Claude Code as primary coding assistant; Blender MCP optional for inspection; FFmpeg encode.
- Work in project-local files and deterministic, testable stages; single shared project spec JSON rather than giant free-form prompts.
- Unit test offline, then greybox preview, then publication gates. Keep render frames out of version control.
- Blender 4.5 LTS and 5.2 LTS supported by source code where possible; 5.x Eevee identifier changed. Runtime Blender rendering on target Mac remains unverified until user runs it.

**Pilot**
- `roof-evolution`: simple house where only roof configuration changes A→B; 6s greybox preview, no factual claim about roof engineering. This is a render technology smoke test, not a full researched YouTube episode.

If a requested change conflicts with these choices, document the reason and update this file before changing architecture.

## Bổ sung 2026-10-26 (M2) — không thay thế các quyết định ở trên
- **Planning tách khỏi bpy.** Logic template là Python thuần và có thể test; Blender chỉ dựng geometry và ghi keyframe. Lý do: validator G0 cần biết timing / ownership mà không phải khởi động Blender.
- **Một shot = một scene Blender độc lập**, dựng lại từ JSON mỗi lần render, có cache theo hash đầu vào. Các shot một-model dùng chung một camera fit theo mọi variant, để cắt cảnh không lộ.
- **Biến mất = di chuyển + mờ dần + hide_render, không bao giờ thu nhỏ scale.** Cấu kiện chỉ được đi qua mép khung khi đã trong suốt ít nhất 50%.
- **Ánh sáng bằng sun** (không dùng area light nhắm vào gốc tọa độ), để SIDE_BY_SIDE có điều kiện chiếu sáng như nhau.
- **Highlight giữ nguyên tông màu gốc**: màu nhấn #D9A441 chỉ chiếm 10%, phần còn lại là phát sáng cùng màu.
- **MCP chỉ để quan sát/kiểm tra.** Mọi output tái lập được đều đi qua CLI. Engine hỗ trợ `isolated=True` để MCP không xóa scene của người dùng.

## Bổ sung 2026-10-27 (M2.5) — không thay thế các quyết định ở trên
- **Mái đọc đúng cấu tạo khi tháo ra:** cấu kiện kết cấu gác lên tường (seat cut), không xuyên vào. QA kiểm tra mọi variant ở vị trí nghỉ.
- **Highlight = phát sáng bằng chính màu của phần đó.** Không dùng màu nhấn trên cấu kiện có màu nhận diện state.
- **Ánh sáng chuẩn "L3"** (nắng trước-trái, cao; AgX Medium High Contrast). Mọi thay đổi ánh sáng phải so sánh ở 960×540 trên các frame đại diện trước khi đổi config.
- **Trong suốt:** twin BLENDED chỉ hiển thị khi đang mờ dần; frame đặc luôn render bằng material dithered.
- **Camera chỉ được chuyển động trong intro của SIDE_BY_SIDE**, để nối liền từ shot single-model. Mọi điểm cắt khác phải liền mạch (SSIM ≥ 0.98) trừ khi khai báo `cut_from_previous: "hard"`.
- **Git là nguồn sự thật cho file nguồn**; `PACKAGE_MANIFEST.sha256` được sinh từ `git ls-files`. Frame/video/blend là output được sinh ra, không commit.
- **M3 không dùng multi-agent:** pipeline tuyến tính có gate; chỉ thêm dữ liệu (nguồn, narration, timing) và bước hậu kỳ (audio, ghép, phụ đề). Pilot Suffolk dựa trên nguồn chính quyền địa phương, phạm vi hẹp.

