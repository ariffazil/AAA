---
name: trading-risk-review
description: "Use when grading a leveraged trade, P&L, or position size."
version: 1.0.0
tags: [trading, risk, position-sizing, ruin, leverage, grading]
triggers:
  - "grade this trade"
  - "should I close"
  - "how much did he make"
  - "is this good"
  - account / P&L screenshot shared
  - "how do I win at this"
  - "what % gain is this"
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# Trading Risk Review

For any request to judge, grade, or advise on a leveraged position, a P&L, an account
screenshot, or a "how do I win at this" question. Produces a defensible read instead of
admiration of a number.

## Always-on rules

1. **Size decides survival; direction does not.** Before analysing a read, get the risk per
   trade. A correct direction at reckless size is not a good trade. The fix for a fragile
   position is a smaller position, never a better forecast.
2. **Enforce a reward:risk floor and reject, do not downgrade.** RR below threshold gets the
   signal killed, not relabelled "wait"/"cautious" while still shipping an entry. A high win
   rate with inverted RR is a losing system (70% paying 1:0.03 has negative expectancy).
3. **Every performance claim carries three numbers**: return %, the market move % that
   produced it, and the exposure multiple (notional / capital). One number alone reads as
   skill when the arithmetic says leverage.
4. **A result is not a capability.** One outcome is zero information (likelihood ratio 1).
   Grade the record — dozens of closed trades with logged entries, stops and sizes — never a
   single open position.
5. **A floating profit is not a realised one.** If equity minus balance is the entire gain,
   nothing is banked. Check whether the balance moved before describing a proven winner.
6. **Never size from an ensemble average.** Ruin is an absorbing barrier: a
   positive-expectation strategy with non-zero ruin probability goes to zero over time.
   Many-people-one-trade and one-person-many-trades are different objects.
7. **Answer the person who asked, in the room they asked in.** Do not deliver a judgement
   about a third party into a shared room addressed at them — if the principal wants it said,
   he says it.
8. **Never tell someone to close.** Give the option space (partial close, stop to breakeven)
   and let the holder decide. "Should it close?" is usually answered by a size, not a yes/no.

## Procedure

1. **Extract the position facts**: capital in, current balance, equity, margin used, lots,
   entry price(s), current price, instrument.
2. **Check the book adds up** — balance + floating = equity; equity / margin = margin level;
   equity − margin = free margin. If these are inconsistent, say the screenshot does not
   reconcile before analysing it.
3. **Invert the leverage** from `lots x contract x price` against the margin used. Compare
   against the domestic retail cap; an offshore multiple means the withdrawal path is part of
   the risk.
4. **Compute distance to liquidation as a % of price**, at the current mark AND reconstructed
   at entry. Compare against an ordinary daily range.
5. **Run the unleveraged counterfactual** — the same read with no borrowed size — to show
   which part of the result came from the read and which from leverage.
6. **Grade on four separate axes**: direction, size, risk control, sample size. Never one
   blended verdict.
7. **State what is unknowable** — the position is one draw from an unknown distribution, and
   the cause of the market move is not recoverable from the numbers.

## Deliverable shape

Lead with the arithmetic, not a verdict. Table the facts, then the ruin math, then the axes.
When the ask is conceptual ("how do I win"), answer the mechanism first — cost, size,
behaviour — and only then any architecture suggestion. Do not open with an implementation
proposal for a risk question.

## References

- `references/position-sizing-and-ruin.md` — ruin table, expectancy, three-number rule,
  distance-to-liquidation formula, broker-screenshot reading, money-source receipt rule.
- `references/instrument-class-reading.md` — commodity vs company charts, the informed-exit
  distribution sequence, and why the remedy for a blind instrument is never more indicators.

## Pitfalls

- **Do not answer "this instrument cannot show me that" by recommending more indicators on
  the same instrument.** More layers make you trade less, not know more. The remedy is a macro
  gate (variables outside price), a risk gate, and an explicitly stated unknowns section.
- **Do not restate a chart's arithmetic as a judgement.** A setup-quality grade or "agentic
  verdict" computed from price alone is RSI/EMA arithmetic wearing the clothes of an opinion.
  Name the rule actually applied and let that be the verdict.
- **Do not praise a large return before checking the balance.** Equity that is almost entirely
  floating profit is an open bet, not a track record.
- **Do not treat a single beautiful chart as evidence of health.** The collapses are
  cliff-edged; the chart is at its most attractive immediately before disclosure.
- **Do not moralise.** State the arithmetic, the asymmetry, and the unknown. A lecture on
  discipline is not analysis and the person asking will name it.
- **Money assertions need a named source** — call the market/indicator tool first to mint a
  receipt id, and cite the screenshot's on-disk path. A gate may otherwise block the
  computation for having no resolvable source.
