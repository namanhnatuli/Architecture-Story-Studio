# Tiến hóa thiết kế: A → B → C (và phản thực tế D)

**Quy tắc chung:**
- Mỗi thay đổi trả lời một vấn đề đã được chỉ ra trên hình **trước** khi thay đổi xuất hiện.
- Không thiết kế nào bị làm cho "ngớ ngẩn" để có xung đột.
- Khi có nhiều lời giải hợp lý, phim nói vì sao một lời giải được ưu tiên **dưới các giả định của kịch bản**, không nói nó luôn tốt hơn.
- Số liệu lấy từ `analysis/results.json` (CALCULATED_ESTIMATE, hộp lý tưởng, nước lặng).

## Design A: phao đầu tiên

| | |
|---|---|
| **Hình** | Một phao bê tông 40 × 40 m, sâu 4 m, 16 khoang kín nước; bốn khối nhà 3 tầng phủ khoảng 40% mặt sàn; một cầu có khớp nối với cầu cảng. |
| **Câu hỏi** | Vì sao một khối bê tông hàng nghìn tấn lại nổi? |
| **Nguyên lý** | Archimedes (CLM_001), hình dạng (CLM_002), chở nặng thì ngập sâu (CLM_003). |
| **Số minh họa** | Khoảng 4.850 t, mớn nước khoảng 3,0 m, mạn khô khoảng 1,0 m. **55% khối lượng là chính thân phao.** Thêm một tầng nhà thì chìm thêm khoảng 33 cm. |
| **Vấn đề lộ ra 1** | Phương án nhà nặng (0,9 t/m² sàn) chỉ còn khoảng 0,7 m mạn khô. |
| **Sửa A′** | Thân sâu 4,5 m: chỉ thêm khoảng 106 t bê tông, mạn khô về khoảng 1,1 m. Nhà giữ thấp tầng để trọng tâm thấp. *Lựa chọn khác hợp lý:* nhà nhẹ hơn (khung gỗ, như Schoonschip, CLM_012). Phim cho thấy cả hai và nói kịch bản chọn thân sâu hơn vì muốn giữ tự do vật liệu cho nhà. |
| **Vấn đề lộ ra 2** | Phao có lật không? Không phải trong nước lặng: phao rộng 40 m và nông có BM khoảng 45 m; dời 100 t ra mép 15 m chỉ nghiêng chưa tới nửa độ (CLM_005, CLM_009). Nhưng phao "cứng" thì **bám theo mặt nước** (CLM_007). Vấn đề chuyển sang sóng và tiện nghi. |
| **Mục tiêu hình** | Người xem hiểu vì sao phao nổi, và vì sao bê tông nặng lại là một phần lời giải (đối trọng, CLM_021). |

## Design B: khu nối nhiều phao

| | |
|---|---|
| **Hình** | Năm tới mười phao 40 × 40 m quanh một bể nước nhỏ, cầu đi bộ mềm qua các khe khoảng 5 m, cọc neo ở góc, một nhà cộng đồng. Khoảng 250–500 cư dân, tức gấp 2,5–5 lần Schoonschip. |
| **Câu hỏi** | Sao không hàn mọi phao thành một tấm? |
| **Vấn đề 1: tải khác nhau** | Hai phao giống nhau, một mang nhà 2 tầng, một mang nhà 4 tầng: mặt sàn lệch nhau khoảng 0,66 m. Một cầu cứng giữa chúng sẽ bị bẻ. Lời giải hợp lý: khớp mềm, hoặc dằn (ballast) để cân mớn nước. Cả hai có giá: khớp phải kiểm tra, dằn làm phao nặng thêm. |
| **Vấn đề 2: chuyển động tương đối** | Sóng gió trong vịnh làm các phao nhấp nhô lệch pha nhau (chỉ minh họa khái niệm). Mối nối là nơi tập trung ứng suất (CLM_042). Nghiên cứu giữ khe và nối mềm để module không chạm nhau và mối nối không quá tải (CLM_056). |
| **Vấn đề 3: hạ tầng qua khe** | Điện, nước sạch, nước thải phải vượt khe đang chuyển động: ống mềm, cáp chống nước, bơm (CLM_023). Tiền lệ: cầu tàu chung mang hạ tầng (CLM_015), một đầu nối lưới điện cho cả khu (CLM_016). |
| **Vấn đề 4: giữ vị trí** | Phao không đứng yên trên nước. Cọc thép cho phao trượt lên xuống theo mực nước (CLM_020, CLM_041). Dải 2 m mực nước (giả định) buộc cầu nối bờ phải có khớp: dốc khoảng 3° với cầu 25 m. |
| **Mục tiêu hình** | Nhân bản một phao **không** phải là sao chép: khe, khớp, ống mềm và cọc xuất hiện vì từng vấn đề. |

