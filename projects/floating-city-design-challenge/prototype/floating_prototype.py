"""Concept-stage visual feasibility prototype (NOT a production asset; no engine/planner integration).

    /Applications/Blender.app/Contents/MacOS/Blender --background --factory-startup \
        --python projects/floating-city-design-challenge/prototype/floating_prototype.py -- [--shot NAME] [--res 960x540]

Writes projects/floating-city-design-challenge/renders/prototype/<shot>.png (git-ignored).
Geometry uses the numbers of analysis/results.json (Design A: 40 x 40 m box, 4 m deep, draft from the model) so that
what the stills show is the calculated waterline, not a drawn guess. Waves, motion and mooring sizes are NOT modelled.
Colours from asset_library/materials/stylized_materials.json and config/visual_style.json.
"""
import json
import math
import sys
from pathlib import Path

import bpy

PROJECT = Path(__file__).resolve().parents[1]
REPO = PROJECT.parents[1]
OUT = PROJECT / "renders" / "prototype"
RES = json.loads((PROJECT / "analysis" / "results.json").read_text())
A = RES["design_A"]["mid"]
L, B, H = A["inputs"]["L_m"], A["inputs"]["B_m"], 4.0
T = A["draft_m"]
T4 = T + RES["sensitivity"]["extra_storey"]["draft_increase_cm"] / 100.0
SLAB, WALL, BH, SPACING = 0.25, 0.25, 0.2, 10.0
DEPTH = 15.0                                  # scenario water depth within 12-25 m (DESIGN_ASSUMPTION)

C = {"bg": "#EDEBE5", "concrete": "#B8B4AA", "concrete_cut": "#8F8B83", "deck": "#9F9B92", "water": "#86A9B8",
     "water_cut": "#6E93A4", "displaced": "#4E86A8", "plaster": "#E5DCCB", "roof": "#657887", "timber": "#A8835F",
     "steel": "#5D7686", "seabed": "#C9C2A8", "line": "#2F3A40", "highlight": "#D9A441", "green": "#9DB08A"}


def rgb(hexs):
    h = hexs.lstrip("#")
    srgb = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in srgb] + [1.0]


_mats = {}


