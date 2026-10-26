"""Blender entry point, always headless:

  Blender --background --factory-startup --python-exit-code 1 --python engine/render_scene.py -- \
      --project <dir> --mode <keystills|still|animation|check> [--shot SC_001] [--preset preview]

keystills  render every storyboard key still (also the legacy output/<slug>_still.png)
still      one frame of one shot: --shot plus --frame or --time, written to --output
animation  one shot (or all shots without --shot) as renders/<preset>/<shot>/frame_####.png
check      run engine/qa_checks.py and write a JSON report (--report)
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import bpy

from engine import motion, shot_builder, templates


def legacy_still_name(project):
    return f"{project['slug'].replace('-', '_')}_still.png"


def resolve_key_still(ctx, still):
    if "marker" in still:
        if still["marker"] not in ctx.plan.markers:
            raise ValueError(f"key still {still['id']}: marker '{still['marker']}' not produced by "
                             f"{ctx.cfg['template']} (markers: {sorted(ctx.plan.markers)})")
        return ctx.plan.markers[still["marker"]]
    return templates.key_still_frame(ctx.shot, float(still["time_seconds"]), ctx.fps)


def render_frame(ctx, frame, output):
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    ctx.scene.frame_set(frame)
    ctx.scene.render.filepath = str(output)
    bpy.ops.render.render(write_still=True)
    print(f"[SUCCESS] still {ctx.shot['id']} frame {frame} => {output}")


def save_blend(ctx, project_dir):
    bpy.context.preferences.filepaths.save_version = 0  # no .blend1 backups
    target = project_dir / "scenes" / f"{ctx.shot['id']}.blend"
    target.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(target), copy=True)
    print(f"[INFO] scene saved => {target}")


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True)
    parser.add_argument("--mode", choices=["keystills", "still", "animation", "check"], required=True)
    parser.add_argument("--preset", choices=["preview", "review", "final"], default="preview")
    parser.add_argument("--shot")
    parser.add_argument("--frame", type=int)
    parser.add_argument("--time", type=float)
    parser.add_argument("--output")
    parser.add_argument("--report")
    args = parser.parse_args(argv)
    project_dir = Path(args.project).resolve()
    data = shot_builder.load_project(project_dir, args.preset)

    if args.mode == "check":
        from engine import qa_checks
        report = qa_checks.run_all(project_dir, args.preset)
        target = Path(args.report) if args.report else project_dir / "qa" / "blender_checks.json"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(report, indent=2), encoding="utf-8")
        s = report["summary"]
        print(f"[QA] {s['passed']} passed, {s['failed']} failed => {target}")
        if s["failed"]:
            sys.exit(3)
        return

    if args.mode == "still" and args.shot is None:
        args.mode = "keystills"  # v0.1 invocation: `--mode still` with no shot

    if args.mode == "keystills":
        stills = data["story"].get("key_stills", [])
        if not stills:
            raise SystemExit("storyboard.json has no key_stills")
        for i, still in enumerate(stills):
            ctx = shot_builder.build_shot(project_dir, still["shot"], args.preset)
            frame = resolve_key_still(ctx, still)
            render_frame(ctx, frame, project_dir / "output" / "stills" / f"{still['id']}.png")
            if i == 0:
                render_frame(ctx, frame, project_dir / "output" / legacy_still_name(data["project"]))
        return

    if args.mode == "still":
        ctx = shot_builder.build_shot(project_dir, args.shot, args.preset)
        if args.frame is not None:
            frame = args.frame
        elif args.time is not None:
            frame = templates.key_still_frame(ctx.shot, args.time, ctx.fps)
        else:
            frame = ctx.plan.markers.get("middle", 1)
        if not 1 <= frame <= ctx.frame_count:
            raise SystemExit(f"frame {frame} outside {args.shot} (1..{ctx.frame_count})")
        output = args.output or project_dir / "output" / "stills" / f"{args.shot}_f{frame:04d}.png"
        render_frame(ctx, frame, output)
        return

    shot_ids = [args.shot] if args.shot else [s["id"] for s in data["story"]["shots"]]
    for shot_id in shot_ids:
        ctx = shot_builder.build_shot(project_dir, shot_id, args.preset)
        save_blend(ctx, project_dir)
        seq = project_dir / "renders" / args.preset / shot_id
        seq.mkdir(parents=True, exist_ok=True)
        ctx.scene.render.filepath = str(seq / "frame_")
        bpy.ops.render.render(animation=True)
        print(f"[SUCCESS] {shot_id}: {ctx.frame_count} frames => {seq}")
        print("[MARKERS] " + json.dumps({"shot": shot_id, **ctx.plan.markers}))


if __name__ == "__main__":
    try:
        main()
    except motion.PlanError as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(2)
