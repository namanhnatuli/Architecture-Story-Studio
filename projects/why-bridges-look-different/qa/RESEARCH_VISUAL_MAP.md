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

## B02.s0 (16.15 s): "So why don't bridges all look the same?"
- Không có claim (câu dẫn dắt).
- Shot: SC_005

## B02.s1 (19.52 s): "It isn't because one design is simply better than the others."
- Không có claim (câu dẫn dắt).
- Shot: SC_005

## B02.s2 (24.32 s): "Each form is a different answer to the same problem, shaped by materials, by the site, and by the time it was built in."
- Không có claim (câu dẫn dắt).
- Shot: SC_005

## B03.s0 (34.02 s): "Every bridge has the same basic job."
- Claim `CLM_701` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Glossary p.365 'live load'); SRC_ODOT_MBI (Glossary p.350 'dead load')
- Claim `CLM_702` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Glossary p.350 'deck')
- Shot: SC_006
- Chú thích `B03_ch` NOTE "2 · The problem every bridge must solve" → SC_006 / bridge_steel_truss_pratt_01 / ; 33.92–43.75 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B03.s1 (37.67 s): "It has to carry loads: the traffic crossing it, and the weight of the bridge itself."
- Claim `CLM_701` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Glossary p.365 'live load'); SRC_ODOT_MBI (Glossary p.350 'dead load')
- Claim `CLM_702` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Glossary p.350 'deck')
- Shot: SC_006
- Chú thích `B03_load` LOAD_ARROW "Load" → SC_006 / bridge_steel_truss_pratt_01 / steel_truss_bridge_span1_deck, steel_truss_bridge_span2_deck; 37.58–48.92 s; claim CLM_701; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B03.s2 (43.85 s): "And it has to pass all of that down into the ground on either side."
- Claim `CLM_701` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Glossary p.365 'live load'); SRC_ODOT_MBI (Glossary p.350 'dead load')
- Claim `CLM_702` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Glossary p.350 'deck')
- Shot: SC_006
- Chú thích `B03_ground` COMPONENT_LABEL "Ground" → SC_006 / site_river_crossing_24 / bank_right; 43.75–48.92 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B04.s0 (49.65 s): "Engineers often describe a bridge in two parts."
- Claim `CLM_702` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Glossary p.350 'deck')
- Claim `CLM_703` [EDITORIALLY_APPROVED]: SRC_FHWA_PBES_CH2 (Chapter 2 introduction (AASHTO definition)); SRC_FHWA_PBES_GLOSSARY (Appendix E 'superstructure')
- Claim `CLM_704` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Glossary p.383 'substructure'); SRC_ODOT_MBI (Glossary p.338 'abutment'); SRC_ODOT_MBI (Glossary p.370 'pier')
- Shot: SC_007

## B04.s1 (53.90 s): "The superstructure is the part that spans the gap, including the deck."
- Claim `CLM_702` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Glossary p.350 'deck')
- Claim `CLM_703` [EDITORIALLY_APPROVED]: SRC_FHWA_PBES_CH2 (Chapter 2 introduction (AASHTO definition)); SRC_FHWA_PBES_GLOSSARY (Appendix E 'superstructure')
- Claim `CLM_704` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Glossary p.383 'substructure'); SRC_ODOT_MBI (Glossary p.338 'abutment'); SRC_ODOT_MBI (Glossary p.370 'pier')
- Shot: SC_007
- Chú thích `B04_super` HIGHLIGHT_REGION "Superstructure" → SC_007 / bridge_steel_truss_pratt_01 / steel_truss_bridge_span1_chords_north, steel_truss_bridge_span1_chords_south, steel_truss_bridge_span1_deck …; 53.79–59.21 s; claim CLM_703; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B04.s2 (59.33 s): "The substructure is what holds it up: abutments at the ends, and sometimes piers in between."
- Claim `CLM_702` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Glossary p.350 'deck')
- Claim `CLM_703` [EDITORIALLY_APPROVED]: SRC_FHWA_PBES_CH2 (Chapter 2 introduction (AASHTO definition)); SRC_FHWA_PBES_GLOSSARY (Appendix E 'superstructure')
- Claim `CLM_704` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Glossary p.383 'substructure'); SRC_ODOT_MBI (Glossary p.338 'abutment'); SRC_ODOT_MBI (Glossary p.370 'pier')
- Shot: SC_007
- Chú thích `B04_abut` COMPONENT_LABEL "Abutment" → SC_007 / bridge_steel_truss_pratt_01 / steel_truss_bridge_seat_left; 59.21–72.75 s; claim CLM_704; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS
- Chú thích `B04_pier` COMPONENT_LABEL "Pier" → SC_007 / bridge_steel_truss_pratt_01 / steel_truss_bridge_pier1; 59.21–72.75 s; claim CLM_704; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B04.s3 (66.50 s): "Load follows a path from the deck, through both parts, into the foundations."
- Claim `CLM_702` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Glossary p.350 'deck')
- Claim `CLM_703` [EDITORIALLY_APPROVED]: SRC_FHWA_PBES_CH2 (Chapter 2 introduction (AASHTO definition)); SRC_FHWA_PBES_GLOSSARY (Appendix E 'superstructure')
- Claim `CLM_704` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Glossary p.383 'substructure'); SRC_ODOT_MBI (Glossary p.338 'abutment'); SRC_ODOT_MBI (Glossary p.370 'pier')
- Shot: SC_007
- Chú thích `B04_path` CONCEPTUAL_LOAD_PATH → SC_007 / bridge_steel_truss_pratt_01 / steel_truss_bridge_pier1, steel_truss_bridge_seat_left, steel_truss_bridge_seat_right …; 66.42–72.75 s; claim CLM_704; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS
- Chú thích `B04_found` COMPONENT_LABEL "Foundation" → SC_007 / bridge_steel_truss_pratt_01 / steel_truss_bridge_seat_left; 66.42–72.75 s; claim CLM_704; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B05.s0 (73.15 s): "What changes from one bridge to the next is how that path is arranged."
- Không có claim (câu dẫn dắt).
- Shot: SC_008

