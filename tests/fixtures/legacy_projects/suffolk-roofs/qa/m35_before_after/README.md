# Ảnh trước/sau M3.5

"Trước" là khung của M3: tag `m3-pilot-preview`, bản sao trong `qa/baseline_m3/stills_review/`, render ở 960×540. "Sau" là khung M3.5 trong `output/stills_review/`, cũng 960×540. Ảnh không có chữ chú thích vì bản FFmpeg trên máy không có `drawtext`.

| File | Bố cục | Cho thấy điều gì |
|---|---|---|
| `06_comparison_960_before_after.png` | trên: M3 · dưới: M3.5 | Hoa văn viên ngói/slate, nhãn có độ dốc, không còn vệt trắng trên mái slate |
| `05_tile_slate_960_before_after.png` | trên: M3 SC_005 (một nhà, đang thay ngói bằng slate) · dưới: M3.5 SC_005 (hai công trình đặt cạnh nhau, có nhãn) | Đã bỏ hình ảnh gợi ý trình tự tuyến tính |
| `06_small_screen_480_before_after.png` | trái: M3 · phải: M3.5, cả hai thu nhỏ còn 480 px | Độ dễ đọc trên màn hình nhỏ: ngói và slate phân biệt được bằng hoa văn và nhãn, không chỉ bằng màu |
| `tile_slate_detail_zoom_before_after.png` | trái: M3 · phải: M3.5 (crop phóng to 2 lần) | Hàng ngói (viên nhỏ) so với hàng slate (viên lớn hơn khoảng 2 lần) |
| `slate_poke_through_before_after.png` | trái: M3 · phải: M3.5 (crop mái slate) | Đỉnh tường hồi và đỉnh tường dọc xuyên qua mái slate mỏng (M3), đã sửa (M3.5) |

Ảnh tĩnh 1920×1080 (preset `production_test`, chỉ render ảnh tĩnh) nằm ở `output/stills_production_test/`.
