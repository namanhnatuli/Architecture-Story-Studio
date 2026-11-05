# Duyệt kịch bản: How Gothic Cathedrals Reached Impossible Heights

- Revision lời dẫn: `g-r3`; 10 chương, 46 beat, 136 câu, 1964 từ.
- Thời lượng đo từ audio đã khóa: khoảng **15.4 phút** (15:22).
- Hình: 10:22 là card 2D (67%) nếu giữ nguyên kế hoạch hiện tại.
- Card chỉ có chữ: dài nhất B22–B24, 40 giây liền.
- Claim: 53 claim được dùng, tất cả `SOURCE_VERIFIED`, **chưa claim nào được duyệt biên tập**.

## Trạng thái

Đây là bản g-r3, sửa theo nhận xét thứ hai của bạn. **Chưa có gì được duyệt.** Chưa render video nào, chưa dựng mô hình. Cấu trúc phim, cách mở và lời kêu gọi giữ nguyên. Bản nghe thử: `output/gothic-cathedral-heights_narration_preview_g-r3.m4a`. Bản xem trước 30 card: `output/card_previews_g-r3/` (`contact_sheet.png`, và `B40_s0.png` đến `B40_s4.png` theo từng câu). Đây là ảnh vẽ thử bằng script riêng để kiểm tra bố cục, không phải bản render của engine: phông chữ và độ mịn sẽ khác.

## Câu chuyện trong năm dòng

1. Mở bằng năm 1284: phần vòm cao nhất thời Trung Cổ ở Beauvais sập, sau đó đặt câu hỏi của phim.
2. Vấn đề: đá gần như không chịu được kéo, còn vòm thì đẩy ra ngoài. Một kiểu nhà thờ Romanesque vòm nôi đáp lại bằng tường và trụ dày.
3. Ba công cụ Gothic bố trí lại hệ đỡ: vòm nhọn, vòm gân, trụ chống bay. Tường không còn là chỗ đỡ chính của vòm, nên có thể mở ra đón ánh sáng.
4. Thợ xây làm bằng hình học, kỹ năng nghề và kinh nghiệm, không có phép tính kết cấu hiện đại. Beauvais đi quá giới hạn, còn Amiens phải cứu bằng xích sắt.
5. Kết luận: đá hiếm khi hỏng vì yếu, mà thường vì mất ổn định, nên hình dạng và tỉ lệ giải thích được nhiều điều. Mô hình giúp hiểu vai trò của tỉ lệ, nhưng tự nó không chứng minh một công trình thật an toàn. Độ cao không hề "bất khả thi", và đây cũng không phải câu chuyện tiến bộ đơn giản.

## Đã sửa theo nhận xét lần hai

| Điểm | Beat | Đã sửa thế nào |
|---|---|---|
| 1. Hình đường lực đẩy | B40 | Không còn hai vòm giống nhau với một đường vẽ lệch. Bên trái: một vòm với nhiều đường hợp lệ. Bên phải: chính vòm đó khi gối đỡ dịch ra, tới giới hạn đường lực chạm đá ở năm điểm. Lời dẫn nói rõ thay đổi này |
| 2. Số liệu dưới hai vòm | B08 | Bỏ phần trăm khỏi card, ghi đây là hình minh họa, không phải hai vòm của nghiên cứu. Lời dẫn: "of two other arches" |
| 3. Cluny | B10, B14 | "Whose construction began around 1088"; timeline "Cluny III: construction begins". Không nêu năm cho chính các vòm nhọn |
| Hồ sơ | CLM_123 | Đồng bộ với B07 |
| Biên tập | B14, B15 | Bỏ câu đọc tên Stalley, giữ ý của ông trong sổ claim (`CLM_144`). B15 không còn "Whatever first inspired them" |

Các sửa đổi của lần nhận xét đầu (vòm nhọn, đường lực đẩy, người thợ, vòm gân, độ cao, Durham, đối lập tối/sáng, B24, B35, B22) vẫn giữ nguyên. Nhật ký đầy đủ nằm ở `script/narration.template.json` → `revision.edits`.

## Tôi tự thêm, xin bạn xem lại

1. **Hình B40 dùng kết quả tính lại.** Đây là chỗ đầu tiên trong phim có hình dựa trên phép tính. Tôi tính lại ví dụ ở Hình 5 của bài Block 2006 bằng cùng phương pháp, không chép hình. Số tính lại gần với số in trong bài nhưng không trùng (bảng ở `research/RESEARCH_REPORT.md`, ví dụ giới hạn sập: nhịp +10,6% so với +11,49%; lực đẩy +86% so với +85,10%). Phim không nêu số nào trong đó. Hình ghi "After Block, DeJong and Ochsendorf, 2006, Fig. 5, recalculated". Bạn có thể yêu cầu người có chuyên môn kết cấu kiểm tra `script/arch_statics.py`.
2. **Thu hẹp thêm 7 claim.** Cùng lý do với `CLM_123`, tôi bỏ các phần lời dẫn không nói ở `CLM_143`, `CLM_156`, `CLM_157`, `CLM_161`, `CLM_185`, `CLM_190`, `CLM_191`, ví dụ "first fully gothic structure" ở `CLM_161`.
3. **Nhãn "Stone web" ở B12** nay nằm ngay trên phần đá giữa các gân, thay vì ở ngoài hình.

## Cần bạn quyết định

1. **Độ tin cậy của một số chi tiết.** Các claim `medium` nằm ở bảng cuối tài liệu. Nhiều mục còn dựa vào Association Beauvais Cathédrale, một hội bảo tồn, không qua bình duyệt: ví von "như cánh cung" (B05), vòm nhọn ở Cluny (B10), đường đi của lực qua trụ chống bay (B17), ba gian thành sáu (B36), tháp khoảng 150 m (B37). Tôi không mở được Britannica, UNESCO, Smarthistory và The Met. Nếu bạn có sách của Stephen Murray hoặc Jacques Heyman, các mục này có thể chắc hơn. Toàn văn Romano và Ochsendorf cũng sẽ giúp cho B08.
2. **Đơn vị.** Phim dùng mét, phim cầu trước dùng feet. Lời dẫn và phụ đề dùng chính tả Mỹ (`meters`), khớp với giọng Mỹ.
3. **Phát âm (chỉ bạn xác nhận được).** Kokoro đọc sai nhiều tên Pháp nên có 6 mục ghi đè chỉ áp dụng cho giọng đọc, tất cả đang `PENDING_LISTENING_REVIEW`: Beauvais (boh-VAY), Amiens (am-YAN), Suger (soo-ZHAIR), Cluny (KLOO-nee), Notre-Dame (NOH-truh DAHM), Viollet-le-Duc (vyoh-LAY luh DOOK). Kiểm tra ASR đạt không chứng minh phát âm đúng, và tôi không nghe được audio.
4. **Giọng.** `am_michael` mới được bạn duyệt riêng cho phim cầu. Muốn xuất bản phim này, bạn cần duyệt lại cho dự án này; hiện tại trạng thái là `LICENSE_REVIEW_REQUIRED`.

