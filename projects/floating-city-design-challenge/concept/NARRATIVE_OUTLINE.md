# Dàn ý kể chuyện (revision c-r2; c-r1 sau review concept, c-r2 sau review c-r1, 2026-11-08)

- **Lời dẫn đầy đủ** ở `script/story.py`, sinh ra `script/narration.json`. Dàn ý này nói vì sao từng chương có mặt và mỗi ý dựa vào đâu:
  - claim trong `research/sources.json`;
  - phép tính trong `analysis/results.json` (*calc*);
  - giả định trong `concept/scenario_contract.json` (*scn*).
- **Thời lượng:** đo từ audio thật sau `lock-audio` (`review/SCRIPT_REVIEW.md`), không còn là ước lượng của storyboard.
- **Nhịp:** *"We solved that — now there's another problem."* Mỗi vòng mang một hình mới.

## Sửa so với c-r0 (theo review concept của chủ kênh, 2026-11-08)

| # | Vấn đề | Đã sửa |
|---|---|---|
| 1 | "Stiff means it follows the water" suy quá từ GM | Bỏ. Nay là: phao nghiêng rất ít **dưới tải dời chỗ minh họa này**, nhưng điều đó nói rất ít về cách nó chuyển động trong sóng. CLM_007 không dùng trong lời dẫn. |
| 2 | 66 cm chênh mớn nước bị dùng để nói "cầu cứng sẽ gãy" | 66 cm là của **hai phao nổi độc lập**. Lời dẫn: tải khác nhau thêm một yêu cầu cho mối nối; thiết kế này chọn cầu có khớp; dằn là một cách khác. Hình không tô đỏ phương án nào. |
| 3 | Ra khơi bị đánh đồng với tự cung tự cấp | Tách hai câu hỏi: (a) xa bờ làm kết nối, bảo trì và tiếp tế khó hơn (cáp, ống, tàu vẫn có thể); (b) **nếu chọn thêm** điều kiện tự chủ thì cần thêm hệ nào. |
| 4 | SH09–SH10 đổi trường hợp giữa chừng | Một nhánh liên tục, tải tĩnh nhà 0,6 t/m² ở mọi bước: 3 tầng (mạn khô 1,04 m) → 4 tầng (0,71 m) → thân 4,5 m (1,15 m), thêm 106 t bê tông (4%). Quận dùng **một** cỡ phao: 60 m (93 phao). |
| 5 | "No peer-reviewed cost basis" quá tuyệt đối; CLM_033 bị mở rộng thành kết luận toàn cầu | Lời dẫn: *"We do not yet have a reliable cost estimate for this design"* (CLM_063). Kết luận về quy mô chỉ nói về dự án đã kiểm (OCEANIX Busan), nêu nơi kiểm và ngày kiểm, và nói rõ không khảo sát toàn thế giới. |
| 6 | Số minh họa bị đọc như thành phố vận hành được | 40 m² sàn mỗi người = 30 nhà ở + 10 trường học, phòng khám, cửa hàng, dịch vụ (giả định). Tổng khoảng 1 triệu tấn chỉ là các phao tiêu chuẩn (không gồm đê, cầu, phao dịch vụ, neo, hạ tầng). Độ dày thân phao chỉ là giả định để tính khối lượng. Câu kết: phép tính cho thấy yêu cầu nổi cơ bản; quận có khả thi hay không còn phụ thuộc địa điểm và thiết kế của mọi hệ khác. |
| — | Mở phim "Not a render" | Thay bằng lời mời giải một bài toán thiết kế. |
| — | C2 quá dày | Còn ba ý: nổi bằng cách nào → thêm tải thì sao → nổi được chưa đủ. Không có ký hiệu G, B, M. |
| — | C7 có bốn card liền nhau | So sánh thân hộp với thân bán chìm thành 3D; thay đổi của hệ neo kể bằng cảnh dưới nước 3D. |
| — | Thêm ảnh thật Schoonschip | Commons chỉ có ảnh CC BY-SA quanh khu vực (Studio chưa dùng ShareAlike), không có ảnh CC0, CC BY hay PD của Schoonschip. **Cần chủ kênh quyết** (`CONCEPT_REVIEW.md`). Tới lúc đó dùng sơ đồ tự vẽ có nhãn "Schoonschip, Amsterdam (schematic)". |

