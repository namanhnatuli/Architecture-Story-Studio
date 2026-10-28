# Giao thức lập kế hoạch hình ảnh (M5)

Tài liệu cho người viết beat (biên tập viên hoặc Claude). Bạn viết **ý đồ** và **khái niệm**; planner chọn hình ảnh. Bạn không viết shot, frame hay camera.

## 1. Viết beat (`script/visual_beats.json`)
```json
{"beat_id": "B4", "kind": "fact", "narrative_intent": "SHOW_COMPONENT", "claim_ids": ["CLM_102"],
 "narration": "A stone arch works differently. It is built from wedge-shaped stones called voussoirs, with a keystone at the top of each arch.",
 "visual_goal": "Introduce the masonry arch and show one arch ring's voussoirs and keystone",
 "required_concepts": ["stone_arch_bridge", "arch_ring"],
 "focus_concepts": [{"concept": "voussoir", "group": "arch_2"}, {"concept": "keystone", "group": "arch_2"}],
 "expected_complexity": "MEDIUM"}
```
| Trường | Bắt buộc | Ý nghĩa |
|---|---|---|
| `beat_id`, `narration` | có | Một câu hoặc một ý của lời thoại; beat được dựng theo đúng thứ tự trong file |
| `kind` | có | `framing` (dẫn dắt, không có claim), `fact` (phải có `claim_ids`), `interpretation` |
| `narrative_intent` | có | Một trong 9 ý đồ (§2) |
| `visual_goal` | có | Một câu cho người review; chỉ là mô tả, không ảnh hưởng render (đổi câu này không làm cũ cache) |
| `required_concepts` | có | Khái niệm trong `config/visual_vocabulary.json`: công trình/khu đất (chọn asset) và thành phần (chọn mục tiêu). Có thể ghi `{"concept", "group"}` để giới hạn trong một nhóm ngữ nghĩa |
| `preferred_states` | không | Danh sách công trình theo thứ tự, dùng cho thay thế hoặc so sánh (A → B, hoặc A, B, C) |
| `focus_concepts` | không | Thành phần để cận cảnh (COMPONENT_CLOSEUP); mặc định là các thành phần trong `required_concepts` |
| `strategy` | không | Ép dùng một chiến lược (§3). Nếu điều kiện của nó không thỏa thì beat bị báo lỗi, không có chuyện lặng lẽ thay bằng chiến lược khác |
| `camera_mode` | không | Ghi đè chế độ camera cho HOLD |
| `required_accuracy` | không | `ILLUSTRATIVE` (mặc định), `REFERENCE_BASED`, `HISTORICALLY_VERIFIED` |
| `graphic` | không | Spec thẻ 2D (MOTION_GRAPHICS) cho chiến lược CARD |
| `timing.estimated_seconds` | không | Ghi đè ước lượng thời lượng của beat (chỉ áp dụng ở chế độ PROVISIONAL) |

Mức tài liệu: `timing_mode`, `publication.restriction` (`INTERNAL_ONLY` hoặc `PUBLICATION_CANDIDATE`), và `synthetic_fixture: true` cho dữ liệu bịa ra để test.

**Luật dữ liệu:** không bịa claim đã xác minh. Beat `fact` phải trích claim có trong `research/sources.json` với `review_status` là `SOURCE_VERIFIED` hoặc mạnh hơn. Nếu không, beat bị `EVIDENCE_BLOCKED` và không có shot nào được dựng cho nó.

