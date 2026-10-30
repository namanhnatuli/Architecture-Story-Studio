"""Chapters of a long-form narrated film (M7, stdlib only).

script/chapters.json groups the narration beats into ordered chapters. Each chapter is a
contiguous run of beats, so once the audio is locked and the shots are built it is also a
contiguous run of shots and frames: a chapter can be rendered, encoded, assembled and
checked on its own, and the film is the concatenation of its chapters in order.

  validate(doc, narration, beats_doc)  structural errors (fail closed)
  shot_ranges(doc, timing)             chapter -> shots / frames, from the locked timing
  manifest(p, preset)                  chapters/chapter_manifest.json content
  longform_qa(p, preset)               long-form checks across the whole film
"""
import hashlib
import json
from pathlib import Path

SCHEMA = "chapters/1"
RUNTIME_RANGE = (8 * 60.0, 15 * 60.0)   # M7 acceptable runtime; target 10-12 min
MIN_CHAPTER_SECONDS = 15.0
MAX_SILENCE = 4.0                        # longest narration gap allowed between beats (s)
SILENCE_REPORT = 2.5                     # gaps above this are listed
MAX_STATIC = 14.0                        # longest stretch without any visual event (s)
MAX_SAME_KIND_RUN = 4                    # consecutive shots of one visual kind
EXTERNAL_KINDS = ("image",)


def _read(path):
    path = Path(path)
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else None


def path(p):
    project = _read(Path(p) / "project.json") or {}
    return Path(p) / project.get("chapters", "script/chapters.json")


def load(p):
    return _read(path(p))


def validate(doc, narration, beats_doc=None):
    """Every narration beat is in exactly one chapter, chapters are contiguous and in narration order."""
    errors = []
    if not doc:
        return ["chapters file missing"]
    if doc.get("schema") != SCHEMA:
        errors.append(f"chapters.schema must be {SCHEMA!r}")
    chapters = doc.get("chapters") or []
    if not chapters:
        return errors + ["chapters list is empty"]
    ids = [c.get("id") for c in chapters]
    for cid in sorted({i for i in ids if ids.count(i) > 1}):
        errors.append(f"duplicate chapter id {cid}")
    order = [b["id"] for b in narration.get("beats", [])]
    seen = {}
    for c in chapters:
        if not (c.get("title") or "").strip():
            errors.append(f"{c.get('id')}: chapter has no title")
        if not c.get("beat_ids"):
            errors.append(f"{c.get('id')}: chapter has no beats")
        for b in c.get("beat_ids") or []:
            if b in seen:
                errors.append(f"beat {b} is in chapters {seen[b]} and {c.get('id')}")
            seen[b] = c.get("id")
            if b not in order:
                errors.append(f"{c.get('id')}: beat {b} is not in the narration")
    missing = [b for b in order if b not in seen]
    if missing:
        errors.append(f"beats in no chapter: {', '.join(missing)}")
    flat = [b for c in chapters for b in c.get("beat_ids") or [] if b in order]
    if not missing and flat != order:
        errors.append("chapters must cover the narration beats contiguously and in narration order")
    if beats_doc:
        for vb in beats_doc.get("beats", []):
            want = seen.get(vb.get("beat_id"))
            if vb.get("chapter") and want and vb["chapter"] != want:
                errors.append(f"{vb['beat_id']}: visual beat says chapter {vb['chapter']}, chapters.json says {want}")
    return errors


