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

    def test_an_orbit_turns_around_the_subject_and_lands_on_each_view(self):
        """g-r5: a view with its own direction: the camera turns on a short arc, held exactly on each fit."""
        from engine import framing
        pts = [(x, y, z) for x in (-5.0, 5.0) for y in (0.0, 20.0) for z in (0.0, 30.0)]
        preset = {"azimuth_degrees": -60.0, "elevation_degrees": 20.0, "margin": 0.06}
        views = motion.sequence_views({"views": [{}, {"start_seconds": 2.0, "move_seconds": 3.0, "azimuth": -30.0}]})
        fits = framing.view_fits(views, lambda focus: pts, preset, 16 / 9)
        plan = motion.Plan(24, 240)
        cam = {"name": templates.CAMERA_NAME, "views": fits}
        motion.plan_sequence(plan, parts("a"), {"template": "SEQUENCE", "state": "s", "views": views, "steps": []}, cam)
        name, settled = templates.CAMERA_NAME, plan.markers["view_1_settled"]
        for f, fit in ((1, fits[0]), (plan.frame(2.0), fits[0]), (settled, fits[1]), (plan.frame_count, fits[1])):
            for got, want in zip(plan.sample(name, motion.LOC, f), fit["location"]):
                self.assertAlmostEqual(got, want, places=6)
            for got, want in zip(framing.basis_from_euler(plan.sample(name, motion.ROT, f))[2],
                                 framing.camera_basis(fit["azimuth"], fit["elevation"])[2]):
                self.assertAlmostEqual(got, want, places=6)
        mid = plan.frame(3.5)   # half way: the camera looks from between the two directions, at the subject
        fwd = framing.basis_from_euler(plan.sample(name, motion.ROT, mid))[2]
        az = framing.math.degrees(framing.math.atan2(-fwd[1], -fwd[0]))
        self.assertTrue(-60.0 < az < -30.0, az)
        loc = plan.sample(name, motion.LOC, mid)
        centre = (0.0, 10.0, 15.0)
        off = [c - l for c, l in zip(centre, loc)]
        along = sum(o * f for o, f in zip(off, fwd))
        across = max(abs(o - along * f) for o, f in zip(off, fwd))
        self.assertGreater(along, 20.0)      # in front of the camera, well clear of it
        self.assertLess(across, 6.0)         # roughly on the axis: the subject stays in frame
        with self.assertRaises(ValueError):  # under the ground plane only with a preset that hides it
            framing.view_fits(motion.sequence_views({"views": [{"elevation": -40.0}]}), lambda f: pts, preset, 16 / 9)

    def test_a_tinted_glow_keys_one_constant_tint(self):
        plan = run([{"do": "HIGHLIGHT", "components": ["c"], "start_seconds": 1.0, "hold_seconds": 1.0, "tint": 0.7},
                    {"do": "HIGHLIGHT", "components": ["d"], "start_seconds": 1.0, "hold_seconds": 1.0}])
        self.assertEqual(plan.sample("c", motion.TINT, 1)[0], 0.7)
        self.assertEqual(plan.sample("c", motion.TINT, plan.frame_count)[0], 0.7)
        self.assertNotIn(motion.TINT, plan.channels("d"))
        with self.assertRaises(motion.PlanError):
            run([{"do": "HIGHLIGHT", "components": ["c"], "start_seconds": 1.0, "hold_seconds": 1.0, "tint": 0.7},
                 {"do": "HIGHLIGHT", "components": ["c"], "start_seconds": 4.0, "hold_seconds": 1.0, "tint": 0.2}])

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

    def test_the_flying_buttress_returns_when_it_is_named_onto_a_solid_pier_buttress(self):
        """g-r5 (owner's pilot review): the support is solid before the flyer arrives, so the flyer never floats."""
        steps = self.shots["B17"]["shot"]["animation"]["steps"]
        back = {s["components"][0].split("section_")[1]: s for s in steps if s["do"] == "UNGHOST"}
        self.assertEqual(sorted(back), ["flying_buttress_east0", "pier_buttress_east0"])
        pier, flyer = back["pier_buttress_east0"], back["flying_buttress_east0"]
        self.assertLessEqual(pier["start_seconds"] + pier["seconds"], flyer["start_seconds"])
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
        v = shot["animation"]["views"][1]                          # the camera move (an orbit) under the bay
        self.assertTrue(any(a <= v["start_seconds"] + v["move_seconds"] / 2 <= b for a, b in moving))
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


