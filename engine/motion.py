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
TRANSPARENCY = '["ass_transparency"]'
HIGHLIGHT = '["ass_highlight"]'
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


def merged_pulse(cfg, where, default_components):
    defaults = dict(PULSE_DEFAULTS, components=default_components)
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
HOLD_DEFAULTS = {"template": "HOLD", "state": None, "duration_seconds": None, "highlight": None}
SIDE_BY_SIDE_DEFAULTS = {"template": "SIDE_BY_SIDE", "states": None, "duration_seconds": None,
                         "gap_ratio": 0.35, "label_band": 0.12, "highlight": None, "intro": None, "labels": None,
                         "layout": "ROW"}
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


def plan_highlight_only(plan, cfg, defaults, names_for, where):
    """HOLD and SIDE_BY_SIDE: no transforms move; an optional highlight pulse."""
    c = merge_config(defaults, cfg, where)
    if c["highlight"]:
        default_sel = "DIFFERENCES" if where == "SIDE_BY_SIDE" else "STATE"
        h = merged_pulse(c["highlight"], f"{where}.highlight", default_sel)
        f0, f3 = plan_pulse(plan, names_for(h["components"]), h["start_seconds"], h["rise_seconds"],
                            h["hold_seconds"], h["fall_seconds"], h["strength"], f"{where}.highlight")
        plan.markers.update({"highlight_start": f0, "highlight_end": f3,
                             "highlight_peak": plan.frame(h["start_seconds"] + h["rise_seconds"]
                                                          + h["hold_seconds"] / 2.0)})
    plan.markers.setdefault("middle", (plan.frame_count + 1) // 2)
    return c
