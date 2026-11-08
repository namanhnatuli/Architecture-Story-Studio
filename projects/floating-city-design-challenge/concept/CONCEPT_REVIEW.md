# Duyệt concept và kịch bản: "Could We Build an Entire City That Floats?"

- **Dự án:** `floating-city-design-challenge`, nhánh `concept-floating-city-design-challenge`.
- **Revision:** c-r1, 2026-11-08, sau review concept của chủ kênh.
- **Trạng thái:** **kịch bản c-r1 chờ chủ kênh đọc và nghe.**
  - Có lời dẫn hoàn chỉnh, audio nội bộ, timing đo từ audio (13:05).
  - Chưa có asset sản xuất hay card. Không claim nào được duyệt.
- **Bắt đầu đọc:**
  1. `review/SCRIPT_REVIEW.md`: đúng các câu đã đọc, mốc thời gian, claim, các quyết định cần bạn;
  2. bản nghe thử `output/floating-city-design-challenge_narration_preview_c-r1.m4a` (ngoài git);
  3. `review/REVIEW_C_R1.md`: góp ý → đã làm → kiểm tra.

## Gói tài liệu

| Mục | Tệp |
|---|---|
| A. Ba hướng kể và đề xuất | `concept/CONCEPT_OPTIONS.md` |
| B. Hợp đồng kịch bản | `concept/SCENARIO_CONTRACT.md`, `concept/scenario_contract.json` |
| C. Nghiên cứu kỹ thuật | `concept/ENGINEERING_RESEARCH.md`; `research/sources.json` (16 nguồn, 63 claim, khớp nguyên văn); `research/source_snapshots.json` |
| Mô hình tính | `analysis/design_model.py` → `analysis/results.json`, `analysis/RESULTS.md`; test `tests/test_floating_city_concept.py` |
| D. Tiến hóa thiết kế | `concept/DESIGN_EVOLUTION.md` |
| E. Dàn ý | `concept/NARRATIVE_OUTLINE.md` |
| **Lời dẫn** | `script/story.py` → `script/narration.json`, `visual_beats.json`, `chapters.json`; `script/timing.json` (khóa từ audio) |
| F. Storyboard | `concept/VISUAL_STORYBOARD.md` (44 shot, 13:05; sinh bởi `concept/build_storyboard.py`) |
| G. Asset thủ tục | `concept/BLENDER_ASSET_BLUEPRINT.md` |
| H. Khả thi sản xuất | `concept/PRODUCTION_FEASIBILITY.md` |
| I. Prototype | `concept/PROTOTYPE_REPORT.md`; `renders/prototype/` (git bỏ qua), gồm hoạt ảnh P6 |
| J. Quyết định | tệp này |

## Vì sao đáng làm
- **Câu hỏi hấp dẫn ngay**, và Studio trả lời bằng cách dựng lại thành phố từng vấn đề một, với số tính minh bạch thay cho render quảng bá.
- **Chủ đề được nghiên cứu nghiêm túc** (hai bài Nature 2026). Thông tin công khai về dự án lớn khan hiếm và mâu thuẫn (CLM_061), nên một phim cẩn thận có giá trị.
- **Hợp ngôn ngữ hình của Studio:** mặt cắt, lộ dưới nước, làm mờ, so sánh A/B. Prototype cho thấy các hình chính đọc được.

## Hướng đã chọn
**C → A, cộng phản thực tế D.**
- Một khu nổi có thật (Schoonschip).
- Một quận 10.000 người nối bờ trong vịnh kín, phao 60 m.
- Thử đặt ngoài khơi.

Review concept của chủ kênh giữ cấu trúc này và yêu cầu sáu nhóm sửa; tất cả đã làm (`review/REVIEW_C_R1.md`).

## Người xem sẽ học được gì
1. Vì sao một khối bê tông hàng nghìn tấn nổi: mỗi tấn đòi khoảng một mét khối nước.
2. Phần lớn thứ phao phải đỡ là chính nó (khoảng 55% trong thiết kế minh họa).
3. Thêm tải thì phao chìm sâu hơn. Nửa mét thân phao (thêm khoảng 4% bê tông) lấy lại mạn khô.
4. Nghiêng ít dưới một tải dời chỗ chưa nói gì về chuyển động trong sóng; nổi được mới là vấn đề đầu tiên.
5. Nhân một phao thành thành phố sinh ra mối nối. Phao to hay nhiều phao là một đánh đổi.
6. Thành phố nổi vẫn buộc vào đất liền: cọc và dây neo, cầu có khớp, cáp và ống về bờ.
7. Ra khơi đổi cả loại thân phao. Tự chủ là một điều kiện chọn thêm, không phải hệ quả tự động.
8. Phần khó nhất có thể không phải kỹ thuật: bảo trì, sinh thái, ai dùng mặt nước, chi phí.

