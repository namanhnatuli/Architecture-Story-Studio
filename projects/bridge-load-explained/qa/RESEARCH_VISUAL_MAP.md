# Ánh xạ nghiên cứu → hình ảnh: bridge-load-explained

Sinh bởi `tools/cli.py research-map` từ visual_plan.json, sources.json, timing.json và blender_checks.json. Mỗi dòng: câu → claim → nguồn (vị trí) → asset/bộ phận → chú thích → thời điểm → QA.
Claim nào cũng mới ở mức `SOURCE_VERIFIED`, **chưa được duyệt biên tập**.

## B1.s0 (0.40 s): "What happens when weight is placed on a bridge?"
- Claim `CLM_601` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.365 'live load'); SRC_ODOT_MBI (Glossary p.350 'dead load')
- Claim `CLM_602` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.350 'deck')
- Shot: SC_001

## B1.s1 (4.22 s): "Traffic, people and the weight of the bridge itself all press on its deck."
- Claim `CLM_601` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.365 'live load'); SRC_ODOT_MBI (Glossary p.350 'dead load')
- Claim `CLM_602` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.350 'deck')
- Shot: SC_001
- Chú thích `B1_load` LOAD_ARROW "Load" → SC_001 / bridge_steel_truss_pratt_01 / steel_truss_bridge_span1_deck, steel_truss_bridge_span2_deck; 4.12–15.96 s; claim CLM_601; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B1.s2 (10.22 s): "To stay standing, the bridge has to carry that load down into the ground."
- Claim `CLM_601` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.365 'live load'); SRC_ODOT_MBI (Glossary p.350 'dead load')
- Claim `CLM_602` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.350 'deck')
- Shot: SC_001
- Chú thích `B1_ground` COMPONENT_LABEL "Ground" → SC_001 / site_river_crossing_24 / bank_right; 10.12–15.96 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B2.s0 (16.69 s): "The load follows a path down through the structure."
- Claim `CLM_602` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.350 'deck')
- Claim `CLM_603` [SOURCE_VERIFIED]: SRC_FHWA_PBES_CH2 (Chapter 2 introduction (AASHTO definition)); SRC_FHWA_PBES_GLOSSARY (Appendix E 'superstructure')
- Claim `CLM_604` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.383 'substructure'); SRC_ODOT_MBI (Glossary p.338 'abutment'); SRC_ODOT_MBI (Glossary p.370 'pier')
- Shot: SC_002
- Chú thích `B2_path` CONCEPTUAL_LOAD_PATH → SC_002 / bridge_steel_truss_pratt_01 / steel_truss_bridge_pier1, steel_truss_bridge_seat_left, steel_truss_bridge_seat_right …; 16.58–38.12 s; claim CLM_604; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B2.s1 (20.74 s): "The deck is carried by the superstructure, the part of the bridge that spans the gap."
- Claim `CLM_602` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.350 'deck')
- Claim `CLM_603` [SOURCE_VERIFIED]: SRC_FHWA_PBES_CH2 (Chapter 2 introduction (AASHTO definition)); SRC_FHWA_PBES_GLOSSARY (Appendix E 'superstructure')
- Claim `CLM_604` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.383 'substructure'); SRC_ODOT_MBI (Glossary p.338 'abutment'); SRC_ODOT_MBI (Glossary p.370 'pier')
- Shot: SC_002
- Chú thích `B2_super` HIGHLIGHT_REGION "Superstructure" → SC_002 / bridge_steel_truss_pratt_01 / steel_truss_bridge_span1_chords_north, steel_truss_bridge_span1_chords_south, steel_truss_bridge_span1_deck …; 20.62–26.62 s; claim CLM_603; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B2.s2 (26.74 s): "That rests on the substructure: abutments at the ends, and sometimes piers in between."
- Claim `CLM_602` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.350 'deck')
- Claim `CLM_603` [SOURCE_VERIFIED]: SRC_FHWA_PBES_CH2 (Chapter 2 introduction (AASHTO definition)); SRC_FHWA_PBES_GLOSSARY (Appendix E 'superstructure')
- Claim `CLM_604` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.383 'substructure'); SRC_ODOT_MBI (Glossary p.338 'abutment'); SRC_ODOT_MBI (Glossary p.370 'pier')
- Shot: SC_002
- Chú thích `B2_abut` COMPONENT_LABEL "Abutment" → SC_002 / bridge_steel_truss_pratt_01 / steel_truss_bridge_seat_left; 26.62–38.12 s; claim CLM_604; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS
- Chú thích `B2_pier` COMPONENT_LABEL "Pier" → SC_002 / bridge_steel_truss_pratt_01 / steel_truss_bridge_pier1; 26.62–38.12 s; claim CLM_604; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B2.s3 (33.29 s): "The abutments pass the load on to the foundations."
- Claim `CLM_602` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.350 'deck')
- Claim `CLM_603` [SOURCE_VERIFIED]: SRC_FHWA_PBES_CH2 (Chapter 2 introduction (AASHTO definition)); SRC_FHWA_PBES_GLOSSARY (Appendix E 'superstructure')
- Claim `CLM_604` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.383 'substructure'); SRC_ODOT_MBI (Glossary p.338 'abutment'); SRC_ODOT_MBI (Glossary p.370 'pier')
- Shot: SC_002
- Chú thích `B2_found` COMPONENT_LABEL "Foundation" → SC_002 / bridge_steel_truss_pratt_01 / steel_truss_bridge_seat_left; 33.21–38.12 s; claim CLM_604; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B3.s0 (38.52 s): "Now take a beam bridge."
- Claim `CLM_605` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.341 'beam')
- Claim `CLM_606` [SOURCE_VERIFIED]: SRC_FHWA_CBM (Chapter 2, 'Component Terminology'); SRC_ODOT_MBI (Glossary p.358 'girder')
- Claim `CLM_607` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.344 'cap'); SRC_ODOT_MBI (Glossary p.341 'bent'); SRC_ODOT_MBI (Glossary p.346 'column')
- Shot: SC_003

