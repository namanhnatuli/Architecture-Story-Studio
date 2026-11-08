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
        if variant == "bay":   # section with a dry hull footprint: 3 water bodies, 2 cut plates, the waterline
            cut = bool(p["section"]) and p["hole_length_m"] > 0
            return {"GROUND": 2, "WATER": 6} if cut else {"GROUND": 1 + int(bool(p["shore"])), "WATER": 1}
        return {"GROUND": 1} if variant == "level_ground" else {"GROUND": 2, "WATER": 1}
    if family == "floating" and variant == "platform":
        nx = int(round(p["length_m"] / p["bulkhead_spacing_m"])) - 1
        ny = int(round(p["width_m"] / p["bulkhead_spacing_m"])) - 1
        ext, n, sec = p["extension_m"] > 0, p["storeys"], bool(p["section"])
        walls = 3 if sec else 4
        blocks = 2 if sec else 4                      # a section keeps the two blocks behind the cut
        ny_kept = sum(1 for j in range(1, ny + 1) if -p["width_m"] / 2 + j * p["bulkhead_spacing_m"] > 0.5) if sec else ny
        out = {"HULL": 1 + walls + (walls if ext else 0), "BULKHEAD": nx + ny_kept + (nx if ext else 0), "DECK": 1,
               "BUILDING": blocks * n, "ROOF": blocks * max(n - 1, 0)}
        if sec:
            out.update(SECTION_CUT=4 + nx + ((2 + nx) if ext else 0), DISPLACED_VOLUME=1, WATER=1, MARKER=1)
        else:
            if p["test_load"]:
                out["LOAD"] = 1
            if p["neighbours"]:   # four three-storey copies: hull, deck, buildings, roofs each
                for t in ("HULL", "DECK", "BUILDING", "ROOF"):
                    out[t] += 4
        return {k: v for k, v in out.items() if v}
    if family == "floating" and variant == "clay_boat":
        nx = int(round(p["length_m"] / p["bulkhead_spacing_m"])) - 1
        ny = int(round(p["width_m"] / p["bulkhead_spacing_m"])) - 1
        ny_kept = sum(1 for j in range(1, ny + 1) if -p["width_m"] / 2 + j * p["bulkhead_spacing_m"] > 0.5)
        return {"HULL": 1 + 1 + 3, "BULKHEAD": nx + ny_kept, "DECK": 1, "SECTION_CUT": 1 + 4 + nx, "WATER": 1}
    if family == "floating" and variant == "pair":
        n_built = sum(1 for k in ("storeys_a", "storeys_b") if p[k] > 0)
        return {k: v for k, v in {"HULL": 2, "DECK": 2, "BUILDING": n_built, "ROOF": n_built, "WALKWAY": 1, "CONNECTOR": 2}.items() if v}
    if family == "floating" and variant == "neighbourhood":   # 5 platforms, 4 joints (2 along X with fenders)
        out = {"HULL": 5, "DECK": 5, "BUILDING": 5, "ROOF": 5, "WALKWAY": 4, "UTILITY_LINE": 4, "CONNECTOR": 4 * 2 + 2 * 2}
        if p["moorings"] in ("piles", "both"):
            out.update(MOORING_PILE=10, CONNECTOR=out["CONNECTOR"] + 10)
        if p["moorings"] in ("lines", "both"):
            out.update(MOORING_LINE=10, ANCHOR=10)
        return out
    if family == "floating" and variant == "semi_sub":
        box = 1 if p["compare_box"] else 0
        return {k: v for k, v in {"HULL": 2 + box, "COLUMN": 6, "DECK": 1 + box, "BUILDING": box, "ROOF": box}.items() if v}
    if family == "floating" and variant == "district":
        cols, rows, lagoon = 11, 9, {(c, r) for c in (4, 5, 6) for r in (4, 5)}
        cells = {(c, r) for c in range(cols) for r in range(rows)} - lagoon
        walks = sum(((c + 1, r) in cells) + ((c, r + 1) in cells) for c, r in cells)
        piles = 2 * sum(1 for c, r in cells if r < p["pile_rows"])
        deep = [(c, r) for c, r in cells if r >= p["pile_rows"] and (r == rows - 1 or c in (0, cols - 1))]
        lines = sum((r == rows - 1) + (c in (0, cols - 1)) for c, r in deep)
        pitch = p["length_m"] + p["gap_m"]
        nseg = int((cols * pitch + 2 * pitch) // 64.0)
        bridges = 0 if p["offshore"] else p["bridges"]
        out = {"HULL": 93, "DECK": 93, "BUILDING": 93, "ROOF": 93, "WALKWAY": walks + 2, "MOORING_PILE": piles,
               "MOORING_LINE": lines, "ANCHOR": lines, "BREAKWATER": nseg, "LINK_SPAN": bridges,
               "CONNECTOR": bridges, "UTILITY_LINE": 3 * bridges + (9 if bridges else 0) + (3 if p["offshore"] and p["shore_link_m"] > 0 else 0),
               "ACCESS_ROUTE": bridges}
        return {k: v for k, v in out.items() if v}
    if variant == "gothic_section":
        n, sides = p["bay_count"], 2
        return {"FLOOR": 1, "NAVE_PIER": sides * (n + 1), "WALL": 4 * sides * n, "CLERESTORY_WINDOW": sides * n, "AISLE_WINDOW": sides * n,
                "VAULT_WEB": n * (1 if p.get("web_courses", 1) <= 1 else 4 * p["web_courses"]), "RIB": 2 * n + n + 1, "AISLE_VAULT": sides * n, "ROOF": 1, "AISLE_ROOF": sides,
                "PIER_BUTTRESS": sides * (n + 1), "PINNACLE": sides * (n + 1), "FLYING_BUTTRESS": sides * (n + 1)}
    if variant == "romanesque_section":
        n, sides = p["bay_count"], 2
        return {"FLOOR": 1, "THICK_WALL": sides * n, "SMALL_WINDOW": sides * n, "BARREL_VAULT": n, "WALL": sides * n,
                "SHALLOW_BUTTRESS": sides * (n + 1), "ROOF": 1}
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
    if variant == "suspension":
        return {"PIER": 2, "TOWER": 2, "ANCHORAGE": 2, "MAIN_CABLE": 2, "HANGER": 2, "FLOOR_BEAM": 1,
                "STIFFENING_TRUSS": 2, "DECK": 1}
    if variant == "cable_stayed":
        n = p["stays_per_side"]
        return {"PIER": 2, "PYLON": 2, "DECK": 4 * n + 3, "STAY_CABLE": 4 * n}
    if variant == "cantilever":
        lay = bridge.cantilever_layout(p)
        braced = sum(1 for h in (lay["h_pier"],) if h >= bridge.THROUGH_CLEARANCE_M + 0.5) * 4   # arms reach the pier depth
        braced += 1 if lay["h_tip"] >= bridge.THROUGH_CLEARANCE_M + 0.5 else 0
        return {"ABUTMENT": 2, "PIER": 2, "ANCHOR_ARM": 4, "CANTILEVER_ARM": 4, "SUSPENDED_SPAN": 2, "FLOOR_BEAM": 5,
                "DECK": 5, "BEARING": 1, **({"BRACING": braced} if braced else {})}
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
        # a suspension bridge's anchorages and cable ends lie on the banks, beyond the gap
        lo_x, hi_x = semantic.union_bbox([c for c in comps if c.type not in ("ANCHORAGE", "MAIN_CABLE")])
        length = hi_x[0] - lo_x[0]
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
    if variant == "suspension":
        lay = bridge.suspension_layout(p)
        return (0.08 <= p["sag_ratio"] <= 0.14 and lay["clearance"] >= 0.8,
                f"main span {p['main_span_m']} m, sag {lay['sag']:.2f} m (sag/span {p['sag_ratio']}), cable "
                f"{lay['clearance']:.2f} m above the deck at mid-span, towers {p['tower_height_m']} m above the deck")
    if variant == "cable_stayed":
        lay = bridge.cable_stayed_layout(p)
        return (lay["flattest_deg"] >= 22.0,
                f"main span {p['main_span_m']} m, pylons {p['pylon_height_m']} m above the deck, flattest stay "
                f"{lay['flattest_deg']:.1f} deg (FHWA: not less than about 22)")
    if variant == "cantilever":
        lay = bridge.cantilever_layout(p)
        return (lay["h_pier"] > max(lay["h_end"], lay["h_tip"]) and lay["suspended_m"] >= 4.0,
                f"anchor arms {p['anchor_arm_m']} m, cantilever arms {p['cantilever_arm_m']} m, suspended span "
                f"{lay['suspended_m']:.1f} m; depth {lay['h_end']} -> {lay['h_pier']} (piers) -> {lay['h_tip']} m")
    return (True, "n/a")
