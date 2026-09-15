# filings-mcp

FastMCP server giving an AI agent structured access to **Malaysian + US financial/regulatory filings**.
Read-only external retrieval: it fetches, hashes, caches and returns JSON. It never judges, never
mutates federation state, never writes VAULT999.

- **Path:** `/root/AAA/mcp/filings/`
- **Transport:** streamable HTTP, `127.0.0.1:18410/mcp` (loopback only)
- **Interpreter (mandated):** `/opt/arifos/venv/bin/python` — fastmcp 3.4.6 + mcp SDK
- **Status:** verified live 2026-09-15. Smoke test: **23 checks, 0 failures**, `FRESH=1` (no cache).

## Tools

| Tool | Lane | What it does |
|---|---|---|
| `filings_edgar_search` | US | SEC EDGAR full-text search across all filings (`q`, `forms`, `date_from/to`) → direct document URLs |
| `filings_edgar_resolve` | US | Ticker or company-name fragment → SEC CIK + registrant title |
| `filings_edgar_company_filings` | US | Recent filing index for one registrant (ticker or CIK), form-filterable |
| `filings_edgar_financials` | US | XBRL company facts — `Revenues`, `NetIncomeLoss`, `Assets`, EPS, … with FY/FP/form |
| `filings_edgar_document` | US | Fetch + text-extract one filing document (sec.gov only), sha256'd |
| `filings_bnm_rates` | MY | Bank Negara Malaysia Open API: `opr`, `base-rate`, `exchange-rate`, `interest-rate` |
| `filings_my_dataset` | MY | Any official data.gov.my open-data catalogue row set |
| `filings_source_health` | both | Live reachability probe of all 8 upstream lanes — the honest witness |

### Provenance contract

Every result carrying external data includes:

```json
"provenance": {"source_url": "...", "fetched_at_utc": "2026-09-15T15:07:26Z",
               "sha256": "0ab40dfafdeece29…", "http_status": 200, "cached": false}
```

`sha256` is over the exact response bytes. Non-200 upstreams are returned as
`{"error": "upstream_non_200", "http_status": …, "response_excerpt": …}` — never masked, never simulated.

### Cache

`cache/` is sha256-addressed (`<sha256>.bin`) with a `cache/index.json` map of `url → {sha256,
fetched_at_utc, http_status, bytes}`. The same URL is not refetched within 24h. A repeat call returns
`"cached": true` with an identical sha256 (verified in the smoke test).

## Run

```bash
/opt/arifos/venv/bin/python /root/AAA/mcp/filings/server.py       # binds 127.0.0.1:18410
cd /root/AAA/mcp/filings && ./smoke_test.sh                        # cached run
FRESH=1 ./smoke_test.sh                                            # wipes cache, proves live fetch
```

## Observed output (real, 2026-09-15, `FRESH=1`)

```
>> starting filings-mcp on 127.0.0.1:18410
>> server up (pid 1896658), running MCP client checks
TOOLS REGISTERED (8): filings_bnm_rates, filings_edgar_company_filings, filings_edgar_document,
  filings_edgar_financials, filings_edgar_resolve, filings_edgar_search, filings_my_dataset,
  filings_source_health
[PASS] edgar_search http 200      [PASS] apple resolved (0000320193)   [PASS] xbrl entity (Apple Inc.)
[PASS] bnm opr http 200           [PASS] bnm fx has USD                [PASS] my dataset rows
[PASS] 6+ lanes reachable         [PASS] bursa block reported honestly  [PASS] doc sha256 present
checks: 23  failures: 0
SMOKE TEST: PASS
```

Live values returned during verification:

- **SEC FTS** `"material weakness"` + 10-K → `total_matches: 10000`, e.g. ChromaDex Corp. 10-K/A filed
  2020-05-18, `document_url: https://www.sec.gov/Archives/edgar/data/1386570/000165495420005725/cdxc10ka_12312019.htm`
- **AAPL filings** → `cik=0000320193`, SIC `Electronic Computers`, latest 10-Q filed 2026-07-31 (period 2026-06-27)
- **AAPL XBRL** → `RevenueFromContractWithCustomerExcludingAssessedTax = 364,357,000,000 (10-Q, 2026-06-27)`,
  `NetIncomeLoss = 101,464,000,000`, `Assets = 383,266,000,000`
- **BNM OPR** → `{"year":2026,"date":"2026-09-03","change_in_opr":0,"new_opr_level":2.75}`
- **BNM FX** → 27 currencies, `USD middle_rate 4.0818` (2026-09-15)
- **data.gov.my** `fuelprice` → 200, rows returned
- **Cache proof** → second identical call: `cached=True`, same sha256 `0ab40dfafdeece29`

## Live lane health (`filings_source_health`) — 7/8 reachable

| Status | Lane |
|---|---|
| 200 | SEC EDGAR full-text search (`efts.sec.gov`) |
| 200 | SEC EDGAR submissions (`data.sec.gov`) |
| 200 | SEC XBRL company facts (`data.sec.gov`) |
| 200 | SEC ticker→CIK map (`www.sec.gov`) |
| 200 | BNM Open API `base-rate` (needs `Accept: application/vnd.BNM.API.v1+json` — handled internally) |
| 200 | BNM Open API `opr` |
| 200 | data.gov.my catalogue API |
| **403** | **Bursa Malaysia announcements API — Cloudflare JS challenge** |

### Known gap: Bursa Malaysia announcements (BLOCKED upstream, not bypassed)

`GET https://www.bursamalaysia.com/api/v1/announcements/announcements?ann_type=company&per_page=1&page=1`
returns **HTTP 403** with a Cloudflare interstitial body:

```html
<!DOCTYPE html><html lang="en-US"><head><title>Just a moment...</title>...
```

Browser-like `User-Agent` / `Referer` / `X-Requested-With` headers and JSON `Accept` were tried — still 403.
No bypass (no headless-chrome shim, no CAPTCHA solver) is bundled, and **no Bursa announcement data is
simulated**. Consequences for the MY corporate-filings lane:

- Available MY coverage today: BNM regulatory/monetary data + data.gov.my official open data.
- Not available today: Bursa listed-company announcements, SSM company registry (SSM has no open API;
  `api.data.gov.my` has no `ssm_*` catalogue — verified 404 with body
  `{"status_code": 404, "details": ["The data catalogue (ssm_company) requested does not exist."]}`).
- To close it: a paid/licensed Bursa or SSM data feed, or a browser-automation lane outside this server.

### Note on `filings_edgar_financials`

Tag selection follows what the registrant actually filed. US-GAAP `Revenues` is legacy for Apple and its
newest values are FY2018; the current tag is
`RevenueFromContractWithCustomerExcludingAssessedTax` — both are in the default tag set. Pass `tags=` to
query any us-gaap/dei tag.

## Files

- `server.py` — FastMCP server (8 tools, sha256 cache, provenance)
- `smoke_test.py` — real `mcp` SDK streamable-http client, 23 assertions
- `smoke_test.sh` — start server → run client → stop server (`FRESH=1` to clear cache)
- `evidence_probe.py` — one-off live evidence capture used for this README
- `requirements.txt`, `cache/` (sha256-addressed bodies + `index.json`)

DITEMPA BUKAN DIBERI — Forged, Not Given.