## B3.s1 (41.30 s): "Its deck rests on long beams that span from one support to the next."
- Claim `CLM_605` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.341 'beam')
- Claim `CLM_606` [SOURCE_VERIFIED]: SRC_FHWA_CBM (Chapter 2, 'Component Terminology'); SRC_ODOT_MBI (Glossary p.358 'girder')
- Claim `CLM_607` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.344 'cap'); SRC_ODOT_MBI (Glossary p.341 'bent'); SRC_ODOT_MBI (Glossary p.346 'column')
- Shot: SC_003
- Chú thích `B3_beams` COMPONENT_LABEL "Beams" → SC_003 / bridge_timber_beam_01 / timber_beam_bridge_span3_stringers; 41.21–51.33 s; claim CLM_605; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B3.s2 (47.10 s): "Each beam carries the load by resisting bending."
- Claim `CLM_601` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.365 'live load'); SRC_ODOT_MBI (Glossary p.350 'dead load')
- Claim `CLM_605` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.341 'beam')
- Claim `CLM_606` [SOURCE_VERIFIED]: SRC_FHWA_CBM (Chapter 2, 'Component Terminology'); SRC_ODOT_MBI (Glossary p.358 'girder')
- Claim `CLM_607` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.344 'cap'); SRC_ODOT_MBI (Glossary p.341 'bent'); SRC_ODOT_MBI (Glossary p.346 'column')
- Shot: SC_003
- Chú thích `B3_load` LOAD_ARROW "Load" → SC_003 / bridge_timber_beam_01 / timber_beam_bridge_span3_planks; 47.00–58.38 s; claim CLM_601; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS
- Chú thích `B3_bend` CALLOUT "Resists bending" → SC_003 / bridge_timber_beam_01 / timber_beam_bridge_span3_stringers; 47.00–58.38 s; claim CLM_606; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B3.s3 (51.42 s): "A cap beam spreads the load onto the posts, and the posts carry it down in compression."
- Claim `CLM_605` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.341 'beam')
- Claim `CLM_606` [SOURCE_VERIFIED]: SRC_FHWA_CBM (Chapter 2, 'Component Terminology'); SRC_ODOT_MBI (Glossary p.358 'girder')
- Claim `CLM_607` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.344 'cap'); SRC_ODOT_MBI (Glossary p.341 'bent'); SRC_ODOT_MBI (Glossary p.346 'column')
- Shot: SC_003
- Chú thích `B3_path` CONCEPTUAL_LOAD_PATH → SC_003 / bridge_timber_beam_01 / timber_beam_bridge_bent3, timber_beam_bridge_bent3_cap, timber_beam_bridge_span3_planks; 51.33–58.38 s; claim CLM_607; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS
- Chú thích `B3_cap` COMPONENT_LABEL "Cap beam" → SC_003 / bridge_timber_beam_01 / timber_beam_bridge_bent3_cap; 51.33–58.38 s; claim CLM_607; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS
- Chú thích `B3_posts` CALLOUT "Posts: compression" → SC_003 / bridge_timber_beam_01 / timber_beam_bridge_bent3; 51.33–58.38 s; claim CLM_607; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B4.s0 (58.77 s): "A masonry arch works differently."
- Claim `CLM_608` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.388 'voussoir'); SRC_ODOT_MBI (Glossary p.363 'keystone')
- Shot: SC_004, SC_005

