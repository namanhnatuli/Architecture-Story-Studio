"""Authoring source of "How Gothic Cathedrals Reached Impossible Heights".

    python3 projects/gothic-cathedral-heights/script/story.py

writes script/narration.json, script/visual_beats.json and script/chapters.json from the chapters
and beats below, so narration and visual beats always carry the same sentences. Every fact beat cites
claims from research/sources.json. Card coordinates: x, y in 0..1 of the frame (origin bottom-left);
nothing below y 0.2 (the subtitle zone ends at 0.17). The 3D beats use the cathedral family
(gothic_cathedral_section, romanesque_church_section; engine/arch/families/cathedral.py). Force graphics are
conceptual: arrows have one length.
"""
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import arch_statics as statics   # noqa: E402

ASPECT = 16 / 9
INK, MUTED, FAINT = "#24231F", "#55524A", "#8A867C"
STONE, WOOD, GLASS = "#B9A887", "#8C654D", "#5E86A6"
THRUST, ACCENT = "#C25110", "#1E5C96"
CHAR_W = 0.26   # text width per character in units of the text size (measured from card QA boxes)
# g-r5 (owner: real buildings need their own pictures): photographs and historic drawings; the rights record of each is
# in assets/manifest.json, the credit below is shown on screen and in the description
PHOTOS = {
    "IMG_BEAUVAIS_CHEVET": {"path": "assets/external/beauvais_chevet_rue_chambiges_2560.jpg", "size": (1706, 2560),
                            "credit": "Photo: Dguendel, CC BY 4.0, Wikimedia Commons"},
    "IMG_BEAUVAIS_CHOIR": {"path": "assets/external/beauvais_choir_interior_2560.jpg", "size": (1126, 2560),
                           "credit": "Photo: Dguendel, CC BY 4.0, Wikimedia Commons"},
    "IMG_BEAUVAIS_TRANSEPT": {"path": "assets/external/beauvais_basse_oeuvre_transept_1743.jpg", "size": (1743, 1409),
                              "credit": "Photo: Chris06, CC0, Wikimedia Commons"},
    "IMG_AMIENS_NAVE": {"path": "assets/external/amiens_nave_from_triforium_2560.jpg", "size": (1892, 2560),
                        "credit": "Photo: Eusebius, CC BY 3.0, Wikimedia Commons"},
    "DRW_VLD_BEAUVAIS_BUTTRESS": {"path": "assets/external/vld_beauvais_flying_buttress.png", "size": (630, 1021),
                                  "credit": "Drawing: Viollet-le-Duc, 1856 (public domain)"},
    "DRW_VLD_BEAUVAIS_PLAN": {"path": "assets/external/vld_beauvais_plan.png", "size": (609, 915),
                              "credit": "Plan: Viollet-le-Duc, 1856 (public domain)"},
    "DRW_VLD_AMIENS_PLAN": {"path": "assets/external/vld_amiens_plan.png", "size": (515, 1008),
                            "credit": "Plan: Viollet-le-Duc, 1854 (public domain)"},
}


def fitted(asset, box, crop=(0.0, 0.0, 1.0, 1.0)):
    """The image's box on the card (as engine/diagram.image_box) and a map from its pixels (x right, y down) to card
    coordinates, so marks land on the drawing."""
    w, h = PHOTOS[asset]["size"]
    u0, v0, u1, v1 = crop
    img = (w * (u1 - u0)) / (h * (v1 - v0))
    x0, y0, x1, y1 = box
    bw, bh = (x1 - x0) * ASPECT, y1 - y0
    fw, fh = (bw, bw / img) if img > bw / bh else (bh * img, bh)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    fb = [cx - fw / ASPECT / 2, cy - fh / 2, cx + fw / ASPECT / 2, cy + fh / 2]

    def at(px, py):
        u, v = px / w, 1 - py / h
        return [round(fb[0] + (u - u0) / (u1 - u0) * (fb[2] - fb[0]), 4), round(fb[1] + (v - v0) / (v1 - v0) * (fb[3] - fb[1]), 4)]
    return fb, at
DASH = [0.012, 0.008]   # dash and gap of a dashed card line, in units of the card height


class Card:
    def __init__(self, name):
        self.name, self.elements = name, []
        self.views, self.staging = [], False   # g-r5: the 2D camera on the picture (stage) and its views

    def add(self, kind, sentence=0, until=None, **kw):
        e = {"id": f"{self.name}_{len(self.elements):02d}", "kind": kind, "sentence": sentence, **kw}
        if until is not None:
            e["until"] = until
        if self.staging:
            e["stage"] = True
        self.elements.append(e)
        return self

    def stage(self, on=True):
        """Elements added while on move with the stage (pictures and the marks drawn on them); texts stay put."""
        self.staging = on
        return self

    def view(self, rect, sentence=0, word=None, move=1.5, delay=0.0):
        """The stage rectangle [x0, y0, x1, y1] (card units; equal sides fill the frame) the camera moves to at a
        moment of the narration; the first view holds from the start."""
        v = {"rect": [round(x, 4) for x in rect]}
        if self.views:
            v.update(sentence=sentence, move_seconds=move, **({"word": word} if word else {}), **({"delay": delay} if delay else {}))
        self.views.append(v)
        return rect

    def gone(self, sentence, word=None):
        """The last element leaves at that sentence (or at that word of it)."""
        self.elements[-1]["until"] = sentence
        if word:
            self.elements[-1]["until_word"] = word
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
            kw["dash"] = DASH
        return self.add("rect", sentence, until, **kw)

    def line(self, points, color=INK, width=0.005, sentence=0, dash=None, until=None, layer=0):
        kw = {"points": [[round(x, 4), round(y, 4)] for x, y in points], "color": color, "width": width, "layer": layer}
        if dash:
            kw["dash"] = DASH
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

    def image(self, asset, box, crop=(0.0, 0.0, 1.0, 1.0), sentence=0, drift=(0.0, 0.0), until=None, word=None):
        """g-r5: a photograph or historic drawing with its rights record in assets/manifest.json (PHOTOS). The first
        picture of a card is on screen from its first frame (g-r6: a card never opens on an empty frame)."""
        first = sentence == 0 and not word and not any(e["kind"] == "image" for e in self.elements)
        return self.add("image", sentence, until, asset=asset, path=PHOTOS[asset]["path"], box=[round(v, 4) for v in box],
                        crop=[round(v, 4) for v in crop], drift=list(drift), **({"word": word} if word else {}),
                        **({"from_start": True} if first else {}))

    def credit(self, asset, x=0.5, y=0.075, align="CENTER", sentence=0):
        """The on-screen credit of a photograph (CC BY: name, licence; the full record is in the description)."""
        return self.text(PHOTOS[asset]["credit"], x, y, 0.017, sentence, align=align, color=MUTED)

    def drawn(self, points, color=INK, width=0.005, sentence=0, word=None, seconds=0.6, dash=False, until=None, layer=2,
              delay=0.0):
        """g-r5 (owner: a path is drawn along its route, then holds): a polyline in short pieces that appear in order
        over `seconds` from its moment (+ delay); returns the time it takes, so a label can wait for it."""
        pts = [(float(x), float(y)) for x, y in points]
        total = sum(math.hypot((b[0] - a[0]) * ASPECT, b[1] - a[1]) for a, b in zip(pts, pts[1:])) or 1e-9
        n = max(2, min(24, int(total / 0.025)))
        cuts, acc, k = [total * i / n for i in range(n + 1)], 0.0, 1
        piece = [list(pts[0])]
        for a, b in zip(pts, pts[1:]):
            seg = math.hypot((b[0] - a[0]) * ASPECT, b[1] - a[1])
            while k <= n and cuts[k] <= acc + seg + 1e-12:
                t = (cuts[k] - acc) / seg if seg else 1.0
                q = [a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t]
                piece.append(q)
                self.line(piece, color, width, sentence, dash=dash, until=until, layer=layer)
                self.elements[-1]["delay"] = round(delay + seconds * (k - 1) / n, 3)
                if word:
                    self.elements[-1]["word"] = word
                piece = [q]
                k += 1
            if piece[-1] != list(b):
                piece.append(list(b))
            acc += seg
        return delay + seconds

    def drawn_arrow(self, points, color=INK, width=0.007, sentence=0, word=None, seconds=0.6, until=None, delay=0.0):
        """A drawn path whose head arrives last; the final shape is a plain arrow (never stretched or pulsing)."""
        (x0, y0), (x1, y1) = points[-2], points[-1]
        d = math.hypot((x1 - x0) * ASPECT, y1 - y0) or 1e-9
        head = min(0.04, d * 0.6)
        base = [x1 - (x1 - x0) / d * head, y1 - (y1 - y0) / d * head]
        end = self.drawn(list(points[:-1]) + [base], color, width * 0.8, sentence, word, seconds, until=until, delay=delay)
        self.arrow(base, [x1, y1], color, width, sentence, until=until)
        self.elements[-1]["delay"] = round(end, 3)
        if word:
            self.elements[-1]["word"] = word
        return end

    def later(self, seconds, word=None):
        """Delay the last element (its label waits for the drawing)."""
        self.elements[-1]["delay"] = round(seconds, 3)
        if word:
            self.elements[-1]["word"] = word
        return self

    def spec(self):
        return {"fade_seconds": 0.35, "elements": self.elements, **({"stage": {"views": self.views}} if self.views else {})}


def square(cx, cy, side):
    return [cx - side / 2, cy - side / 2, cx + side / 2, cy + side / 2]


def around(at, px0, py0, px1, py1, pad=1.2, dx=0.0, dy=0.0):
    """A frame-filling stage view around a region of a picture (pixels), with some room, optionally offset."""
    (x0, y1), (x1, y0) = at(px0, py0), at(px1, py1)
    return square((x0 + x1) / 2 + dx, (y0 + y1) / 2 + dy, max(x1 - x0, y1 - y0) * pad)


def on_screen(rect, p):
    """Where a card point appears on screen while the stage shows `rect` (for labels that stay put in a view)."""
    x0, y0, x1, y1 = rect
    k = 1.0 / max(x1 - x0, y1 - y0)
    return [round((p[0] - (x0 + x1) / 2) * k + 0.5, 4), round((p[1] - (y0 + y1) / 2) * k + 0.5, 4)]


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


