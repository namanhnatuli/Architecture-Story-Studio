# Ghi chú cho buổi đọc kịch bản c-r2 (agent soạn)

**Kịch bản c-r2** (sau review c-r1 của chủ kênh, `review/REVIEW_C_R2.md`) **đã có:**
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

## Theo hướng bạn nêu ở review c-r1 (agent làm theo; không ghi là duyệt)
- **Thời lượng:** giữ gần hiện tại. Bản đo từ audio c-r2: **13:03** (783,5 s). Không cắt về 11 phút. Câu về ụ khô Schoonschip (B16) là chỗ cắt đầu tiên nếu sau này cần.
- **Ảnh Schoonschip:** tạm dùng sơ đồ tự vẽ có nhãn "schematic". Tìm cơ hội xin phép ảnh của đúng công trình. CC BY-SA không giải quyết được vì các ảnh đó chỉ chụp khu vực lân cận.

## Cần bạn quyết
1. **Phát âm "Schoonschip"** (B03, B07, B16, B26). Whisper nghe thành "Schoenskip/scoonskip"; ASR không chứng minh phát âm.
   - Lựa chọn: giữ cách đọc tiếng Anh hóa; thêm override sau khi bạn nghe; hoặc nhắc ít hơn.
2. **Giọng `am_michael` cho dự án này.** Duyệt của hai phim trước không tự áp sang.
3. **Duyệt claim** mà phim dùng, khi kịch bản đã chốt.
   - Sổ hiện có 64 claim `SOURCE_VERIFIED`: 9 phép tính, 5 giả định của Studio, 1 trạng thái "In Design" đọc từ trang kiến trúc sư (CLM_034).
4. **Chốt kịch bản c-r2.** Khi chốt, agent mới dựng họ asset `floating` và làm đoạn thử có lời dẫn cho chuỗi "thêm tải → chìm → sửa thân".

## Điều agent đã tự kiểm (không thay cho việc bạn đọc và nghe)
- Rà từng câu theo câu hỏi bắt buộc của playbook: lời có khẳng định vượt bằng chứng không? Các câu đã sửa ghi ở `review/REVIEW_C_R1.md`.
- **ASR:** Whisper nghe lại từng câu: 126/126 đạt (c-r2). Lời dẫn dùng chính tả Mỹ và viết số ≥ 100 bằng chữ số. "Schoonschip" vẫn bị nghe sai chính tả, đúng như dự đoán với một tên tiếng Hà Lan. ASR không chứng minh được cách phát âm.
- **Đoạn thử hình** "thêm tầng → phao chìm → thân sâu hơn" (prototype P6, mặt cắt, không lời): `renders/prototype/P6_add_storey_sink_fix_PROTOTYPE_INTERNAL_REVIEW.mp4`.
