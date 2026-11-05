"""M3 narration pipeline: cache, scheduling, validation, assembly, gates (no OmniVoice needed)."""
import copy
import json
import shutil
import subprocess
import tempfile
import unittest
import wave
from pathlib import Path

from engine import motion, spec, templates
from integrations.tts import omnivoice as ov
from pipeline import assemble, asr_check, beat_scheduler, narration as nar
from tests.fake_omnivoice import FakeOmniVoice
from tools.cli import ROOT
from tools.validator import validate_project

LEGACY = ROOT / "tests" / "fixtures" / "legacy_projects"   # archived pilots kept as regression fixtures (M7)

PILOT = LEGACY / "suffolk-roofs"
HAS_FFMPEG = bool(shutil.which("ffmpeg") and shutil.which("ffprobe"))


def load(rel):
    return json.loads((PILOT / rel).read_text())


def write_wav(path, seconds, rate=24000, amplitude=8000):
    import math
    import struct
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        n = int(round(seconds * rate))
        w.writeframes(b"".join(struct.pack("<h", int(amplitude * math.sin(i / 7))) for i in range(n)))


def fake_manifest(narration, durations):
    """Measured-audio stand-in: each sentence `durations[beat]` seconds, joined with the pause."""
    pause = narration["pacing"]["sentence_pause_seconds"]
    beats = {}
    for b in narration["beats"]:
        t, sents = 0.0, []
        for i, text in enumerate(b["sentences"]):
            if i:
                t += pause
            d = durations.get(b["id"], 2.0)
            sents.append({"index": i, "text": text, "start": t, "end": t + d, "cache_key": f"{b['id']}{i}"})
            t += d
        beats[b["id"]] = {"file": f"audio/beats/{b['id']}.wav", "duration": t, "sha256": "x", "sentences": sents}
    return {"beats": beats, "segments": {}, "narration_sha256": nar.narration_hash(narration)}


class ScheduleTest(unittest.TestCase):
    def setUp(self):
        self.narration = load("script/narration.json")
        self.template = load("storyboard/storyboard.template.json")
        self.states = load("storyboard/states.json")

    def schedule(self, durations=None, template=None):
        manifest = fake_manifest(self.narration, durations or {})
        return beat_scheduler.schedule(self.narration, manifest, template or self.template, self.states, 24)

    def test_shots_are_whole_frames_contiguous_and_cover_narration(self):
        story, timing = self.schedule()
        frame = 0
        for shot, t in zip(story["shots"], timing["shots"]):
            self.assertEqual(t["start_frame"], frame)
            self.assertAlmostEqual(shot["duration_seconds"] * 24, t["frames"], places=9)
            self.assertGreaterEqual(t["frames"] / 24, t["narration_seconds"] - 1e-9)
            frame += t["frames"]
        self.assertEqual(frame, timing["total_frames"])
        for beat in timing["beats"]:      # every sentence sits inside its shot
            shot = next(s for s in timing["shots"] if s["id"] == beat["shot"])
            for s in beat["sentences"]:
                self.assertGreaterEqual(s["start"], shot["start_seconds"])
                self.assertLessEqual(s["end"], shot["start_seconds"] + shot["duration_seconds"])

    def test_anchors_resolve_relative_to_shot_start(self):
        story, timing = self.schedule({"B3": 3.0})
        sc003 = next(s for s in story["shots"] if s["id"] == "SC_003")
        lead = self.narration["pacing"]["beat_lead_in_seconds"]
        self.assertAlmostEqual(sc003["animation"]["hold_start_seconds"], lead + 0.4)
        card = next(s for s in story["shots"] if s["id"] == "SC_004")
        rail = next(e for e in card["graphic"]["elements"] if e["id"] == "rail")
        b4 = next(b for b in timing["beats"] if b["id"] == "B4")
        self.assertAlmostEqual(card["start_seconds"] + rail["appear"], b4["sentences"][2]["start"], places=5)

    def test_short_narration_extends_shot_for_animation_never_stretches_audio(self):
        story, timing = self.schedule({"B3": 0.5})
        t = next(s for s in timing["shots"] if s["id"] == "SC_003")
        self.assertTrue(t["extended_by_animation"])
        self.assertGreater(t["duration_seconds"], t["narration_seconds"])
        b3 = next(b for b in timing["beats"] if b["id"] == "B3")
        self.assertAlmostEqual(b3["duration"], 0.5 * 2 + self.narration["pacing"]["sentence_pause_seconds"])

    def test_beats_must_be_covered_in_order(self):
        bad = copy.deepcopy(self.template)
        bad["shots"][0]["beat_ids"], bad["shots"][1]["beat_ids"] = ["B2"], ["B1"]
        with self.assertRaisesRegex(beat_scheduler.ScheduleError, "every beat exactly once"):
            self.schedule(template=bad)

    def test_bad_anchor(self):
        bad = copy.deepcopy(self.template)
        bad["shots"][2]["animation"]["hold_start_seconds"] = "@B9.s0"
        with self.assertRaisesRegex(beat_scheduler.ScheduleError, "not in this shot"):
            self.schedule(template=bad)