## Điều gì là sự thật, tính toán, giả định, đề xuất, chưa xác minh

| Loại | Số claim | Ví dụ |
|---|---|---|
| ESTABLISHED_FACT | 39 | Archimedes; Schoonschip (46 hộ, phao bê tông, nhà 340–350 t, một đầu nối lưới); nhà nổi Hà Lan tựa cọc, rung khi bão; các câu hỏi mở được nghiên cứu nêu tên |
| CALCULATED_ESTIMATE | 9 | Mớn nước khoảng 3 m; 55% là thân phao; mạn khô 1,04 → 0,71 → 1,15 m; nghiêng khoảng 0,4°; 66 cm (hai phao nổi độc lập); khoảng 209 phao 40 m, 93 phao 60 m hoặc 34 phao 100 m; dốc cầu khoảng 3° |
| DESIGN_ASSUMPTION | 5 | 10.000 cư dân, vịnh kín, nối bờ; dải mực nước 2 m; 40 m² = 30 + 10; phao 60 m |
| SPECULATIVE_PROPOSAL | 9 | OCEANIX Busan; concept 50.000 người ngoài khơi của Ruzzo 2026 |
| UNVERIFIED | 1 | Tình trạng OCEANIX Busan, chỉ cho dự án đã kiểm và ngày kiểm |

## Đã sẵn sàng cho sản xuất chưa?
**Chưa.** Thứ tự:
1. **Chủ kênh đọc và nghe kịch bản c-r1**, quyết các mục dưới.
2. **Sửa kịch bản** theo quyết định (nếu cắt, chạy lại `narrate` → `lock-audio`).
3. **Dựng họ asset `floating` và site `bay`**, cùng các năng lực nhỏ: mặt cắt, SINK/RISE, TILT, CONCEPT_MOTION có nhãn; site biển mở; nhà theo chức năng.
4. **Đoạn thử có lời dẫn** trên asset thật cho chuỗi "thêm tải → chìm → sửa thân" (`tools/excerpt.py`), để chủ kênh duyệt chất lượng hình trước khi làm cả phim.
5. **Benchmark một shot cảnh quận ở 4K**, rồi theo playbook.

## Cần chủ kênh quyết
1. **Thời lượng 13:05:** giữ (trong 8–15 phút) hay cắt về khoảng 11 phút (danh sách chỗ cắt trong `review/SCRIPT_REVIEW_NOTES.md`)?
2. **Phát âm "Schoonschip":** giữ cách đọc tiếng Anh hóa, thêm override sau khi nghe, hay nhắc ít hơn?
3. **Ảnh Schoonschip:** cho phép CC BY-SA, xin phép, hay giữ sơ đồ?
4. **Giọng `am_michael` cho dự án này.**
5. **Duyệt claim** mà phim dùng, khi kịch bản đã chốt.

## Định nghĩa hoàn thành (brief mục 21)

| # | Điều kiện | Trạng thái |
|---|---|---|
| 1–2 | Ba concept, một đề xuất | Xong; cấu trúc được giữ sau review |
| 3 | Giả định rõ ràng | Xong (có test; làm rõ ở c-r1, không đổi giá trị) |
| 4 | Nguồn tin cậy | Xong (14 nguồn ngoài, 49 claim ngoài; 7 nguồn không mở được hoặc không đọc, ghi ở `not_used`) |
| 5 | Thay đổi thiết kế có lý do | Xong; nhánh số liên tục ở c-r1 |
| 6 | Dàn ý 10–12 phút | Lời dẫn hoàn chỉnh **13:05** đo từ audio; trong 8–15, chờ quyết định |
| 7–8 | Storyboard có hình lộ ra; mỗi cảnh có chiến lược khả thi | Xong (44 shot, mỗi shot một hạng khả thi) |
| 9 | Bản thiết kế asset | Xong |
| 10 | Giới hạn và claim bất định | Xong |
| 11 | Prototype qua kiểm tra hình | P1, P3, P4, P5 đạt; P2 cho thấy phải cận cảnh; P6 (hoạt ảnh) đạt cho số liệu, đạt một phần cho hình |
| 12 | Sẵn sàng cho buổi duyệt | **Có**: duyệt kịch bản c-r1 |
