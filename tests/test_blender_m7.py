"""M7 in Blender: the whole documentary passes the engine QA on a temporary copy (cards with
archival images, NOTE captions, push-ins, every 3D template) in one headless run."""
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from tests.test_blender_m6 import blender_check
from tools.cli import ROOT, blender_bin

FILM = ROOT / "projects" / "why-bridges-look-different"


@unittest.skipUnless(blender_bin(), "Blender not installed")
class DocumentaryBlenderQATest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.p = Path(cls.tmp.name) / FILM.name
        shutil.copytree(FILM, cls.p, ignore=shutil.ignore_patterns("renders", "output", "scenes", "qa", "audio"))
        cls.report = blender_check(cls.p, "review")
        cls.story = json.loads((cls.p / "storyboard/storyboard.json").read_text())

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def rows(self, check):
        return [r for r in self.report["results"] if r["check"] == check]

    def test_every_check_passes(self):
        bad = [(r["shot"], r["check"], r["detail"]) for r in self.report["results"] if r["status"] != "PASS"]
        self.assertEqual(bad, [])

    def test_every_card_is_checked_including_layout(self):
        cards = {s["id"] for s in self.story["shots"] if s.get("visual_type") == "MOTION_GRAPHICS"}
        self.assertGreaterEqual(len(cards), 14)
        self.assertEqual({r["shot"] for r in self.rows("card_layout")}, cards)

    def test_push_in_shots_report_their_camera_move(self):
        moves = {s["id"] for s in self.story["shots"] if (s.get("animation") or {}).get("camera_move")}
        self.assertGreaterEqual(len(moves), 4)
        rows = {r["shot"]: r for r in self.rows("camera_locked")}
        for sid in moves:
            self.assertIn("push-in", rows[sid]["detail"].lower(), sid)

    def test_push_in_annotations_stay_screen_fixed(self):
        annotated = {s["id"] for s in self.story["shots"] if (s.get("animation") or {}).get("camera_move")
                     and (s.get("annotations") or {}).get("items")}
        self.assertGreaterEqual(len(annotated), 3)
        rows = {r["shot"]: r for r in self.rows("overlays_screen_fixed")}
        self.assertEqual(set(rows), annotated)
        self.assertTrue(all(r["status"] == "PASS" for r in rows.values()))


if __name__ == "__main__":
    unittest.main()
