# Sovereign Backlog — Substrate Drift Catalogue

**Date:** 2026-07-14
**Author:** 777_FORGE (acting under sovereign signal "a b then seal")
**Status:** ACTIVE — 5 drifts confirmed live, 1 fixed, 4 awaiting sovereign ack
**Related:** `/root/AAA/contracts/FEDERATION_CONTRACT.yaml`, `/root/AAA/tests/federation_conformance_result.json`

---

## P0 — MCP Gateway / Kernel Identity Propagation

### Drift #1: GEOX session_id=anonymous
**Discovered:** 2026-07-14T16:07Z
**Tool:** `geox_geox_basin(mode=profile)`, `geox_geox_prospect(mode=screen)`
**Symptom:** Pass `session_id=SEAL-cf670a9b5b0a4e25` + `actor_id=ARIF` → response shows `session_id="anonymous"`, `actor_id=None`
**Impact:** All GEOX evidence not bound to sovereign session. Audit trail broken. Cannot trace which session produced which evidence.
**Root cause:** MCP gateway strips session envelope at boundary (or upstream doesn't honor it)
**Severity:** HIGH
**Sovereign action required:** Inspect MCP gateway session propagation code. Fix at boundary OR in GEOX server receive path.

### Drift #3: arifOS actor_verified=false on existing session
**Discovered:** 2026-07-14T16:13Z
**Tool:** `arif_think(mode=plan)` with `session_id=SEAL-cf670a9b5b0a4e25`
**Symptom:** Session init at 15:40Z returned `actor_verified=true`. Same session 33 minutes later returns `actor_verified=false`. TTL 3600s not expired.
**Impact:** F2 TRUTH binding broken mid-session. Reasoning carries "_ATTENTION: IDENTITY_NOT_VERIFIED" warning. Cannot trust verdict provenance.
**Root cause:** Verification state not persisted across MCP gateway hops OR re-verification required per-tool-call
**Severity:** HIGH
**Sovereign action required:** Either (a) persist verification token across calls, or (b) require explicit re-init per tool invocation (then update call sites)

---

## P1 — Capability Registration

### Drift #2: geox_claim create → KERNEL_DENY
**Discovered:** 2026-07-14T16:07Z
**Tool:** `geox_geox_claim(mode=create)`
**Symptom:** Returns `KERNEL_DENY: Capability not registered`
**Impact:** Cannot create canonical claims through GEOX. Evidence cannot be sealed as claim.
**Root cause:** Capability graph missing `geox_claim create` registration, OR GEOX server doesn't expose `create` mode
**Severity:** HIGH
**Sovereign action required:** Register `geox_claim create` capability OR remove `create` mode from public surface contract

### Drift #5: geox_claim evidence → JUDGMENT_LANE routing
**Discovered:** 2026-07-14T16:13Z
**Tool:** `geox_geox_claim(mode=evidence)`
**Symptom:** Returns `JUDGMENT_LANE_DIRECT_CALL: Tool 'geox_claim' is classified as JUDGMENT lane. MUST route via arif_kernel_route(mode=bridge, organ=geox, tool_name='geox_claim')`
**Impact:** Direct MCP call to judgment-lane tools blocked. Forces indirect routing.
**Root cause:** Lane classification enforcement at MCP boundary
**Severity:** MEDIUM (workaround exists: route via arif_route)
**Workaround attempted:** `arif_route(intent=..., organ=geox, organ_tool=geox_claim, arguments=...)` — testing whether arif_route provides the required bridge semantics
**Sovereign action required:** Confirm whether routing via arifOS as bridge preserves constitutional judgment semantics, OR if direct-call enforcement is the intended invariant

---

## P2 — Caller Schema Discipline

### Drift #4: arif_think rejected `intent` kwarg
**Discovered:** 2026-07-14T16:13Z (parallel agent session)
**Tool:** `arif_think(mode=plan)` called with `intent=...`
**Symptom:** `_arif_mind_reason_tool() got an unexpected keyword argument 'intent'`
**Impact:** Caller schema mismatch causes silent failure
**Root cause:** Caller used generic `intent` param (valid for `arif_init`) but `arif_think` expects `query`
**Severity:** LOW (caller-side error)
**Status:** ✅ FIXED — use `query` parameter for arif_think
**Sovereign action:** None (caller discipline)

---

## P3 — Audit Trail Impact

When drifts #1 and #3 both fire on the same call:
1. GEOX returns `session_id="anonymous"` (drift #1)
2. arifOS reasoning shows `actor_verified=false` (drift #3)
3. Result: Evidence chain unprovable. F2 TRUTH unanchored. F11 AUDIT incomplete.

**This is the most operationally serious combination.** Without sovereign fix, every cross-organ evidence pull is untrustworthy for SEAL-grade verdicts.

---

## Recommended Sovereign Sequence

1. **Fix MCP gateway session propagation** (drift #1) — single most impactful change
2. **Persist actor_verified across tool calls** (drift #3) — second most impactful
3. **Register or remove geox_claim create** (drift #2) — capability surface contract fix
4. **Document arif_route vs arif_kernel_route distinction** (drift #5) — clarification only
5. **None for drift #4** — caller-side fix only

---

## Provenance

- Author: 777_FORGE
- Session: SEAL-cf670a9b5b0a4e25 (drift #3 + #5 confirmed)
- Discovery sessions: 2026-07-14T16:07Z (drifts #1, #2), 16:13Z (drifts #3, #4, #5)
- Discovery agents: FORGE (me), parallel GPT-5.6 session
- Authoritative source: this file + `/root/AAA/tests/federation_conformance_result.json`

---

## UPDATE 2026-07-14T16:15Z — Drift #6 discovered via arif_route bridge

### Drift #6: GEOX MCP lifecycle gate not honored
**Discovered:** 2026-07-14T16:15Z
**Tool:** `arif_route(intent=..., organ=geox, organ_tool=geox_claim, arguments=...)`
**Symptom:** Bridge invokes GEOX via `arif_bridge` → GEOX returns `MCP_LIFECYCLE: tools/call rejected until client sends notifications/initialized after initialize. Sequence: initialize → notifications/initialized → tools/call. (GEOX Phase A1 lifecycle gate)`
**Positive finding:** The bridge path CORRECTLY preserves identity:
```
bridge_session_id: SEAL-cf670a9b5b0a4e25
bridge_actor_id: ARIF
drift_detected: false
```
But GEOX server itself rejects the call because the MCP protocol lifecycle (initialize → notifications/initialized → tools/call) was not completed.
**Impact:** Even when identity is correctly bridged, GEOX server requires explicit lifecycle handshake. Most MCP clients skip `notifications/initialized` and go straight to `tools/call`, which works on most servers but breaks on GEOX Phase A1.
**Severity:** MEDIUM-HIGH (workaround exists if arif_route bridge completes the lifecycle)
**Sovereign action required:** Either (a) relax GEOX Phase A1 lifecycle gate to accept tools/call after initialize, or (b) update arif_route bridge to send notifications/initialized before tools/call

### Key Insight from bridge attempt
- Direct MCP call: identity stripped (drift #1) → GEOX treats as anonymous
- arif_route bridge: identity preserved → GEOX receives correctly → but blocks on lifecycle
- The kernel's `_ATTENTION: IDENTITY_NOT_VERIFIED` warning fires even on bridge success because the outer envelope computes `actor_verified=false` from session age/init count, not from the bridge payload's verified identity

---

## UPDATED COUNT: 6 substrate drifts confirmed live, 1 fixed

| # | Drift | Severity | Status |
|---|---|---|---|
| 1 | GEOX session_id=anonymous (direct MCP) | HIGH | UNFIXED |
| 2 | geox_claim create → KERNEL_DENY | HIGH | UNFIXED |
| 3 | arifOS actor_verified=false mid-session | HIGH | UNFIXED |
| 4 | arif_think rejected `intent` kwarg | LOW | ✅ FIXED (use `query`) |
| 5 | geox_claim → JUDGMENT_LANE | MEDIUM | UNFIXED (workaround: bridge) |
| 6 | GEOX MCP lifecycle gate (initialize→initialized→tools/call) | MEDIUM-HIGH | UNFIXED |

DITEMPA BUKAN DIBERI — drift surfaced, not given.
