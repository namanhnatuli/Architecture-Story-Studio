"""M7 topic-to-review workflow: scaffolding from a synthetic topic, Studio defaults, stage
progression derived from files, resume, and the owner-approval stop (offline; no Blender, no TTS).
This validates the intake and stage tracking only - not an autonomous documentary."""
import json
import shutil
import tempfile
import unittest
from unittest import mock
from datetime import date
from pathlib import Path

from tools import episode
from tools.cli import ROOT

FILM = ROOT / "projects" / "why-bridges-look-different"
TOPIC = "Why traditional Japanese houses use different roof forms"   # synthetic topic fixture
CTA_BEAT = {"id": "B99", "kind": "framing", "claim_ids": [], "sentences": [
    "Which building should we explain next? Suggest a topic in the comments.",
    "And if you enjoyed this film, please like it and subscribe."]}


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def rows_of(p):
    return {stage: (status, detail) for stage, status, detail in episode.stage_status(p)}


class ScaffoldTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / "projects"
        self.p = episode.scaffold(TOPIC, projects_root=self.root, today=date(2026, 11, 1))

    def tearDown(self):
        self.tmp.cleanup()

    def test_topic_only_request_gets_the_studio_defaults(self):
        self.assertEqual(self.p.name, "why-traditional-japanese-houses-use-different-roof")
        project = read(self.p / "project.json")
        d = read(ROOT / "config/production_defaults.json")
        self.assertEqual((project["language"], project["fps"], project["mode"]), ("en", 24, "documentary"))
        self.assertEqual(project["production_profile"], "NARRATED_INTERNAL_REVIEW")
        self.assertEqual(project["chapters"], "script/chapters.json")
        self.assertEqual(d["aspect"], "16:9")
        self.assertEqual(d["duration_minutes"], {"target": [10, 12], "acceptable": [8, 15]})
        self.assertEqual(d["presets"]["final"], "final_4k")
        ep = read(self.p / "episode.json")
        self.assertEqual((ep["topic"], ep["created"]), (TOPIC, "2026-11-01"))
        for f in ("research/sources.json", "research/RESEARCH_BRIEF.md", "assets/manifest.json",
                  "review/FINAL_APPROVAL_CHECKLIST.md", "renders/.gitkeep", "output/.gitkeep"):
            self.assertTrue((self.p / f).is_file(), f)
        self.assertIn(TOPIC, (self.p / "research/RESEARCH_BRIEF.md").read_text())
        self.assertEqual(read(self.p / "research/sources.json")["claims"], [])   # nothing invented

    def test_no_bridge_material_leaks_into_a_new_episode(self):
        text = " ".join(f.read_text() for f in self.p.rglob("*") if f.is_file())
        for leak in ("CLM_7", "bridge", "voussoir", "Carrollton", "B35"):
            self.assertNotIn(leak, text, leak)

    def test_existing_projects_and_bad_slugs_are_refused(self):
        with self.assertRaises(SystemExit):
            episode.scaffold(TOPIC, projects_root=self.root)
        for slug in ("../escape", "A B", ""):
            with self.assertRaises(SystemExit):
                episode.scaffold(TOPIC, slug=slug or "x" * 70, projects_root=self.root)

    def test_fresh_project_waits_for_research_by_the_agent(self):
        rows = rows_of(self.p)
        self.assertEqual(rows["TOPIC"][0], "DONE")
        self.assertEqual(rows["RESEARCH"][0], "TODO")
        nxt = episode.next_stage(episode.stage_status(self.p))
        self.assertEqual((nxt["stage"], nxt["who"]), ("RESEARCH", "AGENT"))

    def test_stages_advance_from_files_and_resume_is_idempotent(self):
        src = {"sources": [{"id": "SRC_X", "title": "t", "url": "https://example.org"}],
               "claims": [{"id": "CLM_1", "text": "x", "review_status": "SOURCE_VERIFIED"},
                          {"id": "CLM_2", "text": "y", "review_status": "PROVISIONAL"}]}
        (self.p / "research/sources.json").write_text(json.dumps(src))
        self.assertEqual(rows_of(self.p)["RESEARCH"][0], "DONE")
        narration = {"beats": [{"id": "B01", "sentences": ["x"], "claim_ids": ["CLM_1", "CLM_2"]}, CTA_BEAT]}
        (self.p / "script/narration.json").write_text(json.dumps(narration))
        (self.p / "script/visual_beats.json").write_text(json.dumps({"beats": []}))
        (self.p / "script/chapters.json").write_text(json.dumps({"schema": "chapters/1", "chapters": [
            {"id": "C1", "title": "Hook", "beat_ids": ["B01", "B99"]}]}))
        rows = rows_of(self.p)
        self.assertEqual(rows["SCRIPT"][0], "DONE")
        self.assertEqual(rows["CLAIM_SOURCE_VERIFICATION"][0], "BLOCKED")
        self.assertIn("CLM_2", rows["CLAIM_SOURCE_VERIFICATION"][1])
        src["claims"][1]["review_status"] = "SOURCE_VERIFIED"
        (self.p / "research/sources.json").write_text(json.dumps(src))
        first = episode.stage_status(self.p)
        self.assertEqual(first, episode.stage_status(self.p))   # resume: same answer, nothing changed on disk
        nxt = episode.next_stage(first)
        self.assertEqual((nxt["stage"], nxt["who"]), ("TTS", "CLI"))

    def test_new_episodes_must_close_with_a_call_to_action(self):
        # 2026-11-05: the owner asked that every film end by inviting viewers to suggest topics, like and subscribe
        cta = read(self.p / "episode.json")["defaults"]["closing_call_to_action"]
        self.assertTrue(cta["required"])
        self.assertEqual(set(cta["asks"]), {"suggest a topic", "in the comments", "like", "subscribe"})
        fact = {"id": "B01", "kind": "fact", "sentences": ["x"], "claim_ids": ["CLM_1"]}
        (self.p / "research/sources.json").write_text(json.dumps({"sources": [{"id": "S", "title": "t", "url": "u"}],
                                                                    "claims": [{"id": "CLM_1", "text": "x", "review_status": "SOURCE_VERIFIED"}]}))
        (self.p / "script/visual_beats.json").write_text(json.dumps({"beats": []}))

        def script(beats, chapters):
            (self.p / "script/narration.json").write_text(json.dumps({"beats": beats}))
            (self.p / "script/chapters.json").write_text(json.dumps({"chapters": chapters}))
            return rows_of(self.p)["SCRIPT"]

        two = [{"id": "C1", "beat_ids": ["B01"]}, {"id": "C2", "beat_ids": ["B99"]}]
        status, detail = script([fact], [{"id": "C1", "beat_ids": ["B01"]}])
        self.assertEqual(status, "BLOCKED")
        self.assertIn("closing call to action missing", detail)
        self.assertEqual(script([fact, CTA_BEAT], two)[0], "DONE")
        # only part of the ask, a claim on it, a fact after it, a call in an earlier chapter, too long: refused
        partial = dict(CTA_BEAT, sentences=["Please like this video and subscribe."])
        self.assertIn("missing", script([fact, partial], two)[1])
        self.assertIn("without claims", script([fact, dict(CTA_BEAT, claim_ids=["CLM_1"])], two)[1])
        self.assertIn("before the end of the argument", script([CTA_BEAT, fact], [{"id": "C1", "beat_ids": ["B99", "B01"]}])[1])
        self.assertIn("missing", script([CTA_BEAT, fact], [{"id": "C1", "beat_ids": ["B99"]}, {"id": "C2", "beat_ids": ["B01"]}])[1])
        long = dict(CTA_BEAT, sentences=CTA_BEAT["sentences"] + ["word " * 60])
        self.assertIn("words (max", script([fact, long], two)[1])

    def test_projects_created_before_the_call_to_action_rule_are_not_rechecked(self):
        self.assertNotIn("closing call to action", rows_of(FILM)["SCRIPT"][1])   # reference film: no episode.json
        ep = read(self.p / "episode.json")
        del ep["defaults"]["closing_call_to_action"]
        (self.p / "episode.json").write_text(json.dumps(ep))
        self.assertEqual(episode.call_to_action_problems(self.p, {"beats": [{"id": "B01", "sentences": ["x"]}]},
                                                         [{"id": "C1", "beat_ids": ["B01"]}]), [])


