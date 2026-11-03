# M8: "Why Bridges Don't All Look the Same" với đủ sáu họ cầu

**Yêu cầu của chủ kênh (2026-10-31):** "kết hợp với nội dung đã có để làm lại project why-bridge-look-different với đầy đủ các loại cầu, đầy đủ các mô hình".

**Nhánh:** `m8-all-bridge-families`, tách từ `c7ef80b`. Bản 4K đã duyệt của m7-r1 được gắn tag `m7-final-4k` và cất ở `projects/why-bridges-look-different/output/baseline_m7_final_4k/` (checksum vẫn OK). Chưa merge, chưa push, chưa upload.

## 1. Phạm vi
- **Sáu họ kết cấu:**
  - dầm, vòm, giàn (từ M7, site 24 m);
  - công-xôn, cầu treo dây võng, cầu dây văng (mới, site 72 m).
- **Không làm mô hình cầu di động** (cầu cất, cầu quay). Đây là loại theo chức năng, không phải họ chịu lực. Vocabulary có `bascule_bridge` với `supported: false`.
- **Phim m8-r1:**
  - 11 chương, 54 beat, 133 câu, 1.786 từ;
  - 14,46 phút (867,6 s), trong khoảng cho phép 8–15 phút;
  - 63 shot;
  - giọng `am_michael`, như m7-r1.

## 2. Nghiên cứu
- **Nguồn mới:** FHWA *Steel Bridge Design Handbook: Selecting the Right Bridge Type* (FHWA-IF-12-052, vol. 5, 2012).
  - URL FHWA trả 404, ROSAP chặn truy cập tự động, nên PDF tải từ bản lưu Internet Archive của chính URL FHWA.
  - Các mảnh watermark "Archived" được bỏ trước khi khớp trích dẫn.
- **Nguồn đã có, dùng thêm:** NCHRP 25-25(15) §3.1, §3.5 Suspension, §3.7 Cantilevers.
- **25 claim mới** (CLM_750–777), khớp nguyên văn. Đều SOURCE_VERIFIED, chưa claim nào được duyệt. Ví dụ:
  - cầu công-xôn là dạng cải biến của dầm; gồm tay neo, tay hẫng và nhịp treo; dựng ra từ trụ không cần đà giáo, rồi nâng nhịp treo vào chỗ;
  - mặt cầu treo được treo bằng dây treo đứng vào cáp chịu kéo, cáp vắt qua tháp chịu nén, đầu cáp neo vào khối đá hoặc bê tông;
  - dây văng đi xiên từ tháp xuống dầm biên; tháp rất cao; dây không dốc dưới khoảng 22°; dựng hẫng cân bằng không cần tháp đà giáo;
  - kinh tế nhịp lớn ở Mỹ: dây văng rất cạnh tranh trên 750 ft; cầu treo chỉ có lợi khi nhịp gần 3.000 ft;
  - dầm thép tổ hợp hàn (một dạng dầm) là loại cầu thép phổ biến nhất.
- **Không có câu nguyên văn nào nói dây văng chịu kéo**, nên phim không gắn nhãn kéo cho dây văng. Chỉ có mũi tên nén dọc mặt cầu, theo FHWA (CLM_773).
- **Ảnh mới** (phạm vi công cộng, HAER/LOC):
  - Queensboro Bridge, NY-19 (Jet Lowe, 1991);
  - Brooklyn Bridge, NY-18 (ảnh màu trước 1982).
  - Không có ảnh phạm vi công cộng phù hợp cho cầu dây văng.

## 3. Mô hình và engine
- **Bộ sinh** `bridge.cantilever`, `bridge.suspension`, `bridge.cable_stayed`:
  - kèm tham số, kiểm tra chéo hình học (dây văng ≥ 22°, cáp cách mặt cầu ≥ 0,8 m, công-xôn sâu nhất ở trụ…), số bộ phận kỳ vọng và cấu hình nổ tách;
  - kiểu ngữ nghĩa mới: ANCHOR_ARM, CANTILEVER_ARM, SUSPENDED_SPAN, TOWER, PYLON, MAIN_CABLE, HANGER, STAY_CABLE, ANCHORAGE, STIFFENING_TRUSS;
  - vật liệu mới `cable`.
- **Site mới** `site_river_crossing_72` (khoảng hở 72 m, mặt cầu 6 m).
  - Ảnh xem trước asset tự chọn site khớp (`assets.site_for`).
- **Kiểm tra:**
  - offline 8/8 cho mỗi cầu;
  - Blender 4/4 cho mỗi asset (BVH; danh sách giao nhau có chủ đích nay gồm cáp neo vào khối neo, dây văng vào dầm, giằng vào giàn);
  - dựng hai lần cho cùng kết quả.
- **Planner:**
  - concept có thể khai báo `scene_context` và `site`, nên mỗi ngữ cảnh có site và trạng thái site trống riêng (`site_long_span`);
  - shot ứng viên của bộ bố cục mang `scene_context`; lỗi này có từ M6 nhưng chưa từng lộ ra.
- **Mặt đất** nới từ 160 m lên 1 km (nửa cạnh), để cảnh so sánh xếp chồng ba mô hình 72 m không lộ mép.

