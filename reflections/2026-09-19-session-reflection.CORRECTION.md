# Correction to the 2026-09-19 session reflection (delivered to the principal 10:12)

**Artifact corrected:** `reflections/2026-09-19-session-reflection.md` (sha256 22ecb591d7d7cfe0, 4240 bytes)
**Delivered:** telegram:267378578, 2026-09-19 10:12 (state SENT)
**Correction written:** 2026-09-19, after the delivery — commit 4e6a738e9 caught the claim 5 minutes later.

## The claim, retracted

> "26 identiti berganda masih ada."

**State: RETRACTED.** Not supported by measurement. It was recalled from an earlier number layer, not read off a live instrument.

## What the instruments actually say

| Measure | Instrument | Value |
|---|---|---|
| Routing-name groups whose BODIES differ | `collision_audit.py` (repaired 2026-09-19, commit 4e6a738e9) | **0** |
| Same-name groups, all address bands | same | 59 (one body, several addresses — intended view tree, harmless) |
| Bodies that could never load | same | **0** |
| `duplicate_identity_groups` / `_skills` | `skills-census.py --json`, witness_hash `a08a0496d24cf32d` | 26 groups / 51 skills — **a different question** (identity keys across surfaces), not unloadable skills |

The defect was reading one counter as the other.

**Correction to this correction (verified 2026-09-19, after the paragraph above was written).** An
earlier draft of this line traced "26" back to the 2026-09-16 FROM-ZERO audit's 24 declared-name
collisions, "resolved the same day in commit 1882799ee". Both halves of that are wrong, and both were
measured:

- **The date is wrong.** `1882799ee` is dated **2026-09-19**, not 09-16. The resolution came three
  days later, not the same day.
- **The count is wrong.** That commit's own record says it resolved **2** groups (Agent Onboarding,
  code-review) to zero — not 24.
- **The audit itself is real and traceable.** `reports/FROM-ZERO-live-audit-2026-09-16.md` line 50:
  "24 declared-name collisions (>1 body, same `name:`) among 486 canonical skills" — MEASURED. So the
  ancestor number exists; it simply is not connected to 26 by any evidence.
- **And the ancestry claim repeats the very error this file exists to name.** 24 counted declared-name
  collisions *inside canon*; 26 counts census identity keys *across surfaces*. Asserting descent from
  one to the other is reading one counter as the other — the defect, reproduced inside its own
  correction. Left visible rather than quietly removed, because a correction that hides its own
  retraction is the shape this whole session was about.

Also NOT in the delivered reflection, found by the same instrument run: **20 canonical addresses
resolve OUTSIDE the store root** — the store publishes bodies it does not hold. That is a separate
open debt, and it was missed by both the reflection and the first draft of this correction.

## Replacement sentence

> Sifar nama routing yang badannya bertindih. Yang tinggal 26 grup identiti berganda itu ukuran census — kiraan silang permukaan, bukan skill yang tak boleh load.

## What is NOT corrected

Everything else in that reflection stands, including the four detector false positives (1080→557, 331→80, 60→2, 1→0) and the open-debt list. Those were verified against commits f33764e65, 48e03c774, 1882799ee, e2de7ac22.

Note the shape: the instrument that measures routing collisions had never run — an unterminated f-string raised SyntaxError on every invocation since it was written. A gate that cannot fail measured nothing, inside the session whose whole subject was gates that cannot fail.
