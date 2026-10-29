"""Beat annotations -> resolved, laid-out annotations per shot (M6; deterministic, offline).

A beat (script/visual_beats.json) lists annotations: a type, a semantic target (vocabulary
concept [+ group, + pick]), an anchor point, the sentence that introduces it and, for every
conceptual force graphic, the claim that supports it. For each annotation the planner

1. checks the evidence: the claim is source-verified, already narrated (this beat or an
   earlier one), applies to the shown bridge type and, for a compression/tension statement,
   names the target component (a truss member is never called "in tension" without one);
2. finds the beat's shots that show its state during its sentence window (a moving target
   is annotated only while it is still, e.g. the exploded hold);
3. resolves the target to component ids (planner/mapper.py) and finds the anchor on the
   target's *visible* silhouette in the shot's offline raster (planner/visibility.py: the
   engine's own geometry, layout, camera and motion plan). The anchor is stored as a world
   point (the Blender QA casts a ray through it) and as a frame position;
4. lays the shot out (engine/annotation_layout.py) away from the subtitle zone.

Problems are coverage issues of the beat (fail closed), never silently dropped arrows.
"""
import hashlib
import json
import math

from engine import annotation_layout as AL, framing, templates
from planner import mapper, timing as T, vocabulary as V, visibility as VIS

TYPES = ("COMPONENT_LABEL", "CALLOUT", "LOAD_ARROW", "REACTION_ARROW", "CONCEPTUAL_LOAD_PATH",
         "TENSION_COMPRESSION_LEGEND", "HIGHLIGHT_REGION")
POINTS = {"TOP": (0, 1), "BOTTOM": (0, -1), "CENTER": (0, 0), "LEFT": (-1, 0), "RIGHT": (1, 0),
          "TOP_LEFT": (-1, 1), "TOP_RIGHT": (1, 1), "BOTTOM_LEFT": (-1, -1), "BOTTOM_RIGHT": (1, -1)}
PICKS = ("ALL", "LEFTMOST", "RIGHTMOST", "CENTERMOST")
FORCES = ("COMPRESSION", "TENSION")
MAX_TEXT = {"COMPONENT_LABEL": 28, "CALLOUT": 36, "HIGHLIGHT_REGION": 28, "LOAD_ARROW": 16, "REACTION_ARROW": 24,
            "CONCEPTUAL_LOAD_PATH": 24}
NEEDS_TARGET = ("COMPONENT_LABEL", "CALLOUT", "LOAD_ARROW", "REACTION_ARROW", "HIGHLIGHT_REGION")
CLAIM_OK = ("SOURCE_VERIFIED", "EDITORIALLY_APPROVED", "verified")
VARIANT_TYPE = {"timber_beam": "beam", "stone_arch": "arch", "steel_truss": "truss"}


class AnnotationError(ValueError):
    pass


def style_hash(style):
    return hashlib.sha256(json.dumps(style, sort_keys=True).encode()).hexdigest()


# ---------------------------------------------------------------- static contract
def _refs(a):
    """Every target reference of an annotation (target, path anchors, along)."""
    out = []
    if a.get("target") is not None:
        out.append(a["target"])
    for branch in a.get("path") or []:
        out += [x.get("target") for x in branch]
    if a.get("along") is not None:
        out.append(a["along"])
    return out


def needs_claim(a):
    return a.get("type") in AL.FORCE_TYPES or bool(a.get("force"))


