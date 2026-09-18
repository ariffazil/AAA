# Data sources for distress analysis

## SEC EDGAR — the lane that carries the dead

Best first lane for any US filer, alive or dead, because it serves the filed statement rather than
a price series. It therefore contains companies that no longer have a ticker.

### Company facts (full XBRL history in one call)

```
https://data.sec.gov/api/xbrl/companyfacts/CIK##########.json
```

- Requires a `User-Agent` header identifying the requester. Requests without one are refused.
- Stay under roughly ten requests per second. Space calls and cache each response to disk; the
  payloads are large and re-fetching wastes the budget.
- Returns `entityName` at the top level. **Read it.** Also returns
  `facts.us-gaap.<Tag>.units.USD[]`, where each row carries `form`, `fp`, `fy`, `val`, `end`.

### Entity / CIK lookup

```
https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&company=<name>&type=10-K&owner=include&count=10&output=atom
```

Returns `<cik>` and `<conformed-name>` pairs. A search often returns several candidates; take the
one whose conformed name matches, and keep the alternates only as fallbacks.

### The identifier-reuse trap

An identifier keeps serving data after its filer dies — belonging to whoever holds it now.
Observed substitutions include a bankrupt retailer's identifier answering for an unrelated
technology company, and a liquidated department store's identifier answering for a completely
different issuer.

Consequence: **the entity name is a required field, not a nicety.** In one 37-entity acquisition,
16 records were rejected purely on name mismatch. A pipeline without this check silently analyses
whichever company now owns the identifier.

Guard pattern:

```python
nm = data.get("entityName", "")
if EXPECTED_TOKEN not in nm.upper():
    reject_and_record(label, cik, nm)   # do not fall through to the numbers
```

Also expect that some dead filers have no XBRL at all (pre-XBRL era, or a foreign private issuer).
Those return 404. Report them as unavailable rather than as zero.

### Tag selection

Tag names drift across issuers and years. For each concept, try a list of alternatives and keep the
one with the most years populated.

| Concept | Primary tag | Fallbacks |
|---|---|---|
| Assets | `Assets` | — |
| Liabilities | `Liabilities` | — |
| Equity | `StockholdersEquity` | `StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest` |
| Revenue | `Revenues` | `RevenueFromContractWithCustomerExcludingAssessedTax`, `RevenueFromContractWithCustomerIncludingAssessedTax`, `SalesRevenueNet` |
| Profit | `NetIncomeLoss` | `ProfitLoss` |
| Operating cash | `NetCashProvidedByUsedInOperatingActivities` | `NetCashProvidedByUsedInOperatingActivitiesContinuingOperations` |

Filter to `form == "10-K"` and `fp == "FY"`. For a given fiscal year, keep the row with the latest
`end` date — restatements mean several rows share an `fy`.

## Price-series lanes — what they do and do not carry

- Free price APIs generally serve actively listed tickers only. Delisted tickers commonly return
  empty, and a renamed or relisted entity appears under a different symbol with no history.
- Public quote-reconstruction endpoints are unreliable for survivorship-free panels.
- Consequence for any backtest: a panel assembled from free price data **excludes the dead**. That
  is survivorship bias built into the source, not into the code. State it as a limit and, where
  possible, validate separately against filed statements.

Practical rule: for anything about failure, prefer the filed-statement lane. It reaches the dead,
and its barrier is contractual rather than a price proxy.

## First-party sources for Malaysian listed firms

- The issuer's own investor-relations site carries the reported figures and is the strongest
  first-party source for a Malaysian listed company — annual highlights and ratio-analysis pages
  typically present assets, equity, borrowings, cash, revenue, profit and operating cash flow
  across several years in one table.
- Malaysian fiscal years are frequently not calendar years, and issuers do change year-ends. Check
  for a changed period before comparing two adjacent columns; an eighteen-month or three-month
  column will otherwise read as a collapse or a spike.
- For a delisted Malaysian ticker, the renaming or rebranding that follows a restructuring means
  the old symbol will not resolve. Search the issuer name and cross-check the stock code rather
  than the ticker string.

## State-owned and private entities

- State-owned enterprises publish audited group financial reports, but not on a schedule or in a
  schema comparable to a listed filer. Total assets, total liabilities and shareholders' equity are
  usually retrievable; fiscal commitments are usually narrated in the chairman's statement rather
  than tabulated.
- Board composition, committee membership and independence classifications are published on the
  entity's own leadership page for most large state entities. That page is the citable source for
  governance structure, and it is checkable by anyone.
- Where an entity has no ticker there is no price-based early warning at all. Reporting frequency is
  the only lever that shortens the lag; adding model complexity does not.
