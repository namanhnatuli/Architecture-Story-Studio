#!/usr/bin/env python3
"""Mac-first stdlib CLI: validate, render shots headless with Blender, encode with FFmpeg."""
import argparse
import hashlib
import json
import math
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


def default_project():
    """--project may be omitted while projects/ holds exactly one project (the active film)."""
    slugs = sorted(d.name for d in (ROOT / "projects").iterdir() if (d / "project.json").is_file())
    if len(slugs) != 1:
        raise SystemExit("pass --project <slug>; projects/ holds: " + (", ".join(slugs) or "no project"))
    return slugs[0]


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
    # caffeinate keeps the Mac awake only while this Blender process runs (it cannot stop lid-close sleep).
    if sys.platform == "darwin" and shutil.which("caffeinate"):
        cmd = ["caffeinate", "-is", *cmd]   # -s: no system sleep on AC power, for this process only
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
# M7 audio-first: plan-visuals + build-shots rebuild the storyboard from the new narration beats
DOWNSTREAM_OF_AUDIO_FIRST_NARRATION = DOWNSTREAM_OF_NARRATION + ("shots must cover every narration beat",
                                                                 "Storyboard end", "timing manifest")


def do_validate(p, final=False, before_narrate=False):
    """`before_narrate`: ignore errors that `narrate` + `schedule` themselves resolve (stale timing lock);
    for an audio-first project also the storyboard's beat coverage, which plan-visuals rebuilds."""
    errors, warnings = validate_project(p, final)
    if before_narrate:
        downstream = DOWNSTREAM_OF_AUDIO_FIRST_NARRATION if (p / "script/visual_beats.json").is_file() \
            else DOWNSTREAM_OF_NARRATION
        errors = [e for e in errors if not e.startswith(downstream)]
    for msg in warnings:
        print("WARNING:", msg)
    for msg in errors:
        print("ERROR:", msg)
    if errors:
        raise SystemExit(2)
    print("PASS: structural validation" if not final else "PASS: final gate")


# ---------------------------------------------------------------- stills
def do_still(p, preset):
    do_validate(p, final=(preset in FINAL_PRESETS))
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
PNG_END = b"\x00\x00\x00\x00IEND\xaeB`\x82"


def complete_png(path):
    """A frame Blender finished writing: PNG signature and a final IEND chunk."""
    try:
        with open(path, "rb") as f:
            head = f.read(8)
            f.seek(-12, 2)
            return head == b"\x89PNG\r\n\x1a\n" and f.read(12) == PNG_END
    except OSError:
        return False


NO_REUSE = False   # M7: --no-reuse renders every frame (verification / fallback)


def render_shot(p, shot, preset, force=False):
    """Render one shot unless its visual inputs are unchanged (tools/render_cache.py categories).

    M7 recovery: render_progress.json records the cache key before Blender starts. If a render
    of the same key was interrupted (power, sleep, kill), the complete frames are kept and only
    the missing ones are rendered; a truncated last frame is deleted first."""
    from tools import render_cache
    sid = shot["id"]
    seq = p / "renders" / preset / sid
    manifest_path, progress_path = seq / "render_manifest.json", seq / "render_progress.json"
    parts = render_cache.components(p, shot, preset)
    key, engine_hashes = render_cache.cache_key(parts), render_cache.engine_file_hashes()
    expected = expected_frames(p, shot)
    frames = sorted(seq.glob("frame_*.png"))
    manifest = read_json(manifest_path) if manifest_path.is_file() else None
    reasons = render_cache.stale_reasons(manifest, parts, engine_hashes)
    if not force and not reasons and len(frames) == expected:
        print(f"CACHED: {sid} ({expected} frames, visual inputs unchanged)")
        return "cached"
    progress = read_json(progress_path) if progress_path.is_file() else None
    resume = (not force and progress is not None and progress.get("cache_key") == key
              and progress.get("frames") == expected)
    if resume:
        broken = [f for f in frames if not complete_png(f)]
        extra = [f for f in frames if not f.name[6:10].isdigit() or not 1 <= int(f.name[6:10]) <= expected]
        for frame in broken + extra:
            frame.unlink()
        kept = len(frames) - len(set(broken + extra))
        print(f"RESUME: {sid} (interrupted render of the same inputs: {kept}/{expected} frames kept, "
              f"{len(broken)} incomplete removed)")
    else:
        print(f"RENDER: {sid} ({'forced' if force else '; '.join(reasons) or f'{len(frames)}/{expected} frames on disk'})")
        for frame in frames:  # stale frames of this shot only, inside the project
            frame.unlink()
    if manifest_path.is_file():
        manifest_path.unlink()   # never leave a manifest that vouches for frames being replaced
    seq.mkdir(parents=True, exist_ok=True)
    progress_path.write_text(json.dumps({"shot": sid, "cache_key": key, "frames": expected,
                                         "started_utc": datetime.now(timezone.utc).isoformat()}, indent=2))
    run_logged(blender_command(p, "animation", preset, "--shot", sid, *(["--resume"] if resume else []),
                               *(["--no-reuse"] if NO_REUSE else [])),
               p / "qa" / f"render_{sid}_{preset}.log")
    frames = sorted(seq.glob("frame_*.png"))
    if len(frames) != expected or not all(complete_png(f) for f in frames):
        raise SystemExit(f"{sid}: expected {expected} complete frames, found {len(frames)}. See logs.")
    strategy_path = seq / "render_strategy.json"
    strategy = read_json(strategy_path) if strategy_path.is_file() else {"strategy": "FALLBACK_FULL_BLENDER"}
    manifest_path.write_text(json.dumps({"shot": sid, "key_version": render_cache.KEY_VERSION,
                                         "cache_key": key, "components": parts,
                                         "engine_files": engine_hashes, "frames": expected,
                                         "resumed": resume,
                                         "strategy": {k: strategy.get(k) for k in
                                                      ("strategy", "reason", "distinct_frames", "rendered",
                                                       "reused", "kept")},
                                         "rendered_utc": datetime.now(timezone.utc).isoformat()}, indent=2))
    progress_path.unlink()
    print(f"SUCCESS: {sid} {len(frames)} PNG frames{' (resumed)' if resume else ''}")
    return "resumed" if resume else "rendered"


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


def encode_sequence(p, preset, shot_list, target, log_name):
    """One H.264 file from the PNG frames of consecutive shots (M7): the frames are linked into one
    numbered sequence, so a 100-shot film is a single image input, not 100 parallel decoders."""
    ff = ffmpeg_bin()
    project = read_json(p / "project.json")
    settings = read_json(ROOT / "config/render_presets.json")
    link_dir = p / "renders" / preset / f"_sequence_{target.stem}"
    if link_dir.exists():
        shutil.rmtree(link_dir)
    link_dir.mkdir(parents=True)
    n = 0
    try:
        for shot in shot_list:
            seq = require_frames(p, shot, preset)
            for k in range(1, expected_frames(p, shot) + 1):
                n += 1
                (link_dir / f"f_{n:06d}.png").symlink_to((seq / f"frame_{k:04d}.png").resolve())
        target.parent.mkdir(parents=True, exist_ok=True)
        partial = target.with_name(target.stem + ".partial.mp4")   # atomic: the real name only for a complete file
        wm = watermark_spec(p, preset)
        run_logged([ff, "-y", "-framerate", str(project["fps"]), "-start_number", "1", "-i", str(link_dir / "f_%06d.png"),
                    *(["-i", str(ROOT / wm["image"])] if wm else []),
                    *encode_args(settings, preset, wm), "-movflags", "+faststart", str(partial)],
                   p / "qa" / f"{log_name}.log")
        if not partial.is_file() or partial.stat().st_size == 0:
            raise SystemExit(f"FFmpeg returned success but {partial.name} is missing/empty")
        os.replace(partial, target)
    finally:
        shutil.rmtree(link_dir, ignore_errors=True)
    return target


