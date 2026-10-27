"""Offline geometry validation of planned components (G4-B, pure Python).

Bounding boxes are exact for axis-aligned parts and conservative (larger) for rotated
ones, so connectivity here can only miss a gap smaller than that slack; the Blender
QA (engine/qa_checks.py, `asset` checks) repeats connectivity and intersections on the
evaluated meshes with BVH trees.
"""
import math

from engine.arch import semantic
from engine.arch.families import bridge
from engine.arch.families.site import GROUND_Z

TOUCH = 0.03     # m: boxes closer than this count as connected
# Solid masses whose AABBs are exact (axis-aligned boxes); overlaps between them are defects
# unless the pair is listed in ALLOWED_OVERLAP (designed embedding / framing).
MASSIVE = {"ABUTMENT", "PIER", "SPANDREL", "DECK", "PARAPET", "COPING", "CAP_BEAM", "STRINGER", "PLANK",
           "BEARING", "GROUND", "FLOOR_BEAM"}
ALLOWED_OVERLAP = {frozenset(p) for p in (("WATER", t) for t in semantic.SEMANTIC_TYPES)} | {
    frozenset(("FLOOR_BEAM", "DECK")),      # deck slab rests on / between floor beams
}


def expected_counts(family, variant, p):
    """Component counts implied by the parameters."""
    if family == "site":
        return {"GROUND": 2, "WATER": 1}
    if variant == "timber_beam":
        return {"SUPPORT": p["span_count"] + 1, "CAP_BEAM": p["span_count"] + 1, "STRINGER": p["span_count"],
                "PLANK": p["span_count"], "RAILING": 2}
    if variant == "stone_arch":
        n = p["arch_count"]
        return {"ABUTMENT": 2, "PIER": n - 1, "VOUSSOIR": n * (p["voussoirs_per_arch"] - 1), "KEYSTONE": n,
                "SPANDREL": 1, "DECK": 1, "PARAPET": 2, "COPING": 2}
    if variant == "steel_truss":
        s = p["span_count"]
        counts = {"ABUTMENT": 2, "PIER": s - 1, "TRUSS_CHORD": 2 * s, "END_POST": 2 * s, "TRUSS_DIAGONAL": 2 * s,
                  "JOINT": 2 * s, "FLOOR_BEAM": s, "DECK": s, "BEARING": s}
        if p["truss_height_m"] >= bridge.THROUGH_CLEARANCE_M:
            counts["BRACING"] = s
        if p["truss_pattern"] == "pratt":
            counts["TRUSS_VERTICAL"] = 2 * s
        return counts
    return {}


def _overlap(a, b, tol=0.0):
    return all(a[0][i] - tol <= b[1][i] and b[0][i] - tol <= a[1][i] for i in range(3))


def _overlap_volume(a, b):
    v = 1.0
    for i in range(3):
        d = min(a[1][i], b[1][i]) - max(a[0][i], b[0][i])
        if d <= 0:
            return 0.0
        v *= d
    return v


def _volume(b):
    return max(1e-12, (b[1][0] - b[0][0]) * (b[1][1] - b[0][1]) * (b[1][2] - b[0][2]))


def connectivity(comps, roots=None):
    """(connected ids, floating ids). Roots: components resting on the ground plane."""
    boxes = {c.id: semantic.bbox(c) for c in comps}
    if roots is None:
        roots = [c.id for c in comps if boxes[c.id][0][2] <= GROUND_Z + TOUCH]
    seen, todo = set(roots), list(roots)
    while todo:
        cur = todo.pop()
        for c in comps:
            if c.id not in seen and _overlap(boxes[cur], boxes[c.id], TOUCH):
                seen.add(c.id)
                todo.append(c.id)
    return sorted(seen), sorted(c.id for c in comps if c.id not in seen)