## Chương

| Chương | Tiêu đề | Thiết kế trên màn hình |
|---|---|---|
| C1 | Could We Actually Do This? | Quận C hoàn chỉnh → gỡ về một phao |
| C2 | The First Problem: Making Buildings Float | A (3 tầng → 4 tầng → thân sâu hơn) |
| C3 | Why One Platform Isn't a City | B, rồi chọn cỡ phao cho quận |
| C4 | The Water Never Stays Still | B dưới chuyển động khái niệm → bố cục C |
| C5 | Keeping the City in Place | C, nước mờ dần, cọc và dây neo |
| C6 | A City Needs More Than Buildings | C, nhà mờ dần, mạng hạ tầng |
| C7 | What Would Actually Make This Difficult? | D (ngoài khơi, 3D) + bảo trì, sinh thái, quản trị, chi phí |
| C8 | Could We Really Build It? | A cạnh C; phán quyết; lời kêu gọi |

## C1: Could We Actually Do This?
- **Móc mở:** quận nổi hoàn chỉnh (nhãn *Illustrative design*). Mười nghìn người, nhà, trường, phòng khám, công viên, không ai đứng trên đất liền.
- **Lời mời:** *"Could we design a city like this — one that floats, stays put and keeps working? Let's treat it as a design problem, and solve it one step at a time."*
- **Mốc có thật:**
  - một khu nổi khoảng 100 người đã có ở Amsterdam (CLM_010, CLM_011);
  - một đề xuất 12.000 người ở Busan, công bố năm 2022 (CLM_030, CLM_031). Trang của kiến trúc sư vẫn ghi "In Design" khi kiểm vào tháng 11/2026 (CLM_034, c-r2). Phạm vi kiểm tra để ở ghi chú, không đọc thành tiếng.
- **Gỡ thành phố** về một phao trống.

## C2: The First Problem: Making Buildings Float (ba ý)
1. **Nổi bằng cách nào.**
   - Cùng một lượng bê tông: đúc đặc thì chìm, làm hộp rỗng thì nổi (CLM_002; calc: 1.108 m³, khối 10,35 m, hộp nổi với mớn nước 1,62 m).
   - Archimedes trên mặt cắt (CLM_001).
   - Mốc thật: nhà nặng 340–350 t trên phao bê tông chiếm chỗ khoảng 340 m³ nước kênh (CLM_012, CLM_013, calc).
   - Phao của chúng ta (*illustrative*): khoảng 4.850 t, ngồi sâu khoảng 3 m; hơn nửa là chính thân phao (calc).
2. **Thêm tải thì sao.**
   - Thêm tầng thứ tư: phao chìm thêm khoảng 33 cm, mạn khô từ khoảng 1,04 m xuống khoảng 0,71 m (CLM_003, calc).
   - Sửa: thân sâu thêm nửa mét, tốn khoảng 106 t bê tông (4%); mạn khô về khoảng 1,15 m.
   - Lựa chọn khác hợp lý: nhà nhẹ hơn.
3. **Nổi được chưa đủ.**
   - Dời 100 t ra gần mép, phao nghiêng chưa tới nửa độ trong trường hợp minh họa này (CLM_009, calc; góc nhỏ, CLM_006).
   - *"But a small tilt under a shifted load tells us little about how it will move in waves."*

## C3: Why One Platform Isn't a City
- **Quay về bản 3 tầng** (c-r2): số người (khoảng 50 mỗi phao 40 m) và cả quận đều dùng nhà 3 tầng, không phải bản 4 tầng của nhánh sửa ở C2.
- **Năm phao.** Sao không hàn thành một tấm?
- **Tải khác nhau.** Hai phao giống nhau, nhà 2 tầng và 4 tầng: nếu nổi độc lập, mặt sàn lệch khoảng 66 cm (calc). Tải khác nhau thêm một yêu cầu cho mối nối.
  - Thiết kế này chọn cầu đi bộ có khớp để chấp nhận chênh cao độ; dằn để cân mớn nước là cách khác.
  - Mối nối là chỗ tập trung ứng suất được nghiên cứu nêu tên (CLM_042). Nghiên cứu nối mềm và giữ khoảng cách giữa các module (CLM_056).
