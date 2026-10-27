# Hiệu năng M4 trên Mac (số đo thật, 2026-10-27)

**Máy đo:** Apple **M4 Pro**, bộ nhớ hợp nhất 24 GB, macOS 26.6.2, Blender 5.2.2 LTS (Eevee, raytracing, AgX). Spec M4 ghi máy chuẩn là "M4 / 16 GB"; mọi số liệu dưới đây đo trên M4 Pro 24 GB, nên trên M4 thường có thể sẽ chậm hơn.

Nguồn số liệu:
- `asset_library/catalog/qa/<asset>_<preset>.json`: `build_seconds` đo bằng `time.perf_counter` trong Blender; thời gian render từng góc nhìn; bộ nhớ đo bằng `/usr/bin/time -l` trên toàn bộ tiến trình Blender.
- `projects/bridge-structure-evolution/qa/render_SC_*_preview.log`: thời gian render tính từ dòng `UTC:` ở đầu log tới mtime của log.

Không có số nào là ước lượng.

## Dựng asset (một asset cùng khu đất, chưa render)
| Asset | Object | Mesh datablock | Đỉnh (đã evaluate, gồm bevel) | Thời gian dựng |
|---|---|---|---|---|
| `bridge_timber_beam_01` | 23 (20 của asset) | 11 (8) | 9 192 | 0.032 s |
| `bridge_stone_arch_03` | 52 (49) | 14 (11) | 4 466 | 0.032 s |
| `bridge_stone_arch_05` | 60 (57) | 14 (11) | 5 558 | 0.033 s |
| `bridge_steel_truss_pratt_01` | 32 (29) | 15 (12) | 8 128 | 0.033 s |
| `bridge_steel_truss_warren_01` | 28 (25) | 14 (11) | 7 008 | 0.031 s |

Dùng chung mesh: 36 voussoir của cầu 3 vòm dùng **1** mesh; 5 trụ cầu gỗ dùng 1 mesh; các nhịp giống nhau dùng chung mesh. Không thành phần nào bị "realize" (apply) lặp lại.

## Render ảnh tĩnh asset (một frame)
| Asset | 960×540: ba phần tư / mặt đứng / mặt bằng / bung | 1920×1080: ba phần tư / bung | Max RSS | Peak memory footprint |
|---|---|---|---|---|
| timber_beam_01 | 0.57 / 0.32 / 0.40 / 0.51 s | 1.36 / 1.25 s | 497–521 MB | 1.85–1.94 GB |
| stone_arch_03 | 0.54 / 0.33 / 0.41 / 0.52 s | 1.35 / 1.29 s | 507–531 MB | 1.86–1.95 GB |
| stone_arch_05 | 0.55 / 0.33 / 0.42 / 0.53 s | — | 509 MB | 1.87 GB |
| steel_truss_pratt_01 | 0.54 / 0.32 / 0.39 / 0.50 s | 1.26 / 1.27 s | 500–531 MB | 1.86–1.95 GB |
| steel_truss_warren_01 | 0.54 / 0.32 / 0.38 / 0.52 s | — | 496 MB | 1.85 GB |

Thời gian chạy trọn một lần `asset-render` (khởi động Blender, QA BVH, dựng hai lần, 4 góc nhìn): 2.5–3.4 s cho mỗi asset.

## Render animation pilot (640×360, 24 fps, 708 frame)
| Shot | Template | Frame | Thời gian | Giây/frame |
|---|---|---|---|---|
| SC_001 | HOLD + highlight | 72 | 27.7 s | 0.39 |
| SC_002 | EXPLODED_VIEW (cầu gỗ) | 132 | 52.5 s | 0.40 |
| SC_003 | HOLD + highlight | 72 | 28.5 s | 0.40 |
| SC_004 | EXPLODED_VIEW (cầu đá) | 144 | 57.5 s | 0.40 |
| SC_005 | HOLD + highlight | 72 | 27.8 s | 0.39 |
| SC_006 | REPLACE_PARTS (Pratt → Warren) | 96 | 45.1 s | 0.47 |
| SC_007 | SIDE_BY_SIDE STACK (3 cầu) | 120 | 118.6 s | 0.99 |
| **Tổng** | | **708** | **357.7 s** | 0.51 |

- Lần render đầy đủ đầu tiên (7 shot, encode, media QA) mất 358 s. Max RSS của cả cây tiến trình (tiến trình Blender lớn nhất): 506 MB.
- Shot một mô hình dựng cả 4 variant (3 đang ẩn) để camera khóa giống nhau giữa các shot: 105 mesh object, cộng mặt đất.
- Lần render lại sau khi đổi cách ghi `per_component`: chỉ SC_002 và SC_004 render lại (cache theo nhóm phụ thuộc), 5 shot còn lại dùng cache.

## Nhận xét
- Bộ nhớ không phải điểm nghẽn (khoảng 0.5 GB RSS). Thời gian render tăng gần tuyến tính theo số object hiển thị: SC_007 có 3 cầu nên khoảng 1 s/frame.
- Ở 640×360, một video 10 phút có độ phức tạp tương tự sẽ tốn khoảng 1 giờ render. Đây là phép ngoại suy từ số đo ở trên, chưa phải số đo.
- Không render 4K. Không render chuỗi frame 1080p: preset `production_test` từ chối mọi lệnh render chuỗi frame.
