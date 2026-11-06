"""Level 1 visibility estimate (M5.5): pure Python, no Blender.

For one storyboard shot the offline scene is rebuilt with the engine's own rules:
- parts: M4 library components (planned meshes, exact up to bevels) or, for legacy house/roof
  variants, the engine/house_layout.py boxes (an approximate PROXY: no bevels, no seat cuts,
  ridge caps as boxes);
- the same slot layout, static visibility and locked-camera fit as engine/shot_builder.py;
- the real motion plan (engine/templates.plan_shot): positions, hiding and transparency
  are sampled at each evaluation frame.

Each frame is rasterised into a depth + component-id buffer (orthographic, one sample per
pixel centre on a coarse grid). A target's *silhouette* is every sample its own polygons
cover; it is *visible* where it is also the nearest opaque surface. Parts at >= 50 %
transparency (ghosted) do not occlude. This is an estimate at the grid resolution: values
are ESTIMATED for exact meshes with enough samples, UNCERTAIN for few samples or proxy
geometry near a threshold (Blender verification: tools/cli.py verify-visibility).
"""
import dataclasses
import math
from pathlib import Path

from engine import framing, house_layout, motion, spec, templates
from engine.arch import assets, semantic

ROOT = Path(__file__).resolve().parent.parent
VERIFICATION = ("ESTIMATED", "UNCERTAIN")


@dataclasses.dataclass
class Part:
    name: str             # object name in the shot (slot prefix for SIDE_BY_SIDE)
    id: str               # component id
    slot: str
    role: str
    polys: list           # polygons in object-local space [[(x, y, z), ...], ...]
    location: tuple
    rotation: tuple
    layer: int = 0
    hint: tuple = None
    geometry: str = "MESH"   # MESH (planned mesh) | PROXY (approximate boxes)


# ---------------------------------------------------------------- offline geometry
def _box_polys(center, dims):
    cx, cy, cz = center
    hx, hy, hz = dims[0] / 2, dims[1] / 2, dims[2] / 2
    v = [(cx + sx * hx, cy + sy * hy, cz + sz * hz) for sx in (-1, 1) for sy in (-1, 1) for sz in (-1, 1)]
    quads = [(0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)]
    return [[v[i] for i in q] for q in quads]


def _prism_polys(outline_xz, y0, y1):
    """Polygon in the XZ plane extruded along Y from y0 to y1."""
    a = [(x, y0, z) for x, z in outline_xz]
    b = [(x, y1, z) for x, z in outline_xz]
    polys = [a, list(reversed(b))]
    n = len(outline_xz)
    polys += [[a[k], a[(k + 1) % n], b[(k + 1) % n], b[k]] for k in range(n)]
    return polys


def _layout_polys(part):
    kind = part["kind"]
    if kind == "boxes":
        return [p for c, d in part["boxes"] for p in _box_polys(c, d)]
    if kind == "triangle":   # base at -rise/3, apex at 2 rise/3, solidified (thickness) about y=0
        w, r, t = part["width"], part["rise"], part["thickness"]
        return _prism_polys([(-w / 2, -r / 3), (w / 2, -r / 3), (0.0, 2 * r / 3)], -t, 0.0)
    if kind == "gable":
        return _prism_polys(part["outline"], -part["thickness"], 0.0)
    if kind == "cylinder":
        r = part["radius"]
        return _box_polys((0, 0, 0), (2 * r, part["length"], 2 * r))
    if kind == "v_ridge":
        w, h = part["width"], part["height"]
        return _prism_polys([(-w / 2, 0.0), (w / 2, 0.0), (0.0, h)], -part["length"] / 2, part["length"] / 2)
    raise ValueError(f"unknown house_layout part kind {kind}")


