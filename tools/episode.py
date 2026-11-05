#!/usr/bin/env python3
"""New-documentary intake and stage tracking (M7; stdlib only).

  python3 tools/episode.py new --topic "Why traditional Japanese houses use different roof forms"
  python3 tools/episode.py status --project <slug>
  python3 tools/episode.py next --project <slug>

`new` scaffolds projects/<slug>/ with the Studio defaults (English, 16:9, 24 fps, 8-15 min with a
10-12 min target, the established visual style, Kokoro narration, research first, internal review
before publication). `status` derives every production stage from the files that exist, so a
session can stop at any point and resume; `next` says which stage is next, WHO does it (the
Claude Code agent, the deterministic CLI, or the OWNER) and the commands that the playbook
(docs/production/NEW_DOCUMENTARY_PLAYBOOK.md) uses for it.

This tool does NOT research, write or plan: open-ended work is the agent's (prompts/
NEW_DOCUMENTARY_AUTOPILOT.md). It never approves anything; owner decisions are recorded by the
agent only when the owner states them.
"""
import argparse
import json
import re
import sys
import unicodedata
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULTS_PATH = ROOT / "config" / "production_defaults.json"
SUBDIRS = ("research", "script", "storyboard", "chapters", "assets/external", "audio", "scenes", "renders",
           "output", "qa", "review")
REVIEW_FILES = ("review/EDITORIAL_APPROVAL_PACKAGE.md", "review/PRONUNCIATION_REVIEW.md", "review/RIGHTS_PROVENANCE.md",
                "review/YOUTUBE_DESCRIPTION.md", "qa/EDITORIAL_REVIEW_TIMECODED.md")

# (stage, who, what) in production order; detection is in stage_status()
STAGES = [
    ("TOPIC", "CLI", "episode.py new"),
    ("RESEARCH", "AGENT", "sources + verbatim-checked claims in research/sources.json (+ RESEARCH_REPORT.md)"),
    ("SCRIPT", "AGENT", "script/story.py -> narration.json, visual_beats.json, chapters.json"),
    ("CLAIM_SOURCE_VERIFICATION", "CLI", "every narrated claim SOURCE_VERIFIED; validate"),
    ("TTS", "CLI", "narrate --purpose publication; asr-check; align"),
    ("AUDIO_LOCK", "CLI", "lock-audio"),
    ("VISUAL_PLAN", "CLI", "plan-visuals; validate-plan; build-shots; chapters; check-blender"),
    ("CHAPTER_PRODUCTION", "CLI", "chapter --chapter Cn --preset review (one chapter first)"),
    ("ROUGH_CUT", "CLI", "preview --preset preview; assemble --preset preview"),
    ("EDITORIAL_QA", "AGENT", "watch the rough cut, fix, write qa/EDITORIAL_REVIEW_TIMECODED.md"),
    ("INTERNAL_REVIEW", "CLI", "preview/assemble --preset review or internal_1080p; longform_reports.py; gates"),
    ("OWNER_APPROVAL", "OWNER", "claims, voice for this project, pronunciation, disclosure -> review/OWNER_APPROVALS.json"),
    ("PUBLICATION_CANDIDATE", "AGENT", "record approvals; profile PUBLICATION_CANDIDATE + metadata; final-gate"),
    ("FINAL_RENDER", "CLI", "chapter --preset final_4k --release-frames (each); final-assemble; gates"),
    ("DELIVERY", "AGENT", "checksums, reports, docs, commit (never upload, merge or push)"),
]


def read(path):
    path = Path(path)
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else None


def defaults():
    return read(DEFAULTS_PATH)


def slugify(topic, max_words=7):
    text = unicodedata.normalize("NFKD", topic).encode("ascii", "ignore").decode().lower()
    words = [w for w in re.findall(r"[a-z0-9]+", text) if w not in ("a", "an", "the", "of", "and", "about")]
    slug = "-".join(words[:max_words])
    if not slug:
        raise SystemExit("the topic gives no usable slug; pass --slug")
    return slug


