# Xem lại biên tập có mốc thời gian: M8, revision m8-r1 (đủ sáu họ cầu)

- **Người xem:** agent, trên bản review 1080p đầu tiên của m8-r1 (`output/why_bridges_look_different_M8_INTERNAL_REVIEW_1080p.mp4`, 867,6 s).
- **Cách xem:**
  - tấm ảnh mỗi 3 s cho C1, C6, C7, C8, C11 (`qa/review_cut_m8/C*_sheet.jpg`, chỉ để tham khảo, không commit);
  - frame gốc ở những chỗ nghi ngờ;
  - ảnh tĩnh render trực tiếp sau khi sửa.
- **Phạm vi:**
  - C2–C5 và C10 giữ nguyên hình của m7-r1 (đã xem ở M7, xem phần dưới).
  - C9 chỉ bị bỏ bớt beat.
- Đây là nhận xét **của agent**, không phải duyệt biên tập. Không có số liệu khán giả thật.

## Lỗi tìm thấy ở bản 1080p đầu và đã sửa
| Mốc | Shot | Vấn đề | Vì sao quan trọng | Cách sửa | Ảnh hưởng | Phải render lại |
|---|---|---|---|---|---|---|
| 7:55–8:09 | SC_040 (B50) | Dây văng được highlight gần như biến mất, đúng lúc nhãn "Stay cables" hiện lên | Bộ phận đang được giảng giải lại không nhìn thấy. Highlight là phát sáng theo màu của chính vật liệu, và cáp xám sáng `#C3C7C9` hòa vào nền | Vật liệu `cable` đổi sang xám thép `#7B8890`. Dây treo và dây văng mảnh cũng dễ đọc hơn khi không highlight | Vật liệu | Mọi shot (thư viện vật liệu là đầu vào render) |
| 6:18–6:33 | SC_033 (B43) | Giằng đỉnh bay riêng thành những vệt chéo, như mưa | Rối mắt, đúng lúc người xem cần thấy nhịp treo được nâng lên | Giằng đi cùng phần giàn nó giằng (tay neo +1,0 m, tay hẫng +2,0 m) | Cấu hình nổ tách (engine) | Mọi shot (file engine) |
| 8:27–8:45 | SC_042 (B52) | Các đốt mặt cầu chỉ hạ 0,8 m, nên không thấy thứ tự lắp từ tháp ra | Ý chính của câu (dựng hẫng cân bằng, không đà giáo) không hiện trên hình | Đốt hạ 2,4 m, dây văng nâng 1,8 m. Khối mặt cầu trên tháp đứng yên, các đốt trở lại theo lớp từ tháp ra ngoài | Cấu hình nổ tách | Như trên |
| 5:34–5:50 | SC_030 (B40) | 15,6 s sông trống | Đoạn yếu nhất của chương mới. Vẫn dưới ngưỡng tĩnh 14 s nhờ NOTE xuất hiện ở câu 2 | Push-in chậm 10%. Shot sau là cắt cứng sang cảnh lắp ráp | Camera | Shot này |
| 6:53–7:06 | SC_035 (B45) | Nhãn "Main cable" chỉ hiện khoảng 2 s, vì neo vào từ cuối câu | Không đọc kịp | Neo vào từ "attached" | Chú thích | Shot này |

**Kiểm lại trên bản 1080p lượt 2** (2026-11-01, frame ở 5:46, 6:25, 7:04, 8:04, 8:40): cả 5 bản sửa đều hiện đúng.
- Push-in trên sông trống.
- Giằng đi cùng giàn khi tháo rời.
- Hai nhãn "Main cable" và "Suspenders" cùng hiện.
- Dây văng vẫn thấy rõ lúc highlight.
- Chú thích nén mặt cầu.

**Lỗi đã sửa trước bản 1080p** (QA, planner, ảnh tĩnh):
- giao nhau khi nổ tách ở cả ba cầu nhịp lớn (Blender QA 789/792, sau khi sửa 792/792);
- mép mặt đất lộ ra ở cảnh so sánh ba cầu nhịp lớn;
- B01B, B51: hai mô hình 72 m đặt cạnh nhau không đọc được ở 640×360, nên chuyển thành mỗi shot một cầu và một sơ đồ;
- câu "Side by side…" mâu thuẫn với hình (sửa câu chữ);
- ASR nghe "great" thành "grate";
- bản khóa đầu dài 15,4 phút.

