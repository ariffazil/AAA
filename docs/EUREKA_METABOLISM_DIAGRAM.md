# EUREKA — Operational Metabolism Diagram

> **How governed intelligence processes failure into architecture.**
> **DITEMPA BUKAN DIBERI — Forged, Not Given.**
> **Sealed: 2026-07-13**

---

## THE METABOLISM CYCLE

```
                    ┌─────────────────────────────────────┐
                    │         SOVEREIGN PLANE              │
                    │    Arif (F13) — Final Veto           │
                    └──────────────┬──────────────────────┘
                                   │
                          F13 veto / intent
                                   │
                                   ▼
┌──────────────────────────────────────────────────────────────────────┐
│                      GOVERNANCE PLANE (arifOS)                       │
│                                                                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            │
│  │ CLASSIFY │→ │ AUTHORIZE│→ │  VERDICT │→ │  SEAL    │            │
│  │          │  │          │  │          │  │          │            │
│  │ action   │  │ identity │  │ SEAL     │  │ VAULT999 │            │
│  │ class    │  │ + lease  │  │ HOLD     │  │ immutable│            │
│  │ blast    │  │ + prior  │  │ SABAR    │  │ receipt  │            │
│  │ radius   │  │ verdicts │  │ VOID     │  │          │            │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘            │
│       │              │              │              │                  │
│       ▼              ▼              ▼              ▼                  │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │              16-GATE PRE-EXECUTION CHAIN                      │   │
│  │  G1→G2→G3→G3.5→G4→G5→G6→G7→G8→G9→G10→G11→G12→G13→G14→G16  │   │
│  │  session manifest blast actor lease f13 hash drift ART ACT   │   │
│  │  memory schema fed health cooling verdict                    │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                      │
└───────────────────────────────┬──────────────────────────────────────┘
                                │
                    bounded capability lease
                                │
                                ▼
┌──────────────────────────────────────────────────────────────────────┐
│                    INTELLIGENCE PLANE (Agents)                       │
│                                                                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            │
│  │  REASON  │→ │  PROPOSE │→ │  EVIDENCE│→ │  COMPUTE │            │
│  │          │  │          │  │          │  │          │            │
│  │ plan     │  │ action   │  │ collect  │  │ domain   │            │
│  │ analyze  │  │ artifact │  │ verify   │  │ result   │            │
│  │ reflect  │  │ risk     │  │ classify │  │ GEOX     │            │
│  │          │  │ rollback │  │          │  │ WEALTH   │            │
│  │          │  │          │  │          │  │ WELL     │            │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘            │
│                                                                      │
│  CONSTRAINTS:                                                        │
│  - May READ any accessible data                                      │
│  - May PROPOSE any action                                            │
│  - May COMPUTE any domain result                                     │
│  - May NOT execute without capability                                │
│  - May NOT issue verdicts                                            │
│  - May NOT self-authorize                                            │
│                                                                      │
└───────────────────────────────┬──────────────────────────────────────┘
                                │
                    proposed action + evidence
                                │
                                ▼
┌──────────────────────────────────────────────────────────────────────┐
│                     EXECUTION PLANE (A-FORGE)                        │
│                                                                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            │
│  │EXECUTE   │→ │ VERIFY   │→ │ ARTIFACT │→ │ ROLLBACK │            │
│  │          │  │          │  │          │  │          │            │
│  │ filesystem│  │ tests   │  │ commit   │  │ ready    │            │
│  │ build    │  │ health   │  │ wheel    │  │ before   │            │
│  │ deploy   │  │ import   │  │ hash     │  │ any prod │            │
│  │ restart  │  │ runtime  │  │ receipt  │  │ change   │            │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘            │
│                                                                      │
│  REQUIRES:                                                           │
│  - Valid capability lease from Governance                            │
│  - Prior SEAL verdict                                               │
│  - Blast radius classification                                       │
│  - Rollback artifact ready                                           │
│                                                                      │
│  PRODUCES:                                                           │
│  - Reality change (filesystem, service, deployment)                  │
│  - Verification evidence (test results, health checks)               │
│  - Receipt artifact (for VAULT999 sealing)                           │
│                                                                      │
└───────────────────────────────┬──────────────────────────────────────┘
                                │
                    reality result + receipt
                                │
                ┌───────────────┼───────────────┐
                ▼               ▼               ▼
┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│  CONTINUITY      │ │  TRUTH           │ │  METABOLISM      │
│  PLANE           │ │  PLANE           │ │  LOOP            │
│                  │ │                  │ │                  │
│  Postgres        │ │  VAULT999        │ │  Failure         │
│  Qdrant          │ │  hash-chain      │ │  → Symptom       │
│  filesystem      │ │  immutable       │ │  → Hypothesis    │
│  queues          │ │  receipts        │ │  → Evidence      │
│                  │ │                  │ │  → Repair        │
│  Memory tiers:   │ │  Scar records:   │ │  → Verification  │
│  L1 Redis (now)  │ │  failure →       │ │  → Cooling       │
│  L2 Redis (sess) │ │  constitutional  │ │  → Scar          │
│  L3 Qdrant (sim) │ │  constraint      │ │  → Constraint    │
│  L4 Supabase     │ │                  │ │                  │
│  L5 Graphiti     │ │  Cooling:        │ │  KEY INVARIANT:  │
│  L6 VAULT999     │ │  failure →       │ │  Returns to      │
│  (immutable)     │ │  improvement     │ │  arif_judge      │
│                  │ │  → governance    │ │  NOT A-FORGE     │
│                  │ │  path            │ │                  │
└──────────────────┘ └──────────────────┘ └──────────────────┘
```

