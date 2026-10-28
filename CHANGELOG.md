# Changelog

## 0.5.0 — 2026-10-28 — M5: lập kế hoạch hình ảnh tự động và điều phối storyboard → Blender (nhánh `m5-autonomous-visual-planning`)
- **Planner tất định** (`planner/`, thuần Python, không LLM khi chạy): beat → ý đồ hình ảnh → asset → template → shot/camera → timing → storyboard thực thi được. Cùng đầu vào thì ra cùng kế hoạch, giống từng byte.
- **Hợp đồng mới:**
  - `schemas/narrative_beats.schema.json` (`script/visual_beats.json`) và `schemas/visual_plan.schema.json` (`storyboard/visual_plan.json`).
  - `config/visual_vocabulary.json`: khái niệm khu đất, công trình, thành phần; `where`, `supported`, `ambiguous_if_multiple`, `ghost_roles`.
  - `config/visual_planning.json`: camera theo lớp tỷ lệ, luật timing, ngân sách chuyển động.
- **9 ý đồ hình ảnh** với chiến lược theo thứ tự ưu tiên (13 chiến lược ghép từ template có sẵn). Từ khóa trong lời thoại chỉ dùng để cảnh báo khi lệch với ý đồ khai báo, không bao giờ tự sửa ý đồ.
- **Chọn asset:** REUSE_EXISTING / ADAPT_EXISTING_ASSET (adapter cho mái M2) / GENERATE_FROM_SUPPORTED_FAMILY (spec ILLUSTRATIVE ghi trong dự án) / NEW_ASSET_REQUIRED (kèm nhiệm vụ sinh) / BLOCKED_MISSING_EVIDENCE. Mỗi lựa chọn có lời giải thích; catalog chỉ đọc.
- **Ánh xạ thành phần ngữ nghĩa** theo role/group, với ID ổn định. Thiếu hoặc mơ hồ đều là lỗi, được kiểm tra trước khi chọn chiến lược.
- **Camera:** 6 chế độ → preset có sẵn; COMPONENT_CLOSEUP (`camera_focus`, `camera_safe_band`); nhóm liên tục camera (`build_variants`, cắt match/cứng); kiểm tra hiển thị offline.
- **Timing:** PROVISIONAL (ước lượng, có ghi nhãn) hoặc AUDIO_LOCKED (`script/timing.json` đã khóa). Thời lượng tối thiểu lấy từ motion planner thật; thiếu thời gian thì chọn chiến lược nhẹ hơn hoặc báo `TIMING_CONFLICT`, không bao giờ cắt ngắn.
- **Báo cáo coverage** `qa/VISUAL_COVERAGE.md` + `visual_coverage.json` (7 trạng thái).
- **CLI:** `plan-visuals` (exit 4 khi không thực thi được), `validate-plan` (kiểm tra độc lập + G0), `build-shots`.
- **Engine (tùy chọn, tương thích ngược):**
  - builder `none` (khu đất trống);
  - `build_variants`, `camera_focus`, `camera_safe_band`;
  - `highlight.ghost` cho HOLD (phần che chuyển trong suốt);
  - QA Blender: camera theo nhóm liên tục, và kiểm tra mới **`highlight_targets_visible`** (bắn tia đo phần bị che).
- **Cache:** `states_geometry`/`assets` chỉ băm các variant mà shot dựng. Đổi asset cầu đá chỉ làm cũ 4/13 shot.
- **Pilot** `projects/bridge-story-m5` "Three Ways to Span a Gap": 8 beat → 13 shot, 72.375 s, không lời, INTERNAL ONLY, 5 claim SOURCE_VERIFIED. QA Blender 163/163, media QA PASS, smoke test 2 shot.
- **Fixture tổng quát hóa** `projects/roof-plan-m5` (SYNTHETIC): mái nhà qua adapter, layout ROW, QA Blender 52/52.
- **Sửa lỗi tìm ra khi xem hình:**
  - dầm dọc bị ván che (chỉ 14 % nhìn thấy) → ghost, 82 %; lỗi này cũng có ở pilot M4 SC_001 và đã sửa luôn;
  - ảnh tĩnh của shot lắp ráp toàn khu đất trống → marker `incoming_end`;
  - compiler giữ `audio_timing_locked` chỉ khi kế hoạch là AUDIO_LOCKED.
