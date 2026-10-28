"""Narrative component concepts -> semantic component ids of a state.

Matching uses validated semantic metadata (role = semantic type, group) of the planned
components, never Blender object order or free-text name fragments. Ambiguity and
absence are errors the author must resolve."""
from planner import vocabulary as V


class MappingError(ValueError):
    pass


def resolve_targets(refs, parts, vocab, state):
    """refs: concept names or {"concept", "group"}; parts: [{id, role, group}] visible in `state`.
    Returns [{"concept", "roles", "group", "component_ids"}]."""
    out = []
    for ref in refs:
        name = V.concept_name(ref)
        c = vocab.get(name)
        if c is None:
            raise MappingError(f"component concept '{name}' is not in config/visual_vocabulary.json")
        if c["kind"] != "component":
            continue
        group = ref.get("group") if isinstance(ref, dict) else None
        matched = [p for p in parts if p["role"] in c["roles"] and (group is None or p["group"] == group)]
        if not matched:
            have = sorted({p["role"] for p in parts})
            raise MappingError(f"'{name}' ({', '.join(c['roles'])}{', group ' + group if group else ''}) has no "
                               f"component in state '{state}' (its roles: {', '.join(have)})")
        roles = sorted({p["role"] for p in matched})
        if c.get("ambiguous_if_multiple") and len(roles) > 1:
            raise MappingError(f"'{name}' is ambiguous in state '{state}': it matches {roles}; use a specific concept "
                               f"(e.g. {', '.join(k for k, v in vocab.concepts.items() if v.get('roles') == [roles[0]])})")
        out.append({"concept": name, "roles": roles, "group": group, "component_ids": [p["id"] for p in matched]})
    return out


def component_refs(beat, vocab):
    return [r for r in beat.get("required_concepts", []) if vocab.kind(V.concept_name(r)) == "component"]


def architecture_refs(beat, vocab):
    names = [V.concept_name(r) for r in beat.get("preferred_states", []) + beat.get("required_concepts", [])]
    out = []
    for n in names:
        if vocab.kind(n) in ("architecture", "site", None) and n not in out:
            out.append(n)
    return out
