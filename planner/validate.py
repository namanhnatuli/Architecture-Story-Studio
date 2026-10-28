"""Visual plan validation (independent of the planner: everything is re-derived from the
engine's own spec functions, the asset files, the sources and the beats)."""
import json
import shutil
import tempfile
from pathlib import Path

from engine import spec, templates
from planner import beats as B, camera as CAM, compiler, visibility as VIS, vocabulary as V
from planner.planner import REPLACE_SHARED_BASE_FAMILIES, SITE_STATE

ROOT = Path(__file__).resolve().parent.parent
COVERAGE_STATUSES = ("COVERED", "PARTIALLY_COVERED", "MISSING_ASSET", "MISSING_TEMPLATE", "TIMING_CONFLICT",
                     "EVIDENCE_BLOCKED", "INVALID_REQUEST")
EXECUTABLE_STATUSES = ("COVERED", "PARTIALLY_COVERED")


def _roles(states):
    """component id -> role for the base and every variant (spec functions, not the planner)."""
    roles = {p["id"]: p["role"] for p in spec.base_parts(states)}
    for v in states.get("variants", []):
        for part in spec.builder_parts(dict(v, structure_from=None)):
            roles[part["id"]] = part["role"]
    return roles


def validate_plan(plan, project_dir, root=ROOT, engine_check=True):
    errors = []
    p, root = Path(project_dir), Path(root)
    for key in ("schema", "plan_version", "planner_version", "project_id", "timing_mode", "fps", "total_frames",
                "executable", "inputs", "states", "shots", "coverage"):
        if key not in plan:
            errors.append(f"plan: missing '{key}'")
    if errors:
        return errors
    doc = B.load(p / "script/visual_beats.json")
    src = p / "research/sources.json"
    sources = json.loads(src.read_text()) if src.is_file() else {"sources": [], "claims": []}
    if B.content_hash(doc) != plan["inputs"]["beats_sha256"]:
        errors.append("plan is stale: script/visual_beats.json changed since plan-visuals (re-run plan-visuals)")
    if B.content_hash(sources) != plan["inputs"]["sources_sha256"]:
        errors.append("plan is stale: research/sources.json changed since plan-visuals (re-run plan-visuals)")
    from planner import catalog
    known = {e["asset_id"]: e for e in catalog.index(root)}
    for f in sorted((p / "planning/generated_assets").glob("*.json")):
        known[json.loads(f.read_text())["asset_id"]] = {"path": str(f.resolve())}   # absolute: root / abs == abs
    for asset_id, sha in plan["inputs"]["assets"].items():
        if asset_id not in known:
            errors.append(f"asset {asset_id} is no longer in the catalog or the project's generated assets")
        elif B.content_hash(json.loads((root / known[asset_id]["path"]).read_text())) != sha:
            errors.append(f"plan is stale: asset {asset_id} changed since plan-visuals (re-run plan-visuals)")
    states = plan["states"]
    errors += [f"states: {e}" for e in spec.validate_states(states)]
    if errors:
        return errors
    variants = spec.variant_map(states)
    roles = _roles(states)
    vocab = V.Vocabulary(root / "config/visual_vocabulary.json")
    presets = CAM.style_presets(root)
    beat_order = [b["beat_id"] for b in doc["beats"]]
    beats_by_id = {b["beat_id"]: b for b in doc["beats"]}

    # coverage: every beat exactly once, in order, with a known status
    cov_ids = [c["beat_id"] for c in plan["coverage"]]
    if cov_ids != beat_order:
        errors.append(f"coverage must list every beat once in narration order (got {cov_ids}, beats {beat_order})")
    for c in plan["coverage"]:
        if c["status"] not in COVERAGE_STATUSES:
            errors.append(f"coverage {c['beat_id']}: unknown status {c['status']}")
        shots = [s for s in plan["shots"] if s["beat_id"] == c["beat_id"]]
        if c["status"] in EXECUTABLE_STATUSES and not shots:
            errors.append(f"coverage {c['beat_id']}: {c['status']} but no shot visualises it")
        if c["status"] not in EXECUTABLE_STATUSES and shots:
            errors.append(f"coverage {c['beat_id']}: {c['status']} beat must not have shots")
        ev, detail = B.evidence_status(beats_by_id[c["beat_id"]], sources)
        if ev == "EVIDENCE_BLOCKED" and c["status"] != "EVIDENCE_BLOCKED":
            errors.append(f"beat {c['beat_id']}: claims lack evidence ({detail}) but the plan visualises it")
    executable = all(c["status"] in EXECUTABLE_STATUSES for c in plan["coverage"])
    if plan["executable"] != executable:
        errors.append(f"plan.executable is {plan['executable']} but coverage says {executable}")

    # shots: order, timing, templates, targets, camera, cuts
    t, prev_beat_index, groups = 0, -1, {}
    fps = plan["fps"]
    for i, ps in enumerate(plan["shots"], 1):
        sid, shot = ps["shot_id"], ps["shot"]
        where = f"{sid} ({ps['beat_id']})"
        if sid != f"SC_{i:03d}" or shot.get("id") != sid:
            errors.append(f"{where}: shot ids must be SC_001.. in order")
        bi = beat_order.index(ps["beat_id"]) if ps["beat_id"] in beat_order else -2
        if bi < prev_beat_index:
            errors.append(f"{where}: shots must follow narration order")
        prev_beat_index = bi
        tm = ps["timing"]
        if tm["frames"] != round(tm["duration_seconds"] * fps) or abs(shot["duration_seconds"] - tm["frames"] / fps) > 1e-6:
            errors.append(f"{where}: duration is not a whole number of frames / disagrees with the shot")
        if tm["frames"] + 1e-6 < tm["min_seconds"] * fps - 1:
            errors.append(f"{where}: {tm['frames']} frames is shorter than the visual's minimum {tm['min_seconds']} s")
        if abs(tm["start_seconds"] - t / fps) > 1e-6:
            errors.append(f"{where}: start {tm['start_seconds']} s is not contiguous ({t / fps:.4f} s)")
        t += tm["frames"]
        if tm["mode"] != plan["timing_mode"]:
            errors.append(f"{where}: timing mode {tm['mode']} differs from the plan's {plan['timing_mode']}")
        for s in ps["states"]:
            if s not in variants:
                errors.append(f"{where}: state {s} is not in the plan's states")
        template = ps["template"]
        if template != shot.get("transition") and not (template == "MOTION_GRAPHICS" and shot.get("transition") == "CARD"):
            errors.append(f"{where}: template {template} differs from the shot transition {shot.get('transition')}")
        for s in ps["states"]:
            v = variants.get(s, {})
            if v.get("builder") == spec.ASSET_BUILDER:
                from engine.arch import assets as A
                data, _ = A.load(v["asset"])
                needed = "HIGHLIGHT" if template == "HOLD" and (shot.get("animation") or {}).get("highlight") else template
                if needed not in data["animation_support"] + ["HOLD"] and not (template == "REPLACE_PARTS" and
                                                                               ps["states"][0] == SITE_STATE):
                    errors.append(f"{where}: asset {data['asset_id']} does not support {needed}")
        if template == "REPLACE_PARTS":
            a, b = ps["states"][0], ps["states"][-1]
            va, vb = variants[a], variants[b]
            ok = va.get("builder") == "none" or vb.get("structure_from") == a or va.get("structure_from") == b or \
                (va.get("builder") == vb.get("builder") == "gable_roof" and states.get("building_type") in REPLACE_SHARED_BASE_FAMILIES)
            if not ok:
                errors.append(f"{where}: REPLACE_PARTS {a} -> {b} between states that share no frame")
        visible = set(spec.shared_ids(states))
        for s in ps["states"]:
            visible |= set(spec.state_ids(states, s))
        for tg in ps["semantic_targets"]:
            c = vocab.get(tg["concept"])
            for cid in tg["component_ids"]:
                if cid not in visible:
                    errors.append(f"{where}: target {cid} ({tg['concept']}) is not visible in {ps['states']}")
                elif c is not None and roles.get(cid) not in c.get("roles", []):
                    errors.append(f"{where}: target {cid} has role {roles.get(cid)}, not one of {c.get('roles')} "
                                  f"for concept {tg['concept']}")
        cam = ps["camera"]
        if template != "MOTION_GRAPHICS":
            if cam["mode"] not in CAM.MODES:
                errors.append(f"{where}: unknown camera mode {cam['mode']}")
            if cam["preset"] not in presets:
                errors.append(f"{where}: camera preset {cam['preset']} is not in config/visual_style.json")
        if cam.get("focus") and not set(cam["focus"]) <= visible:
            errors.append(f"{where}: camera focus components are not visible")
        g = groups.setdefault(cam["group"], (shot.get("build_variants"), cam["preset"], cam.get("focus"), cam.get("safe_band")))
        if g != (shot.get("build_variants"), cam["preset"], cam.get("focus"), cam.get("safe_band")):
            errors.append(f"{where}: continuity group {cam['group']} mixes cameras/build sets (match cuts would jump)")
        if ps["cut_from_previous"] == "match" and i > 1:
            prev = plan["shots"][i - 2]
            if prev["camera"]["group"] != cam["group"]:
                errors.append(f"{where}: match cut across continuity groups")
            same = prev["states"] == ps["states"] if template == "SIDE_BY_SIDE" else prev["states"][-1:] == ps["states"][:1]
            if not same:
                errors.append(f"{where}: match cut from {prev['states']} to {ps['states']} changes the shown state")
        if plan["publication"]["restriction"] == "INTERNAL_ONLY" and ps["evidence_status"] != "INTERNAL_PREVIEW":
            errors.append(f"{where}: internal-only plan shots must be marked INTERNAL_PREVIEW")
        try:   # the engine itself must accept the shot (offline template planning)
            templates.plan_shot(shot, states, fps, templates.placeholder_slots(shot, states))
        except Exception as e:   # noqa: BLE001 - report every engine refusal
            errors.append(f"{where}: engine rejects the shot: {e}")
    if t != plan["total_frames"]:
        errors.append(f"total_frames {plan['total_frames']} differs from the sum of shots {t}")
    errors += visibility_errors(plan, root)

    if engine_check and plan["executable"] and not errors:
        errors += [f"engine: {e}" for e in engine_validation(plan, p)]
    return errors


