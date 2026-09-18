---
name: claim-ledger-integrity
description: "Use when auditing a claim or prediction ledger."
version: 1.0.0
owner: Hermes
risk_tier: low
triggers:
  - "two counters disagree"
  - "calibration is wrong"
  - "accuracy is 0 but records are correct"
  - "predictions never verified"
  - "audit a prediction store"
  - "claim ledger"
  - "verification log"
  - "why is this counter zero"
  - "counter mismatch"
  - "retract a verification"
---

# Claim Ledger Integrity

Use for any store that records a claim, bet, or prediction at birth and its outcome later:
prediction ledgers, calibration stores, claim registries, verification logs, scoring tables.

The failure mode this skill exists to catch is not a crash. It is a ledger that answers
confidently and wrongly — an accuracy figure computed over the wrong denominator, a status
field that can never change, a retraction the read path ignores.

## The invariant

**A read surface over a claim ledger is only as trustworthy as its join.**
If outcomes and claims live in different files, every count derived from ONE file is suspect.

## Procedure

### 1. Enumerate surfaces over the same store

Call every read path that summarises the ledger (census/stats, calibration/score, list, due,
health) and write their numbers side by side. Disagreement between two views of one store is
the primary symptom, and it is usually two different bugs at once.

Concretely: a census reporting `verified: 0` while the scoring surface reports `total: 4` is
not a rounding difference. One of them is reading the wrong field.

### 2. Read the write path before believing the read path

Check whether birth records are immutable. If the writer deliberately freezes the birth
record (status permanently `ACTIVE`) and appends outcomes elsewhere, then the birth status
field is **historical metadata, not current state**. Any count read from it is a permanent
zero — and that is the bug, not a missing feature.

```
birth record  -> status: ACTIVE   (frozen forever, by design)
outcome log   -> append-only, references the claim id
=> current state lives at the JOIN, nowhere else
```

### 3. Hunt vocabulary drift at the boundary

Two writers, or a schema that was revised, produce two spellings of one outcome
(`CORRECT` vs `VERIFIED_CORRECT`, `VERIFIED` vs `ok`, `true` vs `"true"`). A comparison
against only one spelling matches nothing and fails **silently to zero**. Normalise verdicts
at the read boundary against an explicit canonical set; never compare raw strings.

### 4. Audit the verifier itself, not just the ledger

Read the code that writes outcomes and ask, for each branch: *what evidence does this branch
require?* A branch that writes a decisive verdict without observing an outcome is minting
confidence. The classic shape is a date comparison standing in for a measurement — the window
closed, therefore the claim held. That is valid for date-shaped claims only.

### 5. Inspect the log for contamination

Scan for harness/test strings stored as real outcomes against real records. A test value left
in a production ledger is a false witness: a downstream reader cannot tell it from evidence.

### 6. Retract by appending, never by editing

The log is append-only. Retraction writes a superseding VOID record naming what it
supersedes. Then **verify the read path honours it** — a retraction the reader ignores is
worse than none, because the ledger now looks maintained.

## Rules for the repaired read path

1. **Silence is not a verdict.** A check that ran and found no evidence yields
   UNVERIFIABLE — never CORRECT, never INCORRECT. A missed check is not a missed claim.
2. **Time passing is not evidence.** Date passage confirms date-shaped claims only.
3. **Only decisive verdicts enter the ratio.** Excluded records are disclosed alongside it.
4. **State the denominator, not just the ratio.** Report scored AND excluded: unverifiable,
   orphan records with no matching birth record, retracted. A ratio without its exclusions
   cannot be audited.
5. **Orphans are disclosed, never scored.**
6. **An unresolved claim stays open.** UNVERIFIABLE must not remove a claim from the active
   set; only a decisive verdict resolves it.

## Pitfalls

- **Counting UNVERIFIABLE as failure manufactures a lie.** Reporting 0% accuracy over a
  ledger that is partly correct is not the conservative default, it is an active false
  statement. If a system must be pessimistic, be pessimistic in the CONFIDENCE, never in
  the arithmetic.
- **An idempotency check must test for a decisive verdict, not for a row.** A
  "does a row exist" test makes a VOID or UNVERIFIABLE row permanently block
  re-verification — the record can never recover.
- **A counter whose source path is hardcoded cannot be tested.** If a summariser ignores an
  injected store path, no fixture-based test can exercise it, which is how the defect
  survives to production. Treat an un-testable read path as a finding in itself.
- **Report the loop that never closes.** If scheduled cycles log all-zero counters while live
  records exist, the loop is counting its own deltas rather than store state, so a hollow
  cycle is indistinguishable from a quiet one. Name it; do not silently pass.

## Proving a fix to a ledger reader

Use an A/B causal test against production payloads — both code versions loaded as isolated
modules, identical input, diffed output, plus a negative control that must behave the same
under both. See `live-service-ops` for the harness pattern. Assert the OLD tree reproduces
the defect, or you have not proven you found the cause.

DITEMPA BUKAN DIBERI
