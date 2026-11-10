"""Visuals of the 44 beats (production layer L4): the 3D shots as SEQUENCE steps timed by the words of the locked
narration, and the 2D cards. story.py keeps the narration (locked, c-r2) and merges these specs into
script/visual_beats.json, so the sentences are never touched here.

Rules (review/PRODUCTION_PLAN.md):
- every number on screen and every MOVE / ROTATE amount comes from analysis/results.json (read below), never typed in;
- conceptual motion (OSCILLATE) carries the label "Conceptual motion visualization — not a hydrodynamic simulation"
  as a NOTE for the whole beat;
- moorings and joints are conceptual geometry ("not sized");
- no photograph of Schoonschip until a licence is granted: schematic drawings only.
"""
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
ROOT = PROJECT.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT))
from cards import (ACCENT, ASPECT, BELL, BG, BUBBLE, CHAR_W, CONCRETE, CUFF, DRINKING, FAINT, GOLD, INK, LAND, MUTED,   # noqa: E402
                   PLASTER, POWER, ROOF, SEABED, THUMB, WARN, WASTE, WATER, WATER_CUT, Card, box_points, icon, pill)
from engine.arch.families import floating as F   # noqa: E402
from engine.motion import CONCEPT_MOTION_LABEL   # noqa: E402

RES = json.loads((PROJECT / "analysis/results.json").read_text())
TIMING = {b["id"]: b for b in json.loads((HERE / "timing.json").read_text())["beats"]}
STEPS = RES["storey_branch"]["steps"]                      # 3 storeys -> 4 storeys -> 4 storeys with a 4.5 m hull
SINK = round(STEPS[1]["draft_m"] - STEPS[0]["draft_m"], 3)       # 0.332 m deeper with the fourth storey
EXT = 0.5                                                  # the hull extension of the asset (extension_m)
RISE = round(STEPS[1]["draft_m"] + EXT - STEPS[2]["draft_m"], 3)  # 0.436 m: the deeper hull floats up to its new draft
NET_UP = round(STEPS[2]["freeboard_m"] - STEPS[0]["freeboard_m"], 3)   # +0.104 m: end of B10 relative to the model
TILT = RES["list_example"]["list_deg"]                     # 0.421 degrees for 100 t moved 15 m
LOAD_SHIFT = RES["list_example"]["d_m"]


def m(x):
    return f"{x:.2f}".rstrip("0").rstrip(".")


VISUALS = {}


def part(concept, local):
    return {"concept": concept, "local": list(local) if isinstance(local, (list, tuple)) else [local]}


def grp(concept, group):
    return {"concept": concept, "group": group}


def at(sentence, word=None, offset=0.0, end=False, occurrence=None):
    a = {"sentence": sentence}
    if word:
        a["word"] = word
    if end:
        a["end"] = True
    if offset:
        a["offset"] = offset
    if occurrence:
        a["occurrence"] = occurrence
    return a


def note(nid, text, sentence=0, until=None, position="BOTTOM_RIGHT", word=None):
    a = {"id": nid, "type": "NOTE", "text": text, "sentence": sentence, "position": position}
    if until is not None:
        a["until"] = until
    if word:
        a["word"] = word
    return a


def label(nid, target, text, sentence, word=None, until=None, point="TOP", until_word=None):
    a = {"id": nid, "type": "COMPONENT_LABEL", "target": target, "point": point, "text": text, "sentence": sentence}
    if word:
        a["word"] = word
    if until is not None:
        a["until"] = until
    if until_word:
        a["until_word"] = until_word
    return a


def glow(targets, start, until, **kw):
    return {"do": "HIGHLIGHT", "targets": targets, "at": start, "until": until, "strength": 1.0, "tint": 0.6, **kw}


def step(do, targets, start, **kw):
    return {"do": do, "targets": targets, "at": start, **kw}


def hide(targets):
    """Hidden from the first frame (parts the beat brings in later, or that an earlier beat removed)."""
    return {"do": "FADE_OUT", "targets": targets, "at": 0, "seconds": 0}


def seq(camera, views, steps):
    return {"camera": camera, "views": views, "steps": steps}


def view(frame, at_=None, move=1.5, **kw):
    v = {"frame": frame, **kw}
    if at_ is not None:
        v.update(at=at_, move_seconds=move)
    return v


def visual(bid, strategy, goal, concepts, complexity="MEDIUM", **kw):
    VISUALS[bid] = {"strategy": strategy, "visual_goal": goal, "required_concepts": list(concepts),
                    "expected_complexity": complexity, **kw}


def duration(bid):
    return TIMING[bid]["duration"]


# ---------------------------------------------------------------- the district (Design C)
DISTRICT = "floating_district"
CELLS = F.district_cells()
CENTRE = (5, 2)   # the home platform that stays when the city is taken apart (B04)


def cell(c, r):
    return f"m{c:02d}{r}"


def platform_parts(cells, kinds=("hull", "deck", "buildings", "roofs")):
    concept = {"hull": "platform_hull", "deck": "deck", "buildings": "building_block", "roofs": "high_roof"}
    return [part(concept[k], [f"{cell(c, r)}_{k}" for c, r, _ in cells]) for k in kinds]


HOMES = [grp("building_block", "homes"), grp("high_roof", "homes")]
SERVICES = [grp("building_block", "services"), grp("high_roof", "services")]
FACADES = [part("facade_detail", [f"{cell(c, r)}_facade" for c, r, _ in CELLS])]
BUILDINGS_ALL = [{"concept": "building_block"}, {"concept": "high_roof"}] + FACADES
GROUND_DETAIL = [{"concept": "facade_detail"}]   # facades, paving, lawns, trees, play courts
MOORINGS = [{"concept": "mooring_pile"}, {"concept": "mooring_line"}, {"concept": "anchor"}]
UTILITIES = [{"concept": "utility_line"}]
WATER_SITE = [{"concept": "water_section"}]
NEAR_SHORE = platform_parts([(c, r, u) for c, r, u in CELLS if r <= 1 and 3 <= c <= 7])
ALL_HULLS = [{"concept": "platform_hull"}]

# ---------------------------------------------------------------- the platform in section (B06, B08-B10)
SEC = "floating_platform_section"
BLOCKS = (2, 4)   # the two blocks behind the cut


def storeys(blocks, levels, prefix=""):
    """A storey's walls, windows and (from the second up) its roof cap."""
    return [part("building_block", [f"{prefix}block{k}_storey{s}" for k in blocks for s in levels]),
            part("facade_detail", [f"{prefix}block{k}_storey{s}_windows" for k in blocks for s in levels])] + \
        ([part("high_roof", [f"{prefix}block{k}_roof{s}" for k in blocks for s in levels if s >= 2])] if any(s >= 2 for s in levels) else [])


STOREY4 = storeys(BLOCKS, (4,))
BUILDINGS3 = storeys(BLOCKS, (1, 2, 3))
FRONT_HALF = [grp(c, "front_half") for c in ("platform_hull", "bulkhead", "deck", "building_block", "high_roof", "facade_detail")]
FRONT_WATER = [grp("water_section", "front_water"), grp("ground", "front_water")]
SITE_WATERLINE = [grp("water_section", "waterline")]   # the site's line on the cut: it would cross the uncut water
FRONT_CUT = [grp(c, "front_half") for c in ("platform_hull", "bulkhead", "deck")] + storeys((1, 3), (1, 2, 3), "front_")   # B08
HULL_EXT = [part("platform_hull", ["hull_ext_west", "hull_ext_east", "hull_ext_north"]),
            part("bulkhead", [f"hull_ext_bulkhead_x{i}" for i in (1, 2, 3)]),
            part("section_cut", ["cut_ext_wall_west", "cut_ext_wall_east"] + [f"cut_ext_bulkhead_x{i}" for i in (1, 2, 3)])]
BOTTOM = [part("platform_hull", ["hull_bottom"]), part("section_cut", ["cut_bottom"]), part("water_section", ["water_below"])]
HULL = [grp("platform_hull", "hull"), {"concept": "bulkhead", "group": "bulkheads"}, {"concept": "deck", "group": "deck"},
        grp("section_cut", "section_cut"), grp("section_cut", "hull_bottom_cut")]
DISPLACED = [{"concept": "displaced_volume"}]
MARKER = [{"concept": "freeboard_marker"}]
DRAFT_DIM = [part("freeboard_marker", ["draft_dim"])]
DECK_REF = [part("freeboard_marker", ["deck_ref"])]
BOTTOM_REF = [part("freeboard_marker", ["bottom_ref"])]
MARKS = DRAFT_DIM + DECK_REF + BOTTOM_REF
SECTION_ONLY = FRONT_HALF + FRONT_WATER   # what a beat that opens on the section hides
EAST = [part("platform_hull", ["hull_wall_east"]), part("freeboard_marker", ["freeboard_marker"]),
        part("section_cut", ["cut_bulkhead_x3", "cut_wall_east"])]   # close on the waterline at the east wall
CORNER = [part("section_cut", ["cut_wall_east", "cut_bulkhead_x2", "cut_ext_wall_east", "cut_ext_bulkhead_x3"]),
          part("building_block", ["block4_storey1"])]   # the east half of the hull, bottom to deck, as it deepens
WHOLE_SECTION = HULL + BUILDINGS3
WHOLE_PLATFORM = HULL + BUILDINGS3 + FRONT_HALF
SECTION_NOTE = "Illustrative design, section through the middle"

# ---------------------------------------------------------------- the platform in 3D, with its load and neighbours (B11-B12)
STORY = "floating_platform_story"
ALL_BLOCKS = (1, 2, 3, 4)
NEIGHBOURS = [grp(c, f"neighbour{k}") for k in (1, 2, 3, 4)
              for c in ("platform_hull", "deck", "building_block", "high_roof", "facade_detail")]
