# SOP 05 — Thư viện template animation

| Template | Công dụng | Điều kiện | Trạng thái (M2, 2026-10-26) |
|---|---|---|---|
| `HOLD` | Giữ một state, có thể highlight | 1 state | **Đã triển khai + test + kiểm tra hình ảnh** |
| `REPLACE_PARTS` | A ra, B vào | Nhóm component nguồn + đích, cùng tọa độ | **Đã triển khai + test + kiểm tra hình ảnh** |
| `EXPLODED_VIEW` | Tách lớp để giải thích | Nhóm component có ngữ nghĩa | **Đã triển khai + test + kiểm tra hình ảnh** |
| `SIDE_BY_SIDE` | 2+ mô hình đặt ngang hàng | Cùng scale/camera/ánh sáng | **Đã triển khai + test + kiểm tra hình ảnh** |
| `HIGHLIGHT_DIFFERENCE` | Chỉ ra phần thay đổi | Không tô cấu kiện giống nhau | Một phần: tùy chọn `highlight` trong HOLD / EXPLODED_VIEW / SIDE_BY_SIDE |
| `ASSEMBLE`, `DISASSEMBLE` | Cấu kiện vào / ra | Object IDs + target transforms | Chưa hỗ trợ dạng template riêng (dùng nửa vào / nửa ra của REPLACE_PARTS) |
| `STATE_TRANSITION`, `CUTAWAY`, `CAUSE_AND_EFFECT`, `TIMELINE` | — | — | Chưa hỗ trợ (V2) |

## Kiến trúc (M2)

```text
storyboard.json shot.animation ──► engine/templates.py ──► engine/motion.py ──► Plan (keyframes)
states.json ownership ───────────► engine/spec.py           (Python thuần, không bpy)   │
                                                                                         ▼
engine/geometry.py (builders) ──► engine/shot_builder.py ──► engine/animate.py ──► Blender keys
                                   engine/framing.py (camera + layout, Python thuần)
```

- **Planning là Python thuần.** `tools/validator.py` chạy cùng planner với geometry giữ chỗ, nên lỗi timing / component / option bị bắt ngay ở G0, trước khi Blender khởi động.
- **Geometry không biết gì về animation.** Builder chỉ gắn metadata: `component_id`, `variant_id`, `role`, `group`, `assembly_layer`, `explode_hint`.
- **Mọi keyframe có interpolation tường minh.** Không phụ thuộc BEZIER mặc định; `Plan.sample()` tái tạo đúng đường cong Blender (sai số đo được < 1e-6).
- **Không bao giờ thu nhỏ scale để làm biến mất.** Biến mất = di chuyển + mờ dần (`ass_transparency`) + `hide_render`.
- **Mỗi shot là một scene độc lập**, có camera khóa được fit theo *mọi* variant, nên các lần cắt giữa các shot một-model không lộ (đã test camera giống hệt nhau).

## Hướng (dùng chung cho mọi template)
`[x, y, z]` | `UP` / `FROM_ABOVE` | `DOWN` / `FROM_BELOW` | `LEFT` `RIGHT` `FRONT` `BACK` |
`OUTWARD` (nằm ngang, từ tâm nhóm ra) | `OUTWARD_UP` (OUTWARD + lên, 45°) | `RADIAL` (3D từ tâm) | `HINT` (hướng gợi ý của builder, ví dụ pháp tuyến của mái).
Component nằm đúng tâm nhóm sẽ dùng `UP`.

## Easing
`LINEAR`, `SMOOTH` (sine in-out), `EASE_IN_OUT` / `EASE_IN` / `EASE_OUT` (cubic), `CONSTANT`.

## Thứ tự và stagger
`order`: `LISTED` | `ASSEMBLY` (layer tăng dần) | `DISASSEMBLY` | `BOTTOM_UP` | `TOP_DOWN`.
`stagger_by`: `LAYER` (các component cùng layer khởi động cùng lúc, ví dụ tấm phủ trái + phải) | `COMPONENT`.

## Tham chiếu cấu hình
Option không xác định là lỗi (để lỗi gõ sai không lọt qua). Giá trị mặc định nằm trong `engine/motion.py`.

