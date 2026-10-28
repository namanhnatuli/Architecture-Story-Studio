# Current project status

- Phase: **M5.5: trí tuệ hình ảnh, bố cục thích ứng, profile sản xuất. Xong phần kỹ thuật (2026-10-28) trên nhánh `m5.5-visual-intelligence`** (tách từ `m5-autonomous-visual-planning` `92a76ac`; chưa merge, chưa push).
- **M5.5:**
  - Mức nhìn thấy L1 offline (`planner/visibility.py`) và L2 trong Blender (`verify-visibility`): 5 dự án, kết luận trùng 100 %.
  - Sửa kế hoạch tự động (`planner/repair.py`): GHOST cho dầm dọc bị che, REFRAME cho đòn nóc nhỏ.
  - Bố cục so sánh được đo (`planner/composition.py`): B7 chuyển sang so sánh tuần tự, cùng camera, cùng tỷ lệ.
  - CLOSEUP_EXPLODE chính diện cho voussoir.
  - `production_profile` cho 5 dự án.
  - Bộ đánh giá 24/24.
  - 207 test.
- **Pilot `bridge-story-m5`:** 15 shot, 72.375 s, QA Blender 188/188, media QA PASS, **TECHNICAL PREVIEW — VALID (silent); NOT FOR PUBLICATION** (claim SOURCE_VERIFIED, chưa duyệt biên tập).
- **M3.5 `suffolk-roofs`:** NARRATED_INTERNAL_REVIEW, không đổi: `TECHNICALLY_VALIDATED` · `EDITORIAL_REVIEW_PENDING` · `TTS_RIGHTS_PENDING`. OmniVoice NOT CLEARED.
- Hồi quy: QA Blender roof-evolution 64/64, suffolk-roofs 71/71, bridge-structure-evolution 92/92, roof-plan-m5 52/52. Các preview không lời đã được render lại bằng engine M5.5 (Suffolk không cần, vì gate của nó tính theo timing đã khóa).
- Máy: macOS 26.6.2, **Apple M4 Pro 24 GB**, Blender 5.2.2 LTS, FFmpeg 9.0.1, Python 3.14.6.

## Lệnh tái tạo M5.5
```bash
P="--project bridge-story-m5"
python3 tools/cli.py plan-visuals $P && python3 tools/cli.py build-shots $P
python3 tools/cli.py check-blender $P && python3 tools/cli.py verify-visibility $P
python3 tools/cli.py preview $P && python3 tools/cli.py gates $P
python3 tools/cli.py evaluate-planning
python3 -m unittest discover -s tests                              # 207 test
```

## Việc người dùng cần quyết định (M5.5)
1. Xem `projects/bridge-story-m5/output/bridge_story_m5_preview.mp4` và `qa/m55_before_after/`. Quyết định có sửa lời thoại B7 ("Side by side" trong khi hình trình bày tuần tự) hay không.
2. Merge các nhánh theo thứ tự M3.5 → M4 → M5 → M5.5 khi đã hài lòng (agent không merge, không push).
3. M6 (`docs/m5_5/M6_READINESS.md`): chọn dịch vụ hoặc người đọc lời dẫn có quyền thương mại; duyệt pilot đề xuất.
4. M3.5: các việc vẫn còn mở (duyệt biên tập, giọng đọc dùng để xuất bản, nghe xác nhận phát âm "Babergh").

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
- M5.5: L1/L2 đo bằng lưới mẫu (không phải phần trăm bề mặt chính xác); proxy mái lệch tới khoảng 5 điểm; ngưỡng mới được hiệu chỉnh trên hai pilot; so sánh tuần tự ở B7 chỉ khoảng 2 s mỗi cầu; độ tương phản màu chưa được đo.
- M5: timing PROVISIONAL là ước lượng; chưa có template bản đồ / ảnh tư liệu / mũi tên lực; mỗi dự án chỉ một họ công trình. (Việc kiểm tra offline không xét vật che đã được giải quyết ở M5.5.)
- Các mô hình cầu là minh họa; không có phân tích kết cấu. Chỉ có vòm bán nguyệt. Thanh giàn là thanh vuông.
- Khung so sánh ba cầu nhỏ ở 640×360. `layout: STACK` không hỗ trợ intro.
- Render của các project cũ sẽ chạy lại một lần nếu chạy `preview` (khóa cache v3); output đã kiểm chứng vẫn được giữ.
- Chưa kiểm tra trên Blender 4.5 LTS, cũng chưa đo trên máy M4 16 GB.
