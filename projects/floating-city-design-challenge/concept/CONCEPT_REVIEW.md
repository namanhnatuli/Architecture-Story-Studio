# Duyệt concept: "Could We Build an Entire City That Floats?"

- **Dự án:** `floating-city-design-challenge`, nhánh `concept-floating-city-design-challenge`, ngày 2026-11-08.
- **Trạng thái:** **CONCEPT, chờ chủ kênh duyệt.**
  - Không có kịch bản (`script/story.py`), lời dẫn hay asset sản xuất.
  - Không claim nào được duyệt.
  - Không render nào ngoài 6 still prototype.

## Gói duyệt

| Mục | Tệp |
|---|---|
| A. Ba hướng kể và đề xuất | `concept/CONCEPT_OPTIONS.md` |
| B. Hợp đồng kịch bản | `concept/SCENARIO_CONTRACT.md`, `concept/scenario_contract.json` |
| C. Nghiên cứu kỹ thuật | `concept/ENGINEERING_RESEARCH.md`; sổ nguồn `research/sources.json` (14 nguồn, 48 claim, khớp nguyên văn); `research/source_snapshots.json` |
| Mô hình tính | `analysis/design_model.py` → `analysis/results.json`, `analysis/RESULTS.md`; test `tests/test_floating_city_concept.py` |
| D. Tiến hóa thiết kế | `concept/DESIGN_EVOLUTION.md` |
| E. Dàn ý | `concept/NARRATIVE_OUTLINE.md` (gồm rà soát biên tập) |
| F. Storyboard | `concept/VISUAL_STORYBOARD.md` (46 shot, 10:36) |
| G. Asset thủ tục | `concept/BLENDER_ASSET_BLUEPRINT.md` |
| H. Khả thi sản xuất | `concept/PRODUCTION_FEASIBILITY.md` |
| I. Prototype | `concept/PROTOTYPE_REPORT.md`; ảnh trong `renders/prototype/` (git bỏ qua; lệnh sinh lại có trong báo cáo) |
| J. Quyết định | tệp này |

## Vì sao đáng làm
- **Câu hỏi hấp dẫn ngay**, và Studio có cách trả lời mà kênh khác thường không có: dựng lại thành phố **từng vấn đề một**, với số tính minh bạch thay cho render quảng bá.
- **Chủ đề đang được nghiên cứu nghiêm túc:** hai bài Nature 2026. Thông tin công khai về dự án lớn khan hiếm và mâu thuẫn (CLM_061), nên một phim cẩn thận có giá trị.
- **Hợp với ngôn ngữ hình của Studio:** mặt cắt, lộ dưới nước, làm mờ, so sánh A/B. Prototype cho thấy hình quan trọng nhất đọc được.

## Concept được chọn
**C → A, cộng phản thực tế D** (bảng điểm 45,5/55):
- bắt đầu từ một khu nổi có thật (Schoonschip, khoảng 100 người);
- leo thang tới quận 10.000 người nối bờ trong vịnh kín;
- rồi đưa thiết kế ra khơi để thấy vì sao địa điểm là một nửa thiết kế.

Giả thuyết khởi đầu của chủ kênh (thành phố ven biển kín, phao module) được giữ nguyên làm xương sống.

## Người xem sẽ học được gì
1. Vì sao một khối bê tông hàng nghìn tấn nổi: hình dạng và nước bị chiếm chỗ. Mỗi tấn đòi khoảng một mét khối nước.
2. Phần lớn thứ phao phải đỡ là chính nó (khoảng 55% trong thiết kế minh họa).
3. Phao rộng rất khó lật, nhưng chính vì thế lại bám theo mặt nước. Ổn định không phải là tiện nghi.
4. Nhân một phao thành thành phố sinh ra mối nối, và mối nối là chỗ yếu. Phao to hay nhiều phao là một đánh đổi thật.
5. Thành phố nổi vẫn buộc vào đất liền: cọc và dây neo, cầu có khớp, cáp và ống về bờ.
6. Địa điểm quyết định: thiết kế ven bờ không dời ra khơi được.
7. Phần khó nhất có thể không phải kỹ thuật: bảo trì, sinh thái, ai sở hữu mặt nước, chi phí.

## Những hình lộ ra mạnh nhất
- **SH06:** mặt cắt Archimedes, mảng vàng là khối nước bị chiếm chỗ (đã thử, P1).
- **SH05:** cùng một khối bê tông, đúc đặc thì chìm, làm hộp thì nổi.
- **SH14:** hai phao giống nhau, khác tải, mặt sàn lệch 66 cm, nên cầu cứng phải thành cầu có khớp.
- **SH25–SH27:** mặt nước mờ dần, lộ cọc rồi dây neo theo độ sâu (đã thử, P4–P5).
- **SH29:** nhà lùi đi, mạng hạ tầng hiện ra theo cầu về bờ.
- **SH33–SH36:** kéo quận ra khơi, cả loại kết cấu phải đổi.

## Điều gì là sự thật, giả thuyết, bất định

