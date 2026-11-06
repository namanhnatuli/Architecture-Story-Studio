"""Write a motion.Plan into Blender keyframes (bpy).

Every key gets an explicit interpolation/easing, so curves never depend on user
preferences (default BEZIER handles would overshoot and break exact landings).
"""
from engine import motion

PROPS = {motion.TRANSPARENCY: "ass_transparency", motion.HIGHLIGHT: "ass_highlight", motion.TINT: "ass_tint"}


def iter_fcurves(obj):
    """F-curves of an object's action: slotted/layered actions (4.4+/5.x) or legacy."""
    ad = obj.animation_data
    if not ad or not ad.action:
        return []
    action = ad.action
    if getattr(action, "layers", None):
        curves = []
        for layer in action.layers:
            for strip in layer.strips:
                bag = strip.channelbag(ad.action_slot) if ad.action_slot else None
                if bag:
                    curves.extend(bag.fcurves)
        return curves
    return list(getattr(action, "fcurves", []))


def _assign(obj, channel, value):
    if channel == motion.LOC:
        obj.location = value
    elif channel == motion.ROT:
        obj.rotation_euler = value
    elif channel == motion.SCALE:
        obj.scale = value
    elif channel in PROPS:
        obj[PROPS[channel]] = value[0]
    elif channel == motion.HIDE:
        obj.hide_render = obj.hide_viewport = value[0] > 0.5
    elif channel == motion.ORTHO:
        obj.data.ortho_scale = value[0]
    else:
        raise ValueError(f"unsupported channel {channel}")


def _insert(obj, channel, frame):
    if channel == motion.HIDE:
        obj.keyframe_insert("hide_render", frame=frame)
        obj.keyframe_insert("hide_viewport", frame=frame)
    elif channel == motion.ORTHO:
        obj.data.keyframe_insert("ortho_scale", frame=frame)
    else:
        obj.keyframe_insert(channel, frame=frame)


def apply_plan(plan, objects):
    """objects: {object name: bpy object}. Unknown names are an error, never ignored."""
    missing = sorted(set(plan.tracks) - set(objects))
    if missing:
        raise ValueError(f"plan animates objects that were not built: {missing}")
    for name in sorted(plan.tracks):
        obj = objects[name]
        for channel in plan.channels(name):
            for key in plan.keys(name, channel):
                _assign(obj, channel, key.value)
                _insert(obj, channel, key.frame)
        curves = [(fc, fc.data_path) for fc in iter_fcurves(obj)]
        if motion.ORTHO in plan.channels(name):
            curves += [(fc, motion.ORTHO) for fc in iter_fcurves(obj.data) if fc.data_path == "ortho_scale"]
        for fc, path in curves:
            channel = motion.HIDE if path in ("hide_render", "hide_viewport") else path
            keys = {k.frame: k for k in plan.keys(name, channel)}
            for kp in fc.keyframe_points:
                key = keys.get(int(round(kp.co.x)))
                if key is None:
                    raise ValueError(f"{name}: unexpected keyframe on {fc.data_path} at {kp.co.x}")
                interpolation, easing = motion.EASINGS["CONSTANT" if channel == motion.HIDE else key.easing]
                kp.interpolation = interpolation
                kp.easing = easing
            fc.update()
