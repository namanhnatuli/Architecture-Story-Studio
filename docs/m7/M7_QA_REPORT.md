# M7: báo cáo QA, "Why Bridges Don't All Look the Same"

- Nhánh `m7-first-full-documentary`. Máy: Apple M4 Pro 24 GB, Blender 5.2.2 LTS (EEVEE), FFmpeg 9.0.1, Python 3.14.6.
- **Trạng thái kỹ thuật** tách riêng khỏi **mức sẵn sàng xuất bản**. Phim chưa được duyệt biên tập, nên mọi bản dựng mang nhãn INTERNAL REVIEW.

## Checkpoint A: nghiên cứu
- 12 nguồn, 42 claim, tất cả `SOURCE_VERIFIED`, chưa claim nào được duyệt biên tập. Mọi trích dẫn khớp nguyên văn với văn bản nguồn tải về. `research/build_sources.py` sinh lại `sources.json` giống hệt từng byte.
- Báo cáo: `projects/why-bridges-look-different/research/RESEARCH_REPORT.md`. Ma trận: `review/EVIDENCE_MATRIX.md`.
- Không chắc chắn đã xử lý: năm xây cầu Bollman (không nói); "still in service" (gán cho báo cáo 2005); "America's greatest stone arch" (gán cho báo cáo).
- Claim bị loại: "mặt trên dầm nén, mặt dưới kéo" và "đá chịu kéo kém" (không có nguồn đủ chặt). Không tô màu thanh bụng giàn.

## Checkpoint B: kịch bản và tính khả thi về hình
- `script/story.py` là nguồn duy nhất: 8 chương, 39 beat, 102 câu, 1310 từ.
- **Lời dẫn:** Kokoro `bm_george`, `--purpose publication`, hạng quyền `PUBLICATION_CLEARED`. ASR 102/102 câu đạt (WER ≤ 0,15).
- **Sửa câu theo bằng chứng đo được**, ghi trong `revision.edits`:
  - B18.s2: đọc chậm 1,47 từ/s.
  - B20.s0, B22.s0, B35.s0: câu quá ngắn, khoảng lặng cuối kéo tốc độ xuống dưới ngưỡng.
  - B15.s0: ASR nghe "Trust".
  - B23.s2: số viết bằng chữ.
  - B20B: tách câu để hình đổi theo ý thứ hai.

  Ngưỡng kiểm tra không bị nới.
- **Sửa nội dung theo nguồn trước khi đọc:**
  - CLM_748 không tồn tại → B12 trích CLM_709/710.
  - Bỏ tên "Wendel", vì excerpt không có.
  - "timber trusses fell out of use", đúng với nguồn.
  - "lack of permanence" thay cho "shorter life".
  - Thêm "reinforced concrete" vào nguyên nhân suy giảm.
  - "Great Depression" thay cho "the 1930s".
- **Timing:** khóa 640,67 s audio. Kế hoạch 47 shot, 15391 frame = 641,29 s (10,69 phút); `validate-plan` đạt.
- **Lỗi pipeline phát hiện và sửa:**
  - Planner chưa từng lập kế hoạch thời lượng cho card (unknown template `CARD`) → thêm `templates.plan_card`.
  - Planner vỡ khi shot trước không có state (card) → chặn chỉ số rỗng.
  - `narrate` chặn dự án audio-first khi beat đổi → lọc lỗi hạ nguồn.
  - Rect chỉ có viền trong helper bị vẽ thành khối đặc.
  - Card QA không phát hiện chữ chồng nhau → thêm kiểm tra.
