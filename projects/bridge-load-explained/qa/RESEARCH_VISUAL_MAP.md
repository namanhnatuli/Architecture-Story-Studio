# Ánh xạ nghiên cứu → hình ảnh: bridge-load-explained

Sinh bởi `tools/cli.py research-map` từ visual_plan.json, sources.json, timing.json và blender_checks.json. Mỗi dòng: câu → claim → nguồn (vị trí) → asset/bộ phận → chú thích → thời điểm → QA.
Claim nào cũng mới ở mức `SOURCE_VERIFIED`, **chưa được duyệt biên tập**.

## B1.s0 (0.40 s): "What happens when weight is placed on a bridge?"
- Claim `CLM_601` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.365 'live load'); SRC_ODOT_MBI (Glossary p.350 'dead load')
- Claim `CLM_602` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.350 'deck')
- Shot: SC_001

## B1.s1 (3.95 s): "Traffic, people and the bridge's own weight all press down on its deck."
- Claim `CLM_601` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.365 'live load'); SRC_ODOT_MBI (Glossary p.350 'dead load')
- Claim `CLM_602` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.350 'deck')
- Shot: SC_001
- Chú thích `B1_load` LOAD_ARROW "Load" → SC_001 / bridge_steel_truss_pratt_01 / steel_truss_bridge_span1_deck, steel_truss_bridge_span2_deck; 3.83–13.88 s; claim CLM_601; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B1.s2 (8.80 s): "To stay standing, the bridge has to carry that load down into the ground."
- Claim `CLM_601` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.365 'live load'); SRC_ODOT_MBI (Glossary p.350 'dead load')
- Claim `CLM_602` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.350 'deck')
- Shot: SC_001
- Chú thích `B1_ground` COMPONENT_LABEL "Ground" → SC_001 / site_river_crossing_24 / bank_right; 8.71–13.88 s; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B2.s0 (14.61 s): "The load follows a path down through the structure."
- Claim `CLM_602` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.350 'deck')
- Claim `CLM_603` [SOURCE_VERIFIED]: SRC_FHWA_PBES_CH2 (Chapter 2 introduction (AASHTO definition)); SRC_FHWA_PBES_GLOSSARY (Appendix E 'superstructure')
- Claim `CLM_604` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.383 'substructure'); SRC_ODOT_MBI (Glossary p.338 'abutment'); SRC_ODOT_MBI (Glossary p.370 'pier')
- Shot: SC_002
- Chú thích `B2_path` CONCEPTUAL_LOAD_PATH → SC_002 / bridge_steel_truss_pratt_01 / steel_truss_bridge_pier1, steel_truss_bridge_seat_left, steel_truss_bridge_seat_right …; 14.50–34.17 s; claim CLM_604; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B2.s1 (18.26 s): "The deck is carried by the superstructure, the part of the bridge that spans the gap."
- Claim `CLM_602` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.350 'deck')
- Claim `CLM_603` [SOURCE_VERIFIED]: SRC_FHWA_PBES_CH2 (Chapter 2 introduction (AASHTO definition)); SRC_FHWA_PBES_GLOSSARY (Appendix E 'superstructure')
- Claim `CLM_604` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.383 'substructure'); SRC_ODOT_MBI (Glossary p.338 'abutment'); SRC_ODOT_MBI (Glossary p.370 'pier')
- Shot: SC_002
- Chú thích `B2_super` HIGHLIGHT_REGION "Superstructure" → SC_002 / bridge_steel_truss_pratt_01 / steel_truss_bridge_span1_chords_north, steel_truss_bridge_span1_chords_south, steel_truss_bridge_span1_deck …; 18.17–23.71 s; claim CLM_603; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B2.s2 (23.81 s): "That rests on the substructure: abutments at the ends, and sometimes piers in between."
- Claim `CLM_602` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.350 'deck')
- Claim `CLM_603` [SOURCE_VERIFIED]: SRC_FHWA_PBES_CH2 (Chapter 2 introduction (AASHTO definition)); SRC_FHWA_PBES_GLOSSARY (Appendix E 'superstructure')
- Claim `CLM_604` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.383 'substructure'); SRC_ODOT_MBI (Glossary p.338 'abutment'); SRC_ODOT_MBI (Glossary p.370 'pier')
- Shot: SC_002
- Chú thích `B2_abut` COMPONENT_LABEL "Abutment" → SC_002 / bridge_steel_truss_pratt_01 / steel_truss_bridge_seat_left; 23.71–34.17 s; claim CLM_604; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS
- Chú thích `B2_pier` COMPONENT_LABEL "Pier" → SC_002 / bridge_steel_truss_pratt_01 / steel_truss_bridge_pier1; 23.71–34.17 s; claim CLM_604; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B2.s3 (29.81 s): "The abutments pass the load on to the foundations."
- Claim `CLM_602` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.350 'deck')
- Claim `CLM_603` [SOURCE_VERIFIED]: SRC_FHWA_PBES_CH2 (Chapter 2 introduction (AASHTO definition)); SRC_FHWA_PBES_GLOSSARY (Appendix E 'superstructure')
- Claim `CLM_604` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.383 'substructure'); SRC_ODOT_MBI (Glossary p.338 'abutment'); SRC_ODOT_MBI (Glossary p.370 'pier')
- Shot: SC_002
- Chú thích `B2_found` COMPONENT_LABEL "Foundation" → SC_002 / bridge_steel_truss_pratt_01 / steel_truss_bridge_seat_left; 29.71–34.17 s; claim CLM_604; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B3.s0 (34.57 s): "Now take a beam bridge."
- Claim `CLM_605` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.341 'beam')
- Claim `CLM_606` [SOURCE_VERIFIED]: SRC_FHWA_CBM (Chapter 2, 'Component Terminology'); SRC_ODOT_MBI (Glossary p.358 'girder')
- Claim `CLM_607` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.344 'cap'); SRC_ODOT_MBI (Glossary p.341 'bent'); SRC_ODOT_MBI (Glossary p.346 'column')
- Shot: SC_003

