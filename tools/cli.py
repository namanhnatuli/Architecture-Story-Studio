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
    cmd = [b, "--background", "--factory-startup", "--python-exit-code", "1", "--python", str(ENGINE),
           "--", "--project", str(p), "--mode", mode, "--preset", preset, *extra]
    # macOS idle sleep froze a frame for 15 minutes mid-render (pmset log, 2026-10-26);
    # caffeinate -i keeps the Mac awake only while this Blender process runs.
    if sys.platform == "darwin" and shutil.which("caffeinate"):
        cmd = ["caffeinate", "-i", *cmd]
    return cmd


def suffix(preset):
    """Output name suffix: preview keeps the v0.1 names, other presets get their own."""
    return "" if preset == "preview" else f"_{preset}"


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


DOWNSTREAM_OF_NARRATION = ("timing lock is stale", "project duration differs from timing.json")


def do_validate(p, final=False, before_narrate=False):
    """`before_narrate`: ignore errors that `narrate` + `schedule` themselves resolve (stale timing lock)."""
    errors, warnings = validate_project(p, final)
    if before_narrate:
        errors = [e for e in errors if not e.startswith(DOWNSTREAM_OF_NARRATION)]
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
    folder = "stills" if preset == "preview" else f"stills_{preset}"
    outputs = [p / "output" / folder / f"{s['id']}.png" for s in story.get("key_stills", [])]
    if preset == "preview":
        outputs.append(p / "output" / f"{slug_name(p)}_still.png")
    missing = [str(o) for o in outputs if not o.is_file() or o.stat().st_size == 0]
    if missing:
        raise SystemExit("Render returned success but stills are missing/empty: " + ", ".join(missing))
    for o in outputs:
        print("SUCCESS:", o)


# ---------------------------------------------------------------- shots
def render_shot(p, shot, preset, force=False):
    """Render one shot unless its visual inputs are unchanged (tools/render_cache.py categories)."""
    from tools import render_cache
    sid = shot["id"]
    seq = p / "renders" / preset / sid
    manifest_path = seq / "render_manifest.json"
    parts = render_cache.components(p, shot, preset)
    expected = expected_frames(p, shot)
    frames = sorted(seq.glob("frame_*.png"))
    manifest = read_json(manifest_path) if manifest_path.is_file() else None
    reasons = render_cache.stale_reasons(manifest, parts, render_cache.engine_file_hashes())
    if not force and not reasons and len(frames) == expected:
        print(f"CACHED: {sid} ({expected} frames, visual inputs unchanged)")
        return "cached"
    print(f"RENDER: {sid} ({'forced' if force else '; '.join(reasons) or f'{len(frames)}/{expected} frames on disk'})")
    for frame in frames:  # stale frames of this shot only, inside the project
        frame.unlink()
    run_logged(blender_command(p, "animation", preset, "--shot", sid), p / "qa" / f"render_{sid}_{preset}.log")
    frames = sorted(seq.glob("frame_*.png"))
    if len(frames) != expected:
        raise SystemExit(f"{sid}: expected {expected} frames, found {len(frames)}. See logs.")
    manifest_path.write_text(json.dumps({"shot": sid, "key_version": render_cache.KEY_VERSION,
                                         "cache_key": render_cache.cache_key(parts), "components": parts,
                                         "engine_files": render_cache.engine_file_hashes(), "frames": expected,
                                         "rendered_utc": datetime.now(timezone.utc).isoformat()}, indent=2))
    print(f"SUCCESS: {sid} {len(frames)} PNG frames")
    return "rendered"


