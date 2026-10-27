"""Reusable architectural utilities (pure Python). Family generators compose these;
none of them knows about bridges specifically.

Conventions: metres; X along the structure, Y across, Z up.
"""
import math

from engine.arch import primitives as P

JOINT_GAP = 0.012   # visible mortar/plank joint between neighbouring units (m)


def spaced(start, end, count):
    """`count` evenly spaced positions from start to end inclusive."""
    if count < 1:
        raise ValueError("count must be >= 1")
    if count == 1:
        return [(start + end) / 2.0]
    return [start + (end - start) * i / (count - 1) for i in range(count)]


def repeat_along_x(make, x0, x1, pitch, gap=JOINT_GAP):
    """Units of width `pitch - gap` filling x0..x1 (the last unit is trimmed to fit).
    `make(center_x, width)` returns a mesh. Returns (merged mesh, unit count)."""
    meshes, x = [], x0
    while x < x1 - 1e-6:
        w = min(pitch, x1 - x) - gap
        if w > gap:
            meshes.append(make(x + w / 2.0, w))
        x += pitch
    return P.merge(*meshes), len(meshes)


def post(height, size, base=(0.0, 0.0, 0.0)):
    """Square timber/steel post standing on `base`."""
    return P.box((size, size, height), (base[0], base[1], base[2] + height / 2.0))


def beam_x(x0, x1, y, z_top, width, depth):
    """Beam along X with its top face at z_top."""
    return P.box((x1 - x0, width, depth), ((x0 + x1) / 2.0, y, z_top - depth / 2.0))


def beam_y(y0, y1, x, z_top, width, depth):
    """Beam across (along Y) with its top face at z_top."""
    return P.box((width, y1 - y0, depth), (x, (y0 + y1) / 2.0, z_top - depth / 2.0))


def x_brace(xa, xb, y, z0, z1, size):
    """Two crossing diagonal braces in the XZ plane at y (e.g. between posts)."""
    return P.merge(P.member((xa, y, z0), (xb, y, z1), size, size),
                   P.member((xa, y, z1), (xb, y, z0), size, size))


def x_brace_y(ya, yb, x, z0, z1, size):
    """Two crossing diagonal braces in the YZ plane at x (between posts of a bent)."""
    return P.merge(P.member((x, ya, z0), (x, yb, z1), size, size, side=(1, 0, 0)),
                   P.member((x, ya, z1), (x, yb, z0), size, size, side=(1, 0, 0)))


# ---------------------------------------------------------------- masonry arches
def arch_angles(count):
    """Angular ranges (a0, a1) of `count` voussoirs over a semicircle, from the left
    springing (pi) to the right springing (0). Odd counts put a keystone at the crown."""
    if count < 3 or count % 2 == 0:
        raise ValueError("voussoir count must be an odd number >= 3 (keystone at the crown)")
    step = math.pi / count
    return [(math.pi - i * step, math.pi - (i + 1) * step) for i in range(count)]


def voussoir_mesh(radius, ring, depth, half_angle, segments=3, gap=JOINT_GAP):
    """One wedge centred on the crown direction (+Z) in arch-centre space; place it by
    rotating about Y. The joint gap is removed from both bed faces."""
    trim = (gap / 2.0) / radius
    return P.sector(radius, radius + ring, math.pi / 2 - half_angle + trim, math.pi / 2 + half_angle - trim,
                    depth, segments)


def keystone_mesh(radius, ring, depth, half_angle, proud=0.06, drop=0.05, segments=3, gap=JOINT_GAP):
    """Crown voussoir: proud of both faces and dropped below the intrados (a common,
    readable detail); its extrados stays flush so it never cuts into the spandrel."""
    trim = (gap / 2.0) / radius
    return P.sector(radius - drop, radius + ring, math.pi / 2 - half_angle + trim,
                    math.pi / 2 + half_angle - trim, depth + 2 * proud, segments)


def rotation_for_angle(theta):
    """Euler rotation about Y that turns the crown direction (+Z, pi/2) to angle theta."""
    return (0.0, math.pi / 2 - theta, 0.0)


