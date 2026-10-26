"""Entry point: Blender --background --python engine/render_scene.py -- --project <path> --mode <still|animation>."""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import bpy
from engine.geometry import build_base, build_roof
from engine.scene import make_materials, build_camera_and_lights, configure_render
from engine.transform import keyframe_replace_parts


def load(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    argv = sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else []
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True)
    parser.add_argument("--mode", choices=["still", "animation"], required=True)
    parser.add_argument("--preset", choices=["preview", "review", "final"], default="preview")
    args = parser.parse_args(argv)
    project_dir = Path(args.project).resolve()
    if not (project_dir / "project.json").exists():
        raise SystemExit(f"Missing project.json in {project_dir}")
    project = load(project_dir / "project.json")
    style = load(ROOT / "config/visual_style.json")
    presets = load(ROOT / "config/render_presets.json")
    states = load(project_dir / "storyboard/states.json")

    # Deliberately simple pilot implementation, not a generic architectural asset import.
    if states["building_type"] != "simple_rectangular_house":
        raise ValueError("MVP renderer supports simple_rectangular_house only")
    if len(states["variants"]) != 2:
        raise ValueError("MVP expects exactly two roof variants")

    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for col in list(bpy.data.collections):
        if col.users == 0:
            bpy.data.collections.remove(col)

    materials = make_materials(style)
    dims, _ = build_base(materials)
    a = build_roof(states["variants"][0], dims, materials)
    b = build_roof(states["variants"][1], dims, materials)
    keyframe_replace_parts(a, b, int(project["fps"]))
    build_camera_and_lights(style)
    configure_render(presets[args.preset], project)

    (project_dir / "scenes").mkdir(parents=True, exist_ok=True)
    blend_file = project_dir / "scenes" / "roof_evolution_preview.blend"
    bpy.ops.wm.save_as_mainfile(filepath=str(blend_file))

    scene = bpy.context.scene
    if args.mode == "still":
        scene.frame_set(round(5.4*int(project["fps"])))
        output = project_dir / "output" / "roof_evolution_still.png"
        output.parent.mkdir(parents=True, exist_ok=True)
        scene.render.filepath = str(output)
        bpy.ops.render.render(write_still=True)
        print(f"[SUCCESS] still => {output}")
    else:
        seq = project_dir / "renders" / args.preset
        seq.mkdir(parents=True, exist_ok=True)
        scene.render.filepath = str(seq / "frame_")
        bpy.ops.render.render(animation=True)
        print(f"[SUCCESS] animation frames => {seq}")


if __name__ == "__main__":
    main()
