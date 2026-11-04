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

---

## M8.1 (2026-11-03): ba họ nhịp lớn trong các chương yếu tố, quyết định và kết luận
**Yêu cầu của chủ kênh:** "không cần quá khắt khe về mặt thời gian, thứ tôi muốn là truyền tải đầy đủ nội dung của video, tôi thấy sau phần liệt kê các loại cầu, các phần c8 c9 c10 chỉ nói chủ yếu về beam, arch, truss mà không đề cập đến cantilever, suspension bridge, cable-stayed bridge, hãy nghiên cứu và bổ sung cho phù hợp, lôi cuốn".

**Revision m8-r2:**
- 12 chương, 66 beat, 167 câu, 2.339 từ;
- **19,3 phút** (1.158 s), 75 shot.

### Nội dung mới
| Chương | Thêm gì | Nguồn |
|---|---|---|
| C9 Why different designs exist | Vật liệu của cáp: xích sắt "only as good as the weakest link", rồi cáp dây, rồi thép cường độ cao | NCHRP §3.5, FHWA §2.5–2.6 |
| | Nền đất: cầu treo neo vào khối lớn hoặc đá gốc; tháp dây văng không cần đá gần mặt đất (sơ đồ mặt cắt mới) | NCHRP §3.5, FHWA §2.6, §3.0 |
| | Công-xôn tự điều chỉnh khi trụ lún | NCHRP §3.7 |
| | Gió: Tacoma Narrows 1940, rồi nghiên cứu về gió và tiêu chuẩn mặt cầu tăng cứng (chỉ kể bằng lời, không có hình sập) | NCHRP §2.2, FHWA §2.6 |
| **C10 Span, cost and time** (mới) | Card dải nhịp của sáu họ cho cầu thép | FHWA §3.0 |
| | Chi phí khối neo; tay nghề hiếm và thời gian dựng cầu treo; dây văng phổ biến lên nhờ cách dựng được hiểu rõ hơn | NCHRP §3.7, FHWA §4.4–4.5 |
| | Dòng thời gian thế kỷ 19 (từ M7) và dòng thời gian nhịp lớn (Wheeling 1849, Brooklyn 1883, Queensboro 1909, công-xôn 1880–1960, dây văng từ 1980) | NCHRP, FHWA |
| C11 Real-world decisions | Cầu treo đường sắt Niagara (1855) và "133 years"; công-xôn cứng cho tàu hỏa, hẻm Kentucky 1877; ảnh Golden Gate (1937, nhịp dài nhất suốt 27 năm); Penobscot Narrows (2006) | NCHRP §2.2, §3.5, §3.7; FHWA-HRT-14-067 |
| C12 Why they look different | "Many small suspension bridges were built simply because they were easy to put up" | NCHRP §3.5 |

**Nguồn và ảnh mới:**
- FHWA-HRT-14-067 (Penobscot Narrows, 2014);
- ảnh HAER CA-31 cầu Golden Gate (Jet Lowe, 1984, phạm vi công cộng);
- 14 claim mới (CLM_780–793), tổng 81 claim.

**Thời lượng:**
- Quyết định của chủ kênh được ghi ở `project.json` → `runtime_decision`: khoảng chấp nhận 8–20 phút. Trần 20 phút do agent đặt, vì chủ kênh không nêu con số.
- QA chỉ dùng quyết định này khi bản ghi có đủ người quyết định, ngày và cơ sở (`pipeline/chapters.runtime_range`). Các dự án khác vẫn dùng 8–15 phút.

**Sửa trong quá trình làm:**
- **Đoạn tĩnh 15,2 s ở dòng thời gian nhịp lớn:** sửa bằng cách cho phần tử hiện theo từ được đọc. Mốc Golden Gate (không được nhắc trong câu) được bỏ khỏi dòng thời gian này.
- **4 cảnh 3D_HOLD liền nhau ở C9:** beat dây cáp được chuyển ra sau ảnh cầu có mái che.
- **Card dải nhịp:** hai đầu thanh do agent tự đặt (600 ft, 1.150 ft) bị bỏ. Giàn đơn nay đi từ 450 tới 750 ft theo FHWA, công-xôn chỉ còn mũi tên.
- **Card nền đất:** vẽ lại với các lớp đất và đá rõ ràng.

