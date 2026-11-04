# Current project status

- Phase: **M8.2: nội dung sửa theo hai lần nhận xét biên tập của chủ kênh (2026-11-04), revision m8-r4. Chưa render m8-r4, theo yêu cầu.** Nhánh `m8-all-bridge-families` (tách từ `c7ef80b`), chưa merge, chưa push, chưa upload.
- **Phim `why-bridges-look-different`, revision m8-r4:**
  - 12 chương; 19,92 phút (1.195,3 s, 28 687 khung); 169 câu; 75 shot, 2 shot cần render lại (SC_058 B24B, SC_073 B33);
  - thời lượng theo quyết định của chủ kênh (`project.json` → `runtime_decision`, chấp nhận 8–30 phút; trần 30 do agent chọn);
  - giọng `am_michael`; hai mục ghi đè phát âm (Corinne, Cincinnati) chờ chủ kênh nghe;
  - 82 claim SOURCE_VERIFIED (76 được lời dẫn dùng), 18 nguồn; 7 ảnh HAER phạm vi công cộng.
- **Trạng thái:** INTERNAL REVIEW (`NARRATED_INTERNAL_REVIEW`).
  - Hai lần nhận xét của chủ kênh ngày 2026-11-04 là yêu cầu sửa (`REV-M8.2-EDITORIAL-REVIEW`, `REV-M8.2-SECOND-TEXT-REVIEW`), không phải duyệt.
  - Duyệt claim và phát âm của m7-r1 không áp sang m8-r4. Duyệt giọng theo dự án vẫn giữ.
  - Video review 720p hiện có (`output/why_bridges_look_different_M8_INTERNAL_REVIEW_720p.mp4`) là của **m8-r3**: chưa có câu B33 và hai card B24B, B33 đã sửa. Gates: G4/G5 FAIL vì media cũ; test ghép video 1 FAIL vì cùng lý do, cho tới khi render lại.
  - Bản 4K đã duyệt của m7-r1: tag `m7-final-4k`, `output/baseline_m7_final_4k/`.
- Tài liệu: `docs/m8/M8_REPORT.md`.

## Việc của chủ kênh
1. Đọc các chỗ sửa của m8-r4 (`review/EDITORIAL_NOTES.md`), rồi cho render lại 2 shot và ghép bản 720p (SC_058, SC_073; vài phút cho shot, cộng thời gian ghép 12 chương).
2. Duyệt hoặc sửa claim (`review/EDITORIAL_APPROVAL_PACKAGE.md`, `review/EVIDENCE_MATRIX.md`), phát âm (`review/PRONUNCIATION_REVIEW.md`), và xác nhận lại giọng.
3. Sau khi duyệt: profile `PUBLICATION_CANDIDATE`, render 4K theo chương (`docs/m7/REPRODUCIBILITY.md` §8).

---

## M7 finalization (2026-10-31, revision m7-r1, trạng thái lúc đó)

- Phase: **M7 finalization và hệ thống sản xuất V1: xong (2026-10-31).** Nhánh `m7-finalization-4k-production` (tách từ `24d13c1`), chưa merge, chưa push, chưa upload.
- **Phim `why-bridges-look-different`** "Why Bridges Don't All Look the Same":
  - bản cuối **native 4K** `output/why_bridges_look_different_FINAL_4K_2160p.mp4`:
    - 3840×2160, 24 fps, H.264 BT.709, AAC, phụ đề SRT + mov_text;
    - 10,69 phút, 15.395 frame;
    - kèm WAV master và `.sha256`;
  - cổng `gates --preset final_4k`: **G0–G6 + GL + GV PASS → `PUBLICATION_READY`**, profile `PUBLICATION_CANDIDATE`.
- **Hồ sơ duyệt của chủ kênh** (`review/OWNER_APPROVALS.json`), mỗi quyết định gắn với revision:
  - 41 claim được phim dùng;
  - giọng `am_michael` cho dự án này (đăng YouTube công khai, kể cả kiếm tiền);
  - chấp nhận audio hiện tại cho 16 mục phát âm, không ghi là đã nghe từng mục;
  - CLM_747 không dùng trong phim và không được duyệt hộ.
