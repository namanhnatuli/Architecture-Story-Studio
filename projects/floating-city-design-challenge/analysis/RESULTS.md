# Kết quả mô hình tính khái niệm (CALCULATED_ESTIMATE)

Sinh bởi `analysis/design_model.py` từ `concept/scenario_contract.json`. Hộp bê tông chữ nhật lý tưởng, nước lặng, góc nghiêng nhỏ. **Không** đánh giá an toàn kết cấu, ổn định động hay ổn định khi hư hỏng theo quy chuẩn, neo, bão, dao động đàn hồi thủy lực hay tiện nghi.

## 1. Một tấn đòi bao nhiêu nước
- Nước biển 1.025 kg/m³: 0.9756 m³ mỗi tấn; nước kênh 1.000 kg/m³: 1.0 m³.
- Nhà nặng nhất ở Schoonschip (340–350 t, CLM_013) chiếm chỗ 340.0–350.0 m³ nước kênh, tức một khối lập phương cạnh khoảng 6.98–7.05 m.

- 'Thuyền đất sét' (CLM_002): 1108.0 m³ bê tông của thân phao, nếu đúc đặc là khối lập phương cạnh 10.35 m, đặc hơn nước biển 2.34 lần, chìm; làm thành hộp 40 × 40 × 4 m thì nổi với mớn nước 1.621 m (chưa có nhà).

## 2. Phao A (40 × 40 m, sâu 4 m, nhà 3 tầng phủ 40%)
| Tải tĩnh nhà (t/m² sàn) | Khối lượng (t) | t/m² mặt sàn phao | Mớn nước (m) | Mạn khô (m) | KG (m) | BM (m) | GM (m) |
|---|---|---|---|---|---|---|---|
| 0.4 (thấp) | 4467.2 | 2.792 | 2.724 | 1.276 | 4.101 | 48.95 | 46.21 |
| 0.6 (giữa) | 4851.2 | 3.032 | 2.958 | 1.042 | 4.449 | 45.07 | 42.1 |
| 0.9 (cao) | 5427.2 | 3.392 | 3.309 | 0.691 | 4.879 | 40.29 | 37.07 |

- Bê tông thân phao chiếm 55% khối lượng (phương án giữa): 2659.2 t trong 4851.2 t.
- Thêm 100 t: mớn nước tăng 6.1 cm. Thêm một tầng: +544.0 t, mớn nước +33.2 cm, KG +1.01 m.
- Dời 100 t ra cách tâm 15 m: nghiêng khoảng 0.421° (công thức góc nhỏ, CLM_009).
- Một ô 10.0 × 10.0 m ngập: phao chìm thêm 0.197 m (mạn khô còn 0.845 m; chỉ tính chìm đều, không xét nghiêng).

## 3. Rộng hay hẹp (cùng mớn nước)
| Bề rộng | BM = B²/(12T) |
|---|---|
| 10m | 2.82 m |
| 20m | 11.27 m |
| 40m | 45.08 m |
| 80m | 180.3 m |

Phao càng rộng so với mớn nước thì BM càng lớn: ổn định ban đầu không phải bài toán khó của phao rộng. Cái giá là phao 'cứng' (CLM_007), bám theo mặt nước; vấn đề chuyển sang sóng, mối nối và tiện nghi.

## 4. Quy mô 10.000 người (theo giả định diện tích sàn mỗi người)
| m² sàn/người | Diện tích mặt phao | m² mặt phao/người | Số phao 40 × 40 | Người/phao | Lượng chiếm nước (t) |
|---|---|---|---|---|---|
| 30 | 25.0 ha | 25.0 | 157 | 64 | 762,000 (701,000–852,000) |
| 40 | 33.3 ha | 33.3 | 209 | 48 | 1,014,000 (934,000–1,134,000) |
| 50 | 41.7 ha | 41.7 | 261 | 38 | 1,266,000 (1,166,000–1,416,000) |

- Mốc so sánh: OCEANIX Busan (đề xuất) 5.2 m² mặt phao mỗi người (12.000 là cư dân và khách); module của Ruzzo 2026: 30.0 m² mỗi người. Ngưỡng 'quy mô lớn' 20 ha (CLM_040).

## 5. Phao lớn hay nhiều phao (33,3 ha, 40 m² sàn mỗi người)
| Cạnh phao | Số phao | Số cạnh chung tối đa (mối nối) | Khối lượng một phao (t) | Người/phao |
|---|---|---|---|---|
| 40m | 209 | 391 | 4,851 | 48 |
| 60m | 93 | 180 | 10,764 | 108 |
| 80m | 53 | 97 | 19,002 | 192 |
| 100m | 34 | 60 | 29,564 | 300 |

Chỉ là phép đếm, không có tải trọng. Phao to: ít mối nối nhưng nặng khi đúc, hạ thủy và kéo, và phần phản ứng uốn theo sóng lớn hơn (CLM_042, CLM_053).

## 6. Cầu nối bờ
Dải mực nước 2.0 m (giả định) cộng dao động mớn nước khi phao rỗng và đầy (0.439 m):
- Cầu 15 m: dốc tối đa khoảng 4.6° mỗi chiều.
- Cầu 25 m: dốc tối đa khoảng 2.8° mỗi chiều.
- Cầu 40 m: dốc tối đa khoảng 1.7° mỗi chiều.

## 7. Các lần sửa thiết kế mà câu chuyện dùng
- A′: thân sâu 4,5 m với nhà nặng (0,9 t/m²): thêm 105.6 t bê tông, mớn nước 3.374 m, mạn khô 1.126 m (thân 4 m: 0.691 m).
- B: hai phao giống nhau, nhà 2 tầng và 4 tầng: mớn nước 2.626 m và 3.29 m; mặt sàn lệch nhau 0.664 m.
