# Playbook: từ một chủ đề tới bản review và bản cuối

Quy trình đã kiểm chứng trên phim tham chiếu M7 `projects/why-bridges-look-different`: 10,7 phút, 8 chương, bản review 1080p và bản cuối 4K. Mọi lệnh dưới đây đều có thật trong repo.

**Ai làm gì:**
- **AGENT:** Claude Code. Đảm nhận nghiên cứu, viết, chọn chiến lược hình, xem lại và sửa.
- **CLI:** `tools/cli.py` và `tools/*.py`. Tất định, không gọi LLM khi render.
- **OWNER:** chủ kênh. Chỉ người này duyệt.

`python3 tools/episode.py status|next --project <slug>` suy ra giai đoạn hiện tại từ chính các file, nên phiên làm việc nào cũng tiếp tục được từ chỗ dừng.

## 0. Mặc định (không hỏi lại người dùng)
`config/production_defaults.json`:
- tiếng Anh, 16:9, 24 fps;
- độ dài mục tiêu 10–12 phút (chấp nhận 8–15);
- phong cách Premium Clean Stylized Architectural 3D (`config/visual_style.json`, `config/annotation_style.json`);
- lời dẫn Kokoro-82M @ `f3ff3571`, giọng `am_michael` (`lang_code='a'`);
- preset: `preview` cho rough cut, `review`/`internal_1080p` cho bản review, `final_4k` cho bản cuối;
- mỗi lúc một Blender.

Chỉ hỏi người dùng khi cần một quyền hạn, khi sự thật không phân định được, hoặc khi có quyết định tốn tiền.

## 1–2. Nhận chủ đề và phạm vi nghiên cứu
```bash
python3 tools/episode.py new --topic "<chủ đề>"     # tạo projects/<slug>/ + research/RESEARCH_BRIEF.md + review/FINAL_APPROVAL_CHECKLIST.md
```
Có thể dùng alias CLI: `python3 tools/cli.py new-episode --topic "<chủ đề>"` và `python3 tools/cli.py episode-status --project <slug>`. Khi `projects/` có từ hai dự án trở lên, mọi lệnh `tools/cli.py` cần `--project`.
AGENT viết câu hỏi trung tâm và câu hỏi nghiên cứu vào `research/RESEARCH_BRIEF.md`.

## 3. Thu thập và kiểm nguồn (AGENT)
- Ưu tiên cơ quan nhà nước, đại học, tổ chức kỹ thuật, tổ chức bảo tồn, tài liệu gốc. Không chỉ dựa vào Wikipedia.
- Tải nguồn về và trích văn bản (`pdftotext`, HTML), rồi ghi SHA256 và URL vào `research/source_snapshots.json`.
- Nguồn nào không mở được thì không được nói là đã đọc.

## 4–6. Thiết kế câu chuyện, viết kịch bản, sổ claim (AGENT)
- `research/build_sources.py` (xem bản M7) sinh `research/sources.json`: mỗi claim có trích nguyên văn, vị trí, giả định, mức tin cậy, `review_status: SOURCE_VERIFIED`. Script **khớp nguyên văn** từng trích dẫn với văn bản nguồn.
- `script/story.py` là **nguồn duy nhất** của kịch bản: sinh `narration.json`, `visual_beats.json` và `chapters.json` với cùng câu chữ. Card và chú thích được khai báo ngay trong beat.
  - Các mẫu card (`photo_card`, `timeline`, panel), cách tính bề rộng chữ (`text_width`, `clamp_x`) và cách dùng `sentence`/`until`/`word`: xem `projects/why-bridges-look-different/script/story.py`. Chỉ chép **cách làm**, không chép claim, nội dung về cầu hay id beat.
- Luật nội dung:
  - không bịa số;
  - không kể chuyện tiến bộ tuyến tính, không nói một kiểu luôn tốt hơn;
  - mô hình đứng cạnh công trình thật phải mang NOTE "Illustrative model, not the …";
  - đánh dấu nén/kéo chỉ khi có trường hợp tải được ghi lại.
  - nhận định có năm của nguồn (ví dụ sổ tay 2012) được nói kèm năm, không chuyển sang thì hiện tại; giữ đủ điều kiện của nguồn (nơi, cỡ nhịp, dạng kết cấu) (M8.2);
  - trích đúng nguồn chưa đủ: một câu nguồn có phản chứng đã biết thì không dùng, và ghi lý do vào `assumptions` của claim (M8.2, "133 years");
  - không đặt các con số khác nghĩa trên cùng một thang mà không phân biệt, ví dụ dải kinh tế và nhịp đã xây (M8.2).
