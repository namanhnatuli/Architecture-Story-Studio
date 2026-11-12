"""Floating-city production layer L4 (projects/floating-city-design-challenge/script/visuals.py): every amount the 3D
shots move or turn comes from analysis/results.json, conceptual motion is labelled on screen, the locked narration is
untouched; and the planner rules this layer needed (sentence counts from the locked timing, colour words inside
technical terms, the on-screen motion label)."""
import importlib
import json
import sys
import unittest
from pathlib import Path

from engine import motion
from planner import annotations as AN, consistency, vocabulary as V

ROOT = Path(__file__).resolve().parents[1]
P = ROOT / "projects" / "floating-city-design-challenge"


def load_visuals():
    sys.path.insert(0, str(P / "script"))
    try:
        return importlib.import_module("visuals")
    finally:
        sys.path.remove(str(P / "script"))


def steps_of(v):
    return (v.get("sequence") or {}).get("steps") or []


@unittest.skipUnless((P / "script" / "visuals.py").is_file(), "floating-city production layer not present")
class VisualsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.V = load_visuals()
        cls.res = json.loads((P / "analysis/results.json").read_text())

    def test_every_beat_has_a_visual(self):
        beats = json.loads((P / "script/narration.json").read_text())["beats"]
        self.assertEqual(sorted(self.V.VISUALS), sorted(b["id"] for b in beats))

    def test_sink_and_rise_are_the_calculated_branch(self):
        st = self.res["storey_branch"]["steps"]
        self.assertAlmostEqual(self.V.SINK, st[0]["freeboard_m"] - st[1]["freeboard_m"], places=6)
        # the deeper hull: its bottom goes down by the extension, then the platform floats up to the new freeboard
        self.assertAlmostEqual(-self.V.SINK - self.V.EXT + self.V.RISE, -(st[2]["draft_m"] - st[0]["draft_m"]), places=6)
        self.assertAlmostEqual(st[0]["freeboard_m"] - self.V.SINK + self.V.RISE, st[2]["freeboard_m"], places=6)
        moves = [s["offset"][2] for s in steps_of(self.V.VISUALS["B09"]) if s["do"] == "MOVE"]
        self.assertEqual(moves, [-self.V.SINK])
        moves = [s["offset"][2] for s in steps_of(self.V.VISUALS["B10"]) if s["do"] == "MOVE"]
        self.assertEqual(moves, [-self.V.SINK, -self.V.EXT, self.V.RISE])

    def test_tilt_is_the_list_calculated_for_the_state_shown(self):
        rot = [s for s in steps_of(self.V.VISUALS["B11"]) if s["do"] == "ROTATE"]
        shown = self.res["list_example_shown_state"]
        self.assertIn("4 storeys, hull 4.5 m", shown["state"])        # B11 shows the end of B10
        self.assertEqual([s["degrees"] for s in rot], [shown["list_deg"]])
        self.assertTrue(0.35 <= shown["list_deg"] < 0.5 and 0.35 <= self.res["list_example"]["list_deg"] < 0.5)   # "about 0.4"
        load = [s for s in steps_of(self.V.VISUALS["B11"]) if s["do"] == "MOVE" and s["offset"][0]]
        self.assertEqual(load[0]["offset"], [self.res["list_example"]["d_m"], 0.0, 0.0])

    def test_the_camera_is_still_whenever_the_platform_moves_or_grows(self):
        """Owner review of the L5 excerpt: frame first, then sink; B10 keeps two framings."""
        plan = json.loads((P / "storyboard/visual_plan.json").read_text())
        for bid in ("B09", "B10"):
            anim = next(s for s in plan["shots"] if s["beat_id"] == bid)["shot"]["animation"]
            cams = [(v["start_seconds"], v["start_seconds"] + v["move_seconds"]) for v in anim["views"][1:]]
            changes = [(st["start_seconds"], st["start_seconds"] + st["seconds"]) for st in anim["steps"]
                       if st["do"] in ("MOVE", "REVEAL") and st["seconds"] > 0]
            self.assertTrue(changes, bid)
            for c0, c1 in cams:
                for m0, m1 in changes:
                    self.assertFalse(c0 < m1 and m0 < c1, f"{bid}: camera {c0:.2f}-{c1:.2f} while {m0:.2f}-{m1:.2f}")
            if bid == "B10":
                self.assertEqual(len({tuple(v["focus"] or ()) for v in anim["views"]}), 2)   # two framings

    def test_water_made_see_through_keeps_its_colour(self):
        """Owner review of R2: ghosted water must still read as water (the surface, its colour, the waterline)."""
        n = 0
        for bid, v in self.V.VISUALS.items():
            for st in steps_of(v):
                if st["do"] == "GHOST" and st["targets"] == self.V.WATER_SITE:
                    n += 1
                    self.assertLessEqual(st["transparency"], 0.65, bid)
        self.assertEqual(n, 7)
        b24 = steps_of(self.V.VISUALS["B24"])
        ghost = next(st for st in b24 if st["do"] == "GHOST")
        self.assertNotEqual(ghost["at"], 0)   # B24 opens on the full water, then makes it see-through

    def test_below_the_surface_the_camera_goes_level_outside_the_water(self):
        """Full review (2026-11-11): seen from above, the see-through water's surface read as a floor and the seabed's
        shade as ground. The mooring and cable beats end on a level view whose camera stands outside the site's water."""
        hood = json.loads((ROOT / "asset_library/architecture/sites/site_bay_01.json").read_text())["parameters"]
        sea = json.loads((ROOT / "asset_library/architecture/sites/site_open_sea_01.json").read_text())["parameters"]
        half_diagonal = {k: 0.5 * (s["site_width_m"] ** 2 + s["site_length_m"] ** 2) ** 0.5 for k, s in (("hood", hood), ("sea", sea))}
        # v2 (Codex review of the full cut v1): B33-B34 go level too; the water clears late in the descent, so the
        # platforms' shade on the seabed never shows as a grid from above (9:23, 9:32)
        for bid, site in (("B22", "hood"), ("B24", "hood"), ("B30", "sea"), ("B31", "sea"), ("B33", "hood"), ("B34", "hood")):
            seq = self.V.VISUALS[bid]["sequence"]
            self.assertEqual(seq["camera"], "FLOAT_UNDERWATER", bid)
            last = seq["views"][-1]
            self.assertLessEqual(abs(last["elevation"]), 1.0, bid)
            self.assertGreater(last["clearance"], half_diagonal[site], bid)   # in front of the water's near face
            motion.sequence_views({"views": [{}, {"start_seconds": 1.0, "move_seconds": 1.0, "clearance": last["clearance"]}]})
            ghost = next(st for st in steps_of(self.V.VISUALS[bid]) if st["do"] == "GHOST" and st["targets"] == self.V.WATER_SITE)
            self.assertEqual((ghost["at"]["sentence"], ghost["at"]["word"]), (last["at"]["sentence"], last["at"]["word"]), bid)
            self.assertAlmostEqual(ghost["at"].get("offset", 0.0) - last["at"].get("offset", 0.0), self.V.CLEAR_AFTER, msg=bid)
            self.assertGreaterEqual(self.V.CLEAR_AFTER + ghost["seconds"], last["move_seconds"], bid)   # clear once level

    def test_chapters_after_the_first_open_with_their_numbered_title(self):
        chapters = json.loads((P / "script/chapters.json").read_text())["chapters"]
        beats = {b["beat_id"]: b for b in json.loads((P / "script/visual_beats.json").read_text())["beats"]}
        for k, c in enumerate(chapters[1:], 2):
            texts = [a.get("text") for a in beats[c["beat_ids"][0]].get("annotations") or []]
            self.assertIn(f"{k} · {c['title']}", texts, c["id"])

    def test_close_details_are_framed_close_when_they_are_named(self):
        """Full review: the hinge pins (B13) were seen end-on; the bridge deck hid the wastewater line (B27); the bridge,
        route and lines of B28 and the systems of B38 were specks in the whole district."""
        b13 = self.V.VISUALS["B13"]["sequence"]["views"]
        self.assertEqual(b13[-1]["frame"], self.V.WALK)
        self.assertGreaterEqual(b13[-1]["elevation"], 20.0)
        step13 = next(a for a in self.V.VISUALS["B13"]["annotations"] if a["id"] == "B13_step")
        self.assertEqual(step13["until"], 2)   # the label leaves before the camera moves
        plan = {s["beat_id"]: s["shot"].get("animation") for s in json.loads((P / "storyboard/visual_plan.json").read_text())["shots"]}
        b27 = plan["B27"]["steps"]
        ghost = next(st for st in b27 if st["do"] == "GHOST")
        first_glow = min(st["start_seconds"] for st in b27 if st["do"] == "HIGHLIGHT")
        self.assertLessEqual(ghost["start_seconds"] + ghost["seconds"], first_glow)
        b28 = self.V.VISUALS["B28"]["sequence"]
        self.assertNotIn(self.V.ALL_HULLS[0], b28["views"][0]["frame"])   # opens close on one bridge
        b38 = plan["B38"]
        self.assertEqual(sum(1 for st in b38["steps"] if st["do"] == "HIGHLIGHT"), 2)

    def test_opening_goes_from_the_district_to_a_park_and_back(self):
        b01, b02 = self.V.VISUALS["B01"]["sequence"], self.V.VISUALS["B02"]["sequence"]
        first, *_, last = b01["views"]
        self.assertEqual(first["frame"], self.V.WHOLE)
        self.assertIn(self.V.PARK[0], [r for vw in b01["views"] for r in vw["frame"]])
        cont = {k: v for k, v in last.items() if k not in ("at", "move_seconds")}
        self.assertEqual(b02["views"][0], cont)   # B02 opens on the frame B01 ends on: the cut does not jump
        self.assertEqual(b02["views"][1]["frame"], self.V.WHOLE)
        self.assertEqual(b02["views"][-1]["frame"], self.V.ONE_PLATFORM)   # L6 review: "Let's treat it..." goes to one platform
        self.assertEqual([(c, r) for c, r, _ in self.V.KEEP], [self.V.CENTRE])   # the platform B04 strips down to
        self.assertEqual([(st["do"], st["targets"]) for st in b02["steps"]], [("HIGHLIGHT", self.V.ONE_PLATFORM_ALL)])   # one glow
        garden = self.V.OPEN_GARDEN
        self.assertEqual(self.V.F.district_kind(*garden)[0], "garden")
        self.assertEqual(self.V.F.GARDEN_SIDE[garden], "-y")   # it opens toward the aerial camera (azimuth -62)

    def test_opening_holds_each_framing_long_enough_to_read(self):
        """L6 review: the park held about 0.67 s before the camera left; B02 held the whole district for 10 s."""
        plan = json.loads((P / "storyboard/visual_plan.json").read_text())
        views = {bid: next(s for s in plan["shots"] if s["beat_id"] == bid)["shot"]["animation"]["views"]
                 for bid in ("B01", "B02")}
        settled = lambda v: v["start_seconds"] + v["move_seconds"]   # noqa: E731
        b01, b02 = views["B01"], views["B02"]
        self.assertEqual(len(b01), 4)
        self.assertGreaterEqual(b01[3]["start_seconds"] - settled(b01[2]), 1.5)   # the park
        self.assertGreaterEqual(b01[2]["start_seconds"] - settled(b01[1]), 0.8)   # the cluster: a pass, its schools glow
        self.assertEqual(len(b02), 3)
        self.assertLessEqual(b02[2]["start_seconds"] - settled(b02[1]), 4.0)      # the whole district, then one platform
        self.assertGreater(b02[2]["start_seconds"], 6.5)                          # at the second sentence

    def test_conceptual_motion_is_labelled_on_screen_for_the_whole_beat(self):
        for bid, v in self.V.VISUALS.items():
            if any(s["do"] == "OSCILLATE" for s in steps_of(v)):
                self.assertEqual(v.get("motion_label"), motion.CONCEPT_MOTION_LABEL, bid)
                notes = [a for a in v.get("annotations", []) if a["type"] == "NOTE" and a["text"] == motion.CONCEPT_MOTION_LABEL]
                self.assertTrue(notes and notes[0]["sentence"] == 0 and "until" not in notes[0] and "word" not in notes[0], bid)

    def test_moorings_and_joints_are_marked_conceptual(self):
        texts = {bid: " ".join(a.get("text", "") for a in v.get("annotations", [])) for bid, v in self.V.VISUALS.items()}
        self.assertIn("not sized", texts["B14"])
        self.assertIn("not sized", texts["B24"])

    def test_no_photograph_of_schoonschip(self):
        for bid, v in self.V.VISUALS.items():
            for e in (v.get("graphic") or {}).get("elements", []):
                self.assertNotEqual(e["kind"], "image", bid)


