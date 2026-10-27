# Audit license TTS: OmniVoice và các phương án xuất bản

- Ngày audit: **2026-10-27** (M3.5, nhánh `m3.5-editorial-polish`).
- Người thực hiện: agent (Claude Code). **Chưa có người duyệt.**
- **Đây là đánh giá tuân thủ, không thay cho tư vấn pháp lý.** Mọi kết luận "được phép" ở đây đều là cách đọc thận trọng các văn bản công khai. Trước khi kiếm tiền từ video, người chịu trách nhiệm kênh phải tự xác nhận.

## 1. Kết luận

| Mục | Kết luận |
|---|---|
| OmniVoice cho **xuất bản thương mại** (kênh YouTube có kiếm tiền) | **NOT CLEARED** |
| OmniVoice cho **preview kỹ thuật nội bộ** (timing, nhịp, lập lịch shot; không phát hành) | Tạm cho phép với hạng quyền `INTERNAL_PREVIEW_ONLY`. Còn một câu hỏi mở (Q3): việc dùng nội bộ để phát triển một sản phẩm thương mại có được coi là "NonCommercial" hay không |
| 15 take audio M3 đã có (`projects/suffolk-roofs/audio/segments/`) | Giữ nguyên, **không xóa**. Gắn nhãn `INTERNAL_PREVIEW_ONLY`. **Không bao giờ** được dùng làm audio xuất bản, kể cả khi trùng chữ và trùng thời lượng |
| Đường xuất bản | Cần chọn một trong: TTS thương mại có giấy phép, model cục bộ có license phù hợp, hoặc giọng người thật. **Quyết định thuộc về người dùng.** Agent không mua, không đăng ký dịch vụ nào |

Lý do chính: trọng số OmniVoice mà máy này đang dùng **trùng từng byte** với trọng số mà nhóm tác giả hiện công bố theo **CC-BY-NC**. Lý do họ đưa ra là ràng buộc từ dữ liệu huấn luyện (Emilia, CC BY-NC 4.0).

## 2. Phiên bản chính xác đang dùng

| Thành phần | Phiên bản / định danh | Kiểm chứng |
|---|---|---|
| Code OmniVoice (`~/Work/Projects/OmniVoice`) | git `30bb7acaf50221d6b8411739e9fc3c007b5d8eb9` (2026-05-28), package `omnivoice 0.1.5` | `git log -1`; `importlib.metadata.version` |
| License code | Apache-2.0 | `LICENSE`; `pyproject.toml` `license = "Apache-2.0"` |
| Model `k2-fsa/OmniVoice` đã cài | revision `999c332499c708b116876ff5fe1aa5dd15f422ce` (commit "Update README.md", 2026-05-07) | thư mục snapshot trong HF cache |
| Model `k2-fsa/OmniVoice` trên HF hiện tại | `main` = `c5fdb5ccb189668d56333f77ba2629f4cd7535f4` (2026-07-03T03:32:17Z, "Update README.md") | HF API `/api/models/k2-fsa/OmniVoice/commits/main` |
| `model.safetensors` | sha256 `730839316de585f4c8298ec0e1712efc10fb19c6fa4e36eb741cb8d51ebcf6aa`: **giống hệt** ở bản đã cài và trên `main` | tính lại sha256 trên máy; so với LFS oid trên HF |
| `audio_tokenizer/model.safetensors` (Higgs Audio v2 tokenizer) | sha256 `fe7c5e8785e0a05833e1bfc3e002ec7f55af21e306b2e7154a448c1f54ccfb0d`: **giống hệt** | như trên |
| `audio_tokenizer/LICENSE` | blob `000139f87ffdc03106fc422a3bd3cebebb9808b3`: **giống hệt** | git blob oid |
| Base LLM | Qwen3-0.6B (Apache-2.0, theo model card OmniVoice) | model card |
| ASR kiểm tra (không nằm trong audio đầu ra) | `openai/whisper-large-v3-turbo` (MIT) | HF cache; chỉ dùng để đo WER |