### REPLACE_PARTS
```json
{"template": "REPLACE_PARTS", "from_state": "roof_A", "to_state": "roof_B", "duration_seconds": 6.0,
 "easing": "SMOOTH", "hold_start_seconds": 0.5, "hold_end_seconds": 1.0,
 "outgoing": {"components": "FROM_STATE", "direction": "OUTWARD_UP", "distance": 3.0,
              "lift": 0.5, "lift_seconds": 0.4, "move_seconds": 1.1,
              "stagger_seconds": 0.15, "stagger_by": "LAYER", "order": "DISASSEMBLY",
              "rotation_degrees": [0, 0, 0], "fade": true, "fade_start": 0.0, "hide_when_done": true,
              "per_component": {"roof_A_ridge_beam": {"direction": "UP", "distance": 2.0}}},
 "incoming": {"components": "TO_STATE", "direction": "FROM_ABOVE", "distance": 2.0, "move_seconds": 1.3,
              "stagger_seconds": 0.25, "stagger_by": "LAYER", "order": "ASSEMBLY",
              "rotation_degrees": [0, 0, 0], "fade": true, "fade_end": 0.75,
              "overlap_seconds": 0.3, "start_seconds": null, "easing": "EASE_OUT", "per_component": {}}}
```
- Phần ra: giữ → nhấc lên `lift` (tùy chọn) → di chuyển theo `direction * distance` trong khi mờ dần → `hide_render`.
- Phần vào: ẩn tại `rest + direction * distance` → hiện lại khi bắt đầu chuyển động → hạ đúng vào transform gốc (khớp chính xác, đã kiểm tra với sai số 1e-5).
- `components` phải là toàn bộ component của state (danh sách chỉ để chọn thứ tự). Component dùng chung bị từ chối.
- Phần vào bắt đầu tại `start_seconds`, hoặc tại `(lúc phần ra kết thúc) - overlap_seconds`.
- Markers (dùng cho stills/QA): `outgoing_start`, `outgoing_end`, `incoming_start`, `incoming_end`, `middle`.

### EXPLODED_VIEW
```json
{"template": "EXPLODED_VIEW", "state": "roof_A", "components": ["..."] ,
 "center": "AUTO", "direction_mode": "HINT", "distance": 0.8,
 "per_component": {"roof_A_covering_left": {"distance": 1.6}},
 "sequence": "SEQUENTIAL", "stagger_seconds": 0.15, "stagger_by": "LAYER", "order": "DISASSEMBLY",
 "hold_start_seconds": 0.4, "explode_seconds": 1.1, "hold_seconds": 1.5, "return_seconds": 1.0,
 "hold_end_seconds": 0.3, "easing": "SMOOTH",
 "highlight": {"components": "ALL", "mode": "SIMULTANEOUS", "strength": 0.55, "fade_seconds": 0.3}}
```
- Thứ tự trở về đảo ngược thứ tự tách (phần ra sau cùng về trước), và về **chính xác** vị trí nghỉ.
- Có thể đưa cả component dùng chung vào `components`; chúng cũng trở về chính xác.
- `highlight.mode`: `SIMULTANEOUS` hoặc `SEQUENTIAL` (khoảng giữ được chia đều cho các component).
- QA: tại `exploded_hold` không được có giao cắt mesh mới so với lúc nghỉ (kiểm tra bằng BVH).
- Markers: `explode_start`, `explode_end`, `exploded_hold`, `return_start`, `return_end`.

### SIDE_BY_SIDE
```json
{"template": "SIDE_BY_SIDE", "states": ["roof_A", "roof_B"], "gap_ratio": 0.35, "label_band": 0.12,
 "intro": {"from_state": "roof_B", "seconds": 1.5, "easing": "SMOOTH", "fade_start": 0.35, "fade_end": 0.9},
 "highlight": {"components": "DIFFERENCES", "start_seconds": 1.7, "rise_seconds": 0.4,
               "hold_seconds": 1.2, "fall_seconds": 0.5, "strength": 0.45}}
```
- **`intro` (M2.5, tùy chọn):** frame 1 dùng *đúng* camera single-model (fit theo base + mọi variant), tịnh tiến theo offset của slot `from_state`. Vì vậy, nếu shot trước kết thúc ở state đó, điểm cắt không lộ (SSIM đo được 0.9996). Sau đó camera (location + `ortho_scale`) chuyển dần sang khung so sánh, các model khác hiện dần trong khoảng `fade_start`–`fade_end` của intro. **Model không di chuyển**, chỉ camera di chuyển, nên không gian luôn liên tục. Highlight phải bắt đầu sau khi intro kết thúc (validator kiểm tra).
- Đã so sánh với dissolve bằng FFmpeg: ở giữa dissolve có ba "bóng ma" nhà chồng nhau (B ở hai tỷ lệ + A), khó đọc → không chọn. Xem `projects/roof-evolution/qa/M2_5_QA_REPORT.md`.
- Mỗi state có một model (base + variant), được parent vào một empty `SLOT_<state>`.
- Bố cục theo trục camera-right trên mặt đất, dùng kích thước footprint (không dùng offset cố định). Khoảng cách = `gap_ratio × model rộng nhất`.
- Camera dùng **cùng hướng nhìn** với các shot một-model; ortho scale được fit cho cả hàng model, chừa `label_band` ở dưới cho nhãn hậu kỳ.
- Ánh sáng là sun nên không phụ thuộc vị trí → các phần giống nhau trông giống hệt nhau.
- `DIFFERENCES` = mọi component do variant sở hữu, trong mọi slot.

