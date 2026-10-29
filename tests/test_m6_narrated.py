"""M6: licensed-TTS adapter, audio lock, semantic annotations, narration/visual consistency,
multi-architecture scene contexts and the publication gates (offline; no Blender, no TTS)."""
import copy
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from engine import annotation_layout as AL, spec
from integrations.tts import kokoro, providers
from pipeline import audio_lock, narration as nar, pronunciation as pron
from planner import annotations as AN, consistency, planner as pl, timing as T, validate, vocabulary as V
from tools.cli import ROOT
from tools import validator

PILOT = ROOT / "projects" / "bridge-load-explained"
BRIDGE = ROOT / "projects" / "bridge-story-m5"
ROOFS = ROOT / "projects" / "roof-plan-m5"
FIXTURE = ROOT / "tests" / "fixtures" / "m6_cross_family"
STYLE = AL.load_style()
VOCAB = V.Vocabulary()


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def copy_project(src, ignore=("renders", "output", "scenes", "qa")):
    tmp = tempfile.TemporaryDirectory()
    dst = Path(tmp.name) / Path(src).name
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns(*ignore))
    return tmp, dst


_PLANS = {}


def plan_of(path):
    if path not in _PLANS:
        _PLANS[path] = pl.plan_project(path)
    return copy.deepcopy(_PLANS[path])


class KokoroRightsTest(unittest.TestCase):
    """Apache weights alone never make a provider publication-cleared."""

    def setUp(self):
        self.registry = providers.load_registry()

    def test_registry_keeps_kokoro_pending_review(self):
        info = self.registry["providers"]["kokoro"]
        self.assertEqual(info["rights_class"], "PENDING_REVIEW")
        self.assertIn("NOT CLEARED", info["license"]["commercial_publication"])
        self.assertEqual(providers.validate_registry(self.registry), [])
        self.assertEqual(providers.check_purpose("kokoro", "internal_preview", self.registry), "PENDING_REVIEW")
        with self.assertRaises(providers.RightsError):
            providers.check_purpose("kokoro", "publication", self.registry)

    def test_unlicensed_tts_asset_is_refused(self):
        reg = copy.deepcopy(self.registry)
        reg["providers"]["kokoro"]["rights_class"] = "PUBLICATION_CLEARED"   # no named human clearance
        self.assertTrue(any("human clearance" in e for e in providers.validate_registry(reg)))
        narration = read(PILOT / "script/narration.json")
        narration["voice"]["license"]["rights_class"] = "PUBLICATION_CLEARED"
        errs = nar.validate(narration, read(PILOT / "research/sources.json"), self.registry)
        self.assertTrue(any("disagrees" in e for e in errs))
        narration["voice"]["license"]["status"] = "APPROVED"     # self-approval without a reviewer
        errs = nar.validate(narration, read(PILOT / "research/sources.json"), self.registry)
        self.assertTrue(any("approved_by" in e for e in errs))

    def test_unaudited_voice_and_changed_weights_stop_generation(self):
        self.assertTrue(any("not in the audited voice list" in e for e in kokoro.verify_release("af_heart")))
        original = kokoro.MODEL_SHA256
        try:
            kokoro.MODEL_SHA256 = "0" * 64
            errs = kokoro.verify_release("bf_emma")
        finally:
            kokoro.MODEL_SHA256 = original
        if kokoro.snapshot_dir().is_dir():
            self.assertTrue(any("differs from the audited" in e for e in errs))

    def test_cache_identity_separates_providers_and_rights(self):
        from pipeline.audio_manifest import cache_key
        a = kokoro.KokoroAdapter(worker=object())
        voice = {"voice": "bf_emma", "voice_sha256": kokoro.VOICE_SHA256["bf_emma"], "lang_code": "b"}
        params = a.params({"params": {"speed": 1.0}})
        args = (a.name, a.adapter_version, a.model, a.model_revision, "Text.", "kokoro_bf_emma",
                a.voice_identity(voice), params)
        k1 = cache_key(*args, "PENDING_REVIEW", None)
        self.assertNotEqual(k1, cache_key(*args, "INTERNAL_PREVIEW_ONLY", None))
        self.assertNotEqual(k1, cache_key("omnivoice", *args[1:], "PENDING_REVIEW", None))

    def test_pilot_audio_is_pending_review_kokoro(self):
        m = read(PILOT / "audio/narration_manifest.json")
        current = {s["cache_key"] for b in m["beats"].values() for s in b["sentences"]}
        recs = [m["segments"][k] for k in current]
        self.assertEqual({r["provider"] for r in recs}, {"kokoro"})
        self.assertEqual({r["rights_class"] for r in recs}, {"PENDING_REVIEW"})
        self.assertEqual({r["model_sha256"] for r in recs}, {kokoro.MODEL_SHA256})
        self.assertTrue(all(r["asr"]["pass"] for r in recs))
        self.assertEqual(m["rights"]["audit"], "docs/licensing/KOKORO_LICENSE_AUDIT.md")

    def test_kokoro_pronunciation_form(self):
        lex = {"entries": [{"id": "P1", "written": "voussoir", "speech": {"kokoro": "voussoir"},
                            "status": "PENDING_LISTENING_REVIEW"}]}
        self.assertTrue(any("Kokoro (misaki) form" in e for e in pron.validate(lex)))
        lex["entries"][0]["speech"]["kokoro"] = "[voussoir](/vˈuːswɑː/)"
        self.assertEqual(pron.validate(lex), [])