Lịch sử commit của repo model cho thấy từ `999c332` đến `c5fdb5c` chỉ có thay đổi ở **README.md** (model card). Không có thay đổi trọng số nào. Thư mục gốc từng có file `LICENSE` (commit `5337ba6`, 2026-04-02), nhưng file này không có ở cả revision đã cài lẫn `main`.

## 3. Nguồn license và trích dẫn nguyên văn

| # | Nguồn | URL | Nội dung (nguyên văn) |
|---|---|---|---|
| L1 | Model card hiện hành (`main` c5fdb5c) | https://huggingface.co/k2-fsa/OmniVoice | "Our code is released under the Apache 2.0 License." / "The pre-trained model is licensed under the CC-BY-NC due to constraints from its training data (e.g., Emilia)." Front matter `cardData` không còn thẻ `license`. |
| L2 | Model card ở revision đã cài (999c332) | HF cache `snapshots/999c332…/README.md` (blob `2fdae21`) | front matter `license: apache-2.0` |
| L3 | Thảo luận HF #29, "How this can be Apache-2.0 if it used Emilia as dataset to train the model?" (vquilonr, 2 Jul) | https://huggingface.co/k2-fsa/OmniVoice/discussions/29 | Maintainer **zhu-han** (tổ chức k2-fsa), 3 Jul: "We have updated the model's license to CC-BY-NC." Ngày 18 Aug có người hỏi "Do you offer a commercial license for the current OmniVoice pretrained weights?" và "Are you planning to release a commercial-safe checkpoint…?". **Chưa có trả lời** (tính đến ngày audit). |
| L4 | Emilia dataset card | https://huggingface.co/datasets/amphion/Emilia-Dataset | Emilia: CC BY-NC 4.0. Emilia-YODAS: CC BY 4.0. Theo trích dẫn trong #29, mrfakename: "you are free to use the Yodas subset under cc-by." |
| L5 | License tokenizer | https://huggingface.co/k2-fsa/OmniVoice/blob/main/audio_tokenizer/LICENSE | Boson Higgs Audio 2 Community License (dựa trên Meta Llama 3 Community License): yêu cầu ghi công "Built with Higgs Materials licensed from Boson AI USA, Inc."; áp dụng Acceptable Use Policy; trên 100.000 người dùng hoạt động mỗi năm phải xin giấy phép mở rộng; cấm dùng đầu ra để cải thiện LLM khác |
| L6 | CC BY-NC 4.0 legal code | https://creativecommons.org/licenses/by-nc/4.0/legalcode | "NonCommercial means not primarily intended for or directed towards commercial advantage or monetary compensation." |

## 4. Đánh giá

### 4.1 Trọng số model: CC-BY-NC
- Nhóm tác giả đã đổi license của **chính các byte trọng số mà máy này đang dùng** từ Apache-2.0 sang CC-BY-NC, và nói rõ lý do là dữ liệu huấn luyện.
- Có một lập luận rằng bản tải xuống khi model card còn ghi `apache-2.0` vẫn giữ license cũ. **Không dựa vào lập luận này.** Nó là câu hỏi pháp lý chưa có lời đáp. Bản thân tác giả cũng xác nhận license Apache trước đây không phù hợp với dữ liệu huấn luyện.
- Một kênh YouTube có kiếm tiền (quảng cáo, tài trợ, affiliate) là "directed towards commercial advantage or monetary compensation". → **NOT CLEARED** cho xuất bản thương mại.
- Kể cả khi phát hành phi thương mại (kênh không kiếm tiền), CC BY vẫn đòi hỏi ghi công. Ngoài ra còn nghĩa vụ ghi công Boson cho tokenizer (L5).

