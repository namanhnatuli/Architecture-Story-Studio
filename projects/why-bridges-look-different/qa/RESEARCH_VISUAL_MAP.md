# Ánh xạ nghiên cứu → hình ảnh: why-bridges-look-different

Sinh bởi `tools/cli.py research-map` từ visual_plan.json, sources.json, timing.json và blender_checks.json. Mỗi dòng: câu → claim → nguồn (vị trí) → asset/bộ phận → chú thích → thời điểm → QA.
Claim nào cũng mới ở mức `SOURCE_VERIFIED`, **chưa được duyệt biên tập**.

## B01.s0 (0.40 s): "One bridge rests on rows of timber posts."
- Không có claim (câu dẫn dắt).
- Shot: SC_001, SC_002, SC_003, SC_004

## B01.s1 (4.30 s): "Another leaps the gap in curves of stone."
- Không có claim (câu dẫn dắt).
- Shot: SC_001, SC_002, SC_003, SC_004

## B01.s2 (7.90 s): "A third is a lattice of steel triangles."
- Không có claim (câu dẫn dắt).
- Shot: SC_001, SC_002, SC_003, SC_004

## B01.s3 (11.72 s): "All three cross exactly the same gap."
- Không có claim (câu dẫn dắt).
- Shot: SC_001, SC_002, SC_003, SC_004

## B01B.s0 (16.15 s): "Over wider water, the answers change again."
- Không có claim (câu dẫn dắt).
- Shot: SC_005

## B01B.s1 (20.30 s): "One bridge reaches out from its piers."
- Không có claim (câu dẫn dắt).
- Shot: SC_005

## B01C.s0 (24.61 s): "Another hangs from huge draped cables."
- Không có claim (câu dẫn dắt).
- Shot: SC_006

## B01D.s0 (29.15 s): "A third is held up by straight lines of steel."
- Không có claim (câu dẫn dắt).
- Shot: SC_007

## B02.s0 (33.77 s): "So why don't bridges all look the same?"
- Không có claim (câu dẫn dắt).
- Shot: SC_008

## B02.s1 (37.15 s): "It isn't because one design is simply better than the others."
- Không có claim (câu dẫn dắt).
- Shot: SC_008

## B02.s2 (41.95 s): "Each form is a different answer to the same problem, shaped by materials, by the site, by the span, and by the time it was built in."
- Không có claim (câu dẫn dắt).
- Shot: SC_008

## B03.s0 (52.73 s): "Every bridge has the same basic job."
- Claim `CLM_701` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.365 'live load'); SRC_ODOT_MBI (Glossary p.350 'dead load')
- Claim `CLM_702` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.350 'deck')
- Shot: SC_009
- Chú thích `B03_ch` NOTE "2 · The problem every bridge must solve" → SC_009 / bridge_steel_truss_pratt_01 / ; 52.62–62.46 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B03.s1 (56.38 s): "It has to carry loads: the traffic crossing it, and the weight of the bridge itself."
- Claim `CLM_701` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.365 'live load'); SRC_ODOT_MBI (Glossary p.350 'dead load')
- Claim `CLM_702` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.350 'deck')
- Shot: SC_009
- Chú thích `B03_load` LOAD_ARROW "Load" → SC_009 / bridge_steel_truss_pratt_01 / steel_truss_bridge_span1_deck, steel_truss_bridge_span2_deck; 56.29–67.62 s; claim CLM_701; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B03.s2 (62.56 s): "And it has to pass all of that down into the ground on either side."
- Claim `CLM_701` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.365 'live load'); SRC_ODOT_MBI (Glossary p.350 'dead load')
- Claim `CLM_702` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.350 'deck')
- Shot: SC_009
- Chú thích `B03_ground` COMPONENT_LABEL "Ground" → SC_009 / site_river_crossing_24 / bank_right; 62.46–67.62 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B04.s0 (68.36 s): "Engineers often describe a bridge in two parts."
- Claim `CLM_702` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.350 'deck')
- Claim `CLM_703` [SOURCE_VERIFIED]: SRC_FHWA_PBES_CH2 (Chapter 2 introduction (AASHTO definition)); SRC_FHWA_PBES_GLOSSARY (Appendix E 'superstructure')
- Claim `CLM_704` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.383 'substructure'); SRC_ODOT_MBI (Glossary p.338 'abutment'); SRC_ODOT_MBI (Glossary p.370 'pier')
- Shot: SC_010

## B04.s1 (72.61 s): "The superstructure is the part that spans the gap, including the deck."
- Claim `CLM_702` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.350 'deck')
- Claim `CLM_703` [SOURCE_VERIFIED]: SRC_FHWA_PBES_CH2 (Chapter 2 introduction (AASHTO definition)); SRC_FHWA_PBES_GLOSSARY (Appendix E 'superstructure')
- Claim `CLM_704` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.383 'substructure'); SRC_ODOT_MBI (Glossary p.338 'abutment'); SRC_ODOT_MBI (Glossary p.370 'pier')
- Shot: SC_010
- Chú thích `B04_super` HIGHLIGHT_REGION "Superstructure" → SC_010 / bridge_steel_truss_pratt_01 / steel_truss_bridge_span1_chords_north, steel_truss_bridge_span1_chords_south, steel_truss_bridge_span1_deck …; 72.50–77.92 s; claim CLM_703; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B04.s2 (78.03 s): "The substructure is what holds it up: abutments at the ends, and sometimes piers in between."
- Claim `CLM_702` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.350 'deck')
- Claim `CLM_703` [SOURCE_VERIFIED]: SRC_FHWA_PBES_CH2 (Chapter 2 introduction (AASHTO definition)); SRC_FHWA_PBES_GLOSSARY (Appendix E 'superstructure')
- Claim `CLM_704` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.383 'substructure'); SRC_ODOT_MBI (Glossary p.338 'abutment'); SRC_ODOT_MBI (Glossary p.370 'pier')
- Shot: SC_010
- Chú thích `B04_abut` COMPONENT_LABEL "Abutment" → SC_010 / bridge_steel_truss_pratt_01 / steel_truss_bridge_seat_left; 77.92–91.46 s; claim CLM_704; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS
- Chú thích `B04_pier` COMPONENT_LABEL "Pier" → SC_010 / bridge_steel_truss_pratt_01 / steel_truss_bridge_pier1; 77.92–91.46 s; claim CLM_704; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B04.s3 (85.21 s): "Load follows a path from the deck, through both parts, into the foundations."
- Claim `CLM_702` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.350 'deck')
- Claim `CLM_703` [SOURCE_VERIFIED]: SRC_FHWA_PBES_CH2 (Chapter 2 introduction (AASHTO definition)); SRC_FHWA_PBES_GLOSSARY (Appendix E 'superstructure')
- Claim `CLM_704` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.383 'substructure'); SRC_ODOT_MBI (Glossary p.338 'abutment'); SRC_ODOT_MBI (Glossary p.370 'pier')
- Shot: SC_010
- Chú thích `B04_path` CONCEPTUAL_LOAD_PATH → SC_010 / bridge_steel_truss_pratt_01 / steel_truss_bridge_pier1, steel_truss_bridge_seat_left, steel_truss_bridge_seat_right …; 85.12–91.46 s; claim CLM_704; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS
- Chú thích `B04_found` COMPONENT_LABEL "Foundation" → SC_010 / bridge_steel_truss_pratt_01 / steel_truss_bridge_seat_left; 85.12–91.46 s; claim CLM_704; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B05.s0 (91.86 s): "What changes from one bridge to the next is how that path is arranged."
- Không có claim (câu dẫn dắt).
- Shot: SC_011

## B05.s1 (97.03 s): "So let's start again with an empty gap."
- Không có claim (câu dẫn dắt).
- Shot: SC_011

## B06.s0 (101.32 s): "The first answer is the beam."
- Claim `CLM_705` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.341 'beam')
- Claim `CLM_720` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.3.1 Timber Stringer, p. 3-80)
- Shot: SC_012, SC_013
- Chú thích `B06_ch` NOTE "3 · The beam" → SC_012 / bridge_timber_beam_01 / ; 101.21–109.96 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS
- Chú thích `B06_ch` NOTE "3 · The beam" → SC_013 / bridge_timber_beam_01 / ; 110.29–114.71 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B06.s1 (104.32 s): "Lay a strong member across the gap, support it at each end, and you have a bridge."
- Claim `CLM_705` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.341 'beam')
- Claim `CLM_720` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.3.1 Timber Stringer, p. 3-80)
- Shot: SC_012, SC_013

## B06.s2 (110.49 s): "It is one of the oldest ideas in bridge building."
- Claim `CLM_705` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.341 'beam')
- Claim `CLM_720` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.3.1 Timber Stringer, p. 3-80)
- Shot: SC_012, SC_013

## B07.s0 (115.44 s): "This timber bridge is a row of short beam spans."
- Claim `CLM_705` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.341 'beam')
- Claim `CLM_707` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.344 'cap'); SRC_ODOT_MBI (Glossary p.341 'bent'); SRC_ODOT_MBI (Glossary p.346 'column')
- Shot: SC_014, SC_015

## B07.s1 (119.67 s): "Planks form the deck, long beams carry the planks, cap beams carry the beams, and posts carry the caps."
- Claim `CLM_705` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.341 'beam')
- Claim `CLM_707` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.344 'cap'); SRC_ODOT_MBI (Glossary p.341 'bent'); SRC_ODOT_MBI (Glossary p.346 'column')
- Shot: SC_014, SC_015

