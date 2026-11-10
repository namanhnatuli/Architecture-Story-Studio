# Đoạn thử có lời dẫn: "thêm tải → chìm → sửa thân" (B08–B11)

## Vòng 2 (R2, 2026-11-10): sau review asset và đoạn thử L5

- **Trạng thái:** `INTERNAL_REVIEW`, chờ chủ kênh duyệt. Chưa render phần còn lại của phim. Kịch bản c-r2 không đổi (lời dẫn không đổi một byte).
- **Tệp xem (ngoài git), trong `output/pilot/`:**
  - `floating_city_design_challenge_EXCERPT_LOAD_SINK_FIX_R2_INTERNAL_REVIEW_720p.mp4` (77,4 s; phụ đề `….en.srt` cùng tên); bản `_no_sfx` để so âm thanh.
  - Ba still 1920×1080 trong `stills_r2/`:
    - `01_platform_SC012.png`: phao;
    - `02_neighbourhood_mooring_lines_SC024.png`: khu có dây neo (và `02b_…_piles_SC022.png` với cọc);
    - `03_district_public_uses_SC021.png`: toàn quận có công trình công cộng (và `03b_district_aerial_SC001.png`).
  - Thử Sand3D trong `sand3d_trial/`: ảnh trước/sau và kịch bản thử. Xem `review/SAND3D_TRIAL.md`.

### Góp ý → đã làm

| # | Góp ý | Đã làm | Kiểm tra |
|---|---|---|---|
| 1 | Nhà là hộp liền, khó đọc ba hay bốn tầng | Mỗi tầng có cửa sổ (nhịp 3 m) và vạch tầng; tầng trệt có lối vào với mái che. Tầng 4 mang theo cửa sổ của nó khi đặt xuống. | Still B08/B09; test `test_storeys_carry_their_windows` |
| 2 | B08: lời nói bốn khối, hình chỉ còn hai | B08 mở trên **cả phao** (bốn khối, nước xung quanh). Hết câu đầu, nửa trước và nước phía trước được bỏ đi; ghi chú "Cut through the middle". | Khung 0:02 → 0:08 |
| 3 | B08: mảng vàng trong khoang giống nước ngập | Bỏ mảng vàng. Khi nói "floats about 3 meters deep", hiện **đường kích thước mớn nước** ngoài thân phao: "Draft ≈ 2.96 m". B06 dùng đường viền phần thân dưới nước, không tô trong khoang. | Khung 0:13 |
| 4 | B09: zoom đúng lúc chìm; vạch vàng như chi tiết vật lý | Tầng 4 đặt xuống ở khung toàn mặt cắt. **Camera vào cận rồi dừng hẳn**, sau đó phao mới chìm. Vạch vàng thành **đường kích thước** (mặt nước → sàn). Nét đứt "Deck before" giữ mức sàn cũ. Nhãn "Freeboard: 1.04 → 0.71 m". | Test `test_the_camera_is_still_whenever_the_platform_moves_or_grows` |
| 5 | B10: bốn lần đổi khung; phần thân thêm nhỏ | Còn **hai khung**. (1) Nửa đông của mặt cắt, từ sàn tới đáy: đáy hạ 0,5 m, vách và thành trượt xuống theo. Phần thêm tô vàng, nên thấy thành một dải vàng qua mọi khoang. Đáy cũ nét đứt một lúc. Nhãn "+0.5 m hull: ≈ 106 t (+4%)". (2) Cận mép nước: phao nổi lên, mức sàn trước nét đứt, nhãn "Freeboard: 0.71 → 1.15 m" giữ tới hết beat. Camera đứng yên trong mọi thay đổi hình học. | Cùng test; QA Blender |
| 6 | B11: thiếu chuẩn so sánh; nhà trong suốt lộ sọc mái, che nhạt khối tải | **Bỏ hẳn** dãy nhà phía trước: nắp mái bên trong ẩn trước, nên không còn sọc. Thêm **đường ngang nét đứt** ở mức sàn trước khi nghiêng (dài quá hai đầu phao), viền mép sàn, và **mũi tên 15 m** trên mặt sàn với nhãn "15 m". Góc vẫn là góc thật. | Khung 1:02–1:17 |
| 7 | B11 dùng góc của bản 3 tầng | Mô hình tính có thêm `list_example_shown_state`: 4 tầng, thân 4,5 m → **0,438°**. Hình xoay đúng giá trị này. Nhãn vẫn "≈ 0.4°". | `analysis/RESULTS.md` mục 11; test `test_tilt_is_the_list_calculated_for_the_state_shown` |
| 8 | Quận: 66 module nhà ở chỉ đủ 9.504 người | Phân bổ mới trong mô hình tính (`district_C_allocation`): 66 nhà ở + **6 hỗn hợp** (tầng trệt cửa hàng/dịch vụ, hai tầng trên nhà ở; ở hai sườn gần bờ) + 21 dịch vụ. Kết quả **10.080 người** ở mức 30 m², khoảng 9,9 m² dịch vụ/người. Mọi module giữ cùng diện tích chiếm đất, số tầng và tải, nên cùng mớn nước 2,917 m. | `analysis/RESULTS.md` mục 10; test `test_district_allocation_is_the_calculated_one`; nguồn và claim không đổi |
| 9 | Quận lặp một kiểu nhà; chưa thấy trường, phòng khám, công viên | 21 module dịch vụ: **3 trường học** (chữ U quanh sân, mái cam, sân chơi), **1 phòng khám** (vòng quanh sân trong, mái xanh ngọc), **17 nhà cộng đồng/cửa hàng/văn phòng** (hai dãy dài, mái xanh lá). **Công viên:** 10 module nhà ở quanh hồ có cỏ và cây trên phần sàn trống. Mọi phao có lối đi lát. | Still 03; test `test_every_use_covers_the_same_floor_area` |
| 10 | Chưa có âm hiệu ứng | Hai âm tổng hợp nhẹ, thấp hơn lời dẫn 14 dB: lúc tầng 4 đặt xuống (B09) và lúc phần thân mới vào chỗ (B10). Hai bản giờ khác nhau theo checksum. | QA: 2 cue, không mẫu bị cắt |