STORY_STOREY4 = storeys(ALL_BLOCKS, (4,))
STORY_EXT = [grp("platform_hull", "hull_extension"), grp("bulkhead", "hull_extension")]
FRONT_OUT = [part("building_block", [f"block{k}_storey{s}" for k in (1, 3) for s in (1, 2, 3, 4)]),
             part("facade_detail", [f"block{k}_storey{s}_windows" for k in (1, 3) for s in (1, 2, 3, 4)]),
             part("high_roof", [f"block{k}_roof4" for k in (1, 3)])]   # the front blocks (their top caps; inner caps go first)
FRONT_INNER_ROOFS = [part("high_roof", [f"block{k}_roof{s}" for k in (1, 3) for s in (2, 3)])]   # caps inside the storeys
LOAD = [{"concept": "test_load"}]
LOAD_PATH = [part("freeboard_marker", ["load_path"])]
LEVEL_REF = [part("freeboard_marker", ["level_ref"])]
CENTRE_PLATFORM = [grp("platform_hull", "hull"), {"concept": "deck", "group": "deck"}] + storeys(ALL_BLOCKS, (1, 2, 3))
TILT_SHOWN = RES["list_example_shown_state"]   # the state B11 shows: four storeys, hull 4.5 m


def story_start(with_load=True):
    """The end of B10 in 3D: four storeys, the hull 0.5 m deeper, freeboard 1.15 m (relative to the model, built at
    the three-storey draft: bottom down by 0.5 - 0.104, everything else up by 0.104). The level reference stays."""
    out = [step("MOVE", [part("platform_hull", ["hull_bottom"])], 0, seconds=0, offset=[0.0, 0.0, round(NET_UP - EXT, 3)]),
           step("MOVE", {"except": [part("platform_hull", ["hull_bottom"])] + NEIGHBOURS + LEVEL_REF}, 0, seconds=0,
                offset=[0.0, 0.0, NET_UP]),
           hide(NEIGHBOURS)]
    if not with_load:
        out.append(hide(LOAD + LOAD_PATH + LEVEL_REF))
    return out


# ---------------------------------------------------------------- the neighbourhood (B14, B17, B22, B24)
HOOD = "neighbourhood_both_moorings"
PILES = [{"concept": "mooring_pile"}, grp("walkway_connector", "piles")]
LINES = [{"concept": "mooring_line"}, {"concept": "anchor"}]
HOOD_PLATFORMS = [grp(c, f"platform{k}") for k in range(1, 6)
                  for c in ("platform_hull", "deck", "building_block", "high_roof", "facade_detail")]


def joint(n):
    return [grp("walkway_connector", f"joint{n}"), grp("utility_line", f"joint{n}")]


# ======================================================================================== C1
visual("B01", "SEQUENCE", "Establishing aerial of the finished illustrative district in its sheltered bay, the quay in the "
       "foreground; a slow push toward the homes; NOTE 'Illustrative design'", [DISTRICT], "HIGH",
       sequence=seq("FLOAT_AERIAL", [view(ALL_HULLS + [{"concept": "breakwater"}], margin=0.04),
                                    view(platform_parts([x for x in CELLS if 2 <= x[0] <= 8 and x[1] <= 6], ("hull",)),
                                         at(1), move=3.4)], []),
       annotations=[note("B01_note", "Illustrative design", 0)])
visual("B02", "SEQUENCE", "The push-in continues over the homes, no claim on screen", [DISTRICT], "HIGH",
       sequence=seq("FLOAT_AERIAL", [view(platform_parts([x for x in CELLS if 2 <= x[0] <= 8 and x[1] <= 6], ("hull",))),
                                    view(platform_parts([x for x in CELLS if 3 <= x[0] <= 7 and 1 <= x[1] <= 4], ("hull",)),
                                         at(0, "design"), move=9.0, elevation=26.0)], []))

c = Card("B03")
c.tag("Already built, and proposed")
c.text("Amsterdam: Schoonschip", 0.27, 0.78, 0.036, 1)
c.text("built · 46 households · a little over 100 people", 0.27, 0.72, 0.024, 1, color=MUTED)
for k in range(46):   # one square per household, a schematic of the floating homes (no photograph)
    col, row = k % 12, k // 12
    c.rect([0.115 + col * 0.026, 0.42 + row * 0.055, 0.135 + col * 0.026, 0.46 + row * 0.055], PLASTER, border=INK,
           sentence=1, border_width=0.0015, word="households")
    c.elements[-1]["delay"] = round(0.01 * k, 3)
c.text("one square = one household (schematic)", 0.27, 0.36, 0.02, 1, color=MUTED)
c.text("Busan, South Korea: OCEANIX Busan", 0.73, 0.78, 0.036, 3)
c.text("proposed 2022 · design for 12,000 people", 0.73, 0.72, 0.024, 3, color=MUTED)
for k, (dx, dy) in enumerate(((0.0, 0.0), (-0.085, -0.13), (0.085, -0.13))):   # three linked hexagonal platforms (schematic)
    cx, cy = 0.73 + dx, 0.56 + dy
    hexa = [[cx + 0.06 / ASPECT * 1.6 * math.cos(math.radians(60 * i)), cy + 0.06 * math.sin(math.radians(60 * i))] for i in range(6)]
    c.polygon(hexa, "#C9D5DA", border=ACCENT, sentence=3, word="busan", border_width=0.003)
    c.elements[-1]["delay"] = round(0.2 * k, 2)
c.text("Architects' project page, Nov 2026: In Design", 0.73, 0.3, 0.026, 4, plate=True, word="architects")
c.line([[0.5, 0.3], [0.5, 0.8]], FAINT, 0.003, 2, dash=True)
visual("B03", "CARD", "Scale card: Schoonschip (built, 46 households, schematic squares, no photograph) beside OCEANIX "
       "Busan (proposed 2022, three linked platforms, schematic); 'Architects' project page, Nov 2026: In Design'", [], "LOW",
       graphic=c.spec())

KEEP = [x for x in CELLS if (x[0], x[1]) == CENTRE]
OTHERS = [x for x in CELLS if (x[0], x[1]) != CENTRE]
visual("B04", "SEQUENCE", "The district comes apart system by system (breakwater, moorings, utilities and routes, "
       "link-spans, buildings, platforms) until one empty platform remains", [DISTRICT], "HIGH",
       sequence=seq("FLOAT_AERIAL",
                    [view(ALL_HULLS, margin=0.08),
                     view(platform_parts(KEEP, ("hull",)), at(1, "back"), move=2.6, margin=0.3)],
                    [step("FADE_OUT", [{"concept": "breakwater"}], at(0, "take"), seconds=0.8),
                     step("FADE_OUT", MOORINGS, at(0, "take", 0.4), seconds=0.8),
                     step("FADE_OUT", UTILITIES + [{"concept": "access_route"}, grp("walkway_connector", "landings")], at(0, "apart"), seconds=0.8),
                     step("FADE_OUT", [{"concept": "link_span"}, grp("walkway_connector", "linkspans")], at(0, "apart", 0.4), seconds=0.8),
                     step("FADE_OUT", BUILDINGS_ALL + GROUND_DETAIL, at(1, "build"), seconds=0.9),
                     step("FADE_OUT", [grp("walkway_connector", "walkways")], at(1, "build", 0.3), seconds=0.8),
                     step("FADE_OUT", platform_parts(OTHERS, ("hull", "deck")), at(1, "back", 0.2), seconds=1.2)]))

# ======================================================================================== C2
BLOCK = [part("platform_hull", ["solid_block"]), part("section_cut", ["solid_block_cut"])]
cb = RES["clay_boat"]
CLAY_DEPTH = 15.0   # water_depth_m of floating_clay_boat_01 (the block rests on the seabed)
LIFT = round(CLAY_DEPTH - cb["solid_cube_side_m"] + 1.0, 3)   # the block first shows at the surface, 1 m above the water
visual("B05", "SEQUENCE", "Section: a block holding the hull's concrete appears at the surface and sinks to the seabed; the "
       "same concrete as a hollow 40 m box then settles at its calculated draft (hull only)", ["clay_boat"], "MEDIUM",
       sequence=seq("FLOAT_SECTION",
                    [view({"except": []}, margin=0.08)],
                    [step("MOVE", BLOCK, 0, seconds=0, offset=[0.0, 0.0, LIFT]),
                     hide(BLOCK), hide({"except": BLOCK}),
                     step("FADE_IN", BLOCK, at(1, "block", -0.2), seconds=0.6),
                     step("MOVE", BLOCK, at(2, "sinks", -0.2), seconds=2.6, offset=[0.0, 0.0, -LIFT],
                          easing="EASE_IN_OUT"),
                     step("REVEAL", {"except": BLOCK}, at(3, "hollow", -0.2), seconds=1.6, direction="FROM_ABOVE", distance=4.0),
                     glow({"except": BLOCK}, at(3, "floats", -0.3), at(3, end=True, offset=0.3))]),
       annotations=[label("B05_block", part("section_cut", "solid_block_cut"), f"{cb['concrete_m3']:,.0f} m³ of concrete", 2,
                          "dense", point="TOP"),
                    label("B05_box", part("platform_hull", "hull_wall_east"), "Same concrete, hollow", 3, "box", point="TOP"),
                    note("B05_note", f"Hull only, 40 m box: draft ≈ {m(cb['hollow_box_draft_hull_only_m'])} m", 3, word="floats")])

visual("B06", "SEQUENCE", "Section of the first platform (three storeys): the outline of the hull below the waterline, the "
       "water it pushes aside, lights up", [SEC], "MEDIUM",
       sequence=seq("FLOAT_SECTION", [view(WHOLE_SECTION, margin=0.07)],
                    [hide(SECTION_ONLY + STOREY4 + HULL_EXT + DISPLACED + MARKER),
                     step("FADE_IN", DISPLACED, at(0, "pushes", -0.2), seconds=0.8),
                     glow(DISPLACED, at(0, "aside", -0.2), at(1, end=True))]),
       annotations=[label("B06_water", {"concept": "displaced_volume"}, "Water pushed aside", 0, "aside", point="BOTTOM"),
                    note("B06_rule", "1 t added ≈ 1 m³ more water pushed aside", 1, word="every"),
                    note("B06_note", SECTION_NOTE, 0, position="TOP_RIGHT")])

