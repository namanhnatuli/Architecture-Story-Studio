"""Offline annotation layout preview (M6; stdlib + ffmpeg, no Blender): the shot's raster
silhouettes in grey, the visible annotation targets darker, and every laid-out annotation
primitive (plates as boxes, text as bars, lines, arrows, dots) at the given time.

  python3 tools/annotation_preview.py --project why-bridges-look-different --shot SC_002 [--time 12.0]

Writes qa/annotations/<shot>_layout_<t>.png. For layout debugging and the QA report; the
rendered Blender frames remain the reference."""
import argparse
import json
import math
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from planner import camera as CAM, visibility as VIS  # noqa: E402
from tools.cli import ffmpeg_bin  # noqa: E402


def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


class Canvas:
    def __init__(self, w, h, bg=(237, 235, 229)):
        self.w, self.h = w, h
        self.px = [[bg] * w for _ in range(h)]

    def put(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.px[self.h - 1 - y][x] = c

    def rect(self, box, c, fill=True, width=1):
        x0, y0, x1, y1 = (int(round(box[0] * self.w)), int(round(box[1] * self.h)),
                          int(round(box[2] * self.w)), int(round(box[3] * self.h)))
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                if fill or min(x - x0, x1 - x, y - y0, y1 - y) < width:
                    self.put(x, y, c)

    def line(self, p, q, c, width=1):
        x0, y0, x1, y1 = p[0] * self.w, p[1] * self.h, q[0] * self.w, q[1] * self.h
        n = int(max(abs(x1 - x0), abs(y1 - y0))) + 1
        r = max(0, width // 2)
        for k in range(n + 1):
            t = k / n
            x, y = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
            for dx in range(-r, r + 1):
                for dy in range(-r, r + 1):
                    self.put(int(x) + dx, int(y) + dy, c)

    def tri(self, a, b, c, col):
        pts = [(a[0] * self.w, a[1] * self.h), (b[0] * self.w, b[1] * self.h), (c[0] * self.w, c[1] * self.h)]
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        for y in range(int(min(ys)), int(max(ys)) + 1):
            for x in range(int(min(xs)), int(max(xs)) + 1):
                def side(p, q):
                    return (q[0] - p[0]) * (y + 0.5 - p[1]) - (q[1] - p[1]) * (x + 0.5 - p[0])
                s = [side(pts[0], pts[1]), side(pts[1], pts[2]), side(pts[2], pts[0])]
                if all(v >= 0 for v in s) or all(v <= 0 for v in s):
                    self.put(x, y, col)

    def save(self, path):
        ppm = Path(path).with_suffix(".ppm")
        with open(ppm, "wb") as f:
            f.write(f"P6 {self.w} {self.h} 255\n".encode())
            f.write(bytes(v for row in self.px for c in row for v in c))
        subprocess.run([ffmpeg_bin(), "-y", "-loglevel", "error", "-i", str(ppm), str(path)], check=True)
        ppm.unlink()


def draw(project, shot_id, t=None, width=960):
    p = ROOT / "projects" / project
    plan = json.loads((p / "storyboard/visual_plan.json").read_text())
    ps = next(s for s in plan["shots"] if s["shot_id"] == shot_id)
    ann = ps.get("annotations") or {"items": []}
    if t is None:
        t = max([a["appear"] for a in ann["items"]] or [0.0]) + 0.5
    scene = VIS.build_scene(ps["shot"], plan["states"], plan["fps"], CAM.style_presets(ROOT))
    h = int(round(width / scene.aspect))
    cv = Canvas(width, h)
    frame = max(1, min(scene.frame_count, int(round(t * plan["fps"])) + 1))
    st = VIS.state_at(scene, frame)
    opaque = [(n, poly) for n, (polys, op) in st.items() if op for poly in polys]
    nx, ny = width // 2, h // 2
    ids = VIS.raster(opaque, scene, nx, ny)
    targets = {f"MAIN__{c}" for a in ann["items"] if a["appear"] <= t < a["disappear"]
               for x in a["anchors"] for c in x.get("component_ids", [])}
    for j in range(ny):
        for i in range(nx):
            v = ids[j][i]
            if v is None:
                continue
            c = (120, 116, 108) if any(v.endswith(k) for k in [x.split("__", 1)[-1] for x in targets]) else (196, 192, 184)
            for dx in (0, 1):
                for dy in (0, 1):
                    cv.put(2 * i + dx, 2 * j + dy, c)
    cv.rect([0, 0, 1, 0.17], (226, 214, 214), fill=False, width=2)   # subtitle zone outline
    for a in ann["items"]:
        if not (a["appear"] <= t < a["disappear"]):
            continue
        for e in a["elements"]:
            col = hex_rgb(e.get("color") or e.get("fill") or "#000000")
            if e["kind"] == "plate":
                cv.rect(e["box"], hex_rgb(e["fill"]))
                cv.rect(e["box"], hex_rgb(e["border"]), fill=False, width=1)
            elif e["kind"] == "text":
                b = e["box"]
                cy = (b[1] + b[3]) / 2
                cv.rect([b[0] + 0.006, cy - e["size"] * 0.25, b[2] - 0.006, cy + e["size"] * 0.25], col)
            elif e["kind"] in ("line",):
                pts = e["points"]
                for q0, q1 in zip(pts, pts[1:]):
                    cv.line(q0, q1, col, max(1, int(e["width"] * h)))
            elif e["kind"] == "rect":
                cv.rect(e["box"], col, fill=False, width=max(1, int(e["width"] * h)))
            elif e["kind"] == "dot":
                r = e["radius"]
                cv.rect([e["center"][0] - r / scene.aspect, e["center"][1] - r, e["center"][0] + r / scene.aspect,
                         e["center"][1] + r], col)
            elif e["kind"] == "arrow":
                tail, tip = e["tail"], e["tip"]
                dx, dy = (tip[0] - tail[0]) * scene.aspect, tip[1] - tail[1]
                n = math.hypot(dx, dy) or 1.0
                ux, uy = dx / n, dy / n
                base = [tip[0] - ux * e["head_length"] / scene.aspect, tip[1] - uy * e["head_length"]]
                if e["width"] > 0:
                    cv.line(tail, base, col, max(1, int(e["width"] * h)))
                hw = e["head_width"] / 2
                left = [base[0] - uy * hw / scene.aspect, base[1] + ux * hw]
                right = [base[0] + uy * hw / scene.aspect, base[1] - ux * hw]
                cv.tri(tip, left, right, col)
    out = p / "qa" / "annotations" / f"{shot_id}_layout_{t:05.2f}.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    cv.save(out)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True)
    ap.add_argument("--shot", required=True)
    ap.add_argument("--time", type=float)
    args = ap.parse_args()
    print(draw(args.project, args.shot, args.time))


if __name__ == "__main__":
    main()