| Loại | Ví dụ | Mã |
|---|---|---|
| **Sự thật** (ESTABLISHED_FACT) | Archimedes; Schoonschip (46 hộ, 30 lô, phao bê tông, nhà 340–350 t, một đầu nối lưới); nhà nổi Hà Lan tựa cọc và rung khi bão; nghiên cứu nêu hydro-elastic, mối nối, sinh thái, quản trị là thách thức | CLM_001–023, 040–048, 051–054, 059–061 |
| **Ước tính tính toán** (CALCULATED_ESTIMATE) | Mớn nước khoảng 3 m, 55% là thân phao, +33 cm mỗi tầng, nghiêng 0,4°, khoảng 209 phao hay khoảng 34 phao, khoảng 1 triệu tấn, dốc cầu khoảng 3° | `analysis/results.json` |
| **Giả định thiết kế** (DESIGN_ASSUMPTION) | 10.000 người, vịnh kín, sâu 12–25 m, dải mực nước 2 m, kích thước phao, tải nhà | `scenario_contract.json` |
| **Đề xuất** (SPECULATIVE_PROPOSAL) | OCEANIX Busan; thiết kế 50.000 người ngoài khơi của Ruzzo 2026; tuyên bố "100% năng lượng tại chỗ" | CLM_030–032, 050, 055–058, 062 |
| **Chưa xác minh** (UNVERIFIED) | OCEANIX Busan đã khởi công chưa (không tìm thấy báo cáo; mốc 2025 đã qua) | CLM_033 |
| **Còn bất định** | Sóng của địa điểm; hydro-elastic; tải và mỏi mối nối; thiết kế neo; sinh thái; quản trị; chi phí | `SCENARIO_CONTRACT.md` |

## Đã sẵn sàng cho sản xuất đầy đủ chưa?
**Chưa. Concept sẵn sàng để duyệt, sản xuất thì chưa.** Thứ tự đề xuất sau khi chủ kênh duyệt concept:
1. **Chủ kênh quyết** (xem mục dưới).
2. **Sửa các điểm nghiên cứu còn mở:**
   - nguồn gốc cho Aquapolis (CLM_060), hoặc bỏ khỏi phim;
   - tìm ảnh Schoonschip có giấy phép, hoặc chốt dùng sơ đồ;
   - kiểm lại tình trạng OCEANIX Busan trước khi khóa kịch bản.
3. **Viết `script/story.py`:** lời dẫn và beat từ dàn ý, chạy kiểm tra "lời và hình có khẳng định vượt bằng chứng không". Chủ kênh đọc kịch bản trước (`tools/script_review.py`).
4. **Dựng họ asset `floating` và site `bay`**, cùng ba năng lực nhỏ: mặt cắt, `SINK`/`RISE`, `CONCEPT_MOTION` có nhãn bắt buộc. Kèm test và ca đánh giá planner.
5. **Benchmark một shot cảnh S1 ở 4K**, rồi mới theo playbook thông thường.

## Cần chủ kênh quyết
1. **Hướng kể:** đồng ý C → A + D, hay chỉ A (bỏ phản thực tế ngoài khơi)?
2. **Mức dùng số minh họa trên hình:** giữ các số tính (mớn nước 3 m, 55%, khoảng 1 triệu tấn) kèm chữ *illustrative*, hay chỉ nói quan hệ ("mỗi tấn khoảng một mét khối")?
3. **Có gắn kịch bản với một địa điểm thật không?** Hiện tại cố ý không gắn, để không biến giả định thành sự thật về một nơi có thật.
4. **Có nhắc OCEANIX Busan không?** Nếu có, chỉ như đề xuất có ngày kiểm.
5. **Duyệt giọng `am_michael` cho dự án này:** duyệt của hai phim trước không tự áp sang.

## Định nghĩa hoàn thành (brief mục 21)

| # | Điều kiện | Trạng thái |
|---|---|---|
| 1 | Đánh giá ba concept | Xong (`CONCEPT_OPTIONS.md`) |
| 2 | Đề xuất một hướng | Xong (C → A + D) |
| 3 | Giả định kịch bản rõ ràng | Xong (`scenario_contract.json`, có test) |
| 4 | Nguyên lý có nguồn tin cậy | Xong (14 nguồn, 48 claim khớp nguyên văn; 7 nguồn không mở được hoặc không đọc, ghi ở `research/source_snapshots.json` → `not_used`) |
| 5 | Thay đổi thiết kế có lý do | Xong (`DESIGN_EVOLUTION.md`) |
| 6 | Dàn ý 10–12 phút mạch lạc | Xong (10:36 theo storyboard) |
| 7 | Storyboard có hình lộ ra có ý nghĩa | Xong (46 shot) |
| 8 | Mỗi cảnh chính có chiến lược hình khả thi | Xong (`PRODUCTION_FEASIBILITY.md` §5) |
| 9 | Bản thiết kế asset thủ tục dạng module | Xong (`BLENDER_ASSET_BLUEPRINT.md`) |
| 10 | Ghi rõ giới hạn và claim bất định | Xong |
| 11 | Prototype qua kiểm tra hình liên quan | Một phần: P1, P3, P4 đạt; P2 cho thấy cần cận cảnh (P2b đạt một phần); P5 đạt một phần; chưa thử hoạt ảnh (`PROTOTYPE_REPORT.md`) |
| 12 | Sẵn sàng cho buổi duyệt concept | **Có** |
