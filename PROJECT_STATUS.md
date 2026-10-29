# Current project status

- Phase: **M6: phim tài liệu có lời dẫn. Xong (2026-10-29).** Nhánh `m6-narrated-documentary` đã merge fast-forward vào `master` theo yêu cầu của chủ kênh (repo không có remote, không push).
- **Quyết định của chủ kênh (Tran Nam Anh), 2026-10-29:** cấp quyền xuất bản cho Kokoro; duyệt 14 claim (narration `m6-r2`); chấp nhận phát âm; giọng `bm_george`. Mọi gate G0–G6 + GV PASS. Profile vẫn `NARRATED_INTERNAL_REVIEW`: cần chuyển sang `PUBLICATION_CANDIDATE` + `publication_metadata` để đánh giá PUBLICATION_READY.
- **Pilot `bridge-load-explained`** "How Does a Bridge Carry Its Load?":
  - 8 beat, 14 claim EDITORIALLY_APPROVED (ODOT/FHWA/SCI/Yale);
  - 26 câu Kokoro **`bm_george`** (giọng do người dùng chọn ngày 2026-10-29; 143.4 wpm);
  - 11 shot, 151.33 s, 27 chú thích kỹ thuật;
  - QA Blender 176/176; media QA PASS; assemble −16.0 LUFS, 35 câu phụ đề (SRT + mov_text);
  - gate: G0–G6 + GV PASS, trạng thái `TECHNICALLY_VALIDATED`; kết luận "INTERNAL REVIEW — ALL GATES PASS" (chờ đổi profile).
  - Video: `projects/bridge-load-explained/output/bridge_load_explained_pilot_review.mp4` (lời dẫn PUBLICATION_CLEARED).
- **TTS:** Kokoro-82M được audit và **được chủ kênh cấp quyền xuất bản** (`PUBLICATION_CLEARED`, clearance 2026-10-29; các điểm mở của audit §5 vẫn ghi lại). Giọng kênh `bm_george`, license giọng APPROVED. OmniVoice không đổi (`INTERNAL_PREVIEW_ONLY`), không dùng cho M6.
- **Đa họ kiến trúc:** scene context (schema 3). Fixture cầu + mái: QA Blender 69/69. Dự án một họ giữ schema 2 giống hệt.
- **bridge-story-m5:** B7 đổi thành "Let's compare them one at a time: …"; bộ kiểm nhất quán báo CONSISTENT.
- **Suffolk-roofs:** không đổi: `TECHNICALLY_VALIDATED` · `EDITORIAL_REVIEW_PENDING` · `TTS_RIGHTS_PENDING`.
- Test: 250/250 (234 offline + 16 Blender). Đánh giá planner 29/29.
- Hồi quy QA Blender:

  | Dự án | QA Blender |
  |---|---|
  | bridge-story-m5 | 188/188 |
  | roof-plan-m5 | 52/52 |
  | suffolk-roofs | 71/71 |
  | roof-evolution | 64/64 |
  | bridge-structure-evolution | 92/92 |

  Các preview không lời đã render lại bằng engine M6 (media QA PASS).
- Máy: Apple M4 Pro 24 GB, Blender 5.2.2 LTS, FFmpeg 9.0.1, Python 3.14.6.

## Lệnh tái tạo M6
```bash
P="--project bridge-load-explained"
python3 tools/cli.py narrate $P && python3 tools/cli.py asr-check $P && python3 tools/cli.py align $P
python3 tools/cli.py lock-audio $P && python3 tools/cli.py plan-visuals $P && python3 tools/cli.py build-shots $P
python3 tools/cli.py check-blender $P --preset review
python3 tools/cli.py smoke $P --shot SC_003 --preset review
python3 tools/cli.py preview $P --preset review && python3 tools/cli.py assemble $P --preset review
python3 tools/cli.py still $P --preset production_test             # 11 still 1080p
python3 tools/cli.py research-map $P && python3 tools/cli.py gates $P --preset review
python3 -m unittest discover -s tests
```

