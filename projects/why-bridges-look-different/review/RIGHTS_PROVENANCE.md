# Bản kê quyền và nguồn gốc: why-bridges-look-different (revision m8-r3)

- Ngày lập: 2026-10-31, cho bản review nội bộ M8 (đủ sáu họ cầu). Người lập: agent. Đây là bản kê, **không phải tư vấn pháp lý**.
- **Trạng thái duyệt** (chi tiết ở `review/OWNER_APPROVALS.json`):
  - Duyệt claim và chấp nhận phát âm của chủ kênh (2026-10-30) gắn với revision m7-r1, tức bản 4K đã duyệt (git tag `m7-final-4k`, file ở `output/baseline_m7_final_4k/`). Hai duyệt này **không áp dụng** cho m8-r1, m8-r2 hay m8-r3.
  - Duyệt giọng `am_michael` được cấp cho cả dự án và vẫn còn hiệu lực. Chủ kênh có thể xác nhận lại hoặc rút.
  - Vì vậy m8-r3 là **INTERNAL REVIEW**. Nhận xét biên tập của chủ kênh ngày 2026-11-04 là yêu cầu sửa, không phải duyệt (`REV-M8.2-EDITORIAL-REVIEW`).

| Thành phần | Nguồn gốc | Quyền / license | Trạng thái |
|---|---|---|---|
| Lời dẫn (169 câu) | Sinh cục bộ bằng Kokoro-82M (`hexgrad/Kokoro-82M` @ `f3ff3571`, giọng **`am_michael`** SHA256 `9a443b79…`, G2P Anh–Mỹ `lang_code='a'`, speed 1.0, seed 0). Mỗi câu có bản ghi provider, revision, hash và tham số trong `audio/narration_manifest.json` | Apache-2.0 (trọng số, code, giọng). Fallback G2P là GPL, chỉ dùng cục bộ. Các điểm mở về dữ liệu huấn luyện: `docs/licensing/KOKORO_LICENSE_AUDIT.md` §5, §8 | Licence APPROVED theo duyệt của chủ kênh cho dự án (`config/tts_providers.json` → `clearance.voice_approvals`). **Phát âm của m8-r3: PENDING**. Hai mục ghi đè chỉ cho giọng đọc (Corinne, Cincinnati, `script/pronunciation.json`) chờ chủ kênh nghe |
| Kịch bản | Agent viết từ 82 claim đã đối chiếu (`research/sources.json`: 42 claim từ M7, 25 claim M8 cho ba họ cầu nhịp lớn, 14 claim m8-r2 cho các yếu tố, quyết định thực tế và phần kết, 1 claim m8-r3 về cầu Queensboro). m8-r3 thu hẹp 10 claim theo nhận xét của chủ kênh | Nội dung của dự án | **Chưa duyệt biên tập** (`SOURCE_VERIFIED`) |
| Mô hình 3D | Sinh thủ tục trong dự án: dầm gỗ, vòm đá, giàn Pratt/Warren trên site 24 m (M4); **công-xôn, cầu treo, cầu dây văng trên site 72 m (M8)** (`asset_library/architecture/…`) | `generated_in_project` | Mô hình minh họa, có nhãn "Illustrative model". Bộ phận và tỉ lệ chính bám theo NCHRP 25-25(15) §3.1, §3.5, §3.7 và FHWA-IF-12-052 §2.5–2.6 (ghi ở `provenance` của từng asset) |
| Sơ đồ, bản đồ, dòng thời gian, thanh tỉ lệ | Agent vẽ bằng phần tử phẳng (`engine/diagram.py`) từ giá trị trong claim | Của dự án | Có nhãn "Conceptual diagram — not to scale" hoặc "Schematic — not to scale". Card kinh tế nhịp lớn (B53) ghi "After FHWA … 2012" |
| Ảnh: Carrollton Viaduct (HAER MD-9) | William E. Barrett cho HAER, 1970–71; LOC `hhh.md0908`; rendition 3840 px từ Wikimedia Commons | Phạm vi công cộng (PD-USGov-NPS) | `approved`. Chỉ cắt viền phim; trôi chậm |
| Ảnh: Promontory Route Trestle 790B (HAER UT-64) | HAER; LOC `ut0393.photos.367543p`; Commons 3840 px | PD-USGov-NPS | `approved`. Như trên |
| Ảnh: Bollman Truss Bridge (HAER MD-1) | William E. Barrett cho HAER, 1970; LOC `md0583.photos.082178p`; Commons 3840 px | PD-USGov-NPS | `approved`. Như trên |
| Ảnh: Humpback Covered Bridge (HAER VA) | Jack E. Boucher cho HAER, 1971; LOC `va0239.photos.161261p`; Commons 3840 px | PD-USGov-NPS | `approved`. Như trên |
| **Ảnh: Queensboro Bridge (HAER NY-19)** (M8) | Jet Lowe cho HAER, 1991, ảnh chụp từ trên không; LOC `ny0326.photos.348966p`; Commons 3840 px (gốc 5000×4069) | PD-USGov-NPS; trang Commons có template `HABS-source` và liên kết hồ sơ LOC | `approved`. Cắt bỏ viền phim, vệt cửa sổ máy bay và nhãn HAER; trôi chậm |
| **Ảnh: Brooklyn Bridge (HAER NY-18)** (M8) | Ảnh màu chụp trước tháng 11/1982, không rõ người chụp, Jet Lowe scan cho HAER; LOC `ny1234.color.570577c`; Commons 3840 px (gốc 4730×3785) | PD-USGov-NPS; `HABS-source` | `approved`. Cắt lấy tháp và nhịp chính; bỏ viền phim và phần bên phải đường chân trời |
| **Ảnh: Golden Gate Bridge (HAER CA-31)** (m8-r2) | Jet Lowe cho HAER, 1984, ảnh màu; LOC `ca1355.color.570641c`; Commons 3840 px (gốc TIFF 4828×3520) | PD-USGov-NPS; `HABS-source` | `approved`. Cắt bỏ viền phim và nhãn HAER; trôi chậm |
| Chữ trên hình | Font `<builtin>` của Blender 5.2.2 | OFL-1.1 / Bitstream Vera | Như M6: chưa xác định file font cụ thể đứng sau `<builtin>` |
| Phụ đề (SRT + track mov_text) | Chép nguyên văn lời dẫn; thời điểm theo khoảng câu đã đo | Của dự án | — |
| ASR (chỉ dùng cho QA) | `openai/whisper-large-v3-turbo` cục bộ | MIT | Không nằm trong video |
| Nhạc / hiệu ứng âm thanh | **Không có** | — | Chưa có nhạc nào được xác minh quyền, nên không dùng |
| Footage / ảnh khác | **Không có** | — | Không tìm được ảnh phạm vi công cộng phù hợp cho cầu dây văng (ảnh của Không quân Mỹ có máy bay che); chương 8 chỉ dùng mô hình và sơ đồ |

