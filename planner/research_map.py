"""Research-to-visual mapping (M6): for every narrated sentence, the chain
sentence -> claim -> source (locator) -> asset -> components -> annotation -> timing -> QA.

Built from the plan, the claim ledger, the locked timing and the Blender QA report; nothing
is inferred that the files do not state. Written to qa/RESEARCH_VISUAL_MAP.{json,md}."""
import json
from pathlib import Path

from planner import timing as T


def _read(path):
    path = Path(path)
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else None


def build(project_dir):
    p = Path(project_dir)
    plan = _read(p / "storyboard/visual_plan.json")
    doc = _read(p / "script/visual_beats.json")
    sources = _read(p / "research/sources.json") or {"sources": [], "claims": []}
    timing = _read(p / "script/timing.json") or {}
    qa = _read(p / "qa/blender_checks.json") or {"results": []}
    claims = {c["id"]: c for c in sources["claims"]}
    qa_by = {}
    for r in qa["results"]:
        qa_by.setdefault(r["shot"], []).append(r)
    abs_beats = {b["id"]: b for b in timing.get("beats", [])}
    from engine import spec as engine_spec
    site_asset = next((r["asset_id"] for r in plan.get("resolutions", []) if r["concept"] == "river_crossing_site"), None)

    def asset_of(ps, comps):
        shared = set(engine_spec.shared_ids(engine_spec.shot_states(plan["states"], ps["shot"])))
        if comps and set(comps) <= shared:
            return site_asset or "shared base"
        return (ps.get("asset_ids") or [None])[-1]
    rows = []
    for beat in doc["beats"]:
        bid = beat["beat_id"]
        shots = [ps for ps in plan["shots"] if ps["beat_id"] == bid]
        anns = {a["id"]: a for a in beat.get("annotations", [])}
        for k, text in enumerate(T.split_sentences(beat["narration"])):
            sent = (abs_beats.get(bid) or {}).get("sentences", [])
            start = sent[k]["start"] if k < len(sent) and "start_seconds" in abs_beats.get(bid, {}) else None
            shown = []
            for ps in shots:
                for a in (ps.get("annotations") or {}).get("items", []):
                    spec = anns.get(a["id"])
                    if spec is None or spec.get("sentence", 0) != k:
                        continue
                    comps = sorted({c for x in a["anchors"] for c in x.get("component_ids", [])})
                    checks = {r["check"]: r["status"] for r in qa_by.get(ps["shot_id"], [])
                              if r["check"].startswith("annotation_")}
                    shown.append({"annotation": a["id"], "type": a["type"], "text": a.get("text"),
                                  "claim_id": a.get("claim_id"), "shot": ps["shot_id"], "state": ps["states"][-1],
                                  "asset": asset_of(ps, comps), "components": comps,
                                  "appear_seconds": round(ps["timing"]["start_seconds"] + a["appear"], 3),
                                  "disappear_seconds": round(ps["timing"]["start_seconds"] + a["disappear"], 3),
                                  "qa": checks or "not run"})
            cited = sorted(set(beat.get("claim_ids", [])) | {s["claim_id"] for s in shown if s["claim_id"]})
            rows.append({"beat_id": bid, "sentence": k, "text": text, "start_seconds": start,
                         "beat_claims": beat.get("claim_ids", []),
                         "claims": [{"id": c, "status": claims[c]["review_status"],
                                     "evidence": [{"source": e["source_id"], "locator": e["locator"]}
                                                  for e in claims[c].get("evidence", [])]}
                                    for c in cited if c in claims],
                         "shots": [ps["shot_id"] for ps in shots], "annotations": shown})
    return {"project_id": doc["project_id"], "rows": rows}


def write(project_dir):
    p = Path(project_dir)
    data = build(p)
    (p / "qa").mkdir(exist_ok=True)
    (p / "qa/RESEARCH_VISUAL_MAP.json").write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    lines = [f"# Ánh xạ nghiên cứu → hình ảnh: {data['project_id']}", "",
             "Sinh bởi `tools/cli.py research-map` từ visual_plan.json, sources.json, timing.json và "
             "blender_checks.json. Mỗi dòng: câu → claim → nguồn (vị trí) → asset/bộ phận → chú thích → thời điểm → QA.",
             "Claim nào cũng mới ở mức `SOURCE_VERIFIED`, **chưa được duyệt biên tập**.", ""]
    for r in data["rows"]:
        t = f"{r['start_seconds']:.2f} s" if r["start_seconds"] is not None else "chưa lập lịch"
        lines.append(f"## {r['beat_id']}.s{r['sentence']} ({t}): \"{r['text']}\"")
        if r["claims"]:
            for c in r["claims"]:
                ev = "; ".join(f"{e['source']} ({e['locator']})" for e in c["evidence"])
                lines.append(f"- Claim `{c['id']}` [{c['status']}]: {ev}")
        else:
            lines.append("- Không có claim (câu dẫn dắt).")
        lines.append(f"- Shot: {', '.join(r['shots'])}")
        for a in r["annotations"]:
            qa = ", ".join(f"{k} {v}" for k, v in a["qa"].items()) if isinstance(a["qa"], dict) else a["qa"]
            lines.append(f"- Chú thích `{a['annotation']}` {a['type']}" + (f" \"{a['text']}\"" if a["text"] else "")
                         + f" → {a['shot']} / {a['asset']} / {', '.join(a['components'][:3])}"
                         + (" …" if len(a["components"]) > 3 else "")
                         + f"; {a['appear_seconds']:.2f}–{a['disappear_seconds']:.2f} s"
                         + (f"; claim {a['claim_id']}" if a["claim_id"] else "") + f"; QA: {qa}")
        lines.append("")
    (p / "qa/RESEARCH_VISUAL_MAP.md").write_text("\n".join(lines), encoding="utf-8")
    return p / "qa/RESEARCH_VISUAL_MAP.md"
