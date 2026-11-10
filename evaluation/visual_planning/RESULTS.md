# Visual-planning evaluation (M5.5)

33/33 cases pass. Small curated dataset: it checks that these cases behave as specified; it is not evidence of unrestricted natural-language understanding.

| Dimension | Checks passed |
|---|---|
| narrative_relevance | 32/32 |
| asset_selection | 9/9 |
| target_selection | 25/25 |
| animation_suitability | 21/21 |
| camera_readability | 5/5 |
| target_visibility | 9/9 |
| timing_feasibility | 2/2 |
| evidence_compatibility | 5/5 |
| visual_continuity | 5/5 |
| cross_family_reuse | 3/3 |

| Kind | Cases passed |
|---|---|
| positive | 14/14 |
| negative | 10/10 |
| ambiguous | 3/3 |
| missing_capability | 6/6 |

| Family | Cases passed |
|---|---|
| bridge | 24/24 |
| floating | 3/3 |
| roof | 6/6 |

## Cases

- **BR-POS-01** (positive, bridge) Introduce the timber beam bridge on the empty site; its stringers must read (hidden under the deck): **PASS**
  - ok [narrative_relevance] status COVERED (want COVERED)
  - ok [narrative_relevance] strategy ASSEMBLE_IN (want ['ASSEMBLE_IN'])
  - ok [asset_selection] timber_beam_bridge: REUSE_EXISTING bridge_timber_beam_01 (want REUSE_EXISTING bridge_timber_beam_01)
  - ok [target_selection] stringer roles ['stringer'] (want ['stringer'])
  - ok [animation_suitability] templates ['REPLACE_PARTS', 'HOLD'] (want ['REPLACE_PARTS', 'HOLD'])
  - ok [visual_continuity] cuts ['match', 'match'] (want ['match', 'match'])
  - ok [target_visibility] every concept reads: True (want True)
  - ok [target_visibility] repairs ['GHOST:plank'] (want GHOST:plank)
  - ok [evidence_compatibility] evidence INTERNAL_PREVIEW
- **BR-POS-02** (positive, bridge) Explain the timber layers; hidden layers read in the exploded view of the same beat (no repair needed): **PASS**
  - ok [narrative_relevance] status COVERED (want COVERED)
  - ok [narrative_relevance] strategy HIGHLIGHT_THEN_EXPLODE (want ['HIGHLIGHT_THEN_EXPLODE'])
  - ok [animation_suitability] templates ['HOLD', 'EXPLODED_VIEW'] (want ['HOLD', 'EXPLODED_VIEW'])
  - ok [visual_continuity] cuts ['match', 'match'] (want ['match', 'match'])
  - ok [target_visibility] every concept reads: True (want True)
  - ok [target_visibility] repairs [] (want None)
- **BR-POS-03** (positive, bridge) Voussoirs and keystone: frontal close-up of arch 2, pieces separate (Test C): **PASS**
  - ok [narrative_relevance] status COVERED (want COVERED)
  - ok [narrative_relevance] strategy CLOSEUP_EXPLODE (want ['CLOSEUP_EXPLODE'])
  - ok [target_selection] voussoir roles ['voussoir'] (want ['voussoir'])
  - ok [target_selection] keystone roles ['keystone'] (want ['keystone'])
  - ok [animation_suitability] templates ['HOLD', 'EXPLODED_VIEW'] (want ['HOLD', 'EXPLODED_VIEW'])
  - ok [camera_readability] camera {'mode': 'SIDE_ELEVATION', 'preset': 'ELEVATION', 'focus': ['stone_arch_bridge_arch2_keystone', 'stone_arch_bridge_arch2_voussoir01', 'stone_arch_bridge_arch2_voussoir02', 'stone_arch_bridge_arch2_voussoir03', 'stone_arch_bridge_arch2_voussoir04', 'stone_arch_bridge_arch2_voussoir05', 'stone_arch_bridge_arch2_voussoir06', 'stone_arch_bridge_arch2_voussoir08', 'stone_arch_bridge_arch2_voussoir09', 'stone_arch_bridge_arch2_voussoir10', 'stone_arch_bridge_arch2_voussoir11', 'stone_arch_bridge_arch2_voussoir12', 'stone_arch_bridge_arch2_voussoir13'], 'safe_band': 0.1, 'group': 2, 'build_variants': ['stone_arch_bridge']} (want {'shot': -1, 'focus_count': 13, 'preset': 'ELEVATION'})
  - ok [target_visibility] every concept reads: True (want True)
