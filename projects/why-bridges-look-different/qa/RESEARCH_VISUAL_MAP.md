# Ánh xạ nghiên cứu → hình ảnh: why-bridges-look-different

Sinh bởi `tools/cli.py research-map` từ visual_plan.json, sources.json, timing.json và blender_checks.json. Mỗi dòng: câu → claim → nguồn (vị trí) → asset/bộ phận → chú thích → thời điểm → QA.
Claim nào cũng mới ở mức `SOURCE_VERIFIED`, **chưa được duyệt biên tập**.

## B01.s0 (0.40 s): "One bridge rests on rows of timber posts."
- Không có claim (câu dẫn dắt).
- Shot: SC_001, SC_002, SC_003, SC_004

## B01.s1 (4.65 s): "Another leaps the gap in curves of stone."
- Không có claim (câu dẫn dắt).
- Shot: SC_001, SC_002, SC_003, SC_004

## B01.s2 (8.50 s): "A third is a lattice of steel triangles."
- Không có claim (câu dẫn dắt).
- Shot: SC_001, SC_002, SC_003, SC_004

## B01.s3 (12.75 s): "All three cross exactly the same gap."
- Không có claim (câu dẫn dắt).
- Shot: SC_001, SC_002, SC_003, SC_004

## B02.s0 (17.44 s): "So why don't bridges all look the same?"
- Không có claim (câu dẫn dắt).
- Shot: SC_005

## B02.s1 (21.09 s): "It isn't because one design is simply better than the others."
- Không có claim (câu dẫn dắt).
- Shot: SC_005

## B02.s2 (26.12 s): "Each form is a different answer to the same problem, shaped by materials, by the site, and by the time it was built in."
- Không có claim (câu dẫn dắt).
- Shot: SC_005

## B03.s0 (35.73 s): "Every bridge has the same basic job."
- Claim `CLM_701` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.365 'live load'); SRC_ODOT_MBI (Glossary p.350 'dead load')
- Claim `CLM_702` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.350 'deck')
- Shot: SC_006
- Chú thích `B03_ch` NOTE "2 · The problem every bridge must solve" → SC_006 / bridge_steel_truss_pratt_01 / ; 35.62–45.54 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B03.s1 (39.58 s): "It has to carry loads: the traffic crossing it, and the weight of the bridge itself."
- Claim `CLM_701` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.365 'live load'); SRC_ODOT_MBI (Glossary p.350 'dead load')
- Claim `CLM_702` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.350 'deck')
- Shot: SC_006
- Chú thích `B03_load` LOAD_ARROW "Load" → SC_006 / bridge_steel_truss_pratt_01 / steel_truss_bridge_span1_deck, steel_truss_bridge_span2_deck; 39.50–50.75 s; claim CLM_701; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B03.s2 (45.66 s): "And it has to pass all of that down into the ground on either side."
- Claim `CLM_701` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.365 'live load'); SRC_ODOT_MBI (Glossary p.350 'dead load')
- Claim `CLM_702` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.350 'deck')
- Shot: SC_006
- Chú thích `B03_ground` COMPONENT_LABEL "Ground" → SC_006 / site_river_crossing_24 / bank_right; 45.54–50.75 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B04.s0 (51.48 s): "Engineers often describe a bridge in two parts."
- Claim `CLM_702` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.350 'deck')
- Claim `CLM_703` [SOURCE_VERIFIED]: SRC_FHWA_PBES_CH2 (Chapter 2 introduction (AASHTO definition)); SRC_FHWA_PBES_GLOSSARY (Appendix E 'superstructure')
- Claim `CLM_704` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.383 'substructure'); SRC_ODOT_MBI (Glossary p.338 'abutment'); SRC_ODOT_MBI (Glossary p.370 'pier')
- Shot: SC_007

## B04.s1 (56.06 s): "The superstructure is the part that spans the gap, including the deck."
- Claim `CLM_702` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.350 'deck')
- Claim `CLM_703` [SOURCE_VERIFIED]: SRC_FHWA_PBES_CH2 (Chapter 2 introduction (AASHTO definition)); SRC_FHWA_PBES_GLOSSARY (Appendix E 'superstructure')
- Claim `CLM_704` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.383 'substructure'); SRC_ODOT_MBI (Glossary p.338 'abutment'); SRC_ODOT_MBI (Glossary p.370 'pier')
- Shot: SC_007
- Chú thích `B04_super` HIGHLIGHT_REGION "Superstructure" → SC_007 / bridge_steel_truss_pratt_01 / steel_truss_bridge_span1_chords_north, steel_truss_bridge_span1_chords_south, steel_truss_bridge_span1_deck …; 55.96–61.62 s; claim CLM_703; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B04.s2 (61.71 s): "The substructure is what holds it up: abutments at the ends, and sometimes piers in between."
- Claim `CLM_702` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.350 'deck')
- Claim `CLM_703` [SOURCE_VERIFIED]: SRC_FHWA_PBES_CH2 (Chapter 2 introduction (AASHTO definition)); SRC_FHWA_PBES_GLOSSARY (Appendix E 'superstructure')
- Claim `CLM_704` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.383 'substructure'); SRC_ODOT_MBI (Glossary p.338 'abutment'); SRC_ODOT_MBI (Glossary p.370 'pier')
- Shot: SC_007
- Chú thích `B04_abut` COMPONENT_LABEL "Abutment" → SC_007 / bridge_steel_truss_pratt_01 / steel_truss_bridge_seat_left; 61.62–75.17 s; claim CLM_704; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS
- Chú thích `B04_pier` COMPONENT_LABEL "Pier" → SC_007 / bridge_steel_truss_pratt_01 / steel_truss_bridge_pier1; 61.62–75.17 s; claim CLM_704; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B04.s3 (68.63 s): "Load follows a path from the deck, through both parts, into the foundations."
- Claim `CLM_702` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.350 'deck')
- Claim `CLM_703` [SOURCE_VERIFIED]: SRC_FHWA_PBES_CH2 (Chapter 2 introduction (AASHTO definition)); SRC_FHWA_PBES_GLOSSARY (Appendix E 'superstructure')
- Claim `CLM_704` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.383 'substructure'); SRC_ODOT_MBI (Glossary p.338 'abutment'); SRC_ODOT_MBI (Glossary p.370 'pier')
- Shot: SC_007
- Chú thích `B04_path` CONCEPTUAL_LOAD_PATH → SC_007 / bridge_steel_truss_pratt_01 / steel_truss_bridge_pier1, steel_truss_bridge_seat_left, steel_truss_bridge_seat_right …; 68.54–75.17 s; claim CLM_704; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS
- Chú thích `B04_found` COMPONENT_LABEL "Foundation" → SC_007 / bridge_steel_truss_pratt_01 / steel_truss_bridge_seat_left; 68.54–75.17 s; claim CLM_704; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B05.s0 (75.57 s): "What changes from one bridge to the next is how that path is arranged."
- Không có claim (câu dẫn dắt).
- Shot: SC_008