### QA kỹ thuật R2

| Kiểm tra | Kết quả |
|---|---|
| Kiểm Blender bốn shot | 73/73 đạt (bộ phận đáp đúng chỗ, kể cả khi đã chìm trước đó; phần phát sáng nhìn thấy được; camera đồng nhất) |
| Khung hình, cắt | 1858 khung, 77,417 s. Cắt khớp SC_008→009 (SSIM 0,9997), SC_009→010 (0,99998). SC_010→011 là cắt thẳng sang phao 3D (0,70, có chủ ý) |
| Âm | −16,5 LUFS, đỉnh −1,4 dBTP; 2 cue hiệu ứng, không mẫu bị cắt |
| Whisper | WER 0,0 cả bốn shot, cả bản có và không có hiệu ứng |
| Phụ đề | Vẫn một cảnh báo nhẹ: cue 8 (B09) 17,1 ký tự/giây |
| Asset | 11 spec: kiểm offline 5/5, Blender 4/4 (quận 899 đối tượng) |

**Agent xem lại video R2** bằng khung trích mỗi 3,25 giây; các điểm trên đều thấy được.

**Còn có thể cải thiện, chờ ý bạn:**
- Toàn quận vẫn là lưới nhà ở giống nhau. Các công trình công cộng đọc được ở góc toàn cảnh; cây và lối đi chỉ thấy khi gần hơn.
- Ở still khu có hệ neo (B24), nước làm mờ tới 85% trông gần như không có nước. Có thể giảm còn khoảng 70% để giữ màu nước. Thay đổi này chưa làm vì B24 không nằm trong đoạn thử.

### Cần bạn quyết
1. B08–B11 R2 đã đạt để áp cách làm cho các chương còn lại chưa?
2. Phân bổ 66 + 6 hỗn hợp + 21 dịch vụ có được không? Đây là giả định minh họa, không đổi lời dẫn hay claim.
3. Sand3D: dùng cho vài cảnh cận (công viên, sân trường) hay chưa? Xem `review/SAND3D_TRIAL.md`.

