# APEX T-SCORE — Time-to-Zero-Trust

**Status:** DERIVATION + BACKTEST · F13-authored insight (Arif, 2026-09-18), agent-derived
**Origin:** F13 directive — *"Support is not a line. It's a point. Like a drilling location geologist pick. And it's all about trust."*
**Artifacts:** `/root/.hermes/workspace/apex-t-score.py` (build) · `apex_t_obs.csv` (24,256 obs) · `gen-apex-t.py` (figure)
**Full report (v3.0, theory paper, 19pp):** `/root/.hermes/workspace/APEX-T-SCORE-THEORY-v3.pdf`
— framed as a scientific theory: 6 axioms · 6 propositions · 8 falsifiable predictions
· 7 tests run (4 refuted) · 3 untested layers, each with stated falsification criteria
**Prior version (v2.0, 19pp):** `/root/.hermes/workspace/APEX-T-SCORE-REPORT-v2.pdf`
**Bound to:** APEX-ZEN canonical compression · state-transition-discipline · authority-envelope

---

## The Insight (F13, verbatim)

> "Support is not a line. It's a point. Like a drilling location geologist pick. And it's all about trust. And you can measure trust."

Three claims, each load-bearing:

1. **Support is a point, not a line.** A price chart collapses a 2-dimensional object (distance AND time) into one axis. The true support is a *location in (price, time)* — same as a drilling target, which is a point in (depth, location), not a depth alone.
2. **It is a drilling problem.** Depth ÷ penetration rate. Not "will it hit" — *how deep, and how fast.*
3. **The barrier is trust, and trust decays.** This is the structural addition over Merton.

---

## Derivation

### Step 1 — Merton (1974)
Equity is a call option on firm assets. Default when asset value crosses the debt barrier at maturity.

### Step 2 — Black & Cox (1976)
Generalise to first-passage: default occurs the **first** time V(t) touches barrier B, not only at maturity.

For log-price with drift μ and vol σ, expected first-passage time to a lower barrier:

```
E[τ] = ln(V/B) / ν ,        ν = σ²/2 − μ      (ν > 0)
```

**This is distance ÷ rate.** Identical functional form to depth ÷ penetration rate.

### Step 3 — the F13 addition: the barrier MOVES

Trust is the barrier. When trust decays:
- covenants tighten
- refinancing windows close
- suppliers demand cash terms
- counterparties shorten tenor

The barrier is **not fixed at B₀**. It lifts: `B(t) = B₀ · e^(λt)`, where λ = trust-decay rate.

Solving the moving-barrier first-passage:

```
APEX T-SCORE      T = ln(V/B) ÷ (λ − μ)

SURVIVAL CONDITION      μ > λ
```

**The firm must build value faster than trust decays.**

### Step 4 — Operationalisation (price-only)

| Term | Proxy | Rationale |
|---|---|---|
| V | current price | observable |
| B₀ | running-max × 0.20 | the −80% level; recovery from there is historically near-terminal |
| μ | log drift, trailing 12m | short-run value creation |
| λ | max(0, μ − g₆₀) | trust decay = short-run promise the long-run record has not backed |
| σ | realised monthly vol, 36m | |

### Step 5 — the Graham identity

> **Margin of Safety (Graham, 1934) ≡ Distance to Default (Merton, 1974)**

Both are `ln(V/B)`. Forty years apart, two literatures, one quantity. Value investing and structural credit risk are not analogues — they are the **same measurement** in different notation.

**Consequence for the gold-vs-company question:**
- **Gold** — `T = ∞` (cannot default), but **carry = 0**. Infinite time, no payment.
- **Company** — finite `T`, but **pays you to wait** (dividends, buybacks, growth).
- **Therefore:** the dividend is not a bonus — it is the *price of the firm's mortality*. High yield + wide distance = buy. Low yield + short distance = sell.

---

## Backtest

**Panel:** 67 names, 24,256 stock-months, 1968-01 → 2024-09, monthly adjusted closes
**Outcome:** price touches the −80% barrier within 24 months
**Base rate:** 4.1%

### T-threshold performance (corrected formula — see Defect Log)

| Signal | n | Hit rate | vs rest | Lift | Sens | Spec |
|---|---|---|---|---|---|---|
| T < 12m | 583 | 32.6% | 4.5% | **5.47×** | 28.6% | 96.3% |
| T < 24m | 1,373 | 21.7% | 3.7% | 3.64× | 44.9% | 89.7% |
| T < 36m | 2,130 | 17.1% | 3.3% | 2.87× | 54.8% | 83.2% |
| T < 60m | 3,430 | 12.8% | 2.9% | 2.15× | 66.1% | 71.5% |