## B05.s1 (81.22 s): "So let's start again with an empty gap."
- Không có claim (câu dẫn dắt).
- Shot: SC_008

## B06.s0 (85.90 s): "The first answer is the beam."
- Claim `CLM_705` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.341 'beam')
- Claim `CLM_720` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.3.1 Timber Stringer, p. 3-80)
- Shot: SC_009, SC_010
- Chú thích `B06_ch` NOTE "3 · The beam" → SC_009 / bridge_timber_beam_01 / ; 85.79–94.71 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS
- Chú thích `B06_ch` NOTE "3 · The beam" → SC_010 / bridge_timber_beam_01 / ; 95.04–99.67 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B06.s1 (89.22 s): "Lay a strong member across the gap, support it at each end, and you have a bridge."
- Claim `CLM_705` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.341 'beam')
- Claim `CLM_720` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.3.1 Timber Stringer, p. 3-80)
- Shot: SC_009, SC_010

## B06.s2 (95.22 s): "It is one of the oldest ideas in bridge building."
- Claim `CLM_705` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.341 'beam')
- Claim `CLM_720` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.3.1 Timber Stringer, p. 3-80)
- Shot: SC_009, SC_010

## B07.s0 (100.40 s): "This timber bridge is a row of short beam spans."
- Claim `CLM_705` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.341 'beam')
- Claim `CLM_707` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.344 'cap'); SRC_ODOT_MBI (Glossary p.341 'bent'); SRC_ODOT_MBI (Glossary p.346 'column')
- Shot: SC_011, SC_012

## B07.s1 (104.95 s): "Planks form the deck, long beams carry the planks, cap beams carry the beams, and posts carry the caps."
- Claim `CLM_705` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.341 'beam')
- Claim `CLM_707` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.344 'cap'); SRC_ODOT_MBI (Glossary p.341 'bent'); SRC_ODOT_MBI (Glossary p.346 'column')
- Shot: SC_011, SC_012

## B08.s0 (113.36 s): "Each beam carries its load by resisting bending."
- Claim `CLM_701` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.365 'live load'); SRC_ODOT_MBI (Glossary p.350 'dead load')
- Claim `CLM_706` [SOURCE_VERIFIED]: SRC_FHWA_CBM (Chapter 2, 'Component Terminology'); SRC_ODOT_MBI (Glossary p.358 'girder')
- Claim `CLM_707` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.344 'cap'); SRC_ODOT_MBI (Glossary p.341 'bent'); SRC_ODOT_MBI (Glossary p.346 'column')
- Shot: SC_013
- Chú thích `B08_load` LOAD_ARROW "Load" → SC_013 / bridge_timber_beam_01 / timber_beam_bridge_span3_planks; 113.25–127.75 s; claim CLM_701; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS
- Chú thích `B08_bend` CALLOUT "Beam resists bending" → SC_013 / bridge_timber_beam_01 / timber_beam_bridge_span3_stringers; 113.25–117.71 s; claim CLM_706; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B08.s1 (117.81 s): "At each support, a cap beam spreads the load onto the posts."
- Claim `CLM_706` [SOURCE_VERIFIED]: SRC_FHWA_CBM (Chapter 2, 'Component Terminology'); SRC_ODOT_MBI (Glossary p.358 'girder')
- Claim `CLM_707` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.344 'cap'); SRC_ODOT_MBI (Glossary p.341 'bent'); SRC_ODOT_MBI (Glossary p.346 'column')
- Shot: SC_013
- Chú thích `B08_path` CONCEPTUAL_LOAD_PATH → SC_013 / bridge_timber_beam_01 / timber_beam_bridge_bent3, timber_beam_bridge_bent3_cap, timber_beam_bridge_span3_planks; 117.71–127.75 s; claim CLM_707; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS
- Chú thích `B08_cap` COMPONENT_LABEL "Cap beam" → SC_013 / bridge_timber_beam_01 / timber_beam_bridge_bent3_cap; 117.71–127.75 s; claim CLM_707; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B08.s2 (122.61 s): "The posts then carry it down into the ground in compression."
- Claim `CLM_706` [SOURCE_VERIFIED]: SRC_FHWA_CBM (Chapter 2, 'Component Terminology'); SRC_ODOT_MBI (Glossary p.358 'girder')
- Claim `CLM_707` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.344 'cap'); SRC_ODOT_MBI (Glossary p.341 'bent'); SRC_ODOT_MBI (Glossary p.346 'column')
- Shot: SC_013
- Chú thích `B08_posts` CALLOUT "Posts: compression" → SC_013 / bridge_timber_beam_01 / timber_beam_bridge_bent3; 122.50–127.75 s; claim CLM_707; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B09.s0 (128.48 s): "Beams are simple, and wood was usually easy to find."
- Claim `CLM_721` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.3.1 Timber Stringer, p. 3-80); SRC_NCHRP_CONTEXT (3.3.1 Timber Stringer, p. 3-80)
- Claim `CLM_722` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2 (North Dakota, quoted), p. 2-9)
- Shot: SC_014
- Chú thích `B09_note` NOTE "Illustrative model" → SC_014 / bridge_timber_beam_01 / ; 128.38–153.42 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B09.s1 (133.41 s): "That is why timber beam bridges were still being built long after timber trusses fell out of use, and why they are still built on quiet rural roads and in parks today."
- Claim `CLM_721` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.3.1 Timber Stringer, p. 3-80); SRC_NCHRP_CONTEXT (3.3.1 Timber Stringer, p. 3-80)
- Claim `CLM_722` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2 (North Dakota, quoted), p. 2-9)
- Shot: SC_014

