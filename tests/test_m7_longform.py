"""M7: the first full-length documentary - chapters, mixed 2D/3D cards, archival image rights,
word-timed card elements, push-ins, NOTE captions, render-cache scope, interrupted-render
recovery, long-form QA and the INTERNAL REVIEW gates (offline; no Blender, no TTS).
M8: the film now covers all six structural families (revision m8-r1, 11 chapters); the owner's
approvals of m7-r1 (tag m7-final-4k) do not carry over, so the approval logic is exercised on a
temporary copy where the owner decisions are simulated (owner_approved_copy), never on the real records."""
import copy
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from engine import framing, motion, templates
from pipeline import chapters as CH, gates, narration as nar, pronunciation as pron
from planner import annotations as AN, planner as pl, timing as T, vocabulary as V
from tools import cli, render_cache, validator
from tools.cli import ROOT

FILM = ROOT / "projects" / "why-bridges-look-different"
FAKE_PNG = b"\x89PNG\r\n\x1a\n" + b"\x00" * 16 + cli.PNG_END


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def copy_film(ignore=("renders", "output", "scenes", "qa", "audio")):
    tmp = tempfile.TemporaryDirectory()
    dst = Path(tmp.name) / FILM.name
    shutil.copytree(FILM, dst, ignore=shutil.ignore_patterns(*ignore))
    return tmp, dst


def owner_approved_copy(ignore=("renders", "output", "scenes", "qa", "*.wav", "*.m4a")):
    """A temporary copy of the film with every owner decision SIMULATED for the current revision
    (claims, pronunciation, factual review, publication-candidate profile): only to test the gate
    logic. The real film's records are never written."""
    from pipeline import pronunciation as pron
    tmp, p = copy_film(ignore)   # the audio manifest stays: output_label checks the narration rights
    n = read(p / "script/narration.json")
    src = read(p / "research/sources.json")
    used = {c for b in n["beats"] for c in b["claim_ids"]}
    for c in src["claims"]:
        if c["id"] in used:
            c["review_status"] = "EDITORIALLY_APPROVED"
            c["editorial_approval"] = {"approved_by": "TEST OWNER (simulated)", "approved_on": "2099-01-01",
                                       "narration_revision": n["revision"]["version"], "basis": "unit test"}
    (p / "research/sources.json").write_text(json.dumps(src))
    lex_path = p / "script/pronunciation.json"   # M8.2: speech-only overrides need a listener too
    if lex_path.is_file():
        lex = read(lex_path)
        for e in lex["entries"]:
            e.update(status="CONFIRMED", confirmed_by="TEST OWNER (simulated)", confirmed_on="2099-01-01")
        lex_path.write_text(json.dumps(lex))
    n["voice"]["pronunciation_review"].update(
        status="ACCEPTED_BY_OWNER", accepted_by="TEST OWNER (simulated)", accepted_on="2099-01-01",
        basis="unit test. No per-item listening session or phonetic verification is recorded here.",
        audio_revision=nar.narration_hash(n, pron.load(p)))
    (p / "script/narration.json").write_text(json.dumps(n))
    project = read(p / "project.json")
    project.update(factual_review="verified", production_profile="PUBLICATION_CANDIDATE")
    (p / "project.json").write_text(json.dumps(project))
    return tmp, p


class ChapterStructureTest(unittest.TestCase):
    def setUp(self):
        self.doc = read(FILM / "script/chapters.json")
        self.narration = read(FILM / "script/narration.json")
        self.beats = read(FILM / "script/visual_beats.json")

    def test_film_chapters_are_valid_and_ordered(self):
        self.assertEqual(CH.validate(self.doc, self.narration, self.beats), [])
        self.assertEqual([c["id"] for c in self.doc["chapters"]], [f"C{i}" for i in range(1, 13)])   # M8.1: 12 chapters
        flat = [b for c in self.doc["chapters"] for b in c["beat_ids"]]
        self.assertEqual(flat, [b["id"] for b in self.narration["beats"]])

    def test_missing_duplicate_and_reordered_beats_fail(self):
        d = copy.deepcopy(self.doc)
        d["chapters"][1]["beat_ids"].pop()
        self.assertTrue(any("in no chapter" in e for e in CH.validate(d, self.narration)))
        d = copy.deepcopy(self.doc)
        d["chapters"][2]["beat_ids"].append(d["chapters"][1]["beat_ids"][0])
        self.assertTrue(any("is in chapters" in e for e in CH.validate(d, self.narration)))
        d = copy.deepcopy(self.doc)
        d["chapters"][0], d["chapters"][1] = d["chapters"][1], d["chapters"][0]
        self.assertTrue(any("narration order" in e for e in CH.validate(d, self.narration)))

    def test_empty_untitled_or_duplicate_chapters_fail(self):
        d = copy.deepcopy(self.doc)
        d["chapters"].append({"id": "C1", "title": " ", "beat_ids": []})
        errors = CH.validate(d, self.narration)
        for want in ("duplicate chapter id C1", "has no title", "has no beats"):
            self.assertTrue(any(want in e for e in errors), want)
        self.assertEqual(CH.validate(None, self.narration), ["chapters file missing"])

    def test_visual_beat_chapter_must_agree(self):
        b = copy.deepcopy(self.beats)
        b["beats"][0]["chapter"] = "C5"
        self.assertTrue(any("chapters.json says C1" in e for e in CH.validate(self.doc, self.narration, b)))

    def test_chapters_are_contiguous_frame_ranges_of_the_locked_timing(self):
        timing = read(FILM / "script/timing.json")
        ranges, errors = CH.shot_ranges(self.doc, timing)
        self.assertEqual(errors, [])
        self.assertEqual(sum(r["frames"] for r in ranges.values()), timing["total_frames"])
        starts = [r["start_frame"] for r in ranges.values()]
        self.assertEqual(starts, sorted(starts))

    def test_a_shot_shared_by_two_chapters_is_refused(self):
        timing = read(FILM / "script/timing.json")
        t = copy.deepcopy(timing)
        first_c2 = self.doc["chapters"][1]["beat_ids"][0]
        t["shots"][0]["beat_ids"] = t["shots"][0]["beat_ids"] + [first_c2]
        _, errors = CH.shot_ranges(self.doc, t)
        self.assertTrue(any("belongs to chapters" in e for e in errors))

    def test_documentary_mode_requires_valid_chapters(self):
        tmp, p = copy_film()
        with tmp:
            project = read(p / "project.json")
            project.pop("chapters")
            (p / "project.json").write_text(json.dumps(project))
            errors, _ = validator.validate_project(p)
            self.assertTrue(any("documentary mode needs project.chapters" in e for e in errors))