def funicular(span, rise, center_share, n=32):
    """Shape of a string under a uniform load plus a load at mid-span (center_share = point load / uniform total):
    proportional to the bending moment of a simple beam with the same loads, scaled to the given rise."""
    def moment(x):
        return x * (span - x) / 2 + center_share * span * min(x, span - x) / 2
    peak = moment(span / 2)
    return [(-span / 2 + span * k / n, rise * moment(span * k / n) / peak) for k in range(n + 1)]


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

    def spoken(first, word, wait=0.0):
        for e in c.elements[first:]:
            if word:
                e["word"] = word
            if wait and "delay" not in e:
                e["delay"] = round(wait, 3)

    # g-r5 (owner: the timeline moves on to each date as it is told; a pause after each): the time line advances
    # (accent) to every event and band in the order they are spoken, then the date appears
    moments = sorted([(s, 0, year, "event", k) for k, (year, label, s, *w) in enumerate(events)] +
                     [(s, 1, y0, "band", k) for k, (y0, y1, label, color, s, ly, *w) in enumerate(bands)])
    reach, wait = X(start), {}
    for s, _, year, kind, k in moments:
        word = (events[k][3:4] if kind == "event" else bands[k][6:7]) or [None]
        if X(year) > reach + 1e-6:
            wait[(kind, k)] = c.drawn([[reach, 0.5], [X(year), 0.5]], ACCENT, 0.009, s, word[0],
                                      seconds=min(0.9, 0.25 + (X(year) - reach) * 2.0), layer=1)
            reach = X(year)
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
        spoken(first, word[0] if word else None, wait.get(("event", k), 0.0))
    for k, (y0, y1, label, color, s, ly, *word) in enumerate(bands):
        first = len(c.elements)
        c.rect([X(y0), 0.53, X(y1), 0.56], color, sentence=s)
        c.text(label, (X(y0) + X(y1)) / 2, ly, 0.024, s, plate=True)
        spoken(first, word[0] if word else None, wait.get(("band", k), 0.0))
    if extra:
        extra(c)
    return c


# ---------------------------------------------------------------- the film
CHAPTERS = [
    ("C1", "Hook", "The highest vaults of the Middle Ages came down; others still stand. Pose the central question."),
    ("C2", "Stone and its outward push", "Stone cannot be pulled apart; a vault pushes outward; one Romanesque answer, the barrel-vaulted church; Gothic rearranges the supports."),
    ("C3", "The pointed arch", "Taller over the same span, thrust depends on geometry and loads, the hanging chain, not a Gothic invention, level crowns over different widths."),
    ("C4", "The rib vault", "In the four-part vault shown, ribs direct the load toward four piers; how vaults stand is debated; the web works too; Durham's dates; the wall is no longer the main support."),
    ("C5", "The flying buttress", "The thrust is carried outside, over the aisle roof, down to a massive buttress."),
    ("C6", "Walls of light", "Why they did it: Saint-Denis, Chartres; was it a revolution or continuity?"),
    ("C7", "Building by geometry", "Rules from trial and error, ropes and squares, templates, centering, carpenters, little room for error."),
    ("C8", "The limit: Beauvais", "Raised beyond its proportions, the vaults fell in 1284; the repair, the tower of 1573; Amiens' iron chain."),
    ("C9", "Why they stand", "Stability rather than strength: the line of thrust under its assumptions, an arch on moving supports, what a scaled model does and does not show."),
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
# g-r6 (owner, g-r5 review: still slides): each picture fills the frame and the camera moves with a purpose (up the
# choir to the vault, out to the building); few words per scene; "today" on photographs while 1284 is told.
FULL = [0.0, 0.0, 1.0, 1.0]
CREDIT_TOP = 0.925   # credits sit at the top right, clear of the subtitles


def credit_top(c, asset, sentence=0, word=None):
    c.text(PHOTOS[asset]["credit"], 0.95, CREDIT_TOP, 0.016, sentence, align="RIGHT", color=MUTED, word=word)
    return c


def lower_left(c, lines, sentence, word=None, y=0.3, size=0.03, color=INK, until=None, until_word=None):
    """Short captions at the lower left, on plates, above the subtitles."""
    for k, t in enumerate(lines):
        c.text(t, 0.06, y - k * (1.85 * size + 0.006), size, sentence, align="LEFT", color=color, plate=True, word=word)   # plates 1.74 x size
        if until is not None:
            c.gone(until, until_word)
    return c


c = Card("B01")
_, at = fitted("IMG_BEAUVAIS_CHOIR", FULL)
c.stage()
c.image("IMG_BEAUVAIS_CHOIR", FULL, sentence=0, until=2)
c.elements[-1]["until_word"] = "choir"    # leaves once the exterior is in: a dissolve, never an empty frame
_, at2 = fitted("IMG_BEAUVAIS_CHEVET", FULL)
c.image("IMG_BEAUVAIS_CHEVET", FULL, sentence=2)
c.elements[-1]["layer"] = 1
c.stage(False)
w = at(1126, 0)[0] - at(0, 0)[0]                      # the photograph's width on the card
low = c.view(square(0.5, w / 2, w))                   # the lowest arcades
top = c.view(square(0.5, 1 - w / 2, w), 0, "november", move=5.2)   # a slow tilt up to the vault
c.view(around(at2, 0, 250, 1706, 1210, pad=1.0), 2, move=1.6)   # out to the choir from outside
c.view(around(at2, 150, 350, 1550, 1200, pad=1.0), 2, "eastern", move=3.0)
credit_top(c, "IMG_BEAUVAIS_CHOIR").gone(2)
credit_top(c, "IMG_BEAUVAIS_CHEVET", 2)
lower_left(c, ["Beauvais Cathedral today"], 0, size=0.026, color=MUTED, y=0.86, until=2)
lower_left(c, ["Beauvais, November 1284"], 0, "november", until=1)
lower_left(c, ["Vault: more than 45 m above the floor"], 1, "45", until=2)
lower_left(c, ["Published heights differ: 46 m to above 48 m"], 1, "45", y=0.25, size=0.02, color=MUTED, until=2)
lower_left(c, ["The choir today: the eastern arm", "In use from 1272: twelve years"], 2, "choir", size=0.028)
beat("C1", "B01", "fact", "INTRODUCE_ARCHITECTURE", [
    "In November 1284, in the French city of Beauvais, part of the highest stone vaults of the Middle Ages came down.",
    "They stood more than 45 meters above the floor.",
    "The choir beneath them, the eastern arm of the cathedral, had been in use for just twelve years."],
    ["CLM_103", "CLM_104", "CLM_106", "CLM_181", "CLM_182"], strategy="CARD", graphic=c.spec(),
    visual_goal="The real Beauvais filling the frame: the camera climbs the choir to its vault while 1284 is told, then "
                "pulls out to the choir seen from outside. The collapse is told, never shown",
    required_concepts=[])

c = Card("B02")
_, at = fitted("IMG_AMIENS_NAVE", FULL)
c.stage()
c.image("IMG_AMIENS_NAVE", FULL, sentence=0)
c.stage(False)
w = at(1892, 0)[0] - at(0, 0)[0]
c.view(square(0.5, w / 2 + 0.02, w))
c.view(square(0.5, 1 - w / 2, w), 1, "begun", move=4.5)   # up the nave to its vault and rose
credit_top(c, "IMG_AMIENS_NAVE")
lower_left(c, ["Amiens Cathedral today"], 0, "many", size=0.026, color=MUTED, y=0.86)
lower_left(c, ["Amiens, begun 1220", "Vault: more than 42 m"], 1, "1220")
beat("C1", "B02", "fact", "INTRODUCE_ARCHITECTURE", [
    "And yet many buildings like it are still standing.",
    "At Amiens, begun in 1220, the vault rises more than 42 meters, in a building that is tall, slender and filled with light."],
    ["CLM_110", "CLM_101", "CLM_102", "CLM_156"], strategy="CARD", graphic=c.spec(),
    visual_goal="Amiens by its own photograph, filling the frame: the camera rises through the nave to its vault",
    required_concepts=[])

# the title holds a few seconds only; the two questions are asked over Beauvais's own section (owner)
c = Card("B03")
_, at = fitted("DRW_VLD_BEAUVAIS_BUTTRESS", FULL)
c.stage()
c.image("DRW_VLD_BEAUVAIS_BUTTRESS", FULL, sentence=0)
c.stage(False)
c.view(FULL)
c.view(around(at, 0, 0, 630, 640, pad=1.0), 0, "relying", move=3.0)       # the section: geometry at work
vault = c.view(around(at, 330, 0, 630, 330, pad=1.15), 1, "how", move=1.6)   # the high vault and its height
flyers = c.view(around(at, 120, 120, 400, 400, pad=1.2), 2, "why", move=1.6)   # the flying buttresses
c.text("How Gothic Cathedrals Reached", 0.5, 0.63, 0.058, 0, plate=True).gone(0, "relying")
c.text("Impossible Heights", 0.5, 0.52, 0.058, 0, plate=True).gone(0, "relying")
c.text("How did they raise stone that high?", 0.5, 0.26, 0.04, 1, plate=True, word="how").gone(2)
c.text("And why, sometimes, did it come down?", 0.5, 0.26, 0.04, 2, plate=True, word="why")
c.text("Section of Beauvais: Viollet-le-Duc, 1856", 0.95, CREDIT_TOP, 0.016, 0, align="RIGHT", color=MUTED)
beat("C1", "B03", "fact", "SHOW_CONTEXT", [
    "The people who built them worked without modern structural calculations, relying on geometry, craft knowledge and experience.",
    "So how did they raise stone that high?",
    "And why, sometimes, did it come down?"],
    ["CLM_110"], strategy="CARD", graphic=c.spec(),
    visual_goal="A short title, then the two questions asked over Beauvais's section: its high vault, then its flying buttresses",
    required_concepts=[])

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
    "So a stone building stands largely by keeping its stones pressed together."],
    ["CLM_111"], strategy="CARD", graphic=c.spec(), visual_goal="An arch of wedge-shaped stones: pressed together, not pulled apart",
    required_concepts=[])
beat("C2", "B05", "fact", "EXPLAIN_LOAD_PATH", [
    "Now put a heavy stone vault on top of two walls.",
    "A vault does not simply press down: it also pushes outward, like a bow being bent.",
    "That outward push is called thrust, and a document from Amiens shows that builders there were well aware of it."],
    ["CLM_120", "CLM_121"], strategy="HOLD", visual_goal="Romanesque section: a barrel vault on two walls; conceptual outward arrows at the top of the walls (no magnitudes)",
    required_concepts=[ROMANESQUE, "barrel_vault"],
    annotations=[note("B05_note", "Illustrative model, arrows are conceptual", 1, position="BOTTOM_RIGHT"),
                 {"id": "B05_thrust", "type": "THRUST_ARROW", "target": "barrel_vault", "points": ["BOTTOM_LEFT", "BOTTOM_RIGHT"],
                  "text": "Thrust", "sentence": 1, "claim_id": "CLM_120"},
                 note("B05_word", "An Amiens document calls it “boutture”", 2)])
