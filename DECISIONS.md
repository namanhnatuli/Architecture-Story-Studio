# Locked product/engineering decisions (2026-10-22)

**Product choices**
- Audience: English-language YouTube, aim 8–15 minutes/video.
- Narration/story-first architecture history/design explainers. 3 formats: decision A→B due to constraints, architecture across time, regional comparison.
- 3D visuals: Clean Stylized Architectural / Technical Visualization; asset geometry separated into meaningful components.
- Transitions: DISASSEMBLE / REPLACE_PARTS / COMPARE / CUTAWAY / EXPLODED_VIEW; careful cause/effect visualizations.
- No required humans/characters/workers/machinery. Destruction is an occasional storytelling device, **not** the channel premise.
- No interactive web application as primary deliverable. Blender renders YouTube videos; Three.js is optional future tool, not MVP.

**Technical choices**
- Mac Apple Silicon M4, RAM 16 GB, creator is beginner.
- Blender + bpy + geometry/procedural modeling, Codex *or* Claude Code as primary coding assistant; Blender MCP optional for inspection; FFmpeg encode.
- Work in project-local files and deterministic, testable stages; single shared project spec JSON rather than giant free-form prompts.
- Unit test offline, then greybox preview, then publication gates. Keep render frames out of version control.
- Blender 4.5 LTS and 5.2 LTS supported by source code where possible; 5.x Eevee identifier changed. Runtime Blender rendering on target Mac remains unverified until user runs it.

**Pilot**
- `roof-evolution`: simple house where only roof configuration changes A→B; 6s greybox preview, no factual claim about roof engineering. This is a render technology smoke test, not a full researched YouTube episode.

If a requested change conflicts with these choices, document the reason and update this file before changing architecture.

## Bổ sung 2026-10-26 (M2) — không thay thế các quyết định ở trên
- **Planning tách khỏi bpy.** Logic template là Python thuần và có thể test; Blender chỉ dựng geometry và ghi keyframe. Lý do: validator G0 cần biết timing / ownership mà không phải khởi động Blender.
- **Một shot = một scene Blender độc lập**, dựng lại từ JSON mỗi lần render, có cache theo hash đầu vào. Các shot một-model dùng chung một camera fit theo mọi variant, để cắt cảnh không lộ.
- **Biến mất = di chuyển + mờ dần + hide_render, không bao giờ thu nhỏ scale.** Cấu kiện chỉ được đi qua mép khung khi đã trong suốt ít nhất 50%.
- **Ánh sáng bằng sun** (không dùng area light nhắm vào gốc tọa độ), để SIDE_BY_SIDE có điều kiện chiếu sáng như nhau.
- **Highlight giữ nguyên tông màu gốc**: màu nhấn #D9A441 chỉ chiếm 10%, phần còn lại là phát sáng cùng màu.
- **MCP chỉ để quan sát/kiểm tra.** Mọi output tái lập được đều đi qua CLI. Engine hỗ trợ `isolated=True` để MCP không xóa scene của người dùng.

## Bổ sung 2026-10-27 (M2.5) — không thay thế các quyết định ở trên
- **Mái đọc đúng cấu tạo khi tháo ra:** cấu kiện kết cấu gác lên tường (seat cut), không xuyên vào. QA kiểm tra mọi variant ở vị trí nghỉ.
- **Highlight = phát sáng bằng chính màu của phần đó.** Không dùng màu nhấn trên cấu kiện có màu nhận diện state.
- **Ánh sáng chuẩn "L3"** (nắng trước-trái, cao; AgX Medium High Contrast). Mọi thay đổi ánh sáng phải so sánh ở 960×540 trên các frame đại diện trước khi đổi config.
- **Trong suốt:** twin BLENDED chỉ hiển thị khi đang mờ dần; frame đặc luôn render bằng material dithered.
- **Camera chỉ được chuyển động trong intro của SIDE_BY_SIDE**, để nối liền từ shot single-model. Mọi điểm cắt khác phải liền mạch (SSIM ≥ 0.98) trừ khi khai báo `cut_from_previous: "hard"`.
- **Git là nguồn sự thật cho file nguồn**; `PACKAGE_MANIFEST.sha256` được sinh từ `git ls-files`. Frame/video/blend là output được sinh ra, không commit.
- **M3 không dùng multi-agent:** pipeline tuyến tính có gate; chỉ thêm dữ liệu (nguồn, narration, timing) và bước hậu kỳ (audio, ghép, phụ đề). Pilot Suffolk dựa trên nguồn chính quyền địa phương, phạm vi hẹp.

