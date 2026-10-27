# Báo cáo QA M3.5: Suffolk roofs

- Ngày: 2026-10-27. Nhánh `m3.5-editorial-polish`, tách từ tag `m3-pilot-preview` (`79375f9`). Chưa merge, chưa push.
- Môi trường: macOS 26.6.2, Apple M4 Pro, Blender 5.2.2 LTS, FFmpeg 9.0.1, Python 3.14.6, OmniVoice 0.1.5 (127.0.0.1:8001), Whisper large-v3-turbo (offline).
- **Kết luận: `TECHNICALLY_VALIDATED` + `EDITORIAL_REVIEW_PENDING` + `TTS_RIGHTS_PENDING`. Đây là preview nội bộ, không sẵn sàng xuất bản** (`qa/gates.json`).

## 1. Baseline M3 (đã kiểm chứng trước khi sửa)
Tag `m3-pilot-preview` khớp với `79375f9`; cây làm việc sạch. Output M3 được lưu tại `qa/baseline_m3/` (MP4, SRT, stills 640/960, contact sheet, manifest v1). MP4 M3 trong `output/` đã đổi tên thành `suffolk_roofs_pilot_M3_INTERNAL.mp4`, để không còn tên trông như bản phát hành.

## 2. Gate
| Gate | Trạng thái | Ghi chú |
|---|---|---|
| G0 project & schema | PASS | validate (gồm registry TTS, lexicon, hồ sơ duyệt) |
| G1 bằng chứng, kịch bản, phát âm | PENDING_EDITORIAL | 0/7 claim được duyệt (không tự duyệt); `factual_review: provisional`; PRON_001 chờ người nghe |
| G2 audio lời dẫn & quyền TTS | BLOCKED_RIGHTS | 14/14 câu đạt ASR; OmniVoice `INTERNAL_PREVIEW_ONLY`, license NOT_CLEARED |
| G3 khóa timing | PASS | 1813 frame (75.542 s), khóa |
| G4 preview Blender | PASS | QA Blender 70/70; media QA PASS (1813 frame, không frame đen, 5 điểm cắt: 1 liền mạch SSIM 1.0, 4 cắt cứng có khai báo) |
| G5 ghép video & phụ đề | PASS | −16.5 LUFS, true peak −1.3 dBTP, lệch A/V ≤ 1 frame, 21 cue, 0 lỗi phụ đề |
| G6 sẵn sàng xuất bản | BLOCKED | claim, license, nguồn gốc audio, phát âm, asset, factual_review |

