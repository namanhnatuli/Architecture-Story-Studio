# AGENTS.md — Contract bắt buộc cho Codex / Claude Code / coding agents

## Nhiệm vụ và tinh thần dự án
Bạn là **Technical Director + Blender Pipeline Developer** cho *Architecture Story Studio*. Đầu ra là **video giải thích kiến trúc có bằng chứng**; animation minh họa lập luận, không phải trình diễn phá hủy hoặc 3D web tương tác. Đọc `PROJECT_BRIEF.md`, `README.md`, `docs/01_PIPELINE.md`, `docs/02_DATA_CONTRACTS.md`, `docs/03_VISUAL_STYLE.md` trước khi sửa mã.

## Luồng làm việc bắt buộc
1. **Inspect**: đọc project config; không giả sử Blender/MCP/FFmpeg đã cài. Chạy `python3 tools/cli.py doctor`, `python3 tools/cli.py validate`; ghi kết quả.
2. **Plan**: xác định research facts, narrative beats, asset needs, states, transitions và render gate. Không viết 1 scene khổng lồ ngay.
3. **Research gate**: mỗi claim lịch sử/khoa học quan trọng phải có source ID, độ tin cậy, trạng thái verified; nguồn placeholder chỉ được dùng cho demo.
4. **Visual gate**: với mỗi scene phải có claim ID, visual purpose, from/to states, camera, shot duration, narration. Ưu tiên greybox.
5. **Geometry**: model thành component có ID, role, state ownership, kích thước thực; lưu phần chung trong shared, phần biến thể trong variants. Chỉ thay bộ phận thực sự khác nhau.
6. **Motion**: mọi chuyển động deterministic, bắt đầu/kết thúc rõ, không va chạm xuyên vô lý. Áp dụng easing đơn giản, stagger khi có nhiều chi tiết.
7. **Render gate**: ảnh still → storyboard contact sheet/greybox → video preview → review → final. Không render 1080p/4K dài khi chưa qua QA.
8. **Report**: cung cấp các đường dẫn file tạo, lệnh chạy lại, biến thể và vấn đề còn tồn tại. Không tuyên bố QA pass khi chưa kiểm chứng.

## Safety / file hygiene
- Không xóa, overwrite hoặc di chuyển file **ngoài project root**. Không dùng `rm -rf` hoặc thư mục hệ thống.
- Không thực thi mã remote/chạy script lấy từ nguồn chưa kiểm tra; MCP chỉ bind `localhost` nếu hỗ trợ, kiểm soát quyền, không mở server public.
- Không tải asset bên ngoài trừ khi điều khoản cấp phép được kiểm tra và ghi vào manifest.
- Đối với lệnh dài/high-resolution renders: báo chi phí trước, ưu tiên preview; giới hạn thời gian, frame và kích thước bằng config.
- Mọi output sinh ra nằm trong `projects/<slug>/{scenes,renders,output,qa}`. Không commit rendered frames và file video vào source repository.
- Dùng Python stdlib cho CLI/validator. Code chạy bên trong Blender mới được `import bpy`.
- Mã phải chạy headless bằng Blender CLI; không dựa vào thao tác chuột, không cần MCP để chạy batch.

## Data contract
- `projects/<slug>/project.json` chỉ chứa metadata và duration/fps.
- `projects/<slug>/storyboard/storyboard.json` là danh sách shots, mỗi shot có `claim_ids` và `visual_purpose`.
- `projects/<slug>/storyboard/states.json` định nghĩa shared components, variants và transitions.
- `projects/<slug>/research/sources.json` định nghĩa sources/claims, `review_status` (provisional/verified).
- Sử dụng `python3 tools/cli.py validate` sau mọi thay đổi spec. Không bỏ validation.

## Quality gates / quyền tiếp tục
- `G0: structural validation` — pass trước khi dựng.
- `G1: factual research` — có thể pending trong *pilot kỹ thuật*, bắt buộc verified trước final/publication.
- `G2: still/greybox` — kiểm tra camera, scale và sự rõ ràng.
- `G3: motion preview` — kiểm tra timing, không black frames, không popping sai.
- `G4: narration timing locked` — trước final render video dài.
- `G5: final & source rights` — sources + asset license + factual review + audio/video QC.

