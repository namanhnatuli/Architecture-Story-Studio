# Visual coverage: Three Ways to Span a Gap

- Planner 1.0.0, timing **PROVISIONAL** (estimates, not measured speech), 15 shots, 73.92 s.
- Executable: **True** · COVERED 8
- Publication: INTERNAL_ONLY — Claims are source-verified, not editorially approved; no rights-cleared narration exists (silent preview).
- Visibility (offline Level 1 estimate): 8 shots, 11/13 target rows read, issues 1, auto-repaired 1, manual review 0, uncertain 0 (Blender check: `verify-visibility`).

| Beat | Intent | Strategy | Assets | Semantic targets | Templates (shots) | Expected / planned s | Evidence | Readable | Coverage | Issues |
|---|---|---|---|---|---|---|---|---|---|---|
| B1 | SHOW_CONTEXT | SITE_HOLD | river_crossing_site: REUSE_EXISTING → `site_river_crossing_24` | — | HOLD (SC_001) | 10.80 / 10.83 | FRAMING | — | **COVERED** | — |
| B2 | INTRODUCE_ARCHITECTURE | ASSEMBLE_IN | timber_beam_bridge: REUSE_EXISTING → `bridge_timber_beam_01` | stringer | REPLACE_PARTS (SC_002), HOLD (SC_003) | 10.80 / 10.83 | INTERNAL_PREVIEW | stringer: reads | **COVERED** | — |
| B3 | EXPLAIN_STRUCTURE | HIGHLIGHT_THEN_EXPLODE | timber_beam_bridge: REUSE_EXISTING → `bridge_timber_beam_01` | cap_beam, deck_planks, stringer | HOLD (SC_004), EXPLODED_VIEW (SC_005) | 9.65 / 9.67 | FRAMING | cap_beam: reads<br>deck_planks: reads<br>stringer: reads | **COVERED** | — |
| B4 | SHOW_COMPONENT | CLOSEUP_EXPLODE | stone_arch_bridge: REUSE_EXISTING → `bridge_stone_arch_03` | arch_ring, keystone, voussoir | HOLD (SC_006), EXPLODED_VIEW (SC_007) | 9.26 / 9.29 | INTERNAL_PREVIEW | arch_ring: reads<br>keystone: reads<br>voussoir: reads | **COVERED** | — |
| B5 | INTRODUCE_ARCHITECTURE | HOLD_HIGHLIGHT | steel_truss_bridge: REUSE_EXISTING → `bridge_steel_truss_pratt_01` | truss_web | HOLD (SC_008) | 5.03 / 5.04 | INTERNAL_PREVIEW | truss_web: reads | **COVERED** | — |
| B6 | EXPLAIN_DESIGN_CHANGE | HIGHLIGHT_REPLACE_HIGHLIGHT | pratt_truss: REUSE_EXISTING → `bridge_steel_truss_pratt_01`<br>warren_truss: REUSE_EXISTING → `bridge_steel_truss_warren_01` | truss_web | HOLD (SC_009), REPLACE_PARTS (SC_010), HOLD (SC_011) | 12.72 / 12.75 | INTERNAL_PREVIEW | truss_web: reads | **COVERED** | — |
| B7 | COMPARE_VARIANTS | SEQUENTIAL_COMPARISON | timber_beam_bridge: REUSE_EXISTING → `bridge_timber_beam_01`<br>stone_arch_bridge: REUSE_EXISTING → `bridge_stone_arch_03`<br>steel_truss_bridge: REUSE_EXISTING → `bridge_steel_truss_pratt_01` | — | HOLD (SC_012), HOLD (SC_013), HOLD (SC_014) | 7.72 / 7.75 | FRAMING | — | **COVERED** | — |
| B8 | SUMMARIZE_DIFFERENCES | COMPARE_SIDE_BY_SIDE | timber_beam_bridge: REUSE_EXISTING → `bridge_timber_beam_01`<br>stone_arch_bridge: REUSE_EXISTING → `bridge_stone_arch_03`<br>steel_truss_bridge: REUSE_EXISTING → `bridge_steel_truss_pratt_01` | — | SIDE_BY_SIDE (SC_015) | 7.72 / 7.75 | FRAMING | — | **COVERED** | — |

## Planner decisions

- **B1**: SITE_HOLD: Hold on the shared site before any structure (the gap to span)
- **B2**: ASSEMBLE_IN: Structure drops into place on the shown empty site, then its focus parts glow
- **B3**: HIGHLIGHT_THEN_EXPLODE: Glow the focus components, then take the assembly apart and back
- **B4**: CLOSEUP_EXPLODE: Establish the structure, then a close-up in which only the focus pieces separate, showing their individual shape
- **B5**: ASSEMBLE_IN rejected (INVALID_REQUEST): ASSEMBLE_IN needs the previous shot to end on the empty site · HOLD_HIGHLIGHT: Hold the structure and glow the focus components
- **B6**: HIGHLIGHT_REPLACE_HIGHLIGHT: Glow the parts that will change, swap them on the shared frame, glow the new parts
- **B7**: COMPARE_SIDE_BY_SIDE rejected (UNREADABLE): no simultaneous layout of 3 models reads at 640x360 (detail): STACK 0.5: members ~1.3 px wide at 640x360 (< 2.5) | STACK 0.25: members ~1.5 px wide at 640x360 (< 2.5) | ROW 0.35: members ~1.1 px wide at 640x360 (< 2.5); smallest model 24% of the frame width (< 25%) | ROW 0.2: members ~1.1 px wide at 640x360 (< 2.5) · FOCUSED_PAIR rejected (INVALID_REQUEST): FOCUSED_PAIR needs focus_states naming two of three or more compared states · DETAIL_THEN_OVERVIEW rejected (TIMING_CONFLICT): DETAIL_THEN_OVERVIEW needs 8.04 s (2.00 + 2.00 + 2.00 + 2.04), the beat has 7.75 s · SEQUENTIAL_COMPARISON: One variant at a time under one shared locked camera (same scale), captioned
- **B8**: CONTINUE_COMPARISON rejected (INVALID_REQUEST): no comparison of the same states to continue · COMPARE_SIDE_BY_SIDE: All variants at identical scale, captioned (layout chosen by planner/composition.py: STACK or ROW, gap)

## Visual repairs (offline, before rendering)

- **B2 SC_003 stringer** at highlight_peak: OCCLUDED (share 0.14, core 0.00%) → **GHOST:plank** (share 0.81, core 1.67%). Evaluated: REFRAME SKIPPED (would break the match cut with the previous shot); ALT_CAMERA:ELEVATION SKIPPED (would break the match-cut continuity (a different view direction)); GHOST:plank PASS (share 0.81, core 1.67%, area 5.04% -> PASS)

## Comparison composition

- SC_012: SEQUENTIAL_COMPARISON, purpose detail, scale COMMON, smallest member 5.8 px, smallest model 88% of the frame width
- SC_013: SEQUENTIAL_COMPARISON, purpose detail, scale COMMON, smallest member 14.3 px, smallest model 88% of the frame width
- SC_014: SEQUENTIAL_COMPARISON, purpose detail, scale COMMON, smallest member 3.9 px, smallest model 88% of the frame width
- SC_015: SIDE_BY_SIDE_STACK gap 0.25, purpose overview, scale COMMON, smallest member 1.5 px, smallest model 34% of the frame width
  - candidate STACK gap 0.5: readable
  - candidate STACK gap 0.25: readable
  - candidate ROW gap 0.35: smallest model 24% of the frame width (< 25%)
  - candidate ROW gap 0.2: readable
