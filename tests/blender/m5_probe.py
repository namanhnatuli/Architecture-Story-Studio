"""Runs inside headless Blender for tests/test_blender_m5.py; prints one 'M5_PROBE {json}' line.
argv: <temp project> built from the M5 pilot's SC_003 (stringers glowing under the deck),
once with the planner's ghosting of the planks and once without it."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import bpy  # noqa: E402,F401
from engine import qa_checks, shot_builder, templates  # noqa: E402

project = Path(sys.argv[sys.argv.index("--") + 1])
out = {"threshold": qa_checks.HIGHLIGHT_MIN_VISIBLE}
for sid in ("GHOST", "PLAIN"):
    ctx = shot_builder.build_shot(project, sid, "preview")
    h = ctx.cfg["highlight"]
    names = {templates.object_name(templates.MAIN_SLOT, i) for i in h["components"]}
    peak = ctx.plan.markers["highlight_peak"]
    share, area = qa_checks.highlight_visibility(ctx, names, peak)
    ctx.scene.frame_set(peak)
    ghosts = h.get("ghost") or []
    twins = [ctx.fade_twins[g] for g in ghosts if g in ctx.fade_twins]
    out[sid] = {"share": round(share, 3), "area": round(area, 4), "ghosts": len(ghosts),
                "twins_shown_at_peak": sum(not t.hide_render for t in twins),
                "originals_hidden_at_peak": sum(ctx.objects[g].hide_render for g in ghosts)}
    ctx.scene.frame_set(ctx.frame_count)
    out[sid]["ghosts_opaque_at_end"] = all(not ctx.objects[g].hide_render and
                                           float(ctx.objects[g]["ass_transparency"]) == 0.0 for g in ghosts)
print("M5_PROBE " + json.dumps(out))
