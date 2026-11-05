# M7 finalization: hồ sơ duyệt, cổng xuất bản, bản cuối 4K, hệ thống sản xuất V1

**Nhánh:** `m7-finalization-4k-production`, tách từ `24d13c1`. Chưa merge, chưa push, chưa upload. Ngày 2026-10-30/31.

## 1. Kết luận

| | Trạng thái | Bằng chứng |
|---|---|---|
| **Kỹ thuật** | `TECHNICALLY_VALIDATED`: G0, G3, G4, G5, GL đều PASS trên bản 4K thật | `projects/why-bridges-look-different/qa/gates.json`, `qa/perf/gates_final_4k.log` |
| **Cổng xuất bản** | **`PUBLICATION_READY`**: G0–G6, GL, GV PASS; profile `PUBLICATION_CANDIDATE` | như trên |
| **Xuất bản** | **Chưa xuất bản.** Upload, chọn ngày và các thiết lập YouTube là quyết định của chủ kênh. Studio không bao giờ upload. | – |

PUBLICATION_READY nghĩa là mọi điều kiện mà Studio kiểm được đều đạt, gồm cả các quyết định đã được chủ kênh ghi lại. Nó không thay cho việc chủ kênh xem bản 4K trước khi đăng.

## 2. Hồ sơ duyệt đã ghi (chỉ ghi lại lời chủ kênh)
Tổng hợp ở `review/OWNER_APPROVALS.json` (schema `owner_approvals/1`). Mỗi quyết định có: phạm vi, đối tượng, revision, quyết định, ngày, bằng chứng, nơi áp dụng, điều kiện, điều kiện mất hiệu lực.

| Id | Quyết định | Gắn với | Mất hiệu lực khi |
|---|---|---|---|
| APP-CLAIMS | 41 claim mà phim dùng: EDITORIALLY_APPROVED (giữ nguyên quyết định ngày 2026-10-30) | `research/editorial_approval.json`: `claims_text_sha256` của từng claim, `narration_sha256` `ab0484de…` | câu chữ một claim đổi, hoặc revision lời dẫn đổi. Khi đó `build_sources.py` để claim về SOURCE_VERIFIED. |
| APP-VOICE | Kokoro-82M @ `f3ff3571`, giọng `am_michael`: được phép đăng công khai trên YouTube, kể cả kiếm tiền, **chỉ cho dự án này** | `config/tts_providers.json` → `clearance.voice_approvals` (SHA256 giọng `9a443b79…`). `voices_cleared` vẫn chỉ gồm 4 giọng Anh–Anh. | đổi hash giọng hoặc model, hoặc dùng cho dự án khác |
| APP-PRONUNCIATION | 16 mục trong `review/PRONUNCIATION_REVIEW.md`: `ACCEPTED_BY_OWNER`, tức chủ kênh chấp nhận audio hiện tại | `voice.pronunciation_review.audio_revision` = hash lời dẫn | audio được sinh lại (gate G1 báo "accepted for another audio revision") |
| DISP-CLM_747 | CLM_747 **không dùng** trong phim. Vẫn SOURCE_VERIFIED, **không được duyệt hộ**. | – | – |
| APP-B35 | Bỏ dòng ghi giọng đọc khỏi card B35; mô tả vẫn ghi lời dẫn là giọng AI | – | – |

**Không ghi những điều sau:**
- chủ kênh đã nghe từng mục phát âm;
- đã có một kiểm tra ngữ âm bổ sung;
- một tên hay chữ ký không có trong yêu cầu.

Ghi chú của G1 nói rõ: "current audio accepted by the owner (no per-item listening recorded)".

## 3. CLM_747 và cổng cuối
- **Kiểm chứng CLM_747 không được dùng:** đã kiểm lời dẫn, `visual_beats.json` (beat và chú thích), `visual_plan.json`, `storyboard.json`, manifest chương, mô tả YouTube, phụ đề và metadata MP4. Không chỗ nào dùng CLM_747.
- **Sửa ở cổng cuối** (`tools/validator.py`): cổng chỉ đòi duyệt các claim **mà phim dùng** (`used_claim_ids`: beat lời dẫn, beat hình, chú thích, shot).
  - Claim được dùng mà chưa duyệt vẫn bị chặn.
  - Claim được dùng mà không có trong sổ cũng bị chặn.
  - CLM_747 vẫn nằm trong sổ, kèm cảnh báo "SOURCE_VERIFIED, not editorially approved".
- **Test** (`tests/test_m7_longform.py`): một claim được dùng mà chưa duyệt thì bị chặn; một claim không dùng thì không chặn.

