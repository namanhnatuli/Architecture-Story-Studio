"""Deterministic, bpy-free motion planning for architectural transformation templates.

A template turns a JSON-compatible config plus component rest transforms into a
``Plan``: explicit keyframes per object and channel. engine/animate.py writes the
same keys into Blender, and ``Plan.sample`` evaluates them here with the same
easing maths Blender uses, so tests and the validator can check timing and
start/end transforms without Blender, the viewport or interpolation defaults.

Frames are shot-local: the first frame of every shot is 1.
"""
import copy
import math
from dataclasses import dataclass

LOC = "location"
ROT = "rotation_euler"
SCALE = "scale"     # M7: the annotation rig of a push-in shot
TRANSPARENCY = '["ass_transparency"]'
HIGHLIGHT = '["ass_highlight"]'
TINT = '["ass_tint"]'   # g-r5: how far a part's glow leans towards the accent colour (one value per part and shot)
HIDE = "hide_render"  # also mirrored to hide_viewport when applied in Blender


class PlanError(ValueError):
    """Invalid template configuration, or timing that does not fit the shot."""


# Easing name -> (Blender keyframe interpolation, Blender easing).
EASINGS = {
    "LINEAR": ("LINEAR", "AUTO"),
    "SMOOTH": ("SINE", "EASE_IN_OUT"),
    "EASE_IN_OUT": ("CUBIC", "EASE_IN_OUT"),
    "EASE_IN": ("CUBIC", "EASE_IN"),
    "EASE_OUT": ("CUBIC", "EASE_OUT"),
    "CONSTANT": ("CONSTANT", "AUTO"),
}


def ease(name, t):
    """Normalised easing curve, identical to Blender's Penner implementations."""
    t = min(1.0, max(0.0, t))
    if name == "LINEAR":
        return t
    if name == "SMOOTH":
        return -(math.cos(math.pi * t) - 1.0) / 2.0
    if name == "EASE_IN":
        return t ** 3
    if name == "EASE_OUT":
        return (t - 1.0) ** 3 + 1.0
    if name == "EASE_IN_OUT":
        return 4.0 * t ** 3 if t < 0.5 else ((2.0 * t - 2.0) ** 3) / 2.0 + 1.0
    if name == "CONSTANT":
        return 0.0
    raise PlanError(f"unknown easing '{name}' (use one of: {', '.join(EASINGS)})")


def frame_at(seconds, fps):
    """Shot-local frame for a time in seconds (round half up, never banker's rounding)."""
    return 1 + int(math.floor(seconds * fps + 0.5))


@dataclass(frozen=True)
class Key:
    frame: int
    value: tuple
    easing: str = "LINEAR"  # easing of the segment that starts at this key


@dataclass(frozen=True)
class Component:
    """What a template needs to know about one object; geometry comes from the builder."""
    name: str                                   # Blender object name, unique in the shot
    id: str                                     # stable component_id from states.json
    location: tuple = (0.0, 0.0, 0.0)           # rest location (parent/slot space)
    rotation: tuple = (0.0, 0.0, 0.0)           # rest rotation_euler, radians
    center: tuple = (0.0, 0.0, 0.0)             # rest bounds centre (slot space)
    layer: int = 0                              # assembly layer: 0 is built first
    hint: tuple = None                          # builder's suggested explode direction


class Plan:
    def __init__(self, fps, frame_count):
        if frame_count < 2:
            raise PlanError("a shot needs at least 2 frames")
        self.fps = fps
        self.frame_count = frame_count
        self.tracks = {}   # object name -> channel -> {frame: Key}
        self.markers = {}  # named shot-local frames for QA/stills, e.g. "exploded_hold"

    def frame(self, seconds):
        return frame_at(seconds, self.fps)

    def key(self, name, channel, frame, value, easing="LINEAR"):
        if easing not in EASINGS:
            raise PlanError(f"unknown easing '{easing}' (use one of: {', '.join(EASINGS)})")
        if frame < 1:
            raise PlanError(f"{name}: {channel} keyframe {frame} is before the first frame")
        if frame > self.frame_count:
            raise PlanError(
                f"{name}: timing needs frame {frame} ({(frame - 1) / self.fps:.2f}s) for {channel} but the "
                f"shot has {self.frame_count} frames ({self.frame_count / self.fps:.2f}s); "
                "shorten move/stagger/hold times or lengthen the shot")
        if not isinstance(value, (tuple, list)):
            value = (value,)
        self.tracks.setdefault(name, {}).setdefault(channel, {})[frame] = Key(
            frame, tuple(float(v) for v in value), easing)

    def keys(self, name, channel):
        return [k for _, k in sorted(self.tracks.get(name, {}).get(channel, {}).items())]

    def channels(self, name):
        return sorted(self.tracks.get(name, {}))

    def sample(self, name, channel, frame):
        keys = self.keys(name, channel)
        if not keys:
            return None
        if frame <= keys[0].frame:
            return keys[0].value
        for a, b in zip(keys, keys[1:]):
            if a.frame <= frame < b.frame:
                if a.easing == "CONSTANT":
                    return a.value
                t = ease(a.easing, (frame - a.frame) / (b.frame - a.frame))
                return tuple(x + (y - x) * t for x, y in zip(a.value, b.value))
        return keys[-1].value

    def require_fits(self, template, end_seconds, hold_end_seconds):
        needed = self.frame(end_seconds) + int(math.floor(hold_end_seconds * self.fps + 0.5))
        if needed > self.frame_count:
            raise PlanError(
                f"{template} timing needs {needed} frames ({needed / self.fps:.2f}s incl. final hold) "
                f"but the shot has {self.frame_count} ({self.frame_count / self.fps:.2f}s); "
                "shorten move/stagger/hold times or lengthen the shot")


# ---------------------------------------------------------------- vector helpers
def _add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def _sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def _mul(a, s):
    return tuple(x * s for x in a)


def _len(a):
    return math.sqrt(sum(x * x for x in a))


def _unit(a, where):
    n = _len(a)
    if n < 1e-9:
        raise PlanError(f"{where}: direction vector must not be zero")
    return _mul(a, 1.0 / n)


def centroid(components):
    if not components:
        return (0.0, 0.0, 0.0)
    return _mul(tuple(sum(c.center[i] for c in components) for i in range(3)), 1.0 / len(components))


NAMED_DIRECTIONS = {
    "UP": (0.0, 0.0, 1.0), "FROM_ABOVE": (0.0, 0.0, 1.0),
    "DOWN": (0.0, 0.0, -1.0), "FROM_BELOW": (0.0, 0.0, -1.0),
    "LEFT": (-1.0, 0.0, 0.0), "RIGHT": (1.0, 0.0, 0.0),
    "FRONT": (0.0, -1.0, 0.0), "BACK": (0.0, 1.0, 0.0),
}
COMPUTED_DIRECTIONS = ("OUTWARD", "OUTWARD_UP", "RADIAL", "HINT")


