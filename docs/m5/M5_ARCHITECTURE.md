# M5: lập kế hoạch hình ảnh tự động và điều phối storyboard → Blender

**Kịch bản → beat → ý đồ hình ảnh → asset → template → shot/camera → kiểm tra timing → storyboard thực thi được → render + QA.**

M5 thêm một tầng **lập kế hoạch tất định** (`planner/`, thuần Python, không gọi LLM khi chạy) nằm trước engine M2–M4. Tác giả (người hoặc Claude) viết beat có cấu trúc trong `script/visual_beats.json`. Planner quyết định mọi thứ còn lại theo luật cố định: asset nào, template nào, bao nhiêu shot, camera nào, mỗi shot bao nhiêu frame. Mỗi quyết định đều có lời giải thích. Không có bước nào ngẫu nhiên: cùng đầu vào thì ra cùng kế hoạch, giống đến từng byte (có test).

M5 **không** hỗ trợ "dựng hình 3D tùy ý từ câu chữ tự nhiên". Planner chỉ dùng các họ đã có (3 biến thể cầu + khu đất của M4, mái gable của M2 qua adapter). Khi thiếu thứ gì, planner báo thiếu và không thay bằng một animation khác.

## 1. Luồng dữ liệu
```text
script/visual_beats.json  (schemas/narrative_beats.schema.json)      ← tác giả viết
research/sources.json     (claim + trạng thái review)
config/visual_vocabulary.json   khái niệm → họ/biến thể/tham số, hoặc → role ngữ nghĩa
config/visual_planning.json     camera theo tỷ lệ công trình, luật timing, ngân sách chuyển động
asset_library/catalog/catalog.json + spec asset M4 + states.json cũ (adapter mái nhà)
        │
        ▼  python3 tools/cli.py plan-visuals --project <slug>
planner/beats.py      kiểm tra beat, trạng thái bằng chứng, thời lượng tạm tính
planner/intents.py    9 ý đồ → danh sách chiến lược theo thứ tự ưu tiên; đối chiếu từ khóa (chỉ cảnh báo)
planner/resolver.py   khái niệm → REUSE / ADAPT / GENERATE / NEW_ASSET_REQUIRED / BLOCKED (docs/m5/ASSET_RESOLUTION.md)
planner/mapper.py     khái niệm thành phần → ID thành phần ngữ nghĩa ổn định (thiếu hoặc mơ hồ đều là lỗi)
planner/planner.py    chiến lược → bản nháp shot → phân bổ frame → nhóm liên tục camera → kiểm tra hiển thị
planner/camera.py     chế độ camera → preset có sẵn; hiển thị offline bằng chính công thức engine/framing.py
planner/timing.py     cửa sổ beat PROVISIONAL / AUDIO_LOCKED; thời lượng tối thiểu từ motion planner thật
        │
        ▼  storyboard/visual_plan.json (schemas/visual_plan.schema.json) + qa/VISUAL_COVERAGE.md
planner/validate.py   python3 tools/cli.py validate-plan   (dựng lại mọi thứ độc lập + G0 của engine)
planner/compiler.py   python3 tools/cli.py build-shots     (chỉ chép lại; không ra quyết định)
        │
        ▼  storyboard/states.json + storyboard.json + project.json   (hợp đồng engine M2–M4, không đổi)
validate → check-blender → still → preview          (engine + cache + QA của M3/M4)
```

## 2. Ranh giới tất định
| Tầng | Ai quyết định | Ghi chú |
|---|---|---|
| Lời thoại, `narrative_intent`, khái niệm cần thấy, claim | Tác giả (có thể là Claude khi viết beat) | Lưu trong file, có kiểm tra schema, có review |
| Asset, chiến lược, template, camera, frame, ID mục tiêu | `planner/` (luật cố định) | Không LLM, không ngẫu nhiên, không phụ thuộc thứ tự dict của Blender |
| Hình học, animation, render | Engine M2–M4 | Đọc storyboard đã biên dịch; không biết planner tồn tại |

Planner chỉ đối chiếu `narrative_intent` khai báo với từ khóa trong lời thoại để **cảnh báo**, không bao giờ tự đổi ý đồ.

## 3. Engine thay đổi gì cho M5 (nhỏ, có test hồi quy)
| Thay đổi | File | Lý do |
|---|---|---|
| Builder `none` (trạng thái chỉ có khu đất) | `engine/spec.py`, `engine/geometry.py` | Cho phép "khe trống → cầu lắp vào" bằng REPLACE_PARTS |
| `build_variants` của shot | `engine/templates.py` (`single_slot_variants`), `tools/render_cache.py` | Mỗi nhóm liên tục chỉ dựng các variant nó dùng; cache chỉ băm hình học các variant đó |
| `camera_focus` + `camera_safe_band` | `engine/templates.py` (`check_camera_focus`), `engine/shot_builder.py`, `engine/qa_checks.py` | COMPONENT_CLOSEUP: camera khóa vừa khung các thành phần trọng tâm; chừa dải phụ đề |
| QA camera theo nhóm | `engine/qa_checks.py` | Camera chỉ cần giống nhau trong cùng nhóm `(variant dựng, preset, focus, band)` |
| `highlight.ghost` cho HOLD | `engine/motion.py` | Phần che (ván mặt cầu) chuyển sang trong suốt trong lúc phần bên dưới (dầm dọc) phát sáng |
| QA `highlight_targets_visible` | `engine/qa_checks.py` | Bắn tia orthographic để kiểm tra phần phát sáng có thật sự nhìn thấy được không (bị che hay không), xem `docs/m5/M5_QA_REPORT.md` |