def encode_args(settings, preset, wm=None):
    """Video encoder arguments: global codec/CRF, per-preset overrides (M7 final_4k: CRF, x264 preset and an
    explicit BT.709 conversion + tags; earlier presets keep their original arguments). With `wm` (watermark_spec,
    the image as the second input) the watermark is laid over the frames in RGB before any colour conversion."""
    cfg = settings.get(preset, {})
    args = ["-c:v", settings["output_codec"], "-crf", str(cfg.get("crf", settings["output_crf"]))]
    if cfg.get("x264_preset"):
        args += ["-preset", cfg["x264_preset"]]
    # PNG frames carry sRGB transfer metadata that newer FFmpeg propagates; setparams pins BT.709 on the frames
    bt709 = "scale=out_color_matrix=bt709:out_range=tv,setparams=colorspace=bt709:color_primaries=bt709:color_trc=bt709:range=tv" \
        if cfg.get("color") == "bt709" else None
    if wm:
        args += ["-filter_complex", watermark_filter(wm) + (f",{bt709}" if bt709 else "") + "[v]", "-map", "[v]"]
    elif bt709:
        args += ["-vf", bt709]
    if bt709:
        args += ["-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv"]
    return args + ["-pix_fmt", "yuv420p"]


BRANDING = ROOT / "config" / "branding.json"


def png_size(path):
    with open(path, "rb") as f:
        head = f.read(24)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        raise SystemExit(f"{path} is not a PNG")
    return int.from_bytes(head[16:20], "big"), int.from_bytes(head[20:24], "big")


def watermark_spec(p, preset):
    """The channel watermark (config/branding.json) as pixel geometry for `preset`, or None when the project does not
    carry it (project.json "watermark": true). The image must be the recorded file (sha256). The box must lie in a
    bottom corner inside the subtitle zone of config/annotation_style.json, which annotations never enter, so the
    watermark cannot cover a label, a note or a card tag."""
    if not read_json(p / "project.json").get("watermark"):
        return None
    cfg = read_json(BRANDING)["watermark"]
    image = ROOT / cfg["image"]
    if not image.is_file() or sha256_of(image) != cfg["sha256"]:
        raise SystemExit(f"watermark {cfg['image']} is missing or not the recorded file (sha256 in config/branding.json)")
    want = read_json(ROOT / "config/render_presets.json")[preset]
    W, H = want["width"], want["height"]
    iw, ih = png_size(image)
    w = 2 * round(W * cfg["width_fraction"] / 2)
    h = 2 * round(w * ih / iw / 2)
    margin_x, margin_y = round(W * cfg["margin_x_fraction"]), round(H * cfg["margin_y_fraction"])
    corner = cfg["corner"]
    if corner not in ("BOTTOM_LEFT", "BOTTOM_RIGHT"):
        raise SystemExit(f"watermark corner {corner}: only the bottom corners lie in the annotation-free subtitle zone")
    zone = read_json(ROOT / "config/annotation_style.json")["subtitle_zone"]
    if (margin_y + h) / H > zone:
        raise SystemExit(f"watermark box reaches {(margin_y + h) / H:.3f} of the frame height, above the subtitle zone {zone}")
    x = margin_x if corner == "BOTTOM_LEFT" else W - margin_x - w
    return {"image": cfg["image"], "sha256": cfg["sha256"], "corner": corner, "x": x, "y": H - margin_y - h,
            "width": w, "height": h, "opacity": cfg["opacity"]}


def watermark_filter(wm):
    """filter_complex chain: input 1 (the watermark) scaled and faded, laid over input 0 in RGB (no output label)."""
    return (f"[1:v]scale={wm['width']}:{wm['height']}:flags=lanczos,format=rgba,colorchannelmixer=aa={wm['opacity']}[wm];"
            f"[0:v][wm]overlay={wm['x']}:{wm['y']}:format=rgb")


def watermark_check(p, preset, video, first_png, wm):
    """The watermark is in the encoded file, where it should be: in its box, the video's first frame is close to the
    shot's first PNG with the watermark laid over it, and far from the PNG without it (PSNR of the box, dB)."""
    work = p / "qa" / "_watermark_check"
    work.mkdir(exist_ok=True)
    try:
        frame, ref = work / "video.png", work / "reference.png"
        subprocess.run([ffmpeg_bin(), "-v", "error", "-y", "-i", str(video), "-frames:v", "1", str(frame)], check=True)
        subprocess.run([ffmpeg_bin(), "-v", "error", "-y", "-i", str(first_png), "-i", str(ROOT / wm["image"]),
                        "-filter_complex", watermark_filter(wm), "-frames:v", "1", str(ref)], check=True)

        def psnr(a, b):
            crop = f"crop={wm['width']}:{wm['height']}:{wm['x']}:{wm['y']}"
            r = subprocess.run([ffmpeg_bin(), "-v", "info", "-i", str(a), "-i", str(b), "-lavfi",
                                f"[0:v]{crop}[a];[1:v]{crop}[b];[a][b]psnr", "-f", "null", "-"], capture_output=True, text=True)
            value = r.stderr.split("average:")[1].split()[0]
            return 99.0 if value == "inf" else float(value)
        with_wm, without = psnr(frame, ref), psnr(frame, first_png)
    finally:
        shutil.rmtree(work, ignore_errors=True)
    return {"box": [wm["x"], wm["y"], wm["width"], wm["height"]], "psnr_to_watermarked_db": round(with_wm, 2),
            "psnr_to_plain_db": round(without, 2), "present": with_wm >= 30.0 and with_wm >= without + 6.0}


def watermark_backgrounds(p, preset, chapter_list, wm, busy=6.0):
    """What lies under the watermark box in the middle frame of each shot: mean edge strength (0-255) of the box in
    the render. Informative: over busy footage the watermark reads less, it never hides a text (subtitle zone)."""
    rows = []
    for s in chapter_list:
        png = p / "renders" / preset / s["id"] / f"frame_{max(1, expected_frames(p, s) // 2):04d}.png"
        r = subprocess.run([ffmpeg_bin(), "-v", "info", "-i", str(png), "-vf",
                            f"crop={wm['width']}:{wm['height']}:{wm['x']}:{wm['y']},edgedetect=low=0.08:high=0.2,"
                            "signalstats,metadata=print:key=lavfi.signalstats.YAVG", "-f", "null", "-"],
                           capture_output=True, text=True)
        edges = float(r.stderr.split("YAVG=")[1].split()[0]) if "YAVG=" in r.stderr else None
        rows.append({"shot": s["id"], "edges": None if edges is None else round(edges, 2),
                     "busy": edges is not None and edges > busy})
    return rows


