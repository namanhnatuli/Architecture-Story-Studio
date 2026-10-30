# Gói duyệt biên tập: "Why Bridges Don't All Look the Same" (M7, narration `m7-r1`)

> **Đã duyệt claim:** Tran Nam Anh (channel owner) duyệt 41 claim được lời dẫn dùng, ngày 2026-10-30, cho narration `m7-r1` (`research/editorial_approval.json`). Agent chỉ ghi lại quyết định. Phát âm và quyền giọng cho phim vẫn là các bước duyệt riêng; tới khi đủ, mọi bản dựng mang nhãn INTERNAL REVIEW.

## Cần chủ kênh quyết định

1. Lời dẫn: mỗi câu đúng với claim nó trích (xem cột trích dẫn nguồn).
2. Chữ trên card: tiêu đề, nhãn, chú thích ảnh, thang nhịp và dòng thời gian.
3. Ảnh lưu trữ: chọn ảnh, cách cắt viền phim, dòng ghi công (xem `review/RIGHTS_PROVENANCE.md`).
4. Nhãn 'Illustrative model' trên các mô hình 3D đứng cạnh cầu có thật (B27, B29).
5. Phát âm các tên mới (narration.voice.pronunciation_review.terms).
6. Giọng: xác nhận quyết định cấp quyền Kokoro / bm_george ngày 2026-10-29 cũng áp dụng cho phim này (narration.voice.license.owner_confirmation_for_this_film = PENDING).

Cách ghi quyết định giống M6: `research/sources.json` → `review_status: EDITORIALLY_APPROVED` + `editorial_approval {approved_by, approved_on, narration_revision}`; `project.json` → `factual_review: verified`; `narration.voice.pronunciation_review.status: CONFIRMED`.

## Các điểm cần lưu ý (agent tự nêu)

- Năm xây cầu Bollman ở Savage **không** được nói, vì các nguồn không thống nhất (ASCE chỉ chắc chắn về bằng sáng chế 1852; các hồ sơ khác ghi khoảng 1869). Phim chỉ nói 'patented in 1852'.
- 'world's oldest stone railroad span still in service' được gán cho báo cáo năm 2005 ('A national report in 2005 called it…'), không khẳng định cho hiện tại.
- 'America's greatest stone arch' là lời của báo cáo NCHRP, được gán rõ ('What one report calls…').
- Địa danh trong chú thích ảnh (Covington, Virginia; Corinne, Utah; Savage, Maryland) lấy từ tiêu đề hồ sơ HAER/LOC của chính bức ảnh.
- Không có con số về nội lực, sức chịu tải, ứng suất, độ võng hay hệ số an toàn. Các nhịp (30 ft, 220 ft, gần 400 ft) là giá trị NCHRP nêu, vẽ đúng tỉ lệ với nhau.
- Đánh dấu nén/kéo cụ thể chỉ có ở biên trên/biên dưới giàn đơn giản dưới tải hướng xuống (CLM_713); thanh bụng không được tô màu nén/kéo (CLM_714 chỉ nói 'một số').
- Không trình bày ba loại cầu như một chuỗi tiến bộ: B02, B19, B33 nói rõ điều ngược lại.

## Lời dẫn theo câu


### C1 · Hook

**B01** (framing; claim: không, câu dẫn dắt)

- `0:00` One bridge rests on rows of timber posts.
- `0:04` Another leaps the gap in curves of stone.
- `0:07` A third is a lattice of steel triangles.
- `0:11` All three cross exactly the same gap.

**B02** (framing; claim: không, câu dẫn dắt)

- `0:16` So why don't bridges all look the same?
- `0:19` It isn't because one design is simply better than the others.
- `0:24` Each form is a different answer to the same problem, shaped by materials, by the site, and by the time it was built in.


### C2 · The problem every bridge must solve

**B03** (fact; claim: CLM_701, CLM_702)

- `0:34` Every bridge has the same basic job.
- `0:37` It has to carry loads: the traffic crossing it, and the weight of the bridge itself.
- `0:43` And it has to pass all of that down into the ground on either side.
  - CLM_701: SRC_ODOT_MBI Glossary p.365 'live load': "live load - a temporary dynamic load such as vehicular traffic that is applied to a structure" · SRC_ODOT_MBI Glossary p.350 'dead load': "dead load - a static load due to the weight of the structure itself" — giả định: Generic definition of load types; no magnitudes.
  - CLM_702: SRC_ODOT_MBI Glossary p.350 'deck': "deck - that portion of a bridge which provides direct support for vehicular and pedestrian traffic, supported by a superstructure" — giả định: Definition.

**B04** (fact; claim: CLM_702, CLM_703, CLM_704)

- `0:49` Engineers often describe a bridge in two parts.
- `0:53` The superstructure is the part that spans the gap, including the deck.
- `0:59` The substructure is what holds it up: abutments at the ends, and sometimes piers in between.
- `1:06` Load follows a path from the deck, through both parts, into the foundations.
  - CLM_702: SRC_ODOT_MBI Glossary p.350 'deck': "deck - that portion of a bridge which provides direct support for vehicular and pedestrian traffic, supported by a superstructure" — giả định: Definition.
  - CLM_703: SRC_FHWA_PBES_CH2 Chapter 2 introduction (AASHTO definition): "Structural parts of the bridge that provide the horizontal span." · SRC_FHWA_PBES_GLOSSARY Appendix E 'superstructure': "It typically includes beams, girders, trusses, and the bridge deck." — giả định: Definition; the cap beams of a timber bent belong to the substructure (pier cap).
  - CLM_704: SRC_ODOT_MBI Glossary p.383 'substructure': "substructure - the abutments and piers built to support the span of a bridge superstructure" · SRC_ODOT_MBI Glossary p.338 'abutment': "abutment - part of bridge substructure at either end of bridge which transfers loads from superstructure to foundation" · SRC_ODOT_MBI Glossary p.370 'pier': "pier - a substructure unit that supports the spans of a multi-span superstructure at an intermediate location between its abutments" — giả định: Definitions; in the timber model the trestle bents play the role of piers and the banks of the site the role of abutments (illustrative).

