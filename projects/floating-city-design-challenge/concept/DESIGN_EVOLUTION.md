# Tiến hóa thiết kế: A → B → C (và phản thực tế D), revision c-r2

**Quy tắc chung:**
- Mỗi thay đổi trả lời một vấn đề đã được chỉ ra trên hình **trước** khi thay đổi xuất hiện.
- Không thiết kế nào bị làm cho "ngớ ngẩn" để có xung đột.
- Khi có nhiều lời giải hợp lý, phim nói vì sao một lời giải được chọn **dưới các giả định của kịch bản**.
- Số liệu lấy từ `analysis/results.json` (CALCULATED_ESTIMATE, hộp lý tưởng, nước lặng, góc nhỏ). Độ dày thân phao chỉ là giả định để tính khối lượng, không phải kết quả thiết kế kết cấu.

## Design A: phao đầu tiên

| | |
|---|---|
| **Hình** | Phao bê tông 40 × 40 m, sâu 4 m, 16 khoang kín nước; bốn khối nhà 3 tầng phủ khoảng 40% mặt sàn; cầu có khớp nối cầu cảng. |
| **Câu hỏi** | Vì sao một khối bê tông hàng nghìn tấn lại nổi? |
| **Nguyên lý** | Hình dạng (CLM_002, CLM_101), Archimedes (CLM_001, CLM_102), chở nặng thì ngập sâu (CLM_003). |
| **Số minh họa** | Khoảng 4.850 t, mớn nước khoảng 2,96 m, mạn khô khoảng 1,04 m (tải tĩnh nhà 0,6 t/m² sàn). Hơn nửa khối lượng (55%) là thân phao (CLM_104). |
| **Vấn đề lộ ra** | Thêm tầng thứ tư, **cùng tải tĩnh 0,6 t/m²**: phao chìm thêm khoảng 33 cm, mạn khô còn khoảng 0,71 m (CLM_105). |
| **Sửa A′ (cùng nhánh)** | Giữ 4 tầng, thân sâu 4,5 m: thêm khoảng 106 t bê tông (4% bê tông thân phao), mạn khô về khoảng 1,15 m (CLM_105). *Cách khác hợp lý:* nhà nhẹ hơn. |
| **Nổi được chưa đủ** | Dời 100 t ra cách tâm 15 m: phao nghiêng khoảng 0,4° **trong trường hợp minh họa này** (CLM_009, CLM_106; góc nhỏ, CLM_006). Con số này nói rất ít về cách phao chuyển động trong sóng; câu hỏi đó để dành cho C4. |
| **Mục tiêu hình** | Người xem hiểu vì sao phao nổi, vì sao thêm tải đòi một lần sửa, và vì sao "nổi" mới là vấn đề đầu tiên. |

## Design B: khu nối nhiều phao

| | |
|---|---|
| **Hình** | **Quay về bản 3 tầng, thân 4 m** (c-r2: nhánh sửa ở A chỉ để giải thích tải). Năm phao 40 m quanh một bể nhỏ, cầu đi bộ có khớp qua các khe, cọc ở góc. Khoảng 50 người mỗi phao (48 với 3 tầng; 64 nếu 4 tầng; CLM_108). |
| **Câu hỏi** | Sao không nối tất cả thành một tấm? |
| **Tải khác nhau** | Hai phao giống nhau, nhà 2 tầng và 4 tầng, **nếu nổi độc lập** thì mặt sàn lệch khoảng 0,66 m (CLM_107). Khi nối cứng, lực ở mối nối làm đổi cân bằng của cả hai, nên phép tính này **không** chứng minh mối nối cứng sẽ hỏng. Nó chỉ cho thấy tải khác nhau thêm một yêu cầu cho mối nối. Thiết kế này chọn cầu đi bộ có khớp; dằn để cân mớn nước là cách khác. Hình không tô đỏ phương án nào. |
| **Chuyển động tương đối** | Chuyển động khái niệm có nhãn bắt buộc. Mối nối là nơi tập trung ứng suất (CLM_042). Nghiên cứu nối mềm và giữ khoảng cách đủ để không va chạm, vì neo mềm cho phép dịch ngang khá lớn; chân vịt dự phòng để tránh va chạm và quá tải mối nối (CLM_056). |
| **Hạ tầng qua khe** | Ống mềm, cáp chống nước, bơm (CLM_023); tiền lệ Schoonschip: một đầu nối lưới cho cả khu (CLM_016). |
| **Giữ vị trí** | Cọc, phao trượt theo mực nước (CLM_020, CLM_041); dải 2 m (giả định, CLM_122) cộng thay đổi mớn nước theo tải (khoảng 0,44 m) buộc cầu nối bờ có khớp: khoảng 3° (±2,8°) với cầu 25 m, khớp ở giữa dải; chỉ mực nước thì khoảng 2,3° (CLM_109). |

