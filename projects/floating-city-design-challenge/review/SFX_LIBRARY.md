# Kho SFX `sfx/`: kiểm kê và quyền sử dụng (2026-11-11)

- **Trạng thái:** chưa dùng file nào. Hai âm trong đoạn thử B09–B10 vẫn là âm tổng hợp của Studio.
- **Nguồn:** chủ kênh cho biết các file lấy từ CapCut.
- **Số liệu chi tiết:** `review/sfx_inventory.json` (đo bằng ffprobe và ffmpeg; chưa ai nghe).

## Kỹ thuật
- **Định dạng:** cả 44 file là AAC trong vỏ MP4/M4A, dù đuôi tên là `.mp3`.
  - Khi đưa vào pipeline, phải dò codec rồi chuyển một bản làm việc sang WAV; giữ nguyên file gốc.
- **Âm lượng chênh rất xa:**
  - hai file sóng biển khoảng −38 LUFS;
  - `boom sub-drop`, `deep bass` khoảng −9 đến −10 LUFS;
  - ba file nảy đỉnh trên 0 dBFS (`asmr stir…`, `call bell…`, `stir ice…`).
  - Nếu dùng, phải chuẩn hóa từng file trước khi trộn dưới lời dẫn.
- **File rất ngắn** (dưới 0,4 s) đo ra −70 LUFS vì phép đo cần tối thiểu 0,4 s; đó không phải file im lặng.

## Quyền sử dụng: điểm chặn
Theo [CapCut Materials License Agreement](https://web-sg.capcut.com/clause/material-license-agreement?lang=en), bản cập nhật 22/01/2026:
- **Phần mở đầu:** hiệu ứng âm thanh thuộc "Platform Materials".
- **Mục 1:** chỉ được chỉnh sửa tư liệu này trên nền tảng CapCut. Sau khi xuất, tư liệu chỉ được hiện như một phần của nội dung, không sửa thêm.
- **Mục 4** cấm:
  - sửa tư liệu bên ngoài nền tảng;
  - tách tư liệu ra khỏi nội dung;
  - khai thác tư liệu như một thứ riêng lẻ.
- **Mục 1–2:** quyền thương mại chỉ có giới hạn, áp dụng cho tư liệu đánh dấu "Dual Use".

Pipeline của Studio cắt, chỉnh âm lượng và trộn file trong ffmpeg, tức là sửa và dùng tư liệu ngoài CapCut, cho một video YouTube có thể kiếm tiền. Đọc theo văn bản, cách dùng này **nằm ngoài phạm vi được phép**. Đây là tóm tắt văn bản, không phải ý kiến pháp lý.

## Đề nghị
1. **Không đưa các file này vào pipeline.** Giữ hai âm tổng hợp hiện có làm chuẩn so sánh.
2. **Nếu cần thêm âm** (đặt khối nhẹ, nước sát mạn, một tiếng "whoosh" chuyển chương):
   - lấy từ nguồn có giấy phép ghi rõ cho dùng thương mại ngoài nền tảng (ví dụ CC0), hoặc tự tổng hợp;
   - lưu nguồn, giấy phép, checksum vào manifest như với Sand3D.
3. **Danh sách ứng viên theo sự kiện** (theo review R2) chỉ có giá trị khi tìm được file thay thế có quyền rõ:
   - chuyển chương: một tiếng whoosh ngắn;
   - vẽ nét: bút chì;
   - lật trang;
   - nước nhẹ sát mạn, không phải sóng đập bãi.
4. **Chủ kênh quyết** có tìm nguồn khác hay giữ âm tổng hợp.
