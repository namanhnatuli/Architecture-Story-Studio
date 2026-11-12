# Bản internal review đầy đủ v2 (2026-11-12)

**Đầu vào:**
- Review của Codex trên bản FULL v1 (`ef13442`), chủ kênh chuyển tiếp ngày 2026-11-12. Phương án A:
  - giữ hai chuỗi 3D;
  - sửa cục bộ B33/B34, B13, khoảng chờ đầu card B03/B20, rồi nước, tương phản và mép bãi nước trong cùng lượt;
  - giao FULL v2, không làm pilot lẻ;
  - giữ hai bản âm thanh để nghe chọn;
  - đính chính câu "không nới ngưỡng QA" về dung sai keyframe.
- Chủ kênh thêm: "hãy thêm watermark `branding/concepts_20261107/A_watermark_burnin_640.png` ở góc video cho hợp lý".
- Quyết định của chủ kênh trong phiên: chấp nhận ngoại lệ `visual_variety` cho đúng hai chuỗi B08–B14 và B27–B31 (câu trả lời "Chấp nhận đúng 2 chuỗi (Recommended)").

**Phạm vi:**
- Giữ nguyên kịch bản c-r2 và lời dẫn: `script/narration.json` không đổi byte nào; 126 take TTS giữ nguyên.
- Giữ mở đầu B01–B02, bộ nhà và công viên, B08–B11.

Đây không phải bản FINAL. Bản này không ghi việc duyệt claim, giọng, phát âm hay xuất bản nào. Quyết định duy nhất được ghi là ngoại lệ ở trên.

## Góp ý → đã làm

