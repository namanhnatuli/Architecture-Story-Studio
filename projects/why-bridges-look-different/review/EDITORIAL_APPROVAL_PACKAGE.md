# Gói duyệt biên tập: "Why Bridges Don't All Look the Same" (narration `m8-r3`)

> **Đang chờ duyệt.** Agent soạn gói này nhưng không tự duyệt claim, giọng hay phát âm. Tới khi chủ kênh duyệt, mọi bản dựng mang nhãn INTERNAL REVIEW.

## Cần chủ kênh quyết định

1. Lời dẫn: mỗi câu đúng với claim nó trích (xem cột trích dẫn nguồn).
2. Chữ trên card: tiêu đề, nhãn, chú thích ảnh, thang nhịp và dòng thời gian.
3. Ảnh lưu trữ: chọn ảnh, cách cắt viền phim, dòng ghi công (xem `review/RIGHTS_PROVENANCE.md`).
4. Nhãn 'Illustrative model' trên các mô hình 3D (B09, B41, B45, B50, B20E, B22C, B22D, B23D, B27, B29, B31A, B31B, B31D).
5. Phát âm các tên mới (narration.voice.pronunciation_review.terms).
6. Giọng: duyệt `am_michael` hiện có (Tran Nam Anh (channel owner), 2026-10-30; theo dự án) vẫn áp dụng cho revision này: xác nhận lại hoặc rút.

Cách ghi quyết định (agent chỉ ghi lại lời chủ kênh; xem `docs/production/NEW_DOCUMENTARY_PLAYBOOK.md` bước 23): `research/editorial_approval.json` (id claim, `claims_text_sha256`, `narration_revision` của revision này), rồi chạy `research/build_sources.py`; `project.json` → `factual_review: verified`; `narration.voice.pronunciation_review` (`ACCEPTED_BY_OWNER` hoặc `CONFIRMED`, gắn với hash audio); `review/OWNER_APPROVALS.json`.

## Các điểm cần lưu ý (agent tự nêu)

- Năm xây cầu Bollman ở Savage **không** được nói, vì các nguồn không thống nhất (ASCE chỉ chắc chắn về bằng sáng chế 1852; các hồ sơ khác ghi khoảng 1869). Phim chỉ nói 'patented in 1852'.
- 'world's oldest stone railroad span still in service' được gán cho báo cáo năm 2005 ('A national report in 2005 called it…'), không khẳng định cho hiện tại.
- 'America's greatest stone arch' (M7) đã bỏ khỏi m8-r1 cùng card thanh nhịp B23B.
- Lời đánh giá về cầu Brooklyn ('few suspension bridges since can claim to stand entirely clear of its shadow') là của báo cáo NCHRP, được gán rõ ('one report says').
- Địa danh trong chú thích ảnh (Covington, Virginia; Corinne, Utah; Savage, Maryland; East River, New York) lấy từ tiêu đề hồ sơ HAER/LOC của chính bức ảnh.
- Không có con số về nội lực, sức chịu tải, ứng suất, độ võng hay hệ số an toàn. Các số trong phim gồm:
  - nhịp "200 to 300 feet" (NCHRP §3.7);
  - 750 ft, 1.200 ft, 3.000 ft (FHWA 2012, kinh tế nhịp lớn ở Mỹ);
  - năm 1883 và 1909.
- Đánh dấu nén/kéo:
  - Biên trên/biên dưới giàn đơn giản dưới tải hướng xuống (CLM_713). Thanh bụng không được tô màu (CLM_714 chỉ nói 'một số').
  - Cáp cầu treo chịu kéo, tháp chịu nén (CLM_760, NCHRP nguyên văn).
  - Mặt cầu dây văng bị nén dọc (CLM_773, FHWA).
  - **Dây văng không được gắn nhãn kéo:** không có câu nguyên văn nào trong bộ nguồn nói điều đó.
- **Mô hình nhịp lớn không theo tỉ lệ thật.** Chúng đặt trên một khúc sông 72 m minh họa; cầu thật dài hàng trăm đến hàng nghìn mét. NOTE ở B40 ghi "A wider crossing (illustrative, not to scale)".
- **Cầu Queensboro thật không có nhịp treo ở giữa** (NCHRP §3.7: "It had no central suspended span"). Phim không nói nó có, nhưng mô hình minh họa có nhịp treo xuất hiện ngay trước ảnh. Người duyệt có thể muốn thêm một NOTE.
- Nguồn FHWA-IF-12-052 (2012) là bản lưu Internet Archive của URL FHWA (URL gốc nay trả 404). Các nhận định kinh tế được nói là "by 2012, a federal handbook said…", không khẳng định cho hiện tại.
- "Since 1980, almost every American bridge with a main span over 1,000 feet has been cable-stayed" (CLM_774, FHWA 2012). Bỏ ở m8-r1; có lại ở m8-r2 (dòng thời gian B24B và B31D, câu "Today, the long-span answer in America is usually cable-stayed").
- Không trình bày các loại cầu như một chuỗi tiến bộ:
  - B02, B19, B33 nói rõ điều ngược lại;
  - B33 thêm "the most common steel bridge today is still a kind of beam" (CLM_777, FHWA 2012).
- **m8-r2 (yêu cầu của chủ kênh, 2026-11-03):** các chương 9–12 nay nói cả về công-xôn, cầu treo và dây văng.
  - **Tacoma Narrows (1940)** chỉ được kể bằng lời, kèm hình giàn tăng cứng trên mô hình. Không có hình sập hay cảnh phá hủy. Nguồn: NCHRP §2.2 và FHWA §2.6 ("only moderately high winds").
  - **"133 years before another suspension bridge was built for railway traffic"** và **"only as good as the weakest link"** là lời của báo cáo NCHRP. Lời dẫn nói rõ "critics said…" và "Their doubts were not unjustified…", đúng theo nguồn.
  - **"Cantilevers, by contrast, were first used by the railroads"**: nguồn không nói đường sắt chọn công-xôn *vì* cầu treo bị nghi ngờ. Lời dẫn chỉ đặt hai sự thật cạnh nhau.
  - **Penobscot Narrows:** số liệu (nhịp 1.161 ft, tháp 430 ft, 42 tháng, thông xe 2006, đài quan sát) lấy từ FHWA-HRT-14-067 (2014).
  - **Dải nhịp (card B23C):** dải kinh tế cho cầu **thép** theo FHWA 2012, không phải giới hạn tuyệt đối. Thanh "Cantilever truss" chỉ có mũi tên ("considerably farther"), không có điểm cuối, vì nguồn không cho con số.
  - **Card nền đất (B22B)** là sơ đồ, không theo tỉ lệ. Ý của nó chỉ là: cầu treo cần neo vào khối lớn hoặc đá gốc (CLM_761); tháp cầu dây văng dựng được ở nơi đá không gần mặt đất (CLM_776).
  - **Thời lượng 19,3 phút** theo quyết định của chủ kênh: không giữ khắt khe giới hạn 15 phút. Trần 20 phút là agent đặt (`project.json` → `runtime_decision`).

## Lời dẫn theo câu


### C1 · Hook

**B01** (framing; claim: không, câu dẫn dắt)

- `0:00` One bridge rests on rows of timber posts.
- `0:04` Another leaps the gap in curves of stone.
- `0:07` A third is a lattice of steel triangles.
- `0:11` All three cross exactly the same gap.

**B01B** (framing; claim: không, câu dẫn dắt)

- `0:16` Over wider water, the answers change again.
- `0:20` One bridge reaches out from its piers.

**B01C** (framing; claim: không, câu dẫn dắt)

- `0:24` Another hangs from huge draped cables.

**B01D** (framing; claim: không, câu dẫn dắt)

- `0:29` A third is held up by straight lines of steel.

**B02** (framing; claim: không, câu dẫn dắt)

- `0:33` So why don't bridges all look the same?
- `0:37` It isn't because one design is simply better than the others.
- `0:41` Each form is a different answer to the same problem, shaped by materials, by the site, by the span, and by the time it was built in.


### C2 · The problem every bridge must solve

**B03** (fact; claim: CLM_701, CLM_702)

- `0:52` Every bridge has the same basic job.
- `0:56` It has to carry loads: the traffic crossing it, and the weight of the bridge itself.
- `1:02` And it has to pass all of that down through its supports into the ground.
  - CLM_701: SRC_ODOT_MBI Glossary p.365 'live load': "live load - a temporary dynamic load such as vehicular traffic that is applied to a structure" · SRC_ODOT_MBI Glossary p.350 'dead load': "dead load - a static load due to the weight of the structure itself" — giả định: Generic definition of load types; no magnitudes.
  - CLM_702: SRC_ODOT_MBI Glossary p.350 'deck': "deck - that portion of a bridge which provides direct support for vehicular and pedestrian traffic, supported by a superstructure" — giả định: Definition.

**B04** (fact; claim: CLM_702, CLM_703, CLM_704)

- `1:08` Engineers often describe a bridge in two parts.
- `1:12` The superstructure is the part that spans the gap, including the deck.
- `1:18` The substructure is what holds it up: abutments at the ends, and sometimes piers in between.
- `1:25` Load follows a path from the deck, through both parts, into the foundations.
  - CLM_702: SRC_ODOT_MBI Glossary p.350 'deck': "deck - that portion of a bridge which provides direct support for vehicular and pedestrian traffic, supported by a superstructure" — giả định: Definition.
  - CLM_703: SRC_FHWA_PBES_CH2 Chapter 2 introduction (AASHTO definition): "Structural parts of the bridge that provide the horizontal span." · SRC_FHWA_PBES_GLOSSARY Appendix E 'superstructure': "It typically includes beams, girders, trusses, and the bridge deck." — giả định: Definition; the cap beams of a timber bent belong to the substructure (pier cap).
  - CLM_704: SRC_ODOT_MBI Glossary p.383 'substructure': "substructure - the abutments and piers built to support the span of a bridge superstructure" · SRC_ODOT_MBI Glossary p.338 'abutment': "abutment - part of bridge substructure at either end of bridge which transfers loads from superstructure to foundation" · SRC_ODOT_MBI Glossary p.370 'pier': "pier - a substructure unit that supports the spans of a multi-span superstructure at an intermediate location between its abutments" — giả định: Definitions; in the timber model the trestle bents play the role of piers and the banks of the site the role of abutments (illustrative).

**B05** (framing; claim: không, câu dẫn dắt)

- `1:31` What changes from one bridge to the next is how that path is arranged.
- `1:37` So let's start again with an empty gap.


### C3 · The beam

**B06** (fact; claim: CLM_705, CLM_720)

- `1:41` The first answer is the beam.
- `1:44` Lay a strong member across the gap, support it at each end, and you have a bridge.
- `1:50` It is one of the oldest ideas in bridge building.
  - CLM_705: SRC_ODOT_MBI Glossary p.341 'beam': "beam - a linear structural member designed to span from one support to another and support vertical loads" — giả định: Definition.
  - CLM_720: SRC_NCHRP_CONTEXT 3.3.1 Timber Stringer, p. 3-80: "Wood stringer (or beam) bridges are a very old type of design that dates back to the origins of bridge building."

