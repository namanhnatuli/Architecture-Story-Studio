# Báo cáo QA M5.5 (2026-10-28)

**Máy đo:** Apple **M4 Pro**, bộ nhớ hợp nhất 24 GB, macOS 26.6.2, Blender 5.2.2 LTS (Eevee, AgX), FFmpeg 9.0.1, Python 3.14.6 (không dùng numpy). Đây **không** phải số đo trên M4 / 16 GB. Mọi con số đều đo thật (log, `/usr/bin/time -l`, các file báo cáo QA).

## 1. Tóm tắt
| Hạng mục | Kết quả |
|---|---|
| Baseline M5 (trước khi sửa gì) | 174/174 test; QA Blender 163/64/71/92/52; trạng thái Suffolk đúng; cache 13/13 |
| Pilot `bridge-story-m5` sau M5.5 | 8/8 beat COVERED, **15 shot**, 1737 frame = 72.375 s; QA Blender **188/188**; media QA PASS; gate: **TECHNICAL PREVIEW — VALID (silent); NOT FOR PUBLICATION** |
| Mức nhìn thấy L1 ↔ L2 | 5 dự án, 209 dòng mục tiêu × frame, **kết luận trùng 100 %** |
| Sửa tự động | SC_003 dầm dọc (GHOST:plank), B7 so sánh (SEQUENTIAL_COMPARISON), R2 mái (REFRAME). Cần xem lại thủ công: 0 |
| Bộ đánh giá | **24/24** ca, 10/10 chiều |
| Test | **207/207** (174 cũ + 29 M5.5 + 4 Blender M5.5), không test nào bị bỏ qua |
| Suffolk | NARRATED_INTERNAL_REVIEW: TECHNICALLY_VALIDATED · EDITORIAL_REVIEW_PENDING · TTS_RIGHTS_PENDING (**không đổi**), G6 BLOCKED |

## 2. Test A: dầm dọc bị che
- **Trước khi render**, L1 đo được: share 0.136, core 0, vật che là 4 tấm ván và lan can phía nam. Kết luận: OCCLUDED.
- Planner thử và ghi lại:
  - REFRAME: bỏ qua, vì phá cắt match với SC_002;
  - ALT_CAMERA:ELEVATION: bỏ qua, vì cũng phá cắt match;
  - **GHOST:plank**: PASS, share 0.81.
- Kết quả **trùng với cách sửa của M5** (4 tấm ván, trong suốt 0.7). Khác biệt: lần này nó được chọn nhờ đo vật che, không nhờ một quy ước trong từ vựng.
- Đo trong Blender:
  - `verify-visibility`: 0.14 → 0.82;
  - MCP (lưới 96×54): 0.140 → 0.838, tức 0.87 % → 5.19 % khung hình; 4 tấm ván ở trạng thái trong suốt.
- Hình học không đổi: chữ ký mesh giống hệt, chỉ có kênh trong suốt chạy theo thời gian.

## 3. Test B: so sánh ba cầu dài
| | Thành phần điển hình nhỏ nhất (640×360) | Mô hình nhỏ nhất | Kết luận |
|---|---|---|---|
| STACK gap 0.5 (M5) | 1.3 px | 30 % | không đọc được |
| STACK gap 0.25 | 1.5 px | 34 % | không đọc được |
| ROW gap 0.35 / 0.2 | 1.1 px | 24–27 % | không đọc được |
| **Tuần tự** (một camera, ortho 33.11 cho cả ba) | **3.9 px** (giàn) | **88 %** | đọc được; tỷ lệ COMMON |

- B7 chọn SEQUENTIAL_COMPARISON. DETAIL_THEN_OVERVIEW cần 8.04 s nhưng beat chỉ có 6.21 s.
- Báo cáo coverage cảnh báo rằng lời thoại nói "side by side".
- B8 (overview) dùng STACK gap 0.25.
- MCP đo vùng giàn nhìn thấy: 0.12 % khung hình (STACK M5) → 1.66 % (tuần tự), tức khoảng **14×**.
- Ảnh trước/sau render thật: `projects/bridge-story-m5/qa/m55_before_after/B7_layout_candidates_640x360.jpg`.
  - Hàng 1: STACK 0.5, STACK 0.25, ROW 0.35, ROW 0.2.
  - Hàng 2: tuần tự gỗ, đá, giàn.
  - Hàng 3: giàn trong STACK ở pixel gốc ×3, bên cạnh giàn trong khung tuần tự ở pixel gốc.

## 4. Test C: cận cảnh voussoir và keystone
- Mục tiêu đúng: 12 voussoir + keystone của vòm 2 (`group: arch_2`).
- Bản nháp đầu của CLOSEUP_EXPLODE dùng preset bung hướng tâm. L1 phát hiện: share 0.14, nhiều viên 0.0, vì các viên đi vào tường spandrel. Kết luận: PIECES_HIDDEN.
- Thử lần hai: kéo các viên ra về phía camera ở góc ba phần tư. Đọc được về mặt số liệu, nhưng **xem ảnh** thì các viên đá sâu 4.8 m trông như những tấm ván chìa ra khỏi tường. Đây là lỗi về truyền đạt, không phải về số đo. Vì vậy chọn **camera chính diện** (ELEVATION): phần kéo ra trở thành chiều sâu, còn trên màn hình chỉ thấy các viên hình nêm tỏa ra.
- Kết quả cuối:
  - share 1.00; mọi viên share 1.00, core nhỏ nhất 0.46 %;
  - nằm trong dải an toàn (đáy y = 0.150, dải 0.10), không có giao cắt mới;
  - camera của Blender khớp offline (ortho 10.889 so với 10.891).
  - MCP: 0.308 (cận cảnh phát sáng M5, spandrel che) → 1.000.
