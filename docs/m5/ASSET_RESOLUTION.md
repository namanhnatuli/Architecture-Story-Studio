# Chọn asset (M5): khái niệm → asset → thành phần ngữ nghĩa

`planner/resolver.py` (asset), `planner/catalog.py` (chỉ mục chỉ đọc), `planner/mapper.py` (thành phần). Không file nào ghi vào `asset_library/`; có test kiểm tra catalog giống từng byte trước và sau khi lập kế hoạch.

## 1. Từ vựng (`config/visual_vocabulary.json`)
| Loại | Ví dụ | Trường |
|---|---|---|
| `site` | `river_crossing_site` | `family: site`, `variant` |
| `architecture` | `timber_beam_bridge`, `five_arch_stone_bridge` (`where: {arch_count: 5}`), `pratt_truss` / `warren_truss` (`truss_pattern`), `low_pitch_gable_roof` (`roof_pitch_degrees ≤ 30`), `steep_gable_roof` (`≥ 40`) | `family`, `variant`, `where` (bằng nhau, hoặc `{min, max}`), `supported: false` cho họ chưa có bộ sinh (`suspension_bridge`, `cable_stayed_bridge`, `cantilever_bridge`) |
| `component` | `voussoir`, `keystone`, `arch_ring`, `deck_planks`, `stringer`, `cap_beam`, `diagonal_members`, `truss_web`, `rafters`, `ridge_beam`, `roof_covering`… | `roles`: role ngữ nghĩa M4 (`type` viết thường) hoặc role mái M2; `ambiguous_if_multiple` cho khái niệm chung chung (`beam`, `member`); `ghost_roles` là role của các phần thường che nó (`stringer` → `plank`) |

Thêm khái niệm là thêm **cách gọi tên**, không thêm hình học. Một khái niệm công trình chỉ thực thi được khi có asset khớp, hoặc khi bộ sinh của họ/biến thể đó sinh được tham số yêu cầu.

## 2. Chỉ mục asset (`catalog.index`)
- **Thư viện M4:** mọi spec hợp lệ trong `asset_library/architecture/**`, kèm tham số đã resolve và trạng thái kiểm tra: `VALIDATED` khi các kiểm tra offline và kiểm tra Blender review trong `catalog.json` đều PASS, nếu không thì `OFFLINE_ONLY`.
- **Adapter tương thích (mái nhà M2):** các variant `gable_roof` trên base `rectangular_house_base` trong `projects/*/storyboard/states.json`, với ID `legacy_<project>_<variant>` và tham số `roof_pitch_degrees`, `color_key`, `covering_style`. Variant được `VALIDATED` khi `qa/blender_checks.json` của dự án đó không có lỗi. Khi dùng, variant được **chép** vào states của dự án mới; dự án nguồn không bị sửa. Kế hoạch do planner sinh (`generated_by: planner`) không bao giờ được dùng làm nguồn.

## 3. Thuật toán (`resolver.resolve`)
1. Khái niệm không có trong từ vựng → `UNKNOWN_CONCEPT` (coverage `MISSING_ASSET`, kèm lời nhắn thêm khái niệm vào từ vựng).
2. Họ hoặc biến thể chưa có bộ sinh (`supported: false`) → `NEW_ASSET_REQUIRED`, kèm **spec nháp** và **nhiệm vụ** `NEW_FAMILY_GENERATOR`: viết bộ sinh, đăng ký `FAMILIES`, preset bung, test, `asset-check`, `asset-render`. Ước tính 1–3 ngày cho một dạng minh họa giản lược. **Không thay bằng asset khác.**
3. Ứng viên: cùng họ, cùng biến thể, khớp `where`. Với cầu, asset phải khớp khu đất chung: chiều dài bằng khe sông, cao độ mặt cầu bằng cao độ bờ.
4. Độ chính xác: nếu beat cần `REFERENCE_BASED` hoặc `HISTORICALLY_VERIFIED` mà mọi ứng viên chỉ là `ILLUSTRATIVE` → `BLOCKED_MISSING_EVIDENCE`. Asset sinh mới luôn là ILLUSTRATIVE, nên cũng không thay được cho asset chính xác.
5. Xếp hạng tất định: `VALIDATED` trước `OFFLINE_ONLY`; thư viện trước adapter; ít tham số lệch khỏi mặc định của họ hơn; cuối cùng theo `asset_id`. Kết quả là `REUSE_EXISTING` (thư viện) hoặc `ADAPT_EXISTING_ASSET` (adapter). Lời giải thích liệt kê các ứng viên bị xếp sau.
6. Không ứng viên nào khớp, nhưng họ/biến thể có bộ sinh → `GENERATE_FROM_SUPPORTED_FAMILY`. Tham số = mặc định của họ + `where` + kích thước khu đất. ID là `<họ>_<biến thể>_gen_<sha6 của tham số>` (tất định). Spec phải qua `assets.validate`; nếu không qua thì `NEW_ASSET_REQUIRED` kèm lỗi. Spec được ghi vào `projects/<slug>/planning/generated_assets/`, **không** ghi vào catalog. Ví dụ có test: cầu đá 4 vòm (khái niệm SYNTHETIC chỉ có trong test) được sinh, vào kế hoạch, qua `validate-plan` và G0, còn catalog không đổi.