## B08.s0 (128.19 s): "Each beam carries its load by resisting bending."
- Claim `CLM_701` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.365 'live load'); SRC_ODOT_MBI (Glossary p.350 'dead load')
- Claim `CLM_706` [SOURCE_VERIFIED]: SRC_FHWA_CBM (Chapter 2, 'Component Terminology'); SRC_ODOT_MBI (Glossary p.358 'girder')
- Claim `CLM_707` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.344 'cap'); SRC_ODOT_MBI (Glossary p.341 'bent'); SRC_ODOT_MBI (Glossary p.346 'column')
- Shot: SC_016
- Chú thích `B08_load` LOAD_ARROW "Load" → SC_016 / bridge_timber_beam_01 / timber_beam_bridge_span3_planks; 128.08–142.38 s; claim CLM_701; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS
- Chú thích `B08_bend` CALLOUT "Beam resists bending" → SC_016 / bridge_timber_beam_01 / timber_beam_bridge_span3_stringers; 128.08–132.38 s; claim CLM_706; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B08.s1 (132.47 s): "At each support, a cap beam spreads the load onto the posts."
- Claim `CLM_706` [SOURCE_VERIFIED]: SRC_FHWA_CBM (Chapter 2, 'Component Terminology'); SRC_ODOT_MBI (Glossary p.358 'girder')
- Claim `CLM_707` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.344 'cap'); SRC_ODOT_MBI (Glossary p.341 'bent'); SRC_ODOT_MBI (Glossary p.346 'column')
- Shot: SC_016
- Chú thích `B08_path` CONCEPTUAL_LOAD_PATH → SC_016 / bridge_timber_beam_01 / timber_beam_bridge_bent3, timber_beam_bridge_bent3_cap, timber_beam_bridge_span3_planks; 132.38–142.38 s; claim CLM_707; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS
- Chú thích `B08_cap` COMPONENT_LABEL "Cap beam" → SC_016 / bridge_timber_beam_01 / timber_beam_bridge_bent3_cap; 132.38–142.38 s; claim CLM_707; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B08.s2 (137.39 s): "The posts then carry it down into the ground in compression."
- Claim `CLM_706` [SOURCE_VERIFIED]: SRC_FHWA_CBM (Chapter 2, 'Component Terminology'); SRC_ODOT_MBI (Glossary p.358 'girder')
- Claim `CLM_707` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.344 'cap'); SRC_ODOT_MBI (Glossary p.341 'bent'); SRC_ODOT_MBI (Glossary p.346 'column')
- Shot: SC_016
- Chú thích `B08_posts` CALLOUT "Posts: compression" → SC_016 / bridge_timber_beam_01 / timber_beam_bridge_bent3; 137.29–142.38 s; claim CLM_707; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B09.s0 (143.11 s): "Beams are simple, and wood was usually easy to find."
- Claim `CLM_721` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.3.1 Timber Stringer, p. 3-80); SRC_NCHRP_CONTEXT (3.3.1 Timber Stringer, p. 3-80)
- Claim `CLM_722` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2 (North Dakota, quoted), p. 2-9)
- Shot: SC_017
- Chú thích `B09_note` NOTE "Illustrative model" → SC_017 / bridge_timber_beam_01 / ; 143.00–167.58 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B09.s1 (148.03 s): "That is why timber beam bridges were still being built long after timber trusses fell out of use, and why they are still built on quiet rural roads and in parks today."
- Claim `CLM_721` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.3.1 Timber Stringer, p. 3-80); SRC_NCHRP_CONTEXT (3.3.1 Timber Stringer, p. 3-80)
- Claim `CLM_722` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2 (North Dakota, quoted), p. 2-9)
- Shot: SC_017

## B09.s2 (159.41 s): "But many early timber bridges had relatively short spans, which is why this one needs so many posts."
- Claim `CLM_721` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.3.1 Timber Stringer, p. 3-80); SRC_NCHRP_CONTEXT (3.3.1 Timber Stringer, p. 3-80)
- Claim `CLM_722` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2 (North Dakota, quoted), p. 2-9)
- Shot: SC_017

## B10.s0 (167.98 s): "A masonry arch takes a different approach."
- Claim `CLM_708` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.388 'voussoir'); SRC_ODOT_MBI (Glossary p.363 'keystone')
- Shot: SC_018, SC_019
- Chú thích `B10_ch` NOTE "4 · The arch" → SC_018 / bridge_stone_arch_03 / ; 167.88–171.38 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B10.s1 (171.56 s): "It is built from wedge-shaped stones called voussoirs, with a keystone at the crown."
- Claim `CLM_708` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.388 'voussoir'); SRC_ODOT_MBI (Glossary p.363 'keystone')
- Shot: SC_018, SC_019
- Chú thích `B10_key` COMPONENT_LABEL "Keystone" → SC_019 / bridge_stone_arch_03 / stone_arch_bridge_arch2_keystone; 172.79–176.92 s; claim CLM_708; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS
- Chú thích `B10_vous` COMPONENT_LABEL "Voussoirs" → SC_019 / bridge_stone_arch_03 / stone_arch_bridge_arch2_voussoir01; 172.96–176.75 s; claim CLM_708; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B11.s0 (178.57 s): "The curve turns the downward load into thrust along the arch, pressing the stones together."
- Claim `CLM_709` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Part 2 Ratings, Item 25 Arch, p.144 (manual p.2-56)); SRC_ODOT_MBI (Glossary p.339 'arch'); SRC_YALE_PHYSICS ('Arch Bridges' section)
- Claim `CLM_710` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.339 'arch'); SRC_YALE_PHYSICS ('Arch Bridges' section)
- Shot: SC_020
- Chú thích `B11_load` LOAD_ARROW "Load" → SC_020 / bridge_stone_arch_03 / stone_arch_bridge_arch2_keystone; 178.46–195.42 s; claim CLM_709; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS
- Chú thích `B11_thrust` CONCEPTUAL_LOAD_PATH → SC_020 / bridge_stone_arch_03 / stone_arch_bridge_arch2_keystone, stone_arch_bridge_arch2_voussoir01, stone_arch_bridge_arch2_voussoir02 …; 178.46–195.42 s; claim CLM_709; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B11.s1 (185.27 s): "So the arch works mainly in compression."
- Claim `CLM_709` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Part 2 Ratings, Item 25 Arch, p.144 (manual p.2-56)); SRC_ODOT_MBI (Glossary p.339 'arch'); SRC_YALE_PHYSICS ('Arch Bridges' section)
- Claim `CLM_710` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.339 'arch'); SRC_YALE_PHYSICS ('Arch Bridges' section)
- Shot: SC_020
- Chú thích `B11_comp` CALLOUT "Mainly compression" → SC_020 / bridge_stone_arch_03 / stone_arch_bridge_arch2_keystone, stone_arch_bridge_arch2_voussoir01, stone_arch_bridge_arch2_voussoir02 …; 185.17–195.42 s; claim CLM_709; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B11.s2 (188.89 s): "At each end it pushes outward and down on its supports, and the supports push back."
- Claim `CLM_709` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Part 2 Ratings, Item 25 Arch, p.144 (manual p.2-56)); SRC_ODOT_MBI (Glossary p.339 'arch'); SRC_YALE_PHYSICS ('Arch Bridges' section)
- Claim `CLM_710` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.339 'arch'); SRC_YALE_PHYSICS ('Arch Bridges' section)
- Shot: SC_020
- Chú thích `B11_react` REACTION_ARROW "Supports push back" → SC_020 / bridge_stone_arch_03 / stone_arch_bridge_arch2_keystone, stone_arch_bridge_arch2_voussoir01, stone_arch_bridge_arch2_voussoir02 …; 188.79–195.42 s; claim CLM_710; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B12.s0 (195.82 s): "That is why arches suit materials that are strong under compression, like stone."
- Claim `CLM_709` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Part 2 Ratings, Item 25 Arch, p.144 (manual p.2-56)); SRC_ODOT_MBI (Glossary p.339 'arch'); SRC_YALE_PHYSICS ('Arch Bridges' section)
- Claim `CLM_710` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.339 'arch'); SRC_YALE_PHYSICS ('Arch Bridges' section)
- Claim `CLM_726` [SOURCE_VERIFIED]: SRC_YALE_PHYSICS (unit 01.05.08, section 6)
- Shot: SC_021

## B12.s1 (201.69 s): "And it is why the supports matter so much: the abutments have to push inward on the arch, against its thrust."
- Claim `CLM_709` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Part 2 Ratings, Item 25 Arch, p.144 (manual p.2-56)); SRC_ODOT_MBI (Glossary p.339 'arch'); SRC_YALE_PHYSICS ('Arch Bridges' section)
- Claim `CLM_710` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.339 'arch'); SRC_YALE_PHYSICS ('Arch Bridges' section)
- Claim `CLM_726` [SOURCE_VERIFIED]: SRC_YALE_PHYSICS (unit 01.05.08, section 6)
- Shot: SC_021
- Chú thích `B12_abut` COMPONENT_LABEL "Abutment" → SC_021 / bridge_stone_arch_03 / stone_arch_bridge_abutment_left; 201.58–210.04 s; claim CLM_710; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS
- Chú thích `B12_pier` COMPONENT_LABEL "Pier" → SC_021 / bridge_stone_arch_03 / stone_arch_bridge_pier1; 201.58–210.04 s; claim CLM_710; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B13.s0 (210.44 s): "Building an arch takes support of its own."
- Claim `CLM_723` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.2.1 Stone Arch, p. 3-48)
- Shot: SC_022

## B13.s1 (213.97 s): "While a stone arch is being built, a temporary timber frame called falsework holds the stones in place."
- Claim `CLM_723` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.2.1 Stone Arch, p. 3-48)
- Shot: SC_022

## B13.s2 (221.84 s): "So building one called for carpenters as well as skilled masons."
- Claim `CLM_723` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.2.1 Stone Arch, p. 3-48)
- Shot: SC_022

## B14.s0 (227.69 s): "Stone arches were generally more expensive to build than timber bridges."
- Claim `CLM_724` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.2.1 Stone Arch, p. 3-49)
- Claim `CLM_725` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.2.1 Stone Arch, p. 3-48)
- Shot: SC_023

