"""Architecture asset specifications: registry, validation, planning (pure Python).

An asset spec (asset_library/architecture/<family>s/<asset_id>.json) names a family
and variant and gives parameters; `plan()` turns it into semantic components with
ids prefixed by the owning variant. Invalid specs fail with readable messages.
Schema: schemas/architecture_asset.schema.json.
"""
import json
from pathlib import Path

from engine.arch import GENERATOR_VERSION
from engine.arch import semantic
from engine.arch.families import bridge, cathedral, floating, site

ROOT = Path(__file__).resolve().parents[2]
ACCURACY_LEVELS = ("ILLUSTRATIVE", "REFERENCE_BASED", "HISTORICALLY_VERIFIED")
TEMPLATES = ("HOLD", "EXPLODED_VIEW", "SIDE_BY_SIDE", "REPLACE_PARTS", "HIGHLIGHT", "SEQUENCE")


def num(lo, hi, default=None, integer=False, odd=False, even=False):
    return {"type": "int" if integer else "number", "min": lo, "max": hi, "default": default,
            "odd": odd, "even": even}


def choice(values, default=None):
    return {"type": "choice", "values": tuple(values), "default": default}


COMMON = {"total_length_m": num(8, 80), "deck_width_m": num(2.5, 12, 4.0), "deck_level_m": num(2.5, 20, 5.0)}

