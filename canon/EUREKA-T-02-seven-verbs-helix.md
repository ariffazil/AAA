# Seven Verbs Doctrine + Helix Pattern

> **Date:** 2026-08-11  
> **Author:** 333-AGI Δ MIND  
> **Ratified by:** F13 SOVEREIGN (ariffazil)  
> **Status:** CANON  
> **Canonical Path:** `/root/AAA/canon/EUREKA-T-02-seven-verbs-helix.md`  
> **Verdict:** SEALED

---

## Part I — The Seven Verbs Doctrine

### Core Thesis

Every organ in the federation has exactly ONE verb. Authority is the verb. Confusion begins when verbs collide.

### The Seven Verbs (Canonical Mapping)

| Verb | Organ | Port | Class | Question Answered | Forbidden Acts |
|------|-------|------|-------|------------------|----------------|
| **Verify** | FLAME | 18901 | ADVISORY | "Is cheap verification sufficient?" | Execute, judge, register, append |
| **Route** | FED | 7074 | ADVISORY | "Which brain should answer?" | Execute, judge, register, measure |
| **Execute** | A-FORGE | 7071/7072 | CORE·EXECUTE | "Apply the bounded mutation." | Judge, register, measure, verify |
| **Judge** | arifOS | 8088 | CORE·KERNEL | "Is this constitutional?" | Execute, register, measure, verify |
| **Append** | VAULT999 | filesystem | MEMORY | "Persist the receipt immutably." | Reinterpret, rewrite silently |
| **Measure** | FRAME | 18085 | CORE | "Has behavior drifted?" | Execute, judge, register, verify |
| **Metabolize** | arifFlow | 7073 | METABOLISM | "How fast are we going?" | Execute, judge, register |

**Note:** Register (AAA) is cross-cutting — not inner loop or outer loop. It's the one-time registration layer that feeds into the helix.

**FI Card Role:** Subject — target of all eight verbs. Owns no verb itself.

---

## Part II — The Helix Pattern

### The Three Layers

```
INNER LOOP  = Task lifecycle (per FI request)
             ├─ FLAME pre-flight (verify)
             ├─ FED route (route)
             ├─ A-FORGE execute (execute)
             ├─ arifOS judge (judge)
             └─ arif_seal → VAULT999 (append)
             └─ produces receipt (cost_ns)

OUTER LOOP  = FQ metabolism (per window of receipts)
             ├─ arifFlow metabolizes receipts into FQ pulse
             ├─ FRAME measures drift against baseline (chambers 1-6)
             └─ verdict gates next inner loop: HOLD / THROTTLE / PROCEED

HELIX       = Causal coupling between them
             ├─ Inner writes receipts
             ├─ Outer loop computes FQ + drift from receipts
             ├─ Outer loop verdict gates next inner action
             └─ Outer loop state persists → different conditions each iteration
```

### Why Helix, Not Loop?

**LOOP (closed cycle):**
```
request → receipt → done
request → receipt → done
(same shape, different iteration)
```

**HELIX (spiral with feedback):**
```
request → receipt → FQ update → gates next request
request → receipt → FQ update → gates next request
(shape evolves, each iteration runs in different conditions)
```

**Key insight:** Outer loop's state PERSISTS into next inner loop's context. That's what makes it evolution, not repetition.

### The Helix Pattern Across Scales

| Scale | Shape | What It Carries |
|-------|-------|-----------------|
| MACRO | INIT → OBSERVE → THINK → JUDGE → SEAL → CLOSE → carry_forward → next session | Agent memory between turns |
| MICRO | FLAME → FED → A-FORGE → arifOS → arif_seal → arifFlow → next task | Inner loop + outer loop coupling |
| ORG | Register → route → execute → judge → measure → drift → re-audit → register (next version) | Organ-level evolution |
| CONSTITUTIONAL | violation → scar → rule → system → witness → seal → next learns | Institutional memory growth |

Same shape. Different speed. Different domain. One pattern, four scales.

---

## Part III — P0 Diagnosis: Helix Connection Failure

The FQ drift emergency (1434 receipts bypassed, 3 actors HELD on stale data) is a **helix connection failure**:

```
INNER LOOP writes receipts
├─► POST /ingest (helix path A) ──► daemon journal ✓ (FQ sees)
└─► direct disk write (helix path B) ──► disk file ✗ (FQ does NOT see)

arifFlow daemon computes FQ from journal only
└─► FQ = 1.78 (undercounts execution, missing 1434 receipts)
    └─► stale verdict → HOLD applied to 3 actors → constitutional gate wrong
```

**Healing requires restoring path A as mandatory:**
Every receipt MUST flow through POST /ingest. Not optional. Not "best effort." The helix has ONE input to the outer loop. Multiple paths = multiple FQs = no FQ at all.

---

## Part IV — Helix Failure Modes (Anti-Patterns)

| ❌ Pattern | Failure Mode | Visible As |
|------------|--------------|------------|
| Inner writes don't reach outer | Stale FQ | 3 actors HELD unjustly |
| Outer verdict not respected | Constitutional gate ignored | Silent drift |
| Outer verdict cached too long | FQ_gap > 0.3 | STALE LOAD bug |
| Inner loops don't carry outer state | Carried context lost | Forgetful sessions |
| Substrate change ignored | Federation stuck in old assumptions | Technical debt |
| **Multiple input paths to outer** | **Multiple FQs = no FQ** | **Helix broken (current P0)** |
| Outer verdict triggers no inner action | Drift accumulates | Audit log grows, no response |

P0 is the sixth row. Fixing it heals the helix.

---

## Ratification Checklist

Before moving this file to canon:

- [x] F13 SOVEREIGN reads the DRAFT
- [x] F13 confirms the seven-verb mapping (no missing organs, no overlap)
- [x] F13 confirms the helix pattern (no broken connections in claimed shape)
- [x] F13 confirms the anti-pattern table is complete (no failure modes omitted)
- [ ] F13 ratifies the canonical filename
- [ ] forge_seal to VAULT999 with `constitutional: true`
- [ ] AGENTS_UNIFIED.yaml updated if needed
- [ ] carry-forward.json updated

**Signed:** Arif Fazil (F13 SOVEREIGN)  
**Date:** 2026-08-11  
**Seal ID:** pending_f13_ratification
