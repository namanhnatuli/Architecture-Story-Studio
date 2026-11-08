"""M5.5 (no Blender): visibility estimate, repairs, adaptive composition, production profiles,
silent media gates, planning evaluation, cache dependencies.

Edited beats/narration in temporary copies are SYNTHETIC test inputs."""
import copy
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from planner import camera as CAM, composition, evaluate, planner as pl, repair, validate, visibility as VIS
from tools import render_cache
from tools.cli import ROOT

LEGACY = ROOT / "tests" / "fixtures" / "legacy_projects"   # archived pilots kept as regression fixtures (M7)

BRIDGE = LEGACY / "bridge-story-m5"
ROOF = LEGACY / "roof-plan-m5"
SUFFOLK = LEGACY / "suffolk-roofs"
CFG = json.loads((ROOT / "config/visual_planning.json").read_text())
VCFG, CCFG = CFG["visibility"], CFG["composition"]
PRESETS = CAM.style_presets()


def plan_of(p):
    return json.loads((p / "storyboard/visual_plan.json").read_text())


def shot(plan, sid):
    return next(s for s in plan["shots"] if s["shot_id"] == sid)


def copy_planning(tmp, src=BRIDGE, edit=None):
    dst = Path(tmp) / src.name
    for sub in ("script", "research"):
        shutil.copytree(src / sub, dst / sub)
    shutil.copy(src / "project.json", dst / "project.json")
    if edit:
        f = dst / "script/visual_beats.json"
        doc = json.loads(f.read_text())
        edit(doc)
        f.write_text(json.dumps(doc))
    return dst


def at(scene, label, targets, ghost=()):
    rows = VIS.measure(scene, VIS.evaluation_frames(scene)[label], targets, VCFG, ghost_extra=set(ghost))
    return {r["concept"]: r for r in rows}


