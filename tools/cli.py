#!/usr/bin/env python3
"""Mac-first stdlib CLI for procedural roof transition pilot."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from datetime import datetime, timezone

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from tools.validator import validate_project


def blender_bin():
    override = os.environ.get("BLENDER_BIN")
    if override:
        p = Path(override).expanduser()
        return str(p) if p.is_file() else None
    standard = Path("/Applications/Blender.app/Contents/MacOS/Blender")
    if standard.is_file():
        return str(standard)
    return shutil.which("blender")


def ffmpeg_bin():
    return shutil.which("ffmpeg")


def project_path(slug):
    if not slug or not all(ch.islower() or ch.isdigit() or ch == "-" for ch in slug):
        raise ValueError("Project slug invalid. Use lowercase a-z, 0-9, hyphens.")
    p = ROOT / "projects" / slug
    if not (p / "project.json").exists():
        raise FileNotFoundError(f"Missing project: {p}")
    return p


def run_logged(command, logfile):
    logfile.parent.mkdir(parents=True, exist_ok=True)
    print("Running:", " ".join(map(str, command)), flush=True)
    with logfile.open("w", encoding="utf-8") as f:
        f.write("UTC: " + datetime.now(timezone.utc).isoformat() + "\n")
        f.write("Command: " + " ".join(map(str, command)) + "\n\n")
        f.flush()
        result = subprocess.run(command, cwd=ROOT, stdout=f, stderr=subprocess.STDOUT)
    if result.returncode != 0:
        print(f"Failed ({result.returncode}). Inspect log: {logfile}", file=sys.stderr)
        try:
            tail = logfile.read_text(encoding="utf-8", errors="replace").splitlines()[-18:]
            print("\n".join(tail), file=sys.stderr)
        except Exception:
            pass
        raise SystemExit(result.returncode)
    print(f"Log: {logfile}")


def do_doctor():
    print("Architecture Story Studio — environment check")
    print("OS:", sys.platform)
    print("Python:", sys.version.split()[0])
    b = blender_bin()
    f = ffmpeg_bin()
    print("Blender:", b or "NOT FOUND")
    print("FFmpeg:", f or "NOT FOUND")
    for name, binary in (("Blender", b), ("FFmpeg", f)):
        if binary:
            result = subprocess.run([binary, "--version" if name=="Blender" else "-version"],
                                    text=True, capture_output=True, timeout=20)
            print(name + " version:", (result.stdout or result.stderr).splitlines()[0])
    if not b:
        print("Install Blender from blender.org; set BLENDER_BIN if nonstandard path.")
    if not f:
        print("Install FFmpeg via brew install ffmpeg (encoding only).")
    print("MCP is optional; do not install until scene render works.")
    return bool(b)


def do_validate(p, final=False):
    errors, warnings = validate_project(p, final)
    for msg in warnings:
        print("WARNING:", msg)
    for msg in errors:
        print("ERROR:", msg)
    if errors:
        raise SystemExit(2)
    print("PASS: structural validation" if not final else "PASS: final gate")


def do_render(p, mode, preset):
    do_validate(p, final=(preset == "final"))
    b = blender_bin()
    if not b:
        raise SystemExit("Blender not found; see QUICKSTART_MAC.md")
    cmd = [b, "--background", "--factory-startup", "--python", str(ROOT / "engine/render_scene.py"),
           "--", "--project", str(p), "--mode", mode, "--preset", preset]
    run_logged(cmd, p / "qa" / f"render_{mode}_{preset}.log")
    if mode == "still":
        still = p / "output" / "roof_evolution_still.png"
        if not still.is_file() or still.stat().st_size == 0:
            raise SystemExit("Render command returned success but still PNG is missing/empty")
        print("SUCCESS:", still)
    else:
        frames = sorted((p / "renders" / preset).glob("frame_*.png"))
        project = json.loads((p / "project.json").read_text())
        expected = round(project["fps"] * project["duration_seconds"])
        if len(frames) != expected:
            raise SystemExit(f"Expected {expected} frames, found {len(frames)}. See logs.")
        print(f"SUCCESS: {len(frames)} PNG frames")


def do_encode(p, preset):
    if preset == "final":
        do_validate(p, final=True)
    ff = ffmpeg_bin()
    if not ff:
        raise SystemExit("FFmpeg not found. Install using brew install ffmpeg.")
    project = json.loads((p / "project.json").read_text())
    settings = json.loads((ROOT / "config/render_presets.json").read_text())
    seq = p / "renders" / preset
    frames = sorted(seq.glob("frame_*.png"))
    expected = round(project["fps"] * project["duration_seconds"])
    if len(frames) != expected:
        raise SystemExit(f"Refusing encode: expected {expected} frames, found {len(frames)}")
    target = p / "output" / "roof_evolution_preview.mp4"
    target.parent.mkdir(parents=True, exist_ok=True)
    cmd = [ff, "-y", "-framerate", str(project["fps"]), "-start_number", "1", "-i", str(seq / "frame_%04d.png"),
           "-c:v", settings["output_codec"], "-crf", str(settings["output_crf"]), "-pix_fmt", "yuv420p",
           "-movflags", "+faststart", str(target)]
    run_logged(cmd, p / "qa" / "ffmpeg_encode.log")
    if not target.is_file() or target.stat().st_size == 0:
        raise SystemExit("FFmpeg returned success but preview MP4 is missing/empty")
    print("SUCCESS:", target)


def main():
    parser = argparse.ArgumentParser(description="Architecture Story Studio — Mac M4 pilot CLI")
    parser.add_argument("command", choices=["doctor", "validate", "still", "preview", "encode", "final-gate"])
    parser.add_argument("--project", default="roof-evolution", help="Project slug in projects/")
    parser.add_argument("--preset", default="preview", choices=["preview", "review", "final"])
    args = parser.parse_args()
    if args.command == "doctor":
        do_doctor()
        return
    p = project_path(args.project)
    if args.command == "validate":
        do_validate(p)
    elif args.command == "final-gate":
        do_validate(p, final=True)
    elif args.command == "still":
        do_render(p, "still", args.preset)
    elif args.command == "preview":
        do_render(p, "animation", args.preset)
        if ffmpeg_bin():
            do_encode(p, args.preset)
        else:
            print("Frames created; FFmpeg absent, so MP4 not encoded.")
    elif args.command == "encode":
        do_encode(p, args.preset)


if __name__ == "__main__":
    main()
