# Duyệt kịch bản: Could We Build an Entire City That Floats?

- Revision lời dẫn: `c-r1`; 8 chương, 44 beat, 127 câu, 1619 từ.
- Thời lượng đo từ audio đã khóa: khoảng **13.1 phút** (13:04).
- Hình: 4:58 là card 2D (38%) nếu giữ nguyên kế hoạch hiện tại.
- Card chỉ có chữ: dài nhất B15–B16, 58 giây liền.
- Claim: 50 claim được dùng, tất cả `SOURCE_VERIFIED`, **chưa claim nào được duyệt biên tập**.

# Ghi chú cho buổi đọc kịch bản c-r1 (agent soạn)

**Kịch bản c-r1 đã có:**
- lời dẫn hoàn chỉnh, sau review concept 2026-11-08 (sáu nhóm sửa, xem `review/REVIEW_C_R1.md`);
- audio nội bộ bằng Kokoro `am_michael`;
- timing đo từ audio.

**Chưa có:** asset, card hay hình nào. Kế hoạch hình báo `NEW_ASSET_REQUIRED` cho các beat 3D; đó là kết quả đúng ở giai đoạn này. Không có gì được duyệt. Bản nghe thử nằm ở `output/` (ngoài git) và không phải bản master.

## Cách đọc
- Mỗi câu dưới đây là câu đã được đọc thành tiếng.
- Cột claim chỉ ra câu dựa vào đâu:
  - nguồn ngoài (CLM_0xx);
  - phép tính minh họa của Studio (CLM_101–109, `analysis/RESULTS.md`);
  - giả định của kịch bản (CLM_121–125, `concept/SCENARIO_CONTRACT.md`).
- Mọi con số tính ra đều được nói là minh họa ("in this illustrative design", "about").

## Cần bạn quyết

1. **Thời lượng.** Bản đo từ audio dài **13:05** (784,9 s, gồm khoảng lặng của mỗi beat; chưa có thời gian cho hình), dài hơn mục tiêu 10–12 phút nhưng vẫn trong khoảng chấp nhận 8–15 phút. Nếu muốn về khoảng 11 phút, các chỗ cắt ít hại nhất là:
   - B16: câu về ụ khô Schoonschip;
   - B14: câu thứ hai (research agenda); B13 đã nêu yêu cầu cho mối nối;
   - B35 và B36: gộp thành một câu về sinh thái và một câu về quyền dùng mặt nước;
   - B37: phần so với đất liền còn một câu;
   - B27: câu thứ hai (cáp và bơm chống nước).

   Agent không tự cắt.
2. **Phát âm "Schoonschip".**
   - Whisper nghe Kokoro đọc thành "Schoenskip" và "scoonskip".
   - Tiếng Hà Lan đọc khác (âm "sch" và "g" họng). Chưa có override nào, vì một override cần nguồn phát âm và một buổi nghe của bạn.
   - Lựa chọn: giữ cách đọc tiếng Anh hóa hiện tại; thêm override sau khi bạn nghe; hoặc giảm số lần nhắc tên (hiện có ở B03, B07, B16, B26).
3. **Ảnh Schoonschip.**
   - Commons không có ảnh PD, CC0 hay CC BY nào của khu này. Ảnh khu vực gần đó đều là CC BY-SA.
   - Lựa chọn: (a) cho phép dùng CC BY-SA (quyết định ShareAlike của kênh); (b) xin phép Schoonschip hoặc Space&Matter; (c) giữ sơ đồ tự vẽ có nhãn "schematic".
4. **Đơn vị và chính tả.**
   - Lời dẫn dùng hệ mét, chính tả Mỹ (meters, tons, story) và chữ số cho số ≥ 100, như hai phim trước.
   - "Tons" ở đây là tấn mét. B07 nói rõ "metric tons" ở lần đầu.
5. **Giọng `am_michael` cho dự án này.** Duyệt của hai phim trước không tự áp sang.
6. **Claim:** 63 claim `SOURCE_VERIFIED` (gồm 9 phép tính và 5 giả định của Studio). Bạn duyệt claim mà phim dùng, khi kịch bản đã chốt.

