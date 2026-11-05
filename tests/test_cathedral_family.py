"""The cathedral family (engine/arch/families/cathedral.py) and what it added to the planner (offline, no Blender)."""
import json
import unittest
from pathlib import Path

from engine import annotation_layout as AL
from engine.arch import assets, checks, semantic
from planner import annotations, catalog, resolver, vocabulary as V

ROOT = Path(__file__).resolve().parent.parent
GOTHIC = ROOT / "asset_library/architecture/cathedrals/cathedral_gothic_section_01.json"
ROMANESQUE = ROOT / "asset_library/architecture/cathedrals/cathedral_romanesque_section_01.json"
SITE = ROOT / "asset_library/architecture/sites/site_level_ground.json"


class CathedralAssetsTest(unittest.TestCase):
    def test_specs_pass_every_offline_check(self):
        for path in (GOTHIC, ROMANESQUE, SITE):
            data, _ = assets.load(path)
            params = assets.resolve_params(data["family"], data["variant"], data["parameters"])[0]
            for check, ok, detail in checks.check_asset(data, assets.plan(data), params):
                self.assertTrue(ok, (path.name, check, detail))

    def test_every_part_the_film_names_is_its_own_role(self):
        roles = {c.role for c in assets.plan_file(GOTHIC)}
        for role in ("nave_pier", "rib", "vault_web", "clerestory_window", "flying_buttress", "pier_buttress", "pinnacle", "aisle_roof"):
            self.assertIn(role, roles)
        roles = {c.role for c in assets.plan_file(ROMANESQUE)}
        for role in ("barrel_vault", "thick_wall", "shallow_buttress", "small_window"):
            self.assertIn(role, roles)

    def test_the_web_is_real_stone_and_every_vault_crown_is_level(self):
        comps = assets.plan_file(GOTHIC)
        web = [c for c in comps if c.type == "VAULT_WEB"]
        params = assets.resolve_params("cathedral", "gothic_section", {})[0]
        self.assertEqual(len(web), params["bay_count"])
        for c in web:      # a closed slab with thickness, not a surface
            lo, hi = semantic.bbox(c)
            self.assertAlmostEqual(hi[2], params["vault_crown_m"] + 0.45, places=3)
            self.assertGreater(len(c.mesh["faces"]), 40)
        ribs = [semantic.bbox(c)[1][2] for c in comps if c.type == "RIB"]
        self.assertLess(max(ribs) - min(ribs), 0.05)    # their section differs a little; the arcs meet one level

    def test_one_frame_of_the_church_can_be_named_on_its_own(self):
        comps = assets.plan_file(GOTHIC)
        frame = {c.type for c in comps if c.group == "frame_east0"}
        self.assertEqual(frame, {"NAVE_PIER", "FLYING_BUTTRESS", "PIER_BUTTRESS", "PINNACLE"})

    def test_the_gothic_model_is_taller_than_the_romanesque_one(self):
        height = lambda path: assets.describe(assets.load(path)[0])["dimensions_m"][2]   # noqa: E731
        self.assertGreater(height(GOTHIC), 2 * height(ROMANESQUE))

    def test_vocabulary_concepts_resolve_to_the_library(self):
        vocab, index = V.Vocabulary(ROOT / "config/visual_vocabulary.json"), catalog.index(ROOT)
        for concept, asset in (("gothic_cathedral_section", "cathedral_gothic_section_01"),
                               ("romanesque_church_section", "cathedral_romanesque_section_01"),
                               ("cathedral_ground_site", "site_level_ground")):
            r = resolver.resolve(concept, vocab, index)
            self.assertEqual((r["status"], r["asset_id"]), ("REUSE_EXISTING", asset))

    def test_a_section_stands_on_its_level_site_not_on_the_river(self):
        self.assertEqual(assets.site_for(GOTHIC), "asset_library/architecture/sites/site_level_ground.json")

    def test_cameras_exist_and_the_low_one_hides_only_what_blocks_it(self):
        style = json.loads((ROOT / "config/visual_style.json").read_text())["camera"]["presets"]
        self.assertGreater(style["CATHEDRAL_SECTION"]["elevation_degrees"], 0)
        self.assertNotIn("hide_ground", style["CATHEDRAL_SECTION"])
        below = style["CATHEDRAL_FROM_BELOW"]
        self.assertLess(below["elevation_degrees"], 0)
        self.assertTrue(below["hide_ground"])
        self.assertEqual(sorted(below["hide_roles"]), ["floor", "ground"])


class ThrustArrowTest(unittest.TestCase):
    def test_a_force_arrow_needs_its_claim(self):
        self.assertIn("THRUST_ARROW", AL.FORCE_TYPES)
        self.assertTrue(annotations.needs_claim({"type": "THRUST_ARROW"}))
        vocab = V.Vocabulary(ROOT / "config/visual_vocabulary.json")
        doc = {"beats": [{"beat_id": "B1", "narration": "It pushes.", "claim_ids": [], "annotations": [
            {"id": "a", "type": "THRUST_ARROW", "target": "barrel_vault", "sentence": 0}]}]}
        errors = annotations.validate_spec(doc, {"claims": []}, vocab)
        self.assertTrue(any("claim_id" in e for e in errors), errors)


if __name__ == "__main__":
    unittest.main()
