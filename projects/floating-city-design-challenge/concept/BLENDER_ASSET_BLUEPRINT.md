# Bản thiết kế asset thủ tục: họ "floating" và site "bay"

**Theo đúng đường của Studio (M4):** spec `asset_library/architecture/floating/*.json` (`schema: architecture_asset/1`) → bộ sinh Python thuần `engine/arch/families/floating.py` → `realize.py` dựng trong Blender. Không dựng tay một thành phố khối liền. Mesh giống nhau dùng chung một datablock (`realize.py` đã làm vậy), nên quận khoảng 200 phao vẫn chỉ vài chục mesh.

**Quy ước có sẵn** (đã kiểm trong mã, `engine/arch/semantic.py`):
- **Component:** `id` viết thường (`p01_hull_bottom`), `type` viết hoa trong `SEMANTIC_TYPES`, `material`, `group` số nhiều (`hulls`, `bulkheads`), `layer` (thứ tự lắp), `animation` (EXPLODE / HIGHLIGHT / REPLACE / STATIC), `evidence`, `meta`.
- **Spec:** `accuracy: "ILLUSTRATIVE"`, `provenance.basis`, `animation_support` (planner trả MISSING_TEMPLATE khi thiếu SEQUENCE).

**Prototype đã chứng minh hình học tối thiểu:** `prototype/floating_prototype.py` dựng được thân phao có khoang, mặt cắt, nước trừ thân phao, cọc, dây neo, cầu đi bộ. Prototype không gắn vào engine. Bản sản xuất phải viết lại thành bộ sinh, không sao chép tọa độ.

## Ánh xạ tên của brief sang loại ngữ nghĩa

| Brief | `type` đề xuất | Có sẵn? | Ghi chú |
|---|---|---|---|
| PLATFORM_HULL | `HULL` | mới | thân phao (đáy, tường bao) |
| PLATFORM_DECK | `DECK` | **có** | sàn trên của phao |
| WATERTIGHT_COMPARTMENT | `BULKHEAD` | mới | vách ngăn; "khoang" là khoảng giữa vách, nhấn bằng HIGHLIGHT vách quanh nó |
| RESIDENTIAL_BLOCK | `BUILDING` | mới | khối nhà thấp tầng; vạch tầng, mái phẳng; dùng `WALL`/`ROOF` có sẵn cho chi tiết |
| CONNECTOR_BRIDGE | `WALKWAY`, `CONNECTOR` | mới | cầu đi bộ qua khe; khớp (khái niệm) |
| MOORING_LINE | `MOORING_LINE` | mới | ống mảnh theo đường vẽ sẵn, không tính độ võng |
| SEABED_ANCHOR | `ANCHOR` | mới | khối tượng trưng, NOTE "not sized" |
| (cọc) | `MOORING_PILE` | mới | ống thép đứng, vòng dẫn trượt |
| BREAKWATER | `BREAKWATER` | mới | hai biến thể: cố định (đá đổ) và nổi (hộp) |
| WATER_SUPPLY, WASTEWATER_ROUTE, ELECTRICAL_DISTRIBUTION | `UTILITY_LINE` (+ `meta.network`) | mới | một loại, ba mạng; màu theo mạng |
| EMERGENCY_ACCESS | `ACCESS_ROUTE` | mới | dải đường đi được nhấn khi cần |
| (cầu nối bờ) | `LINK_SPAN` | mới | cầu có khớp ở bờ |
| (đáy biển) | `GROUND` | **có** | đáy, có dốc tùy chọn |
| (nước) | `WATER` | **có** | thêm khả năng cắt mặt và làm mờ hai bước |

Thêm loại mới vào `SEMANTIC_TYPES` là thay đổi nhỏ. Mỗi loại mới cần một khái niệm trong `config/visual_vocabulary.json` để planner gọi được (ví dụ `floating_platform`, `mooring_line`, `breakwater`).

## Họ A: môi trường biển (site `bay`)

- **Biến thể:** `site.bay` (mới), tham số:
  - `basin_width_m`, `basin_length_m`, `water_depth_m` (12–25), `seabed_slope`, `shore_side`, `quay_height_m`;
  - `section_plane`: `null`, hoặc `{axis: "y", keep: "positive"}`.
