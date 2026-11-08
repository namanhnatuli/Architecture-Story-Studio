"""Floating family (engine/arch/families/floating.py): the pontoon sits at the project's calculated draft, a section
keeps only the cut half with plates on the cut, the blocks cover the stated share of the deck, and the parts the story
switches on and off exist with stable ids."""
import json
import unittest
from pathlib import Path

from engine.arch import assets, semantic
from engine.arch.families import floating

ROOT = Path(__file__).resolve().parents[1]
LIB = ROOT / "asset_library/architecture"
RESULTS = ROOT / "projects/floating-city-design-challenge/analysis/results.json"


def params(**kw):
    p, errors = assets.resolve_params("floating", "platform", kw)
    assert not errors, errors
    return p


def bbox(comps, cid):
    c = next(c for c in comps if c.id == cid)
    return semantic.union_bbox([c])


class PlatformTest(unittest.TestCase):
    def test_hull_sits_at_the_draft_and_deck_at_the_freeboard(self):
        comps = floating.platform(params(draft_m=2.958))
        lo, hi = bbox(comps, "hull_bottom")
        self.assertAlmostEqual(lo[2], -2.958, places=6)
        lo, hi = bbox(comps, "deck")
        self.assertAlmostEqual(hi[2], 4.0 - 2.958, places=6)

    def test_section_keeps_the_cut_half_and_adds_plates(self):
        comps = floating.platform(params(section=1))
        for c in comps:
            lo, _ = semantic.union_bbox([c])
            if c.type not in ("SECTION_CUT", "DISPLACED_VOLUME", "WATER"):
                self.assertGreaterEqual(lo[1], -1e-9, c.id)
        types = {c.type for c in comps}
        self.assertTrue({"SECTION_CUT", "DISPLACED_VOLUME", "WATER"} <= types)
        self.assertFalse(any(c.id == "hull_wall_south" for c in comps))
        self.assertFalse(any(c.id.startswith("bulkhead_y") and abs(semantic.union_bbox([c])[0][1]) < 0.5 for c in comps))

    def test_blocks_cover_the_stated_share(self):
        p = params(building_cover=0.4, storeys=3)
        area = sum((x1 - x0) * (y1 - y0) for x0, x1, y0, y1 in floating.block_layout(40.0, 40.0, 0.4))
        self.assertAlmostEqual(area / 1600.0, 0.4, places=9)
        comps = floating.platform(p)
        self.assertEqual(sum(c.id.endswith("_storey1") for c in comps), 4)

    def test_story_parts_exist(self):
        comps = {c.id for c in floating.platform(params(storeys=4, extension_m=0.5, section=1))}   # section: blocks 2 and 4 (y > 0)
        self.assertNotIn("block1_storey1", comps)
        for cid in ("block2_storey4", "block2_roof3", "block2_roof4", "hull_ext_west", "hull_ext_bulkhead_x1",
                    "cut_ext_wall_west", "displaced_volume", "water_below", "cut_bottom"):
            self.assertIn(cid, comps)

    def test_compatibility_checks(self):
        self.assertTrue(floating.compatibility_errors(params(draft_m=4.2, hull_depth_m=4.0)))
        self.assertTrue(floating.compatibility_errors(params(length_m=35.0)))
        self.assertEqual(floating.compatibility_errors(params()), [])

    def test_library_platform_uses_the_projects_calculated_draft(self):
        res = json.loads(RESULTS.read_text())
        for name in ("floating_platform_a_01.json", "floating_platform_a_section_01.json"):
            data, _ = assets.load(LIB / "floating" / name)
            self.assertEqual(assets.validate(data), [])
            self.assertEqual(data["parameters"]["draft_m"], res["design_A"]["mid"]["draft_m"], name)
            self.assertIsNotNone(assets.site_for(LIB / "floating" / name), name)

    def test_section_bay_keeps_the_hull_footprint_dry(self):
        p, _ = assets.resolve_params("site", "bay", {"section": 1, "hole_length_m": 40.0, "hole_width_m": 40.0})
        comps = floating.bay(p)
        for c in comps:
            if c.type == "WATER" and c.group == "water":
                (x0, y0, _), (x1, y1, _) = semantic.union_bbox([c])
                inside_x = x0 < 20.0 - 1e-9 and x1 > -20.0 + 1e-9
                inside_y = y0 < 20.0 - 1e-9
                self.assertFalse(inside_x and inside_y, c.id)


if __name__ == "__main__":
    unittest.main()
