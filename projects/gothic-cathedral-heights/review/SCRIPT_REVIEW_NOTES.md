## Trạng thái

Đây là bản g-r3, sửa theo nhận xét thứ hai của bạn. **Chưa có gì được duyệt.** Chưa render video nào, chưa dựng mô hình. Cấu trúc phim, cách mở và lời kêu gọi giữ nguyên. Bản nghe thử: `output/gothic-cathedral-heights_narration_preview_g-r3.m4a`. Bản xem trước 30 card: `output/card_previews_g-r3/` (`contact_sheet.png`, và `B40_s0.png` đến `B40_s4.png` theo từng câu). Đây là ảnh vẽ thử bằng script riêng để kiểm tra bố cục, không phải bản render của engine: phông chữ và độ mịn sẽ khác.

## Câu chuyện trong năm dòng

1. Mở bằng năm 1284: phần vòm cao nhất thời Trung Cổ ở Beauvais sập, sau đó đặt câu hỏi của phim.
2. Vấn đề: đá gần như không chịu được kéo, còn vòm thì đẩy ra ngoài. Một kiểu nhà thờ Romanesque vòm nôi đáp lại bằng tường và trụ dày.
3. Ba công cụ Gothic bố trí lại hệ đỡ: vòm nhọn, vòm gân, trụ chống bay. Tường không còn là chỗ đỡ chính của vòm, nên có thể mở ra đón ánh sáng.
4. Thợ xây làm bằng hình học, kỹ năng nghề và kinh nghiệm, không có phép tính kết cấu hiện đại. Beauvais đi quá giới hạn, còn Amiens phải cứu bằng xích sắt.
5. Kết luận: đá hiếm khi hỏng vì yếu, mà thường vì mất ổn định, nên hình dạng và tỉ lệ giải thích được nhiều điều. Mô hình giúp hiểu vai trò của tỉ lệ, nhưng tự nó không chứng minh một công trình thật an toàn. Độ cao không hề "bất khả thi", và đây cũng không phải câu chuyện tiến bộ đơn giản.

## Đã sửa theo nhận xét lần hai

| Điểm | Beat | Đã sửa thế nào |
|---|---|---|
| 1. Hình đường lực đẩy | B40 | Không còn hai vòm giống nhau với một đường vẽ lệch. Bên trái: một vòm với nhiều đường hợp lệ. Bên phải: chính vòm đó khi gối đỡ dịch ra, tới giới hạn đường lực chạm đá ở năm điểm. Lời dẫn nói rõ thay đổi này |
| 2. Số liệu dưới hai vòm | B08 | Bỏ phần trăm khỏi card, ghi đây là hình minh họa, không phải hai vòm của nghiên cứu. Lời dẫn: "of two other arches" |
| 3. Cluny | B10, B14 | "Whose construction began around 1088"; timeline "Cluny III: construction begins". Không nêu năm cho chính các vòm nhọn |
| Hồ sơ | CLM_123 | Đồng bộ với B07 |
| Biên tập | B14, B15 | Bỏ câu đọc tên Stalley, giữ ý của ông trong sổ claim (`CLM_144`). B15 không còn "Whatever first inspired them" |

Các sửa đổi của lần nhận xét đầu (vòm nhọn, đường lực đẩy, người thợ, vòm gân, độ cao, Durham, đối lập tối/sáng, B24, B35, B22) vẫn giữ nguyên. Nhật ký đầy đủ nằm ở `script/narration.template.json` → `revision.edits`.

## Tôi tự thêm, xin bạn xem lại

1. **Hình B40 dùng kết quả tính lại.** Đây là chỗ đầu tiên trong phim có hình dựa trên phép tính. Tôi tính lại ví dụ ở Hình 5 của bài Block 2006 bằng cùng phương pháp, không chép hình. Số tính lại gần với số in trong bài nhưng không trùng (bảng ở `research/RESEARCH_REPORT.md`, ví dụ giới hạn sập: nhịp +10,6% so với +11,49%; lực đẩy +86% so với +85,10%). Phim không nêu số nào trong đó. Hình ghi "After Block, DeJong and Ochsendorf, 2006, Fig. 5, recalculated". Bạn có thể yêu cầu người có chuyên môn kết cấu kiểm tra `script/arch_statics.py`.
2. **Thu hẹp thêm 7 claim.** Cùng lý do với `CLM_123`, tôi bỏ các phần lời dẫn không nói ở `CLM_143`, `CLM_156`, `CLM_157`, `CLM_161`, `CLM_185`, `CLM_190`, `CLM_191`, ví dụ "first fully gothic structure" ở `CLM_161`.
3. **Nhãn "Stone web" ở B12** nay nằm ngay trên phần đá giữa các gân, thay vì ở ngoài hình.

