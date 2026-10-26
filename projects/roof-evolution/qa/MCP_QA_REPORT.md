# Báo cáo QA qua Blender MCP — M2.5 (2026-10-26/27)

## Kết nối
| Mục | Kết quả |
|---|---|
| Tool MCP gốc trong phiên Claude Code | **Không có** (phiên khởi động trước khi server được đăng ký) |
| Cách gọi tool | Client JSON-RPC/stdio bằng stdlib → `uvx mcp-for-blender==2.2.4` (env: `BLENDER_MCP_SAFE_MODE=1`, `DISABLE_TELEMETRY=true`, localhost:9876) |
| Server / addon | MCP for Blender 1.30.0 · addon 1.8 · protocol 15 · `up_to_date: true` · Blender 5.2.2 LTS · `telemetry_consent: false` · mọi thư viện asset + generator **tắt** |
| Blender dùng để kiểm tra | Phiên bản GUI riêng (PID 78428) mở **bản sao** `SC_002/003/005.blend` trong scratchpad; cổng `127.0.0.1:9876` (loopback). Đóng (PID 78428) sau khi xong. Blender của người dùng không bị đụng tới |
| Số lệnh gọi | Trước khi sửa: **21/21 thành công**; sau khi sửa: **9/9 thành công** (`qa/mcp/*/mcp_calls_log.json`) |
| Tool đã dùng | `get_addon_status`, `get_scene_info`, `execute_blender_code` (`open_mainfile`, `frame_set`, đọc thuộc tính), `look` (`frames` qua camera, `angles` + `xray`/`solid`, `camera`) |

Lý do addon trong phiên Blender của người dùng không lắng nghe: phiên đó khởi động lúc 22:16:54, **trước khi** addon được cài/bật (22:19–22:20).
⚠️ `claude mcp list` đang ưu tiên một server `blender` ở **scope local**: không ghim phiên bản, **không safe mode, telemetry bật**. Xem `docs/07_MCP_AND_AGENT_SETUP.md` (không tự sửa).

## Phát hiện trước khi sửa (`qa/mcp/before_fix/`)
| # | Shot / frame | Tool | Phát hiện | Mức độ |
|---|---|---|---|---|
| 1 | SC_002 f1 | `look angles xray` (`rest_xray_front_0.png`) | Đầu dưới rafters của mái A cắm vào đỉnh tường trái/phải | Trung bình: lộ ra khi tấm phủ nhấc lên |
| 2 | SC_003 f84 | `look angles xray` có target (`SC_003_f84_xray_walls_0.png`) | Đuôi rafters của mái B nhô xuyên qua mép trên tường phải ("răng") | Trung bình |
| 3 | SC_003 f36–56, f84 | `look frames camera` + `look camera` (`SC_003_camera_frames_0.png`, `SC_003_f84_camera_0.png`) | Phần đang mờ dần có **nhiễu dithering** dạng lốm đốm/giấy nhám | Thấp–trung bình |
| 4 | SC_005 f47 | `look frames camera` (`SC_005_camera_frames_0.png`) | Ở đỉnh highlight, mái A graphite ngả xám | Trung bình (mất nhận diện A/B) |
| 5 | SC_005 | `look angles top/front` + `execute_blender_code` | **Đạt**: footprint không chồng nhau; slot A (−3.25, −2.53), slot B (3.25, 2.53) dọc trục camera-right; `wall_left` có cùng transform local (−2.3, 0, 1.275) ở cả hai slot, world khác đúng bằng offset | — |
| 6 | Mọi shot | `look angles` không có target | Tự đóng khung theo mặt sàn 160 m → ảnh vô dụng (`SC_003_f84_xray_0.png`). Bài học: luôn truyền `target` | Quy trình |

## Kiểm tra lại sau khi sửa (`qa/mcp/after_fix/`)
| # | Kiểm tra | Bằng chứng | Kết quả |
|---|---|---|---|
| 1 | SC_002 f1 xray: rafters gác trên tường | `after_SC_002_rest_xray_0.png` | **Đạt**: rafters dừng ở đỉnh tường |
| 2 | SC_003 f144 xray: rafters mái B | `after_SC_003_f144_xray_0.png` | **Đạt**: không còn "răng" xuyên mép tường |
| 3 | SC_003 mờ dần mượt, twin chỉ hiện khi đang mờ | `after_SC_003_camera_frames_0.png` + `execute_blender_code`: 14 twin; ở f84 chỉ hiện `roof_B_covering_left/right__fade` và `roof_B_ridge_beam__fade`; ở f144 không twin nào | **Đạt** |
| 4 | SC_005 intro: camera lùi ra, A hiện dần, sau đó khóa | `execute_blender_code`: ortho 14.356 (f1) → 15.52 (f19) → 16.684 (f37 = f60 = f108); độ trong suốt tấm phủ A 1.0 → 0.839 → 0.0; `after_SC_005_camera_frames_0.png` | **Đạt** |
| 5 | Highlight giữ màu A | `after_SC_005_camera_frames_0.png` (f60) + render 960×540 | **Đạt**: mái A sáng lên nhưng vẫn là graphite |

Lưu ý: ảnh `look` là ảnh viewport (material preview), **không phải** bản render Eevee cuối cùng. Kiểm tra cuối cùng về hình ảnh vẫn dựa trên frame render (`qa/progress_*_review.png`, `qa/contact_sheet_preview_review.png`).