| Góp ý (Codex v1) | Đã làm |
|---|---|
| **B33/B34 (10:07–10:40)** trông như mô hình lơ lửng trên nền xám; phải giữ mực nước rõ, chỉ làm trong phần cần nhìn. | Hai cảnh mở bằng nước đục: phao hộp nằm trên mặt nước, nhìn từ trên. Ở "semi" (B33) và "seawater" (B34), camera hạ xuống khung ngang mặt nước, đứng ngoài khối nước, giống B22–B31. Nước chỉ trong dần ở cuối lúc hạ. Mực nước là một đường thẳng; phao chìm, chân cột và thân phao dưới nước nhìn qua mặt nước. B33 thấy cả ba phần: sàn trên mặt nước, cột xuyên mặt nước, phao dưới nước. Khung đầu B33 nâng từ 12° lên 22° để không lộ mép bãi nước. |
| **B13 (3:45–3:53):** camera kéo xa đúng lúc cần thấy chênh 0,66 m. Cận hai mép sàn trong, thước đứng nối đúng hai cao độ, giữ chênh thật, nhãn không đè lên khe. | Khung thứ hai cận khe giữa hai phao, rộng khoảng 17 m (trước là cả hai phao 86 m). Thêm hình vẽ kích thước, đặt trên mặt trước hai phao (`floating.pair`: `deck_step_dim`, `deck_level_a/b`): <br>– cao độ mỗi sàn kéo ngang qua khe bằng nét đứt; <br>– một thước đứng có hai vạch nối hai cao độ, đúng 0,664 m, không phóng đại. <br>Thước hiện ở "decks" và tắt trước khi camera sang khung bản lề. Nhãn "Decks ≈ 0.66 m apart" chỉ vào thước, nằm phía trên khe. |
| **B03, B20:** đầu card gần như chỉ có nhãn góc trong 3,9 s và 6,4 s. | **B03:** ngay từ khung đầu đã có 46 ô nhà Schoonschip và ba lục giác OCEANIX vẽ nét mờ, cùng vạch chia giữa. Mỗi bên tô đầy khi lời nhắc tới ("households", "Busan"). <br>**B20:** mặt nước và đất của hai bờ có từ khung đầu. Tiêu đề, sóng và quận vẫn hiện theo lời. Audio không đổi. |
| **B32, B37** (rà cùng lúc). | **B32:** ba vòng tròn năng lượng, nước, thực phẩm vẽ mờ từ khung đầu, tô màu khi được nhắc. <br>**B37:** dòng "No reliable cost estimate…" hiện ngay đầu câu 2, thay vì ở chữ "reliable". Đo trên video: 2,8 s sau đầu shot, trước là 4,2 s. Trong 2,8 s đầu chỉ có nhãn góc "What would it cost?", đúng lúc lời dẫn hỏi câu đó. |
| **B22/B24/B30/B31:** nước ở khung ngang gần màu nền; lộ lưới bóng đáy khi camera hạ (9:23–9:25, 9:32–9:33). | **Nước trong muộn hơn:** bắt đầu 1,0 s sau khi camera bắt đầu hạ, xong ngay sau khi tới khung ngang (`CLEAR_AFTER`). Có test. <br>**Màu nước khi đã trong:** chuyển sang xanh sâu hơn (`see_through_color` #2A6E8E trong `stylized_materials.json`, đạt đủ ở độ trong 0,5). Nước đục giữ đúng màu cũ, nên mở đầu và mọi cảnh nước đục không đổi. <br>**Nhãn "Sea surface"** chỉ vào mặt biển ở B30 và B31. |
| **B31:** ba tuyến ống nhỏ, lẫn với dây neo. | Dây neo và neo mờ đi (0,85) khi ba tuyến sáng. Ba tuyến chuyển hẳn sang màu nhấn (tint 1,0). |
| **B12/B17:** lộ mép bãi nước. | Khung cuối B12 và khung của B17 nâng từ 20° lên 28°; mép bãi nước ra khỏi khung. Không đổi kích thước bãi nước hay độ sâu. |
| **B38 (11:43–11:49):** mạng nối nhạt khi kéo ra. | Nhà mờ tới 0,95 (trước là 0,85). Mạng nối (lối đi, cầu, tuyến, ống, đê) chuyển hẳn sang màu nhấn, thay vì phát sáng; phát sáng trên nền sáng làm mất tương phản. |
| **Watermark** (chủ kênh). | Đốt vào hình khi mã hóa khung, xem mục Watermark. |
| **`visual_variety`** | Ghi quyết định của chủ kênh, đúng phạm vi. Xem mục Ngoại lệ. |
| **Đính chính dung sai keyframe** | Xem mục Đính chính. |

**Đã thử nhưng bỏ:**
- **Nhìn khung ngang từ mặt khuất sáng (phương vị −10°):** nước chỉ xám hơn, không xanh hơn, và ba tuyến ống ở B31 chồng lên nhau thành một nét.
- **Màu nước khi trong tối hơn #2A6E8E:** với tone mapping AgX của dự án, nước ra màu xám khói.
- **Giảm độ trong của nước dưới 0,5:** không làm. Ở độ trong dưới 0,5, QA không còn coi vật dưới nước là nhìn thấy được, và quy tắc đó hợp lý.
- **Nhãn "Seawater" ở B34:** điểm neo nằm ở mép thân phao, nên nhãn trông như đang gọi tên thân phao. Đã bỏ.

## Watermark
- **File:** `branding/concepts_20261107/A_watermark_burnin_640.png`, bản xanh navy cho nền sáng (`watermarks_navy_revision.json`).
- **Kiểm file:** sha256 được ghi trong `config/branding.json`; file bị thay thì pipeline dừng.
- **Vị trí: góc dưới trái, rộng 14% khung, cách mép 4,5% (trái) và 4% (dưới), độ đậm 55%.** Ở 720p là 180 × 60 px tại (58, 631); ở 4K là 538 × 180 px.
- **Vì sao chọn góc dưới trái** (đo trên bản v1, 2 khung mỗi giây cho mỗi góc):
  - ba góc kia đã có chữ của phim: nhãn card và tiêu đề chương ở trên trái; ghi chú ở trên phải và dưới phải;
  - ô watermark nằm trong vùng phụ đề (17% dưới cùng, `annotation_style.json`), nơi chú thích không bao giờ vào. Pipeline từ chối mọi vị trí ra khỏi vùng này, nên watermark không thể che chữ của phim;
  - góc dưới phải là chỗ YouTube đặt watermark kênh và nút đăng ký ở màn hình kết thúc;
  - độ sáng nền dưới ô watermark trong phim là 118–218 (luma), nên navy 55% đọc được trên mọi nền. Chỉ trên vùng phố dày nhà (vài giây ở SC_001, SC_002, SC_038) chữ chìm hơn.
- **Cách đốt:** lúc mã hóa khung PNG (`tools/cli.py` `encode_sequence`), không vẽ trong Blender, nên cache render không đổi.
  - Áp cho bản chương, bản ghép và bản trích; ở preset BT.709 (4K), watermark được đặt trước bước đổi màu, trong cùng một chuỗi filter.
  - Chỉ áp cho dự án có `"watermark": true` trong `project.json`. Phim cầu và phim Gothic đã xong, nên giữ nguyên bản chương đã kiểm.
  - Dự án mới tạo bằng `episode.py new` có sẵn watermark (`production_defaults.json`).
- **QA:**
  - registry bản chương ghi thông số watermark; đổi watermark thì bản chương phải mã hóa lại;
  - QA chương kiểm watermark có thật trong file. Trong ô watermark, khung đầu của video phải gần với ảnh PNG đã chồng watermark (PSNR ≥ 30 dB) và cách xa ảnh PNG gốc ít nhất 6 dB;
  - báo cáo ghi những shot mà nền dưới watermark nhiều chi tiết.

## Ngoại lệ `visual_variety`
- **Ghi ở `project.json` → `variety_exception.runs`:**
  - SC_008–SC_014 (B08–B14, 7 × 3D_SEQUENCE);
  - SC_027–SC_031 (B27–B31, 5 × 3D_SEQUENCE).
  - Mỗi chuỗi ghi lý do. Phần `basis` chép nguyên câu hỏi và câu trả lời của chủ kênh. Thêm `DEC-VARIETY-B08-B14-B27-B31` trong `review/OWNER_APPROVALS.json`.
- **Validator (`pipeline/chapters.py`):**
  - Trước: `max_run` nâng ngưỡng cho cả phim (Codex đã chỉ ra), và trường `chapter` chỉ xuất hiện trong lời báo cáo.
  - Nay: chỉ miễn những chuỗi khớp đúng shot đầu, shot cuối, độ dài và loại hình. Chuỗi dài ra, ngắn lại hay đổi loại thì cần quyết định mới.
  - Hồ sơ dạng cũ (`chapter` + `max_run`) nay chỉ miễn chuỗi nằm trong chương đó.
  - Ngưỡng chung 4 không đổi. Có test.
- **Phát hiện ở phim Gothic (đã giao, không sửa):** với kiểm tra theo đúng phạm vi, phim Gothic có chuỗi 5 card sơ đồ SC_024–SC_028 (B24–B28) vượt ngưỡng 4 mà chưa được chủ kênh chấp nhận.
  - Ngoại lệ chủ kênh đã ghi chỉ cho chương 8 (SC_031–SC_038); chuỗi kia qua QA vì kiểu cũ nâng ngưỡng lên 8 cho cả phim.
  - Báo cáo `qa/longform_qa.json` đã lưu của phim đó vẫn ghi PASS. Tôi không sửa hồ sơ, không chạy lại báo cáo, không đổi file của phim đó.

## Đính chính: dung sai keyframe
Báo cáo v1 viết "không nới ngưỡng QA". Câu đó **không chính xác**: commit `ef13442` đã đổi cách tính dung sai khi so giá trị khóa Blender với kế hoạch. Ngưỡng hiển thị và các kiểm tra khác giữ nguyên. Chi tiết:
- **v1:** `max(1e-4, 4 × |giá trị| × 2⁻²³)`, mô tả là "4 ulp". Thực ra đó là 4–8 ulp tùy giá trị, ví dụ 7,29 ulp ở 933,27 (Codex chỉ ra). Test v1 cho phép tới 9 ulp, nên test PASS không chứng minh được mô tả "4 ulp".
- **Phép đo độc lập** (`tools/f32_key_error.py`, kết quả `docs/qa/f32_key_error_blender_5.2.2.json`):
  - đo trên Blender 5.2.2, với mọi kiểu easing engine dùng;
  - 400 cặp khóa ngẫu nhiên cho mỗi khoảng giá trị: 0,5–10; 10–100; 100–600; 600–2000; và đi qua 0 (±1500);
  - tổng 640.000 frame trung gian;
  - sai số lớn nhất **2,9 ulp** tính theo độ lớn của đoạn nội suy, max(|a|, |b|, |b − a|);
  - nếu chỉ tính theo hai khóa thì lên tới **4,8 ulp**, vì khi đi qua 0, độ thay đổi lớn hơn cả hai khóa.
- **v2:** dung sai = `max(1e-4, 4 ulp float32 thật của độ lớn đoạn nội suy)`, với ulp tính theo số mũ nhị phân (`motion.f32_ulp`). Ở 933,27 dung sai là 2,44·10⁻⁴, thay vì 4,45·10⁻⁴ ở v1.
- **Test:**
  - ulp khớp đúng khoảng cách float32;
  - sai số SC_038 thật (2,6 ulp) qua;
  - sai số 5 ulp bị bắt;
  - khi đi qua 0 thì tính theo độ thay đổi; khi giữ khóa thì tính theo chính khóa.
- **Báo cáo kiểm Blender** nay ghi thêm sai số lớn nhất bằng bao nhiêu phần trăm dung sai.
- Việc thêm `clearance` vào khóa nhóm camera (SC_042) giữ nguyên như v1.

## Kiểm tra trước render
- `plan-visuals`: 44/44, 784,17 s; `build-shots` PASS.
- Lời dẫn không đổi byte nào. `timing.json` chỉ đổi hai hash của storyboard và kế hoạch.
- `asset-check`: 28/28 spec đạt (cặp phao có thêm 3 MARKER).
- Kiểm Blender trước render, trên 14 shot đã sửa: 211/212. Lỗi duy nhất là B33: thân hộp chỉ thấy 5% khi phát sáng, vì nước còn đục. Đã sửa cho thân và sàn cùng sáng; chạy lại 20/20.
- Test (trừ các file gọi Blender): 466 PASS.
- Trước khi chốt, đã xem ảnh tĩnh mọi shot đã sửa ở các mốc làm sáng, và các khung chuyển ở B30, B31.

## Render
- **Phạm vi render theo báo cáo cache** (`qa/cache_report_internal_720p.json`, trước render): 44/44 shot cũ.
  - Cả 44 shot cũ vì file engine đổi (`arch/families/floating.py`, `motion.py`) và vì phần render của `project.json` đổi.
  - 14 shot còn đổi chính hình của shot.
  - Không có shot nào giữ được cache. Không ép số shot render lại.
- **Render 720p, mỗi lúc một Blender (2026-11-12, 07:20–10:14):**

| Chương | Shot | Frame | Thời gian render |
|---|---|---|---|
| C1 | 4 | 1 539 | 19:43 |
| C2 | 7 | 3 282 | 32:58 |
| C3 | 5 | 3 185 | 21:21 |
| C4 | 5 | 2 142 | 16:03 |
| C5 | 3 | 1 297 | 11:39 |
| C6 | 4 | 1 702 | 16:28 |
| C7 | 9 | 3 683 | 37:34 |
| C8 | 7 | 1 990 | 10:41 |

  Ghép bản đầy đủ mất 1:09; bản FULL_V2 có SFX và không SFX mất 5:39 (dùng lại khung PNG, không render Blender).

## File
- `output/pilot/floating_city_design_challenge_FULL_V2_INTERNAL_REVIEW_720p.mp4`: có SFX, 2 tiếng ở 2:26,5 và 2:44,4.
- `output/pilot/floating_city_design_challenge_FULL_V2_INTERNAL_REVIEW_720p_no_sfx.mp4`: chỉ lời dẫn.
- Phụ đề `.en.srt` đi kèm từng bản.
- `output/floating_city_design_challenge_INTERNAL_REVIEW_720p.mp4`: bản ghép chỉ lời dẫn, cùng hình.
- Bản FULL v1 (`..._FULL_INTERNAL_REVIEW_720p*.mp4`) vẫn để cạnh, để so.
- Tất cả 784,2 s (13:04,2), 18 820 frame, 1280×720, có watermark.

## QA sau render
- **Kiểm Blender trên toàn phim:** 586/586 (`qa/blender_checks.json`).
- **Media:**
  - 8 chương, mỗi chương 0 lỗi; −16,3 đến −16,5 LUFS;
  - bản ghép −16,4 LUFS, đỉnh thật −1,2 dBTP, 0 lỗi giải mã, 0 đoạn đen; 7 điểm nối giữa chương qua SSIM.
- **Watermark:** có mặt ở cả 8 chương và bản FULL_V2. PSNR trong ô là 34,9–43,1 dB so với ảnh có watermark, 16,0–22,1 dB so với ảnh gốc. Chỉ SC_031 có nền nhiều chi tiết dưới ô (đoạn ống chạy dọc đáy).
- **Bản trích FULL_V2** (`qa/excerpt_FULL_V2.json`): PASS.
  - Cả hai bản −16,4 LUFS; đỉnh thật −1,0 dBTP (có SFX) và −1,2 dBTP (không SFX).
  - Mức SFX không đổi so với v1: thấp hơn lời dẫn 14 dB, 0 mẫu bị cắt.
  - Whisper: 44/44 shot không kém đi khi có SFX; WER cao nhất 4,1%.
- **Phụ đề:** 181 cue, dòng dài nhất 42 ký tự, 1 cảnh báo tốc độ (cue 35, 17,1 ký tự/s, có từ v1).
- **QA phim dài** (`qa/longform_qa.json`): 17/17 PASS.
  - `visual_variety` PASS nhờ ngoại lệ đúng hai chuỗi; ngưỡng 4 giữ nguyên.
  - `render_cache_current` PASS (44 shot đúng khóa cache hiện tại).
  - `annotations_consistent` còn 2 mục UNCERTAIN để người duyệt xem: B31.s1 và B40.s0. Không có mâu thuẫn.
- **Gate** (`gates --preset internal_720p`):
  - G0–G6, GL, GV đều PASS ở hồ sơ `NARRATED_INTERNAL_REVIEW`;
  - hồ sơ này không đánh giá xuất bản. Bản này không phải bản FINAL và chưa được duyệt xuất bản.
- **Test:** 487 PASS, kể cả các file gọi Blender, không có test bị bỏ qua.
- **Các báo cáo sinh lại:** `EDITORIAL_APPROVAL_PACKAGE.md` có thêm hai nhãn mới "Sea surface" (B30, B31), cần chủ kênh xem cùng các chữ trên hình khác.

## Xem trong MP4
Xem từng mốc ở `qa/EDITORIAL_REVIEW_TIMECODED.md`. Tóm tắt:
- **Đạt:**
  - B13: cận khe, thước 0,66 m, nhãn không che khe;
  - B33/B34: mực nước rõ ở khung ngang;
  - B30/B31: không còn lưới bóng lúc chuyển; ba ống tách khỏi dây neo;
  - B12/B17: không lộ mép bãi;
  - B38: mạng nối đọc được;
  - đầu card: B03 0,5 s, B20 ngay khung đầu, B32 0,6 s (v1 là 4,0 / 6,5 / 2,5 s).
- **Còn tồn:**
  - nước khi trong vẫn xanh xám nhạt ở 6 shot khung ngang;
  - khoảng 1 s ở B33 (10:07,5–10:08,5): lúc camera hạ, nước đã bắt đầu trong, lộ hai mảng bóng phao dưới đáy và một góc mép bãi;
  - B37 có 2,8 s chỉ nhãn góc, trùng câu hỏi đang được đọc.

## Cần chủ kênh quyết
1. **SFX:** nghe hai bản FULL_V2 ở 2:26,5 và 2:44,4, chọn giữ hay bỏ. Mức không đổi so với v1.
2. **Nước ở khung ngang:** chấp nhận mức hiện tại, hay thử đổi nền phía sau sang màu ấm hơn (6 shot render lại).
3. **B33 khung chuyển 1 s và B37 2,8 s đầu:** sửa ở vòng sau, hay giữ.
4. **Phim Gothic:** chuỗi 5 card SC_024–SC_028 chưa có quyết định. Chủ kênh chấp nhận, hoặc giao việc sửa phim đó.
5. **Watermark:** xem ở góc dưới trái trong bản FULL_V2 (độ đậm 55%, rộng 14%), giữ hay chỉnh.
6. **Hai chữ mới "Sea surface"** (B30, B31) nằm trong gói duyệt chữ trên hình.

Agent không ghi một buổi nghe hay một lần duyệt nào cho các mục trên.
