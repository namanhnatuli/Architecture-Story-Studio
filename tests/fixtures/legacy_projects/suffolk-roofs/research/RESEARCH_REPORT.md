# Báo cáo nghiên cứu & bằng chứng — "Why Did Traditional Roofs in Suffolk Change?"

Trạng thái: **G1 đang chờ duyệt biên tập.** Mọi claim được dùng trong lời dẫn đều đã `SOURCE_VERIFIED` (câu chữ đã đối chiếu với nguồn, có vị trí cụ thể). **Chưa claim nào `EDITORIALLY_APPROVED`**: việc đó cần người duyệt. Sổ bằng chứng có cấu trúc: `research/sources.json`.

## Nguồn
| ID | Nguồn | Cách kiểm tra |
|---|---|---|
| SRC_001 | Babergh & Mid Suffolk District Councils, *Roof Coverings – Traditional Materials, Repairs and Detailing*, Conservation Advice, Nov 2025, ấn bản 3 (PDF) — https://www.babergh.gov.uk/documents/d/asset-library-54706/roof-coverings-traditional-materials-repairs-and-detailing-guidance | Đọc từng trang (tr. 1–4, 9–11). Bản tải từ URL babergh ngày 2026-10-27 **trùng từng byte** với bản đã đọc ngày 2026-10-26 (sha256 bắt đầu bằng `cc388dd2dba70d7c`) |
| SRC_002 | Babergh & Mid Suffolk District Councils, trang web *Roof coverings on historic buildings* — https://babergh.gov.uk/web/mid-suffolk/roof-coverings-on-historic-buildings | Trích bằng công cụ đọc web ngày 2026-10-27 (trang không ghi ngày; footer © 2026). **Cần đọc lại trong trình duyệt ở G1** |

## Claim được dùng trong lời dẫn
| Claim | Nội dung (lời dẫn) | Bằng chứng | Diễn giải / lưu ý | Beat |
|---|---|---|---|---|
| CLM_101 | thatch hoặc oak shingles, "probably", tùy vật liệu sẵn có | SRC_001 tr. 9; SRC_002 | Có chữ rào đón "probably" — giữ trong lời dẫn | B2 |
| CLM_102 | longstraw thatch, "about fifty degrees" | SRC_001 tr. 9 ("most typical"); SRC_002 ("most traditional") | Lời dẫn dùng "most traditional" | B1, B2, B6 |
| CLM_103 | clay peg tiles thay thế **một số** mái tranh | SRC_001 tr. 9; SRC_002 | "some", không phải tất cả → không có trình tự phổ quát | B3, B6 |
| CLM_104 | ngói phẳng khá dốc, "typically forty-five degrees or more" | SRC_001 tr. 10 (45–60°); SRC_002 (khoảng 45°) | **Hai nguồn lệch nhau**; lời dẫn chỉ dùng phần chung | B1, B3, B6 |
| CLM_105 | pantile phổ biến hơn từ thế kỷ 18, khi vận chuyển vật liệu dễ hơn | SRC_001 tr. 9 (sông/kênh); SRC_002 (rẻ hơn) | **Mỗi nguồn có một chi tiết riêng**; lời dẫn bỏ cả hai chi tiết đó | B4 |
| CLM_106 | đường sắt thế kỷ 19 → slate từ Wales, Cornwall, Cumbria "often" được dùng | SRC_001 tr. 9; SRC_002 | "often", không độc quyền; sơ đồ ghi rõ là sơ đồ minh họa, không phải bản đồ | B4 |
| CLM_107 | slate "usually … around thirty degrees", "more effective than smaller tiles at a lower pitch" | SRC_001 tr. 11; SRC_002 | Nguồn chỉ đặt hai ý cạnh nhau; lời dẫn **không** dùng "because" | B1, B5, B6 |
| CLM_108 | slate có từ thế kỷ 18, phổ biến nhất thế kỷ 19 | SRC_001 tr. 11 | Không dùng trong lời dẫn. Giữ lại để biên tập viên biết rằng slate không chỉ xuất hiện khi có đường sắt | — |

B6 là **diễn giải** ("tendencies, not rules … a clue to its covering"), cần biên tập viên chấp thuận câu chữ.

## Đã loại bỏ (REJECTED)
CLM_006 (luật xây dựng Mỹ: ngoài phạm vi), CLM_901 (Shirakawa-go: không đọc được nguồn), CLM_902 (tuyết/mưa → độ dốc: không có nguồn trong phạm vi). Validator báo lỗi nếu shot hoặc lời dẫn nào dùng các claim này.

## Phần nào là minh họa
Nhà là mô hình minh họa (không phải một công trình cụ thể ở Suffolk). Độ dày lớp phủ, khoảng cách hàng ngói/slate, hình ngói nóc và texture là **giả định trực quan đã đơn giản hóa**; chỉ độ dốc (50° / 50° / 30°) và loại ngói nóc (SRC_002) có căn cứ từ nguồn. Ngói phẳng dùng chung kết cấu 50° với mái tranh (nằm trong khoảng 45–60° của PDF), nhằm thể hiện việc **thay lớp phủ** ở CLM_103.

## Việc cần làm cho G1
1. Đọc lại SRC_002 trong trình duyệt, xác nhận các trích dẫn.
2. Duyệt câu chữ từng beat (đặc biệt B1 "do not all look alike" và B6).
3. Quyết định cách phát âm "Babergh" (Whisper nghe thành "Baburg").
4. Chuyển các claim đã duyệt sang `EDITORIALLY_APPROVED`, ghi tên người duyệt và ngày.