def validate_spec(doc, sources, vocab):
    """Contract errors in the beats' annotations (empty when valid)."""
    errors, seen = [], set()
    claims = {c["id"]: c for c in (sources or {}).get("claims", [])}
    narrated = set()
    for b in doc.get("beats", []):
        bid = b.get("beat_id")
        narrated |= set(b.get("claim_ids", []))
        n_sent = len(T.split_sentences(b.get("narration", "")))
        for a in b.get("annotations", []) or []:
            aid = a.get("id")
            where = f"beat {bid} annotation {aid}"
            if not aid or aid in seen:
                errors.append(f"{where}: id missing or duplicated")
            seen.add(aid)
            kind = a.get("type")
            if kind not in TYPES:
                errors.append(f"{where}: type must be one of {TYPES}")
                continue
            s = a.get("sentence", 0)
            if not isinstance(s, int) or not 0 <= s < n_sent:
                errors.append(f"{where}: sentence {s!r} is not a sentence index of the beat (0..{n_sent - 1})")
            u = a.get("until")
            if u is not None and (not isinstance(u, int) or not (isinstance(s, int) and s < u <= n_sent)):
                errors.append(f"{where}: until must be a later sentence index (or omitted for the end of the beat)")
            if kind in NEEDS_TARGET and a.get("target") is None:
                errors.append(f"{where}: {kind} needs a target (vocabulary component concept)")
            if kind == "CONCEPTUAL_LOAD_PATH" and not (a.get("path") or a.get("along")):
                errors.append(f"{where}: a load path needs path (anchor branches) or along (component chain)")
            for branch in a.get("path") or []:
                if len(branch) < 2:
                    errors.append(f"{where}: every path branch needs at least two anchors")
                for x in branch:
                    if x.get("point", "CENTER") not in POINTS:
                        errors.append(f"{where}: unknown path point {x.get('point')!r}")
            for p in a.get("points") or [a.get("point", "CENTER")]:
                if p not in POINTS:
                    errors.append(f"{where}: unknown anchor point {p!r} (one of {', '.join(POINTS)})")
            for ref in _refs(a):
                if ref is None:
                    errors.append(f"{where}: empty target")
                    continue
                name = V.concept_name(ref)
                c = vocab.get(name)
                if c is None or c["kind"] != "component":
                    errors.append(f"{where}: target '{name}' is not a component concept in config/visual_vocabulary.json")
                if isinstance(ref, dict) and ref.get("pick", "ALL") not in PICKS:
                    errors.append(f"{where}: pick must be one of {PICKS}")
            text = a.get("text")
            limit = MAX_TEXT.get(kind)
            if kind in ("COMPONENT_LABEL", "CALLOUT", "HIGHLIGHT_REGION") and not (text or "").strip():
                errors.append(f"{where}: {kind} needs text")
            if text and limit and len(text) > limit:
                errors.append(f"{where}: text longer than {limit} characters")
            if kind == "LOAD_ARROW" and a.get("direction", "DOWN") != "DOWN":
                errors.append(f"{where}: a LOAD_ARROW points DOWN (gravity load); got {a.get('direction')!r}")
            if kind == "LOAD_ARROW" and not (isinstance(a.get("count", 1), int) and 1 <= a.get("count", 1) <= 5):
                errors.append(f"{where}: count must be 1-5")
            if kind == "REACTION_ARROW" and a.get("direction", "UP") not in ("UP", "UP_INWARD"):
                errors.append(f"{where}: a REACTION_ARROW is UP or UP_INWARD; got {a.get('direction')!r}")
            if a.get("force") is not None and a["force"] not in FORCES:
                errors.append(f"{where}: force must be one of {FORCES}")
            if kind == "CONCEPTUAL_LOAD_PATH" and a.get("style", "LOAD") not in ("LOAD", "COMPRESSION"):
                errors.append(f"{where}: path style must be LOAD or COMPRESSION")
            if kind == "TENSION_COMPRESSION_LEGEND" and any(e not in FORCES for e in a.get("entries") or FORCES):
                errors.append(f"{where}: legend entries must be among {FORCES}")
            cid = a.get("claim_id")
            if needs_claim(a) and not cid:
                errors.append(f"{where}: a conceptual force graphic needs claim_id (no arrows without evidence)")
            if cid:
                claim = claims.get(cid)
                if claim is None:
                    errors.append(f"{where}: claim {cid} is not in research/sources.json")
                elif claim.get("review_status") not in CLAIM_OK:
                    errors.append(f"{where}: claim {cid} is {claim.get('review_status')}, not source-verified")
                elif not claim.get("source_ids"):
                    errors.append(f"{where}: claim {cid} has no source")
                elif cid not in narrated:
                    errors.append(f"{where}: claim {cid} is not narrated by this beat or an earlier one")
                else:
                    concept_list = claim.get("components") or []
                    force_target = a.get("along") if kind == "CONCEPTUAL_LOAD_PATH" and a.get("style") == "COMPRESSION" \
                        else (a.get("target") if a.get("force") else None)
                    if force_target is not None and V.concept_name(force_target) not in concept_list:
                        errors.append(f"{where}: claim {cid} does not state a force in "
                                      f"'{V.concept_name(force_target)}' (its components: {concept_list})")
    return errors


