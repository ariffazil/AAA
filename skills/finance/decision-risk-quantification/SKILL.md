---
name: decision-risk-quantification
version: 1.0.0
description: Use when asked to predict a price or size a trade.
tags: [risk, position-sizing, forecasting, volatility, kelly, falsification, uncertainty]
triggers:
  - "will it go up or down"
  - "what happens in N months"
  - "how much should I risk"
  - "will my stop get hit"
  - "can you predict"
  - "can AI trade better than humans"
  - a leveraged position, P&L or account screenshot arrives for assessment
---

# Decision Risk Quantification

> The forecast is the part nobody can compute. The barrier is the part anybody can.

Load when a human asks a prediction or sizing question — *will gold go up, what happens in three
months, should I close, how much should I risk, can you predict, can an agent trade better* — or
when a claimed forecasting edge has to be tested rather than believed.

The deliverable is never a direction. It is an envelope, a barrier probability, and a growth curve,
with the refusal stated first and the arithmetic kept intact.

## 1. Never answer a prediction question with a prediction

Measured, so this is a floor and not an opinion:

- A death-cross state (EMA50 < EMA200) across 30 large caps / 7,858 stock-months flagged a coming
  >=50% drawdown only **7.8%** of the time. Roughly 92% of real collapses carried no such signal;
  lift over the base rate was 1.84x. Treat this as the ceiling for crossover and indicator claims.
- On an anonymised chart test where the second half was hidden, real analysis scored 6/8 —
  identical to answering the majority outcome for every item. The strongest visible run produced
  the weakest hidden run.
- An organ's own refusal verdict (`SABAR` and equivalents) is a **verdict, not a failure**. Deliver
  the refusal and name the gate that failed. Never substitute a chart for the gate.

So: state the no-edge finding first, then supply what *is* computable. A flat refusal wastes the
question; a refusal with arithmetic behind it is the answer.

**The test:** anyone who could predict would be trading it, not explaining it. Absence from the
market is the evidence — including your own.

## 2. Answer with the noise envelope, not a target

```
sd(t) = sigma * sqrt(t)              sigma = std(weekly log returns) * sqrt(52)
band  = spot * exp(+/- z * sd(t))    z = 1.28 -> 10th/90th,  0.67 -> 25th/75th
```

- Draw in log space so the fan is symmetric about the median.
- Print realised `sigma` and its lookback on the artifact.
- **Caption it as the range ordinary movement permits — never as a forecast.** An uncaptioned cone
  gets cited as a prediction by the next reader. Give a calibration anchor too: at ~22% annualised,
  three months spans roughly +/-11%.

## 3. Then price the barrier — that is the actionable number

Whether a stop is hit is a **first-passage** problem. It depends on the stop's distance relative to
`sigma*sqrt(t)`, not on the direction being right.

Run a seeded Monte Carlo, report a hit rate as a number rather than an adjective, and state the
invariant out loud: direction never entered the calculation.

Measured pair at 22.3% annualised over 3 months: a stop 2.1% from spot was hit in **78%** of paths;
an 11% barrier in **27%**. Same direction, same volatility, same horizon — only the barrier moved.

When the barrier sits inside the noise, name the consequence: **that is a sizing error, not an
analysis error.**

## 4. Reward:risk is meaningless without the win rate

```
expectancy = p*b - (1-p)                     b = reward:risk
growth     g(f) = p*ln(1 + f*b) + (1-p)*ln(1-f)
optimal    f*   = (p*(b+1) - 1) / b          (Kelly)
```

| size f | edge present (p=0.45, b=1.5) | no edge (p=0.40, b=1.5) |
|---|---|---|
| 1%  | +0.117% per trade | -0.008% |
| 5%  | +0.433% | -0.185% |
| 10% | +0.495% | -0.731% |
| 20% | **-0.467%** | -2.894% |
| 50% | -12.9% | -19.2% |

`g(f)` is **asymmetric** — past `f*` growth falls fast and crosses zero, so oversizing costs far more
than undersizing. At p=0.45 / b=1.5 the curve peaks near 8.3% and is **already negative at 20%**: an
edge can be surrendered purely by betting too big. With no edge the optimum is `f* = 0`.

Two traders can quote the same "1:1.5" and one can be losing at every size. **Never relay an RR
headline without asking for `p`.** If `p` is unknown, say it is unknown — do not assume 50%.

## 5. Testing a claimed edge instead of arguing about it

When the question becomes *can you actually tell*, build an experiment rather than a demonstration:
blind stimulus, committed guess, sealed answer, score reported beside its trivial baseline. Full
recipe — including the outcome-balance check that decides whether the test can falsify anything at
all: `references/prediction-test-recipe.md`.

## 6. Delivery to a numeric-averse reader

When the recipient has signalled that figures themselves are the barrier (*aku pening matematik*,
*cuba hang lukis*, *aku x faham hang tulis number*), the figure IS the explanation:

- One contrast per panel, three panels maximum. Words on the panel; a number may appear, an equation
  may not.
- Show the **baseline** beside the result on any comparison. A score alone reads as skill.
- Name in the caption the two things to look at, in ordinary language.
- Do not restate the figure as prose — that trains the reader to skip the image.
- Convert PNG to JPEG (~94) and deliver `MEDIA:/abs/path.jpg`.
- Run the collision vision pass before sending; see `visual-artifact-delivery` §3 and
  `human-facing-artifact-design` §1 (fourth case).

## Pitfalls

- **A cone without its caption becomes a forecast.** When the next reader forwards it, the caption
  is the only thing that does not travel.
- **Never let a chart stand in for a gate verdict.** If the organ refused, the chart may illustrate
  *why* the gate failed; it may not imply the call the gate declined to make.
- **`np.concatenate([[1.0], np.exp(np.cumsum(...))])`** — prepend the starting value, or the path and
  the x-axis are one element apart and matplotlib raises a shape mismatch.
- **Fix the seed and print it.** A Monte Carlo figure without its seed is not checkable; 60 paths
  shows the shape while ~500 is needed before quoting a probability.
- **Quote the denominator in any "N% of the time" claim.** Sensitivity, specificity, base rate and
  sample size move together; a hit-rate without its base rate is not a finding.
- **Do not invent `p`.** If the win rate is not measured, the expectancy and Kelly figures are
  illustrations, and must be labelled as such.

## Support files

- `references/noise-barrier-and-growth.md` — the three figure families with code shapes: volatility
  band, first-passage Monte Carlo, and the Kelly growth curve, plus the caption each one needs.
- `references/prediction-test-recipe.md` — building a falsifiable prediction test: anonymised
  stimulus, seeded label shuffle, sealed answer, constant-baseline scoring, and the outcome-balance
  check that decides whether the test can falsify anything.
