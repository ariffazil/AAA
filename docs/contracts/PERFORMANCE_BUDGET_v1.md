# Performance Budget Specification v1 — G6 (Wawa D2)

> **EUREKA P1, G6** — Define latency budgets per step of the 12-step
> governance flow, deferral rules for low-blast actions, and escalation
> when budgets are exceeded.
>
> **Status:** RATIFIED — operational contract
> **Date:** 2026-07-13
> **Author:** Hermes-Prime (on Arif F13 directive, Wawa gap analysis)
> **Floors:** F1 AMANAH, F4 CLARITY, F8 GENIUS

---

## 1. The 12-Step Governance Flow

The canonical arifOS metabolic loop traverses 12 steps from session initiation
through seal. Each step has a latency budget.

```
STEP  1: Identity Binding      (arif_init)
STEP  2: Intent Classification (arif_think → classify)
STEP  3: Capability Issuance   (arif_judge → capability check)
STEP  4: Evidence Gathering    (arif_observe)
STEP  5: Reasoning             (arif_think → reason)
STEP  6: Simulation            (arif_think → simulate / preActionSimulation)
STEP  7: Governance Verdict    (arif_judge → SEAL/HOLD/SABAR/VOID)
STEP  8: Execution Planning    (arif_think → plan)
STEP  9: Execution             (arif_forge / forge_* tool)
STEP 10: Verification          (forge_runtime_verify / post-check)
STEP 11: Continuity Recording  (seal_chain.js write / arif_seal)
STEP 12: Cooling               (forge_cool_drift / forge_cool_pattern)
```

For reversible, low-blast-radius actions, steps 4–6 MAY be deferred (see §4).

---

## 2. Latency Budgets

### 2.1 Normal Mode (all organs healthy)

| Step | Name | Target (p50) | P99 | Budget Exceeded Action |
|------|------|-------------|-----|----------------------|
| 1 | Identity Binding | < 10ms | < 50ms | Log as telemetry. Escalate if persistent > 3 consecutive calls. |
| 2 | Intent Classification | < 30ms | < 100ms | Log as telemetry. Flag in AAA cockpit if > 100ms p50 over 10 calls. |
| 3 | Capability Issuance | < 20ms | < 100ms | Log as telemetry. Escalate if persistent > 5 consecutive calls. |
| 4 | Evidence Gathering | < 200ms | < 1000ms | MAY defer for blast_radius=LOW actions. Log when exceeded. |
| 5 | Reasoning | < 500ms | < 3000ms | MAY defer for blast_radius=LOW actions. Log when exceeded. |
| 6 | Simulation | < 1000ms | < 5000ms | MAY defer for blast_radius=LOW actions. SKIP if simulation not available. |
| 7 | Governance Verdict | < 100ms | < 500ms | Log as telemetry. Escalate if persistent > 3 consecutive calls. |
| 8 | Execution Planning | < 200ms | < 1000ms | Log as telemetry. Alert in AAA cockpit if > 2000ms. |
| 9 | Execution | N/A (action-dependent) | N/A | Per-tool budget defined by tool contract. |
| 10 | Verification | < 500ms | < 2000ms | Log as telemetry. Escalate if persistent > 5 consecutive calls. |
| 11 | Continuity Recording | < 100ms | < 500ms | Log as telemetry. Block execution if seal_chain.js write fails. |
| 12 | Cooling | < 200ms | < 1000ms | Log as telemetry. Defer if system under load. |

**Total loop budget (steps 1–12, excluding step 9):** Target < 2800ms, P99 < 10s.

### 2.2 Degraded Mode (one or more organs degraded)

When any organ reports degraded health, budgets are **doubled** for steps
that involve the degraded organ. Steps that route through the degraded organ
are subject to the timeout defined in the Degradation Mode Spec (§2).

| Step | Degraded Organ | Adjusted Target | Adjusted P99 |
|------|---------------|-----------------|-------------|
| 1–3 | arifOS (governance) | Target × 2 | P99 × 2 |
| 4 | GEOX (if evidence from geoscience) | Target × 2 | P99 × 2 |
| 7 | arifOS (governance) | Target × 2 | P99 × 2 |
| 9 | A-FORGE (execution) | Target × 2 | P99 × 2 |
| 11 | arifOS/VAULT999 (truth) | Target × 2 | P99 × 2 |

---

## 3. Deferral Rules for Low-Blast Actions (Steps 4–6)

### 3.1 Eligibility

Actions are eligible for deferral when ALL of:
1. `blast_radius` parameter is `LOW`
2. Action is `reversible` (not IRREVERSIBLE or EXECUTE_HIGH_IMPACT)
3. Action does NOT require `888_HOLD` or `F13_SOVEREIGN` authority
4. The agent has an active session with verified actor_id

### 3.2 What Gets Deferred

