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
- **Kiểm tra bắt buộc: lời và hình có khẳng định vượt quá bằng chứng không?** (yêu cầu của chủ kênh, 2026-11-05). Làm trước khi giao kịch bản và làm lại trước khi giao bản review. Khớp nguyên văn với nguồn chỉ chứng minh nguồn có viết câu đó. Với từng câu và từng hình, hỏi:
  - **Điều kiện:** câu tổng quát có giữ điều kiện của nguồn không (hình học, tải, giả định phân tích)? Một phép so sánh cụ thể không phải quy luật.
  - **Hình chứng minh gì:** hình có nói nhiều hơn điều nó thực sự cho thấy không? Một đường vẽ không vừa không chứng minh rằng không có đường nào vừa. Hình so sánh phải có thay đổi thật về tải, hình dạng hoặc gối đỡ.
  - **Số trên hình:** số có bị hiểu là của chính vật đang vẽ không? Số của một nghiên cứu chỉ đặt cạnh hình tái hiện đúng ví dụ của nghiên cứu đó, kèm giải thích.
  - **Niên đại:** năm của cả công trình có bị đọc thành năm của một bộ phận không (Durham 1093, Cluny 1088)?
  - **Nguồn được nêu tên:** câu nêu tên nguồn có được beat đó dẫn đúng nguồn không?
  - **Sổ claim:** claim có rộng hơn lời dẫn không? Người duyệt không phải chấp thuận phát biểu rộng hơn điều phim nói.
  - **Đối lập:** phần đầu có tạo ấn tượng mà kết luận của phim phủ nhận không (Romanesque tối, Gothic thông minh)?
  - **Hình dựa trên phép tính:** phải tái hiện ví dụ đã công bố bằng phương pháp đã công bố, đối chiếu với kết quả in trong nguồn, có test giữ phép đối chiếu, và ghi rõ chỗ chưa khớp. Không dùng dung sai tự đặt để qua kiểm tra.
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
- Hai mô hình khác nhau cần so kích thước: `SEQUENTIAL_STATES` với `same_scale: true` (một camera khóa) và `state_targets` (bộ phận phát sáng riêng cho từng mô hình). Với mô hình `ILLUSTRATIVE`, chênh lệch kích thước trên hình không phải số đo: đừng ghi "same scale" nếu lời dẫn và sổ claim không nói về kích thước đó.
- Hai beat liên tiếp cùng một góc nhìn: đặt `close_on` giống nhau (bộ phận để lấy khung, độc lập với bộ phận phát sáng), planner sẽ cho match cut. Khung khác nhau thì là cut thường. `glow_only` chọn riêng bộ phận phát sáng; `highlight_at_sentence` chọn câu bắt đầu. Hai bộ phận sát nhau cùng sáng sẽ lẫn vào nhau, nên cho sáng từng bộ phận.
- Chú thích `THRUST_ARROW`: mũi tên đẩy ngang ra ngoài, cùng độ dài như mọi mũi tên, phải có claim đã kể.
- Chiến lược có sẵn: HOLD, HOLD_HIGHLIGHT, ASSEMBLE_IN, EXPLODE, HIGHLIGHT_THEN_EXPLODE, CLOSEUP_EXPLODE, HIGHLIGHT_REPLACE_HIGHLIGHT, COMPARE_SIDE_BY_SIDE, DETAIL_THEN_OVERVIEW, SITE_HOLD, CARD, SEQUENCE (mục dưới); HOLD có thể kèm `camera_move: PUSH_IN`.
- Trộn 3D, sơ đồ, bản đồ sơ lược, dòng thời gian và ảnh có quyền. Tránh chuỗi 2D dài.

