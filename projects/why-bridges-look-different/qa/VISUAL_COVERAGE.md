# Visual coverage: Why Bridges Don't All Look the Same

- Planner 1.0.0, timing **AUDIO_LOCKED** (measured narration windows), 75 shots, 1193.79 s.
- Executable: **True** · COVERED 66
- Publication: INTERNAL_ONLY — M8 revision m8-r2: claims are source-verified, not yet editorially approved; review cut only.
- Visibility (offline Level 1 estimate): 27 shots, 30/32 target rows read, issues 2, auto-repaired 2, manual review 0, uncertain 0 (Blender check: `verify-visibility`).

| Beat | Intent | Strategy | Assets | Semantic targets | Templates (shots) | Expected / planned s | Evidence | Readable | Coverage | Issues |
|---|---|---|---|---|---|---|---|---|---|---|
| B01 | COMPARE_VARIANTS | DETAIL_THEN_OVERVIEW | timber_beam_bridge: REUSE_EXISTING → `bridge_timber_beam_01`<br>stone_arch_bridge: REUSE_EXISTING → `bridge_stone_arch_03`<br>steel_truss_bridge: REUSE_EXISTING → `bridge_steel_truss_pratt_01` | — | HOLD (SC_001), HOLD (SC_002), HOLD (SC_003), SIDE_BY_SIDE (SC_004) | 15.75 / 15.75 | FRAMING | — | **COVERED** | intent cross-check: declared COMPARE_VARIANTS, narration cues suggest ['SHOW_CONTEXT'] |
| B01B | INTRODUCE_ARCHITECTURE | HOLD | cantilever_bridge: REUSE_EXISTING → `bridge_cantilever_truss_01` | — | HOLD (SC_005) | 8.43 / 8.46 | FRAMING | — | **COVERED** | — |
| B01C | INTRODUCE_ARCHITECTURE | HOLD | suspension_bridge: REUSE_EXISTING → `bridge_suspension_01` | — | HOLD (SC_006) | 4.53 / 4.54 | FRAMING | — | **COVERED** | — |
| B01D | INTRODUCE_ARCHITECTURE | HOLD | cable_stayed_bridge: REUSE_EXISTING → `bridge_cable_stayed_01` | — | HOLD (SC_007) | 4.62 / 4.62 | FRAMING | — | **COVERED** | — |
| B02 | SHOW_CONTEXT | CARD | — | — | MOTION_GRAPHICS (SC_008) | 18.93 / 18.96 | FRAMING | — | **COVERED** | — |
| B03 | INTRODUCE_ARCHITECTURE | HOLD | steel_truss_bridge: REUSE_EXISTING → `bridge_steel_truss_pratt_01` | — | HOLD (SC_009) | 15.68 / 15.71 | INTERNAL_PREVIEW | — | **COVERED** | — |
| B04 | EXPLAIN_LOAD_PATH | HOLD_HIGHLIGHT | steel_truss_bridge: REUSE_EXISTING → `bridge_steel_truss_pratt_01` | substructure | HOLD (SC_010) | 23.50 / 23.50 | INTERNAL_PREVIEW | substructure: reads | **COVERED** | — |
| B05 | SHOW_CONTEXT | SITE_HOLD | river_crossing_site: REUSE_EXISTING → `site_river_crossing_24` | — | HOLD (SC_011) | 9.43 / 9.46 | FRAMING | — | **COVERED** | — |
| B06 | INTRODUCE_ARCHITECTURE | ASSEMBLE_IN | timber_beam_bridge: REUSE_EXISTING → `bridge_timber_beam_01` | stringer | REPLACE_PARTS (SC_012), HOLD (SC_013) | 14.10 / 14.12 | INTERNAL_PREVIEW | stringer: reads | **COVERED** | — |
| B07 | EXPLAIN_STRUCTURE | HIGHLIGHT_THEN_EXPLODE | timber_beam_bridge: REUSE_EXISTING → `bridge_timber_beam_01` | cap_beam, deck_planks, stringer | HOLD (SC_014), EXPLODED_VIEW (SC_015) | 12.72 / 12.75 | INTERNAL_PREVIEW | cap_beam: reads<br>deck_planks: reads<br>stringer: reads | **COVERED** | — |
| B08 | EXPLAIN_LOAD_PATH | HOLD_HIGHLIGHT | timber_beam_bridge: REUSE_EXISTING → `bridge_timber_beam_01` | stringer | HOLD (SC_016) | 14.90 / 14.92 | INTERNAL_PREVIEW | stringer: reads | **COVERED** | — |
| B09 | INTRODUCE_ARCHITECTURE | HOLD_HIGHLIGHT | timber_beam_bridge: REUSE_EXISTING → `bridge_timber_beam_01` | trestle_bent | HOLD (SC_017) | 27.98 / 28.00 | INTERNAL_PREVIEW | trestle_bent: reads | **COVERED** | — |
| B10 | SHOW_COMPONENT | CLOSEUP_EXPLODE | stone_arch_bridge: REUSE_EXISTING → `bridge_stone_arch_03` | arch_ring, keystone, voussoir | HOLD (SC_018), EXPLODED_VIEW (SC_019) | 10.55 / 10.58 | INTERNAL_PREVIEW | arch_ring: reads<br>keystone: reads<br>voussoir: reads | **COVERED** | — |
| B11 | EXPLAIN_LOAD_PATH | HOLD_HIGHLIGHT | stone_arch_bridge: REUSE_EXISTING → `bridge_stone_arch_03` | arch_ring | HOLD (SC_020) | 17.23 / 17.25 | INTERNAL_PREVIEW | arch_ring: reads | **COVERED** | — |
| B12 | INTRODUCE_ARCHITECTURE | HOLD | stone_arch_bridge: REUSE_EXISTING → `bridge_stone_arch_03` | — | HOLD (SC_021) | 14.60 / 14.62 | INTERNAL_PREVIEW | — | **COVERED** | — |
| B13 | EXPLAIN_STRUCTURE | CARD | — | — | MOTION_GRAPHICS (SC_022) | 17.23 / 17.25 | INTERNAL_PREVIEW | — | **COVERED** | — |
| B14 | EXPLAIN_DESIGN_CHANGE | CARD | — | — | MOTION_GRAPHICS (SC_023) | 22.30 / 22.33 | INTERNAL_PREVIEW | — | **COVERED** | — |
| B15 | INTRODUCE_ARCHITECTURE | HOLD_HIGHLIGHT | steel_truss_bridge: REUSE_EXISTING → `bridge_steel_truss_pratt_01` | truss_members | HOLD (SC_024) | 15.90 / 15.92 | INTERNAL_PREVIEW | truss_members: reads | **COVERED** | — |
| B16 | EXPLAIN_LOAD_PATH | HOLD | steel_truss_bridge: REUSE_EXISTING → `bridge_steel_truss_pratt_01` | — | HOLD (SC_025) | 14.57 / 14.58 | INTERNAL_PREVIEW | — | **COVERED** | — |
| B17 | EXPLAIN_DESIGN_CHANGE | HIGHLIGHT_REPLACE_HIGHLIGHT | pratt_truss: REUSE_EXISTING → `bridge_steel_truss_pratt_01`<br>warren_truss: REUSE_EXISTING → `bridge_steel_truss_warren_01` | truss_web | HOLD (SC_026), REPLACE_PARTS (SC_027), HOLD (SC_028) | 32.15 / 32.17 | INTERNAL_PREVIEW | truss_web: reads | **COVERED** | — |
| B18 | EXPLAIN_STRUCTURE | EXPLODE | steel_truss_bridge: REUSE_EXISTING → `bridge_steel_truss_pratt_01` | — | EXPLODED_VIEW (SC_029) | 21.65 / 21.67 | INTERNAL_PREVIEW | — | **COVERED** | intent cross-check: declared EXPLAIN_STRUCTURE, narration cues suggest ['EXPLAIN_DESIGN_CHANGE', 'SHOW_CONTEXT', 'SHOW_EVOLUTION'] |
| B40 | SHOW_CONTEXT | SITE_HOLD | wide_river_crossing_site: REUSE_EXISTING → `site_river_crossing_72` | — | HOLD (SC_030) | 15.88 / 15.88 | INTERNAL_PREVIEW | — | **COVERED** | — |
| B41 | INTRODUCE_ARCHITECTURE | ASSEMBLE_IN | cantilever_bridge: REUSE_EXISTING → `bridge_cantilever_truss_01` | — | REPLACE_PARTS (SC_031) | 14.03 / 14.04 | INTERNAL_PREVIEW | — | **COVERED** | — |
| B42 | INTRODUCE_ARCHITECTURE | HOLD_HIGHLIGHT | cantilever_bridge: REUSE_EXISTING → `bridge_cantilever_truss_01` | cantilever_truss | HOLD (SC_032) | 15.05 / 15.08 | INTERNAL_PREVIEW | cantilever_truss: reads | **COVERED** | — |
| B43 | EXPLAIN_STRUCTURE | EXPLODE | cantilever_bridge: REUSE_EXISTING → `bridge_cantilever_truss_01` | suspended_span | EXPLODED_VIEW (SC_033) | 14.80 / 14.83 | INTERNAL_PREVIEW | suspended_span: reads | **COVERED** | — |
| B44 | SHOW_CONTEXT | CARD | — | — | MOTION_GRAPHICS (SC_034) | 28.60 / 28.62 | INTERNAL_PREVIEW | — | **COVERED** | — |
| B45 | INTRODUCE_ARCHITECTURE | HOLD_HIGHLIGHT | suspension_bridge: REUSE_EXISTING → `bridge_suspension_01` | hanger | HOLD (SC_035) | 13.10 / 13.12 | INTERNAL_PREVIEW | hanger: reads | **COVERED** | — |
| B46 | EXPLAIN_LOAD_PATH | HOLD | suspension_bridge: REUSE_EXISTING → `bridge_suspension_01` | — | HOLD (SC_036) | 13.30 / 13.33 | INTERNAL_PREVIEW | — | **COVERED** | — |
| B47 | EXPLAIN_STRUCTURE | HIGHLIGHT_THEN_EXPLODE | suspension_bridge: REUSE_EXISTING → `bridge_suspension_01` | stiffening_truss | HOLD (SC_037), EXPLODED_VIEW (SC_038) | 12.75 / 12.75 | INTERNAL_PREVIEW | stiffening_truss: reads | **COVERED** | — |
| B48 | SHOW_CONTEXT | CARD | — | — | MOTION_GRAPHICS (SC_039) | 19.68 / 19.71 | INTERNAL_PREVIEW | — | **COVERED** | — |
| B50 | INTRODUCE_ARCHITECTURE | HOLD_HIGHLIGHT | cable_stayed_bridge: REUSE_EXISTING → `bridge_cable_stayed_01` | stay_cable | HOLD (SC_040) | 13.70 / 13.71 | INTERNAL_PREVIEW | stay_cable: reads | **COVERED** | — |
| B51 | COMPARE_VARIANTS | CARD | — | — | MOTION_GRAPHICS (SC_041) | 22.60 / 22.62 | INTERNAL_PREVIEW | — | **COVERED** | — |
| B52 | EXPLAIN_STRUCTURE | EXPLODE | cable_stayed_bridge: REUSE_EXISTING → `bridge_cable_stayed_01` | deck_segment | EXPLODED_VIEW (SC_042) | 17.05 / 17.08 | INTERNAL_PREVIEW | deck_segment: reads | **COVERED** | intent cross-check: declared EXPLAIN_STRUCTURE, narration cues suggest ['COMPARE_VARIANTS'] |
| B53 | EXPLAIN_DESIGN_CHANGE | CARD | — | — | MOTION_GRAPHICS (SC_043) | 24.62 / 24.62 | INTERNAL_PREVIEW | — | **COVERED** | — |
| B19 | SHOW_CONTEXT | CARD | — | — | MOTION_GRAPHICS (SC_044) | 14.40 / 14.42 | FRAMING | — | **COVERED** | — |
| B20A | INTRODUCE_ARCHITECTURE | HOLD_HIGHLIGHT | stone_arch_bridge: REUSE_EXISTING → `bridge_stone_arch_03` | arch_ring | HOLD (SC_045) | 9.65 / 9.67 | INTERNAL_PREVIEW | arch_ring: reads | **COVERED** | — |
| B20B | INTRODUCE_ARCHITECTURE | HOLD_HIGHLIGHT | steel_truss_bridge: REUSE_EXISTING → `bridge_steel_truss_pratt_01` | truss_members | HOLD (SC_046) | 15.88 / 15.88 | INTERNAL_PREVIEW | truss_members: reads | **COVERED** | — |
| B20C | INTRODUCE_ARCHITECTURE | HOLD | timber_beam_bridge: REUSE_EXISTING → `bridge_timber_beam_01` | — | HOLD (SC_047) | 7.22 / 7.25 | INTERNAL_PREVIEW | — | **COVERED** | — |
| B21 | SHOW_CONTEXT | CARD | — | — | MOTION_GRAPHICS (SC_048) | 16.00 / 16.00 | INTERNAL_PREVIEW | — | **COVERED** | — |
| B20E | INTRODUCE_ARCHITECTURE | HOLD_HIGHLIGHT | suspension_bridge: REUSE_EXISTING → `bridge_suspension_01` | main_cable | HOLD (SC_049) | 27.02 / 27.04 | INTERNAL_PREVIEW | main_cable: reads | **COVERED** | — |
| B22 | SHOW_CONTEXT | CARD | — | — | MOTION_GRAPHICS (SC_050) | 20.05 / 20.08 | INTERNAL_PREVIEW | — | **COVERED** | — |
| B22B | SHOW_CONTEXT | CARD | — | — | MOTION_GRAPHICS (SC_051) | 20.68 / 20.71 | INTERNAL_PREVIEW | — | **COVERED** | — |
| B22C | INTRODUCE_ARCHITECTURE | HOLD_HIGHLIGHT | cantilever_bridge: REUSE_EXISTING → `bridge_cantilever_truss_01` | pier | HOLD (SC_052) | 19.95 / 19.96 | INTERNAL_PREVIEW | pier: reads | **COVERED** | — |
| B22D | INTRODUCE_ARCHITECTURE | HOLD_HIGHLIGHT | suspension_bridge: REUSE_EXISTING → `bridge_suspension_01` | stiffening_truss | HOLD (SC_053) | 21.43 / 21.46 | INTERNAL_PREVIEW | stiffening_truss: reads | **COVERED** | — |
| B23C | EXPLAIN_STRUCTURE | CARD | — | — | MOTION_GRAPHICS (SC_054) | 44.35 / 44.38 | INTERNAL_PREVIEW | — | **COVERED** | — |
| B23D | INTRODUCE_ARCHITECTURE | HOLD_HIGHLIGHT | suspension_bridge: REUSE_EXISTING → `bridge_suspension_01` | anchorage | HOLD (SC_055) | 21.50 / 21.50 | INTERNAL_PREVIEW | anchorage: reads | **COVERED** | — |
| B23E | INTRODUCE_ARCHITECTURE | HOLD | cable_stayed_bridge: REUSE_EXISTING → `bridge_cable_stayed_01` | — | HOLD (SC_056) | 13.07 / 13.08 | INTERNAL_PREVIEW | — | **COVERED** | — |
| B24 | SHOW_CONTEXT | CARD | — | — | MOTION_GRAPHICS (SC_057) | 18.65 / 18.67 | INTERNAL_PREVIEW | — | **COVERED** | — |
| B24B | SHOW_CONTEXT | CARD | — | — | MOTION_GRAPHICS (SC_058) | 30.95 / 30.96 | INTERNAL_PREVIEW | — | **COVERED** | — |
| B25 | SHOW_CONTEXT | CARD | — | — | MOTION_GRAPHICS (SC_059) | 20.38 / 20.38 | INTERNAL_PREVIEW | — | **COVERED** | intent cross-check: declared SHOW_CONTEXT, narration cues suggest ['SHOW_EVOLUTION'] |
| B26 | SHOW_CONTEXT | CARD | — | — | MOTION_GRAPHICS (SC_060) | 23.12 / 23.12 | INTERNAL_PREVIEW | — | **COVERED** | — |
| B27 | INTRODUCE_ARCHITECTURE | HOLD | stone_arch_bridge: REUSE_EXISTING → `bridge_stone_arch_03` | — | HOLD (SC_061) | 10.10 / 10.12 | INTERNAL_PREVIEW | — | **COVERED** | — |
| B28 | SHOW_CONTEXT | CARD | — | — | MOTION_GRAPHICS (SC_062) | 19.62 / 19.62 | INTERNAL_PREVIEW | — | **COVERED** | — |
| B29 | INTRODUCE_ARCHITECTURE | HOLD_HIGHLIGHT | timber_beam_bridge: REUSE_EXISTING → `bridge_timber_beam_01` | trestle_bent | HOLD (SC_063) | 12.47 / 12.50 | INTERNAL_PREVIEW | trestle_bent: reads | **COVERED** | — |
| B30 | SHOW_CONTEXT | CARD | — | — | MOTION_GRAPHICS (SC_064) | 27.70 / 27.71 | INTERNAL_PREVIEW | — | **COVERED** | — |
| B31 | SUMMARIZE_DIFFERENCES | CARD | — | — | MOTION_GRAPHICS (SC_065) | 13.05 / 13.08 | INTERNAL_PREVIEW | — | **COVERED** | intent cross-check: declared SUMMARIZE_DIFFERENCES, narration cues suggest ['COMPARE_VARIANTS'] |
| B31A | INTRODUCE_ARCHITECTURE | HOLD | suspension_bridge: REUSE_EXISTING → `bridge_suspension_01` | — | HOLD (SC_066) | 29.75 / 29.75 | INTERNAL_PREVIEW | — | **COVERED** | — |
| B31B | INTRODUCE_ARCHITECTURE | HOLD_HIGHLIGHT | cantilever_bridge: REUSE_EXISTING → `bridge_cantilever_truss_01` | cantilever_truss | HOLD (SC_067) | 29.82 / 29.83 | INTERNAL_PREVIEW | cantilever_truss: reads | **COVERED** | — |
| B31C | SHOW_CONTEXT | CARD | — | — | MOTION_GRAPHICS (SC_068) | 12.22 / 12.25 | INTERNAL_PREVIEW | — | **COVERED** | — |
| B31D | INTRODUCE_ARCHITECTURE | HOLD | cable_stayed_bridge: REUSE_EXISTING → `bridge_cable_stayed_01` | — | HOLD (SC_069) | 28.07 / 28.08 | INTERNAL_PREVIEW | — | **COVERED** | — |
| B32 | SUMMARIZE_DIFFERENCES | COMPARE_SIDE_BY_SIDE | timber_beam_bridge: REUSE_EXISTING → `bridge_timber_beam_01`<br>stone_arch_bridge: REUSE_EXISTING → `bridge_stone_arch_03`<br>steel_truss_bridge: REUSE_EXISTING → `bridge_steel_truss_pratt_01` | — | SIDE_BY_SIDE (SC_070) | 20.43 / 20.46 | INTERNAL_PREVIEW | — | **COVERED** | — |
| B32L | SUMMARIZE_DIFFERENCES | COMPARE_SIDE_BY_SIDE | cantilever_bridge: REUSE_EXISTING → `bridge_cantilever_truss_01`<br>suspension_bridge: REUSE_EXISTING → `bridge_suspension_01`<br>cable_stayed_bridge: REUSE_EXISTING → `bridge_cable_stayed_01` | — | SIDE_BY_SIDE (SC_071) | 9.12 / 9.12 | INTERNAL_PREVIEW | — | **COVERED** | — |
| B32B | SUMMARIZE_DIFFERENCES | CARD | — | — | MOTION_GRAPHICS (SC_072) | 8.65 / 8.67 | INTERNAL_PREVIEW | — | **COVERED** | intent cross-check: declared SUMMARIZE_DIFFERENCES, narration cues suggest ['SHOW_CONTEXT'] |
| B33 | SUMMARIZE_DIFFERENCES | CARD | — | — | MOTION_GRAPHICS (SC_073) | 36.75 / 36.75 | INTERNAL_PREVIEW | — | **COVERED** | — |
| B34 | INTRODUCE_ARCHITECTURE | HOLD | stone_arch_bridge: REUSE_EXISTING → `bridge_stone_arch_03` | — | HOLD (SC_074) | 19.93 / 19.96 | FRAMING | — | **COVERED** | — |
| B35 | SHOW_CONTEXT | CARD | — | — | MOTION_GRAPHICS (SC_075) | 8.75 / 8.75 | FRAMING | — | **COVERED** | — |

