# SELECTIONS LEDGER SPEC — selections.jsonl

> **Status:** PROPOSAL_AWAITING_F13 (parent: EUREKA-IDENTITY-METABOLISM-2026-09-09 — also awaiting ratification)
> **Cross-links:** EUREKA-2026-09-09-WRITE-PRICE-COLLAPSE-001 (entry 65) · EUREKA-SESSION-2026-09-KVM8 #3 (TAC) · EUREKA-2026-09-07-VERIFICATION-GRADIENT-001 (Law #5) · P-DIAL closure schema (canon-locked)
> **Forged:** 2026-09-09 · FI-008 from F13-chat interpret session
> **DITEMPA BUKAN DIBERI**

## Why first (build order rationale)

Selection recording is the only **LEARN-axis** instrument that makes every expensive axis measurable. `predictions.jsonl` records what was expected about the *world*; nothing records what was chosen among *paths* and why. Without it: no observable judgment, no TAC on decisions, no scar target (a scar cannot know what to change), no identity crystallization ("behavior exists but identity does not crystallize" — parent doc).

## Schema (one JSON object per line, append-only)

```json
{
  "ts": "2026-09-09T00:00:00Z",
  "actor": "FI-008-kimi",
  "session": "SEAL-...",
  "decision_context": "deploy_fix_or_hold",
  "axis_of_selection": "DECIDE",
  "candidates": [
    {"path": "fast_deploy", "score": 0.89, "method": "heuristic"},
    {"path": "verify_first", "score": 0.77, "method": "scar_weighted"}
  ],
  "selected": "verify_first",
  "reason": ["reliability_over_speed", "scar_224", "witness_required"],
  "constraints_hit": ["F1_REVERSIBILITY", "no_pretending"],
  "expected_outcome": "verified deploy, +2min",
  "attention_cost_min": 3,
  "outcome": {"filled": false},
  "closure": {"mode": null, "reason_code": null, "scar_link": null}
}
```

**Lifecycle:** selection written at decision time (cheap). `outcome` and `closure` **backfilled by link, never by edit** — a second record `{ref: <selection_id>, outcome: {...}, closure_mode, reason_code, scar_link}`. Immutable append discipline throughout; the ledger itself is LEARN-priced.

`closure` fields reuse the P-DIAL proposal vocabulary (CONTINUE / CLOSE_ACT / CLOSE_HOLD / CLOSE_SABAR + reason codes) — this ledger is the instrumentation that proposal said was required before sealing.

## Consumers (in build order)

1. **Scar metabolism (#2)** — scar candidates evaluate against selection history: which constraint/weight would have flipped the selection. No selection record → scar has no target.
2. **Invoice adaptation (#3, GATED)** — invoices update judgment weights **only through promoted scars**, never directly. Axis-split: auto-adapt permitted on LEARN axis (thresholds, world model); identity (BE axis) never auto-writable. *(WRITE_PRICE_COLLAPSE correction — invoice is unbuyable, judgment updates are scar-priced.)*
3. **Attention budgeting (#4)** — `attention_cost_min` accumulates into ACSC.
4. **Identity semantic survival (#5)** — emergent: constraint persistence measured as selection consistency under load.

## Integration (unify, don't duplicate)

Existing partial ledgers to reference (not copy): `experience_traces` (action→feedback), `predictions.jsonl` (world expectations), skill_select events (SkillGate), arifFlow receipts (step class). selections.jsonl is the decision-point ledger those lack.

## Non-goals

- No auto weight updates from invoices (gate = scar promotion).
- No identity writes from this ledger, ever.
- Not a verdict store — selection ≠ judgment quality until outcome backfilled.

## Falsifier

If judgment-quality metrics (closure-mode distribution, exception escalation rate, scar promotion precision) show no measurable difference between recorded-selection and unrecorded-selection periods under equal load → the selection-ledger hypothesis is falsified; seal as scar.

## Zen

```
Prediction records what the world owed.
Selection records what the agent chose to pay.
Scar explains why the price was right or wrong.
```
