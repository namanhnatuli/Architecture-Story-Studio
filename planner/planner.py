"""Narrative beats -> visual execution plan (deterministic; no model calls).

For each beat, in order: evidence gate -> asset resolution -> the intent's strategies in
preference order, each checked for preconditions (asset support, state compatibility,
semantic targets) and timing (minimum durations from the real motion planner) -> shots
with concrete template configs, camera mode/preset/focus, timing and explanations.
Beats that cannot be visualised are reported, never dropped or padded.
"""
import json
import re
from pathlib import Path

from engine import motion, spec, templates
from engine.arch import assets, semantic
from planner import PLANNER_VERSION, beats as B, camera as CAM, catalog, composition, intents, mapper, resolver
from planner import annotations, consistency, repair, timing as T, vocabulary as V
from engine import annotation_layout as AL

ROOT = Path(__file__).resolve().parent.parent
SITE_STATE = "site"


def is_site_state(sid):
    """The empty site of the bridge context ('site') or of another bridge context ('site_<context>')."""
    return sid == SITE_STATE or (isinstance(sid, str) and sid.startswith(SITE_STATE + "_"))
PARTIAL = {"EXPLAIN_STRUCTURE": {"HOLD_HIGHLIGHT"}, "EXPLAIN_DESIGN_CHANGE": {"SEQUENTIAL_STATES"},
           "COMPARE_VARIANTS": {"SEQUENTIAL_STATES"}, "SHOW_COMPONENT": {"HOLD_HIGHLIGHT"}}
REPLACE_SHARED_BASE_FAMILIES = {"roof"}   # variants are roof assemblies on one shared building


class PlanningError(ValueError):
    def __init__(self, errors):
        self.errors = list(errors)
        super().__init__("; ".join(self.errors))


class StrategyRejected(Exception):
    def __init__(self, kind, detail, capability=None):
        self.kind, self.detail, self.capability = kind, detail, capability
        super().__init__(detail)


def _rel(path, root):
    """Root-relative path when inside the repository, else absolute (temporary test projects)."""
    path, root = Path(path).resolve(), Path(root).resolve()
    return str(path.relative_to(root)) if path.is_relative_to(root) else str(path)


def load_inputs(project_dir, root=ROOT):
    p = Path(project_dir)
    path = p / "script" / "visual_beats.json"
    if not path.is_file():
        raise PlanningError([f"{path} not found (narrative beats, schemas/narrative_beats.schema.json)"])
    doc = B.load(path)
    src = p / "research" / "sources.json"
    sources = json.loads(src.read_text()) if src.is_file() else {"sources": [], "claims": []}
    cfg = json.loads((Path(root) / "config/visual_planning.json").read_text())
    return doc, sources, V.Vocabulary(Path(root) / "config/visual_vocabulary.json"), cfg


# ---------------------------------------------------------------- states
class Model:
    """Resolved states, the draft states.json and per-state semantic parts.

    M6: one *scene context* per building family (bridges on the shared river-crossing site,
    roof assemblies on the shared house); every state belongs to the context of its family.
    M8: a concept may name its own scene_context and site (long-span bridges on a wider crossing);
    each bridge context has its own site and its own empty-site state.
    A single-context project keeps the M5 states.json (schema 2); a multi-context project gets
    schema 3 ("contexts") and every shot names its scene_context."""

    def __init__(self, root, project_dir, vocab, index):
        self.root, self.project_dir, self.vocab, self.index = Path(root), Path(project_dir), vocab, index
        self.states, self.order, self.resolutions = {}, [], {}
        self.family, self.generated = None, {}
        self.contexts, self.context_of = {}, {}

    def ctx(self, family=None):
        return self.contexts.setdefault(family or self.family, {"base": None, "shared_components": [],
                                                                "shared_parts": [], "site_entry": None})

    # the primary context (single-family projects: the only one)
    base = property(lambda self: self.ctx()["base"])
    shared_parts = property(lambda self: self.ctx()["shared_parts"])
    shared_components = property(lambda self: self.ctx()["shared_components"])
    site_entry = property(lambda self: (self.contexts.get("bridge") or {}).get("site_entry"))

    def context_name(self, concept):
        """Scene context of a site/architecture concept: its own (M8) or its family's."""
        c = self.vocab.get(concept) or {}
        if c.get("scene_context"):
            return c["scene_context"]
        return "bridge" if c.get("family") == "site" else (c.get("family") or self.family)

    def site_state(self, context):
        return SITE_STATE if context in (None, "bridge") else f"{SITE_STATE}_{context}"

    @property
    def multi(self):
        return len(self.contexts) > 1

    def state_ctx(self, sid):
        return self.ctx(self.context_of.get(sid, self.family))

    def resolve(self, concept, accuracy):
        key = (concept, accuracy)
        if key not in self.resolutions:
            fam = (self.vocab.get(concept) or {}).get("family")   # the site constrains bridges only
            site = (self.contexts.get(self.context_name(concept)) or {}).get("site_entry")
            self.resolutions[key] = resolver.resolve(concept, self.vocab, self.index, accuracy,
                                                     site if fam in ("bridge", "site", None) else None)
        return self.resolutions[key]

    def set_base(self, families, sites=None):
        """families: building families in order of first appearance in the beats; sites (M8):
        {scene context: site concept} for bridge contexts (default: bridge -> river_crossing_site)."""
        families = list(dict.fromkeys(families))
        self.family = families[0] if families else None
        for fam in families:
            self.ctx(fam)
        sites = dict(sites or {})
        if "bridge" in families:
            sites = {"bridge": "river_crossing_site", **sites}
        for context, concept in sites.items():
            r = resolver.resolve(concept, self.vocab, self.index)
            if r["status"] != "REUSE_EXISTING":
                raise PlanningError([f"bridges need a site asset: {r['explanation']}"])
            c = self.ctx(context)
            c["site_entry"], c["site_concept"] = r["entry"], concept
            c["base"] = {"builder": "architecture_asset", "asset": r["entry"]["path"]}
            parts = catalog.component_parts(r["entry"], "shared")
            c["shared_parts"] = [dict(p) for p in parts]
            c["shared_components"] = sorted({p["group"] for p in parts})
            self.resolutions[(concept, "ILLUSTRATIVE")] = r

    def add_state(self, concept, resolution):
        """State id = concept name; two concepts resolving to the same asset share one state."""
        for sid, st in self.states.items():
            if st.get("asset_id") == resolution.get("asset_id"):
                return sid
        entry = resolution.get("entry")
        if resolution["status"] == "GENERATE_FROM_SUPPORTED_FAMILY":
            spec_data = resolution["generated_spec"]
            path = self.project_dir / "planning" / "generated_assets" / f"{spec_data['asset_id']}.json"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(spec_data, indent=2) + "\n")
            entry = {"asset_id": spec_data["asset_id"], "source": "library", "path": _rel(path, self.root),
                     "family": spec_data["family"], "variant": spec_data["variant"],
                     "params": assets.resolve_params(spec_data["family"], spec_data["variant"], spec_data["parameters"])[0],
                     "accuracy": "ILLUSTRATIVE", "animation_support": spec_data["animation_support"],
                     "validation": "GENERATED", "kind": "architecture"}
            self.generated[spec_data["asset_id"]] = entry["path"]
        family = self.context_name(concept)
        c = self.ctx(family)
        if c["base"] is None and entry["source"] == "legacy_states":
            c["base"] = entry["legacy_base"]
            c["shared_components"] = list(entry["legacy_shared"])
            states = {"base": c["base"], "shared_components": c["shared_components"]}
            c["shared_parts"] = [{"id": p["id"], "role": p["role"], "group": p["group"], "layer": 0, "replaceable": False}
                                 for p in spec.base_parts(states) if p["id"] in spec.shared_ids(states)]
        sid = concept
        self.context_of[sid] = family
        self.states[sid] = {"id": sid, "concept": concept, "label": self.vocab.label(concept), "entry": entry,
                            "asset_id": resolution["asset_id"], "resolution": resolution["status"]}
        self.order.append(sid)
        return sid

    def add_site_state(self, concept="river_crossing_site"):
        context = self.context_name(concept)
        sid = self.site_state(context)
        if sid not in self.states:
            self.states[sid] = {"id": sid, "concept": concept, "label": "Site", "entry": None, "asset_id": None,
                                "resolution": "SITE_ONLY"}
            self.order.insert(len([s for s in self.order if is_site_state(s)]), sid)
            self.context_of[sid] = context
        return sid

    def link_frames(self):
        """structure_from between states that differ only in the family's replaceable params."""
        lib = [s for s in self.order if self.states[s]["entry"] and self.states[s]["entry"]["source"] == "library"]
        for i, a in enumerate(lib):
            for b in lib[i + 1:]:
                ea, eb = self.states[a]["entry"], self.states[b]["entry"]
                if (ea["family"], ea["variant"]) != (eb["family"], eb["variant"]) or self.states[b].get("structure_from"):
                    continue
                free = set(assets.FAMILIES[ea["family"]][ea["variant"]].get("replaceable_params", ()))
                if free and all(ea["params"][k] == eb["params"][k] for k in ea["params"] if k not in free):
                    self.states[b]["structure_from"] = a

    def states_json(self):
        variants = []
        multi = self.multi
        for sid in self.order:
            st = self.states[sid]
            if is_site_state(sid):
                v = {"id": sid, "name": "Empty site (no structure)", "builder": "none"}
                if multi:
                    v["context"] = self.context_of.get(sid, "bridge")
                variants.append(v)
                continue
            e = st["entry"]
            if e["source"] == "library":
                v = {"id": sid, "name": st["label"], "builder": "architecture_asset", "asset": e["path"]}
            else:
                v = {k: val for k, val in e["legacy_variant"].items() if k not in ("components",)}
                v.update(id=sid, name=st["label"])
            if st.get("structure_from"):
                v["structure_from"] = st["structure_from"]
            if multi:
                v["context"] = self.context_of.get(sid, self.family)
            variants.append(v)
        if multi:   # M6: one base per scene context (engine/spec.context_view)
            contexts = {f: {"building_type": "bridge" if c.get("site_concept") else f, "base": c["base"],
                            "shared_components": c["shared_components"]}
                        for f, c in self.contexts.items()}
            return {"schema_version": 3, "generated_by": "planner", "planner_version": PLANNER_VERSION,
                    "building_type": "mixed", "contexts": contexts, "base": self.base,
                    "shared_components": self.shared_components, "variants": variants, "transitions": []}
        return {"schema_version": 2, "generated_by": "planner", "planner_version": PLANNER_VERSION,
                "building_type": self.family, "base": self.base, "shared_components": self.shared_components,
                "variants": variants, "transitions": []}

    def parts(self, sid):
        """Visible semantic parts of a state: shared base + own + inherited frame."""
        st = self.states[sid]
        shared = self.state_ctx(sid)["shared_parts"]
        if is_site_state(sid):
            return list(shared)
        own = catalog.component_parts(st["entry"], sid)
        src = st.get("structure_from")
        if src:
            inherited = [p for p in catalog.component_parts(self.states[src]["entry"], src) if not p["replaceable"]]
            own = [p for p in own if p["replaceable"]] + inherited
        return list(shared) + own

    def pull_out(self, sid, ids, per, preset):
        """Exploded close-up of pieces set in a wall (voussoirs in a spandrel): each piece first
        leaves along its depth axis (its largest extent) towards the camera by that depth +
        0.3 m, plus its preset spread, so it never moves into the parts that stay."""
        from engine import framing
        fwd = framing.camera_basis(preset["azimuth_degrees"], preset["elevation_degrees"])[2]
        comps = {c.id: c for c in assets.plan_cached(self.states[sid]["entry"]["path"], sid)}
        out = {}
        for i in ids:
            lo, hi = semantic.bbox(comps[i])
            ext = [hi[k] - lo[k] for k in range(3)]
            axis = max(range(3), key=lambda k: ext[k])
            pull = [0.0, 0.0, 0.0]
            pull[axis] = (ext[axis] + 0.3) * (1.0 if -fwd[axis] > 0 else -1.0)
            d, dist = per[i]["direction"], per[i]["distance"]
            v = [pull[k] + d[k] * dist for k in range(3)]
            n = sum(c * c for c in v) ** 0.5
            out[i] = {"direction": [round(c / n, 5) for c in v], "distance": round(n, 4)}
        return out

    def explode_components(self, sid):
        """(ids, per_component) for an exploded view of `sid` (generator presets; legacy: hints)."""
        st = self.states[sid]
        entry = st["entry"]
        visible = {p["id"] for p in self.parts(sid)}
        if entry["source"] != "library":   # legacy roofs: the M2 explode rule (gable walls stay)
            own = [p for p in catalog.component_parts(entry, sid) if p["role"] in catalog.LEGACY_EXPLODE]
            return [p["id"] for p in own], {p["id"]: {"distance": catalog.LEGACY_EXPLODE[p["role"]]} for p in own}
        per = {}
        for owner in [sid] + ([st["structure_from"]] if st.get("structure_from") else []):
            per.update(assets.explode_per_component(self.states[owner]["entry"]["path"], owner))
        per = {k: v for k, v in per.items() if k in visible}
        return sorted(per), per


