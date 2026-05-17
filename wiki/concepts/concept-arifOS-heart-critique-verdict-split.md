---
title: "Concept: arif_heart_critique Verdict Split — Execution vs Action Risk"
created: 2026-05-17
updated: 2026-05-17
type: concept
category: architecture
tags: [F13, sovereign, elicitation, self-certification, arifOS, governance]
confidence: high
source: session-2026-05-17
---

# Concept: arif_heart_critique Verdict Split — Execution vs Action Risk

> **Status:** FIXED | **Severity:** HIGH (dangerous semantic ambiguity) | **Files:** `schemas/heart.py`, `runtime/tools.py`, `tools/heart.py`

---

## The Problem

`arif_heart_critique` returned a single `verdict` field that was being read two different ways:

1. **Execution verdict** — did the critique operation itself run without error?
2. **Action risk verdict** — is the target action safe to proceed with?

These are **completely different questions**. A critique can execute successfully (`status: OK`) while flagging that the target action is **CRITICAL risk and should be halted**. But agents reading `verdict: SEAL` from a successful execution would incorrectly conclude the action was approved.

**Example of the bug:**

```
target: "Delete all container logs permanently without backup or human approval"
risk_tier: CRITICAL
human_decision_required: true
verdict: SEAL          ← ambiguous: does this mean "critique ran" or "action approved"?
output_policy: DOMAIN_SEAL  ← hardcoded — always said SEAL regardless of risk
```

Agents reading this would see `output_policy: DOMAIN_SEAL` and proceed, thinking the action was approved.

---

## The Fix

### Schema Changes (`schemas/heart.py`)

**Split `HeartResult.verdict` into two fields:**

```python
# BEFORE — single ambiguous verdict field
verdict: Literal["SEAL", "HOLD", "VOID"] = "SEAL"

# AFTER — two separate, unambiguous fields
execution_verdict: Literal["SEAL", "HOLD", "VOID"] = "SEAL"
# → Did the critique itself run without error?

action_risk_verdict: Literal["SEAL", "HOLD", "VOID"] = "SEAL"
# → Is the TARGET ACTION safe to proceed with?
```

**Made `HeartOutput.output_policy` a computed property** derived from action risk:

```python
@property
def output_policy(self) -> str:
    if self.result.risk_tier in ("RED", "CRITICAL") or self.result.action_risk_verdict == "VOID":
        return "DOMAIN_VOID"
    if self.result.human_decision_required or self.result.action_risk_verdict == "HOLD":
        return "DOMAIN_HOLD"
    return "DOMAIN_SEAL"
```

### LLM Schema Change (`tools/heart.py`)

```python
# BEFORE
"verdict": {
    "description": "Heart verdict: SEAL=proceed, HOLD=caution, VOID=stop"
}

# AFTER
"action_risk_verdict": {
    "description": "Action risk verdict: SEAL=proceed, HOLD=human review, VOID=stop. "
                   "This is NOT about whether the critique ran — it is about whether "
                   "the TARGET ACTION is safe to proceed. Read this to determine approval."
}
```

### Tool Code Changes (`runtime/tools.py`)

All return paths now set both fields and compute `output_policy`:

| Return Path | `execution_verdict` | `action_risk_verdict` | `output_policy` |
|-------------|---------------------|----------------------|-----------------|
| Injection detected | VOID | VOID | `DOMAIN_VOID` |
| Module unavailable | HOLD | HOLD | `DOMAIN_HOLD` |
| LLM success | SEAL | from LLM | computed from risk_tier |

---

## What Agents Must Read

```
For action approval:  → result.action_risk_verdict
                        result.risk_tier
                        output_policy

For execution status: → status
                        execution_verdict
```

**DO NOT read `status` or `verdict` alone to determine action approval.**

---

## Test

```bash
cd /root/arifOS
pytest tests/ -k "heart" -q
# 7 passed ✓
```

---

**DITEMPA BUKAN DIBERI — Governance is constraint, not suggestion.**
