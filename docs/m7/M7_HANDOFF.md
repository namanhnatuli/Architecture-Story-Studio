# M7: báo cáo bàn giao, "Why Bridges Don't All Look the Same"

> **Trạng thái kỹ thuật:** đã hoàn tất (`TECHNICALLY_VALIDATED`).
> **Mức sẵn sàng xuất bản:** CHƯA. INTERNAL REVIEW, vì còn chờ duyệt biên tập 41 claim, xác nhận giọng cho phim và xác nhận phát âm. G6 BLOCKED.

## 1. Nhánh và commit
Nhánh `m7-first-full-documentary`, tách từ `master` @ `f68c61a` (M6 đã duyệt). Commit M7: `b7e5b0a` (nội dung), commit tiếp theo chỉ ghi mã này vào bản bàn giao. **Không merge, không push.**

## 2. Độ dài thực tế
**646,458 s = 10,77 phút** (15.515 frame ở 24 fps). Nằm trong khoảng mục tiêu 10–12 phút.

## 3. Số chương
8 chương, mỗi chương 35–127 s:
- C1 Hook;
- C2 The problem every bridge must solve;
- C3 The beam;
- C4 The arch;
- C5 The truss;
- C6 Why different designs exist;
- C7 Real-world decisions;
- C8 Why they look different.

## 4. Số beat
39 beat lời dẫn, 103 câu, 1320 từ.

## 5. Số shot
47 shot.

## 6. Các loại hình đã dùng
Tính theo thời lượng:
- 3D giữ cảnh, có chú thích dựng dần: 33%;
- sơ đồ tự vẽ (ván khuôn, đánh đổi, thung lũng/cầu cạn, thanh nhịp đúng tỉ lệ, dòng thời gian, sơ đồ Đông/Tây): 24%;
- ảnh lưu trữ HAER: 15%;
- push-in: 11%;
- tách lớp: 6%;
- card tiêu đề: 4%;
- ba mô hình cạnh nhau: 4%;
- thay bộ phận (Pratt → Warren, lắp vào khoảng trống): 3%.

Chi tiết: `projects/why-bridges-look-different/qa/VISUAL_VARIETY.md`.

## 7. Tình trạng bằng chứng
- 12 nguồn, 42 claim, tất cả `SOURCE_VERIFIED` (khớp nguyên văn); lời dẫn dùng 41 claim.
- **0 claim được duyệt biên tập.** Agent không tự duyệt.
- Không có beat fact nào thiếu claim, ở bất kỳ chương nào.
- Các điểm không chắc chắn đã xử lý: năm xây cầu Bollman không nói; "still in service" gán cho báo cáo 2005; "America's greatest stone arch" gán cho báo cáo.
- Tài liệu: `research/RESEARCH_REPORT.md`, `review/EVIDENCE_MATRIX.md`, `review/EDITORIAL_APPROVAL_PACKAGE.md`.

## 8. Quyền giọng và tài sản
- **Giọng:** Kokoro-82M @ `f3ff3571`, `bm_george`, hạng quyền `PUBLICATION_CLEARED` (chủ kênh cấp ở mức provider ngày 2026-10-29). Việc áp dụng cho phim này **chờ chủ kênh xác nhận**, nên G2 = BLOCKED_RIGHTS.
- **Ảnh:** 4 ảnh HAER/Library of Congress, PD-USGov-NPS, có hồ sơ đầy đủ và SHA256; chỉ cắt viền phim. Có ghi công trên card và trong bản nháp mô tả.
- **Khác:** mô hình 3D và sơ đồ do dự án tự tạo. Không có nhạc. Không có ảnh có watermark.
- Tài liệu: `review/RIGHTS_PROVENANCE.md`.

## 9. Kết quả khóa audio
- 103/103 câu qua ASR (WER ≤ 0,15). Speech đo được là 599 s; cửa sổ beat khóa ở 645,83 s; phim 646,46 s.
- Sửa câu theo bằng chứng đo được: 8 lần, ghi trong `revision.edits`. Gồm 6 lần viết lại câu do ASR hoặc tốc độ đọc, 1 lần tách câu, 1 lần thêm câu.

## 10. Render và QA Blender
- QA Blender **577/577**.
- Soi MCP mỗi chương một frame, trên bản sao `.blend`.
- Hồi quy trên dự án cũ: 5/6 dự án đạt hết. `suffolk-roofs` 71/72: kiểm tra mới chỉ ra một lỗi bố cục có từ M3 (xem `docs/m7/M7_QA_REPORT.md`).

## 11. Phát hiện về chất lượng biên tập
- Từ rough cut, tìm thấy 8 lỗi và đã sửa hết: NOTE trôi trong push-in, viền phim trên ảnh, cảnh kết thiếu nhãn, card ghi công quá ngắn. Sau đó sửa thêm cụm chú thích B16.
- Còn để ngỏ: sơ đồ Đông/Tây đơn giản; ảnh Bollman 27,5 s; khu vực xà mũ ở SC_013 hơi dày.
- Tài liệu: `projects/why-bridges-look-different/qa/EDITORIAL_REVIEW_TIMECODED.md` (có 10 câu hỏi trải nghiệm người xem).

