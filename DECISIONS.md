# Locked product/engineering decisions (2026-10-22)

**Product choices**
- Audience: English-language YouTube, aim 8–15 minutes/video.
- Narration/story-first architecture history/design explainers. 3 formats: decision A→B due to constraints, architecture across time, regional comparison.
- 3D visuals: Clean Stylized Architectural / Technical Visualization; asset geometry separated into meaningful components.
- Transitions: DISASSEMBLE / REPLACE_PARTS / COMPARE / CUTAWAY / EXPLODED_VIEW; careful cause/effect visualizations.
- No required humans/characters/workers/machinery. Destruction is an occasional storytelling device, **not** the channel premise.
- No interactive web application as primary deliverable. Blender renders YouTube videos; Three.js is optional future tool, not MVP.

**Technical choices**
- Mac Apple Silicon M4, RAM 16 GB, creator is beginner.
- Blender + bpy + geometry/procedural modeling, Codex *or* Claude Code as primary coding assistant; Blender MCP optional for inspection; FFmpeg encode.
- Work in project-local files and deterministic, testable stages; single shared project spec JSON rather than giant free-form prompts.
- Unit test offline, then greybox preview, then publication gates. Keep render frames out of version control.
- Blender 4.5 LTS and 5.2 LTS supported by source code where possible; 5.x Eevee identifier changed. Runtime Blender rendering on target Mac remains unverified until user runs it.

**Pilot**
- `roof-evolution`: simple house where only roof configuration changes A→B; 6s greybox preview, no factual claim about roof engineering. This is a render technology smoke test, not a full researched YouTube episode.

If a requested change conflicts with these choices, document the reason and update this file before changing architecture.