class AudioLockTest(unittest.TestCase):
    def setUp(self):
        self.tmp, self.p = copy_project(PILOT)

    def tearDown(self):
        self.tmp.cleanup()

    def test_lock_and_finalize_are_consistent_and_idempotent(self):
        t = audio_lock.lock_beats(self.p)
        self.assertTrue(t["locked"], t["problems"])
        f1 = audio_lock.finalize(self.p)
        self.assertEqual(audio_lock.check_consistency(f1), [])
        f2 = audio_lock.finalize(self.p)
        self.assertEqual(f1["beats"], f2["beats"])
        self.assertTrue(read(self.p / "project.json")["audio_timing_locked"])
        self.assertAlmostEqual(read(self.p / "project.json")["duration_seconds"], f1["total_seconds"])
        for b in f1["beats"]:   # audio sits inside its shots, never stretched or cut
            lo = next(s for s in f1["shots"] if s["id"] == b["shots"][0])["start_seconds"]
            last = next(s for s in f1["shots"] if s["id"] == b["shots"][-1])
            self.assertGreaterEqual(b["start_seconds"], lo)
            self.assertLessEqual(b["start_seconds"] + b["duration"], last["start_seconds"] + last["duration_seconds"])

    def test_inconsistent_timing_manifest_is_rejected(self):
        audio_lock.lock_beats(self.p)
        t = audio_lock.finalize(self.p)
        bad = copy.deepcopy(t)
        bad["beats"][2]["sentences"][1]["start"] += 0.5
        self.assertTrue(any("absolute start differs" in e for e in audio_lock.check_consistency(bad)))
        bad = copy.deepcopy(t)
        bad["shots"][3]["start_frame"] += 2
        self.assertTrue(any("gap or overlap" in e for e in audio_lock.check_consistency(bad)))
        bad = copy.deepcopy(t)
        bad["beats"][0]["sentences"][0]["rel_start"] += 0.3
        (self.p / "script/timing.json").write_text(json.dumps(bad))
        errs, _ = validator.validate_project(self.p)
        self.assertTrue(any("inconsistent" in e or "outside" in e or "differs" in e for e in errs), errs)

    def test_script_and_visual_beats_must_narrate_the_same_words(self):
        beats = read(self.p / "script/visual_beats.json")
        beats["beats"][0]["narration"] = beats["beats"][0]["narration"].replace("weight", "mass")
        (self.p / "script/visual_beats.json").write_text(json.dumps(beats))
        t = audio_lock.lock_beats(self.p)
        self.assertFalse(t["locked"])
        self.assertTrue(any("B1" in x for x in t["problems"]))
        with self.assertRaises(T.TimingError):   # the planner refuses an unlocked AUDIO_LOCKED plan
            pl.plan_project(self.p)

    def test_stale_plan_after_new_audio(self):
        audio_lock.lock_beats(self.p)
        plan = pl.plan_project(self.p)
        t = read(self.p / "script/timing.json")
        t["beats"][0]["duration"] += 0.4
        t["beats_sha256"] = audio_lock.beats_hash(t)
        (self.p / "script/timing.json").write_text(json.dumps(t))
        errs = validate.annotation_errors(plan, self.p, read(self.p / "script/visual_beats.json"),
                                          read(self.p / "research/sources.json"), VOCAB)
        self.assertTrue(any("timing changed" in e for e in errs))


