# Gói duyệt biên tập: "Suffolk roofs" (M3.5, narration `m3.5-r1`)

> **Agent không tự duyệt.** Cả 7 claim được kể trong lời dẫn (CLM_101–CLM_107) vẫn ở trạng thái `SOURCE_VERIFIED`. Chỉ người duyệt mới chuyển một claim sang `EDITORIALLY_APPROVED` (xem mục 9). Gate G1 và G6 sẽ chặn cho đến lúc đó.

- Ngày soạn: 2026-10-27. Người soạn: agent. Người duyệt: _(chưa có)_.
- Phạm vi duyệt gồm: câu chữ lời dẫn (`script/narration.json`, revision `m3.5-r1`), chữ trên màn hình (card SC_004, nhãn SC_005/SC_006) và cách thể hiện bằng hình.
- Nguồn đã đối chiếu lại ngày 2026-10-27:
  - **SRC_001**: PDF *Roof Coverings – Traditional Materials, Repairs and Detailing* (Conservation Advice, Nov 2025, ấn bản 3), Babergh & Mid Suffolk District Councils. https://www.babergh.gov.uk/documents/d/asset-library-54706/roof-coverings-traditional-materials-repairs-and-detailing-guidance. sha256 `cc388dd2dba70d7c…`, giống hệt bản đã đọc ở M3. Đã trích lại trang 9–11 bằng `pdftotext`.
  - **SRC_002**: trang web *Roof coverings*, https://www.babergh.gov.uk/roof-coverings-on-historic-buildings (HTTP 200; trang không ghi ngày, footer © 2026), mục "Traditional roof materials". Người duyệt nên tự mở trang này trong trình duyệt để đọc lại.

## 1. Bảng claim

Ký hiệu cột **Hỗ trợ trực tiếp?**: ✅ = nguồn nói gần như nguyên văn; ◐ = được hỗ trợ nhưng có lệch nhỏ hoặc chỉ một nguồn.

### CLM_101: mái nguyên thủy là thatch hoặc oak shingles
| | |
|---|---|
| Câu chữ claim | Older timber-framed buildings in these districts were probably roofed originally with thatch or oak shingles, depending on which materials were available. |
| Câu lời dẫn | **B2.s0**: "Older timber-framed buildings here were probably roofed **originally** with thatch or oak shingles, depending on which materials were available." |
| Nguồn | SRC_001 tr. 9: "Older timber framed buildings would probably have been roofed originally with either thatch or oak shingles depending on the whether materials were available." · SRC_002: "Older, timber framed buildings would probably have been originally roofed with either thatch or oak shingles, depending on which materials were available." |
| Hỗ trợ trực tiếp? | ✅ |
| Chỗ mơ hồ | Bản M3 bỏ chữ "originally", nên câu có thể bị hiểu là nói chung về mọi thời kỳ. M3.5 đã thêm lại. "here" = Babergh và Mid Suffolk (đã nêu ở B1). Oak shingles được nhắc tới nhưng không có hình. |
| Câu an toàn hơn | Đã áp dụng (thêm "originally"). |
| Hình ảnh | SC_002 EXPLODED_VIEW, mô hình minh họa `thatch_50`. Không có mô hình oak shingles. |
| **Đề xuất** | **DUYỆT** (câu chữ M3.5) |

### CLM_102: longstraw thatch, khoảng 50°
| | |
|---|---|
| Câu chữ claim | Longstraw thatch is the most typical / most traditional thatch in these districts and is laid at a steep pitch of about 50 degrees. |
| Câu lời dẫn | **B2.s1**: "Longstraw thatch, the most traditional covering in these districts, is laid at a steep pitch of about fifty degrees." (không đổi so với M3) |
| Nguồn | SRC_001 tr. 9: "Most typical for our districts is longstraw thatch, which is laid at the steeper pitch of about 50ᵒ." · SRC_002: "Longstraw thatch is the most traditional material found in our districts and should be retained - having a characteristically steeper pitch of about 50ᵒ." |
| Hỗ trợ trực tiếp? | ✅ (khớp với cách nói "most traditional material" của SRC_002) |
| Chỗ mơ hồ | Hai nguồn so sánh khác nhau. PDF nói "most typical" trong số các loại thatch. Trang web nói "most traditional material", tức là so với mọi loại vật liệu lợp. PDF còn ghi: "In the north of Suffolk along the Waveney valley, water reed, usually capped with sedge, is more common". Đây là sắc thái vùng miền mà lời dẫn không nhắc tới. |
| Câu an toàn hơn (tùy chọn, **chưa áp dụng**) | "Longstraw thatch, the most typical thatch in these districts, is laid at a steep pitch of about fifty degrees." (theo PDF, hẹp hơn). Nếu áp dụng thì phải sinh lại 1 câu, thời lượng gần như không đổi. |
| Hình ảnh | Mô hình `thatch_50` dốc đúng 50° (nguồn ghi "about"). Nhãn SC_006: "Longstraw thatch · about 50°". |
| **Đề xuất** | **DUYỆT**, hoặc duyệt kèm câu tùy chọn |

