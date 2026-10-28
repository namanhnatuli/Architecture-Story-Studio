# M5.5: trí tuệ hình ảnh, phát hiện phần bị che và sửa kế hoạch trước khi render

**Beat → kế hoạch ban đầu → phân tích mức nhìn thấy → đánh giá bố cục → chọn cách sửa → kế hoạch đã kiểm chứng → preview Blender + QA.**

M5 đã chọn đúng asset, đúng thành phần và đúng template, nhưng một hình ảnh đúng kỹ thuật vẫn có thể không giải thích được gì. Ví dụ: dầm dọc phát sáng nằm dưới lớp ván; ba cây cầu quá nhỏ trong một khung so sánh; các viên đá vòm bung thẳng vào tường spandrel. M5.5 thêm một vòng đánh giá trong **chính planner tất định** của M5 (không có planner thứ hai, không gọi LLM khi chạy). Mọi quyết định sửa đều được ghi vào kế hoạch thực thi (visual plan), nên luôn tái lập được.

## 1. Hai mức kiểm tra
| Mức | Module | Cách làm | Tính chất |
|---|---|---|---|
| **Level 1**, ước lượng khi lập kế hoạch | `planner/visibility.py` | Dựng lại cảnh offline theo đúng luật của engine (`shot_builder`): thành phần, layout slot, ẩn/hiện tĩnh, camera khóa fit theo phần được dựng hoặc `camera_focus` cộng **bao chuyển động**, kế hoạch chuyển động thật (`templates.plan_shot`). Mỗi frame đánh giá được raster thành bộ đệm độ sâu + ID thành phần, lưới 192×108 (1 mẫu cho 3.3 px ở 640×360). Phần trong suốt ≥ 50 % (ghost) không tính là vật che | Ước lượng. **MESH** = mesh đã lập kế hoạch của asset thư viện M4 (chưa có bevel). **PROXY** = hộp lấy từ `engine/house_layout.py` cho nhà/mái cũ (không có bevel, không có vết cắt chân rui, ridge cap thay bằng hộp). Trạng thái `UNCERTAIN` khi ít mẫu (< 30) hoặc PROXY nằm sát ngưỡng (±0.08) |
| **Level 2**, đo thật trong Blender | `engine/qa_visibility.py` (`tools/cli.py verify-visibility`) | Cùng các frame, cùng lưới: bắn tia orthographic lên mesh **đã evaluate** (bevel, vết cắt, transform thật). Fade twin được tính là bản gốc; phần trong suốt ≥ 50 % không che. Với khái niệm đọc theo từng viên (*pieces*), mỗi thành phần được bắn tia riêng | Đo đạc, độ phân giải bằng lưới tia. Chỉ dùng cho QA, không phải phụ thuộc render (được loại khỏi khóa cache) |

`engine/house_layout.py` (mới) chứa toàn bộ số đo của nhà và mái M2 dưới dạng Python thuần. `engine/geometry.py` dựng Blender từ các mô tả này, còn Level 1 raster chính các mô tả đó. Hai bên dùng chung một nguồn số liệu, nên không thể lệch nhau. Đã kiểm chứng: chữ ký đỉnh/mặt/vật liệu/modifier của 27 shot thuộc 4 dự án giống hệt trước và sau khi tách mã.

## 2. Chỉ số cho mỗi mục tiêu (mỗi khái niệm, và mỗi thành phần khi cần)
| Chỉ số | Ý nghĩa |
|---|---|
| `projected_area` | Bóng (silhouette) của mục tiêu chiếm bao nhiêu phần khung hình (chỉ tính các polygon của mục tiêu) |
| `visible_area` | Phần mục tiêu là bề mặt đặc gần camera nhất, tính theo phần khung hình |
| `visible_share` | `visible_area / projected_area`: bao nhiêu phần bóng không bị che |
| `core_area` | Mẫu nhìn thấy mà cả 4 mẫu lân cận cũng nhìn thấy, tức không phải một vệt mảnh. Phân biệt mặt trước gọn của một khối sâu (keystone: share 0.15 nhưng core 0.30 %) với cạnh của một dầm nằm dưới mặt cầu (share 0.14, core 0) |
| `occluders` | Thành phần che nhiều nhất (theo số mẫu) |
| `safe_band_share` | Phần nhìn thấy nằm trong dải phụ đề phía dưới (10 % chiều cao) |
| `outside_share` | Phần đỉnh của mục tiêu nằm ngoài khung (bị cắt) |
| `components` | Từng thành phần: share và core riêng (dùng cho các viên tách rời) |