FAMILIES = {
    "bridge": {
        "timber_beam": {
            "generator": bridge.timber_beam, "materials": ("timber", "timber_dark", "timber_light"),
            "animation": ("HOLD", "HIGHLIGHT", "EXPLODED_VIEW", "SIDE_BY_SIDE"),
            "params": dict(COMMON, span_count=num(1, 12, 4, integer=True), stringer_count=num(2, 8, 4, integer=True),
                           stringer_width_m=num(0.12, 0.6, 0.26), stringer_depth_m=num(0.2, 1.2, 0.46),
                           post_size_m=num(0.15, 0.6, 0.3), plank_pitch_m=num(0.12, 0.6, 0.27)),
        },
        "stone_arch": {
            "generator": bridge.stone_arch, "materials": ("stone", "stone_dark", "stone_light", "road_gravel"),
            "animation": ("HOLD", "HIGHLIGHT", "EXPLODED_VIEW", "SIDE_BY_SIDE"),
            "params": dict(COMMON, arch_count=num(1, 9, 3, integer=True), arch_type=choice(("semicircular",), "semicircular"),
                           pier_width_m=num(0.8, 5, 1.8), abutment_length_m=num(0.5, 4, 1.0),
                           ring_thickness_m=num(0.25, 1.2, 0.5), voussoirs_per_arch=num(5, 31, 13, integer=True, odd=True),
                           springing_level_m=num(0.0, 10, 0.6), deck_thickness_m=num(0.15, 1.0, 0.3),
                           parapet_thickness_m=num(0.2, 0.8, 0.4), parapet_height_m=num(0.5, 1.5, 0.9)),
        },
        "steel_truss": {
            "generator": bridge.steel_truss, "materials": ("steel", "steel_dark", "concrete", "concrete_deck"),
            "animation": ("HOLD", "HIGHLIGHT", "EXPLODED_VIEW", "SIDE_BY_SIDE", "REPLACE_PARTS"),
            "replaceable_params": ("truss_pattern",),   # variants differing only here share the frame
            "params": dict(COMMON, span_count=num(1, 6, 2, integer=True), truss_pattern=choice(("pratt", "warren"), "pratt"),
                           panels_per_span=num(2, 16, 6, integer=True, even=True), truss_height_m=num(1.0, 8.0, 2.2),
                           pier_width_m=num(0.8, 4.0, 1.6), chord_size_m=num(0.15, 0.6, 0.3),
                           web_size_m=num(0.1, 0.4, 0.2)),
        },
        # M8 long-span families: span a wider site (asset_library/architecture/sites/site_river_crossing_72.json)
        "cantilever": {
            "generator": bridge.cantilever, "materials": ("steel", "steel_dark", "concrete", "concrete_deck"),
            "animation": ("HOLD", "HIGHLIGHT", "EXPLODED_VIEW", "SIDE_BY_SIDE"),
            "params": dict(COMMON, anchor_arm_m=num(4, 30, 14.0), cantilever_arm_m=num(3, 25, 11.0),
                           depth_over_piers_m=num(3, 20, 9.0), depth_end_m=num(1.5, 8, 3.5), depth_tip_m=num(1.5, 8, 4.0),
                           panels_anchor=num(2, 16, 6, integer=True, even=True),
                           panels_cantilever=num(2, 12, 4, integer=True, even=True),
                           panels_suspended=num(2, 16, 6, integer=True, even=True), pier_width_m=num(1.0, 6.0, 2.4),
                           chord_size_m=num(0.15, 0.6, 0.32), web_size_m=num(0.1, 0.4, 0.2)),
        },
        "suspension": {
            "generator": bridge.suspension, "materials": ("steel", "steel_dark", "cable", "concrete", "concrete_deck"),
            "animation": ("HOLD", "HIGHLIGHT", "EXPLODED_VIEW", "SIDE_BY_SIDE"),
            "params": dict(COMMON, main_span_m=num(10, 70, 44.0), tower_height_m=num(3, 25, 7.0),
                           sag_ratio=num(0.06, 0.16, 0.11), hanger_spacing_m=num(1.0, 6.0, 2.0),
                           stiffening_depth_m=num(0.5, 3.0, 1.3), anchorage_offset_m=num(1.5, 10, 3.2),
                           cable_size_m=num(0.15, 0.6, 0.3), tower_size_m=num(0.4, 2.0, 0.8)),
        },
        "cable_stayed": {
            "generator": bridge.cable_stayed, "materials": ("cable", "concrete", "concrete_deck"),
            "animation": ("HOLD", "HIGHLIGHT", "EXPLODED_VIEW", "SIDE_BY_SIDE"),
            "params": dict(COMMON, main_span_m=num(10, 70, 40.0), pylon_height_m=num(4, 30, 11.0),
                           stays_per_side=num(2, 10, 5, integer=True), girder_depth_m=num(0.4, 2.0, 0.8),
                           pylon_size_m=num(0.5, 2.0, 0.9), stay_size_m=num(0.06, 0.3, 0.14)),
        },
    },
    # Sections through a few bays, for the worm's-eye axonometric camera (preset CATHEDRAL_FROM_BELOW)
    "cathedral": {
        "gothic_section": {
            "generator": cathedral.gothic_section,
            "materials": ("stone", "stone_dark", "stone_light", "stained_glass", "roof_lead"),
            "animation": ("HOLD", "HIGHLIGHT", "SEQUENCE"),
            "params": {"bay_count": num(1, 6, 3, integer=True), "web_courses": num(1, 12, 1, integer=True), "bay_length_m": num(4, 12, 7.5), "nave_half_width_m": num(4, 12, 7.0),
                       "aisle_width_m": num(3, 12, 7.0), "pier_radius_m": num(0.4, 1.6, 0.8), "vault_spring_m": num(10, 40, 26.0),
                       "vault_crown_m": num(15, 55, 42.0), "arcade_top_m": num(8, 30, 20.0), "arcade_rise_m": num(2, 12, 7.0),
                       "triforium_top_m": num(9, 35, 24.0), "window_spring_m": num(10, 45, 31.0), "window_rise_m": num(2, 12, 6.5),
                       "upper_wall_thickness_m": num(0.3, 1.5, 0.7), "rib_width_m": num(0.2, 1.0, 0.45), "rib_depth_m": num(0.2, 1.2, 0.7),
                       "aisle_spring_m": num(4, 16, 11.0), "aisle_crown_m": num(6, 24, 17.5), "aisle_top_m": num(6, 24, 18.5),
                       "ridge_m": num(20, 70, 52.0), "pier_buttress_depth_m": num(2, 10, 5.5), "pier_buttress_width_m": num(1, 4, 1.9),
                       "pier_buttress_top_m": num(10, 50, 32.0), "pinnacle_shaft_m": num(1, 10, 3.5), "pinnacle_spire_m": num(1, 10, 4.5),
                       "flyer_head_m": num(10, 50, 34.0), "flyer_width_m": num(0.5, 2.5, 1.1)},
        },
        "romanesque_section": {
            "generator": cathedral.romanesque_section,
            "materials": ("stone", "stone_dark", "stone_light", "stained_glass", "roof_lead"),
            "animation": ("HOLD", "HIGHLIGHT", "SEQUENCE"),
            "params": {"bay_count": num(1, 6, 3, integer=True), "bay_length_m": num(4, 12, 7.5), "interior_half_width_m": num(3, 10, 6.0),
                       "wall_thickness_m": num(1, 4, 2.4), "wall_height_m": num(6, 25, 13.0), "vault_thickness_m": num(0.5, 2.5, 1.1),
                       "window_half_width_m": num(0.4, 1.5, 0.7), "window_spring_m": num(3, 18, 9.0), "buttress_depth_m": num(0.3, 1.5, 0.6),
                       "buttress_width_m": num(0.8, 3.0, 1.6), "roof_rise_m": num(2, 10, 4.5)},
        },
    },
    # Floating structures (projects/floating-city-design-challenge): the draft comes from the project's calculation
    "floating": {
        "platform": {
            "generator": floating.platform,
            "materials": ("concrete", "concrete_deck", "plaster", "roof_membrane", "section_poche", "highlight_gold",
                          "displaced_water", "water_cut"),
            "animation": ("HOLD", "HIGHLIGHT", "EXPLODED_VIEW", "SEQUENCE"),
            "params": {"length_m": num(10, 120, 40.0), "width_m": num(10, 120, 40.0), "hull_depth_m": num(1.5, 10, 4.0),
                       "draft_m": num(0.3, 9.5, 2.958), "slab_m": num(0.1, 0.6, 0.25), "wall_m": num(0.1, 0.6, 0.25),
                       "bulkhead_m": num(0.1, 0.5, 0.2), "bulkhead_spacing_m": num(4, 30, 10.0),
                       "building_cover": num(0.0, 0.8, 0.4), "storeys": num(0, 6, 3, integer=True),
                       "storey_height_m": num(2.6, 4.0, 3.0), "extension_m": num(0.0, 2.0, 0.0),
                       "section": num(0, 1, 0, integer=True), "water_depth_m": num(4, 60, 15.0)},
        },
    },
    "site": {
        "bay": {
            "generator": floating.bay, "materials": ("water", "water_cut", "seabed", "seabed_cut", "section_poche"),
            "animation": ("HOLD",),
            "params": {"site_width_m": num(40, 2000, 140.0), "site_length_m": num(40, 2000, 120.0),
                       "water_depth_m": num(4, 60, 15.0), "section": num(0, 1, 0, integer=True),
                       "hole_length_m": num(0, 200, 0.0), "hole_width_m": num(0, 200, 0.0)},
        },
        "level_ground": {
            "generator": site.level_ground, "materials": ("stone_dark",), "animation": ("HOLD",),
            "params": {"site_width_m": num(10, 120, 64.0), "site_length_m": num(10, 120, 36.0), "front_margin_m": num(0, 20, 3.0)},
        },
        "river_crossing": {
            "generator": site.river_crossing, "materials": ("earth_bank", "water"), "animation": ("HOLD",),
            "params": {"gap_m": num(8, 80, 24.0), "deck_level_m": num(2.5, 20, 5.0), "site_width_m": num(6, 40, 12.0),
                       "bank_length_m": num(2, 20, 4.0), "water_level_m": num(-0.3, 5, 0.3)},
        },
    },
}


