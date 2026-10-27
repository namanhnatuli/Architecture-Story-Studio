"""M4: architecture specifications, semantic components, procedural geometry, assets (no Blender)."""
import copy
import json
import math
import shutil
import tempfile
import unittest
from pathlib import Path

from engine import framing, spec, templates
from engine.arch import assets, checks, library as L, primitives as P, semantic
from engine.arch.families import bridge
from engine.arch.families.site import GROUND_Z
from tools import render_cache
from tools.cli import ROOT
from tools.validator import validate_project

LIB = ROOT / "asset_library" / "architecture"
BRIDGES = {p.stem: p for p in (LIB / "bridges").glob("*.json")}
SITE = LIB / "sites" / "site_river_crossing_24.json"
PILOT = ROOT / "projects" / "bridge-structure-evolution"


def spec_of(name):
    return json.loads(BRIDGES[name].read_text())


class SpecificationTest(unittest.TestCase):
    def test_every_library_asset_is_valid(self):
        self.assertGreaterEqual(len(BRIDGES), 5)
        for path in list(BRIDGES.values()) + [SITE]:
            data = json.loads(path.read_text())
            self.assertEqual(assets.validate(data), [], path.name)
            self.assertEqual(data["accuracy"], "ILLUSTRATIVE", "no asset may claim more than it has evidence for")

    def test_schema_file_matches_the_validator(self):
        schema = json.loads((ROOT / "schemas/architecture_asset.schema.json").read_text())
        self.assertEqual(set(schema["required"]),
                         {"asset_id", "family", "variant", "units", "parameters", "accuracy", "animation_support"})
        self.assertEqual(schema["properties"]["accuracy"]["enum"], list(assets.ACCURACY_LEVELS))
        self.assertEqual(set(schema["properties"]["family"]["enum"]), set(assets.FAMILIES))

    def test_invalid_parameters_fail_with_readable_messages(self):
        base = spec_of("bridge_stone_arch_03")
        cases = [
            ({"family": "aqueduct"}, "unknown family 'aqueduct'"),
            ({"variant": "suspension"}, "unknown bridge variant 'suspension'"),
            ({"units": "IMPERIAL"}, "units must be METRIC"),
            ({"parameters": dict(base["parameters"], voussoirs_per_arch=12)}, "must be odd"),
            ({"parameters": dict(base["parameters"], arch_count=40)}, "outside 1..9"),
            ({"parameters": dict(base["parameters"], colour="red")}, "unknown parameter 'colour'"),
            ({"parameters": dict(base["parameters"], arch_count="three")}, "must be a number"),
            ({"parameters": dict(base["parameters"], arch_count=1, deck_level_m=6.0, springing_level_m=0.6)},
             "leaves"),   # one 22 m arch: crown above the deck
            ({"accuracy": "HISTORICALLY_VERIFIED"}, "needs provenance.claim_ids"),
            ({"accuracy": "REFERENCE_BASED", "provenance": {}}, "needs provenance.references"),
            ({"animation_support": ["REPLACE_PARTS"]}, "not supported by bridge/stone_arch"),
        ]
        for change, needle in cases:
            data = dict(copy.deepcopy(base), **change)
            errors = " ".join(assets.validate(data))
            self.assertIn(needle, errors, change)
            with self.assertRaises(assets.AssetError):
                assets.plan(data)

    def test_cross_parameter_geometry_checks(self):
        truss = spec_of("bridge_steel_truss_pratt_01")
        flat = dict(truss, parameters=dict(truss["parameters"], truss_height_m=1.0, panels_per_span=2))
        self.assertTrue(any("diagonals too flat" in e for e in assets.validate(flat)))
        timber = spec_of("bridge_timber_beam_01")
        long = dict(timber, parameters=dict(timber["parameters"], span_count=2))
        self.assertTrue(any("exceeds 9 m" in e for e in assets.validate(long)))


