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
        m8 = [c for cid, c in claims.items() if "CLM_750" <= cid < "CLM_780"]
        m81 = [c for cid, c in claims.items() if cid >= "CLM_780"]   # M8.1/M8.2: factors, decisions, conclusion
        self.assertEqual((len(m8), len(m81)), (25, 15))
        allowed = {"SRC_NCHRP_CONTEXT", "SRC_FHWA_BRIDGE_TYPES"}
        for c in m8 + m81:
            self.assertEqual(c["review_status"], "SOURCE_VERIFIED", c["id"])
            ok = allowed | ({"SRC_FHWA_PENOBSCOT"} if c in m81 else set()) \
                | ({"SRC_EWV_WHEELING"} if c["id"] == "CLM_766" else set())   # M8.2: span, not bridge length
            self.assertTrue(set(c["source_ids"]) <= ok, c["id"])
            self.assertTrue(all(e["excerpt"] and e["locator"] for e in c["evidence"]), c["id"])
        self.assertIn("weakest link", " ".join(e["excerpt"] for e in claims["CLM_780"]["evidence"]))
        # M8.2 (owner's review): the report's "133 years" is not used; the counter-example is recorded
        self.assertNotIn("133 years", " ".join(e["excerpt"] for e in claims["CLM_789"]["evidence"]))
        self.assertIn("Williamsburg Bridge", claims["CLM_789"]["assumptions"])
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



class LongSpanThroughTheFilmTest(unittest.TestCase):
    """M8.1 (owner, 2026-11-03): the chapters after the bridge types cover the long-span families too."""

    def test_factors_decisions_and_conclusion_cover_every_family(self):
        doc = read(FILM / "script/chapters.json")
        beats = {b["beat_id"]: b for b in read(FILM / "script/visual_beats.json")["beats"]}
        text = {c["id"]: " ".join(beats[b]["narration"].lower() for b in c["beat_ids"]) for c in doc["chapters"]}
        for chapter in ("C9", "C10", "C11"):   # factors (materials/ground/wind), span-cost-time, decisions
            for family in ("cantilever", "suspension", "cable-stayed"):
                self.assertIn(family, text[chapter], (chapter, family))
        self.assertIn("suspension", text["C12"])
        self.assertIn("cantilevers", text["C12"])

    def test_the_owner_runtime_decision_is_recorded(self):
        from pipeline import chapters as CH
        lo, hi, decision = CH.runtime_range(FILM)
        self.assertEqual((lo, hi), (8 * 60.0, 30 * 60.0))
        self.assertIn("Tran Nam Anh", decision["decided_by"])
        self.assertIn("truyền tải đầy đủ nội dung", decision["basis"])
        record = read(FILM / "review/OWNER_APPROVALS.json")
        self.assertIn("DEC-M8.1-CONTENT-AND-RUNTIME", [d["id"] for d in record["decisions"]])
        timing = read(FILM / "script/timing.json")
        self.assertLessEqual(timing["total_seconds"], hi)


