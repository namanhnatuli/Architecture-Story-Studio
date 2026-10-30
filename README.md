# Architecture Story Studio — AI + Blender Video Pipeline

**Bản khởi tạo v0.1 | macOS Apple Silicon M4 / RAM 16 GB | Blender 4.5 LTS hoặc 5.x | Codex / Claude Code**

> **Định hướng đã chốt:** Video tiếng Anh 8–15 phút giải thích *vì sao* kiến trúc có hình dạng và cách nó thay đổi theo lựa chọn thiết kế, lịch sử, khí hậu, kỹ thuật và văn hóa. Hình ảnh 3D giúp kể chuyện. Không phải kênh đập phá, không có công nhân/nhân vật bắt buộc, không ưu tiên công cụ 3D tương tác web.

## Bắt đầu tại đây (người mới)

1. Đọc [`QUICKSTART_MAC.md`](QUICKSTART_MAC.md).
2. Mở nguyên thư mục này bằng Codex hoặc Claude Code. AI phải đọc [`AGENTS.md`](AGENTS.md) **trước** khi chỉnh file.
3. Trong Terminal: `python3 tools/cli.py doctor` và `python3 tools/cli.py validate`.
4. Khi đã cài Blender: `python3 tools/cli.py still` để tạo **ảnh preview** của cảnh biến đổi mái nhà.
5. Sau khi xem ảnh: `python3 tools/cli.py preview` để render ảnh tuần tự rồi tạo MP4 qua FFmpeg.

Không cần tự cài package Python ngoài cho MVP; mã Python thuần phục vụ orchestration, còn `bpy` chạy bên trong Blender.

## Sản phẩm có sẵn trong package

- Bộ nguyên tắc dự án (`AGENTS.md`, `CLAUDE.md`, `PROJECT_BRIEF.md`), flow nghiên cứu → nội dung → visual → render → QA.
- Visual style bible, SOP kiểm chứng sự kiện, nguồn tư liệu/giấy phép, quy trình thao tác MCP an toàn.
- Schema JSON và validator không cần package bên thứ ba.
- Blender procedural demo: **một ngôi nhà, mái A dốc thấp → exploded view → mái A tháo rời / mái B lắp vào → so sánh A|B**; thư viện template tái sử dụng được (`REPLACE_PARTS`, `EXPLODED_VIEW`, `SIDE_BY_SIDE`, `HOLD`).
- Render still / PNG sequence theo shot (có cache) / MP4; validate, unit tests và QA tự động trong Blender.
- Prompt dùng với Codex/Claude và cấu trúc để mở rộng thành video dài.

### Sơ đồ thư mục

```text
Architecture-Story-Studio/
├── AGENTS.md                  # Quy tắc bắt buộc cho AI coding agents
├── CLAUDE.md                  # Entry point Claude Code
├── PROJECT_BRIEF.md           # Tuyên ngôn sản phẩm / non-goals
├── QUICKSTART_MAC.md          # Lệnh chạy từ số 0 trên Mac
├── config/                    # Style / render / policy
├── docs/                      # SOP chi tiết (nghiên cứu, storyboard, QA...)
├── prompts/                   # Prompt nghiên cứu, storyboard, coding, QA
├── schemas/                   # JSON Schema mô tả dữ liệu
├── engine/                    # bpy modules chạy trong Blender
├── tools/                     # CLI, validation, orchestration (stdlib Python)
├── scripts/                   # macOS convenience scripts
├── asset_library/             # Asset *được phép dùng* và manifest
├── projects/roof-evolution/   # Pilot có dữ liệu + mã render
└── tests/                     # Offline unit tests
```

## Quy tắc sản xuất

**Research → Narrative/claims → Visual beats → Architecture states → Greybox → TTS/timing lock → Final render → QA.**

- Mỗi hình ảnh phải phục vụ *một luận điểm* và có `visual_purpose` rõ ràng.
- Những kiến trúc có thật phải được kiểm chứng; không cho phép AI tự suy diễn một giả thuyết thành sự thật lịch sử.
- Lựa chọn phương án A/B luôn giữ các cấu kiện chung, chỉ thay cấu kiện thay đổi. Không biến hình vô nghĩa khi geometry không tương thích.
- Không chạy render final khi chưa có nguồn kiểm chứng cho những tuyên bố chính, chưa duyệt greybox và chưa khóa audio/timing.
- Preview được phép sử dụng narration và nguồn **placeholder** nếu ghi rõ trạng thái `provisional`.
- Assets có giấy phép không rõ = không được đưa vào final.

## Pilot có thể chạy

Dự án `roof-evolution` là **prototype minh họa kỹ thuật**, không phải lời khẳng định rằng mái dốc cao luôn tốt hơn mái dốc thấp. Từ M2 (2026-10-26), đây là chuỗi 20 giây, 24 fps, gồm 5 shot:

