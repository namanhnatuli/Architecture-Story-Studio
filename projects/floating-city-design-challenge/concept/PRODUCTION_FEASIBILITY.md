# Khả thi sản xuất

**Kết luận:** phim làm được bằng pipeline hiện có, cộng **một họ asset mới** (floating, site `bay`) và **hai năng lực hoạt ảnh nhỏ** (`SINK`/`RISE`, `CONCEPT_MOTION`), cùng một tham số mặt cắt. Không cần dựng lại renderer hay planner. Không cần mô phỏng chất lỏng.

## 1. Năng lực có sẵn (đã kiểm trong mã, 2026-11-08)

| Năng lực | Có thật? | Bằng chứng trong repo |
|---|---|---|
| Hình học thủ tục, thành phần có id ngữ nghĩa | Có | `engine/arch/semantic.py` (`Component`, `SEMANTIC_TYPES`), `engine/arch/families/{bridge,cathedral,site}.py` |
| REPLACE_PARTS | Có | `engine/motion.plan_replace_parts`; chiến lược `REPLACE`, `HIGHLIGHT_REPLACE_HIGHLIGHT` (`planner/intents.py`) |
| EXPLODED_VIEW | Có | `engine/motion.plan_exploded_view`; `EXPLODE`, `CLOSEUP_EXPLODE` |
| SIDE_BY_SIDE | Có | `COMPARE_SIDE_BY_SIDE`, `FOCUSED_PAIR`, `DETAIL_THEN_OVERVIEW`; `planner/composition.py` |
| HOLD và HIGHLIGHT | Có | `HOLD`, `HOLD_HIGHLIGHT`, `CLOSEUP_HIGHLIGHT`; `plan_pulse` |
| SEQUENCE (GHOST, UNGHOST, FADE_OUT, FADE_IN, REVEAL, HIGHLIGHT; camera trượt giữa các view) | Có | `engine/motion.STEP_DEFAULTS`, `sequence_views`, `plan_sequence` |
| Nhiều họ kiến trúc, ngữ cảnh cảnh | Có | `states.json` schema 3, `scene_context` (M6, M8) |
| Chú thích ngữ nghĩa | Có | `planner/annotations.py`, `engine/annotations.py`, COMPONENT_LABEL |
| Lập camera, phát hiện che khuất, sửa bố cục tự động | Có | `planner/camera.py`, `planner/visibility.py`, `planner/repair.py`, `verify-visibility` |
| Kế hoạch theo audio đã khóa | Có | `lock-audio`, `pipeline/audio_lock.py` |
| Sản xuất theo chương | Có | `chapter`, `chapters`, `final-assemble` (đã chạy cho phim Gothic 4K) |
| Ghép 2D/3D | Có | `engine/diagram.py` (card, stage camera, phần tử theo từ) |
| Dùng lại frame tĩnh, cache render | Có | `render_strategy.json`, `verify-reuse`, `cache-report` |
| **CUTAWAY (template riêng)** | **Không** | Chỉ có trong backlog M3/M4 (`docs/m3/M4_READINESS.md`). Nhà thờ là mô hình mặt cắt do bộ sinh dựng. Prototype P1 cho thấy cách làm tương tự (dựng nửa và tấm mặt cắt) đọc được |
| **Tịnh tiến một nhóm theo trục z (chìm, nổi)** | **Không** | REVEAL chỉ đưa vật *tới* vị trí cuối. Không có bước "dời nhóm Δz" |
| **Dao động tuần hoàn (sóng khái niệm)** | **Không** | Không có kênh hoạt ảnh tuần hoàn nào trong `engine/motion.py` |
| **Nước trong suốt có mặt cắt** | Một phần | WATER là khối mờ (`stylized_materials.json` → `water`, không alpha). GHOST làm trong suốt được. Prototype P4/P5 cần thêm một tấm mặt nước riêng |
| Ảnh ngoài có giấy phép | Có (quy trình) | Hồ sơ `EXTERNAL_LICENSE_FIELDS`. Chưa có ảnh nào cho phim này |

## 2. Năng lực cần thêm (ưu tiên theo brief mục 15)