## B14.s1 (233.74 s): "But stone was the preferred choice where durability and permanence were required, so arches were favoured on busy routes and in important places."
- Claim `CLM_724` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.2.1 Stone Arch, p. 3-49)
- Claim `CLM_725` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.2.1 Stone Arch, p. 3-48)
- Shot: SC_023

## B14.s2 (243.97 s): "Elsewhere, the lower cost of timber made up for its lack of permanence."
- Claim `CLM_724` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.2.1 Stone Arch, p. 3-49)
- Claim `CLM_725` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.2.1 Stone Arch, p. 3-48)
- Shot: SC_023

## B15.s0 (250.03 s): "A third approach is the truss."
- Claim `CLM_711` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.386 'truss'); SRC_SCI_TRUSSES (Introduction)
- Claim `CLM_712` [SOURCE_VERIFIED]: SRC_SCI_TRUSSES (Introduction); SRC_FHWA_CBM (Chapter 2, 'Component Terminology')
- Shot: SC_024
- Chú thích `B15_ch` NOTE "5 · The truss" → SC_024 / bridge_steel_truss_pratt_01 / ; 249.92–252.88 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B15.s1 (252.97 s): "It builds a structure out of straight members, joined into triangles."
- Claim `CLM_711` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.386 'truss'); SRC_SCI_TRUSSES (Introduction)
- Claim `CLM_712` [SOURCE_VERIFIED]: SRC_SCI_TRUSSES (Introduction); SRC_FHWA_CBM (Chapter 2, 'Component Terminology')
- Shot: SC_024
- Chú thích `B15_joints` COMPONENT_LABEL "Joints" → SC_024 / bridge_steel_truss_pratt_01 / steel_truss_bridge_span1_joints_south; 252.88–265.54 s; claim CLM_711; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B15.s2 (258.20 s): "Each member is mainly pulled or pushed along its length, in tension or in compression."
- Claim `CLM_711` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.386 'truss'); SRC_SCI_TRUSSES (Introduction)
- Claim `CLM_712` [SOURCE_VERIFIED]: SRC_SCI_TRUSSES (Introduction); SRC_FHWA_CBM (Chapter 2, 'Component Terminology')
- Shot: SC_024
- Chú thích `B15_legend` TENSION_COMPRESSION_LEGEND → SC_024 / bridge_steel_truss_pratt_01 / ; 258.08–265.54 s; claim CLM_712; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B16.s0 (265.94 s): "In a simple span like these, under a downward load, the top chord is squeezed and the bottom chord is stretched."
- Claim `CLM_712` [SOURCE_VERIFIED]: SRC_SCI_TRUSSES (Introduction); SRC_FHWA_CBM (Chapter 2, 'Component Terminology')
- Claim `CLM_713` [SOURCE_VERIFIED]: SRC_FHWA_CBM (Chapter 2, 'Component Terminology'); SRC_SCI_TRUSSES ('Types of trusses')
- Claim `CLM_714` [SOURCE_VERIFIED]: SRC_FHWA_CBM (Chapter 2, 'Component Terminology')
- Shot: SC_025
- Chú thích `B16_legend` TENSION_COMPRESSION_LEGEND → SC_025 / bridge_steel_truss_pratt_01 / ; 265.83–280.12 s; claim CLM_712; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS
- Chú thích `B16_top` CALLOUT "Top chord: compression" → SC_025 / bridge_steel_truss_pratt_01 / steel_truss_bridge_span1_chords_south; 269.96–280.12 s; claim CLM_713; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS
- Chú thích `B16_bottom` CALLOUT "Bottom chord: tension" → SC_025 / bridge_steel_truss_pratt_01 / steel_truss_bridge_span1_chords_south; 271.50–280.12 s; claim CLM_713; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B16.s1 (273.92 s): "Inside, some web members are in compression and others are in tension."
- Claim `CLM_713` [SOURCE_VERIFIED]: SRC_FHWA_CBM (Chapter 2, 'Component Terminology'); SRC_SCI_TRUSSES ('Types of trusses')
- Claim `CLM_714` [SOURCE_VERIFIED]: SRC_FHWA_CBM (Chapter 2, 'Component Terminology')
- Shot: SC_025
- Chú thích `B16_web` COMPONENT_LABEL "Web members" → SC_025 / bridge_steel_truss_pratt_01 / steel_truss_bridge_span2_diagonals_south; 273.83–280.12 s; claim CLM_714; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B17.s0 (280.52 s): "The triangles can be arranged in different patterns."
- Claim `CLM_711` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.386 'truss'); SRC_SCI_TRUSSES (Introduction)
- Claim `CLM_727` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-7)
- Claim `CLM_728` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-7)
- Shot: SC_026, SC_027, SC_028

## B17.s1 (284.82 s): "This is a Pratt truss."
- Claim `CLM_711` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.386 'truss'); SRC_SCI_TRUSSES (Introduction)
- Claim `CLM_727` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-7)
- Claim `CLM_728` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-7)
- Shot: SC_026, SC_027, SC_028
- Chú thích `B17_pratt` NOTE "Pratt truss (patented 1844)" → SC_026 / bridge_steel_truss_pratt_01 / ; 284.71–296.25 s; claim CLM_727; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B17.s2 (287.40 s): "In the original design, patented in 1844, its verticals were timber and its diagonals were iron rods."
- Claim `CLM_711` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.386 'truss'); SRC_SCI_TRUSSES (Introduction)
- Claim `CLM_727` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-7)
- Claim `CLM_728` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-7)
- Shot: SC_026, SC_027, SC_028

## B17.s3 (296.77 s): "Swap the web for diagonals that alternate in direction, and you have a Warren truss, patented in 1848."
- Claim `CLM_711` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.386 'truss'); SRC_SCI_TRUSSES (Introduction)
- Claim `CLM_727` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-7)
- Claim `CLM_728` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-7)
- Shot: SC_026, SC_027, SC_028
- Chú thích `B17_warren` NOTE "Warren truss (patented 1848)" → SC_027 / bridge_steel_truss_warren_01 / ; 296.67–304.88 s; claim CLM_728; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS
- Chú thích `B17_warren` NOTE "Warren truss (patented 1848)" → SC_028 / bridge_steel_truss_warren_01 / ; 305.21–312.29 s; claim CLM_728; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B17.s4 (305.38 s): "Both patterns carry load through triangles; they simply arrange the members differently."
- Claim `CLM_711` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.386 'truss'); SRC_SCI_TRUSSES (Introduction)
- Claim `CLM_727` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-7)
- Claim `CLM_728` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-7)
- Shot: SC_026, SC_027, SC_028

## B18.s0 (312.69 s): "Trusses also changed how bridges were built."
- Claim `CLM_729` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2 'Foundries and Fabricators', p. 2-11)
- Shot: SC_029

## B18.s1 (316.52 s): "By the middle of the nineteenth century, shops were making and drilling truss members, then shipping them to the bridge site, ready to assemble."
- Claim `CLM_729` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2 'Foundries and Fabricators', p. 2-11)
- Shot: SC_029
- Chú thích `B18_shop` NOTE "Members made and drilled in shops" → SC_029 / bridge_steel_truss_pratt_01 / ; 316.42–326.08 s; claim CLM_729; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B18.s2 (326.17 s): "And by 1860, the railroads relied almost entirely on these prefabricated parts."
- Claim `CLM_729` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2 'Foundries and Fabricators', p. 2-11)
- Shot: SC_029
- Chú thích `B18_1860` NOTE "By 1860: prefabricated parts" → SC_029 / bridge_steel_truss_pratt_01 / ; 326.08–333.96 s; claim CLM_729; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B40.s0 (334.36 s): "To cross wide rivers and deep gorges, bridges needed longer spans."
- Claim `CLM_752` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-142); SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-142)
- Claim `CLM_757` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-142); SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-142)
- Shot: SC_030
- Chú thích `B40_ch` NOTE "6 · The cantilever" → SC_030 / None / ; 334.25–349.25 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B40.s1 (340.13 s): "Beam and arch bridges of steel or reinforced concrete were limited to spans of about 200 to 300 feet."
- Claim `CLM_752` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-142); SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-142)
- Claim `CLM_757` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-142); SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-142)
- Shot: SC_030
- Chú thích `B40_note` NOTE "A wider crossing (illustrative, not to scale)" → SC_030 / None / ; 340.04–349.25 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B41.s0 (349.98 s): "One answer was the cantilever."
- Claim `CLM_750` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-142); SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-142)
- Shot: SC_031

## B41.s1 (353.33 s): "Hold your arm straight out from your shoulder, and it is acting as a cantilever: supported at one end, free at the other, like a diving board."
- Claim `CLM_750` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-142); SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-142)
- Shot: SC_031
- Chú thích `B41_note` NOTE "Illustrative model" → SC_031 / bridge_cantilever_truss_01 / ; 353.25–363.62 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B42.s0 (364.02 s): "A cantilever bridge is a modified beam."
- Claim `CLM_750` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-142); SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-142)
- Claim `CLM_751` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.1 Trusses, p. 3-4); SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-142)
- Shot: SC_032

## B42.s1 (368.10 s): "Anchor arms rest on the banks and the main piers, cantilever arms reach out over the river, and a suspended span hangs between their tips."
- Claim `CLM_750` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-142); SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-142)
- Claim `CLM_751` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.1 Trusses, p. 3-4); SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-142)
- Shot: SC_032
- Chú thích `B42_anchor` COMPONENT_LABEL "Anchor arm" → SC_032 / bridge_cantilever_truss_01 / cantilever_bridge_anchor_arm_left_south; 368.00–378.71 s; claim CLM_751; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS
- Chú thích `B42_arm` COMPONENT_LABEL "Cantilever arm" → SC_032 / bridge_cantilever_truss_01 / cantilever_bridge_cantilever_arm_left_south; 371.42–378.71 s; claim CLM_751; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS
- Chú thích `B42_span` COMPONENT_LABEL "Suspended span" → SC_032 / bridge_cantilever_truss_01 / cantilever_bridge_suspended_span_south; 374.67–378.71 s; claim CLM_751; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B43.s0 (379.11 s): "Its great advantage came during construction."
- Claim `CLM_753` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-143)
- Shot: SC_033

