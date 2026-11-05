"""Authoring source of "How Gothic Cathedrals Reached Impossible Heights".

    python3 projects/gothic-cathedral-heights/script/story.py

writes script/narration.json, script/visual_beats.json and script/chapters.json from the chapters
and beats below, so narration and visual beats always carry the same sentences. Every fact beat cites
claims from research/sources.json. Card coordinates: x, y in 0..1 of the frame (origin bottom-left);
nothing below y 0.2 (the subtitle zone ends at 0.17). The 3D beats need the new cathedral family
(gothic_cathedral_section, romanesque_church_section in config/visual_vocabulary.json, not generated
yet), so `plan-visuals` reports NEW_ASSET_REQUIRED for them until the owner has approved the script.
"""
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
ASPECT = 16 / 9
INK, MUTED, FAINT = "#24231F", "#55524A", "#8A867C"
STONE, WOOD, GLASS = "#B9A887", "#8C654D", "#5E86A6"
THRUST, ACCENT = "#C25110", "#1E5C96"
CHAR_W = 0.26   # text width per character in units of the text size (measured from card QA boxes)


class Card:
    def __init__(self, name):
        self.name, self.elements = name, []

    def add(self, kind, sentence=0, until=None, **kw):
        e = {"id": f"{self.name}_{len(self.elements):02d}", "kind": kind, "sentence": sentence, **kw}
        if until is not None:
            e["until"] = until
        self.elements.append(e)
        return self

    def text(self, text, x, y, size=0.034, sentence=0, align="CENTER", color=INK, plate=False, until=None, word=None):
        """word: appear when that word of the sentence is spoken (Whisper alignment)."""
        return self.add("text", sentence, until, text=text, position=[round(x, 4), round(y, 4)], size=size,
                        align=align, color=color, plate=plate, **({"word": word} if word else {}))

    def rect(self, box, color=None, border=None, sentence=0, border_width=0.004, dash=None, until=None, layer=0):
        kw = {"box": [round(v, 4) for v in box], "layer": layer}
        if color:
            kw["color"] = color
        if border:   # without a fill colour the engine draws the outline only
            kw.update(border=border, border_width=border_width)
        if dash:
            kw["dash"] = dash
        return self.add("rect", sentence, until, **kw)

    def line(self, points, color=INK, width=0.005, sentence=0, dash=None, until=None, layer=0):
        kw = {"points": [[round(x, 4), round(y, 4)] for x, y in points], "color": color, "width": width, "layer": layer}
        if dash:
            kw["dash"] = dash
        return self.add("line", sentence, until, **kw)

    def arrow(self, start, end, color=INK, width=0.007, sentence=0, until=None):
        return self.add("arrow", sentence, until, start=[round(v, 4) for v in start], end=[round(v, 4) for v in end],
                        color=color, width=width)

    def circle(self, center, radius=0.012, color=INK, sentence=0, until=None):
        return self.add("circle", sentence, until, center=[round(v, 4) for v in center], radius=radius, color=color)

    def polygon(self, points, color, border=None, sentence=0, until=None, layer=0):
        kw = {"points": [[round(x, 4), round(y, 4)] for x, y in points], "color": color, "layer": layer}
        if border:
            kw.update(border=border, border_width=0.0025)
        return self.add("polygon", sentence, until, **kw)

    def tag(self, text, sentence=0):
        return self.text(text, 0.055, 0.915, 0.024, sentence, align="LEFT", color=MUTED, plate=True)

    def spec(self):
        return {"fade_seconds": 0.35, "elements": self.elements}


def round_arch(span, n=32):
    """Semicircular arch as (u, v) from foot to foot, in height units: u across, v up."""
    return [(-span / 2 * math.cos(math.pi * k / n), span / 2 * math.sin(math.pi * k / n)) for k in range(n + 1)]


def pointed_arch(span, rise, n=16):
    """Two arcs of a circle that meet at a point, with the given span and rise."""
    r = (span * span / 4 + rise * rise) / span
    top = math.acos((r - span / 2) / r)
    left = [(r - span / 2 - r * math.cos(top * k / n), r * math.sin(top * k / n)) for k in range(n + 1)]
    return left + [(-u, v) for u, v in reversed(left[:-1])]


def catenary(span, rise, n=32):
    """A hanging chain turned upside down, with the given span and rise."""
    lo, hi = 0.01, 10.0
    for _ in range(60):
        a = (lo + hi) / 2
        if a * (math.cosh(span / 2 / a) - 1) > rise:
            lo = a
        else:
            hi = a
    return [(u, rise - a * (math.cosh(u / a) - 1)) for u in (-span / 2 + span * k / n for k in range(n + 1))]


def place(curve, cx, y0, flip=False):
    """Curve in height units -> card coordinates (x scaled by the aspect); flip hangs it from y0."""
    return [[cx + u / ASPECT, y0 - v if flip else y0 + v] for u, v in curve]


def voussoirs(c, cx, y0, span, rise, thick, n, sentence, color=STONE, border="#7A6E58", until=None):
    """Ring of wedge-shaped stones around a pointed opening."""
    inner = pointed_arch(span, rise, n)
    outer = pointed_arch(span + 2 * thick, rise + thick * 1.25, n)
    a, b = place(inner, cx, y0), place(outer, cx, y0)
    for k in range(len(a) - 1):
        c.polygon([a[k], b[k], b[k + 1], a[k + 1]], color, border=border, sentence=sentence, until=until, layer=1)


def timeline(name, events, bands, start, end, ticks, extra=None):
    """Axis start-end; event labels go to the first free row, so two labels never overlap. An event is
    (year, label, sentence[, word]); a band is (year0, year1, label, color, sentence, label_y[, word])."""
    c = Card(name)
    X = lambda year: 0.08 + (year - start) / float(end - start) * 0.84   # noqa: E731
    c.line([[0.08, 0.5], [0.92, 0.5]], INK, 0.006, 0)
    for year in ticks:
        c.line([[X(year), 0.485], [X(year), 0.515]], INK, 0.004, 0)
        c.text(str(year), X(year), 0.455, 0.022, 0, color=MUTED)
    rows = {0.64: [], 0.72: [], 0.36: [], 0.28: []}
    prefs = ((0.64, 0.72, 0.36, 0.28), (0.36, 0.28, 0.64, 0.72))

    def spoken(first, word):
        for e in c.elements[first:]:
            if word:
                e["word"] = word

    for k, (year, label, s, *word) in enumerate(events):
        first = len(c.elements)
        text = f"{year}  {label}"
        w = CHAR_W * 0.025 * len(text) + 0.02
        x = min(max(X(year), 0.06 + w / 2), 0.94 - w / 2)
        y = next(r for r in prefs[k % 2] if all(x + w / 2 + 0.01 < a or x - w / 2 - 0.01 > b for a, b in rows[r]))
        rows[y].append((x - w / 2, x + w / 2))
        c.line([[X(year), 0.5], [X(year), y - 0.03 if y > 0.5 else y + 0.03]], FAINT, 0.003, s)
        c.circle([X(year), 0.5], 0.009, INK, s)
        c.text(text, x, y, 0.025, s, plate=True)
        spoken(first, word[0] if word else None)
    for y0, y1, label, color, s, ly, *word in bands:
        first = len(c.elements)
        c.rect([X(y0), 0.53, X(y1), 0.56], color, sentence=s)
        c.text(label, (X(y0) + X(y1)) / 2, ly, 0.024, s, plate=True)
        spoken(first, word[0] if word else None)
    if extra:
        extra(c)
    return c


