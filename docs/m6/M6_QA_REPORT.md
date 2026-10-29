# M6: báo cáo QA

Nhánh `m6-narrated-documentary` (tách từ `35aa2c0`). Ngày 2026-10-29. Mọi kết quả dưới đây đều lấy từ lệnh đã chạy và file có thật. Mục nào chưa chạy thì ghi rõ là chưa chạy.

## 1. TTS và quyền
- Kokoro-82M `f3ff3571`: hash model, config và 4 giọng khớp với model card và VOICES.md. Hạng quyền `PENDING_REVIEW`; `check_purpose(kokoro, publication)` → RightsError.
- Thử giọng (`review/voice_audition/AUDITION.md`): `bf_emma` (B-, 182.5 wpm trên đoạn kỹ thuật), `bm_george` (C, 161.0), `bm_fable` (C, 180.3), `bm_daniel` (D, 185.1). Mặc định kỹ thuật theo số đo là `bf_emma`. **Người dùng đã chọn `bm_george` (2026-10-29)**, ghi ở `voice.selection`. Chọn giọng không phải cấp quyền: license vẫn `LICENSE_REVIEW_REQUIRED`, provider vẫn `PENDING_REVIEW`.
- Pilot (bản cuối, `bm_george`): 26 câu, tất cả `provider: kokoro`, `rights_class: PENDING_REVIEW`, model SHA256 ghi theo từng đoạn. ASR 26/26 PASS, WER tối đa 0.111: 'peers' cho piers, 'passed' cho pass, 'cord' cho chord. Tốc độ 143.4 wpm (321 từ / 134.32 s giọng nói).
- ASR chặn đúng hai chỗ, cả hai đã được viết lại; đây là sửa câu chữ trong bản nháp, không phải duyệt biên tập:
  - B7.s3 với `bf_emma`: "The truss shares it…" bị nghe thành "The trust…", nên đổi thành "In the truss, the load is shared…".
  - B1.s1 với `bm_george`: "press down" bị nghe thành "pressed" (WER 0.154 > 0.15, timing không khóa), "push down" bị nghe thành "pushed". Câu chốt: "Traffic, people and the weight of the bridge itself all press on its deck." (WER 0).
- Bản đầu dùng `bf_emma`: 160.8 wpm, 136.29 s. Toàn bộ pilot đã được sinh, lập kế hoạch và render lại bằng giọng người dùng chọn.

## 2. Nghiên cứu và bằng chứng
- 6 nguồn (ODOT MBI 2010, FHWA Covered Bridge Manual, FHWA PBES ch. 2 + App. E, SteelConstruction.info, Yale-NHTI). 14 claim `SOURCE_VERIFIED`, trích dẫn được đối chiếu nguyên văn. Không có claim nào là `EDITORIALLY_APPROVED`.
- Gói duyệt: `projects/bridge-load-explained/review/EDITORIAL_REVIEW_PACKAGE.md`. Ánh xạ từng câu: `qa/RESEARCH_VISUAL_MAP.md`.
- Không có nội lực, sức chịu tải, hệ số an toàn, ứng suất, độ võng hay so sánh định lượng nào. Có thẻ "Conceptual load path — not to scale" trên 6/6 shot có đồ họa lực.

## 3. Kế hoạch hình (offline)
- `plan-visuals` (bản `bm_george`): 11 shot, 151.33 s (3632 frame), 8/8 beat COVERED, `executable: true`. `validate-plan`: PASS (cả engine G0 trên bản sao).
- Chú thích: 27/27 PLACED trên 9 shot. Mũi tên tải/phản lực có cùng độ dài 0.085; LOAD hướng xuống, REACTION có thành phần hướng lên. Không chú thích nào vào vùng phụ đề, không chữ nào chồng chữ.
- Nhất quán lời/hình: 0 CONTRADICTION. 1 CONSISTENT (B7 "one at a time"). 1 UNCERTAIN (B8 "the arrows show ideas": chỉ chung về các mũi tên ở beat trước, người duyệt xác nhận).
- B7 cắt trên đầu câu: các shot vòm và giàn bắt đầu 0.2 s trước câu tương ứng. Glow B2 bắt đầu cùng câu "substructure", glow B3 cùng câu "beams".
- Sửa tầm nhìn: B3 GHOST:plank (theo `visual_repair_preference`). Hình học thì đúng, nhưng trên khung hình thấy rất ít, vì nhìn xuyên ván gỗ sẽ gặp mặt bên của dầm cùng màu (xem §7). B5 glow cả ba vành vòm; đường lực nén chỉ trên vòm giữa.