# ---------------------------------------------------------------- shot builders
def _pulse(ids, seconds, m, start=None):
    start = m["start"] if start is None else start
    hold = seconds - start - m["rise"] - m["fall"] - m["tail"]
    if hold < 0.3:
        raise T.TooShort("highlight")
    return {"components": ids, "start_seconds": round(start, 4), "rise_seconds": m["rise"], "hold_seconds": round(hold, 4),
            "fall_seconds": m["fall"], "strength": m["strength"]}


def _shot(template, states_kw, animation, n, fps, camera, focus=None, band=0.0):
    shot = {"id": "PLAN", "duration_seconds": n / fps, "visual_type": "BLENDER_3D", "transition": template,
            "camera": camera, "animation": animation, **states_kw}
    if focus:
        shot["camera_focus"] = focus
    if band and template != "SIDE_BY_SIDE":
        shot["camera_safe_band"] = band
    return shot


class Draft:
    """One planned shot before allocation: make(n_frames) -> storyboard shot."""

    def __init__(self, template, mode, make, weight, states, targets, explanation, focus=None):
        self.template, self.mode, self.make, self.weight = template, mode, make, weight
        self.states, self.targets, self.explanation, self.focus = states, targets, explanation, focus
        self.extend_hold = None   # REPLACE: rebuild with a longer pre-swap hold once frames are allocated
        self.composition = None   # comparison layout decision (planner/composition.py)
        self.sequence = None      # shots of one sequential comparison share a locked camera


def _with_context(d, context):
    """M6: every shot a draft makes names its scene context (the base the engine builds on)."""
    def wrap(make):
        def made(n):
            shot = make(n)
            shot["scene_context"] = context
            return shot
        return made
    d.make = wrap(d.make)
    if d.extend_hold is not None:
        ext = d.extend_hold
        d.extend_hold = lambda extra, ext=ext: wrap(ext(extra))