# ---------------------------------------------------------------- the film
CHAPTERS = [
    ("C1", "Hook", "The highest vaults of the Middle Ages came down; others still stand. Pose the central question."),
    ("C2", "Stone and its outward push", "Stone cannot be pulled apart; a vault pushes outward; the Romanesque answer was mass."),
    ("C3", "The pointed arch", "Less sideways thrust, the hanging chain, not a Gothic invention, level crowns over different widths."),
    ("C4", "The rib vault", "Ribs gather the load onto four piers; how vaults stand is debated; the walls are freed."),
    ("C5", "The flying buttress", "The thrust is carried outside, over the aisle roof, down to a massive buttress."),
    ("C6", "Walls of light", "Why they did it: Saint-Denis, Chartres; was it a revolution or continuity?"),
    ("C7", "Building by geometry", "Rules from trial and error, ropes and squares, templates, centering, carpenters, little room for error."),
    ("C8", "The limit: Beauvais", "Raised beyond its proportions, the vaults fell in 1284; the repair, the tower of 1573; Amiens' iron chain."),
    ("C9", "Why they stand", "Stability rather than strength: the line of thrust, and why proportion scales."),
    ("C10", "Never impossible", "Answer the question; not a simple story of progress; call to action; credits."),
]

BEATS = []


def beat(chapter, bid, kind, intent, sentences, claims=(), **visual):
    BEATS.append({"chapter": chapter, "id": bid, "kind": kind, "intent": intent, "sentences": list(sentences),
                  "claims": list(claims), "visual": visual})


def note(nid, text, sentence=0, until=None, position="TOP_LEFT"):
    a = {"id": nid, "type": "NOTE", "text": text, "sentence": sentence, "position": position}
    if until is not None:
        a["until"] = until
    return a


GOTHIC, ROMANESQUE = "gothic_cathedral_section", "romanesque_church_section"

# C1 -------------------------------------------------------------------------------------------
beat("C1", "B01", "fact", "INTRODUCE_ARCHITECTURE", [
    "In November 1284, in the French city of Beauvais, part of the highest stone vaults of the Middle Ages came down.",
    "They stood nearly 47 meters above the floor.",
    "The choir beneath them, the eastern arm of the cathedral, had been in use for just twelve years."],
    ["CLM_103", "CLM_104", "CLM_106", "CLM_181", "CLM_182"], strategy="HOLD", camera_move={"type": "PUSH_IN", "amount": 0.1},
    visual_goal="A Gothic section through one bay, seen from low down; the collapse is told, never shown",
    required_concepts=[GOTHIC],
    annotations=[note("B01_note", "Illustrative model, not Beauvais Cathedral", 0, position="BOTTOM_RIGHT"),
                 {**note("B01_h", "Published heights differ: about 46 to 48 m", 1), "claim_id": "CLM_104"}])
beat("C1", "B02", "fact", "INTRODUCE_ARCHITECTURE", [
    "And yet many buildings like it are still standing.",
    "At Amiens, begun in 1220, the vault rises more than 42 meters, in a building that is tall, slender and filled with light."],
    ["CLM_110", "CLM_101", "CLM_102", "CLM_156"], strategy="HOLD_HIGHLIGHT", highlight_at_sentence=1,
    visual_goal="The same section: slender piers and tall windows", required_concepts=[GOTHIC, "clerestory_window"],
    annotations=[note("B02_note", "Illustrative model, not Amiens Cathedral", 0, position="BOTTOM_RIGHT")])

c = Card("B03")
c.text("How Gothic Cathedrals Reached", 0.5, 0.7, 0.06, 0)
c.text("Impossible Heights", 0.5, 0.61, 0.06, 0)
c.line([[0.28, 0.56], [0.72, 0.56]], FAINT, 0.003, 0)
c.text("How did they raise stone that high?", 0.5, 0.47, 0.036, 1, color=MUTED)
c.text("And why, sometimes, did it come down?", 0.5, 0.39, 0.036, 2, color=MUTED)
beat("C1", "B03", "fact", "SHOW_CONTEXT", [
    "The people who built them had no knowledge of material properties or allowable stresses.",
    "So how did they raise stone that high?",
    "And why, sometimes, did it come down?"],
    ["CLM_110"], strategy="CARD", graphic=c.spec(), visual_goal="Title card: the central question", required_concepts=[])

# C2 -------------------------------------------------------------------------------------------
c = Card("B04")
c.tag("2 · Stone and its outward push")
voussoirs(c, 0.5, 0.3, 0.42, 0.3, 0.07, 7, 0)
c.rect([0.33, 0.24, 0.5 - 0.2 / ASPECT, 0.3], STONE, sentence=0)
c.rect([0.5 + 0.2 / ASPECT, 0.24, 0.67, 0.3], STONE, sentence=0)
c.text("Pulled apart: little or no strength", 0.5, 0.82, 0.03, 1, plate=True)
c.text("Stones pressed together: it stands", 0.5, 0.75, 0.03, 2, plate=True, color=ACCENT)
c.text("Conceptual diagram, not to scale", 0.82, 0.25, 0.02, 0, color=MUTED)
beat("C2", "B04", "fact", "EXPLAIN_STRUCTURE", [
    "Start with the stone itself.",
    "Stone has little or no strength when it is pulled apart.",
    "So a stone building has to stand by keeping its stones pressed together."],
    ["CLM_111"], strategy="CARD", graphic=c.spec(), visual_goal="An arch of wedge-shaped stones: pressed together, not pulled apart",
    required_concepts=[])
beat("C2", "B05", "fact", "EXPLAIN_CAUSE_EFFECT", [
    "Now put a heavy stone vault on top of two walls.",
    "A vault does not simply press down: it also pushes outward, like a bow being bent.",
    "That outward push is called thrust, and medieval builders were well aware of it."],
    ["CLM_120", "CLM_121"], strategy="HOLD", visual_goal="Romanesque section: a barrel vault on two walls; conceptual outward arrows at the top of the walls (no magnitudes)",
    required_concepts=[ROMANESQUE, "barrel_vault"],
    annotations=[note("B05_note", "Illustrative model, arrows are conceptual", 1, position="BOTTOM_RIGHT")])
beat("C2", "B06", "fact", "EXPLAIN_STRUCTURE", [
    "Before Gothic, Romanesque builders answered it with mass.",
    "Their heavy vaults pushed outward along the whole length of the wall, so walls and supports had to be thick, stiffened by buttresses.",
    "Windows stayed small, and the interiors were dark."],
    ["CLM_122"], strategy="HOLD_HIGHLIGHT", highlight_at_sentence=1, visual_goal="Thick walls and shallow buttresses highlighted; small windows",
    required_concepts=[ROMANESQUE, "thick_wall", "shallow_buttress"])