class SemanticComponentTest(unittest.TestCase):
    def test_ids_are_stable_unique_prefixed_and_slot_safe(self):
        for name in BRIDGES:
            a = [c.id for c in assets.plan(spec_of(name), "v1")]
            b = [c.id for c in assets.plan(spec_of(name), "v1")]
            self.assertEqual(a, b)
            self.assertEqual(len(a), len(set(a)))
            self.assertTrue(all(i.startswith("v1_") and "." not in i for i in a))

    def test_every_component_has_semantic_metadata(self):
        for name in BRIDGES:
            for c in assets.plan(spec_of(name)):
                self.assertIn(c.type, semantic.SEMANTIC_TYPES)
                self.assertTrue(c.material and c.group)
                rec = semantic.component_record(c)
                self.assertTrue(all(d > 0 for d in rec["dimensions"]), c.id)
                if "EXPLODE" in c.animation:
                    self.assertIsNotNone(c.hint, f"{c.id} can explode but has no direction")

    def test_validate_components_catches_defects(self):
        good = assets.plan(spec_of("bridge_timber_beam_01"))
        bad = copy.deepcopy(good[:2])
        bad[1].id = bad[0].id
        bad[0].type = "BRIDGE"
        bad[0].hint = (0, 0, 0)
        errors = " ".join(semantic.validate_components(bad))
        for needle in ("duplicate component id", "unknown semantic type", "non-zero 3-vector"):
            self.assertIn(needle, errors)

    def test_expected_counts_and_dimensions(self):
        for name in BRIDGES:
            data = spec_of(name)
            comps = assets.plan(data)
            params, _ = assets.resolve_params(data["family"], data["variant"], data["parameters"])
            failed = [(c, d) for c, ok, d in checks.check_asset(data, comps, params) if not ok]
            self.assertEqual(failed, [], name)
            lo, hi = semantic.union_bbox(comps)
            self.assertAlmostEqual(lo[2], GROUND_Z, places=6)
            self.assertAlmostEqual(hi[0] - lo[0], 24.0, delta=0.25)

    def test_floating_and_overlap_detection(self):
        comps = assets.plan(spec_of("bridge_stone_arch_03"))
        deck = next(c for c in comps if c.type == "DECK")
        deck.location = (0.0, 0.0, 3.0)   # lifted clear of the parapets (at 1 m it still touches them)
        _, floating = checks.connectivity(comps)
        self.assertIn(deck.id, floating)
        comps = assets.plan(spec_of("bridge_stone_arch_03"))
        pier = next(c for c in comps if c.type == "PIER")
        abut = next(c for c in comps if c.type == "ABUTMENT")
        pier.location = (abut.location[0] + semantic.bbox(abut)[0][0] + 0.5, 0.0, 0.0)   # pushed into the abutment
        self.assertTrue(checks.intersections(comps))


class GeometryLibraryTest(unittest.TestCase):
    def test_primitives(self):
        b = P.box((2, 4, 6), (1, 1, 1))
        lo = [min(v[i] for v in b["verts"]) for i in range(3)]
        self.assertEqual(lo, [0, -1, -2])
        m = P.member((0, 0, 0), (3, 0, 4), 0.2, 0.2)
        self.assertEqual(len(m["verts"]), 8)
        self.assertAlmostEqual(max(v[2] for v in m["verts"]) - min(v[2] for v in m["verts"]), 4 + 0.2 * 0.6, places=6)
        s = P.sector(1.0, 1.5, 0.0, math.pi / 2, 1.0, segments=4)
        radii = {round(math.hypot(x, z), 6) for x, _, z in s["verts"]}
        self.assertEqual(radii, {1.0, 1.5})
        self.assertEqual(len(P.prism_xz([(0, 0), (1, 0), (1, 1), (0, 1)], 2.0)["faces"]), 6)

    def test_arch_and_rotation_conventions(self):
        angles = L.arch_angles(13)
        self.assertAlmostEqual(angles[0][0], math.pi)
        self.assertAlmostEqual(angles[-1][1], 0.0)
        with self.assertRaises(ValueError):
            L.arch_angles(12)
        # A crown-direction point rotated for angle theta lands at angle theta (Blender Euler XYZ)
        c = semantic.Component("x", "VOUSSOIR", "stone", P.box((0.1, 0.1, 0.1), (0, 0, 2.0)),
                               rotation=L.rotation_for_angle(math.radians(30)))
        x, _, z = semantic.to_world(c, (0.0, 0.0, 2.0))
        self.assertAlmostEqual(math.degrees(math.atan2(z, x)), 30.0, places=6)

    def test_truss_patterns_follow_the_documented_arrangement(self):
        bottom, top = L.truss_nodes(12.0, 2.0, 6)
        pratt = L.truss_web("pratt", bottom, top)
        self.assertEqual(sum(1 for k, _, _ in pratt if k == "TRUSS_VERTICAL"), 5)
        for kind, a, b in pratt:   # diagonals descend towards the centre (CLM_001)
            if kind == "TRUSS_DIAGONAL":
                high, low = (a, b) if a[1] > b[1] else (b, a)
                self.assertLess(abs(low[0]), abs(high[0]) + 1e-9)
        warren = L.truss_web("warren", bottom, top)
        self.assertEqual({k for k, _, _ in warren}, {"TRUSS_DIAGONAL"})   # no verticals (CLM_002)
        for (_, a, b), (_, c, d) in zip(warren, warren[1:]):   # alternating up / down
            self.assertNotEqual(a[1] < b[1], c[1] < d[1])
        with self.assertRaises(ValueError):
            L.truss_web("howe", bottom, top)

    def test_identical_parts_share_meshes(self):
        comps = assets.plan(spec_of("bridge_stone_arch_03"))
        voussoirs = {semantic.mesh_signature(c.mesh) for c in comps if c.type == "VOUSSOIR"}
        self.assertEqual(len(voussoirs), 1)
        bents = {semantic.mesh_signature(c.mesh) for c in assets.plan(spec_of("bridge_timber_beam_01"))
                 if c.type == "SUPPORT"}
        self.assertEqual(len(bents), 1)

    def test_repeatable_generation(self):
        for name in BRIDGES:
            a = [semantic.component_record(c) for c in assets.plan(spec_of(name))]
            b = [semantic.component_record(c) for c in assets.plan(spec_of(name))]
            self.assertEqual(a, b)

    def test_parameterisation_changes_counts(self):
        three = assets.plan(spec_of("bridge_stone_arch_03"))
        five = assets.plan(spec_of("bridge_stone_arch_05"))
        self.assertEqual(sum(c.type == "KEYSTONE" for c in three), 3)
        self.assertEqual(sum(c.type == "KEYSTONE" for c in five), 5)
        self.assertEqual(sum(c.type == "PIER" for c in five), 4)


