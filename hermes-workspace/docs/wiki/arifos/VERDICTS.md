# arifOS Verdicts

> **CLAIM** | Source: `canonical_schema_contract.json` | **Confidence:** 0.95 | **Epoch:** 2026-04-23

## Summary

Every arifOS tool output receives a verdict — the constitutional judgment on whether the output is safe to execute, hold for review, or void entirely.

---

## Verdict Registry

| Verdict | Meaning | Behavioral Rule |
|---------|---------|-----------------|
| **SEAL** | Safe to execute | Proceed. Passed all floor checks. |
| **HOLD** | Pause, human review needed | Do not proceed until Arif approves |
| **VOID** | Blocked — dangerous or manipulative | Stop. Do not execute. |
| **CLAIM_ONLY** | Grounded but not ratified | Claims are evidence, not instructions |
| **PARTIAL** | Some claims ratifiable, some not | Proceed with ratifiable parts only |
| **SABAR** | Not yet ratifiable, gather more | Wait, continue grounding |

---

## Verdict Authority

**888_JUDGE is the sole source of SEAL verdicts.**

All other tools emit CLAIM_ONLY unless overridden by 888_JUDGE.
This ensures no tool can self-approve — the separation of execution and ratification is architectural.

---

## Confidence Range

All verdicts carry a `confidence` value in the range **(0.03, 0.97)** — exclusive bounds.
- 0.97 = near-certainty (high evidence, all floors green)
- 0.03 = minimal evidence (SABAR triggered)

---

## Verdict Injection (Current Gap)

The canonical contract requires `original_tool_verdict` injection for SEAL verdicts.
Currently, `constitutional_guard` is a stub — it does not wire `original_tool_verdict` from the tool to the verdict bridge.

See `tests/test_contract_parity.py` — 25 xfails document this gap.

---

## Cross-References

- [[arifos/FLOORS]] — floor checks that feed into verdict
- [[arifos/888_JUDGE]] — SEAL authority implementation
- [[infrastructure/OBSERVABILITY]] — Nine-Signal metrics used alongside verdicts

---

## Status

**Evolving** — verdict injection mechanism not yet wired in runtime.

---

DITEMPA BUKAN DIBERI — 999 SEAL ALIVE