def scaffold(topic, slug=None, projects_root=None, today=None):
    """Create projects/<slug>/ for a topic. Refuses to touch an existing project."""
    d = defaults()
    slug = slug or slugify(topic)
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{1,60}", slug):
        raise SystemExit(f"invalid slug {slug!r}")
    root = Path(projects_root or ROOT / "projects")
    p = root / slug
    if p.exists():
        raise SystemExit(f"{p} exists; resume it with `episode.py status --project {slug}`")
    for sub in SUBDIRS:
        (p / sub).mkdir(parents=True, exist_ok=True)
    for keep in ("renders", "output"):
        (p / keep / ".gitkeep").write_text("")
    day = (today or date.today()).isoformat()
    project = {"slug": slug, "title": topic.strip().rstrip("."), "mode": "documentary", "language": d["language"],
               "fps": d["fps"], "render_preset": "review", "factual_review": "pending",
               "production_profile": "NARRATED_INTERNAL_REVIEW", "chapters": "script/chapters.json",
               "review_label": "FINAL_INTERNAL_REVIEW"}
    (p / "project.json").write_text(json.dumps(project, indent=2) + "\n")
    episode = {"schema": "episode/1", "topic": topic, "created": day, "defaults": d,
               "notes": "Stages are derived from files by `episode.py status`; this file only records the brief. "
                        "Procedure: docs/production/NEW_DOCUMENTARY_PLAYBOOK.md."}
    (p / "episode.json").write_text(json.dumps(episode, indent=2, ensure_ascii=False) + "\n")
    (p / "research" / "sources.json").write_text(json.dumps(
        {"note": f"Evidence registry for: {topic}. Fill by research; nothing is approved here.",
         "sources": [], "claims": []}, indent=2) + "\n")
    (p / "assets" / "manifest.json").write_text(json.dumps(
        {"project": slug, "assets": [{"id": "AST_001", "origin": "procedural", "license": "generated_in_project",
                                      "status": "approved", "note": "procedural Studio assets (asset_library)"}]},
        indent=2) + "\n")
    brief = ROOT / "docs" / "production" / "templates" / "RESEARCH_BRIEF.md"
    (p / "research" / "RESEARCH_BRIEF.md").write_text(
        brief.read_text(encoding="utf-8").replace("{{TOPIC}}", topic).replace("{{DATE}}", day))
    checklist = ROOT / "docs" / "production" / "templates" / "FINAL_APPROVAL_CHECKLIST.md"
    (p / "review" / "FINAL_APPROVAL_CHECKLIST.md").write_text(checklist.read_text(encoding="utf-8").replace("{{TOPIC}}", topic))
    return p


def _all_claims_ok(p, statuses=("SOURCE_VERIFIED", "EDITORIALLY_APPROVED")):
    src, narration = read(p / "research/sources.json") or {}, read(p / "script/narration.json") or {}
    claims = {c["id"]: c.get("review_status") for c in src.get("claims", [])}
    used = {c for b in narration.get("beats", []) for c in b.get("claim_ids", [])}
    return bool(used) and all(claims.get(c) in statuses for c in used), sorted(c for c in used if claims.get(c) not in statuses)


