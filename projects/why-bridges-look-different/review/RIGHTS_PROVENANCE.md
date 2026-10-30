# Bản kê quyền và nguồn gốc: why-bridges-look-different (M7)

- Ngày lập: 2026-10-30, cập nhật cho bản review nội bộ cuối (giọng `am_michael`). Người lập: agent. Đây là bản kê, **không phải tư vấn pháp lý**.
- **Đã duyệt:** chủ kênh duyệt 41 claim được lời dẫn dùng (2026-10-30, `research/editorial_approval.json`), chọn giọng `am_michael`, và yêu cầu bỏ dòng ghi giọng đọc khỏi card B35.
- **Chưa duyệt:**
  - quyền xuất bản cho giọng `am_michael` (clearance ngày 2026-10-29 chỉ nêu tên 4 giọng Anh–Anh);
  - xác nhận phát âm.

  Vì vậy phim vẫn là **INTERNAL REVIEW**.
- Bản trước dùng `bm_george` được giữ làm mốc: git tag `m7-review-bm_george`; file đầu ra cũ ở `output/baseline_bm_george_m7r1/`.

| Thành phần | Nguồn gốc | Quyền / license | Trạng thái |
|---|---|---|---|
| Lời dẫn (103 câu, 102 đoạn audio) | Sinh cục bộ bằng Kokoro-82M (`hexgrad/Kokoro-82M` @ `f3ff3571`, giọng **`am_michael`** SHA256 `9a443b79…`, G2P Anh–Mỹ `lang_code='a'`, speed 1.0, seed 0). Mỗi câu có bản ghi provider/revision/hash/tham số trong `audio/narration_manifest.json`; không câu nào dùng `bm_george` | Apache-2.0 (trọng số, code, giọng). Không có điều khoản ghi công cho giọng Anh–Mỹ trong VOICES.md. Fallback G2P là GPL, chỉ dùng cục bộ. Các điểm mở về dữ liệu huấn luyện: `docs/licensing/KOKORO_LICENSE_AUDIT.md` §5, §8 | Giọng do chủ kênh chọn (2026-10-30), đã audit. **Licence `LICENSE_REVIEW_REQUIRED`**: chờ chủ kênh mở rộng clearance Kokoro cho `am_michael` (`voices_pending` trong `config/tts_providers.json`) |
| Kịch bản | Agent viết từ 42 claim đã đối chiếu (`research/sources.json`) | Nội dung của dự án | **Chưa duyệt biên tập** (`SOURCE_VERIFIED`) |
| Mô hình 3D (cầu dầm gỗ, vòm đá 3 nhịp, giàn Pratt/Warren 2 nhịp, địa hình sông) | Sinh thủ tục trong dự án (M4, `asset_library/architecture/…`) | `generated_in_project` | Mô hình minh họa. Khi đứng cạnh cầu có thật thì mang nhãn "Illustrative model, not the …" (B27, B29) |
| Sơ đồ, bản đồ, dòng thời gian, thanh tỉ lệ nhịp | Agent vẽ bằng phần tử phẳng (`engine/diagram.py`) từ giá trị trong claim | Của dự án | Có nhãn "Conceptual diagram — not to scale" hoặc "Schematic — not to scale". Riêng thanh nhịp vẽ đúng tỉ lệ theo giá trị NCHRP |
| Ảnh: Carrollton Viaduct (HAER MD-9) | William E. Barrett cho HAER, 1970–71; LOC `hhh.md0908`; bản 1920 px từ Wikimedia Commons | Phạm vi công cộng (PD-USGov-NPS); trang Commons có rights advisory của LOC "No known restrictions on images made by the U.S. Government" | `approved` (hồ sơ đủ trường). Chỉ cắt viền phim; trôi chậm; không chỉnh sửa |
| Ảnh: Promontory Route Trestle 790B (HAER UT-64) | HAER; LOC `ut0393.photos.367543p`; Commons | PD-USGov-NPS (rights advisory của LOC không có trong mô tả trên Commons; không đọc được loc.gov do HTTP 403) | `approved`. Như trên |
| Ảnh: Bollman Truss Bridge (HAER MD-1) | William E. Barrett cho HAER, 1970; LOC `md0583.photos.082178p`; Commons | PD-USGov-NPS; có rights advisory của LOC trên Commons | `approved`. Như trên |
| Ảnh: Humpback Covered Bridge (HAER VA) | Jack E. Boucher cho HAER, 1971; LOC `va0239.photos.161261p`; Commons | PD-USGov-NPS (rights advisory không có trong mô tả trên Commons) | `approved`. Như trên |
| Chữ trên hình | Font `<builtin>` của Blender 5.2.2 | Font Blender kèm theo dùng OFL-1.1 / Bitstream Vera | Như M6: chưa xác định file font cụ thể đứng sau `<builtin>` |
| Phụ đề (SRT + track mov_text) | Chép nguyên văn lời dẫn; thời điểm theo khoảng câu đã đo | Của dự án | — |
| ASR (chỉ dùng cho QA) | `openai/whisper-large-v3-turbo` cục bộ | MIT | Không nằm trong video |
| Nhạc / hiệu ứng âm thanh | **Không có** | — | Chưa có nhạc nào được xác minh quyền, nên không dùng |
| Footage / ảnh khác | **Không có** | — | Ảnh Cornish–Windsor bị loại: nguồn là người tải lên Commons, không phải hồ sơ liên bang |

## Ghi công và công bố
- **Dòng "Narration: AI-generated voice (Kokoro-82M, voice bm_george)" đã bỏ khỏi card B35** theo yêu cầu của chủ kênh (2026-10-30). Không còn chữ nào trên hình nhắc tới giọng đọc.
- Kokoro (Apache-2.0) **không** yêu cầu ghi công cho audio tạo ra, nên bỏ dòng này không vi phạm giấy phép nào.
- Phạm vi clearance Kokoro yêu cầu "disclose AI-generated narration". Việc công bố này **vẫn còn** trong bản nháp mô tả (`review/YOUTUBE_DESCRIPTION.md`: "Narration: AI-generated voice (Kokoro-82M, Apache-2.0; voice am_michael)"). Metadata MP4 chỉ có nhãn INTERNAL REVIEW. Khi đăng, phải giữ dòng này trong mô tả.

## Ghi công bắt buộc
- Mỗi card ảnh mang dòng "Photo: …, HAER, Library of Congress (public domain)". Card cuối ghi "Historic American Engineering Record, Library of Congress Prints & Photographs Division (public domain)". QA `image_attribution` kiểm mọi `credit_keys`.
- Mô tả YouTube (bản nháp `review/YOUTUBE_DESCRIPTION.md`) ghi nguồn, ghi công ảnh, nói rõ lời dẫn do AI tạo và mô hình chỉ để minh họa.

## Không được làm
Không đăng, không upload và không gọi phim là sẵn sàng xuất bản khi chủ kênh chưa duyệt gói biên tập và chưa xác nhận giọng cho phim này.
