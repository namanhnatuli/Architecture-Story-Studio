# Storyboard sơ bộ (46 shot, 10:36)

## Cảnh dùng chung (không dựng một cảnh mới cho mỗi câu)

| Cảnh | Nội dung | Shot dùng |
|---|---|---|
| **S1 `district_bay`** | Quận C hoàn chỉnh trong vịnh (nước, đáy biển, bờ, đê, neo, hạ tầng, nhà, phao) | SH01, SH03, SH23, SH25–SH29, SH32, SH38, SH39, SH41, SH43 |
| **S2 `platform_section`** | Một phao, có mặt cắt (đã thử: prototype P1, P2) | SH05, SH06, SH08–SH10, SH37 |
| **S3 `neighbourhood`** | Năm phao, khe, khớp, cọc (đã thử: prototype P3, P4) | SH13–SH15, SH19 |
| **K `cards`** | Card 2D và sơ đồ của Studio | SH02, SH07, SH11, SH12, SH16, SH17, SH20–SH22, SH30, SH33–SH36, SH40, SH42, SH44, SH45 |

## Quy ước cột
- **Ev** (bằng chứng):
  - CLM_xxx là claim trong `research/sources.json`;
  - *calc* là `analysis/results.json`;
  - *scn* là hợp đồng kịch bản.
- **Fam** là họ asset (`BLENDER_ASSET_BLUEPRINT.md`):
  - A môi trường biển, B phao, C mối nối, D neo, E nhà, F hạ tầng, K card.
- **Cplx** là độ phức tạp render: L thấp, M trung bình, H cao.
- **Conf** là độ tin cậy của nội dung: H cao, M trung bình.
- **Chiến lược** là các chiến lược đã có trong planner (`planner/intents.py`). **NEW** đánh dấu năng lực còn thiếu (`PRODUCTION_FEASIBILITY.md`).

## C1: Could We Actually Do This? (0:00–0:50)

| Shot | Beat | Ý lời dẫn | Câu hỏi người xem | Khái niệm | Ev | Fam | Mục tiêu | Camera | Chiến lược / hoạt ảnh | Điều được lộ ra | Dài | Chú thích | Cplx | Conf | Giới hạn |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| SH01 | B01 | "Ten thousand people… not one standing on land." | Đây là gì? Có thật không? | Quy mô | scn | A,B,E,F | toàn quận | Aerial cao, đẩy chậm | HOLD + PUSH_IN | Lời hứa: một thành phố | 12 s | NOTE "Illustrative design — not a real or proposed project" | H | H | Cảnh lớn, cần instancing |
| SH02 | B02 | "One small floating neighbourhood exists. Bigger ones are plans." | Đã có ai làm chưa? | Tiền lệ và đề xuất | CLM_010, 011, 031, 033, 040 | K | thang quy mô: khoảng 100 người (đã xây), 12.000 (đề xuất, chưa được báo cáo là đã xây), ngưỡng 20 ha | 2D | CARD, phần tử theo từ | Ranh giới thật và đề xuất | 12 s | nhãn "built", "proposed", "status checked Nov 2026" | L | M | Không có ảnh có giấy phép (chưa tìm) |
| SH03 | B03 | "We'll take it apart, and build it back one problem at a time." | Thành phố gồm những gì? | Các hệ | scn | A–F | đê → neo → hạ tầng → nhà → phao | Three-quarter, kéo lùi nhẹ | SEQUENCE: FADE_OUT theo nhóm, khớp lời | Thành phố là chồng hệ thống | 20 s | tên từng hệ khi nó biến mất | H | H | — |
| SH04 | B04 | "Problem one: how does something this heavy float?" | — | Chuyển | — | B | một phao trống | Three-quarter gần | HOLD | Điểm bắt đầu | 6 s | — | L | H | Hơi tĩnh; giữ ngắn |

## C2: The First Problem: Making Buildings Float (0:50–2:30)