### CLM_103: clay peg tiles thay thế **một số** mái thatch
| | |
|---|---|
| Câu chữ claim | Clay peg tiles eventually replaced some of the thatched roofs. |
| Câu lời dẫn | **B3.s0**: "Eventually, clay peg tiles replaced some of these thatched roofs." (không đổi) |
| Nguồn | SRC_001 tr. 9: "Clay peg tiles eventually replaced some of these examples." · SRC_002: "Eventually, clay peg tiles replaced some of our thatched roofs." |
| Hỗ trợ trực tiếp? | ✅ |
| Chỗ mơ hồ | Chữ "some" là then chốt. SC_003 cho thấy **một** ngôi nhà đổi mái, đó là một ví dụ của "some", không phải quy luật. Rủi ro khán giả khái quát hóa được giảm bằng chữ "some" và câu B6.s1. Mô hình được gọi là "plain clay tile" trong khi lời dẫn nói "peg tiles". Hai cách gọi này nhất quán: SRC_001 tr. 10 viết "Early examples are known as 'peg tiles'", còn SRC_002 viết peg tiles "evolved into plain tiles, once nails began to be used". |
| Hình ảnh | SC_003 REPLACE_PARTS `thatch_50` → `plain_tile_50` trên cùng một kết cấu (cùng độ dốc). |
| **Đề xuất** | **DUYỆT** |

### CLM_104: ngói phẳng khá dốc, 45–60°
| | |
|---|---|
| Câu chữ claim (M3.5) | Most plain clay tile roofs here are fairly steeply pitched, between 45 and 60 degrees. |
| Câu lời dẫn | **B3.s1 (M3.5)**: "Most plain clay tile roofs here are fairly steep too, between forty-five and sixty degrees." · M3: "Plain clay tile roofs are fairly steep too, typically forty-five degrees or more." |
| Nguồn | SRC_001 tr. 10: "Most plain tile roofs are fairly steeply pitched between 45ᵒ and 60ᵒ, often replacing a former thatch covering." · SRC_002: "In our districts, they are made of red or orange clay and are found on fairly steeply pitched between roofs of about 45ᵒ." (câu bị lỗi ngữ pháp trên trang) |
| Hỗ trợ trực tiếp? | ✅ theo SRC_001 · ◐ theo SRC_002 |
| Chỗ mơ hồ | **Hai nguồn lệch nhau**: PDF ghi 45–60°, trang web ghi khoảng 45°. PDF là tài liệu chi tiết; chính trang web giới thiệu PDF là tài liệu "covers this topic much more extensively". Câu M3 "45 degrees or more" để ngỏ, không có cận trên, và không nguồn nào nói như vậy. |
| Câu an toàn hơn | Đã áp dụng (theo đúng khoảng của PDF, thêm "Most" và "here"). |
| Hình ảnh | `plain_tile_50` dốc 50°, nằm trong khoảng. Nhãn SC_005/SC_006: "Plain clay tile · 45–60°". |
| **Đề xuất** | **DUYỆT** câu M3.5. Nếu muốn chắc chắn hơn, hỏi Heritage Team của hội đồng xem con số nào là hiện hành (heritage@baberghmidsuffolk.gov.uk). |

