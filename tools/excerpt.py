"""An excerpt of a film for review: chosen shots (not necessarily adjacent), their narration, subtitles and sound cues.

    python3 tools/excerpt.py --project <slug> --preset internal_720p --shots SC_012,SC_013,SC_016,SC_017 --label PILOT_G_R4

The shots are rendered (or taken from the render cache) exactly as in the film. Each shot keeps its own stretch of
the film's narration track, so a non-adjacent excerpt is the film with the other shots cut out; where two kept shots
are not adjacent in the film the report marks an "excerpt join" (no continuity is promised there). Sound cues of
SEQUENCE shots (pipeline/sound.py) are mixed under the narration, with the recorded sounds, extra cues and beds of
the project's audio/sound_plan.json when it has one; a second file without any of them is written next to it so the
owner can compare. Names always carry INTERNAL_REVIEW.

QA: frames, decode errors, black segments, the film's own cuts (SSIM), A/V drift, loudness, subtitles, and, with an
ASR interpreter available, Whisper on the clean and the mixed narration of every shot (the sounds must not cost
intelligibility). An agent cannot listen: the sounds themselves are for the owner to judge.
"""
import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from pipeline import assemble, sound, subtitles  # noqa: E402
from tools import cli  # noqa: E402


def excerpt_runs(film_ids, ids):
    """Runs of shots that are adjacent in the film: [[ids...], ...]."""
    pos = {s: i for i, s in enumerate(film_ids)}
    runs = []
    for s in ids:
        if runs and pos[s] == pos[runs[-1][-1]] + 1:
            runs[-1].append(s)
        else:
            runs.append([s])
    return runs


def narration_slices(samples, timing, ids, sr):
    """The film narration (mono samples) cut to the chosen shots, in order, with each shot's offset in the excerpt."""
    fps = timing["fps"]
    per = sr // fps
    by_id = {s["id"]: s for s in timing["shots"]}
    out, offsets, t = [], {}, 0
    for sid in ids:
        s = by_id[sid]
        a, b = s["start_frame"] * per, (s["start_frame"] + s["frames"]) * per
        out += samples[a:b]
        offsets[sid] = t / fps
        t += s["frames"]
    return out, offsets


def excerpt_cues(story_shots, ids, offsets):
    cues = []
    for shot in story_shots:
        if shot["id"] in ids:
            cues += [dict(c, at_seconds=round(offsets[shot["id"]] + c["at_seconds"], 4), shot=shot["id"])
                     for c in shot.get("sound_cues") or []]
    return sorted(cues, key=lambda c: c["at_seconds"])


