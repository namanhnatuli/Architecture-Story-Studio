# Current project status

- Phase: **M5: lập kế hoạch hình ảnh tự động và điều phối storyboard → Blender. Xong phần kỹ thuật (2026-10-28) trên nhánh `m5-autonomous-visual-planning`** (tách từ `m4-architectural-modeling` `d0ee8c1`; chưa merge, chưa push).
- **M5:** `planner/` tất định (không LLM khi chạy): 9 ý đồ hình ảnh, chọn asset kèm lời giải thích, ánh xạ thành phần ngữ nghĩa, camera director, timing PROVISIONAL/AUDIO_LOCKED, báo cáo coverage, `plan-visuals` / `validate-plan` / `build-shots`. Pilot `projects/bridge-story-m5` "Three Ways to Span a Gap": 8/8 beat COVERED, 13 shot, 72.375 s, QA Blender 163/163, media QA PASS, **INTERNAL ONLY** (claim SOURCE_VERIFIED, chưa duyệt biên tập; không lời). Fixture SYNTHETIC `projects/roof-plan-m5` 52/52.
- **M4:** 3 họ cầu + khu đất, mọi asset ILLUSTRATIVE; pilot `bridge-structure-evolution` (SC_001 được sửa ở M5: ván ghost để dầm dọc nhìn thấy được), QA 92/92.
- **M3.5 pilot `suffolk-roofs`:** không đổi. Vẫn là preview nội bộ: `TECHNICALLY_VALIDATED` · `EDITORIAL_REVIEW_PENDING` · `TTS_RIGHTS_PENDING`. OmniVoice NOT CLEARED cho xuất bản thương mại; M5 không sinh audio mới.
- Hồi quy: xem `docs/m5/M5_QA_REPORT.md` §9; QA Blender roof-evolution 64/64, suffolk-roofs 71/71, bridge-structure-evolution 92/92.
- Máy: macOS 26.6.2, **Apple M4 Pro 24 GB**, Blender 5.2.2 LTS, FFmpeg 9.0.1, Python 3.14.6.

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

## Việc người dùng cần quyết định (M5)
1. Xem pilot M5 (`projects/bridge-story-m5/output/bridge_story_m5_preview.mp4`, `qa/review_stills.jpg`, `qa/VISUAL_COVERAGE.md`) và quyết định bước tiếp theo (M6).
2. Merge các nhánh `m3.5-editorial-polish` → `m4-architectural-modeling` → `m5-autonomous-visual-planning` khi đã hài lòng (agent không merge, không push).
3. Nội dung pilot M5: nếu muốn xuất bản, cần duyệt biên tập 5 claim và chọn giọng đọc đã được cấp quyền.
4. M3.5: các việc vẫn còn mở (duyệt biên tập, giọng đọc dùng để xuất bản, nghe xác nhận phát âm "Babergh").

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
- M5: timing PROVISIONAL là ước lượng; kiểm tra hiển thị offline không xét vật che (`check-blender` mới là kiểm tra chính xác); chưa có template bản đồ / ảnh tư liệu / mũi tên lực; mỗi dự án chỉ một họ công trình.
- Các mô hình cầu là minh họa; không có phân tích kết cấu. Chỉ có vòm bán nguyệt. Thanh giàn là thanh vuông.
- Khung so sánh ba cầu nhỏ ở 640×360. `layout: STACK` không hỗ trợ intro.
- Render của các project cũ sẽ chạy lại một lần nếu chạy `preview` (khóa cache v3); output đã kiểm chứng vẫn được giữ.
- Chưa kiểm tra trên Blender 4.5 LTS, cũng chưa đo trên máy M4 16 GB.