- **BR-POS-04** (positive, bridge) Pratt to Warren: swap only the web on the shared frame: **PASS**
  - ok [narrative_relevance] status COVERED (want COVERED)
  - ok [narrative_relevance] strategy HIGHLIGHT_REPLACE_HIGHLIGHT (want ['HIGHLIGHT_REPLACE_HIGHLIGHT'])
  - ok [asset_selection] pratt_truss: REUSE_EXISTING bridge_steel_truss_pratt_01 (want REUSE_EXISTING bridge_steel_truss_pratt_01)
  - ok [asset_selection] warren_truss: REUSE_EXISTING bridge_steel_truss_warren_01 (want REUSE_EXISTING bridge_steel_truss_warren_01)
  - ok [animation_suitability] templates ['HOLD', 'REPLACE_PARTS', 'HOLD'] (want ['HOLD', 'REPLACE_PARTS', 'HOLD'])
  - ok [visual_continuity] cuts ['match', 'match', 'match'] (want ['match', 'match', 'match'])
  - ok [target_visibility] every concept reads: True (want True)
- **BR-POS-05** (positive, bridge) Compare three long bridges at 640x360: no simultaneous layout reads, one at a time at one scale (Test B): **PASS**
  - ok [narrative_relevance] status COVERED (want COVERED)
  - ok [narrative_relevance] strategy SEQUENTIAL_COMPARISON (want ['SEQUENTIAL_COMPARISON'])
  - ok [animation_suitability] templates ['HOLD', 'HOLD', 'HOLD'] (want ['HOLD', 'HOLD', 'HOLD'])
  - ok [camera_readability] composition [{'layout': 'SEQUENTIAL_COMPARISON', 'scale': 'COMMON'}, {'layout': 'SEQUENTIAL_COMPARISON', 'scale': 'COMMON'}, {'layout': 'SEQUENTIAL_COMPARISON', 'scale': 'COMMON'}]
  - ok [visual_continuity] one locked camera for the beat's shots
  - ok [narrative_relevance] report mentions 'no simultaneous layout'
- **BR-POS-06** (positive, bridge) Summarise: an overview only needs the overall forms to read: **PASS**
  - ok [narrative_relevance] status COVERED (want COVERED)
  - ok [narrative_relevance] strategy COMPARE_SIDE_BY_SIDE (want ['COMPARE_SIDE_BY_SIDE'])
  - ok [camera_readability] composition [{'layout': 'SIDE_BY_SIDE_STACK', 'purpose': 'overview', 'scale': 'COMMON'}]
- **BR-POS-07** (positive, bridge) Changing the narrative changes the visual: B5 as SHOW_COMPONENT of the diagonals (SYNTHETIC edit): **PASS**
  - ok [narrative_relevance] status COVERED (want COVERED)
  - ok [narrative_relevance] strategy CLOSEUP_HIGHLIGHT (want ['CLOSEUP_HIGHLIGHT'])
  - ok [target_selection] diagonal_members roles ['truss_diagonal'] (want ['truss_diagonal'])
  - ok [camera_readability] camera {'mode': 'COMPONENT_CLOSEUP', 'preset': 'BRIDGE_THREE_QUARTER', 'focus': ['steel_truss_bridge_span1_diagonals_north', 'steel_truss_bridge_span1_diagonals_south', 'steel_truss_bridge_span2_diagonals_north', 'steel_truss_bridge_span2_diagonals_south'], 'safe_band': 0.1, 'group': 2, 'build_variants': ['steel_truss_bridge']} (want {'shot': -1, 'mode': 'COMPONENT_CLOSEUP'})
  - ok [target_visibility] every concept reads: True (want True)
- **RF-POS-01** (positive, roof) Introduce roof A on the house (legacy roof through the adapter): **PASS**
  - ok [narrative_relevance] status COVERED (want COVERED)
  - ok [narrative_relevance] strategy HOLD (want ['HOLD'])
  - ok [asset_selection] low_pitch_gable_roof: ADAPT_EXISTING_ASSET legacy_roof_evolution_roof_A (want ADAPT_EXISTING_ASSET legacy_roof_evolution_roof_A)
  - ok [animation_suitability] templates ['HOLD'] (want ['HOLD'])
