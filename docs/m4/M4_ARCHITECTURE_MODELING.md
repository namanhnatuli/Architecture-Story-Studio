# M4: dựng hình kiến trúc thủ tục và thư viện asset tái sử dụng

**Spec kiến trúc → thành phần ngữ nghĩa → hình học Blender → QA hình ảnh → asset tái sử dụng.**

M4 **không** giải bài toán "sinh mọi công trình từ câu chữ tự nhiên". Hệ thống là một định dạng spec có ràng buộc và được kiểm tra chặt, hiện có 3 biến thể cầu (`timber_beam`, `stone_arch`, `steel_truss` với bụng giàn Pratt hoặc Warren) và một khu đất dùng chung (`site/river_crossing`). Mọi asset đều là **ILLUSTRATIVE**, tức là mô hình minh họa, không phải bản dựng lại một cây cầu thật và cũng không phải thiết kế kết cấu đã được chứng nhận.

## 1. Kiến trúc
```text
asset_library/architecture/<họ>s/<asset_id>.json        spec (schemas/architecture_asset.schema.json)
        │  engine/arch/assets.py  validate → resolve_params → compatibility_errors → plan
        ▼
engine/arch/families/bridge.py, site.py                 bộ sinh (thuần Python) dùng engine/arch/library.py + primitives.py
        ▼
[Component]  engine/arch/semantic.py                    id, type, material, group, variant, location/rotation,
        │                                               mesh cục bộ, layer, hint, animation, bevel, evidence
        ├─ engine/arch/checks.py (offline G4-B)         số lượng, kích thước, nối liền (AABB), giao cắt khối
        ▼
engine/arch/realize.py (bpy)                            1 object cho 1 thành phần; mesh trùng nhau → dùng chung 1 datablock;
        │                                               bevel và weighted normals là modifier; mỗi nhóm một collection
        ├─ engine/geometry.py  builder "architecture_asset" (base hoặc variant), cho engine M2/M3 dùng
        └─ engine/arch/asset_scene.py                   preview đa góc, QA BVH, build hai lần (G4-B/C/E)
```
Engine animation, camera khóa, cache và QA của M2/M3 được **dùng lại nguyên vẹn**. Engine chỉ thêm ba thứ:
- builder `architecture_asset` trong `spec.py` và `geometry.py`;
- tùy chọn `layout: "STACK"` (cùng `labels`) cho SIDE_BY_SIDE;
- camera orthographic tự lùi ra sau khi mép dưới khung nằm thấp hơn mặt đất.

## 2. Thành phần ngữ nghĩa
| Trường | Ý nghĩa |
|---|---|
| `id` | ID cục bộ ổn định, ví dụ `arch2_voussoir03` hoặc `span1_planks`. Khi lập kế hoạch, ID được thêm tiền tố variant (`stone_arch_arch2_voussoir03`). Chỉ gồm `[A-Za-z0-9_]` (dấu `.` dành cho tên object trong SIDE_BY_SIDE) |
| `type` | `SEMANTIC_TYPES`: FOUNDATION, ABUTMENT, PIER, SUPPORT, CAP_BEAM, BRACING, BEAM, STRINGER, FLOOR_BEAM, ARCH, VOUSSOIR, KEYSTONE, SPANDREL, DECK, PLANK, PARAPET, COPING, RAILING, TRUSS_CHORD, TRUSS_VERTICAL, TRUSS_DIAGONAL, END_POST, JOINT, BEARING, GROUND, WATER… (`role` là `type` viết thường) |
| `material` | khóa trong `asset_library/materials/stylized_materials.json` |
| `group` | nhóm ngữ nghĩa, cũng là collection trong Blender (`arch_2`, `truss_north`, `deck`…) |
| `variant` | variant sở hữu thành phần (`shared` cho khu đất) |
| `location` / `rotation` | gốc của thành phần (mét) và Euler XYZ (radian), đúng quy ước của Blender (có test ở cả hai phía) |
| `layer` / `hint` | thứ tự lắp ráp và hướng bung, dùng cho EXPLODED_VIEW |
| `animation` | `EXPLODE`, `HIGHLIGHT`, `REPLACE`, `STATIC`. `REPLACE` đánh dấu những phần khác nhau giữa hai variant tương thích |
| `evidence` | claim id (tùy chọn) |

Quy ước: đơn vị mét; X dọc theo nhịp, Y theo bề ngang, Z hướng lên. Mặt đất ở z = −0.38, khớp với nền của môi trường. Các phần lặp lại được gộp vào **một** thành phần (ví dụ 21 tấm ván của một nhịp), nên mỗi asset chỉ có 20–57 object thay vì hàng trăm. Riêng voussoir để mỗi viên một object, vì phải bung theo hướng bán kính; tất cả voussoir trong một asset dùng chung một mesh.

