# M3 — Pipeline phim có lời dẫn (đã triển khai 2026-10-27)

**Research → Script → OmniVoice → Visual Storyboard → Blender Animation → Render → Video QA.**
Pilot: `projects/suffolk-roofs` (73.0 s). Tích hợp TTS: [`docs/integrations/OMNIVOICE.md`](../integrations/OMNIVOICE.md).

## File của một project có lời dẫn
| File | Ai viết | Nội dung |
|---|---|---|
| `research/sources.json` | người + AI | Nguồn + claim: `PROVISIONAL` → `SOURCE_VERIFIED` (có locator + excerpt) → `EDITORIALLY_APPROVED` (người duyệt) / `REJECTED` |
| `script/narration.json` | người + AI | Beat (`framing` / `fact` / `interpretation`) gồm các câu + `claim_ids`; giọng đọc + **license**; nhịp (khoảng nghỉ giữa câu, lead-in, tail) |
| `storyboard/states.json` | người + AI | Base + variant (`covering.style`, `structure_from`) |
| `storyboard/storyboard.template.json` | người + AI | Shot gồm `beat_ids`, template, **mốc neo** `@B3.s0+0.4`, card 2D |
| `audio/narration_manifest.json`, `audio/segments/*.wav`, `audio/beats/*.wav` | `narrate` | Cache theo nội dung; thời lượng đo được; kết quả ASR |
| `script/timing.json` | `schedule` | Bản kê timing: ranh giới shot chính xác đến frame, vị trí beat/câu, khóa (hash) |
| `storyboard/storyboard.json` | `schedule` | Storyboard đã giải các mốc neo mà Blender render (**không sửa tay**) |
| `script/SCRIPT_AND_STORYBOARD.md` | `schedule` | Kịch bản + storyboard + ánh xạ claim, dạng người đọc |
| `output/<slug>_preview.mp4` / `_pilot.mp4` / `_pilot.en.srt` | `preview` / `assemble` | Bản câm, bản có lời dẫn, phụ đề cấp câu |
| `qa/*.json`, `qa/M3_QA_REPORT.md`, `qa/gates.json` | các lệnh QA | Bằng chứng |

## Lệnh (tái tạo pilot)
```bash
# 0. OmniVoice (chỉ localhost; xem docs/integrations/OMNIVOICE.md)
cd ~/Work/Projects/OmniVoice && GRADIO_ANALYTICS_ENABLED=False HF_HUB_OFFLINE=1 \
  .venv/bin/omnivoice-demo --ip 127.0.0.1 --port 8001 --no-asr &
cd ~/Work/Projects/Architecture-Story-Studio
P=--project suffolk-roofs
python3 tools/cli.py tts-check $P        # dịch vụ, hợp đồng API, giọng, trạng thái license
python3 tools/cli.py narrate $P          # sinh theo câu (có cache) + audio từng beat (đo thời lượng)
python3 tools/cli.py asr-check $P        # Whisper offline: English + WER <= 0.15
python3 tools/cli.py schedule $P         # khóa timing -> timing.json + storyboard.json + SCRIPT_AND_STORYBOARD.md
python3 tools/cli.py check-blender $P    # QA Blender (66 kiểm tra)
python3 tools/cli.py smoke $P --shot SC_003   # thử đầu-cuối một beat/shot
python3 tools/cli.py preview $P          # render 640×360 (cache theo shot) + MP4 câm + media QA
python3 tools/cli.py assemble $P         # track lời dẫn + loudnorm + ghép + SRT + QA A/V
python3 tools/cli.py gates $P            # G0–G6 -> qa/gates.json
```
`narrate --regenerate` bỏ qua cache. Nếu `narration.json` thay đổi, `schedule` và `validate` sẽ báo khóa timing đã cũ.

## Quy tắc timing (narration-first)
- Mỗi câu được sinh riêng; beat = các câu + khoảng nghỉ cố định, ghép ở mức mẫu. Thời lượng đo bằng ffprobe; **không bao giờ ước lượng từ số chữ**.
- Shot = lead-in + beat + tail, **làm tròn lên** thành số nguyên frame. Shot chỉ được **nới dài** khi animation cần, không bao giờ co lại và không kéo giãn giọng (không dùng tham số `duration` của OmniVoice).
- Track lời dẫn dài đúng bằng video (24 kHz / 24 fps = 1000 mẫu mỗi frame). Ghép xong phải lệch ≤ 1 frame (pilot: 0 ms).
- Phụ đề: cấp câu, từ khoảng thời gian câu đo được. Không có timing theo từ (OmniVoice không cung cấp).

## Gate cho project có lời dẫn (M3)
| Gate | Lệnh kiểm tra | Ghi chú |
|---|---|---|
| G0 project & schema | `validate` | Gồm cả độ bao phủ beat, khóa timing còn mới, card |
| G1 bằng chứng & kịch bản | `gates` | PASS chỉ khi mọi claim được dẫn đều EDITORIALLY_APPROVED |
| G2 API OmniVoice & license giọng | `tts-check`, `asr-check`, `gates` | Đủ về kỹ thuật nhưng license chưa `APPROVED` → BLOCKED_LICENSE |
| G3 khóa timing | `schedule` | `locked` chỉ khi mọi câu đạt ASR |
| G4 preview Blender | `check-blender`, `preview` + xem frame | |
| G5 ghép video | `assemble` | lệch A/V, −16 ±1 LUFS, true peak ≤ −1 dBTP, SRT hợp lệ |
| G6 sẵn sàng xuất bản | `final-gate`, `gates` | Cần G1–G5 PASS + license `APPROVED` + asset đã duyệt + `factual_review: verified` |

Project chưa có lời dẫn (như `roof-evolution`) vẫn dùng gate G0–G5 của SOP 06.

## Mở rộng visual trong M3 (không thêm template animation mới)
- `covering.style`: `thatch` / `plain_tile` / `slate` (độ dày, gân theo hàng, ngói nóc dạng cuộn / nửa tròn / chữ V; vật liệu có texture thủ tục). Lớp phủ kiểu cũ của `roof-evolution` giữ nguyên.
- `structure_from`: variant chỉ sở hữu lớp phủ và kế thừa kết cấu (cùng độ dốc) → REPLACE chỉ thay lớp phủ.
- Shot `MOTION_GRAPHICS` (card): chữ + mũi tên tự dựng, font tích hợp của Blender, hiện dần theo mốc neo; dùng chung `motion.Plan`.