**Reading it honestly:** at T<12m, one in three really collapses vs one in twenty-two otherwise — a 5.5× lift. But **two out of three do not**. This is information, not an oracle. It is a *triage* instrument.

### AVO / DHI mapping — HYPOTHESIS REFUTED

F13's observation: *"Candlestick chart is like seismic to me."* Mapped AVO onto the horizon axis:

```
A (Intercept) = μ_short           surface signal (momentum)
G (Gradient)  = μ_long − μ_short  how signal changes with depth
```

| Class | Description | n | Collapse rate |
|---|---|---|---|
| I | healthy (A>0, G>0) | 4,828 | 1.7% |
| II | inversion (A<0, G>0) | 6,888 | **7.8%** |
| III | bright spot (A<0, G<0) | 274 | 6.9% |
| IV | dim-out (A>0, G<0) | 12,266 | 2.8% |

**The AVO quadrant does NOT separate outcomes cleanly.** The hypothesis (dim-out = Enron shape = most dangerous) is **not supported**. Class II carries the highest rate.

**T separates. AVO quadrant does not.** This is consistent with the session's governing result: *added intelligence buys nothing; the constraint buys everything.*

---

## Defect Log (declared, not hidden)

**Defect 1 — inverted trust term (found and fixed in-session).**
First operationalisation used `λ = max(0, g₆₀ − μ)`. Effect: every stock-month in the dim-out quadrant (A>0, G<0) returned `T = ∞` — 12,265 observations, 50% of the panel, structurally excluded from the score. The quadrant the author expected to be *most* dangerous was the only one the formula silently dropped.

