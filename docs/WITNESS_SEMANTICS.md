# Witness Semantics — arifOS Thermodynamic Witness Model

> **Status:** CLARIFICATION — correcting category error in prior assessment
> **Forged:** 2026-07-12 by AAA Control Plane
> **Floor:** F2 TRUTH (≥ 0.99 fidelity)
> **Doctrine:** DITEMPA BUKAN DIBERI

---

## The Error

Prior assessment compared H=0.42, A=0.32, E=0.26 individually against the 0.75 consensus threshold, concluding "witness diversity below threshold."

This was a **category error**. The three values sum to exactly 1.00. They are **contribution weights** (relative influence), not individual confidence scores.

Comparing weights against a confidence threshold is mathematically meaningless — like saying "42% of the vote is below the 75% approval threshold."

---

## What the Values Mean

```
witness:
  human:  0.42    ← 42% of consensus weight assigned to human channel
  ai:     0.32    ← 32% of consensus weight assigned to AI channel
  earth:  0.26    ← 26% of consensus weight assigned to earth/evidence channel
  sum:    1.00    ← weights are normalized
```

These are **NOT**:
- Individual confidence scores
- Evidence quality metrics
- Agreement percentages
- Reliability ratings

These **ARE**:
- Relative influence weights for consensus computation
- How much each channel's evidence contributes to the final verdict

---

## The Correct Consensus Model

A proper tri-witness consensus needs BOTH weights AND confidence per channel:

```json
{
  "witness_consensus": {
    "human": {
      "weight": 0.42,
      "confidence": 0.68,
      "freshness": "CURRENT",
      "evidence": "self-report from session 2026-07-12T04:30Z"
    },
    "ai": {
      "weight": 0.32,
      "confidence": 0.81,
      "freshness": "CURRENT",
      "evidence": "conformance spine 9/9 pass, tool registry verified"
    },
    "earth": {
      "weight": 0.26,
      "confidence": 0.74,
      "freshness": "PARTIAL",
      "evidence": "machine telemetry green, human biometric stale"
    },
    "weighted_consensus": 0.73,
    "required_threshold": 0.75,
    "verdict": "HOLD",
    "hold_reason": "weighted_consensus (0.73) below required threshold (0.75)"
  }
}
```

### How weighted_consensus is computed

```
weighted_consensus = (H_weight × H_confidence) + (A_weight × A_confidence) + (E_weight × E_confidence)

Example:
= (0.42 × 0.68) + (0.32 × 0.81) + (0.26 × 0.74)
= 0.2856 + 0.2592 + 0.1924
= 0.7372
≈ 0.74
```

### When to HOLD

```
if weighted_consensus < required_threshold:
    verdict = HOLD
    # Missing evidence reduces confidence, which reduces consensus
    # This is the correct behavior — uncertainty produces caution
```

---

## The WELL Distinction

"Arif is degraded" vs "WELL evidence is stale":

| Statement | Meaning | Correct? |
|-----------|---------|----------|
| "WELL is degraded" | WELL service is broken | ❌ WRONG |
| "WELL evidence is stale" | Human biometrics expired 73 days ago | ✅ CORRECT |
| "Arif is degraded" | Arif's condition has worsened | ❌ WRONG — no evidence |
| "Human readiness is UNKNOWN" | No current evidence available | ✅ CORRECT |

### The correct WELL status

```json
{
  "well": {
    "service_health": "GREEN",
    "evidence_state": "STALE",
    "human_readiness": "UNKNOWN",
    "biometric_age_days": 73,
    "required_action": "HUMAN_INPUT_NEEDED",
    "note": "Service is healthy. Evidence is stale. Arif's current condition is unknown. No score fabricated."
  }
}
```

This preserves **maruah** (dignity):
- The system does not pretend to know what it doesn't know
- Stale evidence does not become a judgment about the human
- UNKNOWN is the honest state when evidence is missing

---

## What a Fresh Self-Report Restores

A simple self-report from Arif (e.g., "I slept 6 hours, feeling okay, moderate fatigue") would:

1. Set `human.evidence_type` to `self_report`
2. Set `human.freshness` to `current`
3. Update `human.state` based on reported indicators
4. Increase `weighted_consensus` (higher confidence → higher consensus)
5. Change `human_readiness` from `UNKNOWN` to a computed state

This does NOT replace biometrics. It provides a current evidence source until biometrics are restored.

---

## Implications for Readiness Assessment

The prior 74/100 score's "witness diversity" gap (scored 25/100) was based on a category error.

Corrected assessment:
- **Witness weights**: properly configured (0.42/0.32/0.26)
- **Witness confidence**: needs measurement per channel
- **Weighted consensus**: depends on confidence × weights
- **Real gap**: we don't know the per-channel confidence, so we can't compute actual consensus

The gap is not "witness diversity is low." The gap is "witness confidence is unmeasured."

---

## Status

- [ ] Arif ratification of this clarification
- [ ] Per-channel confidence measurement implemented
- [ ] weighted_consensus computation added to health endpoint
- [ ] Consensus threshold enforced in verdict logic

---

*DITEMPA BUKAN DIBERI — Forged, Not Given*
