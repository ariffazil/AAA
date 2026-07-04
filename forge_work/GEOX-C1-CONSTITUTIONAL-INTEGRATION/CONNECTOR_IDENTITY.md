# 01-connector-identity-propagation

**Sub-forge ID:** 01-connector-identity-propagation
**Parent forge:** GEOX-C1-CONSTITUTIONAL-INTEGRATION
**Priority:** P0 — ship first
**Status:** SPEC DRAFT
**Created:** 2026-06-06

---

## Problem

The OpenClaw GEOX connector drops caller identity. Every `geox_*` tool call returns:
- `session_id: "geox-no-session"`
- `actor_id: "geox-unknown"`

Constitutional chains cannot form. F1 (Amanah) cannot track per-session provenance. F11 (Authority) cannot verify caller authority. F13 (Sovereignty) cannot enforce per-actor floors.

**Live receipt (2026-06-06T14:06Z):**
```json
{
  "audit_receipt": {
    "vault999_ref": "VAULT999-PENDING",
    "session_id": "geox-no-session",
    "actor_id": "geox-unknown",
    "trace_id": "trace-06da059dfa424b9e"
  }
}
```

## Goal

Modify the OpenClaw GEOX connector to:
1. Read caller identity from the arifOS session envelope (or from explicit tool arguments).
2. Inject `session_id` and `actor_id` into every outbound GEOX call.
3. Preserve the GEOX-generated `trace_id` (good as-is) but link it to the caller's `parent_trace_id` if present.

## Design

### Input source (priority order)

| Priority | Source | Field | Example |
|---|---|---|---|
| 1 | Explicit tool argument | `session_id` / `actor_id` | `geox_query_intake(query="...", session_id="SEAL-04a16cf...")` |
| 2 | arifOS session binding (if running in sealed session) | from `arif_session_init` envelope | `SEAL-04a16cf53264461c` |
| 3 | OpenClaw workspace context | `/root/.openclaw/workspace/SUBSTRATE.md` actor_id | `arif-fazil-af-forge` |
| 4 | **FALLBACK** | connector hardcoded `actor_id: "openclaw-default"` (NOT `"unknown"`) | `openclaw-default` |

**Do NOT default to `"unknown"` or `"geox-unknown"`.** If no identity is available, fail closed with `888_HOLD` (consistent with arifOS strict-schema discipline).

### Output contract

Every GEOX response must echo the identity fields:

```json
{
  "session_id": "<caller's session_id, or 888_HOLD if absent>",
  "actor_id": "<caller's actor_id, or 888_HOLD if absent>",
  "trace_id": "<GEOX-generated, preserved>",
  "parent_trace_id": "<caller's trace_id, or null>"
}
```

### Backward compatibility

If a caller does NOT provide identity (legacy call), the connector must:
- Log a warning: `WARN: GEOX call without identity — falling back to 888_HOLD`
- Return `888_HOLD` with reason `"MISSING_CALLER_IDENTITY"`
- Do NOT silently fill in `"unknown"` — that masks the gap

This is consistent with arifOS `arif_judge_deliberate` strict-schema discipline.

## Implementation sketch

**File:** `connectors/geox/identity_propagation.py` (new, ~80 lines)

```python
def propagate_identity(tool_args, session_context):
    """Inject session_id and actor_id from session context into tool args."""
    if "session_id" not in tool_args:
        if session_context.sealed:
            tool_args["session_id"] = session_context.session_id
        else:
            raise IdentityMissing("888_HOLD: session_context not sealed")
    if "actor_id" not in tool_args:
        if session_context.actor_id:
            tool_args["actor_id"] = session_context.actor_id
        else:
            raise IdentityMissing("888_HOLD: actor_id not in session context")
    if "parent_trace_id" not in tool_args and session_context.trace_id:
        tool_args["parent_trace_id"] = session_context.trace_id
    return tool_args
```

**Wire-up:** `connectors/geox/__init__.py` (modify, ~10 lines) — call `propagate_identity()` before every outbound GEOX call.

## Acceptance criteria

1. **W0 self-report:** `geox_system_registry_status` returns the new envelope schema (with `actor_id` + `session_id` echoed).
2. **W1 raw probe:** Direct JSON-RPC to port 18081 with `session_id="SEAL-test01"` and `actor_id="arif-fazil-af-forge"` returns those exact values in the response envelope.
3. **W2 connector probe:** Calling `geox_query_intake(query="test", session_id="SEAL-01", actor_id="arif-fazil")` from OpenClaw returns the same values.
4. **Failure mode:** Calling without identity returns `888_HOLD: MISSING_CALLER_IDENTITY` (not `"unknown"`).
5. **Constitutional chain test:** Two calls in the same session share `session_id` but have distinct `trace_id`s. Both share the same `parent_trace_id` if call 1's `trace_id` is passed as `parent_trace_id` in call 2.

## Reversibility

✅ All changes are in the OpenClaw connector (tactical bridge, sunset epoch-2026.09).
- Rollback: revert `connectors/geox/__init__.py` and delete `connectors/geox/identity_propagation.py`.
- No federation contract change.
- No GEOX substrate change.

## Sunset policy

This sub-forge is part of the **OpenClaw connector tactical bridge** (sunset epoch-2026.09). After sunset, the connector either:
- (a) Is replaced by native GEOX-as-arifOS-organ (identity propagation is a GEOX substrate feature, not a connector shim).
- (b) Is retired and GEOX is called directly from arifOS / A-FORGE / Hermes.

Either way, the identity propagation contract survives — only the implementation layer changes.

## Out of scope

- Does not change GEOX substrate. The connector is the only modification point.
- Does not add new identity fields. Just propagates `session_id`, `actor_id`, `parent_trace_id`.
- Does not touch the `constitution_hash` field. That's sub-forge 02.
- Does not add a Vault write. That's sub-forge 04.

---

**Status:** DRAFT — awaiting Arif review and seal.
**Pairs with:** 03-registry-drift-fix (can ship same day).
**Blocks:** Sub-forges 02, 04, 05 depend on identity propagation working.
