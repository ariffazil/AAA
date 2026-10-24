# SCAR-2026-10-22-003 — A provenance string is not the mechanism

**Class:** agent inference failure — asserted architecture from a log label
**Weight:** w_scar = 0.7
**Filed:** 2026-10-22 · 333-AGI · opencode session (self-filed under F1 AMANAH)

## What I did
In the 12:19Z state report I wrote:

> "F1 gates on the rollup — the 2026-10-18 'rollup = monitoring, not gate' amendment is
> doctrine-only, not yet wired into floor measurement. Rollup != gate is live policy that
> isn't live code."

...derived from ONE string: `/health -> floor_provenance.F1 = "arifflow_fq_probe:fq=0.3333"`.

## What the code actually says (probed 2026-10-22 ~12:4xZ)
- `arifOS/arifosmcp/runtime/rest_routes/rest_routes.py:1247` -> GET `http://127.0.0.1:7073/health` -> `fq.quotient` (the ROLLUP)
- `:1249` -> `_phi_fq_from_quotient()` (`:839`) = `1.0 if quotient >= 0.5 else 0.0` — a STEP, not a band
- `:1258` -> sets `floor_provenance["F1"]` — the string I mis-read
  => The **displayed F1 score** IS the rollup. That part held.
- BUT `arifOS/arifosmcp/runtime/fq_gate.py` (2026-10-19) implements the **ratified per-actor-LANE cap**
  at `arif_init` (`_candidate_lanes(per_actor, actor_id)`), matching `contracts/fq_policy.yaml`
  enforcement plane "arifOS kernel" (F13_RATIFIED_CHAT 2026-09-12).
  => The amendment **IS wired** — at the **enforcement** plane. There is no dead-letter law.

## Failure class
TWO planes collapsed into one:
- **Enforcement** (who gets restricted) -> `fq_gate.py`, per-lane, at session birth.
- **Observability** (`/health` label)    -> federation rollup -> step(>=0.5) -> F1.
A provenance string names the *instrument of the score I was looking at*; it says nothing about
the *gate*. I extrapolated from one to the other, then stated it as a lesson.

## The law
**A provenance string is evidence of an instrument, not of a mechanism.** Before claiming
"policy X is not wired", read the enforcement artifact (`*_gate.py` / `check_verdict.*`) and
name which plane it governs. Representation != Reality applies to my own claims first.

## Correct residual (the finding that survives)
`rollup_formula = "minimum_gated_harmonic_mean"` (`arifFlow/src/main.rs:683`) -> the rollup is
weakest-link **by design**. F1 display = step(rollup >= 0.5). Therefore the kernel reports
`constitutional: degraded` whenever ANY single actor lane is held (4 held at 12:19Z:
anonymous, arif_fazil, fi-002, fi-008). **A floor that turns red whenever one lane is throttled
stops discriminating.** Correct scoping: an observability-semantics question — should the system
label mirror the enforcement-relevant lane state, and report the rollup as a monitoring scalar
(exactly what the 2026-10-18 amendment says)? -> F13/888 design decision, NOT a defect claim.

## Cross-check that also failed (unwitnessed-input admission)
A source document attributed to me an RC table (Federation 0.59 / arifOS 0.83 / A-FORGE 0.81 /
HERMES 0.82 / GEOX 0.39) and `RC = cbrt(PC * CB * LF)`. I produced neither, and neither is on
this box: bounded probe of /root/AAA, /root/scripts, /root/forge_work found no `RealityCoupling`;
`EUREKA_REALITY_ARTIFACT_2026-10-22.pdf` not found under /root /home /tmp /mnt. Unwitnessed input
may not enter my ledger as fact. (The arithmetic itself checks out: (0.30*0.81*0.83)^(1/3)=0.586.)

## Kin
REPRESENTATION-DRIFT THEOREM (2026-10-22T10:20Z) · representation-reality-invariant
(two probes, one map) · L0-L4 cascade doctrine (L1 source < L3 runtime) · evidence-hierarchy.