class PilotPlanTest(unittest.TestCase):
    """bridge-load-explained: audio-locked, annotated, evidence-backed."""

    @classmethod
    def setUpClass(cls):
        cls.plan = plan_of(PILOT)
        cls.doc = read(PILOT / "script/visual_beats.json")

    def test_plan_is_executable_and_validates(self):
        self.assertTrue(self.plan["executable"])
        self.assertEqual(self.plan["timing_mode"], "AUDIO_LOCKED")
        self.assertEqual(validate.validate_plan(self.plan, PILOT, engine_check=False), [])
        self.assertTrue(120 <= self.plan["duration_seconds"] <= 180)

    def test_every_annotation_is_placed_with_evidence(self):
        placed = {r["id"]: r for c in self.plan["coverage"] for r in c.get("annotations", [])}
        wanted = [a["id"] for b in self.doc["beats"] for a in b.get("annotations", [])]
        self.assertEqual(sorted(placed), sorted(wanted))
        self.assertEqual({r["status"] for r in placed.values()}, {"PLACED"})
        for b in self.doc["beats"]:
            for a in b.get("annotations", []):
                if AN.needs_claim(a):
                    self.assertIn(a["claim_id"], {c for x in self.doc["beats"][:self.doc["beats"].index(b) + 1]
                                                  for c in x["claim_ids"]})

    def test_arrow_rules_and_disclaimer_tag(self):
        items = [a for ps in self.plan["shots"] for a in (ps.get("annotations") or {}).get("items", [])]
        lengths = set()
        for a in items:
            for e in a["elements"]:
                if e["kind"] == "arrow" and a["type"] in ("LOAD_ARROW", "REACTION_ARROW") and not e.get("halo"):
                    dx, dy = (e["tip"][0] - e["tail"][0]) * 16 / 9, e["tip"][1] - e["tail"][1]
                    lengths.add(round((dx * dx + dy * dy) ** 0.5, 3))
                    if a["type"] == "LOAD_ARROW":
                        self.assertLess(dy, 0)
                        self.assertAlmostEqual(dx, 0.0, places=6)
                    else:
                        self.assertGreater(dy, 0)
        self.assertEqual(lengths, {STYLE["arrow"]["length"]})   # length never encodes magnitude
        for ps in self.plan["shots"]:
            items = (ps.get("annotations") or {}).get("items", [])
            forces = [a for a in items if a["type"] in AL.FORCE_TYPES or a.get("force")]
            tags = [a for a in items if a["type"] == "TAG"]
            self.assertEqual(len(tags), 1 if forces else 0, ps["shot_id"])
            if tags:
                self.assertIn("not to scale", tags[0]["elements"][1]["text"])

    def test_annotations_avoid_the_subtitle_zone_and_each_other(self):
        for ps in self.plan["shots"]:
            data = ps.get("annotations")
            if data:
                self.assertEqual(AL.check(data["items"], STYLE, 16 / 9, caption_boxes=[r["box"] for r in data["reserved"]]),
                                 [], ps["shot_id"])

    def test_annotations_follow_their_sentences(self):
        offsets = T.sentence_offsets(self.doc, PILOT, read(ROOT / "config/visual_planning.json")["timing"])
        specs = {a["id"]: (b["beat_id"], a) for b in self.doc["beats"] for a in b.get("annotations", [])}
        for ps in self.plan["shots"]:
            for a in (ps.get("annotations") or {}).get("items", []):
                if a["type"] == "TAG":
                    continue
                bid, s = specs[a["id"]]
                start = offsets[bid][s.get("sentence", 0)][0]
                self.assertGreaterEqual(ps["timing"]["beat_offset_seconds"] + a["appear"] + 0.15, start, a["id"])

    def test_sequential_comparison_cuts_on_sentences(self):
        offsets = T.sentence_offsets(self.doc, PILOT, read(ROOT / "config/visual_planning.json")["timing"])["B7"]
        seq = [ps for ps in self.plan["shots"] if ps["beat_id"] == "B7"]
        self.assertEqual([ps["shot"]["animation"]["label"] for ps in seq],
                         ["Timber beam bridge", "Stone arch bridge", "Steel truss bridge"])
        for ps, k in zip(seq[1:], (2, 3)):
            self.assertAlmostEqual(ps["timing"]["beat_offset_seconds"], offsets[k][0] - pl.SENTENCE_CUT_LEAD, delta=1 / 24)
        self.assertTrue(all(ps["shot"]["animation"]["label_position"] == "TOP" for ps in seq))

    def test_narrated_captions_stay_above_the_subtitle_zone(self):
        last = self.plan["shots"][-1]
        self.assertEqual(last["template"], "SIDE_BY_SIDE")
        anim = last["shot"]["animation"]
        self.assertGreaterEqual(anim["label_band"], 0.24)
        if anim["layout"] == "ROW":
            self.assertEqual(anim["label_position"], "BAND_TOP")
        for ps in plan_of(BRIDGE)["shots"]:   # PROVISIONAL (silent) projects keep the M5.5 captions
            self.assertNotIn("label_position", ps["shot"]["animation"])

    def test_glow_starts_with_its_sentence(self):
        offsets = T.sentence_offsets(self.doc, PILOT, read(ROOT / "config/visual_planning.json")["timing"])
        b2 = next(ps for ps in self.plan["shots"] if ps["beat_id"] == "B2")
        self.assertAlmostEqual(b2["shot"]["animation"]["highlight"]["start_seconds"], offsets["B2"][2][0] - 0.2, places=3)

    def test_no_contradiction_and_b8_reference_is_reported(self):
        rows = self.plan["consistency"]["rows"]
        self.assertEqual(self.plan["consistency"]["summary"]["CONTRADICTION"], 0)
        self.assertTrue(any(r["beat_id"] == "B8" and r["verdict"] == "UNCERTAIN" for r in rows))

    def test_truss_members_are_never_force_coloured(self):
        b6 = next(ps for ps in self.plan["shots"] if ps["beat_id"] == "B6")
        for a in b6["annotations"]["items"]:
            if a.get("force"):
                self.assertEqual(a["claim_id"], "CLM_613")
                ids = {c for x in a["anchors"] for c in x["component_ids"]}
                self.assertTrue(all("chords" in c for c in ids), ids)
        h = b6["shot"]["animation"]["highlight"]
        self.assertNotIn("color", h)