### 4.2 Tokenizer: Boson Higgs Audio 2 Community License
Không ảnh hưởng tới kết luận NOT CLEARED, nhưng **không được suy ra quyền thương mại từ license này**. Nó chỉ phủ phần tokenizer. Nghĩa vụ của nó (ghi công, AUP, ngưỡng 100k người dùng) vẫn áp dụng song song với CC-BY-NC.

### 4.3 Quyền đối với audio đầu ra: chưa chắc chắn
- CC-BY-NC áp dụng cho "Licensed Material", tức trọng số. Audio sinh ra có phải "Adapted Material" hay không là câu hỏi chưa ngã ngũ. Model card cũng không nói gì về quyền với đầu ra.
- Ý định của tác giả là phi thương mại, vì dữ liệu huấn luyện. Cách đọc thận trọng là: **audio sinh từ OmniVoice mang cùng hạn chế phi thương mại.**
- Giọng đọc pilot là giọng tổng hợp (voice design → reference tổng hợp → clone). Không có giọng người thật nào bị sao chép. Điều này loại được rủi ro về quyền nhân thân/giọng nói, nhưng **không** gỡ được hạn chế NC.

### 4.4 Preview nội bộ
- Dùng trên máy cục bộ, không phát hành, để đo timing: đây là cách dùng gần nhất với "non-commercial evaluation".
- Tuy vậy, project này nhằm tới một kênh có thể kiếm tiền (Q3). Vì vậy giới hạn cụ thể là: audio OmniVoice chỉ dùng để đo nhịp và lập lịch shot, **không** dùng làm sản phẩm phát hành, và **không** dùng làm dữ liệu huấn luyện hay tham chiếu cho model khác.

