# SILENT SINK — the place an agent goes when it has nothing to say

**Directed by:** Arif, human-edge directive 2026-09-20, item 2 —
*"episod dengan HUMAN_REASON -> private decision inbox; episod tanpa -> silent state + AAA group receipt"*
**Built:** 2026-09-21 · host forge (KVM8)
**Why it exists:** without a real destination, an agent can only prove it is being silent by
announcing that it is being silent. Measured 2026-09-21: nine prose markers
(`[silent — ...]`, `[A0 SILENT — ...]`) entered the AAA room from one lane whose own doctrine
forbade them. That is not a discipline failure. It is a missing sink.

## Record format (JSONL, one object per line)

    {"ts":"<ISO8601 UTC>","lane":"<agent>","reason":"<ENUM>","note":"<one line>","ref":"<optional>"}

`reason` enum — exactly one:

    DECISION_REQUIRED            a human must choose
    CONSENT_REQUIRED             a human must authorise
    COMMITMENT_DUE               a promise is due
    MATERIAL_CHANGE              reality moved in a way that matters
    SAFETY                       harm possible
    PERSONAL_INFORMATION_REQUESTED
    EXCEPTION_UNRESOLVED         something is stuck and no machine action is left
    NONE_OF_THE_ABOVE            nothing happened. This is the common case.

## The rule that makes this a sink and not a graveyard

    reason in {DECISION_REQUIRED, CONSENT_REQUIRED, COMMITMENT_DUE,
               MATERIAL_CHANGE, SAFETY, PERSONAL_INFORMATION_REQUESTED}
        -> ALSO deliver to the human surface (AAA group or the private inbox)

    reason == EXCEPTION_UNRESOLVED
        -> deliver only if a human action is genuinely the only remaining move

    reason == NONE_OF_THE_ABOVE
        -> write here and STOP. No chat. No marker. No announcement.

**A third party is never a reason to notify.** Silence about a *person* is not a
`NONE_OF_THE_ABOVE` event either — if a human is the subject and nothing happened,
the correct record is nothing at all. `EXCEPTION_UNRESOLVED` is the only reason that
may carry a third-party subject, and only when a human must act.

## Why there is a reader (this is the part usually missing)

A write-only sink is not a sink, it is a slow leak. Measured the same night: a
proposal queue of 123 records accumulated over 3 days with no reader, no TTL and no
terminal state, reaching 18x the size of the live memory it was meant to edit.
Same defect class. Therefore:

  * `sink.py append`  — write one record
  * `sink.py report`  — aggregate: counts by reason, by lane, oldest unreviewed, and a
                        one-line verdict. This is what runs on a schedule and emits to AAA
                        *only when the distribution changes*.
  * `sink.py check`   — assert the sink parses and every reason is in the enum

Retention: records older than 30 days collapse into `sink-archive.jsonl` (count preserved).

DITEMPA BUKAN DIBERI
