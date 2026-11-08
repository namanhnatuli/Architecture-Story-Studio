# Storyboard sơ bộ (revision c-r1)

Sinh bởi `concept/build_storyboard.py` từ `script/visual_beats.json` (`script/story.py`) và `script/timing.json` (thời lượng đo từ audio). Một shot cho mỗi beat ở giai đoạn đọc kịch bản (SHnn = Bnn). Sửa ở `story.py` hoặc bảng `SHOTS` trong script này, rồi chạy lại; không sửa tay tệp này.

**Cột:**
- **Fam** là họ asset: A môi trường biển, B phao, C mối nối, D neo, E nhà, F hạ tầng, K card 2D.
- **Cplx** là chi phí render (L/M/H); **Conf** là độ tin cậy của nội dung (H/M).
- **Hạng** là hạng khả thi theo brief mục 15.

## C1: Could We Actually Do This?

| Shot | Lời dẫn (rút gọn) | Câu hỏi | Claim | Fam | Camera | Hoạt ảnh | Lộ ra | Chú thích | Dài | Cplx | Conf | Giới hạn | Hạng |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| SH01 | 10,000 people, with homes, schools, a clinic, parks, and streets to walk along. And not one of them is… | Đây là gì? | — | A,B,E,F | Aerial cao, đẩy chậm | HOLD + PUSH_IN | Lời hứa: một thành phố | NOTE 'Illustrative design' | 11 s | H | H | Cảnh lớn; cần instancing | GENERATE_PROCEDURAL |
| SH02 | Could we design a city like this, one that floats, stays where we put it, and keeps working? Let's treat… | Thiết kế được không? | — | A,B,E,F | Aerial, tiếp B01 | HOLD | Bài toán được đặt ra | — | 13 s | H | H | Dùng chung cảnh B01 | REUSE_EXISTING |
| SH03 | Floating neighborhoods are not science fiction. In Amsterdam, a floating neighborhood called Schoonschip… | Đã có ai làm chưa? | 010, 011, 030, 031, 033, 057 | K | 2D | CARD theo từ | Ranh giới đã xây và đề xuất | 'built' / 'proposed 2022' / 'status checked Nov 2026: OCEANIX news page, BIG project page' | 35 s | L | M | Ảnh Schoonschip chờ quyết định giấy phép; tạm dùng sơ đồ | REUSE_EXISTING |
| SH04 | So let's take our city apart, and build it back, one problem at a time. | Thành phố gồm những gì? | — | A–F | Three-quarter, lùi nhẹ | SEQUENCE: FADE_OUT theo nhóm | Thành phố là chồng hệ thống | tên từng hệ khi nó biến mất | 7 s | H | H | — | GENERATE_PROCEDURAL |

## C2: The First Problem: Making Buildings Float

| Shot | Lời dẫn (rút gọn) | Câu hỏi | Claim | Fam | Camera | Hoạt ảnh | Lộ ra | Chú thích | Dài | Cplx | Conf | Giới hạn | Hạng |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| SH05 | Problem one: how does something this heavy float at all? Take a block of concrete. As a solid lump, it… | Bê tông nổi được à? | 002, 008, 101 | A,B | Mặt cắt ngang | SIDE_BY_SIDE; REVEAL | Hình dạng quyết định | 'same volume of concrete' | 21 s | M | H | Không hoạt ảnh 'chìm dần' | GENERATE_PROCEDURAL |
| SH06 | It floats because it pushes water out of the way, and the water it pushes aside weighs as much as the… | Vì sao nổi? | 001, 102 | A,B,E | Mặt cắt chính diện (prototype P1) | HOLD_HIGHLIGHT | Khối nước bị chiếm chỗ | 'displaced water' | 15 s | M | H | Cần tham số mặt cắt | CREATE_SMALL_NEW_CAPABILITY |
| SH07 | Real floating homes work exactly this way. The Schoonschip houses stand on concrete floats. The heaviest… | Ngoài đời thì sao? | 012, 013, 103 | K | 2D | CARD | Cỡ người thật | 'two builders' figures: 340–350 t' | 23 s | L | H | Sơ đồ, chưa có ảnh | REUSE_EXISTING |
| SH08 | Our first platform, in this illustrative design, carries four blocks of three-story homes. Altogether it… | Cái gì nặng nhất? | 104 | B,E | Three-quarter | EXPLODE + thanh 2D | Bất ngờ: thân phao hơn nửa | 'illustrative' | 21 s | M | H | — | GENERATE_PROCEDURAL |
| SH09 | Now add a fourth story. The platform settles about a third of a meter deeper, and the freeboard, the part… | Thêm tải thì sao? | 003, 105 | B,E | Cận thước mớn nước (P2b, P6) | REPLACE + SINK (mới) | Tải làm phao chìm | thước 1 m; mạn khô 1,04 → 0,71 m | 16 s | M | H | 33 cm không thấy ở khung rộng (P2) | CREATE_SMALL_NEW_CAPABILITY |
| SH10 | One fix is to make the hull half a meter deeper. That adds about 100 tons of concrete, 4% more, and brings… | Sửa thế nào? | 105 | B | Cùng camera B09 | REVEAL phần thân thêm + RISE (mới) | Lần sửa có lý do | mạn khô 0,71 → 1,15 m; '+4% concrete' | 19 s | M | H | Cùng nhánh với B09 (một tải) | CREATE_SMALL_NEW_CAPABILITY |
| SH11 | Will it tip over? Move 100 tons out toward the edge, and in this example the platform tilts by less than… | Có lật không? | 009, 106 | B | Ngang, three-quarter thấp | HOLD + nghiêng nhỏ (TILT, mới) | Nghiêng ít ≠ đứng yên trong sóng | 'illustrative' | 22 s | L | H | Không ký hiệu G, B, M | CREATE_SMALL_NEW_CAPABILITY |

