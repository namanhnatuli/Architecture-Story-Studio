# M6 readiness: từ pilot kỹ thuật đến phim tài liệu đầy đủ đầu tiên

Đề xuất ngắn gọn, dựa trên những gì M2–M5.5 đã kiểm chứng. Không có phần nào dưới đây đã được triển khai.

## 1. Cần thiết hay để sau
| Năng lực M6 | Cho phim đầy đủ đầu tiên | Lý do |
|---|---|---|
| **Lời dẫn tiếng Anh được phép thương mại** (TTS có giấy phép, hoặc giọng người thật) | **Bắt buộc** | G2/G6 chặn mọi audio chưa PUBLICATION_CLEARED. OmniVoice là CC-BY-NC, nên NOT CLEARED. Đây là việc của người dùng (chọn và ký hợp đồng dịch vụ/giọng đọc), agent không tự đăng ký |
| **Lập kế hoạch hình ảnh theo audio đã khóa** (AUDIO_LOCKED đầu cuối) | **Bắt buộc** | Contract đã có (`script/timing.json` → `beat_windows`). Còn thiếu một vòng chạy thật: narrate → ASR → schedule → plan-visuals AUDIO_LOCKED → render → assemble, trên một tập phim |
| **Lớp chú thích / sơ đồ** (nhãn, đường dẫn, kích thước) gắn vào thành phần ngữ nghĩa | **Bắt buộc** | Phim giải thích cần gọi tên chi tiết ngay trên mô hình. Đã có: nhãn SIDE_BY_SIDE/HOLD, thẻ 2D (`engine/diagram.py`), ID thành phần ổn định, frame-space từ `planner/visibility.py` |
| **Mũi tên lực / đường truyền tải** gắn vào thành phần | **Nên có** (EXPLAIN_CAUSE_EFFECT hiện báo MISSING_TEMPLATE FORCE_DIAGRAM) | Cần một contract nói rõ claim nào chứng minh hướng lực. Không được ngầm tuyên bố về độ bền (spec M5) |
| **Nhiều họ công trình trong một phim** | **Nên có** (bắt buộc nếu chủ đề trộn cầu và nhà) | Planner hiện chỉ cho một họ trên một base chung. Cách tối thiểu: nhiều "scene set" trong một dự án, mỗi set có base, camera và nhóm liên tục riêng. Phần đắt là cache và continuity |
| **Bản đồ lịch sử và ảnh tư liệu 2D** | **Để sau, hoặc làm tối thiểu** | Rủi ro license cao nhất. Tối thiểu: thẻ bản đồ tự vẽ từ dữ liệu được phép (ví dụ OpenStreetMap, ODbL, phải ghi nguồn), cộng một sổ ghi asset ngoài |
| Sản xuất phim đầu cuối (8–15 phút) | **Đích của M6** | Ước tính thời gian render bên dưới |

## 2. Module dùng lại được
- `planner/`: beat → kế hoạch, chọn asset, ánh xạ thành phần, mức nhìn thấy L1, sửa kế hoạch, bố cục, đánh giá. Đã có timing AUDIO_LOCKED.
- `engine/`: các template, `camera_focus` cùng bao chuyển động, ghost, nhãn HOLD, QA Blender, `qa_visibility` (L2), `house_layout` (proxy dùng chung).
- `pipeline/`: narration, ASR, pronunciation, subtitles, `beat_scheduler`, gates theo profile (PUBLICATION_CANDIDATE đã có metadata và gate cuối).
- `tools/render_cache.py`: render lại theo shot, khóa theo phụ thuộc.
- `integrations/tts/`: registry nhà cung cấp và hạng quyền. Chỉ cần thêm adapter cho dịch vụ được chọn.

