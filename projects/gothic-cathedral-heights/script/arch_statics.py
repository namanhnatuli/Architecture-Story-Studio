"""Thrust lines of a circular masonry arch under its own weight (stdlib only).

Limit analysis (no tension, no crushing, no sliding) of an arch of many small voussoirs, with the line of thrust as
the locus of pressure points on the joints. The behaviour on spreading supports follows Ochsendorf's dissertation,
"Collapse of masonry structures" (Cambridge, 2002), chapter 5 and program ArchSpread; the example drawn on card B40
comes from Block, DeJong and Ochsendorf, "As Hangs the Flexible Line", Nexus Network Journal 8(2), 2006. The tests
compare this code with the published results. This illustrates a published example; it analyses no building.

Coordinates: radius R = 1, centre at the origin, crown on the +y axis; t = thickness / radius; `half_angle` =
half the angle of embrace, in degrees. A joint is named by its angle from the crown. Only the right half is
computed; the arch and its supports are symmetric.
"""
import math

N = 400   # voussoirs per half arch: enough for the published values to three figures


def _ring_block(a0, a1, t):
    """Weight (area) and centroid of a ring sector between joints a0 and a1 (radians from the crown)."""
    ri, ro = 1 - t / 2, 1 + t / 2
    area = (a1 - a0) * (ro * ro - ri * ri) / 2
    rc = 2 * (ro ** 3 - ri ** 3) / (3 * (ro * ro - ri * ri)) * math.sin((a1 - a0) / 2) / ((a1 - a0) / 2)
    mid = (a0 + a1) / 2
    return area, rc * math.sin(mid), rc * math.cos(mid)


def _blocks(half_angle, t):
    a = math.radians(half_angle)
    return [_ring_block(a * k / N, a * (k + 1) / N, t) for k in range(N)], [a * k / N for k in range(N + 1)]


def line_radii(half_angle, t, crown_r, h):
    """Radius of the pressure point on each joint, for a thrust h at the crown acting at radius crown_r."""
    blocks, joints = _blocks(half_angle, t)
    out, weight, moment = [crown_r], 0.0, 0.0
    for (w, x, _y), angle in zip(blocks, joints[1:]):
        weight += w
        moment += w * x
        out.append((crown_r + moment / h) / (math.cos(angle) + weight / h * math.sin(angle)))
    return out, joints


def half_weight(half_angle, t):
    return sum(b[0] for b in _blocks(half_angle, t)[0])


def fits(radii, t, tol=1e-6):
    return all(1 - t / 2 - tol <= r <= 1 + t / 2 + tol for r in radii)


def crown_interval(half_angle, t, h):
    """The radii at the crown for which a line with thrust h stays inside: (low, high), empty when low > high."""
    blocks, joints = _blocks(half_angle, t)
    ri, ro = 1 - t / 2, 1 + t / 2
    low, high, weight, moment = ri, ro, 0.0, 0.0
    for (w, x, _y), angle in zip(blocks, joints[1:]):
        weight += w
        moment += w * x
        slope = math.cos(angle) + weight / h * math.sin(angle)
        low = max(low, ri * slope - moment / h)
        high = min(high, ro * slope - moment / h)
    return low, high


def thrust_range(half_angle, t):
    """The valid lines of the arch at rest. Returns {"min", "max", "middle"}, each (crown radius, thrust)."""
    def bound(a, b):
        for _ in range(70):
            mid = (a + b) / 2
            low, high = crown_interval(half_angle, t, mid)
            if low <= high:
                a = mid
            else:
                b = mid
        return a
    # a thrust that fits, found by scanning; the arch is too thin to stand if there is none
    def opens(h):
        low, high = crown_interval(half_angle, t, h)
        return low <= high
    start = next((k / 2000 for k in range(1, 4000) if opens(k / 2000)), None)
    if start is None:
        raise ValueError("no thrust line fits this arch")
    h_min, h_max = bound(start, 1e-4), bound(start, 20.0)
    h_mid = (h_min + h_max) / 2
    return {"min": (crown_interval(half_angle, t, h_min)[1], h_min), "max": (crown_interval(half_angle, t, h_max)[0], h_max),
            "middle": (sum(crown_interval(half_angle, t, h_mid)) / 2, h_mid)}


