"""2026-11-12: recorded sounds a project lists with their licence (audio/sound_plan.json), extra cues anchored to
storyboard steps, chapter cues on real cuts, and short beds under one shot (pipeline/sound.py). Offline: FFmpeg on
synthetic tones, no Blender, no downloaded file."""
import copy
import hashlib
import json
import math
import subprocess
import tempfile
import unittest
from pathlib import Path

from pipeline import sound
from tools import cli
from tools.cli import ROOT

SR = 24000


def tone(path, seconds, freq=220, delay=0.0):
    """A sine burst, `delay` s of silence first (a known onset and a known loudest moment)."""
    subprocess.run([cli.ffmpeg_bin(), "-v", "error", "-y", "-f", "lavfi", "-i", f"sine=frequency={freq}:duration={seconds}",
                    "-af", f"adelay={int(delay * 1000)},volume=0.5", "-ar", str(SR), "-ac", "1", str(path)], check=True)


def plan_for(root):
    f = root / "sfx" / "tone.wav"
    f.parent.mkdir(parents=True, exist_ok=True)
    tone(f, 0.4, delay=0.2)
    bed = root / "sfx" / "bed.wav"
    tone(bed, 6.0, freq=150)
    src = lambda path: {"file": str(path.relative_to(root)), "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),  # noqa: E731
                        "page": "https://example.invalid/x", "artist": "test", "license": "test licence",
                        "license_url": "https://example.invalid/l", "checked_on": "2099-01-01"}
    return {"schema": "sound_plan/1", "bed_under_narration_db": 20.0,
            "sources": {"tone": src(f), "bed": src(bed)},
            "kinds": {"HIT": {"source": "tone", "seconds": 0.6},
                      "PEAKY": {"source": "tone", "seconds": 0.6, "align": "peak"},
                      "WASH": {"source": "bed", "seconds": 6.0, "bed": True}},
            "replace": {"STONE": "HIT"},
            "cues": [{"shot": "B", "step": 1, "do": "REVEAL", "edge": "end", "offset": 0.1, "kind": "HIT"}],
            "chapter_cues": {"kind": "PEAKY", "offset": -0.1},
            "beds": [{"shot": "B", "from": 0.5, "to": {"view": 1, "edge": "end"}, "kind": "WASH", "fade_in": 0.5, "fade_out": 0.5}]}


SHOTS = [{"id": "A", "duration_seconds": 4.0, "animation": {"steps": [], "views": [{}]}},
         {"id": "B", "duration_seconds": 5.0,
          "animation": {"views": [{}, {"start_seconds": 1.0, "move_seconds": 2.0}],
                        "steps": [{"do": "MOVE", "start_seconds": 0.5, "seconds": 1.0},
                                  {"do": "REVEAL", "start_seconds": 1.0, "seconds": 1.2}]}}]