## B05.s1 (78.33 s): "So let's start again with an empty gap."
- Không có claim (câu dẫn dắt).
- Shot: SC_008

## B06.s0 (82.61 s): "The first answer is the beam."
- Claim `CLM_705` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Glossary p.341 'beam')
- Claim `CLM_720` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.3.1 Timber Stringer, p. 3-80)
- Shot: SC_009, SC_010
- Chú thích `B06_ch` NOTE "3 · The beam" → SC_009 / bridge_timber_beam_01 / ; 82.50–91.25 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS
- Chú thích `B06_ch` NOTE "3 · The beam" → SC_010 / bridge_timber_beam_01 / ; 91.58–96.00 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B06.s1 (85.61 s): "Lay a strong member across the gap, support it at each end, and you have a bridge."
- Claim `CLM_705` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Glossary p.341 'beam')
- Claim `CLM_720` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.3.1 Timber Stringer, p. 3-80)
- Shot: SC_009, SC_010

## B06.s2 (91.78 s): "It is one of the oldest ideas in bridge building."
- Claim `CLM_705` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Glossary p.341 'beam')
- Claim `CLM_720` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.3.1 Timber Stringer, p. 3-80)
- Shot: SC_009, SC_010

## B07.s0 (96.73 s): "This timber bridge is a row of short beam spans."
- Claim `CLM_705` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Glossary p.341 'beam')
- Claim `CLM_707` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Glossary p.344 'cap'); SRC_ODOT_MBI (Glossary p.341 'bent'); SRC_ODOT_MBI (Glossary p.346 'column')
- Shot: SC_011, SC_012

## B07.s1 (100.96 s): "Planks form the deck, long beams carry the planks, cap beams carry the beams, and posts carry the caps."
- Claim `CLM_705` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Glossary p.341 'beam')
- Claim `CLM_707` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Glossary p.344 'cap'); SRC_ODOT_MBI (Glossary p.341 'bent'); SRC_ODOT_MBI (Glossary p.346 'column')
- Shot: SC_011, SC_012

## B08.s0 (109.48 s): "Each beam carries its load by resisting bending."
- Claim `CLM_701` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Glossary p.365 'live load'); SRC_ODOT_MBI (Glossary p.350 'dead load')
- Claim `CLM_706` [EDITORIALLY_APPROVED]: SRC_FHWA_CBM (Chapter 2, 'Component Terminology'); SRC_ODOT_MBI (Glossary p.358 'girder')
- Claim `CLM_707` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Glossary p.344 'cap'); SRC_ODOT_MBI (Glossary p.341 'bent'); SRC_ODOT_MBI (Glossary p.346 'column')
- Shot: SC_013
- Chú thích `B08_load` LOAD_ARROW "Load" → SC_013 / bridge_timber_beam_01 / timber_beam_bridge_span3_planks; 109.38–123.67 s; claim CLM_701; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS
- Chú thích `B08_bend` CALLOUT "Beam resists bending" → SC_013 / bridge_timber_beam_01 / timber_beam_bridge_span3_stringers; 109.38–113.67 s; claim CLM_706; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B08.s1 (113.76 s): "At each support, a cap beam spreads the load onto the posts."
- Claim `CLM_706` [EDITORIALLY_APPROVED]: SRC_FHWA_CBM (Chapter 2, 'Component Terminology'); SRC_ODOT_MBI (Glossary p.358 'girder')
- Claim `CLM_707` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Glossary p.344 'cap'); SRC_ODOT_MBI (Glossary p.341 'bent'); SRC_ODOT_MBI (Glossary p.346 'column')
- Shot: SC_013
- Chú thích `B08_path` CONCEPTUAL_LOAD_PATH → SC_013 / bridge_timber_beam_01 / timber_beam_bridge_bent3, timber_beam_bridge_bent3_cap, timber_beam_bridge_span3_planks; 113.67–123.67 s; claim CLM_707; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS
- Chú thích `B08_cap` COMPONENT_LABEL "Cap beam" → SC_013 / bridge_timber_beam_01 / timber_beam_bridge_bent3_cap; 113.67–123.67 s; claim CLM_707; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B08.s2 (118.68 s): "The posts then carry it down into the ground in compression."
- Claim `CLM_706` [EDITORIALLY_APPROVED]: SRC_FHWA_CBM (Chapter 2, 'Component Terminology'); SRC_ODOT_MBI (Glossary p.358 'girder')
- Claim `CLM_707` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Glossary p.344 'cap'); SRC_ODOT_MBI (Glossary p.341 'bent'); SRC_ODOT_MBI (Glossary p.346 'column')
- Shot: SC_013
- Chú thích `B08_posts` CALLOUT "Posts: compression" → SC_013 / bridge_timber_beam_01 / timber_beam_bridge_bent3; 118.58–123.67 s; claim CLM_707; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B09.s0 (124.40 s): "Beams are simple, and wood was usually easy to find."
- Claim `CLM_721` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.3.1 Timber Stringer, p. 3-80); SRC_NCHRP_CONTEXT (3.3.1 Timber Stringer, p. 3-80)
- Claim `CLM_722` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2 (North Dakota, quoted), p. 2-9)
- Shot: SC_014
- Chú thích `B09_note` NOTE "Illustrative model" → SC_014 / bridge_timber_beam_01 / ; 124.29–148.88 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B09.s1 (129.32 s): "That is why timber beam bridges were still being built long after timber trusses fell out of use, and why they are still built on quiet rural roads and in parks today."
- Claim `CLM_721` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.3.1 Timber Stringer, p. 3-80); SRC_NCHRP_CONTEXT (3.3.1 Timber Stringer, p. 3-80)
- Claim `CLM_722` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2 (North Dakota, quoted), p. 2-9)
- Shot: SC_014