## 4. Blender
- `check-blender --preset review`: **176/176 PASS** (bản cuối), gồm cho 9 shot có chú thích:
  - `annotation_objects`;
  - `annotation_anchors`: mọi điểm neo chiếu đúng trong 0.004, và tia từ camera chạm chính bộ phận đích trước;
  - `annotation_layout`: bề rộng chữ thật vừa khung nền;
  - `annotation_timing`;
  - `captions_clear_of_subtitles` cho chú thích tiêu đề.
- Lỗi tìm được và đã sửa trong lúc làm:
  - điểm neo nằm ở mép silhouette, tia trượt sang vật phía sau, nên điểm neo phải nằm trong mép 2 bước;
  - QA bỏ qua chính đích đang bị làm mờ;
  - kiểm tra glow M5 lệch tiêu chí so với L1, nay đã thống nhất: share ≥ 0.25 hoặc mặt gọn ≥ 0.2 %;
  - chú thích hàng dưới cùng của cảnh tổng rơi vào vùng phụ đề, nay dải nhãn là 0.24.
- Smoke test SC_003 (cầu dầm, có lời + chú thích): **SMOKE PASS**, 440 frame, −16.1 LUFS, true peak −1.5 dBTP, 5 câu phụ đề.

## 5. Pilot đầy đủ (`preview --preset review` + `assemble`)
- Render review 960×540: 11 shot, 3271 frame, không có đoạn đen.
- Media QA lần đầu **FAIL** ở cắt match SC_001→SC_002: SSIM 0.976 < 0.98, vì chú thích B1 biến mất đúng ở chỗ cắt. Đã sửa: chú thích đang hiện ở cuối shot đứng trước một cắt match sẽ fade-out xong trước khung cắt. Chỉ SC_001 render lại; 10 shot dùng lại cache. Media QA lần hai **PASS**: SSIM ở cắt match 0.99999, các cắt cứng 0.72–0.81.
- Test Blender M6 tìm thêm một lỗi thật: ở cảnh tổng cuối (SC_011), với dải nhãn 0.24 bố cục chọn ROW, và chú thích ROW nằm ở giữa dải (đáy y = 0.098), tức trong vùng phụ đề. Kiểm tra `captions_clear_of_subtitles` trước đó chỉ chạy trên shot có chú thích, nay chạy trên mọi shot AUDIO_LOCKED. Đã sửa bằng `label_position: BAND_TOP` cho so sánh ROW ở dự án có lời dẫn; dự án không lời giữ cách cũ. Vì engine đổi nên **toàn bộ 3271 frame được render lại** bằng engine cuối. Media QA PASS, lắp ráp lại PASS, still 1080p render lại.
- **Bản cuối với giọng `bm_george`**: lập kế hoạch lại (11 shot, 3632 frame), QA Blender 176/176, render lại toàn bộ (median 0.71–1.13 s/frame, không đoạn đen), media QA PASS (cắt match SSIM 1.0), lắp ráp PASS, 11 still 1080p render lại, test Blender M6 PASS.
- `output/bridge_load_explained_pilot_INTERNAL_review.mp4`:
  - h264 960×540 24 fps; AAC 48 kHz mono; track phụ đề `mov_text` (eng);
  - 151.333 s; −16.0 LUFS, true peak −1.5 dBTP;
  - metadata `comment`: "INTERNAL PREVIEW - narration audio rights: PENDING_REVIEW - not for publication".
- SRT `…_INTERNAL_review.en.srt`: 35 câu phụ đề, 9 điểm ngắt căn theo từ đo được, dòng dài nhất 42 ký tự; không có lỗi, không có cảnh báo. Bản `bf_emma` từng có 3 câu trên 17 ký tự/s; giọng chậm hơn đã hết.
- Still 1080p (`still --preset production_test`): 11 ảnh 1920×1080 trong `output/stills_production_test/`.
- Gate (`gates --preset review`):
  - PASS: G0, G3 (3632 frame), G4 (QA Blender 176/176 + media QA), G5 (−16.0 LUFS, 35 câu phụ đề), GV;
  - chưa qua: G1 PENDING_EDITORIAL, G2 BLOCKED_RIGHTS, G6 BLOCKED;
  - trạng thái: **TECHNICALLY_VALIDATED · EDITORIAL_REVIEW_PENDING · TTS_RIGHTS_PENDING**; kết luận "INTERNAL PREVIEW — NOT PUBLICATION-READY".
