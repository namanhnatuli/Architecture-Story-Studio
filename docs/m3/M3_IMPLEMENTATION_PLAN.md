# M3 — Kế hoạch triển khai: dựng hình kiến trúc theo dẫn chuyện

Trạng thái: **ĐỀ XUẤT** (2026-10-26, cuối M2.5). Chưa có gì trong tài liệu này được triển khai.
Pilot: *"Why Do Roof Pitches Vary?"*, 60–90 s, tiếng Anh. Xem [PILOT_RESEARCH_BRIEF.md](PILOT_RESEARCH_BRIEF.md) và [PILOT_STORYBOARD_DRAFT.md](PILOT_STORYBOARD_DRAFT.md).

## Nguyên tắc
- **Một pipeline tuyến tính có các gate, không dùng kiến trúc multi-agent.** Code hiện có đã dựa trên dữ liệu (JSON → planner → Blender → FFmpeg), nên M3 chỉ thêm *dữ liệu* (nguồn, lời dẫn, timing) và *các bước xử lý tiếp theo* (audio, ghép video, phụ đề). Prompt cho research/storyboard/QA (`prompts/01`, `02`, `04`) vẫn là công cụ bán thủ công, có người duyệt ở G1 và G4.
- **Gate xuất bản cuối giữ nguyên.** `final-gate` vẫn yêu cầu mọi claim ở trạng thái `verified`, `audio_timing_locked: true` và asset đã được duyệt. M3 thêm kiểm tra, không bỏ bớt kiểm tra nào.
- **Giữ phạm vi pilot nhỏ:** không thêm loại công trình mới, không thêm template animation, và không dựng mô hình mái tranh (thatch) trong M3.

## Tái sử dụng và phần mới

| Khu vực | Tái sử dụng nguyên trạng | Mở rộng | Module mới |
|---|---|---|---|
| A. Nghiên cứu & bằng chứng | Định dạng claim trong `research/sources.json`, `validator` (claim → source), final gate | Thêm trường cho source (`publisher`, `kind`, `accessed`, `locator`, `quote`) và claim (`scope`, `quote_refs`, `visualization_scope`) | `schemas/sources.schema.json`; quy tắc validator: claim *verified* phải có ≥ 1 source kèm `locator` + `quote` |
| B. Lời dẫn tiếng Anh | `script/narration_draft.md` (định dạng con người đọc được) | — | `script/narration.json`: danh sách beat `{id, text, claim_ids, kind: fact/framing/question}`; validator: beat loại `fact` phải có claim |
| C. Beat ↔ shot | `storyboard.json` (`claim_ids`, `visual_purpose`) | Thêm `beat_ids` cho mỗi shot; mỗi beat gắn với ≥ 1 shot, đúng thứ tự | Kiểm tra độ bao phủ trong validator |
| D. Chọn state kiến trúc | `states.json` v2, builder `gable_roof`, ownership, QA | Variant mới chỉ là tham số (độ dốc + màu), ví dụ `plain_tile_50`, `slate_30` | Không có (palette thêm `roof_slate`) |
| E. Chọn template | `HOLD`, `EXPLODED_VIEW`, `REPLACE_PARTS`, `SIDE_BY_SIDE` (+ intro) | Bảng quy tắc "ý định beat → template" trong tài liệu (người/AI chọn tường minh trong storyboard) | Không có engine mới |
| F. TTS & căn timing | `templates.frame_count`, marker, `key_stills` | `project.audio_timing_locked` chỉ được đặt bởi công cụ timing | `tools/timing.py` (stdlib): đo thời lượng audio từng beat bằng ffprobe → `script/timing.json` → đề xuất thời lượng shot (làm tròn lên số nguyên frame + pad) → kiểm tra storyboard; khóa G4 |
| G. Lên lịch shot & render | Cache theo shot, `shot`, `preview --preset`, `caffeinate` | Ước lượng chi phí từ log (giây/frame), chỉ render lại shot thay đổi | Lệnh `render-plan` (đọc log + hash cache) |
| H. Ghép video bằng FFmpeg | `encode_full` (concat), media QA, kiểm tra SSIM tại điểm cắt | Thêm track audio, phụ đề | `tools/assemble.py`: nối audio beat + khoảng lặng, `loudnorm` (đích -14 LUFS, true peak -1 dBTP), mux với video, sidecar SRT/VTT từ narration + timing |
| I. QA sự thật & hình ảnh | `check-blender` (58 kiểm tra), media QA, MCP `look`, `prompts/04` | Media QA: độ lệch audio/video ≤ 1 frame, loudness, clipping, phụ đề khớp timing | `qa/factual_review.md` theo mẫu: bảng claim ↔ câu narration ↔ trích dẫn nguồn; người ký G1 |

## Luồng dữ liệu M3

```text
research/sources.json ──(G1: người duyệt)──► script/narration.json ──► TTS (đã được phép) ──► audio/beat_*.wav
        │                                         │                                            │
        └─► claim_ids ◄───────────── beat_ids ────┘                      tools/timing.py ◄─────┘
                                       │                                      │ script/timing.json (G4)
storyboard.json (shot.beat_ids, animation) ◄──── thời lượng shot đề xuất ─────┘
        │
        ├─► validate (G0) ─► check-blender ─► still/preview (G2/G3) ─► MCP look (tùy chọn)
        └─► tools/assemble.py: video + audio + SRT ─► media QA (+ audio/subtitle) ─► final-gate (G5)
```

## Quyết định cần người dùng trước khi làm
1. **Nhà cung cấp TTS.** Lệnh `say` có sẵn trên macOS thì miễn phí và chạy offline, nhưng điều khoản cho phép dùng giọng đọc trong video YouTube công khai phải được kiểm tra trước khi xuất bản. Dịch vụ TTS trả phí / bên ngoài cần được phép rõ ràng (AGENTS.md). Đề xuất: dùng `say` cho *timing tạm*, chọn nhà cung cấp cuối trước G4.
2. **Ảnh tư liệu / bản đồ** cho beat về thatch và beat đường sắt: cần nguồn có license hoặc tự vẽ diagram. Phương án dự phòng: thẻ chữ/sơ đồ tự dựng (không cần license).
3. **Ngưỡng loudness** (đề xuất -14 LUFS).

## Thứ tự triển khai (mỗi bước có test chấp nhận)
1. `schemas/sources.schema.json` + validator source/claim → test: claim verified thiếu `quote`/`locator` thì bị chặn.
2. `narration.json` + `beat_ids` + kiểm tra độ bao phủ → test: beat loại fact không có claim thì lỗi; shot tham chiếu beat không tồn tại thì lỗi.
3. Project pilot `projects/roof-pitch-suffolk/` (copy cấu trúc roof-evolution, variant mới) → `validate` + `check-blender` + still.
4. `tools/timing.py` với audio tạm → test offline với file WAV tổng hợp (stdlib `wave`): thời lượng → số frame đúng, làm tròn lên, có pad.
5. `tools/assemble.py` + media QA audio → test: độ lệch A/V ≤ 1 frame, loudness trong ±1 LU so với đích, phụ đề khớp beat.
6. Duyệt người: G1 (sự thật) → khóa narration → TTS cuối → G4 → render `review` → G3 → `final-gate`.

## Ngoài phạm vi M3
Mô hình thatch, mái gãy góc (kicked eaves), template `TIMELINE`/`CUTAWAY`, tải asset tự động, đăng YouTube, video dài 8–15 phút.
