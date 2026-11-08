# Dàn ý kể chuyện (khoảng 10:36 theo storyboard)

**Ghi chú chung:**
- **Lời dẫn:** các câu tiếng Anh dưới đây là *ý lời dẫn*, chưa phải kịch bản. Kịch bản sẽ viết trong `script/story.py` sau khi chủ kênh duyệt concept.
- **Mã claim:** mỗi ý có mã claim (`research/sources.json`), phép tính (`analysis/results.json`) hoặc giả định của kịch bản (`concept/scenario_contract.json`).
- **Nhịp lặp lại:** *"We solved that — but now there's another problem."* Mỗi vòng lặp phải mang một hình mới, không chỉ một câu mới (xem phần rà soát biên tập ở cuối).

| Chương | Tiêu đề | Thời lượng | Thiết kế trên màn hình |
|---|---|---|---|
| C1 | Could We Actually Do This? | 0:00–0:50 | Quận C hoàn chỉnh → gỡ về một phao |
| C2 | The First Problem: Making Buildings Float | 0:50–2:30 | A, A′ |
| C3 | Why One Platform Isn't a City | 2:30–3:52 | B |
| C4 | The Water Never Stays Still | 3:52–5:16 | B dưới sóng khái niệm → C (bố cục trong/ngoài) |
| C5 | Keeping the City in Place | 5:16–6:26 | C, nước làm mờ, cọc và dây neo |
| C6 | A City Needs More Than Buildings | 6:26–7:36 | C, nhà làm mờ, mạng hạ tầng |
| C7 | What Would Actually Make This Difficult? | 7:36–9:16 | D (ngoài khơi) + bảo trì, sinh thái, quản trị |
| C8 | Could We Really Build It? | 9:16–10:36 | A cạnh C; phán quyết; lời kêu gọi |

## C1: Could We Actually Do This? (khoảng 50 giây)
- **Móc mở:** quận nổi hoàn chỉnh trong một vịnh, nhìn từ trên cao. *"Ten thousand people. Homes, schools, a clinic, parks. And not one of them standing on land."*
- **Câu hỏi:** *"Could we actually build a city like this? Not a render — a city that floats, stays put, and keeps working."* Câu này đặt ranh giới với các tầm nhìn không gắn địa điểm (CLM_047).
- **Lời hứa bằng hình:** thành phố được gỡ từng lớp (đê, neo, hạ tầng, nhà, phao) cho tới khi còn **một phao trống**. *"To find out, we'll take it apart, and build it back one problem at a time."*
- **Mốc có thật:** một dòng ngắn trên hình: một khu nổi khoảng 100 người đã có ở Amsterdam (CLM_010, CLM_011); đề xuất 12.000 người ở Busan **chưa được báo cáo là đã xây** (CLM_031, CLM_033).
- **Chuyển:** *"Problem one: how does something this heavy float at all?"*

## C2: The First Problem: Making Buildings Float (khoảng 100 giây)
- **Clay boat:** khối bê tông đặc chìm; cùng lượng bê tông làm thành hộp rỗng thì nổi (CLM_002). *"Shape, not material, decides."*
- **Archimedes:** cắt ngang dưới mực nước. Mảng vàng là khối nước bị chiếm chỗ (CLM_001). Mỗi tấn đòi khoảng một mét khối nước.
- **Mốc có thật:** nhà nặng nhất ở Schoonschip, 340–350 t, đứng trên phao bê tông (CLM_012, CLM_013). Nó chiếm chỗ khoảng 340 m³ nước kênh, *"a cube of water about seven metres on each side"* (tính).
- **Phao của chúng ta** (*illustrative*): khoảng 4.850 t, ngồi sâu khoảng 3 m. **Bất ngờ:** hơn một nửa là chính thân phao. *"Most of what this platform carries… is itself."*
- **Tải tăng:** thêm một tầng, phao chìm thêm khoảng một gang tay (khoảng 33 cm, tính). Mạn khô của phương án nhà nặng mỏng đi.
- **Sửa A′:** thân sâu hơn nửa mét (thêm khoảng 106 t, khoảng 4% bê tông thân phao) thì lấy lại mạn khô. Nhà giữ thấp tầng.
- **Ổn định:** trọng tâm G, tâm nổi B, metacentre M (CLM_005). Phao rộng và nông rất khó lật trong nước lặng: dời 100 t ra mép, phao nghiêng chưa tới nửa độ (CLM_009, tính).
  - Câu nhắc: *"only for small angles"* (CLM_006).