| Shot | Beat | Ý lời dẫn | Câu hỏi | Khái niệm | Ev | Fam | Mục tiêu | Camera | Chiến lược | Lộ ra | Dài | Chú thích | Cplx | Conf | Giới hạn |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| SH05 | B05 | "Same concrete. One sinks, one floats." | Bê tông nổi được à? | Hình dạng | CLM_002, calc (1.108 m³; khối 10,35 m; hộp nổi 1,62 m) | A,B | khối đặc; hộp rỗng | ELEVATION mặt cắt | SIDE_BY_SIDE; REVEAL từ trên; khối đặc dừng ở đáy | Hình dạng quyết định | 14 s | "same volume of concrete" | M | H | Không hoạt ảnh "chìm dần"; REVEAL tới vị trí cuối |
| SH06 | B06 | "It pushes aside its own weight in water." | Vì sao nổi? | Archimedes | CLM_001, calc (khoảng 4.850 t, khoảng 4.730 m³) | A,B,E | khối nước bị chiếm chỗ (vàng), đường nước | Mặt cắt chính diện (prototype P1) | HOLD_HIGHLIGHT: vàng sáng dần | Khối nước bị đẩy ra | 14 s | "displaced water", số minh họa | M | H | Đã thử: đọc được |
| SH07 | B07 | "A real one: about 340 tonnes, about 340 cubic metres." | Ngoài đời thì sao? | Mốc thật | CLM_012, 013, calc (khối 7 m) | K | nhà trên phao; khối nước 7 m | 2D | CARD | Cỡ người thật | 12 s | "two builders' figures: 340–350 t" | L | H | Ảnh Schoonschip chưa có giấy phép; dùng sơ đồ |
| SH08 | B08 | "Most of what it carries is itself." | Cái gì nặng nhất? | Phân bố khối lượng | calc (thân phao 55%) | B,E | thân phao, nhà, tải | Three-quarter | EXPLODE theo lớp + thanh 2D | Bất ngờ 1 | 12 s | % theo lớp, ghi *illustrative* | M | H | — |
| SH09 | B09 | "Add a floor, and it sits deeper." | Thêm tải thì sao? | Mớn nước | CLM_003, calc (+33 cm/tầng) | B,E | tầng 4; thước mớn nước | Cận vạch mớn nước (prototype P2b) | REPLACE (3→4 tầng) + **NEW** `SINK` (hạ cả phao theo Δ tính sẵn) | Tải làm phao chìm | 14 s | thước 1 m, "+33 cm" | M | H | Ở khung toàn cảnh 33 cm không thấy (P2), nên phải cận cảnh |
| SH10 | B10 | "Half a metre more hull buys the freeboard back." | Sửa thế nào? | Mạn khô | calc (0,69 → 1,13 m; +106 t) | B | thân 4 m và 4,5 m | ELEVATION | SIDE_BY_SIDE | Lần sửa A′ có lý do | 10 s | "freeboard" | L | H | — |
| SH11 | B11 | "Push a hundred tonnes to the edge: it barely tilts." | Có lật không? | G, B, M; nghiêng | CLM_005, 006, 009, calc (0,42°) | K | G, B, M; khối 100 t | Sơ đồ mặt cắt | CARD (sơ đồ) | Phao rộng rất "cứng" | 14 s | "small angles only" | L | H | Sơ đồ rõ hơn 3D |
| SH12 | B12 | "Stiff means it follows the water." | Vậy vấn đề là gì? | Ổn định khác tiện nghi | CLM_007 (suy luận, ghi rõ) | K | thân hẹp và phao rộng | 2D | CARD | Mở sang C4 | 10 s | "conceptual" | L | M | Không có số chuyển động |

## C3: Why One Platform Isn't a City (2:30–3:52)

| Shot | Beat | Ý lời dẫn | Câu hỏi | Khái niệm | Ev | Fam | Mục tiêu | Camera | Chiến lược | Lộ ra | Dài | Chú thích | Cplx | Conf | Giới hạn |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| SH13 | B13 | "Why not just weld them together?" | Nhân bản được không? | Module | scn | B,E | 5 phao | Three-quarter | ASSEMBLE_IN (REVEAL từng phao) | Khu hình thành | 12 s | — | M | H | — |
| SH14 | B14 | "Different loads, different heights." | Vì sao không hàn? | Mớn nước khác nhau | calc (lệch 0,66 m) | B,C,E | cầu cứng → cầu có khớp | ELEVATION | HIGHLIGHT_REPLACE_HIGHLIGHT | Phải có khớp | 16 s | "deck levels differ ~0.66 m" | M | H | Không vẽ gãy; cầu cứng chỉ phát sáng đỏ |
| SH15 | B15 | "Every joint is where stress gathers." | Mối nối trông ra sao? | Mối nối | CLM_042, 056, 015 | C,F | khe, cầu đi bộ, đường hạ tầng | Cận cảnh | CLOSEUP_HIGHLIGHT | Ba bộ phận của mối nối | 14 s | "conceptual geometry" | M | H | Không chọn cơ cấu cụ thể |
| SH16 | B16 | "Ten thousand people: two hundred platforms, hundreds of joints." | Bao nhiêu phao? | Đếm | calc (209 phao, khoảng 390 mối nối) | K | lưới mặt bằng | 2D mặt bằng | CARD, chấm hiện dần | Quy mô mối nối | 14 s | số, *illustrative* | L | H | — |
| SH17 | B17 | "Fewer joints, or easier pieces." | To hay nhiều? | Đánh đổi | calc, CLM_014, 053 | K | 40 m và 100 m cùng tỉ lệ | 2D mặt bằng | CARD SIDE_BY_SIDE | Không có đáp án chung | 16 s | khối lượng mỗi phao; "too big for traditional dry docks" | L | H | — |
| SH18 | B18 | "…on water that will not keep still." | — | Chuyển | — | A,B | khu, gợn nước | Ngang mặt nước | HOLD | — | 10 s | — | L | H | Gợn nước tĩnh (texture) |