### Shot SEQUENCE: hình kể theo lời (2026-11-06)
Câu hỏi cho mỗi đoạn: **"trong đoạn này, người xem thấy điều gì thay đổi để hiểu ý đang kể?"**. Zoom chỉ có ích khi đưa người xem tới chi tiết vừa được nhắc. Khi câu trả lời là "chưa có gì", dùng `strategy="SEQUENCE"` với `sequence` trong `story.py`:
- `camera`: một preset cho cả shot. Camera trượt và zoom giữa các `views`. Từ g-r5, một view có thể có `azimuth`, `elevation` riêng: camera đi một cung quanh chủ thể rồi dừng đúng khung (orbit). Dùng cho cảnh mở và cảnh toàn: một cung ngắn, kết thúc ở góc phục vụ phần giải thích tiếp theo. Một view nhìn từ dưới sàn cần preset ẩn mặt đất. Không cho camera vừa quay vừa có bộ phận đang đổi.
- `views`: `{"frame": refs}` cho từng khung (`None` là toàn bộ mô hình), `at` và `move_seconds` cho mỗi lần chuyển.
- `steps`: lần lượt `GHOST` (làm mờ phần còn lại), `UNGHOST`, `FADE_OUT`, `FADE_IN`, `REVEAL` (bộ phận hiện ra và đặt đúng chỗ) và `HIGHLIGHT` (phát sáng). Mỗi lần sáng có bộ phận riêng và có thể kéo `until` một mốc sau.
- Mốc thời gian: `{"sentence": k}`, `{"sentence": k, "word": "ribs"}`, `{"sentence": k, "end": true}`, kèm `offset` (giây). Mọi mốc đo trên audio đã khóa.
- Tham chiếu bộ phận: concept + `group`, hoặc `local` (id cục bộ chính xác, ví dụ `rib_diagonal_b1a`). `{"except": refs}` nghĩa là mọi bộ phận của công trình trừ những cái đó. Các bộ phận bị camera ẩn (sàn khi nhìn từ dưới) không bao giờ bị chọn.
- Hai shot liền nhau mà shot sau mở đúng khung và đúng trạng thái mờ mà shot trước kết thúc thì planner cho match cut. Ghi lại trạng thái đầu shot bằng bước tức thì ở `at: 0, seconds: 0`.
- Chú thích bám vào bộ phận chỉ hiện khi camera đứng yên. Planner tự cắt cửa sổ hiển thị, còn ghi chú cố định màn hình thì đi theo camera.
- Âm thanh: `REVEAL` có `sound` (`STONE`, `STONE_HEAVY`) sinh một mốc âm khi bộ phận đặt xuống. Âm tổng hợp trong `pipeline/sound.py` (`config/sound_design.json`), không có nhạc nền.
  - Âm thu sẵn (từ 2026-11-12): `audio/sound_plan.json` ghi nguồn, giấy phép, sha256; `replace` cho mốc tổng hợp phát file thật; `cues` neo vào một bước storyboard; `chapter_cues` ở mỗi điểm cắt sang chương mới; `beds` là nền âm ngắn dưới đúng một shot.
  - Nguyên tắc chọn âm (phim giải thích kiến thức): chỉ gắn âm khi có hành động vật lý mà lời dẫn đang nói; âm cỡ mô hình; không gắn âm cho chữ hay card; bỏ được thì bỏ. Xem `projects/floating-city-design-challenge/review/SFX_LIBRARY.md`.
- Cách làm hiệu quả: dựng **một đoạn thử 60–90 giây** (`tools/excerpt.py`) cho chủ kênh duyệt chất lượng hình trước, rồi mới áp cho cả phim. Xem frame thử bằng Blender trước khi render cả shot. Kiểm tra Blender riêng các shot mới: `engine/render_scene.py --mode check --shot SC_a,SC_b`.
- Những điều đã học từ đoạn thử của phim Gothic:
  - khung "cả mô hình" của một mặt cắt cao hơn chiều ngang thì bị giới hạn theo chiều cao, nên cận cảnh phải cắt bớt chiều cao;
  - phần bị làm mờ không được đổ bóng (engine tự tắt);
  - nhìn từ dưới lên thì mặt dưới vòm tối, nên preset `CATHEDRAL_VAULT_BELOW` có đèn phụ từ dưới (`under_light`);
  - đá giữa gân chia thành các dải (`web_courses`) để cho thấy cách đọc "một loạt vòm song song".
- Bổ sung sau góp ý của chủ kênh về đoạn thử (g-r5):
  - **Tương phản:** `glow(...)` trong `story.py` dùng `HIGHLIGHT` với `tint` (0..1). Bộ phận chuyển sang màu `highlight` của bảng màu thay vì sáng lên, vì đá sáng trên nền sáng thì mất tương phản.
  - **Ít lớp mờ:** chỉ giữ mờ phần đủ để định vị (ví dụ tường cao của khoang). Phần còn lại cho `FADE_OUT`, vì nhiều lớp mờ chồng nhau thành vệt.
  - **Không để chân trụ lơ lửng:** khi nhìn từ dưới sàn (sàn bị ẩn), nhìn thẳng lên (`elevation` khoảng −84°), hoặc cắt khung sao cho chân trụ nằm ngoài. Cảnh mở nên bắt đầu ở góc thường, công trình đứng trên sàn.
  - **Gối đỡ trước, bộ phận sau:** trụ ngoài phải đặc trước khi trụ chống bay hiện ra.
  - **Đường lực vẽ dần:** `CONCEPTUAL_LOAD_PATH` tự vẽ theo tuyến (`draw_seconds` trong `config/annotation_style.json`) rồi giữ nguyên. Không kéo dài, không phồng, không chạy hạt.