class FamilyAndMaterialTest(unittest.TestCase):
    def test_family_registry_selects_generators(self):
        self.assertIs(assets.FAMILIES["bridge"]["stone_arch"]["generator"], bridge.stone_arch)
        self.assertEqual(set(assets.FAMILIES["bridge"]), {"timber_beam", "stone_arch", "steel_truss"})
        kinds = {spec_of(n)["variant"] for n in BRIDGES}
        self.assertEqual(kinds, {"timber_beam", "stone_arch", "steel_truss"})

    def test_materials_exist_in_the_shared_library(self):
        lib = json.loads((ROOT / "asset_library/materials/stylized_materials.json").read_text())
        keys = set(lib["materials"])
        self.assertEqual(keys, {k for v in lib["categories"].values() for k in v})
        for name in list(BRIDGES) + ["site"]:
            data = spec_of(name) if name != "site" else json.loads(SITE.read_text())
            used = {c.material for c in assets.plan(data)}
            self.assertTrue(used <= keys, used - keys)
            self.assertTrue(used <= set(assets.FAMILIES[data["family"]][data["variant"]]["materials"]))
        for m in lib["materials"].values():
            self.assertRegex(m["color"], r"^#[0-9A-Fa-f]{6}$")
            self.assertTrue(0 <= m["roughness"] <= 1)


class AnimationCompatibilityTest(unittest.TestCase):
    def setUp(self):
        self.states = json.loads((PILOT / "storyboard/states.json").read_text())

    def test_pilot_validates_every_template_offline(self):
        errors, _ = validate_project(PILOT)
        self.assertEqual(errors, [])
        story = json.loads((PILOT / "storyboard/storyboard.json").read_text())
        used = {s["animation"]["template"] for s in story["shots"]}
        self.assertEqual(used, {"HOLD", "EXPLODED_VIEW", "REPLACE_PARTS", "SIDE_BY_SIDE"})
        self.assertTrue(any(s["animation"].get("highlight") for s in story["shots"]))

    def test_structure_from_shares_the_frame_and_replaces_only_the_web(self):
        warren = spec.state_parts(self.states, "steel_truss_warren")
        own = [p["id"] for p in spec.variant_parts(spec.variant_map(self.states)["steel_truss_warren"])]
        self.assertTrue(own and all("diagonals" in i for i in own))
        out_ids, in_ids = templates.replace_sets(self.states, "steel_truss", "steel_truss_warren")
        self.assertTrue(all(("verticals" in i or "diagonals" in i) and i.startswith("steel_truss_span") for i in out_ids))
        self.assertEqual(sorted(in_ids), sorted(own))
        frame = [p for p in warren if p["id"] not in own]
        self.assertTrue(any("chords" in p["id"] for p in frame))

    def test_structure_from_rules_for_assets(self):
        s = copy.deepcopy(self.states)
        v = next(v for v in s["variants"] if v["id"] == "steel_truss_warren")
        v["structure_from"] = "stone_arch"
        self.assertTrue(any("is a bridge/stone_arch" in e for e in spec.validate_states(s)))
        with tempfile.TemporaryDirectory() as tmp:
            alt = json.loads(BRIDGES["bridge_steel_truss_warren_01"].read_text())
            alt["parameters"]["truss_height_m"] = 2.4
            path = Path(tmp) / "alt.json"
            path.write_text(json.dumps(alt))
            s2 = copy.deepcopy(self.states)
            w = next(v for v in s2["variants"] if v["id"] == "steel_truss_warren")
            w["asset"] = str(path)
            self.assertTrue(any("differs in ['truss_height_m']" in e for e in spec.validate_states(s2)))

    def test_explode_presets_match_the_pilot_storyboard(self):
        story = json.loads((PILOT / "storyboard/storyboard.json").read_text())
        for shot_id, path, owner in (("SC_004", BRIDGES["bridge_stone_arch_03"], "stone_arch"),):
            per = next(s for s in story["shots"] if s["id"] == shot_id)["animation"]["per_component"]
            preset = assets.explode_per_component(path, owner)
            self.assertEqual(set(per), set(preset))
            for cid, o in per.items():
                d = o["direction"]
                vec = [0, 1, 0] if d == "BACK" else d
                for a, b in zip([x * o["distance"] for x in vec],
                                [x * preset[cid]["distance"] for x in preset[cid]["direction"]]):
                    self.assertAlmostEqual(a, b, places=3)

    def test_stack_layout_rows_never_overlap_on_screen(self):
        basis = framing.camera_basis(-78.0, 24.0)
        models = [semantic.world_verts(c) for c in assets.plan(spec_of("bridge_steel_truss_pratt_01"))]
        pts = [p for m in models for p in m]
        offs, gap = framing.layout_stack([pts, pts, pts], basis, 0.5)
        up = basis[1]
        rows = [[sum((p[i] + o[i]) * up[i] for i in range(3)) for p in pts] for o in offs]
        for r1, r2 in zip(rows, rows[1:]):
            self.assertGreater(min(r1) - max(r2), 0.0)
        right = basis[0]
        self.assertAlmostEqual(sum(offs[0][i] * right[i] for i in range(3)), 0.0, places=9)


