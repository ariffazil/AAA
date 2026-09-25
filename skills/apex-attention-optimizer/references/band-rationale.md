# Band Rationale — why 0.20 / 0.50 / 0.85

## What canon gives

- W³ (witness credibility) has explicit hysteresis bands: 0.75 / 0.85 / 0.95.
  Source: `/root/AAA/canon/APEX-REALITY-KERNEL.md` §"W³ Governance Law"
- BIJAKSANA ratio has **no** canonical band — only the formula.

## What the optimizer chose

The bands (0.20 DEGRADED / 0.50 OPERATIONAL / 0.85 STRONG_WISDOM) mirror W³
hysteresis shape (3 bands, 0.10 width apart, ceiling at 0.95+) but are
**declared policy**, not doctrine. Reasoning:

- 0.85 chosen as STRONG because it matches the W³ STRONG_WITNESS threshold
  (≥ 0.85). A turn whose BIJAKSANA is at least as strong as a SEAL-grade
  witness is SEAL-worthy.
- 0.50 chosen as the OPERATIONAL floor — half the ceiling. Anything below
  means the debt term is dominant; the turn is degrading state.
- 0.20 chosen as the DEGRADED/BANGANG boundary — a fifth of the ceiling.
  Below this, the turn is noise regardless of how clean it looks.

## How to revise

When canon catches up and assigns explicit bands:

1. Do not silently move the cutoffs. That is an auditability defect — a
   later reader cannot tell whether the change came from doctrine or drift.
2. Edit `APEXScorer.score` with the new thresholds and a comment naming the
   amendment (date + canon path).
3. Add a one-line entry to a `references/changelog.md` (do not create per
   amendment — extend this one).
4. Re-run the demo; the clean turn must still ALLOW and the jargon turn
   must still HOLD, otherwise the change broke the gate.

## What NOT to do

- **Do not tune to make more turns ALLOW.** A band tuned to pass
  comfortable output is the same defect as Goodhart's law — the metric
  succeeds at the expense of the purpose. The purpose is fewer confusing
  turns, not higher pass rates.
- **Do not tune to make more turns HOLD.** A gate that always blocks is a
  gate that always fails; the human stops sending things through it.
- **Do not add a fourth band.** W³ has three. Mirror the shape.
