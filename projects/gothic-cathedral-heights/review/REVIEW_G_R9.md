# Vòng g-r9: sửa cục bộ sau review g-r8

- **Theo review g-r8 của chủ kênh** (2026-11-07; chứng cứ trong `qa/codex_gr8_review_20261107/REVIEW.md`): giữ hướng hình, sửa bốn chỗ, sinh lại manifest chương, rồi ghép bản xem trước toàn phim.
- **Trạng thái:** INTERNAL REVIEW, chưa có gì được duyệt. Lời dẫn và timing giữ nguyên như g-r3. Thêm một nguồn và một claim (CLM_165), chỉ cho chú thích trên hình.
- **File để duyệt** (trong `output/`, ngoài git):
  - `chapters_internal_720p/gothic_cathedral_heights_C3_documentary_INTERNAL_REVIEW.mp4`: B09;
  - `chapters_internal_720p/gothic_cathedral_heights_C6_documentary_INTERNAL_REVIEW.mp4`: B21, B22;
  - `chapters_internal_720p/gothic_cathedral_heights_C7_documentary_INTERNAL_REVIEW.mp4`: B25, B29;
  - **bản ghép toàn phim:** `gothic_cathedral_heights_G_R9_INTERNAL_REVIEW_720p.mp4` (+ `.en.srt`), 15:23.
- **Mốc trong bản ghép:** B09 2:42, B21 7:02, B22 7:26, B25 8:06, B29 9:19. Tính từ đầu chương: B09 ở C3 00:32, B21 ở C6 00:00, B25 ở C7 00:00, B29 ở C7 01:12.

## Theo từng góp ý

| # | Góp ý | Đã làm |
|---|---|---|
| 1 | C6 00:08–00:23: ảnh phần trên dàn hợp xướng (dựng lại từ 1231) đi cùng lời kể về Suger 1140–1144 | **Đổi ảnh.** Atlas du patrimoine de la Seine-Saint-Denis (Michaël Wyss) xác nhận đợt thế kỷ 13 giữ lại *double déambulatoire* và vòm của nó, và dựng lại phần trên. Ảnh mới là **ambulatory của Suger** (NateBergin, CC BY 4.0): cột đơn khối, vòm nhọn, vòm gân, cửa sổ nhà nguyện. Ảnh cửa sổ hoa hồng (ý mở đầu về ánh sáng, "Saint-Denis today") **chuyển hoà** sang ambulatory ở đầu câu về Suger, đúng khung, không giật camera. Rồi camera nghiêng từ cột lên vòm. Chú thích: "The ambulatory of Suger's choir, 1140–1144" và "Upper choir rebuilt in the 13th century". Chú thích **giữ qua lúc chuyển sang B22** ("Saint-Denis today: Suger's ambulatory"). B22 cũng chuyển sang ảnh này: camera đi từ khung cuối của B21 xuống ánh sáng cửa sổ nhà nguyện. Ảnh apse của Ninaras bỏ hẳn (khỏi phim, manifest và mô tả). Nguồn mới và claim CLM_165 đã kiểm nguyên văn. Lời dẫn không đổi. |
| 2 | C6 ~00:19: chấm của "Every vault ribbed" nằm trên mảng đá giữa các gân | Nhãn đổi thành **"Vault rib"**, chấm vào **một gân rõ** (gân chạy xuống đầu cột), tọa độ đo trên ảnh gốc 1:1. Khi đọc "ribbed", gân đó được **vẽ sáng dọc chiều dài** khoảng 1,6 giây rồi tắt. "Pointed arch" chấm gần đỉnh một vòm nhọn; "Stained glass" chấm vào cửa sổ có các ô tròn. |
| 3 | C7/B29 01:12–01:24: vẫn là toàn mô hình, zoom nhẹ | **Đổi thành SEQUENCE như B17.** Mở bằng toàn mặt cắt. Khi đọc "little room", **một trụ chống bay, trụ chống và tháp nhọn của nó sáng lên** ngay trên cả nhà thờ. Khi đọc "error", phần còn lại mờ đi (các hệ trụ phía sau ẩn hẳn, để không chồng thành vệt), camera **tiến vào chỗ flyer chạm đỉnh trụ chống**. Rồi theo lời: vòm cao sáng ("thrust") và đường lực vẽ vào đầu flyer; flyer sáng ("arch"); trụ chống sáng ("buttress") và đường lực đi tiếp tới đỉnh trụ; nhãn **"Lined up with its buttress"** ("supports"). Đường lực vẫn ghi "Conceptual load path — not to scale". Không thêm chi tiết hay hiệu ứng phá hủy. |
| 4a | C3/B09 00:32–00:46: gần 14 giây chỉ có tên và câu trích | Hai gối và đường nối **có từ khung đầu**. **Dây treo được vẽ khi nói tên Hooke** (khoảng giây thứ 4). Câu trích hiện bên phải khi được đọc và ở lại tới cuối. Quả nặng thêm vào ở "weights"; **thao tác lật vẫn đúng chữ "turn"**. Sơ đồ lớn hơn trước (nhịp 0,56). |
| 4b | C7/B25 00:00–00:08: chỉ có chữ và một đường chân vòm | **Mở cận thao tác compa từ giây đầu:** mũi compa đặt lên chân phải, cánh tay mở bằng nhịp quay từ chân trái lên đỉnh trong lúc cung trái được vẽ theo; rồi đổi chân cho cung phải. Hai cánh tay dừng ở đỉnh thành tam giác đều (bán kính bằng nhịp, ghi "One example: the radius equals the span"). Camera đẩy rất chậm khi nói "geometrical rules", rồi **lùi ra ở "scaled"** cho hai bản lớn hơn, nét dày theo đúng tỉ lệ. |
| — | Manifest chương còn mapping shot cũ | Sinh lại `chapters/chapter_manifest.json` và `qa/longform_qa.json` bằng `chapters --preset internal_720p` theo plan hiện tại (B18 một shot, SC_n = Bn từ B18 trở đi). `external_assets` của từng chương nay lấy từ các card đang dùng. |

