"""Narrative beats -> visual execution plan (deterministic; no model calls).

For each beat, in order: evidence gate -> asset resolution -> the intent's strategies in
preference order, each checked for preconditions (asset support, state compatibility,
semantic targets) and timing (minimum durations from the real motion planner) -> shots
with concrete template configs, camera mode/preset/focus, timing and explanations.
Beats that cannot be visualised are reported, never dropped or padded.
"""
import json
from pathlib import Path

from engine import motion, spec, templates
from engine.arch import assets, semantic
from planner import PLANNER_VERSION, beats as B, camera as CAM, catalog, intents, mapper, resolver
from planner import timing as T, vocabulary as V

ROOT = Path(__file__).resolve().parent.parent
SITE_STATE = "site"
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
    """Resolved states, the draft states.json and per-state semantic parts."""

    def __init__(self, root, project_dir, vocab, index):
        self.root, self.project_dir, self.vocab, self.index = Path(root), Path(project_dir), vocab, index
        self.states, self.order, self.resolutions, self.base, self.shared_parts = {}, [], {}, None, []
        self.family, self.site_entry, self.generated = None, None, {}

    def resolve(self, concept, accuracy):
        key = (concept, accuracy)
        if key not in self.resolutions:
            self.resolutions[key] = resolver.resolve(concept, self.vocab, self.index, accuracy, self.site_entry)
        return self.resolutions[key]

    def set_base(self, families):
        if len(families) > 1:
            raise PlanningError([f"one project can show one building family per shared base; beats mix {sorted(families)}"])
        self.family = next(iter(families)) if families else None
        if self.family == "bridge":
            r = resolver.resolve("river_crossing_site", self.vocab, self.index)
            if r["status"] != "REUSE_EXISTING":
                raise PlanningError([f"bridges need a site asset: {r['explanation']}"])
            self.site_entry = r["entry"]
            self.base = {"builder": "architecture_asset", "asset": self.site_entry["path"]}
            parts = catalog.component_parts(self.site_entry, "shared")
            self.shared_parts = [dict(p) for p in parts]
            self.shared_components = sorted({p["group"] for p in parts})
            self.resolutions[("river_crossing_site", "ILLUSTRATIVE")] = r

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
        if self.base is None and entry["source"] == "legacy_states":
            self.base = entry["legacy_base"]
            self.shared_components = list(entry["legacy_shared"])
            states = {"base": self.base, "shared_components": self.shared_components}
            self.shared_parts = [{"id": p["id"], "role": p["role"], "group": p["group"], "layer": 0, "replaceable": False}
                                 for p in spec.base_parts(states) if p["id"] in spec.shared_ids(states)]
        sid = concept
        self.states[sid] = {"id": sid, "concept": concept, "label": self.vocab.label(concept), "entry": entry,
                            "asset_id": resolution["asset_id"], "resolution": resolution["status"]}
        self.order.append(sid)
        return sid

    def add_site_state(self):
        if SITE_STATE not in self.states:
            self.states[SITE_STATE] = {"id": SITE_STATE, "concept": "river_crossing_site", "label": "Site",
                                       "entry": None, "asset_id": None, "resolution": "SITE_ONLY"}
            self.order.insert(0, SITE_STATE)

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
        for sid in self.order:
            st = self.states[sid]
            if sid == SITE_STATE:
                variants.append({"id": SITE_STATE, "name": "Empty site (no structure)", "builder": "none"})
                continue
            e = st["entry"]
            if e["source"] == "library":
                v = {"id": sid, "name": st["label"], "builder": "architecture_asset", "asset": e["path"]}
            else:
                v = {k: val for k, val in e["legacy_variant"].items() if k not in ("components",)}
                v.update(id=sid, name=st["label"])
            if st.get("structure_from"):
                v["structure_from"] = st["structure_from"]
            variants.append(v)
        return {"schema_version": 2, "generated_by": "planner", "planner_version": PLANNER_VERSION,
                "building_type": self.family, "base": self.base, "shared_components": self.shared_components,
                "variants": variants, "transitions": []}

    def parts(self, sid):
        """Visible semantic parts of a state: shared base + own + inherited frame."""
        st = self.states[sid]
        if sid == SITE_STATE:
            return list(self.shared_parts)
        own = catalog.component_parts(st["entry"], sid)
        src = st.get("structure_from")
        if src:
            inherited = [p for p in catalog.component_parts(self.states[src]["entry"], src) if not p["replaceable"]]
            own = [p for p in own if p["replaceable"]] + inherited
        return list(self.shared_parts) + own

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
def _pulse(ids, seconds, m):
    hold = seconds - m["start"] - m["rise"] - m["fall"] - m["tail"]
    if hold < 0.3:
        raise T.TooShort("highlight")
    return {"components": ids, "start_seconds": m["start"], "rise_seconds": m["rise"], "hold_seconds": round(hold, 4),
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

    def support(sid, template):
        st = model.states[sid]
        if sid != SITE_STATE and template not in st["entry"]["animation_support"] and template != "HOLD":
            raise StrategyRejected("MISSING_TEMPLATE", f"asset {st['asset_id']} does not support {template}")

    def targets_in(sid):
        try:
            return mapper.resolve_targets(ctx["component_refs"], model.parts(sid), model.vocab, sid)
        except mapper.MappingError as e:
            raise StrategyRejected("INVALID_REQUEST", str(e))

    def ids_of(tg):
        return sorted({i for t in tg for i in t["component_ids"]})

    def covering(sid, tg):
        """Parts that normally cover the highlighted ones (vocabulary ghost_roles, e.g. deck planks
        over stringers): they turn see-through while the targets glow."""
        roles = set()
        for t in tg:
            roles |= set((model.vocab.get(t["concept"]) or {}).get("ghost_roles", []))
        roles -= {r for t in tg for r in t["roles"]}
        glowing = set(ids_of(tg))
        return sorted(p["id"] for p in model.parts(sid) if p["role"] in roles and p["id"] not in glowing)

    def hold(sid, tg, mode, focus=None):
        ids = ids_of(tg)
        ghost = covering(sid, tg) if ids else []

        def make(n):
            anim = {"template": "HOLD", "state": sid}
            if ids:
                support(sid, "HIGHLIGHT")
                anim["highlight"] = _pulse(ids, n / fps, m["highlight"])
                if ghost:
                    anim["highlight"].update(ghost=ghost, ghost_transparency=m["highlight"]["ghost_transparency"])
            elif n / fps < ctx["cfg"]["timing"]["min_shot_seconds"]:
                raise T.TooShort("hold")
            return _shot("HOLD", {"from_state": sid, "to_state": sid}, anim, n, fps, camera_of(mode), focus, band)
        make.ghost = ghost
        return make

    if name == "SITE_HOLD":
        if not ctx["site_concept"]:
            raise StrategyRejected("MISSING_TEMPLATE", "no site concept in the beat", "MAP_OR_IMAGERY")
        model.add_site_state()
        return [Draft("HOLD", "FULL_OBJECT", hold(SITE_STATE, [], "FULL_OBJECT"), w["HOLD"], [SITE_STATE], [],
                      "the empty shared site: the gap any of the structures must span")]

    if name == "CARD":
        g = beat.get("graphic")
        if not g:
            cap = "FORCE_DIAGRAM" if beat["narrative_intent"] == "EXPLAIN_CAUSE_EFFECT" else "MAP_OR_IMAGERY"
            raise StrategyRejected("MISSING_TEMPLATE", intents.MISSING_CAPABILITIES[cap][0], cap)

        def make(n):
            return {"id": "PLAN", "duration_seconds": n / fps, "visual_type": "MOTION_GRAPHICS", "transition": "CARD",
                    "camera": "CARD", "graphic": g, "from_state": None, "to_state": None}
        return [Draft("MOTION_GRAPHICS", "CARD", make, 1.0, [], [], "2D card supplied by the beat")]

    if name in ("HOLD", "HOLD_HIGHLIGHT"):
        need_states(1)
        sid = arch[0]
        tg = targets_in(sid) if name == "HOLD_HIGHLIGHT" else []
        if name == "HOLD_HIGHLIGHT" and not tg:
            raise StrategyRejected("INVALID_REQUEST", "HOLD_HIGHLIGHT needs component concepts to highlight")
        mode = beat.get("camera_mode", "FULL_OBJECT")
        return [Draft("HOLD", mode, hold(sid, tg, mode), w["HOLD"], [sid], tg,
                      f"hold {sid}" + (f", glowing {', '.join(t['concept'] for t in tg)}" if tg else ""))]

    if name == "ASSEMBLE_IN":
        need_states(1)
        sid = arch[0]
        if ctx["prev_end_state"] != SITE_STATE:
            raise StrategyRejected("INVALID_REQUEST", "ASSEMBLE_IN needs the previous shot to end on the empty site")
        tg = targets_in(sid)

        def make_in(n):
            anim = {"template": "REPLACE_PARTS", "from_state": SITE_STATE, "to_state": sid, "easing": "SMOOTH",
                    "hold_start_seconds": m["assemble"]["min_hold_start"], "hold_end_seconds": m["assemble"]["min_hold_end"],
                    "incoming": {"direction": "FROM_ABOVE", "distance": 2.5, "move_seconds": m["assemble"]["move_in"],
                                 "stagger_seconds": m["assemble"]["stagger"], "fade": True, "fade_end": 0.7,
                                 "overlap_seconds": 0.0, "easing": "EASE_OUT"}}
            return _shot("REPLACE_PARTS", {"from_state": SITE_STATE, "to_state": sid}, anim, n, fps,
                         camera_of("LOCKED_TRANSFORMATION"), None, band)
        drafts = [Draft("REPLACE_PARTS", "LOCKED_TRANSFORMATION", make_in, w["REPLACE_PARTS"], [SITE_STATE, sid], [],
                        f"{sid} assembles into the shown empty site (its parts drop in by assembly layer)")]
        if tg:
            drafts.append(Draft("HOLD", "FULL_OBJECT", hold(sid, tg, "FULL_OBJECT"), w["HOLD"], [sid], tg,
                                f"then {', '.join(t['concept'] for t in tg)} glow"))
        return drafts

    if name == "CLOSEUP_HIGHLIGHT":
        need_states(1)
        sid = arch[0]
        wide = targets_in(sid)
        focus_refs = beat.get("focus_concepts") or ctx["component_refs"]
        try:
            tg = mapper.resolve_targets(focus_refs, model.parts(sid), model.vocab, sid)
        except mapper.MappingError as e:
            raise StrategyRejected("INVALID_REQUEST", str(e))
        if not tg:
            raise StrategyRejected("INVALID_REQUEST", "a close-up needs component concepts to frame")
        focus = ids_of(tg)
        return [Draft("HOLD", "FULL_OBJECT", hold(sid, wide, "FULL_OBJECT"), w["HOLD"], [sid], wide,
                      f"establish {sid} with {', '.join(t['concept'] for t in wide)} glowing"),
                Draft("HOLD", "COMPONENT_CLOSEUP", hold(sid, tg, "COMPONENT_CLOSEUP", focus), w["HOLD"], [sid], tg,
                      f"close-up framed on {len(focus)} component(s)", focus=focus)]

    if name in ("EXPLODE", "HIGHLIGHT_THEN_EXPLODE"):
        need_states(1)
        sid = arch[0]
        support(sid, "EXPLODED_VIEW")
        ids, per = model.explode_components(sid)
        if not ids:
            raise StrategyRejected("MISSING_TEMPLATE", f"{sid} has no explodable components")
        tg = targets_in(sid)
        hl = sorted(set(ids_of(tg)) & set(ids))
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
            return _shot("EXPLODED_VIEW", {"from_state": sid, "to_state": sid}, anim, n, fps,
                         camera_of("LOCKED_TRANSFORMATION"), None, band)
        ex = Draft("EXPLODED_VIEW", "LOCKED_TRANSFORMATION", make_ex, w["EXPLODED_VIEW"], [sid], tg,
                   f"take {sid} apart by assembly layer ({len(ids)} components, {layers} layers) and back"
                   + (f"; {len(hl)} focus components glow" if hl else ""))
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
        tga, tgb = targets_in(a) if ctx["component_refs"] else [], targets_in(b) if ctx["component_refs"] else []
        if name == "SEQUENTIAL_STATES":
            return [Draft("HOLD", "FULL_OBJECT", hold(a, tga, "FULL_OBJECT"), w["HOLD"], [a], tga, f"show {a}"),
                    Draft("HOLD", "FULL_OBJECT", hold(b, tgb, "FULL_OBJECT"), w["HOLD"], [b], tgb,
                          f"cut to {b} (not swap-compatible with {a}, shown separately)")]
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

    if name in ("COMPARE_SIDE_BY_SIDE", "CONTINUE_COMPARISON"):
        need_states(2)
        for s in arch:
            support(s, "SIDE_BY_SIDE")
        if name == "CONTINUE_COMPARISON" and ctx["prev_compare"] != list(arch):
            raise StrategyRejected("INVALID_REQUEST", "no comparison of the same states to continue")
        fam = model.family
        aspect = CAM.aspect_class(ctx["cfg"], fam)
        layout = ctx["cfg"]["aspect_classes"][aspect]["comparison_layout"]
        labels = {s: model.states[s]["label"] for s in arch}
        glow = name == "CONTINUE_COMPARISON" or beat["narrative_intent"] == "SUMMARIZE_DIFFERENCES"

        def make_cmp(n):
            anim = {"template": "SIDE_BY_SIDE", "states": list(arch), "layout": layout,
                    "gap_ratio": 0.5 if layout == "STACK" else 0.35, "label_band": 0.1 if layout == "STACK" else 0.14,
                    "labels": labels}
            if glow:
                anim["highlight"] = dict(_pulse("DIFFERENCES", n / fps, m["highlight"]), strength=0.3)
            elif n / fps < ctx["cfg"]["timing"]["min_shot_seconds"]:
                raise T.TooShort("compare")
            return _shot("SIDE_BY_SIDE", {"from_state": arch[0], "to_state": arch[-1]}, anim, n, fps,
                         camera_of("COMPARISON"))
        return [Draft("SIDE_BY_SIDE", "COMPARISON", make_cmp, w["SIDE_BY_SIDE"], list(arch), [],
                      f"{len(arch)} variants at identical scale ({layout})" + ("; differing parts glow" if glow else ""))]

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
    if a == SITE_STATE:
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


# ---------------------------------------------------------------- plan
def plan_project(project_dir, root=ROOT, vocab=None):
    """`vocab` overrides config/visual_vocabulary.json (tests); its hash is recorded in the plan inputs."""
    root, project_dir = Path(root), Path(project_dir)
    doc, sources, default_vocab, cfg = load_inputs(project_dir, root)
    vocab = vocab or default_vocab
    errors = B.validate(doc, sources) + V.validate(vocab)
    if errors:
        raise PlanningError(errors)
    fps = int(cfg["timing"]["frame_rate"])
    index = catalog.index(root)
    model = Model(root, project_dir, vocab, index)
    families = set()
    for b in doc["beats"]:
        for n in mapper.architecture_refs(b, vocab):
            c = vocab.get(n)
            if c and c["kind"] == "architecture":
                families.add(c["family"])
    model.set_base(families)
    windows = T.beat_windows(doc, project_dir, cfg["timing"])

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
        arch_states, site_concept, blocked = [], False, False
        for n in mapper.architecture_refs(beat, vocab):
            c = vocab.get(n)
            if c and c["kind"] == "site":
                site_concept = True
                cov["assets"].append({"concept": n, "status": "REUSE_EXISTING",
                                      "asset_id": model.site_entry["asset_id"] if model.site_entry else None,
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
            arch_states.append(model.add_state(n, r))
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
               "camera_of": lambda mode: CAM.preset_for(cfg, model.family or "bridge", mode)}
        names = [beat["strategy"]] if beat.get("strategy") else intents.INTENTS[intent]["strategies"]
        if beat.get("strategy") and beat["strategy"] not in intents.STRATEGIES:
            cov.update(status="INVALID_REQUEST")
            cov["issues"].append(f"unknown strategy {beat['strategy']!r} (known: {', '.join(intents.STRATEGIES)})")
            continue
        chosen, rejections = None, []
        for name in names:
            try:
                drafts = build_strategy(name, ctx)
                draft_states = model.states_json()
                alloc, mins = allocate(drafts, D, draft_states, fps)
                if alloc is None:
                    rejections.append(("TIMING_CONFLICT", name, f"{name} needs {sum(mins) / fps:.2f} s "
                                       f"({' + '.join(f'{x / fps:.2f}' for x in mins)}), the beat has {D / fps:.2f} s"))
                    continue
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
        cov["strategy"] = name
        cov["status"] = "PARTIALLY_COVERED" if name in PARTIAL.get(intent, ()) else "COVERED"
        cov["explanation"].append(f"{name}: {intents.STRATEGIES[name][1]}")
        ev_status = "INTERNAL_PREVIEW" if doc["publication"]["restriction"] == "INTERNAL_ONLY" else ev
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
                                          "min_seconds": round(mn / fps, 4)},
                               "explanation": d.explanation + (f"; {len(d.make.ghost)} covering part(s) turn see-through "
                                                               f"while they glow" if getattr(d.make, "ghost", None) else ""),
                               "evidence_status": ev_status,
                               "asset_ids": [model.states[s]["asset_id"] for s in d.states if model.states[s]["asset_id"]]})
            cov["templates"].append(d.template)
        cov["semantic_targets"] = sorted({t["concept"] for d in drafts for t in d.targets})
        last = plan_shots[-1]
        prev_end_state = last["states"][-1] if last["template"] != "SIDE_BY_SIDE" else None
        prev_compare = last["states"] if last["template"] == "SIDE_BY_SIDE" else None

    _continuity(plan_shots, model)
    for i, ps in enumerate(plan_shots, 1):
        ps["shot_id"] = ps["shot"]["id"] = f"SC_{i:03d}"
    t = 0
    for ps in plan_shots:
        ps["timing"]["start_seconds"] = round(t / fps, 6)
        t += ps["timing"]["frames"]
    for cov in coverage:
        cov["shot_ids"] = [ps["shot_id"] for ps in plan_shots if ps["beat_id"] == cov["beat_id"]]
    _visibility(plan_shots, model, cfg, warnings)
    executable = all(c["status"] in ("COVERED", "PARTIALLY_COVERED") for c in coverage)
    inputs = {"beats_sha256": B.content_hash(doc), "sources_sha256": B.content_hash(sources),
              "vocabulary_sha256": B.content_hash(vocab.data), "planning_config_sha256": B.content_hash(cfg),
              "assets": {e["asset_id"]: B.content_hash(json.loads((root / e["path"]).read_text()))
                         for e in sorted({s["entry"]["path"]: s["entry"] for s in model.states.values()
                                          if s["entry"]}.values(), key=lambda e: e["asset_id"])}}
    return {"schema": "visual_plan/1", "plan_version": "1.0", "planner_version": PLANNER_VERSION,
            "project_id": doc["project_id"], "title": doc.get("title"), "timing_mode": doc["timing_mode"],
            "publication": doc["publication"], "fps": fps, "total_frames": t, "duration_seconds": round(t / fps, 6),
            "executable": executable, "inputs": inputs, "family": model.family,
            "states": model.states_json(),
            "resolutions": [{k: r.get(k) for k in ("concept", "status", "asset_id", "explanation")}
                            for r in model.resolutions.values()],
            "shots": plan_shots, "coverage": coverage, "warnings": warnings}


