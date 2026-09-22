# EPOCH-BINDING FOR CANONICAL CANDIDATES — Spec

> **Status:** CANON (received 2026-09-21)
> **Forged:** FI-008 (Kimi Code)
> **Purpose:** codify the invariant that prevents stale canon from gaining authority

---

## The invariant

\[
\boxed{
\textbf{No canonical candidate may outlive the reality epoch that produced it.}
}
\]

Change one relevant bit anywhere in the federation → candidate dies → recollect.

## Why this exists

Before this invariant:

```
machine moves
→ machine snapshots itself
→ machine declares snapshot canonical
```

After:

```
machine moves
→ witness notices movement
→ canonicalization becomes impossible
→ machine waits for reality
```

That is a maturity transition, not just a technical change.

## The three-tier distinction (never confuse these)

```
Historical Artifact    = what was actually produced at time t
Candidate Canon        = potentially ratifiable representation, time-bound
Active Canon           = constitutionally accepted representation
```

\[
\boxed{
\text{ArtifactExistence} \neq \text{CanonicalValidity}
}
\]

Protects from rewriting history (machine law #7) while preventing bad history from gaining authority.

## CanonicalEligible — the continuous lease

\[
\text{CanonicalEligible} = Q_{\text{pre}} \wedge I \wedge D \wedge Q_{\text{during}} \wedge Q_{\text{post}}
\]

Where:

- **Q_pre** — quiet ≥ threshold *before* collection starts
- **I** — identity/contract completeness (every organ's identity tuple is observable)
- **D** — deterministic recollection (root₁ == root₂ across independent re-collection)
- **Q_during** — zero federation mutation during evidence capture (the race-fix)
- **Q_post** — state still matches immediately before ratification

If any state changes during the COLLECT → BUILD → VERIFY → SEAL chain, Q → 0 and the candidate becomes:

\[
\text{INVALIDATED\_BY\_DRIFT}
\]

Not "almost valid." Not "still pending." **Invalidated.**

## The race condition this fixes

Without Q_during:

```
quiet 60 min ✓
   ↓
begin collection
   ↓
organ changes
   ↓
collection finishes
   ↓
root internally deterministic
   ↓
SEAL stale mixed-time reality ✗
```

With Q_during enforced as a continuous lease (not entry ticket):

```
quiet 60 min ✓ (Q_pre)
   ↓
begin collection
   ↓
organ changes → detector fires → Q_during = 0 → CANDIDATE INVALIDATED
   ↓
recollect required
```

## The pipeline (Observer ≠ Judge)

```
REAL SYSTEM
   │
   ▼
quiet detector            ← OBSERVER: "is it moving?"
   │ { changed, quiet_since, eligibility }
   │
   ├─ MOVING → HOLD
   │
   └─ QUIET
        │
        ▼
   collect evidence         ← COLLECTOR: "what is observable?"
        │
        ▼
   identity contracts       ← VERIFIER: "is identity complete?"
        │
        ▼
   build candidate          ← BUILDER: "produce candidate from evidence"
        │
        ▼
   independent verify       ← VERIFIER: "is evidence internally consistent?"
        │
        ▼
   recollect / recompute    ← PROOF: "root₁ == root₂ ?"
        │
        ▼
   check no drift           ← OBSERVER: "is reality still quiet?"
        │
        ▼
   JUDGE                    ← F13 SOVEREIGNTY: "is this ratifiable?"
        │
        ▼
   SEAL                     ← F13: ratify or invalidate
```

**None of the components produces truth:**
- Quiet detector produces observation, not judgment
- Verifier produces evidence, not ratification
- Builder produces candidate, not authority
- Recollect produces proof of determinism, not seal
- JUDGE is sovereign; nothing else

```
Verifier should not produce truth.
Quiet detector should not produce truth.
Collector should not produce truth.
A-FORGE should not produce truth.

They produce evidence and transformations.

Canon becomes authoritative only through the governed boundary.
```

## Current state — honest

\[
\boxed{
\text{STABLE ENOUGH TO OBSERVE, NOT YET STABLE ENOUGH TO CANONIZE.}
}
\]

This is not degradation. It is the architecture learning the difference between:

> "I can produce a snapshot"

and

> "Reality remained still enough that this snapshot deserves authority."

## What this changes about my prior work

### fed-002 DRAFT — annotation escalation

**Old:** `ANNOTATED_DO_NOT_RATIFY` (was: candidate canon, gated on quiet interval)
**New:** `INVALIDATED_BY_DRIFT` (was: candidate canon, but Q_during violated)

Per Q_during: fed-002 was collected at 02:34 MYT. At that moment A-FORGE had moved +1 commit (89b2bac7) from its fed-001-recorded state (26bc319028). The substrate was still moving when fed-002 collection began. **Q_during = false at construction time.**

The DRAFT is preserved as HISTORICAL ARTIFACT (machine law #7 — never destroy evidence) but it is no longer a candidate canon. Recollection required from a quiet substrate that holds throughout the entire pipeline.

### fed-001 — current state

fed-001 was collected at 02:15 MYT. A-FORGE moved at 02:19 MYT. Therefore fed-001 is a HISTORICAL ARTIFACT (correctly), not an accurate description of current reality. It remains in the canonical path `/etc/arifos/canon/federation-release.json` because removing it would require F13 binary.

**There is currently no active canon.** The verifier reports DRIFT continuously because reality has moved past fed-001.

## What "next" engineering work looks like

The user's prescription: stop building more verifiers. Engineer the tiny invariant:

```
No canonical candidate may outlive the reality epoch that produced it.
```

Implementation shape:

1. **Canonical candidate envelope** — every candidate carries:
   - `reality_epoch` (federation_root at moment of collection)
   - `lease_expires_at` (Q_post deadline)
   - `invalidation_events` (any drift during pipeline → populate this)

2. **Epoch-binding check** — before any SEAL:
   - Re-compute current federation_root
   - Compare to candidate.reality_epoch
   - Mismatch → INVALIDATED_BY_DRIFT, refuse SEAL

3. **Lease refresh protocol** — when reality moves, all in-flight candidates are auto-invalidated; recollect.

This is roughly 1-2 days of arifOS kernel work, then F13 binary to activate.

## See also

- `/root/AAA/canon/7-MACHINE-LAWS.md` — substrate canon (law #6 most relevant)
- `/root/AAA/canon/13-CONSTITUTIONAL-LAWS.md` — A2A layer canon
- `/root/AAA/specs/a2a-constitutional-layer.md` — implementation patterns
- `/root/AAA/forge_work/2026-09-21-federation-stabilization-tasks/REMAINING.md` — task state
- `/root/AAA/forge_work/2026-09-21-federation-stabilization-tasks/fed-002-DRAFT.json` — historical artifact example

⚒️ DITEMPA BUKAN DIBERI
