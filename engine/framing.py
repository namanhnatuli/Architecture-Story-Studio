"""Pure-Python camera framing and comparison layout maths (no bpy).

The camera direction comes from a named preset (azimuth/elevation); position and
orthographic scale are fitted to the actual geometry, so the same code frames a
house, a bridge or two models side by side. Blender-side code only converts the
returned basis/location into a matrix.
"""
import math


def _dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def _cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def _unit(a):
    n = math.sqrt(_dot(a, a))
    if n < 1e-12:
        raise ValueError("zero-length vector")
    return tuple(x / n for x in a)


def camera_basis(azimuth_degrees, elevation_degrees):
    """(right, up, forward) unit vectors for a level camera looking at the scene.

    Azimuth/elevation give the direction from the subject towards the camera.
    """
    az, el = math.radians(azimuth_degrees), math.radians(elevation_degrees)
    if not -89.0 < elevation_degrees < 89.0:
        raise ValueError("elevation must be between -89 and 89 degrees")
    forward = (-math.cos(el) * math.cos(az), -math.cos(el) * math.sin(az), -math.sin(el))
    right = _unit(_cross(forward, (0.0, 0.0, 1.0)))
    up = _cross(right, forward)
    return right, up, forward


def fit_ortho(points, basis, aspect, margin=0.07, bottom_band=0.0, clearance=10.0, ground_z=-0.38):
    """Orthographic camera that frames every point with a margin.

    margin is a fraction of the frame on each side; bottom_band is an extra
    fraction kept free at the bottom (future labels). Returns location,
    ortho_scale (frame width, as Blender uses for landscape frames) and clipping.
    """
    if not points:
        raise ValueError("cannot frame an empty set of points")
    right, up, forward = basis
    xs = [_dot(p, right) for p in points]
    ys = [_dot(p, up) for p in points]
    zs = [_dot(p, forward) for p in points]
    usable_w = 1.0 - 2.0 * margin
    usable_h = 1.0 - 2.0 * margin - bottom_band
    if usable_w <= 0 or usable_h <= 0:
        raise ValueError("margins leave no room for the subject")
    width, height = max(xs) - min(xs), max(ys) - min(ys)
    ortho = max(width / usable_w, height / usable_h * aspect, 1e-3)
    frame_h = ortho / aspect
    cx = (min(xs) + max(xs)) / 2.0
    cy = (min(ys) + max(ys)) / 2.0 - bottom_band * frame_h / 2.0
    depth = min(zs) - clearance
    # The bottom edge of a tall orthographic frame can sit below the ground plane; rays
    # starting there never hit the ground (a background-coloured band). Moving the camera
    # back along its own view axis changes nothing in an orthographic projection except
    # that, so push it back until the lowest frame corner is above the ground.
    if ground_z is not None and forward[2] < -0.1:
        frame_bottom = cy - (ortho / aspect) / 2.0
        low = depth * forward[2] + cx * right[2] + frame_bottom * up[2]
        if low < ground_z + 1.0:
            depth -= (ground_z + 1.0 - low) / -forward[2]
    location = tuple(cx * r + cy * u + depth * f for r, u, f in zip(right, up, forward))
    # pivot: the frame centre at the subject's mid depth; location = pivot - distance * forward (camera orbits)
    mid = (min(zs) + max(zs)) / 2.0
    pivot = tuple(cx * r + cy * u + mid * f for r, u, f in zip(right, up, forward))
    # Clip far enough for an "infinite" ground plane, not just the framed subject.
    return {"location": location, "ortho_scale": ortho, "clip_start": 0.1,
            "clip_end": max((max(zs) - depth) + clearance, 1000.0), "pivot": pivot, "distance": mid - depth}


