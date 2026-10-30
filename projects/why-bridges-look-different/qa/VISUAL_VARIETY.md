# Kiểm tra đa dạng hình ảnh (M7)

Sinh tự động bởi `tools/longform_reports.py`. Đây là số liệu cấu trúc; phần nhận xét của người xem nằm trong `qa/EDITORIAL_REVIEW_TIMECODED.md`.

- 47 shot, 641.5 s. Shot dài nhất 27.7 s; trung bình 13.6 s.

| Loại hình | Số shot | Thời lượng | Tỉ lệ |
|---|---|---|---|
| 3D_HOLD | 20 | 212.3 s | 33% |
| DIAGRAM | 8 | 150.8 s | 24% |
| PHOTO | 5 | 99.7 s | 16% |
| 3D_PUSH_IN | 4 | 67.5 s | 11% |
| 3D_EXPLODED_VIEW | 3 | 36.8 s | 6% |
| TITLE | 3 | 31.8 s | 5% |
| 3D_SIDE_BY_SIDE | 2 | 24.7 s | 4% |
| 3D_REPLACE_PARTS | 2 | 18.0 s | 3% |

- Đoạn 2D liên tục dài nhất: 4 shot, 79.9 s (kết thúc ở SC_037).

## Theo chương

| Chương | Bắt đầu | Dài | Shot | Loại hình |
|---|---|---|---|---|
| C1 Hook | 0:00 | 34 s | 5 | 3D_HOLD ×3, 3D_SIDE_BY_SIDE ×1, DIAGRAM ×1 |
| C2 The problem every bridge must solve | 0:33 | 49 s | 3 | 3D_HOLD ×3 |
| C3 The beam | 1:22 | 67 s | 6 | 3D_EXPLODED_VIEW ×1, 3D_HOLD ×3, 3D_PUSH_IN ×1, 3D_REPLACE_PARTS ×1 |
| C4 The arch | 2:28 | 82 s | 6 | 3D_EXPLODED_VIEW ×1, 3D_HOLD ×3, DIAGRAM ×2 |
| C5 The truss | 3:50 | 84 s | 6 | 3D_EXPLODED_VIEW ×1, 3D_HOLD ×4, 3D_REPLACE_PARTS ×1 |
| C6 Why different designs exist | 5:15 | 125 s | 9 | 3D_HOLD ×4, DIAGRAM ×3, PHOTO ×1, TITLE ×1 |
| C7 Real-world decisions | 7:20 | 127 s | 7 | 3D_PUSH_IN ×2, DIAGRAM ×1, PHOTO ×4 |
| C8 Why they look different | 9:27 | 74 s | 5 | 3D_PUSH_IN ×1, 3D_SIDE_BY_SIDE ×1, DIAGRAM ×1, TITLE ×2 |

## Từng shot

| Shot | Beat | Loại | Dài | Cắt |
|---|---|---|---|---|
| SC_001 | B01 | 3D_HOLD | 4.1 s | match |
| SC_002 | B01 | 3D_HOLD | 3.6 s | hard |
| SC_003 | B01 | 3D_HOLD | 3.8 s | hard |
| SC_004 | B01 | 3D_SIDE_BY_SIDE | 4.2 s | hard |
| SC_005 | B02 | DIAGRAM | 17.9 s | hard |
| SC_006 | B03 | 3D_HOLD | 15.6 s | hard |
| SC_007 | B04 | 3D_HOLD | 23.5 s | match |
| SC_008 | B05 | 3D_HOLD | 9.5 s | hard |
| SC_009 | B06 | 3D_REPLACE_PARTS | 9.4 s | match |
| SC_010 | B06 | 3D_HOLD | 4.8 s | match |
| SC_011 | B07 | 3D_HOLD | 4.5 s | match |
| SC_012 | B07 | 3D_EXPLODED_VIEW | 8.3 s | match |
| SC_013 | B08 | 3D_HOLD | 14.9 s | match |
| SC_014 | B09 | 3D_PUSH_IN | 24.9 s | match |
| SC_015 | B10 | 3D_HOLD | 3.8 s | hard |
| SC_016 | B10 | 3D_EXPLODED_VIEW | 6.8 s | hard |
| SC_017 | B11 | 3D_HOLD | 17.2 s | hard |
| SC_018 | B12 | 3D_HOLD | 14.6 s | hard |
| SC_019 | B13 | DIAGRAM | 17.2 s | hard |
| SC_020 | B14 | DIAGRAM | 22.3 s | hard |
| SC_021 | B15 | 3D_HOLD | 15.9 s | hard |
| SC_022 | B16 | 3D_HOLD | 14.6 s | hard |
| SC_023 | B17 | 3D_HOLD | 16.5 s | hard |
| SC_024 | B17 | 3D_REPLACE_PARTS | 8.6 s | match |
| SC_025 | B17 | 3D_HOLD | 7.1 s | match |
| SC_026 | B18 | 3D_EXPLODED_VIEW | 21.7 s | hard |
| SC_027 | B19 | TITLE | 14.4 s | hard |
| SC_028 | B20A | 3D_HOLD | 9.7 s | hard |
| SC_029 | B20B | 3D_HOLD | 15.9 s | hard |
| SC_030 | B20C | 3D_HOLD | 7.2 s | hard |
| SC_031 | B21 | PHOTO | 16.0 s | hard |
| SC_032 | B22 | DIAGRAM | 20.1 s | hard |
| SC_033 | B23 | 3D_HOLD | 5.5 s | hard |
| SC_034 | B23B | DIAGRAM | 17.7 s | hard |
| SC_035 | B24 | DIAGRAM | 18.7 s | hard |
| SC_036 | B25 | DIAGRAM | 20.4 s | hard |
| SC_037 | B26 | PHOTO | 23.1 s | hard |
| SC_038 | B27 | 3D_PUSH_IN | 10.1 s | hard |
| SC_039 | B28 | PHOTO | 19.8 s | hard |
| SC_040 | B29 | 3D_PUSH_IN | 12.5 s | hard |
| SC_041 | B30 | PHOTO | 27.7 s | hard |
| SC_042 | B31 | PHOTO | 13.1 s | hard |
| SC_043 | B32 | 3D_SIDE_BY_SIDE | 20.5 s | hard |
| SC_044 | B32B | TITLE | 8.7 s | hard |
| SC_045 | B33 | DIAGRAM | 16.5 s | hard |
| SC_046 | B34 | 3D_PUSH_IN | 20.0 s | hard |
| SC_047 | B35 | TITLE | 8.8 s | hard |

