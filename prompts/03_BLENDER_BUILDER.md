# Blender builder task template

Read `AGENTS.md`, project spec and `docs/05_ANIMATION_LIBRARY.md`. Build procedural Blender scene using version-adaptive bpy code.

Requirements:
- Separate shared components from variant-specific components.
- Label objects with `component_id`, `variant_id`, `role`.
- Build geometry deterministic from config; no random values without fixed seed.
- If doing REPLACE_PARTS: move old specific components off-screen and inactivate; bring new components in; never disturb shared components.
- Keep a locked 3/4 camera and consistent scale; premium clean stylized materials and soft lights.
- Run tests and JSON validate before preview still; render just one still before 6–10s animation.
- Use only local project outputs. Never claim render success without checking file existence.

Outputs: source diff, `.blend`, still PNG, preview frames/MP4, log and QA notes.
