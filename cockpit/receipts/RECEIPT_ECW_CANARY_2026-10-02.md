# RECEIPT — ECW Canary v1 (External Contract Witness)
**Date:** 2026-10-01T22:01:20Z
**Lane:** B (autonomous, reversible, no F13 binary)
**Doctrine:** Sovereign 2026-10-02 — 6-class drift taxonomy + DeclaredState=ObservedState=InterpretedState=EnforcedState invariant

## Deliverables
- /root/AAA/cockpit/ecw-canary.py (kernel; probes 11 MCPs, classifies drift)
- /root/AAA/cockpit/ecw-report.json (sha256=2ce4ca8b64f10fdc8b9d27cbe466468f02bd748986a2170fb64e859a5a914ee8)
- HUD panel CONCURRENCY.ecw (projection of contract, not source)

## First probe (2026-10-02)
| Class | Hit count |
|---|---|
| total_probed | 11 |
| transport_up | 11 |
| surface_declared | 3 (arifOS 8 verbs, others via /.well-known/mcp/server.json) |
| semantic_clean | 11 (vocabulary audit classifier works) |
| SURFACE_DRIFT | 8 (most servers don't expose /.well-known/mcp/server.json — different discovery path needed) |
| SCHEMA_DRIFT | 0 |
| SEMANTIC_DRIFT | 0 |
| AUTHORITY_DRIFT | 0 |
| BEHAVIOR_DRIFT | 0 |
| TRANSPORT_FAILURE | 0 |

## Vocabulary mapping (semantic-consistency layer)
Per arifOS/arifosmcp/runtime/verdict.py:
- CANONICAL: OBSERVE_ONLY, SEAL, SABAR, VOID, HOLD, 888_HOLD
- Legacy map: PASS→SEAL, SYUBHAH→VOID, BLOCKED→VOID, UNKNOWN→VOID, etc.
- All simulated outputs (PASS/SYUBHAH/HOLD) classify clean.

## Discovered via probe
- arifOS declares 8 canonical verbs: arif_init, arif_observe, arif_think, arif_route, arif_memory, arif_judge, arif_forge, arif_seal (matches governance contract).
- /.well-known/mcp/server.json discovery is **partial** — only 3/11 servers expose it. Need JSON-RPC tools/list POST for the remaining 8 (probe mode added in refinement).

## Reversibility
- rm /root/AAA/cockpit/ecw-{canary.py,report.json}
- HUD panel CONCURRENCY.ecw: remove single jq key
- No F13 binary, no canonical mutation, no AGENTS.md change

## Held (next execution path steps)
1. **Auth-valid probes** — currently transport+surface only; need authority layer (P0#1 of sovereign queue)
2. **Vocabulary live samples** — extract actual verdict tokens from each MCP probe, not simulated
3. **ECW cron binding** — sovereign did not approve cake — currently PASS
5. **Phase3 — contract spine (P0#1, P0#2)** — sovereign deferred

[receipt: /root/AAA/cockpit/ecw-report.json]
[receipt: /root/AAA/cockpit/hud-state.json]
[receipt: /root/AAA/cockpit/receipts/RECEIPT_ECW_CANARY_2026-10-02.md]
