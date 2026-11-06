"""SEQUENCE shots (engine/motion.plan_sequence, planner SEQUENCE strategy), the web in courses, synthesised sound
cues (pipeline/sound.py) and review excerpts (tools/excerpt.py). Offline, no Blender."""
import json
import unittest
from pathlib import Path

from engine import motion, templates
from engine.arch import assets, semantic
from pipeline import chapters, sound
from planner import consistency, mapper, vocabulary as V
from tools import excerpt

ROOT = Path(__file__).resolve().parent.parent
GOTHIC = ROOT / "asset_library/architecture/cathedrals/cathedral_gothic_section_01.json"
PROJECT = ROOT / "projects/gothic-cathedral-heights"
CAM = {"name": templates.CAMERA_NAME, "views": [{"location": (0.0, 0.0, 0.0), "ortho_scale": 40.0},
                                                {"location": (5.0, 0.0, 2.0), "ortho_scale": 20.0}]}


def parts(*ids):
    return {i: motion.Component(name=i, id=i, center=(0.0, 0.0, float(k))) for k, i in enumerate(ids)}


def run(steps, views=None, frames=480, comps=None):
    plan = motion.Plan(24, frames)
    cfg = {"template": "SEQUENCE", "state": "s", "steps": steps, **({"views": views} if views else {})}
    return motion.plan_sequence(plan, comps or parts("a", "b", "c", "d"), cfg, CAM if views else {"name": templates.CAMERA_NAME})


class PlanSequenceTest(unittest.TestCase):
    def test_the_camera_holds_each_view_then_eases_to_the_next(self):
        plan = run([], views=[{}, {"start_seconds": 3.0, "move_seconds": 2.0, "focus": ["a"]}])
        cam = templates.CAMERA_NAME
        self.assertEqual(plan.sample(cam, motion.ORTHO, 1)[0], 40.0)
        self.assertEqual(plan.sample(cam, motion.ORTHO, plan.frame(3.0))[0], 40.0)
        settled = plan.markers["view_1_settled"]
        self.assertEqual(settled, plan.frame(5.0))
        self.assertEqual(plan.sample(cam, motion.ORTHO, settled)[0], 20.0)
        self.assertEqual(plan.sample(cam, motion.LOC, plan.frame_count), (5.0, 0.0, 2.0))
        self.assertLess(plan.sample(cam, motion.ORTHO, plan.frame(4.0))[0], 40.0)

    def test_a_part_that_arrives_is_unseen_until_it_does_and_lands_exactly(self):
        plan = run([{"do": "REVEAL", "components": ["a"], "start_seconds": 2.0, "seconds": 1.0, "distance": 3.0}])
        f0 = plan.frame(2.0)
        self.assertEqual(plan.sample("a", motion.HIDE, f0 - 1)[0], 1.0)
        self.assertEqual(plan.sample("a", motion.LOC, f0 - 1), (0.0, 0.0, 3.0))
        landed = plan.markers["reveal_0_landed"]
        self.assertEqual(plan.sample("a", motion.LOC, landed), (0.0, 0.0, 0.0))
        self.assertEqual(plan.sample("a", motion.TRANSPARENCY, landed)[0], 0.0)
        self.assertEqual(plan.sample("a", motion.HIDE, landed)[0], 0.0)

    def test_a_part_seen_first_stays_at_rest_until_it_has_faded_out(self):
        """The establishing view shows the ribs; they leave, then arrive: they never jump while seen."""
        plan = run([{"do": "FADE_OUT", "components": ["a"], "start_seconds": 1.0, "seconds": 1.0},
                    {"do": "REVEAL", "components": ["a"], "start_seconds": 4.0, "seconds": 1.0, "distance": 3.0}])
        for f in range(1, plan.frame(4.0)):
            if plan.sample("a", motion.HIDE, f)[0] < 0.5:
                self.assertEqual(plan.sample("a", motion.LOC, f), (0.0, 0.0, 0.0), f)
        self.assertEqual(plan.sample("a", motion.LOC, plan.frame(4.0)), (0.0, 0.0, 3.0))

    def test_ghosts_and_glows_follow_their_steps(self):
        plan = run([{"do": "GHOST", "components": ["b"], "start_seconds": 0, "seconds": 0, "transparency": 0.8},
                    {"do": "UNGHOST", "components": ["b"], "start_seconds": 5.0, "seconds": 1.0},
                    {"do": "HIGHLIGHT", "components": ["c"], "start_seconds": 1.0, "hold_seconds": 1.0},
                    {"do": "HIGHLIGHT", "components": ["c"], "start_seconds": 4.0, "hold_seconds": 1.0}])
        self.assertAlmostEqual(plan.sample("b", motion.TRANSPARENCY, 1)[0], 0.8)
        self.assertEqual(plan.sample("b", motion.TRANSPARENCY, plan.frame(6.0))[0], 0.0)
        self.assertGreater(plan.sample("c", motion.HIGHLIGHT, plan.markers["highlight_2_peak"])[0], 0.5)
        self.assertGreater(plan.sample("c", motion.HIGHLIGHT, plan.markers["highlight_3_peak"])[0], 0.5)
        self.assertEqual(plan.sample("c", motion.HIGHLIGHT, plan.frame(3.2))[0], 0.0)

    def test_impossible_sequences_are_refused(self):
        bad = [
            [{"do": "HIGHLIGHT", "components": ["a"], "start_seconds": 1.0, "hold_seconds": 3.0},
             {"do": "HIGHLIGHT", "components": ["a"], "start_seconds": 2.0}],                    # glow over a glow
            [{"do": "REVEAL", "components": ["a"], "start_seconds": 1.0},
             {"do": "REVEAL", "components": ["a"], "start_seconds": 4.0}],                       # arrives twice
            [{"do": "GHOST", "components": ["a"], "start_seconds": 2.0, "seconds": 0}],           # instant mid-shot
            [{"do": "GHOST", "components": ["zz"], "start_seconds": 1.0}],                       # not a part
            [{"do": "UNGHOST", "components": ["a"], "start_seconds": 1.0, "seconds": 2.0},
             {"do": "FADE_OUT", "components": ["a"], "start_seconds": 2.0}],                     # overlapping fades
            [{"do": "SPIN", "components": ["a"], "start_seconds": 1.0}],
        ]
        for steps in bad:
            with self.assertRaises(motion.PlanError, msg=steps):
                run(steps)
        with self.assertRaises(motion.PlanError):   # a camera move must take time
            run([], views=[{}, {"start_seconds": 3.0, "move_seconds": 0.0}])
        with self.assertRaises(motion.PlanError):   # and end before the shot does
            run([], views=[{}, {"start_seconds": 18.0, "move_seconds": 3.0}])

    def test_too_short_is_a_timing_error_the_planner_can_lengthen(self):
        with self.assertRaises(motion.PlanError) as e:
            run([{"do": "HIGHLIGHT", "components": ["a"], "start_seconds": 25.0}])
        self.assertIn("timing needs", str(e.exception))


