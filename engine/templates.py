"""Template dispatcher: storyboard shot + states.json -> motion.Plan (pure Python, no bpy).

Blender (engine/shot_builder.py) passes real rest transforms; tools/validator.py
passes placeholders from ``placeholder_slots`` so timing, ownership and config
errors are caught at G0 before anything is built.
"""
import math

from engine import motion, spec

TEMPLATES = ("HOLD", "REPLACE_PARTS", "EXPLODED_VIEW", "SIDE_BY_SIDE")
MAIN_SLOT = "main"


def animation_config(shot):
    """Shot animation config; v0.1 shots without `animation` fall back to `transition`."""
    sid = shot.get("id", "(missing)")
    cfg = dict(shot.get("animation") or {})
    template = cfg.get("template") or shot.get("transition")
    if template not in TEMPLATES:
        raise motion.PlanError(f"{sid}: unknown template '{template}' (supported: {', '.join(TEMPLATES)})")
    if shot.get("transition") and shot["transition"] != template:
        raise motion.PlanError(f"{sid}: transition '{shot['transition']}' must match animation.template '{template}'")
    if cfg.get("duration_seconds") is not None and \
            abs(float(cfg["duration_seconds"]) - float(shot.get("duration_seconds", 0))) > 1e-6:
        raise motion.PlanError(f"{sid}: animation.duration_seconds must equal the shot duration")
    cfg["template"] = template
    return cfg


def frame_count(shot, fps):
    frames = shot["duration_seconds"] * fps
    if abs(frames - round(frames)) > 1e-6:
        raise motion.PlanError(f"{shot.get('id')}: duration {shot['duration_seconds']}s is not a whole number of frames at {fps} fps")
    return int(round(frames))


def _known_state(states, state_id, sid, field):
    if state_id not in spec.variant_map(states):
        raise motion.PlanError(f"{sid}: {field} '{state_id}' is not a variant in states.json")
    return state_id


def single_state(shot, cfg, states):
    """State shown by HOLD / EXPLODED_VIEW: animation.state, else from_state."""
    sid = shot.get("id")
    state = cfg.get("state") or shot.get("from_state")
    if not state:
        raise motion.PlanError(f"{sid}: {cfg['template']} needs animation.state or from_state")
    if shot.get("to_state") and shot["to_state"] != state:
        raise motion.PlanError(f"{sid}: {cfg['template']} shows one state; to_state must equal '{state}'")
    return _known_state(states, state, sid, "state")


def replace_states(shot, cfg, states):
    sid = shot.get("id")
    a = cfg.get("from_state") or shot.get("from_state")
    b = cfg.get("to_state") or shot.get("to_state")
    for field, value, shot_value in (("from_state", a, shot.get("from_state")), ("to_state", b, shot.get("to_state"))):
        if not value:
            raise motion.PlanError(f"{sid}: REPLACE_PARTS needs {field}")
        if shot_value and value != shot_value:
            raise motion.PlanError(f"{sid}: animation.{field} '{value}' differs from shot {field} '{shot_value}'")
        _known_state(states, value, sid, field)
    if a == b:
        raise motion.PlanError(f"{sid}: REPLACE_PARTS from_state and to_state must differ")
    return a, b


def side_states(shot, cfg, states):
    sid = shot.get("id")
    chosen = cfg.get("states") or [s for s in (shot.get("from_state"), shot.get("to_state")) if s]
    if not isinstance(chosen, list) or len(chosen) < 2 or len(set(chosen)) != len(chosen):
        raise motion.PlanError(f"{sid}: SIDE_BY_SIDE needs a list of at least two different states")
    for state in chosen:
        _known_state(states, state, sid, "states")
    return list(chosen)


