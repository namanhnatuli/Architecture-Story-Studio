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