## B43.s1 (382.96 s): "The arms could be built outward from the piers with no falsework blocking the channel below, and then the suspended span was lifted into place."
- Claim `CLM_753` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-143)
- Shot: SC_033
- Chú thích `B43_note` NOTE "Built outward: no falsework in the channel" → SC_033 / bridge_cantilever_truss_01 / ; 382.88–393.54 s; claim CLM_753; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B44.s0 (393.94 s): "In the United States, cantilevers were a standard answer for intermediate to longer spans from the 1880s to the 1960s."
- Claim `CLM_754` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-143)
- Claim `CLM_756` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-143)
- Shot: SC_034

## B44.s1 (403.72 s): "The Queensboro Bridge in New York was the country's longest cantilever when it was completed in 1909."
- Claim `CLM_754` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-143)
- Claim `CLM_756` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-143)
- Shot: SC_034

## B45.s0 (413.11 s): "For the longest spans of all, engineers hung the deck instead."
- Claim `CLM_760` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-133)
- Claim `CLM_763` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-133); SRC_FHWA_BRIDGE_TYPES (2.6 Suspension Bridges)
- Shot: SC_035
- Chú thích `B45_ch` NOTE "7 · The suspension bridge" → SC_035 / bridge_suspension_01 / ; 413.00–425.50 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS
- Chú thích `B45_model` NOTE "Illustrative model" → SC_035 / bridge_suspension_01 / ; 413.00–425.50 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B45.s1 (418.13 s): "In a suspension bridge, the deck hangs from vertical suspenders attached to great main cables."
- Claim `CLM_760` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-133)
- Claim `CLM_763` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-133); SRC_FHWA_BRIDGE_TYPES (2.6 Suspension Bridges)
- Shot: SC_035
- Chú thích `B45_hangers` COMPONENT_LABEL "Suspenders" → SC_035 / bridge_suspension_01 / suspension_bridge_hangers_south; 421.62–425.50 s; claim CLM_760; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS
- Chú thích `B45_cable` COMPONENT_LABEL "Main cable" → SC_035 / bridge_suspension_01 / suspension_bridge_main_cable_south; 422.33–425.50 s; claim CLM_760; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B46.s0 (426.23 s): "The cables are in tension, and they pass over towers that are in compression."
- Claim `CLM_760` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-133)
- Claim `CLM_761` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-133); SRC_FHWA_BRIDGE_TYPES (2.6 Suspension Bridges)
- Shot: SC_036
- Chú thích `B46_load` LOAD_ARROW "Load" → SC_036 / bridge_suspension_01 / suspension_bridge_deck; 426.12–438.83 s; claim CLM_760; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS
- Chú thích `B46_cable` CALLOUT "Cables: tension" → SC_036 / bridge_suspension_01 / suspension_bridge_main_cable_south; 427.50–438.83 s; claim CLM_760; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS
- Chú thích `B46_tower` CALLOUT "Towers: compression" → SC_036 / bridge_suspension_01 / suspension_bridge_tower_right; 430.25–438.83 s; claim CLM_760; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B46.s1 (432.06 s): "At each end, the cables are anchored, usually in large masses of stone or concrete."
- Claim `CLM_760` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-133)
- Claim `CLM_761` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-133); SRC_FHWA_BRIDGE_TYPES (2.6 Suspension Bridges)
- Shot: SC_036
- Chú thích `B46_anchor` COMPONENT_LABEL "Anchorage" → SC_036 / bridge_suspension_01 / suspension_bridge_anchorage_left; 433.58–438.83 s; claim CLM_761; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B47.s0 (439.57 s): "A suspension deck is light for its span, and it can be very flexible."
- Claim `CLM_765` [SOURCE_VERIFIED]: SRC_FHWA_BRIDGE_TYPES (2.6 Suspension Bridges); SRC_FHWA_BRIDGE_TYPES (2.6 Suspension Bridges)
- Shot: SC_037, SC_038

## B47.s1 (445.22 s): "So a stiffening truss is commonly built under the deck, against wind and earthquakes."
- Claim `CLM_765` [SOURCE_VERIFIED]: SRC_FHWA_BRIDGE_TYPES (2.6 Suspension Bridges); SRC_FHWA_BRIDGE_TYPES (2.6 Suspension Bridges)
- Shot: SC_037, SC_038
- Chú thích `B47_note` NOTE "Stiffening truss under the deck" → SC_038 / bridge_suspension_01 / ; 445.12–451.92 s; claim CLM_765; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B48.s0 (452.32 s): "Towers, cables and suspenders, anchorages and a stiffening truss: these are the features that define a suspension bridge."
- Claim `CLM_764` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-133)
- Claim `CLM_768` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-143); SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-133)
- Shot: SC_039

## B48.s1 (461.54 s): "The Brooklyn Bridge in New York, completed in 1883, has them all, and one report says few suspension bridges since can claim to stand entirely clear of its shadow."
- Claim `CLM_764` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-133)
- Claim `CLM_768` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-143); SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-133)
- Shot: SC_039

## B50.s0 (475.40 s): "A cable-stayed bridge also relies on steel cables, but it uses them differently."
- Claim `CLM_770` [SOURCE_VERIFIED]: SRC_FHWA_BRIDGE_TYPES (2.5 Cable-Stayed)
- Claim `CLM_771` [SOURCE_VERIFIED]: SRC_FHWA_BRIDGE_TYPES (2.5 Cable-Stayed); SRC_FHWA_BRIDGE_TYPES (2.5 Cable-Stayed)
- Shot: SC_040
- Chú thích `B50_ch` NOTE "8 · The cable-stayed bridge" → SC_040 / bridge_cable_stayed_01 / ; 475.29–488.71 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS
- Chú thích `B50_model` NOTE "Illustrative model" → SC_040 / bridge_cable_stayed_01 / ; 475.29–488.71 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B50.s1 (482.05 s): "Straight stay cables run from tall towers directly down to the edges of the deck."
- Claim `CLM_770` [SOURCE_VERIFIED]: SRC_FHWA_BRIDGE_TYPES (2.5 Cable-Stayed)
- Claim `CLM_771` [SOURCE_VERIFIED]: SRC_FHWA_BRIDGE_TYPES (2.5 Cable-Stayed); SRC_FHWA_BRIDGE_TYPES (2.5 Cable-Stayed)
- Shot: SC_040
- Chú thích `B50_stays` COMPONENT_LABEL "Stay cables" → SC_040 / bridge_cable_stayed_01 / cable_stayed_bridge_stay_left_side5; 482.58–488.71 s; claim CLM_770; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS
- Chú thích `B50_tower` COMPONENT_LABEL "Tower" → SC_040 / bridge_cable_stayed_01 / cable_stayed_bridge_pylon_right; 484.25–488.71 s; claim CLM_770; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B51.s0 (489.11 s): "Seen in outline, the difference is clear."
- Claim `CLM_761` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-133); SRC_FHWA_BRIDGE_TYPES (2.6 Suspension Bridges)
- Claim `CLM_763` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-133); SRC_FHWA_BRIDGE_TYPES (2.6 Suspension Bridges)
- Claim `CLM_770` [SOURCE_VERIFIED]: SRC_FHWA_BRIDGE_TYPES (2.5 Cable-Stayed)
- Claim `CLM_771` [SOURCE_VERIFIED]: SRC_FHWA_BRIDGE_TYPES (2.5 Cable-Stayed); SRC_FHWA_BRIDGE_TYPES (2.5 Cable-Stayed)
- Shot: SC_041

## B51.s1 (492.63 s): "The suspension bridge has shorter towers, and its main cables run over them to anchorages at each end."
- Claim `CLM_761` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-133); SRC_FHWA_BRIDGE_TYPES (2.6 Suspension Bridges)
- Claim `CLM_763` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-133); SRC_FHWA_BRIDGE_TYPES (2.6 Suspension Bridges)
- Claim `CLM_770` [SOURCE_VERIFIED]: SRC_FHWA_BRIDGE_TYPES (2.5 Cable-Stayed)
- Claim `CLM_771` [SOURCE_VERIFIED]: SRC_FHWA_BRIDGE_TYPES (2.5 Cable-Stayed); SRC_FHWA_BRIDGE_TYPES (2.5 Cable-Stayed)
- Shot: SC_041

## B51.s2 (500.51 s): "The cable-stayed bridge needs much taller towers, and its stays end at the deck itself."
- Claim `CLM_761` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-133); SRC_FHWA_BRIDGE_TYPES (2.6 Suspension Bridges)
- Claim `CLM_763` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-133); SRC_FHWA_BRIDGE_TYPES (2.6 Suspension Bridges)
- Claim `CLM_770` [SOURCE_VERIFIED]: SRC_FHWA_BRIDGE_TYPES (2.5 Cable-Stayed)
- Claim `CLM_771` [SOURCE_VERIFIED]: SRC_FHWA_BRIDGE_TYPES (2.5 Cable-Stayed); SRC_FHWA_BRIDGE_TYPES (2.5 Cable-Stayed)
- Shot: SC_041

