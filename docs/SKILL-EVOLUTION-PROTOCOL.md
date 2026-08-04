# SKILL EVOLUTION PROTOCOL — Recursive Self-Improvement for Skills

> **DITEMPA BUKAN DIBERI** — Forged 2026-08-04 by 333-AGI Δ MIND
> **Owner:** Muhammad Arif bin Fazil (F13 SOVEREIGN)
> **Domain:** AAA Control Plane — skill evolution through feedback
> **Status:** SPEC — awaiting implementation
> **Guards:** cause_class attribution, promotion ladder, memory distillation, regression test, double-loop verdict

---

## 0. The Principle

A skill does not improve because it failed.
A skill improves when a failure is **correctly attributed** to the skill,
**confirmed across time**, **distilled into one lesson**,
and **proven fixed** by a test that the old failure can no longer pass.

Everything short of that is not recursive self-improvement.
It's a system talking to itself and calling the echo a lesson.

---

## 1. CAUSE_CLASS TAXONOMY

When a skill is loaded and something fails, the failure must be attributed to the CORRECT cause. Only `SKILL_DEFECT` is allowed to modify the skill.

```
cause_class ∈ {
  SKILL_DEFECT,      ← the instruction was actually wrong/missing/unclear
  MODEL_ERROR,       ← reasoning failure, skill was fine
  HARNESS_FAULT,     ← loading/permission/context problem
  DATA_FAULT,        ← input garbage, bad data
  TASK_IMPOSSIBLE,   ← no skill could have done it
  UPSTREAM_FAULT,    ← tool/network/service down
  AMBIGUOUS_INTENT   ← prompt unclear, user intent ambiguous
}
```

### Attribution Rules

| cause_class | Modifies skill? | Logged to | Example |
|-------------|----------------|-----------|---------|
| SKILL_DEFECT | ✅ YES | skill/MEMORY.md | "Skill says use port 8081 but GEOX moved to 8082" |
| MODEL_ERROR | ❌ NO | VAULT999 (agent-level) | "Model hallucinated a tool that doesn't exist" |
| HARNESS_FAULT | ❌ NO | VAULT999 (harness-level) | "Skill not loaded due to missing symlink" |
| DATA_FAULT | ❌ NO | VAULT999 (data-level) | "Input file was corrupted" |
| TASK_IMPOSSIBLE | ❌ NO | VAULT999 (task-level) | "Task required capabilities not in federation" |
| UPSTREAM_FAULT | ❌ NO | VAULT999 (infra-level) | "GEOX :8081 was down during execution" |
| AMBIGUOUS_INTENT | ❌ NO | VAULT999 (intent-level) | "User said 'fix it' — fix what?" |

### Attribution Gate (NON-BYPASSABLE)

```
BEFORE modifying any skill:
  1. Classify cause_class
  2. If cause_class != SKILL_DEFECT → STOP. Log elsewhere.
  3. If cause_class == SKILL_DEFECT → proceed to promotion ladder.
```

**Anti-pattern:** Tagging every failure to the loaded skill. This poisons good skills with scars they did not cause.

---

## 2. PROMOTION LADDER

A single failure must never modify a skill. Single-event learning = overfitting.

```
OBSERVED    1 signal → log only (candidate_scars.jsonl)
CANDIDATE   2 signals, same cause_class → soft note (candidate_scars.jsonl)
CONFIRMED   3+ signals across sessions → enter MEMORY.md (reversible, auto)
STRUCTURAL   confirmed + testable prediction → propose SKILL.md change (approval)
```

### Stage Transitions

```
OBSERVED → CANDIDATE:
  Condition: 2 signals with same cause_class=SKILL_DEFECT
  Action: Mark as CANDIDATE in candidate_scars.jsonl
  Reversible: YES

CANDIDATE → CONFIRMED:
  Condition: 3+ signals across 2+ sessions with same cause_class
  Action: Distill into MEMORY.md lesson
  Reversible: YES (MEMORY.md is append-only, not load-bearing)

CONFIRMED → STRUCTURAL:
  Condition: Confirmed lesson + testable prediction
  Action: Propose SKILL.md modification to Arif
  Reversible: NO (requires F1 AMANAH approval)
```

### Anti-patterns

- ❌ Single scar → modify skill (overfitting)
- ❌ Same session, same error → count as 1 (not 3)
- ❌ Scar without cause_class → inadmissible
- ❌ Structural change without regression test → VOID