class RuntimeAndEvidenceTest(unittest.TestCase):
    def test_runtime_is_within_the_long_form_range(self):
        timing = read(FILM / "script/timing.json")
        self.assertTrue(timing["locked"])
        lo, hi, decision = CH.runtime_range(FILM)
        self.assertGreaterEqual(timing["total_seconds"], lo)
        self.assertLessEqual(timing["total_seconds"], hi)
        if decision:   # M8.1: the owner relaxed the runtime for this film; the record must be complete
            self.assertIn("Tran Nam Anh", decision["decided_by"])
            self.assertIn("không cần quá khắt khe về mặt thời gian", decision["basis"])

    def test_the_owner_approval_is_bound_to_the_m8_r4_narration_and_claim_texts(self):
        # The owner approved 41 claims of m7-r1 on 2026-10-30 (kept in git history and OWNER_APPROVALS.json); that
        # did not cover the remade film. On 2026-11-04 the owner approved the 76 claims m8-r4 narrates; the
        # 6 registry claims it does not narrate stay SOURCE_VERIFIED.
        import hashlib
        claims = {c["id"]: c for c in read(FILM / "research/sources.json")["claims"]}
        narration = read(FILM / "script/narration.json")
        used = {c for b in narration["beats"] for c in b["claim_ids"]}
        record = read(FILM / "research/editorial_approval.json")
        self.assertEqual((record["narration_revision"], len(record["claims"])), ("m8-r4", 76))
        self.assertEqual(narration["revision"]["version"], "m8-r4")
        self.assertIn("Tran Nam Anh", record["approved_by"])
        self.assertEqual(record["previous"]["narration_revision"], "m7-r1")
        self.assertEqual(set(record["claims"]), used)
        self.assertEqual(record["narration_sha256"], nar.narration_hash(narration, pron.load(FILM)))
        for cid in used:   # approval lapses if a claim text changes
            self.assertEqual(record["claims_text_sha256"][cid], hashlib.sha256(claims[cid]["text"].encode()).hexdigest(), cid)
            self.assertEqual(claims[cid]["review_status"], "EDITORIALLY_APPROVED", cid)
            self.assertEqual(claims[cid]["editorial_approval"]["narration_revision"], "m8-r4", cid)
        self.assertEqual({c for c, v in claims.items() if v["review_status"] == "SOURCE_VERIFIED"}, set(claims) - used)
        self.assertEqual(set(claims) - used, {"CLM_730", "CLM_731", "CLM_732", "CLM_747", "CLM_755", "CLM_762"})
        new = {c for c in used if c >= "CLM_750"}
        self.assertTrue(new and new <= set(claims))
        for c in claims.values():
            self.assertTrue(c["evidence"] and all(e["excerpt"] for e in c["evidence"]), c["id"])

    def test_changed_wording_invalidates_the_approval(self):
        tmp, p = owner_approved_copy()
        with tmp:
            self.assertFalse(any("approval is for narration" in e for e in validator.validate_project(p)[0]))
            n = read(p / "script/narration.json")
            n["revision"]["version"] = "m8-r5"
            (p / "script/narration.json").write_text(json.dumps(n))
            errors, _ = validator.validate_project(p)
            self.assertTrue(any("approval is for narration 'm8-r4'" in e for e in errors))

    def test_am_michael_approval_is_the_owners_and_project_scoped(self):
        # Approved by the owner on 2026-10-30 for this documentary only (finalization request, section 3.2).
        from integrations.tts import providers
        n = read(FILM / "script/narration.json")
        voice, lic = n["voice"], n["voice"]["license"]
        self.assertEqual((voice["voice"], voice["params"]["lang_code"]), ("am_michael", "a"))
        self.assertEqual(lic["status"], "APPROVED")
        self.assertIn("Tran Nam Anh", lic["approved_by"])
        self.assertEqual(lic["owner_confirmation_for_this_film"], "CONFIRMED")
        registry = providers.load_registry()
        clearance = registry["providers"]["kokoro"]["clearance"]
        self.assertNotIn("am_michael", clearance["voices_cleared"])   # not a channel-wide clearance
        approval = next(a for a in clearance["voice_approvals"] if a["voice"] == "am_michael")
        self.assertEqual(approval["projects"], ["why-bridges-look-different"])
        self.assertEqual(approval["voice_sha256"], registry["providers"]["kokoro"]["voices"]["am_michael"])
        sources = read(FILM / "research/sources.json")
        self.assertEqual(nar.validate(n, sources, registry, project_id="why-bridges-look-different"), [])
        errors = nar.validate(n, sources, registry, project_id="another-documentary")   # scope is enforced
        self.assertTrue(any("not covered by the provider clearance" in e for e in errors))
        unapproved = copy.deepcopy(n)
        unapproved["voice"].update(voice="am_puck", id="kokoro_am_puck")
        errors = nar.validate(unapproved, sources, registry, project_id="why-bridges-look-different")
        self.assertTrue(any("'am_puck' is not covered" in e for e in errors))

    def test_pronunciation_acceptance_is_bound_to_the_audio_revision(self):
        from pipeline import pronunciation as pron
        n = read(FILM / "script/narration.json")
        review = n["voice"]["pronunciation_review"]
        # the m7-r1 acceptance covered the m7-r1 audio only; on 2026-11-04 the owner accepted the m8-r4 audio
        prev = review["previous_acceptance"]
        self.assertEqual(prev["status"], "ACCEPTED_BY_OWNER")
        self.assertIn("No per-item listening session or phonetic verification is", prev["basis"])
        self.assertNotEqual(prev["audio_revision"], nar.narration_hash(n, pron.load(FILM)))
        self.assertEqual((review["status"], review["accepted_on"]), ("ACCEPTED_BY_OWNER", "2026-11-04"))
        self.assertEqual(review["audio_revision"], nar.narration_hash(n, pron.load(FILM)))
        self.assertIn("no per-item listening session", review["basis"])   # the record never claims a listening
        self.assertTrue({"cantilever", "Queensboro", "Roebling"} <= set(review["terms"]))
        g1 = gates.evaluate(FILM, "_final_4k")["gates"]["G1 evidence, script & pronunciation review"]
        self.assertEqual(g1["status"], "PASS")
        self.assertIn("no per-item listening recorded", g1["notes"][0])
        tmp, p = copy_film()   # the same record on a copy, but for other audio: the acceptance no longer applies
        with tmp:
            n = read(p / "script/narration.json")
            n["beats"][3]["sentences"][0] += " Indeed."
            (p / "script/narration.json").write_text(json.dumps(n))
            g1 = gates.evaluate(p, "_final_4k")["gates"]["G1 evidence, script & pronunciation review"]
            self.assertNotEqual(g1["status"], "PASS")
        tmp, p = owner_approved_copy()
        with tmp:
            g1 = gates.evaluate(p, "_review")["gates"]["G1 evidence, script & pronunciation review"]
            self.assertEqual(g1["status"], "PASS")
            self.assertIn("no per-item listening recorded", g1["notes"][0])   # never reported as "confirmed"
            n = read(p / "script/narration.json")
            n["beats"][3]["sentences"][0] += " Indeed."
            (p / "script/narration.json").write_text(json.dumps(n))
            notes = gates.evaluate(p, "_review")["gates"]["G1 evidence, script & pronunciation review"]["notes"]
            self.assertTrue(any("accepted for another audio revision" in x for x in notes))

    def test_every_sentence_is_am_michael_audio(self):
        from integrations.tts import kokoro
        manifest = read(FILM / "audio/narration_manifest.json")
        keys = [s["cache_key"] for b in manifest["beats"].values() for s in b["sentences"]]
        self.assertEqual(len(keys), 169)   # M8.2: 169 sentences
        for k in set(keys):
            seg = manifest["segments"][k]
            self.assertEqual((seg["voice"], seg["voice_sha256"], seg["lang_code"]),
                             ("am_michael", kokoro.VOICE_SHA256["am_michael"], "a"), k)
            self.assertTrue(seg["asr"]["pass"], k)

    def test_no_invented_quantities_on_cards_or_annotations(self):
        story = read(FILM / "storyboard/storyboard.json")
        texts = [e.get("text", "") for s in story["shots"] for e in (s.get("graphic") or {}).get("elements", [])]
        texts += [a.get("text", "") for b in read(FILM / "script/visual_beats.json")["beats"]
                  for a in b.get("annotations", [])]
        banned = ("kn", "mpa", "kip", "psi", "tonnes", "safety factor", "deflection", "stress", "stronger", "strongest",
                  "best design", "capacity")
        for t in texts:
            words = t.lower()
            self.assertFalse([w for w in banned if f" {w}" in f" {words}"], t)

    def test_models_near_real_bridges_are_labelled_illustrative(self):
        beats = {b["beat_id"]: b for b in read(FILM / "script/visual_beats.json")["beats"]}
        for bid in ("B27", "B29"):
            notes = [a["text"] for a in beats[bid]["annotations"] if a["type"] == "NOTE"]
            self.assertTrue(any(n.startswith("Illustrative model") for n in notes), bid)

    def test_not_a_linear_progress_story(self):
        text = " ".join(s for b in read(FILM / "script/narration.json")["beats"] for s in b["sentences"]).lower()
        self.assertIn("not a simple story of progress", text)
        self.assertIn("isn't because one design is simply better", text)
        self.assertNotIn("superior", text)