## B52.s0 (507.90 s): "Once the towers are up, the deck can be built outward from them in both directions, without falsework towers, until the spans meet."
- Claim `CLM_772` [SOURCE_VERIFIED]: SRC_FHWA_BRIDGE_TYPES (4.4 Cable-Stayed Bridges)
- Claim `CLM_773` [SOURCE_VERIFIED]: SRC_FHWA_BRIDGE_TYPES (2.5 Cable-Stayed)
- Shot: SC_042
- Chú thích `B52_note` NOTE "Built outward from the towers" → SC_042 / bridge_cable_stayed_01 / ; 507.79–517.33 s; claim CLM_772; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B52.s1 (517.42 s): "The stays also squeeze the deck along its length, and that squeeze builds up toward the towers."
- Claim `CLM_772` [SOURCE_VERIFIED]: SRC_FHWA_BRIDGE_TYPES (4.4 Cable-Stayed Bridges)
- Claim `CLM_773` [SOURCE_VERIFIED]: SRC_FHWA_BRIDGE_TYPES (2.5 Cable-Stayed)
- Shot: SC_042
- Chú thích `B52_deck` CALLOUT "Deck: squeezed by the stays" → SC_042 / bridge_cable_stayed_01 / cable_stayed_bridge_deck_closure; 518.54–522.46 s; claim CLM_773; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B53.s0 (524.98 s): "Before 1970, suspension bridges were thought to be the cheapest way to span more than about 1,200 feet."
- Claim `CLM_774` [SOURCE_VERIFIED]: SRC_FHWA_BRIDGE_TYPES (3.0 Economics)
- Claim `CLM_775` [SOURCE_VERIFIED]: SRC_FHWA_BRIDGE_TYPES (3.0 Economics)
- Shot: SC_043

## B53.s1 (534.28 s): "By 2012, a federal handbook said cable-stayed bridges become very competitive above 750 feet, and that suspension bridges pay off only as main spans approach 3,000."
- Claim `CLM_774` [SOURCE_VERIFIED]: SRC_FHWA_BRIDGE_TYPES (3.0 Economics)
- Claim `CLM_775` [SOURCE_VERIFIED]: SRC_FHWA_BRIDGE_TYPES (3.0 Economics)
- Shot: SC_043

## B19.s0 (549.61 s): "So which design is best?"
- Không có claim (câu dẫn dắt).
- Shot: SC_044

## B19.s1 (552.41 s): "The honest answer is that it depends."
- Không có claim (câu dẫn dắt).
- Shot: SC_044

## B19.s2 (555.76 s): "Materials, the site, the span, cost, and the skills available all pull in different directions."
- Không có claim (câu dẫn dắt).
- Shot: SC_044

## B20A.s0 (564.02 s): "Start with the materials themselves."
- Claim `CLM_726` [SOURCE_VERIFIED]: SRC_YALE_PHYSICS (unit 01.05.08, section 6)
- Shot: SC_045

## B20A.s1 (567.20 s): "An arch needs a material that is strong under compression, and stone is."
- Claim `CLM_726` [SOURCE_VERIFIED]: SRC_YALE_PHYSICS (unit 01.05.08, section 6)
- Shot: SC_045
- Chú thích `B20A_note` NOTE "Stone: strong under compression" → SC_045 / bridge_stone_arch_03 / ; 567.08–573.29 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B20B.s0 (573.69 s): "A truss needs members that can work in tension as well as compression."
- Claim `CLM_712` [SOURCE_VERIFIED]: SRC_SCI_TRUSSES (Introduction); SRC_FHWA_CBM (Chapter 2, 'Component Terminology')
- Claim `CLM_735` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-8)
- Shot: SC_046
- Chú thích `B20B_note` NOTE "Truss members: tension and compression" → SC_046 / bridge_steel_truss_pratt_01 / ; 573.58–579.33 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B20B.s1 (579.42 s): "Wrought iron was valued for exactly that: one historian calls it a material strong equally in tension and in compression."
- Claim `CLM_712` [SOURCE_VERIFIED]: SRC_SCI_TRUSSES (Introduction); SRC_FHWA_CBM (Chapter 2, 'Component Terminology')
- Claim `CLM_735` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-8)
- Shot: SC_046
- Chú thích `B20B_iron` NOTE "Wrought iron: valued in tension and compression" → SC_046 / bridge_steel_truss_pratt_01 / ; 579.33–589.17 s; claim CLM_735; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B20C.s0 (589.57 s): "Wood was often plentiful and cheap, but wooden bridges were vulnerable to decay."
- Claim `CLM_734` [SOURCE_VERIFIED]: SRC_ASCE_BOLLMAN (main text)
- Claim `CLM_742` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Shot: SC_047
- Chú thích `B20C_note` NOTE "Timber: plentiful and cheap, but it decays" → SC_047 / bridge_timber_beam_01 / ; 589.46–596.42 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B21.s0 (596.82 s): "That is one reason many timber truss bridges were covered with a roof and siding, to protect them from the weather."
- Claim `CLM_733` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.1.1 King Post, p. 3-7)
- Claim `CLM_746` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (List of figures, 3-5)
- Shot: SC_048

## B21.s1 (605.14 s): "This is the Humpback Covered Bridge, built in 1857 over Dunlap Creek."
- Claim `CLM_733` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.1.1 King Post, p. 3-7)
- Claim `CLM_746` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (List of figures, 3-5)
- Shot: SC_048

## B20E.s0 (612.82 s): "Cables have a materials story of their own."
- Claim `CLM_780` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-132); SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-132)
- Claim `CLM_781` [SOURCE_VERIFIED]: SRC_FHWA_BRIDGE_TYPES (2.5 Cable-Stayed); SRC_FHWA_BRIDGE_TYPES (2.6 Suspension Bridges)
- Shot: SC_049
- Chú thích `B20E_model` NOTE "Illustrative model" → SC_049 / bridge_suspension_01 / ; 612.71–639.17 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B20E.s1 (616.49 s): "America's first metal suspension bridges hung from iron chains, and many failed after only a few years: critics said such a bridge was only as good as the weakest link in one of its chains."
- Claim `CLM_780` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-132); SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-132)
- Claim `CLM_781` [SOURCE_VERIFIED]: SRC_FHWA_BRIDGE_TYPES (2.5 Cable-Stayed); SRC_FHWA_BRIDGE_TYPES (2.6 Suspension Bridges)
- Shot: SC_049
- Chú thích `B20E_chain` NOTE "Iron chains: only as strong as the weakest link" → SC_049 / bridge_suspension_01 / ; 616.38–630.00 s; claim CLM_780; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B20E.s2 (630.12 s): "Wire cables answered that fear, and suspension and cable-stayed bridges now rely on high-strength steel cables."
- Claim `CLM_780` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-132); SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-132)
- Claim `CLM_781` [SOURCE_VERIFIED]: SRC_FHWA_BRIDGE_TYPES (2.5 Cable-Stayed); SRC_FHWA_BRIDGE_TYPES (2.6 Suspension Bridges)
- Shot: SC_049
- Chú thích `B20E_cable` NOTE "Wire cables, then high-strength steel" → SC_049 / bridge_suspension_01 / ; 630.00–639.17 s; claim CLM_781; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B22.s0 (639.57 s): "The site of a bridge matters too."
- Claim `CLM_736` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.6 Trestles and Viaducts, p. 3-137); SRC_NCHRP_CONTEXT (3.6 Trestles and Viaducts, p. 3-137)
- Shot: SC_050

## B22.s1 (642.64 s): "Railway engines have limited traction, so railways need gentle gradients."
- Claim `CLM_736` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.6 Trestles and Viaducts, p. 3-137); SRC_NCHRP_CONTEXT (3.6 Trestles and Viaducts, p. 3-137)
- Shot: SC_050

## B22.s2 (648.77 s): "Where a valley was too deep and wide to fill with an embankment, engineers built viaducts and trestles to keep the line nearly straight and level."
- Claim `CLM_736` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.6 Trestles and Viaducts, p. 3-137); SRC_NCHRP_CONTEXT (3.6 Trestles and Viaducts, p. 3-137)
- Shot: SC_050

## B22B.s0 (659.65 s): "Long spans make the ground beneath them matter even more."
- Claim `CLM_761` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-133); SRC_FHWA_BRIDGE_TYPES (2.6 Suspension Bridges)
- Claim `CLM_776` [SOURCE_VERIFIED]: SRC_FHWA_BRIDGE_TYPES (3.0 Economics)
- Shot: SC_051

## B22B.s1 (664.55 s): "A suspension bridge has to anchor its cables in massive blocks, or directly in bedrock."
- Claim `CLM_761` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-133); SRC_FHWA_BRIDGE_TYPES (2.6 Suspension Bridges)
- Claim `CLM_776` [SOURCE_VERIFIED]: SRC_FHWA_BRIDGE_TYPES (3.0 Economics)
- Shot: SC_051

## B22B.s2 (671.52 s): "The towers of a cable-stayed bridge, by contrast, can be built where good rock does not lie near the surface."
- Claim `CLM_761` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-133); SRC_FHWA_BRIDGE_TYPES (2.6 Suspension Bridges)
- Claim `CLM_776` [SOURCE_VERIFIED]: SRC_FHWA_BRIDGE_TYPES (3.0 Economics)
- Shot: SC_051