## 2. Chín ý đồ hình ảnh và chiến lược (theo thứ tự ưu tiên)
| Ý đồ | Chiến lược | Ghi chú |
|---|---|---|
| `SHOW_CONTEXT` | SITE_HOLD → CARD | Khu đất trống, hoặc thẻ 2D tác giả cung cấp. Không có bản đồ hay ảnh tư liệu (`MAP_OR_IMAGERY`) |
| `INTRODUCE_ARCHITECTURE` | ASSEMBLE_IN → HOLD_HIGHLIGHT → HOLD | ASSEMBLE_IN chỉ dùng được khi shot trước kết thúc trên khu đất trống |
| `EXPLAIN_STRUCTURE` | HIGHLIGHT_THEN_EXPLODE → EXPLODE → HOLD_HIGHLIGHT | Bung theo layer lắp ráp |
| `SHOW_COMPONENT` | CLOSEUP_HIGHLIGHT → HOLD_HIGHLIGHT | Cận cảnh: camera khóa vừa khung các thành phần trọng tâm |
| `EXPLAIN_DESIGN_CHANGE` | HIGHLIGHT_REPLACE_HIGHLIGHT → REPLACE → SEQUENTIAL_STATES | REPLACE_PARTS chỉ dùng được giữa hai trạng thái chung khung (§4) |
| `COMPARE_VARIANTS` | COMPARE_SIDE_BY_SIDE → SEQUENTIAL_STATES | STACK cho công trình dài (cầu), ROW cho công trình gọn (nhà) |
| `SHOW_EVOLUTION` | SEQUENTIAL_STATES | Cần **mọi** claim đã được biên tập duyệt (`EDITORIALLY_APPROVED`); nếu chưa thì `EVIDENCE_BLOCKED` |
| `EXPLAIN_CAUSE_EFFECT` | CARD | Không có lớp mũi tên lực trên mô hình 3D (`FORCE_DIAGRAM`). Không có thẻ thì `MISSING_TEMPLATE` |
| `SUMMARIZE_DIFFERENCES` | CONTINUE_COMPARISON → COMPARE_SIDE_BY_SIDE | Ở lại khung so sánh và cho các phần khác nhau phát sáng |

Lý do một chiến lược bị loại (sai trạng thái, asset không hỗ trợ template, thiếu thời gian…) luôn được ghi trong mục "Planner decisions" của báo cáo coverage.

## 3. Chiến lược → template
| Chiến lược | Shot | Điều kiện |
|---|---|---|
| SITE_HOLD | HOLD (khu đất) | Beat có khái niệm khu đất |
| ASSEMBLE_IN | REPLACE_PARTS (trống → công trình, các phần rơi xuống theo layer) + HOLD phát sáng | Shot trước kết thúc trên khu đất |
| HOLD / HOLD_HIGHLIGHT | HOLD (+ highlight) | HOLD_HIGHLIGHT cần thành phần để phát sáng |
| CLOSEUP_HIGHLIGHT | HOLD toàn cảnh + HOLD cận cảnh (`camera_focus`) | Có thành phần trọng tâm |
| HIGHLIGHT_THEN_EXPLODE / EXPLODE | (HOLD +) EXPLODED_VIEW | Asset hỗ trợ EXPLODED_VIEW, có thành phần bung được |
| HIGHLIGHT_REPLACE_HIGHLIGHT / REPLACE | (HOLD +) REPLACE_PARTS (+ HOLD) | Hai trạng thái chung khung, asset đích hỗ trợ REPLACE_PARTS |
| SEQUENTIAL_STATES | HOLD A, cắt, HOLD B | Dùng khi không thay thế được |
| COMPARE_SIDE_BY_SIDE / CONTINUE_COMPARISON | SIDE_BY_SIDE | Từ 2 trạng thái trở lên; CONTINUE cần shot trước so sánh đúng các trạng thái đó |
| CARD | MOTION_GRAPHICS | Beat có `graphic` |

## 4. Tương thích khi thay thế (REPLACE_PARTS)
Chỉ thay thế được giữa hai trạng thái:
- chung **khung** (`structure_from`): cùng họ, cùng biến thể, và các tham số khác nhau đều nằm trong `replaceable_params`. Ví dụ Pratt → Warren dùng cùng thanh biên, dầm ngang và mặt cầu;
- từ khu đất trống (ASSEMBLE_IN);
- hai mái trên cùng một ngôi nhà (họ `roof`, base dùng chung).

Gỗ → đá, hay giàn → vòm đều **không** thay thế được. Khi tác giả ép `strategy: REPLACE` với hai trạng thái như vậy, beat bị `INVALID_REQUEST` ("share no frame"). Với chiến lược mặc định thì planner chuyển sang SEQUENTIAL_STATES và ghi lý do.

## 5. Timing
- **PROVISIONAL** (mặc định khi chưa có giọng đọc): thời lượng beat = số từ / 2.6 + 0.8 s, hoặc `timing.estimated_seconds`. Đây là ước lượng; báo cáo ghi rõ "estimates, not measured speech".
- **AUDIO_LOCKED**: lấy từ `script/timing.json` đã khóa (`schedule` của M3), bằng lead-in + thời lượng đo được + tail. Timing chưa khóa hoặc thiếu beat thì planner dừng với lỗi.
- Thời lượng tối thiểu của mỗi shot được tính bằng **motion planner thật của engine** (tìm nhị phân trên số frame), không đoán. Thời gian dư được chia theo trọng số (`composite_weights`) và chỉ kéo dài các đoạn giữ (hold). Tốc độ chuyển động không bao giờ thay đổi.
- Nếu chiến lược ưu tiên không đủ thời gian, planner thử chiến lược nhẹ hơn (ví dụ HIGHLIGHT_THEN_EXPLODE cần 7.04 s nhưng beat chỉ có 5.6 s, nên dùng EXPLODE). Nếu không chiến lược nào vừa: `TIMING_CONFLICT`, không có shot nào, **không có gì bị cắt ngắn**. Gợi ý khi gặp lỗi này: đơn giản hóa hình ảnh, tách beat, kéo dài lời thoại, hoặc chọn chiến lược khác.