def spandrel_outline(x0, x1, z_bottom, z_top, arches, segments=24):
    """Outline (XZ) of masonry between springing level and z_top over a row of
    semicircular arches [(centre_x, centre_z, extrados_radius)], walking left to right
    along the bottom (arch extrados and pier tops) and back along the top."""
    pts = [(x0, z_bottom)]
    for cx, cz, r in arches:
        pts.append((cx - r, cz))
        pts += P.arc_points(cx, cz, r, math.pi, 0.0, segments)[1:-1]
        pts.append((cx + r, cz))
    pts += [(x1, z_bottom), (x1, z_top), (x0, z_top)]
    return _dedupe(pts)


def _dedupe(pts, tol=1e-6):
    out = []
    for p in pts:
        if not out or abs(out[-1][0] - p[0]) > tol or abs(out[-1][1] - p[1]) > tol:
            out.append(p)
    if len(out) > 1 and abs(out[0][0] - out[-1][0]) < tol and abs(out[0][1] - out[-1][1]) < tol:
        out.pop()
    return out


def cutwater_outline(half_width, nose):
    """Plan-view triangle (X, Y) of a pier cutwater pointing along -Y (upstream)."""
    return [(-half_width, 0.0), (half_width, 0.0), (0.0, -nose)]


def prism_xy(outline, z0, z1):
    """Plan polygon [(x, y)] extruded vertically from z0 to z1."""
    n = len(outline)
    verts = [(x, y, z) for z in (z0, z1) for x, y in outline]
    faces = [tuple(reversed(range(n))), tuple(n + i for i in range(n))]
    faces += [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)]
    return {"verts": verts, "faces": faces}


# ---------------------------------------------------------------- trusses
TRUSS_PATTERNS = ("pratt", "warren")


def truss_nodes(length, height, panels, z_bottom=0.0):
    """Bottom and top chord node positions (x, z) of a parallel-chord truss centred on x=0."""
    xs = spaced(-length / 2.0, length / 2.0, panels + 1)
    return [(x, z_bottom) for x in xs], [(x, z_bottom + height) for x in xs]


def truss_web(pattern, bottom, top):
    """Web members [(kind, (x0, z0), (x1, z1))] for a parallel-chord truss.

    pratt:  verticals at every interior node; diagonals slope down towards the centre
            (Wikipedia "Truss bridge": "vertical members and diagonals that slope down
            towards the center").
    warren: diagonals alternate up/down between chord nodes (triangles), no interior
            verticals (isosceles here, so both patterns share the same chords and nodes).
    End posts (verticals at both ends) belong to the shared frame, not the web."""
    n = len(bottom) - 1
    if n < 2 or n % 2:
        raise ValueError("truss panels must be an even number >= 2")
    web = []
    if pattern == "pratt":
        for i in range(1, n):
            web.append(("TRUSS_VERTICAL", bottom[i], top[i]))
        for i in range(n):
            if i < n // 2:
                web.append(("TRUSS_DIAGONAL", top[i], bottom[i + 1]))
            else:
                web.append(("TRUSS_DIAGONAL", top[i + 1], bottom[i]))
    elif pattern == "warren":
        for i in range(n):
            a, b = (bottom[i], top[i + 1]) if i % 2 == 0 else (top[i], bottom[i + 1])
            web.append(("TRUSS_DIAGONAL", a, b))
    else:
        raise ValueError(f"unknown truss pattern {pattern!r} (known: {', '.join(TRUSS_PATTERNS)})")
    return web


def truss_members_mesh(members, y, width, depth):
    """Merged bars for [(kind, (x0, z0), (x1, z1))] in the XZ plane at y."""
    return P.merge(*[P.member((a[0], y, a[1]), (b[0], y, b[1]), width, depth) for _, a, b in members])


def gusset(x, z, y, size, thickness):
    """Square connection plate on a truss face (Y-normal)."""
    return P.box((size, thickness, size), (x, y, z))