## C3: Why One Platform Isn't a City

| Shot | Lời dẫn (rút gọn) | Câu hỏi | Claim | Fam | Camera | Hoạt ảnh | Lộ ra | Chú thích | Dài | Cplx | Conf | Giới hạn | Hạng |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| SH12 | A platform like this holds about fifty people. For 10,000, we need a lot of them. So why not simply join… | Nhân bản được không? | 108 | B,E | Three-quarter | ASSEMBLE_IN | Khu hình thành | — | 13 s | M | H | — | GENERATE_PROCEDURAL |
| SH13 | Look at two identical platforms carrying different buildings, one with two stories and one with four.… | Sao không nối cứng? | 107 | B,C,E | Mặt đứng | HIGHLIGHT_REPLACE_HIGHLIGHT | Chênh cao độ → cầu có khớp (một lựa chọn) | 'floating independently' | 31 s | M | H | Không tô đỏ, không vẽ gãy | GENERATE_PROCEDURAL |
| SH14 | Connections are where engineers expect trouble. A 2026 research agenda lists stress concentrations on… | Mối nối trông ra sao? | 042, 056 | C,F | Cận | CLOSEUP_HIGHLIGHT | Khe, cầu có khớp, đường hạ tầng mềm | 'conceptual geometry' | 27 s | M | H | Không chọn cơ cấu cụ thể | GENERATE_PROCEDURAL |
| SH15 | How many platforms would 10,000 people need? Say each resident needs about 40 square meters of floor:… | Bao nhiêu phao? | 124, 108 | K | 2D mặt bằng | CARD, chấm hiện dần | Quy mô mối nối | 'illustrative'; 40 m² = 30 + 10 | 25 s | L | H | — | REUSE_EXISTING |
| SH16 | Bigger platforms mean fewer connections. At 100 meters on a side, 34 would do, but each would weigh about… | To hay nhiều? | 108, 014, 125 | K | 2D mặt bằng cùng tỉ lệ | CARD | Đánh đổi; chọn 60 m | khối lượng mỗi phao; 'not an optimum' | 32 s | L | H | — | REUSE_EXISTING |

## C4: The Water Never Stays Still

| Shot | Lời dẫn (rút gọn) | Câu hỏi | Claim | Fam | Camera | Hoạt ảnh | Lộ ra | Chú thích | Dài | Cplx | Conf | Giới hạn | Hạng |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| SH17 | And all of this sits on water that never keeps still. Each platform rises and falls on its own, and every… | Sóng thì sao? | — | A,B,C | Three-quarter thấp | CONCEPT_MOTION (mới) | Khe co giãn | 'Conceptual motion visualization — not a hydrodynamic simulation' | 12 s | M | M | Biên độ không mang nghĩa | CREATE_SMALL_NEW_CAPABILITY |
| SH18 | People living on the water feel it. Floating homes in the Netherlands can rock in storms, or when large… | Người ở có thấy? | 022 | K,E | 2D + cận nhà | CARD | Chuyển động là chuyện con người | nguồn: Yale E360, 2021 | 16 s | L | H | — | REUSE_EXISTING |
| SH19 | Very large platforms don't only move. They bend, and predicting exactly how is still an open research problem. | Phao lớn thì sao? | 053 | K | 2D mặt cắt | CARD, đường cong vẽ dần | Bài toán mở | 'exaggerated, conceptual' | 10 s | L | M | Không có số | REUSE_EXISTING |
| SH20 | So the first fix is where you build. A 2026 concept study looks for sea areas with limited fetch, near a… | Giảm sóng thế nào? | 050, 121 | K | 2D bản đồ sơ đồ | CARD | Địa điểm là thiết kế | 'limited fetch' | 22 s | L | H | Không gắn địa danh thật | REUSE_EXISTING |
| SH21 | The second fix is the layout. Following one concept study, homes go in the middle, and functions that can… | Bố cục ra sao? | 055, 051, 052 | A–F | Top → three-quarter | SEQUENCE | Tổ chức theo chuyển động | 'reduces waves — does not remove storm risk' | 29 s | H | H | — | GENERATE_PROCEDURAL |