def resolve_direction(spec, comp, group_center):
    """Unit vector for a direction spec: [x, y, z], a named axis or a computed mode.

    OUTWARD is horizontal from the group centre; OUTWARD_UP adds an equal upward
    component; RADIAL is 3D from the centre; HINT uses the builder's hint.
    A component sitting on the centre falls back to UP.
    """
    where = f"{comp.id} direction"
    if isinstance(spec, (list, tuple)):
        if len(spec) != 3:
            raise PlanError(f"{where}: vector needs 3 numbers, got {spec!r}")
        return _unit(tuple(float(v) for v in spec), where)
    name = str(spec).upper()
    if name in NAMED_DIRECTIONS:
        return NAMED_DIRECTIONS[name]
    if name == "HINT":
        if comp.hint is not None:
            return _unit(tuple(comp.hint), where)
        name = "RADIAL"
    if name in ("OUTWARD", "OUTWARD_UP", "RADIAL"):
        d = _sub(comp.center, group_center)
        if name != "RADIAL":
            d = (d[0], d[1], 0.0)
        if _len(d) < 1e-6:
            return (0.0, 0.0, 1.0)
        d = _unit(d, where)
        return _unit(_add(d, (0.0, 0.0, 1.0)), where) if name == "OUTWARD_UP" else d
    raise PlanError(f"{where}: unknown direction '{spec}' (use [x,y,z], "
                    f"{', '.join(NAMED_DIRECTIONS)}, {', '.join(COMPUTED_DIRECTIONS)})")


ORDERS = ("LISTED", "ASSEMBLY", "DISASSEMBLY", "BOTTOM_UP", "TOP_DOWN")


def stagger_groups(components, order, stagger_by):
    """Ordered groups that start together; LAYER groups neighbours sharing an assembly layer."""
    index = {c.name: i for i, c in enumerate(components)}
    keys = {
        "LISTED": lambda c: index[c.name],
        "ASSEMBLY": lambda c: (c.layer, index[c.name]),
        "DISASSEMBLY": lambda c: (-c.layer, index[c.name]),
        "BOTTOM_UP": lambda c: (round(c.center[2], 6), index[c.name]),
        "TOP_DOWN": lambda c: (-round(c.center[2], 6), index[c.name]),
    }
    if order not in keys:
        raise PlanError(f"unknown order '{order}' (use one of: {', '.join(ORDERS)})")
    seq = sorted(components, key=keys[order])
    if stagger_by == "COMPONENT":
        return [[c] for c in seq]
    if stagger_by != "LAYER":
        raise PlanError(f"unknown stagger_by '{stagger_by}' (use LAYER or COMPONENT)")
    groups = []
    for c in seq:
        if groups and groups[-1][0].layer == c.layer:
            groups[-1].append(c)
        else:
            groups.append([c])
    return groups


# ---------------------------------------------------------------- config merging
def merge_config(defaults, cfg, where, free_form=("per_component", "highlight", "components", "center", "states")):
    """Defaults + overrides; unknown keys are errors so typos never pass silently."""
    out = copy.deepcopy(defaults)
    for key, value in (cfg or {}).items():
        if key not in defaults:
            raise PlanError(f"{where}: unknown option '{key}' (allowed: {', '.join(sorted(defaults))})")
        if isinstance(defaults[key], dict) and key not in free_form:
            out[key] = merge_config(defaults[key], value, f"{where}.{key}", free_form)
        else:
            out[key] = copy.deepcopy(value)
    return out


def _number(cfg, key, where, minimum=0.0, positive=False, maximum=None):
    value = cfg[key]
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise PlanError(f"{where}.{key} must be a number, got {value!r}")
    if value < minimum or (positive and value <= 0) or (maximum is not None and value > maximum):
        bound = f"> {minimum}" if positive else f">= {minimum}"
        if maximum is not None:
            bound += f" and <= {maximum}"
        raise PlanError(f"{where}.{key} must be {bound}, got {value}")
    return float(value)


def _rotation(cfg, where):
    rot = cfg.get("rotation_degrees", [0, 0, 0])
    if not isinstance(rot, (list, tuple)) or len(rot) != 3:
        raise PlanError(f"{where}.rotation_degrees needs 3 numbers")
    return tuple(math.radians(float(v)) for v in rot)


def _component_options(group_cfg, comp, where):
    """Per-component overrides of direction/distance/rotation (and lift for outgoing)."""
    allowed = {"direction", "distance", "rotation_degrees", "lift"}
    override = (group_cfg.get("per_component") or {}).get(comp.id, {})
    unknown = set(override) - allowed
    if unknown:
        raise PlanError(f"{where}.per_component.{comp.id}: unknown option(s) {sorted(unknown)}")
    merged = {k: group_cfg.get(k) for k in allowed if k in group_cfg}
    merged.update(override)
    return merged


# ---------------------------------------------------------------- highlight pulse
PULSE_DEFAULTS = {"components": "STATE", "start_seconds": 0.5, "rise_seconds": 0.3,
                  "hold_seconds": 1.0, "fall_seconds": 0.4, "strength": 0.6}


def plan_pulse(plan, names, start, rise, hold, fall, strength, where="highlight"):
    """Highlight ramps 0 -> strength -> 0; no other channel is touched."""
    last = plan.frame_count
    f0, f1 = plan.frame(start), plan.frame(start + rise)
    f2, f3 = plan.frame(start + rise + hold), plan.frame(start + rise + hold + fall)
    if f3 > last:
        raise PlanError(f"{where}: pulse ends at frame {f3}, after the last frame {last}")
    for name in names:
        plan.key(name, HIGHLIGHT, 1, 0.0)
        plan.key(name, HIGHLIGHT, f0, 0.0, "SMOOTH")
        plan.key(name, HIGHLIGHT, f1, strength, "LINEAR")
        plan.key(name, HIGHLIGHT, f2, strength, "SMOOTH")
        plan.key(name, HIGHLIGHT, f3, 0.0)
        plan.key(name, HIGHLIGHT, last, 0.0)
    return f0, f3


# HOLD only: parts that cover the highlighted ones (deck planks over stringers) turn
# see-through on the same envelope as the glow, then return; nothing moves.
GHOST_DEFAULTS = {"ghost": None, "ghost_transparency": 0.7}


def merged_pulse(cfg, where, default_components, extra=None):
    defaults = dict(PULSE_DEFAULTS, components=default_components, **(extra or {}))
    c = merge_config(defaults, cfg, where)
    for key in ("start_seconds", "rise_seconds", "hold_seconds", "fall_seconds"):
        _number(c, key, where)
    _number(c, "strength", where, maximum=1.0)
    return c


# ---------------------------------------------------------------- REPLACE_PARTS
REPLACE_DEFAULTS = {
    "template": "REPLACE_PARTS", "from_state": None, "to_state": None, "duration_seconds": None,
    "easing": "SMOOTH", "hold_start_seconds": 0.5, "hold_end_seconds": 1.0,
    "outgoing": {
        "components": "FROM_STATE", "direction": "OUTWARD_UP", "distance": 3.0,
        "lift": 0.0, "lift_seconds": 0.4, "move_seconds": 1.2,
        "stagger_seconds": 0.15, "stagger_by": "LAYER", "order": "DISASSEMBLY",
        "rotation_degrees": [0, 0, 0], "fade": True, "fade_start": 0.3,
        "hide_when_done": True, "easing": None, "per_component": {},
    },
    "incoming": {
        "components": "TO_STATE", "direction": "FROM_ABOVE", "distance": 4.0, "move_seconds": 1.4,
        "stagger_seconds": 0.2, "stagger_by": "LAYER", "order": "ASSEMBLY",
        "rotation_degrees": [0, 0, 0], "fade": True, "fade_end": 0.6,
        "overlap_seconds": 0.3, "start_seconds": None, "easing": "EASE_OUT", "per_component": {},
    },
}


