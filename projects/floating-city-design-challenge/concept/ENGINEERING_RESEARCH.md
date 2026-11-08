# Nghiên cứu kỹ thuật: thành phố nổi (giai đoạn concept)

- **Kịch bản:** `SCN_FLOATCITY_COASTAL_01` (`concept/scenario_contract.json`).
- **Nguồn và claim (c-r1):** 14 nguồn ngoài và 2 nguồn của Studio, 63 claim: 49 từ nguồn ngoài, 9 phép tính (CALCULATED_ESTIMATE), 5 giả định (DESIGN_ASSUMPTION). Mọi trích dẫn khớp nguyên văn với bản tải về (`research/sources.json`, sinh bởi `research/build_sources.py`; URL và SHA256 trong `research/source_snapshots.json`). Không claim nào được duyệt biên tập.
- **Phép tính:** `analysis/design_model.py` → `analysis/results.json`, `analysis/RESULTS.md`. Mọi con số tính ra là CALCULATED_ESTIMATE cho một hộp bê tông lý tưởng trong nước lặng.
- **Phân loại** (brief mục 16): ESTABLISHED_FACT, CALCULATED_ESTIMATE, DESIGN_ASSUMPTION, SPECULATIVE_PROPOSAL, UNVERIFIED. Mỗi mục dưới đây ghi rõ loại.

## 1. Tiền lệ có thật và đề xuất

| Tiền lệ | Trạng thái | Phân loại | Điều phim dùng được |
|---|---|---|---|
| **Schoonschip**, Amsterdam | Đã xây. Nhà xong năm 2020, khu chính thức hoàn thành 2021 (hai nguồn) | ESTABLISHED_FACT (CLM_010–018) | 46 hộ trên 30 lô nước; hơn 100 cư dân. Mỗi nhà trên một phao bê tông cốt thép hai lớp; nhà nặng nhất 340–350 t. Đúc trên bờ, hạ thủy rồi kéo tới lô, vì phao quá to cho ụ khô truyền thống. "Cầu tàu thông minh" chung mang hạ tầng. Một đầu nối lưới điện cho cả 46 hộ, có pin và lưới điện thông minh. Tách nước xám và nước đen. Bơm nhiệt lấy nhiệt từ nước kênh qua ống đặt ở đáy phao. |
| Nhà nổi Hà Lan nói chung (Yale E360, 2021) | Thực tế đang có | ESTABLISHED_FACT (CLM_020–023) | Thường cố định vào bờ, hay tựa vào cọc thép, nối cống và lưới điện trên bờ. Thân bê tông làm đối trọng thay cho tầng hầm. Cư dân thấy nhà rung lắc khi bão hay khi tàu lớn đi qua, rõ nhất ở tầng trên. Cần cáp chống nước và bơm để nối hạ tầng. |
| **OCEANIX Busan** | **Đề xuất** công bố tháng 4/2022 tại LHQ. Không tìm thấy báo cáo chính thức nào là đã khởi công (kiểm 2026-11-08). Mốc 2025 đã qua | SPECULATIVE_PROPOSAL (CLM_030–032); trạng thái UNVERIFIED (CLM_033) | Thiết kế: các phao nối nhau 15,5 acre cho 12.000 người (cư dân và khách), ba khu ở/nghiên cứu/lưu trú, cầu link-span nối bờ, vịnh nhỏ được che chắn. Lời "100% năng lượng vận hành từ mặt trời" chỉ là tuyên bố thiết kế. |
| Ruzzo, Cacurri & Arena 2026 (Commun. Earth Environ.) | Nghiên cứu concept có bình duyệt, ước tính giản lược | SPECULATIVE_PROPOSAL cho thiết kế; ESTABLISHED_FACT cho các nhận định giới hạn (CLM_050–061) | Thành phố vệ tinh 50.000 người: module vuông khoảng 300 m, đê chắn sóng nổi kiểu π neo căng, neo mềm dư thừa cho module bên trong, nhà ở đặt phía trong. Thừa nhận: hydro-elastic là thách thức mở; đê nổi có thể không đủ với sóng dài vùng hở; chi phí neo tăng phi tuyến theo độ sâu; thiếu tiêu chuẩn chuyên biệt; thông tin dự án lớn khan hiếm và mâu thuẫn vì là tài liệu độc quyền. |
| MacAfee et al. 2026 (Nature Commun., Comment) | Chương trình nghiên cứu, 10 câu hỏi | ESTABLISHED_FACT về các câu hỏi mở (CLM_040–048) | Định nghĩa "quy mô lớn" là ≥ 20 ha. Thách thức: phản ứng hydro-elastic, tập trung ứng suất ở mối nối, tải môi trường lớn. Nối cống, cáp điện, đường với bờ hoặc làm hệ độc lập. Sinh thái (bóng râm, dòng chảy, loài ngoại lai, ăn mòn, bám bẩn). Quản trị và luật chưa rõ. Công bằng xã hội (phục vụ người giàu, rào chắn mặt nước công cộng). |
| Aquapolis, Okinawa (Kikutake, 1975–2000) | Lịch sử | ESTABLISHED_FACT, độ tin cậy trung bình (CLM_060) | Chỉ có một câu nhắc trong Ruzzo 2026. Cần nguồn gốc trước khi kể. |

