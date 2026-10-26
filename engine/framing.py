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


def fit_ortho(points, basis, aspect, margin=0.07, bottom_band=0.0, clearance=10.0):
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
    location = tuple(cx * r + cy * u + depth * f for r, u, f in zip(right, up, forward))
    # Clip far enough for an "infinite" ground plane, not just the framed subject.
    return {"location": location, "ortho_scale": ortho, "clip_start": 0.1,
            "clip_end": max((max(zs) - depth) + clearance, 1000.0)}


def frame_coords(points, fit, basis, aspect):
    """Normalised (x, y) frame coordinates, 0..1 inside the frame (like world_to_camera_view)."""
    right, up, _ = basis
    ortho = fit["ortho_scale"]
    lx, ly = _dot(fit["location"], right), _dot(fit["location"], up)
    return [((_dot(p, right) - lx) / ortho + 0.5, (_dot(p, up) - ly) / (ortho / aspect) + 0.5)
            for p in points]


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