- **Twist:** phao "cứng" thì bám theo mặt nước (CLM_007). *"Floating was the easy part. Staying comfortable is not."* Đây là cầu nối sang C4. Ở đây chỉ gieo câu hỏi.
- **Chuyển:** *"But one platform is a few dozen homes. A city needs hundreds."* (khoảng 50 người mỗi phao, tính).

## C3: Why One Platform Isn't a City (khoảng 80 giây)
- **Nhân bản:** từ một phao thành năm. *"So why not weld them into one big slab?"*
- **Tải khác nhau, mặt sàn lệch nhau:** nhà 2 tầng và nhà 4 tầng trên hai phao giống nhau làm mặt sàn lệch khoảng 66 cm (tính). Cầu cứng sẽ bị bẻ, nên phải có khớp mềm, hoặc dằn để cân mớn nước. Lựa chọn có giá.
- **Mối nối là chỗ yếu được nêu tên** (CLM_042). Nghiên cứu nối mềm và giữ khoảng cách giữa các module (CLM_056).
- **Đếm:** 10.000 người cần khoảng 200 phao 40 m và vài trăm mối nối (tính). **Phao to hay nhiều phao?** Phao 100 m chỉ cần khoảng 34 chiếc, nhưng mỗi chiếc khoảng 30.000 t. Ngay phao Schoonschip đã quá to cho ụ khô truyền thống (CLM_014).
  - *"There's no free answer: fewer joints, or easier pieces."*
- **Chuyển:** *"And all of this sits on water that will not keep still."*

## C4: The Water Never Stays Still (khoảng 85 giây)
- **Sóng khái niệm** (có nhãn *Conceptual motion visualization — not a hydrodynamic simulation*): các phao nhấp nhô lệch pha; khe co giãn; cầu mềm làm việc.
- **Người ở cảm nhận:** ngay trong kênh Amsterdam, cư dân thấy nhà rung lắc khi bão và khi tàu lớn qua, nhất là tầng trên (CLM_022).
- **Phao lớn còn uốn:** hydro-elastic. Đây là thách thức nghiên cứu còn mở (CLM_053).
- **Lời giải thứ nhất là địa điểm:** chọn vùng nước kín, đà gió ngắn (CLM_050). Cho thấy cùng thành phố ở hai vịnh, một kín một hở (sơ đồ).
- **Lời giải thứ hai là bố cục:** nhà ở vào trong, chức năng chịu được chuyển động ra ngoài (CLM_055). Thêm đê chắn ở phía hở, nhưng đê có giới hạn (CLM_051, CLM_052).
- **Chuyển:** *"Calmer water helps. But a floating city still has to stay where we put it."*

## C5: Keeping the City in Place (khoảng 70 giây)
- **Lộ dưới nước:** mặt nước mờ dần (hai bước: thấy mặt nước, rồi làm mờ). Hiện cọc và dây neo.
- **Nước lên xuống:** dải mực nước minh họa 2 m. Phao trượt theo cọc (CLM_020, CLM_041).
  - Cầu nối bờ phải có khớp: khoảng 3° với cầu 25 m (tính).