def plan_replace_parts(plan, outgoing, incoming, cfg):
    """Outgoing parts lift/move away (optionally fading, then hidden); incoming parts
    arrive from an offset and land exactly on their rest transforms; the rest of the
    scene is never keyed."""
    c = merge_config(REPLACE_DEFAULTS, cfg, "REPLACE_PARTS")
    og, ic = c["outgoing"], c["incoming"]
    hold_start = _number(c, "hold_start_seconds", "REPLACE_PARTS")
    hold_end = _number(c, "hold_end_seconds", "REPLACE_PARTS")
    for where, g in (("outgoing", og), ("incoming", ic)):
        _number(g, "distance", where)
        _number(g, "move_seconds", where, positive=True)
        _number(g, "stagger_seconds", where)
    _number(og, "lift", "outgoing")
    _number(og, "lift_seconds", "outgoing")
    fade_start = _number(og, "fade_start", "outgoing", maximum=0.99)
    fade_end = _number(ic, "fade_end", "incoming", maximum=1.0)
    out_ease = og["easing"] or c["easing"]
    in_ease = ic["easing"] or c["easing"]
    last = plan.frame_count

    out_center = centroid(outgoing)
    out_end = hold_start
    for gi, group in enumerate(stagger_groups(outgoing, og["order"], og["stagger_by"])):
        start = hold_start + gi * og["stagger_seconds"]
        for comp in group:
            o = _component_options(og, comp, "outgoing")
            direction = resolve_direction(o["direction"], comp, out_center)
            lift = float(o.get("lift") or 0.0)
            lift_seconds = og["lift_seconds"] if lift > 0 else 0.0
            f0 = plan.frame(start)
            f1 = plan.frame(start + lift_seconds)
            f2 = plan.frame(start + lift_seconds + og["move_seconds"])
            lifted = _add(comp.location, (0.0, 0.0, lift))
            away = _add(lifted, _mul(direction, float(o["distance"])))
            n = comp.name
            plan.key(n, LOC, 1, comp.location)
            plan.key(n, LOC, f0, comp.location, "SMOOTH" if f1 > f0 else out_ease)
            if f1 > f0:
                plan.key(n, LOC, f1, lifted, out_ease)
            plan.key(n, LOC, f2, away)
            plan.key(n, LOC, last, away)
            rot = _rotation(o, f"outgoing.{comp.id}")
            if any(abs(r) > 1e-12 for r in rot):
                plan.key(n, ROT, 1, comp.rotation)
                plan.key(n, ROT, f1, comp.rotation, out_ease)
                plan.key(n, ROT, f2, _add(comp.rotation, rot))
                plan.key(n, ROT, last, _add(comp.rotation, rot))
            if og["fade"]:
                ff = f1 + int(math.floor(fade_start * (f2 - f1) + 0.5))
                plan.key(n, TRANSPARENCY, 1, 0.0)
                plan.key(n, TRANSPARENCY, ff, 0.0, "SMOOTH")
                plan.key(n, TRANSPARENCY, f2, 1.0)
                plan.key(n, TRANSPARENCY, last, 1.0)
            if og["hide_when_done"]:
                if f2 >= last:
                    raise PlanError(f"outgoing {comp.id} must finish before the last frame to be hidden")
                plan.key(n, HIDE, 1, 0.0, "CONSTANT")
                plan.key(n, HIDE, f2 + 1, 1.0, "CONSTANT")
            out_end = max(out_end, start + lift_seconds + og["move_seconds"])

    if ic["start_seconds"] is not None:
        in_start = _number(ic, "start_seconds", "incoming")
    elif outgoing:
        in_start = max(hold_start, out_end - _number(ic, "overlap_seconds", "incoming"))
    else:
        in_start = hold_start
    in_center = centroid(incoming)
    in_end = in_start
    for gi, group in enumerate(stagger_groups(incoming, ic["order"], ic["stagger_by"])):
        start = in_start + gi * ic["stagger_seconds"]
        for comp in group:
            o = _component_options(ic, comp, "incoming")
            direction = resolve_direction(o["direction"], comp, in_center)
            f0, f1 = plan.frame(start), plan.frame(start + ic["move_seconds"])
            begin = _add(comp.location, _mul(direction, float(o["distance"])))
            n = comp.name
            plan.key(n, LOC, 1, begin)
            plan.key(n, LOC, f0, begin, in_ease)
            plan.key(n, LOC, f1, comp.location)
            plan.key(n, LOC, last, comp.location)
            rot = _rotation(o, f"incoming.{comp.id}")
            if any(abs(r) > 1e-12 for r in rot):
                plan.key(n, ROT, 1, _add(comp.rotation, rot))
                plan.key(n, ROT, f0, _add(comp.rotation, rot), in_ease)
                plan.key(n, ROT, f1, comp.rotation)
                plan.key(n, ROT, last, comp.rotation)
            if ic["fade"]:
                fe = f0 + max(1, int(math.floor(fade_end * (f1 - f0) + 0.5)))
                plan.key(n, TRANSPARENCY, 1, 1.0)
                plan.key(n, TRANSPARENCY, f0, 1.0, "SMOOTH")
                plan.key(n, TRANSPARENCY, min(fe, f1), 0.0)
                plan.key(n, TRANSPARENCY, last, 0.0)
            plan.key(n, HIDE, 1, 1.0 if f0 > 1 else 0.0, "CONSTANT")
            plan.key(n, HIDE, f0, 0.0, "CONSTANT")
            in_end = max(in_end, start + ic["move_seconds"])

    plan.require_fits("REPLACE_PARTS", in_end, hold_end)
    plan.markers.update({
        "outgoing_start": plan.frame(hold_start), "outgoing_end": plan.frame(out_end),
        "incoming_start": plan.frame(in_start), "incoming_end": plan.frame(in_end),
        "middle": plan.frame((out_end + in_start) / 2.0),
    })
    return plan


# ---------------------------------------------------------------- EXPLODED_VIEW
EXPLODED_DEFAULTS = {
    "template": "EXPLODED_VIEW", "state": None, "duration_seconds": None,
    "components": "STATE", "center": "AUTO", "direction_mode": "HINT", "distance": 1.0,
    "per_component": {}, "sequence": "SEQUENTIAL", "stagger_seconds": 0.12,
    "stagger_by": "LAYER", "order": "DISASSEMBLY",
    "hold_start_seconds": 0.4, "explode_seconds": 1.0, "hold_seconds": 1.6,
    "return_seconds": 1.0, "hold_end_seconds": 0.2, "easing": "SMOOTH", "highlight": None,
}
EXPLODED_HIGHLIGHT_DEFAULTS = {"components": "ALL", "mode": "SIMULTANEOUS",
                               "strength": 0.6, "fade_seconds": 0.25}


