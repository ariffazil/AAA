# Probing a metric that reports MEASURED

> One line: a number wearing `status: MEASURED` is a claim like any other. Recompute it, and test
> whether it can move at all.

## When to reach for this

- A scalar governs a gate (floor, threshold, promotion criterion) and never changes across
  restarts, deploys, or days.
- The same scalar reads differently on two surfaces of one machine — one says a value, another
  says `null`.
- A learning or promotion loop shows no output (0 lessons, 0 promotions) while its inputs look busy.
- A component's own comment says the value should be `None`/UNMEASURED, but a payload shows a number.

## Procedure

1. **Grep the surfaced field to the function that builds it.** Do not reason about the value; find
   the arithmetic.
2. **Tabulate every input's provenance.** This is the whole finding — and it is a table, not prose:

   | Input | Value used | Provenance |
   |---|---|---|
   | channel A | 0.42 | a module-level fallback constant |
   | channel B | 0.99 | a literal in the function body |
   | channel C | 0.99 | a *boolean* (`if <condition>`) wearing a number |

   Any input whose provenance is not "measured" is a fabrication candidate.
3. **Recompute by hand.** If `reported == f(constants)` to the digit, the status label is wrong —
   the value is arithmetic on defaults, and no observation can change it.
4. **Find the falsy-merge line.** The usual mechanism is one comprehension that hands the default
   the win exactly when the real channel is missing:

   ```python
   resolved = {k: src.get(k) if src.get(k) is not None and src.get(k) != 0 else v
               for k, v in DEFAULTS.items()}
   ```

   `0` and `None` both mean *absent*, so absence is silently converted into a value — and a
   zero-valued real reading is indistinguishable from no reading. Presence must be tested with a
   sentinel, not with falsiness.
5. **Test mobility explicitly: can this number change?** Name the single observation that would
   move it. If no such observation exists, it is a fixed gate, not a measurement — and it will
   report the same figure forever while appearing to measure continuously.
6. **Enumerate every implementation of the same scalar and determine which one SURFACES.** This is
   the step that is usually skipped, and it is the one that matters. One codebase can define the
   same quantity twice:

   | Implementation | Behaviour | Surfaces to clients? |
   |---|---|---|
   | module A | returns `None` — honest, per its own comment | no |
   | module B | returns a constant from three defaults | **yes** |

   The honest implementation is invisible; the inflated one ships. When two definitions of one
   quantity exist, the defect is not "which is correct" but **"the wrong one is wired to the
   surface"** — and the honest sibling is the proof that someone already knew the value was not
   measurable. Corollary: the *disagreement between surfaces* is a downstream symptom. Fix the
   wiring; do not average the two.
7. **Check the threshold consequence, in the gate's own units.** Compare the constant against the
   floor it is supposed to gate. A constant that sits permanently *just below* its own floor is the
   worst case: the gate is perpetually failing, cannot pass, and cannot be repaired by any
   improvement in the system — every downstream HOLD is an artifact of the constant.

## Reporting shape

State, in this order: the reported value and its label · the formula · the input-provenance table ·
which implementation surfaced versus the honest sibling · the consequence at the threshold. Hand the
choice back rather than picking it: (a) make it honestly UNMEASURED until a real channel exists
(remove > duplicate), or (b) wire a real channel. Both are usually one file; neither is a new organ.

Flag the transitional risk with the recommendation: honest `None` will make dependent gates HOLD
more often, and that is **correct behaviour, not a regression** — say so explicitly, or the next
reader will read the increased refusals as a new fault and revert it.

## The rule

**A metric that cannot move cannot govern.** Before crediting any gate, floor, or promotion with
having decided anything, establish that its input can vary — otherwise the system is governed by a
constant, and every verdict that cites it is describing the constant rather than the system.
