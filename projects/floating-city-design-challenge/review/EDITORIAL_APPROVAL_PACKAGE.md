# Gói duyệt biên tập: "Could We Build an Entire City That Floats?" (narration `c-r2`)

> **Đã duyệt claim:** Tran Nam Anh (channel owner) duyệt 50 claim được lời dẫn dùng, ngày 2026-11-08, cho narration `c-r2` (`research/editorial_approval.json`). Agent chỉ ghi lại quyết định. Phát âm và quyền giọng cho phim vẫn là các bước duyệt riêng; tới khi đủ, mọi bản dựng mang nhãn INTERNAL REVIEW.

## Cần chủ kênh quyết định

1. Lời dẫn: mỗi câu đúng với claim nó trích (xem cột trích dẫn nguồn).
2. Chữ trên card: tiêu đề, nhãn, chú thích ảnh, thang nhịp và dòng thời gian.
3. Ảnh lưu trữ: chọn ảnh, cách cắt viền phim, dòng ghi công (xem `review/RIGHTS_PROVENANCE.md`).
4. Nhãn 'Illustrative model' trên các mô hình 3D (không có).
5. Phát âm các tên mới (narration.voice.pronunciation_review.terms).
6. Giọng: duyệt `am_michael` hiện có (Tran Nam Anh (channel owner), 2026-11-08; theo dự án) vẫn áp dụng cho revision này: xác nhận lại hoặc rút.

Cách ghi quyết định (agent chỉ ghi lại lời chủ kênh; xem `docs/production/NEW_DOCUMENTARY_PLAYBOOK.md` bước 23): `research/editorial_approval.json` (id claim, `claims_text_sha256`, `narration_revision` của revision này), rồi chạy `research/build_sources.py`; `project.json` → `factual_review: verified`; `narration.voice.pronunciation_review` (`ACCEPTED_BY_OWNER` hoặc `CONFIRMED`, gắn với hash audio); `review/OWNER_APPROVALS.json`.

## Các điểm cần lưu ý (agent tự nêu)

- Không có.

## Lời dẫn theo câu


### C1 · Could We Actually Do This?

**B01** (framing; claim: không, câu dẫn dắt)

- `0:00` 10,000 people, with homes, schools, a clinic, parks, and streets to walk along.
- `0:06` And not one of them is standing on land.

**B02** (framing; claim: không, câu dẫn dắt)

- `0:11` Could we design a city like this, one that floats, stays where we put it, and keeps working?
- `0:18` Let's treat it as a design problem, and solve it one step at a time.

**B03** (fact; claim: CLM_010, CLM_011, CLM_030, CLM_031, CLM_034, CLM_057)

- `0:24` Floating neighborhoods are not science fiction.
- `0:28` In Amsterdam, a floating neighborhood called Schoonschip is home to 46 households, a little over 100 people.
- `0:37` Much larger designs exist on paper.
- `0:41` One, for 12,000 people off the coast of Busan in South Korea, was unveiled in 2022,
- `0:49` and when we checked in November 2026, its architects still listed it as in design.
  - CLM_010: SRC_SM_SCHOONSCHIP project text: "Officially finished in 2021, the neighborhood comprises 30 water plots with 46 unique homes" · SRC_SCHOONSCHIP_ORG home page: "we live with 46 households, on 30 arks." · SRC_SCHOONSCHIP_ORG timeline: "In the year 2020 all floating houses at Schoonschip were finalised." — giả định: The two sources give 2020 (houses finalised) and 2021 (officially finished); the film says 'finished in 2020–2021' or names both.
  - CLM_011: SRC_SCHOONSCHIP_ORG about: "Schoonschip offers a place of residence for 46 households and a bit more than 100 residents, in all ages."
  - CLM_030: SRC_BIG_OCEANIX_BUSAN text block 1: "prototype for a resilient and sustainable floating community. The project was unveiled at the Second UN Roundtable on Sustainable Floating Cities at The United Nations in April 2022"
  - CLM_031: SRC_BIG_OCEANIX_BUSAN text block 3: "Located off the coast of Busan, the interconnected platforms total 15.5 acres for a community of 12,000 people. Each neighborhood is designed to serve a specific purpose – living, research, and lodging." · SRC_BIG_OCEANIX_BUSAN text block 3: "The floating platforms connect to land with link-span bridges, framing the sheltered blue lagoon" — giả định: Design figures; 12,000 is 'residents and visitors' elsewhere on the same page.
  - CLM_034: SRC_BIG_OCEANIX_BUSAN project facts (page text): "Status In Design" — giả định: A status label on the architects' website on the date checked; BIG's other labels include 'In Construction' and 'Completed'. It says nothing about other projects worldwide.
  - CLM_057: SRC_CEE_2026_RUZZO Results: "The functional modules are square, with ~300 m-long sides" · SRC_CEE_2026_RUZZO Results: "for a total of ~1500 inhabitants" · SRC_CEE_2026_RUZZO Results: "The 50,000-inhabitants sample city is made up of sixteen square functional modules" — giả định: ~1500 inhabitants per triangular module, two per square module (Results).

**B04** (framing; claim: không, câu dẫn dắt)

- `0:57` So let's take our city apart,
- `0:59` and build it back, one problem at a time.


### C2 · The First Problem: Making Buildings Float

**B05** (fact; claim: CLM_002, CLM_008, CLM_101)

- `1:04` Problem one: how does something this heavy float at all?
- `1:08` Take a block of concrete.
- `1:11` As a solid lump, it sinks: concrete is more than twice as dense as seawater.
- `1:17` Shape the same concrete into a hollow box, 40 meters on each side, and it floats.
  - CLM_002: SRC_OPENSTAX_UP1_14_4 Density and Archimedes' Principle: "If you drop a lump of clay in water, it will sink. But if you mold the same lump of clay into the shape of a boat, it will float." · SRC_OPENSTAX_UP1_14_4 Density and Archimedes' Principle: "The same is true of steel ships."
  - CLM_008: SRC_OPENSTAX_UP1_14_1 Table 14.1: "Concrete 2.40×1032.40×103" · SRC_OPENSTAX_UP1_14_1 Table 14.2: "Water (20°C)(20°C) 9.982×1029.982×102" · SRC_OPENSTAX_UP1_14_1 Table 14.2: "Sea water (0°C)(0°C) 1.030×1031.030×103" — giả định: Textbook reference values; real concrete mixes and sea water vary. The scenario uses 1025 kg/m3 for sea water (CLM_004) and 1000 kg/m3 for canal water (rounded).
  - CLM_101: SRC_STUDIO_DESIGN_MODEL §1, clay boat: "1108.0 m³ bê tông của thân phao, nếu đúc đặc là khối lập phương cạnh 10.35 m, đặc hơn nước biển 2.34 lần, chìm; làm thành hộp 40 × 40 × 4 m thì nổi với mớn nước 1.621 m (chưa có nhà)." — giả định: Illustrative: an idealised concrete box in still water under the scenario's assumptions; not a design result.