**B07** (fact; claim: CLM_705, CLM_707)

- `1:55` This timber bridge is a row of short beam spans.
- `1:59` Planks form the deck, long beams carry the planks, cap beams carry the beams, and posts carry the caps.
  - CLM_705: SRC_ODOT_MBI Glossary p.341 'beam': "beam - a linear structural member designed to span from one support to another and support vertical loads" — giả định: Definition.
  - CLM_707: SRC_ODOT_MBI Glossary p.344 'cap': "cap - the topmost portion of a pier or a pile bent serving to distribute the loads upon the columns or piles" · SRC_ODOT_MBI Glossary p.341 'bent': "bent - a substructure unit made up of two or more column or column-like members connected at their top-most ends by a cap" · SRC_ODOT_MBI Glossary p.346 'column': "column - a general term applying to a vertical member resisting compressive stresses" — giả định: Definitions; the posts of the illustrative trestle bents are treated as columns.

**B08** (fact; claim: CLM_706, CLM_707)

- `2:08` Each beam carries its load by resisting bending.
- `2:12` At each support, a cap beam spreads the load onto the posts.
- `2:17` The posts then carry it down into the ground in compression.
  - CLM_706: SRC_FHWA_CBM Chapter 2, 'Component Terminology': "As a beam has strength from its bending resistance" · SRC_ODOT_MBI Glossary p.358 'girder': "girder - a horizontal flexural member that is the main or primary support for a structure" — giả định: Qualitative; no stresses, deflections or capacities. The procedural model has not been analysed.
  - CLM_707: SRC_ODOT_MBI Glossary p.344 'cap': "cap - the topmost portion of a pier or a pile bent serving to distribute the loads upon the columns or piles" · SRC_ODOT_MBI Glossary p.341 'bent': "bent - a substructure unit made up of two or more column or column-like members connected at their top-most ends by a cap" · SRC_ODOT_MBI Glossary p.346 'column': "column - a general term applying to a vertical member resisting compressive stresses" — giả định: Definitions; the posts of the illustrative trestle bents are treated as columns.

**B09** (fact; claim: CLM_721, CLM_722)

- `2:23` Beams are simple, and wood was usually easy to find.
- `2:28` That is why timber beam bridges were still being built long after timber trusses stopped being competitive, and in 2005 a national report found them still being built on quiet rural roads and in parks.
- `2:42` But many early timber bridges had relatively short spans, which is why this one needs so many posts.
  - CLM_721: SRC_NCHRP_CONTEXT 3.3.1 Timber Stringer, p. 3-80: "Long after wood truss bridges had ceased to be competitive with metal truss bridges for use in short spans in the nineteenth century, timber beam bridges were still being built. Because of the structure’s simplicity and readily available material (wood), the timber beam has endured to the present day" · SRC_NCHRP_CONTEXT 3.3.1 Timber Stringer, p. 3-80: "Today, these structures are built on low-trafficked, rural backcountry roads, private roads, or in national forests and parks."
  - CLM_722: SRC_NCHRP_CONTEXT 2.2 (North Dakota, quoted), p. 2-9: "Most were built of timber with relatively short spans." — giả định: The quoted passage describes early bridges west of the Mississippi (North Dakota); used only as 'many early timber bridges had relatively short spans'.


### C4 · The arch

**B10** (fact; claim: CLM_708)

- `2:51` A masonry arch takes a different approach.
- `2:54` It is built from wedge-shaped stones called voussoirs, with a keystone at the crown.
  - CLM_708: SRC_ODOT_MBI Glossary p.388 'voussoir': "Voussoir - one of the truncated wedge-shaped stones composing a ring course in a stone arch" · SRC_ODOT_MBI Glossary p.363 'keystone': "keystone - the symmetrically shaped, wedge-like stone located in a head ring course at the crown of an arch" — giả định: Definitions.

**B11** (fact; claim: CLM_709, CLM_710)

- `3:01` The curve turns the downward load into thrust along the arch, pressing the stones together.
- `3:08` So the arch works mainly in compression.
- `3:12` At each end it pushes outward and down on its supports, and the supports push back.
  - CLM_709: SRC_ODOT_MBI Part 2 Ratings, Item 25 Arch, p.144 (manual p.2-56): "The curve converts vertical (gravity) loads within the span to horizontal and vertical thrusts at the spring lines. As a result, the forces within the arch are generally compression" · SRC_ODOT_MBI Glossary p.339 'arch': "arch - a curved structure element primarily in compression that transfers vertical loads through inclined reactions to its end supports" · SRC_YALE_PHYSICS 'Arch Bridges' section: "Arch bridges rely primarily on compression" — giả định: General principle for masonry arches under gravity load; no thrust line, magnitudes or stability assessment of the illustrative model.
  - CLM_710: SRC_ODOT_MBI Glossary p.339 'arch': "transfers vertical loads through inclined reactions to its end supports" · SRC_YALE_PHYSICS 'Arch Bridges' section: "creating two equal and opposite horizontal forces that push inward on the arch" — giả định: Direction only (inclined, upward and inward on the arch); no magnitudes; the arrow is a support REACTION, distinct from the applied load.

**B12** (fact; claim: CLM_726, CLM_709, CLM_710)

- `3:19` That is why arches suit materials that are strong under compression, like stone.
- `3:24` And it is why the supports matter so much: the abutments have to push inward on the arch, against its thrust.
  - CLM_726: SRC_YALE_PHYSICS unit 01.05.08, section 6: "When selecting a building material for an arch bridge, engineers must consider only materials that are strong under compression. These materials include stone, concrete, or steel." — giả định: Educational secondary source (teacher curriculum unit); used for the general principle only.
  - CLM_709: SRC_ODOT_MBI Part 2 Ratings, Item 25 Arch, p.144 (manual p.2-56): "The curve converts vertical (gravity) loads within the span to horizontal and vertical thrusts at the spring lines. As a result, the forces within the arch are generally compression" · SRC_ODOT_MBI Glossary p.339 'arch': "arch - a curved structure element primarily in compression that transfers vertical loads through inclined reactions to its end supports" · SRC_YALE_PHYSICS 'Arch Bridges' section: "Arch bridges rely primarily on compression" — giả định: General principle for masonry arches under gravity load; no thrust line, magnitudes or stability assessment of the illustrative model.
  - CLM_710: SRC_ODOT_MBI Glossary p.339 'arch': "transfers vertical loads through inclined reactions to its end supports" · SRC_YALE_PHYSICS 'Arch Bridges' section: "creating two equal and opposite horizontal forces that push inward on the arch" — giả định: Direction only (inclined, upward and inward on the arch); no magnitudes; the arrow is a support REACTION, distinct from the applied load.

**B13** (fact; claim: CLM_723)

- `3:33` Building an arch takes support of its own.
- `3:37` While a stone arch is being built, a temporary timber frame called falsework holds the stones in place.
- `3:45` So building one called for carpenters as well as skilled masons.
  - CLM_723: SRC_NCHRP_CONTEXT 3.2.1 Stone Arch, p. 3-48: "the skills necessary for erection of falsework to support arch construction (carpentry) and for the laying of stones (masonry) were commonly found within the local labor pool"

**B14** (fact; claim: CLM_724, CLM_725)

- `3:50` Stone arches were generally more expensive to build than timber bridges.
- `3:56` But stone was the preferred choice where durability and permanence were required, so arches were favoured on busy routes and in important places.
- `4:07` Elsewhere, the lower cost of timber made up for its lack of permanence.
  - CLM_724: SRC_NCHRP_CONTEXT 3.2.1 Stone Arch, p. 3-49: "Stone arch bridges were generally more expensive to build than were timber bridges, but their use for roads and highways was favored for heavily traveled routes or locations of high visibility and importance; otherwise, the cost savings of timber bridges tended to offset their relative lack of permanence."
  - CLM_725: SRC_NCHRP_CONTEXT 3.2.1 Stone Arch, p. 3-48: "Stone and wood were often the most readily available building materials for bridges long before fabricated metal was introduced towards the middle of the nineteenth century, and of the two, stone was by far the preferred choice where durability and permanence were required."


### C5 · The truss

**B15** (fact; claim: CLM_711, CLM_712)

- `4:13` A third approach is the truss.
- `4:16` It builds a structure out of straight members, joined into triangles.
- `4:21` Each member is mainly pulled or pushed along its length, in tension or in compression.
  - CLM_711: SRC_ODOT_MBI Glossary p.386 'truss': "truss - a jointed structure made up of individual members primarily carrying axial loads arranged and connected in triangular panels" · SRC_SCI_TRUSSES Introduction: "A truss is essentially a triangulated system of (usually) straight interconnected structural elements" — giả định: Definition.
  - CLM_712: SRC_SCI_TRUSSES Introduction: "The principal force in each element in a truss is axial tension or compression." · SRC_FHWA_CBM Chapter 2, 'Component Terminology': "These axial forces are either compression or tension." — giả định: Idealisation (pinned joints); the source notes real joints are not perfectly pinned. No member-by-member forces are shown.

**B16** (fact; claim: CLM_713, CLM_714)

- `4:29` In a simple span like these, under a downward load, the top chord is squeezed and the bottom chord is stretched.
- `4:37` Inside, some web members are in compression and others are in tension.
  - CLM_713: SRC_FHWA_CBM Chapter 2, 'Component Terminology': "The upper, or top, chords are in compression. The bottom, or lower, chords are in tension." · SRC_SCI_TRUSSES 'Types of trusses': "Under gravity loads, the top and bottom chords of the truss provide the compression and tension resistance to overall bending" — giả định: ASSUMPTION: each truss span of the illustrative model is treated as a simple span (separate truss on its own bearings) carrying a downward load. The FHWA source calls this a simplified characterization for the common single-span bridge; continuous spans behave differently. Qualitative only.
  - CLM_714: SRC_FHWA_CBM Chapter 2, 'Component Terminology': "Some of these web members will usually be in compression; others will consistently be in tension." — giả định: General statement; which web member carries which force is NOT shown (no load case analysed).

**B17** (fact; claim: CLM_727, CLM_728, CLM_711)

- `4:43` The triangles can be arranged in different patterns.
- `4:48` This is a Pratt truss.
- `4:50` In the original design, patented in 1844, its verticals were timber and its diagonals were iron rods.
- `4:59` Swap the web for diagonals that alternate in direction, and you have a Warren truss, patented in 1848.
- `5:08` Both patterns carry load through triangles; they simply arrange the members differently.
  - CLM_727: SRC_NCHRP_CONTEXT 2.2, p. 2-7: "In 1844, Thomas and Caleb Pratt patented the Pratt Truss, which reversed the Howe system and incorporated vertical timber members in compression and diagonal iron rods in tension, a “combination” structure. The structural principle in this design was used well into the twentieth century when all parts were made in steel." — giả định: Historical design description of the 1844 patent; the film does not mark the model's members as in tension or compression.
  - CLM_728: SRC_NCHRP_CONTEXT 2.2, p. 2-7: "the Warren truss was patented by two British engineers, James Warren and Willoughby Monzani. This truss design had alternating diagonals in either tension or compression" — giả định: The model's Warren variant has no verticals; the film says only that the diagonals alternate.
  - CLM_711: SRC_ODOT_MBI Glossary p.386 'truss': "truss - a jointed structure made up of individual members primarily carrying axial loads arranged and connected in triangular panels" · SRC_SCI_TRUSSES Introduction: "A truss is essentially a triangulated system of (usually) straight interconnected structural elements" — giả định: Definition.