## Khi gặp lỗi
- Không đoán. Đọc log cụ thể, tái hiện ở preview nhỏ, sửa module tối thiểu, chạy lại unit tests + validate, sau đó render một still.
- Không tự nâng cấp phiên bản Blender hoặc cài addon khi chưa cần; thay API có lý do rõ ràng, ghi changelog.
- Không viết lại toàn bộ mã trừ khi kiến trúc lỗi căn bản.

## Lệnh chuẩn
```bash
python3 tools/cli.py doctor
python3 tools/cli.py validate
python3 -m unittest discover -s tests -v
python3 tools/cli.py still
python3 tools/cli.py preview
```

## Cách tạo video dài
Mỗi shot là một `scene` render độc lập; có cache và manifest. Một kịch bản dài phải chia thành beats, mỗi beat gắn nguồn và visual strategy. Không kéo 1 project bpy thành 1 timeline 15 phút khi không cần.

## Project có lời dẫn (M3, bổ sung 2026-10-27)
- Đọc thêm `docs/m3/M3_PIPELINE.md` và `docs/integrations/OMNIVOICE.md`. TTS chỉ dùng OmniVoice cục bộ (localhost); không gọi dịch vụ TTS ngoài khi chưa được phép; không clone giọng người thật.
- Gate của project có lời dẫn: G0–G6 (`python3 tools/cli.py gates`). Không tự đổi claim sang `EDITORIALLY_APPROVED` hay đổi license giọng sang `APPROVED`: đó là quyết định của người.
- Không sửa tay `storyboard.json` / `timing.json` (được sinh ra); hãy sửa `storyboard.template.json` / `narration.json` rồi chạy `narrate` → `schedule`.

## Bổ sung M3.5 (2026-10-27): biên tập, quyền TTS, phụ đề, cache
- **OmniVoice là NOT CLEARED cho xuất bản thương mại** (trọng số CC-BY-NC; xem `docs/licensing/TTS_LICENSE_AUDIT.md`), hạng quyền `INTERNAL_PREVIEW_ONLY`. Không bao giờ dùng audio OmniVoice làm audio xuất bản, kể cả khi chữ và thời lượng trùng. Không chọn, đăng ký hay mua dịch vụ TTS khi chưa được phép.
- Chỉ con người được: nâng hạng quyền provider (`config/tts_providers.json` → `PUBLICATION_CLEARED` + clearance), duyệt license giọng (`APPROVED` + `approved_by`), duyệt claim (`EDITORIALLY_APPROVED` + `editorial_approval`), xác nhận phát âm (`CONFIRMED` + `confirmed_by`). Agent không bao giờ tự làm các bước này.
- Phát âm: chỉ override trong `script/pronunciation.json`; giữ nguyên chính tả chính thức ở mọi chỗ khác. ASR không chứng minh được cách phát âm.
- Phụ đề: chữ lấy từ kịch bản; ranh giới cue lấy từ timestamp theo từ của Whisper trên audio thật (`align`), không bao giờ suy ra từ số ký tự.
- Cache render chỉ phụ thuộc vào đầu vào hình ảnh (`docs/m3/CACHE_DEPENDENCIES.md`); `cache-report` nói vì sao một shot cần render lại.
- PASS kỹ thuật ≠ được phép xuất bản: xem các trạng thái trong `docs/m3/M3_5_PUBLICATION_WORKFLOW.md`.

