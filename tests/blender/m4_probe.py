"""Runs inside headless Blender for tests/test_blender_m4.py; prints one 'M4_PROBE {json}' line."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import bpy  # noqa: E402
from engine import shot_builder  # noqa: E402
from engine.arch import asset_scene, semantic  # noqa: E402

style = json.loads((ROOT / "config/visual_style.json").read_text())
preset = json.loads((ROOT / "config/render_presets.json").read_text())["preview"]
STONE = "asset_library/architecture/bridges/bridge_stone_arch_03.json"
out = {}

scene, objs, comps, stats = asset_scene.build(STONE, style, preset)
v = next(c for c in comps if c.id.endswith("arch2_voussoir03"))
obj = objs[v.id]
blender = [tuple(obj.matrix_world @ p.co) for p in obj.data.vertices]
out["rotation_error"] = max(abs(a - b) for p, q in zip(blender, semantic.world_verts(v)) for a, b in zip(p, q))
out["voussoir_mesh_datablocks"] = len({objs[c.id].data.name for c in comps if c.type == "VOUSSOIR"})
out["voussoirs"] = sum(c.type == "VOUSSOIR" for c in comps)
out["bevel_is_modifier"] = all(any(m.type == "BEVEL" for m in objs[c.id].modifiers) for c in comps if c.bevel)
out["base_mesh_unapplied"] = all(len(objs[c.id].data.vertices) == len(c.mesh["verts"]) for c in comps)
out["collections"] = sorted({col.name for c in comps for col in objs[c.id].users_collection})[:4]
out["clean"] = {n: ok for n, ok, _ in asset_scene.geometry_qa(objs)}

key = next(c for c in comps if c.type == "KEYSTONE")
objs[key.id].location.z -= 0.4
bpy.context.view_layer.update()
res = {n: (ok, d) for n, ok, d in asset_scene.geometry_qa(objs)}
out["keystone_pushed"] = {"intersections_ok": res["bvh_no_unintended_intersections"][0],
                          "mentions_keystone": key.id in res["bvh_no_unintended_intersections"][1]}

scene, objs, comps, stats = asset_scene.build(STONE, style, preset)
deck = next(c for c in comps if c.type == "DECK")
objs[deck.id].location.z += 3.0
bpy.context.view_layer.update()
res = {n: (ok, d) for n, ok, d in asset_scene.geometry_qa(objs)}
out["deck_lifted"] = {"connected_ok": res["bvh_connected_to_ground"][0],
                      "mentions_deck": deck.id in res["bvh_connected_to_ground"][1]}

sigs = []
for _ in range(2):
    scene, objs, comps, stats = asset_scene.build(STONE, style, preset)
    sigs.append(asset_scene.signature(objs)[0])
out["rebuild_identical"] = sigs[0] == sigs[1]

project = Path(sys.argv[sys.argv.index("--") + 1])
ctx = shot_builder.build_shot(project, "S1", "preview")
shown = [o for o in ctx.objects.values() if not o.hide_render]
out["reuse_project"] = {"keystones_shown": sum(o.get("semantic_type") == "KEYSTONE" for o in shown),
                        "camera": ctx.camera.name, "frames": ctx.frame_count}
print("M4_PROBE " + json.dumps(out))