**B18** (fact; claim: CLM_729)

- `5:15` Trusses also changed how bridges were built.
- `5:19` By the middle of the nineteenth century, shops were making and drilling truss members, then shipping them to the bridge site, ready to assemble.
- `5:29` And by 1860, the railroads relied almost entirely on these prefabricated parts.
  - CLM_729: SRC_NCHRP_CONTEXT 2.2 'Foundries and Fabricators', p. 2-11: "These shops formed bridge members, drilled the members and assembled and connected the truss members, before packaging and shipping them to the bridge site. By 1860, the railroads were almost exclusively relying on these private concerns to fill their bridge needs with pre-fabricated parts."


### C6 · The cantilever

**B40** (fact; claim: CLM_752)

- `5:37` To cross wide rivers and deep gorges, bridges needed longer spans.
- `5:43` Wide rivers like the Ohio and the Mississippi, and deep gorges like the one at Niagara, needed bridges that could reach farther.
  - CLM_752: SRC_NCHRP_CONTEXT 3.7 Cantilevers, p. 3-142: "The cantilever was developed to solve the problem of increasing the length of the bridge to enable crossing wide bodies of water like the Ohio and Mississippi rivers, or wide and deep gorges like the Niagara Gorge" · SRC_NCHRP_CONTEXT 3.7 Cantilevers, p. 3-142: "This configuration made longer spans possible and wider clearance beneath."

**B41** (fact; claim: CLM_750)

- `5:53` One answer was the cantilever.
- `5:56` Hold your arm straight out from your shoulder, and it is acting as a cantilever: supported at one end, free at the other, like a diving board.
  - CLM_750: SRC_NCHRP_CONTEXT 3.7 Cantilevers, p. 3-142: "If you hold your arm straight out from your shoulder, it is acting as a cantilever." · SRC_NCHRP_CONTEXT 3.7 Cantilevers, p. 3-142: "Cantilever bridges are a modified form of beam bridge. A cantilever is essentially a beam that is unsupported at one end but supported at the other, like diving boards."

**B42** (fact; claim: CLM_750, CLM_751)

- `6:07` A cantilever bridge is a modified beam.
- `6:11` Anchor arms rest on the banks and the main piers, cantilever arms reach out over the river, and a suspended span hangs between their tips.
  - CLM_750: SRC_NCHRP_CONTEXT 3.7 Cantilevers, p. 3-142: "If you hold your arm straight out from your shoulder, it is acting as a cantilever." · SRC_NCHRP_CONTEXT 3.7 Cantilevers, p. 3-142: "Cantilever bridges are a modified form of beam bridge. A cantilever is essentially a beam that is unsupported at one end but supported at the other, like diving boards."
  - CLM_751: SRC_NCHRP_CONTEXT 3.1 Trusses, p. 3-4: "A cantilevered truss bridge consists of anchor arms supported by piers, and a suspended span that is supported by the anchor arms." · SRC_NCHRP_CONTEXT 3.7 Cantilevers, p. 3-142: "the counterbalanced cantilever with the arms supporting a simple suspended span"

**B43** (fact; claim: CLM_753)

- `6:22` Its great advantage came during construction.
- `6:26` The arms could be built outward from the piers with no falsework blocking the channel below, and then the suspended span was lifted into place.
  - CLM_753: SRC_NCHRP_CONTEXT 3.7 Cantilevers, p. 3-143: "One great advantage of a cantilever is that it can be built outwards from the towers without falsework to block the channel below. Then the suspended span can be lifted into place."

**B44** (fact; claim: CLM_754, CLM_756, CLM_794)

- `6:37` In the United States, cantilevers were a standard answer for intermediate to longer spans from the 1880s to the 1960s.
- `6:47` The Queensboro Bridge in New York was the country's longest cantilever when it was completed in 1909.
- `6:55` Unlike our model, it has no suspended span in the middle, something one report calls unique among cantilevers of its size.
  - CLM_754: SRC_NCHRP_CONTEXT 3.7 Cantilevers, p. 3-143: "The cantilever bridge in the U.S. dates from the 1880s to the 1960s and is one of the standard bridge types for intermediate to longer spans"
  - CLM_756: SRC_NCHRP_CONTEXT 3.7 Cantilevers, p. 3-143: "The Queensboro Bridge over the East River in New York City was the longest cantilever in the United States when completed in 1909."
  - CLM_794: SRC_NCHRP_CONTEXT 3.7 Cantilevers, p. 3-143: "It had no central suspended span which was unique among cantilevers of its size designed with a single hinge to prevent the reversal of stresses."


### C7 · The suspension bridge

**B45** (fact; claim: CLM_763, CLM_760)

- `7:06` For the longest spans of all, engineers hung the deck instead.
- `7:11` In a suspension bridge, the deck hangs from vertical suspenders attached to great main cables.
  - CLM_763: SRC_NCHRP_CONTEXT 3.5 Suspension, p. 3-133: "Suspension bridges are particularly suited for spanning great distances" · SRC_FHWA_BRIDGE_TYPES 2.6 Suspension Bridges: "Suspension bridges, whose towers are significantly shorter than those required for cable-stayed bridges, become economical for very long spans."
  - CLM_760: SRC_NCHRP_CONTEXT 3.5 Suspension, p. 3-133: "The deck of a suspension bridge is hung from vertical suspenders that are affixed to ropes, chains, eyebars or cables that are in tension, passing over towers that are in compression."

**B46** (fact; claim: CLM_760, CLM_761)

- `7:19` The cables are in tension, and they pass over towers that are in compression.
- `7:24` At each end, the cables are anchored, usually in large masses of stone or concrete.
  - CLM_760: SRC_NCHRP_CONTEXT 3.5 Suspension, p. 3-133: "The deck of a suspension bridge is hung from vertical suspenders that are affixed to ropes, chains, eyebars or cables that are in tension, passing over towers that are in compression."
  - CLM_761: SRC_NCHRP_CONTEXT 3.5 Suspension, p. 3-133: "Usually the ends of the cables are anchored in large masses of stone or concrete" · SRC_FHWA_BRIDGE_TYPES 2.6 Suspension Bridges: "The ends of the main suspension cables are anchored either into large counterweights or directly into bedrock at the ends of the structure."

**B47** (fact; claim: CLM_765)

- `7:32` A suspension deck is light for its span, and it can be very flexible.
- `7:38` So a stiffening truss is commonly built under the deck, against wind and earthquakes.
  - CLM_765: SRC_FHWA_BRIDGE_TYPES 2.6 Suspension Bridges: "Suspension bridge superstructures are generally very light relative to the span length which leads to structures that may be very flexible." · SRC_FHWA_BRIDGE_TYPES 2.6 Suspension Bridges: "it is common to provide a lateral stiffening truss under the deck to avoid excessive excitement of the superstructure under wind or seismic loadings."

**B48** (fact; claim: CLM_764, CLM_768)

- `7:45` The Brooklyn Bridge in New York, completed in 1883, was planned with two towers, cables and suspenders, anchorages and a stiffening truss.
- `7:56` One report says few suspension bridges built since can claim to stand entirely clear of its shadow.
  - CLM_764: SRC_NCHRP_CONTEXT 3.5 Suspension, p. 3-133: "Few suspension bridges in the world built since the time of the Roeblings can claim to stand entirely clear of the shadow cast by the Brooklyn Bridge. The plan involved two towers, cables and suspenders, anchorages and a stiffening truss - the character-defining features of a suspension bridge." — giả định: M8.2: 'The plan' is the Brooklyn Bridge plan (the preceding sentence). The film lists these parts for that bridge, not as a definition every suspension bridge meets: FHWA 2012 (CLM_765) calls a stiffening truss 'common'.
  - CLM_768: SRC_NCHRP_CONTEXT 3.7 Cantilevers, p. 3-143: "Washington Roebling for the Brooklyn Bridge (1883)" · SRC_NCHRP_CONTEXT 3.5 Suspension, p. 3-133: "Few suspension bridges in the world built since the time of the Roeblings can claim to stand entirely clear of the shadow cast by the Brooklyn Bridge." — giả định: 'Few ... stand entirely clear of the shadow' is the report's assessment; the narration attributes it ('one report').


### C8 · The cable-stayed bridge

**B50** (fact; claim: CLM_770, CLM_771)

- `8:04` A cable-stayed bridge also relies on steel cables, but it uses them differently.
- `8:11` Straight stay cables run from tall towers directly down to the edges of the deck.
  - CLM_770: SRC_FHWA_BRIDGE_TYPES 2.5 Cable-Stayed: "Cable-Stayed bridges rely on high strength steel cables as major structural elements. The stay cables are inclined from the supporting towers to edge girders at or below the deck elevation."
  - CLM_771: SRC_FHWA_BRIDGE_TYPES 2.5 Cable-Stayed: "Generally the towers are very tall with the height determined as a function of the span length." · SRC_FHWA_BRIDGE_TYPES 2.5 Cable-Stayed: "The flattest cable angle should not be less than about 22 degrees with the horizontal."

**B51** (fact; claim: CLM_763, CLM_761, CLM_770, CLM_771)

- `8:18` Drawn in outline at the same span, the two types differ.
- `8:23` The suspension bridge has much shorter towers, and its main cables run over them to anchorages at each end.
- `8:31` The cable-stayed bridge needs taller towers, because their height depends on the span, and its stays end at the deck itself.
  - CLM_763: SRC_NCHRP_CONTEXT 3.5 Suspension, p. 3-133: "Suspension bridges are particularly suited for spanning great distances" · SRC_FHWA_BRIDGE_TYPES 2.6 Suspension Bridges: "Suspension bridges, whose towers are significantly shorter than those required for cable-stayed bridges, become economical for very long spans."
  - CLM_761: SRC_NCHRP_CONTEXT 3.5 Suspension, p. 3-133: "Usually the ends of the cables are anchored in large masses of stone or concrete" · SRC_FHWA_BRIDGE_TYPES 2.6 Suspension Bridges: "The ends of the main suspension cables are anchored either into large counterweights or directly into bedrock at the ends of the structure."
  - CLM_770: SRC_FHWA_BRIDGE_TYPES 2.5 Cable-Stayed: "Cable-Stayed bridges rely on high strength steel cables as major structural elements. The stay cables are inclined from the supporting towers to edge girders at or below the deck elevation."
  - CLM_771: SRC_FHWA_BRIDGE_TYPES 2.5 Cable-Stayed: "Generally the towers are very tall with the height determined as a function of the span length." · SRC_FHWA_BRIDGE_TYPES 2.5 Cable-Stayed: "The flattest cable angle should not be less than about 22 degrees with the horizontal."

