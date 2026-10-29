"""M5: narrative beats -> visual plan -> engine storyboard (no Blender).

Fixtures that invent narration or claims are SYNTHETIC TEST DATA (see each test)."""
import copy
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from planner import beats as B, catalog, coverage, intents, mapper, planner as pl, resolver, validate, vocabulary as V
from planner import compiler
from tools import render_cache
from tools.cli import ROOT

BRIDGE = ROOT / "projects" / "bridge-story-m5"
ROOF = ROOT / "projects" / "roof-plan-m5"
VOCAB = V.Vocabulary()
INDEX = catalog.index()


def project_copy(tmp, src=BRIDGE, edit_beats=None, edit_sources=None):
    """Temporary copy of a planning project (script, research, project.json)."""
    dst = Path(tmp) / src.name
    for sub in ("script", "research"):
        shutil.copytree(src / sub, dst / sub)
    shutil.copy(src / "project.json", dst / "project.json")
    if edit_beats:
        doc = json.loads((dst / "script/visual_beats.json").read_text())
        edit_beats(doc)
        (dst / "script/visual_beats.json").write_text(json.dumps(doc))
    if edit_sources:
        s = json.loads((dst / "research/sources.json").read_text())
        edit_sources(s)
        (dst / "research/sources.json").write_text(json.dumps(s))
    return dst


def beat(doc, bid):
    return next(b for b in doc["beats"] if b["beat_id"] == bid)


class BeatSchemaTest(unittest.TestCase):
    def test_pilot_and_fixture_beats_are_valid(self):
        for p in (BRIDGE, ROOF):
            doc = B.load(p / "script/visual_beats.json")
            sources = json.loads((p / "research/sources.json").read_text())
            self.assertEqual(B.validate(doc, sources), [], p.name)
        self.assertTrue(B.load(ROOF / "script/visual_beats.json")["synthetic_fixture"])

    def test_invalid_beats_are_reported(self):
        doc = B.load(BRIDGE / "script/visual_beats.json")
        sources = json.loads((BRIDGE / "research/sources.json").read_text())
        bad = copy.deepcopy(doc)
        bad["timing_mode"] = "GUESSED"
        beat(bad, "B2")["claim_ids"] = []
        beat(bad, "B3")["narrative_intent"] = "SHOW_EXPLOSION"           # unsupported visual intent
        beat(bad, "B4")["claim_ids"] = ["CLM_999"]
        beat(bad, "B5")["visual_goal"] = ""
        errors = " ".join(B.validate(bad, sources))
        for needle in ("timing_mode must be one of", "a fact beat must cite claim_ids",
                       "unsupported visual intent 'SHOW_EXPLOSION'", "claim CLM_999 is not in research/sources.json",
                       "visual_goal is required"):
            self.assertIn(needle, errors)

    def test_schema_files_match_the_code(self):
        from planner import camera
        beats = json.loads((ROOT / "schemas/narrative_beats.schema.json").read_text())
        item = beats["properties"]["beats"]["items"]["properties"]
        self.assertEqual(beats["properties"]["timing_mode"]["enum"], list(B.TIMING_MODES))
        self.assertEqual(item["kind"]["enum"], list(B.BEAT_KINDS))
        self.assertEqual(item["narrative_intent"]["enum"], list(intents.INTENTS))
        self.assertEqual(item["camera_mode"]["enum"], list(camera.MODES))
        self.assertEqual(item["required_accuracy"]["enum"], list(resolver.ACCURACY_RANK))
        plan_schema = json.loads((ROOT / "schemas/visual_plan.schema.json").read_text())
        self.assertEqual(plan_schema["properties"]["coverage"]["items"]["properties"]["status"]["enum"],
                         list(validate.COVERAGE_STATUSES))
        plan = json.loads((BRIDGE / "storyboard/visual_plan.json").read_text())
        self.assertTrue(set(plan_schema["required"]) <= set(plan))
        shot_props = plan_schema["properties"]["shots"]["items"]
        for ps in plan["shots"]:
            self.assertTrue(set(shot_props.get("required", [])) <= set(ps), ps["shot_id"])
            self.assertIn(ps["template"], shot_props["properties"]["template"]["enum"])

    def test_provisional_duration_is_an_estimate_from_words(self):
        cfg = json.loads((ROOT / "config/visual_planning.json").read_text())["timing"]
        b = {"narration": "one two three four five six seven eight nine ten eleven twelve thirteen", "timing": {}}
        self.assertAlmostEqual(B.provisional_seconds(b, cfg), 13 / 2.6 + 0.8)
        self.assertEqual(B.provisional_seconds({"narration": "x", "timing": {"estimated_seconds": 7}}, cfg), 7.0)


