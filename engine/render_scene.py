"""Blender entry point, always headless:

  Blender --background --factory-startup --python-exit-code 1 --python engine/render_scene.py -- \
      --project <dir> --mode <keystills|still|animation|check> [--shot SC_001] [--preset preview]

keystills  render every storyboard key still (also the legacy output/<slug>_still.png)
still      one frame of one shot: --shot plus --frame or --time, written to --output
animation  one shot (or all shots without --shot) as renders/<preset>/<shot>/frame_####.png;
           --resume keeps frame files already on disk (M7 interrupted-render recovery)
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


PNG_END = b"\x00\x00\x00\x00IEND\xaeB`\x82"


def complete_png(path):
    try:
        with open(path, "rb") as f:
            head = f.read(8)
            f.seek(-12, 2)
            return head == b"\x89PNG\r\n\x1a\n" and f.read(12) == PNG_END
    except OSError:
        return False


def reuse_plan(ctx, allow=True):
    """M7 render optimisation: (strategy, sources, reason). sources[f-1] is the frame whose image
    frame f repeats (f itself when it must be rendered). Two frames are identical when every
    plan-keyed channel samples to the same value; this is only trusted when the plan is the ONLY
    animation in the scene (no other actions or drivers, no motion blur), else every frame renders."""
    import math
    scene, plan, n = ctx.scene, ctx.plan, ctx.frame_count
    kind = "2D" if ctx.shot.get("visual_type") == "MOTION_GRAPHICS" else "3D"
    tracked = set(plan.tracks)
    every = list(range(1, n + 1))

    def animated(idb):
        ad = getattr(idb, "animation_data", None)
        return bool(ad and (ad.action or len(ad.drivers)))
    stray = [o.name for o in scene.objects if animated(o) and o.name not in tracked]
    cams = {o.data.name for o in scene.objects if o.type == "CAMERA" and o.name in tracked}
    stray += [d.name for coll in (bpy.data.materials, bpy.data.worlds, bpy.data.node_groups, bpy.data.lights,
                                  bpy.data.meshes, bpy.data.curves) for d in coll if animated(d)]
    stray += [c.name for c in bpy.data.cameras if animated(c) and c.name not in cams]
    if not allow:
        return "FALLBACK_FULL_BLENDER", every, "frame reuse disabled (--no-reuse)"
    if scene.render.use_motion_blur:
        return "FALLBACK_FULL_BLENDER", every, "motion blur depends on neighbouring frames"
    if stray:
        return "FALLBACK_FULL_BLENDER", every, f"animation outside the plan: {stray[:5]}"
    channels = [(name, ch) for name in sorted(tracked) for ch in plan.channels(name)]
    sources, last, src = [], None, 1
    for f in every:
        sig = tuple(tuple(round(float(v), 9) for v in plan.sample(name, ch, f)) for name, ch in channels)
        if f == 1 or sig != last:
            src, last = f, sig
        sources.append(src)
        if any(math.isnan(float(v)) for t in sig for v in t):
            return "FALLBACK_FULL_BLENDER", every, f"NaN in the plan at frame {f}"
    unique = len(set(sources))
    strategy = f"ANIMATED_{kind}" if unique == n else f"STATIC_{kind}" if unique == 1 else "HYBRID"
    return strategy, sources, f"{unique} distinct frames of {n}"


def render_with_reuse(ctx, seq, sources, resume):
    """Render each distinct frame once; repeated frames are hard links to their source frame."""
    import os
    counts = {"rendered": 0, "reused": 0, "kept": 0}
    for f, src in enumerate(sources, 1):
        out = seq / f"frame_{f:04d}.png"
        if src == f:
            if resume and complete_png(out):
                counts["kept"] += 1
                continue
            if out.exists():
                out.unlink()   # never write into a file that may be linked to another frame
            ctx.scene.frame_set(f)
            ctx.scene.render.filepath = str(out)
            bpy.ops.render.render(write_still=True)
            counts["rendered"] += 1
        else:
            source = seq / f"frame_{src:04d}.png"
            if out.exists():
                out.unlink()
            os.link(source, out)
            counts["reused"] += 1
    return counts


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", help="project directory (not needed for --mode asset)")
    parser.add_argument("--mode", choices=["keystills", "still", "animation", "check", "asset", "verify-reuse",
                                           "reuse-report"], required=True)
    parser.add_argument("--asset", help="asset mode: architecture asset spec (asset_library/...json)")
    parser.add_argument("--views", default="three_quarter,elevation,top,exploded", help="asset mode: views to render")
    presets = {k: v for k, v in json.loads((ROOT / "config/render_presets.json").read_text()).items()
               if isinstance(v, dict)}
    parser.add_argument("--preset", choices=sorted(presets), default="preview")
    parser.add_argument("--shot")
    parser.add_argument("--frame", type=int)
    parser.add_argument("--time", type=float)
    parser.add_argument("--output")
    parser.add_argument("--report")
    parser.add_argument("--resume", action="store_true", help="animation: skip frames already on disk")
    parser.add_argument("--no-reuse", action="store_true", help="animation: render every frame (no static-frame reuse)")
    parser.add_argument("--frames", help="verify-reuse: comma list of frames to re-render and compare")
    args = parser.parse_args(argv)
    if args.mode == "animation" and args.preset == "production_test":
        parser.error("production_test is for selected stills only, never a full sequence")
    if args.mode == "asset":   # M4: stand-alone architecture asset (previews + QA), no project
        from engine.arch import asset_scene
        style = json.loads((ROOT / "config/visual_style.json").read_text())
        preset = {k: v for k, v in json.loads((ROOT / "config/render_presets.json").read_text()).items()
                  if isinstance(v, dict)}[args.preset]
        report = asset_scene.run_qa(args.asset, style, preset)
        if args.views:
            report["views"] = asset_scene.render_views(args.asset, style, preset, Path(args.output),
                                                       [v for v in args.views.split(",") if v])
        Path(args.report).parent.mkdir(parents=True, exist_ok=True)
        Path(args.report).write_text(json.dumps(report, indent=2), encoding="utf-8")
        failed = [r for r in report["results"] if r["status"] != "PASS"]
        print(f"[ASSET] {report['asset_id']}: {len(report['results']) - len(failed)}/{len(report['results'])} checks => {args.report}")
        sys.exit(3 if failed else 0)
    if not args.project:
        parser.error("--project is required")
    project_dir = Path(args.project).resolve()
    data = shot_builder.load_project(project_dir, args.preset)

    if args.mode == "check":
        from engine import qa_checks
        report = qa_checks.run_all(project_dir, args.preset, args.shot.split(",") if args.shot else None)
        target = Path(args.report) if args.report else project_dir / "qa" / "blender_checks.json"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(report, indent=2), encoding="utf-8")
        s = report["summary"]
        print(f"[QA] {s['passed']} passed, {s['failed']} failed => {target}")
        if s["failed"]:
            sys.exit(3)
        return

    if args.mode == "reuse-report":   # M7: render strategy of every shot, without rendering (for estimates)
        rows = []
        for shot in data["story"]["shots"]:
            ctx = shot_builder.build_shot(project_dir, shot["id"], args.preset)
            strategy, sources, reason = reuse_plan(ctx)
            rows.append({"shot": shot["id"], "strategy": strategy, "frames": ctx.frame_count,
                         "distinct_frames": len(set(sources)), "reason": reason})
        Path(args.report).write_text(json.dumps({"preset": args.preset, "shots": rows}, indent=2))
        print(f"[REUSE] {sum(r['distinct_frames'] for r in rows)} of {sum(r['frames'] for r in rows)} frames to render")
        return

    if args.mode == "verify-reuse":   # M7: a reused frame must equal a direct render of that frame
        import numpy as np
        ctx = shot_builder.build_shot(project_dir, args.shot, args.preset)
        seq = project_dir / "renders" / args.preset / args.shot
        _, sources, _ = reuse_plan(ctx)

        def pixels(path):
            img = bpy.data.images.load(str(path))
            arr = np.empty(len(img.pixels), dtype=np.float32)
            img.pixels.foreach_get(arr)
            bpy.data.images.remove(img)
            return arr

        def compare(a, b):
            if a.shape != b.shape:
                return {"max_abs_diff": 1.0, "differing_pixels": None, "psnr_db": 0.0}
            d = np.abs(a - b)
            mse = float(np.mean(d ** 2))
            return {"max_abs_diff": float(d.max()), "differing_pixels": int(np.count_nonzero(d.reshape(-1, 4).max(axis=1))),
                    "psnr_db": float("inf") if mse == 0 else round(float(10 * np.log10(1.0 / mse)), 2)}
        rows = []
        for f in [int(x) for x in args.frames.split(",")]:
            src = sources[f - 1]
            direct = Path(args.output) / f"{args.shot}_direct_{f:04d}.png"
            render_frame(ctx, f, direct)
            row = {"frame": f, "source_frame": src, **compare(pixels(direct), pixels(seq / f"frame_{f:04d}.png"))}
            # noise floor: the stored source frame against a fresh direct render of that same frame
            again = Path(args.output) / f"{args.shot}_direct_{src:04d}.png"
            render_frame(ctx, src, again)
            floor = compare(pixels(again), pixels(seq / f"frame_{src:04d}.png"))
            row["noise_floor"] = floor
            row["identical"] = row["max_abs_diff"] == 0.0
            row["within_render_noise"] = bool(row["max_abs_diff"] <= max(floor["max_abs_diff"], 1.0 / 255) + 1e-6) \
                and bool(row["psnr_db"] >= 50.0)
            rows.append(row)
        Path(args.report).write_text(json.dumps({"shot": args.shot, "preset": args.preset, "frames": rows}, indent=2))
        print("[VERIFY] " + json.dumps(rows))
        return

    if args.mode == "still" and args.shot is None:
        args.mode = "keystills"  # v0.1 invocation: `--mode still` with no shot

    if args.mode == "keystills":
        stills = data["story"].get("key_stills", [])
        if not stills:
            raise SystemExit("storyboard.json has no key_stills")
        folder = "stills" if args.preset == "preview" else f"stills_{args.preset}"
        for i, still in enumerate(stills):
            ctx = shot_builder.build_shot(project_dir, still["shot"], args.preset)
            frame = resolve_key_still(ctx, still)
            render_frame(ctx, frame, project_dir / "output" / folder / f"{still['id']}.png")
            if i == 0 and args.preset == "preview":
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
        # The caller (tools/cli.py) removed every frame that is not a complete PNG of the same inputs.
        strategy, sources, reason = reuse_plan(ctx, allow=not args.no_reuse)
        if strategy == "FALLBACK_FULL_BLENDER":
            ctx.scene.render.filepath = str(seq / "frame_")
            ctx.scene.render.use_overwrite = not args.resume
            ctx.scene.render.use_placeholder = False
            bpy.ops.render.render(animation=True)
            counts = {"rendered": ctx.frame_count, "reused": 0, "kept": 0}
        else:
            counts = render_with_reuse(ctx, seq, sources, args.resume)
        runs = []   # [source frame, first reused frame, last reused frame]
        for f, src in enumerate(sources, 1):
            if src != f:
                if runs and runs[-1][0] == src and runs[-1][2] == f - 1:
                    runs[-1][2] = f
                else:
                    runs.append([src, f, f])
        (seq / "render_strategy.json").write_text(json.dumps(
            {"shot": shot_id, "strategy": strategy, "reason": reason, "frames": ctx.frame_count,
             "distinct_frames": len(set(sources)), **counts, "reused_runs": runs}, indent=2))
        print(f"[STRATEGY] {shot_id}: {strategy} ({reason}); rendered {counts['rendered']}, "
              f"reused {counts['reused']}, kept {counts['kept']}")
        print(f"[SUCCESS] {shot_id}: {ctx.frame_count} frames => {seq}")
        print("[MARKERS] " + json.dumps({"shot": shot_id, **ctx.plan.markers}))


if __name__ == "__main__":
    try:
        main()
    except motion.PlanError as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(2)
