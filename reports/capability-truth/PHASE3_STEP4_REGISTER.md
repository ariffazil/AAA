# PHASE 3 · STEP 4 — Status-Plane Contradiction Register (333-AGI, 2026-09-18)

> Live capture: `preflight_before.json` (arif_init mode=preflight, anonymous, 2026-09-17T20:09Z).
> **Patch deliberately deferred** — this is the shared verdict envelope used by EVERY tool.
> Additive labels = schema (fast); collapsing/merging verdict fields = constitution-adjacent (§22).
> Decision-ready package for F13/888 below.

## The measured contradictions (all in ONE response)

| # | Duality | Field A | Field B | Same call? |
|---|---|---|---|---|
| 1 | reason_code | top `NEEDS_REVIEW` | `result.reason_code=DEPLOYMENT_DRIFT` | yes |
| 2 | substrate truth | `substrate.state=DEGRADED` | sesat `observed_reality: substrate_scope=HEALTHY` | yes |
| 3 | nine_signal | root `{overall: RETAK}` | `meta.nine_signal.overall=BELUM_SAH/UNAUTHENTICATED` | yes |
| 4 | failed floor | `constitutional_check.failed_floors=["L11"]` | `meta.failed_floors=["F11"]` | yes |
| 5 | next action | top `next_safe_action: "Proceed to arif_observe…"` | `result.next_action=RECONCILE_SOURCE_BUILT_DEPLOYED` (BLOCKED) | yes |
| 6 | actor coercion | top `actor_id="anonymous"` | `meta.reason="actor_id required — null not coerced"` | yes |
| 7 | execution naming | top `execution_state=AWAIT_INPUT` + `status_scope=execution` | `result.execution_state=BLOCKED` | yes |

Prior art in code (already partially done): `session.py` ~706 `session_authority_state` split (APEX-777), `constitutional_check._stab_fix="2026-08-07-P0-dual-truth"`, `_derivation="attach_effective_verdict:degraded_dominates"`.

**Cross-reference (cycle 12 forensics):** an in-flight uncommitted package in the sibling clone (`/opt/arifos/arifosmcp`, 5 files, Sep 17 03:04) targets this same defect family: C1 substrate split, C3 `DEGRADED→HOLD` fail-closed (semantic), C4 synthetic-data annotation, plus vocabulary canonicalization. See `SUBSTRATE_FIX_LINEAGE.md`. Collision with staged `cb2411928`: **disjoint**.

**Duality #8 (new):** hold-verdict spelling — `"888_HOLD"` (`abi/amanah_gate.py`, `schemas/budget_contract.py`) vs canonical `"HOLD"` (`runtime/verdict.py:57`). The in-flight package already fixes this.

## Code sites (assembly points)
- `runtime/verdict.py:363` `attach_effective_verdict()` + `:455` `degraded_dominates` — builds `constitutional_check`/`effective_verdict`.
- `runtime/contradiction_detector.py:264-266` — maps verdict→`execution_state` (`HOLD→AWAIT_INPUT`), `status_scope`.
- `tools/session.py:695-720` — session token: `substrate_state` vs `session_authority_state` (partial split, APEX-777).
- `runtime/tools.py:224 / 8204`, `verbosity.py:445`, `authority_middleware.py:173` — `DEPLOYMENT_DRIFT` reason sites.
- Output wrapper (top-level `status/verdict/reason_code/execution_state` + `next_safe_action: "Derived from result"`).

## Fix options (for F13/888 decision)
- **Option A — additive plane namespacing (schema-only, minimal risk):** emit `planes: {transport, operation, governance, authority, persistence}` with each field namespaced; keep legacy top-level fields as aliases marked `plane_of:` provenance. No verdict semantics change. Cheap, reversible, satisfies "no plane reports success while another reports failure" by making the claims explicit. Est: 1 focused block.
- **Option B — single-source collapse (semantic):** one verdict → one reason_code; top-level = projection of ONE plane (execution). Removes dualities but changes envelope semantics for all tools. Needs 888 + full regression suite. Est: 1–2 sessions.
- **Recommended:** A now (labels only), B later under F13 with the STEP 1/5 KPIs as safety net.

## Also flagged
- `meta.sesat_event.failure_code="JALAN_BENAR"` on a HOLD of correct fail-closed behavior — severity semantics anomaly worth a line in the SESAT taxonomy pass.
- `.bak-333-20260918` + `preflight_before.json` = evidence anchors for any future diff.