**B06** (fact; claim: CLM_001, CLM_102)

- `1:25` It floats because it pushes water out of the way, and the water it pushes aside weighs as much as the platform.
- `1:33` Every ton we add needs roughly one more cubic meter of water pushed aside.
  - CLM_001: SRC_OPENSTAX_UP1_14_4 14.4, Archimedes' Principle box: "The buoyant force on an object equals the weight of the fluid it displaces." · SRC_TUDELFT_OHM_HYDROSTATICS Hydrostatics slide: "The weight of an floating body is equal to the weight of the fluid it displaces"
  - CLM_102: SRC_STUDIO_DESIGN_MODEL §1: "Nước biển 1.025 kg/m³: 0.9756 m³ mỗi tấn; nước kênh 1.000 kg/m³: 1.0 m³."

**B07** (fact; claim: CLM_012, CLM_013, CLM_103)

- `1:40` Real floating homes work exactly this way.
- `1:44` The Schoonschip houses stand on concrete floats.
- `1:48` The heaviest weighs around 340 to 350 metric tons,
- `1:54` so it pushes aside roughly as many cubic meters of canal water: a cube about 7 meters on each side.
  - CLM_012: SRC_STEDENBOUW_FLOATS_2019 paragraph 1: "Every new home, ark or office on the water starts with a concrete hull." · SRC_STEDENBOUW_FLOATS_2019 paragraph 2: "Hercules Floating Concrete realized practically all the concrete floats for the 30 waterfront lots" · SRC_STEDENBOUW_FLOATS_2019 paragraph 2: "The floats consist of double-reinforced concrete floors and walls, on which the contracting parties built the homes." · SRC_STEDENBOUW_LAUNCH_2019 Van der Zande quote: "At the base of each home are a concrete float and a wood-frame construction structure" — giả định: c-r2 claim review (owner): the reinforcement detail is the float maker's description of its own floats (practically all), not a statement about every float.
  - CLM_013: SRC_STEDENBOUW_FLOATS_2019 last paragraph: "The heaviest house - with a total weight of 340 tons - was placed in the water in early May." · SRC_STEDENBOUW_LAUNCH_2019 launch paragraph: "the heaviest home weighs 350,000 kilograms" — giả định: Two sources, two values; the film says 'about 340 to 350 tonnes' and does not pick one.
  - CLM_103: SRC_STUDIO_DESIGN_MODEL §1: "chiếm chỗ 340.0–350.0 m³ nước kênh, tức một khối lập phương cạnh khoảng 6.98–7.05 m."

**B08** (fact; claim: CLM_104)

- `2:03` Our first platform, in this illustrative design, carries four blocks of three-story homes.
- `2:10` Altogether it weighs about 4,800 tons, and floats about 3 meters deep.
- `2:17` And here's the surprise: more than half of that weight is the concrete hull itself.
  - CLM_104: SRC_STUDIO_DESIGN_MODEL §2 table, mid case: "| 0.6 (giữa) | 4851.2 | 3.032 | 2.958 | 1.042 |" · SRC_STUDIO_DESIGN_MODEL §2: "Bê tông thân phao chiếm 55% khối lượng (phương án giữa)" — giả định: Illustrative: an idealised concrete box in still water under the scenario's assumptions; not a design result.

**B09** (fact; claim: CLM_003, CLM_105)

- `2:24` Now add a fourth story.
- `2:27` The platform settles about a third of a meter deeper,
- `2:31` and the freeboard, the part of the hull above the water, shrinks from about a meter to about 70 centimeters.
  - CLM_003: SRC_OPENSTAX_UP1_14_4 Figure 14.22 discussion: "the unloaded ship has a lower density and less of it is submerged compared with the same ship when loaded"
  - CLM_105: SRC_STUDIO_DESIGN_MODEL §8 row 1: "| 3 storeys, hull 4.0 m | 4851.2 | 2.958 | 1.042 |" · SRC_STUDIO_DESIGN_MODEL §8 row 2: "| 4 storeys, hull 4.0 m | 5395.2 | 3.29 | 0.71 |" · SRC_STUDIO_DESIGN_MODEL §8 row 3: "| 4 storeys, hull 4.5 m | 5500.8 | 3.354 | 1.146 |" · SRC_STUDIO_DESIGN_MODEL §8: "Thân sâu thêm 0,5 m tốn thêm 105.6 t bê tông (4.0% bê tông thân phao)." — giả định: Illustrative: an idealised concrete box in still water under the scenario's assumptions; not a design result. One branch: the same building dead load (0.6 t/m² of floor) in every step.

**B10** (fact; claim: CLM_105)

- `2:40` One fix is to make the hull half a meter deeper.
- `2:44` That adds about 100 tons of concrete, 4% more,
- `2:50` and brings the freeboard back to about a meter and 15 centimeters.
- `2:55` Lighter buildings would be another way.
  - CLM_105: SRC_STUDIO_DESIGN_MODEL §8 row 1: "| 3 storeys, hull 4.0 m | 4851.2 | 2.958 | 1.042 |" · SRC_STUDIO_DESIGN_MODEL §8 row 2: "| 4 storeys, hull 4.0 m | 5395.2 | 3.29 | 0.71 |" · SRC_STUDIO_DESIGN_MODEL §8 row 3: "| 4 storeys, hull 4.5 m | 5500.8 | 3.354 | 1.146 |" · SRC_STUDIO_DESIGN_MODEL §8: "Thân sâu thêm 0,5 m tốn thêm 105.6 t bê tông (4.0% bê tông thân phao)." — giả định: Illustrative: an idealised concrete box in still water under the scenario's assumptions; not a design result. One branch: the same building dead load (0.6 t/m² of floor) in every step.

**B11** (fact; claim: CLM_009, CLM_106)

- `2:59` Will it tip over?
- `3:01` Move 100 tons out toward the edge, and in this example the platform tilts by less than half a degree.
- `3:09` But a small tilt under a shifted load tells us very little about how it will move in waves.
- `3:16` Floating is only the first problem.
  - CLM_009: SRC_MIT_13012_READING3 inclining experiment: "Take a vessel floating on the free surface and place a weight directly over the center of gravity. The ship will settle slightly deeper into the water but not roll." · SRC_MIT_13012_READING3 after the formula: "where w is the mass of the weight (lbs), d is the distance (inches) the weight is moved, W is the displacement of the vessel (lbs) and tan θ is the tangent of the roll (list) angle." · SRC_MIT_13012_READING3 after the formula: "Larger values can make a ship excessively stable." — giả định: Ship-design guidance; the film uses the relation, not the ship GM rule of thumb (3–5% of beam).
  - CLM_106: SRC_STUDIO_DESIGN_MODEL §2: "Dời 100 t ra cách tâm 15 m: nghiêng khoảng 0.421° (công thức góc nhỏ, CLM_009)." — giả định: Illustrative: an idealised concrete box in still water under the scenario's assumptions; not a design result. Says nothing about motion in waves.


