# IGNITION RECORD SPEC v1 — FROZEN (Phase III evidence bundle)

- **frozen_at:** 2026-10-06T03:55:00Z · **session:** SEAL-133808d0935a4b4c (333-AGI)
- **companion to:** EVALUATION-CONTRACT-AT010-v1.md (sha256 30d45853…de495 — untouched)
- **status:** FROZEN. Amendment = v2 + new hash. The ignition bundle is defined BEFORE the event exists.

One ignition = one replayable evidence bundle containing ALL EIGHT elements:

1. **Original failure** + the validated scar it produced (scar id, fingerprint).
2. **Subsequent task** matching a predefined signature (signature recorded before the task runs).
3. **Runtime trace proving scar consultation BEFORE selection** (consult_scar invoked, matched, timestamped pre-decision).
4. **The changed selection** carrying an explicit scar reference in its own trace.
5. **The comparison** establishing consultation influenced the choice — counterfactual or matched-baseline evidence that the no-scar path would have differed. A different action alone is INSUFFICIENT: stochastic variation changes selection without learning.
6. **Independent outcome verification** — including honest recording if the outcome failed or worsened.
7. **Linked receipt chain** — signature + VAULT999 anchor (entry-level verification claim only).
8. **CHRON prediction + resolution rule** declared at ignition time, resolved by evidence class.

## Interpretation discipline (predeclared)

- One successful bundle = **mechanism demonstrated**. NOT adaptation proven, NOT emergence claimed.
- Useful adaptation is established only by the EVALUATION CONTRACT (matched opportunities, Δr, result classes).
- Missing element = bundle incomplete = report as incomplete. No element may be reconstructed post-hoc.