## 6. Camera
| Chế độ | Công trình dài (cầu) | Công trình gọn (nhà) |
|---|---|---|
| FULL_OBJECT, THREE_QUARTER, LOCKED_TRANSFORMATION | BRIDGE_THREE_QUARTER | LOCKED_THREE_QUARTER |
| SIDE_ELEVATION | ELEVATION | ELEVATION |
| COMPONENT_CLOSEUP | BRIDGE_THREE_QUARTER + `camera_focus` | LOCKED_THREE_QUARTER + `camera_focus` |
| COMPARISON | BRIDGE_STACK (layout STACK) | LOCKED_THREE_QUARTER (layout ROW) |

- Mọi preset đã có từ M2–M4 (`config/visual_style.json`). M5 không thêm preset mới.
- Mỗi mục tiêu ngữ nghĩa được kiểm tra offline: phải nằm trong khung (trên dải phụ đề 10 %) và chiếm ít nhất 0.4 % diện tích khung hình. Nếu không, planner cảnh báo "too small to read: use COMPONENT_CLOSEUP".
- **Phần bị che:** khái niệm có `ghost_roles` trong từ vựng (dầm dọc nằm dưới ván, dầm ngang dưới bản mặt cầu, rui và đòn nóc dưới lớp phủ mái) sẽ làm các phần che nó chuyển sang trong suốt trong lúc nó phát sáng (`highlight.ghost`). Kiểm tra offline chỉ xét khung hình, không xét bị che; `check-blender` (`highlight_targets_visible`) đo phần thật sự nhìn thấy.
- Cận cảnh dùng camera khóa vừa khung thành phần trọng tâm. Ví dụ 13 viên đá vòm thứ hai (12 voussoir + keystone), với `camera_safe_band` 0.1.

## 7. Trạng thái coverage
| Trạng thái | Nghĩa | Có shot? |
|---|---|---|
| `COVERED` | Chiến lược ưu tiên hoặc một chiến lược thay thế đầy đủ đã được dùng | có |
| `PARTIALLY_COVERED` | Chỉ một chiến lược yếu hơn còn dùng được (ví dụ SEQUENTIAL_STATES thay cho thay thế) | có |
| `MISSING_ASSET` | Khái niệm chưa có asset/bộ sinh (`NEW_ASSET_REQUIRED`), hoặc chưa có trong từ vựng | không |
| `MISSING_TEMPLATE` | Cần năng lực chưa có (bản đồ, mũi tên lực) hoặc asset không hỗ trợ template | không |
| `TIMING_CONFLICT` | Không chiến lược nào vừa thời lượng | không |
| `EVIDENCE_BLOCKED` | Claim thiếu bằng chứng, chronology chưa duyệt, hoặc độ chính xác yêu cầu cao hơn mức của asset | không |
| `INVALID_REQUEST` | Yêu cầu sai: thành phần không tồn tại, mơ hồ, thay thế không tương thích, chiến lược lạ, engine từ chối | không |

Nếu có bất kỳ beat nào không phải COVERED hoặc PARTIALLY_COVERED thì `executable = false`: `plan-visuals` thoát với mã 4, còn `build-shots` từ chối biên dịch. **Không beat nào bị bỏ qua lặng lẽ.**

## 8. Quy trình
1. Viết hoặc sửa beat và claim → `plan-visuals`.
2. Đọc `qa/VISUAL_COVERAGE.md`: trạng thái, asset, mục tiêu, template, thời lượng dự kiến so với thời lượng kế hoạch, lý do.
3. Sửa beat (không sửa storyboard đã biên dịch; nó bị ghi đè và có `plan_sha256`) → lặp lại.
4. `validate-plan` → `build-shots` → `check-blender` → `still --preset review` (xem ảnh) → `preview`.
5. Chỉ shot bị đổi mới render lại. Đổi chữ trong claim hay `visual_goal` không làm cũ cache (có test).