def _library_parts(path, owner, slot, keep=None):
    out = []
    for c in assets.plan_cached(path, owner):
        if keep is not None and c.id not in keep:
            continue
        verts = c.mesh["verts"]
        out.append(Part(name=templates.object_name(slot, c.id), id=c.id, slot=slot, role=c.role,
                        polys=[[tuple(verts[i]) for i in f] for f in c.mesh["faces"]],
                        location=tuple(c.location), rotation=tuple(c.rotation), layer=c.layer, hint=c.hint))
    return out


def slot_parts(states, slot, built):
    """Every part the engine builds for one slot: shared base + the built variants
    (mirrors engine/geometry.build_model)."""
    params = spec.base_params(states)
    roles = {p["id"]: p for p in spec.base_parts(states)}
    if params["builder"] == spec.ASSET_BUILDER:
        out = _library_parts(params["asset"], "shared", slot)
    else:
        out = [Part(name=templates.object_name(slot, p["id"]), id=p["id"], slot=slot, role=roles[p["id"]]["role"],
                    polys=_layout_polys(p), location=tuple(p["location"]), rotation=tuple(p["rotation"]),
                    geometry="PROXY") for p in house_layout.house_base_layout(params)]
    variants = spec.variant_map(states)
    for vid in built:
        v = variants[vid]
        builder = spec.variant_builder(v)
        if builder == "none":
            continue
        if builder == spec.ASSET_BUILDER:
            out += _library_parts(v["asset"], vid, slot, keep={p["id"] for p in spec.builder_parts(v)})
            continue
        declared = {p["id"]: p for p in spec.variant_parts(v)}
        for p in house_layout.gable_roof_layout(v, params):
            d = declared[p["id"]]
            out.append(Part(name=templates.object_name(slot, p["id"]), id=p["id"], slot=slot, role=d["role"],
                            polys=_layout_polys(p), location=tuple(p["location"]), rotation=tuple(p["rotation"]),
                            layer=d.get("layer", 0), hint=p.get("hint"), geometry="PROXY"))
    return out


def _to_world(p, loc, rot, offset):
    m = semantic.rotation_matrix(rot)
    return tuple(offset[i] + loc[i] + m[i][0] * p[0] + m[i][1] * p[1] + m[i][2] * p[2] for i in range(3))


def _verts(part, loc=None, rot=None, offset=(0.0, 0.0, 0.0)):
    loc, rot = loc or part.location, rot or part.rotation
    return [_to_world(p, loc, rot, offset) for poly in part.polys for p in poly]


# ---------------------------------------------------------------- shot scene
@dataclasses.dataclass
class ShotScene:
    shot: dict
    template: str
    parts: dict          # object name -> Part
    offsets: dict        # slot -> world offset
    hidden: set          # statically hidden object names
    plan: object         # motion.Plan
    fit: dict
    basis: tuple
    aspect: float
    band: float
    frame_count: int
    preset: str
    shared: set          # component ids of the shared base (site / house)


