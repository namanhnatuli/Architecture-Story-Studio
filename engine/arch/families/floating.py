"""Floating family generators (pure Python): a concrete box pontoon with homes on it, and the bay it floats in.

Illustrative archetypes for explanation, not engineering designs. Conventions (metres): X along the platform, Y across
it, Z up with the still-water surface at z = 0. The draft is a parameter (it comes from a project's own calculation,
e.g. projects/floating-city-design-challenge/analysis/results.json), never computed or tuned here.

Section views (section = 1) keep only y >= 0 and add thin section plates on the cut (type SECTION_CUT, dark) so walls,
slabs and bulkheads read as a drawing does. A water plate under the hull (type WATER, group water_below) belongs to the
platform so it moves with it when the platform sinks or rises; the bay's own water keeps out of the hull.
Local component ids are stable; the variant id is prefixed when planned (assets.py).
"""
import math

from engine.arch import primitives as P
from engine.arch.semantic import Component

CUT_Y = (-0.04, -0.02)   # section plates sit just in front of the cut plane y = 0
DISPLACED_Y = (-0.012, -0.006)   # the displaced-water plate behind them (the cut lines stay on top)


def _box(x0, x1, y0, y1, z0, z1):
    return P.box((x1 - x0, y1 - y0, z1 - z0), ((x0 + x1) / 2.0, (y0 + y1) / 2.0, (z0 + z1) / 2.0))


def _c(cid, ctype, material, group, mesh, layer, animation=("HIGHLIGHT",), meta=None):
    return Component(id=cid, type=ctype, material=material, group=group, mesh=mesh, layer=layer, animation=animation,
                     meta=dict(meta or {}))


def block_layout(length, width, cover):
    """Four equal blocks, one per quarter, together covering `cover` of the deck, with a cross of streets between."""
    bw, bd = length * math.sqrt(cover) / 2.0, width * math.sqrt(cover) / 2.0
    return [(sx * length / 4.0 - bw / 2.0, sx * length / 4.0 + bw / 2.0, sy * width / 4.0 - bd / 2.0, sy * width / 4.0 + bd / 2.0)
            for sx in (-1, 1) for sy in (-1, 1)]