c = Card("B07")
c.tag("Schoonschip, Amsterdam (schematic)")
SCALE = 0.026   # card units per metre (vertical)
GL = 0.46       # waterline
c.rect([0.06, 0.24, 0.94, GL], WATER, sentence=0)
c.line([[0.06, GL], [0.94, GL]], WATER_CUT, 0.004, 0)
hx0, hx1 = 0.16, 0.42
c.rect([hx0, GL - 1.6 * SCALE, hx1, GL + 0.7 * SCALE], CONCRETE, border=INK, sentence=1, word="floats", border_width=0.002)
c.rect([hx0 + 0.02, GL + 0.7 * SCALE, hx1 - 0.02, GL + 0.7 * SCALE + 7.5 * SCALE], PLASTER, border=INK, sentence=1, word="houses",
       border_width=0.002)
c.text("concrete float", (hx0 + hx1) / 2, GL - 0.8 * SCALE, 0.022, 1, word="floats")
c.text("340–350 t", (hx0 + hx1) / 2, GL + 4.5 * SCALE, 0.04, 2, color=ACCENT, word="weighs")
cube = RES["schoonschip_heaviest_home"]["340_t"]["equivalent_cube_side_m"]
side_y = 7.0 * SCALE
cx0 = 0.62
c.rect([cx0, GL - side_y, cx0 + side_y / ASPECT, GL], WATER_CUT, border=ACCENT, sentence=3, word="cube", border_width=0.004)
c.text("≈ 340–350 m³ of water", cx0 + side_y / ASPECT / 2 + 0.11, GL - side_y / 2 + 0.03, 0.026, 3, align="LEFT", word="cubic")
c.text("a cube about 7 m on each side", cx0 + side_y / ASPECT / 2 + 0.11, GL - side_y / 2 - 0.015, 0.022, 3, align="LEFT", color=MUTED,
       word="cube")
for k, x in enumerate((0.84, 0.88)):   # two builders for scale (schematic figures, 1.8 m)
    c.circle([x, GL + 1.8 * SCALE - 0.006], 0.006, INK, 3, word="side")
    c.line([[x, GL], [x, GL + 1.8 * SCALE - 0.012]], INK, 0.004, 3, word="side")
c.text("1.8 m figures", 0.86, GL - 0.03, 0.018, 3, color=MUTED, word="side")
visual("B07", "CARD", "Schematic section of a floating home on its concrete float; '340–350 t'; the water it pushes aside "
       "as a cube about 7 m on each side, two 1.8 m figures for scale", [], "LOW", graphic=c.spec())

visual("B08", "SEQUENCE", "The whole first platform (four blocks of three storeys) at an angle; its front half and the water "
       "in front are taken away to show the cut; square on, the draft is drawn as a dimension; the buildings ghost and the "
       "concrete hull lights up: more than half of the weight", [SEC], "MEDIUM",
       sequence=seq("FLOAT_SECTION",
                    [view(WHOLE_PLATFORM, azimuth=-62.0, elevation=16.0, margin=0.08),
                     view(WHOLE_SECTION, at(1, "altogether", -0.2), move=2.4, margin=0.07)],
                    [hide(STOREY4 + storeys((1, 3), (4,), "front_") + HULL_EXT + MARKER + DISPLACED + SITE_WATERLINE),
                     glow(BUILDINGS3 + storeys((1, 3), (1, 2, 3), "front_"), at(0, "blocks", -0.3), at(0, end=True, offset=-0.3)),
                     step("FADE_OUT", FRONT_CUT + FRONT_WATER, at(0, end=True, offset=0.1), seconds=1.0),
                     step("FADE_IN", SITE_WATERLINE, at(0, end=True, offset=0.6), seconds=0.5),
                     step("FADE_IN", DRAFT_DIM, at(1, "floats", -0.2), seconds=0.6),
                     step("FADE_OUT", DRAFT_DIM, at(2, "surprise", -0.4), seconds=0.5),
                     step("GHOST", BUILDINGS3, at(2, "half", -0.4), seconds=0.8, transparency=0.8),
                     glow(HULL, at(2, "concrete", -0.3), at(2, end=True, offset=-0.2)),
                     step("UNGHOST", BUILDINGS3, at(2, end=True, offset=-0.9), seconds=0.8)]),
       annotations=[note("B08_cut", "Cut through the middle", 1, position="TOP_LEFT"),
                    label("B08_draft", part("freeboard_marker", "draft_dim"), f"Draft ≈ {m(STEPS[0]['draft_m'])} m", 1, "floats",
                          until=2, point="LEFT"),
                    label("B08_hull", part("section_cut", "cut_wall_east"),
                          f"Hull: ≈ {round(100 * RES['design_A']['mid']['mass_t']['hull_concrete'] / RES['design_A']['mid']['mass_t']['total'])}% of the weight",
                          2, "concrete", point="RIGHT"),
                    note("B08_note", SECTION_NOTE, 0, position="TOP_RIGHT")])

visual("B09", "SEQUENCE", "Square-on section: a fourth storey is set down (the whole section in view); the camera moves close "
       "to the east wall and stops; a dashed line keeps the deck's first level; the platform settles by the calculated 0.33 m "
       "and the freeboard dimension (waterline to deck) shrinks from 1.04 to 0.71 m", [SEC], "MEDIUM",
       sequence=seq("FLOAT_SECTION",
                    [view(WHOLE_SECTION, margin=0.07), view(EAST, at(1, "the", -0.7), move=1.4, margin=0.12)],
                    [hide(SECTION_ONLY + STOREY4 + HULL_EXT + DISPLACED + DRAFT_DIM + DECK_REF + BOTTOM_REF),
                     step("REVEAL", STOREY4, at(0, "fourth", -0.3), seconds=1.2, direction="FROM_ABOVE", distance=6.0, sound="STONE"),
                     step("FADE_IN", DECK_REF, at(1, "settles", -0.3), seconds=0.5),
                     step("MOVE", {"except": DECK_REF + BOTTOM_REF}, at(1, "about", -0.1), seconds=1.8, offset=[0.0, 0.0, -SINK]),
                     step("FADE_OUT", DECK_REF, at(2, end=True, offset=-0.9), seconds=0.6)]),
       annotations=[label("B09_fb0", part("freeboard_marker", "freeboard_marker"), f"Freeboard ≈ {m(STEPS[0]['freeboard_m'])} m", 0,
                          until=1, point="RIGHT"),
                    label("B09_before", part("freeboard_marker", "deck_ref"), "Deck before", 1, "meter", point="TOP_LEFT"),
                    label("B09_fb1", part("freeboard_marker", "freeboard_marker"),
                          f"Freeboard: {m(STEPS[0]['freeboard_m'])} → {m(STEPS[1]['freeboard_m'])} m", 2, "shrinks", point="RIGHT"),
                    note("B09_note", "+1 story, same load per m² of floor", 0, word="fourth")])

visual("B10", "SEQUENCE", "Two framings only, the camera still while anything changes: the east half of the section from deck "
       "to bottom while the bottom moves down 0.5 m and the walls and bulkheads grow with it (gold; the old bottom dashed for "
       "a while); then close on the waterline while the platform floats up to a freeboard of 1.15 m (the previous deck level "
       "dashed)", [SEC], "MEDIUM",
       sequence=seq("FLOAT_SECTION",
                    [view(EAST, margin=0.12),
                     view(CORNER, 0.2, move=1.6, margin=0.07),
                     view(EAST, at(1, end=True, offset=-0.6), move=1.3, margin=0.12)],
                    [step("MOVE", {"except": []}, 0, seconds=0, offset=[0.0, 0.0, -SINK]),
                     hide(SECTION_ONLY + HULL_EXT + DISPLACED + DRAFT_DIM + DECK_REF + BOTTOM_REF),
                     step("FADE_IN", BOTTOM_REF, at(0, "half", -0.2), seconds=0.5),
                     step("MOVE", BOTTOM, at(0, "deeper", -0.3), seconds=1.6, offset=[0.0, 0.0, -EXT]),
                     step("REVEAL", HULL_EXT, at(0, "deeper", -0.3), seconds=1.6, direction="FROM_ABOVE", distance=EXT,
                          fade_end=0.3, easing="SMOOTH", sound="STONE_HEAVY"),
                     step("FADE_OUT", BOTTOM_REF, at(1, end=True, offset=-0.6), seconds=0.6),
                     step("FADE_IN", DECK_REF, at(2, "and", -0.2), seconds=0.4),
                     step("MOVE", {"except": DECK_REF + BOTTOM_REF}, at(2, "brings", -0.1), seconds=1.8, offset=[0.0, 0.0, RISE])]),
       annotations=[label("B10_fb0", part("freeboard_marker", "freeboard_marker"), f"Freeboard ≈ {m(STEPS[1]['freeboard_m'])} m", 0,
                          until=1, point="RIGHT"),
                    label("B10_ext", part("section_cut", "cut_ext_wall_east"),
                          f"+{m(EXT)} m hull: ≈ {RES['storey_branch']['extra_concrete_for_deeper_hull_t']:.0f} t (+{round(100 * RES['storey_branch']['extra_concrete_share_of_hull'])}%)",
                          1, "adds", until=2, point="RIGHT"),
                    label("B10_fb1", part("freeboard_marker", "freeboard_marker"),
                          f"Freeboard: {m(STEPS[1]['freeboard_m'])} → {m(STEPS[2]['freeboard_m'])} m", 2, "centimeters", point="RIGHT"),
                    note("B10_note", "Or: lighter buildings", 3, word="lighter")])

