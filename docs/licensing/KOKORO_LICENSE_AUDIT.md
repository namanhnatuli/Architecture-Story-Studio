# Audit license: Kokoro-82M (TTS cục bộ cho tập phim M6)

- Ngày audit: **2026-10-28** (M6, nhánh `m6-narrated-documentary`).
- Người thực hiện: agent (Claude Code). **Chưa có người duyệt.**
- **Đây là đánh giá tuân thủ, không thay cho tư vấn pháp lý.** Agent chỉ ghi lại những gì văn bản công khai và metadata của gói đã cài nói ra. Quyết định dùng để xuất bản thuộc về người chịu trách nhiệm kênh.

## 1. Kết luận
| Mục | Kết luận |
|---|---|
| Kokoro cho **preview nội bộ có lời dẫn** (M6) | Dùng được |
| Kokoro cho **xuất bản thương mại** (YouTube có kiếm tiền) | **ĐÃ CẤP QUYỀN ngày 2026-10-29 bởi chủ kênh (Tran Nam Anh)**, ghi trong `config/tts_providers.json` → `clearance`; hạng quyền `PUBLICATION_CLEARED`. Phạm vi: đúng revision `f3ff3571` và các giọng đã audit, sinh cục bộ, có ghi rõ lời dẫn do AI tạo. Agent chỉ ghi lại quyết định, **không** tự cấp quyền. Trước quyết định này, hạng quyền là `PENDING_REVIEW` |
| Giọng kênh | **Người dùng chọn `bm_george` (2026-10-29)** sau buổi thử giọng (`projects/bridge-load-explained/review/voice_audition/AUDITION.md`; trước đó mặc định kỹ thuật là `bf_emma`). License giọng `APPROVED` (approved_by/approved_on trong `script/narration.json`); phát âm thuật ngữ được chủ kênh nghe và chấp nhận |
| OmniVoice | Không đổi: `INTERNAL_PREVIEW_ONLY`, không dùng để sinh lời dẫn M6. Audio cũ của Suffolk giữ nguyên |

## 2. Phiên bản chính xác
| Thành phần | Định danh | Kiểm chứng |
|---|---|---|
| Repo model (chính thức) | `hexgrad/Kokoro-82M` trên Hugging Face, không gated | HF API `/api/models/hexgrad/Kokoro-82M` |
| Revision | `f3ff3571791e39611d31c381e3a41a3af07b4987` (lastModified 2025-04-10), bản phát hành v1.0 (2025-01-27) | HF API `sha`; model card |
| `kokoro-v1_0.pth` | SHA256 `496dba118d1a58f5f3db2efc88dbdc216e0483fc89fe6e47ee1f2c53f18ad1e4`: **trùng** với hash in trên model card | tính lại trên máy sau khi tải |
| `config.json` | SHA256 `5abb01e2403b072bf03d04fde160443e209d7a0dad49a423be15196b9b43c17f` | tính trên máy |
| Giọng đã chọn để thử | `bf_emma` `d0a423de…`, `bm_fable` `d44935f3…`, `bm_george` `f1bc8122…`, `bm_daniel` `fc3fce4e…` (hash đầy đủ trong `integrations/tts/kokoro.py`): **trùng** với tiền tố SHA256 trong VOICES.md | tính trên máy |
| Code suy luận | `kokoro==0.9.4`, `misaki[en]==0.9.4` (gói chính thức của hexgrad) | `requirements.lock.txt` |
| Môi trường | `~/Work/Projects/Kokoro/.venv`: Python 3.12.15 (uv), `torch==2.15.0` (CPU), `transformers==5.21.0`, `spacy==3.8.18`, `en_core_web_sm==3.8.0`. Khóa đầy đủ 96 gói ở `~/Work/Projects/Kokoro/requirements.lock.txt` | `uv pip freeze` |
| Tải về | Chỉ 4 file + 4 giọng ở đúng revision, qua `hf_hub_download(revision=…)`. Không tải model nào khác. Khi sinh audio thì chạy offline (`HF_HUB_OFFLINE=1`) | `~/Work/Projects/Kokoro/fetch_pinned.py` |
| Cách nạp | `torch.load(..., weights_only=True)` cho cả trọng số và giọng (trong gói `kokoro`), nên không thực thi pickle | `kokoro/model.py:68`, `kokoro/pipeline.py:147` |

## 3. License từng thành phần
Các thành phần **không** cùng một license.

