## Trạng thái

Đây là revision g-r3 và bản video **internal review 720p**. Bạn yêu cầu dựng mô hình và dựng bản review nên tôi làm tiếp, nhưng **chưa có gì được duyệt**: claim, giọng đọc, phát âm và xuất bản vẫn chờ bạn. Chưa render 4K, chưa tải ảnh thật, chưa đăng gì.

- Video: `output/gothic_cathedral_heights_G_R3_INTERNAL_REVIEW_720p.mp4` và `.en.srt`, 15:23.
- Xem lại có mốc thời gian: `qa/EDITORIAL_REVIEW_TIMECODED.md`.
- Lời dẫn không đổi so với g-r3 nên không đọc lại.

## Câu chuyện trong năm dòng

1. Mở bằng năm 1284: phần vòm cao nhất thời Trung Cổ ở Beauvais sập, sau đó đặt câu hỏi của phim.
2. Vấn đề: đá gần như không chịu được kéo, còn vòm thì đẩy ra ngoài. Một kiểu nhà thờ Romanesque vòm nôi đáp lại bằng tường và trụ dày.
3. Ba công cụ Gothic bố trí lại hệ đỡ: vòm nhọn, vòm gân, trụ chống bay. Tường không còn là chỗ đỡ chính của vòm, nên có thể mở ra đón ánh sáng.
4. Thợ xây làm bằng hình học, kỹ năng nghề và kinh nghiệm, không có phép tính kết cấu hiện đại. Beauvais đi quá giới hạn, còn Amiens phải cứu bằng xích sắt.
5. Kết luận: đá hiếm khi hỏng vì yếu, mà thường vì mất ổn định, nên hình dạng và tỉ lệ giải thích được nhiều điều. Mô hình giúp hiểu vai trò của tỉ lệ, nhưng tự nó không chứng minh một công trình thật an toàn. Độ cao không hề "bất khả thi", và đây cũng không phải câu chuyện tiến bộ đơn giản.

## Đã làm theo nhận xét lần ba

| Điểm | Đã làm |
|---|---|
| B40: sửa và kiểm chứng phép tính giới hạn sập | Viết lại theo đúng phương pháp của chương trình ArchSpread trong luận án Ochsendorf 2002: đo nhịp ở mặt trong vòm, khớp mặt trong dịch về đỉnh vòm khi gối dịch ra, sập khi đường áp lực chạm mặt ngoài ở gối. Xem bảng dưới |
| Nguồn cho Cluny | Thêm Harvard (Loeb Library), New Catholic Encyclopedia và trang của di tích (CMN). `CLM_131` lên mức `high` |
| Nguồn cho Beauvais ba gian thành sáu | Thêm hai trang của Stephen Murray ở Columbia: "transforming three bays into six and quadripartite vaults to sexpartite". `CLM_185` lên mức `high` |
| Playbook | Thêm bước bắt buộc "lời và hình có khẳng định vượt quá bằng chứng không?" |
| Mô hình | Họ `cathedral` mới: mặt cắt Gothic và Romanesque vòm nôi, đều là minh họa, không dựng lại công trình thật nào |
| Video | Bản 720p đủ 47 shot |

**Tin nhắn của bạn không kèm đường dẫn nguồn**, nên các nguồn trên là tôi tự tìm. Nếu bạn đã có nguồn khác, xin gửi để tôi đối chiếu.

## B40: kết quả kiểm chứng

| So sánh | Số đã công bố | Tôi tính lại |
|---|---|---|
| Ochsendorf 2002, Bảng 5.3, t/R 0,10, α 60°, voussoir 0,1°: khớp mặt trong | 53,8° → 42,7° | 53,8° → 42,8° |
| Cùng dòng đó: nhịp tăng khi sập | +8,2% | +8,20% |
| Cùng dòng đó: lực đẩy khi sập | 2,16 Hmin | 2,16 Hmin |
| Cùng dòng đó: độ tụt đỉnh | 1,73t | 1,71t |
| Luận án, t/R 0,1075, α 80° và 60° | 54,5→52,2° và 54,5→43,2° | khớp cả hai |
| Block và cộng sự 2006, Hình 4(a): lực đẩy | 16–25% | 16,2–24,4% |
| Block 2006, Hình 5 (t/R 15,24%, 160°): Hmin | 19,80% | 19,66% |
| Hình 5: nhịp +5,00% thì lực đẩy tăng | +24,59% | +22,6% |
| Hình 5: giới hạn sập, nhịp | +11,49% | +11,17% |
| Hình 5: giới hạn sập, lực đẩy | +85,10% | +83,8% |
| Hình 5: vị trí khớp | 54,4° | 53,9° |

Số 0,9.8 trong `CHANGELOG.md` (+10,6%, +86%) là của phép tính cũ, đã sai.

**Những chỗ còn lệch, xin biết để quyết định:**