### CLM_105: pantile phổ biến hơn từ thế kỷ 18
| | |
|---|---|
| Câu chữ claim | From the eighteenth century, clay pantiles were used more commonly, once it became easier to move materials around the country. |
| Câu lời dẫn | **B4.s0**: "Materials also began to travel further." · **B4.s1**: "From the eighteenth century, clay pantiles were used more commonly, as moving materials around the country became easier." (không đổi) |
| Nguồn | SRC_001 tr. 9: "When it became easier to move materials around the country, clay pantiles would have been used more commonly in the 18th century, being transported by river or canal." · SRC_002: "Clay pantiles were used more commonly from the eighteenth century onward - once it became easier to move materials around the country, and they became cheaper." |
| Hỗ trợ trực tiếp? | ✅ cho phần chung của hai nguồn |
| Chỗ mơ hồ | PDF nói "in the 18th century" (rào đón: "would have been"), trang web nói "from the eighteenth century onward"; lời dẫn theo trang web. Chữ "as" mang nghĩa nhân quả; cả hai nguồn đều ngụ ý điều đó ("When…" / "once…"). Mỗi nguồn có một chi tiết riêng (sông/kênh; giá rẻ hơn), và lời dẫn bỏ cả hai. Theo SRC_001 tr. 10, pantile ở phía bắc Mid Suffolk thường lợp mặt mái chính, còn xa hơn về phía nam thì thường chỉ ở mặt mái sau hoặc nhà phụ. Lời dẫn không khẳng định pantile phổ biến khắp nơi. |
| Câu an toàn hơn (tùy chọn, chưa áp dụng) | "…, once moving materials around the country became easier." ("once" sát với trang web hơn). Chỉ khác về văn phong. |
| Hình ảnh | Card SC_004: "Materials began to travel further" / "18th century: clay pantiles used more commonly". Pantile không có mô hình. |
| **Đề xuất** | **DUYỆT** |

### CLM_106: đường sắt thế kỷ 19 và slate từ Wales, Cornwall, Cumbria
| | |
|---|---|
| Câu chữ claim | In the nineteenth century, the railways meant that slate from Wales, Cornwall and Cumbria was often used in the area. |
| Câu lời dẫn | **B4.s2**: "In the nineteenth century, the railways meant that slate from Wales, Cornwall and Cumbria was often used here." (không đổi) |
| Nguồn | SRC_001 tr. 9: "In the 19th century, the creation of the railways meant that slate from Wales, Cornwall and Cumbria were often also used in our area." · SRC_002: "In the nineteenth century, the creation of the railways meant that slate from Wales, Cornwall and Cumbria were often used in our area." |
| Hỗ trợ trực tiếp? | ✅ |
| Chỗ mơ hồ | Có thể bị hiểu là slate chỉ xuất hiện khi có đường sắt. Nhưng SRC_001 tr. 11 (CLM_108, không đưa vào lời dẫn) ghi: "They date from the 18th century onwards but are most common in the 19th century." "often" không có nghĩa là "chủ yếu". Mũi tên trên card là sơ đồ (có dòng "Schematic, not to scale"); nguồn không nêu tuyến đường. |
| Câu an toàn hơn (tùy chọn) | Có thể thêm bối cảnh CLM_108, nhưng như thế là thêm một claim và kéo dài phim. Chưa áp dụng. |
| Hình ảnh | Card SC_004: "19th century: railways — slate often used here"; mũi tên Cumbria / Wales / Cornwall → Suffolk. |
| **Đề xuất** | **DUYỆT** |

### CLM_107: slate khoảng 30°, hiệu quả hơn ngói nhỏ ở độ dốc thấp
| | |
|---|---|
| Câu chữ claim | Slate roofs there are usually pitched at around 30 degrees, and slate is more effective than other smaller tiles at a lower pitch. |
| Câu lời dẫn | **B5.s0 (M3.5)**: "Slate is different." (M3: "Slate behaves differently.") · **B5.s1**: "Slate roofs here are usually pitched at around thirty degrees, and slate is more effective than smaller tiles at a lower pitch." |
| Nguồn | SRC_001 tr. 11: "Slate is also on timber battens, but roofs are usually pitched at around 30ᵒ and are more effective than other smaller tiles at a lower pitch." · SRC_002: "Roofs are normally pitched at around 30ᵒ, and are more effective than other smaller tiles at a lower pitch." |
| Hỗ trợ trực tiếp? | ✅ |
| Chỗ mơ hồ | Nguồn không giải thích *vì sao*, và lời dẫn cũng không thêm "because". Câu M3 "behaves differently" gợi ý một đặc tính vật lý mà nguồn không mô tả, nên đã đổi thành "Slate is different." SRC_001 tr. 11 có thêm một ví dụ: một mái ngói phẳng có các hàng dưới cùng lợp slate, ở độ dốc thoải hơn. Ví dụ này ủng hộ mối liên hệ giữa độ dốc và vật liệu lợp, đồng thời cho thấy trên một ngôi nhà có thể dùng lẫn nhiều vật liệu. |
| Câu an toàn hơn | Đã áp dụng cho B5.s0. |
| Hình ảnh | SC_005 SIDE_BY_SIDE: nhà ngói và nhà slate là **hai công trình khác nhau**. Nhãn "Plain clay tile · 45–60°" / "Slate · around 30°". Viên slate được vẽ lớn khoảng gấp đôi viên ngói (cách điệu, minh họa "smaller tiles"). Mái slate sáng lên khi lời dẫn nói về độ dốc. |
| **Đề xuất** | **DUYỆT** |