## B22C.s0 (680.36 s): "Cantilevers had an advantage on uncertain ground."
- Claim `CLM_782` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-142)
- Shot: SC_052
- Chú thích `B22C_model` NOTE "Illustrative model" → SC_052 / bridge_cantilever_truss_01 / ; 680.25–694.83 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B22C.s1 (684.66 s): "Unstable soil troubled many foundations, and if a pier sank, a cantilever could adjust, where a continuous beam might fail."
- Claim `CLM_782` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-142)
- Shot: SC_052
- Chú thích `B22C_note` NOTE "If a pier sank, the cantilever could adjust" → SC_052 / bridge_cantilever_truss_01 / ; 684.54–694.83 s; claim CLM_782; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS
- Chú thích `B22C_pier` COMPONENT_LABEL "Main pier" → SC_052 / bridge_cantilever_truss_01 / cantilever_bridge_pier_left; 688.38–694.83 s; claim CLM_782; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B22D.s0 (695.23 s): "Then there is the wind."
- Claim `CLM_765` [SOURCE_VERIFIED]: SRC_FHWA_BRIDGE_TYPES (2.6 Suspension Bridges); SRC_FHWA_BRIDGE_TYPES (2.6 Suspension Bridges)
- Claim `CLM_783` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-28); SRC_NCHRP_CONTEXT (2.2, p. 2-28); SRC_FHWA_BRIDGE_TYPES (2.6 Suspension Bridges)
- Shot: SC_053
- Chú thích `B22D_model` NOTE "Illustrative model" → SC_053 / bridge_suspension_01 / ; 695.12–716.29 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B22D.s1 (697.86 s): "In 1940, the four-month-old Tacoma Narrows suspension bridge collapsed in only moderately high winds."
- Claim `CLM_765` [SOURCE_VERIFIED]: SRC_FHWA_BRIDGE_TYPES (2.6 Suspension Bridges); SRC_FHWA_BRIDGE_TYPES (2.6 Suspension Bridges)
- Claim `CLM_783` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-28); SRC_NCHRP_CONTEXT (2.2, p. 2-28); SRC_FHWA_BRIDGE_TYPES (2.6 Suspension Bridges)
- Shot: SC_053
- Chú thích `B22D_tacoma` NOTE "Tacoma Narrows, 1940: lost to the wind" → SC_053 / bridge_suspension_01 / ; 697.75–706.54 s; claim CLM_783; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B22D.s2 (706.63 s): "The disaster led to intense research on wind, and later suspension bridges were built to new standards for stiffened decks."
- Claim `CLM_765` [SOURCE_VERIFIED]: SRC_FHWA_BRIDGE_TYPES (2.6 Suspension Bridges); SRC_FHWA_BRIDGE_TYPES (2.6 Suspension Bridges)
- Claim `CLM_783` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-28); SRC_NCHRP_CONTEXT (2.2, p. 2-28); SRC_FHWA_BRIDGE_TYPES (2.6 Suspension Bridges)
- Shot: SC_053
- Chú thích `B22D_stiff` NOTE "Afterwards: research and stiffened decks" → SC_053 / bridge_suspension_01 / ; 706.54–716.29 s; claim CLM_783; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS
- Chú thích `B22D_truss` COMPONENT_LABEL "Stiffening truss" → SC_053 / bridge_suspension_01 / suspension_bridge_stiffening_truss_south; 706.54–716.29 s; claim CLM_765; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B23C.s0 (716.69 s): "Span decides a great deal."
- Claim `CLM_775` [SOURCE_VERIFIED]: SRC_FHWA_BRIDGE_TYPES (3.0 Economics)
- Claim `CLM_784` [SOURCE_VERIFIED]: SRC_FHWA_BRIDGE_TYPES (3.0 Economics)
- Claim `CLM_785` [SOURCE_VERIFIED]: SRC_FHWA_BRIDGE_TYPES (3.0 Economics); SRC_FHWA_BRIDGE_TYPES (3.0 Economics)
- Claim `CLM_786` [SOURCE_VERIFIED]: SRC_FHWA_BRIDGE_TYPES (3.0 Economics); SRC_FHWA_BRIDGE_TYPES (3.0 Economics)
- Shot: SC_054

## B23C.s1 (719.62 s): "In steel, a federal handbook puts plate girders at about 90 to over 500 feet, simple trusses at up to about 750, and cantilever trusses considerably farther."
- Claim `CLM_775` [SOURCE_VERIFIED]: SRC_FHWA_BRIDGE_TYPES (3.0 Economics)
- Claim `CLM_784` [SOURCE_VERIFIED]: SRC_FHWA_BRIDGE_TYPES (3.0 Economics)
- Claim `CLM_785` [SOURCE_VERIFIED]: SRC_FHWA_BRIDGE_TYPES (3.0 Economics); SRC_FHWA_BRIDGE_TYPES (3.0 Economics)
- Claim `CLM_786` [SOURCE_VERIFIED]: SRC_FHWA_BRIDGE_TYPES (3.0 Economics); SRC_FHWA_BRIDGE_TYPES (3.0 Economics)
- Shot: SC_054

## B23C.s2 (733.37 s): "Arches have spanned from about 200 to 1,800 feet, and cable-stayed bridges from under 200 to nearly 3,000."
- Claim `CLM_775` [SOURCE_VERIFIED]: SRC_FHWA_BRIDGE_TYPES (3.0 Economics)
- Claim `CLM_784` [SOURCE_VERIFIED]: SRC_FHWA_BRIDGE_TYPES (3.0 Economics)
- Claim `CLM_785` [SOURCE_VERIFIED]: SRC_FHWA_BRIDGE_TYPES (3.0 Economics); SRC_FHWA_BRIDGE_TYPES (3.0 Economics)
- Claim `CLM_786` [SOURCE_VERIFIED]: SRC_FHWA_BRIDGE_TYPES (3.0 Economics); SRC_FHWA_BRIDGE_TYPES (3.0 Economics)
- Shot: SC_054

## B23C.s3 (743.79 s): "And as we saw, suspension bridges only pay off as main spans approach 3,000 feet."
- Claim `CLM_775` [SOURCE_VERIFIED]: SRC_FHWA_BRIDGE_TYPES (3.0 Economics)
- Claim `CLM_784` [SOURCE_VERIFIED]: SRC_FHWA_BRIDGE_TYPES (3.0 Economics)
- Claim `CLM_785` [SOURCE_VERIFIED]: SRC_FHWA_BRIDGE_TYPES (3.0 Economics); SRC_FHWA_BRIDGE_TYPES (3.0 Economics)
- Claim `CLM_786` [SOURCE_VERIFIED]: SRC_FHWA_BRIDGE_TYPES (3.0 Economics); SRC_FHWA_BRIDGE_TYPES (3.0 Economics)
- Shot: SC_054

## B23D.s0 (751.69 s): "Cost and skill pull in different directions."
- Claim `CLM_757` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-142); SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-142)
- Claim `CLM_787` [SOURCE_VERIFIED]: SRC_FHWA_BRIDGE_TYPES (4.5 Suspension Bridges); SRC_FHWA_BRIDGE_TYPES (4.5 Suspension Bridges)
- Shot: SC_055
- Chú thích `B23D_model` NOTE "Illustrative model" → SC_055 / bridge_suspension_01 / ; 751.58–772.79 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B23D.s1 (755.34 s): "A cantilever avoided the expensive anchorages a suspension bridge needs."
- Claim `CLM_757` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-142); SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-142)
- Claim `CLM_787` [SOURCE_VERIFIED]: SRC_FHWA_BRIDGE_TYPES (4.5 Suspension Bridges); SRC_FHWA_BRIDGE_TYPES (4.5 Suspension Bridges)
- Shot: SC_055
- Chú thích `B23D_anchor` COMPONENT_LABEL "Anchorages: costly" → SC_055 / bridge_suspension_01 / suspension_bridge_anchorage_left; 758.17–772.79 s; claim CLM_757; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B23D.s2 (761.57 s): "And a suspension bridge often takes a long time to build: installing its main cables calls for expertise that very few contractors have."
- Claim `CLM_757` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-142); SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-142)
- Claim `CLM_787` [SOURCE_VERIFIED]: SRC_FHWA_BRIDGE_TYPES (4.5 Suspension Bridges); SRC_FHWA_BRIDGE_TYPES (4.5 Suspension Bridges)
- Shot: SC_055
- Chú thích `B23D_cable` COMPONENT_LABEL "Main cables: specialist work" → SC_055 / bridge_suspension_01 / suspension_bridge_main_cable_south; 766.17–772.79 s; claim CLM_787; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B23E.s0 (773.19 s): "Cable-stayed bridges are becoming more common worldwide, and one significant reason is that the methods for erecting them are now better understood."
- Claim `CLM_788` [SOURCE_VERIFIED]: SRC_FHWA_BRIDGE_TYPES (4.4 Cable-Stayed Bridges)
- Shot: SC_056
- Chú thích `B23E_note` NOTE "Erection methods now better understood" → SC_056 / bridge_cable_stayed_01 / ; 773.08–784.50 s; claim CLM_788; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B24.s0 (784.90 s): "Finally, every bridge belongs to its time."
- Claim `CLM_727` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-7)
- Claim `CLM_728` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-7)
- Claim `CLM_729` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2 'Foundries and Fabricators', p. 2-11)
- Claim `CLM_738` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.2.1 Stone Arch, p. 3-49)
- Claim `CLM_739` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Shot: SC_057

## B24.s1 (788.88 s): "As metal trusses spread, skilled masons became fewer and reinforced concrete arrived, stone arch construction declined."
- Claim `CLM_727` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-7)
- Claim `CLM_728` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-7)
- Claim `CLM_729` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2 'Foundries and Fabricators', p. 2-11)
- Claim `CLM_738` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.2.1 Stone Arch, p. 3-49)
- Claim `CLM_739` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Shot: SC_057

## B24.s2 (798.38 s): "Then, during the Great Depression, it briefly returned."
- Claim `CLM_727` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-7)
- Claim `CLM_728` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-7)
- Claim `CLM_729` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2 'Foundries and Fabricators', p. 2-11)
- Claim `CLM_738` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.2.1 Stone Arch, p. 3-49)
- Claim `CLM_739` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Shot: SC_057

## B24B.s0 (803.57 s): "Long spans have a timeline of their own."
- Claim `CLM_754` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-143)
- Claim `CLM_756` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-143)
- Claim `CLM_766` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-132); SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-133)
- Claim `CLM_768` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-143); SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-133)
- Claim `CLM_774` [SOURCE_VERIFIED]: SRC_FHWA_BRIDGE_TYPES (3.0 Economics)
- Shot: SC_058