- **Đếm.**
  - Với 40 m² sàn mỗi người (nhà ở cộng phần dịch vụ), 10.000 người cần khoảng 33 ha mặt phao: khoảng 209 phao 40 m, hoặc 93 phao 60 m, hoặc 34 phao 100 m (calc).
  - Phao to: ít mối nối, nhưng nặng khi đúc, hạ thủy và kéo; ngay phao Schoonschip đã quá to cho ụ khô truyền thống (CLM_014).
  - **Quận của chúng ta dùng phao 60 m với nhà 3 tầng:** một lựa chọn ở giữa cho bản minh họa, không phải tối ưu.
  - B15–B16 là một sơ đồ liên tục (c-r2), không phải hai bảng số.

## C4: The Water Never Stays Still
- **Chuyển động khái niệm** (nhãn bắt buộc): các phao nhấp nhô lệch pha; khe và cầu có khớp làm việc.
- **Người ở cảm nhận:** ngay trong kênh Amsterdam, cư dân thấy nhà rung khi bão và khi tàu lớn qua, rõ nhất ở tầng trên (CLM_022).
- **Phao lớn còn uốn:** hydro-elastic là thách thức nghiên cứu còn mở (CLM_053).
- **Lời giải thứ nhất là địa điểm:** vùng nước kín, đà gió ngắn (CLM_050).
- **Lời giải thứ hai là bố cục:**
  - nhà ở vòng trong, chức năng chịu được chuyển động lớn hơn ở vòng ngoài (CLM_055);
  - đê chắn ở phía hở, có giới hạn (CLM_051, CLM_052).

## C5: Keeping the City in Place
- Mặt nước mờ dần (hai bước), lộ cọc rồi dây neo.
- Mực nước lên xuống (2 m, giả định): phao trượt theo cọc (CLM_020, CLM_041). Cầu nối bờ có khớp: tính cả thay đổi tải, dốc khoảng 3° (±2,8°) với cầu 25 m; chỉ tính mực nước thì khoảng 2,3°; khớp ở giữa dải (CLM_109, c-r2).
- Nước sâu hơn: dây neo dùng chung thay cọc (CLM_055); dây dài hơn, neo sâu hơn, chi phí tăng nhanh hơn độ sâu (CLM_054).
- Đáy biển quyết định (CLM_054). Không có loại hay cỡ neo.

## C6: A City Needs More Than Buildings
- Nhà mờ dần, lộ mạng hạ tầng.
- **Điện:** 46 hộ, một đầu nối lưới; pin, lưới điện thông minh (CLM_016). *"Floating doesn't mean off-grid."*
- **Nước thải:** tách nước xám và nước đen, bơm về bờ (CLM_017, CLM_023). Digester nổi chỉ là kế hoạch.
- **Một dòng cho phần còn lại:** nước sạch, giao thông, cứu hỏa và cấp cứu (hai lối ra, bến tàu), lương thực từ đất liền (CLM_043, scn).

## C7: What Would Actually Make This Difficult?
- **Kéo quận ra khơi** (3D, mô hình nhỏ trên biển mở).
  - Sóng dài qua đê nổi (CLM_051).
  - Dưới nước, cùng cảnh: đáy sâu dần, dây neo dài ra (CLM_054).
