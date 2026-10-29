"""Visual-planning evaluation suite (M5.5; M6 adds annotation and consistency checks).

A small, explicit dataset (evaluation/visual_planning/cases.json) of positive, negative,
ambiguous and missing-capability cases over the bridge and roof projects. Each case edits a
temporary copy of a project, runs the unchanged planner and checks expectations, each tied
to one evaluation dimension. The planner never reads this dataset; a high score on it shows
that these cases behave as specified - it does not demonstrate general language understanding.
"""
import copy
import json
import shutil
import tempfile
from pathlib import Path

from planner import planner as pl

ROOT = Path(__file__).resolve().parent.parent
DIMENSIONS = ("narrative_relevance", "asset_selection", "target_selection", "animation_suitability",
              "camera_readability", "target_visibility", "timing_feasibility", "evidence_compatibility",
              "visual_continuity", "cross_family_reuse")
KINDS = ("positive", "negative", "ambiguous", "missing_capability")
CHECK_DIMENSION = {"strategy": "narrative_relevance", "assets": "asset_selection", "target_roles": "target_selection",
                   "templates": "animation_suitability", "camera": "camera_readability",
                   "composition": "camera_readability", "readable": "target_visibility", "repair": "target_visibility",
                   "evidence": "evidence_compatibility", "cuts": "visual_continuity", "one_camera": "visual_continuity",
                   "annotations": "target_selection", "consistency": "narrative_relevance"}   # M6


def _copy_project(src, tmp):
    dst = Path(tmp) / Path(src).name
    for sub in ("script", "research"):
        if (Path(src) / sub).is_dir():
            shutil.copytree(Path(src) / sub, dst / sub)
    shutil.copy(Path(src) / "project.json", dst / "project.json")
    return dst


def _apply(dst, case):
    doc_path = dst / "script/visual_beats.json"
    doc = json.loads(doc_path.read_text())
    if case.get("keep_beats"):
        doc["beats"] = [b for b in doc["beats"] if b["beat_id"] in case["keep_beats"]]
    for op in case.get("edits", []):
        beat = next(b for b in doc["beats"] if b["beat_id"] == op["beat"])
        for k, v in op.get("set", {}).items():
            beat[k] = copy.deepcopy(v)
        for k, v in op.get("append", {}).items():
            beat.setdefault(k, []).append(v)
    doc_path.write_text(json.dumps(doc))
    if case.get("claims"):
        src = dst / "research/sources.json"
        s = json.loads(src.read_text())
        for c in s["claims"]:
            c.update(case["claims"].get(c["id"], {}))
        src.write_text(json.dumps(s))


def _checks(case, plan):
    """[(dimension, name, ok, detail)] for one planned case."""
    e = case["expect"]
    bid = case["beat"]
    cov = next(c for c in plan["coverage"] if c["beat_id"] == bid)
    shots = [s for s in plan["shots"] if s["beat_id"] == bid]
    out = []

    def add(key, ok, detail, dim=None):
        out.append((dim or CHECK_DIMENSION.get(key, case.get("status_dimension", "narrative_relevance")), key, bool(ok),
                    detail))
    if "status" in e:
        add("status", cov["status"] == e["status"], f"status {cov['status']} (want {e['status']})",
            case.get("status_dimension", "narrative_relevance"))
    if "strategy" in e:
        want = e["strategy"] if isinstance(e["strategy"], list) else [e["strategy"]]
        add("strategy", cov["strategy"] in want, f"strategy {cov['strategy']} (want {want})")
    for concept, (status, asset) in e.get("assets", {}).items():
        got = next((a for a in cov["assets"] if a["concept"] == concept), {})
        add("assets", got.get("status") == status and (asset is None or got.get("asset_id") == asset),
            f"{concept}: {got.get('status')} {got.get('asset_id')} (want {status} {asset})")
    for concept, roles in e.get("target_roles", {}).items():
        got = sorted({r for s in shots for t in s["semantic_targets"] if t["concept"] == concept for r in t["roles"]})
        add("target_roles", got == sorted(roles), f"{concept} roles {got} (want {roles})")
    if "templates" in e:
        got = [s["template"] for s in shots]
        add("templates", got == e["templates"], f"templates {got} (want {e['templates']})")
    if "camera" in e:
        c = e["camera"]
        shot = shots[c.get("shot", -1)] if shots else None
        ok = shot is not None and all((k != "focus_count" or len(shot["shot"].get("camera_focus") or []) == v) and
                                      (k != "preset" or shot["camera"]["preset"] == v) and
                                      (k != "mode" or shot["camera"]["mode"] == v) for k, v in c.items() if k != "shot")
        add("camera", ok, f"camera {shot['camera'] if shot else None} (want {c})")
    if "composition" in e:
        comp = [s.get("composition") or {} for s in shots]
        ok = bool(comp) and all(all(x.get(k) == v for k, v in e["composition"].items()) for x in comp)
        add("composition", ok, f"composition {[{k: x.get(k) for k in e['composition']} for x in comp]}")
    if "one_camera" in e:
        add("one_camera", len({s["camera"]["group"] for s in shots}) == 1, "one locked camera for the beat's shots")
    if "cuts" in e:
        got = [s["cut_from_previous"] for s in shots]
        add("cuts", got == e["cuts"], f"cuts {got} (want {e['cuts']})")
    if "readable" in e:
        rows = [r for s in shots for r in ((s.get("visibility") or {}).get("targets") or [])]
        concepts = {r["concept"] for r in rows}
        ok_all = bool(rows) and all(any(r["ok"] for r in rows if r["concept"] == k) for k in concepts)
        add("readable", ok_all == e["readable"], f"every concept reads: {ok_all} (want {e['readable']})")
    if "repair" in e:
        got = [r["chosen"] for r in cov.get("visual_repairs", []) if r["chosen"]]
        add("repair", (e["repair"] in got) if e["repair"] else not got, f"repairs {got} (want {e['repair']})")
    if "evidence" in e:
        add("evidence", cov.get("evidence_status") == e["evidence"], f"evidence {cov.get('evidence_status')}")
    for aid, status in e.get("annotations", {}).items():   # M6: PLACED / FAILED per annotation
        got = next((r["status"] for r in cov.get("annotations", []) if r["id"] == aid), None)
        add("annotations", got == status, f"annotation {aid}: {got} (want {status})")
    for rule, verdict in e.get("consistency", {}).items():   # M6: narration/visual rule verdicts of the beat
        got = [r["verdict"] for r in (plan.get("consistency") or {}).get("rows", [])
               if r["beat_id"] == bid and r["rule"] == rule]
        add("consistency", verdict in got, f"{rule}: {got} (want {verdict})")
    text = " ".join(cov["issues"] + cov["explanation"] + plan.get("warnings", []))
    for needle in e.get("mentions", []):
        add("mentions", needle in text, f"report mentions {needle!r}", case.get("status_dimension", "narrative_relevance"))
    return out


