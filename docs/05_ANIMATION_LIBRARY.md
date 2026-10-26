# SOP 05 — Animation template catalog

| Template | Công dụng | Điều kiện |
|---|---|---|
| `ASSEMBLE` | Cấu kiện vào vị trí | Object IDs + target transforms |
| `DISASSEMBLE` | Tách các phần không còn dùng | Stagger + exit path, preserve shared |
| `REPLACE_PARTS` | A ra, B vào | Source+target component groups, cùng tọa độ |
| `STATE_TRANSITION` | So sánh A/B/C, thời kỳ | Tách 2 geometry khi topology khác |
| `SIDE_BY_SIDE` | 2–3 mô hình ngang nhau | Cùng scale/camera/lights |
| `EXPLODED_VIEW` | Tách lớp để giải thích | Component semantic groups |
| `CUTAWAY` | Nhìn kết cấu bên trong | Cắt/chia mesh có chủ đích |
| `CAUSE_AND_EFFECT` | Hiển thị yếu tố khí hậu/kỹ thuật | Nguồn bằng chứng và caveat |
| `HIGHLIGHT_DIFFERENCE` | Chỉ ra thành phần thay đổi | Không tô highlight những cấu kiện giống nhau |
| `TIMELINE` | Các mốc thời gian có nguồn | Không ngầm áp đặt tiến hóa tuyến tính |

## Thứ tự ưu tiên triển khai
MVP: `REPLACE_PARTS` (A tháo mái/B lắp mái). V1: `SIDE_BY_SIDE`, `EXPLODED_VIEW`, `HIGHLIGHT_DIFFERENCE`. V2: `CUTAWAY`, `TIMELINE`, `CAUSE_AND_EFFECT`.

## Transform logic
Mỗi object có **target transform** và animation **có thể sample deterministic theo frame**. Variant gốc không bị xóa; chỉ ẩn/di chuyển khỏi camera khi không active. Không dùng Shape Keys giữa hai mesh topology khác biệt.

## Cân nhắc hiệu suất
Các loại brick/roof tiles lặp lại nên dùng instancing; chỉ tách thành objects riêng khi cần animation độc lập. Animation rigid body/destruction không là hướng cốt lõi của kênh.