## B4.s1 (62.08 s): "It is built from wedge-shaped stones called voussoirs, with a keystone at the crown."
- Claim `CLM_608` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.388 'voussoir'); SRC_ODOT_MBI (Glossary p.363 'keystone')
- Shot: SC_004, SC_005
- Chú thích `B4_key` COMPONENT_LABEL "Keystone" → SC_005 / bridge_stone_arch_03 / stone_arch_bridge_arch2_keystone; 63.29–67.25 s; claim CLM_608; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS
- Chú thích `B4_vous` COMPONENT_LABEL "Voussoirs" → SC_005 / bridge_stone_arch_03 / stone_arch_bridge_arch2_voussoir01; 63.46–67.08 s; claim CLM_608; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B5.s0 (68.90 s): "The curve turns the downward load into thrust along the arch, pressing the stones together."
- Claim `CLM_609` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Part 2 Ratings, Item 25 Arch, p.144 (manual p.2-56)); SRC_ODOT_MBI (Glossary p.339 'arch'); SRC_YALE_PHYSICS ('Arch Bridges' section)
- Claim `CLM_610` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.339 'arch'); SRC_YALE_PHYSICS ('Arch Bridges' section)
- Shot: SC_006
- Chú thích `B5_load` LOAD_ARROW "Load" → SC_006 / bridge_stone_arch_03 / stone_arch_bridge_arch2_keystone; 68.79–85.88 s; claim CLM_609; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS
- Chú thích `B5_thrust` CONCEPTUAL_LOAD_PATH → SC_006 / bridge_stone_arch_03 / stone_arch_bridge_arch2_keystone, stone_arch_bridge_arch2_voussoir01, stone_arch_bridge_arch2_voussoir02 …; 68.79–85.88 s; claim CLM_609; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B5.s1 (75.53 s): "So the arch works mainly in compression."
- Claim `CLM_609` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Part 2 Ratings, Item 25 Arch, p.144 (manual p.2-56)); SRC_ODOT_MBI (Glossary p.339 'arch'); SRC_YALE_PHYSICS ('Arch Bridges' section)
- Claim `CLM_610` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.339 'arch'); SRC_YALE_PHYSICS ('Arch Bridges' section)
- Shot: SC_006
- Chú thích `B5_comp` CALLOUT "Mainly compression" → SC_006 / bridge_stone_arch_03 / stone_arch_bridge_arch2_keystone, stone_arch_bridge_arch2_voussoir01, stone_arch_bridge_arch2_voussoir02 …; 75.42–85.88 s; claim CLM_609; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B5.s2 (79.35 s): "At each end it pushes outward and down on its supports, and the supports push back."
- Claim `CLM_609` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Part 2 Ratings, Item 25 Arch, p.144 (manual p.2-56)); SRC_ODOT_MBI (Glossary p.339 'arch'); SRC_YALE_PHYSICS ('Arch Bridges' section)
- Claim `CLM_610` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.339 'arch'); SRC_YALE_PHYSICS ('Arch Bridges' section)
- Shot: SC_006
- Chú thích `B5_react` REACTION_ARROW "Supports push back" → SC_006 / bridge_stone_arch_03 / stone_arch_bridge_arch2_keystone, stone_arch_bridge_arch2_voussoir01, stone_arch_bridge_arch2_voussoir02 …; 79.25–85.88 s; claim CLM_610; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B6.s0 (86.28 s): "The truss we started with takes another approach: straight members joined into triangles."
- Claim `CLM_611` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.386 'truss'); SRC_SCI_TRUSSES (Introduction)
- Claim `CLM_612` [SOURCE_VERIFIED]: SRC_SCI_TRUSSES (Introduction); SRC_FHWA_CBM (Chapter 2, 'Component Terminology')
- Claim `CLM_613` [SOURCE_VERIFIED]: SRC_FHWA_CBM (Chapter 2, 'Component Terminology'); SRC_SCI_TRUSSES ('Types of trusses')
- Claim `CLM_614` [SOURCE_VERIFIED]: SRC_FHWA_CBM (Chapter 2, 'Component Terminology')
- Shot: SC_007
- Chú thích `B6_joints` COMPONENT_LABEL "Joints" → SC_007 / bridge_steel_truss_pratt_01 / steel_truss_bridge_span1_joints_south; 86.17–99.62 s; claim CLM_611; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B6.s1 (92.95 s): "Each member is mainly pulled or pushed along its length, in tension or in compression."
- Claim `CLM_611` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.386 'truss'); SRC_SCI_TRUSSES (Introduction)
- Claim `CLM_612` [SOURCE_VERIFIED]: SRC_SCI_TRUSSES (Introduction); SRC_FHWA_CBM (Chapter 2, 'Component Terminology')
- Claim `CLM_613` [SOURCE_VERIFIED]: SRC_FHWA_CBM (Chapter 2, 'Component Terminology'); SRC_SCI_TRUSSES ('Types of trusses')
- Claim `CLM_614` [SOURCE_VERIFIED]: SRC_FHWA_CBM (Chapter 2, 'Component Terminology')
- Shot: SC_007
- Chú thích `B6_legend` TENSION_COMPRESSION_LEGEND → SC_007 / bridge_steel_truss_pratt_01 / ; 92.83–114.62 s; claim CLM_612; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B6.s2 (99.72 s): "Each span here is a simple span, so under a downward load its top chord is squeezed and its bottom chord is stretched."
- Claim `CLM_611` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.386 'truss'); SRC_SCI_TRUSSES (Introduction)
- Claim `CLM_612` [SOURCE_VERIFIED]: SRC_SCI_TRUSSES (Introduction); SRC_FHWA_CBM (Chapter 2, 'Component Terminology')
- Claim `CLM_613` [SOURCE_VERIFIED]: SRC_FHWA_CBM (Chapter 2, 'Component Terminology'); SRC_SCI_TRUSSES ('Types of trusses')
- Claim `CLM_614` [SOURCE_VERIFIED]: SRC_FHWA_CBM (Chapter 2, 'Component Terminology')
- Shot: SC_007
- Chú thích `B6_top` CALLOUT "Top chord: compression" → SC_007 / bridge_steel_truss_pratt_01 / steel_truss_bridge_span1_chords_south; 99.62–114.62 s; claim CLM_613; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS
- Chú thích `B6_bottom` CALLOUT "Bottom chord: tension" → SC_007 / bridge_steel_truss_pratt_01 / steel_truss_bridge_span1_chords_south; 99.62–114.62 s; claim CLM_613; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B6.s3 (108.42 s): "Inside, some web members are in compression and others are in tension."
- Claim `CLM_611` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.386 'truss'); SRC_SCI_TRUSSES (Introduction)
- Claim `CLM_612` [SOURCE_VERIFIED]: SRC_SCI_TRUSSES (Introduction); SRC_FHWA_CBM (Chapter 2, 'Component Terminology')
- Claim `CLM_613` [SOURCE_VERIFIED]: SRC_FHWA_CBM (Chapter 2, 'Component Terminology'); SRC_SCI_TRUSSES ('Types of trusses')
- Claim `CLM_614` [SOURCE_VERIFIED]: SRC_FHWA_CBM (Chapter 2, 'Component Terminology')
- Shot: SC_007
- Chú thích `B6_web` COMPONENT_LABEL "Web members" → SC_007 / bridge_steel_truss_pratt_01 / steel_truss_bridge_span2_diagonals_south; 108.33–114.62 s; claim CLM_614; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B7.s0 (115.03 s): "Let's compare them one at a time."
- Claim `CLM_606` [SOURCE_VERIFIED]: SRC_FHWA_CBM (Chapter 2, 'Component Terminology'); SRC_ODOT_MBI (Glossary p.358 'girder')
- Claim `CLM_609` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Part 2 Ratings, Item 25 Arch, p.144 (manual p.2-56)); SRC_ODOT_MBI (Glossary p.339 'arch'); SRC_YALE_PHYSICS ('Arch Bridges' section)
- Claim `CLM_612` [SOURCE_VERIFIED]: SRC_SCI_TRUSSES (Introduction); SRC_FHWA_CBM (Chapter 2, 'Component Terminology')
- Shot: SC_008, SC_009, SC_010