## C5: Keeping the City in Place

| Shot | Lời dẫn (rút gọn) | Câu hỏi | Claim | Fam | Camera | Hoạt ảnh | Lộ ra | Chú thích | Dài | Cplx | Conf | Giới hạn | Hạng |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| SH22 | Something also has to hold the city in place. Floating homes in the Netherlands are fixed to the shore,… | Cái gì giữ nó? | 020 | A,D | Three-quarter thấp (P4) | SEQUENCE: nước 2 bước, HIGHLIGHT cọc | Hệ neo vô hình | — | 11 s | H | H | Phải thấy mặt nước trước khi mờ | ADAPT_EXISTING |
| SH23 | Water levels rise and fall, and a floating platform rises and falls with them, sliding along its poles. In… | Triều lên thì sao? | 041, 122, 109 | B,D,F | Mặt đứng | SEQUENCE + RISE/SINK (mới) | Vì sao cầu có khớp | '2 m range, assumed' | 23 s | M | H | — | CREATE_SMALL_NEW_CAPABILITY |
| SH24 | Further out, the water is deeper, and piles give way to mooring lines anchored in the seabed. Deeper water… | Xa bờ hơn? | 055, 054 | A,D | Dưới nước, ngang | REPLACE (cọc → dây) | Neo theo độ sâu | 'Conceptual mooring — not sized' | 17 s | H | H | Độ võng dây chỉ là hình vẽ; tương phản dây (P5) | GENERATE_PROCEDURAL |

## C6: A City Needs More Than Buildings

| Shot | Lời dẫn (rút gọn) | Câu hỏi | Claim | Fam | Camera | Hoạt ảnh | Lộ ra | Chú thích | Dài | Cplx | Conf | Giới hạn | Hạng |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| SH25 | So it floats, and it stays put. But is it a city yet? Fade out the buildings, and the city's other half… | Đã là thành phố chưa? | — | E,F | Three-quarter | SEQUENCE: GHOST nhà | Nửa còn lại của thành phố | — | 10 s | H | H | — | GENERATE_PROCEDURAL |
| SH26 | Power first: at Schoonschip, 46 households share a single connection to the national grid, with solar… | Tự cung tự cấp? | 016 | K | 2D | CARD | 'Floating ≠ off-grid' | — | 17 s | L | H | — | REUSE_EXISTING |
| SH27 | Wastewater is separated there too: gray water from showers and washing machines, black water from toilets.… | Nước thải đi đâu? | 017, 023, 123 | F | Cận một phao | CLOSEUP_HIGHLIGHT | Phụ thuộc vào bờ | — | 25 s | M | H | — | GENERATE_PROCEDURAL |
| SH28 | Transport, fire and medical services, and food all follow the same logic. A large floating development has… | Cấp cứu, đi lại? | 043 | F | Three-quarter | SEQUENCE: HIGHLIGHT 3 mục | Mọi dịch vụ nối bờ | — | 18 s | H | H | Không khẳng định đạt quy chuẩn | GENERATE_PROCEDURAL |

## C7: What Would Actually Make This Difficult?