Storyboard cũ không có các trường này vẫn chạy như trước: các test M2–M4 vẫn pass. Kiểm tra mới `highlight_targets_visible` tìm ra một lỗi có từ M4 (dầm dọc của pilot `bridge-structure-evolution` SC_001 bị ván che 86 %); lỗi này được sửa bằng `ghost`.

## 4. Nhóm liên tục camera và kiểu cắt
- Hai shot một-mô-hình liền nhau thuộc **cùng một nhóm** (cắt `match`) khi: cùng preset, cùng focus, và trạng thái đầu của shot sau là trạng thái cuối của shot trước. Hai shot SIDE_BY_SIDE liền nhau thuộc cùng một nhóm khi cùng danh sách trạng thái và cùng layout.
- Mỗi nhóm dựng đúng tập variant các shot trong nhóm cần (`build_variants`), nên camera khóa giống hệt nhau trong nhóm và không có cú "nhảy" khi cắt. Tập dựng được chọn theo nhóm, không theo cả dự án. Vì vậy đổi asset cầu đá chỉ làm cũ (stale) các shot có dựng cầu đá (có test).
- Chuyển sang nhóm khác là cắt `hard` (ghi `cut_from_previous: "hard"` trong storyboard; QA SSIM ở điểm cắt bỏ qua các cú cắt đó).
- `validate-plan` từ chối: cắt match giữa hai nhóm; cắt match mà trạng thái thay đổi; một nhóm trộn camera hoặc tập dựng.

## 5. Lệnh
```bash
P="--project bridge-story-m5"
python3 tools/cli.py plan-visuals $P     # → storyboard/visual_plan.json, qa/visual_coverage.json, qa/VISUAL_COVERAGE.md
                                         #   exit 4 khi có beat không thực thi được (kế hoạch vẫn được ghi để xem)
python3 tools/cli.py validate-plan $P    # kiểm tra độc lập + biên dịch thử vào thư mục tạm + G0
python3 tools/cli.py build-shots $P      # validate-plan → states/storyboard/project.json → validate
python3 tools/cli.py check-blender $P    # QA hình học/camera/animation trong Blender (không render)
python3 tools/cli.py still $P --preset review
python3 tools/cli.py preview $P          # 640×360; cache theo shot: chỉ render lại shot đã đổi
python3 -m unittest tests.test_m5_planner
```

## 6. Thư mục và file
| Đường dẫn | Nội dung |
|---|---|
| `planner/` | 12 module (khoảng 1 600 dòng), không import `bpy` |
| `config/visual_vocabulary.json` | Khái niệm khu đất, công trình, thành phần (role ngữ nghĩa M4, role mái M2) |
| `config/visual_planning.json` | Lớp tỷ lệ `long`/`compact` → preset camera; luật timing; ngân sách chuyển động; trọng số phân bổ |
| `schemas/narrative_beats.schema.json`, `schemas/visual_plan.schema.json` | Hợp đồng đầu vào và đầu ra của planner |
| `projects/bridge-story-m5/` | Pilot "Three Ways to Span a Gap" (8 beat, 13 shot, 72.38 s, không lời, INTERNAL ONLY) |
| `projects/roof-plan-m5/` | Fixture tổng quát hóa **SYNTHETIC** (mái nhà, 4 beat framing, không claim) |
| `tests/test_m5_planner.py`, `tests/test_blender_m5.py` | 34 test không cần Blender; 2 test Blender (phần bị che bị phát hiện, ghost làm nó lộ ra) |
| `docs/m5/VISUAL_PLANNING_PROTOCOL.md` | Cách viết beat, ý đồ, chiến lược, timing, camera, đọc báo cáo coverage |
| `docs/m5/ASSET_RESOLUTION.md` | Thuật toán chọn asset, adapter, sinh mới, chặn vì thiếu bằng chứng |
| `docs/m5/M5_QA_REPORT.md` | Kết quả QA, smoke test, MCP, hiệu năng |

## 7. Giới hạn
- Một dự án chỉ dùng **một** họ công trình trên một base chung (cầu trên khu đất, hoặc mái trên nhà). Trộn họ sẽ bị báo `PlanningError`.
- Không có template bản đồ, ảnh tư liệu, hay mũi tên lực trên mô hình 3D: SHOW_CONTEXT chỉ có khu đất hoặc thẻ 2D tác giả cung cấp; EXPLAIN_CAUSE_EFFECT chỉ có thẻ 2D (`MISSING_TEMPLATE` nếu không có thẻ).
- Timing PROVISIONAL là ước lượng từ số từ (2.6 từ/giây + 0.8 s), không phải giọng đọc đo được. Nếu timing là AUDIO_LOCKED, lời thoại phải được đo trước (`schedule` của M3) và khóa lại.
- Kiểm tra hiển thị offline chỉ chạy cho asset thư viện M4. Hình học mái cũ chỉ được dựng trong Blender, nên phải dựa vào `check-blender`.
- GENERATE chỉ đổi tham số của bộ sinh đã có; asset sinh ra là ILLUSTRATIVE, ghi trong `planning/generated_assets/` của dự án và không bao giờ ghi vào catalog.
