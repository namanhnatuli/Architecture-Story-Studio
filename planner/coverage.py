"""Visual coverage report: how well the planned visuals cover the narration, beat by beat."""
import json
from pathlib import Path


def rows(plan):
    out = []
    for c in plan["coverage"]:
        shots = [s for s in plan["shots"] if s["beat_id"] == c["beat_id"]]
        planned = round(sum(s["timing"]["duration_seconds"] for s in shots), 3)
        vis = [v for s in shots for v in s.get("visibility", []) if v.get("ok") is False]
        out.append({**{k: c.get(k) for k in ("beat_id", "visual_intent", "strategy", "status", "evidence_status",
                                              "expected_seconds", "timing_source", "issues", "explanation")},
                    "assets": c["assets"], "semantic_targets": c["semantic_targets"], "templates": c["templates"],
                    "shot_ids": c["shot_ids"], "planned_seconds": planned,
                    "visibility_issues": [f"{v['target']}: {v['detail']}" for v in vis]})
    return out


def write(plan, project_dir):
    p = Path(project_dir) / "qa"
    p.mkdir(parents=True, exist_ok=True)
    data = rows(plan)
    (p / "visual_coverage.json").write_text(json.dumps({"project_id": plan["project_id"], "executable": plan["executable"],
                                                        "beats": data}, indent=2, ensure_ascii=False) + "\n")
    counts = {}
    for r in data:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
    lines = [f"# Visual coverage: {plan.get('title') or plan['project_id']}", "",
             f"- Planner {plan['planner_version']}, timing **{plan['timing_mode']}** "
             f"({'estimates, not measured speech' if plan['timing_mode'] == 'PROVISIONAL' else 'measured narration windows'}), "
             f"{len(plan['shots'])} shots, {plan['duration_seconds']:.2f} s.",
             f"- Executable: **{plan['executable']}** · " + ", ".join(f"{k} {v}" for k, v in sorted(counts.items())),
             f"- Publication: {plan['publication']['restriction']} — {plan['publication'].get('reason', '')}", "",
             "| Beat | Intent | Strategy | Assets | Semantic targets | Templates (shots) | Expected / planned s | Evidence | Coverage | Issues |",
             "|---|---|---|---|---|---|---|---|---|---|"]
    for r in data:
        assets = "<br>".join(f"{a['concept']}: {a['status']}" + (f" → `{a['asset_id']}`" if a.get("asset_id") else "")
                             for a in r["assets"]) or "—"
        tmpl = ", ".join(f"{t} ({s})" for t, s in zip(r["templates"], r["shot_ids"])) or "—"
        issues = "<br>".join(r["issues"] + r["visibility_issues"]) or "—"
        lines.append(f"| {r['beat_id']} | {r['visual_intent']} | {r['strategy'] or '—'} | {assets} | "
                     f"{', '.join(r['semantic_targets']) or '—'} | {tmpl} | {r['expected_seconds']:.2f} / "
                     f"{r['planned_seconds']:.2f} | {r['evidence_status']} | **{r['status']}** | {issues} |")
    lines += ["", "## Planner decisions", ""]
    for r in data:
        lines.append(f"- **{r['beat_id']}**: " + " · ".join(r["explanation"]))
    if plan.get("warnings"):
        lines += ["", "## Warnings", ""] + [f"- {w}" for w in plan["warnings"]]
    (p / "VISUAL_COVERAGE.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return p / "VISUAL_COVERAGE.md"
