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
- Claim `CLM_701` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Glossary p.365 'live load'); SRC_ODOT_MBI (Glossary p.350 'dead load')
- Claim `CLM_702` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Glossary p.350 'deck')
- Shot: SC_009
- Chú thích `B03_ch` NOTE "2 · The problem every bridge must solve" → SC_009 / bridge_steel_truss_pratt_01 / ; 52.62–62.46 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B03.s1 (56.38 s): "It has to carry loads: the traffic crossing it, and the weight of the bridge itself."
- Claim `CLM_701` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Glossary p.365 'live load'); SRC_ODOT_MBI (Glossary p.350 'dead load')
- Claim `CLM_702` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Glossary p.350 'deck')
- Shot: SC_009
- Chú thích `B03_load` LOAD_ARROW "Load" → SC_009 / bridge_steel_truss_pratt_01 / steel_truss_bridge_span1_deck, steel_truss_bridge_span2_deck; 56.29–67.71 s; claim CLM_701; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B03.s2 (62.56 s): "And it has to pass all of that down through its supports into the ground."
- Claim `CLM_701` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Glossary p.365 'live load'); SRC_ODOT_MBI (Glossary p.350 'dead load')
- Claim `CLM_702` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Glossary p.350 'deck')
- Shot: SC_009
- Chú thích `B03_ground` COMPONENT_LABEL "Ground" → SC_009 / site_river_crossing_24 / bank_right; 62.46–67.71 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B04.s0 (68.44 s): "Engineers often describe a bridge in two parts."
- Claim `CLM_702` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Glossary p.350 'deck')
- Claim `CLM_703` [EDITORIALLY_APPROVED]: SRC_FHWA_PBES_CH2 (Chapter 2 introduction (AASHTO definition)); SRC_FHWA_PBES_GLOSSARY (Appendix E 'superstructure')
- Claim `CLM_704` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Glossary p.383 'substructure'); SRC_ODOT_MBI (Glossary p.338 'abutment'); SRC_ODOT_MBI (Glossary p.370 'pier')
- Shot: SC_010

## B04.s1 (72.69 s): "The superstructure is the part that spans the gap, including the deck."
- Claim `CLM_702` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Glossary p.350 'deck')
- Claim `CLM_703` [EDITORIALLY_APPROVED]: SRC_FHWA_PBES_CH2 (Chapter 2 introduction (AASHTO definition)); SRC_FHWA_PBES_GLOSSARY (Appendix E 'superstructure')
- Claim `CLM_704` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Glossary p.383 'substructure'); SRC_ODOT_MBI (Glossary p.338 'abutment'); SRC_ODOT_MBI (Glossary p.370 'pier')
- Shot: SC_010
- Chú thích `B04_super` HIGHLIGHT_REGION "Superstructure" → SC_010 / bridge_steel_truss_pratt_01 / steel_truss_bridge_span1_chords_north, steel_truss_bridge_span1_chords_south, steel_truss_bridge_span1_deck …; 72.58–78.00 s; claim CLM_703; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B04.s2 (78.12 s): "The substructure is what holds it up: abutments at the ends, and sometimes piers in between."
- Claim `CLM_702` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Glossary p.350 'deck')
- Claim `CLM_703` [EDITORIALLY_APPROVED]: SRC_FHWA_PBES_CH2 (Chapter 2 introduction (AASHTO definition)); SRC_FHWA_PBES_GLOSSARY (Appendix E 'superstructure')
- Claim `CLM_704` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Glossary p.383 'substructure'); SRC_ODOT_MBI (Glossary p.338 'abutment'); SRC_ODOT_MBI (Glossary p.370 'pier')
- Shot: SC_010
- Chú thích `B04_abut` COMPONENT_LABEL "Abutment" → SC_010 / bridge_steel_truss_pratt_01 / steel_truss_bridge_seat_left; 78.00–91.54 s; claim CLM_704; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS
- Chú thích `B04_pier` COMPONENT_LABEL "Pier" → SC_010 / bridge_steel_truss_pratt_01 / steel_truss_bridge_pier1; 78.00–91.54 s; claim CLM_704; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B04.s3 (85.29 s): "Load follows a path from the deck, through both parts, into the foundations."
- Claim `CLM_702` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Glossary p.350 'deck')
- Claim `CLM_703` [EDITORIALLY_APPROVED]: SRC_FHWA_PBES_CH2 (Chapter 2 introduction (AASHTO definition)); SRC_FHWA_PBES_GLOSSARY (Appendix E 'superstructure')
- Claim `CLM_704` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Glossary p.383 'substructure'); SRC_ODOT_MBI (Glossary p.338 'abutment'); SRC_ODOT_MBI (Glossary p.370 'pier')
- Shot: SC_010
- Chú thích `B04_path` CONCEPTUAL_LOAD_PATH → SC_010 / bridge_steel_truss_pratt_01 / steel_truss_bridge_pier1, steel_truss_bridge_seat_left, steel_truss_bridge_seat_right …; 85.21–91.54 s; claim CLM_704; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS
- Chú thích `B04_found` COMPONENT_LABEL "Foundation" → SC_010 / bridge_steel_truss_pratt_01 / steel_truss_bridge_seat_left; 85.21–91.54 s; claim CLM_704; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B05.s0 (91.94 s): "What changes from one bridge to the next is how that path is arranged."
- Không có claim (câu dẫn dắt).
- Shot: SC_011

## B05.s1 (97.12 s): "So let's start again with an empty gap."
- Không có claim (câu dẫn dắt).
- Shot: SC_011

## B06.s0 (101.40 s): "The first answer is the beam."
- Claim `CLM_705` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Glossary p.341 'beam')
- Claim `CLM_720` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.3.1 Timber Stringer, p. 3-80)
- Shot: SC_012, SC_013
- Chú thích `B06_ch` NOTE "3 · The beam" → SC_012 / bridge_timber_beam_01 / ; 101.29–110.04 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS
- Chú thích `B06_ch` NOTE "3 · The beam" → SC_013 / bridge_timber_beam_01 / ; 110.38–114.79 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B06.s1 (104.40 s): "Lay a strong member across the gap, support it at each end, and you have a bridge."
- Claim `CLM_705` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Glossary p.341 'beam')
- Claim `CLM_720` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.3.1 Timber Stringer, p. 3-80)
- Shot: SC_012, SC_013

## B06.s2 (110.58 s): "It is one of the oldest ideas in bridge building."
- Claim `CLM_705` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Glossary p.341 'beam')
- Claim `CLM_720` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.3.1 Timber Stringer, p. 3-80)
- Shot: SC_012, SC_013

## B07.s0 (115.53 s): "This timber bridge is a row of short beam spans."
- Claim `CLM_705` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Glossary p.341 'beam')
- Claim `CLM_707` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Glossary p.344 'cap'); SRC_ODOT_MBI (Glossary p.341 'bent'); SRC_ODOT_MBI (Glossary p.346 'column')
- Shot: SC_014, SC_015

## B07.s1 (119.75 s): "Planks form the deck, long beams carry the planks, cap beams carry the beams, and posts carry the caps."
- Claim `CLM_705` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Glossary p.341 'beam')
- Claim `CLM_707` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Glossary p.344 'cap'); SRC_ODOT_MBI (Glossary p.341 'bent'); SRC_ODOT_MBI (Glossary p.346 'column')
- Shot: SC_014, SC_015

## B08.s0 (128.28 s): "Each beam carries its load by resisting bending."
- Claim `CLM_701` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Glossary p.365 'live load'); SRC_ODOT_MBI (Glossary p.350 'dead load')
- Claim `CLM_706` [EDITORIALLY_APPROVED]: SRC_FHWA_CBM (Chapter 2, 'Component Terminology'); SRC_ODOT_MBI (Glossary p.358 'girder')
- Claim `CLM_707` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Glossary p.344 'cap'); SRC_ODOT_MBI (Glossary p.341 'bent'); SRC_ODOT_MBI (Glossary p.346 'column')
- Shot: SC_016
- Chú thích `B08_load` LOAD_ARROW "Load" → SC_016 / bridge_timber_beam_01 / timber_beam_bridge_span3_planks; 128.17–142.46 s; claim CLM_701; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS
- Chú thích `B08_bend` CALLOUT "Beam resists bending" → SC_016 / bridge_timber_beam_01 / timber_beam_bridge_span3_stringers; 128.17–132.46 s; claim CLM_706; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B08.s1 (132.55 s): "At each support, a cap beam spreads the load onto the posts."
- Claim `CLM_706` [EDITORIALLY_APPROVED]: SRC_FHWA_CBM (Chapter 2, 'Component Terminology'); SRC_ODOT_MBI (Glossary p.358 'girder')
- Claim `CLM_707` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Glossary p.344 'cap'); SRC_ODOT_MBI (Glossary p.341 'bent'); SRC_ODOT_MBI (Glossary p.346 'column')
- Shot: SC_016
- Chú thích `B08_path` CONCEPTUAL_LOAD_PATH → SC_016 / bridge_timber_beam_01 / timber_beam_bridge_bent3, timber_beam_bridge_bent3_cap, timber_beam_bridge_span3_planks; 132.46–142.46 s; claim CLM_707; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS
- Chú thích `B08_cap` COMPONENT_LABEL "Cap beam" → SC_016 / bridge_timber_beam_01 / timber_beam_bridge_bent3_cap; 132.46–142.46 s; claim CLM_707; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B08.s2 (137.47 s): "The posts then carry it down into the ground in compression."
- Claim `CLM_706` [EDITORIALLY_APPROVED]: SRC_FHWA_CBM (Chapter 2, 'Component Terminology'); SRC_ODOT_MBI (Glossary p.358 'girder')
- Claim `CLM_707` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Glossary p.344 'cap'); SRC_ODOT_MBI (Glossary p.341 'bent'); SRC_ODOT_MBI (Glossary p.346 'column')
- Shot: SC_016
- Chú thích `B08_posts` CALLOUT "Posts: compression" → SC_016 / bridge_timber_beam_01 / timber_beam_bridge_bent3; 137.38–142.46 s; claim CLM_707; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B09.s0 (143.19 s): "Beams are simple, and wood was usually easy to find."
- Claim `CLM_721` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.3.1 Timber Stringer, p. 3-80); SRC_NCHRP_CONTEXT (3.3.1 Timber Stringer, p. 3-80)
- Claim `CLM_722` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2 (North Dakota, quoted), p. 2-9)
- Shot: SC_017
- Chú thích `B09_note` NOTE "Illustrative model" → SC_017 / bridge_timber_beam_01 / ; 143.08–170.79 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B09.s1 (148.12 s): "That is why timber beam bridges were still being built long after timber trusses stopped being competitive, and in 2005 a national report found them still being built on quiet rural roads and in parks."
- Claim `CLM_721` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.3.1 Timber Stringer, p. 3-80); SRC_NCHRP_CONTEXT (3.3.1 Timber Stringer, p. 3-80)
- Claim `CLM_722` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2 (North Dakota, quoted), p. 2-9)
- Shot: SC_017

