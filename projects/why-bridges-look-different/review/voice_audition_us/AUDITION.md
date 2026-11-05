# Thử giọng Kokoro-82M

- Model: `hexgrad/Kokoro-82M` revision `f3ff3571791e…`, tham số speed 1.0, seed 0, lang_code a (af_/am_) or b (bf_/bm_). Sinh cục bộ, offline.
- Giọng có dấu ✗ ở cột "Dùng cho lời dẫn" chỉ để nghe thử: pipeline lời dẫn từ chối chúng, và quyền xuất bản ngày 2026-10-29 chưa áp dụng cho chúng.
- Đo lúc 2026-10-30T12:26:04Z bằng `tools/voice_audition.py`.
- Đoạn thử (lấy từ kịch bản pilot, có thuật ngữ kỹ thuật):
  - B02.s0: "So why don't bridges all look the same?"
  - B10.s1: "It is built from wedge-shaped stones called voussoirs, with a keystone at the crown."
  - B28.s2: "This timber trestle near Corinne, Utah, was built in 1872 by the Central Pacific Railroad."

| Giọng | Giọng đọc | Dùng cho lời dẫn | VOICES.md (target / thời lượng huấn luyện / tổng) | Tốc độ (wpm) | WER lớn nhất | Chênh mức âm giữa các câu (dB) | File nghe |
|---|---|---|---|---|---|---|---|
| `af_heart` | American English, nữ | ✗ | — / — / **A** | 149.5 | 0.067 | 0.4 | `review/voice_audition_us/af_heart.m4a` |
| `af_bella` | American English, nữ | ✗ | A / HH hours / **A-** | 136.6 | 0.067 | 1.6 | `review/voice_audition_us/af_bella.m4a` |
| `af_nicole` | American English, nữ | ✗ | B / HH hours / **B-** | 102.5 | 0.067 | 0.6 | `review/voice_audition_us/af_nicole.m4a` |
| `am_puck` | American English, nam | ✗ | B / H hours / **C+** | 149.7 | 0.067 | 0.6 | `review/voice_audition_us/am_puck.m4a` |
| `am_fenrir` | American English, nam | ✗ | B / H hours / **C+** | 148.5 | 0.067 | 0.2 | `review/voice_audition_us/am_fenrir.m4a` |
| `af_aoede` | American English, nữ | ✗ | B / H hours / **C+** | 147.5 | 0.067 | 0.0 | `review/voice_audition_us/af_aoede.m4a` |
| `af_kore` | American English, nữ | ✗ | B / H hours / **C+** | 145.3 | 0.067 | 0.5 | `review/voice_audition_us/af_kore.m4a` |
| `af_sarah` | American English, nữ | ✗ | B / H hours / **C+** | 136.0 | 0.067 | 0.2 | `review/voice_audition_us/af_sarah.m4a` |
| `am_michael` | American English, nam | ✗ | B / H hours / **C+** | 130.6 | 0.067 | 0.3 | `review/voice_audition_us/am_michael.m4a` |
| `af_nova` | American English, nữ | ✗ | B / MM minutes / **C** | 145.3 | 0.067 | 1.1 | `review/voice_audition_us/af_nova.m4a` |
| `af_alloy` | American English, nữ | ✗ | B / MM minutes / **C** | 141.0 | 0.067 | 1.4 | `review/voice_audition_us/af_alloy.m4a` |
| `bm_george` | British English, nam | ✓ | B / MM minutes / **C** | 131.8 | 0.067 | 0.1 | `review/voice_audition_us/bm_george.m4a` |
| `af_sky` | American English, nữ | ✗ | B / _M minutes_ 🤏 / **C-** | 143.0 | 0.067 | 0.7 | `review/voice_audition_us/af_sky.m4a` |
| `am_eric` | American English, nam | ✗ | C / MM minutes / **D** | 160.0 | 0.067 | 0.6 | `review/voice_audition_us/am_eric.m4a` |
| `af_jessica` | American English, nữ | ✗ | C / MM minutes / **D** | 161.5 | 0.067 | 0.8 | `review/voice_audition_us/af_jessica.m4a` |
| `af_river` | American English, nữ | ✗ | C / MM minutes / **D** | 158.0 | 0.067 | 0.8 | `review/voice_audition_us/af_river.m4a` |
| `am_liam` | American English, nam | ✗ | C / MM minutes / **D** | 153.4 | 0.067 | 0.5 | `review/voice_audition_us/am_liam.m4a` |
| `am_onyx` | American English, nam | ✗ | C / MM minutes / **D** | 143.5 | 0.067 | 1.7 | `review/voice_audition_us/am_onyx.m4a` |
| `am_echo` | American English, nam | ✗ | C / MM minutes / **D** | 139.2 | 0.067 | 1.2 | `review/voice_audition_us/am_echo.m4a` |
| `am_santa` | American English, nam | ✗ | C / _M minutes_ 🤏 / **D-** | 142.1 | 0.067 | 0.5 | `review/voice_audition_us/am_santa.m4a` |
| `am_adam` | American English, nam | ✗ | D / H hours / **F+** | 144.4 | 0.067 | 0.2 | `review/voice_audition_us/am_adam.m4a` |