- **Tài liệu** `docs/m5/` (kiến trúc, giao thức lập kế hoạch, chọn asset, báo cáo QA + hiệu năng). Cập nhật AGENTS, DECISIONS, CACHE_DEPENDENCIES, ANIMATION_LIBRARY.
- **Test:** `tests/test_m5_planner.py` (34), `tests/test_blender_m5.py` (2). Hồi quy: QA Blender roof-evolution 64/64, suffolk-roofs 71/71 (gate không đổi), bridge-structure-evolution 92/92.

## 0.4.0 — 2026-10-27 — M4: dựng hình kiến trúc thủ tục và thư viện asset (nhánh `m4-architectural-modeling`)
- **Hệ thành phần ngữ nghĩa** (`engine/arch/semantic.py`):
  - Mỗi thành phần có ID ổn định, loại (30 `SEMANTIC_TYPES`), vật liệu, nhóm, variant sở hữu, transform, mesh cục bộ, layer, hướng bung, vai trò animation, bevel, evidence.
  - Có bbox và chữ ký mesh để dùng chung mesh và kiểm tra tái lập.
- **Thư viện hình học** (`engine/arch/primitives.py`, `library.py`, thuần Python): box, thanh, cung vành khăn (voussoir), lăng trụ đa giác, trụ tròn; lặp có khe mạch, dầm, cột, giằng chéo X, vòng vòm và keystone, outline spandrel, mũi cản nước, giàn song song Pratt/Warren, bản nút.
- **Spec kiến trúc** (`schemas/architecture_asset.schema.json`, `engine/arch/assets.py`):
  - Registry họ/biến thể với khoảng tham số, kiểm tra tương thích hình học và thông báo lỗi dễ đọc.
  - Ba mức độ chính xác: ILLUSTRATIVE / REFERENCE_BASED / HISTORICALLY_VERIFIED (mức cao hơn phải có bằng chứng).
- **Ba họ cầu và khu đất** (`engine/arch/families/`): timber_beam, stone_arch (3 hoặc 5 vòm), steel_truss Pratt/Warren dùng chung khung; site river_crossing. Tổng cộng 6 spec trong `asset_library/architecture/`.
- **Tích hợp engine M2/M3 (không viết engine mới):**
  - Builder `architecture_asset` (dùng cho cả base và variant), mesh dùng chung, bevel không phá hủy, collection theo nhóm.
  - `structure_from` tổng quát: asset kế thừa mọi phần không mang vai trò REPLACE.
  - SIDE_BY_SIDE `layout: "STACK"` với nhãn theo hàng.
  - Camera orthographic tự lùi ra khi mép dưới khung nằm thấp hơn mặt đất.
  - Preset camera BRIDGE_THREE_QUARTER, ELEVATION, TOP, BRIDGE_STACK.
- **Vật liệu dùng chung** `asset_library/materials/stylized_materials.json` (13 vật liệu thủ tục, không texture); `add_units` có thêm tham số trục cho hàng đá.
- **QA và gate G4-A…E:**
  - Kiểm tra offline (`engine/arch/checks.py`).
  - Kiểm tra trong Blender (`engine/arch/asset_scene.py`): nối liền và độ xuyên sâu bằng BVH, dựng hai lần, gắn tag ngữ nghĩa.
  - Preview đa góc (ba phần tư, mặt đứng, mặt bằng, bung).
  - Lệnh CLI: `asset-check`, `asset-render`, `asset-catalog`. Bộ nhớ đo bằng `/usr/bin/time -l`.