## Design C: quận nổi được che chắn (10.000 cư dân)

| | |
|---|---|
| **Hình** | Khoảng 33 ha mặt phao (giả định 40 m² sàn mỗi cư dân, nhà 3 tầng phủ 40%; dải 25–42 ha). Một bể trong được che chắn. Nhà ở ở vòng trong; phao dịch vụ, chợ, bến và cơ sở hạ tầng ở vòng ngoài. Đê chắn sóng ở phía hở. Cọc gần bờ, dây neo ở phần nước sâu hơn. Ba cầu link-span. Trục hạ tầng chạy theo cầu. |
| **Câu hỏi** | Mười nghìn người cần gì ngoài nhà? |
| **Quyết định 1: phao to hay nhiều phao** | Với phao 40 m cần khoảng 209 phao và tới khoảng 390 mối nối. Với phao 100 m chỉ còn khoảng 34 phao và khoảng 60 mối nối, nhưng mỗi phao khoảng 30.000 t, khó đúc, hạ thủy và kéo hơn (CLM_014), và uốn theo sóng nhiều hơn (CLM_053). **Không có đáp án chung.** Kịch bản dùng phao trung bình (60–80 m) cho khu ở, phao nhỏ cho chức năng phải thay được. Đây là lựa chọn có lý do, không phải tối ưu đã tính. |
| **Quyết định 2: nhà ở ở trong** | Như nghiên cứu đề xuất (CLM_055): chức năng chịu được chuyển động lớn hơn ở vòng ngoài, che cho nhà ở. |
| **Quyết định 3: che chắn** | Chọn địa điểm trước (CLM_050), đê chắn sau. Đê nổi có giới hạn với sóng dài (CLM_051), và truyền sóng qua đê nổi chưa giải hết (CLM_052). Phim không nói đê "loại bỏ" rủi ro bão. |
| **Quyết định 4: neo theo độ sâu** | Cọc ở phần nông; dây neo dùng chung ở phần sâu. Sâu hơn thì đắt hơn, phi tuyến (CLM_054). Không định cỡ. |
| **Quyết định 5: thành phố vẫn buộc vào đất liền** | Điện, nước, nước thải, lương thực qua cầu (CLM_043). Mặt trời trên mái chỉ giảm phụ thuộc. Hai lối thoát độc lập cho mỗi phao; bến tàu cứu hộ. |
| **Quyết định 6: thay được** | Module tháo, kéo đi sửa hay thay được. Đây là một lợi thế thật của kết cấu nổi (CLM_041); ăn mòn cốt thép là lý do phải kiểm tra (CLM_059). |
| **Tổng lượng chiếm nước (minh họa)** | Khoảng 1 triệu tấn nước biển (0,7–1,4 triệu theo giả định). Phim kể như cỡ, không như kết quả. |
| **Mục tiêu hình** | Thành phố như một **hệ thống tích hợp**, không phải một đám nhà nổi: lớp nhà làm mờ đi, lộ mạng hạ tầng, neo và đê. |

## Design D (phản thực tế): đưa thiết kế C ra khơi

| | |
|---|---|
| **Hình** | Cùng quận C, kéo ra biển mở (sơ đồ). Sóng lừng dài đi qua đê nổi (khái niệm, có nhãn). Dây neo dài ra theo đáy biển sâu dần. Cầu nối bờ biến mất. |
| **Điều thay đổi** | Sóng dài: đê nổi có thể không đủ (CLM_051). Độ sâu: neo dài và đắt hơn, phi tuyến (CLM_054). Xa bờ: không còn cầu cho điện, nước, nước thải, cấp cứu; phải tự chủ (CLM_043), mà một concept tự chủ cần năng lượng rất lớn, gần một nửa cho lương thực (CLM_058). |
| **Thiết kế khác hẳn** | Nghiên cứu ngoài khơi dùng phao bán chìm trên cột, neo mềm, sau một đê nổi neo căng (CLM_062). Đó là một loại kết cấu khác, không phải phao hộp dời chỗ. |
| **Kết luận chương** | Địa điểm là một nửa của thiết kế. Không thể dời thiết kế ven bờ ra khơi mà không thiết kế lại từ đầu. |

## Những gì phim không làm
- Không cho một thiết kế "thất bại" khi phân tích không cho thấy điều đó. Mọi vấn đề trên là vấn đề được nguồn nêu tên, hoặc đến từ phép tính minh bạch.
- Không xếp hạng phao lục giác, chữ nhật hay tam giác. Phao chữ nhật được chọn vì dễ đúc, xếp khít và tính trong kịch bản.
- Không kết luận "khả thi" hay "bất khả". Phán quyết chia theo quy mô và địa điểm (`NARRATIVE_OUTLINE.md`, chương 8).
