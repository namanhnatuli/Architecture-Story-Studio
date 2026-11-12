"""Offline tests for the pure-Python template planners (engine/motion.py, engine/templates.py)."""
import json
import math
import unittest

from engine import motion, spec, templates
from tools.cli import ROOT

LEGACY = ROOT / "tests" / "fixtures" / "legacy_projects"   # archived pilots kept as regression fixtures (M7)

PROJECT = LEGACY / "roof-evolution"


def load(name):
    return json.loads((PROJECT / "storyboard" / name).read_text())


def comp(name, loc, layer=0, hint=None, rot=(0.0, 0.0, 0.0)):
    return motion.Component(name=name, id=name, location=loc, rotation=rot, center=loc, layer=layer, hint=hint)


def close(a, b, tol=1e-9):
    return all(abs(x - y) <= tol for x, y in zip(a, b))


class EasingTest(unittest.TestCase):
    def test_endpoints_and_monotonic(self):
        for name in ("LINEAR", "SMOOTH", "EASE_IN", "EASE_OUT", "EASE_IN_OUT"):
            self.assertAlmostEqual(motion.ease(name, 0.0), 0.0)
            self.assertAlmostEqual(motion.ease(name, 1.0), 1.0)
            values = [motion.ease(name, i / 50) for i in range(51)]
            self.assertEqual(values, sorted(values), name)

    def test_matches_blender_closed_forms(self):
        # Same formulas as Blender's BLI_easing (verified against fcurve.evaluate in Blender 5.2).
        self.assertAlmostEqual(motion.ease("SMOOTH", 0.25), -(math.cos(math.pi * .25) - 1) / 2)
        self.assertAlmostEqual(motion.ease("EASE_IN_OUT", 0.5), 0.5)
        self.assertAlmostEqual(motion.ease("EASE_OUT", 0.5), 0.875)

    def test_unknown_easing_is_an_error(self):
        with self.assertRaises(motion.PlanError):
            motion.ease("BOUNCY", 0.5)

    def test_frame_rounding_is_half_up(self):
        self.assertEqual(motion.frame_at(0.0, 24), 1)
        self.assertEqual(motion.frame_at(0.5 / 24, 24), 2)
        self.assertEqual(motion.frame_at(2.5 / 24, 24), 4)


class KeyToleranceTest(unittest.TestCase):
    """Plan.key_tolerance: F32_KEY_ULPS float32 ulps of the scale Blender interpolates (max(|a|, |b|, |b - a|) of the
    bracketing keys), never less than the fixed base; measured independently by tools/f32_key_error.py."""

    @staticmethod
    def plan(a, b, easing="SMOOTH", frames=(1, 25)):
        p = motion.Plan(fps=24, frame_count=40)
        p.key("cam", motion.ORTHO, frames[0], a, easing)
        p.key("cam", motion.ORTHO, frames[1], b, easing)
        return p

    def test_ulp_is_the_float32_spacing(self):
        import struct

        def next_up(x):
            return struct.unpack("f", struct.pack("I", struct.unpack("I", struct.pack("f", x))[0] + 1))[0]
        for x in (0.75, 1.0, 3.0, 150.0, 933.27099609375, 1500.0):
            self.assertEqual(motion.f32_ulp(x), next_up(x) - x, x)

    def test_small_values_keep_the_base_tolerance(self):
        self.assertEqual(self.plan(0.5, 150.0).key_tolerance("cam", motion.ORTHO, 10, 1e-4), 1e-4)

    def test_large_values_allow_four_float32_ulps_of_the_segment_and_no_more(self):
        # SC_038 (full review, 2026-11-11): plan 933.2710799037022, Blender 933.271240234375 (2.6 ulps of 6.1e-5)
        want, got = 933.2710799037022, 933.271240234375
        p = self.plan(want, want * 1.0004)
        tol = p.key_tolerance("cam", motion.ORTHO, 10, 1e-4)
        ulp = 2.0 ** -14   # float32 spacing in [512, 1024)
        self.assertEqual(tol, motion.F32_KEY_ULPS * ulp)
        self.assertGreater(abs(got - want), 1e-4)
        self.assertLessEqual(abs(got - want), tol)
        self.assertGreater(5 * ulp, tol)   # an error of 5 ulps is a mismatch

    def test_a_move_across_zero_uses_the_change_and_a_hold_its_key(self):
        p = self.plan(-891.0, 874.0, frames=(5, 25))   # the change, 1765, is in [1024, 2048): ulp 2**-13
        self.assertEqual(p.key_tolerance("cam", motion.ORTHO, 10, 1e-4), 4 * 2.0 ** -13)
        self.assertEqual(p.key_tolerance("cam", motion.ORTHO, 30, 1e-4), 4 * 2.0 ** -14)   # after the last key: 874
        self.assertEqual(p.key_tolerance("cam", motion.ORTHO, 2, 1e-4), 4 * 2.0 ** -14)    # before the first key: 891


