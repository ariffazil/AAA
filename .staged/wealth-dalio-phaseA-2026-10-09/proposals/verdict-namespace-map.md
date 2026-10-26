# Verdict Namespace Map — WEALTH assessments vs arifOS constitutional verdicts

**Problem:** WEALTH output schemas use constitutional words (SEAL / HOLD / VOID / SABAR).
WEALTH is compute-only (555_COMPUTE_ONLY); bare use of these words risks authority confusion
with arifOS verdicts (666_JUDGE / 888_APEX). Violates separation invariant.

## Mapping (old → namespaced)

| Current WEALTH word | Proposed WEALTH output | Reserved for |
|---|---|---|
| `SEAL` | `WEALTH.ASSESSMENT-LOCKED` | arifOS arif_seal only |
| `HOLD` | `WEALTH.ASSESSMENT-HOLD` (or `assessment: hold`) | arifOS arif_judge only |
| `VOID` | `WEALTH.ASSESSMENT-VOID` | arifOS arif_judge only |
| `SABAR` | `WEALTH.ASSESSMENT-SABAR` | arifOS arif_judge only |
| `verdict` (field name) | `assessment` | arifOS `effective_verdict` only |
| `SAFE_TO_STUDY` ✅ | keep — already WEALTH-namespaced semantics | — |

## Patch strategy (proposal only — DO NOT patch yet)

1. **Phase A1 (this staging):** map + this doc. Zero source changes.
2. **Phase A2 (after F13 binary):** in `/root/WEALTH/wealth_mcp/` — rename top-level output
   field `verdict` → `assessment`, wrap verdict words as `WEALTH.<WORD>`. Keep old words as
   aliases in a deprecation map for one release cycle; log deprecation warnings in receipts.
3. **Phase A3:** remove aliases; grep-gate in pre-push hook (`repo_guard.py`) rejecting bare
   `(SEAL|HOLD|VOID|SABAR)` as top-level output values in `wealth_mcp/` (383 hits today across
   scripts/tests — most are legitimate internal constants; only *output* schema fields change).
4. **arif_judge_handoff:** handoff envelope already reserves verdicts to kernel — no change.

## Blast radius

Consumers of WEALTH MCP output: AAA state router, wealth-briefing-gates.py, chron bridges.
Each reads `verdict` field — single mechanical rename, covered by WEALTH test suite
(`test_wealth_core.py` etc.) before service restart. Service restart gated on F13 approval
per canonical build doctrine.
