# M7: kiến trúc phim tài liệu dài (8–15 phút)

M7 đưa pipeline audio-first của M6 lên một phim hoàn chỉnh: **"Why Bridges Don't All Look the Same"** (`projects/why-bridges-look-different`, khoảng 10,7 phút, 8 chương). Phim trộn hình 3D, sơ đồ 2D tự vẽ và ảnh lưu trữ có hồ sơ quyền. Mỗi chương render, ghép và kiểm tra được riêng.

## 1. Trình tự
```
research        research/build_sources.py → sources.json (12 nguồn, 42 claim, khớp nguyên văn)
 → script       script/story.py → narration.json + visual_beats.json + chapters.json (một nguồn duy nhất)
 → narrate --purpose publication (Kokoro bm_george) → asr-check → align → lock-audio
 → plan-visuals → validate-plan → build-shots (audio_lock.finalize)
 → chapters     chapters/chapter_manifest.json + qa/longform_qa.json (không cần Blender)
 → check-blender
 → chapter --chapter C4      render + mã hóa + ghép lời dẫn/phụ đề cho một chương (checkpoint C)
 → preview / assemble        cả phim (rough cut 640×360, review cut 960×540)
 → still --preset production_test   ảnh 1080p chọn lọc (checkpoint F)
 → gates (G0–G6 + GV + GL) / research-map / tools/longform_reports.py
```

## 2. Chương (`pipeline/chapters.py`)
- `script/chapters.json` (schema `chapters/1`) chia các beat lời dẫn thành chương có thứ tự. `project.json` khai báo `"chapters": "script/chapters.json"`. Mode `documentary` bắt buộc có chương (`tools/validator.py`).
- `validate` (fail closed): mỗi beat thuộc đúng một chương; chương liên tục và theo đúng thứ tự lời dẫn; không có chương rỗng, thiếu tiêu đề hay trùng id; trường `chapter` của visual beat phải khớp.
- `shot_ranges`: sau khi khóa timing, mỗi chương là một dải shot và frame liên tục. Shot nào thuộc hai chương thì báo lỗi.
- `manifest`: dải frame, thời điểm, số câu/từ, claim, loại hình, asset ngoài và số frame đã render của từng chương.
- CLI `chapter --chapter Cn`: render các shot của chương (có cache), nối frame thành một chuỗi, mã hóa, ghép track lời dẫn và phụ đề của đúng dải đó (`assemble.assemble(shot_ids=…)`), rồi QA riêng (frame, định dạng, lỗi giải mã, khung đen, SSIM ở các điểm cắt). Ra `output/chapters_<preset>/<slug>_<Cn>_<nhãn>.mp4`.

## 3. Card 2D (sơ đồ, bản đồ, dòng thời gian, ảnh)
- `engine/diagram.py` dựng các phần tử `text` (có tấm nền), `arrow`, `rect`, `line` (nét đứt), `circle`, `polygon`, `image` (cắt, vừa khung, trôi chậm). Mỗi phần tử fade vào lúc `appear` và có thể fade ra ở `disappear`.
- Lập kế hoạch: chiến lược `CARD` giải `sentence` → `appear`, `until` → `disappear` theo khoảng câu đã đo. M7 thêm `word`: phần tử hiện đúng lúc từ đó được đọc, theo word timestamp Whisper của chính đoạn audio hiện tại (kiểm `segment_sha256`). Từ không có trong alignment thì chiến lược bị từ chối (INVALID_REQUEST).
- `templates.plan_card` (stdlib): card ngắn hơn 1,5 s là `TOO_SHORT`; phần tử phải fade vào xong trước frame cuối và chỉ fade ra sau khi đã hiện đủ. Planner và validator dùng chung hàm này. Trước M7, planner chưa từng lập kế hoạch thời lượng cho card (card M3 viết tay).
- QA Blender `card_layout`: chữ nằm trong vùng an toàn và (khi AUDIO_LOCKED) trên vùng phụ đề; ảnh nằm trong khung.