class AssetError(ValueError):
    """An architecture asset specification is invalid (message lists every problem)."""


def resolve_params(family, variant, given):
    """Defaults + given parameters; returns (params, errors)."""
    schema = FAMILIES[family][variant]["params"]
    errors = [f"unknown parameter '{k}' for {family}/{variant} (known: {', '.join(sorted(schema))})"
              for k in given if k not in schema]
    params = {}
    for key, rule in schema.items():
        value = given.get(key, rule.get("default"))
        if value is None:
            errors.append(f"parameter '{key}' is required for {family}/{variant}")
            continue
        if rule["type"] == "choice":
            if value not in rule["values"]:
                errors.append(f"parameter '{key}' must be one of {list(rule['values'])}, got {value!r}")
        else:
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                errors.append(f"parameter '{key}' must be a number, got {value!r}")
                continue
            if rule["type"] == "int" and int(value) != value:
                errors.append(f"parameter '{key}' must be a whole number, got {value!r}")
            if not rule["min"] <= value <= rule["max"]:
                errors.append(f"parameter '{key}' = {value} is outside {rule['min']}..{rule['max']}")
            if rule.get("odd") and int(value) % 2 == 0:
                errors.append(f"parameter '{key}' must be odd (keystone at the crown), got {value}")
            if rule.get("even") and int(value) % 2:
                errors.append(f"parameter '{key}' must be even, got {value}")
            if rule["type"] == "int":
                value = int(value)
        params[key] = value
    return params, errors


