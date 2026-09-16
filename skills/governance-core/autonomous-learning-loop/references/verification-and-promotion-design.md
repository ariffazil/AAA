# Verification & Promotion Design — reference tables

Depth for `autonomous-learning-loop`. Load when designing the atom schema, extending
the taxonomy, or choosing what a check should re-derive against.

## Atom schema (minimum fields)

```yaml
atom_id:      stable hash of the normalised signature   # same failure → same id
signature:    normalised claim (strip uuids, hashes, paths, digits)
pattern_type: one of the closed taxonomy
layer:        skill | capability | policy | judgment | governance
claim:        one line, states what was observed and its measured impact
evidence:     [ {layer, source, excerpt} ]              # layer must match the claim
evidence_layer: dominant class of the evidence
falsifier:    what would prove this wrong, testably
frequency:    integer, counted from distinct sources
impact:       what it cost, in concrete terms
target:       the capability this atom attaches to
status:       candidate → verified | rejected | quarantined
survived_verification: bool
promotion:    the outcome receipt
```

Normalise BEFORE hashing: the same failure seen twice must collapse to one atom id, or
recurrence is unmeasurable. Strip volatile parts (ids, hashes, absolute paths, digits).

## Closed failure taxonomy (extend only by sovereign edit)

| Pattern | Meaning |
|---|---|
| `PATH_DRIFT` | two names/paths for one thing — case, symlink, legacy dir |
| `REGISTRY_MISMATCH` | declared surface != live surface |
| `DUPLICATE_SOT` | two sources of truth for one fact |
| `DEAD_POINTER` | a cited artifact no longer resolves |
| `QUEUE_BLOCKED` | ingest jammed, retrying the same unit forever |
| `SILENT_FAIL` | failure swallowed by a default or fallback |
| `SELF_EVAL` | producer grades its own output |
| `PROXY_REALITY` | secondary representation treated as primary ground truth |
| `LAYER_MISMATCH` | claim layer != evidence layer |
| `TRUNCATION_LOSS` | silent head/tail cut mistaken for the whole |
| `PERMISSION_DRIFT` | declared authority != effective authority |
| `HUMAN_BURDEN` | work collapsed back onto the principal |
| `RESOURCE_WASTE` | paid/idle capability unused |
| `UNCLASSIFIED` | taxonomy cannot name it → quarantine, never promote |

Keep the taxonomy closed and small. An open taxonomy turns every session into a new
category and makes recurrence uncountable.

## Independence classes

| Class | Test | May do |
|---|---|---|
| `SELF` | producer == verifier | nothing — rejected |
| `NOMINAL` | different names, same author | enter the graph as PROVISIONAL; no survival, no rule proposed |
| `STRUCTURAL` | distinct authors | record survival |
| `EXTERNAL_ORGAN` | different agent, or a durable external receipt | record survival and back a judgment-layer claim |

Determine authorship from a declared map, not from the label. A name-level check passes
while one hand wrote both modules.

## What each check re-derives against

| Pattern | Re-derive against |
|---|---|
| path / pointer claims | the live filesystem, exact names |
| registry / surface claims | the live artifact tree, counted |
| queue claims | the queue directory's current contents |
| authority / burden claims | the live config and scheduled surfaces |
| anything else | a generic independent observer (health of the designated observer organ) |

If the check cannot resolve a concrete token to re-derive, **fail the check** — "no
resolvable evidence" is not a pass. An exception during re-derivation is a FAIL, not a
skip.

## Consequence measurement

```
baseline_occurrences  ← recurrence of the pattern in the window before promotion
promoted_at           ← when the promotion landed
after_occurrences     ← recurrence in the window AFTER promoted_at
```

Verdicts and their probes:

| Verdict | Probe |
|---|---|
| PERSISTED | after ≤ 0.5 × baseline |
| PARTIAL | after < baseline, but not by half |
| NO_EFFECT | within ±10% of baseline |
| REGRESSED | after > baseline |
| PENDING | elapsed < one full window — report "not yet observable" |

A backfilled baseline (for a promotion that predates the instrument) must be marked as
backfilled and dated at backfill time, so it can never claim a full-window verdict for
the period before its instrumentation existed.

## Boundary self-test (run every cycle)

Attempt each of these and assert refusal: the constitution, the canon tree, the kernel
package, the loop's own config, the loop's own verifier, the loop's own gate module,
the loop's own lock module, and the principal's persona/identity file. A leak is
reported as a HOLD outcome, never as a warning.