| Shot | Lời dẫn (rút gọn) | Câu hỏi | Claim | Fam | Camera | Hoạt ảnh | Lộ ra | Chú thích | Dài | Cplx | Conf | Giới hạn | Hạng |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| SH29 | Everything so far assumed sheltered water close to a city. So what happens if we tow it out to sea? | Ra khơi được không? | — | A,B | 3D biển mở, aerial thấp | HOLD | Bắt đầu phản thực tế | 'Counterfactual' | 9 s | M | H | Site biển mở mới | GENERATE_PROCEDURAL |
| SH30 | Longer waves arrive, and a floating breakwater may not be enough against them. Below the surface, the… | Đê và neo còn đủ? | 051, 054 | A,D | Cùng cảnh, xuống dưới nước | SEQUENCE + CONCEPT_MOTION (sóng dài) | Sóng dài; dây dài ra | nhãn chuyển động khái niệm | 14 s | H | H | — | CREATE_SMALL_NEW_CAPABILITY |
| SH31 | Further from shore, cables, pipes and supply ships can still reach the city, but every link becomes longer… | Còn nối bờ được? | 043, 051 | F | Cùng cảnh | HOLD_HIGHLIGHT | Liên kết dài và lộ hơn | — | 11 s | M | H | — | GENERATE_PROCEDURAL |
| SH32 | And if we also asked the city to supply itself, as one 2026 offshore concept does, it would need its own… | Nếu phải tự chủ? | 058 | K | 2D | CARD | Một điều kiện thêm, không mặc định | 'one concept study's estimate' | 21 s | L | H | — | REUSE_EXISTING |
| SH33 | That study also uses a different kind of hull: semi-submersible platforms, with the deck raised above the… | Thiết kế khác ra sao? | 062 | B | 3D cạnh nhau | SIDE_BY_SIDE | Một loại thân khác | 'concept study (2026)' | 19 s | M | H | Biến thể phao bán chìm (sơ đồ) | GENERATE_PROCEDURAL |
| SH34 | Some difficulties remain wherever we build. Concrete in seawater needs watching: chlorides can corrode the… | Bảo trì? | 059 | B | Cận thân phao | CLOSEUP_HIGHLIGHT | Chi phí ẩn | 'no dedicated standards yet' | 19 s | L | H | Không vẽ hư hỏng | GENERATE_PROCEDURAL |
| SH35 | Large floating developments change the light, shade and water movement beneath them, effects that… | Sinh thái? | 044 | A | Dưới nước | HOLD (bóng EEVEE) | Tác động vô hình | — | 17 s | M | M | Không mô phỏng ánh sáng | ADAPT_EXISTING |
| SH36 | And who gets to use the water? How districts like this fit into planning law is not yet known, and… | Ai dùng mặt nước? | 045, 046 | E,F | Three-quarter | SIDE_BY_SIDE 2 biến thể | Câu hỏi phi kỹ thuật | — | 16 s | M | H | — | GENERATE_PROCEDURAL |
| SH37 | And what would it cost? We do not yet have a reliable cost estimate for this design. The one published… | Bao nhiêu tiền? | 063, 041, 054, 042, 059 | K | 2D | CARD 2 cột | Kết luận cân bằng | 'no reliable cost estimate for this design' | 28 s | L | H | — | REUSE_EXISTING |

## C8: Could We Really Build It?

| Shot | Lời dẫn (rút gọn) | Câu hỏi | Claim | Fam | Camera | Hoạt ảnh | Lộ ra | Chú thích | Dài | Cplx | Conf | Giới hạn | Hạng |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| SH38 | From one platform to a district, every part we added answers a question we had to ask. | Đi được bao xa? | — | A–F | DETAIL_THEN_OVERVIEW | SIDE_BY_SIDE + nhãn | So sánh cuối | mỗi hệ một nhãn | 8 s | H | H | Phao 40 m cạnh quận khoảng 600 m: cần khung cận trước | GENERATE_PROCEDURAL |
| SH39 | So, could we build an entire city that floats? Small floating neighborhoods, connected to the shore in… | Kết luận 1? | 010, 011, 016 | K | 2D | CARD theo từ | Đã có thật | — | 11 s | L | H | — | REUSE_EXISTING |
| SH40 | A connected district for 10,000 people, in a sheltered bay, built step by step, may be possible under the… | Kết luận 2? | 121, 053, 042, 063, 033 | K | 2D | CARD theo từ | Có thể, có điều kiện | 'checked: OCEANIX Busan, Nov 2026' | 30 s | L | H | — | REUSE_EXISTING |
| SH41 | A city far out at sea, especially one that has to supply itself, remains much more speculative. | Kết luận 3? | 051, 058, 062 | K | 2D | CARD theo từ | Còn suy đoán | — | 9 s | L | H | — | REUSE_EXISTING |
| SH42 | Our arithmetic shows what it takes for a platform to float. Whether a whole district works depends on the… | Phép tính chứng minh gì? | 104, 121 | A–F | Aerial (dùng lại B01) | HOLD + PUSH_IN | Giới hạn của phép tính | — | 12 s | H | H | Dùng lại cảnh B01 | REUSE_EXISTING |
| SH43 | Which structure should we explain next? Suggest a topic in the comments. And if you enjoyed this film,… | — | — | K | 2D | CARD icon tự vẽ | Lời kêu gọi | — | 12 s | L | H | — | REUSE_EXISTING |
| SH44 | Thank you for watching. The sources are listed in the description. | — | — | K | 2D | CARD | Ghi công, công bố giọng AI | — | 7 s | L | H | — | REUSE_EXISTING |

## Tổng

- **Thời lượng:** 13:05 (đo từ audio, gồm khoảng lặng đầu và cuối mỗi beat).
- **3D:** 502 s (64%); **2D:** 282 s (36%).
- **Theo hạng khả thi:** ADAPT_EXISTING 2; CREATE_SMALL_NEW_CAPABILITY 7; GENERATE_PROCEDURAL 18; REUSE_EXISTING 17.
- **Chuỗi card 2D liền nhau dài nhất:** 3 (B39–B41).
- **Aerial:** chỉ B01–B02 và B42 (dùng lại cùng cảnh).

