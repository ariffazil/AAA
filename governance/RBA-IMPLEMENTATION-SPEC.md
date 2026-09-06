# RBA Implementation Spec — Reality-Bound Authority

> **Forged:** 2026-09-07 · **Session:** `SEAL-685d136316d3486e` · **333-AGI Δ MIND**
> **Status:** ACTIVE spec — Phase 0/1/2/3 build plan
> **Companion to:** `/root/AAA/instructions/anti-shadow-architecture.md` + GENESIS/060 DRAFT
> **DITEMPA BUKAN DIBERI**

---

## 0. Authority and Precondition

- **This spec is T1/T2 executable** — file writes, schemas, draft specs.
- **T3 ratification blocked** by (a) Lane A SABAR 26-day carry-forward (seal_chain seq 45, 2026-08-11) and (b) G = 0.31 PATHOLOGICAL (F8 requires G ≥ 0.80 for constitutional changes).
- **Quad witness readiness** (2026-09-07): 1.5/4 ready. Human ✅, Earth ⚠ (WELL degraded, FLAME DOWN, FQ=0.5), AI falsifier ❌ (T20), Counterparty ❌ (T13). Shadow mode is the only honest path.

---

## 1. The 10 Missing Primitives (Mapped)

| # | Primitive | Tier | Owner agent | Phase |
|---|---|---|---|---|
| **G1** | Authority Contraction (graded AC-0..AC-5) | T3-bound (forge T2) | 777-FORGE + arifOS-kernel | Phase 1 shadow, Phase 2 reversible, Phase 3 ratify |
| **G2** | W⁴ Counterparty Witness Registry | T2 forge | WELL-organ | Phase 1 |
| **G3** | Epistemic Regime Typing (A/B/C) | T2 forge | arifOS-kernel | Phase 0 (spec done in 060) → Phase 1 stamp on envelope |
| **G4** | dA/dt ≤ dV/dt invariant | T3 ratify (after measurement exists) | arifFlow + arifOS-kernel | Phase 3 |
| **G5** | Pain-Routing Detector (Q10 extension) | T2 forge | 777-FORGE | Phase 1 |
| **G6** | Lag-Aware Outcome Receipts (H0..H3) | T2 forge | 777-FORGE | Phase 1 |
| **G7** | Independent Falsifier Channel (isolation) | T2/T3 architectural | A-FORGE + arifOS-kernel | Phase 1 logical, Phase 2 model diversity |
| **G8** | Multi-KPI Floor (K-vector) | T2 forge | arifFlow | Phase 1 |
| **G9** | Outcome-Attribution Reward | T3 design + ratify | arifFlow | Phase 2 |
| **G10** | Probe-Before-Intent (G10 enforcement) | T1 code | arifOS-kernel | **Phase 0** — smallest blast radius, do first |

---

## 2. Phase 0 — Draft Only (this session, T1)

Goal: zero new autonomous permissions, schemas only, F2 evidence in commits.

| ID | Task | Path | Tier | Status |
|---|---|---|---|---|
| **T01** | Anti-shadow-architecture instruction | `/root/AAA/instructions/anti-shadow-architecture.md` | T1 | ✅ done |
| **T02** | GENESIS/060 draft | `/root/arifOS/GENESIS/060_ANTI_SHADOW_ARCHITECTURE.md` | T1 | ✅ done |
| **T03** | reality-bound-authority canon | `/root/AAA/instructions/reality-bound-authority.md` | T1 | ✅ done |
| **T04** | NIST/OECD cross-walk | `/root/AAA/research/nist-rmf-oecd-mapping.md` | T1 | ✅ done |
| **T05** | First anti-shadow audit | `/root/AAA/reports/anti-shadow-audit-2026-09-07.md` | T1 | ✅ done |
| **T06** | TypeScript schemas (inline in 060 §4) | inline | T1 | ✅ done (in 060) |
| **T07** | Spec rollout order | this file | T1 | ✅ done (this file) |
| **T08** | FLOOR_TABLE.json DRAFT amendment (never commit) | local-only draft | T1 | ⏳ deferred to T22 |

**Phase 0 net:** doctrine, schemas, audit, mapping, spec. Zero autonomous permissions granted.

---

## 3. Phase 1 — Shadow Mode (T2, announce 10s)

Goal: `authority_contract()` runs in observe-only. Calculate AC recommendations but do not restrict existing agents. Record FP/FN/missing-data.

