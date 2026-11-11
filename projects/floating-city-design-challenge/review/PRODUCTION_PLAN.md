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
- **L3: xong (2026-11-08).**
  - Biến thể mới trong `engine/arch/families/floating.py`:
    - `pair` (B13): hai phao giống nhau, nhà 2 và 4 tầng, mỗi phao ở mớn nước tính sẵn (2,626 và 3,290 m), cầu đi bộ có khớp nối hai mép sàn lệch nhau 0,664 m;
    - `neighbourhood`: năm phao hình chữ U quanh một bể nước nhỏ, khe, cầu đi bộ có khớp, ống mềm, đệm va; giữ bằng cọc (`moorings = piles`) hoặc dây neo có độ võng vẽ tay tới neo trên đáy (`lines`);
    - `clay_boat` (B05): cùng lượng bê tông 1.108 m³ dưới dạng khối đặc cạnh 10,35 m nằm dưới đáy, cạnh thân phao rỗng nổi ở mớn 1,621 m (chỉ thân, mặt cắt);
    - `semi_sub` (B33): sơ đồ phao bán chìm, hai phao ngầm, cột xuyên mặt nước, sàn cao;
    - `district` (Design C): 93 phao 60 m (66 phao nhà ở trong, 27 phao dịch vụ ở hàng ngoài và hai sườn), cầu đi bộ giữa các phao, ba cầu dẫn 25 m có khớp về kè, cọc ở ba hàng nông, dây neo ở vòng sâu, đê chắn sóng phía biển, ba mạng hạ tầng (điện, nước, nước thải) tựa trên cầu đi bộ, bến thuyền cứu hộ, đường thoát hiểm. `offshore = 1` bỏ cầu dẫn và đường thoát hiểm.
  - Site mới: `site_bay_district_01` (vịnh có kè, đáy dốc 12 → 25 m trên 900 m), `site_open_sea_01` (biển mở sâu 60 m). Cọc và neo của quận theo đúng đáy dốc của site (`seabed_run_m`); cọc cắm vào đáy 3 m, neo lún 0,3 m.
  - Chín loại ngữ nghĩa mới (cầu đi bộ, mối nối, đường ống, cọc, dây neo, neo, đê, cầu dẫn, đường thoát hiểm), 10 vật liệu, 18 khái niệm trong từ vựng.
  - Cho phép chồng có chủ ý: dây neo vào neo, cọc và neo vào đáy (`engine/arch/asset_scene.py`). Các loại này chỉ có ở họ nổi.
  - Kiểm offline 5/5 cho cả chín spec. Blender (`asset-render --preset review`) 4/4 cho cả chín, đã xem ảnh ba phía, mặt đứng, mặt bằng, tách lớp. Catalog 26 asset.
  - Neo và dây neo mang ghi chú "conceptual …, not sized"; độ võng dây là hình vẽ, không phải dây xích tính toán.
  - Test: `tests/test_floating_family.py` (15): số bộ phận khớp `checks.expected_counts` cho mọi spec; mớn nước và bước sàn khớp `results.json`; khối đặc chứa đúng lượng bê tông của thân; cọc và neo theo đáy của site; quận ngoài khơi không có đường về bờ. Toàn bộ 438 test đạt; đánh giá planner 32/32.
  - **Ghi chú cho L4:** ở khung nhìn toàn vịnh, cầu dẫn, dây neo và hạ tầng rất mảnh. Các beat nói về chúng (B27–B31) cần camera gần hoặc làm nổi bật.
