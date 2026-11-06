# Vòng g-r5: sửa đoạn thử, chương Beauvais, mở phim mới

- **Theo góp ý của chủ kênh về đoạn thử g-r4** (2026-11-06), làm đúng thứ tự đề nghị:
  1. sửa các điểm yếu của đoạn thử;
  2. chương Beauvais, cùng hình riêng và ảnh thật cho Beauvais và Amiens;
  3. mở phim bằng các hình vừa có.
- Bước 4 (xây dựng, ánh sáng, các sơ đồ còn tĩnh) **chưa làm**. Riêng timeline đã tiến theo lời ở mọi chương.
- **Trạng thái:** INTERNAL REVIEW. Chưa có gì được duyệt. Lời dẫn, timing và claim giữ nguyên như g-r3.
- **File để duyệt** (trong `projects/gothic-cathedral-heights/output/`, ngoài git):
  - `pilot/gothic_cathedral_heights_PILOT_G_R5_INTERNAL_REVIEW_720p.mp4` (và `_no_sfx`): đoạn thử đã sửa, 1:17,9;
  - `chapters_internal_720p/gothic_cathedral_heights_C8_documentary_INTERNAL_REVIEW.mp4`: chương 8, Beauvais;
  - `chapters_internal_720p/gothic_cathedral_heights_C1_documentary_INTERNAL_REVIEW.mp4`: chương 1, mở phim.
- Các chương khác **chưa render lại**. Bản g-r3 đầy đủ không còn khớp với kế hoạch hình.

## 1. Đoạn thử: đã sửa gì

| Góp ý | Đã làm |
|---|---|
| Giảm lớp hình mờ phía sau | B12, B13 chỉ giữ tường cao của khoang (mờ 0,9) làm mốc; phần còn lại ẩn hẳn. B16, B17 chỉ hệ trụ ở mặt cắt chờ mờ; các khoang sau bỏ hệ trụ, vì lớp mờ chồng nhau thành vệt. |
| Tăng tương phản cấu kiện đang giải thích | Bộ phận đang được nói tới chuyển sang màu vàng đất của bảng màu, thay vì sáng lên. Đá sáng phát sáng trên nền sáng thì mất tương phản. |
| Nhìn từ dưới, chân trụ như treo trong không khí | B12 mở bằng cả nhà thờ đứng trên sàn (góc thường). Phần còn lại, gồm cả sàn, mờ đi; một khoang đứng riêng. Rồi camera **quay một cung** xuống dưới khoang và nhìn **thẳng lên**: chữ X của gân, một trụ ở mỗi góc, không còn chân trụ lơ lửng. B13 giữ góc đó và tiến lại gần. |
| Giữ trụ ngoài rõ khi trụ chống bay xuất hiện | Trụ ngoài đặc lại khi đọc "stands **outside**", trước khi trụ chống bay tới ở "flying". |
| Khung B17 thừa nền bên phải | Khung lấy thêm chân vòm cao, nơi lực đẩy "rời vòm", nên trụ chống bay và trụ ngoài nằm cân hơn. |
| Ổn định camera trong thao tác của B12 | Mỗi lúc chỉ một thay đổi: mờ phần còn lại khi camera đứng yên; camera quay khi không có gì đổi; gân hiện ra khi camera đã dừng. |
| Đường lực vẽ dần, giữ hình cuối ổn định | Mỗi đoạn đường lực hiện dần theo tuyến truyền lực, đầu mũi tên đến cuối, rồi đứng yên. Không kéo dài, không phồng, không chạy hạt. |

Kiểm tra đoạn thử:
- Blender QA 76/76.
- Hai điểm cắt khớp, SSIM 0,99999 và 1,0.
- Âm lượng −16,4 LUFS, đỉnh −1,4 dBTP.
- 3 tiếng đá ở 0:06,9, 0:07,6 và 1:13,4.
- Whisper không sai từ nào ở cả bản có và không có tiếng đá.
- 17 dòng phụ đề.

## 2. Chương 8, Beauvais: chuỗi hình

Ảnh thật xác lập công trình, rồi đánh dấu bộ phận, rồi mặt bằng và mặt cắt của chính Beauvais, rồi trở lại ảnh thật.

