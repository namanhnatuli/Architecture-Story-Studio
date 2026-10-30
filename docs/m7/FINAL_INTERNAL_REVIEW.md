# M7: bản review nội bộ cuối, giọng `am_michael`, 1080p

- Ngày: 2026-10-30. Nhánh `m7-final-internal-review`, tách từ `m7-first-full-documentary`. Bản trước dùng `bm_george` được giữ làm mốc tại git tag `m7-review-bm_george`, file cũ ở `output/baseline_bm_george_m7r1/`.
- **Quyết định của chủ kênh, ghi lại nguyên văn và không mở rộng thêm:**
  1. duyệt 41 claim được lời dẫn dùng;
  2. đổi giọng đọc toàn phim sang `am_michael`;
  3. bỏ dòng "Narration: AI-generated voice" khỏi card B35.

  Không có quyết định nào trong số này là cấp quyền xuất bản.

## 1. Giọng mới
| Mục | Giá trị |
|---|---|
| Provider/model | Kokoro-82M `hexgrad/Kokoro-82M` @ `f3ff3571791e…`, `kokoro-v1_0.pth` SHA256 `496dba11…` (khớp model card) |
| Giọng | `am_michael`, SHA256 `9a443b79…` (khớp VOICES.md), G2P Anh–Mỹ `lang_code='a'`, speed 1.0, seed 0 |
| Giấy phép | Apache-2.0 (repo); không có điều khoản ghi công cho giọng Anh–Mỹ; các điểm mở về dữ liệu huấn luyện như §5 của audit |
| Trạng thái quyền | Đã audit để đọc lời dẫn. **Licence `LICENSE_REVIEW_REQUIRED`**: clearance ngày 2026-10-29 chỉ nêu tên 4 giọng Anh–Anh (`voices_cleared`), còn `am_michael` nằm trong `voices_pending` |
| Mẫu thử trước | 6 câu nhiều thuật ngữ: 136 wpm, chênh mức âm 0,5 dB, WER lớn nhất 0,105, không có lỗi chặn |

## 2. Audio và timing (sinh lại toàn bộ, không chép mốc cũ)
- **Lời dẫn:** 103 câu (102 đoạn audio, vì một câu lặp dùng chung), **593,98 s** giọng đọc, 139,3 wpm. Mức âm trung bình mỗi câu từ −28,4 đến −26,9 dB (độ lệch chuẩn 0,33 dB).
- **ASR:** 102/102 đạt, WER lớn nhất 0,143, trung bình 0,007. Các chỗ lệch là từ đồng âm ("site"/"sight", "chord"/"cord"), "support it" bị nghe thành "supported", và tên riêng.
- **Căn từ (Whisper word timestamps):** 102 câu căn lại. Timing khóa lại: 39 beat, cửa sổ 640,77 s.
- **Phim:** **641,458 s (10,69 phút) = 15.395 frame** ở 24 fps (bản `bm_george` là 646,458 s). Mọi shot đều ở ranh giới frame nguyên.
- **Kế hoạch hình lập lại theo timing mới:** 47 shot, nội dung và ý đồ hình giữ nguyên. Chú thích và phần tử card lại bám theo câu và từ của audio mới.
- **Kiểm tra trên file thật:**
  - 39/39 beat trong master khớp hash với manifest; mọi đoạn là `am_michael`; 0/105 bản ghi `bm_george` được dùng.
  - Whisper nghe hai đoạn cắt từ MP4 cuối (2:50–3:10 và 10:28–10:41) khớp với phụ đề.

## 3. Card B35
- Đã bỏ dòng "Narration: AI-generated voice (Kokoro-82M, voice bm_george)". Bốn dòng ghi công còn lại (ảnh HAER/LOC, nguồn) và dòng "3D models and diagrams are illustrative…" được giãn lại theo nhóm.
- Ảnh xem trước: `projects/why-bridges-look-different/review/b35/B35_credits_1080p.png`.
- Chuỗi này không còn trên hình nào khác, trong phụ đề hay trong mẫu nào (có test).
- **Nghĩa vụ công bố:** Kokoro không đòi ghi công cho audio. Riêng việc nói rõ lời dẫn do AI tạo, vốn là điều kiện của clearance, vẫn nằm trong `review/YOUTUBE_DESCRIPTION.md` ("voice am_michael").

## 4. Tối ưu render (dùng lại frame tĩnh)
- **Cách làm:** hai frame được coi là giống nhau khi mọi kênh mà motion plan key (vị trí, xoay, tỉ lệ, độ trong suốt, highlight, ẩn/hiện, ortho camera) có cùng giá trị. Chỉ áp dụng khi plan là hoạt hình duy nhất trong cảnh; nếu không thì dùng FALLBACK_FULL_BLENDER. Blender chỉ render frame khác frame trước; frame lặp là **hardlink**.
- **Phân loại shot:** STATIC_2D, ANIMATED_2D, STATIC_3D, ANIMATED_3D, HYBRID, FALLBACK_FULL_BLENDER. Bản này có HYBRID 39, STATIC_3D 4, ANIMATED_3D 4.
  - Card có ảnh trôi chậm thì gần như frame nào cũng khác.
  - Push-in là ANIMATED_3D.
