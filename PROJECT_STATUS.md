# Current project status

- Phase: **M4: dựng hình kiến trúc thủ tục và thư viện asset. Xong phần kỹ thuật (2026-10-27) trên nhánh `m4-architectural-modeling`** (tách từ `m3.5-editorial-polish` `da5b603`; chưa merge, chưa push).
- **M4:** 3 họ cầu (timber_beam, stone_arch, steel_truss Pratt/Warren) và khu đất dùng chung, sinh từ 6 spec có ràng buộc; G4-A…E PASS; pilot kỹ thuật `projects/bridge-structure-evolution` 29.5 s (QA Blender 86/86, media QA PASS). Mọi asset là **ILLUSTRATIVE**.
- **M3.5 pilot `suffolk-roofs`:** không đổi. Vẫn là preview nội bộ: `TECHNICALLY_VALIDATED` · `EDITORIAL_REVIEW_PENDING` · `TTS_RIGHTS_PENDING`. OmniVoice NOT CLEARED cho xuất bản thương mại.
- Hồi quy: 138 unit test; QA Blender roof-evolution 63/63, suffolk-roofs 70/70, bridge-structure-evolution 86/86.
- Máy: macOS 26.6.2, **Apple M4 Pro 24 GB**, Blender 5.2.2 LTS, FFmpeg 9.0.1, Python 3.14.6.

## Lệnh tái tạo M4
```bash
python3 tools/cli.py asset-check                                   # G4-A + G4-B offline
python3 tools/cli.py asset-render --preset review                  # preview đa góc + QA BVH + build hai lần
python3 tools/cli.py asset-catalog                                 # asset_library/catalog/
python3 tools/make_bridge_pilot.py                                 # states/storyboard của pilot từ spec
P="--project bridge-structure-evolution"
python3 tools/cli.py validate $P && python3 tools/cli.py check-blender $P
python3 tools/cli.py preview $P                                    # 640×360 → output/bridge_structure_evolution_preview.mp4
python3 -m unittest discover -s tests                              # 138 test
```

## Việc người dùng cần quyết định
1. Xem pilot M4 và các preview asset (`asset_library/catalog/CATALOG.md`); chọn hướng cho M5.
2. Merge `m3.5-editorial-polish`, rồi `m4-architectural-modeling`, khi đã hài lòng (agent không merge, không push).
3. M3.5: các việc vẫn còn mở (duyệt biên tập, chọn giọng đọc dùng để xuất bản, nghe xác nhận phát âm "Babergh").

## Giới hạn đã biết
- Các mô hình cầu là minh họa; không có phân tích kết cấu. Chỉ có vòm bán nguyệt. Thanh giàn là thanh vuông.
- Khung so sánh ba cầu nhỏ ở 640×360. `layout: STACK` không hỗ trợ intro.
- Render của các project cũ sẽ chạy lại một lần nếu chạy `preview` (khóa cache v3); output đã kiểm chứng vẫn được giữ.
- Chưa kiểm tra trên Blender 4.5 LTS, cũng chưa đo trên máy M4 16 GB.
