# M5.5: bố cục so sánh thích ứng

M5 so sánh ba cây cầu bằng một khung SIDE_BY_SIDE STACK: mỗi cầu chỉ khoảng 190 px chiều ngang ở 640×360, và thanh giàn mảnh hơn 2 px. M5.5 **đo** các bố cục ứng viên offline rồi chọn bố cục rõ nhất mà mục đích của câu chuyện cho phép. Khi không bố cục đồng thời nào đọc được, planner tự chuyển sang so sánh tuần tự. Không phải chỉ lùi camera ra xa, và cũng không có hệ render riêng: vẫn là các template SIDE_BY_SIDE và HOLD có sẵn.

## 1. Đo một bố cục (`planner/composition.py`)
Mỗi ứng viên được dựng thành một cảnh offline bằng chính phép layout của engine (`framing.layout_stack`, `layout_side_by_side`, `fit_ortho`, dải nhãn). Các số đo:

| Chỉ số | Cách tính |
|---|---|
| Kích thước mô hình | Khung bao trên màn hình của từng mô hình: rộng, cao, diện tích chiếm, số px chiều ngang ở **độ phân giải tham chiếu** (640×360 = màn hình nhỏ/điện thoại, cấu hình được) |
| px/m | Độ rộng khung (px) / `ortho_scale`: cùng một tỷ lệ cho mọi mô hình trong khung |
| Chi tiết (`detail_px`) | Trung vị của **cạnh nhỏ nhất** trong khung bao của các thành phần riêng của mô hình (gỗ 0.30 m, đá 0.74 m, giàn 0.20 m) × px/m: thành phần điển hình của mô hình rộng bao nhiêu px |
| Cắt khung, chồng lấn, dải nhãn | Khung bao vượt ra ngoài khung hình; các mô hình chồng lên nhau trên màn hình; mô hình lấn vào dải nhãn/phụ đề; nhãn STACK đụng hàng bên dưới |
| Tỷ lệ | `COMMON`: mọi mô hình cùng một camera. Không bố cục nào chuẩn hóa từng mô hình riêng, nên không bao giờ ngầm gợi ý một so sánh kích thước sai |

**Mục đích** (`config/visual_planning.json` → `composition.purposes`, theo ý đồ):
- `detail` (COMPARE_VARIANTS): thành phần điển hình ≥ **2.5 px** và mô hình nhỏ nhất ≥ 25 % chiều rộng khung. Hiệu chỉnh trên frame thật: thanh giàn 1.3–1.5 px trong STACK 3 cầu không đọc được; 3.9 px trong khung một cầu thì đọc được.
- `overview` (SUMMARIZE_DIFFERENCES): chỉ cần hình dáng tổng thể, tức mô hình nhỏ nhất ≥ 25 % chiều rộng.

## 2. Chiến lược bố cục
| Chiến lược (spec) | Trong planner | Khi nào |
|---|---|---|
| SIDE_BY_SIDE_STACK / SIDE_BY_SIDE_ROW | `COMPARE_SIDE_BY_SIDE`: ứng viên STACK (gap 0.5, 0.25) và ROW (gap 0.35, 0.2); chọn ứng viên đọc được có chi tiết lớn nhất, rồi mô hình lớn nhất, rồi theo thứ tự | Khi có bố cục đồng thời đọc được |
| FOCUSED_PAIR | `FOCUSED_PAIR`: chỉ hai trạng thái mà beat nêu trong `focus_states` | Beat có ≥ 3 trạng thái nhưng chỉ nói về một cặp |
| DETAIL_THEN_OVERVIEW | `DETAIL_THEN_OVERVIEW`: từng mô hình một (chi tiết), rồi một khung tổng (overview) | Khi đủ thời gian (N × 2 s + 2 s) |
| SEQUENTIAL_COMPARISON | `SEQUENTIAL_COMPARISON`: mỗi mô hình một shot HOLD có **nhãn** (`animation.label`, mới), cùng **một** camera khóa (một nhóm liên tục, cùng tập variant được dựng), cắt cứng giữa các mô hình | Khi không bố cục đồng thời nào đọc được |
| SINGLE_MODEL_HIGHLIGHT | `HOLD_HIGHLIGHT` có sẵn | Beat chỉ nói về một mô hình |
| (M5) | `CONTINUE_COMPARISON` giữ nguyên bố cục của shot trước (cắt match) nếu nó đọc được cho mục đích hiện tại | — |

Nếu lời thoại nói "side by side / together / at once" mà planner phải chuyển sang so sánh tuần tự, báo cáo coverage ghi rõ điều này và gợi ý sửa lời thoại. Planner không bao giờ tự sửa câu chữ.

## 3. Kết quả đo (640×360, preset BRIDGE_STACK / BRIDGE_THREE_QUARTER / LOCKED_THREE_QUARTER)
| Bố cục | 3 cầu: thành phần nhỏ nhất | 3 cầu: mô hình nhỏ nhất (rộng) | 2 nhà: thành phần nhỏ nhất | 2 nhà: mô hình nhỏ nhất |
|---|---|---|---|---|
| STACK gap 0.5 (M5) | 1.3 px | 30 % | 14.9 px | 17 % |
| STACK gap 0.25 | 1.5 px | 34 % | 16.8 px | 19 % |
| ROW gap 0.35 | 1.1 px | 24 % | **31.9 px** | **35 %** |
| ROW gap 0.2 | 1.1 px | 27 % | 31.9 px | 35 % |
| Tuần tự (một camera) | **3.9 px** (giàn), 5.8 (gỗ), 14.3 (đá) | **88 %** | 33.7 px | 37 % |

Kết quả:
- **B7** (so sánh, `detail`): không bố cục đồng thời nào đạt. DETAIL_THEN_OVERVIEW cần 8.04 s, nhưng beat chỉ có 6.21 s. Planner chọn **SEQUENTIAL_COMPARISON**: SC_012 gỗ → SC_013 đá → SC_014 giàn, 2.07 s mỗi cầu. Cả ba có cùng `ortho_scale` 33.11 (đo trong Blender), nhãn nằm trong dải, và cùng tỷ lệ.
- **B8** (tóm tắt, `overview`): STACK gap **0.25** (34 % chiều rộng, so với 30 % ở M5), các phần khác nhau phát sáng.
- **Mái R4**: ROW gap 0.35 vẫn đọc được (thành phần 31.9 px), không cần dự phòng. Kết quả giống M5. Logic không phụ thuộc họ cầu: công trình gọn giữ ROW, công trình dài chuyển sang tuần tự.

Ảnh trước/sau render thật: `projects/bridge-story-m5/qa/m55_before_after/` (xem `docs/m5_5/M5_5_QA_REPORT.md`).

## 4. Giới hạn
- Độ rộng "thành phần điển hình" là một đại lượng thay thế thô (trung vị cạnh nhỏ nhất). Nó không biết chi tiết nào thật sự quan trọng cho câu chuyện.
- Độ phân giải tham chiếu 640×360 là lựa chọn bảo thủ cho màn hình nhỏ. Ở 1920×1080, STACK ba cầu đạt ngưỡng (có test), nên quyết định phụ thuộc vào cấu hình này.
- Chưa có bố cục kiểu "khung trong khung" (inset) hay phóng chi tiết một phần trong khung so sánh.