## Kiểm tra

- **Blender QA:**
  - 44/44 cho 5 shot đã sửa (SC_009, SC_021, SC_022, SC_025, SC_029);
  - 407/407 cho cả 46 shot trước khi render chương.
- **Chương:** render lại C1, C4, C8, C9, C10 (do mã shot đánh số lại và engine đổi từ g-r8), cùng các shot đã sửa ở C3, C6, C7. C2 và C5 dùng lại file trước. Âm lượng mọi chương −16,3 đến −16,5 LUFS.
  - C3: 1:46,5.
  - C6: 1:03,75.
  - C7: 1:37,25.
- **Bản ghép toàn phim:** ghép từ 10 file chương, không mã hoá lại hình. 22.162 khung (923,4 s), −16,4 LUFS, true peak −1,2 dBTP, 214 dòng phụ đề. 0 lỗi giải mã, 0 đoạn đen, 9 điểm nối chương đều đạt.
- **Rà khung hình từ chính MP4 ghép:** B09, B21, B22, B25, B29, và các điểm cắt B20→B21, B21→B22 (cùng khung hình), B28→B29, B29→B30.
  - Chấm "Vault rib", "Pointed arch" và "Stained glass" nằm đúng bộ phận ở khung 1280×720.
  - Thao tác compa chạy đồng bộ với cung.
- **Manifest chương:** sinh lại, mã shot khớp storyboard hiện tại. Long-form QA:
  - `image_licences` PASS (13 ảnh ngoài, hồ sơ và SHA256 khớp);
  - `image_attribution` PASS;
  - **`visual_variety` FAIL**: 8 shot ảnh hoặc bản vẽ liền nhau (B31–B38, cả chương 8), ngưỡng là 4;
  - `chapter_variety` WARN: C1, C3, C8.
  - Lỗi `visual_variety` có từ khi chương 8 được dựng lại bằng ảnh và bản vẽ (g-r5/g-r6), nhưng tới vòng này manifest mới được sinh lại nên mới hiện ra. Agent **không đổi ngưỡng**. Vì vậy `episode.py status` để EDITORIAL_QA ở TODO. Xem mục "Cần chủ kênh quyết".
- **Công cụ:** `final-assemble` với preset nội bộ từng đặt tên `…_FINAL_720p_INTERNAL_REVIEW.mp4` và một file trung gian `…_FINAL_720p_video.mp4`. Điều này trái quy tắc "chưa duyệt thì không có file nào tên FINAL"; một test đã bắt được. Đã sửa: bản ghép nội bộ đặt tên theo `review_label` trong `project.json` (nay `G_R9_INTERNAL_REVIEW`), như lệnh `assemble`. Các file tên FINAL đã xoá. Có thêm test.
- **Test:** 406/406 (thêm 5 test cho các sửa của vòng này và 1 test cho tên file). Đánh giá planner 30/30.

## Cần chủ kênh quyết

- **Chương 8 và ngưỡng đa dạng hình (tối đa 4 shot cùng loại liền nhau).** Chương 8 nay là 8 card ảnh hoặc bản vẽ liền nhau, theo hướng chủ kênh chọn ở g-r5/g-r6. Hai cách:
  1. Giữ nguyên chương 8 và chủ kênh ghi rõ chấp nhận ngoại lệ này (agent không tự miễn một kiểm tra).
  2. Đổi hai beat sang loại hình khác để chia chuỗi. Ví dụ B33 (so độ cao Beauvais–Amiens) thành sơ đồ độ cao vẽ động, và B36 (trụ mới chia 3 khoang thành 6) thành mặt bằng sơ đồ vẽ dần. Chuỗi dài nhất khi đó còn 2.

## Còn lại

- **Ảnh ambulatory** rộng 2160 px. Ở 720p là 1:1 hoặc tốt hơn; ở 4K sẽ mềm khi phủ kín khung (giống ảnh Durham 1273 px). Cần quyết trước bản cuối.
- **Tùy chọn chủ kênh nêu, chưa làm:** góc xiên cho B06 để thấy độ dày tường; nhắc lại ảnh hoặc đồ họa trong phần tổng kết trước CTA ở C10.
- Vẫn chờ từ g-r3: duyệt claim (nay 54 claim trong phim), giọng `am_michael`, 6 mục phát âm, nghe tiếng đá, duyệt ảnh và ghi công.