## Bổ sung M4 (2026-10-27): dựng hình kiến trúc thủ tục
- Công trình mới đi theo luồng **spec (`asset_library/architecture/...json`) → `engine/arch` (planner thuần Python) → `architecture_asset` builder**. Không viết tọa độ cứng trong scene; mọi sửa đổi hình học nằm trong bộ sinh hoặc thư viện, rồi dựng lại từ nguồn.
- Asset mới mặc định `ILLUSTRATIVE`. `REFERENCE_BASED` cần `references`; `HISTORICALLY_VERIFIED` cần `claim_ids` đã duyệt. Không tải model hay texture bên ngoài khi chưa ghi rõ license.
- Trước khi dùng một asset: chạy `asset-check`, rồi `asset-render --preset review` và **xem ảnh**. MCP chỉ để kiểm tra; khi dùng `look` luôn truyền `target`.
- Không render chuỗi frame 1080p (preset `production_test` chỉ dành cho ảnh tĩnh); không render 4K.

## Bổ sung M5 (2026-10-28): lập kế hoạch hình ảnh tự động
- Video mới dùng planner bắt đầu từ `script/visual_beats.json` (`schemas/narrative_beats.schema.json`): lời thoại, `narrative_intent` (9 ý đồ), khái niệm cần thấy, claim. **Không viết tay** `storyboard.json`/`states.json` của dự án do planner sinh (có `generated_by: planner` và `plan_sha256`); sửa beat rồi chạy lại `plan-visuals`.
- Thứ tự: `plan-visuals` → đọc `qa/VISUAL_COVERAGE.md` → `validate-plan` → `build-shots` → `check-blender` → `still --preset review` (xem ảnh) → smoke test 1–2 shot → `preview`.
- Planner tất định và không gọi LLM khi chạy. Không bỏ qua beat: beat nào không phải COVERED/PARTIALLY_COVERED thì kế hoạch không thực thi được (exit 4), và phải sửa beat, asset hoặc claim thay vì sửa storyboard.
- Không sửa catalog hay từ vựng chỉ để che một yêu cầu còn thiếu: `NEW_ASSET_REQUIRED`, `MISSING_TEMPLATE`, `EVIDENCE_BLOCKED` là kết quả đúng cho tới khi có năng lực thật.
- Beat `fact` chỉ được trích claim có thật trong `research/sources.json` (SOURCE_VERIFIED trở lên). SHOW_EVOLUTION cần claim đã duyệt biên tập. Dữ liệu bịa để test phải có `synthetic_fixture: true` hoặc ghi rõ SYNTHETIC.
- Tài liệu: `docs/m5/M5_ARCHITECTURE.md`, `VISUAL_PLANNING_PROTOCOL.md`, `ASSET_RESOLUTION.md`, `M5_QA_REPORT.md`.

## Bổ sung M5.5 (2026-10-28): trí tuệ hình ảnh và profile
- Sau `plan-visuals`, đọc mục "Visual repairs" và "Comparison composition" trong `qa/VISUAL_COVERAGE.md`. Sau khi build, chạy `verify-visibility` (Blender) với các shot đã được sửa. Một beat `VISIBILITY_UNRESOLVED` cần người xem lại: không ép kết quả bằng cách sửa ngưỡng hay hình học.
- Mỗi dự án phải khai báo `production_profile`. Không đổi profile để vượt gate. Suffolk là NARRATED_INTERNAL_REVIEW, giữ nguyên trạng thái.
- Khi thêm hành vi planner, thêm ca vào `evaluation/visual_planning/cases.json` và chạy `evaluate-planning`. Dataset này không được dùng trong planner.
- Tài liệu: `docs/m5_5/VISUAL_INTELLIGENCE.md`, `ADAPTIVE_COMPOSITION.md`, `PRODUCTION_PROFILES.md`, `M5_5_QA_REPORT.md`, `M6_READINESS.md`.


