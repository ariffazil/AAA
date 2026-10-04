# Auditing a Self-Issued Constitutional SEAL Artifact

Pattern: a sibling lane (e.g. 333-AGI) produces a constitutional audit PDF/artifact for its own doctrine work and issues its own `VERDICT: SEAL`. Verified 2026-08-08 on `AAA_ZEN_ALIGNMENT_CONSTITUTIONAL_AUDIT_2026-08-08.pdf`.

## The three structural checks (run BEFORE claim-by-claim)

1. **Gödel lock:** is the auditor the author? A lane auditing its own doctrine and issuing SEAL is the same 666→888 compression the audit itself warns about. Flag: "The audit cannot certify itself." Adjust verdict SEAL → SEAL-CONDITIONAL.
2. **Unsourced numbers:** every quantitative claim must carry a derivation path. No derivation → downgrade the epistemic band: "67% coverage" → PLAUSIBLE; "20 → 80 separation of powers" → ESTIMATE (no baseline, no rubric); "~−2.5 ΔS (qualitative)" → UNKNOWN (labelled qualitative to escape falsification). An audit that adds decorative numbers has positive ΔS — say so.
3. **SHA/provenance anchors:** verify every cited SHA256 against the live filesystem (`sha256sum`) BEFORE trusting the evidence table. The doctrine layer usually verifies; the numbers layer usually doesn't.

## Verification ledger shape

| # | Claim (C-ID) | Live evidence (exact command) | Verdict |
|---|---|---|---|
| C-1 | cited SHA `fe2c9994…` | `sha256sum /root/AAA/docs/...md` | ✅ TRUE |

Verdict conventions: ✅ TRUE (live match) · ⚠️ PARTIAL (direction right, derivation missing) · ❌ FALSE (form violation / unsourced number) · ❓ UNVERIFIABLE.

## Verdict adjustment rules

- Doctrinal layer (what changed, commits, SHAs) → verify, keep.
- Quantitative layer (scores, percentages, ΔS) → re-band with epistemic tags.
- Verdict form → **SEAL-CONDITIONAL** with a conditions table (condition / required action / owner).
- Report a trust split as numbers: "Trust the doctrine at 90%. Trust the verdict at 30%."

## Output contract

- Lead with the verdict adjustment, not prose.
- Corrected v2 shape: reframed verdict box, epistemic tag on every number, F13 note ("This audit cannot certify its own correctness; F13 sovereign review required for SEAL to be governance, not theatre"), verification ledger appended as appendix.
- Distinguish form failure from substance failure: "SEAL-form failure" (substance sound, verdict structure broken) is the common case — it means re-issue, not re-forge.
