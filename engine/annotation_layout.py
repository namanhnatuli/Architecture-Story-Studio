"""Semantic annotation layout (M6; pure Python, shared by planner/ and the Blender QA).

Input: one shot's resolved annotations - anchors already in normalised frame coordinates
(x 0..1 left to right, y 0..1 bottom to top) - and config/annotation_style.json. Output:
flat primitives in the same coordinates, which engine/annotations.py draws on a plane just
in front of the orthographic camera (geometry never hides them; subtitles stay outside the
3D scene, in the zone at the bottom of the frame that annotations never enter).

Rules (docs/m6/ANNOTATION_STYLE_GUIDE.md):
- every arrow has the same length and width: size never encodes magnitude;
- LOAD arrows point straight down onto their target; REACTION arrows point up (UP) or up
  and towards the middle of their target (UP_INWARD);
- text sits on a plate inside the title-safe area and above the subtitle zone, never on
  another visible text, the legend, the tag or its own target, and its leader does not
  cross another visible text;
- labels are placed by a deterministic search (distance rings x preferred directions).
"""
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STYLE_PATH = ROOT / "config" / "annotation_style.json"
FORCE_TYPES = ("LOAD_ARROW", "REACTION_ARROW", "CONCEPTUAL_LOAD_PATH", "TENSION_COMPRESSION_LEGEND")
_NARROW = set("iljtfrI.,:;'!|() -")
_WIDE = set("mwMW@")


class LayoutError(ValueError):
    pass


def load_style(path=STYLE_PATH):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def text_width(text, size, style):
    """Estimated width of `text` in frame-HEIGHT units for the built-in Blender font
    (calibrated 2026-10-29 on Bfont, Blender 5.2; the Blender QA measures the real width)."""
    w = style["text"]["char_widths"]
    total = 0.0
    for ch in text:
        if ch in _NARROW:
            total += w["narrow"]
        elif ch in _WIDE:
            total += w["wide"]
        elif ch.isdigit():
            total += w["digit"]
        elif ch.isupper():
            total += w["upper"]
        elif ch.islower():
            total += w["lower"]
        else:
            total += w["other"]
    return total * size * style["text"]["margin"]


def text_box_size(text, size, style, aspect):
    """(width in frame-width units, height in frame-height units) of a plated text."""
    pad = style["text"]["padding"] * size
    return (text_width(text, size, style) + 2 * pad) / aspect, size * 1.05 + 2 * pad


# ---------------------------------------------------------------- geometry helpers
def _iso(p, aspect):
    return (p[0] * aspect, p[1])


def _frame(q, aspect):
    return [q[0] / aspect, q[1]]


def overlaps(a, b, pad=0.0):
    return not (a[2] + pad <= b[0] or b[2] + pad <= a[0] or a[3] + pad <= b[1] or b[3] + pad <= a[1])


def _seg_hits_box(p, q, box, pad=0.0):
    """Segment p-q intersects the (padded) box (Liang-Barsky)."""
    x0, y0, x1, y1 = box[0] - pad, box[1] - pad, box[2] + pad, box[3] + pad
    dx, dy = q[0] - p[0], q[1] - p[1]
    t0, t1 = 0.0, 1.0
    for pk, qk in ((-dx, p[0] - x0), (dx, x1 - p[0]), (-dy, p[1] - y0), (dy, y1 - p[1])):
        if abs(pk) < 1e-12:
            if qk < 0:
                return False
        else:
            t = qk / pk
            if pk < 0:
                t0 = max(t0, t)
            else:
                t1 = min(t1, t)
            if t0 > t1:
                return False
    return True


def _nearest_on_box(p, box):
    return [min(max(p[0], box[0]), box[2]), min(max(p[1], box[1]), box[3])]


def _arrow(tail, tip, style_key, style, color):
    a = style[style_key]
    return {"kind": "arrow", "tail": [round(tail[0], 6), round(tail[1], 6)], "tip": [round(tip[0], 6), round(tip[1], 6)],
            "width": a.get("shaft", a.get("width")), "head_length": a["head_length"], "head_width": a["head_width"],
            "color": color}