## Không qua kiểm tra tốc độ/độ dài của lời dẫn (vẫn giữ clip để nghe)

- `af_nicole`: af_nicole.s2.wav: 1.432 words/s is outside 1.5-4.5; generation is likely truncated or garbled

## ASR nghe được gì

- `af_heart`: "So why don't bridges all look the same?" (WER 0.000) / "It is built from wedge-shaped stones called voussoirs, with a keystone at the crown." (WER 0.000) / "This timber trestle near Kareen, Utah, was built in 1872 by the Central Pacific Railroad." (WER 0.067)
- `af_bella`: "So why don't bridges all look the same?" (WER 0.000) / "It is built from wedge-shaped stones called voossoirs, with a keystone at the crown." (WER 0.067) / "This timber trestle near Kareen, Utah, was built in 1872 by the Central Pacific Railroad." (WER 0.067)
- `af_nicole`: "So why don't bridges all look the same?" (WER 0.000) / "It is built from wedge-shaped stones called foossoirs, with a keystone at the crown." (WER 0.067) / "This timber trestle near Kareen, Utah, was built in 1872 by the Central Pacific Railroad." (WER 0.067)
- `am_puck`: "So why don't bridges all look the same?" (WER 0.000) / "It is built from wedge-shaped stones called veussoirs with a keystone at the crown." (WER 0.067) / "This timber trestle near Corrine, Utah, was built in 1872 by the Central Pacific Railroad." (WER 0.067)
- `am_fenrir`: "So why don't bridges all look the same?" (WER 0.000) / "It is built from wedge-shaped stones called voussoirs with a keystone at the crown." (WER 0.000) / "This timber trestle near Corrine, Utah, was built in 1872 by the Central Pacific Railroad." (WER 0.067)
- `af_aoede`: "So why don't bridges all look the same?" (WER 0.000) / "It is built from wedge-shaped stones called voussoirs with a keystone at the crown." (WER 0.000) / "This timber trestle near Corrine, Utah, was built in 1872 by the Central Pacific Railroad." (WER 0.067)
- `af_kore`: "So why don't bridges all look the same?" (WER 0.000) / "It is built from wedge-shaped stones called veussoirs with a keystone at the crown." (WER 0.067) / "This timber trestle near Corrine, Utah was built in 1872 by the Central Pacific Railroad." (WER 0.067)
- `af_sarah`: "So why don't bridges all look the same?" (WER 0.000) / "It is built from wedge-shaped stones called voussoirs, with a keystone at the crown." (WER 0.000) / "This timber trestle near Corrine, Utah, was built in 1872 by the Central Pacific Railroad." (WER 0.067)
- `am_michael`: "So why don't bridges all look the same?" (WER 0.000) / "It is built from wedge-shaped stones called voossoirs with a keystone at the crown." (WER 0.067) / "This timber trestle near Kareen, Utah, was built in 1872 by the Central Pacific Railroad." (WER 0.067)
- `af_nova`: "So why don't bridges all look the same?" (WER 0.000) / "It is built from wedge-shaped stones called voussoirs with a keystone at the crown." (WER 0.000) / "This timber trestle near Kareen, Utah, was built in 1872 by the Central Pacific Railroad." (WER 0.067)
- `af_alloy`: "So why don't bridges all look the same?" (WER 0.000) / "It is built from wedge-shaped stones called voussoirs with a keystone at the crown." (WER 0.000) / "This timber trestle near Kareen, Utah, was built in 1872 by the Central Pacific Railroad." (WER 0.067)
- `bm_george`: "So why don't bridges all look the same?" (WER 0.000) / "It is built from wedge-shaped stones called voussoirs with a keystone at the crown." (WER 0.000) / "This timber trestle near Kareen, Utah, was built in 1872 by the Central Pacific Railroad." (WER 0.067)
- `af_sky`: "So why don't bridges all look the same?" (WER 0.000) / "It is built from wedge-shaped stones called voussoirs with a keystone at the crown." (WER 0.000) / "This timber trestle near Corrine, Utah, was built in 1872 by the Central Pacific Railroad." (WER 0.067)
- `am_eric`: "So why don't bridges all look the same?" (WER 0.000) / "It is built from wedge-shaped stones called voussoirs with a keystone at the crown." (WER 0.000) / "This timber trestle near Kareen, Utah, was built in 1872 by the Central Pacific Railroad." (WER 0.067)
- `af_jessica`: "So why don't bridges all look the same?" (WER 0.000) / "It is built from wedge-shaped stones called voussoirs with a keystone at the crown." (WER 0.000) / "This timber trestle near Kareen, Utah, was built in 1872 by the Central Pacific Railroad." (WER 0.067)
- `af_river`: "So why don't bridges all look the same?" (WER 0.000) / "It is built from wedge-shaped stones called voussoirs with a keystone at the crown." (WER 0.000) / "This timber trestle near Kareen, Utah, was built in 1872 by the Central Pacific Railroad." (WER 0.067)
- `am_liam`: "So why don't bridges all look the same?" (WER 0.000) / "It is built from wedge-shaped stones called voussoirs, with a keystone at the crown." (WER 0.000) / "This timber trestle near Kareen, Utah, was built in 1872 by the Central Pacific Railroad." (WER 0.067)
- `am_onyx`: "So why don't bridges all look the same?" (WER 0.000) / "It is built from wedge-shaped stones called bussoirs with a keystone at the crown." (WER 0.067) / "This timber trestle near Kareen, Utah, was built in 1872 by the Central Pacific Railroad." (WER 0.067)
- `am_echo`: "So why don't bridges all look the same?" (WER 0.000) / "It is built from wedge-shaped stones called voussoirs, with a keystone at the crown." (WER 0.000) / "This timber trestle near Kareen, Utah, was built in 1872 by the Central Pacific Railroad." (WER 0.067)
- `am_santa`: "So why don't bridges all look the same?" (WER 0.000) / "It is built from wedge-shaped stones called voussoirs with a keystone at the crown." (WER 0.000) / "This timber trestle near Kareen, Utah, was built in 1872 by the Central Pacific Railroad" (WER 0.067)
- `am_adam`: "So why don't bridges all look the same?" (WER 0.000) / "It is built from wedge-shaped stones called voussoirs with a keystone at the crown." (WER 0.000) / "This timber trestle near Kareen, Utah, was built in 1872 by the Central Pacific Railroad." (WER 0.067)

## Kết luận kỹ thuật (không phải quyết định chọn giọng)

- Quy tắc xếp hạng (chỉ dựa trên số đo): VOICES.md overall grade, then max ASR WER, then |wpm - 160|, then level spread.
- Giọng mặc định kỹ thuật tạm thời (theo số đo): `af_heart`.
- **Người dùng đã chọn giọng kênh `bm_george` (2026-10-29).** Ghi trong `script/narration.json` → `voice.selection`.
- ASR chỉ chứng minh câu nghe rõ, không chứng minh giọng hay hay phát âm đúng. Thứ hạng không thay cho việc nghe bằng tai.
- Chọn giọng không phải là cấp quyền: `voice.license.status` và hạng quyền provider không đổi. Agent không tự chọn giọng thay người dùng.
- Quyền xuất bản của Kokoro là một bước riêng: `docs/licensing/KOKORO_LICENSE_AUDIT.md` (§5).
