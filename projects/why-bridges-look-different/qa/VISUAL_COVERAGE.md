# Visual coverage: Why Bridges Don't All Look the Same

- Planner 1.0.0, timing **AUDIO_LOCKED** (measured narration windows), 47 shots, 646.46 s.
- Executable: **True** · COVERED 39
- Publication: INTERNAL_ONLY — M7 claims are source-verified, not editorially approved; review cut only.
- Visibility (offline Level 1 estimate): 15 shots, 18/20 target rows read, issues 2, auto-repaired 2, manual review 0, uncertain 0 (Blender check: `verify-visibility`).

| Beat | Intent | Strategy | Assets | Semantic targets | Templates (shots) | Expected / planned s | Evidence | Readable | Coverage | Issues |
|---|---|---|---|---|---|---|---|---|---|---|
| B01 | COMPARE_VARIANTS | DETAIL_THEN_OVERVIEW | timber_beam_bridge: REUSE_EXISTING → `bridge_timber_beam_01`<br>stone_arch_bridge: REUSE_EXISTING → `bridge_stone_arch_03`<br>steel_truss_bridge: REUSE_EXISTING → `bridge_steel_truss_pratt_01` | — | HOLD (SC_001), HOLD (SC_002), HOLD (SC_003), SIDE_BY_SIDE (SC_004) | 17.02 / 17.04 | FRAMING | — | **COVERED** | intent cross-check: declared COMPARE_VARIANTS, narration cues suggest ['SHOW_CONTEXT'] |
| B02 | SHOW_CONTEXT | CARD | — | — | MOTION_GRAPHICS (SC_005) | 18.27 / 18.29 | FRAMING | — | **COVERED** | — |
| B03 | INTRODUCE_ARCHITECTURE | HOLD | steel_truss_bridge: REUSE_EXISTING → `bridge_steel_truss_pratt_01` | — | HOLD (SC_006) | 15.75 / 15.75 | INTERNAL_PREVIEW | — | **COVERED** | — |
| B04 | EXPLAIN_LOAD_PATH | HOLD_HIGHLIGHT | steel_truss_bridge: REUSE_EXISTING → `bridge_steel_truss_pratt_01` | substructure | HOLD (SC_007) | 24.07 / 24.08 | INTERNAL_PREVIEW | substructure: reads | **COVERED** | — |
| B05 | SHOW_CONTEXT | SITE_HOLD | river_crossing_site: REUSE_EXISTING → `site_river_crossing_24` | — | HOLD (SC_008) | 10.32 / 10.33 | FRAMING | — | **COVERED** | — |
| B06 | INTRODUCE_ARCHITECTURE | ASSEMBLE_IN | timber_beam_bridge: REUSE_EXISTING → `bridge_timber_beam_01` | stringer | REPLACE_PARTS (SC_009), HOLD (SC_010) | 14.47 / 14.50 | INTERNAL_PREVIEW | stringer: reads | **COVERED** | — |
| B07 | EXPLAIN_STRUCTURE | HIGHLIGHT_THEN_EXPLODE | timber_beam_bridge: REUSE_EXISTING → `bridge_timber_beam_01` | cap_beam, deck_planks, stringer | HOLD (SC_011), EXPLODED_VIEW (SC_012) | 12.93 / 12.96 | INTERNAL_PREVIEW | cap_beam: reads<br>deck_planks: reads<br>stringer: reads | **COVERED** | — |
| B08 | EXPLAIN_LOAD_PATH | HOLD_HIGHLIGHT | timber_beam_bridge: REUSE_EXISTING → `bridge_timber_beam_01` | stringer | HOLD (SC_013) | 15.10 / 15.12 | INTERNAL_PREVIEW | stringer: reads | **COVERED** | — |
| B09 | INTRODUCE_ARCHITECTURE | HOLD_HIGHLIGHT | timber_beam_bridge: REUSE_EXISTING → `bridge_timber_beam_01` | trestle_bent | HOLD (SC_014) | 25.32 / 25.33 | INTERNAL_PREVIEW | trestle_bent: reads | **COVERED** | — |
| B10 | SHOW_COMPONENT | CLOSEUP_EXPLODE | stone_arch_bridge: REUSE_EXISTING → `bridge_stone_arch_03` | arch_ring, keystone, voussoir | HOLD (SC_015), EXPLODED_VIEW (SC_016) | 10.60 / 10.62 | INTERNAL_PREVIEW | arch_ring: reads<br>keystone: reads<br>voussoir: reads | **COVERED** | — |
| B11 | EXPLAIN_LOAD_PATH | HOLD_HIGHLIGHT | stone_arch_bridge: REUSE_EXISTING → `bridge_stone_arch_03` | arch_ring | HOLD (SC_017) | 17.35 / 17.38 | INTERNAL_PREVIEW | arch_ring: reads | **COVERED** | — |
| B12 | INTRODUCE_ARCHITECTURE | HOLD | stone_arch_bridge: REUSE_EXISTING → `bridge_stone_arch_03` | — | HOLD (SC_018) | 14.35 / 14.38 | INTERNAL_PREVIEW | — | **COVERED** | — |
| B13 | EXPLAIN_STRUCTURE | CARD | — | — | MOTION_GRAPHICS (SC_019) | 17.38 / 17.38 | INTERNAL_PREVIEW | — | **COVERED** | — |
| B14 | EXPLAIN_DESIGN_CHANGE | CARD | — | — | MOTION_GRAPHICS (SC_020) | 22.48 / 22.50 | INTERNAL_PREVIEW | — | **COVERED** | — |
| B15 | INTRODUCE_ARCHITECTURE | HOLD_HIGHLIGHT | steel_truss_bridge: REUSE_EXISTING → `bridge_steel_truss_pratt_01` | truss_members | HOLD (SC_021) | 16.10 / 16.12 | INTERNAL_PREVIEW | truss_members: reads | **COVERED** | — |
| B16 | EXPLAIN_LOAD_PATH | HOLD | steel_truss_bridge: REUSE_EXISTING → `bridge_steel_truss_pratt_01` | — | HOLD (SC_022) | 14.45 / 14.46 | INTERNAL_PREVIEW | — | **COVERED** | — |
| B17 | EXPLAIN_DESIGN_CHANGE | HIGHLIGHT_REPLACE_HIGHLIGHT | pratt_truss: REUSE_EXISTING → `bridge_steel_truss_pratt_01`<br>warren_truss: REUSE_EXISTING → `bridge_steel_truss_warren_01` | truss_web | HOLD (SC_023), REPLACE_PARTS (SC_024), HOLD (SC_025) | 31.45 / 31.46 | INTERNAL_PREVIEW | truss_web: reads | **COVERED** | — |
| B18 | EXPLAIN_STRUCTURE | EXPLODE | steel_truss_bridge: REUSE_EXISTING → `bridge_steel_truss_pratt_01` | — | EXPLODED_VIEW (SC_026) | 21.60 / 21.62 | INTERNAL_PREVIEW | — | **COVERED** | intent cross-check: declared EXPLAIN_STRUCTURE, narration cues suggest ['EXPLAIN_DESIGN_CHANGE', 'SHOW_CONTEXT', 'SHOW_EVOLUTION'] |
| B19 | SHOW_CONTEXT | CARD | — | — | MOTION_GRAPHICS (SC_027) | 14.88 / 14.88 | FRAMING | — | **COVERED** | — |
| B20A | INTRODUCE_ARCHITECTURE | HOLD_HIGHLIGHT | stone_arch_bridge: REUSE_EXISTING → `bridge_stone_arch_03` | arch_ring | HOLD (SC_028) | 9.90 / 9.92 | INTERNAL_PREVIEW | arch_ring: reads | **COVERED** | — |
| B20B | INTRODUCE_ARCHITECTURE | HOLD_HIGHLIGHT | steel_truss_bridge: REUSE_EXISTING → `bridge_steel_truss_pratt_01` | truss_members | HOLD (SC_029) | 15.78 / 15.79 | INTERNAL_PREVIEW | truss_members: reads | **COVERED** | — |
| B20C | INTRODUCE_ARCHITECTURE | HOLD | timber_beam_bridge: REUSE_EXISTING → `bridge_timber_beam_01` | — | HOLD (SC_030) | 7.17 / 7.21 | INTERNAL_PREVIEW | — | **COVERED** | — |
| B21 | SHOW_CONTEXT | CARD | — | — | MOTION_GRAPHICS (SC_031) | 15.53 / 15.54 | INTERNAL_PREVIEW | — | **COVERED** | — |
| B22 | SHOW_CONTEXT | CARD | — | — | MOTION_GRAPHICS (SC_032) | 20.43 / 20.46 | INTERNAL_PREVIEW | — | **COVERED** | — |
| B23 | SHOW_CONTEXT | SITE_HOLD | river_crossing_site: REUSE_EXISTING → `site_river_crossing_24` | — | HOLD (SC_033) | 5.45 / 5.46 | FRAMING | — | **COVERED** | — |
| B23B | EXPLAIN_STRUCTURE | CARD | — | — | MOTION_GRAPHICS (SC_034) | 17.45 / 17.46 | INTERNAL_PREVIEW | — | **COVERED** | — |
| B24 | SHOW_CONTEXT | CARD | — | — | MOTION_GRAPHICS (SC_035) | 18.55 / 18.58 | INTERNAL_PREVIEW | — | **COVERED** | — |
| B25 | SHOW_CONTEXT | CARD | — | — | MOTION_GRAPHICS (SC_036) | 20.00 / 20.00 | INTERNAL_PREVIEW | — | **COVERED** | intent cross-check: declared SHOW_CONTEXT, narration cues suggest ['SHOW_EVOLUTION'] |
| B26 | SHOW_CONTEXT | CARD | — | — | MOTION_GRAPHICS (SC_037) | 23.27 / 23.29 | INTERNAL_PREVIEW | — | **COVERED** | — |
| B27 | INTRODUCE_ARCHITECTURE | HOLD | stone_arch_bridge: REUSE_EXISTING → `bridge_stone_arch_03` | — | HOLD (SC_038) | 10.50 / 10.50 | INTERNAL_PREVIEW | — | **COVERED** | — |
| B28 | SHOW_CONTEXT | CARD | — | — | MOTION_GRAPHICS (SC_039) | 19.52 / 19.54 | INTERNAL_PREVIEW | — | **COVERED** | — |
| B29 | INTRODUCE_ARCHITECTURE | HOLD_HIGHLIGHT | timber_beam_bridge: REUSE_EXISTING → `bridge_timber_beam_01` | trestle_bent | HOLD (SC_040) | 13.07 / 13.08 | INTERNAL_PREVIEW | trestle_bent: reads | **COVERED** | — |
| B30 | SHOW_CONTEXT | CARD | — | — | MOTION_GRAPHICS (SC_041) | 27.45 / 27.46 | INTERNAL_PREVIEW | — | **COVERED** | — |
| B31 | SUMMARIZE_DIFFERENCES | CARD | — | — | MOTION_GRAPHICS (SC_042) | 12.80 / 12.83 | INTERNAL_PREVIEW | — | **COVERED** | intent cross-check: declared SUMMARIZE_DIFFERENCES, narration cues suggest ['COMPARE_VARIANTS'] |
| B32 | SUMMARIZE_DIFFERENCES | COMPARE_SIDE_BY_SIDE | timber_beam_bridge: REUSE_EXISTING → `bridge_timber_beam_01`<br>stone_arch_bridge: REUSE_EXISTING → `bridge_stone_arch_03`<br>steel_truss_bridge: REUSE_EXISTING → `bridge_steel_truss_pratt_01` | — | SIDE_BY_SIDE (SC_043) | 20.40 / 20.42 | INTERNAL_PREVIEW | — | **COVERED** | — |
| B32B | SUMMARIZE_DIFFERENCES | CARD | — | — | MOTION_GRAPHICS (SC_044) | 8.62 / 8.62 | INTERNAL_PREVIEW | — | **COVERED** | intent cross-check: declared SUMMARIZE_DIFFERENCES, narration cues suggest ['SHOW_CONTEXT'] |
| B33 | SUMMARIZE_DIFFERENCES | CARD | — | — | MOTION_GRAPHICS (SC_045) | 17.15 / 17.17 | INTERNAL_PREVIEW | — | **COVERED** | — |
| B34 | INTRODUCE_ARCHITECTURE | HOLD | stone_arch_bridge: REUSE_EXISTING → `bridge_stone_arch_03` | — | HOLD (SC_046) | 19.70 / 19.71 | FRAMING | — | **COVERED** | — |
| B35 | SHOW_CONTEXT | CARD | — | — | MOTION_GRAPHICS (SC_047) | 9.18 / 9.21 | FRAMING | — | **COVERED** | — |

