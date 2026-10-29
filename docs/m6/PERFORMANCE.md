# M6: hiệu năng đo được (pilot `bridge-load-explained`)

Máy: Apple M4 Pro, 24 GB, macOS, Blender 5.2.2 LTS (EEVEE), FFmpeg 9.0.1, Python 3.14.6; Kokoro chạy trên CPU. Số liệu lấy từ `/usr/bin/time -l` (log ở `projects/bridge-load-explained/qa/perf/`) và từ dấu thời gian `Saved:` trong log render của Blender.

> **Lưu ý về wall-clock:** trong phiên này máy nhiều lần ngủ khi tiến trình đang chạy (log render có những khoảng nghỉ 15 phút giữa hai frame; `caffeinate -i` không ngăn được ngủ do đóng nắp). Vì vậy, trừ lần render cuối (không bị ngủ), thời gian render được báo theo **thời gian từng frame khi máy thức** (median/p90 của khoảng cách giữa hai frame, bỏ các khoảng ≥ 10 s), không theo wall-clock tổng. Không có số nào ở đây là suy đoán.

| Bước | Thời gian | Bộ nhớ (max RSS) | Ghi chú |
|---|---|---|---|
| `narrate` `bm_george` (26 câu, 141,53 s audio) | 15,8 s wall; 27,5 s CPU | 2,67 GB (worker Kokoro) | Nạp model ≈ 2,5 s; ≈ **0,11 s/giây audio**. Sửa 1 câu (B1.s1): 25 câu CACHED, 1 câu sinh mới trong 4,1–4,3 s (gồm nạp model). Bản `bf_emma` trước đó: 13,1 s cho 126,58 s audio, 2,89 GB |
| `asr-check` (Whisper large-v3-turbo, MPS) | 50,6 s | 0,75 GB | 26 câu, WER ≤ 0,111 |
| `align` (word timestamps) | 36,0 s | 0,88 GB | 26 câu |
| `lock-audio` | 0,08 s | 34 MB | |
| `plan-visuals` (11 shot, 27 chú thích, raster điểm neo 384×216) | 1,50 s | 53 MB | Gồm visibility L1, sửa tầm nhìn, chú thích, nhất quán |
| `validate-plan` (+ engine G0 trên bản sao) | 0,54 s | 44 MB | |
| `check-blender --preset review` (176 kiểm tra) | ≈ 7 s | | Gồm QA chú thích (ray-cast điểm neo) |
| Smoke SC_003 (440 frame review + encode + assemble) | 359 s wall | 0,52 GB | Lúc này máy không ngủ. Render ≈ 0,8 s/frame |
| Render review 960×540, EEVEE, bản cuối (`bm_george`, 3632 frame, 11 shot, mỗi lúc một Blender) | **3144,9 s wall** (render + encode + media QA), không có lần ngủ nào; tổng thời gian frame 3127 s = **0,86 s/frame**; median từng shot 0,48–1,13 s | 0,53 GB (CLI) | Nhẹ nhất SC_004 (HOLD cận cảnh), nặng nhất SC_011 (3 mô hình cạnh nhau) |
| `assemble` (track lời dẫn, loudnorm 2 lượt, mux, SRT + mov_text, QA) | 6,2 s | 71 MB | |
| Render review bản `bf_emma` (3271 frame) | median 0,95 s/frame | | Wall-clock không dùng được: máy ngủ trong lúc render |
| Thử giọng (4 giọng × 3 câu + 4 lần nạp ASR) | 46,5 s CPU | | Wall-clock 55 phút do máy ngủ: không phải số đo hiệu năng |
| `evaluate-planning` (29 ca) | | | Wall-clock bị kéo dài do máy ngủ |

## Tái sử dụng cache
- **Audio:** khóa cache theo provider/model/giọng/tham số/chữ/hạng quyền. Đổi 1 câu thì chỉ sinh lại câu đó (25/26 CACHED).
- **Render:** khóa theo shot (`tools/render_cache.py`; M6 thêm `config/annotation_style.json` vào nhóm `style` cho shot có chú thích). `qa_annotations.py` không làm cũ frame.
  - Sửa câu B7 của bridge-story-m5 chỉ làm cũ 3 shot B7; 12 shot khác giống hệt về hình.
  - Thay đổi engine M6 (spec/templates/shot_builder) làm cũ mọi frame cũ (hạng mục `engine`). Đây là hành vi cố ý.
- **Planner:** tất định. Chạy lại cho storyboard giống hệt (đã kiểm sau mỗi thay đổi code ở cả ba dự án do planner sinh).