def minimum_thrust_hinge(half_angle, t):
    """Angle in degrees of the joint where the minimum-thrust line touches the intrados."""
    crown, h = thrust_range(half_angle, t)["min"]
    radii, joints = line_radii(half_angle, t, crown, h)
    return math.degrees(joints[min(range(len(radii)), key=lambda k: radii[k])])


def initial_hinge(half_angle, t, voussoir):
    """The joint that gives the largest thrust with the crown hinge on the extrados: the hinge at minimum thrust.
    Returns (hinge angle in degrees, thrust)."""
    r1, r2 = 1 - t / 2, 1 + t / 2
    rad = (r1 ** 3 - r2 ** 3) / (r1 ** 2 - r2 ** 2)
    best, hinge = 0.0, voussoir
    for k in range(1, int(round(half_angle / voussoir)) + 1):
        angle = math.radians(k * voussoir)
        xa, ya = r1 * math.sin(angle), r1 * math.cos(angle)
        xm = 4 / 3 * rad * math.sin(angle / 2) / angle * math.sin(angle / 2)
        mass = angle * (r2 ** 2 - r1 ** 2) / 2
        thrust = mass * (xa - xm) / (r2 - ya)
        if thrust > best:
            best, hinge = thrust, k * voussoir
    return hinge, best


def spread_to_collapse(half_angle, t, voussoir=0.1, steps=1000, stop_at=None):
    """Follows an arch on spreading supports to the five-hinge collapse, after Ochsendorf, 'Collapse of masonry
    structures' (Cambridge PhD, 2002), Figure 5.11 and program ArchSpread, Appendix A.1. In that program's frame the
    support side stays still and the crown moves. The span increase is measured on the intrados span, (2R - t) sin(a),
    as the program does; each support takes half of it. The intrados hinge moves toward the crown whenever the locus of
    pressure points would otherwise leave the intrados one voussoir above it; collapse is the locus reaching the
    extrados at the support. steps = 1000 as in the program; the hinge moves at most one voussoir per step, so the
    result depends slightly on it for small arches (8.2% at 1000 steps, 7.8% at 20000, in the thesis's table 5.3 case).
    stop_at: stop at that span increase and return the state there."""
    a = math.radians(half_angle)
    r1, r2 = 1 - t / 2, 1 + t / 2
    rad = (r1 ** 3 - r2 ** 3) / (r1 ** 2 - r2 ** 2)
    span = 2 * r1 * math.sin(a)
    xd, yd = r2 * math.sin(a), r2 * math.cos(a)
    v = math.radians(voussoir)
    start, thrust_min = initial_hinge(half_angle, t, voussoir)
    q, n = 0, round(start / voussoir)

    def part(p):
        """Hinge A, the upper part's weight and centroid at rest, the capacity of the support part."""
        xa, ya = r1 * math.sin(p), r1 * math.cos(p)
        m1 = p * (r2 ** 2 - r1 ** 2) / 2
        c1 = 4 / 3 * rad * math.sin(p / 2) / p
        m2 = (a - p) * (r2 ** 2 - r1 ** 2) / 2
        xm2 = 4 / 3 * rad * math.sin((a - p) / 2) / (a - p) * math.sin((a + p) / 2)
        hmax = (m2 * (xd - xm2) + m1 * (xd - xa)) / (ya - yd)
        return xa, ya, m1, c1, hmax

    def geometry(p, xa, ya, xc):
        """Crown position, rotation of the upper part and its turned circle centre, for a crown shift xc (negative)."""
        lac = math.hypot(xa, r2 - ya)
        phi0 = math.atan((r2 - ya) / xa)
        if lac * lac <= (xa - xc) ** 2:
            return None
        yc = math.sqrt(lac * lac - (xa - xc) ** 2) + ya
        phi = phi0 - math.asin((yc - ya) / lac)
        return yc, phi, xa - r1 * math.sin(p - phi), ya - r1 * math.cos(p - phi)

    p = n * v
    xa, ya, m1, c1, hmax = part(p)
    limit_xc = math.hypot(xa, r2 - ya) - xa
    state = None
    for c in range(1, steps + 1):
        xc = -limit_xc * c / steps
        if stop_at is not None and -2 * xc / span > stop_at:
            break
        g = geometry(p, xa, ya, xc)
        if g is None:
            raise ValueError("snap-through before the five-hinge collapse")
        yc, phi, x0, y0 = g
        xm1 = x0 + c1 * math.cos(math.pi / 2 - p / 2 + phi)
        thrust = m1 * (xa - xm1) / (yc - ya)
        if thrust > hmax:
            break
        # does the locus leave the intrados one voussoir above the hinge? if so the hinge moves toward the crown
        cv = 4 / 3 * rad * math.sin(v / 2) / v
        xv = x0 + cv * math.cos(math.pi / 2 - p + v / 2 + phi)
        m = v * (r2 ** 2 - r1 ** 2) / 2
        angle = math.pi / 2 - p + v + phi
        rf = ((m1 - m) * (xa - x0) + thrust * (ya - y0) - m * (xv - xa)) / (thrust * math.sin(angle) + (m1 - m) * math.cos(angle))
        if rf < r1:
            q += 1
            p = (n - q) * v
            xa, ya, m1, c1, hmax = part(p)
            g = geometry(p, xa, ya, xc)
            if g is None:
                raise ValueError("snap-through before the five-hinge collapse")
            yc, phi, x0, y0 = g
            xm1 = x0 + c1 * math.cos(math.pi / 2 - p / 2 + phi)
            thrust = m1 * (xa - xm1) / (yc - ya)
            if thrust > hmax:
                break
        state = {"span_increase": -2 * xc / span, "hinge": math.degrees(p), "initial_hinge": start, "thrust": thrust,
                 "thrust_ratio": thrust / thrust_min, "thrust_min": thrust_min, "capacity": hmax, "phi": phi,
                 "crown_y": yc, "dip": (r2 - yc) / t, "shift": -xc, "x0": x0, "y0": y0, "xa": xa, "ya": ya}
    return state


