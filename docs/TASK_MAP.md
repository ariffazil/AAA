# arifOS Repair Programme — Session Task Map
**Forged:** 2026-07-17 · **Seal:** SESSION-ZEN-2026-07-17
**Origin:** Claude audit contrast probe (morning vs evening)
**Authority:** F13 SOVEREIGN — Muhammad Arif bin Fazil

## Executive Summary

This morning the kernel was "confidently wrong" about identity — it claimed `verified: true, method: null`. Tonight it's "honestly uncertain" — `verified: false, method: null, evidence_ref: session://...`. The bluff is gone. The signed token exists. The architecture now correctly restricts authority until proof-of-identity exists.

This repair programme addresses the 10 items identified in the contrast audit.

## Items Executed (2026-07-17)

| # | Item | Commit | Repository |
|---|------|--------|------------|
| 1 | Stabilize kernel/MCP | `e36b4f46a` | arifOS — conformance_block patch |
| 3 | Vault swallowing audit | — | Verified — only connection cleanup |
| 4 | Rename RiskClass | `07d3c529e` | arifOS — ChangeAuthorityClass + OperationalRiskTier |
| 8 | BIJAKSANA ratchet | `07d3c529e` | arifOS — governance/bijaksana_ratchet.yaml |

## Architecture Sessions (Pending)

| Session | File | Blast | Depends On |
|---------|------|-------|------------|
| **A** — Operation + ReceiptOutbox | `SESSION_A_OPERATION_RECEIPTOUTBOX.md` | HIGH | PostgreSQL up, arifOS stable |
| **B** — Memory Lifecycle | `SESSION_B_MEMORY_PIPELINE.md` | MEDIUM | Session A (needs operation_id lineage) |
| **C** — Health Schema | `SESSION_C_HEALTH_SCHEMA.md` | MEDIUM | All 6 organs up |
| **D** — AAA Registry | `SESSION_D_AAA_REGISTRY.md` | LOW | AAA server up |
| **E** — Canary + Change Control | `SESSION_E_CANARY_CHANGE_CONTROL.md` | MEDIUM | Sessions A-D complete |

## Execution Order

```
Session A (Operation+ReceiptOutbox) → Session E (Canary verification)
Session B (Memory pipeline) — independent, can run parallel to C/D
Session C (Health schema) — independent
Session D (AAA registry) — independent
```

## ATLAS333 Context

All five sessions require:
- `arif_think(mode=plan)` before execution
- `arif_judge` SEAL before any MUTATE-class operation
- `arif_seal` on completion
- External witness for SESSION_A (Gödel Lock — blast radius HIGH)

## Change Control

```yaml
change_control:
  reversible: true
  blast_radius: medium
  authority_required: F13_SOVEREIGN_FOR_DEPLOYMENT
  judge_receipt_required: true
  human_ack_required: true
  rollback: revert repair branch, restore prior service unit, preserve pending operations
  post_change_probe: run isolated eight-stage canary, verify VAULT replay
```