c = Card("B07")
c.tag("Three tools")
c.text("Stop fighting thrust. Channel it.", 0.5, 0.82, 0.046, 1)
for x, w, word in ((0.22, "Pointed arch", "pointed"), (0.5, "Rib vault", "rib"), (0.78, "Flying buttress", "flying")):
    c.text(w, x, 0.34, 0.036, 2, plate=True, word=word)
c.line(place(pointed_arch(0.28, 0.26), 0.22, 0.42), STONE, 0.012, 2)
c.elements[-1]["word"] = "pointed"
for pts in ([[0.42, 0.42], [0.58, 0.7]], [[0.58, 0.42], [0.42, 0.7]]):
    c.line(pts, STONE, 0.012, 2)
    c.elements[-1]["word"] = "rib"
c.rect([0.42, 0.42, 0.58, 0.7], border=FAINT, sentence=2, border_width=0.003)
c.elements[-1]["word"] = "rib"
c.line(place(pointed_arch(0.3, 0.2)[:17], 0.8, 0.42), STONE, 0.012, 2)
c.elements[-1]["word"] = "flying"
c.rect([0.71, 0.42, 0.74, 0.7], STONE, sentence=2)
c.elements[-1]["word"] = "flying"
beat("C2", "B07", "fact", "SHOW_CONTEXT", [
    "Gothic builders took a different approach.",
    "They stopped fighting thrust with sheer thickness, and learned to channel it.",
    "Three tools made that possible: the pointed arch, the rib vault, and the flying buttress."],
    ["CLM_123"], strategy="CARD", graphic=c.spec(), visual_goal="The three tools named as they are spoken", required_concepts=[])

# C3 -------------------------------------------------------------------------------------------
c = Card("B08")
c.tag("3 · The pointed arch")
c.line(place(round_arch(0.36), 0.3, 0.32), STONE, 0.014, 0)
c.line(place(pointed_arch(0.36, 0.42), 0.7, 0.32), ACCENT, 0.014, 0)
c.text("Round arch", 0.3, 0.8, 0.034, 1, plate=True)
c.text("Pointed arch", 0.7, 0.8, 0.034, 0, plate=True)
c.arrow([0.3 - 0.18 / ASPECT, 0.32], [0.3 - 0.18 / ASPECT - 0.07, 0.29], THRUST, 0.008, 1)
c.arrow([0.3 + 0.18 / ASPECT, 0.32], [0.3 + 0.18 / ASPECT + 0.07, 0.29], THRUST, 0.008, 1)
c.arrow([0.7 - 0.18 / ASPECT, 0.32], [0.7 - 0.18 / ASPECT - 0.025, 0.25], THRUST, 0.008, 1)
c.arrow([0.7 + 0.18 / ASPECT, 0.32], [0.7 + 0.18 / ASPECT + 0.025, 0.25], THRUST, 0.008, 1)
c.text("Conceptual arrows: direction only, not calculated", 0.5, 0.22, 0.021, 1, color=MUTED)
beat("C3", "B08", "fact", "COMPARE_VARIANTS", [
    "A pointed arch is two arcs of a circle that meet at a point.",
    "Compared with a round arch, it pushes less to the sides, and that lets it rise much higher."],
    ["CLM_130"], strategy="CARD", graphic=c.spec(), visual_goal="Round and pointed arch on the same span; the push turns downward",
    required_concepts=[])

c = Card("B09")
c.line([[0.1, 0.72], [0.44, 0.72]], FAINT, 0.004, 0)
c.line(place(catenary(0.46, 0.34), 0.27, 0.72, flip=True), INK, 0.008, 2)
c.circle([0.27 - 0.23 / ASPECT, 0.72], 0.011, INK, 2)
c.circle([0.27 + 0.23 / ASPECT, 0.72], 0.011, INK, 2)
c.text("A hanging chain", 0.27, 0.3, 0.03, 2, plate=True)
c.line(place(catenary(0.46, 0.34), 0.73, 0.38), INK, 0.008, 2, dash=True)
c.text("Turned upside down", 0.73, 0.3, 0.03, 2, plate=True)
c.line(place(pointed_arch(0.46, 0.34), 0.73, 0.38), ACCENT, 0.008, 3)
c.text("Pointed arch", 0.73, 0.79, 0.03, 3, plate=True, color=ACCENT)
c.text("“As hangs the flexible line, so but inverted", 0.5, 0.88, 0.032, 1)
c.text("will stand the rigid arch.”  Robert Hooke, 1675", 0.5, 0.83, 0.032, 1, until=2)
c.text("Conceptual diagram", 0.5, 0.235, 0.021, 2, color=MUTED)
beat("C3", "B09", "fact", "EXPLAIN_STRUCTURE", [
    "In 1675, the scientist Robert Hooke summed up the shape of a good arch in one line.",
    "As hangs the flexible line, so but inverted will stand the rigid arch.",
    "In other words, the force in an arch follows a curve like a hanging chain, turned upside down.",
    "A Columbia University project says the pointed arch comes closer to that curve than the round arch, and so is more efficient."],
    ["CLM_114", "CLM_133"], strategy="CARD", graphic=c.spec(), visual_goal="Hanging chain, inverted, beside a pointed arch", required_concepts=[])

EARLY = dict(start=1060, end=1160, ticks=(1060, 1080, 1100, 1120, 1140, 1160))
c = timeline("B10", [(1088, "Cluny, Burgundy: pointed arches", 1, "cluny")],
             [(1130, 1144, "Saint-Denis: used systematically", "#5E86A6", 2, 0.64)], **EARLY)
beat("C3", "B10", "fact", "SHOW_CONTEXT", [
    "The pointed arch was not a Gothic invention.",
    "It already appears in Burgundy, at the rebuilding of the abbey of Cluny around 1088, and the same Columbia project traces it to Islamic sources.",
    "At the abbey of Saint-Denis, it was used systematically, together with the other new ideas."],
    ["CLM_131"], strategy="CARD", graphic=c.spec(), visual_goal="Short timeline: pointed arches before Gothic", required_concepts=[])

c = Card("B11")
c.text("Round arches", 0.27, 0.84, 0.034, 0, plate=True)
c.text("Pointed arches", 0.73, 0.84, 0.034, 1, plate=True)
c.line(place(round_arch(0.22), 0.16, 0.3), STONE, 0.012, 0)
c.line(place(round_arch(0.42), 0.34, 0.3), STONE, 0.012, 0)
c.line([[0.06, 0.3 + 0.21], [0.48, 0.3 + 0.21]], FAINT, 0.003, 0, dash=True)
c.text("Crowns at different heights", 0.27, 0.7, 0.026, 0, color=MUTED)
c.line(place(pointed_arch(0.22, 0.34), 0.62, 0.3), ACCENT, 0.012, 1)
c.line(place(pointed_arch(0.42, 0.34), 0.8, 0.3), ACCENT, 0.012, 1)
c.line([[0.54, 0.64], [0.94, 0.64]], ACCENT, 0.003, 1, dash=True)
c.text("Same crown height", 0.73, 0.7, 0.026, 1, color=ACCENT)
c.text("Wide bay, narrow bay: conceptual diagram", 0.5, 0.235, 0.021, 1, color=MUTED)
beat("C3", "B11", "fact", "COMPARE_VARIANTS", [
    "It had a subtler advantage too.",
    "Unlike a round arch, a pointed arch can span sections of different widths, called bays, and still reach the same height at its crown.",
    "That was a valuable asset for keeping complex vaults regular."],
    ["CLM_132"], strategy="CARD", graphic=c.spec(), visual_goal="Level crowns over different widths", required_concepts=[])