- **Gate của planner được giữ:** SHOW_EVOLUTION cần claim niên đại đã duyệt. Hai beat dòng thời gian được khai báo là bối cảnh (SHOW_CONTEXT / SUMMARIZE_DIFFERENCES); không có hình "tiến hóa".
- **QA phim dài** (`qa/longform_qa.json`): 11 kiểm tra, 0 FAIL, 2 WARN.
  - Câu hỏi mở đầu được lặp ở phần kết, có chủ ý.
  - Chương 2 chỉ có 3D_HOLD, nhưng mỗi shot có chú thích dựng dần.
  - Đoạn tĩnh dài nhất 13,0 s (giới hạn 14 s). Khoảng lặng dài nhất 1,23 s.
  - Qua các vòng sửa, phép kiểm này đã bắt được ba đoạn tĩnh thật: B20B 14,4 s, B14 16,3 s, và chương 6 có 8 card liền nhau (165 s).
- **QA Blender toàn phim:** 569/569 (`qa/blender_checks.json`).
  - Lần đầu bắt được nhãn dòng thời gian tràn ra ngoài vùng an toàn và nhãn 1829/1848 chồng nhau. Bố cục timeline được viết lại: ước lượng bề rộng chữ, kẹp trong vùng an toàn, xếp vào hàng trống.

## Checkpoint C: một chương hoàn chỉnh (C4 "The arch", 960×540)
- `chapter --chapter C4 --preset review`: 6 shot, 1974 frame (82,25 s), h264 960×540 24 fps, 0 lỗi giải mã, 0 đoạn đen, 5 điểm cắt cứng.
- Ghép lời dẫn: −16,0 LUFS, true peak −1,4 dBTP, 18 câu phụ đề (tối đa 42 ký tự/dòng, tối đa 16,4 ký tự/s), có track mov_text. Tên file `…_C4_documentary_INTERNAL_REVIEW.mp4`.
- **Xem frame thật, ba lỗi:**
  - SC_018: góc cận bộ phận làm cầu nằm nửa trên khung, mố bị cắt → chuyển sang HOLD góc chính diện toàn cảnh. Ở góc ba phần tư, kiểm tra tầm nhìn báo mố bị địa hình che, nên không dùng.
  - SC_019: chân vòm không đặt lên mố, cột ván khuôn ngoài lòng vòm → vẽ lại hình học.
  - SC_020: ghi chú đè viền khung, dòng nguồn nằm trên tiêu đề → dời.
- **Dựng lại:** 3 shot CACHED, 3 shot render lại, 383 s.
- **MCP** (`mcp-for-blender` 2.2.4, safe mode, `127.0.0.1:9876`): một GUI Blender riêng mở **bản sao** SC_017.blend và SC_019.blend (không có Blender nào khác đang chạy). Đã đóng sau khi kiểm.
  - SC_017 qua camera ở frame 400: lực đẩy chạy dọc vòm giữa; mũi tên tải, phản lực, callout "Mainly compression" và thẻ "not to scale" gắn đúng bộ phận.
  - SC_019 nhìn xiên: 53 phần tử card là mặt phẳng xếp lớp, không phần tử nào còn trong suốt ở frame cuối.
  - Công cụ MCP gốc của phiên không bắt tay được với addon cũ (khác protocol), nhưng `execute_blender_code` và `look` vẫn chạy.

## Checkpoint D: rough cut 640×360
- Cả phim, 47 shot, 15.391 frame (641,29 s). Media QA đạt: h264, 0 lỗi giải mã, 0 đoạn đen, mọi điểm cắt khớp (match cut) có SSIM ≥ 0,98.
- Ghép lời dẫn: −16,0 LUFS, 144 câu phụ đề. Metadata `comment` = "INTERNAL REVIEW - editorial approval and/or rights pending - not for publication".
- **Xem lại theo chương** (ảnh mỗi 3 s và frame gốc), tìm thấy 8 lỗi; tất cả đã sửa. Chi tiết trong `projects/why-bridges-look-different/qa/EDITORIAL_REVIEW_TIMECODED.md`:
  - NOTE trôi khỏi khung trong 3 shot push-in. Đây là lỗi engine; sửa bằng rig chú thích đi theo camera, kèm QA `overlays_screen_fixed`.
  - Viền phim còn trên 3 ảnh HAER.
  - Cảnh kết thiếu nhãn miễn trừ.
  - Card ghi công quá ngắn.

