# Kiểm tra đa dạng hình ảnh: Could We Build an Entire City That Floats?

Sinh tự động bởi `tools/longform_reports.py`. Đây là số liệu cấu trúc; phần nhận xét của người xem nằm trong `qa/EDITORIAL_REVIEW_TIMECODED.md`.

- 44 shot, 784.2 s. Shot dài nhất 34.0 s; trung bình 17.8 s.

| Loại hình | Số shot | Thời lượng | Tỉ lệ |
|---|---|---|---|
| 3D_SEQUENCE | 27 | 450.3 s | 57% |
| DIAGRAM | 16 | 326.9 s | 42% |
| TITLE | 1 | 6.9 s | 1% |

- Đoạn 2D liên tục dài nhất: 2 shot, 59.2 s (kết thúc ở SC_016).

## Theo chương

| Chương | Bắt đầu | Dài | Shot | Loại hình |
|---|---|---|---|---|
| C1 Could We Actually Do This? | 0:00 | 64 s | 4 | 3D_SEQUENCE ×3, DIAGRAM ×1 |
| C2 The First Problem: Making Buildings Float | 1:04 | 137 s | 7 | 3D_SEQUENCE ×6, DIAGRAM ×1 |
| C3 Why One Platform Isn't a City | 3:20 | 133 s | 5 | 3D_SEQUENCE ×3, DIAGRAM ×2 |
| C4 The Water Never Stays Still | 5:33 | 89 s | 5 | 3D_SEQUENCE ×2, DIAGRAM ×3 |
| C5 Keeping the City in Place | 7:02 | 54 s | 3 | 3D_SEQUENCE ×2, DIAGRAM ×1 |
| C6 A City Needs More Than Buildings | 7:56 | 71 s | 4 | 3D_SEQUENCE ×3, DIAGRAM ×1 |
| C7 What Would Actually Make This Difficult? | 9:07 | 153 s | 9 | 3D_SEQUENCE ×6, DIAGRAM ×3 |
| C8 Could We Really Build It? | 11:41 | 83 s | 7 | 3D_SEQUENCE ×2, DIAGRAM ×4, TITLE ×1 |

## Từng shot

| Shot | Beat | Loại | Dài | Cắt |
|---|---|---|---|---|
| SC_001 | B01 | 3D_SEQUENCE | 11.0 s | match |
| SC_002 | B02 | 3D_SEQUENCE | 13.2 s | match |
| SC_003 | B03 | DIAGRAM | 32.5 s | hard |
| SC_004 | B04 | 3D_SEQUENCE | 7.5 s | hard |
| SC_005 | B05 | 3D_SEQUENCE | 20.8 s | hard |
| SC_006 | B06 | 3D_SEQUENCE | 15.2 s | hard |
| SC_007 | B07 | DIAGRAM | 23.4 s | hard |
| SC_008 | B08 | 3D_SEQUENCE | 20.8 s | hard |
| SC_009 | B09 | 3D_SEQUENCE | 15.5 s | match |
| SC_010 | B10 | 3D_SEQUENCE | 19.3 s | match |
| SC_011 | B11 | 3D_SEQUENCE | 21.7 s | hard |
| SC_012 | B12 | 3D_SEQUENCE | 15.4 s | hard |
| SC_013 | B13 | 3D_SEQUENCE | 30.8 s | hard |
| SC_014 | B14 | 3D_SEQUENCE | 27.3 s | hard |
| SC_015 | B15 | DIAGRAM | 25.2 s | hard |
| SC_016 | B16 | DIAGRAM | 34.0 s | hard |
| SC_017 | B17 | 3D_SEQUENCE | 12.1 s | hard |
| SC_018 | B18 | DIAGRAM | 15.7 s | hard |
| SC_019 | B19 | DIAGRAM | 10.4 s | hard |
| SC_020 | B20 | DIAGRAM | 21.7 s | hard |
| SC_021 | B21 | 3D_SEQUENCE | 29.3 s | hard |
| SC_022 | B22 | 3D_SEQUENCE | 11.4 s | hard |
| SC_023 | B23 | DIAGRAM | 25.3 s | hard |
| SC_024 | B24 | 3D_SEQUENCE | 17.3 s | hard |
| SC_025 | B25 | 3D_SEQUENCE | 9.9 s | hard |
| SC_026 | B26 | DIAGRAM | 17.3 s | hard |
| SC_027 | B27 | 3D_SEQUENCE | 25.3 s | hard |
| SC_028 | B28 | 3D_SEQUENCE | 18.4 s | hard |
| SC_029 | B29 | 3D_SEQUENCE | 9.2 s | hard |
| SC_030 | B30 | 3D_SEQUENCE | 14.0 s | hard |
| SC_031 | B31 | 3D_SEQUENCE | 10.9 s | hard |
| SC_032 | B32 | DIAGRAM | 20.7 s | hard |
| SC_033 | B33 | 3D_SEQUENCE | 18.8 s | hard |
| SC_034 | B34 | 3D_SEQUENCE | 18.6 s | hard |
| SC_035 | B35 | 3D_SEQUENCE | 17.2 s | hard |
| SC_036 | B36 | DIAGRAM | 16.2 s | hard |
| SC_037 | B37 | DIAGRAM | 28.0 s | hard |
| SC_038 | B38 | 3D_SEQUENCE | 7.6 s | hard |
| SC_039 | B39 | DIAGRAM | 11.4 s | hard |
| SC_040 | B40 | DIAGRAM | 24.5 s | hard |
| SC_041 | B41 | DIAGRAM | 8.6 s | hard |
| SC_042 | B42 | 3D_SEQUENCE | 11.9 s | hard |
| SC_043 | B43 | DIAGRAM | 12.0 s | hard |
| SC_044 | B44 | TITLE | 6.9 s | hard |