def do_cache_report(p, preset):
    from tools import render_cache
    rows = render_cache.report(p, preset, shots(p))
    for r in rows:
        print(f"{r['status']:>7}  {r['shot']}  {'; '.join(r['reasons'])}")
    out = p / "qa" / f"cache_report_{preset}.json"
    out.write_text(json.dumps({"preset": preset, "key_version": render_cache.KEY_VERSION, "shots": rows}, indent=2))
    print(f"=> {out}")


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
    target = p / "output" / f"shots{suffix(preset)}" / f"{shot['id']}.mp4"
    target.parent.mkdir(parents=True, exist_ok=True)
    run_logged([ff, "-y", "-framerate", str(project["fps"]), "-start_number", "1", "-i", str(seq / "frame_%04d.png"),
                "-c:v", settings["output_codec"], "-crf", str(settings["output_crf"]), "-pix_fmt", "yuv420p",
                "-movflags", "+faststart", str(target)], p / "qa" / f"ffmpeg_{shot['id']}{suffix(preset)}.log")
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
    target = p / "output" / f"{slug_name(p)}_preview{suffix(preset)}.mp4"
    cmd += ["-filter_complex", f"{chain}concat=n={len(all_shots)}:v=1:a=0[v]", "-map", "[v]",
            "-c:v", settings["output_codec"], "-crf", str(settings["output_crf"]), "-pix_fmt", "yuv420p",
            "-movflags", "+faststart", str(target)]
    run_logged(cmd, p / "qa" / f"ffmpeg_encode{suffix(preset)}.log")
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


def boundary_ssim(p, preset):
    """SSIM between the last frame of each shot and the first frame of the next one.

    Shots are cut together; unless a shot declares "cut_from_previous": "hard", the cut
    must be invisible (same camera and state), so SSIM must stay >= CUT_SSIM_MIN."""
    results = []
    all_shots = shots(p)
    for prev, nxt in zip(all_shots, all_shots[1:]):
        a = p / "renders" / preset / prev["id"] / f"frame_{expected_frames(p, prev):04d}.png"
        b = p / "renders" / preset / nxt["id"] / "frame_0001.png"
        out = subprocess.run([ffmpeg_bin(), "-v", "info", "-i", str(a), "-i", str(b), "-lavfi", "ssim", "-f", "null", "-"],
                             text=True, capture_output=True)
        value = float(out.stderr.split("All:")[1].split()[0])
        mode = nxt.get("cut_from_previous", "match")
        results.append({"cut": f"{prev['id']}->{nxt['id']}", "mode": mode, "ssim": round(value, 5),
                        "ok": mode == "hard" or value >= CUT_SSIM_MIN})
    return results


CUT_SSIM_MIN = 0.98


def qa_sheets(p, preset):
    """Contact sheet of the full preview + 0/25/50/75/100% strips for every animated shot."""
    ff = ffmpeg_bin()
    project = read_json(p / "project.json")
    sheets = []
    full = p / "output" / f"{slug_name(p)}_preview{suffix(preset)}.mp4"
    every = project["fps"]
    tiles = max(1, round(project["duration_seconds"]))
    cols = 5
    rows = (tiles + cols - 1) // cols
    contact = p / "qa" / f"contact_sheet_preview{suffix(preset)}.png"
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
        target = p / "qa" / f"progress_{shot['id']}{suffix(preset)}.png"
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
    report["cuts"] = boundary_ssim(p, preset)
    problems += [f"cut {c['cut']}: SSIM {c['ssim']} < {CUT_SSIM_MIN} (visible jump)" for c in report["cuts"] if not c["ok"]]
    report["problems"] = problems
    report["sheets"] = [str(s.relative_to(p)) for s in qa_sheets(p, preset)]
    target = p / "qa" / f"preview_media_report{suffix(preset)}.json"
    target.write_text(json.dumps(report, indent=2))
    for name, info in report["files"].items():
        print(f"  {name}: {info['codec']} {info['width']}x{info['height']} {info['fps']} fps, "
              f"{info['frames']} frames, {info['duration']:.3f}s, black segments {info['black_segments']}")
    for cut in report["cuts"]:
        print(f"  cut {cut['cut']} ({cut['mode']}): SSIM {cut['ssim']}")
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


STILLS_ONLY_PRESETS = ("production_test",)


def do_preview(p, preset, force=False):
    if preset in STILLS_ONLY_PRESETS:
        raise SystemExit(f"--preset {preset} renders selected stills only (`still`), never a full sequence")
    do_validate(p, final=(preset == "final"))
    for shot in shots(p):
        render_shot(p, shot, preset, force)
    if ffmpeg_bin():
        do_encode(p, preset)
    else:
        print("Frames created; FFmpeg absent, so MP4 not encoded.")