- **Kiểm chứng** (`verify-reuse`): render trực tiếp frame bị dùng lại rồi so từng điểm ảnh.

  | Shot | Kết quả |
  |---|---|
  | SC_047 (B35) | trùng khít |
  | SC_016 (tách lớp) | trùng khít |
  | SC_017 (3D có chú thích) | lệch tối đa 1/255 ở ~0,05% điểm ảnh, PSNR 85–88 dB |

  Mức lệch của SC_017 **bằng mức nhiễu nền**: render lại chính frame nguồn cũng lệch y như vậy. Đây là tính không tất định của EEVEE, không phải do dùng lại frame.
- **Làm tiếp khi bị ngắt** (kiểm trên lượt render thật): dừng Blender giữa SC_004 rồi chạy lại chương C1. SC_001–003 CACHED; SC_004 RESUME giữ 86/101 frame, chỉ render 9 frame còn thiếu.

## 5. Render 1080p (preset `internal_1080p`)
| Số đo | Giá trị |
|---|---|
| Frame của phim | 15.395 |
| **Frame Blender render thật** | **5.206** (33,8%), cộng 12 frame giữ lại khi làm tiếp |
| **Frame dùng lại (hardlink)** | **10.177** |
| Thời gian render khi máy thức (log `Saved:`) | 4540 s (≈ 1,26 giờ), 0,873 s cho mỗi frame thật sự render; không có lần ngủ nào |
| Wall-clock C2–C8 + mã hóa + media QA + ghép | 82 phút (21:28 → 22:50); C1 và benchmark thêm khoảng 6 phút |
| Theo chương (wall) | C1 34 s (lần chạy lại), C2 133 s, C3 1274 s, C4 272 s, C5 445 s, C6 287 s, C7 1387 s, C8 863 s; mã hóa cả phim + media QA 218 s; ghép 42 s |
| Bộ nhớ lớn nhất | ≈ 1,0 GB RSS |
| Đĩa | `renders/internal_1080p` 7,7 GB (frame lặp là hardlink, không tốn thêm chỗ); đĩa trống từ 40 GB xuống 32 GB |
| Ước lượng nếu render đủ mọi frame | ≈ 4,3 giờ máy thức (3D 1,55 s/frame, card 0,3 s/frame theo benchmark). Đây là **ước lượng**, không đo |

**Sinh lại và dùng lại:**
- Sinh lại: toàn bộ audio (giọng đổi), căn từ, timing, storyboard, mọi frame 1080p (preset mới, timing mới), MP4 và WAV các chương, master.
- Dùng lại: claim/nguồn (chỉ thêm hồ sơ duyệt), mô hình 3D, ảnh HAER, kịch bản.
- Bên trong mỗi shot: dùng lại 10.177 frame. Frame `preview`/`review` cũ không dùng được, vì timing đổi và preset khác.

## 6. QA cuối
| Hạng mục | Kết quả |
|---|---|
| File | `output/why_bridges_look_different_M7_FINAL_INTERNAL_REVIEW_1080p.mp4` (75,1 MB) + `.en.srt` |
| Video | h264 **1920×1080**, 24 fps, 15.395 frame, 0 lỗi giải mã, 0 đoạn đen, 46/46 điểm cắt đạt |
| Audio | AAC 48 kHz, **−16,4 LUFS**, true peak −1,2 dBTP, A/V lệch ≤ 1 frame |
| Phụ đề | 145 câu cho 103 câu lời dẫn, tối đa 42 ký tự/dòng, tối đa 18,0 ký tự/s, track mov_text |
| QA Blender | 577/577 |
| QA phim dài | PASS (17 kiểm tra; cảnh báo: câu hỏi lặp có chủ ý, chương 2 một loại hình, cache review cũ) |
| Chương | 8 MP4 + SRT + WAV ở `output/chapters_internal_1080p/` |
| Master | `…_narration_master_clean_internal_1080p.wav`, `…_audio_master_internal_1080p.wav` |
| Kiểm tra trên file thật | 9 frame lấy từ MP4 cuối (`qa/final_1080p/final_1080p_grid.png`): đủ 8 chương, push-in giữ NOTE, B35 đã sửa |

**Cổng:**

| Cổng | Kết quả |
|---|---|
| G0, G3, G4, G5, GL, GV | PASS |
| G1 | PENDING: 41/41 claim đã duyệt, `factual_review: verified`; chờ phát âm 16 thuật ngữ |
| G2 | BLOCKED_RIGHTS: licence `am_michael` chờ cấp quyền |
| G6 | BLOCKED |

Kết luận: **INTERNAL PREVIEW — NOT PUBLICATION-READY.**

## 7. Còn chặn việc xuất bản
1. Quyền xuất bản cho `am_michael`: chủ kênh thêm giọng này vào `voices_cleared` và xác nhận cho phim (`owner_confirmation_for_this_film`).
2. Nghe và xác nhận phát âm, theo `review/PRONUNCIATION_REVIEW.md` (đã sinh lại cho `am_michael`).
3. CLM_747: claim không dùng trong phim, vẫn `SOURCE_VERIFIED`. Cổng cuối đòi mọi claim trong registry phải được duyệt; chủ kênh duyệt claim này, hoặc loại nó khỏi registry.
4. Chuyển profile `PUBLICATION_CANDIDATE` + `publication_metadata`, rồi render bằng preset `final`.
