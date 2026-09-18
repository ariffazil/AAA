# Position Sizing and Edge Mathematics

Depth for the falsification and sizing rules in SKILL.md. Load when a human asks what a market will do, when
grading a leveraged position, or when someone quotes reward:risk as though it were a strategy.

## 1. The only controllable number

`Expectancy = p·RR − (1−p)·1` in R units. With RR fixed there is a break-even win rate, `p0 = 1/(1+RR)` — at
RR 1.5 that is 0.40. **Below p0 no sizing saves you; above it, sizing decides whether you survive long enough
to collect.** Never quote RR alone, and never invent `p`.

## 2. Ruin — losses before a drawdown

Each fixed-fractional loss costs `f`; losses to fall to half the account are `n = ln(0.5)/ln(1−f)`.

| Risk per trade | Losses to −50% | Losses to −90% |
|---|---|---|
| 50% | 1 | 7 |
| 20% | 3 | 21 |
| 10% | 7 | 44 |
| 5% | 14 | 90 |
| 2% | 35 | 228 |
| 1% | 69 | 459 |
| 0.5% | 139 | 919 |

The table answers one question — "how many times can I be wrong?" — and it matters because nobody knows how
many times they *will* be wrong.

## 3. The forward cone — how far price can wander

From realised volatility, never from opinion. Weekly log returns:

```
logret = diff(log(close)) ;  VOL = std(logret) * sqrt(52)
sd(t)  = VOL * sqrt(t_years)
level  = spot * exp(z * sd)
z      = -1.28 (10th) / -0.67 (25th) / 0 (median) / +0.67 (75th) / +1.28 (90th)
```

Multiplicative (lognormal) symmetry: the 10th and 90th sit at equal *ratios* from spot, not equal distances.
Gold at ~22% annualised gives roughly ±11% over three months.

**The cone is not a forecast — it is the width of ordinary noise, and it is the yardstick a stop must be
judged against.** Draw the fan, never a direction.

## 4. The barrier problem — stop distance is a sizing decision

Invert the cone: a barrier `d` away is `z = d / sd` standard deviations, and for a driftless walk the one-sided
hit probability over the horizon is `P ≈ 2·(1 − Φ(z))` — slightly conservative once any adverse drift is
present.

**Monte Carlo recipe** (validated, reproducible):

- `rng = np.random.default_rng(SEED)`, `dt = T/STEPS`, `sd = VOL*sqrt(dt)`, N ≈ 60 paths
- `path = concatenate([[1.0], exp(cumsum(z*sd - 0.5*sd**2))])`
- **The leading `1.0` is required** — without it the series is one element short of `arange(STEPS+1)` and
  matplotlib raises `x and y must have same first dimension` at plot time, not build time, so the arithmetic
  looks correct until the render dies.
- Seed it and print the seed. The count must be re-derivable, not asserted.
- Colour hit paths and survivors differently, and print the hit share on the panel.

One run, volatility and horizon identical, **barrier distance the only change**:

| Barrier from spot | Paths that hit it |
|---|---|
| 2.1% | 78% |
| 11% | 27% |

Same direction, same volatility, same analysis. **A stop sitting inside the noise band is not a protection, it
is a scheduled exit — and the remedy is size, not a cleverer stop.**

## 5. The Kelly curve — why "bigger size to catch up" always loses

`g(f) = p·ln(1+f·b) + (1−p)·ln(1−f)`, optimum `f* = (p(b+1)−1)/b`, where `b` = reward:risk ratio.

At RR 1.5, growth per trade:

| Stake | Edge (p=0.45) | No edge (p=0.40) |
|---|---|---|
| 1% | +0.117% | −0.008% |
| 5% | +0.433% | −0.185% |
| 10% | +0.495% | −0.731% |
| 20% | **−0.467%** | −2.894% |
| 50% | −12.9% | −19.2% |

Three things to say out loud:

1. **Over-betting converts a real edge into a loss** — 10% is near-optimal, 20% is negative, with the same win
   rate and the same RR.
2. **With no edge, `f* = 0`** — the best stake is nothing. Sizing cannot create an edge; it only decides how
   slowly the edge-less lose.
3. **The curve is asymmetric.** The penalty for being slightly too large exceeds the reward for being slightly
   too small. A blown account is a size failure, not an analysis failure.

## 6. Testing the claim you are about to make

**Base-rate test** (a rule):

```
base rate   = P(outcome)
conditional = P(outcome | signal)
sensitivity = P(signal | outcome)      <- the number that kills most indicators
specificity = P(-signal | -outcome)
lift        = conditional / base rate
```

Worked example — EMA50 < EMA200 ("death cross", monthly) as a predictor of ≥50% drawdown within 24 months, 30
large caps, all available history: **7,858 stock-months; base rate 4.1%; conditional 7.5%; sensitivity 7.8%;
specificity 95.9%; lift 1.84×.** Specificity of 95.9% is the mirage — "always say no" scores the same.
Sensitivity of 7.8% means the signal misses more than nine in ten of the events it claims to detect, which
makes it a trigger at best and never a diagnosis.

**Blind commitment test** (a predictor):

1. Pick N cases — **N ≥ 4 for a binary call**; with 3 a coin scores 33%.
2. Normalise to 100 at the cut; strip names, tickers, dates and prices.
3. Assign labels by seeded shuffle so label order carries no information.
4. Write the truth map to a **separate file**; do not read it until step 6.
5. Commit answers **and confidence** before the reveal.
6. Score against the trivial baseline (all-"no", always-up).

**If the analysis does not beat the baseline, report that. The null result is the finding.** Measured: an agent
scored 6/8 on eight anonymised charts — identical to answering "no" eight times without looking.

A useful secondary observation from the same run: the strongest first half produced the weakest second half,
and an unremarkable first half produced the strongest second. Past shape carried no forward information here —
which is exactly what the baseline comparison exists to reveal.

## 7. Build notes

- Filter matplotlib font-cache chatter from build stdout (`grep -v "Bad key\|probably need\|mpl-data"`) so a
  genuine traceback is the first thing visible.
- Read the script's own printed percentile/diagnostic table before writing prose around the numbers — that
  table is what the figure is asserting.
- Stagger labels for levels that sit close together, and give each an opaque background box, or four price
  labels land in one column of pixels. Confirm with a vision pass that asks the collision question.
- Render the picture and keep prose to one sentence per conclusion.
