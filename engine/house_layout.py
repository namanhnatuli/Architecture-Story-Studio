"""Pure-Python layout of the legacy (M2) house base and gable roof parts (no bpy).

engine/geometry.py turns these descriptions into Blender objects; planner/ (M5.5)
rasterises the same descriptions offline for visibility estimates. One source of
numbers, so the offline proxy and the rendered model cannot drift apart.

A part is a dict: {"id", "kind", "location", "rotation", "material", "bevel", ...}
with kind "boxes" (boxes = [(local centre, dimensions)], optional clip_below_z),
"triangle" (width, rise, thickness), "gable" (outline [(x, z)], thickness),
"cylinder" (radius, length, segments) or "v_ridge" (width, height, length).
"""
import math

from engine import spec

COVERING_T = 0.105   # roof covering thickness
RAFTER_T = 0.14      # rafter depth (perpendicular to the slope)
RAFTER_W = 0.06
RIDGE_W, RIDGE_H = 0.12, 0.18
GABLE_CLEARANCE = 0.006  # gable top edge this far below the covering underside

# Covering styles (illustrative, simplified; see projects/*/research for sources).
# thickness: covering layer; eave/gable: extra overhang; ribs: (gauge, width, height) of
# course lines on the top face; ridge: shape + size of the ridge capping.
COVERING_STYLES = {
    "thatch": {"thickness": 0.30, "eave": 0.18, "gable": 0.12, "bevel": 0.05, "ribs": None,
               "ridge": ("roll", 0.17)},
    # Course gauges are exaggerated ~1.5x (stylised, readable at 640x360); slate units stay
    # about twice the size of plain tiles, as in reality (sources: slate "more effective than
    # other smaller tiles"). The covering material draws matching unit joints (scene.add_units).
    "plain_tile": {"thickness": 0.05, "eave": 0.05, "gable": 0.0, "bevel": 0.01,
                   "ribs": (0.17, 0.025, 0.012), "ridge": ("half_round", 0.085)},
    # 0.045 (was 0.025): a thinner slab let the side walls' top edge show through at the
    # eave line on 30-degree roofs (QA covering_hides_structure).
    "slate": {"thickness": 0.045, "eave": 0.04, "gable": 0.0, "bevel": 0.006,
              "ribs": (0.30, 0.02, 0.006), "ridge": ("v", (0.22, 0.10))},
}


def house_base_layout(params):
    """Parts of the rectangular house base (shared), in build order."""
    w, d, h = params["width"], params["depth"], params["wall_height"]
    out = []

    def add(cid, boxes, material, location, bevel=0.015):
        out.append({"id": cid, "kind": "boxes", "boxes": boxes, "material": material, "location": location,
                    "rotation": (0, 0, 0), "bevel": bevel})

    add("foundation", [((0, 0, 0), (w + .32, d + .32, .36))], "stone", (0, 0, -0.20))
    add("floor", [((0, 0, 0), (w, d, .10))], "wood", (0, 0, .015))
    for side, x in (("left", -w / 2), ("right", w / 2)):
        add(f"wall_{side}", [((0, 0, 0), (.17, d, h))], "plaster", (x, 0, h / 2))
    for side, y in (("front", -d / 2), ("back", d / 2)):
        add(f"wall_{side}", [((0, 0, 0), (w, .17, h))], "plaster", (0, y, h / 2))
    add("door", [((0, 0, 0), (.83, .065, 1.88))], "wood", (-.8, -d / 2 - .095, .94))
    add("door_handle", [((0, 0, 0), (.075, .04, .075))], "metal", (-.47, -d / 2 - .15, .92))
    for n, x in (("right", 1.05), ("left", -1.82)):
        add(f"window_{n}", [((0, 0, 0), (.66, .06, .79))], "window", (x, -d / 2 - .100, 1.62))
        add(f"window_{n}_frame_h", [((0, 0, 0), (.70, .06, .065))], "wood", (x, -d / 2 - .141, 1.62))
        add(f"window_{n}_frame_v", [((0, 0, 0), (.065, .06, .83))], "wood", (x, -d / 2 - .143, 1.62))
    # Ceiling joists tie the long walls; top flush with the wall top, ends embedded in the walls.
    ys = spec.rafter_positions(d, params["rafter_count"])
    add("ceiling_joists", [((0, y, 0), (w, .06, .12)) for y in ys], "wood", (0, 0, h - .06), bevel=.006)
    return out