## B09.s2 (162.62 s): "But many early timber bridges had relatively short spans, which is why this one needs so many posts."
- Claim `CLM_721` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.3.1 Timber Stringer, p. 3-80); SRC_NCHRP_CONTEXT (3.3.1 Timber Stringer, p. 3-80)
- Claim `CLM_722` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2 (North Dakota, quoted), p. 2-9)
- Shot: SC_017

## B10.s0 (171.19 s): "A masonry arch takes a different approach."
- Claim `CLM_708` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Glossary p.388 'voussoir'); SRC_ODOT_MBI (Glossary p.363 'keystone')
- Shot: SC_018, SC_019
- Chú thích `B10_ch` NOTE "4 · The arch" → SC_018 / bridge_stone_arch_03 / ; 171.08–174.58 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B10.s1 (174.77 s): "It is built from wedge-shaped stones called voussoirs, with a keystone at the crown."
- Claim `CLM_708` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Glossary p.388 'voussoir'); SRC_ODOT_MBI (Glossary p.363 'keystone')
- Shot: SC_018, SC_019
- Chú thích `B10_key` COMPONENT_LABEL "Keystone" → SC_019 / bridge_stone_arch_03 / stone_arch_bridge_arch2_keystone; 176.00–180.12 s; claim CLM_708; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS
- Chú thích `B10_vous` COMPONENT_LABEL "Voussoirs" → SC_019 / bridge_stone_arch_03 / stone_arch_bridge_arch2_voussoir01; 176.17–179.96 s; claim CLM_708; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B11.s0 (181.78 s): "The curve turns the downward load into thrust along the arch, pressing the stones together."
- Claim `CLM_709` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Part 2 Ratings, Item 25 Arch, p.144 (manual p.2-56)); SRC_ODOT_MBI (Glossary p.339 'arch'); SRC_YALE_PHYSICS ('Arch Bridges' section)
- Claim `CLM_710` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Glossary p.339 'arch'); SRC_YALE_PHYSICS ('Arch Bridges' section)
- Shot: SC_020
- Chú thích `B11_load` LOAD_ARROW "Load" → SC_020 / bridge_stone_arch_03 / stone_arch_bridge_arch2_keystone; 181.67–198.62 s; claim CLM_709; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS
- Chú thích `B11_thrust` CONCEPTUAL_LOAD_PATH → SC_020 / bridge_stone_arch_03 / stone_arch_bridge_arch2_keystone, stone_arch_bridge_arch2_voussoir01, stone_arch_bridge_arch2_voussoir02 …; 181.67–198.62 s; claim CLM_709; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B11.s1 (188.47 s): "So the arch works mainly in compression."
- Claim `CLM_709` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Part 2 Ratings, Item 25 Arch, p.144 (manual p.2-56)); SRC_ODOT_MBI (Glossary p.339 'arch'); SRC_YALE_PHYSICS ('Arch Bridges' section)
- Claim `CLM_710` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Glossary p.339 'arch'); SRC_YALE_PHYSICS ('Arch Bridges' section)
- Shot: SC_020
- Chú thích `B11_comp` CALLOUT "Mainly compression" → SC_020 / bridge_stone_arch_03 / stone_arch_bridge_arch2_keystone, stone_arch_bridge_arch2_voussoir01, stone_arch_bridge_arch2_voussoir02 …; 188.38–198.62 s; claim CLM_709; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B11.s2 (192.10 s): "At each end it pushes outward and down on its supports, and the supports push back."
- Claim `CLM_709` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Part 2 Ratings, Item 25 Arch, p.144 (manual p.2-56)); SRC_ODOT_MBI (Glossary p.339 'arch'); SRC_YALE_PHYSICS ('Arch Bridges' section)
- Claim `CLM_710` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Glossary p.339 'arch'); SRC_YALE_PHYSICS ('Arch Bridges' section)
- Shot: SC_020
- Chú thích `B11_react` REACTION_ARROW "Supports push back" → SC_020 / bridge_stone_arch_03 / stone_arch_bridge_arch2_keystone, stone_arch_bridge_arch2_voussoir01, stone_arch_bridge_arch2_voussoir02 …; 192.00–198.62 s; claim CLM_710; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B12.s0 (199.03 s): "That is why arches suit materials that are strong under compression, like stone."
- Claim `CLM_709` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Part 2 Ratings, Item 25 Arch, p.144 (manual p.2-56)); SRC_ODOT_MBI (Glossary p.339 'arch'); SRC_YALE_PHYSICS ('Arch Bridges' section)
- Claim `CLM_710` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Glossary p.339 'arch'); SRC_YALE_PHYSICS ('Arch Bridges' section)
- Claim `CLM_726` [EDITORIALLY_APPROVED]: SRC_YALE_PHYSICS (unit 01.05.08, section 6)
- Shot: SC_021

## B12.s1 (204.90 s): "And it is why the supports matter so much: the abutments have to push inward on the arch, against its thrust."
- Claim `CLM_709` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Part 2 Ratings, Item 25 Arch, p.144 (manual p.2-56)); SRC_ODOT_MBI (Glossary p.339 'arch'); SRC_YALE_PHYSICS ('Arch Bridges' section)
- Claim `CLM_710` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Glossary p.339 'arch'); SRC_YALE_PHYSICS ('Arch Bridges' section)
- Claim `CLM_726` [EDITORIALLY_APPROVED]: SRC_YALE_PHYSICS (unit 01.05.08, section 6)
- Shot: SC_021
- Chú thích `B12_abut` COMPONENT_LABEL "Abutment" → SC_021 / bridge_stone_arch_03 / stone_arch_bridge_abutment_left; 204.79–213.25 s; claim CLM_710; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS
- Chú thích `B12_pier` COMPONENT_LABEL "Pier" → SC_021 / bridge_stone_arch_03 / stone_arch_bridge_pier1; 204.79–213.25 s; claim CLM_710; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B13.s0 (213.65 s): "Building an arch takes support of its own."
- Claim `CLM_723` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.2.1 Stone Arch, p. 3-48)
- Shot: SC_022

## B13.s1 (217.18 s): "While a stone arch is being built, a temporary timber frame called falsework holds the stones in place."
- Claim `CLM_723` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.2.1 Stone Arch, p. 3-48)
- Shot: SC_022

## B13.s2 (225.05 s): "So building one called for carpenters as well as skilled masons."
- Claim `CLM_723` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.2.1 Stone Arch, p. 3-48)
- Shot: SC_022

## B14.s0 (230.90 s): "Stone arches were generally more expensive to build than timber bridges."
- Claim `CLM_724` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.2.1 Stone Arch, p. 3-49)
- Claim `CLM_725` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.2.1 Stone Arch, p. 3-48)
- Shot: SC_023

## B14.s1 (236.95 s): "But stone was the preferred choice where durability and permanence were required, so arches were favoured on busy routes and in important places."
- Claim `CLM_724` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.2.1 Stone Arch, p. 3-49)
- Claim `CLM_725` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.2.1 Stone Arch, p. 3-48)
- Shot: SC_023

## B14.s2 (247.18 s): "Elsewhere, the lower cost of timber made up for its lack of permanence."
- Claim `CLM_724` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.2.1 Stone Arch, p. 3-49)
- Claim `CLM_725` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.2.1 Stone Arch, p. 3-48)
- Shot: SC_023