- Với voussoir 1–10°, nhịp khớp nhưng vị trí khớp lúc sập lệch: tôi ra 43–50°, luận án 40–42°. Phim dùng trường hợp voussoir nhỏ, đúng phần khớp tốt.
- Kết quả hơi đổi theo số bước tính: 8,20% với 1.000 bước (số bước của chương trình gốc), 7,82% với 20.000 bước.
- **Tôi không phải kỹ sư kết cấu.** Khớp số đã công bố không thay thế việc một người có chuyên môn đọc `script/arch_statics.py`. Phim không đọc số nào ở trên; hình ghi rõ "One idealized arch, self-weight only". Test `GothicThrustLineTest` giữ các so sánh này.

## Tôi tự thêm, xin bạn xem lại

1. **B07, B12, B23 chuyển từ card sang 3D.** Lý do là chuỗi 2D quá dài theo QA và nhận xét của bạn về card chữ, không phải để giảm tỉ lệ 2D.
2. **Sửa sau khi tự xem bản dựng đầu** (bảng đầy đủ ở `qa/EDITORIAL_REVIEW_TIMECODED.md`):
   - B12–B13: camera nhảy, gân và web cùng sáng rồi lẫn vào nhau, khung để lộ chân trụ.
   - B09, B10, B21, B25, B41: hình gần như trống trong lúc đang có lời.
   - B19: 31 giây nói về cờ bay mà không chỉ ra cờ bay.
   - B18: ghi chú "same scale" khiến hai mô hình trông như một phép đo. Đã đổi thành "Illustrative models, not measured buildings".
3. **Code dùng chung mới:** `THRUST_ARROW`, `close_on`, `close_on_targets`, `glow_only`, `state_targets`, `same_scale`, hai preset camera, vật liệu `stained_glass` và `roof_lead`. Sửa một lỗi ở planner: `close_on_targets` trước đây không truyền khung hình để so kiểu cắt.
4. **Claim thu hẹp từ lần trước** (`CLM_143`, `CLM_156`, `CLM_157`, `CLM_161`, `CLM_185`, `CLM_190`, `CLM_191`) vẫn giữ nguyên.

## Cần bạn quyết định

1. **Duyệt lời dẫn và claim.** Bạn viết g-r3 "đủ tốt để duyệt phần lời", tôi hiểu là cho phép làm tiếp, chưa phải duyệt chính thức, nên chưa ghi vào `review/OWNER_APPROVALS.json`. Nếu bạn duyệt, xin nói rõ phạm vi.
2. **9 claim đang ở mức `medium`:** `CLM_102`, `CLM_104`, `CLM_120`, `CLM_130`, `CLM_140`, `CLM_143`, `CLM_152`, `CLM_184`, `CLM_186`. Chi tiết ở bảng cuối tài liệu. Vài mục chỉ dựa vào Association Beauvais Cathédrale, một hội bảo tồn: `CLM_120` (ví von cánh cung), `CLM_143`, `CLM_152` (đường lực qua trụ chống bay), `CLM_184`. Tôi không mở được Britannica, UNESCO, Smarthistory, The Met và bài MDPI 2025; không có bản sao lưu nào được dùng để lách.
3. **Giọng.** `am_michael` mới được bạn duyệt riêng cho phim cầu. Hiện dự án này ở trạng thái `LICENSE_REVIEW_REQUIRED`.
4. **Phát âm (chỉ bạn xác nhận được).** 6 mục đang `PENDING_LISTENING_REVIEW`: Beauvais (boh-VAY), Amiens (am-YAN), Suger (soo-ZHAIR), Cluny (KLOO-nee), Notre-Dame (NOH-truh DAHM), Viollet-le-Duc (vyoh-LAY luh DOOK). Tôi không nghe được audio; ASR đạt không chứng minh phát âm đúng.
5. **Đơn vị.** Phim dùng mét, phim cầu trước dùng feet. Lời dẫn và phụ đề dùng chính tả Mỹ (`meters`).
6. **Ảnh thật.** Phim chưa có ảnh nào. Ảnh Saint-Denis, Chartres, Notre-Dame, Amiens và Beauvais sẽ giải quyết điểm yếu lớn nhất: cùng một mô hình, cùng một góc, lặp ở 14 shot. Mỗi ảnh cần hồ sơ quyền đầy đủ. Bạn muốn tôi tìm ảnh có quyền rõ ràng không?
7. **B35 (10:47–11:19):** 31 giây chỉ có chữ. Giữ nguyên hay thay bằng mô hình sáng từng bộ phận theo từng giả thuyết?
8. **Vệt bóng mềm trên trụ ở B12–B13.** Sửa đúng cách là đổi ánh sáng, và việc đó buộc render lại cả phim. Tôi đề nghị làm cùng lần render lớn tiếp theo.