| Step | Deferral Behaviour |
|------|-------------------|
| 4 (Evidence Gathering) | Skip synchronous evidence fetch. Classify into telemetry bucket. |
| 5 (Reasoning) | Use cached/last-known reasoning context if available. Recompute deferred to after execution. |
| 6 (Simulation) | SKIP entirely. PreActionSimulation returns `{deferred: true}`. |

### 3.3 Deferral Recording

When steps 4–6 are deferred, the action payload carries:
```json
{
  "deferred": {
    "steps": ["evidence_gathering", "reasoning", "simulation"],
    "reason": "blast_radius=LOW, action reversible",
    "expected_replay": "post_execution"
  }
}
```

### 3.4 Replay After Execution

Deferred steps MUST be replayed after execution completes (step 9). The replay
is attached as evidence in the verification step (step 10):
```json
{
  "post_execution_analysis": {
    "evidence_gathered": true,
    "reasoning_completed": true,
    "simulation_result": "..."
  }
}
```

If replay reveals that the execution would have been blocked by simulation or
evidence, a COOLING_RECEIPT is emitted with `severity: "SIGNIFICANT"`.

---

## 4. What Happens When Budget Is Exceeded

### 4.1 Telemetry Logging

Every budget exceedance is logged:
```json
{
  "event_type": "performance.budget_exceeded",
  "step": "reasoning",
  "target_ms": 500,
  "actual_ms": 1234,
  "exceedance_pct": 147,
  "actor_id": "hermes-prime",
  "action": "deploy_cooling_verbs",
  "consecutive_count": 1,
  "timestamp": "2026-07-13T01:00:00Z"
}
```

### 4.2 Escalation

| Condition | Action |
|-----------|--------|
| Single exceedance | Log to telemetry. No user-facing action. |
| 3 consecutive exceedances (same step) | Log + COOLING receipt with `severity: MINOR`. |
| 5 consecutive exceedances (same step) | Log + COOLING receipt with `severity: SIGNIFICANT`. Escalate to AAA cockpit alert. |
| 10 consecutive exceedances (same step) | Log + COOLING receipt with `severity: CRITICAL`. HOLD all actions of this type until governance reviews. |
| Any step > 5× target | Immediate COOLING receipt. Escalation to `888_HOLD` regardless of pattern count. |

### 4.3 System Overload Detection

If ≥ 3 of the last 10 action loops have any budget exceedance, the system is
in "elevated latency" mode. In this mode:
- All blast_radius=LOW actions automatically defer steps 4–6
- Step 12 (cooling) is skipped for non-critical observations
- A NOTICE_BOARD entry is created: `"federation-latency-warning"`

---

## 5. Per-Tool Budgets (Step 9 — Execution)

Execution step budgets vary by tool. The canonical budgets are:

| Tool | Target | P99 | Notes |
|------|--------|-----|-------|
| forge_filesystem_read | < 50ms | < 200ms | File I/O bounded |
| forge_filesystem_write | < 100ms | < 500ms | Write + backup |
| forge_shell | < 200ms | < 2000ms | Arbitrary command |
| forge_shell_dryrun | < 100ms | < 500ms | Preview only |
| forge_git_commit | < 500ms | < 2000ms | Index + commit |
| forge_git_push | < 2000ms | < 10000ms | Network bounded |
| forge_docker_run | < 2000ms | < 10000ms | Container lifecyle |
| forge_cool_drift | < 500ms | < 2000ms | seal_chain write + encode |
| forge_cool_pattern | < 500ms | < 2000ms | seal_chain write + encode |
| forge_runtime_verify | < 200ms | < 1000ms | Git + pip + import read |

---

## 6. Monitoring

### 6.1 Metrics Collection

Each step emits Prometheus metrics:
```
arifos_step_duration_ms{step="identity_binding"} 8
arifos_step_duration_ms{step="governance_verdict"} 42
arifos_step_duration_ms{step="execution_planning"} 156
arifos_loop_duration_ms{loop_type="full"} 2842
arifos_loop_duration_ms{loop_type="deferred"} 1150
arifos_budget_exceedances_total{step="reasoning"} 3
```

### 6.2 Budget Health Check

```json
{
  "performance_budget_status": "HEALTHY",
  "total_loops": 152,
  "exceedances": 3,
  "exceedance_rate_pct": 1.97,
  "slowest_step": "evidence_gathering",
  "slowest_ms": 845,
  "elevated_latency_mode": false,
  "deferred_actions_count": 12
}
```

---

## 7. Conformance

All federation organs (A-FORGE, arifOS, AAA, GEOX, WEALTH, WELL) must:
1. Record step-level latency for every action loop
2. Emit `performance.budget_exceeded` events when budgets are breached
3. Support deferred steps 4–6 for blast_radius=LOW actions
4. Respect escalation rules when consecutive exceedances occur

Non-conformance is flagged as a `violated_floors: ["F8"]` (GENIUS — system health)
in the seal chain.

*DITEMPA BUKAN DIBERI — Performance is measured, not guessed.*