**B52** (fact; claim: CLM_772, CLM_773)

- `8:41` Once the towers are up, the deck can be built outward from them in both directions, without falsework towers, until the spans meet.
- `8:50` The stays also squeeze the deck along its length, and that squeeze builds up toward the towers.
  - CLM_772: SRC_FHWA_BRIDGE_TYPES 4.4 Cable-Stayed Bridges: "Once the towers are completed, the cable-stayed superstructures can be constructed without falsework towers, which can provide significant benefits over navigable waterways. The construction uses a balanced cantilever method proceeding away from the towers until the spans can be closed."
  - CLM_773: SRC_FHWA_BRIDGE_TYPES 2.5 Cable-Stayed: "The compressive forces are additive from the end of the longest cables toward the towers. In most cases the edge girder design is not controlled by bending but by the compressive forces imparted by the stay cables"

**B53** (fact; claim: CLM_775, CLM_774)

- `8:58` Before 1970, suspension bridges were thought to be the cheapest way to span more than about 1,200 feet.
- `9:07` By 2012, a federal handbook said cable-stayed bridges become very competitive above 750 feet, and that suspension bridges pay off only as main spans approach 3,000.
  - CLM_775: SRC_FHWA_BRIDGE_TYPES 3.0 Economics: "Prior to 1970, it was generally considered that suspension bridges provided the most economical solution for span lengths in excess of about 1200 feet. With the development of cable-stayed bridge technology, suspension bridges do not become economical until the main span length approaches 3000 feet."
  - CLM_774: SRC_FHWA_BRIDGE_TYPES 3.0 Economics: "In the U.S., cable-stayed bridges become very cost competitive for main span lengths over 750 feet. Almost all bridges with main span lengths in excess of 1000 feet built in the U.S. since 1980 have been cable-stayed structures." — giả định: M8.2: a 2012 statement about bridges built 1980-2012; narrated with its date and its conditions (built in the U.S., main span over 1,000 ft), not as the present.


### C9 · Why different designs exist

**B19** (framing; claim: không, câu dẫn dắt)

- `9:22` So which design is best?
- `9:25` The honest answer is that it depends.
- `9:29` Materials, the site, the span, cost, and the skills available all pull in different directions.

**B20A** (fact; claim: CLM_726)

- `9:37` Start with the materials themselves.
- `9:40` An arch needs a material that is strong under compression, and stone is.
  - CLM_726: SRC_YALE_PHYSICS unit 01.05.08, section 6: "When selecting a building material for an arch bridge, engineers must consider only materials that are strong under compression. These materials include stone, concrete, or steel." — giả định: Educational secondary source (teacher curriculum unit); used for the general principle only.

**B20B** (fact; claim: CLM_712, CLM_735)

- `9:47` A truss needs members that can work in tension as well as compression.
- `9:52` Wrought iron was valued for exactly that: one historian calls it a material strong equally in tension and in compression.
  - CLM_712: SRC_SCI_TRUSSES Introduction: "The principal force in each element in a truss is axial tension or compression." · SRC_FHWA_CBM Chapter 2, 'Component Terminology': "These axial forces are either compression or tension." — giả định: Idealisation (pinned joints); the source notes real joints are not perfectly pinned. No member-by-member forces are shown.
  - CLM_735: SRC_NCHRP_CONTEXT 2.2, p. 2-8: "realized that a great advantage would be gained by the substitution of wrought iron [for cast iron], a material strong equally in tension and in compression" — giả định: A historian's characterisation (David Plowden) quoted in the report.

**B20C** (fact; claim: CLM_742, CLM_734)

- `10:02` Wood was often plentiful and cheap, but wooden bridges were vulnerable to decay.
  - CLM_742: SRC_NCHRP_CONTEXT 2.2, p. 2-6: "While stone was often used in the East, timber was generally used by the western bridge builders because of the pressure to quickly and economically get new railroads on line, and timber was generally abundant and cheap."
  - CLM_734: SRC_ASCE_BOLLMAN main text: "Replacing wooden bridges, which were cumbersome to build and vulnerable to decay"

**B21** (fact; claim: CLM_733, CLM_746)

- `10:10` That is one reason many timber truss bridges were covered with a roof and siding, to protect them from the weather.
- `10:18` This is the Humpback Covered Bridge, built in 1857 over Dunlap Creek.
  - CLM_733: SRC_NCHRP_CONTEXT 3.1.1 King Post, p. 3-7: "the most common extant king post truss bridges are covered by a roof and siding to protect them from the weather" — giả định: Stated for king post trusses; the film says 'many timber truss bridges'.
  - CLM_746: SRC_NCHRP_CONTEXT List of figures, 3-5: "Humpback Covered Bridge (1857), Humpback Bridge spanning Dunlap" — giả định: Only the name, date and crossing are narrated.

**B20E** (fact; claim: CLM_780, CLM_781)

- `10:26` Cables have a materials story of their own.
- `10:29` America's first metal suspension bridges hung from iron chains, and many failed after only a few years: critics said such a bridge was only as good as the weakest link in one of its chains.
- `10:43` Wire cables answered that fear, and suspension and cable-stayed bridges came to rely on high-strength steel cables.
  - CLM_780: SRC_NCHRP_CONTEXT 3.5 Suspension, p. 3-132: "In 1801, James Finley (1756-1828), a justice of the peace and judge in Fayette County, Pennsylvania, constructed the first metal suspension bridge in the United States" · SRC_NCHRP_CONTEXT 3.5 Suspension, p. 3-132: "Although forty or more chain bridges were built according to Finley’s 1808 patent, they tended to fail after only a few years of use. Some critics felt that the Finley design was only as good as the weakest link in one of the chains. This fear was addressed by the introduction of metal cables."
  - CLM_781: SRC_FHWA_BRIDGE_TYPES 2.5 Cable-Stayed: "Cable-Stayed bridges rely on high strength steel cables as major structural elements." · SRC_FHWA_BRIDGE_TYPES 2.6 Suspension Bridges: "suspension bridges rely on high-strength cables as major structural elements."

**B22** (fact; claim: CLM_736)

- `10:53` The site of a bridge matters too.
- `10:56` Railway engines have limited traction, so railways need gentle gradients.
- `11:02` Where a valley was too deep and wide to fill with an embankment, engineers built viaducts and trestles to keep the line nearly straight and level.
  - CLM_736: SRC_NCHRP_CONTEXT 3.6 Trestles and Viaducts, p. 3-137: "both have design attributes that were generated by the need of railroad engineers to maintain easy gradients, especially when crossing deep ravines or depressions, to compensate for the limited traction of railroad engines." · SRC_NCHRP_CONTEXT 3.6 Trestles and Viaducts, p. 3-137: "“Viaducts and trestles were the engineering solution for maintaining a nearly straight and horizontal line where the depth and width of the valley or gorge rendered embankments impracticable.”"

**B22B** (fact; claim: CLM_761, CLM_776)

- `11:13` Long spans make the ground beneath them matter even more.
- `11:18` A suspension bridge has to anchor its cables in massive blocks, or directly in bedrock.
- `11:25` The towers of a cable-stayed bridge, by contrast, can be built where good rock does not lie near the surface.
  - CLM_761: SRC_NCHRP_CONTEXT 3.5 Suspension, p. 3-133: "Usually the ends of the cables are anchored in large masses of stone or concrete" · SRC_FHWA_BRIDGE_TYPES 2.6 Suspension Bridges: "The ends of the main suspension cables are anchored either into large counterweights or directly into bedrock at the ends of the structure."
  - CLM_776: SRC_FHWA_BRIDGE_TYPES 3.0 Economics: "They are more versatile than suspension bridges in that they offer more possible configurations and towers can be constructed in less than optimal foundation conditions because having good rock near the surface is not a requirement."

**B22C** (fact; claim: CLM_782)

- `11:34` A cantilever like this one is a continuous girder with hinges built in, which made its forces easy to calculate.
- `11:42` So on unstable soil, if a pier sank, its superstructure could adjust, where a continuous beam might build up hidden stresses and fail.
  - CLM_782: SRC_NCHRP_CONTEXT 3.7 Cantilevers, p. 3-142: "a cantilever is a continuous girder with hinges at the points of zero moments" · SRC_NCHRP_CONTEXT 3.7 Cantilevers, p. 3-142: "The form was statically determinant, which meant that it was easy to calculate and" · SRC_NCHRP_CONTEXT 3.7 Cantilevers, p. 3-142: "the members did not have the inherent deficiency of the continuous beam or girder developing indiscernible internal stresses and possibly failing should one of the piers or abutments subside. Unstable soil conditions plagued foundation, pier, and abutment design, so the ability of a bridge’s superstructure to adjust should one of the piers or abutments sink, was a significant design breakthrough." — giả định: M8.2: the advantage belongs to the hinged, statically determinate form and to the superstructure; the film does not suggest a cantilever cures bad foundations.

**B22D** (fact; claim: CLM_783, CLM_765)

- `11:53` Then there is the wind.
- `11:56` In 1940, the four-month-old Tacoma Narrows suspension bridge collapsed in only moderately high winds.
- `12:05` The disaster led to intense research on wind, and later suspension bridges were built to new standards for stiffened decks.
  - CLM_783: SRC_NCHRP_CONTEXT 2.2, p. 2-28: "In 1940, the four-month old Tacoma Narrows Bridge over Puget Sound collapsed due to the forces of the wind on the suspension structure. The event led to intense research on the dynamics of the effects of wind in large structures." · SRC_NCHRP_CONTEXT 2.2, p. 2-28: "were based on substantial research that produced new formulae and standards" · SRC_FHWA_BRIDGE_TYPES 2.6 Suspension Bridges: "The structure collapsed due to the harmonic frequency set up during a period of only moderately high winds." — giả định: Narrated as a historical event; the film shows no collapse or destruction.
  - CLM_765: SRC_FHWA_BRIDGE_TYPES 2.6 Suspension Bridges: "Suspension bridge superstructures are generally very light relative to the span length which leads to structures that may be very flexible." · SRC_FHWA_BRIDGE_TYPES 2.6 Suspension Bridges: "it is common to provide a lateral stiffening truss under the deck to avoid excessive excitement of the superstructure under wind or seismic loadings."


### C10 · Span, cost and time

**B23C** (fact; claim: CLM_784, CLM_785, CLM_786, CLM_775)

