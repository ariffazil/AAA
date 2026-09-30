import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
MAP = REPO / "registries" / "models" / "AGENT_MODEL_MAP.json"
CANON = REPO / "instructions" / "gelombang-2-blindspot-laws.md"


def _primary_agents(doc):
    """Extract agent->entry map from AGENT_MODEL_MAP.json (agents is a LIST of
    {agent_id, primary_model, primary_provider, ...}). Returns dict keyed by agent_id."""
    agents = doc.get("agents") if isinstance(doc, dict) else None
    if isinstance(agents, dict):
        return agents
    if isinstance(agents, list):
        out = {}
        for a in agents:
            if isinstance(a, dict) and a.get("agent_id"):
                out[a["agent_id"]] = a
        if out:
            return out
    for key in ("agent_models", "assignments", "agent_map"):
        if isinstance(doc, dict) and isinstance(doc.get(key), dict):
            return doc[key]
    raise KeyError("AGENT_MODEL_MAP.json: no usable agents block found")


def test_judge_and_builder_primary_models_are_distinct():
    """BL11 (F13 SAH 2026-09-30): judge lane MUST NOT share model+provider with builder lane.

    Same-model verdicts are hidden self-judging (role-label artifact; correction ~0%).
    Source: gelombang-2-blindspot-laws.md, canon fragment.
    """
    doc = json.loads(MAP.read_text())
    agents = _primary_agents(doc)

    def entry(name):
        for key in (name, name.upper(), name.lower()):
            if key in agents:
                return agents[key]
        raise KeyError(f"AGENT_MODEL_MAP.json: agent '{name}' missing (lane law needs both ends)")

    judge = entry("888-APEX")
    builder = entry("333-AGI")

    def pm(e):
        if isinstance(e, str):
            return (e.split("/")[0], e)
        prim = e.get("primary_model") or e.get("primary") or e.get("model") or ""
        prov = e.get("primary_provider") or e.get("provider") or (prim.split("/")[0] if "/" in prim else "")
        return (prov, prim)

    jp, jm = pm(judge)
    bp, bm = pm(builder)
    assert jm and bm, "primary model strings must be non-empty"
    assert (jp, jm) != (bp, bm), (
        "BL11 violation: judge lane (888-APEX) and builder lane (333-AGI) share "
        f"provider/model {jm!r} — self-judging configuration; change one lane's primary."
    )


def test_bl_canon_fragment_present_and_ratified():
    """The law itself must not be silently deleted (attention-kill criterion)."""
    txt = CANON.read_text()
    assert "F13_RATIFIED_CHAT" in txt and "sahkan semua" in txt, (
        "gelombang-2-blindspot-laws.md missing ratification provenance — law altered or removed without trace."
    )