## Phần hình (sau khi kịch bản được duyệt)

- **Tiêu chí, theo nhận xét của bạn:** chọn hình giúp người xem hiểu, không đổi sang 3D chỉ để giảm tỉ lệ 2D. Tỉ lệ 2D cao tự nó không phải vấn đề; điều cần tránh là chuỗi card chỉ có chữ kéo dài, và hình không được nói nhiều hơn điều nó thực sự chứng minh. Phần đầu tài liệu có đo chuỗi dài nhất.
- **Giữ ở dạng sơ đồ 2D có diễn tiến:** so sánh vòm (B08), dây xích (B09), giàn chống khi xây (B27), mặt bằng thêm trụ (B36), đường lực đẩy (B40). Đây là nơi sơ đồ 2D giải thích tốt nhất.
- **Cần cải thiện:** chuỗi card chữ B22–B24, về ánh sáng và Saint-Denis. Nên dùng ảnh có quyền rõ ràng ở đây.
- **Thư viện chưa có gì về nhà thờ Gothic.** 16 beat 3D đang báo `NEW_ASSET_REQUIRED`, planner không thay bằng thứ khác. Cần họ mô hình mới: mặt cắt một gian Gothic và một gian Romanesque. Planner ước tính 1–3 ngày cho mỗi kiểu. Phần đá giữa các gân phải trông như đá đang làm việc (B13), và kiểu Romanesque không được dựng tối tăm (B06).
- **Ảnh thật.** Chưa tải ảnh nào. Saint-Denis, Chartres, Notre-Dame, Amiens và Beauvais nên có ảnh thật, mỗi ảnh cần hồ sơ quyền đầy đủ.
- **Các card 2D mới được xem bằng ảnh vẽ thử.** Tôi đã xem cả 30 card ở mức tổng quan và B40, B08 ở kích thước lớn. Khi render bằng engine vẫn phải kiểm tra lại.

## Phát âm cần bạn nghe

Mốc thời gian theo bản nghe thử. ASR đạt không chứng minh phát âm đúng.

| Tên | Cách đọc đang dùng | Nghe ở | Nếu không ghi đè | Trạng thái |
|---|---|---|---|---|
| Beauvais | boh-VAY | 0:00 (B01.s0) | bˈOvIz ('BOH-vize'; Whisper heard 'Bovis') | PENDING_LISTENING_REVIEW |
| Amiens | am-YAN (no nasal vowel in the voice) | 0:25 (B02.s1) | ˈɑmiən ('AH-mee-en') | PENDING_LISTENING_REVIEW |
| Suger | soo-ZHAIR | 7:08 (B21.s2) | sˈuɡəɹ ('SOO-gur') | PENDING_LISTENING_REVIEW |
| Cluny | KLOO-nee | 3:16 (B10.s1) | klˈʌni ('KLUH-nee') | PENDING_LISTENING_REVIEW |
| Notre-Dame | NOH-truh DAHM | 6:41 (B19.s3) | nˈɑTəɹdˈAm (the American 'Noter Dame') | PENDING_LISTENING_REVIEW |
| Viollet-le-Duc | vyoh-LAY luh DOOK | 10:36 (B34.s1) | vˈIəlɪtlədˈʌk ('VY-ə-lit luh DUCK') | PENDING_LISTENING_REVIEW |

## Toàn bộ kịch bản

Lời dẫn là tiếng Anh, đúng câu chữ đã đọc. Mốc thời gian là ước tính từ audio đã khóa.

### C1 · Hook (0:00)

**B01** · 0:00 · 3D, cần bộ sinh mới · CLM_103, CLM_104, CLM_106, CLM_181, CLM_182

> In November 1284, in the French city of Beauvais, part of the highest stone vaults of the Middle Ages came down. They stood more than 45 meters above the floor. The choir beneath them, the eastern arm of the cathedral, had been in use for just twelve years.

- Hình: A Gothic section through one bay, seen from low down; the collapse is told, never shown
- Chữ trên hình: Illustrative model, not Beauvais Cathedral · Published heights differ: 46 m to above 48 m

**B02** · 0:20 · 3D, cần bộ sinh mới · CLM_110, CLM_101, CLM_102, CLM_156

> And yet many buildings like it are still standing. At Amiens, begun in 1220, the vault rises more than 42 meters, in a building that is tall, slender and filled with light.

- Hình: The same section: slender piers and tall windows
- Chữ trên hình: Illustrative model, not Amiens Cathedral

**B03** · 0:35 · sơ đồ/card 2D · CLM_110

> The people who built them worked without modern structural calculations, relying on geometry, craft knowledge and experience. So how did they raise stone that high? And why, sometimes, did it come down?

- Hình: Title card: the central question
- Chữ trên hình: How Gothic Cathedrals Reached · Impossible Heights · How did they raise stone that high? · And why, sometimes, did it come down?

### C2 · Stone and its outward push (0:52)

**B04** · 0:52 · sơ đồ/card 2D · CLM_111

> Start with the stone itself. Stone has little or no strength when it is pulled apart. So a stone building stands largely by keeping its stones pressed together.

- Hình: An arch of wedge-shaped stones: pressed together, not pulled apart
- Chữ trên hình: 2 · Stone and its outward push · Pulled apart: little or no strength · Stones pressed together: it stands · Conceptual diagram, not to scale

**B05** · 1:05 · 3D, cần bộ sinh mới · CLM_120, CLM_121

> Now put a heavy stone vault on top of two walls. A vault does not simply press down: it also pushes outward, like a bow being bent. That outward push is called thrust, and a document from Amiens shows that builders there were well aware of it.

- Hình: Romanesque section: a barrel vault on two walls; conceptual outward arrows at the top of the walls (no magnitudes)
- Chữ trên hình: Illustrative model, arrows are conceptual

**B06** · 1:24 · 3D, cần bộ sinh mới · CLM_122

> Romanesque builders had several ways of covering a great church. In the barrel-vaulted type shown here, the heavy vault pushes outward along the whole length of the wall, so walls and supports are thick, stiffened by buttresses. Large openings would weaken the wall that holds the vault, so windows tend to stay small.

- Hình: One barrel-vaulted example: thick walls and shallow buttresses highlighted; small windows. Not lit or framed as gloomy
- Chữ trên hình: One Romanesque type, illustrative model

**B07** · 1:49 · sơ đồ/card 2D · CLM_123, CLM_153

> Gothic builders rearranged that system of support. Instead of spreading the push along a thick wall, they directed it toward particular points, and carried it to supports outside. Three tools made that possible: the pointed arch, the rib vault, and the flying buttress.