## B09.s2 (145.26 s): "But many early timber bridges had relatively short spans, which is why this one needs so many posts."
- Claim `CLM_721` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.3.1 Timber Stringer, p. 3-80); SRC_NCHRP_CONTEXT (3.3.1 Timber Stringer, p. 3-80)
- Claim `CLM_722` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2 (North Dakota, quoted), p. 2-9)
- Shot: SC_014

## B10.s0 (153.82 s): "A masonry arch takes a different approach."
- Claim `CLM_708` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.388 'voussoir'); SRC_ODOT_MBI (Glossary p.363 'keystone')
- Shot: SC_015, SC_016
- Chú thích `B10_ch` NOTE "4 · The arch" → SC_015 / bridge_stone_arch_03 / ; 153.71–157.42 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B10.s1 (157.62 s): "It is built from wedge-shaped stones called voussoirs, with a keystone at the crown."
- Claim `CLM_708` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.388 'voussoir'); SRC_ODOT_MBI (Glossary p.363 'keystone')
- Shot: SC_015, SC_016
- Chú thích `B10_key` COMPONENT_LABEL "Keystone" → SC_016 / bridge_stone_arch_03 / stone_arch_bridge_arch2_keystone; 158.83–162.79 s; claim CLM_708; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS
- Chú thích `B10_vous` COMPONENT_LABEL "Voussoirs" → SC_016 / bridge_stone_arch_03 / stone_arch_bridge_arch2_voussoir01; 159.00–162.62 s; claim CLM_708; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B11.s0 (164.44 s): "The curve turns the downward load into thrust along the arch, pressing the stones together."
- Claim `CLM_709` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Part 2 Ratings, Item 25 Arch, p.144 (manual p.2-56)); SRC_ODOT_MBI (Glossary p.339 'arch'); SRC_YALE_PHYSICS ('Arch Bridges' section)
- Claim `CLM_710` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.339 'arch'); SRC_YALE_PHYSICS ('Arch Bridges' section)
- Shot: SC_017
- Chú thích `B11_load` LOAD_ARROW "Load" → SC_017 / bridge_stone_arch_03 / stone_arch_bridge_arch2_keystone; 164.33–181.42 s; claim CLM_709; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS
- Chú thích `B11_thrust` CONCEPTUAL_LOAD_PATH → SC_017 / bridge_stone_arch_03 / stone_arch_bridge_arch2_keystone, stone_arch_bridge_arch2_voussoir01, stone_arch_bridge_arch2_voussoir02 …; 164.33–181.42 s; claim CLM_709; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B11.s1 (171.07 s): "So the arch works mainly in compression."
- Claim `CLM_709` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Part 2 Ratings, Item 25 Arch, p.144 (manual p.2-56)); SRC_ODOT_MBI (Glossary p.339 'arch'); SRC_YALE_PHYSICS ('Arch Bridges' section)
- Claim `CLM_710` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.339 'arch'); SRC_YALE_PHYSICS ('Arch Bridges' section)
- Shot: SC_017
- Chú thích `B11_comp` CALLOUT "Mainly compression" → SC_017 / bridge_stone_arch_03 / stone_arch_bridge_arch2_keystone, stone_arch_bridge_arch2_voussoir01, stone_arch_bridge_arch2_voussoir02 …; 170.96–181.42 s; claim CLM_709; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B11.s2 (174.89 s): "At each end it pushes outward and down on its supports, and the supports push back."
- Claim `CLM_709` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Part 2 Ratings, Item 25 Arch, p.144 (manual p.2-56)); SRC_ODOT_MBI (Glossary p.339 'arch'); SRC_YALE_PHYSICS ('Arch Bridges' section)
- Claim `CLM_710` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.339 'arch'); SRC_YALE_PHYSICS ('Arch Bridges' section)
- Shot: SC_017
- Chú thích `B11_react` REACTION_ARROW "Supports push back" → SC_017 / bridge_stone_arch_03 / stone_arch_bridge_arch2_keystone, stone_arch_bridge_arch2_voussoir01, stone_arch_bridge_arch2_voussoir02 …; 174.79–181.42 s; claim CLM_710; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B12.s0 (181.82 s): "That is why arches suit materials that are strong under compression, like stone."
- Claim `CLM_709` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Part 2 Ratings, Item 25 Arch, p.144 (manual p.2-56)); SRC_ODOT_MBI (Glossary p.339 'arch'); SRC_YALE_PHYSICS ('Arch Bridges' section)
- Claim `CLM_710` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.339 'arch'); SRC_YALE_PHYSICS ('Arch Bridges' section)
- Claim `CLM_726` [SOURCE_VERIFIED]: SRC_YALE_PHYSICS (unit 01.05.08, section 6)
- Shot: SC_018