### Các câu không gắn với một claim riêng (cần duyệt câu chữ)
| Câu | Loại | Cơ sở | Đề xuất |
|---|---|---|---|
| B1.s0 "In Babergh and Mid Suffolk, in eastern England, historic roofs do not all look alike." | framing | Tổng hợp từ CLM_102/104/107; "eastern England" là kiến thức địa lý chung | Duyệt |
| B1.s1 "Some rise steeply. Others sit noticeably lower." | framing | 50° / 45–60° so với 30° | Duyệt |
| B6.s0 "Thatch, clay tile and slate each have a typical pitch." | diễn giải | CLM_102/104/107 (phạm vi: hai huyện) | Duyệt |
| B6.s1 "These are tendencies, not rules, and not every building followed the same path." | diễn giải | Nguồn dùng "some", "most", "usually"; các phản ví dụ ở mục 2 | Duyệt |
| B6.s2 (M3.5) "But in this part of Suffolk, a roof's pitch and its covering often go together." · M3: "But the pitch of an old roof can still be a clue to its covering." | diễn giải | Câu M3 **suy ngược** (từ độ dốc đoán ra vật liệu lợp), điều mà nguồn không nói. Hơn nữa, ngói và thatch cùng dốc nên độ dốc không phân biệt được hai loại này. Câu M3.5 chỉ nêu mối liên hệ, có giới hạn phạm vi | Duyệt câu M3.5 |

## 2. Rà soát "trình tự tuyến tính" (thatch → ngói → slate)
Câu chuyện **không được** gợi ý rằng mọi ngôi nhà đều đi theo trình tự thatch → ngói → slate. Nguồn mô tả các xu hướng song song, không phải một trình tự:
- "Thatch can still be found on many old buildings, usually those that are detached." (SRC_001 tr. 9)
- "Clay peg tiles eventually replaced **some** of these examples." (SRC_001 tr. 9)
- "A common feature in Suffolk is a plain tile roof with its lower courses above the eaves laid in slate." (SRC_001 tr. 11): hai vật liệu trên **một** mái.
- Corrugated iron "was often used as a lightweight repair material (usually where thatch had failed)" (SRC_002): một hướng thay thế khác.
- Slate "date from the 18th century onwards" (SRC_001 tr. 11), tức là không chỉ đến sau ngói.

| Vấn đề ở M3 | Sửa ở M3.5 |
|---|---|
| SC_005 REPLACE_PARTS: mái ngói 50° **trên cùng một ngôi nhà** bị thay bằng mái slate 30° (đổi cả kết cấu mái). Nguồn **không** mô tả việc chuyển mái ngói sang slate | SC_005 thành SIDE_BY_SIDE `plain_tile_50` + `slate_30`: hai công trình đặt cạnh nhau, có nhãn, cắt cứng từ card |
| SC_006 kéo camera lùi ra từ đúng ngôi nhà slate đó, càng củng cố cảm giác "một ngôi nhà, ba giai đoạn" | Bỏ intro; cắt cứng sang ba nhà khác nhau có nhãn |
| `states.json` khai báo transition `plain_tile_50 → slate_30` | Đã xóa (có ghi chú lý do) |
| B6.s2 suy ngược từ độ dốc ra vật liệu | Viết lại (xem trên) |

Vẫn giữ: SC_003 (thatch → ngói trên cùng một ngôi nhà), vì có CLM_103 "replaced some" hỗ trợ.