class VisibilityEstimateTest(unittest.TestCase):
    """Level 1: the offline raster sees what the engine will render."""

    @classmethod
    def setUpClass(cls):
        cls.plan = plan_of(BRIDGE)
        cls.states = cls.plan["states"]

    def scene(self, sid, mutate=None):
        s = copy.deepcopy(shot(self.plan, sid)["shot"])
        if mutate:
            mutate(s)
        return VIS.build_scene(s, self.states, 24, PRESETS)

    def test_hidden_beam_is_detected_before_rendering(self):
        sc3 = shot(self.plan, "SC_003")
        sc = self.scene("SC_003", lambda s: s["animation"]["highlight"].pop("ghost"))
        row = at(sc, "highlight_peak", sc3["semantic_targets"])["stringer"]
        self.assertLess(row["visible_share"], 0.2)       # 14 %: three of four stringers under the planks
        self.assertEqual(row["core_area"], 0.0)          # what shows is a sliver
        self.assertIn("timber_beam_bridge_span4_planks", [o["id"] for o in row["occluders"]])
        self.assertEqual(VIS.verdict(row, VCFG)[2], ["OCCLUDED"])
        ghosted = at(sc, "highlight_peak", sc3["semantic_targets"],
                     ghost=[f"timber_beam_bridge_span{i}_planks" for i in range(1, 5)])["stringer"]
        self.assertGreater(ghosted["visible_share"], 0.75)
        self.assertTrue(VIS.verdict(ghosted, VCFG)[0])

    def test_compact_front_face_reads_although_the_block_is_deep(self):
        tg = [{"concept": "keystone", "component_ids": ["stone_arch_bridge_arch2_keystone"]}]
        arch2 = shot(self.plan, "SC_007")["shot"]["camera_focus"]     # the M5 glowing close-up of arch 2
        sc = self.scene("SC_006", lambda s: s.update(camera_focus=arch2, camera_safe_band=0.1))
        row = at(sc, "highlight_peak", tg)["keystone"]
        self.assertLess(row["visible_share"], 0.25)       # the depth of the stone is hidden
        self.assertGreater(row["core_area"], VCFG["min_core_area"])   # but its front face is a block
        self.assertTrue(VIS.verdict(row, VCFG)[0])

    def test_frames_cover_the_animation_not_just_the_middle(self):
        sc = self.scene("SC_005")
        frames = VIS.evaluation_frames(sc)
        self.assertTrue({"start", "q25", "mid", "q75", "end", "exploded_hold", "explode_end", "return_start"} <= set(frames))
        rows = {lab: at(sc, lab, shot(self.plan, "SC_005")["semantic_targets"])["stringer"] for lab in ("start", "exploded_hold")}
        self.assertLess(rows["start"]["visible_share"], 0.2)          # assembled: under the deck
        self.assertGreater(rows["exploded_hold"]["visible_share"], 0.45)   # separated by the explode

    def test_uncertainty_is_reported_not_hidden(self):
        tiny = [{"concept": "handle", "component_ids": ["timber_beam_bridge_bent1_cap"]}]
        row = at(self.scene("SC_003"), "highlight_peak", tiny)["handle"]
        ok, verification, _ = VIS.verdict(dict(row, samples=5), VCFG)
        self.assertEqual(verification, "UNCERTAIN")                    # too few samples to trust
        roof = plan_of(ROOF)
        sc = VIS.build_scene(roof["shots"][1]["shot"], roof["states"], 24, PRESETS)
        r = at(sc, "exploded_hold", roof["shots"][1]["semantic_targets"])["rafters"]
        self.assertEqual(r["geometry"], "PROXY")                       # legacy roof: approximate boxes
        near = dict(r, visible_share=VCFG["min_visible_share"] + 0.01)
        self.assertEqual(VIS.verdict(near, VCFG)[1], "UNCERTAIN")       # proxy near the threshold

    def test_subtitle_band_and_clipping_are_problems(self):
        row = {"shown": True, "samples": 400, "visible_share": 0.9, "core_area": 0.01, "visible_area": 0.02,
               "outside_share": 0.3, "safe_band_share": 0.6, "geometry": "MESH"}
        self.assertEqual(sorted(VIS.verdict(row, VCFG)[2]), ["CLIPPED", "SUBTITLE_SAFE_AREA"])

    def test_poor_framing_is_caught(self):
        """Negative: a close-up framed on the wrong part leaves the target out of frame."""
        sc3 = shot(self.plan, "SC_003")
        sc = self.scene("SC_003", lambda s: s.update(camera_focus=["timber_beam_bridge_bent1_cap"]))
        row = at(sc, "highlight_peak", sc3["semantic_targets"])["stringer"]
        self.assertIn("CLIPPED", VIS.verdict(row, VCFG)[2])

    def test_pieces_must_read_one_by_one_in_an_exploded_close_up(self):
        sc7 = shot(self.plan, "SC_007")
        rows = sc7["visibility"]["targets"]
        vous = next(r for r in rows if r["concept"] == "voussoir")
        self.assertEqual(len(vous["components"]), 12)
        self.assertTrue(all(c["visible_share"] >= 0.5 or c["core_area"] >= VCFG["min_piece_core"]
                            for c in vous["components"].values()))
        moved_into_wall = copy.deepcopy(sc7["shot"])     # the plain preset spread pushes stones into the spandrel
        for i, v in moved_into_wall["animation"]["per_component"].items():
            v["direction"] = [v["direction"][0], 0.0, abs(v["direction"][2]) or 1.0]
            v["distance"] = 0.7
        sc = VIS.build_scene(moved_into_wall, self.states, 24, PRESETS)
        bad = at(sc, "exploded_hold", sc7["semantic_targets"])["voussoir"]
        self.assertIn("PIECES_HIDDEN", VIS.verdict(bad, VCFG, pieces=True)[2])


