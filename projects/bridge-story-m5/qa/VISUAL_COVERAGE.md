# Visual coverage: Three Ways to Span a Gap

- Planner 1.0.0, timing **PROVISIONAL** (estimates, not measured speech), 13 shots, 72.38 s.
- Executable: **True** · COVERED 8
- Publication: INTERNAL_ONLY — Claims are source-verified, not editorially approved; no rights-cleared narration exists (silent preview).

| Beat | Intent | Strategy | Assets | Semantic targets | Templates (shots) | Expected / planned s | Evidence | Coverage | Issues |
|---|---|---|---|---|---|---|---|---|---|
| B1 | SHOW_CONTEXT | SITE_HOLD | river_crossing_site: REUSE_EXISTING → `site_river_crossing_24` | — | HOLD (SC_001) | 10.80 / 10.83 | FRAMING | **COVERED** | — |
| B2 | INTRODUCE_ARCHITECTURE | ASSEMBLE_IN | timber_beam_bridge: REUSE_EXISTING → `bridge_timber_beam_01` | stringer | REPLACE_PARTS (SC_002), HOLD (SC_003) | 10.80 / 10.83 | INTERNAL_PREVIEW | **COVERED** | — |
| B3 | EXPLAIN_STRUCTURE | HIGHLIGHT_THEN_EXPLODE | timber_beam_bridge: REUSE_EXISTING → `bridge_timber_beam_01` | cap_beam, deck_planks, stringer | HOLD (SC_004), EXPLODED_VIEW (SC_005) | 9.65 / 9.67 | FRAMING | **COVERED** | — |
| B4 | SHOW_COMPONENT | CLOSEUP_HIGHLIGHT | stone_arch_bridge: REUSE_EXISTING → `bridge_stone_arch_03` | arch_ring, keystone, voussoir | HOLD (SC_006), HOLD (SC_007) | 9.26 / 9.29 | INTERNAL_PREVIEW | **COVERED** | — |
| B5 | INTRODUCE_ARCHITECTURE | HOLD_HIGHLIGHT | steel_truss_bridge: REUSE_EXISTING → `bridge_steel_truss_pratt_01` | truss_web | HOLD (SC_008) | 5.03 / 5.04 | INTERNAL_PREVIEW | **COVERED** | — |
| B6 | EXPLAIN_DESIGN_CHANGE | HIGHLIGHT_REPLACE_HIGHLIGHT | pratt_truss: REUSE_EXISTING → `bridge_steel_truss_pratt_01`<br>warren_truss: REUSE_EXISTING → `bridge_steel_truss_warren_01` | truss_web | HOLD (SC_009), REPLACE_PARTS (SC_010), HOLD (SC_011) | 12.72 / 12.75 | INTERNAL_PREVIEW | **COVERED** | — |
| B7 | COMPARE_VARIANTS | COMPARE_SIDE_BY_SIDE | timber_beam_bridge: REUSE_EXISTING → `bridge_timber_beam_01`<br>stone_arch_bridge: REUSE_EXISTING → `bridge_stone_arch_03`<br>steel_truss_bridge: REUSE_EXISTING → `bridge_steel_truss_pratt_01` | — | SIDE_BY_SIDE (SC_012) | 6.18 / 6.21 | FRAMING | **COVERED** | — |
| B8 | SUMMARIZE_DIFFERENCES | CONTINUE_COMPARISON | timber_beam_bridge: REUSE_EXISTING → `bridge_timber_beam_01`<br>stone_arch_bridge: REUSE_EXISTING → `bridge_stone_arch_03`<br>steel_truss_bridge: REUSE_EXISTING → `bridge_steel_truss_pratt_01` | — | SIDE_BY_SIDE (SC_013) | 7.72 / 7.75 | FRAMING | **COVERED** | — |

## Planner decisions

- **B1**: SITE_HOLD: Hold on the shared site before any structure (the gap to span)
- **B2**: ASSEMBLE_IN: Structure drops into place on the shown empty site, then its focus parts glow
- **B3**: HIGHLIGHT_THEN_EXPLODE: Glow the focus components, then take the assembly apart and back
- **B4**: CLOSEUP_HIGHLIGHT: Establish the structure with the focus parts glowing, then a close-up framed on them
- **B5**: ASSEMBLE_IN rejected (INVALID_REQUEST): ASSEMBLE_IN needs the previous shot to end on the empty site · HOLD_HIGHLIGHT: Hold the structure and glow the focus components
- **B6**: HIGHLIGHT_REPLACE_HIGHLIGHT: Glow the parts that will change, swap them on the shared frame, glow the new parts
- **B7**: COMPARE_SIDE_BY_SIDE: All variants at identical scale, captioned
- **B8**: CONTINUE_COMPARISON: Stay on the comparison, glow what differs