# C4 -------------------------------------------------------------------------------------------
c = Card("B12")
c.tag("4 · The rib vault")
bx0, by0, bx1, by1 = 0.32, 0.28, 0.68, 0.8
c.rect([bx0, by0, bx1, by1], border=FAINT, sentence=0, border_width=0.004)
c.line([[bx0, by0], [bx1, by1]], ACCENT, 0.009, 1)
c.line([[bx0, by1], [bx1, by0]], ACCENT, 0.009, 1)
for x, y in ((bx0, by0), (bx1, by0), (bx0, by1), (bx1, by1)):
    c.circle([x, y], 0.02, INK, 2)
c.text("Diagonal ribs", 0.82, 0.62, 0.03, 1, plate=True, color=ACCENT)
c.text("Four piers", 0.18, 0.62, 0.03, 2, plate=True)
c.text("One bay, seen from above", 0.5, 0.235, 0.022, 0, color=MUTED)
beat("C4", "B12", "fact", "EXPLAIN_STRUCTURE", [
    "The second tool is the rib vault.",
    "Two pointed arches cross diagonally over each bay of the building.",
    "They gather the vault's load onto four points: the piers, or stone pillars, at its corners."],
    ["CLM_140"], strategy="CARD", graphic=c.spec(), visual_goal="Plan of one bay: ribs to four piers", required_concepts=[])
beat("C4", "B13", "fact", "SHOW_COMPONENT", [
    "How exactly these vaults stand has been debated for centuries.",
    "Engineers following Jacques Heyman assume that the main ribs bring the forces down, and treat the stone between them as a series of parallel arches."],
    ["CLM_141"], strategy="HOLD_HIGHLIGHT", highlight_at_sentence=1, visual_goal="Ribs highlighted, then the web between them",
    required_concepts=[GOTHIC, "rib", "vault_web"],
    annotations=[note("B13_note", "Illustrative model", 0, position="BOTTOM_RIGHT")])
c = timeline("B14", [(1088, "Cluny: pointed arches", 0), (1093, "Durham, England: ribbed vaults", 1, "durham")],
             [(1140, 1144, "Saint-Denis choir", "#5E86A6", 0, 0.64)], **EARLY)
beat("C4", "B14", "fact", "SHOW_CONTEXT", [
    "Ribs were not new either.",
    "They appear at Durham Cathedral, in England, as early as 1093, and Columbia's project traces them to Islamic, Roman and Byzantine sources."],
    ["CLM_142"], strategy="CARD", graphic=c.spec(), visual_goal="The same timeline, with ribbed vaults added", required_concepts=[])
beat("C4", "B15", "fact", "EXPLAIN_DESIGN_CHANGE", [
    "That changes the job of the wall.",
    "With the load gathered onto piers, the walls between them no longer had to hold up the vault.",
    "They could be thinned, and opened up with wide windows."],
    ["CLM_143"], strategy="HOLD_HIGHLIGHT", highlight_at_sentence=2, visual_goal="The wall between two piers opens into a tall window",
    required_concepts=[GOTHIC, "nave_pier", "clerestory_window"])

# C5 -------------------------------------------------------------------------------------------
beat("C5", "B16", "fact", "EXPLAIN_CAUSE_EFFECT", [
    "But gathering the thrust does not make it go away.",
    "Even reduced, that sideways push remains a threat to the stability of the whole building.",
    "It still has to be contained somewhere."],
    ["CLM_150"], strategy="HOLD", visual_goal="Conceptual outward arrow at the top of a pier, with nothing yet to receive it",
    required_concepts=[GOTHIC, "nave_pier"],
    annotations=[note("B16_ch", "5 · The flying buttress", 0, 2),
                 note("B16_note", "Arrows show the idea, not calculated forces", 1, position="BOTTOM_RIGHT")])
beat("C5", "B17", "fact", "EXPLAIN_LOAD_PATH", [
    "The answer stands outside the building: the flying buttress.",
    "It is a stone arch that picks up the thrust where it leaves the vault, carries it across the aisle roof, and brings it down to a massive pier buttress.",
    "Often a pinnacle on top adds weight, to help stabilize the thrust."],
    ["CLM_151", "CLM_152"], strategy="ASSEMBLE_IN", visual_goal="Flyer, pier buttress and pinnacle assemble; a conceptual path follows them to the ground",
    required_concepts=[GOTHIC, "flying_buttress", "pier_buttress", "pinnacle", "aisle_roof"],
    annotations=[note("B17_note", "Illustrative model, conceptual path", 1, position="BOTTOM_RIGHT")])
beat("C5", "B18", "fact", "EXPLAIN_DESIGN_CHANGE", [
    "One way to picture it comes from Columbia's Amiens project.",
    "It is as if the thick outer wall had been cut into segments, and each segment turned 90 degrees.",
    "Those segments become rigid supports, standing out from the building, with exposed arches reaching up to the high vaults."],
    ["CLM_153"], strategy="HIGHLIGHT_REPLACE_HIGHLIGHT", visual_goal="Romanesque thick wall -> segments rotated -> Gothic pier buttresses, same camera",
    required_concepts=[ROMANESQUE, GOTHIC, "thick_wall", "pier_buttress"])
beat("C5", "B19", "fact", "SHOW_CONTEXT", [
    "According to France's national library, the first flying buttresses were used to consolidate Romanesque churches that threatened to collapse.",
    "It also says that the slanting timber props used while building the vaults were, in effect, made permanent in stone.",
    "At Chartres, flying buttresses were part of the original plans.",
    "And around the east end of Notre-Dame in Paris, they look almost like a giant external skeleton."],
    ["CLM_154", "CLM_155"], strategy="HOLD", camera_move={"type": "PUSH_IN", "amount": 0.1},
    visual_goal="Flyers on the model; rights-cleared photographs of Chartres and Notre-Dame replace it where available",
    required_concepts=[GOTHIC, "flying_buttress"],
    annotations=[note("B19_note", "Illustrative model, not Chartres or Notre-Dame", 0, position="BOTTOM_RIGHT")])
beat("C5", "B20", "fact", "INTRODUCE_ARCHITECTURE", [
    "Flying buttresses even help carry rainwater off the roof.",
    "But above all, builders learned how to exploit them, and cathedrals grew ever taller."],
    ["CLM_156", "CLM_157"], strategy="HOLD_HIGHLIGHT", highlight_at_sentence=1, visual_goal="The full exterior of the section, flyers highlighted",
    required_concepts=[GOTHIC, "flying_buttress"])

