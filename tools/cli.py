#!/usr/bin/env python3
"""Mac-first stdlib CLI: validate, render shots headless with Blender, encode with FFmpeg."""
import argparse
import hashlib
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

ENGINE = ROOT / "engine" / "render_scene.py"


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


def ffprobe_bin():
    return shutil.which("ffprobe")


def project_path(slug):
    if not slug or not all(ch.islower() or ch.isdigit() or ch == "-" for ch in slug):
        raise ValueError("Project slug invalid. Use lowercase a-z, 0-9, hyphens.")
    p = ROOT / "projects" / slug
    if not (p / "project.json").exists():
        raise FileNotFoundError(f"Missing project: {p}")
    return p


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


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


def blender_command(p, mode, preset, *extra):
    b = blender_bin()
    if not b:
        raise SystemExit("Blender not found; see QUICKSTART_MAC.md")
    return [b, "--background", "--factory-startup", "--python-exit-code", "1", "--python", str(ENGINE),
            "--", "--project", str(p), "--mode", mode, "--preset", preset, *extra]


def slug_name(p):
    return read_json(p / "project.json")["slug"].replace("-", "_")


def shots(p):
    return read_json(p / "storyboard/storyboard.json")["shots"]


def expected_frames(p, shot):
    return round(read_json(p / "project.json")["fps"] * shot["duration_seconds"])


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
    print("MCP is optional; the CLI never needs it.")
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


# ---------------------------------------------------------------- stills
def do_still(p, preset):
    do_validate(p, final=(preset == "final"))
    run_logged(blender_command(p, "keystills", preset), p / "qa" / f"render_keystills_{preset}.log")
    story = read_json(p / "storyboard/storyboard.json")
    outputs = [p / "output" / "stills" / f"{s['id']}.png" for s in story.get("key_stills", [])]
    outputs.append(p / "output" / f"{slug_name(p)}_still.png")
    missing = [str(o) for o in outputs if not o.is_file() or o.stat().st_size == 0]
    if missing:
        raise SystemExit("Render returned success but stills are missing/empty: " + ", ".join(missing))
    for o in outputs:
        print("SUCCESS:", o)


# ---------------------------------------------------------------- shots
def shot_cache_key(p, shot, preset):
    """Hash of everything that changes a shot's pixels; unchanged shots are not re-rendered."""
    h = hashlib.sha256()
    h.update(json.dumps(shot, sort_keys=True).encode())
    h.update(preset.encode())
    for path in [p / "project.json", p / "storyboard/states.json", ROOT / "config/visual_style.json",
                 ROOT / "config/render_presets.json", *sorted((ROOT / "engine").glob("*.py"))]:
        h.update(path.name.encode())
        h.update(path.read_bytes())
    return h.hexdigest()


def render_shot(p, shot, preset, force=False):
    sid = shot["id"]
    seq = p / "renders" / preset / sid
    manifest = seq / "render_manifest.json"
    key = shot_cache_key(p, shot, preset)
    expected = expected_frames(p, shot)
    frames = sorted(seq.glob("frame_*.png"))
    if not force and manifest.is_file() and read_json(manifest).get("cache_key") == key and len(frames) == expected:
        print(f"CACHED: {sid} ({expected} frames, inputs unchanged)")
        return "cached"
    for frame in frames:  # stale frames of this shot only, inside the project
        frame.unlink()
    run_logged(blender_command(p, "animation", preset, "--shot", sid), p / "qa" / f"render_{sid}_{preset}.log")
    frames = sorted(seq.glob("frame_*.png"))
    if len(frames) != expected:
        raise SystemExit(f"{sid}: expected {expected} frames, found {len(frames)}. See logs.")
    manifest.write_text(json.dumps({"shot": sid, "cache_key": key, "frames": expected,
                                    "rendered_utc": datetime.now(timezone.utc).isoformat()}, indent=2))
    print(f"SUCCESS: {sid} {len(frames)} PNG frames")
    return "rendered"


def require_frames(p, shot, preset):
    seq = p / "renders" / preset / shot["id"]
    found = len(list(seq.glob("frame_*.png")))
    if found != expected_frames(p, shot):
        raise SystemExit(f"Refusing encode: {shot['id']} expected {expected_frames(p, shot)} frames, found {found}")
    return seq