## 3. Định dạng spec (`schemas/architecture_asset.schema.json`)
```json
{"schema": "architecture_asset/1", "asset_id": "bridge_stone_arch_03", "family": "bridge", "variant": "stone_arch",
 "units": "METRIC", "generator": {"name": "bridge.stone_arch", "version": "1.0.0"},
 "parameters": {"total_length_m": 24, "deck_width_m": 4, "deck_level_m": 5, "arch_count": 3, "arch_type": "semicircular",
                "voussoirs_per_arch": 13, "...": "..."},
 "accuracy": "ILLUSTRATIVE", "provenance": {"basis": "...", "references": []},
 "animation_support": ["HOLD", "HIGHLIGHT", "EXPLODED_VIEW", "SIDE_BY_SIDE"]}
```
Validator kiểm tra:
- trường bắt buộc, họ và biến thể, đơn vị;
- tham số lạ, kiểu, khoảng giá trị, ràng buộc chẵn/lẻ (keystone ở đỉnh vòm nên số voussoir phải lẻ);
- tương thích hình học giữa các tham số: nhịp vòm > 0.5 m, trụ rộng hơn hai lần độ dày vòng vòm, ít nhất 0.15 m lớp đắp trên đỉnh vòm, góc thanh chéo của giàn…;
- `animation_support` phải nằm trong khả năng của bộ sinh;
- `REFERENCE_BASED` cần `references`; `HISTORICALLY_VERIFIED` cần `claim_ids`.

Trong project, khi variant asset đặt trên base là khu đất, validator còn kiểm tra hai cái phải khớp: chiều dài cầu với khe sông, cao độ mặt cầu với cao độ bờ.

## 4. Ba họ cầu (các asset cùng khe 24 m và mặt cầu ở cao độ 5.0 m, để so sánh tương đương)
| Asset | Thành phần (mesh khác nhau) | Hình học |
|---|---|---|
| `bridge_timber_beam_01` | 20 (8) | 5 trụ (3 cột, giằng chéo X), xà mũ, 4 dầm dọc mỗi nhịp, ván ngang (pitch 0.27 m), lan can. Đường truyền tải: ván → dầm dọc → xà mũ → cột |
| `bridge_stone_arch_03` / `_05` | 49 (11) / 57 (11) | Vòm bán nguyệt (cùng một bộ sinh, 3 hoặc 5 vòm), voussoir có khe mạch 12 mm, keystone nhô ra hai mặt và thòng xuống dưới mép trong vòm, trụ có mũi cản nước, mố, spandrel (đa giác khoét theo lưng vòm), mặt đường, lan can, gờ |
| `bridge_steel_truss_pratt_01` / `_warren_01` | 29 (17) / 25 (15) | Hai nhịp giàn pony (cao 2.2 m nên không có giằng trên; giằng trên chỉ có khi giàn cao ≥ 4.5 m), thanh biên song song, thanh đứng ở hai đầu, bản nút ở mọi nút, dầm ngang, bản mặt cầu, gối. Pratt: thanh đứng + thanh chéo dốc xuống về phía giữa nhịp; Warren: thanh chéo xen kẽ, không có thanh đứng bên trong (tam giác cân để dùng chung khung với Pratt) |

Nguồn cho mẫu giàn: Wikipedia "Truss bridge" (đọc ngày 2026-10-27). Hai claim tương ứng (CLM_001/002) ở trạng thái SOURCE_VERIFIED trong `projects/bridge-structure-evolution/research/sources.json`.

## 5. Gate M4
| Gate | Lệnh | Kiểm tra |
|---|---|---|
| G4-A spec | `asset-check`, `validate` | Spec hợp lệ, thành phần hợp lệ, tương thích với khu đất |
| G4-B hình học | `asset-check` (offline); `asset-render` (BVH) | Số lượng thành phần đúng như tham số, kích thước (dài 24 m, mặt cầu ở 5.0 m, chạm đất), tỷ lệ, không có phần trôi nổi, không có khối chồng nhau (AABB offline; BVH trên mesh đã evaluate: nối liền ≤ 3 cm, xuyên sâu > 4 mm ngoài các cặp đã thiết kế giao nhau) |
| G4-C hình ảnh | `asset-render --preset review` / `production_test` | Ba phần tư, mặt đứng (cắt sát), mặt bằng (cắt sát), dạng bung; xem trực tiếp ảnh và qua MCP `look` |
| G4-D animation | `validate` + `check-blender` trên `projects/bridge-structure-evolution` | HOLD + HIGHLIGHT, EXPLODED_VIEW, REPLACE_PARTS (Pratt → Warren trên cùng khung), SIDE_BY_SIDE STACK; khung hình, va chạm khi bung, điểm cắt |
| G4-E tái lập | `asset-render` (`reproducible_build`) | Dựng hai lần từ trạng thái sạch: chữ ký (tên, loại, vật liệu, nhóm, layer, transform, chữ ký mesh, đỉnh đã evaluate làm tròn 0.1 mm) phải giống hệt. Ảnh **không** đòi trùng từng bit (Eevee trên GPU, xem M3.5) |

