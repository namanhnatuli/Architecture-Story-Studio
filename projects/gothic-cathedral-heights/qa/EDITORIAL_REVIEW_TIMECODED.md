# Xem lại biên tập có mốc thời gian: phim Gothic, revision g-r3, bản 720p

- **Người xem:** agent, trên bản review 720p (`output/gothic_cathedral_heights_G_R3_INTERNAL_REVIEW_720p.mp4`, 923,4 s, tức 15:23).
- **Cách xem:** 308 ảnh tách mỗi 3 giây, rồi frame gốc 1280×720 ở những chỗ có nghi vấn. Các mốc dưới đây lấy từ bảng shot và frame gốc, vì ảnh tách bằng `fps=1/3` lệch khoảng 1,5 giây.
- **Giới hạn:** agent không nghe được audio. Mọi nhận xét về nhịp đọc và phát âm chỉ suy ra từ timing và kết quả ASR. Chưa có ảnh thật nào trong phim.

## Cập nhật g-r9 (2026-11-07): bản `G_R9_INTERNAL_REVIEW_720p`

- **Đã xem:** khung hình trích từ chính MP4 ghép tại các đoạn đổi ở g-r8 và g-r9 (B09, B21, B22, B25, B29 và các điểm cắt quanh chúng), và chứng cứ review của chủ kênh về C2–C7 (`qa/codex_gr8_review_20261107/`). **Chưa xem liên tục toàn phim ở tốc độ thật**, không nghe audio.
- **Lỗi tìm thấy và đã sửa ở vòng này:**
  - 00:08–00:23 của C6 (≈7:10 trong phim): ảnh phần trên dàn hợp xướng (dựng lại từ 1231) đi cùng lời về Suger 1140–1144. Đã đổi sang ảnh ambulatory còn lại từ thời Suger, thêm chú thích về phần dựng lại sau. Nguồn Atlas du patrimoine de la Seine-Saint-Denis, claim CLM_165.
  - C6 ≈00:19: chấm "Every vault ribbed" nằm trên mảng đá; nay "Vault rib" chấm đúng gân và gân sáng dọc chiều dài.
  - C7/B29 (9:19): toàn mô hình với zoom nhẹ; nay cận một trụ chống bay và trụ chống của nó, phần còn lại mờ đi.
  - C3/B09 (2:42) và C7/B25 (8:06): chờ hình quá lâu; nay dây treo và thao tác compa bắt đầu từ những giây đầu.
  - Lệnh `final-assemble` từng đặt tên FINAL cho bản nội bộ; đã sửa và có test.
- **Chương 8:** 8 shot ảnh hoặc bản vẽ liền nhau. Chủ kênh chấp nhận ngoại lệ này ngày 2026-11-07 (`project.json` → `variety_exception`); ngưỡng chung 4 giữ nguyên.
- **Giới hạn đã biết:** ảnh Durham (1273 px) và ambulatory (2160 px) sẽ mềm khi phủ kín khung 4K.

## Lỗi tìm thấy và đã sửa