| Thành phần | License (theo metadata gói đã cài hoặc trang chính thức) | Có trong đầu ra audio? | Nghĩa vụ |
|---|---|---|---|
| Trọng số Kokoro-82M | Apache-2.0 (model card, metadata repo) | Mô hình sinh ra audio | Apache-2.0 không hạn chế đầu ra. Nếu **phân phối lại** trọng số thì phải giữ LICENSE/NOTICE. Dự án không phân phối lại |
| File giọng `voices/*.pt` | Không có license riêng cho từng giọng tiếng Anh-Anh; repo ghi Apache-2.0. VOICES.md chỉ ghi nguồn CC BY cho một số giọng Nhật và Pháp (không dùng) | Có (vector giọng) | Như trên |
| `kokoro` 0.9.4 (code) | Apache-2.0 | Không | — |
| `misaki` 0.9.4 (G2P) | Apache-2.0 | Không | — |
| `espeakng-loader` 0.2.4 | PyPI **không khai báo license**. Gói **có kèm** thư viện `libespeak-ng 1.52.0` (dylib) và `espeak-ng-data` | Chỉ dùng làm **fallback** phiên âm cho từ ngoài từ điển | eSpeak NG là **GPL-3.0-or-later** (README chính thức). Dùng nội bộ để sinh audio không làm đầu ra phải theo GPL, nhưng **không được phân phối lại** môi trường venv mà không tuân thủ GPL |
| `phonemizer-fork` 3.3.2 | **GPL-3.0-or-later** | Không | Như trên (chỉ dùng cục bộ, không phân phối) |
| `num2words` 0.5.14 | LGPL | Không | Dùng không sửa đổi; không phân phối |
| `spacy` 3.8.18, `en_core_web_sm` 3.8.0, `spacy-curated-transformers` | MIT | Không | — |
| `torch` 2.15.0 | Apache-2.0 AND Apache-2.0 WITH LLVM-exception AND BSD-2/3-Clause AND BSL-1.0 AND ISC AND MIT AND Zlib (metadata) | Không | — |
| `transformers`, `huggingface_hub` | Apache-2.0 | Không | — |
| `soundfile` 0.14.0 (kèm `libsndfile`) | BSD-3-Clause (libsndfile: LGPL-2.1) | Không (adapter ghi WAV bằng `wave` của stdlib) | — |
| ASR kiểm tra: `openai/whisper-large-v3-turbo` | MIT | Không | Chỉ đo WER và căn phụ đề; không nằm trong audio |

**Fallback espeak-ng:** misaki chỉ gọi espeak-ng cho những từ không có trong từ điển của nó. Nếu tắt fallback, những từ đó bị **bỏ qua trong im lặng** ("OOD words will be skipped"). Vì vậy giữ fallback bật, và bước ASR (WER ≤ 0.15) cùng với việc nghe lại có nhiệm vụ bắt các từ bị nói sai hoặc bị mất.

## 4. Nguồn gốc dữ liệu huấn luyện (theo lời nhóm tác giả)
Model card ghi: "trained exclusively on permissive/non-copyrighted audio data and IPA phoneme labels". Các ví dụ được nêu:
- audio public domain;
- audio theo license Apache, MIT;
- **"Synthetic audio generated by closed TTS models from large providers"**, với chú thích "No synthetic audio from open TTS models or 'custom voice clones'".

Tổng cộng khoảng vài trăm giờ. VOICES.md xếp hạng dữ liệu của từng giọng: `bf_emma` có Target Quality B, Training Duration "HH hours" (10–100 giờ), Overall B-.

## 5. Điểm còn mở (chủ kênh đã chấp nhận ngày 2026-10-29; vẫn chưa được giải quyết, vẫn ghi lại đây)
1. **Audio tổng hợp từ TTS đóng trong dữ liệu huấn luyện.** Không rõ nhà cung cấp nào. Điều khoản của các nhà cung cấp đó có thể cấm dùng đầu ra để huấn luyện mô hình cạnh tranh. Rủi ro này thuộc về bên huấn luyện, nhưng **người duyệt cần tự đánh giá** mức chấp nhận rủi ro. Agent không xác minh được.
2. **Giọng có giống một người thật không?** Model card không nói giọng `bf_emma` được làm từ ai. Chú thích "No … custom voice clones" là bằng chứng gián tiếp. Cần một người nghe và xác nhận rằng giọng không mô phỏng một người dễ nhận ra.
3. **Chính sách YouTube** về nội dung tổng hợp hoặc chỉnh sửa và về kiếm tiền (nội dung lặp lại, "inauthentic") có thể thay đổi. Phải kiểm tra lại vào thời điểm xuất bản. Ghi trong mô tả video rằng lời dẫn do AI tạo là cách thận trọng.
4. **Duyệt giọng kênh** (chất lượng, cách đọc, phát âm thuật ngữ) bằng tai người. ASR chỉ chứng minh nghe rõ, không chứng minh phát âm đúng hay giọng hay.
5. Nếu sau này cần **phân phối lại** môi trường hoặc trọng số (ví dụ trong một gói cài đặt): phải tuân thủ GPL-3.0 của espeak-ng/phonemizer và Apache-2.0 NOTICE. Hiện tại không áp dụng.

