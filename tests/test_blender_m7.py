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



@unittest.skipUnless(blender_bin(), "Blender not installed")
class StaticFrameReuseTest(unittest.TestCase):
    """M7 render optimisation: a repeated frame is a hard link to a frame that a direct render reproduces."""

    def test_static_card_renders_once_and_reused_frames_equal_direct_renders(self):
        import os
        import subprocess
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / FILM.name
            shutil.copytree(FILM, p, ignore=shutil.ignore_patterns("renders", "output", "scenes", "qa", "audio"))
            story = json.loads((p / "storyboard/storyboard.json").read_text())
            card = next(s for s in story["shots"] if s["beat_ids"] == ["B35"])
            cmd = [blender_bin(), "--background", "--factory-startup", "--python-exit-code", "1", "--python",
                   str(ROOT / "engine/render_scene.py"), "--", "--project", str(p), "--preset", "preview",
                   "--shot", card["id"]]
            subprocess.run(cmd + ["--mode", "animation"], cwd=ROOT, capture_output=True, check=True, timeout=900)
            seq = p / "renders" / "preview" / card["id"]
            info = json.loads((seq / "render_strategy.json").read_text())
            frames = sorted(seq.glob("frame_*.png"))
            self.assertEqual(len(frames), info["frames"])
            self.assertIn(info["strategy"], ("STATIC_2D", "HYBRID", "ANIMATED_2D"))
            self.assertLess(info["rendered"], info["frames"] // 4)   # a credits card is almost entirely static
            src, first, last = max(info["reused_runs"], key=lambda r: r[2] - r[1])
            self.assertTrue(os.path.samefile(seq / f"frame_{src:04d}.png", seq / f"frame_{last:04d}.png"))
            report = Path(tmp) / "verify.json"
            subprocess.run(cmd + ["--mode", "verify-reuse", "--frames", f"{first},{last}", "--output", tmp,
                                  "--report", str(report)], cwd=ROOT, capture_output=True, check=True, timeout=900)
            rows = json.loads(report.read_text())["frames"]
            self.assertEqual([r["identical"] for r in rows], [True, True])


if __name__ == "__main__":
    unittest.main()
