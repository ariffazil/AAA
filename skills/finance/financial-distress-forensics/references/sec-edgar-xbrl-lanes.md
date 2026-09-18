# Filing-data lanes — pulling balance sheets, including for companies that died

Free price APIs drop delisted tickers, so a panel built from price history contains only
survivors. Corporate registries do not drop anyone. **For any question about failure, go to the
filings first.**

## Primary lane — structured financial data from filings (US registrants)

```
https://data.sec.gov/api/xbrl/companyfacts/CIK{10-digit-padded}.json
```

- A descriptive `User-Agent` header is **required**; requests without one are refused.
- Keep well under 10 requests/second (add a sleep between calls).
- Response shape: `facts.us-gaap.<Tag>.units.USD[]`, each entry carrying
  `form`, `fp`, `fy`, `val`, `end`.
- Cache each response to disk before parsing; these are large and re-fetching wastes the
  rate-limit budget.

### Annual-only extraction

Filter to `form == "10-K"` **and** `fp == "FY"`, then keep the latest-`end` value per `fy` — a
single fiscal year appears many times across subsequent filings as comparatives.

### Tag fallbacks are mandatory, not optional

Tag names drift across filers and years. Try in order and take the first that yields data:

| Concept | Tag candidates |
|---|---|
| Assets | `Assets` |
| Liabilities | `Liabilities` |
| Equity | `StockholdersEquity`, `StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest` |
| Revenue | `Revenues`, `RevenueFromContractWithCustomerExcludingAssessedTax`, `RevenueFromContractWithCustomerIncludingAssessedTax`, `SalesRevenueNet` |
| Net income | `NetIncomeLoss`, `ProfitLoss` |
| Operating cash flow | `NetCashProvidedByUsedInOperatingActivities`, `NetCashProvidedByUsedInOperatingActivitiesContinuingOperations` |

## Registrant-identifier lookup

```
https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&company={urlencoded-name}
    &type=10-K&dateb=&owner=include&count=10&output=atom
```

Parse `<cik>` and `<conformed-name>` pairs from the atom feed. Common names return several
candidates; keep all and disambiguate by entity verification below. Expect intermittent
upstream 500/503 — retry once, then fall back to a different candidate.

## THE TRAP — identifiers are reused after a filer dies

A defunct registrant's identifier is reassigned to an unrelated new company. Its endpoint still
serves data — belonging to somebody else. Observed: a bankrupt retailer's ID later returning a
small private company; a failed luxury retailer's ID returning an unrelated technology firm;
several pre-2010 failures moved to successor registrants or requiring the successor entity's
identifier entirely.

**Therefore:**

1. Read `entityName` from every fetched response.
2. Require it to match the expected filer before a single figure is used.
3. Log rejections with the actual entity name found — a rejection is a finding, and the count
   belongs in the write-up.
4. Some older failures return 404 on their own identifier and must be sourced from the successor
   or reorganisation entity, or omitted. Omit openly rather than substituting a near-match.

## Coverage notes

- Structured filing data starts around 2009. Pre-2009 failures largely have no XBRL and must come
  from published summaries, press archives, or the issuer's own investor-relations pages.
- Fiscal-year ends are not calendar years, and mid-period changes produce stubs (e.g. an
  eighteen-month column). Label the period convention before presenting any table.
- Post-reorganisation figures may describe the *successor* entity. Check the restructuring date
  against the fiscal years being used and drop anything that straddles it.

## Non-US issuers (e.g. Bursa Malaysia)

Not on this registry. Route:

1. **The issuer's own investor-relations pages** — best single source for headline financials,
   because the figures are theirs and the periods are stated. Look for a financial-highlights or
   ratio-analysis page; these often carry assets, liabilities, equity, borrowings, cash and
   operating cash flow in one table.
2. **The exchange's news archive** and the financial press's long-form "timeline of events"
   pieces — these frequently quote total liabilities and net profit year by year, which is
   enough to build the series even when the full statement is not machine-readable.
3. **Aggregator summary pages** for a surviving listed company. Expect bot-protection on some;
   try a different aggregator rather than repeatedly retrying one.

Cross-check at least two of these before publishing a series.

## Sanity checks before trusting a series

- Liabilities ÷ assets should land in (0, ~1.5). Far outside that means the wrong entity or a
  mismatched tag.
- Equity should be roughly assets − liabilities. A large unexplained gap means a tag fell back to
  a different concept.
- Compare a derived figure against any directly-reported one (e.g. net debt ÷ gearing gives
  equity) and mark derived values as derived in the artifact notes.
