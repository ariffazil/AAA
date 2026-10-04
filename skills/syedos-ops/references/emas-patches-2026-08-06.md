# /emas/ patch session — 2026-08-06

Source: `/var/www/html/syedos/emas/index.html` (426 lines, served at https://syedos.arif-fazil.com/emas/)
Backup: `/var/www/html/syedos/emas/index.html.bak-20260806`

## Bugs found + fixed

| # | Bug | Fix location in source |
|---|---|---|
| 1 | Silver hardcoded `$31.2` | Replaced `fetchData()` to call XAU + XAG via Promise.all |
| 2 | DXY hardcoded `98.5` | Kept static (no free CORS API w/o key), now set inside tick() |
| 3 | USD/MYR hardcoded `4.08` | Added `exchangerate.host` live fetch + fallback |
| 4 | RSI = `50 + diff*2` (nonsense) | Replaced with Wilder 14-period from `__lastCloses` |
| 5 | EMA20/50 = `price × 0.995/0.99` (fake) | Replaced with real EMA computation |
| 6 | S1/S2/R1/R2 = `price × ±1.5%/±3%` (fake) | Replaced with swing highs/lows from `__lastHighs`/`__lastLows` |
| 7 | `tfMap['4h'] = '1h'` (typo) | Fixed to `'4h'` |
| 8 | Init fire twice (no `_started` guard) | Replaced both init blocks with single guarded `start()` |
| 9 | "BULLISH SHORT" hybrid label | Changed to plain "BULLISH" / "BEARISH" |
| 10 | RSI/EMA display stale until next 30s tick | Added `tick()` call after `candleSeries.setData(ohlc)` |

## Live verification result (post-fix)

```
price:     $4262.8  ✅
silver:    $61.83   ✅ (was $31.2)
rsi:       89       ✅ (real Wilder; overbought given +3.34% rally)
bias:      OVERBOUGHT ✅ (RSI >65 → HOLD verdict, not SABAR)
ema20:     $4170.5  ✅
ema50:     $4115.8  ✅
s1:        $4019.0  ✅ (real swing low)
r1:        $4294.5  ✅ (real swing high)
closesLoaded: 185 (4H binance fallback)
```

## Known deferred items

- **DXY live feed** — no free CORS-enabled endpoint without API key. Options: `fcsapi.com`, `marketstack.io`, `twelvedata.com`. Add to `kunci-mas.env` (mode 600) when registering.
- **WEALTH engine `arif-fazil.com/gold/api/history`** — never probed whether endpoint alive. Binance fallback handles absence. If you want sovereign-routed candles, first `curl -sfL "https://arif-fazil.com/gold/api/history?interval=4h&period=30d"` to verify.
- **exchangerate.host CORS** — may rate-limit or block browser-origin. `open.er-api.com/v6/latest/USD` is a known CORS-friendly fallback.
- **`SABAR` verdict aesthetic** — kept as the neutral state label. Could rename to NEUTRAL if you want professional tone; `SABAR` is consistent with `HEAL` page voice.

## Edge cases to watch

- `__lastCloses` only populates after `loadChart()` completes (~1-2s after first paint). RSI/EMA first render shows `price` as fallback — expected, not a bug.
- Binance `fapi.binance.com/fapi/v1/klines?symbol=XAUUSDT` works for gold; if ever 4xx, fallback to `api.binance.com/api/v3/klines?symbol=PAXGUSDT`. Do NOT change order — fapi is preferred (more liquid).
- Silver's gold-api.com endpoint updatedAt is sometimes stale by 30s. UI timestamp comes from XAU's updatedAt — fine, but if you add dedicated silver timestamp later, use `jAg.updatedAt`.
