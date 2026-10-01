# WELL Homeostatic Runtime Governor Contract v1 (P2.d — Stage 2 spec)

> **Status:** STAGED-ARTIFACT, FOR STAGE 2 arifOS-L13 BUILD. F13 directive "ok i approve, sah, jalan and go" received 2026-10-01.
> **Lineage:** WELL constitutional role (organ_health vs human_truth); META-WISDOM Canon #4 MG-3 (machine ZEN — Value Of Continuation); Constitutional Architecture Canon HALAL-positive predicate; Trilogy Gap §3.1 (well status=degraded; h_well_honesty=INSUFFICIENT); live `well_observe_federation_thermal` (route=RECOVER, arifos=0.7, geox=0.7, others=0.95).
> **Purpose:** Machine-side telemetry wired into the WELL intensity governor's decision logic. Closes the gap between doctrine (route=RECOVER works) and data (h_well_honesty=INSUFFICIENT).
> **Why this matters:** WELL currently runs on partial inputs. The intensity governor returns RECOVER when in fact, human-side readiness is also honest — but only M-side metrics are wired.

---

## The intensity governor

```yaml
governor_state:
  lookback_hours: <int>
  m_side:
    cpu_pressure: <float>  # 0.0-1.0, PSI some/some 10s
    memory_pressure: <float>
    io_pressure: <float>
    swap_used_ratio: <float>
    network_latency_p95_ms: <float>
    tool_call_failure_rate: <float>
    receipt_chain_gap_rate: <float>
  h_side:
    h_well_signal: <str>  # OPTIMAL | WATCH | DEGRADED | CRITICAL | INSUFFICIENT_DATA
    h_well_honesty: <str>  # HONEST | INSUFFICIENT | GARBLED
    human_state_agent: <str>  # OPTIMAL | WATCH | DEGRADED | CRITICAL | INSUFFICIENT_DATA
  organ_health:
    weakest_organ: <organ_id>
    organ_score: <float>
    critical_count: <int>
  intensity_decision:
    level: explore | compress | essential_only | stop_preserve_state
    reasons: <str[]>
    decided_at: <iso8601>
    decided_by: <actor_id>
```

---

## Decision logic (the four-band ladder)

```python
def intensity_level(m, h, organ):
    if organ.health_score < 0.5:
        return STOP_AND_PRESERVE_STATE, "weakest organ below 0.5"

    if m.cpu_pressure > 0.7 or m.memory_pressure > 0.7 or m.io_pressure > 0.7:
        return ESSENTIAL_ONLY, f"machine pressure above 0.7 (cpu={m.cpu_pressure}, mem={m.memory_pressure}, io={m.io_pressure})"

    if m.swap_used_ratio > 0.3 or m.receipt_chain_gap_rate > 0.05:
        return COMPRESS, f"machine substrate degraded (swap={m.swap_used_ratio}, gaps={m.receipt_chain_gap_rate})"

    if h.h_well_honesty == "INSUFFICIENT" or h.human_state_agent == "DEGRADED":
        return COMPRESS, f"human substrate honest state degraded"

    return EXPLORE, "machine and human substrate within bounds"
```

The ladder is **stop_preserve_state > essential_only > compress > explore**, with regression tests named per the META-WISDOM Canon #4 MG-3 ladder.

---

## What gets adjusted

```
EXPLORE → full surface, full concurrency, full depth, full compute
COMPRESS → reduce concurrency 50%, reduce context, drop non-critical probes
ESSENTIAL_ONLY → reduce concurrency 80%, drop exploration, keep critical path
STOP_AND_PRESERVE_STATE → freeze non-essential mutation, snapshot state, await decision
```

---

## Telemetry wiring (the Stage 2 build)

The current `well_observe_federation_thermal` returns organ scores but not raw CPU/memory/IO PSI. The Stage 2 build must wire:

- `well_machine_diagnose` outputs → `m_side` fields
- `well_assess_homeostasis` outputs → `h_side` fields
- The `intensity_decision` flows to arifFlow and AAA's auto-execution-queue

---

## Stage 0 dependency

Same as P0 and P1.c: Stage 0 (drift-reconcile-unblock-test-2026-10-02) must clear before any kernel wiring.

---

## What this artifact is NOT

- Not the kernel implementation; only the callable signature and decision logic.
- Not the Wisdom/Bangang instrumentation (Trilogy Gap §4 HIGH gap remains HIGH).
- Not a CHANGE to human-substrate scoring; only modifies how the existing scores drive intensity.

---

## Receipt chain

- `forge_experience_trace trace_id=exp-1790838115433-1790836981647` (audit trace)
- This contract artifact: `/root/AAA/.forge_outbox/well_homeostatic_governor_contract_v1.md`
- Live probe evidence: `well_observe_federation_thermal` route=RECOVER, h_well_honesty=INSUFFICIENT

DITEMPA BUKAN DIBERI ⚒️