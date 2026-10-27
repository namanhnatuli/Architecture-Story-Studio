# Tích hợp OmniVoice (TTS cục bộ) — báo cáo + hướng dẫn

Kiểm tra lần đầu: 2026-10-27. Project OmniVoice: `/Users/trananh/Work/Projects/OmniVoice` (git `30bb7ac`, package `omnivoice` 0.1.5). Agent **không sửa** bất cứ thứ gì trong project đó.

## 1. OmniVoice là gì (theo code, không đoán)
- Model TTS mã nguồn mở của k2-fsa (Xiaomi). Có Python API, các CLI `omnivoice-infer` / `omnivoice-infer-batch`, và **demo Gradio** `omnivoice-demo`. **Không có REST server riêng**: HTTP API chính là API tự động mà Gradio sinh ra cho demo.
- 3 chế độ: *voice clone* (cần audio tham chiếu), *voice design* (thuộc tính giọng: giới tính / tuổi / cao độ / giọng địa phương), *auto*.
- Đầu ra: WAV PCM int16, **24 kHz, mono**. Không có timestamp theo từ; không có seed (mỗi lần sinh ngẫu nhiên khác nhau).
- Môi trường đã có sẵn: `.venv` (gradio 6.15.2, torch 2.12 + MPS, transformers 5.9.0). Model `k2-fsa/OmniVoice` có trong HF cache (snapshot `999c3324…`, 3.0 GB). Không cài thêm gì.

## 2. Khởi động (chỉ localhost)
```bash
cd /Users/trananh/Work/Projects/OmniVoice
GRADIO_ANALYTICS_ENABLED=False HF_HUB_OFFLINE=1 \
  .venv/bin/omnivoice-demo --ip 127.0.0.1 --port 8001 --no-asr
```
- ⚠️ Mặc định của demo là `--ip 0.0.0.0` (mở ra toàn mạng LAN): **luôn** truyền `--ip 127.0.0.1`. **Không** dùng `--share` (tạo link công khai).
- `--no-asr` bỏ qua việc tải Whisper (~1.6 GB RAM). Voice design không cần ASR; clone thì luôn truyền `reference_text`.
- `HF_HUB_OFFLINE=1`: không gọi mạng (model đã có trong cache). `GRADIO_ANALYTICS_ENABLED=False`: tắt analytics của Gradio.
- Load model trên MPS mất khoảng 3 s; mỗi câu (5–20 từ) mất 4–8 s.

## 3. Hợp đồng API (xác nhận từ `GET /gradio_api/info`; có cả `/gradio_api/openapi.json`)
| Bước | HTTP |
|---|---|
| Hợp đồng | `GET /gradio_api/info` → `named_endpoints` |
| Upload audio tham chiếu | `POST /gradio_api/upload` (multipart, trường `files`) → `["<server path>"]` |
| Gửi yêu cầu sinh | `POST /gradio_api/call/_design_fn` hoặc `/_clone_fn`, body `{"data": [...]}` → `{"event_id"}` |
| Chờ kết quả | `GET /gradio_api/call/<endpoint>/<event_id>`: luồng SSE `event: heartbeat`, rồi `complete` (`data: [FileData, "Done."]`) hoặc `error` |
| Lấy audio | `GET /gradio_api/file=<path>` |

`/_design_fn` nhận 15 tham số theo thứ tự: text, language (enum 647 ngôn ngữ, có "English"), num_step=32, guidance_scale=2.0, denoise=True, speed=1.0, duration (bỏ trống), preprocess_prompt=True, postprocess_output=True, gender, age, pitch, style, english_accent, chinese_dialect (enum song ngữ, ví dụ `"British Accent / 英国口音"`).
`/_clone_fn` nhận: text, language, ref_audio (FileData), ref_text, instruct, cùng 7 tham số sinh.
**Lỗi sinh giọng không trả về HTTP lỗi**: status là chuỗi khác `"Done."` (ví dụ `"Error: …"`). Adapter kiểm tra trường này.