def view_fits(views, points_of, preset, aspect, band=0.0):
    """SEQUENCE: one orthographic fit per view (engine/shot_builder and planner/visibility share it). A view looks
    from the preset's direction unless it gives its own azimuth/elevation (an orbit); points_of(focus) returns the
    rest vertices of the view's focus parts (every built part when focus is None)."""
    fits = []
    for k, v in enumerate(views):
        az = preset["azimuth_degrees"] if v.get("azimuth") is None else float(v["azimuth"])
        el = preset["elevation_degrees"] if v.get("elevation") is None else float(v["elevation"])
        if el < 0 and not preset.get("hide_ground"):
            raise ValueError(f"view {k} looks from below the ground (elevation {el:g}): use a camera preset with "
                             "hide_ground")
        pts = points_of(v.get("focus"))
        if not pts:
            raise ValueError(f"view focus {sorted(v.get('focus') or [])} matches no built part")
        basis = camera_basis(az, el)
        margin = v["margin"] if v.get("margin") is not None else preset.get("margin", 0.07)
        clearance = 10.0 if v.get("clearance") is None else float(v["clearance"])   # R3: a close view among buildings
        fit = fit_ortho(pts, basis, aspect, margin, band, clearance=clearance)
        fit.update(azimuth=az, elevation=el, rotation=camera_euler(basis))
        fits.append(fit)
    return fits


def camera_euler(basis):
    """Blender rotation_euler (XYZ, radians) of a level camera with this (right, up, forward) basis: the camera
    looks down its local -Z with local +Y up. A level camera has no Y rotation."""
    right, up, forward = basis
    return (math.atan2(up[2], -forward[2]), 0.0, math.atan2(right[1], right[0]))


def basis_from_euler(euler):
    """Inverse of camera_euler for a level camera (Y rotation 0)."""
    x, _, z = euler
    cx, sx, cz, sz = math.cos(x), math.sin(x), math.cos(z), math.sin(z)
    right = (cz, sz, 0.0)
    up = (-sz * cx, cz * cx, sx)
    forward = (-sz * sx, cz * sx, -cx)
    return right, up, forward


ORBIT_FULL_BACK_AWAY_DEGREES = 20.0   # a turn this large (azimuth + elevation) backs away by the larger distance


def orbit_back_away(a, b):
    """How far the camera backs away mid-orbit (at s = 0.5): the larger of the two distances for a turn of
    ORBIT_FULL_BACK_AWAY_DEGREES or more, proportionally less for a smaller turn, nothing when the direction does not
    change (then the move is a straight slide and cannot pass through the subject)."""
    turn = abs(b["azimuth"] - a["azimuth"]) + abs(b["elevation"] - a["elevation"])
    return min(1.0, turn / ORBIT_FULL_BACK_AWAY_DEGREES) * max(a["distance"], b["distance"])


def sequence_clip_end(fits):
    """A SEQUENCE camera's far clip: every view's own, plus the most the camera backs away between two views, so a
    pull-back mid-move never clips the far ground (it showed as a flat background band, R3 opening)."""
    ends = [f.get("clip_end", 1000.0) for f in fits]
    extra = max((orbit_back_away(a, b) for a, b in zip(fits, fits[1:])
                 if all(a.get(k) is not None and b.get(k) is not None for k in ("azimuth", "elevation", "distance"))),
                default=0.0)
    return max(ends) + extra


def orbit_pose(a, b, s):
    """Camera pose at progress s (0..1, already eased) of an orbit between two view fits that carry azimuth,
    elevation, pivot and distance: the pivot, the angles and the scale are interpolated, and the camera backs away
    mid-move so it never passes through the subject. Returns (location, euler, ortho_scale); s = 0 and s = 1 give
    the two fits exactly."""
    az = a["azimuth"] + (b["azimuth"] - a["azimuth"]) * s
    el = a["elevation"] + (b["elevation"] - a["elevation"]) * s
    basis = camera_basis(az, el)
    pivot = tuple(p + (q - p) * s for p, q in zip(a["pivot"], b["pivot"]))
    dist = a["distance"] + (b["distance"] - a["distance"]) * s + 4.0 * s * (1.0 - s) * orbit_back_away(a, b)
    location = tuple(p - dist * f for p, f in zip(pivot, basis[2]))
    return location, camera_euler(basis), a["ortho_scale"] + (b["ortho_scale"] - a["ortho_scale"]) * s


def frame_coords(points, fit, basis, aspect):
    """Normalised (x, y) frame coordinates, 0..1 inside the frame (like world_to_camera_view)."""
    right, up, _ = basis
    ortho = fit["ortho_scale"]
    lx, ly = _dot(fit["location"], right), _dot(fit["location"], up)
    return [((_dot(p, right) - lx) / ortho + 0.5, (_dot(p, up) - ly) / (ortho / aspect) + 0.5)
            for p in points]