## Planner decisions

- **B01**: DETAIL_THEN_OVERVIEW timing: cuts on sentence starts [1, 2, 3] · DETAIL_THEN_OVERVIEW: Each variant alone under one locked camera, then all together
- **B01B**: HOLD: Hold the structure
- **B01C**: HOLD: Hold the structure
- **B01D**: HOLD: Hold the structure
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
- **B40**: SITE_HOLD: Hold on the shared site before any structure (the gap to span)
- **B41**: ASSEMBLE_IN: Structure drops into place on the shown empty site, then its focus parts glow
- **B42**: HOLD_HIGHLIGHT: Hold the structure and glow the focus components
- **B43**: EXPLODE: Take the assembly apart along its layers and back, focus components glowing
- **B44**: CARD: 2D card (text/arrows) supplied by the beat
- **B45**: HOLD_HIGHLIGHT: Hold the structure and glow the focus components
- **B46**: HOLD: Hold the structure
- **B47**: HIGHLIGHT_THEN_EXPLODE timing: cuts on sentence starts [1] · HIGHLIGHT_THEN_EXPLODE: Glow the focus components, then take the assembly apart and back
- **B48**: CARD: 2D card (text/arrows) supplied by the beat
- **B50**: HOLD_HIGHLIGHT: Hold the structure and glow the focus components
- **B51**: CARD: 2D card (text/arrows) supplied by the beat
- **B52**: EXPLODE: Take the assembly apart along its layers and back, focus components glowing
- **B53**: CARD: 2D card (text/arrows) supplied by the beat
- **B19**: CARD: 2D card (text/arrows) supplied by the beat
- **B20A**: HOLD_HIGHLIGHT: Hold the structure and glow the focus components
- **B20B**: HOLD_HIGHLIGHT: Hold the structure and glow the focus components
- **B20C**: HOLD: Hold the structure
- **B21**: CARD: 2D card (text/arrows) supplied by the beat
- **B20E**: HOLD_HIGHLIGHT: Hold the structure and glow the focus components
- **B22**: CARD: 2D card (text/arrows) supplied by the beat
- **B22B**: CARD: 2D card (text/arrows) supplied by the beat
- **B22C**: HOLD_HIGHLIGHT: Hold the structure and glow the focus components
- **B22D**: HOLD_HIGHLIGHT: Hold the structure and glow the focus components
- **B23C**: CARD: 2D card (text/arrows) supplied by the beat
- **B23D**: HOLD_HIGHLIGHT: Hold the structure and glow the focus components
- **B23E**: HOLD: Hold the structure
- **B24**: CARD: 2D card (text/arrows) supplied by the beat
- **B24B**: CARD: 2D card (text/arrows) supplied by the beat
- **B25**: CARD: 2D card (text/arrows) supplied by the beat
- **B26**: CARD: 2D card (text/arrows) supplied by the beat
- **B27**: HOLD: Hold the structure
- **B28**: CARD: 2D card (text/arrows) supplied by the beat
- **B29**: HOLD_HIGHLIGHT: Hold the structure and glow the focus components
- **B30**: CARD: 2D card (text/arrows) supplied by the beat
- **B31**: CARD: 2D card (text/arrows) supplied by the beat
- **B31A**: HOLD: Hold the structure
- **B31B**: HOLD_HIGHLIGHT: Hold the structure and glow the focus components
- **B31C**: CARD: 2D card (text/arrows) supplied by the beat
- **B31D**: HOLD: Hold the structure
- **B32**: COMPARE_SIDE_BY_SIDE: All variants at identical scale, captioned (layout chosen by planner/composition.py: STACK or ROW, gap)
- **B32L**: COMPARE_SIDE_BY_SIDE: All variants at identical scale, captioned (layout chosen by planner/composition.py: STACK or ROW, gap)
- **B32B**: CARD: 2D card (text/arrows) supplied by the beat
- **B33**: CARD: 2D card (text/arrows) supplied by the beat
- **B34**: HOLD: Hold the structure
- **B35**: CARD: 2D card (text/arrows) supplied by the beat