- `12:15` Span decides a great deal.
- `12:18` A 2012 federal handbook for steel bridges gives two kinds of numbers.
- `12:24` Some are practical ranges: plate girders from about 90 to over 500 feet, simple trusses from about 450 to about 750, and cantilever trusses considerably farther.
- `12:39` Others are spans that have actually been built: arches from about 200 to 1,800 feet, and cable-stayed bridges from under 200 to nearly 3,000.
- `12:51` And as we saw, suspension bridges only pay off as main spans approach 3,000 feet.
  - CLM_784: SRC_FHWA_BRIDGE_TYPES 3.0 Economics: "Applicable in span lengths from approximately 90 feet to over 500 feet they provide a versatile choice for the designer."
  - CLM_785: SRC_FHWA_BRIDGE_TYPES 3.0 Economics: "Trusses are generally not cost-effective for span lengths under 450 feet." · SRC_FHWA_BRIDGE_TYPES 3.0 Economics: "The practical upper limit for simple span trusses is approximately 750 feet while continuous trusses begin to be cost-effective when the span length exceeds 550 feet. Continuous or cantilever trusses can span considerably longer distances than simple span trusses."
  - CLM_786: SRC_FHWA_BRIDGE_TYPES 3.0 Economics: "Arches have been used for span lengths from approximately 200 feet up to 1800 feet worldwide." · SRC_FHWA_BRIDGE_TYPES 3.0 Economics: "Cable-stayed bridges have been constructed with main span lengths less than 200 feet and extending up to nearly 3000 feet."
  - CLM_775: SRC_FHWA_BRIDGE_TYPES 3.0 Economics: "Prior to 1970, it was generally considered that suspension bridges provided the most economical solution for span lengths in excess of about 1200 feet. With the development of cable-stayed bridge technology, suspension bridges do not become economical until the main span length approaches 3000 feet."

**B23D** (fact; claim: CLM_757, CLM_787)

- `12:59` Cost and skill pull in different directions.
- `13:03` A cantilever avoided the expensive anchorages a suspension bridge needs.
- `13:09` And a suspension bridge often takes a long time to build: installing its main cables calls for expertise that very few contractors have.
  - CLM_757: SRC_NCHRP_CONTEXT 3.7 Cantilevers, p. 3-142: "The cantilever also eliminated the high cost of building anchorages required by the other long span bridge type, suspension bridges, thus saving money and materials." — giả định: M8.2: the report's preceding sentence (beam and arch bridges of steel or reinforced concrete 'had limited spans not exceeding 200 to 300 feet') is not used. It gives no period or conditions, and far longer arches were built (FHWA 2012: about 200 to 1,800 ft; the Eads Bridge, 1874, has a 520 ft arch span).
  - CLM_787: SRC_FHWA_BRIDGE_TYPES 4.5 Suspension Bridges: "Erection of suspension bridges is relatively specialized. The installation of the main suspender cables requires expertise that very few contractors possess." · SRC_FHWA_BRIDGE_TYPES 4.5 Suspension Bridges: "The time to construct a suspension bridge is often relatively long as well."

**B23E** (fact; claim: CLM_788)

- `13:21` By 2012, cable-stayed bridges were becoming more common worldwide, and one significant reason was that the methods for erecting them had become better understood.
  - CLM_788: SRC_FHWA_BRIDGE_TYPES 4.4 Cable-Stayed Bridges: "Cable-stayed bridges are becoming more common worldwide. One significant reason for this is that the erection methods required for cable-stayed bridges have become better understood over the past 25 years." — giả định: M8.2: a 2012 statement; narrated with 'by 2012', not as the present.

**B24** (fact; claim: CLM_738, CLM_739, CLM_727, CLM_728, CLM_729)

- `13:34` Finally, every bridge belongs to its time.
- `13:38` As metal trusses spread, skilled masons became fewer and reinforced concrete arrived, stone arch construction declined.
- `13:47` Then, during the Great Depression, it briefly returned.
  - CLM_738: SRC_NCHRP_CONTEXT 3.2.1 Stone Arch, p. 3-49: "Increased use of metal truss bridges on highways from the late 1800s into the early twentieth century, coupled with a decrease in the number of skilled masons, and advancements in reinforced concrete construction technology in the early decades of the twentieth century, led to a decline in stone arch bridge construction. A brief resurgence in construction of this type occurred during the Great Depression"
  - CLM_739: SRC_NCHRP_CONTEXT 2.2, p. 2-6: "The first major engineered railroad bridge was the Carrollton Viaduct, completed in 1829 across Gwynn’s Falls, west of Baltimore City. Constructed of approximately 12,000 granite blocks, the 312-foot long bridge featured an 80-foot arch over the waterway."
  - CLM_727: SRC_NCHRP_CONTEXT 2.2, p. 2-7: "In 1844, Thomas and Caleb Pratt patented the Pratt Truss, which reversed the Howe system and incorporated vertical timber members in compression and diagonal iron rods in tension, a “combination” structure. The structural principle in this design was used well into the twentieth century when all parts were made in steel." — giả định: Historical design description of the 1844 patent; the film does not mark the model's members as in tension or compression.
  - CLM_728: SRC_NCHRP_CONTEXT 2.2, p. 2-7: "the Warren truss was patented by two British engineers, James Warren and Willoughby Monzani. This truss design had alternating diagonals in either tension or compression" — giả định: The model's Warren variant has no verticals; the film says only that the diagonals alternate.
  - CLM_729: SRC_NCHRP_CONTEXT 2.2 'Foundries and Fabricators', p. 2-11: "These shops formed bridge members, drilled the members and assembled and connected the truss members, before packaging and shipping them to the bridge site. By 1860, the railroads were almost exclusively relying on these private concerns to fill their bridge needs with pre-fabricated parts."

**B24B** (fact; claim: CLM_766, CLM_768, CLM_754, CLM_756, CLM_774)

- `13:53` Long spans have a timeline of their own.
- `13:56` By 1849, a suspension bridge at Wheeling spanned 1,010 feet, the longest span in the world when it opened.
- `14:06` Cantilevers were a standard American answer from the 1880s to the 1960s, and a 2012 federal handbook found that almost every American bridge built since 1980 with a main span over 1,000 feet was cable-stayed.
  - CLM_766: SRC_NCHRP_CONTEXT 3.5 Suspension, p. 3-132: "He quickly turned his full attention to the Wheeling Bridge, which was completed in 1849. Spanning 1,010 feet, this was the longest bridge in the world for many years after its completion" · SRC_EWV_WHEELING Wheeling Suspension Bridge, first paragraph: "The wire suspension bridge over the Ohio River at Wheeling was opened for traffic in October 1849 amid great public acclaim. It was the longest (1,010 feet) clear span in the world." · SRC_NCHRP_CONTEXT 3.5 Suspension, p. 3-133: "Officially opened on January 1, 1867, this bridge has a main span of 1,057 feet. It had the longest clear span of any bridge in the world when completed" — giả định: M8.2: NCHRP says 'longest bridge in the world for many years'; the film says only 'the longest span in the world when it opened' (e-WV: 'the longest (1,010 feet) clear span in the world'), because 'bridge' could be read as total length and the duration is not corroborated.
  - CLM_768: SRC_NCHRP_CONTEXT 3.7 Cantilevers, p. 3-143: "Washington Roebling for the Brooklyn Bridge (1883)" · SRC_NCHRP_CONTEXT 3.5 Suspension, p. 3-133: "Few suspension bridges in the world built since the time of the Roeblings can claim to stand entirely clear of the shadow cast by the Brooklyn Bridge." — giả định: 'Few ... stand entirely clear of the shadow' is the report's assessment; the narration attributes it ('one report').
  - CLM_754: SRC_NCHRP_CONTEXT 3.7 Cantilevers, p. 3-143: "The cantilever bridge in the U.S. dates from the 1880s to the 1960s and is one of the standard bridge types for intermediate to longer spans"
  - CLM_756: SRC_NCHRP_CONTEXT 3.7 Cantilevers, p. 3-143: "The Queensboro Bridge over the East River in New York City was the longest cantilever in the United States when completed in 1909."
  - CLM_774: SRC_FHWA_BRIDGE_TYPES 3.0 Economics: "In the U.S., cable-stayed bridges become very cost competitive for main span lengths over 750 feet. Almost all bridges with main span lengths in excess of 1000 feet built in the U.S. since 1980 have been cable-stayed structures." — giả định: M8.2: a 2012 statement about bridges built 1980-2012; narrated with its date and its conditions (built in the U.S., main span over 1,000 ft), not as the present.


### C11 · Real-world decisions

**B25** (fact; claim: CLM_741, CLM_742)

- `14:24` These trade-offs played out across nineteenth-century America as the railways spread.
- `14:30` In the East, railroads built massive stone viaducts, while western builders generally used timber.
- `14:38` Three documented examples show how differently builders answered.
  - CLM_741: SRC_NCHRP_CONTEXT 2.2, p. 2-6: "The railroad companies revolutionized bridge design, as they required more sophisticated designs and durable materials for carrying the heavy loads of the railcars." · SRC_NCHRP_CONTEXT 2.2, p. 2-6: "In the east, the railroads built massive high and/or long stone viaducts along the Baltimore and Ohio (B&O) Railroad."
  - CLM_742: SRC_NCHRP_CONTEXT 2.2, p. 2-6: "While stone was often used in the East, timber was generally used by the western bridge builders because of the pressure to quickly and economically get new railroads on line, and timber was generally abundant and cheap."

**B26** (fact; claim: CLM_739, CLM_740)

- `14:44` Near Baltimore, the Carrollton Viaduct was completed in 1829.
- `14:50` Built of roughly twelve thousand granite blocks, it carries the railway over Gwynns Falls on an eighty foot arch.
- `14:58` A national report in 2005 called it the world's oldest stone railroad span still in service.
  - CLM_739: SRC_NCHRP_CONTEXT 2.2, p. 2-6: "The first major engineered railroad bridge was the Carrollton Viaduct, completed in 1829 across Gwynn’s Falls, west of Baltimore City. Constructed of approximately 12,000 granite blocks, the 312-foot long bridge featured an 80-foot arch over the waterway."
  - CLM_740: SRC_NCHRP_CONTEXT 3.6 Trestles and Viaducts, p. 3-137: "The earliest stone arch railroad bridge built in the United States, and the world’s oldest stone railroad span still in service, is the Carrollton Viaduct over Gwynn’s Falls on the old B & O Railroad line near Baltimore, Maryland. Completed in 1829, this National Historic Landmark" — giả định: 'Still in service' is as of the 2005 report; the film attributes it to the report.

**B27** (interpretation; claim: CLM_741, CLM_725)

- `15:07` Early railroads needed durable bridges to carry heavy trains.
- `15:12` For a line meant to last, stone was the answer.
  - CLM_741: SRC_NCHRP_CONTEXT 2.2, p. 2-6: "The railroad companies revolutionized bridge design, as they required more sophisticated designs and durable materials for carrying the heavy loads of the railcars." · SRC_NCHRP_CONTEXT 2.2, p. 2-6: "In the east, the railroads built massive high and/or long stone viaducts along the Baltimore and Ohio (B&O) Railroad."
  - CLM_725: SRC_NCHRP_CONTEXT 3.2.1 Stone Arch, p. 3-48: "Stone and wood were often the most readily available building materials for bridges long before fabricated metal was introduced towards the middle of the nineteenth century, and of the two, stone was by far the preferred choice where durability and permanence were required."

**B28** (fact; claim: CLM_742, CLM_743)