- Hình: The three tools named as they are spoken
- Chữ trên hình: Three tools · The same push, with its supports rearranged · Pointed arch · Rib vault · Flying buttress

### C3 · The pointed arch (2:09)

**B08** · 2:09 · sơ đồ/card 2D · CLM_130, CLM_134

> A pointed arch is two arcs of a circle that meet at a point. Over the same span, it can rise higher than a round arch, and a taller arch can push less to the sides. How much less depends on its exact shape, its thickness and the weight it carries. One comparison by MIT engineers, of two other arches, did find that the pointed one pushed less, but that result belongs to those two arches, not to every arch.

- Hình: Round and pointed arch on the same span; the higher rise. No thrust figures: these are not the arches of the study
- Chữ trên hình: 3 · The pointed arch · Round arch · Pointed arch · Rise: half the span · Same span, higher rise · Conceptual arrows: direction only, not calculated · Illustrations, not the arches of the study (Block, DeJong and Ochsendorf, 2006)

**B09** · 2:42 · sơ đồ/card 2D · CLM_114, CLM_115

> In 1675, the scientist Robert Hooke summed up an idea about arches in one line. As hangs the flexible line, so but inverted will stand the rigid arch. Hang a chain with a set of weights, and it takes a shape. Turn that shape upside down, and it shows a path the force can follow through an arch carrying the same weights. Change the weights, and the shape changes too.

- Hình: Hanging chain with weights, inverted; different weights give a different curve
- Chữ trên hình: A chain with its weights · Turned upside down: a path for the force · Different weights, different curve · “As hangs the flexible line, so but inverted · will stand the rigid arch.”  Robert Hooke, 1675 · Conceptual diagram

**B10** · 3:11 · sơ đồ/card 2D · CLM_131

> The pointed arch was not a Gothic invention. It already appears in Burgundy, at the great abbey church of Cluny, whose construction began around 1088, and Columbia University's Amiens project traces it to Islamic sources. At the abbey of Saint-Denis, it was used systematically, together with the other new ideas.

- Hình: Short timeline: pointed arches before Gothic
- Chữ trên hình: 1060 · 1080 · 1100 · 1120 · 1140 · 1160 · 1088  Cluny III: construction begins · Saint-Denis: used systematically

**B11** · 3:37 · sơ đồ/card 2D · CLM_132

> It had a subtler advantage too. Unlike a round arch, a pointed arch can span sections of different widths, called bays, and still reach the same height at its crown. That was a valuable asset for keeping complex vaults regular.

- Hình: Level crowns over different widths
- Chữ trên hình: Round arches · Pointed arches · Crowns at different heights · Same crown height · Wide bay, narrow bay: conceptual diagram

### C4 · The rib vault (3:56)

**B12** · 3:56 · sơ đồ/card 2D · CLM_140

> The second tool is the rib vault. In the four-part vault shown here, two ribs cross diagonally over each bay of the building. In this simplified picture, they direct the vault's load toward four points: the piers, or stone pillars, at its corners.

- Hình: Plan of one bay of a four-part vault: ribs to four piers, the stone web visible between them
- Chữ trên hình: 4 · The rib vault · Diagonal ribs · Stone web · Four piers · One type: a four-part vault · One bay from above. Simplified: how vaults stand is debated

**B13** · 4:15 · 3D, cần bộ sinh mới · CLM_141

> How exactly these vaults stand has been debated for centuries. Engineers following Jacques Heyman assume that the main ribs bring the forces down, and treat the stone between them as a series of parallel arches. So even in that reading, the stone between the ribs carries load.

- Hình: Ribs highlighted, then the web between them: it must read as working stone, never as empty infill
- Chữ trên hình: Illustrative model of one analysis, still debated

**B14** · 4:37 · sơ đồ/card 2D · CLM_142

> Ribs were not new either. Durham Cathedral in England, begun in 1093, was completely covered by ribbed vaults by the time it was finished in 1133. Its masons refined them in phases over some forty years. Columbia's project traces ribs to Islamic, Roman and Byzantine sources.

- Hình: The same timeline, with Durham's building years as a band, not one date
- Chữ trên hình: 1060 · 1080 · 1100 · 1120 · 1140 · 1160 · 1088  Cluny III: construction begins · Durham, begun 1093, finished 1133: ribbed vaults, in phases · Saint-Denis choir

**B15** · 5:03 · 3D, cần bộ sinh mới · CLM_143

> This kind of vault changes the job of the wall. With the vault's load directed toward the piers, the wall between them was no longer its main support. It could be thinned, and opened up with wide windows.

- Hình: The wall between two piers opens into a tall window

### C5 · The flying buttress (5:20)

**B16** · 5:20 · 3D, cần bộ sinh mới · CLM_150

> But gathering the thrust does not make it go away. Even reduced, that sideways push remains a threat to the stability of the whole building. It still has to be contained somewhere.

- Hình: Conceptual outward arrow at the top of a pier, with nothing yet to receive it
- Chữ trên hình: 5 · The flying buttress · Arrows show the idea, not calculated forces

**B17** · 5:34 · 3D, cần bộ sinh mới · CLM_151, CLM_152

> The answer stands outside the building: the flying buttress. It is a stone arch that picks up the thrust where it leaves the vault, carries it across the aisle roof, and brings it down to a massive pier buttress. Often a pinnacle on top adds weight, to help stabilize the thrust.

- Hình: Flyer, pier buttress and pinnacle assemble; a conceptual path follows them to the ground
- Chữ trên hình: Illustrative model, conceptual path

**B18** · 5:56 · 3D, cần bộ sinh mới · CLM_153

> One way to picture it comes from Columbia's Amiens project. It is as if the thick outer wall had been cut into segments, and each segment turned 90 degrees. Those segments become rigid supports, standing out from the building, with exposed arches reaching up to the high vaults.

- Hình: Romanesque thick wall -> segments rotated -> Gothic pier buttresses, same camera

**B19** · 6:18 · 3D, cần bộ sinh mới · CLM_154, CLM_155

> According to France's national library, the first flying buttresses were used to consolidate Romanesque churches that threatened to collapse. It also says that the slanting timber props used while building the vaults were, in effect, made permanent in stone. At Chartres, flying buttresses were part of the original plans. And around the east end of Notre-Dame in Paris, they look almost like a giant external skeleton.

- Hình: Flyers on the model; rights-cleared photographs of Chartres and Notre-Dame replace it where available
- Chữ trên hình: Illustrative model, not Chartres or Notre-Dame

**B20** · 6:49 · 3D, cần bộ sinh mới · CLM_156, CLM_157

> Flying buttresses even help carry rainwater off the roof. But above all, builders learned how to exploit them, and cathedrals grew ever taller.

- Hình: The full exterior of the section, flyers highlighted