def compatibility_errors(family, variant, p):
    """Cross-parameter geometry checks (beyond single-parameter ranges)."""
    if family == "floating" and variant == "platform":
        return floating.compatibility_errors(p)
    if family != "bridge":
        return []
    errors = []
    if variant == "stone_arch":
        lay = bridge.stone_arch_layout(p)
        if lay["span"] <= 0.5:
            errors.append(f"stone_arch: {p['arch_count']} arches with {p['pier_width_m']} m piers leave "
                          f"{lay['span']:.2f} m per arch; use fewer arches or narrower piers")
        if p["pier_width_m"] < 2 * p["ring_thickness_m"] + 0.1:
            errors.append("stone_arch: pier_width_m must exceed two ring thicknesses (both rings spring from it)")
        if lay["cover"] < 0.15:
            errors.append(f"stone_arch: arch crown (extrados {lay['crown_extrados']:.2f} m) leaves {lay['cover']:.2f} m "
                          f"under the deck (needs >= 0.15 m): raise deck_level_m or use more, smaller arches")
        if lay["radius"] > 0 and lay["radius"] * 3.14159 / p["voussoirs_per_arch"] > 1.6:
            errors.append("stone_arch: voussoirs longer than 1.6 m along the arch; increase voussoirs_per_arch")
    if variant == "timber_beam":
        span = (p["total_length_m"] - 0.7) / p["span_count"]
        if span > 9.0:
            errors.append(f"timber_beam: {span:.1f} m between bents exceeds 9 m; add spans (illustrative limit)")
        if p["stringer_depth_m"] + 0.09 + 0.34 > p["deck_level_m"] - 0.5:
            errors.append("timber_beam: deck_level_m too low for stringers, cap beams and posts")
    if variant == "steel_truss":
        lay = bridge.steel_truss_layout(p)
        lengths = [b - a for a, b in lay["spans"]]
        if min(lengths) <= 2.0:
            errors.append("steel_truss: spans shorter than 2 m; reduce span_count or pier_width_m")
        panel = min(lengths) / p["panels_per_span"]
        ratio = p["truss_height_m"] / panel
        if not 0.5 <= ratio <= 3.0:
            errors.append(f"steel_truss: truss height / panel length = {ratio:.2f} (diagonals too flat or steep); "
                          "keep it between 0.5 and 3.0")
    if variant == "suspension":
        lay = bridge.suspension_layout(p)
        if lay["side"] < 4.0:
            errors.append(f"suspension: side spans of {lay['side']:.1f} m; main_span_m leaves too little room for the towers")
        if lay["clearance"] < 0.8:
            errors.append(f"suspension: the cable dips to {lay['clearance']:.2f} m above the deck at mid-span (needs >= 0.8 m "
                          "for the hangers): raise tower_height_m or lower sag_ratio")
        if p["tower_height_m"] < bridge.THROUGH_CLEARANCE_M + 1.0:
            errors.append("suspension: tower_height_m must leave road clearance under the top strut "
                          f"(>= {bridge.THROUGH_CLEARANCE_M + 1.0} m)")
    if variant == "cable_stayed":
        lay = bridge.cable_stayed_layout(p)
        if lay["side"] < 4.0:
            errors.append(f"cable_stayed: side spans of {lay['side']:.1f} m are too short for the stays")
        if lay["flattest_deg"] < 22.0:   # FHWA-IF-12-052 vol. 5, 2.5: not less than about 22 degrees
            errors.append(f"cable_stayed: the flattest stay is at {lay['flattest_deg']:.1f} deg; stays flatter than about "
                          "22 deg carry the vertical load inefficiently (raise pylon_height_m or shorten main_span_m)")
        if p["pylon_height_m"] - 0.55 * p["stays_per_side"] - 0.6 < bridge.THROUGH_CLEARANCE_M:
            errors.append("cable_stayed: the pylon strut below the stay anchorages would block the road; raise pylon_height_m")
    if variant == "cantilever":
        lay = bridge.cantilever_layout(p)
        if lay["suspended_m"] < 4.0:
            errors.append(f"cantilever: the suspended span is {lay['suspended_m']:.1f} m; shorten the arms")
        if not p["depth_over_piers_m"] > max(p["depth_end_m"], p["depth_tip_m"]):
            errors.append("cantilever: the truss must be deepest over the main piers")
    return errors


