# Render 4K bản cuối: hiệu năng và kiểm chứng (2026-10-30/31)

**Phim:** `why-bridges-look-different`, preset `final_4k`: 3840×2160, 24 fps, EEVEE, PNG 8-bit sRGB → H.264 High, CRF 16, x264 `slow`, BT.709 limited range; AAC.

**Máy:** Mac Apple Silicon, Blender 5.2 chạy nền, mỗi lúc một Blender, `caffeinate -is` cho từng tiến trình.

Số liệu lấy từ log thật: `projects/why-bridges-look-different/qa/perf/`.
- `chapter_C*_final_4k.log`, `final_assemble_4k.log`: chạy dưới `/usr/bin/time -l`.
- `frame_times_final_4k.json`: mốc `Saved:` của Blender.
- `final_4k_wall.txt`: thời điểm bắt đầu và kết thúc.

## 1. Benchmark trước khi chạy cả phim
`python3 tools/cli.py shot --shot <id> --preset final_4k` trên 4 shot đại diện (`frame_times_final_4k_bench.json`):

| Shot | Loại | Frame | Trung vị s/frame |
|---|---|---:|---:|
| SC_004 | 3D | 21 | 4,87 |
| SC_016 | 3D vòm, chú thích | 71 | 4,79 |
| SC_017 | 3D | 42 | 4,99 |
| SC_047 | card 2D (B35) | 10 | 0,61 |

- Mỗi PNG 4K riêng biệt nặng khoảng 6,4 MB. Blender dùng khoảng 3,3–3,6 GB RAM.
- Màu: so với bản 1080p, SSIM 0,994 và trung bình RGB như nhau.
- Lỗi phát hiện ở benchmark: PNG mang metadata sRGB nên luồng H.264 bị gắn transfer `iec61966-2-1`. Đã sửa bằng `setparams` (BT.709 cho matrix, primaries và transfer). C1 được render và mã hóa lại với `--force`.
- Thử ngắt giữa chừng: tiến trình được làm tiếp đúng. 1 PNG dở bị xóa, 95 PNG hoàn chỉnh được giữ, bản trung gian đã kiểm chứng được CACHED.

**Ước lượng trước khi chạy:** 5.218 frame riêng biệt, khoảng 4,2–4,5 giờ khi máy thức.

## 2. Chạy thật
Lệnh, chạy nền một lần cho cả 8 chương:
```bash
P=why-bridges-look-different
python3 tools/cli.py chapter --project $P --chapter C1 --preset final_4k --release-frames --force   # C1: re-render after the colour-tag fix
for c in C2 C3 C4 C5 C6 C7 C8; do python3 tools/cli.py chapter --project $P --chapter $c --preset final_4k --release-frames; done
python3 tools/cli.py final-assemble --project $P --preset final_4k
python3 tools/cli.py gates --project $P --preset final_4k
```

**Thời gian:** bắt đầu 2026-10-30 23:32:01, kết thúc 2026-10-31 03:31:27, tức **3 giờ 59 phút 26 giây**. 0 khoảng ngủ máy.

| Chương | Frame | Frame render riêng biệt | Shot render / cached | Thời gian thực | PNG đã xóa sau kiểm chứng | RSS tối đa của Blender |
|---|---:|---:|---|---:|---:|---:|
| C1 | 807 | 67 | 5 / 0 | 2 phút 55 giây | 0,33 GB | 3,4 GB |
| C2 | 1.166 | 78 | 3 / 0 | 7 phút 14 giây | 0,54 GB | 3,8 GB |
| C3 | 1.600 | 812 | 6 / 0 | 68 phút 27 giây | 5,78 GB | 3,8 GB |
| C4 | 1.969 | 226 | 4 / 2 (benchmark) | 4 phút 28 giây | 1,33 GB | 3,8 GB |
| C5 | 2.024 | 280 | 6 / 0 | 23 phút 20 giây | 1,95 GB | 3,8 GB |
| C6 | 3.005 | 604 | 9 / 0 | 13 phút 48 giây | 3,43 GB | 3,9 GB |
| C7 | 3.040 | 2.550 | 7 / 0 | 68 phút 57 giây | 14,32 GB | 3,9 GB |
| C8 | 1.784 | 601 | 4 / 1 (benchmark) | 45 phút 10 giây | 3,89 GB | 3,8 GB |
| Ghép bản cuối | 15.395 | – | – | 5 phút 8 giây | – | – |
| **Tổng** | **15.395** | **5.218 (33,9%)** | | **3 giờ 59 phút** | **31,57 GB** | **3,9 GB** |