- **Render 4K:**
  - theo chương, dùng lại frame tĩnh: 5.218/15.395 frame được render;
  - 3 giờ 59 phút, không lần nào máy ngủ;
  - PNG chiếm tối đa 14,3 GB, Blender RSS tối đa 3,9 GB.
- **Kiểm chứng:** MP4 cuối so với render trực tiếp đạt PSNR 49–57 dB (1080p phóng to: 35–38 dB). Audio và phụ đề giống từng byte với bản review.
- **Dọn dẹp:** `projects/` chỉ còn phim này. Các pilot M2–M6 ở `tests/fixtures/legacy_projects/`; bản lưu trữ ngoài repo có checksum và `git bundle`.
- **Phim mới:** `docs/production/NEW_DOCUMENTARY_PLAYBOOK.md`, `prompts/NEW_DOCUMENTARY_AUTOPILOT.md`, `tools/episode.py` (`new-episode` / `episode-status` trong CLI). Mới kiểm chứng phần nhận chủ đề và theo dõi giai đoạn, chưa làm thử một phim mới trọn vẹn.
- **Test:** offline 303 OK; Blender 21 OK; `evaluate-planning` 29/29.
- Tài liệu: `docs/m7/M7_FINALIZATION_REPORT.md`, `docs/m7/PERFORMANCE_4K.md`, `docs/production/CLEANUP_REPORT.md`.

### Việc của chủ kênh lúc đó
1. Xem bản 4K trước khi đăng.
2. Nếu đăng: tự upload MP4 + `.en.srt` + `review/YOUTUBE_DESCRIPTION.md` và chọn các thiết lập YouTube. Studio không upload.
3. Merge hay push nhánh cần một lệnh riêng.
4. Phim tiếp theo: đưa một chủ đề, theo `prompts/NEW_DOCUMENTARY_AUTOPILOT.md`.

---

## M7 bản review nội bộ cuối (2026-10-30, trạng thái lúc đó)

- Phase: **M7: phim tài liệu dài đầu tiên. Bản review nội bộ cuối 1080p xong (2026-10-30), chưa sẵn sàng xuất bản.** Nhánh `m7-final-internal-review` (tách từ `m7-first-full-documentary`), chưa merge, chưa push. Bản `bm_george` trước đó: tag `m7-review-bm_george`.
- **Phim `why-bridges-look-different`** "Why Bridges Don't All Look the Same":
  - **10,69 phút** (641,46 s, 15.395 frame); 8 chương, 39 beat, 103 câu, 47 shot;
  - lời dẫn **`am_michael`** (Kokoro-82M @ `f3ff3571`, G2P Anh–Mỹ);
  - **41/41 claim được lời dẫn dùng đã được chủ kênh duyệt** (2026-10-30); `factual_review: verified`;
  - card B35 không còn dòng ghi giọng đọc;
  - QA Blender 577/577; media QA PASS; −16,4 LUFS; 145 câu phụ đề; QA phim dài PASS.
- **Trạng thái:** `TECHNICALLY_VALIDATED` · `EDITORIAL_REVIEW_PENDING` (phát âm) · `TTS_RIGHTS_PENDING` (`am_michael` chưa được cấp quyền xuất bản). G6 BLOCKED.
- **Đầu ra** (không commit; `projects/why-bridges-look-different/output/`):
  - `why_bridges_look_different_M7_FINAL_INTERNAL_REVIEW_1080p.mp4` + `.en.srt`;
  - 8 chương 1080p (`chapters_internal_1080p/`);
  - master audio;
  - bản `bm_george` cũ (`baseline_bm_george_m7r1/`).
- **Render 1080p:** dùng lại frame tĩnh, chỉ render 5.206/15.395 frame; khoảng 1,26 giờ render khi máy thức; 82 phút wall cho C2–C8 + ghép.
- Tài liệu: `docs/m7/` (đặc biệt `FINAL_INTERNAL_REVIEW.md`).