def intersections(comps, threshold=0.02):
    """Pairs of massive components whose boxes overlap by more than `threshold` of the
    smaller one (designed contacts touch; they do not overlap)."""
    solid = [c for c in comps if c.type in MASSIVE]
    boxes = {c.id: semantic.bbox(c) for c in solid}
    bad = []
    for i, a in enumerate(solid):
        for b in solid[i + 1:]:
            if frozenset((a.type, b.type)) in ALLOWED_OVERLAP:
                continue
            v = _overlap_volume(boxes[a.id], boxes[b.id])
            if v > threshold * min(_volume(boxes[a.id]), _volume(boxes[b.id])):
                bad.append((a.id, b.id, round(v, 4)))
    return bad


def check_asset(spec_data, comps, params):
    """[(check, ok, detail)] for one planned asset."""
    family, variant = spec_data["family"], spec_data["variant"]
    results = []
    errs = semantic.validate_components(comps)
    results.append(("components_valid", not errs, "; ".join(errs[:4]) or f"{len(comps)} components, ids unique, types known"))
    counts = {}
    for c in comps:
        counts[c.type] = counts.get(c.type, 0) + 1
    expected = expected_counts(family, variant, params)
    diff = {k: (counts.get(k, 0), v) for k, v in expected.items() if counts.get(k, 0) != v}
    extra = sorted(set(counts) - set(expected))
    results.append(("expected_component_counts", not diff and not extra,
                    f"mismatch {diff}, unexpected types {extra}" if diff or extra else
                    ", ".join(f"{k} {v}" for k, v in sorted(expected.items()))))
    lo, hi = semantic.union_bbox(comps)
    if family == "bridge":
        length = hi[0] - lo[0]
        deck_tops = [semantic.bbox(c)[1][2] for c in comps if c.type in ("DECK", "PLANK")]
        ok_len = abs(length - params["total_length_m"]) <= 0.25
        ok_deck = bool(deck_tops) and all(abs(t - params["deck_level_m"]) < 1e-3 for t in deck_tops)
        results.append(("dimensions", ok_len and ok_deck,
                        f"overall length {length:.3f} m (spec {params['total_length_m']}), deck top "
                        f"{sorted({round(t, 3) for t in deck_tops})} (spec {params['deck_level_m']})"))
        results.append(("rests_on_ground", abs(lo[2] - GROUND_Z) < 1e-3, f"lowest point z={lo[2]:.3f} (ground {GROUND_Z})"))
        results.append(("proportions",) + _proportions(variant, params))
    _, floating = connectivity(comps)
    results.append(("no_floating_components", not floating, f"floating: {floating[:6]}" if floating else
                    "every component connects to the ground through touching parts"))
    bad = intersections(comps)
    results.append(("no_major_intersections", not bad, f"{bad[:4]}" if bad else
                    "no overlapping masonry/timber/deck masses (designed joints touch)"))
    return results


def _proportions(variant, p):
    if variant == "stone_arch":
        lay = bridge.stone_arch_layout(p)
        rise = lay["radius"] / lay["span"]
        return (abs(rise - 0.5) < 1e-6 and lay["cover"] >= 0.15,
                f"semicircular rise/span {rise:.2f}; {lay['span']:.2f} m arches; {lay['cover']:.2f} m fill over the crown")
    if variant == "timber_beam":
        span = (p["total_length_m"] - 0.7) / p["span_count"]
        ratio = span / p["stringer_depth_m"]
        return (ratio <= 20, f"bent spacing {span:.2f} m, span/depth {ratio:.1f} (illustrative limit 20)")
    if variant == "steel_truss":
        lay = bridge.steel_truss_layout(p)
        length = min(b - a for a, b in lay["spans"])
        panel = length / p["panels_per_span"]
        ang = math.degrees(math.atan2(p["truss_height_m"], panel))
        return (35 <= ang <= 70 and 5 <= length / p["truss_height_m"] <= 12,
                f"span {length:.2f} m, depth {p['truss_height_m']} m (span/depth {length / p['truss_height_m']:.1f}), "
                f"diagonals at {ang:.0f} deg")
    return (True, "n/a")