# C6 -------------------------------------------------------------------------------------------
c = timeline("B21", [(1144, "Choir dedicated", 2, "choir")],
             [(1130, 1140, "West front", STONE, 2, 0.36), (1140, 1144, "New choir", "#5E86A6", 2, 0.28)],
             start=1120, end=1160, ticks=(1120, 1130, 1140, 1150, 1160), extra=lambda c: (
                 c.tag("6 · Walls of light"),
                 c.text("Saint-Denis", 0.5, 0.86, 0.05, 2),
                 c.text("Pointed arches throughout", 0.24, 0.76, 0.027, 3, plate=True, word="pointed"),
                 c.text("Every vault ribbed", 0.5, 0.76, 0.027, 3, plate=True, word="ribbed"),
                 c.text("Monumental stained glass", 0.76, 0.76, 0.027, 3, plate=True, word="glass")))
beat("C6", "B21", "fact", "SHOW_CONTEXT", [
    "Why go to all this trouble?",
    "Part of the answer is light.",
    "At the abbey church of Saint-Denis, Abbot Suger built a new choir between 1140 and 1144.",
    "Pointed arches run throughout, every vault is ribbed, and monumental stained glass seems to dissolve the whole structure."],
    ["CLM_160", "CLM_161"], strategy="CARD", graphic=c.spec(), visual_goal="Saint-Denis, dates and three features (a rights-cleared photograph may replace the card)",
    required_concepts=[])

c = Card("B22")
c.text("“A sign or bridge to the divine”", 0.5, 0.62, 0.05, 0)
c.text("Light, for Abbot Suger", 0.5, 0.53, 0.03, 0, color=MUTED)
c.text("The new style had to let in as much light as possible", 0.5, 0.4, 0.032, 1, plate=True)
beat("C6", "B22", "fact", "SHOW_CONTEXT", [
    "For Suger, light was a sign, a bridge to the divine.",
    "France's national library says the new style had to let in as much light as possible."],
    ["CLM_161"], strategy="CARD", graphic=c.spec(), visual_goal="Why light mattered", required_concepts=[])

c = Card("B23")
c.text("2,500 m²", 0.5, 0.62, 0.11, 0, color=GLASS)
c.text("of stained glass at Chartres, most of it original", 0.5, 0.47, 0.034, 0)
beat("C6", "B23", "fact", "SHOW_CONTEXT", [
    "At Chartres, some 2,500 square meters of stained glass survive, most of it original."],
    ["CLM_162"], strategy="CARD", graphic=c.spec(), visual_goal="One number (a rights-cleared photograph of the glass may replace the card)",
    required_concepts=[])

c = Card("B24")
c.text("How new was Gothic?", 0.5, 0.84, 0.046, 0)
c.line([[0.5, 0.3], [0.5, 0.76]], FAINT, 0.003, 2)
c.text("“An entire revolution", 0.27, 0.66, 0.036, 2)
c.text("in the art of building”", 0.27, 0.6, 0.036, 2)
c.text("After Viollet-le-Duc, 19th century", 0.27, 0.52, 0.025, 2, color=MUTED)
c.text("No Gothic break: a creative", 0.73, 0.66, 0.036, 3)
c.text("proposal rooted in continuity", 0.73, 0.6, 0.036, 3)
c.text("Arnaud Timbert, art historian", 0.73, 0.52, 0.025, 3, color=MUTED)
c.text("Suger's crypt: round arches, groin vaults", 0.73, 0.38, 0.026, 4, plate=True)
beat("C6", "B24", "fact", "COMPARE_VARIANTS", [
    "How new was all of this?",
    "On that question, historians still disagree.",
    "Following the 19th-century architect Viollet-le-Duc, some call Gothic an entire revolution in the art of building.",
    "The art historian Arnaud Timbert argues there was no revolution and no Gothic break, but a creative proposal rooted in continuity.",
    "Suger's own crypt still relies almost entirely on round arches and groin vaults."],
    ["CLM_163"], strategy="CARD", graphic=c.spec(), visual_goal="Two readings, side by side", required_concepts=[])

# C7 -------------------------------------------------------------------------------------------
c = Card("B25")
c.tag("7 · Building by geometry")
c.line(place(pointed_arch(0.16, 0.16), 0.24, 0.32), STONE, 0.01, 2)
c.line(place(pointed_arch(0.26, 0.26), 0.44, 0.32), STONE, 0.012, 2)
c.line(place(pointed_arch(0.42, 0.42), 0.7, 0.32), STONE, 0.016, 2)
c.text("Trial and error, over centuries", 0.5, 0.86, 0.036, 1, plate=True)
c.text("The same proportions, scaled up", 0.5, 0.25, 0.03, 2, plate=True)
beat("C7", "B25", "fact", "EXPLAIN_STRUCTURE", [
    "So how did they do all this, with no knowledge of material properties?",
    "Master builders used geometrical rules, developed through centuries of trial and error.",
    "They scaled up the same proportions for new, larger elements."],
    ["CLM_110"], strategy="CARD", graphic=c.spec(), visual_goal="One proportion at three sizes", required_concepts=[])

c = Card("B26")
c.line([[0.2, 0.3], [0.2, 0.8], [0.5, 0.8], [0.5, 0.3], [0.2, 0.3]], WOOD, 0.004, 0)
for x, y in ((0.2, 0.3), (0.2, 0.8), (0.5, 0.3), (0.5, 0.8)):
    c.circle([x, y], 0.012, WOOD, 0)
c.text("Ropes pegged to the ground", 0.35, 0.86, 0.028, 0, plate=True)
c.line([[0.2, 0.55], [0.35, 0.8], [0.5, 0.55], [0.35, 0.3], [0.2, 0.55]], ACCENT, 0.004, 1)
c.text("Squares with right angles", 0.74, 0.68, 0.028, 1, plate=True, word="squares")
c.text("Templates: straight-edge and compass", 0.74, 0.58, 0.026, 1, plate=True, word="templates")
c.text("Schematic, not the Amiens plan", 0.74, 0.3, 0.021, 0, color=MUTED)
beat("C7", "B26", "fact", "EXPLAIN_STRUCTURE", [
    "At Amiens, setting out the site began with ropes pegged to the ground.",
    "Squares with perfect right angles controlled the plan, and templates for piers, windows and vaults were designed with straight-edge and compass."],
    ["CLM_170"], strategy="CARD", graphic=c.spec(), visual_goal="Ropes, pegs and a square turned inside a square", required_concepts=[])

c = Card("B27")
voussoirs(c, 0.5, 0.3, 0.4, 0.38, 0.06, 7, 0)
c.rect([0.33, 0.24, 0.5 - 0.195 / ASPECT, 0.3], STONE, sentence=0)
c.rect([0.5 + 0.195 / ASPECT, 0.24, 0.67, 0.3], STONE, sentence=0)
c.line(place(pointed_arch(0.39, 0.37), 0.5, 0.3), WOOD, 0.01, 1, until=2)
for k in range(-3, 4):
    u = k * 0.045
    r = (0.39 * 0.39 / 4 + 0.37 * 0.37) / 0.39
    top = 0.3 + math.sqrt(r * r - (abs(u) + r - 0.195) ** 2)
    c.line([[0.5 + u / ASPECT, 0.24], [0.5 + u / ASPECT, top]], WOOD, 0.006, 1, until=2, layer=-1)
