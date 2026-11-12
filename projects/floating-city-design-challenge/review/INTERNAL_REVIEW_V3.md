# Bản internal review đầy đủ v3 (2026-11-12)

**Đầu vào:**
- Review của Codex trên FULL v2 (`a2b2bba`), chủ kênh chuyển tiếp ngày 2026-11-12.
  - Codex đề nghị sửa nốt hai đoạn chuyển nước, ở B31 và B33.
  - Codex đề nghị giữ màu nước, watermark và khoảng trống 2,8 s đầu B37.
- Chủ kênh: "tôi đã tải các sfx từ pixabay theo đề nghị tại `review/SFX_LIBRARY.md`, hãy thêm vào video".

**Phạm vi:**
- Lời dẫn, kịch bản và mọi shot khác giữ nguyên. Chỉ render lại SC_031 và SC_033, đúng theo báo cáo cache.
- Màu nước, watermark và B37 giữ như v2, theo đề nghị của Codex. Agent **không ghi** các mục này là quyết định của chủ kênh: chủ kênh chuyển tiếp review, chưa nói đã duyệt.

Đây không phải bản FINAL. Không ghi việc duyệt claim, giọng, phát âm, âm thanh hay xuất bản nào.

## Hai đoạn chuyển nước
| Chỗ | v2 | v3 |
|---|---|---|
| **B31, 9:33,75** | Nước bắt đầu trong 1,0 s sau khi camera bắt đầu hạ, khi camera còn chéo; lộ lưới bóng phao dưới đáy | Nước trong trong 0,6 s, bắt đầu 0,4 s trước khi camera tới khung ngang. Khung ngang cuối giữ nguyên |
| **B33, 10:07,5–10:08,5** | Như trên; lộ bóng hai phao dưới đáy và mép khối nước trong lúc mô-đun đang nhô lên | Như B31. Mô-đun nhô lên khỏi mặt nước đục, rồi nước mới trong |

- **Cách làm:** `CLEAR_LATE_BEFORE, CLEAR_LATE_SECONDS = 0.4, 0.6` trong `script/visuals.py`, chỉ cho hai shot có khung đầu cao (B31 ở 34°, B33 ở 22°). B22, B24, B30, B34 giữ cách cũ, vì Codex không thấy lỗi ở đó.
- **Test** (`test_floating_production`): mọi shot hạ xuống khung ngang chỉ được làm trong nước từ `CLEAR_AFTER` giây trở đi, và phải trong hẳn khi camera tới khung ngang.
- **Trước khi render:**
  - ảnh tĩnh của B31 tại 2,5 / 2,75 / 3,0 / 3,25 s: nước đục khi camera còn chéo, không còn lưới bóng;
  - ảnh tĩnh của B33 tại 5,0 / 5,25 / 5,6 / 6,0 s: không còn bóng phao; khi camera đang hạ vẫn thấy mặt trước của khối nước, nhưng ở dạng một dải nước đục, đều màu;
  - kiểm Blender hai shot: 39/39.

**Đính chính v2:** báo cáo v2 ghi "B30/B31: không còn lưới bóng lúc chuyển". Câu đó **sai với B31**: Codex vẫn thấy lưới bóng ở 9:33,75. Agent đã bỏ sót khung đó khi xem đoạn chuyển. Với B30 thì câu đó đúng trên những khung đã xem.

## Âm thanh (SFX)
- **Nguyên tắc:** theo `review/SFX_LIBRARY.md`:
  - chỉ gắn âm khi có hành động vật lý mà lời dẫn đang nói;
  - âm cỡ mô hình;
  - không gắn âm cho chữ hay card;
  - nền nước chỉ ở hai đoạn mà nước là chủ đề.
- **Agent không nghe được.** Mỗi chỗ chọn một file bằng số đo. Bảng lựa chọn và lý do ở `review/SFX_LIBRARY.md`, mục "Đã đưa vào bản FULL v3".
- **Toàn phim:**
  - 4 tiếng gắn với hành động: B05 khối chìm, B09 đặt tầng, B10 thân phao sâu thêm, B13 đặt cầu;
  - 7 tiếng chuyển chương;
  - 2 đoạn nền nước ngắn: B17 (12 s) và B30 (8 s).
- **Giấy phép:**
  - cả 6 file dùng Pixabay Content License, đã kiểm trên trang từng file ngày 2026-11-12;
  - nguồn, tác giả và sha256 ghi trong `audio/sound_plan.json`;
  - thiếu file hay file bị thay thì pipeline dừng.
- **Pipeline** (`pipeline/sound.py`, `tools/excerpt.py`):
  - **Âm thu sẵn thay âm tổng hợp:** STONE và STONE_HEAVY ở B09/B10 nay phát file thật (`replace`).
  - **Neo theo bước storyboard:** các tiếng thêm neo vào một bước của storyboard (shot, số bước, `do`), nên không đổi shot và không làm mất cache. Bước bị đổi thì pipeline từ chối.
  - **Tiếng chuyển chương** chỉ phát ở điểm cắt thật.
  - **Nền nước** được đặt theo RMS của lời dẫn (thấp hơn 26 dB), có fade.
  - **Test:** 6 test mới (`tests/test_sound_plan.py`).