def build(p, preset, ids, label):
    if "FINAL" in label.upper():
        raise SystemExit("an excerpt is a review file; its label must not say FINAL")
    timing = cli.read_json(p / "script/timing.json")
    story = cli.read_json(p / "storyboard/storyboard.json")["shots"]
    film_ids = [s["id"] for s in story]
    unknown = [s for s in ids if s not in film_ids]
    if unknown:
        raise SystemExit(f"unknown shots {unknown}")
    ids = sorted(ids, key=film_ids.index)
    shots = [s for s in story if s["id"] in ids]
    results = {s["id"]: cli.render_shot(p, s, preset) for s in shots}
    folder = p / "output" / "pilot"
    stem = f"{cli.slug_name(p)}_{label}_INTERNAL_REVIEW_{preset.split('_')[-1]}"
    silent = cli.encode_sequence(p, preset, shots, folder / f"{stem}_silent.mp4", f"ffmpeg_{label}")
    fps = timing["fps"]
    frames = sum(cli.expected_frames(p, s) for s in shots)
    info = cli.probe(silent)
    problems = []
    if info["frames"] != frames:
        problems.append(f"{info['frames']} frames, expected {frames}")
    black, decode = cli.black_segments(silent), cli.decode_errors(silent)
    if black or decode:
        problems.append(f"black segments {black}, decode errors {decode}")
    wm = cli.watermark_spec(p, preset)   # the channel watermark, burnt in by encode_sequence
    if wm:
        wm = dict(wm, check=cli.watermark_check(p, preset, silent, p / "renders" / preset / ids[0] / "frame_0001.png", wm))
        if not wm["check"]["present"]:
            problems.append(f"watermark not found in its box: {wm['check']}")
    runs = excerpt_runs(film_ids, ids)
    cuts = []
    for run in runs:   # the film's own cuts inside each run keep their promise
        cuts += cli.boundary_ssim(p, preset, [s for s in shots if s["id"] in run])
    problems += [f"cut {c['cut']}: SSIM {c['ssim']} < {cli.CUT_SSIM_MIN}" for c in cuts if not c["ok"]]
    joins = [f"{a[-1]}->{b[0]}" for a, b in zip(runs, runs[1:])]

    # audio: the film's narration cut to these shots, the cues under it
    work = p / "audio" / "excerpt"
    work.mkdir(parents=True, exist_ok=True)
    full = assemble.build_narration_track(p, timing, work / "film_narration.wav")
    ch, sr, samples = sound.read_wav(full["path"])
    if ch != 1:
        raise SystemExit("mono narration expected")
    clean, offsets = narration_slices(samples, timing, ids, sr)
    cues = excerpt_cues(story, ids, offsets)
    expected = sum((len(st["components"]) if st.get("stagger_seconds") else 1)
                   for s in shots for st in (s.get("animation") or {}).get("steps") or [] if st.get("sound"))
    if len(cues) != expected:   # a cue lost between the plan and the storyboard would pass silently otherwise
        problems.append(f"{len(cues)} sound cues in the storyboard, {expected} sounding steps in the shots")
    plan, beds = sound.load_plan(p), []
    if plan:   # recorded sounds, extra cues and beds the project lists with their licence (audio/sound_plan.json)
        plan_problems = sound.check_plan(plan)
        if plan_problems:
            raise SystemExit("sound plan: " + "; ".join(plan_problems))
        extra, beds, plan_problems = sound.film_plan_cues(p, plan, story, timing, ids, offsets)
        problems += plan_problems
        cues = sorted(cues + extra, key=lambda c: c["at_seconds"])
    mixed, mix_report = sound.mix_under(clean, cues, sr, plan=plan, beds=beds)
    if mix_report["clipped_samples"]:
        problems.append(f"{mix_report['clipped_samples']} clipped samples in the mix")
    outputs = {}
    for name, track in (("", mixed), ("_no_sfx", clean)):
        raw = work / f"{label}{name}_raw.wav"
        sound.write_wav(raw, track, sr)
        norm = work / f"{label}{name}_norm.wav"
        assemble.loudnorm(raw, norm)
        out = folder / f"{stem}{name}.mp4"
        assemble.mux(silent, norm, out, "INTERNAL REVIEW - pilot excerpt - editorial approval and rights pending - "
                                        "not for publication",
                     cli.read_json(ROOT / "config/render_presets.json")[preset].get("audio_bitrate", "160k"))
        outputs[name or "with_sfx"] = (out, norm, raw)

    # subtitles: each run's cues, moved to the run's place in the excerpt
    manifest = cli.read_json(p / "audio/narration_manifest.json")
    from pipeline import pronunciation as pron
    aliases = pron.asr_aliases(pron.load(p))
    by_id = {s["id"]: s for s in timing["shots"]}
    cues_sub = []
    for run in runs:
        origin = by_id[run[0]]["start_frame"] / fps
        seconds = sum(by_id[s]["frames"] for s in run) / fps
        for c in subtitles.build_cues(p, timing, manifest, aliases, run, origin, total=seconds):
            cues_sub.append(dict(c, start=c["start"] + offsets[run[0]], end=c["end"] + offsets[run[0]]))
    sentences = {f"{b['id']}.s{s['index']}": s["text"] for b in timing["beats"] if b["shot"] in ids for s in b["sentences"]}
    sub_problems, sub_warnings, sub_stats = subtitles.qa(cues_sub, frames / fps, sentences)
    problems += sub_problems
    files = {}
    for key, (out, norm, raw) in outputs.items():
        srt = out.with_suffix(".en.srt")
        subtitles.write_srt(cues_sub, srt)
        assemble.embed_subtitles(out, srt)
        a = cli.probe(out)
        loud = assemble.ebur128(out)
        drift = abs(a["duration"] - frames / fps)
        if a["frames"] != frames:
            problems.append(f"{out.name}: {a['frames']} frames")
        if drift > 1.0 / fps + 0.05:
            problems.append(f"{out.name}: duration differs from the video by {drift * 1000:.0f} ms")
        if abs(loud["integrated_lufs"] - assemble.LOUDNESS_TARGET) > 1.0:
            problems.append(f"{out.name}: {loud['integrated_lufs']} LUFS")
        if loud["true_peak_dbtp"] is not None and loud["true_peak_dbtp"] > -1.0:
            problems.append(f"{out.name}: true peak {loud['true_peak_dbtp']} dBTP")
        files[key] = {"file": str(out.relative_to(p)), "subtitles": str(srt.relative_to(p)), "seconds": round(a["duration"], 3),
                      "frames": a["frames"], "loudness": loud, "size_bytes": out.stat().st_size}
    intelligibility = asr_compare(p, shots, offsets, timing, outputs, sr, aliases)
    if intelligibility.get("worse"):
        problems.append("sounds cost intelligibility: " + "; ".join(intelligibility["worse"]))
    report = {"utc": datetime.now(timezone.utc).isoformat(), "label": label, "preset": preset, "shots": ids,
              "render": results, "runs": runs, "excerpt_joins": joins, "frames": frames, "seconds": round(frames / fps, 3),
              "cuts": cuts, "watermark": wm, "offsets_seconds": offsets, "sound_cues": cues, "mix": mix_report,
              "sound_design": sound.load_design(), "sound_plan": plan, "sound_beds": beds, "subtitle_stats": sub_stats, "subtitle_warnings": sub_warnings,
              "files": files, "intelligibility": intelligibility, "problems": problems}
    target = p / "qa" / f"excerpt_{label}.json"
    target.write_text(json.dumps(report, indent=2, ensure_ascii=False))
    silent.unlink()
    for key, f in files.items():
        print(f"  {f['file']}: {f['seconds']} s, {f['frames']} frames, {f['loudness']['integrated_lufs']} LUFS")
    print(f"  {len(cues)} sound cues, {len(beds)} beds; excerpt joins: {', '.join(joins) or 'none'}; report {target}")
    if problems:
        raise SystemExit("Excerpt QA FAILED: " + "; ".join(problems))
    print("SUCCESS: excerpt QA passed")
    return report