**Snapshot nguồn** nay nằm ở `research/snapshots/` (git bỏ qua). Snapshot trong scratchpad đã bị hệ thống xóa sau vài ngày. Tải lại thì SHA256 trùng, và registry dựng lại trùng từng byte.

### Kết quả (bản review nội bộ 1080p, m8-r2)
File: `projects/why-bridges-look-different/output/why_bridges_look_different_M8_INTERNAL_REVIEW_1080p.mp4`, không commit.

**Thông số:**
- 1920×1080, 24 fps, 27.828 frame, 1.159,5 s (19:19,5);
- −16,4 LUFS, true peak −1,2 dBTP;
- phụ đề: 264 cue cho 167 câu, dòng dài nhất 42 ký tự, tối đa 18 ký tự/giây.

**Hai lượt render:**
- **Lượt 3** (2026-11-03 23:44 → 2026-11-04 02:47, 3 giờ 03 phút): render đủ 75 shot, không dùng lại được cache nào.
  - 12 shot mới, 15 shot đổi hình.
  - 48 shot render lại chỉ vì khóa cache `project_render` đổi: trường mới `runtime_decision` trong `project.json` không nằm trong `PROJECT_NON_VISUAL` (`tools/render_cache.py`). Pixel của 48 shot này không đổi.
  - **Chưa sửa.** Sửa bây giờ thì mọi bản render 1080p hiện có thành "cũ", dù hình không khác. Đề xuất: thêm `runtime_decision` vào `PROJECT_NON_VISUAL` cùng lần thay đổi kế tiếp mà dù sao cũng phải render lại.
- **Lượt 4** (02:55 → 03:30, 35 phút): sửa 3 lỗi agent tìm thấy khi xem bản lượt 3 (`qa/EDITORIAL_REVIEW_TIMECODED.md`):
  - nhãn "Stiffening truss" ở cảnh Tacoma;
  - NOTE "Niagara Gorge, 1855" ở B31A;
  - tiêu đề cho card dòng thời gian nhịp lớn.
  - Chỉ SC_053, SC_058, SC_066 được render lại. Kiểm lại trên video ở 11:49, 13:25, 16:06 và 16:25: cả ba bản sửa hiện đúng.

**Tốc độ** (`qa/perf/m8/frame_times_internal_1080p_m8r2.json`, đo từ dấu thời gian `Saved:` trong log Blender):
- 9.255/27.828 frame được render riêng (33,3%), phần còn lại là frame tĩnh dùng lại;
- 10.305 s thời gian render khi máy thức, 1,11 s/frame, 0 lần máy ngủ;
- frame của cầu nhịp lớn mất khoảng 2,0 s (median), gấp đôi trung bình;
- 14 GB PNG; đĩa còn 76 GB.

**QA:**

| Kiểm tra | Kết quả |
|---|---|
| QA phim dài | PASS: 17 kiểm tra; 2 cảnh báo (câu hỏi lặp có chủ đích; độ đa dạng của C2). Thời lượng 19,32 phút nằm trong khoảng 8–20 phút của chủ kênh; đoạn tĩnh dài nhất 13,5 s; mọi shot có cache hiện hành |
| Blender QA | 944/944 |
| Kiểm tra lời–hình | không mâu thuẫn; 2 UNCERTAIN cho người duyệt (B33.s4, B34.s2) |
| Ảnh ngoài | 7/7 có hồ sơ quyền và ghi công |
| `gates --preset internal_1080p` | G0, G2, G3, G4, G5, GL, GV PASS → `TECHNICALLY_VALIDATED`. G1 PENDING_EDITORIAL (0/75 claim được lời dẫn dùng đã duyệt; 32 thuật ngữ phát âm chờ). G6 BLOCKED. Kết luận: INTERNAL PREVIEW, NOT PUBLICATION-READY |
| Test offline | 316/316 OK |
| Test Blender | 21/21 OK (toàn bộ 337/337). Test không ghi file nào trong repo: mọi file đổi trong lúc chạy đều là tài liệu agent đang sửa |
| `evaluate-planning` | 29/29 |