---

## Vòng 1 (2026-11-08)

- **Trạng thái:** `INTERNAL_REVIEW`, chờ chủ kênh duyệt chất lượng hình. Chưa render phần còn lại của phim.
- **Tệp xem (ngoài git):** `output/pilot/floating_city_design_challenge_EXCERPT_LOAD_SINK_FIX_INTERNAL_REVIEW_720p.mp4` (77,4 s), phụ đề `….en.srt` cùng tên.
  - `tools/excerpt.py` luôn xuất thêm bản `_no_sfx`. Bốn shot này không có âm hiệu ứng nào, nên hai bản giống hệt nhau.
  - Báo cáo kỹ thuật: `qa/excerpt_EXCERPT_LOAD_SINK_FIX.json` và `qa/blender_checks_excerpt.json` (số liệu QA bên dưới lấy từ đây).
- **Phạm vi:** bốn shot liền nhau của phim, đúng như sẽ nằm trong bản đầy đủ: SC_008 (B08), SC_009 (B09), SC_010 (B10), SC_011 (B11). Lời dẫn là bản c-r2 đã khóa, giọng `am_michael`.
- **Vì sao thêm B11:** brief chỉ yêu cầu B08–B10. B11 dùng hai năng lực mới nữa (phao 3D nguyên khối, xoay đúng góc tính) và khép chuỗi bằng câu "Floating is only the first problem". Nhờ vậy đoạn thử dài khoảng 77 giây, nằm trong khoảng 60–90 giây của playbook.

### Bạn sẽ thấy gì

| Beat | Hình | Số trên hình (nguồn: `analysis/results.json`) |
|---|---|---|
| B08 | Mặt cắt phao 3 tầng, nhìn chéo rồi xoay về chính diện. Lúc nói "floats about 3 meters deep", khối nước bị chiếm chỗ hiện ra. Đến "the surprise", nhà mờ đi và thân bê tông sáng lên. | Mớn ≈ 2,96 m; thân ≈ 55% khối lượng |
| B09 | Tầng 4 hạ xuống. Phao chìm thêm đúng 0,332 m. Camera vào cận mép đông. Vạch vàng cạnh thân là mạn khô: phần nằm dưới nước bị mặt cắt nước che, nên phần còn thấy chính là mạn khô. | Mạn khô 1,04 → 0,71 m |
| B10 | Cận góc đáy: đáy hạ 0,5 m, thành và vách nối dài (tô vàng ở mặt cắt). Lùi ra toàn thân phao. Cận lại mép đông khi phao nổi lên 0,436 m. Lùi ra cả mặt cắt: nhà sáng lên ở câu "Lighter buildings". | +0,5 m thân ≈ 106 t (+4%); mạn khô 0,71 → 1,15 m |
| B11 | Phao 3D nguyên khối, cùng trạng thái cuối B10. Dãy nhà phía trước mờ đi. Khối 100 t trượt 15 m ra mép, rồi phao nghiêng đúng góc tính. Góc thật rất nhỏ, đó là ý của câu. | 100 t, 15 m, nghiêng ≈ 0,4° (true scale) |

### Điểm cần bạn đánh giá
1. **Đọc được cơ chế chưa?** Tầng thêm → chìm → mạn khô giảm → thân sâu hơn → mạn khô hồi lại.
2. **Vạch mạn khô vàng** (thay cho thước của prototype P6): có rõ là "phần thân trên mặt nước" không?
3. **Phần thân thêm 0,5 m:** P6 đã cho thấy chi tiết này nhỏ. Bản này vào cận góc đáy lúc đáy hạ, rồi lùi ra cho thấy cả dải vàng. Đủ chưa?
4. **Nhịp camera B10:** bốn lần chuyển khung trong 18 giây (góc đáy → toàn thân → mép đông → toàn cảnh). Có rối không?
5. **B11:** góc nghiêng thật 0,42° gần như không thấy. Lời dẫn và nhãn "true scale" nói đúng điều đó. Bạn muốn giữ góc thật, hay thêm một hình phóng đại có nhãn "exaggerated"?
6. **Âm thanh:** đoạn này chỉ có lời dẫn, không có âm hiệu ứng. Agent không nghe được; mức âm lượng và độ rõ chỉ đo bằng máy (bên dưới).