**B05** (framing; claim: không, câu dẫn dắt)

- `1:13` What changes from one bridge to the next is how that path is arranged.
- `1:18` So let's start again with an empty gap.


### C3 · The beam

**B06** (fact; claim: CLM_705, CLM_720)

- `1:22` The first answer is the beam.
- `1:25` Lay a strong member across the gap, support it at each end, and you have a bridge.
- `1:31` It is one of the oldest ideas in bridge building.
  - CLM_705: SRC_ODOT_MBI Glossary p.341 'beam': "beam - a linear structural member designed to span from one support to another and support vertical loads" — giả định: Definition.
  - CLM_720: SRC_NCHRP_CONTEXT 3.3.1 Timber Stringer, p. 3-80: "Wood stringer (or beam) bridges are a very old type of design that dates back to the origins of bridge building."

**B07** (fact; claim: CLM_705, CLM_707)

- `1:36` This timber bridge is a row of short beam spans.
- `1:40` Planks form the deck, long beams carry the planks, cap beams carry the beams, and posts carry the caps.
  - CLM_705: SRC_ODOT_MBI Glossary p.341 'beam': "beam - a linear structural member designed to span from one support to another and support vertical loads" — giả định: Definition.
  - CLM_707: SRC_ODOT_MBI Glossary p.344 'cap': "cap - the topmost portion of a pier or a pile bent serving to distribute the loads upon the columns or piles" · SRC_ODOT_MBI Glossary p.341 'bent': "bent - a substructure unit made up of two or more column or column-like members connected at their top-most ends by a cap" · SRC_ODOT_MBI Glossary p.346 'column': "column - a general term applying to a vertical member resisting compressive stresses" — giả định: Definitions; the posts of the illustrative trestle bents are treated as columns.

**B08** (fact; claim: CLM_706, CLM_707)

- `1:49` Each beam carries its load by resisting bending.
- `1:53` At each support, a cap beam spreads the load onto the posts.
- `1:58` The posts then carry it down into the ground in compression.
  - CLM_706: SRC_FHWA_CBM Chapter 2, 'Component Terminology': "As a beam has strength from its bending resistance" · SRC_ODOT_MBI Glossary p.358 'girder': "girder - a horizontal flexural member that is the main or primary support for a structure" — giả định: Qualitative; no stresses, deflections or capacities. The procedural model has not been analysed.
  - CLM_707: SRC_ODOT_MBI Glossary p.344 'cap': "cap - the topmost portion of a pier or a pile bent serving to distribute the loads upon the columns or piles" · SRC_ODOT_MBI Glossary p.341 'bent': "bent - a substructure unit made up of two or more column or column-like members connected at their top-most ends by a cap" · SRC_ODOT_MBI Glossary p.346 'column': "column - a general term applying to a vertical member resisting compressive stresses" — giả định: Definitions; the posts of the illustrative trestle bents are treated as columns.

**B09** (fact; claim: CLM_721, CLM_722)

- `2:04` Beams are simple, and wood was usually easy to find.
- `2:09` That is why timber beam bridges were still being built long after timber trusses fell out of use, and why they are still built on quiet rural roads and in parks today.
- `2:20` But many early timber bridges had relatively short spans, which is why this one needs so many posts.
  - CLM_721: SRC_NCHRP_CONTEXT 3.3.1 Timber Stringer, p. 3-80: "Long after wood truss bridges had ceased to be competitive with metal truss bridges for use in short spans in the nineteenth century, timber beam bridges were still being built. Because of the structure’s simplicity and readily available material (wood), the timber beam has endured to the present day" · SRC_NCHRP_CONTEXT 3.3.1 Timber Stringer, p. 3-80: "Today, these structures are built on low-trafficked, rural backcountry roads, private roads, or in national forests and parks."
  - CLM_722: SRC_NCHRP_CONTEXT 2.2 (North Dakota, quoted), p. 2-9: "Most were built of timber with relatively short spans." — giả định: The quoted passage describes early bridges west of the Mississippi (North Dakota); used only as 'many early timber bridges had relatively short spans'.


### C4 · The arch

**B10** (fact; claim: CLM_708)

- `2:29` A masonry arch takes a different approach.
- `2:32` It is built from wedge-shaped stones called voussoirs, with a keystone at the crown.
  - CLM_708: SRC_ODOT_MBI Glossary p.388 'voussoir': "Voussoir - one of the truncated wedge-shaped stones composing a ring course in a stone arch" · SRC_ODOT_MBI Glossary p.363 'keystone': "keystone - the symmetrically shaped, wedge-like stone located in a head ring course at the crown of an arch" — giả định: Definitions.

**B11** (fact; claim: CLM_709, CLM_710)

