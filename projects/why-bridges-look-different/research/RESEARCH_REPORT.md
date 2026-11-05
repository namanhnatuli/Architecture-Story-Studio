# Báo cáo nghiên cứu: "Why Bridges Don't All Look the Same" (M7)

- Ngày: 2026-10-29/30. Người làm: agent. **Chưa có claim nào được duyệt biên tập**: trạng thái cao nhất là `SOURCE_VERIFIED`.
- Bằng chứng máy đọc được nằm trong `research/sources.json` (12 nguồn, 42 claim). File này được sinh lại bằng `research/build_sources.py`, kết quả giống hệt từng byte. Ma trận claim → câu → hình: `review/EVIDENCE_MATRIX.md`.

## 1. Câu hỏi của phim
Vì sao các cây cầu không giống nhau? Phim muốn trả lời bằng hai lớp:
1. **Cách kết cấu chịu tải:** dầm chống uốn; vòm làm việc chủ yếu ở trạng thái nén; giàn gồm các thanh chịu kéo hoặc nén dọc trục.
2. **Hoàn cảnh xây dựng:** vật liệu, địa hình, nhịp, chi phí, tay nghề và thời đại. Phim minh họa bằng ba cây cầu Mỹ thế kỷ 19 có hồ sơ HAER.

Phim không kể theo hướng "tiến bộ tuyến tính" và không xếp hạng kiểu cầu nào tốt hơn.

## 2. Cách làm
- Mọi trích dẫn được **khớp nguyên văn** với văn bản nguồn tải về: PDF NCHRP qua `pdftotext -layout`, HTML ASCE và Yale. Khi khớp, khoảng trắng và kiểu dấu nháy được chuẩn hóa, còn câu chữ thì giữ nguyên chữ của nguồn. SHA256 và cách trích văn bản ghi ở `research/source_snapshots.json`. Bản tải về không được commit.
- Vị trí trích: báo cáo NCHRP dùng số trang in (ví dụ "3.2.1 Stone Arch, p. 3-48"). Trích từ danh mục hình thì ghi số hình, không ghi trang.
- Các claim CLM_701–714 là 14 claim M6 (đã đối chiếu ngày 2026-10-28) được giữ nguyên câu chữ và bằng chứng, chỉ đổi id. Việc chủ kênh duyệt chúng cho pilot M6 **không** được chuyển sang M7.

## 3. Nguồn
| Nguồn | Vì sao chọn |
|---|---|
| TRB/NCHRP 25-25(15) *A Context for Common Historic Bridge Types* (2005) | Nghiên cứu bối cảnh quốc gia do AASHTO/FHWA tài trợ. Nguồn chính cho lịch sử, vật liệu, chi phí, nhịp và các ví dụ có hồ sơ |
| ODOT *Manual of Bridge Inspection*; FHWA Covered Bridge Manual; FHWA PBES (glossary, ch. 2) | Định nghĩa tải trọng, kết cấu phần trên/phần dưới, mố, trụ, xà mũ (từ M6) |
| SteelConstruction.info "Trusses" | Giàn: lực dọc trục, biên trên nén, biên dưới kéo (từ M6) |
| Yale-New Haven Teachers Institute 01.05.08 | Vòm cần vật liệu chịu nén tốt; phản lực của mố (từ M6 + mới) |
| ASCE, *Bollman Truss Bridge* (công trình lịch sử) | Bằng sáng chế 1852, dùng sắt cho mọi bộ phận chính, ví dụ duy nhất còn lại |
| HAER MD-9, UT-64, MD-1, VA (Library of Congress) | Ảnh và tiêu đề hồ sơ của bốn công trình |

