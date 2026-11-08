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
| CREATE_SMALL_NEW_CAPABILITY | Bước SEQUENCE `SINK`/`RISE`: tịnh tiến z một nhóm theo Δ lấy từ `analysis/results.json` | SH09, SH26 | 0,5–1 phiên, kèm test |
| CREATE_SMALL_NEW_CAPABILITY | Chiến lược `CONCEPT_MOTION`: heave/pitch hình sin tất định, lệch pha theo module, khe co giãn. **Nhãn bắt buộc** "Conceptual motion visualization — not a hydrodynamic simulation" do engine tự chèn | SH19 | 1 phiên, kèm test nhãn |
| ADAPT_EXISTING | WATER có `surface` tách riêng và hỗ trợ GHOST hai bước | SH25, SH27, SH38 | 0,5 phiên |
| ADAPT_EXISTING | Khái niệm mới trong `config/visual_vocabulary.json`; ca đánh giá trong `evaluation/visual_planning/cases.json` | Planner gọi được loại mới | 0,5 phiên |
| EXTERNAL_DEPENDENCY_REQUIRED | Ảnh Schoonschip có giấy phép (tùy chọn) | SH02, SH07 | Tìm trên Commons; nếu không có, dùng sơ đồ |

**Không làm:** mô phỏng chất lỏng, mô phỏng hydro-elastic, vật lý dây neo, cảnh phá hủy.

## 3. Chi phí render (ước lượng)

| Hạng mục | Ước lượng |
|---|---|
| Thời lượng | 636 s: 3D 412 s (khoảng 9.900 frame ở 24 fps), 2D 224 s (khoảng 5.400 frame) |
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
   - Cách giảm: thước mớn nước cận cảnh (P2b), hoặc chữ số trên hình.
6. **Chuỗi card 2D dài ở C7** (4 card liền, đúng ngưỡng QA phim dài).
   - Cách giảm: chuyển SH36 sang 3D.
7. **Thiếu ảnh có giấy phép** cho tiền lệ thật.
   - Cách giảm: sơ đồ tự vẽ có nhãn. Không dùng ảnh quảng bá của BIG hay OCEANIX.
8. **Bộ sinh mới gây lỗi cho các họ cũ.**
   - Cách giảm: test hồi quy cầu và nhà thờ; chạy `evaluate-planning`.

## 5. Khả thi theo từng shot

**Cột:**
- **Hôm nay?** là engine làm được ngay;
- **Asset mới?** là cần họ asset mới;
- **Hoạt ảnh mới?** là cần năng lực hoạt ảnh mới;
- **Sơ đồ tốt hơn?** là sơ đồ rõ hơn 3D;
- **Mô phỏng?** là cần mô phỏng thật (luôn là "không");
- **Công sức** và **Render** theo thang L/M/H.

