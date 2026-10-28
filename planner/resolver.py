"""Architecture asset resolution: narrative concept -> asset (with an explanation).

Statuses:
  REUSE_EXISTING                 a validated library asset matches family, variant and parameters
  ADAPT_EXISTING_ASSET           a legacy house/roof variant matches (compatibility adapter)
  GENERATE_FROM_SUPPORTED_FAMILY no asset matches, but the family/variant generator exists: a new
                                 spec is proposed (written to the project, never to the catalog)
  NEW_ASSET_REQUIRED             the concept is known but no generator exists: a spec stub and a
                                 generation task are reported
  BLOCKED_MISSING_EVIDENCE       the beat needs more accuracy than any matching asset has
  UNKNOWN_CONCEPT                not in config/visual_vocabulary.json
"""
import hashlib
import json

from engine.arch import assets
from planner import vocabulary as V

ACCURACY_RANK = {"ILLUSTRATIVE": 0, "REFERENCE_BASED": 1, "HISTORICALLY_VERIFIED": 2}
EXECUTABLE = ("REUSE_EXISTING", "ADAPT_EXISTING_ASSET", "GENERATE_FROM_SUPPORTED_FAMILY")


def _rank(entry, family_defaults):
    """Prefer validated library assets, then the fewest parameters off the family defaults."""
    off = sum(1 for k, v in family_defaults.items() if entry["params"].get(k) != v)
    return ({"VALIDATED": 0, "OFFLINE_ONLY": 1}.get(entry["validation"], 2), entry["source"] != "library", off,
            entry["asset_id"])


def resolve(concept, vocab, index, required_accuracy="ILLUSTRATIVE", site=None):
    """Resolution dict for one site/architecture concept."""
    c = vocab.get(concept)
    if c is None:
        return {"concept": concept, "status": "UNKNOWN_CONCEPT",
                "explanation": f"'{concept}' is not in config/visual_vocabulary.json; add it (with family/variant or "
                               "roles) or use one of the known concepts"}
    if c["kind"] not in ("site", "architecture"):
        return {"concept": concept, "status": "UNKNOWN_CONCEPT",
                "explanation": f"'{concept}' is a {c['kind']} concept, not an architecture or site"}
    family, variant, where = c["family"], c["variant"], c.get("where") or {}
    supported = c.get("supported", True) and (
        (family in assets.FAMILIES and variant in assets.FAMILIES[family]) or family == "roof")
    if not supported:
        stub = {"schema": "architecture_asset/1", "asset_id": f"{family}_{variant}_01", "family": family,
                "variant": variant, "units": "METRIC", "parameters": dict(where), "accuracy": "ILLUSTRATIVE",
                "animation_support": ["HOLD", "HIGHLIGHT"]}
        return {"concept": concept, "status": "NEW_ASSET_REQUIRED", "proposed_spec": stub,
                "task": {"kind": "NEW_FAMILY_GENERATOR", "family": family, "variant": variant,
                         "steps": [f"write engine/arch/families/{family}.py:{variant}(params)",
                                   "register params/materials/animation in engine/arch/assets.py FAMILIES",
                                   "add explode preset + expected counts + tests",
                                   "asset-check, asset-render --preset review, look at the images"],
                         "estimate": "1-3 days for a simplified illustrative archetype"},
                "explanation": f"'{concept}' ({family}/{variant}) has no generator yet; nothing was substituted"}
    defaults = {}
    if family in assets.FAMILIES:
        defaults, _ = assets.resolve_params(family, variant, {})
    candidates = [e for e in index if e["family"] == family and e["variant"] == variant and V.matches(e["params"], where)]
    if site:   # bridges must fit the shared site (same gap and deck level)
        candidates = [e for e in candidates if e["kind"] == "site" or site_fits(e, site)]
    need = ACCURACY_RANK.get(required_accuracy, 0)
    if candidates and all(ACCURACY_RANK[e["accuracy"]] < need for e in candidates):
        return {"concept": concept, "status": "BLOCKED_MISSING_EVIDENCE",
                "explanation": f"the beat needs {required_accuracy}; matching assets are only "
                               f"{sorted({e['accuracy'] for e in candidates})} (illustrative models cannot stand in "
                               "for a documented structure)"}
    candidates = [e for e in candidates if ACCURACY_RANK[e["accuracy"]] >= need]
    if candidates:
        best = sorted(candidates, key=lambda e: _rank(e, defaults))[0]
        status = "REUSE_EXISTING" if best["source"] == "library" else "ADAPT_EXISTING_ASSET"
        why = (f"{best['asset_id']} ({best['validation'].lower().replace('_', ' ')}, {best['accuracy']}) matches "
               f"{family}/{variant}" + (f" with {where}" if where else ""))
        if status == "ADAPT_EXISTING_ASSET":
            why += f"; legacy {best['project']} variant '{best['variant_id']}' used through the M5 adapter"
        if len(candidates) > 1:
            why += f"; preferred over {[e['asset_id'] for e in sorted(candidates, key=lambda e: _rank(e, defaults))[1:]]}"
        return {"concept": concept, "status": status, "asset_id": best["asset_id"], "entry": best, "explanation": why}
    if need > 0:
        return {"concept": concept, "status": "BLOCKED_MISSING_EVIDENCE",
                "explanation": f"no {required_accuracy} asset for {family}/{variant}; generated assets are ILLUSTRATIVE"}
    if family not in assets.FAMILIES:
        return {"concept": concept, "status": "NEW_ASSET_REQUIRED",
                "explanation": f"no {family}/{variant} asset matches {where} and the family cannot generate new ones"}
    params = dict(defaults, **{k: v for k, v in where.items() if not isinstance(v, dict)})
    if site:
        params.update(total_length_m=site["params"]["gap_m"], deck_level_m=site["params"]["deck_level_m"])
    key = hashlib.sha256(json.dumps(params, sort_keys=True).encode()).hexdigest()[:6]
    spec_data = {"schema": "architecture_asset/1", "asset_id": f"{family}_{variant}_gen_{key}",
                 "title": f"Generated {family}/{variant} for concept '{concept}'", "family": family, "variant": variant,
                 "units": "METRIC", "generator": {"name": f"{family}.{variant}", "version": "1.0.0"},
                 "parameters": params, "visual_style": "premium_stylized", "accuracy": "ILLUSTRATIVE",
                 "provenance": {"basis": f"Generated by planner/ for concept '{concept}' (no catalog asset matched)."},
                 "animation_support": list(assets.FAMILIES[family][variant]["animation"])}
    errors = assets.validate(spec_data)
    if errors:
        return {"concept": concept, "status": "NEW_ASSET_REQUIRED", "proposed_spec": spec_data,
                "explanation": "generated parameters are not valid for the family: " + "; ".join(errors)}
    return {"concept": concept, "status": "GENERATE_FROM_SUPPORTED_FAMILY", "asset_id": spec_data["asset_id"],
            "generated_spec": spec_data,
            "explanation": f"no catalog asset matches {where}; generating {spec_data['asset_id']} from the supported "
                           f"{family}/{variant} generator (ILLUSTRATIVE, written under the project's planning/ folder)"}


def site_fits(entry, site):
    p, s = entry["params"], site["params"]
    return abs(p.get("total_length_m", -1) - s["gap_m"]) < 1e-6 and abs(p.get("deck_level_m", -1) - s["deck_level_m"]) < 1e-6
