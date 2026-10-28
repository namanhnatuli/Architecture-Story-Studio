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
