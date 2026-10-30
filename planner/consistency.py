"""Narration <-> visual consistency (M6; deterministic, rule-based, no language model).

Every narrated sentence is checked against what the plan shows while it is spoken (its
time window from the measured or estimated sentence spans, intersected with the beat's
shots). Rules fire on cue phrases; a rule that cannot decide reports UNCERTAIN instead of
guessing. A CONTRADICTION is a coverage issue and a validate-plan error (fail closed).

  SIMULTANEOUS   "side by side", "seen/shown/all ... together", "at once", "at the same time",
                 "simultaneously" (a bare "together" is not a cue: "pressing the stones together")
                 -> a SIDE_BY_SIDE shot must be on screen during the sentence
  SEQUENTIAL     "one at a time", "one by one", "each in turn" -> no SIDE_BY_SIDE shot then
  DEICTIC        "this/that/these/those component|part|member|piece|stone|beam|element"
                 -> a glow or an annotation must point at something during the sentence
  COLOUR         a colour word -> an annotation (or glow) of that colour must be visible
  SIDE           "left"/"right" -> the visible annotation targets / compared model on that
                 side of the frame, else UNCERTAIN
  TRANSFORMATION "turns into", "becomes", "is replaced by", "swaps", "transforms"
                 -> no hard cut between two different structures during the sentence
  ARROWS         "these arrows" / "this arrow" -> arrows visible during the sentence;
                 a generic "the arrows" is reported UNCERTAIN (they may be earlier ones)
"""
import re

RULES = {
    "SIMULTANEOUS": r"\b(side by side|(seen|shown|all|them|models|structures|bridges) together|at once|"
                    r"at the same time|simultaneous(ly)?)\b",
    "SEQUENTIAL": r"\b(one at a time|one by one|each in turn)\b",
    "DEICTIC": r"\b(this|that|these|those) (component|part|member|piece|stone|beam|element)s?\b",
    "SIDE": r"\b(left|right)\b",
    "TRANSFORMATION": r"\b(turns into|becomes|is replaced by|swaps?|transforms?)\b",
    "ARROWS_SPECIFIC": r"\b(these|this) arrows?\b",
    "ARROWS_GENERIC": r"\bthe arrows?\b",
}
VERDICTS = ("CONSISTENT", "CONTRADICTION", "UNCERTAIN")


def _colour_words(style):
    out = {}
    for key, words in (style.get("color_names") or {}).items():
        for w in words:
            out[w] = key
    return out


def _windows(beat_shots, span):
    """Plan shots overlapping a sentence span (beat seconds) with the overlap in shot seconds."""
    out = []
    for ps in beat_shots:
        s0 = ps["timing"]["beat_offset_seconds"]
        s1 = s0 + ps["timing"]["duration_seconds"]
        lo, hi = max(span[0], s0), min(span[1], s1)
        if hi > lo:
            out.append((ps, lo - s0, hi - s0))
    return out


def _visible_annotations(ps, t0, t1):
    return [a for a in ((ps.get("annotations") or {}).get("items") or [])
            if a["appear"] < t1 and a["disappear"] > t0 and a["type"] not in ("TAG", "NOTE")]


def _glowing(ps, t0, t1):
    h = (ps["shot"].get("animation") or {}).get("highlight") or {}
    if not isinstance(h, dict) or not h.get("components"):
        return False
    start = float(h.get("start_seconds", 0.0))
    end = start + float(h.get("rise_seconds", 0)) + float(h.get("hold_seconds", 0)) + float(h.get("fall_seconds", 0))
    return start < t1 and end > t0


