"""Build one storyboard shot as a self-contained, reproducible Blender scene (bpy).

Order of work: geometry (builders) -> rest data -> layout -> camera fit ->
static visibility -> template plan (pure Python) -> keyframes. Nothing depends
on a viewport, selection or a previously open scene.
"""
import json
from dataclasses import dataclass
from pathlib import Path

import bpy

from engine import animate, framing, geometry, motion, spec, templates
from engine import scene as scene_mod

ROOT = Path(__file__).resolve().parent.parent


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_project(project_dir, preset_name="preview"):
    project_dir = Path(project_dir).resolve()
    presets = load_json(ROOT / "config/render_presets.json")
    if preset_name not in presets:
        raise ValueError(f"unknown render preset '{preset_name}'")
    return {
        "dir": project_dir,
        "project": load_json(project_dir / "project.json"),
        "states": load_json(project_dir / "storyboard/states.json"),
        "story": load_json(project_dir / "storyboard/storyboard.json"),
        "style": load_json(ROOT / "config/visual_style.json"),
        "preset": presets[preset_name],
    }


def find_shot(story, shot_id):
    for shot in story.get("shots", []):
        if shot.get("id") == shot_id:
            return shot
    raise ValueError(f"unknown shot '{shot_id}' (shots: {', '.join(s.get('id', '?') for s in story.get('shots', []))})")


@dataclass
class ShotContext:
    shot: dict
    cfg: dict
    scene: object
    plan: object
    fps: int
    frame_count: int
    objects: dict          # object name -> model component object
    slots: dict            # slot id -> {component_id: object}
    slot_roots: dict       # slot id -> empty parenting that slot
    slot_offsets: dict     # slot id -> world offset of the slot root
    visible_variants: dict # slot id -> variant ids visible in the shot
    components: dict       # object name -> motion.Component (rest data)
    camera: object
    camera_fit: dict
    camera_basis: tuple
    aspect: float
    bottom_band: float
    ground: object
    render_objects: dict = None  # objects + camera + fade twins (everything the plan animates)
    fade_twins: dict = None      # original name -> blended twin object
    camera_keys: dict = None     # SIDE_BY_SIDE intro camera start/end, else None
    labels: dict = None          # SIDE_BY_SIDE slot id -> label text object (static, in the label band)


def purge_data():
    """Empty the open file (headless CLI only; MCP sessions use isolated=True instead)."""
    for coll in (bpy.data.objects, bpy.data.meshes, bpy.data.materials, bpy.data.lights,
                 bpy.data.cameras, bpy.data.worlds, bpy.data.actions, bpy.data.collections, bpy.data.curves):
        for item in list(coll):
            coll.remove(item)


def world_vertices(obj, depsgraph):
    ev = obj.evaluated_get(depsgraph)
    mesh = ev.to_mesh()
    try:
        return [tuple(ev.matrix_world @ v.co) for v in mesh.vertices]
    finally:
        ev.to_mesh_clear()


def _bounds(points):
    lo = tuple(min(p[i] for p in points) for i in range(3))
    hi = tuple(max(p[i] for p in points) for i in range(3))
    return lo, hi


def _prepare_scene(shot_id, isolated):
    geometry.reset_mesh_cache()   # shared asset meshes never outlive the scene they were built for
    if isolated:
        scene = bpy.data.scenes.new(f"ASS_{shot_id}")
        window = getattr(bpy.context, "window", None)
        if window is None:
            raise RuntimeError("isolated build needs a Blender window (use the CLI for headless runs)")
        window.scene = scene
        return scene
    purge_data()
    return bpy.context.scene