### Lựa chọn của agent cần bạn biết
- **B11 dùng trạng thái cuối B10 (4 tầng, thân 4,5 m)** để B12 làm đúng hướng bạn nêu: tầng 4 và phần thân thêm mờ đi rồi mới nhân phao. Góc 0,42° tính cho bản 3 tầng; bản 4 tầng thân 4,5 m cho khoảng 0,44°. Cả hai đều "khoảng 0,4°" và "dưới nửa độ" như lời dẫn. Hình xoay đúng 0,42° theo `results.json`.
- **Nhãn khối lượng ở B08:** không ghi "≈ 4 850 t" trên hình, vì lời dẫn nói "about 4,800 tons". Hình chỉ ghi mớn nước và tỉ lệ của thân.
- **"+0,5 m hull: ≈ 106 t"** trên hình, trong khi lời dẫn nói "about 100 tons". Số 106 là giá trị tính; hai cách nói không mâu thuẫn. Có thể đổi nhãn thành "≈ 100 t" nếu bạn muốn khớp tai nghe.
- **Nhãn "+1 story, same load per m² of floor"** dùng đúng cách diễn đạt bạn chọn ở review c-r1.

### QA kỹ thuật (2026-11-08)

| Kiểm tra | Kết quả |
|---|---|
| Kiểm Blender bốn shot (`--mode check`) | 76/76 đạt: bộ phận đáp đúng vị trí, phần phát sáng nhìn thấy được, camera đồng nhất trong nhóm, không giao cắt mới |
| Khung hình | 1858 khung, 77,417 s, khớp timing của phim; không lỗi giải mã, không đoạn đen |
| Điểm cắt | SC_008→SC_009 và SC_009→SC_010 là cắt khớp (SSIM 0,9995 và 0,99998); SC_010→SC_011 là cắt thẳng từ mặt cắt sang phao 3D cùng hướng nhìn (SSIM 0,83, đúng chủ ý) |
| Âm lượng | −16,5 LUFS tích hợp, đỉnh thật −1,4 dBTP, không mẫu bị cắt |
| Whisper trên lời dẫn của từng shot | WER 0,0 cả bốn shot |
| Phụ đề | 19 cue, dòng dài nhất 42 ký tự. Một cảnh báo nhẹ: cue 8 (B09, câu 3) 17,1 ký tự/giây, ngưỡng 17,0 |

**Agent đã xem lại video** bằng khung trích mỗi 3,25 giây và khung tại các nhãn.
- Đã sửa một điểm trước khi gửi: nhãn mớn nước ở B08 chỉ hiện 1,5 giây. Giờ nó hiện từ chữ "floats", cùng lúc khối nước hiện ra. Chỉ SC_008 được render lại.
- Điều agent thấy còn có thể cải thiện, chờ ý bạn:
  - Ở B08, nhà mờ tới 85% nên gần như biến mất khi thân phao sáng lên.
  - Cận cảnh mép đông ở B09–B10 chủ yếu là lòng thân phao màu tối; vạch mạn khô nằm ở rìa phải.
  - Ở B11, lúc dãy nhà phía trước đang mờ dần, các nắp mái bên trong hiện thành vài sọc ngang trong khoảng 1 giây.

### Bước tiếp theo
- **Bạn duyệt:** áp cùng cách làm cho các cảnh còn lại, render cả phim ở `internal_720p` theo chương, rồi review nội bộ toàn phim.
- **Bạn yêu cầu sửa:** sửa `script/visuals.py` (hoặc asset), render lại đúng các shot này, gửi lại đoạn thử.
- Không render 4K trước khi bạn duyệt cả phim.
