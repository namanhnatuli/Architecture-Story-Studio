"""M8: the long-span families (cantilever truss, suspension, cable-stayed) - generators, geometry
checks, sources for every structural claim the models rest on, the wider site and the planner's
per-concept scene contexts (offline; no Blender, no TTS)."""
import copy
import json
import math
import unittest

from engine import spec
from engine.arch import assets, checks, semantic
from engine.arch.families import bridge
from planner import composition, resolver, vocabulary as V, catalog
from tools.cli import ROOT

LIB = ROOT / "asset_library" / "architecture"
FILM = ROOT / "projects" / "why-bridges-look-different"
LONG_SPAN = {"bridge_cantilever_truss_01": "cantilever", "bridge_suspension_01": "suspension",
             "bridge_cable_stayed_01": "cable_stayed"}


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def spec_of(name):
    return read(LIB / "bridges" / f"{name}.json")


def params_of(data):
    return assets.resolve_params(data["family"], data["variant"], data["parameters"])[0]


class GeneratorTest(unittest.TestCase):
    def test_every_long_span_asset_passes_the_offline_checks_on_the_wide_site(self):
        for name, variant in LONG_SPAN.items():
            data = spec_of(name)
            self.assertEqual(data["variant"], variant)
            comps = assets.plan(data)
            failed = [(c, d) for c, ok, d in checks.check_asset(data, comps, params_of(data)) if not ok]
            self.assertEqual(failed, [], name)
            self.assertEqual(assets.site_for(LIB / "bridges" / f"{name}.json"),
                             "asset_library/architecture/sites/site_river_crossing_72.json")
        self.assertEqual(assets.site_for(LIB / "bridges/bridge_timber_beam_01.json"),
                         "asset_library/architecture/sites/site_river_crossing_24.json")

    def test_cantilever_parts_and_profile(self):
        data = spec_of("bridge_cantilever_truss_01")
        p, comps = params_of(data), assets.plan(data)
        lay = bridge.cantilever_layout(p)
        kinds = {c.type for c in comps}
        self.assertTrue({"ANCHOR_ARM", "CANTILEVER_ARM", "SUSPENDED_SPAN"} <= kinds)
        # deepest over the main piers (NCHRP 3.7: arms project from the piers and carry a suspended span)
        self.assertGreater(lay["h_pier"], max(lay["h_end"], lay["h_tip"]))
        span = [c for c in comps if c.type == "SUSPENDED_SPAN"]
        lo, hi = semantic.union_bbox(span)
        self.assertAlmostEqual(hi[0] - lo[0], lay["suspended_m"], delta=0.3)
        for arm in (c for c in comps if c.type == "CANTILEVER_ARM"):   # from the main pier out to the tip
            ends = sorted((abs(arm.meta["from_x"]), abs(arm.meta["to_x"])))
            self.assertAlmostEqual(ends[0], lay["tip_x"], delta=0.1)
            self.assertAlmostEqual(ends[1], lay["pier_x"], delta=0.01)

    def test_suspension_cables_saddles_hangers_and_anchorages(self):
        data = spec_of("bridge_suspension_01")
        p, comps = params_of(data), assets.plan(data)
        lay = bridge.suspension_layout(p)
        by = {}
        for c in comps:
            by.setdefault(c.type, []).append(c)
        self.assertEqual(len(by["MAIN_CABLE"]), 2)
        self.assertEqual(len(by["ANCHORAGE"]), 2)
        # the cable sags between the towers and rises to the saddles; its lowest point is above the deck
        self.assertAlmostEqual(lay["cable_z"](0.0), lay["low"], places=6)
        self.assertAlmostEqual(lay["cable_z"](p["main_span_m"] / 2.0), lay["saddle"], places=6)
        self.assertGreater(lay["low"], p["deck_level_m"] + 0.8)
        # anchorages lie on the banks, beyond the gap; everything else spans it
        for a in by["ANCHORAGE"]:
            lo, hi = semantic.bbox(a)
            self.assertGreaterEqual(min(abs(lo[0]), abs(hi[0])), p["total_length_m"] / 2.0 - 1e-6)
        # vertical hangers, none at the towers
        self.assertTrue(all(abs(abs(x) - p["main_span_m"] / 2.0) > 1.0 for x in lay["hangers"]))

    def test_cable_stayed_towers_are_taller_and_stays_not_flatter_than_22_degrees(self):
        cs, su = spec_of("bridge_cable_stayed_01"), spec_of("bridge_suspension_01")
        lay = bridge.cable_stayed_layout(params_of(cs))
        self.assertGreaterEqual(lay["flattest_deg"], 22.0)   # FHWA-IF-12-052 vol. 5, 2.5 (CLM_771)
        # FHWA 2.6: suspension towers are significantly shorter than cable-stayed towers (CLM_763)
        self.assertGreater(params_of(cs)["pylon_height_m"], params_of(su)["tower_height_m"])
        comps = assets.plan(cs)
        n = params_of(cs)["stays_per_side"]
        self.assertEqual(sum(c.type == "STAY_CABLE" for c in comps), 4 * n)
        self.assertFalse(any(c.type == "ANCHORAGE" for c in comps))   # the stays end at the deck
        layers = sorted({c.layer for c in comps if c.type == "DECK"})
        self.assertEqual(layers, list(range(2, 4 + n)))   # segments outward from each pylon, then the closure

    def test_geometry_checks_reject_bad_long_span_parameters(self):
        cases = [("bridge_cable_stayed_01", {"pylon_height_m": 6.0}, "flattest stay"),
                 ("bridge_suspension_01", {"sag_ratio": 0.16, "tower_height_m": 6.0}, "dips to"),
                 ("bridge_cantilever_truss_01", {"depth_over_piers_m": 3.0}, "deepest over the main piers"),
                 ("bridge_cantilever_truss_01", {"cantilever_arm_m": 21.0}, "suspended span")]
        for name, change, needle in cases:
            data = spec_of(name)
            bad = dict(copy.deepcopy(data), parameters=dict(data["parameters"], **change))
            self.assertIn(needle, " ".join(assets.validate(bad)), (name, change))

    def test_exploded_views_keep_clear_of_the_supports(self):
        # Blender QA once found decks driven into piers and struts; the presets now avoid it
        for name in LONG_SPAN:
            data = spec_of(name)
            comps = assets.plan(data)
            off = assets.explode_offsets(data, comps)
            self.assertTrue(off, name)
            for c in comps:
                if c.type in ("PIER", "ABUTMENT", "TOWER", "PYLON", "ANCHORAGE", "BEARING"):
                    self.assertNotIn(c.id, off, (name, c.id))
            if data["variant"] == "cantilever":
                self.assertFalse(any(c.type in ("DECK", "FLOOR_BEAM") and c.id in off for c in comps))
                self.assertGreater(off[next(c.id for c in comps if c.type == "SUSPENDED_SPAN")][2],
                                   off[next(c.id for c in comps if c.type == "CANTILEVER_ARM")][2])
            if data["variant"] == "cable_stayed":
                blocks = [c for c in comps if c.type == "DECK" and c.meta.get("segment") == 0]
                self.assertEqual(len(blocks), 2)
                self.assertTrue(all(c.id not in off for c in blocks))   # built outward from these