class IntentTest(unittest.TestCase):
    def test_every_intent_maps_to_known_strategies(self):
        self.assertEqual(len(intents.INTENTS), 10)   # M6 added EXPLAIN_LOAD_PATH
        for name, i in intents.INTENTS.items():
            self.assertTrue(i["strategies"], name)
            self.assertTrue(set(i["strategies"]) <= set(intents.STRATEGIES), name)

    def test_cross_check_flags_a_mismatch_but_never_overrides(self):
        self.assertIn("COMPARE_VARIANTS", intents.suggest("Side by side, the three bridges differ"))
        warn = intents.check({"narration": "Side by side, the three bridges differ", "narrative_intent": "SHOW_CONTEXT"})
        self.assertIn("declared SHOW_CONTEXT", warn)
        self.assertIsNone(intents.check({"narration": "Side by side.", "narrative_intent": "COMPARE_VARIANTS"}))


class ResolverTest(unittest.TestCase):
    def site(self):
        return resolver.resolve("river_crossing_site", VOCAB, INDEX)["entry"]

    def test_reuse_adapt_and_parameter_matching(self):
        r = resolver.resolve("timber_beam_bridge", VOCAB, INDEX, site=self.site())
        self.assertEqual((r["status"], r["asset_id"]), ("REUSE_EXISTING", "bridge_timber_beam_01"))
        self.assertEqual(resolver.resolve("warren_truss", VOCAB, INDEX, site=self.site())["asset_id"],
                         "bridge_steel_truss_warren_01")
        self.assertEqual(resolver.resolve("five_arch_stone_bridge", VOCAB, INDEX, site=self.site())["asset_id"],
                         "bridge_stone_arch_05")
        roof = resolver.resolve("steep_gable_roof", VOCAB, INDEX)
        self.assertEqual((roof["status"], roof["asset_id"]), ("ADAPT_EXISTING_ASSET", "legacy_roof_evolution_roof_B"))
        self.assertIn("adapter", roof["explanation"])

    def test_generate_new_and_blocked(self):
        vocab = copy.deepcopy(VOCAB)
        vocab.concepts["four_arch_stone_bridge"] = {"kind": "architecture", "family": "bridge", "variant": "stone_arch",
                                                    "where": {"arch_count": 4}}
        g = resolver.resolve("four_arch_stone_bridge", vocab, INDEX, site=self.site())
        self.assertEqual(g["status"], "GENERATE_FROM_SUPPORTED_FAMILY")
        self.assertEqual(g["generated_spec"]["parameters"]["arch_count"], 4)
        self.assertEqual(g["generated_spec"]["accuracy"], "ILLUSTRATIVE")
        n = resolver.resolve("suspension_bridge", VOCAB, INDEX)
        self.assertEqual(n["status"], "NEW_ASSET_REQUIRED")
        self.assertEqual(n["task"]["kind"], "NEW_FAMILY_GENERATOR")
        self.assertEqual(resolver.resolve("covered_bridge", VOCAB, INDEX)["status"], "UNKNOWN_CONCEPT")
        b = resolver.resolve("stone_arch_bridge", VOCAB, INDEX, "HISTORICALLY_VERIFIED", self.site())
        self.assertEqual(b["status"], "BLOCKED_MISSING_EVIDENCE")

    def test_catalog_is_never_modified(self):
        before = (ROOT / "asset_library/catalog/catalog.json").read_bytes()
        with tempfile.TemporaryDirectory() as tmp:
            pl.plan_project(project_copy(tmp))
        self.assertEqual(before, (ROOT / "asset_library/catalog/catalog.json").read_bytes())