def do_shot(p, shot_id, preset, force=False):
    if preset in STILLS_ONLY_PRESETS:
        raise SystemExit(f"--preset {preset} renders selected stills only (`still`), never a full sequence")
    do_validate(p, final=(preset == "final"))
    match = [s for s in shots(p) if s["id"] == shot_id]
    if not match:
        raise SystemExit(f"Unknown shot {shot_id}; shots: {', '.join(s['id'] for s in shots(p))}")
    render_shot(p, match[0], preset, force)
    if ffmpeg_bin():
        target = encode_shot(p, match[0], preset)
        print("SUCCESS:", target)


MANIFEST = ROOT / "PACKAGE_MANIFEST.sha256"


def manifest_files():
    """Version-controlled files (git ls-files), excluding the manifest itself."""
    if shutil.which("git") and (ROOT / ".git").exists():
        out = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT, capture_output=True, check=True).stdout
        names = [n for n in out.decode().split("\0") if n]
    else:  # packaged copy without git: every file outside generated folders
        skip = ("/renders/", "/output/", "/scenes/", "/qa/", "__pycache__", "/.git/")
        names = [str(f.relative_to(ROOT)) for f in ROOT.rglob("*")
                 if f.is_file() and not any(s in f"/{f.relative_to(ROOT)}" for s in skip)]
    return sorted(n for n in names if n != MANIFEST.name and (ROOT / n).is_file())


def do_manifest(check=False):
    rows = [(hashlib.sha256((ROOT / n).read_bytes()).hexdigest(), n) for n in manifest_files()]
    if check:
        recorded = {}
        for line in MANIFEST.read_text(encoding="utf-8").splitlines():
            if line and not line.startswith("#"):
                digest, name = line.split("  ", 1)
                recorded[name] = digest
        current = {n: d for d, n in rows}
        changed = sorted(n for n in current if n in recorded and recorded[n] != current[n])
        added = sorted(set(current) - set(recorded))
        removed = sorted(set(recorded) - set(current))
        for label, names in (("CHANGED", changed), ("NEW", added), ("MISSING", removed)):
            for n in names:
                print(f"{label}: {n}")
        if changed or added or removed:
            raise SystemExit(f"Manifest out of date ({len(changed)} changed, {len(added)} new, {len(removed)} missing)")
        print(f"PASS: manifest matches {len(rows)} files")
        return
    version = "unversioned"
    for line in (ROOT / "CHANGELOG.md").read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            version = line[3:].split(" —")[0].strip()
            break
    lines = [f"# Package manifest — Architecture Story Studio {version}",
             "## Files (sha256, relative path) — regenerate: python3 tools/cli.py manifest"]
    lines += [f"{d}  {n}" for d, n in rows]
    MANIFEST.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"SUCCESS: {MANIFEST.name} lists {len(rows)} files ({version})")


def do_check_blender(p, preset):
    do_validate(p)
    report = p / "qa" / "blender_checks.json"
    cmd = blender_command(p, "check", preset, "--report", str(report))
    logfile = p / "qa" / "blender_checks.log"
    if report.is_file():  # never summarise a previous run's report after a failed run
        report.unlink()
    try:
        run_logged(cmd, logfile)
    finally:
        if not report.is_file():
            print("Blender QA: NO REPORT (the Blender run failed before writing one)", file=sys.stderr)
        else:
            data = read_json(report)
            for r in data["results"]:
                if r["status"] != "PASS":
                    print(f"FAIL {r['shot']} {r['check']}: {r['detail']}")
            s = data["summary"]
            print(f"Blender QA: {s['passed']}/{s['total']} passed => {report}")


# ---------------------------------------------------------------- M3 narration pipeline
def do_tts_check(p):
    from integrations.tts import omnivoice as ov
    from pipeline import narration as nar
    client = ov.OmniVoiceClient()
    try:
        health = client.health()
    except ov.OmniVoiceError as e:
        raise SystemExit(f"OmniVoice: {e}")
    print(json.dumps(health, indent=2))
    print("Voice-design options:", json.dumps(client.voice_options()))
    narration = nar.load(p)
    if narration:
        spec = nar.voice_spec(narration, p)
        problems = client.validate_voice(spec) if spec.mode == "design" or Path(spec.reference_audio).is_file() else \
            ["reference clip not generated yet (run `narrate`)"]
        print(f"Narrator {narration['voice']['id']} ({spec.mode}): {'OK' if not problems else problems}")
        print(f"Voice licence status: {narration['voice']['license']['status']}")


