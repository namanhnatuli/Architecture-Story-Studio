# Báo cáo nghiên cứu: How Gothic Cathedrals Reached Impossible Heights

Ngày 2026-11-05. Sổ claim: `research/sources.json` (sinh bằng `research/build_sources.py`). 30 trang/tài liệu nguồn, 56 claim `SOURCE_VERIFIED`, mỗi trích dẫn đều được script khớp nguyên văn với bản tải về (`research/source_snapshots.json`, có SHA256). Chưa claim nào được duyệt biên tập. Khớp nguyên văn chỉ cho biết nguồn có viết câu đó, **không chứng minh phép khái quát của phim là đúng**: lần duyệt đầu của chủ kênh (2026-11-05) đã tìm ra nhiều chỗ như vậy (revision g-r2, mục cuối).

## Nguồn chính

| Nhóm | Nguồn | Mức tin cậy và cách dùng |
|---|---|---|
| Kết cấu đá | Luận văn MIT của Philippe Block, 2005 (tóm tắt lý thuyết của Jacques Heyman); Block, DeJong và Ochsendorf, Nexus Network Journal 2006; trang dự án Romano và Ochsendorf (MIT) | Cao. Dùng cho ổn định, đường lực đẩy và các giả định của nó, Hooke 1675, so sánh vòm tròn và vòm nhọn, luật hình học của thợ cả |
| Durham | Roger Stalley, trang dạy học của Columbia; trang của nhà thờ Durham | Cao. Dùng cho niên đại xây dựng, các giai đoạn vòm, vòm nhọn và cao độ đỉnh |
| Beauvais | Vernhes, Renault, Zotna, hai bài ECSMGE 2024, truy cập mở (tác giả gồm cơ quan bảo tồn di tích vùng) | Cao. Dùng cho niên đại, quyết định nâng vòm, ba cách giải thích năm 1284, tháp năm 1573 |
| Amiens và Gothic nói chung | Columbia University, "Life of a Cathedral" (Stephen Murray) | Cao, nhưng là trang dạy học: có lỗi đánh máy và một lỗi niên đại (xem dưới) |
| Vòm nhọn, vòm gân, trụ chống bay | BnF Essentiels / Passerelles (Thư viện Quốc gia Pháp) | Cao, nhưng là tài liệu phổ thông: một câu về Chartres được nói hẹp lại |
| Saint-Denis | Arnaud Timbert, France Mémoire; Columbia (bản đồ Paris) | Cao |
| Chi tiết Beauvais, giải thích lực đẩy | Association Beauvais Cathédrale | Trung bình: hội bảo tồn, không qua bình duyệt. Mọi claim chỉ dựa vào đây đều ghi `confidence: medium` |

Nguồn **không mở được và không dùng**: Britannica, UNESCO, Smarthistory, The Met, kiểm kê vùng Hauts-de-France, visit-amiens (danh sách ở `research/source_snapshots.json` → `not_used`). Vì vậy phim không có claim nào dựa trên các nguồn này.

## Những chỗ nguồn không thống nhất, và phim xử lý ra sao

1. **Độ cao vòm Beauvais:** 46 m (Columbia), 46,7 m và "gần 47 m" (hội Beauvais), "trên 48 m" (cùng hội, trang khác). Lời dẫn nói "more than 45 meters", đúng với mọi nguồn. Hình liệt kê đủ các con số ("Published heights differ: 46 m to above 48 m").
2. **Độ cao vòm Amiens:** Columbia ghi 43,3 m. Tôi đã thấy con số 42,3 m trong kết quả tìm kiếm (Britannica) nhưng không mở được trang đó. Lời dẫn chỉ nói "more than 42 meters", đúng với cả hai.
3. **Nguyên nhân sập năm 1284:** còn tranh luận. Có ba giả thuyết cũ, hội Beauvais nghiêng về bão, bài 2024 bác nguyên nhân nền móng và cho rằng việc nâng vòm vượt tỉ lệ đã kiểm chứng làm phần trên quá mềm. Phim nêu cả ba, và gán luận điểm 2024 cho tác giả của nó, không nói như kết luận chung.
4. **"Cuộc cách mạng" hay không:** Columbia theo Viollet-le-Duc gọi là cách mạng, Timbert viết rằng không có đứt gãy Gothic. Phim nêu hai cách đọc mà không đọc tên; tên chỉ ghi nhỏ trên hình.
5. **"Lần đầu tiên" ở Chartres:** BnF nói Chartres là lần đầu trụ chống bay vào bản vẽ gốc, nhưng trụ ở Notre-Dame khoảng năm 1180 có trước. Phim chỉ nói "part of the original plans", bỏ chữ "đầu tiên".
6. **Vòm gân ở Durham:** hội Beauvais viết "the very first ... as early as 1093", nhưng 1093 là năm khởi công, không phải niên đại của vòm. Stalley mô tả hệ vòm phát triển qua ít nhất ba giai đoạn trong khoảng bốn mươi năm, và cho rằng việc ai đi trước ở bắc Âu là điều còn tranh cãi. Phim nói "begun in 1093", hoàn thành năm 1133, không nói ai đầu tiên.
7. **Lỗi trên trang Columbia:** Hooke bị gọi là nhà vật lý thế kỷ 18 (ông viết năm 1675, theo MIT), và một câu về đường dây xích bị sai ngữ pháp. Từ g-r2 phim không dùng câu này nữa (`CLM_133`), năm lấy từ MIT.
8. **Gian giữa Beauvais:** bài 2024 nói chưa từng xây, hội Beauvais nói dừng ở một gian. Phim nói "the great Gothic nave was never built".
9. **Vòm nhọn đẩy ít hơn bao nhiêu:** bài Block 2006 viết "about 15% less", nhưng các số làm tròn trong chính bài (16% và 25% so với 14% và 23% trọng lượng bản thân) cho khoảng 12,5% và 8%. Phim không đọc và không ghi con số phần trăm: hai vòm trên hình không phải hai vòm của nghiên cứu, và các khoảng số cần giải thích riêng về lực đẩy tối thiểu và tối đa (nhận xét lần hai của chủ kênh).
10. **Hai vòm nhọn chéo nhau:** hội Beauvais và BnF gọi các gân chéo là "hai vòm nhọn". Stalley mô tả gân chéo ở Durham là một đoạn cung tròn, còn vòm nhọn nằm ở vị trí ngang. Phim chỉ nói "two ribs".
11. **Vì sao có gân:** Stalley cho rằng ở Durham lý do có thể là thẩm mỹ và ý nghĩa nhiều hơn kết cấu. Theo quyết định biên tập của chủ kênh, lời dẫn không nêu ý này vì nó kéo người xem khỏi câu hỏi vòm làm việc thế nào; ý này giữ trong sổ claim (`CLM_144`).
12. **Cluny và năm 1088:** trang của di tích (Centre des monuments nationaux) gắn 1088 với dự án xây nhà thờ mới, còn hội Beauvais viết "around 1088" về công trường. Chưa có nguồn nào cho niên đại của chính các vòm nhọn, nên phim nói "whose construction began around 1088" và timeline ghi "Cluny III: construction begins". Việc Cluny III có vòm nhọn hiện dựa vào hội Beauvais; BnF chỉ nói Romanesque thỉnh thoảng dùng vòm nhọn.