def encode_shot(p, shot, preset):
    ff = ffmpeg_bin()
    if not ff:
        raise SystemExit("FFmpeg not found. Install using brew install ffmpeg.")
    project = read_json(p / "project.json")
    settings = read_json(ROOT / "config/render_presets.json")
    seq = require_frames(p, shot, preset)
    target = p / "output" / "shots" / f"{shot['id']}.mp4"
    target.parent.mkdir(parents=True, exist_ok=True)
    run_logged([ff, "-y", "-framerate", str(project["fps"]), "-start_number", "1", "-i", str(seq / "frame_%04d.png"),
                "-c:v", settings["output_codec"], "-crf", str(settings["output_crf"]), "-pix_fmt", "yuv420p",
                "-movflags", "+faststart", str(target)], p / "qa" / f"ffmpeg_{shot['id']}.log")
    return target


def encode_full(p, preset):
    ff = ffmpeg_bin()
    project = read_json(p / "project.json")
    settings = read_json(ROOT / "config/render_presets.json")
    cmd = [ff, "-y"]
    all_shots = shots(p)
    for shot in all_shots:
        seq = require_frames(p, shot, preset)
        cmd += ["-framerate", str(project["fps"]), "-start_number", "1", "-i", str(seq / "frame_%04d.png")]
    chain = "".join(f"[{i}:v]" for i in range(len(all_shots)))
    target = p / "output" / f"{slug_name(p)}_preview.mp4"
    cmd += ["-filter_complex", f"{chain}concat=n={len(all_shots)}:v=1:a=0[v]", "-map", "[v]",
            "-c:v", settings["output_codec"], "-crf", str(settings["output_crf"]), "-pix_fmt", "yuv420p",
            "-movflags", "+faststart", str(target)]
    run_logged(cmd, p / "qa" / "ffmpeg_encode.log")
    if not target.is_file() or target.stat().st_size == 0:
        raise SystemExit("FFmpeg returned success but preview MP4 is missing/empty")
    return target


def probe(path):
    out = subprocess.run([ffprobe_bin(), "-v", "error", "-select_streams", "v:0", "-count_frames",
                          "-show_entries", "stream=codec_name,width,height,pix_fmt,r_frame_rate,nb_read_frames",
                          "-show_entries", "format=duration", "-of", "json", str(path)],
                         text=True, capture_output=True, check=True)
    data = json.loads(out.stdout)
    stream = data["streams"][0]
    return {"codec": stream["codec_name"], "width": stream["width"], "height": stream["height"],
            "pix_fmt": stream["pix_fmt"], "fps": stream["r_frame_rate"],
            "frames": int(stream["nb_read_frames"]), "duration": float(data["format"]["duration"])}


def black_segments(path):
    out = subprocess.run([ffmpeg_bin(), "-v", "info", "-i", str(path), "-vf", "blackdetect=d=0.04:pix_th=0.10",
                          "-an", "-f", "null", "-"], text=True, capture_output=True)
    return out.stderr.count("black_start")


def qa_sheets(p, preset):
    """Contact sheet of the full preview + 0/25/50/75/100% strips for every animated shot."""
    ff = ffmpeg_bin()
    project = read_json(p / "project.json")
    sheets = []
    full = p / "output" / f"{slug_name(p)}_preview.mp4"
    every = project["fps"]
    tiles = max(1, round(project["duration_seconds"]))
    cols = 5
    rows = (tiles + cols - 1) // cols
    contact = p / "qa" / "contact_sheet_preview.png"
    subprocess.run([ff, "-v", "error", "-y", "-i", str(full), "-vf",
                    f"select='not(mod(n\\,{every}))',scale=256:-1,tile={cols}x{rows}:padding=2:color=white",
                    "-frames:v", "1", str(contact)], check=True)
    sheets.append(contact)
    for shot in shots(p):
        n = expected_frames(p, shot)
        picks = [1, max(1, round(n * .25)), max(1, round(n * .5)), max(1, round(n * .75)), n]
        seq = p / "renders" / preset / shot["id"]
        cmd = [ff, "-v", "error", "-y"]
        for f in picks:
            cmd += ["-i", str(seq / f"frame_{f:04d}.png")]
        scaled = "".join(f"[{i}]scale=320:-1,pad=iw+4:ih:0:0:white[s{i}];" for i in range(5))
        target = p / "qa" / f"progress_{shot['id']}.png"
        cmd += ["-filter_complex", scaled + "".join(f"[s{i}]" for i in range(5)) + "hstack=inputs=5", str(target)]
        subprocess.run(cmd, check=True)
        sheets.append(target)
    return sheets


