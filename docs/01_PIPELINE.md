# SOP 01 — End-to-end narrative-first pipeline

## Nguyên lý
**What viewers learn → What they see → What must move → How to render.** Không bắt đầu bằng geometry hoặc animation.

| Giai đoạn | Đầu vào | Đầu ra | Gate |
|---|---|---|---|
| 1. Research | Câu hỏi/video idea | Source ledger, claims, uncertainty | G1: có dẫn chứng phù hợp |
| 2. Narrative outline | Claims | Story arc: hook, why, change, trade-off | Không suy diễn quan hệ nhân quả |
| 3. Script + visual feasibility | Outline | English narration + visual beat list | Tất cả đoạn có giải pháp visual |
| 4. Storyboard | Visual beats | Shot list/time/type/camera/claims | G0: validate JSON |
| 5. State planning | A/B/C designs | Shared components, variants, transitions | Geometry semantics hợp lý |
| 6. Greybox | States + shots | Stills/contact sheet, animation rough | G2: camera/cấu kiện rõ |
| 7. Audio timing | Locked narration/TTS | Timestamp cue per shot | G4: locked |
| 8. Materials/lighting | Greybox approved | Clean stylized 3D | Sát style bible |
| 9. Batch render/edit | Locked scenes | Shot PNG sequences + video | G3: frame/motion QC |
| 10. Factual & legal QA | Final draft | Final MP4 + source/asset credit | G5: pass |

## Chọn visual đúng mục tiêu
- Thay ý tưởng A → B: `REPLACE_PARTS` nếu khác bộ phận; giữ camera, base geometry chung.
- So sánh thời kỳ: timeline + 3D models + **documented exemplars** + bản đồ. Không ngầm nói phương án trước đã biến mất.
- So sánh địa phương: `SIDE_BY_SIDE`, `CUTAWAY`, cùng tỷ lệ; giới hạn khu vực/thời kỳ rõ.
- Giải thích cơ chế: `EXPLODED_VIEW`, `CAUSE_AND_EFFECT` (dùng mô phỏng vật lý chỉ nếu cần minh họa định tính).
- Cảnh có tư liệu thật phù hợp: ảnh/tài liệu gốc thay cho render 3D; nguồn và license phải được kiểm tra.

## Lập lịch 8–15 phút
- Chia thành **visual beats** dài khoảng 5–20 giây (gợi ý, không ràng buộc cứng), rồi gom thành shots nếu chia quá vụn.
- Tạo audio trước khi render final; lock cue thật, không đo thời lượng từ số chữ rồi coi là chính xác.
- Không render nguyên 15 phút như một scene Blender duy nhất. Theo shot, cache asset và render độc lập.
- Thumbnail và social shorts là deliverable riêng, không làm đổi logic video chính.

## Khi AI được phép tự tiếp tục
- Có thể làm research draft, mã procedural, demo preview, test/validator không cần duyệt từng bước.
- Không được khẳng định historical factual pass khi thiếu nguồn.
- Không được render final dài hoặc đăng YouTube nếu thiếu G1/G4/G5.