- **Giới hạn:** `final-assemble` chưa trộn SFX. Hiện chỉ bản trích (`excerpt.py`) có SFX, nên trước khi làm bản 4K có SFX phải thêm bước này.

## Render và file
- **Báo cáo cache:** 2/44 shot cũ (SC_031, SC_033, lý do `shot_visual`), 42 shot dùng cache.
- **Render:** chương 7 render lại 2 shot trong 10:28 (19:03–19:14). Sau đó ghép lại bản đầy đủ, rồi xuất bản FULL_V3.
- **File:**
  - `output/pilot/floating_city_design_challenge_FULL_V3_INTERNAL_REVIEW_720p.mp4`: có SFX;
  - `output/pilot/floating_city_design_challenge_FULL_V3_INTERNAL_REVIEW_720p_no_sfx.mp4`: chỉ lời dẫn, cùng hình;
  - phụ đề `.en.srt` đi kèm từng bản;
  - `output/floating_city_design_challenge_INTERNAL_REVIEW_720p.mp4`: bản ghép của pipeline, chỉ lời dẫn.
  - Tất cả 784,2 s (13:04,2), 18 820 frame, có watermark.
  - Các bản FULL v1 và v2 vẫn để cạnh để so.

## QA
- **Kiểm Blender:** 586/586 toàn phim; trước khi render, kiểm riêng hai shot sửa được 39/39.
- **Bản ghép:** −16,4 LUFS, đỉnh thật −1,2 dBTP, 0 lỗi giải mã, 0 đoạn đen, 7 điểm nối giữa chương qua SSIM.
- **Bản FULL_V3** (`qa/excerpt_FULL_V3.json`): PASS.
  - 11 tiếng, 2 đoạn nền nước; không mẫu nào bị cắt.
  - Hai bản có/không SFX cùng −16,4 LUFS; đỉnh thật −1,1 và −1,2 dBTP.
  - Whisper: 44/44 shot không nghe kém đi khi có SFX.
  - Watermark có mặt.
- **Đo SFX trong file** (hiệu giữa hai bản WAV trước chuẩn hóa):
  - mỗi âm nằm đúng mốc, đúng mức đã đặt (tiếng ngắn thấp hơn đỉnh lời dẫn 12–17 dB; nền nước thấp hơn RMS lời dẫn 26 dB);
  - 7 tiếng chuyển chương đều hết trước khi lời dẫn của chương mới bắt đầu;
  - ngoài các mốc, track SFX im lặng.
  - Bảng mốc ở `qa/EDITORIAL_REVIEW_TIMECODED.md`.
- **QA phim dài:** 17/17. **Gate:** G0–G6, GL, GV đều PASS ở hồ sơ `NARRATED_INTERNAL_REVIEW`; hồ sơ này không đánh giá xuất bản.
- **Test:** 493 PASS, kể cả các file gọi Blender.
- **Một lỗi quy trình:** trong lúc chương 7 render, agent lỡ chạy hai file test có gọi Blender. Hai Blender chạy cùng lúc trong vài giây, chỉ để render 6 frame của một dự án tạm. Kết quả render không đổi, vì render cho ra kết quả giống hệt mỗi lần, và kiểm Blender toàn phim sau đó đạt 586/586.

## Xem trong MP4 v3
- **B31:** đạt. Ở 9:33,75 nước còn đục; không còn lưới bóng.
- **B33:** không còn bóng phao dưới đáy.
- **Còn tồn ở B33:** khoảng 10:07,0–10:07,75 vẫn thấy một góc mép bãi nước ở góc khung, khi camera đang hạ. Lỗi này do đường đi của camera, đã có từ v2. Muốn sửa phải đổi đường camera của B33, hoặc nới bãi nước của site; cách sau làm mất cache mọi shot dùng site đó.

## Cần chủ kênh quyết
1. **SFX:** nghe bản FULL_V3 có SFX và bản `_no_sfx`.
   - Mỗi âm có thể bỏ, đổi file hay chỉnh mức trong `audio/sound_plan.json`, không phải render lại hình.
   - Thứ tự đề nghị nếu thấy thừa: bỏ 7 tiếng chuyển chương trước, rồi tới hai đoạn nền nước.
2. **B33:** giữ góc mép bãi nước khoảng 0,75 s, hay sửa đường camera (render lại SC_033).
3. **Các đề nghị "giữ" của Codex** (màu nước, watermark, B37, nhịp B15/B16, cue phụ đề 35) chưa được ghi là quyết định; cần chủ kênh xác nhận.
4. **Phim Gothic:** chuỗi 5 card SC_024–SC_028 vẫn chưa có quyết định.

**Kho âm thanh trong `sfx/`:**
- `sfx/pixabay/` không được đưa vào git, vì giấy phép Pixabay không cho phân phối file đứng riêng. `audio/sound_plan.json` ghi đủ link và sha256 để tải lại.
- Các file CapCut cũ trong `sfx/` đã bị xóa khỏi thư mục làm việc (đang là thay đổi chưa commit). Agent để nguyên, không commit thay đổi này.

Agent không ghi một buổi nghe hay một lần duyệt nào cho các mục trên.