def shot_ranges(doc, timing):
    """chapter id -> {shots, start_frame, frames}; a shot shared by two chapters is an error."""
    owner = {b: c["id"] for c in doc["chapters"] for b in c["beat_ids"]}
    out, errors = {c["id"]: [] for c in doc["chapters"]}, []
    for s in timing["shots"]:
        cids = sorted({owner.get(b) for b in s["beat_ids"]}, key=str)
        if len(cids) != 1 or cids[0] is None:
            errors.append(f"{s['id']} belongs to chapters {cids}")
            continue
        out[cids[0]].append(s)
    ranges = {}
    prev_end = 0
    for c in doc["chapters"]:
        shots = out[c["id"]]
        if not shots:
            errors.append(f"{c['id']}: no shots")
            continue
        start = shots[0]["start_frame"]
        frames = sum(s["frames"] for s in shots)
        if start != prev_end:
            errors.append(f"{c['id']}: starts at frame {start}, previous chapter ends at {prev_end}")
        if any(b["start_frame"] != a["start_frame"] + a["frames"] for a, b in zip(shots, shots[1:])):
            errors.append(f"{c['id']}: shots are not contiguous")
        prev_end = start + frames
        ranges[c["id"]] = {"shots": [s["id"] for s in shots], "start_frame": start, "frames": frames}
    if timing.get("total_frames") is not None and prev_end != timing["total_frames"]:
        errors.append(f"chapters end at frame {prev_end}, the film has {timing['total_frames']}")
    return ranges, errors


def visual_kind(shot):
    """Coarse visual kind of a storyboard shot for the variety audit."""
    if shot.get("visual_type") == "MOTION_GRAPHICS" or shot.get("camera") == "CARD":
        kinds = {e.get("kind") for e in (shot.get("graphic") or {}).get("elements", [])}
        return "PHOTO" if "image" in kinds else "DIAGRAM" if kinds & {"rect", "line", "polygon", "circle", "arrow"} \
            else "TITLE"
    if (shot.get("animation") or {}).get("camera_move"):
        return "3D_PUSH_IN"
    t = shot.get("transition") or "HOLD"
    return "3D_HOLD" if t == "HOLD" else f"3D_{t}"


def _moving(a, b, step=1.0):
    """Sample points inside an interval of continuous motion (it is never a static stretch)."""
    n = max(1, int((b - a) / step))
    return {a + (b - a) * k / n for k in range(n + 1)}


def motion_intervals(shot):
    """[(start, end)] seconds (shot-relative) during which a template moves something."""
    d = shot["duration_seconds"]
    a = shot.get("animation") or {}
    t = shot.get("transition") or "HOLD"
    out = []
    if a.get("camera_move") or any(e.get("drift") for e in (shot.get("graphic") or {}).get("elements", [])):
        out.append((0.0, d))                                    # push-in, slow photo drift
    if t == "EXPLODED_VIEW":
        h0, h1 = a.get("hold_start_seconds", 0.0), a.get("hold_end_seconds", 0.0)
        ret, hold = a.get("return_seconds", 0.0), a.get("hold_seconds", 0.0)
        out += [(h0, max(h0, d - h1 - ret - hold)), (d - h1 - ret, d - h1)]
    elif t == "REPLACE_PARTS":
        out.append((a.get("hold_start_seconds", 0.0), d - a.get("hold_end_seconds", 0.0)))
    intro = a.get("intro")
    if isinstance(intro, dict) and intro.get("seconds"):
        out.append((0.0, float(intro["seconds"])))
    h = a.get("highlight")
    if isinstance(h, dict) and "start_seconds" in h:
        r0 = h["start_seconds"]
        r1 = r0 + h.get("rise_seconds", 0.0)
        f0 = r1 + h.get("hold_seconds", 0.0)
        out += [(r0, r1), (f0, f0 + h.get("fall_seconds", 0.0))]
    return [(max(0.0, x), min(d, y)) for x, y in out if y > x]


def shot_events(shot):
    """Seconds (shot-relative) at which something visibly changes inside a shot: template motion,
    highlights, annotation and card element fades (appear/disappear)."""
    d = shot["duration_seconds"]
    ev = {0.0}
    for a, b in motion_intervals(shot):
        ev |= _moving(a, b)
    for a in (shot.get("annotations") or {}).get("items", []):
        ev |= {a.get("appear", 0.0), min(d, a.get("disappear", d))}
    for e in (shot.get("graphic") or {}).get("elements", []):
        ev.add(e.get("appear", 0.0))
        if e.get("disappear") is not None:
            ev.add(e["disappear"])
    return sorted(x for x in ev if 0.0 <= x <= d)


