# Visibility: Level 1 estimate vs Level 2 Blender measurement (roof-plan-m5)

- 20 target x frame rows; verdict agreement **1.0**; visible-share error mean 0.0148, max 0.0427.
- Level 2 (Blender, 192x108 orthographic rays, evaluated meshes): 0.8 s; Level 1 (offline raster): 0.1 s.
- Explanatory frames failing in Blender: 0 (a concept only has to read in one shot of its beat); beat concepts unreadable in Blender: none of 2.

| Shot | Frame | Concept | L1 share / core % / area % | L2 share / core % / area % | L1 | L2 | L2 occluders |
|---|---|---|---|---|---|---|---|
| SC_002 | exploded_hold (81) | rafters | 0.59 / 1.03 / 3.26 | 0.55 / 0.65 / 2.57 | reads | reads | low_pitch_gable_roof_covering_right |
| SC_002 | exploded_hold (81) | ridge_beam | 0.35 / 0.12 / 0.29 | 0.35 / 0.12 / 0.29 | reads | reads | low_pitch_gable_roof_covering_right, low_pitch_gable_roof_rafters_right |