## B15.s0 (253.23 s): "A third approach is the truss."
- Claim `CLM_711` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Glossary p.386 'truss'); SRC_SCI_TRUSSES (Introduction)
- Claim `CLM_712` [EDITORIALLY_APPROVED]: SRC_SCI_TRUSSES (Introduction); SRC_FHWA_CBM (Chapter 2, 'Component Terminology')
- Shot: SC_024
- Chú thích `B15_ch` NOTE "5 · The truss" → SC_024 / bridge_steel_truss_pratt_01 / ; 253.12–256.08 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B15.s1 (256.18 s): "It builds a structure out of straight members, joined into triangles."
- Claim `CLM_711` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Glossary p.386 'truss'); SRC_SCI_TRUSSES (Introduction)
- Claim `CLM_712` [EDITORIALLY_APPROVED]: SRC_SCI_TRUSSES (Introduction); SRC_FHWA_CBM (Chapter 2, 'Component Terminology')
- Shot: SC_024
- Chú thích `B15_joints` COMPONENT_LABEL "Joints" → SC_024 / bridge_steel_truss_pratt_01 / steel_truss_bridge_span1_joints_south; 256.08–268.75 s; claim CLM_711; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B15.s2 (261.41 s): "Each member is mainly pulled or pushed along its length, in tension or in compression."
- Claim `CLM_711` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Glossary p.386 'truss'); SRC_SCI_TRUSSES (Introduction)
- Claim `CLM_712` [EDITORIALLY_APPROVED]: SRC_SCI_TRUSSES (Introduction); SRC_FHWA_CBM (Chapter 2, 'Component Terminology')
- Shot: SC_024
- Chú thích `B15_legend` TENSION_COMPRESSION_LEGEND → SC_024 / bridge_steel_truss_pratt_01 / ; 261.29–268.75 s; claim CLM_712; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B16.s0 (269.15 s): "In a simple span like these, under a downward load, the top chord is squeezed and the bottom chord is stretched."
- Claim `CLM_712` [EDITORIALLY_APPROVED]: SRC_SCI_TRUSSES (Introduction); SRC_FHWA_CBM (Chapter 2, 'Component Terminology')
- Claim `CLM_713` [EDITORIALLY_APPROVED]: SRC_FHWA_CBM (Chapter 2, 'Component Terminology'); SRC_SCI_TRUSSES ('Types of trusses')
- Claim `CLM_714` [EDITORIALLY_APPROVED]: SRC_FHWA_CBM (Chapter 2, 'Component Terminology')
- Shot: SC_025
- Chú thích `B16_legend` TENSION_COMPRESSION_LEGEND → SC_025 / bridge_steel_truss_pratt_01 / ; 269.04–283.33 s; claim CLM_712; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS
- Chú thích `B16_top` CALLOUT "Top chord: compression" → SC_025 / bridge_steel_truss_pratt_01 / steel_truss_bridge_span1_chords_south; 273.17–283.33 s; claim CLM_713; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS
- Chú thích `B16_bottom` CALLOUT "Bottom chord: tension" → SC_025 / bridge_steel_truss_pratt_01 / steel_truss_bridge_span1_chords_south; 274.71–283.33 s; claim CLM_713; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B16.s1 (277.12 s): "Inside, some web members are in compression and others are in tension."
- Claim `CLM_713` [EDITORIALLY_APPROVED]: SRC_FHWA_CBM (Chapter 2, 'Component Terminology'); SRC_SCI_TRUSSES ('Types of trusses')
- Claim `CLM_714` [EDITORIALLY_APPROVED]: SRC_FHWA_CBM (Chapter 2, 'Component Terminology')
- Shot: SC_025
- Chú thích `B16_web` COMPONENT_LABEL "Web members" → SC_025 / bridge_steel_truss_pratt_01 / steel_truss_bridge_span2_diagonals_south; 277.04–283.33 s; claim CLM_714; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B17.s0 (283.73 s): "The triangles can be arranged in different patterns."
- Claim `CLM_711` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Glossary p.386 'truss'); SRC_SCI_TRUSSES (Introduction)
- Claim `CLM_727` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-7)
- Claim `CLM_728` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-7)
- Shot: SC_026, SC_027, SC_028

## B17.s1 (288.03 s): "This is a Pratt truss."
- Claim `CLM_711` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Glossary p.386 'truss'); SRC_SCI_TRUSSES (Introduction)
- Claim `CLM_727` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-7)
- Claim `CLM_728` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-7)
- Shot: SC_026, SC_027, SC_028
- Chú thích `B17_pratt` NOTE "Pratt truss (patented 1844)" → SC_026 / bridge_steel_truss_pratt_01 / ; 287.92–299.46 s; claim CLM_727; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B17.s2 (290.61 s): "In the original design, patented in 1844, its verticals were timber and its diagonals were iron rods."
- Claim `CLM_711` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Glossary p.386 'truss'); SRC_SCI_TRUSSES (Introduction)
- Claim `CLM_727` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-7)
- Claim `CLM_728` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-7)
- Shot: SC_026, SC_027, SC_028

## B17.s3 (299.98 s): "Swap the web for diagonals that alternate in direction, and you have a Warren truss, patented in 1848."
- Claim `CLM_711` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Glossary p.386 'truss'); SRC_SCI_TRUSSES (Introduction)
- Claim `CLM_727` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-7)
- Claim `CLM_728` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-7)
- Shot: SC_026, SC_027, SC_028
- Chú thích `B17_warren` NOTE "Warren truss (patented 1848)" → SC_027 / bridge_steel_truss_warren_01 / ; 299.88–308.08 s; claim CLM_728; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS
- Chú thích `B17_warren` NOTE "Warren truss (patented 1848)" → SC_028 / bridge_steel_truss_warren_01 / ; 308.42–315.50 s; claim CLM_728; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B17.s4 (308.58 s): "Both patterns carry load through triangles; they simply arrange the members differently."
- Claim `CLM_711` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Glossary p.386 'truss'); SRC_SCI_TRUSSES (Introduction)
- Claim `CLM_727` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-7)
- Claim `CLM_728` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-7)
- Shot: SC_026, SC_027, SC_028

## B18.s0 (315.90 s): "Trusses also changed how bridges were built."
- Claim `CLM_729` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2 'Foundries and Fabricators', p. 2-11)
- Shot: SC_029

## B18.s1 (319.73 s): "By the middle of the nineteenth century, shops were making and drilling truss members, then shipping them to the bridge site, ready to assemble."
- Claim `CLM_729` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2 'Foundries and Fabricators', p. 2-11)
- Shot: SC_029
- Chú thích `B18_shop` NOTE "Members made and drilled in shops" → SC_029 / bridge_steel_truss_pratt_01 / ; 319.62–329.29 s; claim CLM_729; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B18.s2 (329.38 s): "And by 1860, the railroads relied almost entirely on these prefabricated parts."
- Claim `CLM_729` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2 'Foundries and Fabricators', p. 2-11)
- Shot: SC_029
- Chú thích `B18_1860` NOTE "By 1860: prefabricated parts" → SC_029 / bridge_steel_truss_pratt_01 / ; 329.29–337.17 s; claim CLM_729; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B40.s0 (337.57 s): "To cross wide rivers and deep gorges, bridges needed longer spans."
- Claim `CLM_752` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-142); SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-142)
- Shot: SC_030
- Chú thích `B40_ch` NOTE "6 · The cantilever" → SC_030 / None / ; 337.46–352.71 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B40.s1 (343.34 s): "Wide rivers like the Ohio and the Mississippi, and deep gorges like the one at Niagara, needed bridges that could reach farther."
- Claim `CLM_752` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-142); SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-142)
- Shot: SC_030
- Chú thích `B40_note` NOTE "A wider crossing (illustrative, not to scale)" → SC_030 / None / ; 343.25–352.71 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B41.s0 (353.44 s): "One answer was the cantilever."
- Claim `CLM_750` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-142); SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-142)
- Shot: SC_031

## B41.s1 (356.79 s): "Hold your arm straight out from your shoulder, and it is acting as a cantilever: supported at one end, free at the other, like a diving board."
- Claim `CLM_750` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-142); SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-142)
- Shot: SC_031
- Chú thích `B41_note` NOTE "Illustrative model" → SC_031 / bridge_cantilever_truss_01 / ; 356.71–367.08 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B42.s0 (367.48 s): "A cantilever bridge is a modified beam."
- Claim `CLM_750` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-142); SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-142)
- Claim `CLM_751` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.1 Trusses, p. 3-4); SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-142)
- Shot: SC_032

## B42.s1 (371.56 s): "Anchor arms rest on the banks and the main piers, cantilever arms reach out over the river, and a suspended span hangs between their tips."
- Claim `CLM_750` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-142); SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-142)
- Claim `CLM_751` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.1 Trusses, p. 3-4); SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-142)
- Shot: SC_032
- Chú thích `B42_anchor` COMPONENT_LABEL "Anchor arm" → SC_032 / bridge_cantilever_truss_01 / cantilever_bridge_anchor_arm_left_south; 371.46–382.17 s; claim CLM_751; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS
- Chú thích `B42_arm` COMPONENT_LABEL "Cantilever arm" → SC_032 / bridge_cantilever_truss_01 / cantilever_bridge_cantilever_arm_left_south; 374.88–382.17 s; claim CLM_751; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS
- Chú thích `B42_span` COMPONENT_LABEL "Suspended span" → SC_032 / bridge_cantilever_truss_01 / cantilever_bridge_suspended_span_south; 378.12–382.17 s; claim CLM_751; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B43.s0 (382.57 s): "Its great advantage came during construction."
- Claim `CLM_753` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-143)
- Shot: SC_033

## B43.s1 (386.42 s): "The arms could be built outward from the piers with no falsework blocking the channel below, and then the suspended span was lifted into place."
- Claim `CLM_753` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-143)
- Shot: SC_033
- Chú thích `B43_note` NOTE "Built outward: no falsework in the channel" → SC_033 / bridge_cantilever_truss_01 / ; 386.33–397.00 s; claim CLM_753; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B44.s0 (397.40 s): "In the United States, cantilevers were a standard answer for intermediate to longer spans from the 1880s to the 1960s."
- Claim `CLM_754` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-143)
- Claim `CLM_756` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-143)
- Claim `CLM_794` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-143)
- Shot: SC_034

## B44.s1 (407.18 s): "The Queensboro Bridge in New York was the country's longest cantilever when it was completed in 1909."
- Claim `CLM_754` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-143)
- Claim `CLM_756` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-143)
- Claim `CLM_794` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-143)
- Shot: SC_034

## B44.s2 (415.75 s): "Unlike our model, it has no suspended span in the middle, something one report calls unique among cantilevers of its size."
- Claim `CLM_754` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-143)
- Claim `CLM_756` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-143)
- Claim `CLM_794` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-143)
- Shot: SC_034