**Kết luận về tiền lệ:**
- Khu nổi khoảng 100 người trong nước kênh được che chắn đã có thật.
- Quy mô 10.000 người mới là đề xuất. Dự án quy mô đó mà chúng tôi kiểm (OCEANIX Busan, trên trang của nhà phát triển và kiến trúc sư, 2026-11-08) không có báo cáo khởi công. Đây **không** phải khảo sát toàn thế giới: ví dụ Maldives Floating City (Ruzzo nêu là dự kiến 2027) chưa được kiểm.
- Phim phải giữ ranh giới này ở mọi câu.

## 2. Nổi (buoyancy)

- **Nguyên lý (ESTABLISHED_FACT, CLM_001):** lực đẩy bằng trọng lượng nước bị chiếm chỗ, F_b = ρ·g·V. Khi nổi cân bằng, F_b bằng tổng trọng lượng: thân phao, nhà, người, thiết bị, nước và hàng dự trữ, tải thay đổi.
- **Hình dạng quyết định (CLM_002):** cùng một cục đất sét chìm, nặn thành thuyền thì nổi; tàu thép cũng vậy. Đây là móc mở rất tốt cho chương 2: một khối bê tông đặc chìm, cùng lượng bê tông làm thành hộp rỗng thì nổi.
- **Chở nặng thì ngập sâu hơn (CLM_003).**
- **Hằng số:**
  - nước biển 1.025 kg/m³ (giá trị thiết kế của tài liệu TU Delft, CLM_004);
  - sách giáo khoa cho 1.030 kg/m³ ở 0 °C (CLM_008); chênh 0,5%, không đổi kết luận nào;
  - nước kênh lấy tròn 1.000 kg/m³ (998 kg/m³ ở 20 °C);
  - bê tông 2.400 kg/m³ (CLM_008).
- **CALCULATED_ESTIMATE (`analysis/RESULTS.md` §1):**
  - mỗi tấn cần chiếm chỗ khoảng 0,98 m³ nước biển hoặc 1,0 m³ nước ngọt;
  - nhà nặng nhất ở Schoonschip (340–350 t) chiếm chỗ 340–350 m³ nước kênh, bằng một khối lập phương cạnh khoảng 7 m. Đây là hình ảnh có thật, quy mô người, cho chương 2.
- **Phao A** (DESIGN_ASSUMPTION: 40 × 40 m, sâu 4 m, sàn và tường 0,25 m, vách ngăn mỗi 10 m dày 0,2 m, nhà 3 tầng phủ 40% mặt sàn) cho ra các CALCULATED_ESTIMATE sau:
  - **Khối lượng:** khoảng 4.850 t, khoảng 3 t/m² mặt sàn. Dải 4.470–5.430 t theo tải tĩnh nhà 0,4–0,9 t/m² sàn.
  - **Mớn nước:** khoảng 2,96 m (2,72–3,31 m).
  - **Mạn khô:** khoảng 1,04 m (1,28–0,69 m).
  - **Bất ngờ đáng kể:** khoảng **55% khối lượng là chính thân phao bê tông**. Phần lớn thứ phao phải đỡ là chính nó.
  - **Độ nhạy:** thêm 100 t thì chìm thêm khoảng 6 cm. Thêm một tầng nhà (khoảng 544 t) thì chìm thêm khoảng 33 cm và trọng tâm lên khoảng 1 m.
  - **Nhánh dùng trong phim (c-r1, một tải tĩnh 0,6 t/m² ở mọi bước, `RESULTS.md` §8):** 3 tầng, mạn khô 1,042 m → thêm tầng thứ tư, 0,710 m → giữ 4 tầng, thân 4,5 m, 1,146 m (thêm 105,6 t, 4,0% bê tông thân phao). Bản c-r0 đã ghép nhầm cặp 0,69 → 1,13 m của trường hợp "3 tầng tải nặng" vào chuỗi "thêm tầng"; đã sửa.