def load(path):
    path = Path(path)
    if not path.is_absolute():
        path = ROOT / path
    try:
        return json.loads(path.read_text(encoding="utf-8")), path
    except (OSError, json.JSONDecodeError) as e:
        raise AssetError(f"cannot read architecture asset {path}: {e}") from None


def validate(spec_data, where="asset"):
    """Errors in an asset spec (empty list when valid). G4-A, specification part."""
    errors = []
    for key in ("asset_id", "family", "variant", "units", "parameters", "accuracy", "animation_support"):
        if key not in spec_data:
            errors.append(f"{where}: missing '{key}'")
    if errors:
        return errors
    aid = spec_data["asset_id"]
    if not isinstance(aid, str) or not aid or not all(c.isalnum() or c == "_" for c in aid):
        errors.append(f"{where}: asset_id must be [A-Za-z0-9_]")
    family, variant = spec_data["family"], spec_data["variant"]
    if family not in FAMILIES:
        return errors + [f"{where}: unknown family '{family}' (known: {', '.join(FAMILIES)})"]
    if variant not in FAMILIES[family]:
        return errors + [f"{where}: unknown {family} variant '{variant}' (known: {', '.join(FAMILIES[family])})"]
    if spec_data["units"] != "METRIC":
        errors.append(f"{where}: units must be METRIC (metres), got {spec_data['units']!r}")
    if not isinstance(spec_data["parameters"], dict):
        return errors + [f"{where}: parameters must be an object"]
    params, perr = resolve_params(family, variant, spec_data["parameters"])
    errors += [f"{where}: {e}" for e in perr]
    if not perr:
        errors += [f"{where}: {e}" for e in compatibility_errors(family, variant, params)]
    if spec_data["accuracy"] not in ACCURACY_LEVELS:
        errors.append(f"{where}: accuracy must be one of {ACCURACY_LEVELS}")
    elif spec_data["accuracy"] == "HISTORICALLY_VERIFIED" and not (spec_data.get("provenance") or {}).get("claim_ids"):
        errors.append(f"{where}: HISTORICALLY_VERIFIED needs provenance.claim_ids backed by the research ledger")
    elif spec_data["accuracy"] == "REFERENCE_BASED" and not (spec_data.get("provenance") or {}).get("references"):
        errors.append(f"{where}: REFERENCE_BASED needs provenance.references")
    supported = FAMILIES[family][variant]["animation"]
    bad = [a for a in spec_data["animation_support"] if a not in supported]
    if bad:
        errors.append(f"{where}: animation_support {bad} not supported by {family}/{variant} (supported: {list(supported)})")
    gen = spec_data.get("generator") or {}
    if gen and gen.get("name") != f"{family}.{variant}":
        errors.append(f"{where}: generator.name must be '{family}.{variant}'")
    return errors


def plan(spec_data, owner="shared", where="asset"):
    """Semantic components for a valid spec; ids prefixed with `owner` unless shared."""
    errors = validate(spec_data, where)
    if errors:
        raise AssetError("; ".join(errors))
    family, variant = spec_data["family"], spec_data["variant"]
    params, _ = resolve_params(family, variant, spec_data["parameters"])
    comps = FAMILIES[family][variant]["generator"](params)
    for c in comps:
        c.variant = owner
        if owner != "shared":
            c.id = f"{owner}_{c.id}"
    cerr = semantic.validate_components(comps)
    if cerr:
        raise AssetError(f"{where}: generator produced invalid components: " + "; ".join(cerr[:8]))
    return comps


def plan_file(path, owner="shared"):
    data, resolved = load(path)
    return plan(data, owner, where=str(path))


_CACHE = {}