def asr_compare(p, shots, offsets, timing, outputs, sr, aliases):
    """Whisper on each shot's clean and mixed narration (word error rate against the script)."""
    from pipeline import asr_check
    try:
        python = asr_check.external_python()
        if not Path(python).is_file():
            return {"status": "NOT_RUN", "reason": f"no ASR interpreter at {python}"}
    except Exception as e:   # noqa: BLE001
        return {"status": "NOT_RUN", "reason": str(e)}
    work = p / "audio" / "excerpt"
    fps = timing["fps"]
    texts = {b["shot"]: " ".join(s["text"] for s in b["sentences"]) for b in timing["beats"]}
    paths, keys = [], []
    for key in ("with_sfx", "_no_sfx"):
        _, samples_sr, samples = sound.read_wav(outputs[key][2])
        for s in shots:
            a = int(round(offsets[s["id"]] * sr))
            b = a + int(round(s["duration_seconds"] * sr))
            path = work / f"asr_{key.strip('_')}_{s['id']}.wav"
            sound.write_wav(path, samples[a:b], samples_sr)
            paths.append(path)
            keys.append((key, s["id"]))
    heard = asr_check.transcribe(paths)
    rows, worse = {}, []
    for (key, sid), res in zip(keys, heard):
        rows.setdefault(sid, {})[key] = {"wer": round(asr_check.wer(texts[sid], res["text"], aliases), 4), "text": res["text"]}
    for sid, r in rows.items():
        if r["with_sfx"]["wer"] > r["_no_sfx"]["wer"] + 0.02:
            worse.append(f"{sid} WER {r['_no_sfx']['wer']} -> {r['with_sfx']['wer']}")
    return {"status": "RUN", "model": "openai/whisper-large-v3-turbo", "rows": rows, "worse": worse}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--project", required=True)
    ap.add_argument("--preset", default="internal_720p")
    ap.add_argument("--shots", required=True, help="comma-separated shot ids")
    ap.add_argument("--label", required=True)
    a = ap.parse_args()
    if a.preset not in cli.INTERNAL_PRESETS + ("preview", "review"):
        raise SystemExit("excerpts are review files: use a preview or internal preset")
    build(ROOT / "projects" / a.project, a.preset, [s.strip() for s in a.shots.split(",") if s.strip()], a.label)


if __name__ == "__main__":
    main()
