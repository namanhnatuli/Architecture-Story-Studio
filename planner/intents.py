"""Visual intent taxonomy (M5). Each intent lists visual strategies in preference order; a
strategy is a short sequence of existing templates. The planner takes the first strategy
whose preconditions hold (asset support, state compatibility, timing) and reports when
none does, instead of filling the timeline with an unrelated animation."""
import re

# strategy -> (shot templates, description)
STRATEGIES = {
    "SITE_HOLD": (["HOLD"], "Hold on the shared site before any structure (the gap to span)"),
    "ASSEMBLE_IN": (["REPLACE_PARTS", "HOLD"], "Structure drops into place on the shown empty site, then its focus parts glow"),
    "HOLD_HIGHLIGHT": (["HOLD"], "Hold the structure and glow the focus components"),
    "HOLD": (["HOLD"], "Hold the structure"),
    "CLOSEUP_HIGHLIGHT": (["HOLD", "HOLD"], "Establish the structure with the focus parts glowing, then a close-up framed on them"),
    "HIGHLIGHT_THEN_EXPLODE": (["HOLD", "EXPLODED_VIEW"], "Glow the focus components, then take the assembly apart and back"),
    "EXPLODE": (["EXPLODED_VIEW"], "Take the assembly apart along its layers and back, focus components glowing"),
    "HIGHLIGHT_REPLACE_HIGHLIGHT": (["HOLD", "REPLACE_PARTS", "HOLD"],
                                    "Glow the parts that will change, swap them on the shared frame, glow the new parts"),
    "REPLACE": (["REPLACE_PARTS"], "Swap only the differing parts on the shared frame"),
    "SEQUENTIAL_STATES": (["HOLD", "HOLD"], "Show A, cut, show B (states not geometrically compatible)"),
    "CLOSEUP_EXPLODE": (["HOLD", "EXPLODED_VIEW"],
                        "Establish the structure, then a close-up in which only the focus pieces separate, showing "
                        "their individual shape"),
    "COMPARE_SIDE_BY_SIDE": (["SIDE_BY_SIDE"], "All variants at identical scale, captioned (layout chosen by "
                             "planner/composition.py: STACK or ROW, gap)"),
    "FOCUSED_PAIR": (["SIDE_BY_SIDE"], "Only the two variants the beat focuses on, at identical scale"),
    "DETAIL_THEN_OVERVIEW": (["HOLD", "SIDE_BY_SIDE"], "Each variant alone under one locked camera, then all together"),
    "SEQUENTIAL_COMPARISON": (["HOLD"], "One variant at a time under one shared locked camera (same scale), captioned"),
    "CONTINUE_COMPARISON": (["SIDE_BY_SIDE"], "Stay on the comparison, glow what differs"),
    "CARD": (["MOTION_GRAPHICS"], "2D card (text/arrows) supplied by the beat"),
}

