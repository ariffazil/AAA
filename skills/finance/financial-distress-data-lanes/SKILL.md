---
name: financial-distress-data-lanes
description: Use when pulling company distress data from filings.
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# Financial Distress Data Lanes

Where the numbers for a failed or failing company actually live, and the traps
that produce confident wrong answers.

## Lane map — pick by what you need, not by convenience

| Need | Live tickers | Delisted / bankrupt |
|---|---|---|
| Price history | yfinance, Yahoo chart API | **none free** — probed yfinance, stooq, Yahoo chart API direct; all empty |
| Balance sheet + cash flow | SEC EDGAR XBRL `companyfacts` | SEC EDGAR XBRL (filings survive the filer) |
| Foreign / Bursa | issuer's own IR page, stockanalysis.com, klsescreener | issuer IR page if still hosted |

**Consequence:** a backtest built on free price data is *survivors only*. Say so,
and build a separate fundamental validation set for the dead.

## Rule 1 — Verify the entity before using a CIK

**A SEC CIK is reused after a filer dies.** CIK 0001130713 was Bed Bath & Beyond;
it now serves "Neighborhood Intelligence, Inc." CIK 0001376321 was Neiman Marcus;
it now serves "ZW Data Action Technologies".

A dead company's CIK still returns data — belonging to somebody else. Always read
`entityName` from the payload and require a distinctive token match before using
any number from it. In one 37-name sweep, 16 were rejected this way.

## Rule 2 — Match on a distinctive token, not the brand

A filer can be renamed in reorganisation. JCPenney's post-reorg filing entity is
"OLD COPPER COMPANY, INC." Match on a stable token (`COPPER`, `RADIOSHACK`), never
on the consumer brand or the current ticker.

## Rule 3 — Never interpolate a gap to make a line continuous

If a fiscal year has no sourced figure, leave the gap and label it. Interpolating a
balance sheet to smooth a chart is fabrication with extra steps. Plot only
contiguous runs of finite values.

## Rule 4 — Two detectors, because there are two ways a firm dies

| Mode | Mechanism | Detector | Blind to |
|---|---|---|---|
| EROSION | distance closes over years | distance-to-barrier `T = ln(V/B) / (lambda - mu)` | shocks (commodity collapse, litigation) |
| FABRICATION | books look fine, cash never lands | `OCF / net income`, `cash / total borrowings` | — |

**A distance-to-barrier model cannot see a falsification of its own numerator.**
When assets are the inflated line item (Serba Dinamik: RM3.5B of unconfirmable
contracts; Enron), inflating assets *widens* the apparent distance. The model read
`T = infinity` in exactly the year the auditor raised issues.

**The monotone cash tell is stronger than any ratio level:** cash / borrowings
falling every single year with no jump needs no restatement and no forensic skill.
Serba: `0.445 -> 0.391 -> 0.126 -> 0.016 -> 0.010`. Compare with a healthy control
(PCHEM: 1.77-4.26, flat).

**Report OCF/PAT, not just profit.** Below ~0.5 means reported profit is not
cash-backed. Real businesses convert at or above 1.0.

## Rule 5 — Separation needs a control set and a base rate

Build the survivor control from the same era and sector, run the identical formula,
and report lift. A raw hit rate is uninterpretable: "32.6% of these collapsed" means
nothing until you know the base rate was 4.5% (lift 5.5x).

Always report sensitivity, specificity and PPV together. High specificity alone is
free — predicting "nothing fails" also scores high.

## Rule 6 — Check the unit scale before believing a finding

Sources mix RM'000, RM million, RM billion and USD. A silent 1000x error reads as a
catastrophic discovery. Normalise to one unit at ingest and assert the range of every
series before plotting.

## Rule 7 — Two barriers when the owner is a state, not a shareholder

A contractual barrier answers "can it default". For a state-owned entity that is not
the live question — a sovereign cannot be exited, it can only be paid.

- Shareholder who is unhappy: **sells** — loss transfers, capital stays in the firm.
- State owner who is unhappy: **takes** — capital leaves, investment capacity falls.

Model the fiscal barrier instead: `headroom = operating cash flow - dividend - capex`.
PETRONAS goes from +RM34.4B headroom at Brent $100 to +RM0.8B at $67 and negative
below it — while the dividend is still paid in full. Label this **unvalidated**: no
comparable panel of state-owned entities discloses the fiscal term.

## Rule 8 — Distinguish a solvency failure from an authority transfer

A third mode defeats both detectors: the asset changes hands legitimately. No
default, no falsification, no number moves. When two parties can invoice for the
same thing (PETRONAS vs Petros vs Shell MDS), the arithmetic stays valid and stops
meaning anything. Detect it by reading contracts and jurisdiction, not ledgers.

## Rule 9 — Separate the firm's survival from the shareholder's

A distance-to-barrier score measures **the firm**. It says nothing about the person holding the
share, and the two diverge completely: the company keeps trading while its equity holders are wiped
out. State the model's scope in the artifact — *this scores the firm, not you* — or the reader hears
a survival verdict about their own position.

Two mechanisms do the damage, and both are invisible on a price chart drawn from adjusted history:

- **Share-count change.** A consolidation or capital reduction rescales the price axis, so history
  across the event is not comparable. A 20-to-1 consolidation turns a documented RM4.96 peak into
  ~RM99 on a chart — both correct, describing different share counts. Before comparing prices across
years, find the consolidation ratio and the capital-reduction event and state which share basis each
  number sits on.
- **Dilution.** Market capitalisation and price per share fall by *different* amounts, and the gap is
  the dilution. A firm down ~97% by market cap whose share price is down ~99.7% got there by issuing:
  rights issues, debt-to-equity conversions and rescue placements move the seat from the original
  holder to the creditor. **Report both percentages side by side — the gap is the finding**, and it is
  the part a reader still holding the old shares actually feels.

A state rescue sharpens this rather than softening it: the rescuer becomes the substantial
shareholder and the original holder is diluted toward zero while the firm survives as a going concern.

## Reporting

- Lead with the mechanism, then the number. One governing sentence per section.
- Draw it. Multi-panel figures beat prose for anyone who says they are weak at maths.
- Keep a defect log and state it in the artifact: model bug (and how it was found),
  survivorship, proxy choices, untested formulations. A result that came out clean on
  the first run is suspect — infinities clustered non-randomly in one category are a
  bug signature, not a finding.
- Every figure carries its sources and the retrieval date.
