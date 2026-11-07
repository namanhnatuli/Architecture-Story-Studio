# Đề xuất A/B test: title và thumbnail (Gothic cathedral)

**Trạng thái:** đề xuất của agent, chưa chọn gì. Chủ kênh quyết định bản nào dùng và có chạy test hay không. Studio không đăng và không tự đổi gì trên YouTube.

## Quy tắc chạy
- Mỗi lần chỉ đổi một biến. **Vòng 1:** so thumbnail, giữ nguyên title. **Vòng 2:** so title với thumbnail thắng vòng 1.
- YouTube Test & Compare cho thử tối đa 3 thumbnail. Chưa kiểm tra hiện nay nó có hỗ trợ title không; nếu chưa, đổi title luân phiên theo tuần.
- Chữ trên thumbnail bổ sung cho title, không lặp lại. E2 lặp title nên chỉ dùng làm đối chứng.
- Title ≤ 70 ký tự. Không dùng "secret" hoặc khẳng định nguyên nhân sập (phim nói còn tranh luận).

## Title
| | Title | Ký tự | Ghép thumbnail |
|---|---|---|---|
| G1 | How Gothic Cathedrals Reached Impossible Heights | 48 | E2 (đối chứng; tiêu đề hiện tại) |
| G2 | How Did Medieval Builders Raise Stone This High? | 48 | A2 "STONE THIS HIGH?" |
| G3 | What Holds Up a Gothic Cathedral? Arches, Ribs and Buttresses | 61 | B2 "WHAT HOLDS IT UP?" |
| G4 | How High Could Gothic Builders Go? Beauvais, 1284 | 49 | C2 "VAULTS COLLAPSED" |

## Thumbnail (trong `review/thumbnails/`, 1920×1080 và 1280×720)
| Bản | Chữ | Hình | Ghi công cần có trong description |
|---|---|---|---|
| A2 `thumb_A2_stone_this_high` | STONE THIS HIGH? | Hợp xướng Beauvais nhìn lên (Dguendel, CC BY 4.0) | đã có |
| B2 `thumb_B2_what_holds_it_up` | WHAT HOLDS IT UP? + vòng vàng quanh trụ chống | Notre-Dame chevet (Jebulon, CC0) | đã có |
| C2 `thumb_C2_vaults_collapsed` | VAULTS COLLAPSED, BEAUVAIS · 1284 | Beauvais từ Rue Chambiges (Dguendel, CC BY 4.0) | đã có |
| E2 `thumb_E2_impossible_heights` | IMPOSSIBLE HEIGHTS | Mô hình 3D của phim | không cần |

Bản A, B, C, D, E, F (vòng 1) vẫn nằm trong thư mục; E và F dùng mặt nạ tách nền cũ (viền nhoè) và không còn được đề xuất.

## Đánh giá của chủ kênh (vòng 1) đã áp dụng
Một thông điệp chính cho mỗi bản; bỏ dòng phụ và đường kẻ; công trình lớn hơn; F thay bằng ảnh Beauvais thật (C2); E phóng to và tràn khỏi mép dưới.

## Còn mở
- Chưa có góc nhìn thấp cho mô hình 3D (cần render lại bằng Blender).
- "VAULTS COLLAPSED" ở C2: lời phim nói một phần vòm hợp xướng đổ năm 1284; thông điệp ngắn này đủ gần nhưng không nói "tất cả". Nếu muốn chặt hơn: "VAULT COLLAPSED".
- Chưa thử thu nhỏ 320 px và 160 px cho bản vòng 2.


## Tags
Xem `review/YOUTUBE_TAGS.md`.


## Phụ đề và lồng tiếng
**Trạng thái:** hướng dẫn của agent, chưa thực hiện trên YouTube. Studio không đăng. Tính năng YouTube có thể đổi tên mục; kiểm tra giao diện Studio hiện tại.

### Phụ đề tiếng Anh (ngôn ngữ gốc): nên tải lên
- File: `output/gothic_cathedral_heights_FINAL_4K_2160p.en.srt` (214 dòng, mỗi dòng tối đa 42 ký tự, dòng cuối kết thúc 15:22). Chữ lấy từ kịch bản nên đúng chính tả tên riêng, thời gian căn theo chính lời đọc; chính xác hơn phụ đề tự động của YouTube.
- Tải lên: YouTube Studio → Phụ đề → ngôn ngữ gốc (English) → Thêm → Tải tệp lên → "Có thời gian" (With timing).
- Đặt đúng **ngôn ngữ gốc** của video ở Cài đặt nâng cao; sai ngôn ngữ thì bản dịch và đồng bộ sai theo.
- Track phụ đề nhúng trong MP4 (mov_text) YouTube không dùng; vẫn phải tải `.srt` riêng.
- Sau khi tải: xem mốc đầu, giữa, cuối có khớp tiếng không và tên riêng (Beauvais, Saint-Denis, Suger, Viollet-le-Duc) có đúng không.

### Lồng tiếng tự động (auto dubbing)
- Không bắt buộc tạo phụ đề riêng cho từng ngôn ngữ. YouTube dịch từ phụ đề ngôn ngữ gốc, nên phụ đề gốc chuẩn là việc quan trọng nhất (lỗi trong đó lan sang mọi bản dịch và bản lồng tiếng). Người xem vẫn bật được phụ đề dịch tự động.
- Chỉ tự tải bản dịch cho một ngôn ngữ nếu bạn kiểm tra được chất lượng, thường là ngôn ngữ của khán giả chính.
- Rủi ro 1: giọng AI đọc lại đoạn đã dịch, tên riêng dễ bị đọc sai; bản gốc đã phải thêm ghi đè phát âm cho giọng Kokoro (am_michael), bản lồng tiếng không có.
- Rủi ro 2: phần công bố trong description nói về giọng am_michael; bản lồng tiếng dùng giọng khác.
- Nếu chưa muốn bản lồng tiếng: tắt "Cho phép lồng tiếng tự động" trong Cài đặt nâng cao. Nếu bật: nghe thử vài đoạn có tên riêng trước khi để công khai.