## B3.s1 (37.19 s): "Its deck rests on long beams that span from one support to the next."
- Claim `CLM_605` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.341 'beam')
- Claim `CLM_606` [SOURCE_VERIFIED]: SRC_FHWA_CBM (Chapter 2, 'Component Terminology'); SRC_ODOT_MBI (Glossary p.358 'girder')
- Claim `CLM_607` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.344 'cap'); SRC_ODOT_MBI (Glossary p.341 'bent'); SRC_ODOT_MBI (Glossary p.346 'column')
- Shot: SC_003
- Chú thích `B3_beams` COMPONENT_LABEL "Beams" → SC_003 / bridge_timber_beam_01 / timber_beam_bridge_span3_stringers; 37.08–46.04 s; claim CLM_605; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B3.s2 (42.14 s): "Each beam carries the load by resisting bending."
- Claim `CLM_601` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.365 'live load'); SRC_ODOT_MBI (Glossary p.350 'dead load')
- Claim `CLM_605` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.341 'beam')
- Claim `CLM_606` [SOURCE_VERIFIED]: SRC_FHWA_CBM (Chapter 2, 'Component Terminology'); SRC_ODOT_MBI (Glossary p.358 'girder')
- Claim `CLM_607` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.344 'cap'); SRC_ODOT_MBI (Glossary p.341 'bent'); SRC_ODOT_MBI (Glossary p.346 'column')
- Shot: SC_003
- Chú thích `B3_load` LOAD_ARROW "Load" → SC_003 / bridge_timber_beam_01 / timber_beam_bridge_span3_planks; 42.04–52.50 s; claim CLM_601; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS
- Chú thích `B3_bend` CALLOUT "Resists bending" → SC_003 / bridge_timber_beam_01 / timber_beam_bridge_span3_stringers; 42.04–52.50 s; claim CLM_606; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B3.s3 (46.14 s): "A cap beam spreads the load onto the posts, and the posts carry it down in compression."
- Claim `CLM_605` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.341 'beam')
- Claim `CLM_606` [SOURCE_VERIFIED]: SRC_FHWA_CBM (Chapter 2, 'Component Terminology'); SRC_ODOT_MBI (Glossary p.358 'girder')
- Claim `CLM_607` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.344 'cap'); SRC_ODOT_MBI (Glossary p.341 'bent'); SRC_ODOT_MBI (Glossary p.346 'column')
- Shot: SC_003
- Chú thích `B3_path` CONCEPTUAL_LOAD_PATH → SC_003 / bridge_timber_beam_01 / timber_beam_bridge_bent3, timber_beam_bridge_bent3_cap, timber_beam_bridge_span3_planks; 46.04–52.50 s; claim CLM_607; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS
- Chú thích `B3_cap` COMPONENT_LABEL "Cap beam" → SC_003 / bridge_timber_beam_01 / timber_beam_bridge_bent3_cap; 46.04–52.50 s; claim CLM_607; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS
- Chú thích `B3_posts` CALLOUT "Posts: compression" → SC_003 / bridge_timber_beam_01 / timber_beam_bridge_bent3; 46.04–52.50 s; claim CLM_607; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B4.s0 (52.90 s): "A masonry arch works differently."
- Claim `CLM_608` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.388 'voussoir'); SRC_ODOT_MBI (Glossary p.363 'keystone')
- Shot: SC_004, SC_005