### C3 · Why One Platform Isn't a City

**B12** (fact; claim: CLM_108)

- `3:21` Let's go back to the three-story version. A platform like this holds about 50 people.
- `3:27` For 10,000, we need a lot of them.
- `3:31` So why not simply join them all into one enormous slab?
  - CLM_108: SRC_STUDIO_DESIGN_MODEL §4 table: "| 40 | 33.3 ha | 33.3 | 209 | 48 |" · SRC_STUDIO_DESIGN_MODEL §6b: "Phao 40 m: 3 tầng 48 người, 4 tầng 64 người" · SRC_STUDIO_DESIGN_MODEL §5 table: "| 100m | 34 | 60 | 29,564 | 300 |" · SRC_STUDIO_DESIGN_MODEL §9: "93 phao, 33.5 ha" — giả định: Illustrative: an idealised concrete box in still water under the scenario's assumptions; not a design result.

**B13** (fact; claim: CLM_107)

- `3:36` Look at two identical platforms carrying different buildings, one with two stories and one with four.
- `3:44` Floating on their own, their decks would sit about 66 centimeters apart in height.
- `3:50` So different loads add a demand on whatever connects them.
- `3:55` In this design, the walkways between platforms are hinged, so they can follow the difference.
- `4:02` Adding ballast to even out the decks would be another option.
  - CLM_107: SRC_STUDIO_DESIGN_MODEL §7: "hai phao giống nhau, nhà 2 tầng và 4 tầng: mớn nước 2.626 m và 3.29 m; mặt sàn lệch nhau 0.664 m." — giả định: Illustrative: an idealised concrete box in still water under the scenario's assumptions; not a design result. Independent platforms: a rigid link would change both equilibria, so this does not show that a rigid link fails.

**B14** (fact; claim: CLM_042, CLM_056)

- `4:07` Connections are where engineers expect trouble.
- `4:11` A 2026 research agenda lists stress concentrations on connectors among the challenges of large floating developments.
- `4:20` One concept study links its modules flexibly, and spaces them far enough apart not to collide, because on flexible moorings they are expected to move sideways quite a lot.
  - CLM_042: SRC_NCOMMS_2026_TEN_QUESTIONS question 4: "Large floating developments encounter novel design challenges such as a complex hydro-elastic motion response, stress concentrations on connectors, and high global environmental loads." · SRC_NCOMMS_2026_TEN_QUESTIONS question 4: "Key enablers are innovations that reduce global and mooring loads (e.g., dissipative floating breakwaters)"
  - CLM_056: SRC_CEE_2026_RUZZO Results: "juxtaposed at a certain distance (~30 m) and flexibly connected between each other." · SRC_CEE_2026_RUZZO Discussion: "However, relatively large horizontal motion amplitudes are expected. Thus, the spacing between the architectural modules, and between the city and the floating barrier, must be sufficient to avoid contacts." · SRC_CEE_2026_RUZZO Discussion: "as back-up positioning systems in case of damaged moorings and/or occasional extreme displacements, to avoid contacts between modules and overloading in their connections." — giả định: c-r1 correction: the 'avoid contacts and overloading' clause belongs to the propellers (back-up positioning), not to the flexible links.

**B15** (fact; claim: CLM_124, CLM_108)

- `4:34` How many platforms would 10,000 people need?
- `4:38` Say each resident needs about 40 square meters of floor: thirty for their home, and ten for a share of schools, shops and services.
- `4:48` That's about thirty-three hectares of platform:
- `4:52` about 200 platforms like our first one, with hundreds of connections between them.
  - CLM_124: SRC_STUDIO_SCENARIO fields table: "phương án giữa 40 m² = 30 m² nhà ở + 10 m² trường học, phòng khám, cửa hàng, dịch vụ | DESIGN_ASSUMPTION |"
  - CLM_108: SRC_STUDIO_DESIGN_MODEL §4 table: "| 40 | 33.3 ha | 33.3 | 209 | 48 |" · SRC_STUDIO_DESIGN_MODEL §6b: "Phao 40 m: 3 tầng 48 người, 4 tầng 64 người" · SRC_STUDIO_DESIGN_MODEL §5 table: "| 100m | 34 | 60 | 29,564 | 300 |" · SRC_STUDIO_DESIGN_MODEL §9: "93 phao, 33.5 ha" — giả định: Illustrative: an idealised concrete box in still water under the scenario's assumptions; not a design result.

**B16** (fact; claim: CLM_108, CLM_014, CLM_125)

- `5:00` Bigger platforms mean fewer connections.
- `5:03` At 100 meters on a side, 34 would do,
- `5:08` but each would weigh about 30,000 tons, to build, launch and tow.
- `5:14` Even the Schoonschip floats were too big for the dry docks of traditional houseboat builders, and were cast on the quay instead.
- `5:22` Our district uses 60-meter platforms with three-story homes, 93 of them: a middle choice for this illustration, not an optimum.
  - CLM_108: SRC_STUDIO_DESIGN_MODEL §4 table: "| 40 | 33.3 ha | 33.3 | 209 | 48 |" · SRC_STUDIO_DESIGN_MODEL §6b: "Phao 40 m: 3 tầng 48 người, 4 tầng 64 người" · SRC_STUDIO_DESIGN_MODEL §5 table: "| 100m | 34 | 60 | 29,564 | 300 |" · SRC_STUDIO_DESIGN_MODEL §9: "93 phao, 33.5 ha" — giả định: Illustrative: an idealised concrete box in still water under the scenario's assumptions; not a design result.
  - CLM_014: SRC_STEDENBOUW_LAUNCH_2019 Van Selm quote: "We chose to build all the water homes on the quay and then launch them" · SRC_STEDENBOUW_FLOATS_2019 Gieskens quote: "In fact, due to their size and weight, the floats did not fit in the dry docks of traditional ark builders." · SRC_STEDENBOUW_LAUNCH_2019 launch paragraph: "On May 11, all the water homes sailed to their final destination"
  - CLM_125: SRC_STUDIO_SCENARIO fields table: "| Cỡ phao của quận | 60 × 60 m (93 phao cho khoảng 33 ha), nhà 3 tầng | DESIGN_ASSUMPTION | Lựa chọn ở giữa cho bản minh họa (ít mối nối hơn phao 40 m, nhẹ hơn phao 100 m), không phải tối ưu đã tính |"


### C4 · The Water Never Stays Still

**B17** (framing; claim: không, câu dẫn dắt)

- `5:33` And all of this sits on water that never keeps still.
- `5:38` Each platform rises and falls on its own, and every gap and hinge between them has to cope.

**B18** (fact; claim: CLM_022)