## B12.s1 (187.77 s): "And it is why the supports matter so much: the abutments have to push inward on the arch, against its thrust."
- Claim `CLM_709` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Part 2 Ratings, Item 25 Arch, p.144 (manual p.2-56)); SRC_ODOT_MBI (Glossary p.339 'arch'); SRC_YALE_PHYSICS ('Arch Bridges' section)
- Claim `CLM_710` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.339 'arch'); SRC_YALE_PHYSICS ('Arch Bridges' section)
- Claim `CLM_726` [SOURCE_VERIFIED]: SRC_YALE_PHYSICS (unit 01.05.08, section 6)
- Shot: SC_018
- Chú thích `B12_abut` COMPONENT_LABEL "Abutment" → SC_018 / bridge_stone_arch_03 / stone_arch_bridge_abutment_left; 187.67–195.79 s; claim CLM_710; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS
- Chú thích `B12_pier` COMPONENT_LABEL "Pier" → SC_018 / bridge_stone_arch_03 / stone_arch_bridge_pier1; 187.67–195.79 s; claim CLM_710; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B13.s0 (196.19 s): "Building an arch takes support of its own."
- Claim `CLM_723` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.2.1 Stone Arch, p. 3-48)
- Shot: SC_019

## B13.s1 (199.94 s): "While a stone arch is being built, a temporary timber frame called falsework holds the stones in place."
- Claim `CLM_723` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.2.1 Stone Arch, p. 3-48)
- Shot: SC_019

## B13.s2 (207.64 s): "So building one called for carpenters as well as skilled masons."
- Claim `CLM_723` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.2.1 Stone Arch, p. 3-48)
- Shot: SC_019

## B14.s0 (213.57 s): "Stone arches were generally more expensive to build than timber bridges."
- Claim `CLM_724` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.2.1 Stone Arch, p. 3-49)
- Claim `CLM_725` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.2.1 Stone Arch, p. 3-48)
- Shot: SC_020

## B14.s1 (219.49 s): "But stone was the preferred choice where durability and permanence were required, so arches were favoured on busy routes and in important places."
- Claim `CLM_724` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.2.1 Stone Arch, p. 3-49)
- Claim `CLM_725` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.2.1 Stone Arch, p. 3-48)
- Shot: SC_020

## B14.s2 (229.94 s): "Elsewhere, the lower cost of timber made up for its lack of permanence."
- Claim `CLM_724` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.2.1 Stone Arch, p. 3-49)
- Claim `CLM_725` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.2.1 Stone Arch, p. 3-48)
- Shot: SC_020

