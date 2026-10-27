# Storyboard nháp cho pilot M3 — "Why Do Roof Pitches Vary?" (Suffolk, ~72 s)

> **Đã thay thế (2026-10-27)** bởi `projects/suffolk-roofs/storyboard/storyboard.template.json` và `projects/suffolk-roofs/script/SCRIPT_AND_STORYBOARD.md` (được sinh ra). CLM_006 bị loại; card cho beat thatch được thay bằng mô hình 3D thatch thật. Bản nháp giữ lại làm lịch sử.

Trạng thái: **bản nháp để duyệt.** Narration chưa khóa (G1 chưa đạt; cần TTS cho G4). Thời lượng là ước tính khoảng 150 từ/phút; `tools/timing.py` sẽ thay chúng bằng thời lượng audio đo được.
Mọi chi tiết hình học đều dùng các template và builder hiện có. State mới chỉ là tham số:

| State | Builder | Độ dốc | Màu | Ghi chú |
|---|---|---|---|---|
| `plain_tile_50` | `gable_roof` | 50° | đất nung (`roof_variant_b` #B96A4F) | Nằm trong khoảng 45–60° của CLM_003 |
| `slate_30` | `gable_roof` | 30° | xám slate (palette mới `roof_slate`, đề xuất #5E6670) | "around 30°" của CLM_004 |

Base: nhà chữ nhật hiện có (tường, móng, ceiling joists). Đây là **mô hình minh họa**, không phải bản dựng lại một công trình cụ thể ở Suffolk; mỗi shot có nhà sẽ có dòng chữ "Illustrative model" trên màn hình.

| Beat | Lời dẫn nháp (tiếng Anh) | Claim | Shot / template | Hình ảnh | ~s |
|---|---|---|---|---|---|
| B1 hook | "Why do some old roofs in one corner of England rise steeply, while others sit much lower?" | — (câu hỏi) | SC_001 `SIDE_BY_SIDE` [plain_tile_50, slate_30], không highlight | Hai nhà cùng tỷ lệ; dải chữ dành cho tiêu đề | 6 |
| B2 | "Most roofs do one job above all: they shed water." | CLM_001 | SC_002 `SIDE_BY_SIDE` → cắt sang `HOLD` plain_tile_50 + highlight tấm phủ | Tấm phủ sáng lên; mũi tên nước chảy chèn ở hậu kỳ | 5 |
| B3 | "In Babergh and Mid Suffolk, the most typical traditional thatch, longstraw, is laid at about fifty degrees." | CLM_002 | Thẻ chữ / sơ đồ (không dùng 3D) | Mặt cắt đơn giản + thước đo 50°; ảnh thật chỉ khi có license | 8 |
| B4 | "Most plain clay tile roofs there are fairly steep too — between forty-five and sixty degrees — and often replaced earlier thatch." | CLM_003 | SC_003 `EXPLODED_VIEW` plain_tile_50 | Tấm phủ nhấc lên khỏi rafters; thước đo 45°–60° chèn ở hậu kỳ | 10 |
| B5 | "Slate is different. Slate roofs there are usually pitched at around thirty degrees — and slate is more effective than smaller tiles at a lower pitch." | CLM_004 | SC_004 `REPLACE_PARTS` plain_tile_50 → slate_30 | Cùng tường, camera khóa; mái dốc rời đi, mái thoải hạ xuống | 12 |
| B6 | "Slate arrived in numbers in the nineteenth century, when railways brought it from Wales, Cornwall and Cumbria." | CLM_005 | Thẻ chữ / sơ đồ đơn giản | Ba tên địa danh + đường ray giản lược (tự vẽ) | 9 |
| B7 | "Same walls, a different covering — and a different pitch." | CLM_003, CLM_004 | SC_005 `SIDE_BY_SIDE` + intro từ slate_30, highlight `DIFFERENCES` | Camera lùi ra để thấy cả hai | 8 |
| B8 outro | "Not a universal rule — but in this part of Suffolk, the roof's covering and its pitch go together." | CLM_002–004 (tổng hợp) | `HOLD` comparison (tiếp nối SC_005) | Giữ nguyên khung | 6 |
| | | | | **Tổng** | **≈ 64–72** |

## Rủi ro sự thật cần người duyệt kiểm tra
- **B5** cố ý **không** dùng "because": nguồn chỉ đặt hai ý cạnh nhau ("usually pitched at around 30º and are more effective than other smaller tiles at a lower pitch"), không khẳng định độ dốc được chọn *vì* điều đó. Không được thêm cơ chế (độ thấm nước, kích thước viên slate…) nếu không có nguồn.
- **B6 "arrived in numbers"** phải khớp với "most common in the 19th century" và câu về đường sắt. Không được ngụ ý rằng trước đó không có slate.
- **B8** là kết luận diễn giải. Phải giữ phạm vi ("this part of Suffolk") và dùng từ thận trọng.

## Khớp với hệ thống hiện có
- Mọi shot 3D dùng template M2/M2.5 (HOLD, EXPLODED_VIEW, REPLACE_PARTS, SIDE_BY_SIDE + intro). Không cần template mới.
- Beat B3 và B6 là đồ họa 2D. Công cụ ghép video (bước H của kế hoạch M3) phải hỗ trợ ảnh tĩnh/thẻ chữ có thời lượng. Đó là phần mới duy nhất về hình ảnh.
- Điểm cắt giữa các shot 3D phải đạt kiểm tra SSIM của media QA, trừ khi khai báo `cut_from_previous: "hard"`.