def build_scene(shot, states, fps, presets, aspect=16 / 9):
    """Offline equivalent of engine/shot_builder.build_shot (geometry, layout, camera, plan)."""
    states = spec.shot_states(states, shot)
    cfg = templates.animation_config(shot)
    template = cfg["template"]
    parts, shown, slots_parts = {}, {}, {}
    for slot_id, built, active in templates.layout_slots(shot, states):
        sp = slot_parts(states, slot_id, built)
        slots_parts[slot_id] = sp
        for p in sp:
            parts[p.name] = p
        shown[slot_id] = set(templates.visible_component_ids(states, active))
    rest = {n: _verts(p) for n, p in parts.items()}
    preset = presets[shot["camera"]]
    basis = framing.camera_basis(preset["azimuth_degrees"], preset["elevation_degrees"])
    offsets = {s: (0.0, 0.0, 0.0) for s in slots_parts}
    band = float(shot.get("camera_safe_band", 0.0))
    if template == "SIDE_BY_SIDE":
        gap = cfg.get("gap_ratio", motion.SIDE_BY_SIDE_DEFAULTS["gap_ratio"])
        if cfg.get("layout", "ROW") == "STACK":
            offs, _ = framing.layout_stack([[q for p in sp for q in rest[p.name]] for sp in slots_parts.values()],
                                           basis, gap)
        else:
            foot = []
            for sp in slots_parts.values():
                pts = [q for p in sp for q in rest[p.name]]
                foot.append((min(q[0] for q in pts), min(q[1] for q in pts), max(q[0] for q in pts),
                             max(q[1] for q in pts)))
            offs, _ = framing.layout_side_by_side(foot, basis[0], gap)
        offsets = dict(zip(slots_parts, offs))
        band = cfg.get("label_band", motion.SIDE_BY_SIDE_DEFAULTS["label_band"])
    slot_components = {}
    for slot_id, sp in slots_parts.items():
        slot_components[slot_id] = {}
        for p in sp:
            pts = rest[p.name]
            lo = [min(q[i] for q in pts) for i in range(3)]
            hi = [max(q[i] for q in pts) for i in range(3)]
            slot_components[slot_id][p.id] = motion.Component(
                name=p.name, id=p.id, location=p.location, rotation=p.rotation,
                center=tuple((a + b) / 2 for a, b in zip(lo, hi)), layer=p.layer, hint=p.hint)
    camera = None
    if template == "SEQUENCE":   # one fit per view, as engine/shot_builder.sequence_fits
        fits = []
        for v in motion.sequence_views(cfg):
            ids = set(v["focus"] or [])
            vp = [q for n, p in parts.items() if not ids or p.id in ids for q in rest[n]]
            fits.append(framing.fit_ortho(vp, basis, aspect, v["margin"] if v["margin"] is not None
                                          else preset.get("margin", 0.07), band))
        camera = {"name": templates.CAMERA_NAME, "views": fits, "start": fits[0], "end": fits[-1]}
    plan = templates.plan_shot(shot, states, fps, slot_components, camera)
    focus = set(shot.get("camera_focus") or []) if template != "SIDE_BY_SIDE" else set()
    framed = [n for n, p in parts.items() if not focus or p.id in focus]
    pts = [tuple(q[i] + offsets[parts[n].slot][i] for i in range(3)) for n in framed for q in rest[n]]
    pts += focus_envelope(plan, parts, framed) if focus else []
    fit = camera["views"][0] if camera else framing.fit_ortho(pts, basis, aspect, preset.get("margin", 0.07), band)
    hidden = {n for n, p in parts.items() if p.id not in shown[p.slot]}
    return ShotScene(shot=shot, template=template, parts=parts, offsets=offsets, hidden=hidden, plan=plan, fit=fit,
                     basis=basis, aspect=aspect, band=band, frame_count=templates.frame_count(shot, fps),
                     preset=shot["camera"], shared={p["id"] for p in spec.base_parts(states)})


def scene_at(scene, frame):
    """The scene as the camera sees it at `frame`: a SEQUENCE camera eases between views (its plan keys), every
    other template keeps one fit."""
    name = templates.CAMERA_NAME
    if scene.template != "SEQUENCE" or name not in scene.plan.tracks:
        return scene
    fit = dict(scene.fit, location=tuple(scene.plan.sample(name, motion.LOC, frame)),
               ortho_scale=scene.plan.sample(name, motion.ORTHO, frame)[0])
    return dataclasses.replace(scene, fit=fit)


def focus_envelope(plan, parts, framed):
    """Vertices of framed parts at every keyed position (close-ups of moving parts must keep
    the moved parts in frame; mirrors engine/shot_builder.focus_motion_points)."""
    pts = []
    for n in framed:
        frames = sorted({k.frame for k in plan.keys(n, motion.LOC)} | {k.frame for k in plan.keys(n, motion.ROT)})
        for f in frames:
            loc, rot = _sample(plan, n, motion.LOC, f), _sample(plan, n, motion.ROT, f)
            pts += _verts(parts[n], loc, rot)
    return pts