- `5:46` People living on the water feel it.
- `5:49` Floating homes in the Netherlands can rock in storms, or when large cruise ships pass,
- `5:55` and one Amsterdam resident feels it most on her upper floor.
  - CLM_022: SRC_YALE_E360_2021 paragraph on motion: "Severe wind and rainstorms, or even the passing of large cruise ships, can make the buildings rock." · SRC_YALE_E360_2021 resident quote: "Siti Boelen, the Schoonschip resident, said that when she first moved in, stormy weather made her think twice before venturing up to her third-floor kitchen, where she felt the movement the most." — giả định: c-r2 claim review (owner): one resident's experience, not a general finding about upper floors.

**B19** (fact; claim: CLM_053)

- `6:01` Very large platforms don't only move. They bend,
- `6:06` and predicting exactly how is still an open research problem.
  - CLM_053: SRC_CEE_2026_RUZZO Discussion: "The representation of the hydro-elastic dynamic behavior of such Very Large Floating Structures (VLFSs) is a complex and partially open challenge." · SRC_CEE_2026_RUZZO Methods, recommended analyses: "they neglect or simplify the nonlinear forces, and thus cannot represent accurately some key aspects, including connection behavior under large displacements"

**B20** (fact; claim: CLM_050, CLM_121)

- `6:12` So the first fix is where you build.
- `6:15` A 2026 concept study looks for sea areas with limited fetch, near a gulf, a strait or an archipelago, where waves stay moderate.
- `6:26` That's why our city sits in a sheltered bay, connected to an existing city on shore.
  - CLM_050: SRC_CEE_2026_RUZZO Results, first paragraph: "The ideal installation site would be a limited-fetch sea area in the exclusive economic zones (EEZ) of a coastal/island state, e.g., in proximity of a gulf, a strait, or an archipelago, to draw on moderate wave action and water depth, and facilitate the connection with the mainland."
  - CLM_121: SRC_STUDIO_SCENARIO fields table: "| Dân số | 10.000 cư dân (mục tiêu kịch bản) | DESIGN_ASSUMPTION |" · SRC_STUDIO_SCENARIO fields table: "| Kiểu kịch bản | Phần mở rộng nổi nối bờ, xây theo pha | DESIGN_ASSUMPTION |"

**B21** (fact; claim: CLM_055, CLM_051, CLM_052)

- `6:33` The second fix is the layout.
- `6:36` Following one concept study, homes go in the middle, and functions that can tolerate more motion form the outer ring.
- `6:45` Where the bay opens to the sea, a breakwater reduces the waves.
- `6:51` But a floating breakwater may not be enough against longer waves from the open sea, and how much wave energy passes behind one is still hard to predict.
  - CLM_055: SRC_CEE_2026_RUZZO Discussion: "The mooring system of the internal modules is conceived as redundant and compliant, made up of shared catenary and/or taut lines." · SRC_CEE_2026_RUZZO Discussion: "the residential modules are placed internally, being further protected by the special ones, where larger motions and accelerations are tolerated."
  - CLM_051: SRC_CEE_2026_RUZZO Discussion, resilience: "floating breakwaters may not be sufficient to adequately mitigate the longer waves typically occurring in exposed sea areas, due to local storms or long-transmitting swells." — giả định: From the study's simplified preliminary assessment; the film says 'may not be enough', never 'cannot'.
  - CLM_052: SRC_CEE_2026_RUZZO Discussion, resilience: "Being the characterization of the wave transmission behind a floating breakwater a complex and partly unresolved task"


### C5 · Keeping the City in Place

**B22** (fact; claim: CLM_020)

- `7:03` Something also has to hold the city in place.
- `7:07` Floating homes in the Netherlands are fixed to the shore, often resting against steel poles.
  - CLM_020: SRC_YALE_E360_2021 paragraph on houseboats: "Unlike houseboats, which can easily be unmoored and relocated, floating homes are fixed to the shore, often resting on steel poles, and are usually connected to the local sewer system and power grid."

**B23** (fact; claim: CLM_041, CLM_122, CLM_109)

- `7:14` Water levels rise and fall, and a floating platform rises and falls with them, sliding along its poles.
- `7:22` In our scenario, the water level can change by about 2 meters,
- `7:28` so the bridges to shore need hinges: including changes in loading, the slope of a 25-meter bridge changes by about 3 degrees either way.
  - CLM_041: SRC_NCOMMS_2026_TEN_QUESTIONS introduction: "floating structures can adapt to fluctuating water levels, they can be easily decommissioned, relocated, or repurposed"
  - CLM_122: SRC_STUDIO_SCENARIO fields table: "| Dải mực nước (triều + nước dâng) | 2,0 m (minh họa) | DESIGN_ASSUMPTION |"
  - CLM_109: SRC_STUDIO_DESIGN_MODEL §6: "Dải mực nước 2.0 m (giả định) cộng dao động mớn nước khi phao rỗng và đầy (0.439 m); khớp trên bờ đặt ở giữa dải tổng:" · SRC_STUDIO_DESIGN_MODEL §6: "Cầu 25 m: dốc tối đa khoảng 2.8° mỗi chiều." · SRC_STUDIO_DESIGN_MODEL §6: "Cầu 25 m, chỉ mực nước: dốc tối đa khoảng 2.3° mỗi chiều." — giả định: Illustrative: an idealised concrete box in still water under the scenario's assumptions; not a design result. c-r2 (owner review): the narration names the loading and the screen shows the hinge-height assumption.

**B24** (fact; claim: CLM_055, CLM_054)

- `7:39` Further out, the water is deeper, and piles give way to mooring lines anchored in the seabed.
- `7:46` Deeper water means longer lines, deeper anchors, and higher costs.
- `7:52` The seabed itself shapes the design, and the bill.
  - CLM_055: SRC_CEE_2026_RUZZO Discussion: "The mooring system of the internal modules is conceived as redundant and compliant, made up of shared catenary and/or taut lines." · SRC_CEE_2026_RUZZO Discussion: "the residential modules are placed internally, being further protected by the special ones, where larger motions and accelerations are tolerated."
  - CLM_054: SRC_CEE_2026_RUZZO Methods, cost: "The mooring system cost depends mainly on the bathymetry of the installation site and on the seabed properties." · SRC_CEE_2026_RUZZO Methods, cost: "larger water depths imply longer mooring lines and deeper anchors, with subsequent nonlinear cost increases for material and installation."


### C6 · A City Needs More Than Buildings

**B25** (framing; claim: không, câu dẫn dắt)

- `7:57` So it floats, and it stays put. But is it a city yet?
- `8:01` Fade out the buildings, and the city's other half appears.

**B26** (fact; claim: CLM_016)