beat("C2", "B06", "fact", "EXPLAIN_STRUCTURE", [
    "Romanesque builders had several ways of covering a great church.",
    "In the barrel-vaulted type shown here, the heavy vault pushes outward along the whole length of the wall, so walls and supports are thick, stiffened by buttresses.",
    "Large openings would weaken the wall that holds the vault, so windows tend to stay small."],
    ["CLM_122"], strategy="HOLD_HIGHLIGHT", highlight_at_sentence=1, visual_goal="One barrel-vaulted example: thick walls and shallow buttresses highlighted; small windows. Not lit or framed as gloomy",
    required_concepts=[ROMANESQUE, "thick_wall", "shallow_buttress"],
    annotations=[note("B06_note", "One Romanesque type, illustrative model", 1, position="BOTTOM_RIGHT"),
                 {"id": "B06_vault", "type": "COMPONENT_LABEL", "target": "barrel_vault", "point": "TOP", "text": "Barrel vault", "sentence": 0},
                 {"id": "B06_wall", "type": "COMPONENT_LABEL", "target": {"concept": "thick_wall", "pick": "RIGHTMOST"}, "point": "CENTER",
                  "text": "Thick wall", "sentence": 1, "word": "walls"},
                 {"id": "B06_butt", "type": "COMPONENT_LABEL", "target": {"concept": "shallow_buttress", "pick": "RIGHTMOST"}, "point": "CENTER",
                  "text": "Shallow buttress", "sentence": 1, "word": "buttresses"},
                 {"id": "B06_window", "type": "COMPONENT_LABEL", "target": {"concept": "small_window", "pick": "RIGHTMOST"}, "point": "CENTER",
                  "text": "Small window", "sentence": 2, "word": "windows"}])

beat("C2", "B07", "fact", "SHOW_COMPONENT", [
    "Gothic builders rearranged that system of support.",
    "Instead of spreading the push along a thick wall, they directed it toward particular points, and carried it to supports outside.",
    "Three tools made that possible: the pointed arch, the rib vault, and the flying buttress."],
    ["CLM_123", "CLM_153"], strategy="HOLD_HIGHLIGHT", highlight_at_sentence=2,
    visual_goal="The Gothic section; the three tools named as they are spoken", required_concepts=[GOTHIC, "rib", "flying_buttress"],
    annotations=[note("B07_note", "Illustrative model", 0, position="BOTTOM_RIGHT"),
                 {"id": "B07_arch", "type": "COMPONENT_LABEL", "target": {"concept": "arcade_wall", "group": "arcade"}, "point": "CENTER",
                  "text": "Pointed arch", "sentence": 2, "word": "pointed"},
                 {"id": "B07_rib", "type": "COMPONENT_LABEL", "target": {"concept": "rib", "group": "rib_transverse_0"}, "point": "TOP",
                  "text": "Rib vault", "sentence": 2, "word": "rib"},
                 {"id": "B07_flyer", "type": "COMPONENT_LABEL", "target": {"concept": "flying_buttress", "group": "frame_east0"}, "point": "CENTER",
                  "text": "Flying buttress", "sentence": 2, "word": "flying"}])

# C3 -------------------------------------------------------------------------------------------
c = Card("B08")
c.tag("3 · The pointed arch")
Y8 = 0.4
c.line(place(round_arch(0.36), 0.3, Y8), STONE, 0.014, 0)
c.line(place(pointed_arch(0.36, 0.42), 0.7, Y8), ACCENT, 0.014, 0)
c.text("Round arch", 0.3, 0.87, 0.034, 1, plate=True)
c.text("Pointed arch", 0.7, 0.87, 0.034, 0, plate=True)
c.text("Rise: half the span", 0.3, Y8 + 0.07, 0.024, 1, color=MUTED)
c.text("Same span, higher rise", 0.7, Y8 + 0.07, 0.024, 1, color=ACCENT)
c.arrow([0.3 - 0.18 / ASPECT, Y8], [0.3 - 0.18 / ASPECT - 0.07, Y8 - 0.03], THRUST, 0.008, 1)
c.arrow([0.3 + 0.18 / ASPECT, Y8], [0.3 + 0.18 / ASPECT + 0.07, Y8 - 0.03], THRUST, 0.008, 1)
c.arrow([0.7 - 0.18 / ASPECT, Y8], [0.7 - 0.18 / ASPECT - 0.025, Y8 - 0.07], THRUST, 0.008, 1)
c.arrow([0.7 + 0.18 / ASPECT, Y8], [0.7 + 0.18 / ASPECT + 0.025, Y8 - 0.07], THRUST, 0.008, 1)
c.text("Conceptual arrows: direction only, not calculated", 0.5, 0.3, 0.021, 1, color=MUTED)
c.text("Illustrations, not the arches of the study (Block, DeJong and Ochsendorf, 2006)", 0.5, 0.25, 0.022, 3, color=MUTED)
beat("C3", "B08", "fact", "COMPARE_VARIANTS", [
    "A pointed arch is two arcs of a circle that meet at a point.",
    "Over the same span, it can rise higher than a round arch, and a taller arch can push less to the sides.",
    "How much less depends on its exact shape, its thickness and the weight it carries.",
    "One comparison by MIT engineers, of two other arches, did find that the pointed one pushed less, but that result belongs to those two arches, not to every arch."],
    ["CLM_130", "CLM_134"], strategy="CARD", graphic=c.spec(), visual_goal="Round and pointed arch on the same span; the higher rise. No thrust figures: these are not the arches of the study",
    required_concepts=[])

c = Card("B09")
AY, CY = 0.72, 0.38    # the chain's anchors; the feet of the inverted curve
c.text("Robert Hooke, 1675", 0.5, 0.66, 0.05, 0, until=2)
c.text("“As hangs the flexible line, so but inverted", 0.5, 0.52, 0.042, 1, until=2)
c.text("will stand the rigid arch.”", 0.5, 0.45, 0.042, 1, until=2)
c.line([[0.1, AY], [0.44, AY]], FAINT, 0.004, 2)
chain = place(catenary(0.46, 0.34), 0.27, AY, flip=True)
c.line(chain, INK, 0.008, 2)
c.circle([0.27 - 0.23 / ASPECT, AY], 0.011, INK, 2)
c.circle([0.27 + 0.23 / ASPECT, AY], 0.011, INK, 2)
for k in range(4, len(chain) - 1, 4):
    c.circle(chain[k], 0.009, MUTED, 2)
c.text("A chain with its weights", 0.27, 0.3, 0.03, 2, plate=True)
c.line(place(catenary(0.46, 0.34), 0.73, CY), INK, 0.008, 3, dash=True)
c.text("Turned upside down: a path for the force", 0.73, 0.3, 0.03, 3, plate=True)
c.line(place(funicular(0.46, 0.34, 1.2), 0.27, AY, flip=True), ACCENT, 0.006, 4)
c.line(place(funicular(0.46, 0.34, 1.2), 0.73, CY), ACCENT, 0.006, 4, dash=True)
c.text("Different weights, different curve", 0.5, 0.77, 0.028, 4, plate=True, color=ACCENT)
c.text("“As hangs the flexible line, so but inverted", 0.5, 0.88, 0.032, 2)
c.text("will stand the rigid arch.”  Robert Hooke, 1675", 0.5, 0.83, 0.032, 2)
c.text("Conceptual diagram", 0.5, 0.235, 0.021, 2, color=MUTED)
beat("C3", "B09", "fact", "EXPLAIN_STRUCTURE", [
    "In 1675, the scientist Robert Hooke summed up an idea about arches in one line.",
    "As hangs the flexible line, so but inverted will stand the rigid arch.",
    "Hang a chain with a set of weights, and it takes a shape.",
    "Turn that shape upside down, and it shows a path the force can follow through an arch carrying the same weights.",
    "Change the weights, and the shape changes too."],
    ["CLM_114", "CLM_115"], strategy="CARD", graphic=c.spec(), visual_goal="Hanging chain with weights, inverted; different weights give a different curve", required_concepts=[])

EARLY = dict(start=1060, end=1160, ticks=(1060, 1080, 1100, 1120, 1140, 1160))
c = timeline("B10", [(1088, "Cluny III: construction begins", 1, "cluny")],
             [(1130, 1144, "Saint-Denis: used systematically", "#5E86A6", 2, 0.64)], extra=lambda c: (
                 c.line(place(pointed_arch(0.12, 0.14), 0.5, 0.6), ACCENT, 0.008, 0),
                 c.text("Not a Gothic invention", 0.5, 0.82, 0.036, 0, plate=True)), **EARLY)