# ---------------------------------------------------------------- anchors
def _visible_pixels(ids, names):
    return [(i, j) for j, row in enumerate(ids) for i, v in enumerate(row) if v in names]


def _pick(comps, pixels_of, nx):
    """comps sorted deterministically; pick by the screen centroid of each one's visible pixels."""
    def cx(c):
        px = pixels_of[c]
        return sum(i for i, _ in px) / len(px) / nx
    return {"LEFTMOST": min(comps, key=lambda c: (cx(c), c)), "RIGHTMOST": max(comps, key=lambda c: (cx(c), c)),
            "CENTERMOST": min(comps, key=lambda c: (abs(cx(c) - 0.5), c))}


def _interior(pixels, depth=2):
    """Pixels at least `depth` steps inside the set (4-neighbourhood erosion), or the deepest
    non-empty erosion: an anchor never sits on a silhouette edge, where a ray could miss."""
    cur = set(pixels)
    for _ in range(depth):
        nxt = {(i, j) for i, j in cur if {(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)} <= cur}
        if not nxt:
            break
        cur = nxt
    return sorted(cur)


def _anchor(pixels, point, nx, ny):
    """Pixel of `pixels` for an anchor point: extreme in the point's direction (normalised to
    the pixels' bounding box), the tie broken towards the middle; CENTER: nearest the centroid.
    Chosen among interior pixels (2 raster steps from the silhouette edge)."""
    pixels = _interior(pixels)
    xs, ys = [i for i, _ in pixels], [j for _, j in pixels]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    hw, hh = max((x1 - x0) / 2, 0.5), max((y1 - y0) / 2, 0.5)
    dx, dy = POINTS[point]
    if (dx, dy) == (0, 0):
        mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
        return min(pixels, key=lambda p: ((p[0] - mx) ** 2 + (p[1] - my) ** 2, p))
    def score(p):
        u, v = (p[0] - cx) / hw, (p[1] - cy) / hh
        return dx * u + dy * v
    if dx == 0 or dy == 0:   # TOP/BOTTOM: the middle columns; LEFT/RIGHT: the middle rows (not a far corner)
        band = [p for p in pixels if abs((p[0] - cx) / hw if dx == 0 else (p[1] - cy) / hh) <= 0.25]
        pixels = band or pixels
    best = max(score(p) for p in pixels)
    near = [p for p in pixels if score(p) >= best - 1.5 / min(hw, hh)]
    return min(near, key=lambda p: (abs((p[0] - cx) / hw) * (dx == 0) + abs((p[1] - cy) / hh) * (dy == 0), p))


def _world(scene, i, j, depth, nx, ny):
    ux, uy = (i + 0.5) / nx, (j + 0.5) / ny
    r, u, f = scene.basis
    fit = scene.fit
    loc_f = sum(a * b for a, b in zip(fit["location"], f))
    base = framing.frame_to_world(ux, uy, fit, scene.basis, scene.aspect, toward_camera=0.0)
    return [round(base[k] + f[k] * (depth - loc_f), 5) for k in range(3)], [round(ux, 6), round(uy, 6)]