visual("B11", "SEQUENCE", "The same platform whole (four storeys, deeper hull), seen square on: the front buildings are taken "
       "away (inner roof caps first, so nothing shows through); a dashed level line and the deck's outline stay put; a 100 t "
       "block slides 15 m along a drawn arrow toward the edge, and the platform tilts by the angle calculated for this state "
       "(true scale)", [STORY], "MEDIUM",
       sequence=seq("FLOAT_SECTION",
                    [view(CENTRE_PLATFORM + STORY_STOREY4, elevation=12.0, margin=0.08)],
                    story_start(with_load=True) + [
                        hide(FRONT_INNER_ROOFS + LOAD_PATH + LEVEL_REF),
                        step("FADE_OUT", FRONT_OUT, at(0, "tip", -0.4), seconds=1.0),
                        step("FADE_IN", LEVEL_REF, at(1, "move", -0.6), seconds=0.6),
                        step("FADE_IN", LOAD_PATH, at(1, "move", -0.4), seconds=0.6),
                        step("MOVE", LOAD, at(1, "tons", -0.2), seconds=2.2, offset=[LOAD_SHIFT, 0.0, 0.0]),
                        step("ROTATE", {"except": NEIGHBOURS + LEVEL_REF}, at(1, "tilts", -0.3), seconds=2.0, axis="Y",
                             degrees=TILT_SHOWN["list_deg"], pivot=[0.0, 0.0, 0.0])]),
       annotations=[label("B11_load", {"concept": "test_load"}, f"{RES['list_example']['w_t']} t", 1, "move", until=2, point="TOP"),
                    label("B11_path", part("freeboard_marker", "load_path"), f"{LOAD_SHIFT} m", 1, "edge", until=2, point="BOTTOM"),
                    note("B11_tilt", f"{TILT_SHOWN['w_t']} t moved {TILT_SHOWN['d_m']} m: tilt ≈ {m(round(TILT_SHOWN['list_deg'], 1))}° (true scale)", 1,
                         word="tilts"),
                    note("B11_note", "Illustrative design", 0, position="TOP_RIGHT")])

per_platform = RES["residents_by_storeys"]["40m_3_storeys"]
visual("B12", "SEQUENCE", "Back to the three-storey design: the fourth storey fades and the deck returns to its first "
       "freeboard; then four copies are towed in around a small basin", [STORY], "MEDIUM",
       sequence=seq("FLOAT_THREE_QUARTER",
                    [view(CENTRE_PLATFORM + STORY_STOREY4, margin=0.1),
                     view(CENTRE_PLATFORM + NEIGHBOURS, at(1, "lot", -0.6), move=2.4, margin=0.06)],
                    story_start(with_load=False) + [
                        step("FADE_OUT", STORY_STOREY4, at(0, "story", -0.2), seconds=1.0),
                        step("FADE_OUT", STORY_EXT, at(0, "story", -0.2), seconds=0.6),
                        step("MOVE", [part("platform_hull", ["hull_bottom"])], at(0, "version", 0.3), seconds=1.2,
                             offset=[0.0, 0.0, round(EXT - NET_UP, 3)]),
                        step("MOVE", {"except": [part("platform_hull", ["hull_bottom"])] + NEIGHBOURS + LEVEL_REF}, at(0, "version", 0.3),
                             seconds=1.2, offset=[0.0, 0.0, -NET_UP]),
                    ] + [step("REVEAL", [grp(c, f"neighbour{k}") for c in ("platform_hull", "deck", "building_block", "high_roof",
                                                                            "facade_detail")],
                              at(1, "lot", -0.3 + 0.3 * (k - 1)), seconds=1.8, direction="OUTWARD", distance=40.0) for k in (1, 2, 3, 4)]),
       annotations=[note("B12_people", f"3 stories: about {per_platform} residents per platform", 0, word="people")])

pair = RES["revisions"]["B_neighbours_2_vs_4_storeys"]
WALK = [part("walkway_connector", ["walkway", "walkway_hinge0", "walkway_hinge1"])]
visual("B13", "SEQUENCE", "Side elevation of two identical platforms with two and four storeys at their own drafts; close on "
       "the 0.66 m step between the decks; a hinged walkway arrives and spans it (no part shown failing)",
       ["floating_pair"], "MEDIUM",
       sequence=seq("FLOAT_SECTION",
                    [view({"except": WALK}, margin=0.07),
                     view(WALK + [part("deck", ["platform_a_deck", "platform_b_deck"])], at(1, "decks", -0.6), move=2.2, margin=0.25)],
                    [hide(WALK),
                     glow([grp("building_block", "platform_a"), grp("high_roof", "platform_a")], at(0, "two", -0.2), at(0, "four", -0.2)),
                     glow([grp("building_block", "platform_b"), grp("high_roof", "platform_b")], at(0, "four", -0.1), at(0, end=True, offset=0.4)),
                     step("REVEAL", WALK, at(3, "walkways", -0.3), seconds=1.2, direction="FROM_ABOVE", distance=3.0),
                     glow([part("walkway_connector", ["walkway_hinge0", "walkway_hinge1"])], at(3, "hinged", -0.2), at(3, end=True))]),
       annotations=[label("B13_step", part("deck", "platform_b_deck"), f"Decks ≈ {m(pair['deck_level_step_m'])} m apart", 1, "decks",
                          point="TOP_LEFT"),
                    note("B13_free", "Each floating on its own (illustrative)", 1, word="floating"),
                    note("B13_ballast", "Another option: ballast to even out the decks", 4, word="ballast", position="TOP_LEFT")])

visual("B14", "SEQUENCE", "Close-up of one joint: the gap, the hinged walkway, the flexible utility link and the fenders, "
       "each lit as it is named (conceptual geometry, not sized)", [HOOD], "MEDIUM",
       sequence=seq("FLOAT_THREE_QUARTER",
                    [view(joint(1), margin=0.3, elevation=48.0)],   # steep enough to see into the gap past the buildings
                    [hide(LINES),
                     glow(joint(1), at(0, "trouble", -0.4), at(1, "research")),
                     glow([part("walkway_connector", ["joint1_walkway_hinge0", "joint1_walkway_hinge1"])], at(1, "connectors", -0.2),
                          at(2, "one")),
                     glow([grp("utility_line", "joint1")], at(2, "flexibly", -0.2), at(2, "spaces")),
                     glow([part("walkway_connector", ["joint1_fendera", "joint1_fenderb"])], at(2, "collide", -0.2),
                          at(2, end=True, offset=0.3))]),
       annotations=[label("B14_walk", part("walkway_connector", "joint1_walkway"), "Hinged walkway", 0, "trouble", point="TOP"),
                    label("B14_util", grp("utility_line", "joint1"), "Flexible utility link", 2, "flexibly", point="BOTTOM"),
                    label("B14_fender", part("walkway_connector", "joint1_fendera"), "Fender", 2, "collide", point="BOTTOM"),
                    note("B14_note", "Conceptual geometry, not sized", 0)])

# ---------------------------------------------------------------- B15-B16: one plan diagram that keeps evolving
GRID_X0, GRID_X1, GRID_Y0, GRID_Y1 = 0.45, 0.94, 0.24, 0.84
tr = RES["module_size_tradeoff"]["by_side"]


def grid(c, cols, rows, side, sentence, word=None, until=None, until_word=None, skip=(), color=CONCRETE, joints=True,
         row_delay=0.05, joint_word=None, joint_sentence=None):
    """Square cells of `side` (card x units) centred in the grid area, appearing row by row; the shared edges between
    neighbours as accent lines (joints)."""
    w, h = side, side * ASPECT
    x0 = (GRID_X0 + GRID_X1) / 2 - cols * w / 2
    y0 = (GRID_Y0 + GRID_Y1) / 2 - rows * h / 2
    cells = [(i, j) for j in range(rows) for i in range(cols) if (i, j) not in skip]
    for i, j in cells:
        c.rect([x0 + i * w + 0.0015, y0 + j * h + 0.0015 * ASPECT, x0 + (i + 1) * w - 0.0015, y0 + (j + 1) * h - 0.0015 * ASPECT],
               color, sentence=sentence, word=word, layer=1)
        c.elements[-1]["delay"] = round(row_delay * j, 3)
        if until is not None:
            c.gone(until, until_word)
    cellset = set(cells)
    edges = sum((i + 1, j) in cellset for i, j in cells) + sum((i, j + 1) in cellset for i, j in cells)
    if joints:   # each run of shared edges along a grid line as one line (fewer card elements)
        runs = []
        for i in range(cols - 1):
            run = [j for j in range(rows) if (i, j) in cellset and (i + 1, j) in cellset]
            runs += [[[x0 + (i + 1) * w, y0 + a * h], [x0 + (i + 1) * w, y0 + (b + 1) * h]] for a, b in _spans(run)]
        for j in range(rows - 1):
            run = [i for i in range(cols) if (i, j) in cellset and (i, j + 1) in cellset]
            runs += [[[x0 + a * w, y0 + (j + 1) * h], [x0 + (b + 1) * w, y0 + (j + 1) * h]] for a, b in _spans(run)]
        for pts in runs:
            c.line(pts, ACCENT, 0.0035, joint_sentence if joint_sentence is not None else sentence, word=joint_word, layer=2)
            if until is not None:
                c.gone(until, until_word)
    return len(cells), edges


def _spans(indices):
    """Consecutive runs [(first, last)] of sorted integers."""
    out = []
    for k in indices:
        if out and k == out[-1][1] + 1:
            out[-1][1] = k
        else:
            out.append([k, k])
    return [tuple(x) for x in out]


cs = RES["city_scale"]["40_m2_per_resident"]
c = Card("B15")
c.tag("How many platforms? (illustrative)")
c.text("10,000 people", 0.22, 0.8, 0.046, 0)
c.text("40 m² of floor each", 0.22, 0.7, 0.032, 1, word="square")
c.text("30 home + 10 schools, shops, services", 0.22, 0.65, 0.022, 1, color=MUTED, word="30")
c.text(f"≈ {cs['deck_area_ha']:.0f} ha of platform", 0.22, 0.55, 0.032, 2, word="hectares")
n40, e40 = grid(c, 19, 11, (GRID_X1 - GRID_X0) / 19.5, 2, word="hectares", joint_sentence=3, joint_word="connections")
c.text(f"≈ {tr['40m']['modules']} platforms of 40 m", 0.22, 0.45, 0.032, 3, word="platforms")
c.text(f"up to {tr['40m']['shared_edges_in_grid_max']} joints", 0.22, 0.4, 0.028, 3, color=ACCENT, word="connections")
assert n40 == tr["40m"]["modules"] and e40 <= tr["40m"]["shared_edges_in_grid_max"], (n40, e40)   # "up to": the most compact grid
visual("B15", "CARD", "One plan diagram (continues into B16): 40 m cells appear until about 33 ha are covered (209 cells); "
       "the joints between them light up as they are counted", [], "LOW", graphic=c.spec())