## 3. Kiểm tra theo từng hạng mục
| Hạng mục | Kết quả | Bằng chứng |
|---|---|---|
| Audit license | OmniVoice NOT CLEARED (trọng số CC-BY-NC, trùng byte) | `docs/licensing/TTS_LICENSE_AUDIT.md` |
| Provider/hạng quyền | `narrate --purpose publication` → REFUSED; preview không bao giờ được dùng lại làm publication (test) | `config/tts_providers.json`, `tests/test_m35.py` |
| Giữ take M3 | 15/15 được nhận lại (đổi khóa) khi chưa sửa chữ, audio beat trùng từng byte; sau khi sửa lời dẫn, 9/14 câu vẫn dùng take M3 | `qa/baseline_m3/narration_manifest.v1.json` so với `audio/narration_manifest.json` |
| Gói duyệt biên tập | 7 claim, toàn văn lời dẫn, ký duyệt; rà soát trình tự tuyến tính | `review/EDITORIAL_APPROVAL_PACKAGE.md` |
| Phát âm | Override `[B EY1 B AH0]`; Whisper: "Baburg" (M3) → "Baber". **Chưa xác nhận** (cần người nghe) | `qa/pronunciation/` |
| ASR | 14/14 PASS, WER ≤ 0.111 | manifest `asr` |
| Phụ đề | 21 cue/14 câu, 7 ranh giới căn theo Whisper và đặt vào điểm năng lượng thấp nhất (−42 đến −76 dBFS), dòng dài nhất 41, 0 lỗi, 7 cảnh báo tốc độ đọc (17–19.8 ký tự/giây) | `qa/SUBTITLE_QA.md` |
| Hình ảnh | Hoa văn viên ngói/slate, nhãn, sửa lỗi xuyên mái slate; khung 960×540 và 1920×1080 | `output/stills_review/`, `output/stills_production_test/`, `qa/m35_before_after/` |
| QA Blender | suffolk 70/70; roof-evolution 63/63 (thêm 5 kiểm tra `covering_hides_structure`, không hồi quy) | `qa/blender_checks.json` |
| Phép thử ngược | Đưa slate về dày 0.025 → `covering_hides_structure` FAIL ở 3 shot; đưa nhãn về sâu 5.0 → `labels_in_band`: "hidden by ground" | log trong phiên làm việc |
| Cache render & tính tất định | Sau render: 6/6 CACHED. Render lại sau khi đổi `render_scene.py` (chỉ đổi phần parse tham số): hash file PNG luôn khác vì Blender ghi `Date`/`RenderTime`. So pixel đã giải mã: card 2D giống hệt; khung 3D lệch tối đa 1/255 ở dưới 0.01% số kênh (PSNR 81–104 dB), do Eevee raytracing trên GPU không cho kết quả bit-exact. So video M3.5 trước và sau: SSIM trung bình 0.99953, thấp nhất 0.99697. Kết luận: không có thay đổi nhìn thấy được | `qa/cache_report_preview.json`, `docs/m3/CACHE_DEPENDENCIES.md` |
| MCP | 7/7 lệnh (`mcp-for-blender` 2.2.4, safe mode) trên một Blender GUI riêng mở bản sao của SC_005/SC_006. Safe mode chặn `import os`. Nhãn đúng nội dung, `visible_shadow=False`. `ass_course_origin` = ±1.9535 (ngói), ±1.4683 (slate); material slate đọc thuộc tính này. Ảnh `look` của các frame 1/60/140/237 (SC_005) và 1/120/328 (SC_006) không phát hiện lỗi | `qa/mcp_m35/` |
| Unit test | 107/107 (77 cũ + 30 M3.5) | `python3 -m unittest discover -s tests` |

## 4. Lỗi phát hiện và sửa trong M3.5
1. **Tường hồi/đỉnh tường xuyên qua mái slate** (có từ M3, QA cũ không bắt được): tường hồi được dựng theo mặt dưới lớp phủ; slate dày 0.045; thêm kiểm tra mới.
2. **Nhãn SC_006 bị mặt đất che** khi đặt sâu: đặt sát camera; kiểm tra bằng tia.
3. **`check-blender` in ra báo cáo cũ** khi Blender bị lỗi: xóa báo cáo trước khi chạy và báo rõ "NO REPORT".
4. **QA layout SIDE_BY_SIDE** đọc `matrix_world` cũ của object bị ẩn (sai khi slot ngói không nằm giữa), và lỗi với slot đang mờ dần ở frame 1: chỉ dùng phần đang hiển thị, đo ở frame cuối.
5. **`audio_probe`** ném `KeyError` với WAV rỗng: nay báo `AudioValidationError`. Lỗi xuất hiện khi gửi riêng phiên âm `[B EY1 B AH0].` cho OmniVoice.
6. **`narrate` bị chặn khi khóa timing đã cũ** (vòng lặp: khóa cũ chỉ được cập nhật sau `narrate`): bỏ qua các lỗi thuộc bước sau `narrate`.
7. Gate từng dùng báo cáo media/ghép video cũ: G4/G5 nay so số frame với timing hiện tại.

## 5. Giới hạn còn lại
- Audio hiện tại **không được phép xuất bản**; mọi thời lượng sẽ đổi khi chuyển provider.
- Timestamp theo từ của Whisper là xấp xỉ; tốc độ đọc phụ đề ở mức 17–19.8 ký tự/giây.
- Kích thước viên ngói/slate được cường điệu (minh họa). Chưa kiểm tra trên Blender 4.5. Không có nhạc nền.
