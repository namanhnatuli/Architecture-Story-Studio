# Kho SFX `sfx/`: kiểm kê và quyền sử dụng (2026-11-11)

- **Trạng thái:** chưa dùng file nào. Hai âm trong đoạn thử B09–B10 vẫn là âm tổng hợp của Studio.
- **Nguồn:** chủ kênh cho biết các file lấy từ CapCut.
- **Mục đích:** chủ kênh tải về làm thư viện chung, chủ yếu là âm meme; kho này không dành riêng cho phim này (chủ kênh, 2026-11-12). Phim này chọn âm theo các nguyên tắc ở mục cuối.
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

## Âm thanh cho phim này: nguyên tắc và ứng viên (2026-11-12)
Phong cách kênh: giải thích kiến thức bằng mô hình kiến trúc tối giản, lời dẫn là chính. Âm hiệu ứng phục vụ việc hiểu, không để gây chú ý.

**Nguyên tắc:**
1. **Chỉ gắn âm khi có hành động vật lý.** Trên hình phải có một vật đặt xuống, chìm hay được lắp vào, và lời dẫn đang nói về nó. Âm giúp người xem cảm được khối lượng.
2. **Âm cỡ mô hình.** Dùng tiếng khối gỗ, vật đặt xuống bàn, nước nhỏ; không dùng âm công trường hay âm điện ảnh. Hình là mô hình thu nhỏ, nên âm cũng vậy.
3. **Không gắn âm cho chữ hay card.** Nhãn, ghi chú, card, con số hiện lên đều không có âm. Không dùng chuông, "pop", "ding", boom, riser, stinger, âm meme.
4. **Nền tiếng nước chỉ ở chỗ nước là chủ đề**, và rất nhỏ, vào và ra mờ dần.
5. **Mọi âm nằm dưới lời dẫn.** Nếu bỏ một âm đi mà không ai thấy thiếu, thì bỏ.

**Tổng cộng:** 4 tiếng ở 4 thời điểm, 2 đoạn nền nước ngắn, và 7 tiếng chuyển chương nếu chủ kênh muốn thử.

Agent **chưa nghe file nào**; chọn theo tên, độ dài và mô tả. Mỗi chỗ có 2–3 ứng viên để chủ kênh nghe rồi chọn.

