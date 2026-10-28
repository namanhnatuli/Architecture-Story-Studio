# Báo cáo QA M5 (2026-10-28)

**Máy đo:** Apple **M4 Pro**, bộ nhớ hợp nhất 24 GB, macOS 26.6.2, Blender 5.2.2 LTS (Eevee, AgX), FFmpeg 9.0.1, Python 3.14.6. Đây **không** phải số đo trên máy M4 / 16 GB; trên máy đó thời gian render nhiều khả năng sẽ dài hơn. Mọi con số dưới đây đều là số đo thật (log, `/usr/bin/time -l`, báo cáo QA), không có số ước lượng.

## 1. Tóm tắt
| Hạng mục | Kết quả |
|---|---|
| Pilot `bridge-story-m5` "Three Ways to Span a Gap" | 8/8 beat **COVERED**, 13 shot, 1737 frame = **72.375 s** (PROVISIONAL, không lời, INTERNAL ONLY) |
| `validate-plan` + G0 | PASS |
| QA Blender (`check-blender`) | **163/163** |
| Media QA preview 640×360 | PASS: 0 đoạn đen, đủ frame từng shot; 8 cắt match có SSIM ≥ 0.99999, 4 cắt cứng 0.59–0.80 (cố ý) |
| Fixture mái `roof-plan-m5` (SYNTHETIC) | 4/4 COVERED (ADAPT_EXISTING_ASSET), `validate-plan` PASS, QA Blender **52/52**, 4 ảnh tĩnh review |
| Hồi quy | roof-evolution **64/64**, suffolk-roofs **71/71**, bridge-structure-evolution **92/92** (mỗi dự án có thêm kiểm tra mới `highlight_targets_visible`). Gate suffolk không đổi |
| Test | **174/174** (§9) |

## 2. Lập kế hoạch pilot (`qa/VISUAL_COVERAGE.md`)
| Beat | Ý đồ | Chiến lược | Shot (template) | Giây dự kiến / kế hoạch |
|---|---|---|---|---|
| B1 | SHOW_CONTEXT | SITE_HOLD | SC_001 HOLD (khu đất trống) | 10.80 / 10.83 |
| B2 | INTRODUCE_ARCHITECTURE | ASSEMBLE_IN | SC_002 REPLACE_PARTS (trống → cầu gỗ), SC_003 HOLD (dầm dọc phát sáng, ván ghost) | 10.80 / 10.83 |
| B3 | EXPLAIN_STRUCTURE | HIGHLIGHT_THEN_EXPLODE | SC_004 HOLD, SC_005 EXPLODED_VIEW | 9.65 / 9.67 |
| B4 | SHOW_COMPONENT | CLOSEUP_HIGHLIGHT | SC_006 HOLD (vòng vòm), SC_007 HOLD cận cảnh 13 viên của vòm 2 | 9.26 / 9.29 |
| B5 | INTRODUCE_ARCHITECTURE | HOLD_HIGHLIGHT (ASSEMBLE_IN bị loại vì shot trước không kết thúc trên khu đất trống) | SC_008 HOLD (bụng giàn Pratt) | 5.03 / 5.04 |
| B6 | EXPLAIN_DESIGN_CHANGE | HIGHLIGHT_REPLACE_HIGHLIGHT | SC_009 HOLD, SC_010 REPLACE_PARTS Pratt → Warren (chung khung), SC_011 HOLD | 12.72 / 12.75 |
| B7 | COMPARE_VARIANTS | COMPARE_SIDE_BY_SIDE | SC_012 SIDE_BY_SIDE STACK | 6.18 / 6.21 |
| B8 | SUMMARIZE_DIFFERENCES | CONTINUE_COMPARISON | SC_013 SIDE_BY_SIDE, các phần khác nhau phát sáng | 7.72 / 7.75 |

- Asset: mọi khái niệm đều `REUSE_EXISTING` (5 asset thư viện + khu đất). `steel_truss_bridge` và `pratt_truss` dùng chung một trạng thái.
- Nhóm liên tục camera: (1) SC_001–SC_005, site + cầu gỗ; (2) SC_006; (3) SC_007 cận cảnh; (4) SC_008–SC_011, Pratt + Warren; (5) SC_012–SC_013, so sánh.
- Nội dung có kiểm chứng: 5 claim SOURCE_VERIFIED (Wikipedia, đọc ngày 2026-10-28, trích nguyên văn), chưa claim nào được duyệt biên tập, nên mọi shot mang nhãn `INTERNAL_PREVIEW`. Pilot không nói về công trình lịch sử cụ thể, không có dòng thời gian, không so sánh tải trọng hay "loại nào tốt hơn" (B8: "These are illustrations, not a timeline").
- Không dùng lại timeline M4: M4 có 7 shot / 29.5 s, viết tay bằng `tools/make_bridge_pilot.py`. M5 có 13 shot / 72.4 s, do planner sinh từ 8 beat.