## Visual repairs (offline, before rendering)

- **B06 SC_013 stringer** at highlight_peak: OCCLUDED (share 0.14, core 0.00%) → **GHOST:plank** (share 0.81, core 1.67%). Evaluated: GHOST:plank PASS (share 0.81, core 1.67%, area 5.04% -> PASS)
- **B08 SC_016 stringer** at highlight_peak: OCCLUDED (share 0.14, core 0.00%) → **GHOST:plank** (share 0.81, core 1.67%). Evaluated: GHOST:plank PASS (share 0.81, core 1.67%, area 5.04% -> PASS)

## Comparison composition

- SC_001: SEQUENTIAL_COMPARISON, purpose detail, scale COMMON, smallest member 5.8 px, smallest model 88% of the frame width
- SC_002: SEQUENTIAL_COMPARISON, purpose detail, scale COMMON, smallest member 14.3 px, smallest model 88% of the frame width
- SC_003: SEQUENTIAL_COMPARISON, purpose detail, scale COMMON, smallest member 3.9 px, smallest model 88% of the frame width
- SC_004: SIDE_BY_SIDE_ROW gap 0.2, purpose overview, scale COMMON, smallest member 1.1 px, smallest model 26% of the frame width
- SC_070: SIDE_BY_SIDE_ROW gap 0.2, purpose overview, scale COMMON, smallest member 1.1 px, smallest model 26% of the frame width
  - candidate STACK gap 0.5: smallest model 25% of the frame width (< 25%)
  - candidate STACK gap 0.25: captions collide with the next row
  - candidate ROW gap 0.35: smallest model 24% of the frame width (< 25%)
  - candidate ROW gap 0.2: readable
- SC_071: SIDE_BY_SIDE_STACK gap 0.5, purpose overview, scale COMMON, smallest member 0.7 px, smallest model 33% of the frame width
  - candidate STACK gap 0.5: readable
  - candidate STACK gap 0.25: captions collide with the next row
  - candidate ROW gap 0.35: smallest model 24% of the frame width (< 25%)
  - candidate ROW gap 0.2: readable

## Warnings

- B01: declared COMPARE_VARIANTS, narration cues suggest ['SHOW_CONTEXT']
- B18: declared EXPLAIN_STRUCTURE, narration cues suggest ['EXPLAIN_DESIGN_CHANGE', 'SHOW_CONTEXT', 'SHOW_EVOLUTION']
- B52: declared EXPLAIN_STRUCTURE, narration cues suggest ['COMPARE_VARIANTS']
- B25: declared SHOW_CONTEXT, narration cues suggest ['SHOW_EVOLUTION']
- B31: declared SUMMARIZE_DIFFERENCES, narration cues suggest ['COMPARE_VARIANTS']
- B32B: declared SUMMARIZE_DIFFERENCES, narration cues suggest ['SHOW_CONTEXT']