class DirectionTest(unittest.TestCase):
    def test_named_vector_and_computed(self):
        c = comp("a", (2.0, 0.0, 3.0), hint=(0, 0, 2))
        self.assertEqual(motion.resolve_direction("UP", c, (0, 0, 0)), (0.0, 0.0, 1.0))
        self.assertTrue(close(motion.resolve_direction([3, 0, 4], c, (0, 0, 0)), (0.6, 0.0, 0.8)))
        self.assertTrue(close(motion.resolve_direction("OUTWARD", c, (0, 0, 0)), (1.0, 0.0, 0.0)))
        s = 1 / math.sqrt(2)
        self.assertTrue(close(motion.resolve_direction("OUTWARD_UP", c, (0, 0, 0)), (s, 0.0, s)))
        self.assertTrue(close(motion.resolve_direction("HINT", c, (0, 0, 0)), (0.0, 0.0, 1.0)))

    def test_centered_component_falls_back_to_up(self):
        c = comp("ridge", (0.0, 0.0, 4.0))
        self.assertEqual(motion.resolve_direction("OUTWARD", c, (0.0, 0.0, 1.0)), (0.0, 0.0, 1.0))

    def test_zero_vector_and_unknown_name_are_errors(self):
        c = comp("a", (1.0, 0.0, 0.0))
        for bad in ([0, 0, 0], "SIDEWAYS", [1, 2]):
            with self.assertRaises(motion.PlanError):
                motion.resolve_direction(bad, c, (0, 0, 0))


class ReplacePartsTest(unittest.TestCase):
    def setUp(self):
        self.out = [comp("a_cover", (-1.0, 0, 3.0), layer=3), comp("a_rafter", (-1.0, 0, 2.8), layer=1)]
        self.inc = [comp("b_cover", (-1.0, 0, 4.0), layer=3), comp("b_rafter", (-1.0, 0, 3.6), layer=1)]
        self.cfg = {"hold_start_seconds": 0.5, "hold_end_seconds": 1.0,
                    "outgoing": {"direction": "UP", "distance": 3.0, "lift": 0.5, "stagger_seconds": 0.25},
                    "incoming": {"direction": "FROM_ABOVE", "distance": 2.0, "stagger_seconds": 0.25}}

    @staticmethod
    def cfg_default():
        return {"hold_start_seconds": 0.5, "hold_end_seconds": 1.0,
                "outgoing": {"direction": "UP", "distance": 3.0, "lift": 0.5, "stagger_seconds": 0.25},
                "incoming": {"direction": "FROM_ABOVE", "distance": 2.0, "stagger_seconds": 0.25}}

    def plan(self, cfg=None):
        p = motion.Plan(24, 144)
        return motion.plan_replace_parts(p, self.out, self.inc, cfg or self.cfg)

    def test_start_and_end_transforms(self):
        p = self.plan()
        for c in self.out:
            self.assertEqual(p.sample(c.name, motion.LOC, 1), c.location)
            self.assertEqual(p.sample(c.name, motion.HIDE, 1), (0.0,))
            self.assertEqual(p.sample(c.name, motion.HIDE, 144), (1.0,))
            self.assertEqual(p.sample(c.name, motion.TRANSPARENCY, 144), (1.0,))
        for c in self.inc:
            self.assertTrue(close(p.sample(c.name, motion.LOC, 1), (c.location[0], 0, c.location[2] + 2.0)))
            self.assertEqual(p.sample(c.name, motion.LOC, 144), c.location)  # exact landing
            self.assertEqual(p.sample(c.name, motion.HIDE, 1), (1.0,))
            self.assertEqual(p.sample(c.name, motion.TRANSPARENCY, 144), (0.0,))

    def test_order_and_stagger(self):
        p = self.plan()
        # DISASSEMBLY: covering (layer 3) leaves before rafters; ASSEMBLY: rafters land first.
        start = {n: next(k.frame for k in p.keys(n, motion.LOC)[1:]) for n in p.tracks}
        self.assertEqual(start["a_rafter"] - start["a_cover"], 6)  # 0.25 s at 24 fps
        land = {n: p.keys(n, motion.LOC)[-2].frame for n in ("b_cover", "b_rafter")}
        self.assertLess(land["b_rafter"], land["b_cover"])

    def test_only_listed_parts_are_keyed_and_scale_never(self):
        p = self.plan()
        self.assertEqual(set(p.tracks), {"a_cover", "a_rafter", "b_cover", "b_rafter"})
        for name in p.tracks:
            self.assertNotIn("scale", p.channels(name))

    def test_keys_inside_shot(self):
        p = self.plan()
        for name in p.tracks:
            for ch in p.channels(name):
                for k in p.keys(name, ch):
                    self.assertTrue(1 <= k.frame <= 144)

    def test_rotation_and_per_component_override(self):
        cfg = json.loads(json.dumps(self.cfg))
        cfg["incoming"]["rotation_degrees"] = [0, 0, 90]
        cfg["incoming"]["per_component"] = {"b_cover": {"distance": 1.0}}
        p = self.plan(cfg)
        self.assertTrue(close(p.sample("b_cover", motion.ROT, 1), (0, 0, math.pi / 2)))
        self.assertEqual(p.sample("b_cover", motion.ROT, 144), (0.0, 0.0, 0.0))
        self.assertTrue(close(p.sample("b_cover", motion.LOC, 1), (-1.0, 0, 5.0)))

    def test_timing_overflow_and_typos_are_errors(self):
        cfg = json.loads(json.dumps(self.cfg))
        cfg["incoming"]["move_seconds"] = 5.0
        with self.assertRaisesRegex(motion.PlanError, "needs .* frames"):
            self.plan(cfg)
        cfg = json.loads(json.dumps(self.cfg))
        cfg["outgoing"]["distnce"] = 2
        with self.assertRaisesRegex(motion.PlanError, "unknown option 'distnce'"):
            self.plan(cfg)

    def test_deterministic(self):
        a, b = self.plan(), self.plan()
        self.assertEqual(a.tracks, b.tracks)