def build_shot(project_dir, shot_id, preset_name="preview", isolated=False):
    """Build a shot. isolated=True creates a new scene instead of emptying the file,
    so an interactive (MCP) session never loses unrelated work."""
    data = load_project(project_dir, preset_name)
    states, style, preset = data["states"], data["style"], data["preset"]
    errors = spec.validate_states(states)
    if errors:
        raise ValueError("states.json invalid: " + "; ".join(errors))
    shot = find_shot(data["story"], shot_id)
    if shot.get("visual_type", "BLENDER_3D") == "MOTION_GRAPHICS":
        from engine import diagram
        scene = _prepare_scene(shot_id, isolated)
        return diagram.build_card(data, shot, preset_name, scene)
    cfg = templates.animation_config(shot)
    fps = int(data["project"]["fps"])
    frames = templates.frame_count(shot, fps)

    scene = _prepare_scene(shot_id, isolated)
    root = geometry.make_collection(f"ASS_{shot_id}", scene.collection)
    materials = scene_mod.make_materials(style)
    ground = scene_mod.build_environment(scene, style, materials, geometry.make_collection("90_ENVIRONMENT", root))

    objects, slots, roots, visible = {}, {}, {}, {}
    for slot_id, built, active in templates.layout_slots(shot, states):
        col = geometry.make_collection(f"00_SLOT_{slot_id}", root)
        slot_root = bpy.data.objects.new(f"SLOT_{slot_id}", None)
        slot_root["slot_id"] = slot_id
        col.objects.link(slot_root)
        slots[slot_id] = {}
        for obj in geometry.build_model(states, materials, col, built):
            name = templates.object_name(slot_id, obj["component_id"])
            obj.name = name
            if obj.name != name:
                raise ValueError(f"object name collision for '{name}'")
            obj.parent = slot_root  # root sits at the origin, so local == slot space
            obj["slot_id"] = slot_id
            objects[name] = obj
            slots[slot_id][obj["component_id"]] = obj
        roots[slot_id], visible[slot_id] = slot_root, list(active)

    depsgraph = bpy.context.evaluated_depsgraph_get()
    depsgraph.update()
    verts = {name: world_vertices(obj, depsgraph) for name, obj in objects.items()}
    components = {}
    for name, obj in objects.items():
        lo, hi = _bounds(verts[name])
        components[name] = motion.Component(
            name=name, id=obj["component_id"], location=tuple(obj.location),
            rotation=tuple(obj.rotation_euler), center=tuple((a + b) / 2 for a, b in zip(lo, hi)),
            layer=int(obj["assembly_layer"]),
            hint=tuple(obj["explode_hint"]) if "explode_hint" in obj else None)

    cam_preset = scene_mod.camera_preset(style, shot["camera"])
    basis = framing.camera_basis(cam_preset["azimuth_degrees"], cam_preset["elevation_degrees"])
    offsets = {sid: (0.0, 0.0, 0.0) for sid in slots}
    bottom_band = 0.0
    if cfg["template"] == "SIDE_BY_SIDE":
        gap_ratio = cfg.get("gap_ratio", motion.SIDE_BY_SIDE_DEFAULTS["gap_ratio"])
        if cfg.get("layout", "ROW") == "STACK":   # M4: long models as rows (one behind another)
            offs, _ = framing.layout_stack([[p for name, obj in objects.items() if obj["slot_id"] == sid
                                             for p in verts[name]] for sid in slots], basis, gap_ratio)
        else:
            footprints = []
            for sid in slots:
                lo, hi = _bounds([p for name, obj in objects.items() if obj["slot_id"] == sid for p in verts[name]])
                footprints.append((lo[0], lo[1], hi[0], hi[1]))
            offs, _ = framing.layout_side_by_side(footprints, basis[0], gap_ratio)
        offsets = dict(zip(slots, offs))
        for sid, off in offsets.items():
            roots[sid].location = off
        bottom_band = cfg.get("label_band", motion.SIDE_BY_SIDE_DEFAULTS["label_band"])

    # Camera framed on every built part at rest (hidden variants included), so all
    # single-model shots of a project (or of one M5 continuity group, build_variants)
    # share one identical locked camera. M5: camera_focus frames only the listed
    # components (COMPONENT_CLOSEUP); camera_safe_band keeps a strip free for subtitles.
    focus = set(shot.get("camera_focus") or []) if cfg["template"] != "SIDE_BY_SIDE" else set()
    framed = [name for name, obj in objects.items() if not focus or obj["component_id"] in focus]
    if focus and not framed:
        raise ValueError(f"{shot_id}: camera_focus matches no built component")
    points = [tuple(p[i] + offsets[objects[name]["slot_id"]][i] for i in range(3))
              for name in framed for p in verts[name]]
    if focus:   # M5.5: a close-up of moving parts frames them at every keyed position
        early = templates.plan_shot(shot, states, fps, {sid: {cid: components[obj.name] for cid, obj in parts.items()}
                                                        for sid, parts in slots.items()})
        points += focus_motion_points(early, objects, framed, depsgraph)
    if cfg["template"] != "SIDE_BY_SIDE":
        bottom_band = float(shot.get("camera_safe_band", 0.0))
    aspect = preset["width"] / preset["height"]
    camera, fit, basis = scene_mod.build_camera(scene, geometry.make_collection("90_CAMERA", root),
                                                cam_preset, points, aspect, bottom_band)

    shown = {sid: templates.visible_component_ids(states, vis) for sid, vis in visible.items()}
    for obj in objects.values():
        if obj["component_id"] not in shown[obj["slot_id"]]:
            obj.hide_render = obj.hide_viewport = True

    labels = {}
    if cfg["template"] == "SIDE_BY_SIDE" and cfg.get("labels"):
        labels = build_labels(cfg["labels"], objects, verts, offsets, fit, basis, aspect, bottom_band, style,
                              geometry.make_collection("80_LABELS", root), cfg.get("layout", "ROW"))
    elif cfg["template"] == "HOLD" and cfg.get("label"):   # M5.5: caption of a single model, in the safe band
        labels = build_labels({templates.MAIN_SLOT: cfg["label"]}, objects, verts, offsets, fit, basis, aspect,
                              bottom_band, style, geometry.make_collection("80_LABELS", root), "ROW")

    # SIDE_BY_SIDE intro starts on the single-model framing (same fit as every other
    # shot: base + all variants at the origin), shifted onto the intro state's slot.
    camera_keys = None
    intro = cfg.get("intro") if cfg["template"] == "SIDE_BY_SIDE" else None
    if intro:
        single = framing.fit_ortho([p for name in objects for p in verts[name]], basis, aspect,
                                   cam_preset.get("margin", 0.07))
        shift = offsets[intro["from_state"]]
        camera_keys = {"name": camera.name,
                       "start": {"location": tuple(a + b for a, b in zip(single["location"], shift)),
                                 "ortho_scale": single["ortho_scale"]},
                       "end": {"location": tuple(fit["location"]), "ortho_scale": fit["ortho_scale"]}}

    slot_components = {sid: {cid: components[obj.name] for cid, obj in parts.items()}
                       for sid, parts in slots.items()}
    plan = templates.plan_shot(shot, states, fps, slot_components, camera_keys)
    hidden_but_animated = sorted(n for n in plan.tracks if n in objects and objects[n].hide_render)
    if hidden_but_animated:  # keys (e.g. fade twins) would silently un-hide them
        raise ValueError(f"{shot_id}: plan animates statically hidden parts {hidden_but_animated}")
    render_objects = dict(objects)
    render_objects[camera.name] = camera
    fade_twins = {}
    if style.get("materials", {}).get("fade_render_method", "DITHERED") == "BLENDED":
        fade_twins = make_fade_twins(plan, objects, render_objects)
    animate.apply_plan(plan, render_objects)
    scene_mod.configure_render(scene, preset, fps, frames, style)
    scene.frame_set(1)
    return ShotContext(shot=shot, cfg=cfg, scene=scene, plan=plan, fps=fps, frame_count=frames,
                       objects=objects, slots=slots, slot_roots=roots, slot_offsets=offsets,
                       visible_variants=visible, components=components, camera=camera,
                       camera_fit=fit, camera_basis=basis, aspect=aspect, bottom_band=bottom_band,
                       ground=ground, render_objects=render_objects, fade_twins=fade_twins,
                       camera_keys=camera_keys, labels=labels)