## C4: The Water Never Stays Still (3:52–5:16)

| Shot | Beat | Ý lời dẫn | Câu hỏi | Khái niệm | Ev | Fam | Mục tiêu | Camera | Chiến lược | Lộ ra | Dài | Chú thích | Cplx | Conf | Giới hạn |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| SH19 | B19 | "Each platform moves on its own." | Chuyện gì xảy ra khi có sóng? | Chuyển động tương đối | CLM_042 | A,B,C | 5 phao, khe | Three-quarter thấp | **NEW** `CONCEPT_MOTION` (heave/pitch hình sin, tất định, lệch pha) | Khe co giãn | 18 s | **"Conceptual motion visualization — not a hydrodynamic simulation"** | M | M | Biên độ không mang nghĩa |
| SH20 | B20 | "Even in an Amsterdam canal, residents feel it." | Người ở có thấy? | Tiện nghi | CLM_022 | K,E | tầng trên | 2D + cận nhà | CARD | Chuyển động là chuyện con người | 10 s | dẫn nguồn (Yale E360, 2021) | L | H | — |
| SH21 | B21 | "Big platforms don't just move — they bend." | Phao lớn thì sao? | Hydro-elastic | CLM_053 | K | phao dài uốn | 2D mặt cắt | CARD, đường cong vẽ dần | Bài toán mở | 12 s | "exaggerated, conceptual; an open research problem" | L | M | Không có số |
| SH22 | B22 | "The first fix is where you build." | Giảm sóng thế nào? | Địa điểm | CLM_050 | K | vịnh kín và vịnh hở | 2D bản đồ sơ đồ | CARD | Địa điểm là thiết kế | 14 s | "limited fetch" | L | H | Không gắn địa danh thật |
| SH23 | B23 | "Homes inside, tougher functions outside, a breakwater where it's open." | Bố cục quận? | Bố cục, đê | CLM_055, 051, 052 | A–F | vòng trong/ngoài, đê | TOP → three-quarter | SEQUENCE: HIGHLIGHT vòng trong, REVEAL đê | Thành phố được tổ chức theo chuyển động | 24 s | "reduces waves — does not remove storm risk" | H | H | — |
| SH24 | B24 | "…it still has to stay where we put it." | — | Chuyển | — | A | quận | Ngang mặt nước | HOLD | — | 6 s | — | L | H | Có thể gộp vào SH23 |

## C5: Keeping the City in Place (5:16–6:26)

| Shot | Beat | Ý lời dẫn | Câu hỏi | Khái niệm | Ev | Fam | Mục tiêu | Camera | Chiến lược | Lộ ra | Dài | Chú thích | Cplx | Conf | Giới hạn |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| SH25 | B25 | "Under the surface: what holds it." | Cái gì giữ nó? | Giữ vị trí | CLM_020 | A,D | mặt nước → làm mờ; cọc | Three-quarter thấp (prototype P4) | SEQUENCE: GHOST nước (2 bước), HIGHLIGHT cọc | Hệ neo vô hình | 16 s | — | M | H | Phải thấy mặt nước trước khi làm mờ |
| SH26 | B26 | "Water rises and falls; the city rides up and down." | Triều lên thì sao? | Mực nước | CLM_041, calc (3° với cầu 25 m) | B,D,F | phao trượt theo cọc; khớp cầu | ELEVATION | **NEW** `SINK`/`RISE` (tịnh tiến z) + xoay cầu | Vì sao cầu có khớp | 16 s | dải 2 m *(assumed)* | M | H | Hoạt ảnh tịnh tiến là năng lực mới |
| SH27 | B27 | "Deeper water: lines instead of piles, and the cost climbs." | Xa bờ hơn? | Neo theo độ sâu | CLM_054, 055 | A,D | dây, neo, đáy dốc | Dưới nước, ngang | REPLACE (cọc → dây) | Neo phụ thuộc đáy | 20 s | "conceptual; not sized" | M | H | Độ võng dây chỉ là hình vẽ |
| SH28 | B28 | "And everything depends on the seabed." | — | Đáy biển | CLM_054 | A,D | vùng neo | Cận | CLOSEUP_HIGHLIGHT | — | 10 s | "requires site survey" | L | H | — |
| SH28b | B28 | (chuyển) "Is it a city yet?" | — | — | — | A | quận | Three-quarter | HOLD | — | 8 s | — | L | H | — |