## B45.s0 (426.02 s): "For the longest spans of all, engineers hung the deck instead."
- Claim `CLM_760` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-133)
- Claim `CLM_763` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-133); SRC_FHWA_BRIDGE_TYPES (2.6 Suspension Bridges)
- Shot: SC_035
- Chú thích `B45_ch` NOTE "7 · The suspension bridge" → SC_035 / bridge_suspension_01 / ; 425.92–438.42 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS
- Chú thích `B45_model` NOTE "Illustrative model" → SC_035 / bridge_suspension_01 / ; 425.92–438.42 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B45.s1 (431.05 s): "In a suspension bridge, the deck hangs from vertical suspenders attached to great main cables."
- Claim `CLM_760` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-133)
- Claim `CLM_763` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-133); SRC_FHWA_BRIDGE_TYPES (2.6 Suspension Bridges)
- Shot: SC_035
- Chú thích `B45_hangers` COMPONENT_LABEL "Suspenders" → SC_035 / bridge_suspension_01 / suspension_bridge_hangers_south; 434.54–438.42 s; claim CLM_760; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS
- Chú thích `B45_cable` COMPONENT_LABEL "Main cable" → SC_035 / bridge_suspension_01 / suspension_bridge_main_cable_south; 435.25–438.42 s; claim CLM_760; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B46.s0 (439.15 s): "The cables are in tension, and they pass over towers that are in compression."
- Claim `CLM_760` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-133)
- Claim `CLM_761` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-133); SRC_FHWA_BRIDGE_TYPES (2.6 Suspension Bridges)
- Shot: SC_036
- Chú thích `B46_load` LOAD_ARROW "Load" → SC_036 / bridge_suspension_01 / suspension_bridge_deck; 439.04–451.75 s; claim CLM_760; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS
- Chú thích `B46_cable` CALLOUT "Cables: tension" → SC_036 / bridge_suspension_01 / suspension_bridge_main_cable_south; 440.42–451.75 s; claim CLM_760; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS
- Chú thích `B46_tower` CALLOUT "Towers: compression" → SC_036 / bridge_suspension_01 / suspension_bridge_tower_right; 443.17–451.75 s; claim CLM_760; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B46.s1 (444.98 s): "At each end, the cables are anchored, usually in large masses of stone or concrete."
- Claim `CLM_760` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-133)
- Claim `CLM_761` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-133); SRC_FHWA_BRIDGE_TYPES (2.6 Suspension Bridges)
- Shot: SC_036
- Chú thích `B46_anchor` COMPONENT_LABEL "Anchorage" → SC_036 / bridge_suspension_01 / suspension_bridge_anchorage_left; 446.50–451.75 s; claim CLM_761; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B47.s0 (452.48 s): "A suspension deck is light for its span, and it can be very flexible."
- Claim `CLM_765` [EDITORIALLY_APPROVED]: SRC_FHWA_BRIDGE_TYPES (2.6 Suspension Bridges); SRC_FHWA_BRIDGE_TYPES (2.6 Suspension Bridges)
- Shot: SC_037, SC_038

## B47.s1 (458.13 s): "So a stiffening truss is commonly built under the deck, against wind and earthquakes."
- Claim `CLM_765` [EDITORIALLY_APPROVED]: SRC_FHWA_BRIDGE_TYPES (2.6 Suspension Bridges); SRC_FHWA_BRIDGE_TYPES (2.6 Suspension Bridges)
- Shot: SC_037, SC_038
- Chú thích `B47_note` NOTE "Stiffening truss under the deck" → SC_038 / bridge_suspension_01 / ; 458.04–464.83 s; claim CLM_765; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B48.s0 (465.23 s): "The Brooklyn Bridge in New York, completed in 1883, was planned with two towers, cables and suspenders, anchorages and a stiffening truss."
- Claim `CLM_764` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-133)
- Claim `CLM_768` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-143); SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-133)
- Shot: SC_039

## B48.s1 (476.48 s): "One report says few suspension bridges built since can claim to stand entirely clear of its shadow."
- Claim `CLM_764` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-133)
- Claim `CLM_768` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-143); SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-133)
- Shot: SC_039

## B50.s0 (484.94 s): "A cable-stayed bridge also relies on steel cables, but it uses them differently."
- Claim `CLM_770` [EDITORIALLY_APPROVED]: SRC_FHWA_BRIDGE_TYPES (2.5 Cable-Stayed)
- Claim `CLM_771` [EDITORIALLY_APPROVED]: SRC_FHWA_BRIDGE_TYPES (2.5 Cable-Stayed); SRC_FHWA_BRIDGE_TYPES (2.5 Cable-Stayed)
- Shot: SC_040
- Chú thích `B50_ch` NOTE "8 · The cable-stayed bridge" → SC_040 / bridge_cable_stayed_01 / ; 484.83–498.25 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS
- Chú thích `B50_model` NOTE "Illustrative model" → SC_040 / bridge_cable_stayed_01 / ; 484.83–498.25 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B50.s1 (491.59 s): "Straight stay cables run from tall towers directly down to the edges of the deck."
- Claim `CLM_770` [EDITORIALLY_APPROVED]: SRC_FHWA_BRIDGE_TYPES (2.5 Cable-Stayed)
- Claim `CLM_771` [EDITORIALLY_APPROVED]: SRC_FHWA_BRIDGE_TYPES (2.5 Cable-Stayed); SRC_FHWA_BRIDGE_TYPES (2.5 Cable-Stayed)
- Shot: SC_040
- Chú thích `B50_stays` COMPONENT_LABEL "Stay cables" → SC_040 / bridge_cable_stayed_01 / cable_stayed_bridge_stay_left_side5; 492.12–498.25 s; claim CLM_770; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS
- Chú thích `B50_tower` COMPONENT_LABEL "Tower" → SC_040 / bridge_cable_stayed_01 / cable_stayed_bridge_pylon_right; 493.79–498.25 s; claim CLM_770; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B51.s0 (498.65 s): "Drawn in outline at the same span, the two types differ."
- Claim `CLM_761` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-133); SRC_FHWA_BRIDGE_TYPES (2.6 Suspension Bridges)
- Claim `CLM_763` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-133); SRC_FHWA_BRIDGE_TYPES (2.6 Suspension Bridges)
- Claim `CLM_770` [EDITORIALLY_APPROVED]: SRC_FHWA_BRIDGE_TYPES (2.5 Cable-Stayed)
- Claim `CLM_771` [EDITORIALLY_APPROVED]: SRC_FHWA_BRIDGE_TYPES (2.5 Cable-Stayed); SRC_FHWA_BRIDGE_TYPES (2.5 Cable-Stayed)
- Shot: SC_041

## B51.s1 (503.45 s): "The suspension bridge has much shorter towers, and its main cables run over them to anchorages at each end."
- Claim `CLM_761` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-133); SRC_FHWA_BRIDGE_TYPES (2.6 Suspension Bridges)
- Claim `CLM_763` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-133); SRC_FHWA_BRIDGE_TYPES (2.6 Suspension Bridges)
- Claim `CLM_770` [EDITORIALLY_APPROVED]: SRC_FHWA_BRIDGE_TYPES (2.5 Cable-Stayed)
- Claim `CLM_771` [EDITORIALLY_APPROVED]: SRC_FHWA_BRIDGE_TYPES (2.5 Cable-Stayed); SRC_FHWA_BRIDGE_TYPES (2.5 Cable-Stayed)
- Shot: SC_041

## B51.s2 (511.50 s): "The cable-stayed bridge needs taller towers, because their height depends on the span, and its stays end at the deck itself."
- Claim `CLM_761` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-133); SRC_FHWA_BRIDGE_TYPES (2.6 Suspension Bridges)
- Claim `CLM_763` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-133); SRC_FHWA_BRIDGE_TYPES (2.6 Suspension Bridges)
- Claim `CLM_770` [EDITORIALLY_APPROVED]: SRC_FHWA_BRIDGE_TYPES (2.5 Cable-Stayed)
- Claim `CLM_771` [EDITORIALLY_APPROVED]: SRC_FHWA_BRIDGE_TYPES (2.5 Cable-Stayed); SRC_FHWA_BRIDGE_TYPES (2.5 Cable-Stayed)
- Shot: SC_041

## B52.s0 (521.27 s): "Once the towers are up, the deck can be built outward from them in both directions, without falsework towers, until the spans meet."
- Claim `CLM_772` [EDITORIALLY_APPROVED]: SRC_FHWA_BRIDGE_TYPES (4.4 Cable-Stayed Bridges)
- Claim `CLM_773` [EDITORIALLY_APPROVED]: SRC_FHWA_BRIDGE_TYPES (2.5 Cable-Stayed)
- Shot: SC_042
- Chú thích `B52_note` NOTE "Built outward from the towers" → SC_042 / bridge_cable_stayed_01 / ; 521.17–530.71 s; claim CLM_772; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B52.s1 (530.80 s): "The stays also squeeze the deck along its length, and that squeeze builds up toward the towers."
- Claim `CLM_772` [EDITORIALLY_APPROVED]: SRC_FHWA_BRIDGE_TYPES (4.4 Cable-Stayed Bridges)
- Claim `CLM_773` [EDITORIALLY_APPROVED]: SRC_FHWA_BRIDGE_TYPES (2.5 Cable-Stayed)
- Shot: SC_042
- Chú thích `B52_deck` CALLOUT "Deck: squeezed by the stays" → SC_042 / bridge_cable_stayed_01 / cable_stayed_bridge_deck_closure; 531.92–535.83 s; claim CLM_773; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B53.s0 (538.36 s): "Before 1970, suspension bridges were thought to be the cheapest way to span more than about 1,200 feet."
- Claim `CLM_774` [EDITORIALLY_APPROVED]: SRC_FHWA_BRIDGE_TYPES (3.0 Economics)
- Claim `CLM_775` [EDITORIALLY_APPROVED]: SRC_FHWA_BRIDGE_TYPES (3.0 Economics)
- Shot: SC_043