class RepairTest(unittest.TestCase):
    def test_planner_repairs_the_hidden_beam_in_the_plan(self):
        plan = plan_of(BRIDGE)
        rec = next(r for c in plan["coverage"] for r in c.get("visual_repairs", []) if r["shot_id"] == "SC_003")
        self.assertEqual(rec["chosen"], "GHOST:plank")
        self.assertEqual([(e["remedy"], e["result"]) for e in rec["evaluated"]],
                         [("REFRAME", "SKIPPED"), ("ALT_CAMERA:ELEVATION", "SKIPPED"), ("GHOST:plank", "PASS")])
        self.assertIn("match cut", rec["evaluated"][0]["detail"])
        self.assertEqual(plan["visibility_summary"]["manual_review"], 0)

    def test_small_target_is_reframed_with_every_moving_part(self):
        roof = plan_of(ROOF)
        ps = roof["shots"][1]
        self.assertEqual([r["remedy"] for r in ps["repairs"]], ["REFRAME"])
        self.assertEqual(set(ps["shot"]["camera_focus"]),
                         set(ps["shot"]["animation"]["components"]) | {i for t in ps["semantic_targets"] for i in t["component_ids"]})

    def test_unresolvable_occlusion_falls_back_and_is_flagged(self):
        """SYNTHETIC: cap beams as the only target of a held, assembled timber bridge (no exploded view
        allowed): camera remedies break the match cut, ghosting is the only way out."""
        def edit(d):
            b = next(b for b in d["beats"] if b["beat_id"] == "B2")
            b.update(required_concepts=["timber_beam_bridge", "cap_beam"], strategy="HOLD_HIGHLIGHT")
        with tempfile.TemporaryDirectory() as tmp:
            plan = pl.plan_project(copy_planning(tmp, edit=edit))
        cov = next(c for c in plan["coverage"] if c["beat_id"] == "B2")
        # The author forced the strategy, so there is no fallback; ghosting two role groups (planks,
        # railing) does not reveal cap beams under the stringers: reported for manual review, not hidden.
        self.assertEqual((cov["status"], cov["strategy"]), ("PARTIALLY_COVERED", "HOLD_HIGHLIGHT"))
        self.assertTrue(any(i.startswith("VISIBILITY_UNRESOLVED: cap_beam OCCLUDED") for i in cov["issues"]))
        rec = cov["visual_repairs"][0]
        self.assertIsNone(rec["chosen"])
        self.assertEqual([e["result"] for e in rec["evaluated"]], ["SKIPPED", "SKIPPED", "FAIL", "FAIL"])
        self.assertTrue(plan["executable"])   # a readability problem is a review flag, not a planning failure
        self.assertEqual(plan["visibility_summary"]["manual_review"], 1)

    def test_tampered_visibility_is_caught(self):
        plan = plan_of(BRIDGE)
        sc3 = shot(plan, "SC_003")
        sc3["shot"]["animation"]["highlight"].pop("ghost")       # drop the repair, keep the stale numbers
        errors = " ".join(validate.visibility_errors(plan))
        self.assertIn("stored visibility differs", errors)
        plan = plan_of(BRIDGE)
        sc3 = shot(plan, "SC_003")
        sc3.pop("repairs")
        self.assertIn("without a documented visibility repair", " ".join(validate.visibility_errors(plan)))


