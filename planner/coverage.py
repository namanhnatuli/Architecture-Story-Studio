"""Visual coverage report: how well the planned visuals cover the narration, beat by beat
(M5.5: with target visibility, the visual repairs applied and the comparison layouts)."""
import json
from pathlib import Path


def _vis_rows(shots):
    return [dict(r, shot_id=s["shot_id"]) for s in shots for r in ((s.get("visibility") or {}).get("targets") or [])]


def rows(plan):
    out = []
    for c in plan["coverage"]:
        shots = [s for s in plan["shots"] if s["beat_id"] == c["beat_id"]]
        planned = round(sum(s["timing"]["duration_seconds"] for s in shots), 3)
        vis = _vis_rows(shots)
        concepts = sorted({r["concept"] for r in vis})
        readable = {k: any(r["ok"] for r in vis if r["concept"] == k) for k in concepts}
        out.append({**{k: c.get(k) for k in ("beat_id", "visual_intent", "strategy", "status", "evidence_status",
                                              "expected_seconds", "timing_source", "issues", "explanation")},
                    "assets": c["assets"], "semantic_targets": c["semantic_targets"], "templates": c["templates"],
                    "shot_ids": c["shot_ids"], "planned_seconds": planned,
                    "readable": readable, "visual_repairs": c.get("visual_repairs", []),
                    "composition": [dict(s["composition"], shot_id=s["shot_id"]) for s in shots if s.get("composition")],
                    "visibility": [{k: r.get(k) for k in ("shot_id", "concept", "label", "frame", "visible_share",
                                                           "core_area", "visible_area", "ok", "problems",
                                                           "verification")} for r in vis]})
    return out


def _fmt_vis(r):
    if not r["readable"]:
        return "—"
    return "<br>".join(f"{k}: {'reads' if ok else '**NOT READABLE**'}" for k, ok in sorted(r["readable"].items()))


def write(plan, project_dir):
    p = Path(project_dir) / "qa"
    p.mkdir(parents=True, exist_ok=True)
    data = rows(plan)
    (p / "visual_coverage.json").write_text(json.dumps({"project_id": plan["project_id"], "executable": plan["executable"],
                                                        "visibility_summary": plan.get("visibility_summary"),
                                                        "beats": data}, indent=2, ensure_ascii=False) + "\n")
    counts = {}
    for r in data:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
    vs = plan.get("visibility_summary") or {}
    lines = [f"# Visual coverage: {plan.get('title') or plan['project_id']}", "",
             f"- Planner {plan['planner_version']}, timing **{plan['timing_mode']}** "
             f"({'estimates, not measured speech' if plan['timing_mode'] == 'PROVISIONAL' else 'measured narration windows'}), "
             f"{len(plan['shots'])} shots, {plan['duration_seconds']:.2f} s.",
             f"- Executable: **{plan['executable']}** · " + ", ".join(f"{k} {v}" for k, v in sorted(counts.items())),
             f"- Publication: {plan['publication']['restriction']} — {plan['publication'].get('reason', '')}",
             f"- Visibility (offline Level 1 estimate): {vs.get('shots_assessed', 0)} shots, {vs.get('rows_passing', 0)}/"
             f"{vs.get('target_rows', 0)} target rows read, issues {vs.get('issues_detected', 0)}, auto-repaired "
             f"{vs.get('auto_repaired', 0)}, manual review {vs.get('manual_review', 0)}, uncertain "
             f"{vs.get('uncertain_rows', 0)} (Blender check: `verify-visibility`).", "",
             "| Beat | Intent | Strategy | Assets | Semantic targets | Templates (shots) | Expected / planned s | Evidence | Readable | Coverage | Issues |",
             "|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in data:
        assets = "<br>".join(f"{a['concept']}: {a['status']}" + (f" → `{a['asset_id']}`" if a.get("asset_id") else "")
                             for a in r["assets"]) or "—"
        tmpl = ", ".join(f"{t} ({s})" for t, s in zip(r["templates"], r["shot_ids"])) or "—"
        issues = "<br>".join(r["issues"]) or "—"
        lines.append(f"| {r['beat_id']} | {r['visual_intent']} | {r['strategy'] or '—'} | {assets} | "
                     f"{', '.join(r['semantic_targets']) or '—'} | {tmpl} | {r['expected_seconds']:.2f} / "
                     f"{r['planned_seconds']:.2f} | {r['evidence_status']} | {_fmt_vis(r)} | **{r['status']}** | {issues} |")
    lines += ["", "## Planner decisions", ""]
    for r in data:
        lines.append(f"- **{r['beat_id']}**: " + " · ".join(r["explanation"]))
    repairs = [x for r in data for x in r["visual_repairs"]]
    lines += ["", "## Visual repairs (offline, before rendering)", ""]
    if not repairs:
        lines.append("- none needed")
    for x in repairs:
        tried = "; ".join(f"{e['remedy']} {e['result']}" + (f" ({e['detail']})" if e.get("detail") else "")
                          for e in x["evaluated"])
        before = x["before"]
        after = x.get("after")
        lines.append(f"- **{x['beat_id']} {x['shot_id']} {x['concept']}** at {x['frame']}: {', '.join(x['problems'])} "
                     f"(share {before['visible_share']:.2f}, core {before['core_area'] * 100:.2f}%) → "
                     + (f"**{x['chosen']}** (share {after['visible_share']:.2f}, core {after['core_area'] * 100:.2f}%)"
                        if x["chosen"] else "**unresolved**") + f". Evaluated: {tried}")
    comps = [x for r in data for x in r["composition"]]
    if comps:
        lines += ["", "## Comparison composition", ""]
        for x in comps:
            m = x.get("metrics") or {}
            lines.append(f"- {x['shot_id']}: {x['layout']}" + (f" gap {x['gap_ratio']}" if "gap_ratio" in x else "")
                         + f", purpose {x['purpose']}, scale {x['scale']}"
                         + (f", smallest member {m['min_detail_px']:.1f} px, smallest model {m['min_width'] * 100:.0f}% "
                            f"of the frame width" if m else ""))
            for c in x.get("candidates", []):
                lines.append(f"  - candidate {c['layout']} gap {c['gap_ratio']}: "
                             + ("readable" if c["ok"] else "; ".join(c["problems"])))
    if plan.get("warnings"):
        lines += ["", "## Warnings", ""] + [f"- {w}" for w in plan["warnings"]]
    (p / "VISUAL_COVERAGE.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return p / "VISUAL_COVERAGE.md"