## B53.s1 (547.66 s): "By 2012, a federal handbook said cable-stayed bridges become very competitive above 750 feet, and that suspension bridges pay off only as main spans approach 3,000."
- Claim `CLM_774` [EDITORIALLY_APPROVED]: SRC_FHWA_BRIDGE_TYPES (3.0 Economics)
- Claim `CLM_775` [EDITORIALLY_APPROVED]: SRC_FHWA_BRIDGE_TYPES (3.0 Economics)
- Shot: SC_043

## B19.s0 (562.98 s): "So which design is best?"
- Không có claim (câu dẫn dắt).
- Shot: SC_044

## B19.s1 (565.78 s): "The honest answer is that it depends."
- Không có claim (câu dẫn dắt).
- Shot: SC_044

## B19.s2 (569.13 s): "Materials, the site, the span, cost, and the skills available all pull in different directions."
- Không có claim (câu dẫn dắt).
- Shot: SC_044

## B20A.s0 (577.40 s): "Start with the materials themselves."
- Claim `CLM_726` [EDITORIALLY_APPROVED]: SRC_YALE_PHYSICS (unit 01.05.08, section 6)
- Shot: SC_045

## B20A.s1 (580.58 s): "An arch needs a material that is strong under compression, and stone is."
- Claim `CLM_726` [EDITORIALLY_APPROVED]: SRC_YALE_PHYSICS (unit 01.05.08, section 6)
- Shot: SC_045
- Chú thích `B20A_note` NOTE "Stone: strong under compression" → SC_045 / bridge_stone_arch_03 / ; 580.46–586.67 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B20B.s0 (587.07 s): "A truss needs members that can work in tension as well as compression."
- Claim `CLM_712` [EDITORIALLY_APPROVED]: SRC_SCI_TRUSSES (Introduction); SRC_FHWA_CBM (Chapter 2, 'Component Terminology')
- Claim `CLM_735` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-8)
- Shot: SC_046
- Chú thích `B20B_note` NOTE "Truss members: tension and compression" → SC_046 / bridge_steel_truss_pratt_01 / ; 586.96–592.71 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B20B.s1 (592.79 s): "Wrought iron was valued for exactly that: one historian calls it a material strong equally in tension and in compression."
- Claim `CLM_712` [EDITORIALLY_APPROVED]: SRC_SCI_TRUSSES (Introduction); SRC_FHWA_CBM (Chapter 2, 'Component Terminology')
- Claim `CLM_735` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-8)
- Shot: SC_046
- Chú thích `B20B_iron` NOTE "Wrought iron: valued in tension and compression" → SC_046 / bridge_steel_truss_pratt_01 / ; 592.71–602.54 s; claim CLM_735; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B20C.s0 (602.94 s): "Wood was often plentiful and cheap, but wooden bridges were vulnerable to decay."
- Claim `CLM_734` [EDITORIALLY_APPROVED]: SRC_ASCE_BOLLMAN (main text)
- Claim `CLM_742` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Shot: SC_047
- Chú thích `B20C_note` NOTE "Timber: plentiful and cheap, but it decays" → SC_047 / bridge_timber_beam_01 / ; 602.83–609.79 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B21.s0 (610.19 s): "That is one reason many timber truss bridges were covered with a roof and siding, to protect them from the weather."
- Claim `CLM_733` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.1.1 King Post, p. 3-7)
- Claim `CLM_746` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (List of figures, 3-5)
- Shot: SC_048

## B21.s1 (618.52 s): "This is the Humpback Covered Bridge, built in 1857 over Dunlap Creek."
- Claim `CLM_733` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.1.1 King Post, p. 3-7)
- Claim `CLM_746` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (List of figures, 3-5)
- Shot: SC_048

## B20E.s0 (626.19 s): "Cables have a materials story of their own."
- Claim `CLM_780` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-132); SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-132)
- Claim `CLM_781` [EDITORIALLY_APPROVED]: SRC_FHWA_BRIDGE_TYPES (2.5 Cable-Stayed); SRC_FHWA_BRIDGE_TYPES (2.6 Suspension Bridges)
- Shot: SC_049
- Chú thích `B20E_model` NOTE "Illustrative model" → SC_049 / bridge_suspension_01 / ; 626.08–652.83 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B20E.s1 (629.87 s): "America's first metal suspension bridges hung from iron chains, and many failed after only a few years: critics said such a bridge was only as good as the weakest link in one of its chains."
- Claim `CLM_780` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-132); SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-132)
- Claim `CLM_781` [EDITORIALLY_APPROVED]: SRC_FHWA_BRIDGE_TYPES (2.5 Cable-Stayed); SRC_FHWA_BRIDGE_TYPES (2.6 Suspension Bridges)
- Shot: SC_049
- Chú thích `B20E_chain` NOTE "Iron chains: only as strong as the weakest link" → SC_049 / bridge_suspension_01 / ; 629.75–643.38 s; claim CLM_780; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B20E.s2 (643.49 s): "Wire cables answered that fear, and suspension and cable-stayed bridges came to rely on high-strength steel cables."
- Claim `CLM_780` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-132); SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-132)
- Claim `CLM_781` [EDITORIALLY_APPROVED]: SRC_FHWA_BRIDGE_TYPES (2.5 Cable-Stayed); SRC_FHWA_BRIDGE_TYPES (2.6 Suspension Bridges)
- Shot: SC_049
- Chú thích `B20E_cable` NOTE "Wire cables, then high-strength steel" → SC_049 / bridge_suspension_01 / ; 643.38–652.83 s; claim CLM_781; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B22.s0 (653.23 s): "The site of a bridge matters too."
- Claim `CLM_736` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.6 Trestles and Viaducts, p. 3-137); SRC_NCHRP_CONTEXT (3.6 Trestles and Viaducts, p. 3-137)
- Shot: SC_050

## B22.s1 (656.31 s): "Railway engines have limited traction, so railways need gentle gradients."
- Claim `CLM_736` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.6 Trestles and Viaducts, p. 3-137); SRC_NCHRP_CONTEXT (3.6 Trestles and Viaducts, p. 3-137)
- Shot: SC_050

## B22.s2 (662.43 s): "Where a valley was too deep and wide to fill with an embankment, engineers built viaducts and trestles to keep the line nearly straight and level."
- Claim `CLM_736` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.6 Trestles and Viaducts, p. 3-137); SRC_NCHRP_CONTEXT (3.6 Trestles and Viaducts, p. 3-137)
- Shot: SC_050

## B22B.s0 (673.32 s): "Long spans make the ground beneath them matter even more."
- Claim `CLM_761` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-133); SRC_FHWA_BRIDGE_TYPES (2.6 Suspension Bridges)
- Claim `CLM_776` [EDITORIALLY_APPROVED]: SRC_FHWA_BRIDGE_TYPES (3.0 Economics)
- Shot: SC_051

## B22B.s1 (678.22 s): "A suspension bridge has to anchor its cables in massive blocks, or directly in bedrock."
- Claim `CLM_761` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-133); SRC_FHWA_BRIDGE_TYPES (2.6 Suspension Bridges)
- Claim `CLM_776` [EDITORIALLY_APPROVED]: SRC_FHWA_BRIDGE_TYPES (3.0 Economics)
- Shot: SC_051

## B22B.s2 (685.19 s): "The towers of a cable-stayed bridge, by contrast, can be built where good rock does not lie near the surface."
- Claim `CLM_761` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-133); SRC_FHWA_BRIDGE_TYPES (2.6 Suspension Bridges)
- Claim `CLM_776` [EDITORIALLY_APPROVED]: SRC_FHWA_BRIDGE_TYPES (3.0 Economics)
- Shot: SC_051