| Shot | Hôm nay? | Asset mới? | Hoạt ảnh mới? | Sơ đồ tốt hơn? | Mô phỏng? | Hạng | Công sức | Render |
|---|---|---|---|---|---|---|---|---|
| SH01 | Không | A,B,E,F | Không | Không | Không | GENERATE_PROCEDURAL | H | H |
| SH02 | Có | — | — | Có | Không | REUSE_EXISTING | L | L |
| SH03 | Không | A–F | Không (SEQUENCE) | Không | Không | GENERATE_PROCEDURAL | M | H |
| SH04 | Không | B | Không | Không | Không | GENERATE_PROCEDURAL | L | L |
| SH05 | Không | A,B | Không (REVEAL) | Không | Không | GENERATE_PROCEDURAL | M | M |
| SH06 | Không | A,B (+mặt cắt) | Không | Không | Không | CREATE_SMALL_NEW_CAPABILITY | M | M |
| SH07 | Có | — | — | Có | Không | REUSE_EXISTING | L | L |
| SH08 | Không | B,E | Không (EXPLODE) | Kèm thanh 2D | Không | GENERATE_PROCEDURAL | M | M |
| SH09 | Không | B,E | `SINK` | Thước 2D | Không | CREATE_SMALL_NEW_CAPABILITY | M | M |
| SH10 | Không | B | Không | Không | Không | GENERATE_PROCEDURAL | L | L |
| SH11 | Có | — | — | Có | Không | REUSE_EXISTING | L | L |
| SH12 | Có | — | — | Có | Không | REUSE_EXISTING | L | L |
| SH13 | Không | B,E | Không (REVEAL) | Không | Không | GENERATE_PROCEDURAL | M | M |
| SH14 | Không | B,C,E | Không (REPLACE) | Không | Không | GENERATE_PROCEDURAL | M | M |
| SH15 | Không | C,F | Không | Không | Không | GENERATE_PROCEDURAL | M | M |
| SH16 | Có | — | — | Có | Không | REUSE_EXISTING | L | L |
| SH17 | Có | — | — | Có | Không | REUSE_EXISTING | L | L |
| SH18 | Không | A,B | Không | Không | Không | GENERATE_PROCEDURAL | L | M |
| SH19 | Không | A,B,C | `CONCEPT_MOTION` | Không | **Không** (có nhãn) | CREATE_SMALL_NEW_CAPABILITY | M | M |
| SH20 | Có | — | — | Có | Không | REUSE_EXISTING | L | L |
| SH21 | Có | — | — | Có | Không | REUSE_EXISTING | L | L |
| SH22 | Có | — | — | Có | Không | REUSE_EXISTING | L | L |
| SH23 | Không | A–F | Không (SEQUENCE) | Không | Không | GENERATE_PROCEDURAL | H | H |
| SH24 | Không | A | Không | Không | Không | GENERATE_PROCEDURAL | L | M |
| SH25 | Không | A,D | Nước 2 bước | Không | Không | ADAPT_EXISTING | M | H |
| SH26 | Không | B,D,F | `RISE`/`SINK` | Không | Không | CREATE_SMALL_NEW_CAPABILITY | M | M |
| SH27 | Không | A,D | Không (REPLACE) | Không | Không | GENERATE_PROCEDURAL | M | H |
| SH28 | Không | A,D | Không | Không | Không | GENERATE_PROCEDURAL | L | M |
| SH28b | Không | A | Không | Không | Không | GENERATE_PROCEDURAL | L | M |
| SH29 | Không | E,F | Không (GHOST) | Không | Không | GENERATE_PROCEDURAL | H | H |
| SH30 | Có | — | — | Có | Không | REUSE_EXISTING | L | L |
| SH31 | Không | F | Không | Không | Không | GENERATE_PROCEDURAL | M | M |
| SH32 | Không | F | Không | Không | Không | GENERATE_PROCEDURAL | M | M |
| SH33–SH36 | Có | — | — | Có | Không | REUSE_EXISTING | L | L |
| SH37 | Không | B | Không | Không | Không | GENERATE_PROCEDURAL | L | L |
| SH38 | Không | A | Không (bóng EEVEE) | Không | Không | ADAPT_EXISTING | M | M |
| SH39 | Không | E,F | Không | Không | Không | GENERATE_PROCEDURAL | M | M |
| SH40 | Có | — | — | Có | Không | REUSE_EXISTING | L | L |
| SH41 | Không | A–F | Không | Không | Không | GENERATE_PROCEDURAL | M | H |
| SH42, SH44, SH45 | Có | — | — | Có | Không | REUSE_EXISTING | L | L |
| SH43 | Không (dùng lại cảnh SH01) | — | Không | Không | Không | REUSE_EXISTING | L | H |

**Tóm tắt** (đếm bằng script từ bảng trên, 46 shot):
- 18 shot làm được ngay (card);
- SH43 dùng lại cảnh SH01;
- 21 shot cần họ asset mới nhưng dùng hoạt ảnh có sẵn;
- 4 shot cần năng lực nhỏ mới (SH06, SH09, SH19, SH26);
- 2 shot chỉnh nước (SH25, SH38).

## 6. Phụ thuộc
- Blender 5.2.2 (đã có), FFmpeg 9.0.1 (đã có), Kokoro `am_michael` (cần chủ kênh duyệt riêng cho dự án này; duyệt của hai phim trước không tự áp sang).
- Không cần phần mềm hay dịch vụ trả phí.