## Bổ sung M6 (2026-10-29): phim có lời dẫn, chú thích kỹ thuật, nhiều họ kiến trúc
- **TTS:** lời dẫn M6 dùng Kokoro-82M cục bộ (`integrations/tts/kokoro.py`). Chỉ dùng đúng revision và các giọng đã audit (SHA256 trong adapter). Chạy offline, không mở server. Hạng quyền là `PENDING_REVIEW`: model card Apache-2.0 **không** có nghĩa là đã được phép xuất bản (`docs/licensing/KOKORO_LICENSE_AUDIT.md`). Không dùng OmniVoice cho lời dẫn mới. Không tải model ngoài danh sách. Không dùng trang web bắt chước dự án Kokoro.
- **Thứ tự audio-first:** `narrate → asr-check → align → lock-audio → plan-visuals → validate-plan → build-shots → check-blender → preview → assemble → gates`. `script/narration.json` và `script/visual_beats.json` phải có cùng câu chữ. Đổi một chữ thì chạy lại từ `narrate`.
- **Chú thích** (`docs/m6/ANNOTATION_STYLE_GUIDE.md`):
  - Mỗi đồ họa lực phải trích claim đã đối chiếu và đã được kể. Claim phải áp dụng cho loại cầu đang chiếu và gọi đúng bộ phận.
  - Không bịa nội lực, tải trọng, ứng suất, độ võng.
  - Không tô màu thanh giàn khi không có trường hợp tải và nguồn xác minh.
  - Độ dài mũi tên không mang nghĩa.
  - Chú thích FAILED nghĩa là plan không chạy được: sửa beat, không sửa ngưỡng.
- **Lời và hình phải khớp** (`planner/consistency.py`): một CONTRADICTION là lỗi của `validate-plan`. Sửa câu chữ (người duyệt) hoặc sửa hình, không tắt luật.
- **Nhiều họ kiến trúc:** mỗi họ một scene context (`states.json` schema 3, `scene_context` trên shot). Dự án một họ phải giữ schema 2 giống hệt. Không đặt hai ngữ cảnh chung một khung hay một camera khóa.
- **Quyết định của người** (agent không làm): duyệt giọng kênh, cấp quyền xuất bản Kokoro, duyệt claim, xác nhận phát âm, chuyển profile sang PUBLICATION_CANDIDATE.
- Tài liệu: `docs/m6/M6_ARCHITECTURE.md`, `ANNOTATION_STYLE_GUIDE.md`, `M6_QA_REPORT.md`, `PERFORMANCE.md`.

## Bổ sung M7 (2026-10-30): phim tài liệu dài (8–15 phút)
- **Kịch bản một nguồn:** sửa `projects/<slug>/script/story.py`, rồi chạy nó để sinh lại `narration.json`, `visual_beats.json`, `chapters.json`. Không sửa tay ba file này. Mỗi sửa câu được ghi vào `narration.template.json` → `revision.edits`.
- **Chương:** mode `documentary` bắt buộc có `project.chapters`. Mỗi chương là các beat liên tiếp, đúng thứ tự lời dẫn. Dùng `chapters` (manifest + QA phim dài, không cần Blender) và `chapter --chapter Cn` (render + ghép + QA một chương) trước khi render cả phim.
- **Ảnh ngoài:** chỉ dùng khi có hồ sơ `origin: external` đầy đủ `EXTERNAL_LICENSE_FIELDS`, `credit_keys`, SHA256 và bằng chứng giấy phép kiểm được (không suy từ kết quả tìm kiếm, không fair use, không ảnh có watermark). Ghi công phải xuất hiện trên card hoặc trong mô tả.
- **Mô hình cạnh cầu thật** phải mang NOTE "Illustrative model, not the …". Không bịa số (tải, ứng suất, nội lực, độ võng, hệ số an toàn, xếp hạng độ bền). Không kể chuyện tiến bộ tuyến tính, không nói một kiểu luôn tốt hơn.
- **QA phim dài** (`qa/longform_qa.json`, cổng GL): sửa đoạn tĩnh và sự đơn điệu bằng nội dung (tách câu, NOTE theo câu, phần tử theo từ, push-in có lý do). Không nới ngưỡng. Không thêm người, máy móc hay cảnh phá hủy cho "sinh động".
- **Render dài:** mỗi lúc một Blender. `render_progress.json` cho phép làm tiếp sau khi bị ngắt nếu khóa cache không đổi. Không render 4K trước khi chủ kênh duyệt; 4K chỉ qua `--preset final_4k` theo chương (xem bổ sung M7 finalization). 1080p chỉ dùng cho still chọn lọc hoặc đoạn ngắn, khi đã có ước lượng dung lượng.
- **Quyết định của người** (agent không làm): duyệt claim M7, xác nhận áp dụng quyền giọng cho phim, xác nhận phát âm tên mới, chuyển profile, đăng.
- Tài liệu: `docs/m7/M7_ARCHITECTURE.md`, `M7_QA_REPORT.md`, `PERFORMANCE.md`, `M7_HANDOFF.md`.
- **Bổ sung (bản review nội bộ cuối M7):**
  - Render dùng lại frame tĩnh theo mặc định (`render_strategy.json` trong mỗi thư mục frame). `--no-reuse` buộc render đủ mọi frame. `verify-reuse --shot` so frame dùng lại với bản render trực tiếp. `--mode reuse-report` ước lượng trước số frame cần render.
  - Video 1080p trước khi được duyệt dùng `--preset internal_1080p`; tên file luôn có `INTERNAL_REVIEW`.
  - Không tự đưa giọng mới vào `voices_cleared`.
  - Không ghi đè báo cáo QA của dự án khác khi chạy hồi quy; lưu kết quả vào `qa/regression/` của milestone đang làm.