def plan_exploded_view(plan, components, cfg):
    """Components move out along per-component vectors, hold (optionally highlighted)
    and return in reverse order to exactly their rest transforms."""
    c = merge_config(EXPLODED_DEFAULTS, cfg, "EXPLODED_VIEW")
    w = "EXPLODED_VIEW"
    hold_start = _number(c, "hold_start_seconds", w)
    explode = _number(c, "explode_seconds", w, positive=True)
    hold = _number(c, "hold_seconds", w)
    back = _number(c, "return_seconds", w, positive=True)
    hold_end = _number(c, "hold_end_seconds", w)
    _number(c, "distance", w)
    if c["sequence"] not in ("SEQUENTIAL", "SIMULTANEOUS"):
        raise PlanError(f"{w}.sequence must be SEQUENTIAL or SIMULTANEOUS")
    stagger = _number(c, "stagger_seconds", w) if c["sequence"] == "SEQUENTIAL" else 0.0
    if c["center"] == "AUTO":
        center = centroid(components)
    elif isinstance(c["center"], (list, tuple)) and len(c["center"]) == 3:
        center = tuple(float(v) for v in c["center"])
    else:
        raise PlanError(f"{w}.center must be AUTO or [x, y, z]")
    last = plan.frame_count
    groups = stagger_groups(components, c["order"], c["stagger_by"])
    exploded = {}
    for gi, group in enumerate(groups):
        start = hold_start + gi * stagger
        for comp in group:
            o = dict(direction=c["direction_mode"], distance=c["distance"])
            o.update(_component_options({"per_component": c["per_component"]}, comp, w))
            direction = resolve_direction(o["direction"], comp, center)
            out = _add(comp.location, _mul(direction, float(o["distance"])))
            exploded[comp.name] = out
            plan.key(comp.name, LOC, 1, comp.location)
            plan.key(comp.name, LOC, plan.frame(start), comp.location, c["easing"])
            plan.key(comp.name, LOC, plan.frame(start + explode), out)
    explode_end = hold_start + (len(groups) - 1) * stagger + explode
    return_start = explode_end + hold
    for gi, group in enumerate(reversed(groups)):
        start = return_start + gi * stagger
        for comp in group:
            plan.key(comp.name, LOC, plan.frame(start), exploded[comp.name], c["easing"])
            plan.key(comp.name, LOC, plan.frame(start + back), comp.location)
            plan.key(comp.name, LOC, last, comp.location)
    return_end = return_start + (len(groups) - 1) * stagger + back
    plan.require_fits(w, return_end, hold_end)

    if c["highlight"]:
        h = merge_config(EXPLODED_HIGHLIGHT_DEFAULTS, c["highlight"], f"{w}.highlight")
        fade = _number(h, "fade_seconds", f"{w}.highlight")
        strength = _number(h, "strength", f"{w}.highlight", maximum=1.0)
        by_id = {comp.id: comp.name for comp in components}
        ids = list(by_id) if h["components"] == "ALL" else list(h["components"])
        unknown = [i for i in ids if i not in by_id]
        if unknown:
            raise PlanError(f"{w}.highlight: {unknown} are not exploded components")
        if h["mode"] == "SIMULTANEOUS":
            windows = [(explode_end, hold, ids)]
        elif h["mode"] == "SEQUENTIAL":
            step = hold / max(1, len(ids))
            windows = [(explode_end + i * step, step, [cid]) for i, cid in enumerate(ids)]
        else:
            raise PlanError(f"{w}.highlight.mode must be SIMULTANEOUS or SEQUENTIAL")
        for start, length, chunk in windows:
            if length < 2 * fade:
                raise PlanError(f"{w}.highlight: window {length:.2f}s is shorter than 2 x fade_seconds")
            plan_pulse(plan, [by_id[i] for i in chunk], start, fade, length - 2 * fade, fade,
                       strength, f"{w}.highlight")
    plan.markers.update({
        "explode_start": plan.frame(hold_start), "explode_end": plan.frame(explode_end),
        "exploded_hold": plan.frame(explode_end + hold / 2.0),
        "return_start": plan.frame(return_start), "return_end": plan.frame(return_end),
    })
    return plan


# ---------------------------------------------------------------- fade twins
FADE_SUFFIX = "__fade"
FADE_EPS = 1e-6


def split_fades(plan, suffix=FADE_SUFFIX):
    """Give every fading object a twin that is rendered only while partly transparent.

    Eevee's dithered transparency is noisy mid-fade, while blended transparency is
    clean but shades opaque surfaces slightly differently (a visible pop at shot
    cuts). With twins, the original (dithered) renders whenever the part is opaque
    and the twin (blended) only while 0 < transparency < 1, so held frames are
    unchanged. Twins copy the transforms; visibility windows are complementary.
    Returns {original name: twin name}.
    """
    twins = {}
    for name in sorted(plan.tracks):
        if TRANSPARENCY not in plan.channels(name) or name.endswith(suffix):
            continue
        twin = name + suffix
        for channel in (LOC, ROT, TRANSPARENCY):
            for k in plan.keys(name, channel):
                plan.key(twin, channel, k.frame, k.value, k.easing)
        orig_vis, twin_vis = [], []
        for f in range(1, plan.frame_count + 1):
            t = plan.sample(name, TRANSPARENCY, f)[0]
            hidden = plan.sample(name, HIDE, f)
            shown = hidden is None or hidden[0] < 0.5
            orig_vis.append(shown and t <= FADE_EPS)
            twin_vis.append(shown and FADE_EPS < t < 1.0 - FADE_EPS)
        for target, vis in ((name, orig_vis), (twin, twin_vis)):
            plan.tracks.get(target, {}).pop(HIDE, None)
            previous = None
            for f, v in enumerate(vis, start=1):
                if v != previous:
                    plan.key(target, HIDE, f, 0.0 if v else 1.0, "CONSTANT")
                    previous = v
        twins[name] = twin
    return twins


# ---------------------------------------------------------------- HOLD / SIDE_BY_SIDE
HOLD_DEFAULTS = {"template": "HOLD", "state": None, "duration_seconds": None, "highlight": None, "label": None,
                 "label_position": None, "camera_move": None}
# M7: a slow push-in on a single-model HOLD: it starts on the locked framing of the shot's
# continuity group and ends `amount` closer (orthographic scale), drifting towards `focus`.
CAMERA_MOVE_DEFAULTS = {"type": "PUSH_IN", "amount": 0.1, "focus": None, "easing": "SMOOTH"}
SIDE_BY_SIDE_DEFAULTS = {"template": "SIDE_BY_SIDE", "states": None, "duration_seconds": None,
                         "gap_ratio": 0.35, "label_band": 0.12, "highlight": None, "intro": None, "labels": None,
                         "layout": "ROW", "label_position": None}
INTRO_DEFAULTS = {"from_state": None, "seconds": 1.5, "easing": "SMOOTH", "fade_start": 0.35, "fade_end": 0.9}
ORTHO = "data.ortho_scale"  # camera data channel (orthographic scale)


