# Vòng c-r2: sửa sau review c-r1 của chủ kênh (2026-11-08)

- **Đầu vào:** review c-r1. Kết luận của review: giữ cấu trúc, sửa ba điểm rồi chốt kịch bản; giữ khoảng 13 phút; rút phần kể quy trình nghiên cứu ở B03/B40; B15–B16 không thành hai bảng số; P6 dùng mặt cắt và đổi nhãn.
- **Trạng thái:** kịch bản c-r2 chờ chủ kênh chốt. Không có gì được duyệt.
- **Đọc:** `review/SCRIPT_REVIEW.md`, bản nghe thử `output/floating-city-design-challenge_narration_preview_c-r2.m4a` (ngoài git).

## Theo từng góp ý

| # | Góp ý | Đã làm |
|---|---|---|
| 1 | B23: "khoảng 3° mỗi chiều" thiếu điều kiện | Lời dẫn: *"including changes in loading, the slope of a 25-meter bridge changes by about 3 degrees either way."* Trên hình (mô tả shot): *"2 m water level + loading, assumed; shore hinge at mid-range"*. Mô hình in thêm phép tính chỉ với mực nước (±2,3°) bên cạnh phép tính có tải (±2,8°). CLM_109 nêu cả hai và giả định cao độ khớp. |
| 2 | CLM_054 còn "costs that rise faster than the depth" | Nay là *"with non-linear increases in material and installation cost"*, đúng lời nguồn. Lời dẫn giữ "higher costs". |
| 3 | B12 nhảy từ bản 4 tầng thân 4,5 m sang số người của bản 3 tầng | B12: *"Let's go back to the three-story version. A platform like this holds about 50 people."* Hình B12: tầng 4 và phần thân thêm mờ đi trước khi nhân phao. B16 và CLM_125: quận dùng phao 60 m với nhà 3 tầng. Mô hình in số người theo số tầng: phao 40 m có 48 người (3 tầng) hoặc 64 người (4 tầng); phao 60 m có 108 người (3 tầng). CLM_108 trích thêm dòng này. |
| — | B03/B40 nặng tính báo cáo | Trang BIG ghi **"Status In Design"** (đã kiểm trên bản tải về; danh mục trạng thái của BIG còn có "In Construction" và "Completed"). Thêm claim CLM_034. B03: *"…was unveiled in 2022, and when we checked in November 2026, its architects still listed it as in design."* B40: *"And the one project of that size we checked is still listed as in design."* Phạm vi kiểm tra để ở CLM_033/CLM_034 và ghi chú, không đọc thành tiếng. |
| — | B15–B16 thành hai bảng số | Một sơ đồ liên tục: ô phao 40 m hiện dần, mối nối sáng lên khi đếm (B15), rồi cùng sơ đồ đó gộp thành phao 100 m và về 60 m (B16). Câu về ụ khô giữ lại; nó là chỗ cắt đầu tiên nếu cần. |
| — | P6 chưa cho thấy vì sao thân sâu hơn lấy lại mạn khô; nhãn "same building load" dễ hiểu nhầm | P6 làm lại dạng mặt cắt, đường nước cố định. Vách được nối dài 0,5 m (tô vàng), đáy hạ xuống, sàn nâng lên. Nhãn mới: "same load per m² of floor". Còn lại: phần thêm vẫn nhỏ so với khung (`concept/PROTOTYPE_REPORT.md`). |
| — | Thời lượng; ảnh Schoonschip | Làm theo hướng bạn nêu: giữ gần 13 phút; tạm dùng sơ đồ và tìm cơ hội xin phép ảnh đúng công trình. Ghi ở `review/SCRIPT_REVIEW_NOTES.md` như hướng làm, không ghi là duyệt. |

## Kiểm tra
- **Sổ claim:** 16 nguồn, 64 claim, mọi trích dẫn khớp nguyên văn. CLM_033 không còn được lời dẫn dùng nhưng vẫn ở trong sổ.
- **Lời dẫn c-r2:** 44 beat, 126 câu. Năm lần sửa câu ghi ở `narration.template.json` → `revision.edits`.
- **Audio:** ASR 126/126; `lock-audio` 783,5 s, tức **13:03**.
- **Kế hoạch hình:** vẫn chưa thực thi được (thiếu asset và card), đúng như dự kiến ở giai đoạn này.
- **Storyboard sinh lại** từ timing (`concept/build_storyboard.py`).
- **Mô hình tính:** khớp các số trong review: ±2,3° và ±2,8°; 48, 64 và 108 người.
- **Test:** chạy lại bộ test của dự án và toàn bộ test (kết quả trong commit).

## Cần chủ kênh quyết
1. Phát âm "Schoonschip".
2. Giọng `am_michael` cho dự án.
3. Chốt kịch bản c-r2.
4. Duyệt claim mà phim dùng.