## 5. Câu hỏi cần xác nhận (người dùng / luật sư / tác giả)
1. **Q1.** k2-fsa có cấp license thương mại cho trọng số hiện tại không? Có kế hoạch phát hành checkpoint huấn luyện chỉ trên dữ liệu được phép dùng thương mại (ví dụ Emilia-YODAS) không? (Câu hỏi này trên HF #29 vẫn chưa có trả lời.)
2. **Q2.** Bản tải xuống khi card còn ghi `apache-2.0` (revision 999c332) có được giữ license cũ không? Mặc định của audit: **không dựa vào**.
3. **Q3.** Dùng OmniVoice nội bộ chỉ để đo timing cho một project sau này có kiếm tiền có còn là NonCommercial không? Nếu câu trả lời là "không", phải ngừng dùng OmniVoice ngay cả cho preview, và timing phải lấy từ provider được phép.
4. **Q4.** Kênh có kiếm tiền không, và kiếm tiền khi nào? Nếu kênh không bao giờ kiếm tiền, có thể xét CC-BY-NC kèm ghi công. Nhưng lựa chọn này không nằm trong phạm vi khuyến nghị của dự án.
5. **Q5.** Chính sách YouTube về nội dung tổng hợp/AI và về nội dung sản xuất hàng loạt có đòi hỏi công bố cho giọng đọc AI trong phim tài liệu không? Cần kiểm tra trang chính sách YouTube tại thời điểm xuất bản. Audit này chưa đọc nguồn gốc của các chính sách đó.

## 6. Phương án cho xuất bản (chưa chọn, chưa đăng ký, chưa mua)

Thông tin dưới đây được thu thập ngày 2026-10-27. Ô nào ghi "cần xác nhận" là do audit chưa đọc được văn bản gốc của nhà cung cấp, chỉ có câu trả lời cộng đồng hoặc nguồn thứ cấp.

| Phương án | License / quyền dùng đầu ra | Giọng Anh-Anh | Phát âm "Babergh" | Giữ audio sau khi ngừng dịch vụ | Chi phí | Mức độ tích hợp |
|---|---|---|---|---|---|---|
| **Kokoro-82M** (cục bộ, v1.0, 2025-01-27) | Trọng số **Apache-2.0**. Model card: "trained exclusively on permissive/non-copyrighted audio data". Có phần audio tổng hợp từ TTS đóng của các nhà cung cấp lớn (điều khoản của các nhà cung cấp đó là rủi ro ở phía người huấn luyện; cần xác nhận). Một số tập con là CC BY (Koniwa, SIWIS), nhưng không thuộc giọng Anh-Anh | `bf_emma` (B-), `bm_george` (C), `bm_fable` (C), `bf_isabella` (C) và các giọng khác hạng D. Chất lượng chưa nghe thử | Có thể nhập phiên âm IPA qua misaki/espeak-ng `en-gb` (cần thử) | Có: chạy offline, không có thuê bao | 0 (chạy cục bộ) | Trung bình: venv riêng, `kokoro` + `misaki[en]` + `espeak-ng`. Viết adapter theo interface provider |
| **Piper** en_GB | Code MIT, nhưng **mỗi giọng có license dữ liệu riêng**: `northern_english_male` = CC-BY-SA 4.0 (OpenSLR 83); `alan` = theo mimic3-voices, CC BY-SA 4.0 | Có (giọng vùng miền, chất lượng "medium" 22 kHz) | Qua espeak-ng phoneme (cần thử) | Có | 0 | Thấp. Nhưng ShareAlike có thể kéo theo nghĩa vụ với audio đầu ra (chưa rõ), và chất lượng thấp hơn mức phim tài liệu |
| **ElevenLabs** (gói trả phí) | Gói trả phí: được dùng thương mại (trừ tính năng Beta). Gói free: phi thương mại, phải ghi công. Theo trung tâm trợ giúp chính thức: nội dung tạo **trong thời gian có gói trả phí** được dùng thương mại **vô thời hạn** | Có nhiều giọng | Có từ điển phát âm / alias (cần thử) | **Có** với nội dung tạo khi đang trả phí | Thuê bao tháng | Trung bình: API HTTP, khóa API qua biến môi trường |
| **Azure AI Speech** (Neural, tier trả phí) | Câu trả lời của Microsoft Q&A (2024-11-28): dùng thương mại được khi ở **tier trả phí** (Pay-as-you-go), không cần license riêng nếu input là nội dung của mình; phải công bố (disclosure) là giọng tổng hợp; không dùng đầu ra để làm TTS cạnh tranh. **Product Terms gốc: cần xác nhận** | Có (en-GB) | SSML `<phoneme alphabet="ipa">`: xác định, lặp lại được | Có (theo câu trả lời trên: không cần trả phí bản quyền cho file đã tạo). Cần xác nhận | Trả theo ký tự | Trung bình |
| **Google Cloud TTS** | Tài liệu chính thức: audio có thể "augment media like videos or audio recordings" theo Google Cloud Platform Terms of Service. Quyền sở hữu: **cần xác nhận** | Có (ví dụ `en-GB-Chirp3-HD-*`) | SSML chỉ hỗ trợ một phần, tùy giọng (cần thử) | Cần xác nhận | Trả theo ký tự | Trung bình |
| **Amazon Polly** | FAQ chính thức: "As between you and AWS, your Polly output belongs to you." "You can cache and replay Amazon Polly's generated speech at no additional cost." Phải có quyền với văn bản đầu vào | Có (en-GB; danh sách giọng neural cần xác nhận) | SSML `<phoneme alphabet="ipa">` | Có (output thuộc về người dùng) | Trả theo ký tự | Trung bình |
| **OpenAI TTS** | Chính sách sử dụng: phải công bố rõ với người nghe rằng giọng là do AI tạo. Quyền sở hữu đầu ra: Terms of Use (trang trả HTTP 403 khi audit, **cần xác nhận**) | Không có giọng Anh-Anh cố định (cần thử) | Không có SSML | Cần xác nhận | Trả theo ký tự/phút | Thấp-trung bình |
| **Giọng người thật** | Rõ ràng nhất nếu có hợp đồng: buyout, vĩnh viễn, toàn cầu, mọi phương tiện, được phép chỉnh sửa | Chọn theo casting | Đạo diễn trực tiếp ("BAY-ber") | Có (theo hợp đồng) | Theo hợp đồng; sửa lời phải thu lại | Thấp về code (provider `human`: nhập WAV theo câu), cao về điều phối |

### Khuyến nghị (người dùng quyết định)
1. **Ứng viên cục bộ, không tốn tiền:** Kokoro-82M (`bm_george` / `bm_fable` / `bf_emma`). Bước tiếp theo nhỏ nhất: cài vào venv riêng, nghe thử 3 câu pilot và câu "Babergh", rồi người dùng tự đánh giá chất lượng. Trước khi đặt `PUBLICATION_CLEARED`, vẫn cần một người đọc lại model card và xác nhận câu hỏi về dữ liệu tổng hợp từ TTS đóng.
2. **Ứng viên chất lượng cao, phát âm xác định:** Azure hoặc Polly (tier trả phí, SSML IPA). Cần người dùng cho phép mở tài khoản và đọc Product Terms/FAQ gốc.
3. **Phim chủ lực:** giọng người thật, có hợp đồng buyout.
4. **Không khuyến nghị cho xuất bản:** OmniVoice (NOT CLEARED); Piper (ShareAlike + chất lượng); bất kỳ gói free nào.

## 7. Quy tắc dự án rút ra (đã cài trong code M3.5)
- Mỗi provider có một **hạng quyền** (`rights_class`): `INTERNAL_PREVIEW_ONLY`, `PENDING_REVIEW`, `PUBLICATION_CLEARED` hoặc `REJECTED`. Định nghĩa trong `config/tts_providers.json`.
- Khóa cache audio gồm: provider, adapter, định danh và revision của model, giọng, văn bản đọc, tham số và hạng quyền. Audio `INTERNAL_PREVIEW_ONLY` **không bao giờ** khớp cache của lần chạy xuất bản.
- Gate xuất bản (G2/G6) chỉ PASS khi **mọi** segment trong track cuối cùng đến từ provider có hạng quyền `PUBLICATION_CLEARED` **và** người dùng đã ghi tên mình vào mục duyệt license. Agent không tự điền mục này.

## 8. Nguồn đã dùng
- https://huggingface.co/k2-fsa/OmniVoice: model card hiện hành; API commits/tree
- https://huggingface.co/k2-fsa/OmniVoice/discussions/29
- https://huggingface.co/k2-fsa/OmniVoice/blob/main/audio_tokenizer/LICENSE
- https://huggingface.co/datasets/amphion/Emilia-Dataset, https://arxiv.org/abs/2501.15442
- https://creativecommons.org/licenses/by-nc/4.0/legalcode
- https://huggingface.co/hexgrad/Kokoro-82M, https://huggingface.co/hexgrad/Kokoro-82M/blob/main/VOICES.md
- https://huggingface.co/rhasspy/piper-voices (MODEL_CARD của `en_GB/northern_english_male/medium`, `en_GB/alan/medium`); https://github.com/MycroftAI/mimic3-voices/blob/master/LICENSE
- https://elevenlabs.io/docs/help-center/legal/can-i-publish-the-content-i-generate-on-the-platform
- https://learn.microsoft.com/en-us/answers/questions/2124037/can-i-use-azure-text-to-speech-to-generate-mp3-for (câu trả lời cộng đồng của nhân viên MS, không phải Product Terms)
- https://docs.cloud.google.com/text-to-speech/docs/basics
- https://aws.amazon.com/polly/faqs/
- https://developers.openai.com/api/docs/guides/text-to-speech
- Nguồn thứ cấp, chỉ để định hướng, không dùng để kết luận: smallest.ai/blog/commercial-tts-licensing-guide, terms.law/ai-output-rights/elevenlabs