class MapperTest(unittest.TestCase):
    def parts(self, path, owner):
        return catalog.component_parts({"source": "library", "path": path, "kind": "architecture"}, owner)

    def test_semantic_roles_and_groups(self):
        truss = self.parts("asset_library/architecture/bridges/bridge_steel_truss_pratt_01.json", "t")
        t = mapper.resolve_targets(["diagonal_members"], truss, VOCAB, "t")[0]
        self.assertEqual(t["roles"], ["truss_diagonal"])
        self.assertTrue(all(i.startswith("t_") and "diagonals" in i for i in t["component_ids"]))
        arch = self.parts("asset_library/architecture/bridges/bridge_stone_arch_03.json", "s")
        k = mapper.resolve_targets([{"concept": "voussoir", "group": "arch_2"}], arch, VOCAB, "s")[0]
        self.assertEqual(len(k["component_ids"]), 12)

    def test_missing_and_ambiguous_components_are_errors(self):
        timber = self.parts("asset_library/architecture/bridges/bridge_timber_beam_01.json", "w")
        with self.assertRaisesRegex(mapper.MappingError, "'keystone' .* has no component"):
            mapper.resolve_targets(["keystone"], timber, VOCAB, "w")
        with self.assertRaisesRegex(mapper.MappingError, "ambiguous"):
            mapper.resolve_targets(["beam"], timber, VOCAB, "w")
        truss = self.parts("asset_library/architecture/bridges/bridge_steel_truss_pratt_01.json", "t")
        with self.assertRaisesRegex(mapper.MappingError, "ambiguous"):
            mapper.resolve_targets(["member"], truss, VOCAB, "t")


class PilotPlanTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plan = json.loads((BRIDGE / "storyboard/visual_plan.json").read_text())

    def test_every_beat_is_covered_and_executable(self):
        self.assertTrue(self.plan["executable"])
        self.assertEqual([c["beat_id"] for c in self.plan["coverage"]], [f"B{i}" for i in range(1, 9)])
        self.assertTrue(all(c["status"] == "COVERED" for c in self.plan["coverage"]))
        self.assertTrue(60 <= self.plan["duration_seconds"] <= 90)

    def test_strategies_follow_the_narrative(self):
        s = {c["beat_id"]: c["strategy"] for c in self.plan["coverage"]}
        # M5.5: B4 voussoirs are read as pieces (frontal exploded close-up); B7 three long bridges are
        # unreadable all at once at 640x360, so one at a time under one camera; B8 is the overview.
        self.assertEqual(s, {"B1": "SITE_HOLD", "B2": "ASSEMBLE_IN", "B3": "HIGHLIGHT_THEN_EXPLODE",
                             "B4": "CLOSEUP_EXPLODE", "B5": "HOLD_HIGHLIGHT", "B6": "HIGHLIGHT_REPLACE_HIGHLIGHT",
                             "B7": "SEQUENTIAL_COMPARISON", "B8": "COMPARE_SIDE_BY_SIDE"})
        replace = [p for p in self.plan["shots"] if p["template"] == "REPLACE_PARTS"]
        self.assertEqual([p["states"] for p in replace], [["site", "timber_beam_bridge"], ["steel_truss_bridge", "warren_truss"]])
        warren = next(v for v in self.plan["states"]["variants"] if v["id"] == "warren_truss")
        self.assertEqual(warren["structure_from"], "steel_truss_bridge")

    def test_camera_groups_closeup_and_cuts(self):
        shots = self.plan["shots"]
        closeup = next(p for p in shots if p["shot"].get("camera_focus"))
        self.assertEqual((closeup["template"], closeup["camera"]["preset"]), ("EXPLODED_VIEW", "ELEVATION"))
        self.assertEqual(len(closeup["shot"]["camera_focus"]), 13)
        self.assertEqual(closeup["cut_from_previous"], "hard")
        for a, b in zip(shots, shots[1:]):
            if b["cut_from_previous"] == "match":
                self.assertEqual(a["camera"]["group"], b["camera"]["group"])
                if b["template"] == "SIDE_BY_SIDE":
                    self.assertEqual(a["states"], b["states"])
                else:
                    self.assertEqual(a["states"][-1], b["states"][0])
        first = [p for p in shots if p["camera"]["group"] == 1]
        self.assertTrue(all(p["shot"]["build_variants"] == ["site", "timber_beam_bridge"] for p in first))
        seq = [p for p in shots if p.get("sequence")]
        self.assertEqual([p["states"][0] for p in seq], ["timber_beam_bridge", "stone_arch_bridge", "steel_truss_bridge"])
        self.assertEqual(len({p["camera"]["group"] for p in seq}), 1)          # one locked camera = one scale
        self.assertEqual([p["cut_from_previous"] for p in seq[1:]], ["hard", "hard"])
        self.assertEqual(seq[0]["shot"]["build_variants"], ["timber_beam_bridge", "stone_arch_bridge", "steel_truss_bridge"])

    def test_covered_targets_are_revealed_not_hidden(self):
        """Test A: the stringers lie under the deck planks. The offline estimate detects it before
        rendering (14 % visible), camera remedies are skipped (match cut), and the planner ghosts
        the planks while the stringers glow; when the planks glow themselves nothing is ghosted."""
        by_id = {p["shot_id"]: p for p in self.plan["shots"]}
        h = by_id["SC_003"]["shot"]["animation"]["highlight"]
        self.assertEqual(h["ghost"], [f"timber_beam_bridge_span{i}_planks" for i in range(1, 5)])
        self.assertTrue(all("stringers" in c for c in h["components"]))
        self.assertNotIn("ghost", by_id["SC_004"]["shot"]["animation"]["highlight"])
        rep = by_id["SC_003"]["repairs"][0]
        self.assertEqual((rep["remedy"], rep["problems"]), ("GHOST:plank", ["OCCLUDED"]))
        self.assertLess(rep["before"]["visible_share"], 0.25)
        self.assertGreater(rep["after"]["visible_share"], 0.75)
        record = next(r for c in self.plan["coverage"] for r in c.get("visual_repairs", []) if r["shot_id"] == "SC_003")
        self.assertEqual([e["result"] for e in record["evaluated"]], ["SKIPPED", "SKIPPED", "PASS"])
        from engine import motion, templates
        story = json.loads((BRIDGE / "storyboard/storyboard.json").read_text())
        states = json.loads((BRIDGE / "storyboard/states.json").read_text())
        shot = copy.deepcopy(next(x for x in story["shots"] if x["id"] == "SC_003"))
        plan = templates.plan_shot(shot, states, 24, templates.placeholder_slots(shot, states))
        peak = plan.markers["highlight_peak"]
        self.assertAlmostEqual(plan.sample(h["ghost"][0], motion.TRANSPARENCY, peak)[0], 0.7)
        self.assertEqual(plan.sample(h["ghost"][0], motion.TRANSPARENCY, plan.frame_count)[0], 0.0)
        shot["animation"]["highlight"]["ghost"] = h["components"][:1]
        with self.assertRaisesRegex(motion.PlanError, "also glow"):
            templates.plan_shot(shot, states, 24, templates.placeholder_slots(shot, states))
        sbs = copy.deepcopy(next(x for x in story["shots"] if x["transition"] == "SIDE_BY_SIDE"))
        sbs["animation"]["highlight"]["ghost"] = h["ghost"]
        with self.assertRaisesRegex(motion.PlanError, "unknown option 'ghost'"):
            templates.plan_shot(sbs, states, 24, templates.placeholder_slots(sbs, states))

    def test_plan_validates_and_compiles(self):
        self.assertEqual(validate.validate_plan(self.plan, BRIDGE), [])
        story = compiler.storyboard(self.plan)
        self.assertEqual(len(story["shots"]), len(self.plan["shots"]))
        self.assertEqual(json.loads((BRIDGE / "storyboard/storyboard.json").read_text()), story)

    def test_planning_is_deterministic(self):
        with tempfile.TemporaryDirectory() as tmp:
            a = pl.plan_project(project_copy(tmp))
        with tempfile.TemporaryDirectory() as tmp:
            b = pl.plan_project(project_copy(tmp))
        self.assertEqual(json.dumps(a, sort_keys=True), json.dumps(b, sort_keys=True))
        self.assertEqual(json.dumps(a["shots"], sort_keys=True), json.dumps(self.plan["shots"], sort_keys=True))