- **L4: xong (2026-11-08).**
  - Hình của 44 beat nằm ở `script/visuals.py` (cảnh 3D: bước SEQUENCE theo từ của lời dẫn; 17 card) và `script/cards.py` (công cụ vẽ card). `story.py` chỉ ghép vào `visual_beats.json`; lời dẫn không đổi một byte (`narration.json` so khớp trước và sau).
  - Mọi độ dịch và góc lấy từ `analysis/results.json`: chìm 0,332 m (B09); đáy hạ 0,5 m rồi nổi lên 0,436 m tới mạn khô 1,146 m (B10); tải 100 t dời 15 m, nghiêng 0,421° (B11).
  - Asset bổ sung:
    - vạch mạn khô vàng trên mặt cắt (phần nổi trên nước chính là mạn khô, như prototype P6);
    - phao 3D có khối tải 100 t và bốn phao lân cận (B11–B12, `floating_platform_a_story_01`);
    - khu có cả cọc và dây neo để B24 đổi cọc sang dây (`floating_neighbourhood_both_01`);
    - mô-đun bán chìm đặt cạnh phao hộp 40 m (B33);
    - cáp và ống trên đáy biển về phía bờ ngoài khung (B31, quận ngoài khơi).
  - `floating_platform_a_01` trở lại đúng Design A (3 tầng, không phần thân thêm) vì B33–B34 dùng nó nguyên trạng.
  - Bốn preset camera của họ nổi (`FLOAT_AERIAL`, `FLOAT_THREE_QUARTER`, `FLOAT_SECTION`, `FLOAT_UNDERWATER`); hai preset sau ẩn mặt đất môi trường (nó nằm ngay dưới mặt nước).
  - Thay đổi so với storyboard đã duyệt, cần chủ kênh biết:
    - B23 thành card mặt đứng đúng góc dốc (nước, phao trên cọc, cầu dẫn 25 m quay quanh khớp bờ). Lý do: site không có nước nâng hạ được; nếu chỉ nâng phao thì phao nhô khỏi nước.
    - B36 thành card hai mép nước (công cộng / rào riêng): không có asset rào.
    - B33 là một cảnh SEQUENCE (phao hộp, rồi mô-đun bán chìm hiện lên cạnh), không phải SIDE_BY_SIDE: site 320 m làm hai mô hình quá nhỏ để đọc.
    - B11 dùng phao ở trạng thái cuối B10 (4 tầng, thân sâu), đúng hướng "B12 làm mờ tầng 4 và phần thân thêm". Góc nghiêng 0,42° được tính cho bản 3 tầng; bản 4 tầng thân 4,5 m cho khoảng 0,44°. Cả hai đều "khoảng 0,4°" và "dưới nửa độ" như lời dẫn.
  - Sửa engine và planner (có test):
    - MOVE tức thời ở đầu shot giữ ngay từ khung 1;
    - khóa đầu mỗi bước lấy đúng trạng thái tại thời điểm bắt đầu (trước đây bộ phận trôi khoảng 0,05 mm suốt đoạn giữ, làm hỏng nhãn bám bộ phận);
    - bộ kiểm chú thích và bộ kiểm lời–hình đếm câu theo `timing.json` (câu kết bằng dấu phẩy là một câu riêng);
    - "gray water", "black water" là thuật ngữ, không phải tên màu (`config/annotation_style.json` → `colour_terms`);
    - OSCILLATE phải có NOTE đúng nguyên văn nhãn chuyển động khái niệm suốt beat; riêng nhãn này được dài hơn giới hạn 52 ký tự.
  - Kết quả: `plan-visuals` thực thi được (44/44, 784 s), `validate-plan` đạt. Đánh giá planner 33/33 (thêm FLOAT-SEQ-03). 454 test đạt.
  - Cảnh báo còn lại (không chặn): khai báo intent khác gợi ý từ khóa ở sáu beat; xử lý khi review toàn phim.
- **L5: xong tới điểm dừng (2026-11-08).**
  - `build-shots` (44 shot, 784 s; khóa âm thanh giữ nguyên). Kiểm Blender bốn shot SC_008–SC_011: 76/76.
  - Đoạn thử B08–B11 (77,4 s, `internal_720p`) bằng `tools/excerpt.py`: QA tự động đạt (khung, cắt, âm lượng, Whisper WER 0, phụ đề).
  - Agent đã xem lại video và sửa một nhãn hiện quá ngắn.
  - Sửa thêm trong lúc dựng (có test):
    - mốc `reveal_i_landed` được đặt cả khi REVEAL ghép với MOVE (trước đó kiểm Blender dừng vì thiếu mốc);
    - nhóm camera đồng nhất tính cả hướng mở đầu riêng của SEQUENCE;
    - vạch mạn khô 1,0 × 1,3 m để phần nổi trên nước đủ lớn cho kiểm "phần phát sáng nhìn thấy được".
  - Gói duyệt: `review/EXCERPT_REVIEW_L5.md`. **Dừng chờ chủ kênh duyệt chất lượng hình** trước khi render phần còn lại.
