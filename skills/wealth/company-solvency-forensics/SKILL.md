---
name: company-solvency-forensics
description: Use when judging if a company can survive or will collapse.
version: 1.0.0
tags: [solvency, distress, bankruptcy, sec-edgar, xbrl, cash-conversion, forensics]
---

# Company Solvency Forensics

**Trigger:** "will this company die", "can it survive N years", "is it safe to hold", "did anything warn us before it collapsed", "is this stock cheap or is it a trap". Any listed company, any private company with filed accounts, any historical collapse.

**Scope:** how much runway a company has before its liabilities consume it, and *which* failure mode it faces. This is not price prediction, and a price chart is not the instrument for it.

## The one idea

A company dies in one of two ways, and they need different detectors. Using only one produces a model that looks like it works until the first fraud.

| Mode | Mechanism | Detector |
|---|---|---|
| **EROSION** | distance between assets and liabilities closes steadily over years | distance-to-barrier (T) |
| **FABRICATION** | the books look fine while cash never arrives | cash conversion + cash coverage |

**A distance-to-barrier model is structurally blind to fabrication.** Its numerator is *assets* — the line item most commonly inflated. Inflating assets pushes the computed barrier *further away*, so the model reads **safer** on precisely the companies that are most dangerous. A model whose numerator is the thing being falsified cannot see a falsification.

## Always-on rules

1. **Never publish a distance-to-barrier number without the cash pair beside it** — operating cash flow ÷ net income, and cash ÷ total borrowings. Both, every period.
2. **Cash conversion: OCF ÷ net income.** Genuine businesses convert at or above 1.0. Persistent values under ~0.5 mean reported profit is not arriving as money. The *trend* matters more than any single year.
3. **Cash ÷ total borrowings is the coarsest robust test**, and the hardest to disguise — a monotone decline needs no restatement to be visible, and it cannot be fixed by relabelling.
4. **State which barrier you used.** Total liabilities is a *contractual* threshold. A price level (e.g. −80% from the running max) is a proxy — label it as one, and prefer the real threshold whenever filed statements exist.
5. **Report every miss with its mechanism.** A model that shows only its hits is not evidence. Separate "erosion" misses from "shock" misses: a balanced company killed by a commodity crash will not be caught by any distance model, and presenting it as a model failure mis-teaches the reader.
6. **Validate on outcomes, not on outcomes you can still observe.** A screener calibrated only on surviving tickers is calibrated on the easy population.
7. **Defined ≠ predicted.** The output is an arithmetic fact about distance and rate. Do not let it be read as a date.

## Procedure

### Step 1 — acquire the statements (probe every lane before declaring one absent)

1. **The issuer's own investor-relations / annual-report page** — preferred. These are the figures the company itself reported, and IR "Financial Highlights" / "Ratio Analysis" pages often carry *total borrowings* and *net operating cash flow* that aggregators omit. Both are required for the two detectors.
2. **SEC EDGAR XBRL companyfacts** — the only lane that still serves companies that no longer exist as tickers. Recipe: `references/edgar-xbrl-lane.md`.
3. **Aggregators** for live names — useful for cross-checking balance-sheet totals; label the provenance.

**Price history for delisted tickers is generally unavailable on free lanes.** Spend the budget on fundamentals instead — they are the better instrument for this question anyway, and losing them is the real risk (see the survivorship pitfall).

### Step 2 — compute the table

Run `scripts/solvency_table.py` on a CSV of filed figures. It emits, per period:

```
D       = ln(assets / (assets - equity))      distance to the debt barrier
lambda  = -(dD/dt) over a 3-period window     rate the barrier is closing
T       = D / lambda / (1 + burn)             years to the barrier
          burn = min(|ocf|/assets, 0.6) when ocf < 0
          T = inf when lambda <= 0 (the gap is not closing)
OCF/PAT, cash/borrowings, gearing
```

Same functional form as any depth ÷ rate problem: how far, and how fast you are closing it.