## B4.s1 (56.00 s): "It is built from wedge-shaped stones called voussoirs, with a keystone at the crown."
- Claim `CLM_608` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.388 'voussoir'); SRC_ODOT_MBI (Glossary p.363 'keystone')
- Shot: SC_004, SC_005
- Chú thích `B4_key` COMPONENT_LABEL "Keystone" → SC_005 / bridge_stone_arch_03 / stone_arch_bridge_arch2_keystone; 57.25–60.75 s; claim CLM_608; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS
- Chú thích `B4_vous` COMPONENT_LABEL "Voussoirs" → SC_005 / bridge_stone_arch_03 / stone_arch_bridge_arch2_voussoir01; 57.42–60.58 s; claim CLM_608; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B5.s0 (62.40 s): "The curve turns the downward load into thrust along the arch, pressing the stones together."
- Claim `CLM_609` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Part 2 Ratings, Item 25 Arch, p.144 (manual p.2-56)); SRC_ODOT_MBI (Glossary p.339 'arch'); SRC_YALE_PHYSICS ('Arch Bridges' section)
- Claim `CLM_610` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.339 'arch'); SRC_YALE_PHYSICS ('Arch Bridges' section)
- Shot: SC_006
- Chú thích `B5_load` LOAD_ARROW "Load" → SC_006 / bridge_stone_arch_03 / stone_arch_bridge_arch2_keystone; 62.29–77.62 s; claim CLM_609; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS
- Chú thích `B5_thrust` CONCEPTUAL_LOAD_PATH → SC_006 / bridge_stone_arch_03 / stone_arch_bridge_arch2_keystone, stone_arch_bridge_arch2_voussoir01, stone_arch_bridge_arch2_voussoir02 …; 62.29–77.62 s; claim CLM_609; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B5.s1 (68.25 s): "So the arch works mainly in compression."
- Claim `CLM_609` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Part 2 Ratings, Item 25 Arch, p.144 (manual p.2-56)); SRC_ODOT_MBI (Glossary p.339 'arch'); SRC_YALE_PHYSICS ('Arch Bridges' section)
- Claim `CLM_610` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.339 'arch'); SRC_YALE_PHYSICS ('Arch Bridges' section)
- Shot: SC_006
- Chú thích `B5_comp` CALLOUT "Mainly compression" → SC_006 / bridge_stone_arch_03 / stone_arch_bridge_arch2_keystone, stone_arch_bridge_arch2_voussoir01, stone_arch_bridge_arch2_voussoir02 …; 68.17–77.62 s; claim CLM_609; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B5.s2 (71.60 s): "At each end it pushes outward and down on its supports, and the supports push back."
- Claim `CLM_609` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Part 2 Ratings, Item 25 Arch, p.144 (manual p.2-56)); SRC_ODOT_MBI (Glossary p.339 'arch'); SRC_YALE_PHYSICS ('Arch Bridges' section)
- Claim `CLM_610` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.339 'arch'); SRC_YALE_PHYSICS ('Arch Bridges' section)
- Shot: SC_006
- Chú thích `B5_react` REACTION_ARROW "Supports push back" → SC_006 / bridge_stone_arch_03 / stone_arch_bridge_arch2_keystone, stone_arch_bridge_arch2_voussoir01, stone_arch_bridge_arch2_voussoir02 …; 71.50–77.62 s; claim CLM_610; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B6.s0 (78.03 s): "The truss we started with takes another approach: straight members joined into triangles."
- Claim `CLM_611` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.386 'truss'); SRC_SCI_TRUSSES (Introduction)
- Claim `CLM_612` [SOURCE_VERIFIED]: SRC_SCI_TRUSSES (Introduction); SRC_FHWA_CBM (Chapter 2, 'Component Terminology')
- Claim `CLM_613` [SOURCE_VERIFIED]: SRC_FHWA_CBM (Chapter 2, 'Component Terminology'); SRC_SCI_TRUSSES ('Types of trusses')
- Claim `CLM_614` [SOURCE_VERIFIED]: SRC_FHWA_CBM (Chapter 2, 'Component Terminology')
- Shot: SC_007
- Chú thích `B6_joints` COMPONENT_LABEL "Joints" → SC_007 / bridge_steel_truss_pratt_01 / steel_truss_bridge_span1_joints_south; 77.92–89.92 s; claim CLM_611; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B6.s1 (84.03 s): "Each member is mainly pulled or pushed along its length, in tension or in compression."
- Claim `CLM_611` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.386 'truss'); SRC_SCI_TRUSSES (Introduction)
- Claim `CLM_612` [SOURCE_VERIFIED]: SRC_SCI_TRUSSES (Introduction); SRC_FHWA_CBM (Chapter 2, 'Component Terminology')
- Claim `CLM_613` [SOURCE_VERIFIED]: SRC_FHWA_CBM (Chapter 2, 'Component Terminology'); SRC_SCI_TRUSSES ('Types of trusses')
- Claim `CLM_614` [SOURCE_VERIFIED]: SRC_FHWA_CBM (Chapter 2, 'Component Terminology')
- Shot: SC_007
- Chú thích `B6_legend` TENSION_COMPRESSION_LEGEND → SC_007 / bridge_steel_truss_pratt_01 / ; 83.92–103.17 s; claim CLM_612; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B6.s2 (90.00 s): "Each span here is a simple span, so under a downward load its top chord is squeezed and its bottom chord is stretched."
- Claim `CLM_611` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.386 'truss'); SRC_SCI_TRUSSES (Introduction)
- Claim `CLM_612` [SOURCE_VERIFIED]: SRC_SCI_TRUSSES (Introduction); SRC_FHWA_CBM (Chapter 2, 'Component Terminology')
- Claim `CLM_613` [SOURCE_VERIFIED]: SRC_FHWA_CBM (Chapter 2, 'Component Terminology'); SRC_SCI_TRUSSES ('Types of trusses')
- Claim `CLM_614` [SOURCE_VERIFIED]: SRC_FHWA_CBM (Chapter 2, 'Component Terminology')
- Shot: SC_007
- Chú thích `B6_top` CALLOUT "Top chord: compression" → SC_007 / bridge_steel_truss_pratt_01 / steel_truss_bridge_span1_chords_south; 89.92–103.17 s; claim CLM_613; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS
- Chú thích `B6_bottom` CALLOUT "Bottom chord: tension" → SC_007 / bridge_steel_truss_pratt_01 / steel_truss_bridge_span1_chords_south; 89.92–103.17 s; claim CLM_613; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B6.s3 (97.55 s): "Inside, some web members are in compression and others are in tension."
- Claim `CLM_611` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Glossary p.386 'truss'); SRC_SCI_TRUSSES (Introduction)
- Claim `CLM_612` [SOURCE_VERIFIED]: SRC_SCI_TRUSSES (Introduction); SRC_FHWA_CBM (Chapter 2, 'Component Terminology')
- Claim `CLM_613` [SOURCE_VERIFIED]: SRC_FHWA_CBM (Chapter 2, 'Component Terminology'); SRC_SCI_TRUSSES ('Types of trusses')
- Claim `CLM_614` [SOURCE_VERIFIED]: SRC_FHWA_CBM (Chapter 2, 'Component Terminology')
- Shot: SC_007
- Chú thích `B6_web` COMPONENT_LABEL "Web members" → SC_007 / bridge_steel_truss_pratt_01 / steel_truss_bridge_span2_diagonals_south; 97.46–103.17 s; claim CLM_614; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B7.s0 (103.57 s): "Let's compare them one at a time."
- Claim `CLM_606` [SOURCE_VERIFIED]: SRC_FHWA_CBM (Chapter 2, 'Component Terminology'); SRC_ODOT_MBI (Glossary p.358 'girder')
- Claim `CLM_609` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Part 2 Ratings, Item 25 Arch, p.144 (manual p.2-56)); SRC_ODOT_MBI (Glossary p.339 'arch'); SRC_YALE_PHYSICS ('Arch Bridges' section)
- Claim `CLM_612` [SOURCE_VERIFIED]: SRC_SCI_TRUSSES (Introduction); SRC_FHWA_CBM (Chapter 2, 'Component Terminology')
- Shot: SC_008, SC_009, SC_010

