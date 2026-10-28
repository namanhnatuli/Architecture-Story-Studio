"""Camera director (pure): camera modes -> existing presets (config/visual_planning.json),
continuity groups (shots that must share one locked camera), offline visibility checks
with the same framing maths the engine uses (engine/framing.py)."""
import json
from pathlib import Path

from engine import framing
from engine.arch import assets, semantic

ROOT = Path(__file__).resolve().parent.parent
MODES = ("FULL_OBJECT", "THREE_QUARTER", "SIDE_ELEVATION", "COMPONENT_CLOSEUP", "COMPARISON", "LOCKED_TRANSFORMATION")


def aspect_class(cfg, family):
    for name, a in cfg["aspect_classes"].items():
        if family in a["families"]:
            return name
    raise ValueError(f"no aspect class for family '{family}' in config/visual_planning.json")


def preset_for(cfg, family, mode):
    if mode not in MODES:
        raise ValueError(f"unknown camera mode '{mode}' (known: {', '.join(MODES)})")
    return cfg["aspect_classes"][aspect_class(cfg, family)]["camera"][mode]


def style_presets(root=ROOT):
    return json.loads((Path(root) / "config/visual_style.json").read_text())["camera"]["presets"]


def group_points(base_path, variant_assets):
    """World vertices (planned meshes) of the site and the given library variant assets
    [(path, owner)]; None when a part is not available offline (legacy builders)."""
    pts = []
    if base_path:
        pts += [p for c in assets.plan_cached(base_path, "shared") for p in semantic.world_verts(c)]
    for path, owner in variant_assets:
        if path is None:
            return None
        pts += [p for c in assets.plan_cached(path, owner) for p in semantic.world_verts(c)]
    return pts


def visibility(points, target_points, preset, aspect, band, min_fraction):
    """(ok, detail) for a target seen by the locked camera fitted to `points`."""
    basis = framing.camera_basis(preset["azimuth_degrees"], preset["elevation_degrees"])
    fit = framing.fit_ortho(points, basis, aspect, preset.get("margin", 0.07), band)
    coords = framing.frame_coords(target_points, fit, basis, aspect)
    xs, ys = [c[0] for c in coords], [c[1] for c in coords]
    inside = min(xs) >= -1e-6 and max(xs) <= 1 + 1e-6 and min(ys) >= band - 1e-6 and max(ys) <= 1 + 1e-6
    area = (max(xs) - min(xs)) * (max(ys) - min(ys))
    ok = inside and area >= min_fraction
    return ok, (f"bbox x {min(xs):.2f}-{max(xs):.2f}, y {min(ys):.2f}-{max(ys):.2f}, {area * 100:.1f}% of frame"
                + ("" if inside else "; outside the frame / safe band") +
                ("" if area >= min_fraction else "; too small to read: use COMPONENT_CLOSEUP"))