- `8:07` Power first: at Schoonschip, 46 households share a single connection to the national grid,
- `8:14` with solar panels, a battery in every house, and a smart grid between them.
- `8:20` Floating doesn't mean off-grid.
  - CLM_016: SRC_SCHOONSCHIP_ORG energy: "We generate our own electricity with photovoltaic solar panels." · SRC_SCHOONSCHIP_ORG energy: "Each house has a big battery that stores temporary surpluses." · SRC_SCHOONSCHIP_ORG energy: "All the houses are connected to our smartgrid." · SRC_SCHOONSCHIP_ORG energy: "With 46 households we have only one connection to the national energy grid."

**B27** (fact; claim: CLM_017, CLM_023, CLM_123)

- `8:24` Wastewater is separated there too: gray water from showers and washing machines, black water from toilets.
- `8:32` Connecting floating homes to sewers on land takes extra infrastructure, such as waterproof cables and pumps.
- `8:41` In our city, wastewater is pumped ashore along the bridges, and drinking water comes back the same way.
  - CLM_017: SRC_SCHOONSCHIP_ORG water: "We have separate streams for the disposal of grey water (from the shower, washing machine and so on) and black water (from the toilets)." · SRC_SCHOONSCHIP_ORG water: "In a pilot in cooperation with Waternet in the nearby future the black water will be transposed to a floating processor (a digester)" — giả định: The digester is a plan on the residents' site; the film must not present it as operating.
  - CLM_023: SRC_YALE_E360_2021 paragraph on infrastructure: "Floating homes also require extra infrastructure and work to connect to the electricity grid and sewer system, with special waterproof cords and pumps needed to link to municipal services on higher ground."
  - CLM_123: SRC_STUDIO_SCENARIO fields table: "| Nước thải | Tách nước xám và nước đen, bơm về nhà máy trên bờ | DESIGN_ASSUMPTION |" · SRC_STUDIO_SCENARIO fields table: "| Nước sạch | Từ mạng nước thành phố qua cầu; nước mưa cho mục đích không uống. Không khử mặn | DESIGN_ASSUMPTION |"

**B28** (fact; claim: CLM_043)

- `8:49` Transport, fire and medical services, and food all follow the same logic.
- `8:56` A large floating development has to connect sewage, power and roads to land, or develop alternatives of its own,
- `9:04` and our city connects.
  - CLM_043: SRC_NCOMMS_2026_TEN_QUESTIONS question 4: "Civil engineers and urban designers will also face challenges in connecting civil infrastructure, such as sewage, power cables, and roads, to land or developing off-grid alternatives."


### C7 · What Would Actually Make This Difficult?

**B29** (framing; claim: không, câu dẫn dắt)

- `9:08` Everything so far assumed sheltered water close to a city.
- `9:13` So what happens if we tow it out to sea?

**B30** (fact; claim: CLM_051, CLM_054)

- `9:17` Longer waves arrive, and a floating breakwater may not be enough against them.
- `9:23` Below the surface, the seabed drops away, so mooring lines get longer and anchors deeper.
  - CLM_051: SRC_CEE_2026_RUZZO Discussion, resilience: "floating breakwaters may not be sufficient to adequately mitigate the longer waves typically occurring in exposed sea areas, due to local storms or long-transmitting swells." — giả định: From the study's simplified preliminary assessment; the film says 'may not be enough', never 'cannot'.
  - CLM_054: SRC_CEE_2026_RUZZO Methods, cost: "The mooring system cost depends mainly on the bathymetry of the installation site and on the seabed properties." · SRC_CEE_2026_RUZZO Methods, cost: "larger water depths imply longer mooring lines and deeper anchors, with subsequent nonlinear cost increases for material and installation."

**B31** (fact; claim: CLM_043, CLM_051)

- `9:31` Further from shore, cables, pipes and supply ships can still reach the city,
- `9:37` but every link becomes longer and more exposed.
  - CLM_043: SRC_NCOMMS_2026_TEN_QUESTIONS question 4: "Civil engineers and urban designers will also face challenges in connecting civil infrastructure, such as sewage, power cables, and roads, to land or developing off-grid alternatives."
  - CLM_051: SRC_CEE_2026_RUZZO Discussion, resilience: "floating breakwaters may not be sufficient to adequately mitigate the longer waves typically occurring in exposed sea areas, due to local storms or long-transmitting swells." — giả định: From the study's simplified preliminary assessment; the film says 'may not be enough', never 'cannot'.

**B32** (fact; claim: CLM_058)

- `9:42` And if we also asked the city to supply itself, as one 2026 offshore concept does,
- `9:50` it would need its own systems for energy, water and food.
- `9:54` In that study, growing food alone accounts for nearly half of the city's estimated energy use.
  - CLM_058: SRC_CEE_2026_RUZZO Results: "The estimated total floating city final energy consumption under conservative hypotheses is ~470.3 GWh/yr." · SRC_CEE_2026_RUZZO Results: "Food production is the most energy-intensive activity (~47.5%)" — giả định: Depends on the study's autonomy goal (local food and water); not a requirement of the Studio scenario.

**B33** (fact; claim: CLM_062)

- `10:02` That study also uses a different kind of hull:
- `10:07` semi-submersible platforms, with the deck raised above the sea on columns, behind a floating barrier.
- `10:15` Offshore isn't the same city moved further out. It's a different design.
  - CLM_062: SRC_CEE_2026_RUZZO Results: "The inner city modules are compliantly-moored, semi-submersible floaters, with the deck raised above the sea level by interconnected slenderer floating elements (columns)." · SRC_CEE_2026_RUZZO Results: "The floating city is made up of two main modular components: the external protection barrier, and the inner urban conglomerate."

**B34** (fact; claim: CLM_059)

- `10:21` Some difficulties remain wherever we build.
- `10:25` Concrete in seawater needs watching: chlorides can corrode the steel reinforcement,
- `10:32` and, according to a 2026 study, there are no dedicated standards for floating cities yet.
  - CLM_059: SRC_CEE_2026_RUZZO Methods, cost: "the steel bars are subject to chloride-induced corrosion, which may compromise the structural safety and require expensive repairs during the life cycle of the structure" · SRC_CEE_2026_RUZZO Methods, cost: "the current absence of dedicated standards and recommendations in the regulatory framework"

**B35** (fact; claim: CLM_044)

- `10:40` Large floating developments change the light, shade and water movement beneath them, effects that researchers say still need study,
- `10:49` and they expect the impact on local ecology to be far larger than that of small developments.
  - CLM_044: SRC_NCOMMS_2026_TEN_QUESTIONS question 5: "Any large-scale floating development will impact local ecology far more than current small-scale developments." · SRC_NCOMMS_2026_TEN_QUESTIONS question 5: "changes to light, shade, and hydrodynamics require further study, as do colonization by non-native species, corrosion, management of waste, and prevention of biofouling."

**B36** (fact; claim: CLM_045, CLM_046)