## Giới hạn

- Các claim về lực là định tính, phim không có con số về lực, ứng suất hay hệ số an toàn.
- Vài chi tiết chỉ có một nguồn thứ cấp: ví von "như cánh cung", vòm nhọn ở Cluny, ba gian thành sáu, tháp 150 m. Chủ kênh nên xem kỹ các claim `confidence: medium` khi duyệt.
- Câu "chuỗi vẫn còn chạy qua tòa nhà" dựa vào thì hiện tại trên trang Columbia (bản quyền 2017), chưa kiểm tra tại chỗ.
- `CLM_105` (Gothic xuất hiện ở Pháp những năm 1140), `CLM_133` (câu của Columbia về đường dây xích) và `CLM_144` (ý của Stalley về gân vòm) có trong sổ nhưng lời dẫn không dùng.
- Câu "A taller arch can push less" dựa trên nhiều nguồn định tính và một ví dụ vòm trên gối dịch chuyển, nên phim nói "can". Tôi chưa đọc toàn văn nghiên cứu của Romano và Ochsendorf, chỉ đọc trang tóm tắt; bản đầy đủ sẽ cho biết điều kiện cụ thể hơn.

## Thay đổi sau lần duyệt đầu của chủ kênh (g-r2)

Sổ claim được viết lại ở những chỗ phép khái quát vượt quá nguồn. Mỗi thay đổi ghi trong `assumptions` của claim và `revision.edits` của `script/narration.template.json`. Lời nhận xét của chủ kênh được ghi lại như một yêu cầu sửa, không phải một lần duyệt: chưa claim nào được duyệt.

## Thay đổi sau lần nhận xét thứ hai (g-r3)

**Hình B40 là tính toán lại, không phải chép hình.** Một đường vẽ không vừa không chứng minh được rằng không có đường nào vừa, nên B40 nay dựng theo ví dụ vòm trên gối dịch chuyển trong Block, DeJong và Ochsendorf 2006, Hình 5. Tôi tính lại bằng cùng phương pháp (`script/arch_statics.py`, chỉ trọng lượng bản thân, khớp xoay ở 54,4° như in trên hình) và đối chiếu với các số in trong bài:

| Đại lượng | Trong bài | Tính lại |
|---|---|---|
| Hình 4(a), vòm bán nguyệt t/R 18%: lực đẩy tối thiểu và tối đa, % trọng lượng | 16 và 25 | 16,2 và 24,4 |
| Hình 5, t/R 15,24%, 160°: lực đẩy tối thiểu, % trọng lượng | 19,80 | 19,66 (dùng 54,4°: 19,59) |
| Hình 5(b), nhịp tăng 5,09%: lực đẩy tăng, % | 24,59 | 28 |
| Hình 5(c), giới hạn sập: nhịp tăng, % | 11,49 | 10,6 |
| Hình 5(c), giới hạn sập: lực đẩy tăng, % | 85,10 | 86 |

Các số gần nhau nhưng không trùng, và bài không nêu cách chia khối của nó. Các số trong Hình 5 được đọc từ nhãn trên hình, không có trong phần chữ. Phim và card không nêu số nào trong bảng này. Test `GothicThrustLineTest` giữ các so sánh trên.

Sổ claim cũng được thu hẹp để người duyệt không phải chấp thuận phát biểu rộng hơn lời dẫn: `CLM_123` theo yêu cầu của chủ kênh, và `CLM_143`, `CLM_156`, `CLM_157`, `CLM_161`, `CLM_185`, `CLM_190`, `CLM_191` do tôi rà thêm.
