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


def do_narrate(p, regenerate=False):
    do_validate(p)
    from pipeline import narration as nar
    data = nar.generate(p, regenerate=regenerate)
    total = sum(b["duration"] for b in data["beats"].values())
    print(f"SUCCESS: {len(data['beats'])} beats, {total:.2f}s of measured speech -> {p / 'audio'}")


def do_asr_check(p):
    from pipeline import asr_check
    failures = asr_check.check_project(p)
    if failures:
        raise SystemExit("ASR check failed: " + "; ".join(failures))
    print("ASR check: PASS (every sentence recognised as English, WER <= "
          f"{asr_check.MAX_WER})")


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
    out = p / "output" / f"{slug_name(p)}_pilot{suffix(preset)}.mp4"
    report = assemble.assemble(p, video, out)
    (p / "qa" / f"assembly_report{suffix(preset)}.json").write_text(json.dumps(report, indent=2))
    if report["problems"]:
        raise SystemExit("Assembly QA FAILED: " + "; ".join(report["problems"]))
    print(f"SUCCESS: {out} (+ {Path(report['subtitles']).name})")


def do_gates(p, preset):
    """G0-G6 status for a narrated project (M3 numbering); writes qa/gates.json."""
    from pipeline import narration as nar
    gates = {}
    errors, warnings = validate_project(p)
    gates["G0 project & schema validation"] = ("PASS" if not errors else "FAIL", errors[:5] or ["validate passes"])
    sources = read_json(p / "research/sources.json")
    narration = nar.load(p)
    claims = {c["id"]: c for c in sources.get("claims", [])}
    used = sorted({c for b in (narration or {}).get("beats", []) for c in b.get("claim_ids", [])})
    statuses = {c: claims.get(c, {}).get("review_status") for c in used}
    if any(s in (None, "REJECTED", "PROVISIONAL", "provisional") for s in statuses.values()):
        g1 = ("FAIL", [f"{c}: {s}" for c, s in statuses.items() if s not in ("SOURCE_VERIFIED", "EDITORIALLY_APPROVED")])
    elif all(s in ("EDITORIALLY_APPROVED", "verified") for s in statuses.values()):
        g1 = ("PASS", [f"{len(used)} claims editorially approved"])
    else:
        g1 = ("PENDING_EDITORIAL", [f"{len(used)} narrated claims SOURCE_VERIFIED; editorial approval pending"])
    gates["G1 evidence & script review"] = g1
    manifest_path = p / "audio/narration_manifest.json"
    manifest = read_json(manifest_path) if manifest_path.is_file() else {}
    current = {s["cache_key"] for b in manifest.get("beats", {}).values() for s in b["sentences"]}
    asr = [r.get("asr", {}).get("pass") for r in manifest.get("segments", {}).values() if r.get("cache_key") in current]
    licence = ((narration or {}).get("voice") or {}).get("license", {}).get("status")
    tech_ok = bool(asr) and all(asr)
    gates["G2 OmniVoice API & voice licensing"] = (
        "PASS" if tech_ok and licence == "APPROVED" else ("BLOCKED_LICENSE" if tech_ok else "FAIL"),
        [f"{len(asr)} sentences generated + ASR-verified" if tech_ok else "ASR check missing/failing",
         f"voice licence: {licence}"])
    timing_path = p / "script/timing.json"
    timing = read_json(timing_path) if timing_path.is_file() else {}
    timing_errors = [e for e in errors if "timing" in e]
    gates["G3 narration timing lock"] = ("PASS" if timing.get("locked") and not timing_errors else "FAIL",
                                         [f"{timing.get('total_frames')} frames, locked={timing.get('locked')}"] + timing_errors)
    bq = p / "qa" / "blender_checks.json"
    media = p / "qa" / f"preview_media_report{suffix(preset)}.json"
    b = read_json(bq)["summary"] if bq.is_file() else None
    m = read_json(media) if media.is_file() else None
    g4_ok = bool(b) and b["failed"] == 0 and bool(m) and not m.get("problems")
    gates["G4 Blender visual preview"] = ("PASS" if g4_ok else "FAIL",
                                          [f"Blender QA {b['passed']}/{b['total']}" if b else "no Blender QA report",
                                           "media QA PASS" if m and not m.get("problems") else "media QA missing/failing",
                                           "visual review of rendered frames: see qa/M3_QA_REPORT.md"])
    ar = p / "qa" / f"assembly_report{suffix(preset)}.json"
    a = read_json(ar) if ar.is_file() else None
    gates["G5 media assembly"] = ("PASS" if a and not a["problems"] else "FAIL",
                                  a["problems"] if a and a["problems"] else
                                  ([f"{a['frames']} frames, {a['loudness_after']['integrated_lufs']} LUFS"] if a else ["not assembled"]))
    final_errors, _ = validate_project(p, final=True)
    final_errors = [e for e in final_errors if e.startswith("FINAL gate")]
    gates["G6 final publication readiness"] = ("PASS" if not final_errors and all(v[0] == "PASS" for v in gates.values())
                                               else "BLOCKED", final_errors or ["all gates pass"])
    verdict = "PUBLICATION-READY" if gates["G6 final publication readiness"][0] == "PASS" else \
        "INTERNAL REVIEW PREVIEW — NOT PUBLICATION-READY"
    for name, (status, notes) in gates.items():
        print(f"{status:>18}  {name}: {'; '.join(notes)}")
    print(f"Verdict: {verdict}")
    (p / "qa" / "gates.json").write_text(json.dumps({"verdict": verdict, "gates": {k: {"status": v[0], "notes": v[1]}
                                                                                    for k, v in gates.items()}}, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Architecture Story Studio — Mac M4 pilot CLI")
    parser.add_argument("command", choices=["doctor", "validate", "still", "preview", "shot", "encode",
                                            "check-blender", "final-gate", "manifest", "tts-check", "narrate",
                                            "asr-check", "schedule", "smoke", "assemble", "gates"])
    parser.add_argument("--project", default="roof-evolution", help="Project slug in projects/")
    parser.add_argument("--preset", default="preview", choices=["preview", "review", "final"])
    parser.add_argument("--shot", help="Shot id for the `shot` command, e.g. SC_002")
    parser.add_argument("--force", action="store_true", help="Re-render shots even if cached")
    parser.add_argument("--check", action="store_true", help="manifest: verify instead of rewriting")
    parser.add_argument("--regenerate", action="store_true", help="narrate: ignore the audio cache")
    args = parser.parse_args()
    if args.command == "doctor":
        do_doctor()
        return
    if args.command == "manifest":
        do_manifest(args.check)
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
        do_narrate(p, args.regenerate)
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


if __name__ == "__main__":
    main()