class SoundPlanCheckTest(unittest.TestCase):
    def test_a_complete_plan_passes_and_every_gap_is_named(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            plan = plan_for(root)
            self.assertEqual(sound.check_plan(plan, root), [])
            bad = copy.deepcopy(plan)
            del bad["sources"]["tone"]["license"]
            self.assertTrue(any("no license" in x for x in sound.check_plan(bad, root)))
            bad = copy.deepcopy(plan)
            bad["sources"]["tone"]["sha256"] = "0" * 64
            self.assertTrue(any("not the recorded file" in x for x in sound.check_plan(bad, root)))
            bad = copy.deepcopy(plan)
            bad["kinds"]["STONE"] = dict(plan["kinds"]["HIT"])
            self.assertTrue(any("synthesised kind" in x for x in sound.check_plan(bad, root)))
            bad = copy.deepcopy(plan)
            bad["beds"][0]["kind"] = "HIT"
            self.assertTrue(any("not a bed" in x for x in sound.check_plan(bad, root)))

    def test_the_film_plan_records_a_licence_for_every_source(self):
        plan = sound.load_plan(ROOT / "projects/floating-city-design-challenge")
        if not plan:
            self.skipTest("no sound plan")
        for sid, src in plan["sources"].items():
            self.assertTrue(all(src.get(k) for k in sound.SOURCE_FIELDS), sid)
            self.assertEqual(len(src["sha256"]), 64, sid)


class SoundPlanResolveTest(unittest.TestCase):
    def test_cues_follow_their_step_and_chapter_cues_need_a_real_cut(self):
        plan = plan_for(Path(tempfile.mkdtemp()))
        ids = ["A", "B"]
        cues, beds, problems = sound.resolve_plan(plan, SHOTS, ids, ids, {"A": 0.0, "B": 4.0}, ["B"])
        self.assertEqual(problems, [])
        hit = next(c for c in cues if c["kind"] == "HIT")
        self.assertAlmostEqual(hit["at_seconds"], 4.0 + 1.0 + 1.2 + 0.1)   # the REVEAL lands, +0.1 s
        chapter = next(c for c in cues if c.get("chapter"))
        self.assertAlmostEqual(chapter["at_seconds"], 3.9)
        self.assertEqual((beds[0]["from_seconds"], beds[0]["to_seconds"]), (4.5, 7.0))   # to the second view's arrival
        alone, _, _ = sound.resolve_plan(plan, SHOTS, ids, ["B"], {"B": 0.0}, ["B"])
        self.assertFalse(any(c.get("chapter") for c in alone))   # no cut into B in an excerpt of B alone

    def test_a_cue_on_a_step_that_moved_is_refused(self):
        plan = plan_for(Path(tempfile.mkdtemp()))
        plan["cues"][0]["step"] = 0   # a MOVE now, not the REVEAL the cue was written for
        _, _, problems = sound.resolve_plan(plan, SHOTS, ["A", "B"], ["A", "B"], {"A": 0.0, "B": 4.0}, [])
        self.assertTrue(problems and "not a REVEAL step" in problems[0])


class SoundPlanMixTest(unittest.TestCase):
    def test_recorded_sounds_land_on_their_cue_and_the_bed_sits_under_the_speech(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            plan = plan_for(root)
            x = sound.recorded("HIT", plan, SR, root)
            self.assertAlmostEqual(max(abs(v) for v in x), 1.0, places=6)
            onset = next(i for i, v in enumerate(x) if abs(v) > 0.05) / SR
            self.assertAlmostEqual(onset, 0.2, delta=0.01)
            n = 10 * SR
            narration = [8000 * math.sin(2 * math.pi * 300 * i / SR) if 1 * SR < i < 9 * SR else 0.0 for i in range(n)]
            cues = [{"at_seconds": 2.0, "kind": "STONE"}, {"at_seconds": 5.0, "kind": "PEAKY"}]
            beds = [{"from_seconds": 3.0, "to_seconds": 8.0, "kind": "WASH", "fade_in": 0.5, "fade_out": 0.5, "shot": "B"}]
            mixed, report = sound.mix_under(narration, cues, SR, plan=plan, beds=beds, root=root)
            fx = [m - a for m, a in zip(mixed, narration)]
            # STONE plays the recorded HIT: its tone starts 0.2 s into the stretch, the stretch starts at the cue
            first = next(i for i, v in enumerate(fx[:int(2.9 * SR)]) if abs(v) > 50) / SR
            self.assertAlmostEqual(first, 2.0 - 0.03 + 0.2, delta=0.02)
            # PEAKY: its loudest moment falls on the cue
            w = int(0.02 * SR)
            around = [sum(v * v for v in fx[i:i + w]) for i in range(int(4.7 * SR), int(5.3 * SR), w)]
            loudest = (int(4.7 * SR) + around.index(max(around)) * w + w // 2) / SR
            self.assertAlmostEqual(loudest, 5.0, delta=0.04)
            self.assertAlmostEqual(report["bed_rms"] / report["speech_rms"], 10 ** (-20 / 20), places=3)
            self.assertEqual(report["clipped_samples"], 0)

    def test_without_a_plan_the_mix_is_unchanged(self):
        n = 3 * SR
        narration = [6000 * math.sin(2 * math.pi * 200 * i / SR) for i in range(n)]
        cues = [{"at_seconds": 1.0, "kind": "STONE"}]
        a, ra = sound.mix_under(narration, cues, SR)
        b, rb = sound.mix_under(narration, cues, SR, plan=None, beds=())
        self.assertEqual(a, b)
        self.assertEqual(set(ra), {"cues", "narration_peak", "effect_peak", "under_narration_db", "clipped_samples"})


if __name__ == "__main__":
    unittest.main()
