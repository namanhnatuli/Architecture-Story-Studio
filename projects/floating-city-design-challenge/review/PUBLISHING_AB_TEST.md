# Thumbnail và A/B test: Could We Build an Entire City That Floats?

**Trạng thái:** đề xuất của agent. Chủ kênh chưa chọn bản nào và chưa chạy phép thử nào. Studio không đăng và không đổi gì trên YouTube.

## Vòng 2 (2026-11-13): sửa theo review thumbnail
**Đầu vào:** review biên tập của ba bản v1, chủ kênh chuyển tiếp.
- Bản review đầy đủ ở `qa/codex_thumbnail_review/REVIEW.md`, ngoài git.
- **Đề nghị chính:**
  - A làm bản mặc định, B làm đối thủ chính;
  - C cần sửa nhiều nhất, và chỉ đưa vào phép thử khi xem ở cỡ nhỏ vẫn hiểu;
  - giữ nguyên phong cách: navy, trắng, vàng, chữ serif.

| Bản | Nhận xét v1 | Đã sửa ở v2 |
|---|---|---|
| **A2** `thumb_A2_10000_people_no_land` | Dễ trông như một khu đô thị quanh hồ trên đất; lớp tối che nhiều mô hình | Camera mới (SC_001): mép tây của quận, nước bao quanh và đê chắn sóng nổi ngoài khơi; không lộ bờ hay mép bãi nước. Lớp tối chỉ còn ngay sau chữ |
| **B2** `thumb_B2_4800_tons_and_it_floats` | Hình bị dồn xuống góc phải; thân phao giống bê tông đặc; gần như một card chữ | Phối cảnh xiên vào mặt cắt (SC_008): thấy được sàn và vách trong của bốn khoang rỗng, một đầu phao, mặt nước và mặt cắt nước. Hình chiếm khoảng hai phần ba khung; chữ nằm trên cùng |
| **C2** `thumb_C2_what_holds_it_in_place` | Dây neo quá chìm, nhiều đường cắt nhau | Nhìn ngang từ phía tây (SC_024), vuông góc với mặt phẳng dây neo: dây của các phao cùng hàng trùng nhau, nên chỉ còn hai tuyến không cắt nhau. Tuyến chính chạy xuống neo ở góc dưới trái, xa nhãn thời lượng |

**Đúng đối tượng:**
- **B2:** "4,800 TONS" là phao minh họa đầu tiên rộng 40 m của B08: bốn khối nhà ba tầng, tính cả thân phao. Đó không phải khối lượng cả thành phố, cũng không phải phao chuẩn 60 m của quận cuối. Hình B2 chính là phao 40 m đó.
- **A2:** "NO LAND" nghĩa là người dân sống trên phao (B01). Thiết kế trong phim có cầu dẫn nối vào bờ, nên không mở rộng câu chữ thành lời hứa một thành phố tách hẳn khỏi đất liền.

**Hình:**
- Lấy đúng mô hình của phim, ẩn nhãn chú thích, không có watermark.
- Chỉnh màu như v1: độ bão hòa +15%, tương phản +6%.
- Riêng C2: nước giữ màu nhạt như trong phim, chỉ pha thêm chút xanh ở vùng nước bán trong suốt. Dây, neo, thân phao và nhà giữ nguyên màu. Phần trời được thay bằng nền navy.

**File:**
- **Bản tải lên:** `_3840.jpg`, 3840×2160 (cỡ YouTube khuyến nghị), 0,3–1,2 MB.
- **Bản xem nhanh:** `_1280.jpg`.
- Bản v1 (`thumb_A_…`, `thumb_B_…`, `thumb_C_…`) vẫn để cạnh để so.

**Đọc ở cỡ nhỏ:** agent đã xem cả ba ở 320×180 và 168×94.
- **A2, B2:** chữ và hình đều rõ. B2 dễ hiểu nhất: nhà trên một hộp rỗng nằm trong nước.
- **C2:** ở 168 px dây neo mảnh nhưng vẫn theo được từ phao tới neo, và các neo hiện rõ.
- Agent đánh giá C2 đã đủ để thử, nhưng chủ kênh nên tự xem ở cỡ nhỏ trước khi đưa C2 vào phép thử.

## Phép thử đề xuất
**Giả thuyết:** mỗi bản thử một concept trọn vẹn.

| Bản | Thử sức hút của |
|---|---|
| A2 | quy mô: sống trên mặt nước |
| B2 | câu hỏi vật lý: nặng thế mà vẫn nổi |
| C2 | hệ thống giữ thành phố đứng yên một chỗ |