| # | Thời điểm | Trên hình | Ứng viên (Pixabay) | Ghi chú |
|---|---|---|---|---|
| 1 | 1:12,9 (B05) | Khối bê tông đặc chìm xuống đáy | [Falling of a stone into water](https://pixabay.com/sound-effects/film-special-effects-falling-of-a-stone-into-water-381859/) (0:03) · [Object Drops In Water](https://pixabay.com/sound-effects/film-special-effects-object-drops-in-water-84639/) (0:01) · [Water Splosh](https://pixabay.com/sound-effects/nature-water-splosh-38143/) (0:01) | Chỗ mới. Một tiếng "tõm" nhỏ, không bắn tung |
| 2 | 2:25,3 (B09) | Đặt tầng thứ tư lên nhà | [Place Something](https://pixabay.com/sound-effects/film-special-effects-place-something-42719/) (0:01) · [Small wood Block](https://pixabay.com/sound-effects/film-special-effects-small-wood-block-64458/) (0:42, nhiều lần gõ, chọn một) · [quiet thud hits](https://pixabay.com/sound-effects/nature-quiet-thud-hits-100179/) (0:08) | Đang có âm tổng hợp STONE; nghe so với âm này |
| 3 | 2:42,8 (B10) | Thân phao sâu thêm 0,5 m | [Wooden Thud (Mono)](https://pixabay.com/sound-effects/film-special-effects-wooden-thud-mono-6244/) · [quiet thud hits](https://pixabay.com/sound-effects/nature-quiet-thud-hits-100179/) | Trầm hơn #2. Đang có âm tổng hợp STONE_HEAVY |
| 4 | 3:56,6 (B13) | Đặt cầu đi bộ có bản lề qua khe | [Place Something](https://pixabay.com/sound-effects/film-special-effects-place-something-42719/) · [place](https://pixabay.com/sound-effects/film-special-effects-place-100513/) | Chỗ mới. Nhẹ nhất trong 4 tiếng |
| 5 | 5:33,6–5:45,7 (B17) và 9:17–9:31 (B30) | Phao nhấp nhô theo sóng; sóng dài ngoài khơi | [Water lapping gurgling under dock 05](https://pixabay.com/sound-effects/nature-water-lapping-gurgling-under-dock-05-62167/) (0:45) · [Sound of Water When Sitting in a Boat Looped](https://pixabay.com/sound-effects/nature-sound-of-water-when-sitting-in-a-boat-looped-410627/) (0:08, lặp được) · [200906 Water waves lapping, lake, gentle, close](https://pixabay.com/sound-effects/nature-200906-water-waves-lapping-lake-gentle-close-pec-9am-59256/) (2:12) | Nền rất nhỏ. Không dùng sóng đập bãi |
| 6 (tùy chọn) | 1:04, 3:20, 5:33, 7:02, 7:56, 9:07, 11:41 | Tiêu đề chương | [subtle transition](https://pixabay.com/sound-effects/film-special-effects-subtle-transition-356008/) (0:02) · [Soft luxury air whoosh #1](https://pixabay.com/sound-effects/film-special-effects-soft-luxury-air-whoosh-1-592508/) (bộ #1–#8, mỗi file 1 s) · [Minimalist Light Whoosh FX](https://pixabay.com/sound-effects/film-special-effects-minimalist-light-whoosh-fx-547374/) | Thử một bản; nếu nghe thành "hiệu ứng" thì bỏ hẳn |

**Không dùng** (đã cân nhắc rồi bỏ):
- bút chì, lật trang: card không phải trang sách; phim có nhiều card nên dễ thành ồn;
- xích neo: dây neo trong phim là sơ đồ dưới nước, tiếng xích quá "thật";
- thud bê tông hay đá lớn, "Boom Swoosh", "Cinematic Boom": quá kịch tính so với mô hình;
- chuông thủy tinh (glass chime) cho mạng nối ở B38: là âm giao diện, không phải âm vật lý;
- nền tiếng nước cho cả phim: nước có ở gần như mọi cảnh, nên nền liên tục sẽ thành tiếng ồn.

**Giấy phép:** [Pixabay Content License](https://pixabay.com/service/license/):
- được dùng thương mại, được sửa và trộn, không bắt buộc ghi công;
- không được bán hay phân phối file đứng riêng;
- Pixabay không cam kết về Content ID như YouTube Audio Library. Nếu bị claim, link trang và ngày tải là bằng chứng để khiếu nại.
- File của `freesound_community` là bản đưa lại từ Freesound, có ghi tác giả gốc; agent ghi cả tên đó vào manifest.

**Khi tải:**
- giữ nguyên tên file Pixabay (có số ID khớp với link), để vào `sfx/pixabay/`;
- agent ghi link, tác giả, giấy phép và sha256 vào manifest trước khi dùng.

**YouTube Audio Library:** agent không xem được, vì phải đăng nhập YouTube Studio. Nếu muốn tìm thêm ở đó, dùng các từ khóa `wood block`, `place`, `water drop`, `water lapping`, `subtle whoosh`, và ghi lại loại giấy phép ở cột License.

## Đã đưa vào bản FULL v3 (2026-11-12)
Chủ kênh đã tải các ứng viên vào `sfx/pixabay/` và yêu cầu thêm vào video. Mỗi chỗ, agent chọn **một** file bằng số đo (không nghe được):
- độ dài và điểm bắt đầu;
- nền ồn;
- số tiếng trong file;
- tỉ lệ năng lượng dưới 250 Hz và trên 2,5 kHz;
- với nền nước: độ đều của âm lượng.

Cấu hình ở `audio/sound_plan.json`: nguồn, tác giả, giấy phép đã kiểm trên trang Pixabay ngày 2026-11-12, sha256.

| Thời điểm | Trên hình | File đã chọn | Vì sao (số đo) |
|---|---|---|---|
| 1:13,2 (B05) | Khối bê tông chìm | `water-splosh-38143` (benj500) | Một tiếng duy nhất, sạch, năng lượng dồn ở dải trầm: tiếng "tõm" sâu, không bắn tung. Hai ứng viên kia: một file có 5 tiếng và nhiều tiếng xì; một file nhỏ, sáng hơn |
| 2:26,5 (B09) | Đặt tầng thứ tư | `quiet-thud-hits-100179` (toddcircle), tiếng thứ 5 trong 7 | Thud mềm, trầm, nền ồn thấp hơn 58 dB. `place-something` thu quá nhỏ (đỉnh −18 dBFS), nền ồn tương đối cao hơn |
| 2:44,4 (B10) | Thân phao sâu thêm | `wooden-thud-mono-6244` (Breviceps) | Một tiếng gỗ trầm, rất sạch; trầm hơn B09 và to hơn 2 dB |
| 3:57,8 (B13) | Cầu đi bộ đặt qua khe | `place-100513` (89o) | Một tiếng ngắn, nhẹ, sạch; nhỏ hơn 3 dB |
| 1:04, 3:20, 5:33, 7:02, 7:56, 9:07, 11:41 | Cắt sang chương mới | `soft-luxury-air-whoosh-1` (Sdanezis) | Đường âm lượng mượt nhất trong bộ; gần như không có gì trên 2,5 kHz. Đỉnh đặt 0,1 s trước điểm cắt, trong 1,2 s không có lời |
| 5:33,6–5:45,7 (B17) | Phao nhấp nhô | `water-lapping-gurgling-under-dock-05` (TRP), đoạn 31,8–44,1 s | Đoạn đều nhất của file: đỉnh 0,2 s cao hơn trung vị tối đa 8,8 dB |
| 9:17,0–9:24,9 (B30) | Sóng dài ngoài khơi, tới lúc camera xuống khung ngang | cùng file, đoạn 34,4–42,5 s | Đoạn 8 s đều nhất |

**Mức âm:**
- Tiếng ngắn: đỉnh thấp hơn đỉnh lời dẫn 14 dB, như âm tổng hợp trước đây.
- Nền nước: RMS thấp hơn RMS lời dẫn 26 dB; vào 1 s, ra 1–1,5 s.

**Không dùng:** các file khác trong `sfx/pixabay/` (bút chì, lật trang, xích, boom, whoosh sáng). Lý do ở mục "Không dùng" phía trên.
