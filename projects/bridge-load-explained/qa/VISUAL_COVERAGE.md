# Visual coverage: How Does a Bridge Carry Its Load?

- Planner 1.0.0, timing **AUDIO_LOCKED** (measured narration windows), 11 shots, 136.29 s.
- Executable: **True** · COVERED 8
- Publication: INTERNAL_ONLY — Claims are source-verified, not editorially approved; the narration provider (Kokoro-82M) is PENDING_REVIEW and the voice is not approved by the user.
- Visibility (offline Level 1 estimate): 6 shots, 7/7 target rows read, issues 1, auto-repaired 1, manual review 0, uncertain 0 (Blender check: `verify-visibility`).

| Beat | Intent | Strategy | Assets | Semantic targets | Templates (shots) | Expected / planned s | Evidence | Readable | Coverage | Issues |
|---|---|---|---|---|---|---|---|---|---|---|
| B1 | INTRODUCE_ARCHITECTURE | HOLD | steel_truss_bridge: REUSE_EXISTING → `bridge_steel_truss_pratt_01` | — | HOLD (SC_001) | 14.20 / 14.21 | INTERNAL_PREVIEW | — | **COVERED** | — |
| B2 | EXPLAIN_LOAD_PATH | HOLD_HIGHLIGHT | steel_truss_bridge: REUSE_EXISTING → `bridge_steel_truss_pratt_01` | substructure | HOLD (SC_002) | 19.95 / 19.96 | INTERNAL_PREVIEW | substructure: reads | **COVERED** | — |
| B3 | EXPLAIN_LOAD_PATH | HOLD_HIGHLIGHT | timber_beam_bridge: REUSE_EXISTING → `bridge_timber_beam_01` | stringer | HOLD (SC_003) | 18.30 / 18.33 | INTERNAL_PREVIEW | stringer: reads | **COVERED** | — |
| B4 | SHOW_COMPONENT | CLOSEUP_EXPLODE | stone_arch_bridge: REUSE_EXISTING → `bridge_stone_arch_03` | arch_ring, keystone, voussoir | HOLD (SC_004), EXPLODED_VIEW (SC_005) | 9.50 / 9.50 | INTERNAL_PREVIEW | arch_ring: reads<br>keystone: reads<br>voussoir: reads | **COVERED** | — |
| B5 | EXPLAIN_LOAD_PATH | HOLD_HIGHLIGHT | stone_arch_bridge: REUSE_EXISTING → `bridge_stone_arch_03` | arch_ring | HOLD (SC_006) | 15.60 / 15.62 | INTERNAL_PREVIEW | arch_ring: reads | **COVERED** | — |
| B6 | EXPLAIN_LOAD_PATH | HOLD_HIGHLIGHT | steel_truss_bridge: REUSE_EXISTING → `bridge_steel_truss_pratt_01` | truss_members | HOLD (SC_007) | 25.52 / 25.54 | INTERNAL_PREVIEW | truss_members: reads | **COVERED** | — |
| B7 | COMPARE_VARIANTS | SEQUENTIAL_COMPARISON | timber_beam_bridge: REUSE_EXISTING → `bridge_timber_beam_01`<br>stone_arch_bridge: REUSE_EXISTING → `bridge_stone_arch_03`<br>steel_truss_bridge: REUSE_EXISTING → `bridge_steel_truss_pratt_01` | — | HOLD (SC_008), HOLD (SC_009), HOLD (SC_010) | 18.23 / 18.25 | INTERNAL_PREVIEW | — | **COVERED** | — |
| B8 | SUMMARIZE_DIFFERENCES | COMPARE_SIDE_BY_SIDE | timber_beam_bridge: REUSE_EXISTING → `bridge_timber_beam_01`<br>stone_arch_bridge: REUSE_EXISTING → `bridge_stone_arch_03`<br>steel_truss_bridge: REUSE_EXISTING → `bridge_steel_truss_pratt_01` | — | SIDE_BY_SIDE (SC_011) | 14.88 / 14.88 | FRAMING | — | **COVERED** | — |

## Planner decisions

- **B1**: HOLD: Hold the structure
- **B2**: HOLD_HIGHLIGHT: Hold the structure and glow the focus components
- **B3**: HOLD_HIGHLIGHT: Hold the structure and glow the focus components
- **B4**: CLOSEUP_EXPLODE timing: cuts on sentence starts [1] · CLOSEUP_EXPLODE: Establish the structure, then a close-up in which only the focus pieces separate, showing their individual shape
- **B5**: HOLD_HIGHLIGHT: Hold the structure and glow the focus components
- **B6**: HOLD_HIGHLIGHT: Hold the structure and glow the focus components
- **B7**: SEQUENTIAL_COMPARISON timing: cuts on sentence starts [2, 3] · SEQUENTIAL_COMPARISON: One variant at a time under one shared locked camera (same scale), captioned
- **B8**: CONTINUE_COMPARISON rejected (INVALID_REQUEST): no comparison of the same states to continue · COMPARE_SIDE_BY_SIDE: All variants at identical scale, captioned (layout chosen by planner/composition.py: STACK or ROW, gap)

## Visual repairs (offline, before rendering)

- **B3 SC_003 stringer** at highlight_peak: OCCLUDED (share 0.14, core 0.00%) → **GHOST:plank** (share 0.81, core 1.67%). Evaluated: GHOST:plank PASS (share 0.81, core 1.67%, area 5.04% -> PASS)

## Comparison composition

- SC_008: SEQUENTIAL_COMPARISON, purpose detail, scale COMMON, smallest member 5.8 px, smallest model 88% of the frame width
- SC_009: SEQUENTIAL_COMPARISON, purpose detail, scale COMMON, smallest member 14.3 px, smallest model 88% of the frame width
- SC_010: SEQUENTIAL_COMPARISON, purpose detail, scale COMMON, smallest member 3.9 px, smallest model 88% of the frame width
- SC_011: SIDE_BY_SIDE_ROW gap 0.2, purpose overview, scale COMMON, smallest member 1.1 px, smallest model 26% of the frame width
  - candidate STACK gap 0.5: smallest model 25% of the frame width (< 25%)
  - candidate STACK gap 0.25: captions collide with the next row
  - candidate ROW gap 0.35: smallest model 24% of the frame width (< 25%)
  - candidate ROW gap 0.2: readable