def run(cases_path=None, root=ROOT):
    data = json.loads(Path(cases_path or root / "evaluation/visual_planning/cases.json").read_text())
    results = []
    for case in data["cases"]:
        with tempfile.TemporaryDirectory() as tmp:
            dst = _copy_project(root / case["project"], tmp)
            _apply(dst, case)
            try:
                plan = pl.plan_project(dst, root)
                checks = _checks(case, plan)
                error = None
            except pl.PlanningError as e:
                checks, error = [], "; ".join(e.errors)
        if case["expect"].get("planning_error"):
            checks = [(case.get("status_dimension", "narrative_relevance"), "planning_error",
                       bool(error and case["expect"]["planning_error"] in error), f"planning error: {error}")]
        elif error:
            checks = [("narrative_relevance", "planned", False, f"planning failed: {error}")]
        results.append({"id": case["id"], "kind": case["kind"], "family": case["family"], "title": case["title"],
                        "checks": [{"dimension": d, "check": n, "ok": o, "detail": t} for d, n, o, t in checks],
                        "ok": all(o for _, _, o, _ in checks) and bool(checks)})
    return summarize(results, data)


def summarize(results, data):
    dims = {d: [0, 0] for d in DIMENSIONS}
    for r in results:
        for c in r["checks"]:
            dims[c["dimension"]][1] += 1
            dims[c["dimension"]][0] += c["ok"]
    fams = sorted({r["family"] for r in results})
    by_family = {f: [sum(r["ok"] for r in results if r["family"] == f), sum(1 for r in results if r["family"] == f)]
                 for f in fams}
    # Cross-family reuse: the same planner and checks hold for every family represented.
    dims["cross_family_reuse"] = [sum(1 for f in fams if by_family[f][0] == by_family[f][1]), len(fams)]
    by_kind = {k: [sum(r["ok"] for r in results if r["kind"] == k), sum(1 for r in results if r["kind"] == k)]
               for k in KINDS}
    return {"dataset": data.get("note"), "cases": len(results), "passed": sum(r["ok"] for r in results),
            "dimensions": {d: {"passed": p, "checks": n} for d, (p, n) in dims.items()},
            "by_kind": {k: {"passed": p, "cases": n} for k, (p, n) in by_kind.items()},
            "by_family": {f: {"passed": p, "cases": n} for f, (p, n) in by_family.items()},
            "results": results}


def write_report(summary, out_dir):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "results.json").write_text(json.dumps(summary, indent=1) + "\n")
    lines = ["# Visual-planning evaluation (M5.5)", "",
             f"{summary['passed']}/{summary['cases']} cases pass. Small curated dataset: it checks that these cases "
             "behave as specified; it is not evidence of unrestricted natural-language understanding.", "",
             "| Dimension | Checks passed |", "|---|---|"]
    for d, v in summary["dimensions"].items():
        lines.append(f"| {d} | {v['passed']}/{v['checks']} |")
    lines += ["", "| Kind | Cases passed |", "|---|---|"]
    lines += [f"| {k} | {v['passed']}/{v['cases']} |" for k, v in summary["by_kind"].items()]
    lines += ["", "| Family | Cases passed |", "|---|---|"]
    lines += [f"| {k} | {v['passed']}/{v['cases']} |" for k, v in summary["by_family"].items()]
    lines += ["", "## Cases", ""]
    for r in summary["results"]:
        lines.append(f"- **{r['id']}** ({r['kind']}, {r['family']}) {r['title']}: **{'PASS' if r['ok'] else 'FAIL'}**")
        for c in r["checks"]:
            lines.append(f"  - {'ok' if c['ok'] else 'FAIL'} [{c['dimension']}] {c['detail']}")
    (out / "RESULTS.md").write_text("\n".join(lines) + "\n")
    return out / "RESULTS.md"
