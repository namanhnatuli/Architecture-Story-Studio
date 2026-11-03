"""Semantic architectural components (pure Python).

A component is the unit the animation templates address: one Blender object with
a stable ID, a semantic type, one material, an owner variant, an assembly layer
and an optional explode direction. Its geometry is a mesh in component-local
space (origin = `location`, rotated by `rotation`, Euler XYZ radians as in Blender).
Repeated sub-parts (planks, posts, truss members) are merged into one component
mesh so a model stays tens of objects, not thousands; identical component meshes
are shared as one Blender mesh datablock (realize.py).
"""
import hashlib
import json
import math
from dataclasses import dataclass, field

SEMANTIC_TYPES = (
    # site / foundations
    "GROUND", "WATER", "FOUNDATION", "ABUTMENT", "PIER", "CUTWATER", "BEARING",
    # supports and beams
    "SUPPORT", "COLUMN", "CAP_BEAM", "BRACING", "BEAM", "STRINGER", "FLOOR_BEAM",
    # masonry arches
    "ARCH", "VOUSSOIR", "KEYSTONE", "SPANDREL",
    # deck and edges
    "DECK", "PLANK", "PARAPET", "COPING", "RAILING",
    # trusses
    "TRUSS_CHORD", "TRUSS_VERTICAL", "TRUSS_DIAGONAL", "END_POST", "JOINT",
    # long-span bridges (M8): cantilever trusses, suspension and cable-stayed
    "ANCHOR_ARM", "CANTILEVER_ARM", "SUSPENDED_SPAN", "TOWER", "PYLON", "MAIN_CABLE", "HANGER", "STAY_CABLE",
    "ANCHORAGE", "STIFFENING_TRUSS",
    # buildings (existing house builders use their own roles)
    "ROOF", "WALL", "FLOOR", "DECORATION",
)
ANIMATION_ROLES = ("EXPLODE", "HIGHLIGHT", "REPLACE", "STATIC")


@dataclass
class Component:
    id: str                      # stable local id, e.g. "arch2_voussoir07" (variant prefix added on plan)
    type: str                    # one of SEMANTIC_TYPES
    material: str                # key in the material library
    mesh: dict                   # {"verts", "faces"} in component-local space
    group: str = ""              # semantic group, e.g. "arch_2", "deck", "truss_north"
    location: tuple = (0.0, 0.0, 0.0)
    rotation: tuple = (0.0, 0.0, 0.0)
    layer: int = 0               # assembly order (0 first)
    hint: tuple = None           # explode direction (unit-ish vector) or None
    animation: tuple = ("HIGHLIGHT",)
    bevel: float = 0.0           # non-destructive bevel width in metres
    variant: str = "shared"
    evidence: str = None         # optional claim id
    meta: dict = field(default_factory=dict)

    @property
    def role(self):
        return self.type.lower()


def rotation_matrix(rot):
    """3x3 matrix of Blender's Euler XYZ (R = Rz @ Ry @ Rx)."""
    rx, ry, rz = rot
    cx, sx, cy, sy, cz, sz = math.cos(rx), math.sin(rx), math.cos(ry), math.sin(ry), math.cos(rz), math.sin(rz)
    return ((cz * cy, cz * sy * sx - sz * cx, cz * sy * cx + sz * sx),
            (sz * cy, sz * sy * sx + cz * cx, sz * sy * cx - cz * sx),
            (-sy, cy * sx, cy * cx))


def to_world(comp, p):
    m = rotation_matrix(comp.rotation)
    return tuple(comp.location[i] + sum(m[i][j] * p[j] for j in range(3)) for i in range(3))


def world_verts(comp):
    return [to_world(comp, v) for v in comp.mesh["verts"]]


def bbox(comp):
    pts = world_verts(comp)
    return (tuple(min(p[i] for p in pts) for i in range(3)), tuple(max(p[i] for p in pts) for i in range(3)))


def union_bbox(comps):
    boxes = [bbox(c) for c in comps]
    return (tuple(min(b[0][i] for b in boxes) for i in range(3)), tuple(max(b[1][i] for b in boxes) for i in range(3)))


def mesh_signature(mesh, extra=None, digits=5):
    """Content hash of a local mesh (rounded): equal signatures share a Blender mesh."""
    payload = {"v": [[round(c, digits) for c in v] for v in mesh["verts"]], "f": [list(f) for f in mesh["faces"]],
               "x": extra}
    return hashlib.sha256(json.dumps(payload, separators=(",", ":")).encode()).hexdigest()


def component_record(comp):
    """JSON-able summary (catalog, reproducibility comparisons)."""
    lo, hi = bbox(comp)
    return {"id": comp.id, "type": comp.type, "role": comp.role, "material": comp.material, "group": comp.group,
            "variant": comp.variant, "layer": comp.layer,
            "location": [round(v, 5) for v in comp.location], "rotation": [round(v, 6) for v in comp.rotation],
            "hint": [round(v, 5) for v in comp.hint] if comp.hint else None,
            "animation": list(comp.animation), "bevel": comp.bevel, "evidence": comp.evidence,
            "bbox": [[round(v, 4) for v in lo], [round(v, 4) for v in hi]],
            "dimensions": [round(hi[i] - lo[i], 4) for i in range(3)],
            "verts": len(comp.mesh["verts"]), "faces": len(comp.mesh["faces"]),
            "mesh_signature": mesh_signature(comp.mesh)}


def validate_components(comps):
    """Structural checks of a component list; returns error strings."""
    errors, seen = [], set()
    for c in comps:
        if not c.id or not all(ch.isalnum() or ch == "_" for ch in c.id):
            errors.append(f"component id {c.id!r} must be non-empty [A-Za-z0-9_] (no '.', used by SIDE_BY_SIDE names)")
        if c.id in seen:
            errors.append(f"duplicate component id {c.id}")
        seen.add(c.id)
        if c.type not in SEMANTIC_TYPES:
            errors.append(f"{c.id}: unknown semantic type {c.type!r}")
        if not c.material:
            errors.append(f"{c.id}: no material")
        if not c.mesh.get("verts") or not c.mesh.get("faces"):
            errors.append(f"{c.id}: empty mesh")
            continue
        n = len(c.mesh["verts"])
        if any(i < 0 or i >= n for f in c.mesh["faces"] for i in f):
            errors.append(f"{c.id}: face index out of range")
        lo, hi = bbox(c)
        if any(hi[i] - lo[i] <= 1e-6 for i in range(3)) and c.type != "WATER":
            errors.append(f"{c.id}: degenerate bounding box {lo}..{hi}")
        if any(not math.isfinite(v) for p in (lo, hi) for v in p):
            errors.append(f"{c.id}: non-finite coordinates")
        if c.hint is not None and (len(c.hint) != 3 or math.sqrt(sum(v * v for v in c.hint)) < 1e-6):
            errors.append(f"{c.id}: explode hint must be a non-zero 3-vector")
        if not isinstance(c.layer, int) or c.layer < 0:
            errors.append(f"{c.id}: layer must be an integer >= 0")
        bad = [a for a in c.animation if a not in ANIMATION_ROLES]
        if bad:
            errors.append(f"{c.id}: unknown animation role(s) {bad}")
    return errors