def plan_intro(plan, cfg, camera, fade_names):
    """SIDE_BY_SIDE intro: start on the single-model framing of `from_state` (matching the
    previous shot exactly) and ease the camera out to the comparison framing while the
    other models fade in. Models never move, so spatial continuity is preserved."""
    c = merge_config(INTRO_DEFAULTS, cfg, "SIDE_BY_SIDE.intro")
    seconds = _number(c, "seconds", "SIDE_BY_SIDE.intro", positive=True)
    a = _number(c, "fade_start", "SIDE_BY_SIDE.intro", maximum=1.0)
    b = _number(c, "fade_end", "SIDE_BY_SIDE.intro", maximum=1.0)
    if b <= a:
        raise PlanError("SIDE_BY_SIDE.intro.fade_end must be greater than fade_start")
    end = plan.frame(seconds)
    if end >= plan.frame_count:
        raise PlanError(f"SIDE_BY_SIDE.intro ({seconds}s) must end before the shot does")
    last = plan.frame_count
    name = camera["name"]
    for channel, key in ((LOC, "location"), (ORTHO, "ortho_scale")):
        plan.key(name, channel, 1, camera["start"][key], c["easing"])
        plan.key(name, channel, end, camera["end"][key])
        plan.key(name, channel, last, camera["end"][key])
    f0, f1 = plan.frame(seconds * a), plan.frame(seconds * b)
    for n in fade_names:
        plan.key(n, TRANSPARENCY, 1, 1.0)
        plan.key(n, TRANSPARENCY, f0, 1.0, "SMOOTH")
        plan.key(n, TRANSPARENCY, max(f1, f0 + 1), 0.0)
        plan.key(n, TRANSPARENCY, last, 0.0)
    plan.markers.update({"intro_end": end})
    return end


def plan_camera_move(plan, cfg, camera):
    """HOLD camera_move: the camera eases from its start keys (the locked framing) to its end keys."""
    c = merge_config(CAMERA_MOVE_DEFAULTS, cfg, "HOLD.camera_move", free_form=("focus",))
    if c["type"] != "PUSH_IN":
        raise PlanError(f"HOLD.camera_move.type must be PUSH_IN, got {c['type']!r}")
    _number(c, "amount", "HOLD.camera_move", minimum=0.02, maximum=0.3)
    last = plan.frame_count
    for channel, key in ((LOC, "location"), (ORTHO, "ortho_scale")):
        plan.key(camera["name"], channel, 1, camera["start"][key], c["easing"])
        plan.key(camera["name"], channel, last, camera["end"][key])
    plan.markers["camera_move_end"] = last
    return last


# ---------------------------------------------------------------- SEQUENCE
# One model, several timed steps keyed to the narration: the camera eases between framings of the same preset (pan and
# zoom, never a turn), parts fade to a see-through ghost and back, fade out, arrive (fade in while landing on their rest
# transform) and glow, each pulse on its own parts. Timings are shot-local seconds (the planner resolves sentences and
# words). The camera keys come from the views' fits, computed by the caller from the rest geometry.
SEQUENCE_DEFAULTS = {"template": "SEQUENCE", "state": None, "duration_seconds": None, "views": None, "steps": None}
VIEW_DEFAULTS = {"start_seconds": 0.0, "move_seconds": 0.0, "focus": None, "easing": "SMOOTH", "margin": None,
                 "azimuth": None, "elevation": None}   # g-r5: a view may turn the camera (an orbit); None = the preset
STEP_DEFAULTS = {
    "GHOST": {"components": None, "start_seconds": None, "seconds": 1.0, "transparency": 0.85},
    "UNGHOST": {"components": None, "start_seconds": None, "seconds": 1.0},
    "FADE_OUT": {"components": None, "start_seconds": None, "seconds": 1.0},
    "FADE_IN": {"components": None, "start_seconds": None, "seconds": 1.0},
    "REVEAL": {"components": None, "start_seconds": None, "seconds": 1.2, "direction": "FROM_ABOVE", "distance": 3.0,
               "stagger_seconds": 0.0, "easing": "EASE_OUT", "fade_end": 0.6, "sound": None},
    "HIGHLIGHT": {"components": None, "start_seconds": None, "rise_seconds": 0.3, "hold_seconds": 1.0,
                  "fall_seconds": 0.4, "strength": 0.6, "tint": 0.0},
    # floating family: the parts move as a rigid group by amounts a project has calculated (never tuned to look right)
    "MOVE": {"components": None, "start_seconds": None, "seconds": 1.5, "offset": None, "easing": "SMOOTH"},
    "ROTATE": {"components": None, "start_seconds": None, "seconds": 1.5, "axis": "X", "degrees": None, "pivot": None,
               "easing": "SMOOTH"},
    # conceptual motion only: a sine heave (and optional tilt) with a fade-in and fade-out; the planner requires the
    # beat to carry the label "Conceptual motion visualization — not a hydrodynamic simulation"
    "OSCILLATE": {"components": None, "start_seconds": None, "seconds": 6.0, "amplitude_m": 0.3, "period_seconds": 3.0,
                  "phase_degrees": 0.0, "tilt_degrees": 0.0, "axis": "X", "pivot": None, "fade_seconds": 0.8},
}
TRANSFORM_STEPS = ("MOVE", "ROTATE", "OSCILLATE")
CONCEPT_MOTION_LABEL = "Conceptual motion visualization — not a hydrodynamic simulation"
SOUNDS = (None, "STONE", "STONE_HEAVY")
SEQUENCE_TRANSPARENCY_EPS = 1e-6


def sequence_steps(cfg, where="SEQUENCE"):
    """Validated steps of a SEQUENCE config, each merged with its defaults ({"do": ...} + options)."""
    out = []
    for i, s in enumerate(cfg.get("steps") or []):
        w = f"{where}.steps[{i}]"
        if not isinstance(s, dict) or s.get("do") not in STEP_DEFAULTS:
            raise PlanError(f"{w}: 'do' must be one of {', '.join(STEP_DEFAULTS)}")
        c = merge_config(dict(STEP_DEFAULTS[s["do"]], do=s["do"]), s, w)
        if not isinstance(c["components"], list) or not c["components"]:
            raise PlanError(f"{w}: components must be a non-empty list of component ids")
        _number(c, "start_seconds", w)
        for key in ("seconds", "rise_seconds", "hold_seconds", "fall_seconds", "stagger_seconds", "distance"):
            if key in c:
                _number(c, key, w)
        if c["do"] == "GHOST":
            _number(c, "transparency", w, positive=True, maximum=0.95)
        if c["do"] in TRANSFORM_STEPS:
            vec = lambda key: isinstance(c.get(key), (list, tuple)) and len(c[key]) == 3 and all(   # noqa: E731
                isinstance(v, (int, float)) and not isinstance(v, bool) for v in c[key])
            if c["do"] == "MOVE" and not vec("offset"):
                raise PlanError(f"{w}: MOVE needs offset [dx, dy, dz] in metres")
            if c["do"] in ("ROTATE", "OSCILLATE"):
                if c["axis"] not in ("X", "Y", "Z"):
                    raise PlanError(f"{w}: axis must be X, Y or Z")
                if not vec("pivot"):
                    raise PlanError(f"{w}: {c['do']} needs pivot [x, y, z] in metres")
            if c["do"] == "ROTATE":
                d = c.get("degrees")
                if isinstance(d, bool) or not isinstance(d, (int, float)) or abs(d) > 45:
                    raise PlanError(f"{w}: ROTATE needs degrees within +/-45")
            if c["do"] == "OSCILLATE":
                _number(c, "amplitude_m", w, maximum=5.0)
                _number(c, "period_seconds", w, positive=True)
                _number(c, "fade_seconds", w)
                if abs(c["tilt_degrees"]) > 10:
                    raise PlanError(f"{w}: OSCILLATE tilt_degrees within +/-10")
            if c["seconds"] <= 0 and (c["do"] != "MOVE" or c["start_seconds"] > 0):
                raise PlanError(f"{w}: a {c['do']} needs seconds > 0 (an instant MOVE only at the start of the shot)")
        if c["do"] == "HIGHLIGHT":
            _number(c, "strength", w, positive=True, maximum=1.0)
            _number(c, "tint", w, maximum=1.0)
        if c["do"] == "REVEAL":
            _number(c, "fade_end", w, positive=True, maximum=1.0)
            if c["sound"] not in SOUNDS:
                raise PlanError(f"{w}: sound must be one of {SOUNDS}")
            if c["seconds"] <= 0:
                raise PlanError(f"{w}: a REVEAL needs seconds > 0")
        elif c["do"] != "HIGHLIGHT" and c["seconds"] <= 0 and c["start_seconds"] > 0:
            raise PlanError(f"{w}: an instant {c['do']} is only allowed at the start of the shot (start_seconds 0)")
        out.append(c)
    return out


