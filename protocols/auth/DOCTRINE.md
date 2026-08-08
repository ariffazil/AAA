# AUTH — The Institutional Protocol

> **DITEMPA BUKAN DIBERI** — Forged, Not Given.
> **Ratified:** 2026-08-08 — Arif F13 SOVEREIGN
> **Designation:** `AAA::PROCESS_RUNTIME` — State machine, not agent, not organ
> **Canonical home:** `AAA/protocols/auth/` (protocol definition)
> **Execution engine:** `A-FORGE/src/domain/auth/pipeline.ts`

---

## The Five Questions — Each Layer, Exactly One

| Layer | Question | Lives In | Is | Is NOT |
|-------|----------|----------|-----|--------|
| **333-AGI** | "What should we do?" | AAA — Wisdom | Proposal | Execution |
| **555-ASI** | "Is the evidence sound?" | AAA — Wisdom | Verification | Judgment |
| **888-APEX** | "Is this constitutional?" | AAA — Wisdom | Judgment | Process |
| **AUTH** | "Was the process followed?" | AAA — Process | Protocol | Intelligence |
| **A-FORGE** | "What is executed?" | Execution | Hands | Wisdom |
| **arifFLOW** | "What happened?" | Metabolism | Nerve | Governance |
| **VAULT999** | "What is proven?" | Truth | Bones | Interpretation |

**AAA is the composite: Wisdom (333/555/888) + Process (AUTH).**
AUTH is not a separate layer. It is the process half of AAA.

---

## The Three Laws

```
OBSERVE is free.
MUTATE is governed.
DEPLOY is sealed.
```

Everything else — contracts, leases, evidence bundles, 555 verification, 888 judgment — is implementation detail derived from these three laws.

**Corollary:** Governance depends on **action class**, not agent identity. Claude Code + OBSERVE needs no contract. Kimi + MUTATE needs the same contract as any other agent. The institution does not care who holds the scalpel — only whether the cut requires a contract.

---

## What AUTH Is

AUTH is **not** a new organ.  
AUTH is **not** a new agent.  
AUTH is **not** a replacement for AAA, A-FORGE, arifFLOW, or VAULT999.  
AUTH is **not** a standalone layer between AAA and A-FORGE.

**AUTH is the process layer within AAA — the institutional protocol that ensures the Trinity's judgments cannot bypass procedural machinery.**

AAA is the composite:
```
AAA = Wisdom (333/555/888) + Process (AUTH)
```

Where:
- **333-AGI** proposes what should be done
- **555-ASI** verifies the evidence is sound
- **888-APEX** judges whether the action is constitutional
- **AUTH** ensures every step of the process was followed — contracts, leases, evidence bundles, receipts, seals

It is the thin orchestrator that chains:
- `forge_lease` → worktree isolation
- `forge_lock` → F1 Amanah mutation gate
- `forge_stage` → governance preview
- `forge_sandbox_run` → isolated execution
- `arif_judge` → 888-APEX constitutional verdict
- `forge_vault(mode="receipt")` → Lane B receipt
- `arif_seal` → Lane A immutable append
- `arifflow_flow_ingest` → metabolic checkpoint

Into a **single non-bypassable pipeline**:

```
DECLARE → LEASE → LOCK → EXECUTE → EVIDENCE → VERIFY → JUDGE → MERGE → SEAL → INGEST
```

---

## The Jurisdiction Boundary

```
┌─────────────────────────────────────────────────┐
│                  FREE REALM                       │
│                                                    │
│  Claude Code   OpenCode   Kimi   Codex   Gemini    │
│       │           │         │       │       │       │
│       └───────────┴────┬────┴───────┘       │       │
│                        │                      │       │
│              OBSERVE is free                  │       │
│              (read, explore, explain, think)  │       │
│                                                    │
└────────────────────┬───────────────────────────┘
                     │
              ┌──────┴──────┐
              │  AUTH GATE │  ← "May this happen?"
              └──────┬──────┘
                     │
         ┌───────────┼───────────┐
         │           │           │
    MUTATE       DEPLOY      (blocked)
    governed     sealed
         │           │
         ▼           ▼
    ┌─────────┐ ┌─────────┐
    │RECEIPT  │ │  SEAL   │
    │(Lane B) │ │(Lane A) │
    └────┬────┘ └────┬────┘
         │           │
         └─────┬─────┘
               │
          arifFLOW ← "What happened?"
               │
          VAULT999 ← "What is proven?"
```

---

## Why AUTH Lives Inside AAA — Not As A Separate Layer

**The composite test:**

| Component | Role |
|-----------|------|
| 333-AGI | Proposes what should be done |
| 555-ASI | Verifies the evidence is sound |
| 888-APEX | Judges constitutionality |
| AUTH | Ensures process was followed |