- **RF-POS-02** (positive, roof) Explain rafters and ridge beam: with the steep roof sharing the camera (R3) the ridge is too small, so the explode is reframed: **PASS**
  - ok [narrative_relevance] status COVERED (want COVERED)
  - ok [narrative_relevance] strategy EXPLODE (want ['EXPLODE'])
  - ok [target_selection] rafters roles ['rafters'] (want ['rafters'])
  - ok [target_selection] ridge_beam roles ['ridge_beam'] (want ['ridge_beam'])
  - ok [animation_suitability] templates ['EXPLODED_VIEW'] (want ['EXPLODED_VIEW'])
  - ok [target_visibility] every concept reads: True (want True)
  - ok [target_visibility] repairs ['REFRAME'] (want REFRAME)
- **RF-POS-03** (positive, roof) Replace the roof assembly on the same walls: **PASS**
  - ok [narrative_relevance] status COVERED (want COVERED)
  - ok [asset_selection] steep_gable_roof: ADAPT_EXISTING_ASSET legacy_roof_evolution_roof_B (want ADAPT_EXISTING_ASSET legacy_roof_evolution_roof_B)
  - ok [animation_suitability] templates ['REPLACE_PARTS'] (want ['REPLACE_PARTS'])
- **RF-POS-04** (positive, roof) Compare two compact houses: a ROW reads, no fallback needed: **PASS**
  - ok [narrative_relevance] status COVERED (want COVERED)
  - ok [narrative_relevance] strategy COMPARE_SIDE_BY_SIDE (want ['COMPARE_SIDE_BY_SIDE'])
  - ok [camera_readability] composition [{'layout': 'SIDE_BY_SIDE_ROW', 'scale': 'COMMON'}]
- **NEG-01** (negative, bridge) A keystone requested on the timber bridge (SYNTHETIC): **PASS**
  - ok [target_selection] status INVALID_REQUEST (want INVALID_REQUEST)
  - ok [target_selection] report mentions "'keystone'"
- **NEG-02** (negative, bridge) Forced REPLACE from timber to stone (no shared frame): **PASS**
  - ok [animation_suitability] status INVALID_REQUEST (want INVALID_REQUEST)
  - ok [animation_suitability] report mentions 'share no frame'
- **NEG-03** (negative, bridge) Claim without verified evidence: **PASS**
  - ok [evidence_compatibility] status EVIDENCE_BLOCKED (want EVIDENCE_BLOCKED)
- **NEG-04** (negative, bridge) 1.5 s for an exploded explanation: **PASS**
  - ok [timing_feasibility] status TIMING_CONFLICT (want TIMING_CONFLICT)
  - ok [timing_feasibility] report mentions 'nothing was truncated'
- **NEG-05** (negative, bridge) Evolution without editorially approved chronology: **PASS**
  - ok [evidence_compatibility] status EVIDENCE_BLOCKED (want EVIDENCE_BLOCKED)
- **NEG-06** (negative, roof) A keystone requested on a roof (cross-family negative): **PASS**
  - ok [target_selection] status INVALID_REQUEST (want INVALID_REQUEST)
  - ok [target_selection] report mentions "'keystone'"
- **AMB-01** (ambiguous, bridge) 'beam' on a timber bridge matches stringers and cap beams: **PASS**
  - ok [target_selection] status INVALID_REQUEST (want INVALID_REQUEST)
  - ok [target_selection] report mentions 'ambiguous'
- **AMB-02** (ambiguous, bridge) 'member' on a truss matches chords, posts, verticals and diagonals: **PASS**
  - ok [target_selection] status INVALID_REQUEST (want INVALID_REQUEST)
  - ok [target_selection] report mentions 'ambiguous'
- **AMB-03** (ambiguous, bridge) Narration cues disagree with the declared intent: warned, never silently overridden (SYNTHETIC narration): **PASS**
  - ok [narrative_relevance] status COVERED (want COVERED)
  - ok [narrative_relevance] strategy COMPARE_SIDE_BY_SIDE (want ['COMPARE_SIDE_BY_SIDE'])
  - ok [narrative_relevance] report mentions 'declared SUMMARIZE_DIFFERENCES'
- **MISS-01** (missing_capability, bridge) Bascule (movable) bridge: no generator, nothing substituted: **PASS**
  - ok [asset_selection] status MISSING_ASSET (want MISSING_ASSET)
  - ok [asset_selection] report mentions 'NEW_FAMILY_GENERATOR'
- **MISS-02** (missing_capability, bridge) Cause and effect needs a force diagram: **PASS**
  - ok [animation_suitability] status MISSING_TEMPLATE (want MISSING_TEMPLATE)
  - ok [animation_suitability] report mentions 'FORCE_DIAGRAM'
