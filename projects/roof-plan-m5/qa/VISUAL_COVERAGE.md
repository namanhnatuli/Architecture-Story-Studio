# Visual coverage: Roof generalization fixture (synthetic)

- Planner 1.0.0, timing **PROVISIONAL** (estimates, not measured speech), 4 shots, 20.96 s.
- Executable: **True** · COVERED 4
- Publication: INTERNAL_ONLY — Synthetic planning fixture; invented narration about the illustrative model, no claims.

| Beat | Intent | Strategy | Assets | Semantic targets | Templates (shots) | Expected / planned s | Evidence | Coverage | Issues |
|---|---|---|---|---|---|---|---|---|---|
| R1 | INTRODUCE_ARCHITECTURE | HOLD | low_pitch_gable_roof: ADAPT_EXISTING_ASSET → `legacy_roof_evolution_roof_A` | — | HOLD (SC_001) | 4.65 / 4.67 | FRAMING | **COVERED** | — |
| R2 | EXPLAIN_STRUCTURE | EXPLODE | low_pitch_gable_roof: ADAPT_EXISTING_ASSET → `legacy_roof_evolution_roof_A` | rafters, ridge_beam | EXPLODED_VIEW (SC_002) | 6.57 / 6.58 | FRAMING | **COVERED** | — |
| R3 | EXPLAIN_DESIGN_CHANGE | REPLACE | low_pitch_gable_roof: ADAPT_EXISTING_ASSET → `legacy_roof_evolution_roof_A`<br>steep_gable_roof: ADAPT_EXISTING_ASSET → `legacy_roof_evolution_roof_B` | — | REPLACE_PARTS (SC_003) | 5.42 / 5.42 | FRAMING | **COVERED** | — |
| R4 | COMPARE_VARIANTS | COMPARE_SIDE_BY_SIDE | low_pitch_gable_roof: ADAPT_EXISTING_ASSET → `legacy_roof_evolution_roof_A`<br>steep_gable_roof: ADAPT_EXISTING_ASSET → `legacy_roof_evolution_roof_B` | — | SIDE_BY_SIDE (SC_004) | 4.26 / 4.29 | FRAMING | **COVERED** | — |

## Planner decisions

- **R1**: ASSEMBLE_IN rejected (INVALID_REQUEST): ASSEMBLE_IN needs the previous shot to end on the empty site · HOLD_HIGHLIGHT rejected (INVALID_REQUEST): HOLD_HIGHLIGHT needs component concepts to highlight · HOLD: Hold the structure
- **R2**: HIGHLIGHT_THEN_EXPLODE rejected (TIMING_CONFLICT): HIGHLIGHT_THEN_EXPLODE needs 6.67 s (2.04 + 4.62), the beat has 6.58 s · EXPLODE: Take the assembly apart along its layers and back, focus components glowing
- **R3**: HIGHLIGHT_REPLACE_HIGHLIGHT rejected (TIMING_CONFLICT): HIGHLIGHT_REPLACE_HIGHLIGHT needs 7.71 s (2.04 + 3.62 + 2.04), the beat has 5.42 s · REPLACE: Swap only the differing parts on the shared frame
- **R4**: COMPARE_SIDE_BY_SIDE: All variants at identical scale, captioned