class AnnotationNegativeTest(unittest.TestCase):
    def setUp(self):
        self.tmp, self.p = copy_project(PILOT)
        audio_lock.lock_beats(self.p)
        self.doc = read(self.p / "script/visual_beats.json")
        self.sources = read(self.p / "research/sources.json")

    def tearDown(self):
        self.tmp.cleanup()

    def beat(self, bid):
        return next(b for b in self.doc["beats"] if b["beat_id"] == bid)

    def save(self):
        (self.p / "script/visual_beats.json").write_text(json.dumps(self.doc))

    def test_missing_claim_source(self):
        claim = next(c for c in self.sources["claims"] if c["id"] == "CLM_609")
        claim["source_ids"] = []
        self.assertTrue(any("CLM_609 has no source" in e for e in AN.validate_spec(self.doc, self.sources, VOCAB)))
        self.beat("B5")["annotations"][0].pop("claim_id")
        self.assertTrue(any("needs claim_id" in e for e in AN.validate_spec(self.doc, read(self.p / "research/sources.json"), VOCAB)))

    def test_force_on_a_member_the_claim_does_not_name(self):
        a = next(x for x in self.beat("B6")["annotations"] if x["id"] == "B6_bottom")
        a["target"] = {"concept": "diagonal_members", "group": "truss_south", "pick": "LEFTMOST"}
        self.assertTrue(any("does not state a force in 'diagonal_members'" in e
                            for e in AN.validate_spec(self.doc, self.sources, VOCAB)))

    def test_upward_load_arrow_and_unnarrated_claim(self):
        self.beat("B1")["annotations"][0]["direction"] = "UP"
        self.beat("B1")["annotations"][0]["claim_id"] = "CLM_609"
        errs = AN.validate_spec(self.doc, self.sources, VOCAB)
        self.assertTrue(any("points DOWN" in e for e in errs))
        self.assertTrue(any("not narrated by this beat or an earlier one" in e for e in errs))

    def test_nonexistent_anchor_blocks_the_plan(self):
        self.beat("B6")["annotations"][0]["target"] = {"concept": "voussoir"}   # no voussoir on a truss
        self.save()
        plan = pl.plan_project(self.p)
        b6 = next(c for c in plan["coverage"] if c["beat_id"] == "B6")
        self.assertFalse(plan["executable"])
        self.assertTrue(any("anchor target not found" in i for i in b6["issues"]))

    def test_label_outside_the_frame_and_over_the_subtitles(self):
        plan = plan_of(PILOT)
        items = copy.deepcopy(next(ps for ps in plan["shots"] if ps["beat_id"] == "B2")["annotations"]["items"])
        lab = next(a for a in items if a["id"] == "B2_pier")
        for e in lab["elements"]:
            if e["kind"] in ("plate", "text"):
                e["box"] = [e["box"][0] + 0.9, e["box"][1], e["box"][2] + 0.9, e["box"][3]]
                if "center" in e:
                    e["center"] = [e["center"][0] + 0.9, e["center"][1]]
        probs = AL.check(items, STYLE, 16 / 9)
        self.assertTrue(any("B2_pier: OUTSIDE_SAFE_AREA" in x for x in probs))
        self.assertTrue(any("B2_pier: ELEMENT_OUTSIDE_FRAME" in x for x in probs))
        items = copy.deepcopy(next(ps for ps in plan["shots"] if ps["beat_id"] == "B2")["annotations"]["items"])
        lab = next(a for a in items if a["id"] == "B2_pier")
        for e in lab["elements"]:
            if e["kind"] == "plate":
                e["box"] = [e["box"][0], 0.06, e["box"][2], 0.1]
        self.assertTrue(any("B2_pier: IN_SUBTITLE_ZONE" in x for x in AL.check(items, STYLE, 16 / 9)))

    def test_hand_edited_annotation_is_caught(self):
        plan = plan_of(PILOT)
        ps = next(s for s in plan["shots"] if s["beat_id"] == "B5")
        ps["annotations"]["items"][1]["anchors"][0]["screen"][0] += 0.05
        ps["shot"]["annotations"] = ps["annotations"]
        errs = validate.annotation_errors(plan, PILOT, read(PILOT / "script/visual_beats.json"),
                                          read(PILOT / "research/sources.json"), VOCAB)
        self.assertTrue(any("projects to" in e for e in errs))

    def test_load_path_intent_needs_annotations(self):
        self.beat("B2").pop("annotations")
        self.save()
        with self.assertRaises(pl.PlanningError) as ctx:
            pl.plan_project(self.p)
        self.assertTrue(any("needs annotations" in e for e in ctx.exception.errors))