def build_strategy(name, ctx):
    """Drafts for a strategy, or StrategyRejected(kind, detail[, capability])."""
    m, fps, model, beat = ctx["cfg"]["motion"], ctx["fps"], ctx["model"], ctx["beat"]
    camera_of = ctx["camera_of"]
    band = ctx["cfg"]["camera"]["subtitle_safe_band"]
    arch = ctx["arch_states"]
    w = ctx["cfg"]["composite_weights"]

    def need_states(k):
        if len(arch) < k:
            raise StrategyRejected("INVALID_REQUEST", f"{name} needs {k} architecture state(s); beat names {arch}")
        if k > 1 and name != "SEQUENTIAL_STATES" and model.multi and \
                len({model.context_of.get(s) for s in arch}) > 1:   # M6: one frame / one camera = one context
            raise StrategyRejected("INVALID_REQUEST", f"{name}: {arch} belong to different scene contexts "
                                   f"({', '.join(sorted({model.context_of.get(s) for s in arch}))}); they cannot share "
                                   "one frame or one locked camera (shown one after the other: SEQUENTIAL_STATES)")

    def support(sid, template):
        st = model.states[sid]
        if not is_site_state(sid) and template not in st["entry"]["animation_support"] and template != "HOLD":
            raise StrategyRejected("MISSING_TEMPLATE", f"asset {st['asset_id']} does not support {template}")

    def targets_in(sid):
        try:
            return mapper.resolve_targets(ctx["component_refs"], model.parts(sid), model.vocab, sid)
        except mapper.MappingError as e:
            raise StrategyRejected("INVALID_REQUEST", str(e))

    def ids_of(tg):
        return sorted({i for t in tg for i in t["component_ids"]})

    def hold(sid, tg, mode, focus=None, label=None, glow=None, shot_band=None, glow_start=None, move=None):
        ids = ids_of(tg) if glow is None else glow

        def make(n):
            anim = {"template": "HOLD", "state": sid}
            if move:   # M7: slow push-in (no anchored annotations on this shot)
                anim["camera_move"] = dict(move)
            if ids:
                support(sid, "HIGHLIGHT")
                anim["highlight"] = _pulse(ids, n / fps, m["highlight"], glow_start)
            elif n / fps < ctx["cfg"]["timing"]["min_shot_seconds"]:
                raise T.TooShort("hold")
            if label:
                anim["label"] = label
                if ctx["caption_top"]:   # M6 narrated: captions at the top, the bottom is the subtitle zone
                    anim["label_position"] = "TOP"
            return _shot("HOLD", {"from_state": sid, "to_state": sid}, anim, n, fps, camera_of(mode, sid), focus,
                         band if shot_band is None else shot_band)
        return make

    if name == "SITE_HOLD":
        if not ctx["site_concept"]:
            raise StrategyRejected("MISSING_TEMPLATE", "no site concept in the beat", "MAP_OR_IMAGERY")
        site_sid = model.add_site_state(ctx["site_concept"])
        return [Draft("HOLD", "FULL_OBJECT", hold(site_sid, [], "FULL_OBJECT"), w["HOLD"], [site_sid], [],
                      "the empty shared site: the gap any of the structures must span")]

    if name == "CARD":
        g = beat.get("graphic")
        if not g:
            cap = "FORCE_DIAGRAM" if beat["narrative_intent"] == "EXPLAIN_CAUSE_EFFECT" else "MAP_OR_IMAGERY"
            raise StrategyRejected("MISSING_TEMPLATE", intents.MISSING_CAPABILITIES[cap][0], cap)

        spans = ctx["sentence_offsets"] or []
        lead = ctx["annotation_lead"]
        graphic = {k: v for k, v in g.items() if k != "elements"}
        graphic["elements"] = []
        words = ctx.get("word_offsets") or []
        for e in g["elements"]:   # M7: element timing by sentence (measured when AUDIO_LOCKED), or by word
            e = dict(e)
            word = e.pop("word", None)
            for key, field in (("sentence", "appear"), ("until", "disappear")):
                if key in e:
                    k = e.pop(key)
                    if not isinstance(k, int) or not 0 <= k < len(spans):
                        raise StrategyRejected("INVALID_REQUEST", f"card element {e.get('id')}: {key} {k!r} is not a "
                                               f"sentence of the beat (0..{len(spans) - 1})")
                    t = spans[k][0]
                    if key == "sentence" and word:   # the aligned moment the word is spoken
                        hits = [x for x in (words[k] if k < len(words) else []) if x[0] == T.norm_word(word)]
                        if not hits:
                            raise StrategyRejected("INVALID_REQUEST", f"card element {e.get('id')}: word {word!r} "
                                                   f"has no aligned timestamp in sentence {k} (run align)")
                        t = hits[0][1]
                    e[field] = round(max(0.0, t - lead), 4)
            graphic["elements"].append(e)

        def make(n):
            return {"id": "PLAN", "duration_seconds": n / fps, "visual_type": "MOTION_GRAPHICS", "transition": "CARD",
                    "camera": "CARD", "graphic": graphic, "from_state": None, "to_state": None}
        return [Draft("MOTION_GRAPHICS", "CARD", make, 1.0, [], [], "2D card supplied by the beat"
                      + (f" ({len(graphic['elements'])} elements)" if graphic["elements"] else ""))]

    if name in ("HOLD", "HOLD_HIGHLIGHT"):
        need_states(1)
        sid = arch[0]
        tg = targets_in(sid) if name == "HOLD_HIGHLIGHT" else []
        if name == "HOLD_HIGHLIGHT" and not tg:
            raise StrategyRejected("INVALID_REQUEST", "HOLD_HIGHLIGHT needs component concepts to highlight")
        mode = beat.get("camera_mode", "FULL_OBJECT")
        k = beat.get("highlight_at_sentence")
        glow_start = None
        if tg and k is not None:   # M6: the glow starts when its sentence does
            spans = ctx["sentence_offsets"] or []
            if not 0 <= k < len(spans):
                raise StrategyRejected("INVALID_REQUEST", f"highlight_at_sentence {k} is not a sentence of the beat")
            glow_start = max(m["highlight"]["start"], spans[k][0] - 0.2)
        move = beat.get("camera_move")
        # The framing: only the highlighted parts (close_on_targets), or named parts (close_on), so that two
        # beats lighting different parts can share one locked view. The Draft carries it: the cut type compares it.
        focus = None
        if beat.get("close_on"):
            try:
                focus = ids_of(mapper.resolve_targets(beat["close_on"], model.parts(sid), model.vocab, sid))
            except mapper.MappingError as e:
                raise StrategyRejected("INVALID_REQUEST", f"close_on: {e}")
        elif beat.get("close_on_targets") and tg:
            focus = ids_of(tg)
        glow = None
        if beat.get("glow_only"):   # the beat is about all its targets, but only these light up
            try:
                glow = ids_of(mapper.resolve_targets(beat["glow_only"], model.parts(sid), model.vocab, sid))
            except mapper.MappingError as e:
                raise StrategyRejected("INVALID_REQUEST", f"glow_only: {e}")
        return [Draft("HOLD", mode, hold(sid, tg, mode, focus=focus, glow=glow, glow_start=glow_start, move=move), w["HOLD"], [sid], tg,
                      f"hold {sid}" + (f", glowing {', '.join(t['concept'] for t in tg)}" if tg else "")
                      + (f" from sentence {k}" if glow_start is not None else "")
                      + (f"; slow push-in ({move.get('amount', 0.1):.0%})" if move else ""), focus=focus)]

    if name == "ASSEMBLE_IN":
        need_states(1)
        sid = arch[0]
        site_sid = model.site_state(model.context_of.get(sid))
        if ctx["prev_end_state"] != site_sid:
            raise StrategyRejected("INVALID_REQUEST", "ASSEMBLE_IN needs the previous shot to end on the empty site")
        tg = targets_in(sid)

        def make_in(n):
            anim = {"template": "REPLACE_PARTS", "from_state": site_sid, "to_state": sid, "easing": "SMOOTH",
                    "hold_start_seconds": m["assemble"]["min_hold_start"], "hold_end_seconds": m["assemble"]["min_hold_end"],
                    "incoming": {"direction": "FROM_ABOVE", "distance": 2.5, "move_seconds": m["assemble"]["move_in"],
                                 "stagger_seconds": m["assemble"]["stagger"], "fade": True, "fade_end": 0.7,
                                 "overlap_seconds": 0.0, "easing": "EASE_OUT"}}
            return _shot("REPLACE_PARTS", {"from_state": site_sid, "to_state": sid}, anim, n, fps,
                         camera_of("LOCKED_TRANSFORMATION"), None, band)
        drafts = [Draft("REPLACE_PARTS", "LOCKED_TRANSFORMATION", make_in, w["REPLACE_PARTS"], [site_sid, sid], [],
                        f"{sid} assembles into the shown empty site (its parts drop in by assembly layer)")]
        if tg:
            drafts.append(Draft("HOLD", "FULL_OBJECT", hold(sid, tg, "FULL_OBJECT"), w["HOLD"], [sid], tg,
                                f"then {', '.join(t['concept'] for t in tg)} glow"))
        return drafts

    def focus_targets(sid):
        focus_refs = beat.get("focus_concepts") or ctx["component_refs"]
        try:
            tg = mapper.resolve_targets(focus_refs, model.parts(sid), model.vocab, sid)
        except mapper.MappingError as e:
            raise StrategyRejected("INVALID_REQUEST", str(e))
        if not tg:
            raise StrategyRejected("INVALID_REQUEST", "a close-up needs component concepts to frame")
        return tg

    def exploded(sid, ids, per, hl, tg, mode, focus=None):
        """EXPLODED_VIEW draft of `ids` (layer-staggered disassembly and return)."""
        parts = {p["id"]: p for p in model.parts(sid)}
        layers = len({parts[i]["layer"] for i in ids})
        e = m["exploded"]

        def make_ex(n):
            motion_s = e["hold_start"] + e["explode"] + e["return"] + e["hold_end"] + 2 * (layers - 1) * e["stagger"]
            held = n / fps - motion_s - 2.0 / fps      # two frames of slack for the engine's frame rounding
            if held < e["min_hold"]:
                raise T.TooShort("exploded")
            anim = {"template": "EXPLODED_VIEW", "state": sid, "components": ids, "per_component": per,
                    "sequence": "SEQUENTIAL", "stagger_by": "LAYER", "order": "DISASSEMBLY",
                    "stagger_seconds": e["stagger"], "hold_start_seconds": e["hold_start"],
                    "explode_seconds": e["explode"], "hold_seconds": round(held, 4), "return_seconds": e["return"],
                    "hold_end_seconds": e["hold_end"]}
            if hl:
                anim["highlight"] = {"components": hl, "mode": "SIMULTANEOUS", "strength": 0.5, "fade_seconds": 0.25}
            return _shot("EXPLODED_VIEW", {"from_state": sid, "to_state": sid}, anim, n, fps, camera_of(mode), focus, band)
        return Draft("EXPLODED_VIEW", mode, make_ex, w["EXPLODED_VIEW"], [sid], tg,
                     f"take {sid} apart by assembly layer ({len(ids)} components, {layers} layers) and back"
                     + (f"; {len(hl)} focus components glow" if hl else ""), focus=focus)

    if name == "CLOSEUP_HIGHLIGHT":
        need_states(1)
        sid = arch[0]
        wide = targets_in(sid)
        tg = focus_targets(sid)
        focus = ids_of(tg)
        return [Draft("HOLD", "FULL_OBJECT", hold(sid, wide, "FULL_OBJECT"), w["HOLD"], [sid], wide,
                      f"establish {sid} with {', '.join(t['concept'] for t in wide)} glowing"),
                Draft("HOLD", "COMPONENT_CLOSEUP", hold(sid, tg, "COMPONENT_CLOSEUP", focus), w["HOLD"], [sid], tg,
                      f"close-up framed on {len(focus)} component(s)", focus=focus)]

    if name == "CLOSEUP_EXPLODE":
        need_states(1)
        sid = arch[0]
        tg = focus_targets(sid)
        pieces = [t["concept"] for t in tg if (model.vocab.get(t["concept"]) or {}).get("read_as") == "pieces"]
        if not pieces:
            raise StrategyRejected("INVALID_REQUEST", "no focus concept is read as separate pieces "
                                   "(vocabulary read_as); a glowing close-up is enough")
        support(sid, "EXPLODED_VIEW")
        ids, per = model.explode_components(sid)
        focus = ids_of(tg)
        missing = sorted(set(focus) - set(ids))
        if missing:
            raise StrategyRejected("MISSING_TEMPLATE", f"{len(missing)} focus component(s) have no explode preset "
                                   f"(e.g. {missing[0]})")
        wide = targets_in(sid)
        # Frontal close-up: the pieces' shape lies in the face, and the pull out of the face is
        # then pure depth (invisible in orthographic view) - only the spread shows on screen.
        ex = exploded(sid, focus, model.pull_out(sid, focus, per, ctx["presets"][camera_of("SIDE_ELEVATION")]),
                      focus, tg, "SIDE_ELEVATION", focus)
        ex.explanation = (f"frontal close-up: only the {len(focus)} focus pieces ({', '.join(t['concept'] for t in tg)}) "
                          f"come forward out of the face, spread apart and return, so each piece's shape reads "
                          f"({', '.join(pieces)} are read as pieces)")
        return [Draft("HOLD", "FULL_OBJECT", hold(sid, wide, "FULL_OBJECT"), w["HOLD"], [sid], wide,
                      f"establish {sid} with {', '.join(t['concept'] for t in wide)} glowing"), ex]

    if name in ("EXPLODE", "HIGHLIGHT_THEN_EXPLODE"):
        need_states(1)
        sid = arch[0]
        support(sid, "EXPLODED_VIEW")
        ids, per = model.explode_components(sid)
        if not ids:
            raise StrategyRejected("MISSING_TEMPLATE", f"{sid} has no explodable components")
        tg = targets_in(sid)
        hl = sorted(set(ids_of(tg)) & set(ids))
        ex = exploded(sid, ids, per, hl, tg, "LOCKED_TRANSFORMATION")
        if name == "EXPLODE":
            return [ex]
        if not tg:
            raise StrategyRejected("INVALID_REQUEST", "HIGHLIGHT_THEN_EXPLODE needs component concepts")
        return [Draft("HOLD", "FULL_OBJECT", hold(sid, tg, "FULL_OBJECT"), w["HOLD"], [sid], tg,
                      f"glow {', '.join(t['concept'] for t in tg)}"), ex]

    if name in ("REPLACE", "HIGHLIGHT_REPLACE_HIGHLIGHT", "SEQUENTIAL_STATES"):
        need_states(2)
        a, b = arch[0], arch[1]
        if name != "SEQUENTIAL_STATES":
            ok, why = compatible(model, a, b)
            if not ok:
                raise StrategyRejected("INVALID_REQUEST", f"REPLACE_PARTS {a} -> {b} is not possible: {why}")
            support(b, "REPLACE_PARTS")
        out_ids, in_ids = templates.replace_sets(ctx["draft_states"], a, b) if name != "SEQUENTIAL_STATES" else ([], [])
        per_state = beat.get("state_targets") or {}   # two different structures can light different parts

        def targets_of(sid):
            if sid in per_state:
                return mapper.resolve_targets(per_state[sid], model.parts(sid), model.vocab, sid)
            return targets_in(sid) if ctx["component_refs"] else []
        tga, tgb = targets_of(a), targets_of(b)
        if name == "SEQUENTIAL_STATES":
            same = beat.get("same_scale")   # one locked camera for both, captioned, so their sizes compare honestly
            drafts = [Draft("HOLD", "FULL_OBJECT", hold(s_, t_, "FULL_OBJECT", label=model.states[s_]["label"] if same else None),
                            w["HOLD"], [s_], t_, why) for s_, t_, why in (
                                (a, tga, f"show {a}"), (b, tgb, f"cut to {b} (not swap-compatible with {a}, shown separately)"))]
            if same:
                for d in drafts:
                    d.sequence = f"SEQ_{beat['beat_id']}"
                    d.composition = {"layout": "SEQUENTIAL_COMPARISON", "purpose": beat["narrative_intent"], "scale": "COMMON",
                                     "sequence": [a, b], "metrics": {}}
            return drafts
        r = m["replace"]

        def make_rep(extra_start):
            def make(n):
                anim = {"template": "REPLACE_PARTS", "from_state": a, "to_state": b, "easing": "SMOOTH",
                        "hold_start_seconds": round(r["min_hold_start"] + extra_start(n), 4),
                        "hold_end_seconds": r["min_hold_end"],
                        "outgoing": {"direction": "OUTWARD_UP", "distance": 2.6, "lift": 0.3, "lift_seconds": 0.3,
                                     "move_seconds": r["move_out"], "stagger_seconds": r["stagger"], "fade": True,
                                     "fade_start": 0.0},
                        "incoming": {"direction": "FROM_ABOVE", "distance": 2.2, "move_seconds": r["move_in"],
                                     "stagger_seconds": r["stagger"], "fade": True, "fade_end": 0.75,
                                     "overlap_seconds": 0.3, "easing": "EASE_OUT"}}
                return _shot("REPLACE_PARTS", {"from_state": a, "to_state": b}, anim, n, fps,
                             camera_of("LOCKED_TRANSFORMATION"), None, band)
            return make
        rep = Draft("REPLACE_PARTS", "LOCKED_TRANSFORMATION", make_rep(lambda n: 0.0), w["REPLACE_PARTS"], [a, b], [],
                    f"swap {len(out_ids)} parts of {a} for {len(in_ids)} parts of {b} on the shared "
                    f"{'frame' if model.states[b].get('structure_from') == a else 'base'}")
        rep.extend_hold = make_rep
        if name == "REPLACE":
            return [rep]
        ha = tga or [{"concept": "changing parts", "roles": [], "group": None, "component_ids": out_ids}]
        hb = tgb or [{"concept": "new parts", "roles": [], "group": None, "component_ids": in_ids}]
        return [Draft("HOLD", "FULL_OBJECT", hold(a, ha, "FULL_OBJECT"), w["HOLD"], [a], ha,
                      f"glow the parts of {a} that will change"), rep,
                Draft("HOLD", "FULL_OBJECT", hold(b, hb, "FULL_OBJECT"), w["HOLD"], [b], hb,
                      f"glow the new parts of {b}")]

    ccfg = ctx["cfg"]["composition"]
    purpose = ccfg["intent_purpose"].get(beat["narrative_intent"], "detail")
    presets = ctx["presets"]

    def side_by_side(states_cmp, cand, glow, why, use=purpose):
        labels = {s: model.states[s]["label"] for s in states_cmp}

        def make_cmp(n):
            anim = {"template": "SIDE_BY_SIDE", "states": list(states_cmp), "layout": cand["layout"],
                    "gap_ratio": cand["gap_ratio"], "label_band": cand["label_band"], "labels": labels}
            if ctx["caption_top"] and cand["layout"] == "ROW":   # M6: captions above the subtitle zone
                anim["label_position"] = "BAND_TOP"
            if glow:
                anim["highlight"] = dict(_pulse("DIFFERENCES", n / fps, m["highlight"]), strength=0.3)
            elif n / fps < ctx["cfg"]["timing"]["min_shot_seconds"]:
                raise T.TooShort("compare")
            return _shot("SIDE_BY_SIDE", {"from_state": states_cmp[0], "to_state": states_cmp[-1]}, anim, n, fps,
                         camera_of("COMPARISON"))
        d = Draft("SIDE_BY_SIDE", "COMPARISON", make_cmp, w["SIDE_BY_SIDE"], list(states_cmp), [],
                  f"{len(states_cmp)} variants at identical scale ({cand['layout']}, gap {cand['gap_ratio']})"
                  + ("; differing parts glow" if glow else "") + (f"; {why}" if why else ""))
        d.composition = {"layout": f"SIDE_BY_SIDE_{cand['layout']}", "gap_ratio": cand["gap_ratio"],
                         "label_band": cand["label_band"], "purpose": use, "scale": "COMMON",
                         "metrics": cand.get("metrics")}
        return d

    def choose_layout(states_cmp, use=purpose):
        cc = ccfg
        if ctx["caption_top"]:   # M6 narrated: captions of the bottom row must stay above the subtitle zone
            lb = ccfg["narrated_label_band"]
            cc = dict(ccfg, candidates=[dict(c, label_band=max(c["label_band"], lb)) for c in ccfg["candidates"]])
        rows = composition.evaluate(ctx["draft_states"], states_cmp, camera_of("COMPARISON"), cc, use, presets, fps)
        chosen = composition.best(rows)
        if chosen is None:
            raise StrategyRejected("UNREADABLE", f"no simultaneous layout of {len(states_cmp)} models reads at "
                                   f"{ccfg['reference_resolution'][0]}x{ccfg['reference_resolution'][1]} "
                                   f"({use}): " + composition.summary(rows))
        return chosen, rows

    def sequence(states_cmp, glow):
        """Each model alone, captioned, under one shared camera (build set = every compared model)."""
        built = [v for v in model.order if v in states_cmp]
        seq_band = ctx["cfg"]["camera"]["subtitle_safe_band"] if ctx["caption_top"] else ccfg["sequence_caption_band"]
        rows = composition.evaluate_sequence(ctx["draft_states"], states_cmp, built, camera_of("FULL_OBJECT"), ccfg,
                                             purpose, presets, fps)
        bad = [r for r in rows if not r["ok"]]
        if bad:
            raise StrategyRejected("UNREADABLE", "one model per frame still does not read: " + composition.summary(bad))
        shared = {p["id"] for p in model.state_ctx(states_cmp[0])["shared_parts"]}
        drafts = []
        for k, (s_id, r) in enumerate(zip(states_cmp, rows), 1):
            own = sorted(p["id"] for p in model.parts(s_id) if p["id"] not in shared) if glow else None
            d = Draft("HOLD", "FULL_OBJECT", hold(s_id, [], "FULL_OBJECT", label=model.states[s_id]["label"],
                                                 glow=own, shot_band=seq_band), w["HOLD"], [s_id], [],
                      f"{k}/{len(states_cmp)}: {model.states[s_id]['label']} alone, captioned, same locked camera and "
                      f"scale as the others" + ("; its own parts glow" if glow else ""))
            d.sequence = f"SEQ_{beat['beat_id']}"
            d.composition = {"layout": "SEQUENTIAL_COMPARISON", "purpose": purpose, "scale": "COMMON",
                             "sequence": list(states_cmp), "metrics": r["metrics"]}
            drafts.append(d)
        return drafts

    if name in ("COMPARE_SIDE_BY_SIDE", "CONTINUE_COMPARISON", "FOCUSED_PAIR"):
        states_cmp = list(arch)
        if name == "FOCUSED_PAIR":
            pair = [ctx["state_of"].get(c, c) for c in beat.get("focus_states", [])]
            if len(pair) != 2 or not set(pair) <= set(arch) or len(arch) < 3:
                raise StrategyRejected("INVALID_REQUEST", "FOCUSED_PAIR needs focus_states naming two of three or more "
                                       "compared states")
            states_cmp = [s for s in arch if s in pair]
        need_states(2)
        for s_id in states_cmp:
            support(s_id, "SIDE_BY_SIDE")
        glow = name == "CONTINUE_COMPARISON" or beat["narrative_intent"] == "SUMMARIZE_DIFFERENCES"
        if name == "CONTINUE_COMPARISON":
            prev = ctx["prev_compare"]
            if not prev or prev["states"] != states_cmp:
                raise StrategyRejected("INVALID_REQUEST", "no comparison of the same states to continue")
            cand = dict(prev["cand"])
            pc = composition.purpose_cfg(ccfg, purpose)
            if cand.get("metrics") and not composition.readable(cand["metrics"], pc)[0]:
                raise StrategyRejected("UNREADABLE", "the previous comparison does not read for "
                                       f"{purpose}: " + "; ".join(composition.readable(cand["metrics"], pc)[1]))
            return [side_by_side(states_cmp, cand, True, "continues the previous comparison (same layout)")]
        cand, rows = choose_layout(states_cmp)
        d = side_by_side(states_cmp, cand, glow, None)
        d.composition["candidates"] = [{k: r[k] for k in ("layout", "gap_ratio", "ok", "problems")} for r in rows]
        return [d]

    if name == "SEQUENTIAL_COMPARISON":
        need_states(2)
        return sequence(list(arch), beat["narrative_intent"] == "SUMMARIZE_DIFFERENCES")

    if name == "DETAIL_THEN_OVERVIEW":
        need_states(2)
        drafts = sequence(list(arch), False)
        cand, _ = choose_layout(list(arch), "overview")
        return drafts + [side_by_side(list(arch), cand, True, "overview after the details", "overview")]

    raise StrategyRejected("MISSING_TEMPLATE", f"strategy {name} is not implemented")