def sequence_views(cfg, where="SEQUENCE"):
    views = cfg.get("views") or [{}]
    out = []
    for i, v in enumerate(views):
        c = merge_config(VIEW_DEFAULTS, v, f"{where}.views[{i}]", free_form=("focus",))
        _number(c, "start_seconds", f"{where}.views[{i}]")
        _number(c, "move_seconds", f"{where}.views[{i}]")
        if i == 0 and (c["start_seconds"] or c["move_seconds"]):
            raise PlanError(f"{where}.views[0] is the opening framing: start_seconds and move_seconds must be 0")
        if i > 0 and c["move_seconds"] <= 0:
            raise PlanError(f"{where}.views[{i}]: the camera eases between views (move_seconds > 0); cut to a new shot "
                            "for an instant change")
        if c["focus"] is not None and (not isinstance(c["focus"], list) or not c["focus"]):
            raise PlanError(f"{where}.views[{i}].focus must be null (every built part) or a list of component ids")
        if c["easing"] not in EASINGS:
            raise PlanError(f"{where}.views[{i}]: unknown easing {c['easing']!r}")
        for key, lo, hi in (("azimuth", -360.0, 360.0), ("elevation", -88.0, 88.0)):
            if c[key] is not None and (isinstance(c[key], bool) or not isinstance(c[key], (int, float))
                                       or not lo <= c[key] <= hi):
                raise PlanError(f"{where}.views[{i}].{key} must be null (the preset) or degrees in [{lo:g}, {hi:g}]")
        if i > 0:
            prev = out[-1]
            if c["start_seconds"] < prev["start_seconds"] + prev["move_seconds"] - 1e-9:
                raise PlanError(f"{where}.views[{i}] starts before the previous camera move ends")
        out.append(c)
    return out


def _orbit_camera(plan, name, views, fits):
    """Camera keys when the views look from different directions: each move is baked frame by frame along an orbit
    (engine/framing.orbit_pose: pivot, angles and scale eased together, the camera backing away mid-move), linear
    between baked frames; each view is held exactly on its fit. Returns the end of the last move in seconds."""
    from engine import framing
    last = plan.frame_count
    for k, f in enumerate(fits):
        missing = [x for x in ("azimuth", "elevation", "pivot", "distance", "rotation") if f.get(x) is None]
        if missing:
            raise PlanError(f"SEQUENCE.views[{k}]: an orbit needs fits with {missing}")

    def put(frame, loc, rot, ortho, prev_rot):
        rot = tuple(r + 2 * math.pi * round((p - r) / (2 * math.pi)) for r, p in zip(rot, prev_rot))   # no wrap
        plan.key(name, LOC, frame, loc)
        plan.key(name, ROT, frame, rot)
        plan.key(name, ORTHO, frame, ortho)
        return rot

    rot = put(1, fits[0]["location"], fits[0]["rotation"], fits[0]["ortho_scale"], fits[0]["rotation"])
    for k in range(1, len(views)):
        v = views[k]
        f0, f1 = plan.frame(v["start_seconds"]), plan.frame(v["start_seconds"] + v["move_seconds"])
        if f1 >= last:
            raise PlanError(f"SEQUENCE.views[{k}]: timing needs frame {f1 + 1} (the camera move ends at {f1}, "
                            f"then settles), the shot has {last}")
        a, b = fits[k - 1], fits[k]
        rot = put(f0, a["location"], a["rotation"], a["ortho_scale"], rot)
        for f in range(f0 + 1, f1):
            loc, r, ortho = framing.orbit_pose(a, b, ease(v["easing"], (f - f0) / (f1 - f0)))
            rot = put(f, loc, r, ortho, rot)
        rot = put(f1, b["location"], b["rotation"], b["ortho_scale"], rot)
        plan.markers[f"view_{k}_settled"] = f1
    put(last, fits[-1]["location"], rot, fits[-1]["ortho_scale"], rot)
    return views[-1]["start_seconds"] + views[-1]["move_seconds"]