class OwnerEditorialReviewTest(unittest.TestCase):
    """M8.2 (owner's editorial review, 2026-11-04): wording no broader, more present-tense or less
    conditional than its evidence; practical ranges kept apart from built spans; Queensboro vs the model."""

    def sentences(self):
        n = read(FILM / "script/narration.json")
        return {b["id"]: b["sentences"] for b in n["beats"]}

    def test_removed_or_narrowed_statements(self):
        s = self.sentences()
        text = " ".join(" ".join(v) for v in s.values())
        for gone in ("133 years", "200 to 300 feet", "Today, the long-span answer", "still built today",
                     "most common steel bridge today", "are becoming more common", "the features that define",
                     "longest bridge in the world", "into the ground on either side"):
            self.assertNotIn(gone, text)
        self.assertIn("2012 federal handbook found", s["B24B"][2])
        self.assertIn("main span over 1,000 feet", s["B24B"][2])
        self.assertIn("in 2012", s["B33"][2])
        self.assertTrue(s["B23E"][0].startswith("By 2012"))
        self.assertIn("in 2005 a national report", s["B09"][1])
        self.assertIn("hinges", s["B22C"][0])
        self.assertIn("superstructure could adjust", s["B22C"][1])
        self.assertIn("modern cantilevers", s["B31B"][0])
        self.assertIn("longest span in the world when it opened", s["B24B"][1])
        self.assertIn("same span", s["B51"][0])
        self.assertIn("Unlike our model, it has no suspended span", s["B44"][2])

    def test_dated_claims_say_so(self):
        claims = {c["id"]: c for c in read(FILM / "research/sources.json")["claims"]}
        for cid in ("CLM_774", "CLM_777", "CLM_788"):
            self.assertIn("2012", claims[cid]["text"], cid)
        self.assertIn("2005", claims["CLM_721"]["text"])
        self.assertIn("200 to 300", claims["CLM_757"]["assumptions"])   # recorded as not used
        self.assertNotIn("200 to 300", " ".join(e["excerpt"] for e in claims["CLM_757"]["evidence"]))
        self.assertIn("unique among cantilevers of its size", claims["CLM_794"]["evidence"][0]["excerpt"])

    def test_span_card_keeps_practical_ranges_apart_from_built_spans(self):
        beats = {b["beat_id"]: b for b in read(FILM / "script/visual_beats.json")["beats"]}
        card = beats["B23C"]["graphic"]["elements"]
        texts = [e.get("text", "") for e in card]
        self.assertIn("Practical or economic range", texts)
        self.assertIn("Spans actually built", texts)
        self.assertFalse(any("economic ranges for steel" in t or "How far each type reaches" in t for t in texts))
        bars = [e for e in card if e.get("kind") == "rect" and e.get("word") in ("girders", "simple", "arches", "cable")]
        outlined = {e["word"] for e in bars if not e.get("color")}
        solid = {e["word"] for e in bars if e.get("color")}
        self.assertEqual((outlined, solid), ({"girders", "simple"}, {"arches", "cable"}))

    def test_second_text_review_keeps_the_conditions_on_the_cards(self):
        # M8.2, owner's second text review: the card says what the narration says, with its conditions.
        beats = {b["beat_id"]: b for b in read(FILM / "script/visual_beats.json")["beats"]}
        texts = lambda bid: " ".join(e.get("text", "") for e in beats[bid]["graphic"]["elements"])   # noqa: E731
        self.assertIn("almost all new U.S. bridges with main spans over 1,000 ft were cable-stayed", texts("B24B"))
        self.assertIn("long after timber trusses stopped being competitive", texts("B33"))
        self.assertIn("timber trusses stopped being competitive", self.sentences()["B33"][1])
        self.assertIn("timber trusses stopped being competitive", self.sentences()["B09"][1])
        notes = (FILM / "review/EDITORIAL_NOTES.md").read_text(encoding="utf-8")
        current = notes.split("## Đã bỏ")[0]   # the removed statements are listed only under their own heading
        for gone in ("200 to 300", "133 years", "Today, the long-span", "19,3 phút", "muốn thêm một NOTE"):
            self.assertNotIn(gone, current)

    def test_ground_card_says_or(self):
        beats = {b["beat_id"]: b for b in read(FILM / "script/visual_beats.json")["beats"]}
        texts = [e.get("text", "") for e in beats["B22B"]["graphic"]["elements"]]
        self.assertIn("Suspension: cables anchored in massive blocks or in bedrock", texts)
        self.assertFalse(any("set into rock" in t for t in texts))

    def test_pronunciation_overrides_wait_for_the_owner(self):
        from pipeline import pronunciation as pron
        lex = pron.load(FILM)
        self.assertEqual(pron.validate(lex), [])
        entries = {e["written"]: e for e in lex["entries"]}
        self.assertEqual(set(entries), {"Corinne", "Cincinnati"})
        self.assertTrue(all(e["status"] == "PENDING_LISTENING_REVIEW" and not e["confirmed_by"] for e in entries.values()))
        review = read(FILM / "script/narration.json")["voice"]["pronunciation_review"]
        self.assertEqual(review["status"], "PENDING")
        self.assertFalse({"Promontory", "Covington", "Finley"} & set(review["terms"]))   # not spoken
        self.assertIn("not a listening session", review["owner_text_review"]["kind"])


if __name__ == "__main__":
    unittest.main()