def spread_shape(half_angle, t, state):
    """For drawing, symmetric about the crown: each support moves out by half the crown shift. Returns the transforms
    of the upper and the lower part, and the pressure point on every joint (one per voussoir of 0.2 degrees) in the
    frame of its own part, from the equilibrium of the deformed arch. This is written separately from the collapse
    test above, so a test can compare the two."""
    a, p = math.radians(half_angle), math.radians(state["hinge"])
    phi, shift = state["phi"], state["shift"]
    x0, y0 = state["x0"], state["y0"]

    def upper(x, y):
        """A point of the upper part at rest -> the deformed arch, crown on the axis."""
        return x0 + x * math.cos(phi) - y * math.sin(phi) + shift, y0 + x * math.sin(phi) + y * math.cos(phi)

    def lower(x, y):
        return x + shift, y

    joints = [a * k / 400 for k in range(401)]
    hinge_joint = min(range(len(joints)), key=lambda k: abs(joints[k] - p))
    joints[hinge_joint] = p
    r1, r2 = 1 - t / 2, 1 + t / 2
    crown = upper(0.0, r2)
    radii, weight, moment = [r2], 0.0, 0.0
    for k in range(400):
        move = upper if k < hinge_joint else lower
        w, x, y = _ring_block(joints[k], joints[k + 1], t)
        weight += w
        moment += w * move(x, y)[0]
        joint_move = upper if k + 1 <= hinge_joint else lower
        ix, iy = joint_move(r1 * math.sin(joints[k + 1]), r1 * math.cos(joints[k + 1]))
        ox, oy = joint_move(r2 * math.sin(joints[k + 1]), r2 * math.cos(joints[k + 1]))
        rx, ry = moment / weight, crown[1]
        ex, ey = ox - ix, oy - iy
        s = ((rx - ix) * weight + (ry - iy) * state["thrust"]) / (ex * weight + ey * state["thrust"])
        radii.append(r1 + s * t)
    return {"upper": upper, "lower": lower, "radii": radii, "joints": joints, "hinge_joint": hinge_joint, "crown": crown}
