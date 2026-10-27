# M3.5: workflow lời dẫn độc lập provider và quy trình xuất bản

## 1. Hai mục đích, hai loại audio
| Mục đích | Provider | Hạng quyền | Dùng cho |
|---|---|---|---|
| `internal_preview` | OmniVoice (cục bộ) | `INTERNAL_PREVIEW_ONLY` | Đo timing, nhịp, lập lịch shot, preview nội bộ (`*_INTERNAL.mp4`) |
| `publication` | Chưa chọn: TTS thương mại có giấy phép, model cục bộ có license phù hợp, hoặc giọng người thật | phải là `PUBLICATION_CLEARED` | Video phát hành |

Hạng quyền của từng provider được khai báo trong `config/tts_providers.json`. Chỉ con người được nâng một provider lên `PUBLICATION_CLEARED`, và phải ghi `clearance.cleared_by`, `cleared_on`, `evidence`. Validator báo lỗi nếu thiếu.

## 2. Interface (`integrations/tts/providers.py`)
`NarrationAdapter`: `prepare(voice_cfg, project_dir, cached_segment, log)` → voice; `voice_identity(voice)`; `params(voice_cfg)`; `source_identity(segment_id, …)`; `synthesize(text, voice, out, params, segment_id, project_dir)` → kết quả có thời lượng đo bằng ffprobe.

Đã có hai adapter:
- `OmniVoiceAdapter`: Gradio cục bộ.
- `RecordedNarrationAdapter` (`human`): một WAV cho mỗi câu, ở `audio/recorded/B1.s0.wav`.

Scheduler, assembler và các gate chỉ đọc `audio/narration_manifest.json`, nên đổi provider **không** phải viết lại scheduler.

Thêm một provider:
1. Viết adapter.
2. Đăng ký trong `ADAPTERS`.
3. Thêm vào `config/tts_providers.json` với hạng quyền `PENDING_REVIEW`.
4. Viết test với server giả lập, giống `tests/fake_omnivoice.py`.
5. Người duyệt license ghi clearance.
6. Thêm provider vào `workflow.publication`.

## 3. Lệnh
```bash
python3 tools/cli.py narrate --project P                         # internal_preview (mặc định)
python3 tools/cli.py narrate --project P --purpose publication   # từ chối provider chưa PUBLICATION_CLEARED
python3 tools/cli.py asr-check --project P                       # độ rõ (alias phát âm chỉ dùng để tính WER)
python3 tools/cli.py align --project P                           # timestamp theo từ của Whisper → ranh giới cue phụ đề
python3 tools/cli.py schedule --project P
python3 tools/cli.py cache-report --project P                    # shot nào cần render lại và vì sao
python3 tools/cli.py preview --project P                         # 640×360
python3 tools/cli.py still --project P --preset review           # khung đại diện 960×540
python3 tools/cli.py still --project P --preset production_test  # ảnh tĩnh 1920×1080 (preset này không render chuỗi frame)
python3 tools/cli.py assemble --project P                        # *_INTERNAL.mp4 nếu audio chưa được cấp quyền; qa/SUBTITLE_QA.md
python3 tools/cli.py gates --project P                           # G0–G6 + các trạng thái
python3 tools/pronunciation_test.py --project P --entry PRON_001 # clip bằng chứng phát âm
```

## 4. Các trạng thái (`pipeline/gates.py`)
- `TECHNICALLY_VALIDATED`: G0, G3, G4, G5 PASS và mọi câu đều đạt ASR.
- `EDITORIAL_REVIEW_PENDING`: còn claim chưa được người duyệt (có hồ sơ duyệt khớp narration revision hiện tại), `factual_review` chưa `verified`, hoặc override phát âm chưa `CONFIRMED`.
- `TTS_RIGHTS_PENDING`: có câu nào không phải `PUBLICATION_CLEARED` (theo cả bản ghi lẫn registry hiện tại), hoặc license giọng chưa `APPROVED` (kèm `approved_by`/`approved_on`).
- `PUBLICATION_READY`: mọi gate PASS và không còn gì chờ. Trạng thái này loại trừ các trạng thái khác. PASS về kỹ thuật **không bao giờ** đồng nghĩa với được phép xuất bản.

## 5. Từ preview nội bộ đến bản phát hành (việc của con người)
1. Duyệt `projects/<p>/review/EDITORIAL_APPROVAL_PACKAGE.md`, rồi ghi `editorial_approval` cho từng claim, đặt `factual_review: verified`.
2. Nghe các clip phát âm, rồi đặt `CONFIRMED` kèm tên người nghe.
3. Chọn provider xuất bản theo `docs/licensing/TTS_LICENSE_AUDIT.md` §6. Mở tài khoản hoặc ký hợp đồng (agent không làm việc này).
4. Ghi clearance cho provider và `voice.license` (`APPROVED`, `approved_by`, `approved_on`), đổi `voice.provider`. Khai báo dạng phát âm cho provider mới.
5. Chạy `narrate --purpose publication`, rồi `asr-check`, `align`, `schedule`, `preview`, `assemble`, `gates`. Thời lượng sẽ khác với bản OmniVoice, nên shot sẽ được lên lịch lại theo audio mới.
6. Nghe lại toàn bộ, duyệt asset, chạy `final-gate`.
