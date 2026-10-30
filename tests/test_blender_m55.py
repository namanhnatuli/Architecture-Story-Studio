"""M5.5 in headless Blender: Level 2 (ray casts on evaluated meshes) confirms the Level 1
offline estimate - the hidden beam, its ghosting repair and the separated voussoirs."""
import copy
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from planner import camera as CAM, visibility as VIS
from tools.cli import ROOT, blender_bin

LEGACY = ROOT / "tests" / "fixtures" / "legacy_projects"   # archived pilots kept as regression fixtures (M7)

PILOT = LEGACY / "bridge-story-m5"
CFG = json.loads((ROOT / "config/visual_planning.json").read_text())["visibility"]


@unittest.skipUnless(blender_bin(), "Blender not installed")
class LevelTwoVisibilityTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        story = json.loads((PILOT / "storyboard/storyboard.json").read_text())
        states = json.loads((PILOT / "storyboard/states.json").read_text())
        by_id = {s["id"]: s for s in story["shots"]}
        plain = copy.deepcopy(by_id["SC_003"])
        plain["id"] = "PLAIN"
        for k in ("ghost", "ghost_transparency"):
            plain["animation"]["highlight"].pop(k)
        cls.shots = [dict(copy.deepcopy(by_id["SC_003"]), id="GHOST"), plain, dict(copy.deepcopy(by_id["SC_007"]), id="PIECES")]
        t = 0.0
        for s in cls.shots:
            s["start_seconds"] = t
            t += s["duration_seconds"]
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "visibility-demo"
            (p / "storyboard").mkdir(parents=True)
            (p / "project.json").write_text(json.dumps({"slug": "visibility-demo", "fps": 24, "duration_seconds": t}))
            (p / "storyboard/states.json").write_text(json.dumps(states))
            (p / "storyboard/storyboard.json").write_text(json.dumps({"shots": cls.shots}))
            out = Path(tmp) / "measured.json"
            cmd = [blender_bin(), "--background", "--factory-startup", "--python-exit-code", "1", "--python",
                   str(ROOT / "engine/qa_visibility.py"), "--", "--project", str(p), "--out", str(out)]
            proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=900)
            if not out.is_file():
                raise AssertionError(proc.stdout[-3000:] + proc.stderr[-2000:])
            cls.l2 = json.loads(out.read_text())["shots"]
        cls.l1 = {s["id"]: VIS.assess_all_frames(s, states, 24, CAM.style_presets(), CFG) for s in cls.shots}

    def pair(self, sid, label, concept):
        a = next(r for r in self.l1[sid]["rows"][label] if r["concept"] == concept)
        b = next(r for r in self.l2[sid]["rows"][label] if r["concept"] == concept)
        return a, b

    def test_same_frames_are_evaluated(self):
        for sid in self.l2:
            self.assertEqual(self.l2[sid]["frames"], self.l1[sid]["frames"])

    def test_hidden_beam_and_its_repair_are_measured_in_blender(self):
        a, b = self.pair("PLAIN", "highlight_peak", "stringer")
        self.assertLess(b["visible_share"], CFG["min_visible_share"])
        self.assertFalse(VIS.verdict(b, CFG)[0])
        self.assertAlmostEqual(a["visible_share"], b["visible_share"], delta=0.03)
        a, b = self.pair("GHOST", "highlight_peak", "stringer")
        self.assertGreater(b["visible_share"], 0.75)       # planks at 0.7 transparency do not occlude
        self.assertTrue(VIS.verdict(b, CFG)[0])
        self.assertAlmostEqual(a["visible_share"], b["visible_share"], delta=0.03)

    def test_every_voussoir_reads_on_its_own_when_separated(self):
        a, b = self.pair("PIECES", "exploded_hold", "voussoir")
        self.assertEqual(set(a["components"]), set(b["components"]))
        self.assertTrue(VIS.verdict(b, CFG, pieces=True)[0])
        for cid, c in b["components"].items():
            self.assertAlmostEqual(c["visible_share"], a["components"][cid]["visible_share"], delta=0.05, msg=cid)

    def test_levels_agree_on_every_frame(self):
        rows = 0
        for sid, data in self.l2.items():
            for label, l2rows in data["rows"].items():
                for b in l2rows:
                    if not b.get("shown"):
                        continue
                    a = next(r for r in self.l1[sid]["rows"][label] if r["concept"] == b["concept"])
                    self.assertEqual(VIS.verdict(a, CFG)[0], VIS.verdict(b, CFG)[0], f"{sid} {label} {b['concept']}")
                    rows += 1
        self.assertGreater(rows, 20)


if __name__ == "__main__":
    unittest.main()