| Beat | Lời | Hình |
|---|---|---|
| B31 | "Which brings us back to Beauvais… 1225, a fire…" | **Ảnh thật** dàn hợp xướng Beauvais hôm nay, nhìn từ phố (Dguendel, CC BY 4.0). Năm 1225, đám cháy, ý định xây lại hiện theo lời. |
| B32 | "…two lower levels… finished… adding about five meters to the upper windows…" | **Ảnh thật** bên trong dàn hợp xướng. Ba tầng (vòm cuốn, triforium, cửa sổ cao) được **đánh dấu bên cạnh ảnh** theo lời. Tầng trên đổi màu khi đọc "adding", kèm "+ about 5 m" và ghi chú phần thêm là sơ đồ. |
| B33 | "…more than 45 meters, a few meters above Amiens…" | Hai công trình bằng **ảnh riêng**: lòng chính Amiens (Eusebius, CC BY 3.0) và dàn hợp xướng Beauvais, kèm độ cao và các con số công bố khác nhau. |
| B34 | "…November 1284, part of the vaults over the choir came down…" | **Mặt bằng Beauvais do Viollet-le-Duc vẽ** (1856). Vùng các khoang thẳng của dàn hợp xướng được khoanh và gạch nhẹ: "Vault cells over the choir's straight bays came down", đúng như nguồn ECSMGE 2024 viết. **Không có cảnh sập.** Câu "the last limit" kèm ghi chú: chính Viollet-le-Duc vẽ mặt bằng này. |
| B35 | Các giả thuyết, nghiên cứu 2024, "upper parts too flexible" | **Mặt cắt trụ chống bay Beauvais do Viollet-le-Duc vẽ.** Mỗi giả thuyết một sơ đồ, lần lượt: (1) khoanh trụ chống bay; (2) mũi tên gió vào phần trên; (3) mũi tên lún dưới chân trụ; nghiên cứu 2024 gạch chéo mũi tên lún; giả thuyết của họ ("Their hypothesis") khoanh phần trên. Không còn nhiều dòng chữ cùng lúc. |
| B36 | "New piers went up between the old ones, turning three bays into six… 1340" | **Cùng mặt bằng:** các **trụ mới** (màu cam) hiện lần lượt giữa các trụ cũ của hàng vòm cuốn trong ba khoang thẳng; ghi "positions schematic". Chữ "3 bays become 6" và vòm bốn phần thành sáu phần (Murray). |
| B37 | Thế kỷ 16: cánh ngang, tháp 150 m, bốn trụ mảnh, phía tây không có lòng chính, 1573, lòng chính không bao giờ xây | Mặt bằng Beauvais (phần lòng chính chỉ có nét mờ): khoanh cánh ngang, **bốn trụ giao cánh**, vùng **lòng chính không bao giờ xây**. **Ảnh thật** cánh ngang và dàn hợp xướng hôm nay (Chris06, CC0). **Timeline tiến tới** 1500, 1569, 1573 theo lời. Tháp sập được kể, không được dựng. |
| B38 | "Beauvais was not alone… Amiens… crossing… iron chain…" | **Ảnh thật** Amiens, rồi **mặt bằng Amiens của Viollet-le-Duc**: bốn trụ giao cánh, **tuyến dây xích** vẽ dần dọc lòng chính tới trụ giao cánh, ghi "route schematic", đúng như Columbia mô tả. |

### Kiểm tra vượt quá bằng chứng
- **Vùng vòm sập:** chỉ khoanh các khoang thẳng của dàn hợp xướng (CLM_182: "des voûtains des travées droites du chœur… s'effondrèrent"), ghi "vault cells… came down". Không vẽ khối đổ, không vẽ trạng thái sau sập.
- **Trụ mới:** CLM_185 (Murray) nói trụ bổ sung được chèn giữa các trụ của hàng vòm cuốn, ba khoang thành sáu. Hình đặt trụ mới ở giữa mỗi khoang thẳng, trên hai hàng vòm cuốn, ghi "positions schematic".
  - Mặt bằng của Viollet-le-Duc chỉ có ba khoang thẳng, tức chưa có các trụ chèn thêm, nên đánh dấu trụ mới lên đó là hợp lý.