- `2:39` The curve turns the downward load into thrust along the arch, pressing the stones together.
- `2:46` So the arch works mainly in compression.
- `2:50` At each end it pushes outward and down on its supports, and the supports push back.
  - CLM_709: SRC_ODOT_MBI Part 2 Ratings, Item 25 Arch, p.144 (manual p.2-56): "The curve converts vertical (gravity) loads within the span to horizontal and vertical thrusts at the spring lines. As a result, the forces within the arch are generally compression" · SRC_ODOT_MBI Glossary p.339 'arch': "arch - a curved structure element primarily in compression that transfers vertical loads through inclined reactions to its end supports" · SRC_YALE_PHYSICS 'Arch Bridges' section: "Arch bridges rely primarily on compression" — giả định: General principle for masonry arches under gravity load; no thrust line, magnitudes or stability assessment of the illustrative model.
  - CLM_710: SRC_ODOT_MBI Glossary p.339 'arch': "transfers vertical loads through inclined reactions to its end supports" · SRC_YALE_PHYSICS 'Arch Bridges' section: "creating two equal and opposite horizontal forces that push inward on the arch" — giả định: Direction only (inclined, upward and inward on the arch); no magnitudes; the arrow is a support REACTION, distinct from the applied load.

**B12** (fact; claim: CLM_726, CLM_709, CLM_710)

- `2:57` That is why arches suit materials that are strong under compression, like stone.
- `3:02` And it is why the supports matter so much: the abutments have to push inward on the arch, against its thrust.
  - CLM_726: SRC_YALE_PHYSICS unit 01.05.08, section 6: "When selecting a building material for an arch bridge, engineers must consider only materials that are strong under compression. These materials include stone, concrete, or steel." — giả định: Educational secondary source (teacher curriculum unit); used for the general principle only.
  - CLM_709: SRC_ODOT_MBI Part 2 Ratings, Item 25 Arch, p.144 (manual p.2-56): "The curve converts vertical (gravity) loads within the span to horizontal and vertical thrusts at the spring lines. As a result, the forces within the arch are generally compression" · SRC_ODOT_MBI Glossary p.339 'arch': "arch - a curved structure element primarily in compression that transfers vertical loads through inclined reactions to its end supports" · SRC_YALE_PHYSICS 'Arch Bridges' section: "Arch bridges rely primarily on compression" — giả định: General principle for masonry arches under gravity load; no thrust line, magnitudes or stability assessment of the illustrative model.
  - CLM_710: SRC_ODOT_MBI Glossary p.339 'arch': "transfers vertical loads through inclined reactions to its end supports" · SRC_YALE_PHYSICS 'Arch Bridges' section: "creating two equal and opposite horizontal forces that push inward on the arch" — giả định: Direction only (inclined, upward and inward on the arch); no magnitudes; the arrow is a support REACTION, distinct from the applied load.

**B13** (fact; claim: CLM_723)

- `3:11` Building an arch takes support of its own.
- `3:15` While a stone arch is being built, a temporary timber frame called falsework holds the stones in place.
- `3:23` So building one called for carpenters as well as skilled masons.
  - CLM_723: SRC_NCHRP_CONTEXT 3.2.1 Stone Arch, p. 3-48: "the skills necessary for erection of falsework to support arch construction (carpentry) and for the laying of stones (masonry) were commonly found within the local labor pool"

**B14** (fact; claim: CLM_724, CLM_725)

- `3:28` Stone arches were generally more expensive to build than timber bridges.
- `3:35` But stone was the preferred choice where durability and permanence were required, so arches were favoured on busy routes and in important places.
- `3:45` Elsewhere, the lower cost of timber made up for its lack of permanence.
  - CLM_724: SRC_NCHRP_CONTEXT 3.2.1 Stone Arch, p. 3-49: "Stone arch bridges were generally more expensive to build than were timber bridges, but their use for roads and highways was favored for heavily traveled routes or locations of high visibility and importance; otherwise, the cost savings of timber bridges tended to offset their relative lack of permanence."
  - CLM_725: SRC_NCHRP_CONTEXT 3.2.1 Stone Arch, p. 3-48: "Stone and wood were often the most readily available building materials for bridges long before fabricated metal was introduced towards the middle of the nineteenth century, and of the two, stone was by far the preferred choice where durability and permanence were required."


### C5 · The truss

**B15** (fact; claim: CLM_711, CLM_712)

- `3:51` A third approach is the truss.
- `3:54` It builds a structure out of straight members, joined into triangles.
- `3:59` Each member is mainly pulled or pushed along its length, in tension or in compression.
  - CLM_711: SRC_ODOT_MBI Glossary p.386 'truss': "truss - a jointed structure made up of individual members primarily carrying axial loads arranged and connected in triangular panels" · SRC_SCI_TRUSSES Introduction: "A truss is essentially a triangulated system of (usually) straight interconnected structural elements" — giả định: Definition.
  - CLM_712: SRC_SCI_TRUSSES Introduction: "The principal force in each element in a truss is axial tension or compression." · SRC_FHWA_CBM Chapter 2, 'Component Terminology': "These axial forces are either compression or tension." — giả định: Idealisation (pinned joints); the source notes real joints are not perfectly pinned. No member-by-member forces are shown.

**B16** (fact; claim: CLM_713, CLM_714)

- `4:07` In a simple span like these, under a downward load, the top chord is squeezed and the bottom chord is stretched.
- `4:15` Inside, some web members are in compression and others are in tension.
  - CLM_713: SRC_FHWA_CBM Chapter 2, 'Component Terminology': "The upper, or top, chords are in compression. The bottom, or lower, chords are in tension." · SRC_SCI_TRUSSES 'Types of trusses': "Under gravity loads, the top and bottom chords of the truss provide the compression and tension resistance to overall bending" — giả định: ASSUMPTION: each truss span of the illustrative model is treated as a simple span (separate truss on its own bearings) carrying a downward load. The FHWA source calls this a simplified characterization for the common single-span bridge; continuous spans behave differently. Qualitative only.
  - CLM_714: SRC_FHWA_CBM Chapter 2, 'Component Terminology': "Some of these web members will usually be in compression; others will consistently be in tension." — giả định: General statement; which web member carries which force is NOT shown (no load case analysed).

**B17** (fact; claim: CLM_727, CLM_728, CLM_711)