## B15.s0 (236.07 s): "A third approach is the truss."
- Claim `CLM_711` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.386 'truss'); SRC_SCI_TRUSSES (Introduction)
- Claim `CLM_712` [SOURCE_VERIFIED]: SRC_SCI_TRUSSES (Introduction); SRC_FHWA_CBM (Chapter 2, 'Component Terminology')
- Shot: SC_021
- Chú thích `B15_ch` NOTE "5 · The truss" → SC_021 / bridge_steel_truss_pratt_01 / ; 235.96–239.17 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B15.s1 (239.27 s): "It builds a structure out of straight members, joined into triangles."
- Claim `CLM_711` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.386 'truss'); SRC_SCI_TRUSSES (Introduction)
- Claim `CLM_712` [SOURCE_VERIFIED]: SRC_SCI_TRUSSES (Introduction); SRC_FHWA_CBM (Chapter 2, 'Component Terminology')
- Shot: SC_021
- Chú thích `B15_joints` COMPONENT_LABEL "Joints" → SC_021 / bridge_steel_truss_pratt_01 / steel_truss_bridge_span1_joints_south; 239.17–251.79 s; claim CLM_711; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B15.s2 (244.59 s): "Each member is mainly pulled or pushed along its length, in tension or in compression."
- Claim `CLM_711` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.386 'truss'); SRC_SCI_TRUSSES (Introduction)
- Claim `CLM_712` [SOURCE_VERIFIED]: SRC_SCI_TRUSSES (Introduction); SRC_FHWA_CBM (Chapter 2, 'Component Terminology')
- Shot: SC_021
- Chú thích `B15_legend` TENSION_COMPRESSION_LEGEND → SC_021 / bridge_steel_truss_pratt_01 / ; 244.50–251.79 s; claim CLM_712; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B16.s0 (252.19 s): "In a simple span like these, under a downward load, the top chord is squeezed and the bottom chord is stretched."
- Claim `CLM_712` [SOURCE_VERIFIED]: SRC_SCI_TRUSSES (Introduction); SRC_FHWA_CBM (Chapter 2, 'Component Terminology')
- Claim `CLM_713` [SOURCE_VERIFIED]: SRC_FHWA_CBM (Chapter 2, 'Component Terminology'); SRC_SCI_TRUSSES ('Types of trusses')
- Claim `CLM_714` [SOURCE_VERIFIED]: SRC_FHWA_CBM (Chapter 2, 'Component Terminology')
- Shot: SC_022
- Chú thích `B16_legend` TENSION_COMPRESSION_LEGEND → SC_022 / bridge_steel_truss_pratt_01 / ; 252.08–266.25 s; claim CLM_712; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS
- Chú thích `B16_top` CALLOUT "Top chord: compression" → SC_022 / bridge_steel_truss_pratt_01 / steel_truss_bridge_span1_chords_south; 256.04–266.25 s; claim CLM_713; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS
- Chú thích `B16_bottom` CALLOUT "Bottom chord: tension" → SC_022 / bridge_steel_truss_pratt_01 / steel_truss_bridge_span1_chords_south; 257.67–266.25 s; claim CLM_713; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B16.s1 (260.07 s): "Inside, some web members are in compression and others are in tension."
- Claim `CLM_713` [SOURCE_VERIFIED]: SRC_FHWA_CBM (Chapter 2, 'Component Terminology'); SRC_SCI_TRUSSES ('Types of trusses')
- Claim `CLM_714` [SOURCE_VERIFIED]: SRC_FHWA_CBM (Chapter 2, 'Component Terminology')
- Shot: SC_022
- Chú thích `B16_web` COMPONENT_LABEL "Web members" → SC_022 / bridge_steel_truss_pratt_01 / steel_truss_bridge_span2_diagonals_south; 259.96–266.25 s; claim CLM_714; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B17.s0 (266.65 s): "The triangles can be arranged in different patterns."
- Claim `CLM_711` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.386 'truss'); SRC_SCI_TRUSSES (Introduction)
- Claim `CLM_727` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-7)
- Claim `CLM_728` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-7)
- Shot: SC_023, SC_024, SC_025

## B17.s1 (271.02 s): "This is a Pratt truss."
- Claim `CLM_711` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.386 'truss'); SRC_SCI_TRUSSES (Introduction)
- Claim `CLM_727` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-7)
- Claim `CLM_728` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-7)
- Shot: SC_023, SC_024, SC_025
- Chú thích `B17_pratt` NOTE "Pratt truss (patented 1844)" → SC_023 / bridge_steel_truss_pratt_01 / ; 270.92–282.12 s; claim CLM_727; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B17.s2 (273.65 s): "In the original design, patented in 1844, its verticals were timber and its diagonals were iron rods."
- Claim `CLM_711` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.386 'truss'); SRC_SCI_TRUSSES (Introduction)
- Claim `CLM_727` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-7)
- Claim `CLM_728` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-7)
- Shot: SC_023, SC_024, SC_025

## B17.s3 (282.62 s): "Swap the web for diagonals that alternate in direction, and you have a Warren truss, patented in 1848."
- Claim `CLM_711` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.386 'truss'); SRC_SCI_TRUSSES (Introduction)
- Claim `CLM_727` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-7)
- Claim `CLM_728` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-7)
- Shot: SC_023, SC_024, SC_025
- Chú thích `B17_warren` NOTE "Warren truss (patented 1848)" → SC_024 / bridge_steel_truss_warren_01 / ; 282.54–290.42 s; claim CLM_728; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS
- Chú thích `B17_warren` NOTE "Warren truss (patented 1848)" → SC_025 / bridge_steel_truss_warren_01 / ; 290.75–297.71 s; claim CLM_728; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B17.s4 (290.95 s): "Both patterns carry load through triangles; they simply arrange the members differently."
- Claim `CLM_711` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.386 'truss'); SRC_SCI_TRUSSES (Introduction)
- Claim `CLM_727` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-7)
- Claim `CLM_728` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-7)
- Shot: SC_023, SC_024, SC_025

## B18.s0 (298.11 s): "Trusses also changed how bridges were built."
- Claim `CLM_729` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2 'Foundries and Fabricators', p. 2-11)
- Shot: SC_026

## B18.s1 (302.21 s): "By the middle of the nineteenth century, shops were making and drilling truss members, then shipping them to the bridge site, ready to assemble."
- Claim `CLM_729` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2 'Foundries and Fabricators', p. 2-11)
- Shot: SC_026
- Chú thích `B18_shop` NOTE "Members made and drilled in shops" → SC_026 / bridge_steel_truss_pratt_01 / ; 302.12–311.29 s; claim CLM_729; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B18.s2 (311.38 s): "And by 1860, the railroads relied almost entirely on these prefabricated parts."
- Claim `CLM_729` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2 'Foundries and Fabricators', p. 2-11)
- Shot: SC_026
- Chú thích `B18_1860` NOTE "By 1860: prefabricated parts" → SC_026 / bridge_steel_truss_pratt_01 / ; 311.29–319.33 s; claim CLM_729; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B19.s0 (319.73 s): "So which design is best?"
- Không có claim (câu dẫn dắt).
- Shot: SC_027

## B19.s1 (322.68 s): "The honest answer is that it depends."
- Không có claim (câu dẫn dắt).
- Shot: SC_027

## B19.s2 (326.41 s): "Materials, the site, the span, cost, and the skills available all pull in different directions."
- Không có claim (câu dẫn dắt).
- Shot: SC_027