def do_narrate(p, regenerate=False, purpose="internal_preview"):
    do_validate(p, before_narrate=True)
    from integrations.tts import providers
    from pipeline import narration as nar
    try:
        data = nar.generate(p, regenerate=regenerate, purpose=purpose)
    except providers.RightsError as e:
        raise SystemExit(f"REFUSED: {e}")
    total = sum(b["duration"] for b in data["beats"].values())
    print(f"SUCCESS: {len(data['beats'])} beats, {total:.2f}s of measured speech -> {p / 'audio'} "
          f"[{data['rights']['provider']}: {data['rights']['rights_class']}]")


def do_asr_check(p):
    from pipeline import asr_check
    failures = asr_check.check_project(p)
    if failures:
        raise SystemExit("ASR check failed: " + "; ".join(failures))
    print("ASR check: PASS (every sentence recognised as English, WER <= "
          f"{asr_check.MAX_WER})")


# ---------------------------------------------------------------- M4 architecture assets
ASSET_ROOT = ROOT / "asset_library" / "architecture"
CATALOG_DIR = ROOT / "asset_library" / "catalog"


def asset_specs(only=None):
    paths = sorted(ASSET_ROOT.rglob("*.json"))
    paths = [f for f in paths if "previews" not in f.parts]
    if only:
        target = (ROOT / only).resolve() if not Path(only).is_absolute() else Path(only)
        paths = [f for f in paths if f.resolve() == target]
        if not paths:
            raise SystemExit(f"no architecture asset spec at {only}")
    return paths


def offline_asset_checks(path):
    """G4-A (specification) + offline G4-B (planned geometry) for one asset spec."""
    from engine.arch import assets, checks
    data, _ = assets.load(path)
    errors = assets.validate(data, where=str(path.relative_to(ROOT)))
    if errors:
        return data, [("specification_valid", False, "; ".join(errors))]
    comps = assets.plan(data)
    params, _ = assets.resolve_params(data["family"], data["variant"], data["parameters"])
    results = [("specification_valid", True, f"{data['family']}/{data['variant']}, accuracy {data['accuracy']}")]
    return data, results + checks.check_asset(data, comps, params)


def do_asset_check(only=None):
    report, failed = {}, 0
    for path in asset_specs(only):
        data, results = offline_asset_checks(path)
        rel = str(path.relative_to(ROOT))
        report[rel] = [{"check": c, "status": "PASS" if ok else "FAIL", "detail": d} for c, ok, d in results]
        bad = [c for c, ok, _ in results if not ok]
        failed += len(bad)
        print(f"{'PASS' if not bad else 'FAIL'}  {rel}: {len(results) - len(bad)}/{len(results)}"
              + (f" (failed: {', '.join(bad)})" if bad else ""))
    CATALOG_DIR.mkdir(parents=True, exist_ok=True)
    (CATALOG_DIR / "offline_checks.json").write_text(json.dumps(report, indent=2) + "\n")
    if failed:
        raise SystemExit(f"{failed} offline asset check(s) failed")


