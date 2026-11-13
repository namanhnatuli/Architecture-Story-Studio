# Đề xuất thumbnail: Could We Build an Entire City That Floats?

**Trạng thái:** đề xuất của agent, chủ kênh chưa chọn bản nào. Chủ kênh quyết dùng bản nào, và có chạy A/B test hay không. Studio không đăng và không tự đổi gì trên YouTube.

## Ba bản (trong `review/thumbnails/`)
Mỗi bản có hai cỡ: 1920×1080 (`.jpg`) và 1280×720 (`_1280.jpg`). Tất cả dưới 0,5 MB; giới hạn của YouTube là 2 MB.

| Bản | Chữ | Hình | Câu trong phim làm căn cứ |
|---|---|---|---|
| **A** `thumb_A_10000_people_no_land` | 10,000 PEOPLE / NO LAND | Toàn quận nổi (SC_001), nhìn chéo từ phía tây: hồ giữa quận, kênh nước giữa các phao, đê chắn sóng | B01: "10,000 people, with homes, schools… And not one of them is standing on land." |
| **B** `thumb_B_4800_tons_and_it_floats` | 4,800 TONS / AND IT FLOATS | Mặt cắt phao đầu tiên (SC_008): hai tòa nhà ba tầng trên thân phao rỗng, mặt nước | B08: "Altogether it weighs about 4,800 tons, and floats about 3 meters deep." |
| **C** `thumb_C_what_holds_it_in_place` | WHAT HOLDS IT / IN PLACE? | Khu 5 phao nhìn ngang mặt nước (SC_024): dãy nhà phía trên, dây neo và neo dưới đáy | B22: "Something also has to hold the city in place." B24: dây neo neo vào đáy biển |

- **Ba hướng khác nhau để so:** quy mô (A), vật lý (B), bí ẩn (C).
- **Chữ bổ sung cho tiêu đề, không lặp lại.** Tiêu đề đã hỏi "a city that floats", nên không bản nào ghi lại câu đó.
- **Theo nhận xét của chủ kênh về thumbnail Gothic (vòng 1):**
  - mỗi bản một thông điệp, không dòng phụ, không đường kẻ;
  - công trình lớn, tràn mép khung;
  - chữ serif đậm hai dòng, trắng và vàng, viền tối, giống phim Gothic.
- **Hình lấy đúng từ mô hình của phim**, render lại sạch: ẩn nhãn chú thích, không watermark.
  - Bản A đặt camera riêng để quận lớn trong khung mà không lộ mép bãi nước. Bản B và C dời hoặc thu phóng khung chiếu trực giao của phim.
  - Phần "trời" xám nhạt của bản B và C được thay bằng nền navy.
  - Chỉnh màu nhẹ (độ bão hòa +15%, tương phản +6%); không thêm vật gì phim không có.
- **Font Charter Black** của macOS. Georgia (thử trước) dùng chữ số kiểu cũ, làm "10,000" và "4,800" nhỏ và lệch dòng.

## Đọc được ở cỡ nhỏ
- Agent đã xem cả ba ở 320×180 (trang chủ) và 168×94 (cột gợi ý): chữ đọc được ở cả hai cỡ.
- Bản C có chữ nhỏ nhất, vì phải nằm trong khoảng trời phía trên dãy nhà.
- Dây neo ở bản C mảnh, ở cỡ 168 px chỉ còn thấy thoáng. Phần dễ nhận nhất ở cỡ đó là dãy nhà trên mặt nước và các khối neo dưới đáy.

## Nếu chạy A/B test
- YouTube "Test & Compare" cho thử tối đa 3 thumbnail, vừa đủ cho A, B và C. Giữ nguyên tiêu đề trong lúc test.
- Mỗi lần chỉ đổi một biến; muốn thử tiêu đề thì làm vòng sau, với thumbnail thắng.
- Tiêu đề hiện tại: "Could We Build an Entire City That Floats?" (`project.json` → `publication_metadata.title`).

## Dựng lại
- **Script:** `review/thumbnails/make/`:
  - `still.py`: render một khung sạch từ `scenes/SC_xxx.blend`, mỗi lúc một Blender; không ghi đè file `.blend`;
  - `specs.json`: shot, frame, camera và phần cần ẩn của từng bản;
  - `compose.py`: nền, chỉnh màu và chữ; cần Pillow 13.0.0.
- Chạy lại `compose.py` trên cùng ảnh render cho ra file giống từng byte với các file đang có.
- **Thời gian render:** mỗi ảnh 4K mất 3–8 giây.