def _unmapped_components(beat, model, arch_states):
    """Issues for component concepts (required or focus) that no architecture state of the beat has."""
    refs = mapper.component_refs(beat, model.vocab) + list(beat.get("focus_concepts", []))
    if not refs:
        return []
    if not arch_states:
        return [f"component concepts {[V.concept_name(r) for r in refs]} need an architecture state in the beat"]
    issues = []
    for ref in refs:
        errs = []
        for sid in arch_states:
            try:
                mapper.resolve_targets([ref], model.parts(sid), model.vocab, sid)
                break
            except mapper.MappingError as e:
                errs.append(str(e))
        else:
            issues.append("semantic component not found: " + "; ".join(errs))
    return issues


def compatible(model, a, b):
    """REPLACE_PARTS a -> b is meaningful only between swap-compatible states."""
    if is_site_state(a):
        return True, "assembly from the empty site"
    sa, sb = model.states[a], model.states[b]
    if sb.get("structure_from") == a or sa.get("structure_from") == b or \
            (sa.get("structure_from") and sa.get("structure_from") == sb.get("structure_from")):
        return True, "shared frame (structure_from)"
    if sa["entry"]["family"] == sb["entry"]["family"] and sa["entry"]["family"] in REPLACE_SHARED_BASE_FAMILIES:
        return True, "both are roof assemblies on the same building"
    return False, (f"{sa['entry']['family']}/{sa['entry']['variant']} and {sb['entry']['family']}/{sb['entry']['variant']} "
                   "share no frame; whole structures are not swapped (use SEQUENTIAL_STATES or a cut)")


