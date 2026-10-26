# Brief nghiên cứu pilot M3 — "Why Do Roof Pitches Vary?" (BẢN NHÁP)

Trạng thái: **bản nháp, G1 chưa đạt.** Mọi claim bên dưới đều là `provisional`: nguồn đã được AI đọc và các trích dẫn được chép nguyên văn ngày 2026-10-26, nhưng người duyệt phải kiểm tra lại từng trích dẫn trước khi bất kỳ claim nào được chuyển sang `verified`.

## Phạm vi hẹp đã chọn
**Mái nhà truyền thống ở các huyện Babergh và Mid Suffolk (Suffolk, Anh)** — vật liệu phủ mái và độ dốc điển hình theo một tài liệu tư vấn bảo tồn của chính quyền địa phương.

Lý do chọn: chỉ một nguồn chính thức, đọc trực tiếp được, đưa ra **số liệu độ dốc theo vật liệu**, có giới hạn rõ về vùng và dùng từ ngữ thận trọng ("usually", "most", "about"). Hệ thống A → B hiện có hiển thị đúng được điều này: cùng tường, khác vật liệu phủ, khác độ dốc.

**Video sẽ không nói:** rằng độ dốc mái được chọn *vì* tuyết hay lượng mưa; rằng có một quy luật toàn cầu; hay rằng một loại mái tốt hơn loại kia. Các nguồn mô tả *xu hướng* trong một khu vực, không phải quan hệ nhân quả được chứng minh.

## Nguồn

| ID | Nguồn | Nhà phát hành | Loại | Truy cập | Trạng thái đọc |
|---|---|---|---|---|---|
| SRC_001 | *Roof Coverings – Traditional Materials, Repairs and Detailing*, Conservation Advice, Nov 2025 (3rd ed.) — https://www.midsuffolk.gov.uk/documents/d/asset-library-54706/roof-coverings-traditional-materials-repairs-and-detailing-guidance | Babergh & Mid Suffolk District Councils (Historic Environment) | Tư vấn chính thức của chính quyền địa phương | 2026-10-26 | **Đã đọc** (PDF, tr. 4, 9–11) |
| SRC_002 | *2012 Seattle Residential Code*, Chapter 9 Roof Assemblies (dựa trên IRC 2012, có sửa đổi của Seattle) — https://seattle.gov/documents/departments/sdci/codes/seattleresidentialcode/2012srcchapter9.pdf | City of Seattle SDCI | Mã xây dựng (bối cảnh hiện đại, Mỹ) | 2026-10-26 | **Đã đọc** (PDF, tr. 454–458) |
| SRC_003 | Hồ sơ đề cử UNESCO, *Historic Villages of Shirakawa-go and Gokayama* (734) | Nhà nước Nhật Bản / UNESCO WHC | Hồ sơ di sản | — | **Chưa đọc**: whc.unesco.org trả về HTTP 403; nội dung chỉ thấy qua đoạn trích của công cụ tìm kiếm. **Không dùng.** |
| SRC_004 | North Norfolk Design Guide — Roofs | North Norfolk District Council | Hướng dẫn chính quyền địa phương | — | **Chưa đọc** (kết nối bị từ chối). Chỉ có đoạn trích tìm kiếm ("50° or over" cho thatch). **Không dùng** cho đến khi được đọc. |

## Claim (đề xuất)