class PlanValidationTest(unittest.TestCase):
    def tampered(self, fn):
        plan = json.loads((BRIDGE / "storyboard/visual_plan.json").read_text())
        fn(plan)
        return " ".join(validate.validate_plan(plan, BRIDGE, engine_check=False))

    def test_tampering_is_caught(self):
        def bad_target(p):
            p["shots"][2]["semantic_targets"][0]["component_ids"].append("timber_beam_bridge_no_such_part")
        self.assertIn("is not visible", self.tampered(bad_target))

        def wrong_role(p):
            t = p["shots"][2]["semantic_targets"][0]
            t["component_ids"] = ["timber_beam_bridge_bent1_cap"]
        self.assertIn("has role cap_beam", self.tampered(wrong_role))

        def gap(p):
            p["shots"][3]["timing"]["start_seconds"] += 1.0
        self.assertIn("not contiguous", self.tampered(gap))

        def reorder(p):
            p["shots"][0], p["shots"][2] = p["shots"][2], p["shots"][0]
        self.assertIn("narration order", self.tampered(reorder))

        def bad_replace(p):
            rp = next(s for s in p["shots"] if s["template"] == "REPLACE_PARTS" and s["states"][0] != "site")
            rp["states"] = ["timber_beam_bridge", "stone_arch_bridge"]
        self.assertIn("share no frame", self.tampered(bad_replace))

        def jump(p):
            p["shots"][5]["cut_from_previous"] = "match"     # SC_006 (stone) after SC_005 (timber)
        self.assertIn("match cut across continuity groups", self.tampered(jump))

        def state_jump(p):
            p["shots"][3]["states"] = ["stone_arch_bridge"]
        self.assertIn("match cut from", self.tampered(state_jump))

        def drop_beat(p):
            p["coverage"].pop(3)
        self.assertIn("every beat once", self.tampered(drop_beat))


