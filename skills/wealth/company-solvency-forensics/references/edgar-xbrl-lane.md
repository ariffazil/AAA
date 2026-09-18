# SEC EDGAR XBRL — the lane that still carries dead companies

## Why this lane exists

Price history for delisted tickers is generally unavailable on free market-data lanes — the ticker stops resolving and the series goes with it. Filed statements behave differently: a company that filed Chapter 11 has accounts, and those accounts are still served. For solvency work this is the **only** lane that can validate against companies that actually died, which is the difference between a calibrated instrument and a plausible one.

## Endpoint

```
https://data.sec.gov/api/xbrl/companyfacts/CIK##########.json
```

- Ten-digit zero-padded CIK. A nine-digit CIK returns 404.
- Send a `User-Agent` identifying the tool and a contact address — SEC fair-use policy.
- Keep the request rate under ~10/s. Sequential calls with a short sleep are sufficient for a few dozen filers.
- **Cache every response to disk keyed by CIK.** Re-runs then cost nothing, and the cache becomes the evidence artifact you can point at later.

## The mandatory entity check

**CIKs are reused after a filer dies.** The same identifier keeps serving data for whoever holds it now, and the numbers can look entirely plausible for the wrong company — right shape, right magnitude, wrong entity.

Observed reuse: a large home-goods retailer's CIK now serves an unrelated data company; a luxury department store's CIK now serves an Asian data-action firm; a snack-food baker's CIK now serves a biotech.

So: **read `entityName` from the same response and reject the CIK when it does not match the expected filer.** A substring match on one distinctive word from the original name is the right test, not equality — post-Chapter-11 entities file under successor names that may bear no relation to the brand (a reorganized department-store chain files as `OLD COPPER COMPANY, INC.`).

In one pass over ~30 candidate filers, roughly half were rejected on this test. Treat the rejection rate as normal, not as a sign the lane failed.

## Mapping a name to a CIK

```
https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&company=<urlencoded name>
    &type=10-K&dateb=&owner=include&count=10&output=atom
```

Parse `<cik>` and `<conformed-name>` from the Atom response. Apply the entity check above before fetching facts.

## Extracting a series

Structure: `facts` → `us-gaap` → `<tag>` → `units` → `USD` → rows.

Row filter for annual figures: `form == "10-K"` and `fp == "FY"`. When several rows share a fiscal year (`fy`), keep the one with the latest `end` — later filings restate earlier ones, and you want the restated value.

### Tag alternatives (take the first present, or the one with the most years)

| Concept | Tags to try in order |
|---|---|
| assets | `Assets` |
| liabilities | `Liabilities` |
| equity | `StockholdersEquity`, `StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest` |
| revenue | `Revenues`, `RevenueFromContractWithCustomerExcludingAssessedTax`, `RevenueFromContractWithCustomerIncludingAssessedTax`, `SalesRevenueNet` |
| net income | `NetIncomeLoss`, `ProfitLoss` |
| operating cash flow | `NetCashProvidedByUsedInOperatingActivities`, `NetCashProvidedByUsedInOperatingActivitiesContinuingOperations` |

Tag coverage is uneven: **balance-sheet items are reliable while income-statement and cash-flow items are thinner.** If a series comes back empty, iterate the alternatives before concluding the filer never reported it.

## Failure modes

- **404** — the CIK does not exist or the filer pre-dates the XBRL mandate. Final; do not retry.
- **503 / 504 / read timeout** — transient on this endpoint under load. Retry two or three times with backoff before giving up. A single timeout is not evidence the data is absent.
- **No XBRL facts for pre-mandate failures.** Collapses from the early 2000s and earlier return nothing here even when the CIK is correct. Retrieve those from the filings themselves or the issuer's own archived reports.

## Sanity checks before using the numbers

1. Entity name matches the expected filer.
2. Assets exceed liabilities for at least part of the history (a series where this is inverted everywhere usually means the wrong entity).
3. The fiscal years bracket the event you are studying — a failure in year *X* needs observations from before *X*, not after.
4. Liabilities reconstructed as `assets − equity` tie to the reported `Liabilities` where both exist; a large unexplained gap means a non-controlling-interest line is in play.

## Non-US / non-SEC companies

No equivalent open machine-readable lane was found. Use the issuer's own investor-relations pages — their "Financial Highlights" and "Ratio Analysis" pages typically carry **total borrowings** and **net operating cash flow**, exactly the pair the two-detector method needs and which aggregators routinely omit. Record the retrieval date and the issuer as provenance: these are figures the company reported about itself, a different evidence class from audited statements, and they should be labelled as such.