def covering_underside_z(x, h, a, run):
    """World z of the roof covering's underside above horizontal offset x (from the ridge line)."""
    return h + 0.02 + (run - abs(x)) * math.tan(a) - (COVERING_T / 2) / math.cos(a)


def gable_outline(w, h, a, run):
    """Gable infill outline [(x, z)] whose sloped edges run parallel to, and just under, the
    covering underside: a pentagon when the underside is above the wall top at the wall
    line, else a clipped triangle."""
    top = lambda x: covering_underside_z(x, h, a, run) - GABLE_CLEARANCE
    half = w / 2
    if top(half) > h:
        return [(-half, h), (half, h), (half, top(half)), (0.0, top(0.0)), (-half, top(half))]
    x0 = run - (h + GABLE_CLEARANCE - h - 0.02 + (COVERING_T / 2) / math.cos(a)) / math.tan(a)
    return [(-x0, h), (x0, h), (0.0, top(0.0))]


def styled_covering_boxes(style, slope_len, depth, sign):
    """Covering slab (+ course ribs) in the panel's local frame.

    Local x runs along the slope (towards the eave when x has the sign of `sign`),
    local z is the outward normal; the underside stays where the M2 panel's was, so
    rafters, ridge beam and seat cuts are unchanged."""
    under = -COVERING_T / 2
    t = style["thickness"]
    length = slope_len + .12 + style["eave"]
    width = depth + .42 + 2 * style["gable"]
    eave_end = sign * ((slope_len + .12) / 2 + style["eave"])   # local x of the eave edge
    up = -sign                                                  # local x direction towards the ridge
    slab_center_x = eave_end + up * length / 2
    boxes = [((slab_center_x, 0, under + t / 2), (length, width, t))]
    if style["ribs"]:
        gauge, rib_w, rib_h = style["ribs"]
        n = int((length - gauge / 2) // gauge)
        for i in range(1, n + 1):
            x = eave_end + up * (i * gauge)
            boxes.append(((x, 0, under + t + rib_h / 2), (rib_w, width, rib_h)))
    return boxes


def ridge_cap_layout(style, a, h, rise, depth):
    """Ridge capping over the apex joint: roll (thatch), half-round tile or 'V' tile."""
    t = style["thickness"]
    top = h + rise + 0.02 + (-COVERING_T / 2 + t) / math.cos(a)   # top surface at the apex
    length = depth + .42 + 2 * style["gable"]
    shape, size = style["ridge"]
    if shape == "v":
        width, height = size
        return {"kind": "v_ridge", "width": width, "height": height, "length": length,
                "location": (0, 0, top - height * 0.45), "rotation": (0, 0, 0), "bevel": 0.006}
    radius = size
    sink = 0.35 if shape == "roll" else 0.25
    return {"kind": "cylinder", "radius": radius, "length": length, "segments": 24,
            "location": (0, 0, top - sink * radius), "rotation": (0, 0, 0), "bevel": 0.0}


def gable_roof_layout(variant, params):
    """Parts of one gable roof variant, in build order. "material": "roof" is the
    variant's colour_key; ids are f"{variant id}_{suffix}"; hint = explode direction."""
    vid = variant["id"]
    w, d, h = params["width"], params["depth"], params["wall_height"]
    a = math.radians(float(variant["roof_pitch_degrees"]))
    run = w / 2 + 0.07
    rise = run * math.tan(a)
    slope_len = run / math.cos(a)
    ys = spec.rafter_positions(d, params["rafter_count"])
    style = COVERING_STYLES[spec.covering_style(variant)] if spec.covering_style(variant) else None
    structure_inherited = bool(variant.get("structure_from"))
    out = []

    # Rafter centre line sits just under the covering's underside.
    rafter_off = -COVERING_T / 2 + 0.02 * math.cos(a) - 0.003 - RAFTER_T / 2
    s_start = 0.02
    s_end = (run - 0.065 - RAFTER_T / 2 * math.sin(a) + rafter_off * math.sin(a)) / math.cos(a)
    for side, sign in (("left", -1), ("right", 1)):
        eave_x = sign * run
        sx, sz = -sign * math.cos(a), math.sin(a)   # slope direction, eave -> ridge
        nx, nz = sign * math.sin(a), math.cos(a)     # outward roof normal
        rotation = (0, sign * a, 0)
        center = (eave_x + sx * slope_len / 2, 0, h + sz * slope_len / 2 + 0.02)
        if style is None:  # v0.1/M2 panel, unchanged
            boxes, bevel = [((0, 0, 0), (slope_len + .12, d + .42, COVERING_T))], .018
        else:
            boxes, bevel = styled_covering_boxes(style, slope_len, d, sign), style["bevel"]
        cover = {"id": f"{vid}_covering_{side}", "suffix": f"covering_{side}", "kind": "boxes", "boxes": boxes,
                 "material": "roof", "location": center, "rotation": rotation, "bevel": bevel, "hint": (nx, 0, nz)}
        if style is not None:  # local x of the eave edge: shader course joints start here
            cover["course_origin"] = sign * ((slope_len + .12) / 2 + style["eave"])
        out.append(cover)
        if structure_inherited:
            continue
        s_mid, length = (s_start + s_end) / 2, s_end - s_start
        r_center = (eave_x + sx * s_mid + nx * rafter_off, 0, h + sz * s_mid + nz * rafter_off)
        # Seat cut 1 mm above the wall top: rafters bear on the walls, never sink into them.
        out.append({"id": f"{vid}_rafters_{side}", "suffix": f"rafters_{side}", "kind": "boxes",
                    "boxes": [((0, y, 0), (length, RAFTER_W, RAFTER_T)) for y in ys], "material": "wood",
                    "location": r_center, "rotation": rotation, "bevel": .008, "clip_below_z": h + 0.001,
                    "hint": (nx, 0, nz)})

    if style is not None:
        cap = ridge_cap_layout(style, a, h, rise, d)
        cap.update(id=f"{vid}_ridge_cap", suffix="ridge_cap", material="roof", hint=(0, 0, 1))
        out.append(cap)
    if structure_inherited:
        return out

    # Ridge beam: top touches the covering underside at the beam's edges.
    top = h + (run - RIDGE_W / 2) * math.tan(a) + 0.02 - (COVERING_T / 2) / math.cos(a) - 0.004
    out.append({"id": f"{vid}_ridge_beam", "suffix": "ridge_beam", "kind": "boxes",
                "boxes": [((0, 0, 0), (RIDGE_W, d - .32, RIDGE_H))], "material": "wood",
                "location": (0, 0, top - RIDGE_H / 2), "rotation": (0, 0, 0), "bevel": .008, "hint": (0, 0, 1)})

    for side, y, hint in (("front", -d / 2 + .065, (0, -1, 0)), ("back", d / 2 - .065, (0, 1, 0))):
        part = {"id": f"{vid}_gable_{side}", "suffix": f"gable_{side}", "material": "plaster", "hint": hint,
                "rotation": (0, 0, 0), "bevel": 0, "thickness": 0.06}
        if style is None:  # v0.1/M2 triangle, unchanged
            part.update(kind="triangle", width=w, rise=rise, location=(0, y, h + rise / 3))
        else:
            part.update(kind="gable", outline=gable_outline(w, h, a, run), location=(0.0, y, 0.0))
        out.append(part)
    return out