class ResolutionAndContextTest(unittest.TestCase):
    def setUp(self):
        self.vocab = V.Vocabulary()
        self.index = catalog.index(ROOT)

    def test_sites_and_long_span_concepts_resolve_to_their_own_assets(self):
        narrow = resolver.resolve("river_crossing_site", self.vocab, self.index)
        wide = resolver.resolve("wide_river_crossing_site", self.vocab, self.index)
        self.assertEqual((narrow["asset_id"], wide["asset_id"]), ("site_river_crossing_24", "site_river_crossing_72"))
        for concept, asset in (("cantilever_bridge", "bridge_cantilever_truss_01"), ("suspension_bridge", "bridge_suspension_01"),
                               ("cable_stayed_bridge", "bridge_cable_stayed_01")):
            r = resolver.resolve(concept, self.vocab, self.index, site=wide["entry"])
            self.assertEqual((r["status"], r["asset_id"]), ("REUSE_EXISTING", asset), concept)
            # on the 24 m site no long-span asset fits: a span is never silently squeezed
            n = resolver.resolve(concept, self.vocab, self.index, site=narrow["entry"])
            self.assertNotEqual(n.get("asset_id"), asset)
        self.assertEqual(resolver.resolve("bascule_bridge", self.vocab, self.index)["status"], "NEW_ASSET_REQUIRED")

    def test_the_film_has_a_long_span_scene_context_on_the_wide_site(self):
        states = read(FILM / "storyboard/states.json")
        self.assertEqual(states["schema_version"], 3)
        self.assertEqual(states["contexts"]["long_span"]["base"]["asset"],
                         "asset_library/architecture/sites/site_river_crossing_72.json")
        self.assertEqual(states["contexts"]["bridge"]["base"]["asset"],
                         "asset_library/architecture/sites/site_river_crossing_24.json")
        ctx = {v["id"]: v.get("context") for v in states["variants"]}
        for sid in ("cantilever_bridge", "suspension_bridge", "cable_stayed_bridge", "site_long_span"):
            self.assertEqual(ctx[sid], "long_span", sid)
        for sid in ("site", "timber_beam_bridge", "stone_arch_bridge", "steel_truss_bridge"):
            self.assertEqual(ctx[sid], "bridge", sid)
        story = read(FILM / "storyboard/storyboard.json")
        for shot in story["shots"]:
            if shot.get("visual_type") == "MOTION_GRAPHICS":
                continue
            view = spec.shot_states(states, shot)
            ids = {v["id"] for v in view["variants"]}
            self.assertIn(shot["from_state"], ids, shot["id"])
            self.assertIn(shot["to_state"], ids, shot["id"])
        assemble = next(s for s in story["shots"] if s["transition"] == "REPLACE_PARTS"
                        and s["to_state"] == "cantilever_bridge")
        self.assertEqual((assemble["from_state"], assemble["scene_context"]), ("site_long_span", "long_span"))

    def test_candidate_shots_carry_their_scene_context(self):
        states = read(FILM / "storyboard/states.json")
        shot = composition.in_context(composition.comparison_shot(["suspension_bridge", "cable_stayed_bridge"], "STACK",
                                                                  0.3, 0.1, "BRIDGE_STACK"), states)
        self.assertEqual(shot["scene_context"], "long_span")
        single = composition.in_context(composition.single_shot("timber_beam_bridge", [], "BRIDGE_THREE_QUARTER", 0.1), states)
        self.assertEqual(single["scene_context"], "bridge")