## C6: A City Needs More Than Buildings (6:26–7:36)

| Shot | Beat | Ý lời dẫn | Câu hỏi | Khái niệm | Ev | Fam | Mục tiêu | Camera | Chiến lược | Lộ ra | Dài | Chú thích | Cplx | Conf | Giới hạn |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| SH29 | B29 | "Fade the buildings, and the real city appears." | Thành phố chạy bằng gì? | Mạng hạ tầng | CLM_043 | E,F | điện, nước, nước thải dọc cầu | Three-quarter | SEQUENCE: GHOST nhà, HIGHLIGHT từng mạng theo từ | Hệ thống tích hợp | 22 s | tên mạng | H | H | — |
| SH30 | B30 | "Forty-six homes, one grid connection." | Có phải tự cung tự cấp? | Nối lưới | CLM_016 | K | 46 nhà → 1 cáp | 2D | CARD | "Floating ≠ off-grid" | 14 s | — | L | H | — |
| SH31 | B31 | "Wastewater goes ashore — by pump." | Nước thải đi đâu? | Nước thải | CLM_017, 023 | F | ống xám/đen, bơm, cầu | Cận một phao | CLOSEUP_HIGHLIGHT | Phụ thuộc vào bờ | 16 s | "digester: planned pilot" nếu nhắc | M | H | — |
| SH32 | B32 | "Boats, two ways out, food from land." | Cấp cứu, đi lại? | Dịch vụ | CLM_043, scn | F | bến, lối thoát, cầu | Three-quarter | SEQUENCE: HIGHLIGHT 3 mục | — | 18 s | — | M | H | Không khẳng định đạt quy chuẩn |

## C7: What Would Actually Make This Difficult? (7:36–9:16)

| Shot | Beat | Ý lời dẫn | Câu hỏi | Khái niệm | Ev | Fam | Mục tiêu | Camera | Chiến lược | Lộ ra | Dài | Chú thích | Cplx | Conf | Giới hạn |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| SH33 | B33 | "Now tow it out to sea." | Ra khơi được không? | Phản thực tế | scn | K | bản đồ, quận dời ra | 2D bản đồ | CARD | Bắt đầu D | 12 s | "counterfactual" | L | H | — |
| SH34 | B34 | "Long swells pass a floating breakwater." | Đê còn đủ? | Sóng dài | CLM_051, 052 | K | mặt cắt đê, sóng dài | 2D | CARD | Giới hạn của đê | 14 s | "conceptual" | L | H | — |
| SH35 | B35 | "Longer lines. No bridge. Everything on its own." | Còn gì đổi? | Neo, tự chủ | CLM_054, 043, 058 | K | dây dài, cầu biến mất | 2D | CARD | Chi phí và tự chủ | 16 s | — | L | H | — |
| SH36 | B36 | "Offshore designs use a different kind of hull." | Thiết kế khác ra sao? | Phao bán chìm | CLM_062 | K/B | hộp và cột | 2D sơ đồ | CARD SIDE_BY_SIDE | "A different machine" | 12 s | "concept study (2026)" | L | H | — |
| SH37 | B37 | "Concrete in seawater needs watching." | Bảo trì? | Ăn mòn | CLM_059 | B | mặt thân, vùng kiểm tra | Cận (S2) | CLOSEUP_HIGHLIGHT | Chi phí ẩn | 14 s | "no dedicated standards yet" | L | H | Không vẽ hư hỏng giả |
| SH38 | B38 | "Shade on the seabed." | Sinh thái? | Bóng râm, dòng chảy | CLM_044 | A | bóng phao trên đáy | Dưới nước | HOLD (bóng EEVEE) | Tác động vô hình | 12 s | — | M | M | Chỉ minh họa bóng, không mô phỏng ánh sáng |
| SH39 | B39 | "Who gets to use the water?" | Ai được lợi? | Quản trị, công bằng | CLM_045, 046 | E,F | mép có lối công cộng và mép rào | Three-quarter | SIDE_BY_SIDE 2 biến thể | Câu hỏi phi kỹ thuật | 12 s | — | M | H | — |
| SH40 | B40 | "Not land minus the problems — different problems." | So với đất liền? | So sánh | CLM_041, 061 | K | bảng 2 cột | 2D | CARD | Kết luận cân bằng | 8 s | "no peer-reviewed cost basis" | L | H | — |

