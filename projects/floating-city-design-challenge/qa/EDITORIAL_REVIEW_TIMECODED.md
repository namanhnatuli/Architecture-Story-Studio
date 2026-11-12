# Xem lại biên tập có mốc thời gian: bản internal review đầy đủ v2 (2026-11-12)

- **Người xem:** agent, trên bản FULL v2 720p, 784,2 s (13:04,2):
  - `output/pilot/floating_city_design_challenge_FULL_V2_INTERNAL_REVIEW_720p.mp4` (có SFX) và `..._no_sfx.mp4`;
  - `output/floating_city_design_challenge_INTERNAL_REVIEW_720p.mp4` (bản ghép chỉ lời dẫn). Cả ba cùng hình.
- **Lời dẫn và mốc thời gian không đổi so với v1** (`narration.json` không đổi byte nào), nên mọi mốc dưới đây dùng được cho cả hai bản.
- **Cách xem:**
  - 5 frame mỗi shot, trích thẳng từ MP4: đầu, 25 %, 50 %, 75 % và cuối shot (220 frame);
  - frame 1280×720 ở các chỗ đã sửa: B13 3:43–3:57 (2 s một frame), B33/B34, B30/B31, B22/B24, B38;
  - 6 frame đầu (0,1–4 s) của các card B03, B20, B32, B37;
  - đo thời điểm sơ đồ đầu tiên hiện trên card (độ sáng nhỏ nhất của vùng nội dung), so v1 với v2.
- Đây là nhận xét **của agent**, không phải duyệt biên tập. Agent không nghe chủ quan. Các số âm thanh dưới đây chỉ là kiểm tra kỹ thuật.

## Mốc chương
```
0:00 Could We Actually Do This?
1:04 The First Problem: Making Buildings Float
3:20 Why One Platform Isn't a City
5:33 The Water Never Stays Still
7:02 Keeping the City in Place
7:56 A City Needs More Than Buildings
9:07 What Would Actually Make This Difficult?
11:41 Could We Really Build It?
```

## Các chỗ đã sửa, nhìn trong MP4 v2
| Mốc | Shot (beat) | Thấy gì | Kết luận |
|---|---|---|---|
| 0:24–0:25 | SC_003 (B03) | Vạch chia giữa có ngay khung đầu. 46 ô nhà và ba lục giác vẽ mờ hiện từ 0,5 s (v1: 4,0 s chỉ có nhãn góc) | Đạt |
| 6:12 | SC_020 (B20) | Mặt nước và đất bờ trái có ngay khung đầu; bờ phải (vịnh) từ khoảng 1 s (v1: 6,5 s chỉ có nhãn góc) | Đạt |
| 9:42 | SC_032 (B32) | Ba vòng tròn mờ hiện từ 0,6 s (v1: 2,5 s) | Đạt |
| 11:13–11:16 | SC_037 (B37) | Nhãn góc "What would it cost?" một mình 2,8 s, đúng lúc lời dẫn hỏi câu đó; dòng "No reliable cost estimate…" hiện ở đầu câu 2 (v1: 4,2 s) | Đạt, xem mục 3 ở dưới |
| 3:43–3:57 | SC_013 (B13) | Từ khung hai phao, camera vào cận khe (khoảng 3:46). Thấy rõ hai mép sàn trong, hai nét đứt cao độ kéo qua khe, thước đứng có hai vạch. Nhãn "Decks ≈ 0.66 m apart" nằm trên khe, chỉ vào thước, không che khe. Nhãn tắt ở "whatever", thước tắt trước khung bản lề (3:55) | Đạt |
| 3:21–3:36, 5:34–5:46 | SC_012 (B12), SC_017 (B17) | Mặt nước phủ kín khung; không còn tam giác nền xám ở góc trên phải | Đạt |
| 7:03–7:14, 7:40–7:57 | SC_022 (B22), SC_024 (B24) | Khung ngang: mặt nước là đường ngang dưới phao; khối nước xanh xám tách khỏi nền nhờ dải đáy. Cọc, dây neo, khối neo rõ | Đạt; nước còn nhạt (mục 1) |
| 9:17–9:31 | SC_030 (B30) | Camera hạ xuống trên nước đục; nước trong lúc đã gần tới khung ngang. Nhãn "Sea surface" chỉ vào mặt biển. Không còn thấy lưới bóng đáy lúc chuyển | Đạt |
| 9:31–9:42 | SC_031 (B31) | Dây neo mờ đi; ba ống đứng màu cam nổi rõ từ phao xuống đáy, rồi chạy dọc đáy về phía bờ. "Sea surface" đánh dấu mặt nước | Đạt |
| 10:02–10:21 | SC_033 (B33) | Mở bằng phao hộp nhìn từ trên. Ở "semi", camera hạ xuống khung ngang: phao hộp nằm trên mặt nước; mô-đun nửa chìm có sàn trên mặt nước, cột xuyên mặt nước, phao chìm dưới nước nhuộm xanh. Mực nước là một đường liền | Đạt; khung chuyển xem mục 2 |
| 10:21–10:40 | SC_034 (B34) | Mở nhìn từ trên. Ở "seawater", camera hạ ngang mặt nước: thân phao có phần dưới nước nhuộm xanh, mặt nước là đường ngang ở giữa thân phao. Ghi chú "Illustrative: inspection zone, no damage shown" | Đạt; nước nhạt (mục 1) |
| 11:41–11:49 | SC_038 (B38) | Lối đi cam khi còn cận. Khi kéo ra, nhà gần như trắng; lối đi, cầu, tuyến, ống, đê hiện cùng một màu cam, đọc được như một mạng | Đạt |

