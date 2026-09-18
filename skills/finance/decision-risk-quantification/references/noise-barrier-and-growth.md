# Noise, Barrier and Growth — the three computable figures

Three figure families answer the questions humans actually ask about a position. None of them
forecasts direction. Each must carry the caption that stops it being read as one.

## 1. The volatility envelope (the "cone")

Answers: *where can price be in N months?* — as a range, never as a target.

```python
logret = np.diff(np.log(weekly_closes))
sigma  = logret.std() * np.sqrt(52)        # realise from ~3y of weekly bars
T      = months / 12
for z, band in ((1.28, '10/90'), (0.67, '25/75')):
    up = spot * np.exp( z * sigma * np.sqrt(T))
    dn = spot * np.exp(-z * sigma * np.sqrt(T))
```

- Draw the bands in log space, so the fan is symmetric about the median.
- Label each boundary at the right edge (`90th 5,020` / `75th 4,691` / `median 4,353` / ...).
- Print the realised `sigma`, its lookback and the source in the footer.
- Caption: **the range ordinary movement permits** — explicitly not a direction.
- Calibration anchor to hand the reader: at ~22% annualised, three months spans roughly +/-11%.
  Any stop closer than that band lives inside the noise.

## 2. The first-passage barrier (stop-hit probability)

Answers: *what is the chance my stop gets taken?* — the actionable number.

```python
rng  = np.random.default_rng(SEED)          # fixed seed -> reproducible figure
dt   = T / STEPS
path = np.concatenate([[1.0], np.exp(np.cumsum(z*dt_sd - 0.5*dt_sd**2))])
hit  = np.where(path >= 1.0 + barrier_pct)[0]
```

- Prepend the `1.0` or the path and the x-axis are one element apart and matplotlib raises.
- Truncate each hit path at the crossing so the eye reads "stopped" not "continued".
- 60 paths shows the shape; ~500 before quoting a probability.
- Two panels side by side — same volatility, same horizon, two barrier distances — is the clearest
  teaching object: green survivors, red hits, the hit count in large type at the corner.
- **State the invariant out loud:** direction never entered the calculation. Only barrier distance
  did — which is why sizing, not prediction, is the controllable term.
- Put the seed in the footer. A Monte Carlo figure without its seed is not checkable.

Measured pair (22.3% annualised, 3 months): barrier 2.1% -> **78%** hit; barrier 11% -> **27%** hit.

## 3. The growth curve (Kelly)

Answers: *how much should each trade risk?*

```python
def g(f, p, b): return p*np.log(1+f*b) + (1-p)*np.log(1-f)
f_star = (p*(b+1) - 1) / b
```

Plot two curves on one zero axis and let the picture make the argument:

- **With edge** (p=0.45, b=1.5): peaks at `f* ~= 8.3%`, then falls and crosses zero — an edge can be
  lost purely by betting too big.
- **Without edge** (p=0.40, b=1.5): optimal size is `f* = 0`. No amount of analysis repairs it
  *on this chart*.
- Mark the 1% line (professional norm) and a 20% line annotated *still losing, even with an edge*.
- The asymmetry is the whole lesson: undersizing costs a little, oversizing costs everything.
  Everyone who is wiped out is wiped out by being too large, never too small.

## Captions that keep each figure honest

| Figure | Required on the artifact |
|---|---|
| Cone | realised sigma, lookback, source, and the words *range ordinary movement permits* |
| Barrier MC | seed, path count, barrier distance, and *direction was not used in this calculation* |
| Growth curve | `p` and `b` used, and whether `p` was MEASURED or assumed |

Never let any of the three stand in place of a gate verdict. If the organ returned a refusal, the
figure may illustrate why the gate failed; it may not imply the call the gate declined to make.

## Proof discipline

- Every figure regenerable from a seed and a source; both in the footer.
- Before delivery, run the vision pass as a **collision** question (overlapping annotations, clipped
  labels), not a legibility one — see `visual-artifact-delivery` §3.
- For a numeric-averse reader the figure is the explanation: one contrast per panel, words on the
  panel, no equation in the rendered text.