def _sample(plan, name, channel, frame):
    v = plan.sample(name, channel, frame) if channel in plan.channels(name) else None
    return tuple(v) if v is not None else None


def state_at(scene, frame):
    """{name: (world polygons, opaque)} of the parts shown at `frame`."""
    out = {}
    for n, p in scene.parts.items():
        if n in scene.hidden:
            continue
        hide = _sample(scene.plan, n, motion.HIDE, frame)
        if hide is not None and hide[0] >= 0.5:
            continue
        t = _sample(scene.plan, n, motion.TRANSPARENCY, frame)
        loc = _sample(scene.plan, n, motion.LOC, frame)
        rot = _sample(scene.plan, n, motion.ROT, frame)
        off = scene.offsets[p.slot]
        polys = [[_to_world(q, loc or p.location, rot or p.rotation, off) for q in poly] for poly in p.polys]
        out[n] = (polys, t is None or t[0] < 0.5)
    return out


# ---------------------------------------------------------------- raster
def raster(polys, scene, nx, ny, with_depth=False):
    """Depth/id buffer: ids[j][i] is the owner of the nearest polygon at pixel centre (i, j)
    (j = 0 is the bottom row, as in camera-view coordinates). with_depth: (ids, depth),
    depth = distance along the camera's forward axis (M6 annotation anchors)."""
    fwd = scene.basis[2]
    depth = [[math.inf] * nx for _ in range(ny)]
    ids = [[None] * nx for _ in range(ny)]
    for owner, pts in polys:
        sc = framing.frame_coords(pts, scene.fit, scene.basis, scene.aspect)
        xs = [x * nx for x, _ in sc]
        ys = [y * ny for _, y in sc]
        if max(xs) < 0 or min(xs) > nx or max(ys) < 0 or min(ys) > ny:
            continue
        d = [p[0] * fwd[0] + p[1] * fwd[1] + p[2] * fwd[2] for p in pts]
        n = len(pts)
        a = b = None
        for k in range(1, n - 1):   # depth plane in screen space from a non-degenerate triangle
            det = (xs[k] - xs[0]) * (ys[k + 1] - ys[0]) - (xs[k + 1] - xs[0]) * (ys[k] - ys[0])
            if abs(det) > 1e-9:
                a = ((d[k] - d[0]) * (ys[k + 1] - ys[0]) - (d[k + 1] - d[0]) * (ys[k] - ys[0])) / det
                b = ((xs[k] - xs[0]) * (d[k + 1] - d[0]) - (xs[k + 1] - xs[0]) * (d[k] - d[0])) / det
                break
        if a is None:
            continue   # seen edge-on: covers no pixel centre
        c0 = d[0] - a * xs[0] - b * ys[0]
        i0, i1 = max(0, int(min(xs))), min(nx - 1, int(max(xs)))
        for j in range(max(0, int(min(ys))), min(ny - 1, int(max(ys))) + 1):
            py = j + 0.5
            cross = []
            for k in range(n):   # even-odd scanline crossings (concave polygons too)
                xa, ya, xb, yb = xs[k], ys[k], xs[(k + 1) % n], ys[(k + 1) % n]
                if (ya <= py < yb) or (yb <= py < ya):
                    cross.append(xa + (py - ya) * (xb - xa) / (yb - ya))
            cross.sort()
            row_d, row_i = depth[j], ids[j]
            for m in range(0, len(cross) - 1, 2):
                for i in range(max(i0, math.ceil(cross[m] - 0.5)), min(i1, math.floor(cross[m + 1] - 0.5)) + 1):
                    z = a * (i + 0.5) + b * py + c0
                    if z < row_d[i]:
                        row_d[i], row_i[i] = z, owner
    return (ids, depth) if with_depth else ids


def _projected_outside(polys, scene):
    """Share of the targets' projected vertices outside the frame (cheap clipping check)."""
    pts = [q for _, poly in polys for q in poly]
    if not pts:
        return 0.0
    sc = framing.frame_coords(pts, scene.fit, scene.basis, scene.aspect)
    return sum(1 for x, y in sc if not (0 <= x <= 1 and 0 <= y <= 1)) / len(sc)