## B7.s1 (106.64 s): "The beam bridge carries its load by bending."
- Claim `CLM_606` [SOURCE_VERIFIED]: SRC_FHWA_CBM (Chapter 2, 'Component Terminology'); SRC_ODOT_MBI (Glossary p.358 'girder')
- Claim `CLM_609` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Part 2 Ratings, Item 25 Arch, p.144 (manual p.2-56)); SRC_ODOT_MBI (Glossary p.339 'arch'); SRC_YALE_PHYSICS ('Arch Bridges' section)
- Claim `CLM_612` [SOURCE_VERIFIED]: SRC_SCI_TRUSSES (Introduction); SRC_FHWA_CBM (Chapter 2, 'Component Terminology')
- Shot: SC_008, SC_009, SC_010
- Chú thích `B7_beam` CALLOUT "Bending" → SC_008 / bridge_timber_beam_01 / timber_beam_bridge_span3_stringers; 106.54–110.12 s; claim CLM_606; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B7.s2 (110.32 s): "The arch carries it mainly in compression, pushing against its supports."
- Claim `CLM_606` [SOURCE_VERIFIED]: SRC_FHWA_CBM (Chapter 2, 'Component Terminology'); SRC_ODOT_MBI (Glossary p.358 'girder')
- Claim `CLM_609` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Part 2 Ratings, Item 25 Arch, p.144 (manual p.2-56)); SRC_ODOT_MBI (Glossary p.339 'arch'); SRC_YALE_PHYSICS ('Arch Bridges' section)
- Claim `CLM_612` [SOURCE_VERIFIED]: SRC_SCI_TRUSSES (Introduction); SRC_FHWA_CBM (Chapter 2, 'Component Terminology')
- Shot: SC_008, SC_009, SC_010
- Chú thích `B7_arch` CALLOUT "Compression" → SC_009 / bridge_stone_arch_03 / stone_arch_bridge_arch2_keystone, stone_arch_bridge_arch2_voussoir01, stone_arch_bridge_arch2_voussoir02 …; 110.21–115.25 s; claim CLM_609; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B7.s3 (115.42 s): "In the truss, the load is shared between members in tension and in compression."
- Claim `CLM_606` [SOURCE_VERIFIED]: SRC_FHWA_CBM (Chapter 2, 'Component Terminology'); SRC_ODOT_MBI (Glossary p.358 'girder')
- Claim `CLM_609` [SOURCE_VERIFIED]: SRC_ODOT_MBI (Part 2 Ratings, Item 25 Arch, p.144 (manual p.2-56)); SRC_ODOT_MBI (Glossary p.339 'arch'); SRC_YALE_PHYSICS ('Arch Bridges' section)
- Claim `CLM_612` [SOURCE_VERIFIED]: SRC_SCI_TRUSSES (Introduction); SRC_FHWA_CBM (Chapter 2, 'Component Terminology')
- Shot: SC_008, SC_009, SC_010
- Chú thích `B7_truss` CALLOUT "Tension and compression" → SC_010 / bridge_steel_truss_pratt_01 / steel_truss_bridge_span1_chords_south; 115.33–121.42 s; claim CLM_612; QA: annotation_objects PASS, annotation_anchors PASS, annotation_layout PASS, annotation_timing PASS

## B8.s0 (121.82 s): "Three arrangements of parts, one job: carrying the load across the gap and down into the ground."
- Không có claim (câu dẫn dắt).
- Shot: SC_011

## B8.s1 (128.17 s): "These models are illustrations, not engineering designs, and the arrows show ideas, not calculated forces."
- Không có claim (câu dẫn dắt).
- Shot: SC_011