## Bổ sung 2026-10-27 (M3) — không thay thế các quyết định ở trên
- **TTS = OmniVoice cục bộ** (người dùng chỉ định), qua HTTP API Gradio của demo, **chỉ localhost**. Không dùng dịch vụ TTS ngoài. Adapter tách khỏi pipeline (`integrations/`).
- **Không clone giọng người thật.** Người dẫn chuyện = voice design → giọng mẫu tổng hợp → clone (để âm sắc nhất quán).
- **License TTS là một gate riêng (G2)**: `LICENSE_REVIEW_REQUIRED` cho phép preview nội bộ, chặn xuất bản.
- **Narration-first:** timing của video chạy theo audio đo được; không bao giờ ép thời lượng giọng. Shot chỉ được nới dài cho animation.
- **Xác minh nguồn ≠ duyệt biên tập:** SOURCE_VERIFIED dùng được cho bản nháp; xuất bản cần EDITORIALLY_APPROVED do người duyệt.
- **Take TTS gốc được commit** (sinh ngẫu nhiên nên không tái lập được); audio beat, track, mix thì sinh lại.
- **Mỗi state kiến trúc là một kết hợp thực sự** (độ dốc + hình học lớp phủ + vật liệu), không chỉ là đổi màu; `structure_from` cho các lần thay lớp phủ trên cùng một kết cấu.

## Bổ sung 2026-10-27 (M3.5)
- **Thay quyết định "License TTS = LICENSE_REVIEW_REQUIRED" của M3:** trọng số OmniVoice hiện công bố CC-BY-NC (cùng byte với bản đã cài), nên OmniVoice là **NOT CLEARED** cho xuất bản thương mại và chỉ còn dùng cho preview nội bộ.
- **Workflow TTS độc lập provider:** `NarrationAdapter` + registry hạng quyền. Hạng quyền nằm trong khóa cache audio. Provider xuất bản do người chọn.
- **Không gợi ý trình tự tuyến tính thatch → ngói → slate:** SC_005 đổi thành hai công trình đặt cạnh nhau. REPLACE_PARTS chỉ dùng khi nguồn mô tả đúng việc thay thế đó (CLM_103 "some").
- **Nhãn chữ trên mô hình** (SIDE_BY_SIDE `labels`) là chữ hiển thị claim, nên cũng thuộc gói duyệt biên tập.
- **Kích thước viên ngói/slate được cường điệu khoảng 1.5 lần** để đọc được ở 640×360, giữ tỷ lệ slate:ngói khoảng 2:1. Đây là minh họa, không phải số đo.
- **Cache render theo nhóm phụ thuộc**; trường lạ được coi là trường hình ảnh (an toàn).
- **Preset `production_test` (1920×1080) chỉ để render ảnh tĩnh**; render chuỗi frame 1080p phải chờ các khung đại diện qua QA và gate.