def stage_status(p):
    """[(stage, status, detail)] with status DONE / TODO / BLOCKED / WAITING_FOR_OWNER, derived from files only."""
    p = Path(p)
    rows = []
    project = read(p / "project.json") or {}
    src = read(p / "research/sources.json") or {}
    narration = read(p / "script/narration.json")
    manifest = read(p / "audio/narration_manifest.json") or {}
    timing = read(p / "script/timing.json") or {}
    plan = read(p / "storyboard/visual_plan.json") or {}
    chapters = (read(p / "script/chapters.json") or {}).get("chapters", [])
    longform = read(p / "qa/longform_qa.json") or {}
    approvals = read(p / "review/OWNER_APPROVALS.json")

    def add(stage, ok, detail="", blocked=None, waiting=False):
        status = "DONE" if ok else ("BLOCKED" if blocked else "WAITING_FOR_OWNER" if waiting else "TODO")
        rows.append((stage, status, blocked or detail))

    add("TOPIC", (p / "episode.json").is_file() or (p / "project.json").is_file())
    verified = [c for c in src.get("claims", []) if c.get("review_status") in ("SOURCE_VERIFIED", "EDITORIALLY_APPROVED")]
    add("RESEARCH", bool(src.get("sources")) and bool(verified), f"{len(src.get('sources', []))} sources, {len(verified)} verified claims")
    script_ok = all((p / f).is_file() for f in ("script/narration.json", "script/visual_beats.json", "script/chapters.json"))
    add("SCRIPT", script_ok, f"{len(chapters)} chapters" if script_ok else "")
    ok, bad = _all_claims_ok(p) if narration else (False, [])
    add("CLAIM_SOURCE_VERIFICATION", ok, blocked=(f"claims not source-verified: {', '.join(bad[:6])}" if narration and bad else None))
    beats = {b["id"] for b in (narration or {}).get("beats", [])}
    tts_ok = bool(beats) and beats <= set(manifest.get("beats", {}))
    asr_ok = tts_ok and all((manifest["segments"].get(s["cache_key"], {}).get("asr") or {}).get("pass")
                            for b in beats for s in manifest["beats"][b]["sentences"])
    add("TTS", asr_ok, "narration generated and ASR-verified" if asr_ok else ("generated, ASR pending" if tts_ok else ""))
    add("AUDIO_LOCK", bool(timing.get("locked")), f"{timing.get('total_seconds', 0):.1f} s" if timing.get("locked") else "")
    add("VISUAL_PLAN", bool(plan.get("executable")) and (p / "storyboard/storyboard.json").is_file(),
        f"{len(plan.get('shots', []))} shots" if plan else "")
    done_chapters = [c["id"] for c in chapters
                     if any(not (read(f) or {"problems": [1]}).get("problems") for f in p.glob(f"qa/chapter_{c['id']}_*.json"))]
    add("CHAPTER_PRODUCTION", bool(chapters) and bool(done_chapters), f"{len(done_chapters)}/{len(chapters)} chapters produced")
    rough = [f.name for f in p.glob("qa/assembly_report*.json") if not (read(f) or {}).get("problems")]
    add("ROUGH_CUT", bool(rough), ", ".join(sorted(rough)))
    qa_ok = bool(longform) and not longform.get("failed") and (p / "qa/EDITORIAL_REVIEW_TIMECODED.md").is_file()
    add("EDITORIAL_QA", qa_ok)
    review_ok = all((p / f).is_file() for f in REVIEW_FILES) and any(
        "INTERNAL_REVIEW" in f.name or "documentary" in f.name for f in p.glob("output/*.mp4"))
    add("INTERNAL_REVIEW", review_ok, "review package + internal review video" if review_ok else "")
    from pipeline import gates
    g = gates.evaluate(p) if review_ok else None
    owner_ok = bool(approvals) and g is not None and all(
        g["gates"][k]["status"] == "PASS" for k in g["gates"] if k.startswith(("G1", "G2")))
    add("OWNER_APPROVAL", owner_ok, "", waiting=review_ok and not owner_ok)
    from tools.validator import validate_project
    final_errors = [e for e in validate_project(p, final=True)[0] if e.startswith("FINAL gate")] if owner_ok else ["-"]
    add("PUBLICATION_CANDIDATE", owner_ok and project.get("production_profile") == "PUBLICATION_CANDIDATE" and not final_errors,
        "; ".join(final_errors[:2]) if owner_ok else "")
    final = [f for f in p.glob("qa/assembly_report_final*.json") if not (read(f) or {}).get("problems")]
    add("FINAL_RENDER", bool(final), ", ".join(f.name for f in final))
    delivered = list(p.glob("output/*_FINAL_*.sha256"))
    add("DELIVERY", bool(final) and bool(delivered), ", ".join(f.name for f in delivered))
    return rows


def next_stage(rows):
    who = {s: (w, what) for s, w, what in STAGES}
    for stage, status, detail in rows:
        if status != "DONE":
            return {"stage": stage, "status": status, "who": who[stage][0], "do": who[stage][1], "detail": detail}
    return {"stage": None, "status": "COMPLETE", "who": None, "do": "nothing: the final package is with the owner (publishing is the owner's decision; the Studio never uploads)", "detail": ""}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    n = sub.add_parser("new")
    n.add_argument("--topic", required=True)
    n.add_argument("--slug")
    for name in ("status", "next"):
        s = sub.add_parser(name)
        s.add_argument("--project", required=True)
    for s in sub.choices.values():
        s.add_argument("--projects-root", help="default: projects/ in this repository")
    args = ap.parse_args(argv)
    root = Path(args.projects_root or ROOT / "projects")
    if args.cmd == "new":
        p = scaffold(args.topic, args.slug, root)
        print(f"CREATED {p}")
        print("Next: RESEARCH by the agent - follow prompts/NEW_DOCUMENTARY_AUTOPILOT.md")
        return 0
    p = root / args.project
    if not p.is_dir():
        raise SystemExit(f"no project {p}")
    rows = stage_status(p)
    if args.cmd == "status":
        for stage, status, detail in rows:
            print(f"{status:>18}  {stage:<26} {detail}")
    nxt = next_stage(rows)
    print(f"NEXT: {nxt['stage'] or '-'} ({nxt['status']}) by {nxt['who'] or '-'}: {nxt['do']}"
          + (f" [{nxt['detail']}]" if nxt["detail"] else ""))
    return 0


if __name__ == "__main__":
    sys.path.insert(0, str(ROOT))
    sys.exit(main())