## Bổ sung M7 finalization (2026-10-30): hồ sơ duyệt, 4K, quy trình phim mới
- **Hồ sơ duyệt của chủ kênh** gắn với đúng revision và tự mất hiệu lực khi revision đổi:
  - claim: `research/editorial_approval.json` (`claims_text_sha256`, `narration_sha256`);
  - giọng: `config/tts_providers.json` → `clearance.voice_approvals`, theo dự án, kèm SHA256 của giọng. `voices_cleared` vẫn chỉ gồm các giọng đã được cấp chung;
  - phát âm: `ACCEPTED_BY_OWNER` gắn với `audio_revision` (hash lời dẫn). Đây là chấp nhận audio hiện tại, không phải xác nhận đã nghe từng mục;
  - tổng hợp: `review/OWNER_APPROVALS.json` (phạm vi, đối tượng, revision, quyết định, ngày, bằng chứng, điều kiện, điều kiện mất hiệu lực).
  - Agent chỉ ghi lại đúng lời chủ kênh. Không bịa tên, chữ ký hay một buổi nghe.
- **Cổng cuối** chỉ đòi duyệt các claim mà phim dùng (lời dẫn, beat hình, chú thích, shot). Claim không dùng vẫn ở trong sổ nhưng không được duyệt hộ.
- **4K:** `chapter --preset final_4k --release-frames` cho từng chương, rồi `final-assemble`, rồi `gates --preset final_4k`.
  - PNG của một chương chỉ được xóa sau khi bản trung gian đã kiểm chứng và đăng ký ở `qa/chapter_intermediates_final_4k.json`.
  - Lệnh tự dừng khi đĩa trống dưới 8 GB.
  - Không phóng to bản 1080p, không dùng frame 1080p làm frame 4K.
  - Không ghi đè bản review 1080p.
- **Dự án đang làm:** `projects/` chỉ chứa phim đang sản xuất. Pilot cũ là fixture ở `tests/fixtures/legacy_projects/`; states mái cũ ở `asset_library/legacy_states/` (giữ nguyên asset id). Lưu trữ bằng `tools/archive_projects.py` (ra ngoài repo, có checksum). Không xóa code dùng chung chỉ vì nó ra đời cho một pilot cũ.
- **Phim mới:** `prompts/NEW_DOCUMENTARY_AUTOPILOT.md` + `docs/production/NEW_DOCUMENTARY_PLAYBOOK.md` + `tools/episode.py` (`new`, `status`, `next`). Agent dừng ở OWNER_APPROVAL. Scaffold chạy được không có nghĩa là quy trình tự động đã được kiểm chứng trọn vẹn.
- Tài liệu: `docs/m7/M7_FINALIZATION_REPORT.md`, `docs/m7/PERFORMANCE_4K.md`, `docs/production/CLEANUP_REPORT.md`.

