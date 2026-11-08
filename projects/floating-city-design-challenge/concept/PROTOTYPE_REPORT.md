# Bản thử hình (prototype) cho concept

- **Mục đích:** kiểm xem các hình giải thích quan trọng nhất có làm được không, trước khi đầu tư vào họ asset sản xuất. Không phải asset sản xuất, không gắn vào engine hay planner.
- **Lệnh** (một Blender, không MCP):
  ```bash
  /Applications/Blender.app/Contents/MacOS/Blender --background --factory-startup \
      --python projects/floating-city-design-challenge/prototype/floating_prototype.py -- [--shot NAME] [--res 960x540]
  ```
- **Kết quả:** `renders/prototype/P*.png` và `renders/prototype/CONTACT_SHEET.png`. Thư mục này git bỏ qua, theo quy tắc không commit ảnh render. Chạy lại lệnh trên để sinh lại.
- **Hình học:** dùng đúng số của `analysis/results.json`: phao 40 × 40 m, sâu 4 m, mớn nước 2,958 m, tầng thứ tư làm chìm thêm 33,2 cm, vách ngăn mỗi 10 m. Độ sâu nước 15 m (trong dải 12–25 m của kịch bản).
- **Ánh sáng và màu:** theo `config/visual_style.json` (key và fill sun, world mềm, AgX Medium High Contrast) và `asset_library/materials/stylized_materials.json`.
- **Chi phí:** 6 still ở 960 × 540 EEVEE, khoảng 1 giây mỗi still. Không render chuỗi frame, không render chương, không video.

## Từng ảnh: điều đã kiểm và kết quả

| Ảnh | Kiểm điều gì | Kết quả |
|---|---|---|
| **P1 `design_A_cutaway`** | Mặt cắt dưới nước có làm Archimedes dễ hiểu không (Reveal 1) | **Đạt** sau hai lần sửa. Vách ngăn (tấm mặt cắt tối), mảng vàng là khối nước bị chiếm chỗ, đường nước, mạn khô phía trên đều đọc được ở 960 × 540. Lỗi gặp: một vách ngăn nằm đúng trên mặt cắt che hết mặt cắt (đã sửa: bỏ vách trùng mặt cắt). Bài học cho bộ sinh: kiểm tra "không có thành phần nào nằm trên mặt cắt". |
| **P2 `load_compare`** | Thêm một tầng có thấy phao chìm sâu hơn không (Reveal 2) | **Không đạt ở khung toàn cảnh.** 33 cm trên phao 40 m gần như không thấy. Đây là phát hiện đúng, không phải lỗi dựng hình: phải cận cảnh hoặc dùng số. |
| **P2b `draft_marks_closeup`** | Thước mớn nước cận cảnh | **Đạt một phần.** Thước 1 m và đường nước đọc được. Cần thêm nhãn số và một vạch "trước/sau" khi làm bằng `SINK` thật (SH09). |
| **P3 `neighbourhood`** | Ba phao nối nhau (Design B rút gọn): khe, cầu đi bộ, cọc | **Đạt.** Khe, cầu đi bộ và cọc ở góc đọc rõ từ góc three-quarter. Đường hạ tầng dưới sàn không thấy được, nên phải có shot cận (SH15). |
| **P4 `mooring_piles_water_ghosted`** | Lộ hệ neo dưới mặt nước (Reveal 4) | **Đạt sau khi sửa.** Lần đầu, nước làm mờ quá nên phao trông như sàn đặt trên cột, tức là gợi ý sai rằng cọc đỡ phao. Đã sửa bằng một tấm mặt nước rõ, khối nước mờ nhẹ. Bài học: làm mờ hai bước (thấy mặt nước, rồi làm mờ) là bắt buộc. |
| **P5 `mooring_lines_water_ghosted`** | Dây neo và neo ở đáy | **Đạt một phần.** Dây và neo thấy được nhưng nhạt sau mặt nước. Bản sản xuất cần HIGHLIGHT dây khi lộ ra. Mép khối nước hiện ở góc trên: site cần rộng hơn hoặc mép mờ dần. |

## Câu hỏi khả thi và câu trả lời

| Câu hỏi | Trả lời |
|---|---|
| Hình giải thích quan trọng nhất (Archimedes bằng mặt cắt) làm được không? | Có (P1). |
| So sánh trước và sau làm được không? | Có (P2, P2b). Nhưng thay đổi nhỏ phải cận cảnh. |
| Mặt cắt làm được không? | Có, bằng cách bộ sinh dựng nửa mô hình và tấm mặt cắt. Không cần boolean. |
| Lộ hệ neo dưới nước làm được không? | Có (P4, P5), với nước hai lớp. |
| Có cần mô phỏng chất lỏng không? | Không. Chưa thử hoạt ảnh sóng khái niệm. Brief chỉ cho một thử nghiệm hoạt ảnh "nếu cần", và với concept thì không cần: năng lực `CONCEPT_MOTION` được đánh giá trên giấy (`PRODUCTION_FEASIBILITY.md`). |

## Chưa kiểm
- Bất kỳ hoạt ảnh nào: SINK, RISE, CONCEPT_MOTION, SEQUENCE trên họ mới.
- Cảnh quận C đầy đủ: khoảng 50–200 phao, đê, mạng hạ tầng. Chưa có benchmark 4K.
- Chú thích của Studio trên các cảnh này.