def allocate(drafts, total, states, fps):
    """Frames per draft: each its minimum, the rest by weight (holds stretch, motion never speeds up)."""
    mins = [T.min_frames(d.make, states, fps) for d in drafts]
    if sum(mins) > total:
        return None, mins
    extra = total - sum(mins)
    wsum = sum(d.weight for d in drafts)
    alloc = [mn + int(extra * d.weight / wsum) for mn, d in zip(mins, drafts)]
    alloc[-1] += total - sum(alloc)
    return alloc, mins


SENTENCE_CUT_LEAD = 0.2   # a cut lands this long before the sentence it belongs to starts


def align_to_sentences(alloc, mins, spans, fps):
    """M6: when a beat has at least as many sentences as shots, cut on sentence starts: the
    last (shots - 1) boundaries fall just before the last (shots - 1) sentences (a sequential
    comparison shows each model while its sentence is spoken). Falls back to the weighted
    allocation when a shot would drop below its minimum. Returns (alloc, note)."""
    k = len(alloc)
    if k < 2 or not spans or len(spans) < k:
        return alloc, None
    total = sum(alloc)
    cuts = [T.frames(max(spans[len(spans) - (k - 1) + i][0] - SENTENCE_CUT_LEAD, 0.0), fps) for i in range(k - 1)]
    bounds = [0] + cuts + [total]
    new = [bounds[i + 1] - bounds[i] for i in range(k)]
    if any(n < mn for n, mn in zip(new, mins)):
        return alloc, "weighted (cutting on sentence starts would shorten a shot below its minimum)"
    return new, (f"cuts on sentence starts {[len(spans) - (k - 1) + i for i in range(k - 1)]}")