beat("C3", "B10", "fact", "SHOW_CONTEXT", [
    "The pointed arch was not a Gothic invention.",
    "It already appears in Burgundy, at the great abbey church of Cluny, whose construction began around 1088, and Columbia University's Amiens project traces it to Islamic sources.",
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
c.text("Regular crowns help keep complex vaults regular", 0.5, 0.275, 0.028, 2, plate=True)
c.text("Wide bay, narrow bay: conceptual diagram", 0.5, 0.225, 0.021, 1, color=MUTED)
beat("C3", "B11", "fact", "COMPARE_VARIANTS", [
    "It had a subtler advantage too.",
    "Unlike a round arch, a pointed arch can span sections of different widths, called bays, and still reach the same height at its crown.",
    "That was a valuable asset for keeping complex vaults regular."],
    ["CLM_132"], strategy="CARD", graphic=c.spec(), visual_goal="Level crowns over different widths", required_concepts=[])

# C4 -------------------------------------------------------------------------------------------
# The pilot (g-r4): rib vault and flying buttress as SEQUENCE shots. One bay is taken out of the model; its parts arrive
# and light in the order the narration names them; the camera eases from the whole section to that bay.
def part(concept, local):
    return {"concept": concept, "local": local}


BAY_PIERS = [{"concept": "nave_pier", "group": g} for g in ("frame_west0", "frame_east0", "frame_west1", "frame_east1")]
BAY_ARCHES = [{"concept": "rib", "group": g} for g in ("rib_transverse_0", "rib_transverse_1")]
BAY_DIAGONALS = [part("rib", "rib_diagonal_b1a"), part("rib", "rib_diagonal_b1b")]
COURSES = [f"vault_web_b1_{panel}{k}" for k in range(5, 0, -1) for panel in "fbwe"]   # from the arches and walls inwards
BAY_WEB = [part("vault_web", COURSES)]
STRIPES = [part("vault_web", [c for c in COURSES if int(c[-1]) % 2])]                # every other course
BAY = BAY_PIERS + BAY_ARCHES + BAY_DIAGONALS + BAY_WEB
BAY_VAULT = BAY_ARCHES + BAY_DIAGONALS + BAY_WEB
OUTSIDE = ["flying_buttress", "pier_buttress", "pinnacle", "high_roof", "aisle_roof"]   # nothing a worm's-eye view needs
# g-r5 (owner: fewer see-through layers): only the bay's own high walls stay, faded, to place it; the rest leaves
BAY_WALLS = [part("arcade_wall", ["clerestory_wall_b1_west", "clerestory_wall_b1_east"]),
             part("clerestory_window", ["clerestory_window_b1_west", "clerestory_window_b1_east"])]
REST_OF_CHURCH = {"except": BAY + BAY_WALLS + OUTSIDE}   # the church floor included: the camera goes under it
# the establishing view: the row of high vaults and the top of the piers (the pier feet stay below the frame, since the
# floor is hidden for a camera under it: owner, g-r4 pilot review)
UNDER_BAY = {"azimuth": -90.0, "elevation": -84.0}
FLOOR = {"concept": "church_floor"}
AROUND_BAY = {"except": BAY + BAY_WALLS + OUTSIDE + [FLOOR]}   # the church around the bay, kept faded while the camera turns   # straight up under the bay: the X of the ribs, a pier at each corner
WAS_THERE = {"why": "B12 ends this way: the cut from it is invisible"}


def glow(targets, at, until, **kw):
    """g-r5 (owner: more contrast on the part being explained): a stronger glow, leaning to the accent colour."""
    return {"do": "HIGHLIGHT", "targets": targets, "at": at, "until": until, "strength": 1.0, "tint": 0.8, **kw}


beat("C4", "B12", "fact", "SHOW_COMPONENT", [
    "The second tool is the rib vault.",
    "In the four-part vault shown here, two ribs cross diagonally over each bay of the building.",
    "In this simplified picture, they direct the vault's load toward four points: the piers, or stone pillars, at its corners."],
    ["CLM_140"], strategy="SEQUENCE",
    visual_goal="The church on its floor; one bay is marked, the rest fades but stays while the camera turns under the "
                "bay; then the bay stands alone: its piers, the two diagonal ribs one after the other, the stone web; "
                "the light runs along the ribs to the four piers",
    required_concepts=[GOTHIC, "rib", "vault_web", "nave_pier"],
    sequence={"camera": "CATHEDRAL_VAULT_BELOW",
              # g-r5: the church as in every other shot, standing on its floor; the rest leaves and one bay stands
              # alone; then (nothing else moving) the camera turns under it and looks straight up
              "views": [{"azimuth": -66.0, "elevation": 12.0},
                        {"frame": BAY, **UNDER_BAY, "margin": 0.08, "at": {"sentence": 0, "end": True, "offset": 0.3},
                         "move_seconds": 2.6}],
              "steps": [glow(BAY, {"sentence": 0, "word": "second"}, {"sentence": 0, "word": "vault", "offset": 0.2}),
                        # owner (g-r5): the chosen bay is marked before the rest goes, and stays placed in its church
                        # while the camera turns; only then is it set apart
                        {"do": "GHOST", "targets": AROUND_BAY, "at": {"sentence": 0, "word": "vault", "offset": 0.2},
                         "seconds": 1.0, "transparency": 0.88},
                        {"do": "FADE_OUT", "targets": [FLOOR], "at": {"sentence": 0, "word": "vault", "offset": 0.2},
                         "seconds": 1.0, "why": "the camera passes under it"},
                        {"do": "GHOST", "targets": BAY_WALLS, "at": {"sentence": 0, "word": "vault", "offset": 0.2},
                         "seconds": 1.0, "transparency": 0.9},
                        {"do": "FADE_OUT", "targets": OUTSIDE + BAY_DIAGONALS + BAY_WEB, "at": {"sentence": 0, "word": "vault",
                                                                                               "offset": 0.2}, "seconds": 1.0},
                        {"do": "FADE_OUT", "targets": AROUND_BAY, "at": {"sentence": 1, "word": "here", "offset": 0.45},
                         "seconds": 0.5},
                        {"do": "REVEAL", "targets": BAY_DIAGONALS[:1], "at": {"sentence": 1, "word": "two", "offset": 0.3},
                         "seconds": 1.0, "direction": "FROM_BELOW", "distance": 4.0, "sound": "STONE"},
                        {"do": "REVEAL", "targets": BAY_DIAGONALS[1:], "at": {"sentence": 1, "word": "cross", "offset": 0.1},
                         "seconds": 1.0, "direction": "FROM_BELOW", "distance": 4.0, "sound": "STONE"},
                        glow(BAY_DIAGONALS, {"sentence": 1, "word": "over"}, {"sentence": 2, "offset": -0.2}),
                        {"do": "REVEAL", "targets": BAY_WEB, "at": {"sentence": 2, "offset": -0.1}, "seconds": 0.7,
                         "stagger_seconds": 0.04, "direction": "FROM_BELOW", "distance": 1.5},
                        # the ribs, not the web, light while they "direct the load": the two lit together wash out
                        glow(BAY_DIAGONALS, {"sentence": 2, "word": "they", "offset": -0.2}, {"sentence": 2, "word": "piers"}),
                        glow(BAY_PIERS, {"sentence": 2, "word": "points", "offset": -0.2}, {"sentence": 2, "end": True, "offset": 0.3})]},
    annotations=[note("B12_ch", "4 · The rib vault", 0, 2),
                 note("B12_note", "Illustrative model, one type: a four-part vault", 1, position="BOTTOM_RIGHT"),
                 {"id": "B12_rib", "type": "COMPONENT_LABEL", "target": part("rib", ["rib_diagonal_b1a", "rib_diagonal_b1b"]),
                  "point": "TOP", "text": "Diagonal ribs", "sentence": 1, "word": "diagonally", "until": 2},   # the crossing
                 {"id": "B12_pier", "type": "COMPONENT_LABEL", "target": BAY_PIERS[1], "point": "TOP",
                  "text": "Pier", "sentence": 2, "word": "piers"}])
beat("C4", "B13", "fact", "SHOW_COMPONENT", [
    "How exactly these vaults stand has been debated for centuries.",
    "Engineers following Jacques Heyman assume that the main ribs bring the forces down, and treat the stone between them as a series of parallel arches.",
    "So even in that reading, the stone between the ribs carries load."],
    ["CLM_141"], strategy="SEQUENCE",
    visual_goal="Closer on the bay's vault: the ribs light, then every other course of the web (the parallel arches of "
                "Heyman's reading), then the whole web: it reads as working stone, never as infill",
    required_concepts=[GOTHIC, "rib", "vault_web"],
    sequence={"camera": "CATHEDRAL_VAULT_BELOW",
              # while the debate is named, the camera moves in on the vault surface it is about
              "views": [{"frame": BAY, **UNDER_BAY, "margin": 0.08},
                        {"frame": BAY_WEB, **UNDER_BAY, "margin": 0.04, "at": {"sentence": 0, "word": "stand"},
                         "move_seconds": 4.5}],
              "steps": [{"do": "GHOST", "targets": BAY_WALLS, "at": 0, "seconds": 0, "transparency": 0.9, **WAS_THERE},
                        {"do": "FADE_OUT", "targets": REST_OF_CHURCH, "at": 0, "seconds": 0, **WAS_THERE},
                        {"do": "FADE_OUT", "targets": OUTSIDE, "at": 0, "seconds": 0, **WAS_THERE},
                        glow(BAY_DIAGONALS + BAY_ARCHES, {"sentence": 1, "word": "ribs", "offset": -0.2},
                             {"sentence": 1, "word": "treat"}),
                        glow(STRIPES, {"sentence": 1, "word": "parallel", "offset": -0.3}, {"sentence": 2, "offset": -0.1}),
                        glow(BAY_WEB, {"sentence": 2, "word": "stone", "offset": -0.2}, {"sentence": 2, "end": True, "offset": 0.4})]},
    annotations=[note("B13_note", "Illustrative model of one analysis, still debated", 0),
                 {"id": "B13_ribs", "type": "COMPONENT_LABEL", "target": BAY_DIAGONALS[1], "point": "CENTER",
                  "text": "Main ribs", "sentence": 1, "word": "ribs", "until": 2},
                 {"id": "B13_arches", "type": "COMPONENT_LABEL", "target": {**STRIPES[0], "pick": "CENTERMOST"}, "point": "CENTER",
                  "text": "A series of arches", "sentence": 1, "word": "parallel", "until": 2},
                 {"id": "B13_web", "type": "COMPONENT_LABEL", "target": {**BAY_WEB[0], "pick": "CENTERMOST"}, "point": "CENTER",
                  "text": "Stone web", "sentence": 2, "word": "stone"}])
c = timeline("B14", [(1088, "Cluny III: construction begins", 0)],
             [(1093, 1133, "Durham, begun 1093, finished 1133: ribbed vaults, in phases", STONE, 1, 0.72, "durham"),
              (1140, 1144, "Saint-Denis choir", "#5E86A6", 0, 0.64)], extra=lambda c: (
                 c.text("At least three technical phases, some forty years", 0.5, 0.34, 0.028, 2, plate=True),
                 c.text("Earlier sources: Islamic, Roman, Byzantine (Columbia)", 0.5, 0.26, 0.028, 3, plate=True)), **EARLY)
beat("C4", "B14", "fact", "SHOW_CONTEXT", [
    "Ribs were not new either.",
    "Durham Cathedral in England, begun in 1093, was completely covered by ribbed vaults by the time it was finished in 1133.",
    "Its masons refined them in phases over some forty years.",
    "Columbia's project traces ribs to Islamic, Roman and Byzantine sources."],
    ["CLM_142"], strategy="CARD", graphic=c.spec(), visual_goal="The same timeline, with Durham's building years as a band, not one date", required_concepts=[])
beat("C4", "B15", "fact", "EXPLAIN_DESIGN_CHANGE", [
    "This kind of vault changes the job of the wall.",
    "With the vault's load directed toward the piers, the wall between them was no longer its main support.",
    "It could be thinned, and opened up with wide windows."],
    ["CLM_143"], strategy="HOLD_HIGHLIGHT", highlight_at_sentence=2, camera_move={"type": "PUSH_IN", "amount": 0.1}, visual_goal="The wall between two piers opens into a tall window",
    required_concepts=[GOTHIC, "nave_pier", "clerestory_window"])

# C5 -------------------------------------------------------------------------------------------
# The east flying buttress at the cut, and what it stands on; the rest of the system waits, faded, until B17 names it.
EAST = "frame_east0"
FLYER, PIER_BUTTRESS, PINNACLE = ({"concept": c, "group": EAST} for c in ("flying_buttress", "pier_buttress", "pinnacle"))
# g-r5 (owner: fewer see-through layers): only the system at the cut face waits, faded; the bays behind lose theirs,
# whose stacked ghosts read as smudges in a near-square view
SYSTEM = [{"concept": c, "group": g} for c in ("flying_buttress", "pier_buttress") for g in ("frame_west0", EAST)]
SYSTEM_BEHIND = [{"concept": c, "group": f"frame_{side}{k}"} for c in ("flying_buttress", "pier_buttress", "pinnacle")
                 for side in ("west", "east") for k in (1, 2, 3)]
AISLE_ROOF = part("aisle_roof", "aisle_roof_east")
# The section is taller than it is wide, so a frame on the whole east side is hardly closer than the full view; the
# close-up keeps the upper part: high window, flyer, pinnacle, aisle roof (the pier buttress runs down out of frame).
# g-r5: and the springing of the high vault, where the thrust "leaves the vault" (the frame was a third empty)
EAST_SIDE = [{"concept": "rib", "group": "rib_transverse_0"}, part("clerestory_window", "clerestory_window_b1_east"),
             FLYER, PINNACLE, AISLE_ROOF]
HIGH_PIERS = [{"concept": "nave_pier", "group": g} for g in ("frame_west0", EAST)]
SET_ASIDE = [{"do": "GHOST", "targets": SYSTEM, "at": 0, "seconds": 0, "transparency": 0.8,
              "why": "the supports outside wait, faded, until B17 names them"},
             {"do": "FADE_OUT", "targets": [{"concept": "pinnacle", "group": g} for g in ("frame_west0", EAST)],
              "at": 0, "seconds": 0},
             {"do": "FADE_OUT", "targets": SYSTEM_BEHIND, "at": 0, "seconds": 0}]

beat("C5", "B16", "fact", "EXPLAIN_LOAD_PATH", [
    "But gathering the thrust does not make it go away.",
    "Even reduced, that sideways push remains a threat to the stability of the whole building.",
    "It still has to be contained somewhere."],
    ["CLM_150"], strategy="SEQUENCE",
    visual_goal="The cut face of the church, square on: an outward arrow at each springing of the high vault, the high "
                "piers it pushes on, and the supports outside still faded; then the camera turns to the east side",
    required_concepts=[GOTHIC, "nave_pier"],
    sequence={"camera": "CATHEDRAL_TRANSVERSE",
              "views": [{"frame": None}, {"frame": EAST_SIDE, "at": {"sentence": 2, "offset": -0.2}, "move_seconds": 2.4}],
              "steps": SET_ASIDE + [glow(HIGH_PIERS, {"sentence": 1, "word": "threat", "offset": -0.2},
                                         {"sentence": 2, "offset": -0.3})]},
    annotations=[note("B16_ch", "5 · The flying buttress", 0, 2),
                 note("B16_note", "Illustrative model", 0, position="BOTTOM_RIGHT"),   # the force tag says "not to scale"
                 {"id": "B16_thrust", "type": "THRUST_ARROW", "target": {"concept": "rib", "group": "rib_transverse_0"},
                  "points": ["BOTTOM_LEFT", "BOTTOM_RIGHT"], "text": "Thrust", "sentence": 0, "word": "thrust",
                  "until": 2, "claim_id": "CLM_150"}])
beat("C5", "B17", "fact", "EXPLAIN_LOAD_PATH", [
    "The answer stands outside the building: the flying buttress.",
    "It is a stone arch that picks up the thrust where it leaves the vault, carries it across the aisle roof, and brings it down to a massive pier buttress.",
    "Often a pinnacle on top adds weight, to help stabilize the thrust."],
    ["CLM_151", "CLM_152"], strategy="SEQUENCE",
    visual_goal="One flying buttress in profile: it returns in full when named, the path follows the narration from the "
                "vault over the aisle roof down the pier buttress, and the pinnacle is set on top when it is named",
    required_concepts=[GOTHIC, "flying_buttress", "pier_buttress", "pinnacle", "aisle_roof"],
    sequence={"camera": "CATHEDRAL_TRANSVERSE",
              "views": [{"frame": EAST_SIDE}],
              "steps": SET_ASIDE + [
                  # g-r5 (owner): the pier buttress is solid before the flyer arrives, so the flyer never floats
                  {"do": "UNGHOST", "targets": [PIER_BUTTRESS], "at": {"sentence": 0, "word": "outside", "offset": -0.2},
                   "seconds": 0.8},
                  {"do": "UNGHOST", "targets": [FLYER], "at": {"sentence": 0, "word": "flying", "offset": -0.3}, "seconds": 0.8},
                  glow([FLYER], {"sentence": 0, "word": "flying"}, {"sentence": 1, "word": "picks"}),
                  glow([AISLE_ROOF], {"sentence": 1, "word": "across"},
                       {"sentence": 1, "word": "brings"}),
                  glow([PIER_BUTTRESS], {"sentence": 1, "word": "massive", "offset": -0.2}, {"sentence": 2, "offset": -0.2}),
                  {"do": "REVEAL", "targets": [PINNACLE], "at": {"sentence": 2, "word": "pinnacle", "offset": -0.5},
                   "seconds": 1.1, "direction": "FROM_ABOVE", "distance": 5.0, "sound": "STONE_HEAVY"},
                  glow([PINNACLE], {"sentence": 2, "word": "weight", "offset": -0.2}, {"sentence": 2, "end": True, "offset": 0.4})]},
    annotations=[note("B17_note", "Illustrative model", 0, position="BOTTOM_RIGHT"),
                 {"id": "B17_flyer", "type": "COMPONENT_LABEL", "target": FLYER, "point": "CENTER",
                  "text": "Flying buttress", "sentence": 0, "word": "flying", "until": 2},
                 {"id": "B17_path1", "type": "CONCEPTUAL_LOAD_PATH", "style": "LOAD", "sentence": 1, "word": "picks",
                  "claim_id": "CLM_152", "until": 2,
                  "path": [[{"target": {"concept": "rib", "group": "rib_transverse_0"}, "point": "BOTTOM_RIGHT"},
                            {"target": FLYER, "point": "TOP_LEFT"}]]},
                 {"id": "B17_path2", "type": "CONCEPTUAL_LOAD_PATH", "style": "LOAD", "sentence": 1, "word": "across",
                  "claim_id": "CLM_152", "until": 2,
                  "path": [[{"target": FLYER, "point": "TOP_LEFT"}, {"target": FLYER, "point": "CENTER"},
                            {"target": PIER_BUTTRESS, "point": "TOP"}]]},
                 {"id": "B17_path3", "type": "CONCEPTUAL_LOAD_PATH", "style": "LOAD", "sentence": 1, "word": "down",
                  "claim_id": "CLM_152", "until": 2,
                  "path": [[{"target": PIER_BUTTRESS, "point": "TOP"}, {"target": PIER_BUTTRESS, "point": "BOTTOM"}]]},
                 {"id": "B17_pier", "type": "COMPONENT_LABEL", "target": PIER_BUTTRESS, "point": "CENTER",
                  "text": "Pier buttress", "sentence": 1, "word": "massive"},
                 {"id": "B17_weight", "type": "LOAD_ARROW", "target": PINNACLE, "text": "Weight", "sentence": 2,
                  "word": "weight", "claim_id": "CLM_152"},
                 {"id": "B17_pinnacle", "type": "COMPONENT_LABEL", "target": PINNACLE, "point": "TOP",
                  "text": "Pinnacle", "sentence": 2, "word": "pinnacle"}])
beat("C5", "B18", "fact", "EXPLAIN_DESIGN_CHANGE", [
    "One way to picture it comes from Columbia's Amiens project.",
    "It is as if the thick outer wall had been cut into segments, and each segment turned 90 degrees.",
    "Those segments become rigid supports, standing out from the building, with exposed arches reaching up to the high vaults."],
    ["CLM_153"], strategy="SEQUENTIAL_STATES", visual_goal="Romanesque thick wall, lit; then Gothic pier buttresses, lit; same camera and scale",
    required_concepts=[ROMANESQUE, GOTHIC], state_targets={ROMANESQUE: ["thick_wall"], GOTHIC: ["pier_buttress"]}, same_scale=True,
    annotations=[note("B18_note", "Illustrative models, not measured buildings", 0, position="BOTTOM_RIGHT")])
beat("C5", "B19", "fact", "INTRODUCE_ARCHITECTURE", [
    "According to France's national library, the first flying buttresses were used to consolidate Romanesque churches that threatened to collapse.",
    "It also says that the slanting timber props used while building the vaults were, in effect, made permanent in stone.",
    "At Chartres, flying buttresses were part of the original plans.",
    "And around the east end of Notre-Dame in Paris, they look almost like a giant external skeleton."],
    ["CLM_154", "CLM_155"], strategy="HOLD_HIGHLIGHT", camera_move={"type": "PUSH_IN", "amount": 0.1},
    visual_goal="Flyers on the model; rights-cleared photographs of Chartres and Notre-Dame replace it where available",
    required_concepts=[GOTHIC, "flying_buttress"],
    annotations=[note("B19_note", "Illustrative model, not Chartres or Notre-Dame", 0, position="BOTTOM_RIGHT")])
beat("C5", "B20", "fact", "INTRODUCE_ARCHITECTURE", [
    "Flying buttresses even help carry rainwater off the roof.",
    "But above all, builders learned how to exploit them, and cathedrals grew ever taller."],
    ["CLM_156", "CLM_157"], strategy="HOLD_HIGHLIGHT", highlight_at_sentence=1, visual_goal="The full exterior of the section, the nearest flyers highlighted",
    required_concepts=[GOTHIC, {"concept": "flying_buttress", "group": "frame_east0"}, {"concept": "flying_buttress", "group": "frame_west0"}])

# C6 -------------------------------------------------------------------------------------------
c = timeline("B21", [(1144, "Choir dedicated", 2, "choir")],
             [(1130, 1140, "West front", STONE, 2, 0.36), (1140, 1144, "New choir", "#5E86A6", 2, 0.28)],
             start=1120, end=1160, ticks=(1120, 1130, 1140, 1150, 1160), extra=lambda c: (
                 c.tag("6 · Walls of light"),
                 c.text("Part of the answer: light", 0.5, 0.74, 0.05, 1, until=2),
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
c.text("Bibliothèque nationale de France", 0.5, 0.33, 0.022, 1, color=MUTED)
beat("C6", "B22", "fact", "SHOW_CONTEXT", [
    "For Suger, light was a sign, a bridge to the divine.",
    "France's national library says the new style had to let in as much light as possible."],
    ["CLM_161", "CLM_164"], strategy="CARD", graphic=c.spec(), visual_goal="Why light mattered", required_concepts=[])

beat("C6", "B23", "fact", "SHOW_COMPONENT", [
    "At Chartres, some 2,500 square meters of stained glass survive, most of it original."],
    ["CLM_162"], strategy="HOLD_HIGHLIGHT", visual_goal="The tall windows on the model, lit; the number on screen (a rights-cleared photograph of the glass may replace the model)",
    required_concepts=[GOTHIC, "clerestory_window"],
    annotations=[note("B23_n", "Chartres: about 2,500 m² of stained glass", 0),
                 note("B23_note", "Illustrative model, not Chartres Cathedral", 0, position="BOTTOM_RIGHT")])

c = Card("B24")
c.text("How new was Gothic?", 0.5, 0.84, 0.046, 0)
c.line([[0.5, 0.3], [0.5, 0.76]], FAINT, 0.003, 1)
c.text("“An entire revolution", 0.27, 0.66, 0.036, 1, word="revolution")
c.text("in the art of building”", 0.27, 0.6, 0.036, 1, word="revolution")
c.text("After Viollet-le-Duc, 19th century", 0.27, 0.52, 0.025, 1, color=MUTED, word="revolution")
c.text("No Gothic break: a creative", 0.73, 0.66, 0.036, 1, word="others")
c.text("proposal rooted in continuity", 0.73, 0.6, 0.036, 1, word="others")
c.text("Arnaud Timbert, art historian", 0.73, 0.52, 0.025, 1, color=MUTED, word="others")
c.text("Suger's crypt: round arches, groin vaults", 0.73, 0.38, 0.026, 2, plate=True)
beat("C6", "B24", "fact", "COMPARE_VARIANTS", [
    "How new was all of this?",
    "Some historians call Gothic a revolution in the art of building, while others see a creative step rooted in continuity.",
    "Suger's own crypt still relies almost entirely on round arches and groin vaults."],
    ["CLM_163"], strategy="CARD", graphic=c.spec(), visual_goal="Two readings, side by side; the names stay in small type on the card and are not spoken", required_concepts=[])

# C7 -------------------------------------------------------------------------------------------
c = Card("B25")
c.tag("7 · Building by geometry")
c.line(place(pointed_arch(0.16, 0.16), 0.24, 0.32), STONE, 0.01, 0)
c.line(place(pointed_arch(0.26, 0.26), 0.44, 0.32), STONE, 0.012, 1)
c.line(place(pointed_arch(0.42, 0.42), 0.7, 0.32), STONE, 0.016, 2)
c.text("Trial and error, over centuries", 0.5, 0.86, 0.036, 1, plate=True)
c.text("The same proportions, scaled up", 0.5, 0.25, 0.03, 2, plate=True)
beat("C7", "B25", "fact", "EXPLAIN_STRUCTURE", [
    "So how did they do all this, without modern structural calculations?",
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
# g-r5/g-r6 (owner): the real buildings by their own pictures, filling the frame. Each document is first seen whole,
# then the camera moves in on the area the narration names, then out again (before and after). Viollet-le-Duc's own
# plan and section of Beauvais (1856) carry the marks; every mark is schematic and says so; no collapse is shown.
_, AT_PLAN = fitted("DRW_VLD_BEAUVAIS_PLAN", FULL)
CHOIR_VIEW = around(AT_PLAN, 90, 0, 540, 480, pad=1.05)        # choir and transept
STRAIGHT = around(AT_PLAN, 235, 150, 380, 340, pad=1.3)        # the three straight bays of the choir


def mark_box(c, at, px0, py0, px1, py1, sentence, word=None, color=THRUST, until=None, delay=0.0, dash=True, width=0.004):
    """A drawn outline around a region of a picture (pixels), in order around it."""
    (x0, y1), (x1, y0) = at(px0, py0), at(px1, py1)
    return c.drawn([[x0, y0], [x1, y0], [x1, y1], [x0, y1], [x0, y0]], color, width, sentence, word, seconds=0.8,
                   dash=dash, until=until, delay=delay)


def top_left(c, lines, sentence, word=None, size=0.03, color=INK, until=None, until_word=None, delay=0.0):
    for k, t in enumerate(lines):
        c.text(t, 0.06, 0.86 - k * (1.85 * size + 0.006), size, sentence, align="LEFT", color=color, plate=True, word=word)
        if delay:
            c.later(delay, word)
        if until is not None:
            c.gone(until, until_word)
    return c


c = Card("B31")
_, at = fitted("IMG_BEAUVAIS_CHEVET", FULL)
c.stage()
c.image("IMG_BEAUVAIS_CHEVET", FULL, sentence=0)
c.stage(False)
c.view(around(at, 0, 250, 1706, 1210, pad=1.0))
c.view(around(at, 230, 330, 1480, 1050, pad=1.0), 0, "beauvais", move=11.0)   # a slow push in on the choir
c.tag("8 · The limit: Beauvais")
credit_top(c, "IMG_BEAUVAIS_CHEVET")
lower_left(c, ["Beauvais Cathedral today: the choir"], 0, "beauvais", size=0.028, until=1)
lower_left(c, ["1225: fire in the old Romanesque choir"], 1, "fire", size=0.03)
beat("C8", "B31", "fact", "SHOW_CONTEXT", [
    "Which brings us back to Beauvais.",
    "In 1225, a fire damaged the old Romanesque choir, and the bishop decided to rebuild it, inspired by the greatest buildings of his time."],
    ["CLM_180"], strategy="CARD", graphic=c.spec(), visual_goal="The real building first, filling the frame: the choir of Beauvais today, then the date",
    required_concepts=[])

c = Card("B32")
_, at = fitted("IMG_BEAUVAIS_CHOIR", FULL)
w = at(1126, 0)[0] - at(0, 0)[0]
level_y = lambda p0, p1: (at(0, p0)[1] + at(0, p1)[1]) / 2   # noqa: E731
c.stage()
c.image("IMG_BEAUVAIS_CHOIR", FULL, sentence=0)
bx = at(1126, 0)[0] - 0.02   # the bracket inside the photograph, along its right side
ya, yb = at(0, 1280)[1] + 0.006, at(0, 430)[1] - 0.006
c.drawn([[bx - 0.008, ya], [bx, ya], [bx, yb], [bx - 0.008, yb]], THRUST, 0.004, 1, "adding", seconds=0.5, delay=1.8)
c.stage(False)
# the camera climbs the choir level by level, as the narration builds it: arcade, triforium, then the upper windows
arcade = c.view(square(0.5, w / 2, w))
trif = c.view(square(0.5, level_y(1300, 1585), w), 0, "lower", move=1.6)
upper = c.view(square(0.5, level_y(430, 1280), 0.3), 1, "adding", move=1.8)
credit_top(c, "IMG_BEAUVAIS_CHOIR")
lower_left(c, ["Arcade"], 0, size=0.032, until=0, until_word="lower")
c.text("Triforium", 0.06, 0.5, 0.032, 0, align="LEFT", plate=True, word="lower").later(1.6, "lower").gone(1, "adding")
lower_left(c, ["1250s: arcade and triforium finished"], 0, "finished", size=0.028, until=1, until_word="adding")
x, y = on_screen(upper, [bx, level_y(430, 1280)])
c.text("Upper windows: + about 5 m", x - 0.03, y + 0.03, 0.03, 1, align="RIGHT", color=THRUST, plate=True, word="adding").later(2.3, "adding")
c.text("the added height is schematic", x - 0.03, y - 0.03, 0.02, 1, align="RIGHT", color=MUTED, plate=True, word="adding").later(2.3, "adding")
lower_left(c, ["1272: the choir in use"], 2, "1272", size=0.028)
beat("C8", "B32", "fact", "EXPLAIN_DESIGN_CHANGE", [
    "By the 1250s, the two lower levels of the new choir were finished.",
    "Then the bishop apparently decided to go beyond the planned proportions, adding about five meters to the upper windows, and so to the vaults.",
    "By 1272, the clergy could use the new choir."],
    ["CLM_181"], strategy="CARD", graphic=c.spec(),
    visual_goal="The choir itself: its three levels marked; the camera moves in on the upper windows when they are said to grow",
    required_concepts=[])

c = Card("B33")
c.image("IMG_BEAUVAIS_CHOIR", [0.5, 0.0, 1.0, 1.0], (0.0, 0.45, 1.0, 1.0), 0)   # first: a card never opens empty
c.image("IMG_AMIENS_NAVE", [0.0, 0.0, 0.5, 1.0], sentence=0, word="above")
c.text("Amiens: more than 42 m", 0.25, 0.9, 0.032, 0, plate=True, word="above")
c.text("Beauvais: more than 45 m", 0.75, 0.9, 0.032, 0, plate=True, word="45")
c.text("The highest vaults built in the Middle Ages", 0.5, 0.28, 0.032, 1, plate=True, word="highest")
c.text("Published for Beauvais: 46 m, 46.7 m, nearly 47 m, above 48 m", 0.5, 0.215, 0.018, 0, color=MUTED, plate=True, word="45")
c.text(PHOTOS["IMG_AMIENS_NAVE"]["credit"], 0.25, 0.83, 0.015, 0, color=MUTED, word="above")
c.text(PHOTOS["IMG_BEAUVAIS_CHOIR"]["credit"], 0.75, 0.83, 0.015, 0, color=MUTED)
beat("C8", "B33", "fact", "COMPARE_VARIANTS", [
    "Its vault rose more than 45 meters, a few meters above Amiens.",
    "These were the highest vaults built in the Middle Ages."],
    ["CLM_102", "CLM_103", "CLM_104"], strategy="CARD", graphic=c.spec(),
    visual_goal="Two real buildings side by side, each by its own photograph, with its height; the caveat on the published figures",
    required_concepts=[])

c = Card("B34")
c.stage()
c.image("DRW_VLD_BEAUVAIS_PLAN", FULL, sentence=0)
end = mark_box(c, AT_PLAN, 255, 165, 358, 325, 0, "part", delay=1.4)
(x0, y1), (x1, y0) = AT_PLAN(255, 165), AT_PLAN(358, 325)
for k in range(5):   # a light hatch: the area, not a picture of a collapse
    y = y0 + (y1 - y0) * (k + 1) / 6
    c.line([[x0 + 0.002, y], [x1 - 0.002, y]], THRUST, 0.0015, 0, layer=2)
    c.elements[-1].update(word="part", delay=round(end + 0.08 * k, 3))
c.stage(False)
c.view(CHOIR_VIEW)
c.view(STRAIGHT, 0, "part", move=1.4)
c.text("Plan of Beauvais: Viollet-le-Duc, 1856", 0.95, CREDIT_TOP, 0.016, 0, align="RIGHT", color=MUTED)
top_left(c, ["29 November 1284"], 0, "november", size=0.034)
lower_left(c, ["Vault cells over the choir's straight bays fell"], 0, "part", size=0.028).later(end, "part")
lower_left(c, ["“The last limit”: Viollet-le-Duc, who drew this plan"], 1, "called", y=0.24, size=0.026)
beat("C8", "B34", "fact", "SHOW_COMPONENT", [
    "Then, in November 1284, part of the vaults over the choir came down.",
    "The architect Viollet-le-Duc, writing centuries later, called it the last limit that the great churches of the 13th century could reach."],
    ["CLM_182"], strategy="CARD", graphic=c.spec(),
    visual_goal="Beauvais's own plan, whole; the camera moves in on the straight bays where vault cells fell, marked; no collapse is shown",
    required_concepts=[])

c = Card("B35")
_, at = fitted("DRW_VLD_BEAUVAIS_BUTTRESS", FULL)
c.stage()
c.image("DRW_VLD_BEAUVAIS_BUTTRESS", FULL, sentence=0)
mark_box(c, at, 165, 130, 385, 370, 1, "blame", delay=1.2, until=2)               # 1: the flying buttresses
for k, py in enumerate((150, 260, 370)):                                           # 2: wind on the upper parts
    y = at(0, py)[1]
    n = len(c.elements)
    c.drawn_arrow([[at(0, 0)[0] - 0.09, y], [at(0, 0)[0] - 0.006, y]], ACCENT, 0.005, 2, "gusts", seconds=0.5,
                  until=2, delay=0.15 * k)
    for e in c.elements[n:]:
        e["until_word"] = "or"
for k, px_ in enumerate((110, 235, 360)):                                          # 3: settling foundations
    (xa, ya), (_, yb) = at(px_, 860), at(px_, 965)
    c.drawn_arrow([[xa, ya], [xa, yb]], ACCENT, 0.005, 2, "settlement", seconds=0.4, until=3, delay=0.1 * k)
    c.line([[xa, ya], [xa, yb + 0.012]], FAINT, 0.004, 3, layer=2)                # the study: the arrows grey out
    c.elements[-1]["until"] = 4
mark_box(c, at, 60, 15, 600, 565, 4, "raising", color=THRUST)                      # their hypothesis: the upper parts
c.stage(False)
c.view(FULL)
c.view(around(at, 150, 120, 400, 380, pad=1.25), 1, "blame", move=1.2)
c.view(around(at, 0, 0, 630, 600, pad=1.1), 2, "others", move=1.2)
low = c.view(square(0.5, 0.128, at(630, 0)[0] - at(0, 0)[0]), 2, "or", move=1.0)
c.view(around(at, 0, 0, 630, 600, pad=1.1), 4, "authors", move=1.2)
c.text("Section of Beauvais: Viollet-le-Duc, 1856; marks schematic", 0.95, CREDIT_TOP, 0.016, 0, align="RIGHT", color=MUTED)
top_left(c, ["Why did the vaults fall? Still debated."], 0, size=0.034, until=1)
top_left(c, ["Hypothesis: settling masonry broke", "the flying buttresses"], 1, "blame", until=2)
top_left(c, ["Hypothesis: gusts of wind set the", "buttress system resonating"], 2, "gusts", until=2, until_word="or")
top_left(c, ["Hypothesis: slow settlement", "of the foundations"], 2, "settlement", until=3)
x, y = on_screen(low, at(235, 900))
c.text("Not supported by this study", x, y + 0.13, 0.026, 3, color=MUTED, plate=True, word="nothing").gone(4)
top_left(c, ["Vernhes, Renault and Zotna, 2024:", "“nothing appears to justify", "a geotechnical origin”"], 3, "study",
         size=0.028, color=THRUST, until=4)
top_left(c, ["Their hypothesis: vaults raised against proven", "proportions left the upper parts too flexible"], 4,
         "raising", size=0.028, color=THRUST)
lower_left(c, ["ECSMGE 2024: an argument, not a settled result"], 3, "study", y=0.25, size=0.02, color=MUTED)
beat("C8", "B35", "fact", "EXPLAIN_CAUSE_EFFECT", [
    "Why it happened is still debated.",
    "Some blame settling masonry that broke the flying buttresses.",
    "Others point to gusts of wind setting the buttress system resonating, or to slow settlement of the foundations.",
    "A 2024 study found nothing to justify a foundation cause.",
    "Its authors argue that raising the vaults, against proven proportions, left the upper parts too flexible."],
    ["CLM_183", "CLM_184"], strategy="CARD", graphic=c.spec(),
    visual_goal="One hypothesis at a time on Viollet-le-Duc's section of Beauvais, the camera on the part each names; the 2024 "
                "study greys the foundation hypothesis (not supported by that study, not ruled out); their argument last",
    required_concepts=[])

c = Card("B36")
c.stage()
c.image("DRW_VLD_BEAUVAIS_PLAN", FULL, sentence=0)
OLD_ROWS, NEW_ROWS = (167.5, 222.5, 275, 322.5), (195, 248.75, 298.75)
for k, (px_, py) in enumerate((x_, y_) for x_ in (260, 353.5) for y_ in NEW_ROWS):   # new piers between the old ones
    c.circle(AT_PLAN(px_, py), 0.006, THRUST, 1)
    c.elements[-1].update(word="piers", delay=round(1.0 + 0.1 * k, 3))
for k, py in enumerate(NEW_ROWS):   # the new transverse lines: six bays
    (xa, y), (xb, _) = AT_PLAN(260, py), AT_PLAN(353.5, py)
    c.drawn([[xa, y], [xb, y]], THRUST, 0.0025, 1, "six", seconds=0.4, dash=True, delay=0.15 * k)
c.stage(False)
c.view(CHOIR_VIEW)
c.view(STRAIGHT, 1, move=1.2)
c.view(CHOIR_VIEW, 2, "finished", move=1.4, delay=0.3)
for k, py in enumerate((195, 248.75, 298.75)):   # three bays, numbered while the camera is on them
    x, y = on_screen(STRAIGHT, AT_PLAN(306, py))
    c.text(str(k + 1), x, y, 0.034, 1, plate=True).later(1.2).gone(1, "six")
for k, (a, b) in enumerate(zip(sorted(OLD_ROWS + NEW_ROWS), sorted(OLD_ROWS + NEW_ROWS)[1:])):
    x, y = on_screen(STRAIGHT, AT_PLAN(306, (a + b) / 2))
    c.text(str(k + 1), x, y, 0.026, 1, color=THRUST, plate=True, word="six").later(0.6, "six").gone(2, "finished")
c.text("Plan of Beauvais: Viollet-le-Duc, 1856", 0.95, CREDIT_TOP, 0.016, 0, align="RIGHT", color=MUTED)
top_left(c, ["The repair"], 0, size=0.034)
lower_left(c, ["New piers between the old ones (positions schematic)"], 1, "piers", size=0.026, until=2).later(1.0, "piers")
lower_left(c, ["Finished in 1340", "“Longer to repair the choir than to build it”: Stephen Murray"], 2, "finished", size=0.026)
beat("C8", "B36", "fact", "EXPLAIN_DESIGN_CHANGE", [
    "The repair tells its own story.",
    "New piers went up between the old ones, turning three bays into six.",
    "The work was not finished until 1340: as the historian Stephen Murray put it, it took longer to repair the choir than to build it."],
    ["CLM_185", "CLM_182"], strategy="CARD", graphic=c.spec(),
    visual_goal="The plan, then close on the three straight bays: numbered 1 to 3, the new piers appear, the bays become 1 to 6; "
                "then out again for the date",
    required_concepts=[])

c = Card("B37")
_, at_photo = fitted("IMG_BEAUVAIS_TRANSEPT", FULL)
c.stage()
c.image("IMG_BEAUVAIS_TRANSEPT", FULL, sentence=0, until=1)
c.elements[-1]["until_word"] = "instead"   # dissolves under the plan
c.image("DRW_VLD_BEAUVAIS_PLAN", FULL, sentence=1, until=4)
c.elements[-1].update(layer=1, until_word="great")
for k, (px_, py) in enumerate(((260, 322.5), (353.5, 322.5), (260, 416), (353.5, 416))):
    c.circle(AT_PLAN(px_, py), 0.006, THRUST, 2)
    c.elements[-1].update(word="slender", delay=round(0.15 * k, 3), until=4)
mark_box(c, AT_PLAN, 150, 475, 460, 905, 2, "west", color=THRUST, until=4, delay=0.3)
c.image("IMG_BEAUVAIS_TRANSEPT", FULL, sentence=4)
c.elements[-1]["layer"] = 2
c.stage(False)
pw = at_photo(1743, 0)[0] - at_photo(0, 0)[0]
photo = c.view(square(0.5, 0.56, pw))
c.view(around(AT_PLAN, 200, 270, 410, 470, pad=1.5), 1, move=1.5)          # the crossing, where the tower stood
nave = c.view(around(AT_PLAN, 100, 270, 520, 905, pad=1.05), 2, "lack", move=1.5)   # and the west side: no nave
c.view(square(0.5, 0.56, pw), 4, move=1.2)
# a timeline band at the top: it moves on to each date as it is told
c.rect([0.04, 0.76, 0.96, 0.95], "#EDEBE5", border=FAINT, sentence=0, border_width=0.002, layer=3)
X = lambda year: 0.08 + (year - 1480) / 120.0 * 0.84   # noqa: E731
c.line([[X(1480), 0.85], [X(1600), 0.85]], INK, 0.004, 0, layer=4)
for year in (1480, 1520, 1560, 1600):
    c.text(str(year), X(year), 0.815, 0.016, 0, color=MUTED)
reach = X(1480)
for year, label, s_, word, y in ((1500, "1500  Transept begun", 0, "transept", 0.9),
                                 (1569, "1569  Tower and spire, about 150 m", 1, "finished", 0.9),
                                 (1573, "1573  The tower falls", 3, "1573", 0.78)):
    wait = c.drawn([[reach, 0.85], [X(year), 0.85]], ACCENT, 0.007, s_, word, seconds=min(0.9, 0.25 + (X(year) - reach) * 2),
                   layer=5)
    reach = X(year)
    c.circle([X(year), 0.85], 0.007, INK, s_).later(wait, word)
    c.text(label, min(max(X(year), 0.2), 0.8), y, 0.02, s_, plate=True).later(wait, word)
c.text(PHOTOS["IMG_BEAUVAIS_TRANSEPT"]["credit"] + "; plan: Viollet-le-Duc, 1856", 0.95, 0.205, 0.015, 0, align="RIGHT",
       color=MUTED)
lower_left(c, ["Beauvais Cathedral today: transept and choir"], 0, "transept", size=0.026, until=1)
x, y = on_screen(nave, AT_PLAN(305, 690))
c.text("No nave: no support to the west", x, y, 0.026, 2, plate=True, word="west").later(1.0, "west").gone(4)
lower_left(c, ["The Gothic nave: never built"], 4, "never", size=0.03, color=THRUST)
beat("C8", "B37", "fact", "SHOW_CONTEXT", [
    "In the sixteenth century, work began again, with a new transept, the cross-arm of the building.",
    "Then, instead of a nave, the builders raised a lantern tower and spire about 150 meters high, finished in 1569.",
    "It rested on four slender piers, and the sources point to a lack of support on the west side, where the nave had not been built.",
    "In 1573, just four years after it was finished, the tower came down.",
    "The great Gothic nave was never built."],
    ["CLM_186", "CLM_187", "CLM_106"], strategy="CARD", graphic=c.spec(),
    visual_goal="The building today, then its plan: the crossing and its four piers, then the west side where no nave stands; "
                "back to the photograph; the timeline moves on to each date. The fall is told, not shown",
    required_concepts=[])

c = Card("B38")
_, at = fitted("IMG_AMIENS_NAVE", FULL)
_, at_plan = fitted("DRW_VLD_AMIENS_PLAN", FULL)
c.stage()
c.image("IMG_AMIENS_NAVE", FULL, sentence=0, until=1)
c.elements[-1]["until_word"] = "within"
c.image("DRW_VLD_AMIENS_PLAN", FULL, sentence=1)
c.elements[-1]["layer"] = 1
for k, (px_, py) in enumerate(((213, 447), (305, 447), (213, 541), (305, 541))):
    c.circle(at_plan(px_, py), 0.004, THRUST, 1)
    c.elements[-1].update(word="crossing", delay=round(1.2 + 0.12 * k, 3))
xa, ya = at_plan(318, 875)
_, yb = at_plan(318, 548)
c.drawn([[xa, ya], [xa, yb]], ACCENT, 0.007, 2, "chain", seconds=1.6, dash=True)
c.stage(False)
w = at(1892, 0)[0] - at(0, 0)[0]
c.view(square(0.5, 1 - w / 2, w))
nave_view = c.view(around(at_plan, 60, 400, 460, 900, pad=1.05), 1, move=1.5)
crossing = c.view(around(at_plan, 170, 400, 350, 590, pad=1.5), 1, "crossing", move=1.2)
c.view(nave_view, 2, "between", move=1.5)
credit_top(c, "IMG_AMIENS_NAVE").gone(1)
c.text("Plan of Amiens: Viollet-le-Duc, 1854", 0.95, CREDIT_TOP, 0.016, 1, align="RIGHT", color=MUTED)
lower_left(c, ["Amiens Cathedral today"], 0, size=0.028, until=1)
lower_left(c, ["Crossing piers: threatening collapse within two centuries"], 1, "crossing", size=0.026, until=2).later(1.2, "crossing")
x, y = on_screen(nave_view, [xa, (ya + yb) / 2])
c.text("Iron chain, 1497–1500", x + 0.03, y + 0.03, 0.03, 2, align="LEFT", color=ACCENT, plate=True, word="chain")
c.text("route schematic", x + 0.03, y - 0.025, 0.022, 2, align="LEFT", color=MUTED, plate=True, word="chain")
lower_left(c, ["Iron rods linked together, along the nave, tying the crossing pier"], 2, "runs", size=0.024, color=MUTED)
beat("C8", "B38", "fact", "SHOW_CONTEXT", [
    "Beauvais was not alone.",
    "At Amiens, within two centuries, the piers at the crossing, where the arms of the building meet, were threatening collapse.",
    "Between 1497 and 1500, an iron chain was installed to stop the movement, and it still runs through the building today."],
    ["CLM_190", "CLM_191", "CLM_106"], strategy="CARD", graphic=c.spec(),
    visual_goal="Amiens by its own photograph, then its plan, large: the camera moves in on the crossing piers, then out "
                "along the nave while the chain's route is drawn",
    required_concepts=[])

# C9 -------------------------------------------------------------------------------------------
beat("C9", "B39", "fact", "EXPLAIN_STRUCTURE", [
    "So why do these buildings stand at all?",
    "One answer from modern engineers is that the stone's strength is rarely the limit.",
    "Stresses in masonry are typically only a fraction of what the stone can bear, and in most cases structures fail through instability, not a lack of strength."],
    ["CLM_112"], strategy="HOLD", camera_move={"type": "PUSH_IN", "amount": 0.1}, visual_goal="The full section at rest",
    required_concepts=[GOTHIC],
    annotations=[note("B39_ch", "9 · Why they stand", 0, 2)])

# The example of Block, DeJong and Ochsendorf 2006, figure 5: thickness 15.24% of the radius, 160 degrees. The behaviour
# on moving supports, with an intrados hinge that moves toward the crown, follows Ochsendorf 2002 (arch_statics.py).
T40, HALF40 = 0.1524, 80.0
R40, FOOT40 = 0.3, 0.345
REST40, MOVED40 = 0.26, 0.74   # centres of the two arches on the card


def arch_card(cx):
    """Arch coordinates (radius 1, crown on +y) to card coordinates, with the feet at FOOT40."""
    base = math.cos(math.radians(HALF40))
    return lambda x, y: [cx + R40 * x / ASPECT, FOOT40 + R40 * (y - base)]


def joint_point(degrees, r):
    return r * math.sin(math.radians(degrees)), r * math.cos(math.radians(degrees))


def arch40(c, cx, sentence, hinge=None, shape=None, until=None):
    """Stones and abutments, at rest or deformed (shape from statics.spread_shape): the stones above the hinge turn as
    one part, the stones below it and the abutment move with the support."""
    card = arch_card(cx)
    upper = shape["upper"] if shape else (lambda x, y: (x, y))
    lower = shape["lower"] if shape else (lambda x, y: (x, y))
    ri, ro = 1 - T40 / 2, 1 + T40 / 2
    joints = sorted(set(list(range(0, 90, 10)) + ([hinge] if hinge else [])))
    joints = [j for j in joints if not hinge or j == hinge or abs(j - hinge) > 2]
    for side in (1, -1):
        def to_card(move, x, y):
            mx, my = move(x, y)
            return card(side * mx, my)
        for a0, a1 in zip(joints, joints[1:]):
            move = upper if hinge and a1 <= hinge else lower
            inner = [to_card(move, *joint_point(a0 + (a1 - a0) * k / 2, ri)) for k in range(3)]
            outer = [to_card(move, *joint_point(a1 - (a1 - a0) * k / 2, ro)) for k in range(3)]
            c.polygon(inner + outer, STONE, border="#7A6E58", sentence=sentence, until=until, layer=1)
        ix, iy = joint_point(HALF40, ri)
        ox, oy = joint_point(HALF40, ro)
        c.polygon([to_card(lower, ix, iy), to_card(lower, ox, oy), to_card(lower, ox + 0.05, -0.06), to_card(lower, ix - 0.03, -0.06)],
                  "#9A927F", sentence=sentence, until=until)


def line40(c, cx, radii, joints, sentence, shape=None, color=ACCENT, width=0.006, until=None, step=8):
    """A thrust line through the pressure points on the joints; symmetric about the crown."""
    card = arch_card(cx)
    right = []
    for k in list(range(0, len(joints), step)) + [len(joints) - 1]:
        x, y = joint_point(math.degrees(joints[k]), radii[k])
        if shape:
            x, y = (shape["upper"] if k <= shape["hinge_joint"] else shape["lower"])(x, y)
        right.append((x, y))
    c.line([card(-x, y) for x, y in reversed(right[1:])] + [card(x, y) for x, y in right], color, width, sentence, until=until, layer=2)


c = Card("B40")
valid = statics.thrust_range(HALF40, T40)
arch40(c, REST40, 0)
line40(c, REST40, *statics.line_radii(HALF40, T40, *valid["middle"]), 0)
c.text("The line of thrust", REST40, 0.69, 0.028, 0, plate=True, color=ACCENT)
c.text("Assumed: stones resist no pulling, never slide, never crush", 0.5, 0.9, 0.028, 1, plate=True)
line40(c, REST40, *statics.line_radii(HALF40, T40, *valid["min"]), 2)
line40(c, REST40, *statics.line_radii(HALF40, T40, *valid["max"]), 2)
c.text("Many lines can fit. One is enough", REST40, 0.76, 0.028, 2, plate=True, color=ACCENT)
moving = statics.spread_to_collapse(HALF40, T40, stop_at=0.05)
moving_shape = statics.spread_shape(HALF40, T40, moving)
limit = statics.spread_to_collapse(HALF40, T40)
limit_shape = statics.spread_shape(HALF40, T40, limit)
arch40(c, MOVED40, 3, moving["hinge"], moving_shape, until=4)
line40(c, MOVED40, moving_shape["radii"], moving_shape["joints"], 3, moving_shape, THRUST, until=4)
c.text("Supports moved apart: the arch deforms", MOVED40, 0.76, 0.028, 3, plate=True, until=4)
for side in (1, -1):
    foot = MOVED40 + side * R40 * 1.3 / ASPECT
    c.arrow([foot, 0.3], [foot + side * 0.025, 0.3], INK, 0.006, 3)
arch40(c, MOVED40, 4, limit["hinge"], limit_shape)
line40(c, MOVED40, limit_shape["radii"], limit_shape["joints"], 4, limit_shape, THRUST)
card40 = arch_card(MOVED40)
hinges = [limit_shape["upper"](*joint_point(0, 1 + T40 / 2)), limit_shape["lower"](*joint_point(limit["hinge"], 1 - T40 / 2)),
          limit_shape["lower"](*joint_point(HALF40, 1 + T40 / 2))]
for x, y in hinges + [(-x, y) for x, y in hinges[1:]]:
    c.circle(card40(x, y), 0.009, THRUST, 4)
c.text("At the limit, the line touches the stone at five points", MOVED40, 0.76, 0.028, 4, plate=True, color=THRUST)
c.text("Any further, and no line can fit", MOVED40, 0.69, 0.028, 4, plate=True, color=THRUST)
c.text("After Block, DeJong and Ochsendorf, 2006, Fig. 5, recalculated by Ochsendorf's 2002 method. One idealized arch, self-weight only", 0.5, 0.225, 0.021, 0, color=MUTED)
beat("C9", "B40", "fact", "EXPLAIN_STRUCTURE", [
    "Picture one idealized arch, and the path of the force through its stones, which engineers call the line of thrust.",
    "This analysis assumes that the stones resist no pulling, never slide and never crush.",
    "Under those assumptions and a given load, many such lines can fit inside the masonry, and finding one is enough to show the arch can stand.",
    "Now move its supports apart, and the arch deforms.",
    "Past a certain point, no line can fit inside it, and this idealized arch collapses."],
    ["CLM_113", "CLM_111", "CLM_117", "CLM_118"], strategy="CARD", graphic=c.spec(),
    visual_goal="One arch at rest with several valid lines; the same arch with its supports moved apart, up to the limit. The fall itself is not shown",
    required_concepts=[])

c = Card("B41")
c.line(place(pointed_arch(0.12, 0.14), 0.22, 0.3), ACCENT, 0.008, 0)
c.line(place(pointed_arch(0.5, 0.58), 0.62, 0.26), ACCENT, 0.016, 0)
c.text("Small model", 0.22, 0.24, 0.028, 1, plate=True)
c.text("Real building", 0.62, 0.22, 0.028, 1, plate=True)
c.text("Same proportions", 0.32, 0.72, 0.034, 1, plate=True, word="proportions")
c.text("Shows the role of proportion", 0.2, 0.62, 0.026, 1, color=ACCENT, word="show")
c.text("Does not prove a real building safe", 0.2, 0.55, 0.026, 2, color=THRUST)
c.text("Rules of geometry, learned by trial and error", 0.5, 0.88, 0.03, 3, plate=True, word="geometry")
beat("C9", "B41", "fact", "EXPLAIN_STRUCTURE", [
    "That puts shape and proportion at the center of the question.",
    "Unlike some other engineering problems, stability can be scaled, so a small model with the same proportions helps show what proportion does.",
    "On its own, that does not show a whole real building is safe: this kind of analysis can miss effects such as local crushing, cracking and sliding.",
    "But it helps explain how rules of geometry, learned by trial and error, could carry builders so far."],
    ["CLM_112", "CLM_116", "CLM_110"], strategy="CARD", graphic=c.spec(), visual_goal="One shape at two sizes; what the model shows and what it does not", required_concepts=[])

# C10 ------------------------------------------------------------------------------------------
beat("C10", "B42", "interpretation", "SUMMARIZE_DIFFERENCES", [
    "So the heights were never impossible.",
    "Pointed arches gave builders taller, more adaptable shapes, ribs helped direct the load toward the piers, and flying buttresses carried the thrust outside and down to the ground.",
    "The walls in between could open up to glass."],
    ["CLM_130", "CLM_132", "CLM_140", "CLM_152", "CLM_143"], strategy="HOLD_HIGHLIGHT", highlight_at_sentence=1, camera_move={"type": "PUSH_IN", "amount": 0.08},
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
for y, line in ((0.68, "Sources: Columbia University (Life of a Cathedral; S. Murray; R. Stalley); Harvard (Loeb Library); New Catholic Encyclopedia;"),
                (0.63, "MIT (P. Block, 2005; Block, DeJong and Ochsendorf, 2006; Romano and Ochsendorf); Cambridge (J. Ochsendorf, 2002);"),
                (0.58, "Bibliothèque nationale de France; France Mémoire (A. Timbert); Durham Cathedral; Abbaye de Cluny (CMN);"),
                (0.53, "ECSMGE 2024 (Vernhes, Renault, Zotna); Association Beauvais Cathédrale"),
                (0.44, "3D models and diagrams are illustrative, not structural analyses")):
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
                           "reason": "Revision g-r3: script after the owner's second review; claims source-verified, not editorially approved."},
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