class CompositionTest(unittest.TestCase):
    def test_three_long_bridges_do_not_read_at_once_at_640(self):
        plan = plan_of(BRIDGE)
        ids = ["timber_beam_bridge", "stone_arch_bridge", "steel_truss_bridge"]
        rows = composition.evaluate(plan["states"], ids, "BRIDGE_STACK", CCFG, "detail", PRESETS)
        self.assertIsNone(composition.best(rows))
        self.assertTrue(all(r["metrics"]["min_detail_px"] < CCFG["purposes"]["detail"]["min_detail_px"]
                            for r in rows if r["metrics"]))
        seq = composition.evaluate_sequence(plan["states"], ids, ids, "BRIDGE_THREE_QUARTER", CCFG, "detail", PRESETS)
        self.assertTrue(all(r["ok"] for r in seq))
        ov = composition.best(composition.evaluate(plan["states"], ids, "BRIDGE_STACK", CCFG, "overview", PRESETS))
        self.assertEqual((ov["layout"], ov["gap_ratio"]), ("STACK", 0.25))

    def test_readability_depends_on_the_screen_resolution(self):
        plan = plan_of(BRIDGE)
        ids = ["timber_beam_bridge", "stone_arch_bridge", "steel_truss_bridge"]
        big = dict(CCFG, reference_resolution=[1920, 1080])
        self.assertIsNotNone(composition.best(composition.evaluate(plan["states"], ids, "BRIDGE_STACK", big, "detail",
                                                                   PRESETS)))

    def test_compact_houses_keep_a_row(self):
        roof = plan_of(ROOF)
        comp = roof["shots"][-1]["composition"]
        self.assertEqual((comp["layout"], comp["gap_ratio"], comp["scale"]), ("SIDE_BY_SIDE_ROW", 0.35, "COMMON"))

    def test_sequential_comparison_keeps_one_scale(self):
        plan = plan_of(BRIDGE)
        seq = [s for s in plan["shots"] if s.get("sequence")]
        fits = {round(VIS.build_scene(s["shot"], plan["states"], 24, PRESETS).fit["ortho_scale"], 6) for s in seq}
        self.assertEqual(len(fits), 1)
        self.assertEqual({s["composition"]["scale"] for s in seq}, {"COMMON"})
        self.assertEqual([s["shot"]["animation"]["label"] for s in seq],
                         ["Timber beam bridge", "Stone arch bridge", "Steel truss bridge"])
        bad = plan_of(BRIDGE)
        for s in bad["shots"]:
            if s.get("sequence"):
                s["composition"]["scale"] = "NORMALIZED"
        self.assertIn("scale COMMON", " ".join(validate.visibility_errors(bad)))

    def test_side_by_side_cue_is_reported_when_shown_one_at_a_time(self):
        # M6 reworded the real B7 ("Let's compare them one at a time"); the M5.5 wording, on a
        # copy, is still reported - and since M6 it blocks the plan (planner/consistency.py).
        b7 = next(c for c in plan_of(BRIDGE)["coverage"] if c["beat_id"] == "B7")
        self.assertFalse(any("seen together" in i for i in b7["issues"]))
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / BRIDGE.name
            shutil.copytree(BRIDGE, p, ignore=shutil.ignore_patterns("renders", "output", "scenes"))
            doc = json.loads((p / "script/visual_beats.json").read_text())
            old = next(b for b in doc["beats"] if b["beat_id"] == "B7")
            old["narration"] = "Side by side, the three models span the same gap in three different ways."
            (p / "script/visual_beats.json").write_text(json.dumps(doc))
            plan = pl.plan_project(p)
            b7 = next(c for c in plan["coverage"] if c["beat_id"] == "B7")
            self.assertTrue(any("seen together" in i for i in b7["issues"]))
            self.assertFalse(plan["executable"])