- **Catalog** `asset_library/catalog/catalog.json` + `CATALOG.md`: metadata, nguồn gốc, vật liệu, preview, kết quả kiểm tra.
- **Pilot** `projects/bridge-structure-evolution` (29.5 s, không lời dẫn, sinh bằng `tools/make_bridge_pilot.py`): QA Blender 86/86, media QA PASS.
- **Cache render** khóa v3: đệ quy `engine/**` và nhóm phụ thuộc `assets` (spec được tham chiếu + thư viện vật liệu).
- **Test:** 138 (thêm `tests/test_m4_arch.py` 26 test, `tests/test_blender_m4.py` 5 test, gồm phép thử ngược cho BVH). QA Blender roof-evolution 63/63, suffolk-roofs 70/70; trạng thái xuất bản của suffolk không đổi.

## 0.3.5 — 2026-10-27 — M3.5: duyệt biên tập, quyền TTS, hoàn thiện hình ảnh (nhánh `m3.5-editorial-polish`)
- **Audit license** (`docs/licensing/TTS_LICENSE_AUDIT.md`):
  - Model card OmniVoice hiện ghi trọng số là **CC-BY-NC** (do dữ liệu Emilia), và trọng số này trùng từng byte với revision đã cài → OmniVoice **NOT CLEARED** cho xuất bản thương mại, chỉ dùng cho preview nội bộ.
  - Đã so sánh 7 phương án xuất bản (Kokoro, Piper, ElevenLabs, Azure, Google, Polly, OpenAI) và phương án giọng người thật. Không đăng ký hay mua dịch vụ nào.
- **Workflow TTS độc lập provider:**
  - Interface `NarrationAdapter` gồm adapter OmniVoice và adapter thu âm người thật; registry `config/tts_providers.json` có hạng quyền; `narrate --purpose publication` từ chối provider chưa được cấp quyền.
  - Khóa cache audio v2 gồm: model, voice id, chữ đọc thực tế và hạng quyền.
  - 15 take M3 được nhận lại (đổi khóa), không sinh lại; audio beat trùng từng byte.
- **Gói duyệt biên tập** (`projects/suffolk-roofs/review/EDITORIAL_APPROVAL_PACKAGE.md`): 7 claim đều đã đối chiếu lại với PDF (cùng sha256 với M3) và với trang web theo đúng URL đã cho; có đề xuất cho từng claim và danh sách ký duyệt. **Không tự duyệt claim nào.** Validator yêu cầu hồ sơ duyệt (`editorial_approval`) gắn với narration revision.
- **Lời dẫn `m3.5-r1`:** 4 câu sửa vì độ chính xác (thêm "originally"; 45–60°; "Slate is different."; câu kết bỏ suy diễn ngược) + sửa phát âm B1.s0. 9/14 take giữ nguyên. Tổng thời lượng 73.0 → 75.542 s.
- **Trình tự tuyến tính:** SC_005 không còn "thay ngói bằng slate trên cùng một nhà", mà là hai công trình đặt cạnh nhau; SC_006 cắt cứng; đã xóa transition ngói → slate.
- **Phát âm "Babergh":** override chỉ cho TTS (`[B EY1 B AH0]`), chữ viết giữ nguyên; có clip bằng chứng và danh sách nghe; trạng thái `PENDING_LISTENING_REVIEW`. Alias ASR chỉ dùng để tính WER.
- **Phụ đề:**
  - 21 cue theo cụm từ. Ranh giới lấy từ timestamp theo từ của Whisper rồi đặt vào điểm năng lượng thấp nhất của audio thật. Chữ lấy từ kịch bản.
  - Dòng dài nhất 41 ký tự, 1–2 dòng mỗi cue. Báo cáo `qa/SUBTITLE_QA.md`.