## B7.s1 (118.50 s): "The beam bridge carries its load by bending."
- Claim `CLM_606` [SOURCE_VERIFIED]: SRC_FHWA_CBM (Chapter 2, 'Component Terminology'); SRC_ODOT_MBI (Glossary p.358 'girder')
- Claim `CLM_609` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Part 2 Ratings, Item 25 Arch, p.144 (manual p.2-56)); SRC_ODOT_MBI (Glossary p.339 'arch'); SRC_YALE_PHYSICS ('Arch Bridges' section)
- Claim `CLM_612` [SOURCE_VERIFIED]: SRC_SCI_TRUSSES (Introduction); SRC_FHWA_CBM (Chapter 2, 'Component Terminology')
- Shot: SC_008, SC_009, SC_010
- Chú thích `B7_beam` CALLOUT "Bending" → SC_008 / bridge_timber_beam_01 / timber_beam_bridge_span3_stringers; 118.42–122.33 s; claim CLM_606; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B7.s2 (122.53 s): "The arch carries it mainly in compression, pushing against its supports."
- Claim `CLM_606` [SOURCE_VERIFIED]: SRC_FHWA_CBM (Chapter 2, 'Component Terminology'); SRC_ODOT_MBI (Glossary p.358 'girder')
- Claim `CLM_609` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Part 2 Ratings, Item 25 Arch, p.144 (manual p.2-56)); SRC_ODOT_MBI (Glossary p.339 'arch'); SRC_YALE_PHYSICS ('Arch Bridges' section)
- Claim `CLM_612` [SOURCE_VERIFIED]: SRC_SCI_TRUSSES (Introduction); SRC_FHWA_CBM (Chapter 2, 'Component Terminology')
- Shot: SC_008, SC_009, SC_010
- Chú thích `B7_arch` CALLOUT "Compression" → SC_009 / bridge_stone_arch_03 / stone_arch_bridge_arch2_keystone, stone_arch_bridge_arch2_voussoir01, stone_arch_bridge_arch2_voussoir02 …; 122.42–127.83 s; claim CLM_609; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B7.s3 (128.03 s): "In the truss, the load is shared between members in tension and in compression."
- Claim `CLM_606` [SOURCE_VERIFIED]: SRC_FHWA_CBM (Chapter 2, 'Component Terminology'); SRC_ODOT_MBI (Glossary p.358 'girder')
- Claim `CLM_609` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Part 2 Ratings, Item 25 Arch, p.144 (manual p.2-56)); SRC_ODOT_MBI (Glossary p.339 'arch'); SRC_YALE_PHYSICS ('Arch Bridges' section)
- Claim `CLM_612` [SOURCE_VERIFIED]: SRC_SCI_TRUSSES (Introduction); SRC_FHWA_CBM (Chapter 2, 'Component Terminology')
- Shot: SC_008, SC_009, SC_010
- Chú thích `B7_truss` CALLOUT "Tension and compression" → SC_010 / bridge_steel_truss_pratt_01 / steel_truss_bridge_span1_chords_south; 127.92–134.58 s; claim CLM_612; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B8.s0 (134.98 s): "Three arrangements of parts, one job: carrying the load across the gap and down into the ground."
- Không có claim (câu dẫn dắt).
- Shot: SC_011

## B8.s1 (142.16 s): "These models are illustrations, not engineering designs, and the arrows show ideas, not calculated forces."
- Không có claim (câu dẫn dắt).
- Shot: SC_011