## Nhận xét theo chương (m8-r1)
- **C1 Hook (0:00–0:52):**
  - Ba cầu trên khoảng hở nhỏ, rồi "Over wider water, the answers change again": công-xôn (8,5 s), cầu treo (4,5 s), dây văng (4,6 s), mỗi cầu một shot.
  - Card tiêu đề hiện thêm chữ "Span".
  - Phần mở đầu dài hơn m7-r1 (52 s so với 34 s), nhưng có hình mới liên tục.
- **C6 The cantilever (5:34–6:53):**
  - sông rộng trống, có NOTE "A wider crossing (illustrative, not to scale)";
  - cầu được lắp theo lớp: trụ, tay neo, tay hẫng, nhịp treo;
  - mặt đứng có ba nhãn hiện theo đúng từ được đọc;
  - nổ tách: nhịp treo nâng cao nhất;
  - ảnh Queensboro.
- **C7 The suspension bridge (6:53–7:55):**
  - dây treo và cáp chính được highlight và gắn nhãn;
  - "Cables: tension" và "Towers: compression" xuất hiện theo từ "tension"/"compression", nhãn khối neo theo "anchored";
  - giàn tăng cứng hạ xuống trong cảnh nổ tách;
  - ảnh Brooklyn (23 s, chữ hiện theo hai câu).
- **C8 The cable-stayed bridge (7:55–9:09):**
  - dây văng và tháp gắn nhãn;
  - sơ đồ so sánh hai mặt đứng: tháp thấp và cáp võng về khối neo, đối lại tháp cao và dây văng xuống mặt cầu;
  - nổ tách theo thứ tự hẫng cân bằng, kèm "Deck: squeezed by the stays";
  - card kinh tế nhịp lớn, ba thanh hiện theo từ.
- **C11 (12:58–14:28):**
  - so sánh ba cầu nhịp ngắn (ROW), rồi ba cầu nhịp lớn (STACK, chỉ cần đọc được dáng tổng thể);
  - dòng thời gian thêm "Most common steel bridge: the plate girder, a beam" theo câu mới.

## Rủi ro người xem rời đi (định tính) và còn để ngỏ
- **Thời lượng 14,46 phút** sát mức trên của khoảng chấp nhận (15). Mục tiêu 10–12 phút không còn đạt được nếu giữ đủ sáu họ. Nếu chủ kênh muốn ngắn hơn, ứng viên cắt là: B27/B29 (mô hình nối ảnh ở C10), B22 (cầu cạn), B48 câu 2.
- **Card ảnh Brooklyn 23 s** và **card kinh tế 24,6 s** là hai shot 2D dài nhất.
- **Mô hình nhịp lớn không theo tỉ lệ thật:** cầu thật dài hàng trăm đến hàng nghìn mét. NOTE ở B40 nói rõ điều này. Các con số nhịp đều nằm trong lời dẫn và card, có nguồn.
- **Cầu Queensboro thật không có nhịp treo ở giữa** (NCHRP §3.7). Phim không nói nó có. Tuy vậy, mô hình minh họa (có nhịp treo) xuất hiện ngay trước ảnh, nên người duyệt có thể muốn thêm một NOTE.
- **Hai UNCERTAIN của kiểm tra lời–hình** để người duyệt xem: B33.s3 ("right answer in the right place", không phải trái/phải) và B34.s2 ("the arrows" nói chung).

## Mười câu hỏi trải nghiệm người xem (đánh giá của agent, m8-r1)
1. **Câu hỏi trung tâm có rõ ngay không?** Có. Sáu cầu xuất hiện trong 33 s đầu, câu hỏi ở 0:34.
2. **Ba chương mới có nói điều mới, không lặp lại không?** Có:
   - công-xôn: dầm cải biến, dựng không cần đà giáo;
   - cầu treo: treo bằng cáp, kéo và nén, khối neo, giàn tăng cứng;
   - dây văng: dây thẳng xuống mặt cầu, tháp cao, dựng hẫng cân bằng, kinh tế.
