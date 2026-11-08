"""Floating-city concept (projects/floating-city-design-challenge): the transparent design model obeys the physics it
cites, the scenario contract labels every value, and the evidence registry approves nothing."""
import importlib.util
import json
import math
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
P = ROOT / "projects" / "floating-city-design-challenge"


def load_model():
    spec = importlib.util.spec_from_file_location("floating_design_model", P / "analysis" / "design_model.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


@unittest.skipUnless(P.is_dir(), "floating-city concept project not present")
class DesignModelTest(unittest.TestCase):
    def setUp(self):
        self.m = load_model()

    def test_archimedes_balance(self):
        p = self.m.platform(dead=0.6)
        displaced_t = self.m.RHO_SEA * p["inputs"]["L_m"] * p["inputs"]["B_m"] * p["draft_m"] / 1000
        self.assertAlmostEqual(displaced_t, p["mass_t"]["total"], delta=0.5)
        self.assertAlmostEqual(p["freeboard_m"], p["inputs"]["H_m"] - p["draft_m"], places=3)

    def test_box_bm_equals_waterplane_inertia_over_volume(self):
        L, B, T = 40.0, 40.0, 3.0
        n = 4000                                   # numeric second moment of the waterplane about the centreline
        dy = B / n
        inertia = sum(L * ((-B / 2 + (i + 0.5) * dy) ** 2) * dy for i in range(n))
        self.assertAlmostEqual(inertia / (L * B * T), B * B / (12 * T), places=3)

    def test_draft_grows_linearly_with_added_mass(self):
        a, b = self.m.platform(dead=0.6, finishes=0.2), self.m.platform(dead=0.6, finishes=0.2 + 100 / 1600)
        self.assertAlmostEqual((b["draft_m"] - a["draft_m"]) * 100, 100e3 / (1025 * 1600) * 100, delta=0.01)

    def test_list_angle_matches_inclining_relation(self):
        deg = self.m.list_angle_deg(100, 15, 5000, 40)
        self.assertAlmostEqual(math.tan(math.radians(deg)), 100 * 15 / (5000 * 40), places=9)

    def test_results_file_is_current_and_labelled(self):
        res = json.loads((P / "analysis" / "results.json").read_text())
        self.assertEqual(res["class"], "CALCULATED_ESTIMATE")
        self.assertIn("Not a stability", res["limits"])
        fresh = self.m.platform(**{"dead": 0.6})
        self.assertAlmostEqual(res["design_A"]["mid"]["draft_m"], fresh["draft_m"], places=3)


@unittest.skipUnless(P.is_dir(), "floating-city concept project not present")
class ScenarioAndEvidenceTest(unittest.TestCase):
    def test_every_scenario_field_is_classified_with_a_basis(self):
        c = json.loads((P / "concept" / "scenario_contract.json").read_text())
        classes = set(c["classes"])
        for name, f in c["fields"].items():
            self.assertIn(f["class"], classes, name)
            self.assertTrue(f.get("basis"), name)
        self.assertEqual(c["fields"]["proposed_population"]["class"], "DESIGN_ASSUMPTION")

    def test_no_claim_is_approved_and_every_claim_is_classified(self):
        s = json.loads((P / "research" / "sources.json").read_text())
        external = {"ESTABLISHED_FACT", "SPECULATIVE_PROPOSAL", "UNVERIFIED"}
        studio = {"CALCULATED_ESTIMATE": {"SRC_STUDIO_DESIGN_MODEL"}, "DESIGN_ASSUMPTION": {"SRC_STUDIO_SCENARIO"}}
        self.assertTrue(s["claims"])
        for c in s["claims"]:
            self.assertEqual(c["review_status"], "SOURCE_VERIFIED", c["id"])
            self.assertNotIn("editorial_approval", c)
            if c["evidence_class"] in studio:   # the Studio's numbers and assumptions cite only the Studio's own files
                self.assertEqual(set(c["source_ids"]), studio[c["evidence_class"]], c["id"])
            else:
                self.assertIn(c["evidence_class"], external, c["id"])
                self.assertFalse(set(c["source_ids"]) & set(s["studio_sources"]), c["id"])
        oceanix = {c["id"]: c for c in s["claims"]}["CLM_033"]
        self.assertEqual(oceanix["evidence_class"], "UNVERIFIED")   # status of OCEANIX Busan is never stated as built


if __name__ == "__main__":
    unittest.main()