## 3. Data contract mới cần có
| Contract | Nội dung chính |
|---|---|
| `overlay` của shot (`schemas/overlay.schema.json`) | Loại (LABEL, CALLOUT, DIMENSION, FORCE_ARROW, LOAD_PATH), điểm neo = ID thành phần + điểm neo ngữ nghĩa (đỉnh, tâm, mặt), hướng, khoảng thời gian, `claim_ids` (bắt buộc với FORCE_ARROW/LOAD_PATH). Kiểm tra: neo nhìn thấy được (dùng lại L1/L2), không lấn dải phụ đề |
| Sổ asset ngoài (`assets/external_ledger.json`) | URL nguồn, người giữ quyền, license (SPDX nếu có), dòng ghi nguồn, vùng cắt, ngày truy cập, người duyệt. Gate: không được PUBLICATION_CANDIDATE khi còn asset chưa duyệt |
| Scene set (`storyboard/scene_sets.json`) | Nhiều base hoặc họ công trình trong một dự án; mỗi beat thuộc một set; continuity và cache theo từng set |
| Hồ sơ quyền giọng đọc | Đã có (`voice.license`, registry). Thêm số hợp đồng và phạm vi sử dụng (YouTube, kiếm tiền) |

## 4. Rủi ro kỹ thuật
- **Thời gian render.** Pilot M5.5 đo được 0.53 s/frame ở 640×360 trên M4 Pro 24 GB. Một phim 10 phút ở 640×360 (14 400 frame) sẽ mất khoảng 2 giờ (ngoại suy). Ở 1080p, chi phí mỗi frame tăng theo số pixel, nhưng **chưa đo**: cần một benchmark 1080p có giới hạn (một shot ngắn) trước khi lên kế hoạch.
- **Bộ nhớ** không phải điểm nghẽn: khoảng 0.5 GB RSS mỗi tiến trình Blender. Máy M4 16 GB vẫn đủ nếu render tuần tự.
- **Nhiều họ công trình:** continuity camera, cache theo build set, layout so sánh giữa các họ có tỷ lệ rất khác nhau (cầu 24 m và nhà 7 m; xem `ADAPTIVE_COMPOSITION.md`: phải ghi `NORMALIZED`).
- **Mũi tên lực:** dễ ngầm tuyên bố về kết cấu. Mỗi mũi tên phải trỏ về một claim đã duyệt.
- **Lời thoại và hình:** M5.5 đã gặp trường hợp lời thoại nói "side by side" nhưng hình phải trình bày tuần tự. Với AUDIO_LOCKED thì lời thoại không thể sửa nữa, nên cần chạy `plan-visuals` ở chế độ PROVISIONAL **trước** khi thu âm.

## 5. License
- Giọng đọc: dịch vụ TTS có điều khoản thương mại rõ ràng, hoặc người đọc có hợp đồng. Lưu hồ sơ trong `voice.license`, rồi chạy `narrate --purpose publication`.
- Ảnh và bản đồ: chỉ dùng public domain hoặc license cho phép phái sinh và thương mại (ví dụ ảnh của chính phủ Mỹ, CC BY có ghi nguồn, OSM ODbL). Không dùng ảnh "tìm thấy trên mạng". Mọi asset vào sổ trước khi dùng.
- Nhạc (nếu có): thư viện có giấy phép YouTube.
- Claim: duyệt biên tập (EDITORIALLY_APPROVED) bởi người có tên, như quy trình của M3.5.

## 6. Pilot đề xuất cho M6
**"How a bridge carries its load: beam, arch and truss"** (khoảng 8 phút, tiếng Anh).
- Dùng lại ba họ cầu đã kiểm chứng và khu đất chung, nên rủi ro asset thấp.
- Thêm overlay LOAD_PATH: ván → dầm dọc → xà mũ → cột (đường truyền tải đã có trong docstring của bộ sinh), mũi tên nén trong vòng vòm, mũi tên kéo/nén trong giàn. Mỗi mũi tên gắn một claim có nguồn và được duyệt.
- Một hoặc hai bản đồ/ảnh tư liệu public domain (ví dụ bản vẽ HAER của Thư viện Quốc hội Mỹ), qua sổ asset ngoài. Không ngụ ý rằng mô hình minh họa là công trình thật.
- Profile: NARRATED_INTERNAL_REVIEW trong lúc làm, rồi PUBLICATION_CANDIDATE khi có giọng đọc được phép và claim đã duyệt.

Không cần hệ đa agent: luồng hiện tại (tác giả viết beat → planner tất định → engine → QA) là đủ. Thứ còn thiếu là contract và quyền sử dụng, không phải điều phối.
