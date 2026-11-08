# Hợp đồng kịch bản: SCN_FLOATCITY_COASTAL_01

- **Bản máy đọc:** `concept/scenario_contract.json`. Đây là nguồn duy nhất của các giá trị; `analysis/design_model.py` đọc từ đó.
- **Trạng thái:** khóa cho buổi duyệt concept (2026-11-08).
- **Quy tắc đổi:** mọi thay đổi là một revision mới (`_02`, `_03`…), ghi lý do ở cuối tệp này. Không bao giờ đổi giá trị để một thiết kế "qua".

## Một câu
Một phần mở rộng nổi **nối với bờ** của một thành phố ven biển có sẵn, trong **vịnh hay bể cảng được che chắn**, xây theo ba pha (một phao → một khu → một quận) hướng tới 10.000 cư dân. Đại dương mở chỉ xuất hiện như một phản thực tế (Design D).

## Các trường

| Trường | Giá trị | Loại | Căn cứ |
|---|---|---|---|
| Kiểu kịch bản | Phần mở rộng nổi nối bờ, xây theo pha | DESIGN_ASSUMPTION | Giả thuyết khởi đầu chủ kênh ưu tiên; gần các tiền lệ đã xây (CLM_010, CLM_020); nghiên cứu cũng đặt cả concept lớn ở vùng nước có đà gió hạn chế (CLM_050) |
| Dân số | 10.000 cư dân (mục tiêu kịch bản) | DESIGN_ASSUMPTION | Brief. Mốc so sánh: Schoonschip hơn 100 người (CLM_011); OCEANIX Busan đề xuất 12.000 cư dân và khách (CLM_031) |
| Địa điểm | Vịnh hay bể cảng có đà gió hạn chế; sóng lừng đại dương bị chặn bởi mũi đất hoặc công trình sẵn có | DESIGN_ASSUMPTION | CLM_050, CLM_048, CLM_051 |
| Khoảng cách tới bờ | 0–800 m | DESIGN_ASSUMPTION | Đi bộ được, trong tầm cầu link-span (CLM_031) |
| Độ sâu nước | 12–25 m | DESIGN_ASSUMPTION | Đủ sâu dưới mớn nước khoảng 3 m; đủ nông để pha đầu dùng cọc. Sâu hơn thì neo đắt hơn, phi tuyến (CLM_054) |
| Khối lượng riêng nước | 1.025 kg/m³ | ESTABLISHED_FACT | CLM_004 (sách giáo khoa: 1.030 ở 0 °C, CLM_008) |
| Gia tốc trọng trường | 9,81 m/s² | ESTABLISHED_FACT | CLM_004 |
| Sóng đại diện | Sóng gió đà ngắn trong vịnh; không có sóng lừng đại dương. **Không chốt chiều cao hay chu kỳ sóng thiết kế** | DESIGN_ASSUMPTION | Cần số liệu khí tượng hải văn của địa điểm. Phim không nói biên độ |
| Gió và bão | Có bão mạnh thỉnh thoảng, kèm nước dâng. Thiết kế phải giữ an toàn cho người; không giả định "không hư hỏng" | DESIGN_ASSUMPTION | Brief 6.6; cư dân Amsterdam vẫn thấy rung lắc khi bão (CLM_022) |
| Dải mực nước (triều + nước dâng) | 2,0 m (minh họa) | DESIGN_ASSUMPTION | Chỉ để cho thấy vì sao phao trượt theo cọc và cầu phải có khớp; kết cấu nổi đi theo mực nước (CLM_041) |
| Đáy biển | Trầm tích mềm (cát hay sét) trên nền chắc hơn, chưa khảo sát | DESIGN_ASSUMPTION | CLM_054. Không nêu loại neo như đã định cỡ |
| Nối bờ | Cầu link-span có khớp (đi bộ, xe đạp, xe dịch vụ và cấp cứu nhẹ), hạ tầng chạy dọc cầu; taxi nước và phà giữa các phao | DESIGN_ASSUMPTION | CLM_031, CLM_023, CLM_015 |
| Công nghệ xây dựng | Phao bê tông cốt thép có khoang kín nước, đúc trong ụ hoặc trên bờ rồi kéo tới; nhà thấp tầng khung gỗ hay thép nhẹ | DESIGN_ASSUMPTION | Tiền lệ Schoonschip (CLM_012, CLM_014, CLM_021) |
| Vật liệu | Thân bê tông 2.400 kg/m³; nhà 2–4 tầng để giữ trọng tâm thấp; mối nối thép kiểm tra và thay được | DESIGN_ASSUMPTION | CLM_008; ăn mòn cốt thép do clorua (CLM_059) |
| Năng lượng ngoài | Lưới điện thành phố qua cầu; mặt trời và pin trên phao chỉ giảm, không thay lưới | DESIGN_ASSUMPTION | Tiền lệ Schoonschip (CLM_016). Không nói tự cung tự cấp |
| Nước sạch | Từ mạng nước thành phố qua cầu; nước mưa cho mục đích không uống. Không khử mặn | DESIGN_ASSUMPTION | CLM_043 |
| Nước thải | Tách nước xám và nước đen, bơm về nhà máy trên bờ | DESIGN_ASSUMPTION | CLM_017, CLM_023 |
| Lương thực | Từ đất liền như mọi quận khác; không đặt mục tiêu tự chủ | DESIGN_ASSUMPTION | Sản xuất lương thực tại chỗ chiếm gần nửa nhu cầu năng lượng của một concept tự chủ (CLM_058) |
| Cấp cứu | Mỗi phao có hai lối độc lập ra bờ (cầu hoặc phao bên cạnh) và bến cho tàu cứu hỏa, cứu hộ; chỗ trú tại chỗ trên mỗi phao khu | DESIGN_ASSUMPTION | Không khẳng định đạt quy chuẩn phòng cháy nào |
| Mục tiêu thiết kế | (1) mỗi pha dùng được độc lập; (2) nhà ở đặt nơi chuyển động nhỏ nhất (CLM_055); (3) mọi module, mối nối, phần neo đều kiểm tra và thay được; (4) hạ tầng nối bờ, bờ nước công cộng, không thành khu khép kín (CLM_046) | DESIGN_ASSUMPTION | Brief mục 2 và 8 |
| Hình học module (cho phép tính) | Phao A 40 × 40 m, sâu 4 m, sàn và tường 0,25 m, vách ngăn mỗi 10 m dày 0,2 m; nhà phủ 40%, 3 tầng × 3 m; tải tĩnh nhà 0,4 / 0,6 / 0,9 t/m² sàn; tải thay đổi 0,25 t/m²; hoàn thiện mặt sàn 0,2 t/m²; 30 / 40 / 50 m² sàn mỗi cư dân | DESIGN_ASSUMPTION | Hợp lý cho một phác thảo concept và được cho thay đổi trong phép thử độ nhạy; **không** là số đo hay số quy chuẩn |
| Loại trừ | Ngoài khơi (chỉ là phản thực tế); chủ quyền và seasteading; nhà cao tầng; xe riêng; tự cung tự cấp; công nghiệp; mọi khẳng định về đủ an toàn kết cấu, neo, bão hay tiện nghi; con số chi phí | DESIGN_ASSUMPTION | Brief mục 5–7 |
| Bất định | Khí tượng hải văn địa điểm; hydro-elastic (CLM_053); tải và mỏi mối nối (CLM_042, CLM_056); thiết kế neo và cọc (CLM_054); sinh thái (CLM_044); quản trị, sở hữu, bảo hiểm (CLM_045); chi phí (CLM_061) | UNVERIFIED | Mỗi mục được nêu tên trong phần kết luận của phim |

## Những gì phim được và không được nói từ hợp đồng này
- **Được:** "In our scenario…", "under these assumptions…", "in our illustrative design, the platform sits about three metres deep". Mọi con số tính ra đều kèm chữ *illustrative* hoặc *in our design*.
- **Không:** đưa một giá trị DESIGN_ASSUMPTION thành sự thật ("bays like this have 2-metre tides"). Không nói thành phố "would survive" một cơn bão nào. Không nêu tên một vịnh có thật như địa điểm của kịch bản.

## Lịch sử revision
- `SCN_FLOATCITY_COASTAL_01` (2026-11-08): bản đầu, khóa cho buổi duyệt concept.