## Điều agent đã tự kiểm (không thay cho việc bạn đọc và nghe)
- Rà từng câu theo câu hỏi bắt buộc của playbook: lời có khẳng định vượt bằng chứng không? Các câu đã sửa ghi ở `review/REVIEW_C_R1.md`.
- **ASR:** Whisper nghe lại từng câu: 127/127 đạt, sau khi đổi sang chính tả Mỹ và viết số ≥ 100 bằng chữ số. "Schoonschip" vẫn bị nghe sai chính tả, đúng như dự đoán với một tên tiếng Hà Lan. ASR không chứng minh được cách phát âm.
- **Đoạn thử hình** "thêm tầng → phao chìm → thân sâu hơn" (prototype P6, không lời): `renders/prototype/P6_add_storey_sink_fix_PROTOTYPE_INTERNAL_REVIEW.mp4`.

## Toàn bộ kịch bản

Lời dẫn là tiếng Anh, đúng câu chữ đã đọc. Mốc thời gian là ước tính từ audio đã khóa.

### C1 · Could We Actually Do This? (0:00)

**B01** · 0:00 · 3D, cần bộ sinh mới · không có claim

> 10,000 people, with homes, schools, a clinic, parks, and streets to walk along. And not one of them is standing on land.

- Hình: Establishing aerial of the finished illustrative district in a sheltered bay; NOTE 'Illustrative design'

**B02** · 0:10 · 3D, cần bộ sinh mới · không có claim

> Could we design a city like this, one that floats, stays where we put it, and keeps working? Let's treat it as a design problem, and solve it one step at a time.

- Hình: Slow push-in on the district; no claim on screen

**B03** · 0:24 · sơ đồ/card 2D · CLM_010, CLM_011, CLM_030, CLM_031, CLM_033, CLM_057

> Floating neighborhoods are not science fiction. In Amsterdam, a floating neighborhood called Schoonschip is home to 46 households, a little over 100 people. Much larger designs exist on paper. One, for 12,000 people off the coast of Busan in South Korea, was unveiled in 2022. When we checked the developer's and the architects' websites in November 2026, neither reported that construction had begun.

- Hình: Scale card: Schoonschip (built, ~100 people; schematic unless a licensed photo is approved), OCEANIX Busan (proposed 2022; 'status checked Nov 2026: OCEANIX news page, BIG project page')

**B04** · 0:58 · 3D, cần bộ sinh mới · không có claim

> So let's take our city apart, and build it back, one problem at a time.

- Hình: The district comes apart layer by layer (breakwater, moorings, utilities, buildings, platforms) until one empty platform remains

### C2 · The First Problem: Making Buildings Float (1:06)

**B05** · 1:06 · 3D, cần bộ sinh mới · CLM_002, CLM_008, CLM_101

> Problem one: how does something this heavy float at all? Take a block of concrete. As a solid lump, it sinks: concrete is more than twice as dense as seawater. Shape the same concrete into a hollow box, 40 meters on each side, and it floats.

- Hình: Section: the hull's concrete as a solid block on the seabed beside the same concrete as a floating box (draft from analysis)

**B06** · 1:27 · 3D, cần bộ sinh mới · CLM_001, CLM_102

> It floats because it pushes water out of the way, and the water it pushes aside weighs as much as the platform. Every ton we add needs roughly one more cubic meter of water pushed aside.

- Hình: Cutaway below the waterline: the displaced volume glows (prototype P1)

**B07** · 1:42 · sơ đồ/card 2D · CLM_012, CLM_013, CLM_103

> Real floating homes work exactly this way. The Schoonschip houses stand on concrete floats. The heaviest weighs around 340 to 350 metric tons, so it pushes aside roughly as many cubic meters of canal water: a cube about 7 meters on each side.

