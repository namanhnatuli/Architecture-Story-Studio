"""Runs engine/qa_checks.py inside headless Blender (skipped when Blender is not installed).

Covers what offline tests cannot: evaluated transforms after scene.frame_set(),
local vs world space with slot parents, final visibility, camera framing, mesh
intersections in the exploded view and bit-identical rebuilds.
"""
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from tools.cli import ROOT, blender_bin, blender_command

PROJECT = ROOT / "projects" / "roof-evolution"


@unittest.skipUnless(blender_bin(), "Blender not installed")
class BlenderQATest(unittest.TestCase):
    def test_all_blender_checks_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            report = Path(tmp) / "checks.json"
            cmd = blender_command(PROJECT, "check", "preview", "--report", str(report))
            proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=600)
            self.assertTrue(report.is_file(), proc.stdout[-2000:] + proc.stderr[-2000:])
            data = json.loads(report.read_text())
        failed = [f"{r['shot']} {r['check']}: {r['detail']}" for r in data["results"] if r["status"] != "PASS"]
        self.assertEqual(failed, [])
        self.assertEqual(proc.returncode, 0)
        checks = {r["check"] for r in data["results"]}
        for required in ("plan_matches_evaluated_keys", "unanimated_parts_static", "replace_start_end_states",
                         "exploded_returns_exactly", "exploded_no_new_intersections", "final_visibility",
                         "camera_framing", "side_by_side_layout", "repeatable_build",
                         "camera_identical_across_single_model_shots"):
            self.assertIn(required, checks)


if __name__ == "__main__":
    unittest.main()