## B20A.s0 (334.61 s): "Start with the materials themselves."
- Claim `CLM_726` [SOURCE_VERIFIED]: SRC_YALE_PHYSICS (unit 01.05.08, section 6)
- Shot: SC_028

## B20A.s1 (338.03 s): "An arch needs a material that is strong under compression, and stone is."
- Claim `CLM_726` [SOURCE_VERIFIED]: SRC_YALE_PHYSICS (unit 01.05.08, section 6)
- Shot: SC_028
- Chú thích `B20A_note` NOTE "Stone: strong under compression" → SC_028 / bridge_stone_arch_03 / ; 337.92–344.12 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B20B.s0 (344.52 s): "A truss needs members that can work in tension as well as compression."
- Claim `CLM_712` [SOURCE_VERIFIED]: SRC_SCI_TRUSSES (Introduction); SRC_FHWA_CBM (Chapter 2, 'Component Terminology')
- Claim `CLM_735` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-8)
- Shot: SC_029
- Chú thích `B20B_note` NOTE "Truss members: tension and compression" → SC_029 / bridge_steel_truss_pratt_01 / ; 344.42–350.21 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B20B.s1 (350.30 s): "Wrought iron was valued for exactly that: one historian calls it a material strong equally in tension and in compression."
- Claim `CLM_712` [SOURCE_VERIFIED]: SRC_SCI_TRUSSES (Introduction); SRC_FHWA_CBM (Chapter 2, 'Component Terminology')
- Claim `CLM_735` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-8)
- Shot: SC_029
- Chú thích `B20B_iron` NOTE "Wrought iron: valued in tension and compression" → SC_029 / bridge_steel_truss_pratt_01 / ; 350.21–359.92 s; claim CLM_735; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B20C.s0 (360.32 s): "Wood was often plentiful and cheap, but wooden bridges were vulnerable to decay."
- Claim `CLM_734` [SOURCE_VERIFIED]: SRC_ASCE_BOLLMAN (main text)
- Claim `CLM_742` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Shot: SC_030
- Chú thích `B20C_note` NOTE "Timber: plentiful and cheap, but it decays" → SC_030 / bridge_timber_beam_01 / ; 360.21–367.12 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B21.s0 (367.52 s): "That is one reason many timber truss bridges were covered with a roof and siding, to protect them from the weather."
- Claim `CLM_733` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.1.1 King Post, p. 3-7)
- Claim `CLM_746` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (List of figures, 3-5)
- Shot: SC_031

## B21.s1 (375.57 s): "This is the Humpback Covered Bridge, built in 1857 over Dunlap Creek."
- Claim `CLM_733` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.1.1 King Post, p. 3-7)
- Claim `CLM_746` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (List of figures, 3-5)
- Shot: SC_031

## B22.s0 (383.07 s): "The site of a bridge matters too."
- Claim `CLM_736` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.6 Trestles and Viaducts, p. 3-137); SRC_NCHRP_CONTEXT (3.6 Trestles and Viaducts, p. 3-137)
- Shot: SC_032

## B22.s1 (386.47 s): "Railway engines have limited traction, so railways need gentle gradients."
- Claim `CLM_736` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.6 Trestles and Viaducts, p. 3-137); SRC_NCHRP_CONTEXT (3.6 Trestles and Viaducts, p. 3-137)
- Shot: SC_032

## B22.s2 (392.54 s): "Where a valley was too deep and wide to fill with an embankment, engineers built viaducts and trestles to keep the line nearly straight and level."
- Claim `CLM_736` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.6 Trestles and Viaducts, p. 3-137); SRC_NCHRP_CONTEXT (3.6 Trestles and Viaducts, p. 3-137)
- Shot: SC_032

## B23.s0 (403.52 s): "Then there is span: how far a single structure has to reach."
- Không có claim (câu dẫn dắt).
- Shot: SC_033
- Chú thích `B23_note` NOTE "Span: how far one structure reaches" → SC_033 / None / ; 403.42–408.58 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B23B.s0 (408.98 s): "A simple king post truss could span only about thirty feet."
- Claim `CLM_730` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.1 Trusses, p. 3-4)
- Claim `CLM_731` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.1.1 King Post, p. 3-7)
- Claim `CLM_732` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.2.1 Stone Arch, p. 3-48)
- Shot: SC_034

## B23B.s1 (414.11 s): "What one report calls America's greatest stone arch, the Cabin John Aqueduct Bridge, spans 220 feet, and some through trusses approach 400."
- Claim `CLM_730` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.1 Trusses, p. 3-4)
- Claim `CLM_731` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.1.1 King Post, p. 3-7)
- Claim `CLM_732` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.2.1 Stone Arch, p. 3-48)
- Shot: SC_034

## B24.s0 (426.44 s): "Finally, every bridge belongs to its time."
- Claim `CLM_727` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-7)
- Claim `CLM_728` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-7)
- Claim `CLM_729` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2 'Foundries and Fabricators', p. 2-11)
- Claim `CLM_738` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.2.1 Stone Arch, p. 3-49)
- Claim `CLM_739` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Shot: SC_035

## B24.s1 (430.32 s): "As metal trusses spread, skilled masons became fewer and reinforced concrete arrived, stone arch construction declined."
- Claim `CLM_727` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-7)
- Claim `CLM_728` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-7)
- Claim `CLM_729` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2 'Foundries and Fabricators', p. 2-11)
- Claim `CLM_738` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.2.1 Stone Arch, p. 3-49)
- Claim `CLM_739` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Shot: SC_035