def frame_to_world(ux, uy, fit, basis, aspect, toward_camera=5.0):
    """World point at normalised frame position (ux, uy), `toward_camera` units in front of
    the camera's near side of the subject (inverse of frame_coords for an ortho camera)."""
    right, up, forward = basis
    ortho = fit["ortho_scale"]
    return tuple(c + r * (ux - 0.5) * ortho + u * (uy - 0.5) * ortho / aspect + f * toward_camera
                 for c, r, u, f in zip(fit["location"], right, up, forward))


def layout_stack(points_per_model, basis, gap_ratio):
    """SIDE_BY_SIDE layout "STACK": ground offsets placing models one behind another
    along the camera's horizontal forward axis so that, on screen, they form rows
    (first model on top) whose vertical extents never overlap. Needs an elevated
    camera (the screen-up shift per metre of depth is sin(elevation)).

    points_per_model: [[(x, y, z), ...], ...] at the origin. Returns (offsets, gap) where
    gap is in screen-up metres."""
    right, up, forward = basis
    g = _unit((forward[0], forward[1], 0.0))
    k = _dot(up, g)
    if k < 0.2:
        raise ValueError("STACK layout needs a camera elevation of at least ~12 degrees")
    extents = [(min(_dot(p, up) for p in pts), max(_dot(p, up) for p in pts)) for pts in points_per_model]
    gap = gap_ratio * max(hi - lo for lo, hi in extents)
    shifts, cursor = [], 0.0
    for lo, hi in extents:
        s = cursor - hi
        shifts.append(s)
        cursor = lo + s - gap
    mid = (shifts[0] + extents[0][1] + cursor + gap) / 2.0   # centre the stack on screen
    return [tuple(gi * (s - mid) / k for gi in g) for s in shifts], gap


def layout_side_by_side(footprints, axis, gap_ratio):
    """Ground offsets placing models in a row along `axis` (camera right on the ground).

    footprints: (min_x, min_y, max_x, max_y) per model in its own space. Spacing
    uses each model's projected extent, so models never overlap (their projections
    on the axis are disjoint) and the gap scales with the largest model.
    """
    if len(footprints) < 2:
        raise ValueError("side-by-side needs at least two models")
    if gap_ratio <= 0:
        raise ValueError("gap_ratio must be > 0")
    ax = _unit((axis[0], axis[1], 0.0))
    spans = []
    for x0, y0, x1, y1 in footprints:
        proj = [x * ax[0] + y * ax[1] for x in (x0, x1) for y in (y0, y1)]
        spans.append((min(proj), max(proj)))
    widths = [b - a for a, b in spans]
    gap = gap_ratio * max(widths)
    cursor = -(sum(widths) + gap * (len(widths) - 1)) / 2.0
    offsets = []
    for (a, _), w in zip(spans, widths):
        shift = cursor - a
        offsets.append((shift * ax[0], shift * ax[1], 0.0))
        cursor += w + gap
    return offsets, gap


def push_in_keys(fit, basis, aspect, points, amount):
    """M7 HOLD camera_move PUSH_IN: (start, end) camera keys. Start = the locked fit; end = the
    orthographic scale reduced by `amount`, shifted towards the centre of `points` (frame
    coordinates) but never past the start frame, so the end view lies inside the start view."""
    right, up, _ = basis
    coords = frame_coords(points, fit, basis, aspect) if points else [(0.5, 0.5)]
    cx = sum(x for x, _ in coords) / len(coords)
    cy = sum(y for _, y in coords) / len(coords)
    lim = amount / 2.0
    sx = max(-lim, min(lim, cx - 0.5))
    sy = max(-lim, min(lim, cy - 0.5))
    ortho = fit["ortho_scale"]
    loc = tuple(fit["location"][i] + right[i] * sx * ortho + up[i] * sy * ortho / aspect for i in range(3))
    return ({"location": tuple(fit["location"]), "ortho_scale": ortho},
            {"location": loc, "ortho_scale": ortho * (1.0 - amount)})
