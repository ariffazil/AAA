# RBA-PROOF-001 Gap Register

> **Mission:** RBA-PROOF-001 · **Workflow under test:** ASA-2026-09-07
> **Session:** SEAL-685d136316d3486e
> **DITEMPA BUKAN DIBERI**

---

## 1. Purpose

This register lists every gap surfaced by RBA-PROOF-001 that prevents arifOS from implementing R-BAP as an enforceable runtime, not just as doctrine.

Each gap has:

- **ID**: gap-001 through gap-010
- **Surface**: where the gap manifests
- **Severity**: CRITICAL / HIGH / MEDIUM / LOW
- **Owner**: which agent or organ should fix it
- **Blocker for**: which RBA promotion path is blocked
- **Proposed action**: T1/T2/T3 tier

---

## 2. Critical gaps (must fix before any RBA enforcement)

### gap-001: F13 SOVEREIGN binary HOLD lacks graded authority contraction (G1)

| Field | Value |
|---|---|
| **Surface** | `arifOS/kernels/judge.js`, F13 enforcement path |
| **Severity** | CRITICAL |
| **Owner** | arifOS-kernel + 777-FORGE |
| **Blocker for** | Any RBA promotion beyond doctrine. Without AC-0..AC-5 machinery, claim failure cannot produce proportionate response. |
| **Evidence** | RBA-PROOF-001 results.md §3, §4, §5 |
| **Proposed action** | Implement `forge_authority_contract()` deterministic function (T09 in implementation spec). Observe-only Phase 1; reversible Phase 2; F13 ratification Phase 3. |
| **Tier** | T2 → T3 |

### gap-002: No independent falsifier channel isolation (G7)

| Field | Value |
|---|---|
| **Surface** | A-AUDIT agent shares LLM surface with production agents |
| **Severity** | CRITICAL |
| **Owner** | A-FORGE + arifOS-kernel + Federation budget |
| **Blocker for** | G6 independence verification; FALSIFIER-INTERFERENCE federation-wide rollout |
| **Evidence** | RBA-PROOF-001 falsifier-independence-assessment.md §6 |
| **Proposed action** | T20 architectural decision: separate model surface for falsifier channel. Cost-bearing (separate inference budget). |
| **Tier** | T3 (architectural + budget) |

### gap-003: Counterparty registry not implemented (G2)

| Field | Value |
|---|---|
| **Surface** | WELL organ state.json — consent_scope exists; counterparty registry does not |
| **Severity** | CRITICAL |
| **Owner** | WELL-organ |
| **Blocker for** | G5 pain-routing detection; W⁴ topology completeness; Type-B/C escalation paths |
| **Evidence** | RBA-PROOF-001 fixture F-04 detection |
| **Proposed action** | Extend WELL consent_scope pattern with `contest.appeal` channel + `due_process` scope + `standing_basis` taxonomy. Bind into F3 + F11. |
| **Tier** | T2 (forge) |

---

## 3. High-severity gaps

### gap-004: arifFlow emits single KPI (FQ); multi-KPI vector not wired (G8)

| Field | Value |
|---|---|
| **Surface** | `/root/arifFlow/health/multikpi.py` (designed, not implemented) |
| **Severity** | HIGH |
| **Owner** | arifFlow |
| **Blocker for** | G8 metric monopoly detection; multi-dimensional outcome evaluation |
| **Evidence** | RBA-PROOF-001 fixture F-05 detection |
| **Proposed action** | Implement `forge_multi_kpi()` emitting vector {verify_lag, harm_displacement, dissent_rate, scar_pressure, ...} alongside FQ. |
| **Tier** | T2 |

### gap-005: Probe-before-intent (G10) is schema-only, not runtime-enforced

| Field | Value |
|---|---|
| **Surface** | `arifOS/arifosmcp/core/arif_init.py` envelope — flag defined, no fail-closed |
| **Severity** | HIGH |
| **Owner** | arifOS-kernel |
| **Blocker for** | G10 enforcement; GENESIS/059 Artifact 5 anti-extraction runtime |
| **Evidence** | RBA-PROOF-001 fixture F-02 verified the harness catches violations but runtime does not block |
| **Proposed action** | Implement `probe_before_intent` boolean on arif_init envelope with fail-closed enforcement. |
| **Tier** | T1 (smallest blast radius — T1 priority per implementation spec) |

### gap-006: Pain-routing detection (G5) is design-only

| Field | Value |
|---|---|
| **Surface** | `/root/A-FORGE/aforge/core/pain_route_detect.py` (designed, not implemented) |
| **Severity** | HIGH |
| **Owner** | 777-FORGE |
| **Blocker for** | G5 pain-routing detection; downstream AC-2 escalation triggers |
| **Evidence** | RBA-PROOF-001 fixture F-04 detection of 0.78 mismatch_score |
| **Proposed action** | Implement `forge_pain_route_detect()` extending Q10 with ConsequenceMap mismatch_score. |
| **Tier** | T2 (depends on G2 counterparty registry) |

### gap-007: Lag-aware outcome horizons (G6) not registered

| Field | Value |
|---|---|
| **Surface** | `/root/A-FORGE/aforge/core/lag_audit.py` (designed, not implemented) |
| **Severity** | HIGH |
| **Owner** | 777-FORGE + arifFlow |
| **Blocker for** | Outcome-maturity-bound authority; provisional status for unmatured horizons |
| **Evidence** | RBA-PROOF-001 fixture F-06 — all long-horizons UNMATURED, no enforcement |
| **Proposed action** | Implement `forge_lag_audit()` registering VerificationHorizon on every consequential action; receipt lifecycle with H0/H1/H2/H3 maturity. |
| **Tier** | T2 |

