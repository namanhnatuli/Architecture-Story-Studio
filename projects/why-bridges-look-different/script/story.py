"""Authoring source of "Why Bridges Don't All Look the Same" (M7).

    python3 projects/why-bridges-look-different/script/story.py

writes script/narration.json, script/visual_beats.json and script/chapters.json from the
chapters and beats below, so narration and visual beats always carry the same sentences.
Every fact beat cites claims from research/sources.json; every card is built from the small
helpers at the top (one visual language for titles, panels, diagrams, maps and photos).
Card coordinates: x, y in 0..1 of the frame (origin bottom-left); nothing below y 0.2 (the
subtitle zone ends at 0.17).
"""
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
ASPECT = 16 / 9
INK, MUTED, FAINT = "#24231F", "#55524A", "#8A867C"
STONE, WOOD, IRON, GROUND = "#B9A887", "#8C654D", "#4F5A64", "#C9CCBA"
LOAD, COMP, TENS, ACCENT = "#C25110", "#A3263A", "#16756F", "#1E5C96"


# ---------------------------------------------------------------- card helpers
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

    def image(self, asset, path, box, crop, sentence=0, drift=(0.012, 0.0), until=None):
        return self.add("image", sentence, until, asset=asset, path=path, box=[round(v, 4) for v in box],
                        crop=crop, drift=list(drift))

    def symbol(self, force, cx, cy, sentence=0):
        """Conceptual force symbol: arrowheads towards (compression) or away from (tension) each other."""
        half, gap = 0.028 / ASPECT, 0.004 / ASPECT
        color = COMP if force == "COMPRESSION" else TENS
        if force == "COMPRESSION":
            self.arrow([cx - half, cy], [cx - gap, cy], color, 0.006, sentence)
            self.arrow([cx + half, cy], [cx + gap, cy], color, 0.006, sentence)
        else:
            self.arrow([cx - gap, cy], [cx - half, cy], color, 0.006, sentence)
            self.arrow([cx + gap, cy], [cx + half, cy], color, 0.006, sentence)
        return self

    def tag(self, text, sentence=0):
        return self.text(text, 0.055, 0.915, 0.024, sentence, align="LEFT", color=MUTED, plate=True)

    def spec(self, background=None):
        out = {"fade_seconds": 0.35, "elements": self.elements}
        if background:
            out["background"] = background
        return out


PHOTO_CROP = {
    "IMG_HAER_CARROLLTON": [0.17, 0.11, 0.83, 0.89], "IMG_HAER_PROMONTORY": [0.025, 0.045, 0.955, 0.955],
    "IMG_HAER_BOLLMAN": [0.035, 0.045, 0.965, 0.955], "IMG_HAER_HUMPBACK": [0.035, 0.05, 0.968, 0.95]}
PHOTO_PATH = {
    "IMG_HAER_CARROLLTON": "assets/external/haer_md9_carrollton_viaduct_west_3840.jpg",
    "IMG_HAER_PROMONTORY": "assets/external/haer_ut64_promontory_trestle_790b_3840.jpg",
    "IMG_HAER_BOLLMAN": "assets/external/haer_md1_bollman_truss_east_3840.jpg",
    "IMG_HAER_HUMPBACK": "assets/external/haer_va_humpback_covered_bridge_west_3840.jpg"}


def photo_card(name, asset, title, lines, credit, chapter=None):
    """Archival photograph (left) + caption column (right); lines: [(sentence, text)]."""
    c = Card(name)
    if chapter:
        c.tag(chapter)
    c.image(asset, PHOTO_PATH[asset], [0.05, 0.21, 0.64, 0.88], PHOTO_CROP[asset], 0)
    c.text(title, 0.805, 0.82, 0.036, 0, plate=False)
    c.line([[0.69, 0.785], [0.92, 0.785]], FAINT, 0.003, 0)
    y = 0.72
    for s, t in lines:
        c.text(t, 0.805, y, 0.028, s, color=INK)
        y -= 0.062
    c.text(credit, 0.805, 0.235, 0.019, 0, color=MUTED)
    return c