def encode_full(p, preset):
    target = p / "output" / f"{slug_name(p)}_preview{suffix(preset)}.mp4"
    return encode_sequence(p, preset, shots(p), target, f"ffmpeg_encode{suffix(preset)}")


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


def stream_types(path):
    out = subprocess.run([ffprobe_bin(), "-v", "error", "-show_entries", "stream=codec_type", "-of", "json", str(path)],
                         text=True, capture_output=True, check=True)
    types = [st["codec_type"] for st in json.loads(out.stdout).get("streams", [])]
    return {"video": types.count("video"), "audio": types.count("audio")}


def decode_errors(path):
    """Container/bitstream integrity: errors reported while decoding every frame."""
    out = subprocess.run([ffmpeg_bin(), "-v", "error", "-i", str(path), "-f", "null", "-"], text=True, capture_output=True)
    return len([l for l in out.stderr.splitlines() if l.strip()])


def black_segments(path):
    out = subprocess.run([ffmpeg_bin(), "-v", "info", "-i", str(path), "-vf", "blackdetect=d=0.04:pix_th=0.10",
                          "-an", "-f", "null", "-"], text=True, capture_output=True)
    return out.stderr.count("black_start")


def boundary_ssim(p, preset, shot_list=None):
    """SSIM between the last frame of each shot and the first frame of the next one.

    Shots are cut together; unless a shot declares "cut_from_previous": "hard", the cut
    must be invisible (same camera and state), so SSIM must stay >= CUT_SSIM_MIN."""
    results = []
    all_shots = shot_list or shots(p)
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
MAX_SHEET_TILES = 150


def qa_sheets(p, preset):
    """Contact sheet of the full preview + 0/25/50/75/100% strips for every animated shot."""
    ff = ffmpeg_bin()
    project = read_json(p / "project.json")
    sheets = []
    full = p / "output" / f"{slug_name(p)}_preview{suffix(preset)}.mp4"
    step = max(1, math.ceil(project["duration_seconds"] / MAX_SHEET_TILES))   # M7: long films sample sparser
    every = project["fps"] * step
    tiles = max(1, math.ceil(project["duration_seconds"] / step))
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
    """Silent preview media QA (M5.5): per file frames, resolution, fps, codec, duration vs
    frames, no audio stream, decode errors, black segments; cut continuity; and what the
    media were rendered from (storyboard hash, per-shot render-cache keys) for staleness."""
    import hashlib
    from tools import render_cache
    settings = read_json(ROOT / "config/render_presets.json")
    want = settings[preset]
    fps = read_json(p / "project.json")["fps"]
    report = {"utc": datetime.now(timezone.utc).isoformat(), "preset": preset, "files": {},
              "expected": {"width": want["width"], "height": want["height"], "fps": f"{fps}/1", "codec": "h264",
                           "pix_fmt": "yuv420p", "audio_streams": 0}}
    problems = []
    expected_total, boundaries = 0, []
    for shot in shots(p):
        boundaries.append({"shot": shot["id"], "start_frame": expected_total + 1, "frames": expected_frames(p, shot)})
        expected_total += expected_frames(p, shot)
    for label, path, expected in outputs:
        info = probe(path)
        info["black_segments"] = black_segments(path)
        info["streams"] = stream_types(path)
        info["decode_errors"] = decode_errors(path)
        info["size_bytes"] = path.stat().st_size
        report["files"][str(path.relative_to(p))] = info
        if info["frames"] != expected:
            problems.append(f"{label}: {info['frames']} frames, expected {expected}")
        if (info["width"], info["height"]) != (want["width"], want["height"]):
            problems.append(f"{label}: {info['width']}x{info['height']}, expected {want['width']}x{want['height']}")
        if info["fps"] != f"{fps}/1" or info["codec"] != "h264" or info["pix_fmt"] != "yuv420p":
            problems.append(f"{label}: {info['codec']} {info['pix_fmt']} {info['fps']} fps, expected h264 yuv420p {fps}/1")
        if abs(info["duration"] - info["frames"] / fps) > 1.5 / fps:
            problems.append(f"{label}: duration {info['duration']:.3f}s does not match {info['frames']} frames")
        if info["streams"]["video"] != 1 or info["streams"]["audio"] != 0:
            problems.append(f"{label}: streams {info['streams']} (a preview is one silent video stream)")
        if info["decode_errors"]:
            problems.append(f"{label}: {info['decode_errors']} decode error(s) (damaged container or frames)")
        if info["black_segments"]:
            problems.append(f"{label}: {info['black_segments']} black segment(s)")
    report["expected_total_frames"] = expected_total
    report["shot_boundaries"] = boundaries
    story_path = p / "storyboard" / "storyboard.json"
    report["storyboard_sha256"] = hashlib.sha256(story_path.read_bytes()).hexdigest()
    report["plan_sha256"] = read_json(story_path).get("plan_sha256")
    report["render_keys"] = {s["id"]: render_cache.cache_key(render_cache.components(p, s, preset)) for s in shots(p)}
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
INTERNAL_PRESETS = ("internal_1080p", "internal_720p")
FINAL_PRESETS = ("final", "final_4k")   # these require the FINAL gate before anything is rendered
HEADROOM_GB = 8.0                        # never let a render run the volume below this


def do_preview(p, preset, force=False):
    if preset in STILLS_ONLY_PRESETS:
        raise SystemExit(f"--preset {preset} renders selected stills only (`still`), never a full sequence")
    do_validate(p, final=(preset in FINAL_PRESETS))
    for shot in shots(p):
        render_shot(p, shot, preset, force)
    if ffmpeg_bin():
        do_encode(p, preset)
    else:
        print("Frames created; FFmpeg absent, so MP4 not encoded.")


def do_shot(p, shot_id, preset, force=False):
    if preset in STILLS_ONLY_PRESETS:
        raise SystemExit(f"--preset {preset} renders selected stills only (`still`), never a full sequence")
    do_validate(p, final=(preset in FINAL_PRESETS))
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
    if (p / "script/visual_beats.json").is_file() and not (p / "storyboard/storyboard.json").is_file():
        # M6 audio-first: the storyboard is planned after the audio lock (narration is validated by `generate`)
        print("Audio-first project: narration -> lock-audio -> plan-visuals (no storyboard yet)")
    else:
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
                          "module": f"engine/arch/families/{data['family']}.py"},
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
    """Validated plan -> storyboard/states.json + storyboard.json + project.json (engine contract);
    an AUDIO_LOCKED plan also schedules the measured narration onto the shots (script/timing.json)."""
    from planner import compiler
    do_validate_plan(p)
    plan = read_json(p / "storyboard" / "visual_plan.json")
    for path in compiler.compile_plan(plan, p):
        print("WROTE:", path)
    if plan["timing_mode"] == "AUDIO_LOCKED":
        from pipeline import audio_lock
        try:
            timing = audio_lock.finalize(p)
        except audio_lock.AudioLockError as e:
            raise SystemExit(f"ERROR: {e}")
        print(f"WROTE: {p / 'script/timing.json'} ({len(timing['shots'])} shots, {timing['total_frames']} frames = "
              f"{timing['total_seconds']:.3f} s, narration locked)")
    do_validate(p)