c = Card("B16")
c.tag("How many platforms? (illustrative)")
c.text("10,000 people", 0.22, 0.8, 0.046, 0)
c.text("Bigger platforms: fewer joints", 0.22, 0.7, 0.03, 0, color=ACCENT)
grid(c, 19, 11, (GRID_X1 - GRID_X0) / 19.5, 0, until=1, until_word="meters")
s100 = (GRID_X1 - GRID_X0) / 19.5 * 2.5
n100, e100 = grid(c, 7, 5, s100, 1, word="meters", skip={(6, 4)}, until=4, until_word="our")
assert n100 == tr["100m"]["modules"], n100
c.text(f"{tr['100m']['modules']} platforms of 100 m · {tr['100m']['shared_edges_in_grid_max']} joints", 0.22, 0.6, 0.026, 1,
       word="would").gone(4, "our")
c.text(f"≈ {round(tr['100m']['module_mass_t'], -3):,.0f} t each", 0.22, 0.54, 0.032, 2, color=WARN, word="weigh").gone(4, "our")
c.text("to build, launch and tow", 0.22, 0.49, 0.022, 2, color=MUTED, word="launch").gone(4, "our")
c.text("Schoonschip's floats: cast on the quay,", 0.22, 0.4, 0.022, 3, word="even").gone(4, "our")
c.text("too big for houseboat dry docks", 0.22, 0.36, 0.022, 3, word="even").gone(4, "our")
s60 = (GRID_X1 - GRID_X0) / 19.5 * 1.5
lagoon = {(c_, 8 - r_) for c_, r_ in F.DISTRICT_LAGOON}
n60, e60 = grid(c, F.DISTRICT_COLS, F.DISTRICT_ROWS, s60, 4, word="our", skip=lagoon)
assert n60 == tr["60m"]["modules"] == RES["district_C"]["modules"], n60
c.text(f"Our district: {tr['60m']['modules']} platforms of 60 m", 0.22, 0.6, 0.03, 4, word="our")
c.text(f"3 stories · {tr['60m']['shared_edges_in_grid_max']} joints at most", 0.22, 0.54, 0.024, 4, color=MUTED, word="story")
c.text("a middle choice for this illustration,", 0.22, 0.46, 0.024, 4, word="middle")
c.text("not an optimum", 0.22, 0.42, 0.024, 4, word="optimum")
visual("B16", "CARD", "Same diagram as B15: the cells regroup into 34 platforms of 100 m (fewer joints; about 30,000 t "
       "each), the Schoonschip quay note, then settle on the district's 93 platforms of 60 m around their lagoon", [], "LOW",
       graphic=c.spec())

# ======================================================================================== C4
PHASE = {1: 0.0, 2: 110.0, 3: 220.0, 4: 300.0, 5: 40.0}
TILT_AXIS = {1: "X", 2: "Y", 3: "X", 4: "Y", 5: "X"}
OWN_JOINTS = {1: [1], 2: [], 3: [2], 4: [3], 5: [4]}   # each joint moves with one of its two platforms
PITCH = 46.0   # neighbourhood: 40 m platforms, 6 m gaps
CENTRES = {k: (i * PITCH, j * PITCH) for k, (i, j) in enumerate(F.NEIGHBOURHOOD, 1)}
d17 = duration("B17")
visual("B17", "SEQUENCE", "Five platforms rise, fall and tilt out of step; the gaps open and close and the walkways follow "
       "one side (conceptual motion, labelled)", [HOOD], "MEDIUM",
       motion_label=CONCEPT_MOTION_LABEL,
       sequence=seq("FLOAT_THREE_QUARTER", [view(HOOD_PLATFORMS, margin=0.06)],
                    [hide(PILES + LINES)] +
                    [step("OSCILLATE", [grp(cc, f"platform{k}") for cc in ("platform_hull", "deck", "building_block", "high_roof",
                                                                          "facade_detail")]
                          + [r for n in OWN_JOINTS[k] for r in joint(n)], 0.3, seconds=round(d17 - 0.6, 2), amplitude_m=0.3,
                          period_seconds=5.5, phase_degrees=PHASE[k], tilt_degrees=0.8, axis=TILT_AXIS[k],
                          pivot=[CENTRES[k][0], CENTRES[k][1], 0.0], fade_seconds=1.2) for k in range(1, 6)]),
       annotations=[note("B17_label", CONCEPT_MOTION_LABEL, 0)])

c = Card("B18")
c.tag("Living on the water")
GL = 0.42
c.rect([0.08, 0.24, 0.92, GL], WATER, sentence=0)
hx0, hx1 = 0.3, 0.52
c.rect([hx0, GL - 0.05, hx1, GL + 0.02], CONCRETE, border=INK, sentence=0, border_width=0.002)
c.rect([hx0 + 0.015, GL + 0.02, hx1 - 0.015, GL + 0.14], PLASTER, border=INK, sentence=0, border_width=0.002)
c.rect([hx0 + 0.015, GL + 0.14, hx1 - 0.015, GL + 0.26], PLASTER, border=INK, sentence=0, border_width=0.002)
c.text("upper floor", (hx0 + hx1) / 2, GL + 0.2, 0.022, 0)
arc = [[0.41 + 0.16 / ASPECT * math.cos(math.radians(a)), GL + 0.13 + 0.16 * math.sin(math.radians(a))] for a in range(60, 121, 5)]
t = c.drawn(arc, ACCENT, 0.006, 1, word="rock", seconds=0.6)
c.arrow(arc[-2], arc[-1], ACCENT, 0.008, 1).at("rock", t)
c.arrow(arc[1], arc[0], ACCENT, 0.008, 1).at("rock", t)
for k in range(3):   # storm wind
    c.drawn([[0.1, 0.7 - k * 0.04], [0.22, 0.7 - k * 0.04]], MUTED, 0.004, 1, word="storms", seconds=0.3, delay=0.1 * k)
c.polygon([[0.66, GL], [0.9, GL], [0.92, GL + 0.06], [0.64, GL + 0.06]], "#7D8B93", sentence=1, word="cruise")
c.rect([0.7, GL + 0.06, 0.86, GL + 0.11], "#C9CED1", sentence=1, word="cruise")
c.text("large cruise ship passing", 0.78, GL + 0.15, 0.02, 1, color=MUTED, word="cruise")
c.rect([hx0 + 0.008, GL + 0.135, hx1 - 0.008, GL + 0.268], None, border=WARN, sentence=2, word="upper", border_width=0.005)
c.text("felt most on the upper floor", (hx0 + hx1) / 2, GL + 0.31, 0.026, 2, color=WARN, word="upper")
c.text("Source: Yale Environment 360, 2021", 0.5, 0.2, 0.018, 0, color=MUTED)
visual("B18", "CARD", "Floating home in section rocking (storm, passing cruise ship); the upper floor marked; source "
       "line", [], "LOW", graphic=c.spec())

c = Card("B19")
c.tag("Very large platforms bend")
flat = [[0.12, 0.5], [0.88, 0.5]]
c.line(flat, CONCRETE, 0.03, 0)
c.line(flat, FAINT, 0.003, 0, dash=True, word="bend", layer=1)
bent = [[0.12 + 0.76 * k / 20, 0.5 + 0.04 * math.sin(math.pi * (k / 20) * 2.0 - 0.5)] for k in range(21)]
c.drawn(bent, ACCENT, 0.012, 0, word="bend", seconds=0.9)
c.text("bending exaggerated, conceptual", 0.5, 0.36, 0.024, 0, color=MUTED, word="bend")
c.text("How exactly? An open research problem", 0.5, 0.68, 0.034, 1, word="open")
visual("B19", "CARD", "A long platform drawn flat, then bending (exaggerated, conceptual); 'an open research problem'", [], "LOW",
       graphic=c.spec())

c = Card("B20")
c.tag("Where to build")
for k, (cx, title) in enumerate(((0.28, "Open coast"), (0.72, "Sheltered bay"))):
    c.text(title, cx, 0.8, 0.034, 1, word="fetch" if k else "sea")
c.rect([0.08, 0.3, 0.48, 0.72], WATER, sentence=1, word="sea")
c.rect([0.08, 0.3, 0.48, 0.38], LAND, sentence=1, word="sea")
for k in range(4):   # long waves rolling in over a long fetch
    y = 0.68 - k * 0.075
    c.drawn([[0.1 + 0.04 * k, y], [0.42, y]], ACCENT, 0.005, 1, word="fetch", seconds=0.5, delay=0.12 * k)
c.text("long fetch: big waves", 0.28, 0.25, 0.022, 1, color=MUTED, word="fetch")
bay = [[0.52, 0.3], [0.92, 0.3], [0.92, 0.72], [0.86, 0.72], [0.82, 0.54], [0.66, 0.5], [0.6, 0.72], [0.52, 0.72]]
c.rect([0.52, 0.3, 0.92, 0.72], WATER, sentence=1, word="gulf")
c.polygon([[0.52, 0.3], [0.92, 0.3], [0.92, 0.66], [0.85, 0.66], [0.8, 0.5], [0.66, 0.47], [0.6, 0.66], [0.52, 0.66]], LAND,
          sentence=1, word="gulf")
c.text("land", 0.72, 0.36, 0.022, 1, color=MUTED, word="gulf")
c.drawn([[0.66, 0.69], [0.8, 0.69]], ACCENT, 0.005, 1, word="moderate", seconds=0.4)
c.text("limited fetch: moderate waves", 0.72, 0.25, 0.022, 1, color=MUTED, word="moderate")
for i in range(5):   # the district in the bay, beside the city's quay
    for j in range(2):
        c.rect([0.66 + i * 0.022, 0.505 + j * 0.035, 0.68 + i * 0.022, 0.535 + j * 0.035], CONCRETE, sentence=2, word="sheltered")
