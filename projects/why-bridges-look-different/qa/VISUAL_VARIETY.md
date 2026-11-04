# Kiểm tra đa dạng hình ảnh: Why Bridges Don't All Look the Same

Sinh tự động bởi `tools/longform_reports.py`. Đây là số liệu cấu trúc; phần nhận xét của người xem nằm trong `qa/EDITORIAL_REVIEW_TIMECODED.md`.

- 75 shot, 1193.8 s. Shot dài nhất 44.4 s; trung bình 15.9 s.

| Loại hình | Số shot | Thời lượng | Tỉ lệ |
|---|---|---|---|
| 3D_HOLD | 33 | 421.2 s | 35% |
| DIAGRAM | 12 | 297.7 s | 25% |
| PHOTO | 8 | 160.1 s | 13% |
| 3D_PUSH_IN | 7 | 141.5 s | 12% |
| 3D_EXPLODED_VIEW | 6 | 75.5 s | 6% |
| 3D_SIDE_BY_SIDE | 3 | 33.8 s | 3% |
| 3D_REPLACE_PARTS | 3 | 32.0 s | 3% |
| TITLE | 3 | 31.8 s | 3% |

- Đoạn 2D liên tục dài nhất: 4 shot, 93.1 s (kết thúc ở SC_060).

## Theo chương

| Chương | Bắt đầu | Dài | Shot | Loại hình |
|---|---|---|---|---|
| C1 Hook | 0:00 | 52 s | 8 | 3D_HOLD ×6, 3D_SIDE_BY_SIDE ×1, DIAGRAM ×1 |
| C2 The problem every bridge must solve | 0:52 | 49 s | 3 | 3D_HOLD ×3 |
| C3 The beam | 1:41 | 70 s | 6 | 3D_EXPLODED_VIEW ×1, 3D_HOLD ×3, 3D_PUSH_IN ×1, 3D_REPLACE_PARTS ×1 |
| C4 The arch | 2:50 | 82 s | 6 | 3D_EXPLODED_VIEW ×1, 3D_HOLD ×3, DIAGRAM ×2 |
| C5 The truss | 4:12 | 84 s | 6 | 3D_EXPLODED_VIEW ×1, 3D_HOLD ×4, 3D_REPLACE_PARTS ×1 |
| C6 The cantilever | 5:37 | 88 s | 5 | 3D_EXPLODED_VIEW ×1, 3D_HOLD ×2, 3D_REPLACE_PARTS ×1, PHOTO ×1 |
| C7 The suspension bridge | 7:05 | 59 s | 5 | 3D_EXPLODED_VIEW ×1, 3D_HOLD ×3, PHOTO ×1 |
| C8 The cable-stayed bridge | 8:04 | 78 s | 4 | 3D_EXPLODED_VIEW ×1, 3D_HOLD ×1, DIAGRAM ×2 |
| C9 Why different designs exist | 9:22 | 172 s | 10 | 3D_HOLD ×6, DIAGRAM ×2, PHOTO ×1, TITLE ×1 |
| C10 Span, cost and time | 12:15 | 129 s | 5 | 3D_HOLD ×1, 3D_PUSH_IN ×1, DIAGRAM ×3 |
| C11 Real-world decisions | 14:23 | 226 s | 11 | 3D_HOLD ×1, 3D_PUSH_IN ×4, DIAGRAM ×1, PHOTO ×5 |
| C12 Why they look different | 18:10 | 104 s | 6 | 3D_PUSH_IN ×1, 3D_SIDE_BY_SIDE ×2, DIAGRAM ×1, TITLE ×2 |

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
| SC_009 | B03 | 3D_HOLD | 15.7 s | hard |
| SC_010 | B04 | 3D_HOLD | 23.5 s | match |
| SC_011 | B05 | 3D_HOLD | 9.5 s | hard |
| SC_012 | B06 | 3D_REPLACE_PARTS | 9.4 s | match |
| SC_013 | B06 | 3D_HOLD | 4.8 s | match |
| SC_014 | B07 | 3D_HOLD | 4.5 s | match |
| SC_015 | B07 | 3D_EXPLODED_VIEW | 8.3 s | match |
| SC_016 | B08 | 3D_HOLD | 14.9 s | match |
| SC_017 | B09 | 3D_PUSH_IN | 28.0 s | match |
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
| SC_030 | B40 | 3D_HOLD | 15.9 s | hard |
| SC_031 | B41 | 3D_REPLACE_PARTS | 14.0 s | match |
| SC_032 | B42 | 3D_HOLD | 15.1 s | hard |
| SC_033 | B43 | 3D_EXPLODED_VIEW | 14.8 s | hard |
| SC_034 | B44 | PHOTO | 28.6 s | hard |
| SC_035 | B45 | 3D_HOLD | 13.1 s | hard |
| SC_036 | B46 | 3D_HOLD | 13.3 s | match |
| SC_037 | B47 | 3D_HOLD | 5.9 s | match |
| SC_038 | B47 | 3D_EXPLODED_VIEW | 6.9 s | match |
| SC_039 | B48 | PHOTO | 19.7 s | hard |
| SC_040 | B50 | 3D_HOLD | 13.7 s | hard |
| SC_041 | B51 | DIAGRAM | 22.6 s | hard |
| SC_042 | B52 | 3D_EXPLODED_VIEW | 17.1 s | hard |
| SC_043 | B53 | DIAGRAM | 24.6 s | hard |
| SC_044 | B19 | TITLE | 14.4 s | hard |
| SC_045 | B20A | 3D_HOLD | 9.7 s | hard |
| SC_046 | B20B | 3D_HOLD | 15.9 s | hard |
| SC_047 | B20C | 3D_HOLD | 7.2 s | hard |
| SC_048 | B21 | PHOTO | 16.0 s | hard |
| SC_049 | B20E | 3D_HOLD | 27.0 s | hard |
| SC_050 | B22 | DIAGRAM | 20.1 s | hard |
| SC_051 | B22B | DIAGRAM | 20.7 s | hard |
| SC_052 | B22C | 3D_HOLD | 20.0 s | hard |
| SC_053 | B22D | 3D_HOLD | 21.5 s | hard |
| SC_054 | B23C | DIAGRAM | 44.4 s | hard |
| SC_055 | B23D | 3D_HOLD | 21.5 s | hard |
| SC_056 | B23E | 3D_PUSH_IN | 13.1 s | hard |
| SC_057 | B24 | DIAGRAM | 18.7 s | hard |
| SC_058 | B24B | DIAGRAM | 31.0 s | hard |
| SC_059 | B25 | DIAGRAM | 20.4 s | hard |
| SC_060 | B26 | PHOTO | 23.1 s | hard |
| SC_061 | B27 | 3D_PUSH_IN | 10.1 s | hard |
| SC_062 | B28 | PHOTO | 19.6 s | hard |
| SC_063 | B29 | 3D_PUSH_IN | 12.5 s | hard |
| SC_064 | B30 | PHOTO | 27.7 s | hard |
| SC_065 | B31 | PHOTO | 13.1 s | hard |
| SC_066 | B31A | 3D_PUSH_IN | 29.8 s | hard |
| SC_067 | B31B | 3D_HOLD | 29.8 s | hard |
| SC_068 | B31C | PHOTO | 12.2 s | hard |
| SC_069 | B31D | 3D_PUSH_IN | 28.1 s | hard |
| SC_070 | B32 | 3D_SIDE_BY_SIDE | 20.5 s | hard |
| SC_071 | B32L | 3D_SIDE_BY_SIDE | 9.1 s | hard |
| SC_072 | B32B | TITLE | 8.7 s | hard |
| SC_073 | B33 | DIAGRAM | 36.8 s | hard |
| SC_074 | B34 | 3D_PUSH_IN | 20.0 s | hard |
| SC_075 | B35 | TITLE | 8.8 s | hard |