- **Hình ảnh:**
  - Hoa văn viên ngói/slate (shader, căn theo gân hàng), nhãn chữ dưới mô hình trong SIDE_BY_SIDE.
  - Sửa tường hồi và đỉnh tường xuyên qua mái slate mỏng (có từ M3).
  - Ảnh tĩnh ở 960×540 và 1920×1080 (`production_test`, chỉ ảnh tĩnh); ảnh trước/sau.
- **Cache render theo nhóm phụ thuộc** (`tools/render_cache.py`, `cache-report`): sửa chữ, claim hay timeline không làm render lại.
- **Gate:** `pipeline/gates.py` với TECHNICALLY_VALIDATED / EDITORIAL_REVIEW_PENDING / TTS_RIGHTS_PENDING / PUBLICATION_READY; gate cuối kiểm tra nguồn gốc audio và xác nhận phát âm; G4/G5 phát hiện báo cáo cũ. MP4 có audio chưa được cấp quyền mang tên `*_INTERNAL.mp4` kèm metadata.
- **QA và độ tin cậy:**
  - Kiểm tra Blender mới: `covering_hides_structure`, `labels_in_band` (cả kiểm tra bị che khuất). Phép thử ngược cho thấy cả hai bắt được lỗi cũ.
  - Sửa: `check-blender` từng in ra báo cáo **cũ** khi Blender bị lỗi; QA layout SIDE_BY_SIDE từng đọc `matrix_world` cũ của object bị ẩn; `audio_probe` từng ném `KeyError` với WAV rỗng.
- **Test:** 107 (thêm 30 ở `tests/test_m35.py`). QA Blender: suffolk 70/70, roof-evolution 63/63.

## 0.3.0 — 2026-10-27 — M3: pipeline phim có lời dẫn + OmniVoice cục bộ (nhánh `m3-narrative-pipeline`)
- **OmniVoice:** đã khảo sát project người dùng (không sửa gì); khởi động demo Gradio **chỉ ở localhost** (`--ip 127.0.0.1 --no-asr`, tắt analytics, HF offline); hợp đồng API xác nhận qua `/gradio_api/info`. Adapter stdlib `integrations/tts/omnivoice.py` ghép tham số theo nhãn, có timeout/retry, lỗi rõ ràng, kiểm tra audio (`integrations/audio_probe.py`).
- **License:** code + trọng số Apache-2.0, nhưng tokenizer Higgs Audio v2 đi kèm theo Boson Higgs Audio 2 Community License → `LICENSE_REVIEW_REQUIRED`; chặn xuất bản. Giọng = voice design → giọng mẫu tổng hợp → clone (không giọng người thật).
- **Pipeline** (`pipeline/`): `narration` (sinh theo câu, cache theo nội dung, sinh lại khi lỗi, audio beat ghép ở mức mẫu), `asr_check` (Whisper offline, WER), `beat_scheduler` (narration-first, frame chính xác, mốc neo, khóa timing), `assemble` (track, loudnorm 2 lượt, ghép, SRT cấp câu, QA), `storyboard_report`.
- **Engine:** `covering.style` (thatch / plain_tile / slate + ngói nóc + vật liệu có texture thủ tục), `structure_from`, card 2D `engine/diagram.py` (font tích hợp), chốt chặn "không animate phần đang bị ẩn".
- **Validator/CLI:** trạng thái claim PROVISIONAL / SOURCE_VERIFIED / EDITORIALLY_APPROVED / REJECTED (bắt buộc locator + excerpt), kiểm tra narration/license/beat/khóa timing, card; lệnh `tts-check`, `narrate`, `asr-check`, `schedule`, `smoke`, `assemble`, `gates`. Schema `narration`, `sources` v2.
- **Pilot `suffolk-roofs`:** 73.0 s; QA Blender 66/66; 77 unit test; smoke + bản đầy đủ: lệch A/V 0 ms, −16.5 LUFS; gate → PREVIEW NỘI BỘ, chưa sẵn sàng xuất bản.
- **MCP:** gỡ server `blender` ở scope local (đã sao lưu `~/.claude.json`); scope project (2.2.4, safe mode, không telemetry) đang có hiệu lực; tool + việc chặn của safe mode đã kiểm chứng.
- **Lỗi đã sửa trong M3:** đọc vội (sinh lại), mất bản ghi cache (lưu theo từng đoạn), intro làm hiện mái tranh bị ẩn ở SIDE_BY_SIDE, ngói nóc ra ngoài khung khi exploded, mô tả SC_002 sai so với hình, ngắt dòng phụ đề.