## 4. Kết quả cổng (`gates --preset final_4k`, 2026-10-31)
| Cổng | KQ | Ghi chú |
|---|---|---|
| G0 cấu trúc | PASS | validate |
| G1 bằng chứng, kịch bản, phát âm | PASS | 41 claim duyệt; `factual_review: verified`; audio hiện tại được chủ kênh chấp nhận |
| G2 audio và quyền TTS | PASS | 102 câu riêng biệt (103 câu xếp lịch) qua ASR; Kokoro PUBLICATION_CLEARED; licence giọng APPROVED cho dự án |
| G3 khóa timing | PASS | 15.395 frame |
| G4 QA Blender + media | PASS | Blender QA 577/577 (chạy ở `final_4k` lúc 23:17, sau lần sinh storyboard cuối lúc 23:14); media QA của file 4K thật |
| G5 ghép và phụ đề | PASS | 15.395 frame, −16,4 LUFS, 145 câu phụ đề |
| GL phim dài và quyền ảnh | PASS | 17 kiểm tra đạt, 2 cảnh báo (một câu hỏi lặp có chủ đích; độ đa dạng của C2) |
| G6 sẵn sàng xuất bản | PASS | – |
| GV kế hoạch hình | PASS | 47 shot, 39 beat COVERED |

**Không cổng nào PASS nhờ báo cáo cũ.**
- Lần chạy gates đầu tiên sau khi render cho **GL FAIL**: "long-form QA is stale". Báo cáo được lập trước khi `timing.json` được sinh lại. Timing của các frame không đổi; chỉ hash storyboard và plan đổi, do đường dẫn ảnh 3840 px.
- `chapters --preset final_4k` đã chạy lại kiểm tra thật trên timing hiện tại, rồi mới chạy lại gates. Không sửa ngưỡng hay luật nào.

## 5. Bản cuối
Thư mục `projects/why-bridges-look-different/output/` (không commit):

| File | Kích thước | SHA256 |
|---|---:|---|
| `why_bridges_look_different_FINAL_4K_2160p.mp4` | 303.243.683 B | `7fd17d1041871b95d04d25b33519997ee7f04843e1825a885f25d9e4b94a7807` |
| `why_bridges_look_different_FINAL_4K_2160p.en.srt` | 12.669 B | `3457599753ac0a7baef3d8eae16f3963da21cdc3f1668fe510d557e8bfdaee29` |
| `why_bridges_look_different_audio_master_final_4k.wav` | 61.580.078 B | `1196bb30cf268f1fc52a8a3fe2f0daf727081f0024b6033526b603f949f59102` |
| `why_bridges_look_different_narration_master_clean_final_4k.wav` | 30.790.044 B | `8a16f5b0bdbb4a6ac547144c84bf575a93f8e39ca82d9be6255ed3aafce65448` |
| `why_bridges_look_different_FINAL_4K_2160p.sha256` | – | danh sách trên; `shasum -a 256 -c` OK |

**Thông số:**
- Hình: H.264 High@5.1, 3840×2160, 24/1, yuv420p, BT.709 (space, primaries, transfer), range tv, 15.395 frame, 641,458 s, trung bình 3,6 Mb/s.
- Tiếng: AAC-LC 48 kHz mono, khoảng 164 kb/s.
- Phụ đề: mov_text, `eng`.
- Thời lượng: 10,69 phút.

**Bản review 1080p còn nguyên:**
- File `why_bridges_look_different_M7_FINAL_INTERNAL_REVIEW_1080p.mp4`, mtime 2026-10-30 22:49, trước khi render 4K.
- SHA256 `0ac644d2f5bac86df35e56da25008b1cd3718996fd4ba5743443359a2e211b1c`.

## 6. QA bản cuối
- **Giải mã:** đọc trọn file: 0 lỗi giải mã, 0 đoạn đen. Số frame bằng timing.
- **Thẻ màu:** đúng BT.709. Lỗi `iec61966-2-1` của lần benchmark đầu đã sửa và kiểm lại.
- **Ranh giới chương:** cắt C2→C3 là match cut, SSIM 0,997, không thấy. Các ranh giới khác là hard cut có chủ đích.
- **Native 4K, không phóng to:** 3 frame được render trực tiếp lại để so. MP4 cuối so với render trực tiếp đạt PSNR 49,5 / 50,9 / 57,3 dB; bản 1080p phóng to chỉ đạt 38,3 / 34,8 / 35,9 dB. Chi tiết ở `docs/m7/PERFORMANCE_4K.md` §3.
- **Cùng nội dung với bản đã review:**
  - 48 frame mẫu (cứ 321 frame một mẫu) của bản 4K thu về 1080p, so với bản review: SSIM trung bình 0,995, thấp nhất 0,988 (card ảnh, nay sắc hơn nhờ ảnh 3840 px).
  - Xem contact sheet 24 ô và crop 1:1: không thấy frame hỏng.