**Ước lượng 4K sau khi chủ kênh duyệt:**
- Ở M7, 4K chậm hơn 1080p khoảng 3,1 lần cho mỗi frame (2,69 so với 0,87 s/frame).
- m8-r2 có 10.305 s render 1080p, nên khoảng **8,5–10 giờ** render 4K, chạy theo chương với `--release-frames`. Máy phải thức suốt thời gian đó.
- Ước lượng 5–5,5 giờ trước đây cho m8-r1 tính theo số frame và đã thấp hơn thực tế: frame cầu nhịp lớn tốn gấp đôi.

### Trạng thái duyệt (m8-r2)
- **Claim:** 0/75 claim được lời dẫn dùng đã duyệt cho m8-r2. Duyệt của m7-r1 không áp sang, và builder in ra "editorial approval of narration m7-r1 does not cover m8-r2: NOT applied".
- **Phát âm:** PENDING, 32 thuật ngữ (thêm Tacoma Narrows, Niagara, Penobscot, Kentucky, Golden Gate, Finley).
- **Giọng:** duyệt theo dự án, vẫn giữ.
- **Thời lượng:** quyết định của chủ kênh, ghi ở `DEC-M8.1-CONTENT-AND-RUNTIME`.

### Việc của chủ kênh (m8-r2)
1. Xem bản review M8.1. Các cảnh mới có mốc thời gian ở `qa/EDITORIAL_REVIEW_TIMECODED.md`.
2. Xác nhận hoặc chỉnh trần 20 phút mà agent đặt.
3. Duyệt hoặc sửa claim (`review/EDITORIAL_APPROVAL_PACKAGE.md`, `review/EVIDENCE_MATRIX.md`) và phát âm (`review/PRONUNCIATION_REVIEW.md`).
4. Sau đó: profile PUBLICATION_CANDIDATE, render 4K theo chương.

---

## M8.2 (2026-11-04): sửa nội dung theo nhận xét biên tập của chủ kênh
**Yêu cầu:** "đọc nhận xét sau và sửa nội dung trước, chưa cần tạo video internal review". Chủ kênh rà 75 claim và 32 mục phát âm của m8-r2.
- Đây là **yêu cầu sửa**, không phải duyệt. Bản ghi: `review/OWNER_APPROVALS.json` → `REV-M8.2-EDITORIAL-REVIEW`.
- Chủ kênh nói rõ không coi nhận xét này là chứng nhận độc lập cho cả 75 claim.

**Revision m8-r3:**
- 12 chương, 66 beat, 169 câu, 2.416 từ;
- **19,90 phút** (1.193,8 s, 28.651 frame), 75 shot;
- 82 claim (76 được lời dẫn dùng), 18 nguồn.

### Đã sửa
| # | Nhận xét | Sửa | Claim |
|---|---|---|---|
| 1 | "133 năm mới có cầu treo đường sắt tiếp theo": cầu Williamsburg (1903) có đường ray | Bỏ câu và NOTE; B31A dừng ở "repairs in 1877 and 1880 … declared inadequate in 1890". Phản chứng ghi trong `assumptions` | CLM_789 |
| 2 | Giới hạn 200–300 ft của dầm/vòm kể quá rộng | Bỏ con số; B40 dùng ví dụ của nguồn (sông Ohio, Mississippi, hẻm Niagara) | CLM_757, CLM_752 |
| 3 | Card dải nhịp trộn các loại số khác nghĩa | Lời dẫn và card tách hai loại: viền rỗng = dải thực dụng/kinh tế, đặc = nhịp đã xây; tiêu đề "Two kinds of span numbers"; chân card "ranges, not limits" | CLM_784–786, 775 |
| 4 | Nhận định 2005/2012 nói ở thì hiện tại | Nói kèm năm: B24B, B23E, B33, B09; câu B31D bỏ; B20E "came to rely"; nhãn B53 "by 2012" | CLM_774, 777, 788, 721 |
| 5 | Lợi thế khi trụ lún của công-xôn mất điều kiện | "a continuous girder with hinges built in … its superstructure could adjust" | CLM_782 |
| 6 | Card nền đất ghi "set into rock" | "massive blocks **or** in bedrock", mỗi bờ một cách; móng tháp dây văng trong đất, đá sâu | CLM_761, 776 |
| 7 | Mô hình có nhịp treo đứng trước ảnh Queensboro | B44 thêm câu "Unlike our model, it has no suspended span in the middle…"; card ảnh thêm hai dòng | CLM_794 (mới) |
| nhẹ | B03, B51, B24B, B48, B31B | Lần lượt: "through its supports"; "at the same span" và chiều cao tháp phụ thuộc nhịp; "longest span … when it opened" (thêm nguồn e-WV của Emory L. Kemp); các bộ phận của bản thiết kế cầu Brooklyn; "modern cantilevers … and only later for highways" | CLM_771, 766, 764, 790 |

