"""2026-11-12: the channel watermark burnt in at encode time (config/branding.json), and owner exceptions to the
visual-variety limit scoped to the runs the owner accepted (Codex review of the floating film's full cut v1).
Offline: FFmpeg on synthetic frames, no Blender."""
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from pipeline import chapters as CH
from tools import cli
from tools.cli import ROOT


def write_project(p, **fields):
    p.mkdir(parents=True, exist_ok=True)
    (p / "qa").mkdir(exist_ok=True)
    (p / "project.json").write_text(json.dumps({"slug": p.name, "fps": 24, **fields}))


class WatermarkSpecTest(unittest.TestCase):
    def test_only_projects_that_opt_in_carry_it(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "film"
            write_project(p)
            self.assertIsNone(cli.watermark_spec(p, "internal_720p"))
            # the finished films keep their verified intermediates: neither carries the watermark
            for slug in ("why-bridges-look-different", "gothic-cathedral-heights"):
                if (ROOT / "projects" / slug / "project.json").is_file():
                    self.assertIsNone(cli.watermark_spec(ROOT / "projects" / slug, "final_4k"), slug)

    def test_the_box_lies_in_the_annotation_free_subtitle_zone_at_every_size(self):
        style = json.loads((ROOT / "config/annotation_style.json").read_text())
        presets = json.loads((ROOT / "config/render_presets.json").read_text())
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "film"
            write_project(p, watermark=True)
            for preset in ("internal_720p", "internal_1080p", "final_4k"):
                wm, cfg = cli.watermark_spec(p, preset), presets[preset]
                self.assertEqual((wm["width"] % 2, wm["height"] % 2), (0, 0))
                self.assertLessEqual(cfg["height"] - wm["y"], style["subtitle_zone"] * cfg["height"], preset)
                self.assertGreaterEqual(wm["x"], 0)
                self.assertLessEqual(wm["x"] + wm["width"], cfg["width"] * style["safe_area"]["right"])
                self.assertAlmostEqual(wm["width"] / cfg["width"], 0.14, delta=0.002)

    def test_a_replaced_image_or_a_box_above_the_subtitle_zone_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "film"
            write_project(p, watermark=True)
            cfg = json.loads(cli.BRANDING.read_text())
            bad = dict(cfg, watermark=dict(cfg["watermark"], sha256="0" * 64))
            path = Path(tmp) / "branding.json"
            path.write_text(json.dumps(bad))
            with mock.patch.object(cli, "BRANDING", path), self.assertRaises(SystemExit):
                cli.watermark_spec(p, "internal_720p")
            high = dict(cfg, watermark=dict(cfg["watermark"], margin_y_fraction=0.12))
            path.write_text(json.dumps(high))
            with mock.patch.object(cli, "BRANDING", path), self.assertRaises(SystemExit):
                cli.watermark_spec(p, "internal_720p")
            top = dict(cfg, watermark=dict(cfg["watermark"], corner="TOP_RIGHT"))
            path.write_text(json.dumps(top))
            with mock.patch.object(cli, "BRANDING", path), self.assertRaises(SystemExit):
                cli.watermark_spec(p, "internal_720p")


class WatermarkEncodeTest(unittest.TestCase):
    def test_encoded_frames_carry_it_and_the_check_tells_them_apart(self):
        settings = json.loads((ROOT / "config/render_presets.json").read_text())
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "film"
            write_project(p, watermark=True)
            wm = cli.watermark_spec(p, "internal_720p")
            png = Path(tmp) / "frame.png"
            subprocess.run([cli.ffmpeg_bin(), "-v", "error", "-y", "-f", "lavfi", "-i", "color=c=0xEDEBE5:s=1280x720",
                            "-frames:v", "1", str(png)], check=True)
            videos = {}
            for name, mark in (("with", wm), ("without", None)):
                out = Path(tmp) / f"{name}.mp4"
                subprocess.run([cli.ffmpeg_bin(), "-v", "error", "-y", "-loop", "1", "-framerate", "24", "-t", "0.25",
                                "-i", str(png), *(["-i", str(ROOT / wm["image"])] if mark else []),
                                *cli.encode_args(settings, "internal_720p", mark), str(out)], check=True)
                videos[name] = out
            self.assertTrue(cli.watermark_check(p, "internal_720p", videos["with"], png, wm)["present"])
            self.assertFalse(cli.watermark_check(p, "internal_720p", videos["without"], png, wm)["present"])
            self.assertFalse((p / "qa" / "_watermark_check").exists())

    def test_bt709_conversion_follows_the_overlay_in_one_chain(self):
        settings = json.loads((ROOT / "config/render_presets.json").read_text())
        wm = {"image": "x.png", "x": 173, "y": 1894, "width": 538, "height": 180, "opacity": 0.55}
        args = cli.encode_args(settings, "final_4k", wm)
        chain = args[args.index("-filter_complex") + 1]
        self.assertLess(chain.index("overlay="), chain.index("out_color_matrix=bt709"))
        self.assertTrue(chain.endswith("[v]"))
        self.assertEqual(args[args.index("-map") + 1], "[v]")
        self.assertNotIn("-vf", args)
        self.assertIn("-vf", cli.encode_args(settings, "final_4k"))   # unchanged without a watermark
        self.assertNotIn("-filter_complex", cli.encode_args(settings, "internal_720p"))


class VarietyExceptionScopeTest(unittest.TestCase):
    RUN = {"first": "SC_008", "last": "SC_014", "length": 7, "kind": "3D_SEQUENCE",
           "shots": [f"SC_{k:03d}" for k in range(8, 15)]}
    DECIDED = {"decided_by": "TEST OWNER", "decided_on": "2099-01-01", "basis": "unit test"}

    def test_runs_of_one_kind(self):
        shots = [{"id": "a", "visual_type": "MOTION_GRAPHICS", "graphic": {"elements": [{"kind": "rect"}]}},
                 {"id": "b", "transition": "SEQUENCE"}, {"id": "c", "transition": "SEQUENCE"},
                 {"id": "d", "visual_type": "MOTION_GRAPHICS", "graphic": {"elements": [{"kind": "text"}]}}]
        runs = CH.same_kind_runs(shots)
        self.assertEqual([(r["first"], r["last"], r["length"], r["kind"]) for r in runs],
                         [("a", "a", 1, "DIAGRAM"), ("b", "c", 2, "3D_SEQUENCE"), ("d", "d", 1, "TITLE")])

    def test_an_exception_covers_exactly_the_accepted_runs(self):
        exc = dict(self.DECIDED, runs=[{k: self.RUN[k] for k in ("first", "last", "length", "kind")}])
        self.assertTrue(CH.variety_excepted(self.RUN, exc, {}))
        longer = dict(self.RUN, last="SC_015", length=8, shots=self.RUN["shots"] + ["SC_015"])
        self.assertFalse(CH.variety_excepted(longer, exc, {}))
        other = dict(self.RUN, first="SC_027", last="SC_033")
        self.assertFalse(CH.variety_excepted(other, exc, {}))
        self.assertFalse(CH.variety_excepted(self.RUN, {k: v for k, v in exc.items() if k != "basis"}, {}))

    def test_a_chapter_exception_no_longer_raises_the_limit_for_the_whole_film(self):
        exc = dict(self.DECIDED, chapter="C8", max_run=8)
        chapters = {"C8": {f"SC_{k:03d}" for k in range(31, 39)}, "C3": set(self.RUN["shots"])}
        in_c8 = dict(self.RUN, first="SC_031", last="SC_038", length=8, shots=sorted(chapters["C8"]))
        self.assertTrue(CH.variety_excepted(in_c8, exc, chapters))
        self.assertFalse(CH.variety_excepted(self.RUN, exc, chapters))   # 7 shots, but in C3


if __name__ == "__main__":
    unittest.main()
