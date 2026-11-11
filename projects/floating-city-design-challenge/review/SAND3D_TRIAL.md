# Thử Sand3D cho chi tiết đô thị (2026-11-10)

- **Trạng thái:** thử nghiệm. Chưa đưa đối tượng nào vào shot của phim, chưa ghi vào `assets/manifest.json`.
- **Đầu vào:** đề xuất của chủ kênh: dùng Sand3D cho đồ phụ đô thị; giữ bộ sinh của dự án cho phao, mặt cắt và mọi chuyển động gắn với phép tính.
- **Tệp:**
  - ảnh và kịch bản thử: `output/pilot/sand3d_trial/` (ngoài git);
  - nguồn, checksum, ghi công từng đối tượng: `review/sand3d_candidates.json`.

## Cách làm
- **Không cài thư viện Sand3D.** Nhập thẳng file `.usda` đã dựng sẵn của dataset `Sandflow/sand3d-objaverse` (revision `92dd5858…`) bằng bộ nhập USD có sẵn của Blender 5.2.
  - Lý do: package yêu cầu Python ≥ 3.11, < 3.14 và loại trừ 3.12; CLI của Studio chạy 3.14.
  - Chỉ cần thư viện khi muốn dựng lại hình theo tham số.
- **Chọn từ dataset** bằng API tìm kiếm của Hugging Face. Tiêu chí: file nhỏ, `f_score` ≥ 0,97, giấy phép nguồn CC-BY-4.0. Chọn được bốn mẫu: ghế công viên, đèn đường, bộ đồ chơi sân chơi, bàn picnic. **Ngoại lệ:** bộ đồ chơi có `f_score` khoảng 0,966, dưới ngưỡng; bản trước ghi nhầm là cả bốn mẫu đều đạt. Điểm này cũng không thay cho việc xem hình.
- **Kiểm tra trước khi nhập:**
  - checksum SHA256 khớp metadata của dataset;
  - nội dung chỉ là lưới đa giác thuần (mét, trục Z lên), không tham chiếu file ngoài, không có mã.
- **Chuẩn hóa:** vật liệu gốc (oak, pine, painted metal, plastic…) đổi sang vật liệu phẳng của Studio (gỗ sáng, thép tối, sân chơi cam); giữ nguyên kích thước thật.
- **Đặt trên một phao 40 m** (`floating_platform_a_01`):
  - 4 ghế dọc phố giữa;
  - 2 đèn ở góc ngã tư;
  - bộ đồ chơi ở ngã tư;
  - 2 bàn picnic ở dải sàn trống ven mép.
- **Render** trước và sau, cùng camera, 1280×720, EEVEE.

## Kết quả

| | Trước | Sau |
|---|---|---|
| Khung cả phao (camera ba phía như phim) | 1,23 s | 1,14 s |
| Khung cận vào ngã tư | 1,32 s | 1,38 s |
| Đối tượng lưới trong cảnh | 47 | 190 (thêm 143: ghế 9, đèn 7, bộ đồ chơi 52, bàn 20 mỗi cái) |

- **Nhập và chuẩn hóa thuận lợi.** Mỗi file nhập dưới 10 ms; tỉ lệ đúng (ghế 1,5 m, đèn 6 m, bộ đồ chơi 4 × 3,8 × 3 m). Hình hợp phong cách Studio sau khi đổi vật liệu.
- **Chi phí render không đáng kể** ở khung này.
- **Chỉ có tác dụng ở khung cận.**
  - Ở khung cả phao, đồ vật gần như biến mất: chỉ thấy bàn picnic và đỉnh đèn.
  - Ở khung cận ngã tư, đèn và bàn đọc được, nhưng ghế và bộ đồ chơi phần lớn bị nhà che.
  - Phim hiện chủ yếu dùng khung trung và toàn cảnh, đúng như nhận xét trong góp ý.
- **Quyền sử dụng:**
  - dataset CC-BY-4.0; giấy phép nguồn của cả bốn mẫu là CC-BY-4.0 (`license_status: ok`);
  - mỗi mẫu có dòng ghi công riêng (tên, tác giả, URL Sketchfab, giấy phép, ghi chú đã sửa).
  - Nếu dùng, phải giữ các dòng này trong mô tả video và phần ghi công, liên kết giấy phép, và nêu Studio đã đổi vật liệu.

## Đề xuất
1. **Chưa nhân ra toàn quận.** Với toàn cảnh, hình dáng công trình, mái, mảng xanh và lối đi (đã làm ở vòng R2) có tác dụng lớn hơn.
2. **Nếu bạn đồng ý, dùng ở hai loại cảnh cận:**
   - công viên quanh hồ: ghế, đèn, bàn picnic;
   - sân trường: bộ đồ chơi, thay các khối đồ chơi đơn giản hiện có.
   Hiện chưa có shot nào cận tới mức đó. Cần thêm một khung cận, ví dụ khi B01 nói "parks".
3. **Cách đưa vào thư viện khi được duyệt:**
   - chép file `.usda` vào `asset_library/` kèm manifest (nguồn, revision, checksum, ghi công);
   - viết bộ nhập: USD → component có ID, vật liệu Studio, loại `DECORATION`;
   - ghi `assets/manifest.json` của dự án với `status: approved` trước bản final.

---

# Vòng 2 (2026-11-11): tòa nhà và cận cảnh công viên