def mat(name, color, rough=0.8, alpha=1.0, emit=0.0):
    key = (name, alpha)
    if key in _mats:
        return _mats[key]
    m = bpy.data.materials.new(f"{name}_{alpha}")
    m.use_nodes = True
    bsdf = next(n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    bsdf.inputs["Base Color"].default_value = rgb(color)
    bsdf.inputs["Roughness"].default_value = rough
    if emit:
        bsdf.inputs["Emission Color"].default_value = rgb(color)
        bsdf.inputs["Emission Strength"].default_value = emit
    if alpha < 1.0:
        bsdf.inputs["Alpha"].default_value = alpha
        for attr, val in (("surface_render_method", "BLENDED"), ("blend_method", "BLEND")):
            try:
                setattr(m, attr, val)
                break
            except (AttributeError, TypeError):
                continue
    _mats[key] = m
    return m


def box(name, x0, x1, y0, y1, z0, z1, material, coll=None):
    v = [(x, y, z) for x in (x0, x1) for y in (y0, y1) for z in (z0, z1)]
    f = [(0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)]
    me = bpy.data.meshes.new(name)
    me.from_pydata(v, [], f)
    me.update()
    ob = bpy.data.objects.new(name, me)
    ob.data.materials.append(material)
    (coll or bpy.context.scene.collection).objects.link(ob)
    return ob


def cylinder(name, x, y, z0, z1, r, material, seg=24):
    v, f = [], []
    for i in range(seg):
        a = 2 * math.pi * i / seg
        v += [(x + r * math.cos(a), y + r * math.sin(a), z0), (x + r * math.cos(a), y + r * math.sin(a), z1)]
    for i in range(seg):
        j = (i + 1) % seg
        f.append((2 * i, 2 * j, 2 * j + 1, 2 * i + 1))
    f.append(tuple(2 * i for i in reversed(range(seg))))
    f.append(tuple(2 * i + 1 for i in range(seg)))
    me = bpy.data.meshes.new(name)
    me.from_pydata(v, [], f)
    me.update()
    ob = bpy.data.objects.new(name, me)
    ob.data.materials.append(material)
    bpy.context.scene.collection.objects.link(ob)
    return ob


def tube_path(name, pts, r, material):
    """A thin polyline tube (mooring line) through pts."""
    cu = bpy.data.curves.new(name, "CURVE")
    cu.dimensions = "3D"
    sp = cu.splines.new("POLY")
    sp.points.add(len(pts) - 1)
    for p, q in zip(sp.points, pts):
        p.co = (*q, 1.0)
    cu.bevel_depth = r
    ob = bpy.data.objects.new(name, cu)
    ob.data.materials.append(material)
    bpy.context.scene.collection.objects.link(ob)
    return ob


def hull(cx, cy, draft, half=False, name="hull"):
    """Concrete box pontoon (slabs, walls, 10 m bulkhead grid) floating at `draft`; half=True keeps y >= cy (section)."""
    zb, zt = -draft, H - draft
    y0 = cy if half else cy - B / 2
    y1 = cy + B / 2
    cut = mat("concrete_cut", C["concrete_cut"])
    con = mat("concrete", C["concrete"])
    deck = mat("deck", C["deck"], 0.85)
    box(f"{name}_bottom", cx - L / 2, cx + L / 2, y0, y1, zb, zb + SLAB, con)
    box(f"{name}_top", cx - L / 2, cx + L / 2, y0, y1, zt - SLAB, zt, deck)
    for sx in (-1, 1):
        x = cx + sx * (L / 2 - WALL / 2)
        box(f"{name}_wall_x{sx}", x - WALL / 2, x + WALL / 2, y0, y1, zb, zt, con)
    box(f"{name}_wall_back", cx - L / 2, cx + L / 2, y1 - WALL, y1, zb, zt, con)
    if not half:
        box(f"{name}_wall_front", cx - L / 2, cx + L / 2, y0, y0 + WALL, zb, zt, con)
    n = int(round(L / SPACING))
    for i in range(1, n):
        x = cx - L / 2 + i * SPACING
        box(f"{name}_bh_x{i}", x - BH / 2, x + BH / 2, y0, y1, zb + SLAB, zt - SLAB, cut if half else con)
        y = cy - B / 2 + i * SPACING
        if y > y0 + 0.5:   # a bulkhead on the section plane itself would hide the cut
            box(f"{name}_bh_y{i}", cx - L / 2, cx + L / 2, y - BH / 2, y + BH / 2, zb + SLAB, zt - SLAB, con)
    return zt


def buildings(cx, cy, zdeck, storeys, half=False, name="bldg"):
    """Low-rise blocks covering ~40% of the deck (3 x 2 bars), simple pitched-roof-free slabs."""
    pl, roof = mat("plaster", C["plaster"], 0.85), mat("roof", C["roof"], 0.7)
    h = 3.0 * storeys
    blocks = [(-14, -4, -15, -3), (2, 14, -15, -3), (-14, -4, 4, 15), (2, 14, 4, 15)]   # 4 blocks ~ 0.38 of deck
    for i, (x0, x1, y0, y1) in enumerate(blocks):
        if half and y1 <= 0:
            continue
        yy0 = max(y0, 0) if half else y0
        box(f"{name}_{i}", cx + x0, cx + x1, cy + yy0, cy + y1, zdeck, zdeck + h, pl)
        box(f"{name}_{i}_roof", cx + x0 - 0.2, cx + x1 + 0.2, cy + yy0 - (0 if half and y0 < 0 else 0.2), cy + y1 + 0.2,
            zdeck + h, zdeck + h + 0.35, roof)
        for s in range(1, storeys):   # floor lines
            box(f"{name}_{i}_band{s}", cx + x0 - 0.05, cx + x1 + 0.05, cy + yy0 - 0.05, cy + y1 + 0.05,
                zdeck + 3.0 * s - 0.08, zdeck + 3.0 * s + 0.08, mat("line", C["line"], 0.9))
    box(f"{name}_trees", cx - 2.5, cx + 0.5, cy + (0 if half else -12), cy + 12, zdeck, zdeck + 0.5, mat("green", C["green"], 0.9))


def water_around(x0, x1, y0, y1, holes, depth=DEPTH, alpha=1.0, name="water"):
    """Water volume (x0..x1, y0..y1, -depth..0) minus rectangular hull holes [(hx0,hx1,hy0,hy1,draft)] split in boxes."""
    w = mat("water", C["water"], 0.15, alpha)
    xs = sorted({x0, x1} | {h[0] for h in holes} | {h[1] for h in holes})
    ys = sorted({y0, y1} | {h[2] for h in holes} | {h[3] for h in holes})
    k = 0
    for i in range(len(xs) - 1):
        for j in range(len(ys) - 1):
            cxm, cym = (xs[i] + xs[i + 1]) / 2, (ys[j] + ys[j + 1]) / 2
            if not (x0 <= cxm <= x1 and y0 <= cym <= y1):
                continue
            top = 0.0
            for hx0, hx1, hy0, hy1, d in holes:
                if hx0 <= cxm <= hx1 and hy0 <= cym <= hy1:
                    top = -d
            box(f"{name}_{k}", xs[i], xs[i + 1], ys[j], ys[j + 1], -depth, top, w)
            k += 1


def seabed(x0, x1, y0, y1, depth=DEPTH):
    box("seabed", x0, x1, y0, y1, -depth - 1.5, -depth, mat("seabed", "#B7AE90", 0.95))


def _sun(name, direction, energy, angle, shadow=True):
    from mathutils import Vector
    lt = bpy.data.lights.new(name, "SUN")
    lt.energy, lt.angle, lt.use_shadow = energy, math.radians(angle), shadow
    ob = bpy.data.objects.new(name, lt)
    ob.rotation_euler = Vector(direction).normalized().to_track_quat("Z", "Y").to_euler()
    bpy.context.scene.collection.objects.link(ob)


def setup(res, ortho, az, el, target, dist=400):
    """Studio look (config/visual_style.json): key + fill suns, soft world, AgX Medium High Contrast; camera rays see a
    flat backdrop colour while the world keeps lighting at the style's strength (as engine/scene.py does)."""
    sc = bpy.context.scene
    for eng in ("BLENDER_EEVEE", "BLENDER_EEVEE_NEXT"):
        try:
            sc.render.engine = eng
            break
        except TypeError:
            continue
    sc.render.resolution_x, sc.render.resolution_y = res
    style = json.loads((REPO / "config" / "visual_style.json").read_text())
    li = style["lighting"]
    world = bpy.data.worlds.new("w")
    sc.world = world
    world.use_nodes = True
    nt = world.node_tree
    bg = next(n for n in nt.nodes if n.type == "BACKGROUND")
    bg.inputs["Color"].default_value = rgb(style["background_color"])
    bg.inputs["Strength"].default_value = li["world_strength"]
    seen = nt.nodes.new("ShaderNodeBackground")
    seen.inputs["Color"].default_value = rgb(style["background_color"])
    seen.inputs["Strength"].default_value = 1.0
    lp, mix = nt.nodes.new("ShaderNodeLightPath"), nt.nodes.new("ShaderNodeMixShader")
    out = next(n for n in nt.nodes if n.type == "OUTPUT_WORLD")
    nt.links.new(lp.outputs["Is Camera Ray"], mix.inputs[0])
    nt.links.new(bg.outputs[0], mix.inputs[1])
    nt.links.new(seen.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs["Surface"])
    cm = style.get("color_management", {})
    try:
        sc.view_settings.view_transform = cm.get("view_transform", "AgX")
        sc.view_settings.look = cm.get("look", "None")
    except TypeError:
        pass
    _sun("key", li["key_direction"], li["key_strength"], li["key_angle_degrees"])
    _sun("fill", li["fill_direction"], li["fill_strength"], 20.0, shadow=False)
    cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam"))
    cam.data.type = "ORTHO"
    cam.data.ortho_scale = ortho
    cam.data.clip_end = 5000
    a, e = math.radians(az), math.radians(el)
    cam.location = (target[0] + dist * math.cos(e) * math.cos(a), target[1] + dist * math.cos(e) * math.sin(a),
                    target[2] + dist * math.sin(e))
    d = [target[i] - cam.location[i] for i in range(3)]
    cam.rotation_euler = (math.atan2(math.hypot(d[0], d[1]), -d[2]), 0, math.atan2(d[1], d[0]) - math.pi / 2)
    sc.collection.objects.link(cam)
    sc.camera = cam


def poche(x0, x1, z0, z1, color, alpha=1.0, y=-0.02, name="poche"):
    """A thin plate on the section plane (y = 0) so cut faces read as a section (dark), the classic cutaway convention."""
    return box(name, x0, x1, y - 0.02, y, z0, z1, mat(f"poche_{color}", color, 0.9, alpha))


def shot_design_a_cutaway():
    """Section through the middle (y = 0): hull compartments, waterline, the displaced volume (L x B x draft)."""
    zt = hull(0, 0, T, half=True)
    buildings(0, 0, zt, 3, half=True)
    water_around(-70, 70, 0, 60, [(-L / 2, L / 2, 0, B / 2, T)], depth=DEPTH)
    seabed(-70, 70, 0, 60)
    dark, wcut = "#4A4642", "#5F8CA2"
    zb = -T
    poche(-L / 2, L / 2, zb, zb + SLAB, dark, name="p_bottom")
    poche(-L / 2, L / 2, zt - SLAB, zt, dark, name="p_top")
    for sx in (-1, 1):
        poche(sx * L / 2 - (WALL if sx > 0 else 0), sx * L / 2 + (0 if sx > 0 else WALL), zb, zt, dark, name=f"p_wall{sx}")
    for i in range(1, int(round(L / SPACING))):
        x = -L / 2 + i * SPACING
        poche(x - BH / 2, x + BH / 2, zb + SLAB, zt - SLAB, dark, name=f"p_bh{i}")
    poche(-70, -L / 2, -DEPTH, 0, wcut, name="p_water_l")
    poche(L / 2, 70, -DEPTH, 0, wcut, name="p_water_r")
    poche(-L / 2, L / 2, -DEPTH, zb, wcut, name="p_water_below")
    poche(-L / 2 + WALL, L / 2 - WALL, zb + SLAB, 0, C["highlight"], alpha=0.45, y=-0.05, name="displaced")   # water pushed aside
    box("waterline", -70, 70, -0.1, -0.06, -0.07, 0.07, mat("line", C["line"], 0.9))
    return dict(ortho=96, az=-90, el=7, target=(0, 8, -4))


def shot_load_compare():
    """Side elevation: the same platform with 3 and 4 storeys; drafts from the model (water is a thin band)."""
    for cx, d, st in ((-26, T, 3), (26, T4, 4)):
        zt = hull(cx, 0, d, name=f"hull{st}")
        buildings(cx, 0, zt, st, name=f"bldg{st}")
    water_around(-60, 60, -30, 30, [(-26 - L / 2, -26 + L / 2, -B / 2, B / 2, T), (26 - L / 2, 26 + L / 2, -B / 2, B / 2, T4)],
                 depth=6.0, alpha=0.6)
    box("waterline", -60, 60, -30.5, -30.4, -0.05, 0.05, mat("line", C["line"], 0.9))
    for cx, d in ((-26, T), (26, T4)):
        box(f"draftmark_{cx}", cx + L / 2 + 0.6, cx + L / 2 + 1.2, -B / 2 - 0.6, -B / 2, -d, 0, mat("highlight", C["highlight"], 0.5, 1.0, 0.4))
    return dict(ortho=112, az=-90, el=2, target=(0, 0, 3))


def neighbourhood(gap=5.0, piles=True, alpha=1.0, lines=False):
    centres = [(-(L + gap), 0), (0, 0), (L + gap, 0)]
    holes = []
    for i, (cx, cy) in enumerate(centres):
        zt = hull(cx, cy, T, name=f"hull{i}")
        buildings(cx, cy, zt, 3 if i != 1 else 2, name=f"bldg{i}")
        holes.append((cx - L / 2, cx + L / 2, cy - B / 2, cy + B / 2, T))
    zt = H - T
    tim, steel = mat("timber", C["timber"], 0.7), mat("steel", C["steel"], 0.45)
    for k in range(2):
        x0 = centres[k][0] + L / 2
        for yb in (-8, 8):
            box(f"walk{k}_{yb}", x0 - 1.0, x0 + gap + 1.0, yb - 1.5, yb + 1.5, zt + 0.05, zt + 0.3, tim)          # flexible walkway
            box(f"util{k}_{yb}", x0 - 0.5, x0 + gap + 0.5, yb - 0.4, yb + 0.4, zt - 0.9, zt - 0.6,
                mat("highlight", C["highlight"], 0.5))                                                            # utility crossing
    if piles:
        for cx, cy in centres:
            for sx, sy in ((-1, -1), (1, 1)):
                cylinder(f"pile_{cx}_{sx}", cx + sx * (L / 2 + 1.4), cy + sy * (B / 2 + 1.4), -DEPTH - 1.5, zt + 3.0, 0.6, steel)
                box(f"bracket_{cx}_{sx}", cx + sx * (L / 2) - (0 if sx > 0 else 1.0), cx + sx * (L / 2) + (1.0 if sx > 0 else 0),
                    cy + sy * (B / 2 + 1.4) - 0.9, cy + sy * (B / 2 + 1.4) + 0.9, zt - 0.6, zt - 0.1, steel)
    if lines:
        cab = mat("cable", "#1F2A30", 0.35)   # c-r1: darker than water and seabed (owner review: P5 hard to read)
        for cx, cy in centres:
            for sy in (-1, 1):
                fx, fy = cx, cy + sy * B / 2
                ax, ay = cx, cy + sy * (B / 2 + 55)
                pts = []
                for i in range(13):
                    t = i / 12
                    x, y = fx + (ax - fx) * t, fy + (ay - fy) * t
                    z = (-T + 0.5) * (1 - t) + (-DEPTH) * t - 4.0 * math.sin(math.pi * t) * (1 - t)   # sagging line (drawn, not computed)
                    pts.append((x, y, max(z, -DEPTH)))
                tube_path(f"line_{cx}_{sy}", pts, 0.45, cab)
                box(f"anchor_{cx}_{sy}", ax - 2.0, ax + 2.0, ay - 2.0, ay + 2.0, -DEPTH - 0.3, -DEPTH + 1.2, mat("anchor", "#1F2A30", 0.5))
    if alpha < 1.0:   # ghosted water: a faint volume plus a visible surface, so the platforms still read as floating
        box("water_ghost", -200, 200, -150, 150, -DEPTH, -0.05, mat("water", C["water"], 0.15, alpha))
        box("water_surface", -200, 200, -150, 150, -0.05, 0.0, mat("water_surface", "#5F8CA2", 0.1, 0.4 if lines else 0.55))
    else:
        water_around(-200, 200, -150, 150, holes, alpha=alpha)
    seabed(-200, 200, -150, 150)
    return centres


def shot_neighbourhood():
    neighbourhood(piles=True)
    return dict(ortho=150, az=-58, el=28, target=(0, 0, 0))


def shot_mooring_reveal_piles():
    neighbourhood(piles=True, alpha=0.3)
    return dict(ortho=150, az=-58, el=14, target=(0, 0, -6))


def shot_mooring_reveal_lines():
    neighbourhood(piles=False, alpha=0.15, lines=True)
    return dict(ortho=200, az=-30, el=14, target=(0, 0, -6))


def shot_load_compare_closeup():
    shot_load_compare()
    for cx, d in ((-26, T), (26, T4)):
        for k in range(0, 5):   # 1 m scale ticks on each draft mark
            box(f"tick_{cx}_{k}", cx + L / 2 + 1.2, cx + L / 2 + 1.8, -B / 2 - 0.62, -B / 2 - 0.6, -k - 0.02, -k + 0.02,
                mat("line", C["line"], 0.9))
    return dict(ortho=10, az=-90, el=2, target=(46.4, 0, -1.6))


def text(name, body, x, z, size, color, y=-B / 2 - 3.0):
    cu = bpy.data.curves.new(name, "FONT")
    cu.body, cu.size, cu.align_x = body, size, "LEFT"
    ob = bpy.data.objects.new(name, cu)
    ob.location, ob.rotation_euler = (x, y, z), (math.radians(90), 0, 0)
    ob.data.materials.append(mat(f"text_{color}", color, 0.9, 1.0, 0.6))
    ob.visible_shadow = False   # labels in front of the model must not cast shadows on it
    bpy.context.scene.collection.objects.link(ob)
    return ob


def show_between(ob, f0, f1, last):
    """Visible from frame f0 to f1 (hide_render/hide_viewport keys)."""
    for f, hidden in ((1, f0 > 1), (f0, False), (f1, True) if f1 <= last else (last, False)):
        ob.hide_render = ob.hide_viewport = hidden
        ob.keyframe_insert("hide_render", frame=f)
        ob.keyframe_insert("hide_viewport", frame=f)


def anim_add_storey_sink_fix(fps=24):
    """P6 (owner review c-r0): one continuous branch from analysis/results.json storey_branch: 3 storeys -> a 4th arrives
    -> the platform settles -> the hull grows 0.5 m -> the deck rises. Freeboards are the model's, not drawn guesses."""
    br = RES["storey_branch"]["steps"]
    f1, f2, f3 = (st["freeboard_m"] for st in br)
    con, deck = mat("concrete", C["concrete"]), mat("deck", C["deck"], 0.85)
    pl, roof, gold = mat("plaster", C["plaster"], 0.85), mat("roof", C["roof"], 0.7), mat("highlight", C["highlight"], 0.5, 1.0, 0.3)
    root = bpy.data.objects.new("platform", None)
    bpy.context.scene.collection.objects.link(root)

    def child(ob):
        ob.parent = root
        return ob
    # platform in local coordinates: deck top at z = 0, hull 4 m deep
    child(box("hull", -L / 2, L / 2, -B / 2, B / 2, -4.0, -SLAB, con))
    child(box("deck", -L / 2, L / 2, -B / 2, B / 2, -SLAB, 0.0, deck))
    blocks = [(-14, -4, -15, -3), (2, 14, -15, -3), (-14, -4, 4, 15), (2, 14, 4, 15)]
    for i, (x0, x1, y0, y1) in enumerate(blocks):
        child(box(f"b{i}", x0, x1, y0, y1, 0.0, 9.0, pl))
        r3 = child(box(f"b{i}_roof", x0 - 0.2, x1 + 0.2, y0 - 0.2, y1 + 0.2, 9.0, 9.3, roof))
        r3.name = f"b{i}_roof3"
        for k in (3.0, 6.0):
            child(box(f"b{i}_band{k}", x0 - 0.05, x1 + 0.05, y0 - 0.05, y1 + 0.05, k - 0.08, k + 0.08, mat("line", C["line"], 0.9)))
    T = lambda sec: int(round(sec * fps)) + 1   # noqa: E731
    last = T(12.0)
    for i in range(len(blocks)):   # the 3-storey roof goes when the 4th storey lands on it
        show_between(bpy.data.objects[f"b{i}_roof3"], 1, T(2.7), last)
    # the 4th storey: four blocks that land on the roofs between 1.5 s and 2.7 s
    for i, (x0, x1, y0, y1) in enumerate(blocks):
        st = child(box(f"b{i}_storey4", x0, x1, y0, y1, 9.3, 12.3, pl))
        rf = child(box(f"b{i}_storey4_roof", x0 - 0.2, x1 + 0.2, y0 - 0.2, y1 + 0.2, 12.3, 12.6, roof))
        for ob in (st, rf):
            ob.location.z = 14.0
            ob.keyframe_insert("location", frame=1)
            ob.keyframe_insert("location", frame=T(1.5))
            ob.location.z = 0.0
            ob.keyframe_insert("location", frame=T(2.7))
            show_between(ob, T(1.5), last + 1, last)
    # the extra half metre of hull grows downward between 6.5 s and 8.0 s (gold while new)
    ext = child(box("hull_extension", -L / 2, L / 2, -B / 2, B / 2, -0.5, 0.0, gold))
    ext.location.z = -4.0
    ext.scale.z = 0.001
    ext.keyframe_insert("scale", frame=1)
    ext.keyframe_insert("scale", frame=T(6.5))
    ext.scale.z = 1.0
    ext.keyframe_insert("scale", frame=T(8.0))
    # platform height = freeboard (deck top above the still water)
    for sec, fb in ((0.0, f1), (2.7, f1), (4.7, f2), (8.0, f2), (10.0, f3), (12.0, f3)):
        root.location.z = fb
        root.keyframe_insert("location", frame=T(sec))
    # freeboard gauge beside the hull: a gold bar from the water to the deck
    gauge = box("gauge", L / 2 + 0.6, L / 2 + 1.4, -B / 2 - 1.0, -B / 2 - 0.4, 0.0, 1.0, gold)
    gauge.visible_shadow = False
    for sec, fb in ((0.0, f1), (2.7, f1), (4.7, f2), (8.0, f2), (10.0, f3), (12.0, f3)):
        gauge.scale.z = fb
        gauge.keyframe_insert("scale", frame=T(sec))
    ink = C["line"]
    for name, body, a, b in (("l1", f"freeboard ≈ {f1:.2f} m", 0.0, 3.0), ("l2", f"freeboard ≈ {f2:.2f} m", 4.7, 8.5),
                             ("l3", f"freeboard ≈ {f3:.2f} m", 10.0, 12.1)):
        show_between(text(name, body, L / 2 + 1.9, 0.25, 0.75, ink), T(a), T(b), last)
    show_between(text("c1", "+1 storey (same building load)", -2.5, -3.0, 0.8, ink), T(1.5), T(6.2), last)
    show_between(text("c2", "hull +0.5 m  (+106 t concrete, +4%)", -2.5, -3.0, 0.8, ink), T(6.5), T(12.1), last)
    text("note", "Concept prototype: illustrative, still water (analysis/results.json, storey_branch)", -2.5, -4.1, 0.45, ink)
    box("waterline", -60, 60, -B / 2 - 0.3, -B / 2 - 0.2, -0.04, 0.04, mat("line", ink, 0.9))
    box("water", -60, 60, -B / 2 - 0.1, 60, -DEPTH, 0.0, mat("water", C["water"], 0.15, 0.55))
    bpy.context.scene.frame_start, bpy.context.scene.frame_end = 1, last
    return dict(ortho=32, az=-90, el=2, target=(13, 0, 4.4))


ANIMS = {"P6_add_storey_sink_fix": anim_add_storey_sink_fix}


SHOTS = {"P1_design_A_cutaway": shot_design_a_cutaway, "P2_load_compare": shot_load_compare,
         "P2b_draft_marks_closeup": shot_load_compare_closeup,
         "P3_neighbourhood": shot_neighbourhood, "P4_mooring_piles_water_ghosted": shot_mooring_reveal_piles,
         "P5_mooring_lines_water_ghosted": shot_mooring_reveal_lines}


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    if "--anim" in argv:   # an animation test: PNG frames in renders/prototype/<name>/ (ffmpeg joins them)
        name = argv[argv.index("--anim") + 1]
        res = tuple(int(v) for v in (argv[argv.index("--res") + 1] if "--res" in argv else "960x540").split("x"))
        bpy.ops.wm.read_factory_settings(use_empty=True)
        _mats.clear()
        cam = ANIMS[name]()
        setup(res, cam["ortho"], cam["az"], cam["el"], cam["target"])
        bpy.context.scene.render.fps = 24
        out = OUT / name
        out.mkdir(parents=True, exist_ok=True)
        bpy.context.scene.render.filepath = str(out / "f_")
        bpy.ops.render.render(animation=True)
        print("WROTE", out)
        return
    shots = [argv[argv.index("--shot") + 1]] if "--shot" in argv else list(SHOTS)
    res = tuple(int(v) for v in (argv[argv.index("--res") + 1] if "--res" in argv else "960x540").split("x"))
    OUT.mkdir(parents=True, exist_ok=True)
    for name in shots:
        bpy.ops.wm.read_factory_settings(use_empty=True)
        _mats.clear()
        cam = SHOTS[name]()
        setup(res, cam["ortho"], cam["az"], cam["el"], cam["target"])
        bpy.context.scene.render.filepath = str(OUT / f"{name}.png")
        bpy.ops.render.render(write_still=True)
        print("WROTE", OUT / f"{name}.png")


main()
