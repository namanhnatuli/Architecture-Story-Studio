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
        narration = {"beats": [{"id": "B01", "sentences": ["x"], "claim_ids": ["CLM_1", "CLM_2"]}]}
        (self.p / "script/narration.json").write_text(json.dumps(narration))
        (self.p / "script/visual_beats.json").write_text(json.dumps({"beats": []}))
        (self.p / "script/chapters.json").write_text(json.dumps({"schema": "chapters/1", "chapters": [
            {"id": "C1", "title": "Hook", "beat_ids": ["B01"]}]}))
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


class OwnerStopTest(unittest.TestCase):
    def test_reference_film_has_its_owner_approvals_recorded(self):
        rows = rows_of(FILM)
        for stage in ("TOPIC", "RESEARCH", "SCRIPT", "CLAIM_SOURCE_VERIFICATION", "TTS", "AUDIO_LOCK", "VISUAL_PLAN",
                      "EDITORIAL_QA", "INTERNAL_REVIEW", "OWNER_APPROVAL"):
            self.assertEqual(rows[stage][0], "DONE", (stage, rows[stage]))

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
