# Vòng c-r1: sửa sau review concept của chủ kênh (2026-11-08)

- **Đầu vào:** review concept của chủ kênh. Kết luận của review: hướng phim tốt, nhưng chưa khóa kịch bản và chưa dựng; sửa sáu nhóm vấn đề, viết lời dẫn hoàn chỉnh, rồi làm đoạn thử "thêm tải → phao chìm → sửa thân".
- **Trạng thái:** kịch bản c-r1 đã có lời dẫn hoàn chỉnh và audio nội bộ, **chờ chủ kênh đọc và nghe**. Không có gì được duyệt.
- **Bắt đầu đọc:** `review/SCRIPT_REVIEW.md`, gồm đúng các câu đã đọc, mốc thời gian, claim và các quyết định cần chủ kênh.

## Theo từng góp ý

| # | Góp ý | Đã làm |
|---|---|---|
| 1 | "Stiff means it follows the water" suy quá từ GM | Bỏ câu đó. B11 nay nói phao nghiêng rất ít dưới tải dời chỗ minh họa này, nhưng điều đó nói rất ít về cách nó chuyển động trong sóng. CLM_007 ghi "not planned for narration" kèm lý do. `ENGINEERING_RESEARCH.md` §3 đã sửa. |
| 2 | Chênh 66 cm không chứng minh nối cứng sẽ hỏng | B13 nói rõ: hai phao **nổi độc lập**; tải khác nhau thêm một yêu cầu cho mối nối; thiết kế này chọn cầu có khớp; dằn là cách khác. Claim CLM_107 ghi giới hạn của phép tính. Hình không tô đỏ phương án nào. |
| 3 | Ra khơi không đồng nghĩa tự cung tự cấp | Tách thành hai câu hỏi. B31: cáp, ống và tàu vẫn tới được, nhưng mọi liên kết dài và lộ hơn. B32: *nếu* chọn thêm điều kiện tự chủ (như concept 2026) thì cần thêm hệ năng lượng, nước, lương thực. |
| 4 | SH09–SH10 đổi trường hợp giữa chừng; cỡ phao cuối không thống nhất | Mô hình có `storey_branch`, một nhánh với cùng tải tĩnh 0,6 t/m²: mạn khô 1,042 → 0,710 → 1,146 m, thêm 105,6 t (4,0%). Khớp đúng bảng trong review. Quận chốt phao 60 m (93 phao, khoảng 108 người mỗi phao, tới 180 mối nối); mọi tổng của quận tính theo cỡ đó. |
| 5a | "No peer-reviewed cost basis" quá tuyệt đối | Thêm CLM_063 (khung chi phí sơ bộ của Ruzzo, chỉ cho phần nổi và năng lượng). B37: *"We do not yet have a reliable cost estimate for this design."* |
| 5b | CLM_033 bị mở rộng thành kết luận toàn cầu | B03 và B40 chỉ nói về dự án đã kiểm (OCEANIX Busan), nêu nơi kiểm (trang tin OCEANIX, trang dự án BIG) và tháng kiểm, và nói rõ *"We didn't survey every project in the world."* CLM_033 thêm bằng chứng từ trang BIG và ghi phạm vi. |
| 6 | Số minh họa chưa đủ chứng minh thành phố vận hành được | 40 m² sàn mỗi người = 30 nhà ở + 10 trường học, phòng khám, cửa hàng, dịch vụ (CLM_124). Khoảng 1 triệu tấn chỉ là 93 phao tiêu chuẩn; kèm danh sách những gì không tính. Độ dày thân phao ghi là giả định khối lượng. Câu kết B42: phép tính cho thấy yêu cầu nổi cơ bản; quận có vận hành được hay không còn phụ thuộc địa điểm và mọi hệ khác. |
| — | Mở phim "Not a render" | B02 nay là lời mời giải bài toán thiết kế. |
| — | C2 quá dày | Còn ba ý (nổi bằng cách nào → thêm tải → nổi chưa đủ). Không có G, B, M. |
| — | C7 có bốn card liền nhau | Ra khơi (B29–B31) và thân bán chìm (B33) thành 3D; neo đổi theo độ sâu kể bằng cảnh dưới nước. |
| — | Thêm ảnh thật Schoonschip | Đã tìm trên Commons qua API: không có ảnh PD, CC0 hay CC BY của Schoonschip; ảnh khu vực đều là CC BY-SA. **Cần chủ kênh quyết** (mục dưới). Tạm dùng sơ đồ có nhãn. |
| — | P5 khó đọc | Dây neo và neo đậm hơn, dày hơn; nước làm mờ trong hơn (`concept/PROTOTYPE_REPORT.md`). |
| — | Đoạn thử "thêm tải → chìm → sửa thân" | Prototype P6: hoạt ảnh 12 giây, không lời, số lấy từ `storey_branch`. Đoạn thử có lời dẫn trên asset thật phải chờ kịch bản được duyệt (AGENTS.md: không dựng asset mới trước khi kịch bản được duyệt). |