### C6 · Walls of light (7:02)

**B21** · 7:02 · sơ đồ/card 2D · CLM_160, CLM_161

> Why go to all this trouble? Part of the answer is light. At the abbey church of Saint-Denis, Abbot Suger built a new choir between 1140 and 1144. Pointed arches run throughout, every vault is ribbed, and monumental stained glass seems to dissolve the whole structure.

- Hình: Saint-Denis, dates and three features (a rights-cleared photograph may replace the card)
- Chữ trên hình: 1120 · 1130 · 1140 · 1150 · 1160 · 1144  Choir dedicated · West front · New choir · 6 · Walls of light · Saint-Denis · Pointed arches throughout · Every vault ribbed · Monumental stained glass

**B22** · 7:25 · sơ đồ/card 2D · CLM_161, CLM_164

> For Suger, light was a sign, a bridge to the divine. France's national library says the new style had to let in as much light as possible.

- Hình: Why light mattered
- Chữ trên hình: “A sign or bridge to the divine” · Light, for Abbot Suger · The new style had to let in as much light as possible · Bibliothèque nationale de France

**B23** · 7:38 · sơ đồ/card 2D · CLM_162

> At Chartres, some 2,500 square meters of stained glass survive, most of it original.

- Hình: One number (a rights-cleared photograph of the glass may replace the card)
- Chữ trên hình: 2,500 m² · of stained glass at Chartres, most of it original

**B24** · 7:46 · sơ đồ/card 2D · CLM_163

> How new was all of this? Some historians call Gothic a revolution in the art of building, while others see a creative step rooted in continuity. Suger's own crypt still relies almost entirely on round arches and groin vaults.

- Hình: Two readings, side by side; the names stay in small type on the card and are not spoken
- Chữ trên hình: How new was Gothic? · “An entire revolution · in the art of building” · After Viollet-le-Duc, 19th century · No Gothic break: a creative · proposal rooted in continuity · Arnaud Timbert, art historian · Suger's crypt: round arches, groin vaults

### C7 · Building by geometry (8:05)

**B25** · 8:05 · sơ đồ/card 2D · CLM_110

> So how did they do all this, without modern structural calculations? Master builders used geometrical rules, developed through centuries of trial and error. They scaled up the same proportions for new, larger elements.

- Hình: One proportion at three sizes
- Chữ trên hình: 7 · Building by geometry · Trial and error, over centuries · The same proportions, scaled up

**B26** · 8:23 · sơ đồ/card 2D · CLM_170

> At Amiens, setting out the site began with ropes pegged to the ground. Squares with perfect right angles controlled the plan, and templates for piers, windows and vaults were designed with straight-edge and compass.

- Hình: Ropes, pegs and a square turned inside a square
- Chữ trên hình: Ropes pegged to the ground · Squares with right angles · Templates: straight-edge and compass · Schematic, not the Amiens plan

**B27** · 8:40 · sơ đồ/card 2D · CLM_172

> Arches were usually drawn full size on the ground, then divided into wedge-shaped stones called voussoirs. Each voussoir was cut to a wooden template, and the stones were laid on a rigid wooden frame called centering. The frame came away only once the mortar had set: at Amiens, after a couple of months or so.

- Hình: An arch on centering; the centering goes away
- Chữ trên hình: Wedge-shaped voussoirs · Each cut to a wooden template · Centering (temporary) · Centering removed · once the mortar has set

**B28** · 9:04 · sơ đồ/card 2D · CLM_173

> Carpenters built the scaffolding, the formwork for the vaults and the lifting gear. They also tied the upper piers with wood, and later iron, to stop the arches pushing them over.

- Hình: What the carpenters made (words, no workers or machinery)
- Chữ trên hình: The carpenters · Scaffolding · Formwork for the vaults · Lifting gear · Ties: wood, later iron · Ties stopped the arches pushing the upper piers over

**B29** · 9:18 · 3D, cần bộ sinh mới · CLM_171

> And there was little room for error. The whole stone skeleton relies on lining up the thrust of each arch with the buttress that supports it.

- Hình: Close on the point where the flyer meets the pier

**B30** · 9:29 · sơ đồ/card 2D · CLM_101

> All of this took generations of work. The foundation stone of Amiens was laid in 1220, and its main roof was not finished until about 1310.

- Hình: Ninety years on one line
- Chữ trên hình: 1200 · 1240 · 1280 · 1320 · 1220  Foundation stone · 1310  Main roof finished (about) · Amiens Cathedral

### C8 · The limit: Beauvais (9:42)

**B31** · 9:42 · sơ đồ/card 2D · CLM_180

> Which brings us back to Beauvais. In 1225, a fire damaged the old Romanesque choir, and the bishop decided to rebuild it, inspired by the greatest buildings of his time.

- Hình: Place and date
- Chữ trên hình: 8 · The limit: Beauvais · Beauvais, 1225 · A fire damages the old Romanesque choir · The bishop rebuilds, after the greatest buildings of his time

**B32** · 9:58 · sơ đồ/card 2D · CLM_181

> By the 1250s, the two lower levels of the new choir were finished. Then the bishop apparently decided to go beyond the planned proportions, adding about five meters to the upper windows, and so to the vaults. By 1272, the clergy could use the new choir.

- Hình: Three levels; the top one grows
- Chữ trên hình: Arcade · Triforium · Upper windows · + about 5 m · Beyond the planned proportions · 1250s: lower levels finished · 1272: choir in use · Schematic, not to scale

**B33** · 10:19 · sơ đồ/card 2D · CLM_102, CLM_103, CLM_104

> Its vault rose more than 45 meters, a few meters above Amiens. These were the highest vaults built in the Middle Ages.

- Hình: Two heights side by side, with the caveat on screen
- Chữ trên hình: Amiens · more than 42 m · Beauvais · more than 45 m · The highest vaults of the Middle Ages · Published for Beauvais: · 46 m, 46.7 m, nearly 47 m, · above 48 m · Bars are schematic

**B34** · 10:30 · 3D, cần bộ sinh mới · CLM_182

> Then, in November 1284, part of the vaults over the choir came down. The architect Viollet-le-Duc, writing centuries later, called it the last limit that the great churches of the 13th century could reach.

- Hình: The section at rest, the vault highlighted; no collapse or debris is shown
- Chữ trên hình: Illustrative model, not Beauvais Cathedral

**B35** · 10:47 · sơ đồ/card 2D · CLM_183, CLM_184

> Why it happened is still debated. Some blame settling masonry that broke the flying buttresses. Others point to gusts of wind setting the buttress system resonating, or to slow settlement of the foundations. A 2024 study found nothing to justify a foundation cause. Its authors argue that raising the vaults, against proven proportions, left the upper parts too flexible.