class ScriptReviewTest(unittest.TestCase):
    def test_the_owner_reads_the_narrated_sentences_with_their_visual_status(self):
        from tools import script_review
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "film"
            for d in ("script", "research", "qa", "review"):
                (p / d).mkdir(parents=True)
            write = lambda rel, data: (p / rel).write_text(json.dumps(data))   # noqa: E731
            write("project.json", {"title": "A film"})
            write("script/narration.json", {"revision": {"version": "x-r1"}, "beats": [
                {"id": "B01", "kind": "fact", "claim_ids": ["CLM_1"], "sentences": ["Beauvais fell.", "It stood high."]},
                {"id": "B02", "kind": "framing", "claim_ids": [], "sentences": ["Thanks."]}]})
            write("script/visual_beats.json", {"beats": [
                {"beat_id": "B01", "visual_goal": "A model", "annotations": [{"type": "NOTE", "text": "Illustrative model"}]},
                {"beat_id": "B02", "strategy": "CARD", "visual_goal": "Credits",
                 "graphic": {"elements": [{"kind": "text", "text": "The end"}, {"kind": "line"}]}}]})
            write("script/chapters.json", {"chapters": [{"id": "C1", "title": "One", "beat_ids": ["B01", "B02"]}]})
            write("script/timing.json", {"pacing": {"beat_lead_in_seconds": 0.5, "beat_tail_seconds": 0.5}, "beats": [
                {"id": "B01", "duration": 60.0, "sentences": [{"index": 0, "text": "Beauvais fell.", "start": 1.0}]},
                {"id": "B02", "duration": 9.0, "sentences": []}]})
            write("research/sources.json", {"claims": [{"id": "CLM_1", "text": "It fell.", "confidence": "medium",
                                                        "source_ids": ["SRC_A"], "assumptions": "A caveat."}]})
            write("qa/visual_coverage.json", {"beats": [{"beat_id": "B01", "status": "MISSING_ASSET"}, {"beat_id": "B02", "status": "COVERED"}]})
            write("script/pronunciation.json", {"entries": [{"written": "Beauvais", "respelling": "boh-VAY", "status": "PENDING_LISTENING_REVIEW"}]})
            (p / "review/SCRIPT_REVIEW_NOTES.md").write_text("## Decide this")
            doc = script_review.build(p)
        for want in ("`x-r1`", "1.2 phút", "> Beauvais fell. It stood high.", "3D, cần bộ sinh mới", "sơ đồ/card 2D", "The end",
                     "Illustrative model", "| CLM_1 | medium | It fell. | SRC_A | A caveat. |", "## Decide this",
                     "boh-VAY | 0:01 (B01.s0)", "chưa claim nào được duyệt biên tập"):
            self.assertIn(want, doc)
        self.assertLess(doc.index("## Decide this"), doc.index("## Toàn bộ kịch bản"))

    def test_runs_of_cards_with_only_words_are_measured(self):
        from tools.script_review import text_only_runs
        words = {"strategy": "CARD", "graphic": {"elements": [{"kind": "text"}, {"kind": "line", "points": [[0, 0], [1, 0]]}]}}
        drawing = {"strategy": "CARD", "graphic": {"elements": [{"kind": "text"}, {"kind": "arrow"}]}}
        visuals = {"A": words, "B": words, "C": drawing, "D": {"strategy": "HOLD"}, "E": words}
        windows = {k: (i * 10.0, i * 10.0 + 10.0) for i, k in enumerate("ABCDE")}
        self.assertEqual(text_only_runs(list("ABCDE"), visuals, windows), [(["A", "B"], 20.0), (["E"], 10.0)])