def platform(p):
    """A box pontoon (bottom, perimeter walls, bulkhead grid, deck) floating at `draft_m`, with low-rise blocks.

    Optional parts the story switches on and off with SEQUENCE steps: storeys up to `storeys`, a roof cap for every
    storey count from 2 up (inset so a lower cap hides inside the storey above), and a hull extension of `extension_m`
    below the bottom (walls and bulkheads; the bottom itself is moved by the story)."""
    L, B, H, T = p["length_m"], p["width_m"], p["hull_depth_m"], p["draft_m"]
    slab, wall, bh, spacing = p["slab_m"], p["wall_m"], p["bulkhead_m"], p["bulkhead_spacing_m"]
    section = bool(p["section"])
    zb, zt = -T, H - T
    y0 = 0.0 if section else -B / 2.0
    comps = [_c("hull_bottom", "HULL", "concrete", "hull", _box(-L / 2, L / 2, y0, B / 2, zb, zb + slab), 0)]
    walls = [("hull_wall_west", -L / 2, -L / 2 + wall, y0, B / 2), ("hull_wall_east", L / 2 - wall, L / 2, y0, B / 2),
             ("hull_wall_north", -L / 2, L / 2, B / 2 - wall, B / 2)]
    if not section:
        walls.append(("hull_wall_south", -L / 2, L / 2, -B / 2, -B / 2 + wall))
    for cid, x0, x1, ya, yb in walls:
        comps.append(_c(cid, "HULL", "concrete", "hull", _box(x0, x1, ya, yb, zb, zt), 0))
    nx, ny = int(round(L / spacing)), int(round(B / spacing))
    xs = [-L / 2 + i * spacing for i in range(1, nx)]
    ys = [-B / 2 + j * spacing for j in range(1, ny) if not section or -B / 2 + j * spacing > 0.5]
    for i, x in enumerate(xs, 1):
        comps.append(_c(f"bulkhead_x{i}", "BULKHEAD", "concrete", "bulkheads", _box(x - bh / 2, x + bh / 2, y0, B / 2, zb + slab, zt - slab), 1))
    for j, y in enumerate(ys, 1):
        comps.append(_c(f"bulkhead_y{j}", "BULKHEAD", "concrete", "bulkheads", _box(-L / 2, L / 2, y - bh / 2, y + bh / 2, zb + slab, zt - slab), 1))
    comps.append(_c("deck", "DECK", "concrete_deck", "deck", _box(-L / 2, L / 2, y0, B / 2, zt - slab, zt), 2))
    ext = p["extension_m"]
    if ext > 0:   # the deeper hull of the design revision: walls and bulkheads grow below the present bottom
        for cid, x0, x1, ya, yb in walls:
            comps.append(_c(cid.replace("hull_wall", "hull_ext"), "HULL", "concrete", "hull_extension",
                            _box(x0, x1, ya, yb, zb - ext, zb), 0))
        for i, x in enumerate(xs, 1):
            comps.append(_c(f"hull_ext_bulkhead_x{i}", "BULKHEAD", "concrete", "hull_extension",
                            _box(x - bh / 2, x + bh / 2, y0, B / 2, zb - ext, zb), 1))
    if section:   # section plates on the cut, the displaced water, and the water below the hull
        cy0, cy1 = CUT_Y
        cuts = [("cut_bottom", -L / 2, L / 2, zb, zb + slab), ("cut_deck", -L / 2, L / 2, zt - slab, zt),
                ("cut_wall_west", -L / 2, -L / 2 + wall, zb, zt), ("cut_wall_east", L / 2 - wall, L / 2, zb, zt)]
        cuts += [(f"cut_bulkhead_x{i}", x - bh / 2, x + bh / 2, zb + slab, zt - slab) for i, x in enumerate(xs, 1)]
        for cid, x0, x1, z0, z1 in cuts:
            group = "hull_bottom_cut" if cid == "cut_bottom" else "section_cut"
            comps.append(_c(cid, "SECTION_CUT", "section_poche", group, _box(x0, x1, cy0, cy1, z0, z1), 3))
        if ext > 0:
            ext_cuts = [("cut_ext_wall_west", -L / 2, -L / 2 + wall), ("cut_ext_wall_east", L / 2 - wall, L / 2)]
            ext_cuts += [(f"cut_ext_bulkhead_x{i}", x - bh / 2, x + bh / 2) for i, x in enumerate(xs, 1)]
            for cid, x0, x1 in ext_cuts:
                comps.append(_c(cid, "SECTION_CUT", "highlight_gold", "hull_extension_cut",
                                _box(x0, x1, cy0, cy1, zb - ext, zb), 3))
        dy0, dy1 = DISPLACED_Y
        comps.append(_c("displaced_volume", "DISPLACED_VOLUME", "displaced_water", "displaced",
                        _box(-L / 2, L / 2, dy0, dy1, zb, 0.0), 3,
                        meta={"note": "the outer hull below the waterline: L x B x draft of water pushed aside"}))
        depth = p["water_depth_m"]
        comps.append(_c("water_below", "WATER", "water_cut", "water_below",
                        _box(-L / 2, L / 2, cy0, cy1, -depth - 1.0, zb), 0, animation=("STATIC",)))   # stays behind the seabed cut while the platform moves
    for k, (x0, x1, ya, yb) in enumerate(block_layout(L, B, p["building_cover"]), 1):
        if section and yb <= 0.0:
            continue
        ya = max(ya, 0.0) if section else ya
        for s in range(1, p["storeys"] + 1):
            z0, z1 = zt + (s - 1) * p["storey_height_m"], zt + s * p["storey_height_m"]
            comps.append(_c(f"block{k}_storey{s}", "BUILDING", "plaster", f"storey_{s}", _box(x0, x1, ya, yb, z0, z1), 4 + s))
            if s >= 2:   # a roof cap for this storey count, inset so it hides inside the storey above
                comps.append(_c(f"block{k}_roof{s}", "ROOF", "roof_membrane", f"roof_{s}",
                                _box(x0 + 0.05, x1 - 0.05, ya + (0.0 if section and ya == 0.0 else 0.05), yb - 0.05, z1, z1 + 0.3), 4 + s))
    return comps