## Lặp lại, mật độ và kích thước mục tiêu

- Template theo số shot: SEQUENCE ×27, MOTION_GRAPHICS ×17
- Push-in: 0 shot (), mỗi cái cách nhau ít nhất một chương, trừ B27/B29 (hai mô hình minh họa đứng cạnh ảnh thật).
- Cụm chú thích dày (≥ 3 chú thích hiện trong 1,5 s): SC_033 @10:06
- Mục tiêu nhỏ hoặc bị che nhiều (diện tích thấy < 0,4% khung hoặc thấy < 35%): không có
- Tầm nhìn (planner L1): 0/0 dòng mục tiêu đạt, 0 tự sửa, 0 cần xem tay.

## Kiểm tra phim dài (pipeline/chapters.py)

- PASS `chapters_structure`: 8 chapters cover every beat contiguously, in order
- PASS `chapter_durations`: C1 64s, C2 137s, C3 133s, C4 89s, C5 54s, C6 71s, C7 153s, C8 83s
- PASS `runtime`: 13.07 min (18820 frames); acceptable 8-15 min
- PASS `no_duplicate_shots`: 44 unique shots
- PASS `no_repeated_sentences`: 126 sentences, none repeated verbatim
- PASS `narration_sentences_complete`: 126 sentences scheduled, same text and order as narration.json
- PASS `audio_no_overlap`: no two beats' speech overlaps
- PASS `narration_silences`: longest gap 1.23s (limit 4.0s), after the last line 0.82s
- PASS `no_static_stretches`: longest stretch without a visual change 12.4s at 188.5s (limit 14.0s)
- PASS `visual_variety`: longest run of one visual kind: 7 x 3D_SEQUENCE (limit 4); owner exception for SC_008-SC_014 (7 x 3D_SEQUENCE), SC_027-SC_031 (5 x 3D_SEQUENCE), Tran Nam Anh (channel owner), 2026-11-12; 3D_SEQUENCE 27, DIAGRAM 16, TITLE 1
- PASS `no_repeated_visuals`: no two consecutive shots show the same picture
- PASS `chapter_openings`: chapters 2-8 open with a numbered title on their first shot
- PASS `annotations_consistent`: narration/visual consistency: no contradiction; 2 UNCERTAIN for the reviewer (B31.s1 TRANSFORMATION, B40.s0 SIDE); every annotation placed
- PASS `render_cache_current`: all 44 shots rendered at internal_720p with current cache keys
- PASS `chapter_variety`: every multi-shot chapter mixes at least two visual kinds
- PASS `image_licences`: 0 external images, all approved with matching files
- PASS `image_attribution`: every external image is credited (credit card or description)