3. **Có so sánh trực tiếp hai loại dễ nhầm không?** Có, sơ đồ B51 đặt cầu treo cạnh cầu dây văng.
4. **Lực có được bịa không?** Không. Mỗi mũi tên hay nhãn lực trích một claim được đọc. Dây văng không mang nhãn kéo vì không có câu nguồn nào nói thế.
5. **Có kể chuyện tiến bộ tuyến tính không?** Không. Cầu treo đã dài nhất thế giới năm 1849; công-xôn là chuẩn suốt 1880–1960; dầm vẫn là cầu thép phổ biến nhất.
6. **Có đoạn tĩnh dài không?** Không có đoạn nào > 14 s không đổi hình. Đoạn dài nhất 12,4 s.
7. **Chương nào yếu nhất?** C2 (toàn 3D_HOLD, có cảnh báo `chapter_variety`), như ở m7-r1.
8. **Người xem có hiểu mô hình chỉ là minh họa không?** Có. "Illustrative model" xuất hiện ở các cầu mới, NOTE ở B40, và lời miễn trừ ở cuối.
9. **Phụ đề:** 199 câu, SRT + mov_text.
10. **Âm lượng:** −16,4 LUFS, true peak −1,0 dBTP.

---

# Xem lại biên tập và trải nghiệm người xem, có mốc thời gian (M7)

- Người xem: agent, trên **rough cut 640×360** (`output/why_bridges_look_different_documentary_INTERNAL_REVIEW.mp4` bản preview, 641,29 s). Cách xem: tấm ảnh mỗi 3 s cho từng chương (`qa/rough_cut/C*_sheet.png`), frame gốc ở độ phân giải đầy đủ cho mọi chỗ nghi ngờ, và soi qua MCP cho C4.
- Đây là nhận xét **của agent**, không phải duyệt biên tập. **Không có số liệu khán giả thật**: phim chưa đăng, nên không có số liệu giữ chân người xem (retention). "Rủi ro người xem rời đi" dưới đây chỉ là đánh giá định tính.
- Mốc thời gian theo bản 641,29 s. Bản review cuối dài 646,46 s; khác biệt chỉ ở câu thêm vào cuối B35.

## Lỗi tìm thấy và đã sửa
| Mốc | Shot | Vấn đề | Vì sao quan trọng | Cách sửa | Ảnh hưởng | Phải render lại |
|---|---|---|---|---|---|---|
| 2:08–2:33 | SC_014 (B09 push-in) | NOTE "Illustrative model" lớn dần và trôi ra mép phải | Nhãn bắt buộc bị cắt mất, đúng lúc người xem cần biết đây là mô hình minh họa | Rig chú thích đi theo camera và co giãn theo ortho; QA `overlays_screen_fixed` (độ trôi ≈ 1e-7) | Hoạt hình (engine) | Mọi shot, vì file engine đổi (cache nhóm `engine`) |
| 8:07–8:18 | SC_038 (B27) | NOTE "…not the Carrollton Viaduct" bị cắt | Mô hình có thể bị hiểu là bản dựng lại cây cầu thật | Như trên | Hoạt hình | Như trên |
| 8:37–8:51 | SC_040 (B29) | NOTE "…not the Promontory trestle" bị cắt | Như trên | Như trên | Hoạt hình | Như trên |
| 6:07–6:22 | SC_031 (B21) | Ảnh Humpback còn viền phim đen | Trông như ảnh scan chưa xử lý; viền HAER không phải nội dung | Đo dải tối ở mép, nới vùng cắt; ghi trong `modifications` | Dựng hình (card) | Chỉ card này (byte ảnh và vùng cắt là đầu vào render) |
| 8:18–8:37 | SC_039 (B28) | Ảnh Promontory còn viền đen | Như trên | Như trên | Dựng hình | Chỉ card này |
| 8:51–9:18 | SC_041 (B30) | Ảnh Bollman còn viền đen | Như trên | Như trên | Dựng hình | Chỉ card này |
| 10:17–10:37 | SC_046 (B34) | 19,7 s push-in không chữ, trong khi câu cuối là lời miễn trừ | Lời miễn trừ quan trọng nên có cả trên hình, không chỉ trong lời | NOTE "Models are illustrations, not engineering designs" theo câu đó | Hoạt hình (chú thích) | Shot này |
| 10:37–10:41 | SC_047 (B35) | Card credit 6 dòng chỉ hiện 4 s | Không đọc kịp phần ghi công ảnh và nguồn | Thêm câu "The sources and photo credits are listed in the description." (ASR WER 0); card hiện 9,2 s | Lời dẫn + dựng | Shot này; timing chỉ đổi ở cuối phim |

