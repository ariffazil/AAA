# P0 arifOS Kernel Patches — MCP 2026-07-28 Alignment

**Status:** SPEC ONLY · awaiting forge authority (requires SEAL verdict + MUTATE band)
**Date:** 2026-09-29
**Author:** FI-008 (kimi-code) per sovereign directive *"ffff qqqq apex-zen all"*
**Authority band required:** LIMITED_MUTATE or MUTATE
**Reversibility:** reversible (server-side filter + new endpoint, no state mutation)
**Canon grounding:** Constitutional Architecture Canon (F13_RATIFIED_CHAT 2026-09-21); Canon #0 Complexity Budget (F13_SEAL 2026-09-21); APEX-ZEN Runtime Prompt vNext (F13_RATIFIED_CHAT 2026-09-20)

---

## 0. Verification of live scar (already done)

`arif_init mode=light` returned `session_token: "act_v1.eyJ..."` (full bearer JWT) in model-visible output. Decoded payload contains: `actor, allowed, auth, apex, exp, iat, sid, verdict, witness`. The token is echoed 3× (top-level, `result.session_token`, `meta.act_claims`). Default token is unsigned (Ed25519 challenge required for full authority).

`arif_init mode=canary` confirmed `protocol_conformant: true` but did not expose `mcp_versions_supported`. Live state is `effective_verdict: HOLD, substrate.state: DEGRADED, reason_code: DEPLOYMENT_DRIFT`. Receipt chain has gaps (`receipt_chain_valid: false, status: "gaps-found"`).

---

## 1. Patch A — REDACT_BEARER_TOKEN in output_policy

### 1.1 What

Add a new value to `output_policy` enum: `"REDACT_BEARER_TOKEN"`. When active, the server filters every `arif_*` tool response to remove:
- `session_token` (any field whose key matches `*token*` or whose value matches `^act_v\d+\.`)
- `act_claims` (full reconstructed JWT)
- `act_*` fields in `meta.*`

The model only ever sees `session_id` (opaque handle), `challenge.nonce` (server-side kept), `authority_band` (label, not capability).

### 1.2 Where

File: `/root/.arifos/arifosmcp/__init__.py` (or wherever the `arif_init` response is constructed — verify by grep).

### 1.3 Patch (pseudo-Python, ~20 lines)

```python
import re

BEARER_PATTERN = re.compile(r'^act_v\d+\.')
TOKEN_KEYS = {'session_token', 'act_claims'} | {f'act_{k}' for k in (
    'claims','actor','allowed','apex','auth','av','exp','iat','kid','lane',
    'nbf','sid','stage','ttl','verdict','witness'
)}

def redact_bearer(payload: dict) -> dict:
    """Apply REDACT_BEARER_TOKEN policy to a tool response payload."""
    out = {}
    for k, v in payload.items():
        if k in TOKEN_KEYS:
            continue
        if k == 'meta' and isinstance(v, dict):
            out[k] = {kk: vv for kk, vv in v.items() if not kk.startswith('act_')}
            continue
        if isinstance(v, str) and BEARER_PATTERN.match(v):
            continue
        if isinstance(v, dict):
            out[k] = redact_bearer(v)
        else:
            out[k] = v
    return out

def arif_init_response(...):
    response = build_response(...)
    if response.get('output_policy') == 'REDACT_BEARER_TOKEN':
        response = redact_bearer(response)
    return response
```

### 1.4 Acceptance test

```
assert 'session_token' not in response
assert 'act_claims' not in response
assert not any(isinstance(v, str) and v.startswith('act_v1.') for v in walk(response))
assert 'session_id' in response
assert response.get('output_policy') == 'REDACT_BEARER_TOKEN'
```

### 1.5 Canon #0 gate

- (a) Eliminate demonstrated failure class: ✅ removes bearer-token-in-model-context
- (b) Compile into enforceable mechanism: ✅ server-side filter, ~20 LOC
- (c) Materially improve a decision: ✅ unblocks production authority delegation without credential leak

---

## 2. Patch B — `server/discover` endpoint (MCP 2026-07-28)

### 2.1 What

New endpoint `POST /{mcp_version}/discover` that returns server metadata WITHOUT requiring `initialize` handshake or session header. Stateless. Returns:

```json
{
  "server_info": {
    "name": "arifOS",
    "version": "arifos-bceb6f2ef0ee",
    "build_commit": "b9eeec7e6f3c0776233369e112483b6985411e4b"
  },
  "capabilities": {
    "tools": {"listChanged": false},
    "resources": {"subscribe": false, "listChanged": false},
    "prompts": {"listChanged": false},
    "tasks": {"supported": true, "long_running": ["arif_judge","arif_forge","arif_seal","arif_stage"]},
    "logging": {"supported": true}
  },
  "mcp_versions_supported": ["2026-07-28", "2025-11-25", "2025-03-26"],
  "mcp_versions_default": "2026-07-28",
  "tools": ["arif_init","arif_observe","arif_think","arif_route","arif_memory","arif_judge","arif_forge","arif_seal","arif_stage"],
  "constitutional_reference": "arifos-constitution-v2026.05.05-SSCT",
  "constitution_hash": "sha256:c65465c98bc2cfa0",
  "kernel_epoch": "2026-07-03",
  "deprecation_warnings": []
}
```

### 2.2 Where

New file: `/root/.arifos/arifosmcp/server/discover.py`
Hook into existing HTTP router.

### 2.3 Patch (pseudo-Python, ~60 lines)

