# Bản kê quyền và nguồn gốc: gothic-cathedral-heights (revision g-r3, đoạn thử g-r4, các vòng g-r5 tới g-r9)

- Ngày lập: 2026-11-06, cho bản review nội bộ 720p. Cập nhật 2026-11-07 (g-r9): đủ mọi ảnh đang dùng, số nguồn và claim mới. Người lập: agent. Đây là bản kê, **không phải tư vấn pháp lý**.
- **Trạng thái duyệt:** chưa có. Chưa có `review/OWNER_APPROVALS.json`. Các nhận xét của chủ kênh về g-r1, g-r2 và g-r3 là yêu cầu sửa hoặc cho làm tiếp, không phải duyệt. Bản này là **INTERNAL REVIEW**.

| Thành phần | Nguồn gốc | Quyền / license | Trạng thái |
|---|---|---|---|
| Lời dẫn (136 câu) | Sinh cục bộ bằng Kokoro-82M (`hexgrad/Kokoro-82M` @ `f3ff3571`), giọng `am_michael`, `lang_code='a'`, speed 1.0, seed 0 | Apache-2.0. Kiểm toán: `docs/licensing/KOKORO_LICENSE_AUDIT.md`, còn một điểm chưa giải quyết ở mục 5 của bản kiểm toán | `LICENSE_REVIEW_REQUIRED`. Chủ kênh mới duyệt `am_michael` cho `why-bridges-look-different`. Chỉ dùng review nội bộ tới khi chủ kênh duyệt cho dự án này |
| Phát âm | 6 mục ghi đè trong `script/pronunciation.json` | Của dự án | `PENDING_LISTENING_REVIEW`. Agent không nghe được audio |
| Kịch bản | Agent viết từ claim đã đối chiếu (`research/sources.json`: 36 nguồn, 57 claim, phim dùng 54). g-r9 thêm nguồn Atlas du patrimoine de la Seine-Saint-Denis (Michaël Wyss) và claim CLM_165, chỉ cho chú thích trên hình (lời dẫn không đổi) | Của dự án. Câu trích ngắn của Hooke, Viollet-le-Duc, Suger và Vernhes và cộng sự có ghi tên người nói | Chờ duyệt. 0/54 claim được duyệt |
| Mô hình 3D | Sinh thủ tục trong dự án: `cathedral_gothic_section_01`, `cathedral_romanesque_section_01`, `site_level_ground` (`engine/arch/families/cathedral.py`) | `generated_in_project` | `ILLUSTRATIVE`: tỉ lệ tự chọn cho dễ nhìn, không dựng lại công trình thật, không phải phân tích kết cấu. Hình có ghi chú nói rõ |
| Sơ đồ, dòng thời gian, thanh độ cao | Agent vẽ bằng phần tử phẳng (`engine/diagram.py`) từ giá trị trong claim | Của dự án | Có nhãn "Conceptual diagram" hoặc "Schematic" khi cần |
| Hình B40 | Tính lại bằng `script/arch_statics.py` theo phương pháp đã công bố, không chép hình | Của dự án. Ghi "After Block, DeJong and Ochsendorf, 2006, Fig. 5, recalculated by Ochsendorf's 2002 method" | Chưa có người có chuyên môn kết cấu đọc lại |
| Ảnh chụp (chương 1, 4, 5, 6, 8) | Wikimedia Commons và Flickr Commons, tải 2026-11-06 và 2026-11-07 (không lách qua bản sao lưu):<br>– Beauvais, dàn hợp xướng nhìn từ phố Chambiges (Dguendel, CC BY 4.0)<br>– Beauvais, dàn hợp xướng bên trong (Dguendel, CC BY 4.0)<br>– Beauvais, cánh ngang và dàn hợp xướng (Chris06, CC0)<br>– Amiens, lòng chính nhìn từ triforium (Eusebius, CC BY 3.0)<br>– Durham, nội thất, bản in khoảng 1865–1895 (Cornell University Library, không có hạn chế bản quyền đã biết)<br>– Chartres, trụ chống bay lòng chính (Florestan, CC BY 3.0)<br>– Notre-Dame Paris, mặt đông (Jebulon, CC0)<br>– Saint-Denis, cửa sổ hoa hồng (Guilhem Vellut, CC BY 2.0)<br>– Saint-Denis, ambulatory còn lại từ dàn hợp xướng của Suger (NateBergin, CC BY 4.0; g-r9, thay ảnh apse của Ninaras vì phần trên của dàn hợp xướng được dựng lại ở thế kỷ 13)<br>– Chartres, cửa sổ hoa hồng bắc (Eusebius, public domain) | Không dùng ảnh CC BY-SA, vì điều khoản ShareAlike với video chưa rõ | Hồ sơ đầy đủ trong `assets/manifest.json`: nguồn, tác giả, giấy phép, SHA256, chỉnh sửa (thu nhỏ, cắt khung khi render, đánh dấu bên cạnh). Ghi công trên hình và trong mô tả. Ảnh chụp công trình hôm nay đều ghi "today"; không khẳng định kính màu hiện nay là của thời Suger. **Agent chỉ kiểm giấy phép theo hồ sơ nguồn. Chủ kênh chưa duyệt ảnh và ghi công** |
| Bản vẽ lịch sử (g-r5, chương 8) | Eugène Viollet-le-Duc, *Dictionnaire raisonné de l'architecture française* (1854–1868), bản quét trên Wikimedia Commons:<br>– mặt cắt trụ chống bay Beauvais<br>– mặt bằng Beauvais<br>– mặt bằng Amiens | Public domain (tác giả mất năm 1879) | Dùng nguyên bản quét. Dấu vẽ lên (vùng vòm sập, giả thuyết, trụ mới, giao cánh, tuyến dây xích) đều ghi "schematic". Mặt bằng Amiens là thiết kế gốc theo Viollet-le-Duc, chú thích có nói rõ. Bản vẽ thanh sắt Amiens trên Commons bị bỏ, vì tác giả và năm ghi không chắc chắn |
| Footage | **Không có** | — | — |
| Chữ trên hình | Font `<builtin>` của Blender | Như các phim trước: chưa xác định file font cụ thể đứng sau `<builtin>` | Cần chốt trước khi xuất bản |
| Phụ đề (SRT + track mov_text) | Chép nguyên văn lời dẫn; thời điểm theo khoảng câu đã đo | Của dự án | — |
| ASR (chỉ dùng cho QA) | `openai/whisper-large-v3-turbo` cục bộ | MIT | Không nằm trong video |
| Nhạc | **Không có** | — | — |
| Hiệu ứng âm thanh (từ đoạn thử g-r4; có trong các chương và bản ghép g-r9) | Tổng hợp trong dự án bằng `pipeline/sound.py` theo `config/sound_design.json`: tiếng đá đặt xuống (`STONE`, `STONE_HEAVY`), không dùng bản ghi hay thư viện nào | Của dự án | Agent không nghe được. Chủ kênh chưa nghe duyệt |

## Nguồn không dùng được

Những nguồn này không mở được ngày 2026-11-05 và không được lách qua bản sao lưu: Britannica, UNESCO, Smarthistory, kho kiểm kê Hauts-de-France, bài MDPI 2025 (HTTP 403); The Met (HTTP 429); visit-amiens.com (lỗi kết nối). Chi tiết ở `research/source_snapshots.json` → `not_used`.

## Công bố khi xuất bản

Lời dẫn do AI sinh phải được nêu trong phần mô tả (`review/YOUTUBE_DESCRIPTION.md`, đang là bản nháp). Việc duyệt và đăng thuộc về chủ kênh.