---

## METABOLISM STATE MACHINE

```
                    ┌─────────┐
                    │   HOT   │ ← active failure, immediate response
                    └────┬────┘
                         │
                    classify symptom
                         │
                         ▼
                    ┌─────────┐
                    │  WARM   │ ← recent failure, repair in progress
                    └────┬────┘
                         │
                    implement repair
                         │
                         ▼
                    ┌─────────┐
                    │  COOL   │ ← failure resolved, cooling record written
                    └────┬────┘
                         │
                    metabolize → scar seal
                         │
                         ▼
                    ┌─────────┐
                    │  COLD   │ ← metabolized, constitutional constraint added
                    └─────────┘
```

**COLD_LINK artifact:**
```
{
  "failure_id": "F-2026-07-13-001",
  "symptom": "arif_seal blocked by Gate 3.5 (INFRASTRUCTURE blast radius)",
  "hypothesis": "blast_radius classification was wrong — append-only vault write is not infrastructure",
  "evidence": ["pre_execution_gate.py:749 had BlastRadius.INFRASTRUCTURE", "Gate 3.5 unconditionally blocks INFRASTRUCTURE"],
  "repair": "Change blast_radius to HIGH",
  "verification": "d6fe84b78 committed, tests pass",
  "scar_id": "SCAR-20260713-BLAST-RADIUS-001",
  "constraint": "Append-only vault writes are HIGH blast radius, not INFRASTRUCTURE",
  "metabolism_state": "COLD",
  "sealed_to": "VAULT999"
}
```

---

## COOLING LOOP — DETAILED FLOW

```
┌─────────────────────────────────────────────────────────────────┐
│                    COOLING LOOP                                  │
│                                                                 │
│  INPUT: Failure event (from any plane)                          │
│                                                                 │
│  STEP 1: CLASSIFY SYMPTOM                                       │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ What happened?                                           │   │
│  │ What was expected?                                       │   │
│  │ What actually occurred?                                  │   │
│  │ Which gate/plane/component failed?                       │   │
│  │ Is this a new failure or a recurrence?                   │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  STEP 2: FORM HYPOTHESIS                                        │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Why did it fail?                                         │   │
│  │ Was the original diagnosis right?                        │   │
│  │ Was the classification correct?                          │   │
│  │ Was the authority calculation correct?                   │   │
│  │ Was the evidence sufficient?                             │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  STEP 3: COLLECT EVIDENCE                                       │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Which code was running?                                  │   │
│  │ Which tests caught the issue?                            │   │
│  │ Which gate blocked?                                      │   │
│  │ What was the runtime state?                              │   │
│  │ What was the session state?                              │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  STEP 4: PROPOSE REPAIR                                         │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ What change would fix this?                              │   │
│  │ Is the change reversible?                                │   │
│  │ What is the blast radius of the change?                  │   │
│  │ Does it require F13 approval?                            │   │
│  │ Is there a reusable procedural improvement?              │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  STEP 5: GOVERNED IMPLEMENTATION                                │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Route through: arif_judge → SEAL → A-FORGE → verify     │   │
│  │ NOT: A-FORGE → self-approve → deploy                     │   │
│  │ The repair follows the same governance as any action.    │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  STEP 6: VERIFY                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Does the fix resolve the symptom?                        │   │
│  │ Does it introduce new failure modes?                     │   │
│  │ Do existing tests still pass?                            │   │
│  │ Are new tests needed?                                    │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  STEP 7: SEAL SCAR                                              │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Record failure → constitutional constraint               │   │
│  │ The scar becomes part of the system's immune system.     │   │
│  │ Future agents will check against this scar before acting.│   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  OUTPUT: COLD_LINK artifact → VAULT999                          │
│                                                                 │
│  INVARIANT: Returns to arif_judge, NOT A-FORGE.                 │
│  This is safe recursive improvement.                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## WHY METABOLISM MATTERS

Before metabolism:
- Failure → log → forget → repeat
- The system has scars but no immune system
- Every failure is a potential future failure

After metabolism:
- Failure → classify → hypothesize → repair → verify → seal → constraint
- The system converts scars into architecture
- Every failure makes the system harder to break

**This is the operational meaning of DITEMPA, BUKAN DIBERI.**

The system is not given immunity. It is forged through failure.

---

*DITEMPA BUKAN DIBERI — 999 SEAL ALIVE*