## 3. Smoke test (trước khi render toàn bộ)
| Shot | Kiểm tra | Frame kế hoạch / MP4 | Thời gian | Max RSS |
|---|---|---|---|---|
| SC_005 (B3, bung cầu gỗ) | asset `bridge_timber_beam_01`, 13 thành phần phát sáng, bung theo layer rồi trả về đúng chỗ | 160 / 160 | 65.3 s | 444 MB |
| SC_007 (B4, cận cảnh vòm 2) | camera khóa vừa khung 13 thành phần trọng tâm, đáy khung trên dải phụ đề | 112 / 112 | 47.1 s | 451 MB |

## 4. Lỗi tìm ra khi xem hình và cách sửa
| # | Lỗi | Phát hiện bằng | Sửa | Kiểm tra lại |
|---|---|---|---|---|
| 1 | **Dầm dọc bị ván che.** SC_003 cho dầm dọc phát sáng, nhưng từ camera ba phần tư chỉ thấy một vệt mảnh ở mép mặt cầu. Kiểm tra offline chỉ xét khung hình, không xét bị che. Pilot M4 `bridge-structure-evolution` SC_001 cũng có lỗi này nhưng QA M4 không bắt được | Xem frame, rồi so sai khác từng pixel (chỉ 2 212 px đổi), rồi đo bằng tia trong Blender: **14 %** bóng nhìn thấy, 0.85 % khung hình | (a) Engine: `highlight.ghost` cho HOLD, ván chuyển trong suốt 0.7 theo nhịp xung sáng. (b) Từ vựng: `ghost_roles` (dầm dọc → ván, dầm ngang → bản mặt cầu, rui/đòn nóc → lớp phủ mái); planner tự thêm ghost. (c) QA Blender mới `highlight_targets_visible` (≥ 25 % bóng nhìn thấy, ≥ 0.3 % khung hình). (d) Pilot M4 SC_001 cũng được ghost | SC_003: **82 %** nhìn thấy, 5.13 % khung hình; test Blender `tests/test_blender_m5.py` (không ghost: 13.7 % → FAIL; có ghost: 82.3 %); xem frame 65: ván trong suốt, dầm dọc phát sáng bên dưới; MCP: bản gốc ẩn, twin hiện ở 0.7 |
| 2 | **Ảnh tĩnh của shot lắp ráp toàn khu đất trống.** Marker `middle` của REPLACE_PARTS nằm giữa lúc phần cũ đi ra và phần mới đi vào; với ASSEMBLE_IN (không có phần cũ) thì đó vẫn là khung trống | Xem bảng ảnh tĩnh review | Compiler dùng `incoming_end` cho shot lắp ráp vào khu đất | Ảnh SC_002 cho thấy cầu đã lắp xong. Cache render không đổi (13/13 CACHED) |
| 3 | Khung so sánh ba cầu nhỏ: mỗi cầu khoảng 190 px chiều ngang ở 640×360, khoảng 570 px ở 1080p | Xem frame SC_012 | **Không sửa** (giới hạn đã biết từ M4: cùng `gap_ratio` 0.5 và `label_band` 0.1 với layout đã được kiểm chứng ở M4). Vẫn đọc được ở 1080p | — |

Không có lỗi nào được sửa trực tiếp trong scene MCP; mọi sửa đổi đều nằm trong code hoặc cấu hình, rồi dựng lại qua CLI.

## 5. QA bằng MCP (Blender GUI riêng, bản sao `scenes/*.blend`)
- `mcp-for-blender==2.2.4` (server 1.30.0, addon 1.8, protocol 15). Safe mode bật: `import os` bị từ chối, và `bpy_extras` cũng bị từ chối, nên phép chiếu được viết lại chỉ bằng `mathutils`. Socket chỉ lắng nghe `127.0.0.1:9876`. Telemetry tắt; mọi thư viện asset và generator đều tắt. Không có Blender nào khác đang chạy. Blender QA được đóng sau khi xong, không lưu gì.
- Mọi lệnh `look` đều truyền `target`. Một lần `look` chạy nhầm scene vì script mở file bị safe mode từ chối (lỗi "No object named …"); đã chạy lại sau khi sửa script.

