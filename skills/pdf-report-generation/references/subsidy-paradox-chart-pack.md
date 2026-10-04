# Subsidy Paradox Chart Pack — Recipe

> Companion to `references/petronas-subsidy-paradox-2026.md` (numbers bank).
> Use when the deliverable is a PDF chart pack or a live-site chart strip
> showing the Malaysia fuel-subsidy-vs-PETRONAS-dividend paradox.

## When to use

- Any PETRONAS scenario fan that includes a "high oil = bull case"
- Any sovereign-page (/malaysia/) chart that needs to show why Brent
  above ~$95/bbl is a fiscal trap, not a windfall
- Any "/propa/" chart that needs to show the corporate binding
  constraint (cap × floor × subsidy) and the hidden-tax ratio

## Chart recipes (4 charts, all JS-free matplotlib)

### S01 — Subsidy Paradox: the inversion curve

Show Brent (x) → dividend, subsidy bill, net-to-budget (y), with crossover
marked explicitly. The "paradox zone" is where net < 0.

Inputs:
- `brent = np.arange(50, 131, 2)` ($/bbl)
- `petronas_pat = max(0, 24 + (brent - 65) * 0.7)` (RM B)
- `dividend = min(pat * 0.60, 50)` then `max(dividend, 20)` (60% cap × RM20B floor)
- `subsidy = piecewise: $65 → 8+(brent-50)*0.5; 65-90 → 15+(brent-65)*1.5; 90+ → 37.5+(brent-90)*0.8`
- `petrol_revenue = max(0, 60 + (brent - 60) * 0.5)`
- `net = petrol_revenue - subsidy` ← **the inversion curve**

Plot:
- 3 lines (gold=dividend, red=subsidy, navy=net)
- Fill green where `net >= 0` ("zone of comfort")
- Fill red where `net < 0` ("paradox zone")
- `np.where(np.diff(np.sign(net)))[0]` → find crossover Brent
- axvline at crossover, annotate "Paradox crossover · Brent ≈ $X"

### S02 — Subsidy regime history

Show years (x) → subsidy bill bars (y, colour-coded by severity) +
Brent avg line on twin axis.

Bands:
- GREEN: subsidy ≤ RM10B (commodity-stable regime, 2018-21)
- ORANGE: RM10-20B (transitional, 2024)
- RED: RM20B+ (war-shock regime, 2022 + 2026E)

2026E bill: RM30-40B per Anwar parliamentary reply (1 Jul 2026).

### S03 — Cap-floor-subsidy collision

Show PAT (x) → AMEND cap, MoF floor, subsidy cost (y).

Key geometry:
- `amend_cap = pat * 0.60` (governance ceiling)
- `mof_floor = max(20, pat * 0.40)` (fiscal floor)
- `subsidy = full(pat_range, 25.0)` (constant subsidy backdrop)

The crossover where `amend_cap == mof_floor` is at `pat = 20/0.60 ≈ 33.3B`.
Below that, the two instructions point in opposite directions.
Mark with axvline + annotation "Cap-floor collision at PAT = RM33.3B".

Also mark MoF FY26 outlook band (RM30-35B PAT) with axvspan in BLUE alpha 0.08.

### S04 — Hidden-tax ratio

Show Brent (x) → subsidy/dividend ratio (y). Parity line at 1.0.

Crossover at Brent ~$80 (where subsidy bill ≈ dividend).

Above parity: every ringgit PETRONAS pays in dividend costs the
government more than one ringgit in subsidy support.

## File output paths

- Live site: `public/<route>/_charts/S0[1-4]_<topic>.png`
- PDF report: `charts/S0[1-4]_<topic>.png`
- Both can share the same source PNG via `cp`

## Proven Aug 2026

Used on /propa/ + /malaysia/ coupled site revamp. 4 charts × 2 routes
= 7 PNGs (S01 only on malaysia, S03 only on propa, S02+S04 on both).
All HTTP 200, all rendered correctly in WeasyPrint PDF (no JS).