"""Narrative concepts (config/visual_vocabulary.json)."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PATH = ROOT / "config" / "visual_vocabulary.json"
KINDS = ("site", "architecture", "component")


class Vocabulary:
    def __init__(self, path=PATH):
        self.data = json.loads(Path(path).read_text(encoding="utf-8"))
        self.concepts = self.data["concepts"]

    def get(self, name):
        return self.concepts.get(name)

    def kind(self, name):
        c = self.get(name)
        return c["kind"] if c else None

    def label(self, name):
        c = self.get(name) or {}
        return c.get("label", name.replace("_", " "))


def concept_name(ref):
    """A concept reference is a name or {"concept": name, "group": ...}."""
    return ref["concept"] if isinstance(ref, dict) else ref


def matches(params, where):
    """Parameter predicates: {"key": value} or {"key": {"min": a, "max": b}}."""
    for key, rule in (where or {}).items():
        value = params.get(key)
        if isinstance(rule, dict):
            if value is None or ("min" in rule and value < rule["min"]) or ("max" in rule and value > rule["max"]):
                return False
        elif value != rule:
            return False
    return True


def validate(vocab):
    errors = []
    for name, c in vocab.concepts.items():
        if c.get("kind") not in KINDS:
            errors.append(f"vocabulary {name}: kind must be one of {KINDS}")
        if c.get("kind") in ("site", "architecture") and not (c.get("family") and c.get("variant")):
            errors.append(f"vocabulary {name}: needs family and variant")
        if c.get("kind") == "component" and not c.get("roles"):
            errors.append(f"vocabulary {name}: component concepts need roles")
        if set(c.get("ghost_roles", [])) & set(c.get("roles", [])):
            errors.append(f"vocabulary {name}: ghost_roles (the parts covering it) must differ from its roles")
    return errors