- **Audio:**
  - Hai WAV master của bản 4K **giống từng byte** với bản review 1080p (`1196bb30…`, `8a16f5b0…`). Lời dẫn đúng là audio `am_michael` đã được duyệt (hash lời dẫn `ab0484de…`).
  - Độ to −16,4 LUFS, true peak −1,4 dBTP, LRA 4,2 LU (đo lại bằng ebur128 trên MP4).
- **Phụ đề:** SRT giống hệt bản review: 145 câu, dòng dài nhất 42 ký tự. Có cả SRT riêng và track mov_text.
- **Card B35:** đã xem ở 4K. Không còn dòng ghi giọng đọc. Còn: ghi công ảnh HAER/LoC, danh sách nguồn, NOTE "3D models and diagrams are illustrative, not engineering designs", tên Studio.
- **Ảnh ngoài:** 4 ảnh HAER, phạm vi công cộng.
  - Dùng rendition 3840 px từ Wikimedia Commons, có SHA256 và `previous_rendition` trong `assets/manifest.json`.
  - Ghi công có ở card và ở mô tả (`review/YOUTUBE_DESCRIPTION.md`).
  - Mốc chương trong mô tả khớp timing: 0:00 / 0:33 / 1:22 / 2:28 / 3:50 / 5:15 / 7:20 / 9:27.

## 7. Dọn dẹp
Xem `docs/production/CLEANUP_REPORT.md`.
- `projects/` chỉ còn phim này.
- 6 pilot cũ:
  - 286 file tracked được `git mv` làm fixture;
  - 9.979 file sinh ra (3,36 GB) chuyển ra ngoài repo, có checksum, kiểm lại 0 sai lệch;
  - có `git bundle --all`.
- Không xóa code dùng chung, không xóa test, không nới assertion.

## 8. Hệ thống sản xuất V1 (phim mới từ một chủ đề)
- **Tài liệu và prompt:**
  - `docs/production/NEW_DOCUMENTARY_PLAYBOOK.md`: 26 bước, với lệnh có thật;
  - `prompts/NEW_DOCUMENTARY_AUTOPILOT.md`;
  - `config/production_defaults.json`;
  - các mẫu trong `docs/production/templates/`.
- **Lệnh:**
  - `tools/episode.py new|status|next`;
  - alias CLI `new-episode --topic …` và `episode-status`;
  - `--project` giờ mặc định là dự án duy nhất trong `projects/`; có nhiều dự án thì bắt buộc ghi;
  - `evaluate-planning` không còn cần dự án.
- **Đã kiểm chứng:**
  - `tests/test_episode_workflow.py` (9 test): dựng dự án từ một chủ đề giả lập; mặc định của Studio; không lọt nội dung cầu sang dự án mới; từ chối slug xấu; giai đoạn suy từ file; chạy lại cho cùng kết quả; dừng ở OWNER_APPROVAL khi thiếu quyết định; alias CLI.
  - Phim tham chiếu: `episode.py status` cho thấy mọi giai đoạn DONE.
- **Chưa kiểm chứng:** một phim mới trọn vẹn do agent tự làm. Test chỉ chứng minh phần nhận chủ đề và theo dõi giai đoạn. Nghiên cứu, viết, thiết kế hình và QA biên tập vẫn là việc của agent và chưa chạy thử trên chủ đề mới (theo yêu cầu "không bắt đầu phim mới").

## 9. Test
| Bộ | Kết quả |
|---|---|
| Offline (14 module, gồm workflow mới) | 303 test OK |
| Blender (6 module, mỗi lúc một Blender) | 21 test OK (35 s) |
| `evaluate-planning` trên fixture | 29/29 ca; `RESULTS.md` không đổi |
| Trạng thái repo trước và sau test Blender | không đổi (fixture không bị ghi) |

## 10. Những gì không bị đụng tới
- **OmniVoice** (`~/Work/Projects/OmniVoice`): commit cuối `30bb7ac` (2026-05-28). Các file untracked đều có từ tháng 5. File duy nhất mang ngày 30/10 là `.DS_Store` do Finder ghi.
- **Lịch sử git:** mọi branch và tag còn nguyên (`m2-baseline`, `m2.5-validated`, `m3-pilot-preview`, `m7-review-bm_george`, `m7-final-internal-review-1080p`) và nằm trong bundle.
- **Trạng thái `suffolk-roofs`:** không đổi (fixture là rename 100%).

## 11. Việc của chủ kênh
1. Xem bản 4K: `output/why_bridges_look_different_FINAL_4K_2160p.mp4`.
2. Nếu đăng: upload file MP4, file `.en.srt` và mô tả `review/YOUTUBE_DESCRIPTION.md` (bỏ dòng chú thích HTML đầu file). Các thiết lập YouTube (nội dung thay đổi/tổng hợp, kiếm tiền, lịch đăng) do chủ kênh chọn.
3. Merge hay push nhánh `m7-finalization-4k-production` cần một lệnh riêng.