```python
from fastapi import APIRouter
from arifosmcp import __version__, KERNEL_EPOCH

router = APIRouter()

@router.get("/discover")
@router.post("/discover")
async def server_discover():
    return {
        "server_info": {
            "name": "arifOS",
            "version": __version__,
            "build_commit": BUILD_COMMIT_SHA,
        },
        "capabilities": {
            "tools": {"listChanged": False},
            "resources": {"subscribe": False, "listChanged": False},
            "prompts": {"listChanged": False},
            "tasks": {
                "supported": True,
                "long_running": ["arif_judge","arif_forge","arif_seal","arif_stage"],
            },
            "logging": {"supported": True},
        },
        "mcp_versions_supported": ["2026-07-28", "2025-11-25", "2025-03-26"],
        "mcp_versions_default": "2026-07-28",
        "tools": CANONICAL_NINE,
        "constitutional_reference": CONSTITUTION_REF,
        "kernel_epoch": KERNEL_EPOCH,
        "deprecation_warnings": [],
    }
```

### 2.4 Acceptance test

```
GET /discover → 200, contains mcp_versions_supported[0] == "2026-07-28"
POST /discover → 200 (idempotent)
No auth required, no session header
Response contains server_info.name == "arifOS"
Response contains tools list of length 9
```

### 2.5 Canon #0 gate

- (a) Eliminate demonstrated failure class: ✅ unifies capability advertisement
- (b) Compile into enforceable mechanism: ✅ stateless GET endpoint
- (c) Materially improve a decision: ✅ client can negotiate era before initialize

---

## 3. Patch C — Stateless `session_id`-in-body handler

### 3.1 What

Stop requiring `Mcp-Session-Id` header on modern path. Accept `session_id` as ordinary argument on every `arif_*` tool call. Server resolves `session_id` → capability store entry server-side. The transport becomes stateless; authority lives in the constitution.

### 3.2 Where

File: `/root/.arifos/arifosmcp/server/router.py` (or wherever tool dispatch happens).

### 3.3 Patch (pseudo-Python, ~40 lines)

```python
async def dispatch_tool_call(tool_name: str, arguments: dict, headers: dict):
    """Dual-path dispatch: modern accepts session_id in body, legacy uses header."""

    # Modern path (MCP 2026-07-28): session_id in body
    session_id = arguments.get("session_id") or arguments.get("constitutional_handle")

    # Legacy path: fall back to Mcp-Session-Id header
    if not session_id:
        session_id = headers.get("Mcp-Session-Id") or headers.get("mcp-session-id")

    if not session_id:
        raise JSONRPCError(-32602, "session_id required (in body or Mcp-Session-Id header)")

    # Resolve server-side — capability never enters model context
    cap = capability_store.get(session_id)
    if not cap:
        raise JSONRPCError(-32004, f"session_id {session_id!r} not found", code="RESOURCE_NOT_FOUND")

    # Verify constitutional authority for this verb
    if tool_name not in cap.allowed_verbs:
        raise JSONRPCError(-32603, f"verb {tool_name!r} not in allowed set for this session")

    # Strip session_id from arguments before dispatching to tool implementation
    tool_args = {k: v for k, v in arguments.items() if k not in ("session_id", "constitutional_handle")}

    return await invoke_tool(tool_name, tool_args, capability=cap)
```

### 3.4 Acceptance test

```
POST /mcp {tool: arif_observe, args: {session_id: "SEAL-...", ...}}  → succeeds
POST /mcp {tool: arif_observe, args: {session_id: "SEAL-..."}, headers: {Mcp-Session-Id: ...}}  → succeeds (legacy)
POST /mcp {tool: arif_observe, args: {}}  → -32602 missing session_id
POST /mcp {tool: arif_observe, args: {session_id: "FAKE-..."}}  → -32004 RESOURCE_NOT_FOUND
POST /mcp {tool: arif_observe, args: {session_id: "SEAL-...", but_authority_band: OBSERVE_ONLY}, call: arif_forge}  → -32603 verb denied
```

### 3.5 Canon #0 gate

- (a) Eliminate demonstrated failure class: ✅ removes implicit transport-state ↔ authority coupling
- (b) Compile into enforceable mechanism: ✅ dual-path dispatcher with verb ACL
- (c) Materially improve a decision: ✅ aligns with MCP 2026-07-28 stateless pattern; survives worker changes

---

## 4. Manifest

| Patch | LOC | Reversibility | Authority required | Test gate |
|---|---|---|---|---|
| A — REDACT_BEARER_TOKEN | ~20 | reversible | LIMITED_MUTATE | Q3, Q10 |
| B — server/discover | ~60 | additive | LIMITED_MUTATE | Q1 |
| C — Stateless dispatcher | ~40 | additive | MUTATE | Q5, Q6, Q8 |

Total: ~120 LOC across 3 files. Zero new dependencies. Zero state mutation. All patches are server-side and additive.

---

## 5. HOLD gates

| Gate | Why HOLD | Unblock condition |
|---|---|---|
| Forge execution | Requires MUTATE band; my session is OBSERVE_ONLY | sovereign grants via arif_init with Ed25519 signature |
| DEPLOYMENT_DRIFT | `built_commit ≠ deployed_commit`; software_release.drift=true | Reconcile source/built/deployed (separate governance, A-FORGE lane) |
| Receipt chain gaps | `receipt_chain_valid: false, status: gaps-found` | Audit + replay of /var/lib/arifos/proof_spine/* |
| Signing-lane key drift | `challenge_required: true` for full authority | F13 SOVEREIGN signature rotation |

---

## 6. EUREKA (binding to canon)

> **Transport carries capability (handle, opaque). Constitution determines authority (band, witness, freshness).**

This patch set makes the constitutional canon literal in the wire protocol. The bearer token stops being an authority object and becomes an internal capability reference; the constitution (F1-F13) remains the only authority grant.

---

DITEMPA BUKAN DIBERI ⚒️
