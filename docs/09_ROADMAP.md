# SOP 09 — Roadmap / milestones

## M0 — Package verification
- `doctor`, `validate`, offline unit tests đều chạy không lỗi.

## M1 — Blender demo
- Still PNG và scene.blend; mái A/B với góc camera cố định.
- Animation 6s thể hiện A bay ra / B bay vào; MP4 preview qua FFmpeg.

## M2 — Visualization foundations
- `SIDE_BY_SIDE`, `EXPLODED_VIEW`, `HIGHLIGHT_DIFFERENCE`; tests cho mỗi template; asset manifest chuẩn.
- **Trạng thái 2026-10-26:** `REPLACE_PARTS`, `EXPLODED_VIEW`, `SIDE_BY_SIDE`, `HOLD` đã triển khai, có test và đã kiểm tra hình ảnh (pilot 20 s). `HIGHLIGHT_DIFFERENCE` mới có ở dạng tùy chọn `highlight`. Còn chờ: kiểm tra hình ảnh qua MCP, test Blender 4.5, preset review 960×540.

## M3 — Narrative video
- Pilot 60–90s có nguồn thật về một luận điểm thiết kế; TTS và timing lock; montage với ảnh tư liệu có license.

## M4 — Long-form
- 8–15 phút chia thành shots độc lập; script có research ledger, source credits; render resume/cache, ffprobe QA, subtitles.

## Không trong scope ban đầu
- Mô phỏng kết cấu chính xác bằng Blender rigid bodies.
- Web app Three.js tương tác.
- Rigs nhân vật/công nhân; marketplace asset downloading tự động.
- Tự đăng YouTube.