## Lỗi agent tự tìm thấy khi rà lại (ngoài review)
- **Claim CLM_056 đã gán nhầm mục đích.** Trong Ruzzo, "tránh va chạm và quá tải mối nối" là việc của chân vịt dự phòng; khoảng cách giữa module là để tránh va chạm vì neo mềm cho phép dịch ngang lớn. Đã sửa claim và câu B14.
- **Rà lại các câu khác so với nguồn:**
  - "Each Schoonschip house": nguồn nói "practically all" floats, nên đổi thành "The Schoonschip houses stand on concrete floats";
  - "usually fixed": nguồn chỉ nói "are fixed", đã bỏ "usually";
  - "the cost rises faster than the depth": nguồn nói "nonlinear", nay là "higher costs";
  - "constant maintenance" đổi thành "ongoing";
  - câu sinh thái giữ "effects that researchers say still need study";
  - câu rung lắc tách câu chung (Hà Lan) khỏi câu của một cư dân Amsterdam.
- **Ba câu quá ngắn bị kiểm tra tốc độ đọc từ chối.** Đã gộp với câu bên cạnh; không nới ngưỡng (`narration.template.json` → `revision.edits`).

## Kiểm tra
- **Sổ claim:** 16 nguồn (14 ngoài, 2 của Studio), 63 claim, mọi trích dẫn khớp nguyên văn (`research/build_sources.py`). Phân loại:
  - 39 ESTABLISHED_FACT;
  - 9 SPECULATIVE_PROPOSAL;
  - 1 UNVERIFIED;
  - 9 CALCULATED_ESTIMATE (chỉ dẫn `analysis/RESULTS.md`);
  - 5 DESIGN_ASSUMPTION (chỉ dẫn `concept/SCENARIO_CONTRACT.md`).
  - Test giữ ranh giới này.
- **Lời dẫn:** 8 chương, 44 beat, 127 câu. `pipeline/narration.validate`: 0 lỗi. `episode.py status`: SCRIPT DONE, kể cả lời kêu gọi cuối.
- **Audio:**
  - Kokoro `am_michael`, 732 s lời đọc.
  - ASR: 127/127 câu đạt. "Schoonschip" bị Whisper viết thành "Schoenskip" và "scoonskip"; ASR không chứng minh phát âm.
  - `lock-audio`: 44 beat, 784,9 s, tức **13:05**.
- **Kế hoạch hình:** 29 MISSING_ASSET (chưa có họ asset nổi) và 15 MISSING_TEMPLATE (card chưa vẽ). Đúng như dự kiến ở giai đoạn đọc kịch bản. Planner cảnh báo bốn chỗ ý đồ beat có thể đặt khác (B23, B35, B37, B42); chưa đổi.
- **Storyboard sinh lại từ timing thật:**
  - 44 shot, 3D 64%;
  - chuỗi card dài nhất 3 (B39–B41);
  - hạng khả thi: 17 REUSE, 18 GENERATE_PROCEDURAL, 7 CREATE_SMALL_NEW_CAPABILITY, 2 ADAPT.
- **Mô hình tính:** `storey_branch` khớp đúng bảng trong review (1,042 / 0,710 / 1,146 m). Test 7/7.
- **Prototype:**
  - P5 sửa xong;
  - P6 là hoạt ảnh 12 s (288 khung, 960 × 540), số theo `storey_branch`; đọc được qua thước và nhãn. Phần thân thêm 0,5 m còn mờ; bản sản xuất dùng mặt cắt.

## Cần chủ kênh quyết
Năm mục ở `review/SCRIPT_REVIEW_NOTES.md` (đứng đầu `review/SCRIPT_REVIEW.md`):
1. Thời lượng 13:05: giữ hay cắt về khoảng 11 phút.
2. Phát âm "Schoonschip".
3. Ảnh Schoonschip: CC BY-SA, xin phép, hay sơ đồ.
4. Giọng `am_michael` cho dự án này.
5. Duyệt claim khi kịch bản đã chốt.
