"""Cathedral family generators (pure Python): a Gothic and a Romanesque section through a few bays.

Illustrative archetypes for explanation, not reconstructions of a real building and not engineering designs.

Conventions (metres): X across the church (nave centred on x = 0), Y along it (bays recede towards +Y from the cut
at y = 0), Z up with the floor at z = 0. The section is open at both ends, so a worm's-eye axonometric (the classic
way to draw vaults) sees the ribs from below; the camera preset CATHEDRAL_FROM_BELOW is made for it.
Local component ids are stable; the variant id is prefixed when planned (assets.py).
"""
import math

from engine.arch import primitives as P
from engine.arch.families.site import GROUND_Z
from engine.arch.semantic import Component

WEB_THICKNESS = 0.45
SIDES = (("west", -1), ("east", 1))


# ---------------------------------------------------------------- geometry helpers
def prism_yz(outline, thickness, x_center=0.0):
    """Polygon outline [(y, z), ...] extruded along X (a wall seen face-on from inside the church)."""
    if len(outline) < 3:
        raise ValueError("prism needs at least 3 outline points")
    n = len(outline)
    verts = [(x_center + d, y, z) for d in (-thickness / 2.0, thickness / 2.0) for y, z in outline]
    faces = [tuple(range(n)), tuple(n + i for i in reversed(range(n)))]
    faces += [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)]
    return {"verts": verts, "faces": faces}


def sweep(points, width, depth, side):
    """A bar of rectangular section along a polyline. `width` lies along the fixed horizontal vector `side`, `depth`
    across it; ribs keep their section vertical in the plane of the arch."""
    sx, sy, sz = side
    verts = []
    for k, p in enumerate(points):
        a, b = points[max(k - 1, 0)], points[min(k + 1, len(points) - 1)]
        t = [b[i] - a[i] for i in range(3)]
        n = math.sqrt(sum(v * v for v in t)) or 1.0
        t = [v / n for v in t]
        nx, ny, nz = (t[1] * sz - t[2] * sy, t[2] * sx - t[0] * sz, t[0] * sy - t[1] * sx)
        for a_, b_ in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
            verts.append((p[0] + a_ * width / 2.0 * sx + b_ * depth / 2.0 * nx,
                          p[1] + a_ * width / 2.0 * sy + b_ * depth / 2.0 * ny,
                          p[2] + a_ * width / 2.0 * sz + b_ * depth / 2.0 * nz))
    faces = [(0, 3, 2, 1), tuple(4 * (len(points) - 1) + i for i in range(4))]
    for k in range(len(points) - 1):
        base = 4 * k
        for i in range(4):
            j = (i + 1) % 4
            faces.append((base + i, base + j, base + 4 + j, base + 4 + i))
    return {"verts": verts, "faces": faces}


def shell(rows, thickness):
    """A closed slab from a grid of points (rows of equal length): the top is the grid raised by `thickness`."""
    nu, nv = len(rows), len(rows[0])
    verts = [p for row in rows for p in row] + [(p[0], p[1], p[2] + thickness) for row in rows for p in row]
    idx = lambda top, u, v: (nu * nv if top else 0) + u * nv + v   # noqa: E731
    faces = []
    for u in range(nu - 1):
        for v in range(nv - 1):
            faces.append((idx(0, u, v), idx(0, u, v + 1), idx(0, u + 1, v + 1), idx(0, u + 1, v)))
            faces.append((idx(1, u, v), idx(1, u + 1, v), idx(1, u + 1, v + 1), idx(1, u, v + 1)))
    for u in range(nu - 1):
        for v in (0, nv - 1):
            faces.append((idx(0, u, v), idx(0, u + 1, v), idx(1, u + 1, v), idx(1, u, v)))
    for v in range(nv - 1):
        for u in (0, nu - 1):
            faces.append((idx(0, u, v), idx(1, u, v), idx(1, u, v + 1), idx(0, u, v + 1)))
    return {"verts": verts, "faces": faces}