| Shot | Kiểm tra (execute + look) | Kết quả |
|---|---|---|
| SC_002 | Variant được dựng; trạng thái hiển thị ở frame 1 và frame cuối; look frames 1/30/55/80/140 (target trụ, ván, bờ) | Chỉ site + cầu gỗ (40 mesh gồm 20 twin); frame 1 chỉ có khu đất, frame cuối có cầu gỗ; các phần rơi xuống theo layer |
| SC_003 | Trong suốt và highlight ở frame 1/65/120; look (target 4 dầm dọc) | Frame 65: 4 bản gốc ẩn, 4 twin hiện ở 0.7, dầm dọc 0.45; frame 1/120: đặc, không phát sáng |
| SC_007 | Chiếu 13 thành phần vòm 2 vào khung; số phần đang phát sáng; look frames + angles (front/three_quarter/top) | x 0.158–0.842, y 0.159–0.944 (trên dải 0.1); đúng 13 phần phát sáng, 0 phần khác; hình học vòm, keystone, trụ đúng ở mọi góc |
| SC_010 | Phần riêng của Warren; look frames 1/40/62/90/124 | Warren chỉ có 4 thanh chéo (+ twin), khung kế thừa từ Pratt; thanh đứng Pratt bay ra, thanh chéo Warren rơi vào |
| SC_012 | Slot, nhãn; look frames 1/75/149 (target thuộc 3 slot) | 3 slot xếp chồng, nhãn "Timber beam bridge / Stone arch bridge / Steel truss bridge", 108 mesh |

## 6. Bộ test âm (`tests/test_m5_planner.py`, dữ liệu SYNTHETIC chèn vào bản sao pilot)
| Trường hợp | Kết quả mong đợi (đã đạt) |
|---|---|
| Asset không tồn tại (`suspension_bridge`) | `MISSING_ASSET` + nhiệm vụ `NEW_FAMILY_GENERATOR`, không có shot, `executable=false`; `covered_bridge` → "not in config/visual_vocabulary.json" |
| Thành phần không tồn tại (`keystone` trên cầu gỗ) | `INVALID_REQUEST` "'keystone' … has no component in state 'timber_beam_bridge'". Kiểm tra chạy trước khi chọn chiến lược, nên HOLD không lặng lẽ bỏ mất thành phần |
| Thành phần mơ hồ (`beam`, `member`) | `MappingError` "ambiguous" |
| REPLACE không tương thích (gỗ → đá, ép `strategy: REPLACE`) | `INVALID_REQUEST` "share no frame" |
| Ý đồ không hỗ trợ / thiếu năng lực | `SHOW_EXPLOSION` bị từ chối khi kiểm tra beat; EXPLAIN_CAUSE_EFFECT không có thẻ → `MISSING_TEMPLATE` (FORCE_DIAGRAM) |
| Không đủ thời gian (B3 = 1.5 s) | `TIMING_CONFLICT`, "nothing was truncated", không có shot; B3 = 5.6 s → chọn EXPLODE thay HIGHLIGHT_THEN_EXPLODE (cần 7.04 s) |
| Claim không có bằng chứng (CLM_102 PROVISIONAL) | `EVIDENCE_BLOCKED`, không có shot |
| SHOW_EVOLUTION khi chưa có chronology đã duyệt | `EVIDENCE_BLOCKED` |
| Sửa tay kế hoạch | `validate-plan` bắt được: mục tiêu không hiển thị, sai role, khe hở thời gian, sai thứ tự, REPLACE không chung khung, cắt match giữa hai nhóm, cắt match đổi trạng thái, thiếu beat |
| AUDIO_LOCKED khi timing chưa khóa | lỗi "not locked" |

Có test dương tương ứng: sinh asset 4 vòm (`GENERATE_FROM_SUPPORTED_FAMILY`) ghi vào `planning/generated_assets/`, qua `validate-plan` + G0, catalog không đổi; đổi beat B5 thành SHOW_COMPONENT thì hình ảnh đổi theo (cận cảnh thanh chéo).

## 7. Phụ thuộc cache (`CacheDependencyTest`)
- Sửa chữ claim, caveat, `visual_goal`: **0** shot cũ.
- Đổi mục tiêu ngữ nghĩa của B5 (`truss_web` → `diagonal_members`): chỉ **SC_008** cũ.
- Đổi hình học cầu đá (`voussoirs_per_arch` 11): chỉ các shot có dựng cầu đá cũ (SC_006, SC_007, SC_012, SC_013); các shot khu đất/cầu gỗ/giàn vẫn dùng cache.
- Đã đo thực tế: sau khi đổi marker ảnh tĩnh và chạy lại `plan-visuals`/`build-shots`, `cache-report` cho 13/13 CACHED. Sửa `engine/motion.py` (thêm ghost) thì cả 13 shot render lại, đúng luật cache (code engine là phụ thuộc của mọi shot).

## 8. Hiệu năng
**Lập kế hoạch (thuần Python):** `plan-visuals` 0.16 s, `validate-plan` 0.07 s (gồm biên dịch thử + G0), `build-shots` 0.08 s (pilot); fixture mái 0.05 s. `check-blender` pilot: 7.5 s, max RSS 307 MB.