- `10:57` And who gets to use the water?
- `11:00` How districts like this fit into planning law is not yet known,
- `11:05` and researchers warn they could end up serving the wealthy, and fencing off water that used to be public.
  - CLM_045: SRC_NCOMMS_2026_TEN_QUESTIONS question 6: "Governance of large-scale floating developments is highly complex." · SRC_NCOMMS_2026_TEN_QUESTIONS question 6: "it is not yet known how and to what extent large floating developments can be integrated into existing spatial policy, legislation, and regulations"
  - CLM_046: SRC_NCOMMS_2026_TEN_QUESTIONS question 9: "inequalities by catering to the needs of the wealthy, relying on exploitative supply chains, displacing or leaving behind marginalized groups, or causing enclosure of water which has previously been common public space."

**B37** (fact; claim: CLM_063, CLM_041, CLM_054, CLM_042, CLM_059)

- `11:13` And what would it cost?
- `11:16` We do not yet have a reliable cost estimate for this design. The one published framework we found is preliminary, and covers only flotation and energy.
- `11:27` Compared with land, floating structures can follow the water level, and can be moved or reused,
- `11:34` but they trade a fixed foundation for moorings, connections and ongoing maintenance.
  - CLM_063: SRC_CEE_2026_RUZZO Methods, cost: "To the authors’ knowledge the only available source in this regard is a report from the “Floating city project”72, which provides limited justification for each cost estimation and is not peer-reviewed." · SRC_CEE_2026_RUZZO Methods, cost: "In the following, we propose a simplified framework for the preliminary cost assessment of the floating city, limited to floatation and energy systems." — giả định: Owner review 2026-11-08: a framework exists (this study), so the film must not say 'no cost basis'. It says the Studio has no reliable cost estimate for its own design.
  - CLM_041: SRC_NCOMMS_2026_TEN_QUESTIONS introduction: "floating structures can adapt to fluctuating water levels, they can be easily decommissioned, relocated, or repurposed"
  - CLM_054: SRC_CEE_2026_RUZZO Methods, cost: "The mooring system cost depends mainly on the bathymetry of the installation site and on the seabed properties." · SRC_CEE_2026_RUZZO Methods, cost: "larger water depths imply longer mooring lines and deeper anchors, with subsequent nonlinear cost increases for material and installation."
  - CLM_042: SRC_NCOMMS_2026_TEN_QUESTIONS question 4: "Large floating developments encounter novel design challenges such as a complex hydro-elastic motion response, stress concentrations on connectors, and high global environmental loads." · SRC_NCOMMS_2026_TEN_QUESTIONS question 4: "Key enablers are innovations that reduce global and mooring loads (e.g., dissipative floating breakwaters)"
  - CLM_059: SRC_CEE_2026_RUZZO Methods, cost: "the steel bars are subject to chloride-induced corrosion, which may compromise the structural safety and require expensive repairs during the life cycle of the structure" · SRC_CEE_2026_RUZZO Methods, cost: "the current absence of dedicated standards and recommendations in the regulatory framework"


### C8 · Could We Really Build It?

**B38** (framing; claim: không, câu dẫn dắt)

- `11:41` From one platform to a district, every part we added answers a question we had to ask.

**B39** (fact; claim: CLM_010, CLM_011, CLM_016)

- `11:49` So, could we build an entire city that floats?
- `11:53` Small floating neighborhoods, connected to the shore in sheltered water, already exist.
  - CLM_010: SRC_SM_SCHOONSCHIP project text: "Officially finished in 2021, the neighborhood comprises 30 water plots with 46 unique homes" · SRC_SCHOONSCHIP_ORG home page: "we live with 46 households, on 30 arks." · SRC_SCHOONSCHIP_ORG timeline: "In the year 2020 all floating houses at Schoonschip were finalised." — giả định: The two sources give 2020 (houses finalised) and 2021 (officially finished); the film says 'finished in 2020–2021' or names both.
  - CLM_011: SRC_SCHOONSCHIP_ORG about: "Schoonschip offers a place of residence for 46 households and a bit more than 100 residents, in all ages."
  - CLM_016: SRC_SCHOONSCHIP_ORG energy: "We generate our own electricity with photovoltaic solar panels." · SRC_SCHOONSCHIP_ORG energy: "Each house has a big battery that stores temporary surpluses." · SRC_SCHOONSCHIP_ORG energy: "All the houses are connected to our smartgrid." · SRC_SCHOONSCHIP_ORG energy: "With 46 households we have only one connection to the national energy grid."

**B40** (interpretation; claim: CLM_121, CLM_053, CLM_042, CLM_063, CLM_034)

- `12:00` A connected district for 10,000 people, in a sheltered bay, built step by step, may be possible under the right conditions.
- `12:10` But how very large platforms bend, how their connections hold up, and what they would cost are still open questions.
- `12:18` And the one project of that size we checked is still listed as in design.
  - CLM_121: SRC_STUDIO_SCENARIO fields table: "| Dân số | 10.000 cư dân (mục tiêu kịch bản) | DESIGN_ASSUMPTION |" · SRC_STUDIO_SCENARIO fields table: "| Kiểu kịch bản | Phần mở rộng nổi nối bờ, xây theo pha | DESIGN_ASSUMPTION |"
  - CLM_053: SRC_CEE_2026_RUZZO Discussion: "The representation of the hydro-elastic dynamic behavior of such Very Large Floating Structures (VLFSs) is a complex and partially open challenge." · SRC_CEE_2026_RUZZO Methods, recommended analyses: "they neglect or simplify the nonlinear forces, and thus cannot represent accurately some key aspects, including connection behavior under large displacements"
  - CLM_042: SRC_NCOMMS_2026_TEN_QUESTIONS question 4: "Large floating developments encounter novel design challenges such as a complex hydro-elastic motion response, stress concentrations on connectors, and high global environmental loads." · SRC_NCOMMS_2026_TEN_QUESTIONS question 4: "Key enablers are innovations that reduce global and mooring loads (e.g., dissipative floating breakwaters)"
  - CLM_063: SRC_CEE_2026_RUZZO Methods, cost: "To the authors’ knowledge the only available source in this regard is a report from the “Floating city project”72, which provides limited justification for each cost estimation and is not peer-reviewed." · SRC_CEE_2026_RUZZO Methods, cost: "In the following, we propose a simplified framework for the preliminary cost assessment of the floating city, limited to floatation and energy systems." — giả định: Owner review 2026-11-08: a framework exists (this study), so the film must not say 'no cost basis'. It says the Studio has no reliable cost estimate for its own design.
  - CLM_034: SRC_BIG_OCEANIX_BUSAN project facts (page text): "Status In Design" — giả định: A status label on the architects' website on the date checked; BIG's other labels include 'In Construction' and 'Completed'. It says nothing about other projects worldwide.

**B41** (interpretation; claim: CLM_051, CLM_058, CLM_062)