- `4:21` The triangles can be arranged in different patterns.
- `4:26` This is a Pratt truss.
- `4:28` In the original design, patented in 1844, its verticals were timber and its diagonals were iron rods.
- `4:38` Swap the web for diagonals that alternate in direction, and you have a Warren truss, patented in 1848.
- `4:46` Both patterns carry load through triangles; they simply arrange the members differently.
  - CLM_727: SRC_NCHRP_CONTEXT 2.2, p. 2-7: "In 1844, Thomas and Caleb Pratt patented the Pratt Truss, which reversed the Howe system and incorporated vertical timber members in compression and diagonal iron rods in tension, a “combination” structure. The structural principle in this design was used well into the twentieth century when all parts were made in steel." — giả định: Historical design description of the 1844 patent; the film does not mark the model's members as in tension or compression.
  - CLM_728: SRC_NCHRP_CONTEXT 2.2, p. 2-7: "the Warren truss was patented by two British engineers, James Warren and Willoughby Monzani. This truss design had alternating diagonals in either tension or compression" — giả định: The model's Warren variant has no verticals; the film says only that the diagonals alternate.
  - CLM_711: SRC_ODOT_MBI Glossary p.386 'truss': "truss - a jointed structure made up of individual members primarily carrying axial loads arranged and connected in triangular panels" · SRC_SCI_TRUSSES Introduction: "A truss is essentially a triangulated system of (usually) straight interconnected structural elements" — giả định: Definition.

**B18** (fact; claim: CLM_729)

- `4:53` Trusses also changed how bridges were built.
- `4:57` By the middle of the nineteenth century, shops were making and drilling truss members, then shipping them to the bridge site, ready to assemble.
- `5:07` And by 1860, the railroads relied almost entirely on these prefabricated parts.
  - CLM_729: SRC_NCHRP_CONTEXT 2.2 'Foundries and Fabricators', p. 2-11: "These shops formed bridge members, drilled the members and assembled and connected the truss members, before packaging and shipping them to the bridge site. By 1860, the railroads were almost exclusively relying on these private concerns to fill their bridge needs with pre-fabricated parts."


### C6 · Why different designs exist

**B19** (framing; claim: không, câu dẫn dắt)

- `5:15` So which design is best?
- `5:18` The honest answer is that it depends.
- `5:21` Materials, the site, the span, cost, and the skills available all pull in different directions.

**B20A** (fact; claim: CLM_726)

- `5:30` Start with the materials themselves.
- `5:33` An arch needs a material that is strong under compression, and stone is.
  - CLM_726: SRC_YALE_PHYSICS unit 01.05.08, section 6: "When selecting a building material for an arch bridge, engineers must consider only materials that are strong under compression. These materials include stone, concrete, or steel." — giả định: Educational secondary source (teacher curriculum unit); used for the general principle only.

**B20B** (fact; claim: CLM_712, CLM_735)

- `5:39` A truss needs members that can work in tension as well as compression.
- `5:45` Wrought iron was valued for exactly that: one historian calls it a material strong equally in tension and in compression.
  - CLM_712: SRC_SCI_TRUSSES Introduction: "The principal force in each element in a truss is axial tension or compression." · SRC_FHWA_CBM Chapter 2, 'Component Terminology': "These axial forces are either compression or tension." — giả định: Idealisation (pinned joints); the source notes real joints are not perfectly pinned. No member-by-member forces are shown.
  - CLM_735: SRC_NCHRP_CONTEXT 2.2, p. 2-8: "realized that a great advantage would be gained by the substitution of wrought iron [for cast iron], a material strong equally in tension and in compression" — giả định: A historian's characterisation (David Plowden) quoted in the report.

**B20C** (fact; claim: CLM_742, CLM_734)

- `5:55` Wood was often plentiful and cheap, but wooden bridges were vulnerable to decay.
  - CLM_742: SRC_NCHRP_CONTEXT 2.2, p. 2-6: "While stone was often used in the East, timber was generally used by the western bridge builders because of the pressure to quickly and economically get new railroads on line, and timber was generally abundant and cheap."
  - CLM_734: SRC_ASCE_BOLLMAN main text: "Replacing wooden bridges, which were cumbersome to build and vulnerable to decay"

**B21** (fact; claim: CLM_733, CLM_746)

- `6:02` That is one reason many timber truss bridges were covered with a roof and siding, to protect them from the weather.
- `6:11` This is the Humpback Covered Bridge, built in 1857 over Dunlap Creek.
  - CLM_733: SRC_NCHRP_CONTEXT 3.1.1 King Post, p. 3-7: "the most common extant king post truss bridges are covered by a roof and siding to protect them from the weather" — giả định: Stated for king post trusses; the film says 'many timber truss bridges'.
  - CLM_746: SRC_NCHRP_CONTEXT List of figures, 3-5: "Humpback Covered Bridge (1857), Humpback Bridge spanning Dunlap" — giả định: Only the name, date and crossing are narrated.

**B22** (fact; claim: CLM_736)

- `6:18` The site of a bridge matters too.
- `6:21` Railway engines have limited traction, so railways need gentle gradients.
- `6:28` Where a valley was too deep and wide to fill with an embankment, engineers built viaducts and trestles to keep the line nearly straight and level.
  - CLM_736: SRC_NCHRP_CONTEXT 3.6 Trestles and Viaducts, p. 3-137: "both have design attributes that were generated by the need of railroad engineers to maintain easy gradients, especially when crossing deep ravines or depressions, to compensate for the limited traction of railroad engines." · SRC_NCHRP_CONTEXT 3.6 Trestles and Viaducts, p. 3-137: "“Viaducts and trestles were the engineering solution for maintaining a nearly straight and horizontal line where the depth and width of the valley or gorge rendered embankments impracticable.”"