class GothicFilmTest(unittest.TestCase):
    """The film stops at the owner's script review: nothing may look approved or rendered."""
    P = ROOT / "projects" / "gothic-cathedral-heights"

    def test_script_stage_is_done_and_nothing_is_approved(self):
        rows = rows_of(self.P)
        for stage in ("RESEARCH", "SCRIPT", "CLAIM_SOURCE_VERIFICATION", "TTS", "AUDIO_LOCK"):
            self.assertEqual(rows[stage][0], "DONE", (stage, rows[stage]))
        self.assertEqual(rows["VISUAL_PLAN"][0], "DONE")   # the cathedral family (engine/arch/families/cathedral.py)
        n = read(self.P / "script/narration.json")
        self.assertEqual(n["voice"]["license"]["status"], "LICENSE_REVIEW_REQUIRED")
        self.assertEqual(n["voice"]["license"]["owner_confirmation_for_this_film"], "PENDING")
        self.assertEqual(n["voice"]["pronunciation_review"]["status"], "PENDING")
        self.assertEqual({e["status"] for e in read(self.P / "script/pronunciation.json")["entries"]}, {"PENDING_LISTENING_REVIEW"})
        self.assertEqual({c["review_status"] for c in read(self.P / "research/sources.json")["claims"]}, {"SOURCE_VERIFIED"})
        self.assertEqual(read(self.P / "project.json")["production_profile"], "NARRATED_INTERNAL_REVIEW")
        self.assertFalse((self.P / "review/OWNER_APPROVALS.json").exists())
        self.assertFalse((self.P / "research/editorial_approval.json").exists())
        # the owner asked for a 720p internal review; every video must say so, and no final may exist
        for video in self.P.glob("output/*.mp4"):
            self.assertIn("INTERNAL", video.name.upper())
        self.assertEqual(list(self.P.glob("output/*FINAL*")), [])

    def test_a_match_cut_never_moves_the_camera(self):
        """A match cut promises the same view. SC_012 to SC_013 once jumped because the framing differed."""
        plan = read(self.P / "storyboard/visual_plan.json")
        matches = [(a, b) for a, b in zip(plan["shots"], plan["shots"][1:]) if b["cut_from_previous"] == "match"]
        self.assertTrue(matches)
        for a, b in matches:
            self.assertEqual(a["camera"]["preset"], b["camera"]["preset"], b["shot"]["id"])
            self.assertEqual(a["shot"].get("camera_focus"), b["shot"].get("camera_focus"), b["shot"]["id"])

    def test_b13_names_the_ribs_then_lights_the_web(self):
        """Ribs and web lit together wash out: the ribs must stay readable while the web is lit."""
        shots = {s["beat_id"]: s for s in read(self.P / "storyboard/visual_plan.json")["shots"]}
        b12, b13 = shots["B12"], shots["B13"]
        self.assertEqual(b13["cut_from_previous"], "match")
        self.assertEqual(b12["shot"]["camera_focus"], b13["shot"]["camera_focus"])
        glow = b13["shot"]["animation"]["highlight"]
        self.assertTrue(glow["components"])
        self.assertTrue(all("vault_web" in c for c in glow["components"]), glow["components"])
        timing = {b["id"]: b for b in read(self.P / "script/timing.json")["beats"]}["B13"]
        carries_load = timing["sentences"][2]
        self.assertIn("carries load", carries_load["text"])
        self.assertAlmostEqual(glow["start_seconds"], carries_load["rel_start"], delta=1.0)

    def test_runtime_is_the_owners_and_within_it(self):
        decision = read(self.P / "project.json")["runtime_decision"]
        self.assertEqual(decision["acceptable_minutes"], [10, 18])
        self.assertIn("10–18", decision["basis"])
        t = read(self.P / "script/timing.json")
        pad = t["pacing"]["beat_lead_in_seconds"] + t["pacing"]["beat_tail_seconds"]
        minutes = sum(b["duration"] + pad for b in t["beats"]) / 60
        self.assertTrue(10 <= minutes <= 18, minutes)

    def test_published_heights_are_given_with_their_disagreement(self):
        text = " ".join(s for b in read(self.P / "script/narration.json")["beats"] for s in b["sentences"])
        self.assertIn("more than 45 meters", text)   # the wording that every published figure supports
        self.assertNotIn("nearly 47", text)
        self.assertIn("more than 42 meters", text)
        self.assertNotIn("48.5", text)
        cards = (self.P / "script/visual_beats.json").read_text()
        self.assertIn("46 m to above 48 m", cards)
        self.assertIn("46 m, 46.7 m, nearly 47 m,", cards)
        self.assertIn("above 48 m", cards)
        # sources disagree on who was "first": the film does not say so for Chartres or Durham
        self.assertIn("part of the original plans", text)
        self.assertNotIn("first time", text)
        self.assertNotIn("very first", text)

    def test_the_owners_script_review_stays_applied(self):
        # The owner's review of g-r1 (2026-11-05): statements must keep their conditions.
        beats = {b["id"]: b for b in read(self.P / "script/narration.json")["beats"]}
        said = {k: " ".join(b["sentences"]) for k, b in beats.items()}
        text = " ".join(said.values())
        # 1: the pointed arch is no general rule; the garbled Columbia sentence carries nothing
        self.assertIn("can rise higher", said["B08"])
        self.assertIn("not to every arch", said["B08"])
        self.assertIn("of two other arches", said["B08"])   # the arches drawn on the card are not the study's
        self.assertIn("same weights", said["B09"])
        self.assertNotIn("more efficient", text)
        self.assertNotIn("CLM_133", {c for b in beats.values() for c in b["claim_ids"]})
        # 2: thrust line and models under their assumptions, no general safety standard
        self.assertIn("idealized arch", said["B40"])
        for assumption in ("no pulling", "never slide", "never crush"):
            self.assertIn(assumption, said["B40"])
        self.assertIn("does not show a whole real building is safe", said["B41"])
        self.assertNotIn("What matters most", text)
        # 3: the builders are not described as ignorant
        self.assertNotIn("no knowledge", text)
        for b in ("B03", "B25"):
            self.assertIn("without modern structural calculations", said[b])
        # 4: one kind of vault, and the stone between the ribs works too
        self.assertIn("four-part vault shown here", said["B12"])
        self.assertIn("simplified picture", said["B12"])
        self.assertIn("carries load", said["B13"])
        self.assertIn("main support", said["B15"])
        # 6: Durham's dates belong to the building, not to the vaults
        self.assertIn("begun in 1093", said["B14"])
        self.assertNotIn("as early as 1093", text)
        # second review: Cluny likewise; 1088 dates the building, and no year is given for the arches
        self.assertIn("whose construction began around 1088", said["B10"])
        cards = {b["beat_id"]: [e["text"] for e in b["graphic"]["elements"] if e["kind"] == "text"]
                 for b in read(self.P / "script/visual_beats.json")["beats"] if b.get("graphic")}
        for b in ("B10", "B14"):
            self.assertIn("1088  Cluny III: construction begins", cards[b])
        # second review: no percentages under the arches of B08
        self.assertFalse([w for w in cards["B08"] if "%" in w])
        self.assertTrue(any("not the arches of the study" in w for w in cards["B08"]))
        # second review: a pacing choice; Stalley's remark stays in the sources and is not spoken
        self.assertNotIn("Stalley", text)
        ledger = {c["id"]: c for c in read(self.P / "research/sources.json")["claims"]}
        self.assertIn("Stalley", ledger["CLM_144"]["text"])
        self.assertNotIn("CLM_144", {c for b in beats.values() for c in b["claim_ids"]})
        # second review: a claim is no wider than the narration it backs
        self.assertNotIn("stopped fighting", ledger["CLM_123"]["text"])
        self.assertIn("rearranged", ledger["CLM_123"]["text"])
        # second review: a badly drawn line proves nothing; B40 shows a real change of the supports
        self.assertIn("many such lines", said["B40"])
        self.assertIn("move its supports apart", said["B40"])
        self.assertIn("Many lines can fit. One is enough", cards["B40"])
        self.assertFalse([w for w in cards["B40"] if "No line fits" in w])
        self.assertTrue(any("Fig. 5, recalculated by Ochsendorf's 2002 method" in w for w in cards["B40"]))
        # the sources the owner asked for: Cluny's pointed arches and the three bays no longer rest on the association alone
        self.assertIn("SRC_HARVARD_CLUNY", ledger["CLM_131"]["source_ids"])
        self.assertIn("SRC_CU_MURRAY_COLLAPSE", ledger["CLM_185"]["source_ids"])
        # remarks: no dark Romanesque, no long debate of names
        self.assertNotIn("dark", said["B06"])
        self.assertIn("type shown here", said["B06"])
        self.assertNotIn("Timbert", text)
        self.assertNotIn("PRON_TIMBERT", {e["id"] for e in read(self.P / "script/pronunciation.json")["entries"]})
        # B35: each cause is a labelled hypothesis, and the 2024 argument carries its authors
        card = next(b for b in read(self.P / "script/visual_beats.json")["beats"] if b["beat_id"] == "B35")
        words = [e["text"] for e in card["graphic"]["elements"] if e["kind"] == "text"]
        self.assertEqual(sum(w.startswith("Hypothesis:") for w in words), 3)
        self.assertTrue(any(w.startswith("Their hypothesis:") for w in words))
        self.assertTrue(any("Vernhes, Renault and Zotna" in w for w in words))

    def test_a_sentence_that_names_a_source_cites_that_source(self):
        # Verbatim excerpts do not catch a sentence attributed to a source its beat never cites (B22 in g-r1).
        marks = {"Columbia": "SRC_CU_", "national library": "SRC_BNF_", "MIT": "SRC_MIT_", "Heyman": "SRC_MIT_BLOCK",
                 "Murray": "SRC_ISSMGE", "2024 study": "SRC_ISSMGE", "Viollet-le-Duc": "SRC_ISSMGE"}
        claims = {c["id"]: c for c in read(self.P / "research/sources.json")["claims"]}
        seen = set()
        for b in read(self.P / "script/narration.json")["beats"]:
            sources = {s for c in b["claim_ids"] for s in claims[c]["source_ids"]}
            for sentence in b["sentences"]:
                for name, prefix in marks.items():
                    if name in sentence:
                        seen.add(name)
                        self.assertTrue(any(s.startswith(prefix) for s in sources), (b["id"], name))
        self.assertEqual(seen, set(marks))