def pointed_half(half_span, rise, n=12):
    """One side of a pointed arch, from the springing (u = half_span, v = 0) to the apex (u = 0, v = rise): an arc of a
    circle centred beyond the far side, as two such arcs meeting at a point make a pointed arch."""
    r = (half_span * half_span + rise * rise) / (2.0 * half_span)
    top = math.atan2(rise, r - half_span)
    return [(half_span - r + r * math.cos(top * k / n), r * math.sin(top * k / n)) for k in range(n + 1)]


def round_half(half_span, n=12):
    return [(half_span * math.cos(math.pi / 2.0 * k / n), half_span * math.sin(math.pi / 2.0 * k / n)) for k in range(n + 1)]


def _head_pieces(y0, y1, spring, head, top, thickness, x, sill=None):
    """A wall panel between y0 and y1 up to `top`, with an opening whose head is `head` (half profile from the
    springing to the apex, u across, v up from `spring`). Two prisms that meet on the centre line. sill: the wall goes
    below the opening from there; None: the opening reaches the bottom of the panel, which starts at `spring`."""
    yc = (y0 + y1) / 2.0
    half = (y1 - y0) / 2.0
    margin = half - head[0][0]
    panels = []
    for sign in (-1, 1):
        edge = yc + sign * half
        pts = [(yc + sign * u, spring + v) for u, v in head]
        if sill is None:
            outline = ([(edge, spring)] if margin > 1e-6 else []) + pts + [(yc, top), (edge, top)]
        else:
            bottom, z_sill = sill
            outline = [(edge, bottom), (yc, bottom), (yc, z_sill), (yc + sign * head[0][0], z_sill)] + pts + [(yc, top), (edge, top)]
        panels.append(prism_yz(outline, thickness, x))
    return P.merge(*panels)


def _window_glass(half_width, spring, head, sill, thickness, yc, x):
    outline = [(yc - half_width, sill), (yc + half_width, sill)]
    outline += [(yc + u, spring + v) for u, v in head[:-1]]
    outline += [(yc, spring + head[-1][1])]
    outline += [(yc - u, spring + v) for u, v in reversed(head[:-1])]
    return prism_yz(outline, thickness, x)


def _vault_bay(cx, half_span, cy, half_bay, spring, rise, n=14):
    """Web strips and rib lines of one four-part vault bay. The web is a groin-type surface: at each height the cell
    against a transverse arch is ruled along Y, the cell against a wall along X, and the diagonal ribs are where they
    meet. All crowns lie at one level (the pointed arch's property). Returns (web mesh, diagonal rib lines, transverse
    rib line)."""
    half = pointed_half(half_span, rise, n)
    curve = [(u, spring + v) for u, v in half][1:]      # the web starts just above the springing, not at a zero-width corner
    y_at = [half_bay * u / half_span for u, _ in curve]
    strips = []
    for sx in (-1, 1):       # cells against the transverse arches (y = cy +/- half_bay)
        for sy in (-1, 1):
            strips.append([[(cx + sx * u, cy + sy * half_bay, z), (cx + sx * u, cy + sy * y, z)]
                           for (u, z), y in zip(curve, y_at)])
    for sx in (-1, 1):       # cells against the walls (x = cx +/- half_span)
        for sy in (-1, 1):
            strips.append([[(cx + sx * half_span, cy + sy * y, z), (cx + sx * u, cy + sy * y, z)]
                           for (u, z), y in zip(curve, y_at)])
    web = P.merge(*[shell(s, WEB_THICKNESS) for s in strips])
    full = [(u, spring + v) for u, v in half]
    diagonals = [[(cx + sx * u, cy + sy * half_bay * u / half_span, z) for u, z in full] for sx in (-1, 1) for sy in (-1, 1)]
    transverse = [[(cx + sx * u, 0.0, z) for u, z in full] for sx in (-1, 1)]
    return web, diagonals, transverse


