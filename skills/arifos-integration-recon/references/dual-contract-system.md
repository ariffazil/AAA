# Dual Contract System — Three Layers of arifOS Tool Contracts

The arifOS kernel uses THREE independent contract dictionaries that all describe the same tools. They MUST agree, but they often don't — these are the primary source of contradictions.

## The three layers

| Layer | Location | Purpose | When consulted |
|-------|----------|---------|----------------|
| `TOOL_PURPOSE_CONTRACTS` | `runtime/tools.py` ~line 617 | Human-readable: `purpose`, `use_when`, `do_not_use_when`, `agency_level` | Tool discovery, charter rendering |
| `TOOL_AFFORDANCE_CONTRACTS` | `runtime/tools.py` ~line 1254 | Machine-gated: `action_class`, `irreversible`, `requires_human_ack`, `safe_autonomous_use` | Verdict derivation, affordance narrowing |
| `MODE_AFFORDANCE_OVERRIDES` | `runtime/tools.py` ~line 2085 | Per-mode overrides applied AFTER base contract lookup | Envelope surface only (NOT verdict path) |

## How they relate

```python
# Pseudocode of _get_affordance_contract(tool_name, mode=None)
contract = dict(TOOL_AFFORDANCE_CONTRACTS[tool_name])  # base
if mode and mode in MODE_AFFORDANCE_OVERRIDES.get(tool_name, {}):
    contract.update(MODE_AFFORDANCE_OVERRIDES[tool_name][mode])  # override
return contract
```

`TOOL_PURPOSE_CONTRACTS` is parallel — it's not merged into the affordance contract; it feeds a separate documentation/rendering pipeline.

## Known contradictions (as of 2026-08-06 investigation)

### 1. D4 mode override missing from verdict path (CRITICAL)

`MODE_AFFORDANCE_OVERRIDES` is consulted in TWO places:

```python
# Place A: verdict derivation (tools.py ~line 2742, inside _compute_canonical_verdict Step 6)
affordance = _get_affordance_contract(tool_name)          # NO mode parameter
verdict = _derive_affordance_verdict(tool_name, verdict, affordance)

# Place B: envelope surface (tools.py ~line 4844, inside _enforce_nine_signal)
affordance_contract = _get_affordance_contract(
    tool_name, mode=out.get("mode") if isinstance(out, dict) else None
)  # HAS mode parameter
```

**Effect**: For `arif_seal(mode=verify_chain)`:
- Envelope shows `action_class: "OBSERVE"` (mode override applied) ✓
- Verdict derivation uses `action_class: "SEAL"`, `irreversible: True` (base contract only) ✗
- `_derive_affordance_verdict` never narrows when `irreversible=True`, so the read-only mode stays over-gated

**Fix sketch**: thread `mode` through `_compute_canonical_verdict` → `_get_affordance_contract(tool_name, mode)`.

### 2. arif_memory write modes not in MODE_AFFORDANCE_OVERRIDES

`MODE_AFFORDANCE_OVERRIDES["arif_memory"]` only has read modes (`recall`, `inspect`, `attest`). Write modes (`remember`, `promote`, `revise`, `forget`) fall through to the OBSERVE base contract despite being genuine mutations.

Base contract (line 1657):
```python
"arif_memory": {
    "action_class": "OBSERVE",
    "mutation": False,
    ...
}
```

Internal gating exists in the handler (`_arif_memory_v5_router`), but the affordance system treats writes as reads.

**Fix sketch**: Either add EXECUTE-class entries for write modes, or flip the base to `MUTATE` and add OBSERVE overrides for read modes.

### 3. arif_seal `action_class: "SEAL"` is non-canonical

Canonical `action_class` values per the affordance system are: `OBSERVE`, `ANALYZE`, `DRAFT`, `EXECUTE`. But `TOOL_AFFORDANCE_CONTRACTS["arif_seal"]` (line 1683) declares `action_class: "SEAL"`. The verdict narrowing logic at `_derive_affordance_verdict` checks for `action_class == "EXECUTE"` to skip narrowing — `"SEAL"` falls through to the OBSERVE/irreversible branches with subtle effects.

## Investigation pattern

When investigating a contract contradiction:

1. `grep -n '"action_class"' arifosmcp/runtime/tools.py | head -50` — find all declarations
2. For the tool in question, check if `TOOL_PURPOSE_CONTRACTS`, `TOOL_AFFORDANCE_CONTRACTS`, and `MODE_AFFORDANCE_OVERRIDES` agree on `action_class`, `irreversible`, `mutation`, `requires_human_ack`
3. Check both callsites of `_get_affordance_contract` — does the mode propagate?
4. Check `_derive_affordance_verdict` (line 2237) — what narrowing rules apply?

## Related reading

- `references/dual-verdict-paths.md` — how the wrapper path and judge path differ
- `references/d-series-defects-20260806.md` — D4 specifically