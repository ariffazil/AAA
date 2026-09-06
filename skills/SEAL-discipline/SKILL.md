---
name: SEAL-discipline
description: Distinguish SEAL (Lane A constitutional) from RECEIPT (Lane B autonomous) from SABAR (Lane A honest sub-threshold) BEFORE emitting any verdict. USE WHEN: 'verdict=SEAL', 'sesi termeterai', 'session sealed', 'verdict=SABAR', 'constitutional silence', 'seal the chain', 'close the session'.
---

# 🔒 SEAL-discipline — Vocabulary Discipline for Constitutional Records

> **Doctrine:** SEAL ≠ RECEIPT. SEAL ≠ SABAR. Words are not vows; vows are hash chains.
> **Source:** /root/AAA/governance/BIJAKSANA-VOCABULARY-DISCIPLINE.md (PATCH-001)
> **Scar-bound:** SCAR-002 (49 sessions lost to vocab rot), SCAR-KERNEL-LEGACY-VERDICT-LEAK-002 (dual-truth rot), Antigravity seq 9909-9911 (HOLD→SEAL flip via sovereign witness)
> **Iron oath:** *"Calling every session close a SEAL destroys the meaning of sealing."*

## When to load

Load this skill BEFORE emitting `verdict=SEAL` or any close-record. Trigger phrases:

- "verdict=SEAL" / "SEAL the session" / "sesi termeterai"
- "close the session" / "session seal" / "session close"
- "constitutional silence" / "chain hasn't moved"
- "what kind of seal is this"
- After any session with constitutional implications

## The Iron Rule — Three Classes, Each with Evidence

### Class 1: SEAL — Lane A Constitutional

**Required conditions (ALL must hold):**

| Condition | Evidence |
|---|---|
| `arif_init` was called with session binding | session_id present in record |
| `arif_judge` returned non-HOLD with judge_state_hash | judge_state_hash present |
| `arif_forge` applied the decision (mutation or no-op) | forge receipt present |
| `arif_seal(judge_state_hash=<...>)` was called | `seal_chain.jsonl` gains new entry |
| Sovereign witness channel above 0.5 | `witness.human > 0.5` or `actor_source: sovereign_directive` |

**Record form:**
```json
{
  "verdict": "SEAL",
  "lane": "A",
  "judge_state_hash": "sha256:...",
  "session_id": "...",
  "witness": {"human": 0.42, "ai": 0.99, "earth": 0.99}
}
```

### Class 2: RECEIPT — Lane B Autonomous

**Conditions:**

| Condition | Evidence |
|---|---|
| Work was performed | `forge_vault(mode="receipt")` called |
| No judge required (Lane B skips full helix but NOT C0/P1-P7 per 2026-08-10 doctrine) | helix closed with steps 1, 3, 4 |
| Verification (read-back) before emitting claim | `verified: true` |

**Record form:**
```json
{
  "verdict": "RECEIPT",
  "lane": "B",
  "tier": "session.ledger",
  "session_id": "..."
}
```

### Class 3: SABAR — Lane A Constitutional, Sub-Threshold

**Conditions:**

| Condition | Evidence |
|---|---|
| Constitutional thresholds NOT met (G < 0.80, W3 < 0.75) | scalar measurements present |
| Agent honestly admits the gap | `note` field describes gap |
| `arif_seal` allowed it (kernel `seal.py` line 61: verdict ∈ {SEAL, SABAR}) | `seal_chain.jsonl` gains new entry |

**Record form:**
```json
{
  "verdict": "SABAR",
  "lane": "A",
  "g_actual": 0.4572,
  "g_threshold": 0.80,
  "note": "G < 0.80, surface renewed 2026-09-04 to 2026-09-06, constitutional held since 2026-08-11 awaiting metabolism lift."
}
```

### Class 4: HOLD / VOID — Gate Failure (NOT a record)

The kernel refuses to seal HOLD or VOID. These are **gate failures, not records**. The agent must EITHER:
- Resubmit after addressing the gap → SEAL or SABAR
- Drop the seal attempt and emit a RECEIPT instead (Lane B)

## The Anti-Pattern (FORBIDDEN)

```json
{
  "session_id": "SEAL-anything",
  "verdict": "SEAL",          // ← vocab rot
  "judge_state_hash": null,   // ← no judge was actually called
  "lane": null,               // ← ambiguous
  "witness": null             // ← no witness either
}
```