**B23** (framing; claim: không, câu dẫn dắt)

- `6:38` Then there is span: how far a single structure has to reach.

**B23B** (fact; claim: CLM_731, CLM_732, CLM_730)

- `6:44` A simple king post truss could span only about thirty feet.
- `6:49` What one report calls America's greatest stone arch, the Cabin John Aqueduct Bridge, spans 220 feet, and some through trusses approach 400.
  - CLM_731: SRC_NCHRP_CONTEXT 3.1.1 King Post, p. 3-7: "Simple king post trusses were used only to span very short distances up to about 30 feet"
  - CLM_732: SRC_NCHRP_CONTEXT 3.2.1 Stone Arch, p. 3-48: "America’s greatest stone arch is the 220-foot span Cabin John Aqueduct Bridge (1864) over Cabin John Creek in suburban Maryland outside Washington, DC. It was the longest arch bridge in the world until 1905."
  - CLM_730: SRC_NCHRP_CONTEXT 3.1 Trusses, p. 3-4: "Through trusses are designed to carry heavier traffic loads than the pony truss and are longer in span, some approaching 400 feet."

**B24** (fact; claim: CLM_738, CLM_739, CLM_727, CLM_728, CLM_729)

- `7:02` Finally, every bridge belongs to its time.
- `7:06` As metal trusses spread, skilled masons became fewer and reinforced concrete arrived, stone arch construction declined.
- `7:15` Then, during the Great Depression, it briefly returned.
  - CLM_738: SRC_NCHRP_CONTEXT 3.2.1 Stone Arch, p. 3-49: "Increased use of metal truss bridges on highways from the late 1800s into the early twentieth century, coupled with a decrease in the number of skilled masons, and advancements in reinforced concrete construction technology in the early decades of the twentieth century, led to a decline in stone arch bridge construction. A brief resurgence in construction of this type occurred during the Great Depression"
  - CLM_739: SRC_NCHRP_CONTEXT 2.2, p. 2-6: "The first major engineered railroad bridge was the Carrollton Viaduct, completed in 1829 across Gwynn’s Falls, west of Baltimore City. Constructed of approximately 12,000 granite blocks, the 312-foot long bridge featured an 80-foot arch over the waterway."
  - CLM_727: SRC_NCHRP_CONTEXT 2.2, p. 2-7: "In 1844, Thomas and Caleb Pratt patented the Pratt Truss, which reversed the Howe system and incorporated vertical timber members in compression and diagonal iron rods in tension, a “combination” structure. The structural principle in this design was used well into the twentieth century when all parts were made in steel." — giả định: Historical design description of the 1844 patent; the film does not mark the model's members as in tension or compression.
  - CLM_728: SRC_NCHRP_CONTEXT 2.2, p. 2-7: "the Warren truss was patented by two British engineers, James Warren and Willoughby Monzani. This truss design had alternating diagonals in either tension or compression" — giả định: The model's Warren variant has no verticals; the film says only that the diagonals alternate.
  - CLM_729: SRC_NCHRP_CONTEXT 2.2 'Foundries and Fabricators', p. 2-11: "These shops formed bridge members, drilled the members and assembled and connected the truss members, before packaging and shipping them to the bridge site. By 1860, the railroads were almost exclusively relying on these private concerns to fill their bridge needs with pre-fabricated parts."


### C7 · Real-world decisions

**B25** (fact; claim: CLM_741, CLM_742)

- `7:20` These trade-offs played out across nineteenth-century America as the railways spread.
- `7:27` In the East, railroads built massive stone viaducts, while western builders generally used timber.
- `7:34` Three documented examples show how differently builders answered.
  - CLM_741: SRC_NCHRP_CONTEXT 2.2, p. 2-6: "The railroad companies revolutionized bridge design, as they required more sophisticated designs and durable materials for carrying the heavy loads of the railcars." · SRC_NCHRP_CONTEXT 2.2, p. 2-6: "In the east, the railroads built massive high and/or long stone viaducts along the Baltimore and Ohio (B&O) Railroad."
  - CLM_742: SRC_NCHRP_CONTEXT 2.2, p. 2-6: "While stone was often used in the East, timber was generally used by the western bridge builders because of the pressure to quickly and economically get new railroads on line, and timber was generally abundant and cheap."

**B26** (fact; claim: CLM_739, CLM_740)

- `7:41` Near Baltimore, the Carrollton Viaduct was completed in 1829.
- `7:47` Built of roughly twelve thousand granite blocks, it carries the railway over Gwynns Falls on an eighty foot arch.
- `7:55` A national report in 2005 called it the world's oldest stone railroad span still in service.
  - CLM_739: SRC_NCHRP_CONTEXT 2.2, p. 2-6: "The first major engineered railroad bridge was the Carrollton Viaduct, completed in 1829 across Gwynn’s Falls, west of Baltimore City. Constructed of approximately 12,000 granite blocks, the 312-foot long bridge featured an 80-foot arch over the waterway."
  - CLM_740: SRC_NCHRP_CONTEXT 3.6 Trestles and Viaducts, p. 3-137: "The earliest stone arch railroad bridge built in the United States, and the world’s oldest stone railroad span still in service, is the Carrollton Viaduct over Gwynn’s Falls on the old B & O Railroad line near Baltimore, Maryland. Completed in 1829, this National Historic Landmark" — giả định: 'Still in service' is as of the 2005 report; the film attributes it to the report.

**B27** (interpretation; claim: CLM_741, CLM_725)

