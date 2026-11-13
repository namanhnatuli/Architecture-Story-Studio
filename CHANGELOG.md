# Changelog

## 0.12.3 — 2026-11-13 — Phim thành phố nổi: sửa mô tả, dọn dẹp, kinh nghiệm chung
- **Mô tả YouTube** (chủ kênh yêu cầu):
  - bỏ dòng ghi công lời dẫn và dòng ghi công SFX; không render lại;
  - `tools/longform_reports.py` đọc `publication_metadata.description_omit` (`narration`, `sound_effects`), bắt buộc kèm `description_omit_decision`; giá trị lạ thì dừng;
  - phim cầu và phim Gothic sinh lại giống hệt; 3 test mới;
  - chủ kênh duyệt bản mô tả đã sửa (APP-DESCRIPTION, kèm sha256 của file).
- **Hồ sơ:**
  - `review/RIGHTS_PROVENANCE.md` cho phim thành phố nổi; trước đây thiếu, nên `episode.py status` dừng ở INTERNAL_REVIEW;
  - DEC-DESCRIPTION-CREDITS trong `OWNER_APPROVALS.json`.
- **Dọn dẹp:**
  - khoảng 6,0 GB file render thử và review cũ (`docs/production/CLEANUP_REPORT.md`);
  - commit riêng việc xóa 42 file SFX CapCut cũ mà chủ kênh đã tự xóa khỏi thư mục làm việc.
- **Thumbnail:** 3 đề xuất (quy mô, vật lý, dây neo), render sạch từ scene của phim; script để dựng lại ở `review/thumbnails/make/`.
- **Kinh nghiệm chung:** playbook mục 29 và AGENTS.md (phim concept, nhịp review, hình 3D ở tầm toàn quận, nước làm trong, dựng mô hình 3D, thử Sand3D, SFX, kiểm bản final, hồ sơ xuất bản). Mục 9–10 của playbook liệt kê họ asset nổi.

## 0.12.2 — 2026-11-13 — Phim thành phố nổi: bản cuối 4K
- **Duyệt của chủ kênh** (ghi trong `review/OWNER_APPROVALS.json`):
  - hình FULL v3, giữ nguyên cả 6 điểm;
  - SFX như FULL_V3;
  - lời kêu gọi cuối phim;
  - yêu cầu render final. Hồ sơ dự án chuyển sang `PUBLICATION_CANDIDATE`.
  - Mô tả YouTube chưa duyệt: chủ kênh muốn sửa.
- **Pipeline:**
  - `final-assemble` trộn SFX khi `audio/sound_plan.json` có `"final": true`; file WAV chỉ lời dẫn vẫn xuất riêng;
  - mô tả YouTube cho phim không có ảnh: không mục ảnh, câu công bố riêng của dự án (`publication_metadata.disclosures`), ghi công âm thanh.
- **Bản cuối:**
  - 8 chương, 44 shot, render 8 giờ 10 phút;
  - bản trộn giống từng mẫu với FULL_V3; SSIM so với FULL_V3 ≥ 0,970;
  - −16,4 LUFS, đỉnh thật −1,4 dBTP; QA phim dài 17/17;
  - gate `final_4k` cho kết quả PUBLICATION_READY. Gate không kiểm việc duyệt mô tả, nên phim chưa sẵn sàng đăng.
  - Chi tiết: `projects/floating-city-design-challenge/review/FINAL_4K.md`.

## 0.12.1 — 2026-11-12 — Âm thu sẵn có giấy phép; phim thành phố nổi FULL v3
- **Âm thu sẵn** (chủ kênh yêu cầu; `pipeline/sound.py`, `tools/excerpt.py`):
  - **`audio/sound_plan.json`:** mỗi file ghi trang nguồn, tác giả, giấy phép, ngày kiểm giấy phép và sha256. Thiếu file hay file bị thay thì không trộn.
  - **`replace`:** mốc âm tổng hợp phát file thật.
  - **`cues`:** tiếng thêm neo vào một bước của storyboard, không đổi shot, không làm mất cache render.
  - **`chapter_cues`:** chỉ phát ở điểm cắt thật sang chương mới.
  - **`beds`:** nền âm ngắn dưới đúng một shot, đặt theo RMS của lời dẫn.
  - **Test:** 6 test mới. AGENTS.md và playbook ghi lại quy tắc.
  - **Giới hạn:** `final-assemble` chưa trộn SFX.
- **Phim thành phố nổi, FULL v3:**
  - B31 và B33 chỉ làm trong nước ở 0,4 s cuối lúc camera hạ, không còn lưới bóng hay bóng phao dưới đáy ở đoạn chuyển;
  - 4 tiếng gắn với hành động, 7 tiếng chuyển chương, 2 đoạn nền nước ngắn (Pixabay Content License);
  - chi tiết ở `projects/floating-city-design-challenge/review/INTERNAL_REVIEW_V3.md`.

## 0.12.0 — 2026-11-12 — Watermark kênh, ngoại lệ đúng phạm vi, đính chính dung sai keyframe; phim thành phố nổi FULL v2
- **Watermark kênh** (chủ kênh yêu cầu):
  - file `branding/concepts_20261107/A_watermark_burnin_640.png`, đặt ở góc dưới trái, rộng 14% khung, độ đậm 55%;
  - đốt vào hình lúc mã hóa khung PNG (`tools/cli.py`), nên cache render Blender không đổi;
  - cấu hình ở `config/branding.json`, có sha256 của file ảnh;
  - ô watermark phải nằm trong vùng phụ đề, nơi chú thích không bao giờ vào; pipeline từ chối mọi vị trí khác;
  - chỉ áp cho dự án có `"watermark": true`. Dự án mới có sẵn (`production_defaults.json`); phim cầu và phim Gothic giữ nguyên;
  - QA chương kiểm watermark có thật trong file (PSNR trong ô); registry bản chương ghi thông số, đổi watermark thì phải mã hóa lại.
- **Ngoại lệ `visual_variety` theo đúng phạm vi** (`pipeline/chapters.py`):
  - `variety_exception.runs` chỉ miễn những chuỗi khớp đúng shot đầu, shot cuối, độ dài và loại;
  - hồ sơ phải có `decided_by`, `decided_on`, `basis`;
  - dạng cũ `chapter` + `max_run` nay chỉ miễn chuỗi nằm trong chương đó, không còn nâng ngưỡng cho cả phim.
  - Phát hiện: phim Gothic có chuỗi 5 card SC_024–SC_028 chưa được chấp nhận, trước đây qua QA nhờ kiểu cũ. Chỉ báo cáo, không sửa phim đó.
- **Đính chính dung sai keyframe** (`engine/motion.py`): báo cáo trước ghi "4 ulp" và "không nới ngưỡng QA", nhưng công thức thực chất cho 4–8 ulp.
  - Đo độc lập trên Blender 5.2.2 (`tools/f32_key_error.py`, 640.000 frame): sai số lớn nhất 2,9 ulp của độ lớn đoạn nội suy.
  - Dung sai nay là đúng 4 ulp float32 của đoạn đó, ulp tính theo số mũ nhị phân.
