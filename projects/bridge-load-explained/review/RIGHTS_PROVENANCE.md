# Bản kê quyền và nguồn gốc: bridge-load-explained (M6)

- Ngày lập: 2026-10-29. Người lập: agent. Đây là bản kê, không phải tư vấn pháp lý.
- **Quyết định của chủ kênh (Tran Nam Anh), 2026-10-29:** cấp quyền xuất bản cho Kokoro; duyệt 14 claim (narration `m6-r2`); chấp nhận phát âm; giọng `bm_george`.
- Lời dẫn đã được sinh lại dưới hạng quyền `PUBLICATION_CLEARED`. Nhờ seed cố định, cả 26 câu giống hệt từng bit bản preview.
- Bản MP4 mới là `output/bridge_load_explained_pilot_review.mp4`, không còn hậu tố `_INTERNAL` hay nhãn "not for publication". Bản `_INTERNAL` cũ vẫn nằm trong `output/`, không được commit.
- Profile vẫn là `NARRATED_INTERNAL_REVIEW` cho tới khi chủ kênh chuyển sang `PUBLICATION_CANDIDATE` (cần `publication_metadata`).

| Thành phần trong video | Nguồn gốc | Quyền / license | Trạng thái |
|---|---|---|---|
| Lời dẫn (26 câu, 141,53 s) | Sinh cục bộ bằng Kokoro-82M (`hexgrad/Kokoro-82M` @ `f3ff3571`, `kokoro-v1_0.pth` SHA256 `496dba11…`, giọng `bm_george` SHA256 `f1bc8122…`, do người dùng chọn ngày 2026-10-29, speed 1.0, seed 0). Mỗi đoạn có bản ghi provider, revision, SHA256 model/giọng, tham số và hạng quyền trong `audio/narration_manifest.json` | Trọng số và code là Apache-2.0. Fallback G2P là GPL (chỉ dùng cục bộ). Dữ liệu huấn luyện gồm audio tổng hợp từ TTS đóng. Xem `docs/licensing/KOKORO_LICENSE_AUDIT.md` | **PUBLICATION_CLEARED** (chủ kênh, 2026-10-29). Giọng `bm_george` do chủ kênh chọn; license giọng APPROVED |
| Kịch bản lời dẫn | Agent viết dựa trên claim đã đối chiếu (`research/sources.json`) | Nội dung của dự án | **Đã duyệt biên tập** (chủ kênh, 2026-10-29, narration `m6-r2`) |
| Trích dẫn nguồn | ODOT Manual of Bridge Inspection; FHWA Covered Bridge Manual; FHWA PBES (ch. 2, App. E); SteelConstruction.info "Trusses"; Yale-New Haven Teachers Institute 01.05.08 | Trích ngắn để nghiên cứu/dẫn chứng. Không có văn bản nguồn nào xuất hiện trên hình | Ghi nguồn trong mô tả video khi xuất bản |
| Mô hình 3D (cầu dầm gỗ, cầu vòm đá 3 nhịp, cầu giàn Pratt 2 nhịp, địa hình sông) | Sinh thủ tục trong dự án (`asset_library/architecture/…`, M4), vật liệu thủ tục (`asset_library/materials/stylized_materials.json`) | `generated_in_project` | Mô hình minh họa, không phải thiết kế kỹ thuật |
| Chú thích kỹ thuật (mũi tên, nhãn, đường truyền tải, chú giải) | Hình học phẳng do engine dựng (`engine/annotations.py`) | Của dự án | Khái niệm, có nhãn "Conceptual load path — not to scale" |
| Chữ trên hình | Font dựng sẵn `<builtin>` "Bfont Regular" của Blender 5.2.2. Các font Blender kèm theo: Inter, Noto, Last Resort (SIL OFL-1.1), DejaVu Sans Mono (Bitstream Vera/Arev) | OFL-1.1 cho phép dùng font để dựng chữ trong sản phẩm. Video không phân phối lại file font | Điểm mở nhỏ: chưa xác minh file font cụ thể đứng sau `<builtin>` (dự đoán là Inter) |
| Phụ đề (SRT + track mov_text nếu có) | Chép nguyên văn lời dẫn; thời điểm lấy từ khoảng câu đã đo (Whisper word timestamps chỉ dùng để ngắt dòng) | Của dự án | — |
| ASR kiểm tra (không nằm trong video) | `openai/whisper-large-v3-turbo`, cục bộ | MIT | Chỉ dùng cho QA |
| Nhạc / hiệu ứng âm thanh | **Không có** | — | — |
| Ảnh / footage bên ngoài | **Không có** | — | — |

## Quyết định đã ghi (chủ kênh, 2026-10-29)
1. Cấp quyền xuất bản cho Kokoro: `config/tts_providers.json` → `clearance {cleared_by, cleared_on, evidence, scope}`.
2. Giọng kênh `bm_george`, license giọng APPROVED: `script/narration.json` → `voice.selection`, `voice.license.approved_by/approved_on`.
3. Duyệt biên tập 14 claim: `research/sources.json` → `editorial_approval` (narration `m6-r2`); `factual_review: verified`.
4. Phát âm thuật ngữ được chấp nhận: `voice.pronunciation_review`.

## Còn lại trước khi đăng
- Chuyển `production_profile` sang `PUBLICATION_CANDIDATE` kèm `publication_metadata` (title, description, language, credits), rồi chạy lại `gates`.
- Kiểm tra chính sách YouTube về nội dung tổng hợp tại thời điểm đăng. Ghi "AI-generated narration (Kokoro-82M, Apache-2.0)" trong mô tả.
