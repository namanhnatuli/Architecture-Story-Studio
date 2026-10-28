# Visibility: Level 1 estimate vs Level 2 Blender measurement (roof-evolution)

- 10 target x frame rows; verdict agreement **1.0**; visible-share error mean 0.0248, max 0.0452.
- Level 2 (Blender, 192x108 orthographic rays, evaluated meshes): 0.7 s; Level 1 (offline raster): 0.08 s.
- Explanatory frames failing in Blender: 0 (a concept only has to read in one shot of its beat); beat concepts unreadable in Blender: none of 1.

| Shot | Frame | Concept | L1 share / core % / area % | L2 share / core % / area % | L1 | L2 | L2 occluders |
|---|---|---|---|---|---|---|---|
| SC_002 | exploded_hold (62) | highlight | 0.57 / 0.23 / 1.61 | 0.53 / 0.08 / 1.31 | reads | reads | roof_A_covering_right, roof_A_covering_left |