class ExplodedViewTest(unittest.TestCase):
    def setUp(self):
        self.parts = [comp("cover", (0, 0, 3.0), layer=3, hint=(0, 0, 1)),
                      comp("beam", (0, 0, 2.8), layer=2, hint=(0, 0, 1)),
                      comp("rafters", (-1, 0, 2.6), layer=1, hint=(-1, 0, 0))]
        self.cfg = {"distance": 1.0, "per_component": {"cover": {"distance": 2.0}},
                    "highlight": {"components": ["beam"], "mode": "SIMULTANEOUS"}}

    def test_explodes_by_distance_and_returns_exactly(self):
        p = motion.plan_exploded_view(motion.Plan(24, 120), self.parts, self.cfg)
        hold = p.markers["exploded_hold"]
        self.assertTrue(close(p.sample("cover", motion.LOC, hold), (0, 0, 5.0)))
        self.assertTrue(close(p.sample("rafters", motion.LOC, hold), (-2.0, 0, 2.6)))
        for c in self.parts:
            self.assertEqual(p.sample(c.name, motion.LOC, 120), c.location)

    def test_return_order_reverses_explode_order(self):
        p = motion.plan_exploded_view(motion.Plan(24, 120), self.parts, self.cfg)
        out_start = {n: p.keys(n, motion.LOC)[1].frame for n in p.tracks}
        back_start = {n: p.keys(n, motion.LOC)[3].frame for n in p.tracks}
        self.assertLess(out_start["cover"], out_start["rafters"])
        self.assertLess(back_start["rafters"], back_start["cover"])

    def test_highlight_inside_hold_window(self):
        p = motion.plan_exploded_view(motion.Plan(24, 120), self.parts, self.cfg)
        keys = p.keys("beam", motion.HIGHLIGHT)
        lit = [k.frame for k in keys if k.value[0] > 0]
        self.assertTrue(all(p.markers["explode_end"] <= f <= p.markers["return_start"] for f in lit))
        self.assertEqual(p.sample("beam", motion.HIGHLIGHT, 120), (0.0,))

    def test_simultaneous_has_no_stagger(self):
        cfg = dict(self.cfg, sequence="SIMULTANEOUS")
        p = motion.plan_exploded_view(motion.Plan(24, 120), self.parts, cfg)
        self.assertEqual(len({p.keys(n, motion.LOC)[1].frame for n in p.tracks}), 1)