### Ảnh thật và bản vẽ lịch sử (g-r5)
- Vai trò:
  - ảnh thật xác lập địa điểm, vật liệu, quy mô và trải nghiệm không gian;
  - mô hình 3D giải thích cấu tạo;
  - sơ đồ động giải thích lực, so sánh, thời gian và giả thuyết;
  - chữ chỉ dành cho tên gọi, con số, trích dẫn ngắn và giới hạn của minh họa.
- Chuỗi hiệu quả: ảnh thật xác lập công trình → đánh dấu bộ phận liên quan → chuyển sang mặt cắt hoặc mô hình để giải thích → trở lại ảnh thật.
- Nguồn: Wikimedia Commons, kiểm giấy phép qua API (`extmetadata`).
  - Ưu tiên public domain (bản vẽ của Viollet-le-Duc), CC0, CC BY. Tránh CC BY-SA.
  - Nếu Commons trả HTTP 429, tải chậm lại, không lách qua bản sao.
  - Bỏ ảnh có tác giả hoặc năm không chắc chắn.
- Trong `story.py`: `PHOTOS` (đường dẫn, kích thước, dòng ghi công), `Card.image(...)`, `Card.credit(...)`. `fitted(asset, box, crop)` trả về hàm đổi pixel của ảnh sang tọa độ card, để dấu vẽ rơi đúng chỗ trên bản vẽ.
- Phần tử card có thể xoay (`spin`: `degrees`, `pivot`, `sentence`/`word`, `seconds`). Dùng khi lời dẫn kể một phép biến đổi: "mỗi đoạn tường xoay 90°", "lật ngược dây xích".
- Các helper vẽ dần: `Card.drawn(...)` vẽ đường theo thứ tự trong `seconds`; `Card.drawn_arrow(...)` vẽ mũi tên, đầu đến cuối cùng; `.later(s)` cho nhãn chờ nét vẽ xong. Phần tử card có `delay` (giây sau câu hoặc từ của nó).
- **Không dựng như slide** (góp ý g-r5): tránh kiểu ảnh nhỏ bên trái, chữ bên phải.
  - Ảnh chiếm phần lớn khung. Camera 2D (`Card.stage()` và `Card.view(rect, sentence, word, move)`) đi tới đúng vùng đang được kể: lia lên vòm, cận vùng đánh dấu, rồi lùi ra để so trước–sau.
  - Ảnh và dấu vẽ nằm trên stage; chữ đứng yên trên màn hình. `on_screen(view, point)` cho biết một điểm của ảnh hiện ở đâu trong view đó, để đặt nhãn cạnh nó.
  - Mỗi cảnh ít chữ: tên, con số, trích dẫn ngắn, giới hạn của minh họa. Không chép lại lời dẫn.
  - Tiêu đề chỉ giữ vài giây (`gone(sentence, word)`); các câu hỏi tiếp theo hiện trên hình.
  - Khi kể một sự kiện cũ trên ảnh chụp hôm nay, ghi "today".
  - **"today" chưa đủ khi công trình đã được dựng lại** (góp ý g-r8). Khi lời dẫn kể một giai đoạn xây dựng, ảnh phải cho thấy phần còn lại từ đúng giai đoạn đó (ví dụ ambulatory của Suger ở Saint-Denis, không phải phần trên dàn hợp xướng dựng lại từ 1231). Chú thích nói rõ phần nào, và giữ qua lúc chuyển cảnh. Phần nào dựng lại phải có nguồn và claim.
  - Nhãn chỉ bộ phận phải chấm đúng vào bộ phận đó (một gân rõ, không phải mảng đá giữa các gân). Soi khung 1:1 trước khi render. Nếu cần, vẽ sáng ngắn dọc bộ phận khi nó được gọi tên.
  - Tọa độ phần tử phải nằm trong 0..1. Nếu bố cục stage cần rộng hơn (ví dụ một ảnh dọc rất cao đặt cạnh ảnh ngang), thu cả bố cục về giữa card theo một tỉ lệ. Camera stage bù lại nên khung hình không đổi; nét vẽ trên stage cũng thu theo tỉ lệ đó.
  - Card ảnh không bao giờ mở bằng khung trống: ảnh đầu tiên có `from_start` (`Card.image` tự gán).
  - Đổi ảnh bằng chuyển hoà: ảnh sau ở `layer` cao hơn và vào trước; ảnh trước rời đi bằng `until_word` vài từ sau.
