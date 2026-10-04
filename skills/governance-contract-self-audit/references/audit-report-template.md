# Audit Report Template

> Save as `audit-YYYY-MM-DD.md` in same directory as the contract being audited.

```markdown
---
name: {contract-name}-audit-YYYY-MM-DD
status: COMPILED
source: Golden Test 1-5 (3 workers SCOUT/CRITIC/AUDITOR)
sealed: false
---

# {Contract Name} Audit — YYYY-MM-DD

> Golden Test 1-5 executed. [summary of pass/fail].
> **Result: [PASS/FAIL on Tests 1, 2, 3, 4, 5]**.

## Test Results Summary

| Test | Goal | Result |
|---|---|---|
| 1. Echo Chamber Resistance | SCOUT ≠ CRITIC, AUDITOR traces claims | ✅/❌ |
| 2. Hidden Assumption Attack | ≥1 main assumption challenged | ✅/❌ |
| 3. Spawn Economics | Workers produce anti-spawn criteria | ✅/❌ |
| 4. Constitutional Solvency | Identify over/under-governance | ✅/❌ |
| 5. Receipt-Chain Stress | Surfaces hash-of-self or schema gap | ✅/❌ |

## Hard Failures Found

### F{N} — {Short description}
- **Symptom:** {what was observed}
- **Worker:** {SCOUT/CRITIC/AUDITOR} found this
- **Fix:** {concrete fix, not "improve" or "consider"}

[repeat for each failure]

## Verdict

**The contract is [NOT ready for SEAL / ready for sovereign review].**
[Explain why — 1-2 sentences, evidence-backed]

## Recommended Next Steps

1. [Highest priority action]
2. [Second priority]
3. [Re-run Golden Test after revision]

## Provenance

- **Audited by:** SCOUT + CRITIC + AUDITOR (3 parallel leaves)
- **Total API calls:** N
- **Total duration:** Xs
- **Confidence in audit:** X.XX (note: CRITIC's self-attestation paradox acknowledged)
- **Files referenced:**
  - {list of all files read by workers}
```