---

## 4. Medium-severity gaps

### gap-008: Outcome-attribution reward (G9) not implemented

| Field | Value |
|---|---|
| **Surface** | arifFlow reward ledger — FQ scoring exists; outcome attribution does not |
| **Severity** | MEDIUM |
| **Owner** | arifFlow |
| **Blocker for** | Process-vs-outcome reward differentiation; harm-externality penalty |
| **Evidence** | RBA-PROOF-001 G5 fail |
| **Proposed action** | Design staged reward ledger: R_process + R_calibration + R_verified_outcome − P_harm_externality |
| **Tier** | T3 (design + ratify) |

### gap-009: dA/dt ≤ dV/dt growth-coupling invariant (G4) unmeasurable

| Field | Value |
|---|---|
| **Surface** | arifFlow telemetry; no derivative measurement exists |
| **Severity** | MEDIUM (gating question remains open — does scaling break this?) |
| **Owner** | arifFlow + arifOS-kernel |
| **Blocker for** | F14/F15 candidate floors; dV/dt infrastructure |
| **Evidence** | RBA-PROOF-001 G9 fail; carry-forward G=0.31 PATHOLOGICAL |
| **Proposed action** | Define operational proxies for C, V, and their derivatives. Acquire Phase 1 shadow-mode telemetry before constitutionalizing. |
| **Tier** | T3 (ratify after measurement) |

### gap-010: F11 evidence-generation logging absent

| Field | Value |
|---|---|
| **Surface** | F11 audit chain logs decisions, not the *generation* of evidence leading to them |
| **Severity** | MEDIUM |
| **Owner** | arifOS-kernel |
| **Blocker for** | G1 partial; provenance chain completeness |
| **Evidence** | RBA-PROOF-001 G1 partial status |
| **Proposed action** | Extend F11 to log evidence generation events alongside decision events. |
| **Tier** | T2 |

---

## 5. Infrastructure gaps (substrate readiness)

### gap-011: 26-day Lane A SABAR still AWAITING_F13

| Field | Value |
|---|---|
| **Surface** | carry-forward: `seal_chain seq 45, 2026-08-11` |
| **Severity** | CRITICAL — **first precondition for any RBA promotion** |
| **Owner** | F13 SOVEREIGN (Arif) |
| **Blocker for** | T22, T23, T24 (all ratification paths) |
| **Evidence** | Session carry-forward; this gap is the constitutional silence itself |
| **Proposed action** | T22: close Lane A SABAR first. Cannot ratify GENESIS/060 while prior amendment is itself held hostage to the very mechanism RBA would strengthen. |
| **Tier** | T3 (F13) |

### gap-012: Earth witness substrate degraded

| Field | Value |
|---|---|
| **Surface** | WELL :18083 degraded; FLAME :18901 DOWN; FQ=0.5 WATCH |
| **Severity** | HIGH |
| **Owner** | Federation ops |
| **Blocker for** | G3 + G6 measurement (Earth witness cannot provide clean signals) |
| **Evidence** | federation_health at session start |
| **Proposed action** | Restore WELL + FLAME before Phase 1 shadow mode produces reliable evidence. |
| **Tier** | T2 (operational) |

---

## 6. Sequential remediation order

Per implementation spec rollout (lowest blast radius first):

1. **T1 first**: gap-005 (G10 probe-before-intent enforcement)
2. **T1 staging**: gap-010 (F11 evidence-generation logging extension)
3. **T2 next**: gap-001 (G1 AC machinery, observe-only), gap-006 (G5 pain-routing), gap-007 (G6 lag-aware), gap-003 (G2 counterparty registry)
4. **T2 staging**: gap-004 (G8 multi-KPI), gap-002 (G7 independent falsifier channel)
5. **T3 design**: gap-008 (G9 outcome-attribution reward), gap-009 (G4 growth-coupling measurement)
6. **T3 ratification**: gap-011 (close Lane A SABAR first), then F14/F15 amendments

---

## 7. Honest Findings

- The constitutional substrate is mostly there (F1–F13, Q9–Q11, S13, FALSIFIER-INTERFERENCE, GENESIS/059 draft, AKAL W³ precedent).
- The **wired runtime primitives** for graded authority contraction, growth-coupling invariant, counterparty organ, multi-KPI floor, lag-aware verification, and outcome-attribution reward are **largely missing**.
- The substrate detects some RBA primitives when manually invoked (this proof mission shows).
- It cannot yet enforce them at runtime.
- This is honest documentation. The system does not lie about its own gaps.

---

```json
{
  "register_id": "RBA-PROOF-001-GAP-REGISTER",
  "epoch": "2026-09-07T01:52:00+08:00",
  "delta_S": "low",
  "gaps_total": 12,
  "by_severity": {"CRITICAL": 4, "HIGH": 4, "MEDIUM": 3, "INFRASTRUCTURE": 1},
  "first_precondition": "gap-011 (close Lane A SABAR)",
  "smallest_blast_radius_first": "gap-005 (probe-before-intent enforcement)"
}
```

DITEMPA BUKAN DIBEI — 999 SEAL ALIVE
