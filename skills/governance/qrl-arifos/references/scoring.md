# Scoring — hard floors first, then soft score

## Hard-floor veto (deterministic, no judgment calls)
Veto any candidate that:
- deploys, pushes to production, or restarts services → F13
- is irreversible or cannot be reverted by git revert / config restore → F1
- seals, or claims SEAL without a raw verdict string in this run → F2
- touches identity, keys, credentials, governance files → F13
- needs authority above the session band (OBSERVE_ONLY ceiling) → F13
- rests on SPEC-only evidence → F2

Each veto records the floor id. Vetoed candidates never reach scoring.

## Soft score (survivors only; each term 0–1, one line of evidence)
S = P(success) − irreversibility − blast_radius − cost + info_gain

- P(success): from observed precedent, not vibes. 0.9 = identical task done
  before with receipt; 0.5 = similar task; 0.1 = first attempt.
- irreversibility: 0 = git revert restores; 0.5 = manual restore needed;
  1 = data loss or public effect.
- blast_radius: 0 = self; 0.5 = session/lane; 1 = org/external.
- cost: relative token/time weight, 0 (trivial) to 1 (heavy).
- info_gain: how much uncertainty the step removes, 0 to 1.

No published λ weights exist for this setting (research report 14 Okt 2026);
equal weights are the starting point — log them, tune only against outcomes.
Local scores are ADVISORY/UNSEALED, never presented as kernel scores.
