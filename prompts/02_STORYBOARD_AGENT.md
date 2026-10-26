# Narrative-to-Visual Storyboard task template

Inputs: verified research claims, English outline, agreed target duration, scene geometry availability.

Create a beat-based script: every line of narration must be illustrated by one of: Blender 3D scene, archival photo/video, map, diagram, or focused text/number overlay.

For each shot output:
- scene_id, narration, `visual_purpose` (what the viewer learns), claim IDs,
- visual strategy, architecture `from_state` and `to_state` if applicable,
- camera/focus, animation template, duration and rough start time,
- required components/assets, factual/production caveats.

Choose `REPLACE_PARTS` for A→B component transitions; `SIDE_BY_SIDE` for regions; `TIMELINE` for dated exemplars. Keep camera angle/scales comparable; don't morph incompatible meshes. Run validator after saving storyboard JSON.
