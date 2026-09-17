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

---

## Live specimens — post-reconciliation (333-AGI, 2026-09-18 20:34–20:42Z, deployed 60b9c0f)

**Duality #9 (judge lane) — wrapper HOLD on intercept ALLOW.** `arif_judge` on a reversible, floor-clean candidate (push+deploy reconciliation):
- intercept: `decision=ALLOW`, "Action authorized under standard capability bounds", `failed_floors=[]`, chain `cc_07f05c3aafd27759d5961aa80fda1511e1417e90` minted, `reversibility: REVERSIBLE`, `requires_human_signature: false`.
- wrapper: `effective_verdict=HOLD` via `_derivation=attach_effective_verdict:degraded_dominates`; `_wrapper_degradation=["inner verdict=HOLD"]`.
- sesat: `failure_code=JALAN_BENAR`, `failed_claim="HOLD: Action authorized under standard capability bounds."`, `observed_reality: status=OK, substrate_scope=HEALTHY`, remediation `inspect_and_retry (max 1)`.
- Classification: status-plane collapse, NOT a floor refusal. Action executed under F13 order with divergence logged; no success claimed pre-verification.

**Duality #10 (boot attestation) — session plane reads an unseeded in-memory registry.** After drift cleared, `session_authority_state`: `DEPLOYMENT_DRIFT → BOOT_ATTESTATION_FAILED` (branch order `tools/session.py:705-710`).
- Root cause: `get_organ_attestation("arifOS")` reads `_ORGAN_REGISTRY` (`organ_attestation.py:122`), populated ONLY by an attestation call; nothing seeds it at boot. Absence → `UNATTESTED` → `is_healthy()=False` → `_boot_unhealthy=True`. Masked until now: `_drift` short-circuited the branch.
- Simultaneity: `/health` shows `boot_attestation: true`, `deployment_drift_status: aligned`, `degraded_reasons: []` while `execution_readiness: held` — three surfaces, three stories.
- Heal attempted: `POST /tools/arif_kernel_attest/call` → correctly gated (`ART_EVIDENCE_INSUFFICIENT`). Gate works; runtime seeding rejected as the wrong fix.
- **Required fix (engineering intake):** seed self-attestation at boot (or first init), OR treat registry-absence as "must attest" rather than "failed". Postcondition: `execution_readiness=ready` + `session_authority_state=VERIFIED` converge.

**Parallel-lane note (do not duplicate):** at 20:42Z `/root/arifOS` carried 4 uncommitted files from another lane — `constitutional_map.py`, `resources/schema.py`, `schemas/memory_modes.py`, `tool_discovery.py` — consistent with steps 3–4 (schema/runtime mismatch + mode authority) in flight. Left untouched.