First-passage is governed by the **long-run** drift (the barrier's own time scale), with the short-run signal as the *unbacked-promise* term. Corrected to `ν = σ²/2 − g₆₀ + max(0, μ − g₆₀)`.

**Lesson:** a formula that returns a "clean" result on first run is suspect. Infinities distributed non-randomly across a category are a bug signature, not a finding.

**Defect 2 — survivorship.**
yfinance serves **no price history for delisted tickers** (probed: LEHMQ, ENRNQ, SHLDQ, JCPNQ, BBBYQ, HTZGQ, RSLHCQ, WCOEQ, AAMRQ — all empty; evidence ref `/root/.hermes/workspace/probe-dead-names.py`). The panel therefore contains **survivors only**. The genuinely dead are absent.

Direction of bias: the measured base rate (4.1%) is **understated**, so measured lift is **overstated** relative to true lift... but the *test population* is also harder (no easy kills), so the effect on sensitivity/specificity is ambiguous. **This is stated as a limitation, not resolved.**

**Defect 3 — price-only.**
No balance sheet, no actual debt, no covenants. The barrier is proxied as a price level, not a contractual threshold. Full form requires total liabilities, debt maturity ladder, and cash-flow coverage.

---

## Extension Path (not yet built)

1. **Bring in the balance sheet** — `Total Liabilities Net Minority Interest` and `Total Debt` are available for live names (probed 2026-09-18). Replaces the −80% proxy with an actual contractual barrier.
2. **Add cash-flow coverage** — operating cash flow ÷ interest, plus the NI-vs-OCF divergence (see `/root/.hermes/workspace/ni_vs_ocf.csv`) as the λ term. A firm whose profit is accrual-only has a widening gap between promise and delivery.
3. **Debt maturity ladder** — a wall of maturity is a *deterministic* λ spike. This is what killed Lehman (repo rollover) and Sears (supplier terms).
4. **Institutional λ** (Acemoglu) — governance structure enters as a *floor* on λ. Extractive structures cannot reduce λ below a positive level because the extraction itself is the decay.

---

## ADDENDUM — Bursa Malaysia test: Serba Dinamik (2026-09-18, same session)

**Question from F13:** *"Kalau kat bursa Malaysia. Serba Dinamik tu hang boleh predict ka x?"*

**Data source:** the issuer's OWN investor-relations pages
(`investors-centre.com/serbadk/investor-relations/ratio-analysis.html`) — the
figures Serba Dinamik itself reported. Retrieved read-only 2026-09-18.
Period note: FY-end changed 31 Dec 2020 → 30 Jun 2021; the "2021" column is an
18-month period, and FY2020 was never reported as a standalone year.

| Period | Assets (RM'000) | Liab (RM'000) | L/A | D | λ | **T** | OCF/PAT | cash/borrow |
|---|---|---|---|---|---|---|---|---|
| FY2018 | 4,370,755 | 2,282,580 | 0.522 | 0.650 | — | ∞ | **0.21** | 0.445 |
| FY2019 | 6,418,010 | 3,985,285 | 0.621 | 0.476 | +0.173 | **2.75 y** | **0.44** | 0.391 |
| FY2021 (18m) | 7,728,478 | 4,771,588 | 0.617 | 0.482 | −0.004 | **∞** | n/a | 0.126 |
| FY2022 | 6,436,697 | 4,532,210 | 0.704 | 0.351 | +0.088 | 3.84 y | n/a | 0.016 |
| FY2023 (3m) | 6,511,023 | 4,692,975 | 0.721 | 0.327 | +0.094 | 3.47 y | n/a | 0.010 |

### Answer: NO — and the failure mode is predictable

T fired once (FY2019, 2.75 years — before the scandal) and then **went blind
exactly when it mattered** (FY2021, T = ∞, when KPMG raised the audit issues).

**Why:** Serba Dinamik is not an erosion case, it is a **fabrication** case. The
falsified line item was *assets* (RM3.5B of contracts whose existence KPMG could
not confirm; later a disclaimer of opinion and a restatement). Inflating assets
inflates `ln(A/L)`, so the barrier looks *further away* than it is. A model whose
numerator is the thing being falsified cannot see a falsification.

This is the same lesson as the NI-vs-OCF divergence: **profit is a claim, cash
is a receipt.** Serba reported RM392.8M profit in FY2018 and generated RM83.2M
of operating cash — **RM0.21 of cash per RM1 of reported profit**. FY2019:
RM0.44. A genuine business converts close to or above RM1.

### The detector that DID fire

**Cash ÷ total borrowings**, monotone every single year:
`0.445 → 0.391 → 0.126 → 0.016 → 0.010`. No jump, no restatement needed, visible
from FY2019 onward. The company ran out of ability to service its own debt while
still reporting profits.

### Malaysian control — PETRONAS Chemicals (Bursa 5183)

| FY | Assets (RM m) | Liab (RM m) | D | cash/borrow | OCF/PAT | T |
|---|---|---|---|---|---|---|
| 2021 | 46,454 | 11,068 | 1.434 | 4.257 | 1.49 | — |
| 2022 | 55,430 | 15,697 | 1.262 | 1.962 | 1.51 | 7.3 y |
| 2023 | 60,206 | 18,132 | 1.200 | 1.806 | 3.76 | 19.5 y |
| 2024 | 59,591 | 19,612 | 1.111 | 1.870 | 2.68 | 12.5 y |
| 2025 | 57,690 | 20,310 | **1.044** | 1.766 | 2.80 | **15.5 y** |

**Honest reading:** PCHEM's distance has closed **four years running**
(1.434 → 1.044). T ≈ 15.5 years — not danger, but not stable either. Crucially
its *cash* signal is healthy and flat (1.77–4.26 coverage; OCF/PAT 1.5–2.8). A
company can erode slowly and still be sound; the erosion only matters when the
cash stops arriving.

### The generalisation — two failure modes, two detectors

| Failure mode | Mechanism | Detector | Catches | Misses |
|---|---|---|---|---|
| **EROSION** | distance closes steadily over years | **APEX T** | Sears (T=1.2, 5y early) | Whiting, JCPenney (shock) |
| **FABRICATION** | distance looks fine, cash never arrives | **OCF/PAT + cash/borrowings** | Serba (0.21, 0.44) | — |

**Neither alone is sufficient. Both together are.**
This is why the T-score must never be published without the cash-conversion pair
beside it — a company can be walking toward the barrier while reporting profit,
and the profit line is the one being watched.

---

## ADDENDUM 2 — GOVERNANCE LAYER: λ is not exogenous (2026-09-18, same session)

**F13 raising:** *"You are missing the apex governance — the singular governance capture."*

**Correct — and the omission was structural, not cosmetic.** The model treated
`λ` (trust-decay rate) as an exogenous observable. It is not. Governance structure
**sets a floor** on λ, because a firm whose overseer is appointed by the party it
oversees cannot self-correct. Correction must then arrive from outside, and outside
is slow.

```
T = ln(V / B) / (λ − μ)
λ = λ_market + λ_governance
```

`λ_governance ≥ 0` **by structure, not by intent.** No individual need be acting in
bad faith for the floor to bind.

### Board composition — PETRONAS, as published (retrieved 2026-09-18)

Source: `petronas.com/about-us/our-leaders`. 8 directors.

| Director | Role | Classification |
|---|---|---|
| Tan Sri Mohd Bakke Salleh | Chairman | Independent NED |
| YM Tan Sri Tengku M. Taufik | President & Group CEO | **Executive** |
| Azizan Zakaria | Chair, Audit; Chair, Risk; Member, N&R | Independent NED |
| Tan Sri Zaharah Ibrahim | Chair, N&R; Member, Audit & Risk | Independent NED |
| Datuk Dr Shahrazat Hj Ahmad | Member, Audit + Risk + N&R | **Non-Independent** NED |
| Dato' Seri Abdul Rasheed Ghaffour | — | Independent NED |
| Mohd Jukris Abdul Wahab | COO; EVP & CEO Upstream | **Executive** (from 1 Feb 2026) |
| Liza Mustapha | EVP & Group CFO | **Executive** |

**Headcount:** 4/8 independent (50%) · 1/8 non-independent · 3/8 executive (37.5%).
50% independence is **not** a captured board by count. The finding is elsewhere.

### The finding — oversight concentration

**One director chairs BOTH the Audit Committee AND the Risk Committee, and sits on
the Nomination & Remuneration Committee.** A second director sits on all three
committees as a **non-independent** member.

That means: the same seat holds audit oversight, risk oversight, and input into the
CEO's remuneration and succession. The MCCG recommends separating committee chair
roles. Here three converge.

### The appointment mechanism

The **Prime Minister's Office appoints the chairman** (documented: PMO/Reuters
announcement of the Bakke Salleh appointment, 12 July 2021). The chain is therefore
`PMO → Chairman → Board → Management`, with the control loop running
`Management → PMO` **absent**.