class GothicThrustLineTest(unittest.TestCase):
    """The geometry of card B40 comes from a port of Ochsendorf's program ArchSpread (Cambridge PhD, 2002). It must keep
    reproducing his published results and agreeing with the example of Block, DeJong and Ochsendorf 2006, figure 5."""
    T, HALF = 0.1524, 80.0

    @classmethod
    def setUpClass(cls):
        import importlib.util
        spec = importlib.util.spec_from_file_location("arch_statics", GothicFilmTest.P / "script/arch_statics.py")
        cls.a = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.a)

    def test_thesis_table_5_3_small_voussoirs(self):
        s = self.a.spread_to_collapse(60, 0.10, 0.1)
        self.assertAlmostEqual(s["initial_hinge"], 53.8, places=1)
        self.assertAlmostEqual(s["hinge"], 42.7, delta=0.15)
        self.assertAlmostEqual(s["span_increase"] * 100, 8.2, delta=0.05)
        self.assertAlmostEqual(s["thrust_ratio"], 2.16, delta=0.01)
        self.assertAlmostEqual(s["dip"], 1.73, delta=0.03)

    def test_thesis_hinge_movements_at_minimum_thickness(self):
        for half, end in ((80, 52.2), (60, 43.2)):
            s = self.a.spread_to_collapse(half, 0.1075, 0.1)
            self.assertAlmostEqual(s["initial_hinge"], 54.5, places=1)
            self.assertAlmostEqual(s["hinge"], end, places=1)

    def test_block_figure_4_range_of_thrust(self):
        total = 2 * self.a.half_weight(90, 0.18)
        valid = self.a.thrust_range(90, 0.18)
        self.assertAlmostEqual(valid["min"][1] / total, 0.16, delta=0.005)
        self.assertAlmostEqual(valid["max"][1] / total, 0.25, delta=0.01)

    def test_block_figure_5_arch_on_spreading_supports(self):
        a = self.a
        self.assertAlmostEqual(a.thrust_range(self.HALF, self.T)["min"][1] / (2 * a.half_weight(self.HALF, self.T)), 0.198, delta=0.003)
        s = a.spread_to_collapse(self.HALF, self.T)
        self.assertAlmostEqual(s["span_increase"], 0.1149, delta=0.004)
        self.assertAlmostEqual(s["thrust_ratio"] - 1, 0.851, delta=0.02)
        self.assertAlmostEqual(s["hinge"], 54.4, delta=0.6)
        self.assertAlmostEqual(a.spread_to_collapse(self.HALF, self.T, stop_at=0.05)["thrust_ratio"] - 1, 0.2459, delta=0.025)

    def test_the_lines_on_the_card_are_valid_and_the_limit_is_real(self):
        a = self.a
        for crown, h in a.thrust_range(self.HALF, self.T).values():
            self.assertTrue(a.fits(a.line_radii(self.HALF, self.T, crown, h)[0], self.T))
        ri, ro = 1 - self.T / 2, 1 + self.T / 2
        # two separate calculations of the collapse: the capacity of the support part, and the pressure points on the joints
        s = a.spread_to_collapse(self.HALF, self.T)
        self.assertAlmostEqual(s["thrust"] / s["capacity"], 1.0, delta=0.005)
        shape = a.spread_shape(self.HALF, self.T, s)
        self.assertAlmostEqual(shape["radii"][-1], ro, delta=0.001)        # the locus reaches the extrados at the support
        self.assertGreaterEqual(min(shape["radii"]), ri - 0.0005)          # and never leaves the stone before that
        self.assertLessEqual(max(shape["radii"]), ro + 0.0005)
        self.assertAlmostEqual(shape["crown"][0], 0.0, places=6)           # the crown hinge stays on the axis
        self.assertAlmostEqual(shape["lower"](0, 0)[0], s["shift"])
        moving = a.spread_to_collapse(self.HALF, self.T, stop_at=0.05)
        self.assertGreater(moving["hinge"], s["hinge"])                    # the hinge moves toward the crown as it spreads
        with self.assertRaises(ValueError):                                # an arch too thin has no valid line
            a.thrust_range(90, 0.09)


