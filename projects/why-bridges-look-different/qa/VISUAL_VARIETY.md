# Kiểm tra đa dạng hình ảnh: Why Bridges Don't All Look the Same

Sinh tự động bởi `tools/longform_reports.py`. Đây là số liệu cấu trúc; phần nhận xét của người xem nằm trong `qa/EDITORIAL_REVIEW_TIMECODED.md`.

- 63 shot, 867.6 s. Shot dài nhất 27.7 s; trung bình 13.8 s.

| Loại hình | Số shot | Thời lượng | Tỉ lệ |
|---|---|---|---|
| 3D_HOLD | 28 | 301.1 s | 35% |
| DIAGRAM | 9 | 183.9 s | 21% |
| PHOTO | 7 | 141.9 s | 16% |
| 3D_EXPLODED_VIEW | 6 | 75.5 s | 9% |
| 3D_PUSH_IN | 4 | 67.5 s | 8% |
| 3D_SIDE_BY_SIDE | 3 | 33.8 s | 4% |
| 3D_REPLACE_PARTS | 3 | 32.0 s | 4% |
| TITLE | 3 | 31.8 s | 4% |

- Đoạn 2D liên tục dài nhất: 5 shot, 98.2 s (kết thúc ở SC_052).

## Theo chương

| Chương | Bắt đầu | Dài | Shot | Loại hình |
|---|---|---|---|---|
| C1 Hook | 0:00 | 52 s | 8 | 3D_HOLD ×6, 3D_SIDE_BY_SIDE ×1, DIAGRAM ×1 |
| C2 The problem every bridge must solve | 0:52 | 49 s | 3 | 3D_HOLD ×3 |
| C3 The beam | 1:40 | 67 s | 6 | 3D_EXPLODED_VIEW ×1, 3D_HOLD ×3, 3D_PUSH_IN ×1, 3D_REPLACE_PARTS ×1 |
| C4 The arch | 2:47 | 82 s | 6 | 3D_EXPLODED_VIEW ×1, 3D_HOLD ×3, DIAGRAM ×2 |
| C5 The truss | 4:09 | 84 s | 6 | 3D_EXPLODED_VIEW ×1, 3D_HOLD ×4, 3D_REPLACE_PARTS ×1 |
| C6 The cantilever | 5:33 | 79 s | 5 | 3D_EXPLODED_VIEW ×1, 3D_HOLD ×2, 3D_REPLACE_PARTS ×1, PHOTO ×1 |
| C7 The suspension bridge | 6:52 | 62 s | 5 | 3D_EXPLODED_VIEW ×1, 3D_HOLD ×3, PHOTO ×1 |
| C8 The cable-stayed bridge | 7:55 | 74 s | 4 | 3D_EXPLODED_VIEW ×1, 3D_HOLD ×1, DIAGRAM ×2 |
| C9 Why different designs exist | 9:09 | 102 s | 7 | 3D_HOLD ×3, DIAGRAM ×2, PHOTO ×1, TITLE ×1 |
| C10 Real-world decisions | 10:51 | 127 s | 7 | 3D_PUSH_IN ×2, DIAGRAM ×1, PHOTO ×4 |
| C11 Why they look different | 12:57 | 90 s | 6 | 3D_PUSH_IN ×1, 3D_SIDE_BY_SIDE ×2, DIAGRAM ×1, TITLE ×2 |

## Từng shot

