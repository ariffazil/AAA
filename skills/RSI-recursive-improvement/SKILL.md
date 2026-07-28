---
name: RSI-recursive-improvement
description: >
  Recursive Self-Improvement protocol for AAA warga agents. Each agent iteratively audits its own
  outputs, identifies errors, computes correction vectors, and applies them before next execution.
  Governed by F1 (AMANAH — reversible only), F2 (TRUTH), F4 (CLARITY — ΔS ≤ 0), F7 (HUMILITY).
  RSI cycle: Observe → Diagnose → Correct → Verify → Metabolize → Repeat.
trigger_phrases:
  - recursive self improvement
  - rsi cycle
  - self audit
  - improve my output
  - iterative refinement
  - correct and verify
harness: copilot-cli|grok|claude|codex
domain: meta
risk_tier: LOW
autonomy: T1
forged: 2026-07-28
version: 1.0.0
---

# 🔄 RSI — Recursive Self-Improvement

> **DITEMPA BUKAN DIBERI** — Every agent improves through governed recursion, not unbounded self-modification.

## What This Skill Does

RSI (Recursive Self-Improvement) is the protocol by which AAA warga agents audit their own outputs, identify errors, compute correction vectors, and apply them before the next execution cycle. Governed by F1 (AMANAH — reversible only), F2 (TRUTH), F4 (CLARITY — ΔS ≤ 0, entropy must not increase), and F7 (HUMILITY — Ω₀ ∈ [0.03, 0.05]).

## The RSI Cycle

```
OBSERVE → DIAGNOSE → CORRECT → VERIFY → METABOLIZE → REPEAT
```

| Phase | Action | Floor |
|-------|--------|-------|
| OBSERVE | Review last output against ground truth | F2 TRUTH |
| DIAGNOSE | Identify root cause of any error | F4 CLARITY |
| CORRECT | Apply correction vector (reversible) | F1 AMANAH |
| VERIFY | Check correction improved the output | F2 TRUTH |
| METABOLIZE | Integrate learning into skill/scar | F7 HUMILITY |
| REPEAT | Cycle until Δ error ≈ 0 | F4 CLARITY |

## Enforcement

- RSI corrections are ALWAYS reversible (F1 AMANAH)
- No self-modification of constitutional floors
- Correction vectors must reduce or maintain entropy (F4 CLARITY — ΔS ≤ 0)
- Confidence in corrections capped at Ω₀ ∈ [0.03, 0.05] (F7 HUMILITY)
- Every RSI cycle emits a receipt to VAULT999 (F11 AUDIT)

## Key Paths

| What | Where |
|------|-------|
| RSI cycle script | `rsi-cycle.py` |
| RSI doctrine | `/root/AAA/governance/` |
| VAULT999 | `/root/arifOS/VAULT999/outcomes.jsonl` |

---

*DITEMPA BUKAN DIBERI — Improvement is recursive, not autonomous. The agent improves itself through governed observation and correction, never through unbounded self-modification.*