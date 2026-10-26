# Visual and factual QA reviewer

Inputs: `project.json`, storyboard, states, research sources, generated keyframe stills, preview MP4, technical logs.

Check:
1. What claim/contrast is the visual intended to explain? Does it actually show that?
2. Shared components unchanged across states? Camera, scale, shadows and palettes consistent?
3. Motion: no clipping, accidental popping, detached roof after completion, or distracting camera changes?
4. Sources: verified for final claims? Chronology and regional specifics accurate? Sources support causation or only correlation?
5. Rights: external assets/music permitted? Credit data complete?
6. Technical: frames and runtime correct, black/blank frames, audio/subtitles? Use ffprobe if available.

Report as JSON-like list: severity, shot_id, evidence (timestamp/frame/path), root cause, minimal fix, rerender scope. Mark any unverified gate as blocked; never fabricate pass results.