## C8: Could We Really Build It? (9:16–10:36)

| Shot | Beat | Ý lời dẫn | Câu hỏi | Khái niệm | Ev | Fam | Mục tiêu | Camera | Chiến lược | Lộ ra | Dài | Chú thích | Cplx | Conf | Giới hạn |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| SH41 | B41 | "From one platform to a city: every part answers a question." | Đi được bao xa? | Tổng hợp | calc, scn | A–F | A cạnh C | DETAIL_THEN_OVERVIEW (A riêng, rồi cả hai) | SIDE_BY_SIDE + nhãn | So sánh cuối | 22 s | mỗi hệ một nhãn | H | H | 40 m cạnh khoảng 600 m: A rất nhỏ, cần khung cận trước |
| SH42 | B42 | "Built. Plausible here. Speculative out there." | Kết luận? | Phán quyết 3 tầng | CLM_010, 011, 033, 042, 053, 051, 058 | K | 3 tầng | 2D | CARD, phần tử theo từ | Câu trả lời | 20 s | — | L | H | Card dài: phần tử phải hiện theo từ |
| SH43 | B43 | "The hardest parts may not be the engineering." | — | Câu kết | — | A–F | quận, ánh chiều | Aerial | HOLD + PUSH_IN | — | 12 s | — | H | H | Dùng lại cảnh SH01 |
| SH44 | B44 | Lời kêu gọi (≤ 60 từ) | — | — | — | K | icon tự vẽ | 2D | CARD | — | 20 s | — | L | H | — |
| SH45 | — | Ghi công, công bố giọng AI | — | — | — | K | — | 2D | CARD | — | 6 s | — | L | H | — |

**Tổng thời lượng:** 636 s (10:36), trong mục tiêu 10–12 phút. Số đếm bằng script từ chính các bảng trên. Chia theo loại shot (chỉ họ K là 2D; shot có cả card và cận cảnh 3D tính là 3D):

| Loại | Số shot | Thời lượng | Tỉ lệ |
|---|---|---|---|
| 3D | 29 | 412 s | 65% |
| 2D | 17 | 224 s | 35% |

## Đoạn tĩnh và chuyển động dư thừa (đã đánh dấu)
- **SH04, SH18, SH24, SH28b** là HOLD ngắn để chuyển chương. Mỗi shot ≤ 10 s. Có thể gộp SH24 vào SH23 và SH28b vào SH29 khi lời dẫn thật đã đo.
- **SH42** (card 20 s): nguy cơ tĩnh. Ba tầng phải hiện theo từ.
- **SH43** dùng lại cảnh SH01 (cùng camera aerial, ánh chiều). Đây là shot aerial thứ hai và là cuối cùng. Phim không có quá hai aerial.
- **Chuyển động sóng chỉ có ở SH19**, không lặp. SH34 là sơ đồ 2D.
- **Chuỗi 2D liền nhau dài nhất** là SH33–SH36 (4 card, ngưỡng QA phim dài là 4). Nếu cần giảm, chuyển SH36 thành 3D (họ B có hai biến thể thân).

## Mỗi hình đẩy câu chuyện thế nào (tóm tắt)
- **C1:** lời hứa (thành phố), ranh giới thật và đề xuất, cam kết dựng lại.
- **C2:** từ "sao lại nổi" qua "nặng ở đâu", "thêm tải thì sao", "sửa", "không lật" tới "nhưng bám theo nước".
- **C3:** nhân bản sinh ra mối nối; đếm ra quy mô; đánh đổi to hay nhiều.
- **C4:** sóng làm lộ mối nối và tiện nghi; lời giải là địa điểm và bố cục; đê có giới hạn.
- **C5:** phần dưới nước lộ ra; mực nước giải thích khớp; độ sâu đổi cách neo.
- **C6:** nhà lùi đi, hệ thống hiện ra; thành phố vẫn buộc vào bờ.
- **C7:** dời ra khơi đổi cả loại kết cấu; ba câu hỏi còn lại ở mọi nơi.
- **C8:** đặt điểm đầu cạnh điểm cuối; trả lời theo ba tầng.
