# Bản internal review đầy đủ v1 (2026-11-11)

**Đầu vào:**
- Chủ kênh: "review lại, tôi muốn sản xuất bản internal review luôn, không làm từng đoạn nhỏ nữa".
- Review toàn phim của Codex trên mốc `fc7901a`:
  - đoạn mở đầu đủ tốt;
  - kiểm Blender 44 shot được 560/569, trong đó 6 lỗi hình (B13, B27, B28, B30, B31, B38) và 3 lỗi cần điều tra ở pipeline;
  - QA phim dài báo thiếu tiêu đề chương C2–C8 và một chuỗi 7 shot cùng loại.

**Phạm vi:** giữ nguyên kịch bản c-r2, lời dẫn (`script/narration.json` không đổi byte nào) và mọi giả định đã chốt. Chỉ sửa cục bộ các hình chưa rõ, rồi render theo chương và giao một MP4 720p đầy đủ.

Đây không phải bản FINAL. Bản này không ghi lại việc duyệt claim, giọng, phát âm hay xuất bản nào.

## Góp ý → đã làm

| Góp ý | Đã làm |
|---|---|
| **B27:** mặt cầu che đường ống ở lần làm sáng đầu (2% silhouette). Phải giữ phân biệt Schoonschip với thiết kế minh họa. | Mặt cầu mờ đi ngay ở chữ đầu tiên ("Wastewater"), trước lần sáng đầu ở "black water". Thêm ghi chú "Our illustrative design" trong hai câu đầu, là hai câu nói về Schoonschip. |
| **B30:** neo chỉ chiếm 0,01% khung; nước mờ và bóng nhà làm cảnh giống nền đất. | Câu 1 giữ toàn cảnh đê với sóng khái niệm. Tới "Below the surface", camera hạ xuống góc ngang mặt nước, đứng ngoài khối nước của site, và cận một dây neo phía đông cùng neo của nó. Dây và neo sáng cùng lúc (riêng neo chỉ khoảng 0,05% khung). Thêm nhãn "Anchor". |
| **B31:** cáp và ống mảnh, 0,08% khung; nước như B30. | Mở bằng toàn quận nhìn từ trên với nước đầy. Tới "cables", nước trong dần và camera xuống góc ngang, cận chỗ ba tuyến rời phao giữa hàng trước: ống đứng xuống đáy rồi chạy ra khỏi khung về phía bờ. Các tuyến sáng từ "supply". |
| **B13:** chốt bản lề gần như không đọc được (nhìn từ cạnh, chốt hiện ra như một chấm). | Thêm khung thứ ba ở "whatever connects them": nhìn xiên qua khe từ trên (phương vị −70°, cao 20°), cận cầu đi bộ. Thấy được hai mép sàn chênh nhau, khe nước và hai chốt. Nhãn "Decks ≈ 0.66 m apart" tắt trước khi camera đi. |
| **B28:** bến, tuyến, ống và cầu chỉ chiếm 0,04–0,16% khung; nhãn lớn hơn vật. | Mở bằng khung nhìn dọc tuyến thoát hiểm của cầu thứ nhất, từ kè lên (phương vị −90°, cao 50°). Thứ tự sáng: tuyến ("fire"), ống hạ tầng ("sewage"), cầu ("roads"). Tới "alternatives", camera kéo ra toàn quận và nhà mờ đi. Ở "and our city connects", mọi thứ nối quận với đất liền (cầu, tuyến, ống) sáng cùng lúc. Nhãn có đường dẫn đổi thành ghi chú "Emergency route to land": tuyến chạy suốt khung nên không có chỗ đặt nhãn. |
| **B38:** lối đi và ống chỉ chiếm 0,20–0,24% khung khi kéo ra. | Lối đi sáng khi camera còn cận phao (cao 50°). Khi kéo ra toàn quận, nhà mờ đi và mọi thứ "we added" (lối đi, cầu, tuyến, ống, đê) sáng như một mạng. |
| **B22/B24** (nhắc từ L6: mép mặt nước, tương phản đáy, bóng). | Cùng cách với B30/B31: mở bằng nước đầy ở góc cũ. Khi nước trong dần, camera xuống góc ngang mặt nước, đứng ngoài khối nước, và cận phao 2 cùng cọc (B22) hoặc dây neo (B24) của nó. Mặt nước còn một đường thẳng, nước thành một khối màu, đáy là một dải, bóng nhà trên đáy không còn. |
| **SC_004/SC_038** `plan_matches_evaluated_keys`: lệch ortho 0,00011–0,00016 ở giá trị khoảng 933–1098. | **Nguyên nhân:** Blender lưu và nội suy khóa F-curve bằng float32. Ở 933–1098 m, sai số là 1–3 ulp (một ulp bằng 6,1·10⁻⁵ hoặc 1,2·10⁻⁴). **Sửa:** dung sai = max(1·10⁻⁴; 4 ulp float32 của giá trị) (`motion.Plan.key_tolerance`). Dưới khoảng 210 m ngưỡng không đổi. Test dùng đúng số đo và vẫn bắt một khóa sai 0,1%. |
| **SC_042** `camera_identical_across_single_model_shots`. | **Nguyên nhân:** SC_001 và SC_042 mở cùng một khung toàn quận, nhưng SC_001 đứng cách 400 m (`clearance`), còn SC_042 dùng mặc định. Khóa nhóm chưa tính `clearance`. **Sửa:** khóa nhóm tính thêm `clearance`. Không đổi camera nào. |
| **`chapter_openings`:** C2–C8 thiếu tiêu đề có số. | `story.py` thêm ghi chú "N · tên chương" (góc trên trái, trong câu đầu) cho beat đầu của chương 2–8, lấy từ `CHAPTERS`. Không thêm khoảng dừng, không đổi lời dẫn. |
| **`visual_variety`:** chuỗi 7 shot cùng loại. | Không đổi nhãn, không chèn card. Xem phần "Cần chủ kênh quyết". |