- **Kết quả của một nghiên cứu không phải phán quyết:** không gạch chéo một giả thuyết. Làm mờ nó và ghi "Not supported by this study", kèm tên nghiên cứu.
- Mọi dấu vẽ lên ảnh hay bản vẽ đều ghi "schematic". Không đánh dấu vị trí mà nguồn không nói, ví dụ tuyến dây xích Amiens: chỉ vẽ "dọc lòng chính, giằng trụ giao cánh" như Columbia viết.
- Mỗi ảnh có hồ sơ đầy đủ trong `assets/manifest.json` và dòng ghi công trên hình. `tools/longform_reports.py` đưa ảnh vào mô tả YouTube (mục "Photographs and drawings").
- Ảnh khổ 2560 px ở cạnh dài để không làm nặng git. Bản vẽ Viollet-le-Duc chỉ khoảng 600 px, nên ở 4K sẽ hơi mềm; cần chốt trước bản cuối.

## 9–10. Tìm và tạo asset
- `python3 tools/cli.py asset-catalog` liệt kê thư viện:
  - cầu trên site 24 m: dầm gỗ, vòm đá, giàn Pratt/Warren;
  - cầu nhịp lớn trên site 72 m (M8): công-xôn, cầu treo, dây văng;
  - mặt cắt nhà thờ (phim Gothic): Gothic và Romanesque kiểu vòm nôi, trên nền `site_level_ground`; camera `CATHEDRAL_SECTION` cho cảnh chung, `CATHEDRAL_FROM_BELOW` cho cận cảnh vòm (`camera_mode: COMPONENT_CLOSEUP`, `close_on` hoặc `close_on_targets: true`; cắt sát một gian, vì khung rộng để lộ chân trụ nhìn từ dưới lên);
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
  - Tìm riêng những gì QA tự động không bắt được: card trống hoặc chỉ có trục trong lúc đang có lời; nhãn chỉ vào phần không còn nhìn thấy; hai bộ phận cùng sáng đến mức lẫn vào nhau; một góc máy lặp lại quá nhiều.
  - Đọc cả `render_*.log`: `Media QA failed` không làm lệnh `preview` dừng chuỗi lệnh nối bằng `;`, nên phải tìm dòng này trước khi ghép phim.
  - Ảnh tách bằng `fps=1/3` lệch mốc khoảng 1,5 giây. Muốn mốc chính xác thì lấy frame bằng `-ss`.
  - Render lại ít nhất có thể: mọi thay đổi trong `engine/**` hoặc `config/visual_style.json` làm toàn bộ shot thành stale. Thử sửa bằng planner hoặc nội dung trước.
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

## 27. Kinh nghiệm từ phim Gothic (g-r1 tới g-r9, bản final 4K, 2026-11-05 tới 2026-11-07)
Rút ra từ một phim 15 phút, 46 shot, chín vòng review. Đây là cách làm, không phải nội dung; không chép claim hay id beat.