# ---------------------------------------------------------------- plan
def plan_project(project_dir, root=ROOT, vocab=None):
    """Plan, assess target visibility, repair (camera, ghosting) and, where a strategy's shots
    cannot be made readable, re-plan that beat with its next strategy (bounded; deterministic).
    `vocab` overrides config/visual_vocabulary.json (tests); its hash is recorded in the plan inputs."""
    excluded = {}
    for _ in range(6):
        plan, unresolved = _plan_pass(project_dir, root, vocab, excluded)
        progress = False
        for bid, (strategy, detail, alternatives) in unresolved.items():
            if alternatives:
                excluded.setdefault(bid, {})[strategy] = detail
                progress = True
        if not progress:
            return plan
    return plan


def _plan_pass(project_dir, root, vocab, excluded):
    root, project_dir = Path(root), Path(project_dir)
    doc, sources, default_vocab, cfg = load_inputs(project_dir, root)
    vocab = vocab or default_vocab
    errors = B.validate(doc, sources) + V.validate(vocab) + annotations.validate_spec(doc, sources, vocab)
    errors += [f"beat {b['beat_id']}: {b['narrative_intent']} needs annotations (what the viewer must see is the "
               "load path, not only the model)" for b in doc["beats"]
               if intents.INTENTS.get(b["narrative_intent"], {}).get("needs_annotations") and not b.get("annotations")]
    if errors:
        raise PlanningError(errors)
    fps = int(cfg["timing"]["frame_rate"])
    index = catalog.index(root)
    model = Model(root, project_dir, vocab, index)
    families, sites = [], {}
    for b in doc["beats"]:
        for n in mapper.architecture_refs(b, vocab):
            c = vocab.get(n)
            if c and c["kind"] == "architecture" and c["family"] not in families:
                families.append(c["family"])
            if c and c.get("scene_context"):   # M8: a context with its own site
                sites.setdefault(c["scene_context"], c.get("site") or n)
    model.set_base(families, sites)
    windows = T.beat_windows(doc, project_dir, cfg["timing"])
    offsets = T.sentence_offsets(doc, project_dir, cfg["timing"])
    word_times = T.word_offsets(doc, project_dir)
    caption_top = doc["timing_mode"] == "AUDIO_LOCKED"   # narrated: the bottom of the frame is for subtitles
    presets = CAM.style_presets(root)

    coverage, plan_shots, warnings = [], [], []
    prev_end_state, prev_compare = None, None
    for beat in doc["beats"]:
        bid = beat["beat_id"]
        intent = beat["narrative_intent"]
        cov = {"beat_id": bid, "visual_intent": intent, "narration": beat["narration"], "status": None,
               "strategy": None, "assets": [], "semantic_targets": [], "templates": [], "shot_ids": [],
               "expected_seconds": round(windows[bid][0], 3), "timing_source": windows[bid][1], "issues": [],
               "explanation": []}
        coverage.append(cov)
        hint = intents.check(beat)
        if hint:
            warnings.append(f"{bid}: {hint}")
            cov["issues"].append(f"intent cross-check: {hint}")
        ev, ev_detail = B.evidence_status(beat, sources)
        cov["evidence_status"] = ev
        if ev == "EVIDENCE_BLOCKED":
            cov.update(status="EVIDENCE_BLOCKED")
            cov["issues"].append(ev_detail + " (add sources/evidence to research/sources.json; no visual is planned)")
            continue
        if intents.INTENTS[intent].get("needs_verified_chronology") and ev != "APPROVED":
            cov.update(status="EVIDENCE_BLOCKED")
            cov["issues"].append(intents.MISSING_CAPABILITIES["VERIFIED_CHRONOLOGY"][0] + "; " +
                                 intents.MISSING_CAPABILITIES["VERIFIED_CHRONOLOGY"][1])
            continue
        accuracy = beat.get("required_accuracy", "ILLUSTRATIVE")
        arch_states, site_concept, blocked, state_of = [], False, False, {}
        for n in mapper.architecture_refs(beat, vocab):
            c = vocab.get(n)
            if c and c["kind"] == "site":
                site_concept = n
                entry = (model.contexts.get(model.context_name(n)) or {}).get("site_entry")
                cov["assets"].append({"concept": n, "status": "REUSE_EXISTING",
                                      "asset_id": entry["asset_id"] if entry else None,
                                      "explanation": "shared site of the project"})
                continue
            r = model.resolve(n, accuracy)
            cov["assets"].append({k: r.get(k) for k in ("concept", "status", "asset_id", "explanation")})
            if r["status"] not in resolver.EXECUTABLE:
                blocked = True
                cov["issues"].append(r["explanation"])
                if r.get("task"):
                    cov["issues"].append(f"generation task: {r['task']['kind']} for {r['task']['family']}/"
                                         f"{r['task']['variant']} ({r['task']['estimate']})")
                cov["status"] = "EVIDENCE_BLOCKED" if r["status"] == "BLOCKED_MISSING_EVIDENCE" else "MISSING_ASSET"
                continue
            state_of[n] = model.add_state(n, r)
            arch_states.append(state_of[n])
        if blocked:
            continue
        unmapped = _unmapped_components(beat, model, arch_states)
        if unmapped:   # never let a lighter fallback strategy silently drop a named component
            cov.update(status="INVALID_REQUEST")
            cov["issues"] += unmapped
            continue
        model.link_frames()
        draft_states = model.states_json()
        D = T.frames(windows[bid][0], fps)
        ctx = {"cfg": cfg, "fps": fps, "model": model, "beat": beat, "arch_states": arch_states,
               "site_concept": site_concept, "component_refs": mapper.component_refs(beat, vocab),
               "draft_states": draft_states, "prev_end_state": prev_end_state, "prev_compare": prev_compare,
               "camera_of": lambda mode, sid=None, fam=(model.context_of.get(arch_states[0]) if arch_states else None) or
               (model.context_name(site_concept) if site_concept else model.family) or "bridge":
               CAM.preset_for(cfg, model.context_of.get(sid, fam) if sid else fam, mode),
               "presets": presets, "state_of": state_of, "sentence_offsets": offsets.get(bid),
               "word_offsets": word_times.get(bid),
               "caption_top": caption_top, "annotation_lead": AL.load_style()["timing"]["appear_lead_seconds"]}
        names = [beat["strategy"]] if beat.get("strategy") else intents.INTENTS[intent]["strategies"]
        if beat.get("strategy") and beat["strategy"] not in intents.STRATEGIES:
            cov.update(status="INVALID_REQUEST")
            cov["issues"].append(f"unknown strategy {beat['strategy']!r} (known: {', '.join(intents.STRATEGIES)})")
            continue
        chosen, rejections = None, []
        for name in names:
            if name in excluded.get(bid, {}):
                rejections.append(("VISIBILITY", name, excluded[bid][name]))
                continue
            try:
                drafts = build_strategy(name, ctx)
                if model.multi:
                    for d in drafts:
                        if d.states:
                            _with_context(d, model.context_of.get(d.states[0], model.family))
                draft_states = model.states_json()
                alloc, mins = allocate(drafts, D, draft_states, fps)
                if alloc is None:
                    rejections.append(("TIMING_CONFLICT", name, f"{name} needs {sum(mins) / fps:.2f} s "
                                       f"({' + '.join(f'{x / fps:.2f}' for x in mins)}), the beat has {D / fps:.2f} s"))
                    continue
                alloc, cut_note = align_to_sentences(alloc, mins, offsets.get(bid) if caption_top else None, fps)
                if cut_note:
                    cov["explanation"].append(f"{name} timing: {cut_note}")
                chosen = (name, drafts, alloc, mins)
                break
            except StrategyRejected as e:
                rejections.append((e.kind, name, e.detail + (f" [{e.capability}: {intents.MISSING_CAPABILITIES[e.capability][1]}]"
                                                             if e.capability else "")))
            except T.TimingError as e:
                rejections.append(("TIMING_CONFLICT", name, str(e)))
            except motion.PlanError as e:   # the engine refuses the configuration: report, never crash
                rejections.append(("INVALID_REQUEST", name, f"engine rejects the shot: {e}"))
        for kind, name, detail in rejections:
            cov["explanation"].append(f"{name} rejected ({kind}): {detail}")
        if chosen is None:
            kinds = {k for k, _, _ in rejections}
            status = ("TIMING_CONFLICT" if "TIMING_CONFLICT" in kinds else
                      "MISSING_TEMPLATE" if "MISSING_TEMPLATE" in kinds and "INVALID_REQUEST" not in kinds else
                      "INVALID_REQUEST" if "INVALID_REQUEST" in kinds else "MISSING_TEMPLATE")
            cov["status"] = status
            if status == "TIMING_CONFLICT":
                cov["issues"].append("timing conflict: simplify the visual (choose a lighter strategy), split the beat, "
                                     "extend the narration, or change the visual strategy; nothing was truncated")
            else:
                cov["issues"] += [d for k, _, d in rejections if k == status]
            continue
        name, drafts, alloc, mins = chosen
        if name in ("SEQUENTIAL_COMPARISON", "DETAIL_THEN_OVERVIEW") and \
                re.search(r"\b(side by side|together|at once|simultaneous(ly)?)\b", beat["narration"].lower()):
            note = (f"narration says the models are seen together, but no simultaneous layout reads at the reference "
                    f"resolution: {name} (same camera and scale) instead; consider rewording the narration")
            cov["issues"].append(note)
            warnings.append(f"{bid}: {note}")
        cov["strategy"] = name
        cov["status"] = "PARTIALLY_COVERED" if name in PARTIAL.get(intent, ()) else "COVERED"
        cov["explanation"].append(f"{name}: {intents.STRATEGIES[name][1]}")
        ev_status = "INTERNAL_PREVIEW" if doc["publication"]["restriction"] == "INTERNAL_ONLY" else ev
        beat_t = 0
        for i, (d, n, mn) in enumerate(zip(drafts, alloc, mins)):
            if getattr(d, "extend_hold", None) is not None:      # REPLACE: extra time is a longer pre-swap hold
                d.make = d.extend_hold(lambda nn, mn=mn: max(0.0, (nn - mn) / fps * 0.4))
            shot = d.make(n)
            shot.update(beat_ids=[bid], claim_ids=list(beat.get("claim_ids", [])), narration=beat["narration"],
                        visual_purpose=f"{beat['visual_goal']} [{name} {i + 1}/{len(drafts)}: {d.explanation}]")
            plan_shots.append({"shot": shot, "beat_id": bid, "visual_intent": intent, "strategy": name,
                               "part": [i + 1, len(drafts)], "template": d.template, "states": d.states,
                               "camera": {"mode": d.mode, "preset": shot["camera"], "focus": d.focus,
                                          "safe_band": shot.get("camera_safe_band", 0.0)},
                               "semantic_targets": [{"concept": t["concept"], "roles": t["roles"], "group": t["group"],
                                                     "component_ids": t["component_ids"]} for t in d.targets],
                               "timing": {"mode": windows[bid][1], "frames": n, "duration_seconds": round(n / fps, 6),
                                          "min_seconds": round(mn / fps, 4), "beat_offset_seconds": round(beat_t / fps, 6)},
                               "explanation": d.explanation, "evidence_status": ev_status,
                               "composition": d.composition, "sequence": d.sequence,
                               **({"repair_preference": list(beat["visual_repair_preference"])}
                                  if beat.get("visual_repair_preference") else {}),
                               "asset_ids": [model.states[s]["asset_id"] for s in d.states if model.states[s]["asset_id"]]})
            cov["templates"].append(d.template)
            beat_t += n
        cov["semantic_targets"] = sorted({t["concept"] for d in drafts for t in d.targets})
        last = plan_shots[-1]
        prev_end_state = last["states"][-1] if last["template"] != "SIDE_BY_SIDE" and last["states"] else None
        prev_compare = ({"states": last["states"], "cand": {k: last["shot"]["animation"][k] for k in
                                                           ("layout", "gap_ratio", "label_band")}
                         | {"metrics": (last["composition"] or {}).get("metrics")}}
                        if last["template"] == "SIDE_BY_SIDE" else None)

    _continuity(plan_shots, model)
    for i, ps in enumerate(plan_shots, 1):
        ps["shot_id"] = ps["shot"]["id"] = f"SC_{i:03d}"
    t = 0
    for ps in plan_shots:
        ps["timing"]["start_seconds"] = round(t / fps, 6)
        t += ps["timing"]["frames"]
    for cov in coverage:
        cov["shot_ids"] = [ps["shot_id"] for ps in plan_shots if ps["beat_id"] == cov["beat_id"]]
    records, unresolved = repair.repair_plan(plan_shots, model.states_json, lambda: _continuity(plan_shots, model),
                                             cfg, presets, fps,
                                             (lambda ps: model.context_of.get(ps["states"][-1], model.family))
                                             if model.multi else model.family or "bridge",
                                             {k for k, c in vocab.concepts.items() if c.get("read_as") == "pieces"})
    replan = {}
    cov_by = {c["beat_id"]: c for c in coverage}
    by_shot = {ps["shot_id"]: ps for ps in plan_shots}
    for rec in records:
        cov_by[rec["beat_id"]].setdefault("visual_repairs", []).append(rec)
        if rec["chosen"]:
            ps = by_shot[rec["shot_id"]]
            ps.setdefault("repairs", []).append({"concept": rec["concept"], "remedy": rec["chosen"],
                                                 "problems": rec["problems"], "before": rec["before"],
                                                 "after": rec["after"]})
            ps["explanation"] += f"; repaired ({rec['chosen']}): {rec['concept']} was {', '.join(rec['problems'])}"
    for bid, rows in unresolved.items():
        cov = cov_by[bid]
        beat = next(b for b in doc["beats"] if b["beat_id"] == bid)
        names = [beat["strategy"]] if beat.get("strategy") else intents.INTENTS[beat["narrative_intent"]]["strategies"]
        later = [n for n in names[names.index(cov["strategy"]) + 1:] if n not in excluded.get(bid, {})]
        detail = "; ".join(f"{r['concept']} {','.join(r['problems'])} (share {r.get('visible_share', 0):.2f}, "
                           f"core {r.get('core_area', 0) * 100:.2f}%)" for r in rows) + " after camera/ghost repairs"
        replan[bid] = (cov["strategy"], detail, bool(later))
        if not later:
            if cov["status"] == "COVERED":
                cov["status"] = "PARTIALLY_COVERED"
            cov["issues"].append(f"VISIBILITY_UNRESOLVED: {detail}; manual review (or verify-visibility in Blender)")
            warnings.append(f"{bid}: visibility unresolved: {detail}")
    for ps in plan_shots:
        if ps.get("visibility"):
            unc = [r["concept"] for r in ps["visibility"]["targets"] if r.get("verification") == "UNCERTAIN"]
            if unc:
                warnings.append(f"{ps['shot_id']} {', '.join(sorted(set(unc)))}: visibility UNCERTAIN offline "
                                "(proxy geometry or few samples): verify in Blender (verify-visibility)")
    _annotate(doc, plan_shots, coverage, model, vocab, sources, offsets, windows, presets, fps, caption_top, warnings,
              word_times=word_times)
    checks = consistency.check_plan({"shots": plan_shots}, doc, offsets, AL.load_style(root / "config/annotation_style.json"))
    cov_by = {c["beat_id"]: c for c in coverage}
    for r in checks:   # M6: narration that contradicts the picture blocks the plan (fail closed)
        if r["verdict"] == "CONTRADICTION":
            c = cov_by[r["beat_id"]]
            c["consistency_failures"] = c.get("consistency_failures", 0) + 1
            c["issues"].append(f"NARRATION_CONTRADICTION ({r['rule']}, sentence {r['sentence']}): {r['detail']}")
            warnings.append(f"{r['beat_id']}.s{r['sentence']}: narration/visual contradiction: {r['detail']}")
    executable = all(c["status"] in ("COVERED", "PARTIALLY_COVERED") and not c.get("annotation_failures")
                     and not c.get("consistency_failures") for c in coverage)
    inputs = {"beats_sha256": B.content_hash(doc), "sources_sha256": B.content_hash(sources),
              "vocabulary_sha256": B.content_hash(vocab.data), "planning_config_sha256": B.content_hash(cfg),
              "assets": {e["asset_id"]: B.content_hash(json.loads((root / e["path"]).read_text()))
                         for e in sorted({s["entry"]["path"]: s["entry"] for s in model.states.values()
                                          if s["entry"]}.values(), key=lambda e: e["asset_id"])}}
    if any(b.get("annotations") for b in doc["beats"]):
        inputs["annotation_style_sha256"] = annotations.style_hash(AL.load_style(root / "config/annotation_style.json"))
    if doc["timing_mode"] == "AUDIO_LOCKED":
        from pipeline import audio_lock
        inputs["timing_sha256"] = audio_lock.beats_hash(json.loads((project_dir / "script/timing.json").read_text()))
    return {"schema": "visual_plan/1", "plan_version": "1.0", "planner_version": PLANNER_VERSION,
            "project_id": doc["project_id"], "title": doc.get("title"), "timing_mode": doc["timing_mode"],
            "publication": doc["publication"], "fps": fps, "total_frames": t, "duration_seconds": round(t / fps, 6),
            "executable": executable, "inputs": inputs, "family": model.family,
            **({"scene_contexts": list(model.contexts)} if model.multi else {}),
            "states": model.states_json(),
            "resolutions": [{k: r.get(k) for k in ("concept", "status", "asset_id", "explanation")}
                            for r in model.resolutions.values()],
            "shots": plan_shots, "coverage": coverage, "warnings": warnings,
            "visibility_summary": _visibility_summary(plan_shots, records, unresolved),
            "consistency": {"rows": checks, "summary": consistency.summary(checks)},
            "pieces_concepts": sorted(k for k, c in vocab.concepts.items() if c.get("read_as") == "pieces")}, replan