Lỗi đã sửa trước rough cut (checkpoint C và QA): góc nhìn mố B12; hình học ván khuôn B13; bố cục B14; nhãn dòng thời gian tràn và chồng nhau (B24, B33); 8 card liền nhau ở chương 6; ba đoạn tĩnh > 14 s.

## Nhận xét theo chương (sau khi sửa)
- **C1 Hook (0:00–0:35):** ba mô hình lần lượt hiện, mỗi cái ~4 s, rồi đặt cạnh nhau cùng tỉ lệ. Câu hỏi xuất hiện ở 0:17. Card tiêu đề hiện từng chữ "Materials / Site / Time" đúng lúc được đọc. Mở đầu rõ ràng, không giật gân.
- **C2 The problem (0:35–1:25):** dựng dần: tải → mặt đất → kết cấu phần trên → mố/trụ → đường truyền tải → móng, mỗi bước theo đúng câu. Shot nào cũng là 3D_HOLD (QA ghi cảnh báo `chapter_variety`), nhưng không có đoạn tĩnh nào > 14 s. Kết bằng khoảng trống sông 10 s, làm cầu nối sang chương sau.
- **C3 The beam (1:25–2:33):** cầu gỗ "rơi" vào khoảng trống, tách theo lớp, rồi chú thích dầm → xà mũ → cột. Push-in 25 s chậm, có điểm nhấn sáng ở các cột khi câu nói về nhịp ngắn. Đây là shot dài nhất của phần 3D, nhưng có chuyển động liên tục.
- **C4 The arch (2:33–3:55):** mạnh nhất về hình: các đá vòm tách ra kèm tên; lực đẩy dọc vòm và phản lực; góc chính diện với mố/trụ; card ván khuôn; card đánh đổi chi phí/độ bền với khung nhấn cột gỗ.
- **C5 The truss (3:55–5:19):** khớp và chú giải → biên nén/kéo ở góc chính diện (thanh bụng không tô màu) → Pratt có NOTE năm → thay bụng sang Warren → tách lớp chế tạo sẵn có NOTE theo câu.
- **C6 Why designs differ (5:19–7:24):** card "Which design is best? It depends." → ba shot 3D vật liệu có NOTE → ảnh Humpback → sơ đồ thung lũng/cầu cạn → khoảng trống sông ("how far one structure has to reach") → thanh nhịp hiện theo từ được đọc → dòng thời gian. Không còn chuỗi 2D dài.
- **C7 Real-world decisions (7:24–9:31):** sơ đồ Đông/Tây → ảnh Carrollton → mô hình vòm có nhãn "not the Carrollton Viaduct" → ảnh Promontory → mô hình gỗ có nhãn → ảnh Bollman (27,5 s, ảnh trôi chậm, chú thích hiện theo câu) → ba ảnh cạnh nhau.
- **C8 Conclusion (9:31–10:46):** ba mô hình cạnh nhau với hai NOTE "1 · …" → card "2 · The world it was built in" → dòng thời gian "not a simple story of progress" → push-in cuối có lời miễn trừ → credit.

## Rủi ro người xem rời đi (định tính) và còn để ngỏ
- **Sơ đồ Đông/Tây (7:24, SC_036)** chỉ là một khung chữ nhật chia đôi, có nhãn "schematic, not to scale". Trung thực nhưng đơn giản. Nếu muốn bản đồ thật, cần dữ liệu đường biên có giấy phép (ví dụ Natural Earth, phạm vi công cộng), và phải được chủ kênh chọn.
- **Ảnh Bollman 27,5 s (8:51)** là shot 2D dài nhất. Chú thích hiện theo 4 câu và ảnh trôi chậm, nhưng có thể cắt bớt khi biên tập.
- **Đầu mỗi card** có 0,3–0,4 s nền giấy trước khi phần tử đầu tiên fade vào. Đây là cách chuyển cố ý từ 3D sang 2D. Nếu người duyệt thấy như chớp trắng, có thể cho phần tử đầu hiện từ frame 1.
- **Câu hỏi được lặp** ("So why don't bridges all look the same?" ở 0:17 và 9:31) là có chủ ý: câu đóng khung toàn phim.
- Tốc độ phụ đề tối đa 19,3 ký tự/s (bản rough cut); 144 câu, không dòng nào quá 42 ký tự.