def _image_elements(story):
    for s in story["shots"]:
        for e in (s.get("graphic") or {}).get("elements", []):
            if e.get("kind") in EXTERNAL_KINDS:
                yield s["id"], e


def manifest(p, preset="review"):
    p = Path(p)
    doc, timing = load(p), _read(p / "script/timing.json")
    story = _read(p / "storyboard/storyboard.json")
    narration = _read(p / "script/narration.json")
    if not (doc and timing and story and narration):
        raise ValueError("chapters, script/timing.json, storyboard and narration are required (run build-shots)")
    if "shots" not in timing:
        raise ValueError("script/timing.json has no scheduled shots yet (run build-shots)")
    errors = validate(doc, narration, _read(p / "script/visual_beats.json"))
    ranges, rerr = shot_ranges(doc, timing)
    errors += rerr
    fps = timing["fps"]
    shots = {s["id"]: s for s in story["shots"]}
    beats = {b["id"]: b for b in narration["beats"]}
    src = _read(p / "research/sources.json") or {}
    claims = {c["id"]: c for c in src.get("claims", [])}
    sources = {x["id"]: x for x in src.get("sources", [])}
    assets = {a["id"]: a for a in (_read(p / "assets/manifest.json") or {}).get("assets", [])}
    images = {}
    for sid, e in _image_elements(story):
        images.setdefault(sid, set()).add(e["asset"])
    out = []
    for c in doc["chapters"]:
        r = ranges.get(c["id"])
        if not r:
            continue
        kinds = [visual_kind(shots[s]) for s in r["shots"]]
        sentences = [t for b in c["beat_ids"] for t in beats[b]["sentences"]]
        rendered = sum(len(list((p / "renders" / preset / s).glob("frame_*.png"))) for s in r["shots"])
        out.append({"id": c["id"], "title": c["title"], "purpose": c.get("purpose"), "beats": c["beat_ids"],
                    "shots": r["shots"], "start_frame": r["start_frame"], "frames": r["frames"],
                    "start_seconds": round(r["start_frame"] / fps, 3), "duration_seconds": round(r["frames"] / fps, 3),
                    "sentences": len(sentences), "words": sum(len(t.split()) for t in sentences),
                    "claims": sorted({x for b in c["beat_ids"] for x in beats[b].get("claim_ids", [])}),
                    "visual_kinds": {k: kinds.count(k) for k in sorted(set(kinds))},
                    "external_assets": sorted({a for s in r["shots"] for a in images.get(s, ())}),
                    "evidence": chapter_evidence(c, beats, claims, sources, narration, shots, r["shots"], assets),
                    "render": {"preset": preset, "frames_on_disk": rendered, "complete": rendered == r["frames"]}})
    return {"schema": "chapter_manifest/1", "project": p.name, "fps": fps, "total_frames": timing["total_frames"],
            "total_seconds": round(timing["total_frames"] / fps, 3), "chapters": out, "errors": errors,
            "timing_sha256": hashlib.sha256((p / "script/timing.json").read_bytes()).hexdigest()}


