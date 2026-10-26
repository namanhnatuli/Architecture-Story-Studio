"""Offline tests for camera framing and side-by-side layout maths (engine/framing.py)."""
import itertools
import math
import unittest

from engine import framing


def box(lo, hi):
    return [tuple(c) for c in itertools.product(*zip(lo, hi))]


class CameraBasisTest(unittest.TestCase):
    def test_orthonormal_and_level(self):
        r, u, f = framing.camera_basis(-52.13, 25.19)
        for a, b in ((r, u), (r, f), (u, f)):
            self.assertAlmostEqual(sum(x * y for x, y in zip(a, b)), 0.0)
        for v in (r, u, f):
            self.assertAlmostEqual(math.sqrt(sum(x * x for x in v)), 1.0)
        self.assertAlmostEqual(r[2], 0.0)  # no roll: screen right stays horizontal
        self.assertGreater(u[2], 0.0)

    def test_matches_v01_view_direction(self):
        _, _, f = framing.camera_basis(-52.13, 25.19)
        v01 = (-7.7, 9.9, -5.9)
        n = math.sqrt(sum(x * x for x in v01))
        self.assertTrue(all(abs(a - b / n) < 1e-3 for a, b in zip(f, v01)))


class FitOrthoTest(unittest.TestCase):
    def setUp(self):
        self.basis = framing.camera_basis(-52.13, 25.19)
        self.points = box((-2.5, -1.8, -0.4), (2.5, 1.8, 5.2))

    def test_everything_inside_with_margin_and_tight(self):
        fit = framing.fit_ortho(self.points, self.basis, 16 / 9, margin=0.07)
        coords = framing.frame_coords(self.points, fit, self.basis, 16 / 9)
        margins = [min(x, 1 - x, y, 1 - y) for x, y in coords]
        self.assertGreaterEqual(min(margins), 0.07 - 1e-9)
        self.assertAlmostEqual(min(margins), 0.07, places=6)  # no wasted zoom

    def test_bottom_band_is_kept_free(self):
        fit = framing.fit_ortho(self.points, self.basis, 16 / 9, margin=0.07, bottom_band=0.12)
        coords = framing.frame_coords(self.points, fit, self.basis, 16 / 9)
        self.assertGreaterEqual(min(y for _, y in coords), 0.19 - 1e-9)
        self.assertLessEqual(max(y for _, y in coords), 0.93 + 1e-9)

    def test_ground_plane_is_not_clipped(self):
        fit = framing.fit_ortho(self.points, self.basis, 16 / 9)
        self.assertGreaterEqual(fit["clip_end"], 1000.0)

    def test_bad_inputs(self):
        with self.assertRaises(ValueError):
            framing.fit_ortho([], self.basis, 16 / 9)
        with self.assertRaises(ValueError):
            framing.fit_ortho(self.points, self.basis, 16 / 9, margin=0.3, bottom_band=0.5)


class LayoutTest(unittest.TestCase):
    def spans(self, footprints, offsets, axis):
        out = []
        for (x0, y0, x1, y1), (dx, dy, _) in zip(footprints, offsets):
            proj = [(x + dx) * axis[0] + (y + dy) * axis[1] for x in (x0, x1) for y in (y0, y1)]
            out.append((min(proj), max(proj)))
        return out

    def test_houses_do_not_overlap_and_gap_scales(self):
        axis = framing.camera_basis(-52.13, 25.19)[0]
        fps = [(-2.5, -1.8, 2.5, 1.8)] * 2
        offsets, gap = framing.layout_side_by_side(fps, axis, 0.35)
        (a0, a1), (b0, b1) = self.spans(fps, offsets, axis)
        self.assertAlmostEqual(b0 - a1, gap)
        self.assertAlmostEqual(gap, 0.35 * (a1 - a0))
        self.assertAlmostEqual((a0 + b1) / 2, 0.0)  # row centred on the origin

    def test_different_sizes_like_a_bridge_and_a_column(self):
        axis = (1.0, 0.0)
        fps = [(-20, -2, 20, 2), (-0.5, -0.5, 0.5, 0.5), (-3, -3, 3, 3)]
        offsets, gap = framing.layout_side_by_side(fps, axis, 0.1)
        spans = self.spans(fps, offsets, axis)
        for (_, hi), (lo, _) in zip(spans, spans[1:]):
            self.assertAlmostEqual(lo - hi, gap)
        self.assertAlmostEqual(gap, 4.0)

    def test_invalid_layouts(self):
        with self.assertRaises(ValueError):
            framing.layout_side_by_side([(0, 0, 1, 1)], (1, 0), 0.3)
        with self.assertRaises(ValueError):
            framing.layout_side_by_side([(0, 0, 1, 1)] * 2, (1, 0), 0)


if __name__ == "__main__":
    unittest.main()