## 3. Đánh giá cách kể chuyện
| Tiêu chí | Nhận xét | Hành động |
|---|---|---|
| Mở đầu (B1) | Ba mái đặt cạnh nhau, câu ngắn, có tương phản (dốc/thoải). Không có câu hỏi "vì sao", điều này hợp lý vì nguồn chỉ trả lời "vì sao" một phần (vật liệu sẵn có, vận chuyển) | Giữ nguyên |
| Mạch truyện | Mạch: nguồn gốc (thatch) → thay đổi (ngói, "some") → bối cảnh (vận chuyển) → slate → tổng kết. Mạch theo thời gian dễ bị hiểu thành trình tự tuyến tính; đã giảm thiểu như ở mục 2 | Đã sửa SC_005/SC_006 |
| Nhịp | Khoảng 170 từ/phút, 75.5 s. B4 (card, 16.7 s) là đoạn dài nhất và nhiều chữ nhất, nhưng chữ hiện dần theo lời dẫn | Giữ nguyên |
| Độ rõ | Số đo được đọc thành chữ; M3.5 thêm nhãn chữ dưới mô hình và hoa văn viên ngói/slate để phân biệt ngói và slate trên màn hình nhỏ | Đã làm (Phase 5) |
| Kết | M3 kết bằng một suy diễn ngược; M3.5 kết bằng một câu có giới hạn phạm vi, rào đón bằng "often" | Đã sửa |
| Tiêu đề project | "Why Did Traditional Roofs in Suffolk Change?" rộng hơn bằng chứng (chỉ hai huyện) và hứa một câu trả lời nhân quả. Gợi ý: "Why Do Old Roofs in Babergh and Mid Suffolk Differ?" | **Người duyệt quyết định** (chưa đổi) |

## 4. Các chỉnh sửa lời dẫn và ảnh hưởng tới timing
Thời lượng đo bằng ffprobe trên audio OmniVoice (`INTERNAL_PREVIEW_ONLY`). 9 câu khác giữ nguyên take M3, không sinh lại.

| Câu | Lý do | M3 → M3.5 (giây) |
|---|---|---|
| B1.s0 | Chỉ sửa phát âm "Babergh" (override `[B EY1 B AH0]`), chữ viết giữ nguyên | 4.88 → 5.40 |
| B2.s0 | Thêm "originally" (bám sát nguồn) | 6.93 → 7.86 |
| B3.s1 | Khoảng 45–60° theo PDF, thay cho "45 or more" | 4.76 → 5.28 |
| B5.s0 | "Slate is different." thay cho "behaves differently" | 1.70 → 1.35 |
| B6.s2 | Bỏ suy diễn ngược | 3.46 → 4.39 |

| Shot | M3 (frame / s) | M3.5 (frame / s) |
|---|---|---|
| SC_001 (B1) | 216 / 9.000 | 228 / 9.500 |
| SC_002 (B2) | 348 / 14.500 | 370 / 15.417 |
| SC_003 (B3) | 236 / 9.833 | 249 / 10.375 |
| SC_004 (B4) | 401 / 16.708 | 401 / 16.708 (không đổi) |
| SC_005 (B5) | 246 / 10.250 | 237 / 9.875 |
| SC_006 (B6) | 305 / 12.708 | 328 / 13.667 |
| **Tổng** | **1752 / 73.000** | **1813 / 75.542** |

## 5. Toàn văn lời dẫn sau sửa (`m3.5-r1`)
**B1:** In Babergh and Mid Suffolk, in eastern England, historic roofs do not all look alike. Some rise steeply. Others sit noticeably lower.

**B2:** Older timber-framed buildings here were probably roofed originally with thatch or oak shingles, depending on which materials were available. Longstraw thatch, the most traditional covering in these districts, is laid at a steep pitch of about fifty degrees.

**B3:** Eventually, clay peg tiles replaced some of these thatched roofs. Most plain clay tile roofs here are fairly steep too, between forty-five and sixty degrees.

**B4:** Materials also began to travel further. From the eighteenth century, clay pantiles were used more commonly, as moving materials around the country became easier. In the nineteenth century, the railways meant that slate from Wales, Cornwall and Cumbria was often used here.

**B5:** Slate is different. Slate roofs here are usually pitched at around thirty degrees, and slate is more effective than smaller tiles at a lower pitch.