**Engine:**
- **Giới hạn `clearance`:** nâng từ 500 m lên 2 km, để khung ngang ngoài khơi đứng ngoài khối nước của site biển mở (1,7 × 1,5 km). Có test.
- **Hai sửa ở `engine/qa_checks.py`:** chỉ đổi cách so sánh, không nới ngưỡng hiển thị nào.

## Kiểm tra trước render
- `plan-visuals`: 44/44 beat thực thi được; `validate-plan` PASS; `build-shots` PASS.
- `check-blender --preset internal_720p`: **585/585 PASS** (trước: 560/569).
- `chapters --preset internal_720p`:
  - 16/17 kiểm tra đạt (thêm `chapter_openings`, `annotations_consistent`);
  - còn `visual_variety` FAIL (xem dưới).
- Test: 473 PASS (trừ `test_blender_m6` gọi Blender).
- Lời dẫn: sha256 `af99cab7…` không đổi.
- Trước khi chốt, đã xem ảnh tĩnh của mọi shot đã sửa ở các mốc làm sáng.

## Render và ghép (2026-11-11 21:09 → 2026-11-12 00:04)
- Render theo chương ở `internal_720p`, mỗi lúc một Blender, C1 → C8. Cả 44 shot render mới (không dùng cache cũ), tổng khoảng 2 giờ 45 phút.

| Chương | Shot | Frame | Thời gian render | Lỗi media |
|---|---|---|---|---|
| C1 | SC_001–004 | 1539 | 19 phút | 0 |
| C2 | SC_005–011 | 3282 | 33 phút | 0 |
| C3 | SC_012–016 | 3185 | 21 phút | 0 |
| C4 | SC_017–021 | 2142 | 17 phút | 0 |
| C5 | SC_022–024 | 1297 | 11 phút | 0 |
| C6 | SC_025–028 | 1702 | 16 phút | 0 |
| C7 | SC_029–037 | 3683 | 36 phút | 0 |
| C8 | SC_038–044 | 1990 | 11 phút | 0 |

**Tệp giao** (không commit, nằm trong `output/`):

| Tệp | Nội dung |
|---|---|
| `output/pilot/floating_city_design_challenge_FULL_INTERNAL_REVIEW_720p.mp4` + `.en.srt` | Bản đầy đủ có SFX tổng hợp |
| `output/pilot/floating_city_design_challenge_FULL_INTERNAL_REVIEW_720p_no_sfx.mp4` + `.en.srt` | Bản đầy đủ không SFX |
| `output/floating_city_design_challenge_INTERNAL_REVIEW_720p.mp4` + `.en.srt` | Bản ghép chuẩn của pipeline (`final-assemble`, chỉ lời dẫn). Cùng hình và cùng lời với bản không SFX |

- Cả ba bản đều dài 784,2 s (13:04,2), 18 820 frame, có INTERNAL_REVIEW trong tên file. Hai bản FULL còn ghi "not for publication" trong metadata.
- **SFX:** chỉ có 2 tiếng tổng hợp, đều có sẵn từ L5: đặt tầng ở 2:26,5 (B09) và đặt tầng nặng ở 2:44,4 (B10). Không dùng kho `sfx/`. Vì vậy hai bản chỉ khác nhau ở hai chỗ này.

**Công cụ:** `tools/asr_whisper.py`: Whisper chỉ nghe 30 s mỗi lần. Shot dài hơn (SC_003, SC_013, SC_016) cần chế độ nhiều cửa sổ nối tiếp, mà transformers chỉ cho bật khi có mốc thời gian. Không đổi gì với clip ≤ 30 s, nên kết quả ASR từng câu đã lưu vẫn như cũ.