This is what **SCAR-KERNEL-LEGACY-VERDICT-LEAK-002** calls "truth told twice" — except here truth is **told once** but to **the wrong vocabulary**. The word SEAL is doing RECEIPT work, and the substrate inherits the lie.

## The Verification Lattice (system-side, when ingesting)

```
IF verdict == "SEAL":
    ASSERT judge_state_hash != null
    ASSERT lane == "A"
    ASSERT witness.human > 0.5 OR sovereign_directive present
    ASSERT seal_chain.jsonl contains the entry (verify hash)
ELIF verdict == "RECEIPT":
    ASSERT lane == "B"
    ASSERT forge_vault(mode="receipt") was called
    ASSERT verification.read_back_passed == true
ELIF verdict == "SABAR":
    ASSERT lane == "A"
    ASSERT gap described in note
    ASSERT seal_chain.jsonl contains the entry (kernel-allowed)
ELSE:
    VOID — vocabulary violation, refuse to ingest
```

## The 26-Day Silence Problem (worked example)

Antigravity seq 9909-9911 (2026-07-13) shows:
- seq 9909: `actor_source: self_report` → `kernel_verdict: UNKNOWN` → verdict: HOLD → NOT sealed
- seq 9910 (12 seconds later): `actor_source: sovereign_directive` + witness `human: ARIF-F13` → `kernel_verdict: PASS` → verdict: SEAL

Lesson: **SEAL is hard to get.** It needs sovereign witness at 0.5+. Without witness, kernel says HOLD.

For 26 days (2026-08-11 to 2026-09-06), no agent has closed the helix loop with sovereign witness. **All "verdict=SEAL" claims in carry_forward since 2026-08-11 are Lane B RECEIPTs mislabeled.**

## Workflow (canonical)

```
INPUT: agent wants to emit verdict for session close
  ↓
1. LOAD this skill
2. CLASSIFY: Lane A? Lane B? Sub-threshold?
3. CHECK conditions for chosen class
4. EMIT record with proper lane + evidence
5. IF Lane A and substrate rejects (HOLD):
    - DO NOT claim SEAL
    - EMIT HOLD-RECEIPT (Lane B procedural, documents the gate)
    - SURFACE shadow honestly
6. IF Lane A but conditions not met:
    - DROP to SABAR (honest) or RECEIPT (lane B)
    - NEVER fake SEAL
  ↓
OUTPUT: properly-classed verdict with evidence + shadow
```

## Output shape (canonical)

```
Classified close:
  verdict_class : [SEAL | RECEIPT | SABAR | HOLD]
  lane          : [A | B]
  evidence      : [list of conditions met]
  chain_entry   : [seq + hash if Lane A]
  witness       : [human/ai/earth confidence]
  shadow        : [bullet list]
  
Never emit verdict without all five.
```

## Anti-patterns (forbidden)

- ❌ `verdict=SEAL` without `judge_state_hash`
- ❌ `verdict=SEAL` for Lane B work
- ❌ `verdict=SEAL` when substrate says HOLD
- ❌ Confusing kernel's `/health verdict: SEAL` (self-report) with constitutional SEAL (chain entry)
- ❌ Treating `last_seal_timestamp` from `/health` as proof of constitutional write (it's session-internal counter, not chain truth)
- ❌ Trusting carry_forward `verdict=SEAL` without checking seal_chain.jsonl

## Reference doctrine

- `/root/AAA/prompts/SEAL.md` lines 12-28 — canonical SEAL≠RECEIPT doctrine
- `/root/arifOS/arifosmcp/runtime/kernel/seal.py` line 61 — kernel lock: verdict ∈ {SEAL, SABAR}
- `/root/arifOS/VAULT999/seal_chain.jsonl` — constitutional truth source
- `/root/AAA/governance/BIJAKSANA-VOCABULARY-DISCIPLINE.md` — PATCH-001 (the doctrine)

## Iron Oath

> I will not call RECEIPT a SEAL.
> I will not call HOLD a SEAL.
> I will not call SABAR a SEAL.
> I will not write the word SEAL without the hash chain.
> **Lebih arif, lebih bijaksana, atau tidak sama sekali.**