## B22C.s0 (694.02 s): "A cantilever like this one is a continuous girder with hinges built in, which made its forces easy to calculate."
- Claim `CLM_782` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-142); SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-142); SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-142)
- Shot: SC_052
- Chú thích `B22C_model` NOTE "Illustrative model" → SC_052 / bridge_cantilever_truss_01 / ; 693.92–713.58 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B22C.s1 (702.80 s): "So on unstable soil, if a pier sank, its superstructure could adjust, where a continuous beam might build up hidden stresses and fail."
- Claim `CLM_782` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-142); SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-142); SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-142)
- Shot: SC_052
- Chú thích `B22C_note` NOTE "Hinged: superstructure could adjust if a pier sank" → SC_052 / bridge_cantilever_truss_01 / ; 702.71–713.58 s; claim CLM_782; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS
- Chú thích `B22C_pier` COMPONENT_LABEL "Main pier" → SC_052 / bridge_cantilever_truss_01 / cantilever_bridge_pier_left; 705.17–713.58 s; claim CLM_782; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B22D.s0 (713.98 s): "Then there is the wind."
- Claim `CLM_765` [EDITORIALLY_APPROVED]: SRC_FHWA_BRIDGE_TYPES (2.6 Suspension Bridges); SRC_FHWA_BRIDGE_TYPES (2.6 Suspension Bridges)
- Claim `CLM_783` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-28); SRC_NCHRP_CONTEXT (2.2, p. 2-28); SRC_FHWA_BRIDGE_TYPES (2.6 Suspension Bridges)
- Shot: SC_053
- Chú thích `B22D_model` NOTE "Illustrative model" → SC_053 / bridge_suspension_01 / ; 713.88–735.04 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B22D.s1 (716.61 s): "In 1940, the four-month-old Tacoma Narrows suspension bridge collapsed in only moderately high winds."
- Claim `CLM_765` [EDITORIALLY_APPROVED]: SRC_FHWA_BRIDGE_TYPES (2.6 Suspension Bridges); SRC_FHWA_BRIDGE_TYPES (2.6 Suspension Bridges)
- Claim `CLM_783` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-28); SRC_NCHRP_CONTEXT (2.2, p. 2-28); SRC_FHWA_BRIDGE_TYPES (2.6 Suspension Bridges)
- Shot: SC_053
- Chú thích `B22D_tacoma` NOTE "Tacoma Narrows, 1940: lost to the wind" → SC_053 / bridge_suspension_01 / ; 716.50–725.29 s; claim CLM_783; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B22D.s2 (725.38 s): "The disaster led to intense research on wind, and later suspension bridges were built to new standards for stiffened decks."
- Claim `CLM_765` [EDITORIALLY_APPROVED]: SRC_FHWA_BRIDGE_TYPES (2.6 Suspension Bridges); SRC_FHWA_BRIDGE_TYPES (2.6 Suspension Bridges)
- Claim `CLM_783` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-28); SRC_NCHRP_CONTEXT (2.2, p. 2-28); SRC_FHWA_BRIDGE_TYPES (2.6 Suspension Bridges)
- Shot: SC_053
- Chú thích `B22D_stiff` NOTE "Afterwards: research and stiffened decks" → SC_053 / bridge_suspension_01 / ; 725.29–735.04 s; claim CLM_783; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS
- Chú thích `B22D_truss` COMPONENT_LABEL "Stiffening truss" → SC_053 / bridge_suspension_01 / suspension_bridge_stiffening_truss_south; 725.29–735.04 s; claim CLM_765; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B23C.s0 (735.44 s): "Span decides a great deal."
- Claim `CLM_775` [EDITORIALLY_APPROVED]: SRC_FHWA_BRIDGE_TYPES (3.0 Economics)
- Claim `CLM_784` [EDITORIALLY_APPROVED]: SRC_FHWA_BRIDGE_TYPES (3.0 Economics)
- Claim `CLM_785` [EDITORIALLY_APPROVED]: SRC_FHWA_BRIDGE_TYPES (3.0 Economics); SRC_FHWA_BRIDGE_TYPES (3.0 Economics)
- Claim `CLM_786` [EDITORIALLY_APPROVED]: SRC_FHWA_BRIDGE_TYPES (3.0 Economics); SRC_FHWA_BRIDGE_TYPES (3.0 Economics)
- Shot: SC_054

## B23C.s1 (738.37 s): "A 2012 federal handbook for steel bridges gives two kinds of numbers."
- Claim `CLM_775` [EDITORIALLY_APPROVED]: SRC_FHWA_BRIDGE_TYPES (3.0 Economics)
- Claim `CLM_784` [EDITORIALLY_APPROVED]: SRC_FHWA_BRIDGE_TYPES (3.0 Economics)
- Claim `CLM_785` [EDITORIALLY_APPROVED]: SRC_FHWA_BRIDGE_TYPES (3.0 Economics); SRC_FHWA_BRIDGE_TYPES (3.0 Economics)
- Claim `CLM_786` [EDITORIALLY_APPROVED]: SRC_FHWA_BRIDGE_TYPES (3.0 Economics); SRC_FHWA_BRIDGE_TYPES (3.0 Economics)
- Shot: SC_054

## B23C.s2 (744.49 s): "Some are practical ranges: plate girders from about 90 to over 500 feet, simple trusses from about 450 to about 750, and cantilever trusses considerably farther."
- Claim `CLM_775` [EDITORIALLY_APPROVED]: SRC_FHWA_BRIDGE_TYPES (3.0 Economics)
- Claim `CLM_784` [EDITORIALLY_APPROVED]: SRC_FHWA_BRIDGE_TYPES (3.0 Economics)
- Claim `CLM_785` [EDITORIALLY_APPROVED]: SRC_FHWA_BRIDGE_TYPES (3.0 Economics); SRC_FHWA_BRIDGE_TYPES (3.0 Economics)
- Claim `CLM_786` [EDITORIALLY_APPROVED]: SRC_FHWA_BRIDGE_TYPES (3.0 Economics); SRC_FHWA_BRIDGE_TYPES (3.0 Economics)
- Shot: SC_054

## B23C.s3 (759.19 s): "Others are spans that have actually been built: arches from about 200 to 1,800 feet, and cable-stayed bridges from under 200 to nearly 3,000."
- Claim `CLM_775` [EDITORIALLY_APPROVED]: SRC_FHWA_BRIDGE_TYPES (3.0 Economics)
- Claim `CLM_784` [EDITORIALLY_APPROVED]: SRC_FHWA_BRIDGE_TYPES (3.0 Economics)
- Claim `CLM_785` [EDITORIALLY_APPROVED]: SRC_FHWA_BRIDGE_TYPES (3.0 Economics); SRC_FHWA_BRIDGE_TYPES (3.0 Economics)
- Claim `CLM_786` [EDITORIALLY_APPROVED]: SRC_FHWA_BRIDGE_TYPES (3.0 Economics); SRC_FHWA_BRIDGE_TYPES (3.0 Economics)
- Shot: SC_054

## B23C.s4 (771.89 s): "And as we saw, suspension bridges only pay off as main spans approach 3,000 feet."
- Claim `CLM_775` [EDITORIALLY_APPROVED]: SRC_FHWA_BRIDGE_TYPES (3.0 Economics)
- Claim `CLM_784` [EDITORIALLY_APPROVED]: SRC_FHWA_BRIDGE_TYPES (3.0 Economics)
- Claim `CLM_785` [EDITORIALLY_APPROVED]: SRC_FHWA_BRIDGE_TYPES (3.0 Economics); SRC_FHWA_BRIDGE_TYPES (3.0 Economics)
- Claim `CLM_786` [EDITORIALLY_APPROVED]: SRC_FHWA_BRIDGE_TYPES (3.0 Economics); SRC_FHWA_BRIDGE_TYPES (3.0 Economics)
- Shot: SC_054

## B23D.s0 (779.82 s): "Cost and skill pull in different directions."
- Claim `CLM_757` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-142)
- Claim `CLM_787` [EDITORIALLY_APPROVED]: SRC_FHWA_BRIDGE_TYPES (4.5 Suspension Bridges); SRC_FHWA_BRIDGE_TYPES (4.5 Suspension Bridges)
- Shot: SC_055
- Chú thích `B23D_model` NOTE "Illustrative model" → SC_055 / bridge_suspension_01 / ; 779.71–800.92 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B23D.s1 (783.47 s): "A cantilever avoided the expensive anchorages a suspension bridge needs."
- Claim `CLM_757` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-142)
- Claim `CLM_787` [EDITORIALLY_APPROVED]: SRC_FHWA_BRIDGE_TYPES (4.5 Suspension Bridges); SRC_FHWA_BRIDGE_TYPES (4.5 Suspension Bridges)
- Shot: SC_055
- Chú thích `B23D_anchor` COMPONENT_LABEL "Anchorages: costly" → SC_055 / bridge_suspension_01 / suspension_bridge_anchorage_left; 786.29–800.92 s; claim CLM_757; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B23D.s2 (789.69 s): "And a suspension bridge often takes a long time to build: installing its main cables calls for expertise that very few contractors have."
- Claim `CLM_757` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-142)
- Claim `CLM_787` [EDITORIALLY_APPROVED]: SRC_FHWA_BRIDGE_TYPES (4.5 Suspension Bridges); SRC_FHWA_BRIDGE_TYPES (4.5 Suspension Bridges)
- Shot: SC_055
- Chú thích `B23D_cable` COMPONENT_LABEL "Main cables: specialist work" → SC_055 / bridge_suspension_01 / suspension_bridge_main_cable_south; 794.29–800.92 s; claim CLM_787; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B23E.s0 (801.32 s): "By 2012, cable-stayed bridges were becoming more common worldwide, and one significant reason was that the methods for erecting them had become better understood."
- Claim `CLM_788` [EDITORIALLY_APPROVED]: SRC_FHWA_BRIDGE_TYPES (4.4 Cable-Stayed Bridges)
- Shot: SC_056
- Chú thích `B23E_note` NOTE "By 2012: erection methods better understood" → SC_056 / bridge_cable_stayed_01 / ; 801.21–814.00 s; claim CLM_788; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B24.s0 (814.40 s): "Finally, every bridge belongs to its time."
- Claim `CLM_727` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-7)
- Claim `CLM_728` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-7)
- Claim `CLM_729` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2 'Foundries and Fabricators', p. 2-11)
- Claim `CLM_738` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.2.1 Stone Arch, p. 3-49)
- Claim `CLM_739` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Shot: SC_057

## B24.s1 (818.38 s): "As metal trusses spread, skilled masons became fewer and reinforced concrete arrived, stone arch construction declined."
- Claim `CLM_727` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-7)
- Claim `CLM_728` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-7)
- Claim `CLM_729` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2 'Foundries and Fabricators', p. 2-11)
- Claim `CLM_738` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.2.1 Stone Arch, p. 3-49)
- Claim `CLM_739` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Shot: SC_057

## B24.s2 (827.88 s): "Then, during the Great Depression, it briefly returned."
- Claim `CLM_727` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-7)
- Claim `CLM_728` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-7)
- Claim `CLM_729` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2 'Foundries and Fabricators', p. 2-11)
- Claim `CLM_738` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.2.1 Stone Arch, p. 3-49)
- Claim `CLM_739` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Shot: SC_057

## B24B.s0 (833.07 s): "Long spans have a timeline of their own."
- Claim `CLM_754` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-143)
- Claim `CLM_756` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-143)
- Claim `CLM_766` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-132); SRC_EWV_WHEELING (Wheeling Suspension Bridge, first paragraph); SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-133)
- Claim `CLM_768` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-143); SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-133)
- Claim `CLM_774` [EDITORIALLY_APPROVED]: SRC_FHWA_BRIDGE_TYPES (3.0 Economics)
- Shot: SC_058