- **Giới hạn:** cân bằng lực nổi **không** có nghĩa là an toàn. Nó không nói gì về ổn định, sóng, va chạm, ngập, mỏi hay bão.

## 3. Ổn định

- **Nguyên lý (ESTABLISHED_FACT):**
  - GM = KB + BM − KG (CLM_005);
  - BM = I_t/∇ cho góc nhỏ, với mặt đường nước chữ nhật I_t = LB³/12 (slide TU Delft 10 và 15, đọc trên PDF);
  - với hộp sà lan, BM = B²/(12T).
  - Khái niệm metacentre chỉ đúng với góc nhỏ. Quá khoảng 10–15° phải dùng đường cong cánh tay đòn phục hồi GZ (CLM_006).
  - Dời một khối nặng w một khoảng d thì vật nghiêng góc θ với tan θ = w·d/(W·GM) (CLM_009).
  - GM lớn làm tàu "cứng" khi lắc ngang, mô-men phục hồi lớn ngay ở góc nhỏ; GM nhỏ thì tàu lắc chậm. GM quá lớn có thể làm tàu ổn định quá mức (CLM_007, CLM_009). **CLM_007 không dùng trong lời dẫn** (xem dưới).
  - Thân bê tông đặt thấp làm đối trọng (CLM_021).
- **CALCULATED_ESTIMATE (§2–3):**
  - Với phao A, BM khoảng 45 m, KG khoảng 4,4 m, GM khoảng 42 m (hộp lý tưởng).
  - Dời 100 t ra cách tâm 15 m thì phao nghiêng chưa tới nửa độ (khoảng 0,42°).
  - BM tăng theo bình phương bề rộng: rộng 10 m cho khoảng 2,8 m, 80 m cho khoảng 180 m.
- **Ý nghĩa cho câu chuyện (sửa ở c-r1):** dưới tải dời chỗ minh họa, phao nghiêng rất ít. Nhưng GM chỉ mô tả mô-men phục hồi ở góc nghiêng nhỏ; nó **không** cho biết phao chuyển động thế nào trong sóng. Lời dẫn chỉ nói: *"a small tilt under a shifted load tells us very little about how it will move in waves."* Bản c-r0 viết "stiff means it follows the water"; câu đó suy quá mức từ GM và đã bỏ.
- **Không được nói:** không có biên an toàn ổn định nào được tính hay được khẳng định. Chưa xét: ổn định góc lớn, ổn định khi hư hỏng theo quy chuẩn, mô-men gió, mặt thoáng chất lỏng trong két (TU Delft có phần "Free surfaces in tanks", chỉ nêu định tính), tải lệch tâm khi xây dựng.
- **Khoang kín nước (CALCULATED_ESTIMATE §2):** vách ngăn chia phao thành 16 ô 10 × 10 m. Một ô ngập (tính giản lược, chỉ chìm đều) làm phao chìm thêm khoảng 0,2 m, mạn khô còn khoảng 0,85 m. Ô lệch tâm còn gây nghiêng; không kiểm theo quy tắc hư hỏng nào. Đây là lý do có vách ngăn, kể định tính.

## 4. Sóng và chuyển động

- **Sáu bậc tự do:** heave, surge, sway, roll, pitch, yaw (slide TU Delft chương 1). Phim chỉ cần heave (nhấp nhô), pitch và roll (chúi và lắc) và chuyển động **tương đối** giữa các phao.
- **Thực tế:**
  - Cư dân Schoonschip thấy chuyển động khi bão, rõ nhất ở tầng ba (CLM_022);
  - phao lớn có phản ứng hydro-elastic phức tạp, nghĩa là phao uốn chứ không chỉ chuyển động như vật cứng (CLM_042, CLM_053);
  - phần mềm tuyến tính phổ biến bỏ qua hoặc giản lược lực phi tuyến như ứng xử mối nối khi chuyển vị lớn (CLM_053).
