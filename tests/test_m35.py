"""M3.5: TTS rights, audio/render cache separation, pronunciation, subtitles, approvals, gates."""
import copy
import json
import math
import shutil
import struct
import tempfile
import unittest
import wave
from pathlib import Path

from integrations.tts import omnivoice as ov
from integrations.tts import providers
from pipeline import asr_check, audio_manifest, narration as nar, pronunciation as pron, subtitles
from tests.fake_omnivoice import FakeOmniVoice
from tools import render_cache
from tools.cli import ROOT
from tools.validator import publication_audio_errors, validate_project

PILOT = ROOT / "projects" / "suffolk-roofs"
HAS_FFMPEG = bool(shutil.which("ffmpeg") and shutil.which("ffprobe"))


def load(rel):
    return json.loads((PILOT / rel).read_text())


def registry(rc="INTERNAL_PREVIEW_ONLY", clearance=None):
    info = {"rights_class": rc, "license": {"x": "y"}}
    if clearance:
        info["clearance"] = clearance
    return {"providers": {"omnivoice": info, "human": {"rights_class": "PENDING_REVIEW", "license": {"x": "y"}}},
            "workflow": {"internal_preview": ["omnivoice"], "publication": []}}


def tone_with_gap(path, before, gap, after, rate=24000):
    """16-bit WAV: tone, silence, tone (a measurable pause for subtitle breaks)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1), w.setsampwidth(2), w.setframerate(rate)
        def tone(sec):
            return b"".join(struct.pack("<h", int(9000 * math.sin(i / 5))) for i in range(int(sec * rate)))
        w.writeframes(tone(before) + b"\x00\x00" * int(gap * rate) + tone(after))


class ProviderRightsTest(unittest.TestCase):
    def test_project_registry_is_valid_and_omnivoice_is_preview_only(self):
        reg = providers.load_registry()
        self.assertEqual(providers.validate_registry(reg), [])
        self.assertEqual(providers.rights_class("omnivoice", reg), "INTERNAL_PREVIEW_ONLY")
        self.assertEqual(reg["workflow"]["publication"], [])

    def test_publication_purpose_is_refused_unless_cleared(self):
        self.assertEqual(providers.check_purpose("omnivoice", "internal_preview", registry()), "INTERNAL_PREVIEW_ONLY")
        with self.assertRaises(providers.RightsError):
            providers.check_purpose("omnivoice", "publication", registry())
        with self.assertRaises(providers.RightsError):
            providers.check_purpose("human", "publication", registry())
        with self.assertRaises(providers.RightsError):
            providers.check_purpose("omnivoice", "internal_preview", registry("REJECTED"))
        with self.assertRaises(providers.RightsError):
            providers.check_purpose("unknown_tts", "internal_preview", registry())

    def test_cleared_needs_a_human_clearance_record(self):
        errs = providers.validate_registry(registry("PUBLICATION_CLEARED"))
        self.assertTrue(any("cleared_by" in e for e in errs), errs)
        ok = registry("PUBLICATION_CLEARED", {"cleared_by": "A. Person", "cleared_on": "2026-11-01", "evidence": "contract"})
        self.assertEqual(providers.validate_registry(ok), [])
        bad = registry()
        bad["workflow"]["publication"] = ["omnivoice"]
        self.assertTrue(any("not PUBLICATION_CLEARED" in e for e in providers.validate_registry(bad)))

    def test_narration_licence_must_match_registry_and_name_a_reviewer(self):
        n, s = load("script/narration.json"), load("research/sources.json")
        self.assertEqual(nar.validate(n, s, providers.load_registry(), pron.load(PILOT)), [])
        m = copy.deepcopy(n)
        m["voice"]["license"]["rights_class"] = "PUBLICATION_CLEARED"
        self.assertTrue(any("disagrees" in e for e in nar.validate(m, s, registry())))
        m = copy.deepcopy(n)
        m["voice"]["license"]["status"] = "APPROVED"
        errs = nar.validate(m, s, registry())
        self.assertTrue(any("APPROVED but provider" in e for e in errs), errs)
        self.assertTrue(any("approved_by" in e for e in errs), errs)


class AudioCacheSeparationTest(unittest.TestCase):
    def key(self, **kw):
        base = dict(provider="omnivoice", adapter_version="1.0", model="k2-fsa/OmniVoice", model_revision="r1",
                    spoken_text="Hello.", voice_id="v1", voice_identity={"mode": "design"}, params={"speed": 1.0},
                    rights_class="INTERNAL_PREVIEW_ONLY")
        base.update(kw)
        return audio_manifest.cache_key(**base)

    def test_every_dimension_separates_the_cache(self):
        k = self.key()
        for change in (dict(provider="human"), dict(model="other/model"), dict(model_revision="r2"),
                       dict(spoken_text="Hello there."), dict(voice_id="v2"), dict(voice_identity={"mode": "clone"}),
                       dict(params={"speed": 0.9}), dict(rights_class="PUBLICATION_CLEARED")):
            self.assertNotEqual(k, self.key(**change), change)

    @unittest.skipUnless(HAS_FFMPEG, "ffmpeg required")
    def test_preview_audio_is_never_reused_for_publication(self):
        with tempfile.TemporaryDirectory() as tmp, FakeOmniVoice() as fake:
            p = Path(tmp) / "demo"
            (p / "script").mkdir(parents=True)
            (p / "research").mkdir()
            (p / "research/sources.json").write_text(json.dumps({
                "sources": [{"id": "S1", "url": "https://example.org"}],
                "claims": [{"id": "C1", "text": "x", "source_ids": ["S1"], "review_status": "SOURCE_VERIFIED",
                            "evidence": [{"source_id": "S1", "locator": "p1", "excerpt": "x"}]}]}))
            narration = {"voice": {"provider": "omnivoice", "id": "t", "mode": "design", "language": "English",
                                   "design": {"gender": "Male"}, "params": {},
                                   "license": {"status": "NOT_CLEARED", "rights_class": "INTERNAL_PREVIEW_ONLY",
                                               "components": [{"name": "x"}]}},
                         "pacing": {"sentence_pause_seconds": 0.3, "beat_lead_in_seconds": 0.3,
                                    "beat_tail_seconds": 0.5},
                         "beats": [{"id": "B1", "kind": "fact", "claim_ids": ["C1"],
                                    "sentences": ["Hello there friend, this is a test."]}]}
            (p / "script/narration.json").write_text(json.dumps(narration))
            client = ov.OmniVoiceClient(base_url=fake.url, retries=0, model_revision="r1")
            quiet = lambda *a: None
            nar.generate(p, client, log=quiet, registry=registry())
            self.assertEqual(len(fake.calls), 1)
            with self.assertRaises(providers.RightsError):  # not cleared -> refused outright
                nar.generate(p, client, log=quiet, purpose="publication", registry=registry())
            cleared = registry("PUBLICATION_CLEARED", {"cleared_by": "x", "cleared_on": "y", "evidence": "z"})
            narration["voice"]["license"]["rights_class"] = "PUBLICATION_CLEARED"
            (p / "script/narration.json").write_text(json.dumps(narration))
            data = nar.generate(p, client, log=quiet, purpose="publication", registry=cleared)
            self.assertEqual(len(fake.calls), 2)  # same text, same voice: still regenerated
            rec = data["segments"][data["beats"]["B1"]["sentences"][0]["cache_key"]]
            self.assertEqual(rec["rights_class"], "PUBLICATION_CLEARED")
            self.assertEqual(len(data["segments"]), 2)  # the preview take is kept, not overwritten

    def test_pilot_m3_takes_were_adopted_not_regenerated(self):
        m = load("audio/narration_manifest.json")
        adopted = [r for r in m["segments"].values() if r.get("legacy_cache_key")]
        self.assertGreaterEqual(len(adopted), 9)
        self.assertTrue(all(r["rights_class"] == "INTERNAL_PREVIEW_ONLY" for r in m["segments"].values()))


class PronunciationTest(unittest.TestCase):
    LEX = {"entries": [{"id": "P1", "written": "Babergh", "speech": {"omnivoice": "[B EY1 B AH0]"},
                        "asr_aliases": ["baber"], "status": "PENDING_LISTENING_REVIEW"}]}

    def test_override_is_speech_only_whole_word_and_per_provider(self):
        text = "In Babergh and Mid Suffolk."
        spoken, applied = pron.spoken_text(text, self.LEX, "omnivoice")
        self.assertEqual(spoken, "In [B EY1 B AH0] and Mid Suffolk.")
        self.assertEqual(applied, ["P1"])
        self.assertEqual(text, "In Babergh and Mid Suffolk.")             # written text untouched
        self.assertEqual(pron.spoken_text(text, self.LEX, "human")[0], text)  # no form for this provider
        for other in ("Baberghs roofs", "Babergh-style", "babergh"):
            self.assertEqual(pron.spoken_text(other, self.LEX, "omnivoice")[0], other)

    def test_validation_and_confirmation(self):
        self.assertEqual(pron.validate(self.LEX), [])
        bad = copy.deepcopy(self.LEX)
        bad["entries"][0]["speech"]["omnivoice"] = "[b ey1 b ah0]"
        self.assertTrue(pron.validate(bad))
        conf = copy.deepcopy(self.LEX)
        conf["entries"][0]["status"] = "CONFIRMED"
        self.assertTrue(any("confirmed_by" in e for e in pron.validate(conf)))

    def test_asr_aliases_keep_wer_about_intelligibility(self):
        ref, heard = "In Babergh and Mid Suffolk", "In Baber and Mid Suffolk"
        self.assertGreater(asr_check.wer(ref, heard), 0)
        self.assertEqual(asr_check.wer(ref, heard, pron.asr_aliases(self.LEX)), 0)

    def test_pilot_uses_the_override_only_in_the_spoken_text(self):
        n, lex = load("script/narration.json"), pron.load(PILOT)
        self.assertEqual(pron.used_entries(n, lex, "omnivoice"), ["PRON_001"])
        self.assertIn("Babergh", n["beats"][0]["sentences"][0])
        m = load("audio/narration_manifest.json")
        rec = m["segments"][m["beats"]["B1"]["sentences"][0]["cache_key"]]
        self.assertIn("[B EY1 B AH0]", rec["spoken_text"])
        self.assertEqual(rec["text"], n["beats"][0]["sentences"][0])
        self.assertEqual(m["beats"]["B1"]["sentences"][0]["text"], n["beats"][0]["sentences"][0])

    def test_narration_hash_tracks_spoken_form_not_licence_notes(self):
        n, lex = load("script/narration.json"), pron.load(PILOT)
        h = nar.narration_hash(n, lex)
        m = copy.deepcopy(n)
        m["voice"]["license"]["decision"] = "edited note"
        self.assertEqual(h, nar.narration_hash(m, lex))
        lex2 = copy.deepcopy(lex)
        lex2["entries"][0]["speech"]["omnivoice"] = "[B EY1 B ER0]"
        self.assertNotEqual(h, nar.narration_hash(n, lex2))


class SubtitleTest(unittest.TestCase):
    def test_wrap_limits_and_prefers_punctuation(self):
        lines = subtitles.wrap("in eastern England, historic roofs do not all look alike.")
        self.assertEqual(lines, ["in eastern England,", "historic roofs do not all look alike."])
        self.assertTrue(all(len(l) <= 42 for l in lines))
        self.assertIsNone(subtitles.wrap("x" * 50 + " " + "y" * 50))

    def test_breaks_only_between_aligned_words(self):
        words = "Older timber-framed buildings here were probably roofed originally with thatch or oak shingles, " \
                "depending on which materials were available.".split()
        times = [(i * 0.35, i * 0.35 + 0.3) for i in range(len(words))]
        times[14] = times[13] = None   # 'depending' / 'shingles,' unmatched
        spans = subtitles.segment(words, times, 0.0, len(words) * 0.35)
        for a, b in spans[:-1]:
            self.assertIsNotNone(times[b])
            self.assertIsNotNone(times[b + 1])
        self.assertEqual(" ".join(" ".join(words[a:b + 1]) for a, b in spans), " ".join(words))

    def test_match_words_handles_numbers_hyphens_and_aliases(self):
        script = "about fifty degrees in Babergh".split()
        heard = [{"text": "about", "start": 0.0, "end": 0.3}, {"text": "50", "start": 0.3, "end": 0.7},
                 {"text": "degrees", "start": 0.7, "end": 1.1}, {"text": "in", "start": 1.1, "end": 1.2},
                 {"text": "Baber", "start": 1.2, "end": 1.6}]
        times = subtitles.match_words(script, heard, {"baber": "babergh"})
        self.assertEqual(times[1], (0.3, 0.7))
        self.assertEqual(times[4], (1.2, 1.6))
        self.assertIsNone(subtitles.match_words(script, heard[:3])[4])

    def test_boundary_lands_in_the_measured_pause(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)
            tone_with_gap(p / "audio/segments/s.wav", 1.6, 0.4, 1.8)
            text = "From the eighteenth century, clay pantiles were used more commonly in many villages across the county."
            words = text.split()  # > 84 characters: must become two cues
            t = [(0.1 + i * 0.37, 0.1 + i * 0.37 + 0.3) for i in range(4)] + \
                [(2.05 + i * 0.14, 2.05 + i * 0.14 + 0.12) for i in range(len(words) - 4)]
            asr_words = [{"text": w, "start": a, "end": b} for w, (a, b) in zip(words, t)]
            manifest = {"segments": {"k": {"file": "audio/segments/s.wav", "sha256": "h",
                                           "alignment": {"segment_sha256": "h", "words": asr_words}}},
                        "beats": {"B1": {"sentences": [{"index": 0, "cache_key": "k"}]}}}
            timing = {"beats": [{"id": "B1", "shot": "S1", "sentences": [{"index": 0, "text": text,
                                                                         "start": 10.0, "end": 13.8}]}]}
            cues = subtitles.build_cues(p, timing, manifest)
            self.assertGreaterEqual(len(cues), 2)
            first_break = cues[0]["boundary"]
            self.assertEqual(first_break["after_word"], "century,")
            self.assertTrue(11.6 <= cues[1]["start"] <= 12.0, cues[1]["start"])  # inside the 1.6-2.0 s pause
            self.assertLess(first_break["rms_db_at_boundary"], -60)
            self.assertEqual(" ".join(c["text"] for c in cues), text)

    def test_unaligned_sentence_falls_back_to_its_measured_span(self):
        timing = {"beats": [{"id": "B1", "shot": "S1", "sentences": [{"index": 0, "text": "Slate is different.",
                                                                     "start": 1.0, "end": 2.4}]}]}
        cues = subtitles.build_cues(PILOT, timing, {"segments": {}, "beats": {}})
        self.assertEqual((cues[0]["start"], cues[0]["source"]), (1.0, "sentence span (no alignment)"))

    def test_qa_catches_overlap_long_lines_and_dropped_words(self):
        cues = [{"start": 0.0, "end": 2.0, "lines": ["One two three."], "text": "One two three.", "sentence": "a",
                 "boundary": None, "source": "x"},
                {"start": 1.5, "end": 3.0, "lines": ["y" * 45], "text": "y" * 45, "sentence": "b",
                 "boundary": None, "source": "x"}]
        problems, _, _ = subtitles.qa(cues, 10.0, {"a": "One two three four.", "b": "y" * 45})
        joined = " ".join(problems)
        self.assertIn("overlaps", joined)
        self.assertIn("45 chars", joined)
        self.assertIn("does not rebuild", joined)

    def test_srt_roundtrip(self):
        cues = [{"start": 0.3, "end": 2.345, "lines": ["In Babergh and Mid Suffolk,"]},
                {"start": 2.345, "end": 5.95, "lines": ["in eastern England,", "historic roofs do not all look alike."]}]
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "x.srt"
            subtitles.write_srt(cues, out)
            back = subtitles.parse_srt(out.read_text())
        self.assertEqual([(round(a, 3), round(b, 3), l) for a, b, l in back],
                         [(c["start"], c["end"], c["lines"]) for c in cues])

    def test_pilot_cues_meet_limits(self):
        timing, manifest = load("script/timing.json"), load("audio/narration_manifest.json")
        cues = subtitles.build_cues(PILOT, timing, manifest, pron.asr_aliases(pron.load(PILOT)))
        sentences = {f"{b['id']}.s{s['index']}": s["text"] for b in timing["beats"] for s in b["sentences"]}
        problems, _, stats = subtitles.qa(cues, timing["total_seconds"], sentences)
        self.assertEqual(problems, [])
        self.assertLessEqual(stats["max_line"], 42)
        self.assertEqual(stats["sentence_fallbacks"], 0)
        self.assertTrue(all("Babergh" in c["text"] for c in cues if "Bab" in c["text"]))


class RenderCacheTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.p = Path(self.tmp.name) / "proj"
        (self.p / "storyboard").mkdir(parents=True)
        for rel in ("project.json", "storyboard/states.json"):
            shutil.copy(PILOT / rel, self.p / rel)
        self.shot = copy.deepcopy(next(s for s in load("storyboard/storyboard.json")["shots"] if s["id"] == "SC_003"))

    def tearDown(self):
        self.tmp.cleanup()

    def parts(self, shot=None):
        return render_cache.components(self.p, shot or self.shot, "preview")

    def edit(self, rel, fn):
        path = self.p / rel
        data = json.loads(path.read_text())
        fn(data)
        path.write_text(json.dumps(data))

    def test_non_visual_edits_keep_the_render_cache(self):
        before = render_cache.cache_key(self.parts())
        shot = copy.deepcopy(self.shot)
        shot.update(narration="Different words.", visual_purpose="new text", claim_ids=["CLM_999"],
                    beat_ids=["B9"], start_seconds=99.0, cut_from_previous="hard")
        self.assertEqual(before, render_cache.cache_key(self.parts(shot)))
        self.edit("project.json", lambda d: d.update(title="New title", factual_review="verified",
                                                     duration_seconds=99.0, audio_timing_locked=False))
        self.edit("storyboard/states.json", lambda d: (d.update(transitions=[]),
                                                       d["variants"][0].update(name="renamed", claim_ids=[])))
        self.assertEqual(before, render_cache.cache_key(self.parts(shot)))

    def test_visual_edits_invalidate_and_are_named(self):
        manifest = {"key_version": render_cache.KEY_VERSION, "components": self.parts(),
                    "engine_files": render_cache.engine_file_hashes()}
        shot = copy.deepcopy(self.shot)
        shot["duration_seconds"] += 1 / 24
        self.assertEqual(render_cache.stale_reasons(manifest, self.parts(shot)), ["shot_visual"])
        shot = copy.deepcopy(self.shot)
        shot["animation"]["incoming"]["distance"] = 1.5
        self.assertEqual(render_cache.stale_reasons(manifest, self.parts(shot)), ["shot_visual"])
        self.edit("storyboard/states.json", lambda d: d["variants"][2].update(roof_pitch_degrees=32))
        self.assertEqual(render_cache.stale_reasons(manifest, self.parts()), ["states_geometry"])
        self.edit("project.json", lambda d: d.update(fps=25))
        self.assertIn("project_render", render_cache.stale_reasons(manifest, self.parts()))
        fresh = dict(manifest, components=self.parts())
        other = dict(self.parts(), engine="x")
        eh = dict(render_cache.engine_file_hashes(), **{"geometry.py": "changed"})
        reasons = render_cache.stale_reasons(fresh, other, eh)
        self.assertEqual(reasons, ["engine (geometry.py)"])

    def test_preset_and_legacy_manifest(self):
        self.assertNotEqual(self.parts()["preset"], render_cache.components(self.p, self.shot, "review")["preset"])
        self.assertIn("one-time", render_cache.stale_reasons({"cache_key": "old"}, self.parts())[0])
        self.assertEqual(render_cache.stale_reasons(None, self.parts()), ["never rendered"])

    def test_qa_only_engine_files_are_not_render_dependencies(self):
        names = [f.name for f in render_cache.engine_files()]
        self.assertNotIn("qa_checks.py", names)
        self.assertIn("geometry.py", names)


class ApprovalAndCitationTest(unittest.TestCase):
    def copy_pilot(self, tmp):
        dst = Path(tmp) / "suffolk-roofs"
        shutil.copytree(PILOT, dst, ignore=shutil.ignore_patterns("renders", "output", "qa", "audio"))
        shutil.copytree(PILOT / "audio", dst / "audio", ignore=shutil.ignore_patterns("*.wav"))
        return dst

    def edit_claim(self, dst, cid, fn):
        path = dst / "research/sources.json"
        d = json.loads(path.read_text())
        fn(next(c for c in d["claims"] if c["id"] == cid))
        path.write_text(json.dumps(d))

    def test_approval_needs_a_record_for_the_current_narration_revision(self):
        with tempfile.TemporaryDirectory() as tmp:
            dst = self.copy_pilot(tmp)
            self.edit_claim(dst, "CLM_101", lambda c: c.update(review_status="EDITORIALLY_APPROVED"))
            errors, _ = validate_project(dst)
            self.assertTrue(any("CLM_101: EDITORIALLY_APPROVED needs" in e for e in errors), errors)
            self.edit_claim(dst, "CLM_101", lambda c: c.update(editorial_approval={
                "approved_by": "Editor", "approved_on": "2026-11-01", "narration_revision": "m3.5-r0"}))
            errors, _ = validate_project(dst)
            self.assertTrue(any("approval is for narration 'm3.5-r0'" in e for e in errors), errors)
            self.edit_claim(dst, "CLM_101", lambda c: c["editorial_approval"].update(narration_revision="m3.5-r1"))
            errors, _ = validate_project(dst)
            self.assertFalse(any("CLM_101" in e for e in errors), errors)

    def test_no_claim_in_the_pilot_is_self_approved(self):
        claims = load("research/sources.json")["claims"]
        self.assertFalse([c["id"] for c in claims if c["review_status"] == "EDITORIALLY_APPROVED"])
        self.assertNotEqual(load("project.json")["factual_review"], "verified")

    def test_missing_citations_are_errors(self):
        with tempfile.TemporaryDirectory() as tmp:
            dst = self.copy_pilot(tmp)
            self.edit_claim(dst, "CLM_104", lambda c: c["evidence"][0].update(excerpt=""))
            path = dst / "research/sources.json"
            d = json.loads(path.read_text())
            d["sources"][1]["url"] = ""
            path.write_text(json.dumps(d))
            errors, _ = validate_project(dst)
            self.assertTrue(any("CLM_104" in e and "excerpt" in e for e in errors), errors)
            self.assertTrue(any("SRC_002 has no url" in e for e in errors), errors)
            n = json.loads((dst / "script/narration.json").read_text())
            n["beats"][2]["claim_ids"].append("CLM_777")
            (dst / "script/narration.json").write_text(json.dumps(n))
            errors, _ = validate_project(dst)
            self.assertTrue(any("CLM_777 is not in research/sources.json" in e for e in errors), errors)


class PublicationReadinessTest(unittest.TestCase):
    def test_pilot_is_blocked_for_the_right_reasons(self):
        errors, _ = validate_project(PILOT, final=True)
        joined = " ".join(errors)
        for needle in ("EDITORIALLY_APPROVED", "NOT_CLEARED", "INTERNAL_PREVIEW_ONLY, not PUBLICATION_CLEARED",
                       "PRON_001", "factual_review"):
            self.assertIn(needle, joined)

    def test_audio_provenance_passes_only_when_cleared_everywhere(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)
            (p / "audio").mkdir()
            manifest = {"segments": {"k1": {"provider": "omnivoice", "rights_class": "PUBLICATION_CLEARED"}},
                        "beats": {"B1": {"sentences": [{"cache_key": "k1", "text": "x"}]}}}
            (p / "audio/narration_manifest.json").write_text(json.dumps(manifest))
            n = {"voice": {"provider": "omnivoice"}, "beats": [{"id": "B1", "sentences": ["In Babergh."]}]}
            lex = copy.deepcopy(PronunciationTest.LEX)
            cleared = registry("PUBLICATION_CLEARED", {"cleared_by": "x", "cleared_on": "y", "evidence": "z"})
            self.assertTrue(any("PRON" not in e and "P1" in e for e in publication_audio_errors(p, n, cleared, lex)))
            lex["entries"][0].update(status="CONFIRMED", confirmed_by="L", confirmed_on="2026-11-01")
            self.assertEqual(publication_audio_errors(p, n, cleared, lex), [])
            # a record claiming clearance is not enough if the registry no longer clears the provider
            self.assertTrue(publication_audio_errors(p, n, registry(), lex))

    def test_gate_statuses_are_separate(self):
        from pipeline import gates
        result = gates.evaluate(PILOT)
        self.assertIn("EDITORIAL_REVIEW_PENDING", result["statuses"])
        self.assertIn("TTS_RIGHTS_PENDING", result["statuses"])
        self.assertNotIn("PUBLICATION_READY", result["statuses"])
        self.assertTrue(result["verdict"].startswith("INTERNAL PREVIEW"))
        self.assertTrue(set(result["statuses"]) <= set(gates.STATUSES))


if __name__ == "__main__":
    unittest.main()