class ConsistencyTest(unittest.TestCase):
    def test_side_by_side_wording_on_a_sequential_comparison_fails_closed(self):
        tmp, p = copy_project(BRIDGE)
        try:
            doc = read(p / "script/visual_beats.json")
            b7 = next(b for b in doc["beats"] if b["beat_id"] == "B7")
            b7["narration"] = "Side by side, the three models span the same gap in three different ways."
            (p / "script/visual_beats.json").write_text(json.dumps(doc))
            plan = pl.plan_project(p)
            self.assertFalse(plan["executable"])
            row = next(r for r in plan["consistency"]["rows"] if r["beat_id"] == "B7")
            self.assertEqual((row["rule"], row["verdict"]), ("SIMULTANEOUS", "CONTRADICTION"))
            self.assertTrue(any("contradiction" in e for e in validate.validate_plan(plan, p, engine_check=False)))
        finally:
            tmp.cleanup()

    def test_bridge_story_b7_is_fixed(self):
        doc = read(BRIDGE / "script/visual_beats.json")
        b7 = next(b for b in doc["beats"] if b["beat_id"] == "B7")
        self.assertTrue(b7["narration"].startswith("Let's compare them one at a time"))
        plan = plan_of(BRIDGE)
        self.assertTrue(plan["executable"])
        row = next(r for r in plan["consistency"]["rows"] if r["beat_id"] == "B7")
        self.assertEqual((row["rule"], row["verdict"]), ("SEQUENTIAL", "CONSISTENT"))

    def _plan_with(self, bid, sentence_text, mutate=None):
        plan = plan_of(PILOT)
        doc = read(PILOT / "script/visual_beats.json")
        b = next(x for x in doc["beats"] if x["beat_id"] == bid)
        sentences = T.split_sentences(b["narration"])
        sentences[-1] = sentence_text
        b["narration"] = " ".join(sentences)
        if mutate:
            mutate(plan)
        offsets = T.sentence_offsets(doc, PILOT, read(ROOT / "config/visual_planning.json")["timing"])
        return [r for r in consistency.check_plan(plan, doc, offsets, STYLE) if r["beat_id"] == bid]

    def test_deictic_colour_and_arrow_rules(self):
        def no_glow(plan):
            for ps in plan["shots"]:
                if ps["beat_id"] == "B8":
                    ps["shot"]["animation"].pop("highlight", None)
        rows = self._plan_with("B8", "Look at this component on the far side.", no_glow)
        self.assertTrue(any(r["rule"] == "DEICTIC" and r["verdict"] == "CONTRADICTION" for r in rows))
        rows = self._plan_with("B8", "These arrows are red.")
        self.assertTrue(any(r["rule"] == "ARROWS" and r["verdict"] == "CONTRADICTION" for r in rows))
        self.assertTrue(any(r["rule"] == "COLOUR" and r["verdict"] == "CONTRADICTION" for r in rows))
        rows = self._plan_with("B5", "The red arrows show compression.")
        self.assertTrue(any(r["rule"] == "COLOUR" and r["verdict"] == "CONSISTENT" for r in rows))
        rows = self._plan_with("B5", "On the left, the arch meets its pier.")
        self.assertTrue(any(r["rule"] == "SIDE" and r["verdict"] == "UNCERTAIN" for r in rows))

    def test_plain_together_is_not_a_comparison_cue(self):
        doc = read(PILOT / "script/visual_beats.json")
        self.assertIn("pressing the stones together", doc["beats"][4]["narration"])
        self.assertFalse(any(r["rule"] == "SIMULTANEOUS" for r in plan_of(PILOT)["consistency"]["rows"]))

    def test_narration_incompatible_transition(self):
        def as_hard_cut(plan):   # the cut to the truss now falls 2 s into the last sentence
            seq = [ps for ps in plan["shots"] if ps["beat_id"] == "B7"]
            seq[1]["timing"]["duration_seconds"] += 2.0
            seq[2]["timing"]["beat_offset_seconds"] += 2.0
            seq[2]["cut_from_previous"] = "hard"
        rows = self._plan_with("B7", "In the truss the arch becomes a truss.", as_hard_cut)
        self.assertTrue(any(r["rule"] == "TRANSFORMATION" and r["verdict"] == "CONTRADICTION" for r in rows))