## 6. Ghi nhận và thông báo nên có
- Khi xuất bản: ghi "Narration voice: Kokoro-82M (hexgrad, Apache-2.0)" và "AI-generated narration" trong mô tả hoặc credits. Apache-2.0 không bắt buộc ghi nhận cho đầu ra; đây là khuyến nghị về minh bạch.
- Mỗi đoạn audio có bản ghi nguồn gốc trong `audio/narration_manifest.json`: provider, revision, SHA256 của model và giọng, tham số sinh, hạng quyền.
- Bản kê nguồn gốc của dự án: `projects/bridge-load-explained/review/RIGHTS_PROVENANCE.md`.

## 7. Nguồn
- https://huggingface.co/hexgrad/Kokoro-82M (model card, license apache-2.0, hash v1.0)
- https://huggingface.co/hexgrad/Kokoro-82M/blob/main/VOICES.md (hạng giọng, tiền tố SHA256)
- https://huggingface.co/api/models/hexgrad/Kokoro-82M (revision `f3ff3571…`, danh sách file)
- https://raw.githubusercontent.com/hexgrad/kokoro/main/pyproject.toml, https://raw.githubusercontent.com/hexgrad/misaki/main/pyproject.toml
- https://github.com/espeak-ng/espeak-ng (GPL-3.0-or-later)
- PyPI JSON: `espeakng-loader`, `phonemizer-fork`, `num2words`
- Metadata các gói đã cài trong `~/Work/Projects/Kokoro/.venv`

## 8. Bổ sung 2026-10-30 (M7): giọng Anh–Mỹ và `am_michael`
- **Tải về:** 20 giọng Anh–Mỹ (`af_*`, `am_*`), lấy từ đúng revision `f3ff3571` bằng `tools/kokoro_fetch_voices.py` (`hf_hub_download`). SHA256 của cả 20 file **khớp** tiền tố trong VOICES.md của revision đó. Các giọng này được ghi trong `kokoro.AUDITION_VOICE_SHA256` và **chỉ dùng để nghe thử**.
- **License:**
  - Repo vẫn là Apache-2.0. README nói rõ model "has been deployed in numerous projects and commercial APIs".
  - VOICES.md **không** có cột CC BY cho giọng Anh–Mỹ (cột này chỉ có ở phần giọng Nhật và giọng Pháp), nên không có nghĩa vụ ghi công cho các giọng này.
  - Audio tạo ra không bị Apache-2.0 hạn chế.
  - Các điểm mở ở §5 (dữ liệu huấn luyện có audio tổng hợp từ TTS đóng; không rõ giọng mô phỏng ai) áp dụng y như với các giọng Anh–Anh.
- **`am_michael`:**
  - Chủ kênh chọn làm giọng đọc cho bản review nội bộ cuối của M7 (2026-10-30), sau khi nghe `review/voice_audition_us/`.
  - SHA256 `9a443b79…` (đầy đủ trong `integrations/tts/kokoro.py`). VOICES.md: Target Quality B, Training Duration H hours, Overall C+.
  - Dùng G2P Anh–Mỹ (`lang_code='a'`; fallback espeak-ng `en-us`).
  - Đã đưa vào danh sách giọng **đã audit để đọc lời dẫn** (`VOICE_SHA256`).
- **Quyền xuất bản: CHƯA mở rộng.**
  - Clearance ngày 2026-10-29 giờ ghi rõ `voices_cleared` = `bf_emma`, `bm_fable`, `bm_george`, `bm_daniel`.
  - `am_michael` nằm trong `voices_pending`.
  - Licence của lời dẫn M7 là `LICENSE_REVIEW_REQUIRED`. Validator từ chối mọi bản ghi `APPROVED` cho một giọng ngoài `voices_cleared`.
  - Chỉ chủ kênh mới mở rộng được clearance.
- **Mẫu thử trước khi sinh toàn bộ:** 6 câu nhiều thuật ngữ (`review/voice_sample_am_michael/`): 136 wpm, mức âm giữa các câu chênh 0,5 dB, WER lớn nhất 0,105, không câu nào bị ngưỡng tốc độ hay độ dài từ chối. ASR nghe sai tên riêng (Gwynns, Corinne, Bollman) giống như với `bm_george`, nên cần người nghe.