def arch_ring(c, cx, y0, r1, r2, n, sentence, key_color=INK):
    """Voussoirs of a semicircular ring as polygons (height units; x scaled by the aspect)."""
    for k in range(n):
        a0, a1 = math.pi * k / n, math.pi * (k + 1) / n
        pts = []
        for r, a in ((r1, a0), (r2, a0), (r2, a1), (r1, a1)):
            pts.append([cx + r * math.cos(a) / ASPECT, y0 + r * math.sin(a)])
        c.polygon(pts, key_color if k == n // 2 else STONE, border="#7A6E58", sentence=sentence, layer=1)


# ---------------------------------------------------------------- the film
CHAPTERS = [
    ("C1", "Hook", "Three bridges, one gap: pose the central question within the first seconds."),
    ("C2", "The problem every bridge must solve", "Loads, supports and the load path every bridge shares."),
    ("C3", "The beam", "The beam arrangement: spans, bending, caps and posts; why it endures."),
    ("C4", "The arch", "Voussoirs and keystone, thrust and compression, supports, falsework, cost vs permanence."),
    ("C5", "The truss", "Triangles, axial members, chords, Pratt vs Warren, prefabrication."),
    ("C6", "Why different designs exist", "Materials, weather, site, span and the era: the trade-offs."),
    ("C7", "Real-world decisions", "Three documented 19th-century American bridges and the choices behind them."),
    ("C8", "Why they look different", "Answer the question; not a story of linear progress."),
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


# C1 -------------------------------------------------------------------------------------------
beat("C1", "B01", "framing", "COMPARE_VARIANTS", [
    "One bridge rests on rows of timber posts.",
    "Another leaps the gap in curves of stone.",
    "A third is a lattice of steel triangles.",
    "All three cross exactly the same gap."],
    strategy="DETAIL_THEN_OVERVIEW", visual_goal="Each structure alone, then all three at one scale",
    preferred_states=["timber_beam_bridge", "stone_arch_bridge", "steel_truss_bridge"], required_concepts=[])

c = Card("B02")
c.text("Why Bridges Don't All Look the Same", 0.5, 0.64, 0.072, 0)
c.line([[0.28, 0.585], [0.72, 0.585]], FAINT, 0.003, 0)
c.text("Same problem. Different answers.", 0.5, 0.5, 0.04, 1, color=MUTED)
for k, (w, x) in enumerate((("Materials", 0.32), ("Site", 0.5), ("Time", 0.68))):
    c.text(w, x, 0.36, 0.036, 2, plate=True, word=w.lower())
beat("C1", "B02", "framing", "SHOW_CONTEXT", [
    "So why don't bridges all look the same?",
    "It isn't because one design is simply better than the others.",
    "Each form is a different answer to the same problem, shaped by materials, by the site, and by the time it was built in."],
    strategy="CARD", graphic=c.spec(), visual_goal="Title card: the central question", required_concepts=[])

# C2 -------------------------------------------------------------------------------------------
beat("C2", "B03", "fact", "INTRODUCE_ARCHITECTURE", [
    "Every bridge has the same basic job.",
    "It has to carry loads: the traffic crossing it, and the weight of the bridge itself.",
    "And it has to pass all of that down into the ground on either side."],
    ["CLM_701", "CLM_702"], strategy="HOLD", visual_goal="A whole bridge; the load on its deck and the ground it must reach",
    required_concepts=["steel_truss_bridge"], annotations=[
        note("B03_ch", "2 · The problem every bridge must solve", 0, 2),
        {"id": "B03_load", "type": "LOAD_ARROW", "target": "deck", "point": "TOP", "count": 3, "text": "Load",
         "sentence": 1, "claim_id": "CLM_701"},
        {"id": "B03_ground", "type": "COMPONENT_LABEL", "target": {"concept": "ground", "pick": "RIGHTMOST"},
         "point": "TOP", "text": "Ground", "sentence": 2}])
beat("C2", "B04", "fact", "EXPLAIN_LOAD_PATH", [
    "Engineers often describe a bridge in two parts.",
    "The superstructure is the part that spans the gap, including the deck.",
    "The substructure is what holds it up: abutments at the ends, and sometimes piers in between.",
    "Load follows a path from the deck, through both parts, into the foundations."],
    ["CLM_702", "CLM_703", "CLM_704"], strategy="HOLD_HIGHLIGHT", highlight_at_sentence=2,
    visual_goal="Superstructure over substructure; a conceptual path to the foundations",
    required_concepts=["steel_truss_bridge", "substructure"], annotations=[
        {"id": "B04_super", "type": "HIGHLIGHT_REGION", "target": "superstructure", "text": "Superstructure",
         "sentence": 1, "until": 2, "claim_id": "CLM_703"},
        {"id": "B04_abut", "type": "COMPONENT_LABEL", "target": {"concept": "abutment", "pick": "LEFTMOST"},
         "point": "CENTER", "text": "Abutment", "sentence": 2, "claim_id": "CLM_704"},
        {"id": "B04_pier", "type": "COMPONENT_LABEL", "target": "pier", "point": "CENTER", "text": "Pier",
         "sentence": 2, "claim_id": "CLM_704"},
        {"id": "B04_path", "type": "CONCEPTUAL_LOAD_PATH", "style": "LOAD", "sentence": 3, "claim_id": "CLM_704",
         "path": [
             [{"target": {"concept": "deck", "pick": "LEFTMOST"}, "point": "TOP"},
              {"target": {"concept": "abutment", "pick": "LEFTMOST"}, "point": "TOP"},
              {"target": {"concept": "abutment", "pick": "LEFTMOST"}, "point": "BOTTOM"}],
             [{"target": {"concept": "deck", "pick": "LEFTMOST"}, "point": "TOP"},
              {"target": "pier", "point": "TOP"}, {"target": "pier", "point": "BOTTOM"}],
             [{"target": {"concept": "deck", "pick": "RIGHTMOST"}, "point": "TOP"}, {"target": "pier", "point": "TOP"}],
             [{"target": {"concept": "deck", "pick": "RIGHTMOST"}, "point": "TOP"},
              {"target": {"concept": "abutment", "pick": "RIGHTMOST"}, "point": "TOP"},
              {"target": {"concept": "abutment", "pick": "RIGHTMOST"}, "point": "BOTTOM"}]]},
        {"id": "B04_found", "type": "COMPONENT_LABEL", "target": {"concept": "abutment", "pick": "LEFTMOST"},
         "point": "BOTTOM", "text": "Foundation", "sentence": 3, "claim_id": "CLM_704"}])
beat("C2", "B05", "framing", "SHOW_CONTEXT", [
    "What changes from one bridge to the next is how that path is arranged.",
    "So let's start again with an empty gap."],
    visual_goal="The empty site: the gap any structure must span", required_concepts=["river_crossing_site"])

# C3 -------------------------------------------------------------------------------------------
beat("C3", "B06", "fact", "INTRODUCE_ARCHITECTURE", [
    "The first answer is the beam.",
    "Lay a strong member across the gap, support it at each end, and you have a bridge.",
    "It is one of the oldest ideas in bridge building."],
    ["CLM_705", "CLM_720"], strategy="ASSEMBLE_IN", visual_goal="A timber beam bridge appears on the empty site",
    required_concepts=["timber_beam_bridge", "stringer"], visual_repair_preference=["GHOST", "REFRAME"],
    annotations=[note("B06_ch", "3 · The beam", 0)])
beat("C3", "B07", "fact", "EXPLAIN_STRUCTURE", [
    "This timber bridge is a row of short beam spans.",
    "Planks form the deck, long beams carry the planks, cap beams carry the beams, and posts carry the caps."],
    ["CLM_705", "CLM_707"], strategy="HIGHLIGHT_THEN_EXPLODE", visual_goal="Taken apart by layer",
    required_concepts=["timber_beam_bridge", "deck_planks", "stringer", "cap_beam"])
beat("C3", "B08", "fact", "EXPLAIN_LOAD_PATH", [
    "Each beam carries its load by resisting bending.",
    "At each support, a cap beam spreads the load onto the posts.",
    "The posts then carry it down into the ground in compression."],
    ["CLM_706", "CLM_707"], strategy="HOLD_HIGHLIGHT", highlight_at_sentence=0,
    visual_repair_preference=["GHOST", "REFRAME"], visual_goal="Beam, cap, posts: the path to the ground",
    required_concepts=["timber_beam_bridge", "stringer"], annotations=[
        {"id": "B08_load", "type": "LOAD_ARROW", "target": {"concept": "deck_planks", "pick": "CENTERMOST"},
         "point": "TOP", "count": 2, "text": "Load", "sentence": 0, "claim_id": "CLM_701"},
        {"id": "B08_bend", "type": "CALLOUT", "target": {"concept": "stringer", "pick": "CENTERMOST"},
         "point": "BOTTOM", "text": "Beam resists bending", "sentence": 0, "until": 1, "claim_id": "CLM_706"},
        {"id": "B08_path", "type": "CONCEPTUAL_LOAD_PATH", "style": "LOAD", "sentence": 1, "claim_id": "CLM_707",
         "path": [[{"target": {"concept": "deck_planks", "pick": "CENTERMOST"}, "point": "TOP"},
                   {"target": {"concept": "cap_beam", "pick": "CENTERMOST"}, "point": "TOP"},
                   {"target": {"concept": "trestle_bent", "pick": "CENTERMOST"}, "point": "BOTTOM"}]]},
        {"id": "B08_cap", "type": "COMPONENT_LABEL", "target": {"concept": "cap_beam", "pick": "CENTERMOST"},
         "point": "CENTER", "text": "Cap beam", "sentence": 1, "claim_id": "CLM_707"},
        {"id": "B08_posts", "type": "CALLOUT", "target": {"concept": "trestle_bent", "pick": "CENTERMOST"},
         "point": "CENTER", "text": "Posts: compression", "force": "COMPRESSION", "sentence": 2,
         "claim_id": "CLM_707"}])
beat("C3", "B09", "fact", "INTRODUCE_ARCHITECTURE", [
    "Beams are simple, and wood was usually easy to find.",
    "That is why timber beam bridges were still being built long after timber trusses fell out of use, and why they are still built on quiet rural roads and in parks today.",
    "But many early timber bridges had relatively short spans, which is why this one needs so many posts."],
    ["CLM_721", "CLM_722"], strategy="HOLD_HIGHLIGHT", highlight_at_sentence=2,
    camera_move={"type": "PUSH_IN", "amount": 0.12}, visual_goal="The posts that short spans require",
    required_concepts=["timber_beam_bridge", "trestle_bent"],
    annotations=[note("B09_note", "Illustrative model", 0, position="BOTTOM_RIGHT")])

# C4 -------------------------------------------------------------------------------------------
beat("C4", "B10", "fact", "SHOW_COMPONENT", [
    "A masonry arch takes a different approach.",
    "It is built from wedge-shaped stones called voussoirs, with a keystone at the crown."],
    ["CLM_708"], visual_goal="One arch ring's voussoirs and keystone read as separate wedge-shaped pieces",
    required_concepts=["stone_arch_bridge", "arch_ring"],
    focus_concepts=[{"concept": "voussoir", "group": "arch_2"}, {"concept": "keystone", "group": "arch_2"}],
    annotations=[note("B10_ch", "4 · The arch", 0, 1),
                 {"id": "B10_vous", "type": "COMPONENT_LABEL",
                  "target": {"concept": "voussoir", "group": "arch_2", "pick": "LEFTMOST"}, "point": "CENTER",
                  "text": "Voussoirs", "sentence": 1, "claim_id": "CLM_708"},
                 {"id": "B10_key", "type": "COMPONENT_LABEL", "target": {"concept": "keystone", "group": "arch_2"},
                  "point": "TOP", "text": "Keystone", "sentence": 1, "claim_id": "CLM_708"}])
beat("C4", "B11", "fact", "EXPLAIN_LOAD_PATH", [
    "The curve turns the downward load into thrust along the arch, pressing the stones together.",
    "So the arch works mainly in compression.",
    "At each end it pushes outward and down on its supports, and the supports push back."],
    ["CLM_709", "CLM_710"], strategy="HOLD_HIGHLIGHT", highlight_at_sentence=0,
    visual_goal="Thrust along one ring; inclined reactions", required_concepts=["stone_arch_bridge", "arch_ring"],
    annotations=[
        {"id": "B11_load", "type": "LOAD_ARROW", "target": {"concept": "keystone", "group": "arch_2"}, "point": "TOP",
         "count": 1, "text": "Load", "sentence": 0, "claim_id": "CLM_709"},
        {"id": "B11_thrust", "type": "CONCEPTUAL_LOAD_PATH", "style": "COMPRESSION", "sentence": 0,
         "claim_id": "CLM_709", "along": {"concept": "arch_ring", "group": "arch_2"}},
        {"id": "B11_comp", "type": "CALLOUT", "target": {"concept": "arch_ring", "group": "arch_2"},
         "point": "TOP_LEFT", "text": "Mainly compression", "force": "COMPRESSION", "sentence": 1,
         "claim_id": "CLM_709"},
        {"id": "B11_react", "type": "REACTION_ARROW", "target": {"concept": "arch_ring", "group": "arch_2"},
         "points": ["BOTTOM_LEFT", "BOTTOM_RIGHT"], "direction": "UP_INWARD", "text": "Supports push back",
         "sentence": 2, "claim_id": "CLM_710"}])
beat("C4", "B12", "fact", "INTRODUCE_ARCHITECTURE", [
    "That is why arches suit materials that are strong under compression, like stone.",
    "And it is why the supports matter so much: the abutments have to push inward on the arch, against its thrust."],
    ["CLM_726", "CLM_709", "CLM_710"], strategy="HOLD", camera_mode="SIDE_ELEVATION",
    visual_goal="The supports that hold the arch's ends", required_concepts=["stone_arch_bridge", "abutment", "pier"],
    annotations=[
        {"id": "B12_abut", "type": "COMPONENT_LABEL", "target": {"concept": "abutment", "pick": "LEFTMOST"},
         "point": "TOP", "text": "Abutment", "sentence": 1, "claim_id": "CLM_710"},
        {"id": "B12_pier", "type": "COMPONENT_LABEL", "target": {"concept": "pier", "pick": "LEFTMOST"},
         "point": "TOP", "text": "Pier", "sentence": 1, "claim_id": "CLM_710"}])

c = Card("B13")
c.tag("Conceptual diagram — not to scale")
c.line([[0.12, 0.28], [0.88, 0.28]], GROUND, 0.012, 0)
# abutments carry the ring's feet (inner foot 0.5 -/+ 0.30/ASPECT, outer 0.5 -/+ 0.37/ASPECT)
c.rect([0.24, 0.28, 0.5 - 0.295 / ASPECT, 0.36], STONE, sentence=0)
c.rect([0.5 + 0.295 / ASPECT, 0.28, 0.76, 0.36], STONE, sentence=0)
arch_ring(c, 0.5, 0.36, 0.30, 0.37, 13, 0, key_color="#8D7B5A")
for k in range(-3, 4):   # falsework posts stand inside the opening, up to the curved centring
    x = 0.5 + k * 0.045
    top = 0.36 + 0.295 * math.sin(math.acos((x - 0.5) * ASPECT / 0.295))
    c.line([[x, 0.28], [x, top]], WOOD, 0.007, 1, layer=-1)
pts = [[0.5 + 0.295 * math.cos(a) / ASPECT, 0.36 + 0.295 * math.sin(a)] for a in [math.pi * k / 24 for k in range(25)]]
c.line(pts, WOOD, 0.008, 1)
c.line([[0.5 - 0.29 / ASPECT, 0.36], [0.5 + 0.29 / ASPECT, 0.36]], WOOD, 0.007, 1)
c.text("Keystone", 0.5, 0.80, 0.03, 0, plate=True)
c.text("Falsework (temporary)", 0.5, 0.47, 0.03, 1, plate=True)
c.text("Carpenters build the frame", 0.205, 0.66, 0.026, 2, plate=True)
c.text("Masons lay the stones", 0.795, 0.66, 0.026, 2, plate=True)
beat("C4", "B13", "fact", "EXPLAIN_STRUCTURE", [
    "Building an arch takes support of its own.",
    "While a stone arch is being built, a temporary timber frame called falsework holds the stones in place.",
    "So building one called for carpenters as well as skilled masons."],
    ["CLM_723"], strategy="CARD", graphic=c.spec(), visual_goal="Falsework under an arch ring (diagram)",
    required_concepts=[])

c = Card("B14")
c.text("A trade-off", 0.5, 0.86, 0.05, 0)
c.text("Timber beam", 0.3, 0.73, 0.04, 0, plate=True)
c.text("Stone arch", 0.7, 0.73, 0.04, 0, plate=True)
for y, label, a, b, s, w in ((0.6, "Cost to build", "lower", "higher", 0, "expensive"),
                             (0.48, "Permanence", "lower", "higher", 1, "permanence"),
                             (0.36, "Favoured for", "other crossings", "busy, important routes", 1, "busy")):
    c.text(label, 0.5, y, 0.026, s, color=MUTED, word=w)
    c.text(a, 0.3, y - 0.045, 0.032, s, word=w)
    c.text(b, 0.7, y - 0.045, 0.032, s, word=w)
c.rect([0.17, 0.29, 0.43, 0.775], border=WOOD, sentence=2, border_width=0.005, layer=-1)
c.text("Lower cost made up for less permanence", 0.3, 0.235, 0.024, 2, plate=True, word="cost")
c.text("After NCHRP 25-25(15), 2005", 0.7, 0.235, 0.02, 0, color=MUTED)
beat("C4", "B14", "fact", "EXPLAIN_DESIGN_CHANGE", [
    "Stone arches were generally more expensive to build than timber bridges.",
    "But stone was the preferred choice where durability and permanence were required, so arches were favoured on busy routes and in important places.",
    "Elsewhere, the lower cost of timber made up for its lack of permanence."],
    ["CLM_724", "CLM_725"], strategy="CARD", graphic=c.spec(), visual_goal="Cost versus permanence panel",
    required_concepts=[])

# C5 -------------------------------------------------------------------------------------------
beat("C5", "B15", "fact", "INTRODUCE_ARCHITECTURE", [
    "A third approach is the truss.",
    "It builds a structure out of straight members, joined into triangles.",
    "Each member is mainly pulled or pushed along its length, in tension or in compression."],
    ["CLM_711", "CLM_712"], strategy="HOLD_HIGHLIGHT", highlight_at_sentence=1,
    visual_goal="Triangulated members and joints", required_concepts=["steel_truss_bridge", {"concept": "truss_members", "group": "truss_south"}],
    annotations=[note("B15_ch", "5 · The truss", 0, 1),
                 {"id": "B15_joints", "type": "COMPONENT_LABEL",
                  "target": {"concept": "truss_joint", "group": "truss_south", "pick": "LEFTMOST"},
                  "point": "TOP_LEFT", "text": "Joints", "sentence": 1, "claim_id": "CLM_711"},
                 {"id": "B15_legend", "type": "TENSION_COMPRESSION_LEGEND", "sentence": 2, "claim_id": "CLM_712"}])
beat("C5", "B16", "fact", "EXPLAIN_LOAD_PATH", [
    "In a simple span like these, under a downward load, the top chord is squeezed and the bottom chord is stretched.",
    "Inside, some web members are in compression and others are in tension."],
    ["CLM_713", "CLM_714"], strategy="HOLD", camera_mode="SIDE_ELEVATION",
    visual_goal="Chords named, web members not colour-coded", required_concepts=["steel_truss_bridge"],
    annotations=[
        {"id": "B16_legend", "type": "TENSION_COMPRESSION_LEGEND", "sentence": 0, "claim_id": "CLM_712"},
        {"id": "B16_top", "type": "CALLOUT", "target": {"concept": "truss_chord", "group": "truss_south", "pick": "LEFTMOST"},
         "point": "TOP", "text": "Top chord: compression", "force": "COMPRESSION", "sentence": 0, "word": "top", "claim_id": "CLM_713"},
        {"id": "B16_bottom", "type": "CALLOUT",
         "target": {"concept": "truss_chord", "group": "truss_south", "pick": "LEFTMOST"}, "point": "BOTTOM",
         "text": "Bottom chord: tension", "force": "TENSION", "sentence": 0, "word": "bottom", "claim_id": "CLM_713"},
        {"id": "B16_web", "type": "COMPONENT_LABEL",
         "target": {"concept": "diagonal_members", "group": "truss_south", "pick": "RIGHTMOST"}, "point": "CENTER",
         "text": "Web members", "sentence": 1, "claim_id": "CLM_714"}])
beat("C5", "B17", "fact", "EXPLAIN_DESIGN_CHANGE", [
    "The triangles can be arranged in different patterns.",
    "This is a Pratt truss.",
    "In the original design, patented in 1844, its verticals were timber and its diagonals were iron rods.",
    "Swap the web for diagonals that alternate in direction, and you have a Warren truss, patented in 1848.",
    "Both patterns carry load through triangles; they simply arrange the members differently."],
    ["CLM_727", "CLM_728", "CLM_711"], strategy="HIGHLIGHT_REPLACE_HIGHLIGHT",
    visual_goal="Pratt and Warren web patterns on the same chords",
    preferred_states=["pratt_truss", "warren_truss"], required_concepts=["truss_web"],
    annotations=[{**note("B17_pratt", "Pratt truss (patented 1844)", 1, 3), "claim_id": "CLM_727"},
                 {**note("B17_warren", "Warren truss (patented 1848)", 3), "claim_id": "CLM_728"}])
beat("C5", "B18", "fact", "EXPLAIN_STRUCTURE", [
    "Trusses also changed how bridges were built.",
    "By the middle of the nineteenth century, shops were making and drilling truss members, then shipping them to the bridge site, ready to assemble.",
    "And by 1860, the railroads relied almost entirely on these prefabricated parts."],
    ["CLM_729"], strategy="EXPLODE", visual_goal="The truss as separate prefabricated members",
    required_concepts=["steel_truss_bridge"],
    annotations=[{**note("B18_shop", "Members made and drilled in shops", 1, 2), "claim_id": "CLM_729"},
                 {**note("B18_1860", "By 1860: prefabricated parts", 2), "claim_id": "CLM_729"}])

# C6 -------------------------------------------------------------------------------------------
c = Card("B19")
c.tag("6 · Why different designs exist")
c.text("Which design is best?", 0.5, 0.66, 0.068, 0)
c.text("It depends.", 0.5, 0.53, 0.048, 1, color=MUTED)
for w, x in (("Materials", 0.2), ("Site", 0.35), ("Span", 0.5), ("Cost", 0.65), ("Skills", 0.8)):
    c.text(w, x, 0.38, 0.034, 2, plate=True, word=w.lower())
beat("C6", "B19", "framing", "SHOW_CONTEXT", [
    "So which design is best?",
    "The honest answer is that it depends.",
    "Materials, the site, the span, cost, and the skills available all pull in different directions."],
    strategy="CARD", graphic=c.spec(), visual_goal="The factors that shape a bridge", required_concepts=[])

beat("C6", "B20A", "fact", "INTRODUCE_ARCHITECTURE", [
    "Start with the materials themselves.",
    "An arch needs a material that is strong under compression, and stone is."],
    ["CLM_726"], strategy="HOLD_HIGHLIGHT", highlight_at_sentence=1, visual_goal="Stone in compression: the arch rings",
    required_concepts=["stone_arch_bridge", "arch_ring"],
    annotations=[note("B20A_note", "Stone: strong under compression", 1)])
beat("C6", "B20B", "fact", "INTRODUCE_ARCHITECTURE", [
    "A truss needs members that can work in tension as well as compression.",
    "Wrought iron was valued for exactly that: one historian calls it a material strong equally in tension and in compression."],
    ["CLM_712", "CLM_735"], strategy="HOLD_HIGHLIGHT", highlight_at_sentence=0,
    visual_goal="Truss members that work both ways",
    required_concepts=["steel_truss_bridge", {"concept": "truss_members", "group": "truss_south"}],
    annotations=[note("B20B_note", "Truss members: tension and compression", 0, 1),
                 {**note("B20B_iron", "Wrought iron: valued in tension and compression", 1), "claim_id": "CLM_735"}])
beat("C6", "B20C", "fact", "INTRODUCE_ARCHITECTURE", [
    "Wood was often plentiful and cheap, but wooden bridges were vulnerable to decay."],
    ["CLM_742", "CLM_734"], strategy="HOLD", visual_goal="The timber structure",
    required_concepts=["timber_beam_bridge"],
    annotations=[note("B20C_note", "Timber: plentiful and cheap, but it decays", 0)])

beat("C6", "B21", "fact", "SHOW_CONTEXT", [
    "That is one reason many timber truss bridges were covered with a roof and siding, to protect them from the weather.",
    "This is the Humpback Covered Bridge, built in 1857 over Dunlap Creek."],
    ["CLM_733", "CLM_746"], strategy="CARD", visual_goal="Archival photograph of a covered timber bridge",
    graphic=photo_card("B21", "IMG_HAER_HUMPBACK", "Humpback Covered Bridge",
                       [(0, "Roof and siding protect"), (0, "the timber trusses"), (1, "Dunlap Creek, built 1857"),
                        (1, "Covington, Virginia")],
                       "Photo: Jack E. Boucher, HAER, Library of Congress (public domain)").spec(), required_concepts=[])

c = Card("B22")
c.tag("Schematic — not to scale")
c.polygon([[0.05, 0.6], [0.24, 0.58], [0.36, 0.33], [0.5, 0.26], [0.64, 0.33], [0.76, 0.58], [0.95, 0.6],
           [0.95, 0.21], [0.05, 0.21]], GROUND, sentence=0)
c.line([[0.25, 0.6], [0.37, 0.355], [0.5, 0.285], [0.63, 0.355], [0.75, 0.6]], COMP, 0.005, 1, dash=[0.02, 0.012])
c.text("Down and up again: too steep for trains", 0.5, 0.42, 0.026, 1, plate=True, until=2)
for x, bottom in ((0.33, 0.38), (0.41, 0.3), (0.5, 0.27), (0.59, 0.3), (0.67, 0.38)):
    c.rect([x - 0.012, bottom, x + 0.012, 0.64], STONE, sentence=2)
c.line([[0.05, 0.645], [0.95, 0.645]], INK, 0.008, 2)
c.text("A viaduct keeps the line nearly level", 0.5, 0.74, 0.03, 2, plate=True)
beat("C6", "B22", "fact", "SHOW_CONTEXT", [
    "The site of a bridge matters too.",
    "Railway engines have limited traction, so railways need gentle gradients.",
    "Where a valley was too deep and wide to fill with an embankment, engineers built viaducts and trestles to keep the line nearly straight and level."],
    ["CLM_736"], strategy="CARD", graphic=c.spec(), visual_goal="Valley profile with a level line on piers",
    required_concepts=[])

beat("C6", "B23", "framing", "SHOW_CONTEXT", [
    "Then there is span: how far a single structure has to reach."],
    visual_goal="The gap itself: the distance one structure must cross", required_concepts=["river_crossing_site"],
    annotations=[note("B23_note", "Span: how far one structure reaches", 0)])

c = Card("B23B")
c.text("How far one structure can reach", 0.5, 0.86, 0.045, 0)
x0, scale = 0.12, 0.72 / 400.0
for y, ft, label, color, s, w in ((0.68, 30, "Simple king post truss: about 30 ft", WOOD, 0, None),
                                  (0.5, 220, "Cabin John Aqueduct, stone arch (1864): 220 ft", STONE, 1, "cabin"),
                                  (0.32, 400, "Some through trusses: approaching 400 ft", IRON, 1, "trusses")):
    c.add("rect", s, None, box=[round(x0, 4), round(y - 0.025, 4), round(x0 + ft * scale, 4), round(y + 0.025, 4)],
          layer=0, color=color, **({"word": w} if w else {}))
    c.text(label, x0, y + 0.065, 0.028, s, align="LEFT", word=w)
c.text("Spans as given in NCHRP 25-25(15), 2005 \u2014 bars to scale", 0.5, 0.22, 0.02, 0, color=MUTED)
beat("C6", "B23B", "fact", "EXPLAIN_STRUCTURE", [
    "A simple king post truss could span only about thirty feet.",
    "What one report calls America's greatest stone arch, the Cabin John Aqueduct Bridge, spans 220 feet, and some through trusses approach 400."],
    ["CLM_731", "CLM_732", "CLM_730"], strategy="CARD", graphic=c.spec(), visual_goal="Span scale (sourced values)",
    required_concepts=[])


CHAR_W = 0.26   # text width per character in units of the text size (measured from card QA boxes)


def text_width(text, size, plate=True):
    return CHAR_W * size * len(text) + (0.02 if plate else 0.0)


def clamp_x(x, w, lo=0.06, hi=0.94):
    """Centre x so a text of width w stays inside the title-safe area."""
    return min(max(x, lo + w / 2), hi - w / 2)


def timeline(name, events, bands, extra=None):
    """Axis 1820-1945; event labels go to the first free row (above/below alternating), so two
    labels never overlap; every label is clamped inside the safe area."""
    c = Card(name)
    X = lambda year: 0.08 + (year - 1820) / 125.0 * 0.84   # noqa: E731
    c.line([[0.08, 0.5], [0.92, 0.5]], INK, 0.006, 0)
    for year in (1820, 1840, 1860, 1880, 1900, 1920, 1940):
        c.line([[X(year), 0.485], [X(year), 0.515]], INK, 0.004, 0)
        c.text(str(year), X(year), 0.455, 0.022, 0, color=MUTED)
    rows = {0.64: [], 0.72: [], 0.36: [], 0.28: []}
    prefs = ((0.64, 0.72, 0.36, 0.28), (0.36, 0.28, 0.64, 0.72))
    for k, (year, label, s) in enumerate(events):
        text = f"{year}  {label}"
        w = text_width(text, 0.025)
        x = clamp_x(X(year), w)
        y = next(r for r in prefs[k % 2] if all(x + w / 2 + 0.01 < a or x - w / 2 - 0.01 > b for a, b in rows[r]))
        rows[y].append((x - w / 2, x + w / 2))
        c.line([[X(year), 0.5], [X(year), y - 0.03 if y > 0.5 else y + 0.03]], FAINT, 0.003, s)
        c.circle([X(year), 0.5], 0.009, INK, s)
        c.text(text, x, y, 0.025, s, plate=True)
    for y0, y1, label, color, s, ly in bands:
        c.rect([X(y0), 0.53, X(y1), 0.56], color, sentence=s)
        c.text(label, clamp_x((X(y0) + X(y1)) / 2, text_width(label, 0.024)), ly, 0.024, s, plate=True)
    if extra:
        extra(c)
    return c


TL_EVENTS = [(1829, "Carrollton Viaduct (stone)", 0), (1844, "Pratt truss patented", 0),
             (1848, "Warren truss patented", 0), (1860, "Prefabricated truss parts", 0)]
c = timeline("B24", TL_EVENTS, [(1880, 1925, "Metal trusses spread; stone arches decline", IRON, 1, 0.78),
                                (1929, 1939, "Great Depression: stone arches return", STONE, 2, 0.7)])
beat("C6", "B24", "fact", "SHOW_CONTEXT", [
    "Finally, every bridge belongs to its time.",
    "As metal trusses spread, skilled masons became fewer and reinforced concrete arrived, stone arch construction declined.",
    "Then, during the Great Depression, it briefly returned."],
    ["CLM_738", "CLM_739", "CLM_727", "CLM_728", "CLM_729"], strategy="CARD", graphic=c.spec(),
    visual_goal="Timeline (dates from the evidence registry)", required_concepts=[])

# C7 -------------------------------------------------------------------------------------------
c = Card("B25")
c.tag("7 · Real-world decisions")
c.rect([0.08, 0.3, 0.92, 0.8], "#E2DFD6", sentence=0)
c.rect([0.08, 0.3, 0.92, 0.8], border="#9C988D", sentence=0, border_width=0.003)
c.line([[0.5, 0.31], [0.5, 0.79]], "#B8B4A9", 0.003, 0, dash=[0.015, 0.012])
c.text("WEST", 0.29, 0.74, 0.03, 0, color=MUTED)
c.text("EAST", 0.71, 0.74, 0.03, 0, color=MUTED)
c.text("United States — schematic, not to scale", 0.5, 0.25, 0.022, 0, color=MUTED)
c.text("Timber, built fast", 0.29, 0.62, 0.03, 1, plate=True)
c.text("Massive stone viaducts", 0.71, 0.62, 0.03, 1, plate=True)
c.circle([0.27, 0.46], 0.012, WOOD, 2)
c.text("Corinne, Utah", 0.27, 0.405, 0.025, 2)
c.circle([0.84, 0.47], 0.012, STONE, 2)
c.text("Baltimore", 0.84, 0.415, 0.025, 2)
c.circle([0.81, 0.53], 0.012, IRON, 2)
c.text("Savage, Maryland", 0.765, 0.54, 0.025, 2, align="RIGHT")
beat("C7", "B25", "fact", "SHOW_CONTEXT", [
    "These trade-offs played out across nineteenth-century America as the railways spread.",
    "In the East, railroads built massive stone viaducts, while western builders generally used timber.",
    "Three documented examples show how differently builders answered."],
    ["CLM_741", "CLM_742"], strategy="CARD", graphic=c.spec(), visual_goal="Schematic map: East and West",
    required_concepts=[])
beat("C7", "B26", "fact", "SHOW_CONTEXT", [
    "Near Baltimore, the Carrollton Viaduct was completed in 1829.",
    "Built of roughly twelve thousand granite blocks, it carries the railway over Gwynns Falls on an eighty foot arch.",
    "A national report in 2005 called it the world's oldest stone railroad span still in service."],
    ["CLM_739", "CLM_740"], strategy="CARD", visual_goal="Archival photograph of the Carrollton Viaduct",
    graphic=photo_card("B26", "IMG_HAER_CARROLLTON", "Carrollton Viaduct",
                       [(0, "Baltimore, Maryland"), (0, "completed 1829"), (1, "about 12,000 granite blocks"),
                        (1, "80 ft arch over Gwynns Falls")],
                       "Photo: William E. Barrett, HAER, Library of Congress (public domain)").spec(), required_concepts=[])
beat("C7", "B27", "interpretation", "INTRODUCE_ARCHITECTURE", [
    "Early railroads needed durable bridges to carry heavy trains.",
    "For a line meant to last, stone was the answer."],
    ["CLM_741", "CLM_725"], strategy="HOLD", camera_move={"type": "PUSH_IN", "amount": 0.14},
    visual_goal="The stone arch archetype", required_concepts=["stone_arch_bridge"],
    annotations=[note("B27_note", "Illustrative model, not the Carrollton Viaduct", 0, position="BOTTOM_RIGHT")])
beat("C7", "B28", "fact", "SHOW_CONTEXT", [
    "In the West, the pressure was different.",
    "Railroads had to open new lines quickly and economically, and timber was abundant and cheap.",
    "This timber trestle near Corinne, Utah, was built in 1872 by the Central Pacific Railroad."],
    ["CLM_742", "CLM_743"], strategy="CARD", visual_goal="Archival photograph of a timber trestle",
    graphic=photo_card("B28", "IMG_HAER_PROMONTORY", "Promontory Route trestle",
                       [(1, "Timber: abundant, cheap"), (1, "and quick to build"), (2, "near Corinne, Utah"),
                        (2, "Central Pacific, 1872")],
                       "Photo: HAER, Library of Congress (public domain)").spec(), required_concepts=[])
beat("C7", "B29", "interpretation", "INTRODUCE_ARCHITECTURE", [
    "A trestle is a succession of towers supporting short spans.",
    "It is the same beam idea as our timber model, repeated as often as the crossing needs."],
    ["CLM_737"], strategy="HOLD_HIGHLIGHT", highlight_at_sentence=0, camera_move={"type": "PUSH_IN", "amount": 0.1},
    visual_goal="The timber archetype's repeated bents", required_concepts=["timber_beam_bridge", "trestle_bent"],
    annotations=[note("B29_note", "Illustrative model, not the Promontory trestle", 0, position="BOTTOM_RIGHT")])
beat("C7", "B30", "fact", "SHOW_CONTEXT", [
    "Iron offered a third path.",
    "The Bollman truss, patented in 1852, was one of the first designs to use iron in all of its essential structural parts.",
    "It could be built relatively quickly and inexpensively, while offering the long-lasting qualities of metal.",
    "The bridge at Savage, Maryland, is the only remaining example of the design."],
    ["CLM_744", "CLM_745"], strategy="CARD", visual_goal="Archival photograph of the Bollman truss",
    graphic=photo_card("B30", "IMG_HAER_BOLLMAN", "Bollman Truss Bridge",
                       [(1, "Patented 1852"), (1, "iron in all essential parts"), (2, "quick, inexpensive,"),
                        (2, "long-lasting"), (3, "Savage, Maryland")],
                       "Photo: William E. Barrett, HAER, Library of Congress (public domain)").spec(), required_concepts=[])

c = Card("B31")
for k, (asset, label, s) in enumerate((("IMG_HAER_CARROLLTON", "Stone: permanence", 0),
                                       ("IMG_HAER_PROMONTORY", "Timber: speed and economy", 0),
                                       ("IMG_HAER_BOLLMAN", "Iron: some of both", 0))):
    x0 = 0.06 + k * 0.305
    c.image(asset, PHOTO_PATH[asset], [x0, 0.42, x0 + 0.27, 0.86], PHOTO_CROP[asset], s, drift=(0.004, 0.0))
    c.text(label, x0 + 0.135, 0.355, 0.03, s, plate=True)
c.text("Three places, three sets of constraints", 0.5, 0.27, 0.032, 1, color=MUTED)
c.text("Photos: HAER, Library of Congress (public domain)", 0.5, 0.215, 0.018, 0, color=MUTED)
beat("C7", "B31", "interpretation", "SUMMARIZE_DIFFERENCES", [
    "Stone for permanence, timber for speed and economy, and iron trusses that offered some of both.",
    "Three places, three sets of constraints, three different bridges."],
    ["CLM_741", "CLM_742", "CLM_744"], strategy="CARD", graphic=c.spec(), visual_goal="Three answers, side by side",
    required_concepts=[])

# C8 -------------------------------------------------------------------------------------------
beat("C8", "B32", "interpretation", "SUMMARIZE_DIFFERENCES", [
    "So why don't bridges all look the same?",
    "Because a bridge's form comes from two things working together.",
    "One is how its structure carries load: beams resist bending, arches work in compression, and trusses share load among members in tension and compression."],
    ["CLM_706", "CLM_709", "CLM_712"], strategy="COMPARE_SIDE_BY_SIDE",
    visual_goal="The three structures at one scale", preferred_states=["timber_beam_bridge", "stone_arch_bridge", "steel_truss_bridge"],
    required_concepts=[], annotations=[note("B32_ch", "8 · Why they look different", 0, 2),
                                       note("B32_one", "1 · How the structure carries load", 2)])

c = Card("B32B")
c.text("2 \u00b7 The world it was built in", 0.5, 0.66, 0.056, 0)
for w, x in (("Materials", 0.18), ("Site", 0.34), ("Span", 0.5), ("Budget", 0.66), ("Builders", 0.82)):
    c.text(w, x, 0.46, 0.036, 0, plate=True, word=w.lower())
beat("C8", "B32B", "interpretation", "SUMMARIZE_DIFFERENCES", [
    "The other is the world it was built in: its materials, its site, its span, its budget and its builders."],
    ["CLM_742", "CLM_724"], strategy="CARD", graphic=c.spec(), visual_goal="The second answer: the world around it",
    required_concepts=[])

c = timeline("B33", TL_EVENTS, [(1929, 1939, "Stone arches return briefly", STONE, 1, 0.7)],
             extra=lambda c: (c.text("Today: timber beam bridges", 0.8, 0.86, 0.025, 1, plate=True),
                              c.text("are still built on quiet roads", 0.8, 0.805, 0.025, 1, plate=True)))
beat("C8", "B33", "interpretation", "SUMMARIZE_DIFFERENCES", [
    "And it is not a simple story of progress.",
    "Timber beam bridges are still built today, and stone arches briefly returned during the Great Depression.",
    "Each form can still be the right answer in the right place."],
    ["CLM_721", "CLM_738"], strategy="CARD", graphic=c.spec(), visual_goal="Not a linear progression (timeline)",
    required_concepts=[])
beat("C8", "B34", "framing", "INTRODUCE_ARCHITECTURE", [
    "Next time you cross a bridge, look at its shape.",
    "It shows how the load reaches the ground, and something about the people who built it.",
    "These models are illustrations, not engineering designs, and the arrows show ideas, not calculated forces."],
    strategy="HOLD", camera_move={"type": "PUSH_IN", "amount": 0.12}, visual_goal="A last look at a bridge",
    required_concepts=["stone_arch_bridge"],
    annotations=[note("B34_note", "Models are illustrations, not engineering designs", 2, position="BOTTOM_RIGHT")])

c = Card("B35")
c.text("Why Bridges Don't All Look the Same", 0.5, 0.8, 0.05, 0)
# The narration credit line was removed on the owner's instruction (2026-10-30); the AI-narration
# disclosure the Kokoro clearance asks for stays in review/YOUTUBE_DESCRIPTION.md.
for y, line in ((0.665, "Archival photographs: Historic American Engineering Record,"),
                (0.615, "Library of Congress Prints & Photographs Division (public domain)"),
                (0.525, "Sources: TRB NCHRP 25-25(15); FHWA; Ohio DOT; ASCE;"),
                (0.475, "SteelConstruction.info; Yale-New Haven Teachers Institute"),
                (0.385, "3D models and diagrams are illustrative, not engineering designs")):
    c.text(line, 0.5, y, 0.026, 0, color=MUTED)
c.text("Architecture Story Studio", 0.5, 0.28, 0.032, 0)
beat("C8", "B35", "framing", "SHOW_CONTEXT", ["Thank you very much for watching.", "The sources and photo credits are listed in the description."], strategy="CARD", graphic=c.spec(),
     visual_goal="Credits", required_concepts=[])


# ---------------------------------------------------------------- write
def main():
    narration = json.loads((HERE / "narration.template.json").read_text())
    narration["beats"] = [{"id": b["id"], "kind": b["kind"], "claim_ids": b["claims"], "sentences": b["sentences"]}
                          for b in BEATS]
    (HERE / "narration.json").write_text(json.dumps(narration, indent=2, ensure_ascii=False) + "\n")
    doc = {"schema": "narrative_beats/1", "project_id": "why-bridges-look-different",
           "title": "Why Bridges Don't All Look the Same", "status": "INTERNAL_REVIEW_DRAFT", "timing_mode": "AUDIO_LOCKED",
           "publication": {"restriction": "INTERNAL_ONLY",
                           "reason": "M7 claims are source-verified, not editorially approved; review cut only."},
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
    chapters = {"schema": "chapters/1", "project_id": "why-bridges-look-different",
                "chapters": [{"id": cid, "title": title, "purpose": purpose,
                              "beat_ids": [b["id"] for b in BEATS if b["chapter"] == cid]}
                             for cid, title, purpose in CHAPTERS]}
    (HERE / "chapters.json").write_text(json.dumps(chapters, indent=2, ensure_ascii=False) + "\n")
    words = sum(len(s.split()) for b in BEATS for s in b["sentences"])
    print(f"{len(CHAPTERS)} chapters, {len(BEATS)} beats, {sum(len(b['sentences']) for b in BEATS)} sentences, "
          f"{words} words")


if __name__ == "__main__":
    main()