| Shot | Beat | Loại | Dài | Cắt |
|---|---|---|---|---|
| SC_001 | B01 | 3D_HOLD | 4.1 s | match |
| SC_002 | B01 | 3D_HOLD | 3.6 s | hard |
| SC_003 | B01 | 3D_HOLD | 3.8 s | hard |
| SC_004 | B01 | 3D_SIDE_BY_SIDE | 4.2 s | hard |
| SC_005 | B01B | 3D_HOLD | 8.5 s | hard |
| SC_006 | B01C | 3D_HOLD | 4.5 s | hard |
| SC_007 | B01D | 3D_HOLD | 4.6 s | hard |
| SC_008 | B02 | DIAGRAM | 19.0 s | hard |
| SC_009 | B03 | 3D_HOLD | 15.6 s | hard |
| SC_010 | B04 | 3D_HOLD | 23.5 s | match |
| SC_011 | B05 | 3D_HOLD | 9.5 s | hard |
| SC_012 | B06 | 3D_REPLACE_PARTS | 9.4 s | match |
| SC_013 | B06 | 3D_HOLD | 4.8 s | match |
| SC_014 | B07 | 3D_HOLD | 4.5 s | match |
| SC_015 | B07 | 3D_EXPLODED_VIEW | 8.3 s | match |
| SC_016 | B08 | 3D_HOLD | 14.9 s | match |
| SC_017 | B09 | 3D_PUSH_IN | 24.9 s | match |
| SC_018 | B10 | 3D_HOLD | 3.8 s | hard |
| SC_019 | B10 | 3D_EXPLODED_VIEW | 6.8 s | hard |
| SC_020 | B11 | 3D_HOLD | 17.2 s | hard |
| SC_021 | B12 | 3D_HOLD | 14.6 s | hard |
| SC_022 | B13 | DIAGRAM | 17.2 s | hard |
| SC_023 | B14 | DIAGRAM | 22.3 s | hard |
| SC_024 | B15 | 3D_HOLD | 15.9 s | hard |
| SC_025 | B16 | 3D_HOLD | 14.6 s | hard |
| SC_026 | B17 | 3D_HOLD | 16.5 s | hard |
| SC_027 | B17 | 3D_REPLACE_PARTS | 8.6 s | match |
| SC_028 | B17 | 3D_HOLD | 7.1 s | match |
| SC_029 | B18 | 3D_EXPLODED_VIEW | 21.7 s | hard |
| SC_030 | B40 | 3D_HOLD | 15.6 s | hard |
| SC_031 | B41 | 3D_REPLACE_PARTS | 14.0 s | match |
| SC_032 | B42 | 3D_HOLD | 15.1 s | hard |
| SC_033 | B43 | 3D_EXPLODED_VIEW | 14.8 s | hard |
| SC_034 | B44 | PHOTO | 19.2 s | hard |
| SC_035 | B45 | 3D_HOLD | 13.1 s | hard |
| SC_036 | B46 | 3D_HOLD | 13.3 s | match |
| SC_037 | B47 | 3D_HOLD | 5.9 s | match |
| SC_038 | B47 | 3D_EXPLODED_VIEW | 6.9 s | match |
| SC_039 | B48 | PHOTO | 23.1 s | hard |
| SC_040 | B50 | 3D_HOLD | 13.7 s | hard |
| SC_041 | B51 | DIAGRAM | 18.8 s | hard |
| SC_042 | B52 | 3D_EXPLODED_VIEW | 17.1 s | hard |
| SC_043 | B53 | DIAGRAM | 24.6 s | hard |
| SC_044 | B19 | TITLE | 14.4 s | hard |
| SC_045 | B20A | 3D_HOLD | 9.7 s | hard |
| SC_046 | B20B | 3D_HOLD | 15.9 s | hard |
| SC_047 | B20C | 3D_HOLD | 7.2 s | hard |
| SC_048 | B21 | PHOTO | 16.0 s | hard |
| SC_049 | B22 | DIAGRAM | 20.1 s | hard |
| SC_050 | B24 | DIAGRAM | 18.7 s | hard |
| SC_051 | B25 | DIAGRAM | 20.4 s | hard |
| SC_052 | B26 | PHOTO | 23.1 s | hard |
| SC_053 | B27 | 3D_PUSH_IN | 10.1 s | hard |
| SC_054 | B28 | PHOTO | 19.8 s | hard |
| SC_055 | B29 | 3D_PUSH_IN | 12.5 s | hard |
| SC_056 | B30 | PHOTO | 27.7 s | hard |
| SC_057 | B31 | PHOTO | 13.1 s | hard |
| SC_058 | B32 | 3D_SIDE_BY_SIDE | 20.5 s | hard |
| SC_059 | B32L | 3D_SIDE_BY_SIDE | 9.1 s | hard |
| SC_060 | B32B | TITLE | 8.7 s | hard |
| SC_061 | B33 | DIAGRAM | 22.8 s | hard |
| SC_062 | B34 | 3D_PUSH_IN | 20.0 s | hard |
| SC_063 | B35 | TITLE | 8.8 s | hard |