def layout_slots(shot, states):
    """[(slot_id, built variant ids, visible variant ids)] for the shot.

    Single-slot shots build every variant (hidden when inactive) so the locked
    camera is identical across shots; SIDE_BY_SIDE builds one model per state.
    """
    cfg = animation_config(shot)
    all_variants = list(spec.variant_map(states))
    if cfg["template"] == "SIDE_BY_SIDE":
        return [(state, spec.build_set(states, state), [state]) for state in side_states(shot, cfg, states)]
    if cfg["template"] == "REPLACE_PARTS":
        active = list(replace_states(shot, cfg, states))
    else:
        active = [single_state(shot, cfg, states)]
    return [(MAIN_SLOT, single_slot_variants(shot, states, active), active)]


def single_slot_variants(shot, states, active):
    """Variants built in a single-model shot: `build_variants` (M5: one continuity group,
    whose shots share a locked camera) or, by default, every variant of the project.
    Active states and their structure_from sources must be included."""
    all_variants = list(spec.variant_map(states))
    chosen = shot.get("build_variants")
    if chosen is None:
        return all_variants
    sid = shot.get("id", "(missing)")
    if not isinstance(chosen, list) or not chosen or len(set(chosen)) != len(chosen):
        raise motion.PlanError(f"{sid}: build_variants must be a non-empty list of distinct variant ids")
    unknown = [v for v in chosen if v not in all_variants]
    if unknown:
        raise motion.PlanError(f"{sid}: build_variants {unknown} are not variants in states.json")
    needed = {s2 for a in active for s2 in spec.build_set(states, a)}
    missing = sorted(needed - set(chosen))
    if missing:
        raise motion.PlanError(f"{sid}: build_variants must include {missing} (shown or inherited by the shot)")
    return [v for v in all_variants if v in chosen]


def check_camera_focus(shot, states, active):
    """camera_focus (M5 COMPONENT_CLOSEUP): component ids visible in the shot."""
    focus = shot.get("camera_focus")
    if focus is None:
        return
    sid = shot.get("id", "(missing)")
    if not isinstance(focus, list) or not focus:
        raise motion.PlanError(f"{sid}: camera_focus must be a non-empty list of component ids")
    shown = visible_component_ids(states, active)
    bad = sorted(set(focus) - shown)
    if bad:
        raise motion.PlanError(f"{sid}: camera_focus {bad} are not visible components of {active}")
    band = shot.get("camera_safe_band", 0.0)
    if isinstance(band, bool) or not isinstance(band, (int, float)) or not 0 <= band < 0.4:
        raise motion.PlanError(f"{sid}: camera_safe_band must be between 0 and 0.4")


def replace_sets(states, a, b):
    """REPLACE_PARTS moves only what differs: parts of `a` not shown in `b`, and vice versa
    (parts inherited through structure_from stay in place)."""
    shown_a, shown_b = spec.state_ids(states, a), spec.state_ids(states, b)
    return [i for i in shown_a if i not in shown_b], [i for i in shown_b if i not in shown_a]


def visible_component_ids(states, visible_states):
    """Shared parts + every part shown by the visible states."""
    ids = set(spec.shared_ids(states))
    for state in visible_states:
        ids |= set(spec.state_ids(states, state))
    return ids


def object_name(slot_id, component_id):
    return component_id if slot_id == MAIN_SLOT else f"{slot_id}.{component_id}"


def placeholder_slots(shot, states):
    """Slots with zero geometry: enough for ownership and timing checks offline."""
    layers = {}
    for variant in states.get("variants", []):
        for part in spec.variant_parts(variant):
            layers[part["id"]] = part.get("layer", 0)
    slots = {}
    for slot_id, built, _ in layout_slots(shot, states):
        ids = spec.shared_ids(states) + [i for v in built for i in spec.variant_ids(states, v)]
        slots[slot_id] = {i: motion.Component(name=object_name(slot_id, i), id=i, layer=layers.get(i, 0))
                          for i in ids}
    return slots


