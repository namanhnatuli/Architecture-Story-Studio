"""Semantic annotations in a Blender shot (M6; bpy).

Draws the planner's laid-out annotations (storyboard shot "annotations", made by
planner/annotations.py + engine/annotation_layout.py) as flat, unlit, shadowless meshes and
texts on planes just in front of the orthographic camera: nothing in the model can hide
them, they never touch the architectural geometry, and subtitles stay outside the scene.
Every annotation fades in and out with motion.TRANSPARENCY keys on its own objects
(flat emission materials with blended transparency, engine/diagram.py), so the plan and the
Blender QA see the exact appear/disappear frames.

Depth order towards the camera: plates and region outlines, leaders and lines, arrows, text.
"""
import math

import bpy
from mathutils import Matrix

from engine import diagram, framing, motion

DEPTH = {"rect": 0.48, "plate": 0.47, "line": 0.46, "dot": 0.45, "arrow": 0.44, "text": 0.42}
PREFIX = "ANN_"


class Plane:
    """Frame coordinates (0..1) -> local coordinates of a camera-facing plane at a depth."""

    def __init__(self, fit, basis, aspect):
        self.fit, self.basis, self.aspect = fit, basis, aspect
        self.w = fit["ortho_scale"]
        self.h = self.w / aspect

    def local(self, p):
        return ((p[0] - 0.5) * self.w, (p[1] - 0.5) * self.h, 0.0)

    def matrix(self, depth):
        r, u, f = self.basis
        o = framing.frame_to_world(0.5, 0.5, self.fit, self.basis, self.aspect, toward_camera=depth)
        return Matrix(((r[0], u[0], -f[0], o[0]), (r[1], u[1], -f[1], o[1]),
                       (r[2], u[2], -f[2], o[2]), (0.0, 0.0, 0.0, 1.0)))


def _quad(a, b, width_h, plane):
    """Quad along a-b (frame coords) with a width in frame-HEIGHT units (isotropic)."""
    ax, ay = a[0] * plane.w, a[1] * plane.h
    bx, by = b[0] * plane.w, b[1] * plane.h
    dx, dy = bx - ax, by - ay
    n = math.hypot(dx, dy) or 1.0
    ox, oy = -dy / n * width_h * plane.h / 2, dx / n * width_h * plane.h / 2
    cx, cy = plane.w / 2, plane.h / 2
    return [(ax + ox - cx, ay + oy - cy, 0), (bx + ox - cx, by + oy - cy, 0),
            (bx - ox - cx, by - oy - cy, 0), (ax - ox - cx, ay - oy - cy, 0)]


def _dashes(points, dash, gap, plane):
    """Split a polyline (frame coords) into dash segments (lengths in frame-height units)."""
    out = []
    pos, on = 0.0, True
    for a, b in zip(points, points[1:]):
        ax, ay, bx, by = a[0] * plane.aspect, a[1], b[0] * plane.aspect, b[1]
        seg = math.hypot(bx - ax, by - ay)
        t = 0.0
        while t < seg - 1e-9:
            step = (dash if on else gap) - pos
            t1 = min(seg, t + step)
            if on:
                out.append(([(ax + (bx - ax) * t / seg) / plane.aspect, ay + (by - ay) * t / seg],
                            [(ax + (bx - ax) * t1 / seg) / plane.aspect, ay + (by - ay) * t1 / seg]))
            pos += t1 - t
            if pos >= (dash if on else gap) - 1e-9:
                pos, on = 0.0, not on
            t = t1
    return out


def _mesh(name, verts, faces, plane, depth, material, collection):
    mesh = bpy.data.meshes.new(name + "_mesh")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    obj.data.materials.append(material)
    obj.matrix_world = plane.matrix(depth)
    obj.visible_shadow = False
    obj["ass_transparency"] = 1.0
    collection.objects.link(obj)
    return obj