- **Thiết kế đáp lại (SPECULATIVE_PROPOSAL, CLM_055):** đặt nhà ở bên trong, sau các module chịu được chuyển động lớn hơn.
- **Che chắn:**
  - vị trí lý tưởng là vùng biển có đà gió hạn chế, sóng vừa phải (CLM_050);
  - đê chắn sóng nổi có thể không đủ với sóng dài vùng hở (CLM_051);
  - truyền sóng qua đê nổi là bài toán phức tạp, còn chưa giải hết (CLM_052).
- **Quy tắc hình:** mọi hoạt ảnh sóng là "Conceptual motion visualization — not a hydrodynamic simulation". Không biên độ, không chu kỳ, không cộng hưởng định lượng. Không có nguồn nào cho chu kỳ sóng thiết kế của kịch bản, nên phim không nói con số.

## 5. Mối nối module

- **Bằng chứng:**
  - tập trung ứng suất ở mối nối là thách thức được nêu tên (CLM_042);
  - nghiên cứu concept nối mềm các module và giữ khoảng cách đủ để không va chạm, vì neo mềm cho phép dịch ngang khá lớn; chân vịt dự phòng để tránh va chạm và quá tải mối nối (CLM_056, SPECULATIVE_PROPOSAL; c-r1 sửa việc gán mục đích);
  - chênh mớn nước 0,66 m (CLM_107) là của **hai phao nổi độc lập**. Khi nối cứng, cân bằng của cả hai đổi, nên phép tính không chứng minh mối nối cứng sẽ hỏng; nó chỉ cho thấy tải khác nhau thêm yêu cầu cho mối nối;
  - Schoonschip dùng cầu tàu chung mang hạ tầng (CLM_015).
- **CALCULATED_ESTIMATE (§5, chỉ đếm):** cho khoảng 33 ha mặt phao,
  - phao 40 m: 209 phao, tới khoảng 390 cạnh chung;
  - phao 100 m: 34 phao, khoảng 60 cạnh chung;
  - nhưng mỗi phao 100 m nặng khoảng 30.000 t, so với khoảng 4.900 t của phao 40 m.
  - Phao to: ít mối nối, nhưng khó đúc, hạ thủy và kéo (phao Schoonschip đã quá to cho ụ khô truyền thống, CLM_014) và uốn theo sóng nhiều hơn.
  - **Phao to hay nhiều phao** là một đánh đổi thật, không có đáp án chung.
- **Phim không chọn một kiểu mối nối "đúng".** Hình chỉ là khái niệm: khe hở, cầu đi bộ mềm, đường hạ tầng đi qua khe. Không vẽ chi tiết cơ khí như thể đã được tính.

## 6. Neo và giữ vị trí

- **Bằng chứng:**
  - nhà nổi Hà Lan thường tựa vào cọc thép (CLM_020); kết cấu nổi đi theo mực nước (CLM_041);
  - chi phí neo phụ thuộc chủ yếu vào độ sâu và đáy biển: sâu hơn thì dây dài hơn, neo sâu hơn, chi phí tăng phi tuyến (CLM_054);
  - nghiên cứu concept đề xuất neo mềm dư thừa (dây catenary hoặc dây căng dùng chung) cho module trong, và chân căng cho đê (CLM_055).
- **Kịch bản:**
  - pha A–B: cọc ở nước nông, phao trượt lên xuống theo cọc;
  - pha C: phần xa bờ hơn dùng dây neo, vì độ sâu 12–25 m là DESIGN_ASSUMPTION.
  - Không định cỡ neo, không chọn loại neo như đã tính.
- **CALCULATED_ESTIMATE (§6):** dải mực nước 2 m (giả định) cộng dao động mớn nước khi phao rỗng và đầy (khoảng 0,44 m) cho dốc tối đa của cầu nối bờ khoảng 4,6° với cầu 15 m, 2,8° với cầu 25 m, 1,7° với cầu 40 m. Đây là lý do cầu phải có khớp. Giới hạn tiếp cận cho người khuyết tật không được kiểm.

## 7. Bão, hạ tầng, kinh tế, môi trường

- **Bão:**
  - không chọn chu kỳ lặp hay tốc độ gió;
  - kịch bản đòi giữ an toàn cho người qua bão, có kế hoạch sơ tán hoặc trú tại chỗ;
  - không nói "không hư hỏng gì";
  - đê chắn không xóa hết rủi ro bão (CLM_051).
