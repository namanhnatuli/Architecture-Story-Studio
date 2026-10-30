# M7: hiệu năng đo được, "Why Bridges Don't All Look the Same"

Máy: Apple M4 Pro, 24 GB, macOS 27.2, Blender 5.2.2 LTS (EEVEE), FFmpeg 9.0.1, Python 3.14.6. Kokoro chạy trên CPU.

> **Máy ngủ trong lúc render.** `caffeinate -i` chỉ chặn ngủ khi máy rảnh, không chặn ngủ bảo trì hay ngủ khi gập nắp. Log Blender có **29** khoảng ngủ trong rough cut và **11** khoảng ngủ trong bản review. Vì vậy tốc độ render được đo bằng **thời gian máy thức**: cộng các khoảng cách giữa hai dòng `Saved:` liên tiếp, bỏ các khoảng ≥ 10 s (`tools/frame_times.py`, kết quả ở `projects/why-bridges-look-different/qa/perf/frame_times_*.json`). Wall-clock chỉ ghi để tham khảo.

## Render
| Bước | Frame | Thời gian máy thức | s/frame | Wall-clock | RSS lớn nhất |
|---|---|---|---|---|---|
| Shot đại diện SC_015 (3D cận cảnh, 960×540), dùng để ước lượng trước khi render chương | 96 | ≈ 110 s | 1,14 | — | — |
| Checkpoint C: chương C4, 960×540, lần 1 | 1974 | 1124 s (không ngủ) | 0,57 | 1124 s | 0,51 GB |
| C4 lần 2 (3 shot sửa, 3 CACHED) | 1302 render | 383 s | — | 383 s | — |
| Checkpoint D: rough cut 640×360 | 15.391 | **8435 s (2,3 giờ)** | **0,548** | 29.094 s (8,1 giờ) | 0,58 GB |
| Checkpoint E: review cut 960×540 | 15.515 | **≈ 8990 s (2,5 giờ)** | **0,593** | 16.589 s (4,6 giờ) | 0,59 GB |
| E, sau khi sửa B16 (chỉ SC_022 render lại, mã hóa lại cả phim, media QA) | 347 render | — | — | 260 s | 0,50 GB |
| Checkpoint F: 47 still 1920×1080 | 47 | — | ≈ 1,1 s/still (gồm dựng cảnh) | 53 s | 0,83 GB |

Tốc độ theo loại shot, chỉ tính lúc máy thức:

| Loại | 640×360 | 960×540 |
|---|---|---|
| 3D (giữ, tách lớp, thay bộ phận, push-in) | 0,744 s/frame | 0,893 s/frame |
| 3D ba mô hình cạnh nhau | 1,912 s/frame | 1,486 s/frame |
| Card (chữ, sơ đồ, ảnh lưu trữ) | 0,188 s/frame | 0,171 s/frame |

- Số điểm ảnh tăng 2,25 lần (640×360 → 960×540) nhưng thời gian 3D chỉ tăng khoảng 1,2 lần. Phần lớn chi phí mỗi frame là cố định: đánh giá cảnh, bóng đổ, ghi PNG.
- Thời gian rough cut bị ảnh hưởng thêm vì máy ngủ ở giữa shot: p90 của SC_043 là 2,9 s/frame. Hai cột tốc độ vì thế không so sánh chặt được với nhau.
- Chưa render video 1080p; chỉ có still. Tôi ước đoán video 1080p sẽ mất 1,5–2 lần thời gian bản 960×540. Đây là ước đoán, chưa đo.

## Âm thanh, lập kế hoạch, ghép
| Bước | Kết quả |
|---|---|
| `narrate` một câu mới (B35.s1) | 4,5 s, gồm nạp model; 101 câu khác CACHED |
| `asr-check` toàn bộ (lần đầu, 101 câu) | khoảng 10 phút. Không đo bằng `time`: ASR chạy song song với việc khác |
| `asr-check` sau khi thêm cache (M7) | 101 câu dùng lại bản chép cũ, 1 câu nghe mới |
| `align` | chỉ căn câu mới; những câu còn lại CACHED |
| `check-blender` toàn phim (577 kiểm tra) | 21,9 s wall, 0,37 GB |
| `assemble` review (track lời dẫn, loudnorm 2 lượt, mux, SRT + mov_text, QA) | 26,7 s wall, 0,10 GB |
| Thử giọng: 21 giọng × 3 câu + một lượt ASR | vài phút |

## Đĩa
| Thư mục | Dung lượng |
|---|---|
| `renders/preview` (15.391 PNG) | 2,8 GB (0,18 MB/frame) |
| `renders/review` (15.515 PNG) | 5,9 GB (0,38 MB/frame) |
| `output/` (MP4 cả phim, 8 chương, WAV, still 1080p) | 363 MB |
| `audio/segments` (102 đoạn, được commit) | 28 MB |

Ước lượng cho video 1080p cả phim: 1,53 MB/frame (đo trên 47 still: 72 MB) × 15.515 ≈ 24 GB PNG. Máy còn khoảng 50 GB trống, nên nên render theo chương và xóa PNG sau khi mã hóa.

## Hiệu quả của cache
- **Render:** sửa chú thích B16 chỉ làm cũ 1/47 shot. C4 lần 2: 3/6 shot CACHED. Tám MP4 chương dựng hoàn toàn từ frame CACHED (47/47).
- Thay đổi file engine (rig chú thích cho push-in) làm cũ mọi frame, theo đúng thiết kế (nhóm `engine`). Đó là lý do bản review phải render lại từ đầu.
- **Không làm cũ frame** (có test riêng): hồ sơ quyền ảnh, trạng thái claim, `factual_review`, đường dẫn `chapters`. Đổi byte của một ảnh chỉ làm cũ các card dùng ảnh đó.
- **Audio:** đổi hoặc thêm câu chỉ sinh lại câu đó. ASR không nghe lại audio giống hệt.
- **Khôi phục khi bị ngắt:** có `render_progress.json` cùng khóa cache thì giữ các PNG hoàn chỉnh và render tiếp (có test). Trong lượt render thật chưa xảy ra lần ngắt nào: máy ngủ chỉ làm chậm, không làm chết tiến trình.