## Bổ sung M8 (2026-10-31): đủ sáu họ cầu, ngữ cảnh cảnh theo concept
- **Họ cầu nhịp lớn:** `bridge.cantilever`, `bridge.suspension`, `bridge.cable_stayed` (`engine/arch/families/bridge.py`). Asset nằm ở `asset_library/architecture/bridges/` và đặt trên site 72 m (`sites/site_river_crossing_72.json`).
  - Cầu treo: khối neo và đầu cáp nằm trên bờ, ngoài khoảng hở. Kiểm tra kích thước không tính chúng.
  - Cầu dây văng: dây văng dốc tối thiểu khoảng 22° (FHWA). Validator từ chối dây dốc hơn ngưỡng đó.
  - Mỗi tham số hình học đều có kiểm tra chéo (`assets.compatibility_errors`). Sửa bằng tham số, không nới kiểm tra.
- **Ngữ cảnh cảnh theo concept:** một concept kiến trúc có thể khai báo `scene_context` và `site` (`config/visual_vocabulary.json`).
  - Planner tạo một ngữ cảnh cho mỗi site, mỗi ngữ cảnh có trạng thái site trống riêng (`site`, `site_<context>`).
  - Shot ứng viên của bộ bố cục mang `scene_context` (`planner/composition.in_context`).
  - Ngưỡng đọc được 2,5 px ở 640×360 vẫn giữ. Mô hình 72 m không đọc được khi đặt cạnh nhau thì dùng sơ đồ hoặc mỗi shot một mô hình.
- **Revision lời dẫn:** duyệt claim và chấp nhận phát âm gắn với một revision.
  - `research/build_sources.py` không áp duyệt của revision khác. Ví dụ: duyệt m7-r1 không áp sang m8-r1.
  - Duyệt giọng theo dự án giữ nguyên, trừ khi điều kiện mất hiệu lực của chính nó xảy ra.
  - Khi làm lại phim: cất bản đã duyệt vào `output/baseline_*`, gắn tag git, và đưa profile về `NARRATED_INTERNAL_REVIEW`.
- **Cầu di động** (cầu cất, cầu quay) là loại theo chức năng, chưa có bộ sinh (`bascule_bridge` có `supported: false`). Planner báo NEW_ASSET_REQUIRED, không thay bằng thứ khác.
- Tài liệu: `docs/m8/M8_REPORT.md`.
- **Bổ sung M8.1 (2026-11-03): quyết định thời lượng của chủ kênh.**
  - Khoảng 8–15 phút của QA phim dài chỉ được đổi cho một dự án khi chủ kênh đã quyết định. Bản ghi ở `project.json` → `runtime_decision` phải có đủ `acceptable_minutes`, `decided_by`, `decided_on` và `basis` (trích lời chủ kênh). Thiếu trường nào thì QA dùng mặc định.
  - Agent không tự nới thời lượng.
- **Snapshot nguồn:** để ở `projects/<slug>/research/snapshots/` (git bỏ qua), không để trong scratchpad vì hệ thống có thể xóa.