## B24B.s1 (836.64 s): "By 1849, a suspension bridge at Wheeling spanned 1,010 feet, the longest span in the world when it opened."
- Claim `CLM_754` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-143)
- Claim `CLM_756` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-143)
- Claim `CLM_766` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-132); SRC_EWV_WHEELING (Wheeling Suspension Bridge, first paragraph); SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-133)
- Claim `CLM_768` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-143); SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-133)
- Claim `CLM_774` [EDITORIALLY_APPROVED]: SRC_FHWA_BRIDGE_TYPES (3.0 Economics)
- Shot: SC_058

## B24B.s2 (846.19 s): "Cantilevers were a standard American answer from the 1880s to the 1960s, and a 2012 federal handbook found that almost every American bridge built since 1980 with a main span over 1,000 feet was cable-stayed."
- Claim `CLM_754` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-143)
- Claim `CLM_756` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-143)
- Claim `CLM_766` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-132); SRC_EWV_WHEELING (Wheeling Suspension Bridge, first paragraph); SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-133)
- Claim `CLM_768` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-143); SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-133)
- Claim `CLM_774` [EDITORIALLY_APPROVED]: SRC_FHWA_BRIDGE_TYPES (3.0 Economics)
- Shot: SC_058

## B25.s0 (864.02 s): "These trade-offs played out across nineteenth-century America as the railways spread."
- Claim `CLM_741` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6); SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Claim `CLM_742` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Shot: SC_059

## B25.s1 (870.38 s): "In the East, railroads built massive stone viaducts, while western builders generally used timber."
- Claim `CLM_741` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6); SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Claim `CLM_742` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Shot: SC_059

## B25.s2 (878.15 s): "Three documented examples show how differently builders answered."
- Claim `CLM_741` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6); SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Claim `CLM_742` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Shot: SC_059

## B26.s0 (884.40 s): "Near Baltimore, the Carrollton Viaduct was completed in 1829."
- Claim `CLM_739` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Claim `CLM_740` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.6 Trestles and Viaducts, p. 3-137)
- Shot: SC_060

## B26.s1 (890.48 s): "Built of roughly twelve thousand granite blocks, it carries the railway over Gwynns Falls on an eighty foot arch."
- Claim `CLM_739` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Claim `CLM_740` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.6 Trestles and Viaducts, p. 3-137)
- Shot: SC_060

## B26.s2 (898.90 s): "A national report in 2005 called it the world's oldest stone railroad span still in service."
- Claim `CLM_739` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Claim `CLM_740` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.6 Trestles and Viaducts, p. 3-137)
- Shot: SC_060

## B27.s0 (907.52 s): "Early railroads needed durable bridges to carry heavy trains."
- Claim `CLM_725` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.2.1 Stone Arch, p. 3-48)
- Claim `CLM_741` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6); SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Shot: SC_061
- Chú thích `B27_note` NOTE "Illustrative model, not the Carrollton Viaduct" → SC_061 / bridge_stone_arch_03 / ; 907.42–917.25 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B27.s1 (912.65 s): "For a line meant to last, stone was the answer."
- Claim `CLM_725` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.2.1 Stone Arch, p. 3-48)
- Claim `CLM_741` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6); SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Shot: SC_061

## B28.s0 (917.65 s): "In the West, the pressure was different."
- Claim `CLM_742` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Claim `CLM_743` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (List of figures, 3-106)
- Shot: SC_062

## B28.s1 (920.90 s): "Railroads had to open new lines quickly and economically, and timber was abundant and cheap."
- Claim `CLM_742` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Claim `CLM_743` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (List of figures, 3-106)
- Shot: SC_062

## B28.s2 (927.95 s): "This timber trestle near Corinne, Utah, was built in 1872 by the Central Pacific Railroad."
- Claim `CLM_742` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Claim `CLM_743` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (List of figures, 3-106)
- Shot: SC_062

## B29.s0 (937.27 s): "A trestle is a succession of towers supporting short spans."
- Claim `CLM_737` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.6 Trestles and Viaducts, p. 3-137)
- Shot: SC_063
- Chú thích `B29_note` NOTE "Illustrative model, not the Promontory trestle" → SC_063 / bridge_timber_beam_01 / ; 937.17–949.38 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B29.s1 (942.12 s): "It is the same beam idea as our timber model, repeated as often as the crossing needs."
- Claim `CLM_737` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.6 Trestles and Viaducts, p. 3-137)
- Shot: SC_063

## B30.s0 (949.77 s): "Iron offered a third path."
- Claim `CLM_744` [EDITORIALLY_APPROVED]: SRC_ASCE_BOLLMAN (main text); SRC_ASCE_BOLLMAN (main text)
- Claim `CLM_745` [EDITORIALLY_APPROVED]: SRC_ASCE_BOLLMAN (main text)
- Shot: SC_064

## B30.s1 (952.67 s): "The Bollman truss, patented in 1852, was one of the first designs to use iron in all of its essential structural parts."
- Claim `CLM_744` [EDITORIALLY_APPROVED]: SRC_ASCE_BOLLMAN (main text); SRC_ASCE_BOLLMAN (main text)
- Claim `CLM_745` [EDITORIALLY_APPROVED]: SRC_ASCE_BOLLMAN (main text)
- Shot: SC_064

## B30.s2 (962.62 s): "It could be built relatively quickly and inexpensively, while offering the long-lasting qualities of metal."
- Claim `CLM_744` [EDITORIALLY_APPROVED]: SRC_ASCE_BOLLMAN (main text); SRC_ASCE_BOLLMAN (main text)
- Claim `CLM_745` [EDITORIALLY_APPROVED]: SRC_ASCE_BOLLMAN (main text)
- Shot: SC_064

## B30.s3 (970.33 s): "The bridge at Savage, Maryland, is the only remaining example of the design."
- Claim `CLM_744` [EDITORIALLY_APPROVED]: SRC_ASCE_BOLLMAN (main text); SRC_ASCE_BOLLMAN (main text)
- Claim `CLM_745` [EDITORIALLY_APPROVED]: SRC_ASCE_BOLLMAN (main text)
- Shot: SC_064

## B31.s0 (977.48 s): "Stone for permanence, timber for speed and economy, and iron trusses that offered some of both."
- Claim `CLM_741` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6); SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Claim `CLM_742` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Claim `CLM_744` [EDITORIALLY_APPROVED]: SRC_ASCE_BOLLMAN (main text); SRC_ASCE_BOLLMAN (main text)
- Shot: SC_065

## B31.s1 (984.71 s): "Three places, three sets of constraints, three different bridges."
- Claim `CLM_741` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6); SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Claim `CLM_742` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Claim `CLM_744` [EDITORIALLY_APPROVED]: SRC_ASCE_BOLLMAN (main text); SRC_ASCE_BOLLMAN (main text)
- Shot: SC_065

## B31A.s0 (990.57 s): "Long spans forced hard decisions too."
- Claim `CLM_789` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-132); SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-133)
- Shot: SC_066
- Chú thích `B31A_note` NOTE "Illustrative model, not the Niagara bridge" → SC_066 / bridge_suspension_01 / ; 990.46–1019.92 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B31A.s1 (994.17 s): "In 1855, John Roebling's suspension bridge carried trains across the Niagara Gorge, but railroad executives doubted that suspension bridges could bear heavy trains."
- Claim `CLM_789` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-132); SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-133)
- Shot: SC_066
- Chú thích `B31A_1855` NOTE "Niagara Gorge, 1855: trains on a suspension bridge" → SC_066 / bridge_suspension_01 / ; 994.08–1007.21 s; claim CLM_789; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B31A.s2 (1007.32 s): "Their doubts were not unjustified: the bridge needed substantial repairs in 1877 and 1880, and it was declared inadequate in 1890."
- Claim `CLM_789` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-132); SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-133)
- Shot: SC_066
- Chú thích `B31A_1890` NOTE "Repaired 1877 and 1880; declared inadequate in 1890" → SC_066 / bridge_suspension_01 / ; 1007.21–1019.92 s; claim CLM_789; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B31B.s0 (1020.32 s): "In America, modern cantilevers were first used by the railroads, and only later for highways."
- Claim `CLM_790` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-142); SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-143)
- Claim `CLM_791` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-143)
- Shot: SC_067
- Chú thích `B31B_note` NOTE "Illustrative model, not the Kentucky River bridge" → SC_067 / bridge_cantilever_truss_01 / ; 1020.21–1049.75 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B31B.s1 (1027.99 s): "A cantilever is inherently rigid, so if properly designed, heavy locomotives pulling trains are no threat to it."
- Claim `CLM_790` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-142); SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-143)
- Claim `CLM_791` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-143)
- Shot: SC_067
- Chú thích `B31B_rigid` NOTE "Inherently rigid: suited to heavy trains" → SC_067 / bridge_cantilever_truss_01 / ; 1027.88–1036.58 s; claim CLM_790; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B31B.s2 (1036.69 s): "In 1877, one carried the Cincinnati Southern Railroad across the 275-foot-deep Kentucky River gorge: the longest cantilever in the world."
- Claim `CLM_790` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-142); SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-143)
- Claim `CLM_791` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-143)
- Shot: SC_067
- Chú thích `B31B_1877` NOTE "1877: the world's longest cantilever" → SC_067 / bridge_cantilever_truss_01 / ; 1036.58–1049.75 s; claim CLM_791; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B31C.s0 (1050.15 s): "In San Francisco, the Golden Gate Bridge opened in 1937."
- Claim `CLM_792` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-28)
- Shot: SC_068

## B31C.s1 (1056.38 s): "For 27 years, it stood as the world's longest span."
- Claim `CLM_792` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-28)
- Shot: SC_068