class ShotRaster:
    """Opaque-geometry raster with depth of one shot at one frame (cached)."""

    def __init__(self, scene, frame, res):
        self.scene, self.frame = scene, frame
        self.nx, self.ny = res
        self.st = VIS.state_at(scene, frame)
        self.opaque = [(n, poly) for n, (polys, op) in self.st.items() if op for poly in polys]
        self.ids, self.depth = VIS.raster(self.opaque, scene, self.nx, self.ny, with_depth=True)
        self.shown = set(self.st)
        self._ghost_rasters = {}
        self._depth_of = {}

    def pixels(self, comp_ids):
        names = {templates.object_name(templates.MAIN_SLOT, c): c for c in comp_ids}
        return {names[n]: px for n, px in self._by_name(set(names)).items()}

    def _by_name(self, names):
        """Visible pixels per object. A ghosted (see-through) target counts where it is the
        nearest surface among the opaque parts and itself: what the viewer sees through."""
        ghosted = frozenset(n for n in names if n in self.st and not self.st[n][1])
        ids, depth = self.ids, self.depth
        if ghosted:
            if ghosted not in self._ghost_rasters:
                extra = [(n, poly) for n in sorted(ghosted) for poly in self.st[n][0]]
                self._ghost_rasters[ghosted] = VIS.raster(self.opaque + extra, self.scene, self.nx, self.ny,
                                                          with_depth=True)
            ids, depth = self._ghost_rasters[ghosted]
        out = {n: [] for n in names}
        for j, row in enumerate(ids):
            for i, v in enumerate(row):
                if v in out:
                    out[v].append((i, j))
                    self._depth_of[(i, j, v)] = depth[j][i]
        return {n: px for n, px in out.items() if px}

    def depth_at(self, i, j, names=None):
        for n in names or ():
            if (i, j, n) in self._depth_of:
                return self._depth_of[(i, j, n)]
        return self.depth[j][i]

    def anchor(self, pixels, point, names=None):
        i, j = _anchor(pixels, point, self.nx, self.ny)
        world, screen = _world(self.scene, i, j, self.depth_at(i, j, names), self.nx, self.ny)
        return {"world": world, "screen": screen, "point": point}

    def box(self, pixels):
        xs, ys = [i for i, _ in pixels], [j for _, j in pixels]
        return [round(min(xs) / self.nx, 6), round(min(ys) / self.ny, 6), round((max(xs) + 1) / self.nx, 6),
                round((max(ys) + 1) / self.ny, 6)]


def _static_window(scene, comp_ids, f0, f1, min_frames):
    """Longest run of frames inside [f0, f1] in which the components do not move, or None."""
    from engine import motion
    names = [templates.object_name(templates.MAIN_SLOT, c) for c in comp_ids]
    def pos(f):
        out = []
        for n in names:
            if motion.LOC in scene.plan.channels(n):
                out.append(tuple(round(v, 5) for v in scene.plan.sample(n, motion.LOC, f)))
        return tuple(out)
    runs, start, prev = [], f0, pos(f0)
    for f in range(f0 + 1, f1 + 1):
        cur = pos(f)
        if cur != prev:
            runs.append((start, f - 1))
            start = f
            prev = cur
    runs.append((start, f1))
    best = max(runs, key=lambda r: (r[1] - r[0], -r[0]))
    return best if best[1] - best[0] + 1 >= min_frames else None