This is Acemoglu's **extractive institution** in a single legal entity: not corrupt
persons, wrong incentive architecture. The overseer's incentives align with the
appointing party, not the firm.

### Two corrections to the F13 raising (facts, checked)

1. **Bakke Salleh and 1MDB.** He was 1MDB chairman in 2009 — and **resigned twice,
   citing dissatisfaction with the company's management** (FMT, 12 Jul 2021). The
   record shows him as a person who *exited* on governance grounds. That is the
   opposite of the inference drawn, and the direction matters.
2. **Jukris.** He was appointed **COO effective 1 February 2026**, concurrently
   **Executive Director**; he had been EVP & CEO Upstream from 1 July 2024. He did
   not "join the board" as an outside appointment — he was promoted into it from
   inside, which *raises* executive density (3 of 8 seats) rather than adding
   independence.

### What is NOT claimed

- No allegation of corruption, collusion, or criminal conduct against any named person.
- "Clique" and similar framings are **not** evidenced and are not used here.
- This is a **structural** finding about incentive architecture. It names how the
  architecture is arranged, and it can be checked by anyone reading the company's
  own published board page.

### Status

**NOT backtested.** Board-composition data for the 13 failed firms is not in hand,
so the governance term cannot yet be run against the validation panel. Labelled as
**formulation**, exactly as the fiscal barrier in the NOC addendum. To test it, the
next step is board-independence and committee-concentration data for the same 13
firms at t−3, which is obtainable from their proxy statements.

---

## What This Is Not

- Not a forecast. It does not say *"X collapses in March 2029."*
- Not a signal to sell everything on. Sens = 28.6%.
- Not validated against actual bankruptcies (survivorship).
- Not a substitute for the balance sheet.

**It is an arithmetic fact about distance and rate.** What the user does with it is F13.

---

## SO WHAT

The session's question was *"will it go up or down"* — demonstrated twice to be unanswerable (8-chart blind test tied with a null baseline; 7,858-observation death-cross test caught 7.8% of collapses).

The answerable question is: **how much time do I have, and what am I paid for it.**

That is `T`, and it is arithmetic — and it **changes when you change the entry price.** Which is why the same asset with two different start dates produced opposite winners (gold 15.8× vs 2.7×; S&P 5.0× vs 6.7×).

**DITEMPA BUKAN DIBERI ⚒️**