- `8:04` Early railroads needed durable bridges to carry heavy trains.
- `8:09` For a line meant to last, stone was the answer.
  - CLM_741: SRC_NCHRP_CONTEXT 2.2, p. 2-6: "The railroad companies revolutionized bridge design, as they required more sophisticated designs and durable materials for carrying the heavy loads of the railcars." · SRC_NCHRP_CONTEXT 2.2, p. 2-6: "In the east, the railroads built massive high and/or long stone viaducts along the Baltimore and Ohio (B&O) Railroad."
  - CLM_725: SRC_NCHRP_CONTEXT 3.2.1 Stone Arch, p. 3-48: "Stone and wood were often the most readily available building materials for bridges long before fabricated metal was introduced towards the middle of the nineteenth century, and of the two, stone was by far the preferred choice where durability and permanence were required."

**B28** (fact; claim: CLM_742, CLM_743)

- `8:14` In the West, the pressure was different.
- `8:17` Railroads had to open new lines quickly and economically, and timber was abundant and cheap.
- `8:24` This timber trestle near Corinne, Utah, was built in 1872 by the Central Pacific Railroad.
  - CLM_742: SRC_NCHRP_CONTEXT 2.2, p. 2-6: "While stone was often used in the East, timber was generally used by the western bridge builders because of the pressure to quickly and economically get new railroads on line, and timber was generally abundant and cheap."
  - CLM_743: SRC_NCHRP_CONTEXT List of figures, 3-106: "Promontory Route Railroad Trestles 790B (1872), Corinne vicinity, Box Elder County, Utah. This nineteenth century structure was built by the Central Pacific Railroad Company."

**B29** (interpretation; claim: CLM_737)

- `8:34` A trestle is a succession of towers supporting short spans.
- `8:39` It is the same beam idea as our timber model, repeated as often as the crossing needs.
  - CLM_737: SRC_NCHRP_CONTEXT 3.6 Trestles and Viaducts, p. 3-137: "a trestle consists of a succession of towers of steel, timber, or reinforced concrete, supporting short spans"

**B30** (fact; claim: CLM_744, CLM_745)

- `8:46` Iron offered a third path.
- `8:49` The Bollman truss, patented in 1852, was one of the first designs to use iron in all of its essential structural parts.
- `8:59` It could be built relatively quickly and inexpensively, while offering the long-lasting qualities of metal.
- `9:07` The bridge at Savage, Maryland, is the only remaining example of the design.
  - CLM_744: SRC_ASCE_BOLLMAN main text: "patented in 1852 and one of the first to use iron exclusively in all essential structural elements" · SRC_ASCE_BOLLMAN main text: "the Bollman Truss Bridge could be built relatively quickly and inexpensively, while providing the long-lasting qualities associated with metal."
  - CLM_745: SRC_ASCE_BOLLMAN main text: "The Bollman Truss Bridge is the only remaining example of a patented design that was used extensively on the Baltimore & Ohio and other railroads."

**B31** (interpretation; claim: CLM_741, CLM_742, CLM_744)

- `9:14` Stone for permanence, timber for speed and economy, and iron trusses that offered some of both.
- `9:21` Three places, three sets of constraints, three different bridges.
  - CLM_741: SRC_NCHRP_CONTEXT 2.2, p. 2-6: "The railroad companies revolutionized bridge design, as they required more sophisticated designs and durable materials for carrying the heavy loads of the railcars." · SRC_NCHRP_CONTEXT 2.2, p. 2-6: "In the east, the railroads built massive high and/or long stone viaducts along the Baltimore and Ohio (B&O) Railroad."
  - CLM_742: SRC_NCHRP_CONTEXT 2.2, p. 2-6: "While stone was often used in the East, timber was generally used by the western bridge builders because of the pressure to quickly and economically get new railroads on line, and timber was generally abundant and cheap."
  - CLM_744: SRC_ASCE_BOLLMAN main text: "patented in 1852 and one of the first to use iron exclusively in all essential structural elements" · SRC_ASCE_BOLLMAN main text: "the Bollman Truss Bridge could be built relatively quickly and inexpensively, while providing the long-lasting qualities associated with metal."


### C8 · Why they look different

**B32** (interpretation; claim: CLM_706, CLM_709, CLM_712)

- `9:27` So why don't bridges all look the same?
- `9:30` Because a bridge's form comes from two things working together.
- `9:35` One is how its structure carries load: beams resist bending, arches work in compression, and trusses share load among members in tension and compression.
  - CLM_706: SRC_FHWA_CBM Chapter 2, 'Component Terminology': "As a beam has strength from its bending resistance" · SRC_ODOT_MBI Glossary p.358 'girder': "girder - a horizontal flexural member that is the main or primary support for a structure" — giả định: Qualitative; no stresses, deflections or capacities. The procedural model has not been analysed.
  - CLM_709: SRC_ODOT_MBI Part 2 Ratings, Item 25 Arch, p.144 (manual p.2-56): "The curve converts vertical (gravity) loads within the span to horizontal and vertical thrusts at the spring lines. As a result, the forces within the arch are generally compression" · SRC_ODOT_MBI Glossary p.339 'arch': "arch - a curved structure element primarily in compression that transfers vertical loads through inclined reactions to its end supports" · SRC_YALE_PHYSICS 'Arch Bridges' section: "Arch bridges rely primarily on compression" — giả định: General principle for masonry arches under gravity load; no thrust line, magnitudes or stability assessment of the illustrative model.
  - CLM_712: SRC_SCI_TRUSSES Introduction: "The principal force in each element in a truss is axial tension or compression." · SRC_FHWA_CBM Chapter 2, 'Component Terminology': "These axial forces are either compression or tension." — giả định: Idealisation (pinned joints); the source notes real joints are not perfectly pinned. No member-by-member forces are shown.