class ReuseAndCacheTest(unittest.TestCase):
    def _project(self, tmp, variants):
        p = Path(tmp) / "reuse-demo"
        (p / "storyboard").mkdir(parents=True)
        (p / "project.json").write_text(json.dumps({"slug": "reuse-demo", "fps": 24}))
        (p / "storyboard/states.json").write_text(json.dumps({
            "schema_version": 2, "base": {"builder": "architecture_asset", "asset": str(SITE.relative_to(ROOT))},
            "shared_components": ["banks", "water"], "variants": variants}))
        return p

    def test_library_asset_loads_in_another_project(self):
        with tempfile.TemporaryDirectory() as tmp:
            v = [{"id": "five_arches", "builder": "architecture_asset",
                  "asset": str(BRIDGES["bridge_stone_arch_05"].relative_to(ROOT))}]
            p = self._project(tmp, v)
            states = json.loads((p / "storyboard/states.json").read_text())
            self.assertEqual(spec.validate_states(states), [])
            ids = spec.state_ids(states, "five_arches")
            self.assertEqual(sum("keystone" in i for i in ids), 5)
            shot = {"id": "S1", "duration_seconds": 2.0, "animation": {"template": "HOLD", "state": "five_arches"}}
            slots = templates.placeholder_slots(shot, states)
            plan = templates.plan_shot(shot, states, 24, slots)
            self.assertEqual(plan.frame_count, 48)

    def test_asset_must_fit_the_site(self):
        with tempfile.TemporaryDirectory() as tmp:
            data = spec_of("bridge_timber_beam_01")
            data["parameters"]["total_length_m"] = 30.0
            data["parameters"]["span_count"] = 5
            path = Path(tmp) / "long.json"
            path.write_text(json.dumps(data))
            p = self._project(tmp, [{"id": "long", "builder": "architecture_asset", "asset": str(path)}])
            errors = spec.validate_states(json.loads((p / "storyboard/states.json").read_text()))
            self.assertTrue(any("does not fit the site's gap_m" in e for e in errors), errors)

    def test_render_cache_tracks_referenced_assets_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            asset = Path(tmp) / "a.json"
            asset.write_text(BRIDGES["bridge_timber_beam_01"].read_text())
            p = self._project(tmp, [{"id": "t", "builder": "architecture_asset", "asset": str(asset)}])
            shot = {"id": "S1", "duration_seconds": 2.0, "animation": {"template": "HOLD", "state": "t"}}
            before = render_cache.components(p, shot, "preview")
            unrelated = Path(tmp) / "unused.json"
            unrelated.write_text("{}")
            self.assertEqual(before, render_cache.components(p, shot, "preview"))
            data = json.loads(asset.read_text())
            data["parameters"]["plank_pitch_m"] = 0.3
            asset.write_text(json.dumps(data))
            manifest = {"key_version": render_cache.KEY_VERSION, "components": before}
            self.assertEqual(render_cache.stale_reasons(manifest, render_cache.components(p, shot, "preview")),
                             ["assets"])

    def test_engine_dependency_is_recursive(self):
        names = {str(f.relative_to(ROOT / "engine")) for f in render_cache.engine_files()}
        self.assertIn("arch/families/bridge.py", names)
        self.assertNotIn("qa_checks.py", names)


if __name__ == "__main__":
    unittest.main()
