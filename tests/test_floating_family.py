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
            if c.type not in ("SECTION_CUT", "DISPLACED_VOLUME", "WATER", "MARKER"):   # plates and the marker sit on the cut
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


class StoryPartsTest(unittest.TestCase):
    """Parts added for the story's shots (production layer L4)."""

    def setUp(self):
        self.res = json.loads(RESULTS.read_text())

    def test_freeboard_marker_shows_the_freeboard_above_the_water(self):
        p = params(section=1)
        comps = {c.id: c for c in floating.platform(p)}
        (x0, y0, z0), (x1, y1, z1) = semantic.union_bbox([comps["freeboard_marker"]])
        self.assertAlmostEqual(z1, p["hull_depth_m"] - p["draft_m"], places=6)          # level with the deck
        self.assertGreater(z1 - z0, max(s["freeboard_m"] for s in self.res["storey_branch"]["steps"]))   # reaches below the water in every state
        self.assertLess(y1, 0.0)                                                      # on the cut face
        self.assertGreater(y0, floating.CUT_Y[1])                                     # behind the water's cut plate
        self.assertAlmostEqual(x0, p["length_m"] / 2, places=6)                       # against the hull's side

    def test_story_platform_has_the_tilt_examples_load_and_four_neighbours(self):
        data, p = spec("floating_platform_a_story_01")
        comps = floating.platform(p)
        load = next(c for c in comps if c.type == "LOAD")
        (x0, y0, z0), (x1, y1, z1) = semantic.union_bbox([load])
        self.assertAlmostEqual((x1 - x0) * (y1 - y0) * (z1 - z0) * floating.LOAD_DENSITY_T_M3, self.res["list_example"]["w_t"], delta=0.5)
        moved = (x0 + self.res["list_example"]["d_m"], x1 + self.res["list_example"]["d_m"])
        for c in comps:   # the 15 m slide runs along the street: it never meets a building
            if c.type == "BUILDING" and c.group.startswith("storey"):
                (bx0, by0, _), (bx1, by1, _) = semantic.union_bbox([c])
                self.assertFalse(moved[0] < bx1 and moved[1] > bx0 and y0 < by1 and y1 > by0, c.id)
        self.assertEqual({c.group for c in comps if c.group.startswith("neighbour")}, {f"neighbour{k}" for k in (1, 2, 3, 4)})

    def test_neighbourhood_with_both_moorings(self):
        _, p = spec("floating_neighbourhood_both_01")
        types = [c.type for c in floating.neighbourhood(p)]
        self.assertEqual((types.count("MOORING_PILE"), types.count("MOORING_LINE"), types.count("ANCHOR")), (10, 10, 10))

    def test_semi_sub_stays_above_the_seabed_beside_design_a(self):
        data, p = spec("floating_semi_sub_01")
        comps = floating.semi_sub(p)
        for c in comps:
            self.assertGreater(semantic.union_bbox([c])[0][2], -p["water_depth_m"], c.id)
        self.assertEqual(floating.COMPARE_BOX_DRAFT, self.res["design_A"]["mid"]["draft_m"])
        self.assertTrue(assets.compatibility_errors("floating", "semi_sub", dict(p, pontoon_depth_m=12.0, pontoon_height_m=6.0)))

    def test_offshore_district_has_links_to_a_distant_shore_on_the_seabed(self):
        data, p = spec("floating_district_offshore_01")
        links = [c for c in floating.district(p) if c.id.startswith("shore_link_")]
        self.assertEqual({c.meta["network"] for c in links}, {"power", "water", "wastewater"})
        for c in links:
            (x0, y0, z0), _ = semantic.union_bbox([c])
            self.assertAlmostEqual(z0, -p["depth_far_m"], places=6)   # lying on the seabed
            self.assertLess(y0, -p["shore_link_m"] + p["shore_gap_m"] + 1.0)


