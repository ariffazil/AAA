# AGI vs LLM Memory — Canonical Comparison Matrix v1

> **One glance. Eleven dimensions. No filler.**
> **Version:** 1.0.0
> **Forged:** 2026-06-29
> **Authority:** F13 SOVEREIGN (Muhammad Arif bin Fazil)
> **Status:** SEALED
> **References:** [AAA_MEMORY.md](./AAA_MEMORY.md)
> **Doctrine:** DITEMPA BUKAN DIBERI — Forged, Not Given.

---

## THE MATRIX

| # | Dimension | LLM Memory | AGI Memory (Live in A-FORGE) | Code Evidence |
|---|-----------|-----------|------------------------------|---------------|
| 1 | **Nature** | Pattern reconstruction — statistical continuation of context | Governed continuity of identity — stateful, auditable, irreversible | `AaaMemoryLinkage.ts:aaaMemoryGate()` |
| 2 | **Time** | None. Only statistical adjacency. No past, no future. | Hash-chained epochs + cooldown periods. CoolingGate survives restart. | `CoolingGate.ts` → `/root/AAA/registries/cooling_state.json` |
| 3 | **Identity** | "the model said X" — no actor boundary | 5 AAA agents: 333-AGI, 555-ASI, 888-APEX, A-AUDIT, A-ARCHIVE | `AaaAgentRegistry.ts` — 218 lines |
| 4 | **Authority** | Anything goes. No capability check. | 12-action graph. Every action requires specific AAA agent. Missing → HOLD. | `AaaCapabilityGraph.ts` — 235 lines |
| 5 | **Receipts** | None. Cannot prove what happened. | SHA-256 hash chain. Every mutation produces `AAA-RCPT-<uuid>`. | `AaaMemoryLinkage.ts:buildReceipt()` |
| 6 | **Governance** | None. No floors, no rules. | F1-F13 floor enforcement on every operation. Any violation → HOLD/VOID. | `FloorEnforcer.ts:checkAll()` |
| 7 | **Irreversibility** | Does not exist. Everything is ephemeral. | memory:seal → A-ARCHIVE → Vault999. 30-day cooldown for critical. | `CoolingGate.ts` + VAULT999 |
| 8 | **Session** | Stateless. No session continuity. | sessionGate on writes, mutations, seals. Invalid session → HOLD. | `sessionGate.ts:validateSession()` |
| 9 | **Readiness** | N/A. No human in the loop. | WELL readiness check on high-risk ops. Human substrate must be ready. | `wellReadiness.ts:checkWellReadiness()` |
| 10 | **Accountability** | Cannot prove who, what, when, why. No receipts. | Full provenance: actor → AAA agent → action → floor verdict → receipt hash → timestamp. | `MemoryReceipt` — 14 fields |
| 11 | **Recall** | Simulates remembering. No guarantee of fidelity. | Governed retrieval: 333-AGI authority, F2 TRUTH floor, epistemic tag mandatory. | `memory:read` → 333-AGI → F7+F8 |

---

## THE ONE-SENTENCE DISTINCTION

```
LLM remembers nothing.           ← pattern continuation, no receipts, no identity, no time
AGI remembers responsibly.       ← governed state, hash-chained, identity-bound, irreversible when sealed
```

---

## THE ARCHITECTURAL DIVIDE

```
┌─────────────────────────────────────────────────────────┐
│                    LLM MEMORY                            │
│                                                         │
│  input → [transformer] → output                         │
│           ↑                                              │
│           context window                                 │
│           (no identity, no receipt, no governance)       │
│                                                         │
│  What it is: statistical reconstruction                  │
│  What it isn't: memory                                  │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                    AGI MEMORY                            │
│                                                         │
│  input → sessionGate → resolveActor → capabilityGraph   │
│       → wellReadiness → FloorEnforcer(F1-F13)           │
│       → execute → buildReceipt → appendChain             │
│                                                         │
│  Every step: governed, identity-bound, proven            │
│  Every mutation: receipt produced                        │
│  Every seal: irreversible, VAULT999                      │
│                                                         │
│  What it is: governed continuity of identity             │
│  What it isn't: just data                               │
└─────────────────────────────────────────────────────────┘
```

