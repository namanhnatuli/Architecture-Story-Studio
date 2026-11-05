"""M6 in Blender: annotation QA on the narrated pilot and the cross-family scene contexts
(one headless Blender run each, on temporary copies)."""
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from planner import compiler, planner as pl
from tools.cli import ROOT, blender_bin

LEGACY = ROOT / "tests" / "fixtures" / "legacy_projects"   # archived pilots kept as regression fixtures (M7)

PILOT = LEGACY / "bridge-load-explained"
FIXTURE = ROOT / "tests" / "fixtures" / "m6_cross_family"


def blender_check(project, preset="preview"):
    report = Path(project) / "qa" / "blender_checks.json"
    report.parent.mkdir(parents=True, exist_ok=True)
    proc = subprocess.run([blender_bin(), "--background", "--factory-startup", "--python-exit-code", "1", "--python",
                           str(ROOT / "engine/render_scene.py"), "--", "--project", str(project), "--mode", "check",
                           "--preset", preset, "--report", str(report)],
                          cwd=ROOT, capture_output=True, text=True, timeout=1800)
    if not report.is_file():
        raise AssertionError(proc.stdout[-3000:] + proc.stderr[-2000:])
    return json.loads(report.read_text())


@unittest.skipUnless(blender_bin(), "Blender not installed")
class PilotAnnotationQATest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.p = Path(cls.tmp.name) / PILOT.name
        shutil.copytree(PILOT, cls.p, ignore=shutil.ignore_patterns("renders", "output", "scenes", "qa", "audio"))
        cls.report = blender_check(cls.p, "review")

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def rows(self, check):
        return [r for r in self.report["results"] if r["check"] == check]

    def test_every_check_passes(self):
        bad = [(r["shot"], r["check"], r["detail"]) for r in self.report["results"] if r["status"] != "PASS"]
        self.assertEqual(bad, [])

    def test_annotation_checks_ran_on_every_annotated_shot(self):
        story = json.loads((self.p / "storyboard/storyboard.json").read_text())
        annotated = {s["id"] for s in story["shots"] if s.get("annotations")}
        for check in ("annotation_objects", "annotation_anchors", "annotation_layout", "annotation_timing"):
            self.assertEqual({r["shot"] for r in self.rows(check)}, annotated, check)
        self.assertTrue(all("attached to their own components" in r["detail"] for r in self.rows("annotation_anchors")))

    def test_captions_stay_above_the_subtitles(self):
        rows = self.rows("captions_clear_of_subtitles")
        self.assertGreaterEqual(len(rows), 4)    # three sequential captions + the overview stack
        self.assertTrue(all(r["status"] == "PASS" for r in rows))


@unittest.skipUnless(blender_bin(), "Blender not installed")
class CrossFamilyBlenderTest(unittest.TestCase):
    """Bridge and roof shots in one project: each shot is built on its own scene context."""

    def test_both_contexts_build_and_pass_qa(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "m6-cross-family"
            shutil.copytree(FIXTURE, p)
            plan = pl.plan_project(p)
            compiler.compile_plan(plan, p)
            report = blender_check(p)
            bad = [(r["shot"], r["check"], r["detail"]) for r in report["results"] if r["status"] != "PASS"]
            self.assertEqual(bad, [])
            regs = {r["shot"]: r["detail"] for r in report["results"] if r["check"] == "components_registered"}
            self.assertEqual(len(regs), len(plan["shots"]))
            cams = next(r for r in report["results"] if r["check"] == "camera_identical_across_single_model_shots")
            self.assertEqual(cams["status"], "PASS")


if __name__ == "__main__":
    unittest.main()