class NarrationValidationTest(unittest.TestCase):
    def setUp(self):
        self.narration = load("script/narration.json")
        self.sources = load("research/sources.json")

    def test_pilot_is_valid(self):
        self.assertEqual(nar.validate(self.narration, self.sources), [])

    def test_missing_voice_licensing_information(self):
        n = copy.deepcopy(self.narration)
        n["voice"]["license"] = {}
        errors = nar.validate(n, self.sources)
        self.assertTrue(any("license.status" in e for e in errors), errors)
        self.assertTrue(any("components is empty" in e for e in errors), errors)

    def test_missing_source_ids_and_rejected_claims(self):
        s = copy.deepcopy(self.sources)
        next(c for c in s["claims"] if c["id"] == "CLM_102")["source_ids"] = []
        n = copy.deepcopy(self.narration)
        n["beats"][0]["claim_ids"].append("CLM_006")
        errors = nar.validate(n, s)
        self.assertTrue(any("CLM_102 has no source_ids" in e for e in errors), errors)
        self.assertTrue(any("CLM_006 is REJECTED" in e for e in errors), errors)

    def test_fact_beat_needs_claims(self):
        n = copy.deepcopy(self.narration)
        n["beats"][1]["claim_ids"] = []
        self.assertTrue(any("must cite claim_ids" in e for e in nar.validate(n, self.sources)))


class GateTest(unittest.TestCase):
    def test_final_gate_blocks_pilot(self):
        errors, _ = validate_project(PILOT, final=True)
        joined = " ".join(errors)
        self.assertIn("EDITORIALLY_APPROVED", joined)
        self.assertIn("NOT_CLEARED", joined)
        self.assertIn("unapproved assets", joined)

    def test_source_verified_claim_needs_locator_and_excerpt(self):
        with tempfile.TemporaryDirectory() as tmp:
            dst = Path(tmp) / "suffolk-roofs"
            shutil.copytree(PILOT, dst, ignore=shutil.ignore_patterns("renders", "output", "scenes", "audio", "qa"))
            src = json.loads((dst / "research/sources.json").read_text())
            next(c for c in src["claims"] if c["id"] == "CLM_107")["evidence"][0]["excerpt"] = ""
            (dst / "research/sources.json").write_text(json.dumps(src))
            errors, _ = validate_project(dst)
            self.assertTrue(any("CLM_107" in e and "excerpt" in e for e in errors), errors)


class StateOwnershipTest(unittest.TestCase):
    def setUp(self):
        self.states = load("storyboard/states.json")

    def test_structure_from_shares_structure_and_replace_moves_only_the_covering(self):
        out_ids, in_ids = templates.replace_sets(self.states, "thatch_50", "plain_tile_50")
        self.assertEqual({spec.variant_parts(spec.variant_map(self.states)["thatch_50"])[0]["role"]}, {"gable_wall"})
        roles = {p["id"]: p["role"] for v in self.states["variants"] for p in v["components"]}
        self.assertEqual({roles[i] for i in out_ids + in_ids}, {"roof_covering", "ridge_cap"})
        out2, in2 = templates.replace_sets(self.states, "plain_tile_50", "slate_30")
        self.assertIn("thatch_50_rafters_left", out2)   # inherited structure leaves with the tile roof

    def test_structure_from_rules(self):
        s = copy.deepcopy(self.states)
        s["variants"][1]["roof_pitch_degrees"] = 45
        self.assertTrue(any("same builder and pitch" in e for e in spec.validate_states(s)))

    def test_intro_never_fades_in_hidden_source_covering(self):
        """Regression (M3): the tile slot builds the thatch variant for its structure; its thatch
        covering is hidden and must not get transparency keys (fade twins would un-hide it)."""
        story = load("storyboard/storyboard.json")
        shot = next(s for s in story["shots"] if s["id"] == "SC_006")
        plan = templates.plan_shot(shot, self.states, 24, templates.placeholder_slots(shot, self.states))
        self.assertFalse([n for n in plan.tracks if n.startswith("plain_tile_50.thatch_50_covering")])
        self.assertTrue([n for n in plan.tracks if n.startswith("plain_tile_50.plain_tile_50_covering")])