- **Lời kêu gọi cuối phim** (yêu cầu của chủ kênh, 2026-11-05; `production_defaults.json` → `closing_call_to_action`):
  - một beat `framing` trong chương cuối, sau kết luận và trước card ghi công;
  - mời người xem gợi ý chủ đề trong phần bình luận, like và subscribe; tối đa 60 từ;
  - không trích claim, không hứa điều Studio không kiểm được (lịch đăng, trả lời mọi bình luận, tên video sau), không thúc ép;
  - trên hình chỉ là chữ theo phong cách Studio, không logo, nút bấm hay nhãn hiệu của nền tảng;
  - `episode.py status` chặn bước SCRIPT khi thiếu (chỉ với dự án tạo sau quy định này).

### Khi chủ kênh muốn đọc kịch bản trước (2026-11-05)
Nếu chủ kênh yêu cầu xem kịch bản trước khi có video:
- làm tới `lock-audio` và `plan-visuals`, rồi dừng; không render, không dựng asset mới (kịch bản có thể đổi);
- `python3 tools/script_review.py --project <slug> --audio` sinh `review/SCRIPT_REVIEW.md` (đúng câu đã đọc, mốc thời gian, loại hình, claim, phát âm) và một bản nghe thử trong `output/`; phần quyết định do AGENT viết ở `review/SCRIPT_REVIEW_NOTES.md`;
- audio nháp không vào git cho tới khi kịch bản được duyệt.

## 7–8. Tính khả thi về hình và beat (AGENT, kiểm bằng CLI)
- Mỗi beat có ý đồ, claim, mục tiêu hình, concept bộ phận, chiến lược và phương án dự phòng.
- Chiến lược có sẵn: HOLD, HOLD_HIGHLIGHT, ASSEMBLE_IN, EXPLODE, HIGHLIGHT_THEN_EXPLODE, CLOSEUP_EXPLODE, HIGHLIGHT_REPLACE_HIGHLIGHT, COMPARE_SIDE_BY_SIDE, DETAIL_THEN_OVERVIEW, SITE_HOLD, CARD; HOLD có thể kèm `camera_move: PUSH_IN`.
- Trộn 3D, sơ đồ, bản đồ sơ lược, dòng thời gian và ảnh có quyền. Tránh chuỗi 2D dài.

## 9–10. Tìm và tạo asset
- `python3 tools/cli.py asset-catalog` liệt kê thư viện:
  - cầu trên site 24 m: dầm gỗ, vòm đá, giàn Pratt/Warren;
  - cầu nhịp lớn trên site 72 m (M8): công-xôn, cầu treo, dây văng;
  - nhà, mái (gồm states mái cũ ở `asset_library/legacy_states/`), site.
- Một concept cần site riêng thì khai báo `scene_context` và `site` trong `config/visual_vocabulary.json` (xem M8).
- Asset mới: viết spec trong `asset_library/architecture/`, chạy `asset-check --asset …` và `asset-render --asset …`. Chỉ tạo khi thật sự cần.
- Ảnh ngoài: hồ sơ đầy đủ trong `assets/manifest.json` (`EXTERNAL_LICENSE_FIELDS`, `credit_keys`, SHA256, rendition).

## 11. Chú thích kỹ thuật
Theo `docs/m6/ANNOTATION_STYLE_GUIDE.md`. NOTE dùng cho tiêu đề chương và nhãn mô hình minh họa. Chú thích theo câu (`sentence`/`until`) hoặc theo từ (`word`).

## 12–14. Lời dẫn, phát âm, khóa audio (CLI)
```bash
P="--project <slug>"
python3 projects/<slug>/script/story.py
python3 tools/cli.py narrate $P --purpose publication     # chỉ sinh câu mới; giọng phải đã audit
python3 tools/cli.py asr-check $P && python3 tools/cli.py align $P && python3 tools/cli.py lock-audio $P
```
- Câu không qua ASR hoặc kiểm tra tốc độ: sửa câu trong `story.py`, ghi lý do vào `revision.edits`. Không nới ngưỡng. Câu rất ngắn dễ rớt ngưỡng 1,5 từ/giây (3–5 từ, nhất là có năm).
- Tên riêng tiếng nước ngoài: đọc cột phiên âm trong manifest ngay sau `narrate`. Kokoro đọc theo quy tắc tiếng Anh Mỹ (Beauvais thành "BOH-vize"), nên ghi đè trong `script/pronunciation.json` kèm nguồn cách đọc, để `PENDING_LISTENING_REVIEW`. Chỉ chủ kênh xác nhận.
- Thử giọng: `python3 tools/voice_audition.py --project <slug> --voices us --passage B02:0,B10:1`.
- Phát âm: `python3 tools/longform_reports.py $P` sinh `review/PRONUNCIATION_REVIEW.md` (mốc thời gian, âm vị, những gì ASR nghe được).

