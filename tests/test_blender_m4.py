"""M4 in headless Blender: realisation conventions, shared meshes, evaluated-mesh QA with
negative cases, rebuild equality and loading a library asset in another project."""
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from tools.cli import ROOT, blender_bin

SITE = "asset_library/architecture/sites/site_river_crossing_24.json"
FIVE = "asset_library/architecture/bridges/bridge_stone_arch_05.json"


@unittest.skipUnless(blender_bin(), "Blender not installed")
class BlenderArchitectureTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "reuse-demo"
            (p / "storyboard").mkdir(parents=True)
            (p / "project.json").write_text(json.dumps({"slug": "reuse-demo", "fps": 24, "duration_seconds": 2.0}))
            (p / "storyboard/states.json").write_text(json.dumps({
                "schema_version": 2, "base": {"builder": "architecture_asset", "asset": SITE},
                "shared_components": ["banks", "water"],
                "variants": [{"id": "five", "builder": "architecture_asset", "asset": FIVE}]}))
            (p / "storyboard/storyboard.json").write_text(json.dumps({"shots": [{
                "id": "S1", "duration_seconds": 2.0, "camera": "BRIDGE_THREE_QUARTER", "transition": "HOLD",
                "visual_purpose": "reuse test", "animation": {"template": "HOLD", "state": "five"}}]}))
            cmd = [blender_bin(), "--background", "--factory-startup", "--python-exit-code", "1",
                   "--python", str(ROOT / "tests/blender/m4_probe.py"), "--", str(p)]
            proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=900)
        line = next((l for l in proc.stdout.splitlines() if l.startswith("M4_PROBE ")), None)
        if line is None:
            raise AssertionError(proc.stdout[-3000:] + proc.stderr[-2000:])
        cls.r = json.loads(line[len("M4_PROBE "):])

    def test_python_plan_and_blender_agree(self):
        self.assertLess(self.r["rotation_error"], 1e-5)
        self.assertTrue(self.r["base_mesh_unapplied"])
        self.assertTrue(self.r["bevel_is_modifier"])

    def test_repeated_parts_share_one_mesh(self):
        self.assertEqual(self.r["voussoirs"], 36)
        self.assertEqual(self.r["voussoir_mesh_datablocks"], 1)

    def test_clean_model_passes_and_defects_are_caught(self):
        self.assertTrue(all(self.r["clean"].values()), self.r["clean"])
        self.assertEqual(self.r["keystone_pushed"], {"intersections_ok": False, "mentions_keystone": True})
        self.assertEqual(self.r["deck_lifted"], {"connected_ok": False, "mentions_deck": True})

    def test_rebuild_from_clean_state_is_identical(self):
        self.assertTrue(self.r["rebuild_identical"])

    def test_library_asset_loads_in_another_project(self):
        self.assertEqual(self.r["reuse_project"]["keystones_shown"], 5)
        self.assertEqual(self.r["reuse_project"]["frames"], 48)


if __name__ == "__main__":
    unittest.main()
