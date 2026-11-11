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


def _hull(prefix, group, L, B, H, T, slab, wall, bh, spacing, ya, yb, south, north, skip_y=()):
    """Bottom, perimeter walls, bulkheads and deck of a box hull between y = ya and y = yb (a whole hull, or the half on
    one side of a section). south / north: whether that wall is built. Returns (components, walls, bulkhead xs)."""
    zb, zt = -T, H - T
    comps = [_c(f"{prefix}hull_bottom", "HULL", "concrete", group, _box(-L / 2, L / 2, ya, yb, zb, zb + slab), 0)]
    walls = [(f"{prefix}hull_wall_west", -L / 2, -L / 2 + wall, ya, yb), (f"{prefix}hull_wall_east", L / 2 - wall, L / 2, ya, yb)]
    if north:
        walls.append((f"{prefix}hull_wall_north", -L / 2, L / 2, yb - wall, yb))
    if south:
        walls.append((f"{prefix}hull_wall_south", -L / 2, L / 2, ya, ya + wall))
    for cid, x0, x1, y0, y1 in walls:
        comps.append(_c(cid, "HULL", "concrete", group, _box(x0, x1, y0, y1, zb, zt), 0))
    nx, ny = int(round(L / spacing)), int(round(B / spacing))
    xs = [-L / 2 + i * spacing for i in range(1, nx)]
    ys = [y for y in (-B / 2 + j * spacing for j in range(1, ny)) if ya + 0.5 < y < yb - 0.5 and y not in skip_y]
    bgroup = "bulkheads" if not prefix else group
    for i, x in enumerate(xs, 1):
        comps.append(_c(f"{prefix}bulkhead_x{i}", "BULKHEAD", "concrete", bgroup, _box(x - bh / 2, x + bh / 2, ya, yb, zb + slab, zt - slab), 1))
    for j, y in enumerate(ys, 1):
        comps.append(_c(f"{prefix}bulkhead_y{j}", "BULKHEAD", "concrete", bgroup, _box(-L / 2, L / 2, y - bh / 2, y + bh / 2, zb + slab, zt - slab), 1))
    comps.append(_c(f"{prefix}deck", "DECK", "concrete_deck", "deck" if not prefix else group, _box(-L / 2, L / 2, ya, yb, zt - slab, zt), 2))
    return comps, walls, xs


def platform(p):
    """A box pontoon (bottom, perimeter walls, bulkhead grid, deck) floating at `draft_m`, with low-rise blocks.

    Optional parts the story switches on and off with SEQUENCE steps: storeys up to `storeys` (each with its windows
    and floor line), a roof cap for every storey count from 2 up (inset so a lower cap hides inside the storey above),
    and a hull extension of `extension_m` below the bottom (walls and bulkheads; the bottom itself is moved by the
    story). Section: the half at y >= 0 with plates on the cut and the drawing's marks (draft and freeboard dimensions,
    the outline of the water pushed aside, dashed lines at the deck's and the bottom's first levels); front_half adds
    the other half and the water in front of it, which the story removes to show the cut."""
    L, B, H, T = p["length_m"], p["width_m"], p["hull_depth_m"], p["draft_m"]
    slab, wall, bh, spacing = p["slab_m"], p["wall_m"], p["bulkhead_m"], p["bulkhead_spacing_m"]
    section = bool(p["section"])
    zb, zt = -T, H - T
    y0 = 0.0 if section else -B / 2.0
    comps, walls, xs = _hull("", "hull", L, B, H, T, slab, wall, bh, spacing, y0, B / 2, south=not section, north=True,
                             skip_y=(0.0,) if section else ())
    ext = p["extension_m"]
    if ext > 0:   # the deeper hull of the design revision: walls and bulkheads grow below the present bottom
        ext_mat = "highlight_gold" if section else "concrete"   # in section the added depth reads as one gold band
        for cid, x0, x1, ya, yb in walls:
            comps.append(_c(cid.replace("hull_wall", "hull_ext"), "HULL", ext_mat, "hull_extension", _box(x0, x1, ya, yb, zb - ext, zb), 0))
        for i, x in enumerate(xs, 1):
            comps.append(_c(f"hull_ext_bulkhead_x{i}", "BULKHEAD", ext_mat, "hull_extension",
                            _box(x - bh / 2, x + bh / 2, y0, B / 2, zb - ext, zb), 1))
    if section:
        comps += _section_marks(p, L, B, T, zb, zt, slab, wall, bh, xs, ext)
    if p.get("test_load") and not section:   # B11: a 100 t load the story slides toward the edge, along the street
        side = round((p["test_load_t"] / LOAD_DENSITY_T_M3 / LOAD_HEIGHT_M) ** 0.5, 3)
        zl = zt + PATH_H
        comps.append(_c("test_load", "LOAD", "highlight_gold", "load", _box(-side / 2, side / 2, -side / 2, side / 2, zl, zl + LOAD_HEIGHT_M), 3,
                        meta={"mass_t": p["test_load_t"], "note": "a concrete block of this mass, for the tilt example"}))
        x0, x1 = side / 2 + 0.3, side / 2 + p["test_load_shift_m"]
        comps.append(_c("load_path", "MARKER", "highlight_gold", "load",
                        P.merge(_box(x0, x1 - 1.2, -0.2, 0.2, zl, zl + 0.03), _tri_prism(x1 - 1.2, x1, 0.8, zl, zl + 0.03)), 3,
                        meta={"note": f"the {p['test_load_shift_m']} m the load moves"}))
        comps.append(_c("level_ref", "MARKER", "section_poche", "reference", _level_ref(L, B, zt), 3, animation=("STATIC",),
                        meta={"note": "the deck's level before the tilt (a dashed line in front, the deck's outline)"}))
    if p.get("neighbours") and not section:   # B12: four copies arrive around a small basin (the neighbourhood's U)
        pitch_x, pitch_y = L + p["neighbour_gap_m"], B + p["neighbour_gap_m"]
        for k, (i, j) in enumerate([ij for ij in NEIGHBOURHOOD if ij != (0, 0)], 1):
            comps += _platform_set(f"neighbour{k}", L, B, H, T, p["building_cover"], 3, i * pitch_x, j * pitch_y,
                                   group=f"neighbour{k}")
    if not section:
        comps.append(_c("paths", "DECORATION", "paving", "paths", _paths_mesh("home", L, B, zt), 2))
    front = section and p.get("front_half")
    if front:   # the half in front of the cut (y < 0), its blocks, and the water and seabed in front of it
        fc, _, _ = _hull("front_", "front_half", L, B, H, T, slab, wall, bh, spacing, -B / 2, 0.0, south=True, north=False,
                         skip_y=(0.0,))
        comps += fc
        fw, fd, depth = p["front_width_m"], p["front_depth_m"], p["water_depth_m"]
        for cid, x0, x1, ya, yb in (("front_water_west", -fw / 2, -L / 2, -fd, FRONT_Y), ("front_water_east", L / 2, fw / 2, -fd, FRONT_Y),
                                    ("front_water_south", -L / 2, L / 2, -fd, -B / 2)):
            comps.append(_c(cid, "WATER", "water", "front_water", _box(x0, x1, ya, yb, -depth, 0.0), 0, animation=("STATIC",)))
        comps.append(_c("front_seabed", "GROUND", "seabed", "front_water", _box(-fw / 2, fw / 2, -fd, FRONT_Y, -depth - 1.5, -depth), 0,
                        animation=("STATIC",)))
    for k, (x0, x1, ya, yb) in enumerate(block_layout(L, B, p["building_cover"]), 1):
        in_front = section and yb <= 0.0
        if in_front and not front:
            continue
        prefix, grp_ = ("front_", "front_half") if in_front else ("", None)
        ya = max(ya, 0.0) if section and not in_front else ya
        door_face = ("y", yb, 1) if (ya + yb) / 2 < 0 else ("y", ya, -1)   # the entrance faces the street across the platform
        for s in range(1, p["storeys"] + 1):
            z0, z1 = zt + (s - 1) * p["storey_height_m"], zt + s * p["storey_height_m"]
            g = grp_ or f"storey_{s}"
            comps.append(_c(f"{prefix}block{k}_storey{s}", "BUILDING", "plaster", g, _box(x0, x1, ya, yb, z0, z1), 4 + s))
            comps.append(_c(f"{prefix}block{k}_storey{s}_windows", "DECORATION", "window_dark", g,
                            _facade([(x0, x1, ya, yb)], z0, 1, p["storey_height_m"], doors=[door_face] if s == 1 else [],
                                    first_storey=s), 4 + s))
            if s >= 2:   # a roof cap for this storey count, inset so it hides inside the storey above
                comps.append(_c(f"{prefix}block{k}_roof{s}", "ROOF", "roof_membrane", grp_ or f"roof_{s}",
                                _box(x0 + 0.05, x1 - 0.05, ya + (0.0 if section and ya == 0.0 else 0.05), yb - 0.05, z1, z1 + 0.3), 4 + s))
    return comps


