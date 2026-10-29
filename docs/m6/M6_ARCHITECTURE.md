# M6: kiến trúc phim tài liệu có lời dẫn

M6 nối các phần đã có (M3 lời dẫn, M4 asset, M5/M5.5 lập kế hoạch hình) thành một quy trình **audio-first** cho video có lời dẫn tiếng Anh, chú thích kỹ thuật bám theo bộ phận, và nhiều họ kiến trúc trong một dự án.

## 1. Trình tự (khóa theo audio)
```
research (sources.json, claim có bằng chứng)
 → script (narration.json + visual_beats.json, cùng câu chữ)
 → narrate (Kokoro, cục bộ) → asr-check (Whisper) → align (word timestamps)
 → lock-audio      script/timing.json: thời lượng beat + khoảng câu đã đo, khóa nếu ASR đạt
 → plan-visuals    AUDIO_LOCKED: cửa sổ beat = lead + giọng đo được + tail
 → validate-plan   tham chiếu, timing, chú thích, nhất quán lời/hình, engine
 → build-shots     storyboard + audio_lock.finalize (shot, mốc tuyệt đối, khóa project)
 → check-blender   QA engine + QA chú thích (ray-cast điểm neo, chữ thật)
 → preview         render review 960×540 → MP4 không tiếng + media QA
 → assemble        track lời dẫn (−16 LUFS), mux, SRT + track mov_text
 → gates / research-map
```
Lời dẫn không bao giờ bị kéo giãn hay cắt cho vừa hình. Nếu hình không vừa thời lượng đo được thì beat bị TIMING_CONFLICT và chọn chiến lược nhẹ hơn (planner/timing.py).

## 2. Module mới
| File | Vai trò |
|---|---|
| `integrations/tts/kokoro.py`, `tools/kokoro_tts.py` | Adapter Kokoro-82M: kiểm SHA256 model/giọng đã audit, worker con nói JSON qua stdin/stdout (không mở server), HF offline, seed theo từng câu để tái lập |
| `pipeline/audio_lock.py` | `lock_beats` (sau ASR) và `finalize` (sau build-shots, idempotent); `check_consistency` kiểm lại manifest một cách độc lập |
| `planner/annotations.py` | Hợp đồng chú thích, kiểm bằng chứng, gắn vào shot theo câu, điểm neo trên silhouette **nhìn thấy được** (raster offline có độ sâu), điểm neo nằm trong mép 2 bước raster |
| `engine/annotation_layout.py` | Bố cục thuần Python (dùng chung planner và QA Blender): mũi tên cùng độ dài, tìm chỗ đặt nhãn tất định, tránh vùng phụ đề, kiểm luật |
| `engine/annotations.py` | Dựng chú thích trong Blender: mặt phẳng trước camera, emission phẳng, fade bằng TRANSPARENCY |
| `engine/qa_annotations.py` | QA Blender: đủ object, điểm neo chiếu đúng và ray-cast trúng chính bộ phận đích, bề rộng chữ thật, thời điểm fade, chú thích tiêu đề không vào vùng phụ đề |
| `planner/consistency.py` | Kiểm mâu thuẫn lời/hình theo luật (side by side / one at a time / "this component" / màu / trái-phải / biến đổi / mũi tên) |
| `planner/research_map.py` | `research-map`: câu → claim → nguồn → asset → bộ phận → chú thích → thời điểm → QA |
| `tools/voice_audition.py` | Thử 4 giọng Anh–Anh đã audit trên cùng đoạn văn; xếp hạng theo số đo; không tự duyệt giọng |
| `tools/annotation_preview.py` | Xem trước bố cục offline (PPM → PNG qua ffmpeg), để debug mà không cần render |

## 3. Ngữ cảnh cảnh quay (nhiều họ kiến trúc)
- `planner.Model` giữ một **scene context** cho mỗi họ: `bridge` dùng nền địa hình sông, `roof` dùng nền nhà chung. Mỗi trạng thái thuộc ngữ cảnh của họ của nó.
- Dự án một họ vẫn ra `states.json` schema 2, **giống hệt từng byte** (đã kiểm với bridge-story-m5, roof-plan-m5, bridge-load-explained).
- Dự án nhiều họ ra schema 3: `contexts: {bridge: {base, shared_components}, roof: {...}}`, mỗi variant có `context`, mỗi shot có `scene_context`.
- Engine chỉ thấy **view** của một ngữ cảnh (`engine/spec.context_view` / `shot_states`). `templates.layout_slots/plan_shot/placeholder_slots`, `shot_builder.build_shot`, `visibility.build_scene`, QA Blender và khóa render cache đều đi qua view này.
- Luật: chiến lược đặt nhiều mô hình chung một khung hoặc một camera khóa (SIDE_BY_SIDE, FOCUSED_PAIR, SEQUENTIAL_COMPARISON, DETAIL_THEN_OVERVIEW, REPLACE…) bị từ chối nếu các trạng thái thuộc khác ngữ cảnh. Khi đó dùng SEQUENTIAL_STATES với cắt cứng. Preset camera đi theo ngữ cảnh của từng trạng thái. Site của sông chỉ ràng buộc việc tìm asset cầu.
- Fixture hồi quy: `tests/fixtures/m6_cross_family` (cầu → mái → mái → so sánh → cầu). Plan validate PASS, QA Blender 69/69.

## 4. Bổ sung cho hợp đồng beat (`schemas/narrative_beats.schema.json`)
- `annotations[]`: `id`, `type`, `target` (khái niệm + `group` + `pick` LEFTMOST/RIGHTMOST/CENTERMOST), `point`/`points`, `text`, `sentence`, `until`, `claim_id`, `state`, `count`, `direction`, `style`, `force`, `path`/`along`, `leaders`, `entries`.
- `highlight_at_sentence`: glow bắt đầu cùng câu.
- `visual_repair_preference`: thứ tự biện pháp sửa tầm nhìn (ví dụ GHOST trước ALT_CAMERA để giữ góc nhìn).
- Intent mới `EXPLAIN_LOAD_PATH` (HOLD_HIGHLIGHT, HOLD). Bắt buộc phải có chú thích.

## 5. Cắt theo câu và phụ đề
- Với AUDIO_LOCKED, nếu một beat có số câu ≥ số shot, (n−1) điểm cắt cuối rơi 0,2 s trước các câu cuối. Ví dụ B7: dầm/vòm/giàn hiện đúng khi câu của nó được đọc. Nếu cắt như vậy làm một shot ngắn hơn mức tối thiểu thì quay về chia theo trọng số.
- Dự án có lời dẫn: chú thích tiêu đề của mô hình đặt **trên cùng** (`label_position: TOP`); dải nhãn của so sánh xếp chồng ≥ 0,24; chú thích không vào vùng phụ đề 0,17 dưới cùng. Phụ đề là SRT riêng, kèm track mov_text trong MP4, không bao giờ in vào hình.

## 6. Quyền và trạng thái
- Kokoro: `PENDING_REVIEW`. Agent không bao giờ tự nâng hạng quyền. OmniVoice giữ nguyên, không dùng cho M6.
- Profile pilot: `NARRATED_INTERNAL_REVIEW`; tên trong spec M6 `INTERNAL_NARRATED_PREVIEW` là alias.
- Trạng thái kỳ vọng: `TECHNICALLY_VALIDATED` + `EDITORIAL_REVIEW_PENDING` + `TTS_RIGHTS_PENDING`. Không bao giờ `PUBLICATION_READY` nếu chưa có người duyệt.