- `15:17` In the West, the pressure was different.
- `15:20` Railroads had to open new lines quickly and economically, and timber was abundant and cheap.
- `15:27` This timber trestle near Corinne, Utah, was built in 1872 by the Central Pacific Railroad.
  - CLM_742: SRC_NCHRP_CONTEXT 2.2, p. 2-6: "While stone was often used in the East, timber was generally used by the western bridge builders because of the pressure to quickly and economically get new railroads on line, and timber was generally abundant and cheap."
  - CLM_743: SRC_NCHRP_CONTEXT List of figures, 3-106: "Promontory Route Railroad Trestles 790B (1872), Corinne vicinity, Box Elder County, Utah. This nineteenth century structure was built by the Central Pacific Railroad Company."

**B29** (interpretation; claim: CLM_737)

- `15:37` A trestle is a succession of towers supporting short spans.
- `15:42` It is the same beam idea as our timber model, repeated as often as the crossing needs.
  - CLM_737: SRC_NCHRP_CONTEXT 3.6 Trestles and Viaducts, p. 3-137: "a trestle consists of a succession of towers of steel, timber, or reinforced concrete, supporting short spans"

**B30** (fact; claim: CLM_744, CLM_745)

- `15:49` Iron offered a third path.
- `15:52` The Bollman truss, patented in 1852, was one of the first designs to use iron in all of its essential structural parts.
- `16:02` It could be built relatively quickly and inexpensively, while offering the long-lasting qualities of metal.
- `16:10` The bridge at Savage, Maryland, is the only remaining example of the design.
  - CLM_744: SRC_ASCE_BOLLMAN main text: "patented in 1852 and one of the first to use iron exclusively in all essential structural elements" · SRC_ASCE_BOLLMAN main text: "the Bollman Truss Bridge could be built relatively quickly and inexpensively, while providing the long-lasting qualities associated with metal."
  - CLM_745: SRC_ASCE_BOLLMAN main text: "The Bollman Truss Bridge is the only remaining example of a patented design that was used extensively on the Baltimore & Ohio and other railroads."

**B31** (interpretation; claim: CLM_741, CLM_742, CLM_744)

- `16:17` Stone for permanence, timber for speed and economy, and iron trusses that offered some of both.
- `16:24` Three places, three sets of constraints, three different bridges.
  - CLM_741: SRC_NCHRP_CONTEXT 2.2, p. 2-6: "The railroad companies revolutionized bridge design, as they required more sophisticated designs and durable materials for carrying the heavy loads of the railcars." · SRC_NCHRP_CONTEXT 2.2, p. 2-6: "In the east, the railroads built massive high and/or long stone viaducts along the Baltimore and Ohio (B&O) Railroad."
  - CLM_742: SRC_NCHRP_CONTEXT 2.2, p. 2-6: "While stone was often used in the East, timber was generally used by the western bridge builders because of the pressure to quickly and economically get new railroads on line, and timber was generally abundant and cheap."
  - CLM_744: SRC_ASCE_BOLLMAN main text: "patented in 1852 and one of the first to use iron exclusively in all essential structural elements" · SRC_ASCE_BOLLMAN main text: "the Bollman Truss Bridge could be built relatively quickly and inexpensively, while providing the long-lasting qualities associated with metal."

**B31A** (fact; claim: CLM_789)

- `16:30` Long spans forced hard decisions too.
- `16:34` In 1855, John Roebling's suspension bridge carried trains across the Niagara Gorge, but railroad executives doubted that suspension bridges could bear heavy trains.
- `16:47` Their doubts were not unjustified: the bridge needed substantial repairs in 1877 and 1880, and it was declared inadequate in 1890.
  - CLM_789: SRC_NCHRP_CONTEXT 3.5 Suspension, p. 3-132: "who won the contract to build the second suspension bridge, and the first railroad bridge, across the Niagara Gorge. Completed in 1855" · SRC_NCHRP_CONTEXT 3.5 Suspension, p. 3-133: "railroad company executives were not convinced that suspension bridges were capable of bearing the live loads imposed on them by heavy rail traffic. Their skepticism was not unjustified because the Niagara Bridge needed substantial repair in 1877 and 1880, and was declared inadequate in 1890." — giả định: M8.2: the report's next sentence ('It would be 133 years before the next suspension bridge designed for railway traffic was built') is not used. The Williamsburg Bridge, a suspension bridge opened in 1903, carried rail and trolley traffic on stiffening trusses 'designed ... to support rail traffic on the deck' (NYC DOT, https://www.nyc.gov/html/dot/html/infrastructure/williamsburg-bridge.shtml); the statement would need a restriction the source does not give.

**B31B** (fact; claim: CLM_790, CLM_791)

- `17:00` In America, modern cantilevers were first used by the railroads, and only later for highways.
- `17:07` A cantilever is inherently rigid, so if properly designed, heavy locomotives pulling trains are no threat to it.
- `17:16` In 1877, one carried the Cincinnati Southern Railroad across the 275-foot-deep Kentucky River gorge: the longest cantilever in the world.
  - CLM_790: SRC_NCHRP_CONTEXT 3.7 Cantilevers, p. 3-142: "Cantilevers first were used by the railroads (Poughkeepsie, Memphis, High Bridge) and then as highway bridges" · SRC_NCHRP_CONTEXT 3.7 Cantilevers, p. 3-143: "Another is that it is inherently rigid so that heavy locomotives pulling trains of cars are no threat to the structure if properly designed." — giả định: M8.2: the passage follows Gerber's Hassfurt Bridge (1867), 'the first modern cantilever', and the type's use in the U.S.; the report also describes far older cantilevers (Nikko, fourth century; Wandipore, about 1643), so the film says 'in America, modern cantilevers'.
  - CLM_791: SRC_NCHRP_CONTEXT 3.7 Cantilevers, p. 3-143: "In 1877, American engineer C. Shaler Smith, Baltimore Bridge Company, and Louis Frederic Gustav Bouscaren, chief railroad engineer, built the world’s longest cantilever for the Cincinnati Southern Railroad over the 275-foot deep Kentucky River gorge at Dixville."

**B31C** (fact; claim: CLM_792)

- `17:30` In San Francisco, the Golden Gate Bridge opened in 1937.
- `17:36` For 27 years, it stood as the world's longest span.
  - CLM_792: SRC_NCHRP_CONTEXT 2.2, p. 2-28: "In May 1937, the Golden Gate Bridge opened in San Francisco. For twenty-seven years, the bridge stood as the world’s longest span"

**B31D** (fact; claim: CLM_793)

- `17:42` In Maine, a modern cable-stayed bridge went up remarkably fast.
- `17:47` The Penobscot Narrows Bridge, opened in 2006, carries its 1,161-foot main span on two concrete pylons 430 feet tall.
- `18:00` It took just 42 months from conception to completion, and one of its pylons has a public observatory at the top.
  - CLM_793: SRC_FHWA_PENOBSCOT Chapter 3, The test bridge: "The Penobscot Narrows Bridge is a 2,120 ft (646 m) long cable-stayed bridge that carries U.S. Route 1 over the Penobscot River connecting Verona Island to Prospect in Maine." · SRC_FHWA_PENOBSCOT Chapter 3, The test bridge: "has a main span of 1,161 ft (354 m)" · SRC_FHWA_PENOBSCOT Chapter 3, The test bridge: "The bridge spans are supported by two 430-ft (131.1-m) tall concrete pylons, each containing 40 stay cables." · SRC_FHWA_PENOBSCOT Chapter 3, The test bridge: "spanned a mere 42 months from conception to completion; construction was started in 2004 and the bridge was opened to traffic on December 30, 2006." · SRC_FHWA_PENOBSCOT Chapter 3, The test bridge: "A unique feature of the west pylon, Pier 1, is the public observatory, accessible by elevator, located at its top."


### C12 · Why they look different

**B32** (interpretation; claim: CLM_706, CLM_709, CLM_712)

- `18:10` So why don't bridges all look the same?
- `18:13` Because a bridge's form comes from two things working together.
- `18:18` One is how its structure carries load: beams resist bending, arches work in compression, and trusses share load among members in tension and compression.
  - CLM_706: SRC_FHWA_CBM Chapter 2, 'Component Terminology': "As a beam has strength from its bending resistance" · SRC_ODOT_MBI Glossary p.358 'girder': "girder - a horizontal flexural member that is the main or primary support for a structure" — giả định: Qualitative; no stresses, deflections or capacities. The procedural model has not been analysed.
  - CLM_709: SRC_ODOT_MBI Part 2 Ratings, Item 25 Arch, p.144 (manual p.2-56): "The curve converts vertical (gravity) loads within the span to horizontal and vertical thrusts at the spring lines. As a result, the forces within the arch are generally compression" · SRC_ODOT_MBI Glossary p.339 'arch': "arch - a curved structure element primarily in compression that transfers vertical loads through inclined reactions to its end supports" · SRC_YALE_PHYSICS 'Arch Bridges' section: "Arch bridges rely primarily on compression" — giả định: General principle for masonry arches under gravity load; no thrust line, magnitudes or stability assessment of the illustrative model.
  - CLM_712: SRC_SCI_TRUSSES Introduction: "The principal force in each element in a truss is axial tension or compression." · SRC_FHWA_CBM Chapter 2, 'Component Terminology': "These axial forces are either compression or tension." — giả định: Idealisation (pinned joints); the source notes real joints are not perfectly pinned. No member-by-member forces are shown.

**B32L** (interpretation; claim: CLM_750, CLM_760, CLM_770)

- `18:30` Cantilevers reach out from their piers, and suspension and cable-stayed bridges hang their decks from steel cables.
  - CLM_750: SRC_NCHRP_CONTEXT 3.7 Cantilevers, p. 3-142: "If you hold your arm straight out from your shoulder, it is acting as a cantilever." · SRC_NCHRP_CONTEXT 3.7 Cantilevers, p. 3-142: "Cantilever bridges are a modified form of beam bridge. A cantilever is essentially a beam that is unsupported at one end but supported at the other, like diving boards."
  - CLM_760: SRC_NCHRP_CONTEXT 3.5 Suspension, p. 3-133: "The deck of a suspension bridge is hung from vertical suspenders that are affixed to ropes, chains, eyebars or cables that are in tension, passing over towers that are in compression."
  - CLM_770: SRC_FHWA_BRIDGE_TYPES 2.5 Cable-Stayed: "Cable-Stayed bridges rely on high strength steel cables as major structural elements. The stay cables are inclined from the supporting towers to edge girders at or below the deck elevation."

**B32B** (interpretation; claim: CLM_742, CLM_724)

- `18:40` The other is the world it was built in: its materials, its site, its span, its budget and its builders.
  - CLM_742: SRC_NCHRP_CONTEXT 2.2, p. 2-6: "While stone was often used in the East, timber was generally used by the western bridge builders because of the pressure to quickly and economically get new railroads on line, and timber was generally abundant and cheap."
  - CLM_724: SRC_NCHRP_CONTEXT 3.2.1 Stone Arch, p. 3-49: "Stone arch bridges were generally more expensive to build than were timber bridges, but their use for roads and highways was favored for heavily traveled routes or locations of high visibility and importance; otherwise, the cost savings of timber bridges tended to offset their relative lack of permanence."