## B09.s2 (140.70 s): "But many early timber bridges had relatively short spans, which is why this one needs so many posts."
- Claim `CLM_721` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.3.1 Timber Stringer, p. 3-80); SRC_NCHRP_CONTEXT (3.3.1 Timber Stringer, p. 3-80)
- Claim `CLM_722` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2 (North Dakota, quoted), p. 2-9)
- Shot: SC_014

## B10.s0 (149.28 s): "A masonry arch takes a different approach."
- Claim `CLM_708` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Glossary p.388 'voussoir'); SRC_ODOT_MBI (Glossary p.363 'keystone')
- Shot: SC_015, SC_016
- Chú thích `B10_ch` NOTE "4 · The arch" → SC_015 / bridge_stone_arch_03 / ; 149.17–152.67 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B10.s1 (152.85 s): "It is built from wedge-shaped stones called voussoirs, with a keystone at the crown."
- Claim `CLM_708` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Glossary p.388 'voussoir'); SRC_ODOT_MBI (Glossary p.363 'keystone')
- Shot: SC_015, SC_016
- Chú thích `B10_key` COMPONENT_LABEL "Keystone" → SC_016 / bridge_stone_arch_03 / stone_arch_bridge_arch2_keystone; 154.08–158.21 s; claim CLM_708; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS
- Chú thích `B10_vous` COMPONENT_LABEL "Voussoirs" → SC_016 / bridge_stone_arch_03 / stone_arch_bridge_arch2_voussoir01; 154.25–158.04 s; claim CLM_708; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B11.s0 (159.86 s): "The curve turns the downward load into thrust along the arch, pressing the stones together."
- Claim `CLM_709` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Part 2 Ratings, Item 25 Arch, p.144 (manual p.2-56)); SRC_ODOT_MBI (Glossary p.339 'arch'); SRC_YALE_PHYSICS ('Arch Bridges' section)
- Claim `CLM_710` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Glossary p.339 'arch'); SRC_YALE_PHYSICS ('Arch Bridges' section)
- Shot: SC_017
- Chú thích `B11_load` LOAD_ARROW "Load" → SC_017 / bridge_stone_arch_03 / stone_arch_bridge_arch2_keystone; 159.75–176.71 s; claim CLM_709; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS
- Chú thích `B11_thrust` CONCEPTUAL_LOAD_PATH → SC_017 / bridge_stone_arch_03 / stone_arch_bridge_arch2_keystone, stone_arch_bridge_arch2_voussoir01, stone_arch_bridge_arch2_voussoir02 …; 159.75–176.71 s; claim CLM_709; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B11.s1 (166.56 s): "So the arch works mainly in compression."
- Claim `CLM_709` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Part 2 Ratings, Item 25 Arch, p.144 (manual p.2-56)); SRC_ODOT_MBI (Glossary p.339 'arch'); SRC_YALE_PHYSICS ('Arch Bridges' section)
- Claim `CLM_710` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Glossary p.339 'arch'); SRC_YALE_PHYSICS ('Arch Bridges' section)
- Shot: SC_017
- Chú thích `B11_comp` CALLOUT "Mainly compression" → SC_017 / bridge_stone_arch_03 / stone_arch_bridge_arch2_keystone, stone_arch_bridge_arch2_voussoir01, stone_arch_bridge_arch2_voussoir02 …; 166.46–176.71 s; claim CLM_709; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B11.s2 (170.18 s): "At each end it pushes outward and down on its supports, and the supports push back."
- Claim `CLM_709` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Part 2 Ratings, Item 25 Arch, p.144 (manual p.2-56)); SRC_ODOT_MBI (Glossary p.339 'arch'); SRC_YALE_PHYSICS ('Arch Bridges' section)
- Claim `CLM_710` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Glossary p.339 'arch'); SRC_YALE_PHYSICS ('Arch Bridges' section)
- Shot: SC_017
- Chú thích `B11_react` REACTION_ARROW "Supports push back" → SC_017 / bridge_stone_arch_03 / stone_arch_bridge_arch2_keystone, stone_arch_bridge_arch2_voussoir01, stone_arch_bridge_arch2_voussoir02 …; 170.08–176.71 s; claim CLM_710; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B12.s0 (177.11 s): "That is why arches suit materials that are strong under compression, like stone."
- Claim `CLM_709` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Part 2 Ratings, Item 25 Arch, p.144 (manual p.2-56)); SRC_ODOT_MBI (Glossary p.339 'arch'); SRC_YALE_PHYSICS ('Arch Bridges' section)
- Claim `CLM_710` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Glossary p.339 'arch'); SRC_YALE_PHYSICS ('Arch Bridges' section)
- Claim `CLM_726` [EDITORIALLY_APPROVED]: SRC_YALE_PHYSICS (unit 01.05.08, section 6)
- Shot: SC_018