- Hình: House on its float beside a 7 m cube of water (schematic, labelled; 'two builders' figures')

**B08** · 2:05 · 3D, cần bộ sinh mới · CLM_104

> Our first platform, in this illustrative design, carries four blocks of three-story homes. Altogether it weighs about 4,800 tons, and floats about 3 meters deep. And here's the surprise: more than half of that weight is the concrete hull itself.

- Hình: Layers lift apart (homes, deck finishes, hull) with their share of the mass; label 'illustrative'

**B09** · 2:26 · 3D, cần bộ sinh mới · CLM_003, CLM_105

> Now add a fourth story. The platform settles about a third of a meter deeper, and the freeboard, the part of the hull above the water, shrinks from about a meter to about 70 centimeters.

- Hình: Close-up of the draft gauge: the fourth storey arrives, the platform sinks by the calculated amount (prototype P2b; new SINK step)

**B10** · 2:41 · 3D, cần bộ sinh mới · CLM_105

> One fix is to make the hull half a meter deeper. That adds about 100 tons of concrete, 4% more, and brings the freeboard back to about a meter and 15 centimeters. Lighter buildings would be another way.

- Hình: Same camera: the extra half metre of hull appears below, the deck rises to the calculated freeboard (same branch as B09)

**B11** · 3:01 · 3D, cần bộ sinh mới · CLM_009, CLM_106

> Will it tip over? Move 100 tons out toward the edge, and in this example the platform tilts by less than half a degree. But a small tilt under a shifted load tells us very little about how it will move in waves. Floating is only the first problem.

- Hình: A 100 t load slides to the edge; the platform tilts by the calculated small angle (no G, B, M symbols)

### C3 · Why One Platform Isn't a City (3:22)

**B12** · 3:22 · 3D, cần bộ sinh mới · CLM_108

> A platform like this holds about fifty people. For 10,000, we need a lot of them. So why not simply join them all into one enormous slab?

- Hình: Five platforms arrive around a small basin

**B13** · 3:35 · 3D, cần bộ sinh mới · CLM_107

> Look at two identical platforms carrying different buildings, one with two stories and one with four. Floating on their own, their decks would sit about 66 centimeters apart in height. So different loads add a demand on whatever connects them. In this design, the walkways between platforms are hinged, so they can follow the difference. Adding ballast to even out the decks would be another option.

- Hình: Side elevation: two decks at different heights; a hinged walkway spans them (no part shown as failing)

**B14** · 4:06 · 3D, cần bộ sinh mới · CLM_042, CLM_056

> Connections are where engineers expect trouble. A 2026 research agenda lists stress concentrations on connectors among the challenges of large floating developments. One concept study links its modules flexibly, and spaces them far enough apart not to collide, because on flexible moorings they are expected to move sideways quite a lot.

- Hình: Close-up of a joint: gap, hinged walkway, flexible utility link (conceptual geometry)

**B15** · 4:33 · sơ đồ/card 2D · CLM_124, CLM_108

> How many platforms would 10,000 people need? Say each resident needs about 40 square meters of floor: thirty for their home, and ten for a share of schools, shops and services. That's about thirty-three hectares of platform: about 200 platforms like our first one, with hundreds of connections between them.

- Hình: Plan grid: dots appear to ~209 platforms; joints counted (label 'illustrative')

**B16** · 4:58 · sơ đồ/card 2D · CLM_108, CLM_014, CLM_125

> Bigger platforms mean fewer connections. At 100 meters on a side, 34 would do, but each would weigh about 30,000 tons, to build, launch and tow. Even the Schoonschip floats were too big for the dry docks of traditional houseboat builders, and were cast on the quay instead. Our district uses 60-meter platforms, 93 of them: a middle choice for this illustration, not an optimum.

- Hình: Same-scale plans: 40 m, 60 m, 100 m modules with counts and masses

### C4 · The Water Never Stays Still (5:31)

**B17** · 5:31 · 3D, cần bộ sinh mới · không có claim

> And all of this sits on water that never keeps still. Each platform rises and falls on its own, and every gap and hinge between them has to cope.

- Hình: Five platforms move out of phase; gaps open and close; label 'Conceptual motion visualization — not a hydrodynamic simulation' (new CONCEPT_MOTION) | required label: 'Conceptual motion visualization — not a hydrodynamic simulation'

**B18** · 5:43 · sơ đồ/card 2D · CLM_022

> People living on the water feel it. Floating homes in the Netherlands can rock in storms, or when large cruise ships pass, and one Amsterdam resident feels it most on her upper floor.

- Hình: Floating home section; upper floor marked; source line (Yale E360, 2021)

**B19** · 5:59 · sơ đồ/card 2D · CLM_053

> Very large platforms don't only move. They bend, and predicting exactly how is still an open research problem.

- Hình: Long platform drawn flexing; 'exaggerated, conceptual'

**B20** · 6:09 · sơ đồ/card 2D · CLM_050, CLM_121

> So the first fix is where you build. A 2026 concept study looks for sea areas with limited fetch, near a gulf, a strait or an archipelago, where waves stay moderate. That's why our city sits in a sheltered bay, connected to an existing city on shore.

- Hình: Two schematic bays: sheltered vs open; the district placed in the sheltered one

**B21** · 6:31 · 3D, cần bộ sinh mới · CLM_055, CLM_051, CLM_052

> The second fix is the layout. Following one concept study, homes go in the middle, and functions that can tolerate more motion form the outer ring. Where the bay opens to the sea, a breakwater reduces the waves. But a floating breakwater may not be enough against longer waves from the open sea, and how much wave energy passes behind one is still hard to predict.

- Hình: Top view to three-quarter: inner homes glow, outer ring, breakwater arrives on the open side; NOTE 'reduces waves, does not remove storm risk'

### C5 · Keeping the City in Place (7:00)

**B22** · 7:00 · 3D, cần bộ sinh mới · CLM_020

> Something also has to hold the city in place. Floating homes in the Netherlands are fixed to the shore, often resting against steel poles.

- Hình: Water surface visible, then ghosted in a second step; piles glow (prototype P4)

**B23** · 7:11 · 3D, cần bộ sinh mới · CLM_041, CLM_122, CLM_109

> Water levels rise and fall, and a floating platform rises and falls with them, sliding along its poles. In our scenario, the water level can change by about 2 meters, so the bridges to shore need hinges: on a 25-meter bridge, the slope changes by about 3 degrees either way.

- Hình: Elevation: water rises, platform slides up its piles, the link-span turns on its shore hinge (new RISE/SINK step); '2 m range, assumed'

**B24** · 7:35 · 3D, cần bộ sinh mới · CLM_055, CLM_054

> Further out, the water is deeper, and piles give way to mooring lines anchored in the seabed. Deeper water means longer lines, deeper anchors, and higher costs. The seabed itself shapes the design, and the bill.

- Hình: Underwater, water ghosted: piles replaced by mooring lines toward deeper seabed; NOTE 'Conceptual mooring — not sized'

### C6 · A City Needs More Than Buildings (7:52)

**B25** · 7:52 · 3D, cần bộ sinh mới · không có claim

> So it floats, and it stays put. But is it a city yet? Fade out the buildings, and the city's other half appears.

- Hình: Buildings ghost; utility networks appear along the bridges

**B26** · 8:02 · sơ đồ/card 2D · CLM_016

> Power first: at Schoonschip, 46 households share a single connection to the national grid, with solar panels, a battery in every house, and a smart grid between them. Floating doesn't mean off-grid.

- Hình: Many homes, one cable to shore (schematic)

**B27** · 8:19 · 3D, cần bộ sinh mới · CLM_017, CLM_023, CLM_123

> Wastewater is separated there too: gray water from showers and washing machines, black water from toilets. Connecting floating homes to sewers on land takes extra infrastructure, such as waterproof cables and pumps. In our city, wastewater is pumped ashore along the bridges, and drinking water comes back the same way.

- Hình: One platform: grey and black lines, a pump, the line along the bridge

**B28** · 8:45 · 3D, cần bộ sinh mới · CLM_043

> Transport, fire and medical services, and food all follow the same logic. A large floating development has to connect sewage, power and roads to land, or develop alternatives of its own, and our city connects.

- Hình: Boat landings, two routes to land from each platform, rescue-boat berth glow in turn

### C7 · What Would Actually Make This Difficult? (9:03)

**B29** · 9:03 · 3D, cần bộ sinh mới · không có claim

> Everything so far assumed sheltered water close to a city. So what happens if we tow it out to sea?

- Hình: Small 3D district on an open sea (counterfactual); label 'Counterfactual'

**B30** · 9:12 · 3D, cần bộ sinh mới · CLM_051, CLM_054

> Longer waves arrive, and a floating breakwater may not be enough against them. Below the surface, the seabed drops away, so mooring lines get longer and anchors deeper.

- Hình: Same open-sea scene: long conceptual swell passes the breakwater (labelled); water ghosts, lines lengthen to a deeper seabed | required label: 'Conceptual motion visualization — not a hydrodynamic simulation'

**B31** · 9:26 · 3D, cần bộ sinh mới · CLM_043, CLM_051

> Further from shore, cables, pipes and supply ships can still reach the city, but every link becomes longer and more exposed.

- Hình: The links to shore stretch across open water and glow

**B32** · 9:37 · sơ đồ/card 2D · CLM_058

> And if we also asked the city to supply itself, as one 2026 offshore concept does, it would need its own systems for energy, water and food. In that study, growing food alone accounts for nearly half of the city's estimated energy use.

- Hình: An added condition: three systems appear; 'one concept study's estimate'

**B33** · 9:58 · 3D, cần bộ sinh mới · CLM_062

> That study also uses a different kind of hull: semi-submersible platforms, with the deck raised above the sea on columns, behind a floating barrier. Offshore isn't the same city moved further out. It's a different design.

- Hình: 3D: our box pontoon beside a column-stabilised module (schematic, labelled 'concept study')

**B34** · 10:16 · 3D, cần bộ sinh mới · CLM_059

> Some difficulties remain wherever we build. Concrete in seawater needs watching: chlorides can corrode the steel reinforcement, and, according to a 2026 study, there are no dedicated standards for floating cities yet.

- Hình: Hull surface, inspection zone glows (no damage shown)

**B35** · 10:35 · 3D, cần bộ sinh mới · CLM_044

> Large floating developments change the light, shade and water movement beneath them, effects that researchers say still need study, and they expect the impact on local ecology to be far larger than that of small developments.

- Hình: Underwater view: the district's shadow on the seabed (EEVEE shadow, illustrative)

**B36** · 10:52 · 3D, cần bộ sinh mới · CLM_045, CLM_046

> And who gets to use the water? How districts like this fit into planning law is not yet known, and researchers warn they could end up serving the wealthy, and fencing off water that used to be public.

- Hình: Two waterfront edges: public path vs fenced edge

**B37** · 11:08 · sơ đồ/card 2D · CLM_063, CLM_041, CLM_054, CLM_042, CLM_059

> And what would it cost? We do not yet have a reliable cost estimate for this design. The one published framework we found is preliminary, and covers only flotation and energy. Compared with land, floating structures can follow the water level, and can be moved or reused, but they trade a fixed foundation for moorings, connections and ongoing maintenance.

- Hình: Two columns: what floating gives, what it costs (no numbers)

### C8 · Could We Really Build It? (11:36)

**B38** · 11:36 · 3D, cần bộ sinh mới · không có claim

> From one platform to a district, every part we added answers a question we had to ask.

- Hình: Platform A alone, then beside district C; one label per added system

**B39** · 11:44 · sơ đồ/card 2D · CLM_010, CLM_011, CLM_016

> So, could we build an entire city that floats? Small floating neighborhoods, connected to the shore in sheltered water, already exist.

- Hình: Verdict tier 1 of 3 (elements appear with the words)

**B40** · 11:55 · sơ đồ/card 2D · CLM_121, CLM_053, CLM_042, CLM_063, CLM_033

> A connected district for 10,000 people, in a sheltered bay, built step by step, may be possible under the right conditions. But how very large platforms bend, how their connections hold up, and what they would cost are still open questions. And the one project of that size we checked had not been reported as under construction when we looked. We didn't survey every project in the world.

- Hình: Verdict tier 2 of 3

**B41** · 12:25 · sơ đồ/card 2D · CLM_051, CLM_058, CLM_062

> A city far out at sea, especially one that has to supply itself, remains much more speculative.

- Hình: Verdict tier 3 of 3

**B42** · 12:34 · 3D, cần bộ sinh mới · CLM_104, CLM_121

> Our arithmetic shows what it takes for a platform to float. Whether a whole district works depends on the site, and on every other system we added.

- Hình: Closing aerial of the district (re-uses the opening scene)

**B43** · 12:46 · sơ đồ/card 2D · không có claim

> Which structure should we explain next? Suggest a topic in the comments. And if you enjoyed this film, please like it and subscribe.

- Hình: Closing call to action with self-drawn icons (comment, like, subscribe, bell) as each is asked; no platform logo or trademark

**B44** · 12:58 · sơ đồ/card 2D · không có claim

> Thank you for watching. The sources are listed in the description.

- Hình: Credits; AI-voice disclosure; 'Models are illustrative, not engineering designs'

## Các claim phim dùng

`medium` = chỉ có hoặc chủ yếu dựa vào nguồn thứ cấp, hoặc các nguồn lệch nhau. Nên xem kỹ các mục này.

| Claim | Tin cậy | Nội dung | Nguồn | Giả định, giới hạn |
|---|---|---|---|---|
| CLM_001 | high | A floating object is pushed up by a force equal to the weight of the water it displaces (Archimedes' principle). | SRC_OPENSTAX_UP1_14_4, SRC_TUDELFT_OHM_HYDROSTATICS |  |
| CLM_002 | high | Shape decides whether something floats: a lump of clay sinks, the same clay shaped like a boat floats, and so do steel ships. | SRC_OPENSTAX_UP1_14_4 |  |
| CLM_003 | high | A loaded vessel sits deeper in the water than the same vessel unloaded. | SRC_OPENSTAX_UP1_14_4 |  |
| CLM_008 | high | Reference densities: concrete about 2,400 kg/m³, fresh water at 20 °C about 998 kg/m³, sea water at 0 °C about 1,030 kg/m³. | SRC_OPENSTAX_UP1_14_1 | Textbook reference values; real concrete mixes and sea water vary. The scenario uses 1025 kg/m3 for sea water (CLM_004) and 1000 kg/m3 for canal water (rounded). |
| CLM_009 | high | Moving a weight sideways on a floating body makes it list until the shifted centre of gravity is balanced: for small angles GM = w·d / (W·tan θ). A vessel can also be excessively stable. | SRC_MIT_13012_READING3 | Ship-design guidance; the film uses the relation, not the ship GM rule of thumb (3–5% of beam). |
| CLM_010 | high | Schoonschip in Amsterdam is a floating neighbourhood of 46 households on 30 water plots; its houses were finished in 2020 and the neighbourhood was officially finished in 2021. | SRC_SCHOONSCHIP_ORG, SRC_SM_SCHOONSCHIP | The two sources give 2020 (houses finalised) and 2021 (officially finished); the film says 'finished in 2020–2021' or names both. |
| CLM_011 | high | Schoonschip is home to a little more than 100 residents. | SRC_SCHOONSCHIP_ORG |  |
| CLM_012 | high | Each Schoonschip home sits on a concrete float built of double-reinforced concrete floors and walls. | SRC_STEDENBOUW_FLOATS_2019, SRC_STEDENBOUW_LAUNCH_2019 |  |
| CLM_013 | high | The heaviest Schoonschip home weighs about 340 to 350 tonnes (two builders' figures). | SRC_STEDENBOUW_FLOATS_2019, SRC_STEDENBOUW_LAUNCH_2019 | Two sources, two values; the film says 'about 340 to 350 tonnes' and does not pick one. |
| CLM_014 | high | The Schoonschip homes were built on the quay, launched and towed to their plots in the canal; their floats were too big and heavy for the dry docks of traditional ark builders. | SRC_STEDENBOUW_FLOATS_2019, SRC_STEDENBOUW_LAUNCH_2019 |  |
| CLM_016 | high | Schoonschip's 46 households share one connection to the national grid; every house has solar panels, a battery and a link to a shared smart grid. | SRC_SCHOONSCHIP_ORG |  |
| CLM_017 | high | Schoonschip separates grey water from black water; turning the black water into energy in a floating digester was described as a planned pilot. | SRC_SCHOONSCHIP_ORG | The digester is a plan on the residents' site; the film must not present it as operating. |
| CLM_020 | high | Dutch floating homes are usually fixed in place, often against steel poles, and connected to the sewer and power grid on land. | SRC_YALE_E360_2021 |  |
| CLM_022 | high | Residents feel floating homes move in storms and in the wakes of large ships, most on upper floors. | SRC_YALE_E360_2021 |  |
| CLM_023 | high | Connecting floating homes to the grid and sewer needs extra infrastructure, such as waterproof cables and pumps. | SRC_YALE_E360_2021 |  |
| CLM_030 | high | OCEANIX Busan, designed by BIG with SAMOO, was unveiled at the United Nations in April 2022 as a prototype for a floating community. | SRC_BIG_OCEANIX_BUSAN |  |
| CLM_031 | high | As designed, OCEANIX Busan's interconnected platforms total 15.5 acres for a community of 12,000 people, in three neighbourhoods for living, research and lodging, linked to land by link-span bridges around a sheltered lagoon. | SRC_BIG_OCEANIX_BUSAN | Design figures; 12,000 is 'residents and visitors' elsewhere on the same page. |
| CLM_033 | medium | We found no official report that construction of OCEANIX Busan has started: the developer's news page lists plans and press coverage (latest footer 2024), and a 2026 study still described it as expected, with a 2025 completion date that has passed. | SRC_BIG_OCEANIX_BUSAN, SRC_CEE_2026_RUZZO, SRC_OCEANIX_NEWS | Absence of a report is not proof. The check covered OCEANIX's own news page and BIG's project page on 2026-11-08 (UN-Habitat and Busan pages could not be opened). It is about this project only: it does not show that no 10,000-person floating district exists anywhere. The film names what was checked and when. |
| CLM_041 | high | Floating structures can follow changing water levels and can be relocated or repurposed, which land reclamation cannot. | SRC_NCOMMS_2026_TEN_QUESTIONS |  |
| CLM_042 | high | Large floating developments face a complex hydro-elastic response, stress concentrations at connectors and high global environmental loads; reducing global and mooring loads, for example with dissipative floating breakwaters, is a key need. | SRC_NCOMMS_2026_TEN_QUESTIONS |  |
| CLM_043 | high | Large floating developments must connect sewage, power cables and roads to land, or develop off-grid alternatives. | SRC_NCOMMS_2026_TEN_QUESTIONS |  |
| CLM_044 | high | Large floating developments will affect local ecology far more than small ones: light, shade and water flow change, and non-native species, corrosion, waste and biofouling need study. | SRC_NCOMMS_2026_TEN_QUESTIONS |  |
| CLM_045 | high | How large floating developments fit existing spatial policy, legislation and regulation is not yet known. | SRC_NCOMMS_2026_TEN_QUESTIONS |  |
| CLM_046 | high | Floating urbanisation risks serving the wealthy and enclosing water that used to be common public space. | SRC_NCOMMS_2026_TEN_QUESTIONS |  |
| CLM_050 | high | A 2026 floating-city concept study places its city ideally in a limited-fetch sea area, near a gulf, strait or archipelago, for moderate waves and water depth and an easier link to the mainland. | SRC_CEE_2026_RUZZO |  |
| CLM_051 | high | Floating breakwaters may not be enough against the longer waves of exposed sea areas, from storms or long swells. | SRC_CEE_2026_RUZZO | From the study's simplified preliminary assessment; the film says 'may not be enough', never 'cannot'. |
| CLM_052 | high | Predicting how much wave energy passes a floating breakwater is complex and partly unresolved. | SRC_CEE_2026_RUZZO |  |
| CLM_053 | high | Describing how very large floating structures bend and flex in waves (hydro-elasticity) is complex and partly an open challenge; common linear software neglects or simplifies non-linear effects such as connector behaviour under large displacements. | SRC_CEE_2026_RUZZO |  |
| CLM_054 | high | Mooring cost depends mainly on water depth and seabed: deeper water means longer lines and deeper anchors, with costs that rise faster than the depth. | SRC_CEE_2026_RUZZO |  |
| CLM_055 | high | The study proposes redundant, compliant moorings (shared catenary or taut lines) for its inner modules, and puts residential modules inside, behind modules where larger motions are tolerated. | SRC_CEE_2026_RUZZO |  |
| CLM_056 | high | In the study's layout, modules are flexibly connected and spaced far enough apart to avoid contact, because relatively large horizontal motions are expected on compliant moorings; propellers are envisaged as back-up positioning to avoid contacts and overloading of the connections. | SRC_CEE_2026_RUZZO | c-r1 correction: the 'avoid contacts and overloading' clause belongs to the propellers (back-up positioning), not to the flexible links. |
| CLM_057 | high | The study's 50,000-inhabitant concept uses square functional modules about 300 m on a side, each for about 3,000 people, sixteen of them in all. | SRC_CEE_2026_RUZZO | ~1500 inhabitants per triangular module, two per square module (Results). |
| CLM_058 | high | The study estimates its 50,000-person city would use about 470 GWh of final energy a year under conservative hypotheses, nearly half of it for local food production. | SRC_CEE_2026_RUZZO | Depends on the study's autonomy goal (local food and water); not a requirement of the Studio scenario. |
| CLM_059 | high | Reinforced concrete in seawater suffers chloride-induced corrosion of the steel bars, which can compromise safety and need expensive repairs; dedicated standards for floating cities are currently absent. | SRC_CEE_2026_RUZZO |  |
| CLM_062 | high | For its offshore city the 2026 concept study uses semi-submersible inner modules on compliant moorings, with the deck raised above the sea on columns, behind a moored floating barrier. | SRC_CEE_2026_RUZZO |  |
| CLM_063 | high | A 2026 concept study proposes only a simplified, preliminary cost framework for a floating city, limited to flotation and energy systems, and notes that the only cost source it knew of was a project report with limited justification that is not peer-reviewed. | SRC_CEE_2026_RUZZO | Owner review 2026-11-08: a framework exists (this study), so the film must not say 'no cost basis'. It says the Studio has no reliable cost estimate for its own design. |
| CLM_101 | high | In the illustrative design, the hull's 1,108 m³ of concrete would sink as a solid block (concrete is about 2.3 times denser than seawater) but floats when shaped into a 40 × 40 × 4 m box. | SRC_STUDIO_DESIGN_MODEL | Illustrative: an idealised concrete box in still water under the scenario's assumptions; not a design result. |
| CLM_102 | high | Each tonne added needs about one more cubic metre of water displaced (0.98 m³ of seawater, 1.0 m³ of canal water). | SRC_STUDIO_DESIGN_MODEL |  |
| CLM_103 | high | A 340–350-tonne floating home displaces about 340–350 m³ of canal water, a cube about 7 m on each side. | SRC_STUDIO_DESIGN_MODEL |  |
| CLM_104 | high | The illustrative first platform (40 × 40 m, 4 m deep, three-storey homes) weighs about 4,850 t and floats about 3 m deep; more than half of that is the concrete hull. | SRC_STUDIO_DESIGN_MODEL | Illustrative: an idealised concrete box in still water under the scenario's assumptions; not a design result. |
| CLM_105 | high | Adding a fourth storey sinks the illustrative platform about a third of a metre deeper and cuts its freeboard from about 1.04 m to about 0.71 m; a hull 0.5 m deeper (about 106 t, 4% more concrete) brings the freeboard back to about 1.15 m. | SRC_STUDIO_DESIGN_MODEL | Illustrative: an idealised concrete box in still water under the scenario's assumptions; not a design result. One branch: the same building dead load (0.6 t/m² of floor) in every step. |
| CLM_106 | high | Moving 100 t to 15 m from the centre tilts the illustrative platform by about 0.4 degrees (small-angle relation). | SRC_STUDIO_DESIGN_MODEL | Illustrative: an idealised concrete box in still water under the scenario's assumptions; not a design result. Says nothing about motion in waves. |
| CLM_107 | high | Two identical illustrative platforms floating independently, one with two storeys and one with four, would have decks about 0.66 m apart in height. | SRC_STUDIO_DESIGN_MODEL | Illustrative: an idealised concrete box in still water under the scenario's assumptions; not a design result. Independent platforms: a rigid link would change both equilibria, so this does not show that a rigid link fails. |
| CLM_108 | high | At 40 m² of floor per resident, 10,000 people need about 33 ha of platform: about 209 platforms 40 m wide (about 48 people each), 93 at 60 m, or 34 at 100 m, each of the last weighing about 30,000 t. | SRC_STUDIO_DESIGN_MODEL | Illustrative: an idealised concrete box in still water under the scenario's assumptions; not a design result. |
| CLM_109 | high | With a 2 m water-level range, the slope of a 25 m hinged bridge to shore changes by about 3 degrees either way. | SRC_STUDIO_DESIGN_MODEL | Illustrative: an idealised concrete box in still water under the scenario's assumptions; not a design result. |
| CLM_121 | high | The scenario: a shore-connected floating district for 10,000 residents in a sheltered bay, built in phases. | SRC_STUDIO_SCENARIO |  |
| CLM_122 | high | The scenario assumes a water-level range of about 2 m (tide plus surge), for illustration. | SRC_STUDIO_SCENARIO |  |
| CLM_123 | high | In the scenario, wastewater is separated and pumped ashore, and drinking water comes from the city mains along the bridges. | SRC_STUDIO_SCENARIO |  |
| CLM_124 | high | The scenario counts 40 m² of floor per resident: 30 m² of home and 10 m² of schools, clinic, shops and services. | SRC_STUDIO_SCENARIO |  |
| CLM_125 | high | The illustrative district uses 60 m platforms, 93 of them: a middle choice, not an optimum. | SRC_STUDIO_SCENARIO |  |