**Phát âm:**
- **Ghi đè chỉ cho giọng đọc** (`script/pronunciation.json`, `PENDING_LISTENING_REVIEW`):
  - Corinne: /kəɹˈɪn/ (Cambridge; Wikipedia không trích nguồn; chưa có bản ghi giọng địa phương);
  - Cincinnati: /sˌɪnsɪnˈæTi/ (Cambridge).
  - ASR nay nghe "Corrine" (trước là "Kareen") và nghe đúng "Cincinnati". Đây không phải bằng chứng phát âm đúng.
- **Promontory, Covington, Finley:** bỏ khỏi danh sách nghe vì không được đọc trong phim. Danh sách còn 29 thuật ngữ.
- **Bollman, Tacoma Narrows:** để chủ kênh nghe.
- `pronunciation_review` vẫn PENDING. Nhận xét dạng chữ của chủ kênh được ghi ở `owner_text_review`.

**Lỗi hình phát hiện khi xem ảnh preview của 8 card đã sửa** (đã sửa):
- cáp neo vào đá cắt ngang mặt cầu;
- dây văng ngoài cùng ở card nền đất kết thúc ngoài không trung (có từ m8-r2);
- QA phim dài báo đoạn tĩnh 16,2 s ở B33, vì chữ card chờ từ "common" ở cuối câu; nay chữ hiện ở từ "handbook".

### Kiểm tra (không render video, theo yêu cầu)
| Kiểm tra | Kết quả |
|---|---|
| Sổ claim | 18 nguồn, 82 claim, mọi trích dẫn khớp nguyên văn; nguồn mới e-WV có snapshot và SHA256 |
| ASR | PASS, 26 câu mới |
| QA phim dài | PASS: thời lượng 19,90 phút (trong khoảng 8–20); đoạn tĩnh dài nhất 13,5 s; `render_cache_current` WARN: 18/75 shot cần render lại |
| Blender QA | 944/944 |
| `gates --preset internal_1080p` | G0, G2, G3, GL, GV PASS. **G4, G5 FAIL vì media cũ** (chưa render). G1 PENDING_EDITORIAL: 0/76 claim, 2 mục ghi đè, 29 thuật ngữ. G6 BLOCKED |
| Test offline | 320/321. Không đạt duy nhất: `test_final_internal_review_assembly_matches_the_locked_timing` (bản ghép cũ 27.828 frame so với 28.651), sẽ đạt sau khi render |
| Test Blender | 21/21; trạng thái repo không đổi |
| `evaluate-planning` | 29/29 |

**Còn để ngỏ:**
- **Thời lượng 19,90 phút** sát trần 20 phút do agent đặt. Thêm nội dung nữa sẽ vượt trần; khi đó chủ kênh cần quyết định trần mới hoặc chỗ cắt.
- **Render lại:** 18 shot ở 1080p. Theo thời gian render lần trước của chính các shot đó, khoảng 89 phút, cộng thêm preview và ghép phim là khoảng **1,5–1,75 giờ**. Phần lớn thời gian là bốn cảnh push-in (B09, B23E, B31A, B31D), phải render lại vì lời dẫn đổi độ dài.