## Nguồn tư liệu mới của M8
- **TRB/NCHRP 25-25(15)** (đã dùng từ M7): §3.5 Suspension, §3.7 Cantilevers, §3.1 Trusses.
- **FHWA, *Steel Bridge Design Handbook: Selecting the Right Bridge Type* (FHWA-IF-12-052, vol. 5, 2012)**:
  - URL gốc của FHWA nay trả 404, còn ROSAP chặn truy cập tự động;
  - PDF tải từ bản lưu của Internet Archive cho đúng URL FHWA;
  - đây là tài liệu của chính phủ liên bang Mỹ;
  - trích dẫn được khớp nguyên văn sau khi bỏ các mảnh chữ watermark "Archived".

- **e-WV: The West Virginia Encyclopedia**, bài "Wheeling Suspension Bridge" của Emory L. Kemp (West Virginia Humanities Council, bản sửa 24/4/2026) (m8-r3): "the longest (1,010 feet) clear span in the world". Chỉ trích dẫn.
- **FHWA-HRT-14-067 (2014)**, *Dynamic Properties of Stay Cables on the Penobscot Narrows Bridge*, chương 3 (m8-r2): số liệu cầu Penobscot Narrows. Là tài liệu của chính phủ liên bang Mỹ; trích dẫn khớp nguyên văn.

## Ghi công và công bố
- Card B35 không có dòng ghi giọng đọc (theo yêu cầu của chủ kênh, 2026-10-30).
- Mô tả YouTube (`review/YOUTUBE_DESCRIPTION.md`) giữ dòng "Narration: AI-generated voice (Kokoro-82M, Apache-2.0; voice am_michael)" như clearance yêu cầu.
- Mỗi card ảnh mang dòng "Photo: …, HAER, Library of Congress (public domain)". QA `image_attribution` kiểm mọi `credit_keys`.

## Không được làm
Không đăng, không upload, không gọi m8-r3 là sẵn sàng xuất bản khi chủ kênh chưa duyệt gói biên tập và phát âm của revision này.