- **Đầu vào:** review R2 đề nghị thử 3–5 kiểu nhà thấp tầng, trong đó có tòa nhà Sand3D, trên một cụm 3–5 phao. Không kéo giãn nhà một tầng thành ba tầng.
- **Tệp:**
  - ảnh so sánh và script thử: `output/pilot/cluster_trial/` (ngoài git);
  - hồ sơ 7 mẫu đã tải và đo: `review/sand3d_candidates.json` → `buildings_screened`.

## Sàng lọc tòa nhà
- **Cách làm:**
  - truy vấn dataset (`apartment building`, `residential house`; các truy vấn khác bị máy chủ Hugging Face báo lỗi tạm thời);
  - xem ảnh xem trước của khoảng 100 mẫu thuộc nhóm `building`;
  - tải 7 mẫu ở revision cố định, so checksum, đọc file (chỉ là lưới, không tham chiếu ngoài);
  - nhập vào Blender 5.2 và đo.
- **Tiêu chí:** nhà ở thấp tầng **3 tầng**, mỗi tầng khoảng 3 m, đúng tỉ lệ hoặc chỉ cần phóng đều, phong cách Studio theo kịp.
- **Kết quả: trong 7 mẫu đã tải và đo, không mẫu nào đạt.** Đợt thử chỉ chạy hai truy vấn và xem khoảng 100 ảnh xem trước, nên kết luận đúng phạm vi là *chưa tìm được mẫu phù hợp trong đợt thử này*, không phải Sand3D không có nhà ba tầng dùng được.

| Mẫu | Đo được | Kết luận |
|---|---|---|
| "Batiment Marin" (dãy có ban công) | 4 hàng ban công trong 5,8 m; ở tầng 3 m là dãy 4 tầng 18 × 51 m | 4 tầng |
| "Apartment Building [Game Asset]" | ghi là townhouse; đặt lên phao thấy 2 hàng cửa sổ; phóng lên 9 m thì mỗi tầng 4,5 m | 2 tầng |
| "Old Building" | chỉ là mặt tiền sâu 4,2 m, 15.677 đỉnh | không phải một tòa nhà |
| "Apartment" (khối nâu) | cao 25,8 m, ảnh xem trước 3 hàng cửa | sai tỉ lệ |
| 3 nhà phố Pháp (Troyes, Dijon, Fumay) | 2 tầng và mái dốc, 48–62 m² | 2 tầng |

- Trong các ảnh xem trước đã xem, nhóm `building` chủ yếu là mô hình vì kèo, tháp cao, nhà kho và nhà 1–2 tầng.
- Mẫu "townhouse" vẫn được đặt thử lên một phao (8 căn) để so hình: xem `sand3d_platform4.png` cạnh `types_platform4.png`.

## Kiểu nhà của Studio (dùng thay)
- **5 kiểu nhà ở và một kiểu "phòng vườn"** trong `engine/arch/families/floating.py`:
  - dãy nhà liền kề mái dốc;
  - khối sân trong có pin mặt trời;
  - biệt thự mái lệch ốp gỗ;
  - bốn thanh nhà xoay có ban công;
  - bốn khối cũ;
  - phao vườn mở ra mặt hồ.
- **Kiểu nào cũng giữ:** 40% diện tích chiếm đất, 3 tầng, trọng tâm ở giữa sàn, và phố chữ thập ở giữa phao. Test kiểm cả bốn điều này.

## Cận cảnh công viên: đồ vật Sand3D và đồ của Studio
- **Cùng camera, cùng phao vườn:**
  - `types2_park.png`: ghế, bàn picnic, đèn, xích đu và tháp cầu trượt do bộ sinh của Studio dựng;
  - `sand3d_park.png`: thay bằng 4 mẫu Sand3D đã kiểm ở vòng 1.
- **Nhận xét:**
  - ghế, bàn và đèn tương đương nhau;
  - bộ đồ chơi Sand3D chi tiết hơn, nhưng xích đu và cầu trượt của Studio cũng đọc ra là sân chơi.
- **Thời gian render:** gần như không đổi (cận cảnh 1080p: 1,97 s so với 1,97 s).

## Đề nghị
1. **Không dùng tòa nhà Sand3D cho phim này:** trong đợt thử chưa tìm được mẫu đúng 3 tầng.
2. **Phim dùng đồ của Studio** trong đoạn mở đầu: không cần ghi công, không phụ thuộc giấy phép ngoài.
3. **Nếu bạn thích bộ đồ chơi Sand3D hơn:** cần viết bộ nhập USD vào thư viện, ghi manifest và dòng ghi công trước khi dùng.

## Sau review L6 (2026-11-11)
- **Review L6 đồng ý** giữ nhà và đồ công viên của Studio cho vòng sản xuất này:
  - nhà Sand3D đặt thử đọc thành hai tầng, lệch giả định ba tầng;
  - bộ sân chơi và ghế Sand3D chi tiết hơn, nhưng đèn lớn và đậm tạo nhiều điểm hút mắt; trong cận cảnh ngắn, lợi ích chưa đủ để tích hợp.
- **Giữ các ứng viên Sand3D** (`review/sand3d_candidates.json`) cho cảnh nào cần cận lâu hơn. Khi đó vẫn phải viết bộ nhập USD, ghi manifest và dòng ghi công CC-BY-4.0 trước khi dùng.
- **Không tìm tiếp trong vòng này.** Kết luận chỉ áp cho đợt thử đã ghi ở trên.