- **Mặt nước khi làm trong** (`engine/scene.py`): vật liệu có `see_through_color` chuyển màu khi trong (nước: #2A6E8E); nước đục giữ đúng màu cũ.
- **Cặp phao `floating.pair`:** thêm thước chênh sàn (3 MARKER) đặt trên mặt trước hai phao.
- **Phim thành phố nổi, bản internal review FULL v2:** sửa B03, B12, B13, B17, B20, B22, B24, B30–B34, B37, B38; render lại 8 chương 720p; 13:04,2. Chi tiết ở `projects/floating-city-design-challenge/review/INTERNAL_REVIEW_V2.md`.

## 0.11.2 — 2026-11-08 — Phim thành phố nổi c-r2: ba điểm sau review c-r1
- **B23 (dốc cầu nối bờ):** lời dẫn nêu "including changes in loading". CLM_109 nêu đủ cả dải mực nước 2 m, thay đổi mớn nước khoảng 0,44 m và khớp ở giữa dải (±2,8°). Mô hình in thêm phép tính chỉ với mực nước (±2,3°).
- **CLM_054:** thay "costs that rise faster than the depth" bằng "non-linear increases in material and installation cost", đúng lời nguồn.
- **B12 và B16:** quay về bản 3 tầng trước khi nhân phao; quận dùng phao 60 m với nhà 3 tầng. Mô hình in số người theo số tầng (48, 64 và 108).
- **Nhịp:**
  - B03/B40 dùng trạng thái "In Design" trên trang kiến trúc sư (claim mới CLM_034), thay cho câu dài về quy trình kiểm tra;
  - B15–B16 là một sơ đồ liên tục.
- **Audio:** ASR 126/126; timing 13:03.
- **Prototype P6** làm lại dạng mặt cắt, đường nước cố định, vách nối dài tô vàng; nhãn "same load per m² of floor".

## 0.11.1 — 2026-11-08 — Phim thành phố nổi c-r1: sửa sau review concept, lời dẫn hoàn chỉnh
- **Theo review concept của chủ kênh** (sáu nhóm sửa, `projects/floating-city-design-challenge/review/REVIEW_C_R1.md`):
  - bỏ câu suy chuyển động trong sóng từ GM;
  - 66 cm chênh mớn nước chỉ là của hai phao nổi độc lập;
  - ra khơi không đồng nghĩa tự chủ;
  - một nhánh số liên tục (mạn khô 1,042 → 0,710 → 1,146 m) và một cỡ phao cho quận (60 m, 93 phao);
  - chi phí: "no reliable cost estimate for this design";
  - tình trạng OCEANIX chỉ nói về dự án đã kiểm;
  - định nghĩa 40 m² sàn mỗi người;
  - tổng chỉ tính các phao tiêu chuẩn.
- **Lời dẫn hoàn chỉnh** `script/story.py`: 44 beat, 127 câu.
  - Số tính và giả định của Studio cũng là claim: CALCULATED_ESTIMATE dẫn `analysis/RESULTS.md`, DESIGN_ASSUMPTION dẫn `concept/SCENARIO_CONTRACT.md`, khớp nguyên văn như nguồn ngoài.
  - 16 nguồn, 63 claim.
- **Audio nội bộ và timing:** ASR 127/127; `lock-audio` 13:05. Ba câu quá ngắn bị kiểm tra tốc độ đọc từ chối nên được gộp; chính tả Mỹ và chữ số cho số ≥ 100 để Whisper khớp. Không nới ngưỡng nào.
- **Agent tự sửa:** claim CLM_056 đã gán nhầm mục đích của chân vịt dự phòng cho khoảng cách giữa module.
- **Storyboard sinh từ timing thật** (`concept/build_storyboard.py`).
- **Prototype:** P5 dễ đọc hơn; P6 là hoạt ảnh "thêm tầng → chìm → thân sâu hơn" theo đúng nhánh số.
- **Ảnh Schoonschip:** Commons không có ảnh PD, CC0 hay CC BY; chờ chủ kênh quyết.

## 0.11.0 — 2026-11-08 — Concept phim mới: "Could We Build an Entire City That Floats?"
- **Dự án concept mới `projects/floating-city-design-challenge`** (nhánh `concept-floating-city-design-challenge`). Đây là giai đoạn tiền sản xuất, không có kịch bản hay render sản xuất. Dừng ở buổi duyệt concept của chủ kênh.
- **Nghiên cứu:**
  - 14 nguồn, 48 claim, mọi trích dẫn khớp nguyên văn với bản tải về (`research/build_sources.py`).
  - Mỗi claim có `evidence_class` (ESTABLISHED_FACT, SPECULATIVE_PROPOSAL, UNVERIFIED).
  - Nguồn chặn tải hoặc không đọc được ghi ở `not_used`; không dùng bản lưu trữ để lách.
- **Hợp đồng kịch bản máy đọc** (`concept/scenario_contract.json`): mỗi giá trị có loại và căn cứ.
- **Mô hình tính minh bạch** (`analysis/design_model.py`, stdlib):
  - tính lực nổi, mớn nước, khoang, GM góc nhỏ, độ nhạy, quy mô, đánh đổi kích thước phao, dốc cầu;
  - nêu rõ những gì mô hình không chứng nhận.
- **Prototype hình độc lập** (`prototype/floating_prototype.py`): mặt cắt Archimedes, so sánh tải, khu ba phao, lộ cọc và dây neo dưới nước. Lỗi tìm thấy và bài học ghi ở `concept/PROTOTYPE_REPORT.md`.
- **Test:** `tests/test_floating_city_concept.py` (7 test).
- **`PROJECT_STATUS.md`:** cập nhật trạng thái hiện tại của cả ba dự án.

## 0.10.7 — 2026-11-07 — Phim Gothic: duyệt của chủ kênh, bản final 4K, kinh nghiệm chung
- **Chủ kênh duyệt bản g-r9 để render final 4K** và chọn bốn nhóm: 54 claim; giọng `am_michael` và phát âm; ảnh, ghi công và công bố AI; lời kêu gọi cuối và ngoại lệ chương 8. Agent ghi đúng các mục được chọn: `research/editorial_approval.json`, `config/tts_providers.json` (giọng cho dự án), `voice.license`, `voice.pronunciation_review`, `script/pronunciation.json`, `review/OWNER_APPROVALS.json`. Profile `PUBLICATION_CANDIDATE`; `final-gate` đạt.
- **`variety_exception` trong `project.json`** (`pipeline/chapters.py`): một chuỗi cùng loại hình dài hơn ngưỡng chung chỉ khi chủ kênh ghi quyết định; báo cáo QA nêu rõ. Ngưỡng chung 4 không đổi.
- **Kinh nghiệm chung** vào `docs/production/NEW_DOCUMENTARY_PLAYBOOK.md` mục 27–28 và `AGENTS.md`.

## 0.10.6 — 2026-11-07 — Phim Gothic g-r9: sửa cục bộ sau review g-r8
- **Theo review g-r8 của chủ kênh:** giữ hướng hình, chỉ sửa bốn chỗ. Chưa có gì được duyệt.
- **C6/B21–B22 (ảnh và niên đại):**
  - Phần trên dàn hợp xướng Saint-Denis được dựng lại từ 1231, nên ảnh apse (Ninaras) không còn đứng cho công trình 1140–1144 của Suger.
  - Ảnh mới: ambulatory còn lại từ thời Suger (NateBergin, CC BY 4.0).
  - Ảnh cửa sổ hoa hồng chuyển hoà sang ambulatory, đúng khung, không giật camera.
  - Chú thích "The ambulatory of Suger's choir, 1140–1144" và "Upper choir rebuilt in the 13th century" giữ qua lúc chuyển sang B22.
  - Nguồn mới: Atlas du patrimoine de la Seine-Saint-Denis (Michaël Wyss) và claim CLM_165, kiểm nguyên văn.
- **C6/B21 (nhãn gân vòm):** nhãn "Vault rib" chấm đúng vào một gân rõ; gân đó được vẽ sáng dọc chiều dài trong khoảng 1,6 giây.
- **C7/B29:** đổi thành SEQUENCE như B17.
  - Một trụ chống bay và trụ chống của nó được đánh dấu trên cả nhà thờ; phần còn lại mờ đi trong lúc camera tiến vào chỗ tiếp xúc.
  - Lực đẩy của vòm được vẽ vào flyer rồi tới đỉnh trụ chống, kèm nhãn "Lined up with its buttress".
- **C3/B09:** hai gối có từ đầu; dây treo được vẽ khi giới thiệu Hooke, lớn hơn; câu trích nằm bên phải; thao tác lật vẫn đúng chữ "turn".
- **C7/B25:** mở cận cảnh. Từ giây đầu, mũi compa đặt lên một chân vòm, cánh tay quay từ chân kia lên đỉnh, cung vẽ theo, rồi camera lùi ra cho hai bản lớn hơn. Độ dày nét theo đúng tỉ lệ.
- **Manifest chương** sinh lại theo mã shot hiện tại. Có bản ghép xem trước toàn phim 720p từ các chương: `gothic_cathedral_heights_G_R9_INTERNAL_REVIEW_720p.mp4`.
- **`final-assemble` với preset nội bộ** không còn đặt tên file FINAL. Bản ghép nội bộ lấy tên theo `review_label` của `project.json`, như `assemble`. Thêm test.
- **Long-form QA báo `visual_variety` FAIL:** 8 shot ảnh liền nhau ở chương 8, ngưỡng 4. Ngưỡng giữ nguyên; chờ chủ kênh quyết.

## 0.10.5 — 2026-11-07 — Phim Gothic g-r8: C4, C5, C2, C3, C7, C6 theo bảng việc của chủ kênh
- **Chủ kênh giao bảng việc từng chương**, thứ tự C4 → C5 → C2 → C3 → C7 → C6. Chưa có gì được duyệt.
- **C4:**
  - B14: ảnh nội thất Durham (Cornell University Library, không có hạn chế bản quyền đã biết), camera lên vòm gân; timeline tiến tới dải 1093–1133.
  - B15: sơ đồ một khoang, trước và sau: lực xuống trụ; tường nhạt, mỏng, mở thành cửa sổ rộng.
- **C5:**
  - B18: mặt bằng; tường dày cắt thành đoạn, **mỗi đoạn xoay 90°** thành trụ chống; vòm lộ vẽ dần.
  - B19: sơ đồ hai nguồn gốc theo BnF; ảnh trụ chống bay Chartres (CC BY 3.0) và mặt đông Notre-Dame (CC0).
  - B20: đường nước mưa vẽ dần, ghi "schematic"; hệ trụ cao lên bằng nét đứt.
- **C2:**
  - B04: đá bị kéo tách rời; vòm đá nén ở từng mạch.
  - B05: SEQUENCE Romanesque; vòm hạ xuống đặt lên tường, ép xuống rồi đẩy ngang.
  - B06: camera quay chính diện bức tường; tường, trụ áp tường, cửa sổ lần lượt sáng.
  - B07: mặt cắt Gothic; trụ, hệ trụ ngoài, ba công cụ lần lượt sáng.
- **C3:**
  - B08: vòm nhọn vẽ thành hai cung; đo đỉnh vòm.
  - B09: dây xích **xoay 180°** thành vòm.
  - B11: đỉnh vòm tròn và vòm nhọn được kẻ.
- **C7:**
  - B25: vòm dựng bằng compa, cùng tỉ lệ vẽ lớn dần.
  - B26: cọc, dây, hình vuông, thước và compa.
  - B27: trình tự theo nguồn: vẽ đủ cỡ, khung đỡ, đặt đá từ hai chân lên đá khoá, tháo khung.
  - B28: giàn giáo, ván khuôn, cần trục, thanh giằng gỗ rồi sắt.
- **C6:**
  - B21: ảnh thật Saint-Denis (CC BY 2.0, CC BY 4.0); nhãn có đường dẫn chỉ vòm nhọn, gân vòm, kính màu.
  - B22: camera vào ánh sáng của cửa sổ.
  - B23: cửa sổ hoa hồng bắc Chartres (public domain).
- **Card:**
  - `spin`: phần tử xoay quanh một tâm, theo câu hoặc từ.
  - Mọi phần tử của câu đầu không gắn với từ có mặt từ khung đầu, nên không card nào mở bằng khung trống.
- **Romanesque:** hỗ trợ SEQUENCE.
- **QA chú thích:** tia kiểm tra điểm neo theo hướng thật của camera tại khung đó. Trước đây QA dùng hướng của view đầu, nên sai với camera quay.
- **Mã shot đánh số lại** từ B18 (SC_n trùng Bn).
- Test: `ChapterRedesignTest` (5).

## 0.10.4 — 2026-11-07 — Phim Gothic g-r7: bản quét lớn, ghi công dễ đọc, nhịp B35, icon kêu gọi
- **Chủ kênh nhận xét g-r6:**
  - Giữ cấu trúc hình của đoạn thử, C1 và C8.
  - Bản vẽ mềm khi phóng lớn; dòng ghi công chìm vào ảnh; đoạn giả thuyết đổi điểm nhìn hơi nhiều; hai giây đầu C1 tối.
  - Đề nghị icon thay chữ ở đoạn kêu gọi like và subscribe.
  - Chưa có gì được duyệt.
- **Bản quét lớn:**
  - Ba hình của Viollet-le-Duc lấy từ bản quét DjVu public domain của *Dictionnaire raisonné* trên Commons: tập 1 trang 96 (hình 61), tập 2 trang 342 (hình 22) và 335 (hình 19). Mỗi trang dựng ở 1920 px.
  - Khớp tự động với các file 600 px cũ (tỉ lệ 2,32–2,41), nên khung giữ nguyên và dấu vẽ không phải đặt lại. Chi tiết gấp khoảng 2,4 lần.
  - Chữ của trang sách quanh hình 61 được cắt khỏi khung.
  - Bỏ bốn file PNG cũ, trong đó một file không được dùng và không có hồ sơ quyền.
- **Ghi công:** mọi dòng ghi công trên ảnh nằm trên một nền chữ nhỏ (`credit_line`).
- **B35:** giả thuyết 1 và 2 dùng chung một khung (trụ chống bay và phần trên), bớt một lần phóng–thu; các lần chuyển chậm hơn (1,4–1,6 giây).
- **B01:** camera bắt đầu ở đỉnh hàng vòm cuốn và triforium (có kính sáng), không còn ở vùng tối dưới cùng.
- **B45, kêu gọi cuối phim:** icon tự vẽ.
  - Bóng thoại khi đọc "comments"; ngón tay cái hiện viền rồi tô kín khi đọc "like".
  - Nút "SUBSCRIBE" đỏ đổi sang "SUBSCRIBED" xám, rồi chuông hiện.
  - Không dùng logo hay nhãn hiệu nền tảng. `config/production_defaults.json` và AGENTS.md ghi lại quyết định này.
- **Card:** `until_delay`, để phần tử rời đi một khoảng sau mốc `until` (nút được bấm).
- Bản review: C1, C8, C10 (720p, ngoài git). Blender QA 73/73; test 395/395.

## 0.10.3 — 2026-11-06 — Phim Gothic g-r6: chương 1 và 8 bớt dạng slide, chuyển góc B12, bỏ dấu X
- **Chủ kênh nhận xét g-r5:**
  - Hình rõ hơn, công trình được nhận diện; đoạn thử 3D gần đạt mức làm mẫu.
  - Nhưng C1 và C8 vẫn có cảm giác slide; dấu X ở B35 khẳng định quá mạnh; tiêu đề giữ quá lâu.
  - Đoạn chuyển vào khoang ở B12 khó định hướng; tuyến dây xích Amiens còn nhỏ.
  - Chưa có gì được duyệt.
- **Camera 2D cho card (stage):**
  - `graphic.stage.views`: các khung `rect` mà camera tới, theo câu hoặc từ, có `move_seconds`.
  - Phần tử `stage: true` (ảnh, dấu vẽ) zoom và lia cùng nhau; chữ đứng yên.
  - Thực thi trong `engine/diagram.py` (`stage_transform`, `key_stage`); planner tính thời điểm; `validator` kiểm view và phần tử; QA không coi ảnh trên stage là "ra ngoài khung".
- **`until_word`:** một phần tử card rời màn hình đúng lúc một từ được đọc.
- **`from_start`:** ảnh đầu tiên của card có mặt ngay từ khung đầu. Card ảnh không còn mở bằng 0,3 giây nền trống.
- **Đổi ảnh bằng chuyển hoà:** ảnh sau hiện đè lên ảnh trước (lớp cao hơn), ảnh trước rời đi khi ảnh sau đã vào. Trước đây hai lần mờ nối tiếp nhau tạo một khung trống.
- **C1:**
  - B01: ảnh dàn hợp xướng Beauvais phủ kín khung, camera lia lên vòm trong lúc kể 1284, rồi kéo ra ảnh bên ngoài. Chữ ghi "today".
  - B02: Amiens, camera lên dọc lòng chính tới vòm và cửa sổ hoa hồng.
  - B03: tiêu đề chỉ giữ tới "relying"; hai câu hỏi hiện trên mặt cắt Beauvais của Viollet-le-Duc (vòm cao, rồi trụ chống bay).
- **C8:**
  - B31, B32: ảnh phủ kín khung. Camera lên từng tầng theo lời; tầng trên đổi màu khi nói "adding".
  - B34: mặt bằng toàn cảnh rồi cận các khoang thẳng.
  - B35: mỗi giả thuyết, camera tới đúng phần đó. Nghiên cứu 2024 làm mờ mũi tên lún, ghi "Not supported by this study" (không còn dấu X).
  - B36: cận ba khoang đánh số 1–3, trụ mới hiện, rồi thành 1–6.
  - B37: ảnh, mặt bằng (giao cánh, phía tây), rồi lại ảnh; timeline trên dải đầu khung.
  - B38: ảnh Amiens, rồi mặt bằng lớn, cận trụ giao cánh, tuyến dây xích vẽ dần kèm nhãn "route schematic".
- **B12 (đoạn thử):** khoang được chọn đổi màu trên cả nhà thờ trước. Phần còn lại mờ nhưng vẫn còn trong lúc camera quay xuống; sàn ẩn hẳn. Khoang chỉ đứng riêng khi camera đã dừng.
- Test: `StageCardTest` (7).

## 0.10.2 — 2026-11-06 — Phim Gothic g-r5, bước 2–3: chương Beauvais và mở phim bằng ảnh thật
- **Chủ kênh đề nghị:**
  - Beauvais và Amiens phải có hình riêng.
  - Chuỗi trình bày: ảnh thật → đánh dấu bộ phận → mặt cắt hoặc mô hình → trở lại ảnh thật.
  - Timeline tiến theo lời.
  - Giả thuyết sập: mỗi giả thuyết một sơ đồ.
  - Duyệt từng chương trước khi render lại toàn bộ.
  - Chưa có gì được duyệt.
- **Ảnh và bản vẽ (Wikimedia Commons, kiểm giấy phép qua API):**
  - 4 ảnh chụp: Beauvais ba ảnh (CC BY 4.0, CC0), Amiens một ảnh (CC BY 3.0).
  - 3 bản vẽ public domain của Viollet-le-Duc: mặt cắt trụ chống bay Beauvais, mặt bằng Beauvais, mặt bằng Amiens.
  - Hồ sơ trong `assets/manifest.json`; ghi công trên hình và trong mô tả. Không dùng CC BY-SA. Bỏ một bản vẽ có tác giả và năm không chắc chắn.
- **Chương 8 (B31–B38):** card ảnh và bản vẽ, đánh dấu theo lời.
  - Ba tầng của dàn hợp xướng.
  - Vùng các khoang thẳng có vòm sập; không dựng cảnh sập.
  - Từng giả thuyết trên mặt cắt của Viollet-le-Duc.
  - Trụ mới giữa trụ cũ.
  - Cánh ngang, bốn trụ giao cánh, lòng chính không bao giờ xây.
  - Timeline tiến theo lời.
  - Tuyến dây xích Amiens dọc lòng chính, đúng như nguồn tả.
- **Mở phim (B01, B02):** ảnh thật của Beauvais (trong và ngoài dàn hợp xướng) và Amiens, thay cho mô hình chung ghi "not Beauvais/Amiens".
- **Card:** `Card.image`, `Card.credit`, `fitted` (pixel của ảnh → tọa độ card), `Card.drawn`, `Card.drawn_arrow`, `.later()`; phần tử card có `delay`.
- **`tools/longform_reports.py`:**
  - Mô tả YouTube không còn chép câu và dòng ghi công HAER của phim cầu vào phim khác.
  - Mục "Photographs and drawings" có giấy phép, đường dẫn và chỉnh sửa.
  - Phim cầu giữ nguyên văn.
- Bản review: `output/chapters_internal_720p/…C8…`, `…C1…` (ngoài git). Ghi chú duyệt: `review/REVIEW_G_R5.md`.

## 0.10.1 — 2026-11-06 — Phim Gothic g-r5, bước 1: sửa đoạn thử theo góp ý của chủ kênh
- **Chủ kênh nhận xét đoạn thử g-r4:** giữ hướng (chuyển động mang thông tin), nhưng phải rõ hơn trước khi nhân rộng.
  - Bớt lớp mờ phía sau.
  - Tăng tương phản cho bộ phận đang giải thích.
  - Hết cảm giác chân trụ treo trong không khí khi nhìn từ dưới.
  - Trụ ngoài phải rõ khi trụ chống bay xuất hiện.
  - Khung B17 thừa nền bên phải.
  - Camera đứng yên trong các thao tác quan trọng của B12.
  - Chưa có gì được duyệt.
- **Camera quay một cung ngắn (orbit) trong SEQUENCE:**
  - Mỗi view có thể có `azimuth`, `elevation` riêng; giữa hai view khác hướng, camera đi theo một cung quanh chủ thể (`framing.orbit_pose`).
  - Trong lúc quay, camera lùi ra rồi trở lại đúng khung của view sau, và dừng đúng khung tại mỗi view.
  - Một view nhìn từ dưới mặt đất thì preset phải ẩn mặt đất.
  - Chú thích xoay theo camera. Kiểm tra Blender còn so hướng nhìn ở mỗi view.
  - Planner so cả hướng camera ở match cut.
- **Màu nhấn (`tint`) cho bước HIGHLIGHT:**
  - Bộ phận chuyển dần sang màu `highlight` của bảng màu thay vì sáng lên; độ sáng phát ra giảm theo đúng tỉ lệ đó.
  - Lý do: đá sáng phát sáng trên nền sáng làm mất tương phản. `tint` mặc định 0, nên shot cũ không đổi.
- **Đường lực vẽ dần (`draw_seconds` trong `config/annotation_style.json`):**
  - `CONCEPTUAL_LOAD_PATH` hiện từng đoạn theo tuyến truyền lực, đầu mũi tên đến cuối cùng, rồi giữ nguyên hình.
  - Không kéo dài, không phồng lên, không có hạt chạy.
- **Card và timeline:**
  - Phần tử card có thể có `delay` sau câu hoặc từ của nó.
  - Timeline có vạch thời gian màu nhấn tiến tới từng mốc theo lời dẫn, rồi mốc mới hiện.
- **B12:**
  - Mở bằng cả nhà thờ đứng trên sàn. Phần còn lại, gồm cả sàn, mờ đi; một khoang đứng riêng, rồi camera quay xuống dưới khoang và nhìn thẳng lên (`UNDER_BAY`, −84°).
  - Gân chéo, phần đá giữa gân và trụ lần lượt hiện theo lời; trụ thành bốn tiết diện ở bốn góc.
  - Camera không chuyển động khi bộ phận đang đổi.
  - Chỉ giữ tường cao của khoang (mờ 0,9) làm mốc.
- **B13:** giữ góc nhìn thẳng từ dưới lên, tiến lại gần phần đá giữa gân. Các dải xen kẽ đọc thành "một chuỗi vòm"; không còn chân trụ lơ lửng.
- **B16, B17:**
  - Chỉ hệ trụ ở mặt cắt chờ mờ; các khoang phía sau bỏ hẳn hệ trụ, vì lớp mờ chồng nhau thành vệt.
  - Trụ ngoài đặc lại khi đọc "outside", trước khi trụ chống bay tới.
  - Khung B17 lấy thêm chân vòm cao, nơi lực đẩy "rời vòm".
- **Preset `CATHEDRAL_VAULT_BELOW`:** giữ sàn nhà thờ; shot bắt đầu dưới sàn phải ẩn sàn ngay từ đầu. Concept mới `church_floor`.
- **Đoạn thử g-r5:** `output/pilot/…PILOT_G_R5…` (git-ignored); báo cáo `qa/excerpt_PILOT_G_R5.json`.
  - Kiểm tra Blender 76/76.
  - Điểm cắt SSIM 0,99999 và 1,0.
  - −16,4 LUFS.
  - WER 0 ở cả bản có và không có tiếng đá.
- Test: 388/388 (thêm orbit, `tint`; test trụ chống bay đổi theo thiết kế mới: trụ ngoài đặc trước). Đánh giá planner 30/30.

## 0.10.0 — 2026-11-06 — Phim Gothic: đoạn thử vòm gân và trụ chống bay (shot SEQUENCE, âm thanh tổng hợp)
- **Chủ kênh nhận xét bản g-r3:** vẫn là bản dựng sơ bộ; mô hình đứng yên, camera chỉ tiến gần, ít cỡ cảnh. Chủ kênh đề nghị làm một đoạn thử 60–90 giây (vòm gân, trụ chống bay) để duyệt chất lượng hình trước khi áp cho cả phim. Chưa có gì được duyệt.
- **Shot SEQUENCE (mới):** một mô hình, các bước theo câu và theo từ của lời dẫn.
  - Camera trượt và zoom giữa các khung của một preset.
  - Các bước: làm mờ phần còn lại, cho mờ trở lại, ẩn dần, hiện dần, cho bộ phận hiện ra và đặt đúng chỗ, phát sáng. Mỗi lần sáng có bộ phận riêng.
  - Phần thực thi: `engine/motion.plan_sequence`, `templates`, `shot_builder` (khung từng view, rig chú thích theo camera, phần mờ không đổ bóng), Blender QA (`sequence_arrivals_land`, `sequence_views_framed`, chú thích theo camera), planner (chiến lược `SEQUENCE`, `sequence_clock`, match cut theo khung cuối), chú thích (chỉ bám khi camera đứng yên), `validate-plan`, QA phim dài, kiểm lời–hình.
- **Mô hình Gothic 1.1.0:**
  - mỗi khoang có hai gân chéo riêng (`rib_diagonal_b{n}a/b`);
  - phần đá giữa gân chia thành 5 dải mỗi mặt (`web_courses`): mỗi dải là một vòm từ gân chéo này sang gân chéo kia, đúng cách Heyman đọc vòm.
  - Concept mới: `high_roof`, `aisle_vault`. Tham chiếu `local` chọn đúng một bộ phận.
- **Camera:** `CATHEDRAL_VAULT_BELOW` (nhìn dốc từ dưới, đèn phụ từ dưới cho mặt dưới vòm), `CATHEDRAL_TRANSVERSE` (mặt cắt ngang, gần như chính diện).
- **Âm thanh:** `pipeline/sound.py` và `config/sound_design.json`: tiếng đá đặt xuống, tổng hợp trong dự án, tất định, nhỏ hơn lời dẫn 14 dB, không nhạc nền.
- **`tools/excerpt.py`:** đoạn trích của phim (các shot không cần liền nhau). Kèm bản không âm thanh để so; Whisper so lời dẫn có âm và không âm; ghi rõ chỗ nối đoạn trích.
- **Beat B12, B13, B16, B17** viết lại thành SEQUENCE; lời dẫn và timing không đổi. Bỏ ghi chú "Arrows show the idea…" ở B16 vì trùng với nhãn tự động "not to scale".
- **Kiểm tra Blender bắt được hai lỗi của chính SEQUENCE và đã sửa:** bộ phận đang hiện mà bị dời trước khi ẩn; bản sao mờ bị coi là lỗi khi cố ý mờ liên tục qua điểm cắt.
- Test: `tests/test_sequence.py` (18), cập nhật hai test về B13 và phần đá giữa gân theo thiết kế mới; ca đánh giá planner `SEQ-NEG-01`.

## 0.9.9 — 2026-11-06 — Phim Gothic: họ mô hình nhà thờ và bản review 720p
- **Chủ kênh yêu cầu:** dựng mô hình và bản internal review 720p; sửa và kiểm chứng B40; bổ sung nguồn Cluny và Beauvais; thêm bước kiểm tra vào playbook. Chưa có gì được duyệt.
- **B40:** số ở mục 0.9.8 (+10,6%, +86%) là của phép tính cũ, đã sai. `script/arch_statics.py` viết lại theo chương trình ArchSpread trong luận án Ochsendorf 2002: đo nhịp ở mặt trong, khớp mặt trong dịch chuyển, sập khi đường áp lực chạm mặt ngoài ở gối.
  - Bảng 5.3 (t/R 0,10, α 60°, voussoir 0,1°): nhịp +8,20% so với +8,2%; lực đẩy 2,16 Hmin; khớp 53,8→42,8° so với 53,8→42,7°.
  - Block 2006, Hình 5: giới hạn sập nhịp +11,17%, lực đẩy +83,8%, so với +11,49%, +85,10%.
  - Còn lệch: voussoir 1–10° cho khớp lúc sập 43–50°, luận án 40–42°; kết quả hơi đổi theo số bước tính. Phim không đọc các số này. Test `GothicThrustLineTest` giữ các so sánh.
- **Nguồn:** 35 nguồn, thêm luận án Ochsendorf, hai trang Stephen Murray, Harvard (Loeb Library), New Catholic Encyclopedia. `CLM_131`, `CLM_185` lên `high`; 9 claim dùng ở mức `medium`. Bài MDPI 2025 (HTTP 403) ghi ở `not_used`, không lách qua bản sao.
- **Họ mô hình `cathedral`:** mặt cắt Gothic và Romanesque vòm nôi, nền `site_level_ground`, vật liệu `stained_glass`, `roof_lead`, preset `CATHEDRAL_SECTION`, `CATHEDRAL_FROM_BELOW`. Đều `ILLUSTRATIVE`.
- **Planner và chú thích:**
  - `THRUST_ARROW`: mũi tên đẩy ngang, cùng độ dài, phải có claim.
  - `close_on`, `close_on_targets`: bộ phận để lấy khung hình. `glow_only`: bộ phận phát sáng.
  - `state_targets`, `same_scale` cho `SEQUENTIAL_STATES`.
  - Sửa lỗi: `close_on_targets` không truyền khung hình để so kiểu cắt, nên planner cho match cut trong khi camera có nhảy.
- **Tự xem bản dựng đầu rồi sửa** (`qa/EDITORIAL_REVIEW_TIMECODED.md`): camera nhảy và gân, web lẫn vào nhau ở B12–B13; hình gần như trống lúc có lời ở B09, B10, B21, B25, B41; cờ bay không được chỉ ra ở B19; ghi chú "same scale" ở B18 vượt quá bằng chứng. Không đổi lời dẫn, timing, ngưỡng hay cổng.
- **Playbook:** thêm bước bắt buộc "lời và hình có khẳng định vượt quá bằng chứng không?" và những lỗi QA tự động không bắt được.

## 0.9.8 — 2026-11-05 — Phim Gothic: g-r3 theo nhận xét thứ hai của chủ kênh (chưa render)
- **Nhận xét của chủ kênh về g-r2:** yêu cầu sửa, không phải duyệt. Chưa render, chưa dựng mô hình, chưa có gì được duyệt.
- **B40:** một đường vẽ lệch không chứng minh được rằng không có đường nào vừa. Card nay cho thấy nhiều đường hợp lệ trong một vòm, rồi chính vòm đó khi gối đỡ dịch ra tới giới hạn. Lời dẫn nói rõ thay đổi này.
- **`script/arch_statics.py` (mới):** tính lại ví dụ của Block, DeJong và Ochsendorf 2006 (Hình 4, Hình 5). So với số in trong bài: lực đẩy 16,2–24,4% so với 16–25%; giới hạn sập nhịp +10,6%, lực đẩy +86% so với +11,49%, +85,10%. Gần nhau, không trùng; bảng đầy đủ ở `research/RESEARCH_REPORT.md`. Phim không nêu các số này. Test `GothicThrustLineTest` giữ các so sánh.
- **B08:** bỏ phần trăm khỏi card, vì hai vòm trên hình không phải hai vòm của nghiên cứu.
- **B10, B14:** Cluny "whose construction began around 1088", timeline "Cluny III: construction begins". Nguồn mới: trang của di tích (Centre des monuments nationaux).
- **B14, B15:** bỏ câu đọc tên Roger Stalley vì nhịp kể; ý của ông giữ trong sổ claim (`CLM_144`).
- **Sổ claim:** 30 nguồn, 56 claim, phim dùng 53. `CLM_123` đồng bộ với B07 theo yêu cầu; tự rà thêm `CLM_143`, `CLM_156`, `CLM_157`, `CLM_161`, `CLM_185`, `CLM_190`, `CLM_191` để claim không rộng hơn lời dẫn.
- **Lời dẫn và timing:** 136 câu, 1.964 từ, 15:22; ASR đạt toàn bộ.
- **Xem trước:** ảnh vẽ thử 30 card ở `output/card_previews_g-r3/` (ngoài git), không phải bản render của engine.

## 0.9.7 — 2026-11-05 — Phim Gothic: g-r2 theo nhận xét đầu tiên của chủ kênh (chưa render)
- **Nhận xét của chủ kênh về g-r1:** yêu cầu sửa, không phải duyệt. Giữ cấu trúc, cách mở và lời kêu gọi. Chưa render, chưa dựng mô hình, chưa có gì được duyệt.
- **Lời dẫn:**
  - vòm nhọn có thể cao hơn trên cùng nhịp, và mức giảm lực đẩy tùy hình dạng, độ dày và tải (B08, B09, B42);
  - đường lực đẩy chỉ nói cho một vòm lý tưởng hóa, đọc rõ giả định, và mô hình không chứng minh công trình thật an toàn (B39–B41);
  - thay "no knowledge of material properties" bằng "without modern structural calculations" (B03, B25);
  - vòm gân nói rõ là kiểu bốn phần, hình đơn giản hóa, phần đá giữa các gân cũng chịu tải (B12, B13, B15);
  - Beauvais "more than 45 meters", hình liệt kê đủ các số (B01, B33);
  - Durham "begun in 1093", xong 1133, vòm làm theo giai đoạn (B14);
  - bớt đối lập Romanesque và Gothic (B06, B07), rút ngắn tranh luận sử gia và bỏ tên đọc (B24);
  - card B35 gắn nhãn "Hypothesis" và tên tác giả.
- **Nguồn mới:** Block, DeJong và Ochsendorf 2006; trang dự án Romano và Ochsendorf; Roger Stalley (hai trang Columbia); trang của nhà thờ Durham. Sổ claim: 29 nguồn, 53 claim, phim dùng 51. `CLM_133` không còn được đọc, `CLM_164` bổ sung bằng chứng cho B22. Bài 2006 viết "about 15% less" nhưng các số của chính bài cho 12,5% và 8%, nên phim không đọc phần trăm.
- **Tự rà thêm cùng loại lỗi:** B05 chỉ nói về thợ ở Amiens, B04 "stands largely by", B12 "two ribs" thay cho "two pointed arches".
- **Lời dẫn và timing:** 135 câu, 1.963 từ, 15:20; ASR đạt toàn bộ. Bỏ mục phát âm Timbert, còn 6 mục chờ chủ kênh nghe.
- **Công cụ và test:** `script_review.py` đo chuỗi card chỉ có chữ (`text_only_runs`). Test mới: các điểm chủ kênh đã sửa không bị đảo lại, và câu có nêu tên nguồn phải được beat đó dẫn đúng nguồn.

## 0.9.6 — 2026-11-05 — Phim mới "How Gothic Cathedrals Reached Impossible Heights": kịch bản để chủ kênh đọc (chưa render)
- **Dự án `gothic-cathedral-heights`, revision g-r1** (nhánh `episode-gothic-cathedral-heights`): 10 chương, 46 beat, 129 câu, 1.782 từ, khoảng 14,1 phút. Chưa render video nào, chưa có gì được duyệt, theo yêu cầu của chủ kênh.
- **Nghiên cứu:** 24 trang/tài liệu nguồn (MIT, Columbia, BnF, France Mémoire, ECSMGE 2024, Association Beauvais Cathédrale); 49 claim khớp nguyên văn với bản tải về. Britannica, UNESCO, Smarthistory, The Met chặn tải tự động nên không dùng (`research/source_snapshots.json` → `not_used`). Những chỗ nguồn lệch nhau nằm trong `research/RESEARCH_REPORT.md`.
- **Lời dẫn:** `am_michael`, ASR 129/129, đã khóa timing. Bảy mục ghi đè phát âm cho tên Pháp, tất cả `PENDING_LISTENING_REVIEW`. Audio nháp chưa vào git (`.gitignore`) để không làm nặng `.git` trước khi kịch bản được duyệt.
- **Hình:** kế hoạch chưa thực thi được: 30 card 2D có kế hoạch, 16 beat 3D `NEW_ASSET_REQUIRED`. Concept Gothic được thêm vào `config/visual_vocabulary.json` với `supported: false`.
- **Quy trình, lời kêu gọi cuối phim** (yêu cầu của chủ kênh): `production_defaults.json` → `closing_call_to_action`; `episode.py` chặn bước SCRIPT khi thiếu (chỉ với dự án có quy định này); playbook, prompt autopilot, checklist duyệt, AGENTS và CLAUDE đã cập nhật.
- **Công cụ mới:** `tools/script_review.py` sinh `review/SCRIPT_REVIEW.md` và bản nghe thử.
- **Sửa `episode.py`:**
  - bước INTERNAL_REVIEW nhận báo cáo ghép sạch khi video review đã bị dọn. Lỗi có sẵn từ lần dọn dẹp của 0.9.5, làm phim cầu báo sai OWNER_APPROVAL và làm một test thất bại;
  - AUDIO_LOCK báo đúng số giây (trước đó luôn là 0,0 s);
  - VISUAL_PLAN báo BLOCKED khi kế hoạch không thực thi được.

## 0.9.5 — 2026-11-05 — M8.2: duyệt m8-r4 và bản cuối 4K
- **Bản cuối 4K của m8-r4:** `output/why_bridges_look_different_FINAL_4K_2160p.mp4` (+ `.en.srt`, `audio_master_final_4k.wav`, `.sha256`; `shasum -a 256 -c` đạt cả bốn file). 3840×2160, H.264 BT.709, 24 fps, 28 687 khung (19:55), −16,4 LUFS, đỉnh thật −1,3 dBTP, 271 cue phụ đề. MP4 sha256 `47bd654f…`. Mọi gate `--preset final_4k` đạt: **PUBLICATION_READY**. Chưa đăng, chưa merge, chưa push; đăng là quyết định của chủ kênh.
- **Duyệt (2026-11-04, `APP-M8.4-CLAIMS-AND-PRONUNCIATION`):** 76 claim được lời dẫn dùng EDITORIALLY_APPROVED (6 claim không được nói giữ SOURCE_VERIFIED); danh sách 29 thuật ngữ ACCEPTED_BY_OWNER cho audio m8-r4; Corinne và Cincinnati CONFIRMED theo lời chủ kênh. **Agent không chứng kiến và không ghi một buổi nghe nào**; hồ sơ ghi rõ điều đó (`confirmation_basis`). Duyệt giọng `am_michael` theo dự án giữ nguyên.
- **Render:** 12 chương theo thứ tự, mỗi lần một Blender, `--release-frames`. Từ 19:27 đến 04:08 (8 giờ 41 phút; thời gian render thực 8,2 giờ, không có khoảng nghỉ do máy ngủ). Khoảng 3,1 giây mỗi khung ở shot 3D 4K, khoảng 0,6 giây ở shot 2D. Chương nặng nhất: C11 (khoảng 4,4 giờ).
- **Dọn dẹp trước render:** xóa PNG và video review cũ (m8-r2 1080p, m8-r3 720p, `renders/review`, `renders/preview`), giải phóng khoảng 31 GB. Giữ `renders/final_4k`, `output/chapters_final_4k` (bản trung gian 4K) và hai thư mục `baseline_*` của M7. Các file này nằm ngoài git (`.gitignore`).
- **Kiểm tra:** test offline 322/322, test Blender 21/21 (repo không đổi), đánh giá lập kế hoạch 29/29, Blender QA 944/944, manifest khớp.
- **Đã sửa khi ghép:** kế hoạch hình báo cũ vì `sources.json` đổi khi ghi duyệt; chạy lại `plan-visuals`, `validate-plan`, `build-shots`. Chỉ hai hash của kế hoạch đổi; shot, khung và timing giữ nguyên.

## 0.9.4 — 2026-11-04 — M8.2: m8-r4 theo lần nhận xét thứ hai của chủ kênh (chưa render)
- **Nhận xét** (`REV-M8.2-SECOND-TEXT-REVIEW`): yêu cầu sửa, không phải duyệt. Chưa render gì, theo yêu cầu.
- **Gói duyệt:** phần "Các điểm cần lưu ý" (từ `review/EDITORIAL_NOTES.md`) viết lại theo phim hiện tại. Các câu đã bỏ ("200 to 300 feet", "133 years", "Today…") chỉ còn ở mục "Đã bỏ" kèm lý do. Card B23C được mô tả là hai loại số, không phải toàn dải kinh tế. Thời lượng và trần ghi đúng 19,9 phút / 30 phút.
- **Card B24B:** "1980–2012: almost all new U.S. bridges with / main spans over 1,000 ft were cable-stayed" (trước: "U.S. spans over 1,000 ft cable-stayed").
- **B33:** lời dẫn và card giữ "long after timber trusses stopped being competitive", như B09 và NCHRP §3.3.1. Nhãn "Stone arches return briefly" hạ xuống để có chỗ cho dòng thứ ba.
- **Revision m8-r4:** 169 câu, 19,92 phút (28 687 khung); B33.s1 đọc lại, ASR WER 0. QA dài PASS; 2 shot cần render (SC_058, SC_073).
- **Kiểm tra:** test offline 321/322; test còn lại so bản ghép 720p (m8-r3) với timing m8-r4 và sẽ đạt sau lần render tới. Gates G4/G5 FAIL vì media cũ. Không chạy Blender.

## 0.9.3 — 2026-11-04 — M8.2: bản review nội bộ cuối 720p
- **Bản review nội bộ cuối 720p (m8-r3):** `output/why_bridges_look_different_M8_INTERNAL_REVIEW_720p.mp4` + `.en.srt`; 1280×720, 28 651 khung (19:54), −16,4 LUFS, 271 cue phụ đề. Render 75 shot + 12 chương + ghép mất 2 giờ 10 phút (07:28–09:38, 2026-11-04). Cổng G0–G5, GL, GV đạt; G1 và G6 vẫn chờ chủ kênh (claim, phát âm, giọng nghe thực).
- **Trần thời lượng:** `runtime_decision` 8–30 phút (30 do agent chọn khi chủ kênh bảo nâng trần; `DEC-M8.2-CEILING-AND-720P`).
- **Preset mới:** `internal_720p` (1280×720). Test offline 321/321.

## 0.9.2 — 2026-11-04 — M8.2: sửa nội dung theo nhận xét biên tập của chủ kênh (nhánh `m8-all-bridge-families`)
- **Nhận xét của chủ kênh** (`REV-M8.2-EDITORIAL-REVIEW`): là yêu cầu sửa, không phải duyệt. Chưa render video, theo yêu cầu.
- **Revision m8-r3:** 169 câu, 19,90 phút; 82 claim, 18 nguồn.
  - Bỏ câu "133 years" (phản chứng: cầu Williamsburg 1903) và giới hạn "200 to 300 feet".
  - Card dải nhịp tách dải thực dụng/kinh tế khỏi nhịp đã xây.
  - Các nhận định 2005/2012 được nói kèm năm.
  - Công-xôn: nói rõ dạng có khớp. Card nền đất: "blocks or bedrock". Queensboro: "Unlike our model, it has no suspended span".
  - Năm sửa nhỏ về câu chữ.
  - Mỗi claim thu hẹp có `assumptions` ghi phần không dùng và lý do.
- **Nguồn mới:** e-WV "Wheeling Suspension Bridge" (Emory L. Kemp): nhịp, không phải chiều dài cầu. **Claim mới:** CLM_794.
- **Ghi đè phát âm đầu tiên của phim** (`script/pronunciation.json`): Corinne, Cincinnati, đều chờ chủ kênh nghe. Promontory, Covington, Finley bỏ khỏi danh sách vì không được đọc.
- **Test:**
  - class `OwnerEditorialReviewTest` mới;
  - bản sao "chủ kênh đã duyệt" giả lập trong test nay đánh dấu cả mục ghi đè phát âm;
  - kiểm tra khóa timing truyền lexicon;
  - cổng cuối của phim thật phải báo PRON_CORINNE chưa nghe.

## 0.9.1 — 2026-11-03 — M8.1: ba họ nhịp lớn trong các chương yếu tố, quyết định và kết luận (nhánh `m8-all-bridge-families`)
- **Yêu cầu của chủ kênh:** các chương sau phần giới thiệu các loại cầu cũng phải nói về công-xôn, cầu treo và dây văng (có nghiên cứu, lôi cuốn), và không giữ khắt khe giới hạn thời lượng.
- **Revision m8-r2:** 12 chương (thêm C10 "Span, cost and time"), 66 beat, 167 câu, 19,3 phút. 14 claim mới (tổng 81).
  - Câu chuyện mới: xích sắt và "weakest link"; nền đất và khối neo; công-xôn khi trụ lún; gió và Tacoma Narrows (chỉ kể bằng lời); dải nhịp của sáu họ cho cầu thép; chi phí và tay nghề; dòng thời gian nhịp lớn; cầu đường sắt Niagara và "133 years"; hẻm Kentucky 1877; Golden Gate; Penobscot Narrows; các cầu treo nhỏ.
  - Nguồn mới: FHWA-HRT-14-067. Ảnh mới: HAER CA-31 cầu Golden Gate.
- **Thời lượng:** `project.json` → `runtime_decision` (quyết định của chủ kênh, 8–20 phút; trần 20 do agent đặt).
  - `pipeline/chapters.runtime_range` chỉ dùng bản ghi khi có đủ người quyết định, ngày và cơ sở. Test kiểm cả trường hợp bản ghi thiếu.
- **Phần tử dòng thời gian hiện theo từ được đọc** (sửa một đoạn tĩnh 15,2 s).
- **Card dải nhịp chỉ vẽ con số có nguồn:** giàn đơn 450–750 ft; công-xôn chỉ có mũi tên.
- **Snapshot nguồn** chuyển vào `research/snapshots/` (git bỏ qua); `source_snapshots.json` nay có cả FHWA (vốn bị bỏ sót ở 0.9.0) và Penobscot.
- **Bản review nội bộ 1080p của m8-r2:** 27.828 frame, 19:19,5, −16,4 LUFS, 264 cue phụ đề.
  - Gates: `TECHNICALLY_VALIDATED`; G1 PENDING_EDITORIAL (0/75 claim, 32 thuật ngữ); G6 BLOCKED.
  - Agent xem lại trên video và sửa 3 chỗ: nhãn "Stiffening truss" ở cảnh Tacoma; NOTE "Niagara Gorge, 1855"; tiêu đề card dòng thời gian nhịp lớn.
- **Đã biết, chưa sửa:** `runtime_decision` không nằm trong `PROJECT_NON_VISUAL` (`tools/render_cache.py`), nên ghi trường này làm mọi shot mất cache; 48 shot render lại chỉ vì lý do này. Đề xuất sửa cùng lần thay đổi kế tiếp mà dù sao cũng phải render lại.

## 0.9.0 — 2026-10-31 — M8: phim làm lại với đủ sáu họ cầu (nhánh `m8-all-bridge-families`)
- **Yêu cầu của chủ kênh:** làm lại `why-bridges-look-different`, kết hợp nội dung đã có, với đủ các loại cầu và đủ mô hình. Bản 4K đã duyệt của m7-r1 được giữ (tag `m7-final-4k`, `output/baseline_m7_final_4k/`).
- **Mô hình mới:**
  - cầu công-xôn (tay neo, tay hẫng, nhịp treo);
  - cầu treo (tháp, cáp chính qua yên cáp, dây treo, dầm ngang, giàn tăng cứng, khối neo);
  - cầu dây văng (tháp chữ H bê tông, dây văng xuống dầm biên, mặt cầu chia đốt).
  - Đặt trên site mới 72 m, kèm tham số, kiểm tra chéo hình học, số bộ phận kỳ vọng và cấu hình nổ tách.
  - Offline 8/8 và Blender 4/4 cho mỗi asset.
- **Planner:**
  - concept khai báo được `scene_context` và `site`; mỗi ngữ cảnh có site và trạng thái site trống riêng;
  - shot ứng viên của bộ bố cục mang `scene_context` (sửa một lỗi có từ M6);
  - mặt đất nới lên 1 km.
- **Nghiên cứu:**
  - thêm FHWA-IF-12-052 vol. 5 (2012, bản lưu Internet Archive của URL FHWA) và các mục NCHRP §3.1, §3.5, §3.7;
  - 25 claim mới khớp nguyên văn, tổng 67;
  - hai ảnh HAER phạm vi công cộng: Queensboro (NY-19), Brooklyn (NY-18).
- **Kịch bản m8-r1:** 11 chương, 54 beat, 133 câu, 14,46 phút.
  - Bỏ B23, B23B, B24B và một câu của B53 để giữ thời lượng ≤ 15 phút.
  - Sửa câu chữ, không nới luật: một chỗ ASR nghe nhầm đồng âm; một mâu thuẫn lời–hình ("side by side" khi hình là sơ đồ).
- **Duyệt:**
  - duyệt claim và phát âm của m7-r1 không áp sang m8-r1 (`build_sources.py` nay kiểm `narration_revision`);
  - duyệt giọng theo dự án vẫn giữ;
  - profile trở về `NARRATED_INTERNAL_REVIEW`;
  - `review/OWNER_APPROVALS.json` ghi REQ-M8-ALL-FAMILIES.
- **Sửa lỗi:** `research/build_sources.py` còn trỏ tới đường dẫn cũ của sổ claim M6, bị bỏ sót khi dọn dẹp ở 0.8.0. Nay trỏ sang fixture; bản build lại trùng từng byte.
- **Test:**
  - `tests/test_m8_long_span.py` (mới);
  - các test M7 kiểm logic duyệt trên một bản sao mô phỏng duyệt; phim thật được khẳng định đang chờ duyệt;
  - ca "họ chưa có bộ sinh" chuyển từ cầu treo sang cầu cất (bascule).
- Tài liệu: `docs/m8/M8_REPORT.md`; bổ sung AGENTS.md, playbook, báo cáo dọn dẹp.

## 0.8.0 — 2026-10-31 — M7 finalization: hồ sơ duyệt, cổng xuất bản, bản cuối 4K, hệ thống sản xuất V1 (nhánh `m7-finalization-4k-production`)
- **Hồ sơ duyệt của chủ kênh** (`review/OWNER_APPROVALS.json`), mỗi quyết định gắn với revision và tự mất hiệu lực khi revision đổi:
  - 41 claim (`claims_text_sha256` + `narration_sha256`);
  - giọng `am_michael` cho riêng dự án này (`clearance.voice_approvals`, kèm SHA256 giọng). `voices_cleared` không đổi;
  - phát âm `ACCEPTED_BY_OWNER`, gắn với hash audio, không ghi là đã nghe từng mục;
  - CLM_747: không dùng trong phim, không duyệt hộ.
- **Cổng:**
  - cổng cuối chỉ đòi duyệt các claim mà phim dùng (`validator.used_claim_ids`);
  - validator từ chối licence APPROVED cho giọng không có trong `voices_cleared` cũng không có duyệt cho dự án;
  - G1 báo đúng cơ sở phát âm ("accepted by the owner, no per-item listening recorded").
  - `gates --preset final_4k`: **PUBLICATION_READY**. Lần chạy đầu GL FAIL vì báo cáo phim dài đã cũ; kiểm tra được chạy lại trên timing hiện tại, không nới luật nào.
- **Preset `final_4k`** (3840×2160, CRF 16, x264 `slow`, BT.709, AAC 256k):
  - `chapter --release-frames`: render → bản trung gian H.264 (ghi nguyên tử) → kiểm chứng (SHA256, khóa cache từng shot, số frame, giải mã) → registry `qa/chapter_intermediates_final_4k.json` → mới xóa PNG;
  - dừng khi đĩa còn dưới 8 GB;
  - `final-assemble`: ghép stream copy, thêm lời dẫn và phụ đề, QA media (thẻ màu, giải mã, đoạn đen, SSIM ranh giới chương), WAV master, `.sha256`.
- **Sửa lỗi:** PNG sRGB làm luồng H.264 bị gắn transfer `iec61966-2-1`. Bộ lọc giờ ghi rõ BT.709 (`setparams`).
- **Bản cuối 4K** `why_bridges_look_different_FINAL_4K_2160p.mp4`:
  - 5.218/15.395 frame được render, 3 giờ 59 phút;
  - so với render trực tiếp: PSNR 49–57 dB;
  - audio và phụ đề giống từng byte với bản review.
  - Bản review 1080p giữ nguyên. Ảnh HAER được thay bằng rendition 3840 px (có `previous_rendition`).
- **Dọn dẹp:**
  - `projects/` chỉ còn phim đang làm. 6 pilot cũ được `git mv` sang `tests/fixtures/legacy_projects/`; 13 module test đọc fixture, assertion giữ nguyên;
  - file sinh ra (3,36 GB) chuyển ra ngoài repo bằng `tools/archive_projects.py` (checksum trước và sau), kèm `git bundle --all`;
  - states mái cũ ở `asset_library/legacy_states/`, catalog giữ asset id.
- **Sản xuất V1:**
  - `docs/production/NEW_DOCUMENTARY_PLAYBOOK.md`, `prompts/NEW_DOCUMENTARY_AUTOPILOT.md`, `config/production_defaults.json`, `docs/production/templates/`;
  - `tools/episode.py` (`new`, `status`, `next`; giai đoạn suy từ file) và alias CLI `new-episode`, `episode-status`;
  - `--project` mặc định là dự án duy nhất trong `projects/`; `evaluate-planning` không cần dự án; `pronunciation_test.py` bắt buộc `--project`.
- **Tài liệu:** `docs/m7/M7_FINALIZATION_REPORT.md`, `docs/m7/PERFORMANCE_4K.md`, `docs/production/CLEANUP_REPORT.md`; cập nhật `AGENTS.md`, `CLAUDE.md`, `PROJECT_BRIEF.md`, `README.md`, `QUICKSTART_MAC.md`.

## 0.7.1 — 2026-10-30 — M7: bản review nội bộ cuối (giọng `am_michael`, 1080p, nhánh `m7-final-internal-review`)
- **Quyết định của chủ kênh:**
  - Duyệt 41 claim được lời dẫn dùng (`research/editorial_approval.json`, được `build_sources.py` áp vào; `factual_review: verified`).
  - Đổi giọng đọc sang `am_michael`.
  - Bỏ dòng ghi giọng đọc khỏi card B35.
- **Lời dẫn:** sinh lại toàn bộ bằng `am_michael` (G2P Anh–Mỹ): 103 câu, ASR 102/102 đạt, căn từ lại, timing khóa lại. Phim dài **641,46 s**.
- **Quyền giọng:** `am_michael` đã audit (hash khớp VOICES.md) nhưng **chưa được cấp quyền xuất bản**.
  - Clearance của Kokoro giờ ghi rõ `voices_cleared` và `voices_pending`.
  - Validator từ chối licence APPROVED cho giọng chưa được cấp quyền.
  - Tên file chỉ "sạch" khi đủ cả claim, licence, xác nhận cho phim và phát âm.
- **Tối ưu render:** dùng lại frame tĩnh dựa trên motion plan.
  - Phân loại STATIC/ANIMATED 2D/3D, HYBRID, FALLBACK_FULL_BLENDER; frame lặp là hardlink.
  - Thêm `--no-reuse`, `verify-reuse` (so với mức nhiễu nền của EEVEE) và `--mode reuse-report`.
  - Ở 1080p chỉ render 5.206/15.395 frame.
- **Preset `internal_1080p`:** 1920×1080 cho review nội bộ; tên `…_M7_FINAL_INTERNAL_REVIEW_1080p.mp4`; `final` vẫn sau G6.
- **Worker và gói tạo giọng:** worker Kokoro giữ G2P riêng cho mỗi `lang_code`. Thêm `tools/kokoro_fetch_voices.py`; `voice_audition.py` hỗ trợ `--voices us`, `--passage` và ghi nhận clip không qua kiểm tra mà không dừng.
- **Sửa lỗi:** commit `b7e5b0a` đã ghi đè báo cáo QA chính thức của `suffolk-roofs` bằng kết quả hồi quy 71/72, làm `test_suffolk_statuses_are_unchanged` thất bại. Báo cáo của `suffolk-roofs` được khôi phục; kết quả hồi quy được giữ ở `qa/regression/` của M7.
- Tài liệu: `docs/m7/FINAL_INTERNAL_REVIEW.md`; bổ sung audit Kokoro §8.

## 0.7.0 — 2026-10-30 — M7: phim tài liệu dài đầu tiên, "Why Bridges Don't All Look the Same" (nhánh `m7-first-full-documentary`)
- **Phim** `projects/why-bridges-look-different`: 10,77 phút, 8 chương, 39 beat, 103 câu, 47 shot.
  - Hình trộn: 3D, sơ đồ, bản đồ sơ lược, dòng thời gian, 4 ảnh HAER phạm vi công cộng.
  - Bản review 960×540, MP4 cho từng chương, rough cut 640×360, 47 still 1080p.
  - Trạng thái INTERNAL REVIEW (`TECHNICALLY_VALIDATED`, `EDITORIAL_REVIEW_PENDING`, `TTS_RIGHTS_PENDING`).
- **Nghiên cứu:** `research/build_sources.py` → 12 nguồn, 42 claim khớp nguyên văn (NCHRP 25-25(15), ASCE, Yale, FHWA, ODOT, SCI, HAER), kèm báo cáo nghiên cứu, ma trận bằng chứng và gói duyệt biên tập. Chưa claim nào được duyệt.
- **Kịch bản một nguồn:** `script/story.py` sinh `narration.json`, `visual_beats.json` và `chapters.json`.
- **Chương** (`pipeline/chapters.py`):
  - validate (fail closed), dải shot/frame của từng chương, manifest kèm bằng chứng theo chương;
  - QA phim dài với 17 kiểm tra; cổng GL;
  - CLI `chapters` và `chapter --chapter Cn` (render + mã hóa + ghép + QA một chương, có WAV);
  - mode `documentary`.
- **Card 2D** (`engine/diagram.py`): phần tử rect/line/circle/polygon/image (vùng cắt, trôi chậm), `disappear`, tấm nền chữ. Planner lập kế hoạch thời lượng card (`templates.plan_card`). Phần tử card và chú thích hiện theo **từ được đọc** (word timestamp Whisper). QA `card_layout`: vùng an toàn, vùng phụ đề, chữ không chồng nhau.
- **Ảnh ngoài:** hồ sơ quyền đầy đủ (`EXTERNAL_LICENSE_FIELDS` + `credit_keys` + SHA256). Validator từ chối ảnh thiếu hồ sơ, sai đường dẫn hoặc thiếu file. QA kiểm giấy phép và ghi công. Byte ảnh là đầu vào render.
- **Camera và chú thích:**
  - HOLD `camera_move` PUSH_IN; shot kế tiếp luôn cắt cứng;
  - chú thích NOTE cố định trên màn hình;
  - rig chú thích đi theo camera trong push-in (kênh `scale`, QA `overlays_screen_fixed`).
- **Render:** khôi phục render bị ngắt cùng khóa cache (`render_progress.json`, kiểm PNG hoàn chỉnh, `--resume`). Mã hóa cả phim từ một chuỗi frame liên kết. Contact sheet giới hạn số ô. Hồ sơ quyền, chương và trạng thái claim không làm cũ frame.
- **Âm thanh:** ASR dùng lại bản chép cho audio giống hệt. `narrate` không còn bị chặn khi beat của dự án audio-first đổi. Worker Kokoro giữ G2P riêng cho mỗi `lang_code`. Xuất master lời dẫn và audio từng chương. Tên file có `_INTERNAL_REVIEW` và metadata ghi rõ khi còn thiếu duyệt.
- **Cổng:** G2 tôn trọng `owner_confirmation_for_this_film: PENDING`; G1 tôn trọng `pronunciation_review.status: PENDING`; GL bắt buộc cho dự án có chương.
- **Thử giọng Anh–Mỹ:** `tools/kokoro_fetch_voices.py` + `tools/voice_audition.py --voices us`. 20 giọng đã kiểm hash, chỉ dùng để nghe.
- **Công cụ:** `tools/longform_reports.py` (ma trận bằng chứng, gói duyệt, mô tả YouTube bản nháp, kiểm tra đa dạng hình, gói nghe phát âm), `tools/frame_times.py` (tốc độ render không tính lúc máy ngủ).
- **Test:** 310 test đạt (290 offline + 20 Blender), gồm 60 test M7 mới có ca âm. Đánh giá planner 29/29.
- **Phát hiện:** kiểm tra `card_layout` mới chỉ ra ghi chú chân trang của card `suffolk-roofs` SC_004 nằm dưới vùng an toàn từ M3. Chưa sửa vì dự án M3 giữ nguyên trạng thái.

## 0.6.1 — 2026-10-29 — M6: quyết định của chủ kênh
- Giọng kênh `bm_george` (do người dùng chọn). Lời dẫn được sinh lại, 143.4 wpm. B1.s1 viết lại vì ASR nghe nhầm. Pilot dài 151.33 s.
- Chủ kênh cấp quyền xuất bản cho Kokoro (`clearance` trong registry, `PUBLICATION_CLEARED`); license giọng APPROVED; 14 claim EDITORIALLY_APPROVED (narration `m6-r2`); phát âm được chấp nhận; `factual_review: verified`.
- Lời dẫn được sinh lại dưới hạng quyền mới. Seed cố định nên giống hệt từng bit bản preview; khung hình không cần render lại.
- `bridge_load_explained_pilot_review.mp4`: gate G0–G6 + GV PASS. Profile vẫn là NARRATED_INTERNAL_REVIEW.
- Test được cập nhật theo trạng thái đã duyệt; các ca âm (thiếu clearance, provider đang chờ duyệt, rút lại một phê duyệt) vẫn bị chặn.

## 0.6.0 — 2026-10-29 — M6: phim tài liệu có lời dẫn, chú thích kỹ thuật, nhiều họ kiến trúc (nhánh `m6-narrated-documentary`)
- **TTS Kokoro-82M** (`integrations/tts/kokoro.py`, `tools/kokoro_tts.py`):
  - pin revision `f3ff3571` và 4 giọng Anh–Anh có SHA256 đã kiểm; worker con stdin/stdout (không mở server); offline; seed theo câu;
  - audit license `docs/licensing/KOKORO_LICENSE_AUDIT.md`; hạng quyền `PENDING_REVIEW`;
  - `tools/voice_audition.py` (4 giọng, số đo + ASR, không tự duyệt giọng);
  - dạng phát âm misaki trong `pronunciation.json`; đường dẫn audit lấy từ registry.
- **Khóa theo audio cho dự án do planner lập kế hoạch:**
  - `pipeline/audio_lock.py`, lệnh `lock-audio`; `build-shots` gọi finalize;
  - validator nhận beat trải nhiều shot; `check_consistency`;
  - plan lưu `timing_sha256` để phát hiện plan cũ.
- **Chú thích ngữ nghĩa:**
  - `planner/annotations.py`, `engine/annotation_layout.py`, `engine/annotations.py`, `engine/qa_annotations.py`, `config/annotation_style.json`;
  - 7 loại: COMPONENT_LABEL, CALLOUT, LOAD_ARROW, REACTION_ARROW, CONCEPTUAL_LOAD_PATH, TENSION_COMPRESSION_LEGEND, HIGHLIGHT_REGION;
  - kiểm bằng chứng theo claim và bộ phận; điểm neo trên silhouette nhìn thấy được; bố cục tránh vùng phụ đề; fade theo câu;
  - QA Blender: ray-cast điểm neo, đo bề rộng chữ thật;
  - `tools/annotation_preview.py`.
- **Planner:**
  - intent `EXPLAIN_LOAD_PATH`; `highlight_at_sentence`; `visual_repair_preference`;
  - cắt theo câu (AUDIO_LOCKED); chú thích tiêu đề đặt trên cùng và dải nhãn 0.24 cho dự án có lời dẫn;
  - từ vựng `superstructure`, `substructure`, `ground`.
- **Nhất quán lời/hình** (`planner/consistency.py`): 7 luật, CONTRADICTION làm plan không chạy được, `validate-plan` tính lại.
- **Nhiều họ kiến trúc:** scene context (`states.json` schema 3, `spec.context_view/shot_states`, `scene_context` trên shot); camera theo ngữ cảnh; từ chối khung chung giữa hai ngữ cảnh; fixture `tests/fixtures/m6_cross_family`.
- **Lắp ráp:** phụ đề mềm mov_text trong MP4 (ngoài SRT); media QA yêu cầu track phụ đề.
- **QA Blender:**
  - kiểm tra glow dùng cùng luật với L1 (share ≥ 0.25 hoặc mặt gọn ≥ 0.2 %);
  - kiểm tra exploded bỏ qua track chú thích;
  - nhãn TOP được kiểm.
- **Báo cáo:** `research-map` (câu → claim → nguồn → asset → bộ phận → chú thích → thời điểm → QA).
- **Profile:** alias `INTERNAL_NARRATED_PREVIEW` = `NARRATED_INTERNAL_REVIEW`.
- **Pilot mới `bridge-load-explained`:** "How Does a Bridge Carry Its Load?", 8 beat, 14 claim (ODOT/FHWA/SCI/Yale), 26 câu Kokoro `bm_george` (giọng do người dùng chọn; bản đầu dùng `bf_emma`), 11 shot, 151.33 s, 27 chú thích trên 9 shot (+ thẻ "not to scale").
- **Sửa bridge-story-m5 B7:** "Side by side, …" thành "Let's compare them one at a time: …". Chỉ 3 shot của B7 đổi thời lượng.
- **Đánh giá planner:** 29 ca (thêm 5 ca M6).

## 0.5.5 — 2026-10-28 — M5.5: trí tuệ hình ảnh, bố cục thích ứng, profile sản xuất (nhánh `m5.5-visual-intelligence`)
- **Level 1, mức nhìn thấy offline** (`planner/visibility.py`): dựng lại cảnh theo luật của engine, rồi raster độ sâu + ID (192×108) tại frame đầu, 25/50/75 %, frame cuối và mọi marker. Các chỉ số: diện tích chiếu, share nhìn thấy, *core* (không phải vệt mảnh), vật che, dải phụ đề, cắt khung, từng viên. Trạng thái ESTIMATED/UNCERTAIN.
- **Level 2 trong Blender** (`engine/qa_visibility.py`, `verify-visibility`): tia orthographic trên mesh đã evaluate, cùng các frame. Báo cáo so với L1 ở `qa/VISIBILITY.md`. Pilot: 122 dòng, kết luận trùng 100 %, sai số share trung bình 0.006.
- **Sửa kế hoạch** (`planner/repair.py`): REFRAME → SAFE_BAND → ALT_CAMERA → GHOST → chiến lược tiếp theo → VISIBILITY_UNRESOLVED. Camera không được phá cắt match, trừ vấn đề kích thước. Mọi ứng viên được ghi lại; cách chọn ghi vào plan; `validate-plan` tính lại và kiểm tra. Ghost giờ dựa trên vật che đo được; `ghost_roles` của từ vựng đã bị bỏ.
- **Bố cục so sánh thích ứng** (`planner/composition.py`): đo STACK và ROW (nhiều gap) ở 640×360 (thành phần điển hình ≥ 2.5 px; mô hình ≥ 25 % chiều rộng), theo mục đích `detail` hoặc `overview`. Chiến lược mới: SEQUENTIAL_COMPARISON (một camera, một tỷ lệ, nhãn HOLD), DETAIL_THEN_OVERVIEW, FOCUSED_PAIR. CLOSEUP_EXPLODE cho thành phần `read_as: pieces`: cận cảnh chính diện, các viên kéo ra khỏi mặt và tỏa ra.
- **Engine:**
  - `engine/house_layout.py`: số đo nhà/mái M2 thuần Python, dùng chung với proxy offline (27 shot giống hệt);
  - `animation.label` cho HOLD;
  - `camera_focus` fit cả bao chuyển động;
  - kiểm tra nhãn cho HOLD.
- **Profile sản xuất:** `production_profile` = TECHNICAL_SILENT_PREVIEW / NARRATED_INTERNAL_REVIEW / PUBLICATION_CANDIDATE.
  - Profile không lời: G2/G3/G5 là NOT_APPLICABLE; thêm gate GV (plan + coverage); G4 stale tính theo khóa render.
  - Validator từ chối profile không lời trên dự án có lời dẫn.
  - PUBLICATION_READY chỉ có ở PUBLICATION_CANDIDATE (cần `publication_metadata`).
  - Gate của Suffolk không đổi.
- **Media QA cho video không lời:**
  - kiểm tra độ phân giải, fps, codec, thời lượng so với số frame;
  - kiểm tra không có audio và không có lỗi giải mã;
  - ghi ranh giới shot, `storyboard_sha256`, `plan_sha256` và khóa render từng shot.
- **Bộ đánh giá** `evaluation/visual_planning/cases.json` (24 ca: dương, âm, mơ hồ, thiếu năng lực; cầu + mái), `evaluate-planning` → `RESULTS.md`. 24/24 ca đạt trên 10 chiều.
- **Pilot** `bridge-story-m5` lập kế hoạch lại:
  - 15 shot, 72.375 s;
  - B4 CLOSEUP_EXPLODE; B7 SEQUENTIAL_COMPARISON; B8 STACK gap 0.25 (overview);
  - SC_003 ghost chọn tự động;
  - QA Blender 188/188, media QA PASS, profile không lời: VALID, NOT FOR PUBLICATION.
- **Fixture mái:** R2 được REFRAME (đòn nóc quá nhỏ), và khung giữ trọn mọi phần bung. QA 52/52.
- **Test:** 207 (thêm `tests/test_m55_visual_intelligence.py` 29 test, `tests/test_blender_m55.py` 4 test).

## 0.5.0 — 2026-10-28 — M5: lập kế hoạch hình ảnh tự động và điều phối storyboard → Blender (nhánh `m5-autonomous-visual-planning`)
- **Planner tất định** (`planner/`, thuần Python, không LLM khi chạy): beat → ý đồ hình ảnh → asset → template → shot/camera → timing → storyboard thực thi được. Cùng đầu vào thì ra cùng kế hoạch, giống từng byte.
- **Hợp đồng mới:**
  - `schemas/narrative_beats.schema.json` (`script/visual_beats.json`) và `schemas/visual_plan.schema.json` (`storyboard/visual_plan.json`).
  - `config/visual_vocabulary.json`: khái niệm khu đất, công trình, thành phần; `where`, `supported`, `ambiguous_if_multiple`, `ghost_roles`.
  - `config/visual_planning.json`: camera theo lớp tỷ lệ, luật timing, ngân sách chuyển động.
- **9 ý đồ hình ảnh** với chiến lược theo thứ tự ưu tiên (13 chiến lược ghép từ template có sẵn). Từ khóa trong lời thoại chỉ dùng để cảnh báo khi lệch với ý đồ khai báo, không bao giờ tự sửa ý đồ.
- **Chọn asset:** REUSE_EXISTING / ADAPT_EXISTING_ASSET (adapter cho mái M2) / GENERATE_FROM_SUPPORTED_FAMILY (spec ILLUSTRATIVE ghi trong dự án) / NEW_ASSET_REQUIRED (kèm nhiệm vụ sinh) / BLOCKED_MISSING_EVIDENCE. Mỗi lựa chọn có lời giải thích; catalog chỉ đọc.
- **Ánh xạ thành phần ngữ nghĩa** theo role/group, với ID ổn định. Thiếu hoặc mơ hồ đều là lỗi, được kiểm tra trước khi chọn chiến lược.
- **Camera:** 6 chế độ → preset có sẵn; COMPONENT_CLOSEUP (`camera_focus`, `camera_safe_band`); nhóm liên tục camera (`build_variants`, cắt match/cứng); kiểm tra hiển thị offline.
- **Timing:** PROVISIONAL (ước lượng, có ghi nhãn) hoặc AUDIO_LOCKED (`script/timing.json` đã khóa). Thời lượng tối thiểu lấy từ motion planner thật; thiếu thời gian thì chọn chiến lược nhẹ hơn hoặc báo `TIMING_CONFLICT`, không bao giờ cắt ngắn.
- **Báo cáo coverage** `qa/VISUAL_COVERAGE.md` + `visual_coverage.json` (7 trạng thái).
- **CLI:** `plan-visuals` (exit 4 khi không thực thi được), `validate-plan` (kiểm tra độc lập + G0), `build-shots`.
- **Engine (tùy chọn, tương thích ngược):**
  - builder `none` (khu đất trống);
  - `build_variants`, `camera_focus`, `camera_safe_band`;
  - `highlight.ghost` cho HOLD (phần che chuyển trong suốt);
  - QA Blender: camera theo nhóm liên tục, và kiểm tra mới **`highlight_targets_visible`** (bắn tia đo phần bị che).
- **Cache:** `states_geometry`/`assets` chỉ băm các variant mà shot dựng. Đổi asset cầu đá chỉ làm cũ 4/13 shot.
- **Pilot** `projects/bridge-story-m5` "Three Ways to Span a Gap": 8 beat → 13 shot, 72.375 s, không lời, INTERNAL ONLY, 5 claim SOURCE_VERIFIED. QA Blender 163/163, media QA PASS, smoke test 2 shot.
- **Fixture tổng quát hóa** `projects/roof-plan-m5` (SYNTHETIC): mái nhà qua adapter, layout ROW, QA Blender 52/52.
- **Sửa lỗi tìm ra khi xem hình:**
  - dầm dọc bị ván che (chỉ 14 % nhìn thấy) → ghost, 82 %; lỗi này cũng có ở pilot M4 SC_001 và đã sửa luôn;
  - ảnh tĩnh của shot lắp ráp toàn khu đất trống → marker `incoming_end`;
  - compiler giữ `audio_timing_locked` chỉ khi kế hoạch là AUDIO_LOCKED.
- **Tài liệu** `docs/m5/` (kiến trúc, giao thức lập kế hoạch, chọn asset, báo cáo QA + hiệu năng). Cập nhật AGENTS, DECISIONS, CACHE_DEPENDENCIES, ANIMATION_LIBRARY.
- **Test:** `tests/test_m5_planner.py` (34), `tests/test_blender_m5.py` (2). Hồi quy: QA Blender roof-evolution 64/64, suffolk-roofs 71/71 (gate không đổi), bridge-structure-evolution 92/92.

## 0.4.0 — 2026-10-27 — M4: dựng hình kiến trúc thủ tục và thư viện asset (nhánh `m4-architectural-modeling`)
- **Hệ thành phần ngữ nghĩa** (`engine/arch/semantic.py`):
  - Mỗi thành phần có ID ổn định, loại (30 `SEMANTIC_TYPES`), vật liệu, nhóm, variant sở hữu, transform, mesh cục bộ, layer, hướng bung, vai trò animation, bevel, evidence.
  - Có bbox và chữ ký mesh để dùng chung mesh và kiểm tra tái lập.
- **Thư viện hình học** (`engine/arch/primitives.py`, `library.py`, thuần Python): box, thanh, cung vành khăn (voussoir), lăng trụ đa giác, trụ tròn; lặp có khe mạch, dầm, cột, giằng chéo X, vòng vòm và keystone, outline spandrel, mũi cản nước, giàn song song Pratt/Warren, bản nút.
- **Spec kiến trúc** (`schemas/architecture_asset.schema.json`, `engine/arch/assets.py`):
  - Registry họ/biến thể với khoảng tham số, kiểm tra tương thích hình học và thông báo lỗi dễ đọc.
  - Ba mức độ chính xác: ILLUSTRATIVE / REFERENCE_BASED / HISTORICALLY_VERIFIED (mức cao hơn phải có bằng chứng).
- **Ba họ cầu và khu đất** (`engine/arch/families/`): timber_beam, stone_arch (3 hoặc 5 vòm), steel_truss Pratt/Warren dùng chung khung; site river_crossing. Tổng cộng 6 spec trong `asset_library/architecture/`.
- **Tích hợp engine M2/M3 (không viết engine mới):**
  - Builder `architecture_asset` (dùng cho cả base và variant), mesh dùng chung, bevel không phá hủy, collection theo nhóm.
  - `structure_from` tổng quát: asset kế thừa mọi phần không mang vai trò REPLACE.
  - SIDE_BY_SIDE `layout: "STACK"` với nhãn theo hàng.
  - Camera orthographic tự lùi ra khi mép dưới khung nằm thấp hơn mặt đất.
  - Preset camera BRIDGE_THREE_QUARTER, ELEVATION, TOP, BRIDGE_STACK.
- **Vật liệu dùng chung** `asset_library/materials/stylized_materials.json` (13 vật liệu thủ tục, không texture); `add_units` có thêm tham số trục cho hàng đá.
- **QA và gate G4-A…E:**
  - Kiểm tra offline (`engine/arch/checks.py`).
  - Kiểm tra trong Blender (`engine/arch/asset_scene.py`): nối liền và độ xuyên sâu bằng BVH, dựng hai lần, gắn tag ngữ nghĩa.
  - Preview đa góc (ba phần tư, mặt đứng, mặt bằng, bung).
  - Lệnh CLI: `asset-check`, `asset-render`, `asset-catalog`. Bộ nhớ đo bằng `/usr/bin/time -l`.
- **Catalog** `asset_library/catalog/catalog.json` + `CATALOG.md`: metadata, nguồn gốc, vật liệu, preview, kết quả kiểm tra.
- **Pilot** `projects/bridge-structure-evolution` (29.5 s, không lời dẫn, sinh bằng `tools/make_bridge_pilot.py`): QA Blender 86/86, media QA PASS.
- **Cache render** khóa v3: đệ quy `engine/**` và nhóm phụ thuộc `assets` (spec được tham chiếu + thư viện vật liệu).
- **Test:** 138 (thêm `tests/test_m4_arch.py` 26 test, `tests/test_blender_m4.py` 5 test, gồm phép thử ngược cho BVH). QA Blender roof-evolution 63/63, suffolk-roofs 70/70; trạng thái xuất bản của suffolk không đổi.

## 0.3.5 — 2026-10-27 — M3.5: duyệt biên tập, quyền TTS, hoàn thiện hình ảnh (nhánh `m3.5-editorial-polish`)
- **Audit license** (`docs/licensing/TTS_LICENSE_AUDIT.md`):
  - Model card OmniVoice hiện ghi trọng số là **CC-BY-NC** (do dữ liệu Emilia), và trọng số này trùng từng byte với revision đã cài → OmniVoice **NOT CLEARED** cho xuất bản thương mại, chỉ dùng cho preview nội bộ.
  - Đã so sánh 7 phương án xuất bản (Kokoro, Piper, ElevenLabs, Azure, Google, Polly, OpenAI) và phương án giọng người thật. Không đăng ký hay mua dịch vụ nào.
- **Workflow TTS độc lập provider:**
  - Interface `NarrationAdapter` gồm adapter OmniVoice và adapter thu âm người thật; registry `config/tts_providers.json` có hạng quyền; `narrate --purpose publication` từ chối provider chưa được cấp quyền.
  - Khóa cache audio v2 gồm: model, voice id, chữ đọc thực tế và hạng quyền.
  - 15 take M3 được nhận lại (đổi khóa), không sinh lại; audio beat trùng từng byte.
- **Gói duyệt biên tập** (`projects/suffolk-roofs/review/EDITORIAL_APPROVAL_PACKAGE.md`): 7 claim đều đã đối chiếu lại với PDF (cùng sha256 với M3) và với trang web theo đúng URL đã cho; có đề xuất cho từng claim và danh sách ký duyệt. **Không tự duyệt claim nào.** Validator yêu cầu hồ sơ duyệt (`editorial_approval`) gắn với narration revision.
- **Lời dẫn `m3.5-r1`:** 4 câu sửa vì độ chính xác (thêm "originally"; 45–60°; "Slate is different."; câu kết bỏ suy diễn ngược) + sửa phát âm B1.s0. 9/14 take giữ nguyên. Tổng thời lượng 73.0 → 75.542 s.
- **Trình tự tuyến tính:** SC_005 không còn "thay ngói bằng slate trên cùng một nhà", mà là hai công trình đặt cạnh nhau; SC_006 cắt cứng; đã xóa transition ngói → slate.
- **Phát âm "Babergh":** override chỉ cho TTS (`[B EY1 B AH0]`), chữ viết giữ nguyên; có clip bằng chứng và danh sách nghe; trạng thái `PENDING_LISTENING_REVIEW`. Alias ASR chỉ dùng để tính WER.
- **Phụ đề:**
  - 21 cue theo cụm từ. Ranh giới lấy từ timestamp theo từ của Whisper rồi đặt vào điểm năng lượng thấp nhất của audio thật. Chữ lấy từ kịch bản.
  - Dòng dài nhất 41 ký tự, 1–2 dòng mỗi cue. Báo cáo `qa/SUBTITLE_QA.md`.
- **Hình ảnh:**
  - Hoa văn viên ngói/slate (shader, căn theo gân hàng), nhãn chữ dưới mô hình trong SIDE_BY_SIDE.
  - Sửa tường hồi và đỉnh tường xuyên qua mái slate mỏng (có từ M3).
  - Ảnh tĩnh ở 960×540 và 1920×1080 (`production_test`, chỉ ảnh tĩnh); ảnh trước/sau.
- **Cache render theo nhóm phụ thuộc** (`tools/render_cache.py`, `cache-report`): sửa chữ, claim hay timeline không làm render lại.
- **Gate:** `pipeline/gates.py` với TECHNICALLY_VALIDATED / EDITORIAL_REVIEW_PENDING / TTS_RIGHTS_PENDING / PUBLICATION_READY; gate cuối kiểm tra nguồn gốc audio và xác nhận phát âm; G4/G5 phát hiện báo cáo cũ. MP4 có audio chưa được cấp quyền mang tên `*_INTERNAL.mp4` kèm metadata.
- **QA và độ tin cậy:**
  - Kiểm tra Blender mới: `covering_hides_structure`, `labels_in_band` (cả kiểm tra bị che khuất). Phép thử ngược cho thấy cả hai bắt được lỗi cũ.
  - Sửa: `check-blender` từng in ra báo cáo **cũ** khi Blender bị lỗi; QA layout SIDE_BY_SIDE từng đọc `matrix_world` cũ của object bị ẩn; `audio_probe` từng ném `KeyError` với WAV rỗng.
- **Test:** 107 (thêm 30 ở `tests/test_m35.py`). QA Blender: suffolk 70/70, roof-evolution 63/63.

## 0.3.0 — 2026-10-27 — M3: pipeline phim có lời dẫn + OmniVoice cục bộ (nhánh `m3-narrative-pipeline`)
- **OmniVoice:** đã khảo sát project người dùng (không sửa gì); khởi động demo Gradio **chỉ ở localhost** (`--ip 127.0.0.1 --no-asr`, tắt analytics, HF offline); hợp đồng API xác nhận qua `/gradio_api/info`. Adapter stdlib `integrations/tts/omnivoice.py` ghép tham số theo nhãn, có timeout/retry, lỗi rõ ràng, kiểm tra audio (`integrations/audio_probe.py`).
- **License:** code + trọng số Apache-2.0, nhưng tokenizer Higgs Audio v2 đi kèm theo Boson Higgs Audio 2 Community License → `LICENSE_REVIEW_REQUIRED`; chặn xuất bản. Giọng = voice design → giọng mẫu tổng hợp → clone (không giọng người thật).
- **Pipeline** (`pipeline/`): `narration` (sinh theo câu, cache theo nội dung, sinh lại khi lỗi, audio beat ghép ở mức mẫu), `asr_check` (Whisper offline, WER), `beat_scheduler` (narration-first, frame chính xác, mốc neo, khóa timing), `assemble` (track, loudnorm 2 lượt, ghép, SRT cấp câu, QA), `storyboard_report`.
- **Engine:** `covering.style` (thatch / plain_tile / slate + ngói nóc + vật liệu có texture thủ tục), `structure_from`, card 2D `engine/diagram.py` (font tích hợp), chốt chặn "không animate phần đang bị ẩn".
- **Validator/CLI:** trạng thái claim PROVISIONAL / SOURCE_VERIFIED / EDITORIALLY_APPROVED / REJECTED (bắt buộc locator + excerpt), kiểm tra narration/license/beat/khóa timing, card; lệnh `tts-check`, `narrate`, `asr-check`, `schedule`, `smoke`, `assemble`, `gates`. Schema `narration`, `sources` v2.
- **Pilot `suffolk-roofs`:** 73.0 s; QA Blender 66/66; 77 unit test; smoke + bản đầy đủ: lệch A/V 0 ms, −16.5 LUFS; gate → PREVIEW NỘI BỘ, chưa sẵn sàng xuất bản.
- **MCP:** gỡ server `blender` ở scope local (đã sao lưu `~/.claude.json`); scope project (2.2.4, safe mode, không telemetry) đang có hiệu lực; tool + việc chặn của safe mode đã kiểm chứng.
- **Lỗi đã sửa trong M3:** đọc vội (sinh lại), mất bản ghi cache (lưu theo từng đoạn), intro làm hiện mái tranh bị ẩn ở SIDE_BY_SIDE, ngói nóc ra ngoài khung khi exploded, mô tả SC_002 sai so với hình, ngắt dòng phụ đề.

## 0.2.5 — 2026-10-27 — M2.5: ổn định hóa, QA qua MCP, sẵn sàng cho M3
- **Git:** giữ nguyên commit `init` của người dùng; baseline M2 được commit (`75487d3`, tag `m2-baseline`); `.gitignore` bổ sung media QA, `.blend@`, file tạm, `.env*`, `.claude/settings.local.json`.
- **MCP:** gọi thật `get_addon_status`/`get_scene_info`/`execute_blender_code`/`look` qua stdio (21/21 lệnh trước khi sửa, kèm lượt kiểm tra lại sau khi sửa) trên một phiên bản Blender riêng mở bản sao của các scene. Đã xác định vì sao addon không lắng nghe (Blender mở trước khi addon được cài) và phát hiện cấu hình scope local ghi đè safe mode (chỉ ghi lại, không tự sửa).
- **Sửa #1 — rafters xuyên tường:** cắt đầu dưới rafters 1 mm trên đỉnh tường (`box_object(clip_below_z=…)`). Kiểm tra mới `structure_clear_of_shared_at_rest` FAIL trên geometry M2, PASS sau khi sửa.
- **Sửa #2 — highlight:** chỉ còn tự phát sáng bằng màu của chính phần đó (bỏ pha màu nhấn); mái A giữ màu graphite.
- **Sửa #3 — ánh sáng phẳng:** chọn L3 sau khi so 4 biến thể ở 960×540: nắng chính từ trước-trái và cao (bóng ngắn, không chạm model bên cạnh), fill 0.3, world 0.4, AgX `Medium High Contrast`, ray tracing Eevee, smooth shading + weighted normals cho cạnh vát (edge highlight). Mọi thông số nằm trong `config/visual_style.json`.
- **Sửa #4 — nhiễu dithering:** twin BLENDED chỉ hiển thị khi đang mờ dần (`motion.split_fades`). Frame tĩnh và điểm cắt không đổi; đã so sánh với dithered 64/128 mẫu và BLENDED cho mọi object.
- **Sửa #5 — cắt cứng SC_004 → SC_005:** `SIDE_BY_SIDE.intro` (camera lùi ra, model đứng yên). Đã so sánh với dissolve bằng FFmpeg. SC_001 2.0 s, SC_005 4.5 s, tổng vẫn 20.0 s.
- **Sửa #6 — manifest:** lệnh `python3 tools/cli.py manifest [--check]` tạo lại từ `git ls-files`.
- **Sửa #7 — frame v0.1:** 144 PNG được nén không mất dữ liệu (đã kiểm checksum) vào `qa/baseline_v0_1/v0_1_preview_frames.tar.gz` rồi mới xóa bản rời; file `.blend` của v0.1 được chuyển vào cùng thư mục.
- **QA:** 58 kiểm tra Blender (thêm structure/twins/intro; chữ ký tái lập chỉ băm những gì được render); media QA đo SSIM tại điểm cắt (`cut_from_previous`); 49 unit test. CLI chạy Blender dưới `caffeinate -i` (máy ngủ khi idle từng làm một frame đứng 15 phút).
- **Output review riêng:** `--preset review` ghi vào `output/stills_review/`, `output/shots_review/`, `*_review.mp4`; preview 640×360 giữ nguyên tên cũ.
- **M3:** kế hoạch + brief nghiên cứu + storyboard nháp trong `docs/m3/` (chưa sản xuất).

## 0.2.0 — 2026-10-26 — M2: Engine biến đổi trực quan tái sử dụng v1
- Template mới: `REPLACE_PARTS`, `EXPLODED_VIEW`, `SIDE_BY_SIDE`, `HOLD` (+ highlight), điều khiển hoàn toàn bằng `storyboard.json` → `animation`.
- Planning bằng Python thuần (`engine/motion.py`, `templates.py`, `spec.py`, `framing.py`), nên validator kiểm tra được timing, ownership và option ngay ở G0. Keyframe được ghi với interpolation tường minh (`engine/animate.py`, hỗ trợ cả slotted actions của 5.x).
- Builder có metadata: mái gable gồm tấm phủ, rafters, ridge beam, tường hồi; base có thêm ceiling joists. `states.json` v2 có quyền sở hữu tường minh (v1 vẫn tương thích).
- Mỗi shot là một scene độc lập (`engine/shot_builder.py`) với camera ortho khóa, fit theo hình học. Ánh sáng chuyển sang sun (không phụ thuộc vị trí); mặt đất liền khối.
- CLI: `still` (key stills), `preview` (render theo shot có cache + MP4 theo shot + MP4 đầy đủ + media QA + contact sheet / dải tiến trình), `shot`, `check-blender`. Gọi Blender với `--python-exit-code 1`.
- QA: `engine/qa_checks.py` (50 kiểm tra), 38 test offline mới + 1 test tích hợp Blender (tổng 43 cùng 4 test cũ).
- Pilot roof-evolution: 20 s, 5 shot. Đã sửa: dải nền ở mép trên (clip_end), highlight làm đổi tông màu, bóng đổ lên model bên cạnh, cấu kiện đặc bị khung cắt (2 trường hợp), móng nổi 5 cm.
- Loại bỏ: cơ chế thu nhỏ còn 1% của v0.1 (`engine/transform.py` được giữ lại làm tham khảo, đánh dấu DEPRECATED, không còn được import).

## 0.1.1 — 2026-10-26
- Pilot `roof-evolution` render lần đầu trên Mac thật: macOS 26.6.2, Apple M4 Pro 24 GB, Blender 5.2.2 LTS, FFmpeg 9.0.1, Python 3.14.6.
- Fix framing (`engine/scene.py`): đỉnh mái B (48°, ~5.2 m) bị cắt 19% ở mép trên, móng hụt 3% ở mép dưới. Camera giờ nhắm z=2.1 (đèn vẫn nhắm z=1.6), `ortho_scale` 10.1 → 14.0; đo bằng `world_to_camera_view` trên geometry thật: cả A và B có lề dọc ~6%.
- Preview 6 s / 144 frame / 640×360 render trong ~35 s; MP4 h264 yuv420p, không black frame.
- Cài MCP for Blender 2.2.4 (`ahujasid/mcp-for-blender`, commit `febcd90`, MIT) sau khi review mã: wheel PyPI khớp source, addon SHA-256 `8e193a24…7083`. Addon → `~/Library/Application Support/Blender/5.2/scripts/addons/blender_mcp.py` (đã enable). Server đăng ký ở `.mcp.json` (scope project), ghim version, `DISABLE_TELEMETRY=true`, `BLENDER_MCP_SAFE_MODE=1`, localhost:9876. Pipeline CLI dùng `--factory-startup` nên không nạp addon.

## 0.1 — 2026-10-22
- Chốt narrative-first architecture 3D pipeline.
- Tạo chính sách AI coding, workflow, JSON schemas, validation, Mac CLI, sample roof transitions.
- Thêm unit tests và tài liệu đầu vào cho Codex/Claude.
- MVP chưa được render bằng Blender thực tế trong môi trường đóng gói.