## Checkpoint E: review cut 960×540
- Render lại toàn bộ, vì file engine thay đổi. Sau đó sửa nhãn B16 theo từ: chỉ SC_022 render lại, còn 46 shot CACHED.
- `output/why_bridges_look_different_documentary_INTERNAL_REVIEW_review.mp4`: **15.515 frame, 646,458 s (10,77 phút)**, h264 960×540 24 fps + AAC 48 kHz + phụ đề mov_text.
  - −16,0 LUFS, true peak −1,5 dBTP, độ lệch tiếng/hình ≤ 1 frame.
  - **145 câu phụ đề** cho 103 câu: tối đa 42 ký tự/dòng, 19,3 ký tự/s, 0 câu phải lùi về mốc theo cả câu.
- Media QA đạt (`qa/preview_media_report_review.json`).
- **Tám chương** có MP4 + SRT + WAV riêng (`output/chapters_review/`), tất cả dựng từ frame CACHED:

  | Chương | Frame | Thời lượng | Câu phụ đề |
  |---|---|---|---|
  | C1 | 848 | 35,3 s | 8 |
  | C2 | 1204 | 50,2 s | 11 |
  | C3 | 1630 | 67,9 s | 15 |
  | C4 | 1974 | 82,3 s | 18 |
  | C5 | 2008 | 83,7 s | 21 |
  | C6 | 3007 | 125,3 s | 26 |
  | C7 | 3041 | 126,7 s | 29 |
  | C8 | 1803 | 75,1 s | 17 |

  Tổng frame và tổng câu phụ đề khớp với cả phim. Mỗi chương −16,0 LUFS.
- Master audio: `…_narration_master_clean_review.wav` (track gốc) và `…_audio_master_review.wav` (đã chuẩn hóa loudness).
- **Không có bản khắc phụ đề vào hình** (mục tùy chọn), vì bản FFmpeg này không có libass/freetype.

## Checkpoint F: chất lượng 1080p
- 47 still 1920×1080 (`output/stills_production_test/`), 53 s, mỗi still 1,53 MB.
- Ở độ phân giải gốc: chữ chú thích và card sắc nét, vân đá và mũi tên lực rõ.
- **Chưa render video 1080p.** Preset `final` bị G6 chặn khi chưa có duyệt; video 1080p nhãn INTERNAL REVIEW cần một preset riêng, hiện chưa có. Ước lượng đĩa: khoảng 24 GB PNG cho cả phim.

## Soi qua MCP, mỗi chương một frame
- GUI Blender riêng, chỉ mở **bản sao** `.blend`, safe mode, `127.0.0.1:9876`; không có Blender nào khác đang chạy; đã đóng sau khi kiểm.
- Các frame đã soi:
  - C1 SC_004: ba mô hình cùng tỉ lệ.
  - C2 SC_007: đường truyền tải tới móng.
  - C3 SC_013: dầm, xà mũ, cột.
  - C4 SC_017/SC_019: lực đẩy vòm, ván khuôn.
  - C5 SC_024: Warren sau khi thay bụng.
  - C6 SC_029: NOTE sắt rèn.
  - C7 SC_041: card Bollman.
  - C8 SC_046: frame cuối push-in, rig co 0,88 đúng bằng tỉ lệ ortho, NOTE vẫn trong khung.
- Nhận xét:
  - SC_013 (≈1:54): đường truyền tải, nhãn xà mũ, mũi tên tải và nhãn cột gặp nhau quanh xà mũ, hơi dày nhưng vẫn đọc được. Có thể cân nhắc khi biên tập.
  - Bản sao `.blend` ở thư mục khác thì ảnh hiện màu hồng, vì `.blend` lưu đường dẫn **tương đối** `//../assets/external/…`. Đó là đúng thiết kế (dữ liệu di chuyển được), không ảnh hưởng render.