class NegativePlanningTest(unittest.TestCase):
    """SYNTHETIC beats injected into copies of the pilot."""

    def plan_with(self, edit, edit_sources=None):
        with tempfile.TemporaryDirectory() as tmp:
            return pl.plan_project(project_copy(tmp, edit_beats=edit, edit_sources=edit_sources))

    def cov(self, plan, bid):
        return next(c for c in plan["coverage"] if c["beat_id"] == bid)

    def test_nonexistent_asset(self):
        plan = self.plan_with(lambda d: beat(d, "B5")["required_concepts"].__setitem__(0, "suspension_bridge"))
        c = self.cov(plan, "B5")
        self.assertEqual(c["status"], "MISSING_ASSET")
        self.assertFalse(plan["executable"])
        self.assertFalse([s for s in plan["shots"] if s["beat_id"] == "B5"])
        self.assertTrue(any("NEW_FAMILY_GENERATOR" in i for i in c["issues"]))
        plan = self.plan_with(lambda d: beat(d, "B5")["required_concepts"].__setitem__(0, "covered_bridge"))
        self.assertIn("not in config/visual_vocabulary.json", " ".join(self.cov(plan, "B5")["issues"]))

    def test_nonexistent_semantic_component(self):
        plan = self.plan_with(lambda d: beat(d, "B2")["required_concepts"].append("keystone"))
        c = self.cov(plan, "B2")
        self.assertEqual(c["status"], "INVALID_REQUEST")
        self.assertIn("'keystone'", " ".join(c["issues"]))

    def test_incompatible_replace_request(self):
        def edit(d):
            b = beat(d, "B6")
            b.update(preferred_states=["timber_beam_bridge", "stone_arch_bridge"], strategy="REPLACE", required_concepts=[])
        c = self.cov(self.plan_with(edit), "B6")
        self.assertEqual(c["status"], "INVALID_REQUEST")
        self.assertIn("share no frame", " ".join(c["issues"]))

    def test_cause_effect_without_a_diagram_is_a_missing_capability(self):
        def edit(d):
            beat(d, "B5")["narrative_intent"] = "EXPLAIN_CAUSE_EFFECT"
        c = self.cov(self.plan_with(edit), "B5")
        self.assertEqual(c["status"], "MISSING_TEMPLATE")
        self.assertIn("FORCE_DIAGRAM", " ".join(c["explanation"]))

    def test_insufficient_timing(self):
        plan = self.plan_with(lambda d: beat(d, "B3").__setitem__("timing", {"estimated_seconds": 1.5}))
        c = self.cov(plan, "B3")
        self.assertEqual(c["status"], "TIMING_CONFLICT")
        self.assertIn("nothing was truncated", " ".join(c["issues"]))
        self.assertFalse([s for s in plan["shots"] if s["beat_id"] == "B3"])

    def test_simpler_strategy_when_time_is_short(self):
        plan = self.plan_with(lambda d: beat(d, "B3").__setitem__("timing", {"estimated_seconds": 5.6}))
        c = self.cov(plan, "B3")
        self.assertEqual((c["status"], c["strategy"]), ("COVERED", "EXPLODE"))
        self.assertTrue(any("HIGHLIGHT_THEN_EXPLODE rejected (TIMING_CONFLICT)" in e for e in c["explanation"]))

    def test_generated_asset_is_planned_validated_and_compiled(self):
        """SYNTHETIC concept (four-arch bridge, not in the vocabulary): the supported stone_arch generator
        makes a project-local spec; the catalog is untouched and the plan validates against the engine."""
        vocab = copy.deepcopy(VOCAB)
        vocab.concepts["four_arch_stone_bridge"] = {"kind": "architecture", "family": "bridge", "variant": "stone_arch",
                                                    "label": "Four-arch stone bridge", "where": {"arch_count": 4}}
        before = (ROOT / "asset_library/catalog/catalog.json").read_bytes()
        with tempfile.TemporaryDirectory() as tmp:
            p = project_copy(tmp, edit_beats=lambda d: beat(d, "B4")["required_concepts"].__setitem__(0, "four_arch_stone_bridge"))
            plan = pl.plan_project(p, vocab=vocab)
            c = self.cov(plan, "B4")
            self.assertEqual((c["status"], c["assets"][0]["status"]), ("COVERED", "GENERATE_FROM_SUPPORTED_FAMILY"))
            gen = list((p / "planning/generated_assets").glob("*.json"))
            self.assertEqual(len(gen), 1)
            self.assertEqual(json.loads(gen[0].read_text())["parameters"]["arch_count"], 4)
            self.assertEqual(validate.validate_plan(plan, p), [])
        self.assertEqual(before, (ROOT / "asset_library/catalog/catalog.json").read_bytes())

    def test_claim_without_evidence_blocks_the_beat(self):
        def sources(s):
            next(c for c in s["claims"] if c["id"] == "CLM_102")["review_status"] = "PROVISIONAL"
        plan = self.plan_with(None, sources)
        c = self.cov(plan, "B4")
        self.assertEqual(c["status"], "EVIDENCE_BLOCKED")
        self.assertFalse([s for s in plan["shots"] if s["beat_id"] == "B4"])

    def test_evolution_needs_approved_chronology(self):
        def edit(d):
            beat(d, "B7")["narrative_intent"] = "SHOW_EVOLUTION"
        c = self.cov(self.plan_with(edit), "B7")
        self.assertEqual(c["status"], "EVIDENCE_BLOCKED")

    def test_changing_the_narrative_changes_the_visuals(self):
        def edit(d):
            beat(d, "B5").update(narrative_intent="SHOW_COMPONENT", required_concepts=["steel_truss_bridge", "truss_web"],
                                 focus_concepts=["diagonal_members"])
        plan = self.plan_with(edit)
        shots = [s for s in plan["shots"] if s["beat_id"] == "B5"]
        self.assertEqual([s["camera"]["mode"] for s in shots], ["FULL_OBJECT", "COMPONENT_CLOSEUP"])
        self.assertTrue(all("diagonals" in i for i in shots[1]["shot"]["camera_focus"]))


class RoofGeneralizationTest(unittest.TestCase):
    def test_roof_fixture_plans_with_the_same_planner(self):
        plan = json.loads((ROOF / "storyboard/visual_plan.json").read_text())
        self.assertTrue(plan["executable"])
        self.assertEqual({r["status"] for r in plan["resolutions"]}, {"ADAPT_EXISTING_ASSET"})
        self.assertEqual([p["template"] for p in plan["shots"]], ["HOLD", "EXPLODED_VIEW", "REPLACE_PARTS", "SIDE_BY_SIDE"])
        self.assertEqual(plan["shots"][-1]["shot"]["animation"]["layout"], "ROW")
        self.assertEqual(plan["shots"][0]["camera"]["preset"], "LOCKED_THREE_QUARTER")
        self.assertEqual(validate.validate_plan(plan, ROOF), [])
        exploded = plan["shots"][1]["shot"]["animation"]["components"]
        self.assertFalse([c for c in exploded if c.endswith(("_gable_front", "_gable_back"))])   # M2 rule: gable walls stay