**B32B** (interpretation; claim: CLM_742, CLM_724)

- `9:47` The other is the world it was built in: its materials, its site, its span, its budget and its builders.
  - CLM_742: SRC_NCHRP_CONTEXT 2.2, p. 2-6: "While stone was often used in the East, timber was generally used by the western bridge builders because of the pressure to quickly and economically get new railroads on line, and timber was generally abundant and cheap."
  - CLM_724: SRC_NCHRP_CONTEXT 3.2.1 Stone Arch, p. 3-49: "Stone arch bridges were generally more expensive to build than were timber bridges, but their use for roads and highways was favored for heavily traveled routes or locations of high visibility and importance; otherwise, the cost savings of timber bridges tended to offset their relative lack of permanence."

**B33** (interpretation; claim: CLM_721, CLM_738)

- `9:56` And it is not a simple story of progress.
- `10:00` Timber beam bridges are still built today, and stone arches briefly returned during the Great Depression.
- `10:07` Each form can still be the right answer in the right place.
  - CLM_721: SRC_NCHRP_CONTEXT 3.3.1 Timber Stringer, p. 3-80: "Long after wood truss bridges had ceased to be competitive with metal truss bridges for use in short spans in the nineteenth century, timber beam bridges were still being built. Because of the structure’s simplicity and readily available material (wood), the timber beam has endured to the present day" · SRC_NCHRP_CONTEXT 3.3.1 Timber Stringer, p. 3-80: "Today, these structures are built on low-trafficked, rural backcountry roads, private roads, or in national forests and parks."
  - CLM_738: SRC_NCHRP_CONTEXT 3.2.1 Stone Arch, p. 3-49: "Increased use of metal truss bridges on highways from the late 1800s into the early twentieth century, coupled with a decrease in the number of skilled masons, and advancements in reinforced concrete construction technology in the early decades of the twentieth century, led to a decline in stone arch bridge construction. A brief resurgence in construction of this type occurred during the Great Depression"

**B34** (framing; claim: không, câu dẫn dắt)

- `10:13` Next time you cross a bridge, look at its shape.
- `10:17` It shows how the load reaches the ground, and something about the people who built it.
- `10:23` These models are illustrations, not engineering designs, and the arrows show ideas, not calculated forces.

**B35** (framing; claim: không, câu dẫn dắt)

- `10:33` Thank you very much for watching.
- `10:36` The sources and photo credits are listed in the description.

## Bộ kiểm nhất quán lời/hình: cần người duyệt xác nhận

- B33.s2 (SIDE, UNCERTAIN): "Each form can still be the right answer in the right place." — left/right wording; no annotation to locate - confirm the referent in review
- B34.s2 (ARROWS, UNCERTAIN): "These models are illustrations, not engineering designs, and the arrows show ideas, not calculated forces." — generic reference to the arrows (shown in earlier beats); editorial check

## Chữ trên card

- **SC_005** (B02): Why Bridges Don't All Look the Same | Same problem. Different answers. | Materials | Site | Time
- **SC_019** (B13): Conceptual diagram — not to scale | Keystone | Falsework (temporary) | Carpenters build the frame | Masons lay the stones
- **SC_020** (B14): A trade-off | Timber beam | Stone arch | Cost to build | lower | higher | Permanence | lower | higher | Favoured for | other crossings | busy, important routes | Lower cost made up for less permanence | After NCHRP 25-25(15), 2005
- **SC_027** (B19): 6 · Why different designs exist | Which design is best? | It depends. | Materials | Site | Span | Cost | Skills
- **SC_031** (B21): Humpback Covered Bridge | Roof and siding protect | the timber trusses | Dunlap Creek, built 1857 | Covington, Virginia | Photo: Jack E. Boucher, HAER, Library of Congress (public domain)
- **SC_032** (B22): Schematic — not to scale | Down and up again: too steep for trains | A viaduct keeps the line nearly level
- **SC_034** (B23B): How far one structure can reach | Simple king post truss: about 30 ft | Cabin John Aqueduct, stone arch (1864): 220 ft | Some through trusses: approaching 400 ft | Spans as given in NCHRP 25-25(15), 2005 — bars to scale
- **SC_035** (B24): 1820 | 1840 | 1860 | 1880 | 1900 | 1920 | 1940 | 1829  Carrollton Viaduct (stone) | 1844  Pratt truss patented | 1848  Warren truss patented | 1860  Prefabricated truss parts | Metal trusses spread; stone arches decline | Great Depression: stone arches return
- **SC_036** (B25): 7 · Real-world decisions | WEST | EAST | United States — schematic, not to scale | Timber, built fast | Massive stone viaducts | Corinne, Utah | Baltimore | Savage, Maryland
- **SC_037** (B26): Carrollton Viaduct | Baltimore, Maryland | completed 1829 | about 12,000 granite blocks | 80 ft arch over Gwynns Falls | Photo: William E. Barrett, HAER, Library of Congress (public domain)
- **SC_039** (B28): Promontory Route trestle | Timber: abundant, cheap | and quick to build | near Corinne, Utah | Central Pacific, 1872 | Photo: HAER, Library of Congress (public domain)
- **SC_041** (B30): Bollman Truss Bridge | Patented 1852 | iron in all essential parts | quick, inexpensive, | long-lasting | Savage, Maryland | Photo: William E. Barrett, HAER, Library of Congress (public domain)
- **SC_042** (B31): Stone: permanence | Timber: speed and economy | Iron: some of both | Three places, three sets of constraints | Photos: HAER, Library of Congress (public domain)
- **SC_044** (B32B): 2 · The world it was built in | Materials | Site | Span | Budget | Builders
- **SC_045** (B33): 1820 | 1840 | 1860 | 1880 | 1900 | 1920 | 1940 | 1829  Carrollton Viaduct (stone) | 1844  Pratt truss patented | 1848  Warren truss patented | 1860  Prefabricated truss parts | Stone arches return briefly | Today: timber beam bridges | are still built on quiet roads
- **SC_047** (B35): Why Bridges Don't All Look the Same | Archival photographs: Historic American Engineering Record, | Library of Congress Prints & Photographs Division (public domain) | Sources: TRB NCHRP 25-25(15); FHWA; Ohio DOT; ASCE; | SteelConstruction.info; Yale-New Haven Teachers Institute | 3D models and diagrams are illustrative, not engineering designs | Architecture Story Studio