c.text("our city: sheltered, connected to the shore", 0.5, 0.18 + 0.03, 0.026, 2, plate=True, word="connected")
visual("B20", "CARD", "Two schematic coasts: open coast with long fetch vs a sheltered bay with limited fetch; the district "
       "placed in the bay beside the city's quay", [], "LOW", graphic=c.spec())

visual("B21", "SEQUENCE", "From the plan to an aerial view: inner homes light, then the outer ring of services; the "
       "breakwater arrives on the open side; NOTE 'reduces waves, does not remove storm risk'", [DISTRICT, "breakwater"], "HIGH",
       sequence=seq("FLOAT_AERIAL",
                    [view(ALL_HULLS + [{"concept": "breakwater"}], azimuth=-90.0, elevation=88.0, margin=0.05),
                     view(ALL_HULLS + [{"concept": "breakwater"}], at(1, "following", -0.3), move=3.0, margin=0.05)],
                    [hide([{"concept": "breakwater"}]),
                     glow(HOMES, at(1, "go", -0.4), at(1, "functions")),   # Whisper hears "homes" as "holmes"
                     glow(SERVICES, at(1, "outer", -0.3), at(2, "where")),
                     step("REVEAL", [{"concept": "breakwater"}], at(2, "breakwater", -0.3), seconds=1.6, direction="BACK",
                          distance=60.0, stagger_seconds=0.06),
                     glow([{"concept": "breakwater"}], at(3, "floating", -0.2), at(3, "energy"))]),
       annotations=[note("B21_note", "Reduces waves; does not remove storm risk", 3, word="enough"),
                    label("B21_homes", part("building_block", f"{cell(5, 2)}_buildings"), "Homes", 1, "go", until=2),
                    label("B21_ring", part("building_block", f"{cell(0, 4)}_buildings"), "Services", 1, "outer", until=3,
                          point="LEFT")])

# ======================================================================================== C5
visual("B22", "SEQUENCE", "Low view of the neighbourhood: the water ghosts and the steel piles beneath light up",
       [HOOD], "MEDIUM",
       sequence=seq("FLOAT_UNDERWATER", [view([grp(cc, f"platform{k}") for k in (1, 2) for cc in ("platform_hull", "deck")] + PILES,
                                              margin=0.1)],
                    [hide(LINES),
                     step("GHOST", WATER_SITE, at(1, "floating", -0.3), seconds=1.2, transparency=0.85),
                     glow(PILES, at(1, "poles", -0.4), at(1, end=True, offset=0.3))]),
       annotations=[label("B22_pile", part("mooring_pile", "platform2_pile1"), "Steel pile", 1, "poles", point="BOTTOM")])

c = Card("B23")
c.tag("Water level and the hinged bridge (illustrative)")
ls = RES["link_span"]
HINGE = (0.2, 0.52)
BR = 0.42                    # bridge length on the card (x units) for 25 m
k_m = BR * ASPECT / 25.0     # card height units per metre at that scale
swing = 25.0 * math.tan(math.radians(ls["25_m_bridge"]["max_slope_deg_each_way"]))   # metres up or down at the far end
c.rect([0.04, 0.24, HINGE[0], HINGE[1]], LAND, sentence=0)
c.text("quay", 0.12, 0.47, 0.022, 0, color=MUTED)
c.circle(list(HINGE), 0.01, INK, 0)
c.text("hinge", HINGE[0], HINGE[1] + 0.045, 0.02, 0, color=MUTED)


def bridge_end(dz):
    return [HINGE[0] + BR * math.cos(math.atan2(dz * k_m, BR * ASPECT)), HINGE[1] + dz * k_m]


def platform_at(dz, sentence, color, until=None, word=None, border=INK, dash=False):
    end = bridge_end(dz)
    c.line([list(HINGE), end], color, 0.008, sentence, until=until, word=word, dash=dash, layer=2)
    c.rect([end[0], end[1] - 4.0 * k_m, 0.98, end[1]], CONCRETE if not dash else None, border=border, sentence=sentence,
           until=until, word=word, border_width=0.002, dash=dash, layer=1)


for z, s, w, u in ((0.0, 0, None, None),):
    pass
c.rect([HINGE[0], 0.24, 0.98, HINGE[1] - 1.0 * k_m], WATER, sentence=0).gone(0, "rise")
platform_at(0.0, 0, INK, until=0)
c.elements[-1]["until_word"] = "rise"
c.elements[-2]["until_word"] = "rise"
pile_x = 0.9
c.rect([pile_x - 0.006, 0.24, pile_x + 0.006, 0.86], "#5D7686", sentence=0, layer=3)
c.text("pile", pile_x, 0.88, 0.02, 0, color=MUTED)
# high and low water, each drawn with its platform
c.rect([HINGE[0], 0.24, 0.98, HINGE[1] - 1.0 * k_m + swing * k_m], WATER, sentence=0, word="rise").gone(1, "scenario")
platform_at(swing, 0, ACCENT, until=1, word="rise")
for e in c.elements[-2:]:
    e["until_word"] = "scenario"
c.rect([HINGE[0], 0.24, 0.98, HINGE[1] - 1.0 * k_m - swing * k_m], WATER, sentence=1, word="scenario", layer=0)
platform_at(-swing, 1, ACCENT, word="scenario")
platform_at(swing, 1, ACCENT, word="scenario", dash=True, border=ACCENT)
c.text(f"water level range ≈ {m(ls['water_level_range_m'])} m (assumed)", 0.6, 0.8, 0.026, 1, word="meters")
c.text(f"plus loading: draft changes ≈ {m(ls['draft_swing_empty_to_full_m'])} m", 0.6, 0.75, 0.022, 2, color=MUTED, word="loading")
c.text(f"25 m bridge: slope changes ≈ {ls['25_m_bridge']['max_slope_deg_each_way']}° either way", 0.6, 0.69, 0.028, 2, color=ACCENT,
       word="degrees")
c.text("shore hinge at the middle of the range", 0.6, 0.64, 0.02, 2, color=MUTED, word="degrees")
visual("B23", "CARD", "Elevation at true slope: quay, shore hinge, a 25 m link-span to a platform on its pile; the water and "
       "the platform rise and fall, the bridge turns on its hinge; '2 m water level (assumed) + loading; about 2.8° either way'",
       [], "LOW", graphic=c.spec())

visual("B24", "SEQUENCE", "Same neighbourhood with the water ghosted: the piles fade and mooring lines to anchors on the "
       "seabed take their place; lines and anchors light (conceptual mooring, not sized)", [HOOD], "MEDIUM",
       sequence=seq("FLOAT_UNDERWATER", [view(HOOD_PLATFORMS + LINES, margin=0.06)],
                    [hide(LINES), step("GHOST", WATER_SITE, 0, seconds=0, transparency=0.85),
                     step("FADE_OUT", PILES, at(0, "piles", -0.2), seconds=1.0),
                     step("REVEAL", LINES, at(0, "mooring", -0.3), seconds=1.4, direction="FROM_ABOVE", distance=4.0),
                     glow([{"concept": "mooring_line"}], at(1, "lines", -0.3), at(1, "anchors")),
                     glow([{"concept": "anchor"}], at(1, "anchors", -0.2), at(1, end=True, offset=0.3))]),
       annotations=[note("B24_note", "Conceptual mooring — not sized", 0, word="mooring"),
                    label("B24_anchor", part("anchor", "platform2_anchor1"), "Anchor", 1, "anchors", point="TOP")])

# ======================================================================================== C6
SHORE_LINK_IDS = [f"linkspan{k}_{net}" for k in (1, 2, 3) for net in ("power", "water", "wastewater")]
visual("B25", "SEQUENCE", "Close to the quay: the buildings ghost and the city's other half appears: power, water and "
       "wastewater lines along the bridges and through the district", [DISTRICT, "utility_line"], "HIGH",
       sequence=seq("FLOAT_AERIAL", [view(NEAR_SHORE + [{"concept": "link_span"}], margin=0.08)],
                    [hide(UTILITIES),
                     step("GHOST", BUILDINGS_ALL, at(1, "fade", -0.2), seconds=1.2, transparency=0.9),
                     step("FADE_IN", UTILITIES, at(1, "half", -0.4), seconds=1.2),
                     glow(UTILITIES, at(1, "appears", -0.3), at(1, end=True, offset=0.3))]))