| Mốc | Vấn đề | Vì sao quan trọng | Cách sửa | Ảnh hưởng | Render lại |
|---|---|---|---|---|---|
| 04:16 (SC_012→SC_013) | Camera nhảy giữa một match cut. Media QA báo SSIM 0,877, dưới ngưỡng 0,98 | Người xem thấy hình giật trong khi vẫn là một góc nhìn. Lỗi nằm ở planner: `close_on_targets` không truyền khung hình để so kiểu cắt | Sửa planner. Thêm `close_on`, B12 và B13 dùng chung một khung. SSIM nay 1,0 | Mọi phim sau dùng `close_on` hoặc `close_on_targets` | SC_012, SC_013 |
| 04:21–04:38 (B13) | Gân vòm và web đá cùng sáng, hòa thành một mảng nhạt. Nhãn "Main ribs" chỉ vào chỗ không còn thấy gân | Đây là đoạn phân biệt gân và đá, đúng ý chủ kênh đã yêu cầu sửa ở B13 | Thêm `glow_only`. Câu 1 chỉ gọi tên gân; câu 2 ("carries load") chỉ web sáng lên, gân nổi rõ thành dải tối | Chỉ B13 | SC_013 |
| 03:56–04:38 | Khung rộng từ dưới lên để lộ chân trụ và vòm cánh lởm chởm, trông như đá vỡ | Người xem có thể tưởng công trình bị hỏng | Cắt sát gian gần nhất. B12 chỉ cho sáng gân của gian đó | B12, B13 | SC_012, SC_013 |
| 02:42–02:55 (B09) | 13 giây gần như chỉ có một đường kẻ ngang | Khoảng trống đúng lúc lời đọc giới thiệu Hooke | "Robert Hooke, 1675" hiện từ câu đầu, rồi câu trích, rồi mới tới dây xích | B09 | SC_009 |
| 03:12–03:22 (B10) | 10 giây chỉ có trục năm | Hình không nói gì trong lúc lời nói "not a Gothic invention" | Thêm hình vòm nhọn và dòng "Not a Gothic invention" từ câu đầu | B10 | SC_010 |
| 07:02–07:08 (B21) | Chỉ có trục năm trong câu "Part of the answer is light" | Như trên | Thêm dòng "Part of the answer: light" | B21 | SC_022 |
| 08:06–08:14 (B25) | 5,6 giây trống, rồi một dòng chữ | Như trên | Ba vòm lớn dần theo ba câu | B25 | SC_026 |
| 13:38–13:42 (B41) | 4,4 giây trống ở đầu shot | Như trên | Hai vòm hiện từ câu đầu, nhãn theo sau | B41 | SC_042 |
| 06:18–06:50 (B19) | 31 giây nói về cờ bay mà không có gì được chỉ ra | Shot 3D dài nhất phim, người xem không biết nhìn vào đâu | Cho cờ bay sáng suốt shot, vẫn đẩy camera chậm | B19 | SC_020 |
| 05:57–06:18 (B18) | Ghi chú "same scale" khiến mô hình Romanesque cao khoảng nửa Gothic trông như một phép đo | Tỉ lệ mô hình là tự chọn cho dễ nhìn; lời dẫn và sổ claim không nói về chiều cao này. Đây là lỗi vượt quá bằng chứng | Đổi thành "Illustrative models, not measured buildings" | B18 | SC_018, SC_019 |

Các sửa trên đều không đổi lời dẫn, timing, ngưỡng hay cổng kiểm tra.

## Kiểm tra "lời và hình có khẳng định vượt quá bằng chứng không?"

Làm lại trên bản đã render, theo mục bắt buộc trong playbook:

- **B40:** hai vòm ghi rõ "One idealized arch, self-weight only" và các giả định. Hình bên trái có nhiều đường hợp lệ, hình bên phải là chính vòm đó ở giới hạn. Phim không đọc số nào trong các số tính lại.
- **B08:** không có phần trăm trên hình, ghi rõ đây không phải hai vòm của nghiên cứu.
- **B10, B14:** ghi "Cluny III: construction begins", không gán năm 1088 cho các vòm nhọn.
- **B12, B13:** ghi "one type: a four-part vault" và "one analysis, still debated".
- **B33:** thanh ghi "more than 42 m", "more than 45 m", kèm đủ các số đã công bố cho Beauvais và "Bars are schematic".
- **B36:** ba gian thành sáu, khớp câu của Stephen Murray.
- **B05, B16, B17:** mũi tên và đường lực ghi rõ là minh họa, cùng một độ dài, không biểu thị độ lớn.
- **B18:** có lỗi, đã sửa như bảng trên.

## Còn để ngỏ, chưa sửa