## 12. Phụ đề
145 câu cho 103 câu lời dẫn: tối đa 42 ký tự/dòng, tối đa 19,3 ký tự/s, mốc lấy từ khoảng câu đã đo, 0 câu phải lùi về mốc theo cả câu. Có SRT và track mov_text. Mỗi chương có SRT riêng.

## 13. Kết quả media cuối
Bản review: h264 960×540 24 fps, AAC 48 kHz, −16,0 LUFS, true peak −1,5 dBTP, A/V lệch ≤ 1 frame, 0 lỗi giải mã, 0 đoạn đen. Mọi match cut có SSIM ≥ 0,98.

## 14. Thời gian render và bộ nhớ
Đo khi máy thức:
- 0,548 s/frame ở 640×360 và 0,593 s/frame ở 960×540, tức khoảng 2,3–2,5 giờ cho cả phim. Wall-clock là 8,1 giờ và 4,6 giờ vì máy ngủ 29 và 11 lần.
- Bộ nhớ: CLI ≤ 0,59 GB RSS; still 1080p 0,83 GB.

Chi tiết: `docs/m7/PERFORMANCE.md`.

## 15. Hiệu quả của cache
- Sửa B16 chỉ làm cũ 1/47 shot. 8 MP4 chương dựng hoàn toàn từ frame CACHED.
- ASR dùng lại 101/102 đoạn audio; narrate chỉ sinh câu mới.
- Hồ sơ quyền, chương và trạng thái claim không làm cũ frame.

## 16. Giới hạn còn lại
- Chưa có video 1080p. Preset `final` bị G6 chặn; chỉ có 47 still 1080p.
- Không có bản khắc phụ đề vào hình, vì FFmpeg không có libass/freetype.
- Sơ đồ Đông/Tây chỉ là khung sơ lược.
- Bản dựng mất nhiều thời gian chủ yếu vì máy ngủ.
- Khôi phục render bị ngắt mới được kiểm bằng test, chưa xảy ra trong lượt render thật.
- Ghi chú chân trang ở `suffolk-roofs` SC_004 nằm ngoài vùng an toàn.
- ASR không kiểm được cách đọc tên riêng.

## 17. Vị trí file đầu ra
Thư mục `projects/why-bridges-look-different/output/` (không commit):
- `why_bridges_look_different_documentary_INTERNAL_REVIEW_review.mp4` + `.en.srt` (bản review 960×540);
- `why_bridges_look_different_documentary_INTERNAL_REVIEW.mp4` (rough cut 640×360);
- `chapters_review/…_C1…C8_documentary_INTERNAL_REVIEW.mp4` + `.en.srt` + `_narration.wav`;
- `…_narration_master_clean_review.wav`, `…_audio_master_review.wav`;
- `stills_production_test/*.png` (47 still 1080p);
- file nghe thử giọng: `review/voice_audition_us/`.

## 18. Lệnh tái tạo
Xem `docs/m7/REPRODUCIBILITY.md`: môi trường, lệnh đầy đủ, vị trí cache, kế hoạch kiểm tra build sạch.

## 19. Cần người duyệt
1. Duyệt 41 claim. Gói duyệt có kèm 2 dòng nhất quán lời/hình UNCERTAIN cần xác nhận. Sau đó đặt `factual_review: verified`.
2. Xác nhận quyền giọng cho phim (`owner_confirmation_for_this_film`), hoặc chọn một giọng Anh–Mỹ. Đổi giọng thì phải render lại toàn phim.
3. Nghe phát âm 16 thuật ngữ và tên riêng (`review/PRONUNCIATION_REVIEW.md`), nhất là Bollman, Corinne, Gwynns Falls.
4. Quyết định dòng ghi công "Narration: AI-generated voice (…)" trên card B35.
5. Chuyển profile `PUBLICATION_CANDIDATE` + `publication_metadata`, rồi render 1080p với preset `final`.
6. Có sửa `suffolk-roofs` SC_004 hay không.
7. Merge hay không.

## 20. Đề xuất cho phim tiếp theo
- **Dùng lại frame tĩnh:** card và cảnh giữ chiếm phần lớn frame nhưng phần lớn giống hệt nhau. Chỉ render các frame có thay đổi sẽ rút ngắn đáng kể thời gian render; đây là ước đoán, chưa đo.
- **Giữ máy thức khi render dài** (`caffeinate -dims` khi cắm sạc), hoặc render theo chương qua đêm.
- **Duyệt claim theo từng chương** ngay sau checkpoint B, để tránh dồn duyệt vào cuối.
- **Chọn giọng trước khi khóa audio.** Đổi giọng sau khi khóa thì phải render lại toàn bộ.
- **Bản đồ có giấy phép** (ví dụ dữ liệu Natural Earth, phạm vi công cộng) cho các chương địa lý.
- Thêm preset video 1080p INTERNAL REVIEW tách khỏi `final`, nếu muốn xem 1080p trước khi duyệt.