## Cần bạn quyết định

1. **Độ tin cậy của một số chi tiết.** Các claim `medium` nằm ở bảng cuối tài liệu. Nhiều mục còn dựa vào Association Beauvais Cathédrale, một hội bảo tồn, không qua bình duyệt: ví von "như cánh cung" (B05), vòm nhọn ở Cluny (B10), đường đi của lực qua trụ chống bay (B17), ba gian thành sáu (B36), tháp khoảng 150 m (B37). Tôi không mở được Britannica, UNESCO, Smarthistory và The Met. Nếu bạn có sách của Stephen Murray hoặc Jacques Heyman, các mục này có thể chắc hơn. Toàn văn Romano và Ochsendorf cũng sẽ giúp cho B08.
2. **Đơn vị.** Phim dùng mét, phim cầu trước dùng feet. Lời dẫn và phụ đề dùng chính tả Mỹ (`meters`), khớp với giọng Mỹ.
3. **Phát âm (chỉ bạn xác nhận được).** Kokoro đọc sai nhiều tên Pháp nên có 6 mục ghi đè chỉ áp dụng cho giọng đọc, tất cả đang `PENDING_LISTENING_REVIEW`: Beauvais (boh-VAY), Amiens (am-YAN), Suger (soo-ZHAIR), Cluny (KLOO-nee), Notre-Dame (NOH-truh DAHM), Viollet-le-Duc (vyoh-LAY luh DOOK). Kiểm tra ASR đạt không chứng minh phát âm đúng, và tôi không nghe được audio.
4. **Giọng.** `am_michael` mới được bạn duyệt riêng cho phim cầu. Muốn xuất bản phim này, bạn cần duyệt lại cho dự án này; hiện tại trạng thái là `LICENSE_REVIEW_REQUIRED`.

## Phần hình (sau khi kịch bản được duyệt)

- **Tiêu chí, theo nhận xét của bạn:** chọn hình giúp người xem hiểu, không đổi sang 3D chỉ để giảm tỉ lệ 2D. Tỉ lệ 2D cao tự nó không phải vấn đề; điều cần tránh là chuỗi card chỉ có chữ kéo dài, và hình không được nói nhiều hơn điều nó thực sự chứng minh. Phần đầu tài liệu có đo chuỗi dài nhất.
- **Giữ ở dạng sơ đồ 2D có diễn tiến:** so sánh vòm (B08), dây xích (B09), giàn chống khi xây (B27), mặt bằng thêm trụ (B36), đường lực đẩy (B40). Đây là nơi sơ đồ 2D giải thích tốt nhất.
- **Cần cải thiện:** chuỗi card chữ B22–B24, về ánh sáng và Saint-Denis. Nên dùng ảnh có quyền rõ ràng ở đây.
- **Thư viện chưa có gì về nhà thờ Gothic.** 16 beat 3D đang báo `NEW_ASSET_REQUIRED`, planner không thay bằng thứ khác. Cần họ mô hình mới: mặt cắt một gian Gothic và một gian Romanesque. Planner ước tính 1–3 ngày cho mỗi kiểu. Phần đá giữa các gân phải trông như đá đang làm việc (B13), và kiểu Romanesque không được dựng tối tăm (B06).
- **Ảnh thật.** Chưa tải ảnh nào. Saint-Denis, Chartres, Notre-Dame, Amiens và Beauvais nên có ảnh thật, mỗi ảnh cần hồ sơ quyền đầy đủ.
- **Các card 2D mới được xem bằng ảnh vẽ thử.** Tôi đã xem cả 30 card ở mức tổng quan và B40, B08 ở kích thước lớn. Khi render bằng engine vẫn phải kiểm tra lại.
