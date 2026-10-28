# Visibility: Level 1 estimate vs Level 2 Blender measurement (suffolk-roofs)

- 10 target x frame rows; verdict agreement **1.0**; visible-share error mean 0.0134, max 0.0138.
- Level 2 (Blender, 192x108 orthographic rays, evaluated meshes): 0.7 s; Level 1 (offline raster): 0.09 s.
- Explanatory frames failing in Blender: 0 (a concept only has to read in one shot of its beat); beat concepts unreadable in Blender: none of 1.

| Shot | Frame | Concept | L1 share / core % / area % | L2 share / core % / area % | L1 | L2 | L2 occluders |
|---|---|---|---|---|---|---|---|
| SC_002 | exploded_hold (275) | highlight | 0.93 / 9.30 / 10.39 | 0.95 / 9.37 / 10.48 | reads | reads | thatch_50_ridge_cap, thatch_50_gable_front |