def focus_motion_points(plan, objects, framed, depsgraph):
    """World vertices of the framed objects at every frame where the plan keys their
    location or rotation (single slot: the slot root is at the origin). Mirrors
    planner/visibility.focus_envelope."""
    from mathutils import Euler, Matrix
    pts = []
    for name in framed:
        frames = sorted({k.frame for k in plan.keys(name, motion.LOC)} | {k.frame for k in plan.keys(name, motion.ROT)})
        if not frames:
            continue
        obj = objects[name]
        ev = obj.evaluated_get(depsgraph)
        mesh = ev.to_mesh()
        try:
            local = [v.co.copy() for v in mesh.vertices]
        finally:
            ev.to_mesh_clear()
        for f in frames:
            loc = plan.sample(name, motion.LOC, f) if motion.LOC in plan.channels(name) else None
            rot = plan.sample(name, motion.ROT, f) if motion.ROT in plan.channels(name) else None
            m = Matrix.LocRotScale(tuple(loc) if loc else tuple(obj.location),
                                   Euler(tuple(rot) if rot else tuple(obj.rotation_euler)), None)
            pts += [tuple(m @ v) for v in local]
    return pts


def build_labels(texts, objects, verts, offsets, fit, basis, aspect, band, style, collection, layout="ROW"):
    """Static captions centred under each model, facing the locked camera, never casting
    shadows: in the reserved bottom band (ROW) or just below each model's row (STACK).
    Built-in font; flat colour (engine.diagram)."""
    from mathutils import Matrix
    from engine import diagram
    cfg = style.get("labels", {})
    material = diagram._flat_material("Label text", cfg.get("color", "#3B3A36"))
    r, u, f = basis
    frame_h = fit["ortho_scale"] / aspect
    out = {}
    for sid, text in texts.items():
        pts = [tuple(p[i] + offsets[sid][i] for i in range(3))
               for name, obj in objects.items() if obj["slot_id"] == sid and not obj.hide_render
               for p in verts[name]]
        coords = framing.frame_coords(pts, fit, basis, aspect)
        xs = [x for x, _ in coords]
        size = float(cfg.get("size", 0.042))
        uy = band / 2 if layout != "STACK" else min(y for _, y in coords) - 0.9 * size
        # Just in front of the camera plane: deeper placements can sink below the ground plane
        # at the bottom of wide (3-model) frames and be hidden by it.
        pos = framing.frame_to_world((min(xs) + max(xs)) / 2, uy, fit, basis, aspect, toward_camera=0.5)
        curve = bpy.data.curves.new(f"LABEL_{sid}_text", type="FONT")
        curve.body = text
        curve.size = size * frame_h
        curve.align_x, curve.align_y = "CENTER", "CENTER"
        obj = bpy.data.objects.new(f"LABEL_{sid}", curve)
        obj.data.materials.append(material)
        obj.matrix_world = Matrix(((r[0], u[0], -f[0], pos[0]), (r[1], u[1], -f[1], pos[1]),
                                   (r[2], u[2], -f[2], pos[2]), (0.0, 0.0, 0.0, 1.0)))
        obj.visible_shadow = False
        obj["label_for"] = sid
        collection.objects.link(obj)
        out[sid] = obj
    return out


def make_fade_twins(plan, objects, render_objects):
    """Blended-transparency twins shown only mid-fade (see motion.split_fades)."""
    blended = {}
    twins = {}
    for name, twin_name in motion.split_fades(plan).items():
        src = objects[name]
        twin = src.copy()          # shares the mesh; keeps parent and parent inverse
        twin.animation_data_clear()
        twin.name = twin_name
        twin["fade_twin_of"] = name
        for col in src.users_collection:
            col.objects.link(twin)
        for slot in twin.material_slots:
            base = slot.material
            if base.name not in blended:
                copy = base.copy()
                copy.name = f"{base.name} (fade)"
                copy.surface_render_method = "BLENDED"
                copy.use_backface_culling = True
                blended[base.name] = copy
            slot.link = "OBJECT"
            slot.material = blended[base.name]
        render_objects[twin_name] = twin
        twins[name] = twin
    return twins