| Hạng | Việc | Lý do | Công sức (ước lượng) |
|---|---|---|---|
| GENERATE_PROCEDURAL | Họ `floating` (B–F) và site `bay` (A) | Không có asset nổi nào trong thư viện | 6–8 phiên agent (`BLENDER_ASSET_BLUEPRINT.md`) |
| CREATE_SMALL_NEW_CAPABILITY | Tham số `section_plane` cho bộ sinh: dựng nửa, thêm tấm mặt cắt | SH06, SH08, SH09 | 0,5 phiên |
| CREATE_SMALL_NEW_CAPABILITY | Bước SEQUENCE `SINK`/`RISE`: tịnh tiến z một nhóm theo Δ lấy từ `analysis/results.json` | SH09, SH10, SH23 (đã thử bằng prototype P6) | 0,5–1 phiên, kèm test |
| CREATE_SMALL_NEW_CAPABILITY | Bước SEQUENCE `TILT`: xoay một nhóm một góc nhỏ tính sẵn quanh trục giữa (B11) | SH11 | 0,5 phiên |
| CREATE_SMALL_NEW_CAPABILITY | Chiến lược `CONCEPT_MOTION`: heave/pitch hình sin tất định, lệch pha theo module, khe co giãn. **Nhãn bắt buộc** "Conceptual motion visualization — not a hydrodynamic simulation" do engine tự chèn | SH17, SH30 | 1 phiên, kèm test nhãn |
| GENERATE_PROCEDURAL | Site biển mở (`site.open_sea`) và biến thể phao bán chìm sơ đồ (Design D, 3D theo review c-r0) | SH29–SH31, SH33 | 1 phiên |
| ADAPT_EXISTING | Nhà theo chức năng (nhà ở, trường, phòng khám, chợ, bến) và không gian công cộng phân biệt được bằng hình khối và màu (review c-r0: greybox lặp lại chấp nhận được, bản phim thì không) | mọi cảnh quận | 0,5 phiên |
| ADAPT_EXISTING | WATER có `surface` tách riêng và hỗ trợ GHOST hai bước | SH25, SH27, SH38 | 0,5 phiên |
| ADAPT_EXISTING | Khái niệm mới trong `config/visual_vocabulary.json`; ca đánh giá trong `evaluation/visual_planning/cases.json` | Planner gọi được loại mới | 0,5 phiên |
| EXTERNAL_DEPENDENCY_REQUIRED | Ảnh Schoonschip có giấy phép (tùy chọn) | SH02, SH07 | Tìm trên Commons; nếu không có, dùng sơ đồ |

**Không làm:** mô phỏng chất lỏng, mô phỏng hydro-elastic, vật lý dây neo, cảnh phá hủy.

## 3. Chi phí render (ước lượng)

| Hạng mục | Ước lượng |
|---|---|
| Thời lượng | Theo `VISUAL_STORYBOARD.md` (đo từ audio c-r1). Ở khoảng 13 phút: chừng 18.700 frame ở 24 fps, khoảng hai phần ba là 3D |
| Mốc đo của Studio | Phim Gothic ở 4K khoảng 2,2 s mỗi frame 3D (AGENTS.md, bổ sung 2026-11-07) |
| 4K, cận trên khi không dùng lại frame | 3D khoảng 6 giờ với độ nặng như Gothic. Cảnh S1 có khoảng 50–200 phao instancing và nước trong suốt, có thể nặng gấp 2–3: **6–18 giờ**. 2D nhẹ hơn nhiều |
| Dùng lại frame tĩnh | Giảm đáng kể ở các shot HOLD và card. Số thật đo bằng `--mode reuse-report` khi có kế hoạch |
| Prototype | 6 still 960 × 540 EEVEE, khoảng 1 giây mỗi still (cảnh nhỏ) |
| Đĩa | Như Gothic: PNG 4K theo chương, xóa sau khi có bản trung gian đã kiểm (`--release-frames`) |

Ước lượng này **chưa đo** trên cảnh S1 thật. Bước đầu của sản xuất là benchmark một shot S1 ở 4K.

## 4. Rủi ro chính

1. **Hình bị đọc như bằng chứng:** sóng, độ võng dây, đê chắn.
   - Cách giảm: nhãn bắt buộc trên mọi chuyển động khái niệm; dây và neo có NOTE "not sized"; không biên độ.
2. **Con số minh họa bị hiểu thành kết quả kỹ thuật** (mớn nước 3 m, 1 triệu tấn).
   - Cách giảm: luôn kèm *illustrative / in our design*; không đặt số cạnh công trình thật.
3. **Tình trạng OCEANIX Busan đổi** sau ngày kiểm.
   - Cách giảm: ghi ngày kiểm trên hình; kiểm lại trước khi khóa kịch bản.
4. **Quy mô:** phao 40 m cạnh quận khoảng 600 m không cùng đọc được trong một khung (SH41).
   - Cách giảm: DETAIL_THEN_OVERVIEW, hoặc khung cận trước rồi kéo lùi.
5. **Thay đổi 33 cm không thấy ở khung rộng** (prototype P2).
   - Cách giảm: thước mạn khô cận cảnh và nhãn số. Prototype P6 (hoạt ảnh) thử đúng cách này.
6. **Chuỗi card 2D ở C7.**
   - Đã xử lý ở c-r1: phần ngoài khơi và thân bán chìm thành 3D. Chuỗi card dài nhất ghi ở cuối `VISUAL_STORYBOARD.md`.
7. **Thiếu ảnh có giấy phép** cho tiền lệ thật.
   - Cách giảm: sơ đồ tự vẽ có nhãn. Không dùng ảnh quảng bá của BIG hay OCEANIX.
8. **Bộ sinh mới gây lỗi cho các họ cũ.**
   - Cách giảm: test hồi quy cầu và nhà thờ; chạy `evaluate-planning`.

## 5. Khả thi theo từng shot
Từ c-r1, bảng từng shot nằm trong `concept/VISUAL_STORYBOARD.md` (cột "Hạng"). Bảng đó do `concept/build_storyboard.py` sinh từ kịch bản và timing đo từ audio, nên không lệch với lời dẫn. Bảng tổng kết theo hạng ở cuối tệp đó.

## 6. Phụ thuộc
- Blender 5.2.2 (đã có), FFmpeg 9.0.1 (đã có), Kokoro `am_michael` (cần chủ kênh duyệt riêng cho dự án này; duyệt của hai phim trước không tự áp sang).
- Không cần phần mềm hay dịch vụ trả phí.
