# Đề xuất A/B test: title và thumbnail (Why bridges look different)

**Trạng thái:** đề xuất của agent, chưa chọn gì. Chủ kênh quyết định. Studio không đăng và không tự đổi gì trên YouTube.

## Quy tắc chạy
- Mỗi lần chỉ đổi một biến: vòng 1 so thumbnail với title cố định, vòng 2 so title với thumbnail thắng.
- YouTube Test & Compare cho thử tối đa 3 thumbnail; chưa kiểm tra hiện nay nó có hỗ trợ title không, nếu chưa thì đổi title luân phiên theo tuần.
- Chữ trên thumbnail bổ sung cho title, không lặp lại. Title ≤ 70 ký tự.

## Title
| | Title | Ký tự | Ghi chú |
|---|---|---|---|
| B1 | Why Bridges Don't All Look the Same | 35 | đối chứng; tiêu đề hiện tại |
| B2 | How Do Bridges Carry Load? Six Designs Explained | 48 | đúng sáu kiểu của phim: beam, arch, truss, cantilever, suspension, cable-stayed |
| B3 | Beam, Arch, Truss, Suspension: Why Bridges Look So Different | 61 | chỉ nêu bốn trong sáu kiểu để title không quá dài; người xem có thể tưởng phim chỉ có bốn |

## Thumbnail (trong `review/thumbnails/`, 1280×720)
Bảy thiết kế của chủ kênh, đều dùng mô hình 3D và đồ họa tự dựng của phim nên không có ghi công ảnh nào thêm. Mỗi bản có `.jpg` (100–160 KB); bản D–G có thêm `.png` (khoảng 1,8 MB, gần giới hạn 2 MB của YouTube, nên dùng `.jpg`).

| Bản | Chữ | Hình | Nhận xét thiết kế (chưa phải dự đoán CTR) |
|---|---|---|---|
| A `thumb_A_3_bridges_3_answers` | 3 BRIDGES. 3 ANSWERS. / WHY THEY LOOK DIFFERENT | Ba cầu xếp dọc (arch, truss, cable-stayed), khối chữ nền tối bên trái | Có dòng phụ nhỏ ("WHY THEY LOOK DIFFERENT") sẽ khó đọc ở 160 px; ba cầu nhỏ. Hứa "3" trong khi phim có 6 kiểu. |
| B `thumb_B_why_that_shape` | WHY THAT SHAPE? | Một cầu treo lớn, chữ trên cùng | Đơn giản và dễ đọc nhất khi thu nhỏ; một vật thể, một câu hỏi. Chữ gần như lặp title B1. |
| C `thumb_C_see_the_forces` | SEE THE FORCES + nhãn PUSH / PULL | Cầu giàn thép có mũi tên xanh (đẩy), đỏ (kéo) | Khác biệt rõ nhất: cho thấy phim có đồ họa lực. Nhớ rằng mũi tên là khái niệm, không phải lực tính toán (phim đã ghi chú). |
| D `thumb_D_blueprint_sheet` | nhãn từng kiểu: Timber Beam, Stone Arch, Steel Truss, Cantilever, Suspension, Cable-Stayed | Lưới 2×3 sáu cầu | Khớp đúng sáu kiểu của phim. Nhiều chi tiết nhỏ và nhãn nhỏ; ít hiệu quả ở 160 px. Hợp với title B2 "Six Designs". |
| E `thumb_E_why_that_shape_sheet` | WHY THAT SHAPE? (serif) | Lưới sáu cầu bên dưới | D với tiêu đề hỏi; chữ serif hợp chất "lịch sử" nhưng cầu nhỏ. |
| F `thumb_F_title_in_middle` | WHY THAT SHAPE? ở giữa | Ba cầu trên, ba cầu dưới | Chữ ở giữa chia hình thành hai nửa; dễ đọc hơn E. |
| G `thumb_G_title_sans` | WHY THAT SHAPE? (sans, đậm) | Ba cầu trên, ba cầu dưới | F với chữ sans-serif đậm; chữ mạnh nhất trong nhóm E–G. |