def do_asset_render(only, preset):
    """Blender: multi-view previews + BVH QA + build-twice check per asset; measured peak memory."""
    import re
    from engine.arch import assets
    b = blender_bin()
    if not b:
        raise SystemExit("Blender not found")
    failures = []
    for path in asset_specs(only):
        data, _ = assets.load(path)
        if data["family"] == "site":
            continue
        out = path.parent / "previews" / data["asset_id"]
        report = CATALOG_DIR / "qa" / f"{data['asset_id']}_{preset}.json"
        log = CATALOG_DIR / "qa" / f"{data['asset_id']}_{preset}.log"
        # 1920x1080 is for selected stills only: the two presentation views
        views = "three_quarter,exploded" if preset == "production_test" else "three_quarter,elevation,top,exploded"
        cmd = ["/usr/bin/time", "-l", b, "--background", "--factory-startup", "--python-exit-code", "1",
               "--python", str(ENGINE), "--", "--mode", "asset", "--asset", str(path.relative_to(ROOT)),
               "--preset", preset, "--output", str(out / preset), "--report", str(report), "--views", views]
        if sys.platform == "darwin" and shutil.which("caffeinate"):
            cmd = ["caffeinate", "-i", *cmd]
        t0 = datetime.now(timezone.utc)
        try:
            run_logged(cmd, log)
        except SystemExit:
            failures.append(data["asset_id"])
        if not report.is_file():
            failures.append(f"{data['asset_id']} (no report)")
            continue
        rep = read_json(report)
        text = log.read_text(errors="replace")
        rss = re.search(r"(\d+)\s+maximum resident set size", text)
        foot = re.search(r"(\d+)\s+peak memory footprint", text)
        rep["process"] = {"wall_seconds": round((datetime.now(timezone.utc) - t0).total_seconds(), 1),
                          "peak_rss_mb": round(int(rss.group(1)) / 2 ** 20, 1) if rss else None,
                          "peak_memory_footprint_mb": round(int(foot.group(1)) / 2 ** 20, 1) if foot else None,
                          "measured_with": "/usr/bin/time -l on the whole Blender process (macOS)"}
        if shutil.which("ffmpeg"):   # small JPEG copies are tracked in git; PNGs stay local
            bg = read_json(ROOT / "config/visual_style.json")["palette"]["ground"].lstrip("#")
            for png in sorted((out / preset).glob("*.png")):
                w, h = (int(v) for v in subprocess.run(
                    [ffprobe_bin(), "-v", "error", "-show_entries", "stream=width,height", "-of", "csv=p=0", str(png)],
                    capture_output=True, text=True, check=True).stdout.strip().split(","))
                # transparent pixels (elevation sky) land on the ground colour
                subprocess.run([ffmpeg_bin(), "-v", "error", "-y", "-f", "lavfi", "-i", f"color=c=0x{bg}:s={w}x{h}",
                                "-i", str(png), "-filter_complex", "[0][1]overlay=format=auto", "-frames:v", "1",
                                "-q:v", "3", str(png.with_suffix(".jpg"))], check=True)
        report.write_text(json.dumps(rep, indent=2) + "\n")
        bad = [r["check"] for r in rep["results"] if r["status"] != "PASS"]
        print(f"{'PASS' if not bad else 'FAIL'}  {data['asset_id']} [{preset}]: "
              f"{len(rep['results']) - len(bad)}/{len(rep['results'])} Blender checks; "
              f"{rep['stats']['objects']} objects, {rep['stats']['mesh_datablocks']} meshes; "
              f"peak {rep['process']['peak_rss_mb']} MB; views -> {out / preset}")
    if failures:
        raise SystemExit("asset render/QA failed: " + ", ".join(failures))