**B33** (interpretation; claim: CLM_721, CLM_738, CLM_777, CLM_767)

- `18:48` And it is not a simple story of progress.
- `18:52` Timber beam bridges were still being built long after timber trusses, and stone arches briefly returned during the Great Depression.
- `19:01` And in 2012, a federal handbook still named a kind of beam, the welded plate girder, as the most common steel bridge.
- `19:11` At one time, a great number of small suspension bridges were built across the country, simply because they were easy to put up.
- `19:20` Each form can still be the right answer in the right place.
  - CLM_721: SRC_NCHRP_CONTEXT 3.3.1 Timber Stringer, p. 3-80: "Long after wood truss bridges had ceased to be competitive with metal truss bridges for use in short spans in the nineteenth century, timber beam bridges were still being built. Because of the structure’s simplicity and readily available material (wood), the timber beam has endured to the present day" · SRC_NCHRP_CONTEXT 3.3.1 Timber Stringer, p. 3-80: "Today, these structures are built on low-trafficked, rural backcountry roads, private roads, or in national forests and parks."
  - CLM_738: SRC_NCHRP_CONTEXT 3.2.1 Stone Arch, p. 3-49: "Increased use of metal truss bridges on highways from the late 1800s into the early twentieth century, coupled with a decrease in the number of skilled masons, and advancements in reinforced concrete construction technology in the early decades of the twentieth century, led to a decline in stone arch bridge construction. A brief resurgence in construction of this type occurred during the Great Depression"
  - CLM_777: SRC_FHWA_BRIDGE_TYPES 3.0 Economics: "Welded plate girders are currently the most common type of steel bridge." — giả định: A 2012 FHWA statement about steel bridges; M8.2: narrated with its date ('in 2012'), not as the present.
  - CLM_767: SRC_NCHRP_CONTEXT 3.5 Suspension, p. 3-133: "At one time, however, a great number of suspension bridges of very modest span length were built across the country due to the type’s basic simplicity and ease of erection."

**B34** (framing; claim: không, câu dẫn dắt)

- `19:25` Next time you cross a bridge, look at its shape.
- `19:29` It shows how the load reaches the ground, and something about the people who built it.
- `19:35` These models are illustrations, not engineering designs, and the arrows show ideas, not calculated forces.

**B35** (framing; claim: không, câu dẫn dắt)

- `19:45` Thank you very much for watching.
- `19:48` The sources and photo credits are listed in the description.

## Bộ kiểm nhất quán lời/hình: cần người duyệt xác nhận

- B33.s4 (SIDE, UNCERTAIN): "Each form can still be the right answer in the right place." — left/right wording; no annotation to locate - confirm the referent in review
- B34.s2 (ARROWS, UNCERTAIN): "These models are illustrations, not engineering designs, and the arrows show ideas, not calculated forces." — generic reference to the arrows (shown in earlier beats); editorial check

## Chữ trên card

- **SC_008** (B02): Why Bridges Don't All Look the Same | Same problem. Different answers. | Materials | Site | Span | Time
- **SC_022** (B13): Conceptual diagram — not to scale | Keystone | Falsework (temporary) | Carpenters build the frame | Masons lay the stones
- **SC_023** (B14): A trade-off | Timber beam | Stone arch | Cost to build | lower | higher | Permanence | lower | higher | Favoured for | other crossings | busy, important routes | Lower cost made up for less permanence | After NCHRP 25-25(15), 2005
- **SC_034** (B44): Queensboro Bridge | A standard U.S. type, | 1880s to 1960s | Longest U.S. cantilever | when completed, 1909 | No central suspended span, | unlike the model | Photo: Jet Lowe, HAER, Library of Congress (public domain)
- **SC_039** (B48): Brooklyn Bridge | East River, New York | completed 1883 | Towers, cables, suspenders, | anchorages, stiffening truss | Photo: HAER, Library of Congress (public domain)
- **SC_041** (B51): Conceptual diagram — not to scale | Suspension: shorter towers, main cables to anchorages | Cable-stayed: taller towers, stays end at the deck
- **SC_043** (B53): Where long spans pay off (United States) | 0 ft | 1,000 ft | 2,000 ft | 3,000 ft | Before 1970: suspension above about 1,200 ft | Cable-stayed: very competitive above 750 ft | Suspension by 2012: as spans approach 3,000 ft | After FHWA, Steel Bridge Design Handbook (FHWA-IF-12-052), 2012
- **SC_044** (B19): 9 · Why different designs exist | Which design is best? | It depends. | Materials | Site | Span | Cost | Skills
- **SC_048** (B21): Humpback Covered Bridge | Roof and siding protect | the timber trusses | Dunlap Creek, built 1857 | Covington, Virginia | Photo: Jack E. Boucher, HAER, Library of Congress (public domain)
- **SC_050** (B22): Schematic — not to scale | Down and up again: too steep for trains | A viaduct keeps the line nearly level
- **SC_051** (B22B): Schematic — not to scale | Rock | Rock | Massive block | Into bedrock | Suspension: cables anchored in massive blocks or in bedrock | Cable-stayed: good rock near the surface is not required
- **SC_054** (B23C): 10 · Span, cost and time | Two kinds of span numbers (steel bridge handbook, 2012) | 0 ft | 1,000 ft | 2,000 ft | 3,000 ft | Practical or economic range | Spans actually built | Plate girder: about 90 to over 500 ft | Simple truss: about 450 to about 750 ft | Cantilever truss: considerably farther | Arch: about 200 to 1,800 ft | Cable-stayed: under 200 to nearly 3,000 ft | Suspension: economic as main spans approach 3,000 ft | After FHWA, Steel Bridge Design Handbook (FHWA-IF-12-052), 2012 — ranges, not limits of what a type can span
- **SC_057** (B24): 1820 | 1840 | 1860 | 1880 | 1900 | 1920 | 1940 | 1829  Carrollton Viaduct (stone) | 1844  Pratt truss patented | 1848  Warren truss patented | 1860  Prefabricated truss parts | Metal trusses spread; stone arches decline | Great Depression: stone arches return
- **SC_058** (B24B): 1840 | 1870 | 1900 | 1930 | 1960 | 1990 | 1849  Wheeling suspension bridge: 1,010 ft span | 1883  Brooklyn Bridge | 1909  Queensboro cantilever | Cantilevers: a standard U.S. type | 1980–2012: U.S. spans over 1,000 ft cable-stayed | Long spans: a timeline of their own
- **SC_059** (B25): 11 · Real-world decisions | WEST | EAST | United States — schematic, not to scale | Timber, built fast | Massive stone viaducts | Corinne, Utah | Baltimore | Savage, Maryland
- **SC_060** (B26): Carrollton Viaduct | Baltimore, Maryland | completed 1829 | about 12,000 granite blocks | 80 ft arch over Gwynns Falls | Photo: William E. Barrett, HAER, Library of Congress (public domain)
- **SC_062** (B28): Promontory Route trestle | Timber: abundant, cheap | and quick to build | near Corinne, Utah | Central Pacific, 1872 | Photo: HAER, Library of Congress (public domain)
- **SC_064** (B30): Bollman Truss Bridge | Patented 1852 | iron in all essential parts | quick, inexpensive, | long-lasting | Savage, Maryland | Photo: William E. Barrett, HAER, Library of Congress (public domain)
- **SC_065** (B31): Stone: permanence | Timber: speed and economy | Iron: some of both | Three places, three sets of constraints | Photos: HAER, Library of Congress (public domain)
- **SC_068** (B31C): Golden Gate Bridge | San Francisco, California | opened 1937 | World's longest span | for 27 years | Photo: Jet Lowe, HAER, Library of Congress (public domain)
- **SC_072** (B32B): 2 · The world it was built in | Materials | Site | Span | Budget | Builders
- **SC_073** (B33): 1820 | 1840 | 1860 | 1880 | 1900 | 1920 | 1940 | 1829  Carrollton Viaduct (stone) | 1844  Pratt truss patented | 1848  Warren truss patented | 1860  Prefabricated truss parts | Stone arches return briefly | Timber beam bridges: built | long after timber trusses | 2012: most common steel bridge | is the plate girder, a beam | Small suspension bridges: | simple and easy to put up
- **SC_075** (B35): Why Bridges Don't All Look the Same | Archival photographs: Historic American Engineering Record, | Library of Congress Prints & Photographs Division (public domain) | Sources: TRB NCHRP 25-25(15); FHWA; Ohio DOT; ASCE; | SteelConstruction.info; Yale-New Haven Teachers Institute | 3D models and diagrams are illustrative, not engineering designs | Architecture Story Studio

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
- B40 `B40_ch` NOTE: "6 · The cantilever"
- B40 `B40_note` NOTE: "A wider crossing (illustrative, not to scale)"
- B41 `B41_note` NOTE: "Illustrative model"
- B42 `B42_anchor` COMPONENT_LABEL: "Anchor arm" (CLM_751)
- B42 `B42_arm` COMPONENT_LABEL: "Cantilever arm" (CLM_751)
- B42 `B42_span` COMPONENT_LABEL: "Suspended span" (CLM_751)
- B43 `B43_note` NOTE: "Built outward: no falsework in the channel" (CLM_753)
- B45 `B45_ch` NOTE: "7 · The suspension bridge"
- B45 `B45_model` NOTE: "Illustrative model"
- B45 `B45_hangers` COMPONENT_LABEL: "Suspenders" (CLM_760)
- B45 `B45_cable` COMPONENT_LABEL: "Main cable" (CLM_760)
- B46 `B46_load` LOAD_ARROW: "Load" (CLM_760)
- B46 `B46_cable` CALLOUT: "Cables: tension" (CLM_760)
- B46 `B46_tower` CALLOUT: "Towers: compression" (CLM_760)
- B46 `B46_anchor` COMPONENT_LABEL: "Anchorage" (CLM_761)
- B47 `B47_note` NOTE: "Stiffening truss under the deck" (CLM_765)
- B50 `B50_ch` NOTE: "8 · The cable-stayed bridge"
- B50 `B50_model` NOTE: "Illustrative model"
- B50 `B50_stays` COMPONENT_LABEL: "Stay cables" (CLM_770)
- B50 `B50_tower` COMPONENT_LABEL: "Tower" (CLM_770)
- B52 `B52_note` NOTE: "Built outward from the towers" (CLM_772)
- B52 `B52_deck` CALLOUT: "Deck: squeezed by the stays" (CLM_773)
- B20A `B20A_note` NOTE: "Stone: strong under compression"
- B20B `B20B_note` NOTE: "Truss members: tension and compression"
- B20B `B20B_iron` NOTE: "Wrought iron: valued in tension and compression" (CLM_735)
- B20C `B20C_note` NOTE: "Timber: plentiful and cheap, but it decays"
- B20E `B20E_chain` NOTE: "Iron chains: only as strong as the weakest link" (CLM_780)
- B20E `B20E_cable` NOTE: "Wire cables, then high-strength steel" (CLM_781)
- B20E `B20E_model` NOTE: "Illustrative model"
- B22C `B22C_pier` COMPONENT_LABEL: "Main pier" (CLM_782)
- B22C `B22C_note` NOTE: "Hinged: superstructure could adjust if a pier sank" (CLM_782)
- B22C `B22C_model` NOTE: "Illustrative model"
- B22D `B22D_tacoma` NOTE: "Tacoma Narrows, 1940: lost to the wind" (CLM_783)
- B22D `B22D_stiff` NOTE: "Afterwards: research and stiffened decks" (CLM_783)
- B22D `B22D_truss` COMPONENT_LABEL: "Stiffening truss" (CLM_765)
- B22D `B22D_model` NOTE: "Illustrative model"
- B23D `B23D_anchor` COMPONENT_LABEL: "Anchorages: costly" (CLM_757)
- B23D `B23D_cable` COMPONENT_LABEL: "Main cables: specialist work" (CLM_787)
- B23D `B23D_model` NOTE: "Illustrative model"
- B23E `B23E_note` NOTE: "By 2012: erection methods better understood" (CLM_788)
- B27 `B27_note` NOTE: "Illustrative model, not the Carrollton Viaduct"
- B29 `B29_note` NOTE: "Illustrative model, not the Promontory trestle"
- B31A `B31A_note` NOTE: "Illustrative model, not the Niagara bridge"
- B31A `B31A_1855` NOTE: "Niagara Gorge, 1855: trains on a suspension bridge" (CLM_789)
- B31A `B31A_1890` NOTE: "Repaired 1877 and 1880; declared inadequate in 1890" (CLM_789)
- B31B `B31B_note` NOTE: "Illustrative model, not the Kentucky River bridge"
- B31B `B31B_rigid` NOTE: "Inherently rigid: suited to heavy trains" (CLM_790)
- B31B `B31B_1877` NOTE: "1877: the world's longest cantilever" (CLM_791)
- B31D `B31D_note` NOTE: "Illustrative model, not the Penobscot Narrows Bridge"
- B31D `B31D_fact` NOTE: "Penobscot Narrows, 2006: 430 ft concrete pylons" (CLM_793)
- B31D `B31D_42` NOTE: "42 months from conception to completion" (CLM_793)
- B32 `B32_ch` NOTE: "12 · Why they look different"
- B32 `B32_one` NOTE: "1 · How the structure carries load"
- B32L `B32L_one` NOTE: "1 · How the structure carries load"
- B34 `B34_note` NOTE: "Models are illustrations, not engineering designs"