- **L5 vòng 2 (2026-11-10), sau review asset và đoạn thử:**
  - **Mô hình tính:** thêm góc nghiêng của trạng thái B11 chiếu (0,438°) và phân bổ 93 module (66 nhà ở + 6 hỗn hợp + 21 dịch vụ → 10.080 người ở mức 30 m²). Nguồn và 50 claim không đổi (`build_sources.py` cho cùng `sources.json`).
  - **Asset:**
    - cửa sổ, vạch tầng, lối vào cho mọi nhà;
    - lối đi lát trên mọi phao;
    - trường học (chữ U, sân chơi), phòng khám (vòng quanh sân trong), nhà cộng đồng (hai dãy dài); cỏ và cây trên 10 phao quanh hồ;
    - mọi kiểu sử dụng phủ cùng diện tích và số tầng, nên giữ đúng tải và mớn nước;
    - mặt cắt có nửa trước và nước phía trước để B08 "cắt"; có đường kích thước mớn nước và mạn khô, các nét đứt chuẩn trước/sau, đường viền phần thân dưới nước;
    - phao 3D có mũi tên 15 m và đường ngang chuẩn.
  - **B08–B11 làm lại theo từng điểm góp ý**, gồm hai âm hiệu ứng nhẹ. Kiểm Blender 73/73; QA đoạn thử đạt.
  - **Engine:**
    - khóa cuối của bước REVEAL/MOVE lấy đúng trạng thái kết thúc (không trôi);
    - kiểm "bộ phận đáp đúng chỗ" chấp nhận vị trí do các bước MOVE trước đó đặt.
  - **Thử Sand3D** (`review/SAND3D_TRIAL.md`): nhập USD được, đúng tỉ lệ, chi phí render không đáng kể, nhưng chỉ thấy ở khung cận. Chưa dùng trong phim.
  - **Dừng chờ chủ kênh duyệt R2.**
- **L6: diện mạo đô thị và đoạn mở đầu (2026-11-11), sau review R2.**
  - **Đầu vào:** review R2 coi cách giải thích B08–B11 là mẫu cho các chương cơ chế. Toàn quận vẫn lặp lại, công viên chưa đọc được, cảnh neo mất cảm giác nước, hồ sơ khối lượng còn câu cũ.
  - **Hồ sơ khối lượng:**
    - `analysis/design_model.py` tách "đã gồm" (nhà ở; trường, phòng khám, cửa hàng, văn phòng trong 40 m²/người) và "không gồm" (phao cảng, bến thuyền, phao hạ tầng; đê; cầu dẫn; neo; mạng hạ tầng);
    - thêm ghi chú kiểu nhà và giới hạn tải cây xanh;
    - không số nào đổi. Câu tương ứng trong `concept/scenario_contract.json` sửa theo.
  - **Kiểu nhà** (`engine/arch/families/floating.py`):
    - dãy nhà liền kề mái dốc, khối sân trong có pin mặt trời, biệt thự mái lệch ốp gỗ, bốn thanh nhà xoay có ban công, bốn khối cũ, và phao vườn mở ra mặt hồ;
    - kiểu nào cũng 40% diện tích chiếm đất, 3 tầng, trọng tâm giữa sàn, phố chữ thập ở giữa phao. Vì vậy tải, mớn nước và độ nghiêng của phép tính giữ nguyên (có test).
  - **Quận:**
    - nhà ở chia thành ô 2 × 2 phao cùng kiểu, ô cạnh nhau khác kiểu;
    - 10 phao quanh hồ là phao vườn: cỏ, cây, ghế, đèn, sân chơi, lối dạo ven nước;
    - ống hạ tầng chuyển từ hàng 6 sang hàng 7 để không cắt ngang công viên;
    - `home_types = blocks` dựng lại được diện mạo cũ để so sánh.
  - **Khu 5 phao** (B14, B17, B22, B24) dùng 5 kiểu nhà.
  - **Nước làm trong:** giữ 50% màu ở mọi cảnh (B31: 35%, vì cáp nằm sâu 60 m). B24 mở bằng nước đầy, rồi mới làm trong. B22 có ghi chú "Water drawn see-through".
  - **Đoạn mở đầu B01–B02:** toàn quận → cụm có hai trường và ba phao vườn → cận công viên → sát mặt nước → kéo lui ra toàn quận. Đã thử làm sáng thân phao, neo và hạ tầng ở B02 nhưng bỏ: ở tầm toàn quận chúng chỉ chiếm 0,05–0,5% khung hình và kiểm Blender từ chối.
  - **Engine:** camera giữa hai khung khác hướng lùi ra quá khoảng cắt xa, làm hiện mảng nền phẳng. Sửa hai chỗ:
    - `clip_end` của SEQUENCE tính cả lúc lùi;
    - mức lùi tỉ lệ với góc quay, không lùi khi chỉ đổi khung.
    Có test.
  - **Khóa `clearance` cho khung nhìn** (khoảng camera đứng trước phần được đóng khung; mặc định 10 m):
    - đoạn mở đầu dùng 400 m để mặt phẳng cắt gần không xén các phao phía trước;
    - B14 dùng 40 m và nhìn dọc khe nước.
  - **Sand3D vòng 2:** không mẫu tòa nhà nào đúng 3 tầng (`review/SAND3D_TRIAL.md`). Phim dùng đồ của Studio.
  - **SFX:** kho `sfx/` có vẻ không được dùng ngoài CapCut theo thỏa thuận giấy phép của CapCut (`review/SFX_LIBRARY.md`). Chưa dùng.