def do_asset_catalog():
    """asset_library/catalog/catalog.json (+ .md): metadata, provenance, previews, validation."""
    import hashlib
    from engine.arch import GENERATOR_VERSION, assets
    lib = ROOT / "asset_library/materials/stylized_materials.json"
    entries = []
    for path in asset_specs():
        data, results = offline_asset_checks(path)
        rel = str(path.relative_to(ROOT))
        meta = assets.describe(data)
        previews = {}
        for preset in ("review", "production_test", "preview"):
            folder = path.parent / "previews" / data["asset_id"] / preset
            jpgs = sorted(folder.glob("*.jpg"))
            if jpgs:
                previews[preset] = [str(j.relative_to(ROOT)) for j in jpgs]
        blender = {}
        for preset in ("review", "production_test", "preview"):
            q = CATALOG_DIR / "qa" / f"{data['asset_id']}_{preset}.json"
            if q.is_file():
                rq = read_json(q)
                blender[preset] = {"checks": {r["check"]: r["status"] for r in rq["results"]},
                                   "signature": rq["signature"], "stats": rq["stats"], "process": rq.get("process"),
                                   "views": {k: {"render_seconds": v["render_seconds"]} for k, v in rq.get("views", {}).items()}}
        entries.append({
            "asset_id": data["asset_id"], "title": data.get("title"), "family": data["family"], "variant": data["variant"],
            "generator": {"name": f"{data['family']}.{data['variant']}", "version": GENERATOR_VERSION,
                          "module": "engine/arch/families/" + ("bridge.py" if data["family"] == "bridge" else "site.py")},
            "source_config": {"path": rel, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()},
            "units": data["units"], "accuracy": data["accuracy"], "provenance": data.get("provenance", {}),
            "geometry": {k: meta[k] for k in ("components", "unique_meshes", "by_type", "verts", "faces", "bbox", "dimensions_m")},
            "resolved_parameters": meta["resolved_parameters"],
            "materials": {"keys": meta["materials"], "library": str(lib.relative_to(ROOT)),
                          "library_sha256": hashlib.sha256(lib.read_bytes()).hexdigest(), "external_textures": []},
            "animation_support": data["animation_support"],
            "previews": previews,
            "validation": {"offline": {c: ("PASS" if ok else "FAIL") for c, ok, _ in results}, "blender": blender},
        })
    CATALOG_DIR.mkdir(parents=True, exist_ok=True)
    catalog = {"schema": "asset_catalog/1", "generated_utc": datetime.now(timezone.utc).isoformat(),
               "generator_version": GENERATOR_VERSION, "assets": entries}
    (CATALOG_DIR / "catalog.json").write_text(json.dumps(catalog, indent=2, ensure_ascii=False) + "\n")
    rows = ["# Architecture asset catalog", "",
            "Generated by `python3 tools/cli.py asset-catalog`. Every asset is **ILLUSTRATIVE** unless stated otherwise.", "",
            "| Asset | Family / variant | Components (unique meshes) | Size L×W×H m | Accuracy | Offline QA | Blender QA (review) | Preview |",
            "|---|---|---|---|---|---|---|---|"]
    for e in entries:
        off = e["validation"]["offline"]
        bl = e["validation"]["blender"].get("review", {}).get("checks", {})
        prev = next((j for j in e["previews"].get("review", []) if j.endswith("three_quarter.jpg")), "")
        dims = "×".join(f"{d:.1f}" for d in e["geometry"]["dimensions_m"])
        rows.append(f"| `{e['asset_id']}` | {e['family']}/{e['variant']} | {e['geometry']['components']} "
                    f"({e['geometry']['unique_meshes']}) | {dims} | {e['accuracy']} | "
                    f"{sum(v == 'PASS' for v in off.values())}/{len(off)} | "
                    f"{(str(sum(v == 'PASS' for v in bl.values())) + '/' + str(len(bl))) if bl else 'n/a'} | "
                    f"{('[3/4](../' + prev.split('asset_library/', 1)[1] + ')') if prev else '—'} |")
    (CATALOG_DIR / "CATALOG.md").write_text("\n".join(rows) + "\n")
    print(f"Catalog: {len(entries)} assets => {CATALOG_DIR / 'catalog.json'}")


# ---------------------------------------------------------------- M5 visual planning
def do_plan_visuals(p):
    """Narrative beats -> storyboard/visual_plan.json + qa/VISUAL_COVERAGE.md (no Blender)."""
    from planner import coverage, planner as pl
    try:
        plan = pl.plan_project(p)
    except pl.PlanningError as e:
        for err in e.errors:
            print("ERROR:", err)
        raise SystemExit(2)
    (p / "storyboard").mkdir(parents=True, exist_ok=True)
    (p / "storyboard" / "visual_plan.json").write_text(json.dumps(plan, indent=2, ensure_ascii=False) + "\n")
    report = coverage.write(plan, p)
    for c in plan["coverage"]:
        print(f"{c['status']:>17}  {c['beat_id']} {c['visual_intent']:<22} {c['strategy'] or '-':<28} "
              f"{', '.join(c['shot_ids']) or '-'}")
    for w in plan["warnings"]:
        print("WARNING:", w)
    print(f"{len(plan['shots'])} shots, {plan['duration_seconds']:.2f} s ({plan['timing_mode']}); "
          f"executable={plan['executable']} => {p / 'storyboard/visual_plan.json'}, {report}")
    if not plan["executable"]:
        raise SystemExit(4)


def do_validate_plan(p):
    from planner import validate
    path = p / "storyboard" / "visual_plan.json"
    if not path.is_file():
        raise SystemExit(f"{path} missing; run plan-visuals first")
    errors = validate.validate_plan(read_json(path), p)
    for e in errors:
        print("ERROR:", e)
    if errors:
        raise SystemExit(2)
    print("PASS: visual plan (references, timing, templates, targets, camera, evidence) + engine validation")


