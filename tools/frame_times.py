"""Render speed from Blender logs (M7): per-shot frame deltas from the `Saved:` timestamps, so a
Mac that slept mid-render does not distort the numbers (gaps >= 10 s are counted, not summed).

  python3 tools/frame_times.py projects/<slug>/qa preview   -> JSON on stdout
"""
import json
import re
import statistics
import sys
from pathlib import Path

SLEEP_GAP = 10.0


def secs(stamp):
    t = 0.0
    for x in stamp.split(":"):
        t = t * 60 + float(x)
    return t


def shot_times(log):
    ts = [secs(m.group(1)) for m in re.finditer(r"^(\d+:\d+(?::\d+)?\.\d+)\s+render\s+\| Saved:", log.read_text(), re.M)]
    if len(ts) < 2:
        return None
    d = [b - a for a, b in zip(ts, ts[1:])]
    awake = [x for x in d if x < SLEEP_GAP]
    return {"frames": len(ts), "median": round(statistics.median(d), 3), "p90": round(sorted(d)[int(len(d) * 0.9)], 3),
            "awake_seconds": round(sum(awake) + ts[0], 1), "sleep_gaps": sum(1 for x in d if x >= SLEEP_GAP)}


def main():
    qa, preset = Path(sys.argv[1]), sys.argv[2]
    rows = {}
    for log in sorted(qa.glob(f"render_SC_*_{preset}.log")):
        r = shot_times(log)
        if r:
            rows[log.stem.split("_")[1] + "_" + log.stem.split("_")[2]] = r
    frames = sum(r["frames"] for r in rows.values())
    awake = sum(r["awake_seconds"] for r in rows.values())
    print(json.dumps({"preset": preset, "shots": len(rows), "frames": frames, "awake_render_seconds": round(awake, 1),
                      "seconds_per_frame": round(awake / max(frames, 1), 3),
                      "sleep_gaps": sum(r["sleep_gaps"] for r in rows.values()), "per_shot": rows}, indent=2))


if __name__ == "__main__":
    main()