def do_research_map(p):
    """M6: sentence -> claim -> source -> asset -> component -> annotation -> timing -> QA."""
    from planner import research_map
    print("WROTE:", research_map.write(p))


def do_lock_audio(p):
    """M6: measured narration (narrate + asr-check + align) -> locked beat timing for plan-visuals."""
    from pipeline import audio_lock
    try:
        timing = audio_lock.lock_beats(p)
    except audio_lock.AudioLockError as e:
        raise SystemExit(f"ERROR: {e}")
    lead, tail = timing["pacing"]["beat_lead_in_seconds"], timing["pacing"]["beat_tail_seconds"]
    for b in timing["beats"]:
        print(f"  {b['id']}: {b['duration']:.3f} s speech, window {lead + b['duration'] + tail:.3f} s, "
              f"{len(b['sentences'])} sentences")
    total = sum(lead + b["duration"] + tail for b in timing["beats"])
    if not timing["locked"]:
        for prob in timing["problems"]:
            print("ERROR:", prob)
        raise SystemExit("timing NOT locked (fail closed): plan-visuals refuses AUDIO_LOCKED planning")
    print(f"LOCKED: {len(timing['beats'])} beats, about {total:.2f} s -> {p / 'script/timing.json'}")


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
    # Never give restricted narration (M7: or unapproved claims) a publishable-looking name.
    label = output_label(p)
    out = p / "output" / f"{slug_name(p)}_{label}{suffix(preset)}.mp4"
    if preset in INTERNAL_PRESETS:   # M7: an internal review, never publication-named (M8.2: also 720p)
        review_label = read_json(p / "project.json").get("review_label", "FINAL_INTERNAL_REVIEW")
        out = p / "output" / f"{slug_name(p)}_{review_label}_{preset.split('_')[1]}.mp4"
        label = "documentary_INTERNAL_REVIEW"
    report = assemble.assemble(p, video, out, comment=internal_comment(label) if label.startswith("documentary") else None)
    if preset in INTERNAL_PRESETS and "INTERNAL_REVIEW" not in out.name:
        raise SystemExit(f"refusing an {preset} output without INTERNAL_REVIEW in its name: {out.name}")
    if label.startswith("documentary"):   # M7: clean narration master + loudness-normalised full audio next to the film
        raw = Path(report["narration_track"]).with_name("narration_track_full.wav")
        for src, name in ((raw, "narration_master_clean"), (Path(report["narration_track"]), "audio_master")):
            target = out.with_name(f"{slug_name(p)}_{name}{suffix(preset)}.wav")
            shutil.copyfile(src, target)
            report[name] = str(target.relative_to(p))
    (p / "qa" / f"assembly_report{suffix(preset)}.json").write_text(json.dumps(portable(report, p), indent=2))
    if report["problems"]:
        raise SystemExit("Assembly QA FAILED: " + "; ".join(report["problems"]))
    write_subtitle_qa(p, report)
    print(f"SUCCESS: {out} (+ {Path(report['subtitles']).name}); narration rights: {', '.join(classes)}")


def portable(report, p):
    """Copy of an assembly report with project paths made project-relative (M7: no absolute local
    paths in tracked QA data)."""
    out = dict(report)
    for key in ("output", "subtitles", "narration_track"):
        if out.get(key) and Path(out[key]).is_absolute() and Path(out[key]).is_relative_to(p):
            out[key] = str(Path(out[key]).relative_to(p))
    return out


def output_label(p):
    """Name part of an assembled film: never publishable-looking while anything is pending (M7)."""
    from pipeline import assemble
    project = read_json(p / "project.json")
    cleared, _ = assemble.narration_rights(p)
    if project.get("mode") != "documentary":
        return "pilot" if cleared else "pilot_INTERNAL"
    claims = {c["id"]: c.get("review_status") for c in read_json(p / "research/sources.json")["claims"]}
    narration = read_json(p / "script/narration.json")
    used = {c for b in narration["beats"] for c in b.get("claim_ids", [])}
    approved = all(claims.get(c) == "EDITORIALLY_APPROVED" for c in used) and project.get("factual_review") == "verified"
    voice = narration.get("voice") or {}
    lic = voice.get("license") or {}
    voice_ok = lic.get("status") == "APPROVED" and lic.get("owner_confirmation_for_this_film") != "PENDING" \
        and (voice.get("pronunciation_review") or {}).get("status") != "PENDING"
    return "documentary" if cleared and approved and voice_ok else "documentary_INTERNAL_REVIEW"


def internal_comment(label):
    return None if not label.endswith(("_INTERNAL", "_INTERNAL_REVIEW")) else \
        "INTERNAL REVIEW - editorial approval and/or rights pending - not for publication"


def chapter_shots(p, chapter):
    from pipeline import chapters as CH
    doc = CH.load(p)
    if not doc:
        raise SystemExit(f"{p.name} has no chapters file")
    ranges, errors = CH.shot_ranges(doc, read_json(p / "script/timing.json"))
    if errors:
        raise SystemExit("chapters invalid: " + "; ".join(errors))
    if chapter not in ranges:
        raise SystemExit(f"Unknown chapter {chapter}; chapters: {', '.join(ranges)}")
    ids = set(ranges[chapter]["shots"])
    return [s for s in shots(p) if s["id"] in ids]


def chapter_media_qa(p, preset, chapter, video, chapter_list):
    """Per-chapter silent-video checks: frame count, format, decode errors, black segments, cuts."""
    want = read_json(ROOT / "config/render_presets.json")[preset]
    fps = read_json(p / "project.json")["fps"]
    expected = sum(expected_frames(p, s) for s in chapter_list)
    info = probe(video)
    info.update(black_segments=black_segments(video), decode_errors=decode_errors(video), streams=stream_types(video))
    problems = []
    if info["frames"] != expected:
        problems.append(f"{info['frames']} frames, expected {expected}")
    if (info["width"], info["height"]) != (want["width"], want["height"]) or info["fps"] != f"{fps}/1":
        problems.append(f"{info['width']}x{info['height']} {info['fps']}")
    if info["decode_errors"] or info["black_segments"]:
        problems.append(f"decode errors {info['decode_errors']}, black segments {info['black_segments']}")
    ids = [s["id"] for s in chapter_list]
    cuts = [c for c in boundary_ssim(p, preset, chapter_list)]
    problems += [f"cut {c['cut']}: SSIM {c['ssim']} < {CUT_SSIM_MIN}" for c in cuts if not c["ok"]]
    wm = watermark_spec(p, preset)
    watermark = None
    if wm:
        watermark = dict(wm, check=watermark_check(p, preset, video, p / "renders" / preset / ids[0] / "frame_0001.png", wm),
                         backgrounds=watermark_backgrounds(p, preset, chapter_list, wm))
        if not watermark["check"]["present"]:
            problems.append(f"watermark not found in its box: {watermark['check']}")
    return {"chapter": chapter, "video": str(video.relative_to(p)), "shots": ids, "expected_frames": expected,
            "probe": info, "cuts": cuts, "watermark": watermark, "problems": problems}


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 22), b""):
            h.update(block)
    return h.hexdigest()


