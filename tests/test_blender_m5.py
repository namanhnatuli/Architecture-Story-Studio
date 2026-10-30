"""M5 in headless Blender: a highlighted part hidden under other parts is caught by the
visibility check, and the planner's ghosting of the covering parts makes it readable."""
import copy
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from tools.cli import ROOT, blender_bin

LEGACY = ROOT / "tests" / "fixtures" / "legacy_projects"   # archived pilots kept as regression fixtures (M7)

PILOT = LEGACY / "bridge-story-m5"


@unittest.skipUnless(blender_bin(), "Blender not installed")
class HighlightVisibilityTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        story = json.loads((PILOT / "storyboard/storyboard.json").read_text())
        src = next(s for s in story["shots"] if s["id"] == "SC_003")
        ghost = dict(copy.deepcopy(src), id="GHOST", start_seconds=0.0)
        plain = copy.deepcopy(ghost)
        plain["id"] = "PLAIN"
        for k in ("ghost", "ghost_transparency"):
            plain["animation"]["highlight"].pop(k)
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "ghost-demo"
            (p / "storyboard").mkdir(parents=True)
            (p / "project.json").write_text(json.dumps({"slug": "ghost-demo", "fps": 24,
                                                        "duration_seconds": 2 * ghost["duration_seconds"]}))
            (p / "storyboard/states.json").write_text((PILOT / "storyboard/states.json").read_text())
            (p / "storyboard/storyboard.json").write_text(json.dumps({"shots": [ghost, plain]}))
            cmd = [blender_bin(), "--background", "--factory-startup", "--python-exit-code", "1",
                   "--python", str(ROOT / "tests/blender/m5_probe.py"), "--", str(p)]
            proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=900)
        line = next((l for l in proc.stdout.splitlines() if l.startswith("M5_PROBE ")), None)
        if line is None:
            raise AssertionError(proc.stdout[-3000:] + proc.stderr[-2000:])
        cls.r = json.loads(line[len("M5_PROBE "):])

    def test_hidden_highlight_is_caught(self):
        self.assertLess(self.r["PLAIN"]["share"], self.r["threshold"])

    def test_ghosting_reveals_the_target(self):
        g = self.r["GHOST"]
        self.assertGreaterEqual(g["share"], self.r["threshold"])
        self.assertGreater(g["area"], self.r["PLAIN"]["area"] * 3)
        self.assertEqual((g["ghosts"], g["twins_shown_at_peak"], g["originals_hidden_at_peak"]), (4, 4, 4))
        self.assertTrue(g["ghosts_opaque_at_end"])


if __name__ == "__main__":
    unittest.main()
