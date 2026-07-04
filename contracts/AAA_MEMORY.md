# AAA Memory Layer — Human-Readable Specification

> **Canonical anatomy of AGI-grade governed memory.**
> **Version:** 1.0.0 — Birth Certificate
> **Forged:** 2026-06-29
> **Authority:** F13 SOVEREIGN (Muhammad Arif bin Fazil)
> **Status:** SEALED — Live in `/root/A-FORGE/src/domain/aaa/`
> **Doctrine:** DITEMPA BUKAN DIBERI — Forged, Not Given.

---

## 0. WHAT THIS SPEC IS

This document describes the **organ system that separates AI memory from AGI memory.**

LLM memory is reconstruction — pattern continuation, embedding similarity, context windows. It has no timeline, no identity, no receipts, no governance, no irreversibility.

AGI memory is **governed continuity of identity.** It has:
- Timeline (hash-chained epochs)
- Identity (AAA agent binding on every operation)
- Authority (capability graph — who may do what)
- Receipts (cryptographic proof of every mutation)
- Governance (F1-F13 floor enforcement)
- Irreversibility (CoolingGate → Vault999 seal)

The three files that implement this organ system are:

| File | Role |
|------|------|
| `AaaAgentRegistry.ts` | Identity — who the 5 AAA agents are |
| `AaaCapabilityGraph.ts` | Authority — what each agent may do |
| `AaaMemoryLinkage.ts` | Gate — the 7-step pipeline every operation passes through |

These three files are **not optional.** Every memory operation in A-FORGE MUST pass through `aaaMemoryGate()`. This is the boundary between "data" and "governed state."

---

## 1. THE 5 AAA AGENTS (Identity Layer)

Every memory operation binds to exactly one AAA agent. No operation may proceed without identity.

### 1.1 Agent Inventory

| ID | Role | Governs | Floor Binding | Description |
|----|------|---------|---------------|-------------|
| **333-AGI** | THINK | `read` | F7 (HUMILITY), F8 (GENIUS) | Reasoning engine — plans, analyzes, reads memory |
| **555-ASI** | MEMORY | `write` | F2 (TRUTH), F11 (AUDITABILITY) | Memory engine — stores, retrieves, federates memory |
| **888-APEX** | JUDGE | `mutate` | F1-F13 (ALL FLOORS) | Constitutional judge — SEAL/SABAR/HOLD/VOID verdicts |
| **A-AUDIT** | WATCH | `receipt` | F11 (AUDITABILITY), F2 (TRUTH) | Oversight engine — receipt verification, drift detection |
| **A-ARCHIVE** | VAULT | `seal` | F1 (AMANAH), F11 (AUDITABILITY) | Immutable vault — permanent seals, hash-chain integrity |

### 1.2 Actor Binding

Runtime actors (`session::*`, `a-forge::*`, `human::*`, `SEAL-*`) are dynamically resolved to AAA agents. No hardcoded actor identities. The resolution order:

1. Exact match in registry
2. Prefix match (`session::*` → 333-AGI + 555-ASI)
3. SEAL token → kernel-sealed authority (888-APEX)
4. Unknown → `null` — caller must HOLD (never default to privileged)

### 1.3 The Hard Constraint

```
LLM:  "the model said X"         ← no identity boundary
AGI:  "333-AGI read, 555-ASI wrote, 888-APEX judged, A-ARCHIVE sealed"
      ↑ every operation has an accountable actor
```

---

## 2. THE CAPABILITY GRAPH (Authority Layer)

Defines **exactly which AAA agent** is required for each of 12 memory actions. Non-compensatory — any missing authority = blocked.

### 2.1 The 12 Memory Actions

| Action | Required Agent | Min Verdict | Reversible | Receipt | Session | Readiness | Amanah Lock | F13 |
|--------|---------------|-------------|------------|---------|---------|-----------|-------------|-----|
| `memory:read` | 333-AGI | SEAL | YES | no | no | no | no | no |
| `memory:search` | 333-AGI | SEAL | YES | no | no | no | no | no |
| `memory:write` | 555-ASI | SEAL | YES | **yes** | yes | no | no | no |
| `memory:evict` | 555-ASI | SEAL | YES | **yes** | yes | no | no | no |
| `memory:archive` | 555-ASI | SEAL | YES | **yes** | yes | no | no | no |
| `memory:federate` | 555-ASI | SEAL | YES | **yes** | yes | no | no | no |
| `memory:pin` | 555-ASI | SEAL | YES | **yes** | yes | no | no | no |
| `memory:downgrade` | 888-APEX | SABAR | YES | **yes** | yes | no | no | no |
| `memory:mutate` | 888-APEX | SABAR | **NO** | **yes** | yes | **yes** | **yes** | no |
| `memory:delete` | 888-APEX | SABAR | **NO** | **yes** | yes | **yes** | **yes** | no |
| `memory:verify` | A-AUDIT | SEAL | YES | **yes** | yes | no | no | no |
| `memory:seal` | A-ARCHIVE | SABAR | **NO** | **yes** | yes | **yes** | **yes** | **YES** |