c.text("Wedge-shaped voussoirs", 0.19, 0.74, 0.028, 0, plate=True)
c.text("Each cut to a wooden template", 0.19, 0.66, 0.026, 1, plate=True)
c.text("Centering (temporary)", 0.81, 0.74, 0.028, 1, until=2, plate=True)
c.text("Centering removed", 0.81, 0.74, 0.028, 2, plate=True)
c.text("once the mortar has set", 0.81, 0.67, 0.026, 2, plate=True)
beat("C7", "B27", "fact", "EXPLAIN_STRUCTURE", [
    "Arches were usually drawn full size on the ground, then divided into wedge-shaped stones called voussoirs.",
    "Each voussoir was cut to a wooden template, and the stones were laid on a rigid wooden frame called centering.",
    "The frame came away only once the mortar had set: at Amiens, after a couple of months or so."],
    ["CLM_172"], strategy="CARD", graphic=c.spec(), visual_goal="An arch on centering; the centering goes away", required_concepts=[])

c = Card("B28")
c.text("The carpenters", 0.5, 0.82, 0.05, 0)
for x, y, w, word, s in ((0.3, 0.64, "Scaffolding", "scaffolding", 0), (0.7, 0.64, "Formwork for the vaults", "formwork", 0),
                         (0.3, 0.5, "Lifting gear", "lifting", 0), (0.7, 0.5, "Ties: wood, later iron", "tied", 1)):
    c.text(w, x, y, 0.034, s, plate=True, word=word)
c.text("Ties stopped the arches pushing the upper piers over", 0.5, 0.34, 0.028, 1, color=MUTED, word="pushing")
beat("C7", "B28", "fact", "EXPLAIN_STRUCTURE", [
    "Carpenters built the scaffolding, the formwork for the vaults and the lifting gear.",
    "They also tied the upper piers with wood, and later iron, to stop the arches pushing them over."],
    ["CLM_173"], strategy="CARD", graphic=c.spec(), visual_goal="What the carpenters made (words, no workers or machinery)", required_concepts=[])
beat("C7", "B29", "fact", "SHOW_COMPONENT", [
    "And there was little room for error.",
    "The whole stone skeleton relies on lining up the thrust of each arch with the buttress that supports it."],
    ["CLM_171"], strategy="HOLD_HIGHLIGHT", highlight_at_sentence=1, camera_move={"type": "PUSH_IN", "amount": 0.12},
    visual_goal="Close on the point where the flyer meets the pier", required_concepts=[GOTHIC, "flying_buttress", "pier_buttress"])
c = timeline("B30", [(1220, "Foundation stone", 1, "foundation"), (1310, "Main roof finished (about)", 1, "roof")],
             [(1220, 1310, "Amiens Cathedral", STONE, 1, 0.72)], start=1200, end=1320, ticks=(1200, 1240, 1280, 1320))
beat("C7", "B30", "fact", "SHOW_CONTEXT", [
    "All of this took generations of work.",
    "The foundation stone of Amiens was laid in 1220, and its main roof was not finished until about 1310."],
    ["CLM_101"], strategy="CARD", graphic=c.spec(), visual_goal="Ninety years on one line", required_concepts=[])

# C8 -------------------------------------------------------------------------------------------
c = Card("B31")
c.tag("8 · The limit: Beauvais")
c.text("Beauvais, 1225", 0.5, 0.66, 0.06, 0)
c.text("A fire damages the old Romanesque choir", 0.5, 0.54, 0.034, 1, word="fire")
c.text("The bishop rebuilds, after the greatest buildings of his time", 0.5, 0.46, 0.034, 1, word="bishop")
beat("C8", "B31", "fact", "SHOW_CONTEXT", [
    "Which brings us back to Beauvais.",
    "In 1225, a fire damaged the old Romanesque choir, and the bishop decided to rebuild it, inspired by the greatest buildings of his time."],
    ["CLM_180"], strategy="CARD", graphic=c.spec(), visual_goal="Place and date", required_concepts=[])

c = Card("B32")
x0, x1 = 0.36, 0.64
for y0, y1, label, s in ((0.24, 0.46, "Arcade", 0), (0.46, 0.56, "Triforium", 0), (0.56, 0.72, "Upper windows", 1)):
    c.rect([x0, y0, x1, y1], STONE if s == 0 else GLASS, border="#7A6E58", sentence=s, border_width=0.003)
    c.text(label, 0.5, (y0 + y1) / 2, 0.028, s, plate=True)
c.rect([x0, 0.72, x1, 0.84], border=THRUST, sentence=1, border_width=0.005, dash=True)
c.text("+ about 5 m", 0.5, 0.78, 0.032, 1, color=THRUST, word="adding")
c.text("Beyond the planned proportions", 0.82, 0.78, 0.026, 1, plate=True, word="beyond")
c.text("1250s: lower levels finished", 0.18, 0.5, 0.026, 0, plate=True)
c.text("1272: choir in use", 0.18, 0.78, 0.026, 2, plate=True)
c.text("Schematic, not to scale", 0.82, 0.26, 0.021, 0, color=MUTED)
beat("C8", "B32", "fact", "EXPLAIN_DESIGN_CHANGE", [
    "By the 1250s, the two lower levels of the new choir were finished.",
    "Then the bishop apparently decided to go beyond the planned proportions, adding about five meters to the upper windows, and so to the vaults.",
    "By 1272, the clergy could use the new choir."],
    ["CLM_181"], strategy="CARD", graphic=c.spec(), visual_goal="Three levels; the top one grows", required_concepts=[])

c = Card("B33")
for x, h, name, label, s in ((0.36, 42.5, "Amiens", "more than 42 m", 0), (0.64, 47.0, "Beauvais", "nearly 47 m", 0)):
    top = 0.24 + h * 0.012
    c.rect([x - 0.07, 0.24, x + 0.07, top], STONE if name == "Amiens" else ACCENT, sentence=s)
    c.text(name, x, 0.3, 0.034, s, plate=True)
    c.text(label, x, top + 0.04, 0.03, s)
c.text("The highest vaults of the Middle Ages", 0.5, 0.88, 0.034, 1)
c.text("Published heights differ:", 0.86, 0.5, 0.021, 0, color=MUTED)
c.text("about 46 to 48 m at Beauvais", 0.86, 0.46, 0.021, 0, color=MUTED)
beat("C8", "B33", "fact", "COMPARE_VARIANTS", [
    "Its vault rose nearly 47 meters, a few meters above Amiens.",
    "These were the highest vaults built in the Middle Ages."],
    ["CLM_102", "CLM_103", "CLM_104"], strategy="CARD", graphic=c.spec(), visual_goal="Two heights side by side, with the caveat on screen",
    required_concepts=[])
beat("C8", "B34", "fact", "SHOW_CONTEXT", [
    "Then, in November 1284, part of the vaults over the choir came down.",
    "The architect Viollet-le-Duc, writing centuries later, called it the last limit that the great churches of the 13th century could reach."],
    ["CLM_182"], strategy="HOLD", camera_move={"type": "PUSH_IN", "amount": 0.1}, visual_goal="The section at rest, the vault highlighted; no collapse or debris is shown",
    required_concepts=[GOTHIC, "vault_web"],
    annotations=[note("B34_note", "Illustrative model, not Beauvais Cathedral", 0, position="BOTTOM_RIGHT")])