## Việc người dùng cần quyết định (M6)
1. ~~Chọn giọng kênh~~, ~~cấp quyền xuất bản Kokoro~~, ~~duyệt 14 claim~~, ~~xác nhận phát âm~~, ~~merge vào master~~: đã xong ngày 2026-10-29.
2. Còn lại để đăng: chuyển `production_profile` sang `PUBLICATION_CANDIDATE` với `publication_metadata` (title, description, language, credits; nên ghi "AI-generated narration (Kokoro-82M)"), chạy lại `gates`, rồi render bản final nếu muốn độ phân giải cao hơn review 960×540.

## Lệnh tái tạo M5
```bash
P="--project bridge-story-m5"
python3 tools/cli.py plan-visuals $P        # visual_plan.json + qa/VISUAL_COVERAGE.md
python3 tools/cli.py validate-plan $P
python3 tools/cli.py build-shots $P         # states/storyboard/project.json
python3 tools/cli.py check-blender $P
python3 tools/cli.py still $P --preset review
python3 tools/cli.py preview $P             # 640×360 → output/bridge_story_m5_preview.mp4
python3 -m unittest tests.test_m5_planner tests.test_blender_m5
```

## Lệnh tái tạo M4
```bash
python3 tools/cli.py asset-check                                   # G4-A + G4-B offline
python3 tools/cli.py asset-render --preset review                  # preview đa góc + QA BVH + build hai lần
python3 tools/cli.py asset-catalog                                 # asset_library/catalog/
python3 tools/make_bridge_pilot.py                                 # states/storyboard của pilot từ spec
P="--project bridge-structure-evolution"
python3 tools/cli.py validate $P && python3 tools/cli.py check-blender $P
python3 tools/cli.py preview $P                                    # 640×360 → output/bridge_structure_evolution_preview.mp4
python3 -m unittest discover -s tests                              # toàn bộ test (docs/m5/M5_QA_REPORT.md §9)
```

## Giới hạn đã biết
- M6 (`docs/m6/M6_QA_REPORT.md` §7):
  - GHOST ván gỗ (B3) đúng về hình học nhưng khó thấy, vì ván và dầm cùng màu;
  - exploded view toàn mô hình có thể ra khỏi khung khi nhóm camera chỉ có một mô hình nhỏ (lỗi từ M5);
  - luật nhất quán dựa trên cụm từ gợi ý; trái/phải luôn UNCERTAIN;
  - chú thích chỉ gắn vào phần đứng yên;
  - chưa xác minh file font cụ thể đứng sau `<builtin>`.
- Render của các dự án cũ đã cũ theo khóa engine sau M6. Lần `preview` tới sẽ render lại; output đã kiểm chứng vẫn được giữ.
- M5.5: L1/L2 đo bằng lưới mẫu (không phải phần trăm bề mặt chính xác); proxy mái lệch tới khoảng 5 điểm; ngưỡng mới được hiệu chỉnh trên hai pilot; so sánh tuần tự ở B7 chỉ khoảng 2 s mỗi cầu; độ tương phản màu chưa được đo.
- M5: timing PROVISIONAL là ước lượng; chưa có template bản đồ / ảnh tư liệu / mũi tên lực; mỗi dự án chỉ một họ công trình. (Việc kiểm tra offline không xét vật che đã được giải quyết ở M5.5.)
- Các mô hình cầu là minh họa; không có phân tích kết cấu. Chỉ có vòm bán nguyệt. Thanh giàn là thanh vuông.
- Khung so sánh ba cầu nhỏ ở 640×360. `layout: STACK` không hỗ trợ intro.
- Render của các project cũ sẽ chạy lại một lần nếu chạy `preview` (khóa cache v3); output đã kiểm chứng vẫn được giữ.
- Chưa kiểm tra trên Blender 4.5 LTS, cũng chưa đo trên máy M4 16 GB.
