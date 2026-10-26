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
| SC_001 (2.5s) | `HOLD` | Nhà với mái A dốc thấp |
| SC_002 (5.0s) | `EXPLODED_VIEW` | Mái A tách thành tấm phủ / ridge beam / rafters, rồi trở về chính xác |
| SC_003 (6.0s) | `REPLACE_PARTS` | Mái A rời đi, mái B lắp vào; móng, tường, joists đứng yên |
| SC_004 (2.5s) | `HOLD` + highlight | Thiết kế mới với mái B |
| SC_005 (4.0s) | `SIDE_BY_SIDE` | A và B cùng tỷ lệ, cùng camera, cùng ánh sáng |

```bash
python3 tools/cli.py doctor
python3 tools/cli.py validate
python3 -m unittest discover -s tests -v
python3 tools/cli.py still            # 5 key stills -> output/stills/, kèm output/roof_evolution_still.png
python3 tools/cli.py check-blender    # QA tự động trong Blender -> qa/blender_checks.json
python3 tools/cli.py preview          # render từng shot (có cache) -> output/shots/*.mp4 + output/roof_evolution_preview.mp4
python3 tools/cli.py shot --shot SC_002   # chỉ render lại một shot
```

Output: `output/` (stills, MP4 từng shot, MP4 đầy đủ), `scenes/SC_00X.blend` (scene tái lập được của từng shot), `renders/<preset>/SC_00X/` (frame PNG), `qa/` (log, báo cáo, contact sheet, dải tiến trình). Template và cấu hình: [`docs/05_ANIMATION_LIBRARY.md`](docs/05_ANIMATION_LIBRARY.md).

## Trạng thái và giới hạn đã kiểm tra

**Đã kiểm tra trên Mac (Apple M4 Pro, Blender 5.2.2 LTS, FFmpeg 9.0.1):** validate, 43 unit/integration test, 50 kiểm tra Blender, preview 20s (480 frame, không frame đen), và kiểm tra hình ảnh trên frame đã render. Chưa kiểm tra trên Blender 4.5 LTS. Blender MCP chưa được dùng để kiểm tra hình ảnh (xem `docs/07_MCP_AND_AGENT_SETUP.md`).

## Tài liệu tham khảo kỹ thuật

- Blender release/LTS: https://www.blender.org/releases/
- Blender CLI rendering: https://docs.blender.org/manual/en/latest/advanced/command_line/render.html
- Blender Python keyframes: https://docs.blender.org/api/current/info_quickstart.html
- Blender MCP: https://www.blender.org/lab/mcp-server/
- FFmpeg: https://ffmpeg.org/

Toàn bộ thư viện bên ngoài là tùy chọn. **MCP không phải điều kiện tiên quyết để chạy pilot**.

### Duy trì bối cảnh giữa các phiên làm việc với AI

Đọc `DECISIONS.md` (các quyết định đã chốt), `PROJECT_STATUS.md` (đang ở đâu), `docs/11_AI_COLLABORATION_PROTOCOL.md` (cách bàn giao). Khi một AI hoàn thành bước, yêu cầu cập nhật status thay vì dựa vào lịch sử chat.
