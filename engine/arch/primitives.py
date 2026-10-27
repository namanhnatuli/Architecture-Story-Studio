"""Mesh primitives as plain data: {"verts": [(x, y, z)], "faces": [(i, ...)]} (no bpy).

Conventions (metres): X along the structure (span), Y across it (width), Z up.
Faces may be n-gons; face winding is made consistent in Blender (realize.py).
"""
import math


def merge(*meshes):
    verts, faces = [], []
    for m in meshes:
        base = len(verts)
        verts += list(m["verts"])
        faces += [tuple(base + i for i in f) for f in m["faces"]]
    return {"verts": verts, "faces": faces}


def translate(mesh, offset):
    ox, oy, oz = offset
    return {"verts": [(x + ox, y + oy, z + oz) for x, y, z in mesh["verts"]], "faces": list(mesh["faces"])}


def box(size, center=(0.0, 0.0, 0.0)):
    sx, sy, sz = (s / 2.0 for s in size)
    cx, cy, cz = center
    verts = [(cx + dx * sx, cy + dy * sy, cz + dz * sz)
             for dz in (-1, 1) for dy in (-1, 1) for dx in (-1, 1)]
    faces = [(0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)]
    return {"verts": verts, "faces": faces}


def _sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def _cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def _norm(a):
    n = math.sqrt(sum(x * x for x in a))
    if n < 1e-9:
        raise ValueError("zero-length vector")
    return tuple(x / n for x in a)


def member(p0, p1, width, height, side=(0.0, 1.0, 0.0)):
    """Rectangular bar from p0 to p1. `width` is measured along `side` (projected
    perpendicular to the bar), `height` along the third axis. Used for beams,
    truss members, braces and rails."""
    u = _norm(_sub(p1, p0))
    s = tuple(c - u[i] * sum(side[j] * u[j] for j in range(3)) for i, c in enumerate(side))
    v = _norm(s)
    w = _cross(u, v)
    hv, hw = width / 2.0, height / 2.0
    verts = []
    for p in (p0, p1):
        for a, b in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
            verts.append(tuple(p[i] + a * hv * v[i] + b * hw * w[i] for i in range(3)))
    faces = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    return {"verts": verts, "faces": faces}


def sector(r_in, r_out, a0, a1, depth, segments=4, center=(0.0, 0.0, 0.0)):
    """Annular sector (voussoir) in the XZ plane between angles a0..a1 (radians,
    0 = +X, pi/2 = +Z), extruded `depth` along Y and centred on `center`."""
    if not 0 < r_in < r_out:
        raise ValueError("sector needs 0 < r_in < r_out")
    cx, cy, cz = center
    verts = []
    for y in (-depth / 2.0, depth / 2.0):
        for r in (r_in, r_out):
            for k in range(segments + 1):
                a = a0 + (a1 - a0) * k / segments
                verts.append((cx + r * math.cos(a), cy + y, cz + r * math.sin(a)))
    n = segments + 1
    idx = lambda side, ring, k: side * 2 * n + ring * n + k   # side 0/1 (y), ring 0 inner / 1 outer
    faces = []
    for side in (0, 1):  # caps: outer arc forward, inner arc back
        faces.append(tuple([idx(side, 1, k) for k in range(n)] + [idx(side, 0, k) for k in reversed(range(n))]))
    for k in range(segments):
        faces.append((idx(0, 0, k), idx(0, 0, k + 1), idx(1, 0, k + 1), idx(1, 0, k)))   # intrados
        faces.append((idx(0, 1, k), idx(1, 1, k), idx(1, 1, k + 1), idx(0, 1, k + 1)))   # extrados
    for k in (0, segments):  # joint faces (bed joints)
        faces.append((idx(0, 0, k), idx(1, 0, k), idx(1, 1, k), idx(0, 1, k)))
    return {"verts": verts, "faces": faces}


def prism_xz(outline, depth, y_center=0.0):
    """Polygon outline [(x, z), ...] (simple, any winding) extruded along Y."""
    if len(outline) < 3:
        raise ValueError("prism needs at least 3 outline points")
    n = len(outline)
    verts = [(x, y_center + y, z) for y in (-depth / 2.0, depth / 2.0) for x, z in outline]
    faces = [tuple(range(n)), tuple(n + i for i in reversed(range(n)))]
    faces += [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)]
    return {"verts": verts, "faces": faces}


def cylinder_z(radius, height, segments=16, center=(0.0, 0.0, 0.0)):
    """Vertical cylinder (posts, rivet heads); base at center z - height/2."""
    cx, cy, cz = center
    verts = []
    for z in (cz - height / 2.0, cz + height / 2.0):
        for k in range(segments):
            a = 2 * math.pi * k / segments
            verts.append((cx + radius * math.cos(a), cy + radius * math.sin(a), z))
    n = segments
    faces = [tuple(reversed(range(n))), tuple(range(n, 2 * n))]
    faces += [(k, (k + 1) % n, n + (k + 1) % n, n + k) for k in range(n)]
    return {"verts": verts, "faces": faces}


def arc_points(cx, cz, radius, a0, a1, segments):
    """Points on a circular arc in the XZ plane, a0 -> a1 inclusive."""
    return [(cx + radius * math.cos(a0 + (a1 - a0) * k / segments),
             cz + radius * math.sin(a0 + (a1 - a0) * k / segments)) for k in range(segments + 1)]