# ---------------------------------------------------------------- planning
def plan_beat(beat, beat_shots, offsets, window_seconds, model, vocab, sources, style, presets, fps, caption_top,
              match_after=()):
    """Attach resolved, laid-out annotations to the beat's plan shots (ps["annotations"]).
    beat_shots: [(plan_shot, start seconds within the beat)]; match_after: ids of shots followed by
    a match cut, whose annotations finish fading out before the cut (an invisible cut stays
    invisible). Returns (records, issues)."""
    claims = {c["id"]: c for c in sources.get("claims", [])}
    tm = style["timing"]
    records, issues = [], []
    per_shot = {id(ps): [] for ps, _ in beat_shots}
    for order, a in enumerate(beat.get("annotations", []) or []):
        aid, kind = a["id"], a["type"]
        w0 = max(0.0, offsets[a.get("sentence", 0)][0] - tm["appear_lead_seconds"])
        # ends when the next sentence's annotations start (touching windows never overlap)
        w1 = offsets[a["until"]][0] - tm["appear_lead_seconds"] if a.get("until") is not None else window_seconds
        rec = {"id": aid, "type": kind, "claim_id": a.get("claim_id"), "sentence": a.get("sentence", 0),
               "until": a.get("until"), "window": [round(w0, 3), round(w1, 3)], "shots": [], "status": None,
               "issues": []}
        records.append(rec)
        want_state = a.get("state")
        for ps, s0 in beat_shots:
            s1 = s0 + ps["timing"]["duration_seconds"]
            if ps["shot_id"] in match_after:   # nothing may pop off at a match cut
                s1 -= tm["fade_seconds"] + 1.0 / fps
            lo, hi = max(w0, s0), min(w1, s1)
            if hi - lo < tm["min_display_seconds"]:
                continue
            if ps["template"] in ("SIDE_BY_SIDE", "MOTION_GRAPHICS") or (ps["template"] == "REPLACE_PARTS"):
                rec["issues"].append(f"{ps['shot_id']}: {ps['template']} shots are not annotated (parts change or "
                                     "several models share the frame)")
                continue
            sid = ps["states"][-1]
            if want_state is not None and want_state != sid:
                continue
            per_shot[id(ps)].append((order, a, rec, lo - s0, hi - s0))
        if not any(rec is r for lst in per_shot.values() for _, _, r, _, _ in lst):
            rec["status"] = "FAILED"
            if not rec["issues"]:
                rec["issues"].append(f"no shot of the beat shows {want_state or 'the structure'} for "
                                     f"{tm['min_display_seconds']} s during sentence {a.get('sentence', 0)}")
    for ps, s0 in beat_shots:
        items = per_shot[id(ps)]
        if not items:
            continue
        shot = ps["shot"]
        scene = VIS.build_scene(shot, model.states_json(), fps, presets)
        sid = ps["states"][-1]
        parts = model.parts(sid)
        entry = model.states[sid].get("entry") or {}
        btype = VARIANT_TYPE.get(entry.get("variant"))
        rasters = {}
        resolved = []
        for order, a, rec, t0, t1 in items:
            try:
                item = _resolve(a, rec, ps, scene, parts, vocab, sid, btype, claims, rasters, style, fps, t0, t1)
            except AnnotationError as e:
                rec["issues"].append(f"{ps['shot_id']}: {e}")
                continue
            item["order"] = order
            resolved.append(item)
            rec["shots"].append(ps["shot_id"])
        reserved = []
        if caption_top and (shot.get("animation") or {}).get("label"):
            reserved.append((caption_box(scene, shot["animation"]["label"], style), "CAPTION"))
        laid, problems = AL.layout_shot(resolved, style, scene.aspect, reserved)
        problems += AL.check(laid, style, scene.aspect, caption_boxes=[b for b, _ in reserved])
        for prob in problems:
            owner = prob.split(":")[0]
            for rec in records:
                if rec["id"] in owner.split(" / "):
                    rec["issues"].append(f"{ps['shot_id']}: {prob}")
        if laid:
            ps["annotations"] = {"style_sha256": style_hash(style), "items": laid,
                                 "reserved": [{"box": b, "owner": o} for b, o in reserved]}
            shot["annotations"] = ps["annotations"]
    for rec in records:
        if rec["status"] is None:
            rec["status"] = "PLACED" if rec["shots"] and not rec["issues"] else "FAILED"
        issues += [f"ANNOTATION {rec['id']}: {i}" for i in rec["issues"]]
    return records, issues


