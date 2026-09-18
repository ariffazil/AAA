# SURFACE-CONFORMANCE PROBE — 2026-09-18
> Host: KVM8 (forge, 100.64.0.2) · Deployed: `kanon-2026.09.17+eff8a59` · Method: live MCP wire calls

## Verdict on the external audit

**Directionally right, mislocated.** The audit's *conclusion* (surface divergence is real and
governance-relevant) holds. Its *diagnosis* (the public MCP surface is broken) does not.

The public surface is clean. The audit's client was reading a **stale cached tool list**.

## A. MCP wire `tools/list` — CORRECT (the surface clients actually use)

| Tool | Stage live | Canon (`CORE_NINE_STAGE_MAP`) | Match |
|---|---|---|---|
| arif_init | 000 | 000 | ✓ |
| arif_observe | 111 | 111 | ✓ |
| arif_think | 333 | 333 | ✓ |
| arif_route | 444 | 444 | ✓ |
| arif_memory | 555 | 555 | ✓ |
| arif_judge | 666 | 666 | ✓ |
| arif_forge | 777 | 777 | ✓ |
| arif_seal | 999 | 999 | ✓ |

Count = 8 = `KERNEL_ABI_8`. All callable — arif_init, arif_observe, arif_seal exercised live
this session. Public endpoint `mcp.arif-fazil.com` serves the identical 8. **No defect here.**

## B. The audit's 17 names — not advertised anywhere live

Dispatched the audit's names against the live server:

| Name | Live result |
|---|---|
| arif_session_init | **resolves** → aliased to `arif_init`; returns HOLD, actor `{}`, session `null` — resolves but does not work |
| arif_gateway_connect | **resolves** → aliased to `arif_bridge_connect`; `2 validation errors … organ: Missing required argument` — audit's schema-mismatch finding CONFIRMED |
| arif_sense_observe | `Unknown tool` |
| arif_stack_health_probe | `Unknown tool` |

So: a **partial legacy alias residue** exists server-side (some old names map, most don't),
and the client's cached list supplies the rest. The names are not in `tools/list`, not in
`peer-contract.json` (which carries the canonical 8 + RFC8785-JCS semantic hash), not on the
public endpoint.

**Cause:** MCP clients cache `tools/list` at connect time. A client connected before the
8-verb migration keeps dispatching pre-migration names. Not a server-side surface defect.

## C. CONFIRMED defects (real, reproduced live)

### C1 — BOOT_ATTESTATION_FAILED with drift=false (P0/P1)
```
source_commit  = eff8a59e3188cdda81a4dfdae0634c446a4fa36a
deployed_commit= eff8a59e3188cdda81a4dfdae0634c446a4fa36a
drift          = false
effective_state.session_authority_state = "BOOT_ATTESTATION_FAILED"
effective_state.substrate_state         = "DEGRADED"
```
Commit equality holds, yet boot attestation fails. The attestation chain checks something
beyond commit equality (wheel hash / runtime manifest / canon version). **Root cause NOT
established — UNMEASURED.** Audit claim reproduced exactly.

### C2 — Substrate triple-contradiction in one envelope (P0) — K6 reproduced, worse
One `arif_init` response carries **three** substrate readings:
```
top-level  substrate.state            = "HEALTHY"   (source: runtime_attestation_injected)
result     .substrate.state           = "DEGRADED"
effective_state.substrate_state       = "DEGRADED"
```
Earlier (58e5740) this was two readings; now it is three. Same envelope, two truths.
This is the live instance of the audit's Critical Blocker #1 (one request, two interpretations).

### C3 — HTTP `/tools` stage projection wrong for 4 of 8 (P2)
The HTTP convenience endpoint (`/tools`, local and public) reports stages that disagree with
both canon and the MCP wire surface:
```
arif_route  = "555"   (canon 444)
arif_memory = "555m"  (canon 555)
arif_judge  = "888"   (canon 666 — and 888 is explicitly DEPRECATED in constitutional_map)
arif_forge  = "010"   (canon 777)
```
`tools/list` is correct; `/tools` is stale. A second view telling a different truth —
third surface divergence found tonight.

### C4 — Legacy alias residue (P2)
Partial old-name dispatch layer. Inconsistent by construction: some names resolve, most
return `Unknown tool`. Either complete the translation or remove the aliases; a partial
alias surface is a false affordance either way.

## D. NOT reproduced / corrected

| Audit claim | Finding |
|---|---|
| "Public capability manifest broken, 1/17" | Measured against a stale client cache, not the live surface. Live: 8/8 correct |
| "connector advertises arif_session_init, arif_sense_observe…" | No live surface advertises these. Client-side cache |
| "allowed_next_verbs uses older compact verbs" | The 6 listed ARE canonical (subset of KERNEL_ABI_8). Audit inverted: the *compact* verbs are the current ones |
| "memory engineering is the priority" | Audit's own retraction is correct — memory was never the issue |
| OpenClaw: "live surface has no kernel 888" | KVM4 stale-mirror artifact. Live `tools/list` = `arif_judge` stage 666, description "KERNEL 666" |

## E. Corrected priority

1. **C2 substrate triple-contradiction** — governance/verifier territory → **888 HOLD.** Prepare patch proposal, F13 decides. Must not be self-patched.
2. **C1 BOOT_ATTESTATION_FAILED** — root cause probe first (cheapest single check: compare wheel_hash + runtime_manifest_hash against the attested root). Governance → HOLD.
3. **C3 /tools stage projection** — display-only, cheap, safe. Can be a Wave-1 item.
4. **C4 alias residue** — decide: remove or complete. F13 call on intent; mechanical either way.
5. **Distribution:** legacy `arifosmcp` on PyPI remains publicly installable with the old
   architecture — that is the upstream source of stale surfaces. Deprecate/tombstone.

## F. UNMEASURED in this probe

- Root cause of BOOT_ATTESTATION_FAILED
- Full 17-name alias sweep (4 of 17 tested)
- Which client/connector produced the audit's cached list
- Whether `/tools` is consumed by any live component (if none, delete it)

## G. Coordination note

Writer on this repo is **kimi-code/FI-008** (commits 21:04→00:37 tonight, including the
entropy audit). Any patch must race-check against FI-008 and target the deployed wheel path
(`build→wheel→deploy→/opt/arifos/current/venv`), never the moving checkout.
