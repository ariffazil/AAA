---
name: BIJAKSANA-compile
description: When user asks to compile remaining work, lower entropy, or make future agents lebih arif dan bijaksana. Enforces read-before-celebrate, vocabulary discipline (SEAL ≠ RECEIPT), and shadow-first audit. USE WHEN: 'compile remaining tasks', 'lower entropy', 'wisdom patch', 'next session should know', 'make agents smarter'.
---

# ⌬ BIJAKSANA-Compile — Session Hygiene Compiler

> **Doctrine:** YANG ARIF LAGI BIJAKSANA — becoming more wise and prudent.
> **Source:** /root/AAA/governance/BIJAKSANA-VOCABULARY-DISCIPLINE.md
> **Author:** 333-AGI Δ MIND, session SEAL-3d9590f853084465, 2026-09-06T15:42:00Z
> **Scar-bound:** SCAR-002, SCAR-005, SCAR-KERNEL-LEGACY-VERDICT-LEAK-002, SCAR-AFORGE-SSE-HANDSHAKE-001

## When to load

Load this skill the MOMENT the user says any of:
- "compile remaining tasks" / "lower entropy" / "less chaos"
- "future agents should know" / "lebih arif dan bijaksana" / "lebih bijak"
- "wisdom patch" / "encode this lesson"
- "audit / validate / verify this"
- "what's still open" / "what's missing"

## Iron Rules (do not skip)

### Rule 1 — Read the substrate FIRST

Before compiling anything, read in this order:

```
1. /root/.local/share/arifos/carry_forward.json — last session's residue
2. /root/.local/share/arifos/carry_forward_backups/*.json — evolution trail
3. /root/.local/share/arifos/scars/SCAR-*.json — failure patterns
4. /root/.local/share/arifos/vault999/audit_chain.jsonl — recent verdicts
5. /root/.local/share/arifos/vault999/seal_chain.jsonl — constitutional chain
6. /root/.local/share/arifos/vault999/seal_chain_head.json — current head
7. /root/AAA/docs/deprecation-registry.json — tombstone inventory
8. arifOS /health + arifFlow /health — current metabolism
```

Do NOT skip. The substrate remembers what your narrative forgot.

### Rule 2 — Distinguish SEAL from RECEIPT before emitting

| Word | Means | Required |
|------|-------|----------|
| SEAL | Lane A constitutional | judge_state_hash + sovereign witness + chain entry |
| RECEIPT | Lane B autonomous | forge_vault + read-back verification |
| SABAR | Lane A honest sub-threshold | gap described in note |
| HOLD/VOID | Gate failure | not a record — re-submit or drop |

**Forbidden:** `verdict=SEAL` without `judge_state_hash` and chain entry. This is precision rot and SCAR-002/KERNEL-LEGACY-VERDICT-LEAK-002 both attest to the damage.

### Rule 3 — Every audit MUST include a SHADOW section

Before claiming victory / cleanliness / completion, enumerate:

```
SHADOW:
- What is unverified? (e.g. chain head age, Lean sorry count)
- What is assumed vs proven? (e.g. carry_forward says SEAL, but is it constitutional?)
- What is missing or stale? (e.g. H-WELL biometric 54h, FLAME retired)
- What floors are PASS vs HOLD vs UNKNOWN? (e.g. F8 G=0.4572 < 0.80)
```

If you cannot enumerate shadow, you have not audited. You have echoed.

### Rule 4 — Compile into entropy-ranked task manifest

For each remaining task, compute:

```
entropy_delta = how much chaos reduces when this is fixed
priority       = P0 (block everything) | P1 (high entropy reduction) | P2 (medium) | P3 (cleanup)
depends_on     = explicit list, not vibes
blocks         = explicit list, enables topological ordering
autonomy_tier  = T0/T1/T2/T3 with F13 sovereignty flags
```

Write to `/root/work/tasks.json` with `$schema: "arifos.work.tasks.v1"`.

### Rule 5 — Encode wisdom into SKILLs, not just docs

Future agents inherit SKILLs (auto-loaded at session start). Docs (doctrine) require lookup. **Encode lessons as skills first, doctrine second.**

Suggested skills to author:
- `BIJAKSANA-compile` (this one)
- `WISDOM-reader` — read scars + carry_forward before claiming
- `SEAL-discipline` — distinguish SEAL from RECEIPT

### Rule 6 — Close with witnessed SABAR, not fake SEAL

If metabolism is sub-threshold (G < 0.80, W3 < 0.75), do NOT claim SEAL. Close as SABAR — acknowledge the gap honestly. The kernel allows SABAR (seal.py line 61). SABAR is constitutional honesty.

## Workflow (canonical)

```
INPUT: user asks to compile/lower entropy
  ↓
1. LOAD this skill
2. READ substrate (Rule 1)
3. DISTINGUISH verdicts (Rule 2)
4. ENUMERATE shadow (Rule 3) — write shadow first
5. COMPILE /root/work/tasks.json (Rule 4)
6. ENCODE wisdom into skills (Rule 5)
7. PROPOSE doctrine patches for F13 ratification (do NOT auto-apply)
8. CLOSE with witnessed SABAR if metabolism < threshold (Rule 6)
  ↓
OUTPUT: manifest + skills + doctrine proposals + close SABAR
```

## Output shape (canonical)

```
Done. Compiled N tasks. ΔS=[entropy delta].
   - P0 (block): [count]
   - P1 (high):  [count]
   - P2 (med):   [count]
   - P3 (cleanup): [count]

3 doctrine patches proposed (F13 ratification pending):
   - PATCH-XXX [title] — entropy delta if applied: [val]

3 skills encoded (load at session start):
   - [skill-1], [skill-2], [skill-3]

SHADOW (what remains unverified):
   - [bullet 1]
   - [bullet 2]

Verdict: [SEAL | RECEIPT | SABAR]
Evidence: [seal_chain seq | forge_vault receipt | carry_forward residue]
```

## Anti-patterns (forbidden)

- ❌ Echoing celebration before reading carry_forward
- ❌ Writing `verdict=SEAL` for Lane B events
- ❌ Patching doctrine without F13 ratification
- ❌ "Closing" a session without enumerating shadow
- ❌ Declaring entropy reduced without measuring (must cite entropy_delta per item)
- ❌ Trusting carry_forward without probing the constitutional chain

## Reference scars (carry these)

- **SCAR-002-CEREMONY_FAILED_406** — 49 sessions failed because seal ceremony had a hard test gate. Tests are verify-phase, not seal-gate. Vocabulary confusion: "test pass" ≠ "seal".
- **SCAR-005** — A doctrine archived out of its declared SoT path is chat history, not constitutional memory. Substrate forgot what it forged.
- **SCAR-KERNEL-LEGACY-VERDICT-LEAK-002** — Truth told twice is truth fractured. One verdict field per response — the canonical one.
- **SCAR-AFORGE-SSE-HANDSHAKE-001** — Discovery handshake needs explicit handling; don't conflate surface reachability with capability.

## Iron Oath

> I will not call RECEIPT a SEAL.
> I will not close a session without shadow.
> I will not patch doctrine without F13.
> I will not celebrate before I have witnessed.
> **Lebih arif, lebih bijaksana, atau tidak sama sekali.**