class StageCardTest(unittest.TestCase):
    """g-r6 (owner's g-r5 review): pictures fill the frame and a 2D camera moves on them; the 2024 study greys a
    hypothesis, it does not cross it out; the chosen bay is marked before the church around it fades."""

    @classmethod
    def setUpClass(cls):
        shots = json.loads((PROJECT / "storyboard/storyboard.json").read_text())["shots"]
        cls.story = {b: s for s in shots for b in s.get("beat_ids", [])}   # by beat: shot ids follow the plan
        cls.beats = {b["beat_id"]: b for b in json.loads((PROJECT / "script/visual_beats.json").read_text())["beats"]}

    def test_stage_views_are_timed_and_in_order(self):
        for sid in ("B01", "B35", "B36"):
            views = self.story[sid]["graphic"]["stage"]["views"]
            self.assertEqual(views[0]["at"], 0.0)
            for a, b in zip(views[1:], views[2:]):
                self.assertGreaterEqual(b["at"], a["at"] + a["move_seconds"] - 1e-6)
            self.assertLess(views[-1]["at"] + views[-1]["move_seconds"], self.story[sid]["duration_seconds"])

    def test_pictures_on_the_stage_fill_the_frame_when_the_camera_climbs(self):
        g = self.story["B01"]["graphic"]
        self.assertTrue(any(e["kind"] == "image" and e.get("stage") for e in g["elements"]))
        texts = [e for e in g["elements"] if e["kind"] == "text"]
        self.assertFalse([e for e in texts if e.get("stage")])          # words stay put on screen
        self.assertTrue(any("today" in e["text"] for e in texts))       # the photograph is of the building today

    def test_the_2024_study_greys_the_foundation_hypothesis_without_crossing_it_out(self):
        els = self.beats["B35"]["graphic"]["elements"]
        texts = [e["text"] for e in els if e["kind"] == "text"]
        self.assertIn("Not supported by this study", texts)
        self.assertTrue(any("not a settled result" in t for t in texts))
        crossing = [e for e in els if e["kind"] == "line" and e.get("sentence") == 3 and e.get("color") == "#C25110"]
        self.assertEqual(crossing, [])   # no X over the arrows

    def test_the_bay_is_marked_before_the_church_around_it_fades(self):
        steps = self.story["B12"]["animation"]["steps"]
        first_glow = min(s["start_seconds"] for s in steps if s["do"] == "HIGHLIGHT")
        first_ghost = min(s["start_seconds"] for s in steps if s["do"] == "GHOST")
        isolate = max(s["start_seconds"] for s in steps if s["do"] == "FADE_OUT")
        move = self.story["B12"]["animation"]["views"][1]
        self.assertLess(first_glow, first_ghost)
        self.assertGreaterEqual(isolate + 1e-6, move["start_seconds"] + move["move_seconds"] - 0.5)   # after the turn

    def test_a_picture_card_never_opens_on_an_empty_frame(self):
        for sid in ("B01", "B31", "B33", "B35", "B37", "B38"):
            images = [e for e in self.story[sid]["graphic"]["elements"] if e["kind"] == "image"]
            self.assertEqual(images[0]["appear"], 0.0, sid)

    def test_a_picture_change_is_a_dissolve(self):
        """The next picture arrives over the last one, which leaves only once it is in (no dip to the background)."""
        els = self.story["B01"]["graphic"]["elements"]
        inside, outside = [e for e in els if e["kind"] == "image"][:2]
        self.assertLess(outside["appear"] + 0.35, inside["disappear"])
        self.assertGreater(outside.get("layer", 0), inside.get("layer", 0))

    def test_a_stage_needs_views_and_its_elements_need_a_stage(self):
        from tools import validator
        img = {"id": "x", "kind": "rect", "box": [0.1, 0.1, 0.2, 0.2], "stage": True, "appear": 0.0}
        self.assertTrue(any("without graphic.stage" in e for e in validator.validate_graphic({"elements": [img]}, 5.0)))
        bad = {"elements": [img], "stage": {"views": [{"rect": [0, 0, 1, 1], "at": 0.0},
                                                      {"rect": [0.2, 0.2, 0.4, 0.4], "at": 4.5, "move_seconds": 1.0}]}}
        self.assertTrue(any("after the shot" in e for e in validator.validate_graphic(bad, 5.0)))


