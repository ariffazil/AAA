---
name: arifos-philosophy-anchor-wiring
description: Wire philosophical quotes (27-zone atlas) into arifOS MCP tool responses. Fixes silent quote extraction failures when select_governed_philosophy() returns empty primary_quote.
triggers: ["philosophical anchor", "philosophical quotes", "select_governed_philosophy", "philosophy atlas", "27-zone", "quote injection", "PHILOSOPHY_ATLAS"]
---

# arifOS Philosophical Anchor — Wiring Skill

## When to use
- Wiring philosophical quotes into any of the 13 canonical MCP tools
- Auditing whether tool responses carry a `philosophical_anchor` field
- Debugging why `select_governed_philosophy()` returns an empty quote

## The Problem: Non-Obvious Return Structure

`select_governed_philosophy()` in `runtime/philosophy.py` has a **nested** return structure. The quote is NOT at the top level — it is buried in `atlas_result.primary_quote`. Code that reads top-level `primary_quote` will silently get an empty dict every time.

**Wrong (silent failure — quote always empty):**
```python
phi_result = select_governed_philosophy(...)
phi_quote = phi_result.get("primary_quote", {})  # ALWAYS EMPTY
```

**Correct extraction:**
```python
phi_result = select_governed_philosophy(...)
phi_quote = (
    phi_result.get("atlas_result", {}).get("primary_quote", {})
    or phi_result.get("agi")
    or phi_result.get("asi")
    or phi_result.get("apex")
    or {}
)
```

## The 27-Zone Atlas Return Structure

```
phi_result
├── apex_mode: "atlas_27"
├── role: str              # "mind" | "heart" | "soul"
├── stage: str             # e.g. "444"
├── g_score: float
├── label: str             # zone name, e.g. "Humble Sovereign"
├── label_source: "atlas_27"
├── is_pseudo: False
│
├── atlas_result: {
│   ├── motto: str
│   ├── primary_quote: {   # <-- quote lives HERE (not at top level)
│   │   ├── quote_id: "Z01-Q01"
│   │   ├── quote: "You have power over your mind..."
│   │   ├── author: "Marcus Aurelius"
│   │   ├── source: "Meditations"
│   │   ├── year: 180
│   │   ├── zone_id: "Z01"
│   │   └── ...
│   └── zone: {            # zone info also nested here
│       ├── id: "Z01"
│       ├── name: "Humble Sovereign"
│       ├── S: 1, G: 1, Omega: 1
│       └── ...
└── }
```

Zone extraction (also wrong if you look at top level):
```python
atlas_zone = phi_result.get("atlas_result", {}).get("zone", {})
# NOT: phi_result.get("zone", {})  ← wrong, always empty
```

## Where to Wire It

`_enforce_nine_signal()` in `runtime/tools.py` — the single choke point wrapping all 13 canonical tool responses. This is the right place because every tool passes through here.

The philosophy call must be wrapped in `try/except` — it is non-fatal and must never crash a tool response.

## Verified Working Code

```python
try:
    g_proxy = 0.85 if (healthy and verdict_str == "SEAL") else 0.50
    delta_s_proxy = -0.01 if healthy else 0.01

    phi_result = select_governed_philosophy(
        context=tool_name,
        stage=session_stage,
        verdict=verdict_str,
        g_score=g_proxy,
        failed_floors=enforced.get("_violations", []) or [],
        session_id=session_id or "global",
        delta_s=delta_s_proxy,
        omega_score=0.05,
    )

    phi_quote = (
        phi_result.get("atlas_result", {}).get("primary_quote", {})
        or phi_result.get("agi")
        or phi_result.get("asi")
        or phi_result.get("apex")
        or {}
    )

    if phi_quote and phi_quote.get("quote"):
        atlas_zone = phi_result.get("atlas_result", {}).get("zone", {})
        enforced["philosophical_anchor"] = {
            "quote_id": phi_quote.get("quote_id", "NONE"),
            "text": phi_quote.get("quote", ""),
            "author": phi_quote.get("author", "arifOS"),
            "source": phi_quote.get("source", ""),
            "zone": atlas_zone.get("name", "Unknown"),
            "zone_id": atlas_zone.get("id", "Z??"),
            "atlas_mode": phi_result.get("apex_mode", "atlas_27"),
        }
except Exception:
    # Non-fatal: philosophy injection must never crash a tool response
    pass
```

## Verification

```python
from arifosmcp.runtime.philosophy import select_governed_philosophy

phi = select_governed_philosophy(
    context="arif_mind_reason", stage="444", verdict="SEAL",
    g_score=0.85, failed_floors=[], session_id="global",
    delta_s=-0.01, omega_score=0.05,
)

quote = phi.get("atlas_result", {}).get("primary_quote", {})
assert quote.get("quote"), "Quote empty — wrong extraction path"
print(quote["quote"], "|", quote["author"], "|", quote["zone_id"])
# → "You have power over your mind... | Marcus Aurelius | Z01"
```

## Key Files
| File | Role |
|------|------|
| `arifosmcp/runtime/philosophy.py` | `select_governed_philosophy()`, `PHILOSOPHY_ATLAS` (27 zones, 135 quotes), `select_atlas_philosophy()` |
| `arifosmcp/runtime/tools.py` | `_enforce_nine_signal()` — choke point for all 13 tools |
| `arifosmcp/runtime/tools_internal.py` | Separate RuntimeEnvelope system (NOT the canonical 13 tools) |
| `arifosmcp/runtime/philosophy_registry.py` | Per-tool philosophy registration |

## Sessions Where This Was Learned
- 2026-05-03: Audit of LLM wiring + philosophical quotes in arifOS MCP. Found that quotes were wired in `tools_internal.py` but NOT in the 13 canonical tools. Also found `select_governed_philosophy()` returns empty `primary_quote` at top level — actual quote is at `atlas_result.primary_quote`. Quote selection based on: verdict type, g_score, session_stage, delta_s, omega_score.