- **Thành phần:**
  - `water` (WATER): khối nước **trừ** chân phao. Dựng thành các khối như prototype, để mặt cắt không có nước bên trong thân phao.
  - `water_surface` (WATER): tấm mỏng riêng cho bước "thấy mặt nước, rồi làm mờ".
  - `seabed` (GROUND), `shore` và `quay` (GROUND).
  - `section_poche_*`: tấm mặt cắt tối đặt trên mặt cắt.
- **Sóng:** **không** mô phỏng chất lỏng. Mặt nước tĩnh có bump nhẹ (`stylized_materials.json` → `water`). Sóng khái niệm (SH19) là chuyển động tất định của các phao, không phải của nước (xem năng lực mới `CONCEPT_MOTION`).
- **Độ khó:** S (dựa trên `site.river_crossing`). **Dùng lại:** cao (mọi phim về cảng, đê, cầu nổi).

## Họ B: phao

- **Biến thể:**
  - `floating.box_pontoon`;
  - `floating.semi_sub_module` (chỉ cho Design D, sơ đồ đơn giản: sàn trên cột trên phao chìm, CLM_062).
- **Tham số `box_pontoon`:**
  - kích thước và kết cấu: `length_m`, `width_m`, `hull_depth_m`, `slab_m`, `wall_m`, `bulkhead_spacing_m`, `bulkhead_m`;
  - `draft_m`: **lấy từ `analysis/results.json`**; spec ghi `provenance.draft_source`;
  - `footprint`: `rect`, `l_shape` hoặc `polygon` (không ép lục giác);
  - `section_plane`.
- **Thành phần** (ví dụ phao `p01`):
  - `p01_hull_bottom`, `p01_hull_wall_{n,e,s,w}` (HULL);
  - `p01_bulkhead_x{i}`, `p01_bulkhead_y{j}` (BULKHEAD);
  - `p01_deck` (DECK);
  - `p01_displaced_volume` (HIGHLIGHT-only, vàng trong suốt; chỉ hiện trong shot Archimedes);
  - `p01_waterline` (đường mảnh), `p01_draft_gauge` (thước 1 m, cho SH09).
- **Kiểm tra chéo** (như `assets.compatibility_errors`):
  - `draft_m < hull_depth_m`;
  - vách ngăn chia hết kích thước;
  - tâm khối bê tông nằm trong thân;
  - chênh mớn nước so với `results.json` > 1 mm thì báo lỗi, không tự sửa.
- **Độ khó:** M. **Dùng lại:** cao (phao, bến nổi, nhà nổi).

## Họ C: mối nối

- **Biến thể:** `floating.gap_connector`, `floating.link_span`.
- **Thành phần:**
  - `c01_walkway` (WALKWAY);
  - `c01_hinge_{a,b}` (CONNECTOR, hình khái niệm: trục và tấm);
  - `c01_utility_flex` (UTILITY_LINE, đoạn cong mềm qua khe);
  - `c01_fender` (CONNECTOR).
- **Link-span:** `ls01_deck`, `ls01_shore_hinge`, `ls01_float_bearing`.
- **Quy tắc:** chi tiết cơ khí chỉ là khái niệm (NOTE "conceptual geometry"). Không vẽ bu lông hay kích thước như đã thiết kế.
- **Độ khó:** S. **Dùng lại:** trung bình.

## Họ D: neo

- **Biến thể:** `floating.pile_mooring`, `floating.line_mooring`.
- **Thành phần:**
  - `m01_pile` (MOORING_PILE), `m01_guide` (CONNECTOR: vòng dẫn trên thân phao);
  - `m01_line` (MOORING_LINE, đường đa đoạn theo một hình vẽ sẵn);
  - `m01_anchor` (ANCHOR).
- **Quy tắc:**
  - Độ võng dây là **hình vẽ**, không phải nghiệm catenary.
  - Không gán kích thước neo hay loại neo cụ thể.
  - NOTE "Conceptual mooring — not sized" trên mọi shot có neo.
