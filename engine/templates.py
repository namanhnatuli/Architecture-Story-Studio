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
        return [(state, [state], [state]) for state in side_states(shot, cfg, states)]
    if cfg["template"] == "REPLACE_PARTS":
        active = list(replace_states(shot, cfg, states))
    else:
        active = [single_state(shot, cfg, states)]
    return [(MAIN_SLOT, all_variants, active)]


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


def plan_shot(shot, states, fps, slots):
    """Plan keyframes for one shot. slots: {slot_id: {component_id: motion.Component}}."""
    sid = shot.get("id", "(missing)")
    cfg = animation_config(shot)
    plan = motion.Plan(fps, frame_count(shot, fps))
    template = cfg["template"]
    try:
        if template == "REPLACE_PARTS":
            a, b = replace_states(shot, cfg, states)
            slot = slots[MAIN_SLOT]
            out_ids, in_ids = spec.variant_ids(states, a), spec.variant_ids(states, b)
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
            own = spec.variant_ids(states, state)
            allowed = set(own) | set(spec.shared_ids(states))
            comps = _select(cfg.get("components"), "STATE", own, slot, sid, "components", allowed)
            unknown = sorted(set(cfg.get("per_component") or {}) - {c.id for c in comps})
            if unknown:
                raise motion.PlanError(f"{sid}: per_component names {unknown}, which are not exploded components")
            motion.plan_exploded_view(plan, comps, cfg)
        elif template == "HOLD":
            state = single_state(shot, cfg, states)
            slot = slots[MAIN_SLOT]
            own = spec.variant_ids(states, state)
            allowed = set(own) | set(spec.shared_ids(states))

            def names_for(selector):
                return [c.name for c in _select(selector, "STATE", own, slot, sid, "highlight.components", allowed)]
            motion.plan_highlight_only(plan, cfg, motion.HOLD_DEFAULTS, names_for, "HOLD")
        elif template == "SIDE_BY_SIDE":
            chosen = side_states(shot, cfg, states)
            gap = cfg.get("gap_ratio", motion.SIDE_BY_SIDE_DEFAULTS["gap_ratio"])
            band = cfg.get("label_band", motion.SIDE_BY_SIDE_DEFAULTS["label_band"])
            if isinstance(gap, bool) or not isinstance(gap, (int, float)) or gap <= 0:
                raise motion.PlanError(f"{sid}: gap_ratio must be > 0")
            if isinstance(band, bool) or not isinstance(band, (int, float)) or not 0 <= band < 0.5:
                raise motion.PlanError(f"{sid}: label_band must be between 0 and 0.5")

            def names_for(selector):
                if selector == "DIFFERENCES":
                    return [slots[s][i].name for s in chosen for i in spec.variant_ids(states, s)]
                names = []
                for s in chosen:
                    own = spec.variant_ids(states, s)
                    allowed = set(own) | set(spec.shared_ids(states))
                    picked = [i for i in selector if i in slots[s]] if isinstance(selector, list) else selector
                    names += [c.name for c in _select(picked, "STATE", own, slots[s], sid,
                                                      "highlight.components", allowed)]
                return names
            motion.plan_highlight_only(plan, cfg, motion.SIDE_BY_SIDE_DEFAULTS, names_for, "SIDE_BY_SIDE")
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