## Bổ sung 2026-11-05: lời kêu gọi cuối phim, duyệt kịch bản trước
- **Mỗi phim mới kết bằng lời kêu gọi** gợi ý chủ đề trong bình luận, like và subscribe (`config/production_defaults.json` → `closing_call_to_action`): một beat `framing` trong chương cuối, sau kết luận, tối đa 60 từ, không claim, không hứa điều Studio không kiểm được, không logo hay nhãn hiệu nền tảng. Trên hình dùng icon tự vẽ đơn giản (bóng thoại, ngón tay cái, nút subscribe, chuông), mỗi icon hiện khi lời dẫn nhắc tới (chủ kênh yêu cầu ngày 2026-11-06, thay cho chữ trơn). `episode.py status` chặn bước SCRIPT khi thiếu. Chỉ áp dụng cho dự án có quy định này trong `episode.json`; phim cầu không bị kiểm lại.
- **Chủ kênh có thể đọc kịch bản trước khi có video:** `tools/script_review.py` (xem playbook). Không dựng asset mới trước khi kịch bản được duyệt.
- **Nguồn chặn tải tự động:** không lấy bản lưu trữ của nguồn đó để lách, ghi vào `research/source_snapshots.json` → `not_used` và tìm nguồn khác.
- **Kiểm tra "lời và hình có khẳng định vượt quá bằng chứng không?"** là bắt buộc trước khi giao kịch bản và trước khi giao bản review (danh sách câu hỏi ở playbook, mục 4–6). Khớp nguyên văn với nguồn chưa đủ.
- **Các nguồn lệch nhau về một con số:** nói cách diễn đạt đúng với mọi nguồn đã đọc ("more than 42 meters") và ghi rõ trên hình khi cần. Đừng chọn một con số rồi im lặng.

## Bổ sung 2026-11-06: shot SEQUENCE, âm thanh tổng hợp, đoạn thử
- **SEQUENCE** (`engine/motion.plan_sequence`, chiến lược planner cùng tên): một mô hình, nhiều bước theo lời dẫn (làm mờ, hiện ra, phát sáng; camera trượt và zoom giữa các khung của một preset). Cách viết: playbook, mục "Shot SEQUENCE".
  - Asset phải khai báo `SEQUENCE` trong `animation_support`. Không có thì planner trả MISSING_TEMPLATE, không thay bằng hình giữ.
  - Camera chỉ quay một cung ngắn giữa hai view (từ g-r5), không quay khi bộ phận đang đổi. Không dùng hoạt ảnh để tái hiện một vụ sập lịch sử: nguyên nhân còn tranh luận thì vẽ từng giả thuyết riêng, có nhãn.
- **Âm thanh:** âm tổng hợp trong dự án (`pipeline/sound.py`, `config/sound_design.json`), mỗi âm gắn với một sự kiện nhìn thấy được, nhỏ hơn lời dẫn.
  - Không nhạc nền, không tải âm thanh ngoài khi chưa kiểm giấy phép.
  - **Từ 2026-11-12 (chủ kênh yêu cầu):** dự án được dùng âm thu sẵn, ghi ở `audio/sound_plan.json` (schema `sound_plan/1`, xem docstring `pipeline/sound.py`).
    - Mỗi file ghi trang nguồn, tác giả, giấy phép, ngày kiểm giấy phép và sha256. Thiếu file hay file bị thay thì không trộn.
    - Âm thêm neo vào một bước của storyboard (shot, số thứ tự bước, `do`), nên không đổi shot và không làm mất cache render.
    - Nền âm (ambience) chỉ được dùng ngắn, dưới đúng một shot mà chính âm đó là chủ đề (nước làm phao nhấp nhô), thấp hơn lời dẫn nhiều (`bed_under_narration_db`). Không trải nền âm dưới cả phim.
    - Agent chọn file bằng số đo (độ dài, điểm bắt đầu, nền ồn, cân bằng trầm/bổng), không nghe được. Chủ kênh nghe rồi quyết.
    - `final-assemble` trộn âm hiệu ứng khi chủ kênh đã duyệt và `audio/sound_plan.json` ghi `"final": true` (từ 2026-11-12): cùng cách trộn như bản trích, trước khi chuẩn hóa âm lượng.
      - File WAV `narration_master_clean` vẫn chỉ có lời dẫn; `audio_master` có SFX.
      - Trước khi ghép bản cuối, so bản trộn cả phim với bản trộn của đoạn trích đã duyệt: hai bản phải giống nhau từng mẫu.
  - Agent không nghe được, nên luôn giao kèm một bản không âm thanh để so. Whisper trên lời dẫn có âm và không âm phải cho WER tương đương (`tools/excerpt.py`).
