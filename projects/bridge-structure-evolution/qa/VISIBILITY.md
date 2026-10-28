# Visibility: Level 1 estimate vs Level 2 Blender measurement (bridge-structure-evolution)

- 47 target x frame rows; verdict agreement **1.0**; visible-share error mean 0.0045, max 0.0152.
- Level 2 (Blender, 192x108 orthographic rays, evaluated meshes): 2.2 s; Level 1 (offline raster): 1.0 s.
- Explanatory frames failing in Blender: 0 (a concept only has to read in one shot of its beat); beat concepts unreadable in Blender: none of 5.

| Shot | Frame | Concept | L1 share / core % / area % | L2 share / core % / area % | L1 | L2 | L2 occluders |
|---|---|---|---|---|---|---|---|
| SC_001 | highlight_peak (41) | highlight | 0.81 / 1.70 / 5.04 | 0.82 / 1.79 / 5.10 | reads | reads | timber_beam_railing_south, bank_right |
| SC_002 | exploded_hold (64) | highlight | 0.50 / 1.39 / 3.14 | 0.51 / 1.42 / 3.17 | reads | reads | timber_beam_span4_planks, timber_beam_span2_planks |
| SC_003 | highlight_peak (41) | highlight | 0.31 / 1.76 / 3.20 | 0.31 / 1.71 / 3.12 | reads | reads | stone_arch_spandrel, stone_arch_parapet_south |
| SC_004 | exploded_hold (73) | highlight | 1.00 / 0.87 / 1.36 | 1.00 / 0.84 / 1.34 | reads | reads | — |
| SC_005 | highlight_peak (41) | highlight | 0.79 / 0.04 / 3.03 | 0.79 / 0.05 / 3.12 | reads | reads | steel_truss_span1_joints_south, steel_truss_span2_joints_south |