### Việc cần quyết định lúc đó (đã giải quyết ở M7 finalization)
1. ~~Duyệt 41 claim~~ (đã xong, 2026-10-30). Còn CLM_747 (không dùng trong phim): duyệt, hoặc loại khỏi registry. Cổng cuối đòi mọi claim trong registry phải được duyệt.
2. Cấp quyền xuất bản cho `am_michael` (thêm vào `voices_cleared`) và xác nhận cho phim (`owner_confirmation_for_this_film`).
3. Nghe phát âm 16 thuật ngữ với `am_michael` (`review/PRONUNCIATION_REVIEW.md`). ASR nghe sai tên riêng (Bollman, Corinne, Gwynns Falls).
4. Sau đó: profile `PUBLICATION_CANDIDATE` + `publication_metadata`, rồi render bằng preset `final`.
5. Có sửa ghi chú chân trang của `suffolk-roofs` SC_004 hay không (lỗi bố cục có từ M3).

### Lệnh tái tạo M7
Xem `docs/m7/REPRODUCIBILITY.md` (lệnh đầy đủ + kế hoạch kiểm tra build sạch).

---

## M6 (đã xong, 2026-10-29)

- Phase: **M6: phim tài liệu có lời dẫn. Xong (2026-10-29).** Nhánh `m6-narrated-documentary` đã merge fast-forward vào `master` theo yêu cầu của chủ kênh (repo không có remote, không push).
- **Quyết định của chủ kênh (Tran Nam Anh), 2026-10-29:** cấp quyền xuất bản cho Kokoro; duyệt 14 claim (narration `m6-r2`); chấp nhận phát âm; giọng `bm_george`. Mọi gate G0–G6 + GV PASS. Profile vẫn `NARRATED_INTERNAL_REVIEW`: cần chuyển sang `PUBLICATION_CANDIDATE` + `publication_metadata` để đánh giá PUBLICATION_READY.
- **Pilot `bridge-load-explained`** "How Does a Bridge Carry Its Load?":
  - 8 beat, 14 claim EDITORIALLY_APPROVED (ODOT/FHWA/SCI/Yale);
  - 26 câu Kokoro **`bm_george`** (giọng do người dùng chọn ngày 2026-10-29; 143.4 wpm);
  - 11 shot, 151.33 s, 27 chú thích kỹ thuật;
  - QA Blender 176/176; media QA PASS; assemble −16.0 LUFS, 35 câu phụ đề (SRT + mov_text);
  - gate: G0–G6 + GV PASS, trạng thái `TECHNICALLY_VALIDATED`; kết luận "INTERNAL REVIEW — ALL GATES PASS" (chờ đổi profile).
  - Video: `projects/bridge-load-explained/output/bridge_load_explained_pilot_review.mp4` (lời dẫn PUBLICATION_CLEARED).
- **TTS:** Kokoro-82M được audit và **được chủ kênh cấp quyền xuất bản** (`PUBLICATION_CLEARED`, clearance 2026-10-29; các điểm mở của audit §5 vẫn ghi lại). Giọng kênh `bm_george`, license giọng APPROVED. OmniVoice không đổi (`INTERNAL_PREVIEW_ONLY`), không dùng cho M6.
- **Đa họ kiến trúc:** scene context (schema 3). Fixture cầu + mái: QA Blender 69/69. Dự án một họ giữ schema 2 giống hệt.
- **bridge-story-m5:** B7 đổi thành "Let's compare them one at a time: …"; bộ kiểm nhất quán báo CONSISTENT.
- **Suffolk-roofs:** không đổi: `TECHNICALLY_VALIDATED` · `EDITORIAL_REVIEW_PENDING` · `TTS_RIGHTS_PENDING`.
- Test: 250/250 (234 offline + 16 Blender). Đánh giá planner 29/29.
- Hồi quy QA Blender:

  | Dự án | QA Blender |
  |---|---|
  | bridge-story-m5 | 188/188 |
  | roof-plan-m5 | 52/52 |
  | suffolk-roofs | 71/71 |
  | roof-evolution | 64/64 |
  | bridge-structure-evolution | 92/92 |

  Các preview không lời đã render lại bằng engine M6 (media QA PASS).
- Máy: Apple M4 Pro 24 GB, Blender 5.2.2 LTS, FFmpeg 9.0.1, Python 3.14.6.

