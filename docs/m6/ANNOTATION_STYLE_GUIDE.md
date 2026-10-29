# Hướng dẫn phong cách chú thích kỹ thuật (M6)

Cấu hình: `config/annotation_style.json`. Bố cục: `engine/annotation_layout.py`. Mọi kích thước tính theo tỷ lệ **chiều cao khung hình**.

## 1. Nguyên tắc
1. **Không bịa số liệu.** Không có nội lực, sức chịu tải, hệ số an toàn, ứng suất, độ võng hay so sánh định lượng nào. Mọi đồ họa về lực đều là *khái niệm*. Hễ khung hình có đồ họa lực là có thẻ **"Conceptual load path — not to scale"**.
2. **Độ dài mũi tên không mang nghĩa.** Mọi mũi tên tải và phản lực dài 0,085, thân 0,0065. Kích thước không bao giờ biểu diễn độ lớn.
3. **Không vẽ mũi tên chỉ vì trông có vẻ giáo dục.** Mỗi LOAD_ARROW, REACTION_ARROW, CONCEPTUAL_LOAD_PATH, TENSION_COMPRESSION_LEGEND, hay CALLOUT có `force`, phải trích một claim:
   - claim ở mức SOURCE_VERIFIED trở lên và có nguồn;
   - đã được kể ở beat này hoặc beat trước;
   - `applies_to` gồm loại cầu đang chiếu;
   - với phát biểu nén/kéo: `components` của claim phải chứa đúng khái niệm đích.
   
   Ví dụ, gắn "tension" cho thanh xiên bằng CLM_613 (chỉ nói về chord) sẽ bị từ chối.
4. **Không tô màu từng thanh giàn** theo kéo/nén. Pilot chỉ gọi tên biên trên và biên dưới (CLM_613, giả định nhịp giản đơn). Thanh bụng chỉ được gọi tên chung là "Web members".
5. **Chú thích không chạm hình học kiến trúc.** Chúng nằm trên các mặt phẳng ngay trước camera trực giao, emission phẳng, không đổ bóng. Phụ đề không bao giờ nằm trong cảnh 3D.

## 2. Loại chú thích
| Loại | Hình | Bắt buộc |
|---|---|---|
| COMPONENT_LABEL | Nhãn trên nền sáng + đường dẫn + chấm tại điểm neo | `target`, `text` ≤ 28 |
| CALLOUT | Như nhãn; có `force` thì kèm ký hiệu lực | `text` ≤ 36; `force` cần claim |
| LOAD_ARROW | 1–5 mũi tên thẳng **xuống**, cam, rải đều trên phần nhìn thấy của đích | claim |
| REACTION_ARROW | Mũi tên xanh, `UP` hoặc `UP_INWARD` (35°, hướng về giữa đích), đặt dưới điểm neo | claim |
| CONCEPTUAL_LOAD_PATH | Đường đứt nét cam (LOAD) hoặc liền đỏ (COMPRESSION), mỗi đoạn một đầu mũi tên. `path` gồm các nhánh điểm neo; `along` chạy qua tâm các viên, từ giữa ra hai đầu | claim |
| TENSION_COMPRESSION_LEGEND | Ô góc trên phải: "Conceptual forces", nén →← (pushed), kéo ←→ (pulled) | claim |
| HIGHLIGHT_REGION | Khung đứt nét quanh phần nhìn thấy của đích + nhãn | `text` |

Màu (Okabe-Ito, tương phản trên nền #EDEBE5):
- tải #C25110;
- phản lực #1E5C96;
- nén #A3263A;
- kéo #16756F;
- chữ #24231F trên nền #FBF9F4 có viền.

Mỗi loại lực còn khác nhau về **hình dạng**, nên màu không bao giờ là dấu hiệu duy nhất. Đường kẻ và mũi tên có viền sáng (halo) để đọc được trên phần tối.

## 3. Điểm neo
- Đích là khái niệm từ vựng (+ `group`, + `pick` theo vị trí trên màn hình). Ví dụ `{"concept": "truss_chord", "group": "truss_south", "pick": "LEFTMOST"}`.
- Điểm (`TOP`, `BOTTOM`, `CENTER`, `LEFT`, `RIGHT`, các góc) được chọn trên **silhouette nhìn thấy được** của đích, trong raster offline 384×216 có độ sâu:
  - TOP/BOTTOM lấy ở các cột giữa;
  - điểm phải cách mép ít nhất 2 bước raster;
  - đích đang bị làm mờ (ghost) vẫn được tính, vì người xem nhìn xuyên thấy nó.
- Điểm neo lưu cả tọa độ thế giới lẫn tọa độ khung hình. `validate-plan` kiểm phép chiếu. QA Blender bắn tia qua điểm neo và yêu cầu chạm chính bộ phận đích trước.
- Bộ phận đang chuyển động (ví dụ trong exploded view) chỉ được chú thích khi đứng yên. Khung thời gian tự thu về đoạn tĩnh dài nhất, như B4 (đoạn giữ khi các viên đá tách ra).

## 4. Thời điểm
- Chú thích xuất hiện 0,1 s trước câu `sentence` của nó, fade 0,3 s, giữ tới hết beat hoặc tới câu `until`. Chú thích của câu trước và câu sau không bao giờ cùng lúc hiện.
- Hiển thị tối thiểu 1,2 s. Glow có thể đồng bộ bằng `highlight_at_sentence`.

## 5. Bố cục
- Vùng an toàn: x 0,045–0,955, y 0,05–0,95. **Vùng phụ đề: y < 0,17, không chú thích nào được vào.**
- Tìm chỗ đặt theo vòng khoảng cách (0,07…0,28) × hướng ưu tiên (lên trước). Bị loại nếu: chồng lên chữ đang hiện, chồng lên chú giải, thẻ hay tiêu đề, chồng lên đích của chính nó, hoặc leader cắt qua chữ khác. Đoạn thẳng của mũi tên và đường dẫn được kiểm theo đúng đoạn, không theo khung bao.
- Không đặt được thì chú thích FAILED, beat không chạy được (fail closed). Planner không bao giờ âm thầm bỏ một mũi tên.
- Chữ: Bfont của Blender, cao 0,036 (19 px ở 540p). QA đo bề rộng chữ thật trong Blender và so với nền.

## 6. Lời dẫn và hình phải khớp (`planner/consistency.py`)
| Luật | Lời dẫn | Điều kiện |
|---|---|---|
| SIMULTANEOUS | "side by side", "at once", "seen/shown/all … together"… | Phải có shot SIDE_BY_SIDE trong lúc câu được đọc. Chữ "together" đứng một mình không tính |
| SEQUENTIAL | "one at a time", "one by one", "each in turn" | Không có SIDE_BY_SIDE |
| DEICTIC | "this/that component/part/member/…" | Có glow hoặc chú thích đang trỏ |
| COLOUR | tên màu | Có đồ họa màu đó đang hiện |
| SIDE | "left"/"right" | Báo UNCERTAIN kèm vị trí các chú thích; người duyệt xác nhận |
| TRANSFORMATION | "turns into", "becomes", "is replaced by"… | Không có cắt cứng giữa hai công trình khác nhau trong câu |
| ARROWS | "these arrows" | Mũi tên đang hiện. "the arrows" chung chung thì báo UNCERTAIN |

Mâu thuẫn là lỗi của `validate-plan` và làm plan không chạy được. Ví dụ đã sửa: bridge-story-m5 B7 "Side by side, …" đổi thành "Let's compare them one at a time: …".