def registry_path(p, preset):
    return p / "qa" / f"chapter_intermediates{suffix(preset)}.json"


def read_registry(p, preset):
    path = registry_path(p, preset)
    return read_json(path) if path.is_file() else {"preset": preset, "chapters": {}}


def write_registry(p, preset, reg):
    path = registry_path(p, preset)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(reg, indent=2))
    os.replace(tmp, path)   # atomic


def shot_keys(p, chapter_list, preset):
    from tools import render_cache
    return {s["id"]: render_cache.cache_key(render_cache.components(p, s, preset)) for s in chapter_list}


def intermediate_problem(p, preset, entry, chapter_list):
    """Why a registered chapter intermediate cannot be reused (None = valid). A corrupt, partial or
    stale file is rejected: checksum, inputs of every shot, frame count, size and a full decode."""
    f = p / entry["file"]
    if not f.is_file():
        return "intermediate missing"
    if sha256_of(f) != entry["sha256"]:
        return "checksum differs (corrupt or replaced)"
    if shot_keys(p, chapter_list, preset) != entry["shot_keys"]:
        return "shot inputs changed since it was encoded"
    if entry.get("watermark") != watermark_spec(p, preset):
        return "watermark changed since it was encoded (config/branding.json, project.json)"
    info = probe(f)
    want = read_json(ROOT / "config/render_presets.json")[preset]
    if info["frames"] != entry["frames"] or (info["width"], info["height"]) != (want["width"], want["height"]):
        return f"{info['frames']} frames {info['width']}x{info['height']}, registry says {entry['frames']}"
    if decode_errors(f):
        return "decode errors"
    return None


def free_gb(p):
    return shutil.disk_usage(p).free / 1e9


def do_chapter(p, chapter, preset, force=False, release=False):
    """M7: render, encode, assemble (narration + subtitles) and check one chapter on its own.
    Streaming presets (final_4k) keep a verified chapter intermediate in a registry and, with
    `release`, delete the chapter's PNGs once that intermediate is verified (resumable per chapter)."""
    if preset in STILLS_ONLY_PRESETS:
        raise SystemExit(f"--preset {preset} renders selected stills only (`still`), never a full sequence")
    from pipeline import assemble
    do_validate(p, final=(preset in FINAL_PRESETS))
    chapter_list = chapter_shots(p, chapter)
    folder = p / "output" / f"chapters{suffix(preset)}"
    video = folder / f"{slug_name(p)}_{chapter}_silent.mp4"
    reg = read_registry(p, preset)
    entry = reg["chapters"].get(chapter)
    problem = intermediate_problem(p, preset, entry, chapter_list) if entry and not force else "not registered"
    if problem is None:
        print(f"CACHED: chapter {chapter} intermediate {entry['file']} (verified: checksum, inputs, "
              f"{entry['frames']} frames, decode)")
        results = ["cached-intermediate"] * len(chapter_list)
        media = entry["media"]
    else:
        if entry:
            print(f"RE-ENCODE: chapter {chapter} ({problem})")
        cfg = read_json(ROOT / "config/render_presets.json")[preset]
        need = sum(expected_frames(p, s) for s in chapter_list) * cfg.get("est_png_mb", 1.0) / 1000 * 0.6
        if free_gb(p) - need < HEADROOM_GB:
            raise SystemExit(f"Refusing chapter {chapter}: {free_gb(p):.1f} GB free, about {need:.1f} GB of frames "
                             f"needed and {HEADROOM_GB} GB headroom must remain")
        results = [render_shot(p, s, preset, force) for s in chapter_list]
        encode_sequence(p, preset, chapter_list, video, f"ffmpeg_{chapter}{suffix(preset)}")
        media = chapter_media_qa(p, preset, chapter, video, chapter_list)
        if media["problems"]:
            raise SystemExit(f"Chapter {chapter} intermediate QA FAILED: " + "; ".join(media["problems"]))
        reg["chapters"][chapter] = {"file": str(video.relative_to(p)), "sha256": sha256_of(video),
                                    "frames": media["expected_frames"], "shot_keys": shot_keys(p, chapter_list, preset),
                                    "watermark": watermark_spec(p, preset), "media": media, "encoded_utc": datetime.now(timezone.utc).isoformat(),
                                    "free_gb_after_encode": round(free_gb(p), 1)}
        write_registry(p, preset, reg)
        if release:   # the verified intermediate (+ registry, manifests) now stands for these frames
            freed = 0
            for s in chapter_list:
                seq = p / "renders" / preset / s["id"]
                for frame in seq.glob("frame_*.png"):
                    if frame.stat().st_nlink == 1:
                        freed += frame.stat().st_size
                    frame.unlink()
                m = read_json(seq / "render_manifest.json")
                m["frames_released"] = {"intermediate": reg["chapters"][chapter]["file"],
                                        "sha256": reg["chapters"][chapter]["sha256"]}
                (seq / "render_manifest.json").write_text(json.dumps(m, indent=2))
            reg["chapters"][chapter]["png_bytes_released"] = freed
            write_registry(p, preset, reg)
            print(f"RELEASED: {freed / 1e9:.2f} GB of {chapter} PNG frames (intermediate verified first)")
    label = output_label(p)
    out = folder / f"{slug_name(p)}_{chapter}_{label}.mp4"
    report = assemble.assemble(p, video, out, [s["id"] for s in chapter_list], comment=internal_comment(label),
                               audio_bitrate=read_json(ROOT / "config/render_presets.json")[preset].get("audio_bitrate", "160k"))
    report["media"] = media
    report["render_results"] = {s["id"]: r for s, r in zip(chapter_list, results)}
    audio_out = folder / f"{slug_name(p)}_{chapter}_narration.wav"   # chapter audio (loudness-normalised)
    shutil.copyfile(report["narration_track"], audio_out)
    report["chapter_audio"] = str(audio_out.relative_to(p))
    report["problems"] = media["problems"] + report["problems"]
    (p / "qa" / f"chapter_{chapter}{suffix(preset)}.json").write_text(json.dumps(portable(report, p), indent=2))
    if report["problems"]:
        raise SystemExit(f"Chapter {chapter} QA FAILED: " + "; ".join(report["problems"]))
    print(f"SUCCESS: {out} ({media['expected_frames']} frames, {len(chapter_list)} shots: "
          + ", ".join(f"{k} {list(report['render_results'].values()).count(k)}" for k in ("rendered", "resumed", "cached")) + ")")


def final_outputs(p, preset, cfg):
    """The assembled film and its silent concatenation. g-r9: an internal preset assembled from its chapters is an
    internal review, named like `assemble` names one (project.json review_label + INTERNAL_REVIEW), never FINAL: no
    file named FINAL may exist before the owner's approval."""
    if preset in INTERNAL_PRESETS:
        review_label = read_json(p / "project.json").get("review_label", "INTERNAL_REVIEW")
        if "INTERNAL_REVIEW" not in review_label or "FINAL" in review_label.upper():
            raise SystemExit(f"project.json review_label {review_label!r}: an internal review needs INTERNAL_REVIEW "
                             "in its name and never FINAL")
        stem = f"{slug_name(p)}_{review_label}_{preset.split('_')[1]}"
        return p / "output" / f"{stem}.mp4", p / "output" / f"{stem}_video.mp4"
    tag = "FINAL_4K_2160p" if cfg["height"] == 2160 else f"FINAL_{cfg['height']}p"
    out = p / "output" / (f"{slug_name(p)}_{tag}.mp4" if output_label(p) == "documentary"
                          else f"{slug_name(p)}_{tag}_INTERNAL_REVIEW.mp4")
    return out, p / "output" / f"{slug_name(p)}_{tag}_video.mp4"