def _section_marks(p, L, B, T, zb, zt, slab, wall, bh, xs, ext):
    """The section's plates on the cut and the drawing's marks."""
    comps = []
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
            comps.append(_c(cid, "SECTION_CUT", "highlight_gold", "hull_extension_cut", _box(x0, x1, cy0, cy1, zb - ext, zb), 3))
    f0, f1 = FRONT_MARK_Y
    t = OUTLINE_T   # the water pushed aside: an outline around the hull below the waterline, drawn in front of the water
    outline = P.merge(_box(-L / 2 - t, -L / 2, f0, f1, zb - t, 0.0), _box(L / 2, L / 2 + t, f0, f1, zb - t, 0.0),
                      _box(-L / 2 - t, L / 2 + t, f0, f1, zb - t, zb))
    comps.append(_c("displaced_volume", "DISPLACED_VOLUME", "displaced_water", "displaced", outline, 3,
                    meta={"note": "outline of the hull below the waterline: L x B x draft of water pushed aside"}))
    x = -L / 2 - DIM_OFFSET   # the draft as a dimension: waterline to the bottom, ticks at both ends
    comps.append(_c("draft_dim", "MARKER", "section_poche", "dimensions",
                    P.merge(_box(x - DIM_W / 2, x + DIM_W / 2, f0, f1, zb, 0.0), _box(x - 0.45, x + 0.45, f0, f1, -DIM_TICK, 0.0),
                            _box(x - 0.45, x + 0.45, f0, f1, zb, zb + DIM_TICK)), 3, animation=("STATIC",)))
    m0, m1 = MARKER_Y   # the freeboard: a line hanging from a tick level with the deck, hidden below the waterline by the
    xm = L / 2 + 0.55     # water's cut plate, so the part that shows is the freeboard
    comps.append(_c("freeboard_marker", "MARKER", "highlight_gold", "freeboard",
                    P.merge(_box(xm - DIM_W / 2, xm + DIM_W / 2, m0, m1, zt - FREEBOARD_MARKER_H, zt),
                            _box(L / 2, L / 2 + 1.0, m0, m1, zt - DIM_TICK, zt)), 3,
                    meta={"note": "moves with the hull; below the waterline the water's cut plate hides it"}))
    r0, r1 = REF_Y
    comps.append(_c("deck_ref", "MARKER", "section_poche", "reference", _dashes(-L / 2 - 1.5, L / 2 + 1.5, r0, r1, zt - 0.03, zt + 0.03), 3,
                    animation=("STATIC",), meta={"note": "the deck's level before a change (dashed)"}))
    comps.append(_c("bottom_ref", "MARKER", "section_poche", "reference", _dashes(-L / 2 - 1.5, L / 2 + 1.5, r0, r1, zb - 0.03, zb + 0.03), 3,
                    animation=("STATIC",), meta={"note": "the bottom's level before a change (dashed)"}))
    depth = p["water_depth_m"]
    comps.append(_c("water_below", "WATER", "water_cut", "water_below",
                    _box(-L / 2, L / 2, cy0, cy1, -depth - 1.0, zb), 0, animation=("STATIC",)))   # behind the seabed cut while the platform moves
    return comps


def _dashes(x0, x1, y0, y1, z0, z1, dash=0.8, gap=0.5):
    out, x = [], x0
    while x < x1 - 1e-9:
        out.append(_box(x, min(x + dash, x1), y0, y1, z0, z1))
        x += dash + gap
    return P.merge(*out)


def _tri_prism(x0, x1, half_w, z0, z1):
    """An arrow head pointing +x: a flat triangle from x0 (base, +-half_w) to x1 (tip), z0..z1."""
    verts = [(x0, -half_w, z0), (x1, 0.0, z0), (x0, half_w, z0), (x0, -half_w, z1), (x1, 0.0, z1), (x0, half_w, z1)]
    faces = [(0, 2, 1), (3, 4, 5), (0, 1, 4, 3), (1, 2, 5, 4), (2, 0, 3, 5)]
    return {"verts": verts, "faces": faces}


def _level_ref(L, B, zt):
    """B11's references: a dashed line at the deck's first level in front of the platform, reaching past both ends, and
    the outline of the deck's edges at that level."""
    y = -B / 2
    line = _dashes(-L / 2 - 5.0, L / 2 + 5.0, y - 0.06, y, zt - 0.05, zt + 0.05, dash=1.2, gap=0.6)
    edge = P.merge(_box(-L / 2, L / 2, B / 2 - 0.12, B / 2, zt, zt + 0.04), _box(-L / 2, -L / 2 + 0.12, -B / 2, B / 2, zt, zt + 0.04),
                   _box(L / 2 - 0.12, L / 2, -B / 2, B / 2, zt, zt + 0.04))
    return P.merge(line, edge)


# ---------------------------------------------------------------- facades, paths and the uses of a platform
WINDOW_W, WINDOW_H, WINDOW_SILL, WINDOW_PITCH, PANE = 1.4, 1.5, 0.9, 3.0, 0.05
SHOP_W, SHOP_H, SHOP_SILL = 2.4, 2.3, 0.3
LINE_H, LINE_OUT = 0.14, 0.06
DOOR_W, DOOR_H = 2.0, 2.4
PATH_H = 0.03


def _subtract(interval, covered):
    lo, hi = interval
    parts = [(lo, hi)]
    for c0, c1 in covered:
        nxt = []
        for a, b in parts:
            if c1 <= a or c0 >= b:
                nxt.append((a, b))
                continue
            if c0 > a:
                nxt.append((a, c0))
            if c1 < b:
                nxt.append((c1, b))
        parts = nxt
    return parts


def _faces(rects):
    """Exposed faces of touching, non-overlapping footprint rectangles: [(axis, coord, lo, hi, outward sign)]; a face on
    x = coord spans y lo..hi (axis 'x'), a face on y = coord spans x lo..hi (axis 'y')."""
    out = []
    for i, (x0, x1, y0, y1) in enumerate(rects):
        for axis, coord, lo, hi, sign in (("x", x0, y0, y1, -1), ("x", x1, y0, y1, 1), ("y", y0, x0, x1, -1), ("y", y1, x0, x1, 1)):
            covered = []
            for j, (a0, a1, b0, b1) in enumerate(rects):
                if j == i:
                    continue
                if axis == "x" and abs((a1 if sign < 0 else a0) - coord) < 1e-6:
                    covered.append((b0, b1))
                if axis == "y" and abs((b1 if sign < 0 else b0) - coord) < 1e-6:
                    covered.append((a0, a1))
            out += [(axis, coord, a, b, sign) for a, b in _subtract((lo, hi), covered) if b - a > 1.0]
    return out


def _pane(axis, coord, sign, u0, u1, z0, z1, out=PANE):
    a, b = sorted((coord, coord + sign * out))
    return _box(a, b, u0, u1, z0, z1) if axis == "x" else _box(u0, u1, a, b, z0, z1)


def _on(face_list, axis, coord, sign):
    return any(f[0] == axis and abs(f[1] - coord) < 1e-6 and f[2] == sign for f in face_list)