class OwnerStopTest(unittest.TestCase):
    def test_reference_film_records_the_owner_approval_of_its_m8_revision(self):
        # M8 (2026-10-31): the owner's approvals of m7-r1 did not cover the remade film, so the workflow
        # stopped for the owner. 2026-11-04: the owner approved the claims and pronunciations of m8-r4
        # (APP-M8.4-CLAIMS-AND-PRONUNCIATION); the stop is exercised on a copy below.
        rows = rows_of(FILM)
        for stage in ("TOPIC", "RESEARCH", "SCRIPT", "CLAIM_SOURCE_VERIFICATION", "TTS", "AUDIO_LOCK", "VISUAL_PLAN",
                      "OWNER_APPROVAL", "PUBLICATION_CANDIDATE"):
            self.assertEqual(rows[stage][0], "DONE", (stage, rows[stage]))
        ids = [d["id"] for d in read(FILM / "review/OWNER_APPROVALS.json")["decisions"]]
        for want in ("REQ-M8-ALL-FAMILIES", "APP-M8.4-CLAIMS-AND-PRONUNCIATION"):
            self.assertIn(want, ids)

    def test_without_owner_decisions_the_workflow_stops_for_the_owner(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / FILM.name
            shutil.copytree(FILM, p, ignore=shutil.ignore_patterns("renders", "scenes", "audio", "chapters_*",
                                                                   "baseline_*", "*.wav", "*.mp4"))
            shutil.copytree(FILM / "audio", p / "audio", ignore=shutil.ignore_patterns("*.wav"))
            (p / "output" / "why_bridges_look_different_documentary_INTERNAL_REVIEW.mp4").write_bytes(b"placeholder")
            (p / "review/OWNER_APPROVALS.json").unlink()
            n = read(p / "script/narration.json")
            n["voice"]["pronunciation_review"]["status"] = "PENDING"
            (p / "script/narration.json").write_text(json.dumps(n))
            rows = rows_of(p)
            self.assertEqual(rows["INTERNAL_REVIEW"][0], "DONE")
            self.assertEqual(rows["OWNER_APPROVAL"][0], "WAITING_FOR_OWNER")
            self.assertNotEqual(rows["PUBLICATION_CANDIDATE"][0], "DONE")
            nxt = episode.next_stage(episode.stage_status(p))
            self.assertEqual((nxt["stage"], nxt["who"]), ("OWNER_APPROVAL", "OWNER"))


class CliEpisodeCommandsTest(unittest.TestCase):
    def test_project_defaults_to_the_only_active_project(self):
        from tools import cli
        with tempfile.TemporaryDirectory() as tmp, mock.patch.object(cli, "ROOT", Path(tmp)):
            for slug in ("first-film", "second-film"):
                (Path(tmp) / "projects" / slug).mkdir(parents=True)
                (Path(tmp) / "projects" / slug / "project.json").write_text("{}")
                if slug == "first-film":
                    self.assertEqual(cli.default_project(), "first-film")
            with self.assertRaises(SystemExit):   # two projects: --project is required
                cli.default_project()

    def test_new_episode_and_episode_status_delegate_to_the_episode_tool(self):
        from tools import cli
        with mock.patch.object(episode, "main") as main, \
                mock.patch("sys.argv", ["cli.py", "new-episode", "--topic", TOPIC]):
            cli.main()
        main.assert_called_once_with(["new", "--topic", TOPIC])
        with mock.patch.object(episode, "main") as main, \
                mock.patch("sys.argv", ["cli.py", "episode-status", "--project", FILM.name]):
            cli.main()
        main.assert_called_once_with(["status", "--project", FILM.name])
        with mock.patch("sys.argv", ["cli.py", "new-episode"]), self.assertRaises(SystemExit):
            cli.main()


if __name__ == "__main__":
    unittest.main()