def check_plan(plan, doc, offsets, style):
    """Rows for every sentence that triggers a rule: {beat_id, sentence, text, rule, verdict, detail}."""
    from planner import timing as T
    colours = _colour_words(style)
    colour_re = r"\b(" + "|".join(sorted(map(re.escape, colours), key=len, reverse=True)) + r")\b" if colours else None
    rows = []
    for beat in doc["beats"]:
        bid = beat["beat_id"]
        shots = [ps for ps in plan["shots"] if ps["beat_id"] == bid]
        if not shots:
            continue
        sentences = T.split_sentences(beat["narration"])
        for k, text in enumerate(sentences):
            span = offsets[bid][k] if k < len(offsets.get(bid, [])) else (0.0, 1e9)
            win = _windows(shots, span)
            low = text.lower()

            def row(rule, verdict, detail):
                rows.append({"beat_id": bid, "sentence": k, "text": text, "rule": rule, "verdict": verdict,
                             "detail": detail, "shots": [ps["shot_id"] for ps, _, _ in win]})
            templates = {ps["template"] for ps, _, _ in win}
            if re.search(RULES["SIMULTANEOUS"], low):
                if "SIDE_BY_SIDE" in templates:
                    row("SIMULTANEOUS", "CONSISTENT", "a side-by-side comparison is on screen")
                else:
                    row("SIMULTANEOUS", "CONTRADICTION", f"narration says the models are seen together, but the "
                        f"shots during the sentence are {sorted(templates)} (one model at a time); reword "
                        f"(e.g. \"Let's compare them one at a time\") or show them side by side")
            if re.search(RULES["SEQUENTIAL"], low):
                if "SIDE_BY_SIDE" in templates:
                    row("SEQUENTIAL", "CONTRADICTION", "narration says one at a time, but a side-by-side shot is on screen")
                else:
                    row("SEQUENTIAL", "CONSISTENT", "one model per shot")
            if re.search(RULES["DEICTIC"], low):
                pointed = [a["id"] for ps, t0, t1 in win for a in _visible_annotations(ps, t0, t1)]
                glow = any(_glowing(ps, t0, t1) for ps, t0, t1 in win)
                if pointed or glow:
                    row("DEICTIC", "CONSISTENT", "target shown by " + (", ".join(pointed) if pointed else "the glow"))
                else:
                    row("DEICTIC", "CONTRADICTION", "the sentence points at a component, but nothing is highlighted "
                        "or annotated while it is spoken")
            if colour_re:
                for m in re.finditer(colour_re, low):
                    key = colours[m.group(1)]
                    shown = set()
                    for ps, t0, t1 in win:
                        for a in _visible_annotations(ps, t0, t1):
                            shown |= {a["type"] == "LOAD_ARROW" and "LOAD", a["type"] == "REACTION_ARROW" and "REACTION",
                                      a["type"] == "HIGHLIGHT_REGION" and "REGION", a.get("force"),
                                      a["type"] == "CONCEPTUAL_LOAD_PATH" and (a.get("style") or "LOAD")}
                            if a["type"] == "TENSION_COMPRESSION_LEGEND":
                                shown |= {"COMPRESSION", "TENSION"}
                        if _glowing(ps, t0, t1):
                            shown.add("highlight")
                    if key in shown:
                        row("COLOUR", "CONSISTENT", f"'{m.group(1)}' = {key}, visible")
                    else:
                        row("COLOUR", "CONTRADICTION", f"narration names the colour '{m.group(1)}' ({key}), but no "
                            f"{key.lower()} graphic is visible during the sentence")
            if re.search(RULES["SIDE"], low):
                row("SIDE", "UNCERTAIN", _side_detail(win, low))
            if re.search(RULES["TRANSFORMATION"], low):
                cuts = [(a, b) for (a, _, _), (b, _, _) in zip(win, win[1:])
                        if b["cut_from_previous"] == "hard" and a["states"][-1] != b["states"][0]]
                if cuts:
                    row("TRANSFORMATION", "CONTRADICTION", "narration describes a transformation, but the visual cuts "
                        f"between different structures ({cuts[0][0]['shot_id']} -> {cuts[0][1]['shot_id']})")
                elif "REPLACE_PARTS" in templates:
                    row("TRANSFORMATION", "CONSISTENT", "a REPLACE_PARTS transformation is on screen")
                else:
                    row("TRANSFORMATION", "UNCERTAIN", "transformation wording without a shown transformation (may be "
                        "figurative); editorial check")
            if re.search(RULES["ARROWS_SPECIFIC"], low):
                arrows = [a["id"] for ps, t0, t1 in win for a in _visible_annotations(ps, t0, t1)
                          if a["type"] in ("LOAD_ARROW", "REACTION_ARROW", "CONCEPTUAL_LOAD_PATH")]
                row("ARROWS", "CONSISTENT" if arrows else "CONTRADICTION",
                    f"arrows visible: {arrows}" if arrows else "the sentence points at arrows, none is visible")
            elif re.search(RULES["ARROWS_GENERIC"], low):
                row("ARROWS", "UNCERTAIN", "generic reference to the arrows (shown in earlier beats); editorial check")
    return rows


def _side_detail(win, low):
    """left/right: report what is on each side (an automatic verdict needs the referent)."""
    parts = []
    for ps, t0, t1 in win:
        for a in _visible_annotations(ps, t0, t1):
            xs = [x["screen"][0] for x in a["anchors"]]
            if xs:
                side = "left" if sum(xs) / len(xs) < 0.5 else "right"
                parts.append(f"{a['id']} on the {side}")
    return ("left/right wording; " + (", ".join(parts) if parts else "no annotation to locate") +
            " - confirm the referent in review")


def summary(rows):
    return {v: sum(1 for r in rows if r["verdict"] == v) for v in VERDICTS}