def engine_validation(plan, project_dir):
    """Compile into a temporary copy and run the project validator (G0) on it."""
    from tools.validator import validate_project
    with tempfile.TemporaryDirectory() as tmp:
        dst = Path(tmp) / Path(project_dir).name
        dst.mkdir()
        for sub in ("research", "script", "assets", "planning"):
            if (Path(project_dir) / sub).is_dir():
                shutil.copytree(Path(project_dir) / sub, dst / sub)
        compiler.compile_plan(plan, dst)
        errs, _ = validate_project(dst)
        return errs


def visibility_errors(plan, root=ROOT):
    """M5.5: stored visibility equals a recomputation; every target concept reads in its beat
    (or the beat says it does not); every ghost / close-up repair is documented; comparison
    layouts read for their purpose; a sequential comparison shares one locked camera."""
    from planner import composition, repair
    errors = []
    cfg = json.loads((Path(root) / "config/visual_planning.json").read_text())
    vcfg, ccfg = cfg["visibility"], cfg["composition"]
    presets = CAM.style_presets(root)
    pieces = set(plan.get("pieces_concepts", []))
    states, fps = plan["states"], plan["fps"]
    readable = {}
    for ps in plan["shots"]:
        sid = ps["shot_id"]
        assessed = ps["semantic_targets"] and ps["template"] in ("HOLD", "EXPLODED_VIEW", "REPLACE_PARTS")
        if assessed:
            try:
                _, a = repair.assess_shot(ps, states, vcfg, presets, fps, pieces)
            except Exception as e:   # noqa: BLE001
                errors.append(f"{sid}: visibility cannot be recomputed: {e}")
                continue
            if repair.stored(a) != ps.get("visibility"):
                errors.append(f"{sid}: stored visibility differs from a recomputation (plan edited by hand?)")
            for r in a["targets"]:
                readable.setdefault((ps["beat_id"], r["concept"]), []).append(r["ok"])
        h = (ps["shot"].get("animation") or {}).get("highlight") or {}
        remedies = [r["remedy"] for r in ps.get("repairs", [])]
        if isinstance(h, dict) and h.get("ghost") and not any(r.startswith("GHOST") for r in remedies):
            errors.append(f"{sid}: ghosted parts without a documented visibility repair")
        comp = ps.get("composition") or {}
        if ps["template"] == "SIDE_BY_SIDE" and comp:
            anim = ps["shot"]["animation"]
            shot = composition.comparison_shot(ps["states"], anim["layout"], anim["gap_ratio"], anim["label_band"],
                                               ps["shot"]["camera"])
            m = composition.measure_layout(VIS.build_scene(shot, states, fps, presets), ccfg)
            ok, problems = composition.readable(m, composition.purpose_cfg(ccfg, comp.get("purpose", "detail")))
            if not ok:
                errors.append(f"{sid}: comparison layout does not read for {comp.get('purpose')}: {'; '.join(problems)}")
            if comp.get("scale") != "COMMON":
                errors.append(f"{sid}: a SIDE_BY_SIDE comparison is always at a common scale")
    sequences = {}
    for ps in plan["shots"]:
        if ps.get("sequence"):
            sequences.setdefault(ps["sequence"], []).append(ps)
    for name, members in sequences.items():
        if len({m["camera"]["group"] for m in members}) != 1:
            errors.append(f"{name}: a sequential comparison must keep one locked camera (one continuity group)")
        if any(not (m["shot"]["animation"].get("label")) for m in members):
            errors.append(f"{name}: every model of a sequential comparison needs its caption")
        if any((m.get("composition") or {}).get("scale") != "COMMON" for m in members):
            errors.append(f"{name}: sequential comparison shots must declare scale COMMON (shared camera)")
    cov = {c["beat_id"]: c for c in plan["coverage"]}
    for (bid, concept), oks in readable.items():
        if not any(oks) and (cov[bid]["status"] == "COVERED" or
                             not any(i.startswith("VISIBILITY_UNRESOLVED") for i in cov[bid]["issues"])):
            errors.append(f"beat {bid}: {concept} does not read in any of its shots, but the beat is not flagged "
                          "(PARTIALLY_COVERED + VISIBILITY_UNRESOLVED)")
    return errors
