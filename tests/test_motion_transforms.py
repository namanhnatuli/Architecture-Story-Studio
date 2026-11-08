"""SEQUENCE transform steps (engine/motion.py): MOVE (a calculated sink or rise), ROTATE (a small tilt about a pivot)
and OSCILLATE (conceptual motion, labelled), composed with REVEAL on the same part, never overlapping in time."""
import math
import unittest

from engine import motion, templates

CAM = {"name": templates.CAMERA_NAME}


def parts(*ids):
    return {i: motion.Component(name=i, id=i, location=(float(k), 0.0, 0.0), center=(float(k), 0.0, 0.0)) for k, i in enumerate(ids)}


def run(steps, frames=480, comps=None):
    plan = motion.Plan(24, frames)
    motion.plan_sequence(plan, comps or parts("a", "b"), {"template": "SEQUENCE", "state": "s", "steps": steps}, CAM)
    return plan


def at(plan, name, channel, seconds):
    return plan.sample(name, channel, plan.frame(seconds))


class TransformStepsTest(unittest.TestCase):
    def test_move_shifts_the_parts_by_the_offset_and_holds(self):
        p = run([{"do": "MOVE", "components": ["a", "b"], "start_seconds": 2.0, "seconds": 2.0, "offset": [0.0, 0.0, -0.332]}])
        self.assertAlmostEqual(at(p, "a", motion.LOC, 1.0)[2], 0.0, places=6)
        self.assertAlmostEqual(at(p, "a", motion.LOC, 4.0)[2], -0.332, places=6)
        self.assertAlmostEqual(at(p, "b", motion.LOC, 19.0)[2], -0.332, places=6)
        self.assertAlmostEqual(at(p, "b", motion.LOC, 19.0)[0], 1.0, places=6)   # x unchanged

    def test_moves_compose_in_time_order(self):
        p = run([{"do": "MOVE", "components": ["a"], "start_seconds": 1.0, "seconds": 1.0, "offset": [0.0, 0.0, -0.332]},
                 {"do": "MOVE", "components": ["a"], "start_seconds": 3.0, "seconds": 1.0, "offset": [0.0, 0.0, 0.436]}])
        self.assertAlmostEqual(at(p, "a", motion.LOC, 2.5)[2], -0.332, places=6)
        self.assertAlmostEqual(at(p, "a", motion.LOC, 5.0)[2], 0.104, places=6)

    def test_reveal_then_move_on_the_same_part(self):
        p = run([{"do": "REVEAL", "components": ["a"], "start_seconds": 1.0, "seconds": 1.0, "direction": "FROM_BELOW", "distance": 2.0},
                 {"do": "MOVE", "components": ["a", "b"], "start_seconds": 3.0, "seconds": 1.0, "offset": [0.0, 0.0, 0.5]}])
        self.assertAlmostEqual(at(p, "a", motion.LOC, 2.5)[2], 0.0, places=6)       # landed at rest
        self.assertAlmostEqual(at(p, "a", motion.LOC, 5.0)[2], 0.5, places=6)       # then moved with the group
        self.assertLess(at(p, "a", motion.LOC, 0.5)[2], -1.9)                       # came from below

    def test_overlapping_motions_on_one_part_are_refused(self):
        with self.assertRaises(motion.PlanError):
            run([{"do": "MOVE", "components": ["a"], "start_seconds": 1.0, "seconds": 2.0, "offset": [0, 0, 1]},
                 {"do": "MOVE", "components": ["a"], "start_seconds": 2.0, "seconds": 1.0, "offset": [0, 0, 1]}])

    def test_rotate_turns_location_and_rotation_about_the_pivot(self):
        p = run([{"do": "ROTATE", "components": ["b"], "start_seconds": 1.0, "seconds": 1.0, "axis": "Y", "degrees": 10.0,
                  "pivot": [0.0, 0.0, 0.0]}])
        loc, rot = at(p, "b", motion.LOC, 3.0), at(p, "b", motion.ROT, 3.0)
        self.assertAlmostEqual(rot[1], math.radians(10.0), places=6)
        self.assertAlmostEqual(loc[0], math.cos(math.radians(10.0)), places=6)
        self.assertAlmostEqual(loc[2], -math.sin(math.radians(10.0)), places=6)

    def test_oscillate_returns_to_rest(self):
        p = run([{"do": "OSCILLATE", "components": ["a"], "start_seconds": 1.0, "seconds": 6.0, "amplitude_m": 0.3,
                  "period_seconds": 2.0, "axis": "X", "pivot": [0.0, 0.0, 0.0], "tilt_degrees": 1.0}])
        self.assertAlmostEqual(at(p, "a", motion.LOC, 0.5)[2], 0.0, places=6)
        self.assertAlmostEqual(at(p, "a", motion.LOC, 7.5)[2], 0.0, places=6)
        peak = max(abs(p.sample("a", motion.LOC, f)[2]) for f in range(p.frame(1.0), p.frame(7.0)))
        self.assertGreater(peak, 0.2)
        self.assertLessEqual(peak, 0.3 + 1e-6)

    def test_missing_offset_or_pivot_is_refused(self):
        for step in ({"do": "MOVE", "components": ["a"], "start_seconds": 1.0},
                     {"do": "ROTATE", "components": ["a"], "start_seconds": 1.0, "degrees": 5.0},
                     {"do": "ROTATE", "components": ["a"], "start_seconds": 1.0, "degrees": 60.0, "pivot": [0, 0, 0]}):
            with self.assertRaises(motion.PlanError):
                run([step])

    def test_the_concept_motion_label_is_the_briefs_wording(self):
        self.assertEqual(motion.CONCEPT_MOTION_LABEL, "Conceptual motion visualization — not a hydrodynamic simulation")


if __name__ == "__main__":
    unittest.main()