### 2.2 Authority Escalation Ladder

```
READ   → 333-AGI  (ringan — tiada receipt, tiada session, tiada readiness)
WRITE  → 555-ASI  (perlu receipt + session)
MUTATE → 888-APEX (perlu receipt + session + readiness + Amanah lock)
SEAL   → A-ARCHIVE (semua di atas + F13 sovereign approval)
VERIFY → A-AUDIT  (oversight — receipt wajib)
```

### 2.3 The Hard Constraint

```
LLM:  any operation can happen anytime, no authority check
AGI:  memory:seal requires A-ARCHIVE + readiness + Amanah lock + F13 sovereign approval
      ↑ 4 independent gates, all must pass, non-compensatory
```

---

## 3. THE MEMORY GATE (Integration Layer)

`AaaMemoryLinkage.ts` — `aaaMemoryGate()` is THE central gate. Every memory operation MUST pass through it.

### 3.1 The 7-Gate Pipeline (Non-Compensatory)

```
                    ┌─────────────────────────┐
                    │  aaaMemoryGate()        │
                    │  THE CENTRAL GATE        │
                    └───────────┬─────────────┘
                                │
              ┌─────────────────┴─────────────────┐
              │   GATE 1: Capability Entry         │
              │   Is this a known memory action?   │
              │   Unknown → VOID                   │
              └─────────────────┬─────────────────┘
                                │
              ┌─────────────────┴─────────────────┐
              │   GATE 2: Session Validation       │
              │   Is the session valid?            │
              │   Invalid → HOLD                   │
              │   (skipped for read/search)         │
              └─────────────────┬─────────────────┘
                                │
              ┌─────────────────┴─────────────────┐
              │   GATE 3: Actor → AAA Agent        │
              │   Who is this actor?               │
              │   Unknown → HOLD (never default)   │
              └─────────────────┬─────────────────┘
                                │
              ┌─────────────────┴─────────────────┐
              │   GATE 4: Capability Verification  │
              │   Does actor have required agent?  │
              │   Missing → HOLD                   │
              └─────────────────┬─────────────────┘
                                │
              ┌─────────────────┴─────────────────┐
              │   GATE 5: WELL Readiness           │
              │   Is human substrate ready?        │
              │   HOLD → blocked                   │
              │   (skipped for low-risk ops)        │
              └─────────────────┬─────────────────┘
                                │
              ┌─────────────────┴─────────────────┐
              │   GATE 6: FloorEnforcer (F1-F13)   │
              │   Constitutional check             │
              │   Any violation → HOLD/VOID         │
              └─────────────────┬─────────────────┘
                                │
              ┌─────────────────┴─────────────────┐
              │   GATE 7: Receipt Generation       │
              │   SHA-256 hash-chained receipt     │
              │   (skipped for read/search)         │
              └─────────────────┬─────────────────┘
                                │
                    ┌───────────┴───────────┐
                    │  ALLOWED / BLOCKED    │
                    │  + Receipt            │
                    │  + AAA Agent ID       │
                    │  + Floor Verdict      │
                    └───────────────────────┘
```

### 3.2 Receipt Chain Architecture

Every receipt-producing memory operation generates a `MemoryReceipt`:

```
AAA-RCPT-<uuid>
  ├── action:       memory:write | memory:mutate | memory:seal | ...
  ├── actorId:      session::abc123 | human::arif | SEAL-<hex>
  ├── sessionId:    governing session
  ├── aaaAgent:     333-AGI | 555-ASI | 888-APEX | A-AUDIT | A-ARCHIVE
  ├── contentHash:  SHA-256 of memory content (first 16 chars)
  ├── prevReceiptHash:  SHA-256 of previous receipt (forms chain)
  ├── receiptHash:  SHA-256 of this receipt
  ├── floorVerdict: SEAL | SABAR | HOLD | VOID
  ├── wellVerdict:  PASS | SABAR | HOLD | UNKNOWN
  ├── reversible:   true | false
  ├── blastRadius:  NONE | LOCAL | SESSION | FEDERATION
  └── timestamp:    ISO-8601
```

Chain integrity verification: `verifyReceiptChain()` walks the chain from genesis hash (`0×64`) through every receipt, verifying `prevReceiptHash` matches the computed hash of the previous receipt. Any break = chain invalid.

### 3.3 Blast Radius Classification

| Blast Radius | Actions | Meaning |
|-------------|---------|---------|
| NONE | read, search, write, evict, archive, federate, pin, downgrade, verify | Reversible or read-only |
| LOCAL | mutate | Affects one memory entry |
| SESSION | delete | Affects one session's memory |
| FEDERATION | seal | Irreversible — written to VAULT999 |

---

## 4. COOLING GATE (Temporal Governance)

