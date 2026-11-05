# Báo cáo QA M3 — pilot "Why Did Traditional Roofs in Suffolk Change?" (2026-10-27)

**Kết luận: PREVIEW NỘI BỘ ĐỂ DUYỆT — CHƯA SẴN SÀNG XUẤT BẢN.** Về kỹ thuật pipeline đã hoàn chỉnh; G1 (duyệt biên tập) và G2 (license giọng đọc) vẫn mở, nên G6 bị chặn đúng thiết kế.

Môi trường: macOS 26.6.2 · M4 Pro 24 GB · Blender 5.2.2 LTS · FFmpeg 9.0.1 · Python 3.14.6 · OmniVoice 0.1.5 (gradio 6.15.2, torch 2.12, MPS). Nhánh git: `m3-narrative-pipeline` (tách từ tag `m2.5-validated`).

## Gate (`python3 tools/cli.py gates --project suffolk-roofs` → `qa/gates.json`)
| Gate | Trạng thái | Bằng chứng |
|---|---|---|
| G0 project & schema | PASS | `validate` |
| G1 bằng chứng & kịch bản | **PENDING_EDITORIAL** | 7 claim được dẫn đều SOURCE_VERIFIED (có vị trí + trích dẫn); chưa claim nào EDITORIALLY_APPROVED; `research/RESEARCH_REPORT.md` |
| G2 OmniVoice API & license | **BLOCKED_LICENSE** | API: adapter có test, 14/14 câu được sinh + kiểm tra ASR; license: `LICENSE_REVIEW_REQUIRED` (Boson Higgs Audio 2 Community License trong tokenizer) |
| G3 khóa timing lời dẫn | PASS | `script/timing.json`: 1752 frame, `locked: true`, hash của narration và audio khớp |
| G4 preview Blender | PASS | QA Blender 66/66, media QA PASS, đã xem frame (mục bên dưới), MCP 6/6 lệnh gọi |
| G5 ghép video | PASS | 1752 frame / 73.000 s, lệch A/V 0 ms, −16.5 LUFS, −1.3 dBTP, 14 cue phụ đề |
| G6 sẵn sàng xuất bản | **BLOCKED** | claim chưa duyệt biên tập; license giọng đọc; asset AST_003 đang chờ; `factual_review` vẫn provisional |

## Kiểm tra tự động
- `python3 -m unittest discover -s tests` → **77/77 OK** (59 cũ + 18 M3). Cụ thể: adapter OmniVoice ×10 (mất kết nối, phản hồi sai, sự kiện lỗi, status sai, im lặng, hợp đồng đổi, timeout, tốc độ nói bất thường, clone/upload, đo thời lượng); cache tái sử dụng (+ khóa đổi khi đổi bản model); lập lịch (frame chính xác, neo thời gian, nới shot cho animation, độ bao phủ beat, neo sai); thiếu source_ids / thiếu thông tin license / claim REJECTED; locator + excerpt; ghép FFmpeg (độ dài track, SRT, lệch, beat chồng nhau); final gate; `structure_from`; hồi quy lỗi fade ở intro.
- `check-blender`: `suffolk-roofs` **66/66**, `roof-evolution` **58/58** (không hồi quy).
- Smoke test đầu-cuối (`smoke --shot SC_003`): beat B3 → OmniVoice → render Blender → MP4 có lời dẫn: **PASS** (236 frame, lệch 0 ms, −16.8 LUFS). Kiểm tra độc lập bằng ffprobe/silencedetect.
- Media: 6 MP4 theo shot + bản câm + bản có lời dẫn, 0 đoạn đen. Điểm nối "match": SC_002→SC_003 SSIM 1.0; SC_005→SC_006 0.99974. Điểm cắt cứng khai báo `hard`: SC_001→002, 003→004, 004→005.
- ASR (Whisper large-v3-turbo, offline): 14/14 câu là English, WER tối đa 0.111.

