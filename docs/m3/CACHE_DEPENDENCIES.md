# Phụ thuộc cache (M3.5)

Có hai cache độc lập: **audio** (từng câu lời dẫn) và **render** (khung hình PNG của từng shot). Mỗi đầu vào chỉ làm mất hiệu lực đúng cache phụ thuộc vào nó.

## Cache audio: `audio/narration_manifest.json` (khóa v2)
Khóa = sha256 của `{provider, adapter, model, model_revision, spoken_text, voice_id, voice identity (hash của reference clip), params, rights_class}`. Riêng provider `human` thì khóa có thêm hash của file thu âm.

| Thay đổi | Ảnh hưởng |
|---|---|
| Chữ của một câu | Chỉ câu đó được sinh lại (thường kéo theo thời lượng beat → `schedule` → render lại shot chứa beat đó, vì số frame đổi) |
| Override phát âm (`script/pronunciation.json`) | Chỉ những câu mà dạng đọc (`spoken_text`) bị đổi |
| Giọng, tham số, revision model, provider | Mọi câu của giọng đó |
| **Hạng quyền** (`config/tts_providers.json`) | Mọi câu. Audio của hạng này không bao giờ được dùng làm audio của hạng khác, kể cả khi chữ và thời lượng trùng nhau |
| Ghi chú license (`voice.license.*`), `pace_note` | Không ảnh hưởng (không có trong khóa, không có trong `narration_hash`) |

Khóa v1 (M3) không có model, voice id và hạng quyền. Bản ghi v1 chỉ được *nhận lại* (đổi khóa, giữ nguyên file) khi chạy `internal_preview` với OmniVoice và chữ đọc trùng chữ viết. Ở M3.5, 9/14 câu được giữ theo cách này, đã kiểm chứng audio beat trùng từng byte.

## Cache render: `renders/<preset>/<shot>/render_manifest.json` (khóa v3 từ M4)
`tools/render_cache.py` băm riêng 7 nhóm và lưu từng hash. Nhờ vậy `cache-report` nói được **vì sao** một shot cần render lại.

| Nhóm | Gồm | Không gồm |
|---|---|---|
| `shot_visual` | Mọi trường của shot **trừ** các trường không phải hình ảnh: animation/graphic, state, camera, transition, `duration_seconds`, nhãn | `narration`, `visual_purpose`, `claim_ids`, `beat_ids`, `start_seconds`, `cut_from_previous`, `notes`, `editorial` |
| `states_geometry` | base + các variant mà shot **dựng**: mọi variant (camera khóa fit theo mọi variant), hoặc chỉ các variant trong `build_variants` của shot (M5: mỗi nhóm liên tục camera một tập) | `name`, `claim_ids`, `note(s)`, `description`, `transitions`, `schema_version` |
| `project_render` | Các trường project mà engine đọc (`fps`) | `title`, `slug`, `mode`, `language`, `duration_seconds`, `render_preset`, `factual_review`, `audio_timing_locked` |
| `style` | `config/visual_style.json` | — |
| `preset` | Mục của preset (kích thước, fps, engine, định dạng) | codec/CRF khi encode (chỉ ảnh hưởng MP4) |
| `engine` | `engine/**/*.py` (đệ quy từ M4: `engine/arch/`), hash theo từng file | `qa_checks.py` (chỉ dùng cho QA), `transform.py` (đã bỏ) |
| `assets` (M4, khóa v3) | Nội dung các spec asset của base và của các variant shot dựng (M5: giới hạn theo `build_variants`), cùng `asset_library/materials/stylized_materials.json` nếu có tham chiếu | Spec asset không được dùng; catalog; ảnh preview |

**M5 (`build_variants`, `camera_focus`, `camera_safe_band`):** ba trường này là trường hình ảnh (thuộc `shot_visual`). `build_variants` còn giới hạn `states_geometry` và `assets` của shot. Vì vậy sửa spec cầu đá chỉ làm cũ các shot có dựng cầu đá; các shot khu đất/cầu gỗ vẫn dùng cache (`tests/test_m5_planner.py` `CacheDependencyTest`). Storyboard do planner biên dịch ghi `editorial` (không phải phụ thuộc render) và `plan_sha256` ở mức tài liệu.

**M5.5:**
- Các quyết định hình ảnh do planner viết vào shot là trường hình ảnh: `highlight.ghost`, `camera_focus` của REFRAME, preset khác, `layout`/`gap_ratio` của bố cục, `animation.label`. Mỗi quyết định chỉ làm cũ shot của nó. Đã đo: đổi độ trong suốt ghost thì chỉ SC_003 render lại; đổi `gap_ratio` thì chỉ SC_015.
- Các phần sau không phải phụ thuộc render:
  - `editorial` (gồm `visibility_targets`, `visibility_estimate`, `repairs`, `composition`);
  - `production_profile`, `publication_metadata`;
  - `engine/qa_visibility.py` (chỉ dùng cho QA);
  - ngưỡng trong `config/visual_planning.json`, khi chúng không làm thay đổi quyết định nào.
- Báo cáo QA (visibility, coverage, media) vẫn có thể cần chạy lại dù frame render còn dùng được.

Trường lạ (không có trong danh sách loại trừ) được coi là **trường hình ảnh**, tức là an toàn: thà render lại còn hơn dùng nhầm khung cũ.

Không phải phụ thuộc render: audio và hạng quyền, phát âm, phụ đề, sổ nguồn/trạng thái duyệt, vị trí shot trên timeline. Các thứ này chỉ ảnh hưởng tới `assemble` (track audio, SRT) và các gate.

## Lệnh
```bash
python3 tools/cli.py cache-report --project suffolk-roofs [--preset review]   # CACHED/STALE + lý do
```
Manifest render v1 (M3) được render lại **một lần** (lý do ghi: "render manifest key v1 (pre-M3.5): one-time re-render"). Ở M3.5, lần render lại một lần này trùng với các thay đổi hình ảnh thật (engine, độ dài shot), nên không tốn thêm.

## Test
`tests/test_m5_planner.py` `CacheDependencyTest`: sửa chữ claim, `visual_goal` không đổi khóa nào; đổi mục tiêu ngữ nghĩa của B5 chỉ đổi SC_008; đổi hình học cầu đá chỉ đổi các shot dựng cầu đá.

`tests/test_m35.py`:
- `AudioCacheSeparationTest`: mỗi chiều của khóa tách cache; audio preview không bao giờ được dùng lại cho publication; các take M3 được nhận lại.
- `RenderCacheTest`: sửa chữ, tiêu đề, claim, `start_seconds` không làm mất cache; sửa độ dài, animation, hình học, fps, engine thì có, và lý do được nêu đúng tên.