## 15–16. Lịch chương, shot và kế hoạch hình (CLI)
```bash
python3 tools/cli.py plan-visuals $P && python3 tools/cli.py build-shots $P
python3 tools/cli.py chapters $P --preset review           # manifest chương + QA phim dài (17 kiểm tra)
python3 tools/cli.py check-blender $P --preset review
```
Sửa theo báo cáo, bằng nội dung (tách câu, NOTE, phần tử theo từ), không nới ngưỡng. Các báo cáo cần đọc: `qa/VISUAL_COVERAGE.md`, `qa/longform_qa.json`, `qa/VISUAL_VARIETY.md`.

## 17–19. Render, ghép 2D/3D, phụ đề (CLI)
```bash
python3 tools/cli.py chapter $P --chapter C4 --preset review        # một chương hoàn chỉnh trước
python3 tools/cli.py preview $P --preset preview && python3 tools/cli.py assemble $P --preset preview   # rough cut
```
- Frame tĩnh được dùng lại tự động; `verify-reuse --shot SC_xxx` kiểm chứng.
- Muốn ước lượng trước thì chạy `--mode reuse-report` của `engine/render_scene.py`.
- Phụ đề là SRT + mov_text, mốc từ câu đã đo.

## 20–22. Ghép media, QA, giao bản review
- AGENT xem rough cut bằng ảnh mỗi 3 giây và frame gốc, rồi ghi `qa/EDITORIAL_REVIEW_TIMECODED.md`. Mỗi lỗi có: mốc, vấn đề, vì sao quan trọng, cách sửa, ảnh hưởng, phải render lại hay không. Kèm 10 câu hỏi trải nghiệm người xem.
- Bản review:
```bash
python3 tools/cli.py preview $P --preset internal_1080p && python3 tools/cli.py assemble $P --preset internal_1080p
python3 tools/longform_reports.py $P && python3 tools/cli.py research-map $P && python3 tools/cli.py gates $P --preset internal_1080p
```
- Gói giao cho chủ kênh: `docs/production/templates/INTERNAL_REVIEW_PACKAGE.md`. **Dừng ở đây và chờ chủ kênh.**

## 23. Duyệt của chủ kênh (OWNER)
- `review/FINAL_APPROVAL_CHECKLIST.md`: claim, giọng cho dự án, phát âm, ảnh, công bố, xuất bản.
- AGENT chỉ ghi lại những gì chủ kênh nói, theo các schema:
  - `research/editorial_approval.json`: id claim, hash câu chữ, revision lời dẫn;
  - `config/tts_providers.json` → `clearance.voice_approvals`: giọng, hash, dự án, mục đích;
  - `voice.license` (APPROVED, `owner_confirmation_for_this_film`);
  - `voice.pronunciation_review` (`ACCEPTED_BY_OWNER` hoặc `CONFIRMED`, gắn với hash audio);
  - `review/OWNER_APPROVALS.json`.
- Không bao giờ ghi một việc duyệt hay một buổi nghe mà chủ kênh không làm.

## 24. Kiểm cổng xuất bản
`project.json`: `production_profile: PUBLICATION_CANDIDATE` + `publication_metadata`. Sau đó `python3 tools/cli.py final-gate $P`. Cổng cuối chỉ đòi duyệt các claim **mà phim dùng**.

## 25. Render bản cuối 4K theo chương
```bash
for c in C1 C2 …; do python3 tools/cli.py chapter $P --chapter $c --preset final_4k --release-frames; done
python3 tools/cli.py final-assemble $P --preset final_4k
python3 tools/cli.py gates $P --preset final_4k
```
- Mỗi chương: render (dùng lại frame tĩnh) → bản trung gian H.264 BT.709 → kiểm chứng (checksum, đầu vào từng shot, số frame, giải mã) → ghi `qa/chapter_intermediates_final_4k.json` → mới xóa PNG.
- Chạy lại thì: chương nào có bản trung gian hợp lệ được CACHED; shot nào đang dở được làm tiếp từ PNG hoàn chỉnh.
- Lệnh tự dừng nếu đĩa trống dưới mức dự phòng 8 GB.
- Benchmark 1–4 shot ở 4K trước khi chạy cả phim.

## 26. Đóng gói
`output/<slug>_FINAL_4K_2160p.mp4` + `.en.srt` + WAV master + `.sha256`; cập nhật PROJECT_STATUS, CHANGELOG và docs; commit trên nhánh riêng. **Không upload, không merge, không push.**

## Làm tiếp sau khi dừng
1. `python3 tools/episode.py status --project <slug>`.
2. Đọc `NEXT:`: AGENT thì làm theo mục tương ứng ở trên; CLI thì chạy lệnh; OWNER thì dừng và trình gói review.
3. Render bị ngắt: chạy lại đúng lệnh cũ.

## Phim tham chiếu
`projects/why-bridges-look-different/`: kịch bản (`script/story.py`), nghiên cứu (`research/`), hồ sơ duyệt (`review/OWNER_APPROVALS.json`), báo cáo (`docs/m7/`). Các dự án pilot cũ (M2–M6) được giữ làm fixture test ở `tests/fixtures/legacy_projects/`; không phải dự án đang làm.