- **Đoạn thử** (`tools/excerpt.py`): các shot của phim, render đúng như trong phim, ghép với đúng đoạn lời dẫn của chúng.
  - Tên file luôn có `INTERNAL_REVIEW`. Chỗ nối giữa hai shot không liền nhau trong phim được ghi là "excerpt join".
  - Chủ kênh duyệt chất lượng hình trên đoạn thử trước khi agent áp cách làm đó cho cả phim.


## Bổ sung 2026-11-06 (g-r5): công trình thật có hình riêng
- **Không thay tên trên cùng một mô hình chung để giới thiệu hai công trình thật.** Dùng ảnh thật và tài liệu của chính công trình đó (mặt bằng, mặt cắt lịch sử). Chỉ dựng 3D phần phục vụ câu chuyện, dựa trên tài liệu tham chiếu. Mô hình chung chỉ dùng cho phần giải thích nguyên lý.
- **Ảnh và bản vẽ ngoài:**
  - Tìm trên Wikimedia Commons, kiểm giấy phép qua API.
  - Ưu tiên public domain, CC0, CC BY. Không dùng CC BY-SA khi chưa có quyết định về ShareAlike.
  - Bỏ ảnh có tác giả hoặc ngày không chắc chắn.
  - Mỗi ảnh có hồ sơ đầy đủ trong `assets/manifest.json` và dòng ghi công trên hình.
  - `status: approved` ở đó chỉ nghĩa là agent đã kiểm giấy phép theo hồ sơ nguồn. Việc chủ kênh duyệt ảnh và ghi công vẫn là một mục riêng trong checklist duyệt cuối, agent không đánh dấu.
- **Dấu vẽ lên ảnh hay bản vẽ** (vùng, mũi tên, tuyến) chỉ đặt ở nơi nguồn nói tới, và ghi "schematic". Khi nguồn chỉ tả một tuyến ("dọc lòng chính, giằng trụ giao cánh"), vẽ đúng tuyến đó, không tự thêm hình dạng.
- **Duyệt theo chương:** khi cách làm hình thay đổi, render và giao từng chương đã làm lại (`chapter --chapter Cn --preset internal_720p`). Chỉ render lại cả phim khi chủ kênh đã duyệt các chương.

## Bổ sung 2026-11-07 (phim Gothic, g-r9 và bản final 4K): kinh nghiệm chung
- **Chi tiết đầy đủ ở `docs/production/NEW_DOCUMENTARY_PLAYBOOK.md` mục 27–28.** Điểm cần nhớ cho mọi phim sau:
  - Mỗi vòng review có `review/REVIEW_<vòng>.md` (góp ý → đã làm → kiểm tra → cần quyết). Sửa cục bộ, giữ hướng; đổi mã shot thì sinh lại manifest chương và báo cáo.
  - Ảnh phải khớp giai đoạn lời đang kể; "today" chưa đủ cho công trình đã được dựng lại. Nhãn chỉ bộ phận phải chấm đúng bộ phận (soi khung 1:1).
  - Xem video thật bằng khung trích từ MP4 ghép. Một kiểm tra QA báo sai đáng ngờ thì tìm nguyên nhân trước (QA cũng có lỗi). Không nới ngưỡng.
  - Chủ kênh quyết từng mục (claim, giọng và phát âm, ảnh và ghi công và công bố, lời kêu gọi). Chỉ ghi các mục được chọn. Ngoại lệ của một ngưỡng là quyết định của chủ kênh, ghi ở `project.json` (`variety_exception`); không tự miễn. Ngoại lệ ghi đúng chuỗi được chấp nhận (`runs`: shot đầu, shot cuối, độ dài, loại hình); validator chỉ miễn đúng các chuỗi đó, không nâng ngưỡng cho cả phim.
  - Không có file tên FINAL trước khi duyệt; `final-assemble` ở preset nội bộ đặt tên theo `review_label`.
  - Render: một Blender, không sửa engine hay chạy test gọi Blender khi đang render; benchmark 4K trước (3D khoảng 2,2 giây mỗi frame).
  - Sau bản final: dọn file render thử và review cũ theo mục 28, giữ bản final, bản review đã duyệt và mọi hồ sơ trong git.
