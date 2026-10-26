# SOP 11 — AI collaboration across chat / Codex / Claude

## Session start
1. Read `AGENTS.md`, `DECISIONS.md`, `PROJECT_STATUS.md`, then current project's JSONs.
2. Confirm phase and working directory; `doctor`/`validate` before editing.
3. Write an implementation plan with file targets and exact proposed acceptance test.

## Session close
1. Run unit tests and structural validation.
2. If Blender available, generate still/preview and report exact verified file paths.
3. Update `PROJECT_STATUS.md`: achieved milestones, outstanding issues, command that reproduces results.
4. If design policy changed, update `DECISIONS.md` and corresponding docs; avoid silent drift.
5. Provide 1–3 next actionable tasks, no generic prompts to re-explain requirements already in files.

## AI code editing
- Make smallest diff; do not overwrite creator-authored narratives or research materials without permission.
- Add tests for reusable behavior. Always distinguish implemented/placeholder/unverified.
- Keep user-visible README beginner-friendly, while engineer detail lives in `docs/`.

## Rendering and rights
- Final render is not synonymous with publish-ready. Final QA includes factual claims, license and audio timing.
- Preview should be cached per shot, rerender only affected shots in future iterations.