def do_final_assemble(p, preset):
    """M7: the final film from the verified chapter intermediates of a streaming preset: concatenated
    without re-encoding, then narration + subtitles (assemble.assemble) and a media QA of the actual file."""
    from pipeline import assemble, chapters as CH
    do_validate(p, final=(preset in FINAL_PRESETS))
    doc = CH.load(p)
    timing = read_json(p / "script/timing.json")
    ranges, errors = CH.shot_ranges(doc, timing)
    if errors:
        raise SystemExit("chapters invalid: " + "; ".join(errors))
    reg = read_registry(p, preset)
    story = {s["id"]: s for s in shots(p)}
    files = []
    for c in doc["chapters"]:
        entry = reg["chapters"].get(c["id"])
        problem = intermediate_problem(p, preset, entry, [story[x] for x in ranges[c["id"]]["shots"]]) if entry \
            else "no intermediate"
        if problem:
            raise SystemExit(f"chapter {c['id']}: {problem} - run `chapter --chapter {c['id']} --preset {preset}`")
        files.append(p / entry["file"])
    cfg = read_json(ROOT / "config/render_presets.json")[preset]
    out, video = final_outputs(p, preset, cfg)
    label = output_label(p)
    lst = p / "output" / f".concat_{preset}.txt"
    lst.write_text("".join(f"file '{f.resolve()}'\n" for f in files))
    partial = video.with_name(video.stem + ".partial.mp4")
    try:
        run_logged([ffmpeg_bin(), "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy",
                    "-movflags", "+faststart", str(partial)], p / "qa" / f"ffmpeg_concat{suffix(preset)}.log")
    finally:
        lst.unlink()
    os.replace(partial, video)
    effects = None
    from pipeline import sound
    plan = sound.load_plan(p)
    if plan and plan.get("final"):   # the owner's sound effects for the final mix (audio/sound_plan.json, 2026-11-12)
        plan_problems = sound.check_plan(plan)
        if plan_problems:
            raise SystemExit("sound plan: " + "; ".join(plan_problems))
        effects = lambda raw, track: sound.final_effects(p, plan, raw, timing, shots(p))   # noqa: E731
    report = assemble.assemble(p, video, out, comment=internal_comment(label) if label != "documentary" else None,
                               audio_bitrate=cfg.get("audio_bitrate", "160k"), effects=effects)
    media = final_media_qa(p, preset, out, files, doc, ranges, timing)
    report["media"] = media
    report["problems"] = media["problems"] + report["problems"]
    sums = {}
    for f in (out, Path(report["subtitles"]), p / "output" / f"{slug_name(p)}_audio_master{suffix(preset)}.wav"):
        if f.is_file():
            sums[f.name] = sha256_of(f)
    raw = Path(report["narration_track"]).with_name("narration_track_full.wav")
    for src, name in ((raw, "narration_master_clean"), (Path(report["narration_track"]), "audio_master")):
        target = out.with_name(f"{slug_name(p)}_{name}{suffix(preset)}.wav")
        shutil.copyfile(src, target)
        sums[target.name] = sha256_of(target)
    (out.with_suffix(".sha256")).write_text("".join(f"{v}  {k}\n" for k, v in sorted(sums.items())))
    report["checksums"] = sums
    (p / "qa" / f"assembly_report{suffix(preset)}.json").write_text(json.dumps(portable(report, p), indent=2))
    (p / "qa" / f"preview_media_report{suffix(preset)}.json").write_text(json.dumps(media, indent=2))
    write_subtitle_qa(p, report)
    if report["problems"]:
        raise SystemExit("Final assembly QA FAILED: " + "; ".join(report["problems"]))
    print(f"SUCCESS: {out} ({media['frames']} frames {media['width']}x{media['height']}, {report['seconds']:.3f} s)")


def final_media_qa(p, preset, out, files, doc, ranges, timing):
    """QA of the actual final file: size, fps, frame count, codec, colour tags, full decode, black
    frames, and every chapter boundary (match cuts must stay invisible: SSIM >= CUT_SSIM_MIN)."""
    want = read_json(ROOT / "config/render_presets.json")[preset]
    info = probe(out)
    tags = json.loads(subprocess.run([ffprobe_bin(), "-v", "error", "-select_streams", "v:0", "-show_entries",
                                      "stream=color_space,color_primaries,color_transfer,color_range,profile,level",
                                      "-of", "json", str(out)], capture_output=True, text=True, check=True).stdout)["streams"][0]
    problems = []
    if info["frames"] != timing["total_frames"]:
        problems.append(f"{info['frames']} frames, timing says {timing['total_frames']}")
    if (info["width"], info["height"]) != (want["width"], want["height"]) or info["fps"] != f"{want['fps']}/1":
        problems.append(f"{info['width']}x{info['height']} {info['fps']}")
    if want.get("color") == "bt709" and (tags.get("color_space"), tags.get("color_primaries"), tags.get("color_transfer")) \
            != ("bt709", "bt709", "bt709"):
        problems.append(f"colour tags {tags}")
    errs, blacks = decode_errors(out), black_segments(out)
    if errs or blacks:
        problems.append(f"decode errors {errs}, black segments {blacks}")
    story = {s["id"]: s for s in shots(p)}
    boundaries = []   # the final file is a stream copy of the intermediates: compare their edge frames
    for (a, fa), (b, fb) in zip(zip(doc["chapters"], files), list(zip(doc["chapters"], files))[1:]):
        first_next = story[ranges[b["id"]]["shots"][0]]
        last_png, first_png = p / "qa" / "_boundary_last.png", p / "qa" / "_boundary_first.png"
        subprocess.run([ffmpeg_bin(), "-v", "error", "-y", "-sseof", "-0.5", "-i", str(fa), "-update", "1",
                        str(last_png)], check=True)
        subprocess.run([ffmpeg_bin(), "-v", "error", "-y", "-i", str(fb), "-frames:v", "1", str(first_png)], check=True)
        r = subprocess.run([ffmpeg_bin(), "-v", "info", "-i", str(last_png), "-i", str(first_png), "-lavfi", "ssim",
                            "-f", "null", "-"], capture_output=True, text=True)
        value = float(r.stderr.split("All:")[1].split()[0])
        last_png.unlink()
        first_png.unlink()
        mode = first_next.get("cut_from_previous", "match")
        boundaries.append({"cut": f"{a['id']}->{b['id']}", "frame": ranges[b["id"]]["start_frame"], "mode": mode,
                           "ssim": round(value, 5), "ok": mode == "hard" or value >= CUT_SSIM_MIN})
    problems += [f"chapter cut {x['cut']}: SSIM {x['ssim']} (match cut must be invisible)" for x in boundaries if not x["ok"]]
    return {"preset": preset, "file": str(out.relative_to(p)), **info, "color": tags, "decode_errors": errs,
            "black_segments": blacks, "watermark": watermark_spec(p, preset), "chapter_intermediates": [str(f.relative_to(p)) for f in files],
            "chapter_boundaries": boundaries, "expected_total_frames": timing["total_frames"], "problems": problems}