- **Độ khó:** S. **Dùng lại:** cao.

## Họ E: nhà

- **Biến thể:** `floating.lowrise_block` (tham số `storeys` 2–4, `footprint`, `roof`: flat hoặc green), `floating.community_hall`, `floating.service_building`, `floating.clinic`.
- **Thành phần:**
  - `b01_volume` (BUILDING);
  - `b01_floor_bands` (DECORATION);
  - `b01_roof` (ROOF);
  - `b01_pv` (SOLAR_ARRAY, tùy chọn).
- **Quy tắc:**
  - Không cửa sổ chi tiết, không nội thất, không người.
  - Biến thể bằng tham số (số tầng, kích thước, mái), không bằng mô hình tay.
  - Số tầng đổi phải khớp với mớn nước tính sẵn (B).
- **Độ khó:** S. **Dùng lại:** cao.

## Họ F: hạ tầng

- **Biến thể:** `floating.utility_network` (sinh từ đồ thị phao và cầu), `floating.boat_landing`, `floating.breakwater_fixed`, `floating.breakwater_floating`.
- **Thành phần:**
  - `u_power_*`, `u_water_*`, `u_waste_*` (UTILITY_LINE với `meta.network`);
  - `u_pump_*` (CONNECTOR);
  - `access_*` (ACCESS_ROUTE);
  - `landing_*`;
  - `bw_*` (BREAKWATER).
- **Màu theo mạng:** nằm trong `config/annotation_style.json`, phân biệt với màu kết cấu. Luật của Studio: vật thể thật và khái niệm (lực, dòng) có ngôn ngữ hình khác nhau.
- **Độ khó:** M (đồ thị mạng). **Dùng lại:** trung bình.

## Họ K: card và sơ đồ (2D)
Dùng `engine/diagram.py` có sẵn (text, arrow, rect, line, circle, polygon, image; phần tử theo từ; stage camera). Sơ đồ mới cần: thang quy mô, lưới mặt bằng có chấm hiện dần, mặt cắt G/B/M, sóng dài qua đê, hai vịnh. Tất cả vẽ được bằng phần tử hiện có. **Độ khó:** S.

## Planner phải làm được gì với các thành phần này

| Yêu cầu của brief | Cách làm trong Studio |
|---|---|
| Nhấn một bộ phận | HIGHLIGHT, SEQUENCE.HIGHLIGHT (có sẵn) |
| Tách riêng | SEQUENCE.FADE_OUT các nhóm khác (có sẵn) |
| Làm mờ vật che | SEQUENCE.GHOST (có sẵn); sửa bố cục tự động của planner (`planner/repair.py`, M5.5) áp được cho loại mới khi có mục tiêu tầm nhìn |
| Mặt cắt | tham số `section_plane` của bộ sinh (mới, nhỏ); cách giống mô hình mặt cắt nhà thờ |
| So sánh phiên bản | REPLACE_PARTS, SIDE_BY_SIDE, DETAIL_THEN_OVERVIEW (có sẵn) |
| Hoạt ảnh thay đổi liên quan | REVEAL (có sẵn); **mới:** `SINK`/`RISE` (tịnh tiến z một nhóm theo Δ tính sẵn), `CONCEPT_MOTION` (dao động hình sin tất định, lệch pha theo module, có nhãn bắt buộc) |
| Gắn chú thích | `planner/annotations.py`, COMPONENT_LABEL (có sẵn) |
| Kiểm tra tầm nhìn | `verify-visibility` (Blender ray cast, có sẵn); thêm mục tiêu cho loại mới |

## Ước lượng công sức dựng
- **Tổng:** khoảng 6–8 phiên làm việc của agent cho họ A–F cùng test và catalog. Đây là ước lượng theo kinh nghiệm các họ cầu và nhà thờ, không phải đo.
- **Phần tốn nhất:** họ F (đồ thị mạng) và site `bay` có mặt cắt.
- **Năng lực hoạt ảnh mới:** khoảng 2 phiên, chi tiết ở `PRODUCTION_FEASIBILITY.md`.