- Mức nhìn thấy được đo ở mọi frame của màn bung (bắt đầu, kết thúc bung, giữ, bắt đầu trả về, kết thúc), xem `qa/VISIBILITY.md`.

## 5. Test D và E: profile
- **D** `bridge-story-m5` (TECHNICAL_SILENT_PREVIEW):
  - G0, GV, G4 PASS;
  - G1 PENDING_EDITORIAL (5 claim mới SOURCE_VERIFIED);
  - G2, G3, G5 NOT_APPLICABLE;
  - G6 BLOCKED;
  - trạng thái TECHNICALLY_VALIDATED + EDITORIAL_REVIEW_PENDING; không có PUBLICATION_READY.
- **E** `suffolk-roofs` (NARRATED_INTERNAL_REVIEW): gate và trạng thái giống hệt M5. Có test cho các trường hợp sau, chạy trên bản sao:
  - gắn profile TECHNICAL_SILENT_PREVIEW: G0 FAIL ("has narration"), kết luận NOT VALID;
  - PUBLICATION_CANDIDATE: G6 BLOCKED (thiếu metadata, claim chưa duyệt, giọng đọc NOT_CLEARED);
  - mọi gate PASS dưới NARRATED_INTERNAL_REVIEW: vẫn không thành PUBLICATION_READY.
- Các preview không lời khác sau khi render lại:
  - roof-plan-m5: VALID (silent);
  - roof-evolution: VALID (silent), EDITORIAL_REVIEW_PENDING (CLM_001 provisional);
  - bridge-structure-evolution: VALID (silent), EDITORIAL_REVIEW_PENDING.

## 6. Tổng quát hóa sang mái (cùng planner, cùng giao diện QA)
| Kiểm tra | Kết quả |
|---|---|
| Nhà gọn | camera LOCKED_THREE_QUARTER, lớp tỷ lệ `compact` |
| Phát sáng thành phần mái | R2: rafters share 0.59, đòn nóc 0.35 (proxy). L2: 0.55 và 0.36 |
| Mục tiêu nhỏ | Đòn nóc TOO_SMALL (0.11 %) → REFRAME trên mọi phần bung (0.29 %). Phát hiện khi xem ảnh: bản reframe đầu chỉ fit theo mục tiêu nên các tấm phủ bay ra ngoài khung; đã sửa luật |
| Thay mái | R3 REPLACE_PARTS (hai mái trên cùng tường), QA 52/52 |
| So sánh hai biến thể | R4 ROW gap 0.35 (thành phần 31.9 px, mô hình 35 %). Không cần dự phòng; giống M5 |
| Proxy mái so với Blender | 20 dòng, trùng 100 %, sai số share trung bình 0.015 (tối đa 0.043) |

## 7. QA bằng MCP (Blender GUI riêng, bản sao `.blend`)
- `mcp-for-blender==2.2.4`, safe mode (`import subprocess` bị từ chối; **lambda cũng bị từ chối**, nên script dùng `def`), chỉ lắng nghe 127.0.0.1:9876, không có Blender nào khác đang chạy. Đã đóng sau khi xong, không lưu gì.
- Lần chạy đầu: các script mở file bị từ chối vì có lambda, nên mọi lệnh `look` sau đó chạy nhầm scene. Toàn bộ kết quả lần đó đã bị bỏ và chạy lại.
- Cho mỗi visual được sửa: (1) baseline, (2) vấn đề đo được, (3) sửa ở mức plan, (4) dựng lại, (5) chụp bản đã sửa, (6) so sánh hình và số:

| Cặp | Trước | Sau | `look` (target) |
|---|---|---|---|
| A SC_003 dầm dọc | share 0.140, 0.87 % khung | 0.838, 5.19 %, 4 phần trong suốt | frame 1/65/120: mặt cầu trong suốt ở đỉnh, đặc lại ở frame 120 |
| C SC_007 vòm 2 | 0.308 (cận cảnh phát sáng M5) | 1.000, 8.87 % (chính diện, bung) | frame 1/40/76/148: các viên tiến ra, tỏa, trở về |
| R SC_002 mái | 1.06 % khung (ortho 16.25) | 2.72 % (ortho 9.69) | frame 1/81 |
| B B7 giàn | 0.12 % (STACK) | 1.66 % (tuần tự); overview 0.27 % | frame 75 / 25 |

Bằng chứng nằm ở `projects/bridge-story-m5/qa/m55_before_after/`: `mcp_*.jpg` và `mcp_session_log.txt` (đường dẫn máy đã được ẩn).