class ProfileGateTest(unittest.TestCase):
    """Technical preview eligibility is not publication authorization."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.suffolk = Path(cls.tmp.name) / "suffolk-roofs"
        shutil.copytree(SUFFOLK, cls.suffolk, ignore=shutil.ignore_patterns("renders", "output", "scenes"))

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def set_profile(self, p, profile, **extra):
        f = p / "project.json"
        d = json.loads(f.read_text())
        d["production_profile"] = profile
        d.update(extra)
        f.write_text(json.dumps(d))

    def test_suffolk_statuses_are_unchanged(self):
        from pipeline import gates
        r = gates.evaluate(SUFFOLK)
        self.assertEqual(r["profile"], "NARRATED_INTERNAL_REVIEW")
        self.assertEqual(r["statuses"], ["TECHNICALLY_VALIDATED", "EDITORIAL_REVIEW_PENDING", "TTS_RIGHTS_PENDING"])
        self.assertEqual(r["gates"]["G6 final publication readiness"]["status"], "BLOCKED")
        self.assertNotIn("PUBLICATION_READY", r["statuses"])

    def test_silent_profile_cannot_switch_off_narration_gates(self):
        from pipeline import gates
        self.set_profile(self.suffolk, "TECHNICAL_SILENT_PREVIEW")
        try:
            r = gates.evaluate(self.suffolk)
            self.assertEqual(r["gates"]["G0 project & schema validation"]["status"], "FAIL")
            self.assertIn("has narration", " ".join(r["gates"]["G0 project & schema validation"]["notes"]))
            self.assertNotIn("TECHNICALLY_VALIDATED", r["statuses"])
            self.assertIn("NOT VALID", r["verdict"])
        finally:
            self.set_profile(self.suffolk, "NARRATED_INTERNAL_REVIEW")

    def test_unknown_profile_is_rejected(self):
        from tools.validator import validate_project
        self.set_profile(self.suffolk, "PUBLISH_ANYWAY")
        try:
            errors, _ = validate_project(self.suffolk)
            self.assertIn("production_profile must be one of", " ".join(errors))
        finally:
            self.set_profile(self.suffolk, "NARRATED_INTERNAL_REVIEW")

    def test_publication_candidate_needs_metadata_and_stays_blocked(self):
        from pipeline import gates
        self.set_profile(self.suffolk, "PUBLICATION_CANDIDATE")
        try:
            r = gates.evaluate(self.suffolk)
            g6 = r["gates"]["G6 final publication readiness"]
            self.assertEqual(g6["status"], "BLOCKED")
            self.assertIn("publication metadata missing", " ".join(g6["notes"]))
            self.assertIn("unverified claims", " ".join(g6["notes"]))
            self.assertNotIn("PUBLICATION_READY", r["statuses"])
        finally:
            self.set_profile(self.suffolk, "NARRATED_INTERNAL_REVIEW")

    def test_internal_review_is_never_promoted_implicitly(self):
        from pipeline import gates
        original = gates._evaluate_narrated
        gates._evaluate_narrated = lambda p, s="": {
            "verdict": "PUBLICATION_READY", "statuses": ["PUBLICATION_READY"],
            "gates": {"G6 final publication readiness": {"status": "PASS", "notes": ["all gates pass"]}}}
        try:
            r = gates.evaluate(self.suffolk)
            self.assertNotIn("PUBLICATION_READY", r["statuses"])
            self.assertIn("set production_profile PUBLICATION_CANDIDATE", r["verdict"])
        finally:
            gates._evaluate_narrated = original

    def test_silent_preview_gates_are_not_applicable_not_failures(self):
        from pipeline import gates
        r = gates.evaluate(BRIDGE)
        g = r["gates"]
        self.assertEqual(r["profile"], "TECHNICAL_SILENT_PREVIEW")
        for name in ("G2 narration audio & TTS rights", "G3 narration timing lock", "G5 media assembly & subtitles"):
            self.assertEqual(g[name]["status"], "NOT_APPLICABLE")
        self.assertEqual(g["G6 final publication readiness"]["status"], "BLOCKED")
        self.assertNotIn("PUBLICATION_READY", r["statuses"])
        self.assertTrue(r["verdict"].startswith("TECHNICAL PREVIEW"))
        self.assertTrue("NOT FOR PUBLICATION" in r["verdict"] or "NOT VALID" in r["verdict"])
        self.assertFalse(any("audio" in n.lower() and v["status"] == "FAIL" for v in g.values() for n in v["notes"]))


class SilentMediaTest(unittest.TestCase):
    def test_staleness_comes_from_render_dependencies(self):
        from pipeline import gates
        from tools.cli import shots, expected_frames
        current = shots(BRIDGE)
        total = sum(expected_frames(BRIDGE, s) for s in current)
        keys = {s["id"]: render_cache.cache_key(render_cache.components(BRIDGE, s, "preview")) for s in current}
        b = {"passed": 1, "failed": 0, "total": 1}
        good = {"problems": [], "expected_total_frames": total, "render_keys": keys}
        self.assertEqual(gates.silent_media(BRIDGE, good, b, "preview")[0], "PASS")
        changed = dict(good, render_keys=dict(keys, SC_003="0" * 64))
        status, notes = gates.silent_media(BRIDGE, changed, b, "preview")
        self.assertEqual(status, "FAIL")
        self.assertIn("SC_003 changed", " ".join(notes))
        self.assertEqual(gates.silent_media(BRIDGE, dict(good, expected_total_frames=total + 1), b, "preview")[0], "FAIL")
        self.assertEqual(gates.silent_media(BRIDGE, dict(good, problems=["full: 3 decode error(s)"]), b, "preview")[0], "FAIL")
        self.assertIn("predates", " ".join(gates.silent_media(BRIDGE, {"problems": [], "expected_total_frames": total}, b,
                                                              "preview")[1]))


class EvaluationSuiteTest(unittest.TestCase):
    def test_dataset_passes_on_every_dimension(self):
        s = evaluate.run()
        self.assertEqual(s["passed"], s["cases"])
        self.assertEqual(set(s["by_kind"]), {"positive", "negative", "ambiguous", "missing_capability"})
        self.assertEqual(set(s["by_family"]), {"bridge", "roof", "floating"})   # floating: SEQUENCE MOVE / OSCILLATE label (2026-11-08)
        self.assertTrue(all(v["checks"] > 0 for v in s["dimensions"].values()))

    def test_checker_detects_a_wrong_expectation(self):
        data = json.loads((ROOT / "evaluation/visual_planning/cases.json").read_text())
        case = copy.deepcopy(next(c for c in data["cases"] if c["id"] == "BR-POS-01"))
        case["expect"]["repair"] = "REFRAME"               # wrong on purpose
        with tempfile.TemporaryDirectory() as tmp:
            f = Path(tmp) / "cases.json"
            f.write_text(json.dumps({"cases": [case]}))
            s = evaluate.run(f)
        self.assertEqual(s["passed"], 0)


class CacheDependencyM55Test(unittest.TestCase):
    """Which plan decisions invalidate which rendered shots."""

    def keys(self, p, story=None):
        story = story or json.loads((p / "storyboard/storyboard.json").read_text())
        return {s["id"]: render_cache.cache_key(render_cache.components(p, s, "preview")) for s in story["shots"]}

    def compiled(self, tmp, plan_edit=None, cfg_edit=None, project_edit=None):
        from planner import compiler
        p = copy_planning(tmp)
        plan = plan_of(BRIDGE)
        if plan_edit:
            plan_edit(plan)
        compiler.compile_plan(plan, p)
        if project_edit:
            d = json.loads((p / "project.json").read_text())
            project_edit(d)
            (p / "project.json").write_text(json.dumps(d))
        return self.keys(p)

    def test_visual_decisions_invalidate_only_their_shots(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = self.compiled(tmp)
        cases = {
            "camera": (lambda pl_: shot(pl_, "SC_008")["shot"].update(camera="ELEVATION"), ["SC_008"]),
            "ghost": (lambda pl_: shot(pl_, "SC_003")["shot"]["animation"]["highlight"].update(ghost_transparency=0.6),
                      ["SC_003"]),
            "layout": (lambda pl_: shot(pl_, "SC_015")["shot"]["animation"].update(gap_ratio=0.5), ["SC_015"]),
            "target": (lambda pl_: shot(pl_, "SC_008")["shot"]["animation"]["highlight"].update(
                components=shot(pl_, "SC_008")["shot"]["animation"]["highlight"]["components"][:2]), ["SC_008"]),
            "editorial": (lambda pl_: shot(pl_, "SC_008").update(explanation="reworded"), []),
        }
        for name, (edit, expected) in cases.items():
            with tempfile.TemporaryDirectory() as tmp:
                changed = self.compiled(tmp, plan_edit=edit)
            self.assertEqual(sorted(k for k in base if base[k] != changed[k]), expected, name)

    def test_profile_metadata_and_thresholds_do_not_rerender(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = self.compiled(tmp)
        with tempfile.TemporaryDirectory() as tmp:
            prof = self.compiled(tmp, project_edit=lambda d: d.update(production_profile="PUBLICATION_CANDIDATE",
                                                                     publication_metadata={"title": "x"}))
        self.assertEqual(base, prof)
        # A threshold change that does not change any decision leaves the compiled shots identical.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "root"
            shutil.copytree(ROOT / "config", root / "config")
            (root / "asset_library").symlink_to(ROOT / "asset_library")
            (root / "projects").mkdir()
            cfg = json.loads((root / "config/visual_planning.json").read_text())
            cfg["visibility"]["min_visible_share"] = 0.24
            (root / "config/visual_planning.json").write_text(json.dumps(cfg))
            p = copy_planning(root / "projects")
            a = pl.plan_project(p, root)
        b = plan_of(BRIDGE)
        self.assertEqual([s["shot"] for s in a["shots"]], [s["shot"] for s in b["shots"]])


class SchemaM55Test(unittest.TestCase):
    def test_schemas_match_the_code(self):
        from pipeline import gates
        plan_schema = json.loads((ROOT / "schemas/visual_plan.schema.json").read_text())
        shot_props = plan_schema["properties"]["shots"]["items"]["properties"]
        problems = shot_props["visibility"]["properties"]["targets"]["items"]["properties"]["problems"]["items"]["enum"]
        self.assertEqual(set(problems), {"OCCLUDED", "TOO_SMALL", "CLIPPED", "SUBTITLE_SAFE_AREA", "PIECES_HIDDEN", "NOT_SHOWN"})
        self.assertEqual(shot_props["composition"]["properties"]["layout"]["enum"], list(composition.LAYOUTS))
        self.assertEqual(shot_props["visibility"]["properties"]["targets"]["items"]["properties"]["verification"]["enum"],
                         list(VIS.VERIFICATION))
        project = json.loads((ROOT / "schemas/project.schema.json").read_text())
        self.assertEqual(project["properties"]["production_profile"]["enum"], list(gates.PROFILES))
        self.assertEqual(project["properties"]["publication_metadata"]["required"], list(gates.PUBLICATION_METADATA))
        for remedy in [r["remedy"] for ps in plan_of(BRIDGE)["shots"] + plan_of(ROOF)["shots"] for r in ps.get("repairs", [])]:
            self.assertRegex(remedy, shot_props["repairs"]["items"]["properties"]["remedy"]["pattern"])
        self.assertEqual(repair.REMEDIES, ("REFRAME", "SAFE_BAND", "ALT_CAMERA", "GHOST"))


class ReproducibilityTest(unittest.TestCase):
    def test_visibility_and_repairs_are_deterministic(self):
        with tempfile.TemporaryDirectory() as tmp:
            a = pl.plan_project(copy_planning(tmp))
        stored = plan_of(BRIDGE)
        self.assertEqual(json.dumps([s.get("visibility") for s in a["shots"]], sort_keys=True),
                         json.dumps([s.get("visibility") for s in stored["shots"]], sort_keys=True))
        self.assertEqual(json.dumps([c.get("visual_repairs") for c in a["coverage"]], sort_keys=True),
                         json.dumps([c.get("visual_repairs") for c in stored["coverage"]], sort_keys=True))


if __name__ == "__main__":
    unittest.main()
