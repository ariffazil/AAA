# Verdict-Field Divergence — post-redeploy reproduction + hypothesis refutation (2026-10-06)

**Status:** REPRODUCED 3/3 · root-cause candidate advanced · not auto-implemented
**Reporter:** FI-008 (kimi-code) · session SEAL-50a696aa9d854a11 → SEAL-356199e374d94c37
**Bundle:** belongs in the same kernel review as `kernel-actor-mismatch-falsehold-2026-10-02.md` (per AGENTS.md row intent: "bundle for one kernel review")

## Defect signature

Same kernel build, same session, 13 seconds apart:

- `arif_init` (18:41:50Z): substrate **HEALTHY**, drift=false, runtime CONVERGED, source==built==deployed==`c98e9a6b`, constitutional_state OPERATIONAL, token verdict.state **OK**
- `arif_think(mode=plan)` (18:42:03Z): `substrate_state: DEGRADED`, `INCONSISTENT_STATE: VERDICT_FIELD_DIVERGENCE` (fields split OBSERVE_ONLY ↔ HOLD), L13 fail, `meta.reconciliation.inconsistent=true`, reconciled fail-closed → HOLD

The kernel's own reconciliation layer catches the contradiction every time and reconciles to HOLD (fail-closed — safety holds; coherence does not).

## Reproduction (all timestamps UTC 2026-10-05)

| # | token | call | result | call_hash |
|---|---|---|---|---|
| 1 | pre-redeploy (SABAR.DEGRADED embedded) | arif_think plan | HOLD + VERDICT_FIELD_DIVERGENCE | ac39c03f… |
| 2 | fresh post-redeploy (OK embedded) | arif_think plan | HOLD + VERDICT_FIELD_DIVERGENCE | 5a150493… |
| 3 | (corroboration, other lane, pre-redeploy) | arif_think plan | L13 HOLD, OBSERVE_ONLY ↔ HOLD divergence | — |

## Hypothesis tested and REFUTED

**H:** divergence stems from stale ACT-embedded verdict state (pre-redeploy tokens carrying SABAR.DEGRADED).
**Test:** bind fresh post-redeploy session (token verdict.state=OK) → rerun same probe.
**Result:** identical divergence → hypothesis refuted. The defect survives a clean token on a healthy substrate.

## Root-cause candidate (measured)

In the think-path response: `verdicts.substrate.evidence_reference = "affordance_narrowed: HOLD → OBSERVE_ONLY (…)"` — the wrapper's OWN degradation note is consumed as substrate-degradation evidence by the scoped-verdicts layer, while `arif_init` derives substrate from live runtime attestation (`runtime_attestation_injected` → HEALTHY). Two substrate derivations, two truths, one response. Self-referential: the narrowing note is an output of `_compute_canonical_verdict`, then re-enters as evidence.

Observed scope: 333-lane `arif_think` **mode=plan** (3/3). mode=reason on the old token held for a *different* reason (empty evidence block) without the divergence flag — scope may be plan-family-specific; untested on other verbs.

## Impact

- Every plan-family 333 call lands HOLD on a healthy substrate → plan/approve lifecycle effectively blocked.
- All governed responses carry contradictory verdict fields → downstream consumers cannot know which field is canonical (L13 integrity cost).
- Fail-closed everywhere: no safety breach; this is a coherence defect, not an authorization bypass.

## Fix direction (for kernel review, not auto-implemented)

1. One canonical verdict function: raw evidence → single `effective_verdict` → projections. No wrapper may independently reinterpret (already the analysis-level intent; now evidenced).
2. Substrate truth must derive from live attestation only; wrapper degradation notes are outputs, never inputs (break the self-reference).
3. Regression: plan-mode call on healthy substrate must show zero `VERDICT_FIELD_DIVERGENCE` flags across old AND fresh tokens.

## Provenance

Trigger: sovereign-p forwarded lane analysis claiming two P0s (runtime truth; verdict singularity). P0#1 (runtime truth) was already resolved by the 18:32:48Z reconcile deploy — the forwarded probe predated it (stale map). P0#2 confirmed live by this report.