| Shot | Template | Nội dung |
|---|---|---|
| SC_001 (2.0s) | `HOLD` | Nhà với mái A dốc thấp |
| SC_002 (5.0s) | `EXPLODED_VIEW` | Mái A tách thành tấm phủ / ridge beam / rafters, rồi trở về chính xác |
| SC_003 (6.0s) | `REPLACE_PARTS` | Mái A rời đi, mái B lắp vào; móng, tường, joists đứng yên |
| SC_004 (2.5s) | `HOLD` + highlight | Thiết kế mới với mái B |
| SC_005 (4.5s) | `SIDE_BY_SIDE` + intro | Camera lùi ra từ nhà B (không có cắt cứng) để thấy A bên cạnh; cùng tỷ lệ, camera, ánh sáng |

```bash
python3 tools/cli.py doctor
python3 tools/cli.py validate
python3 -m unittest discover -s tests -v
python3 tools/cli.py still            # 5 key stills -> output/stills/, kèm output/roof_evolution_still.png
python3 tools/cli.py check-blender    # QA tự động trong Blender -> qa/blender_checks.json
python3 tools/cli.py preview          # render từng shot (có cache) -> output/shots/*.mp4 + output/roof_evolution_preview.mp4
python3 tools/cli.py shot --shot SC_002   # chỉ render lại một shot
python3 tools/cli.py preview --preset review   # 960×540 -> output/*_review.mp4, output/shots_review/
python3 tools/cli.py manifest --check     # PACKAGE_MANIFEST.sha256 khớp file đang được git theo dõi
```

Output: `output/` (stills, MP4 từng shot, MP4 đầy đủ), `scenes/SC_00X.blend` (scene tái lập được của từng shot), `renders/<preset>/SC_00X/` (frame PNG), `qa/` (log, báo cáo, contact sheet, dải tiến trình). Template và cấu hình: [`docs/05_ANIMATION_LIBRARY.md`](docs/05_ANIMATION_LIBRARY.md).

## Pilot M3 có lời dẫn: `projects/suffolk-roofs`
*"Why Did Traditional Roofs in Suffolk Change?"* — 75.5 giây (M3.5), lời dẫn tiếng Anh, phụ đề theo cụm từ. Đây là **preview nội bộ, chưa sẵn sàng xuất bản**: chờ duyệt biên tập (`projects/suffolk-roofs/review/EDITORIAL_APPROVAL_PACKAGE.md`), và **OmniVoice là NOT CLEARED cho xuất bản thương mại** ([audit](docs/licensing/TTS_LICENSE_AUDIT.md)), nên cần chọn một provider giọng đọc dùng để xuất bản. Quy trình: [`docs/m3/M3_PIPELINE.md`](docs/m3/M3_PIPELINE.md), [`docs/m3/M3_5_PUBLICATION_WORKFLOW.md`](docs/m3/M3_5_PUBLICATION_WORKFLOW.md).

## Trạng thái và giới hạn đã kiểm tra

**Đã kiểm tra trên Mac (Apple M4 Pro, Blender 5.2.2 LTS, FFmpeg 9.0.1) — M2.5:** validate, 49 unit/integration test, 58 kiểm tra Blender, preview 20s ở 640×360 và 960×540 (480 frame, không frame đen, 4 điểm cắt liền mạch theo SSIM), kiểm tra hình ảnh trên frame render và qua Blender MCP `look` (xem `docs/07_MCP_AND_AGENT_SETUP.md`). Chưa kiểm tra trên Blender 4.5 LTS. Kế hoạch M3: [`docs/m3/`](docs/m3/).

## Tài liệu tham khảo kỹ thuật

- Blender release/LTS: https://www.blender.org/releases/
- Blender CLI rendering: https://docs.blender.org/manual/en/latest/advanced/command_line/render.html
- Blender Python keyframes: https://docs.blender.org/api/current/info_quickstart.html
- Blender MCP: https://www.blender.org/lab/mcp-server/
- FFmpeg: https://ffmpeg.org/

Toàn bộ thư viện bên ngoài là tùy chọn. **MCP không phải điều kiện tiên quyết để chạy pilot**.

### Duy trì bối cảnh giữa các phiên làm việc với AI

Đọc `DECISIONS.md` (các quyết định đã chốt), `PROJECT_STATUS.md` (đang ở đâu), `docs/11_AI_COLLABORATION_PROTOCOL.md` (cách bàn giao). Khi một AI hoàn thành bước, yêu cầu cập nhật status thay vì dựa vào lịch sử chat.

## M4: dựng hình kiến trúc thủ tục và thư viện asset
Spec kiến trúc → thành phần ngữ nghĩa → hình học Blender → QA → asset tái sử dụng (`engine/arch/`, `asset_library/`). Có ba họ cầu (gỗ dầm, vòm đá, giàn thép Pratt/Warren), tất cả là mô hình **minh họa**. Pilot kỹ thuật: `projects/bridge-structure-evolution` (29.5 s, không lời dẫn). Tài liệu: [`docs/m4/M4_ARCHITECTURE_MODELING.md`](docs/m4/M4_ARCHITECTURE_MODELING.md); catalog: [`asset_library/catalog/CATALOG.md`](asset_library/catalog/CATALOG.md).