## B24B.s1 (807.14 s): "By 1849, a suspension bridge at Wheeling spanned 1,010 feet, the longest bridge in the world for many years."
- Claim `CLM_754` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-143)
- Claim `CLM_756` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-143)
- Claim `CLM_766` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-132); SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-133)
- Claim `CLM_768` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-143); SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-133)
- Claim `CLM_774` [SOURCE_VERIFIED]: SRC_FHWA_BRIDGE_TYPES (3.0 Economics)
- Shot: SC_058

## B24B.s2 (816.92 s): "Cantilevers were a standard American answer from the 1880s to the 1960s, and since 1980 almost every American bridge with a main span over 1,000 feet has been cable-stayed."
- Claim `CLM_754` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-143)
- Claim `CLM_756` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-143)
- Claim `CLM_766` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-132); SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-133)
- Claim `CLM_768` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-143); SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-133)
- Claim `CLM_774` [SOURCE_VERIFIED]: SRC_FHWA_BRIDGE_TYPES (3.0 Economics)
- Shot: SC_058

## B25.s0 (832.44 s): "These trade-offs played out across nineteenth-century America as the railways spread."
- Claim `CLM_741` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6); SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Claim `CLM_742` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Shot: SC_059

## B25.s1 (838.79 s): "In the East, railroads built massive stone viaducts, while western builders generally used timber."
- Claim `CLM_741` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6); SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Claim `CLM_742` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Shot: SC_059

## B25.s2 (846.57 s): "Three documented examples show how differently builders answered."
- Claim `CLM_741` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6); SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Claim `CLM_742` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Shot: SC_059

## B26.s0 (852.82 s): "Near Baltimore, the Carrollton Viaduct was completed in 1829."
- Claim `CLM_739` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Claim `CLM_740` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.6 Trestles and Viaducts, p. 3-137)
- Shot: SC_060

## B26.s1 (858.89 s): "Built of roughly twelve thousand granite blocks, it carries the railway over Gwynns Falls on an eighty foot arch."
- Claim `CLM_739` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Claim `CLM_740` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.6 Trestles and Viaducts, p. 3-137)
- Shot: SC_060

## B26.s2 (867.32 s): "A national report in 2005 called it the world's oldest stone railroad span still in service."
- Claim `CLM_739` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Claim `CLM_740` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.6 Trestles and Viaducts, p. 3-137)
- Shot: SC_060

## B27.s0 (875.94 s): "Early railroads needed durable bridges to carry heavy trains."
- Claim `CLM_725` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.2.1 Stone Arch, p. 3-48)
- Claim `CLM_741` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6); SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Shot: SC_061
- Chú thích `B27_note` NOTE "Illustrative model, not the Carrollton Viaduct" → SC_061 / bridge_stone_arch_03 / ; 875.83–885.67 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B27.s1 (881.07 s): "For a line meant to last, stone was the answer."
- Claim `CLM_725` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.2.1 Stone Arch, p. 3-48)
- Claim `CLM_741` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6); SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Shot: SC_061

## B28.s0 (886.07 s): "In the West, the pressure was different."
- Claim `CLM_742` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Claim `CLM_743` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (List of figures, 3-106)
- Shot: SC_062

## B28.s1 (889.32 s): "Railroads had to open new lines quickly and economically, and timber was abundant and cheap."
- Claim `CLM_742` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Claim `CLM_743` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (List of figures, 3-106)
- Shot: SC_062

## B28.s2 (896.37 s): "This timber trestle near Corinne, Utah, was built in 1872 by the Central Pacific Railroad."
- Claim `CLM_742` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Claim `CLM_743` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (List of figures, 3-106)
- Shot: SC_062

## B29.s0 (905.82 s): "A trestle is a succession of towers supporting short spans."
- Claim `CLM_737` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.6 Trestles and Viaducts, p. 3-137)
- Shot: SC_063
- Chú thích `B29_note` NOTE "Illustrative model, not the Promontory trestle" → SC_063 / bridge_timber_beam_01 / ; 905.71–917.92 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B29.s1 (910.67 s): "It is the same beam idea as our timber model, repeated as often as the crossing needs."
- Claim `CLM_737` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.6 Trestles and Viaducts, p. 3-137)
- Shot: SC_063

## B30.s0 (918.32 s): "Iron offered a third path."
- Claim `CLM_744` [SOURCE_VERIFIED]: SRC_ASCE_BOLLMAN (main text); SRC_ASCE_BOLLMAN (main text)
- Claim `CLM_745` [SOURCE_VERIFIED]: SRC_ASCE_BOLLMAN (main text)
- Shot: SC_064

## B30.s1 (921.22 s): "The Bollman truss, patented in 1852, was one of the first designs to use iron in all of its essential structural parts."
- Claim `CLM_744` [SOURCE_VERIFIED]: SRC_ASCE_BOLLMAN (main text); SRC_ASCE_BOLLMAN (main text)
- Claim `CLM_745` [SOURCE_VERIFIED]: SRC_ASCE_BOLLMAN (main text)
- Shot: SC_064

## B30.s2 (931.17 s): "It could be built relatively quickly and inexpensively, while offering the long-lasting qualities of metal."
- Claim `CLM_744` [SOURCE_VERIFIED]: SRC_ASCE_BOLLMAN (main text); SRC_ASCE_BOLLMAN (main text)
- Claim `CLM_745` [SOURCE_VERIFIED]: SRC_ASCE_BOLLMAN (main text)
- Shot: SC_064

## B30.s3 (938.87 s): "The bridge at Savage, Maryland, is the only remaining example of the design."
- Claim `CLM_744` [SOURCE_VERIFIED]: SRC_ASCE_BOLLMAN (main text); SRC_ASCE_BOLLMAN (main text)
- Claim `CLM_745` [SOURCE_VERIFIED]: SRC_ASCE_BOLLMAN (main text)
- Shot: SC_064

## B31.s0 (946.02 s): "Stone for permanence, timber for speed and economy, and iron trusses that offered some of both."
- Claim `CLM_741` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6); SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Claim `CLM_742` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Claim `CLM_744` [SOURCE_VERIFIED]: SRC_ASCE_BOLLMAN (main text); SRC_ASCE_BOLLMAN (main text)
- Shot: SC_065

## B31.s1 (953.25 s): "Three places, three sets of constraints, three different bridges."
- Claim `CLM_741` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6); SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Claim `CLM_742` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Claim `CLM_744` [SOURCE_VERIFIED]: SRC_ASCE_BOLLMAN (main text); SRC_ASCE_BOLLMAN (main text)
- Shot: SC_065

## B31A.s0 (959.11 s): "Long spans forced hard decisions too."
- Claim `CLM_789` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-132); SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-133)
- Shot: SC_066
- Chú thích `B31A_note` NOTE "Illustrative model, not the Niagara bridge" → SC_066 / bridge_suspension_01 / ; 959.00–991.88 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B31A.s1 (962.71 s): "In 1855, John Roebling's suspension bridge carried trains across the Niagara Gorge, but railroad executives doubted that suspension bridges could bear heavy trains."
- Claim `CLM_789` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-132); SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-133)
- Shot: SC_066
- Chú thích `B31A_1855` NOTE "Niagara Gorge, 1855: trains on a suspension bridge" → SC_066 / bridge_suspension_01 / ; 962.62–975.75 s; claim CLM_789; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B31A.s2 (975.86 s): "Their doubts were not unjustified: the bridge needed major repairs, was declared inadequate in 1890, and it would be 133 years before another suspension bridge was built for railway traffic."
- Claim `CLM_789` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-132); SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-133)
- Shot: SC_066
- Chú thích `B31A_133` NOTE "Next railway suspension bridge: 133 years later" → SC_066 / bridge_suspension_01 / ; 975.75–991.88 s; claim CLM_789; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B31B.s0 (992.27 s): "Cantilevers, by contrast, were first used by the railroads."
- Claim `CLM_790` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-142); SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-143)
- Claim `CLM_791` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-143)
- Shot: SC_067
- Chú thích `B31B_note` NOTE "Illustrative model, not the Kentucky River bridge" → SC_067 / bridge_cantilever_truss_01 / ; 992.17–1019.38 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B31B.s1 (997.55 s): "A cantilever is inherently rigid, so if properly designed, heavy locomotives pulling trains are no threat to it."
- Claim `CLM_790` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-142); SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-143)
- Claim `CLM_791` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-143)
- Shot: SC_067
- Chú thích `B31B_rigid` NOTE "Inherently rigid: suited to heavy trains" → SC_067 / bridge_cantilever_truss_01 / ; 997.46–1006.17 s; claim CLM_790; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B31B.s2 (1006.25 s): "In 1877, one carried the Cincinnati Southern Railroad across the 275-foot-deep Kentucky River gorge: the longest cantilever in the world."
- Claim `CLM_790` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-142); SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-143)
- Claim `CLM_791` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-143)
- Shot: SC_067
- Chú thích `B31B_1877` NOTE "1877: the world's longest cantilever" → SC_067 / bridge_cantilever_truss_01 / ; 1006.17–1019.38 s; claim CLM_791; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B31C.s0 (1019.77 s): "In San Francisco, the Golden Gate Bridge opened in 1937."
- Claim `CLM_792` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-28)
- Shot: SC_068

## B31C.s1 (1026.00 s): "For 27 years, it stood as the world's longest span."
- Claim `CLM_792` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-28)
- Shot: SC_068