## B24.s2 (439.69 s): "Then, during the Great Depression, it briefly returned."
- Claim `CLM_727` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-7)
- Claim `CLM_728` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-7)
- Claim `CLM_729` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2 'Foundries and Fabricators', p. 2-11)
- Claim `CLM_738` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.2.1 Stone Arch, p. 3-49)
- Claim `CLM_739` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Shot: SC_035

## B25.s0 (445.02 s): "These trade-offs played out across nineteenth-century America as the railways spread."
- Claim `CLM_741` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6); SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Claim `CLM_742` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Shot: SC_036

## B25.s1 (451.38 s): "In the East, railroads built massive stone viaducts, while western builders generally used timber."
- Claim `CLM_741` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6); SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Claim `CLM_742` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Shot: SC_036

## B25.s2 (458.90 s): "Three documented examples show how differently builders answered."
- Claim `CLM_741` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6); SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Claim `CLM_742` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Shot: SC_036

## B26.s0 (465.02 s): "Near Baltimore, the Carrollton Viaduct was completed in 1829."
- Claim `CLM_739` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Claim `CLM_740` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.6 Trestles and Viaducts, p. 3-137)
- Shot: SC_037

## B26.s1 (471.27 s): "Built of roughly twelve thousand granite blocks, it carries the railway over Gwynns Falls on an eighty foot arch."
- Claim `CLM_739` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Claim `CLM_740` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.6 Trestles and Viaducts, p. 3-137)
- Shot: SC_037

## B26.s2 (479.52 s): "A national report in 2005 called it the world's oldest stone railroad span still in service."
- Claim `CLM_739` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Claim `CLM_740` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.6 Trestles and Viaducts, p. 3-137)
- Shot: SC_037

## B27.s0 (488.32 s): "Early railroads needed durable bridges to carry heavy trains."
- Claim `CLM_725` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.2.1 Stone Arch, p. 3-48)
- Claim `CLM_741` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6); SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Shot: SC_038
- Chú thích `B27_note` NOTE "Illustrative model, not the Carrollton Viaduct" → SC_038 / bridge_stone_arch_03 / ; 488.21–498.42 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B27.s1 (493.89 s): "For a line meant to last, stone was the answer."
- Claim `CLM_725` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.2.1 Stone Arch, p. 3-48)
- Claim `CLM_741` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6); SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Shot: SC_038

## B28.s0 (498.82 s): "In the West, the pressure was different."
- Claim `CLM_742` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Claim `CLM_743` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (List of figures, 3-106)
- Shot: SC_039

## B28.s1 (502.14 s): "Railroads had to open new lines quickly and economically, and timber was abundant and cheap."
- Claim `CLM_742` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Claim `CLM_743` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (List of figures, 3-106)
- Shot: SC_039

## B28.s2 (509.14 s): "This timber trestle near Corinne, Utah, was built in 1872 by the Central Pacific Railroad."
- Claim `CLM_742` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Claim `CLM_743` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (List of figures, 3-106)
- Shot: SC_039

## B29.s0 (518.36 s): "A trestle is a succession of towers supporting short spans."
- Claim `CLM_737` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.6 Trestles and Viaducts, p. 3-137)
- Shot: SC_040
- Chú thích `B29_note` NOTE "Illustrative model, not the Promontory trestle" → SC_040 / bridge_timber_beam_01 / ; 518.25–531.04 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B29.s1 (523.61 s): "It is the same beam idea as our timber model, repeated as often as the crossing needs."
- Claim `CLM_737` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.6 Trestles and Viaducts, p. 3-137)
- Shot: SC_040

## B30.s0 (531.44 s): "Iron offered a third path."
- Claim `CLM_744` [SOURCE_VERIFIED]: SRC_ASCE_BOLLMAN (main text); SRC_ASCE_BOLLMAN (main text)
- Claim `CLM_745` [SOURCE_VERIFIED]: SRC_ASCE_BOLLMAN (main text)
- Shot: SC_041

## B30.s1 (534.54 s): "The Bollman truss, patented in 1852, was one of the first designs to use iron in all of its essential structural parts."
- Claim `CLM_744` [SOURCE_VERIFIED]: SRC_ASCE_BOLLMAN (main text); SRC_ASCE_BOLLMAN (main text)
- Claim `CLM_745` [SOURCE_VERIFIED]: SRC_ASCE_BOLLMAN (main text)
- Shot: SC_041

## B30.s2 (544.27 s): "It could be built relatively quickly and inexpensively, while offering the long-lasting qualities of metal."
- Claim `CLM_744` [SOURCE_VERIFIED]: SRC_ASCE_BOLLMAN (main text); SRC_ASCE_BOLLMAN (main text)
- Claim `CLM_745` [SOURCE_VERIFIED]: SRC_ASCE_BOLLMAN (main text)
- Shot: SC_041

## B30.s3 (551.92 s): "The bridge at Savage, Maryland, is the only remaining example of the design."
- Claim `CLM_744` [SOURCE_VERIFIED]: SRC_ASCE_BOLLMAN (main text); SRC_ASCE_BOLLMAN (main text)
- Claim `CLM_745` [SOURCE_VERIFIED]: SRC_ASCE_BOLLMAN (main text)
- Shot: SC_041

## B31.s0 (558.90 s): "Stone for permanence, timber for speed and economy, and iron trusses that offered some of both."
- Claim `CLM_741` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6); SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Claim `CLM_742` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Claim `CLM_744` [SOURCE_VERIFIED]: SRC_ASCE_BOLLMAN (main text); SRC_ASCE_BOLLMAN (main text)
- Shot: SC_042