All four are part of AAA's governance surface. The Trinity provides wisdom. AUTH provides process. Together they form the complete governance organ.

**If AUTH were a separate layer between AAA and A-FORGE:**
```
AUTH → AAA → A-FORGE
```
This implies AAA judges AFTER AUTH gates — but AUTH needs AAA's judgment (555 verify, 888 seal) AS PART of its pipeline. The pipeline stages VERIFY and JUDGE delegate to AAA's wisdom layer. So the relationship is not sequential layers — it's interleaved delegation within one organ.

**The correct model — AUTH inside AAA:**
```
AAA
├── Wisdom (333, 555, 888)
│   "Should this happen?"
│
└── Process (AUTH)
    "Was the proper contract filed?"
    "Is there a lease?"
    "Where is the evidence?"
    "Has it been sealed?"
```

AUTH delegates TO the Trinity (steps VERIFY → JUDGE) while enforcing that those steps CANNOT be skipped. This is not two layers — it's one organ with two halves: wisdom that decides, and process that ensures decisions are accountable.

---

## Why CAS Is Not AUTH

CAS revealed the *pattern* — a supervisor/worker protocol with evidence-gated closure and snapshot-bound verification gates. But CAS is:

- **Claude-Code-locked** (violates F13 anti-vendor-capture)
- **Stalled** (5 months without commits, single maintainer)
- **Factory model** (all work flows through supervisor → owns agents)

AUTH metabolizes CAS's best patterns without adopting its architecture:

| CAS Pattern | AUTH Implementation |
|---|---|
| Worktree isolation | `forge_lease` + git worktrees |
| Evidence-gated closure | `TaskContract.evidence_required` |
| Supervisor/worker split | Pipeline delegates to AAA (judge) + A-FORGE (execute) |
| Verification before merge | Step VERIFY → Step JUDGE → Step MERGE |

**AUTH is CAS's pattern without CAS's dependency.**

---

## The Contract Schema

```yaml
task_id: AUTH_001
objective: Eliminate token refresh race condition
action_class: MUTATE
worker_role: builder
acceptance_criteria:
  - All auth tests pass
  - Race condition reproduced before fix
  - Race condition absent after fix
evidence_required:
  - diff
  - test_output
merge_policy: require_555_verification
seal_required: false
reversible: true
risk_tier: medium
target: /root/A-FORGE/src/auth/token.ts
requested_by: ARIF
```

---

## AUTH in the 000→999 Reality Loop

AUTH is not a new node. AUTH is the **transition protocol** between nodes.

```
000 — Intent       "Why does this exist?"
111 — Reality      "What is actually happening?"
333 — Thought      "What should be done?"
        │
   ┌────┴────┐
   │ AUTH  │  ← "May shared reality now be changed?"
   │ CONTRACT │     Contract · Lease · Evidence Requirements
   └────┬────┘
        │
555 — Truth        "Is the proposal true?"
888 — Constitution "Is it lawful?"
777 — Action       "Execute the mutation."
999 — Witness      "Can this be proven later?"
        │
  arifFLOW          "Remember what happened."
```

**The anti-short-circuit guarantee:**

```
WITHOUT AUTH:  333 → 777  (thought → execution, too fast)
WITH AUTH:     333 → AUTH → 555 → 888 → 777 → 999
```

AUTH forces the long path. It prevents the federation's oldest failure mode: execution outrunning verification.

**The compression:**

```
000 — Why
111 — What Is
333 — What Could Be
AUTH — May We
555 — Is It True
888 — Is It Right
777 — Do It
999 — Prove It
arifFLOW — Remember It
```

---

## The AAA Composite

```
AAA = Why + How
A-FORGE = Do
VAULT999 = Prove
arifFLOW = Remember
```

Where `Why` = 333/555/888 (wisdom) and `How` = AUTH (process).

**Within AAA:**
```
333-AGI = Proposal    ("What should we do?")
555-ASI = Verification ("Is the evidence sound?")
888-APEX = Judgment   ("Is this constitutional?")
AUTH  = Process     ("Was the process followed?")
```

Bureaucracy is not an insult. It is the difference between a wise decision and a wise decision that is recorded, attributed, evidenced, and sealed. Civilizations do not fail because wisdom is absent. They fail because the registry was lost, the lease was verbal, the receipt was never written, and no one can prove who approved what.

---

## The One-Sentence Doctrine

> **AUTH governs transitions, not agents. The moment any agent attempts to alter shared reality, AUTH jurisdiction begins.**

---

*Forged: 2026-08-08 by 333-AGI Δ MIND under F13 SOVEREIGN directive.*
*Metabolized from: CAS architecture patterns, arifOS constitutional floors, A-FORGE execution verbs, arifFLOW metabolic nerve.*
*DITEMPA BUKAN DIBERI ⚒️*