## Design C: quận nổi được che chắn (10.000 cư dân)

| | |
|---|---|
| **Diện tích** | 40 m² sàn mỗi cư dân, gồm 30 m² nhà ở và 10 m² trường học, phòng khám, cửa hàng, dịch vụ (CLM_124). Nhà 3 tầng phủ 40%, nên cần khoảng 33 ha mặt phao. |
| **Phao to hay nhiều phao** | Cho cùng khoảng 33 ha (CLM_108): phao 40 m là 209 phao (tới khoảng 390 mối nối); phao 100 m là 34 phao (khoảng 60 mối nối, mỗi phao khoảng 30.000 t). Phao Schoonschip đã quá to cho ụ khô truyền thống (CLM_014). **Quận dùng phao 60 m với nhà 3 tầng: 93 phao, tới 180 mối nối, mỗi phao khoảng 10.800 t, khoảng 108 người** (CLM_125). Đây là lựa chọn ở giữa cho bản minh họa, không phải tối ưu. |
| **Bố cục** | Nhà ở vòng trong; chức năng chịu được chuyển động lớn hơn ở vòng ngoài, như nghiên cứu đề xuất (CLM_055). Đê chắn ở phía mở ra biển, có giới hạn (CLM_051, CLM_052). |
| **Neo theo độ sâu** | Cọc ở phần nông; dây neo dùng chung ở phần sâu (CLM_055). Sâu hơn thì dây dài hơn, neo sâu hơn, chi phí cao hơn (CLM_054). Không định cỡ. |
| **Buộc vào đất liền** | Điện, nước, nước thải, lương thực qua cầu (CLM_043, CLM_123). Hai lối ra cho mỗi phao, bến tàu cứu hộ. |
| **Thay được** | Module tháo, kéo đi sửa (CLM_041); ăn mòn cốt thép là lý do phải kiểm tra (CLM_059). |
| **Tổng (minh họa)** | Khoảng 1,0 triệu tấn lượng chiếm nước cho **93 phao tiêu chuẩn**. **Không gồm:** phao cảng và dịch vụ, đê, cầu, neo, nhà máy và mạng hạ tầng. Phép tính cho thấy yêu cầu nổi cơ bản, **không** cho thấy cả quận vận hành được. |

## Design D (phản thực tế): kéo quận C ra khơi

| | |
|---|---|
| **Hình** | Quận nhỏ trên biển mở (3D). Sóng dài khái niệm đi qua đê nổi (có nhãn). Dưới nước, đáy sâu dần, dây neo dài ra. |
| **(a) Điều đổi vì xa bờ** | Sóng dài: đê nổi có thể không đủ (CLM_051). Đáy sâu hơn: dây và neo dài, sâu hơn (CLM_054). Kết nối, bảo trì và tiếp tế khó hơn: cáp, ống và tàu vẫn có thể, nhưng mọi liên kết dài và lộ hơn (CLM_043). |
| **(b) Nếu chọn thêm điều kiện tự chủ** | Đây là một **lựa chọn thêm**, không mặc định khi ra khơi. Phải thêm hệ năng lượng, nước, lương thực. Trong concept 2026 đã chọn tự chủ, lương thực chiếm gần nửa nhu cầu năng lượng (CLM_058). |
| **Một loại thân khác** | Nghiên cứu ngoài khơi dùng phao bán chìm trên cột, sau một đê nổi (CLM_062). 3D đặt cạnh phao hộp. |
| **Kết luận chương** | Ra khơi không phải cùng một thành phố dời xa hơn. Đó là một thiết kế khác. |

## Những gì phim không làm
- Không cho một thiết kế "thất bại" khi phân tích không cho thấy điều đó.
- Không suy chuyển động trong sóng từ độ nghiêng tĩnh hay từ GM.
- Không xếp hạng hình dạng phao.
- Không kết luận "khả thi" hay "bất khả" cho cả quận. Phán quyết chia theo quy mô và địa điểm, và nói rõ điều phép tính không chứng minh.