def _inside(box, safe):
    return box[0] >= safe["left"] and box[2] <= safe["right"] and box[1] >= safe["bottom"] and box[3] <= safe["top"]


# ---------------------------------------------------------------- layout
class Layout:
    """Placed annotations of one shot; `occupied` holds (box, appear, disappear, owner, kind)."""

    def __init__(self, style, aspect, reserved=()):
        self.style, self.aspect = style, aspect
        self.items, self.occupied, self.problems = [], [], []
        for box, owner in reserved:   # e.g. the model caption of a sequential comparison
            self.occupied.append((list(box), -1e9, 1e9, owner, "text"))

    def _free(self, box, t0, t1, owner, avoid=(), leaders=()):
        pad = self.style["placement"]["padding"]
        safe = self.style["safe_area"]
        if not _inside(box, safe) or box[1] < self.style["subtitle_zone"]:
            return False
        for b in avoid:
            if overlaps(box, b, pad):
                return False
        for ob, a0, a1, own, kind in self.occupied:
            if own == owner or a1 <= t0 or t1 <= a0:
                continue
            if kind == "segment":   # arrows and path lines: the segment itself, not its bounding box
                if _seg_hits_box(ob[0], ob[1], box, pad * 0.4):
                    return False
            elif overlaps(box, ob, pad if kind == "text" else pad * 0.4):
                return False
        clear = self.style["placement"]["leader_clearance"]
        for p, q in leaders:          # the label's own leaders must not cross another visible text
            for ob, a0, a1, own, kind in self.occupied:
                if own != owner and kind == "text" and not (a1 <= t0 or t1 <= a0) and _seg_hits_box(p, q, ob, clear):
                    return False
        if not _inside(box, safe):
            return False
        return True

    def place(self, w, h, anchors, t0, t1, owner, avoid=(), leader_to=None, prefer=None):
        """Box (x0, y0, x1, y1) of size w x h near the anchors' centroid, or None."""
        pl = self.style["placement"]
        cx = sum(a[0] for a in anchors) / len(anchors)
        cy = sum(a[1] for a in anchors) / len(anchors)
        base = list(pl["directions_degrees"])
        dirs = base if prefer is None else sorted(base, key=lambda d: (abs(((d - prefer) + 180) % 360 - 180), base.index(d)))
        for dist in pl["distances"]:
            for deg in dirs:
                bx = cx + dist * math.cos(math.radians(deg)) / self.aspect
                by = cy + dist * math.sin(math.radians(deg))
                box = [bx - w / 2, by - h / 2, bx + w / 2, by + h / 2]
                leaders = [(_nearest_on_box(a, box), a) for a in (leader_to or [])]
                if self._free(box, t0, t1, owner, avoid, leaders):
                    return box
        return None

    def occupy(self, box, t0, t1, owner, kind):
        self.occupied.append((list(box), t0, t1, owner, kind))

    def plate_text(self, text, box, size, color=None):
        s = self.style
        return [{"kind": "plate", "box": [round(v, 6) for v in box], "fill": s["colors"]["plate"],
                 "border": s["colors"]["plate_border"], "border_width": s["text"]["border"]},
                {"kind": "text", "text": text, "size": size, "color": color or s["colors"]["text"],
                 "center": [round((box[0] + box[2]) / 2, 6), round((box[1] + box[3]) / 2, 6)],
                 "box": [round(v, 6) for v in box]}]


def _leader(p, box, style):
    return [{"kind": "line", "points": [[round(v, 6) for v in _nearest_on_box(p, box)], [round(p[0], 6), round(p[1], 6)]],
             "width": style["leader"]["width"], "color": style["colors"]["leader"], "dash": None},
            {"kind": "dot", "center": [round(p[0], 6), round(p[1], 6)], "radius": style["leader"]["dot"],
             "color": style["colors"]["leader"]}]