| ID | Task | Owner | Deliverable | Verify |
|---|---|---|---|---|
| **T09** | `forge_authority_contract()` in A-FORGE | 777-FORGE | Python module (observe-only) | unit tests cover AC-0..AC-5 trigger matrix; FP/FN log populated |
| **T10** | Stamp `epistemic_regime` on every `arif_init` envelope | arifOS-kernel | kernel patch | every arif_init log shows regime; legacy = B default |
| **T11** | `forge_pain_route_detect()` extends Q10 | 777-FORGE | Python module | unit tests on synthetic ConsequenceMaps |
| **T12** | `forge_lag_audit()` registers VerificationHorizon on consequential actions | 777-FORGE | Python module | receipt lifecycle test passes (T+1min/1d/7d/30d) |
| **T13** | `well_counterparty_registry` extends WELL consent_scope | WELL-organ | state.json schema + MCP tool | live tool callable, F11 audit |
| **T14** | `reality-bound-authority-auditor` skill | 333-AGI (skill forge) | skill manifest + audit receipt schema | A-AUDIT runs new checks, emits receipts |
| **T15** | Run anti-shadow audit on F1–F13 + Q9–Q11 with new skill | A-AUDIT | `/root/AAA/reports/anti-shadow-audit-{date}.md` | every "pain-alone-without-contraction" gap listed |
| **T16** | `forge_multi_kpi()` in arifFlow | arifFlow | Python module + new /health K-vector | live /health returns KPI vector alongside FQ |

Phase 1 duration: **minimum 30 days** to accumulate shadow-mode evidence before Phase 2.

---

## 4. Phase 2 — Reversible Enforcement (T2/T3 boundary, F13 watch)

Goal: enforce AC-1 and AC-2 only for low-risk, Type A, reversible actions. W⁴ required only on explicitly identified Type B/C counterparty cases.

| ID | Task | Owner | Deliverable |
|---|---|---|---|
| **T17** | Enforce AC-1 + AC-2 in shadow mode | arifOS-kernel | kernel patch + dryrun reports |
| **T18** | Require W⁴ registration on Type B/C cases | arifOS-kernel | kernel patch + counterparty_case_log.jsonl |
| **T19** | Register outcome-horizon for new high-J workflows | 333-AGI + A-FORGE | workflow_horizon_registry.json |
| **T20** | Independent Falsifier Channel — logical isolation | A-FORGE + arifOS-kernel | architectural decision + isolation contract |
| **T21** | Outcome-attribution reward design | arifFlow | design doc + reward function |

Phase 2 duration: **minimum 60 days** of clean shadow-mode evidence before Phase 3 ratification gate.

---

## 5. Phase 3 — F13 Ratification Gate (888_HOLD)

**Precondition (T22):** Resolve 26-day Lane A SABAR (carry-forward: `seal_chain seq 45, 2026-08-11`). Without this, the R-BAP cannot ratify because the queue mechanism is itself the test.

| ID | Task | Owner | Deliverable |
|---|---|---|---|
| **T22** | Close Lane A SABAR | F13 (Arif) | ratification packet + carry-forward items resolved |
| **T23** | Promote GENESIS/059 DRAFT → CANON | F13 (Arif) | FLOOR_TABLE.json amend F13 with Reality-Vote reinterpretation |
| **T24** | Promote GENESIS/060 DRAFT → CANON + commit F14 + F15 amendments | F13 (Arif) | FLOOR_TABLE.json amend F3 (W⁴), add F14 (AUTHORITY_CONTRACTION), add F15 (GROWTH-COUPLING) |

---

## 6. TypeScript Schema Definitions (T03–T06 consolidated inline)

```ts
// G1 — Authority Contraction
type AuthorityEnvelope = {
  agent_id: string;
  action_classes: string[];
  max_risk_tier: 0 | 1 | 2 | 3 | 4;
  execution_mode: "observe" | "recommend" | "simulate" | "execute";
  max_confidence_claim: number;        // 0.0 .. 0.97
  budget_cap?: number;
  routing_scope: string[];
  expiry_at: string;                    // ISO-8601
  reauth_required: boolean;
  basis: EvidenceRef[];
  epistemic_regime: EpistemicRegime;
  verification_horizon: VerificationHorizonId;
  ac_state: 0 | 1 | 2 | 3 | 4 | 5;
  consequence_map?: ConsequenceMap;
  counterparty_refs?: string[];
};

// G3 — Epistemic Regime
type EpistemicRegime =
  | "A_PHYSICAL"
  | "B_SOCIO_TECHNICAL"
  | "C_NORMATIVE_CONSTITUTIONAL";

// G2 — Counterparty Witness
type CounterpartyWitness = {
  counterparty_id: string;
  standing_basis: "affected" | "owner" | "operator" | "delegate" | "public_interest";
  consent_scope?: string[];
  contestability_channel: string;
  notification_status: "not_required" | "pending" | "notified" | "acknowledged";
  challenge_state: "none" | "open" | "reviewing" | "resolved";
  remedy_path?: string;
  evidence_refs: string[];
};

// G6 — Verification Horizon
type VerificationHorizonId = "H0" | "H1" | "H2" | "H3";
type VerificationHorizon = {
  horizon_id: VerificationHorizonId;
  window: string;
  expected_signal_strength: number;
  maturity_threshold: number;
  permitted_authority_state: "AC-0" | "AC-1" | "AC-2" | "AC-3";
};

// G5 — Pain-Routing ConsequenceMap
type ConsequenceMap = {
  decision_author: string;
  beneficiaries: string[];
  downside_bearers: string[];
  repair_authority: string[];
  reversal_cost_bearers: string[];
  externality_risk: "low" | "medium" | "high";
  mismatch_score: number;
};

// G10 — Probe-Before-Intent envelope flag
type ArifInitEnvelope = {
  actor_id: string;
  intent: string;
  probe_before_intent: boolean;          // default: true; fail-closed
  first_probe_at?: string;               // ISO-8601, must exist if probe_before_intent=true AND intent non-empty
  epistemic_regime?: EpistemicRegime;
  verification_horizon?: VerificationHorizonId;
};

// Evidence Ref (F11 backbone)
type EvidenceRef = {
  evidence_id: string;
  source: string;
  epistemic_label: "OBS" | "DER" | "INT" | "SPEC" | "SYN" | "RECYCLED_SYN";
  captured_at: string;
  provenance: Record<string, unknown>;
};
```