## Lặp lại, mật độ và kích thước mục tiêu

- Template theo số shot: HOLD ×40, MOTION_GRAPHICS ×23, EXPLODED_VIEW ×6, SIDE_BY_SIDE ×3, REPLACE_PARTS ×3
- Push-in: 7 shot (SC_017, SC_056, SC_061, SC_063, SC_066, SC_069, SC_074), mỗi cái cách nhau ít nhất một chương, trừ B27/B29 (hai mô hình minh họa đứng cạnh ảnh thật).
- Cụm chú thích dày (≥ 3 chú thích hiện trong 1,5 s): không có
- Mục tiêu nhỏ hoặc bị che nhiều (diện tích thấy < 0,4% khung hoặc thấy < 35%): SC_014 stringer (visible area 0.0085, share 0.14); SC_014 cap_beam (visible area 0.0017, share 0.17); SC_018 arch_ring (visible area 0.0318, share 0.31); SC_020 arch_ring (visible area 0.0318, share 0.31); SC_035 hanger (visible area 0.0036, share 0.87); SC_045 arch_ring (visible area 0.0318, share 0.31)
- Tầm nhìn (planner L1): 30/32 dòng mục tiêu đạt, 2 tự sửa, 0 cần xem tay.

## Kiểm tra phim dài (pipeline/chapters.py)

- PASS `chapters_structure`: 12 chapters cover every beat contiguously, in order
- PASS `chapter_durations`: C1 52s, C2 49s, C3 70s, C4 82s, C5 84s, C6 88s, C7 59s, C8 78s, C9 172s, C10 129s, C11 226s, C12 104s
- PASS `runtime`: 19.90 min (28651 frames); acceptable 8-20 min (owner decision, Tran Nam Anh (channel owner), 2026-11-03)
- PASS `no_duplicate_shots`: 75 unique shots
- WARN `no_repeated_sentences`: so why don't bridges all look the same?
- PASS `narration_sentences_complete`: 169 sentences scheduled, same text and order as narration.json
- PASS `audio_no_overlap`: no two beats' speech overlaps
- PASS `narration_silences`: longest gap 1.23s (limit 4.0s), after the last line 0.80s
- PASS `no_static_stretches`: longest stretch without a visual change 13.5s at 629.8s (limit 14.0s)
- PASS `visual_variety`: longest run of one visual kind: 3 x 3D_HOLD (limit 4); 3D_EXPLODED_VIEW 6, 3D_HOLD 33, 3D_PUSH_IN 7, 3D_REPLACE_PARTS 3, 3D_SIDE_BY_SIDE 3, DIAGRAM 12, PHOTO 8, TITLE 3
- PASS `no_repeated_visuals`: no two consecutive shots show the same picture
- PASS `chapter_openings`: chapters 2-12 open with a numbered title on their first shot
- PASS `annotations_consistent`: narration/visual consistency: no contradiction; 2 UNCERTAIN for the reviewer (B33.s4 SIDE, B34.s2 ARROWS); every annotation placed
- WARN `render_cache_current`: 75/75 shots not rendered or stale at review: SC_001, SC_002, SC_003, SC_004, SC_005, SC_006
- WARN `chapter_variety`: C2
- PASS `image_licences`: 7 external images, all approved with matching files
- PASS `image_attribution`: every external image is credited (credit card or description)
