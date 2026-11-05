# Báo cáo QA M4: dựng hình kiến trúc và thư viện asset

- Ngày: 2026-10-27. Nhánh `m4-architectural-modeling`, tách từ `m3.5-editorial-polish` (`da5b603`). Chưa merge, chưa push.
- Máy: Apple M4 Pro 24 GB, macOS 26.6.2, Blender 5.2.2 LTS, FFmpeg 9.0.1, Python 3.14.6.
- **Kết luận:** cả 3 họ cầu (5 asset) và khu đất đều sinh được từ spec, mang metadata ngữ nghĩa, đạt QA offline lẫn Blender, và dùng được với các template animation có sẵn. Pilot kỹ thuật 29.5 s đã render xong. Đây là **mô hình minh họa**, không phải phim tài liệu đã kiểm chứng sự thật.

## Gate M4
| Gate | Kết quả | Bằng chứng |
|---|---|---|
| G4-A spec | PASS: 6/6 spec hợp lệ; 11 loại spec sai đều bị từ chối, mỗi lỗi có thông báo riêng | `asset_library/catalog/offline_checks.json`, `tests/test_m4_arch.py` |
| G4-B hình học | PASS: offline 8/8 cho mỗi cầu (số lượng, kích thước, đặt trên mặt đất, tỷ lệ, không trôi nổi, không chồng khối); BVH trong Blender nối liền ≤ 3 cm, xuyên sâu ≤ 4 mm (ngoài các cặp đã thiết kế giao nhau) | `asset_library/catalog/qa/*_review.json` |
| G4-C hình ảnh | PASS sau 6 vòng sửa (mục 3); đã xem trực tiếp mọi ảnh và qua MCP | `asset_library/architecture/bridges/previews/*/{review,production_test}/*.jpg` |
| G4-D animation | PASS: QA Blender 86/86 trên 7 shot dùng HOLD + HIGHLIGHT, EXPLODED_VIEW (×2), REPLACE_PARTS (Pratt → Warren trên cùng khung), SIDE_BY_SIDE STACK. Media QA PASS, 3 điểm cắt liền mạch SSIM 1.0 | `qa/blender_checks.json`, `qa/preview_media_report.json` |
| G4-E tái lập | PASS: dựng hai lần từ trạng thái sạch cho chữ ký giống hệt (5/5 asset, cả hai preset). Render lại cho pixel lệch ≤ 1/255 (GPU, xem M3.5), không đòi trùng từng bit | `reproducible_build` trong `catalog/qa`, `tests/test_blender_m4.py` |

## 1. Asset
| Asset | Thành phần (mesh) | Ghi chú |
|---|---|---|
| `bridge_timber_beam_01` | 20 (8) | 4 nhịp, 5 trụ |
| `bridge_stone_arch_03` | 49 (11) | 3 vòm × 13 voussoir |
| `bridge_stone_arch_05` | 57 (11) | 5 vòm × 9 voussoir, cùng bộ sinh (thử tham số hóa) |
| `bridge_steel_truss_pratt_01` | 29 (12) | 2 nhịp giàn pony |
| `bridge_steel_truss_warren_01` | 25 (11) | Dùng chung khung Pratt, `REPLACE` chỉ thay phần bụng giàn |
| `site_river_crossing_24` | 3 (3) | Khu đất dùng chung (khe 24 m) |

## 2. MCP (`mcp-for-blender` 2.2.4, safe mode, chỉ localhost, instance GUI riêng mở bản sao của SC_004/006/007)
- 12/12 lệnh hợp lệ chạy được. Safe mode chặn `import subprocess`.
- Scene SC_004 có 49 object `stone_arch`, đúng số lượng theo loại; 36 voussoir dùng 1 mesh; bevel chưa apply; ba variant còn lại bị ẩn.
- `look` ở chế độ `frames` (SC_004/006/007) và `angles` có `target` là vòm số 2 (front/top/right/three_quarter): voussoir có mạch, keystone nhô ra, mũi cản nước trên trụ, mạch giữa vòng vòm và spandrel. Không phát hiện lỗi hình học.
- Hạn chế: `look` không có `target` sẽ khung theo cả mặt nền 320 m, nên ảnh không dùng được. Chế độ `views` và góc `iso` không tồn tại (thông báo lỗi của tool đã liệt kê các giá trị hợp lệ).
- Log: `qa/mcp_m4/calls1_log.json`, `calls2_log.json`.

