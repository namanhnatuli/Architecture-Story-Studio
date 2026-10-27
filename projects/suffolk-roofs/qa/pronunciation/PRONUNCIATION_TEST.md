# Thử phát âm "Babergh" (PRON_001)

- Mục tiêu: **BAY-ber**, IPA **/ˈbeɪbə/** (theo brief M3.5). Chữ viết vẫn là "Babergh" ở mọi nơi: lời dẫn, phụ đề, trích dẫn, metadata.
- Cơ chế: override chỉ áp dụng cho TTS, khai báo trong `script/pronunciation.json`. OmniVoice nhận dạng phiên âm CMU `[B EY1 B AH0]` (README OmniVoice: "Use CMU pronunciation dictionary (uppercase, in brackets) to override default English pronunciations").
- Giọng đọc: chính giọng narrator của pilot (clone từ reference tổng hợp), cùng tham số. Hạng quyền: `INTERNAL_PREVIEW_ONLY` (OmniVoice).
- Sinh ngày 2026-10-27 bằng `python3 tools/pronunciation_test.py --project suffolk-roofs`. Chi tiết trong `PRON_001_report.json`.

| Clip | Văn bản gửi cho TTS | Whisper nghe được (chỉ tham khảo) |
|---|---|---|
| `PRON_001_V0_baseline_m3.wav` | "In Babergh and Mid Suffolk, …" (take M3, không override) | "In **Baburg** and Mid-Suffolk, …" |
| `PRON_001_V1_cmu.wav` | "In [B EY1 B AH0] and Mid Suffolk, …" | "In **Baber** and Mid-Suffolk, …" |
| `PRON_001_V2_respell.wav` | "In Bayber and Mid Suffolk, …" | "In **Baber** and Mid-Suffolk …" |
| `PRON_001_V3_respell.wav` | "In Bay-ber and Mid Suffolk, …" | "In **Babur** and Mid-Suffolk …" |
| `PRON_001_V1_cmu_phrase.wav` | "[B EY1 B AH0] District." | "**Baber** district." |

## Cách đọc kết quả
- Whisper chỉ ghi ra cách viết tiếng Anh gần nhất. "Baber" **không phân biệt được** /ˈbeɪbə/ ("BAY-ber") với /ˈbæbə/ ("BAB-er"). Vì vậy ASR **không chứng minh** được phát âm đúng.
- Điều ASR cho thấy được: bản M3 có âm cuối giống /g/ ("Baburg"); các bản override thì không.
- Lần thử đầu, khi chỉ gửi riêng phiên âm `[B EY1 B AH0].`, OmniVoice trả về file WAV rỗng (0 mẫu). Lỗi này đã được bắt thành `AudioValidationError` (trước đó là `KeyError`). Vì thế clip ngắn được thử ở dạng cụm "… District.".
- Override được chọn cho lời dẫn: **V1 (CMU)**. Đây là cách mô tả âm vị tường minh nhất và không phụ thuộc vào cách model đoán chính tả. Chỉ câu B1.s0 được sinh lại. 13 câu khác giữ nguyên take M3, trừ những câu có sửa chữ (xem gói duyệt biên tập).

## Danh sách nghe (người duyệt điền)
- [ ] V0: xác nhận bản M3 sai (nghe như "BAB-urg").
- [ ] V1 (câu): âm tiết đầu là **BAY** (/beɪ/), không phải BAB (/bæ/).
- [ ] V1 (câu): âm tiết cuối là /ə/ nhẹ, **không có** /g/ và không có /r/ rõ.
- [ ] V1 (câu): trọng âm ở âm tiết đầu; ngữ điệu cả câu tự nhiên, không bị ngắt quãng quanh từ này.
- [ ] Câu B1.s0 trong `output/suffolk_roofs_pilot_INTERNAL.mp4` (giây 0.3–5.5) nghe giống V1.
- [ ] Nếu V1 không đạt: ghi lại biến thể tốt nhất (V2/V3) hoặc đề xuất phiên âm khác.

Khi đạt, sửa `script/pronunciation.json` → `"status": "CONFIRMED", "confirmed_by": "<tên>", "confirmed_on": "<YYYY-MM-DD>"`. Gate xuất bản sẽ chặn chừng nào mục này chưa ở trạng thái CONFIRMED. Lưu ý: audio OmniVoice dù sao cũng không được xuất bản. Khi đổi sang provider xuất bản, phải khai báo phiên âm cho provider đó (ví dụ SSML IPA) và nghe lại.
