"""G0 validator: clear errors for broken component ownership, template configs and timing."""
import copy
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from tools.cli import ROOT
from tools.validator import validate_project

SOURCE = ROOT / "projects" / "roof-evolution"


class ValidatorM2Test(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.project = Path(self.tmp.name) / "roof-evolution"
        for rel in ("project.json", "storyboard/storyboard.json", "storyboard/states.json",
                    "research/sources.json", "assets/manifest.json"):
            (self.project / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(SOURCE / rel, self.project / rel)

    def tearDown(self):
        self.tmp.cleanup()

    def edit(self, rel, fn):
        path = self.project / rel
        data = json.loads(path.read_text())
        fn(data)
        path.write_text(json.dumps(data))

    def shot(self, data, sid):
        return next(s for s in data["shots"] if s["id"] == sid)

    def errors(self):
        return validate_project(self.project)[0]

    def assertError(self, fragment):
        errors = self.errors()
        self.assertTrue(any(fragment in e for e in errors), f"{fragment!r} not in {errors}")

    def test_pilot_is_clean(self):
        self.assertEqual(self.errors(), [])

    def test_unknown_component_in_exploded_view(self):
        self.edit("storyboard/storyboard.json",
                  lambda d: self.shot(d, "SC_002")["animation"]["components"].append("roof_A_chimney"))
        self.assertError("roof_A_chimney")

    def test_shared_component_cannot_be_replaced(self):
        def fn(d):
            self.shot(d, "SC_003")["animation"]["outgoing"]["components"] = ["wall_left"]
        self.edit("storyboard/storyboard.json", fn)
        self.assertError("wall_left")

    def test_partial_replace_is_rejected(self):
        def fn(d):
            self.shot(d, "SC_003")["animation"]["incoming"]["components"] = ["roof_B_covering_left"]
        self.edit("storyboard/storyboard.json", fn)
        self.assertError("must include every component")

    def test_timing_that_does_not_fit(self):
        self.edit("storyboard/storyboard.json",
                  lambda d: self.shot(d, "SC_003")["animation"]["incoming"].update(move_seconds=5.0))
        self.assertError("SC_003: ")
        self.assertError("timing needs")
        self.assertError("lengthen the shot")

    def test_unknown_option_and_template(self):
        self.edit("storyboard/storyboard.json",
                  lambda d: self.shot(d, "SC_002")["animation"].update(explode_secs=1.0))
        self.assertError("unknown option 'explode_secs'")

        def fn(d):
            s = self.shot(d, "SC_001")
            s["transition"] = s["animation"]["template"] = "MORPH"
        self.edit("storyboard/storyboard.json", fn)
        self.assertError("unknown template 'MORPH'")

    def test_bad_key_still_marker(self):
        self.edit("storyboard/storyboard.json", lambda d: d["key_stills"][1].update(marker="nope"))
        self.assertError("marker 'nope'")

    def test_intro_state_and_highlight_order(self):
        self.edit("storyboard/storyboard.json",
                  lambda d: self.shot(d, "SC_005")["animation"]["intro"].update(from_state="roof_C"))
        self.assertError("intro.from_state must be one of")
        self.edit("storyboard/storyboard.json",
                  lambda d: self.shot(d, "SC_005")["animation"]["intro"].update(from_state="roof_B"))
        self.edit("storyboard/storyboard.json",
                  lambda d: self.shot(d, "SC_005")["animation"]["highlight"].update(start_seconds=0.5))
        self.assertError("before the intro ends")

    def test_declared_components_must_match_builder(self):
        self.edit("storyboard/states.json", lambda d: d["variants"][0]["components"].pop())
        self.assertError("components must match builder")

    def test_every_base_part_must_be_shared(self):
        self.edit("storyboard/states.json", lambda d: d["shared_components"].remove("structure"))
        self.assertError("ceiling_joists")

    def test_v1_states_and_single_replace_shot_still_validate(self):
        """Backward compatibility with the v0.1 data contract."""
        def states_v1(d):
            for v in d["variants"]:
                v.pop("components")
                v.pop("builder")
            d.pop("schema_version")
            d.pop("base")
            d["shared_components"] = ["foundation", "walls", "floor", "door", "windows", "ground", "structure"]
        self.edit("storyboard/states.json", states_v1)

        def story_v1(d):
            shot = copy.deepcopy(self.shot(d, "SC_003"))
            shot.pop("animation")
            shot.update(start_seconds=0.0, duration_seconds=6.0)
            d.clear()
            d["shots"] = [shot]
        self.edit("storyboard/storyboard.json", story_v1)
        self.edit("project.json", lambda d: d.update(duration_seconds=6.0))
        self.assertEqual(self.errors(), [])


if __name__ == "__main__":
    unittest.main()