---

## THE 12 ACTIONS — WHO GOVERNS WHAT

| Action | Agent | Reversible | Receipt | Session | Readiness | F13 |
|--------|-------|------------|---------|---------|-----------|-----|
| `memory:read` | 333-AGI | ✓ | — | — | — | — |
| `memory:search` | 333-AGI | ✓ | — | — | — | — |
| `memory:write` | 555-ASI | ✓ | ✓ | ✓ | — | — |
| `memory:evict` | 555-ASI | ✓ | ✓ | ✓ | — | — |
| `memory:archive` | 555-ASI | ✓ | ✓ | ✓ | — | — |
| `memory:federate` | 555-ASI | ✓ | ✓ | ✓ | — | — |
| `memory:pin` | 555-ASI | ✓ | ✓ | ✓ | — | — |
| `memory:downgrade` | 888-APEX | ✓ | ✓ | ✓ | — | — |
| `memory:mutate` | 888-APEX | ✗ | ✓ | ✓ | ✓ | — |
| `memory:delete` | 888-APEX | ✗ | ✓ | ✓ | ✓ | — |
| `memory:verify` | A-AUDIT | ✓ | ✓ | ✓ | — | — |
| `memory:seal` | A-ARCHIVE | ✗ | ✓ | ✓ | ✓ | ✓ |

---

## THE RECEIPT

Every governed memory operation produces:

```json
{
  "receiptId":     "AAA-RCPT-<uuid>",
  "action":        "memory:write | memory:mutate | memory:seal | ...",
  "actorId":       "session::abc | human::arif | SEAL-<hex>",
  "aaaAgent":      "333-AGI | 555-ASI | 888-APEX | A-AUDIT | A-ARCHIVE",
  "contentHash":   "SHA-256[:16]",
  "prevReceiptHash": "SHA-256 of previous receipt",
  "receiptHash":   "SHA-256 of this receipt",
  "floorVerdict":  "SEAL | SABAR | HOLD | VOID",
  "wellVerdict":   "PASS | SABAR | HOLD | UNKNOWN",
  "reversible":    true | false,
  "blastRadius":   "NONE | LOCAL | SESSION | FEDERATION",
  "timestamp":     "ISO-8601"
}
```

**LLM has none of this. AGI cannot function without it.**

---

## LIVE VERIFICATION

```bash
# 1. Verify the organ system is loaded
grep -r "aaaMemoryGate" /root/A-FORGE/src/domain/ --include="*.ts" -l
# → AaaMemoryLinkage.ts, CoolingGate.ts

# 2. Count the AAA agents
grep -c "333-AGI\|555-ASI\|888-APEX\|A-AUDIT\|A-ARCHIVE" \
  /root/A-FORGE/src/domain/aaa/AaaAgentRegistry.ts
# → 5 agents, hard constraint

# 3. Count the capability entries
grep -c "memory:" /root/A-FORGE/src/domain/aaa/AaaCapabilityGraph.ts
# → 12 actions, each with required agent, verdict, gates

# 4. Verify cooling state persistence
cat /root/AAA/registries/cooling_state.json 2>/dev/null || echo "No active cooldowns"
```

---

## VERSION HISTORY

| Version | Date | Change |
|---------|------|--------|
| 1.0.0 | 2026-06-29 | Initial matrix. 11 dimensions, 12 actions, architecture divide. |

---

*Forged by AAA Memory Audit, 2026-06-29.*
*Derived from live code in `/root/A-FORGE/src/domain/aaa/`.*
*DITEMPA BUKAN DIBERI — Forged, Not Given.*