## Watermark, nhìn trong MP4
- Góc dưới trái, có ở mọi frame đã xem, kể cả card nền sáng, mặt nước, cảnh phố dày. QA chương: PSNR trong ô 34,9–43,1 dB so với ảnh có watermark, 16,0–22,1 dB so với ảnh gốc; có mặt ở cả 8 chương.
- Nằm trong vùng phụ đề, nên không đè chữ nào của phim. Phụ đề YouTube canh giữa; dòng dài nhất 42 ký tự không chạm tới ô 4,5–18,6 % chiều ngang.
- Duy nhất SC_031 (9:31–9:42) có nền nhiều chi tiết dưới ô (độ cạnh 7,2, ngưỡng báo 6): ô đè lên một đoạn ống chạy dọc đáy. Ống vẫn thấy được ở phần còn lại của khung.

## Vấn đề còn tồn tại
Các mục dưới đây **chưa sửa** trong bản này.

| # | Mốc | Shot (beat) | Vấn đề | Vì sao quan trọng | Cách sửa đề xuất | Ảnh hưởng | Phải render lại |
|---|---|---|---|---|---|---|---|
| 1 | 7:03–7:14, 7:40–7:57, 9:25–9:42, 10:09–10:21, 10:29–10:40 | SC_022, SC_024, SC_030, SC_031, SC_033, SC_034 | Khi nước đã trong (độ trong 0,5), khối nước vẫn xanh xám nhạt. Mặt nước, dải đáy và nhãn "Sea surface" giúp đọc ra là nước, nhưng màu nước tự nó còn gần màu nền | Người xem mới phải dựa vào đường mặt nước và dải đáy | Có hai hướng, đều phải chủ kênh chọn: (a) đổi nền sau khung ngang sang màu ấm hơn để nước tách ra; (b) chấp nhận mức hiện tại. Nước đậm hơn thì AgX làm xám đi (đã thử) | Hình | 6 shot nếu chọn (a) |
| 2 | 10:07,5–10:08,5 | SC_033 (B33), lúc camera hạ | Khoảng 1 s: nước bắt đầu trong khi camera chưa tới khung ngang. Lộ hai mảng bóng phao xanh đậm dưới đáy và một góc mép bãi nước | Ngắn, nhưng cùng loại hình mà v1 đã sửa ở B30/B31 | Lùi thời điểm làm trong ở B33 thêm khoảng 0,5 s, hoặc kéo dài lúc hạ camera | Hình | SC_033 (450 frame) |
| 3 | 11:13–11:16 | SC_037 (B37) | 2,8 s đầu chỉ có nhãn góc | Lời dẫn đang hỏi đúng câu trên nhãn, nên không lạc; nhưng vẫn là một khoảng trống | Hiện vạch chia hai cột vẽ mờ từ khung đầu, giống B03 | Hình | SC_037 (671 frame) |
| 4 | 2:24–2:39 (cue 35) | SC_009 (B09.s2) | Phụ đề 17,1 ký tự/s, vượt khuyến nghị 17,0 (chưa đổi từ v1) | Chỉ là cảnh báo | Tách cue ở chỗ ngắt cụm | Phụ đề | Không |
| 5 | 4:59–5:34 | SC_016 (B16) | Card số học dài 34 s (chưa đổi từ v1) | Đoạn tĩnh dài nhất phim | Để chủ kênh xem rồi quyết | Nhịp | Không (nếu giữ) |
| 6 | 2:26,5 và 2:44,4 | SC_009, SC_010 | Hai tiếng SFX chưa có ai nghe chọn | Chủ kênh muốn nghe hai bản trước khi quyết | Chủ kênh nghe bản có SFX và bản `_no_sfx` | Âm thanh | Không |