def _select(selector, keyword, default_ids, slot, sid, where, allowed_ids):
    if selector in (None, keyword):
        ids = list(default_ids)
    elif isinstance(selector, list) and all(isinstance(i, str) for i in selector):
        ids = list(selector)
    else:
        raise motion.PlanError(f"{sid}: {where} must be '{keyword}' or a list of component ids")
    if len(set(ids)) != len(ids):
        raise motion.PlanError(f"{sid}: {where} lists a component twice")
    bad = [i for i in ids if i not in allowed_ids]
    if bad:
        raise motion.PlanError(f"{sid}: {where} contains {bad}, which are not allowed here "
                               f"(allowed: {sorted(allowed_ids)})")
    missing = [i for i in ids if i not in slot]
    if missing:
        raise motion.PlanError(f"{sid}: {where} components {missing} were not built")
    return [slot[i] for i in ids]


CAMERA_NAME = "Camera_LOCKED"


def placeholder_camera():
    rest = {"location": (0.0, 0.0, 0.0), "ortho_scale": 1.0}
    return {"name": CAMERA_NAME, "start": rest, "end": rest}


def plan_shot(shot, states, fps, slots, camera=None):
    """Plan keyframes for one shot. slots: {slot_id: {component_id: motion.Component}}.

    camera: {"name", "start": {location, ortho_scale}, "end": {...}}, needed only by a
    SIDE_BY_SIDE intro; the validator passes a placeholder."""
    sid = shot.get("id", "(missing)")
    cfg = animation_config(shot)
    plan = motion.Plan(fps, frame_count(shot, fps))
    template = cfg["template"]
    if template != "SIDE_BY_SIDE":
        check_camera_focus(shot, states, layout_slots(shot, states)[0][2])
    elif shot.get("camera_focus") or shot.get("build_variants"):
        raise motion.PlanError(f"{sid}: camera_focus/build_variants are for single-model shots")
    try:
        if template == "REPLACE_PARTS":
            a, b = replace_states(shot, cfg, states)
            slot = slots[MAIN_SLOT]
            out_ids, in_ids = replace_sets(states, a, b)
            if not out_ids and not in_ids:
                raise motion.PlanError(f"{sid}: {a} and {b} show identical parts; nothing to replace")
            outgoing = _select((cfg.get("outgoing") or {}).get("components"), "FROM_STATE", out_ids,
                               slot, sid, "outgoing.components", set(out_ids))
            incoming = _select((cfg.get("incoming") or {}).get("components"), "TO_STATE", in_ids,
                               slot, sid, "incoming.components", set(in_ids))
            for label, chosen, full in (("outgoing", outgoing, out_ids), ("incoming", incoming, in_ids)):
                if len(chosen) != len(full):
                    raise motion.PlanError(f"{sid}: {label}.components must include every component of its "
                                           f"state (missing {sorted(set(full) - {c.id for c in chosen})})")
            motion.plan_replace_parts(plan, outgoing, incoming, cfg)
        elif template == "EXPLODED_VIEW":
            state = single_state(shot, cfg, states)
            slot = slots[MAIN_SLOT]
            own = spec.state_ids(states, state)
            allowed = set(own) | set(spec.shared_ids(states))
            comps = _select(cfg.get("components"), "STATE", own, slot, sid, "components", allowed)
            unknown = sorted(set(cfg.get("per_component") or {}) - {c.id for c in comps})
            if unknown:
                raise motion.PlanError(f"{sid}: per_component names {unknown}, which are not exploded components")
            motion.plan_exploded_view(plan, comps, cfg)
        elif template == "HOLD":
            state = single_state(shot, cfg, states)
            slot = slots[MAIN_SLOT]
            own = spec.state_ids(states, state)
            allowed = set(own) | set(spec.shared_ids(states))

            def names_for(selector):
                return [c.name for c in _select(selector, "STATE", own, slot, sid, "highlight.components", allowed)]
            motion.plan_highlight_only(plan, cfg, motion.HOLD_DEFAULTS, names_for, "HOLD")
            label = cfg.get("label")
            if label is not None:   # M5.5: caption of a single model (sequential comparisons)
                if not isinstance(label, str) or not label.strip() or len(label) > 40:
                    raise motion.PlanError(f"{sid}: label must be 1-40 characters")
                if float(shot.get("camera_safe_band", 0.0)) < 0.08:
                    raise motion.PlanError(f"{sid}: a HOLD label needs camera_safe_band >= 0.08 (it sits in that band)")
        elif template == "SIDE_BY_SIDE":
            chosen = side_states(shot, cfg, states)
            gap = cfg.get("gap_ratio", motion.SIDE_BY_SIDE_DEFAULTS["gap_ratio"])
            band = cfg.get("label_band", motion.SIDE_BY_SIDE_DEFAULTS["label_band"])
            if isinstance(gap, bool) or not isinstance(gap, (int, float)) or gap <= 0:
                raise motion.PlanError(f"{sid}: gap_ratio must be > 0")
            if isinstance(band, bool) or not isinstance(band, (int, float)) or not 0 <= band < 0.5:
                raise motion.PlanError(f"{sid}: label_band must be between 0 and 0.5")
            if cfg.get("layout", "ROW") not in ("ROW", "STACK"):
                raise motion.PlanError(f"{sid}: layout must be ROW or STACK")
            if cfg.get("layout") == "STACK" and cfg.get("intro"):
                raise motion.PlanError(f"{sid}: intro is only supported with layout ROW")
            labels = cfg.get("labels")
            if labels is not None:
                if not isinstance(labels, dict) or not labels:
                    raise motion.PlanError(f"{sid}: labels must map state ids to caption text")
                for state_id, text in labels.items():
                    if state_id not in chosen:
                        raise motion.PlanError(f"{sid}: label for '{state_id}', which is not in this comparison")
                    if not isinstance(text, str) or not text.strip() or len(text) > 40:
                        raise motion.PlanError(f"{sid}: label for '{state_id}' must be 1-40 characters")
                if band < 0.08:
                    raise motion.PlanError(f"{sid}: labels need label_band >= 0.08")

            def names_for(selector):
                if selector == "DIFFERENCES":
                    return [slots[s][i].name for s in chosen for i in spec.state_ids(states, s)]
                names = []
                for s in chosen:
                    own = spec.state_ids(states, s)
                    allowed = set(own) | set(spec.shared_ids(states))
                    picked = [i for i in selector if i in slots[s]] if isinstance(selector, list) else selector
                    names += [c.name for c in _select(picked, "STATE", own, slots[s], sid,
                                                      "highlight.components", allowed)]
                return names
            motion.plan_highlight_only(plan, cfg, motion.SIDE_BY_SIDE_DEFAULTS, names_for, "SIDE_BY_SIDE")
            intro = cfg.get("intro")
            if intro:
                origin = intro.get("from_state") if isinstance(intro, dict) else None
                if origin not in chosen:
                    raise motion.PlanError(f"{sid}: intro.from_state must be one of {chosen}")
                # Only parts the state actually shows: a structure_from slot also builds the
                # source variant's covering, which stays hidden and must never be faded in.
                fading = [c.name for s in chosen if s != origin
                          for cid, c in slots[s].items() if cid in visible_component_ids(states, [s])]
                end = motion.plan_intro(plan, intro, camera or placeholder_camera(), fading)
                start = plan.markers.get("highlight_start")
                if start is not None and start < end:
                    raise motion.PlanError(f"{sid}: highlight starts at frame {start}, before the intro "
                                           f"ends (frame {end}); start it after the camera settles")
    except motion.PlanError as e:
        message = str(e)
        raise motion.PlanError(message if message.startswith(f"{sid}:") else f"{sid}: {message}") from None
    return plan


def key_still_frame(shot, time_seconds, fps):
    frames = frame_count(shot, fps)
    frame = motion.frame_at(time_seconds, fps)
    if not 1 <= frame <= frames or time_seconds < 0 or math.isnan(time_seconds):
        raise motion.PlanError(f"{shot.get('id')}: key still at {time_seconds}s is outside the shot")
    return frame
