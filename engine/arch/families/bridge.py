"""Bridge family generators (pure Python): timber beam, stone arch, steel truss.

Illustrative archetypes for explanation, not reconstructions of real bridges and not
engineering designs. All three span the same site gap (`total_length_m`, bank face to
bank face) with the deck top at `deck_level_m`, so they can be compared like for like.
Local component ids are stable; the variant id is prefixed when planned (assets.py).
"""
import math

from engine.arch import library as L
from engine.arch import primitives as P
from engine.arch.families.site import GROUND_Z
from engine.arch.semantic import Component

UP, DOWN = (0.0, 0.0, 1.0), (0.0, 0.0, -1.0)
# Trusses lower than this are "pony" trusses: no top lateral bracing over the roadway.
THROUGH_CLEARANCE_M = 4.5


def _y_sides(half):
    return (("north", half), ("south", -half))   # south = -Y = facing the default cameras


# ---------------------------------------------------------------- timber beam (trestle)
def timber_beam(p):
    """Timber stringers spanning between trestle bents, transverse deck planks, railings.

    Load path shown: planks -> stringers -> cap beams -> posts -> riverbed."""
    gap, deck, width = p["total_length_m"], p["deck_level_m"], p["deck_width_m"]
    spans, lines = p["span_count"], p["stringer_count"]
    plank_t, s_w, s_d = 0.09, p["stringer_width_m"], p["stringer_depth_m"]
    cap_d, post = 0.34, p["post_size_m"]
    half = width / 2.0
    edge = gap / 2.0 - 0.35                               # end bents stand just in front of the bank faces
    bents = L.spaced(-edge, edge, spans + 1)
    s_top = deck - plank_t                                # stringer top = plank underside
    cap_top = s_top - s_d - 0.002
    post_top = cap_top - cap_d
    comps = []
    ys = L.spaced(-half + 0.55, half - 0.55, 3)
    frame = P.merge(*[L.post(post_top - GROUND_Z, post, (0.0, y, GROUND_Z)) for y in ys],
                    L.x_brace_y(ys[0], ys[-1], 0.0, GROUND_Z + 0.9, post_top - 0.4, 0.14))
    cap = L.beam_y(-half - 0.25, half + 0.25, 0.0, cap_top, 0.34, cap_d)
    for i, x in enumerate(bents):   # identical bents: one shared mesh each for frame and cap
        comps.append(Component(f"bent{i + 1}", "SUPPORT", "timber_dark", frame, group="bents",
                               location=(x, 0.0, 0.0), layer=0, animation=("HIGHLIGHT", "STATIC"), bevel=0.012))
        comps.append(Component(f"bent{i + 1}_cap", "CAP_BEAM", "timber", cap, group="caps",
                               location=(x, 0.0, 0.0), layer=1, hint=UP, animation=("EXPLODE", "HIGHLIGHT"),
                               bevel=0.01))
    s_ys = L.spaced(-half + 0.45, half - 0.45, lines)
    ends = [-gap / 2.0] + bents[1:-1] + [gap / 2.0]
    for i in range(spans):
        x0, x1 = ends[i] + (0.006 if i else 0.0), ends[i + 1] - (0.006 if i < spans - 1 else 0.0)
        cx = (x0 + x1) / 2.0
        beams = P.merge(*[L.beam_x(x0 - cx, x1 - cx, y, s_top, s_w, s_d) for y in s_ys])
        comps.append(Component(f"span{i + 1}_stringers", "STRINGER", "timber", beams, group="stringers",
                               location=(cx, 0.0, 0.0), layer=2, hint=UP, animation=("EXPLODE", "HIGHLIGHT"),
                               bevel=0.012, meta={"span_m": round(x1 - x0, 3)}))
        planks, count = L.repeat_along_x(lambda c, w: P.box((w, width + 0.3, plank_t), (c, 0.0, deck - plank_t / 2.0)),
                                         x0 - cx, x1 - cx, p["plank_pitch_m"])
        comps.append(Component(f"span{i + 1}_planks", "PLANK", "timber_light", planks, group="deck",
                               location=(cx, 0.0, 0.0), layer=3, hint=UP, animation=("EXPLODE", "HIGHLIGHT"),
                               bevel=0.008, meta={"planks": count}))
    for side, y in _y_sides(half + 0.05):
        posts_x = L.spaced(-gap / 2.0 + 0.3, gap / 2.0 - 0.3, int(gap // 2.4) + 1)
        rail = P.merge(*[L.post(1.05, 0.14, (x, y, deck)) for x in posts_x],
                       L.beam_x(-gap / 2.0 + 0.2, gap / 2.0 - 0.2, y, deck + 1.1, 0.12, 0.1),
                       L.beam_x(-gap / 2.0 + 0.2, gap / 2.0 - 0.2, y, deck + 0.6, 0.08, 0.08))
        comps.append(Component(f"railing_{side}", "RAILING", "timber_dark", rail, group="railings",
                               layer=4, hint=(0.0, 1.0 if y > 0 else -1.0, 0.35), animation=("EXPLODE", "HIGHLIGHT"),
                               bevel=0.01))
    return comps


# ---------------------------------------------------------------- stone arch
def stone_arch_layout(p):
    """Arch centres, spans and levels (shared by the generator and validation)."""
    gap, n = p["total_length_m"], p["arch_count"]
    a, pier, ring = p["abutment_length_m"], p["pier_width_m"], p["ring_thickness_m"]
    x0 = -gap / 2.0 + a
    span = (gap - 2 * a - (n - 1) * pier) / n
    radius = span / 2.0
    spring = p["springing_level_m"]
    centres = [x0 + radius + i * (span + pier) for i in range(n)]
    crown_extrados = spring + radius + ring
    deck_bottom = p["deck_level_m"] - p["deck_thickness_m"]
    return {"x0": x0, "x1": -x0, "span": span, "radius": radius, "spring": spring, "centres": centres,
            "crown_extrados": crown_extrados, "deck_bottom": deck_bottom,
            "cover": deck_bottom - crown_extrados}


def stone_arch(p):
    """Semicircular masonry arches: voussoir rings with keystones on piers with cutwaters,
    spandrel fill, road deck, parapets with coping.

    Each voussoir is its own component (radial explode shows how a ring is assembled);
    voussoirs share one mesh, placed by rotation about the arch centre."""
    lay = stone_arch_layout(p)
    deck, width, ring = p["deck_level_m"], p["deck_width_m"], p["ring_thickness_m"]
    par_t, par_h = p["parapet_thickness_m"], p["parapet_height_m"]
    depth = width + 2 * par_t                       # barrel depth = full bridge width
    r, spring, count = lay["radius"], lay["spring"], p["voussoirs_per_arch"]
    gap, a = p["total_length_m"], p["abutment_length_m"]
    comps = []
    for side, sign in (("left", -1), ("right", 1)):
        xa, xb = sign * gap / 2.0, sign * (gap / 2.0 - a)
        comps.append(Component(f"abutment_{side}", "ABUTMENT", "stone_dark",
                               P.box((a, depth + 0.4, spring - GROUND_Z),
                                     ((xa + xb) / 2.0, 0.0, (spring + GROUND_Z) / 2.0)),
                               group="foundations", layer=0, animation=("HIGHLIGHT", "STATIC"), bevel=0.03))
    pier_w = p["pier_width_m"]
    for i in range(p["arch_count"] - 1):
        x = (lay["centres"][i] + lay["centres"][i + 1]) / 2.0
        body = P.box((pier_w, depth, spring - GROUND_Z), (0.0, 0.0, (spring + GROUND_Z) / 2.0))
        noses = [P.translate(L.prism_xy(L.cutwater_outline(pier_w / 2.0, pier_w * 0.55), GROUND_Z, spring - 0.25),
                             (0.0, -depth / 2.0, 0.0)),
                 P.translate(L.prism_xy([(x_, -y_) for x_, y_ in reversed(L.cutwater_outline(pier_w / 2.0, pier_w * 0.55))],
                                        GROUND_Z, spring - 0.25), (0.0, depth / 2.0, 0.0))]
        comps.append(Component(f"pier{i + 1}", "PIER", "stone_dark", P.merge(body, *noses), group="foundations",
                               location=(x, 0.0, 0.0), layer=0, animation=("HIGHLIGHT", "STATIC"), bevel=0.03))
    angles = L.arch_angles(count)
    half = math.pi / count / 2.0
    vmesh = L.voussoir_mesh(r, ring, depth, half)
    kmesh = L.keystone_mesh(r, ring, depth, half)
    for ai, cx in enumerate(lay["centres"]):
        for vi, (a0, a1) in enumerate(angles):
            theta = (a0 + a1) / 2.0
            key = vi == count // 2
            comps.append(Component(
                f"arch{ai + 1}_keystone" if key else f"arch{ai + 1}_voussoir{vi + 1:02d}",
                "KEYSTONE" if key else "VOUSSOIR", "stone_light" if key else "stone", kmesh if key else vmesh,
                group=f"arch_{ai + 1}", location=(cx, 0.0, spring), rotation=L.rotation_for_angle(theta),
                layer=2 if key else 1, hint=(math.cos(theta), 0.0, math.sin(theta)),
                animation=("EXPLODE", "HIGHLIGHT"), bevel=0.02, meta={"theta_deg": round(math.degrees(theta), 3)}))
    ext = r + ring + L.JOINT_GAP
    outline = L.spandrel_outline(-gap / 2.0, gap / 2.0, spring, lay["deck_bottom"],
                                 [(cx, spring, ext) for cx in lay["centres"]])
    comps.append(Component("spandrel", "SPANDREL", "stone", P.prism_xz(outline, depth), group="spandrel",
                           layer=3, hint=UP, animation=("EXPLODE", "HIGHLIGHT"), bevel=0.02))
    comps.append(Component("deck", "DECK", "road_gravel",
                           P.box((gap, width, p["deck_thickness_m"]), (0.0, 0.0, deck - p["deck_thickness_m"] / 2.0)),
                           group="deck", layer=4, hint=UP, animation=("EXPLODE", "HIGHLIGHT"), bevel=0.01))
    for side, y in _y_sides(width / 2.0 + par_t / 2.0):
        comps.append(Component(f"parapet_{side}", "PARAPET", "stone",
                               P.box((gap, par_t, par_h + p["deck_thickness_m"]),
                                     (0.0, y, lay["deck_bottom"] + (par_h + p["deck_thickness_m"]) / 2.0)),
                               group="parapets", layer=5, hint=(0.0, 1.0 if y > 0 else -1.0, 0.6),
                               animation=("EXPLODE", "HIGHLIGHT"), bevel=0.02))
        comps.append(Component(f"coping_{side}", "COPING", "stone_light",
                               P.box((gap + 0.1, par_t + 0.1, 0.12), (0.0, y, deck + par_h + 0.06)),
                               group="parapets", layer=6, hint=(0.0, 1.0 if y > 0 else -1.0, 1.0),
                               animation=("EXPLODE", "HIGHLIGHT"), bevel=0.02))
    return comps


# ---------------------------------------------------------------- steel truss
def steel_truss_layout(p):
    gap, spans = p["total_length_m"], p["span_count"]
    seat, pier = 0.7, p["pier_width_m"]
    bearings = []
    if spans == 1:
        bearings = [(-gap / 2.0 + seat / 2.0, gap / 2.0 - seat / 2.0)]
    else:
        inner = L.spaced(-gap / 2.0 + seat / 2.0, gap / 2.0 - seat / 2.0, spans + 1)
        for i in range(spans):
            a = inner[i] + (pier / 2.0 - 0.3 if i else 0.0)
            b = inner[i + 1] - (pier / 2.0 - 0.3 if i < spans - 1 else 0.0)
            bearings.append((a, b))
    deck = p["deck_level_m"]
    floor_top = deck - 0.18
    chord_c = floor_top - 0.35 + 0.15           # floor beams (0.35 deep) frame into the bottom chord
    return {"seat": seat, "spans": bearings, "inner": L.spaced(-gap / 2.0 + seat / 2.0, gap / 2.0 - seat / 2.0, spans + 1),
            "floor_top": floor_top, "chord_z": chord_c, "bearing_top": chord_c - 0.15}


def steel_truss(p):
    """Parallel-chord trusses (Pratt or Warren web) on bearings, floor beams and a deck
    slab; top lateral struts only when the truss is tall enough to be a through truss
    (THROUGH_CLEARANCE_M), otherwise a pony truss. Repeated identical spans share meshes."""
    lay = steel_truss_layout(p)
    deck, width, h, panels = p["deck_level_m"], p["deck_width_m"], p["truss_height_m"], p["panels_per_span"]
    gap, pattern = p["total_length_m"], p["truss_pattern"]
    ty = width / 2.0 + 0.3                         # truss planes
    chord, web = p["chord_size_m"], p["web_size_m"]
    comps = []
    seat_top = lay["bearing_top"] - 0.18
    for side, sign in (("left", -1), ("right", 1)):
        xa, xb = sign * gap / 2.0, sign * (gap / 2.0 - lay["seat"])
        comps.append(Component(f"seat_{side}", "ABUTMENT", "concrete",
                               P.box((lay["seat"], 2 * ty + 1.0, seat_top - GROUND_Z),
                                     ((xa + xb) / 2.0, 0.0, (seat_top + GROUND_Z) / 2.0)),
                               group="foundations", layer=0, animation=("HIGHLIGHT", "STATIC"), bevel=0.03))
    for i in range(1, len(lay["inner"]) - 1):
        x = lay["inner"][i]
        comps.append(Component(f"pier{i}", "PIER", "concrete",
                               P.box((p["pier_width_m"], 2 * ty + 1.0, seat_top - GROUND_Z),
                                     (0.0, 0.0, (seat_top + GROUND_Z) / 2.0)),
                               group="foundations", location=(x, 0.0, 0.0), layer=0,
                               animation=("HIGHLIGHT", "STATIC"), bevel=0.03))
    for si, (a, b) in enumerate(lay["spans"]):
        length, cx = b - a, (a + b) / 2.0
        bottom, top = L.truss_nodes(length, h, panels, lay["chord_z"])
        n = f"span{si + 1}"
        frame_members = [("TRUSS_CHORD", bottom[0], bottom[-1]), ("TRUSS_CHORD", top[0], top[-1])]
        posts = [("END_POST", bottom[0], top[0]), ("END_POST", bottom[-1], top[-1])]
        for side, y in _y_sides(ty):
            comps.append(Component(f"{n}_chords_{side}", "TRUSS_CHORD", "steel",
                                   L.truss_members_mesh(frame_members, 0.0, chord, chord), group=f"truss_{side}",
                                   location=(cx, y, 0.0), layer=2, hint=(0.0, 1.0 if y > 0 else -1.0, 0.0),
                                   animation=("EXPLODE", "HIGHLIGHT"), bevel=0.01, meta={"frame": True}))
            comps.append(Component(f"{n}_endposts_{side}", "END_POST", "steel",
                                   L.truss_members_mesh(posts, 0.0, chord, chord), group=f"truss_{side}",
                                   location=(cx, y, 0.0), layer=2, hint=(0.0, 1.0 if y > 0 else -1.0, 0.0),
                                   animation=("EXPLODE", "HIGHLIGHT"), bevel=0.01, meta={"frame": True}))
            members = L.truss_web(pattern, bottom, top)
            for kind, label in (("TRUSS_VERTICAL", "verticals"), ("TRUSS_DIAGONAL", "diagonals")):
                chosen = [m for m in members if m[0] == kind]
                if not chosen:
                    continue
                comps.append(Component(f"{n}_{label}_{side}", kind, "steel",
                                       L.truss_members_mesh(chosen, 0.0, web, web), group=f"truss_{side}",
                                       location=(cx, y, 0.0), layer=3, hint=(0.0, 1.0 if y > 0 else -1.0, 0.25),
                                       animation=("EXPLODE", "HIGHLIGHT", "REPLACE"), bevel=0.008,
                                       meta={"pattern": pattern, "members": len(chosen)}))
            off = chord / 2.0 + 0.016                   # plate touches the chord face
            plates = P.merge(*[L.gusset(x, z, off if y > 0 else -off, 0.5, 0.03) for x, z in bottom + top])
            comps.append(Component(f"{n}_joints_{side}", "JOINT", "steel_dark", plates, group=f"truss_{side}",
                                   location=(cx, y, 0.0), layer=4, hint=(0.0, 1.0 if y > 0 else -1.0, 0.0),
                                   animation=("EXPLODE", "HIGHLIGHT"), bevel=0.004, meta={"frame": True}))
        beams = P.merge(*[L.beam_y(-ty, ty, x, lay["floor_top"], 0.22, 0.35) for x, _ in bottom])
        comps.append(Component(f"{n}_floor_beams", "FLOOR_BEAM", "steel_dark", beams, group="floor",
                               location=(cx, 0.0, 0.0), layer=1, hint=DOWN, animation=("EXPLODE", "HIGHLIGHT"),
                               bevel=0.008, meta={"frame": True}))
        comps.append(Component(f"{n}_deck", "DECK", "concrete_deck",
                               P.box((length - 0.04, width, deck - lay["floor_top"]),
                                     (0.0, 0.0, (deck + lay["floor_top"]) / 2.0)),
                               group="deck", location=(cx, 0.0, 0.0), layer=1, hint=UP,
                               animation=("EXPLODE", "HIGHLIGHT"), bevel=0.01, meta={"frame": True}))
        if h >= THROUGH_CLEARANCE_M:  # through truss: top lateral struts clear the roadway
            struts = P.merge(*[P.member((x, -ty, z), (x, ty, z), 0.16, 0.16, side=(1, 0, 0)) for x, z in top[1:-1]])
            comps.append(Component(f"{n}_top_bracing", "BRACING", "steel_dark", struts, group="bracing",
                                   location=(cx, 0.0, 0.0), layer=5, hint=UP, animation=("EXPLODE", "HIGHLIGHT"),
                                   bevel=0.006, meta={"frame": True}))
        pads = P.merge(*[P.box((0.45, 0.5, 0.18), (x, y, lay["bearing_top"] - 0.09))
                         for x in (bottom[0][0], bottom[-1][0]) for y in (-ty, ty)])
        comps.append(Component(f"{n}_bearings", "BEARING", "steel_dark", pads, group="foundations",
                               location=(cx, 0.0, 0.0), layer=0, animation=("HIGHLIGHT", "STATIC"), bevel=0.01,
                               meta={"frame": True}))
    return comps


# ---------------------------------------------------------------- exploded-view presets
def _unit(v):
    n = math.sqrt(sum(x * x for x in v))
    return tuple(x / n for x in v)


def _side(c):
    return 1.0 if (c.hint and c.hint[1] > 0) else -1.0


def explode_offsets(variant, comps):
    """Recommended exploded-view offsets {component id: (dx, dy, dz)} for previews and
    storyboards. Chosen so that, from the default cameras, nothing moves in front of the
    parts being explained and nothing collides (checked by the Blender QA)."""
    out = {}
    for c in comps:
        if "EXPLODE" not in c.animation:
            continue
        t = c.type
        if variant == "timber_beam":
            d = {"RAILING": 1.6, "PLANK": 1.9, "STRINGER": 1.1, "CAP_BEAM": 0.6}.get(t)
            vec = _unit(c.hint) if t == "RAILING" else UP
        elif variant == "stone_arch":
            if t in ("VOUSSOIR", "KEYSTONE"):   # ring opens slightly from its centre and lifts off the piers
                radial, up = (0.35, 0.5) if t == "VOUSSOIR" else (0.6, 0.75)
                out[c.id] = (c.hint[0] * radial, 0.0, c.hint[2] * radial + up)
                continue
            # masses move up and BACK (+Y): the front of the arch rings stays clear
            rule = {"SPANDREL": ((0.0, 1.0, 0.0), 6.5), "DECK": ((0.0, 1.0, 0.45), 6.6),
                    "PARAPET": (((0.0, 1.0, 0.6), 3.2) if _side(c) > 0 else ((0.0, 0.7, 0.7), 4.0)),
                    "COPING": (((0.0, 1.0, 1.0), 3.4) if _side(c) > 0 else ((0.0, 0.6, 0.8), 4.4))}.get(t)
            if rule is None:
                continue
            vec, d = _unit(rule[0]), rule[1]
        elif variant == "steel_truss":
            s = _side(c)
            rule = {"JOINT": ((0.0, s, 0.0), 2.4), "TRUSS_VERTICAL": ((0.0, s, 0.0), 1.6),
                    "TRUSS_DIAGONAL": ((0.0, s, 0.0), 1.6), "TRUSS_CHORD": ((0.0, s, 0.0), 0.8),
                    "END_POST": ((0.0, s, 0.0), 0.8), "DECK": (UP, 1.4), "FLOOR_BEAM": (DOWN, 0.6),
                    "BRACING": (UP, 1.2)}.get(t)
            if rule is None:
                continue
            vec, d = _unit(rule[0]), rule[1]
        else:
            continue
        if d:
            out[c.id] = tuple(x * d for x in vec)
    return out
