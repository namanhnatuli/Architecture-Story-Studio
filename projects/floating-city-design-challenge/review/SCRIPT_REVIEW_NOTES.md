# Ghi chú cho buổi đọc kịch bản c-r1 (agent soạn)

**Kịch bản c-r1 đã có:**
- lời dẫn hoàn chỉnh, sau review concept 2026-11-08 (sáu nhóm sửa, xem `review/REVIEW_C_R1.md`);
- audio nội bộ bằng Kokoro `am_michael`;
- timing đo từ audio.

**Chưa có:** asset, card hay hình nào. Kế hoạch hình báo `NEW_ASSET_REQUIRED` cho các beat 3D; đó là kết quả đúng ở giai đoạn này. Không có gì được duyệt. Bản nghe thử nằm ở `output/` (ngoài git) và không phải bản master.

## Cách đọc
- Mỗi câu dưới đây là câu đã được đọc thành tiếng.
- Cột claim chỉ ra câu dựa vào đâu:
  - nguồn ngoài (CLM_0xx);
  - phép tính minh họa của Studio (CLM_101–109, `analysis/RESULTS.md`);
  - giả định của kịch bản (CLM_121–125, `concept/SCENARIO_CONTRACT.md`).
- Mọi con số tính ra đều được nói là minh họa ("in this illustrative design", "about").

## Cần bạn quyết

1. **Thời lượng.** Bản đo từ audio dài **13:05** (784,9 s, gồm khoảng lặng của mỗi beat; chưa có thời gian cho hình), dài hơn mục tiêu 10–12 phút nhưng vẫn trong khoảng chấp nhận 8–15 phút. Nếu muốn về khoảng 11 phút, các chỗ cắt ít hại nhất là:
   - B16: câu về ụ khô Schoonschip;
   - B14: câu thứ hai (research agenda); B13 đã nêu yêu cầu cho mối nối;
   - B35 và B36: gộp thành một câu về sinh thái và một câu về quyền dùng mặt nước;
   - B37: phần so với đất liền còn một câu;
   - B27: câu thứ hai (cáp và bơm chống nước).

   Agent không tự cắt.
2. **Phát âm "Schoonschip".**
   - Whisper nghe Kokoro đọc thành "Schoenskip" và "scoonskip".
   - Tiếng Hà Lan đọc khác (âm "sch" và "g" họng). Chưa có override nào, vì một override cần nguồn phát âm và một buổi nghe của bạn.
   - Lựa chọn: giữ cách đọc tiếng Anh hóa hiện tại; thêm override sau khi bạn nghe; hoặc giảm số lần nhắc tên (hiện có ở B03, B07, B16, B26).
3. **Ảnh Schoonschip.**
   - Commons không có ảnh PD, CC0 hay CC BY nào của khu này. Ảnh khu vực gần đó đều là CC BY-SA.
   - Lựa chọn: (a) cho phép dùng CC BY-SA (quyết định ShareAlike của kênh); (b) xin phép Schoonschip hoặc Space&Matter; (c) giữ sơ đồ tự vẽ có nhãn "schematic".
4. **Đơn vị và chính tả.**
   - Lời dẫn dùng hệ mét, chính tả Mỹ (meters, tons, story) và chữ số cho số ≥ 100, như hai phim trước.
   - "Tons" ở đây là tấn mét. B07 nói rõ "metric tons" ở lần đầu.
5. **Giọng `am_michael` cho dự án này.** Duyệt của hai phim trước không tự áp sang.
6. **Claim:** 63 claim `SOURCE_VERIFIED` (gồm 9 phép tính và 5 giả định của Studio). Bạn duyệt claim mà phim dùng, khi kịch bản đã chốt.

## Điều agent đã tự kiểm (không thay cho việc bạn đọc và nghe)
- Rà từng câu theo câu hỏi bắt buộc của playbook: lời có khẳng định vượt bằng chứng không? Các câu đã sửa ghi ở `review/REVIEW_C_R1.md`.
- **ASR:** Whisper nghe lại từng câu: 127/127 đạt, sau khi đổi sang chính tả Mỹ và viết số ≥ 100 bằng chữ số. "Schoonschip" vẫn bị nghe sai chính tả, đúng như dự đoán với một tên tiếng Hà Lan. ASR không chứng minh được cách phát âm.
- **Đoạn thử hình** "thêm tầng → phao chìm → thân sâu hơn" (prototype P6, không lời): `renders/prototype/P6_add_storey_sink_fix_PROTOTYPE_INTERNAL_REVIEW.mp4`.
