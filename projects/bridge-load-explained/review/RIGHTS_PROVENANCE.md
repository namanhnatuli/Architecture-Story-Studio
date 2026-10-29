# Bản kê quyền và nguồn gốc: bridge-load-explained (M6)

- Ngày lập: 2026-10-29. Người lập: agent. **Không có mục nào được người duyệt xác nhận.** Đây là bản kê để người chịu trách nhiệm kênh ra quyết định, không phải tư vấn pháp lý.
- Kết luận chung: **chỉ dùng cho preview nội bộ có lời dẫn** (`production_profile: NARRATED_INTERNAL_REVIEW`; spec M6 gọi là INTERNAL_NARRATED_PREVIEW). Bản MP4 có hậu tố `_INTERNAL` và metadata `comment` ghi "INTERNAL PREVIEW – narration audio rights: PENDING_REVIEW – not for publication".

| Thành phần trong video | Nguồn gốc | Quyền / license | Trạng thái |
|---|---|---|---|
| Lời dẫn (26 câu, 126,58 s) | Sinh cục bộ bằng Kokoro-82M (`hexgrad/Kokoro-82M` @ `f3ff3571`, `kokoro-v1_0.pth` SHA256 `496dba11…`, giọng `bf_emma` SHA256 `d0a423de…`, speed 1.0, seed 0). Mỗi đoạn có bản ghi provider, revision, SHA256 model/giọng, tham số và hạng quyền trong `audio/narration_manifest.json` | Trọng số và code là Apache-2.0. Fallback G2P là GPL (chỉ dùng cục bộ). Dữ liệu huấn luyện gồm audio tổng hợp từ TTS đóng. Xem `docs/licensing/KOKORO_LICENSE_AUDIT.md` | **PENDING_REVIEW**: chưa được cấp quyền xuất bản. Giọng chưa được người dùng duyệt |
| Kịch bản lời dẫn | Agent viết dựa trên claim đã đối chiếu (`research/sources.json`) | Nội dung của dự án | Chưa duyệt biên tập (`review/EDITORIAL_REVIEW_PACKAGE.md`) |
| Trích dẫn nguồn | ODOT Manual of Bridge Inspection; FHWA Covered Bridge Manual; FHWA PBES (ch. 2, App. E); SteelConstruction.info "Trusses"; Yale-New Haven Teachers Institute 01.05.08 | Trích ngắn để nghiên cứu/dẫn chứng. Không có văn bản nguồn nào xuất hiện trên hình | Ghi nguồn trong mô tả video khi xuất bản |
| Mô hình 3D (cầu dầm gỗ, cầu vòm đá 3 nhịp, cầu giàn Pratt 2 nhịp, địa hình sông) | Sinh thủ tục trong dự án (`asset_library/architecture/…`, M4), vật liệu thủ tục (`asset_library/materials/stylized_materials.json`) | `generated_in_project` | Mô hình minh họa, không phải thiết kế kỹ thuật |
| Chú thích kỹ thuật (mũi tên, nhãn, đường truyền tải, chú giải) | Hình học phẳng do engine dựng (`engine/annotations.py`) | Của dự án | Khái niệm, có nhãn "Conceptual load path — not to scale" |
| Chữ trên hình | Font dựng sẵn `<builtin>` "Bfont Regular" của Blender 5.2.2. Các font Blender kèm theo: Inter, Noto, Last Resort (SIL OFL-1.1), DejaVu Sans Mono (Bitstream Vera/Arev) | OFL-1.1 cho phép dùng font để dựng chữ trong sản phẩm. Video không phân phối lại file font | Điểm mở nhỏ: chưa xác minh file font cụ thể đứng sau `<builtin>` (dự đoán là Inter) |
| Phụ đề (SRT + track mov_text nếu có) | Chép nguyên văn lời dẫn; thời điểm lấy từ khoảng câu đã đo (Whisper word timestamps chỉ dùng để ngắt dòng) | Của dự án | — |
| ASR kiểm tra (không nằm trong video) | `openai/whisper-large-v3-turbo`, cục bộ | MIT | Chỉ dùng cho QA |
| Nhạc / hiệu ứng âm thanh | **Không có** | — | — |
| Ảnh / footage bên ngoài | **Không có** | — | — |

## Việc cần một người có tên quyết định trước khi xuất bản
1. Cấp quyền xuất bản cho Kokoro (audit §5): ghi `clearance {cleared_by, cleared_on, evidence}` trong `config/tts_providers.json` và nâng `rights_class`. Agent không được làm việc này.
2. Duyệt giọng kênh sau khi nghe `review/voice_audition/*.m4a`, rồi ghi `approved_by` và `approved_on` vào `script/narration.json`.
3. Duyệt biên tập 14 claim (`review/EDITORIAL_REVIEW_PACKAGE.md` §5).
4. Kiểm tra chính sách YouTube về nội dung tổng hợp tại thời điểm đăng. Đề nghị ghi "AI-generated narration (Kokoro-82M, Apache-2.0)" trong mô tả.
5. Đổi `production_profile` sang `PUBLICATION_CANDIDATE` kèm `publication_metadata`; gate G6 sẽ đánh giá lại.