**B6:** Thatch, clay tile and slate each have a typical pitch. These are tendencies, not rules, and not every building followed the same path. But in this part of Suffolk, a roof's pitch and its covering often go together.

## 6. Chữ trên màn hình (cũng cần duyệt)
| Vị trí | Chữ | Claim |
|---|---|---|
| SC_004 card | "Materials began to travel further" · "18th century: clay pantiles used more commonly" · "19th century: railways — slate often used here" · "Cumbria" "Wales" "Cornwall" → "Suffolk" · "Schematic, not to scale. Source: Babergh & Mid Suffolk District Councils" | CLM_105, CLM_106 |
| SC_005 nhãn | "Plain clay tile · 45–60°" · "Slate · around 30°" | CLM_104, CLM_107 |
| SC_006 nhãn | "Longstraw thatch · about 50°" · "Plain clay tile · 45–60°" · "Slate · around 30°" | CLM_102, CLM_104, CLM_107 |

Phần minh họa: mô hình nhà, độ dày lớp phủ, kích thước viên ngói/slate (cường điệu khoảng 1.5 lần cho dễ đọc; tỷ lệ slate:ngói khoảng 2:1), ngói nóc và màu sắc đều là giản lược trực quan. Chỉ có độ dốc là lấy theo nguồn.

## 7. Phát âm
"Babergh" được phát âm theo override chỉ dành cho TTS (BAY-ber, /ˈbeɪbə/). Bằng chứng và danh sách nghe ở `qa/pronunciation/PRONUNCIATION_TEST.md`. **ASR không xác nhận được cách phát âm**: Whisper ghi "Baber" cho cả /ˈbeɪbə/ lẫn /ˈbæbə/. Trạng thái: `PENDING_LISTENING_REVIEW`.

## 8. Những gì agent **không** làm
- Không chuyển claim nào sang `EDITORIALLY_APPROVED`, không đặt `factual_review: verified`.
- Không đổi tiêu đề project. Không áp dụng các câu "tùy chọn" của CLM_102 và CLM_105.
- Không thêm sự kiện lịch sử mới (CLM_108 vẫn không đưa vào lời dẫn).

## 9. Danh sách ký duyệt (người duyệt điền)
Duyệt cho narration revision **`m3.5-r1`**. Nếu narration đổi revision, các duyệt cũ sẽ hết hiệu lực và validator sẽ báo lỗi.

- [ ] CLM_101: DUYỆT / SỬA / LOẠI. Ghi chú: ______
- [ ] CLM_102: DUYỆT / DUYỆT KÈM CÂU TÙY CHỌN / LOẠI. Ghi chú: ______
- [ ] CLM_103: DUYỆT / SỬA / LOẠI. Ghi chú: ______
- [ ] CLM_104: DUYỆT / SỬA / LOẠI. Ghi chú: ______
- [ ] CLM_105: DUYỆT / SỬA / LOẠI. Ghi chú: ______
- [ ] CLM_106: DUYỆT / SỬA / LOẠI. Ghi chú: ______
- [ ] CLM_107: DUYỆT / SỬA / LOẠI. Ghi chú: ______
- [ ] Các câu framing/diễn giải B1, B6 (mục 1, bảng cuối)
- [ ] Chữ trên màn hình (mục 6)
- [ ] Bản sửa SC_005/SC_006 (mục 2) chấp nhận được về biên tập
- [ ] Tiêu đề project: giữ / đổi thành ______
- [ ] Phát âm "Babergh": xem `qa/pronunciation/PRONUNCIATION_TEST.md`

Cách ghi nhận (do **người duyệt** làm, trong `research/sources.json`) với mỗi claim đã duyệt:
```json
"review_status": "EDITORIALLY_APPROVED",
"editorial_approval": {"approved_by": "<tên>", "approved_on": "YYYY-MM-DD",
                       "narration_revision": "m3.5-r1", "package": "review/EDITORIAL_APPROVAL_PACKAGE.md"}
```
Sau khi cả 7 claim đều đã duyệt, đặt `"factual_review": "verified"` trong `project.json`, rồi chạy `python3 tools/cli.py gates --project suffolk-roofs`. G1 sẽ PASS. G6 vẫn bị chặn cho đến khi có audio xuất bản được cấp quyền (xem `docs/licensing/TTS_LICENSE_AUDIT.md`).