- **Hạ tầng:**
  - nối hạ tầng với bờ hoặc làm hệ độc lập là thách thức được nêu (CLM_043); cần cáp và bơm đặc biệt (CLM_023);
  - ví dụ thật: một đầu nối lưới điện cho 46 hộ (CLM_016), tách nước thải (CLM_017), bơm nhiệt dùng nước kênh (CLM_018);
  - kịch bản nối bờ (điện, nước sạch, nước thải, lương thực) nên phim **không** nói thành phố tự cung tự cấp;
  - ra khơi **không** tự động đồng nghĩa với tự chủ: cáp, ống và tàu tiếp tế vẫn có thể, nhưng dài và lộ hơn. Tự chủ là một điều kiện **chọn thêm** (Ruzzo chọn nó), kéo theo hệ năng lượng, nước, lương thực riêng;
  - cho một thành phố tự chủ, Ruzzo ước tính khoảng 470 GWh/năm cho 50.000 người, gần một nửa cho sản xuất lương thực tại chỗ (CLM_058). Chỉ là bối cảnh, không kể.
- **Kinh tế:**
  - Ruzzo 2026 đề xuất một khung đánh giá chi phí sơ bộ, chỉ cho phần nổi và năng lượng, và nêu rằng nguồn chi phí duy nhất họ biết là một báo cáo không bình duyệt (CLM_063). Phim nói: *"We do not yet have a reliable cost estimate for this design."* Câu "no peer-reviewed cost basis" của c-r0 quá tuyệt đối và đã bỏ;
  - chi phí neo theo độ sâu (CLM_054); nhân công chiếm 30–60% tổng chi phí ở các kết cấu nổi khác (Ruzzo, phần Methods; chưa vào sổ claim, không dùng trong phim);
  - ăn mòn cốt thép do clorua và chi phí sửa chữa (CLM_059);
  - phim không nêu con số chi phí.
- **Môi trường và xã hội:**
  - tác động sinh thái lớn hơn nhiều so với khu nhỏ (CLM_044);
  - quản trị và luật chưa rõ (CLM_045);
  - nguy cơ phục vụ người giàu và rào chắn mặt nước công cộng (CLM_046).

## 8. Những gì mô hình đơn giản không làm được

Cần phân tích hàng hải chuyên sâu:
- phản ứng động theo sóng (tần số, cộng hưởng, hydro-elastic);
- tải và mỏi mối nối;
- thiết kế neo và cọc theo địa chất;
- ổn định góc lớn và khi hư hỏng theo quy chuẩn;
- tải bão và nước dâng;
- tiện nghi người ở (gia tốc);
- tác động sinh thái;
- chi phí vòng đời.

Mô hình hiện tại không chứng nhận điều nào trong số này. Phim nói rõ điều đó trong chương kết.

## 9. Câu hỏi chưa trả lời (cần làm trước khi viết kịch bản)

1. **Nguồn gốc cho Aquapolis (CLM_060):** cần tìm, hoặc bỏ khỏi phim.
2. **Ảnh Schoonschip có giấy phép kiểm được:** đã tìm trên Commons qua API (2026-11-08). Không có ảnh PD, CC0 hay CC BY nào của Schoonschip. Ảnh khu Buiksloterham và Johan van Hasseltkanaal gần đó đều là CC BY-SA, và không rõ có cho thấy Schoonschip không. Năm ảnh CC0 tìm thấy là quảng trường Paardenbloemplein. Cần chủ kênh quyết (`CONCEPT_REVIEW.md`).
3. **Nguồn kỹ thuật công khai cho ứng xử phao bê tông nhà nổi:** NPR 7250 hoặc hướng dẫn SBR-CURnet không truy cập được (trả phí), nên **không** dẫn.
4. **Một nguồn sơ cấp cho tình trạng OCEANIX Busan:** thông cáo của thành phố Busan không mở được. Phim nói "theo những gì chúng tôi tìm được, tính tới tháng 11/2026".
5. **Bộ dữ liệu sóng thực cho một vịnh ví dụ:** chỉ cần nếu chủ kênh muốn gắn kịch bản với một địa điểm có thật. Hiện tại kịch bản cố ý không gắn địa danh.
