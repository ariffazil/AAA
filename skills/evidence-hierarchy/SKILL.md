---
name: evidence-hierarchy
version: 1.0.0
description: "Use when evidence contradicts. MEASURED outranks DERIVED."
tags: [governance, evidence, F2, F11]
layer: substrate
floor_scope: [F2, F11]
owner: F13 SOVEREIGN
status: active
---

# evidence-hierarchy

> MEASURED > DERIVED > REASON_CODE > NARRATIVE_LABEL

When a control checks multiple evidence sources in the same payload and they contradict, this hierarchy resolves the conflict.

## Tiers

| Tier | What It Is | Example | Weight |
|---|---|---|---|
| **MEASURED** | Explicit boolean/fact from runtime attestation | `software_release.drift = false` | Highest |
| **DERIVED** | Computed state label from other signals | `substrate.state = "DEGRADED"` | Medium |
| **REASON_CODE** | Label applied by a control | `reason_code = "DEPLOYMENT_DRIFT"` | Low |
| **NARRATIVE** | Human-readable description | "The system is degraded" | Lowest |

## Rules

1. **MEASURED outranks DERIVED.** A measured `drift=false` clears a derived `state=DEGRADED` from the drift decision.
2. **MEASURED still fires when true.** A measured `drift=true` fires the floor regardless of derived labels.
3. **No measurement = fail closed.** When no measurement exists, the derived label is honoured.
4. **Never default a reason code.** If the cause was not measured, use an honest sentinel (`REASON_UNMEASURED`), never a specific-sounding label.
5. **Audit the block.** When a control fires, stamp WHICH location and WHICH field produced it.

## Origin

Discovered during the kernel dual-truth fix: `_payload_has_deployment_drift()` fired on `substrate.state == "DEGRADED"` (a DERIVED label) even when `software_release.drift = false` (a MEASURED fact) sat in the same payload. The reason_code was then defaulted to `"DEPLOYMENT_DRIFT"` — a label nothing had measured.

## Application

Apply this hierarchy whenever:
- A control checks multiple evidence sources in the same payload
- A derived state label could override a measured fact
- A reason code needs to name an actual cause, not a default

## A/B Causal Testing

When verifying a code change that implements this hierarchy:

1. Build same payloads with OLD and NEW code
2. Feed identical inputs through both
3. Diff the machine-visible outputs (seal_allowed, reason_code, effective_verdict, _drift_floor_applied)
4. Negative test: construct payload where measured fact says drift=true — confirm floor still fires
5. Report which cases changed and which stayed the same

This is stronger than running the full test suite because it isolates the causal effect of the code change from pre-existing failures.