## Lỗi phát hiện và đã sửa trong M3
| # | Phát hiện | Bằng chứng | Cách sửa |
|---|---|---|---|
| 1 | Câu B6.s2 đọc vội (14 từ trong 3.0 s) | Kiểm tra tốc độ nói 4.67 từ/giây > 4.5 | Sinh lại tối đa 3 lần (`MAX_TAKES`); lần sau 4.05 từ/giây |
| 2 | Manifest chỉ được lưu ở cuối → một câu lỗi làm mất bản ghi cache của 13 câu đã sinh | Lần chạy đầu | Lưu sau mỗi đoạn |
| 3 | **Nhà giữa của SC_006 hiện mái tranh thay vì ngói** | Still 06_comparison | Intro chỉ làm hiện dần các phần state thực sự hiển thị; thêm chốt chặn khi plan animate phần đang bị ẩn tĩnh; có test hồi quy |
| 4 | Exploded view của thatch đưa ngói nóc ra ngoài khung 4.3% | `camera_framing` FAIL | Quãng tách 0.9/1.1 → 0.55/0.5 m |
| 5 | SC_002 đứng yên 14.5 s và mô tả nói "lộ rafters" trong khi hình không lộ | Contact sheet; still tại exploded_hold | Đổi sang EXPLODED_VIEW (tách lớp tranh); sửa `visual_purpose` cho đúng với hình |
| 6 | Ngắt dòng phụ đề để chữ trơ trọi | SRT | Chia hai dòng cân bằng |
| 7 | Ghi chú nguồn trên card quá nhỏ ở 640×360 | Still card | Cỡ chữ 0.024 → 0.03 |

## Hình khớp với lời (frame đã render + MCP `look`)
| Shot | Lời dẫn được minh họa | Kiểm tra |
|---|---|---|
| SC_001 | "historic roofs do not all look alike … steeply … lower" | Ba nhà cùng tỷ lệ: thatch 50° / ngói 50° / slate 30° |
| SC_002 | "Longstraw thatch … about fifty degrees" | Lớp tranh dày nhấc lên, highlight trong lúc giữ, trở về chính xác |
| SC_003 | "clay peg tiles replaced some of these thatched roofs" | Chỉ thay 3 phần lớp phủ; 28 object (gồm rafters) đứng yên; xảy ra ở 1.2–3.0 s trong câu dài 0.3–4.2 s |
| SC_004 | pantile thế kỷ 18; đường sắt thế kỷ 19 → slate | Chữ/mũi tên hiện đúng mốc câu; dòng "Schematic, not to scale" |
| SC_005 | "Slate … around thirty degrees" | Thay toàn bộ 8 phần (kết cấu 30° riêng) |
| SC_006 | "typical pitch … tendencies, not rules" | Camera lùi ra từ slate (khớp camera SC_002); highlight sau intro |

## Giới hạn còn lại
- **Cách phát âm "Babergh"** cần người kiểm tra (Whisper nghe thành "Baburg").
- **Phụ đề** cấp câu; các câu dài cho ra dòng 46–67 ký tự. Muốn tách cue cần căn chỉnh theo từ (Whisper word timestamps), chưa triển khai — không chia theo tỷ lệ ký tự để tránh bịa timing.
- Đường hàng ngói/slate chỉ hiện mờ ở 640/960; texture rơm rất nhẹ. Mô hình là minh họa, không phải tái dựng.
- Exploded view của thatch không lộ được rafters từ góc camera này (mô tả đã ghi đúng như vậy).
- Sửa câu chữ của shot vẫn kích hoạt render lại (khóa cache băm toàn bộ JSON của shot).
- Âm sắc giọng nhất quán nhờ clone từ một mẫu tổng hợp; chưa có chỉ số đo độ tương đồng giọng nói.
- Không có nhạc nền (không cần, và chưa kiểm tra quyền).