## 3. Lỗi phát hiện và sửa (mọi thay đổi nằm trong module Python, không sửa tay trong scene)
1. **Bung cầu đá 0.8 m theo bán kính:** chân vòm đâm vào vòm kế bên và vào bờ, va với spandrel đang được nâng (QA `exploded_no_new_intersections`). Sửa: spandrel trượt ra sau; vòng vòm mở theo bán kính 0.35 m cộng 0.5 m đi lên. Đã tính khe hở: 0.78 m − 2×0.33 m = 0.12 m.
2. **Lan can phía nam bay về phía camera** và che các vòng vòm. Sửa: mọi khối khác ngoài vòm đều đi lên và ra sau; QA khung hình bắt và giúp chỉnh 3 lần các phần vượt khung (−3.2%, −2.9%, −0.8%).
3. **Kiểm tra chồng nhãn chỉ xét trục x** (sai với layout STACK). Sửa: xét chồng nhau theo cả hai trục.
4. **Dải xám ở đáy khung STACK:** mép dưới mặt phẳng camera orthographic thấp hơn mặt đất. Sửa: `fit_ortho` lùi camera dọc theo hướng nhìn (với phép chiếu orthographic thì hình chiếu không đổi).
5. **Ảnh mặt đứng có nền world xám tối:** cắt sát mô hình, render nền trong suốt rồi ghép lên màu nền khi xuất JPEG. Lần đầu ra nền đen vì PNG ghi ở RGB; sửa bằng RGBA.
6. **BVH báo dương tính giả** với các mặt chạm nhau đồng phẳng (bờ/mố). Sửa: chỉ tính là giao cắt khi có độ xuyên sâu. Có test chứng minh vẫn bắt được keystone bị đẩy xuyên và mặt cầu trôi nổi.
7. **Tỷ lệ giàn:** cao 2.6 m trên nhịp 11.15 m bị kiểm tra tỷ lệ từ chối. Đổi thành giàn pony 2.2 m (không có giằng trên; giằng trên chỉ khi giàn ≥ 4.5 m).
8. **Bờ quá nặng nề:** dài 4 m → 2.2 m, rộng 12 m → 8 m, tông màu nhẹ hơn.

## 4. Hồi quy
- Unit test 138/138: 107 cũ + 26 `test_m4_arch` + 5 `test_blender_m4`.
- QA Blender: roof-evolution 63/63, suffolk-roofs 70/70.
- Trạng thái xuất bản của suffolk-roofs **không đổi**: `TECHNICALLY_VALIDATED`, `EDITORIAL_REVIEW_PENDING`, `TTS_RIGHTS_PENDING`.
- Cache render của project cũ báo "key v2: one-time re-render" (thay đổi engine và nhóm `assets` mới). Output M3.5 đã kiểm chứng được giữ nguyên, không render lại.

## 5. Output
- Pilot: `output/bridge_structure_evolution_preview.mp4` (708 frame, 640×360).
- Khung hình: `output/stills` (640), `output/stills_review` (960), `output/stills_production_test` (1920×1080, 7 khung chính).
- Scene: `scenes/SC_00x.blend`.
- Asset: `asset_library/architecture/bridges/previews/<asset>/{review,production_test}/`.
- Catalog: `asset_library/catalog/{catalog.json, CATALOG.md}`.
- Hiệu năng: `docs/m4/M4_PERFORMANCE.md`.

## 6. Giới hạn
Xem `docs/m4/M4_ARCHITECTURE_MODELING.md` §8. Tóm tắt:
- chỉ minh họa, chưa có phân tích kết cấu;
- chỉ có vòm bán nguyệt;
- thanh giàn là thanh vuông;
- khung so sánh ba cầu còn nhỏ ở 640×360;
- STACK không hỗ trợ intro;
- kiểm tra nối liền offline dùng AABB (bản chính xác là BVH).