## B31D.s0 (1032.03 s): "Today, the long-span answer in America is usually cable-stayed."
- Claim `CLM_774` [SOURCE_VERIFIED]: SRC_FHWA_BRIDGE_TYPES (3.0 Economics)
- Claim `CLM_793` [SOURCE_VERIFIED]: SRC_FHWA_PENOBSCOT (Chapter 3, The test bridge); SRC_FHWA_PENOBSCOT (Chapter 3, The test bridge); SRC_FHWA_PENOBSCOT (Chapter 3, The test bridge); SRC_FHWA_PENOBSCOT (Chapter 3, The test bridge); SRC_FHWA_PENOBSCOT (Chapter 3, The test bridge)
- Shot: SC_069
- Chú thích `B31D_note` NOTE "Illustrative model, not the Penobscot Narrows Bridge" → SC_069 / bridge_cable_stayed_01 / ; 1031.92–1060.46 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B31D.s1 (1037.58 s): "In Maine, the Penobscot Narrows Bridge, opened in 2006, carries its 1,161-foot main span on two concrete pylons 430 feet tall."
- Claim `CLM_774` [SOURCE_VERIFIED]: SRC_FHWA_BRIDGE_TYPES (3.0 Economics)
- Claim `CLM_793` [SOURCE_VERIFIED]: SRC_FHWA_PENOBSCOT (Chapter 3, The test bridge); SRC_FHWA_PENOBSCOT (Chapter 3, The test bridge); SRC_FHWA_PENOBSCOT (Chapter 3, The test bridge); SRC_FHWA_PENOBSCOT (Chapter 3, The test bridge); SRC_FHWA_PENOBSCOT (Chapter 3, The test bridge)
- Shot: SC_069
- Chú thích `B31D_fact` NOTE "Penobscot Narrows, 2006: 430 ft concrete pylons" → SC_069 / bridge_cable_stayed_01 / ; 1037.46–1051.08 s; claim CLM_793; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B31D.s2 (1051.20 s): "It took just 42 months from conception to completion, and one of its pylons has a public observatory at the top."
- Claim `CLM_774` [SOURCE_VERIFIED]: SRC_FHWA_BRIDGE_TYPES (3.0 Economics)
- Claim `CLM_793` [SOURCE_VERIFIED]: SRC_FHWA_PENOBSCOT (Chapter 3, The test bridge); SRC_FHWA_PENOBSCOT (Chapter 3, The test bridge); SRC_FHWA_PENOBSCOT (Chapter 3, The test bridge); SRC_FHWA_PENOBSCOT (Chapter 3, The test bridge); SRC_FHWA_PENOBSCOT (Chapter 3, The test bridge)
- Shot: SC_069
- Chú thích `B31D_42` NOTE "42 months from conception to completion" → SC_069 / bridge_cable_stayed_01 / ; 1051.08–1060.46 s; claim CLM_793; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B32.s0 (1060.86 s): "So why don't bridges all look the same?"
- Claim `CLM_706` [SOURCE_VERIFIED]: SRC_FHWA_CBM (Chapter 2, 'Component Terminology'); SRC_ODOT_MBI (Glossary p.358 'girder')
- Claim `CLM_709` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Part 2 Ratings, Item 25 Arch, p.144 (manual p.2-56)); SRC_ODOT_MBI (Glossary p.339 'arch'); SRC_YALE_PHYSICS ('Arch Bridges' section)
- Claim `CLM_712` [SOURCE_VERIFIED]: SRC_SCI_TRUSSES (Introduction); SRC_FHWA_CBM (Chapter 2, 'Component Terminology')
- Shot: SC_070
- Chú thích `B32_ch` NOTE "12 · Why they look different" → SC_070 / bridge_steel_truss_pratt_01 / ; 1060.76–1069.01 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B32.s1 (1064.23 s): "Because a bridge's form comes from two things working together."
- Claim `CLM_706` [SOURCE_VERIFIED]: SRC_FHWA_CBM (Chapter 2, 'Component Terminology'); SRC_ODOT_MBI (Glossary p.358 'girder')
- Claim `CLM_709` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Part 2 Ratings, Item 25 Arch, p.144 (manual p.2-56)); SRC_ODOT_MBI (Glossary p.339 'arch'); SRC_YALE_PHYSICS ('Arch Bridges' section)
- Claim `CLM_712` [SOURCE_VERIFIED]: SRC_SCI_TRUSSES (Introduction); SRC_FHWA_CBM (Chapter 2, 'Component Terminology')
- Shot: SC_070

## B32.s2 (1069.11 s): "One is how its structure carries load: beams resist bending, arches work in compression, and trusses share load among members in tension and compression."
- Claim `CLM_706` [SOURCE_VERIFIED]: SRC_FHWA_CBM (Chapter 2, 'Component Terminology'); SRC_ODOT_MBI (Glossary p.358 'girder')
- Claim `CLM_709` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Part 2 Ratings, Item 25 Arch, p.144 (manual p.2-56)); SRC_ODOT_MBI (Glossary p.339 'arch'); SRC_YALE_PHYSICS ('Arch Bridges' section)
- Claim `CLM_712` [SOURCE_VERIFIED]: SRC_SCI_TRUSSES (Introduction); SRC_FHWA_CBM (Chapter 2, 'Component Terminology')
- Shot: SC_070
- Chú thích `B32_one` NOTE "1 · How the structure carries load" → SC_070 / bridge_steel_truss_pratt_01 / ; 1069.01–1080.92 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B32L.s0 (1081.32 s): "Cantilevers reach out from their piers, and suspension and cable-stayed bridges hang their decks from steel cables."
- Claim `CLM_750` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-142); SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-142)
- Claim `CLM_760` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-133)
- Claim `CLM_770` [SOURCE_VERIFIED]: SRC_FHWA_BRIDGE_TYPES (2.5 Cable-Stayed)
- Shot: SC_071
- Chú thích `B32L_one` NOTE "1 · How the structure carries load" → SC_071 / bridge_cable_stayed_01 / ; 1081.22–1090.04 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B32B.s0 (1090.44 s): "The other is the world it was built in: its materials, its site, its span, its budget and its builders."
- Claim `CLM_724` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.2.1 Stone Arch, p. 3-49)
- Claim `CLM_742` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Shot: SC_072

## B33.s0 (1099.11 s): "And it is not a simple story of progress."
- Claim `CLM_721` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.3.1 Timber Stringer, p. 3-80); SRC_NCHRP_CONTEXT (3.3.1 Timber Stringer, p. 3-80)
- Claim `CLM_738` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.2.1 Stone Arch, p. 3-49)
- Claim `CLM_767` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-133)
- Claim `CLM_777` [SOURCE_VERIFIED]: SRC_FHWA_BRIDGE_TYPES (3.0 Economics)
- Shot: SC_073

## B33.s1 (1102.81 s): "Timber beam bridges are still built today, and stone arches briefly returned during the Great Depression."
- Claim `CLM_721` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.3.1 Timber Stringer, p. 3-80); SRC_NCHRP_CONTEXT (3.3.1 Timber Stringer, p. 3-80)
- Claim `CLM_738` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.2.1 Stone Arch, p. 3-49)
- Claim `CLM_767` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-133)
- Claim `CLM_777` [SOURCE_VERIFIED]: SRC_FHWA_BRIDGE_TYPES (3.0 Economics)
- Shot: SC_073

## B33.s2 (1110.41 s): "And the most common steel bridge today is still a kind of beam: the welded plate girder."
- Claim `CLM_721` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.3.1 Timber Stringer, p. 3-80); SRC_NCHRP_CONTEXT (3.3.1 Timber Stringer, p. 3-80)
- Claim `CLM_738` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.2.1 Stone Arch, p. 3-49)
- Claim `CLM_767` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-133)
- Claim `CLM_777` [SOURCE_VERIFIED]: SRC_FHWA_BRIDGE_TYPES (3.0 Economics)
- Shot: SC_073

## B33.s3 (1116.76 s): "At one time, a great number of small suspension bridges were built across the country, simply because they were easy to put up."
- Claim `CLM_721` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.3.1 Timber Stringer, p. 3-80); SRC_NCHRP_CONTEXT (3.3.1 Timber Stringer, p. 3-80)
- Claim `CLM_738` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.2.1 Stone Arch, p. 3-49)
- Claim `CLM_767` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-133)
- Claim `CLM_777` [SOURCE_VERIFIED]: SRC_FHWA_BRIDGE_TYPES (3.0 Economics)
- Shot: SC_073

## B33.s4 (1126.01 s): "Each form can still be the right answer in the right place."
- Claim `CLM_721` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.3.1 Timber Stringer, p. 3-80); SRC_NCHRP_CONTEXT (3.3.1 Timber Stringer, p. 3-80)
- Claim `CLM_738` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.2.1 Stone Arch, p. 3-49)
- Claim `CLM_767` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-133)
- Claim `CLM_777` [SOURCE_VERIFIED]: SRC_FHWA_BRIDGE_TYPES (3.0 Economics)
- Shot: SC_073

## B34.s0 (1131.19 s): "Next time you cross a bridge, look at its shape."
- Không có claim (câu dẫn dắt).
- Shot: SC_074

## B34.s1 (1135.04 s): "It shows how the load reaches the ground, and something about the people who built it."
- Không có claim (câu dẫn dắt).
- Shot: SC_074

## B34.s2 (1141.22 s): "These models are illustrations, not engineering designs, and the arrows show ideas, not calculated forces."
- Không có claim (câu dẫn dắt).
- Shot: SC_074
- Chú thích `B34_note` NOTE "Models are illustrations, not engineering designs" → SC_074 / bridge_stone_arch_03 / ; 1141.12–1150.75 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B35.s0 (1151.15 s): "Thank you very much for watching."
- Không có claim (câu dẫn dắt).
- Shot: SC_075

## B35.s1 (1154.12 s): "The sources and photo credits are listed in the description."
- Không có claim (câu dẫn dắt).
- Shot: SC_075
