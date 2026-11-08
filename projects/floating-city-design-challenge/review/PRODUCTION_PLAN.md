# Kế hoạch sản xuất sau khi chốt kịch bản c-r2

**Bối cảnh:**
- Chủ kênh chốt c-r2, duyệt 50 claim, giọng và phát âm, và yêu cầu bắt đầu dựng ngay (2026-11-08, `review/OWNER_APPROVALS.json`).
- **Điểm dừng:** đoạn thử có lời dẫn "thêm tải → chìm → sửa thân" (B09–B10, có B08 dẫn vào) để chủ kênh duyệt chất lượng hình trước khi làm cả phim.

**Vì sao phải phủ đủ 44 beat trước đoạn thử:**
- `tools/excerpt.py` cắt từ timing của cả phim (`script/timing.json` → `shots`). Timing đó chỉ có sau `build-shots`, mà `build-shots` đòi kế hoạch hình thực thi được cho **mọi** beat.
- Planner không có chế độ lập kế hoạch cho một phần phim. Thêm một chế độ bỏ qua beat là trái AGENTS.md ("Không bỏ qua beat").
- Vì vậy mọi beat phải có asset hoặc card thật. Chỉ các shot của đoạn thử được render.

## Các lớp (mỗi lớp kiểm chứng được và commit riêng)

| Lớp | Nội dung | Kiểm chứng |
|---|---|---|
| **L1** | Họ asset `floating`, biến thể `platform`: thân phao có khoang, sàn, nhà theo tầng, phần thân nối dài, mặt cắt, tấm nước dưới đáy. Site `bay` (thường và mặt cắt). Loại ngữ nghĩa, vật liệu, khái niệm trong từ vựng. Spec trong `asset_library/architecture/floating/`. | Test bộ sinh: mớn nước khớp `analysis/results.json`; mặt cắt chỉ giữ y ≥ 0; nhà phủ đúng tỉ lệ; `asset-check`; `asset-render --preset review`, rồi xem ảnh |
| **L2** | Bước SEQUENCE mới: `MOVE` (SINK/RISE), `ROTATE` (TILT), `OSCILLATE` (CONCEPT_MOTION, kèm nhãn bắt buộc). Engine và planner. | Test kế hoạch keyframe, ghép với REVEAL, cấm chồng thời gian; ca đánh giá planner |
| **L3** | Khu và quận: nhiều phao, khe, cầu có khớp, cọc, dây neo, đê, mạng hạ tầng, nhà theo chức năng, không gian công cộng. Site biển mở. Phao bán chìm (sơ đồ). Khối bê tông đặc (B05). | Như L1 |
| **L4** | `script/story.py`: hình của cả 44 beat (17 card; các bước SEQUENCE theo từ của lời dẫn). | `plan-visuals` thực thi được; `validate-plan` |
| **L5** | `build-shots` → `check-blender` → render shot của đoạn thử ở `internal_720p` → `tools/excerpt.py` (B08–B10) → QA (khung, giải mã, âm lượng, phụ đề, ASR) → gói duyệt. | Đoạn thử, `INTERNAL_REVIEW` |

## Quy tắc giữ suốt các lớp
- Số trên hình lấy từ `analysis/results.json`, không viết tay. Đặc biệt mớn nước, độ dịch SINK/RISE, góc TILT.
- Mọi chuyển động khái niệm mang nhãn "Conceptual motion visualization — not a hydrodynamic simulation".
- Neo và mối nối là hình khái niệm: "not sized" hoặc "conceptual geometry".
- Không ảnh Schoonschip cho tới khi có giấy phép; dùng sơ đồ.
- Mỗi lúc một Blender. Không 4K trước khi chủ kênh duyệt.

## Trạng thái
- **L1: xong (2026-11-08).**
  - Bộ sinh `engine/arch/families/floating.py` (`platform`, `bay`), đăng ký trong `engine/arch/assets.py`.
  - Thêm 5 loại ngữ nghĩa, 8 vật liệu, 10 khái niệm trong từ vựng, preset tách lớp.
  - Spec `asset_library/architecture/floating/floating_platform_a_01.json` và `floating_platform_a_section_01.json`; site `site_bay_01`, `site_bay_section_platform_a`.
  - Kiểm offline 5/5 cho cả bốn spec. Blender (`asset-render --preset review`) 4/4 cho cả hai phao, đã xem ảnh: ba phía, mặt đứng mặt cắt, tách lớp.
  - Cho phép chồng có chủ ý (ROOF, BUILDING) và tấm mặt cắt nằm trên mặt cắt của phần nó vẽ (`engine/arch/asset_scene.py`). Các cặp này chỉ có ở họ nổi.
  - Test: `tests/test_floating_family.py` (7). Toàn bộ test đạt; đánh giá planner 30/30.
- **L2: xong (2026-11-08).**
  - Bước SEQUENCE mới trong `engine/motion.py`:
    - `MOVE`: tịnh tiến nhóm theo độ dịch tính sẵn;
    - `ROTATE`: xoay nhỏ quanh một trục qua pivot, góc ≤ 45°;
    - `OSCILLATE`: nhấp nhô hình sin với nghiêng tùy chọn, mờ vào và ra, trở về vị trí nghỉ.
  - Các bước được ghép với REVEAL trên cùng bộ phận theo thứ tự thời gian. Hai chuyển động chồng thời gian trên một bộ phận bị từ chối. Bộ phận chỉ có REVEAL vẫn đi đúng đường cũ.
  - Planner từ chối OSCILLATE nếu beat không mang `motion_label` đúng chữ "Conceptual motion visualization — not a hydrodynamic simulation". `{"except": []}` nghĩa là cả công trình.
  - Bộ đánh giá chép thêm `audio/narration_manifest.json` (mốc theo từ) khi dự án có. Thêm ca FLOAT-SEQ-01 (dương) và FLOAT-SEQ-02 (âm): 32/32.
  - Test: `tests/test_motion_transforms.py` (8).
  - **Còn mở:** hiển thị nhãn chuyển động khái niệm trên hình. NOTE giới hạn 52 ký tự, câu nhãn dài 63 ký tự; xử lý ở L4.
- **L3:** tiếp theo.
