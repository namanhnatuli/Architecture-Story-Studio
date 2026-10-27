# Current project status

- Phase: **M3 — pipeline phim có lời dẫn + OmniVoice cục bộ: hoàn tất về kỹ thuật (2026-10-27), trên nhánh `m3-narrative-pipeline`** (tách từ tag `m2.5-validated`, chưa merge, chưa push).
- Pilot `projects/suffolk-roofs` — *"Why Did Traditional Roofs in Suffolk Change?"*: **73.0 s**, 6 beat → 6 shot (SIDE_BY_SIDE, EXPLODED_VIEW, REPLACE_PARTS ×2, card 2D, SIDE_BY_SIDE + intro), lời dẫn tiếng Anh do OmniVoice sinh, phụ đề cấp câu.
- **Kết luận: PREVIEW NỘI BỘ ĐỂ DUYỆT — CHƯA SẴN SÀNG XUẤT BẢN.** G0/G3/G4/G5 PASS · G1 PENDING_EDITORIAL · G2 BLOCKED_LICENSE · G6 BLOCKED (`qa/gates.json`).
- Pilot cũ `projects/roof-evolution` (M2/M2.5) không hồi quy: QA Blender 58/58.
- Môi trường đã kiểm chứng: macOS 26.6.2, Apple M4 Pro 24 GB, Blender 5.2.2 LTS, FFmpeg 9.0.1, Python 3.14.6, OmniVoice 0.1.5 (localhost:8001).

## Lệnh tái tạo pilot M3
Xem đầy đủ trong `docs/m3/M3_PIPELINE.md`. Tóm tắt:
```bash
python3 tools/cli.py tts-check --project suffolk-roofs
python3 tools/cli.py narrate   --project suffolk-roofs     # dùng lại các take đã commit (cache)
python3 tools/cli.py asr-check --project suffolk-roofs
python3 tools/cli.py schedule  --project suffolk-roofs
python3 tools/cli.py preview   --project suffolk-roofs     # 640×360
python3 tools/cli.py assemble  --project suffolk-roofs     # output/suffolk_roofs_pilot.mp4 + .en.srt
python3 tools/cli.py gates     --project suffolk-roofs
python3 -m unittest discover -s tests                      # 77 test
```

## Đã làm / đã kiểm chứng / còn chờ
| Hạng mục | Trạng thái |
|---|---|
| Adapter OmniVoice (`integrations/tts/omnivoice.py`) | ✅ đã làm · ✅ 10 test (server giả lập) · ✅ đã chạy thật với 14 câu + giọng mẫu |
| Cache audio, kiểm tra tốc độ/độ lớn, sinh lại khi lỗi, ASR | ✅ · ✅ test · ✅ 14/14 ASR PASS |
| Lập lịch narration-first, khóa timing, mốc neo | ✅ · ✅ test · ✅ 1752 frame, 0 shot phải nới cho animation |
| Lớp phủ thatch / ngói / slate, `structure_from`, card 2D | ✅ · ✅ QA Blender 66/66 · ✅ đã xem frame + MCP |
| Ghép video (loudnorm, ghép, SRT, QA A/V) | ✅ · ✅ test · ✅ lệch 0 ms, −16.5 LUFS |
| Sổ bằng chứng (SOURCE_VERIFIED) | ✅ · ⏳ **duyệt biên tập (G1) do người làm** |
| License giọng đọc | ⏳ **LICENSE_REVIEW_REQUIRED** (Boson Higgs Audio 2 License trong tokenizer của OmniVoice) |
| MCP: xung đột scope | ✅ đã xử lý (chỉ còn scope project, bản 2.2.4, safe mode) · ✅ tool + safe mode đã kiểm chứng |

## Việc người dùng cần quyết định / làm
1. **G1:** duyệt `projects/suffolk-roofs/research/RESEARCH_REPORT.md` và câu chữ trong `script/SCRIPT_AND_STORYBOARD.md`; chuyển claim sang `EDITORIALLY_APPROVED`.
2. **Phát âm "Babergh"** (Whisper nghe thành "Baburg").
3. **G2:** review license Boson / dữ liệu huấn luyện → đổi `narration.voice.license.status`.
4. Khởi động lại Claude Code và phê duyệt server MCP của project (lúc đó sẽ có tool MCP gốc).
5. Merge nhánh `m3-narrative-pipeline` khi đã hài lòng (agent không merge, không push).

## Giới hạn đã biết
- Phụ đề cấp câu (dòng dài tới 67 ký tự); muốn tách cue cần căn chỉnh theo từ.
- Đường hàng ngói/slate chỉ hiện mờ ở 640/960; mô hình là minh họa.
- Sửa câu chữ của shot vẫn kích hoạt render lại (khóa cache băm toàn bộ JSON của shot).
- Chưa kiểm tra trên Blender 4.5 LTS. Không có nhạc nền.