class UsesAndDetailTest(unittest.TestCase):
    """Owner review of the L5 excerpt: readable storeys, entrances, public buildings, and an allocation that houses the
    scenario's 10,000 people, without changing any platform's load."""

    def setUp(self):
        self.res = json.loads(RESULTS.read_text())

    def test_every_use_covers_the_same_floor_area(self):
        for use in ("home", "mixed", "school", "clinic", "community"):
            for orient in ("x", "y"):
                rects = floating.use_layout(use, 60.0, 60.0, 0.4, orient)
                area = sum((x1 - x0) * (y1 - y0) for x0, x1, y0, y1 in rects)
                self.assertAlmostEqual(area, 0.4 * 3600.0, places=6, msg=use)
                for x0, x1, y0, y1 in rects:   # on the deck, clear of the 1.2 m where walkways land
                    self.assertTrue(-28.8 <= x0 < x1 <= 28.8 and -28.8 <= y0 < y1 <= 28.8, use)

    def test_district_allocation_is_the_calculated_one(self):
        al = self.res["district_C_allocation"]
        uses = [u for _, _, u in floating.district_cells()]
        self.assertEqual(uses.count("home"), al["modules"]["home"])
        self.assertEqual(uses.count("mixed"), al["modules"]["mixed"])
        self.assertEqual(uses.count("school"), al["service_types"]["school"])
        self.assertEqual(uses.count("clinic"), al["service_types"]["clinic"])
        self.assertEqual(uses.count("community"), al["service_types"]["community_shops_offices"])
        self.assertGreaterEqual(al["residents_at_homes_m2_each"], 10000)
        self.assertTrue(floating.PARKS <= {(c, r) for c, r, u in floating.district_cells() if u == "home"})

    def test_every_platform_has_facades_and_paving(self):
        _, p = spec("floating_district_01")
        comps = floating.district(p)
        ids = {c.id for c in comps}
        for c, r, use in floating.district_cells():
            for k in ("facade", "paths"):
                self.assertIn(f"m{c:02d}{r}_{k}", ids)
            if use == "school":
                self.assertIn(f"m{c:02d}{r}_playground", ids)
        self.assertEqual(sum(c.id.endswith("_trees") for c in comps), len(floating.PARKS))

    def test_storeys_carry_their_windows(self):
        comps = {c.id: c for c in floating.platform(params(storeys=4, section=1))}
        for k in (2, 4):
            for s in (1, 2, 3, 4):
                w = comps[f"block{k}_storey{s}_windows"]
                self.assertEqual((w.type, w.group), ("DECORATION", f"storey_{s}"))

    def test_section_with_front_half_shows_the_whole_platform_before_the_cut(self):
        data, p = spec("floating_platform_a_section_01")
        comps = {c.id: c for c in floating.platform(p)}
        front = [c for c in comps.values() if c.group == "front_half"]
        self.assertTrue(any(c.type == "BUILDING" for c in front) and any(c.type == "HULL" for c in front))
        for c in front:
            self.assertLessEqual(semantic.union_bbox([c])[1][1], 1e-9, c.id)    # all of it in front of the cut
        for cid in ("front_water_west", "front_water_east", "front_water_south", "front_seabed", "draft_dim", "deck_ref",
                    "bottom_ref", "freeboard_marker", "displaced_volume"):
            self.assertIn(cid, comps)
        (x0, y0, z0), (x1, y1, z1) = semantic.union_bbox([comps["draft_dim"]])
        self.assertAlmostEqual(z1 - z0, p["draft_m"], places=6)                  # waterline to the bottom
        self.assertLess(y1, floating.CUT_Y[0])                                    # drawn in front of the water

    def test_story_platform_draws_the_load_path_and_a_level_reference(self):
        data, p = spec("floating_platform_a_story_01")
        comps = {c.id: c for c in floating.platform(p)}
        (x0, _, _), (x1, _, _) = semantic.union_bbox([comps["load_path"]])
        load = semantic.union_bbox([comps["test_load"]])
        self.assertAlmostEqual(x1, load[1][0] + self.res["list_example"]["d_m"], places=6)   # the arrow ends where the load stops
        self.assertEqual(comps["level_ref"].animation, ("STATIC",))

if __name__ == "__main__":
    unittest.main()