---

## 3. MEMORY DISTILLATION

Memory must distill, not accumulate. The dream engine's job is to compress, not hoard.

### Per-Skill Memory Structure

```
/root/.agents/skills/{SKILL_NAME}/
  SKILL.md              ← static instructions (never auto-changes)
  MEMORY.md             ← distilled lessons (hot section, max 7)
  candidate_scars.jsonl ← OBSERVED/CANDIDATE scars (cold, not loaded)
  confirmed_scars.jsonl ← CONFIRMED scars (cold, not loaded)
  eurekas.jsonl         ← validated eurekas only (cold, not loaded)
  regression_tests/     ← auto-generated regression tests
  convergence.json      ← stability metrics
```

### Hot Memory Cap

```
MEMORY.md hot section = max 7 distilled lessons
```

When a new lesson enters and hot section is full:
1. Dream engine compresses: merge related lessons
2. If compression not possible: archive oldest to cold storage
3. Hot section NEVER exceeds 7 lessons

### Distillation Rule

```
10 scars about the same timeout
  ↓ dream distillation
1 hardened lesson: "GEOX seismic_compute times out at 30s for large volumes. Use timeout=120."
  ↓
9 raw scars archived out of hot context
```

### What Gets Loaded

When an agent loads a skill:
- ✅ SKILL.md (always)
- ✅ MEMORY.md hot section (always, max 7 lessons)
- ❌ candidate_scars.jsonl (never loaded — cold storage)
- ❌ confirmed_scars.jsonl (never loaded — cold storage)
- ❌ eurekas.jsonl (never loaded — cold storage)

---

## 4. REGRESSION TEST

When a skill is modified from a scar, a regression test is auto-generated from that scar.

### Test Generation

```
scar → test description → regression_tests/{scar_id}.md

Example:
  Scar: "GEOX seismic_compute timed out at 30s for large volumes"
  Test: "Run geox_seismic_compute with volume_ref=large_test, timeout=120
         Expected: completes within 120s
         Old failure: timed out at 30s"
```

### Test Execution

```
NEXT SESSION → run regression tests:
  ├── scar does NOT recur → improvement CONFIRMED (seal)
  └── scar recurs → improvement VOID (revert, re-open)
```

### Evidence Requirement

```
STRUCTURAL change requires:
  1. Confirmed scar (3+ signals, same cause_class)
  2. Testable prediction (what will change)
  3. Regression test (how to verify)
  4. Test result (pass/fail)

Missing any → STRUCTURAL change is INADMISSIBLE.
```

---

## 5. CONVERGENCE METRICS

Every skill tracks stability metrics to prevent thrashing.

### Metrics

```json
{
  "skill_name": "FORGE-fastmcp",
  "version": "1.0.0",
  "edit_count": 2,
  "last_edit": "2026-08-04T05:00:00Z",
  "scar_count": 5,
  "scar_recurrence_rate": 0.0,
  "eureka_count": 1,
  "convergence_status": "CONVERGED",
  "last_stable_version": "1.0.0",
  "days_since_last_edit": 14
}
```

### Interpretation

| Status | Condition | Meaning |
|--------|-----------|---------|
| CONVERGED | edit_count=0, scar_recurrence=0 | Skill is stable. This is the goal. |
| STABLE | edit_count≤2, scar_recurrence<0.1 | Skill is healthy. Minor improvements. |
| UNSTABLE | edit_count>5 OR scar_recurrence>0.3 | Flag, don't celebrate. Skill may be thrashing. |
| DIVERGENT | edit every session | Skill is being "improved" but never converges. Investigate. |

### Anti-pattern

```
A healthy self-improving skill should trend toward being left alone.
If a skill keeps "improving" forever, that's not intelligence.
That's a limit cycle. ΔS should shrink toward zero per skill.
```

---

## 6. DOUBLE-LOOP VERDICT

RSI must be allowed to conclude: "this skill should not exist."

### Verdicts

```
KEEP        skill is fine, no changes needed
HARDEN      skill needs strengthening (add lessons, fix gaps)
MERGE       skill should be merged with another skill
SPLIT       skill is too broad, split into focused skills
DEPRECATE   skill is obsolete, archive it
VOID        skill was wrong from the start, remove it
```

