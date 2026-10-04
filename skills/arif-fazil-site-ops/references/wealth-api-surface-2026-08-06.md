# WEALTH API Surface (verified 2026-08-06)

Live endpoints behind every market page on arif-fazil.com. All CORS-enabled, all
return `application/json`, all 200 OK at time of verification. Probe before
assuming any of these are dead — sibling reports claiming "WEALTH down" are
usually just seeing stale cached HTML.

## Snapshot endpoints (current state)

Each `/<asset>/api/snapshot` returns a `wealth.snapshot.v1` envelope with:
`asset`, `observed_at`, `source`, `ticker` (symbol, price, change, changePct,
rsi, rsiState, signal, confidence, ema20/50/200, emaTrend, pivot), `levels`
(support[3], resistance[3], support_daily[3], resistance_daily[3], pivot),
`macro` (asset-specific), `coherence_id`.

| Path | Asset | Ticker | Macro includes |
|---|---|---|---|
| `/gold/api/snapshot` | gold | XAUUSD | dxy, us10y, vix, silver, gsr, usmyr |
| `/oil/api/snapshot` | oil | XBRENT | dxy, us10y, vix, silver, usmyr |
| `/gas/api/snapshot` | gas | XNATGAS | dxy, us10y, vix, silver, usmyr |
| `/klci/api/snapshot` | klci | FBMKLCI | dxy, us10y, vix, usmyr, ewm, sti, hsi, opr_pct, opr_status |
| `/usdmyr/api/snapshot` | usdmyr | USDMYR | dxy, us10y, vix, sgd_myr, usd_sgd, usd_idr, usd_thb, usd_cny, opr_pct, opr_status, fed_funds_pct, fed_status, rate_differential_pct |

## History endpoints

`/<asset>/api/history?interval=<tf>&period=<p>` returns:
`candles` (open/high/low/close/volume), `ema20`, `ema50`, `ema200`, `rsi`,
plus `interval` and `period`.

| Asset | interval options | period options |
|---|---|---|
| gold | 1h, 4h, 1d, 1wk | 7d, 30d, 3mo, 6mo (mapped per tf in client) |
| oil/gas/klci/usdmyr | same | same |

Default 200 candles per response.

## Apex endpoint (gold only)

`/gold/api/apex` returns the F8 weighted geometry:
`apex` (A, P, E, X, Phi), `G` (genius score), `C_dark` (antihantu), `dS`
(entropy delta), `state` (CHAOS/BALANCED/SEALED), `direction`, `confidence`,
`volume_trend`, `volume_confirmation`, `momentum`, `volatility_regime`,
`verdict` (HOLD/BUY/SELL), `price`, `ema_20/50/200`, `rsi_14`, `atr_14`,
`data_points` (1H/4H/1D candle counts), `timestamp`.

## Macro context

Stale cache warning: `Cache-Control: no-cache, no-store, must-revalidate`
is set on `/wealth/*` paths (per Caddyfile). CDN may still serve old HTML if
you update the wrong disk path. The pitfall is documented in SKILL.md
("Caddyfile root path ≠ /var/www/html/<slug>/").

## Pattern: use snapshot for "now", history for "chart"

```js
const snap = await fetch('/gold/api/snapshot').then(r => r.json());
// snap.ticker.price, snap.ticker.rsi, snap.ticker.signal — UI numbers

const hist = await fetch('/gold/api/history?interval=4h&period=30d').then(r => r.json());
// hist.candles — chart OHLC; hist.ema20/50/200 — overlay lines
```

Combine: render `ticker.price` as the latest point label, `levels.support[0]`
and `levels.resistance[0]` as dotted horizontal lines on the chart.

## Live values captured during verification (2026-08-06, ~12:24 MYT)

- Gold: $4,254.62, RSI 49.4, signal LONG, conf 0.8, EMA20/50/200 =
  4246.01/4193.33/4103.01, pivot 4253.82
- Oil: $80.24, RSI 62.3, signal SHORT, EMA20/50/200 = 79.74/80.27/82.16
- Gas: $2.66, RSI 38, signal NEUTRAL, conf 0.3 (low — avoid)
- KLCI: 1737.15, RSI 64.2, signal LONG, conf 0.5, EMA20/50/200 =
  1717.95/1708.16/1715.02, OPR 3.00%
- USD/MYR: 4.087, RSI 51.6, signal NEUTRAL, EMA20/50/200 =
  4.0837/4.0629/3.9976, stress band 4.50, 90d mean 4.0218