class CacheTest(unittest.TestCase):
    @unittest.skipUnless(HAS_FFMPEG, "ffmpeg required")
    def test_identical_requests_reuse_audio(self):
        with tempfile.TemporaryDirectory() as tmp, FakeOmniVoice() as fake:
            p = Path(tmp) / "demo"
            (p / "script").mkdir(parents=True)
            (p / "research").mkdir()
            sources = {"sources": [{"id": "S1", "url": "https://example.org"}],
                       "claims": [{"id": "C1", "text": "x", "source_ids": ["S1"], "review_status": "SOURCE_VERIFIED",
                                   "evidence": [{"source_id": "S1", "locator": "p1", "excerpt": "x"}]}]}
            (p / "research/sources.json").write_text(json.dumps(sources))
            narration = {"voice": {"provider": "omnivoice", "id": "t", "mode": "design", "language": "English",
                                   "design": {"gender": "Male"}, "params": {},
                                   "license": {"status": "NOT_CLEARED", "rights_class": "INTERNAL_PREVIEW_ONLY",
                                               "components": [{"name": "x"}]}},
                         "pacing": {"sentence_pause_seconds": 0.3, "beat_lead_in_seconds": 0.3, "beat_tail_seconds": 0.5},
                         "beats": [{"id": "B1", "kind": "fact", "claim_ids": ["C1"],
                                    "sentences": ["Hello there friend, this is a test.", "Hello there friend, this is a test."]}]}
            (p / "script/narration.json").write_text(json.dumps(narration))
            client = ov.OmniVoiceClient(base_url=fake.url, retries=0, model_revision="r1")
            first = nar.generate(p, client, log=lambda *a: None)
            self.assertEqual(len(fake.calls), 1)          # two identical sentences -> one generation
            nar.generate(p, client, log=lambda *a: None)
            self.assertEqual(len(fake.calls), 1)          # second run fully cached
            beat = first["beats"]["B1"]
            self.assertAlmostEqual(beat["duration"], 2.0 + 0.3 + 2.0, places=3)
            self.assertAlmostEqual(beat["sentences"][1]["start"], 2.3, places=3)
            nar.generate(p, ov.OmniVoiceClient(base_url=fake.url, retries=0, model_revision="r2"), log=lambda *a: None)
            self.assertEqual(len(fake.calls), 2)          # new model revision -> new cache key


class AsrNormalisationTest(unittest.TestCase):
    def test_numbers_and_ordinals(self):
        self.assertEqual(asr_check.wer("about fifty degrees in the eighteenth century", "about 50 degrees in the 18th century"), 0.0)
        self.assertAlmostEqual(asr_check.wer("a b c d", "a b x d"), 0.25)


@unittest.skipUnless(HAS_FFMPEG, "ffmpeg required")
class AssemblyTest(unittest.TestCase):
    def test_track_mux_srt_and_drift(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)
            write_wav(p / "audio/beats/B1.wav", 1.5)
            write_wav(p / "audio/beats/B2.wav", 1.0)
            timing = {"fps": 24, "total_frames": 96, "total_seconds": 4.0,
                      "shots": [{"id": "S1", "start_frame": 0, "frames": 48}, {"id": "S2", "start_frame": 48, "frames": 48}],
                      "beats": [{"id": "B1", "shot": "S1", "audio_file": "audio/beats/B1.wav", "start_seconds": 0.25,
                                 "duration": 1.5, "sentences": [{"index": 0, "text": "One.", "start": 0.25, "end": 1.75}]},
                                {"id": "B2", "shot": "S2", "audio_file": "audio/beats/B2.wav", "start_seconds": 2.25,
                                 "duration": 1.0, "sentences": [{"index": 0, "text": "Two.", "start": 2.25, "end": 3.25}]}]}
            (p / "script").mkdir()
            (p / "script/timing.json").write_text(json.dumps(timing))
            video = p / "v.mp4"
            subprocess.run(["ffmpeg", "-v", "error", "-f", "lavfi", "-i", "color=c=gray:s=160x90:r=24:d=4",
                            "-pix_fmt", "yuv420p", str(video)], check=True)
            report = assemble.assemble(p, video, p / "out.mp4", log=lambda *a: None)
            self.assertEqual(report["problems"], [])
            self.assertEqual(report["frames"], 96)
            srt = (p / "out.en.srt").read_text()
            # cue = measured sentence span + up to 0.25 s lead-out into the following pause (M3.5)
            self.assertIn("00:00:00,250 --> 00:00:02,000", srt)
            self.assertIn("00:00:02,250 --> 00:00:03,500", srt)
            with wave.open(str(p / "audio/narration_track_full.wav")) as w:
                self.assertEqual(w.getnframes(), 96 * 1000)   # 24 kHz / 24 fps = 1000 samples per frame

    def test_overlapping_beats_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)
            write_wav(p / "a.wav", 1.0)
            timing = {"fps": 24, "shots": [{"id": "S1", "start_frame": 0, "frames": 48}],
                      "beats": [{"id": "B1", "shot": "S1", "audio_file": "a.wav", "start_seconds": 0.2},
                                {"id": "B2", "shot": "S1", "audio_file": "a.wav", "start_seconds": 0.8}]}
            with self.assertRaisesRegex(ValueError, "overlaps"):
                assemble.build_narration_track(p, timing, p / "t.wav")


if __name__ == "__main__":
    unittest.main()
