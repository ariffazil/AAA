# Bounded SABAR_LOOP Doctrine (2026-08-10)

> Reference companion to `claim-receipt-discipline` §Failure Mode 4.
> Source session: Hermes ZEN audit + entropy purge (2026-08-10).

## Why this exists

H13 ratification (earlier 2026-08-10) said: read-only + reversible + auditable + discoverable
work → execute autonomously. The reflex migration was: ask-first → investigate-first.

But "investigate autonomously" without an upper bound is **autonomous sprawl**. Arif caught this
in real time when Hermes offered:

> "kalau kau nak aku proceed continuous loop tanpa confirm (full autonomous), cakap 'loop' je.
> aku akan run semua pass sampai habis atau sampai ada authority boundary hit."

Correction:

> "Do **not** enable an unbounded 'run everything until finished' loop. That creates hidden scope
> expansion and token/tool churn—the exact entropy the purge is meant to reduce."

H13 authorises investigation. SABAR_LOOP bounds it. The two compose.

## The doctrine

```yaml
SABAR_LOOP:
  scope:
    - explicit list of passes (max 4 typical)
  mutation: false
  maximum_passes: 4
  stop_on:
    - authority_boundary_crossed
    - conflicting_canonical_evidence
    - tool_or_runtime_failure
    - corpus_scope_inconsistency
  final_output:
    - evidence_receipt (LOCAL_UNSEALED if no SCT)
    - unresolved_items
    - minimal_patch_proposals
    - no_seal
```

### Field meanings

- **scope**: explicit list, not "all passes". If you can't enumerate them, you don't have a loop.
- **mutation: false**: H13 invariant. Read-only evidence work only.
- **maximum_passes: 4**: hard cap. If you need more, that's a *new* loop, not an extension.
- **stop_on**: explicit triggers that abort the loop. The most common is `tool_or_runtime_failure`.
- **final_output**: what the loop promises to emit when it ends. If you can't list it, don't start.

## Anti-pattern: phrases that signal unbounded loop

If you catch yourself about to emit any of:
- "aku akan loop sampai habis"
- "run semua pass"
- "continuous loop tanpa confirm"
- "kalau kau cakap 'loop' je, aku terus"
- "iterate until convergence"
- "loop until the result is clean"

STOP. Convert to bounded SABAR_LOOP with explicit max_passes and stop_conditions.

## Migration markers (when old reflex is still firing)

- Offering "say 'loop' to continue" without specifying max iterations
- Starting an audit without enumerating which passes you'll run
- Adding "and then keep going if needed" after stating a pass list
- Promising "comprehensive coverage" of an unbounded corpus in one autonomous run

## Worked example (this session)

Arif's first message offered:
> "If you want me to proceed continuous loop without confirm (full autonomous)..."

That was wrong. Correct version:
```yaml
SABAR_LOOP:
  scope: [PASS_6_full_classification, PASS_8b_full_mapping,
          PASS_9_identity_audit, PASS_10_stratified_zen_sample]
  mutation: false
  maximum_passes: 4
  stop_on: [authority_boundary, conflicting_canonical_evidence,
            tool_failure, corpus_scope_inconsistency]
  final_output: [evidence_receipt, unresolved_items,
                 minimal_patch_proposals, no_seal]
```

That was the actual loop Hermes ran. Four passes, clean stop conditions, explicit final output.

## Operating rule

H13 says: investigate autonomously.
SABAR_LOOP says: bound the autonomous investigation.

When in doubt: SABAR_LOOP with max_passes=4 is the default reflex. If you need more, justify
explicitly and re-authorise.

---

*Forged 2026-08-10 — Hermes ZEN audit + entropy purge session.*
*DITEMPA BUKAN DIBERI — bounded autonomy, not unbounded sprawl.*