## B31D.s0 (1062.40 s): "In Maine, a modern cable-stayed bridge went up remarkably fast."
- Claim `CLM_793` [EDITORIALLY_APPROVED]: SRC_FHWA_PENOBSCOT (Chapter 3, The test bridge); SRC_FHWA_PENOBSCOT (Chapter 3, The test bridge); SRC_FHWA_PENOBSCOT (Chapter 3, The test bridge); SRC_FHWA_PENOBSCOT (Chapter 3, The test bridge); SRC_FHWA_PENOBSCOT (Chapter 3, The test bridge)
- Shot: SC_069
- Chú thích `B31D_note` NOTE "Illustrative model, not the Penobscot Narrows Bridge" → SC_069 / bridge_cable_stayed_01 / ; 1062.29–1090.08 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B31D.s1 (1067.67 s): "The Penobscot Narrows Bridge, opened in 2006, carries its 1,161-foot main span on two concrete pylons 430 feet tall."
- Claim `CLM_793` [EDITORIALLY_APPROVED]: SRC_FHWA_PENOBSCOT (Chapter 3, The test bridge); SRC_FHWA_PENOBSCOT (Chapter 3, The test bridge); SRC_FHWA_PENOBSCOT (Chapter 3, The test bridge); SRC_FHWA_PENOBSCOT (Chapter 3, The test bridge); SRC_FHWA_PENOBSCOT (Chapter 3, The test bridge)
- Shot: SC_069
- Chú thích `B31D_fact` NOTE "Penobscot Narrows, 2006: 430 ft concrete pylons" → SC_069 / bridge_cable_stayed_01 / ; 1067.58–1080.71 s; claim CLM_793; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B31D.s2 (1080.83 s): "It took just 42 months from conception to completion, and one of its pylons has a public observatory at the top."
- Claim `CLM_793` [EDITORIALLY_APPROVED]: SRC_FHWA_PENOBSCOT (Chapter 3, The test bridge); SRC_FHWA_PENOBSCOT (Chapter 3, The test bridge); SRC_FHWA_PENOBSCOT (Chapter 3, The test bridge); SRC_FHWA_PENOBSCOT (Chapter 3, The test bridge); SRC_FHWA_PENOBSCOT (Chapter 3, The test bridge)
- Shot: SC_069
- Chú thích `B31D_42` NOTE "42 months from conception to completion" → SC_069 / bridge_cable_stayed_01 / ; 1080.71–1090.08 s; claim CLM_793; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B32.s0 (1090.48 s): "So why don't bridges all look the same?"
- Claim `CLM_706` [EDITORIALLY_APPROVED]: SRC_FHWA_CBM (Chapter 2, 'Component Terminology'); SRC_ODOT_MBI (Glossary p.358 'girder')
- Claim `CLM_709` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Part 2 Ratings, Item 25 Arch, p.144 (manual p.2-56)); SRC_ODOT_MBI (Glossary p.339 'arch'); SRC_YALE_PHYSICS ('Arch Bridges' section)
- Claim `CLM_712` [EDITORIALLY_APPROVED]: SRC_SCI_TRUSSES (Introduction); SRC_FHWA_CBM (Chapter 2, 'Component Terminology')
- Shot: SC_070
- Chú thích `B32_ch` NOTE "12 · Why they look different" → SC_070 / bridge_steel_truss_pratt_01 / ; 1090.38–1098.63 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B32.s1 (1093.86 s): "Because a bridge's form comes from two things working together."
- Claim `CLM_706` [EDITORIALLY_APPROVED]: SRC_FHWA_CBM (Chapter 2, 'Component Terminology'); SRC_ODOT_MBI (Glossary p.358 'girder')
- Claim `CLM_709` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Part 2 Ratings, Item 25 Arch, p.144 (manual p.2-56)); SRC_ODOT_MBI (Glossary p.339 'arch'); SRC_YALE_PHYSICS ('Arch Bridges' section)
- Claim `CLM_712` [EDITORIALLY_APPROVED]: SRC_SCI_TRUSSES (Introduction); SRC_FHWA_CBM (Chapter 2, 'Component Terminology')
- Shot: SC_070

## B32.s2 (1098.73 s): "One is how its structure carries load: beams resist bending, arches work in compression, and trusses share load among members in tension and compression."
- Claim `CLM_706` [EDITORIALLY_APPROVED]: SRC_FHWA_CBM (Chapter 2, 'Component Terminology'); SRC_ODOT_MBI (Glossary p.358 'girder')
- Claim `CLM_709` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Part 2 Ratings, Item 25 Arch, p.144 (manual p.2-56)); SRC_ODOT_MBI (Glossary p.339 'arch'); SRC_YALE_PHYSICS ('Arch Bridges' section)
- Claim `CLM_712` [EDITORIALLY_APPROVED]: SRC_SCI_TRUSSES (Introduction); SRC_FHWA_CBM (Chapter 2, 'Component Terminology')
- Shot: SC_070
- Chú thích `B32_one` NOTE "1 · How the structure carries load" → SC_070 / bridge_steel_truss_pratt_01 / ; 1098.63–1110.54 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B32L.s0 (1110.94 s): "Cantilevers reach out from their piers, and suspension and cable-stayed bridges hang their decks from steel cables."
- Claim `CLM_750` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-142); SRC_NCHRP_CONTEXT (3.7 Cantilevers, p. 3-142)
- Claim `CLM_760` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-133)
- Claim `CLM_770` [EDITORIALLY_APPROVED]: SRC_FHWA_BRIDGE_TYPES (2.5 Cable-Stayed)
- Shot: SC_071
- Chú thích `B32L_one` NOTE "1 · How the structure carries load" → SC_071 / bridge_cable_stayed_01 / ; 1110.84–1119.67 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B32B.s0 (1120.07 s): "The other is the world it was built in: its materials, its site, its span, its budget and its builders."
- Claim `CLM_724` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.2.1 Stone Arch, p. 3-49)
- Claim `CLM_742` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Shot: SC_072

## B33.s0 (1128.73 s): "And it is not a simple story of progress."
- Claim `CLM_721` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.3.1 Timber Stringer, p. 3-80); SRC_NCHRP_CONTEXT (3.3.1 Timber Stringer, p. 3-80)
- Claim `CLM_738` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.2.1 Stone Arch, p. 3-49)
- Claim `CLM_767` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-133)
- Claim `CLM_777` [EDITORIALLY_APPROVED]: SRC_FHWA_BRIDGE_TYPES (3.0 Economics)
- Shot: SC_073

## B33.s1 (1132.43 s): "Timber beam bridges were still being built long after timber trusses stopped being competitive, and stone arches briefly returned during the Great Depression."
- Claim `CLM_721` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.3.1 Timber Stringer, p. 3-80); SRC_NCHRP_CONTEXT (3.3.1 Timber Stringer, p. 3-80)
- Claim `CLM_738` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.2.1 Stone Arch, p. 3-49)
- Claim `CLM_767` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-133)
- Claim `CLM_777` [EDITORIALLY_APPROVED]: SRC_FHWA_BRIDGE_TYPES (3.0 Economics)
- Shot: SC_073

## B33.s2 (1143.13 s): "And in 2012, a federal handbook still named a kind of beam, the welded plate girder, as the most common steel bridge."
- Claim `CLM_721` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.3.1 Timber Stringer, p. 3-80); SRC_NCHRP_CONTEXT (3.3.1 Timber Stringer, p. 3-80)
- Claim `CLM_738` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.2.1 Stone Arch, p. 3-49)
- Claim `CLM_767` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-133)
- Claim `CLM_777` [EDITORIALLY_APPROVED]: SRC_FHWA_BRIDGE_TYPES (3.0 Economics)
- Shot: SC_073

## B33.s3 (1152.53 s): "At one time, a great number of small suspension bridges were built across the country, simply because they were easy to put up."
- Claim `CLM_721` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.3.1 Timber Stringer, p. 3-80); SRC_NCHRP_CONTEXT (3.3.1 Timber Stringer, p. 3-80)
- Claim `CLM_738` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.2.1 Stone Arch, p. 3-49)
- Claim `CLM_767` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-133)
- Claim `CLM_777` [EDITORIALLY_APPROVED]: SRC_FHWA_BRIDGE_TYPES (3.0 Economics)
- Shot: SC_073

## B33.s4 (1161.78 s): "Each form can still be the right answer in the right place."
- Claim `CLM_721` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.3.1 Timber Stringer, p. 3-80); SRC_NCHRP_CONTEXT (3.3.1 Timber Stringer, p. 3-80)
- Claim `CLM_738` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.2.1 Stone Arch, p. 3-49)
- Claim `CLM_767` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.5 Suspension, p. 3-133)
- Claim `CLM_777` [EDITORIALLY_APPROVED]: SRC_FHWA_BRIDGE_TYPES (3.0 Economics)
- Shot: SC_073

## B34.s0 (1166.98 s): "Next time you cross a bridge, look at its shape."
- Không có claim (câu dẫn dắt).
- Shot: SC_074

## B34.s1 (1170.83 s): "It shows how the load reaches the ground, and something about the people who built it."
- Không có claim (câu dẫn dắt).
- Shot: SC_074

## B34.s2 (1177.01 s): "These models are illustrations, not engineering designs, and the arrows show ideas, not calculated forces."
- Không có claim (câu dẫn dắt).
- Shot: SC_074
- Chú thích `B34_note` NOTE "Models are illustrations, not engineering designs" → SC_074 / bridge_stone_arch_03 / ; 1176.92–1186.54 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B35.s0 (1186.94 s): "Thank you very much for watching."
- Không có claim (câu dẫn dắt).
- Shot: SC_075

## B35.s1 (1189.92 s): "The sources and photo credits are listed in the description."
- Không có claim (câu dẫn dắt).
- Shot: SC_075
