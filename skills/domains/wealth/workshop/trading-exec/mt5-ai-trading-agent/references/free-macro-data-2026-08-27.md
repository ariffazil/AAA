# Free Live Macro Data Sources (proven 2026-08-27 14:32 MYT)

When you need real-time market context for XAUUSD/forex dashboards WITHOUT paid API keys, this 3-source combo covers 90% of what a retail trading agent needs.

## The Stack (proven 2026-08-27)

### 1. Gold/Silver spot (live, every 60s refresh)
```
GET https://api.gold-api.com/price/XAU
GET https://api.gold-api.com/price/XAG
```
- **No API key**, CORS `Access-Control-Allow-Origin: *`
- Returns `{price, currency, currencySymbol, exchangeRate, name, symbol, updatedAt, updatedAtReadable}`
- Pair with `setInterval(fetch, 60000)` in JS — polite, well under any rate limit
- ⚠️ `gold-api.com/price/XBR` (Brent) returns 404 — symbol not supported
- ⚠️ `gold-api.com/price/PALLADIUM` returns 404 — use other sources for PG/PT

### 2. USD/MYR FX (live, daily)
```
GET https://open.er-api.com/v6/latest/USD
```
- **No API key**, returns all fiat vs USD
- Read `data.rates.MYR` for live USDMYR (~4.03 MYR per USD as of 8/27/2026)
- Updates daily; cache for the day
- Alternative: `https://api.exchangerate.host/latest?base=USD&symbols=MYR` (CORS ok, but sometimes slow)

### 3. FRED public CSV (daily macro, no key, no rate limit)
```
GET https://fred.stlouisfed.org/graph/fredgraph.csv?id=SERIES_ID&cosd=YYYY-MM-DD
```
- ⚠️ Set socket timeout ≥6s — FRED is sometimes slow
- ⚠️ Requires `User-Agent: curl/7.81` header or 403
- CSV format: `observation_date,VALUE` — last line is the latest reading

| FRED Series ID | What | Used for | As of 8/27/2026 |
|----------------|------|----------|-----------------|
| `DTWEXAFEGS` | DXY Advanced Foreign Economies (closest to "DXY") | Gold inverse correlation | 111.36 (Aug 21) |
| `DTWEXBGS` | DXY Broad (Jan 2006=100) | Broader USD strength | 118.06 (Aug 21) |
| `DGS10` | 10Y Treasury yield | Gold inverse | 4.64% (Aug 25) |
| `DFII10` | 10Y real yield (TIPS) | **Strongest gold driver** | 2.32% (Aug 25) |
| `DCOILBRENTEU` | Brent crude USD/bbl | Geopolitical/risk-off | $88.24 (Aug 25) |
| `DCOILWTICO` | WTI crude USD/bbl | US energy benchmark | $83.90 (Aug 25) |

### What doesn't work (avoid)
- ❌ Yahoo Finance `query1.finance.yahoo.com` → 429 Too Many Requests
- ❌ Investing.com / WSJ quotes → 401/403 without auth
- ❌ Stooq direct CSV → 404 (requires JS)
- ❌ Twelve Data demo → 401 (no real demo)
- ❌ Brent/PG/PT via gold-api → symbol not supported

## FRED Trick: Pull Multiple Series in Parallel

```python
import urllib.request, json
from concurrent.futures import ThreadPoolExecutor

def fetch_fred(series_id, start="2025-08-01"):
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}&cosd={start}"
    req = urllib.request.Request(url, headers={"User-Agent": "curl/7.81"})
    r = urllib.request.urlopen(req, timeout=8)
    lines = r.read().decode().strip().split("\n")
    return series_id, lines[-1].split(",")  # ("DGS10", ["2026-08-25", "4.64"])

with ThreadPoolExecutor(max_workers=5) as ex:
    futures = [ex.submit(fetch_fred, sid) for sid in ["DTWEXAFEGS","DGS10","DFII10","DCOILBRENTEU","DCOILWTICO"]]
    results = {sid: row for sid, row in (f.result() for f in futures)}
print(json.dumps(results, indent=2))
```

End-to-end: ~3-4 seconds for 5 series. Safe to refresh every 4h or daily via cron.

## ATR-Aware Gold Verdict (proven 8/27/2026)

For trading dashboards, tight thresholds around current spot:

```js
const base = 4611.70;  // rebase on each major move, e.g. +$50 increments
const pctFromBase = ((goldPrice - base) / base) * 100;
if (goldPrice > base * 1.005)        verdict = 'OVERBOUGHT';  // >$4,635
else if (goldPrice < base * 0.995)   verdict = 'OVERSOLD';    // <$4,588
else if (pctFromBase > 0.2)          verdict = 'BULLISH';
else if (pctFromBase < -0.2)         verdict = 'BEARISH';
else                                  verdict = 'SABAR';
```

For richer verdict, combine with RSI + EMA20/50 + S/R bands:
- **R1 band** = spot + 0.3% (~$4,625 at $4,611)
- **S1 band** = spot - 0.3% (~$4,595)
- OVERBOUGHT only fires when RSI>65 AND price > R1 (both conditions)
- OVERSOLD only fires when RSI<35 AND price < S1

## Macro Contextual Narrative (what to say)

When the verdict fires, append the macro state to the explanation:
- **US10Y turun** (4.74→4.64 in 1 week) → USD weakening → gold supportive
- **Real yield 2.32%** → still elevated, caps gold upside
- **Brent -8.9% in 2 days** → risk-off mixed; usually mild gold-positive

Footer pattern (BM casual):
```
"Macro: US10Y ↓ (USD weaken = gold ↑), Brent ↓↓ (risk-off mixed). 
Setup bersih. Confluence EMA+RSI+S/R ok. Buy 4625, SL 4595. Jangan gerakkan SL."
```

## When to rebase

Rebase `base` price weekly, or when:
- Spot moves >2% from base in 1 week
- Major macro event (FOMC, NFP, CPI)
- New ATH/ATL

Don't rebase daily — adds noise, breaks ATR calibration.

## Pitfall: Pasting FRED IDs in URL

`?id=DGS10` works. `?id=dgs10` (lowercase) returns empty. Case-sensitive. Always paste from FRED's series page directly.

## Pitfall: Gold-API vs OANDA / MT5

Broker XAUUSD (OANDA feed) shows OANDA:XAUUSD. Gold-API returns spot XAU. Difference is typically $0-2 for retail purposes. Don't try to match exactly — basis-point drift is noise.

## Pitfall: time-of-day bias in narrative

US10Y reading from FRED is end-of-day. Brent is end-of-day. If you're producing an Asia-open narrative, the values reflect US close. Don't claim "Brent dropped today" when it's actually US-session movement. Use "Brent ditutup lower" or specify session.
