# M7: tái lập và kiểm tra build sạch, "Why Bridges Don't All Look the Same"

## 1. Môi trường đã dùng (đo ngày 2026-10-30)
| Thành phần | Phiên bản / cấu hình |
|---|---|
| Máy | Apple M4 Pro, 24 GB, macOS 27.2 |
| Blender | 5.2.2 LTS (EEVEE), `/Applications/Blender.app`, luôn chạy `--background --factory-startup` |
| Python của pipeline | 3.14.6, **chỉ stdlib** (pipeline, planner, tools, tests) |
| FFmpeg / ffprobe | 9.0.1 (Homebrew). Không có libass/freetype, nên **không có bản khắc phụ đề vào hình**; phụ đề là SRT + track mov_text |
| TTS | Kokoro-82M `hexgrad/Kokoro-82M` @ `f3ff3571791e39611d31c381e3a41a3af07b4987`, `kokoro-v1_0.pth` SHA256 `496dba11…`, giọng `bm_george` SHA256 `f1bc8122…`. Venv `~/Work/Projects/Kokoro/.venv`: Python 3.12, kokoro 0.9.4, misaki 0.9.4, torch 2.15.0 CPU. Chạy offline (`HF_HUB_OFFLINE=1`) |
| ASR / alignment | `openai/whisper-large-v3-turbo` qua venv `~/Work/Projects/OmniVoice/.venv` (transformers 5.9.0, torch 2.12.0; biến `OMNIVOICE_PYTHON` nếu ở chỗ khác). Chỉ dùng cho QA và ngắt dòng phụ đề |
| Nghiên cứu | `pdftotext` 25.12.0 (poppler) để sinh lại `research/sources.json` từ ảnh chụp nguồn |
| Blender MCP | **Không cần cho build.** Chỉ dùng để soi cảnh (`mcp-for-blender` 2.2.4, safe mode, `127.0.0.1:9876`). MP4 cuối không phụ thuộc phiên MCP nào |

## 2. Dữ liệu nguồn của dự án (đều trong git)
- `research/build_sources.py` → `research/sources.json` (khớp nguyên văn).
  - Ảnh chụp nguồn **không** được commit: PDF NCHRP và HTML ASCE/Yale. Mỗi file có SHA256, URL và cách trích văn bản trong `research/source_snapshots.json`.
  - Muốn sinh lại: tải lại các file đó vào một thư mục, đặt `M7_SOURCE_SNAPSHOTS=<thư mục>`, rồi so SHA256.
- `script/story.py` + `script/narration.template.json` → `narration.json`, `visual_beats.json`, `chapters.json`.
- `assets/manifest.json` + `assets/external/*.jpg`: 4 ảnh HAER bản 1920 px, có SHA256 trong hồ sơ. Mô hình 3D sinh thủ tục từ `asset_library/architecture/*.json` (M4).
- `audio/segments/*.wav` + `audio/narration_manifest.json`: lời dẫn đã sinh (được commit), kèm khóa cache, hash model/giọng và kết quả ASR. Với cùng model, giọng, tham số và seed, Kokoro sinh lại giống hệt từng bit (đã kiểm ở M6).
- Không có đường dẫn tuyệt đối trong dữ liệu dự án. Không có bí mật nào trong manifest.

## 3. Lệnh build
```bash
P="--project why-bridges-look-different"
python3 projects/why-bridges-look-different/script/story.py
python3 tools/cli.py narrate $P --purpose publication     # dùng audio cache; chỉ sinh câu mới
python3 tools/cli.py asr-check $P && python3 tools/cli.py align $P && python3 tools/cli.py lock-audio $P
python3 tools/cli.py plan-visuals $P && python3 tools/cli.py build-shots $P
python3 tools/cli.py chapters $P --preset review          # manifest chương + qa/longform_qa.json
python3 tools/cli.py check-blender $P --preset review
python3 tools/cli.py preview $P --preset preview && python3 tools/cli.py assemble $P --preset preview   # rough cut
python3 tools/cli.py preview $P --preset review && python3 tools/cli.py assemble $P --preset review     # review cut
for c in C1 C2 C3 C4 C5 C6 C7 C8; do python3 tools/cli.py chapter $P --chapter $c --preset review; done
python3 tools/cli.py still $P --preset production_test     # still 1080p (checkpoint F)
python3 tools/longform_reports.py $P && python3 tools/cli.py research-map $P
python3 tools/cli.py cache-report $P --preset review && python3 tools/cli.py gates $P --preset review
python3 -m unittest discover -s tests
```

## 4. Vị trí cache và đầu ra (không commit)
| Đường dẫn | Nội dung | Làm mới khi |
|---|---|---|
| `renders/<preset>/<shot>/frame_####.png` + `render_manifest.json` (+ `render_progress.json` khi đang render) | Frame từng shot | Khóa cache của shot đổi (`tools/render_cache.py`) |
| `audio/beats/`, `audio/narration_track_*.wav`, `audio/narration_mix_*.wav` | Audio beat và track ghép | Mỗi lần `narrate` / `assemble` |
| `output/` | MP4 toàn phim, MP4 + WAV từng chương, SRT, master audio, still 1080p | Mỗi lần `preview` / `chapter` / `assemble` / `still` |
| `scenes/SC_*.blend` | Cảnh Blender đã dựng (để soi qua MCP) | Mỗi lần render |
| `~/.cache/huggingface` | Trọng số Kokoro và Whisper | Không bao giờ tự tải trong pipeline (offline) |