## Chú thích trên cảnh 3D

- B03 `B03_ch` NOTE: "2 · The problem every bridge must solve"
- B03 `B03_load` LOAD_ARROW: "Load" (CLM_701)
- B03 `B03_ground` COMPONENT_LABEL: "Ground"
- B04 `B04_super` HIGHLIGHT_REGION: "Superstructure" (CLM_703)
- B04 `B04_abut` COMPONENT_LABEL: "Abutment" (CLM_704)
- B04 `B04_pier` COMPONENT_LABEL: "Pier" (CLM_704)
- B04 `B04_found` COMPONENT_LABEL: "Foundation" (CLM_704)
- B06 `B06_ch` NOTE: "3 · The beam"
- B08 `B08_load` LOAD_ARROW: "Load" (CLM_701)
- B08 `B08_bend` CALLOUT: "Beam resists bending" (CLM_706)
- B08 `B08_cap` COMPONENT_LABEL: "Cap beam" (CLM_707)
- B08 `B08_posts` CALLOUT: "Posts: compression" (CLM_707)
- B09 `B09_note` NOTE: "Illustrative model"
- B10 `B10_ch` NOTE: "4 · The arch"
- B10 `B10_vous` COMPONENT_LABEL: "Voussoirs" (CLM_708)
- B10 `B10_key` COMPONENT_LABEL: "Keystone" (CLM_708)
- B11 `B11_load` LOAD_ARROW: "Load" (CLM_709)
- B11 `B11_comp` CALLOUT: "Mainly compression" (CLM_709)
- B11 `B11_react` REACTION_ARROW: "Supports push back" (CLM_710)
- B12 `B12_abut` COMPONENT_LABEL: "Abutment" (CLM_710)
- B12 `B12_pier` COMPONENT_LABEL: "Pier" (CLM_710)
- B15 `B15_ch` NOTE: "5 · The truss"
- B15 `B15_joints` COMPONENT_LABEL: "Joints" (CLM_711)
- B16 `B16_top` CALLOUT: "Top chord: compression" (CLM_713)
- B16 `B16_bottom` CALLOUT: "Bottom chord: tension" (CLM_713)
- B16 `B16_web` COMPONENT_LABEL: "Web members" (CLM_714)
- B17 `B17_pratt` NOTE: "Pratt truss (patented 1844)" (CLM_727)
- B17 `B17_warren` NOTE: "Warren truss (patented 1848)" (CLM_728)
- B18 `B18_shop` NOTE: "Members made and drilled in shops" (CLM_729)
- B18 `B18_1860` NOTE: "By 1860: prefabricated parts" (CLM_729)
- B20A `B20A_note` NOTE: "Stone: strong under compression"
- B20B `B20B_note` NOTE: "Truss members: tension and compression"
- B20B `B20B_iron` NOTE: "Wrought iron: valued in tension and compression" (CLM_735)
- B20C `B20C_note` NOTE: "Timber: plentiful and cheap, but it decays"
- B23 `B23_note` NOTE: "Span: how far one structure reaches"
- B27 `B27_note` NOTE: "Illustrative model, not the Carrollton Viaduct"
- B29 `B29_note` NOTE: "Illustrative model, not the Promontory trestle"
- B32 `B32_ch` NOTE: "8 · Why they look different"
- B32 `B32_one` NOTE: "1 · How the structure carries load"
- B34 `B34_note` NOTE: "Models are illustrations, not engineering designs"

## Bản ghi sửa câu (ASR / tốc độ đọc)

- B18.s2: "By 1860, railroads relied almost entirely on these prefabricated parts." → "And by 1860, the railroads relied almost entirely on these prefabricated parts." (bm_george spoke it at 1.47 written words/s (below the 1.5 truncation guard; ASR text was exact))
- B20.s0: "Start with materials." → "Start with the materials themselves." (very short sentence: trailing silence put it under the 1.5 words/s guard)
- B22.s0: "The site matters too." → "The site of a bridge matters too." (very short sentence: trailing silence put it under the 1.5 words/s guard)
- B35.s0: "Thanks for watching." → "Thank you very much for watching." (very short sentence: trailing silence put it under the 1.5 words/s guard)
- B15.s0: "The truss takes yet another approach." → "A third approach is the truss." (ASR heard 'The Trust takes' (WER 0.17))
- B23.s2: "spans two hundred and twenty feet, and some through trusses approach four hundred." → "spans 220 feet, and some through trusses approach 400." (numbers written as digits so the subtitles read '220' and ASR text matches (WER 0.23 from spelled-out numbers))
- B20B.s0-s1: "A truss needs members that can work in tension as well as compression, and wrought iron was valued for exactly that: one historian calls it a material strong equally in tension and in compression." → "A truss needs members that can work in tension as well as compression. Wrought iron was valued for exactly that: one historian calls it a material strong equally in tension and in compression." (split in two so the picture can change with the second idea (15 s single-sentence hold))
- B35.s1: "(none)" → "The sources and photo credits are listed in the description." (rough-cut review: the 6-line credits card was on screen for 4 s only)