def _element_geometry(e, plane):
    """(verts, faces) of one primitive in plane-local coordinates."""
    verts, faces = [], []

    def add_quad(q):
        k = len(verts)
        verts.extend(q)
        faces.append((k, k + 1, k + 2, k + 3))

    def add_tri(a, b, c):
        k = len(verts)
        verts.extend([a, b, c])
        faces.append((k, k + 1, k + 2))

    kind = e["kind"]
    if kind == "plate":
        x0, y0, x1, y1 = e["box"]
        bw = e["border_width"]
        add_quad([plane.local((x0, y0)), plane.local((x1, y0)), plane.local((x1, y1)), plane.local((x0, y1))])
        return verts, faces, [(x0, y0, x1, y1, bw)]
    if kind == "rect":
        x0, y0, x1, y1 = e["box"]
        pts = [[x0, y0], [x1, y0], [x1, y1], [x0, y1], [x0, y0]]
        segs = _dashes(pts, e["dash"][0], e["dash"][1], plane) if e.get("dash") else list(zip(pts, pts[1:]))
        for a, b in segs:
            add_quad(_quad(a, b, e["width"], plane))
        return verts, faces, None
    if kind == "line":
        pts = e["points"]
        segs = _dashes(pts, e["dash"][0], e["dash"][1], plane) if e.get("dash") else list(zip(pts, pts[1:]))
        for a, b in segs:
            add_quad(_quad(a, b, e["width"], plane))
        return verts, faces, None
    if kind == "dot":
        cx, cy = e["center"]
        r = e["radius"]
        ring = [plane.local((cx + r * math.cos(2 * math.pi * k / 12) / plane.aspect,
                             cy + r * math.sin(2 * math.pi * k / 12))) for k in range(12)]
        c = plane.local((cx, cy))
        for k in range(12):
            add_tri(c, ring[k], ring[(k + 1) % 12])
        return verts, faces, None
    if kind == "arrow":
        tail, tip = e["tail"], e["tip"]
        dx, dy = (tip[0] - tail[0]) * plane.aspect, tip[1] - tail[1]
        n = math.hypot(dx, dy) or 1.0
        ux, uy = dx / n, dy / n
        hl, hw = e["head_length"], e["head_width"] / 2
        base = [tip[0] - ux * hl / plane.aspect, tip[1] - uy * hl]
        if e["width"] > 0:
            add_quad(_quad(tail, base, e["width"], plane))
        add_tri(plane.local(tip), plane.local((base[0] - uy * hw / plane.aspect, base[1] + ux * hw)),
                plane.local((base[0] + uy * hw / plane.aspect, base[1] - ux * hw)))
        return verts, faces, None
    raise ValueError(f"unknown annotation primitive {kind}")


def build(shot, fit, basis, aspect, collection):
    """Objects for every annotation of the shot: {annotation id: [objects]} (+ texts list)."""
    data = shot.get("annotations") or {}
    plane = Plane(fit, basis, aspect)
    materials, out, texts = {}, {}, {}

    def material(color):
        if color not in materials:
            materials[color] = diagram._flat_material(f"Annotation {color}", color)
        return materials[color]

    for ann in data.get("items", []):
        objs = []
        for k, e in enumerate(ann["elements"]):
            name = f"{PREFIX}{ann['id']}_{k:02d}_{e['kind']}"
            if e["kind"] == "text":
                curve = bpy.data.curves.new(name + "_text", type="FONT")
                curve.body = e["text"]
                curve.size = e["size"] * plane.h
                curve.align_x, curve.align_y = "CENTER", "CENTER"
                obj = bpy.data.objects.new(name, curve)
                obj.data.materials.append(material(e["color"]))
                m = plane.matrix(DEPTH["text"])
                loc = plane.local(e["center"])
                obj.matrix_world = m @ Matrix.Translation(loc)
                obj.visible_shadow = False
                obj["ass_transparency"] = 1.0
                collection.objects.link(obj)
                texts.setdefault(ann["id"], []).append((obj, e))
                objs.append(obj)
                continue
            verts, faces, border = _element_geometry(e, plane)
            depth = DEPTH[e["kind"]] + (0.003 if e.get("halo") else 0.0)   # halos sit just behind their line
            obj = _mesh(name, verts, faces, plane, depth, material(e.get("fill") or e["color"]), collection)
            objs.append(obj)
            if border:   # plate outline (slightly behind the plate fill)
                x0, y0, x1, y1, bw = border[0]
                pts = [[x0, y0], [x1, y0], [x1, y1], [x0, y1], [x0, y0]]
                bv, bf = [], []
                for a, b in zip(pts, pts[1:]):
                    q = _quad(a, b, bw, plane)
                    k2 = len(bv)
                    bv.extend(q)
                    bf.append((k2, k2 + 1, k2 + 2, k2 + 3))
                objs.append(_mesh(name + "_border", bv, bf, plane, DEPTH["plate"] - 0.005, material(e["border"]),
                                  collection))
        for obj in objs:
            obj["annotation_id"] = ann["id"]
            obj["annotation_type"] = ann["type"]
        out[ann["id"]] = objs
    return out, texts


def key_fades(plan, built, shot, fps, fade_seconds):
    """Transparency keys: invisible before `appear`, fade in, hold, fade out at `disappear`."""
    data = shot.get("annotations") or {}
    n = plan.frame_count
    for ann in data.get("items", []):
        f_in = max(1, int(round(ann["appear"] * fps)) + 1)
        f_out = min(n, int(round(ann["disappear"] * fps)))
        fade = max(1, int(round(fade_seconds * fps)))
        for obj in built.get(ann["id"], []):
            name = obj.name
            if f_in <= 1:
                plan.key(name, motion.TRANSPARENCY, 1, 0.0)
            else:
                plan.key(name, motion.TRANSPARENCY, 1, 1.0)
                plan.key(name, motion.TRANSPARENCY, f_in, 1.0, "SMOOTH")
                plan.key(name, motion.TRANSPARENCY, min(f_in + fade, n), 0.0)
            if f_out < n:
                plan.key(name, motion.TRANSPARENCY, max(f_out - fade, f_in + fade), 0.0, "SMOOTH")
                plan.key(name, motion.TRANSPARENCY, f_out, 1.0)
                plan.key(name, motion.TRANSPARENCY, n, 1.0)
            else:
                plan.key(name, motion.TRANSPARENCY, n, 0.0)
