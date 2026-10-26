# Current project status

- Phase: **M2 — Engine biến đổi trực quan tái sử dụng v1: đã triển khai và kiểm chứng trên Mac của người dùng (2026-10-26).**
- Pilot `projects/roof-evolution`: 20 giây, 5 shot (HOLD → EXPLODED_VIEW → REPLACE_PARTS → HOLD + highlight → SIDE_BY_SIDE), 640×360, 24 fps. Đây là bản minh họa kỹ thuật, không phải tập phim đã được nghiên cứu.
- Gates: G0 PASS · G1 provisional (đúng như kỳ vọng với pilot kỹ thuật) · G2 PASS (key stills đã xem) · G3 PASS ở mức preview kỹ thuật (QA tự động + đã xem frame) · G4 chưa khóa · G5 bị chặn. `final-gate` vẫn trả về lỗi.
- Môi trường đã kiểm chứng: macOS 26.6.2, Apple M4 Pro 24 GB, Blender 5.2.2 LTS, FFmpeg 9.0.1, Python 3.14.6.

## Lệnh tái tạo kết quả
```bash
python3 tools/cli.py validate
python3 -m unittest discover -s tests -v      # 43 test, gồm cả QA trong Blender
python3 tools/cli.py check-blender            # 50 kiểm tra -> projects/roof-evolution/qa/blender_checks.json
python3 tools/cli.py still                    # output/stills/*.png
python3 tools/cli.py preview                  # output/shots/*.mp4 + output/roof_evolution_preview.mp4 (~2.5 phút)
```

## Trạng thái theo hạng mục
| Hạng mục | Đã triển khai | Đã test | Đã kiểm tra hình ảnh |
|---|---|---|---|
| `REPLACE_PARTS` (nhấc lên / di chuyển / mờ dần / ẩn; hạ xuống + khớp đúng vị trí; stagger, thứ tự, xoay, override theo component) | ✅ | ✅ offline + Blender | ✅ ảnh render (CLI) |
| `EXPLODED_VIEW` (hướng theo từng component / gợi ý / tỏa ra, tuần tự hoặc đồng thời, trở về chính xác, highlight) | ✅ | ✅ (+ giao cắt BVH) | ✅ ảnh render (CLI) |
| `SIDE_BY_SIDE` (bố cục theo kích thước, cùng camera / ánh sáng / scale, dải nhãn, highlight khác biệt) | ✅ | ✅ (local vs world) | ✅ ảnh render (CLI) |
| `HOLD` + highlight | ✅ | ✅ | ✅ |
| Validator G0 cho template / ownership / timing | ✅ | ✅ (10 test, gồm tương thích ngược v1) | — |
| Cache render theo shot, MP4 theo shot, contact sheet / dải tiến trình, ffprobe / blackdetect | ✅ | ✅ (chạy thật) | ✅ |
| Kiểm tra hình ảnh qua Blender MCP | ❌ **Chưa làm** — phiên làm việc không có tool MCP; addon chưa lắng nghe | — | — |
| Blender 4.5 LTS | Mã có nhánh tương thích | ❌ chưa kiểm tra | — |
| Preset review 960×540 | Có cấu hình | ❌ chưa render | — |

## Giới hạn đã biết
- Không có TTS, dựng audio, nhập footage hay lấy nguồn tự động. Narration là placeholder.
- Chỉ có builder nhà hình chữ nhật + mái gable. Cầu, cột, khung… cần builder mới (cách mở rộng: `docs/05_ANIMATION_LIBRARY.md`).
- Ánh sáng/vật liệu ở mức greybox (hơi phẳng). Đỉnh highlight làm mái A ngả nhẹ về xám.
- Rafters ăn vào đỉnh tường khi ở vị trí nghỉ (không thấy được khi đã lắp đủ).
- Lần cắt SC_004 → SC_005 là cắt cứng.
- Animation chỉ mang tính gợi ý vật lý, không phải mô phỏng kỹ thuật hay vật lý.
- `PACKAGE_MANIFEST.sha256` mô tả gói v0.1 và không khớp với các file đã sửa.
- Frame cũ của v0.1 vẫn nằm ở `projects/roof-evolution/renders/preview/frame_*.png` (đã được thay bằng thư mục theo shot; bản sao v0.1 được lưu ở `qa/baseline_v0_1/`).

## Việc tiếp theo
1. Khởi động lại Claude Code để nạp `.mcp.json`, bật server MCP trong Blender, rồi lặp lại bước kiểm tra hình ảnh qua `look` (`isolated=True`).
2. Chỉnh ánh sáng/vật liệu (stage 8) và render thử preset `review` 960×540.
3. M3: một luận điểm thiết kế có nguồn thật (G1), narration + TTS timing lock (G4).