def bay(p):
    """Still water (z <= 0) over a seabed, optionally cut at y = 0 with section plates, and with the footprint of
    one platform (`hole_length_m` x `hole_width_m`, centred) kept dry in section so the hull interior reads as air."""
    W, D, depth = p["site_width_m"], p["site_length_m"], p["water_depth_m"]
    section = bool(p["section"])
    y0 = 0.0 if section else -D / 2.0
    comps = [_c("seabed", "GROUND", "seabed", "seabed", _box(-W / 2, W / 2, y0, D / 2, -depth - 1.5, -depth), 0, ("STATIC",))]
    hl, hw = p["hole_length_m"], p["hole_width_m"]
    if not section or hl <= 0:
        comps.append(_c("water", "WATER", "water", "water", _box(-W / 2, W / 2, y0, D / 2, -depth, 0.0), 0, ("STATIC",)))
        return comps
    pieces = [("water_west", -W / 2, -hl / 2, 0.0, D / 2), ("water_east", hl / 2, W / 2, 0.0, D / 2),
              ("water_north", -hl / 2, hl / 2, hw / 2, D / 2)]
    for cid, x0, x1, ya, yb in pieces:
        comps.append(_c(cid, "WATER", "water", "water", _box(x0, x1, ya, yb, -depth, 0.0), 0, ("STATIC",)))
    cy0, cy1 = CUT_Y
    for cid, x0, x1 in (("water_cut_west", -W / 2, -hl / 2), ("water_cut_east", hl / 2, W / 2)):
        comps.append(_c(cid, "WATER", "water_cut", "water_cut", _box(x0, x1, cy0, cy1, -depth, 0.0), 1, ("STATIC",)))
    comps.append(_c("seabed_cut", "GROUND", "seabed_cut", "seabed", _box(-W / 2, W / 2, cy0 - 0.01, cy1 + 0.01, -depth - 1.5, -depth), 1, ("STATIC",)))
    comps.append(_c("waterline", "WATER", "section_poche", "waterline", _box(-W / 2, W / 2, cy0 - 0.02, cy0, -0.04, 0.04), 2, ("STATIC",)))
    return comps


EXPLODE_LIFT = {"BUILDING": 14.0, "ROOF": 14.0, "DECK": 8.0, "BULKHEAD": 4.0}   # metres up; the hull shell stays


def explode_offsets(comps):
    """Layers lift straight up, in the order the mass sits: buildings, deck, bulkheads; the hull shell stays."""
    return {c.id: (0.0, 0.0, EXPLODE_LIFT[c.type]) for c in comps if c.type in EXPLODE_LIFT}


def compatibility_errors(p):
    errors = []
    if p["draft_m"] >= p["hull_depth_m"]:
        errors.append(f"draft_m {p['draft_m']} must be less than hull_depth_m {p['hull_depth_m']} (no freeboard)")
    if p["draft_m"] + p["extension_m"] >= p["water_depth_m"]:
        errors.append("the hull would touch the seabed")
    for key, size in (("length_m", p["length_m"]), ("width_m", p["width_m"])):
        n = size / p["bulkhead_spacing_m"]
        if abs(n - round(n)) > 1e-6:
            errors.append(f"{key} {size} is not a whole number of bulkhead spacings ({p['bulkhead_spacing_m']})")
    if 2 * p["slab_m"] >= p["hull_depth_m"]:
        errors.append("slabs leave no room inside the hull")
    return errors