## Cổng (`qa/gates.json`)
| Cổng | Kết quả |
|---|---|
| G0 dữ liệu/schema | PASS |
| G1 bằng chứng, kịch bản, phát âm | PENDING_EDITORIAL: 0/41 claim được lời dẫn dùng đã duyệt; `factual_review: pending`; phát âm 16 thuật ngữ PENDING |
| G2 lời dẫn & quyền TTS | **BLOCKED_RIGHTS**: Kokoro `PUBLICATION_CLEARED`, licence APPROVED ở mức provider, nhưng chủ kênh chưa xác nhận cho phim này |
| G3 khóa timing | PASS (15.515 frame) |
| G4 QA Blender + media | PASS (577/577) |
| G5 ghép media & phụ đề | PASS |
| GL phim dài | PASS (17 kiểm tra, 2 cảnh báo có chủ ý) |
| G6 sẵn sàng xuất bản | **BLOCKED** |
| GV kế hoạch hình | PASS |

Trạng thái: `TECHNICALLY_VALIDATED`, `EDITORIAL_REVIEW_PENDING`, `TTS_RIGHTS_PENDING`. Kết luận: **INTERNAL PREVIEW — NOT PUBLICATION-READY.**

## Test (đã chạy thật, 2026-10-30)
- `python3 -m unittest discover -s tests`: **310 test, OK**, không bỏ qua test nào, 104,6 s. Gồm 290 offline và 20 Blender.
  - 250 test cũ (234 offline + 16 Blender) vẫn đạt, không test nào bị nới.
  - Mới: `tests/test_m7_longform.py` (56 test) và `tests/test_blender_m7.py` (4 test).
- Test M7 phủ các mục spec yêu cầu:
  - chương: thứ tự, thiếu/trùng beat, chương rỗng, chương không tiêu đề, shot thuộc hai chương, mode `documentary`;
  - timing qua ranh giới chương;
  - trộn 2D/3D;
  - giấy phép ảnh (thiếu hồ sơ, thiếu trường, sai đường dẫn, thiếu file, vùng cắt sai, chưa approved, thiếu ghi công, hash khác);
  - claim thiếu;
  - cache theo chương (sửa một card chỉ làm cũ đúng shot đó);
  - khôi phục render bị ngắt (giữ frame hoàn chỉnh, xóa frame dở, khác khóa thì render lại);
  - sinh lại lời dẫn (timing bị coi là cũ), ASR dùng lại bản chép;
  - đồng bộ phụ đề (mỗi câu phụ đề nằm trong khoảng câu đã đo);
  - ghép media và độ dài phim cuối;
  - cổng xuất bản (không PUBLICATION_READY khi còn chờ; GL thiếu thì FAIL; xác nhận giọng và phát âm đang chờ thì chặn; đổi profile không tắt được cổng);
  - nhịp theo từ cho card và chú thích; NOTE; push-in và rig;
  - các ca âm của QA phim dài: câu thiếu, audio chồng nhau, hình lặp, chương không tiêu đề, mâu thuẫn lời/hình, đoạn tĩnh, đơn điệu, sai độ dài.
- Đánh giá planner: **29/29**.

## Hồi quy QA Blender trên dự án cũ (engine M7)
| Dự án | QA Blender |
|---|---|
| bridge-load-explained (pilot M6) | 176/176 |
| bridge-story-m5 | 188/188 |
| roof-plan-m5 | 52/52 |
| roof-evolution | 64/64 |
| bridge-structure-evolution | 92/92 |
| suffolk-roofs | **71/72** |

Ở `suffolk-roofs`, kiểm tra **mới** `card_layout` báo ghi chú chân trang của card SC_004 nằm dưới vùng an toàn: y 0,029–0,057, trong khi mép dưới là 0,05. Lỗi bố cục này có từ M3; code M7 không làm hỏng gì. Chưa sửa, vì dự án M3 giữ nguyên trạng thái. Cách sửa đề xuất: dời ghi chú lên y ≥ 0,07, rồi render lại SC_004.

Frame preview cũ của các dự án trên giờ là cache cũ, vì file engine đã thay đổi. Chúng sẽ được render lại khi chạy `preview`. Không render lại trong M7.
