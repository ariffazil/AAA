# FORGE-route-least-power v2 — Two-Axis Routing Gate
**Forged:** 2026-08-03 · **Status:** CANDIDATE (awaiting F13 SEAL)
**Supersedes:** FORGE-route-least-power v1 (capability-only axis)
**Eureka source:** Session 2026-08-03 — E4 (Two-Boundary Theory of LLM Math) + E7 (Scratchpad-Engine Distinction)

---

## WHAT CHANGED

**v1 doctrine:** Route every task to the smallest capability that can accomplish it. One axis: capability boundary. "Can the LLM do this? If not, route to an organ that can."

**v2 upgrade:** Route to the smallest capability whose *per-step error does not compound* to unacceptable levels over the task's step count. Two axes: capability boundary AND error-accumulation boundary. "Even if the LLM CAN do this (via scratchpad/CoT), does its irreducible per-step error compound to failure over the required step count?"

---

## THE TWO AXES

### Axis 1 — Capability Boundary (HARD)

| Condition | Action |
|---|---|
| Task is ABOVE the LLM's single-pass ceiling (e.g., exact large arithmetic, deterministic long-chain reasoning) | Route to exact engine (Python, GEOX, WEALTH) — **structural impossibility** |
| Task is WITHIN the LLM's single-pass ceiling (e.g., summarization, translation, sentiment) | Pass to Axis 2 |

### Axis 2 — Error-Accumulation Boundary (SOFT)

| Condition | Action |
|---|---|
| Task step count × LLM per-step error rate > acceptable threshold | Route to exact engine — **unreliability, not impossibility** |
| Task step count × LLM per-step error rate ≤ acceptable threshold | LLM may proceed (with verification) |
| Task has zero-tolerance for error (financial transfer, irreversible mutation, geological claim) | Route to exact engine — **regardless of step count** |

---

## THE GOVERNING EQUATION

```
route_to_exact_engine = (step_count × per_step_error_rate > ε_max)
                      ∨ (task_requires_zero_error)
                      ∨ (task_above_single_pass_ceiling)
```

Where:
- `step_count` = number of sequential reasoning/execution steps required
- `per_step_error_rate` = estimated probability of error per step (LLM ≈ 0.01–0.05 for complex reasoning; exact engine = 0)
- `ε_max` = maximum acceptable cumulative error (domain-dependent)
- `task_requires_zero_error` = financial, irreversible, geological claims, constitutional changes
- `task_above_single_pass_ceiling` = the hard boundary (E4)

---

## FEDERATION EXAMPLES

| Task | Axis 1 (Capability) | Axis 2 (Error Accum.) | Routing Decision |
|---|---|---|---|
| Large multiplication | ABOVE ceiling | — | Route to Python |
| Medium multiplication via CoT | Within reach | 40 carries × 0.03 error/carry → compounding → unacceptable | Route to Python |
| Geological claim (basin interpretation) | Within reach (LLM can sound plausible) | Zero-tolerance — claim must be falsifiable | Route to GEOX `geox_falsify` |
| Irreversible mutation (rm -rf, DROP) | Within reach | Zero-tolerance — no undo | Route to `arif_judge` → F13 |
| Code generation | Within reach | Moderate step count, errors caught by compiler/tests | LLM may proceed → verify |
| Summarization | Within reach | Single step, low stakes | LLM may proceed |
| Portfolio NPV calculation | Within reach (LLM can approximate) | Zero-tolerance — capital decision | Route to WEALTH `capital_primitive` |
| Vitality assessment | Within reach | Zero-tolerance — human substrate | Route to WELL |

---

## WHY THIS UPGRADE MATTERS

**v1 fails in the dangerous middle:** v1 only routes when the LLM *cannot* do something. But the LLM *can* do many things approximately via chain-of-thought — including arithmetic that's 99% right, geological claims that sound plausible, and financial estimates that look reasonable. v1 lets these through. v2 catches them on the error-accumulation axis.

**The soft boundary governs the cases where the LLM looks capable and quietly isn't.** These are exactly the cases where agents typically skip routing because the LLM's output is fluent, confident, and superficially correct. v2 closes this gap by making error-accumulation an explicit gate, not an afterthought.

**This is the architectural justification for GEOX/WEALTH/WELL routing even when the LLM can produce domain-sounding answers.** You don't route to GEOX because the LLM cannot reason about basins (it can, roughly). You route because the LLM's per-claim error is nonzero and compounding, and GEOX's falsification engine (K001–K007) drives it to zero. Same for WEALTH capital math and WELL vitality assessment.

---

## INTEGRATION WITH EXISTING DOCTRINE

- **F2 TRUTH:** The error-accumulation axis is an operationalization of F2 — "probability of truth must be ≥ 0.99." For multi-step tasks, P(truth) = (1 − per_step_error)^step_count. v2 enforces this before execution.
- **F1 AMANAH:** The zero-error-tolerance override ("task_requires_zero_error") is the F1 gate for irreversible actions.
- **FORGE-route-least-power v1:** Preserved as the Axis-1 check. v2 adds Axis 2, not replaces.

---

## LIMITS

1. **Per-step error rates are estimates, not measurements.** An empirical calibration study across task classes would strengthen the gate from heuristic to operational.
2. **The threshold ε_max is domain-dependent and currently set by agent judgment.** Formalizing per-domain ε_max (financial: 0.001, geological: 0.01, creative: 0.10) would make the gate programmable.
3. **This does not address adversarial CoT** — an LLM could learn to produce convincing scratchpad steps that are systematically wrong. The soft boundary assumes independent per-step errors; correlated errors are a harder class.

---

**Status: CANDIDATE.** Skill upgrade ready for integration into `FORGE-route-least-power` SKILL.md. Awaiting F13 SEAL.

*DITEMPA BUKAN DIBERI — forged on two axes, not one.*