## B12.s1 (182.98 s): "And it is why the supports matter so much: the abutments have to push inward on the arch, against its thrust."
- Claim `CLM_709` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Part 2 Ratings, Item 25 Arch, p.144 (manual p.2-56)); SRC_ODOT_MBI (Glossary p.339 'arch'); SRC_YALE_PHYSICS ('Arch Bridges' section)
- Claim `CLM_710` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Glossary p.339 'arch'); SRC_YALE_PHYSICS ('Arch Bridges' section)
- Claim `CLM_726` [EDITORIALLY_APPROVED]: SRC_YALE_PHYSICS (unit 01.05.08, section 6)
- Shot: SC_018
- Chú thích `B12_abut` COMPONENT_LABEL "Abutment" → SC_018 / bridge_stone_arch_03 / stone_arch_bridge_abutment_left; 182.88–191.33 s; claim CLM_710; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS
- Chú thích `B12_pier` COMPONENT_LABEL "Pier" → SC_018 / bridge_stone_arch_03 / stone_arch_bridge_pier1; 182.88–191.33 s; claim CLM_710; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B13.s0 (191.73 s): "Building an arch takes support of its own."
- Claim `CLM_723` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.2.1 Stone Arch, p. 3-48)
- Shot: SC_019

## B13.s1 (195.26 s): "While a stone arch is being built, a temporary timber frame called falsework holds the stones in place."
- Claim `CLM_723` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.2.1 Stone Arch, p. 3-48)
- Shot: SC_019

## B13.s2 (203.13 s): "So building one called for carpenters as well as skilled masons."
- Claim `CLM_723` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.2.1 Stone Arch, p. 3-48)
- Shot: SC_019

## B14.s0 (208.98 s): "Stone arches were generally more expensive to build than timber bridges."
- Claim `CLM_724` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.2.1 Stone Arch, p. 3-49)
- Claim `CLM_725` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.2.1 Stone Arch, p. 3-48)
- Shot: SC_020

## B14.s1 (215.03 s): "But stone was the preferred choice where durability and permanence were required, so arches were favoured on busy routes and in important places."
- Claim `CLM_724` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.2.1 Stone Arch, p. 3-49)
- Claim `CLM_725` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.2.1 Stone Arch, p. 3-48)
- Shot: SC_020

## B14.s2 (225.26 s): "Elsewhere, the lower cost of timber made up for its lack of permanence."
- Claim `CLM_724` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.2.1 Stone Arch, p. 3-49)
- Claim `CLM_725` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.2.1 Stone Arch, p. 3-48)
- Shot: SC_020

## B15.s0 (231.32 s): "A third approach is the truss."
- Claim `CLM_711` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Glossary p.386 'truss'); SRC_SCI_TRUSSES (Introduction)
- Claim `CLM_712` [EDITORIALLY_APPROVED]: SRC_SCI_TRUSSES (Introduction); SRC_FHWA_CBM (Chapter 2, 'Component Terminology')
- Shot: SC_021
- Chú thích `B15_ch` NOTE "5 · The truss" → SC_021 / bridge_steel_truss_pratt_01 / ; 231.21–234.17 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B15.s1 (234.27 s): "It builds a structure out of straight members, joined into triangles."
- Claim `CLM_711` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Glossary p.386 'truss'); SRC_SCI_TRUSSES (Introduction)
- Claim `CLM_712` [EDITORIALLY_APPROVED]: SRC_SCI_TRUSSES (Introduction); SRC_FHWA_CBM (Chapter 2, 'Component Terminology')
- Shot: SC_021
- Chú thích `B15_joints` COMPONENT_LABEL "Joints" → SC_021 / bridge_steel_truss_pratt_01 / steel_truss_bridge_span1_joints_south; 234.17–246.83 s; claim CLM_711; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B15.s2 (239.49 s): "Each member is mainly pulled or pushed along its length, in tension or in compression."
- Claim `CLM_711` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Glossary p.386 'truss'); SRC_SCI_TRUSSES (Introduction)
- Claim `CLM_712` [EDITORIALLY_APPROVED]: SRC_SCI_TRUSSES (Introduction); SRC_FHWA_CBM (Chapter 2, 'Component Terminology')
- Shot: SC_021
- Chú thích `B15_legend` TENSION_COMPRESSION_LEGEND → SC_021 / bridge_steel_truss_pratt_01 / ; 239.38–246.83 s; claim CLM_712; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B16.s0 (247.23 s): "In a simple span like these, under a downward load, the top chord is squeezed and the bottom chord is stretched."
- Claim `CLM_712` [EDITORIALLY_APPROVED]: SRC_SCI_TRUSSES (Introduction); SRC_FHWA_CBM (Chapter 2, 'Component Terminology')
- Claim `CLM_713` [EDITORIALLY_APPROVED]: SRC_FHWA_CBM (Chapter 2, 'Component Terminology'); SRC_SCI_TRUSSES ('Types of trusses')
- Claim `CLM_714` [EDITORIALLY_APPROVED]: SRC_FHWA_CBM (Chapter 2, 'Component Terminology')
- Shot: SC_022
- Chú thích `B16_legend` TENSION_COMPRESSION_LEGEND → SC_022 / bridge_steel_truss_pratt_01 / ; 247.12–261.42 s; claim CLM_712; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS
- Chú thích `B16_top` CALLOUT "Top chord: compression" → SC_022 / bridge_steel_truss_pratt_01 / steel_truss_bridge_span1_chords_south; 251.25–261.42 s; claim CLM_713; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS
- Chú thích `B16_bottom` CALLOUT "Bottom chord: tension" → SC_022 / bridge_steel_truss_pratt_01 / steel_truss_bridge_span1_chords_south; 252.79–261.42 s; claim CLM_713; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B16.s1 (255.21 s): "Inside, some web members are in compression and others are in tension."
- Claim `CLM_713` [EDITORIALLY_APPROVED]: SRC_FHWA_CBM (Chapter 2, 'Component Terminology'); SRC_SCI_TRUSSES ('Types of trusses')
- Claim `CLM_714` [EDITORIALLY_APPROVED]: SRC_FHWA_CBM (Chapter 2, 'Component Terminology')
- Shot: SC_022
- Chú thích `B16_web` COMPONENT_LABEL "Web members" → SC_022 / bridge_steel_truss_pratt_01 / steel_truss_bridge_span2_diagonals_south; 255.12–261.42 s; claim CLM_714; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B17.s0 (261.82 s): "The triangles can be arranged in different patterns."
- Claim `CLM_711` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Glossary p.386 'truss'); SRC_SCI_TRUSSES (Introduction)
- Claim `CLM_727` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-7)
- Claim `CLM_728` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-7)
- Shot: SC_023, SC_024, SC_025

