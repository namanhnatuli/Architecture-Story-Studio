import json
import tempfile
import unittest
from pathlib import Path
from tools.validator import validate_project
from tools.cli import ROOT, project_path


class ProjectContractsTest(unittest.TestCase):
    def setUp(self):
        self.project = ROOT / "projects" / "roof-evolution"

    def test_demo_validates(self):
        errors, warnings = validate_project(self.project)
        self.assertEqual(errors, [])
        self.assertTrue(any("not verified" in warning for warning in warnings))

    def test_final_is_blocked_on_provisional_research_and_audio(self):
        errors, _ = validate_project(self.project, final=True)
        self.assertTrue(any("FINAL gate" in error for error in errors))

    def test_references_are_consistent(self):
        states = json.loads((self.project / "storyboard" / "states.json").read_text())
        ids = [v["id"] for v in states["variants"]]
        self.assertEqual(ids, ["roof_A", "roof_B"])
        self.assertEqual(states["transitions"][0]["template"], "REPLACE_PARTS")

    def test_project_slug_safety(self):
        with self.assertRaises(ValueError):
            project_path("../../etc")


if __name__ == "__main__":
    unittest.main()
