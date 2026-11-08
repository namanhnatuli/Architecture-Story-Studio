"""2D card authoring for "Could We Build an Entire City That Floats?" (engine/diagram.py draws them).

The same element vocabulary as the Gothic film's cards (text, rect, line, arrow, circle, polygon; drawn paths appear
along their route; elements appear at a sentence or at a spoken word). Card coordinates: x, y in 0..1 of the frame,
origin bottom-left; nothing below y 0.2 (the subtitle zone ends at 0.17).
"""
import math

ASPECT = 16 / 9
INK, MUTED, FAINT = "#24231F", "#55524A", "#8A867C"
ACCENT, GOLD, WARN = "#1E5C96", "#D9A441", "#B5523B"
WATER, WATER_CUT, SEABED = "#86A9B8", "#5F8CA2", "#B7AE90"
CONCRETE, PLASTER, ROOF, LAND = "#B8B4AA", "#E5DCCB", "#657887", "#ADA98F"
POWER, DRINKING, WASTE = "#C8962E", "#3F7FA8", "#7A5C3E"
BG = "#EDEBE5"
CHAR_W = 0.26   # text width per character in units of the text size (Gothic card QA)
DASH = [0.012, 0.008]


class Card:
    def __init__(self, name):
        self.name, self.elements = name, []

    def add(self, kind, sentence=0, until=None, **kw):
        e = {"id": f"{self.name}_{len(self.elements):02d}", "kind": kind, "sentence": sentence, **kw}
        if until is not None:
            e["until"] = until
        self.elements.append(e)
        return self

    def at(self, word=None, delay=None):
        """Time the last element by a spoken word of its sentence and/or a delay after its moment."""
        if word:
            self.elements[-1]["word"] = word
        if delay:
            self.elements[-1]["delay"] = round(delay, 3)
        return self

    def gone(self, sentence, word=None):
        self.elements[-1]["until"] = sentence
        if word:
            self.elements[-1]["until_word"] = word
        return self

    def text(self, text, x, y, size=0.034, sentence=0, align="CENTER", color=INK, plate=False, until=None, word=None):
        return self.add("text", sentence, until, text=text, position=[round(x, 4), round(y, 4)], size=size, align=align,
                        color=color, plate=plate, **({"word": word} if word else {}))

    def rect(self, box, color=None, border=None, sentence=0, border_width=0.004, dash=False, until=None, layer=0, word=None):
        kw = {"box": [round(v, 4) for v in box], "layer": layer}
        if color:
            kw["color"] = color
        if border:
            kw.update(border=border, border_width=border_width)
        if dash:
            kw["dash"] = DASH
        if word:
            kw["word"] = word
        return self.add("rect", sentence, until, **kw)

    def line(self, points, color=INK, width=0.005, sentence=0, dash=False, until=None, layer=0, word=None):
        kw = {"points": [[round(x, 4), round(y, 4)] for x, y in points], "color": color, "width": width, "layer": layer}
        if dash:
            kw["dash"] = DASH
        if word:
            kw["word"] = word
        return self.add("line", sentence, until, **kw)

    def arrow(self, start, end, color=INK, width=0.007, sentence=0, until=None, word=None):
        return self.add("arrow", sentence, until, start=[round(v, 4) for v in start], end=[round(v, 4) for v in end],
                        color=color, width=width, **({"word": word} if word else {}))

    def circle(self, center, radius=0.012, color=INK, sentence=0, until=None, word=None):
        return self.add("circle", sentence, until, center=[round(v, 4) for v in center], radius=radius, color=color,
                        **({"word": word} if word else {}))

    def polygon(self, points, color, border=None, sentence=0, until=None, layer=0, word=None, border_width=0.0025):
        kw = {"points": [[round(x, 4), round(y, 4)] for x, y in points], "color": color, "layer": layer}
        if border:
            kw.update(border=border, border_width=border_width)
        if word:
            kw["word"] = word
        return self.add("polygon", sentence, until, **kw)

    def tag(self, text, sentence=0):
        return self.text(text, 0.055, 0.915, 0.024, sentence, align="LEFT", color=MUTED, plate=True)

    def drawn(self, points, color=INK, width=0.005, sentence=0, word=None, seconds=0.6, dash=False, until=None, layer=2,
              delay=0.0):
        """A polyline in short pieces that appear in order over `seconds` from its moment (+ delay); returns the time
        it takes, so a label can wait for it."""
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

    def spec(self):
        """Whatever the first sentence shows from its start is on screen from the first frame (a card never opens on an
        empty frame); later elements fade in at their moment."""
        for e in self.elements:
            if e.get("sentence") == 0 and not e.get("word") and not e.get("delay"):
                e["from_start"] = True
        return {"fade_seconds": 0.35, "elements": self.elements}


def box_points(x0, y0, x1, y1):
    return [[x0, y0], [x1, y0], [x1, y1], [x0, y1]]


def icon(points, cx, cy, size):
    """A shape drawn in a unit box (u right, v up, 0..1), centred at (cx, cy), `size` tall in card height units."""
    return [[cx + (u - 0.5) * size / ASPECT, cy + (v - 0.5) * size] for u, v in points]


def pill(cx, cy, w, h, n=10):
    """A rounded button, w wide (card x units) and h tall."""
    r = h / 2
    pts = [[cx + w / 2 - r / ASPECT + r / ASPECT * math.cos(math.pi * (k / n - 0.5)), cy + r * math.sin(math.pi * (k / n - 0.5))]
           for k in range(n + 1)]
    pts += [[cx - w / 2 + r / ASPECT - r / ASPECT * math.cos(math.pi * (k / n - 0.5)), cy - r * math.sin(math.pi * (k / n - 0.5))]
            for k in range(n + 1)]
    return pts


# Self-drawn, generic symbols in the Studio style (no platform logo or trademark), as in the Gothic film's closing card
THUMB = [(0.30, 0.0), (0.84, 0.0), (0.93, 0.07), (0.99, 0.50), (0.93, 0.58), (0.64, 0.58), (0.68, 0.82), (0.64, 0.97),
         (0.56, 1.0), (0.49, 0.95), (0.45, 0.78), (0.30, 0.57)]
CUFF = [(0.0, 0.0), (0.24, 0.0), (0.24, 0.58), (0.0, 0.58)]
BUBBLE = [(0.0, 0.32), (0.0, 1.0), (1.0, 1.0), (1.0, 0.32), (0.42, 0.32), (0.16, 0.04), (0.22, 0.32)]
BELL = [(0.5, 0.94), (0.30, 0.84), (0.22, 0.62), (0.20, 0.36), (0.08, 0.22), (0.92, 0.22), (0.80, 0.36), (0.78, 0.62),
        (0.70, 0.84)]