- Hình: The explanations, one by one
- Chữ trên hình: Why did the vaults fall? Still debated. · Hypothesis: settling masonry broke the flying buttresses · Hypothesis: gusts of wind set the buttress system resonating · Hypothesis: slow settlement of the foundations · Vernhes, Renault and Zotna, 2024: · “nothing appears to justify a geotechnical origin” · Their hypothesis: vaults raised against proven proportions, · upper parts too flexible · ECSMGE 2024, an argument, not a settled result

**B36** · 11:18 · sơ đồ/card 2D · CLM_185, CLM_182

> The repair tells its own story. New piers went up between the old ones, turning three bays into six. The work was not finished until 1340: as the historian Stephen Murray put it, it took longer to repair the choir than to build it.

- Hình: Plan of the choir's straight bays: three become six
- Chữ trên hình: Three bays · New piers: six bays · Repairs finished in 1340 · Longer to repair than to build (Stephen Murray)

**B37** · 11:38 · sơ đồ/card 2D · CLM_186, CLM_187, CLM_106

> In the sixteenth century, work began again, with a new transept, the cross-arm of the building. Then, instead of a nave, the builders raised a lantern tower and spire about 150 meters high, finished in 1569. It rested on four slender piers, and the sources point to a lack of support on the west side, where the nave had not been built. In 1573, just four years after it was finished, the tower came down. The great Gothic nave was never built.

- Hình: Timeline; the fall is told, not shown
- Chữ trên hình: 1480 · 1520 · 1560 · 1600 · 1500  Transept begun · 1569  Lantern tower finished · 1573  Tower falls · Four slender piers, no support to the west · The great Gothic nave: never built

**B38** · 12:15 · sơ đồ/card 2D · CLM_190, CLM_191, CLM_106

> Beauvais was not alone. At Amiens, within two centuries, the piers at the crossing, where the arms of the building meet, were threatening collapse. Between 1497 and 1500, an iron chain was installed to stop the movement, and it still runs through the building today.

- Hình: Two piers tied by a chain
- Chữ trên hình: Amiens · Iron chain, 1497–1500 · Within two centuries, the crossing piers were threatening collapse · Schematic, not to scale

### C9 · Why they stand (12:37)

**B39** · 12:37 · 3D, cần bộ sinh mới · CLM_112

> So why do these buildings stand at all? One answer from modern engineers is that the stone's strength is rarely the limit. Stresses in masonry are typically only a fraction of what the stone can bear, and in most cases structures fail through instability, not a lack of strength.

- Hình: The full section at rest
- Chữ trên hình: 9 · Why they stand

**B40** · 12:59 · sơ đồ/card 2D · CLM_113, CLM_111, CLM_117, CLM_118

> Picture one idealized arch, and the path of the force through its stones, which engineers call the line of thrust. This analysis assumes that the stones resist no pulling, never slide and never crush. Under those assumptions and a given load, many such lines can fit inside the masonry, and finding one is enough to show the arch can stand. Now move its supports apart, and the arch deforms. Past a certain point, no line can fit inside it, and this idealized arch collapses.

- Hình: One arch at rest with several valid lines; the same arch with its supports moved apart, up to the limit. The fall itself is not shown
- Chữ trên hình: The line of thrust · Assumed: stones resist no pulling, never slide, never crush · Many lines can fit. One is enough · Supports moved apart: the arch deforms · At the limit, the line touches the stone at five points · Any further, and no line can fit · After Block, DeJong and Ochsendorf, 2006, Fig. 5, recalculated. One idealized arch, self-weight only

**B41** · 13:37 · sơ đồ/card 2D · CLM_112, CLM_116, CLM_110

> That puts shape and proportion at the center of the question. Unlike some other engineering problems, stability can be scaled, so a small model with the same proportions helps show what proportion does. On its own, that does not show a whole real building is safe: this kind of analysis can miss effects such as local crushing, cracking and sliding. But it helps explain how rules of geometry, learned by trial and error, could carry builders so far.

- Hình: One shape at two sizes; what the model shows and what it does not
- Chữ trên hình: Small model · Real building · Same proportions · Shows the role of proportion · Does not prove a real building safe · Rules of geometry, learned by trial and error

### C10 · Never impossible (14:11)

**B42** · 14:11 · 3D, cần bộ sinh mới · CLM_130, CLM_132, CLM_140, CLM_152, CLM_143

> So the heights were never impossible. Pointed arches gave builders taller, more adaptable shapes, ribs helped direct the load toward the piers, and flying buttresses carried the thrust outside and down to the ground. The walls in between could open up to glass.

- Hình: The section once more: ribs, flyer, buttress and windows lit in turn
- Chữ trên hình: 10 · Never impossible

**B43** · 14:31 · sơ đồ/card 2D · CLM_185, CLM_190, CLM_163, CLM_110

> But it is not a simple story of progress. Beauvais needed new piers, Amiens needed an iron chain, and Suger's bright choir rose above a crypt of older forms. Each cathedral was a test in stone, built by people who learned from centuries of trial and error.

- Hình: Not a linear progression
- Chữ trên hình: Not a simple story of progress · Beauvais: new piers · Amiens: an iron chain · Saint-Denis: a bright choir over a crypt of older forms · Centuries of trial and error

**B44** · 14:52 · 3D, cần bộ sinh mới · không có claim

> These models are illustrations, not structural analyses, and the arrows show ideas, not calculated forces.

- Hình: A last look at the section
- Chữ trên hình: Models are illustrations, not structural analyses

**B45** · 15:02 · sơ đồ/card 2D · không có claim

> Which building or structure should we explain next? Suggest a topic in the comments. And if you enjoyed this film, please like it and subscribe.

- Hình: Closing call to action: plain text, no platform logos or buttons
- Chữ trên hình: What should we explain next? · Suggest a topic in the comments · Like · Subscribe

**B46** · 15:15 · sơ đồ/card 2D · không có claim

> Thank you very much for watching. The sources are listed in the description.

- Hình: Credits
- Chữ trên hình: How Gothic Cathedrals Reached Impossible Heights · Sources: Columbia University (Life of a Cathedral; S. Murray; R. Stalley); · MIT (P. Block, 2005; Block, DeJong and Ochsendorf, 2006; Romano and Ochsendorf); · Bibliothèque nationale de France; France Mémoire (A. Timbert); Durham Cathedral; Abbaye de Cluny (CMN); · ECSMGE 2024 (Vernhes, Renault, Zotna); Association Beauvais Cathédrale · 3D models and diagrams are illustrative, not structural analyses · Architecture Story Studio

## Các claim phim dùng

`medium` = chỉ có hoặc chủ yếu dựa vào nguồn thứ cấp, hoặc các nguồn lệch nhau. Nên xem kỹ các mục này.