## Mười câu hỏi về trải nghiệm người xem (đánh giá của agent)
1. **Câu hỏi trung tâm có rõ ngay từ đầu không?** Có. Ba kiểu cầu hiện trong 15 s đầu; câu hỏi được nói ở 0:17 và hiện thành tiêu đề.
2. **Mỗi chương có cho biết điều gì mới không?** Có. Bài toán chung → dầm → vòm → giàn → các yếu tố quyết định → ba ví dụ thật → câu trả lời hai lớp.
3. **Hình có giải thích trực tiếp lời dẫn không?** Phần lớn có: chú thích và phần tử card hiện theo câu, thậm chí theo từ. Chỗ yếu nhất là sơ đồ Đông/Tây (7:24), vì chỉ là khung chia đôi.
4. **Người không học kỹ thuật có theo được không?** Thuật ngữ được giới thiệu ngay trên hình (voussoir, keystone, superstructure/substructure, chord, web). Không có công thức hay con số lực nào.
5. **Có thuật ngữ thừa không?** Ít. "Superstructure/substructure" và "web members" là các từ khó nhất; mỗi từ đều có nhãn trên hình.
6. **Bộ phận quan trọng có thực sự nhìn thấy không?** Kiểm tra tầm nhìn đạt (18/20 dòng mục tiêu, 2 dòng tự sửa). Chỗ mố cầu vòm bị che ở góc ba phần tư đã đổi sang góc chính diện.
7. **Chuyển cảnh có hợp lý không?** Cắt khớp (match cut) trong cùng một nhóm camera; cắt cứng khi đổi mô hình hoặc sang card. Đầu card có 0,3–0,4 s nền giấy (xem bên dưới).
8. **Có đoạn lặp về hình không?** Không có hai shot liên tiếp giống nhau (`no_repeated_visuals`). Ba mô hình cạnh nhau xuất hiện hai lần (mở đầu và kết), có chủ ý. Chương 2 chỉ có 3D_HOLD (cảnh báo).
9. **Có cảm giác tiến triển không?** Có. Từ vật lý chung sang từng kiểu cầu, rồi sang bối cảnh, ví dụ thật và kết luận. Dòng thời gian được dùng để nói rằng đây *không* phải chuỗi tiến bộ.
10. **Phần kết có trả lời câu hỏi mở đầu không?** Có, theo hai lớp: cách kết cấu chịu tải, và thế giới mà cây cầu được xây trong đó. Phần kết cũng nhắc rằng mỗi dạng vẫn có thể là câu trả lời đúng ở đúng nơi.

## Sửa thêm sau bản review và kiểm tra cuối
| Mốc | Shot | Vấn đề | Vì sao quan trọng | Cách sửa | Ảnh hưởng | Phải render lại |
|---|---|---|---|---|---|---|
| 4:12 | SC_022 (B16) | Chú giải, "Top chord" và "Bottom chord" hiện cùng lúc (phát hiện bằng báo cáo "cụm chú thích dày") | Ba chữ và hai ký hiệu lực mới xuất hiện một lúc, khó theo dõi | Hai nhãn biên hiện đúng lúc từ "top" (4,25 s trong shot) và "bottom" (5,88 s) được đọc | Chú thích | Chỉ SC_022 (347 frame) |
| ≈1:54 | SC_013 (B08) | Quanh xà mũ có đường truyền tải, nhãn xà mũ, mũi tên tải và nhãn cột (soi qua MCP) | Dày về không gian, nhưng các phần hiện lần lượt theo câu | Chưa sửa; để người duyệt quyết định khi biên tập | Chú thích | SC_013 nếu sửa |

Still 1080p (checkpoint F): chữ chú thích, chữ card, vân đá và mũi tên đều sắc nét ở độ phân giải gốc. Không thấy chi tiết nào khó đọc trên màn hình nhỏ.
