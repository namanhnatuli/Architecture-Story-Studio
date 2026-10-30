# Visibility: Level 1 estimate vs Level 2 Blender measurement (bridge-story-m5)

- 122 target x frame rows; verdict agreement **1.0**; visible-share error mean 0.006, max 0.0174.
- Level 2 (Blender, 192x108 orthographic rays, evaluated meshes): 3.6 s; Level 1 (offline raster): 1.73 s.
- Explanatory frames failing in Blender: 2 (a concept only has to read in one shot of its beat); beat concepts unreadable in Blender: none of 9.

| Shot | Frame | Concept | L1 share / core % / area % | L2 share / core % / area % | L1 | L2 | L2 occluders |
|---|---|---|---|---|---|---|---|
| SC_003 | highlight_peak (65) | stringer | 0.81 / 1.67 / 5.04 | 0.82 / 1.78 / 5.13 | reads | reads | timber_beam_bridge_railing_south, bank_right |
| SC_004 | highlight_peak (41) | deck_planks | 0.82 / 1.74 / 5.15 | 0.83 / 1.87 / 5.25 | reads | reads | timber_beam_bridge_railing_south, timber_beam_bridge_railing_north |
| SC_004 | highlight_peak (41) | stringer | 0.14 / 0.00 / 0.85 | 0.14 / 0.00 / 0.85 | OCCLUDED | OCCLUDED | timber_beam_bridge_span4_planks, timber_beam_bridge_span1_planks |
| SC_004 | highlight_peak (41) | cap_beam | 0.17 / 0.03 / 0.17 | 0.18 / 0.04 / 0.18 | OCCLUDED | OCCLUDED | bank_right, timber_beam_bridge_railing_south |
| SC_005 | exploded_hold (82) | deck_planks | 1.00 / 4.98 / 6.28 | 1.00 / 4.98 / 6.29 | reads | reads | — |
| SC_005 | exploded_hold (82) | stringer | 0.50 / 1.37 / 3.14 | 0.51 / 1.43 / 3.19 | reads | reads | timber_beam_bridge_span4_planks, timber_beam_bridge_span2_planks |
| SC_005 | exploded_hold (82) | cap_beam | 0.49 / 0.10 / 0.48 | 0.50 / 0.10 / 0.48 | reads | reads | timber_beam_bridge_railing_south, timber_beam_bridge_span3_stringers |
| SC_006 | highlight_peak (42) | arch_ring | 0.31 / 1.75 / 3.18 | 0.31 / 1.71 / 3.14 | reads | reads | stone_arch_bridge_spandrel, stone_arch_bridge_parapet_south |
| SC_007 | exploded_hold (76) | voussoir | 1.00 / 6.12 / 8.35 | 1.00 / 6.12 / 8.33 | reads | reads | — |
| SC_007 | exploded_hold (76) | keystone | 1.00 / 0.55 / 0.76 | 1.00 / 0.55 / 0.76 | reads | reads | — |
| SC_008 | highlight_peak (65) | truss_web | 0.79 / 0.05 / 3.05 | 0.80 / 0.06 / 3.12 | reads | reads | steel_truss_bridge_span1_joints_south, steel_truss_bridge_span2_joints_south |
| SC_009 | highlight_peak (50) | truss_web | 0.79 / 0.05 / 3.05 | 0.80 / 0.06 / 3.12 | reads | reads | steel_truss_bridge_span1_joints_south, steel_truss_bridge_span2_joints_south |
| SC_011 | highlight_peak (51) | truss_web | 0.79 / 0.00 / 1.91 | 0.78 / 0.00 / 1.86 | reads | reads | steel_truss_bridge_span2_joints_south, steel_truss_bridge_span1_joints_south |