### HOLD
```json
{"template": "HOLD", "state": "roof_B",
 "highlight": {"components": "STATE", "start_seconds": 0.3, "rise_seconds": 0.35,
               "hold_seconds": 0.9, "fall_seconds": 0.45, "strength": 0.45}}
```
- **`highlight.ghost` (M5, chỉ cho HOLD):** danh sách component **che** phần đang phát sáng, ví dụ ván mặt cầu nằm trên dầm dọc. Các component này chuyển sang trong suốt `ghost_transparency` (mặc định 0.7, tối đa 0.9) theo đúng nhịp của xung sáng, rồi trở lại đặc. Không có gì di chuyển, và trong lúc mờ thì fade twin (BLENDED) hiển thị thay cho bản gốc. Một component không được vừa phát sáng vừa ghost. SIDE_BY_SIDE từ chối tùy chọn này.
- QA Blender `highlight_targets_visible` (M5): ở đỉnh xung sáng (HOLD) hoặc giữa khoảng giữ bung (EXPLODED_VIEW), bắn tia orthographic trên lưới 192×108 qua khung camera. Ít nhất 25 % bóng (silhouette) của các phần phát sáng phải không bị phần đặc khác che, và phần nhìn thấy phải chiếm ít nhất 0.3 % khung hình. Phần trong suốt ≥ 50 % (ghost) không tính là vật che.

## Highlight và trong suốt
Material đọc 2 custom property trên từng object qua node Attribute (kiểu OBJECT):
- `ass_highlight`: 0..1, làm phần đó **tự phát sáng bằng chính màu của nó** (`materials.highlight_glow_gain`). M2.5 đã bỏ phần pha màu nhấn, vì ngay cả 10% vàng cũng kéo mái A (graphite) về xám/be và làm mất nhận diện A/B.
- `ass_transparency`: 0 = đặc, 1 = trong suốt hoàn toàn, có bóng trong suốt.
- **Fade twins (M2.5):** với `materials.fade_render_method = "BLENDED"`, mỗi object có kênh trong suốt được nhân đôi (`<tên>__fade`, dùng chung mesh, material BLENDED gán ở cấp object). Bản gốc (dithered) hiển thị khi đặc; twin chỉ hiển thị khi 0 < t < 1 (`motion.split_fades`, khoảng hiển thị bổ sung cho nhau, có test). Lý do: dithered bị nhiễu hạt khi đang mờ dần; còn BLENDED dùng cho mọi object thì đổi shading của phần đặc, gây giật hình ở điểm cắt (SSIM 0.992). Twin cho cả hai ưu điểm.

## Thêm loại công trình mới (cầu, cột, khung…)
1. Thêm danh sách parts vào `engine/spec.py` (`BASE_BUILDERS` / `VARIANT_BUILDERS`), gồm `role` và `assembly layer`.
2. Viết builder trong `engine/geometry.py`, đăng ký vào `*_BUILDER_FUNCS`. Builder phải gắn metadata qua `annotate()`, và `explode_hint` khi có hướng tách tự nhiên.
3. Khai báo variant trong `states.json`, dùng lại các template mà không sửa template.

## Transform logic / hiệu suất
Variant gốc không bị xóa, chỉ ẩn khi không active. Không dùng Shape Keys giữa hai mesh khác topology. Rafters/joists là mesh nhiều hộp trong một object (một component), không phải hàng chục object. Instancing (Geometry Nodes) chỉ cần khi số chi tiết lặp lớn (ngói, gạch).

## M3 — mở rộng
- **Mốc neo** (chỉ trong `storyboard.template.json`): mọi giá trị giây trong `animation` / `graphic` có thể là `@B3`, `@B3.s1+0.4`, `@B3.end` (beat / câu, tính từ đầu shot). `pipeline/beat_scheduler.py` giải chúng từ audio đo được.
- **Lớp phủ:** `covering.style` = `thatch` / `plain_tile` / `slate` (thêm part `<variant>_ridge_cap`, role `ridge_cap`, layer 4).
- **`structure_from`:** variant cùng độ dốc dùng chung gables / rafters / ridge beam; REPLACE_PARTS giữa hai variant như vậy chỉ di chuyển lớp phủ (`templates.replace_sets`).
- **Card 2D** (`visual_type: MOTION_GRAPHICS`, `graphic.elements` gồm text / arrow, `appear`): `engine/diagram.py`. Không phải template 3D; QA dùng `check_card`.
- Bài học (lỗi M3 #3): intro của SIDE_BY_SIDE chỉ làm hiện dần các phần mà state hiển thị; shot_builder từ chối plan nào animate phần đang bị ẩn tĩnh.
