"""Render-cache dependency model (stdlib only, no Blender).

A shot's frames depend only on *visual* inputs. Each input category is hashed
separately and stored in renders/<preset>/<shot>/render_manifest.json, so a stale
shot can say which category changed:

  shot_visual      the shot's own render fields (animation/graphic, states, camera, duration...)
  states_geometry  base + the variants the shot builds, without editorial metadata (single-model
                   shots build every variant unless M5 build_variants limits them to one
                   continuity group; the locked camera is fitted to what is built)
  project_render   project fields the engine reads (fps)
  style            config/visual_style.json
  preset           the preset entry (width, height, fps, engine, format)
  engine           engine/**/*.py that run during a render (qa_checks.py and the deprecated
                   transform.py are excluded); recursive since M4 (engine/arch/)
  assets           M4: contents of the architecture asset specs referenced by states.json
                   (base + variants) and, when any is referenced, the shared material library

Not render dependencies (never invalidate frames): narration text, audio and its
rights class, pronunciation, subtitles, timeline position (start_seconds),
cut_from_previous, beat/claim ids, visual_purpose, source ledger and review
statuses, project title/duration/factual_review/audio_timing_locked.
Unknown shot/state/project fields are treated as visual (fail-safe: re-render).
"""
import hashlib
import json
from pathlib import Path

KEY_VERSION = 3
ROOT = Path(__file__).resolve().parent.parent

SHOT_NON_VISUAL = ("beat_ids", "visual_purpose", "narration", "claim_ids", "start_seconds", "cut_from_previous",
                   "notes", "editorial")
STATE_NON_VISUAL = ("name", "claim_ids", "note", "notes", "description")
STATES_TOP_NON_VISUAL = ("note", "transitions", "schema_version")
PROJECT_NON_VISUAL = ("slug", "title", "mode", "language", "duration_seconds", "render_preset", "factual_review",
                      "audio_timing_locked", "notes", "production_profile", "publication_metadata")
ENGINE_EXCLUDED = ("qa_checks.py", "qa_visibility.py", "transform.py")
CATEGORIES = ("shot_visual", "states_geometry", "project_render", "style", "preset", "engine", "assets")
MATERIAL_LIBRARY = "asset_library/materials/stylized_materials.json"


def digest(obj):
    data = obj if isinstance(obj, bytes) else json.dumps(obj, sort_keys=True, ensure_ascii=False).encode()
    return hashlib.sha256(data).hexdigest()


def shot_visual(shot):
    return {k: v for k, v in shot.items() if k not in SHOT_NON_VISUAL}


def built_variants(shot, states):
    """Variants a shot builds (M5): its slots' build sets; every variant if it cannot be planned."""
    from engine import templates
    try:
        return {v for _, built, _ in templates.layout_slots(shot, states) for v in built}
    except Exception:   # invalid shot: depend on everything (fail-safe)
        return {v.get("id") for v in states.get("variants", [])}


def states_geometry(states, only=None):
    out = {k: v for k, v in states.items() if k not in STATES_TOP_NON_VISUAL}
    out["variants"] = [{k: v for k, v in var.items() if k not in STATE_NON_VISUAL}
                       for var in states.get("variants", []) if only is None or var.get("id") in only]
    return out


def project_render(project):
    return {k: v for k, v in project.items() if k not in PROJECT_NON_VISUAL}


def engine_files(root=ROOT):
    base = Path(root) / "engine"
    return [f for f in sorted(base.rglob("*.py")) if f.name not in ENGINE_EXCLUDED and "__pycache__" not in f.parts]


def asset_files(states, root=ROOT, only=None):
    """Asset spec files referenced by a states.json (+ material library if any); with `only`,
    just the base and those variants (the ones a shot builds)."""
    refs = [(states.get("base") or {}).get("asset")] + [v.get("asset") for v in states.get("variants", [])
                                                          if only is None or v.get("id") in only]
    refs = sorted({r for r in refs if r})
    return refs + ([MATERIAL_LIBRARY] if refs else [])


def components(p, shot, preset, root=ROOT):
    """{category: sha256} for one shot at one preset."""
    p, root = Path(p), Path(root)
    read = lambda path: json.loads(Path(path).read_text(encoding="utf-8"))
    presets = read(root / "config/render_presets.json")
    states = read(p / "storyboard/states.json")
    built = built_variants(shot, states)
    return {
        "shot_visual": digest(shot_visual(shot)),
        "states_geometry": digest(states_geometry(states, built)),
        "project_render": digest(project_render(read(p / "project.json"))),
        "style": digest((root / "config/visual_style.json").read_bytes()),
        "preset": digest({"name": preset, **presets[preset]}),
        "engine": digest(engine_file_hashes(root)),
        "assets": digest({rel: digest((root / rel).read_bytes()) if (root / rel).is_file() else "missing"
                          for rel in asset_files(states, root, built)}),
    }


def engine_file_hashes(root=ROOT):
    base = Path(root) / "engine"
    return {str(f.relative_to(base)): digest(f.read_bytes()) for f in engine_files(root)}


def cache_key(parts):
    return digest({"v": KEY_VERSION, **parts})


def stale_reasons(manifest, parts, engine_hashes=None):
    """Why a stored render no longer matches (empty list = cache valid)."""
    if not manifest:
        return ["never rendered"]
    if manifest.get("key_version") != KEY_VERSION:
        return [f"render manifest key v{manifest.get('key_version', 1)} (older pipeline): one-time re-render"]
    stored = manifest.get("components", {})
    reasons = [c for c in CATEGORIES if stored.get(c) != parts.get(c)]
    if "engine" in reasons and engine_hashes and manifest.get("engine_files"):
        changed = sorted(n for n in set(engine_hashes) | set(manifest["engine_files"])
                         if engine_hashes.get(n) != manifest["engine_files"].get(n))
        reasons[reasons.index("engine")] = "engine (" + ", ".join(changed) + ")"
    return reasons


def report(p, preset, shots, root=ROOT):
    """Rows {shot, status, reasons} for every shot at a preset."""
    rows = []
    eh = engine_file_hashes(root)
    for shot in shots:
        mpath = Path(p) / "renders" / preset / shot["id"] / "render_manifest.json"
        manifest = json.loads(mpath.read_text()) if mpath.is_file() else None
        reasons = stale_reasons(manifest, components(p, shot, preset, root), eh)
        rows.append({"shot": shot["id"], "status": "CACHED" if not reasons else "STALE", "reasons": reasons})
    return rows