### Nhịp làm việc với chủ kênh
- **Mỗi vòng một bản `review/REVIEW_G_Rn.md`:** bảng "góp ý → đã làm", mục Kiểm tra và mục Còn lại/Cần quyết. Giữ hướng hình đã được khen, sửa cục bộ; không làm lại cả chương khi chủ kênh nói "giữ hướng".
- **Thứ tự sửa:** làm trọn một chương mẫu cho tới khi chủ kênh hài lòng, rồi mới áp phương pháp sang chương khác. Đừng thêm hiệu ứng vào đoạn chủ kênh đã bảo là rõ.
- **Đổi mã shot thì sinh lại manifest chương** (`chapters --preset internal_720p`) và báo cáo (`tools/longform_reports.py`) ở mỗi vòng. Chủ kênh đã gặp manifest còn mã shot cũ.
- **Việc cần quyết của chủ kênh:** hỏi bằng câu hỏi có lựa chọn, mỗi lựa chọn nêu đúng điều nó ghi vào hồ sơ. Chỉ ghi các mục được chọn. Câu "duyệt bản này" chưa phải duyệt từng mục.
- **Ngoại lệ của một ngưỡng** (ví dụ một chuỗi dài cùng loại hình) là quyết định của chủ kênh, ghi ở `project.json` (`variety_exception`, như `runtime_decision`), hiện trong báo cáo QA. Ngưỡng chung không đổi. Không tự miễn một kiểm tra.
  - Ghi đúng phạm vi chủ kênh chấp nhận: `runs` (`first`, `last`, `length`, `kind`) cùng `decided_by`, `decided_on`, `basis`. `longform_qa` chỉ miễn đúng các chuỗi đó. Một chuỗi dài ra, ngắn lại hay đổi loại thì cần quyết định mới. (Từ 2026-11-12. Trước đó `max_run` nâng ngưỡng cho cả phim.)
- **Watermark kênh** (`config/branding.json`, từ 2026-11-12): được đốt vào hình khi mã hóa khung (`encode_sequence`), cho mọi bản chương, bản ghép và bản trích. Chỉ áp cho dự án có `"watermark": true` trong `project.json`; dự án mới có sẵn. Watermark nằm ở góc dưới trái, trong vùng phụ đề nơi chú thích không bao giờ vào. QA chương kiểm watermark có trong file xuất. Không vẽ watermark trong Blender, nên cache render không đổi.
- **Không bao giờ có file tên FINAL trước khi duyệt.** `final-assemble` từng đặt tên FINAL cho bản nội bộ; một test của dự án bắt được. Bản nội bộ lấy tên theo `review_label`.

### Hình phải khớp lời, niên đại và nguồn
- **Ảnh phải cho thấy đúng giai đoạn lời đang kể.** "today" chưa đủ nếu công trình đã được dựng lại; chọn ảnh phần còn lại từ giai đoạn đó, hoặc chú thích phần dựng lại, và chú thích giữ qua chuyển cảnh. Khẳng định về phần nào còn lại phải có nguồn và claim riêng.
- **Nhãn chỉ bộ phận phải chấm đúng bộ phận.** Soi khung 1:1 sau khi render, ở từng nhãn. Nếu cần, vẽ sáng ngắn dọc bộ phận khi nó được gọi tên.
- **Hình giải thích một phép biến đổi thì vẽ chính phép đó** (xoay 90°, lật dây xích, compa quay từ chân vòm lên đỉnh), theo đúng từ trong lời, thay vì card chữ hay mô hình đứng yên. Chữ chỉ cho tên, con số, trích dẫn ngắn và giới hạn của minh họa.
- **Không để khung chờ lâu:** tên người và câu trích không nên chiếm cả chục giây khi hình đã có thể bắt đầu. Cho hình xuất hiện từ những giây đầu, giữ thao tác chính đúng từ trong lời.
- **Cận cảnh thật sự:** "close on X" nghĩa là camera tới X, làm mờ phần còn lại (SEQUENCE), sáng bộ phận theo lời; không phải toàn mô hình với zoom nhẹ.
- **Cái nguồn không nói thì không vẽ.** Mọi dấu vẽ lên ảnh hay sơ đồ ghi "schematic"; một nghiên cứu không phải phán quyết; không dựng lại vụ sập.

### Kiểm tra: máy bắt một phần, mắt bắt phần còn lại
- **Xem video thật, không chỉ ảnh tĩnh.** Trích khung từ MP4 ghép quanh mọi lần đổi ảnh và điểm cắt. Hai lỗi chỉ thấy ở video: card mở bằng nền trống, và đổi ảnh để lộ một khung trống.
- **QA Blender cũng có lỗi.** Khi một kiểm tra báo sai đáng ngờ, tìm nguyên nhân trước khi sửa hình (tia kiểm tra nhãn từng đi theo hướng camera lúc dựng shot, không theo hướng thật).
- **Planner từ chối là có lý do:** vệt sáng quá ngắn, phần tử biến mất trước khi hiện đủ. Sửa nhịp, không nới ngưỡng.
- **Đổi bố cục stage:** tọa độ phải trong 0..1; muốn rộng hơn thì thu cả bố cục về giữa card theo một tỉ lệ, camera stage bù lại, nét vẽ trên stage thu theo.
- **Chạy toàn bộ test sau mỗi vòng.** Hai lần test bắt lỗi quy trình mà QA hình không thấy (tên file FINAL; trạng thái duyệt).