- **(a) Xa bờ:** kết nối, bảo trì và tiếp tế khó hơn. Cáp, ống và tàu vẫn có thể, nhưng dài hơn và lộ hơn (CLM_043).
- **(b) Nếu chọn thêm điều kiện tự chủ**, như nghiên cứu ngoài khơi năm 2026 đã chọn: phải thêm năng lượng, nước, lương thực. Trong nghiên cứu đó, sản xuất lương thực chiếm gần nửa năng lượng (CLM_058).
- **Thân phao khác** (3D, đặt cạnh nhau): nghiên cứu ngoài khơi dùng phao bán chìm trên cột, sau một đê nổi (CLM_062). *"Offshore isn't the same city moved further out."*
- **Ba khó khăn ở mọi nơi:**
  - bảo trì: ăn mòn cốt thép do clorua; chưa có tiêu chuẩn chuyên (CLM_059);
  - sinh thái: bóng râm, dòng chảy, loài ngoại lai, bám bẩn (CLM_044);
  - ai sở hữu mặt nước (CLM_045, CLM_046).
- **Chi phí:** *"We do not yet have a reliable cost estimate for this design."* Khung chi phí công bố mới là sơ bộ, chỉ cho phần nổi và năng lượng (CLM_063).
- **So với đất liền:** kết cấu nổi theo kịp mực nước và có thể dời đi (CLM_041), đổi lại phải có neo, mối nối và bảo trì liên tục.

## C8: Could We Really Build It?
- **So sánh cuối:** phao A cạnh quận C. Mỗi hệ một nhãn và câu hỏi nó trả lời.
- **Phán quyết ba tầng:**
  1. **Đã có thật:** khu nổi khoảng 100 người, nối bờ, trong nước kín (CLM_010, CLM_011, CLM_016).
  2. **Có thể trong điều kiện cụ thể:** một quận nối bờ trong vịnh kín, xây theo pha. Mỗi hệ có tiền lệ hoặc nghiên cứu, nhưng hydro-elastic, mối nối và chi phí còn mở (CLM_042, CLM_053, CLM_063). Dự án quy mô này mà chúng tôi kiểm (OCEANIX Busan) vẫn được kiến trúc sư ghi "In Design" (CLM_034, tháng 11/2026).
  3. **Còn suy đoán:** một thành phố ngoài khơi, nhất là nếu phải tự chủ (CLM_051, CLM_058).
- **Câu kết:** *"Our arithmetic shows what it takes for a platform to float. Whether a whole district works depends on the site, and on every other system we've added."*
- **Lời kêu gọi** (beat `framing`, ≤ 60 từ, không claim) và card ghi công.

## Rà soát biên tập (brief mục 17, cập nhật c-r1)

**1. Câu hỏi trung tâm có hấp dẫn ngay không?**
Có. Hình thành phố cùng lời mời giải bài toán.

**2. Luật chơi có dễ hiểu không?**
Có. Một phao, một quy tắc.

**3. Mỗi vấn đề có dẫn logic sang vấn đề sau không?**
Có: nổi → thêm tải → nổi chưa đủ → nhân lên → sóng → giữ vị trí → hoạt động như thành phố → dời ra khơi → phi kỹ thuật.

**4. Mỗi lần sửa có lý do rõ không?**
Có. Nhánh thêm tầng nay liên tục, cùng một tải ở mọi bước.

**5. Giải thích có dễ tiếp cận không?**
Có. Không còn ký hiệu G, B, M; độ nghiêng kể bằng hình.

**6. Có tránh được vòng lặp nhàm không?**
Có. Mỗi chương đổi kiểu hình:
- C3 là đếm;
- C4 là chuyển động khái niệm và hai vịnh;
- C5 là lộ dưới nước;
- C6 là làm mờ nhà;
- C7 là cảnh biển mở 3D.

**7. Thành phố có tinh vi dần lên không?**
Có.

**8. Có bất ngờ thật không?**
Có ba:
- hơn nửa khối lượng là thân phao;
- nửa mét thân phao lấy lại mạn khô với 4% bê tông;
- ngoài khơi cần một loại thân phao khác.

**9. Kết luận có trả lời câu hỏi không?**
Có, theo ba tầng, và nói rõ phép tính chứng minh được gì và không chứng minh được gì.

**10. Người xem có hiểu hơn không?**
Có. Họ hiểu vì sao từng bộ phận tồn tại.

**Chương yếu nhất:** C7, dù đã sửa. Nếu lời dẫn đo được dài quá 110 giây, cắt phần so với đất liền xuống một câu.