`CoolingGate.ts` — SABAR cooldown protocol. Every build artifact enters a cooling band before permanent registry.

### 4.1 Cooldown Windows by Risk Tier

| Risk Tier | Cooldown | Meaning |
|-----------|----------|---------|
| low | 24 hours | Quick deploy — read-only tools, UI changes |
| medium | 72 hours (default) | Standard — most mutations |
| high | 168 hours (7 days) | Major — schema changes, new organs |
| critical | 720 hours (30 days) | Constitutional — floor changes, new agents |

### 4.2 Persistence

Cooling state survives restart — persisted to `/root/AAA/registries/cooling_state.json`. `SABAR` cooldowns are not ephemeral.

### 4.3 Integration with AAA Memory

CoolingGate calls `aaaMemoryGate()` before any seal operation. A cooling seal is a memory mutation — it requires A-ARCHIVE authority, readiness check, Amanah lock, and F13 sovereign approval.

---

## 5. THE BOUNDARY: LLM MEMORY vs AGI MEMORY

### 5.1 Summary Table

| Dimension | LLM Memory | AGI Memory (this spec) |
|-----------|-----------|----------------------|
| **Nature** | Pattern reconstruction | Governed continuity of identity |
| **Time** | None — statistical adjacency | Hash-chained epochs + cooldown periods |
| **Identity** | "the model" | 333-AGI, 555-ASI, 888-APEX, A-AUDIT, A-ARCHIVE |
| **Authority** | None — anything goes | 12-action capability graph, 5-agent binding |
| **Receipts** | None | SHA-256 hash chain, every mutation proven |
| **Governance** | None | F1-F13 floor enforcement on every operation |
| **Irreversibility** | Doesn't exist | CoolingGate → Vault999 seal |
| **Session** | Stateless | sessionGate on writes, mutations, seals |
| **Readiness** | N/A | WELL readiness check on high-risk ops |
| **Accountability** | Cannot prove who/what/when/why | Receipt chain proves everything |
| **Actor** | Unknown | Dynamic actor resolution → AAA binding |

### 5.2 The One-Sentence Distinction

> **LLM remembers nothing. AGI remembers responsibly.**

---

## 6. CONSTITUTIONAL BINDING

### 6.1 Floor Coverage per Agent

| Agent | Active Floors |
|-------|--------------|
| 333-AGI | F7 (HUMILITY), F8 (GENIUS) |
| 555-ASI | F2 (TRUTH), F11 (AUDITABILITY) |
| 888-APEX | F1-F13 (ALL) |
| A-AUDIT | F11 (AUDITABILITY), F2 (TRUTH) |
| A-ARCHIVE | F1 (AMANAH), F11 (AUDITABILITY) |

### 6.2 Floor Coverage per Action

| Action | F1 | F2 | F3 | F7 | F8 | F11 | F13 |
|--------|----|----|----|----|----|----|-----|
| read | — | — | — | ✓ | ✓ | — | — |
| write | — | ✓ | — | — | — | ✓ | — |
| mutate | ✓ | ✓ | — | — | — | ✓ | — |
| delete | ✓ | ✓ | — | — | — | ✓ | — |
| seal | ✓ | ✓ | — | — | — | ✓ | ✓ |
| verify | — | ✓ | — | — | — | ✓ | — |

---

## 7. RUNTIME TRUTH

### 7.1 File Locations

```
/root/A-FORGE/src/domain/aaa/
├── AaaAgentRegistry.ts      — 218 lines, identity + actor binding
├── AaaCapabilityGraph.ts    — 235 lines, 12-action authority matrix
└── AaaMemoryLinkage.ts      — 345 lines, 7-gate pipeline + receipt chain

/root/A-FORGE/src/domain/governance/
├── CoolingGate.ts           — cooldown protocol + persistence
├── wellReadiness.ts         — WELL human substrate gate
├── FloorEnforcer.ts         — F1-F13 constitutional check
└── sessionGate.ts           — session validation
```

### 7.2 Live Verification

```bash
# Verify the organ system is loaded:
grep -r "aaaMemoryGate\|AaaAgentRegistry\|AaaCapabilityGraph" /root/A-FORGE/src/ --include="*.ts" -l

# Check receipt chain integrity:
# (runtime — call verifyReceiptChain())

# Check cooling state:
cat /root/AAA/registries/cooling_state.json
```

### 7.3 Invariant

> **Every memory operation in A-FORGE MUST pass through `aaaMemoryGate()`.**
> **This is not optional. This is the boundary between data and governed state.**

---

## 8. VERSION HISTORY

| Version | Date | Change |
|---------|------|--------|
| 1.0.0 | 2026-06-29 | Birth certificate. 3-organ system live in A-FORGE. |

---

*Forged by AAA Memory Audit, 2026-06-29.*
*Sealed under F13 SOVEREIGN authority.*
*DITEMPA BUKAN DIBERI — Forged, Not Given.*