- Kiểm tra MCP (`mcp-for-blender` 2.2.4, addon 1.8, safe mode, `127.0.0.1:9876`): một Blender GUI riêng chỉ mở **bản sao** SC_006/SC_007, đã đóng sau khi kiểm.
  - SC_006 có 47 object chú thích (5 chú thích, gồm thẻ), tất cả hiện ở frame 289 và không đổ bóng. Chú thích nằm ở độ sâu 0.44–0.47 từ camera, 52 bộ phận mô hình ở 12.0–31.5, nên không chạm hình học kiến trúc.
  - SC_007: mọi thanh giàn cùng một vật liệu ("Painted steel"), nghĩa là không có thanh nào tô màu kéo/nén; glow cùng màu trên 8 thanh giàn nam; "Joints" đã tắt đúng `until`.
  - `look` (mode camera, có `target`) xác nhận bố cục.
  - Safe mode từ chối `import os`.

## 6. Hồi quy
- Test: **249/249 OK**: 233 offline (`python3 -m unittest discover -s tests -p "test_[!b]*.py"`) + 16 Blender (`tests.test_blender_*`). M6 thêm 38 test offline (`tests/test_m6_narrated.py`), đủ các ca âm mà spec yêu cầu:
  - asset TTS chưa có quyền; claim thiếu nguồn; điểm neo không tồn tại;
  - nhãn ra ngoài khung; chú thích chồng phụ đề;
  - manifest timing không nhất quán; chuyển cảnh không khớp lời dẫn;
  - trạng thái publication-ready sai;
  - cùng lực trên bộ phận mà claim không nêu, mũi tên tải hướng lên, claim chưa được kể.
- Đánh giá planner: 29/29 ca (5 ca mới của M6).
- Dự án một họ giữ nguyên: bridge-story-m5 chỉ đổi 3 shot B7 (do câu chữ mới); roof-plan-m5 giống hệt (chỉ khác mã băm plan); `states.json` của cả ba dự án do planner sinh vẫn ở schema 2.
- Fixture đa họ `tests/fixtures/m6_cross_family`: validate PASS, QA Blender 69/69.
- QA Blender hồi quy, chạy với engine M6:

  | Dự án | QA Blender |
  |---|---|
  | bridge-story-m5 | 188/188 |
  | roof-plan-m5 | 52/52 |
  | suffolk-roofs | 71/71 |
  | roof-evolution | 64/64 |
  | bridge-structure-evolution | 92/92 |

  Số kiểm tra giống hệt M5.5.
- Preview của bridge-story-m5 render lại vì B7 đổi: media QA PASS, gate "TECHNICAL PREVIEW — VALID (silent); NOT FOR PUBLICATION". roof-plan-m5, roof-evolution và bridge-structure-evolution báo G4 media cũ sau khi khóa engine đổi; đã render lại cả ba (media QA PASS), gate về lại "TECHNICAL PREVIEW — VALID (silent); NOT FOR PUBLICATION".
- Suffolk-roofs không đổi trạng thái: `TECHNICALLY_VALIDATED` · `EDITORIAL_REVIEW_PENDING` · `TTS_RIGHTS_PENDING`.
- Test Blender M6 (`tests/test_blender_m6.py`, 4 test): PASS.

## 7. Giới hạn đã biết
1. **GHOST ván gỗ khó thấy** (B3): ván đã làm mờ 70 % nhưng phía sau là dầm cùng màu. Kiểm tra hình học (L1 và Blender) đều đạt; ý nghĩa do nhãn "Beams" đảm nhiệm. Một tông glow có màu, hoặc góc nhìn khác, là việc cho bước sau.
2. **Exploded view toàn mô hình có thể ra khỏi khung** khi nhóm camera chỉ dựng một mô hình nhỏ: fixture đa họ với mái thấp, khung tính lúc nghỉ, lớp phủ bay ra −0.145. QA Blender bắt được; fixture dùng HOLD_HIGHLIGHT. Lỗi có từ M5, M6 chưa sửa.
3. Góc nhìn ELEVATION để lộ nền trời xám của world (cảnh cận B4).
4. Luật nhất quán dựa trên cụm từ gợi ý: phát hiện được các mẫu đã liệt kê, không phải hiểu ngôn ngữ tự nhiên. Trái/phải luôn báo UNCERTAIN.
5. Chú thích chỉ gắn vào phần đứng yên. Điểm neo chưa đi theo bộ phận đang chuyển động; ví dụ B4 hiện nhãn trong đoạn giữ khi các viên đá tách ra.
6. Font: chưa xác minh file font cụ thể đứng sau `<builtin>` của Blender (mọi font Blender kèm theo đều OFL hoặc Bitstream Vera).