## Lệnh tái tạo M6
```bash
P="--project bridge-load-explained"
python3 tools/cli.py narrate $P && python3 tools/cli.py asr-check $P && python3 tools/cli.py align $P
python3 tools/cli.py lock-audio $P && python3 tools/cli.py plan-visuals $P && python3 tools/cli.py build-shots $P
python3 tools/cli.py check-blender $P --preset review
python3 tools/cli.py smoke $P --shot SC_003 --preset review
python3 tools/cli.py preview $P --preset review && python3 tools/cli.py assemble $P --preset review
python3 tools/cli.py still $P --preset production_test             # 11 still 1080p
python3 tools/cli.py research-map $P && python3 tools/cli.py gates $P --preset review
python3 -m unittest discover -s tests
```

## Việc người dùng cần quyết định (M6)
1. ~~Chọn giọng kênh~~, ~~cấp quyền xuất bản Kokoro~~, ~~duyệt 14 claim~~, ~~xác nhận phát âm~~, ~~merge vào master~~: đã xong ngày 2026-10-29.
2. Còn lại để đăng: chuyển `production_profile` sang `PUBLICATION_CANDIDATE` với `publication_metadata` (title, description, language, credits; nên ghi "AI-generated narration (Kokoro-82M)"), chạy lại `gates`, rồi render bản final nếu muốn độ phân giải cao hơn review 960×540.

## Lệnh tái tạo M5
```bash
P="--project bridge-story-m5"
python3 tools/cli.py plan-visuals $P        # visual_plan.json + qa/VISUAL_COVERAGE.md
python3 tools/cli.py validate-plan $P
python3 tools/cli.py build-shots $P         # states/storyboard/project.json
python3 tools/cli.py check-blender $P
python3 tools/cli.py still $P --preset review
python3 tools/cli.py preview $P             # 640×360 → output/bridge_story_m5_preview.mp4
python3 -m unittest tests.test_m5_planner tests.test_blender_m5
```

## Lệnh tái tạo M4
```bash
python3 tools/cli.py asset-check                                   # G4-A + G4-B offline
python3 tools/cli.py asset-render --preset review                  # preview đa góc + QA BVH + build hai lần
python3 tools/cli.py asset-catalog                                 # asset_library/catalog/
python3 tools/make_bridge_pilot.py                                 # states/storyboard của pilot từ spec
P="--project bridge-structure-evolution"
python3 tools/cli.py validate $P && python3 tools/cli.py check-blender $P
python3 tools/cli.py preview $P                                    # 640×360 → output/bridge_structure_evolution_preview.mp4
python3 -m unittest discover -s tests                              # toàn bộ test (docs/m5/M5_QA_REPORT.md §9)
```

## Giới hạn đã biết
- M6 (`docs/m6/M6_QA_REPORT.md` §7):
  - GHOST ván gỗ (B3) đúng về hình học nhưng khó thấy, vì ván và dầm cùng màu;
  - exploded view toàn mô hình có thể ra khỏi khung khi nhóm camera chỉ có một mô hình nhỏ (lỗi từ M5);
  - luật nhất quán dựa trên cụm từ gợi ý; trái/phải luôn UNCERTAIN;
  - chú thích chỉ gắn vào phần đứng yên;
  - chưa xác minh file font cụ thể đứng sau `<builtin>`.
- Render của các dự án cũ đã cũ theo khóa engine sau M6. Lần `preview` tới sẽ render lại; output đã kiểm chứng vẫn được giữ.
- M5.5: L1/L2 đo bằng lưới mẫu (không phải phần trăm bề mặt chính xác); proxy mái lệch tới khoảng 5 điểm; ngưỡng mới được hiệu chỉnh trên hai pilot; so sánh tuần tự ở B7 chỉ khoảng 2 s mỗi cầu; độ tương phản màu chưa được đo.
- M5: timing PROVISIONAL là ước lượng; chưa có template bản đồ / ảnh tư liệu / mũi tên lực; mỗi dự án chỉ một họ công trình. (Việc kiểm tra offline không xét vật che đã được giải quyết ở M5.5.)
- Các mô hình cầu là minh họa; không có phân tích kết cấu. Chỉ có vòm bán nguyệt. Thanh giàn là thanh vuông.
- Khung so sánh ba cầu nhỏ ở 640×360. `layout: STACK` không hỗ trợ intro.
- Render của các project cũ sẽ chạy lại một lần nếu chạy `preview` (khóa cache v3); output đã kiểm chứng vẫn được giữ.
- Chưa kiểm tra trên Blender 4.5 LTS, cũng chưa đo trên máy M4 16 GB.
