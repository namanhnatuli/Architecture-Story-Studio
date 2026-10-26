# SOP 10 — How to start a real episode

## Step 1 — Chọn đề tài có question-first hook
Ví dụ:
- **Design decision:** Why did some buildings develop steep roofs? (phải chọn vùng và thời kỳ cụ thể)
- **Evolution:** Three bridge structures across documented historical examples, not an invented sequence of 10th→15th→20th-century 'global progression'.
- **Regional comparison:** Compare traditional *minka* and a clearly defined *siheyuan* type in their historical contexts; don't generalize national housing.

## Step 2 — Tạo 4 nguồn dữ liệu nội dung
`research/sources.json`, `script/outline.md`, `script/narration.md`, `storyboard/storyboard.json`.

Use research prompt then storyboard prompt. Every beat includes claim IDs and a visually testable `visual_purpose`.

## Step 3 — Build state registry
- List shared components of same building (walls/foundation).
- List exclusive components for each design variant, including whether variants share camera/ground scale.
- Set transition strategy: swap_parts / side_by_side / cutaway / timeline; don't use arbitrary morphing.

## Step 4 — AI chooses renderer (Blender-first)
- Blender: object geometry, camera, shader, animation, render.
- Archive/maps/diagrams: use web/file sources with verified rights and data; compose offline later.
- Three.js not needed for video-only workflow.

## Step 5 — Implement in tiny increments
1. One greybox still.
2. A/B contact sheet.
3. 4–8s shot animation preview.
4. Review accuracy and readability.
5. Only then expand detailed asset quality and render final.

## Step 6 — Long-form production
For 8–15 min output, create multiple shots with independent render jobs and reliable cache. Do not try to use the demo renderer unchanged for an arbitrary regional/timeline research project: extend a generic scene dispatcher first.

## Production deliverables (target, not all implemented in v0.1)
- Evidence ledger, script with links, storyboard, variant registry.
- Source-backed 3D model and compliant media assets.
- Numbered PNG shots and video/audio/subtitle files.
- QA report for technical, visual, factual and rights gates.

## Supported status in the starter package
- ✅ sample 6-second Roof A → B procedural render code.
- ✅ structural data validation and final gate.
- ✅ FFmpeg video encoding helper.
- ⏳ real episode research ingestion, automatic TTS, archival downloader, subtitle generation, generic shot dispatcher, scene-cache/resume, visual AI judge (roadmap, not implemented).