def chapter_evidence(chapter, beats, claims, sources, narration, shots, shot_ids, assets):
    """M7 chapter-level evidence check: claims used and their status, sources, statements without a
    claim (fact beats only), narration revision, visual assumptions and how historical the visuals are."""
    used = sorted({x for b in chapter["beat_ids"] for x in beats[b].get("claim_ids", [])})
    unsupported = [f"{b}" for b in chapter["beat_ids"] if beats[b].get("kind") == "fact" and not beats[b].get("claim_ids")]
    missing = [x for x in used if x not in claims]
    statuses = sorted({claims[x].get("review_status") for x in used if x in claims})
    notes = sorted({a.get("text") for s in shot_ids for a in (shots[s].get("annotations") or {}).get("items", [])
                    if a.get("type") in ("NOTE", "TAG") and a.get("text")})
    photos = sorted({e.get("asset") for s in shot_ids for e in (shots[s].get("graphic") or {}).get("elements", [])
                     if e.get("kind") == "image"})
    has_3d = any(shots[s].get("visual_type") != "MOTION_GRAPHICS" for s in shot_ids)
    has_2d = any(shots[s].get("visual_type") == "MOTION_GRAPHICS" and not
                 any(e.get("kind") == "image" for e in (shots[s].get("graphic") or {}).get("elements", []))
                 for s in shot_ids)
    accuracy = [k for k, on in (("illustrative 3D archetypes (not replicas)", has_3d),
                                ("self-made conceptual/schematic graphics", has_2d),
                                ("archival photographs of the named bridges (public domain)", bool(photos))) if on]
    editorial = "EDITORIALLY_APPROVED" if used and statuses == ["EDITORIALLY_APPROVED"] else \
        ("NO_CLAIMS (framing only)" if not used else "PENDING_EDITORIAL_REVIEW")
    return {"claims_used": used, "claim_statuses": statuses, "missing_claims": missing,
            "sources": sorted({sid for x in used if x in claims for sid in claims[x]["source_ids"]}),
            "sources_known": all(sid in sources for x in used if x in claims for sid in claims[x]["source_ids"]),
            "unsupported_fact_beats": unsupported,
            "narration_revision": (narration.get("revision") or {}).get("version"),
            "visual_assumptions": notes + [f"image {a}: {assets.get(a, {}).get('license', 'NO RECORD')}" for a in photos],
            "historical_accuracy": accuracy, "editorial_status": editorial}


def _credits_text(p, story):
    """Every text of the film's credit card(s) and the publication description, lower-cased."""
    texts = [e.get("text", "") for s in story["shots"] for e in (s.get("graphic") or {}).get("elements", [])
             if e.get("kind") == "text"]
    desc = Path(p) / "review" / "YOUTUBE_DESCRIPTION.md"
    if desc.is_file():
        texts.append(desc.read_text(encoding="utf-8"))
    return " ".join(texts).lower()