## 4. Kịch bản (m8-r1)
| Chương | Nội dung |
|---|---|
| C1 Hook | Ba cầu trên khoảng hở 24 m, rồi ba cầu nhịp lớn trên sông rộng, mỗi shot một cầu |
| C2–C5 | Bài toán chung, dầm, vòm, giàn (giữ từ m7-r1) |
| **C6 The cantilever** | Vì sao cần nhịp dài hơn; cánh tay / tấm ván nhảy; tay neo, tay hẫng, nhịp treo (nhãn trên mặt đứng); nổ tách nâng nhịp treo; ảnh Queensboro |
| **C7 The suspension bridge** | Dây treo và cáp chính; cáp kéo, tháp nén, khối neo; giàn tăng cứng; ảnh Brooklyn |
| **C8 The cable-stayed bridge** | Dây văng xuống mép mặt cầu; sơ đồ so sánh với cầu treo; dựng hẫng cân bằng (các đốt mặt cầu trở lại từ tháp ra ngoài) và mặt cầu bị nén; kinh tế nhịp lớn |
| C9–C10 | Các yếu tố quyết định; ba ví dụ thật thế kỷ 19 |
| C11 | Câu trả lời cho cả sáu họ; "không phải chuyện tiến bộ tuyến tính" (cầu thép phổ biến nhất vẫn là một dạng dầm) |

**Đã bỏ để giữ thời lượng ≤ 15 phút** (bản khóa đầu dài 15,4 phút):
- card thanh nhịp ngắn và cảnh site trống trước nó (B23, B23B): chương 6–8 đã nói về nhịp, kèm số liệu có nguồn;
- dòng thời gian nhịp lớn (B24B);
- một câu mở đầu ở B53.

**Sửa câu chữ** (ghi trong `narration.template.json` → `revision.edits`):
- B01C.s0 "great" → "huge" (ASR nghe nhầm thành "grate");
- B51.s0 "Side by side…" → "Seen in outline…", vì kiểm tra lời–hình phát hiện câu hứa hai mô hình cùng lúc nhưng hình là sơ đồ.

## 5. Kết quả (bản review nội bộ 1080p)
File: `projects/why-bridges-look-different/output/why_bridges_look_different_M8_INTERNAL_REVIEW_1080p.mp4`, không commit.

**Thông số:**
- 1920×1080, 24 fps, 20.823 frame, 867,6 s;
- −16,4 LUFS, true peak −1,0 dBTP;
- phụ đề: 199 câu, SRT + mov_text.

**Hai lượt render:**
- **Lượt 1** (2026-10-31 23:04 → 2026-11-01 01:01): agent xem lại các chương mới bằng tấm ảnh mỗi 3 s và frame gốc, rồi tìm ra 5 lỗi hình (`qa/EDITORIAL_REVIEW_TIMECODED.md`).
  - Sau khi sửa, ảnh tĩnh render lại cho thấy đủ 5 chỗ.
  - 12 shot của C1–C3 bị render lại ở bước preview, vì agent đã sửa hai file engine khi C3 đang chạy (khóa cache tính cả file engine).
- **Lượt 2** (01:05 → 02:57, 1 giờ 53 phút):
  - 6.853/20.823 frame được render (32,9%), phần còn lại là frame tĩnh dùng lại;
  - 0,91 s/frame khi máy thức (6.256 s), 0 lần máy ngủ;
  - Blender RSS tối đa 0,95 GiB;
  - 10 GB PNG; đĩa còn 79 GB.

**QA:**

| Kiểm tra | Kết quả |
|---|---|
| QA phim dài (`qa/longform_qa.json`) | PASS: 17 kiểm tra; 2 cảnh báo (câu hỏi lặp có chủ đích; độ đa dạng của C2); đoạn tĩnh dài nhất 12,4 s; mọi shot có cache hiện hành |
| Blender QA | 792/792 |
| Kiểm tra lời–hình | không mâu thuẫn; 2 UNCERTAIN cho người duyệt (B33.s3, B34.s2) |
| Ảnh ngoài | 6/6 có hồ sơ quyền và ghi công |
| `gates --preset internal_1080p` | G0, G2, G3, G4, G5, GL, GV PASS → `TECHNICALLY_VALIDATED`. G1 PENDING_EDITORIAL (0/58 claim được lời dẫn dùng đã duyệt; 26 thuật ngữ phát âm chờ). G6 BLOCKED. Kết luận: INTERNAL PREVIEW, NOT PUBLICATION-READY |
| Test offline | 314/314 OK (gồm 11 test M8 mới) |
| Test Blender | 21/21 OK; trạng thái repo không đổi |
| `evaluate-planning` | 29/29 |

**Ước lượng 4K sau khi chủ kênh duyệt:**
- 6.853 frame riêng biệt, so với 5.218 của m7-r1 (3 giờ 59 phút).
- Vì vậy khoảng 5–5,5 giờ, chạy theo chương với `--release-frames`.

## 6. Trạng thái duyệt
Xem `review/OWNER_APPROVALS.json` (REQ-M8-ALL-FAMILIES).
- **Claim:** duyệt 41 claim gắn với m7-r1, không áp sang m8-r1. Builder nay kiểm `narration_revision`.
- **Phát âm:** PENDING, gồm 26 thuật ngữ (thêm cantilever, Queensboro, Brooklyn, Roebling…).
- **Giọng:** duyệt theo dự án, vẫn giữ.
- **Profile:** NARRATED_INTERNAL_REVIEW; `factual_review` là pending.

## 7. Việc của chủ kênh
1. Xem bản review M8.
2. Duyệt hoặc sửa các claim mà phim dùng (`review/EDITORIAL_APPROVAL_PACKAGE.md`, `review/EVIDENCE_MATRIX.md`).
3. Phát âm m8-r1 (`review/PRONUNCIATION_REVIEW.md`).
4. Xác nhận lại hoặc rút duyệt giọng cho bản mới.
5. Sau đó: profile PUBLICATION_CANDIDATE, render 4K theo chương.
