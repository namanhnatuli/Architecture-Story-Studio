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


def _platform_set(prefix, L, B, H, T, cover, storeys, cx, cy, use="home", group=None):
    """One platform as a few merged components (hull, deck, buildings, roof) placed at (cx, cy): identical platforms
    share their meshes. use: home | service | park."""
    g = group or prefix
    zt = H - T
    parts = [_placed(f"{prefix}_hull", "HULL", "concrete", g, _local_box(L, B, H - 0.25, -(H - 0.25) / 2.0), (cx, cy, zt - 0.25), 0),
             _placed(f"{prefix}_deck", "DECK", "concrete_deck" if use != "park" else "park_lawn", g,
                     _local_box(L, B, 0.25, -0.125), (cx, cy, zt), 1)]
    if use == "park" or storeys <= 0:
        return parts
    blocks = block_layout(L, B, cover)
    h = storeys * 3.0
    body = P.merge(*[P.box((x1 - x0, y1 - y0, h), ((x0 + x1) / 2.0, (y0 + y1) / 2.0, h / 2.0)) for x0, x1, y0, y1 in blocks])
    roof = P.merge(*[P.box((x1 - x0 - 0.1, y1 - y0 - 0.1, 0.3), ((x0 + x1) / 2.0, (y0 + y1) / 2.0, h + 0.15)) for x0, x1, y0, y1 in blocks])
    parts.append(_placed(f"{prefix}_buildings", "BUILDING", "plaster" if use == "home" else "plaster_service", g, body,
                         (cx, cy, zt), 2, meta={"use": use}))
    parts.append(_placed(f"{prefix}_roofs", "ROOF", "roof_membrane" if use == "home" else "roof_green", g, roof, (cx, cy, zt), 2))
    return parts


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


def neighbourhood(p):
    """Five platforms around a small basin with gaps, hinged walkways, flexible utility links and fenders, held by
    piles (moorings = piles) or by mooring lines to anchors on the seabed (moorings = lines)."""
    L, B, H, T, gap = p["length_m"], p["width_m"], p["hull_depth_m"], p["draft_m"], p["gap_m"]
    pitch_x, pitch_y = L + gap, B + gap
    zt = H - T
    storeys = [int(s) for s in str(p["storeys_pattern"]).split(",")]
    comps, centres = [], {}
    for k, (i, j) in enumerate(NEIGHBOURHOOD, 1):
        cx, cy = i * pitch_x, j * pitch_y
        centres[(i, j)] = (cx, cy)
        comps += _platform_set(f"platform{k}", L, B, H, T, p["building_cover"], storeys[(k - 1) % len(storeys)], cx, cy,
                               group=f"platform{k}")
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
    if p["moorings"] == "piles":
        for k, (i, j) in enumerate(NEIGHBOURHOOD, 1):
            cx, cy = centres[(i, j)]
            for s, (sx, sy) in enumerate(((-1, -1), (1, 1)), 1):
                px, py = cx + sx * (L / 2.0 + 1.4), cy + sy * (B / 2.0 - 4.0)
                comps.append(_c(f"platform{k}_pile{s}", "MOORING_PILE", "steel", "piles",
                                P.cylinder_z(0.6, depth + 1.5 + zt + 3.0, 16, (px, py, (zt + 3.0 - depth - 1.5) / 2.0)), 4))
                comps.append(_c(f"platform{k}_pile{s}_guide", "CONNECTOR", "steel_dark", "piles",
                                _box(min(px, cx + sx * L / 2.0) - (0.0 if sx > 0 else 0.0), max(px, cx + sx * L / 2.0),
                                     py - 0.9, py + 0.9, zt - 0.6, zt - 0.1), 4))
    else:
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
    return comps + [c for c in hull if c.type not in ("BUILDING", "ROOF", "DISPLACED_VOLUME")]


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
    return comps


# ---------------------------------------------------------------- the district (Design C) and its counterfactual
DISTRICT_COLS, DISTRICT_ROWS = 11, 9
PILE_EMBED_M = 3.0     # piles are drawn driven this far into the seabed
WALK_TOP_M = 0.24      # walkway plank thickness on the deck
ANCHOR_EMBED_M = 0.3   # anchors are drawn bedded into the seabed (a sloping bed would otherwise leave a gap)
DISTRICT_LAGOON = {(c, r) for c in (4, 5, 6) for r in (4, 5)}


def district_cells():
    """[(col, row, use)]: 93 platforms of an 11 x 9 grid around a 3 x 2 lagoon; row 0 faces the shore; the seaward
    row and both flanks (27 platforms) carry services, the 66 inside are homes."""
    out = []
    for c in range(DISTRICT_COLS):
        for r in range(DISTRICT_ROWS):
            if (c, r) in DISTRICT_LAGOON:
                continue
            ring = r == DISTRICT_ROWS - 1 or c in (0, DISTRICT_COLS - 1)
            out.append((c, r, "service" if ring else "home"))
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
        comps += _platform_set(f"m{c:02d}{r}", L, B, H, T, p["building_cover"], p["storeys"], cx, cy, use=use,
                               group="homes" if use == "home" else "services")
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
            for r in (0, 2, 6):   # spines along the street through the middle of a row, carried on the walkways
                y = y_first + r * pitch + dy
                xa, xb = x_first, x_first + (DISTRICT_COLS - 1) * pitch
                z = zt + WALK_TOP_M + 0.3 - 0.002   # resting on the planks (2 mm contact, under the 4 mm penetration limit)
                comps.append(_c(f"spine_{net}_r{r}", "UTILITY_LINE", mat, f"utility_{net}",
                                _bar((xa, y, z), (xb, y, z), 0.6, 0.6), 4, meta={"network": net}))
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
            parts.append(_box(x - 1.3, x + 1.3, ya, yb, zt, zt + 0.05))
            if (c, r + 1) in pos:
                parts.append(_box(x - 1.3, x + 1.3, cy + B / 2.0 - 1.0, cy + B / 2.0 + gap + 1.0, zt + WALK_TOP_M, zt + WALK_TOP_M + 0.05))
            r += 1
        comps.append(_c(f"route{k}", "ACCESS_ROUTE", "route_emergency", "routes", P.merge(*parts), 5,
                        meta={"use": "emergency route to land", "rows": r}))
    return comps