def do_verify_reuse(p, preset, shot_id):
    """M7: re-render up to three reused frames of a rendered shot directly and compare pixels."""
    seq = p / "renders" / preset / shot_id
    strategy = read_json(seq / "render_strategy.json")
    runs = sorted(strategy.get("reused_runs") or [], key=lambda r: r[2] - r[1], reverse=True)
    if not runs:
        raise SystemExit(f"{shot_id}: no reused frames ({strategy.get('strategy')})")
    picks = sorted({runs[0][1], (runs[0][1] + runs[0][2]) // 2, runs[-1][2]})
    out = p / "qa" / "reuse_verification"
    out.mkdir(parents=True, exist_ok=True)
    report = out / f"{shot_id}_{preset}.json"
    run_logged(blender_command(p, "verify-reuse", preset, "--shot", shot_id, "--frames", ",".join(map(str, picks)),
                               "--output", str(out), "--report", str(report)), p / "qa" / f"verify_{shot_id}_{preset}.log")
    rows = read_json(report)["frames"]
    for r in rows:
        nf = r["noise_floor"]
        print(f"  frame {r['frame']} (reuses {r['source_frame']}): max |diff| {r['max_abs_diff']:.2e}, "
              f"{r['differing_pixels']} px differ, PSNR {r['psnr_db']} dB | noise floor of a re-render of the same "
              f"frame: max {nf['max_abs_diff']:.2e}, {nf['differing_pixels']} px, PSNR {nf['psnr_db']} dB")
    if not all(r["identical"] or r["within_render_noise"] for r in rows):
        raise SystemExit(f"{shot_id}: a reused frame differs from its direct render beyond the render noise")
    print(f"PASS: {len(rows)} reused frames of {shot_id} match direct renders "
          f"({'identical' if all(r['identical'] for r in rows) else 'within EEVEE render noise'}; {strategy['strategy']})")


def do_chapters(p, preset):
    """M7: validate chapters, write chapters/chapter_manifest.json + qa/longform_qa.json."""
    from pipeline import chapters as CH
    try:
        rows, m = CH.longform_qa(p, preset)
    except ValueError as e:
        raise SystemExit(f"ERROR: {e}")
    (p / "chapters").mkdir(exist_ok=True)
    (p / "chapters" / "chapter_manifest.json").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    for c in m["chapters"]:
        print(f"  {c['id']} {c['start_seconds']:7.1f}s {c['duration_seconds']:6.1f}s  {len(c['shots']):>2} shots  "
              f"{c['render']['frames_on_disk']:>5}/{c['frames']} frames [{preset}]  {c['title']}")
    for r in rows:
        print(f"{r['status']:>5}  {r['check']}: {r['detail']}")
    report = {"utc": datetime.now(timezone.utc).isoformat(), "preset": preset, "timing_sha256": m["timing_sha256"],
              "results": rows, "failed": sum(r["status"] == "FAIL" for r in rows)}
    (p / "qa" / "longform_qa.json").write_text(json.dumps(report, indent=2, ensure_ascii=False))
    if report["failed"]:
        raise SystemExit(f"Long-form QA: {report['failed']} check(s) FAILED")
    print(f"Long-form QA: PASS => {p / 'qa/longform_qa.json'}")


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


def do_verify_visibility(p, preset):
    """Level 2 (Blender ray casts) vs Level 1 (offline raster) for every evaluation frame of every
    shot with explanatory targets: qa/visibility_measured.json, qa/visibility_report.json, qa/VISIBILITY.md."""
    import time
    from planner import camera as CAM, visibility as VIS
    measured = p / "qa" / "visibility_measured.json"
    cmd = [blender_bin(), "--background", "--factory-startup", "--python-exit-code", "1", "--python",
           str(ROOT / "engine" / "qa_visibility.py"), "--", "--project", str(p), "--preset", preset, "--out", str(measured)]
    t0 = time.time()
    run_logged(cmd, p / "qa" / "verify_visibility.log")
    t_blender = time.time() - t0
    l2 = read_json(measured)
    cfg = read_json(ROOT / "config/visual_planning.json")["visibility"]
    states, story = read_json(p / "storyboard/states.json"), read_json(p / "storyboard/storyboard.json")
    fps = read_json(p / "project.json")["fps"]
    presets = CAM.style_presets()
    t0 = time.time()
    rows, deltas, agree, total = [], [], 0, 0
    for shot in story["shots"]:
        if shot["id"] not in l2["shots"]:
            continue
        l1 = VIS.assess_all_frames(shot, states, fps, presets, cfg)
        for label, frame in l1["frames"].items():
            for a, b in zip(l1["rows"][label], l2["shots"][shot["id"]]["rows"].get(label, [])):
                if not (a.get("shown") and b.get("shown")):
                    continue
                pieces = any(t.get("pieces") for t in VIS.targets_of(shot) if t["concept"] == b["concept"]) and \
                    templates_template(shot) == "EXPLODED_VIEW"
                ok2, _, prob2 = VIS.verdict(b, cfg, pieces)
                total += 1
                agree += ok2 == a["ok"]
                deltas.append(abs(a["visible_share"] - b["visible_share"]))
                rows.append({"shot": shot["id"], "beat": (shot.get("beat_ids") or [shot["id"]])[0],
                             "frame": frame, "label": label, "concept": a["concept"],
                             "explanatory": label in l1["explanatory"],
                             "L1": {k: a[k] for k in ("visible_share", "core_area", "visible_area", "ok")} | {
                                 "problems": a["problems"], "geometry": a["geometry"], "verification": a["verification"]},
                             "L2": {k: b[k] for k in ("visible_share", "core_area", "visible_area")} | {
                                 "ok": ok2, "problems": prob2, "occluders": b["occluders"]}})
    t_l1 = time.time() - t0
    summary = {"rows": total, "verdict_agreement": round(agree / total, 4) if total else None,
               "mean_abs_share_error": round(sum(deltas) / len(deltas), 4) if deltas else None,
               "max_abs_share_error": round(max(deltas), 4) if deltas else None,
               "level2_seconds": round(t_blender, 1), "level1_seconds": round(t_l1, 2),
               "explanatory_failures_L2": sum(1 for r in rows if r["explanatory"] and not r["L2"]["ok"])}
    by_beat = {}
    for r in rows:   # a concept must read at an explanatory frame of at least one shot of its beat
        if r["explanatory"]:
            by_beat.setdefault((r["beat"], r["concept"]), []).append(r["L2"]["ok"])
    summary["beat_concepts"] = len(by_beat)
    summary["beat_concepts_unreadable_L2"] = sorted(f"{b} {c}" for (b, c), oks in by_beat.items() if not any(oks))
    report = {"project": p.name, "preset": preset, "grid": cfg["raster"], "summary": summary, "rows": rows}
    (p / "qa" / "visibility_report.json").write_text(json.dumps(report, indent=1) + "\n")
    lines = [f"# Visibility: Level 1 estimate vs Level 2 Blender measurement ({p.name})", "",
             f"- {total} target x frame rows; verdict agreement **{summary['verdict_agreement']}**; visible-share error "
             f"mean {summary['mean_abs_share_error']}, max {summary['max_abs_share_error']}.",
             f"- Level 2 (Blender, {cfg['raster'][0]}x{cfg['raster'][1]} orthographic rays, evaluated meshes): "
             f"{summary['level2_seconds']} s; Level 1 (offline raster): {summary['level1_seconds']} s.",
             f"- Explanatory frames failing in Blender: {summary['explanatory_failures_L2']} (a concept only has to read "
             f"in one shot of its beat); beat concepts unreadable in Blender: "
             f"{', '.join(summary['beat_concepts_unreadable_L2']) or 'none'} of {summary['beat_concepts']}.", "",
             "| Shot | Frame | Concept | L1 share / core % / area % | L2 share / core % / area % | L1 | L2 | L2 occluders |",
             "|---|---|---|---|---|---|---|---|"]
    for r in rows:
        if not (r["explanatory"] or r["L1"]["ok"] != r["L2"]["ok"]):
            continue
        a, b = r["L1"], r["L2"]
        lines.append(f"| {r['shot']} | {r['label']} ({r['frame']}) | {r['concept']} | {a['visible_share']:.2f} / "
                     f"{a['core_area'] * 100:.2f} / {a['visible_area'] * 100:.2f} | {b['visible_share']:.2f} / "
                     f"{b['core_area'] * 100:.2f} / {b['visible_area'] * 100:.2f} | {'reads' if a['ok'] else ', '.join(a['problems'])} | "
                     f"{'reads' if b['ok'] else ', '.join(b['problems'])} | {', '.join(o['id'] for o in b['occluders'][:2]) or '—'} |")
    (p / "qa" / "VISIBILITY.md").write_text("\n".join(lines) + "\n")
    print(f"Visibility: {total} rows, agreement {summary['verdict_agreement']}, share error mean "
          f"{summary['mean_abs_share_error']} max {summary['max_abs_share_error']}; Blender {summary['level2_seconds']} s"
          f" => {p / 'qa' / 'VISIBILITY.md'}")
    if summary["beat_concepts_unreadable_L2"]:
        raise SystemExit("unreadable in Blender: " + ", ".join(summary["beat_concepts_unreadable_L2"]))


def do_evaluate_planning():
    """Visual-planning evaluation dataset (planner/evaluate.py) -> evaluation/visual_planning/RESULTS.md."""
    import time
    from planner import evaluate
    t0 = time.time()
    summary = evaluate.run()
    report = evaluate.write_report(summary, ROOT / "evaluation/visual_planning")
    for r in summary["results"]:
        print(f"{'PASS' if r['ok'] else 'FAIL'}  {r['id']:<10} {r['kind']:<19} {r['family']:<7} {r['title']}")
    for d, v in summary["dimensions"].items():
        print(f"  {d:<24} {v['passed']}/{v['checks']}")
    print(f"{summary['passed']}/{summary['cases']} cases in {time.time() - t0:.1f} s => {report}")
    if summary["passed"] != summary["cases"]:
        raise SystemExit(2)


def templates_template(shot):
    return (shot.get("animation") or {}).get("template") or shot.get("transition")


def do_gates(p, preset):
    """G0-G6 (+GV) + status flags for the project's production profile (pipeline/gates.py); writes qa/gates.json."""
    from pipeline import gates
    result = gates.evaluate(p, suffix(preset))
    for name, g in result["gates"].items():
        print(f"{g['status']:>18}  {name}: {'; '.join(g['notes'])}")
    print("Profile:", result.get("profile"))
    print("Statuses:", ", ".join(result["statuses"]))
    print(f"Verdict: {result['verdict']}")
    (p / "qa" / "gates.json").write_text(json.dumps(result, indent=2, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description="Architecture Story Studio — Mac M4 pilot CLI")
    parser.add_argument("command", choices=["doctor", "validate", "still", "preview", "shot", "encode",
                                            "check-blender", "final-gate", "manifest", "tts-check", "narrate",
                                            "asr-check", "schedule", "smoke", "assemble", "gates", "cache-report", "align",
                                            "asset-check", "asset-render", "asset-catalog",
                                            "plan-visuals", "validate-plan", "build-shots", "verify-visibility", "lock-audio",
                                            "research-map", "chapters", "chapter", "verify-reuse", "final-assemble",
                                            "evaluate-planning", "new-episode", "episode-status"])
    parser.add_argument("--project", help="Project slug in projects/ (default: the only project there)")
    parser.add_argument("--topic", help="new-episode: the documentary topic")
    parser.add_argument("--slug", help="new-episode: project slug (default: derived from the topic)")
    parser.add_argument("--preset", default="preview",
                        choices=["preview", "review", "production_test", "internal_1080p", "internal_720p", "final", "final_4k"])
    parser.add_argument("--release-frames", action="store_true",
                        help="chapter: delete the chapter's PNG frames after its intermediate is verified")
    parser.add_argument("--shot", help="Shot id for the `shot` command, e.g. SC_002")
    parser.add_argument("--chapter", help="chapter: chapter id from script/chapters.json, e.g. C4")
    parser.add_argument("--asset", help="asset-*: one asset spec path (default: every spec in asset_library/architecture)")
    parser.add_argument("--force", action="store_true", help="Re-render shots even if cached")
    parser.add_argument("--no-reuse", action="store_true", help="render every frame (no static-frame reuse)")
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
    if args.command == "evaluate-planning":
        do_evaluate_planning()
        return
    from tools import episode
    if args.command == "new-episode":
        if not args.topic:
            raise SystemExit('--topic is required, e.g. --topic "Why traditional Japanese houses use different roof forms"')
        episode.main(["new", "--topic", args.topic] + (["--slug", args.slug] if args.slug else []))
        return
    global NO_REUSE
    NO_REUSE = args.no_reuse
    p = project_path(args.project or default_project())
    if args.command == "episode-status":
        episode.main(["status", "--project", p.name])
    elif args.command == "validate":
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
    elif args.command == "verify-visibility":
        do_verify_visibility(p, args.preset)
    elif args.command == "build-shots":
        do_build_shots(p)
    elif args.command == "lock-audio":
        do_lock_audio(p)
    elif args.command == "research-map":
        do_research_map(p)
    elif args.command == "chapters":
        do_chapters(p, args.preset)
    elif args.command == "chapter":
        if not args.chapter:
            raise SystemExit("--chapter is required, e.g. --chapter C4")
        do_chapter(p, args.chapter, args.preset, args.force, release=args.release_frames)
    elif args.command == "final-assemble":
        do_final_assemble(p, args.preset)
    elif args.command == "verify-reuse":
        if not args.shot:
            raise SystemExit("--shot is required, e.g. --shot SC_017")
        do_verify_reuse(p, args.preset, args.shot)
    elif args.command == "cache-report":
        do_cache_report(p, args.preset)


if __name__ == "__main__":
    main()