### Nguồn và ảnh
- **Kiểm nguyên văn** mọi trích dẫn nguồn (`research/build_sources.py`); nguồn tiếng Pháp trích bằng tiếng Pháp, claim nêu nghĩa tiếng Anh. Nguồn mới thêm vào build, kèm bản chụp và SHA256 ở `research/source_snapshots.json` (thư mục chụp không vào git).
- **Ảnh:** Wikimedia Commons qua API (`extmetadata`); ưu tiên public domain, CC0, CC BY; tránh CC BY-SA; tải chậm khi gặp HTTP 429; không lách qua bản sao. Lấy bản gốc lớn nhất có thể (bản vẽ 600 px phải thay bằng bản quét lớn, đối chiếu tự động bằng tương quan FFT để dấu vẽ giữ nguyên chỗ).
- **Hồ sơ ảnh đầy đủ** ở `assets/manifest.json`. `status: approved` ban đầu chỉ nghĩa agent đã kiểm giấy phép; chủ kênh duyệt ảnh và ghi công là một bước riêng ở `OWNER_APPROVALS.json`.
- Ảnh lưu 2560 px ở cạnh dài để không làm nặng git. Ảnh nguồn nhỏ (dưới khoảng 2000 px) sẽ mềm ở 4K khi phủ kín khung: biết trước và ghi vào báo cáo.

### Render
- **Một Blender tại một lúc;** không sửa `engine/*.py` và không chạy test gọi Blender khi đang render.
- Tốc độ tham khảo (Mac Apple Silicon, EEVEE): 3D ở 4K khoảng 2,2 giây mỗi frame; card 2D rẻ hơn nhiều. Benchmark một shot 3D trước khi chạy cả phim; `caffeinate -is` cho chuỗi dài.
- **Thứ tự cuối:** `final-gate` → `chapter --preset final_4k --release-frames` từng chương → `final-assemble` → `gates --preset final_4k` → dọn file render thử và review cũ (mục 28).

## 28. Dọn dẹp sau bản final
- **Chỉ dọn sau khi** bản final được kiểm (gates, media QA) và checksum đã ghi.
- **Xóa:** thư mục render thử và review cũ không còn dùng (PNG và shot 720p, bản ghép g-r cũ, đoạn thử, preview card), file trung gian 4K đã được thay bằng bản ghép cuối nếu chủ kênh không cần.
- **Giữ:** bản final 4K + `.en.srt` + WAV master + `.sha256`; bản review nội bộ 720p mới nhất đã được duyệt (một file); `review/`, `qa/*.json`, `research/`, `script/`, `assets/` (trong git).
- **Sau khi ghi duyệt, trước `gates` cuối:** `sources.json` đã đổi nên chạy lại `plan-visuals` → `build-shots` → `chapters --preset final_4k` (chỉ đổi `evidence_status` và hash; không render lại). Nếu không, GV báo kế hoạch cũ và GL báo QA cũ.
- Không xóa trong git; không động tới dự án khác. Ghi những gì đã xóa và dung lượng vào `docs/production/CLEANUP_REPORT.md`.
- **Cách làm an toàn:** chuyển file ra một thư mục tạm, chạy lại `chapters`, `gates --preset final_4k`, `episode.py status`, toàn bộ test và `shasum -c` các file giữ lại; chỉ xóa khi mọi bước đạt.
- **Đo dung lượng bằng `du`.** Frame tĩnh dùng lại là hard link, nên tổng kích thước logic lớn hơn nhiều so với dung lượng thật (phim thành phố nổi: 15,8 GB logic, 6,0 GB thật).

## 29. Kinh nghiệm từ phim thành phố nổi (concept tới bản final 4K, 2026-11-08 tới 2026-11-13)
Rút ra từ một phim "bài toán thiết kế" 13 phút, 44 shot, hầu hết là 3D, không có ảnh của bên thứ ba. Đây là cách làm, không phải nội dung.

