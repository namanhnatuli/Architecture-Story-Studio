# Visual coverage: Roof generalization fixture (synthetic)

- Planner 1.0.0, timing **PROVISIONAL** (estimates, not measured speech), 4 shots, 20.96 s.
- Executable: **True** · COVERED 4
- Publication: INTERNAL_ONLY — Synthetic planning fixture; invented narration about the illustrative model, no claims.
- Visibility (offline Level 1 estimate): 1 shots, 2/2 target rows read, issues 1, auto-repaired 1, manual review 0, uncertain 0 (Blender check: `verify-visibility`).

| Beat | Intent | Strategy | Assets | Semantic targets | Templates (shots) | Expected / planned s | Evidence | Readable | Coverage | Issues |
|---|---|---|---|---|---|---|---|---|---|---|
| R1 | INTRODUCE_ARCHITECTURE | HOLD | low_pitch_gable_roof: ADAPT_EXISTING_ASSET → `legacy_roof_evolution_roof_A` | — | HOLD (SC_001) | 4.65 / 4.67 | FRAMING | — | **COVERED** | — |
| R2 | EXPLAIN_STRUCTURE | EXPLODE | low_pitch_gable_roof: ADAPT_EXISTING_ASSET → `legacy_roof_evolution_roof_A` | rafters, ridge_beam | EXPLODED_VIEW (SC_002) | 6.57 / 6.58 | FRAMING | rafters: reads<br>ridge_beam: reads | **COVERED** | — |
| R3 | EXPLAIN_DESIGN_CHANGE | REPLACE | low_pitch_gable_roof: ADAPT_EXISTING_ASSET → `legacy_roof_evolution_roof_A`<br>steep_gable_roof: ADAPT_EXISTING_ASSET → `legacy_roof_evolution_roof_B` | — | REPLACE_PARTS (SC_003) | 5.42 / 5.42 | FRAMING | — | **COVERED** | — |
| R4 | COMPARE_VARIANTS | COMPARE_SIDE_BY_SIDE | low_pitch_gable_roof: ADAPT_EXISTING_ASSET → `legacy_roof_evolution_roof_A`<br>steep_gable_roof: ADAPT_EXISTING_ASSET → `legacy_roof_evolution_roof_B` | — | SIDE_BY_SIDE (SC_004) | 4.26 / 4.29 | FRAMING | — | **COVERED** | — |

## Planner decisions

- **R1**: ASSEMBLE_IN rejected (INVALID_REQUEST): ASSEMBLE_IN needs the previous shot to end on the empty site · HOLD_HIGHLIGHT rejected (INVALID_REQUEST): HOLD_HIGHLIGHT needs component concepts to highlight · HOLD: Hold the structure
- **R2**: HIGHLIGHT_THEN_EXPLODE rejected (TIMING_CONFLICT): HIGHLIGHT_THEN_EXPLODE needs 6.67 s (2.04 + 4.62), the beat has 6.58 s · EXPLODE: Take the assembly apart along its layers and back, focus components glowing
- **R3**: HIGHLIGHT_REPLACE_HIGHLIGHT rejected (TIMING_CONFLICT): HIGHLIGHT_REPLACE_HIGHLIGHT needs 7.71 s (2.04 + 3.62 + 2.04), the beat has 5.42 s · REPLACE: Swap only the differing parts on the shared frame
- **R4**: COMPARE_SIDE_BY_SIDE: All variants at identical scale, captioned (layout chosen by planner/composition.py: STACK or ROW, gap)

## Visual repairs (offline, before rendering)

- **R2 SC_002 ridge_beam** at exploded_hold: TOO_SMALL (share 0.34, core 0.02%) → **REFRAME** (share 0.35, core 0.12%). Evaluated: REFRAME PASS (share 0.35, core 0.12%, area 0.29% -> PASS)

## Comparison composition

- SC_004: SIDE_BY_SIDE_ROW gap 0.35, purpose detail, scale COMMON, smallest member 31.9 px, smallest model 35% of the frame width
  - candidate STACK gap 0.5: smallest model 17% of the frame width (< 25%)
  - candidate STACK gap 0.25: smallest model 19% of the frame width (< 25%)
  - candidate ROW gap 0.35: readable
  - candidate ROW gap 0.2: readable