## 8. Hiệu năng và cache
**Lập kế hoạch** (pilot, không cần Blender): `plan-visuals` 1.49 s (gồm L1 và sửa kế hoạch), `validate-plan` 0.47 s (tính lại mức nhìn thấy và bố cục), `build-shots` 0.42 s; fixture mái 0.15 s; `evaluate-planning` (24 ca) 3.4 s.

**Mức nhìn thấy:** L1 1.7 s cho 122 dòng của pilot (offline, toàn bộ frame); L2 3.6 s trong Blender (lưới 192×108).

**Render preview 640×360** (engine thay đổi nên cả 15 shot render lại):
| Shot | Template | Frame | Thời gian | s/frame |
|---|---|---|---|---|
| SC_001 | HOLD khu đất | 260 | 106.3 s | 0.41 |
| SC_002 | lắp ráp | 140 | 63.5 s | 0.45 |
| SC_003 | HOLD + ghost | 120 | 78.8 s | 0.66 |
| SC_004 | HOLD | 72 | 29.9 s | 0.42 |
| SC_005 | EXPLODED_VIEW | 160 | 66.1 s | 0.41 |
| SC_006 | HOLD | 75 | 32.5 s | 0.43 |
| SC_007 | EXPLODED_VIEW cận cảnh chính diện | 148 | 62.3 s | 0.42 |
| SC_008–SC_011 | HOLD / REPLACE_PARTS | 427 | 188.9 s | 0.42–0.50 |
| SC_012–SC_014 | tuần tự (3 variant được dựng) | 149 | 107.4 s | 0.71–0.74 |
| SC_015 | SIDE_BY_SIDE STACK | 186 | 176.9 s | 0.95 |
| **Tổng** | | **1737** | **912.5 s** | 0.53 |

- Toàn bộ `preview` mất 920 s, max RSS **508 MB**.
- Fixture mái: 503 frame, 198 s, 465 MB. roof-evolution: 480 frame, 182 s, 459 MB. Pilot M4: 708 frame, 373 s, 503 MB.
- Ảnh tĩnh review: 15 ảnh 960×540 mất 10.8 s.
- Render tuần tự từng tiến trình Blender một; không render 4K.
- **Cache:**
  - thay đổi engine (`house_layout`, nhãn HOLD, bao chuyển động) làm toàn bộ cũ, đúng luật;
  - sau đó, đổi `ghost_transparency` của plan chỉ làm cũ **1/15** (SC_003); trả lại giá trị cũ thì 15/15 CACHED (đo bằng `cache-report`);
  - test: camera → 1 shot, ghost → 1 shot, layout → 1 shot, mục tiêu → 1 shot; lời giải thích, profile, metadata xuất bản → 0 shot; ngưỡng không đổi quyết định → plan giống hệt.
- **Vấn đề hình ảnh** (kế hoạch cuối):
  - pilot: 1 vấn đề nhìn thấy được tự sửa (SC_003), 1 bố cục tự chọn lại (B7), 2 dòng bị che ở SC_004 nhưng đọc được trong SC_005 của cùng beat (không cần sửa);
  - mái: 1 vấn đề tự sửa (R2);
  - cần xem lại thủ công: 0.
- **Phát hiện trong lúc phát triển và đã sửa trong code:**
  - voussoir bung vào tường;
  - voussoir trông như tấm ván ở góc ba phần tư;
  - reframe làm khung cắt phần bung;
  - hai lần reframe ghi đè nhau;
  - TOO_SMALL quá nghiêm.

## 9. Test
| Bộ | Số test |
|---|---|
| `tests/test_m55_visual_intelligence.py` | 29: ước lượng, bất định, che khuất, ghost, dải phụ đề, framing sai (âm), từng viên, sửa, plan bị sửa tay (âm), bố cục, độ phân giải, tỷ lệ, cảnh báo lời thoại, profile, Suffolk cô lập, publication giả (âm), media không lời, đánh giá + checker bắt kỳ vọng sai (âm), cache, tái lập, schema |
| `tests/test_blender_m55.py` | 4: L2 đo cùng frame, dầm dọc bị che và bản sửa, từng voussoir, L1/L2 trùng ở mọi frame |
| Toàn bộ `python3 -m unittest discover -s tests` | **207/207 OK** |

## 10. Giới hạn còn lại
- L1/L2 đều là lưới mẫu, nên không đo được phần trăm bề mặt chính xác. Proxy mái lệch tới khoảng 5 điểm. Không đo độ tương phản màu.
- Ngưỡng được hiệu chỉnh trên hai pilot. Các họ công trình mới cần hiệu chỉnh lại.
- So sánh tuần tự chỉ cho mỗi cầu khoảng 2 s, vì B7 chỉ dài 6.2 s. Lời thoại nói "side by side" đã được cảnh báo nhưng chưa được viết lại.
- `max_ghost_role_groups` = 2: nếu cần ghost nhiều hơn thì xem lại thủ công (có test).
- Mỗi dự án vẫn chỉ một họ công trình. Chưa có overlay, mũi tên lực, bản đồ (xem `M6_READINESS.md`).