1. **Cùng một mô hình, cùng một góc.** 14 shot dùng góc `CATHEDRAL_SECTION` nhìn toàn cảnh mô hình Gothic: SC_001, 002, 007, 015, 016, 017, 019, 020, 024, 030, 035, 040, 043, 045. Về cuối phim hình dễ lặp (B29, B34, B39, B42, B44). Ảnh thật của Saint-Denis, Chartres, Notre-Dame, Amiens và Beauvais sẽ giúp nhiều nhất. Cách rẻ hơn là thêm cận cảnh như SC_021, shot đẹp nhất trong số các shot 3D.
2. **B35 (10:47–11:19):** 31 giây chỉ có chữ. Chữ hiện dần theo câu và mỗi dòng ghi "Hypothesis", nhưng đây là card chữ dài nhất. Có thể thay bằng mô hình sáng từng bộ phận theo từng giả thuyết, nhưng mô hình chưa có phần móng.
3. **Vệt bóng mềm trên trụ bên phải (03:56–04:38) và góc dưới trái SC_021.** Đã giảm nhờ cắt sát, nhưng vẫn còn, trông hơi như vết bẩn. Sửa đúng cách là đổi ánh sáng trong `config/visual_style.json`, và việc đó làm cả 47 shot stale, nên nên làm cùng lúc với lần render lại lớn.
4. **Ghi chú chồng nhau ở B05 và B16:** ba nhãn nhỏ góc trên trái, hai nhãn trong đó gần cùng ý. Ít ảnh hưởng.
5. **C3 toàn sơ đồ 2D (2:10–3:56).** `chapter_variety` cảnh báo. Giữ nguyên vì đây đúng là nơi sơ đồ giải thích tốt nhất, theo tiêu chí của chủ kênh.
6. **Card tiêu đề B03 (0:36–0:52):** 16 giây. Giữ nguyên vì chủ kênh yêu cầu giữ cách mở.
7. **8 beat `PARTIALLY_COVERED` (B06, B07, B12, B13, B18, B23, B29, B34):** planner xếp loại này vì một cú giữ hình chỉ minh họa được một phần ý đồ của beat; các bộ phận cần thấy đều đọc được và không có lỗi nào được ghi. Đây là nhận xét về loại hình, không phải lỗi render.
8. **Ba hàng UNCERTAIN của kiểm tra lời–hình:** agent đã đọc, cả ba đều là báo nhầm do từ khóa. B26.s1 "right angles", B35.s4 "left the upper parts", B44.s0 nói chung về các mũi tên ở những beat trước. Người duyệt vẫn nên xem lại.

## Mười câu hỏi trải nghiệm người xem (đánh giá của agent)

1. **Câu hỏi trung tâm có rõ ngay không?** Có. Beauvais sập năm 1284 ở câu đầu, câu hỏi hiện trên màn hình ở khoảng 0:45–0:52.
2. **Có đoạn tĩnh dài không?** Dài nhất 13,7 giây ở 2:15 (B08), dưới ngưỡng 14 giây. Ngưỡng này không bắt được card trống nên agent phải tự tìm, xem bảng trên.
3. **Hình có khớp câu đang đọc không?** Sau khi sửa thì có. Nhãn, mũi tên và phần phát sáng bám theo câu hoặc từ.
4. **Người xem có hiểu vòm gân không?** B12 và B13 giờ phân biệt rõ gân và web. Góc từ dưới lên vẫn lạ với người không quen hình chiếu trục đo.
5. **Người xem có hiểu trụ chống bay không?** B17 có đường lực từ cờ bay xuống trụ. Đây là đoạn rõ nhất phim. Nhãn "Flying buttress" che một phần công trình phía trên.
6. **B40 có đọc được không?** Có. Đọc ở 720p vẫn rõ, nhưng đây là đoạn khó nhất phim và cần chủ kênh xem lại.
7. **Có kể chuyện tiến bộ một chiều không?** Không. B24 giữ cả hai cách nhìn, B37 kể tháp Beauvais sập năm 1573, B43 nói rõ "Not a simple story of progress".
8. **Người xem có hiểu mô hình chỉ là minh họa không?** Có. Ghi chú nói rõ ở các chỗ nhắc công trình thật, và B44 đọc thành lời.
9. **Phụ đề:** 214 cue, dòng dài nhất 42 ký tự. Agent chưa đọc hết phụ đề trên hình; chi tiết ở `qa/SUBTITLE_QA.md`.
10. **Âm lượng:** −16,4 LUFS, true peak −1,2 dBTP, đo bằng máy. Agent không nghe được.