def _symbol(force, center, style, aspect):
    """Conceptual force symbol: arrowheads towards each other (compression, pushed) or
    away from each other (tension, pulled) on a short bar."""
    s = style["symbol"]
    half = s["length"] / 2 / aspect
    left, right = [center[0] - half, center[1]], [center[0] + half, center[1]]
    mid_l, mid_r = [center[0] - 0.004 / aspect, center[1]], [center[0] + 0.004 / aspect, center[1]]
    color = style["colors"][force]
    if force == "COMPRESSION":
        out = [_arrow(left, mid_l, "symbol", style, color), _arrow(right, mid_r, "symbol", style, color)]
    else:
        out = [_arrow(mid_l, left, "symbol", style, color), _arrow(mid_r, right, "symbol", style, color)]
    for e in out:
        e["symbol"] = force   # drawn without a halo (too small)
    return out


def layout_shot(items, style, aspect, reserved=()):
    """items: resolved annotations of one shot (planner/annotations.py), each with
    id, type, appear, disappear (shot seconds), anchors [{"screen": [x, y]}], target_boxes,
    and per type: text, count, direction, inward, branches, style, force, entries.
    Returns (laid-out annotations, problems)."""
    L = Layout(style, aspect, reserved)
    out = []
    size = style["text"]["size"]
    a = style["arrow"]
    force_times = [(it["appear"], it["disappear"]) for it in items
                   if it["type"] in FORCE_TYPES or it.get("force")]
    tag = None
    if force_times:   # one "not to scale" tag while any conceptual force graphic is shown
        t0, t1 = min(t for t, _ in force_times), max(t for _, t in force_times)
        ts = style["tag"]["size"]
        w, h = text_box_size(style["tag"]["text"], ts, style, aspect)
        safe = style["safe_area"]
        box = [safe["left"], safe["top"] - h, safe["left"] + w, safe["top"]]
        L.occupy(box, t0, t1, "TAG", "text")
        tag = {"id": "CONCEPTUAL_TAG", "type": "TAG", "appear": t0, "disappear": t1,
               "elements": L.plate_text(style["tag"]["text"], box, ts, style["colors"]["tag"]), "boxes": [box],
               "anchors": [], "segments": []}
    for it in sorted(items, key=lambda i: (i["appear"], i["order"])):
        t0, t1, owner, kind = it["appear"], it["disappear"], it["id"], it["type"]
        anchors = [x["screen"] for x in it["anchors"]]
        elements, boxes, segments = [], [], []
        avoid = list(it.get("target_boxes") or [])

        def text_near(text, pts, prefer=None, leaders=True, extra_avoid=()):
            w, h = text_box_size(text, size, style, aspect)
            box = L.place(w, h, pts, t0, t1, owner, avoid + list(extra_avoid), pts if leaders else None, prefer)
            if box is None:
                L.problems.append(f"{owner}: no free place for '{text}' (safe area, subtitle zone, other labels)")
                return None
            L.occupy(box, t0, t1, owner, "text")
            boxes.append(box)
            elements.extend(L.plate_text(text, box, size))
            if leaders:
                for p in pts:
                    elements.extend(_leader(p, box, style))
                    segments.append([_nearest_on_box(p, box), list(p)])
                    L.occupy([_nearest_on_box(p, box), list(p)], t0, t1, owner, "segment")
            return box

        if kind == "LOAD_ARROW":
            color = style["colors"]["LOAD"]
            tails = []
            for p in anchors:
                tip = [p[0], p[1] + a["gap"]]
                tail = [p[0], tip[1] + a["length"]]
                elements.append(_arrow(tail, tip, "arrow", style, color))
                segments.append([tail, tip])
                L.occupy([tail, tip], t0, t1, owner, "segment")
                tails.append(tail)
            if it.get("text"):
                mid = tails[len(tails) // 2]
                text_near(it["text"], [[mid[0], mid[1] + 0.01]], prefer=90, leaders=False)
        elif kind == "REACTION_ARROW":
            color = style["colors"]["REACTION"]
            th = math.radians(a["inward_degrees"]) if it.get("direction") == "UP_INWARD" else 0.0
            tails = []
            for p, s in zip(anchors, it.get("inward") or [0] * len(anchors)):
                d = (s * math.sin(th), math.cos(th))   # isotropic unit vector towards the tip
                tip_i = (p[0] * aspect - d[0] * a["gap"], p[1] - d[1] * a["gap"])
                tail_i = (tip_i[0] - d[0] * a["length"], tip_i[1] - d[1] * a["length"])
                tip, tail = _frame(tip_i, aspect), _frame(tail_i, aspect)
                elements.append(_arrow(tail, tip, "arrow", style, color))
                segments.append([tail, tip])
                L.occupy([tail, tip], t0, t1, owner, "segment")
                tails.append(tail)
            if it.get("text"):
                text_near(it["text"], tails, prefer=-90, leaders=False)
        elif kind == "CONCEPTUAL_LOAD_PATH":
            color = style["colors"]["COMPRESSION" if it.get("style") == "COMPRESSION" else "LOAD"]
            p = style["path"]
            for branch in it["branches"]:
                pts = [[round(x, 6), round(y, 6)] for x, y in branch]
                elements.append({"kind": "line", "points": pts[:-1] + [pts[-1]], "width": p["width"], "color": color,
                                 "dash": None if it.get("style") == "COMPRESSION" else [p["dash"], p["gap"]]})
                for k in range(1, len(pts)):   # one head per segment: the path's direction reads everywhere
                    q0, q1 = pts[k - 1], pts[k]
                    seg = math.hypot((q1[0] - q0[0]) * aspect, q1[1] - q0[1])
                    if seg < p["head_length"] * 1.5:
                        continue
                    f = 1.0 if k == len(pts) - 1 else 0.6
                    tip = [q0[0] + (q1[0] - q0[0]) * f, q0[1] + (q1[1] - q0[1]) * f]
                    back = p["head_length"] / seg
                    base = [tip[0] - (q1[0] - q0[0]) * back, tip[1] - (q1[1] - q0[1]) * back]
                    elements.append({"kind": "arrow", "tail": base, "tip": tip, "width": 0.0, "head_length": p["head_length"],
                                     "head_width": p["head_width"], "color": color})
                    segments.append([q0, q1])
                    L.occupy([q0, q1], t0, t1, owner, "segment")
            if it.get("text"):
                text_near(it["text"], [it["branches"][0][len(it["branches"][0]) // 2]], leaders=False)
        elif kind == "TENSION_COMPRESSION_LEGEND":
            lg = style["legend"]
            ls = lg["size"]
            rows = [lg["title"]] + [lg["entries"][e] for e in it.get("entries") or ["COMPRESSION", "TENSION"]]
            sym_w = (style["symbol"]["length"] + 0.02) / aspect
            w = max(text_width(r, ls, style) for r in rows) / aspect + sym_w + 2 * style["text"]["padding"] * ls / aspect
            rh = ls * 1.45
            h = rh * len(rows) + 2 * style["text"]["padding"] * ls
            safe = style["safe_area"]
            box = [safe["right"] - w, safe["top"] - h, safe["right"], safe["top"]]
            if not L._free(box, t0, t1, owner):
                L.problems.append(f"{owner}: the legend's corner is taken (top right)")
            L.occupy(box, t0, t1, owner, "text")
            boxes.append(box)
            elements.append({"kind": "plate", "box": [round(v, 6) for v in box], "fill": style["colors"]["plate"],
                             "border": style["colors"]["plate_border"], "border_width": style["text"]["border"]})
            pad_x = style["text"]["padding"] * ls / aspect
            for k, r in enumerate(rows):
                cy = box[3] - style["text"]["padding"] * ls - rh * (k + 0.5)
                if k == 0:
                    tx0 = box[0] + pad_x
                else:
                    force = (it.get("entries") or ["COMPRESSION", "TENSION"])[k - 1]
                    elements.extend(_symbol(force, [box[0] + pad_x + sym_w / 2 - 0.005 / aspect, cy], style, aspect))
                    tx0 = box[0] + pad_x + sym_w
                tw = text_width(r, ls, style) / aspect
                elements.append({"kind": "text", "text": r, "size": ls, "color": style["colors"]["text"],
                                 "center": [round(tx0 + tw / 2, 6), round(cy, 6)],
                                 "box": [round(tx0, 6), round(cy - ls * 0.6, 6), round(tx0 + tw, 6), round(cy + ls * 0.6, 6)]})
        elif kind in ("COMPONENT_LABEL", "CALLOUT"):
            text = it["text"]
            box = text_near(text, anchors, prefer=it.get("prefer"),
                            extra_avoid=[])
            if box is not None and it.get("force"):
                cx, cy = box[0] - style["symbol"]["length"] / 2 / aspect - 0.008 / aspect, (box[1] + box[3]) / 2
                sym_box = [cx - style["symbol"]["length"] / 2 / aspect - 0.004, cy - 0.015,
                           cx + style["symbol"]["length"] / 2 / aspect + 0.004, cy + 0.015]
                if not _inside(sym_box, style["safe_area"]) or not L._free(sym_box, t0, t1, owner):
                    cx = box[2] + style["symbol"]["length"] / 2 / aspect + 0.008 / aspect
                    sym_box = [cx - style["symbol"]["length"] / 2 / aspect - 0.004, cy - 0.015,
                               cx + style["symbol"]["length"] / 2 / aspect + 0.004, cy + 0.015]
                if _inside(sym_box, style["safe_area"]) and L._free(sym_box, t0, t1, owner):
                    elements.extend(_symbol(it["force"], [cx, cy], style, aspect))
                    L.occupy(sym_box, t0, t1, owner, "graphic")
                else:
                    L.problems.append(f"{owner}: no room for the {it['force'].lower()} symbol next to its text")
        elif kind == "HIGHLIGHT_REGION":
            r = style["region"]
            tb = it["target_boxes"][0]
            pad = r["padding"]
            box = [tb[0] - pad / aspect, tb[1] - pad, tb[2] + pad / aspect, tb[3] + pad]
            elements.append({"kind": "rect", "box": [round(v, 6) for v in box], "width": r["width"],
                             "color": style["colors"]["REGION"], "dash": [r["dash"], r["gap"]]})
            if it.get("text"):
                w, h = text_box_size(it["text"], size, style, aspect)
                g = 0.006
                cands = [[box[0], box[3] + g, box[0] + w, box[3] + g + h],             # above, left-aligned
                         [box[2] - w, box[3] + g, box[2], box[3] + g + h],             # above, right-aligned
                         [box[0], box[1] - g - h, box[0] + w, box[1] - g],             # below, left-aligned
                         [box[2] - w, box[1] - g - h, box[2], box[1] - g],             # below, right-aligned
                         [box[0] + g, box[3] - g - h, box[0] + g + w, box[3] - g]]     # inside the top-left corner
                placed = next((c for c in cands if L._free(c, t0, t1, owner)), None)
                if placed is None:
                    placed = L.place(w, h, [[box[0], box[3]]], t0, t1, owner, [box], None, 90)
                if placed is None:
                    L.problems.append(f"{owner}: no free place for '{it['text']}'")
                else:
                    L.occupy(placed, t0, t1, owner, "text")
                    boxes.append(placed)
                    elements.extend(L.plate_text(it["text"], placed, size))
        else:
            raise LayoutError(f"{owner}: unknown annotation type {kind}")
        out.append({"id": owner, "type": kind, "appear": round(t0, 4), "disappear": round(t1, 4),
                    "claim_id": it.get("claim_id"), "text": it.get("text"), "style": it.get("style"),
                    "force": it.get("force"), "direction": it.get("direction"), "anchors": it["anchors"],
                    "elements": elements, "boxes": [[round(v, 6) for v in b] for b in boxes],
                    "segments": [[[round(v, 6) for v in p] for p in s] for s in segments]})
    if tag:
        out.insert(0, tag)
    halo = style.get("halo", 0.0)
    if halo:   # a light outline under every line and arrow keeps them legible on dark parts
        for ann in out:
            els = []
            for e in ann["elements"]:
                if e["kind"] in ("line", "arrow", "rect") and not e.get("symbol"):
                    h = dict(e, color=style["colors"]["plate"], halo=True, width=e["width"] + 2 * halo if e["width"] else 0.0)
                    if e["kind"] == "arrow":
                        h.update(head_length=e["head_length"] + 2.4 * halo, head_width=e["head_width"] + 3 * halo,
                                 tip=[e["tip"][0] + (e["tip"][0] - e["tail"][0]) * 0, e["tip"][1]])
                        if not e["width"]:
                            h["width"] = 0.0
                    if e["kind"] == "line" and e.get("dash"):
                        h["dash"] = None   # one continuous halo under a dashed line
                    els.append(h)
                els.append(e)
            ann["elements"] = els
    return out, L.problems


# ---------------------------------------------------------------- checks (planner validate + Blender QA)
def check(laid, style, aspect, text_extent=None, caption_boxes=()):
    """Rule violations of a shot's laid-out annotations. text_extent(id, k) -> real text width
    (frame-width units) of the k-th text element, from Blender (None: estimates only)."""
    problems = []
    safe = style["safe_area"]
    length = style["arrow"]["length"]
    texts = []
    for ann in laid:
        for k, e in enumerate(e for e in ann["elements"] if e["kind"] in ("text", "plate")):
            if e["kind"] == "plate" or ann["type"] == "TENSION_COMPRESSION_LEGEND":
                box = e["box"]
                if not _inside(box, safe):
                    problems.append(f"{ann['id']}: OUTSIDE_SAFE_AREA {box}")
                if box[1] < style["subtitle_zone"] - 1e-9:
                    problems.append(f"{ann['id']}: IN_SUBTITLE_ZONE (bottom {box[1]:.3f} < {style['subtitle_zone']})")
        for b in ann["boxes"]:
            texts.append((ann, b))
        for e in ann["elements"]:
            for pt in [e.get("tip"), e.get("tail"), e.get("center")] + list(e.get("points") or []):
                if pt is not None and not (0.0 <= pt[0] <= 1.0 and 0.0 <= pt[1] <= 1.0):
                    problems.append(f"{ann['id']}: ELEMENT_OUTSIDE_FRAME at {pt}")
        if ann["type"] in ("LOAD_ARROW", "REACTION_ARROW"):
            for e in ann["elements"]:
                if e["kind"] != "arrow":
                    continue
                dx, dy = (e["tip"][0] - e["tail"][0]) * aspect, e["tip"][1] - e["tail"][1]
                n = math.hypot(dx, dy)
                if abs(n - length) > 1e-3:
                    problems.append(f"{ann['id']}: ARROW_LENGTH_VARIES ({n:.4f} != {length})")
                if ann["type"] == "LOAD_ARROW" and not (dy < 0 and abs(dx) < 1e-6):
                    problems.append(f"{ann['id']}: LOAD_NOT_DOWN (a load arrow must point straight down)")
                if ann["type"] == "REACTION_ARROW" and dy <= 0:
                    problems.append(f"{ann['id']}: REACTION_NOT_UP (a reaction must have an upward component)")
        for x in ann["anchors"]:
            sx, sy = x["screen"]
            if not (0.0 <= sx <= 1.0 and 0.0 <= sy <= 1.0):
                problems.append(f"{ann['id']}: ANCHOR_OUTSIDE_FRAME {x['screen']}")
    for i, (a, ba) in enumerate(texts):
        for b, bb in texts[i + 1:]:
            if a is b or a["disappear"] <= b["appear"] or b["disappear"] <= a["appear"]:
                continue
            if overlaps(ba, bb):
                problems.append(f"{a['id']} / {b['id']}: TEXT_OVERLAP")
        for cb in caption_boxes:
            if overlaps(ba, cb):
                problems.append(f"{a['id']}: OVERLAPS_CAPTION")
    if text_extent is not None:
        for ann in laid:
            for k, e in enumerate(e for e in ann["elements"] if e["kind"] == "text"):
                real = text_extent(ann["id"], k)
                if real is not None and real > (e["box"][2] - e["box"][0]) + 1e-4:
                    problems.append(f"{ann['id']}: TEXT_OVERFLOW '{e['text']}' ({real:.4f} > box {e['box'][2] - e['box'][0]:.4f})")
    return problems