def _continuity(plan_shots, model):
    """Continuity groups (one locked camera each) and cut types. A group continues only through
    a match cut: same camera preset and focus, and the next shot starts where the last ended."""
    group, prev = 0, None
    for ps in plan_shots:
        single = ps["template"] not in ("SIDE_BY_SIDE", "MOTION_GRAPHICS")
        if prev is not None and single and prev["template"] not in ("SIDE_BY_SIDE", "MOTION_GRAPHICS") and \
                prev["camera"]["preset"] == ps["camera"]["preset"] and prev["camera"]["focus"] == ps["camera"]["focus"] \
                and prev["states"][-1] == ps["states"][0]:
            cut = "match"
        elif prev is not None and ps["template"] == "SIDE_BY_SIDE" and prev["template"] == "SIDE_BY_SIDE" and \
                prev["states"] == ps["states"] and prev["shot"]["animation"]["layout"] == ps["shot"]["animation"]["layout"]:
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


def _visibility(plan_shots, model, cfg, warnings):
    """Offline check that semantic targets are inside the locked camera and large enough."""
    presets = CAM.style_presets()
    aspect = 16 / 9
    for ps in plan_shots:
        ps["visibility"] = []
        if not ps["semantic_targets"] or ps["template"] in ("SIDE_BY_SIDE", "MOTION_GRAPHICS"):
            continue
        built = ps["shot"].get("build_variants") or []
        variant_assets = []
        for v in built:
            st = model.states[v]
            if v == SITE_STATE:
                continue
            e = st["entry"]
            variant_assets.append((e["path"] if e["source"] == "library" else None, v))
        pts = CAM.group_points(model.base.get("asset") if model.family == "bridge" else None, variant_assets)
        if pts is None:
            ps["visibility"].append({"target": "*", "ok": None,
                                     "detail": "not checked offline (legacy geometry is built in Blender); see Blender QA"})
            continue
        if ps["camera"]["focus"]:
            focus = set(ps["camera"]["focus"])
            pts = [p for v, owner in variant_assets for c in assets.plan_cached(v, owner) if c.id in focus
                   for p in semantic.world_verts(c)]
        comps = {}
        for v, owner in variant_assets:
            for c in assets.plan_cached(v, owner):
                comps[c.id] = c
        for t in ps["semantic_targets"]:
            tp = [p for cid in t["component_ids"] if cid in comps for p in semantic.world_verts(comps[cid])]
            if not tp:
                continue
            ok, detail = CAM.visibility(pts, tp, presets[ps["camera"]["preset"]], aspect, ps["camera"]["safe_band"],
                                        cfg["camera"]["min_target_frame_fraction"])
            ps["visibility"].append({"target": t["concept"], "ok": ok, "detail": detail})
            if not ok:
                warnings.append(f"{ps['beat_id']} {t['concept']}: {detail}")