| Claim | Tin cậy | Nội dung | Nguồn | Giả định, giới hạn |
|---|---|---|---|---|
| CLM_101 | high | Work on the Gothic cathedral of Amiens began in 1220, after a disastrous fire; its main roof was not finished until about 1310. | SRC_CU_AMIENS_ETEXT_1, SRC_CU_AMIENS_MASONS |  |
| CLM_102 | medium | The high vault of Amiens Cathedral rises more than 42 metres (Columbia's Amiens project gives 43.3 m); Beauvais is a few metres higher. | SRC_ABC_HISTORY, SRC_CU_AMIENS_UPPER_NAVE | Published heights differ: Columbia gives Amiens 43.3 m and Beauvais 46 m; the Beauvais association gives Beauvais nearly 47 m and 4 m more than Amiens. The film says only 'more than 42 metres' for Amiens and 'more than 45 metres' for Beauvais, which all of these support. |
| CLM_103 | high | Beauvais Cathedral has the highest vaults built in the Middle Ages; it suffered two famous structural accidents, in the choir in 1284 and at the transept crossing in 1573. | SRC_ISSMGE_BEAUVAIS_1 |  |
| CLM_104 | medium | The choir vault of Beauvais rises more than 45 metres; published figures differ (46 m, 46.7 m, nearly 47 m, above 48 m). | SRC_ABC_DESCRIPTION, SRC_ABC_FRENCH_ART, SRC_ABC_HISTORY, SRC_CU_AMIENS_UPPER_NAVE | The figures disagree, even within one association's pages (nearly 47 m, 46.7 m, above 48 m; Columbia: 46 m). The narration says only 'more than 45 meters', which all of them support, and the card lists the published figures, from 46 m to above 48 m (owner's script review, 2026-11-05). |
| CLM_106 | high | The eastern arm of a cathedral is commonly called the choir; the long body of the building is crossed by a cross-arm, the transept, and the piers where they meet are the crossing piers. | SRC_CU_AMIENS_ETEXT_11, SRC_CU_AMIENS_ETEXT_4 | E-Text 11 adds that the term is 'something of a misnomer' because the choir proper is where the clergy sat; the film uses the common meaning. 'Crossing piers' is the term used in CLM_190. |
| CLM_110 | high | Medieval master builders worked without modern structural calculations, using geometrical rules developed through centuries of trial and error, craft methods such as templates, and proven proportions scaled up for larger elements; many of their buildings still stand. | SRC_CU_AMIENS_GEOMETRY, SRC_MIT_BLOCK_2005, SRC_MIT_BLOCK_2006 | Block writes 'no knowledge of material properties or allowable stresses'. The film does not repeat that phrase (owner's script review, 2026-11-05): heard alone it denies the builders' practical knowledge, which the film itself shows (CLM_121, CLM_170, CLM_172, CLM_173). 'Without modern structural calculations' is the narrower reading: formal structural analysis came centuries later. |
| CLM_111 | high | Limit analysis of historic masonry rests on three assumptions: no tensile strength, unlimited compressive strength and no sliding; stone has little or no tensile capacity. | SRC_MIT_BLOCK_2005 | These are the assumptions of limit analysis (Heyman), and the film states them as such: 'never crush' is its plain wording of 'infinite compression'. |
| CLM_112 | high | Masonry structures usually fail through instability rather than lack of material strength; stresses are typically only a fraction of the stone's crushing capacity; rigid block models with the same proportions are good models for understanding stability, and unlike problems in elasticity, stability problems can be scaled. | SRC_MIT_BLOCK_2005 | A statement about what such models help to understand, not a safety test of a real building: see CLM_116. |
| CLM_113 | high | Within the assumptions of limit analysis and for a given set of loads, the line of thrust is the path of the compressive force through the stone; a pure compression structure is in equilibrium only if a line of thrust lies entirely within the masonry, and an arch whose profile can no longer contain such a line collapses. | SRC_MIT_BLOCK_2005, SRC_MIT_BLOCK_2006 | Narrated for one idealized arch and a given load, with the assumptions of CLM_111 stated first (owner's script review, 2026-11-05). |
| CLM_114 | high | In 1675 Robert Hooke wrote that the rigid arch stands as a hanging chain hangs, inverted ('As hangs the flexible line, so but inverted will stand the rigid arch'). | SRC_MIT_BLOCK_2005 |  |
| CLM_115 | high | Generalizing Hooke: the shape a string takes under a set of loads, if made rigid and inverted, illustrates a path of compressive forces for an arch carrying the same loads; the shape belongs to those loads. | SRC_MIT_BLOCK_2006 |  |
| CLM_116 | high | Thrust-line analysis is a first-order method resting on strong assumptions: the analyst must then check them, and it can give unconservative results because local crushing, crack propagation and sliding are not considered. | SRC_MIT_BLOCK_2005, SRC_MIT_BLOCK_2006 |  |
| CLM_117 | high | A masonry element that can stand has not one but many valid thrust lines within its section, all lying between a minimum and a maximum thrust; finding one that fits is enough to show the structure can stand for that load, within the assumptions. | SRC_MIT_BLOCK_2006 |  |
| CLM_118 | high | In the published example of an arch on spreading supports, with thickness 15% of the radius and a total angle of embrace of 160 degrees, the arch deforms as its supports move apart; collapse comes when a thrust line can no longer fit, with the line touching the boundaries in more than three places. | SRC_MIT_BLOCK_2006 | The card's geometry is the agent's recalculation of this example with the paper's method (script/arch_statics.py, self-weight only, hinge at 54.4 degrees as printed in Fig. 5), not a tracing of the figure. Against the values printed on the figure: minimum thrust 19.6% of total weight (paper 19.80%); at span +5.09%, thrust +28% (paper +24.59%); limit at span +10.6% and thrust +86% (paper +11.49% and +85.10%). Close, not identical, and the paper does not state its block layout. The card and the narration give none of these numbers. The narration says 'this idealized arch', not any building. |
| CLM_120 | medium | A vault does not only press down: it also pushes outward, like a bow being bent; this outward push is called thrust. | SRC_ABC_THRUST |  |
| CLM_121 | high | Builders at Amiens knew about thrust: a document from the time of the 1497 crisis calls the thrust in the arcade arches 'boutture'. | SRC_CU_AMIENS_POINTED_ARCH | 'Contemporary' refers to the late-medieval Amiens context of the paragraph (the 1497 crisis); the film says only that builders there knew about it, not that every medieval builder did. |
| CLM_122 | high | Romanesque builders had several ways of covering a great church; in the heavily vaulted type shown in the film, the vault's considerable outward thrust called for thick supports and outer walls, stiffened by buttresses, and only small openings. | SRC_ABC_THRUST, SRC_CU_AMIENS_REVOLUTION, SRC_CU_STALLEY_STRUCTURE | Limited to the type illustrated, because Stalley lists barrel vaults, groin vaults and wooden ceilings around 1100. Columbia's page also calls the interior 'dark'; the film drops that word (owner's script review, 2026-11-05), so as not to set a dark Romanesque against a bright Gothic. |
| CLM_123 | high | Gothic builders rearranged the support of the vault: instead of spreading its thrust along a thick wall, they directed it toward particular points and carried it to supports outside, using the pointed arch, the ribbed vault and the flying buttress. | SRC_ABC_THRUST, SRC_CU_AMIENS_ETEXT_18 | The association's wording ('stopped fighting ... with sheer wall thickness') is broader than this claim, which follows B07 (owner's script review, 2026-11-05). Columbia's 'rigid peripheral supports' backs the narrower wording; mass and buttressing still mattered. |
| CLM_130 | medium | A pointed arch is formed by two arcs of a circle meeting at a point; over the same span it can rise higher than a round arch, whose rise is half its span. Sources describe its sideways thrust as reduced; how much depends on the arch's geometry and loads, so a taller arch can push less, not always by the same amount. | SRC_ABC_THRUST, SRC_BNF_ARC_BRISE, SRC_CU_AMIENS_REVOLUTION, SRC_MIT_BLOCK_2006, SRC_MIT_ROMANO | BnF and Columbia state the reduction without conditions; the film adds them (owner's script review, 2026-11-05). 'Half its span' is the geometry of a semicircle. The link between shallowness and thrust is quoted from an arch on spreading supports, so the film says 'can', and gives no general figure. |
| CLM_131 | medium | The pointed arch was not born with Gothic: examples appear in Burgundian Romanesque architecture, including the great abbey church of Cluny (Cluny III), whose construction began around 1088, and Columbia's Amiens project says it was appropriated from Islamic sources; at Saint-Denis it was used systematically with the other Gothic innovations. | SRC_ABC_THRUST, SRC_BNF_ARC_BRISE, SRC_CMN_CLUNY, SRC_CU_AMIENS_REVOLUTION | 1088 dates the building project (the monument's own page), not the pointed arches themselves, so the film gives no year for the arches (owner's script review, 2026-11-05). That Cluny III had pointed arches rests here on the association; BnF says only that Romanesque used them occasionally. |
| CLM_132 | high | Unlike a round arch, a pointed arch can span bays of different widths while keeping the same height at its crown, a valuable asset for keeping complex vaults regular. | SRC_ABC_THRUST, SRC_CU_STALLEY_STRUCTURE | Geometric property also shown on the card: a semicircular arch's rise is half its span. Stalley's second sentence is why the film treats the pointed arch as a geometric tool first. |
| CLM_134 | high | In one comparison by Block, DeJong and Ochsendorf, two arches with the same thickness-to-radius ratio (18%) have thrusts of 16-25% of their self-weight (semicircular) and 14-23% (pointed): the pointed one pushes less. This is a result for those two arches, not a rule for every arch. | SRC_MIT_BLOCK_2006 | The paper's text says 'about 15% less', while its own rounded figures give about 12.5% (minimum) and 8% (maximum). The film narrates no percentage and shows none (owner's second review, 2026-11-05): the arches on the card are not those of the study, and the ranges would need the study's geometry and an explanation of minimum and maximum thrust. |
| CLM_140 | medium | In the simplified picture of a four-part ribbed vault, two ribs cross diagonally over each bay and direct the vault's load toward four points, the corner piers, rather than to the walls. | SRC_ABC_THRUST, SRC_BNF_SAINT_DENIS, SRC_CU_STALLEY_DESCRIBE | Both quoted sources simplify, and how such vaults stand is debated (CLM_141), so the film says 'in this simplified picture' (owner's script review, 2026-11-05). The association and BnF call the crossing ribs 'two pointed arches'; Stalley describes Durham's diagonal ribs as segments of a circle and its pointed arches as transverse, so the film says only 'two ribs'. |
| CLM_141 | high | How quadripartite vaults stand has been debated for centuries; engineers following Jacques Heyman assume the main ribs bring the forces down to the buttresses, with the stone web between them acting as a series of parallel arches, so in that model the web carries load too. | SRC_MIT_BLOCK_2005 | One analysis's assumptions for four-part vaults, attributed as such. 'The web carries load' follows from treating it as arches spanning between the ribs. |
| CLM_142 | high | Durham Cathedral in England was rebuilt between 1093 and 1133 and, when completed, was completely covered by ribbed vaults; its vaults fall into at least three technical phases over some forty years. Columbia's Amiens project gives ribs Islamic, Roman and Byzantine sources. | SRC_CU_AMIENS_REVOLUTION, SRC_CU_STALLEY_STRUCTURE, SRC_DURHAM_CATHEDRAL | 1093 is when the building began, not a date for any vault (owner's script review, 2026-11-05). The association's 'very first ribbed vaults ... as early as 1093' is no longer used, and the film says nothing about who was first: Stalley calls that contentious for northern Europe. |
| CLM_143 | medium | With the vault's load directed toward the piers, the wall between them is no longer the vault's main support, so it can be thinned and opened with wide windows. | SRC_ABC_THRUST, SRC_BNF_ARC_BRISE | The sources are absolute ('no longer carry any load', 'perdent ainsi leur rôle de soutien'). The film says 'main support': a wall still carries at least its own weight, and how vaults stand is debated (CLM_141). |
| CLM_150 | high | Even reduced, the sideways thrust of the vaults remains a threat to the stability of the whole building, so it still has to be resisted. | SRC_ABC_THRUST, SRC_BNF_ARCS_BOUTANTS |  |
| CLM_151 | high | In Gothic buildings, the Romanesque buttresses became flying buttresses: supports set away from the wall and hollowed into arches. | SRC_BNF_ARCS_BOUTANTS |  |
| CLM_152 | medium | A flying buttress picks up the thrust where it leaves the vault, carries it across the aisle roof and down to a massive pier buttress, often topped with a pinnacle whose weight helps stabilise the thrust. | SRC_ABC_THRUST |  |
| CLM_153 | high | Columbia's Amiens project describes the exterior supports (culées) as if the outer wall had been cut into segments, each turned 90 degrees, to give rigid supports for the flying buttresses that hold up the high vaults. | SRC_CU_AMIENS_REVOLUTION |  |
| CLM_154 | high | The first flying buttresses were used to consolidate Romanesque churches that threatened to collapse; at Chartres they were part of the original plans; at Notre-Dame de Paris the flyers around the east end look almost like a giant external skeleton. | SRC_ABC_THRUST, SRC_BNF_ARCS_BOUTANTS | The BnF page says Chartres was the first time ('pour la première fois'). The film drops 'first' and says only 'part of the original plans': flying buttresses at Notre-Dame around 1180 are earlier, and whether those were planned from the start is a question the sources here do not settle. |
| CLM_155 | high | According to France's national library, the slanting timber props that builders used while constructing vaults were made permanent in stone in Gothic architecture. | SRC_BNF_ARCS_BOUTANTS | An explanation given by the BnF educational page; the film attributes it ('according to France's national library'). |
| CLM_156 | high | Flying buttresses allowed builders to create tall, slender, light-filled structures, and builders learned to exploit them to build ever taller cathedrals. | SRC_CU_AMIENS_UPPER_NAVE |  |
| CLM_157 | high | Flying buttresses also help carry rainwater off the roof. | SRC_BNF_ARCS_BOUTANTS |  |
| CLM_160 | high | At the abbey church of Saint-Denis, Abbot Suger built a west front with rib vaults and pointed arches between 1130 and 1140, then a new choir between 1140 and 1144 in which the pointed arch is used throughout, the vaults are all ribbed and monumental stained-glass windows fill the walls. | SRC_FM_TIMBERT_SAINT_DENIS |  |
| CLM_161 | high | Columbia's teaching map says that Suger's choir at Saint-Denis was dedicated in 1144, and that for Suger, light was a sign or bridge to the divine. | SRC_CU_SAINT_DENIS |  |
| CLM_162 | high | Chartres Cathedral keeps about 2,500 square metres of stained glass, most of it original. | SRC_BNF_ARCS_BOUTANTS |  |
| CLM_163 | high | Historians disagree on how new Gothic was: Columbia's Amiens project follows Viollet-le-Duc in calling it an entire revolution in the art of building, while the art historian Arnaud Timbert argues that there was no revolution and no Gothic break, but a creative proposal rooted in continuity; Suger's crypt still relies almost entirely on groin vaults and round arches. | SRC_CU_AMIENS_REVOLUTION, SRC_FM_TIMBERT_SAINT_DENIS, SRC_ISSMGE_BEAUVAIS_1 | Since g-r2 the narration gives the two readings without names (owner's script review, 2026-11-05); the card keeps the attributions in small type. |
| CLM_164 | high | France's national library says that the new style of Saint-Denis had to convey this idea of light to the faithful as soon as they entered, so it became necessary to let in as much light as possible. | SRC_BNF_SAINT_DENIS |  |
| CLM_170 | high | At Amiens the site was set out by stretching ropes pegged to the ground and forming squares with right-angled corners; templates for piers, windows and vaults were drawn with straight-edge and compass. | SRC_CU_AMIENS_GEOMETRY |  |
| CLM_171 | high | The Gothic skeleton relies on lining up the thrust of each arch with the buttress that supports it: there is little room for error. | SRC_CU_AMIENS_GEOMETRY |  |
| CLM_172 | high | Arches were usually drawn full size on the ground and divided into voussoirs; a wooden template was made for each voussoir, and the stones were laid on wooden centering, removed once the mortar had set (at Amiens after a couple of months or so). | SRC_BNF_ARCS_BOUTANTS, SRC_CU_AMIENS_ETEXT_17 |  |
| CLM_173 | high | Carpenters built the scaffolding, the wooden formwork for the vaults and the lifting gear, and tied the upper piers with wooden (later iron) ties to stop the arches pushing them over. | SRC_CU_AMIENS_CARPENTERS |  |
| CLM_180 | high | In 1225 a fire damaged the Romanesque choir of Beauvais; Bishop Milon de Nanteuil decided to rebuild it after the greatest buildings of his time, in the French (Gothic) style. | SRC_ISSMGE_BEAUVAIS_1 |  |
| CLM_181 | high | In the 1250s, with the arcades and triforium finished, Bishop Guillaume de Grès apparently decided to go beyond the originally planned proportions, adding a few metres (about five) to the upper windows and so to the vaults; the clergy could use the new choir from 1272. | SRC_ISSMGE_BEAUVAIS_1 | 'Apparemment': the paper presents the decision as probable, and the film says 'apparently'. |
| CLM_182 | high | On 29 November 1284, twelve years after the choir came into use, part of the vaults of the choir's straight bays collapsed; Viollet-le-Duc called it the last limit that the building of the great 13th-century churches could reach; the repairs ended in 1340, and Stephen Murray notes that the choir took longer to repair than to build. | SRC_ISSMGE_BEAUVAIS_1, SRC_ISSMGE_BEAUVAIS_2 | The film shows no collapse or destruction; it says 'in 1284' (the association gives 'a Friday in November 1284'). |
| CLM_183 | high | Why the 1284 vaults fell is still debated: explanations include monolithic colonnettes and settling mortar breaking flying buttresses, gusts of wind setting the buttress system resonating, and slow differential settlement of the foundations; the 2024 study finds no geotechnical cause and argues that raising the vaults by several metres, against proven proportions, made the upper structure too flexible. | SRC_ISSMGE_BEAUVAIS_2 | The sentence on the raised vaults runs across a page break of the paper, so it is quoted in two excerpts. This is the authors' argument, not a settled result: the film attributes it to them. The association's view (CLM_184) is that a storm was the likely trigger. |
| CLM_184 | medium | The Beauvais association describes the flying buttresses twisting and breaking in November 1284 and thinks a storm was the likely trigger, since the very tall building is exposed to wind. | SRC_ABC_HISTORY |  |
| CLM_185 | medium | After 1284 the Beauvais choir was rebuilt with new intermediate piers that divided its three straight bays into six. | SRC_ABC_DESCRIPTION, SRC_ABC_HISTORY |  |
| CLM_186 | medium | In the 16th century Beauvais built a transept and then, instead of a nave, a lantern tower with a spire about 150 metres high, completed in 1569; the tower rested on four slender crossing piers with no buttressing to the west, where the nave had not been built, and it fell in 1573. | SRC_ABC_HISTORY, SRC_ISSMGE_BEAUVAIS_1, SRC_ISSMGE_BEAUVAIS_2 | 'About 150 metres' is the association's figure for the tower with its spire; the film rounds it as 'about 150 metres'. |
| CLM_187 | high | Beauvais Cathedral's Gothic nave was never built. | SRC_ABC_HISTORY, SRC_ISSMGE_BEAUVAIS_1 | The paper says the Gothic nave was never built; the association says work stopped at a nave reduced to a single bay. The film says 'the great Gothic nave was never built', which both support. |
| CLM_190 | high | At Amiens the crossing piers were threatening collapse, and an iron chain was installed between 1497 and 1500 to arrest the deformation; the chain still runs through the building. | SRC_CU_AMIENS_ETEXT_1, SRC_CU_AMIENS_TRIFORIUM_CHAIN | 'Still runs' rests on the present tense of Columbia's page (copyright 2017, with a note dated 2017). |
| CLM_191 | high | Stephen Murray writes that at Amiens, within two centuries, the crossing piers were threatening collapse. | SRC_CU_AMIENS_ETEXT_17 |  |