- **Sâu hơn thì khác:** ra chỗ nước sâu, cọc nhường chỗ cho dây neo dùng chung (CLM_055). Dây dài hơn, neo sâu hơn, chi phí tăng nhanh hơn độ sâu (CLM_054).
- **Đáy biển quyết định** (CLM_054): phim không nêu loại neo hay kích cỡ.
- **Chuyển:** *"Now it floats, and it stays. Is it a city yet?"*

## C6: A City Needs More Than Buildings (khoảng 70 giây)
- **Nhà làm mờ, lộ mạng hạ tầng.** Chỉ kể sâu hai ví dụ:
  1. **Điện:** một khu 46 hộ dùng chung **một** đầu nối lưới quốc gia; mỗi nhà có pin và lưới điện thông minh (CLM_016). Ở quy mô quận, đường cáp đi dọc cầu link-span.
     - *"Floating doesn't mean off-grid."*
  2. **Nước thải:** tách nước xám và nước đen, bơm về bờ (CLM_017, CLM_023). Dự án digester nổi chỉ được nhắc là kế hoạch.
- **Một dòng cho phần còn lại:** nước sạch, giao thông (cầu, taxi nước), cứu hỏa và cấp cứu (hai lối ra, bến tàu), lương thực từ đất liền.
  - Dẫn CLM_043: *connect to land, or develop off-grid alternatives.*
- **Chuyển:** *"Everything so far assumed sheltered water near a city. What if we moved it?"*

## C7: What Would Actually Make This Difficult? (khoảng 100 giây)
- **Phản thực tế D:** kéo quận ra khơi (sơ đồ).
  - Sóng dài đi qua đê nổi (CLM_051).
  - Dây neo dài theo đáy sâu (CLM_054).
  - Cầu biến mất, nên mọi thứ phải tự lo, và tự chủ rất tốn năng lượng (CLM_058).
  - Nghiên cứu ngoài khơi chuyển sang một loại phao khác: bán chìm, trên cột (CLM_062).
  - *"Offshore isn't the same city further out. It's a different machine."*
- **Ba khó khăn không biến mất ở vịnh kín:**
  1. **Bảo trì:** bê tông trong nước biển, cốt thép bị ăn mòn do clorua. Chưa có tiêu chuẩn chuyên cho thành phố nổi (CLM_059).
  2. **Sinh thái:** bóng râm, dòng chảy, loài ngoại lai, bám bẩn. Ở quy mô lớn, tác động lớn hơn nhiều (CLM_044).
  3. **Ai sở hữu mặt nước:** luật và quản trị chưa rõ (CLM_045). Nguy cơ phục vụ người giàu và rào mặt nước công cộng (CLM_046).
- **So sánh trung thực với đất liền:**
  - kết cấu nổi theo kịp mực nước và có thể dời đi, dùng lại (CLM_041);
  - đổi lại phải có neo, mối nối và bảo trì liên tục.
  - *"It's not land, minus the problems. It's a different set of problems."*
- **Chi phí:** chưa có cơ sở chi phí có bình duyệt cho một thành phố nổi (CLM_061). Phim nói đúng điều đó, không nêu con số.

## C8: Could We Really Build It? (khoảng 80 giây, gồm lời kêu gọi)
- **So sánh cuối:** phao A cạnh quận C, cùng camera, cùng tỉ lệ. Gắn nhãn cho từng hệ đã thêm và vấn đề nó trả lời.
- **Phán quyết theo ba tầng:**
  1. **Đã có thật:** khu nổi khoảng 100 người, nối bờ, trong nước kín (CLM_010, CLM_011, CLM_016).
  2. **Hợp lý trong điều kiện cụ thể:** một quận nổi nối bờ trong vịnh kín, xây theo pha. Mọi hệ cần thiết đều có tiền lệ hoặc có nghiên cứu, nhưng **chưa có quận 10.000 người nào được báo cáo là đã xây** (CLM_033). Những câu hỏi lớn nhất (hydro-elastic, mối nối, chi phí) vẫn còn mở (CLM_042, CLM_053, CLM_061).
  3. **Còn suy đoán:** thành phố ngoài khơi tự chủ (CLM_051, CLM_058).
