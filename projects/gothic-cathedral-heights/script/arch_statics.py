"""Thrust lines of a circular masonry arch under its own weight (stdlib only).

Follows the method of Block, DeJong and Ochsendorf, "As Hangs the Flexible Line", Nexus Network Journal 8(2),
2006: limit analysis (no tension, no crushing, no sliding), an arch of many small voussoirs, the line of thrust
as the locus of pressure points on the joints. Used for the geometry of one card (B40), and checked in the tests
against the values printed in that paper (figures 4 and 5). This is an illustration of the published example,
not an analysis of any building.

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


def spread_state(half_angle, t, hinge_angle, span_increase):
    """The half arch when each support has moved out by span_increase / 2 of the original span.

    The stones between the haunch hinge and the support move with the support; the stones above the hinge turn
    about it, and the crown hinge stays on the axis. Returns the geometry and the thrust that passes through the
    two hinges. A joint's pressure point is measured along that joint, in the frame of its own rigid part.
    """
    a, ah = math.radians(half_angle), math.radians(hinge_angle)
    t2 = t / 2
    span = 2 * math.sin(a)
    d = span * span_increase / 2
    # hinges: crown on the extrados, haunch on the intrados
    px, py = (1 - t2) * math.sin(ah), (1 - t2) * math.cos(ah)
    cx, cy = 0.0, 1 + t2
    arm = math.hypot(cx - px, cy - py)
    moved_px = px + d
    if moved_px >= arm:
        return None
    new_cy = py + math.sqrt(arm * arm - moved_px * moved_px)
    before = math.atan2(cx - px, cy - py)                # hinge-to-crown, clockwise from vertical
    after = math.atan2(-moved_px, new_cy - py)
    phi = before - after                                 # rotation of the upper part, counter-clockwise positive

    def upper(x, y):
        dx, dy = x - px, y - py
        return moved_px + dx * math.cos(phi) - dy * math.sin(phi), py + dx * math.sin(phi) + dy * math.cos(phi)

    def lower(x, y):
        return x + d, y

    blocks, joints = _blocks(half_angle, t)
    hinge_joint = min(range(len(joints)), key=lambda k: abs(joints[k] - ah))
    # weight of the upper part about the haunch hinge fixes the thrust through both hinges
    w_up = sum(b[0] for b in blocks[:hinge_joint])
    x_up = sum(b[0] * upper(b[1], b[2])[0] for b in blocks[:hinge_joint]) / w_up
    h = w_up * (moved_px - x_up) / (new_cy - py)
    # pressure point on every joint, in the deformed geometry
    radii, weight, moment = [1 + t2], 0.0, 0.0
    for k, (w, x, y) in enumerate(blocks):
        move = upper if k < hinge_joint else lower
        weight += w
        moment += w * move(x, y)[0]
        angle = joints[k + 1]
        transform = upper if k + 1 <= hinge_joint else lower
        ix, iy = transform((1 - t2) * math.sin(angle), (1 - t2) * math.cos(angle))
        ox, oy = transform((1 + t2) * math.sin(angle), (1 + t2) * math.cos(angle))
        # resultant through (moment / weight, new_cy) with direction (h, -weight); find it on the joint
        rx, ry = moment / weight, new_cy
        ex, ey = ox - ix, oy - iy
        denom = ex * weight + ey * h
        s = ((rx - ix) * weight + (ry - iy) * h) / denom      # 0 at the intrados, 1 at the extrados
        radii.append(1 - t2 + s * t)
    return {"h": h, "radii": radii, "joints": joints, "hinge_joint": hinge_joint, "phi": phi, "d": d, "upper": upper,
            "lower": lower, "crown_y": new_cy}


def collapse_span_increase(half_angle, t, hinge_angle):
    """The largest span increase for which the line stays inside the deformed arch (bisection). The hinge stays on
    one joint, a simplification that lets the line graze the intrados just above it: 0.1% of the radius is allowed
    there. The limit itself is the line reaching the extrados at the support, as in the paper's figure 5(c)."""
    def inside(increase):
        state = spread_state(half_angle, t, hinge_angle, increase)
        return bool(state) and state["h"] > 0 and max(state["radii"]) <= 1 + t / 2 and min(state["radii"]) >= 1 - t / 2 - 1e-3
    lo, hi = 0.0, 0.6
    for _ in range(50):
        mid = (lo + hi) / 2
        if inside(mid):
            lo = mid
        else:
            hi = mid
    return lo