def measure(scene, frame, targets, cfg, ghost_extra=()):
    """Per target {id set}: silhouette, visible, occluders at one frame.

    targets: [{"concept", "component_ids"}]; ghost_extra: object names treated as
    see-through in addition to the plan (to evaluate a candidate repair)."""
    nx, ny = cfg["raster"]
    st = state_at(scene, frame)
    opaque = [(n, poly) for n, (polys, op) in st.items() if op and n not in ghost_extra for poly in polys]
    ids = raster(opaque, scene, nx, ny)
    band_rows = int(round(cfg["subtitle_safe_band"] * ny))
    out = []
    for t in targets:
        names = {templates.object_name(templates.MAIN_SLOT, i) for i in t["component_ids"]} & set(scene.parts)
        shown = [n for n in names if n in st]
        if not shown:
            out.append({"concept": t["concept"], "shown": False})
            continue
        tpolys = [(n, poly) for n in shown for poly in st[n][0]]
        sil_ids = raster(tpolys, scene, nx, ny)
        sil = vis = in_band = 0
        occ, seen = {}, {n: 0 for n in shown}
        for j in range(ny):
            for i in range(nx):
                top = ids[j][i]
                if top in seen:
                    seen[top] += 1
                if sil_ids[j][i] is None:
                    continue
                sil += 1
                if top in names:
                    vis += 1
                    in_band += j < band_rows
                else:
                    occ[top] = occ.get(top, 0) + 1
        core = 0   # visible samples whose 4 neighbours are visible target samples too (not a sliver)
        for j in range(1, ny - 1):
            for i in range(1, nx - 1):
                if ids[j][i] in names and ids[j - 1][i] in names and ids[j + 1][i] in names and \
                        ids[j][i - 1] in names and ids[j][i + 1] in names:
                    core += 1
        comps = {}
        if len(shown) > 1:   # each component alone: separation from the other targets counts
            own_core = {n: 0 for n in shown}
            for j in range(1, ny - 1):
                for i in range(1, nx - 1):
                    top = ids[j][i]
                    if top in own_core and ids[j - 1][i] == top and ids[j + 1][i] == top and \
                            ids[j][i - 1] == top and ids[j][i + 1] == top:
                        own_core[top] += 1
            for n in sorted(shown):
                own = raster([(n, poly) for poly in st[n][0]], scene, nx, ny)
                s_own = sum(1 for row in own for v in row if v is not None)
                comps[scene.parts[n].id] = {"samples": s_own, "visible_share": round(seen[n] / s_own, 4) if s_own else 0.0,
                                            "core_area": round(own_core[n] / (nx * ny), 5)}
        total = nx * ny
        out.append({
            "concept": t["concept"], "shown": True, "samples": sil,
            "projected_area": round(sil / total, 5), "visible_area": round(vis / total, 5),
            "visible_share": round(vis / sil, 4) if sil else 0.0,
            "core_area": round(core / total, 5),
            "safe_band_share": round(in_band / vis, 4) if vis else 0.0,
            "outside_share": round(_projected_outside(tpolys, scene), 4),
            "occluders": [{"id": scene.parts[n].id, "role": scene.parts[n].role, "samples": c,
                           "share": round(c / max(sil - vis, 1), 3)}
                          for n, c in sorted(((n, c) for n, c in occ.items() if n is not None),
                                             key=lambda kv: (-kv[1], kv[0]))],
            "components": comps,
            "geometry": "PROXY" if any(scene.parts[n].geometry == "PROXY" for n in shown) else "MESH",
        })
    return out