- **Câu kết:**
  - *"So, could we build an entire city that floats? Near a coast, in sheltered water, step by step — possibly."*
  - *"Far out at sea, on its own — not yet, as far as anyone has shown."*
  - *"And the hardest parts may not be the engineering at all."*
- **Lời kêu gọi** (beat `framing`, ≤ 60 từ, không claim): mời gợi ý chủ đề trong bình luận, like, subscribe; icon tự vẽ (`config/production_defaults.json`).

## Rà soát biên tập (brief mục 17)

**1. Câu hỏi trung tâm có hấp dẫn ngay không?**
Có. Hình một thành phố hoàn chỉnh cùng câu "not a render" đặt cược ngay từ đầu.

**2. Luật chơi có dễ hiểu không?**
Có. Một phao, một quy tắc (Archimedes). Mọi hệ thêm vào đều có một vấn đề đi trước.

**3. Mỗi vấn đề có dẫn logic sang vấn đề sau không?**
Có. Chuỗi là: nổi → ổn định nhưng "cứng" → nhân lên → sóng → giữ vị trí → hoạt động như thành phố → dời ra khơi → phi kỹ thuật.
- *Điểm yếu đã sửa:* bản nháp đầu đặt "ổn định" thành một chương riêng. Nó tạo một vòng "vấn đề → sửa" không có vấn đề thật, vì phao rộng không dễ lật. Giờ ổn định là một twist ngắn trong C2.

**4. Mỗi lần sửa có lý do rõ không?**
Có. Xem `DESIGN_EVOLUTION.md`. Chỗ dễ trượt là đê chắn: nó phải xuất hiện *sau* khi người xem đã thấy vịnh hở.

**5. Giải thích có dễ tiếp cận không?**
Phần lớn có. Rủi ro là metacentre (C2). Giữ nó ở một hình và hai câu; không đọc công thức thành tiếng.

**6. Có tránh được vòng lặp nhàm không?**
- *Rủi ro:* C3–C6 có cùng nhịp "thêm hệ".
- *Đã sửa:* mỗi chương đổi kiểu hình:
  - C3 là đếm và so sánh;
  - C4 là chuyển động khái niệm và so sánh hai vịnh;
  - C5 là lộ dưới nước;
  - C6 là làm mờ nhà, lộ mạng.

**7. Thành phố có tinh vi dần lên trên hình không?**
Có: một phao → năm phao có khe và khớp → quận có vòng trong/ngoài, đê, neo, hạ tầng.

**8. Có một bất ngờ thật không?**
Có ba:
- hơn nửa khối lượng là chính thân phao;
- phao rộng khó lật, nhưng chính vì thế lại bám theo sóng;
- thiết kế ven bờ không dời ra khơi được.

**9. Kết luận có trả lời câu hỏi mở đầu không?**
Có, theo ba tầng. Không nói "hoàn toàn khả thi" hay "bất khả".

**10. Người xem có hiểu kiến trúc nổi hơn không?**
Có. Họ hiểu vì sao từng bộ phận tồn tại.

**Chương yếu nhất:** C7. Nó có thể thành một danh sách vấn đề. Cách giữ: mở bằng phản thực tế có hình (D), rồi chỉ ba khó khăn, mỗi khó khăn một hình (mặt thân phao bị ăn mòn được kiểm tra; bóng râm trên đáy biển; bờ nước có hay không có lối đi công cộng). Nếu vẫn dài, cắt phần so sánh với đất liền xuống một câu.

**Ý tưởng bị loại:** chương "Ổn định" riêng (lý do ở mục 3); chương "chi phí" có con số (không có cơ sở, CLM_061); cảnh bão phá phao (không có cơ sở, và vi phạm quy tắc).
