# Current project status

- Phase: **M3.5: duyệt biên tập, quyền TTS, hoàn thiện hình ảnh. Xong phần kỹ thuật (2026-10-27) trên nhánh `m3.5-editorial-polish`** (tách từ tag `m3-pilot-preview`; chưa merge, chưa push). M4 **chưa bắt đầu**.
- Pilot `projects/suffolk-roofs`: **75.542 s**, 6 shot, lời dẫn `m3.5-r1`, 21 cue phụ đề theo cụm từ, `output/suffolk_roofs_pilot_INTERNAL.mp4`.
- **Trạng thái: `TECHNICALLY_VALIDATED` · `EDITORIAL_REVIEW_PENDING` · `TTS_RIGHTS_PENDING`. Không sẵn sàng xuất bản.** G0/G3/G4/G5 PASS · G1 PENDING_EDITORIAL · G2 BLOCKED_RIGHTS · G6 BLOCKED (`projects/suffolk-roofs/qa/gates.json`).
- **OmniVoice: NOT CLEARED cho xuất bản thương mại** (trọng số CC-BY-NC). Chỉ dùng cho preview nội bộ. Xem `docs/licensing/TTS_LICENSE_AUDIT.md`.
- Không hồi quy: `roof-evolution` QA Blender 63/63; 107 unit test.
- Môi trường: macOS 26.6.2, Apple M4 Pro 24 GB, Blender 5.2.2 LTS, FFmpeg 9.0.1, Python 3.14.6, OmniVoice 0.1.5 (localhost:8001).

## Lệnh tái tạo (M3.5)
```bash
P="--project suffolk-roofs"
python3 tools/cli.py narrate $P            # cache: không sinh lại gì
python3 tools/cli.py asr-check $P
python3 tools/cli.py align $P              # timestamp theo từ (đã cache trong manifest)
python3 tools/cli.py schedule $P
python3 tools/cli.py check-blender $P      # 70 kiểm tra
python3 tools/cli.py preview $P            # 640×360, cache theo nhóm phụ thuộc hình ảnh
python3 tools/cli.py still $P --preset review           # 960×540
python3 tools/cli.py still $P --preset production_test  # ảnh tĩnh 1920×1080
python3 tools/cli.py assemble $P           # *_INTERNAL.mp4 + .en.srt + qa/SUBTITLE_QA.md
python3 tools/cli.py gates $P
python3 -m unittest discover -s tests      # 107 test
```

## Việc người dùng cần quyết định / làm
1. **Duyệt biên tập:** `projects/suffolk-roofs/review/EDITORIAL_APPROVAL_PACKAGE.md` (7 claim, câu chữ B1/B6, chữ trên màn hình, tiêu đề). Ghi `editorial_approval` theo hướng dẫn ở §9 của gói.
2. **Chọn giọng đọc để xuất bản:** Kokoro / Azure / Polly / ElevenLabs / giọng người thật (`TTS_LICENSE_AUDIT.md` §6). Agent không mua hay đăng ký gì.
3. **Nghe phát âm "Babergh":** `projects/suffolk-roofs/qa/pronunciation/PRONUNCIATION_TEST.md`.
4. Trả lời các câu hỏi Q1–Q5 trong audit (đặc biệt Q3: việc dùng OmniVoice nội bộ có được coi là phi thương mại không).
5. Merge `m3.5-editorial-polish` khi đã hài lòng. Quyết định phạm vi M4 (`docs/m3/M4_READINESS.md`).

## Giới hạn đã biết
- Audio hiện tại không được xuất bản; khi đổi provider thì timing và render sẽ chạy lại.
- Tốc độ đọc phụ đề 17–19.8 ký tự/giây ở 7 cue (do tốc độ đọc lời dẫn).
- Kích thước viên ngói/slate được cường điệu để dễ đọc (minh họa). Chưa kiểm tra trên Blender 4.5 LTS. Không có nhạc nền.