COURSE_PANELS = ("f", "b", "w", "e")   # web panels against the front / back transverse arch, the west / east wall


def _vault_courses(cx, half_span, cy, half_bay, spring, rise, courses, n=14):
    """The web of one four-part bay cut into courses: {panel: [mesh per course]}.

    The same groin-type surface as _vault_bay, sliced the way Heyman's analysis reads it: each course is one arch that
    springs from a diagonal rib and lands on the other one (or on the wall), parallel to the transverse arch (panels
    f, b) or to the wall (panels w, e). The course against the arch or wall is a full arch; the courses towards the crown
    are shorter, as the diagonals close in. Courses touch, so at rest the web reads as one surface."""
    curve = [(u, spring + v) for u, v in pointed_half(half_span, rise, n)][1:]
    ratio = half_bay / half_span
    out = {}
    for panel in COURSE_PANELS:
        along_y = panel in ("f", "b")        # f/b courses are cut at constant y, w/e at constant x
        extent = half_bay if along_y else half_span

        def reach(u):                        # where the diagonal rib is at the height of curve point u, in the cut direction
            return u * ratio if along_y else u
        meshes = []
        for k in range(courses):
            a, b = extent * k / courses, extent * (k + 1) / courses
            strips, pts = [], []             # pts: (u, z, inner end of the row) from the course's foot to the crown
            for j, (u, z) in enumerate(curve):
                if reach(u) >= b - 1e-6:
                    continue
                if not pts and j > 0:        # the course starts exactly where the diagonal crosses b (no sliver gap)
                    (pu, pz) = curve[j - 1]
                    t = (reach(pu) - b) / (reach(pu) - reach(u))
                    pts.append((pu + (u - pu) * t, pz + (z - pz) * t, b - 0.02))
                pts.append((u, z, max(a, reach(u))))
            for sa in (-1, 1):               # the two halves of the course, either side of the crown line
                rows = []
                for u, z, lo in pts:
                    if along_y:
                        sy = -1 if panel == "f" else 1
                        rows.append([(cx + sa * u, cy + sy * b, z), (cx + sa * u, cy + sy * lo, z)])
                    else:
                        sx = -1 if panel == "w" else 1
                        y = u * ratio
                        rows.append([(cx + sx * b, cy + sa * y, z), (cx + sx * lo, cy + sa * y, z)])
                if len(rows) >= 2:
                    strips.append(rows)
            meshes.append(P.merge(*[shell(s, WEB_THICKNESS) for s in strips]))
        out[panel] = meshes
    return out