def do_build_shots(p):
    """Validated plan -> storyboard/states.json + storyboard.json + project.json (engine contract)."""
    from planner import compiler
    do_validate_plan(p)
    for path in compiler.compile_plan(read_json(p / "storyboard" / "visual_plan.json"), p):
        print("WROTE:", path)
    do_validate(p)


def do_align(p):
    """Whisper word timestamps for every current narration sentence (subtitle phrase breaks)."""
    from pipeline import subtitles
    n = subtitles.align_project(p)
    print(f"Alignment: {n} sentence(s) aligned ({'others cached' if n else 'all cached'})")


def do_schedule(p):
    from pipeline import beat_scheduler
    timing = beat_scheduler.run(p)
    for s in timing["shots"]:
        flag = " (extended for animation)" if s["extended_by_animation"] else ""
        print(f"  {s['id']}: frames {s['start_frame']}-{s['start_frame'] + s['frames'] - 1} "
              f"({s['duration_seconds']:.3f}s) beats {', '.join(s['beat_ids'])}{flag}")
    print(f"Total {timing['total_frames']} frames = {timing['total_seconds']:.3f}s; "
          f"timing {'LOCKED' if timing['locked'] else 'NOT locked (ASR check missing or failing)'}")
    from pipeline import storyboard_report
    print("Script & storyboard:", storyboard_report.write(p))
    do_validate(p)


def do_smoke(p, shot_id, preset):
    """One shot end to end: its narration beats -> Blender render -> MP4 with narration."""
    from pipeline import assemble
    do_validate(p)
    match = [s for s in shots(p) if s["id"] == shot_id]
    if not match:
        raise SystemExit(f"Unknown shot {shot_id}")
    render_shot(p, match[0], preset)
    video = encode_shot(p, match[0], preset)
    out = p / "qa" / "smoke" / f"{shot_id}_smoke{suffix(preset)}.mp4"
    report = assemble.assemble(p, video, out, shot_ids=[shot_id])
    (p / "qa" / "smoke" / f"{shot_id}_smoke_report.json").write_text(json.dumps(report, indent=2))
    if report["problems"]:
        raise SystemExit("Smoke test FAILED: " + "; ".join(report["problems"]))
    print(f"SMOKE PASS: {out}")


def do_assemble(p, preset):
    from pipeline import assemble
    video = p / "output" / f"{slug_name(p)}_preview{suffix(preset)}.mp4"
    if not video.is_file():
        raise SystemExit(f"Missing {video}; run `preview --project {p.name}` first")
    cleared, classes = assemble.narration_rights(p)
    # Never give restricted narration a publishable-looking name.
    out = p / "output" / f"{slug_name(p)}_pilot{'' if cleared else '_INTERNAL'}{suffix(preset)}.mp4"
    report = assemble.assemble(p, video, out)
    (p / "qa" / f"assembly_report{suffix(preset)}.json").write_text(json.dumps(report, indent=2))
    if report["problems"]:
        raise SystemExit("Assembly QA FAILED: " + "; ".join(report["problems"]))
    write_subtitle_qa(p, report)
    print(f"SUCCESS: {out} (+ {Path(report['subtitles']).name}); narration rights: {', '.join(classes)}")


