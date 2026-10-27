# Structural components (reusable primitives)

Pure-Python building blocks in `engine/arch/library.py` and `engine/arch/primitives.py` (no bpy), shared by
every family generator:

| Utility | Produces |
|---|---|
| `primitives.box`, `member(p0, p1, w, h)`, `sector(...)`, `prism_xz(outline, depth)`, `cylinder_z` | mesh data (verts, faces) |
| `library.spaced`, `repeat_along_x` | positions / repeated units with joint gaps (planks, courses) |
| `library.post`, `beam_x`, `beam_y`, `x_brace`, `x_brace_y` | timber/steel posts, beams, cross braces |
| `library.arch_angles`, `voussoir_mesh`, `keystone_mesh`, `rotation_for_angle`, `spandrel_outline` | masonry arch rings and the fill around them |
| `library.cutwater_outline`, `prism_xy` | pier noses and other plan-extruded shapes |
| `library.truss_nodes`, `truss_web(pattern)`, `truss_members_mesh`, `gusset` | parallel-chord trusses (Pratt, Warren), connection plates |

Semantic metadata (`engine/arch/semantic.py`): `Component` with id, type, material, group, variant, transform,
layer, explode hint, animation roles, bevel, evidence.