def _pinnacle(size, z0, shaft, spire):
    h = size / 2.0
    tip = z0 + shaft + spire
    verts = [(sx * h, sy * h, z0) for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
    verts += [(sx * h, sy * h, z0 + shaft) for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
    verts.append((0.0, 0.0, tip))
    faces = [(3, 2, 1, 0)] + [(i, (i + 1) % 4, 4 + (i + 1) % 4, 4 + i) for i in range(4)]
    faces += [(4 + i, 4 + (i + 1) % 4, 8) for i in range(4)]
    return {"verts": verts, "faces": faces}


def _gable(half_width, eave, ridge, length, thickness, y0):
    """Two roof slopes over a church, open beneath so the section reads as a roof, not a solid."""
    panels = []
    for sign in (-1, 1):
        outline = [(sign * half_width, eave), (0.0, ridge), (0.0, ridge + thickness), (sign * half_width, eave + thickness)]
        panels.append(P.prism_xz(outline, length, y0 + length / 2.0))
    return P.merge(*panels)


# ---------------------------------------------------------------- Gothic section
def gothic_layout(p):
    """Key positions, shared by the generator and the checks."""
    nave, aisle = p["nave_half_width_m"], p["aisle_width_m"]
    wall_x = nave + aisle
    return {"wall_x": wall_x, "buttress_inner": wall_x, "buttress_outer": wall_x + p["pier_buttress_depth_m"],
            "length": p["bay_length_m"] * p["bay_count"], "frames": [p["bay_length_m"] * j for j in range(p["bay_count"] + 1)]}


def gothic_section(p):
    """Compound piers rising to the high vault, arcade and triforium, tall clerestory windows, four-part rib vaults with
    their stone web, aisles with lean-to roofs, flying buttresses onto pier buttresses topped by pinnacles.

    Each kind of part the film names is its own component, so a beat can light it: rib, vault_web, nave_pier,
    clerestory_window, flying_buttress, pier_buttress, pinnacle, aisle_roof."""
    lay = gothic_layout(p)
    nave, aisle, bay, n = p["nave_half_width_m"], p["aisle_width_m"], p["bay_length_m"], p["bay_count"]
    pier_r = p["pier_radius_m"]
    spring, crown = p["vault_spring_m"], p["vault_crown_m"]
    arcade_top, trif_top = p["arcade_top_m"], p["triforium_top_m"]
    wall_t = p["upper_wall_thickness_m"]
    top = crown + 1.0
    length, frames = lay["length"], lay["frames"]
    comps = [Component("floor", "FLOOR", "stone_dark",
                       P.box((2 * lay["buttress_outer"] + 1.2, length + 2.0, -GROUND_Z), (0.0, length / 2.0, GROUND_Z / 2.0)),
                       group="floor", layer=0, animation=("STATIC",))]
    # piers run from the floor to the roof: the frame everything else hangs on
    shaft = P.merge(P.cylinder_z(pier_r, top, 16, (0.0, 0.0, top / 2.0)),
                    *[P.cylinder_z(pier_r * 0.3, spring, 8, (dx, dy, spring / 2.0))
                      for dx, dy in ((pier_r, 0.0), (-pier_r, 0.0), (0.0, pier_r), (0.0, -pier_r))])
    for j, y in enumerate(frames):
        for side, s in SIDES:
            comps.append(Component(f"nave_pier_{side}{j}", "NAVE_PIER", "stone", shaft, group=f"frame_{side}{j}",
                                   location=(s * nave, y, 0.0), layer=1, animation=("HIGHLIGHT", "STATIC")))
    # walls between the piers
    jamb = pier_r * 0.9
    arcade_head = pointed_half(bay / 2.0 - jamb, p["arcade_rise_m"])
    window_half = bay / 2.0 - jamb - 0.35
    window_head = pointed_half(window_half, p["window_rise_m"])
    z_sill, win_spring = trif_top + 0.3, p["window_spring_m"]
    aisle_web_spring = p["aisle_spring_m"]
    for i in range(n):
        y0, y1 = frames[i] + jamb, frames[i + 1] - jamb
        yc = (y0 + y1) / 2.0
        for side, s in SIDES:
            x = s * nave
            arc_spring = arcade_top - p["arcade_rise_m"] - 1.0
            comps.append(Component(f"arcade_wall_b{i + 1}_{side}", "WALL", "stone",
                                   _head_pieces(y0, y1, arc_spring, arcade_head, arcade_top, wall_t, x),
                                   group="arcade", layer=2, animation=("HIGHLIGHT", "STATIC")))
            comps.append(Component(f"triforium_b{i + 1}_{side}", "WALL", "stone_dark",
                                   P.box((wall_t, y1 - y0, trif_top - arcade_top), (x, yc, (arcade_top + trif_top) / 2.0)),
                                   group="triforium", layer=2, animation=("HIGHLIGHT", "STATIC")))
            comps.append(Component(f"clerestory_wall_b{i + 1}_{side}", "WALL", "stone",
                                   _head_pieces(y0, y1, win_spring, window_head, top, wall_t, x, sill=(trif_top, z_sill)),
                                   group="upper_wall", layer=3, animation=("HIGHLIGHT", "STATIC")))
            comps.append(Component(f"clerestory_window_b{i + 1}_{side}", "CLERESTORY_WINDOW", "stained_glass",
                                   _window_glass(window_half, win_spring, window_head, z_sill, 0.14, yc, x),
                                   group="clerestory", layer=3, animation=("HIGHLIGHT", "STATIC")))
            # the aisle: outer wall with its window, then its lean-to roof
            ax = s * lay["wall_x"]
            aisle_head = pointed_half(window_half, 3.2)
            comps.append(Component(f"aisle_wall_b{i + 1}_{side}", "WALL", "stone",
                                   _head_pieces(y0, y1, aisle_web_spring, aisle_head, p["aisle_top_m"], 0.9, ax, sill=(0.0, 3.0)),
                                   group="aisle_wall", layer=2, animation=("HIGHLIGHT", "STATIC")))
            comps.append(Component(f"aisle_window_b{i + 1}_{side}", "AISLE_WINDOW", "stained_glass",
                                   _window_glass(window_half, aisle_web_spring, aisle_head, 3.0, 0.14, yc, ax),
                                   group="aisle_windows", layer=2, animation=("HIGHLIGHT", "STATIC")))
    # vaults: nave and both aisles
    rise = crown - spring
    courses = int(p.get("web_courses", 1))
    for i in range(n):
        cy = frames[i] + bay / 2.0
        web, diagonals, _ = _vault_bay(0.0, nave, cy, bay / 2.0, spring, rise)
        if courses > 1:   # the web as courses (one arch each), so a shot can show Heyman's reading of it
            for panel, meshes in _vault_courses(0.0, nave, cy, bay / 2.0, spring, rise, courses).items():
                for k, mesh in enumerate(meshes):
                    comps.append(Component(f"vault_web_b{i + 1}_{panel}{k + 1}", "VAULT_WEB", "stone_light", mesh,
                                           group="high_vault", layer=4, animation=("HIGHLIGHT", "STATIC")))
        else:
            comps.append(Component(f"vault_web_b{i + 1}", "VAULT_WEB", "stone_light", web, group="high_vault",
                                   layer=4, animation=("HIGHLIGHT", "STATIC")))
        d = math.hypot(nave, bay / 2.0)
        rib_lines = []
        for k, line in enumerate(diagonals):
            sx = 1 if k < 2 else -1
            sy = 1 if k % 2 == 0 else -1
            side = (-sy * (bay / 2.0) / d, sx * nave / d, 0.0)
            rib_lines.append(sweep([(a, b, c - 0.12) for a, b, c in line], p["rib_width_m"], p["rib_depth_m"], side))
        # the two diagonal ribs of the bay are separate parts (half-ribs 0 and 3 make one, 1 and 2 the other), so "two
        # ribs cross diagonally" can show them one after the other
        for suffix, halves in (("a", (0, 3)), ("b", (1, 2))):
            comps.append(Component(f"rib_diagonal_b{i + 1}{suffix}", "RIB", "stone_light", P.merge(*[rib_lines[h] for h in halves]),
                                   group=f"rib_diagonal_{i + 1}", layer=5, animation=("HIGHLIGHT", "STATIC")))
    transverse_lines = _vault_bay(0.0, nave, 0.0, bay / 2.0, spring, rise)[2]
    for j, y in enumerate(frames):
        rib = P.merge(*[sweep([(a, 0.0, c - 0.12) for a, _b, c in line], p["rib_width_m"] * 1.2, p["rib_depth_m"], (0.0, 1.0, 0.0))
                        for line in transverse_lines])
        comps.append(Component(f"rib_transverse_{j}", "RIB", "stone_light", rib, group=f"rib_transverse_{j}",
                               location=(0.0, y, 0.0), layer=5, animation=("HIGHLIGHT", "STATIC")))
    a_half = aisle / 2.0
    a_rise = p["aisle_crown_m"] - p["aisle_spring_m"]
    for i in range(n):
        cy = frames[i] + bay / 2.0
        for side, s in SIDES:
            web, diagonals, _ = _vault_bay(s * (nave + a_half), a_half, cy, bay / 2.0, p["aisle_spring_m"], a_rise, 10)
            comps.append(Component(f"aisle_vault_b{i + 1}_{side}", "AISLE_VAULT", "stone_light", web, group="aisle_vaults",
                                   layer=4, animation=("HIGHLIGHT", "STATIC")))
    # roofs
    comps.append(Component("high_roof", "ROOF", "roof_lead", _gable(nave + 1.1, top - 0.6, p["ridge_m"], length, 0.35, 0.0),
                           group="roofs", layer=6, animation=("HIGHLIGHT", "STATIC")))
    for side, s in SIDES:
        inner, outer = s * (nave + wall_t / 2.0), s * (lay["wall_x"] + 0.5)
        outline = [(inner, trif_top), (outer, p["aisle_top_m"]), (outer, p["aisle_top_m"] + 0.35), (inner, trif_top + 0.35)]
        comps.append(Component(f"aisle_roof_{side}", "AISLE_ROOF", "roof_lead", P.prism_xz(outline, length, length / 2.0),
                               group="aisle_roofs", layer=6, animation=("HIGHLIGHT", "STATIC")))
    # flying buttresses, pier buttresses, pinnacles at every frame
    b_in, b_out = lay["buttress_inner"], lay["buttress_outer"]
    w = p["pier_buttress_width_m"]
    h1, h2, h3 = p["pier_buttress_top_m"] * 0.45, p["pier_buttress_top_m"] * 0.75, p["pier_buttress_top_m"]
    for j, y in enumerate(frames):
        for side, s in SIDES:
            def box_x(a, b, z0, z1):
                lo, hi = min(s * a, s * b), max(s * a, s * b)
                return P.box((hi - lo, w, z1 - z0), ((lo + hi) / 2.0, y, (z0 + z1) / 2.0))
            depth = b_out - b_in
            comps.append(Component(f"pier_buttress_{side}{j}", "PIER_BUTTRESS", "stone",
                                   P.merge(box_x(b_in, b_out, 0.0, h1), box_x(b_in, b_in + depth * 0.82, h1, h2),
                                           box_x(b_in, b_in + depth * 0.62, h2, h3)),
                                   group=f"frame_{side}{j}", layer=2, animation=("HIGHLIGHT", "STATIC")))
            comps.append(Component(f"pinnacle_{side}{j}", "PINNACLE", "stone_light",
                                   _pinnacle(w * 0.72, h3, p["pinnacle_shaft_m"], p["pinnacle_spire_m"]), group=f"frame_{side}{j}",
                                   location=(s * (b_in + depth * 0.31), y, 0.0), layer=5, animation=("HIGHLIGHT", "STATIC")))
            # flyer: straight top, curved underside, from the high pier down to the buttress
            x_hi, x_lo = nave + pier_r, b_in + depth * 0.05
            z_hi, z_lo = p["flyer_head_m"], h3 - 1.0
            upper = [(s * x_hi, z_hi + 1.5), (s * x_lo, z_lo + 1.5)]
            steps = 12
            under = []
            for k in range(steps + 1):
                t = k / steps
                under.append((s * (x_lo + (x_hi - x_lo) * t), z_lo - 1.4 + (z_hi - z_lo + 1.4 - 0.2) * math.sqrt(t)))
            comps.append(Component(f"flying_buttress_{side}{j}", "FLYING_BUTTRESS", "stone", P.prism_xz(upper + under, p["flyer_width_m"], y),
                                   group=f"frame_{side}{j}", layer=5, animation=("HIGHLIGHT", "STATIC")))
    return comps


# ---------------------------------------------------------------- Romanesque section
def romanesque_layout(p):
    half = p["interior_half_width_m"]
    wall = p["wall_thickness_m"]
    return {"wall_inner": half, "wall_outer": half + wall, "crown": p["wall_height_m"] + half,
            "length": p["bay_length_m"] * p["bay_count"], "frames": [p["bay_length_m"] * j for j in range(p["bay_count"] + 1)]}


def romanesque_section(p):
    """One type of Romanesque church: a stone barrel vault on two thick walls, stiffened by shallow buttresses, with
    small round-headed windows. Not lit or coloured differently from the Gothic section."""
    lay = romanesque_layout(p)
    half, wall = p["interior_half_width_m"], p["wall_thickness_m"]
    bay, n, height = p["bay_length_m"], p["bay_count"], p["wall_height_m"]
    length, frames = lay["length"], lay["frames"]
    ring = p["vault_thickness_m"]
    x_mid = half + wall / 2.0
    win_half = p["window_half_width_m"]
    win_spring = p["window_spring_m"]
    head = round_half(win_half)
    comps = [Component("floor", "FLOOR", "stone_dark",
                       P.box((2 * (lay["wall_outer"] + p["buttress_depth_m"]) + 1.2, length + 2.0, -GROUND_Z), (0.0, length / 2.0, GROUND_Z / 2.0)),
                       group="floor", layer=0, animation=("STATIC",))]
    for i in range(n):
        y0, y1 = frames[i], frames[i + 1]
        yc = (y0 + y1) / 2.0
        for side, s in SIDES:
            x = s * x_mid
            comps.append(Component(f"thick_wall_b{i + 1}_{side}", "THICK_WALL", "stone",
                                   _head_pieces(y0, y1, win_spring, head, height, wall, x, sill=(0.0, win_spring - 2.2)),
                                   group="walls", layer=1, animation=("HIGHLIGHT", "STATIC")))
            comps.append(Component(f"small_window_b{i + 1}_{side}", "SMALL_WINDOW", "stained_glass",
                                   _window_glass(win_half, win_spring, head, win_spring - 2.2, 0.14, yc, s * (half + wall * 0.93)),
                                   group="windows", layer=1, animation=("HIGHLIGHT", "STATIC")))
        comps.append(Component(f"barrel_vault_b{i + 1}", "BARREL_VAULT", "stone_light",
                               P.sector(half, half + ring, 0.0, math.pi, bay, 24, (0.0, yc, height)),
                               group="vault", layer=2, animation=("HIGHLIGHT", "STATIC")))
        # masonry over the haunches, up to the roof line
        for side, s in SIDES:
            outer = half + ring
            arc = [(outer * math.cos(a), height + outer * math.sin(a)) for a in [math.radians(d) for d in range(0, 61, 10)]]
            outline = [(s * lay["wall_outer"], height)] + [(s * x_, z_) for x_, z_ in arc] + [(s * lay["wall_outer"], arc[-1][1])]
            comps.append(Component(f"haunch_fill_b{i + 1}_{side}", "WALL", "stone", P.prism_xz(outline, bay, yc),
                                   group="walls", layer=2, animation=("HIGHLIGHT", "STATIC")))
    for j, y in enumerate(frames):
        for side, s in SIDES:
            outer = lay["wall_outer"]
            depth = p["buttress_depth_m"]
            lo, hi = min(s * outer, s * (outer + depth)), max(s * outer, s * (outer + depth))
            comps.append(Component(f"shallow_buttress_{side}{j}", "SHALLOW_BUTTRESS", "stone",
                                   P.box((hi - lo, p["buttress_width_m"], height), ((lo + hi) / 2.0, y, height / 2.0)),
                                   group="buttresses", layer=2, animation=("HIGHLIGHT", "STATIC")))
    ring_top = height + (half + ring) * math.sin(math.radians(60))
    comps.append(Component("high_roof", "ROOF", "roof_lead",
                           _gable(lay["wall_outer"] + 0.4, ring_top - 0.3, ring_top + p["roof_rise_m"], length, 0.35, 0.0),
                           group="roofs", layer=3, animation=("HIGHLIGHT", "STATIC")))
    return comps