## `visual_variety`
- Chủ kênh đã chấp nhận ngoại lệ cho đúng hai chuỗi: **B08–B14** (SC_008–SC_014, 7 shot) và **B27–B31** (SC_027–SC_031, 5 shot). Hồ sơ ở `project.json` → `variety_exception.runs`, và `DEC-VARIETY-B08-B14-B27-B31`.
- Mọi chuỗi khác vẫn theo ngưỡng 4. Thêm, bớt hay đổi loại một shot trong hai chuỗi này thì cần quyết định mới.

## Kỹ thuật (đo, không phải nghe)
- **Bản ghép:**
  - 18 820 frame, 1280×720, 24 fps;
  - −16,4 LUFS, đỉnh thật −1,2 dBTP;
  - 0 lỗi giải mã, 0 đoạn đen;
  - 7 điểm nối giữa chương đều qua SSIM.
- **8 chương:** mỗi chương 0 lỗi, có watermark; −16,3 đến −16,5 LUFS.
- **Phụ đề:** 181 cue, 126 câu; dòng dài nhất 42 ký tự; 1 cảnh báo tốc độ (mục 4).
- **Bản có SFX và không SFX** (`qa/excerpt_FULL_V2.json`, PASS):
  - −16,4 LUFS; đỉnh thật −1,0 và −1,2 dBTP;
  - chỉ khác ở 2 tiếng: 2:26,5 (B09) và 2:44,4 (B10). Mức SFX không đổi: thấp hơn lời dẫn 14 dB, 0 mẫu bị cắt;
  - Whisper theo từng shot: 44/44 shot không kém đi khi có SFX; WER cao nhất 4,1 % (SC_016, tên riêng).

## Rủi ro người xem rời đi (định tính)
Không đổi so với v1, vì kịch bản và nhịp không đổi:
- **0:24–0:57 (SC_003):** card hai tiền lệ 32,5 s. Nay có sơ đồ từ 0,5 s, nhưng vẫn là đoạn chữ đầu tiên.
- **4:34–5:34 (SC_015–SC_016):** gần một phút card số học.
- **10:57–11:41 (SC_036–SC_037):** hai card liền nhau ngay trước kết luận.

## Mười câu hỏi trải nghiệm người xem (đánh giá của agent)
1. **30 giây đầu có cho biết phim hỏi gì không?** Có. Mở đầu giữ nguyên v1.
2. **Người xem có biết đang xem thiết kế minh họa hay công trình thật không?** Có. "Illustrative design" ở mô hình; B33 ghi "Schematic of a 2026 concept study's module"; tiền lệ thật là card có nguồn.
3. **Cơ chế nổi (C2) có hiểu được mà không cần công thức không?** Có, giữ nguyên v1.
4. **Vì sao một phao chưa thành thành phố?** Rõ hơn v1. Khung cận cho thấy chênh 0,66 m bằng thước, rồi mới tới cầu bản lề.
5. **Nước chuyển động (C4) có bị hiểu thành mô phỏng không?** Không. Có ghi chú "not a hydrodynamic simulation".
6. **Cọc, dây neo, neo (C5) có thấy được không?** Có. Nước còn nhạt (mục 1).
7. **Hạ tầng (C6) có cho thấy thành phố vẫn nối với đất liền không?** Có. B31 nay tách rõ ba tuyến ống khỏi dây neo.
8. **Phần "khó" (C7) có cân bằng không?** Có. B33/B34 nay thấy rõ mực nước, không còn trông như mô hình trên cạn. Còn 1 s chuyển ở B33 (mục 2).
9. **Kết luận có trả lời câu hỏi mở đầu không?** Có, theo ba mức. B38 nay đọc được thành một mạng nối.
10. **Có chỗ nào người xem dễ bỏ không?** Ba đoạn card dài ở trên. Agent không đo được, chủ kênh cần xem.
