# Quickstart Mac M4 · Beginner (từ 0 đến video thử)

## 0. Phần mềm tối thiểu
1. Tải và cài **Blender 5.2 LTS** cho macOS Apple Silicon: https://www.blender.org/download/ (hoặc Blender 4.5 LTS nếu bạn cần bản cũ). Mở Blender một lần sau khi kéo vào Applications.
2. Mở Terminal (Command + Space → Terminal).
3. Cài **Homebrew** theo đúng hướng dẫn tại https://brew.sh/ (không chạy lệnh cài ngẫu nhiên từ nguồn khác).
4. Sau khi `brew` hoạt động: `brew install ffmpeg`.
5. **Python 3:** `python3 --version`. Nếu macOS báo chưa có, có thể `brew install python`.

Bạn **không cần** cài `bpy` qua pip. Script Blender chạy bằng Python đi kèm Blender.

## 1. Giải nén và vào project

Tải ZIP, giải nén (nhấp đúp). Mở Terminal, gõ `cd ` (có dấu cách), kéo thư mục `Architecture-Story-Studio` vào Terminal, nhấn Enter.

```bash
pwd
python3 tools/cli.py doctor
python3 tools/cli.py validate
python3 -m unittest discover -s tests -v
```

`doctor` cho biết máy đã thấy Blender/FFmpeg chưa. Nếu Blender cài ở đường dẫn khác, đặt biến môi trường:

```bash
export BLENDER_BIN="/Applications/Blender.app/Contents/MacOS/Blender"
```

## 2. Render ảnh đầu tiên (mặc định preview)

```bash
python3 tools/cli.py still
```

Đợi Blender thoát, sau đó xem:
`projects/roof-evolution/output/roof_evolution_still.png`

Nếu ảnh đúng, tiếp tục:

```bash
python3 tools/cli.py preview
```

Kết quả:
`projects/roof-evolution/output/roof_evolution_preview.mp4`

**Cảnh 6 giây, 24 FPS, 640×360.** 144 frame có thể tốn thời gian trên máy cá nhân. Chạy ảnh still trước để tránh render hàng loạt khi scene còn lỗi.

## 3. File mà AI cần đọc

Đưa AI vào thư mục này và dùng prompt trong `prompts/00_START_CODING_AGENT.md`. Codex và Claude Code đều phải tuân thủ `AGENTS.md`.

## 4. Nếu gặp lỗi

- `blender not found`: kiểm tra Blender ở Applications và `BLENDER_BIN`.
- `ffmpeg not found`: `brew install ffmpeg`; có thể vẫn render PNG, nhưng chưa encode MP4.
- `bpy` missing trong terminal Python: bình thường. Chỉ gọi Python script Blender bằng Blender CLI.
- Blender 4.5/5.x engine errors: `engine/scene.py` chọn Eevee theo phiên bản (`BLENDER_EEVEE_NEXT` / `BLENDER_EEVEE`).
- Renders lỗi do thiếu quyền: giữ project trong Documents/Home, tránh iCloud hay thư mục bảo vệ khó ghi.
- Máy nóng hoặc hết RAM: giảm `preview.width/height` trong `config/render_presets.json`, đóng ứng dụng nặng; không bật Cycles/4K.
- Lỗi nào khác: gửi nguyên dòng lệnh và đoạn cuối của log trong `projects/roof-evolution/qa/`.

## 5. Quy trình làm tiếp

Không chuyển thẳng từ pilot sang video 15 phút. Bước kế tiếp là kiểm tra 10s animation biến đổi cấu kiện, sau đó thử một scene theo luận điểm thực tế (có nguồn), rồi xây thư viện `REPLACE_PARTS`, `CUTAWAY`, `SIDE_BY_SIDE`.

## 6. MCP (tùy chọn)

Pilot không cần MCP. Đọc `docs/07_MCP_AND_AGENT_SETUP.md` nếu muốn Codex/Claude tương tác với Blender trực tiếp. Cài plugin MCP là thay đổi có nguy cơ chạy Python: sử dụng project thử và không cấp quyền file ngoài dự án.