## 5. Kế hoạch kiểm tra build sạch (clean-room)
1. Clone nhánh `m7-first-full-documentary` vào một thư mục mới trên một máy có các phiên bản ở mục 1. Không sao chép `renders/`, `output/`, `scenes/`.
2. `python3 tools/cli.py doctor`: Blender, FFmpeg, đĩa trống.
3. `python3 -m unittest discover -s tests`: toàn bộ test offline và Blender.
4. `python3 projects/why-bridges-look-different/script/story.py` → `git diff --exit-code projects/why-bridges-look-different/script/` (kịch bản sinh lại giống hệt).
5. `narrate … --purpose publication` phải báo mọi câu **CACHED** (audio có trong git). Sau đó `--regenerate` trên một bản sao và so SHA256 của 102 file segment (103 câu; câu hỏi lặp lại dùng chung một đoạn audio) với `narration_manifest.json` (Kokoro tất định).
6. `asr-check`, `align`, `lock-audio`, `plan-visuals`, `build-shots` → `git diff --exit-code` cho `script/timing.json`, `storyboard/*.json` (planner tất định).
7. `chapters`, `check-blender` → so số kiểm tra đạt với `qa/blender_checks.json` (577 cho bản này).
8. `chapter --chapter C4 --preset review` → so số frame, độ dài, loudness và số câu phụ đề với `qa/chapter_C4_review.json`. Pixel có thể lệch nhẹ nếu GPU hay driver khác; số frame và timing phải trùng.
9. Render toàn phim nếu cần, rồi `gates`. Kết luận phải vẫn là INTERNAL REVIEW cho tới khi có duyệt.
10. Tùy chọn: sinh lại `research/sources.json` từ ảnh chụp nguồn (mục 2) và `git diff --exit-code`.

## 6. Giới hạn tài nguyên đã đặt
- Độ phân giải: review 960×540; 1080p **chỉ cho still chọn lọc** (`production_test`). Không render 4K. Bản `final` 1080p bị chặn bởi G6 khi chưa có duyệt.
- Mỗi lúc **một** tiến trình Blender (CLI tuần tự; MCP chỉ mở khi không render).
- Bộ nhớ đo được: CLI render ≤ 0,58 GB RSS; Blender QA 0,37 GB; worker Kokoro ≈ 2,7 GB (M6).
- File tạm: chuỗi symlink để mã hóa (`renders/<preset>/_sequence_*`) bị xóa ngay sau khi mã hóa. Frame PNG đo được: 0,18 MB/frame ở 640×360 (2,7 GB cho 15.391 frame); 960×540 xem `docs/m7/PERFORMANCE.md`.
- Render lại toàn phim chỉ khi khóa cache đổi. Ước lượng thời gian lấy từ shot và chương đại diện (SC_015 rồi C4), trước khi render cả phim.

## 7. Bản review nội bộ cuối (giọng `am_michael`, 1080p)
```bash
P="--project why-bridges-look-different"
# tải giọng Anh–Mỹ đúng revision và kiểm hash (dùng interpreter của Kokoro)
~/Work/Projects/Kokoro/.venv/bin/python tools/kokoro_fetch_voices.py am_michael
python3 projects/why-bridges-look-different/script/story.py
python3 tools/cli.py narrate $P --purpose publication && python3 tools/cli.py asr-check $P && python3 tools/cli.py align $P
python3 tools/cli.py lock-audio $P && python3 tools/cli.py plan-visuals $P && python3 tools/cli.py build-shots $P
python3 tools/cli.py check-blender $P --preset internal_1080p
/Applications/Blender.app/Contents/MacOS/Blender --background --factory-startup --python engine/render_scene.py -- \
  --project projects/why-bridges-look-different --mode reuse-report --preset internal_1080p \
  --report projects/why-bridges-look-different/qa/perf/reuse_report_internal_1080p.json    # ước lượng trước
for c in C1 C2 C3 C4 C5 C6 C7 C8; do python3 tools/cli.py chapter $P --chapter $c --preset internal_1080p; done
python3 tools/cli.py preview $P --preset internal_1080p && python3 tools/cli.py assemble $P --preset internal_1080p
python3 tools/cli.py verify-reuse $P --shot SC_017 --preset internal_1080p
python3 tools/cli.py gates $P --preset internal_1080p
```
- Hồ sơ duyệt claim (`research/editorial_approval.json`) là dữ liệu của người duyệt. `build_sources.py` chỉ áp hồ sơ này vào registry.
- Frame lặp là hardlink. Muốn sao chép thư mục `renders/` sang máy khác thì dùng công cụ giữ hardlink (`rsync -H`); nếu không, dung lượng tăng khoảng 3 lần.
- `--no-reuse` render đủ mọi frame. Dùng khi nghi ngờ hoặc để so sánh.