def plan_cached(path, owner="shared"):
    """plan_file memoised on (file content, owner); callers must not mutate the result."""
    import hashlib
    data, resolved = load(path)
    key = (str(resolved), hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest(), owner)
    if key not in _CACHE:
        _CACHE[key] = plan(data, owner, where=str(path))
    return _CACHE[key]


def site_for(path):
    """The library site whose gap and deck level a bridge spans (M8: the long-span bridges have their
    own wider site), as a repository-relative path; None when no site matches."""
    data, _ = load(path)
    if data.get("family") == "cathedral":
        return "asset_library/architecture/sites/site_level_ground.json"
    if data.get("family") == "floating":   # the bay drawn the same way (section or not) with this hull kept dry
        p = resolve_params(data["family"], data["variant"], data["parameters"])[0]
        for site in sorted((ROOT / "asset_library/architecture/sites").glob("*.json")):
            s, _ = load(site)
            if s["variant"] != "bay":
                continue
            sp = resolve_params(s["family"], s["variant"], s["parameters"])[0]
            same_cut = sp["section"] == p["section"]
            hole_ok = not p["section"] or (abs(sp["hole_length_m"] - p["length_m"]) < 1e-6 and abs(sp["hole_width_m"] - p["width_m"]) < 1e-6)
            if same_cut and hole_ok and abs(sp["water_depth_m"] - p["water_depth_m"]) < 1e-6:
                return str(site.relative_to(ROOT))
        return None
    if data.get("family") != "bridge":
        return None
    p = resolve_params(data["family"], data["variant"], data["parameters"])[0]
    for site in sorted((ROOT / "asset_library/architecture/sites").glob("*.json")):
        s, _ = load(site)
        if s["variant"] != "river_crossing":
            continue
        sp = resolve_params(s["family"], s["variant"], s["parameters"])[0]
        if abs(sp["gap_m"] - p["total_length_m"]) < 1e-6 and abs(sp["deck_level_m"] - p["deck_level_m"]) < 1e-6:
            return str(site.relative_to(ROOT))
    return None


def resolved_params_file(path):
    data, _ = load(path)
    return data, resolve_params(data["family"], data["variant"], data["parameters"])[0]


def describe(spec_data):
    """Catalog metadata that does not need Blender."""
    comps = plan(spec_data)
    lo, hi = semantic.union_bbox(comps)
    counts = {}
    for c in comps:
        counts[c.type] = counts.get(c.type, 0) + 1
    signatures = {semantic.mesh_signature(c.mesh, c.material) for c in comps}
    family, variant = spec_data["family"], spec_data["variant"]
    return {"components": len(comps), "unique_meshes": len(signatures), "by_type": dict(sorted(counts.items())),
            "verts": sum(len(c.mesh["verts"]) for c in comps), "faces": sum(len(c.mesh["faces"]) for c in comps),
            "bbox": [[round(v, 3) for v in lo], [round(v, 3) for v in hi]],
            "dimensions_m": [round(hi[i] - lo[i], 3) for i in range(3)],
            "materials": sorted({c.material for c in comps}),
            "generator": {"name": f"{family}.{variant}", "version": GENERATOR_VERSION},
            "resolved_parameters": resolve_params(family, variant, spec_data["parameters"])[0]}


EXPLODE_PRESETS = {("bridge", "timber_beam"): "timber_beam", ("bridge", "stone_arch"): "stone_arch",
                   ("bridge", "steel_truss"): "steel_truss", ("bridge", "cantilever"): "cantilever",
                   ("bridge", "suspension"): "suspension", ("bridge", "cable_stayed"): "cable_stayed"}


def explode_offsets(spec_data, comps):
    """{component id: (dx, dy, dz)} recommended for an exploded view of this asset."""
    if spec_data["family"] == "floating":
        return floating.explode_offsets(comps)
    key = EXPLODE_PRESETS.get((spec_data["family"], spec_data["variant"]))
    return bridge.explode_offsets(key, comps) if key else {}


def explode_per_component(path, owner):
    """EXPLODED_VIEW `per_component` config (direction + distance) from the preset."""
    import math
    data, _ = load(path)
    out = {}
    for cid, v in explode_offsets(data, plan_cached(path, owner)).items():
        d = math.sqrt(sum(x * x for x in v))
        out[cid] = {"direction": [round(x / d, 5) for x in v], "distance": round(d, 4)}
    return out