class ArchivalImageRightsTest(unittest.TestCase):
    def setUp(self):
        self.assets = read(FILM / "assets/manifest.json")
        self.story = read(FILM / "storyboard/storyboard.json")
        self.image = next(e for s in self.story["shots"] for e in (s.get("graphic") or {}).get("elements", [])
                          if e["kind"] == "image")

    def graphic(self, **change):
        e = dict(self.image, appear=0.0, **change)
        return {"elements": [e]}

    def test_every_external_image_has_a_complete_rights_record(self):
        externals = [a for a in self.assets["assets"] if a.get("origin") == "external"]
        self.assertEqual(len(externals), 7)   # M8: + Brooklyn (NY-18), Queensboro (NY-19); M8.1: + Golden Gate (CA-31)
        for a in externals:
            self.assertEqual([k for k in validator.EXTERNAL_LICENSE_FIELDS if not a.get(k)], [], a["id"])
            self.assertEqual(a["status"], "approved")
            self.assertIn("PD-USGov", a["license_evidence"])
            self.assertTrue(a["credit_keys"])
        self.assertEqual(validator.validate_graphic(self.graphic(), 10.0, FILM, self.assets), [])

    def test_image_without_rights_record_is_refused(self):
        errors = validator.validate_graphic(self.graphic(asset="IMG_UNKNOWN"), 10.0, FILM, self.assets)
        self.assertTrue(any("no external image without a rights record" in e for e in errors))

    def test_incomplete_record_wrong_path_missing_file_and_bad_crop_are_refused(self):
        assets = copy.deepcopy(self.assets)
        rec = next(a for a in assets["assets"] if a["id"] == self.image["asset"])
        rec.pop("license")
        rec["attribution"] = ""
        errors = validator.validate_graphic(self.graphic(), 10.0, FILM, assets)
        self.assertTrue(any("lacks license, attribution" in e for e in errors), errors)
        errors = validator.validate_graphic(self.graphic(path="assets/external/other.jpg", crop=[0.5, 0, 0.4, 1]),
                                            10.0, FILM, self.assets)
        for want in ("differs from the asset's local_path", "not found", "crop must be"):
            self.assertTrue(any(want in e for e in errors), want)

    def test_unresolved_sentence_timing_is_refused(self):
        errors = validator.validate_graphic(self.graphic(sentence=1), 10.0, FILM, self.assets)
        self.assertTrue(any("unresolved timing" in e for e in errors))

    def test_longform_qa_flags_unapproved_and_uncredited_images(self):
        tmp, p = copy_film()
        with tmp:
            assets = read(p / "assets/manifest.json")
            rec = next(a for a in assets["assets"] if a["id"] == self.image["asset"])
            rec["status"] = "pending"
            rec["credit_keys"] = ["Nobody Credited"]
            (p / "assets/manifest.json").write_text(json.dumps(assets))
            rows = {r["check"]: r for r in CH.longform_qa(p)[0]}
            self.assertEqual(rows["image_licences"]["status"], "FAIL")
            self.assertEqual(rows["image_attribution"]["status"], "FAIL")
            (p / "assets/external" / Path(rec["local_path"]).name).write_bytes(b"changed")
            rows = {r["check"]: r for r in CH.longform_qa(p)[0]}
            self.assertIn("hash differs", rows["image_licences"]["detail"])


class RenderCacheScopeTest(unittest.TestCase):
    """Rights metadata, chapters and editorial status never invalidate frames; image bytes do."""

    def setUp(self):
        self.tmp, self.p = copy_film(ignore=("renders", "output", "scenes", "qa"))
        self.story = read(self.p / "storyboard/storyboard.json")
        self.card = next(s for s in self.story["shots"] if render_cache.image_files(s))
        self.other = next(s for s in self.story["shots"] if s.get("visual_type") != "MOTION_GRAPHICS")

    def tearDown(self):
        self.tmp.cleanup()

    def keys(self):
        return [render_cache.cache_key(render_cache.components(self.p, s, "review")) for s in (self.card, self.other)]

    def test_rights_metadata_chapters_and_claim_status_are_not_render_inputs(self):
        before = self.keys()
        assets = read(self.p / "assets/manifest.json")
        for a in assets["assets"]:
            a["approval_note"] = "changed"
            a["attribution"] = a.get("attribution", "") + " (edited)"
        (self.p / "assets/manifest.json").write_text(json.dumps(assets))
        project = read(self.p / "project.json")
        project["chapters"] = "script/chapters_v2.json"
        project["factual_review"] = "verified"
        (self.p / "project.json").write_text(json.dumps(project))
        src = read(self.p / "research/sources.json")
        src["claims"][0]["review_status"] = "EDITORIALLY_APPROVED"
        (self.p / "research/sources.json").write_text(json.dumps(src))
        self.assertEqual(self.keys(), before)

    def test_changing_an_image_file_invalidates_only_its_cards(self):
        before = self.keys()
        rel = render_cache.image_files(self.card)[0]
        (self.p / rel).write_bytes((self.p / rel).read_bytes() + b"\x00")
        after = self.keys()
        self.assertNotEqual(after[0], before[0])
        self.assertEqual(after[1], before[1])


