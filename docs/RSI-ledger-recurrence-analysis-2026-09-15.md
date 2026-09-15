# RSI Ledger Recurrence Analysis — empirical readout

> DATE: 2026-09-15 · METHOD: parse of /root/.local/share/arifos/rsi-ledger.jsonl
> STATUS: read-only measurement. Answers draft §6 questions #2, #6, #7. No mutation.

---

## What was measured

950 valid JSON rows (8 corrupt lines in the file). Time span 2026-09-09 → 2026-09-14
(5 days), ~191 distinct opencode sessions + 78 distinct 333-AGI sessions.

## The ledger is a PULSE log, not a DIAGNOSIS log

| Field | Count | Meaning |
|---|---|---|
| turn_rsi.pulse | 776 (82%) | per-turn heartbeat, actor opencode |
| recursive_improvement.pulse | 169 (18%) | OBSERVE-phase heartbeat |
| recursive_improvement.proposed | 2 | proposal emitted, never sealed |
| bottleneck→fix diagnosis rows | 5 (0.5%) | the only real DIAGNOSE records (3× 333-AGI + 2 proposed) |

The RSI DIAGNOSE→REMEDIATE spine is almost absent: 5 of 950 rows carry a bottleneck and
fix. The other 99.5% are heartbeats that say "I observed, nothing improved."

## Proposals without application (the inhale-only signature)

- `improvements` (fixes applied): 259 rows, ALL ZERO. Zero fixes recorded as applied.
- `improvements_proposed`: 945 rows, only 23 nonzero, sum = 26 proposals over 5 days.

26 proposals, 0 applications. This is the empirical signature of the F13 2026-09-10
diagnosis ("Tak flow lagi"): the loop INHALES (observes, proposes) but the EXHALE
(correction applied → reality re-tested → h updated) never lands in the ledger.

## No timing signal

`last_delta_s` is a dead field — min/median/max all zero. Inter-arrival time between
pulses is not recorded. Draft question #1 (bottleneck inter-arrival distribution) is
therefore unmeasurable from this store; the diagnosis rows carry no inter-arrival either.

---

## Answers to the draft's stability questions

**Q2 — is the ledger read, or written-only?**
Write side is dominated by heartbeat noise (82%), with diagnosis writes near-zero (0.5%).
Whether the ledger is READ at session start is not answerable from a write log — but the
signal that matters (diagnosis → fix) is barely being written at all.

**Q6 — recurrence rate / closed-loop pole.**
UNMEASURABLE from this store — not because there is no recurrence, but because diagnoses
are not logged. 5 diagnosis records across ~191 sessions ≈ 2.6% of the session rate.
The feedback signal (bottleneck → fix) is sampled far below Nyquist for the failure modes
the controller is meant to govern. This IS the finding.

**Q7 — gain of Imp.**
26 proposed / 0 applied. The forward path is open at the application step: proposals
either die unsealed, or the `improvements` field is simply not written on apply. Either
way the loop does not close at the correction step.

---

## Conclusion

The improvement loop, by its own ledger, is observation-plus-proposal, not a closed
diagnose → remediate → verify → apply loop. The three diagram corrections in the draft
(R ∉ S, inhale+exhale, independent Eval) are not merely theoretically correct — the
exhale correction is what this data is screaming for. 26 inhales, 0 exhales.

## Bounded recommendation (no mutation, for ratification)

The highest-leverage fix is NOT more crons. It is making the RSI DIAGNOSE phase mandatory
per session and writing a bottleneck record (with the L2 transition delta) every session,
so that (1) the feedback signal exists at ≥1× session rate, and (2) recurrence becomes
measurable next cycle. Without that, the loop has no difference signal to improve on —
which is exactly what the empty transitions/ store and the 0-applied ledger already tell us.