class PlannerRulesTest(unittest.TestCase):
    def test_sentence_counts_follow_the_locked_timing(self):
        doc = {"beats": [{"beat_id": "B1", "narration": "One. Two, three, four.", "claim_ids": [],
                          "annotations": [{"id": "n", "type": "NOTE", "text": "x", "sentence": 2}]}]}
        self.assertTrue(AN.validate_spec(doc, {"claims": []}, V.Vocabulary()))                  # 2 sentences by punctuation
        self.assertEqual(AN.validate_spec(doc, {"claims": []}, V.Vocabulary(), {"B1": 3}), [])   # 3 narration items

    def test_motion_label_may_exceed_the_note_length_only_verbatim(self):
        def doc(text):
            return {"beats": [{"beat_id": "B1", "narration": "One.", "claim_ids": [],
                               "annotations": [{"id": "n", "type": "NOTE", "text": text, "sentence": 0}]}]}
        self.assertEqual(AN.validate_spec(doc(motion.CONCEPT_MOTION_LABEL), {"claims": []}, V.Vocabulary()), [])
        self.assertTrue(AN.validate_spec(doc(motion.CONCEPT_MOTION_LABEL + " (approx.)"), {"claims": []}, V.Vocabulary()))

    def test_colour_words_inside_technical_terms_name_no_colour(self):
        style = json.loads((ROOT / "config/annotation_style.json").read_text())
        plan = {"shots": [{"shot_id": "S1", "beat_id": "B1", "template": "HOLD", "timing": {"beat_offset_seconds": 0.0, "duration_seconds": 5.0},
                           "annotations": {"items": []}, "shot": {"animation": {"template": "HOLD"}}}]}
        doc = {"beats": [{"beat_id": "B1", "narration": "Gray water from showers, black water from toilets."}]}
        rows = consistency.check_plan(plan, doc, {"B1": [(0.0, 5.0)]}, style)
        self.assertFalse([r for r in rows if r["rule"] == "COLOUR"])
        doc = {"beats": [{"beat_id": "B1", "narration": "The gray band shows the hull."}]}
        rows = consistency.check_plan(plan, doc, {"B1": [(0.0, 5.0)]}, style)
        self.assertTrue([r for r in rows if r["rule"] == "COLOUR" and r["verdict"] == "CONTRADICTION"])


if __name__ == "__main__":
    unittest.main()