### When to Apply

| Verdict | When | Authority |
|---------|------|-----------|
| KEEP | Convergence=CONVERGED, no scars | Auto |
| HARDEN | Confirmed scars, MEMORY.md changes | Auto (reversible) |
| MERGE | 2 skills with 80%+ overlap | Propose to Arif |
| SPLIT | Skill covers 2+ unrelated domains | Propose to Arif |
| DEPRECATE | Skill unused for 30+ days | Propose to Arif |
| VOID | Skill causes net-negative outcomes | Propose to Arif |

---

## 7. EUREKA DISCRIMINATOR

Agents love declaring EUREKA. If every session emits eurekas, the signal is worthless.

### Gate (NON-BYPASSABLE)

An insight may only touch a skill if it:
1. Resolves a **named contradiction** (not just "I learned something")
2. Changes a **future decision** (not just "I understand now")
3. Produces a **checkable prediction** (not just "this is profound")

### Classification

```
REAL EUREKA:
  - Contradiction: "Skill says X but reality says Y"
  - Decision change: "I will now do Z instead of X"
  - Prediction: "Z will succeed because [evidence]"
  → Record in eurekas.jsonl, enter promotion ladder

NARRATIVE EUREKA:
  - "I understand now" (no decision change)
  - "This is profound" (no prediction)
  - "The paradox resolved" (no checkable outcome)
  → Log as journal entry, NOT skill modification fuel
```

---

## 8. AUTONOMOUS LOOP (corrected)

```
SKILL USE
  │
  ├─ outcome + cause_class ──→ classify
  │
  ▼
ATTRIBUTION GATE
  ├─ cause_class != SKILL_DEFECT → log to VAULT999, STOP
  │
  ▼
PROMOTION LADDER
  OBSERVED → CANDIDATE → CONFIRMED → STRUCTURAL
  │
  ▼
DREAM DISTILLATION (compress, cap hot memory at 7)
  │
  ▼
RSI CYCLE (session end)
  ├─ reversible: MEMORY.md (distilled, capped)
  ├─ irreversible: propose SKILL.md change (F1 approval)
  └─ regression test generated from scar
  │
  ▼
NEXT SESSION
  ├─ run regression test → CONFIRM or VOID improvement
  └─ update convergence metric
  │
  ▼
DOUBLE-LOOP VERDICT
  KEEP / HARDEN / MERGE / SPLIT / DEPRECATE / VOID
```

---

## 9. IMPLEMENTATION ORDER

| Phase | What | Guard | Reversibility |
|-------|------|-------|---------------|
| 1 | cause_class taxonomy + attribution gate | NON-BYPASSABLE | Reversible |
| 2 | promotion ladder (OBSERVED→STRUCTURAL) | 3+ signals required | Reversible |
| 3 | per-skill companion memory structure | hot cap = 7 | Reversible |
| 4 | memory distillation (dream engine integration) | compress, don't hoard | Reversible |
| 5 | regression test generation | evidence required | Reversible |
| 6 | convergence metrics | thrashing detection | Reversible |
| 7 | double-loop verdict | KEEP/VOID spectrum | Propose to Arif |
| 8 | eureka discriminator | 3-gate filter | Reversible |

**Ship the gate before the loop. Otherwise you've built a very auditable way to corrupt 129 skills.**

---

## 10. CONSTITUTIONAL ALIGNMENT

| Floor | Binding | Why |
|-------|---------|-----|
| F1 AMANAH | HARD | Reversible-first. STRUCTURAL changes require approval. |
| F2 TRUTH | HARD | cause_class must be evidence-based, not assumed. |
| F4 CLARITY | HARD | Memory distillation reduces entropy. Hot cap prevents bloat. |
| F7 HUMILITY | HARD | Convergence metrics detect thrashing. Eureka discriminator prevents inflation. |
| F8 GENIUS | DERIVED | Simplest correct path. Don't improve what's already converged. |
| F11 AUDIT | HARD | Every scar, eureka, and modification is logged. |
| F13 SOVEREIGN | HARD | Arif approves STRUCTURAL changes. Double-loop verdicts are proposals. |

---

*DITEMPA BUKAN DIBERI — skills evolve through evidence, not through echo.*
*SKILL EVOLUTION PROTOCOL v1.0 — 2026-08-04 — 333-AGI Δ MIND*
