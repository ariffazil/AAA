# 01-bridge — `arif_kernel_route(mode="manifest")` tactical bridge

**Sub-forge of:** C1-MCP-NATIVE-SURFACE
**Priority:** P1
**Reversible until:** GREEN-SEAL of full forge C1-MCP-NATIVE-SURFACE
**Sunset epoch:** epoch-2026.09 (hard expiry — must migrate to MCP-native resources in sub-forge 02)
**Spec version:** v2026.06
**Spec author:** arif-fazil-af-forge (session SEAL-91e12b6644f64589)

---

## Problem

`arif_session_init` advertises an internal resource manifest at `resource://agent/capabilities/raw`. The advertised read path is `arif_evidence_fetch`, but `arif_evidence_fetch` rejects `resource://` URLs under F12:

```json
{
  "verdict": "HOLD",
  "reasons": ["Constitutional gate blocked: 1 validation error for ActionContext\nurl\n  Value error, Invalid URL scheme: resource://agent/capabilities/raw"],
  "failed_floors": ["F12"]
}
```

This is a **contract mismatch**: the manifest is advertised but not fetchable. Result: federation consumers cannot read the raw manifest, and downstream tools (GEOX/WEALTH/WELL) have no canonical reference for the arifOS surface.

## Non-negotiable constraint

**Do NOT broaden `arif_evidence_fetch` to accept `resource://` URLs.**

That handler is for **external evidence with provenance** (F12). Internal resources are a different namespace. Broadening it would weaken F12 — a constitutional regression, not a fix.

## Solution

Add a new safe mode `manifest` to the existing tool `arif_kernel_route`. The tactical bridge:

- Lives inside an existing tool (no MCP server contract change)
- Has a sunset epoch baked in (must migrate in sub-forge 02)
- Inherits the existing `arif_kernel_route` permission envelope (read-only, no side effects)
- Does not touch `arif_evidence_fetch` or F12

## Schema (canonical)

```yaml
tool: arif_kernel_route
new_mode: manifest
version: v2026.06
sunset_epoch: epoch-2026.09

allowed_fields:
  mode:
    type: str
    required: true
    fixed_value: "manifest"
    description: "Required, must be 'manifest'. Other values → 888_HOLD (F10)."
  resource:
    type: str
    required: true
    default: "agent/capabilities/raw"
    description: "Canonical resource key (allowlisted). Non-allowlisted → 888_HOLD."
    allowlist:
      - "agent/capabilities/raw"
      - "arifos/constitution"
      - "arifos/policy"
      - "arifos/tool-registry"
      - "arifos/floors"
      - "arifos/prompts"
      - "arifos/health"
      - "arifos/attestation"
      - "arifos/floor-status"
      - "arifos/audit/{session_id}"
    reject_list:
      - "evidence/external/*"   # F12 — must go through arif_evidence_fetch
      - "arifos/secrets"         # not in allowlist
      - "arifos/private-keys"    # not in allowlist
  session_id:
    type: str
    required: true
    format: "^SEAL-[a-f0-9]{16}$"
    description: "Canonical SEAL-* session ID from arif_session_init."
  actor_id:
    type: str
    required: true
    description: "Claimed actor identity. Verified by arifOS, not by this tool."

safe_modes_for_this_route:
  - manifest    # read-only, no side effects, no authority escalation

dangerous_modes_for_this_route: []    # none — this is a pure read

requires_ack_irreversible: false
requires_judge_state_hash: false

response_schema:
  resource_uri: str              # canonical resource:// URI
  content: object                # resource contents (typed per resource)
  content_hash: str              # sha256 of content
  fetched_at: str                # ISO-8601 timestamp
  session_id: str
  actor_id: str
  verdict: str                   # SEAL | HOLD
  reasons: [str]
```

## Example valid calls

```json
// Default: read the raw capabilities manifest
{
  "mode": "manifest",
  "session_id": "SEAL-91e12b6644f64589",
  "actor_id": "arif-fazil-af-forge"
}
```

```json
// Explicit: read the constitution
{
  "mode": "manifest",
  "resource": "arifos/constitution",
  "session_id": "SEAL-91e12b6644f64589",
  "actor_id": "arif-fazil-af-forge"
}
```

```json
// Audit trace for a specific session
{
  "mode": "manifest",
  "resource": "arifos/audit/SEAL-91e12b6644f64589",
  "session_id": "SEAL-91e12b6644f64589",
  "actor_id": "arif-fazil-af-forge"
}
```