INTENTS = {
    "INTRODUCE_ARCHITECTURE": {"strategies": ["ASSEMBLE_IN", "HOLD_HIGHLIGHT", "HOLD"],
                               "doc": "Introduce a structure: it appears (if the site was shown empty) or holds; focus parts glow"},
    "EXPLAIN_STRUCTURE": {"strategies": ["HIGHLIGHT_THEN_EXPLODE", "EXPLODE", "HOLD_HIGHLIGHT"],
                          "doc": "How the parts are arranged: exploded view with the focus parts highlighted"},
    "SHOW_COMPONENT": {"strategies": ["CLOSEUP_EXPLODE", "CLOSEUP_HIGHLIGHT", "HOLD_HIGHLIGHT"],
                       "doc": "One component group: close-up and highlight; pieces read as pieces separate"},
    "EXPLAIN_DESIGN_CHANGE": {"strategies": ["HIGHLIGHT_REPLACE_HIGHLIGHT", "REPLACE", "SEQUENTIAL_STATES"],
                              "doc": "A -> B: replace compatible parts on a shared frame, else show the states separately"},
    "COMPARE_VARIANTS": {"strategies": ["COMPARE_SIDE_BY_SIDE", "FOCUSED_PAIR", "DETAIL_THEN_OVERVIEW",
                                        "SEQUENTIAL_COMPARISON", "SEQUENTIAL_STATES"],
                         "doc": "Variants at identical scale; the clearest readable composition (M5.5)"},
    "SHOW_EVOLUTION": {"strategies": ["SEQUENTIAL_STATES"], "needs_verified_chronology": True,
                       "doc": "A sequence in time: only with editorially approved chronology claims"},
    "EXPLAIN_CAUSE_EFFECT": {"strategies": ["CARD"], "needs_graphic": True,
                             "doc": "Cause and effect needs force/flow diagrams: only a supplied 2D card is supported"},
    "SHOW_CONTEXT": {"strategies": ["SITE_HOLD", "CARD"],
                     "doc": "Context: the shared site, or a supplied 2D card (maps / sourced imagery are not supported)"},
    "SUMMARIZE_DIFFERENCES": {"strategies": ["CONTINUE_COMPARISON", "COMPARE_SIDE_BY_SIDE", "SEQUENTIAL_COMPARISON"],
                              "doc": "Close on the comparison, glowing the differing parts"},
    "EXPLAIN_LOAD_PATH": {"strategies": ["HOLD_HIGHLIGHT", "HOLD"], "needs_annotations": True,
                          "doc": "M6: how a structure carries load - a steady model with semantic annotations "
                                 "(conceptual load path, load/reaction arrows, labels; planner/annotations.py)"},
}

MISSING_CAPABILITIES = {
    "MAP_OR_IMAGERY": ("No map or sourced-imagery renderer; only self-made 2D cards (engine/diagram.py)",
                       "Supply a MOTION_GRAPHICS card spec in the beat, or add a map/image card template (~1-2 days)"),
    "FORCE_DIAGRAM": ("No supplied 2D card; force arrows on 3D models are semantic annotations (M6)",
                      "Use intent EXPLAIN_LOAD_PATH with beat annotations (planner/annotations.py), or supply a card"),
    "VERIFIED_CHRONOLOGY": ("SHOW_EVOLUTION needs editorially approved chronology claims",
                            "Approve the chronology claims, or reframe the beat as COMPARE_VARIANTS"),
}

# Rule-based cross-check of the declared intent (keywords in the narration); a disagreement is a
# warning for the author, never a silent override.
_KEYWORDS = [
    ("COMPARE_VARIANTS", r"\b(side by side|compare|compared|versus|vs\.?|three bridges|both)\b"),
    ("EXPLAIN_DESIGN_CHANGE", r"\b(change[sd]?|instead|replace[sd]?|swap|switch)\b"),
    ("SUMMARIZE_DIFFERENCES", r"\b(in summary|to sum up|three arrangements|each form|differences)\b"),
    ("EXPLAIN_STRUCTURE", r"\b(taken apart|arrangement|made of|form[s]? a|assembled|works differently|joined)\b"),
    ("SHOW_CONTEXT", r"\b(gap|bank|site|river|valley)\b"),
    ("SHOW_EVOLUTION", r"\b(later|over time|evolved|replaced by|centur(y|ies))\b"),
]


def suggest(narration):
    """Intents whose cue words appear in the narration (ordered)."""
    text = narration.lower()
    return [intent for intent, pattern in _KEYWORDS if re.search(pattern, text)]


def check(beat):
    """Warning text if the declared intent is not supported by any cue in the narration."""
    hits = suggest(beat.get("narration", ""))
    declared = beat.get("narrative_intent")
    if hits and declared not in hits and declared not in ("INTRODUCE_ARCHITECTURE", "SHOW_COMPONENT", "EXPLAIN_LOAD_PATH"):
        return f"declared {declared}, narration cues suggest {hits}"
    return None