class PilotPlansTest(unittest.TestCase):
    """The real pilot storyboard plans offline with placeholder geometry."""

    def test_every_shot_plans_and_markers_exist(self):
        states, story = load("states.json"), load("storyboard.json")
        for shot in story["shots"]:
            plan = templates.plan_shot(shot, states, 24, templates.placeholder_slots(shot, states))
            self.assertEqual(plan.frame_count, round(shot["duration_seconds"] * 24))
            shared = set(spec.shared_ids(states))
            intro = (shot.get("animation") or {}).get("intro")
            for name in plan.tracks:
                if name.split(".")[-1] not in shared:
                    continue
                # Shared parts never move; the only exception is a SIDE_BY_SIDE intro fading in
                # the *other* models (transparency only, never on the intro state's own slot).
                self.assertFalse({motion.LOC, motion.ROT} & set(plan.channels(name)), f"{shot['id']} {name}")
                self.assertTrue(intro and not name.startswith(intro["from_state"] + "."), f"{shot['id']} {name}")
                self.assertEqual(plan.channels(name), [motion.TRANSPARENCY], f"{shot['id']} {name}")
        total = sum(s["duration_seconds"] for s in story["shots"])
        self.assertAlmostEqual(total, 20.0)


if __name__ == "__main__":
    unittest.main()


class FadeTwinsTest(unittest.TestCase):
    """M2.5: blended twins render only mid-fade; held frames keep the dithered originals."""

    def setUp(self):
        out = [comp("a_cover", (-1.0, 0, 3.0), layer=3), comp("a_rafter", (-1.0, 0, 2.8), layer=1)]
        inc = [comp("b_cover", (-1.0, 0, 4.0), layer=3), comp("b_rafter", (-1.0, 0, 3.6), layer=1)]
        self.plan = motion.plan_replace_parts(motion.Plan(24, 144), out, inc, ReplacePartsTest.cfg_default())
        self.twins = motion.split_fades(self.plan)

    def visible(self, name, f):
        hide = self.plan.sample(name, motion.HIDE, f)
        return hide is None or hide[0] < 0.5

    def test_every_fading_part_has_a_twin_with_identical_motion(self):
        self.assertEqual(set(self.twins), {"a_cover", "a_rafter", "b_cover", "b_rafter"})
        for name, twin in self.twins.items():
            for f in range(1, 145):
                self.assertEqual(self.plan.sample(name, motion.LOC, f), self.plan.sample(twin, motion.LOC, f))

    def test_windows_are_exclusive_and_cover_partial_transparency(self):
        for name, twin in self.twins.items():
            for f in range(1, 145):
                t = self.plan.sample(name, motion.TRANSPARENCY, f)[0]
                self.assertFalse(self.visible(name, f) and self.visible(twin, f), f"{name}@{f}")
                self.assertEqual(self.visible(twin, f), 1e-6 < t < 1 - 1e-6, f"{twin}@{f}")
            self.assertFalse(self.visible(twin, 1))
            self.assertFalse(self.visible(twin, 144))

    def test_end_states_unchanged(self):
        for name in ("b_cover", "b_rafter"):
            self.assertTrue(self.visible(name, 144))
        for name in ("a_cover", "a_rafter"):
            self.assertTrue(self.visible(name, 1))
            self.assertFalse(self.visible(name, 144))


class IntroTest(unittest.TestCase):
    camera = {"name": "cam", "start": {"location": (1.0, 2.0, 3.0), "ortho_scale": 14.0},
              "end": {"location": (0.0, 0.0, 3.0), "ortho_scale": 17.0}}

    def test_camera_moves_from_start_to_end_and_models_fade_in(self):
        p = motion.Plan(24, 108)
        end = motion.plan_intro(p, {"from_state": "B", "seconds": 1.5}, self.camera, ["a_wall"])
        self.assertEqual(end, 37)
        self.assertEqual(p.sample("cam", motion.LOC, 1), (1.0, 2.0, 3.0))
        self.assertEqual(p.sample("cam", motion.ORTHO, 1), (14.0,))
        self.assertEqual(p.sample("cam", motion.ORTHO, end), (17.0,))
        self.assertEqual(p.sample("cam", motion.LOC, 108), (0.0, 0.0, 3.0))
        self.assertEqual(p.sample("a_wall", motion.TRANSPARENCY, 1), (1.0,))
        self.assertEqual(p.sample("a_wall", motion.TRANSPARENCY, end), (0.0,))

    def test_bad_intro_configs(self):
        with self.assertRaisesRegex(motion.PlanError, "fade_end"):
            motion.plan_intro(motion.Plan(24, 108), {"fade_start": 0.8, "fade_end": 0.5}, self.camera, [])
        with self.assertRaisesRegex(motion.PlanError, "before the shot does"):
            motion.plan_intro(motion.Plan(24, 30), {"seconds": 2.0}, self.camera, [])