## 4. Adapter (`integrations/tts/omnivoice.py`, chỉ dùng stdlib)
- Ghép tham số theo **nhãn** của hợp đồng đang chạy, không theo vị trí hard-code → nếu form thay đổi thì báo `OmniVoiceContractError` thay vì gửi sai.
- Các lỗi: `OmniVoiceUnavailable` (kèm lệnh khởi động), `OmniVoiceProtocolError`, `OmniVoiceGenerationError`, `OmniVoiceTimeout`, `AudioValidationError`.
- Biến môi trường: `OMNIVOICE_URL` (mặc định `http://127.0.0.1:8001`), `OMNIVOICE_TIMEOUT` (300 s), `OMNIVOICE_RETRIES` (2, **chỉ** cho lỗi kết nối), `OMNIVOICE_MODEL_REVISION`.
- Không bao giờ truyền `duration`: ép độ dài làm méo giọng. Timing của video chạy theo audio, không phải ngược lại.
- Kiểm tra đầu ra (`integrations/audio_probe.py`): ffprobe giải mã được, mức âm (không im lặng, peak > −35 dBFS), tốc độ 1.5–4.5 từ/giây (phát hiện bản bị cụt hoặc đọc vội). Nếu không đạt thì sinh lại, tối đa 3 lần.
- Test: `tests/test_omnivoice_adapter.py` (10 test, chạy với server Gradio giả lập: mất kết nối, JSON hỏng, sự kiện lỗi, status sai, im lặng, hợp đồng đổi, timeout, tốc độ bất thường).

## 5. Giọng đã chọn
- **`narrator_en_gb_m1`**: voice design `Male, Middle-aged, Low Pitch, British Accent` tạo **một clip tham chiếu tổng hợp 5.19 s**; mọi câu sau đó được sinh bằng **clone từ clip này**, để âm sắc nhất quán (voice design không có seed). **Không clone giọng người thật nào.** Các file `vi_*.mp3` / `voices/` trong thư mục OmniVoice không được dùng.
- Tốc độ chung 0.92 (≈173 từ/phút đo được, so với 185 ở 1.0), áp dụng cho toàn bộ lời dẫn, không chỉnh theo từng beat.
- Kiểm tra độ rõ: Whisper large-v3-turbo (cache cục bộ, chạy offline bằng venv của OmniVoice qua `tools/asr_whisper.py`). 14/14 câu nhận dạng là English, WER ≤ 0.111. Lưu ý: "Babergh" được nghe thành "Baburg" → **cần người kiểm tra cách phát âm** (OmniVoice hỗ trợ sửa phát âm bằng ký hiệu CMU).

## 6. License — `LICENSE_REVIEW_REQUIRED` (không phải tư vấn pháp lý)
| Thành phần | License | Ghi chú |
|---|---|---|
| Code OmniVoice | Apache-2.0 | `LICENSE`, pyproject |
| Trọng số `k2-fsa/OmniVoice` | `apache-2.0` (front matter của model card) | Base model Qwen3-0.6B |
| **`audio_tokenizer` (Higgs Audio v2 tokenizer, Boson AI)** | **Boson Higgs Audio 2 Community License** (dựa trên Llama 3 Community License) | Phải ghi "Built with Higgs Materials licensed from Boson AI USA, Inc. …" khi phân phối sản phẩm/dịch vụ có dùng nó; áp dụng Llama 3 AUP; **trên 100.000 người dùng hoạt động mỗi năm phải xin giấy phép mở rộng** (chưa rõ có áp dụng cho kênh YouTube không); không dùng đầu ra để cải thiện LLM khác |
| Dữ liệu huấn luyện | Model card không ghi | Tài liệu repo chỉ dùng Emilia làm ví dụ huấn luyện |
| Model card | Cấm clone giọng trái phép, giả mạo, lừa đảo | Đáp ứng: chỉ dùng giọng tổng hợp |

**Quyết định:** chỉ dùng cho preview nội bộ. Xuất bản bị chặn (gate G2/G6) cho đến khi người duyệt các điều khoản Boson và nguồn gốc dữ liệu huấn luyện.
