# Diện mạo đô thị và đoạn mở đầu (L6, 2026-11-11)

Vòng này trả lời review R2: cách giải thích của B08–B11 đã đạt, nhưng toàn quận vẫn lặp lại, công viên chưa đọc được, cảnh neo mất cảm giác nước, và hồ sơ khối lượng còn câu cũ.

- **Kịch bản c-r2 giữ nguyên;** `script/narration.json` không đổi một byte.
- **Chưa sản xuất chương nào.** Đây là bản để chủ kênh xem diện mạo trước khi làm từng chương.

## Bạn sẽ xem gì (ngoài git, trong `output/pilot/`)
- **Đoạn mở đầu B01–B02:** `floating_city_design_challenge_OPENING_INTERNAL_REVIEW_720p.mp4` (24,2 giây), kèm bản `_no_sfx` và phụ đề.
  - **B01:** toàn quận → cụm có hai trường học và ba phao vườn bên hồ → cận công viên → hạ thấp sát mặt nước khi lời dẫn nói "not one of them is standing on land".
  - **B02:** kéo lui ra toàn quận.
- **`stills_r3/`, ảnh tĩnh 1920 × 1080:**
  - 01–04: các mốc của đoạn mở đầu;
  - 05: khu 5 phao với 5 kiểu nhà (B22, trước khi nước làm trong); 05b: cận khớp nối B14;
  - 06–07: hai cảnh neo với nước làm trong;
  - 08: toàn quận có công trình công cộng (B21).
- **`cluster_trial/`, cụm thử 5 phao 60 m, cùng camera:**
  - `before_*`: diện mạo cũ, mọi phao bốn khối nhà;
  - `types2_*`: các kiểu nhà mới;
  - `sand3d_*`: thay bằng mẫu Sand3D (8 căn "townhouse" trên phao 4; ghế, bàn, đèn, bộ đồ chơi trong vườn).

## Góp ý → đã làm

| Góp ý R2 | Đã làm | Kiểm tra |
|---|---|---|
| Cảnh neo gần như mất nước; cảnh cọc dễ hiểu thành nhà sàn | Nước làm trong còn giữ 50% màu ở cả 7 cảnh (B31: 35%, vì cáp nằm sâu 60 m). B24 mở bằng nước đầy rồi mới làm trong. B22 có ghi chú "Water drawn see-through". | Ảnh 06–07; test đếm cả 7 bước làm trong nước |
| Hồ sơ khối lượng ghi loại trừ "service and port platforms" | `design_model.py` tách **đã gồm** (nhà ở; trường, phòng khám, cửa hàng, văn phòng trong 40 m²/người) và **không gồm** (phao cảng, bến thuyền, phao hạ tầng; đê; cầu dẫn; neo; mạng hạ tầng). Câu tương tự trong `scenario_contract.json` cũng sửa. | `RESULTS.md` mục 9–10; không số nào đổi |
| Phân bổ 66 + 6 + 21 chỉ là giả định minh họa | Ghi rõ ở mục 10: không phải kiểm tra đủ trường, y tế hay dịch vụ theo tiêu chuẩn quy hoạch. | `RESULTS.md` |
| Thử 3–5 kiểu nhà thấp tầng, khác khối, mặt đứng, mái, lối vào; cùng bảng màu | 5 kiểu nhà ở và phao vườn (xem bảng dưới). Bảng màu thêm gạch nhạt, ốp gỗ, mái đá phiến, mái kẽm, vữa sáng, ban công, pin mặt trời. | Cụm thử; test kiểu nhà |
| Giữ số tầng, diện tích sàn, tải; đổi trọng tâm thì phải tính lại | Kiểu nào cũng 40% diện tích chiếm đất, 3 tầng, trọng tâm ở giữa sàn, nên tải, mớn nước và độ nghiêng của phép tính không đổi. Tải bằng nhau giữa các kiểu nhà được ghi là giả định của mô hình. | Test: diện tích ±0,5 m², trọng tâm < 1 cm, cao đúng 9 m |
| Cây và đất trồng nằm trong khoản tải đã khai báo, hoặc ghi giới hạn | Ghi ở `RESULTS.md` mục 10: lớp hoàn thiện 0,2 t/m² và tải thay đổi 0,25 t/m² trên sàn trống chỉ đủ cho lớp trồng mỏng; bồn cây sâu không có trong mô hình. | `RESULTS.md` |
| Mỗi cụm có một nét dễ nhận | Nhà ở chia ô 2 × 2 phao cùng kiểu; ô cạnh nhau khác kiểu. 10 phao quanh hồ thành phao vườn mở ra mặt nước. Trường chữ U, phòng khám vòng sân, nhà cộng đồng mái xanh giữ nguyên. | Test: ô cạnh nhau khác kiểu, phao vườn mở đúng về phía hồ |
| Cận cảnh công viên có bố cục rõ, không nhìn qua mái nhà | Phao vườn: bãi cỏ, lối đi ra mặt nước, cây lá kim và cây tán tròn, ghế dọc lối, bàn picnic, xích đu và tháp cầu trượt, đèn có cần, dãy ghế ven nước; nhà có ban công nhìn ra vườn. Camera nhìn từ mặt hồ vào. | Ảnh 03 |
| Thử tòa nhà Sand3D | Sàng lọc khoảng 100 mẫu, tải và đo 7: không mẫu nào là nhà 3 tầng đúng tỉ lệ. Phim dùng nhà và đồ của Studio. | `review/SAND3D_TRIAL.md` vòng 2 |
| Đoạn mở đầu: toàn cảnh → cụm có công trình công cộng → công viên → vấn đề | B01–B02 như mô tả ở trên. | Đoạn mở đầu; ảnh 01–04 |
| Kho SFX: chọn tiết chế, cần hồ sơ quyền | Kiểm kê cả 44 file. Theo thỏa thuận giấy phép của CapCut, tư liệu chỉ được sửa trên nền tảng và cấm tách ra dùng riêng, nên chưa dùng file nào. | `review/SFX_LIBRARY.md` |