| Claim | Nội dung đề xuất (tiếng Anh, dùng cho narration) | Nguồn + vị trí | Trích dẫn nguyên văn | Mức tin cậy / lưu ý | Cách thể hiện bằng hình |
|---|---|---|---|---|---|
| CLM_001 | Most roofs work by shedding water. | SRC_001 tr. 4 | "Most roofs perform their job by shedding water." | Cao. Câu chung trong tư vấn bảo tồn | HOLD + highlight tấm phủ mái; mũi tên nước chảy chèn ở hậu kỳ (không dựng mô phỏng) |
| CLM_002 | In Babergh and Mid Suffolk, the most typical thatch is longstraw, laid at a steep pitch of about 50°. | SRC_001 tr. 9 | "Most typical for our districts is longstraw thatch, which is laid at the steeper pitch of about 50º." | Cao về phạm vi; "about 50°" là xấp xỉ | Thẻ chữ + thước đo góc 50° trên mặt cắt sơ đồ (không có mô hình 3D mái tranh trong M3) |
| CLM_003 | Most plain clay tile roofs there are fairly steep, between 45° and 60°, often replacing earlier thatch. | SRC_001 tr. 10 | "Most plain tile roofs are fairly steeply pitched between 45° and 60°, often replacing a former thatch covering." | Cao về phạm vi; "most" | State `plain_tile_50` (gable_roof 50°, màu đất nung); EXPLODED_VIEW để thấy tấm phủ đặt trên kết cấu gỗ |
| CLM_004 | Slate roofs there are usually pitched at around 30°; slate works better than smaller tiles at a lower pitch. | SRC_001 tr. 11 | "Slate is also on timber battens, but roofs are usually pitched at around 30º and are more effective than other smaller tiles at a lower pitch." | Cao về phạm vi; "usually", "around". Nguồn **không** giải thích cơ chế: không được tự thêm | REPLACE_PARTS `plain_tile_50` → `slate_30`, tường giữ nguyên, camera khóa |
| CLM_005 | Slate roofs there date from the 18th century onwards and are most common in the 19th; railways brought slate from Wales, Cornwall and Cumbria. | SRC_001 tr. 11 + tr. 9 | "They date from the 18th century onwards but are most common in the 19th century." / "In the 19th century, the creation of the railways meant that slate from Wales, Cornwall and Cumbria were often also used in our area." | Cao về phạm vi; ngày tháng ở mức thế kỷ | Thẻ chữ/sơ đồ (bản đồ chỉ dùng khi có nguồn được cấp phép) |
| CLM_006 *(tùy chọn, bối cảnh khác)* | A modern US residential code (Seattle 2012, IRC-based) sets minimum slopes by covering: e.g. asphalt shingles 2:12, slate 4:12. | SRC_002 tr. 454 R905.2.2; tr. 458 R905.6.2 | "Asphalt shingles shall be used only on roof slopes of two units vertical in 12 units horizontal (2:12) or greater." / "Slate shingles shall be used only on slopes of four units vertical in 12 units horizontal (33-percent slope) or greater." | Cao, nhưng là **độ dốc tối thiểu** theo **luật hiện đại ở một thành phố của Mỹ**, không phải độ dốc điển hình trong lịch sử. Nếu dùng phải ghi rõ bối cảnh, hoặc bỏ đi để pilot không lẫn lộn | Nếu dùng: thước đo tối thiểu trên SIDE_BY_SIDE. Ghi chú: mái A của pilot (18° ≈ 3.9:12) thấp hơn mức 4:12 (18.4°) dành cho slate |

### Đã cân nhắc và loại bỏ
- **Tuyết / lượng mưa → độ dốc**: chưa có nguồn đọc được trong phạm vi Suffolk. Loại khỏi pilot.
- **Shirakawa-go gassho ">60°" so với nhà làng Nhật thông thường "<45°"**: chưa đọc được nguồn gốc (HTTP 403). Có thể là đề tài cho video khác sau khi người kiểm tra trực tiếp hồ sơ đề cử.
- **"Suffolk: mái ngói phẳng với các hàng dưới lợp slate ở độ dốc thoải hơn"** (SRC_001 tr. 11): ví dụ "một tòa nhà, hai độ dốc" rất hay, nhưng cần hình học mái gãy góc (kicked eaves) → ứng viên cho sau M3.

## Câu hỏi mở cho người duyệt (G1)
1. Kiểm tra lại trích dẫn của CLM_001–005 trên bản PDF hiện hành (ấn bản 3, Nov 2025); ghi ngày truy cập.
2. Tìm thêm một nguồn độc lập cho độ dốc slate ~30° và thatch ~50° (Historic England / SPAB / sách chuyên ngành) để không chỉ dựa vào một tài liệu.
3. Quyết định có đưa CLM_006 (luật Mỹ) vào video Suffolk hay không. Mặc định: không.
4. Ảnh: dùng ảnh nhà mái tranh Suffolk có license, hay chỉ dùng sơ đồ?