class InterruptedRenderRecoveryTest(unittest.TestCase):
    """A render of the same inputs interrupted mid-shot resumes; anything else re-renders."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.p = Path(self.tmp.name) / "film"
        (self.p / "qa").mkdir(parents=True)
        (self.p / "project.json").write_text(json.dumps({"fps": 24}))
        self.shot = {"id": "SC_001", "duration_seconds": 0.25}   # 6 frames
        self.seq = self.p / "renders" / "review" / "SC_001"
        self.seq.mkdir(parents=True)
        self.parts = {c: "x" for c in render_cache.CATEGORIES}
        self.commands = []

    def tearDown(self):
        self.tmp.cleanup()

    def fake_blender(self, command, logfile):
        self.commands.append(command)
        for k in range(1, 7):
            f = self.seq / f"frame_{k:04d}.png"
            if "--resume" not in command or not f.exists():
                f.write_bytes(FAKE_PNG)

    def run_render(self):
        with mock.patch.object(render_cache, "components", return_value=self.parts), \
                mock.patch.object(cli, "run_logged", self.fake_blender), \
                mock.patch.object(cli, "blender_command", lambda p, mode, preset, *extra: ["blender", *extra]):
            return cli.render_shot(self.p, self.shot, "review")

    def progress(self, key=None):
        (self.seq / "render_progress.json").write_text(json.dumps(
            {"shot": "SC_001", "cache_key": key or render_cache.cache_key(self.parts), "frames": 6}))

    def test_complete_frames_are_kept_and_a_truncated_frame_is_redone(self):
        for k in (1, 2, 3):
            (self.seq / f"frame_{k:04d}.png").write_bytes(FAKE_PNG.replace(b"\x00" * 16, bytes([k]) * 16))
        (self.seq / "frame_0004.png").write_bytes(FAKE_PNG[:20])   # killed while writing
        self.progress()
        self.assertEqual(self.run_render(), "resumed")
        self.assertIn("--resume", self.commands[0])
        self.assertEqual((self.seq / "frame_0002.png").read_bytes()[8:24], bytes([2]) * 16)   # untouched
        self.assertTrue(all(cli.complete_png(f) for f in self.seq.glob("frame_*.png")))
        self.assertEqual(len(list(self.seq.glob("frame_*.png"))), 6)
        manifest = read(self.seq / "render_manifest.json")
        self.assertTrue(manifest["resumed"])
        self.assertFalse((self.seq / "render_progress.json").exists())

    def test_changed_inputs_never_resume(self):
        for k in (1, 2):
            (self.seq / f"frame_{k:04d}.png").write_bytes(FAKE_PNG.replace(b"\x00" * 16, b"\x07" * 16))
        self.progress(key="an older cache key")
        self.assertEqual(self.run_render(), "rendered")
        self.assertNotIn("--resume", self.commands[0])
        self.assertEqual((self.seq / "frame_0001.png").read_bytes(), FAKE_PNG)

    def test_partial_frames_without_a_progress_record_are_re_rendered(self):
        (self.seq / "frame_0001.png").write_bytes(FAKE_PNG.replace(b"\x00" * 16, b"\x09" * 16))
        self.assertEqual(self.run_render(), "rendered")
        self.assertEqual((self.seq / "frame_0001.png").read_bytes(), FAKE_PNG)

    def test_complete_png_detection(self):
        f = self.seq / "x.png"
        f.write_bytes(FAKE_PNG)
        self.assertTrue(cli.complete_png(f))
        f.write_bytes(FAKE_PNG[:-1])
        self.assertFalse(cli.complete_png(f))
        self.assertFalse(cli.complete_png(self.seq / "missing.png"))


class CardTimingTest(unittest.TestCase):
    def ctx(self, beat):
        return {"cfg": {"motion": {}, "camera": {"subtitle_safe_band": 0.1}, "composite_weights": {}}, "fps": 24,
                "model": None, "beat": beat, "camera_of": None, "arch_states": [], "annotation_lead": 0.1,
                "sentence_offsets": [(0.4, 3.0), (3.4, 7.0)],
                "word_offsets": [[("so", 0.4, 0.6)], [("materials", 4.2, 4.9), ("site", 5.5, 5.9)]]}

    def card(self, *elements):
        return {"beat_id": "BX", "narrative_intent": "SHOW_CONTEXT",
                "graphic": {"elements": [dict(id=f"e{i}", kind="text", text="t", position=[0.5, 0.5], **e)
                                         for i, e in enumerate(elements)]}}

    def test_sentence_until_and_word_cues_resolve_to_measured_times(self):
        drafts = pl.build_strategy("CARD", self.ctx(self.card({"sentence": 0, "until": 1}, {"sentence": 1},
                                                              {"sentence": 1, "word": "Site,"})))
        els = drafts[0].make(240)["graphic"]["elements"]
        self.assertEqual((els[0]["appear"], els[0]["disappear"]), (0.3, 3.3))
        self.assertEqual(els[1]["appear"], 3.3)
        self.assertEqual(els[2]["appear"], 5.4)
        self.assertFalse(any(k in e for e in els for k in ("sentence", "until", "word")))

    def test_unknown_sentence_or_unaligned_word_is_refused(self):
        for bad in ({"sentence": 2}, {"sentence": 1, "word": "bridge"}):
            with self.assertRaises(pl.StrategyRejected):
                pl.build_strategy("CARD", self.ctx(self.card(bad)))

    def test_card_plan_refuses_flash_cards_and_late_elements(self):
        shot = {"id": "C", "visual_type": "MOTION_GRAPHICS", "duration_seconds": 1.0,
                "graphic": {"elements": [{"id": "a", "appear": 0.0}]}}
        with self.assertRaises(motion.PlanError):
            templates.plan_card(shot, 24)
        shot.update(duration_seconds=4.0)
        self.assertEqual(templates.plan_card(shot, 24).markers["middle"], 48)   # (96 + 1) // 2
        shot["graphic"]["elements"].append({"id": "b", "appear": 3.9})
        with self.assertRaises(motion.PlanError):
            templates.plan_card(shot, 24)
        shot["graphic"]["elements"][-1] = {"id": "b", "appear": 1.0, "disappear": 1.2}
        with self.assertRaises(motion.PlanError):
            templates.plan_card(shot, 24)

    def test_word_offsets_come_from_the_current_alignment(self):
        doc = read(FILM / "script/visual_beats.json")
        words = T.word_offsets(doc, FILM)
        self.assertEqual(set(words), {b["id"] for b in read(FILM / "script/timing.json")["beats"]})
        b02 = words["B02"][2]
        self.assertIn("materials", [w for w, _, _ in b02])
        plan = read(FILM / "storyboard/visual_plan.json")
        card = next(ps for ps in plan["shots"] if ps["beat_id"] == "B02")
        chip = next(e for e in card["shot"]["graphic"]["elements"] if e.get("text") == "Materials")
        spoken = next(t for w, t, _ in b02 if w == "materials")
        self.assertAlmostEqual(chip["appear"], spoken - 0.1, places=3)


class WordTimedAnnotationTest(unittest.TestCase):
    def test_chord_callouts_follow_the_spoken_words(self):
        story = read(FILM / "storyboard/storyboard.json")
        shot = next(s for s in story["shots"] if s["beat_ids"] == ["B16"])
        appear = {a["id"]: a["appear"] for a in shot["annotations"]["items"]}
        words = {w: t for w, t, _ in T.word_offsets(read(FILM / "script/visual_beats.json"), FILM)["B16"][0]}
        self.assertLess(appear["B16_legend"], appear["B16_top"])
        self.assertLess(appear["B16_top"], appear["B16_bottom"])
        lead = 0.1   # annotation_style appear_lead_seconds; frame-rounded by the layout
        self.assertAlmostEqual(appear["B16_top"], words["top"] - lead, delta=1 / 24)
        self.assertAlmostEqual(appear["B16_bottom"], words["bottom"] - lead, delta=1 / 24)

    def test_unaligned_word_fails_the_annotation(self):
        beat = {"beat_id": "BX", "annotations": [{"id": "n", "type": "NOTE", "text": "x", "sentence": 0, "word": "zebra"}]}
        records, issues = AN.plan_beat(beat, [], [(0.4, 3.0)], 4.0, None, V.Vocabulary(), {"claims": []},
                                       {"timing": {"appear_lead_seconds": 0.1}}, {}, 24, True,
                                       words=[[("so", 0.4, 0.6)]])
        self.assertEqual(records[0]["status"], "FAILED")
        self.assertTrue(issues and "zebra" in issues[0])


class NoteAndPushInTest(unittest.TestCase):
    def test_note_validation(self):
        sources = read(FILM / "research/sources.json")
        doc = read(FILM / "script/visual_beats.json")
        self.assertEqual(AN.validate_spec(doc, sources, V.Vocabulary()), [])
        bad = copy.deepcopy(doc)
        beat = next(b for b in bad["beats"] if b.get("annotations"))
        beat["annotations"] = [{"id": "n1", "type": "NOTE", "text": "x" * 60, "sentence": 0, "position": "TOP_LEFT"},
                               {"id": "n2", "type": "NOTE", "text": "ok", "sentence": 0, "position": "MIDDLE"},
                               {"id": "n3", "type": "NOTE", "text": " ", "sentence": 0}]
        errors = AN.validate_spec(bad, sources, V.Vocabulary())
        for want in ("n1", "NOTE position must be", "NOTE needs text"):
            self.assertTrue(any(want in e for e in errors), want)

    def test_push_in_stays_inside_the_locked_framing(self):
        fit = {"location": (0.0, -10.0, 0.0), "ortho_scale": 10.0}
        basis = ((1.0, 0.0, 0.0), (0.0, 0.0, 1.0), (0.0, 1.0, 0.0))
        start, end = framing.push_in_keys(fit, basis, 16 / 9, [(9.0, 0.0, 4.0)], 0.2)
        self.assertEqual(start["ortho_scale"], 10.0)
        self.assertAlmostEqual(end["ortho_scale"], 8.0)
        self.assertLessEqual(abs(end["location"][0]) / 10.0, 0.1 + 1e-9)   # shift clamped to amount / 2

    def test_push_in_amount_is_bounded(self):
        plan = motion.Plan(24, 48)
        cam = {"name": "Camera_LOCKED", "start": {"location": (0, 0, 0), "ortho_scale": 1.0},
               "end": {"location": (0, 0, 0), "ortho_scale": 0.9}}
        with self.assertRaises(motion.PlanError):
            motion.plan_camera_move(plan, {"type": "PUSH_IN", "amount": 0.5}, cam)
        with self.assertRaises(motion.PlanError):
            motion.plan_camera_move(plan, {"type": "ORBIT", "amount": 0.1}, cam)

    def test_film_push_ins_are_followed_by_hard_cuts_and_carry_no_anchored_labels(self):
        plan = read(FILM / "storyboard/visual_plan.json")
        moves = [i for i, ps in enumerate(plan["shots"]) if (ps["shot"].get("animation") or {}).get("camera_move")]
        self.assertGreaterEqual(len(moves), 4)
        for i in moves:
            if i + 1 < len(plan["shots"]):
                self.assertEqual(plan["shots"][i + 1]["cut_from_previous"], "hard")
            items = (plan["shots"][i].get("annotations") or {}).get("items", [])
            self.assertTrue(all(a["type"] in ("NOTE", "TENSION_COMPRESSION_LEGEND") for a in items))


class LongFormQATest(unittest.TestCase):
    def test_film_passes_long_form_qa(self):
        rows, m = CH.longform_qa(FILM)
        failed = [(r["check"], r["detail"]) for r in rows if r["status"] == "FAIL"]
        self.assertEqual(failed, [])
        self.assertEqual(len(m["chapters"]), 12)
        kinds = {k for c in m["chapters"] for k in c["visual_kinds"]}
        self.assertTrue({"PHOTO", "DIAGRAM", "3D_HOLD", "3D_PUSH_IN"} <= kinds, kinds)

    def test_long_silence_static_stretch_and_monotony_fail(self):
        tmp, p = copy_film()
        with tmp:
            timing = read(p / "script/timing.json")
            timing["beats"][3]["start_seconds"] += 6.0   # a 6 s hole in the narration
            (p / "script/timing.json").write_text(json.dumps(timing))
            story = read(p / "storyboard/storyboard.json")
            for s in story["shots"]:   # every shot a bare 3D hold without annotations
                s.update(visual_type="BLENDER_3D", transition="HOLD", annotations=None, graphic=None,
                         animation={})
            (p / "storyboard/storyboard.json").write_text(json.dumps(story))
            rows = {r["check"]: r for r in CH.longform_qa(p)[0]}
            for check in ("narration_silences", "no_static_stretches", "visual_variety"):
                self.assertEqual(rows[check]["status"], "FAIL", check)

    def test_runtime_outside_the_range_fails(self):
        tmp, p = copy_film()
        with tmp:
            project = read(p / "project.json")
            project.pop("runtime_decision", None)
            (p / "project.json").write_text(json.dumps(project))
            with mock.patch.object(CH, "RUNTIME_RANGE", (20 * 60.0, 30 * 60.0)):
                rows = {r["check"]: r for r in CH.longform_qa(p)[0]}
            self.assertEqual(rows["runtime"]["status"], "FAIL")
            # an owner decision moves the range only when it is complete
            project["runtime_decision"] = {"acceptable_minutes": [20, 30], "decided_by": "TEST OWNER", "decided_on": "2099-01-01"}
            (p / "project.json").write_text(json.dumps(project))
            self.assertEqual(CH.runtime_range(p)[2], None)
            project["runtime_decision"]["basis"] = "unit test"
            (p / "project.json").write_text(json.dumps(project))
            self.assertEqual(CH.runtime_range(p)[:2], (1200.0, 1800.0))
            rows = {r["check"]: r for r in CH.longform_qa(p)[0]}
            self.assertEqual(rows["runtime"]["status"], "FAIL")   # this film is shorter than 20 min


class AudioFirstNarrateTest(unittest.TestCase):
    def test_new_beats_do_not_block_narrate_but_still_block_validate(self):
        tmp, p = copy_film()
        with tmp:
            n = read(p / "script/narration.json")
            beat = copy.deepcopy(n["beats"][-1])
            beat["id"] = "B36"
            n["beats"].append(beat)
            (p / "script/narration.json").write_text(json.dumps(n))
            ch = read(p / "script/chapters.json")
            ch["chapters"][-1]["beat_ids"].append("B36")
            (p / "script/chapters.json").write_text(json.dumps(ch))
            errors, _ = validator.validate_project(p)
            self.assertTrue(any(e.startswith("shots must cover every narration beat") for e in errors))
            with mock.patch("builtins.print"):
                cli.do_validate(p, before_narrate=True)   # the storyboard is rebuilt after the audio
                with self.assertRaises(SystemExit):
                    cli.do_validate(p)


class AsrReuseTest(unittest.TestCase):
    """Unchanged audio + text + model keeps its transcript (re-scored); anything else is re-heard."""

    def setUp(self):
        from pipeline import asr_check
        self.A = asr_check
        self.tmp = tempfile.TemporaryDirectory()
        self.p = Path(self.tmp.name)
        (self.p / "audio").mkdir()
        seg = {"role": "sentence", "beat_id": "B1", "sentence_index": 0, "cache_key": "k1", "file": "audio/a.wav",
               "text": "A third approach is the truss.", "sha256": "s1"}
        self.manifest = {"segments": {"k1": seg}, "beats": {"B1": {"sentences": [{"cache_key": "k1"}]}}}
        self.write()

    def tearDown(self):
        self.tmp.cleanup()

    def write(self):
        (self.p / "audio/narration_manifest.json").write_text(json.dumps(self.manifest))

    def run_check(self, heard="A third approach is the truss."):
        calls = []

        def fake(paths, words=False):
            calls.append(list(paths))
            return [{"text": heard, "language": "english"} for _ in paths]
        with mock.patch.object(self.A, "transcribe", fake):
            failures = self.A.check_project(self.p, log=lambda *_: None)
        return calls, failures, read(self.p / "audio/narration_manifest.json")["segments"]["k1"]["asr"]

    def test_unchanged_segment_is_not_transcribed_twice(self):
        calls, failures, asr = self.run_check()
        self.assertEqual((len(calls), failures, asr["segment_sha256"]), (1, [], "s1"))
        calls, failures, asr = self.run_check(heard="ignored, reused")
        self.assertEqual((calls, failures, asr["text"]), ([], [], "A third approach is the truss."))

    def test_changed_audio_or_text_is_heard_again_and_can_fail(self):
        self.run_check()
        m = read(self.p / "audio/narration_manifest.json")
        m["segments"]["k1"]["sha256"] = "s2"   # new audio bytes under the same key
        self.manifest = m
        self.write()
        calls, failures, _ = self.run_check(heard="The trust takes yet another approach.")
        self.assertEqual(len(calls), 1)
        self.assertTrue(failures)


class ReviewDocumentsTest(unittest.TestCase):
    def test_generated_documents_never_claim_approval(self):
        from tools import longform_reports as LR
        tmp, p = copy_film()
        with tmp:
            (p / "qa").mkdir(exist_ok=True)
            d = LR._load(p)
            rows, manifest = CH.longform_qa(p)
            desc = LR.youtube_description(p, d, manifest).read_text()
            candidate = read(p / "project.json").get("production_profile") == "PUBLICATION_CANDIDATE"
            self.assertTrue(desc.startswith("<!-- PUBLICATION CANDIDATE" if candidate else "<!-- DRAFT"))
            self.assertIn("never uploads" if candidate else "not for publication", desc.splitlines()[0])
            stamps = [l.split(" ", 1)[0] for l in desc.split("Chapters\n\n")[1].split("\n\n")[0].splitlines()]
            self.assertEqual(stamps[0], "0:00")
            self.assertEqual(len(stamps), 12)
            self.assertIn("AI-generated voice", desc)
            for name in ("William E. Barrett", "Jack E. Boucher", "Jet Lowe", "Historic American Engineering Record"):
                self.assertIn(name, desc)
            pkg = LR.editorial_package(p, d).read_text()
            self.assertIn("Đã duyệt claim", pkg)   # m8-r4: the owner approved the 76 claims on 2026-11-04
            matrix = LR.evidence_matrix(p, d).read_text()
            self.assertEqual(matrix.count("| EDITORIALLY_APPROVED |"), 76)
            self.assertEqual(matrix.count("| SOURCE_VERIFIED |"), 6)
            self.assertIn("voice am_michael", desc)
            # a copy without the owner's records neither says nor counts an approval
            (p / "research/editorial_approval.json").unlink()
            src = read(p / "research/sources.json")
            for c in src["claims"]:
                c["review_status"] = "SOURCE_VERIFIED"
                c.pop("editorial_approval", None)
            (p / "research/sources.json").write_text(json.dumps(src))
            d = LR._load(p)
            self.assertNotIn("Đã duyệt claim", LR.editorial_package(p, d).read_text())
            self.assertEqual(LR.evidence_matrix(p, d).read_text().count("| EDITORIALLY_APPROVED |"), 0)

    def test_b35_credits_no_longer_name_the_narration_but_keep_the_other_credits(self):
        story = read(FILM / "storyboard/storyboard.json")
        card = next(s for s in story["shots"] if s["beat_ids"] == ["B35"])
        texts = [e["text"] for e in card["graphic"]["elements"] if e.get("kind") == "text"]
        self.assertFalse([t for t in texts if "Narration" in t or "AI-generated" in t])
        for keep in ("Historic American Engineering Record", "Library of Congress", "NCHRP", "illustrative"):
            self.assertTrue(any(keep in t for t in texts), keep)
        visual = {s["id"] for s in story["shots"] for e in (s.get("graphic") or {}).get("elements", [])
                  if "AI-generated" in e.get("text", "")}
        self.assertEqual(visual, set())


class LongFormNegativeTest(unittest.TestCase):
    """Each extended long-form check fails on a crafted defect."""

    def setUp(self):
        self.tmp, self.p = copy_film()

    def tearDown(self):
        self.tmp.cleanup()

    def rows(self):
        return {r["check"]: r for r in CH.longform_qa(self.p)[0]}

    def edit(self, rel, fn):
        d = read(self.p / rel)
        fn(d)
        (self.p / rel).write_text(json.dumps(d))

    def test_missing_sentence_and_overlapping_audio_fail(self):
        def damage(t):
            t["beats"][4]["sentences"][0]["text"] = "Something else."
            t["beats"][6]["start_seconds"] = t["beats"][5]["start_seconds"] + 0.5
        self.edit("script/timing.json", damage)
        rows = self.rows()
        self.assertEqual(rows["narration_sentences_complete"]["status"], "FAIL")
        self.assertEqual(rows["audio_no_overlap"]["status"], "FAIL")

    def test_repeated_visual_and_untitled_chapter_fail(self):
        def damage(story):
            twin = copy.deepcopy(story["shots"][7])
            story["shots"][8] = dict(twin, id=story["shots"][8]["id"], beat_ids=story["shots"][8]["beat_ids"],
                                     duration_seconds=story["shots"][8]["duration_seconds"])
            c3 = next(s for s in story["shots"] if s["beat_ids"] == ["B06"])
            c3["annotations"] = None
        self.edit("storyboard/storyboard.json", damage)
        rows = self.rows()
        self.assertEqual(rows["no_repeated_visuals"]["status"], "FAIL")
        self.assertIn("C3", rows["chapter_openings"]["detail"])

    def test_narration_visual_contradiction_fails(self):
        self.edit("storyboard/visual_plan.json", lambda plan: plan["consistency"]["rows"].append(
            {"beat_id": "B32", "sentence": 0, "rule": "SIMULTANEOUS", "verdict": "CONTRADICTION", "text": "x",
             "detail": "x", "shots": []}))
        self.assertEqual(self.rows()["annotations_consistent"]["status"], "FAIL")

    def test_fact_beat_without_claims_is_reported_per_chapter(self):
        self.edit("script/narration.json", lambda n: next(b for b in n["beats"] if b["id"] == "B12").update(claim_ids=[]))
        m = CH.manifest(self.p)
        owner = next(c for c in m["chapters"] if "B12" in c["beats"])
        self.assertIn("B12", owner["evidence"]["unsupported_fact_beats"])
        self.assertTrue(all(not c["evidence"]["missing_claims"] for c in m["chapters"]))


class ChapterEvidenceTest(unittest.TestCase):
    def test_every_chapter_reports_evidence_and_pending_review(self):
        m = CH.manifest(FILM)
        for c in m["chapters"]:
            ev = c["evidence"]
            self.assertEqual(ev["unsupported_fact_beats"], [], c["id"])
            self.assertEqual(ev["missing_claims"], [], c["id"])
            self.assertTrue(ev["sources_known"], c["id"])
            self.assertEqual(ev["narration_revision"], "m8-r4")
            self.assertEqual(ev["editorial_status"], "NO_CLAIMS (framing only)" if c["id"] == "C1" else "EDITORIALLY_APPROVED", c["id"])
            self.assertTrue(ev["historical_accuracy"], c["id"])
        c11 = next(c for c in m["chapters"] if c["id"] == "C11")
        for bridge in ("Carrollton Viaduct", "Niagara bridge", "Kentucky River bridge", "Penobscot Narrows Bridge"):
            self.assertIn(f"Illustrative model, not the {bridge}", c11["evidence"]["visual_assumptions"])


class ChapterCacheAndRegenerationTest(unittest.TestCase):
    def test_editing_one_chapter_invalidates_only_its_shots(self):
        tmp, p = copy_film(ignore=("renders", "output", "scenes", "qa"))
        with tmp:
            story = read(p / "storyboard/storyboard.json")
            before = {s["id"]: render_cache.cache_key(render_cache.components(p, s, "review")) for s in story["shots"]}
            m = CH.manifest(p)
            c6 = set(next(c for c in m["chapters"] if c["id"] == "C6")["shots"])
            card = next(s for s in story["shots"] if s["id"] in c6 and s.get("visual_type") == "MOTION_GRAPHICS")
            card["graphic"]["elements"][0]["text"] = card["graphic"]["elements"][0].get("text", "") + " (edited)"
            (p / "storyboard/storyboard.json").write_text(json.dumps(story))
            after = {s["id"]: render_cache.cache_key(render_cache.components(p, s, "review")) for s in story["shots"]}
            self.assertEqual({k for k in before if before[k] != after[k]}, {card["id"]})

    def test_editing_one_sentence_makes_the_timing_lock_stale(self):
        n = read(FILM / "script/narration.json")
        timing = read(FILM / "script/timing.json")
        story = read(FILM / "storyboard/storyboard.json")
        project = read(FILM / "project.json")
        from pipeline import pronunciation as pron
        lex = pron.load(FILM)   # M8.2: the film has speech-only overrides, part of the narration hash
        self.assertEqual(validator.validate_timing(timing, n, story, project["fps"], project["duration_seconds"], lex), [])
        n["beats"][9]["sentences"][0] += " Indeed."
        errors = validator.validate_timing(timing, n, story, project["fps"], project["duration_seconds"], lex)
        self.assertTrue(any("timing lock is stale" in e for e in errors))


class SubtitleAndMediaTest(unittest.TestCase):
    def test_cues_stay_inside_their_measured_sentences(self):
        from pipeline import pronunciation as pron, subtitles
        timing = read(FILM / "script/timing.json")
        manifest = read(FILM / "audio/narration_manifest.json")
        cues = subtitles.build_cues(FILM, timing, manifest, pron.asr_aliases(pron.load(FILM)),
                                    total=timing["total_seconds"])
        spans = {}
        for b in timing["beats"]:
            base = b["start_seconds"] - b["sentences"][0]["rel_start"]
            for s in b["sentences"]:
                spans[f"{b['id']}.s{s['index']}"] = (base + s["rel_start"], base + s["rel_end"])
        self.assertEqual({c["sentence"] for c in cues}, set(spans))
        for c in cues:
            a, b = spans[c["sentence"]]
            self.assertGreaterEqual(c["start"], a - 0.05, c)
            self.assertLessEqual(c["end"], b + 0.6, c)   # a cue may linger briefly after the sentence, never before
        self.assertEqual([c["start"] for c in cues], sorted(c["start"] for c in cues))

    def test_final_4k_assembly_matches_the_locked_timing(self):
        # M8.2: the owner approved m8-r4 on 2026-11-04 and asked for the native 4K final; it must match the lock.
        report = FILM / "qa" / "assembly_report_final_4k.json"
        if not report.is_file():
            self.skipTest("4K final not assembled yet")
        r = read(report)
        timing = read(FILM / "script/timing.json")
        self.assertEqual(r["problems"], [])
        self.assertEqual(r["frames"], timing["total_frames"])
        self.assertEqual((r["video"]["width"], r["video"]["height"]), (3840, 2160))
        lo, hi, _ = CH.runtime_range(FILM)
        self.assertTrue(lo <= r["seconds"] <= hi)
        self.assertIn("FINAL_4K_2160p", Path(r["output"]).name)
        self.assertAlmostEqual(r["loudness_after"]["integrated_lufs"], -16.0, delta=1.0)
        self.assertEqual(r["subtitle_entries"], r["subtitle_stats"]["cues"])


class InternalReviewGateTest(unittest.TestCase):
    def test_output_name_is_clean_only_with_every_approval(self):
        self.assertEqual(cli.output_label(FILM), "documentary")   # m8-r4: every approval is recorded
        tmp, p = copy_film()
        with tmp:
            (p / "review/OWNER_APPROVALS.json").unlink()   # without the owner's records
            n = read(p / "script/narration.json")
            n["voice"]["pronunciation_review"]["status"] = "PENDING"
            (p / "script/narration.json").write_text(json.dumps(n))
            self.assertEqual(cli.output_label(p), "documentary_INTERNAL_REVIEW")
        tmp, p = owner_approved_copy()
        with tmp:
            self.assertEqual(cli.output_label(p), "documentary")
        self.assertIn("INTERNAL REVIEW", cli.internal_comment("documentary_INTERNAL_REVIEW"))
        self.assertIsNone(cli.internal_comment("documentary"))
        for field, value in (("pronunciation_review", {"status": "PENDING"}),
                             ("license", {"owner_confirmation_for_this_film": "PENDING"}),
                             ("license", {"status": "LICENSE_REVIEW_REQUIRED"})):
            tmp, p = owner_approved_copy()
            with tmp:
                n = read(p / "script/narration.json")
                n["voice"][field].update(value)
                (p / "script/narration.json").write_text(json.dumps(n))
                self.assertEqual(cli.output_label(p), "documentary_INTERNAL_REVIEW", (field, value))

    def test_withdrawn_approvals_block_publication(self):
        cases = []
        tmp, p = owner_approved_copy()
        with tmp:
            self.assertEqual(gates.evaluate(p, "_final_4k")["gates"]["G1 evidence, script & pronunciation review"]["status"],
                             "PASS")
            src = read(p / "research/sources.json")
            next(c for c in src["claims"] if c["id"] == "CLM_709")["review_status"] = "SOURCE_VERIFIED"
            (p / "research/sources.json").write_text(json.dumps(src))
            cases.append(gates.evaluate(p, "_final_4k"))
        tmp, p = owner_approved_copy()
        with tmp:
            n = read(p / "script/narration.json")
            n["voice"]["license"].update(owner_confirmation_for_this_film="PENDING")
            n["voice"]["pronunciation_review"].update(status="PENDING")
            (p / "script/narration.json").write_text(json.dumps(n))
            cases.append(gates.evaluate(p, "_final_4k"))
        claims, voice = cases
        self.assertIn("EDITORIAL_REVIEW_PENDING", claims["statuses"])
        self.assertTrue(any("CLM_709" in x for x in claims["gates"]["G6 final publication readiness"]["notes"]))
        self.assertIn("TTS_RIGHTS_PENDING", voice["statuses"])
        self.assertTrue(any("owner confirmation for this film PENDING" in x
                            for x in voice["gates"]["G2 narration audio & TTS rights"]["notes"]))
        self.assertTrue(any("pronunciation_review PENDING" in x
                            for x in voice["gates"]["G1 evidence, script & pronunciation review"]["notes"]))
        for r in cases:
            self.assertNotIn("PUBLICATION_READY", r["statuses"])
            self.assertNotEqual(r["gates"]["G6 final publication readiness"]["status"], "PASS")

    def test_final_gate_checks_the_claims_the_film_uses(self):
        # CLM_747 is in the research archive only; a claim the film uses must be approved.
        errors, warnings = validator.validate_project(FILM, final=True)   # m8-r4: approved by the owner, 2026-11-04
        self.assertEqual([e for e in errors if e.startswith("FINAL gate")], [])
        tmp, p = copy_film(("renders", "output", "scenes", "qa", "*.wav", "*.m4a"))   # without the owner's records: every approval is demanded
        with tmp:
            src = read(p / "research/sources.json")
            for c in src["claims"]:
                c["review_status"] = "SOURCE_VERIFIED"
            (p / "research/sources.json").write_text(json.dumps(src))
            lex = read(p / "script/pronunciation.json")
            for e in lex["entries"]:
                e.update(status="PENDING_LISTENING_REVIEW", confirmed_by=None, confirmed_on=None)
            (p / "script/pronunciation.json").write_text(json.dumps(lex))
            project = read(p / "project.json")
            project["factual_review"] = "pending"
            (p / "project.json").write_text(json.dumps(project))
            errors, _ = validator.validate_project(p, final=True)
            self.assertTrue(any(e.startswith("FINAL gate: unverified claims used in the film") for e in errors))
            self.assertIn("FINAL gate: factual_review is not verified", errors)
            self.assertTrue(any(e.startswith("FINAL gate: pronunciation PRON_CORINNE") for e in errors))
        tmp, p = owner_approved_copy()
        with tmp:
            errors, _ = validator.validate_project(p, final=True)
            self.assertEqual([e for e in errors if e.startswith("FINAL gate")], [])
            vb = read(p / "script/visual_beats.json")
            vb["beats"][0].setdefault("annotations", []).append(
                {"id": "x", "type": "NOTE", "text": "x", "sentence": 0, "claim_id": "CLM_747"})
            (p / "script/visual_beats.json").write_text(json.dumps(vb))
            errors, _ = validator.validate_project(p, final=True)
            self.assertTrue(any("CLM_747" in e and "FINAL gate" in e for e in errors))

    def test_missing_long_form_qa_fails_the_gate(self):
        tmp, p = copy_film()
        with tmp:
            result = gates.evaluate(p, "_review")
            self.assertEqual(result["gates"]["GL long-form chapters & rights"]["status"], "FAIL")
            self.assertIn("long-form QA missing", result["gates"]["GL long-form chapters & rights"]["notes"][0])

    def test_profile_cannot_switch_off_the_narrated_gates(self):
        tmp, p = copy_film(ignore=("renders", "output", "scenes", "qa"))
        with tmp:
            project = read(p / "project.json")
            project["production_profile"] = "TECHNICAL_SILENT_PREVIEW"
            (p / "project.json").write_text(json.dumps(project))
            errors, _ = validator.validate_project(p)
            self.assertTrue(any("cannot be switched off" in e for e in errors))

    def test_editorial_metadata_does_not_change_the_narration_hash(self):
        n = read(FILM / "script/narration.json")
        h = nar.narration_hash(n, None)
        n2 = copy.deepcopy(n)
        n2["voice"]["license"]["owner_confirmation_for_this_film"] = "CONFIRMED"
        n2["voice"]["pronunciation_review"]["status"] = "CONFIRMED"
        n2["revision"]["status"] = "EDITORIALLY_APPROVED"
        self.assertEqual(nar.narration_hash(n2, None), h)


if __name__ == "__main__":
    unittest.main()