### Các kiểu nhà (phao 60 m, 1.440 m² chiếm đất, 3 tầng)

| Kiểu | Hình khối | Mặt đứng, lối vào | Mái | Vườn |
|---|---|---|---|---|
| Bốn khối (cũ) | 4 khối vuông | cửa sổ đều, một cửa mỗi khối | phẳng | lối lát |
| Nhà liền kề | 8 dãy, hai hàng mỗi góc phao | gạch nhạt, cửa mỗi 6 m | dốc hai mái, đá phiến | vườn sau giữa hai hàng |
| Sân trong | vòng 4 cánh chữ L, cổng trên hai trục | cửa sổ hẹp cao | phẳng, pin mặt trời | sân cỏ, 4 cây tán tròn |
| Biệt thự | 8 nhà 10,5 × 17 m, so le | ốp gỗ, cửa sổ rộng | lệch một mái, kẽm | cỏ, cây sau nhà |
| Thanh xoay | 4 thanh xoay quanh tâm | ban công liền ở hai mặt dài | phẳng | dải cỏ, hàng cây |
| Phao vườn (10 phao quanh hồ) | 4 thanh ở hai bên | ban công nhìn ra vườn, cửa mỗi 6 m | phẳng | công viên đầy đủ (xem trên) |

## Lựa chọn của agent cần bạn biết
- **Bỏ phần làm sáng ở B02.** Agent đã thử làm sáng thân phao, neo và hạ tầng đúng lúc lời dẫn nói "floats / stays / keeps working". Ở tầm toàn quận, các phần này chỉ chiếm 0,05–0,5% khung hình và kiểm Blender từ chối. B02 giờ chỉ kéo lui ra toàn quận; B04 vẫn tháo rời các hệ thống đó.
- **Đường ống hạ tầng** chuyển từ hàng 6 sang hàng 7 để không cắt ngang công viên ven hồ. Kế hoạch hình của B25–B27 vẫn thực thi được. Hai shot này chưa render lại, sẽ xem khi làm chương 6.
- **Camera trong đoạn mở đầu đứng cách 400 m** (khóa mới `clearance` của khung nhìn SEQUENCE). Với mặc định 10 m, mặt phẳng cắt gần xén các phao ở phía trước, rõ nhất khi camera di chuyển. Hệ quả: khung sát mặt nước có mái nhà bờ hồ đối diện ở mép dưới.
- **B14 (cận khớp nối) đổi khung.** Lần kiểm Blender đầu tiên của shot này (R2 chưa kiểm) cho thấy:
  - với 5 kiểu nhà, mặt phẳng cắt gần xén tòa nhà sân trong;
  - khi camera lùi xa thì tòa nhà đó che bản lề, ống nối và đệm va.
  Giờ camera nhìn dọc theo khe nước (từ phía nam, nghiêng 55°), đứng cách 40 m, khung chặt hơn (lề 0,12) để bản lề, ống và đệm va đều đạt tối thiểu 0,3% khung hình.
- **Khu 5 phao** (B14, B17, B22, B24) dùng 5 kiểu nhà. Cặp phao B13, phao mẫu B08–B12 và phao so sánh B33 giữ bốn khối, vì câu chuyện cần đếm tầng và so trực tiếp.
- **Tham số `home_types = blocks`** dựng lại diện mạo cũ để so trước/sau.