def caption_box(scene, text, style):
    """Frame box of a sequential-comparison caption drawn at the top (narrated projects):
    centred over the shown model like engine/shot_builder.build_labels."""
    pts = [q for n, p in scene.parts.items() if n not in scene.hidden for q in VIS._verts(p)]
    xs = [x for x, _ in framing.frame_coords(pts, scene.fit, scene.basis, scene.aspect)]
    size = style["caption"]["size"]
    w = AL.text_width(text, size, style) / scene.aspect
    cx = (min(xs) + max(xs)) / 2
    top = style["safe_area"]["top"]
    return [round(cx - w / 2, 6), round(top - size * 1.2, 6), round(cx + w / 2, 6), round(top, 6)]


def _resolve(a, rec, ps, scene, parts, vocab, sid, btype, claims, rasters, style, fps, t0, t1):
    kind = a["type"]
    claim = claims.get(a.get("claim_id")) if a.get("claim_id") else None
    if claim is not None and btype and not ({"all", btype} & set(claim.get("applies_to") or ["all"])):
        raise AnnotationError(f"claim {claim['id']} applies to {claim.get('applies_to')}, not to the {btype} shown")
    res = style["anchor_raster"]

    def comps_of(ref):
        r = dict(ref) if isinstance(ref, dict) else {"concept": ref}
        pick = r.pop("pick", "ALL")
        try:
            tg = mapper.resolve_targets([r], parts, vocab, sid)
        except mapper.MappingError as e:
            raise AnnotationError(f"anchor target not found: {e}")
        if not tg:
            raise AnnotationError(f"'{V.concept_name(ref)}' is not a component concept")
        return sorted(tg[0]["component_ids"]), pick

    refs = _refs(a)
    all_ids = sorted({c for ref in refs for c in comps_of(ref)[0]})
    f0 = max(1, int(round(t0 * fps)) + 1)
    f1 = min(scene.frame_count, int(round(t1 * fps)))
    run = _static_window(scene, all_ids, f0, f1, int(math.ceil(style["timing"]["min_display_seconds"] * fps)))
    if run is None:
        raise AnnotationError(f"its targets move during the whole display window (frames {f0}-{f1}); anchors "
                              "are only attached to still parts")
    if run != (f0, f1):
        rec.setdefault("clipped", []).append({"shot": ps["shot_id"], "requested": [f0, f1], "static": list(run)})
    f0, f1 = run
    ref_frame = (f0 + f1) // 2
    key = ref_frame
    if key not in rasters:
        rasters[key] = ShotRaster(scene, ref_frame, res)
    R = rasters[key]

    def resolve_ref(ref, point, each=False):
        ids, pick = comps_of(ref)
        px = R.pixels(ids)
        missing = [c for c in ids if c not in px]
        if len(missing) == len(ids):
            raise AnnotationError(f"target {V.concept_name(ref)} is not visible in {ps['shot_id']} "
                                  f"(occluded or off-frame at frame {ref_frame})")
        visible = [c for c in ids if c in px]
        if pick != "ALL":
            visible = [_pick(visible, px, R.nx)[pick]]
        on = lambda cs: [templates.object_name(templates.MAIN_SLOT, c) for c in cs]   # noqa: E731
        if each:
            return [R.anchor(px[c], point, on([c])) | {"component_ids": [c]} for c in visible], \
                [R.box(px[c]) for c in visible]
        pixels = [p for c in visible for p in px[c]]
        return [R.anchor(pixels, point, on(visible)) | {"component_ids": visible}], [R.box(pixels)]

    item = {"id": a["id"], "type": kind, "appear": round((f0 - 1) / fps, 4), "disappear": round(f1 / fps, 4),
            "text": a.get("text"), "claim_id": a.get("claim_id"), "style": a.get("style"), "force": a.get("force"),
            "direction": a.get("direction"), "entries": a.get("entries"), "anchors": [], "target_boxes": []}
    if kind == "TENSION_COMPRESSION_LEGEND":
        return item
    if kind == "CONCEPTUAL_LOAD_PATH":
        branches = []
        if a.get("along"):
            ids, _ = comps_of(a["along"])
            px = R.pixels(ids)
            chain = sorted((c for c in ids if c in px), key=lambda c: sum(i for i, _ in px[c]) / len(px[c]))
            if len(chain) < 3:
                raise AnnotationError(f"'along' needs at least 3 visible components, found {len(chain)}")
            mid = len(chain) // 2
            nm = lambda c: [templates.object_name(templates.MAIN_SLOT, c)]   # noqa: E731
            pts = [R.anchor(px[c], "CENTER", nm(c)) | {"component_ids": [c]} for c in chain]
            ends = [R.anchor(px[chain[0]], "BOTTOM_LEFT", nm(chain[0])) | {"component_ids": [chain[0]]},
                    R.anchor(px[chain[-1]], "BOTTOM_RIGHT", nm(chain[-1])) | {"component_ids": [chain[-1]]}]
            left = pts[mid::-1] + [ends[0]]
            right = pts[mid:] + [ends[1]]
            branches = [[p["screen"] for p in left], [p["screen"] for p in right]]
            item["anchors"] = pts + ends
            item["target_boxes"] = [R.box([p for c in chain for p in px[c]])]
        else:
            for branch in a["path"]:
                screen = []
                for x in branch:
                    anc, box = resolve_ref(x["target"], x.get("point", "CENTER"))
                    item["anchors"] += anc
                    screen.append(anc[0]["screen"])
                branches.append(screen)
        item["branches"] = branches
        return item
    points = a.get("points") or [a.get("point", "TOP" if kind == "LOAD_ARROW" else "CENTER")]
    if kind == "LOAD_ARROW":
        anc, boxes = resolve_ref(a["target"], "TOP")
        ids, pick = comps_of(a["target"])
        px = R.pixels(ids)
        visible = [c for c in ids if c in px]
        if pick != "ALL":
            visible = [_pick(visible, px, R.nx)[pick]]
        pixels = [p for c in visible for p in px[c]]
        n = int(a.get("count", 1))
        xs = sorted({i for i, _ in pixels})
        spread = style["arrow"]["spread"]
        cols = [xs[0] + (xs[-1] - xs[0]) * (0.5 if n == 1 else (1 - spread) / 2 + spread * k / (n - 1)) for k in range(n)]
        anchors = []
        pixels = _interior(pixels)
        for c in cols:
            col = [p for p in pixels if abs(p[0] - c) <= 1.0]
            if not col:
                raise AnnotationError("no visible deck/target pixel under a load arrow")
            ys = sorted(j for _, j in col)
            j = ys[len(ys) // 2]
            i = min((p for p in col if p[1] == j), key=lambda p: abs(p[0] - c))[0]
            world, screen = _world(scene, i, j, R.depth_at(i, j, [templates.object_name(templates.MAIN_SLOT, c)
                                                                   for c in visible]), R.nx, R.ny)
            anchors.append({"world": world, "screen": screen, "point": "TOP", "component_ids": visible})
        item["anchors"], item["target_boxes"] = anchors, boxes
        return item
    each = a.get("leaders") == "EACH"
    for p in points:
        anc, boxes = resolve_ref(a["target"], p, each)
        item["anchors"] += anc
        item["target_boxes"] += boxes
    if kind == "REACTION_ARROW":
        box = item["target_boxes"][0]
        mid = (box[0] + box[2]) / 2
        item["inward"] = [1 if x["screen"][0] < mid else -1 for x in item["anchors"]]
    if kind == "HIGHLIGHT_REGION":
        b = item["target_boxes"]
        item["target_boxes"] = [[min(x[0] for x in b), min(x[1] for x in b), max(x[2] for x in b), max(x[3] for x in b)]]
    return item
