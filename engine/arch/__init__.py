"""M4 procedural architecture: specification -> semantic components -> geometry.

Pure Python (no bpy) except `realize.py`, so specifications, component plans,
bounding boxes, connectivity and reproducibility can be validated offline.

  semantic.py    component/part records, transforms, bounding boxes, signatures
  primitives.py  mesh primitives (box, member, annular sector, polygon prism, cylinder)
  library.py     reusable architectural utilities (repeat, beams, posts, arches, trusses)
  families/      family generators (bridge.py, site.py) registered in assets.py
  assets.py      architecture asset specifications: load, validate, plan
  checks.py      offline geometry validation (G4-A/G4-B)
  realize.py     Blender objects from components (shared meshes, bevels, materials)
"""
GENERATOR_VERSION = "1.0.0"