def _annotate(doc, plan_shots, coverage, model, vocab, sources, offsets, windows, presets, fps, caption_top, warnings,
              word_times=None):
    """M6: semantic annotations of every planned beat (planner/annotations.py); a beat whose
    annotations cannot be attached, anchored or placed is not executable (fail closed)."""
    if not any(b.get("annotations") for b in doc["beats"]):
        return
    style = AL.load_style()
    cov_by = {c["beat_id"]: c for c in coverage}
    match_after = {a["shot_id"] for a, b in zip(plan_shots, plan_shots[1:]) if b["cut_from_previous"] == "match"}
    for beat in doc["beats"]:
        cov = cov_by[beat["beat_id"]]
        if not beat.get("annotations") or cov["status"] not in ("COVERED", "PARTIALLY_COVERED"):
            continue
        shots = [(ps, ps["timing"]["beat_offset_seconds"]) for ps in plan_shots if ps["beat_id"] == beat["beat_id"]]
        seconds = sum(ps["timing"]["frames"] for ps, _ in shots) / fps
        records, issues = annotations.plan_beat(beat, shots, offsets[beat["beat_id"]], seconds, model, vocab, sources,
                                                style, presets, fps, caption_top, match_after,
                                                words=(word_times or {}).get(beat["beat_id"]))
        cov["annotations"] = records
        cov["annotation_failures"] = sum(1 for r in records if r["status"] != "PLACED")
        if issues:
            cov["status"] = "PARTIALLY_COVERED"
            cov["issues"] += issues
            warnings += [f"{beat['beat_id']}: {i}" for i in issues]