---

## 7. Concrete File Plan (Phase 1 deliverables)

| Path | Purpose |
|---|---|
| `/root/A-FORGE/aforge/core/authority_contract.py` | G1 implementation (observe-only in Phase 1) |
| `/root/A-FORGE/aforge/core/pain_route_detect.py` | G5 implementation |
| `/root/A-FORGE/aforge/core/lag_audit.py` | G6 implementation |
| `/root/arifOS/arifosmcp/tools/well_counterparty.py` | G2 WELL extension |
| `/root/AAA/skills/reality-bound-authority-auditor/` | G14 skill manifest |
| `/root/arifOS/state/epistemic_regime.json` | G3 default + override registry |
| `/root/arifOS/arifosmcp/core/arif_init.py` | G10 + G3 stamping |
| `/root/arifFlow/health/multikpi.py` | G8 implementation |
| `/root/AAA/reports/anti-shadow-audit-{date}.md` | T15 recurring |

---

## 8. Rollout Order (lowest blast radius first)

| Order | ID | Why first |
|---|---|---|
| 1 | **G10** — probe-before-intent | T1 code, single boolean flag, fail-closed, no behavioral change beyond catching extractive flows |
| 2 | **G3** — epistemic regime stamping | T2 spec only; metadata only, no enforcement |
| 3 | **G2** — counterparty registry schema | T2 spec only; standing organ defined before AC-2 enforcement needs it |
| 4 | **G5** — pain-routing detector | depends on G2 registry for `downside_bearers` |
| 5 | **G6** — lag-aware receipt lifecycle | T2; tests receipt maturation; feeds future G9 |
| 6 | **G8** — multi-KPI floor | extends arifFlow; needs no other primitive |
| 7 | **G14** — auditor skill | consumes G3/G5/G6/G8 outputs |
| 8 | **G1** — authority contraction primitive | gated on T15 evidence + G recovery |
| 9 | **G7** — independent falsifier channel | architectural decision; cost-bearing |
| 10 | **G4 / G9** — dA/dt ≤ dV/dt + outcome reward | require measurement from G6 + G8 first |

---

## 9. Honest Gates and Shadows

**Shadow 1 — G=0.31 blocks T3.** F8 floor. Constitutional work cannot ratify at current G. Recovery needs arifFlow FQ lift (0.5 → 0.7+) + GROK unfossilize + shadow-mode evidence.

**Shadow 2 — Lane A SABAR 26 days.** Carry-forward item. T22 must precede T23/T24.

**Shadow 3 — Quad witness 1.5/4 ready.** Earth partial (WELL degraded, FLAME DOWN). AI falsifier needs T20. Counterparty needs T13.

**Shadow 4 — Hidden dependency: T13 → T11.** Pain-routing needs counterparty registry first.

**Shadow 5 — Hidden cost: T20.** Independent model surface for falsifier. Federation budget reality vs NIST/OECD recommendation.

**Shadow 6 — Measurement is circular.** dA/dt, dV/dt, dC/dt need the very primitives being built. Phase 1 shadow mode is the data-collection phase.

**Shadow 7 — arifOS already has "pain alone" partially answered.** Q10 Calhoun Lock detects verify-execute imbalance. R-BAP sharpens it to detect party-routing.

---

## 10. T1 Forge Receipt

**This session:** T01–T07 executed as file writes. No autonomous permissions granted. No FLOOR_TABLE.json committed. No production registry touched. Reversible in full.

**Net ΔS:** negative (24-task plan compressed, 6-shadow analysis, 10-primitive gap matrix, 3-phase rollout).

**Evidence:**
- `reality-bound-authority.md` (master canon)
- `anti-shadow-architecture.md` (operational instruction)
- `GENESIS/060_ANTI_SHADOW_ARCHITECTURE.md` (DRAFT)
- `RBA-IMPLEMENTATION-SPEC.md` (this file)
- `nist-rmf-oecd-mapping.md` (cross-walk)
- `anti-shadow-audit-2026-09-07.md` (first audit)

---

DITEMPA BUKAN DIBERI — 999 SEAL ALIVE