- **Giả thuyết:** mỗi dấu nằm đúng vùng mà giả thuyết nói tới (trụ chống bay, gió vào phần trên, móng) và đều ghi "schematic". Mũi tên gió không thể hiện cường độ. Nghiên cứu 2024 vẫn ghi "an argument, not a settled result".
- **Dây xích Amiens:** nguồn chỉ nói "runs the length of the nave and ties the crossing pier". Hình vẽ một tuyến dọc hàng vòm cuốn phía nam tới trụ giao cánh, ghi "route schematic"; không vẽ một vòng quanh giao cánh.
- **Mặt bằng Amiens:** đây là thiết kế gốc theo Viollet-le-Duc (tháp vuông, chưa có nhà nguyện bên). Chỉ dùng phần lòng chính và giao cánh.
- **Độ cao:** vẫn "more than 45 m" và "more than 42 m", kèm "Published heights differ".

## 3. Mở phim (chương 1)

- **B01:**
  - Lúc đọc "November 1284… Beauvais… came down": **ảnh thật** bên trong dàn hợp xướng Beauvais, nhìn lên, trôi rất chậm.
  - Lúc đọc "45 meters": một ngoặc độ cao "more than 45 m above the floor", vẽ dần, kèm "Published heights differ: 46 m to above 48 m".
  - Lúc đọc "the choir… eastern arm… twelve years": thêm ảnh dàn hợp xướng nhìn từ ngoài, "In use since 1272".
  - Sập được kể, không được dựng.
- **B02:** "Many still stand", rồi **ảnh thật** lòng chính Amiens, "begun 1220", "more than 42 m", "tall, slender, filled with light".
- **B03:** card tiêu đề và câu hỏi, giữ nguyên.
- Mô hình 3D chung của B01, B02 cũ (ghi "Illustrative model, not Beauvais/Amiens") bị thay, đúng nhận xét "không thay tên trên cùng một mô hình".

## 4. Timeline ở các chương khác

Mọi timeline (B10 Cluny, B14 Durham, B21 Saint-Denis, B30 Amiens, B37 Beauvais) giờ có một vạch thời gian tiến tới từng mốc theo lời, rồi mốc mới hiện. Đã kiểm tra bằng khung tĩnh và Blender QA; các chương đó chưa render lại thành video.

## 5. Quyền ảnh

Bảy tài liệu: 4 ảnh chụp và 3 bản vẽ.
- Hồ sơ đầy đủ ở `assets/manifest.json`, bảng kê ở `review/RIGHTS_PROVENANCE.md`.
- Mỗi ảnh có dòng ghi công trên hình. Mô tả YouTube nháp có mục "Photographs and drawings", liệt kê giấy phép, đường dẫn và các chỉnh sửa.
- Không dùng ảnh CC BY-SA.
- Agent chỉ kiểm giấy phép theo hồ sơ Commons. **Chủ kênh chưa duyệt ảnh và ghi công** (mục "Images and attribution" trong checklist).

## 6. Còn yếu, và cần chủ kênh quyết

1. **Mô hình 3D riêng của Beauvais chưa dựng.** Vòng này dùng mặt cắt và mặt bằng của chính Viollet-le-Duc (có ghi "46 m 50 jusqu'au sol") làm hình riêng. Nếu muốn 3D, có thể dựng phần dàn hợp xướng (khoang thẳng, hai tầng trụ chống bay) theo mặt cắt đó.
2. Bản vẽ Viollet-le-Duc chỉ khoảng 600 px. Ở 720p và 1080p thì rõ, ở 4K sẽ hơi mềm. Cần chốt trước bản cuối: tìm bản quét lớn hơn, hoặc chấp nhận.
3. Ảnh chụp lấy khổ 2560 px để không làm nặng git. Ở 4K đủ cho khung chiếm khoảng 60% chiều cao.
4. **Bước 4 chưa làm:** phần xây dựng (giàn đỡ, đặt đá, tháo đỡ), "Walls of light" bằng ảnh kính màu thật, các sơ đồ còn tĩnh.
5. Âm lượng và chất lượng tiếng đá: agent không nghe được, cần chủ kênh nghe hai bản.
6. Vẫn chờ từ g-r3: duyệt claim, giọng `am_michael` cho dự án này, 6 mục phát âm.