def write_subtitle_qa(p, report):
    """qa/SUBTITLE_QA.md: every cue with timing source, reading speed and line lengths."""
    st = report["subtitle_stats"]
    rows = ["# Subtitle QA", "",
            f"- File: `{Path(report['subtitles']).relative_to(p)}` — {st['cues']} cues for {st['sentences']} sentences; "
            f"{st['two_line_cues']} two-line cues; longest line {st['max_line']} chars (limit 42); "
            f"max reading speed {st['max_cps']} chars/s.",
            f"- Phrase breaks from Whisper word alignment, placed at the quietest 10 ms frame of the real audio: "
            f"{st['aligned_boundaries']}; sentence-span fallbacks: {st['sentence_fallbacks']}.",
            "- Text comes from the script (official spellings kept); ASR text is never used as subtitle text.",
            f"- Problems: {'; '.join(p_ for p_ in report['problems'] if 'cue' in p_ or 'subtitle' in p_ or 'SRT' in p_) or 'none'}",
            f"- Warnings: {len(report['subtitle_warnings'])}" + "".join(f"\n  - {w}" for w in report["subtitle_warnings"]),
            "", "| # | Start | End | Dur | cps | Lines (chars) | Timing source | Break (audio level) |",
            "|---|---|---|---|---|---|---|---|"]
    for i, c in enumerate(report["subtitle_cues"], 1):
        d = c["end"] - c["start"]
        lines = " / ".join(f"{l} ({len(l)})" for l in c["lines"])
        b = c.get("boundary")
        brk = f"after “{b['after_word']}” at {b['placed_at']:.2f}s ({b['rms_db_at_boundary']} dBFS)" if b else "sentence end"
        rows.append(f"| {i} | {c['start']:.3f} | {c['end']:.3f} | {d:.2f} | {len(c['text']) / d:.1f} | {lines} | "
                    f"{c['source']} | {brk} |")
    (p / "qa" / "SUBTITLE_QA.md").write_text("\n".join(rows) + "\n", encoding="utf-8")


def do_gates(p, preset):
    """G0-G6 + status flags for a narrated project (pipeline/gates.py); writes qa/gates.json."""
    from pipeline import gates
    result = gates.evaluate(p, suffix(preset))
    for name, g in result["gates"].items():
        print(f"{g['status']:>18}  {name}: {'; '.join(g['notes'])}")
    print("Statuses:", ", ".join(result["statuses"]))
    print(f"Verdict: {result['verdict']}")
    (p / "qa" / "gates.json").write_text(json.dumps(result, indent=2, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description="Architecture Story Studio — Mac M4 pilot CLI")
    parser.add_argument("command", choices=["doctor", "validate", "still", "preview", "shot", "encode",
                                            "check-blender", "final-gate", "manifest", "tts-check", "narrate",
                                            "asr-check", "schedule", "smoke", "assemble", "gates", "cache-report", "align",
                                            "asset-check", "asset-render", "asset-catalog",
                                            "plan-visuals", "validate-plan", "build-shots"])
    parser.add_argument("--project", default="roof-evolution", help="Project slug in projects/")
    parser.add_argument("--preset", default="preview", choices=["preview", "review", "production_test", "final"])
    parser.add_argument("--shot", help="Shot id for the `shot` command, e.g. SC_002")
    parser.add_argument("--asset", help="asset-*: one asset spec path (default: every spec in asset_library/architecture)")
    parser.add_argument("--force", action="store_true", help="Re-render shots even if cached")
    parser.add_argument("--check", action="store_true", help="manifest: verify instead of rewriting")
    parser.add_argument("--regenerate", action="store_true", help="narrate: ignore the audio cache")
    parser.add_argument("--purpose", default="internal_preview", choices=["internal_preview", "publication"],
                        help="narrate: publication refuses providers that are not PUBLICATION_CLEARED")
    args = parser.parse_args()
    if args.command == "doctor":
        do_doctor()
        return
    if args.command == "manifest":
        do_manifest(args.check)
        return
    if args.command == "asset-check":
        do_asset_check(args.asset)
        return
    if args.command == "asset-render":
        do_asset_render(args.asset, args.preset)
        return
    if args.command == "asset-catalog":
        do_asset_catalog()
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
    elif args.command == "tts-check":
        do_tts_check(p)
    elif args.command == "narrate":
        do_narrate(p, args.regenerate, args.purpose)
    elif args.command == "asr-check":
        do_asr_check(p)
    elif args.command == "schedule":
        do_schedule(p)
    elif args.command == "smoke":
        if not args.shot:
            raise SystemExit("--shot is required, e.g. --shot SC_003")
        do_smoke(p, args.shot, args.preset)
    elif args.command == "assemble":
        do_assemble(p, args.preset)
    elif args.command == "gates":
        do_gates(p, args.preset)
    elif args.command == "align":
        do_align(p)
    elif args.command == "plan-visuals":
        do_plan_visuals(p)
    elif args.command == "validate-plan":
        do_validate_plan(p)
    elif args.command == "build-shots":
        do_build_shots(p)
    elif args.command == "cache-report":
        do_cache_report(p, args.preset)


if __name__ == "__main__":
    main()
