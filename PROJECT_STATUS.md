# Current project status

- Phase: **M0 packaging completed; M1 Blender runtime preview pending**.
- Environment used for packaging: Python 3.13 on Linux; Blender not installed. Static syntax validation, structural JSON validation and unit tests pass.
- Current playable video: **none in package**; final MP4 must be generated on user's Mac.
- Pilot project: `projects/roof-evolution` (`project.json` + storyboard + variants).
- Next commands on user's Mac: `python3 tools/cli.py doctor`, `python3 tools/cli.py validate`, `python3 tools/cli.py still`, then `python3 tools/cli.py preview`.
- QA: research/factual claim marked provisional. Final/publication gate intentionally blocked.
- Current source supports a **specific simple-house roof A→B renderer**, not arbitrary building geometry generated from any narrative. Extend scene dispatcher and geometry library after pilot passes.

## Known limitations
- No TTS, audio montage, footage ingestion, or source fetching yet.
- No finished thumbnail, video or factual research episode.
- No Blender headless render test in packaging environment; compatibility to be verified on user's Blender version.
- Animation is physically suggestive, not engineering or physics simulation.