class LongSpanEvidenceTest(unittest.TestCase):
    def test_new_claims_quote_the_report_and_the_federal_handbook(self):
        src = read(FILM / "research/sources.json")
        sources = {s["id"]: s for s in src["sources"]}
        fhwa = sources["SRC_FHWA_BRIDGE_TYPES"]
        self.assertIn("FHWA-IF-12-052", fhwa["title"])
        self.assertTrue(fhwa["archived_url"].startswith("https://web.archive.org/"))
        claims = {c["id"]: c for c in src["claims"]}
        new = [c for cid, c in claims.items() if cid >= "CLM_750"]
        self.assertEqual(len(new), 25)
        for c in new:
            self.assertEqual(c["review_status"], "SOURCE_VERIFIED", c["id"])
            self.assertTrue(set(c["source_ids"]) <= {"SRC_NCHRP_CONTEXT", "SRC_FHWA_BRIDGE_TYPES"}, c["id"])
            self.assertTrue(all(e["excerpt"] and e["locator"] for e in c["evidence"]), c["id"])
        self.assertIn("in tension, passing over towers that are in compression", claims["CLM_760"]["evidence"][0]["excerpt"])
        self.assertIn("22 degrees", " ".join(e["excerpt"] for e in claims["CLM_771"]["evidence"]))

    def test_force_graphics_on_the_new_models_cite_narrated_claims(self):
        beats = read(FILM / "script/visual_beats.json")["beats"]
        forces = [(b, a) for b in beats for a in b.get("annotations", []) if a.get("force")]
        new = [(b, a) for b, a in forces if b["beat_id"] in ("B46", "B52")]
        self.assertEqual({a["force"] for _, a in new}, {"TENSION", "COMPRESSION"})
        for b, a in new:
            self.assertIn(a["claim_id"], b["claim_ids"], a["id"])
        # stays are never marked as in tension: no quoted source says it (only the deck compression)
        self.assertFalse(any(a.get("force") == "TENSION" and "stay" in json.dumps(a.get("target")) for _, a in forces))


if __name__ == "__main__":
    unittest.main()