## Lặp lại, mật độ và kích thước mục tiêu

- Template theo số shot: HOLD ×24, MOTION_GRAPHICS ×16, EXPLODED_VIEW ×3, SIDE_BY_SIDE ×2, REPLACE_PARTS ×2
- Push-in: 4 shot (SC_014, SC_038, SC_040, SC_046), mỗi cái cách nhau ít nhất một chương, trừ B27/B29 (hai mô hình minh họa đứng cạnh ảnh thật).
- Cụm chú thích dày (≥ 3 chú thích hiện trong 1,5 s): không có
- Mục tiêu nhỏ hoặc bị che nhiều (diện tích thấy < 0,4% khung hoặc thấy < 35%): SC_011 stringer (visible area 0.0085, share 0.14); SC_011 cap_beam (visible area 0.0017, share 0.17); SC_015 arch_ring (visible area 0.0318, share 0.31); SC_017 arch_ring (visible area 0.0318, share 0.31); SC_028 arch_ring (visible area 0.0318, share 0.31)
- Tầm nhìn (planner L1): 18/20 dòng mục tiêu đạt, 2 tự sửa, 0 cần xem tay.

## Kiểm tra phim dài (pipeline/chapters.py)

- PASS `chapters_structure`: 8 chapters cover every beat contiguously, in order
- PASS `chapter_durations`: C1 34s, C2 49s, C3 67s, C4 82s, C5 84s, C6 125s, C7 127s, C8 74s
- PASS `runtime`: 10.69 min (15395 frames); acceptable 8-15 min
- PASS `no_duplicate_shots`: 47 unique shots
- WARN `no_repeated_sentences`: so why don't bridges all look the same?
- PASS `narration_sentences_complete`: 103 sentences scheduled, same text and order as narration.json
- PASS `audio_no_overlap`: no two beats' speech overlaps
- PASS `narration_silences`: longest gap 1.23s (limit 4.0s), after the last line 0.80s
- PASS `no_static_stretches`: longest stretch without a visual change 12.5s at 600.2s (limit 14.0s)
- PASS `visual_variety`: longest run of one visual kind: 3 x 3D_HOLD (limit 4); 3D_EXPLODED_VIEW 3, 3D_HOLD 20, 3D_PUSH_IN 4, 3D_REPLACE_PARTS 2, 3D_SIDE_BY_SIDE 2, DIAGRAM 8, PHOTO 5, TITLE 3
- PASS `no_repeated_visuals`: no two consecutive shots show the same picture
- PASS `chapter_openings`: chapters 2-8 open with a numbered title on their first shot
- PASS `annotations_consistent`: narration/visual consistency: no contradiction; 2 UNCERTAIN for the reviewer (B33.s2 SIDE, B34.s2 ARROWS); every annotation placed
- WARN `render_cache_current`: 47/47 shots not rendered or stale at review: SC_001, SC_002, SC_003, SC_004, SC_005, SC_006
- WARN `chapter_variety`: C2
- PASS `image_licences`: 4 external images, all approved with matching files
- PASS `image_attribution`: every external image is credited (credit card or description)
