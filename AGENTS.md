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

