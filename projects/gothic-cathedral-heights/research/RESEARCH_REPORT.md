# Báo cáo nghiên cứu: How Gothic Cathedrals Reached Impossible Heights

Ngày 2026-11-05. Sổ claim: `research/sources.json` (sinh bằng `research/build_sources.py`). 22 trang/tài liệu nguồn, 48 claim `SOURCE_VERIFIED`, mỗi trích dẫn đều được script khớp nguyên văn với bản tải về (`research/source_snapshots.json`, có SHA256). Chưa claim nào được duyệt biên tập.

## Nguồn chính

| Nhóm | Nguồn | Mức tin cậy và cách dùng |
|---|---|---|
| Kết cấu đá | Luận văn MIT của Philippe Block, 2005 (tóm tắt lý thuyết của Jacques Heyman) | Cao. Dùng cho ổn định, đường lực đẩy, Hooke 1675, luật hình học của thợ cả |
| Beauvais | Vernhes, Renault, Zotna, hai bài ECSMGE 2024, truy cập mở (tác giả gồm cơ quan bảo tồn di tích vùng) | Cao. Dùng cho niên đại, quyết định nâng vòm, ba cách giải thích năm 1284, tháp năm 1573 |
| Amiens và Gothic nói chung | Columbia University, "Life of a Cathedral" (Stephen Murray) | Cao, nhưng là trang dạy học: có lỗi đánh máy và một lỗi niên đại (xem dưới) |
| Vòm nhọn, vòm gân, trụ chống bay | BnF Essentiels / Passerelles (Thư viện Quốc gia Pháp) | Cao, nhưng là tài liệu phổ thông: một câu về Chartres được nói hẹp lại |
| Saint-Denis | Arnaud Timbert, France Mémoire; Columbia (bản đồ Paris) | Cao |
| Chi tiết Beauvais, giải thích lực đẩy | Association Beauvais Cathédrale | Trung bình: hội bảo tồn, không qua bình duyệt. Mọi claim chỉ dựa vào đây đều ghi `confidence: medium` |

Nguồn **không mở được và không dùng**: Britannica, UNESCO, Smarthistory, The Met, kiểm kê vùng Hauts-de-France, visit-amiens (danh sách ở `research/source_snapshots.json` → `not_used`). Vì vậy phim không có claim nào dựa trên các nguồn này.

## Những chỗ nguồn không thống nhất, và phim xử lý ra sao

1. **Độ cao vòm Beauvais:** 46 m (Columbia), 46,7 m và "gần 47 m" (hội Beauvais), "trên 48 m" (cùng hội, trang khác). Lời dẫn nói "nearly 47 meters". Hình ghi rõ "Published heights differ: about 46 to 48 m".
2. **Độ cao vòm Amiens:** Columbia ghi 43,3 m. Tôi đã thấy con số 42,3 m trong kết quả tìm kiếm (Britannica) nhưng không mở được trang đó. Lời dẫn chỉ nói "more than 42 meters", đúng với cả hai.
3. **Nguyên nhân sập năm 1284:** còn tranh luận. Có ba giả thuyết cũ, hội Beauvais nghiêng về bão, bài 2024 bác nguyên nhân nền móng và cho rằng việc nâng vòm vượt tỉ lệ đã kiểm chứng làm phần trên quá mềm. Phim nêu cả ba, và gán luận điểm 2024 cho tác giả của nó, không nói như kết luận chung.
4. **"Cuộc cách mạng" hay không:** Columbia theo Viollet-le-Duc gọi là cách mạng, Timbert viết rằng không có đứt gãy Gothic. Phim nói rõ hai cách đọc.
5. **"Lần đầu tiên" ở Chartres:** BnF nói Chartres là lần đầu trụ chống bay vào bản vẽ gốc, nhưng trụ ở Notre-Dame khoảng năm 1180 có trước. Phim chỉ nói "part of the original plans", bỏ chữ "đầu tiên".
6. **Vòm gân "đầu tiên" ở Durham:** hội Beauvais viết "the very first", còn Columbia nêu nguồn gốc Hồi giáo, La Mã và Byzantine. Phim chỉ nói "as early as 1093".
7. **Lỗi trên trang Columbia:** Hooke bị gọi là nhà vật lý thế kỷ 18 (ông viết năm 1675, theo MIT), và một câu về đường dây xích bị sai ngữ pháp. Claim ghi rõ cách đọc, năm lấy từ MIT.
8. **Gian giữa Beauvais:** bài 2024 nói chưa từng xây, hội Beauvais nói dừng ở một gian. Phim nói "the great Gothic nave was never built".

## Giới hạn

- Các claim về lực là định tính, phim không có con số về lực, ứng suất hay hệ số an toàn.
- Vài chi tiết chỉ có một nguồn thứ cấp: ví von "như cánh cung", vòm nhọn giữ cùng cao độ đỉnh, Cluny khoảng 1088, Durham 1093, ba gian thành sáu, tháp 150 m. Chủ kênh nên xem kỹ các claim `confidence: medium` khi duyệt.
- Câu "chuỗi vẫn còn chạy qua tòa nhà" dựa vào thì hiện tại trên trang Columbia (bản quyền 2017), chưa kiểm tra tại chỗ.
- `CLM_105` (Gothic xuất hiện ở Pháp những năm 1140) có trong sổ nhưng lời dẫn không dùng.