Hình và chữ cùng khác nhau giữa các bản, nên kết quả chỉ cho biết concept nào tốt hơn. Không thể quy riêng cho font, màu, một từ hay góc máy.

**Vòng đầu:**
- **Tiêu đề:** giữ nguyên tiêu đề hiện tại, "Could We Build an Entire City That Floats?" (`project.json` → `publication_metadata.title`).
- **Cách chạy:** dùng "Test & Compare" trong YouTube Studio, chỉ có trên máy tính.
- **Tải A2 lên đầu tiên.** Khi kết quả là "Performed Same" hoặc "Inconclusive", YouTube giữ bản tải lên đầu tiên, và A2 là lựa chọn biên tập mặc định.
- **Số bản:** không cần đủ ba. Nếu chủ kênh thấy C2 chưa đủ rõ ở cỡ nhỏ thì chỉ thử A2 và B2.
- **Không đổi tiêu đề hay thumbnail khi phép thử đang chạy:** đổi thì phép thử dừng.
- **Vòng sau** mới giữ một concept và đổi một yếu tố (ví dụ góc máy), để tìm nguyên nhân rõ hơn. Studio hiện cũng thử được tiêu đề, và cả tiêu đề cùng thumbnail.

**Đọc kết quả:**
- YouTube chọn bản thắng theo **thời gian xem**, không theo CTR. Không chọn tay theo CTR.
- Chờ phép thử tự hoàn tất, thường từ vài ngày tới 2 tuần.
- Kết quả là "Winner", "Performed Same" hoặc "Inconclusive". Với hai kết quả sau, không coi bản có số nhỉnh hơn là bản thắng; giữ A2 theo định hướng biên tập.
- Không so hai lần đổi thumbnail bằng tay ở hai thời điểm như thể cùng một nhóm người xem.

**Nhật ký** (chủ kênh điền khi chạy):

| Mục | Ghi |
|---|---|
| Các bản và file | A2, B2 (C2 nếu dùng): tên file `_3840.jpg` và commit chứa file |
| Tiêu đề cố định | |
| Bắt đầu / kết thúc | |
| Kết quả YouTube | Winner / Performed Same / Inconclusive; bản được chọn |
| Ảnh chụp báo cáo | đường dẫn |

## Yêu cầu file của YouTube
Kiểm trên trang trợ giúp ngày 2026-11-13: https://support.google.com/youtube/answer/72431 và https://support.google.com/youtube/answer/16391400.
- **Kích thước:** khuyến nghị 3840×2160, tỉ lệ 16:9, rộng tối thiểu 640 px; định dạng JPG hoặc PNG.
- **Dung lượng:** tối đa 2 MB khi tải lên từ điện thoại, 50 MB từ máy tính. Mọi file `_3840.jpg` đều dưới 2 MB, nên tải lên được cả từ điện thoại.
- **Test & Compare:** tối đa 3 tiêu đề hoặc thumbnail, chỉ trên máy tính, hoàn tất trong 2 tuần.

## Dựng lại
- **Script:** `review/thumbnails/make/`:
  - `still.py`: render một khung sạch từ `scenes/SC_xxx.blend`, mỗi lúc một Blender; không ghi file `.blend`;
  - `specs_v2.json`: shot, frame, camera, phần cần ẩn; riêng C2 có thêm một lần render nền trong suốt để lấy kênh alpha;
  - `compose_v2.py`: nền, chỉnh màu, vùng tối sau chữ, chữ; cần Pillow 13.0.0.
- Chạy lại cho ra file giống từng byte với các file v2. Bản v1 vẫn dựng lại được bằng `specs.json` và `compose.py`.
- **Thời gian:** mỗi ảnh 4K render mất 3–8 giây.

---

## Vòng 1 (2026-11-13, đã thay bằng vòng 2)
| Bản | Chữ | Hình | Câu trong phim |
|---|---|---|---|
| A `thumb_A_10000_people_no_land` | 10,000 PEOPLE / NO LAND | Toàn quận (SC_001), nhìn chéo; lớp tối lớn bên trái | B01 |
| B `thumb_B_4800_tons_and_it_floats` | 4,800 TONS / AND IT FLOATS | Mặt cắt phẳng của phao 40 m (SC_008) | B08 |
| C `thumb_C_what_holds_it_in_place` | WHAT HOLDS IT / IN PLACE? | Dãy nhà và dây neo theo góc của phim (SC_024) | B22, B24 |

- Chữ của cả ba vòng giữ nguyên, và mỗi chữ đều có câu tương ứng trong lời dẫn (B01, B08, B22).
- Font Charter Black: Georgia dùng chữ số kiểu cũ, làm "10,000" và "4,800" nhỏ và lệch dòng.