class CoursesAndRibsTest(unittest.TestCase):
    def test_two_diagonal_ribs_per_bay_each_spanning_corner_to_corner(self):
        comps = {c.id: c for c in assets.plan_file(GOTHIC)}
        for bay in (1, 2, 3):
            for rib in "ab":
                lo, hi = semantic.bbox(comps[f"rib_diagonal_b{bay}{rib}"])
                self.assertGreater(hi[0] - lo[0], 13.0)     # across the nave, corner to corner
        self.assertNotIn("rib_diagonal_b1", comps)

    def test_each_course_is_an_arch_springing_from_the_diagonals(self):
        """Courses of panel f lie between y = 0 and the transverse arch and get longer towards it."""
        comps = {c.id: c for c in assets.plan_file(GOTHIC)}
        spans = [semantic.bbox(comps[f"vault_web_b1_f{k}"]) for k in range(1, 6)]
        widths = [hi[0] - lo[0] for lo, hi in spans]
        self.assertEqual(widths, sorted(widths))            # inner courses are shorter
        self.assertGreater(widths[-1], 13.0)                # the outer one is a full arch
        for lo, hi in spans:
            self.assertGreaterEqual(lo[1], -0.01)
            self.assertLessEqual(hi[1], 3.76)

    def test_a_ref_can_name_exact_parts(self):
        vocab = V.Vocabulary()
        parts = [{"id": "s_rib_diagonal_b1a", "role": "rib", "group": "rib_diagonal_1"},
                 {"id": "s_rib_diagonal_b1b", "role": "rib", "group": "rib_diagonal_1"}]
        out = mapper.resolve_targets([{"concept": "rib", "local": "rib_diagonal_b1b"}], parts, vocab, "s")
        self.assertEqual(out[0]["component_ids"], ["s_rib_diagonal_b1b"])
        with self.assertRaises(mapper.MappingError):
            mapper.resolve_targets([{"concept": "rib", "local": ["rib_diagonal_b9a"]}], parts, vocab, "s")