c = Card("B26")
c.tag("Schoonschip, Amsterdam (schematic)")
c.rect([0.06, 0.24, 0.94, 0.5], WATER, sentence=0)
c.rect([0.06, 0.24, 0.2, 0.62], LAND, sentence=0)
c.text("land", 0.13, 0.66, 0.022, 0, color=MUTED)
homes = [(0.3 + (k % 12) * 0.045, 0.31 + (k // 12) * 0.045) for k in range(46)]
for k, (x, y) in enumerate(homes):
    c.rect([x, y, x + 0.03, y + 0.03], PLASTER, border=INK, sentence=0, border_width=0.0012)
c.text("46 households", 0.57, 0.56, 0.028, 0, word="households")
c.drawn([[0.29, 0.4], [0.2, 0.4], [0.16, 0.5]], POWER, 0.008, 0, word="single", seconds=0.6)
c.circle([0.16, 0.52], 0.014, POWER, 0, word="single")
c.text("one grid connection", 0.13, 0.75, 0.024, 0, color=POWER, word="connection")
for k, (x, y) in enumerate(homes):
    c.rect([x + 0.004, y + 0.019, x + 0.026, y + 0.027], "#2E3A44", sentence=1, word="solar")
    c.elements[-1]["delay"] = round(0.01 * k, 3)
c.text("solar panels", 0.4, 0.62, 0.022, 1, color=MUTED, word="solar")
for k, (x, y) in enumerate(homes):
    c.rect([x + 0.01, y + 0.004, x + 0.02, y + 0.012], GOLD, sentence=1, word="battery")
c.text("a battery in every house", 0.6, 0.62, 0.022, 1, color=MUTED, word="battery")
for j in range(4):
    c.line([[0.3, 0.325 + j * 0.045], [0.83, 0.325 + j * 0.045]], ACCENT, 0.002, 1, word="smart", layer=0)
c.text("smart grid", 0.8, 0.62, 0.022, 1, color=ACCENT, word="smart")
c.text("Floating ≠ off-grid", 0.5, 0.8, 0.05, 2, color=ACCENT)
visual("B26", "CARD", "Schematic: 46 homes on the water, one cable to the grid on land; solar panels, a battery per house, "
       "a smart grid between them; 'Floating ≠ off-grid'", [], "LOW", graphic=c.spec())

LS2 = [part("link_span", "linkspan2")]
visual("B27", "SEQUENCE", "One bridge to the quay, close: the bridge deck ghosts, and the wastewater line beneath it, then "
       "the drinking-water line, light as they are named", [DISTRICT, "utility_line", "link_span"], "MEDIUM",
       sequence=seq("FLOAT_THREE_QUARTER",
                    [view(LS2 + [part("utility_line", [f"linkspan2_{n}" for n in ("power", "water", "wastewater")])], margin=0.25,
                          elevation=14.0)],
                    [glow([part("utility_line", ["linkspan2_wastewater"])], at(0, "black", -0.3), at(1, "connecting")),
                     step("GHOST", LS2, at(1, "infrastructure", -0.4), seconds=1.0, transparency=0.85),
                     glow([part("utility_line", ["linkspan2_wastewater"])], at(2, "wastewater", -0.2), at(2, "drinking")),
                     glow([part("utility_line", ["linkspan2_water"])], at(2, "drinking", -0.2), at(2, end=True, offset=0.3))]),
       annotations=[label("B27_waste", part("utility_line", "linkspan2_wastewater"), "Wastewater to shore", 2, "wastewater",
                          point="RIGHT"),
                    label("B27_water", part("utility_line", "linkspan2_water"), "Drinking water from shore", 2, "drinking", point="RIGHT")])

visual("B28", "SEQUENCE", "The whole district: boat landings for fire and rescue, the emergency routes to the bridges, the "
       "utility lines, then the bridges themselves light in turn", [DISTRICT, "access_route"], "HIGH",
       sequence=seq("FLOAT_AERIAL", [view(ALL_HULLS, margin=0.05)],
                    [glow([grp("walkway_connector", "landings")], at(0, "fire", -0.3), at(0, "food")),
                     glow([{"concept": "access_route"}], at(0, "medical", -0.2), at(1, "large")),
                     glow(UTILITIES, at(1, "sewage", -0.3), at(1, "roads")),
                     glow([{"concept": "link_span"}], at(1, "roads", -0.2), at(2, end=True, offset=0.4))]),
       annotations=[label("B28_landing", part("walkway_connector", "landing1"), "Boat landing", 0, "fire", until=1, point="LEFT"),
                    label("B28_route", part("access_route", "route2"), "Route to land", 0, "medical", until=2, point="TOP")])

# ======================================================================================== C7
OFF = "floating_district_offshore"
visual("B29", "SEQUENCE", "The same district alone on the open sea (counterfactual), seen from above", [OFF], "MEDIUM",
       sequence=seq("FLOAT_AERIAL", [view(ALL_HULLS + [{"concept": "breakwater"}], margin=0.05),
                                    view(ALL_HULLS, at(1), move=3.0, margin=0.05)], []),
       annotations=[note("B29_note", "Counterfactual: the same district at open sea", 0, position="TOP_RIGHT")])

BW = [part("breakwater", [f"breakwater{k:02d}"]) for k in range(13)]
d30 = duration("B30")
off_pitch = 66.0
bw_y = 25.0 + 30.0 + 8 * off_pitch + 30.0 + 60.0
visual("B30", "SEQUENCE", "Long conceptual swell passes along the breakwater (labelled); the water ghosts and the long "
       "mooring lines to deep anchors light", [OFF, "breakwater", "mooring_line"], "MEDIUM",
       motion_label=CONCEPT_MOTION_LABEL,
       sequence=seq("FLOAT_UNDERWATER", [view([{"concept": "breakwater"}, {"concept": "mooring_line"}, {"concept": "anchor"}],
                                              margin=0.06, elevation=12.0)],
                    [step("OSCILLATE", [ref], 0.3, seconds=round(d30 - 0.6, 2), amplitude_m=0.8, period_seconds=9.0,
                          phase_degrees=round(-28.0 * k, 1), tilt_degrees=1.5, axis="X",
                          pivot=[-6 * 64.0 + (k + 0.5) * 64.0 - 2.0, bw_y, 0.0], fade_seconds=1.5) for k, ref in enumerate(BW)] +
                    [step("GHOST", WATER_SITE, at(1, "below", -0.3), seconds=1.2, transparency=0.88),
                     glow([{"concept": "mooring_line"}], at(1, "mooring", -0.3), at(1, "anchors")),
                     glow([{"concept": "anchor"}], at(1, "anchors", -0.2), at(1, end=True, offset=0.3))]),
       annotations=[note("B30_label", CONCEPT_MOTION_LABEL, 0)])

visual("B31", "SEQUENCE", "From above with the water ghosted: three cables and pipes run along the seabed toward a shore "
       "beyond the frame, and light", [OFF, "utility_line"], "MEDIUM",
       sequence=seq("FLOAT_UNDERWATER", [view(ALL_HULLS + UTILITIES, margin=0.04, elevation=34.0)],
                    [step("GHOST", WATER_SITE, at(0, "cables", -0.6), seconds=1.0, transparency=0.9),
                     glow(UTILITIES, at(0, "cables", -0.2), at(1, end=True, offset=0.3))]),
       annotations=[note("B31_note", "Links to a shore beyond the frame, not sized", 0, word="cables")])

rz = RES["reference_points"]["ruzzo_energy_per_inhabitant_MWh_yr"]
food = rz["total"] - rz["excluding_food_production"]
c = Card("B32")
c.tag("An added condition: supply itself")
for k, (x, name, color) in enumerate(((0.25, "energy", POWER), (0.5, "water", DRINKING), (0.75, "food", "#6F8F4E"))):
    c.circle([x, 0.66], 0.05, color, 1, word=name)
    c.text(name, x, 0.57, 0.03, 1, word=name)
X0, X1 = 0.15, 0.85
c.rect([X0, 0.4, X1, 0.46], CONCRETE, sentence=2, word="growing")
c.rect([X0, 0.4, X0 + (X1 - X0) * food / rz["total"], 0.46], "#6F8F4E", sentence=2, word="half")
c.text(f"food production: ≈ {round(100 * food / rz['total'])}% of the estimated energy use", 0.5, 0.33, 0.026, 2, word="half")
c.text("one 2026 offshore concept study's estimate", 0.5, 0.27, 0.02, 2, color=MUTED, word="half")
c.text("Autonomy is an extra choice, not a consequence of floating", 0.5, 0.8, 0.028, 0, color=ACCENT, word="supply")
visual("B32", "CARD", "An added condition: three systems (energy, water, food) appear; a bar shows food production as "
       "nearly half of the study's estimated energy use; 'one concept study's estimate'", [], "LOW", graphic=c.spec())

BOX = [grp(c, "box") for c in ("platform_hull", "deck", "building_block", "high_roof", "facade_detail")]
SEMI = {"except": BOX}
visual("B33", "SEQUENCE", "Our box pontoon, then beside it a semi-submersible module rises into place: pontoons under the "
       "water (ghosted), columns through the surface, the deck raised above the sea (schematic of a 2026 concept study)",
       ["semi_submersible_module"], "MEDIUM",
       sequence=seq("FLOAT_UNDERWATER", [view(BOX, margin=0.2, elevation=12.0),
                                         view({"except": []}, at(1, "semi", -0.6), move=2.0, margin=0.08, elevation=12.0)],
                    [hide(SEMI),
                     step("GHOST", WATER_SITE, at(0, "different", -0.3), seconds=1.0, transparency=0.85),
                     glow([grp("platform_hull", "box")], at(0, "hull", -0.3), at(1, "semi")),
                     step("REVEAL", SEMI, at(1, "semi", -0.2), seconds=1.6, direction="FROM_BELOW", distance=8.0),
                     glow([{"concept": "column"}], at(1, "columns", -0.3), at(1, "behind")),
                     glow([part("deck", "deck")], at(1, "raised", -0.3), at(1, "columns", -0.3))]),
       annotations=[label("B33_box", part("platform_hull", "box_hull"), "Our box pontoon", 0, "hull", point="TOP"),
                    label("B33_semi", part("deck", "deck"), "Semi-submersible module", 1, "semi", point="TOP"),
                    note("B33_note", "Schematic of a 2026 concept study's module", 1, word="semi")])

visual("B34", "SEQUENCE", "Low on the hull's side: the water ghosts and the concrete below the waterline lights (no damage "
       "shown)", ["floating_platform"], "LOW",
       sequence=seq("FLOAT_UNDERWATER", [view([grp("platform_hull", "hull")], margin=0.12, elevation=8.0)],
                    [step("GHOST", WATER_SITE, at(1, "seawater", -0.4), seconds=1.0, transparency=0.85),
                     glow([grp("platform_hull", "hull")], at(1, "chlorides", -0.3), at(2, end=True, offset=0.3))]),
       annotations=[note("B34_note", "Illustrative: inspection zone, no damage shown", 1, word="chlorides")])

visual("B35", "SEQUENCE", "Below the district with the water ghosted: the platforms' shade on the seabed (illustrative)",
       [DISTRICT], "MEDIUM",
       sequence=seq("FLOAT_UNDERWATER", [view(platform_parts([x for x in CELLS if 3 <= x[0] <= 7 and 2 <= x[1] <= 6], ("hull",)),
                                              margin=0.05, elevation=24.0),
                                         view(ALL_HULLS, at(1), move=4.0, margin=0.05, elevation=30.0)],
                    [step("GHOST", WATER_SITE, at(0, "light", -0.4), seconds=1.4, transparency=0.88)]),
       annotations=[note("B35_note", "Shade illustrative; effects still need study", 0, word="study")])

c = Card("B36")
c.tag("Who gets to use the water?")
for k, (x0, title, word) in enumerate(((0.08, "Public waterfront", "who"), (0.54, "Private, fenced edge", "fencing"))):
    s = 0 if k == 0 else 2
    c.rect([x0, 0.3, x0 + 0.38, 0.42], WATER, sentence=s, word=word if k else None)
    c.rect([x0, 0.42, x0 + 0.38, 0.47], CONCRETE, sentence=s, word=word if k else None)
    c.rect([x0, 0.47, x0 + 0.38, 0.62], PLASTER, border=INK, sentence=s, word=word if k else None, border_width=0.002)
    c.text(title, x0 + 0.19, 0.72, 0.03, s, word=word if k else None)
for k in range(5):   # people walking along the public edge
    x = 0.12 + k * 0.065
    c.circle([x, 0.505], 0.0055, INK, 0)
    c.line([[x, 0.47], [x, 0.497]], INK, 0.004, 0)
for k in range(9):   # fence
    x = 0.56 + k * 0.042
    c.line([[x, 0.47], [x, 0.53]], WARN, 0.004, 2, word="fencing")
c.line([[0.56, 0.515], [0.9, 0.515]], WARN, 0.004, 2, word="fencing")
c.text("Planning law: not yet known", 0.5, 0.82, 0.03, 1, color=MUTED, word="planning")
visual("B36", "CARD", "Two waterfront edges: a public path along the water vs a private, fenced edge; 'planning law: "
       "not yet known'", [], "LOW", graphic=c.spec())

c = Card("B37")
c.tag("What would it cost?")
c.text("No reliable cost estimate for this design yet", 0.5, 0.82, 0.034, 1, word="reliable")
c.text("the one published framework: preliminary; flotation and energy only", 0.5, 0.76, 0.022, 1, color=MUTED, word="framework")
c.text("Floating gives", 0.28, 0.64, 0.034, 2, color=ACCENT, word="compared")
for k, (t_, w) in enumerate((("follows the water level", "level"), ("can be moved or reused", "moved"))):
    c.text(t_, 0.28, 0.56 - 0.06 * k, 0.026, 2, word=w)
c.text("Floating costs", 0.72, 0.64, 0.034, 3, color=WARN, word="trade")
for k, (t_, w) in enumerate((("moorings", "moorings"), ("connections", "connections"), ("ongoing maintenance", "maintenance"))):
    c.text(t_, 0.72, 0.56 - 0.06 * k, 0.026, 3, word=w)
c.line([[0.5, 0.34], [0.5, 0.66]], FAINT, 0.003, 2, dash=True, word="compared")
visual("B37", "CARD", "Two columns, no numbers: what floating gives (follows the water, movable) and what it costs "
       "(moorings, connections, maintenance); 'no reliable cost estimate for this design yet'", [], "LOW", graphic=c.spec())

# ======================================================================================== C8
visual("B38", "SEQUENCE", "From one platform to the whole district: the camera pulls back while the systems we added light "
       "in turn (walkways, moorings, breakwater, utilities)", [DISTRICT], "HIGH",
       sequence=seq("FLOAT_AERIAL", [view(platform_parts(KEEP, ("hull", "buildings")), margin=0.25),
                                    view(ALL_HULLS + [{"concept": "breakwater"}], at(0, "district", -0.3), move=2.6, margin=0.05)],
                    [glow([grp("walkway_connector", "walkways")], at(0, "every", -0.2), at(0, "added")),
                     glow([{"concept": "breakwater"}], at(0, "added", -0.2), at(0, "question")),
                     glow(UTILITIES + [{"concept": "link_span"}], at(0, "question", -0.2), at(0, end=True, offset=0.2))]))

TIERS = (("Small floating neighbourhoods, sheltered and connected", "already exist", "#4E7D4A"),
         ("A connected district for 10,000 in a sheltered bay", "possible, under the right conditions", GOLD),
         ("A city far out at sea that supplies itself", "much more speculative", WARN))


def verdict(name, upto, extra=None):
    c = Card(name)
    c.text("Could we build an entire city that floats?", 0.5, 0.85, 0.04, 0)
    for k, (what, verdict_, color) in enumerate(TIERS[:upto + 1]):
        y = 0.68 - k * 0.14
        now = k == upto
        s, word = (0, None) if not now or name == "B41" else (1 if name == "B39" else 0, None)
        c.rect([0.1, y - 0.045, 0.9, y + 0.045], "#F6F4EF" if now else BG, border=color if now else FAINT, sentence=s,
               border_width=0.004 if now else 0.002)
        c.circle([0.14, y], 0.016, color if now else FAINT, s)
        c.text(what, 0.17, y + 0.012, 0.026, s, align="LEFT", color=INK if now else MUTED)
        c.text(verdict_, 0.17, y - 0.022, 0.024, s, align="LEFT", color=color if now else MUTED)
    if extra:
        extra(c)
    return c


c = verdict("B39", 0)
visual("B39", "CARD", "Verdict, tier 1 of 3: small floating neighbourhoods, sheltered and connected: already exist", [], "LOW",
       graphic=c.spec())


def open_questions(c):
    for k, (t_, w) in enumerate((("how very large platforms bend", "bend"), ("how connections hold up", "connections"),
                                 ("what they would cost", "cost"))):
        c.text("· " + t_, 0.2, 0.36 - 0.045 * k, 0.024, 1, align="LEFT", color=MUTED, word=w)
    c.text("Open questions", 0.2, 0.41, 0.026, 1, align="LEFT", word="open")
    c.text("The one project of that size we checked: still listed as in design", 0.5, 0.2 + 0.02, 0.022, 2, plate=True,
           word="checked")


c = verdict("B40", 1, open_questions)
visual("B40", "CARD", "Verdict, tier 2 of 3: a connected district in a sheltered bay, possible under the right conditions; "
       "the open questions; 'the one project of that size we checked: still listed as in design'", [], "LOW", graphic=c.spec())
c = verdict("B41", 2)
visual("B41", "CARD", "Verdict, tier 3 of 3: a city far out at sea that supplies itself: much more speculative", [], "LOW",
       graphic=c.spec())

visual("B42", "SEQUENCE", "Closing aerial of the district (the opening view), a slow push", [DISTRICT], "HIGH",
       sequence=seq("FLOAT_AERIAL", [view(ALL_HULLS + [{"concept": "breakwater"}], margin=0.04),
                                    view(ALL_HULLS, at(1, "whether"), move=5.0, margin=0.05)], []),
       annotations=[note("B42_note", "Illustrative design", 0)])

c = Card("B43")
c.text("What should we explain next?", 0.5, 0.74, 0.056, 0)
c.polygon(icon(BUBBLE, 0.31, 0.585, 0.075), BG, border=ACCENT, sentence=1, layer=1, word="suggest", border_width=0.004)
for k in range(3):   # the three dots of a comment being written
    c.circle([0.31 + (k - 1) * 0.012, 0.6], 0.0045, ACCENT, 1, word="suggest")
    c.elements[-1].update(delay=round(0.25 + 0.15 * k, 2), layer=2)
c.text("Suggest a topic in the comments", 0.535, 0.585, 0.036, 1, color=ACCENT, word="suggest")
c.polygon(icon(CUFF, 0.37, 0.38, 0.09), BG, border=INK, sentence=2, layer=1, word="like", border_width=0.004)
c.polygon(icon(THUMB, 0.37, 0.38, 0.09), BG, border=INK, sentence=2, layer=1, word="like", border_width=0.004)
c.polygon(icon(CUFF, 0.37, 0.38, 0.09), INK, sentence=2, layer=2, word="it")
c.polygon(icon(THUMB, 0.37, 0.38, 0.09), INK, sentence=2, layer=2, word="it")
RED, GREY = "#C4302B", "#8A867C"
c.polygon(pill(0.53, 0.38, 0.17, 0.07), RED, sentence=2, layer=1, word="subscribe")
c.text("SUBSCRIBE", 0.53, 0.38, 0.03, 2, color="#FFFFFF", word="subscribe").gone(2, "subscribe")
c.elements[-1]["until_delay"] = 0.8   # pressed: the grey button and its word take over
c.polygon(pill(0.53, 0.38, 0.17, 0.07), GREY, sentence=2, layer=3, word="subscribe")
c.elements[-1]["delay"] = 0.8
c.text("SUBSCRIBED", 0.53, 0.38, 0.03, 2, color="#FFFFFF", word="subscribe").at(delay=0.8)
c.polygon(icon(BELL, 0.66, 0.385, 0.07), INK, sentence=2, layer=1, word="subscribe")
c.elements[-1]["delay"] = 1.1
c.circle([0.66, 0.385 - 0.035 + 0.006], 0.008, INK, 2, word="subscribe")
c.elements[-1]["delay"] = 1.1
visual("B43", "CARD", "Closing call to action with self-drawn icons (comment, like, subscribe, bell) as each is asked; no "
       "platform logo or trademark", [], "LOW", graphic=c.spec())

c = Card("B44")
c.text("Could We Build an Entire City That Floats?", 0.5, 0.8, 0.044, 0)
for y, line in ((0.68, "Sources are listed in the description."),
                (0.62, "Models and numbers are illustrative, not engineering designs."),
                (0.56, "Schoonschip and OCEANIX Busan are shown as schematic drawings."),
                (0.48, "Narration: AI voice (Kokoro, am_michael)")):
    c.text(line, 0.5, y, 0.026, 0, color=MUTED)
c.text("Architecture Story Studio", 0.5, 0.36, 0.032, 0)
visual("B44", "CARD", "Credits: sources in the description; models illustrative; schematic drawings; AI-voice disclosure",
       [], "LOW", graphic=c.spec())