### Phim concept: con số phải có gốc
- **Mô hình thiết kế trước kịch bản.** Bản hợp đồng kịch bản (`concept/SCENARIO_CONTRACT.md`) và mô hình tính (`analysis/results.json`) có trước lời dẫn. Mọi độ dịch, góc và tổng số trên hình lấy từ mô hình, có test giữ; không viết tay số nào.
- **Phép tính của Studio là claim riêng**, ghi rõ loại (ước tính, giả định) và giới hạn. Lời dẫn, ghi chú trên hình và mô tả đều nói rõ: tính ở mức concept, không phải thiết kế được chứng nhận; chuyển động là minh họa, không phải mô phỏng.
- **Đổi hình cho dễ đọc thì giữ nguyên bất biến kỹ thuật.** Ví dụ thêm kiểu nhà, cửa sổ, công viên nhưng giữ diện tích chiếm đất, số tầng và trọng tâm, có test chứng minh tải và mớn nước không đổi.
- **Tự rà kịch bản với nguồn**, đọc cả câu quanh đoạn trích. Agent tự tìm ra một claim gán nhầm mục đích (khoảng cách giữa module là để tránh va chạm, không phải để giảm tải mối nối).

### Nhịp review
- **Thứ tự đã chạy tốt:**
  1. Concept, rồi hai vòng kịch bản (c-r1, c-r2). Chốt lời dẫn và duyệt claim, giọng, phát âm.
  2. Các lớp asset và engine L1–L4, mỗi lớp kiểm được và commit riêng.
  3. Đoạn thử chương cơ chế khó nhất (L5, hai vòng), rồi đoạn mở đầu (L6, hai vòng).
  4. Cả phim (FULL v1–v3), rồi bản final.
  - Khi đoạn thử đã chốt ngôn ngữ hình, chủ kênh chuyển sang duyệt cả phim, không duyệt từng đoạn nhỏ nữa.
- **Muốn có đoạn thử thì phải phủ đủ mọi beat trước.** `build-shots` đòi kế hoạch hình thực thi được cho cả phim. Phủ cả 44 beat bằng asset hoặc card thật, nhưng chỉ render các shot của đoạn thử.
- **Prototype không lời** (ví dụ P6: thêm tải, phao chìm, sửa thân) được làm trước khi chốt kịch bản. Asset thật chỉ dựng sau khi chốt, theo AGENTS.md.
- **Review của người duyệt thứ hai** (Codex) là đầu vào để sửa. Các đề nghị "giữ nguyên" trong đó chưa phải quyết định của chủ kênh: hỏi lại từng mục rồi mới ghi.

### Hình 3D ở tầm toàn quận
- **Bộ phận lời dẫn gọi tên phải đủ lớn trong khung.** Ở tầm toàn quận, neo, cáp và cầu chỉ chiếm 0,01–0,5% khung, và kiểm Blender từ chối. Đưa camera tới bộ phận đó, đừng chỉ làm sáng nó trong khung rộng.
- **Một mạng lưới trên nền sáng:** làm mờ mọi thứ khác và đổi sang màu nhấn, thay vì phát sáng (phát sáng làm mất tương phản).
- **Mô-đun lặp lại đọc như một mảng vân.** Chia quận thành ô nhiều kiểu nhà, thêm công trình công cộng và công viên đọc được: cửa sổ, lối vào, sân chơi.
- **Camera mà lộ mép bãi:** nâng góc nhìn hoặc đổi đường camera trước khi tính đến chuyện nới bãi. Nới bãi làm mất cache của mọi shot dùng site đó.

### Nước làm trong
- **Nước trong để lộ thứ không nên thấy:** lưới bóng trên đáy, mép bãi nước, mặt bên của khối nước.
- **Cách đã chốt:**
  - mở bằng nước đục;
  - camera hạ xuống khung ngang, đứng ngoài khối nước;
  - nước chỉ trong ở cuối lúc hạ; khi camera xuống từ góc cao thì bắt đầu trong 0,4 s trước khi tới khung ngang, trong 0,6 s;
  - giữ mực nước là một đường thẳng.
- **Độ trong (alpha) không phải tiêu chí nghiệm thu.** Xem mọi đoạn chuyển trong MP4 ở 4 khung mỗi giây.
- **Báo cáo v2 từng ghi B31 đã sửa** trong khi một khung vẫn lộ lưới bóng: agent đã bỏ sót khung đó. Khi báo một lỗi đã sửa, xem đủ mọi khung quanh đoạn chuyển. Nếu báo sai thì đính chính công khai ở vòng sau.

