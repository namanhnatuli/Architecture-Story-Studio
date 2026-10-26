# Current project status

- Phase: **M2.5 — ổn định hóa: xong và đã kiểm chứng (2026-10-27). Sẵn sàng bắt đầu M3** (kế hoạch trong `docs/m3/`, cần người dùng quyết định một số điểm trước).
- Pilot `projects/roof-evolution`: 20 giây, 5 shot (HOLD 2.0 s → EXPLODED_VIEW 5.0 s → REPLACE_PARTS 6.0 s → HOLD + highlight 2.5 s → SIDE_BY_SIDE + intro 4.5 s). Đây là bản minh họa kỹ thuật, không phải tập phim đã được nghiên cứu.
- Gates: G0 PASS · G1 provisional (đúng như kỳ vọng) · G2 PASS (960×540) · G3 PASS ở mức preview kỹ thuật (640 + 960) · G4 chưa khóa · G5 bị chặn (`final-gate` vẫn báo lỗi, đúng thiết kế).
- Git: nhánh `master`, các commit `init` (v0.1 của người dùng) → `m2-baseline` → M2.5. Không có remote; chưa push.
- Môi trường đã kiểm chứng: macOS 26.6.2, Apple M4 Pro 24 GB, Blender 5.2.2 LTS, FFmpeg 9.0.1, Python 3.14.6.

## Lệnh tái tạo kết quả
```bash
python3 tools/cli.py validate
python3 -m unittest discover -s tests -v          # 49 test, gồm QA trong Blender
python3 tools/cli.py check-blender                # 58 kiểm tra -> qa/blender_checks.json
python3 tools/cli.py still                        # 640×360 key stills -> output/stills/
python3 tools/cli.py preview                      # 640×360 -> output/roof_evolution_preview.mp4 (~3.5 phút)
python3 tools/cli.py preview --preset review      # 960×540 -> output/roof_evolution_preview_review.mp4 (~9.3 phút)
python3 tools/cli.py manifest --check             # PACKAGE_MANIFEST.sha256 khớp git
```

## Đã làm / đã kiểm chứng / đề xuất
| Hạng mục | Đã làm | Đã kiểm chứng | Ghi chú |
|---|---|---|---|
| Template REPLACE_PARTS / EXPLODED_VIEW / SIDE_BY_SIDE (+ intro) / HOLD | ✅ | ✅ test + Blender QA + render 640/960 + MCP `look` | |
| Sửa 7 lỗi M2 (rafters, highlight, ánh sáng, dithering, cắt cứng, manifest, frame cũ) | ✅ | ✅ (`qa/M2_5_QA_REPORT.md`) | |
| Kiểm tra hình ảnh qua Blender MCP | ✅ 30/30 lệnh gọi tool thành công (trước + sau khi sửa) | ✅ (`qa/MCP_QA_REPORT.md`) | Qua client stdio; phiên Claude Code vẫn chưa có tool MCP gốc |
| Git baseline + `.gitignore` | ✅ | ✅ | Chưa push (cần cho phép) |
| Kế hoạch M3, brief nghiên cứu, storyboard nháp | ✅ (tài liệu) | — | **Đề xuất**: chưa triển khai, claim đều provisional |
| Blender 4.5 LTS | Mã có nhánh tương thích | ❌ chưa kiểm tra | |
| Audio / TTS / phụ đề / ghép video có tiếng | ❌ | — | Phạm vi M3 |

## Giới hạn đã biết
- Chỉ có builder nhà hình chữ nhật + mái gable. Mái tranh và mái gãy góc nằm ngoài phạm vi M3.
- Tấm phủ mái vẫn ăn vào mép ngoài đỉnh tường khi nghỉ (không camera nào thấy); kiểm tra cấu kiện chỉ áp cho rafters / ridge beam.
- ⚠️ MCP: một server `blender` ở scope local (không safe mode, telemetry bật, không ghim phiên bản) đang ghi đè `.mcp.json`. Cần người dùng quyết định (`docs/07_MCP_AND_AGENT_SETUP.md`).
- Animation chỉ mang tính gợi ý vật lý, không phải mô phỏng kỹ thuật.

## Việc tiếp theo (M3)
1. Người dùng quyết định: nhà cung cấp TTS (license), dùng ảnh tư liệu hay sơ đồ cho thatch/đường sắt, có dùng claim luật Mỹ (CLM_006) hay không, và xử lý server MCP ở scope local.
2. Duyệt G1 cho `docs/m3/PILOT_RESEARCH_BRIEF.md` (kiểm tra lại trích dẫn, tìm nguồn độc lập thứ hai).
3. Triển khai M3 theo thứ tự trong `docs/m3/M3_IMPLEMENTATION_PLAN.md` (schema nguồn → narration/beat → project pilot → timing → ghép video).