## B17.s1 (266.12 s): "This is a Pratt truss."
- Claim `CLM_711` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Glossary p.386 'truss'); SRC_SCI_TRUSSES (Introduction)
- Claim `CLM_727` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-7)
- Claim `CLM_728` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-7)
- Shot: SC_023, SC_024, SC_025
- Chú thích `B17_pratt` NOTE "Pratt truss (patented 1844)" → SC_023 / bridge_steel_truss_pratt_01 / ; 266.00–277.54 s; claim CLM_727; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B17.s2 (268.69 s): "In the original design, patented in 1844, its verticals were timber and its diagonals were iron rods."
- Claim `CLM_711` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Glossary p.386 'truss'); SRC_SCI_TRUSSES (Introduction)
- Claim `CLM_727` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-7)
- Claim `CLM_728` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-7)
- Shot: SC_023, SC_024, SC_025

## B17.s3 (278.07 s): "Swap the web for diagonals that alternate in direction, and you have a Warren truss, patented in 1848."
- Claim `CLM_711` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Glossary p.386 'truss'); SRC_SCI_TRUSSES (Introduction)
- Claim `CLM_727` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-7)
- Claim `CLM_728` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-7)
- Shot: SC_023, SC_024, SC_025
- Chú thích `B17_warren` NOTE "Warren truss (patented 1848)" → SC_024 / bridge_steel_truss_warren_01 / ; 277.96–286.17 s; claim CLM_728; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS
- Chú thích `B17_warren` NOTE "Warren truss (patented 1848)" → SC_025 / bridge_steel_truss_warren_01 / ; 286.50–293.58 s; claim CLM_728; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B17.s4 (286.67 s): "Both patterns carry load through triangles; they simply arrange the members differently."
- Claim `CLM_711` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Glossary p.386 'truss'); SRC_SCI_TRUSSES (Introduction)
- Claim `CLM_727` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-7)
- Claim `CLM_728` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-7)
- Shot: SC_023, SC_024, SC_025

## B18.s0 (293.98 s): "Trusses also changed how bridges were built."
- Claim `CLM_729` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2 'Foundries and Fabricators', p. 2-11)
- Shot: SC_026

## B18.s1 (297.81 s): "By the middle of the nineteenth century, shops were making and drilling truss members, then shipping them to the bridge site, ready to assemble."
- Claim `CLM_729` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2 'Foundries and Fabricators', p. 2-11)
- Shot: SC_026
- Chú thích `B18_shop` NOTE "Members made and drilled in shops" → SC_026 / bridge_steel_truss_pratt_01 / ; 297.71–307.38 s; claim CLM_729; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B18.s2 (307.46 s): "And by 1860, the railroads relied almost entirely on these prefabricated parts."
- Claim `CLM_729` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2 'Foundries and Fabricators', p. 2-11)
- Shot: SC_026
- Chú thích `B18_1860` NOTE "By 1860: prefabricated parts" → SC_026 / bridge_steel_truss_pratt_01 / ; 307.38–315.25 s; claim CLM_729; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B19.s0 (315.65 s): "So which design is best?"
- Không có claim (câu dẫn dắt).
- Shot: SC_027

## B19.s1 (318.45 s): "The honest answer is that it depends."
- Không có claim (câu dẫn dắt).
- Shot: SC_027

## B19.s2 (321.80 s): "Materials, the site, the span, cost, and the skills available all pull in different directions."
- Không có claim (câu dẫn dắt).
- Shot: SC_027

## B20A.s0 (330.07 s): "Start with the materials themselves."
- Claim `CLM_726` [EDITORIALLY_APPROVED]: SRC_YALE_PHYSICS (unit 01.05.08, section 6)
- Shot: SC_028

