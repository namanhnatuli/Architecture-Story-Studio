"""Pure-Python project spec helpers: component ownership and states.json checks (no bpy).

The Blender builders in engine/geometry.py create exactly the parts listed here,
so tools/validator.py can check ownership, shared components and template timing
offline, and the engine can fail with a clear message when they disagree.
"""

# Base builders: (component_id, role, group). `shared_components` in states.json may
# name a component_id or a group.
BASE_BUILDERS = {
    "rectangular_house_base": (
        ("foundation", "foundation", "foundation"),
        ("floor", "floor", "floor"),
        ("wall_left", "wall", "walls"), ("wall_right", "wall", "walls"),
        ("wall_front", "wall", "walls"), ("wall_back", "wall", "walls"),
        ("door", "door", "door"), ("door_handle", "detail", "door"),
        ("window_right", "window", "windows"), ("window_right_frame_h", "detail", "windows"),
        ("window_right_frame_v", "detail", "windows"),
        ("window_left", "window", "windows"), ("window_left_frame_h", "detail", "windows"),
        ("window_left_frame_v", "detail", "windows"),
        ("ceiling_joists", "joists", "structure"),
    ),
}

# Variant builders: (id suffix, role, assembly layer). Layer 0 is assembled first.
VARIANT_BUILDERS = {
    "gable_roof": (
        ("gable_front", "gable_wall", 0), ("gable_back", "gable_wall", 0),
        ("rafters_left", "rafters", 1), ("rafters_right", "rafters", 1),
        ("ridge_beam", "ridge_beam", 2),
        ("covering_left", "roof_covering", 3), ("covering_right", "roof_covering", 3),
    ),
}

# Names accepted in shared_components that belong to the environment, not the model.
ENVIRONMENT_NAMES = ("ground",)

DEFAULT_BASE = {"builder": "rectangular_house_base", "width": 4.6, "depth": 3.2,
                "wall_height": 2.55, "rafter_count": 5}


def base_params(states):
    params = dict(DEFAULT_BASE)
    params.update(states.get("base") or {})
    return params


def base_parts(states):
    builder = base_params(states)["builder"]
    if builder not in BASE_BUILDERS:
        raise ValueError(f"unknown base builder '{builder}' (known: {', '.join(BASE_BUILDERS)})")
    return [{"id": i, "role": r, "group": g} for i, r, g in BASE_BUILDERS[builder]]


def variant_builder(variant):
    return variant.get("builder", "gable_roof")


def builder_parts(variant):
    builder = variant_builder(variant)
    if builder not in VARIANT_BUILDERS:
        raise ValueError(f"unknown variant builder '{builder}' (known: {', '.join(VARIANT_BUILDERS)})")
    return [{"id": f"{variant['id']}_{s}", "role": r, "layer": layer}
            for s, r, layer in VARIANT_BUILDERS[builder]]


def variant_parts(variant):
    """Declared parts (explicit ownership) or, for v1 states files, the builder's list."""
    return variant.get("components") or builder_parts(variant)


def variant_map(states):
    return {v.get("id"): v for v in states.get("variants", [])}


def variant_ids(states, variant_id):
    return [p["id"] for p in variant_parts(variant_map(states)[variant_id])]


def shared_ids(states):
    """Component IDs covered by shared_components (ids or group names), in build order."""
    names = set(states.get("shared_components", []))
    return [p["id"] for p in base_parts(states) if p["id"] in names or p["group"] in names]


def rafter_positions(depth, count, margin=0.25):
    """Evenly spaced positions along the depth, shared by rafters and ceiling joists."""
    if count < 2:
        raise ValueError("rafter_count must be >= 2")
    start, end = -depth / 2 + margin, depth / 2 - margin
    return [start + (end - start) * i / (count - 1) for i in range(count)]


def validate_states(states):
    """Structural ownership checks; returns a list of error strings."""
    errors = []
    try:
        base = base_parts(states)
    except ValueError as e:
        return [str(e)]
    params = base_params(states)
    for key in ("width", "depth", "wall_height"):
        value = params.get(key)
        if isinstance(value, bool) or not isinstance(value, (int, float)) or value <= 0:
            errors.append(f"base.{key} must be a positive number")
    count = params.get("rafter_count")
    if isinstance(count, bool) or not isinstance(count, int) or count < 2:
        errors.append("base.rafter_count must be an integer >= 2")

    seen = {p["id"]: "shared" for p in base}
    for variant in states.get("variants", []):
        vid = variant.get("id")
        if not vid:
            continue
        try:
            expected = builder_parts(variant)
        except ValueError as e:
            errors.append(f"variant {vid}: {e}")
            continue
        if variant_builder(variant) == "gable_roof":
            pitch = variant.get("roof_pitch_degrees")
            if isinstance(pitch, bool) or not isinstance(pitch, (int, float)) or not 5 <= pitch <= 70:
                errors.append(f"variant {vid}: roof_pitch_degrees must be between 5 and 70")
            if not variant.get("color_key"):
                errors.append(f"variant {vid}: color_key is required")
        declared = variant.get("components")
        if declared is not None:
            roles = {p["id"]: p["role"] for p in expected}
            ids = [p.get("id") for p in declared]
            missing = sorted(set(roles) - set(ids))
            extra = sorted(set(ids) - set(roles))
            if missing or extra:
                errors.append(f"variant {vid}: components must match builder '{variant_builder(variant)}' "
                              f"(missing {missing}, unexpected {extra})")
            for part in declared:
                pid = part.get("id")
                if pid in roles and part.get("role") != roles[pid]:
                    errors.append(f"variant {vid}: {pid} role must be '{roles[pid]}'")
                layer = part.get("layer")
                if isinstance(layer, bool) or not isinstance(layer, int) or layer < 0:
                    errors.append(f"variant {vid}: {pid} layer must be an integer >= 0")
        for part in variant_parts(variant):
            pid = part.get("id")
            if pid in seen:
                errors.append(f"component id {pid} is owned by both {seen[pid]} and {vid}")
            seen[pid] = vid

    names = states.get("shared_components", [])
    known = {p["id"] for p in base} | {p["group"] for p in base} | set(ENVIRONMENT_NAMES)
    for name in names:
        if name not in known:
            errors.append(f"shared component '{name}' matches no base component id or group")
    covered = set(shared_ids(states))
    uncovered = [p["id"] for p in base if p["id"] not in covered]
    if uncovered:
        errors.append(f"base components not declared in shared_components: {uncovered}")
    return errors
