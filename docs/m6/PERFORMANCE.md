# M6: hiệu năng đo được (pilot `bridge-load-explained`)

Máy: Apple M4 Pro, 24 GB, macOS, Blender 5.2.2 LTS (EEVEE), FFmpeg 9.0.1, Python 3.14.6; Kokoro chạy trên CPU. Số liệu lấy từ `/usr/bin/time -l` (log ở `projects/bridge-load-explained/qa/perf/`) và từ dấu thời gian `Saved:` trong log render của Blender.

> **Lưu ý về wall-clock:** trong phiên này máy nhiều lần ngủ khi tiến trình đang chạy (log render có những khoảng nghỉ 15 phút giữa hai frame; `caffeinate -i` không ngăn được ngủ do đóng nắp). Vì vậy thời gian render được báo theo **thời gian từng frame khi máy thức** (median/p90 của khoảng cách giữa hai frame, bỏ các khoảng ≥ 10 s), không theo wall-clock tổng. Không có số nào ở đây là suy đoán.

| Bước | Thời gian | Bộ nhớ (max RSS) | Ghi chú |
|---|---|---|---|
| `narrate` (Kokoro, 26 câu, 126,58 s audio) | 13,1 s wall; 25,1 s CPU | 2,89 GB (worker Kokoro) | Nạp model ≈ 2,5 s. Mỗi câu 0,2–0,6 s ≈ **0,13 s/giây audio**. Lần chạy lại sau khi sửa B7.s3: 25 câu CACHED, 1 câu sinh mới (4,4 s, gồm cả nạp model) |
| `asr-check` (Whisper large-v3-turbo, MPS) | 57,4 s | 0,75 GB | 26 câu, WER ≤ 0,087 |
| `align` (word timestamps) | 40,9 s | 0,88 GB | 26 câu |
| `lock-audio` | 0,08 s | 34 MB | |
| `plan-visuals` (11 shot, 27 chú thích, raster điểm neo 384×216) | 1,50 s | 53 MB | Gồm visibility L1, sửa tầm nhìn, chú thích, nhất quán |
| `validate-plan` (+ engine G0 trên bản sao) | 0,54 s | 44 MB | |
| `check-blender --preset review` (175 kiểm tra) | ≈ 7 s | | Gồm QA chú thích (ray-cast điểm neo) |
| Smoke SC_003 (440 frame review + encode + assemble) | 359 s wall | 0,52 GB | Lúc này máy không ngủ. Render ≈ 0,8 s/frame |
| Render review 960×540, EEVEE | median **0,95 s/frame**, p90 ≈ 1,0–1,4 s | | Đo trên các shot đã xong. Tổng 3271 frame ≈ 52 phút thời gian máy thức |
| Thử giọng (4 giọng × 3 câu + 4 lần nạp ASR) | 46,5 s CPU | | Wall-clock 55 phút do máy ngủ: không phải số đo hiệu năng |
| `evaluate-planning` (29 ca) | | | Wall-clock bị kéo dài do máy ngủ |

## Tái sử dụng cache
- **Audio:** khóa cache theo provider/model/giọng/tham số/chữ/hạng quyền. Đổi 1 câu thì chỉ sinh lại câu đó (25/26 CACHED).
- **Render:** khóa theo shot (`tools/render_cache.py`; M6 thêm `config/annotation_style.json` vào nhóm `style` cho shot có chú thích). `qa_annotations.py` không làm cũ frame.
  - Sửa câu B7 của bridge-story-m5 chỉ làm cũ 3 shot B7; 12 shot khác giống hệt về hình.
  - Thay đổi engine M6 (spec/templates/shot_builder) làm cũ mọi frame cũ (hạng mục `engine`). Đây là hành vi cố ý.
- **Planner:** tất định. Chạy lại cho storyboard giống hệt (đã kiểm sau mỗi thay đổi code ở cả ba dự án do planner sinh).