## 4. Ảnh lưu trữ và quyền
- Mỗi ảnh ngoài có một bản ghi `assets/manifest.json` với `origin: external` và đủ các trường `EXTERNAL_LICENSE_FIELDS`. Ngoài ra có `credit_keys`: các cụm chữ phải xuất hiện trong phần ghi công.
- Validator từ chối: ảnh không có hồ sơ, hồ sơ thiếu trường, đường dẫn khác `local_path`, file không tồn tại, vùng cắt sai.
- QA phim dài kiểm thêm: hồ sơ `approved`, SHA256 của file đúng với hồ sơ, và mọi `credit_keys` có trong chữ trên card hoặc trong `review/YOUTUBE_DESCRIPTION.md`.
- Bốn ảnh HAER (Thư viện Quốc hội Mỹ, phạm vi công cộng PD-USGov-NPS) chỉ bị cắt bỏ viền phim. Thao tác cắt được ghi trong `modifications`.

## 5. Chuyển động camera và chú thích
- `HOLD.camera_move = {type: PUSH_IN, amount ≤ 0.3}`: bắt đầu đúng khung khóa và thu ortho theo `amount`. Độ lệch tâm bị kẹp ±amount/2 nên khung cuối nằm trong khung đầu (`engine/framing.push_in_keys`). Shot kế tiếp luôn cắt cứng. Shot push-in không mang chú thích neo vào bộ phận.
- `NOTE`: chú thích cố định trên màn hình (tối đa 52 ký tự, 4 góc), dùng cho tiêu đề chương và nhãn "Illustrative model, not the …". NOTE và chú giải được phép trên SIDE_BY_SIDE và REPLACE_PARTS. Một chú thích chỉ FAILED khi không shot nào nhận nó.

## 6. Render cache và khôi phục khi bị ngắt
- Byte của mọi ảnh mà card vẽ là đầu vào render (nhóm `assets`). Đổi ảnh chỉ làm cũ các card dùng ảnh đó.
- Không làm cũ frame: hồ sơ quyền và ghi công, trạng thái claim, `factual_review`, đường dẫn `chapters` (thêm vào `PROJECT_NON_VISUAL`).
- `render_shot` ghi `render_progress.json` (khóa cache, số frame) trước khi Blender chạy.
  - Nếu một lần render **cùng khóa** bị ngắt (ngủ, mất điện, kill): giữ các PNG hoàn chỉnh (kiểm chữ ký PNG và chunk `IEND`), xóa frame dở dang, và gọi Blender với `--resume` (`use_overwrite = False`).
  - Khác khóa, hoặc không có bản ghi tiến độ: render lại cả shot.
  - Manifest cũ bị xóa trước khi render, nên không bao giờ có manifest bảo chứng cho frame đang bị thay.
- Phim dài được mã hóa từ **một** chuỗi PNG liên kết (symlink theo thứ tự). Cách này không mở 46 bộ giải mã song song như bộ lọc concat cũ. Contact sheet giới hạn 150 ô.

## 7. QA phim dài và cổng GL
`chapters` chạy `longform_qa` và ghi `qa/longform_qa.json`:

| Kiểm tra | Luật |
|---|---|
| `chapters_structure` | validate + `shot_ranges` không lỗi |
| `chapter_durations` | mỗi chương ≥ 15 s |
| `runtime` | 8–15 phút |
| `no_duplicate_shots` | id shot duy nhất |
| `no_repeated_sentences` | cảnh báo nếu một câu lặp nguyên văn (câu hỏi mở và kết của phim lặp có chủ ý) |
| `narration_silences` | khoảng lặng giữa hai beat ≤ 4 s, sau câu cuối ≤ 4 s |
| `no_static_stretches` | không có đoạn > 14 s mà hình không đổi. Đổi hình gồm: chuyển động của template (explode/return, replace, intro, highlight lên/xuống), push-in, ảnh trôi, chú thích và phần tử card hiện/ẩn |
| `visual_variety` | không quá 4 shot cùng loại liên tiếp |
| `chapter_variety` | cảnh báo nếu chương nhiều shot chỉ có một loại hình |
| `image_licences`, `image_attribution` | như mục 4 |