c = Card("B35")
c.text("Why did the vaults fall? Still debated.", 0.5, 0.86, 0.04, 0)
for y, t, s, word in ((0.72, "Settling masonry broke the flying buttresses", 1, None),
                      (0.63, "Gusts of wind set the buttress system resonating", 2, "gusts"),
                      (0.54, "Slow settlement of the foundations", 2, "settlement")):
    c.text(t, 0.5, y, 0.03, s, plate=True, word=word)
c.line([[0.2, 0.47], [0.8, 0.47]], FAINT, 0.003, 3)
c.text("2024 study: nothing justifies a foundation cause", 0.5, 0.4, 0.03, 3, color=ACCENT)
c.text("Vaults raised against proven proportions: upper parts too flexible", 0.5, 0.32, 0.028, 4, color=ACCENT)
c.text("Vernhes, Renault and Zotna, ECSMGE 2024", 0.5, 0.245, 0.021, 3, color=MUTED)
beat("C8", "B35", "fact", "EXPLAIN_CAUSE_EFFECT", [
    "Why it happened is still debated.",
    "Some blame settling masonry that broke the flying buttresses.",
    "Others point to gusts of wind setting the buttress system resonating, or to slow settlement of the foundations.",
    "A 2024 study found nothing to justify a foundation cause.",
    "Its authors argue that raising the vaults, against proven proportions, left the upper parts too flexible."],
    ["CLM_183", "CLM_184"], strategy="CARD", graphic=c.spec(), visual_goal="The explanations, one by one", required_concepts=[])

c = Card("B36")
xs = [0.2 + 0.2 * k for k in range(4)]
c.rect([0.2, 0.46, 0.8, 0.72], border=FAINT, sentence=0, border_width=0.004)
for x in xs:
    for y in (0.46, 0.72):
        c.circle([x, y], 0.016, INK, 0)
for x in (0.3, 0.5, 0.7):
    for y in (0.46, 0.72):
        c.circle([x, y], 0.016, ACCENT, 1)
c.text("Three bays", 0.2, 0.82, 0.03, 0, plate=True)
c.text("New piers: six bays", 0.76, 0.82, 0.03, 1, plate=True, color=ACCENT)
c.text("Repairs finished in 1340", 0.5, 0.36, 0.032, 2, plate=True, word="finished")
c.text("Longer to repair than to build (Stephen Murray)", 0.5, 0.28, 0.026, 2, color=MUTED, word="longer")
beat("C8", "B36", "fact", "EXPLAIN_DESIGN_CHANGE", [
    "The repair tells its own story.",
    "New piers went up between the old ones, turning three bays into six.",
    "The work was not finished until 1340: as the historian Stephen Murray put it, it took longer to repair the choir than to build it."],
    ["CLM_185", "CLM_182"], strategy="CARD", graphic=c.spec(), visual_goal="Plan of the choir's straight bays: three become six", required_concepts=[])

c = timeline("B37", [(1500, "Transept begun", 0, "transept"), (1569, "Lantern tower finished", 1, "finished"),
                     (1573, "Tower falls", 3, "tower")],
             [], start=1480, end=1600, ticks=(1480, 1520, 1560, 1600), extra=lambda c: (
                 c.text("Four slender piers, no support to the west", 0.5, 0.82, 0.03, 2, plate=True, word="slender"),
                 c.text("The great Gothic nave: never built", 0.5, 0.24, 0.03, 4, plate=True)))
beat("C8", "B37", "fact", "SHOW_CONTEXT", [
    "In the sixteenth century, work began again, with a new transept, the cross-arm of the building.",
    "Then, instead of a nave, the builders raised a lantern tower and spire about 150 meters high, finished in 1569.",
    "It rested on four slender piers, and the sources point to a lack of support on the west side, where the nave had not been built.",
    "In 1573, just four years after it was finished, the tower came down.",
    "The great Gothic nave was never built."],
    ["CLM_186", "CLM_187", "CLM_106"], strategy="CARD", graphic=c.spec(), visual_goal="Timeline; the fall is told, not shown", required_concepts=[])

c = Card("B38")
c.text("Amiens", 0.5, 0.86, 0.05, 0)
for x in (0.3, 0.7):
    c.rect([x - 0.03, 0.24, x + 0.03, 0.78], STONE, sentence=0)
c.line([[0.3, 0.6], [0.7, 0.6]], INK, 0.008, 2, dash=True)
c.text("Iron chain, 1497–1500", 0.5, 0.66, 0.032, 2, plate=True, word="chain")
c.text("Within two centuries, the crossing piers were threatening collapse", 0.5, 0.48, 0.027, 1, plate=True)
c.text("Schematic, not to scale", 0.5, 0.26, 0.021, 0, color=MUTED)
beat("C8", "B38", "fact", "SHOW_CONTEXT", [
    "Beauvais was not alone.",
    "At Amiens, within two centuries, the piers at the crossing, where the arms of the building meet, were threatening collapse.",
    "Between 1497 and 1500, an iron chain was installed to stop the movement, and it still runs through the building today."],
    ["CLM_190", "CLM_191", "CLM_106"], strategy="CARD", graphic=c.spec(), visual_goal="Two piers tied by a chain", required_concepts=[])

# C9 -------------------------------------------------------------------------------------------
beat("C9", "B39", "fact", "EXPLAIN_STRUCTURE", [
    "So why do these buildings stand at all?",
    "The answer from modern engineers is that strength is rarely the problem.",
    "Stresses in masonry are typically only a fraction of what the stone can bear, and in most cases structures fail through instability, not a lack of strength."],
    ["CLM_112"], strategy="HOLD", camera_move={"type": "PUSH_IN", "amount": 0.1}, visual_goal="The full section at rest",
    required_concepts=[GOTHIC],
    annotations=[note("B39_ch", "9 · Why they stand", 0, 2)])

c = Card("B40")
voussoirs(c, 0.3, 0.3, 0.34, 0.36, 0.07, 7, 0)
c.line(place(pointed_arch(0.41, 0.42), 0.3, 0.3), ACCENT, 0.006, 0, dash=True)
c.text("Line of thrust inside the stone", 0.3, 0.84, 0.028, 1, plate=True, color=ACCENT)
voussoirs(c, 0.7, 0.3, 0.34, 0.36, 0.07, 7, 2)
c.line(place(catenary(0.41, 0.3), 0.7, 0.3), THRUST, 0.006, 2, dash=True)
c.text("No line fits: it collapses", 0.7, 0.84, 0.028, 2, plate=True, color=THRUST)
c.text("Conceptual lines, not calculated", 0.5, 0.235, 0.021, 0, color=MUTED)
beat("C9", "B40", "fact", "EXPLAIN_STRUCTURE", [
    "Picture the path of the force through the stone, which engineers call the line of thrust.",
    "As long as that line can stay inside the masonry, the structure can stand in compression.",
    "If no such line can be found, it collapses."],
    ["CLM_113", "CLM_111"], strategy="CARD", graphic=c.spec(), visual_goal="The line of thrust inside an arch; a line that no longer fits",
    required_concepts=[])

