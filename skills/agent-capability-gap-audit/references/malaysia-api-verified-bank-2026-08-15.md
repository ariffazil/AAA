# Malaysia Reality APIs — Verified Bank (probed live from af-forge VPS, 2026-08-14/15)

Every entry below was curl-probed from the federation VPS itself, not read from docs. Council citations were NOT trusted until re-probed (data.gov.my weather docs → live 404; Aladhan needs -L).

## ALIVE — verified working

### AlAdhan prayer times (JAKIM)
- `https://api.aladhan.com/v1/timingsByCity?city=George%20Town&country=Malaysia&method=17`
- **Quirk: returns 302 without `-L`.** Always `curl -sL`.
- method=17 (JAKIM) vs method=20: identical times for George Town on probe day (Fajr 05:55, Maghrib 19:32). Use 17.
- Shape: `data.timings.{Fajr,Syuruk,Dhuhr,Asr,Maghrib,Isha}`, `data.date.readable`.

### Open-Meteo weather
- `https://api.open-meteo.com/v1/forecast?latitude=5.4141&longitude=100.3288&current=temperature_2m,relative_humidity_2m,precipitation,weather_code,wind_speed_10m&daily=precipitation_probability_max,temperature_2m_max,temperature_2m_min&forecast_days=1&timezone=Asia%2FKuala_Lumpur`
- Keyless, no UA needed. WMO weather_code → BM label map in my-reality script.
- Shape: `current.*`, `daily.*` arrays.

### Open-Meteo air quality (AQI)
- `https://air-quality-api.open-meteo.com/v1/air-quality?latitude=5.4141&longitude=100.3288&current=pm10,pm2_5,us_aqi&timezone=Asia%2FKuala_Lumpur`
- Shape: `current.{pm10,pm2_5,us_aqi}`.

### BNM exchange rate
- `https://api.bnm.gov.my/public/exchange-rate?quote_code=USD&session=1200&date=YYYY-MM-DD`
- Header REQUIRED: `Accept: application/vnd.BNM.API.v1+json`. Without quote_code returns all currencies.
- **Quirk: nested shape — `data[].rate.middle_rate`**, NOT `data[].middle_rate` (first parse attempt failed on this).
- Sample: USD middle RM 4.0855 (2026-08-14).

### BNM Kijang Emas (gold)
- `https://api.bnm.gov.my/public/kijang-emas` (same Accept header)
- Shape: `data.{effective_date, one_oz/half_oz/quarter_oz.{buying,selling}}`.
- Sample: 1oz RM 18,157/18,925 buy/sell (2026-08-14).

## DEAD / UNRELIABLE — do not cite

| Source | Result | Note |
|---|---|---|
| data.gov.my weather (`/weather/1.0/*`) | 404 | Council's citation #3 — docs stale, endpoints gone. Use Open-Meteo. |
| `api.data.gov.my` catalog + `portal.data.gov.my` | 404 / HTTP 000 | Fuel-price API does not exist cleanly. KPDN needs scraping — P1. |
| date.nager.at `/publicholidays/2026/MY` | HTTP 204 empty | MY 2026 dataset not published yet. |
| Nager.Date generic | 204 | — |
| BNM `earth-exchange-rate` endpoint | 404 | Wrong endpoint name; correct is `/public/exchange-rate`. |

## Related probes (transport, not MY data)

- Egress sanity: google.com 200 from VPS — failures above are source-side, not network.
- gold-api.com XAU, Yahoo v8, jsdelivr currency-api work as non-BNM fallbacks (documented in arifos-cron-ops).

## Consumers (the paying customers)

- `arif-morning-pulse` (06:00 daily) and `arif-world-reality-intel` (09:00 daily) cron jobs currently burn web_search for this same data every morning — the adapters' first consumers. Patch pending per one-day-one-patch flow.