## 6. Lệnh tái tạo
```bash
python3 tools/cli.py asset-check                          # G4-A + G4-B offline, cho mọi spec
python3 tools/cli.py asset-render --preset review         # preview 960×540 + QA Blender cho mọi asset
python3 tools/cli.py asset-render --preset production_test --asset asset_library/architecture/bridges/bridge_stone_arch_03.json
python3 tools/cli.py asset-catalog                        # asset_library/catalog/catalog.json + CATALOG.md
python3 tools/make_bridge_pilot.py                        # sinh lại states/storyboard của pilot từ spec + preset bung
P="--project bridge-structure-evolution"
python3 tools/cli.py validate $P && python3 tools/cli.py check-blender $P
python3 tools/cli.py still $P --preset review             # khung chính
python3 tools/cli.py preview $P                           # 640×360, 708 frame → output/bridge_structure_evolution_preview.mp4
python3 -m unittest tests.test_m4_arch tests.test_blender_m4
```

## 7. Thêm một họ công trình mới (ví dụ `aqueduct` hoặc `timber_truss`)
1. **Thành phần:** dùng các `SEMANTIC_TYPES` có sẵn. Chỉ thêm loại mới khi có một vai trò kiến trúc thật sự khác, và thêm cả test.
2. **Bộ sinh:** viết `engine/arch/families/<họ>.py` với các hàm `generator(params) -> [Component]`, chỉ dùng `library.py` và `primitives.py`. Đặt gốc của phần lặp lại tại tâm của nó (để mesh được dùng chung). ID cục bộ phải ổn định, gán `layer`, `hint`, `animation` (`REPLACE` cho những phần khác nhau giữa các variant dùng chung khung).
3. **Đăng ký:** khai báo trong `FAMILIES` (`engine/arch/assets.py`): `params` (kiểu, khoảng, mặc định), `materials`, `animation`, có thể thêm `replaceable_params`. Kiểm tra liên tham số đặt trong `compatibility_errors`; số lượng mong đợi đặt trong `checks.expected_counts`; preset bung đặt trong `explode_offsets`.
4. **Vật liệu:** thêm vào `asset_library/materials/stylized_materials.json` (chỉ thủ tục; nếu có texture ngoài thì ghi nguồn và license).
5. **Spec:** viết `asset_library/architecture/<họ>s/<id>.json`, mặc định `accuracy: ILLUSTRATIVE`.
6. Chạy `asset-check`, rồi `asset-render --preset review`; xem ảnh; sửa bộ sinh (không sửa scene); chạy `asset-catalog`.
7. Thêm test: số lượng, kích thước, tham số sai, hình học lặp lại (theo mẫu `tests/test_m4_arch.py`).

## 8. Giới hạn
- Ba biến thể cầu là minh họa. Kích thước được chọn cho dễ đọc, không có bất kỳ phân tích tải trọng hay kết cấu nào.
- Chỉ có vòm bán nguyệt (`arch_type`). Vòm cánh cung (segmental) và vòm nhọn chưa làm.
- Kiểm tra nối liền offline dùng AABB nên có sai số với phần bị xoay (voussoir); bản kiểm tra chính xác là BVH trong Blender.
- Phần bụng giàn là thanh vuông. Chưa có tiết diện chữ I, đinh tán hay chi tiết bản nút thật.
- `layout: STACK` không hỗ trợ `intro`. Khung so sánh ba mô hình vẫn nhỏ ở 640×360 (mỗi cầu khoảng 200 px chiều ngang).

## 9. Test
| File | Nội dung |
|---|---|
| `tests/test_m4_arch.py` (26) | spec và tham số sai, khớp schema, ID ổn định/duy nhất/có tiền tố, metadata ngữ nghĩa, số lượng và kích thước, phát hiện trôi nổi và chồng khối, primitive, quy ước góc quay, mẫu giàn Pratt/Warren (CLM_001/002), mesh dùng chung, sinh lặp lại, tham số hóa (3 hoặc 5 vòm), registry họ, vật liệu, pilot validate mọi template, kế thừa `structure_from`, preset bung khớp pilot, layout STACK, nạp asset trong project khác, khớp khu đất, cache phụ thuộc asset, phụ thuộc engine đệ quy |
| `tests/test_blender_m4.py` (5, cần Blender) | Python và Blender khớp nhau (góc quay, mesh chưa apply, bevel là modifier), 36 voussoir dùng 1 mesh, QA sạch + hai phép thử ngược (keystone bị đẩy xuyên, mặt cầu trôi nổi), dựng lại giống hệt, asset 5 vòm nạp qua `shot_builder` của một project khác |