## QA bản ghép
| Kiểm tra | Kết quả |
|---|---|
| Media (bản ghép) | 18 820 frame; 0 lỗi giải mã; 0 đoạn đen; 7 điểm nối giữa chương qua SSIM |
| Âm lượng | Không SFX −16,4 LUFS, đỉnh thật −1,2 dBTP. Có SFX −16,4 LUFS, đỉnh thật −1,0 dBTP. Không sample nào bị cắt |
| Phụ đề | 181 cue cho 126 câu; dòng dài nhất 42 ký tự. Một cảnh báo: B09.s2 17,1 ký tự/s (ngưỡng khuyến nghị 17,0) |
| Whisper từng shot (có SFX so với không SFX) | 44/44 shot không kém đi khi thêm SFX. WER trung bình 0,4%, cao nhất 4,1% ở SC_016 (Whisper nghe "Schoonschip" thành "scoonskip", "quay" thành "key"; giống hệt nhau ở cả hai bản). Đây là kiểm tra kỹ thuật, không thay việc nghe |
| `excerpt_FULL` | PASS (`qa/excerpt_FULL.json`) |
| `gates --preset internal_720p` | G0–G5 và GV PASS. **GL FAIL** (`visual_variety`). G6 BLOCKED. Kết luận: INTERNAL PREVIEW, NOT PUBLICATION-READY |

**Không gọi toàn phim là PASS:** QA phim dài còn một mục FAIL (`visual_variety`). Mục này chờ chủ kênh quyết.

## Xem hình trong MP4
- **Cách xem:**
  - 5 frame mỗi shot, đủ hai phía của mọi điểm nối;
  - 46 frame 1280×720 ở các mốc làm sáng, mốc đổi khung và tiêu đề chương.
  - Chi tiết: `qa/EDITORIAL_REVIEW_TIMECODED.md`.
- **Đạt:**
  - B13: cận bản lề;
  - B14: từng bộ phận sáng;
  - B22/B24: cọc, dây neo, neo ở khung ngang mặt nước;
  - B27: ống lộ trước khi được nhắc;
  - B28: nhìn dọc tuyến;
  - B30/B31: dây, neo, ống ở khung ngang. Không còn cảm giác quận đứng trên nền đất;
  - tiêu đề chương 2–8.
- **Còn tồn tại** (chưa sửa; mốc thời gian trong tệp trên):
  1. B13 3:45–3:53: khung "Decks ≈ 0.66 m apart" thật ra kéo ra xa, nên chênh lệch chỉ khoảng 1 px (khung này có từ trước).
  2. B33/B34 10:07–10:40: nước mờ hẳn, phao như treo trên nền xám. Cùng kiểu lỗi B30/B31.
  3. B30/B31: khoảng 1–2 s lúc camera hạ xuống, lưới bóng trên đáy lộ ra.
  4. Nước ở khung ngang có màu rất nhạt, ngoài khơi gần trùng màu nền.
  5. B12/B17: lộ một góc nền ngoài mép mặt nước.
  6. B38: mạng nối nhạt khi kéo ra toàn quận.
  7. Phụ đề B09.s2 nhanh 17,1 ký tự/s.

## Cần chủ kênh quyết
1. **`visual_variety`:**
   - Chuỗi B08–B14 (7 shot `3D_SEQUENCE`, 2:03–4:34) và B27–B31 (5 shot, 8:24–9:41) vượt ngưỡng 4.
   - Mỗi shot trong hai chuỗi đổi góc và cỡ khung rõ. B08–B11 là đoạn cơ chế chủ kênh đã khen ở L5.
   - Hai cách:
     - **(a)** ghi ngoại lệ trong `project.json` → `variety_exception` (max_run, chapter, decided_by, decided_on, basis);
     - **(b)** tách chuỗi bằng một card. Cách này phải đổi kịch bản hình và render lại.
   - Agent không tự ghi ngoại lệ.
2. **Có sửa vòng sau không** (mục 1–6 ở trên; mỗi mục kèm số shot phải render lại trong tệp timecode)? Theo agent, nên ưu tiên mục 2 (B33/B34) và mục 1 (B13).
3. **SFX:** nghe so sánh bản có SFX và không SFX ở 2:26 và 2:44. Agent không nghe được, nên không có nhận xét chủ quan.

## Đóng gói source (commit này)
- **TTS:**
  - đúng 126 take mà `audio/narration_manifest.json` đang dùng (33,5 MB); sha256 của từng file khớp manifest;
  - 40 take cũ còn trong `audio/segments/` (ghi trong manifest nhưng không thuộc câu hiện hành), cùng một file ngoài manifest, không được commit.
- **Không commit:**
  - MP4, WAV nháp, frame render;
  - `qa/gates.json`;
  - `qa/codex_*`;
  - hai file `sfx/waves*.mp3` của chủ kênh;
  - thay đổi `.gitignore` của chủ kênh.