- `12:25` A city far out at sea, especially one that has to supply itself, remains much more speculative.
  - CLM_051: SRC_CEE_2026_RUZZO Discussion, resilience: "floating breakwaters may not be sufficient to adequately mitigate the longer waves typically occurring in exposed sea areas, due to local storms or long-transmitting swells." — giả định: From the study's simplified preliminary assessment; the film says 'may not be enough', never 'cannot'.
  - CLM_058: SRC_CEE_2026_RUZZO Results: "The estimated total floating city final energy consumption under conservative hypotheses is ~470.3 GWh/yr." · SRC_CEE_2026_RUZZO Results: "Food production is the most energy-intensive activity (~47.5%)" — giả định: Depends on the study's autonomy goal (local food and water); not a requirement of the Studio scenario.
  - CLM_062: SRC_CEE_2026_RUZZO Results: "The inner city modules are compliantly-moored, semi-submersible floaters, with the deck raised above the sea level by interconnected slenderer floating elements (columns)." · SRC_CEE_2026_RUZZO Results: "The floating city is made up of two main modular components: the external protection barrier, and the inner urban conglomerate."

**B42** (interpretation; claim: CLM_104, CLM_121)

- `12:33` Our arithmetic shows what it takes for a platform to float.
- `12:38` Whether a whole district works depends on the site, and on every other system we added.
  - CLM_104: SRC_STUDIO_DESIGN_MODEL §2 table, mid case: "| 0.6 (giữa) | 4851.2 | 3.032 | 2.958 | 1.042 |" · SRC_STUDIO_DESIGN_MODEL §2: "Bê tông thân phao chiếm 55% khối lượng (phương án giữa)" — giả định: Illustrative: an idealised concrete box in still water under the scenario's assumptions; not a design result.
  - CLM_121: SRC_STUDIO_SCENARIO fields table: "| Dân số | 10.000 cư dân (mục tiêu kịch bản) | DESIGN_ASSUMPTION |" · SRC_STUDIO_SCENARIO fields table: "| Kiểu kịch bản | Phần mở rộng nổi nối bờ, xây theo pha | DESIGN_ASSUMPTION |"

**B43** (framing; claim: không, câu dẫn dắt)

- `12:45` Which structure should we explain next?
- `12:48` Suggest a topic in the comments.
- `12:52` And if you enjoyed this film, please like it and subscribe.

**B44** (framing; claim: không, câu dẫn dắt)

- `12:57` Thank you for watching.
- `13:00` The sources are listed in the description.

## Bộ kiểm nhất quán lời/hình: cần người duyệt xác nhận

- B31.s1 (TRANSFORMATION, UNCERTAIN): "but every link becomes longer and more exposed." — transformation wording without a shown transformation (may be figurative); editorial check
- B40.s0 (SIDE, UNCERTAIN): "A connected district for 10,000 people, in a sheltered bay, built step by step, may be possible under the right conditions." — left/right wording; no annotation to locate - confirm the referent in review

## Chữ trên card

- **SC_003** (B03): Already built, and proposed | Amsterdam: Schoonschip | built · 46 households · a little over 100 people | one square = one household (schematic) | Busan, South Korea: OCEANIX Busan | proposed 2022 · design for 12,000 people | Architects' project page, Nov 2026: In Design
- **SC_007** (B07): Schoonschip, Amsterdam (schematic) | concrete float | 340–350 t | ≈ 340–350 m³ of water | a cube about 7 m on each side | 1.8 m figures
- **SC_015** (B15): How many platforms? (illustrative) | 10,000 people | 40 m² of floor each | 30 home + 10 schools, shops, services | ≈ 33 ha of platform | ≈ 209 platforms of 40 m | up to 391 joints
- **SC_016** (B16): How many platforms? (illustrative) | 10,000 people | Bigger platforms: fewer joints | 34 platforms of 100 m · 60 joints | ≈ 30,000 t each | to build, launch and tow | Schoonschip's floats: cast on the quay, | too big for houseboat dry docks | Our district: 93 platforms of 60 m | 3 stories · 180 joints at most | a middle choice for this illustration, | not an optimum
- **SC_018** (B18): Living on the water | upper floor | large cruise ship passing | felt most on the upper floor | Source: Yale Environment 360, 2021
- **SC_019** (B19): Very large platforms bend | bending exaggerated, conceptual | How exactly? An open research problem
- **SC_020** (B20): Where to build | Open coast | Sheltered bay | long fetch: big waves | land | limited fetch: moderate waves | our city: sheltered, connected to the shore
- **SC_023** (B23): Water level and the hinged bridge (illustrative) | quay | hinge | pile | water level range ≈ 2 m (assumed) | plus loading: draft changes ≈ 0.44 m | 25 m bridge: slope changes ≈ 2.8° either way | shore hinge at the middle of the range
- **SC_026** (B26): Schoonschip, Amsterdam (schematic) | land | 46 households | one grid connection | solar panels | a battery in every house | smart grid | Floating ≠ off-grid
- **SC_032** (B32): An added condition: supply itself | energy | water | food | food production: ≈ 48% of the estimated energy use | one 2026 offshore concept study's estimate | Autonomy is an extra choice, not a consequence of floating
- **SC_036** (B36): Who gets to use the water? | Public waterfront | Private, fenced edge | Planning law: not yet known
- **SC_037** (B37): What would it cost? | No reliable cost estimate for this design yet | the one published framework: preliminary; flotation and energy only | Floating gives | follows the water level | can be moved or reused | Floating costs | moorings | connections | ongoing maintenance
- **SC_039** (B39): Could we build an entire city that floats? | Small floating neighbourhoods, sheltered and connected | already exist
- **SC_040** (B40): Could we build an entire city that floats? | Small floating neighbourhoods, sheltered and connected | already exist | A connected district for 10,000 in a sheltered bay | possible, under the right conditions | · how very large platforms bend | · how connections hold up | · what they would cost | Open questions | The one project of that size we checked: still listed as in design
- **SC_041** (B41): Could we build an entire city that floats? | Small floating neighbourhoods, sheltered and connected | already exist | A connected district for 10,000 in a sheltered bay | possible, under the right conditions | A city far out at sea that supplies itself | much more speculative
- **SC_043** (B43): What should we explain next? | Suggest a topic in the comments | SUBSCRIBE | SUBSCRIBED
- **SC_044** (B44): Could We Build an Entire City That Floats? | Sources are listed in the description. | Models and numbers are illustrative, not engineering designs. | Schoonschip and OCEANIX Busan are shown as schematic drawings. | Narration: AI voice (Kokoro, am_michael) | Architecture Story Studio

## Chú thích trên cảnh 3D

