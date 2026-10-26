"""Reusable deterministic transform animation: shared pieces never move."""
from mathutils import Vector


def _key(obj, frame):
    obj.keyframe_insert(data_path="location", frame=frame)
    obj.keyframe_insert(data_path="scale", frame=frame)


def _origin(obj):
    return obj.location.copy(), obj.scale.copy()


def keyframe_replace_parts(parts_out, parts_in, fps):
    """6-sec A -> B shot; keyframes are independent of preview framerate."""
    # Outgoing A: hold, then fly upward/out with slight stagger; shrink offscreen.
    for i, obj in enumerate(parts_out):
        base, default_scale = _origin(obj)
        sign = -1 if i % 2 == 0 else 1
        lift = Vector((sign * (3.2 + 0.3*i), 0.2 * i, 2.0 + 0.25*i))
        begin = round(1.25*fps) + i*3
        end = round(2.65*fps) + i*3
        obj.location = base
        obj.scale = default_scale
        _key(obj, 1)
        _key(obj, begin)
        obj.location = base + lift
        obj.scale = default_scale * 0.01
        _key(obj, end)
        _key(obj, round(6*fps))

    # Incoming B: start outside, become visible while flying in, then hold.
    for i, obj in enumerate(parts_in):
        dest, default_scale = _origin(obj)
        sign = -1 if i % 2 == 0 else 1
        launch = dest + Vector((sign * (3.8 + 0.35*i), -.3*i, 2.6 + .2*i))
        start = round(2.15*fps) + i*4
        visible = start + round(.25*fps)
        end = round(4.75*fps) + i*4
        obj.location = launch
        obj.scale = default_scale * .001
        _key(obj, 1)
        _key(obj, start)
        obj.scale = default_scale
        _key(obj, visible)
        obj.location = dest
        _key(obj, end)
        _key(obj, round(6*fps))

    # All keyframe interpolation defaults to Bezier for ease-in/out.
    # Explicit frame values allow deterministic seek/render of any frame.