class SceneContextTest(unittest.TestCase):
    """Multi-architecture orchestration: one base per family, per-shot scene context."""

    @classmethod
    def setUpClass(cls):
        cls.tmp, cls.p = copy_project(FIXTURE)
        cls.plan = pl.plan_project(cls.p)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_contexts_and_shots(self):
        st = self.plan["states"]
        self.assertEqual(st["schema_version"], 3)
        self.assertEqual(sorted(st["contexts"]), ["bridge", "roof"])
        self.assertEqual(spec.validate_states(st), [])
        ctx = [ps["shot"]["scene_context"] for ps in self.plan["shots"]]
        self.assertEqual(ctx, ["bridge", "roof", "roof", "bridge", "roof", "bridge"])
        presets = {c: {ps["camera"]["preset"] for ps in self.plan["shots"] if ps["shot"]["scene_context"] == c}
                   for c in ("bridge", "roof")}
        self.assertEqual(presets, {"bridge": {"BRIDGE_THREE_QUARTER"}, "roof": {"LOCKED_THREE_QUARTER"}})
        for a, b in zip(self.plan["shots"], self.plan["shots"][1:]):
            if a["shot"]["scene_context"] != b["shot"]["scene_context"]:
                self.assertEqual(b["cut_from_previous"], "hard")
                self.assertNotEqual(a["camera"]["group"], b["camera"]["group"])
        self.assertEqual(validate.validate_plan(self.plan, self.p), [])

    def test_shared_frames_never_cross_contexts(self):
        x4 = next(c for c in self.plan["coverage"] if c["beat_id"] == "X4")
        self.assertEqual(x4["strategy"], "SEQUENTIAL_STATES")
        self.assertTrue(any("different scene contexts" in e for e in x4["explanation"]))

    def test_context_view_is_a_single_base_states(self):
        st = self.plan["states"]
        roof = spec.context_view(st, "roof")
        self.assertNotIn("contexts", roof)
        self.assertEqual({v["context"] for v in roof["variants"]}, {"roof"})
        self.assertEqual(spec.base_params(roof)["builder"], "rectangular_house_base")
        with self.assertRaises(ValueError):
            spec.shot_states(st, {"id": "SC_X"})
        bad = copy.deepcopy(st)
        bad["variants"][0]["context"] = "tower"
        self.assertTrue(any("not one of" in e for e in spec.validate_states(bad)))

    def test_single_family_projects_keep_schema_2(self):
        for project in (BRIDGE, ROOFS, PILOT):
            plan = plan_of(project)
            self.assertEqual(plan["states"]["schema_version"], 2)
            self.assertNotIn("contexts", plan["states"])
            self.assertTrue(all("scene_context" not in ps["shot"] for ps in plan["shots"]))
            self.assertEqual(plan["states"], read(project / "storyboard/states.json"), project.name)


class GateTest(unittest.TestCase):
    """A technically complete narrated preview is never reported publication-ready."""

    def test_false_publication_ready_status_is_impossible(self):
        from pipeline import gates
        tmp, p = copy_project(PILOT, ignore=("renders", "output", "scenes"))
        try:
            project = read(p / "project.json")
            project["production_profile"] = "PUBLICATION_CANDIDATE"
            project["publication_metadata"] = {"title": "t", "description": "d", "language": "en", "credits": "c"}
            (p / "project.json").write_text(json.dumps(project))
            result = gates.evaluate(p, "_review")
            self.assertNotIn("PUBLICATION_READY", result["statuses"])
            self.assertIn("TTS_RIGHTS_PENDING", result["statuses"])
            self.assertIn("EDITORIAL_REVIEW_PENDING", result["statuses"])
            self.assertNotEqual(result["gates"]["G6 final publication readiness"]["status"], "PASS")
        finally:
            tmp.cleanup()

    def test_internal_narrated_preview_alias(self):
        from pipeline import gates
        self.assertEqual(gates.profile_of({"production_profile": "INTERNAL_NARRATED_PREVIEW"}), "NARRATED_INTERNAL_REVIEW")


if __name__ == "__main__":
    unittest.main()