## Lặp lại, mật độ và kích thước mục tiêu

- Template theo số shot: HOLD ×32, MOTION_GRAPHICS ×19, EXPLODED_VIEW ×6, SIDE_BY_SIDE ×3, REPLACE_PARTS ×3
- Push-in: 4 shot (SC_017, SC_053, SC_055, SC_062), mỗi cái cách nhau ít nhất một chương, trừ B27/B29 (hai mô hình minh họa đứng cạnh ảnh thật).
- Cụm chú thích dày (≥ 3 chú thích hiện trong 1,5 s): không có
- Mục tiêu nhỏ hoặc bị che nhiều (diện tích thấy < 0,4% khung hoặc thấy < 35%): SC_014 stringer (visible area 0.0085, share 0.14); SC_014 cap_beam (visible area 0.0017, share 0.17); SC_018 arch_ring (visible area 0.0318, share 0.31); SC_020 arch_ring (visible area 0.0318, share 0.31); SC_035 hanger (visible area 0.0036, share 0.87); SC_045 arch_ring (visible area 0.0318, share 0.31)
- Tầm nhìn (planner L1): 25/27 dòng mục tiêu đạt, 2 tự sửa, 0 cần xem tay.

## Kiểm tra phim dài (pipeline/chapters.py)

- PASS `chapters_structure`: 11 chapters cover every beat contiguously, in order
- PASS `chapter_durations`: C1 52s, C2 49s, C3 67s, C4 82s, C5 84s, C6 79s, C7 62s, C8 74s, C9 102s, C10 127s, C11 90s
- PASS `runtime`: 14.46 min (20823 frames); acceptable 8-15 min
- PASS `no_duplicate_shots`: 63 unique shots
- WARN `no_repeated_sentences`: so why don't bridges all look the same?
- PASS `narration_sentences_complete`: 133 sentences scheduled, same text and order as narration.json
- PASS `audio_no_overlap`: no two beats' speech overlaps
- PASS `narration_silences`: longest gap 1.23s (limit 4.0s), after the last line 0.80s
- PASS `no_static_stretches`: longest stretch without a visual change 12.4s at 527.0s (limit 14.0s)
- PASS `visual_variety`: longest run of one visual kind: 3 x 3D_HOLD (limit 4); 3D_EXPLODED_VIEW 6, 3D_HOLD 28, 3D_PUSH_IN 4, 3D_REPLACE_PARTS 3, 3D_SIDE_BY_SIDE 3, DIAGRAM 9, PHOTO 7, TITLE 3
- PASS `no_repeated_visuals`: no two consecutive shots show the same picture
- PASS `chapter_openings`: chapters 2-11 open with a numbered title on their first shot
- PASS `annotations_consistent`: narration/visual consistency: no contradiction; 2 UNCERTAIN for the reviewer (B33.s3 SIDE, B34.s2 ARROWS); every annotation placed
- WARN `render_cache_current`: 63/63 shots not rendered or stale at review: SC_001, SC_002, SC_003, SC_004, SC_005, SC_006
- WARN `chapter_variety`: C2
- PASS `image_licences`: 6 external images, all approved with matching files
- PASS `image_attribution`: every external image is credited (credit card or description)
