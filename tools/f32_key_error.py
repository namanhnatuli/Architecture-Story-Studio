"""Independent check of engine.motion.F32_KEY_ULPS (2026-11-12): how far Blender's evaluated F-curve value sits from
the float64 plan, in float32 ulps. Random key pairs over the value ranges the films use (0.5 m to a 2 km camera scale,
and moves across zero), every easing the engine writes (engine/animate.py), every in-between frame; no engine code
writes the keys, so the plan's own key writer is not what is being checked.

    blender -b --factory-startup --python tools/f32_key_error.py -- OUT.json [segment|keys]

segment (default): ulps of max(|a|, |b|, |b - a|), the scale Plan.key_tolerance uses; keys: ulps of max(|a|, |b|).
Result on Blender 5.2.2 (2026-11-12, 400 key pairs x 5 ranges per easing, 640,000 frames): at most 2.9 ulps of the
segment scale (4.8 ulps of the key scale: a move across zero changes by more than either key).
"""
import json
import math
import random
import sys
from pathlib import Path

import bpy

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from engine import motion  # noqa: E402
from engine.animate import iter_fcurves  # noqa: E402

args = sys.argv[sys.argv.index("--") + 1:]
out = args[0]
scale_kind = args[1] if len(args) > 1 else "segment"
TRIALS = 400
RANGES = [(0.5, 10), (10, 100), (100, 600), (600, 2000), (-1500, 1500)]
rng = random.Random(20261112)
ob = bpy.data.objects.new("probe", None)
bpy.context.scene.collection.objects.link(ob)

rows = {}
for easing in [e for e in motion.EASINGS if e != "CONSTANT"]:
    interp, ease_mode = motion.EASINGS[easing]
    worst, hist = {"ulps": 0.0}, {}
    for lo, hi in RANGES:
        for trial in range(TRIALS):
            a, b = rng.uniform(lo, hi), rng.uniform(lo, hi)
            if trial % 4 == 0:
                b = a * (1 + rng.uniform(-0.02, 0.02))   # small moves on large values (a slow push)
            n = rng.choice((12, 24, 43, 62, 96, 140))
            f0 = rng.randint(1, 40)
            if ob.animation_data:
                ob.animation_data_clear()
            ob.location[0] = a
            ob.keyframe_insert("location", index=0, frame=f0)
            ob.location[0] = b
            ob.keyframe_insert("location", index=0, frame=f0 + n)
            fc = iter_fcurves(ob)[0]
            for kp in fc.keyframe_points:
                kp.interpolation, kp.easing = interp, ease_mode
            fc.update()
            scale = max(abs(a), abs(b), abs(b - a)) if scale_kind == "segment" else max(abs(a), abs(b))
            for k in range(n + 1):
                want = a + (b - a) * motion.ease(easing, k / n)
                got = fc.evaluate(f0 + k)
                u = abs(got - want) / motion.f32_ulp(scale)
                hist[int(math.ceil(u))] = hist.get(int(math.ceil(u)), 0) + 1
                if u > worst["ulps"]:
                    worst = {"ulps": round(u, 3), "a": a, "b": b, "frames": n, "k": k, "want": want, "got": got}
    rows[easing] = {"worst": worst, "histogram_ceil_ulps": dict(sorted(hist.items()))}
report = {"blender": bpy.app.version_string, "scale": scale_kind, "trials_per_range": TRIALS, "ranges": RANGES,
          "f32_key_ulps": motion.F32_KEY_ULPS, "rows": rows,
          "max_ulps": max(r["worst"]["ulps"] for r in rows.values())}
Path(out).write_text(json.dumps(report, indent=2))
print("F32_KEY_ERROR", json.dumps({k: v["worst"]["ulps"] for k, v in rows.items()}))