def _continuity(plan_shots, model):
    """Continuity groups (one locked camera each) and cut types. A group continues through a
    match cut (same camera preset and focus, the next shot starts where the last ended) and
    through the hard cuts inside one sequential comparison (one camera for every model)."""
    group, prev = 0, None
    for ps in plan_shots:
        single = ps["template"] not in ("SIDE_BY_SIDE", "MOTION_GRAPHICS")
        if prev is not None and (prev["shot"].get("animation") or {}).get("camera_move"):
            cut = "hard"    # M7: after a push-in the view is closer than the locked framing
            group += 1
        elif prev is not None and ps.get("sequence") and prev.get("sequence") == ps["sequence"]:
            cut = "hard"    # next model of a sequential comparison: same locked camera, new state
        elif prev is not None and single and prev["template"] not in ("SIDE_BY_SIDE", "MOTION_GRAPHICS") and \
                prev["camera"]["preset"] == ps["camera"]["preset"] and prev["camera"]["focus"] == ps["camera"]["focus"] \
                and prev["states"][-1] == ps["states"][0]:
            cut = "match"
        elif prev is not None and ps["template"] == "SIDE_BY_SIDE" and prev["template"] == "SIDE_BY_SIDE" and \
                prev["states"] == ps["states"] and all(prev["shot"]["animation"].get(k) == ps["shot"]["animation"].get(k)
                                                       for k in ("layout", "gap_ratio", "label_band")):
            cut = "match"
        else:
            cut = "hard" if prev is not None else "first"
            group += 1
        ps["camera"]["group"] = group
        ps["cut_from_previous"] = cut
        prev = ps
    states = model.states_json()
    for g in sorted({ps["camera"]["group"] for ps in plan_shots}):
        members = [ps for ps in plan_shots if ps["camera"]["group"] == g]
        if members[0]["template"] in ("SIDE_BY_SIDE", "MOTION_GRAPHICS"):
            continue
        built = []
        for ps in members:
            for s in ps["states"]:
                for v in spec.build_set(states, s):
                    if v not in built:
                        built.append(v)
        order = [v["id"] for v in states["variants"]]
        built = [v for v in order if v in built]
        for ps in members:
            ps["shot"]["build_variants"] = built
        for ps in members:
            ps["camera"]["build_variants"] = built


def _visibility_summary(plan_shots, records, unresolved):
    rows = [r for ps in plan_shots if ps.get("visibility") for r in ps["visibility"]["targets"]]
    return {"shots_assessed": sum(1 for ps in plan_shots if ps.get("visibility")),
            "target_rows": len(rows), "rows_passing": sum(1 for r in rows if r.get("ok")),
            "uncertain_rows": sum(1 for r in rows if r.get("verification") == "UNCERTAIN"),
            "issues_detected": len({(r["beat_id"], r["concept"]) for r in records}),
            "auto_repaired": len({(r["beat_id"], r["concept"]) for r in records if r["chosen"]}),
            "manual_review": sum(len(v) for v in unresolved.values()),
            "method": "LEVEL_1_OFFLINE_RASTER (planner/visibility.py); Level 2: tools/cli.py verify-visibility"}