## Planner decisions

- **B01**: DETAIL_THEN_OVERVIEW timing: cuts on sentence starts [1, 2, 3] · DETAIL_THEN_OVERVIEW: Each variant alone under one locked camera, then all together
- **B02**: CARD: 2D card (text/arrows) supplied by the beat
- **B03**: HOLD: Hold the structure
- **B04**: HOLD_HIGHLIGHT: Hold the structure and glow the focus components
- **B05**: SITE_HOLD: Hold on the shared site before any structure (the gap to span)
- **B06**: ASSEMBLE_IN timing: cuts on sentence starts [2] · ASSEMBLE_IN: Structure drops into place on the shown empty site, then its focus parts glow
- **B07**: HIGHLIGHT_THEN_EXPLODE timing: cuts on sentence starts [1] · HIGHLIGHT_THEN_EXPLODE: Glow the focus components, then take the assembly apart and back
- **B08**: HOLD_HIGHLIGHT: Hold the structure and glow the focus components
- **B09**: HOLD_HIGHLIGHT: Hold the structure and glow the focus components
- **B10**: CLOSEUP_EXPLODE timing: cuts on sentence starts [1] · CLOSEUP_EXPLODE: Establish the structure, then a close-up in which only the focus pieces separate, showing their individual shape
- **B11**: HOLD_HIGHLIGHT: Hold the structure and glow the focus components
- **B12**: HOLD: Hold the structure
- **B13**: CARD: 2D card (text/arrows) supplied by the beat
- **B14**: CARD: 2D card (text/arrows) supplied by the beat
- **B15**: HOLD_HIGHLIGHT: Hold the structure and glow the focus components
- **B16**: HOLD: Hold the structure
- **B17**: HIGHLIGHT_REPLACE_HIGHLIGHT timing: cuts on sentence starts [3, 4] · HIGHLIGHT_REPLACE_HIGHLIGHT: Glow the parts that will change, swap them on the shared frame, glow the new parts
- **B18**: EXPLODE: Take the assembly apart along its layers and back, focus components glowing
- **B19**: CARD: 2D card (text/arrows) supplied by the beat
- **B20A**: HOLD_HIGHLIGHT: Hold the structure and glow the focus components
- **B20B**: HOLD_HIGHLIGHT: Hold the structure and glow the focus components
- **B20C**: HOLD: Hold the structure
- **B21**: CARD: 2D card (text/arrows) supplied by the beat
- **B22**: CARD: 2D card (text/arrows) supplied by the beat
- **B23**: SITE_HOLD: Hold on the shared site before any structure (the gap to span)
- **B23B**: CARD: 2D card (text/arrows) supplied by the beat
- **B24**: CARD: 2D card (text/arrows) supplied by the beat
- **B25**: CARD: 2D card (text/arrows) supplied by the beat
- **B26**: CARD: 2D card (text/arrows) supplied by the beat
- **B27**: HOLD: Hold the structure
- **B28**: CARD: 2D card (text/arrows) supplied by the beat
- **B29**: HOLD_HIGHLIGHT: Hold the structure and glow the focus components
- **B30**: CARD: 2D card (text/arrows) supplied by the beat
- **B31**: CARD: 2D card (text/arrows) supplied by the beat
- **B32**: COMPARE_SIDE_BY_SIDE: All variants at identical scale, captioned (layout chosen by planner/composition.py: STACK or ROW, gap)
- **B32B**: CARD: 2D card (text/arrows) supplied by the beat
- **B33**: CARD: 2D card (text/arrows) supplied by the beat
- **B34**: HOLD: Hold the structure
- **B35**: CARD: 2D card (text/arrows) supplied by the beat