def media_qa(p, preset, outputs):
    report = {"utc": datetime.now(timezone.utc).isoformat(), "preset": preset, "files": {}}
    problems = []
    expected_total = 0
    for shot in shots(p):
        expected_total += expected_frames(p, shot)
    for label, path, expected in outputs:
        info = probe(path)
        info["black_segments"] = black_segments(path)
        info["size_bytes"] = path.stat().st_size
        report["files"][str(path.relative_to(p))] = info
        if info["frames"] != expected:
            problems.append(f"{label}: {info['frames']} frames, expected {expected}")
        if info["black_segments"]:
            problems.append(f"{label}: {info['black_segments']} black segment(s)")
    report["expected_total_frames"] = expected_total
    report["problems"] = problems
    report["sheets"] = [str(s.relative_to(p)) for s in qa_sheets(p, preset)]
    target = p / "qa" / "preview_media_report.json"
    target.write_text(json.dumps(report, indent=2))
    for name, info in report["files"].items():
        print(f"  {name}: {info['codec']} {info['width']}x{info['height']} {info['fps']} fps, "
              f"{info['frames']} frames, {info['duration']:.3f}s, black segments {info['black_segments']}")
    if problems:
        raise SystemExit("Media QA failed: " + "; ".join(problems))
    print(f"Media QA: PASS => {target}")
    for s in report["sheets"]:
        print("Sheet:", p / s)


def do_encode(p, preset):
    if preset == "final":
        do_validate(p, final=True)
    if not ffmpeg_bin() or not ffprobe_bin():
        raise SystemExit("FFmpeg/ffprobe not found. Install using brew install ffmpeg.")
    outputs = []
    for shot in shots(p):
        outputs.append((shot["id"], encode_shot(p, shot, preset), expected_frames(p, shot)))
    full = encode_full(p, preset)
    total = sum(expected_frames(p, s) for s in shots(p))
    outputs.append(("full", full, total))
    media_qa(p, preset, outputs)
    print("SUCCESS:", full)


def do_preview(p, preset, force=False):
    do_validate(p, final=(preset == "final"))
    for shot in shots(p):
        render_shot(p, shot, preset, force)
    if ffmpeg_bin():
        do_encode(p, preset)
    else:
        print("Frames created; FFmpeg absent, so MP4 not encoded.")


def do_shot(p, shot_id, preset, force=False):
    do_validate(p, final=(preset == "final"))
    match = [s for s in shots(p) if s["id"] == shot_id]
    if not match:
        raise SystemExit(f"Unknown shot {shot_id}; shots: {', '.join(s['id'] for s in shots(p))}")
    render_shot(p, match[0], preset, force)
    if ffmpeg_bin():
        target = encode_shot(p, match[0], preset)
        print("SUCCESS:", target)


def do_check_blender(p, preset):
    do_validate(p)
    report = p / "qa" / "blender_checks.json"
    cmd = blender_command(p, "check", preset, "--report", str(report))
    logfile = p / "qa" / "blender_checks.log"
    try:
        run_logged(cmd, logfile)
    finally:
        if report.is_file():
            data = read_json(report)
            for r in data["results"]:
                if r["status"] != "PASS":
                    print(f"FAIL {r['shot']} {r['check']}: {r['detail']}")
            s = data["summary"]
            print(f"Blender QA: {s['passed']}/{s['total']} passed => {report}")


def main():
    parser = argparse.ArgumentParser(description="Architecture Story Studio — Mac M4 pilot CLI")
    parser.add_argument("command", choices=["doctor", "validate", "still", "preview", "shot", "encode",
                                            "check-blender", "final-gate"])
    parser.add_argument("--project", default="roof-evolution", help="Project slug in projects/")
    parser.add_argument("--preset", default="preview", choices=["preview", "review", "final"])
    parser.add_argument("--shot", help="Shot id for the `shot` command, e.g. SC_002")
    parser.add_argument("--force", action="store_true", help="Re-render shots even if cached")
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
        do_still(p, args.preset)
    elif args.command == "preview":
        do_preview(p, args.preset, args.force)
    elif args.command == "shot":
        if not args.shot:
            raise SystemExit("--shot is required, e.g. --shot SC_002")
        do_shot(p, args.shot, args.preset, args.force)
    elif args.command == "encode":
        do_encode(p, args.preset)
    elif args.command == "check-blender":
        do_check_blender(p, args.preset)


if __name__ == "__main__":
    main()