- **MISS-03** (missing_capability, roof) Context for a house without a site model or map: **PASS**
  - ok [animation_suitability] status MISSING_TEMPLATE (want MISSING_TEMPLATE)
  - ok [animation_suitability] report mentions 'MAP_OR_IMAGERY'
- **MISS-04** (missing_capability, bridge) A historically verified arch: illustrative assets cannot stand in: **PASS**
  - ok [asset_selection] status EVIDENCE_BLOCKED (want EVIDENCE_BLOCKED)
  - ok [asset_selection] report mentions 'HISTORICALLY_VERIFIED'
- **M6-POS-01** (positive, bridge) Audio-locked arch beat: load arrow, compression path, callout and inclined reactions all anchor and place: **PASS**
  - ok [narrative_relevance] status COVERED (want COVERED)
  - ok [narrative_relevance] strategy HOLD_HIGHLIGHT (want ['HOLD_HIGHLIGHT'])
  - ok [evidence_compatibility] evidence APPROVED
  - ok [target_selection] annotation B5_load: PLACED (want PLACED)
  - ok [target_selection] annotation B5_thrust: PLACED (want PLACED)
  - ok [target_selection] annotation B5_comp: PLACED (want PLACED)
  - ok [target_selection] annotation B5_react: PLACED (want PLACED)
- **M6-POS-02** (positive, bridge) 'One at a time' narration on a sequential comparison is consistent; one locked camera; per-model callouts: **PASS**
  - ok [narrative_relevance] strategy SEQUENTIAL_COMPARISON (want ['SEQUENTIAL_COMPARISON'])
  - ok [visual_continuity] one locked camera for the beat's shots
  - ok [target_selection] annotation B7_beam: PLACED (want PLACED)
  - ok [target_selection] annotation B7_arch: PLACED (want PLACED)
  - ok [target_selection] annotation B7_truss: PLACED (want PLACED)
  - ok [narrative_relevance] SEQUENTIAL: ['CONSISTENT'] (want CONSISTENT)
- **M6-NEG-01** (negative, bridge) A tension statement on a diagonal backed only by the chord claim (CLM_613) is refused: **PASS**
  - ok [evidence_compatibility] planning error: beat B6 annotation B6_bottom: claim CLM_613 does not state a force in 'diagonal_members' (its components: ['truss_chord'])
- **M6-NEG-02** (negative, bridge) 'Side by side' narration while the models are shown one at a time is a blocking contradiction (M5.5 B7): **PASS**
  - ok [narrative_relevance] strategy SEQUENTIAL_COMPARISON (want ['SEQUENTIAL_COMPARISON'])
  - ok [narrative_relevance] SIMULTANEOUS: ['CONTRADICTION'] (want CONTRADICTION)
- **M6-MISS-01** (missing_capability, bridge) An annotation anchored to a component the arch does not have (truss chord) fails instead of floating: **PASS**
  - ok [target_selection] status PARTIALLY_COVERED (want PARTIALLY_COVERED)
  - ok [target_selection] annotation B5_comp: FAILED (want FAILED)
  - ok [target_selection] annotation B5_react: PLACED (want PLACED)
  - ok [target_selection] report mentions 'anchor target not found'
- **SEQ-NEG-01** (missing_capability, bridge) A SEQUENCE on an asset that does not declare it is refused (MISSING_TEMPLATE), never faked with a hold: **PASS**
  - ok [animation_suitability] status MISSING_TEMPLATE (want MISSING_TEMPLATE)
  - ok [animation_suitability] report mentions 'does not support SEQUENCE'
- **FLOAT-SEQ-01** (positive, floating) A floating platform in section sinks by a calculated amount: SEQUENCE with REVEAL and MOVE on the same parts (the beat's own labels are left out: the case is about the steps): **PASS**
  - ok [animation_suitability] status COVERED (want COVERED)
  - ok [narrative_relevance] strategy SEQUENCE (want ['SEQUENCE'])
- **FLOAT-SEQ-02** (negative, floating) Conceptual motion (OSCILLATE) without the mandatory label is refused, never shown as if simulated: **PASS**
  - ok [animation_suitability] status INVALID_REQUEST (want INVALID_REQUEST)
  - ok [animation_suitability] report mentions 'motion_label'
- **FLOAT-SEQ-03** (negative, floating) Conceptual motion with the label but no on-screen NOTE is refused: the label must be seen for the whole beat: **PASS**
  - ok [animation_suitability] status INVALID_REQUEST (want INVALID_REQUEST)
  - ok [animation_suitability] report mentions 'NOTE'
