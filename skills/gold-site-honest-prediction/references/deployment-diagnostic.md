# Gold Site Deployment Diagnostic

Standalone diagnostic script for any gold page deployment. Run after every mutation to verify live state.

## Usage

```bash
chmod +x references/deployment-diagnostic.sh
./references/deployment-diagnostic.sh <site_url> [live_path]
```

Default: `site_url=https://syedos.arif-fazil.com/emas/`, `live_path=/var/www/html/syedos/emas/index.html`

## Checks (in order)

1. **HTTP layer** — 200 status, CSP intact, HSTS active, no-cache headers
2. **Page integrity** — DOCTYPE, charset, viewport, no broken HTML
3. **Content audit** — all key BM Penang markers present
4. **API cross-origin** — all 7 endpoints serve valid JSON
5. **Live state consistency** — ticker price == forecast basis.close == apex price
6. **Service status** — gold-api.service active, port 3456 listening
7. **Visual screenshot** — for vision_analyze verification

## Exit codes

- 0: all checks pass
- 1: HTTP failure
- 2: content audit failed (key markers missing)
- 3: API endpoints failing
- 4: live state inconsistent (price mismatch)
- 5: service not running

## Decision table

| Symptom | Likely cause | Action |
|---|---|---|
| 200 OK but content audit fails | Deployment wrote to wrong path | Verify `live_path` matches build output target |
| API 200 but live state inconsistent | Cache serving stale data | Restart gold-api.service + clear node cache |
| Service not running | systemd unit failed | `journalctl -u gold-api.service` |
| Visual screenshot shows missing bands | JS error in chart init | Check browser console, verify lightweight-charts CDN loaded |

## Key endpoints to probe

| Endpoint | Returns | Notes |
|---|---|---|
| `/api/gold/ticker` | live price + levels + signal | Most volatile, refreshes every 30s |
| `/api/gold/apex` | APEX state machine | State, G, C_dark at TOP LEVEL (not nested under apex) |
| `/api/gold/forecast?horizon=3` | wealth.forecast.v1 cone | horizon_days=30 (3 daily points) |
| `/api/gold/snapshot` | full snapshot | ticker + levels + macro combined |
| `/api/gold/macro` | DXY/US10Y/VIX/Silver/USDMYR | Lightweight, ~140 bytes |
| `/api/gold/history?interval=1h&period=7d` | OHLCV + EMA20/50/200 | Heavy, ~169KB |
| `/api/gold/calendar` | scheduled events | For event sentinel input |

## Common false alarms

1. **Cached data showing wrong price** — node server has 10-min cache (line 16 of server.js: `CACHE_TTL = 600_000`). Restart service or wait.
2. **forecast?horizon=3 returning 30-day cone** — backend API interprets `?horizon=3` as integer 3 (==30 day) not "3 days". Want real 3-day endpoint? Backend work needed.
3. **History endpoint returning HTML fallback** — old bug, fixed Sep 2026. If regresses, check `/api/gold/history` returns JSON not HTML.
4. **Macro endpoint returning None** — yfinance rate limit. Backoff + retry.

## Honest edge cases

If multiple checks fail simultaneously:
- Service down → all endpoints fail → fix service first
- Wrong deployment path → HTTP 200 but content fails → check build output target
- Engine changed but live didn't reload → price stale → restart service
