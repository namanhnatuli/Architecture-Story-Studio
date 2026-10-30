"""Asset index for planning: M4 library specs (asset_library/architecture) plus a minimal
compatibility adapter for legacy house/roof states with the M2 gable_roof builder: the states
of archived pilots kept in asset_library/legacy_states/<slug>/ (M7) and of any active project
(projects/*/storyboard/states.json). Read-only: the planner never edits the catalog."""
import json
from pathlib import Path

from engine import spec
from engine.arch import assets

ROOT = Path(__file__).resolve().parent.parent
LEGACY_TEMPLATES = ["HOLD", "HIGHLIGHT", "EXPLODED_VIEW", "REPLACE_PARTS", "SIDE_BY_SIDE"]
# Exploded-view rule of the validated M2 roof pilot (roof-evolution SC_002, archived): role -> distance
# along the builder's explode hint; gable walls stay with the house.
LEGACY_EXPLODE = {"roof_covering": 1.6, "rafters": 0.8, "ridge_beam": 0.5}


def _blender_validation(catalog, asset_id):
    for e in catalog.get("assets", []):
        if e["asset_id"] == asset_id:
            checks = (e.get("validation", {}).get("blender", {}).get("review") or {}).get("checks", {})
            offline = e.get("validation", {}).get("offline", {})
            ok = bool(checks) and all(v == "PASS" for v in checks.values()) and all(v == "PASS" for v in offline.values())
            return "VALIDATED" if ok else "OFFLINE_ONLY"
    return "NOT_IN_CATALOG"


def index(root=ROOT):
    """[entry] sorted by asset_id; entries are plain dicts (JSON-able)."""
    root = Path(root)
    cat_path = root / "asset_library/catalog/catalog.json"
    catalog = json.loads(cat_path.read_text()) if cat_path.is_file() else {}
    entries = []
    for path in sorted((root / "asset_library/architecture").rglob("*.json")):
        if "previews" in path.parts:
            continue
        data, _ = assets.load(path)
        if assets.validate(data):
            continue
        params, _ = assets.resolve_params(data["family"], data["variant"], data["parameters"])
        entries.append({"asset_id": data["asset_id"], "source": "library", "path": str(path.relative_to(root)),
                        "family": data["family"], "variant": data["variant"], "params": params,
                        "accuracy": data["accuracy"], "animation_support": data["animation_support"],
                        "validation": _blender_validation(catalog, data["asset_id"]),
                        "kind": "site" if data["family"] == "site" else "architecture"})
    sources = [(p, p.parent / "blender_checks_summary.json", p.parts[-2])
               for p in sorted((root / "asset_library/legacy_states").glob("*/states.json"))]
    sources += [(p, p.parents[1] / "qa" / "blender_checks.json", p.parts[-3])
                for p in sorted((root / "projects").glob("*/storyboard/states.json"))]
    seen = set()
    for states_path, qa, project in sources:
        if project in seen:
            continue
        states = json.loads(states_path.read_text())
        if states.get("generated_by") == "planner":     # M5 output, not a source
            continue
        base = spec.base_params(states)
        if base["builder"] != "rectangular_house_base":
            continue
        seen.add(project)
        summary = json.loads(qa.read_text()).get("summary", {}) if qa.is_file() else {}
        validated = "VALIDATED" if summary and not summary.get("failed") else "OFFLINE_ONLY"
        for v in states.get("variants", []):
            if spec.variant_builder(v) != "gable_roof":
                continue
            params = {"roof_pitch_degrees": v.get("roof_pitch_degrees"), "color_key": v.get("color_key"),
                      "covering_style": (v.get("covering") or {}).get("style")}
            entries.append({"asset_id": f"legacy_{project.replace('-', '_')}_{v['id']}", "source": "legacy_states",
                            "path": str(states_path.relative_to(root)), "project": project, "variant_id": v["id"],
                            "family": "roof", "variant": "gable_roof", "params": params, "accuracy": "ILLUSTRATIVE",
                            "animation_support": LEGACY_TEMPLATES, "validation": validated, "kind": "architecture",
                            "legacy_variant": v, "legacy_base": states.get("base"),
                            "legacy_shared": states.get("shared_components", [])})
    return sorted(entries, key=lambda e: e["asset_id"])


def component_parts(entry, owner):
    """[{id, role, group, layer, replaceable}] an entry builds when planned as variant `owner`."""
    if entry["source"] == "library":
        return [{"id": c.id, "role": c.role, "group": c.group or c.role, "layer": c.layer,
                 "replaceable": "REPLACE" in c.animation, "type": c.type}
                for c in assets.plan_cached(entry["path"], owner if entry["kind"] != "site" else "shared")]
    variant = dict(entry["legacy_variant"], id=owner)
    variant.pop("components", None)       # ids follow the new owner id
    return [{"id": p["id"], "role": p["role"], "group": p["role"], "layer": p["layer"],
             "replaceable": p["role"] not in spec.STRUCTURE_ROLES, "type": p["role"].upper()}
            for p in spec.builder_parts(variant)]