def longform_qa(p, preset="review"):
    """[{check, status, detail}] for the whole film (no Blender): structure, silence, repeats,
    static stretches, variety, image licences and attribution, runtime."""
    p = Path(p)
    m = manifest(p, preset)
    story = _read(p / "storyboard/storyboard.json")
    timing = _read(p / "script/timing.json")
    narration = _read(p / "script/narration.json")
    assets = {a["id"]: a for a in (_read(p / "assets/manifest.json") or {}).get("assets", [])}
    rows = []

    def row(check, ok, detail, warn=False):
        rows.append({"check": check, "status": "PASS" if ok else ("WARN" if warn else "FAIL"), "detail": detail})

    row("chapters_structure", not m["errors"], "; ".join(m["errors"]) or
        f"{len(m['chapters'])} chapters cover every beat contiguously, in order")
    short = [f"{c['id']} {c['duration_seconds']:.1f}s" for c in m["chapters"] if c["duration_seconds"] < MIN_CHAPTER_SECONDS]
    row("chapter_durations", not short, ", ".join(short) or
        ", ".join(f"{c['id']} {c['duration_seconds']:.0f}s" for c in m["chapters"]))
    lo, hi = RUNTIME_RANGE
    row("runtime", lo <= m["total_seconds"] <= hi, f"{m['total_seconds'] / 60:.2f} min ({m['total_frames']} frames); "
        f"acceptable {lo / 60:.0f}-{hi / 60:.0f} min")

    ids = [s["id"] for s in story["shots"]]
    dup = sorted({i for i in ids if ids.count(i) > 1})
    row("no_duplicate_shots", not dup, ", ".join(dup) or f"{len(ids)} unique shots")
    said = [t.strip().lower() for b in narration["beats"] for t in b["sentences"]]
    rep = sorted({t for t in said if said.count(t) > 1})
    row("no_repeated_sentences", not rep, "; ".join(rep) or f"{len(said)} sentences, none repeated verbatim",
        warn=True)

    tbeats = {b["id"]: b for b in timing["beats"]}
    lost = [f"{b['id']}.s{i}" for b in narration["beats"] for i, t in enumerate(b["sentences"])
            if b["id"] not in tbeats or i >= len(tbeats[b["id"]]["sentences"])
            or tbeats[b["id"]]["sentences"][i]["text"] != t]
    lost += [b for b in tbeats if b not in {x["id"] for x in narration["beats"]}]
    row("narration_sentences_complete", not lost, ", ".join(lost[:8]) or
        f"{len(said)} sentences scheduled, same text and order as narration.json")
    by_start = sorted(timing["beats"], key=lambda b: b["start_seconds"])
    overlap = [f"{a['id']}/{b['id']}" for a, b in zip(by_start, by_start[1:])
               if a["start_seconds"] + a["duration"] > b["start_seconds"] + 1e-6]
    row("audio_no_overlap", not overlap, ", ".join(overlap) or "no two beats' speech overlaps")
    spans = sorted((b["start_seconds"], b["start_seconds"] + b["duration"], b["id"]) for b in timing["beats"])
    every = [(b0, b1, round(s1 - e0, 2)) for (_, e0, b0), (s1, _, b1) in zip(spans, spans[1:])]
    gaps = [g for g in every if g[2] > SILENCE_REPORT]
    worst = max([g[2] for g in every] or [0.0])
    end_gap = round(m["total_seconds"] - spans[-1][1], 2)
    row("narration_silences", worst <= MAX_SILENCE and end_gap <= MAX_SILENCE,
        f"longest gap {worst:.2f}s (limit {MAX_SILENCE}s), after the last line {end_gap:.2f}s"
        + (": " + ", ".join(f"{a}->{b} {g}s" for a, b, g in gaps) if gaps else ""))

    events, t0 = [], 0.0
    for s in story["shots"]:
        events += [t0 + x for x in shot_events(s)]
        t0 += s["duration_seconds"]
    events = sorted(set(round(e, 3) for e in events) | {round(t0, 3)})
    longest = max(((b - a), a) for a, b in zip(events, events[1:]))
    row("no_static_stretches", longest[0] <= MAX_STATIC,
        f"longest stretch without a visual change {longest[0]:.1f}s at {longest[1]:.1f}s (limit {MAX_STATIC}s)")

    kinds = [visual_kind(s) for s in story["shots"]]
    run, best, at = 1, 1, kinds[0] if kinds else None
    for a, b in zip(kinds, kinds[1:]):
        run = run + 1 if a == b else 1
        if run > best:
            best, at = run, b
    row("visual_variety", best <= MAX_SAME_KIND_RUN,
        f"longest run of one visual kind: {best} x {at} (limit {MAX_SAME_KIND_RUN}); "
        + ", ".join(f"{k} {kinds.count(k)}" for k in sorted(set(kinds))))
    def signature(sh):
        return (sh.get("visual_type"), sh.get("transition"), sh.get("from_state"), sh.get("to_state"), sh.get("camera"),
                json.dumps((sh.get("animation") or {}).get("camera_move"), sort_keys=True),
                json.dumps(sh.get("graphic"), sort_keys=True),
                tuple(sorted(a.get("id", "") for a in (sh.get("annotations") or {}).get("items", []))))
    same = [f"{a['id']}->{b['id']}" for a, b in zip(story["shots"], story["shots"][1:]) if signature(a) == signature(b)]
    row("no_repeated_visuals", not same, ", ".join(same) or "no two consecutive shots show the same picture")
    shots_by_id = {s["id"]: s for s in story["shots"]}
    untitled = []
    for k, c in enumerate(m["chapters"][1:], 2):
        first = shots_by_id[c["shots"][0]]
        texts = [a.get("text", "") for a in (first.get("annotations") or {}).get("items", [])] + \
            [e.get("text", "") for e in (first.get("graphic") or {}).get("elements", [])]
        if not any(t.startswith(f"{k} \u00b7") for t in texts):
            untitled.append(c["id"])
    row("chapter_openings", not untitled, ("chapters opening without a numbered title: " + ", ".join(untitled))
        if untitled else f"chapters 2-{len(m['chapters'])} open with a numbered title on their first shot")
    plan = _read(p / "storyboard/visual_plan.json") or {}
    verdicts = [r for r in (plan.get("consistency") or {}).get("rows", [])]
    contra = [f"{r['beat_id']}.s{r['sentence']} {r['rule']}" for r in verdicts if r["verdict"] == "CONTRADICTION"]
    unsure = [f"{r['beat_id']}.s{r['sentence']} {r['rule']}" for r in verdicts if r["verdict"] == "UNCERTAIN"]
    failed = [f"{a['id']}" for c in plan.get("coverage", []) for a in (c.get("annotations") or [])
              if a.get("status") not in ("PLACED", None)]
    row("annotations_consistent", not contra and not failed,
        "; ".join(contra + [f"annotation {x} not placed" for x in failed]) or
        f"narration/visual consistency: no contradiction; {len(unsure)} UNCERTAIN for the reviewer"
        + (f" ({', '.join(unsure)})" if unsure else "") + "; every annotation placed")
    try:
        from tools import render_cache
        cache = render_cache.report(p, preset, story["shots"])
        stale = [r["shot"] for r in cache if r["status"] != "CACHED"]
        row("render_cache_current", not stale, (f"{len(stale)}/{len(cache)} shots not rendered or stale at {preset}: "
                                                 + ", ".join(stale[:6])) if stale else
            f"all {len(cache)} shots rendered at {preset} with current cache keys", warn=True)
    except Exception as e:   # noqa: BLE001 - the report is informative; staleness of media is gated by G4/G5
        row("render_cache_current", False, f"cache report unavailable: {e}", warn=True)
    flat = [c["id"] for c in m["chapters"] if len(c["visual_kinds"]) < 2 and len(c["shots"]) > 1]
    row("chapter_variety", not flat, ", ".join(flat) or "every multi-shot chapter mixes at least two visual kinds",
        warn=True)

    used = {}
    for sid, e in _image_elements(story):
        used.setdefault(e["asset"], []).append(sid)
    bad = []
    credits = _credits_text(p, story)
    for aid, sids in sorted(used.items()):
        a = assets.get(aid)
        if not a:
            bad.append(f"{aid}: not in assets/manifest.json")
            continue
        if a.get("status") != "approved" or not a.get("license"):
            bad.append(f"{aid}: status {a.get('status')}, licence {a.get('license')!r}")
        f = p / a.get("local_path", "")
        if not f.is_file():
            bad.append(f"{aid}: file {a.get('local_path')} missing")
        elif a.get("sha256") and hashlib.sha256(f.read_bytes()).hexdigest() != a["sha256"]:
            bad.append(f"{aid}: file hash differs from the rights record")
    row("image_licences", not bad, "; ".join(bad) or f"{len(used)} external images, all approved with matching files")
    missing = [aid for aid in sorted(used) if aid in assets
               and not (assets[aid].get("credit_keys") and all(k.lower() in credits for k in assets[aid]["credit_keys"]))]
    row("image_attribution", not missing, ("not credited on screen or in the description: " + ", ".join(missing))
        if missing else "every external image is credited (credit card or description)")
    return rows, m