## M5: lập kế hoạch hình ảnh tự động
Beat có cấu trúc (`script/visual_beats.json`) → `planner/` tất định (không LLM khi chạy) → asset, template, shot, camera, timing → storyboard của engine. Thiếu năng lực thì báo thiếu, không lấp chỗ trống. Pilot: `projects/bridge-story-m5` "Three Ways to Span a Gap" (8 beat, 13 shot, 72.4 s, không lời, nội bộ). Fixture SYNTHETIC: `projects/roof-plan-m5`.
```bash
P="--project bridge-story-m5"
python3 tools/cli.py plan-visuals $P && python3 tools/cli.py build-shots $P   # → qa/VISUAL_COVERAGE.md
python3 tools/cli.py check-blender $P && python3 tools/cli.py preview $P
```
Tài liệu: [`docs/m5/M5_ARCHITECTURE.md`](docs/m5/M5_ARCHITECTURE.md), [`VISUAL_PLANNING_PROTOCOL.md`](docs/m5/VISUAL_PLANNING_PROTOCOL.md), [`ASSET_RESOLUTION.md`](docs/m5/ASSET_RESOLUTION.md), [`M5_QA_REPORT.md`](docs/m5/M5_QA_REPORT.md).

## M5.5: trí tuệ hình ảnh và production profile
Planner ước lượng mức nhìn thấy của từng mục tiêu trước khi render, rồi tự sửa kế hoạch: reframe, dải phụ đề, camera khác, ghost tạm thời, hoặc chiến lược khác. Bố cục so sánh được đo theo độ đọc được ở 640×360. Blender đo lại để kiểm chứng (`verify-visibility`). `production_profile` tách preview kỹ thuật không lời khỏi việc xuất bản.
```bash
python3 tools/cli.py plan-visuals --project bridge-story-m5 && python3 tools/cli.py build-shots --project bridge-story-m5
python3 tools/cli.py verify-visibility --project bridge-story-m5   # Level 2 (Blender) vs Level 1
python3 tools/cli.py gates --project bridge-story-m5               # TECHNICAL PREVIEW — VALID (silent); NOT FOR PUBLICATION
python3 tools/cli.py evaluate-planning                              # 24 ca đánh giá
```
Tài liệu: [`docs/m5_5/`](docs/m5_5/).


## M6: phim tài liệu có lời dẫn
Lời dẫn tiếng Anh sinh cục bộ bằng Kokoro-82M, hạng quyền `PENDING_REVIEW` (chưa được phép xuất bản). Hình được lập kế hoạch theo **thời lượng đo được** của từng câu. Chú thích kỹ thuật (mũi tên tải, phản lực, đường truyền tải khái niệm, nhãn, chú giải nén/kéo) bám vào bộ phận nhìn thấy được, và mỗi chú thích về lực đều trích claim. Lời dẫn và hình được kiểm mâu thuẫn. Một dự án có thể chứa nhiều họ kiến trúc nhờ scene context.
```bash
P="--project bridge-load-explained"
python3 tools/cli.py narrate $P && python3 tools/cli.py asr-check $P && python3 tools/cli.py align $P
python3 tools/cli.py lock-audio $P                                    # timing.json khóa theo audio
python3 tools/cli.py plan-visuals $P && python3 tools/cli.py build-shots $P
python3 tools/cli.py check-blender $P --preset review                 # gồm QA chú thích
python3 tools/cli.py smoke $P --shot SC_003 --preset review           # một cảnh có lời + chú thích
python3 tools/cli.py preview $P --preset review && python3 tools/cli.py assemble $P --preset review
python3 tools/cli.py research-map $P && python3 tools/cli.py gates $P --preset review
python3 tools/voice_audition.py $P                                    # thử 4 giọng; người dùng chọn
```
Tài liệu: [`docs/m6/`](docs/m6/), [`docs/licensing/KOKORO_LICENSE_AUDIT.md`](docs/licensing/KOKORO_LICENSE_AUDIT.md).

## M7: phim tài liệu dài "Why Bridges Don't All Look the Same"
Khoảng 10,7 phút, 8 chương, 38 beat, 102 câu. Phim trộn hình 3D, sơ đồ/bản đồ/dòng thời gian tự vẽ và 4 ảnh lưu trữ HAER (phạm vi công cộng, có hồ sơ quyền). Mọi bản dựng là **INTERNAL REVIEW** cho tới khi chủ kênh duyệt gói biên tập.
```bash
P="--project why-bridges-look-different"
python3 projects/why-bridges-look-different/script/story.py          # sinh narration/visual_beats/chapters
python3 tools/cli.py narrate $P --purpose publication && python3 tools/cli.py asr-check $P && python3 tools/cli.py align $P
python3 tools/cli.py lock-audio $P && python3 tools/cli.py plan-visuals $P && python3 tools/cli.py build-shots $P
python3 tools/cli.py chapters $P --preset review                      # manifest chương + QA phim dài
python3 tools/cli.py check-blender $P --preset review
python3 tools/cli.py chapter $P --chapter C4 --preset review          # một chương hoàn chỉnh
python3 tools/cli.py preview $P --preset review && python3 tools/cli.py assemble $P --preset review
python3 tools/longform_reports.py $P && python3 tools/cli.py gates $P --preset review
```
Tài liệu: [`docs/m7/`](docs/m7/).