## Visual repairs (offline, before rendering)

- **B06 SC_010 stringer** at highlight_peak: OCCLUDED (share 0.14, core 0.00%) → **GHOST:plank** (share 0.81, core 1.67%). Evaluated: GHOST:plank PASS (share 0.81, core 1.67%, area 5.04% -> PASS)
- **B08 SC_013 stringer** at highlight_peak: OCCLUDED (share 0.14, core 0.00%) → **GHOST:plank** (share 0.81, core 1.67%). Evaluated: GHOST:plank PASS (share 0.81, core 1.67%, area 5.04% -> PASS)

## Comparison composition

- SC_001: SEQUENTIAL_COMPARISON, purpose detail, scale COMMON, smallest member 5.8 px, smallest model 88% of the frame width
- SC_002: SEQUENTIAL_COMPARISON, purpose detail, scale COMMON, smallest member 14.3 px, smallest model 88% of the frame width
- SC_003: SEQUENTIAL_COMPARISON, purpose detail, scale COMMON, smallest member 3.9 px, smallest model 88% of the frame width
- SC_004: SIDE_BY_SIDE_ROW gap 0.2, purpose overview, scale COMMON, smallest member 1.1 px, smallest model 26% of the frame width
- SC_043: SIDE_BY_SIDE_ROW gap 0.2, purpose overview, scale COMMON, smallest member 1.1 px, smallest model 26% of the frame width
  - candidate STACK gap 0.5: smallest model 25% of the frame width (< 25%)
  - candidate STACK gap 0.25: captions collide with the next row
  - candidate ROW gap 0.35: smallest model 24% of the frame width (< 25%)
  - candidate ROW gap 0.2: readable

## Warnings

- B01: declared COMPARE_VARIANTS, narration cues suggest ['SHOW_CONTEXT']
- B18: declared EXPLAIN_STRUCTURE, narration cues suggest ['EXPLAIN_DESIGN_CHANGE', 'SHOW_CONTEXT', 'SHOW_EVOLUTION']
- B25: declared SHOW_CONTEXT, narration cues suggest ['SHOW_EVOLUTION']
- B31: declared SUMMARIZE_DIFFERENCES, narration cues suggest ['COMPARE_VARIANTS']
- B32B: declared SUMMARIZE_DIFFERENCES, narration cues suggest ['SHOW_CONTEXT']