- B01 `B01_note` NOTE: "Illustrative design"
- B05 `B05_ch` NOTE: "2 · The First Problem: Making Buildings Float"
- B05 `B05_block` COMPONENT_LABEL: "1,108 m³ of concrete"
- B05 `B05_box` COMPONENT_LABEL: "Same concrete, hollow"
- B05 `B05_note` NOTE: "Hull only, 40 m box: draft ≈ 1.62 m"
- B06 `B06_water` COMPONENT_LABEL: "Water pushed aside"
- B06 `B06_rule` NOTE: "1 t added ≈ 1 m³ more water pushed aside"
- B06 `B06_note` NOTE: "Illustrative design, section through the middle"
- B08 `B08_cut` NOTE: "Cut through the middle"
- B08 `B08_draft` COMPONENT_LABEL: "Draft ≈ 2.96 m"
- B08 `B08_hull` COMPONENT_LABEL: "Hull: ≈ 55% of the weight"
- B08 `B08_note` NOTE: "Illustrative design, section through the middle"
- B09 `B09_fb0` COMPONENT_LABEL: "Freeboard ≈ 1.04 m"
- B09 `B09_before` COMPONENT_LABEL: "Deck before"
- B09 `B09_fb1` COMPONENT_LABEL: "Freeboard: 1.04 → 0.71 m"
- B09 `B09_note` NOTE: "+1 story, same load per m² of floor"
- B10 `B10_fb0` COMPONENT_LABEL: "Freeboard ≈ 0.71 m"
- B10 `B10_ext` COMPONENT_LABEL: "+0.5 m hull: ≈ 106 t (+4%)"
- B10 `B10_fb1` COMPONENT_LABEL: "Freeboard: 0.71 → 1.15 m"
- B10 `B10_note` NOTE: "Or: lighter buildings"
- B11 `B11_load` COMPONENT_LABEL: "100 t"
- B11 `B11_path` COMPONENT_LABEL: "15 m"
- B11 `B11_tilt` NOTE: "100 t moved 15 m: tilt ≈ 0.4° (true scale)"
- B11 `B11_note` NOTE: "Illustrative design"
- B12 `B12_ch` NOTE: "3 · Why One Platform Isn't a City"
- B12 `B12_people` NOTE: "3 stories: about 48 residents per platform"
- B13 `B13_step` COMPONENT_LABEL: "Decks ≈ 0.66 m apart"
- B13 `B13_free` NOTE: "Each floating on its own (illustrative)"
- B13 `B13_ballast` NOTE: "Another option: ballast to even out the decks"
- B14 `B14_walk` COMPONENT_LABEL: "Hinged walkway"
- B14 `B14_util` COMPONENT_LABEL: "Flexible utility link"
- B14 `B14_fender` COMPONENT_LABEL: "Fender"
- B14 `B14_note` NOTE: "Conceptual geometry, not sized"
- B17 `B17_ch` NOTE: "4 · The Water Never Stays Still"
- B17 `B17_label` NOTE: "Conceptual motion visualization — not a hydrodynamic simulation"
- B21 `B21_note` NOTE: "Reduces waves; does not remove storm risk"
- B21 `B21_homes` COMPONENT_LABEL: "Homes"
- B21 `B21_ring` COMPONENT_LABEL: "Services"
- B22 `B22_ch` NOTE: "5 · Keeping the City in Place"
- B22 `B22_pile` COMPONENT_LABEL: "Steel pile"
- B22 `B22_note` NOTE: "Water drawn see-through"
- B24 `B24_note` NOTE: "Conceptual mooring — not sized"
- B24 `B24_anchor` COMPONENT_LABEL: "Anchor"
- B25 `B25_ch` NOTE: "6 · A City Needs More Than Buildings"
- B27 `B27_note` NOTE: "Our illustrative design"
- B27 `B27_waste` COMPONENT_LABEL: "Wastewater to shore"
- B27 `B27_water` COMPONENT_LABEL: "Drinking water from shore"
- B28 `B28_route` NOTE: "Emergency route to land"
- B29 `B29_ch` NOTE: "7 · What Would Actually Make This Difficult?"
- B29 `B29_note` NOTE: "Counterfactual: the same district at open sea"
- B30 `B30_label` NOTE: "Conceptual motion visualization — not a hydrodynamic simulation"
- B30 `B30_anchor` COMPONENT_LABEL: "Anchor"
- B31 `B31_note` NOTE: "Links to a shore beyond the frame, not sized"
- B33 `B33_box` COMPONENT_LABEL: "Our box pontoon"
- B33 `B33_semi` COMPONENT_LABEL: "Semi-submersible module"
- B33 `B33_note` NOTE: "Schematic of a 2026 concept study's module"
- B34 `B34_note` NOTE: "Illustrative: inspection zone, no damage shown"
- B35 `B35_note` NOTE: "Shade illustrative; effects still need study"
- B38 `B38_ch` NOTE: "8 · Could We Really Build It?"
- B42 `B42_note` NOTE: "Illustrative design"

## Bản ghi sửa câu (ASR / tốc độ đọc)

- B01.s0 (c-r1): "Ten thousand people. / Homes, schools, a clinic, parks, and streets to walk along." → "Ten thousand people, with homes, schools, a clinic, parks, and streets to walk along." (Kokoro output of a 2-3-word sentence fell below the 1.5 words/s speech check (1.43 words/s, deterministic seed); merged with its neighbour instead of loosening the check)
- B26.s0 (c-r1): "Power first. / At Schoonschip, forty-six households share a single connection to the national grid," → "Power first: at Schoonschip, forty-six households share a single connection to the national grid," (same check, pre-emptively (2-word sentence))
- B28.s1 (c-r1): "... or develop alternatives of its own. / Ours connects." → "... or develop alternatives of its own, / and ours connects." (same check, pre-emptively (2-word sentence))
- all (c-r1: American spelling (meter, ton, story, neighborhood, gray) and digits for numbers of 100 and more, as in the Studio's other films; 'and ours connects' -> 'and our city connects'): ASR check: Whisper writes American spelling and digits, so British spelling and spelled-out large numbers failed the word-error check although the speech was right; 'ours' was heard as 'hours'. Meaning unchanged.
- B03.s3-s4 (c-r1: One, for 12,000 people off the coast of Busan in South Korea, was unveiled in 2022. / When we checked the developer's and the architects' websites in November 2026, neither reported that construction had begun.): owner: the research process made the opening read like a report; the architects' page lists the status 'In Design' (CLM_034)
- B12.s0 (c-r1: A platform like this holds about fifty people.): owner: B09-B10 end at four stories; the count (48) and the district are three-story
- B16.s4 (c-r1: Our district uses 60-meter platforms, 93 of them: ...): same
- B23.s2 (c-r1: ... on a 25-meter bridge, the slope changes by about 3 degrees either way.): owner: 2.8 degrees includes the 0.44 m loading change and a mid-range hinge; water level alone gives 2.3 (CLM_109)
- B40.s2-s3 (c-r1: And the one project of that size we checked had not been reported as under construction when we looked. / We didn't survey every project in the world.): owner: shorter; the scope of the check stays in the notes and in CLM_034