def _facade(rects, z0, storeys, h, doors=(), first_storey=1, shop=False, window=None, door_pitch=None, no_lines=()):
    """Windows (a pane every pitch along every exposed face), a floor line at the foot of every storey above the
    first, and doors with a canopy on the given faces [(axis, coord, sign)], for storeys first_storey.. of a building.
    window: (width, height, sill, pitch); door_pitch: a door every so many metres along a door face (a terrace's
    houses) instead of one in the middle; no_lines: faces whose floor lines the balconies replace."""
    ww, wwh, wsill, pitch = window or (WINDOW_W, WINDOW_H, WINDOW_SILL, WINDOW_PITCH)
    out = []
    for axis, coord, lo, hi, sign in _faces(rects):
        length = hi - lo
        mid = (lo + hi) / 2
        door_cs = []
        if _on(doors, axis, coord, sign) and length >= 5.0:
            n_d = max(1, int(length // door_pitch)) if door_pitch else 1
            door_cs = [mid + (i - (n_d - 1) / 2) * (door_pitch or 0.0) for i in range(n_d)]
        lines = not _on(no_lines, axis, coord, sign)
        for k in range(storeys):
            s = first_storey + k
            zs = z0 + k * h
            if s >= 2 and lines:
                out.append(_pane(axis, coord, sign, lo, hi, zs - LINE_H / 2, zs + LINE_H / 2, LINE_OUT))
            w, wh, sill = (SHOP_W, SHOP_H, SHOP_SILL) if (shop and s == 1) else (ww, wwh, wsill)
            n = int((length - 1.0) // pitch)
            for i in range(n):
                c = mid + (i - (n - 1) / 2) * pitch
                if s == 1 and any(abs(c - dc) < (DOOR_W + w) / 2 + 0.3 for dc in door_cs):
                    continue
                out.append(_pane(axis, coord, sign, c - w / 2, c + w / 2, zs + sill, zs + sill + wh))
            if s == 1:
                for dc in door_cs:
                    out.append(_pane(axis, coord, sign, dc - DOOR_W / 2, dc + DOOR_W / 2, zs + PATH_H + 0.02, zs + DOOR_H))   # above the paving
                    out.append(_pane(axis, coord, sign, dc - DOOR_W / 2 - 0.4, dc + DOOR_W / 2 + 0.4, zs + DOOR_H + 0.2, zs + DOOR_H + 0.35, 1.2))
    return P.merge(*out) if out else _box(0, 0.01, 0, 0.01, z0, z0 + 0.01)


def use_layout(use, L, B, cover, orient="x"):
    """Footprint rectangles of a platform's buildings by use; every use covers the same share of the deck with the same
    storeys, so the load, and the draft, stay those of the calculation."""
    area = cover * L * B
    if use in ("home", "mixed"):
        return block_layout(L, B, cover)
    if use == "school":   # a U around a yard that opens to the +y edge
        W, D = 0.9 * L, 0.6 * B
        t = ((W + 2 * D) - math.sqrt((W + 2 * D) ** 2 - 8 * area)) / 4
        return [(-W / 2, W / 2, -D / 2, -D / 2 + t), (-W / 2, -W / 2 + t, -D / 2 + t, D / 2), (W / 2 - t, W / 2, -D / 2 + t, D / 2)]
    if use == "clinic":   # a ring around a courtyard
        a = 0.733 * L
        c = math.sqrt(a * a - area)
        return [(-a / 2, a / 2, -a / 2, -c / 2), (-a / 2, a / 2, c / 2, a / 2), (-a / 2, -c / 2, -c / 2, c / 2), (c / 2, a / 2, -c / 2, c / 2)]
    if use == "community":   # two long halls either side of a street
        length, gap = 0.9 * L, 2.0
        w = area / (2 * length)
        if orient == "x":
            return [(-length / 2, length / 2, gap, gap + w), (-length / 2, length / 2, -gap - w, -gap)]
        return [(gap, gap + w, -length / 2, length / 2), (-gap - w, -gap, -length / 2, length / 2)]
    raise ValueError(f"unknown use {use!r}")


USE_LOOK = {   # walls, roof
    "home": ("plaster", "roof_membrane"), "mixed": ("plaster", "roof_membrane"), "school": ("plaster_school", "roof_school"),
    "clinic": ("plaster_clinic", "roof_clinic"), "community": ("plaster_service", "roof_green")}


def _paths_mesh(use, L, B, z, orient="x", rects=None):
    """Paving on the deck: the streets between the buildings, stopping short of the edges where walkways land."""
    e = L / 2 - 1.2
    w = 1.75
    if use in ("home", "mixed"):
        boxes = [(-e, e, -w, w), (-w, w, -e, e)]
    elif use == "school":
        base_top = rects[0][3]
        boxes = [(-w, w, base_top, e), (-e, e, rects[0][2] - (rects[0][2] + B / 2) / 2 - w, rects[0][2] - (rects[0][2] + B / 2) / 2 + w)]
    elif use == "clinic":
        a, c = rects[1][3], rects[1][2]
        boxes = [(a, e, -w, w), (-e, -a, -w, w), (-w, w, a, e), (-w, w, -e, -a), (-c + 1.0, c - 1.0, -c + 1.0, c - 1.0)]
    else:   # community
        boxes = [(-e, e, -w, w)] if orient == "x" else [(-w, w, -e, e)]
    return P.merge(*[_box(x0, x1, y0, y1, z, z + PATH_H) for x0, x1, y0, y1 in boxes])


def _cone(cx, cy, z0, r, h, n=8):
    verts = [(cx + r * math.cos(2 * math.pi * k / n), cy + r * math.sin(2 * math.pi * k / n), z0) for k in range(n)] + [(cx, cy, z0 + h)]
    faces = [tuple(reversed(range(n)))] + [(k, (k + 1) % n, n) for k in range(n)]
    return {"verts": verts, "faces": faces}


def _trees(L, B, z):
    """Lawn along the open edges of the deck and trees on it (a park around the lagoon)."""
    e0, e1 = L / 2 - 4.6, L / 2 - 0.4    # the strip between the buildings and the edge
    lawns = []
    for sx in (-1, 1):
        a, b = sorted((sx * e0, sx * e1))
        lawns += [_box(a, b, 3.0, e1, z, z + PATH_H), _box(a, b, -e1, -3.0, z, z + PATH_H)]
    for sy in (-1, 1):
        a, b = sorted((sy * e0, sy * e1))
        lawns += [_box(3.0, e0, a, b, z, z + PATH_H), _box(-e0, -3.0, a, b, z, z + PATH_H)]
    trees = []
    zt = z + PATH_H
    for sx in (-1, 1):
        for sy in (-1, 1):
            for u, v in ((L / 2 - 2.5, 8.0), (L / 2 - 2.5, 19.0), (8.0, L / 2 - 2.5), (19.0, L / 2 - 2.5)):
                x, y = sx * u, sy * v
                trees += [P.cylinder_z(0.22, 1.6, 6, (x, y, zt + 0.8)), _cone(x, y, zt + 1.4, 1.5, 4.2)]
    return P.merge(*lawns), P.merge(*trees)


def _playground(rects, z):
    """A play court and three play structures in a school's yard."""
    yard_x = rects[1][1]          # inner face of the west wing
    y0 = rects[0][3]              # the yard starts at the base's inner face
    court = _box(yard_x + 1.0, -2.5, y0 + 6.0, y0 + 22.0, z, z + PATH_H)
    play = [_box(3.0, 5.0, y0 + 7.0, y0 + 9.0, z, z + 2.2), _box(6.5, 9.5, y0 + 12.0, y0 + 13.0, z, z + 1.2),
            _box(3.5, 8.5, y0 + 17.0, y0 + 18.2, z, z + 0.6)]
    return P.merge(court, *play)


# ---------------------------------------------------------------- home building types
# Every type covers the same share of the deck with the same storeys (the load and the draft of the calculation), keeps
# its footprint centred on the deck (no list), and keeps the cross streets on both axes open, where the walkways land.
STREET_CLEAR = 3.5   # buildings keep this far from both axes
EDGE_CLEAR = 2.5     # and this far from the deck's edges
LAWN_FROM = 1.75     # lawns start at the paving's edge (the streets are 3.5 m wide)
BALCONY_D = 1.4
HOME_KINDS = ("blocks", "terrace", "courtyard", "villas", "pinwheel", "garden")
KIND_LOOK = {   # walls, roof, windows (width, height, sill, pitch)
    "blocks": ("plaster", "roof_membrane", None),
    "terrace": ("brick_pale", "roof_slate", (1.2, 1.6, 0.8, 3.0)),
    "courtyard": ("plaster", "roof_membrane", (0.9, 1.9, 0.6, 2.2)),
    "villas": ("timber_clad", "roof_zinc", (2.4, 1.9, 0.5, 4.5)),
    "pinwheel": ("plaster_light", "roof_membrane", (1.8, 2.1, 0.3, 3.0)),
    "garden": ("plaster_light", "roof_membrane", (1.8, 2.1, 0.3, 3.0)),
}
KIND_EXTRAS = {   # the optional DECORATION parts of each type (besides facade and paving)
    "blocks": (), "terrace": ("lawn", "trees"), "courtyard": ("solar", "lawn", "trees"), "villas": ("lawn", "trees"),
    "pinwheel": ("balconies", "lawn", "trees"), "garden": ("balconies", "lawn", "trees", "furniture", "lamps", "playground")}
EXTRA_MATERIAL = {"balconies": "balcony", "solar": "pv_panel", "lawn": "park_lawn", "trees": "tree", "furniture": "timber_light",
                  "lamps": "steel_dark", "playground": "court_play"}
LAGOON_TURN = {"+y": 0, "-x": 1, "-y": 2, "+x": 3}   # quarter turns (counter-clockwise) of the garden drawn facing +y


def _mirror4(rect):
    """A rectangle in the +x +y quadrant and its mirror images in the other three."""
    x0, x1, y0, y1 = rect
    return [(x0, x1, y0, y1), (-x1, -x0, y0, y1), (x0, x1, -y1, -y0), (-x1, -x0, -y1, -y0)]


def _mirror_pts(pts):
    return [(sx * x, sy * y) + tuple(rest) for x, y, *rest in pts for sx in (1, -1) for sy in (1, -1)]


def _rect_minus(rect, holes):
    """Cells of `rect` not covered by any hole (a grid on all their edges), as non-overlapping rectangles."""
    x0, x1, y0, y1 = rect
    xs = sorted({x0, x1} | {min(max(v, x0), x1) for h in holes for v in h[:2]})
    ys = sorted({y0, y1} | {min(max(v, y0), y1) for h in holes for v in h[2:]})
    out = []
    for a, b in zip(xs, xs[1:]):
        for c, d in zip(ys, ys[1:]):
            mx, my = (a + b) / 2, (c + d) / 2
            if b - a > 0.2 and d - c > 0.2 and not any(h[0] < mx < h[1] and h[2] < my < h[3] for h in holes):
                out.append((a, b, c, d))
    return out


def _sloped_box(x0, x1, y0, y1, z0, top):
    """A box whose top corners sit at top(x, y): a pitched roof's wedge."""
    corners = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    verts = [(x, y, z0) for x, y in corners] + [(x, y, top(x, y)) for x, y in corners]
    faces = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    return {"verts": verts, "faces": faces}


def _gable(rect, z, rise, over=0.3):
    """A gable roof on a rectangle, the ridge along its long side, with eaves overhanging by `over`."""
    x0, x1, y0, y1 = rect[0] - over, rect[1] + over, rect[2] - over, rect[3] + over
    if x1 - x0 >= y1 - y0:
        ym = (y0 + y1) / 2
        verts = [(x0, y0, z), (x1, y0, z), (x1, y1, z), (x0, y1, z), (x0, ym, z + rise), (x1, ym, z + rise)]
    else:
        xm = (x0 + x1) / 2
        verts = [(x0, y1, z), (x0, y0, z), (x1, y0, z), (x1, y1, z), (xm, y1, z + rise), (xm, y0, z + rise)]
    return {"verts": verts, "faces": [(0, 3, 2, 1), (0, 1, 5, 4), (2, 3, 4, 5), (1, 2, 5), (3, 0, 4)]}


def _mono(rect, z, rise, high, over=0.3, eave=0.3):
    """A single-pitch roof rising toward `high` ('+x', '-x', '+y', '-y'), eave edge `eave` thick."""
    x0, x1, y0, y1 = rect[0] - over, rect[1] + over, rect[2] - over, rect[3] + over
    axis, sign = high[1], 1 if high[0] == "+" else -1
    lo_, hi_ = (x0, x1) if axis == "x" else (y0, y1)

    def top(x, y):
        u = (x if axis == "x" else y) - lo_
        t = u / (hi_ - lo_)
        return z + eave + rise * (t if sign > 0 else 1.0 - t)
    return _sloped_box(x0, x1, y0, y1, z, top)


def _balconies(faces, storeys, h, inset=1.0):
    """A slab with a parapet in front of each face [(axis, coord, sign, lo, hi)] at every storey above the first."""
    out = []
    for axis, coord, sign, lo, hi in faces:
        for s in range(2, storeys + 1):
            z = (s - 1) * h
            out.append(_pane(axis, coord, sign, lo + inset, hi - inset, z - 0.2, z, BALCONY_D))
            out.append(_pane(axis, coord + sign * (BALCONY_D - 0.08), sign, lo + inset, hi - inset, z, z + 1.0, 0.08))
    return P.merge(*out)


def _solar(rects, z, pitch=1.7, size=1.0):
    """Rows of solar panels across each roof wing (flat, dark), leaving a metre at the edges."""
    out = []
    for x0, x1, y0, y1 in rects:
        along_x = x1 - x0 >= y1 - y0
        lo, hi = (x0, x1) if along_x else (y0, y1)
        n = int((hi - lo - 2.0) // pitch)
        for i in range(n):
            c = lo + 1.0 + size / 2 + i * pitch
            out.append(_box(c - size / 2, c + size / 2, y0 + 1.0, y1 - 1.0, z, z + 0.12) if along_x
                       else _box(x0 + 1.0, x1 - 1.0, c - size / 2, c + size / 2, z, z + 0.12))
    return P.merge(*out)


def _tree(x, y, z, scale=1.0):
    return [P.cylinder_z(0.22 * scale, 1.6 * scale, 6, (x, y, z + 0.8 * scale)), _cone(x, y, z + 1.4 * scale, 1.5 * scale, 4.2 * scale)]


def _bench(x, y, z, facing):
    """A park bench 1.8 m long; `facing` is the direction a seated person looks ('+x', '-x', '+y', '-y')."""
    along_x = facing[1] == "y"
    s = 1 if facing[0] == "+" else -1
    parts = []
    for u0, u1, v0, v1, z0, z1 in ((-0.9, 0.9, -0.25, 0.25, 0.4, 0.48), (-0.9, 0.9, -0.3, -0.22, 0.48, 0.9),
                                   (-0.8, -0.7, -0.22, 0.22, 0.0, 0.4), (0.7, 0.8, -0.22, 0.22, 0.0, 0.4)):
        v0, v1 = (v0, v1) if s > 0 else (-v1, -v0)   # the back on the side away from where it faces
        parts.append(_box(x + u0, x + u1, y + v0, y + v1, z + z0, z + z1) if along_x else _box(x + v0, x + v1, y + u0, y + u1, z + z0, z + z1))
    return parts


def _picnic(x, y, z):
    """A picnic table with its two benches (1.8 x 1.6 m)."""
    return [_box(x - 0.9, x + 0.9, y - 0.4, y + 0.4, z + 0.7, z + 0.76), _box(x - 0.1, x + 0.1, y - 0.3, y + 0.3, z, z + 0.7),
            _box(x - 0.9, x + 0.9, y - 0.8, y - 0.55, z + 0.42, z + 0.47), _box(x - 0.9, x + 0.9, y + 0.55, y + 0.8, z + 0.42, z + 0.47),
            _box(x - 0.1, x + 0.1, y - 0.8, y - 0.55, z, z + 0.42), _box(x - 0.1, x + 0.1, y + 0.55, y + 0.8, z, z + 0.42)]


def _lamp(x, y, z, arm=(0.0, 1.0)):
    """A street lamp: a pole, an arm toward `arm` (a unit direction in plan) and the lantern under its end."""
    ax, ay = x + 0.7 * arm[0], y + 0.7 * arm[1]
    return [P.cylinder_z(0.08, 4.2, 6, (x, y, z + 2.1)), _bar((x, y, z + 4.15), (ax, ay, z + 4.15), 0.1, 0.1),
            _box(ax - 0.22, ax + 0.22, ay - 0.22, ay + 0.22, z + 3.95, z + 4.1)]


def _crown(x, y, z, r, segs=7, rings=4):
    """A round tree crown: a low-poly ball of radius r whose lowest point is at z."""
    cz = z + r
    verts = [(x, y, cz - r)]
    for i in range(1, rings):
        a = math.pi * i / rings - math.pi / 2
        verts += [(x + r * math.cos(a) * math.cos(2 * math.pi * k / segs), y + r * math.cos(a) * math.sin(2 * math.pi * k / segs),
                   cz + r * math.sin(a)) for k in range(segs)]
    verts.append((x, y, cz + r))
    top = len(verts) - 1
    faces = [(0, 1 + (k + 1) % segs, 1 + k) for k in range(segs)]
    for i in range(rings - 2):
        b0, b1 = 1 + i * segs, 1 + (i + 1) * segs
        faces += [(b0 + k, b0 + (k + 1) % segs, b1 + (k + 1) % segs, b1 + k) for k in range(segs)]
    last = 1 + (rings - 2) * segs
    faces += [(last + k, last + (k + 1) % segs, top) for k in range(segs)]
    return {"verts": verts, "faces": faces}


def _round_tree(x, y, z, scale=1.0):
    return [P.cylinder_z(0.22 * scale, 2.0 * scale, 6, (x, y, z + 1.0 * scale)), _crown(x, y, z + 1.7 * scale, 1.9 * scale)]


def _play_set(x0, x1, y0, y1, z):
    """Timber play equipment on a play court: a swing frame (two A-frames, a beam, two seats on ropes) and a slide
    tower (four posts, a deck, a ramp)."""
    out = []
    xc, ya, yb = x0 + 1.2, y0 + 0.6, y0 + 3.6
    for y in (ya, yb):
        # legs start 2 cm up: a slanted bar's lower corners would otherwise dip into the court
        out += [_bar((xc - 0.9, y, z + 0.02), (xc, y, z + 2.4), 0.1, 0.1), _bar((xc + 0.9, y, z + 0.02), (xc, y, z + 2.4), 0.1, 0.1)]
    out.append(_bar((xc, ya, z + 2.4), (xc, yb, z + 2.4), 0.12, 0.12))
    for y in (ya + 1.0, yb - 1.0):
        out.append(_box(xc - 0.12, xc + 0.12, y - 0.25, y + 0.25, z + 0.5, z + 0.55))
        for dy in (-0.22, 0.22):
            out.append(_bar((xc, y + dy, z + 0.55), (xc, y + dy, z + 2.34), 0.03, 0.03))
    tx, ty = x1 - 1.0, y1 - 1.6
    for px in (tx - 0.6, tx + 0.6):
        for py in (ty - 0.6, ty + 0.6):
            out.append(_box(px - 0.06, px + 0.06, py - 0.06, py + 0.06, z, z + 2.4))
    out.append(_box(tx - 0.66, tx + 0.66, ty - 0.66, ty + 0.66, z + 1.5, z + 1.6))
    out.append(_bar((tx, ty - 0.66, z + 1.55), (tx, ty - 3.2, z + 0.05), 0.6, 0.06))
    return out


def _turn(mesh, quarter):
    """Rotate a mesh by quarter turns (counter-clockwise) about the platform's centre (winding is kept)."""
    q = quarter % 4
    if q == 0:
        return mesh
    rot = {1: lambda x, y: (-y, x), 2: lambda x, y: (-x, -y), 3: lambda x, y: (y, -x)}[q]
    return {"verts": [rot(x, y) + (z,) for x, y, z in mesh["verts"]], "faces": mesh["faces"]}


def home_layout(kind, L, B, cover, storeys=3, h=3.0):
    """A home platform's buildings by type, drawn for a garden opening toward +y (turned afterwards):
    {rects, roofs: [mesh], doors, door_pitch, balconies: [faces], solar: [rects], lawns, trees: [(x, y, scale)],
    benches: [(x, y, facing)], picnic: [(x, y)], lamps: [(x, y)], play: [rects]}."""
    A = cover * L * B
    q0, qx, qy = STREET_CLEAR, L / 2 - EDGE_CLEAR, B / 2 - EDGE_CLEAR
    sx, sy = qx - q0, qy - q0
    zr = storeys * h
    out = {"rects": [], "roofs": [], "doors": [], "door_pitch": None, "balconies": [], "solar": [], "lawns": [], "trees": [],
           "benches": [], "picnic": [], "lamps": [], "play": [], "promenade": [], "round_trees": []}
    quad = (q0, qx, q0, qy)
    if kind == "blocks":
        out["rects"] = block_layout(L, B, cover)
        out["doors"] = [("y", y1, 1) if (y0 + y1) / 2 < 0 else ("y", y0, -1) for x0, x1, y0, y1 in out["rects"]]
        out["roofs"] = [_box(x0 + 0.05, x1 - 0.05, y0 + 0.05, y1 - 0.05, zr, zr + 0.3) for x0, x1, y0, y1 in out["rects"]]
        return out
    if kind == "terrace":   # rows of houses with gable roofs, a door every 6 m; back gardens between two rows
        nb = 2 if sy >= 20.0 else 1
        d = A / (4 * nb * sx)
        rows = [(q0, qx, q0, q0 + d)] + ([(q0, qx, qy - d, qy)] if nb == 2 else [])
        for r in rows:
            out["rects"] += _mirror4(r)
        out["doors"] = [("y", q0, -1), ("y", -q0, 1)] + ([("y", qy, 1), ("y", -qy, -1)] if nb == 2 else [])
        out["door_pitch"] = 6.0
        out["roofs"] = [_gable(r, zr, 0.5 * d / 2) for r in out["rects"]]
        gardens = _rect_minus(quad, rows)
        out["lawns"] = [m for g in gardens for m in _mirror4(g)]
        if nb == 2:
            out["trees"] = _mirror_pts([(q0 + 0.3 * sx, q0 + d + (sy - 2 * d) / 2, 0.8), (q0 + 0.7 * sx, q0 + d + (sy - 2 * d) / 2, 0.8)])
        return out
    if kind == "courtyard":   # a ring of four L-shaped wings around a garden, gates on the axes, solar panels
        a, g = min(qx, qy) - 1.5, 5.0
        k = 8 * a - 4 * g
        d = (k - math.sqrt(k * k - 16 * A)) / 8
        wing = [(g / 2, a, a - d, a), (a - d, a, g / 2, a - d)]
        for r in wing:
            out["rects"] += _mirror4(r)
        out["doors"] = [("y", a, 1), ("y", -a, -1), ("x", a, 1), ("x", -a, -1)]
        out["roofs"] = [_box(x0 + 0.05, x1 - 0.05, y0 + 0.05, y1 - 0.05, zr, zr + 0.3) for x0, x1, y0, y1 in out["rects"]]
        out["solar"] = out["rects"]
        inner = a - d
        out["lawns"] = _mirror4((LAWN_FROM, inner, LAWN_FROM, inner))
        out["round_trees"] = _mirror_pts([((LAWN_FROM + inner) / 2, (LAWN_FROM + inner) / 2, 1.0)])
        return out
    if kind == "villas":   # two houses a quadrant, staggered, single-pitch roofs facing each other, timber
        w = (sx - 3.0) / 2
        dh = A / 8 / w
        if dh > sy:
            w = (sx - 2.0) / 2
            dh = A / 8 / w
        stagger = max(0.0, min(3.0, sy - dh))
        houses = [(q0, q0 + w, q0 + stagger, q0 + stagger + dh), (qx - w, qx, q0, q0 + dh)]
        for r in houses:
            out["rects"] += _mirror4(r)
        out["doors"] = [("y", q0 + stagger, -1), ("y", q0, -1), ("y", -q0 - stagger, 1), ("y", -q0, 1)]
        for x0, x1, y0, y1 in out["rects"]:
            inner_x = "+x" if (x0 + x1) / 2 < 0 else "-x"
            outer = (abs(x0 + x1) / 2) > (q0 + qx) / 2
            high = ("-" if inner_x == "+x" else "+") + "x" if outer else inner_x   # the pair's roofs rise toward the gap
            out["roofs"].append(_mono((x0, x1, y0, y1), zr, 0.18 * w, high))
        out["lawns"] = [m for g in _rect_minus(quad, houses) for m in _mirror4(g)]
        trees = []
        for x0, x1, y0, y1 in houses:
            if qy - y1 >= 3.5:
                trees.append(((x0 + x1) / 2, y1 + (qy - y1) / 2, 0.8))
        out["round_trees"] = _mirror_pts(trees)
        return out
    if kind == "pinwheel":   # four bars turning about the centre, balconies on their long faces
        d = A / (4 * sx)
        bars = [(q0, qx, q0, q0 + d), (-q0 - d, -q0, q0, qy), (-qx, -q0, -q0 - d, -q0), (q0, q0 + d, -qy, -q0)]
        out["rects"] = bars
        out["doors"] = [("y", q0, -1), ("x", -q0, 1), ("y", -q0, 1), ("x", q0, -1)]
        out["door_pitch"] = 8.0
        out["roofs"] = [_box(x0 + 0.05, x1 - 0.05, y0 + 0.05, y1 - 0.05, zr, zr + 0.3) for x0, x1, y0, y1 in bars]
        out["balconies"] = [("y", q0 + d, 1, q0, qx), ("y", q0, -1, q0, qx), ("x", -q0 - d, -1, q0, qy), ("x", -q0, 1, q0, qy),
                            ("y", -q0 - d, -1, -qx, -q0), ("y", -q0, 1, -qx, -q0), ("x", q0 + d, 1, -qy, -q0), ("x", q0, -1, -qy, -q0)]
        quads = [(q0, qx, q0, qy), (-qx, -q0, q0, qy), (-qx, -q0, -qy, -q0), (q0, qx, -qy, -q0)]
        for qd, bar in zip(quads, bars):
            out["lawns"] += _rect_minus(qd, [bar])
        free = sy - d - BALCONY_D
        if free >= 4.0:   # a row of trees in each quadrant's open strip, clear of the balconies
            v = q0 + d + BALCONY_D + free / 2
            for u in (q0 + 0.2 * sx, q0 + 0.5 * sx, q0 + 0.8 * sx):
                out["trees"] += [(u, v, 0.9), (-v, u, 0.9), (-u, -v, 0.9), (v, -u, 0.9)]
        return out
    if kind == "garden":   # homes on both sides of a garden that runs to the water (+y): lawn, trees, seats, play
        d = A / (4 * sy)
        bar = (qx - d, qx, q0, qy)
        out["rects"] = _mirror4(bar)
        gx = qx - d    # the garden's half-width
        out["doors"] = [("x", gx, -1), ("x", -gx, 1)]
        out["door_pitch"] = 6.0
        out["roofs"] = [_box(x0 + 0.05, x1 - 0.05, y0 + 0.05, y1 - 0.05, zr, zr + 0.3) for x0, x1, y0, y1 in out["rects"]]
        out["balconies"] = [("x", gx, -1, q0, qy), ("x", -gx, 1, q0, qy), ("x", gx, -1, -qy, -q0), ("x", -gx, 1, -qy, -q0)]
        prom = B / 2 - 3.5                    # the waterside promenade: 3.5 m in the garden, the deck's edge strip beyond
        out["promenade"] = [(-gx, gx, prom, B / 2 - 0.4), (-L / 2 + 0.4, -gx, qy, B / 2 - 0.4), (gx, L / 2 - 0.4, qy, B / 2 - 0.4)]
        out["play"] = [(3.5, 7.0, -18.0, -11.0)]
        for sgn in (1, -1):   # lawn on both halves: up to the promenade on the water side, round the play court on the other
            out["lawns"].append(tuple(sorted((sgn * LAWN_FROM, sgn * gx))) + (LAWN_FROM, prom))
            out["lawns"] += _rect_minus(tuple(sorted((sgn * LAWN_FROM, sgn * gx))) + (-qy, -LAWN_FROM), out["play"])
        tx = gx - BALCONY_D - 2.1
        out["trees"] = _mirror_pts([(tx, 7.0, 1.0), (tx, 21.0, 1.0)])
        out["round_trees"] = _mirror_pts([(tx, 14.0, 1.0)])
        out["benches"] = [(sgn * 3.0, y, ("-x" if sgn > 0 else "+x")) for sgn in (1, -1) for y in (8.0, 18.0, -8.0, -18.0)]
        out["benches"] += [(x, B / 2 - 2.0, "+y") for x in (-8.0, -4.0, 4.0, 8.0)]
        out["picnic"] = [(6.0, 17.0), (-6.0, 17.0)]
        out["lamps"] = [(sgn * 2.6, y, (-sgn, 0.0)) for sgn in (1, -1) for y in (13.0, -13.0)] + \
                       [(x, B / 2 - 0.9, (0.0, -1.0)) for x in (-10.0, -6.0, 6.0, 10.0)]
        return out
    raise ValueError(f"unknown home type {kind!r}")


def home_parts(kind, L, B, H, T, cover, storeys, turn=0, shop=False):
    """{part: (component type, material, mesh)} of a home platform of this type in the platform's own frame (deck top at
    z = 0), turned by quarter turns: buildings, roofs, facade, paving and the type's extras (KIND_EXTRAS)."""
    lay = home_layout(kind, L, B, cover, storeys)
    walls, roof_mat, window = KIND_LOOK[kind]
    h = 3.0
    rects = lay["rects"]
    no_lines = [(f[0], f[1], f[2]) for f in lay["balconies"]]
    parts = {"buildings": ("BUILDING", walls, P.merge(*[_box(x0, x1, y0, y1, 0.0, storeys * h) for x0, x1, y0, y1 in rects])),
             "roofs": ("ROOF", roof_mat, P.merge(*lay["roofs"])),
             "facade": ("DECORATION", "window_dark", _facade(rects, 0.0, storeys, h, doors=lay["doors"], shop=shop, window=window,
                                                              door_pitch=lay["door_pitch"], no_lines=no_lines))}
    e, w = L / 2 - 1.2, 1.75
    paths = [_box(-e, e, -w, w, 0.0, PATH_H), _box(-w, w, -e, e, 0.0, PATH_H)] + [_box(*r, 0.0, PATH_H) for r in lay["promenade"]]
    parts["paths"] = ("DECORATION", "paving", P.merge(*paths))
    z = PATH_H
    extras = {"balconies": lambda: _balconies(lay["balconies"], storeys, h),
              "solar": lambda: _solar(lay["solar"], storeys * h + 0.3),
              "lawn": lambda: P.merge(*[_box(*r, 0.0, PATH_H) for r in lay["lawns"]]),
              "trees": lambda: P.merge(*[m for x, y, s in lay["trees"] for m in _tree(x, y, z, s)],
                                       *[m for x, y, s in lay["round_trees"] for m in _round_tree(x, y, z, s)]),
              "furniture": lambda: P.merge(*[m for x, y, f in lay["benches"] for m in _bench(x, y, z, f)],
                                           *[m for x, y in lay["picnic"] for m in _picnic(x, y, z)],
                                           *[m for r in lay["play"] for m in _play_set(*r, z)]),
              "lamps": lambda: P.merge(*[m for x, y, arm in lay["lamps"] for m in _lamp(x, y, z, arm)]),
              "playground": lambda: P.merge(*[_box(x0, x1, y0, y1, 0.0, PATH_H) for x0, x1, y0, y1 in lay["play"]])}
    for name in KIND_EXTRAS[kind]:
        mesh = extras[name]()
        if mesh["verts"]:
            parts[name] = ("DECORATION", EXTRA_MATERIAL[name], mesh)
    return {k: (t, m, _turn(mesh, turn)) for k, (t, m, mesh) in parts.items()}


def home_extras(kind, L, B, cover, storeys=3):
    """The optional parts a home type brings at this platform size (some have no room for trees on a 40 m deck)."""
    if kind == "blocks":
        return ()
    return tuple(name for name in KIND_EXTRAS[kind] if name in home_parts(kind, L, B, 0.0, 0.0, cover, storeys))


def set_counts(use, kind="blocks", park=False, L=60.0, B=60.0, cover=0.4, storeys=3):
    """Component types of one built platform (_platform_set with storeys > 0)."""
    out = {"HULL": 1, "DECK": 1, "BUILDING": 1, "ROOF": 1}
    if use == "home" and kind != "blocks":
        out["DECORATION"] = 2 + len(home_extras(kind, L, B, cover, storeys))
    else:
        out["DECORATION"] = 2 + (use == "school") + 2 * bool(park)
    return out


def _platform_set(prefix, L, B, H, T, cover, storeys, cx, cy, use="home", group=None, orient="x", park=False, kind="blocks",
                  turn=0):
    """One platform as a few merged components placed at (cx, cy): hull, deck, buildings, roofs, facades (windows, floor
    lines, entrances), paving, and by use a playground or a park; identical platforms share their meshes.
    use: home | mixed (shops below, homes above) | school | clinic | community. kind: the home type (HOME_KINDS); a type
    other than blocks brings its own gardens; turn: quarter turns of the type (a garden opens toward +y unturned)."""
    g = group or prefix
    zt = H - T
    parts = [_placed(f"{prefix}_hull", "HULL", "concrete", g, _local_box(L, B, H - 0.25, -(H - 0.25) / 2.0), (cx, cy, zt - 0.25), 0),
             _placed(f"{prefix}_deck", "DECK", "concrete_deck", g, _local_box(L, B, 0.25, -0.125), (cx, cy, zt), 1)]
    if storeys <= 0:
        return parts
    if use == "home" and kind != "blocks":
        layer = {"buildings": 2, "roofs": 2}
        for name, (ctype, mat, mesh) in home_parts(kind, L, B, H, T, cover, storeys, turn).items():
            parts.append(_placed(f"{prefix}_{name}", ctype, mat, g, mesh, (cx, cy, zt), layer.get(name, 3),
                                 meta={"use": use, "type": kind} if name == "buildings" else None))
        return parts
    rects = use_layout(use, L, B, cover, orient)
    h = storeys * 3.0
    walls, roofs = USE_LOOK[use]
    body = P.merge(*[_box(x0, x1, y0, y1, 0.0, h) for x0, x1, y0, y1 in rects])
    roof = P.merge(*[_box(x0 + 0.05, x1 - 0.05, y0 + 0.05, y1 - 0.05, h, h + 0.3) for x0, x1, y0, y1 in rects])
    if use in ("home", "mixed"):   # each block's entrance faces the street across the middle
        doors = [("y", y1, 1) if (y0 + y1) / 2 < 0 else ("y", y0, -1) for x0, x1, y0, y1 in rects]
        facade = P.merge(*[_facade([r], 0.0, storeys, 3.0, doors=[d], shop=use == "mixed") for r, d in zip(rects, doors)])
    else:
        x0, x1, y0, y1 = max(rects, key=lambda r: (r[1] - r[0]) * (r[3] - r[2]))
        door = ("y", y1, 1) if use != "community" or orient == "x" else ("x", x1, 1)
        facade = _facade(rects, 0.0, storeys, 3.0, doors=[door])
    meta = {"use": use}
    parts.append(_placed(f"{prefix}_buildings", "BUILDING", walls, g, body, (cx, cy, zt), 2, meta=meta))
    parts.append(_placed(f"{prefix}_roofs", "ROOF", roofs, g, roof, (cx, cy, zt), 2))
    parts.append(_placed(f"{prefix}_facade", "DECORATION", "window_dark", g, facade, (cx, cy, zt), 3))
    parts.append(_placed(f"{prefix}_paths", "DECORATION", "paving", g, _paths_mesh(use, L, B, 0.0, orient, rects), (cx, cy, zt), 3))
    if use == "school":
        parts.append(_placed(f"{prefix}_playground", "DECORATION", "court_play", g, _playground(rects, 0.0), (cx, cy, zt), 3))
    if park:
        lawn, trees = _trees(L, B, 0.0)
        parts.append(_placed(f"{prefix}_lawn", "DECORATION", "park_lawn", g, lawn, (cx, cy, zt), 3))
        parts.append(_placed(f"{prefix}_trees", "DECORATION", "tree", g, trees, (cx, cy, zt), 3))   # standing on the lawn
    return parts


def _sloped_slab(x0, x1, y0, y1, z_top0, z_top1, z_bottom):
    """A slab whose top falls linearly along Y from z_top0 (at y0) to z_top1 (at y1): a sloping seabed."""
    verts = [(x0, y0, z_bottom), (x1, y0, z_bottom), (x1, y1, z_bottom), (x0, y1, z_bottom),
             (x0, y0, z_top0), (x1, y0, z_top0), (x1, y1, z_top1), (x0, y1, z_top1)]
    faces = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    return {"verts": verts, "faces": faces}


def bay(p):
    """Still water (z <= 0) over a seabed, optionally cut at y = 0 with section plates, and with the footprint of
    one platform (`hole_length_m` x `hole_width_m`, centred) kept dry in section so the hull interior reads as air.
    With shore = 1 the land and a quay lie at y < 0 and the site extends from y = 0 towards the sea; the seabed then
    slopes from water_depth_m at the quay to depth_far_m at the far edge (when depth_far_m > water_depth_m)."""
    W, D, depth = p["site_width_m"], p["site_length_m"], p["water_depth_m"]
    section, shore = bool(p["section"]), bool(p["shore"])
    far = max(depth, p["depth_far_m"])
    y0 = 0.0 if (section or shore) else -D / 2.0
    y1 = D if shore else D / 2.0
    comps = []
    if shore:
        q = p["quay_level_m"]
        comps.append(_c("land", "GROUND", "earth_bank", "shore", _box(-W / 2, W / 2, -p["land_depth_m"], 0.0, -far - 1.5, q), 0, ("STATIC",)))
    if far > depth:
        comps.append(_c("seabed", "GROUND", "seabed", "seabed", _sloped_slab(-W / 2, W / 2, y0, y1, -depth, -far, -far - 1.5), 0, ("STATIC",)))
    else:
        comps.append(_c("seabed", "GROUND", "seabed", "seabed", _box(-W / 2, W / 2, y0, y1, -depth - 1.5, -depth), 0, ("STATIC",)))
    hl, hw = p["hole_length_m"], p["hole_width_m"]
    if not section or hl <= 0:
        comps.append(_c("water", "WATER", "water", "water", _box(-W / 2, W / 2, y0, y1, -far, 0.0), 0, ("STATIC",)))
        return comps
    pieces = [("water_west", -W / 2, -hl / 2, 0.0, y1), ("water_east", hl / 2, W / 2, 0.0, y1),
              ("water_north", -hl / 2, hl / 2, hw / 2, y1)]
    for cid, x0, x1, ya, yb in pieces:
        comps.append(_c(cid, "WATER", "water", "water", _box(x0, x1, ya, yb, -depth, 0.0), 0, ("STATIC",)))
    cy0, cy1 = CUT_Y
    for cid, x0, x1 in (("water_cut_west", -W / 2, -hl / 2), ("water_cut_east", hl / 2, W / 2)):
        comps.append(_c(cid, "WATER", "water_cut", "water_cut", _box(x0, x1, cy0, cy1, -depth, 0.0), 1, ("STATIC",)))
    comps.append(_c("seabed_cut", "GROUND", "seabed_cut", "seabed", _box(-W / 2, W / 2, cy0 - 0.01, cy1 + 0.01, -depth - 1.5, -depth), 1, ("STATIC",)))
    comps.append(_c("waterline", "WATER", "section_poche", "waterline", _box(-W / 2, W / 2, cy0 - 0.02, cy0, -0.04, 0.04), 2, ("STATIC",)))
    return comps


FREEBOARD_MARKER_H = 1.3     # m; longer than any freeboard the story shows (1.146 m)
MARKER_Y = (-0.016, -0.006)  # just behind the water's cut plate (CUT_Y), in front of the hull
REF_Y = (-0.005, -0.001)     # dashed reference lines, between the marker and the hull
FRONT_MARK_Y = (-0.075, -0.065)   # marks that stay visible over the water: in front of its cut plate
FRONT_Y = -0.08              # the water in front of the cut ends here
DIM_W, DIM_TICK, DIM_OFFSET, OUTLINE_T = 0.12, 0.08, 1.2, 0.15
LOAD_DENSITY_T_M3, LOAD_HEIGHT_M = 2.4, 2.6

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


def _bar(p0, p1, width, height):
    """A bar from p0 to p1 whose `width` lies horizontal and across it (a walkway plank, a cable, a pipe)."""
    ux, uy = p1[0] - p0[0], p1[1] - p0[1]
    side = (-uy, ux, 0.0) if abs(ux) + abs(uy) > 1e-9 else (1.0, 0.0, 0.0)
    return P.member(p0, p1, width, height, side)


# ---------------------------------------------------------------- many platforms (shared meshes, placed by location)
def _local_box(sx, sy, sz, cz=0.0):
    return P.box((sx, sy, sz), (0.0, 0.0, cz))


def _placed(cid, ctype, material, group, mesh, loc, layer, animation=("HIGHLIGHT",), meta=None):
    c = _c(cid, ctype, material, group, mesh, layer, animation, meta)
    c.location = tuple(loc)
    return c


def _walkway(cid, x0, y0, z0, x1, y1, z1, width, group="walkways", hinged=True):
    """A walkway between two deck edges (it tilts when the decks differ), with hinge pins at both ends."""
    import math as _m
    dx, dy, dz = x1 - x0, y1 - y0, z1 - z0
    length = _m.sqrt(dx * dx + dy * dy + dz * dz)
    deck = _bar((x0, y0, z0 + 0.12), (x1, y1, z1 + 0.12), width, 0.24)
    comps = [_c(cid, "WALKWAY", "timber_light", group, deck, 3)]
    if hinged:
        horizontal = (-dy, dx, 0.0)
        n = _m.hypot(*horizontal[:2]) or 1.0
        hx, hy = horizontal[0] / n * width / 2.0, horizontal[1] / n * width / 2.0
        for k, (px, py, pz) in enumerate(((x0, y0, z0), (x1, y1, z1))):
            comps.append(_c(f"{cid}_hinge{k}", "CONNECTOR", "steel_dark", group,
                            _bar((px - hx, py - hy, pz + 0.15), (px + hx, py + hy, pz + 0.15), 0.3, 0.3), 3))
    return comps


def pair(p):
    """Two identical hulls side by side along X with different buildings, each at its own calculated draft, and a
    hinged walkway between their deck edges (B13: different loads put the decks at different heights)."""
    L, B, H, gap = p["length_m"], p["width_m"], p["hull_depth_m"], p["gap_m"]
    xa, xb = -(L + gap) / 2.0, (L + gap) / 2.0
    comps = _platform_set("platform_a", L, B, H, p["draft_a_m"], p["building_cover"], p["storeys_a"], xa, 0.0)
    comps += _platform_set("platform_b", L, B, H, p["draft_b_m"], p["building_cover"], p["storeys_b"], xb, 0.0)
    za, zb = H - p["draft_a_m"], H - p["draft_b_m"]
    comps += _walkway("walkway", xa + L / 2.0, -B / 4.0, za, xb - L / 2.0, -B / 4.0, zb, 3.0)
    return comps


NEIGHBOURHOOD = [(-1, 0), (0, 0), (1, 0), (-1, 1), (1, 1)]   # a U of five platforms around a small basin (0, 1)
NEIGHBOURHOOD_KINDS = {   # home types of the five platforms, in NEIGHBOURHOOD order
    "blocks": ("blocks",) * 5,
    "varied": ("terrace", "courtyard", "villas", "pinwheel", "blocks"),
    "varied_garden": ("terrace", "garden", "courtyard", "villas", "pinwheel")}   # (0, 0) opens onto the basin (60 m decks)


def neighbourhood(p):
    """Five platforms around a small basin with gaps, hinged walkways, flexible utility links and fenders, held by
    piles (moorings = piles) or by mooring lines to anchors on the seabed (moorings = lines)."""
    L, B, H, T, gap = p["length_m"], p["width_m"], p["hull_depth_m"], p["draft_m"], p["gap_m"]
    pitch_x, pitch_y = L + gap, B + gap
    zt = H - T
    storeys = [int(s) for s in str(p["storeys_pattern"]).split(",")]
    kinds = NEIGHBOURHOOD_KINDS[p.get("home_types", "blocks")]
    comps, centres = [], {}
    for k, (i, j) in enumerate(NEIGHBOURHOOD, 1):
        cx, cy = i * pitch_x, j * pitch_y
        centres[(i, j)] = (cx, cy)
        comps += _platform_set(f"platform{k}", L, B, H, T, p["building_cover"], storeys[(k - 1) % len(storeys)], cx, cy,
                               group=f"platform{k}", kind=kinds[k - 1])
    joints = [((-1, 0), (0, 0)), ((0, 0), (1, 0)), ((-1, 0), (-1, 1)), ((1, 0), (1, 1))]
    for n, (a, b) in enumerate(joints, 1):
        (ax, ay), (bx, by) = centres[a], centres[b]
        if ay == by:   # side by side along X
            x0, x1, y = ax + L / 2.0, bx - L / 2.0, ay + B / 4.0
            comps += _walkway(f"joint{n}_walkway", x0, y, zt, x1, y, zt, 3.0, group=f"joint{n}")
            comps.append(_c(f"joint{n}_utility", "UTILITY_LINE", "utility_flex", f"joint{n}",
                            _bar((x0, y - 3.0, zt - 0.6), (x1, y - 3.0, zt - 0.6), 0.5, 0.5), 3))
            for s in (-1, 1):
                comps.append(_c(f"joint{n}_fender{'ab'[s > 0]}", "CONNECTOR", "fender", f"joint{n}",
                                _box(x0 if s < 0 else x1 - 0.5, x0 + 0.5 if s < 0 else x1, y - 8, y - 5, zt - 1.5, zt - 0.3), 3))
        else:          # one behind the other along Y
            y0, y1, x = ay + B / 2.0, by - B / 2.0, ax
            comps += _walkway(f"joint{n}_walkway", x, y0, zt, x, y1, zt, 3.0, group=f"joint{n}")
            comps.append(_c(f"joint{n}_utility", "UTILITY_LINE", "utility_flex", f"joint{n}",
                            _bar((x + 3.0, y0, zt - 0.6), (x + 3.0, y1, zt - 0.6), 0.5, 0.5), 3))
    depth = p["water_depth_m"]
    if p["moorings"] in ("piles", "both"):
        for k, (i, j) in enumerate(NEIGHBOURHOOD, 1):
            cx, cy = centres[(i, j)]
            for s, (sx, sy) in enumerate(((-1, -1), (1, 1)), 1):
                px, py = cx + sx * (L / 2.0 + 1.4), cy + sy * (B / 2.0 - 4.0)
                comps.append(_c(f"platform{k}_pile{s}", "MOORING_PILE", "steel", "piles",
                                P.cylinder_z(0.6, depth + 1.5 + zt + 3.0, 16, (px, py, (zt + 3.0 - depth - 1.5) / 2.0)), 4))
                comps.append(_c(f"platform{k}_pile{s}_guide", "CONNECTOR", "steel_dark", "piles",
                                _box(min(px, cx + sx * L / 2.0) - (0.0 if sx > 0 else 0.0), max(px, cx + sx * L / 2.0),
                                     py - 0.9, py + 0.9, zt - 0.6, zt - 0.1), 4))
    if p["moorings"] in ("lines", "both"):   # both: the story swaps piles for lines (B24)
        for k, (i, j) in enumerate(NEIGHBOURHOOD, 1):
            cx, cy = centres[(i, j)]
            for s, sy in enumerate((-1, 1), 1):
                fx, fy, fz = cx, cy + sy * (B / 2.0 + 0.25), -T + 0.5
                ax, ay, az = cx, cy + sy * (B / 2.0 + p["line_reach_m"]), -depth + 1.5
                pts = []
                for q in range(9):   # a drawn sag (not a computed catenary)
                    t = q / 8.0
                    pts.append((fx, fy + (ay - fy) * t, max(fz + (az - fz) * t - 3.0 * (4 * t * (1 - t)) * 0.5, -depth + 1.0)))
                mesh = P.merge(*[_bar(a, b, 0.5, 0.5) for a, b in zip(pts, pts[1:])])
                comps.append(_c(f"platform{k}_line{s}", "MOORING_LINE", "cable_dark", "lines", mesh, 4,
                                meta={"note": "conceptual mooring, not sized; drawn sag"}))
                comps.append(_c(f"platform{k}_anchor{s}", "ANCHOR", "steel_dark", "anchors",
                                _box(ax - 2.0, ax + 2.0, ay - 2.0, ay + 2.0, -depth, -depth + 1.5), 4,
                                meta={"note": "conceptual anchor, not sized"}))
    return comps


def clay_boat(p):
    """B05, in section: the hull's concrete as one solid block on the seabed, beside the same concrete shaped as a
    hollow box floating at its calculated draft (hull only)."""
    L, B, H, T = p["length_m"], p["width_m"], p["hull_depth_m"], p["draft_m"]
    side, depth = p["block_side_m"], p["water_depth_m"]
    bx = p["block_x_m"]
    comps = [_c("solid_block", "HULL", "concrete", "solid_block",
                _box(bx - side / 2, bx + side / 2, 0.0, side / 2, -depth, -depth + side), 0, meta={"note": "same concrete volume as the hull"}),
             _c("solid_block_cut", "SECTION_CUT", "section_poche", "solid_block",
                _box(bx - side / 2, bx + side / 2, -0.06, -0.05, -depth, -depth + side), 1)]
    hull = platform(dict(p, storeys=0, extension_m=0.0, section=1))
    return comps + [c for c in hull if c.type not in ("BUILDING", "ROOF", "DISPLACED_VOLUME", "MARKER", "DECORATION")]


def semi_sub(p):
    """B33 schematic of the concept study's module type: two pontoons under water, columns through the surface and a
    deck raised above the sea (not a design; proportions for legibility)."""
    L, B, depth_p, h_p = p["length_m"], p["width_m"], p["pontoon_depth_m"], p["pontoon_height_m"]
    deck_z, col = p["deck_level_m"], p["column_size_m"]
    comps = []
    for s, sy in enumerate((-1, 1), 1):
        cy = sy * (B / 2.0 - p["pontoon_width_m"] / 2.0)
        comps.append(_c(f"pontoon{s}", "HULL", "concrete", "pontoons",
                        _box(-L / 2, L / 2, cy - p["pontoon_width_m"] / 2, cy + p["pontoon_width_m"] / 2, -depth_p - h_p, -depth_p), 0))
        for q, x in enumerate((-L / 2 + col, 0.0, L / 2 - col), 1):
            comps.append(_c(f"column{s}_{q}", "COLUMN", "concrete", "columns",
                            P.cylinder_z(col / 2.0, deck_z + depth_p, 20, (x, cy, (deck_z - depth_p) / 2.0)), 1))
    comps.append(_c("deck", "DECK", "concrete_deck", "deck", _box(-L / 2, L / 2, -B / 2, B / 2, deck_z, deck_z + 1.0), 2))
    if p.get("compare_box"):   # B33: our first platform (Design A, three storeys, at its draft) beside it, for comparison
        comps += _platform_set("box", 40.0, 40.0, 4.0, COMPARE_BOX_DRAFT, 0.4, 3, -(L / 2 + 20.0 + 25.0), 0.0, group="box")
    return comps


COMPARE_BOX_DRAFT = 2.958   # analysis/results.json design_A.mid.draft_m (tests check it)


# ---------------------------------------------------------------- the district (Design C) and its counterfactual
DISTRICT_COLS, DISTRICT_ROWS = 11, 9
PILE_EMBED_M = 3.0     # piles are drawn driven this far into the seabed
WALK_TOP_M = 0.24      # walkway plank thickness on the deck
ANCHOR_EMBED_M = 0.3   # anchors are drawn bedded into the seabed (a sloping bed would otherwise leave a gap)
DISTRICT_LAGOON = {(c, r) for c in (4, 5, 6) for r in (4, 5)}


DISTRICT_USES = {   # the 27 modules of the outer ring by use (results.json district_C_allocation); the rest are homes
    **{(c, r): "mixed" for c in (0, DISTRICT_COLS - 1) for r in (0, 1, 2)},          # shops below, homes above, near the quay
    (4, 8): "school", (6, 8): "school", (0, 5): "school", (10, 3): "clinic"}
PARKS = {(4, 3), (5, 3), (6, 3), (4, 6), (5, 6), (6, 6), (3, 4), (3, 5), (7, 4), (7, 5)}   # the homes around the lagoon
SPINE_ROWS = (0, 2, 7)   # utility spines: not row 6, whose gardens open onto the lagoon (owner review of R2)
ROUTE_COLS = (2, 5, 8)   # the bridges' columns (a district with 3 bridges): halls there stand either side of the route


DISTRICT_TILE_KINDS = ("terrace", "villas", "blocks", "courtyard", "pinwheel")   # neighbours' tiles always differ
GARDEN_SIDE = {**{(c, 3): "+y" for c in (4, 5, 6)}, **{(c, 6): "-y" for c in (4, 5, 6)},
               (3, 4): "+x", (3, 5): "+x", (7, 4): "-x", (7, 5): "-x"}   # where the lagoon lies from each garden platform


def district_kind(c, r):
    """(home type, quarter turns) of a home platform: gardens open onto the lagoon; elsewhere 2 x 2 tiles of one type
    (a neighbourhood that reads as one), neighbouring tiles of different types, every other platform turned."""
    if (c, r) in GARDEN_SIDE:
        return "garden", LAGOON_TURN[GARDEN_SIDE[(c, r)]]
    tc, tr = (c - 1) // 2, r // 2
    return DISTRICT_TILE_KINDS[(tc + 2 * tr) % len(DISTRICT_TILE_KINDS)], (c + r) % 2


def district_cells():
    """[(col, row, use)]: 93 platforms of an 11 x 9 grid around a 3 x 2 lagoon; row 0 faces the shore. The seaward row
    and both flanks (27 platforms) carry the mixed and service uses, the 66 inside are homes."""
    out = []
    for c in range(DISTRICT_COLS):
        for r in range(DISTRICT_ROWS):
            if (c, r) in DISTRICT_LAGOON:
                continue
            ring = r == DISTRICT_ROWS - 1 or c in (0, DISTRICT_COLS - 1)
            out.append((c, r, DISTRICT_USES.get((c, r), "community") if ring else "home"))
    return out


def district(p):
    """Design C: 93 platforms (shared meshes), hinged walkways between neighbours, link-span bridges to the quay,
    piles in the shallow rows and mooring lines in the deep rows, a breakwater on the open side, utility spines along
    the bridges, boat landings and emergency routes. offshore = 1 drops the bridges (the counterfactual at sea)."""
    L, B, H, T, gap = p["length_m"], p["width_m"], p["hull_depth_m"], p["draft_m"], p["gap_m"]
    pitch = L + gap
    x_first = -(DISTRICT_COLS - 1) * pitch / 2.0
    y_first = p["shore_gap_m"] + B / 2.0
    zt = H - T
    comps = []
    cells = district_cells()
    pos = {}
    for c, r, use in cells:
        cx, cy = x_first + c * pitch, y_first + r * pitch
        pos[(c, r)] = (cx, cy)
        varied = p.get("home_types", "varied") == "varied"
        kind, turn = district_kind(c, r) if varied and use == "home" else ("blocks", 0)
        comps += _platform_set(f"m{c:02d}{r}", L, B, H, T, p["building_cover"], p["storeys"], cx, cy, use=use,
                               group="homes" if use in ("home", "mixed") else "services",
                               orient="y" if c in ROUTE_COLS else "x", park=(c, r) in PARKS and not varied, kind=kind, turn=turn)
    walk = P.box((gap + 2.0, 3.0, WALK_TOP_M), (0.0, 0.0, WALK_TOP_M / 2.0))
    walk_y = P.box((3.0, gap + 2.0, WALK_TOP_M), (0.0, 0.0, WALK_TOP_M / 2.0))
    n = 0
    for (c, r), (cx, cy) in sorted(pos.items()):
        if (c + 1, r) in pos:
            n += 1
            comps.append(_placed(f"walk_x{n:03d}", "WALKWAY", "timber_light", "walkways", walk, (cx + pitch / 2.0, cy, zt), 3))
        if (c, r + 1) in pos:
            n += 1
            comps.append(_placed(f"walk_y{n:03d}", "WALKWAY", "timber_light", "walkways", walk_y, (cx, cy + pitch / 2.0, zt), 3))
    depth_near, depth_far, run = p["depth_near_m"], p["depth_far_m"], p["seabed_run_m"]

    def seabed(y):   # the site's seabed: depth_near at the quay (y = 0), falling linearly to depth_far at y = run
        return depth_near + (depth_far - depth_near) * min(1.0, max(0.0, y / run))

    for (c, r), (cx, cy) in sorted(pos.items()):
        if r <= p["pile_rows"] - 1:
            for s, (sx, sy) in enumerate(((-1, -1), (1, 1)), 1):
                py = cy + sy * (B / 2.0 - 6.0)
                bottom = seabed(py) + PILE_EMBED_M   # driven into the seabed
                h = bottom + zt + 3.0
                mesh = P.cylinder_z(0.7, h, 12, (0.0, 0.0, h / 2.0))
                comps.append(_placed(f"m{c:02d}{r}_pile{s}", "MOORING_PILE", "steel", "piles", mesh,
                                     (cx + sx * (L / 2.0 + 1.5), py, -bottom), 4))
        elif r == DISTRICT_ROWS - 1 or c in (0, DISTRICT_COLS - 1):
            reach = p["line_reach_m"]
            dirs = [(0.0, 1.0)] if r == DISTRICT_ROWS - 1 else []
            dirs += [(-1.0, 0.0)] if c == 0 else [(1.0, 0.0)] if c == DISTRICT_COLS - 1 else []
            for s, (dx, dy) in enumerate(dirs, 1):
                fx, fy = cx + dx * (L / 2.0 + 0.3), cy + dy * (B / 2.0 + 0.3)
                ax, ay = fx + dx * reach, fy + dy * reach
                depth = seabed(ay)
                drop = (depth - 1.5) - (T - 0.5)
                mesh = _bar((0.0, 0.0, 0.0), (ax - fx, ay - fy, -drop), 0.6, 0.6)
                comps.append(_placed(f"m{c:02d}{r}_line{s}", "MOORING_LINE", "cable_dark", "lines", mesh, (fx, fy, -T + 0.5), 4,
                                     meta={"note": "conceptual mooring, not sized; straight drawn line"}))
                comps.append(_placed(f"m{c:02d}{r}_anchor{s}", "ANCHOR", "steel_dark", "anchors", _local_box(4.0, 4.0, 1.5, 0.75),
                                     (ax, ay, -depth - ANCHOR_EMBED_M), 4, meta={"note": "conceptual anchor, not sized"}))
    # breakwater on the open (seaward) side, in modules with gaps
    bw_y = y_first + (DISTRICT_ROWS - 1) * pitch + B / 2.0 + p["breakwater_offset_m"]
    span = DISTRICT_COLS * pitch + 2 * pitch
    seg = 60.0
    nseg = int(span // (seg + 4.0))
    x0 = -nseg * (seg + 4.0) / 2.0
    bw_mesh = _local_box(seg, 12.0, 5.0, 0.5)
    for k in range(nseg):
        comps.append(_placed(f"breakwater{k:02d}", "BREAKWATER", "concrete", "breakwater", bw_mesh,
                             (x0 + k * (seg + 4.0) + seg / 2.0, bw_y, 0.0), 5, meta={"note": "reduces waves; does not remove storm risk"}))
    bridge_cols = [int(round((k + 1) * (DISTRICT_COLS - 1) / (p["bridges"] + 1))) for k in range(p["bridges"])]
    if not p["offshore"]:   # link-spans from the quay (y = 0) to the first row, utility spines along them
        for k, c in enumerate(bridge_cols, 1):
            cx, cy = pos[(c, 0)]
            y_edge = cy - B / 2.0
            q = p["quay_level_m"]
            comps.append(_c(f"linkspan{k}", "LINK_SPAN", "concrete_deck", "linkspans",
                            _bar((cx, 0.0, q + 0.33), (cx, y_edge, zt + 0.3), 8.0, 0.6), 3))
            comps.append(_c(f"linkspan{k}_hinge", "CONNECTOR", "steel_dark", "linkspans",
                            _bar((cx - 4.5, -0.32, q + 0.3), (cx + 4.5, -0.32, q + 0.3), 0.6, 0.6), 3))
            for u, (mat, dx) in enumerate((("utility_power", -2.5), ("utility_water", 0.0), ("utility_waste", 2.5)), 1):
                net = ("power", "water", "wastewater")[u - 1]
                comps.append(_c(f"linkspan{k}_{net}", "UTILITY_LINE", mat, f"utility_{net}",
                                _bar((cx + dx, 0.5, q + 0.33 - 0.575), (cx + dx, y_edge - 0.5, zt + 0.3 - 0.575), 0.5, 0.5), 4,
                                meta={"network": net}))
        for u, (mat, dy) in enumerate((("utility_power", -1.0), ("utility_water", 0.0), ("utility_waste", 1.0)), 1):
            net = ("power", "water", "wastewater")[u - 1]
            for r in SPINE_ROWS:   # spines along the street through the middle of a row, carried on the walkways
                y = y_first + r * pitch + dy
                xa, xb = x_first, x_first + (DISTRICT_COLS - 1) * pitch
                z = zt + WALK_TOP_M + 0.3 - 0.002   # resting on the planks (2 mm contact, under the 4 mm penetration limit)
                comps.append(_c(f"spine_{net}_r{r}", "UTILITY_LINE", mat, f"utility_{net}",
                                _bar((xa, y, z), (xb, y, z), 0.6, 0.6), 4, meta={"network": net}))
    if p["offshore"] and p["shore_link_m"] > 0:   # B31: cables and pipes to a shore beyond the frame, on the seabed
        cx, cy = pos[(DISTRICT_COLS // 2, 0)]
        ys, depth = cy - B / 2.0 - 0.5, seabed(cy - B / 2.0)
        for u, (mat, dx) in enumerate((("utility_power", -2.5), ("utility_water", 0.0), ("utility_waste", 2.5)), 1):
            net = ("power", "water", "wastewater")[u - 1]
            x = cx + dx
            riser = _bar((x, ys, zt), (x, ys, -depth + 0.3), 0.6, 0.6)
            run = _bar((x, ys + 0.3, -depth + 0.3), (x, ys - p["shore_link_m"], -depth + 0.3), 0.6, 0.6)
            comps.append(_c(f"shore_link_{net}", "UTILITY_LINE", mat, f"utility_{net}", P.merge(riser, run), 4,
                            meta={"network": net, "note": "to a shore beyond the frame; not routed or sized"}))
    for k, c in enumerate((0, DISTRICT_COLS - 1), 1):   # boat landings on the flanks, emergency routes to the bridges
        cx, cy = pos[(c, 4)]
        side = -1 if c == 0 else 1
        comps.append(_c(f"landing{k}", "WALKWAY", "timber", "landings",
                        _box(cx + side * L / 2.0, cx + side * (L / 2.0 + 14.0), cy - 10.0, cy + 10.0, zt - 0.8, zt - 0.5), 3,
                        meta={"use": "boat landing (fire and rescue boats, water taxis)"}))
    for k, c in enumerate([] if p["offshore"] else bridge_cols, 1):
        # painted on the decks and walkways of the bridge's column, from the link-span up to the lagoon
        x = x_first + c * pitch
        parts, r = [], 0
        while (c, r) in pos:
            cy = pos[(c, r)][1]
            ya = cy - B / 2.0 + (1.0 if r else 0.05)          # clear of the link-span's end and the walkway's overlap
            yb = cy + B / 2.0 - (1.0 if (c, r + 1) in pos else 0.0)
            parts.append(_box(x - 1.3, x + 1.3, ya, yb, zt + PATH_H, zt + PATH_H + 0.05))   # painted on the paving
            if (c, r + 1) in pos:
                parts.append(_box(x - 1.3, x + 1.3, cy + B / 2.0 - 1.0, cy + B / 2.0 + gap + 1.0, zt + WALK_TOP_M, zt + WALK_TOP_M + 0.05))
            r += 1
        comps.append(_c(f"route{k}", "ACCESS_ROUTE", "route_emergency", "routes", P.merge(*parts), 5,
                        meta={"use": "emergency route to land", "rows": r}))
    return comps