- **Frame dùng lại:** 10.177/15.395 (66,1%). Frame tĩnh được hardlink, không render lại. Chiến lược shot: 4 STATIC_3D, 39 HYBRID, 4 ANIMATED_3D.
- **Tốc độ:** thời gian render khi thức là 14.046 s cho 5.214 frame có log, trung bình 2,69 s/frame. Đây là tổng hợp giữa 3D (khoảng 4,8 s) và card 2D (khoảng 0,6 s).
- **So với 1080p:** bản `internal_1080p` render 5.206 frame trong khoảng 1,26 giờ khi thức. Bản 4K có số điểm ảnh gấp 4 nhưng tốn khoảng 3,1 lần thời gian.
- **Đĩa:**
  - Lúc cao nhất, PNG chỉ chiếm 14,32 GB (C7). Nếu giữ cả 8 chương thì cần 31,57 GB.
  - Đĩa còn trống luôn ≥ 91 GB (ngưỡng dừng 8 GB).
  - Còn lại sau render: bản trung gian các chương 640 MB, MP4 cuối 303 MB, bản chỉ có hình 290 MB, WAV master 92 MB.
- **Bộ nhớ:** chỉ một Blender mỗi lúc, RSS tối đa 3,9 GB (C7). Không có tiến trình Blender song song.

## 3. Kiểm chứng ảnh 4K
**Không phải phóng to từ 1080p.** Ba frame được render trực tiếp lại bằng Blender (`--mode still --preset final_4k`), rồi so với cùng frame giải mã từ MP4 cuối và với frame của bản 1080p phóng lên 4K (lanczos):

| Frame | MP4 cuối so với render trực tiếp | 1080p phóng to so với render trực tiếp |
|---|---|---|
| SC_016 f80 (3D vòm, nhãn "Keystone") | PSNR 49,5 dB · SSIM 0,9946 | PSNR 38,3 dB · SSIM 0,9859 |
| SC_037 f300 (card) | PSNR 50,9 dB · SSIM 0,9967 | PSNR 34,8 dB · SSIM 0,9727 |
| SC_047 f100 (card B35) | PSNR 57,3 dB · SSIM 0,9995 | PSNR 35,9 dB · SSIM 0,9877 |

- MP4 cuối gần như trùng bản render trực tiếp. Chênh lệch còn lại là YUV 4:2:0 cộng nhiễu EEVEE.
- Bản 1080p phóng to kém hơn 11–21 dB, nên các frame của bản cuối mang chi tiết 4K thật.
- Bitrate video trung bình chỉ 3,6 Mb/s vì khoảng 2/3 số frame tĩnh và hình phẳng. Chất lượng do CRF 16 quyết định, không phải bitrate. Phép so ở trên cho thấy nén gần như trong suốt.

## 4. Ghi chú
- Âm thanh: preset yêu cầu AAC 256k. Bộ mã hóa AAC của FFmpeg cho ra trung bình 164 kb/s trên lời đọc mono 48 kHz (bản 1080p yêu cầu 160k, ra 137k). Đây là hành vi của bộ mã hóa, không phải tham số bị bỏ qua.
- Ước lượng 4,2–4,5 giờ hơi cao so với thực tế 3 giờ 59 phút: 3 shot đã render ở benchmark, và x264 mã hóa frame tĩnh nhanh.
- Chạy lại cùng lệnh: chương có bản trung gian hợp lệ trong `qa/chapter_intermediates_final_4k.json` được CACHED. Shot dở được làm tiếp từ PNG hoàn chỉnh.