class PilotPlanTest(unittest.TestCase):
    def setUp(self):
        self.plan = json.loads((PROJECT / "storyboard/visual_plan.json").read_text())
        self.shots = {s["beat_id"]: s for s in self.plan["shots"]}

    def test_the_pilot_beats_are_sequences_timed_to_their_words(self):
        for bid in ("B12", "B13", "B16", "B17"):
            self.assertEqual(self.shots[bid]["template"], "SEQUENCE", bid)
        steps = self.shots["B12"]["shot"]["animation"]["steps"]
        reveals = [s for s in steps if s["do"] == "REVEAL"]
        ribs = [s for s in reveals if any("rib_diagonal" in c for c in s["components"])]
        self.assertEqual(len(ribs), 2)                       # "two ribs": one after the other
        self.assertLess(ribs[0]["start_seconds"], ribs[1]["start_seconds"])
        web = next(s for s in reveals if any("vault_web" in c for c in s["components"]))
        self.assertGreater(web["start_seconds"], ribs[1]["start_seconds"])   # piers, then ribs, then the web

    def test_every_stone_that_lands_with_a_sound_has_one_cue(self):
        shot = self.shots["B12"]["shot"]
        cues = shot["sound_cues"]
        self.assertEqual(len(cues), 2)
        for cue, step in zip(cues, [s for s in shot["animation"]["steps"] if s.get("sound")]):
            self.assertAlmostEqual(cue["at_seconds"], step["start_seconds"] + step["seconds"], places=3)
        self.assertEqual([c["kind"] for c in self.shots["B17"]["shot"]["sound_cues"]], ["STONE_HEAVY"])

    def test_the_flying_buttress_returns_when_it_is_named(self):
        steps = self.shots["B17"]["shot"]["animation"]["steps"]
        back = next(s for s in steps if s["do"] == "UNGHOST")
        self.assertTrue(all("flying_buttress_east0" in c for c in back["components"]))
        pinnacle = next(s for s in steps if s["do"] == "REVEAL")
        self.assertEqual([c.split("section_")[1] for c in pinnacle["components"]], ["pinnacle_east0"])

    def test_glows_of_a_sequence_count_for_the_narration_check(self):
        ps = self.shots["B13"]
        glows = [s for s in ps["shot"]["animation"]["steps"] if s["do"] == "HIGHLIGHT"]
        t = glows[0]["start_seconds"] + 0.5
        self.assertTrue(consistency._glowing(ps, t, t + 0.1))
        self.assertFalse(consistency._glowing(ps, 0.0, 0.2))

    def test_long_form_qa_sees_the_motion_of_a_sequence(self):
        shot = self.shots["B12"]["shot"]
        moving = chapters.motion_intervals(shot)
        self.assertTrue(any(a <= 3.0 <= b for a, b in moving))     # the camera move to the bay
        self.assertGreater(len(moving), 6)


class SoundTest(unittest.TestCase):
    def test_sounds_are_deterministic_short_and_peak_normalised(self):
        a, b = sound.synth("STONE", 24000, 0), sound.synth("STONE", 24000, 0)
        self.assertEqual(a, b)
        self.assertNotEqual(a, sound.synth("STONE", 24000, 1))
        self.assertAlmostEqual(max(abs(v) for v in a), 1.0, places=6)
        self.assertLess(len(sound.synth("STONE_HEAVY", 24000, 0)) / 24000, 1.0)
        self.assertAlmostEqual(a[0], 0.0, places=6)          # soft attack and release: no click
        self.assertLess(abs(a[-1]), 1e-3)

    def test_cues_sit_under_the_narration_at_their_time(self):
        sr = 24000
        narration = [0.0] * (2 * sr)
        narration[100] = 10000.0
        mixed, rep = sound.mix_under(narration, [{"at_seconds": 1.0, "kind": "STONE"}], sr)
        d = sound.load_design()
        start = int(round((1.0 - d["lead_seconds"]) * sr))
        self.assertTrue(all(v == 0.0 for v in mixed[200:start]))
        peak = max(abs(v) for v in mixed[start:])
        self.assertAlmostEqual(peak, 10000.0 * 10 ** (-d["under_narration_db"] / 20), delta=1.0)
        self.assertEqual(rep["clipped_samples"], 0)


class ExcerptTest(unittest.TestCase):
    def test_runs_and_joins_of_non_adjacent_shots(self):
        film = [f"SC_{i:03d}" for i in range(1, 20)]
        self.assertEqual(excerpt.excerpt_runs(film, ["SC_012", "SC_013", "SC_016", "SC_017"]),
                         [["SC_012", "SC_013"], ["SC_016", "SC_017"]])

    def test_each_shot_keeps_its_own_stretch_of_narration(self):
        timing = {"fps": 24, "shots": [{"id": "A", "start_frame": 0, "frames": 2}, {"id": "B", "start_frame": 2, "frames": 3},
                                       {"id": "C", "start_frame": 5, "frames": 1}]}
        samples = list(range(6 * 1000))
        out, offsets = excerpt.narration_slices(samples, timing, ["A", "C"], 24000)
        self.assertEqual(out, list(range(0, 2000)) + list(range(5000, 6000)))
        self.assertEqual(offsets, {"A": 0.0, "C": 2 / 24})
        cues = excerpt.excerpt_cues([{"id": "C", "sound_cues": [{"at_seconds": 0.01, "kind": "STONE"}]}], ["A", "C"], offsets)
        self.assertAlmostEqual(cues[0]["at_seconds"], 2 / 24 + 0.01, places=3)


if __name__ == "__main__":
    unittest.main()