## Bản ghi sửa câu (ASR / tốc độ đọc)

- B18.s2 (m7-r1): "By 1860, railroads relied almost entirely on these prefabricated parts." → "And by 1860, the railroads relied almost entirely on these prefabricated parts." (bm_george spoke it at 1.47 written words/s (below the 1.5 truncation guard; ASR text was exact))
- B20.s0 (m7-r1): "Start with materials." → "Start with the materials themselves." (very short sentence: trailing silence put it under the 1.5 words/s guard)
- B22.s0 (m7-r1): "The site matters too." → "The site of a bridge matters too." (very short sentence: trailing silence put it under the 1.5 words/s guard)
- B35.s0 (m7-r1): "Thanks for watching." → "Thank you very much for watching." (very short sentence: trailing silence put it under the 1.5 words/s guard)
- B15.s0 (m7-r1): "The truss takes yet another approach." → "A third approach is the truss." (ASR heard 'The Trust takes' (WER 0.17))
- B23.s2 (m7-r1): "spans two hundred and twenty feet, and some through trusses approach four hundred." → "spans 220 feet, and some through trusses approach 400." (numbers written as digits so the subtitles read '220' and ASR text matches (WER 0.23 from spelled-out numbers))
- B20B.s0-s1 (m7-r1): "A truss needs members that can work in tension as well as compression, and wrought iron was valued for exactly that: one historian calls it a material strong equally in tension and in compression." → "A truss needs members that can work in tension as well as compression. Wrought iron was valued for exactly that: one historian calls it a material strong equally in tension and in compression." (split in two so the picture can change with the second idea (15 s single-sentence hold))
- B35.s1 (m7-r1): "(none)" → "The sources and photo credits are listed in the description." (rough-cut review: the 6-line credits card was on screen for 4 s only)
- B01C.s0 (m8-r1): "Another hangs from great draped cables." → "Another hangs from huge draped cables." (ASR heard 'grate' (homophone; WER 0.17))
- B51.s0 (m8-r1): "Side by side, the difference is clear." → "Seen in outline, the difference is clear." (planner/consistency.py: 'side by side' promised two models on screen together, but the comparison is a diagram (two 72 m models do not read side by side at 640x360))
- B31A.s2 (m8-r3): "Their doubts were not unjustified: the bridge needed major repairs, was declared inadequate in 1890, and it would be 133 years before another suspension bridge was built for railway traffic." → "Their doubts were not unjustified: the bridge needed substantial repairs in 1877 and 1880, and it was declared inadequate in 1890." (owner's editorial review of 2026-11-04, item 1: the Williamsburg Bridge (1903) carried rail on its suspension deck (NYC DOT), so the report's '133 years' needs a restriction the source does not give; NOTE '133 years later' removed)
- B40.s1 (m8-r3): "Beam and arch bridges of steel or reinforced concrete were limited to spans of about 200 to 300 feet." → "Wide rivers like the Ohio and the Mississippi, and deep gorges like the one at Niagara, needed bridges that could reach farther." (owner's editorial review of 2026-11-04, item 2: the 200-300 ft limit had no period or conditions and contradicts the 1,800 ft arches of C10 (and the Eads Bridge, 1874, 520 ft); replaced by the source's own examples (CLM_752))
- B23C.s1-s3 (m8-r3): "In steel, a federal handbook puts plate girders at about 90 to over 500 feet, simple trusses at up to about 750, and cantilever trusses considerably farther. / Arches have spanned from about 200 to 1,800 feet, and cable-stayed bridges from under 200 to nearly 3,000." → "A 2012 federal handbook for steel bridges gives two kinds of numbers. / Some are practical ranges: ... / Others are spans that have actually been built: ..." (owner's editorial review of 2026-11-04, item 3: the card mixed practical/economic ranges with spans built and called all of them 'economic ranges'; the narration and the card now keep the two kinds apart (outlined vs solid bars))
- B24B.s2 (m8-r3): "... and since 1980 almost every American bridge with a main span over 1,000 feet has been cable-stayed." → "... and a 2012 federal handbook found that almost every American bridge built since 1980 with a main span over 1,000 feet was cable-stayed." (owner's editorial review of 2026-11-04, item 4: a 2012 statistic, now dated)
- B31D.s0 (m8-r3): "Today, the long-span answer in America is usually cable-stayed." → "In Maine, a modern cable-stayed bridge went up remarkably fast." (owner's editorial review of 2026-11-04, item 4: the present-tense claim dropped the conditions of CLM_774 (built in the U.S., main span over 1,000 ft, as of 2012))
- B33.s1-s2 (m8-r3): "Timber beam bridges are still built today, ... / And the most common steel bridge today is still a kind of beam: the welded plate girder." → "Timber beam bridges were still being built long after timber trusses, ... / And in 2012, a federal handbook still named a kind of beam, the welded plate girder, as the most common steel bridge." (owner's editorial review of 2026-11-04, item 4: 2005 and 2012 statements, now dated (card text too))
- B23E.s0 (m8-r3): "Cable-stayed bridges are becoming more common worldwide, and one significant reason is that the methods for erecting them are now better understood." → "By 2012, cable-stayed bridges were becoming more common worldwide, and one significant reason was that the methods for erecting them had become better understood." (owner's editorial review of 2026-11-04, item 4: a 2012 statement, now dated)
- B09.s1 (m8-r3): "... long after timber trusses fell out of use, and why they are still built on quiet rural roads and in parks today." → "... long after timber trusses stopped being competitive, and in 2005 a national report found them still being built on quiet rural roads and in parks." (owner's editorial review of 2026-11-04, item 4: a 2005 statement, now dated; 'fell out of use' was stronger than the source ('ceased to be competitive'))
- B20E.s2 (m8-r3): "... suspension and cable-stayed bridges now rely on high-strength steel cables." → "... suspension and cable-stayed bridges came to rely on high-strength steel cables." (same review, item 4 (present tense))
- B22C.s0-s1 (m8-r3): "Cantilevers had an advantage on uncertain ground. / Unstable soil troubled many foundations, and if a pier sank, a cantilever could adjust, where a continuous beam might fail." → "A cantilever like this one is a continuous girder with hinges built in, which made its forces easy to calculate. / So on unstable soil, if a pier sank, its superstructure could adjust, where a continuous beam might build up hidden stresses and fail." (owner's editorial review of 2026-11-04, item 5: the source attributes the advantage to the hinged, statically determinate form and to the superstructure)
- B22B (card) (m8-r3): "Suspension: cables anchored in massive blocks, set into rock" → "Suspension: cables anchored in massive blocks or in bedrock (one bank each); cable-stayed foundations drawn in the earth, rock deep" (owner's editorial review of 2026-11-04, item 6: the card said 'and' where the narration and CLM_761 say 'or')
- B44.s2 (m8-r3): "(none)" → "Unlike our model, it has no suspended span in the middle, something one report calls unique among cantilevers of its size." (owner's editorial review of 2026-11-04, item 7: the illustrative model (with a suspended span) is shown just before the Queensboro photograph (CLM_794))
- B03.s2 (m8-r3): "And it has to pass all of that down into the ground on either side." → "And it has to pass all of that down through its supports into the ground." (same review (minor): the load also reaches the ground through the piers)
- B51.s0-s2 (m8-r3): "Seen in outline, the difference is clear. / The suspension bridge has shorter towers ... / The cable-stayed bridge needs much taller towers ..." → "Drawn in outline at the same span, the two types differ. / ... much shorter towers ... / ... taller towers, because their height depends on the span ..." (same review (minor): the tower comparison holds at a comparable span (CLM_763, CLM_771); not an identification rule)
- B24B.s1 (m8-r3): "... the longest bridge in the world for many years." → "... the longest span in the world when it opened." (same review (minor): span, not total length; 'for many years' not corroborated (e-WV, Emory L. Kemp: 'the longest (1,010 feet) clear span in the world'))
- B48.s0-s1 (m8-r3): "Towers, cables and suspenders, anchorages and a stiffening truss: these are the features that define a suspension bridge. / The Brooklyn Bridge ... has them all, and one report says ..." → "The Brooklyn Bridge in New York, completed in 1883, was planned with two towers, cables and suspenders, anchorages and a stiffening truss. / One report says few suspension bridges built since ..." (same review (minor): the source lists these parts for the Brooklyn Bridge plan; B47 (FHWA) calls a stiffening truss only 'common')
- B31B.s0 (m8-r3): "Cantilevers, by contrast, were first used by the railroads." → "In America, modern cantilevers were first used by the railroads, and only later for highways." (same review (minor): the source speaks of the modern cantilever in the U.S. ('and then as highway bridges') and also describes ancient cantilevers)