## B20A.s1 (333.24 s): "An arch needs a material that is strong under compression, and stone is."
- Claim `CLM_726` [EDITORIALLY_APPROVED]: SRC_YALE_PHYSICS (unit 01.05.08, section 6)
- Shot: SC_028
- Chú thích `B20A_note` NOTE "Stone: strong under compression" → SC_028 / bridge_stone_arch_03 / ; 333.12–339.33 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B20B.s0 (339.73 s): "A truss needs members that can work in tension as well as compression."
- Claim `CLM_712` [EDITORIALLY_APPROVED]: SRC_SCI_TRUSSES (Introduction); SRC_FHWA_CBM (Chapter 2, 'Component Terminology')
- Claim `CLM_735` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-8)
- Shot: SC_029
- Chú thích `B20B_note` NOTE "Truss members: tension and compression" → SC_029 / bridge_steel_truss_pratt_01 / ; 339.62–345.38 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B20B.s1 (345.46 s): "Wrought iron was valued for exactly that: one historian calls it a material strong equally in tension and in compression."
- Claim `CLM_712` [EDITORIALLY_APPROVED]: SRC_SCI_TRUSSES (Introduction); SRC_FHWA_CBM (Chapter 2, 'Component Terminology')
- Claim `CLM_735` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-8)
- Shot: SC_029
- Chú thích `B20B_iron` NOTE "Wrought iron: valued in tension and compression" → SC_029 / bridge_steel_truss_pratt_01 / ; 345.38–355.21 s; claim CLM_735; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B20C.s0 (355.61 s): "Wood was often plentiful and cheap, but wooden bridges were vulnerable to decay."
- Claim `CLM_734` [EDITORIALLY_APPROVED]: SRC_ASCE_BOLLMAN (main text)
- Claim `CLM_742` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Shot: SC_030
- Chú thích `B20C_note` NOTE "Timber: plentiful and cheap, but it decays" → SC_030 / bridge_timber_beam_01 / ; 355.50–362.46 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B21.s0 (362.86 s): "That is one reason many timber truss bridges were covered with a roof and siding, to protect them from the weather."
- Claim `CLM_733` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.1.1 King Post, p. 3-7)
- Claim `CLM_746` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (List of figures, 3-5)
- Shot: SC_031

## B21.s1 (371.18 s): "This is the Humpback Covered Bridge, built in 1857 over Dunlap Creek."
- Claim `CLM_733` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.1.1 King Post, p. 3-7)
- Claim `CLM_746` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (List of figures, 3-5)
- Shot: SC_031

## B22.s0 (378.86 s): "The site of a bridge matters too."
- Claim `CLM_736` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.6 Trestles and Viaducts, p. 3-137); SRC_NCHRP_CONTEXT (3.6 Trestles and Viaducts, p. 3-137)
- Shot: SC_032

## B22.s1 (381.93 s): "Railway engines have limited traction, so railways need gentle gradients."
- Claim `CLM_736` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.6 Trestles and Viaducts, p. 3-137); SRC_NCHRP_CONTEXT (3.6 Trestles and Viaducts, p. 3-137)
- Shot: SC_032

## B22.s2 (388.06 s): "Where a valley was too deep and wide to fill with an embankment, engineers built viaducts and trestles to keep the line nearly straight and level."
- Claim `CLM_736` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.6 Trestles and Viaducts, p. 3-137); SRC_NCHRP_CONTEXT (3.6 Trestles and Viaducts, p. 3-137)
- Shot: SC_032

## B23.s0 (398.94 s): "Then there is span: how far a single structure has to reach."
- Không có claim (câu dẫn dắt).
- Shot: SC_033
- Chú thích `B23_note` NOTE "Span: how far one structure reaches" → SC_033 / None / ; 398.83–404.08 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B23B.s0 (404.48 s): "A simple king post truss could span only about thirty feet."
- Claim `CLM_730` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.1 Trusses, p. 3-4)
- Claim `CLM_731` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.1.1 King Post, p. 3-7)
- Claim `CLM_732` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.2.1 Stone Arch, p. 3-48)
- Shot: SC_034

## B23B.s1 (409.33 s): "What one report calls America's greatest stone arch, the Cabin John Aqueduct Bridge, spans 220 feet, and some through trusses approach 400."
- Claim `CLM_730` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.1 Trusses, p. 3-4)
- Claim `CLM_731` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.1.1 King Post, p. 3-7)
- Claim `CLM_732` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.2.1 Stone Arch, p. 3-48)
- Shot: SC_034

## B24.s0 (422.19 s): "Finally, every bridge belongs to its time."
- Claim `CLM_727` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-7)
- Claim `CLM_728` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-7)
- Claim `CLM_729` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2 'Foundries and Fabricators', p. 2-11)
- Claim `CLM_738` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.2.1 Stone Arch, p. 3-49)
- Claim `CLM_739` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Shot: SC_035

## B24.s1 (426.17 s): "As metal trusses spread, skilled masons became fewer and reinforced concrete arrived, stone arch construction declined."
- Claim `CLM_727` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-7)
- Claim `CLM_728` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-7)
- Claim `CLM_729` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2 'Foundries and Fabricators', p. 2-11)
- Claim `CLM_738` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.2.1 Stone Arch, p. 3-49)
- Claim `CLM_739` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Shot: SC_035

## B24.s2 (435.67 s): "Then, during the Great Depression, it briefly returned."
- Claim `CLM_727` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-7)
- Claim `CLM_728` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-7)
- Claim `CLM_729` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2 'Foundries and Fabricators', p. 2-11)
- Claim `CLM_738` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.2.1 Stone Arch, p. 3-49)
- Claim `CLM_739` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Shot: SC_035