### Âm thanh
- **Kiểm giấy phép trước khi dùng một kho có sẵn.** Kho `sfx/` cũ của chủ kênh chỉ được dùng trong CapCut.
- **Nguồn âm thanh:**
  - YouTube Audio Library: không crawl (trái điều khoản); chủ kênh tải tay;
  - Pixabay: kiểm giấy phép trên trang của từng file;
  - ghi trang, tác giả, giấy phép, ngày kiểm và sha256 vào `audio/sound_plan.json`;
  - không commit file Pixabay.
- **Agent không nghe được.** Chọn bằng số đo (điểm bắt đầu, nền nhiễu, phổ, độ đều), giao kèm bản không SFX, và ghi rõ là chưa ai nghe.
- **Chỉ gắn âm khi có lý do:**
  - hành động vật lý mà lời đang kể;
  - điểm cắt chương;
  - nền nước ngắn, chỉ ở nơi nước là chủ đề.
  - Không gắn âm cho chữ hay card.
- **Neo tiếng thêm vào bước của storyboard, không neo vào giây.** Như vậy cache render không đổi, và một bước bị dời thì pipeline từ chối.

### Bản final
- **Trước khi render 4K:** kiểm rằng bước ghép cuối tái tạo đủ mọi thành phần của bản review đã duyệt. Ở phim này, `final-assemble` lúc đầu chưa trộn SFX; lỗi được phát hiện trước khi render.
- **Sau khi ghép:**
  - so âm thanh trước chuẩn hóa với bản review đã duyệt, từng mẫu (0 mẫu khác);
  - so hình bằng SSIM, mỗi giây một khung (≥ 0,97);
  - so phụ đề byte-to-byte.
- **Ước lượng thời gian render theo loại shot, có trọng số số frame.** Đừng ước theo shot nặng nhất.
  - Agent ước 15–25 giờ theo cảnh toàn quận (5,5–6 giây mỗi frame); thực tế 8 giờ 10 phút cho 18 820 frame (trung bình khoảng 1,6 giây mỗi frame).
  - `caffeinate -is` giữ máy thức suốt lượt render.
- **Khi đang render chỉ chạy test offline,** liệt kê từng module. Agent từng lỡ chạy hai file test gọi Blender trong lúc render, làm hai Blender chạy cùng lúc.
- **Đổi dung sai của một kiểm tra thì nói thẳng là đã đổi.** Dung sai phải suy từ cách lưu số (ví dụ ulp float32 của khóa F-curve). Báo cáo v1 từng viết "không nới ngưỡng" trong khi công thức đã đổi; v2 phải đính chính.

### Hồ sơ xuất bản
- **`RIGHTS_PROVENANCE.md` cần cho mọi phim**, kể cả phim không có ảnh: lời dẫn, mô hình, SFX, font, phụ đề. `episode.py status` đòi file này.
- **Gate `PUBLICATION_READY` không kiểm việc chủ kênh duyệt mô tả.** Báo riêng mục này, đừng gọi phim là "sẵn sàng đăng" khi mô tả chưa được duyệt.
- **Lựa chọn của chủ kênh về mô tả** ghi vào `publication_metadata` (`disclosures`, `description_omit` kèm `description_omit_decision`), không sửa tay `YOUTUBE_DESCRIPTION.md`. Lý do: `tools/longform_reports.py` ghi đè file này mỗi khi bản sinh tự động dưới 5 000 ký tự.
- **Ví dụ ở phim này:** chủ kênh bỏ dòng ghi công lời dẫn và SFX (DEC-DESCRIPTION-CREDITS). Apache-2.0 và Pixabay Content License đều không đòi ghi công. Điều kiện "nêu lời dẫn AI trong mô tả" của lần duyệt giọng vì vậy không áp cho phim này. Cài đặt "nội dung tổng hợp" trên YouTube vẫn do chủ kênh chọn khi đăng.

## Làm tiếp sau khi dừng
1. `python3 tools/episode.py status --project <slug>`.
2. Đọc `NEXT:`: AGENT thì làm theo mục tương ứng ở trên; CLI thì chạy lệnh; OWNER thì dừng và trình gói review.
3. Render bị ngắt: chạy lại đúng lệnh cũ.

## Phim tham chiếu
`projects/why-bridges-look-different/`: kịch bản (`script/story.py`), nghiên cứu (`research/`), hồ sơ duyệt (`review/OWNER_APPROVALS.json`), báo cáo (`docs/m7/`). Các dự án pilot cũ (M2–M6) được giữ làm fixture test ở `tests/fixtures/legacy_projects/`; không phải dự án đang làm.