Hai khái niệm resolve ra cùng một asset thì dùng chung một trạng thái. Ví dụ `steel_truss_bridge` (B5) và `pratt_truss` (B6) đều là `bridge_steel_truss_pratt_01`, nên B5 → B6 là cắt match trên cùng mô hình.

## 4. Khung chung (`structure_from`)
Sau khi resolve, `Model.link_frames` nối hai trạng thái thư viện khi chúng cùng họ, cùng biến thể và chỉ khác nhau ở `replaceable_params` (ví dụ `truss_pattern`). Trạng thái sau kế thừa khung (các thành phần không có `REPLACE`) từ trạng thái trước. REPLACE_PARTS khi đó chỉ thay phần bụng giàn. Đây là điều kiện duy nhất để thay thế giữa hai mô hình thư viện. Hai họ khác nhau không bao giờ được thay thế cho nhau.

## 5. Thành phần ngữ nghĩa (`mapper.resolve_targets`)
- Ghép theo **metadata ngữ nghĩa** của thành phần đã lập kế hoạch (`role` và `group`), không theo thứ tự object trong Blender hay theo mảnh tên.
- ID là ID ổn định của M4 có tiền tố trạng thái, ví dụ `stone_arch_bridge_arch2_voussoir03`. Với trạng thái có khung kế thừa, phần kế thừa lấy ID của trạng thái nguồn (giống cách engine dựng).
- **Lỗi** (beat thành `INVALID_REQUEST`, không có shot):
  - khái niệm không có thành phần nào trong mọi trạng thái của beat, ví dụ `keystone` trên cầu gỗ: "'keystone' (keystone) has no component in state 'timber_beam_bridge' (its roles: …)";
  - khái niệm mơ hồ, ví dụ `beam` trên cầu gỗ khớp cả `cap_beam` và `stringer`: thông báo gợi ý dùng khái niệm cụ thể;
  - khái niệm thành phần trong beat không có trạng thái công trình nào.
- Kiểm tra này chạy **trước** khi chọn chiến lược, nên một chiến lược nhẹ (HOLD không có mục tiêu) không thể lặng lẽ bỏ mất một thành phần đã được nêu tên.
- `validate-plan` kiểm tra lại độc lập: mọi ID mục tiêu phải hiển thị trong trạng thái của shot (dựng lại bằng `engine/spec.py`), và role phải thuộc khái niệm.

## 6. Thêm asset mới cho planner
1. Thêm spec (M4, `docs/m4/M4_ARCHITECTURE_MODELING.md` §7) → `asset-check` → `asset-render --preset review` → xem ảnh → `asset-catalog`.
2. Thêm khái niệm vào `config/visual_vocabulary.json` nếu cần một tên mới (kèm `where`).
3. `plan-visuals`: lời giải thích trong `qa/VISUAL_COVERAGE.md` cho biết asset nào được chọn và vì sao.

Không sửa catalog chỉ để che một yêu cầu còn thiếu: trạng thái `NEW_ASSET_REQUIRED` là kết quả đúng cho tới khi có bộ sinh thật.