## B25.s0 (440.86 s): "These trade-offs played out across nineteenth-century America as the railways spread."
- Claim `CLM_741` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6); SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Claim `CLM_742` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Shot: SC_036

## B25.s1 (447.21 s): "In the East, railroads built massive stone viaducts, while western builders generally used timber."
- Claim `CLM_741` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6); SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Claim `CLM_742` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Shot: SC_036

## B25.s2 (454.98 s): "Three documented examples show how differently builders answered."
- Claim `CLM_741` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6); SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Claim `CLM_742` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Shot: SC_036

## B26.s0 (461.23 s): "Near Baltimore, the Carrollton Viaduct was completed in 1829."
- Claim `CLM_739` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Claim `CLM_740` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.6 Trestles and Viaducts, p. 3-137)
- Shot: SC_037

## B26.s1 (467.31 s): "Built of roughly twelve thousand granite blocks, it carries the railway over Gwynns Falls on an eighty foot arch."
- Claim `CLM_739` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Claim `CLM_740` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.6 Trestles and Viaducts, p. 3-137)
- Shot: SC_037

## B26.s2 (475.73 s): "A national report in 2005 called it the world's oldest stone railroad span still in service."
- Claim `CLM_739` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Claim `CLM_740` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.6 Trestles and Viaducts, p. 3-137)
- Shot: SC_037

## B27.s0 (484.36 s): "Early railroads needed durable bridges to carry heavy trains."
- Claim `CLM_725` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.2.1 Stone Arch, p. 3-48)
- Claim `CLM_741` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6); SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Shot: SC_038
- Chú thích `B27_note` NOTE "Illustrative model, not the Carrollton Viaduct" → SC_038 / bridge_stone_arch_03 / ; 484.25–494.08 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B27.s1 (489.48 s): "For a line meant to last, stone was the answer."
- Claim `CLM_725` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.2.1 Stone Arch, p. 3-48)
- Claim `CLM_741` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6); SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Shot: SC_038

## B28.s0 (494.48 s): "In the West, the pressure was different."
- Claim `CLM_742` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Claim `CLM_743` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (List of figures, 3-106)
- Shot: SC_039

## B28.s1 (497.73 s): "Railroads had to open new lines quickly and economically, and timber was abundant and cheap."
- Claim `CLM_742` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Claim `CLM_743` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (List of figures, 3-106)
- Shot: SC_039

## B28.s2 (504.78 s): "This timber trestle near Corinne, Utah, was built in 1872 by the Central Pacific Railroad."
- Claim `CLM_742` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Claim `CLM_743` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (List of figures, 3-106)
- Shot: SC_039

## B29.s0 (514.23 s): "A trestle is a succession of towers supporting short spans."
- Claim `CLM_737` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.6 Trestles and Viaducts, p. 3-137)
- Shot: SC_040
- Chú thích `B29_note` NOTE "Illustrative model, not the Promontory trestle" → SC_040 / bridge_timber_beam_01 / ; 514.12–526.33 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B29.s1 (519.08 s): "It is the same beam idea as our timber model, repeated as often as the crossing needs."
- Claim `CLM_737` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.6 Trestles and Viaducts, p. 3-137)
- Shot: SC_040

## B30.s0 (526.73 s): "Iron offered a third path."
- Claim `CLM_744` [EDITORIALLY_APPROVED]: SRC_ASCE_BOLLMAN (main text); SRC_ASCE_BOLLMAN (main text)
- Claim `CLM_745` [EDITORIALLY_APPROVED]: SRC_ASCE_BOLLMAN (main text)
- Shot: SC_041

## B30.s1 (529.63 s): "The Bollman truss, patented in 1852, was one of the first designs to use iron in all of its essential structural parts."
- Claim `CLM_744` [EDITORIALLY_APPROVED]: SRC_ASCE_BOLLMAN (main text); SRC_ASCE_BOLLMAN (main text)
- Claim `CLM_745` [EDITORIALLY_APPROVED]: SRC_ASCE_BOLLMAN (main text)
- Shot: SC_041

## B30.s2 (539.58 s): "It could be built relatively quickly and inexpensively, while offering the long-lasting qualities of metal."
- Claim `CLM_744` [EDITORIALLY_APPROVED]: SRC_ASCE_BOLLMAN (main text); SRC_ASCE_BOLLMAN (main text)
- Claim `CLM_745` [EDITORIALLY_APPROVED]: SRC_ASCE_BOLLMAN (main text)
- Shot: SC_041

## B30.s3 (547.28 s): "The bridge at Savage, Maryland, is the only remaining example of the design."
- Claim `CLM_744` [EDITORIALLY_APPROVED]: SRC_ASCE_BOLLMAN (main text); SRC_ASCE_BOLLMAN (main text)
- Claim `CLM_745` [EDITORIALLY_APPROVED]: SRC_ASCE_BOLLMAN (main text)
- Shot: SC_041

## B31.s0 (554.44 s): "Stone for permanence, timber for speed and economy, and iron trusses that offered some of both."
- Claim `CLM_741` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6); SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Claim `CLM_742` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Claim `CLM_744` [EDITORIALLY_APPROVED]: SRC_ASCE_BOLLMAN (main text); SRC_ASCE_BOLLMAN (main text)
- Shot: SC_042

