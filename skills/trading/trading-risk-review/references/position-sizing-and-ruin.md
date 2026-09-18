# Position Sizing and Risk of Ruin

## 1. The ruin table

| Risk per trade | Losing streak to halve | Losing streak to −99% |
|---|---|---|
| 50% | 1 | 7 |
| 20% | 3 | 21 |
| 10% | 7 | 44 |
| 5% | 14 | 90 |
| 2% | 35 | 228 |
| **1%** | **69** | **459** |
| 0.5% | 139 | 919 |

State why when explaining it: the point of 1% is not that you will be wrong 69 times — it is
that **you do not know how many times you will be wrong**, so size for a streak you cannot
predict.

**Do not raise size after a win.** Raise on new equity only, and only once a hundred-trade
sample exists. Name the pattern when you see it: *losing small while the position was small,
winning big while it was reckless* — that teaches the wrong lesson about courage and is the
most common way an account dies.

## 2. Expectancy

```
Expectancy = (P_win x avg_win) - (P_loss x avg_loss)
```

A 70% win rate paying 1:0.03 has negative expectancy. A reward:risk floor is the
highest-value gate in any signal stack.

## 3. Three-number rule

Return % / the market move % that produced it / the exposure multiple. A leveraged account up
several hundred percent is often a sub-1% favourable move at an exposure hundreds of times
capital. If only the first number is given, the implied message is skill when the arithmetic
says leverage.

Unleveraged counterfactual: `capital / price = units`; `units x move = P&L`. The contrast
(thousands versus tens on the identical read) shows leverage, not judgement, produced the
result — and that without leverage the position would have been unaffordable at all.

## 4. Distance to the edge

```
move_to_liquidation = (equity - margin x stop_out_level) / (lots x contract x fx_rate)
```

Express as a **percentage of price**, then compare against an ordinary day's range. "This
account dies if the market moves 0.09%" is legible; a margin-level percentage is not.
Compute at entry too: a position that looks cushioned now may have been opened at near-full
margin, where the cushion is unrealised profit rather than design.

## 5. Broker-screenshot reading

- **Invert the leverage out of the numbers.** `notional = lots x contract x price`; convert
  margin used at the account FX rate (a live market quote, not a guess); the ratio is
effective leverage. Domestic retail caps sit near 1:20 for metals, so orders of magnitude
  above that means an offshore entity — which makes the withdrawal path part of the risk.
  Recommend testing a small withdrawal before treating the displayed balance as money.
- **Margin exceeding balance means the position was opened near full margin.** The headroom
  visible later is unrealised profit, not risk management.
- Closing converts floating to realised but does not deliver cash: close → balance →
  withdrawal, and each step can stall independently.
- **A partial close is not all-or-nothing.** Closing most of the position and leaving a
  remainder with the stop at breakeven converts an open bet into a banked win with
  optionality.
- Two positions in one direction are one decision, not a sample of two.
- If the account belongs to someone else, ask who bears the loss before commenting on the
  gain.

## 6. Why the house does not simply win

A casino's edge is locked in the rules and applies every round — playing longer must lose. A
market has no fixed house edge; participants trade against each other, roughly zero-sum before
costs. The recurring costs (spread, swap, commission) are the only true house edge and they are
small. The reason most retail participants lose is **size, then behaviour**: an uncapped loss
that becomes the whole account, winners cut early and losers held. So the honest framing is not
"the game is rigged" — it is that the player kills themselves, and the costs bury the body.

## 7. Money assertions need a named source

The pre-execution gate blocks a computation that asserts a money variable with no resolvable
source. Call the organ tool first and cite the receipt: live price / FX / macro via the market
tool (it returns a `receipt_id`), computed indicators via the indicator tool; both persist under
the wealth receipts log. Quote the receipt id and the input screenshot's on-disk path in the
working note.