## Sửa engine (có test)
- **Camera lùi giữa hai khung khác hướng** (`framing.orbit_pose`):
  - trước đây có thể lùi quá khoảng cắt xa của camera, hiện mảng nền phẳng ở 123/580 khung của bản render đầu;
  - nay `clip_end` của SEQUENCE tính cả lúc lùi (`framing.sequence_clip_end`);
  - mức lùi tỉ lệ với góc quay, không lùi khi chỉ đổi khung;
  - quét lại: 0/580 khung có mảng phẳng.
- **Khóa `clearance` cho khung nhìn SEQUENCE**, mặc định 10 m như cũ. Planner chuyển tiếp khóa này. Camera dựng cho khung đầu (cả shot chỉ có một khung) cũng dùng nó (`scene.build_camera`).

## QA kỹ thuật
- **Kế hoạch hình:** `plan-visuals` thực thi được 44/44; `validate-plan` và dựng shot đạt.
- **Kiểm Blender** (SC_001, SC_002, SC_014, SC_022, SC_024): **85/85** (`qa/blender_checks_opening.json`).
- **Đoạn mở đầu** (`qa/excerpt_OPENING.json`):
  - 24,167 s, 580 khung, 720p;
  - −16,4 LUFS, đỉnh thật −1,4 dBTP;
  - cắt SC_001 → SC_002 khớp khung (SSIM 0,99992);
  - Whisper WER 0 cho cả hai câu của mỗi beat;
  - phụ đề 5 cue, tối đa 14,9 ký tự/giây, không cảnh báo.
- **Không có âm hiệu ứng** trong đoạn này, nên bản `_no_sfx` giống hệt (cùng checksum).
- **Agent tự xem khung hình:**
  - quét cả 580 khung tìm mảng nền phẳng ở một phần ba trên: 0 (bản render đầu có 123);
  - xem từng giây: không thấy tòa nhà bị xén.
- **Cụm thử, 1080p, cùng camera** (`output/pilot/cluster_trial/*_report.json`):

  | | Cũ (bốn khối) | Kiểu nhà mới | Có mẫu Sand3D |
  |---|---|---|---|
  | Khung cả cụm | 2,58 s | 2,57 s | 2,67 s |
  | Cận công viên | 1,96 s | 1,97 s | 1,98 s |
  | Đối tượng lưới | 73 | 89 | 114 |

- **Toàn quận:** 1.048 đối tượng (R2: 899). Kiểm BVH 4/4 cho quận, quận ngoài khơi và khu 5 phao.
- **Test:** 467 test đạt (trừ `test_blender_m6`, cần mở Blender); đánh giá planner 33/33.
- **Chưa có ai nghe;** các số âm thanh trên là đo bằng máy.

## Còn có thể làm tốt hơn
- **B02 giữ toàn quận gần 10 giây** (từ khoảng giây 14) trong lúc lời dẫn nói câu thứ hai, chỉ có camera chỉnh khung rất chậm. Nếu thấy dài, có thể đẩy chậm vào phao giữa (B04 bắt đầu từ đó).
- **Ở tầm toàn quận** các kiểu nhà khác nhau chủ yếu qua màu (gạch, gỗ, pin mặt trời) và hình mái. Công viên quanh hồ chỉ rõ khi vào gần.
- **Các shot khác của quận và khu 5 phao chưa render lại** với kiểu nhà mới (B04, B12–B21, B25–B31, B35, B38). Kế hoạch hình thực thi được, nhưng phải xem từng khung khi làm từng chương: lỗi xén ở B14 chỉ lộ ra khi kiểm Blender.

## Cần bạn quyết
1. **Diện mạo đô thị:** kiểu nhà, phao vườn, công viên và nước làm trong 50% đã đủ để làm từng chương chưa?
2. **Đoạn mở đầu:** nhịp và đường camera có đạt không? Riêng khung sát mặt nước có mái nhà bờ đối diện ở mép dưới: giữ, hay đổi sang khung chỉ có nước (khi đó phải xử lý mặt phẳng cắt theo cách khác)?
3. **Sand3D:** đồng ý không dùng tòa nhà Sand3D? Bộ đồ chơi Sand3D chi tiết hơn của Studio; có muốn đưa vào (cần bộ nhập USD, manifest, ghi công) không?
4. **SFX:** tìm nguồn âm có giấy phép rõ ràng, hay giữ âm tổng hợp của Studio?
5. **(Vẫn mở từ trước)** Có commit các file TTS gốc (`audio/segments/*.wav`) không?