## B31.s1 (565.80 s): "Three places, three sets of constraints, three different bridges."
- Claim `CLM_741` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6); SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Claim `CLM_742` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Claim `CLM_744` [SOURCE_VERIFIED]: SRC_ASCE_BOLLMAN (main text); SRC_ASCE_BOLLMAN (main text)
- Shot: SC_042

## B32.s0 (571.73 s): "So why don't bridges all look the same?"
- Claim `CLM_706` [SOURCE_VERIFIED]: SRC_FHWA_CBM (Chapter 2, 'Component Terminology'); SRC_ODOT_MBI (Glossary p.358 'girder')
- Claim `CLM_709` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Part 2 Ratings, Item 25 Arch, p.144 (manual p.2-56)); SRC_ODOT_MBI (Glossary p.339 'arch'); SRC_YALE_PHYSICS ('Arch Bridges' section)
- Claim `CLM_712` [SOURCE_VERIFIED]: SRC_SCI_TRUSSES (Introduction); SRC_FHWA_CBM (Chapter 2, 'Component Terminology')
- Shot: SC_043
- Chú thích `B32_ch` NOTE "8 · Why they look different" → SC_043 / bridge_steel_truss_pratt_01 / ; 571.63–580.23 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B32.s1 (575.38 s): "Because a bridge's form comes from two things working together."
- Claim `CLM_706` [SOURCE_VERIFIED]: SRC_FHWA_CBM (Chapter 2, 'Component Terminology'); SRC_ODOT_MBI (Glossary p.358 'girder')
- Claim `CLM_709` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Part 2 Ratings, Item 25 Arch, p.144 (manual p.2-56)); SRC_ODOT_MBI (Glossary p.339 'arch'); SRC_YALE_PHYSICS ('Arch Bridges' section)
- Claim `CLM_712` [SOURCE_VERIFIED]: SRC_SCI_TRUSSES (Introduction); SRC_FHWA_CBM (Chapter 2, 'Component Terminology')
- Shot: SC_043

## B32.s2 (580.33 s): "One is how its structure carries load: beams resist bending, arches work in compression, and trusses share load among members in tension and compression."
- Claim `CLM_706` [SOURCE_VERIFIED]: SRC_FHWA_CBM (Chapter 2, 'Component Terminology'); SRC_ODOT_MBI (Glossary p.358 'girder')
- Claim `CLM_709` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Part 2 Ratings, Item 25 Arch, p.144 (manual p.2-56)); SRC_ODOT_MBI (Glossary p.339 'arch'); SRC_YALE_PHYSICS ('Arch Bridges' section)
- Claim `CLM_712` [SOURCE_VERIFIED]: SRC_SCI_TRUSSES (Introduction); SRC_FHWA_CBM (Chapter 2, 'Component Terminology')
- Shot: SC_043
- Chú thích `B32_one` NOTE "1 · How the structure carries load" → SC_043 / bridge_steel_truss_pratt_01 / ; 580.23–591.75 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B32B.s0 (592.15 s): "The other is the world it was built in: its materials, its site, its span, its budget and its builders."
- Claim `CLM_724` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.2.1 Stone Arch, p. 3-49)
- Claim `CLM_742` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Shot: SC_044

## B33.s0 (600.77 s): "And it is not a simple story of progress."
- Claim `CLM_721` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.3.1 Timber Stringer, p. 3-80); SRC_NCHRP_CONTEXT (3.3.1 Timber Stringer, p. 3-80)
- Claim `CLM_738` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.2.1 Stone Arch, p. 3-49)
- Shot: SC_045

## B33.s1 (604.62 s): "Timber beam bridges are still built today, and stone arches briefly returned during the Great Depression."
- Claim `CLM_721` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.3.1 Timber Stringer, p. 3-80); SRC_NCHRP_CONTEXT (3.3.1 Timber Stringer, p. 3-80)
- Claim `CLM_738` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.2.1 Stone Arch, p. 3-49)
- Shot: SC_045

## B33.s2 (612.40 s): "Each form can still be the right answer in the right place."
- Claim `CLM_721` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.3.1 Timber Stringer, p. 3-80); SRC_NCHRP_CONTEXT (3.3.1 Timber Stringer, p. 3-80)
- Claim `CLM_738` [SOURCE_VERIFIED]: SRC_NCHRP_CONTEXT (3.2.1 Stone Arch, p. 3-49)
- Shot: SC_045

## B34.s0 (617.94 s): "Next time you cross a bridge, look at its shape."
- Không có claim (câu dẫn dắt).
- Shot: SC_046

## B34.s1 (621.94 s): "It shows how the load reaches the ground, and something about the people who built it."
- Không có claim (câu dẫn dắt).
- Shot: SC_046

## B34.s2 (628.09 s): "These models are illustrations, not engineering designs, and the arrows show ideas, not calculated forces."
- Không có claim (câu dẫn dắt).
- Shot: SC_046
- Chú thích `B34_note` NOTE "Models are illustrations, not engineering designs" → SC_046 / bridge_stone_arch_03 / ; 628.00–637.25 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B35.s0 (637.65 s): "Thank you very much for watching."
- Không có claim (câu dẫn dắt).
- Shot: SC_047

## B35.s1 (640.88 s): "The sources and photo credits are listed in the description."
- Không có claim (câu dẫn dắt).
- Shot: SC_047
