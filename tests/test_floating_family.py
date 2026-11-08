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



def spec(name):
    data, _ = assets.load(LIB / "floating" / f"{name}.json")
    assert assets.validate(data) == [], name
    p, errors = assets.resolve_params("floating", data["variant"], data.get("parameters", {}))
    assert not errors, errors
    return data, p


def site_params(data):
    site, _ = assets.load(ROOT / data["site"])
    p, errors = assets.resolve_params("site", site["variant"], site.get("parameters", {}))
    assert not errors, errors
    return p


class LibraryVariantsTest(unittest.TestCase):
    def setUp(self):
        self.res = json.loads(RESULTS.read_text())

    def test_every_floating_spec_builds_the_counts_the_checks_expect(self):
        from engine.arch import checks
        for path in sorted((LIB / "floating").glob("*.json")):
            data, p = spec(path.stem)
            comps = assets.FAMILIES["floating"][data["variant"]]["generator"](p)
            counts = {}
            for c in comps:
                counts[c.type] = counts.get(c.type, 0) + 1
            for t, n in checks.expected_counts("floating", data["variant"], p).items():
                self.assertEqual(counts.get(t, 0), n, f"{path.stem} {t}")

    def test_pair_decks_differ_by_the_calculated_step(self):
        rev = self.res["revisions"]["B_neighbours_2_vs_4_storeys"]
        data, p = spec("floating_pair_b_01")
        self.assertEqual((p["draft_a_m"], p["draft_b_m"]), (rev["draft_2_storeys_m"], rev["draft_4_storeys_m"]))
        comps = floating.pair(p)
        deck = {c.id: c.location[2] for c in comps if c.type == "DECK"}
        self.assertAlmostEqual(deck["platform_a_deck"] - deck["platform_b_deck"], rev["deck_level_step_m"], places=6)
        self.assertTrue(any(c.type == "WALKWAY" for c in comps) and sum(c.type == "CONNECTOR" for c in comps) == 2)

    def test_clay_boat_block_holds_the_hulls_concrete(self):
        cb = self.res["clay_boat"]
        data, p = spec("floating_clay_boat_01")
        self.assertEqual(p["block_side_m"], cb["solid_cube_side_m"])
        self.assertEqual(p["draft_m"], cb["hollow_box_draft_hull_only_m"])
        self.assertAlmostEqual(p["block_side_m"] ** 3, cb["concrete_m3"], delta=0.01 * cb["concrete_m3"])
        comps = {c.id: c for c in floating.clay_boat(p)}
        lo, hi = semantic.union_bbox([comps["solid_block"]])
        self.assertAlmostEqual(lo[2], -p["water_depth_m"], places=6)        # resting on the seabed
        self.assertLess(hi[2], 0.0)                                         # entirely under water
        self.assertNotIn("block1_storey1", comps)                           # hull only

    def test_neighbourhood_moorings(self):
        _, piles = spec("floating_neighbourhood_piles_01")
        _, lines = spec("floating_neighbourhood_lines_01")
        a, b = floating.neighbourhood(piles), floating.neighbourhood(lines)
        self.assertEqual(sum(c.type == "MOORING_PILE" for c in a), 10)
        self.assertFalse(any(c.type in ("MOORING_LINE", "ANCHOR") for c in a))
        self.assertEqual(sum(c.type == "MOORING_LINE" for c in b), 10)
        self.assertFalse(any(c.type == "MOORING_PILE" for c in b))
        for c in b:   # nothing reaches below the seabed; anchors sit on it
            lo, _ = semantic.union_bbox([c])
            self.assertGreaterEqual(lo[2], -lines["water_depth_m"] - 1e-6, c.id)
            if c.type == "ANCHOR":
                self.assertAlmostEqual(lo[2], -lines["water_depth_m"], places=6)
        for c in a + b:
            if c.type in ("MOORING_LINE", "ANCHOR"):
                self.assertIn("not sized", c.meta["note"])

    def test_district_is_design_c(self):
        dc = self.res["district_C"]
        data, p = spec("floating_district_01")
        self.assertEqual(p["draft_m"], dc["module_draft_m"])
        self.assertEqual(p["length_m"], dc["module_m"])
        cells = floating.district_cells()
        self.assertEqual(len(cells), dc["modules"])
        self.assertEqual(sum(u == "home" for _, _, u in cells), 66)
        comps = floating.district(p)
        self.assertEqual(sum(c.type == "HULL" for c in comps), dc["modules"])
        self.assertEqual(sum(c.type == "LINK_SPAN" for c in comps), p["bridges"])
        nets = {c.meta.get("network") for c in comps if c.type == "UTILITY_LINE"}
        self.assertEqual(nets, {"power", "water", "wastewater"})

    def test_district_link_span_is_the_analysed_bridge(self):
        data, p = spec("floating_district_01")
        self.assertIn("25_m_bridge", self.res["link_span"])
        self.assertEqual(p["shore_gap_m"], 25.0)

    def test_district_moorings_follow_the_sites_seabed(self):
        data, p = spec("floating_district_01")
        site = site_params(data)
        self.assertEqual((p["depth_near_m"], p["depth_far_m"], p["seabed_run_m"]),
                         (site["water_depth_m"], site["depth_far_m"], site["site_length_m"]))

        def seabed(y):
            return -(site["water_depth_m"] + (site["depth_far_m"] - site["water_depth_m"]) * min(1.0, max(0.0, y / site["site_length_m"])))

        zt = p["hull_depth_m"] - p["draft_m"]
        n_piles = n_anchors = 0
        for c in floating.district(p):
            (x0, y0, z0), (x1, y1, z1) = semantic.union_bbox([c])
            if c.type == "MOORING_PILE":
                n_piles += 1
                self.assertLess(z0, seabed((y0 + y1) / 2.0) - 1.0, c.id)       # driven into the seabed
                self.assertGreater(z1, zt, c.id)                               # standing above the deck
            if c.type == "ANCHOR":
                n_anchors += 1
                self.assertLess(z0, seabed((y0 + y1) / 2.0), c.id)               # bedded in the seabed
                self.assertGreater(z1, seabed(min(y0, y1)), c.id)                # and showing above it
                self.assertIn("not sized", c.meta["note"])
        self.assertGreater(n_piles, 0)
        self.assertGreater(n_anchors, 0)

    def test_offshore_district_has_no_link_to_land(self):
        data, p = spec("floating_district_offshore_01")
        types = {c.type for c in floating.district(p)}
        self.assertTrue({"MOORING_LINE", "ANCHOR"} <= types)
        self.assertFalse(types & {"LINK_SPAN", "ACCESS_ROUTE", "MOORING_PILE"})
        self.assertEqual(data["site"], "asset_library/architecture/sites/site_open_sea_01.json")

if __name__ == "__main__":
    unittest.main()