## Example rejected calls

```json
// Missing session_id → 888_HOLD (F10 strict-schema)
{
  "mode": "manifest",
  "actor_id": "arif-fazil-af-forge"
}
```

```json
// External evidence — must use arif_evidence_fetch → 888_HOLD (F12)
{
  "mode": "manifest",
  "resource": "evidence/external/https://example.com/paper.pdf",
  "session_id": "SEAL-91e12b6644f64589",
  "actor_id": "arif-fazil-af-forge"
}
```

```json
// Resource not in allowlist → 888_HOLD
{
  "mode": "manifest",
  "resource": "arifos/secrets",
  "session_id": "SEAL-91e12b6644f64589",
  "actor_id": "arif-fazil-af-forge"
}
```

```json
// Wrong mode value → 888_HOLD (F10)
{
  "mode": "manifest_v2",     // ← unknown mode
  "session_id": "SEAL-91e12b6644f64589",
  "actor_id": "arif-fazil-af-forge"
}
```

## Migration path (sunset policy)

| Date | Action | Reversible? |
|---|---|---|
| 2026-06 (now) | Ship tactical bridge. `manifest` mode added to `arif_kernel_route`. | ✅ |
| 2026-07 | First deprecation warning in tool response metadata. | ✅ |
| 2026-08 | Sub-forge 02 ships MCP-native `resources/list` + `resources/read`. Bridge enters deprecation mode. | ✅ |
| 2026-09 (sunset epoch) | Tactical bridge mode is **removed**. Federation must use MCP-native primitives. | ⚠️ **Point of no return for the bridge.** |

**The sunset epoch is a hard field in the spec. It is not "we'll add it later."** Without a sunset, tactical bridges become permanent debt.

## Test cases

| # | Test | Expected | Floor |
|---|---|---|---|
| 1 | `mode=manifest, resource=agent/capabilities/raw` | SEAL, returns manifest | — |
| 2 | `mode=manifest, resource=arifos/constitution` | SEAL, returns constitution | — |
| 3 | `mode=manifest, resource=evidence/external/*` | HOLD | F12 |
| 4 | `mode=manifest, resource=arifos/secrets` | HOLD | F10 |
| 5 | `mode=manifest, session_id` missing | HOLD | F10 |
| 6 | `mode=manifest, actor_id` missing | HOLD | F10 |
| 7 | `mode=manifest_v2` (unknown mode) | HOLD | F10 |
| 8 | `mode=manifest, session_id="INVALID-FORMAT"` | HOLD | F10 |
| 9 | `arif_evidence_fetch(url="resource://...")` (post-bridge, regression check) | HOLD | F12 (unchanged) |
| 10 | `arif_kernel_route(mode=list)` still returns 13 tools (no regression) | SEAL | — |

## Acceptance criteria

1. All 10 test cases pass.
2. Manifest content returns with verified `content_hash` (sha256 of expected manifest).
3. `arif_evidence_fetch` F12 boundary unchanged (regression test 9 passes).
4. `arif_kernel_route(mode=list)` still returns 13 tools (regression test 10 passes).
5. `docs/MCP_CONTRACTS.md` updated with the new `manifest` mode entry.
6. `forge_work/C1-MCP-NATIVE-SURFACE/MCP_BRIDGE_REGISTRY.json` updated with the new bridge entry and sunset epoch.

## Rollback plan

Single-mode addition. To rollback:
1. Remove the `manifest` mode from `arif_kernel_route` allowlist.
2. Remove the bridge entry from `MCP_BRIDGE_REGISTRY.json`.
3. Revert the `docs/MCP_CONTRACTS.md` change.

**Zero state change.** No data migration. No federation consumer notification (the bridge is opt-in by callers, no caller was required to adopt it).

## Sealing

When Arif signs off on this spec:

1. Spec is sealed via `arif_vault_seal` with `ack_irreversible=true` and `judge_state_hash` from prior SEAL judgment.
2. `arif_forge_execute(mode=engineer, plan_id="C1-MCP-NATIVE-SURFACE/01-bridge")` lands the code.
3. Test cases run. Acceptance criteria verified.
4. Sub-forge marked SEALED in the forge work manifest.

---

**Status:** DRAFT — awaiting Arif review and seal.
**Next action:** Generate sub-forge 02-prompts-resources spec, then 03-mindreason, 04-fl-naming, 05-contract-tests.