**Render preview 640×360 (lần render đầy đủ thứ hai, cả 13 shot, sau khi thêm ghost):**
| Shot | Template | Variant dựng | Frame | Thời gian | Giây/frame |
|---|---|---|---|---|---|
| SC_001 | HOLD khu đất | 2 | 260 | 106.3 s | 0.41 |
| SC_002 | REPLACE_PARTS (lắp ráp) | 2 | 140 | 65.0 s | 0.46 |
| SC_003 | HOLD + ghost | 2 | 120 | 79.7 s | **0.66** (twin trong suốt BLENDED) |
| SC_004 | HOLD | 2 | 72 | 30.7 s | 0.43 |
| SC_005 | EXPLODED_VIEW | 2 | 160 | 67.9 s | 0.42 |
| SC_006 | HOLD | 1 | 111 | 47.6 s | 0.43 |
| SC_007 | HOLD cận cảnh | 1 | 112 | 46.7 s | 0.42 |
| SC_008 | HOLD | 2 | 121 | 51.7 s | 0.43 |
| SC_009 | HOLD | 2 | 90 | 38.3 s | 0.43 |
| SC_010 | REPLACE_PARTS Pratt → Warren | 2 | 124 | 59.2 s | 0.48 |
| SC_011 | HOLD | 2 | 92 | 35.9 s | 0.39 |
| SC_012 | SIDE_BY_SIDE STACK | 3 | 149 | 152.8 s | 1.03 |
| SC_013 | SIDE_BY_SIDE STACK | 3 | 186 | 191.0 s | 1.03 |
| **Tổng** | | | **1737** | **972.7 s** | 0.56 |

- Toàn bộ `preview` (render, encode, media QA, contact sheet): **978 s**, max RSS **509 MB** (tiến trình Blender lớn nhất). Lần đầu (11 shot, SC_005/SC_007 lấy cache từ smoke test): 817 s, 502 MB.
- Số object: shot site + cầu gỗ có 44 mesh (20 là twin); cận cảnh cầu đá 53; Pratt + Warren 49; khung so sánh 3 cầu 108.
- Ảnh tĩnh: 13 ảnh review 960×540 mất 9.1 s (524 MB); 13 ảnh `production_test` 1920×1080 mất 18.8 s (619 MB); 4 ảnh review mái mất 3.5 s.
- Nhờ `build_variants`, shot một mô hình chỉ dựng 1–2 variant thay vì cả 5 (site, gỗ, đá, Pratt, Warren); M4 dựng mọi variant để khóa camera chung.
- Không render 4K, không render chuỗi 1080p, không mô phỏng vật lý. Không chạy hai tiến trình Blender nặng cùng lúc: smoke test, preview, ảnh tĩnh, `check-blender` và MCP chạy lần lượt. Không render song song.

## 9. Test
| Bộ | Số test | Kết quả |
|---|---|---|
| `tests/test_m5_planner.py` (không cần Blender) | 34 | OK |
| `tests/test_blender_m5.py` (Blender) | 2 | OK |
| Toàn bộ `python3 -m unittest discover -s tests` (M2–M5, gồm test Blender) | **174** | OK, không test nào bị bỏ qua (15.7 s) |

Pilot M4 `bridge-structure-evolution` được render lại sau khi sửa SC_001: 7 shot, 368 s, max RSS 507 MB, media QA PASS (engine đổi từ M4, nên mọi shot đều render lại).

## 9b. Gate xuất bản (`gates`)
- `bridge-story-m5`: **INTERNAL PREVIEW — NOT PUBLICATION-READY** (fail closed). G0 PASS. G1 chờ duyệt biên tập. G2, G3, G5 FAIL vì pilot không có lời đọc (không dùng OmniVoice). G4 ghi "Blender QA 163/163; media QA is stale": gate M3.5 so số frame với `script/timing.json`, mà dự án không lời thì không có file này. Đây không phải lỗi render. G6 BLOCKED (claim chưa duyệt, timing chưa khóa).
- `suffolk-roofs`: không đổi (`TECHNICALLY_VALIDATED` · `EDITORIAL_REVIEW_PENDING` · `TTS_RIGHTS_PENDING`); chỉ số kiểm tra G4 đổi từ 70/70 thành 71/71.

## 10. Giới hạn còn lại
- Timing PROVISIONAL là ước lượng (2.6 từ/giây). Pilot không có lời đọc (OmniVoice không được dùng cho M5, vì quyền thương mại chưa rõ).
- Kiểm tra hiển thị offline không xét vật che; kiểm tra chính xác là `check-blender`. Asset mái cũ không kiểm tra hiển thị offline được.
- Khung so sánh STACK nhỏ ở 640×360 (§4 #3).
- Chưa có bản đồ, ảnh tư liệu hay mũi tên lực trên mô hình 3D. Mỗi dự án chỉ dùng một họ công trình.
