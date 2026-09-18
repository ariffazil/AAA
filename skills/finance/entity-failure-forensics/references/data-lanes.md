# Data lanes for solvency and failure analysis

Routing rules first, endpoints second. Pick the lane from the entity class, not from
convenience.

## Routing table

| Entity class | Lane | Why |
|---|---|---|
| Live listed company | price lane (yfinance etc.) | fast, daily granularity, market-implied |
| **Delisted / bankrupt / renamed** | **filed financial statements** | the only lane that carries the dead |
| Private company | filed statements if available; otherwise internal accounts | no market data by definition |
| State-owned enterprise / NOC | filed statements + **fiscal transfer data** | contractual barrier is not the binding one |
| An individual's own position | their own statements + position size | the binding barrier is personal, not corporate |

**Rule: for a dead entity, do not spend time hunting price history. Go to filings.**
Price lanes are built for live tickers. Filed balance sheets also give a *contractual*
barrier (liabilities) instead of a price proxy — strictly better for the same work.

## Lane 1 — EDGAR XBRL company facts (US filers, filings from ~2009)

```
https://data.sec.gov/api/xbrl/companyfacts/CIK##########.json
```

- Requires a descriptive `User-Agent` header identifying you and a contact.
- Zero-pad the CIK to 10 digits.
- Rate-limit to well under 10 requests/second; sleep ~0.3s between calls and cache
  every response to disk. The payloads are large (several MB) and re-fetching them
  is the slowest part of the pipeline.
- Returns `entityName`, `tickers`, and `facts.us-gaap.<Tag>.units.USD[]` where each
  row carries `form`, `fp`, `fy`, `val`, `end`.
- Pull only annual periods: `form == "10-K"` and `fp == "FY"`. When several filings
  report the same `fy`, keep the one with the latest `end` — later filings restate.
- Useful tags, with fallbacks (the tag varies by filer and era):

| Concept | Primary tag | Fallbacks |
|---|---|---|
| Assets | `Assets` | — |
| Liabilities | `Liabilities` | — |
| Equity | `StockholdersEquity` | `StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest` |
| Revenue | `Revenues` | `RevenueFromContractWithCustomerExcludingAssessedTax`, `RevenueFromContractWithCustomerIncludingAssessedTax`, `SalesRevenueNet` |
| Net income | `NetIncomeLoss` | `ProfitLoss` |
| Operating cash flow | `NetCashProvidedByUsedInOperatingActivities` | `NetCashProvidedByUsedInOperatingActivitiesContinuingOperations` |

- Acceptance test for a pulled series: it must return a plausible number of annual
  periods for the entity's life. A filer that returns zero to three years either
  delisted before the XBRL era or the identifier is wrong — check the name.

## The identity trap (this is the one that bites)

**Filing identifiers are reassigned after a filer dies.** A record that resolves
cleanly can belong to an entirely unrelated live company. Verified examples: a defunct
home-goods retailer's identifier now resolves to a name unrelated to retail; a defunct
luxury department store's now resolves to a technology company.

Mitigation, in order:

1. Read `entityName` for **every** record before using any number from it.
2. Match it against the expected filer name. Reject on mismatch — do not reason about
   how likely the mismatch is.
3. Where the entity was renamed or restructured (common after bankruptcy), allow the
   successor name but record it explicitly, so a later reader can audit the join.
4. Report how many identifiers were rejected. In the origin panel, 16 of ~25 candidate
   dead firms were rejected. That rejection count is itself evidence the gate ran.

Look up identifiers by company name through the company-search endpoint rather than
guessing, and expect the search to return several historical entities per name
(pre-merger, post-merger, successor shell) — pick by era, then confirm by name.

## Lane 2 — price data (live tickers)

- Monthly adjusted closes are enough for annual-horizon work and much cheaper than daily.
- For an NOC or private entity there is no ticker at all; skip this lane entirely.
- When a ticker has been renamed, a single symbol will return nothing while the
  successor symbol works. Probe both, and probe the suffix convention for the exchange.
- Commodity and index proxies are available under their own symbols and are useful as
  reference legs (e.g. a commodity continuous contract against an equity index) to
  show that the same asset with two different entry dates produces two opposite
  "winners". That comparison is about the **price paid**, not the asset.

## Lane 3 — regulator / company investor-relations pages

For non-US filers and for narrative facts (who held which role, when a scheme was
approved, what the company itself reported), the issuer's own IR pages and the
business press are primary. Prefer the issuer's own reported figures when available —
it removes the argument that the analyst misread the accounts, because the numbers
are the company's own.

Watch for **period-length changes**: a company that moves its financial year end will
report one column covering 15 or 18 months. That column is not comparable to a
12-month column and must be labelled as such everywhere it appears. A change of
financial year end is itself a governance signal worth noting.

## Lane 4 — governance data

Board composition, committee membership, and independence classification are on the
company's own published board page. This is free, checkable by anyone, and is the
right source for a structural governance observation. Capture: independence ratio,
who chairs each committee, whether one seat holds several oversight roles, and **who
appoints the chair** (the appointment mechanism is the load-bearing fact, not the
composition).

## Probing discipline

Before declaring a lane empty: probe several symbol conventions, both asset classes,
and more than one source. Record what the sweep tested, so the next reader knows the
absence was measured rather than assumed. An absence that was measured is a finding;
an absence that was assumed is a gap.