c = Card("B41")
c.line(place(pointed_arch(0.12, 0.14), 0.22, 0.3), ACCENT, 0.008, 1)
c.line(place(pointed_arch(0.5, 0.58), 0.62, 0.26), ACCENT, 0.016, 1)
c.text("Small model", 0.22, 0.24, 0.028, 1, plate=True)
c.text("Real building", 0.62, 0.22, 0.028, 1, plate=True)
c.text("Same proportions", 0.32, 0.72, 0.034, 1, plate=True, word="proportions")
c.text("Rules of geometry, learned by trial and error", 0.5, 0.88, 0.03, 2, plate=True, word="geometry")
beat("C9", "B41", "fact", "EXPLAIN_STRUCTURE", [
    "What matters most, then, is shape and proportion.",
    "Stability, unlike some other engineering problems, can be scaled: a model with the same proportions is a good guide to the stability of the real building.",
    "That helps explain how rules of geometry, learned by trial and error, could carry builders so far."],
    ["CLM_112", "CLM_110"], strategy="CARD", graphic=c.spec(), visual_goal="One shape at two sizes", required_concepts=[])

# C10 ------------------------------------------------------------------------------------------
beat("C10", "B42", "interpretation", "SUMMARIZE_DIFFERENCES", [
    "So the heights were never impossible.",
    "Pointed arches reduced the push, rib vaults gathered it onto piers, and flying buttresses carried it outside and down to the ground.",
    "The walls in between could become glass."],
    ["CLM_130", "CLM_140", "CLM_152", "CLM_143"], strategy="HOLD_HIGHLIGHT", highlight_at_sentence=1, camera_move={"type": "PUSH_IN", "amount": 0.08},
    visual_goal="The section once more: ribs, flyer, buttress and windows lit in turn",
    required_concepts=[GOTHIC, "rib", "flying_buttress", "clerestory_window"],
    annotations=[note("B42_ch", "10 · Never impossible", 0, 2)])

c = Card("B43")
c.text("Not a simple story of progress", 0.5, 0.84, 0.046, 0)
for y, t, word in ((0.68, "Beauvais: new piers", "beauvais"), (0.59, "Amiens: an iron chain", "amiens"),
                   (0.5, "Saint-Denis: a bright choir over a crypt of older forms", "suger's")):
    c.text(t, 0.5, y, 0.032, 1, plate=True, word=word)
c.text("Centuries of trial and error", 0.5, 0.36, 0.036, 2, color=ACCENT)
beat("C10", "B43", "interpretation", "SUMMARIZE_DIFFERENCES", [
    "But it is not a simple story of progress.",
    "Beauvais needed new piers, Amiens needed an iron chain, and Suger's bright choir rose above a crypt of older forms.",
    "Each cathedral was a test in stone, built by people who learned from centuries of trial and error."],
    ["CLM_185", "CLM_190", "CLM_163", "CLM_110"], strategy="CARD", graphic=c.spec(), visual_goal="Not a linear progression", required_concepts=[])
beat("C10", "B44", "framing", "INTRODUCE_ARCHITECTURE", [
    "These models are illustrations, not structural analyses, and the arrows show ideas, not calculated forces."],
    strategy="HOLD", visual_goal="A last look at the section", required_concepts=[GOTHIC],
    annotations=[note("B44_note", "Models are illustrations, not structural analyses", 0, position="BOTTOM_RIGHT")])

c = Card("B45")
c.text("What should we explain next?", 0.5, 0.68, 0.056, 0)
c.text("Suggest a topic in the comments", 0.5, 0.54, 0.038, 1, color=ACCENT)
c.text("Like", 0.42, 0.4, 0.038, 2, plate=True, word="like")
c.text("Subscribe", 0.58, 0.4, 0.038, 2, plate=True, word="subscribe")
beat("C10", "B45", "framing", "SHOW_CONTEXT", [
    "Which building or structure should we explain next?",
    "Suggest a topic in the comments.",
    "And if you enjoyed this film, please like it and subscribe."],
    strategy="CARD", graphic=c.spec(), visual_goal="Closing call to action: plain text, no platform logos or buttons", required_concepts=[])

c = Card("B46")
c.text("How Gothic Cathedrals Reached Impossible Heights", 0.5, 0.8, 0.044, 0)
for y, line in ((0.66, "Sources: Columbia University (Life of a Cathedral; Stephen Murray); MIT (P. Block, 2005);"),
                (0.61, "Bibliothèque nationale de France; France Mémoire (A. Timbert);"),
                (0.56, "ECSMGE 2024 (Vernhes, Renault, Zotna); Association Beauvais Cathédrale"),
                (0.46, "3D models and diagrams are illustrative, not structural analyses")):
    c.text(line, 0.5, y, 0.026, 0, color=MUTED)
c.text("Architecture Story Studio", 0.5, 0.34, 0.032, 0)
beat("C10", "B46", "framing", "SHOW_CONTEXT", [
    "Thank you very much for watching.",
    "The sources are listed in the description."],
    strategy="CARD", graphic=c.spec(), visual_goal="Credits", required_concepts=[])


# ---------------------------------------------------------------- write
def main():
    narration = json.loads((HERE / "narration.template.json").read_text())
    narration["beats"] = [{"id": b["id"], "kind": b["kind"], "claim_ids": b["claims"], "sentences": b["sentences"]}
                          for b in BEATS]
    (HERE / "narration.json").write_text(json.dumps(narration, indent=2, ensure_ascii=False) + "\n")
    doc = {"schema": "narrative_beats/1", "project_id": "gothic-cathedral-heights",
           "title": "How Gothic Cathedrals Reached Impossible Heights", "status": "INTERNAL_REVIEW_DRAFT", "timing_mode": "AUDIO_LOCKED",
           "publication": {"restriction": "INTERNAL_ONLY",
                           "reason": "Revision g-r1: script for the owner's review; claims source-verified, not editorially approved."},
           "beats": []}
    for b in BEATS:
        v = dict(b["visual"])
        entry = {"beat_id": b["id"], "chapter": b["chapter"], "kind": b["kind"], "narrative_intent": b["intent"],
                 "claim_ids": b["claims"], "narration": " ".join(b["sentences"]),
                 "visual_goal": v.pop("visual_goal"), "required_concepts": v.pop("required_concepts", []),
                 "expected_complexity": v.pop("expected_complexity", "MEDIUM")}
        entry.update(v)
        doc["beats"].append(entry)
    (HERE / "visual_beats.json").write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
    chapters = {"schema": "chapters/1", "project_id": "gothic-cathedral-heights",
                "chapters": [{"id": cid, "title": title, "purpose": purpose,
                              "beat_ids": [b["id"] for b in BEATS if b["chapter"] == cid]}
                             for cid, title, purpose in CHAPTERS]}
    (HERE / "chapters.json").write_text(json.dumps(chapters, indent=2, ensure_ascii=False) + "\n")
    words = sum(len(s.split()) for b in BEATS for s in b["sentences"])
    print(f"{len(CHAPTERS)} chapters, {len(BEATS)} beats, {sum(len(b['sentences']) for b in BEATS)} sentences, "
          f"{words} words")


if __name__ == "__main__":
    main()