def plan_sequence(plan, components, cfg, camera):
    """Keys for a SEQUENCE shot. components: {id: Component} the steps may name (the shown state + shared parts);
    camera: {"name", "views": [{"location", "ortho_scale"}, ...]} (one fit per view, same basis)."""
    c = merge_config(SEQUENCE_DEFAULTS, cfg, "SEQUENCE", free_form=("views", "steps"))
    views, steps = sequence_views(c), sequence_steps(c)
    last = plan.frame_count
    fits = camera.get("views") or [camera.get("start")] * len(views)
    if len(fits) != len(views):
        raise PlanError(f"SEQUENCE: {len(views)} views but {len(fits)} camera fits")
    end = 0.0
    turns = len(views) > 1 and any(f.get("rotation") is not None and f.get("rotation") != fits[0].get("rotation")
                                   for f in fits)
    if turns:   # g-r5: an orbit between views that look from different directions
        end = _orbit_camera(plan, camera["name"], views, fits)
    elif len(views) > 1:   # the camera holds each view, then eases to the next
        name = camera["name"]
        for channel, key in ((LOC, "location"), (ORTHO, "ortho_scale")):
            plan.key(name, channel, 1, fits[0][key])
            for k in range(1, len(views)):
                v = views[k]
                f0, f1 = plan.frame(v["start_seconds"]), plan.frame(v["start_seconds"] + v["move_seconds"])
                if f1 >= last:
                    raise PlanError(f"SEQUENCE.views[{k}]: timing needs frame {f1 + 1} (the camera move ends at {f1}, "
                                    f"then settles), the shot has {last}")
                plan.key(name, channel, f0, fits[k - 1][key], v["easing"])
                plan.key(name, channel, f1, fits[k][key])
                plan.markers[f"view_{k}_settled"] = f1
            plan.key(name, channel, last, fits[-1][key])
        end = views[-1]["start_seconds"] + views[-1]["move_seconds"]
    for i, s in enumerate(steps):
        unknown = [x for x in s["components"] if x not in components]
        if unknown:
            raise PlanError(f"SEQUENCE.steps[{i}] ({s['do']}): {unknown} are not parts of the shown state")
    # transparency: per part, a timeline of (frame0, frame1, target) segments that must not overlap
    segments, reveals, pulses, transforms = {}, [], {}, {}
    for i, s in enumerate(steps):
        t0 = s["start_seconds"]
        if s["do"] in TRANSFORM_STEPS:
            for cid in s["components"]:
                transforms.setdefault(cid, []).append((t0, t0 + s["seconds"], s, i))
            end = max(end, t0 + s["seconds"])
            continue
        if s["do"] == "HIGHLIGHT":
            t3 = t0 + s["rise_seconds"] + s["hold_seconds"] + s["fall_seconds"]
            for cid in s["components"]:
                pulses.setdefault(cid, []).append((t0, t3, s, i))
            end = max(end, t3)
            continue
        groups = [[cid] for cid in s["components"]] if s["do"] == "REVEAL" and s["stagger_seconds"] > 0 \
            else [list(s["components"])]
        for gi, group in enumerate(groups):
            start = t0 + gi * (s["stagger_seconds"] if s["do"] == "REVEAL" else 0.0)
            stop = start + s["seconds"]
            target = {"GHOST": s.get("transparency"), "UNGHOST": 0.0, "FADE_OUT": 1.0, "FADE_IN": 0.0, "REVEAL": 0.0}[s["do"]]
            fade_stop = start + s["seconds"] * s["fade_end"] if s["do"] == "REVEAL" else stop
            for cid in group:
                segments.setdefault(cid, []).append((start, fade_stop, target, s["do"], i))
                if s["do"] == "REVEAL":
                    reveals.append((cid, start, stop, s, i))
            end = max(end, stop)
    if plan.frame(end) > last:
        raise PlanError(f"SEQUENCE timing needs {end:.2f}s for its last step; the shot has {last / plan.fps:.2f}s")
    for cid, segs in segments.items():
        segs.sort()
        n = components[cid].name
        first_do = segs[0][3]
        value = 1.0 if first_do in ("REVEAL", "FADE_IN") else 0.0    # a part that arrives starts unseen
        plan.key(n, TRANSPARENCY, 1, value)
        prev_end = -1.0
        for start, stop, target, do, i in segs:
            if start < prev_end - 1e-9:
                raise PlanError(f"SEQUENCE.steps[{i}] ({do}): {cid} is still fading from an earlier step")
            if do in ("REVEAL", "FADE_IN") and value < 1.0 - SEQUENCE_TRANSPARENCY_EPS:
                raise PlanError(f"SEQUENCE.steps[{i}] ({do}): {cid} is already visible; only an unseen part can arrive")
            if do in ("GHOST", "UNGHOST", "FADE_OUT") and value >= 1.0 - SEQUENCE_TRANSPARENCY_EPS:
                raise PlanError(f"SEQUENCE.steps[{i}] ({do}): {cid} is not visible at that point")
            f0, f1 = plan.frame(start), plan.frame(stop)
            if f1 <= f0:   # instant (only at frame 1, checked in sequence_steps)
                plan.key(n, TRANSPARENCY, 1, target)
            else:
                plan.key(n, TRANSPARENCY, max(f0, 1), value, "SMOOTH")
                plan.key(n, TRANSPARENCY, f1, target)
            value, prev_end = target, stop
        plan.key(n, TRANSPARENCY, last, value)
        # hidden whenever fully transparent (no shadow, no stray dither); visibility changes only between frames
        previous = None
        for f in range(1, last + 1):
            hidden = plan.sample(n, TRANSPARENCY, f)[0] >= 1.0 - SEQUENCE_TRANSPARENCY_EPS
            if hidden != previous:
                plan.key(n, HIDE, f, 1.0 if hidden else 0.0, "CONSTANT")
                previous = hidden
    center = centroid([components[cid] for cid, *_ in reveals]) if reveals else (0.0, 0.0, 0.0)
    if len({cid for cid, *_ in reveals}) != len(reveals):
        raise PlanError("SEQUENCE: a part arrives twice; fade it out and back in instead")
    for cid in transforms:   # parts that also move: their REVEAL is composed with the moves below
        _plan_transforms(plan, components[cid], transforms[cid],
                         [(st, sp, s, i) for c2, st, sp, s, i in reveals if c2 == cid], center, last)
    reveals = [r for r in reveals if r[0] not in transforms]
    for cid, start, stop, s, i in reveals:
        comp = components[cid]
        direction = resolve_direction(s["direction"], comp, center)
        begin = _add(comp.location, _mul(direction, float(s["distance"])))
        f0, f1 = plan.frame(start), plan.frame(stop)
        hidden_from = f0   # a part seen earlier in the shot (then faded out) moves to its start only once unseen
        while hidden_from > 1 and plan.sample(comp.name, HIDE, hidden_from - 1)[0] > 0.5:
            hidden_from -= 1
        if hidden_from > 1:
            plan.key(comp.name, LOC, 1, comp.location, "CONSTANT")
            plan.key(comp.name, LOC, hidden_from, begin, "CONSTANT")
        else:
            plan.key(comp.name, LOC, 1, begin)
        plan.key(comp.name, LOC, f0, begin, s["easing"])
        plan.key(comp.name, LOC, f1, comp.location)
        plan.key(comp.name, LOC, last, comp.location)
        plan.markers[f"reveal_{i}_landed"] = max(plan.markers.get(f"reveal_{i}_landed", 0), f1)
    if len({cid for cid, *_ in reveals}) != len(reveals):
        raise PlanError("SEQUENCE: a part arrives twice; fade it out and back in instead")
    for cid, ps in pulses.items():
        ps.sort(key=lambda x: x[0])
        n = components[cid].name
        plan.key(n, HIGHLIGHT, 1, 0.0)
        tints = {s["tint"] for _, _, s, _ in ps}
        if len(tints) > 1:
            raise PlanError(f"SEQUENCE: {cid} glows with tints {sorted(tints)}; one tint per part and shot")
        if tints != {0.0}:   # a constant: the tint only shows while the part glows
            plan.key(n, TINT, 1, tints.pop(), "CONSTANT")
        prev = -1.0
        for t0, t3, s, i in ps:
            if t0 < prev + 1.0 / plan.fps - 1e-9:
                raise PlanError(f"SEQUENCE.steps[{i}] (HIGHLIGHT): {cid} is still glowing from an earlier step")
            f0, f1 = plan.frame(t0), plan.frame(t0 + s["rise_seconds"])
            f2 = plan.frame(t0 + s["rise_seconds"] + s["hold_seconds"])
            f3 = plan.frame(t3)
            plan.key(n, HIGHLIGHT, max(f0, 1), 0.0, "SMOOTH")
            plan.key(n, HIGHLIGHT, f1, s["strength"], "LINEAR")
            plan.key(n, HIGHLIGHT, f2, s["strength"], "SMOOTH")
            plan.key(n, HIGHLIGHT, f3, 0.0)
            plan.markers[f"highlight_{i}_peak"] = plan.frame(t0 + s["rise_seconds"] + s["hold_seconds"] / 2.0)
            prev = t3
        plan.key(n, HIGHLIGHT, last, 0.0)
    plan.markers.setdefault("middle", (plan.frame_count + 1) // 2)
    return plan


def _rotate_about(p, pivot, axis, radians):
    """Point p turned by `radians` about the axis through `pivot` parallel to X, Y or Z."""
    x, y, z = (p[k] - pivot[k] for k in range(3))
    c, s = math.cos(radians), math.sin(radians)
    if axis == "X":
        x, y, z = x, y * c - z * s, y * s + z * c
    elif axis == "Y":
        x, y, z = x * c + z * s, y, -x * s + z * c
    else:
        x, y, z = x * c - y * s, x * s + y * c, z
    return (x + pivot[0], y + pivot[1], z + pivot[2])


def _plan_transforms(plan, comp, moves, reveals, center, last):
    """Location (and rotation) keys of one part under MOVE / ROTATE / OSCILLATE steps, composed in time order with
    an optional REVEAL. Events on one part must not overlap; each starts from where the previous one left the part."""
    events = sorted([(st, sp, s, i, "REVEAL") for st, sp, s, i in reveals] + [(st, sp, s, i, s["do"]) for st, sp, s, i in moves],
                    key=lambda e: e[0])
    for a, b in zip(events, events[1:]):
        if b[0] < a[1] - 1e-9:
            raise PlanError(f"SEQUENCE.steps[{b[3]}] ({b[4]}): {comp.id} is still moving from steps[{a[3]}] ({a[4]})")
    axis_index = {"X": 0, "Y": 1, "Z": 2}

    def state(t):
        loc, rot = tuple(comp.location), list(comp.rotation)
        for st, sp, s, i, do in events:
            if do == "REVEAL":
                direction = resolve_direction(s["direction"], comp, center)
                f = 0.0 if t <= st else 1.0 if t >= sp else ease(s["easing"], (t - st) / (sp - st))
                loc = _add(loc, _mul(direction, float(s["distance"]) * (1.0 - f)))
                continue
            if t < st or (t <= st and sp > st):   # an instant MOVE (seconds 0, at the start) holds from its moment
                break
            f = 1.0 if sp <= st or t >= sp else ease(s.get("easing", "SMOOTH"), (t - st) / (sp - st))
            if do == "MOVE":
                loc = _add(loc, _mul(tuple(float(v) for v in s["offset"]), f))
            elif do == "ROTATE":
                r = math.radians(float(s["degrees"])) * f
                loc = _rotate_about(loc, s["pivot"], s["axis"], r)
                rot[axis_index[s["axis"]]] += r
            else:   # OSCILLATE: heave and tilt with a fade at both ends, back to rest at the end
                u = min(t, sp) - st
                env = min(1.0, u / s["fade_seconds"], max(0.0, (sp - st - u)) / s["fade_seconds"]) if s["fade_seconds"] > 0 else 1.0
                phase = 2 * math.pi * u / s["period_seconds"] + math.radians(s["phase_degrees"])
                loc = _add(loc, (0.0, 0.0, s["amplitude_m"] * math.sin(phase) * env))
                r = math.radians(s["tilt_degrees"]) * math.sin(phase + math.pi / 2) * env
                if r:
                    loc = _rotate_about(loc, s["pivot"], s["axis"], r)
                    rot[axis_index[s["axis"]]] += r
        return loc, tuple(rot)

    frames = {1: "LINEAR", last: "LINEAR"}
    begins, ends = {}, {}   # an event's first key holds the state at its exact start, its last key the state at its
    for st, sp, s, i, do in events:    # exact end (frames round to 1/48 s around them; parts must not drift while they wait)
        f0, f1 = max(1, plan.frame(st)), min(last, plan.frame(sp))
        begins[f0] = min(begins.get(f0, st), st)
        if do in ("REVEAL", "MOVE"):
            ends[f1] = max(ends.get(f1, sp), sp)
        if do in ("REVEAL", "MOVE"):
            frames[f0] = s.get("easing", "SMOOTH")
            frames.setdefault(f1, "LINEAR")
        else:   # rotations and oscillations follow their path: a key every second frame
            for f in range(f0, f1 + 1, 2):
                frames[f] = "LINEAR"
            frames[f1] = "LINEAR"
    rotates = any(do in ("ROTATE", "OSCILLATE") for *_, do in events)
    for f in sorted(frames):
        t = (f - 1) / plan.fps
        if f in ends and t < ends[f]:
            t = ends[f]
        if f in begins and t > begins[f]:
            t = begins[f]
        loc, rot = state(t)
        plan.key(comp.name, LOC, f, loc, frames[f])
        if rotates:
            plan.key(comp.name, ROT, f, rot, frames[f])
        for st, sp, s, i, do in events:
            if f == min(last, plan.frame(sp)):
                key = f"reveal_{i}_landed" if do == "REVEAL" else f"{do.lower()}_{i}_done"   # the name the QA reads
                plan.markers[key] = max(plan.markers.get(key, 0), f)


def plan_highlight_only(plan, cfg, defaults, names_for, where):
    """HOLD and SIDE_BY_SIDE: no transforms move; an optional highlight pulse."""
    c = merge_config(defaults, cfg, where)
    if c["highlight"]:
        default_sel = "DIFFERENCES" if where == "SIDE_BY_SIDE" else "STATE"
        h = merged_pulse(c["highlight"], f"{where}.highlight", default_sel, GHOST_DEFAULTS if where == "HOLD" else None)
        glowing = names_for(h["components"])
        f0, f3 = plan_pulse(plan, glowing, h["start_seconds"], h["rise_seconds"],
                            h["hold_seconds"], h["fall_seconds"], h["strength"], f"{where}.highlight")
        if h.get("ghost"):
            if not isinstance(h["ghost"], list):
                raise PlanError(f"{where}.highlight.ghost must be a list of component ids")
            t = _number(h, "ghost_transparency", f"{where}.highlight", positive=True, maximum=0.9)
            ghosts = names_for(h["ghost"])
            both = sorted(set(ghosts) & set(glowing))
            if both:
                raise PlanError(f"{where}.highlight.ghost: {both} also glow; ghost only the parts covering them")
            f1 = plan.frame(h["start_seconds"] + h["rise_seconds"])
            f2 = plan.frame(h["start_seconds"] + h["rise_seconds"] + h["hold_seconds"])
            for n in ghosts:
                plan.key(n, TRANSPARENCY, 1, 0.0)
                plan.key(n, TRANSPARENCY, f0, 0.0, "SMOOTH")
                plan.key(n, TRANSPARENCY, f1, t, "LINEAR")
                plan.key(n, TRANSPARENCY, f2, t, "SMOOTH")
                plan.key(n, TRANSPARENCY, f3, 0.0)
                plan.key(n, TRANSPARENCY, plan.frame_count, 0.0)
        plan.markers.update({"highlight_start": f0, "highlight_end": f3,
                             "highlight_peak": plan.frame(h["start_seconds"] + h["rise_seconds"]
                                                          + h["hold_seconds"] / 2.0)})
    plan.markers.setdefault("middle", (plan.frame_count + 1) // 2)
    return c
