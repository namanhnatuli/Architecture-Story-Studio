"""Bridge family generators (pure Python): timber beam, stone arch, steel truss, and (M8) the
long-span families: cantilever truss, suspension and cable-stayed.

Illustrative archetypes for explanation, not reconstructions of real bridges and not
engineering designs. Every variant spans its site gap (`total_length_m`, bank face to bank
face) with the deck top at `deck_level_m`, so bridges on one site compare like for like; a
suspension bridge's anchorages (and the cable ends) lie on the banks, beyond the gap.
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


# ---------------------------------------------------------------- long-span families (M8)
def _bars(points, size, side=(0.0, 1.0, 0.0)):
    """A polyline of square bars (cables, chords): one bar per segment, end to end."""
    return P.merge(*[P.member(a, b, size, size, side=side) for a, b in zip(points, points[1:])])


def _cross_strut(x, y, z, size):
    return P.member((x, -y, z), (x, y, z), size, size, side=(1.0, 0.0, 0.0))


def suspension_layout(p):
    """Towers, cable profile and hanger positions (shared by the generator and validation).

    The main cables are draped over the towers and anchored beyond the bank faces; the deck
    hangs from vertical hangers at the ends of floor beams (FHWA-IF-12-052 vol. 5, 2.6)."""
    gap, deck, width, main = p["total_length_m"], p["deck_level_m"], p["deck_width_m"], p["main_span_m"]
    side = (gap - main) / 2.0
    top = deck + p["tower_height_m"]
    saddle = top - 0.35
    sag = main * p["sag_ratio"]
    low = saddle - sag
    truss_y = width / 2.0 + 0.25                       # stiffening truss planes, just outside the slab
    cable_y = truss_y + 0.7                            # cables and tower legs outside the trusses
    anchor_x = gap / 2.0 + p["anchorage_offset_m"] - 1.4
    anchor_z = deck + 1.0

    def cable_z(x):
        ax = abs(x)
        if ax <= main / 2.0:
            return low + sag * (ax / (main / 2.0)) ** 2
        t_ = (ax - main / 2.0) / (anchor_x - main / 2.0)
        chord = saddle + (anchor_z - saddle) * t_
        return chord - 0.03 * (anchor_x - main / 2.0) * 4 * t_ * (1 - t_)

    pitch = p["hanger_spacing_m"]
    xs = [x for x in L.spaced(-gap / 2.0 + 0.8, gap / 2.0 - 0.8, int(round((gap - 1.6) / pitch)) + 1)
          if abs(abs(x) - main / 2.0) > 1.0]
    return {"side": side, "top": top, "saddle": saddle, "sag": sag, "low": low, "truss_y": truss_y,
            "cable_y": cable_y, "anchor_x": anchor_x, "anchor_z": anchor_z, "cable_z": cable_z, "hangers": xs,
            "clearance": low - deck}


def suspension(p):
    """Two towers, two main cables over saddles to anchorages on the banks, vertical hangers to
    floor-beam ends, a deck on floor beams and a stiffening truss along each edge."""
    lay = suspension_layout(p)
    gap, deck, width, main = p["total_length_m"], p["deck_level_m"], p["deck_width_m"], p["main_span_m"]
    d, leg, cable = p["stiffening_depth_m"], p["tower_size_m"], p["cable_size_m"]
    ty, cy = lay["truss_y"], lay["cable_y"]
    comps = []
    pier_top = 1.2
    for side, sign in (("left", -1), ("right", 1)):
        x = sign * main / 2.0
        comps.append(Component(f"pier_{side}", "PIER", "concrete",
                               P.box((leg + 1.6, 2 * cy + leg + 1.6, pier_top - GROUND_Z), (0.0, 0.0, (pier_top + GROUND_Z) / 2.0)),
                               group="foundations", location=(x, 0.0, 0.0), layer=0, animation=("HIGHLIGHT", "STATIC"),
                               bevel=0.04))
        legs = P.merge(*[P.box((leg, leg, lay["top"] - pier_top), (0.0, y, (lay["top"] + pier_top) / 2.0)) for y in (-cy, cy)])
        # portal struts: one low on the legs (the deck system drops past it in an exploded view), one at the top
        struts = P.merge(_cross_strut(0.0, cy, pier_top + 1.0, leg * 0.8), _cross_strut(0.0, cy, lay["top"] - 0.5, leg * 0.8))
        saddles = P.merge(*[P.box((leg * 1.3, leg * 1.1, 0.3), (0.0, y, lay["top"] + 0.15)) for y in (-cy, cy)])
        comps.append(Component(f"tower_{side}", "TOWER", "steel", P.merge(legs, struts, saddles), group="towers",
                               location=(x, 0.0, 0.0), layer=1, hint=UP, animation=("HIGHLIGHT", "STATIC"), bevel=0.02,
                               meta={"height_above_deck_m": p["tower_height_m"]}))
        ax = sign * (gap / 2.0 + p["anchorage_offset_m"])
        comps.append(Component(f"anchorage_{side}", "ANCHORAGE", "concrete",
                               P.box((2.8, 2 * cy + 1.6, 2.2), (0.0, 0.0, deck + 1.1)), group="anchorages",
                               location=(ax, 0.0, 0.0), layer=0, animation=("HIGHLIGHT", "STATIC"), bevel=0.05))
    xs = L.spaced(-lay["anchor_x"], lay["anchor_x"], 121)
    xs = sorted(set([round(x, 6) for x in xs] + [-main / 2.0, main / 2.0]))
    for side, y in _y_sides(cy):
        pts = [(x, y, lay["cable_z"](x)) for x in xs]
        comps.append(Component(f"main_cable_{side}", "MAIN_CABLE", "cable", _bars(pts, cable), group="cables",
                               layer=2, hint=UP, animation=("EXPLODE", "HIGHLIGHT"), bevel=0.0,
                               meta={"sag_m": round(lay["sag"], 3), "main_span_m": main}))
        hangers = P.merge(*[P.member((x, y, deck - 0.12), (x, y, lay["cable_z"](x) - cable / 2.0), 0.1, 0.1)
                            for x in lay["hangers"]])
        comps.append(Component(f"hangers_{side}", "HANGER", "cable", hangers, group="hangers", layer=3,
                               hint=(0.0, 1.0 if y > 0 else -1.0, 0.0), animation=("EXPLODE", "HIGHLIGHT"),
                               meta={"hangers": len(lay["hangers"])}))
    floor = P.merge(*[L.beam_y(-cy - 0.15, cy + 0.15, x, deck - 0.12, 0.2, 0.3) for x in lay["hangers"]])
    comps.append(Component("floor_beams", "FLOOR_BEAM", "steel_dark", floor, group="deck_system", layer=4, hint=DOWN,
                           animation=("EXPLODE", "HIGHLIGHT"), bevel=0.006))
    length = gap - 0.4                                 # chord ends stay clear of the bank faces
    panels = max(2, int(round(length / 2.4 / 2.0)) * 2)
    bottom, top = L.truss_nodes(length, d, panels, deck - d - 0.12)
    members = [("TRUSS_CHORD", bottom[0], bottom[-1]), ("TRUSS_CHORD", top[0], top[-1]),
               ("END_POST", bottom[0], top[0]), ("END_POST", bottom[-1], top[-1])] + L.truss_web("warren", bottom, top)
    for side, y in _y_sides(ty):
        comps.append(Component(f"stiffening_truss_{side}", "STIFFENING_TRUSS", "steel_dark",
                               L.truss_members_mesh(members, 0.0, 0.16, 0.16), group="deck_system", location=(0.0, y, 0.0),
                               layer=4, hint=DOWN, animation=("EXPLODE", "HIGHLIGHT"), bevel=0.004))
    comps.append(Component("deck", "DECK", "concrete_deck", P.box((gap, 2 * ty - 0.1, 0.12), (0.0, 0.0, deck - 0.06)),
                           group="deck_system", layer=5, hint=DOWN, animation=("EXPLODE", "HIGHLIGHT"), bevel=0.01))
    return comps


def cable_stayed_layout(p):
    """Pylons, deck segments and stay anchor points (shared by the generator and validation).

    Stays run in straight lines from the pylons to the edge girders (FHWA-IF-12-052 vol. 5, 2.5);
    the deck is divided into segments built outward from each pylon (4.4: balanced cantilever)."""
    gap, deck, width, main = p["total_length_m"], p["deck_level_m"], p["deck_width_m"], p["main_span_m"]
    n = p["stays_per_side"]
    side = (gap - main) / 2.0
    closure = 2.0
    main_seg = (main / 2.0 - closure / 2.0 - 1.0) / n   # 1.0 m: the deck block over the pylon (half)
    side_seg = (side - 1.0) / n
    top = deck + p["pylon_height_m"]
    girder_y = width / 2.0 + 0.1
    leg_y = girder_y + 0.25 + p["pylon_size_m"] / 2.0
    anchors_z = [top - 0.5 - 0.55 * k for k in range(n)]     # outermost stay anchored highest
    stays = []
    for sign in (-1, 1):
        px = sign * main / 2.0
        for k in range(1, n + 1):
            for direction, seg in (("main", main_seg), ("side", side_seg)):
                outward = -sign if direction == "main" else sign
                x_end = px + outward * (1.0 + k * seg - 0.35)
                z_top = anchors_z[n - k]
                angle = math.degrees(math.atan2(z_top - deck, abs(x_end - px)))
                stays.append({"pylon": sign, "dir": direction, "k": k, "x_deck": x_end, "z_pylon": z_top,
                              "angle_deg": angle})
    return {"side": side, "closure": closure, "main_seg": main_seg, "side_seg": side_seg, "top": top,
            "girder_y": girder_y, "leg_y": leg_y, "stays": stays,
            "flattest_deg": min(s["angle_deg"] for s in stays)}


def cable_stayed(p):
    """Two H-pylons (concrete) with a strut below the stay anchorages, straight stays in a vertical
    plane above each edge girder, a deck in segments (slab + edge girders) built outward from the
    pylons and closed at mid-span; no anchorages."""
    lay = cable_stayed_layout(p)
    gap, deck, width, main = p["total_length_m"], p["deck_level_m"], p["deck_width_m"], p["main_span_m"]
    n, g_d, leg, stay = p["stays_per_side"], p["girder_depth_m"], p["pylon_size_m"], p["stay_size_m"]
    gy, ly = lay["girder_y"], lay["leg_y"]
    comps = []
    pier_top = 1.2
    slab_t = 0.2

    def segment(name, x0, x1, layer, k):
        cx, length = (x0 + x1) / 2.0, x1 - x0 - 0.02
        slab = P.box((length, 2 * gy, slab_t), (0.0, 0.0, deck - slab_t / 2.0))
        girders = P.merge(*[P.box((length, 0.35, g_d), (0.0, y, deck - slab_t - g_d / 2.0)) for y in (-gy, gy)])
        comps.append(Component(name, "DECK", "concrete_deck", P.merge(slab, girders), group="deck", location=(cx, 0.0, 0.0),
                               layer=layer, hint=DOWN, animation=("EXPLODE", "HIGHLIGHT"), bevel=0.008,
                               meta={"segment": k, "length_m": round(length, 3)}))

    for side, sign in (("left", -1), ("right", 1)):
        px = sign * main / 2.0
        comps.append(Component(f"pier_{side}", "PIER", "concrete",
                               P.box((leg + 1.8, 2 * ly + leg + 1.6, pier_top - GROUND_Z), (0.0, 0.0, (pier_top + GROUND_Z) / 2.0)),
                               group="foundations", location=(px, 0.0, 0.0), layer=0, animation=("HIGHLIGHT", "STATIC"),
                               bevel=0.04))
        legs = P.merge(*[P.box((leg, leg, lay["top"] - pier_top), (0.0, y, (lay["top"] + pier_top) / 2.0)) for y in (-ly, ly)])
        struts = P.merge(_cross_strut(0.0, ly, deck - slab_t - g_d - leg * 0.45, leg * 0.9),   # carries the pylon block
                         _cross_strut(0.0, ly, lay["top"] - 0.55 * n - 0.6, leg * 0.75))
        comps.append(Component(f"pylon_{side}", "PYLON", "concrete", P.merge(legs, struts), group="pylons",
                               location=(px, 0.0, 0.0), layer=1, hint=UP, animation=("HIGHLIGHT", "STATIC"), bevel=0.03,
                               meta={"height_above_deck_m": p["pylon_height_m"]}))
        segment(f"deck_{side}_pylon", px - 1.0, px + 1.0, 2, 0)
        for k in range(1, n + 1):
            for direction, seg in (("main", lay["main_seg"]), ("side", lay["side_seg"])):
                outward = -sign if direction == "main" else sign
                a, b = px + outward * (1.0 + (k - 1) * seg), px + outward * (1.0 + k * seg)
                segment(f"deck_{side}_{direction}{k}", min(a, b), max(a, b), 2 + k, k)
                s = next(s for s in lay["stays"] if s["pylon"] == sign and s["dir"] == direction and s["k"] == k)
                face = outward * leg * 0.25          # fore and back stays anchor on opposite faces of the leg
                bars = P.merge(*[P.member((face, y_top, s["z_pylon"]), (s["x_deck"] - px, y_bot, deck - slab_t),
                                          stay, stay) for y_top, y_bot in ((-ly, -gy), (ly, gy))])
                comps.append(Component(f"stay_{side}_{direction}{k}", "STAY_CABLE", "cable", bars, group="stays",
                                       location=(px, 0.0, 0.0), layer=2 + k, hint=UP, animation=("EXPLODE", "HIGHLIGHT"),
                                       meta={"angle_deg": round(s["angle_deg"], 2), "segment": k}))
    half = lay["closure"] / 2.0
    segment("deck_closure", -half, half, 3 + n, n + 1)
    return comps


def cantilever_layout(p):
    """Main piers, arm tips and the top-chord profile of a through cantilever truss (validation too).

    Anchor arms rest on the abutments and main piers; cantilever arms project from the piers and
    carry a suspended span (NCHRP 25-25(15) 3.1, 3.7)."""
    gap, deck = p["total_length_m"], p["deck_level_m"]
    a, c = p["anchor_arm_m"], p["cantilever_arm_m"]
    xp = gap / 2.0 - a
    tip = xp - c
    zb = deck - 0.18 - 0.35 + 0.15            # bottom chord: floor beams frame into it (as steel_truss)
    return {"pier_x": xp, "tip_x": tip, "suspended_m": 2 * tip, "z_bottom": zb, "bearing_top": zb - p["chord_size_m"] / 2.0,
            "h_end": p["depth_end_m"], "h_pier": p["depth_over_piers_m"], "h_tip": p["depth_tip_m"]}


def _arm_nodes(x0, x1, h0, h1, panels, zb):
    xs = L.spaced(x0, x1, panels + 1)
    return [(x, zb) for x in xs], [(x, zb + h0 + (h1 - h0) * (x - x0) / (x1 - x0)) for x in xs]


def _arm_members(bottom, top, toward_end):
    """Chords, verticals and one diagonal per panel; toward_end: the nodes run toward the deep
    (pier) end, so each diagonal slopes down away from the pier either way."""
    out = [("TRUSS_CHORD", a, b) for a, b in zip(bottom, bottom[1:])] + [("TRUSS_CHORD", a, b) for a, b in zip(top, top[1:])]
    out += [("TRUSS_VERTICAL", b, t) for b, t in zip(bottom, top)]
    for i in range(len(bottom) - 1):
        out.append(("TRUSS_DIAGONAL", top[i + 1], bottom[i]) if toward_end else ("TRUSS_DIAGONAL", top[i], bottom[i + 1]))
    return out


def cantilever(p):
    """Balanced cantilever through truss: anchor arms (abutment to main pier), cantilever arms
    projecting from the piers, and a suspended span hung between the arm tips."""
    lay = cantilever_layout(p)
    gap, deck, width = p["total_length_m"], p["deck_level_m"], p["deck_width_m"]
    zb, xp, tip = lay["z_bottom"], lay["pier_x"], lay["tip_x"]
    ty = width / 2.0 + 0.35
    chord, web = p["chord_size_m"], p["web_size_m"]
    comps = []
    seat = 0.7
    seat_top = lay["bearing_top"] - 0.18
    for side, sign in (("left", -1), ("right", 1)):
        xa, xb = sign * gap / 2.0, sign * (gap / 2.0 - seat)
        comps.append(Component(f"seat_{side}", "ABUTMENT", "concrete",
                               P.box((seat, 2 * ty + 1.0, seat_top - GROUND_Z), ((xa + xb) / 2.0, 0.0, (seat_top + GROUND_Z) / 2.0)),
                               group="foundations", layer=0, animation=("HIGHLIGHT", "STATIC"), bevel=0.03))
        comps.append(Component(f"pier_{side}", "PIER", "concrete",
                               P.box((p["pier_width_m"], 2 * ty + 1.4, seat_top - GROUND_Z), (0.0, 0.0, (seat_top + GROUND_Z) / 2.0)),
                               group="foundations", location=(sign * xp, 0.0, 0.0), layer=0,
                               animation=("HIGHLIGHT", "STATIC"), bevel=0.04))
    end = gap / 2.0 - seat / 2.0
    gapj = 0.15                                   # joint between an arm tip and the suspended span
    parts = []
    for side, sign in (("left", -1), ("right", 1)):
        b, t = _arm_nodes(sign * end, sign * xp, lay["h_end"], lay["h_pier"], p["panels_anchor"], zb)
        parts.append((f"anchor_arm_{side}", "ANCHOR_ARM", 1, b, t, True))
        b, t = _arm_nodes(sign * xp, sign * (tip + gapj / 2.0), lay["h_pier"], lay["h_tip"], p["panels_cantilever"], zb)
        parts.append((f"cantilever_arm_{side}", "CANTILEVER_ARM", 2, b, t, False))
    b, t = L.truss_nodes(2 * tip - gapj, lay["h_tip"], p["panels_suspended"], zb)
    parts.append(("suspended_span", "SUSPENDED_SPAN", 3, b, t, None))
    for name, kind, layer, bottom, top, toward in parts:
        members = (_arm_members(bottom, top, toward) if toward is not None else
                   [("TRUSS_CHORD", bottom[0], bottom[-1]), ("TRUSS_CHORD", top[0], top[-1]),
                    ("END_POST", bottom[0], top[0]), ("END_POST", bottom[-1], top[-1])] + L.truss_web("pratt", bottom, top))
        x0, x1 = bottom[0][0], bottom[-1][0]
        for side, y in _y_sides(ty):
            comps.append(Component(f"{name}_{side}", kind, "steel", L.truss_members_mesh(members, y, chord, chord),
                                   group=f"truss_{side}", layer=layer, hint=UP, animation=("EXPLODE", "HIGHLIGHT"),
                                   bevel=0.008, meta={"from_x": round(min(x0, x1), 3), "to_x": round(max(x0, x1), 3)}))
        lo, hi = min(x0, x1), max(x0, x1)
        floor_top = deck - 0.18
        # the pier node's beam belongs to the anchor arm, the tip's to the suspended span it carries
        nodes = bottom[1:-1] if kind == "CANTILEVER_ARM" else bottom
        beams = P.merge(*[L.beam_y(-ty, ty, x, floor_top, 0.22, 0.35) for x, _ in nodes])
        comps.append(Component(f"{name}_floor", "FLOOR_BEAM", "steel_dark", beams, group="floor", layer=4, hint=DOWN,
                               animation=("EXPLODE", "HIGHLIGHT"), bevel=0.008))
        comps.append(Component(f"{name}_deck", "DECK", "concrete_deck",
                               P.box((hi - lo - 0.04, width, 0.18), ((lo + hi) / 2.0, 0.0, deck - 0.09)), group="deck",
                               layer=4, hint=UP, animation=("EXPLODE", "HIGHLIGHT"), bevel=0.01))
        high = [(x, z) for x, z in top if z - zb >= THROUGH_CLEARANCE_M + 0.5]
        if high:
            struts = P.merge(*[P.member((x, -ty, z), (x, ty, z), 0.16, 0.16, side=(1, 0, 0)) for x, z in high])
            comps.append(Component(f"{name}_bracing", "BRACING", "steel_dark", struts, group="bracing", layer=5, hint=UP,
                                   animation=("EXPLODE", "HIGHLIGHT"), bevel=0.006))
    pads = P.merge(*[P.box((0.45, 0.5, 0.18), (x, y, lay["bearing_top"] - 0.09))
                     for x in (-end, end, -xp, xp) for y in (-ty, ty)])
    comps.append(Component("bearings", "BEARING", "steel_dark", pads, group="foundations", layer=0,
                           animation=("HIGHLIGHT", "STATIC"), bevel=0.01))
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
        elif variant == "cantilever":   # the truss lifts apart in its hierarchy; the suspended span (set in last)
            # rises highest; deck and floor stay on the piers (a downward move would enter them); top bracing
            # travels with the truss part it braces (alone it read as loose sticks)
            lift = {"SUSPENDED_SPAN": 3.2, "CANTILEVER_ARM": 2.0, "ANCHOR_ARM": 1.0}
            if t == "BRACING":
                part = next((k for k in ("suspended_span", "cantilever_arm", "anchor_arm") if k in c.id), None)
                rule = (UP, lift[part.upper()]) if part else None
            else:
                rule = (UP, lift[t]) if t in lift else None
            if rule is None:
                continue
            vec, d = _unit(rule[0]), rule[1]
        elif variant == "suspension":   # what hangs from what: deck system down, cables up
            rule = {"DECK": (DOWN, 0.6), "STIFFENING_TRUSS": (DOWN, 1.8), "FLOOR_BEAM": (DOWN, 1.2),
                    "MAIN_CABLE": (UP, 1.4), "HANGER": (UP, 0.7)}.get(t)
            if rule is None:
                continue
            vec, d = _unit(rule[0]), rule[1]
        elif variant == "cable_stayed":   # stays lift off; the segments drop and return outward from the
            # deck block over each pylon, which stays on its strut (the balanced-cantilever order)
            if t == "DECK" and c.meta.get("segment") == 0:
                continue
            rule = {"STAY_CABLE": (UP, 1.8), "DECK": (DOWN, 2.4)}.get(t)   # large enough to read the order
            if rule is None:
                continue
            vec, d = _unit(rule[0]), rule[1]
        else:
            continue
        if d:
            out[c.id] = tuple(x * d for x in vec)
    return out