## 0.2.5 — 2026-10-27 — M2.5: ổn định hóa, QA qua MCP, sẵn sàng cho M3
- **Git:** giữ nguyên commit `init` của người dùng; baseline M2 được commit (`75487d3`, tag `m2-baseline`); `.gitignore` bổ sung media QA, `.blend@`, file tạm, `.env*`, `.claude/settings.local.json`.
- **MCP:** gọi thật `get_addon_status`/`get_scene_info`/`execute_blender_code`/`look` qua stdio (21/21 lệnh trước khi sửa, kèm lượt kiểm tra lại sau khi sửa) trên một phiên bản Blender riêng mở bản sao của các scene. Đã xác định vì sao addon không lắng nghe (Blender mở trước khi addon được cài) và phát hiện cấu hình scope local ghi đè safe mode (chỉ ghi lại, không tự sửa).
- **Sửa #1 — rafters xuyên tường:** cắt đầu dưới rafters 1 mm trên đỉnh tường (`box_object(clip_below_z=…)`). Kiểm tra mới `structure_clear_of_shared_at_rest` FAIL trên geometry M2, PASS sau khi sửa.
- **Sửa #2 — highlight:** chỉ còn tự phát sáng bằng màu của chính phần đó (bỏ pha màu nhấn); mái A giữ màu graphite.
- **Sửa #3 — ánh sáng phẳng:** chọn L3 sau khi so 4 biến thể ở 960×540: nắng chính từ trước-trái và cao (bóng ngắn, không chạm model bên cạnh), fill 0.3, world 0.4, AgX `Medium High Contrast`, ray tracing Eevee, smooth shading + weighted normals cho cạnh vát (edge highlight). Mọi thông số nằm trong `config/visual_style.json`.
- **Sửa #4 — nhiễu dithering:** twin BLENDED chỉ hiển thị khi đang mờ dần (`motion.split_fades`). Frame tĩnh và điểm cắt không đổi; đã so sánh với dithered 64/128 mẫu và BLENDED cho mọi object.
- **Sửa #5 — cắt cứng SC_004 → SC_005:** `SIDE_BY_SIDE.intro` (camera lùi ra, model đứng yên). Đã so sánh với dissolve bằng FFmpeg. SC_001 2.0 s, SC_005 4.5 s, tổng vẫn 20.0 s.
- **Sửa #6 — manifest:** lệnh `python3 tools/cli.py manifest [--check]` tạo lại từ `git ls-files`.
- **Sửa #7 — frame v0.1:** 144 PNG được nén không mất dữ liệu (đã kiểm checksum) vào `qa/baseline_v0_1/v0_1_preview_frames.tar.gz` rồi mới xóa bản rời; file `.blend` của v0.1 được chuyển vào cùng thư mục.
- **QA:** 58 kiểm tra Blender (thêm structure/twins/intro; chữ ký tái lập chỉ băm những gì được render); media QA đo SSIM tại điểm cắt (`cut_from_previous`); 49 unit test. CLI chạy Blender dưới `caffeinate -i` (máy ngủ khi idle từng làm một frame đứng 15 phút).
- **Output review riêng:** `--preset review` ghi vào `output/stills_review/`, `output/shots_review/`, `*_review.mp4`; preview 640×360 giữ nguyên tên cũ.
- **M3:** kế hoạch + brief nghiên cứu + storyboard nháp trong `docs/m3/` (chưa sản xuất).