## 4. Kết quả theo chủ đề
- **Dầm:** kiểu rất cổ (CLM_720). Đơn giản, gỗ sẵn có nên vẫn được xây đến nay trên đường nông thôn và trong công viên (CLM_721). Cầu gỗ thời đầu thường có nhịp ngắn (CLM_722).
- **Vòm:** ván khuôn tạm do thợ mộc dựng, thợ đá xây (CLM_723). Đắt hơn cầu gỗ nhưng được chọn cho tuyến đông và nơi quan trọng; ở chỗ khác, giá rẻ của gỗ bù cho việc kém bền (CLM_724, CLM_725). Cần vật liệu chịu nén tốt (CLM_726). Suy giảm khi giàn kim loại phổ biến, thợ đá ít đi và bê tông cốt thép xuất hiện, rồi hồi phục ngắn trong thời Đại khủng hoảng (CLM_738).
- **Giàn:** Pratt 1844 (đứng gỗ, chéo sắt), Warren 1848 (chéo xen kẽ) (CLM_727, CLM_728). Cấu kiện chế tạo sẵn trong xưởng; tới 1860 đường sắt gần như chỉ dùng loại này (CLM_729). Giàn thông qua có nhịp gần 400 ft; giàn king post đơn giản khoảng 30 ft (CLM_730, CLM_731). Gỗ dễ mục, nên nhiều cầu giàn gỗ có mái che (CLM_733, CLM_734). Sắt rèn "strong equally in tension and in compression" (Plowden, NCHRP trích lại, CLM_735).
- **Địa hình:** cầu cạn và cầu khung giữ tuyến gần như thẳng và bằng ở thung lũng quá sâu để đắp nền, vì đầu máy có độ bám hạn chế (CLM_736). Định nghĩa trestle (Waddell, CLM_737).
- **Ví dụ:**
  - Carrollton Viaduct: 1829, khoảng 12.000 khối granit, vòm 80 ft. Là cầu vòm đá đường sắt sớm nhất ở Mỹ, và tính tới 2005 là nhịp đá đường sắt còn khai thác lâu đời nhất (CLM_739, CLM_740).
  - Trestle 790B: 1872, Central Pacific (CLM_743).
  - Bollman: bằng sáng chế 1852, ví dụ duy nhất còn lại (CLM_744, CLM_745).
  - Humpback Covered Bridge: 1857 (CLM_746).
  - Đông/Tây: phía Đông xây cầu cạn đá đồ sộ; phía Tây dùng gỗ vì cần làm nhanh, rẻ, gỗ nhiều (CLM_741, CLM_742).

## 5. Điều không chắc chắn và cách xử lý
- **Năm xây cầu Bollman ở Savage:** các nguồn không thống nhất. Phim chỉ nói năm cấp bằng sáng chế 1852.
- **"Still in service":** đúng tại thời điểm báo cáo 2005. Lời dẫn gán rõ cho báo cáo đó.
- **"America's greatest stone arch":** là đánh giá của báo cáo NCHRP. Lời dẫn nói "What one report calls…".
- **Địa danh trong chú thích ảnh** lấy từ tiêu đề hồ sơ HAER/LOC của chính bức ảnh, không thuộc claim nào.
- loc.gov trả HTTP 403 cho truy cập tự động. Siêu dữ liệu ảnh (giấy phép, tác giả, mã LOC) lấy từ trang file Wikimedia Commons, có liên kết nguồn HABS/HAER.

## 6. Claim bị loại hoặc không dùng
- "Mặt trên dầm nén, mặt dưới kéo" và "đá chịu kéo kém": **không tìm được nguồn đủ chặt trong bộ nguồn**, nên không đưa vào phim. Phim chỉ nói dầm chịu tải bằng cách chống uốn.
- Màu nén/kéo cho từng thanh bụng: CLM_714 chỉ nói "một số thanh nén, một số kéo", không có trường hợp tải nào được ghi lại. Vì vậy các thanh bụng **không** được tô màu. Chỉ biên trên/biên dưới của giàn nhịp giản đơn dưới tải hướng xuống được ghi nén/kéo (CLM_713).
- CLM_747 (đá địa phương; Kansas và Michigan) đã kiểm nhưng không dùng trong lời dẫn, để phim không quá dài.
- Cầu Cornish–Windsor: ảnh có nguồn là người tải lên Commons ("Daderot"), không phải hồ sơ liên bang, nên bị loại.
- Không có con số nào về sức chịu tải, ứng suất, nội lực, độ võng, hệ số an toàn hay xếp hạng độ bền.