**Frame đánh giá:** frame đầu, 25 %, 50 %, 75 %, frame cuối và mọi marker của kế hoạch (`highlight_peak`, `exploded_hold`, `explode_end`, `return_start`, `incoming_end`, …). Không bao giờ chỉ dùng frame giữa. Frame *giải thích* (dùng để kết luận) là đỉnh phát sáng (HOLD), giữa khoảng giữ bung (EXPLODED_VIEW) hoặc lúc lắp xong (REPLACE_PARTS).

## 3. Kết luận đọc được hay không (`visibility.verdict`, ngưỡng trong `config/visual_planning.json` → `visibility`)
| Vấn đề | Điều kiện | Hiệu chỉnh trên frame thật của pilot |
|---|---|---|
| `OCCLUDED` | share < 0.25 **và** core < 0.2 % | Dầm dọc dưới ván: 0.14 / 0 → không đọc được (frame M5 trước khi sửa: chỉ thấy một vệt ở mép mặt cầu). Keystone trong cận cảnh: 0.15 / 0.30 % → đọc được (khối sáng ở đỉnh vòm). Vòng vòm: 0.31 → đọc được |
| `TOO_SMALL` | visible_area < 0.15 % (khoảng 350 px ở 640×360) | Đòn nóc mái khi cả ngôi nhà nằm trong khung: 0.11 % → nhỏ; reframe lên 0.55 % |
| `CLIPPED` | > 2 % đỉnh nằm ngoài khung | Cận cảnh fit sai thành phần (test âm) |
| `SUBTITLE_SAFE_AREA` | > 20 % phần nhìn thấy nằm trong dải phụ đề | — |
| `PIECES_HIDDEN` | Chỉ với khái niệm `read_as: pieces` trong một exploded view: có viên mà share < 0.5 và core < 0.1 % | Voussoir bung theo preset hướng tâm thì đi vào tường spandrel: share cả vòng 0.14, nhiều viên 0.0 |

Một khái niệm chỉ cần **đọc được ở ít nhất một shot của beat**. Ví dụ ở B3, xà mũ và dầm dọc bị che trong cảnh HOLD (SC_004), nhưng đọc được trong exploded view ngay sau đó (SC_005), nên không cần sửa.

## 4. Sửa kế hoạch (`planner/repair.py`)
Khi một khái niệm không đọc được ở bất kỳ shot nào của beat, các cách sửa được thử offline trên **bản sao** của shot, theo thứ tự ưu tiên mặc định:

1. **REFRAME**: `camera_focus` trên mọi mục tiêu của shot; với exploded view thì gồm cả **mọi phần chuyển động**, để màn bung không bị khung cắt (lỗi tìm ra ở mái nhà: các tấm phủ bay ra ngoài khung); kèm dải phụ đề. Vẫn giữ hướng nhìn.
2. **SAFE_BAND**: chừa dải phụ đề cho shot đó (nếu shot nằm trong một chuỗi cắt match, nhóm sẽ bị tách và điểm cắt thành cắt cứng).
3. **ALT_CAMERA**: một preset khác của lớp tỷ lệ (trừ preset so sánh).
4. **GHOST**: các nhóm role đang che mục tiêu (xếp theo số mẫu che, tối đa 2 nhóm, không bao giờ là site hay chính mục tiêu) chuyển sang trong suốt 0.7 theo nhịp xung sáng, rồi trở lại đặc (`highlight.ghost`, chỉ cho HOLD). Hình học không đổi; độ trong suốt chỉ tạm thời.
5. Nếu không cách nào đạt: chuyển sang **chiến lược tiếp theo** của beat (chạy lại kế hoạch có giới hạn và tất định), ví dụ CLOSEUP_EXPLODE → CLOSEUP_HIGHLIGHT.
6. Nếu vẫn không được: beat thành `PARTIALLY_COVERED` + `VISIBILITY_UNRESOLVED` (xem lại thủ công). Không có gì bị bỏ qua lặng lẽ.