# ---------------------------------------------------------------- frames and verdicts
def evaluation_frames(scene):
    """{label: frame}: start, 25/50/75 %, end and every plan marker inside the shot."""
    n = scene.frame_count
    frames = {"start": 1, "q25": max(1, round(n * 0.25)), "mid": max(1, round(n * 0.5)),
              "q75": max(1, round(n * 0.75)), "end": n}
    for k, f in sorted(scene.plan.markers.items()):
        if 1 <= f <= n:
            frames[k] = f
    return frames


def explanatory_labels(scene):
    """Frames at which the targets must read: the glow peak (HOLD), the exploded hold
    (EXPLODED_VIEW, plus the glow when exploded parts also glow), the end of an assembly."""
    m = scene.plan.markers
    if scene.template == "EXPLODED_VIEW":
        return [k for k in ("exploded_hold",) if k in m]
    if scene.template == "HOLD":
        return ["highlight_peak"] if "highlight_peak" in m else ["mid"]
    if scene.template == "REPLACE_PARTS":
        return [k for k in ("incoming_end",) if k in m] or ["end"]
    return ["mid"]


def verdict(row, cfg, pieces=False):
    """(ok, verification, problems) for one target measurement.

    A target reads when most of it is unhidden (visible_share), or when a compact visible
    part is large enough to recognise although the rest is hidden (core_area: e.g. the front
    face of a deep keystone); a thin visible sliver (a beam edge under a deck) is neither.
    pieces=True (an exploded view of pieces read as pieces, vocabulary read_as): every
    piece must also read on its own (mostly visible, or a compact face of min_piece_core)."""
    if not row.get("shown"):
        return False, "ESTIMATED", ["NOT_SHOWN"]
    problems = []
    if row["visible_share"] < cfg["min_visible_share"] and row["core_area"] < cfg["min_core_area"]:
        problems.append("OCCLUDED")
    if row["visible_area"] < cfg["min_visible_area"]:
        problems.append("TOO_SMALL")
    if row["outside_share"] > cfg["max_outside_share"]:
        problems.append("CLIPPED")
    if row["safe_band_share"] > cfg["max_safe_band_share"]:
        problems.append("SUBTITLE_SAFE_AREA")
    if pieces and row.get("components"):   # separated pieces: each one must read on its own
        hidden = [c for c in row["components"].values()
                  if c["visible_share"] < cfg["min_piece_share"] and c["core_area"] < cfg["min_piece_core"]]
        if hidden:
            problems.append("PIECES_HIDDEN")
    near = abs(row["visible_share"] - cfg["min_visible_share"]) < cfg["uncertainty_margin"]
    verification = "ESTIMATED"
    if row["samples"] < cfg["min_samples"] or (row["geometry"] == "PROXY" and near):
        verification = "UNCERTAIN"
    return not problems, verification, problems


def targets_of(shot):
    """Targets of a storyboard shot: editorial.visibility_targets (planner) or, for hand-written
    storyboards, the highlight components."""
    ed = shot.get("editorial") or {}
    if ed.get("visibility_targets"):
        return ed["visibility_targets"]
    h = (shot.get("animation") or {}).get("highlight") or {}
    if isinstance(h.get("components"), list):
        return [{"concept": "highlight", "component_ids": h["components"], "pieces": False}]
    return []


def assess_all_frames(shot, states, fps, presets, vcfg, targets=None):
    """Level 1 rows (with verdicts) for every evaluation frame of one storyboard shot."""
    targets = targets if targets is not None else targets_of(shot)
    scene = build_scene(shot, states, fps, presets)
    frames = evaluation_frames(scene)
    rows = {}
    for label, f in frames.items():
        rows[label] = []
        for r in measure(scene, f, targets, vcfg):
            pieces = scene.template == "EXPLODED_VIEW" and any(t.get("pieces") for t in targets if t["concept"] == r["concept"])
            ok, ver, problems = verdict(r, vcfg, pieces)
            rows[label].append(dict(r, ok=ok, verification=ver, problems=problems))
    return {"frames": frames, "explanatory": explanatory_labels(scene), "rows": rows}