class CacheDependencyTest(unittest.TestCase):
    """Compiled shots' render dependencies across narrative / citation / visual / geometry edits."""

    def compiled(self, tmp, edit_beats=None, edit_sources=None, asset_override=None):
        p = project_copy(tmp, edit_beats=edit_beats, edit_sources=edit_sources)
        plan = pl.plan_project(p)
        if asset_override:
            for v in plan["states"]["variants"]:
                if v.get("asset", "").endswith(asset_override[0]):
                    v["asset"] = asset_override[1]
        compiler.compile_plan(plan, p)
        story = json.loads((p / "storyboard/storyboard.json").read_text())
        return {s["id"]: render_cache.cache_key(render_cache.components(p, s, "preview")) for s in story["shots"]}

    def test_citations_and_descriptions_do_not_invalidate_renders(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = self.compiled(tmp)
        with tempfile.TemporaryDirectory() as tmp:
            cited = self.compiled(tmp, edit_sources=lambda s: next(c for c in s["claims"] if c["id"] == "CLM_101").update(
                text="Edited citation wording", caveat="edited"))
        with tempfile.TemporaryDirectory() as tmp:
            described = self.compiled(tmp, edit_beats=lambda d: beat(d, "B3").update(visual_goal="Reworded goal"))
        self.assertEqual(base, cited)
        self.assertEqual(base, described)

    def test_semantic_target_change_invalidates_only_that_shot(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = self.compiled(tmp)
        with tempfile.TemporaryDirectory() as tmp:
            changed = self.compiled(tmp, edit_beats=lambda d: beat(d, "B5")["required_concepts"].__setitem__(1, "diagonal_members"))
        self.assertEqual(sorted(k for k in base if base[k] != changed[k]), ["SC_008"])

    def test_asset_geometry_change_invalidates_only_dependent_shots(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = self.compiled(tmp)
            asset = json.loads((ROOT / "asset_library/architecture/bridges/bridge_stone_arch_03.json").read_text())
            asset["parameters"]["voussoirs_per_arch"] = 11
            alt = Path(tmp) / "stone_alt.json"
            alt.write_text(json.dumps(asset))
        with tempfile.TemporaryDirectory() as tmp2:
            alt2 = Path(tmp2) / "stone_alt.json"
            alt2.write_text(json.dumps(asset))
            changed = self.compiled(tmp2, asset_override=("bridge_stone_arch_03.json", str(alt2)))
        stale = sorted(k for k in base if base[k] != changed[k])
        plan = json.loads((BRIDGE / "storyboard/visual_plan.json").read_text())
        expected = sorted(p["shot_id"] for p in plan["shots"] if "stone_arch_bridge" in
                          (p["shot"].get("build_variants") or p["states"]))
        self.assertEqual(stale, expected)
        self.assertIn("SC_001", base)
        self.assertNotIn("SC_001", stale)     # site/timber shots untouched


class CoverageReportTest(unittest.TestCase):
    def test_report_lists_every_beat(self):
        plan = json.loads((BRIDGE / "storyboard/visual_plan.json").read_text())
        with tempfile.TemporaryDirectory() as tmp:
            path = coverage.write(plan, tmp)
            text = path.read_text()
        for b in range(1, 9):
            self.assertIn(f"| B{b} |", text)
        self.assertIn("PROVISIONAL", text)


class AudioLockedTimingTest(unittest.TestCase):
    """SYNTHETIC timing fixture: measured-looking durations, not approved narration."""

    def test_audio_locked_windows_come_from_the_timing_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = project_copy(tmp, edit_beats=lambda d: d.update(timing_mode="AUDIO_LOCKED"))
            timing = {"locked": True, "pacing": {"beat_lead_in_seconds": 0.3, "beat_tail_seconds": 0.5},
                      "beats": [{"id": f"B{i}", "duration": 8.0 + i} for i in range(1, 9)]}
            (p / "script/timing.json").write_text(json.dumps(timing))
            plan = pl.plan_project(p)
            self.assertEqual(plan["timing_mode"], "AUDIO_LOCKED")
            c = plan["coverage"][0]
            self.assertAlmostEqual(c["expected_seconds"], 0.3 + 9.0 + 0.5)
            self.assertTrue(all(s["timing"]["mode"] == "AUDIO_LOCKED" for s in plan["shots"]))
            timing["locked"] = False
            (p / "script/timing.json").write_text(json.dumps(timing))
            with self.assertRaisesRegex(Exception, "not locked"):
                pl.plan_project(p)


if __name__ == "__main__":
    unittest.main()