Cách sửa bằng camera sẽ bị **bỏ qua (có ghi lý do)** nếu nó phá một cắt match, trừ khi vấn đề là kích thước hoặc bị cắt khung, vì những vấn đề đó chỉ khung gần hơn mới sửa được. Mọi ứng viên đã thử (PASS/FAIL/SKIPPED, kèm số đo) được ghi vào `coverage[].visual_repairs`; cách được chọn ghi vào `shots[].repairs` và `explanation`. `validate-plan` tính lại toàn bộ và từ chối:
- mức nhìn thấy đã lưu khác với kết quả tính lại;
- ghost không có bản ghi sửa;
- khái niệm không đọc được mà beat không bị gắn cờ.

## 5. Ví dụ trong pilot và fixture
| Shot | Vấn đề tìm ra offline | Các ứng viên | Chọn | Trước → sau (L1) | Đo trong Blender (L2) |
|---|---|---|---|---|---|
| B2 SC_003 dầm dọc | OCCLUDED (share 0.14, core 0) | REFRAME bỏ qua (cắt match với SC_002), ALT_CAMERA:ELEVATION bỏ qua (cắt match), GHOST:plank PASS | **GHOST:plank** (4 tấm ván) | 0.14 → 0.81 | 0.14 → 0.82 |
| B4 CLOSEUP_EXPLODE (bản nháp đầu) | voussoir bung vào tường (share 0.14, nhiều viên 0) | — | đổi cách bung: kéo mỗi viên ra khỏi mặt theo trục chiều sâu về phía camera (sâu + 0.3 m), cộng độ tỏa của preset; camera **chính diện** (ELEVATION), để phần kéo ra chỉ là chiều sâu, còn trên màn hình chỉ thấy các viên tỏa ra | 1.00, mọi viên đọc được | 1.00 |
| R2 SC_002 đòn nóc (fixture mái) | TOO_SMALL (0.11 %) | REFRAME PASS | **REFRAME** (mục tiêu + mọi phần bung) | 0.11 % → 0.29 % (share 0.35) | 0.29 % (share 0.36) |

## 6. Hiệu chỉnh Level 1 theo Level 2 (`qa/VISIBILITY.md` của mỗi dự án)
| Dự án | Dòng (mục tiêu × frame) | Kết luận trùng nhau | Sai số share trung bình / tối đa | Thời gian L2 / L1 |
|---|---|---|---|---|
| bridge-story-m5 | 122 | **100 %** | 0.006 / 0.017 | 3.6 s / 1.7 s |
| bridge-structure-evolution (M4) | 47 | 100 % | 0.005 / 0.015 | 2.2 s |
| roof-plan-m5 (PROXY) | 20 | 100 % | 0.015 / 0.043 | 0.8 s |
| roof-evolution (PROXY) | 10 | 100 % | 0.025 / 0.045 | 0.7 s |
| suffolk-roofs (PROXY) | 10 | 100 % | 0.013 / 0.014 | 0.7 s |

Cả hai mức đều là lưới mẫu 192×108, nên giá trị là **tỷ lệ mẫu**, không phải phần trăm bề mặt chính xác. Mesh thư viện khớp Blender trong khoảng 2 điểm phần trăm; proxy mái lệch tới khoảng 5 điểm, nên trạng thái UNCERTAIN gần ngưỡng là cần thiết.

## 7. Lệnh
```bash
P="--project bridge-story-m5"
python3 tools/cli.py plan-visuals $P        # Level 1 + sửa kế hoạch → qa/VISUAL_COVERAGE.md (mục "Visual repairs")
python3 tools/cli.py build-shots $P
python3 tools/cli.py verify-visibility $P   # Level 2 → qa/visibility_measured.json, visibility_report.json, VISIBILITY.md
```

## 8. Giới hạn
- Level 1 không thấy bevel, và với nhà cũ thì không thấy vết cắt chân rui hay hình dạng ridge cap (PROXY).
- Ngưỡng được hiệu chỉnh trên hai pilot (cầu, mái), chưa phải chuẩn chung cho mọi loại công trình. Độ tương phản của màu phát sáng **không** được đo; chỉ đo hình học có bị che hay không.
- Cách sửa chỉ gồm: framing, preset có sẵn, ghost tạm thời, chiến lược khác. Không bao giờ sửa hình học kiến trúc để dễ nhìn hơn.
