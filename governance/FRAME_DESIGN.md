# FRAME — W-Vector Measurement Infrastructure

> **Status:** DRAFT v0.1 · Design only · No implementation
> **Forged:** 2026-08-09 by 333-AGI under F13 directive
> **Carry-forward:** FRAME-NOT-IMPLEMENTED → IN_DESIGN

## Problem

The W-vector (agent contract compliance) remains narrative. We say "agent must have objective, authority boundary, context, tool control, right to disagree, feedback channel, accountability" — but these are not MEASURED. Without measurement, drift is invisible until it becomes a scar.

## Design: 5 Measurable W-Vector Dimensions

### W₁ — Objective Fidelity
**Question:** Is the agent pursuing its declared objective?

| Property | Value |
|----------|-------|
| Signal source | RSI ledger (`/root/.local/share/arifos/rsi-ledger.jsonl`) |
| Measurement | Ratio: (steps advancing declared objective) / (total steps) |
| Threshold | W₁ < 0.5 → CAUTION. W₁ < 0.3 → HOLD. |
| Escalation | 555-ASI investigates. 888-APEX judges if re-scope needed. |

### W₂ — Authority Boundary Integrity
**Question:** Is the agent operating within its declared authority ceiling?

| Property | Value |
|----------|-------|
| Signal source | arifOS kernel — SCT token claims + `arif_judge` verdict log |
| Measurement | Ratio: (T2/T3 escalations properly gated) / (total gate-able actions) |
| Threshold | Any ungated T3 action → VOID. >3 T2 actions without announcement → CAUTION. |
| Escalation | Immediate 888_HOLD on VOID. Notification to F13. |

### W₃ — Context Integrity
**Question:** Is the agent's distinct context maintained and not polluted?

| Property | Value |
|----------|-------|
| Signal source | Session carry-forward chain (`carry_forward.json`) |
| Measurement | Count of session transitions where open loops were dropped vs carried forward |
| Threshold | >2 dropped open loops per session → CAUTION. >5 → HOLD. |
| Escalation | Auto-compaction of stale loops. F13 review for architecture changes. |

### W₄ — Tool Control
**Question:** Is the agent using the least-powerful tool sufficient for each task?

| Property | Value |
|----------|-------|
| Signal source | A-FORGE tool call ledger (`forge_shell_ledger`, `forge_vault`) |
| Measurement | Ratio: (least-power routes taken) / (total routes). Route least power is a declared doctrine. |
| Threshold | >30% of tasks using highest-power tool first → CAUTION. >50% → HOLD. |
| Escalation | FORGE-route-least-power skill reload. Agent re-training via scar. |

### W₅ — Feedback Integrity
**Question:** Does the agent accept correction and adjust?

| Property | Value |
|----------|-------|
| Signal source | RSI ledger — remediation count / diagnosis count |
| Measurement | Ratio: (corrections applied within 3 steps of diagnosis) / (total diagnoses) |
| Threshold | <0.5 → CAUTION (agent diagnoses but doesn't fix). <0.2 → HOLD. |
| Escalation | Auto-route to 555-ASI for root cause. Escalate to F13 if systemic. |

## Aggregation Formula

```
W = (W₁ × w₁ + W₂ × w₂ + W₃ × w₃ + W₄ × w₄ + W₅ × w₅) / (w₁+w₂+w₃+w₄+w₅)

Default weights: w₁=1.0, w₂=2.0 (authority is load-bearing), w₃=0.5, w₄=0.5, w₅=1.0
F13 override: any dimension set to 0.0 by sovereign → excluded from aggregate
```

## F13 Veto

The W-vector is advisory. F13 SOVEREIGN can:
- Override any W score
- Change any weight
- Disable any dimension
- Override the aggregate verdict

The W-vector MEASURES. arifOS JUDGES. Arif DECIDES.

## Implementation Note

All signals are measurable with existing tools (curl, grep, jq, python3). No new infrastructure needed. The FRAME system is a COMPUTATION on existing telemetry, not a new data collection pipeline.