Cổng `GL long-form chapters & rights` chỉ áp dụng cho dự án có chương. Cổng này FAIL nếu báo cáo thiếu, cũ (SHA256 của `timing.json` khác) hoặc có kiểm tra FAIL. G6 và trạng thái `TECHNICALLY_VALIDATED` cần GL đạt.

## 8. Nhãn INTERNAL REVIEW
- `output_label`: mode `documentary` chỉ có tên `…_documentary.mp4` khi audio đã `PUBLICATION_CLEARED` **và** mọi claim được lời dẫn dùng đều `EDITORIALLY_APPROVED` **và** `factual_review: verified`. Nếu không, tên là `…_documentary_INTERNAL_REVIEW…`, và metadata `comment` là "INTERNAL REVIEW - editorial approval and/or rights pending - not for publication".
- Profile vẫn là `NARRATED_INTERNAL_REVIEW`. Đổi profile không tắt được cổng nào (validator từ chối `TECHNICAL_SILENT_PREVIEW` cho dự án có lời dẫn).

## 9. Báo cáo sinh tự động
`python3 tools/longform_reports.py --project why-bridges-look-different` sinh `review/EVIDENCE_MATRIX.md`, `review/EDITORIAL_APPROVAL_PACKAGE.md`, `review/YOUTUBE_DESCRIPTION.md` (BẢN NHÁP) và `qa/VISUAL_VARIETY.md`. Công cụ này chỉ chép trạng thái, không bao giờ nâng trạng thái.

## 10. Bổ sung sau rough cut
- **Rig chú thích cho push-in** (`engine/shot_builder.annotation_rig`). Khi một HOLD có `camera_move`, mọi chú thích được gắn vào một empty `ANN_RIG` đặt tại camera. Rig được key vị trí giống camera và tỉ lệ = ortho(t)/ortho(đầu), cùng easing, nên chú thích giữ nguyên vị trí và cỡ trên khung hình. Kênh mới `motion.SCALE`. Các QA liên quan:
  - `overlays_screen_fixed` đo độ trôi trên khung ở frame đầu, giữa và cuối (≈ 1e-7);
  - `no_scale_change` chỉ miễn cho rig và các con của nó, không miễn cho mô hình hay camera.
- **Chú thích theo từ** (`planner/annotations.plan_beat(words=…)`). Chú thích có thể khai `"word"`, giống phần tử card. Từ không có trong alignment thì chú thích bị FAILED, plan không chạy được.
- **ASR dùng lại bản chép** khi byte audio (`segment_sha256`), chữ và model đều trùng. Kết quả vẫn được chấm lại bằng luật WER hiện hành.
- **Worker Kokoro** giữ một pipeline G2P cho mỗi `lang_code`. Trước đây worker chạy liên tục chỉ dùng `lang_code` của yêu cầu đầu tiên.
- **Giọng nghe thử** (`kokoro.AUDITION_VOICE_SHA256`, `tools/kokoro_fetch_voices.py`, `tools/voice_audition.py --voices us`). 20 giọng Anh–Mỹ đã kiểm hash nhưng chỉ dùng để nghe; `verify_release` của lời dẫn vẫn từ chối chúng.
- **Cổng tôn trọng cờ của từng phim:**
  - `voice.license.owner_confirmation_for_this_film: PENDING` → G2 `BLOCKED_RIGHTS`;
  - `voice.pronunciation_review.status: PENDING` → G1 không PASS.
- **QA phim dài bổ sung:** `narration_sentences_complete`, `audio_no_overlap`, `no_repeated_visuals`, `chapter_openings` (chương 2–8 mở đầu bằng tiêu đề đánh số), `annotations_consistent`, `render_cache_current`.
- **Bằng chứng theo chương** (`chapter_manifest.json` → `evidence`): claim dùng và trạng thái, nguồn, beat fact không có claim, revision lời dẫn, giả định hình ảnh (NOTE, giấy phép ảnh), phân loại độ chính xác lịch sử, trạng thái biên tập.
- **Xuất thêm:** WAV từng chương; master lời dẫn gốc và master đã chuẩn hóa loudness.