E, F, G chỉ khác phông chữ và bố cục; nếu chạy test, chọn một trong ba, không đưa cả ba vào cùng vòng.

## Ghép đề xuất
| Vòng | Thumbnail | Title | Lý do |
|---|---|---|---|
| 1 (so thumbnail, title B1 cố định) | B, C, và G hoặc D | B1 "Why Bridges Don't All Look the Same" | Ba hướng khác hẳn nhau: một cầu + câu hỏi, đồ họa lực, và bảng sáu kiểu. A bỏ vì hứa "3" và có dòng phụ nhỏ. |
| 2 (so title, thumbnail thắng vòng 1) | thắng vòng 1 | B1, B2, B3 | Nếu thắng là B hoặc G (chữ "WHY THAT SHAPE?") thì title B1 trùng ý; thử B2 hoặc B3 để title bổ sung chứ không lặp lại. Nếu thắng là D, B2 "Six Designs" khớp nhất. |

## Còn mở
- Chưa kiểm tra cả bảy bản ở 320 px và 160 px (tôi xem ở cỡ ~640 px).
- Chưa đối chiếu hình cầu trong thumbnail với cảnh của phim; nên xem các mô hình trùng với những gì phim cho thấy.


## Tags
Xem `review/YOUTUBE_TAGS.md`.


## Phụ đề và lồng tiếng
**Trạng thái:** hướng dẫn của agent, chưa thực hiện trên YouTube. Studio không đăng. Tính năng YouTube có thể đổi tên mục; kiểm tra giao diện Studio hiện tại.

### Phụ đề tiếng Anh (ngôn ngữ gốc): nên tải lên
- File: `output/why_bridges_look_different_FINAL_4K_2160p.en.srt` (271 dòng, mỗi dòng tối đa 42 ký tự, dòng cuối kết thúc 19:54). Chữ lấy từ kịch bản nên đúng chính tả tên riêng, thời gian căn theo chính lời đọc; chính xác hơn phụ đề tự động của YouTube.
- Tải lên: YouTube Studio → Phụ đề → ngôn ngữ gốc (English) → Thêm → Tải tệp lên → "Có thời gian" (With timing).
- Đặt đúng **ngôn ngữ gốc** của video ở Cài đặt nâng cao; sai ngôn ngữ thì bản dịch và đồng bộ sai theo.
- Track phụ đề nhúng trong MP4 (mov_text) YouTube không dùng; vẫn phải tải `.srt` riêng.
- Sau khi tải: xem mốc đầu, giữa, cuối có khớp tiếng không và tên riêng (Bollman, Penobscot, Wheeling) có đúng không.

### Lồng tiếng tự động (auto dubbing)
- Không bắt buộc tạo phụ đề riêng cho từng ngôn ngữ. YouTube dịch từ phụ đề ngôn ngữ gốc, nên phụ đề gốc chuẩn là việc quan trọng nhất (lỗi trong đó lan sang mọi bản dịch và bản lồng tiếng). Người xem vẫn bật được phụ đề dịch tự động.
- Chỉ tự tải bản dịch cho một ngôn ngữ nếu bạn kiểm tra được chất lượng, thường là ngôn ngữ của khán giả chính.
- Rủi ro 1: giọng AI đọc lại đoạn đã dịch, tên riêng dễ bị đọc sai; bản gốc đã phải thêm ghi đè phát âm cho giọng Kokoro (am_michael), bản lồng tiếng không có.
- Rủi ro 2: phần công bố trong description nói về giọng am_michael; bản lồng tiếng dùng giọng khác.
- Nếu chưa muốn bản lồng tiếng: tắt "Cho phép lồng tiếng tự động" trong Cài đặt nâng cao. Nếu bật: nghe thử vài đoạn có tên riêng trước khi để công khai.