**Calibration to expect** (from bankruptcy-tested panels): failing companies sit at a median T near 1 year; profitable survivors near 10. At the threshold T < 1 year, roughly 45% of failing-company observations fall below it versus ~7% of surviving ones — a 6–7× separation. Treat it as a **triage instrument, not an oracle**: at the tightest threshold two out of three flagged names do *not* fail.

### Step 3 — read the two detectors together

- **T falling, cash healthy** → slow erosion, company still sound. Erosion only becomes binding when cash stops arriving.
- **T stable or rising, cash deteriorating** → the fabrication signature. The distance is not real.
- **Both deteriorating** → the ordinary pre-collapse profile.
- **T = inf while cash collapses** → the model has gone blind on you. Do not report the infinity as safety; report the blindness and the cash trend.

### Step 4 — report

Lead with the two numbers, not the model. Name the failure mode you believe you are looking at. List the cases the model missed and why. State the barrier used and its provenance.

## Testing a claimed predictor (blind protocol)

When someone — including you — claims an indicator predicts collapse, run this rather than arguing:

1. **Cut the series at a point.** Show only the left half. Hide the outcome.
2. **Commit the prediction in writing before revealing.** No edits after.
3. **Always include a null baseline**: score the trivial always-one-class strategy on the same items.
4. **Report skill as the difference from the baseline**, not as the raw hit rate. A raw score that ties the baseline is zero skill.
5. **Choose cases where the visible half and the hidden half disagree**, so the test can actually discriminate. If every visible half looks alike, the test measures nothing.
6. **Keep the set balanced.** With a small odd number of binary calls a guesser scores well by chance.

A worked instance of this ended at 6/8 correct — exactly what the always-one-class baseline scored on the same items. When a test like that ties, the honest output is "this identifies nothing", and the useful follow-up is asking what *else* the tool can legitimately do (as a tripwire, not a verdict).

## Pitfalls

- **CIKs are reused after a filer dies.** A dead company's CIK keeps serving data belonging to whoever holds it now, so raw numbers can look entirely plausible for the wrong entity. Read `entityName` from the same response and reject any CIK that does not match the expected filer. In one acquisition pass, roughly half the candidate CIKs were rejected on this test. Recipe and the matching rule: `references/edgar-xbrl-lane.md`.
- **An infinity that is not randomly distributed is a bug signature, not a finding.** When a derived score returns unbounded values for an entire category, suspect the formula before reporting that category as structurally safe. A sign-inverted decay term in this class of model silently assigned "infinite runway" to half a panel — and the quadrant it dropped was the one the author expected to be the most dangerous.
- **A clean result from the first run of a derived formula is suspicious.** Check the value distribution *by category* before interpreting any of it.
- **Survivorship bias: name it and its direction.** Aggregator panels contain only companies that still trade. Say whether the bias makes the measured signal look stronger or weaker, and validate separately on filed statements of known failures.
- **Pre-XBRL failures have no XBRL facts.** Bankruptcy-era filers from before the XBRL mandate return nothing from the companyfacts API. Use the filings themselves or the issuer's archived reports — and do not conclude the company never filed.
- **A reorganized company files under a new name.** Post-Chapter-11 entities appear as successor shells whose name may bear no relation to the brand. Match on a distinctive word from the original, not on equality.
- **Do not compute net profit from revenue and a cost guess.** Net profit is a filed figure; revenue-minus-estimated-cost is a different quantity and will be corrected by anyone with an accounting background.

## Related

- Canonical derivation, backtests and defect log: `/root/AAA/canon/APEX-T-SCORE-DERIVATION-2026-09-18.md` — **load it instead of re-deriving**, and note it is `DRAFT_AWAITING_F13` with two declared defects.
- SEC XBRL lane recipe: `references/edgar-xbrl-lane.md`
- Solvency table calculator: `scripts/solvency_table.py`
- Long HTML→PDF delivery of these findings: `paged-media-report-layout`