## Bổ sung 2026-10-27 (M4)
- **Spec có ràng buộc, không phải sinh từ câu chữ tự do:** họ/biến thể đã đăng ký, tham số có kiểu và khoảng giá trị, kiểm tra tương thích hình học. Thêm họ mới bằng code + test (`docs/m4/M4_ARCHITECTURE_MODELING.md` §7).
- **Planner thuần Python, Blender chỉ hiện thực hóa:** thành phần, bbox, nối liền và chữ ký tái lập kiểm tra được offline; BVH trong Blender là bản kiểm tra chính xác.
- **Một thành phần = một object**; phần lặp lại được gộp (ván, thanh giàn). Voussoir để riêng từng viên vì phải bung theo hướng bán kính. Mesh giống nhau dùng chung một datablock; không apply modifier.
- **Mọi asset M4 là ILLUSTRATIVE.** Cầu không phải bản dựng lại công trình thật, cũng không phải thiết kế kết cấu. Mẫu giàn có ghi nguồn (Wikipedia, CLM_001/002 SOURCE_VERIFIED), nhưng điều đó không nâng mức độ chính xác của asset.
- **Ba cầu dùng chung một khu đất (khe 24 m, mặt cầu ở cao độ 5.0 m)** để so sánh tương đương; validator chặn asset không khớp khu đất.
- **REPLACE_PARTS chỉ giữa các variant tương thích** (Pratt ↔ Warren trên cùng khung), không thay nguyên cây cầu này bằng cây cầu khác. Chuyển giữa các họ cầu dùng cắt cứng.
- **SIDE_BY_SIDE `STACK`** (mở rộng nhỏ, không viết lại template) cho mô hình dài: mỗi mô hình một hàng trên màn hình.
- **Ảnh preview:** JPEG được track trong git, PNG để cục bộ.

## Bổ sung 2026-10-28 (M5)
- **Lập kế hoạch hình ảnh tất định, không có LLM khi chạy.** Tác giả viết beat có cấu trúc (lời thoại, ý đồ, khái niệm, claim); `planner/` quyết định asset, template, shot, camera và frame theo luật cố định. Cùng đầu vào thì ra cùng kế hoạch (có test so từng byte). LLM chỉ có mặt ở bước viết beat, và beat là file được review.
- **Planner nằm trước engine, không thay engine.** Kế hoạch được biên dịch thành đúng hợp đồng M2–M4 (`states.json`, `storyboard.json`). Engine chỉ thêm các trường tùy chọn: builder `none`, `build_variants`, `camera_focus`/`camera_safe_band`, `highlight.ghost`.
- **Không bỏ qua beat lặng lẽ, không lấp chỗ trống bằng animation không liên quan.** Mỗi beat có đúng một trạng thái coverage. Kế hoạch có beat không thực thi được thì không biên dịch được.
- **Thiếu năng lực thì báo thiếu:** `NEW_ASSET_REQUIRED` kèm nhiệm vụ sinh, `MISSING_TEMPLATE` (bản đồ, mũi tên lực), `EVIDENCE_BLOCKED`. Không sửa catalog hay từ vựng để che yêu cầu.
- **REPLACE_PARTS chỉ giữa trạng thái chung khung** (hoặc từ khu đất trống, hoặc hai mái trên cùng một nhà). Hai họ khác nhau thì dùng SEQUENTIAL_STATES, tức là cắt cứng.
- **Asset sinh mới (GENERATE) là ILLUSTRATIVE và thuộc về dự án** (`planning/generated_assets/`), không bao giờ ghi vào catalog. Mức chính xác yêu cầu cao hơn mức của asset thì `BLOCKED_MISSING_EVIDENCE`.
- **SHOW_EVOLUTION cần chronology đã duyệt biên tập.** Pilot M5 cố ý không trình bày gỗ → đá → thép như một dòng thời gian.
- **Timing PROVISIONAL là ước lượng, có ghi nhãn.** AUDIO_LOCKED lấy từ `schedule` của M3. Thiếu thời gian thì chọn chiến lược nhẹ hơn hoặc báo `TIMING_CONFLICT`. Không bao giờ cắt ngắn hay tăng tốc chuyển động.
- **Nhóm liên tục camera:** shot nối bằng cắt match dùng chung một camera khóa và một tập variant được dựng. Cache chỉ phụ thuộc các variant shot đó dựng.
- **Phần phát sáng phải nhìn thấy được.** QA Blender đo phần bị che bằng tia. Phần thường bị che (dầm dọc dưới ván…) được làm lộ bằng cách cho phần che trong suốt (`ghost`), không phải bằng cách đổi camera.