class ChapterRedesignTest(unittest.TestCase):
    """g-r8 (owner's chapter list): pictures that do what the narration says. Shots are looked up by beat."""

    @classmethod
    def setUpClass(cls):
        shots = json.loads((PROJECT / "storyboard/storyboard.json").read_text())["shots"]
        cls.story = {b: s for s in shots for b in s.get("beat_ids", [])}

    def els(self, beat):
        return self.story[beat]["graphic"]["elements"]

    def test_the_wall_segments_turn_90_degrees_when_it_is_said(self):
        spins = [e["spin"] for e in self.els("B18") if e.get("spin")]
        self.assertEqual(len(spins), 6)
        self.assertTrue(all(abs(s["degrees"]) == 90 for s in spins))
        self.assertEqual(sorted(s["at"] for s in spins), [s["at"] for s in spins])   # one after another

    def test_the_hanging_chain_is_turned_upside_down(self):
        spins = {round(e["spin"]["degrees"]) for e in self.els("B09") if e.get("spin")}
        self.assertEqual(spins, {180})

    def test_stones_are_laid_from_both_springings_to_the_key_then_the_centering_goes(self):
        els = self.els("B27")
        stones = [e for e in els if e["kind"] == "polygon"]
        n = len(stones)
        key = stones[n // 2]
        self.assertGreater(key["appear"], max(stones[0]["appear"], stones[-1]["appear"]))
        centering = [e for e in els if e["kind"] == "line" and e.get("color") == "#8C654D" and e.get("disappear")]
        self.assertTrue(centering)
        self.assertGreater(min(e["disappear"] for e in centering), max(s["appear"] for s in stones))

    def test_no_card_opens_on_an_empty_frame(self):
        for bid, shot in self.story.items():
            g = shot.get("graphic")
            if g:
                self.assertTrue(any(e.get("appear", 1) == 0.0 for e in g["elements"]), bid)

    def test_the_vault_is_set_on_its_walls_before_it_pushes(self):
        steps = self.story["B05"]["animation"]["steps"]
        reveal = next(s for s in steps if s["do"] == "REVEAL")
        self.assertEqual(reveal["direction"], "FROM_ABOVE")
        thrust = next(a for a in self.story["B05"]["annotations"]["items"] if a["type"] == "THRUST_ARROW")
        self.assertGreater(thrust["appear"], reveal["start_seconds"] + reveal["seconds"])


class ReviewG8FixesTest(unittest.TestCase):
    """g-r9 (owner's g-r8 review): the photograph matches the period told, labels land on the part they name, B29 closes
    on one flyer and its buttress, and B09/B25 show their drawing from the first seconds."""

    @classmethod
    def setUpClass(cls):
        shots = json.loads((PROJECT / "storyboard/storyboard.json").read_text())["shots"]
        cls.story = {b: s for s in shots for b in s.get("beat_ids", [])}

    def els(self, beat):
        return self.story[beat]["graphic"]["elements"]

    def texts(self, beat):
        return {e["text"]: e for e in self.els(beat) if e["kind"] == "text"}

    def test_suger_is_shown_by_the_part_of_his_choir_that_survives(self):
        used = {e.get("asset") for s in self.story.values() for e in (s.get("graphic") or {}).get("elements", [])}
        self.assertNotIn("IMG_SAINT_DENIS_APSE", used)   # the upper choir, rebuilt from 1231
        images = [e for e in self.els("B21") if e["kind"] == "image"]
        self.assertEqual([e["asset"] for e in images], ["IMG_SAINT_DENIS_ROSE", "IMG_SAINT_DENIS_AMBULATORY"])
        caption = next(e for t, e in self.texts("B21").items() if t.startswith("The ambulatory of Suger's choir"))
        self.assertLessEqual(images[1]["appear"], caption["appear"])        # Suger's dates only over his ambulatory
        self.assertGreater(images[0]["disappear"], images[1]["appear"])     # a dissolve
        self.assertIn("Upper choir rebuilt in the 13th century", self.texts("B21"))
        self.assertEqual({e["asset"] for e in self.els("B22") if e["kind"] == "image"}, {"IMG_SAINT_DENIS_AMBULATORY"})
        for beat in ("B21", "B22"):
            self.assertIn("CLM_165", self.story[beat]["claim_ids"])

    def test_the_rib_label_names_a_rib_lit_along_its_length_for_a_moment(self):
        texts = self.texts("B21")
        self.assertIn("Vault rib", texts)
        self.assertNotIn("Every vault ribbed", texts)
        rib = [e for e in self.els("B21") if e["kind"] == "line" and e.get("stage") and e.get("disappear")]
        self.assertTrue(rib)
        self.assertLessEqual(min(e["appear"] for e in rib), texts["Vault rib"]["appear"] + 0.01)
        self.assertLess(max(e["disappear"] for e in rib) - min(e["appear"] for e in rib), 3.0)   # a short highlight

    def test_the_chain_hangs_while_hooke_is_introduced(self):
        chain = [e for e in self.els("B09") if e.get("spin")]
        quote = next(e for t, e in self.texts("B09").items() if t.startswith("“As hangs"))
        self.assertLess(max(e["appear"] for e in chain if e["kind"] == "line"), quote["appear"])
        anchors = [e for e in self.els("B09") if e["kind"] == "circle" and not e.get("spin")]
        self.assertTrue(anchors and all(e["appear"] == 0.0 for e in anchors))

    def test_the_compass_swings_from_the_first_seconds_close_up_then_pulls_back(self):
        arms = [e for e in self.els("B25") if e.get("spin")]
        self.assertEqual(sorted(round(e["spin"]["degrees"]) for e in arms), [-60, 60])
        self.assertLess(min(e["spin"]["at"] for e in arms), 2.0)
        views = self.story["B25"]["graphic"]["stage"]["views"]
        x0, y0, x1, y1 = views[0]["rect"]
        self.assertLess(x1 - x0, 0.5)                              # opens close on the operation
        self.assertEqual(views[-1]["rect"], [0.0, 0.0, 1.0, 1.0])  # back out for the larger elements

    def test_b29_closes_on_one_flyer_and_its_buttress_and_the_rest_fades(self):
        a = self.story["B29"]["animation"]
        self.assertEqual(sorted(a["views"][-1]["focus"]), ["gothic_cathedral_section_flying_buttress_east0",
                                                           "gothic_cathedral_section_pinnacle_east0"])
        ghost = next(s for s in a["steps"] if s["do"] == "GHOST")
        self.assertNotIn("gothic_cathedral_section_pier_buttress_east0", ghost["components"])
        self.assertNotIn("gothic_cathedral_section_flying_buttress_east0", ghost["components"])
        lit = [s["components"] for s in a["steps"] if s["do"] == "HIGHLIGHT" and s["start_seconds"] > a["views"][-1]["start_seconds"]]
        self.assertIn(["gothic_cathedral_section_pier_buttress_east0"], lit)
        label = next(x for x in self.story["B29"]["annotations"]["items"] if x["type"] == "COMPONENT_LABEL")
        self.assertGreater(label["appear"], a["views"][-1]["start_seconds"] + a["views"][-1]["move_seconds"])