## B31.s1 (561.67 s): "Three places, three sets of constraints, three different bridges."
- Claim `CLM_741` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6); SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Claim `CLM_742` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Claim `CLM_744` [EDITORIALLY_APPROVED]: SRC_ASCE_BOLLMAN (main text); SRC_ASCE_BOLLMAN (main text)
- Shot: SC_042

## B32.s0 (567.52 s): "So why don't bridges all look the same?"
- Claim `CLM_706` [EDITORIALLY_APPROVED]: SRC_FHWA_CBM (Chapter 2, 'Component Terminology'); SRC_ODOT_MBI (Glossary p.358 'girder')
- Claim `CLM_709` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Part 2 Ratings, Item 25 Arch, p.144 (manual p.2-56)); SRC_ODOT_MBI (Glossary p.339 'arch'); SRC_YALE_PHYSICS ('Arch Bridges' section)
- Claim `CLM_712` [EDITORIALLY_APPROVED]: SRC_SCI_TRUSSES (Introduction); SRC_FHWA_CBM (Chapter 2, 'Component Terminology')
- Shot: SC_043
- Chú thích `B32_ch` NOTE "8 · Why they look different" → SC_043 / bridge_steel_truss_pratt_01 / ; 567.42–575.67 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B32.s1 (570.90 s): "Because a bridge's form comes from two things working together."
- Claim `CLM_706` [EDITORIALLY_APPROVED]: SRC_FHWA_CBM (Chapter 2, 'Component Terminology'); SRC_ODOT_MBI (Glossary p.358 'girder')
- Claim `CLM_709` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Part 2 Ratings, Item 25 Arch, p.144 (manual p.2-56)); SRC_ODOT_MBI (Glossary p.339 'arch'); SRC_YALE_PHYSICS ('Arch Bridges' section)
- Claim `CLM_712` [EDITORIALLY_APPROVED]: SRC_SCI_TRUSSES (Introduction); SRC_FHWA_CBM (Chapter 2, 'Component Terminology')
- Shot: SC_043

## B32.s2 (575.77 s): "One is how its structure carries load: beams resist bending, arches work in compression, and trusses share load among members in tension and compression."
- Claim `CLM_706` [EDITORIALLY_APPROVED]: SRC_FHWA_CBM (Chapter 2, 'Component Terminology'); SRC_ODOT_MBI (Glossary p.358 'girder')
- Claim `CLM_709` [EDITORIALLY_APPROVED]: SRC_ODOT_MBI (Part 2 Ratings, Item 25 Arch, p.144 (manual p.2-56)); SRC_ODOT_MBI (Glossary p.339 'arch'); SRC_YALE_PHYSICS ('Arch Bridges' section)
- Claim `CLM_712` [EDITORIALLY_APPROVED]: SRC_SCI_TRUSSES (Introduction); SRC_FHWA_CBM (Chapter 2, 'Component Terminology')
- Shot: SC_043
- Chú thích `B32_one` NOTE "1 · How the structure carries load" → SC_043 / bridge_steel_truss_pratt_01 / ; 575.67–587.58 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B32B.s0 (587.98 s): "The other is the world it was built in: its materials, its site, its span, its budget and its builders."
- Claim `CLM_724` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.2.1 Stone Arch, p. 3-49)
- Claim `CLM_742` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (2.2, p. 2-6)
- Shot: SC_044

## B33.s0 (596.65 s): "And it is not a simple story of progress."
- Claim `CLM_721` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.3.1 Timber Stringer, p. 3-80); SRC_NCHRP_CONTEXT (3.3.1 Timber Stringer, p. 3-80)
- Claim `CLM_738` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.2.1 Stone Arch, p. 3-49)
- Shot: SC_045

## B33.s1 (600.35 s): "Timber beam bridges are still built today, and stone arches briefly returned during the Great Depression."
- Claim `CLM_721` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.3.1 Timber Stringer, p. 3-80); SRC_NCHRP_CONTEXT (3.3.1 Timber Stringer, p. 3-80)
- Claim `CLM_738` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.2.1 Stone Arch, p. 3-49)
- Shot: SC_045

## B33.s2 (607.95 s): "Each form can still be the right answer in the right place."
- Claim `CLM_721` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.3.1 Timber Stringer, p. 3-80); SRC_NCHRP_CONTEXT (3.3.1 Timber Stringer, p. 3-80)
- Claim `CLM_738` [EDITORIALLY_APPROVED]: SRC_NCHRP_CONTEXT (3.2.1 Stone Arch, p. 3-49)
- Shot: SC_045

## B34.s0 (613.15 s): "Next time you cross a bridge, look at its shape."
- Không có claim (câu dẫn dắt).
- Shot: SC_046

## B34.s1 (617.00 s): "It shows how the load reaches the ground, and something about the people who built it."
- Không có claim (câu dẫn dắt).
- Shot: SC_046

## B34.s2 (623.17 s): "These models are illustrations, not engineering designs, and the arrows show ideas, not calculated forces."
- Không có claim (câu dẫn dắt).
- Shot: SC_046
- Chú thích `B34_note` NOTE "Models are illustrations, not engineering designs" → SC_046 / bridge_stone_arch_03 / ; 623.08–632.71 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B35.s0 (633.11 s): "Thank you very much for watching."
- Không có claim (câu dẫn dắt).
- Shot: SC_047

## B35.s1 (636.08 s): "The sources and photo credits are listed in the description."
- Không có claim (câu dẫn dắt).
- Shot: SC_047