## 0.2.0 — 2026-10-26 — M2: Engine biến đổi trực quan tái sử dụng v1
- Template mới: `REPLACE_PARTS`, `EXPLODED_VIEW`, `SIDE_BY_SIDE`, `HOLD` (+ highlight), điều khiển hoàn toàn bằng `storyboard.json` → `animation`.
- Planning bằng Python thuần (`engine/motion.py`, `templates.py`, `spec.py`, `framing.py`), nên validator kiểm tra được timing, ownership và option ngay ở G0. Keyframe được ghi với interpolation tường minh (`engine/animate.py`, hỗ trợ cả slotted actions của 5.x).
- Builder có metadata: mái gable gồm tấm phủ, rafters, ridge beam, tường hồi; base có thêm ceiling joists. `states.json` v2 có quyền sở hữu tường minh (v1 vẫn tương thích).
- Mỗi shot là một scene độc lập (`engine/shot_builder.py`) với camera ortho khóa, fit theo hình học. Ánh sáng chuyển sang sun (không phụ thuộc vị trí); mặt đất liền khối.
- CLI: `still` (key stills), `preview` (render theo shot có cache + MP4 theo shot + MP4 đầy đủ + media QA + contact sheet / dải tiến trình), `shot`, `check-blender`. Gọi Blender với `--python-exit-code 1`.
- QA: `engine/qa_checks.py` (50 kiểm tra), 38 test offline mới + 1 test tích hợp Blender (tổng 43 cùng 4 test cũ).
- Pilot roof-evolution: 20 s, 5 shot. Đã sửa: dải nền ở mép trên (clip_end), highlight làm đổi tông màu, bóng đổ lên model bên cạnh, cấu kiện đặc bị khung cắt (2 trường hợp), móng nổi 5 cm.
- Loại bỏ: cơ chế thu nhỏ còn 1% của v0.1 (`engine/transform.py` được giữ lại làm tham khảo, đánh dấu DEPRECATED, không còn được import).

## 0.1.1 — 2026-10-26
- Pilot `roof-evolution` render lần đầu trên Mac thật: macOS 26.6.2, Apple M4 Pro 24 GB, Blender 5.2.2 LTS, FFmpeg 9.0.1, Python 3.14.6.
- Fix framing (`engine/scene.py`): đỉnh mái B (48°, ~5.2 m) bị cắt 19% ở mép trên, móng hụt 3% ở mép dưới. Camera giờ nhắm z=2.1 (đèn vẫn nhắm z=1.6), `ortho_scale` 10.1 → 14.0; đo bằng `world_to_camera_view` trên geometry thật: cả A và B có lề dọc ~6%.
- Preview 6 s / 144 frame / 640×360 render trong ~35 s; MP4 h264 yuv420p, không black frame.
- Cài MCP for Blender 2.2.4 (`ahujasid/mcp-for-blender`, commit `febcd90`, MIT) sau khi review mã: wheel PyPI khớp source, addon SHA-256 `8e193a24…7083`. Addon → `~/Library/Application Support/Blender/5.2/scripts/addons/blender_mcp.py` (đã enable). Server đăng ký ở `.mcp.json` (scope project), ghim version, `DISABLE_TELEMETRY=true`, `BLENDER_MCP_SAFE_MODE=1`, localhost:9876. Pipeline CLI dùng `--factory-startup` nên không nạp addon.

## 0.1 — 2026-10-22
- Chốt narrative-first architecture 3D pipeline.
- Tạo chính sách AI coding, workflow, JSON schemas, validation, Mac CLI, sample roof transitions.
- Thêm unit tests và tài liệu đầu vào cho Codex/Claude.
- MVP chưa được render bằng Blender thực tế trong môi trường đóng gói.
