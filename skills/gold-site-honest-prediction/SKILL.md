---
name: gold-site-honest-prediction
description: 'Use when deploying or modifying any arifOS gold page (syedos.arif-fazil.com/emas/, arif-fazil.com/world/economics/gold/, /gold/) or any wealth.gold.* forecast surface. Captures the operating discipline proven across the 2026-09-25 audit cycle: two-rail (Trade + Simpan) without auto-translation, SHADOW-by-default until walk-forward beats baseline, honest horizon labels, calibration metrics as live gate.'
trigger:
- gold site
- WEALTH forecast
- SHADOW
- calibration harness
- two-rail
- quantile path
- XAUUSD
- emas page
- CommodityPage
- wealth.gold.forecast
- wealth.gold.orchestration
---

# Honest Gold Site Deployment Discipline

This skill is the institutional memory of the 2026-09-25 gold site audit + rebuild cycle. Use it as the operating contract for any agentic gold prediction surface in arifOS.

## Conductor-Execute Hybrid (2026-09-25 lesson — ARIF will call you out)

User explicitly demanded direct execution, not always-subagent delegation: **"Why u don't execute. Why biar @ASI_arifos_bot which execute???"**

Decision rule:
- **Direct execute_code / patch / write_file**: tactical single-file edits (<5 tool calls, single-session loop). Examples: add CSS, edit a function, write a build script.
- **delegate_task subagents**: multi-step architecture, parallel research, heavy compute (>10 tool calls OR >5min OR parallel work). Examples: build 8-agent pipeline, run walk-forward validation, generate reports.
- **Stay as conductor** when agents are running: report honest verdict in BM Penang when they return; don't disappear.

## Multi-Copy Engine Trap (CRITICAL — caught via 3 attempt failures)

There are **3+ copies** of fetch_gold.py on this system:
- `/root/WEALTH/forecast/calibration/harness.py` (AUDIT REPLICA — synthetic, modified by calibration harness)
- `/root/WEALTH/engines/commodity/gold-api/fetch_gold.py` (SOURCE REPLICA — not served)
- `/var/www/html/gold/api/fetch_gold.py` (TRUE LIVE — served by node server.js on localhost:3456 since Sep 20)

**Before claiming "engine changed"** verify via:
```bash
ss -tlnp | grep 3456                    # confirm gold-api port
systemctl status gold-api.service       # confirm node server running
ls -la /var/www/html/gold/api/         # confirm live file location
curl -s https://arif-fazil.com/gold/api/forecast?horizon=3 | python3 -m json.tool | head -20
```
Modify the LIVE one. After service restart (`systemctl restart gold-api.service`), re-curl to confirm new code took effect.

## 3-Attempt Honest Failure Pattern (template for future tuning)

When user asks "back test / tune / improve" the forecast engine, EXPECT 3 attempts and report honestly at each:
1. **Engine modifications** (add atr_multiplier / momentum bias) → likely FAIL (modified wrong file first, then calibration worse)
2. **Generic pattern mining** (engulfing/hammer/doji) → likely STOP (wrong spec)
3. **Proper wave/cycle challenger** (wavelet + CEEMDAN + Hilbert) → BUILT but admission rule FAILS (-8.39 vs M0)

**Per attempt**: write receipt with honest verdict. Don't synthesize "partial recovery" if there's none.

## Core Doctrine (5 invariants)

### 1. Two rails, NEVER auto-translate
- **Trade rail** (margin technical): `LONG BIAS / SHORT BIAS / NO TRADE / EVENT RISK`
- **Simpan rail** (physical saver, BM Penang): `SABAR / TUNGGU / JAGA / TAMBAH BERPERINGKAT`
- Simpan rail derives ONLY from saver-side signals (dispersion, median return magnitude, calibration state). NEVER consumes APEX verdict.
- Honest label for users: "Default conservative — jangan ubah jumlah simpanan berdasarkan model yang belum divalidasi."

### 2. SHADOW is the default until walk-forward proves edge
- Status values: `SHADOW → DEGRADED → LIVE → QUARANTINE`
- Promotion requires ALL THREE: pinball_skill_score > 0 AND coverage ∈ [0.70, 0.90] AND brier_skill > 0, on ≥ 30 walk-forward windows
- If model doesn't beat baseline on real data, **stay SHADOW**. Calibration discipline > aspirational promotion.

### 3. Quantile path, NEVER fake OHLC
- Emit P10/P25/P50/P75/P90 for +24h/+48h/+72h horizons
- Honest label: "Projeksi quantile (hari 1–3)" if backend is 30-day cone — don't label as purpose-built 72H
- Median displacement is NOT a probability. Display as "% median", not "P(up)"

### 4. Caddy reload is T3 HOLD — never autonomous
- Per `/root/arif-fazil.com/AGENTS.md`: never run `make deploy`, never reload Caddy
- Sync to `/var/www/html/arif/` and `/var/www/html/syedos/emas/` via rsync only
- If backend route needs new Caddy handle, queue for human authorization

### 5. Honest labels > aspirational labels
- "G = 0.0064 (tiada edge)" beats "70% confidence" when underlying signal is weak
- "Calibration belum selesai" beats "walk-forward passed"
- "TradingView library (BSD-3)" beats "custom chart library" when both render the same chart engine

## Backend Integration (canonical)

### Endpoints (already running at localhost:3456)
- `/api/gold/ticker` — current price + levels + signal
- `/api/gold/apex` — APEX state machine (state, direction, verdict, G, C_dark)
- `/api/gold/forecast?horizon=3` — wealth.forecast.v1 cone (currently 30-day daily)
- `/api/gold/snapshot` — full snapshot with macro
- `/api/gold/macro` — DXY/US10Y/VIX/Silver/USDMYR
- `/api/gold/history?interval=1h&period=7d` — OHLCV + EMA20/50/200
- `/api/gold/calendar` — economic calendar (when event sentinel needs it)

### Caddy routing for syedos (cross-origin workaround)
- `syedos.arif-fazil.com` vhost does NOT have `/gold/api/*` reverse proxy
- Solution: Syed's template uses `https://arif-fazil.com/gold/api/*` (CORS allowlisted via `access-control-allow-origin: *`)
- CSP allows: `connect-src https://arif-fazil.com ... https://*.tradingview.com`
- Native same-origin route requires Caddy reload (T3 HOLD)

## Build Pattern (Syed's site as canonical example)

```
/root/WEALTH/site/src/syedos-emas/
├── template.html        # Single-file HTML with inline CSS+JS
├── gold.json            # Config: endpoints, stance vocab, calibration gate
├── build.py             # Atomic write renderer (write to .tmp, then rename)
├── tests/               # (optional) unit tests for derivation logic
└── .backup-<ts>         # Backup before any mutation

Deploy flow:
1. Backup live HTML to source tree
3. Run: python3 build.py [/custom/output/path]
4. Verify: curl + check key markers
5. Write receipt to /root/AAA/VAULT999/receipts/
```

## Calibration State Machine

```
SHADOW (default)
  ↓ walk_forward_passed=True AND coverage in band AND brier>0
LIVE
  ↓ any adversarial test fails
QUARANTINE
  ↓ at any time
NO_FORECAST
  ↓ 555 reports ok
SHADOW
```

## Forbidden Patterns (from IRFANCLAW audit 2026-09-25)

1. ❌ **72 fake future OHLC candles** — model doesn't know future price action at hourly resolution. Emit quantile path only.
2. ❌ **Median displacement labeled as probability** — they're different quantities.
3. ❌ **Auto-translate LONG BIAS → TAMBAH BERPERINGKAT** — leverage trade state ≠ savings advice.
4. ❌ **Hardcoded market values in template** — only runtime snapshot values.
5. ❌ **Receipt per frontend fetch** — 1 receipt per forecast issuance.
6. ❌ **"Hardening queued" treated as completion** — needs files + tests + hashes.
7. ❌ **Silent model changes** — every tuning produces new versioned file.
8. ❌ **WebMCP advertise new routes before 2xx verified**.

## Required Receipts (per deployment)

Every gold page mutation must write to `/root/AAA/VAULT999/receipts/`:
- `forecast_id` (uuid)
- `trace_id` (uuid, links to orchestrator)
- `digest` (sha256 of payload)
- `governance.execution_enabled = False`
- `governance.human_confirmation_required = True`
- `governance.authority = "F13 required for promotion out of SHADOW"`

## Honest Calibration Findings (Live XAUUSD 2026-09-25)

On real XAUUSD 30-day walk-forward:
- Pinball skill: **-0.81** (model 81% WORSE than random walk baseline on quantile loss)
- Coverage: **0.72** (in band but misleading — bands too narrow on real data)
- Brier skill: **-1.15** (directional 115% worse than 50/50)
- PSI: **1.39** (well above 0.25 → QUARANTINE)
- Missing data degradation: **7.76×** (model degrades 7.7× faster than baseline)

**Verdict: stay SHADOW. Promotion to LIVE would be dangerous and dishonest.**

## Cross-Asset Lessons

Per WGC H1 2026:
- Momentum: 24% of gold return (dominant driver)
- Risk premium: 17%
- USD/FX: 14%
- Economic expansion: 12%
- Real rates: 3% (surprising weak — the real rate = gold inverse model is broken post-2022)

**Implication:** system that watches ONLY real rates will miss 76% of variance. Must include momentum + risk + USD.

## Memory Notes

- "REALITY > EVERYTHIN..." pattern works as session closer
- User prefers BM Penang kampung register over formal/baku
- Subagent pattern: 2-3 parallel agents + delegated scope beats single mega-agent
- Honest calibration > aspirational metrics — user accepts SHADOW when warranted
- Independence test (IRFANCLAW audit) caught real defects — keep independent verification in pipeline

## References

- arifOS AGENTS.md (federation canonical)
- IRFANCLAW audit 2026-09-25 (9 defects found, 6 fixed immediately)
- WGC Gold Outlook 2026 (driver attribution: momentum 24% / risk 17% / FX 14% / expansion 12% / rates 3%)
- Chen-Pu Jan 2026 (agentic AI nowcasting, top-20 alpha 18.4 bps/day)
- Bailey 2014 PBO (backtest overfitting probability)
- LuxAlgo Mar 2026 (logistic signal calibration discipline)

DITEMPA BUKAN DIBERI ⚒️

## Wave Forge Admission Rule (2026-09-25 update)

When adding new forecast components (wave/cycle/sentiment/etc.) to the gold engine:

1. **M4 challenger must beat BOTH M0 (random walk) AND M4-TREND (trend only)** — not just baseline. If only M0 is beaten, the apparent edge is just smoothing.

2. **Wavelet + CEEMDAN/EMD + Hilbert transform** for non-stationary signal processing. NEVER raw FFT on prices (spurious cycles from trend + structural breaks).

3. **Stability attacks required**: 14/30/60/90-day lookback perturbations, endpoint perturbation, regime stratification, block bootstrap. If a candidate mode doesn't survive, reject.

4. **Endpoint problem**: Phase estimates at right edge are unreliable due to Hilbert end-effect. Need revision_after_1h, revision_after_4h metrics. If phase flips with one new candle, model is not safe.

5. **Status default = SHADOW_CHALLENGER**. Never auto-promote. F13 authorization required to move out of SHADOW.

## Multi-Model Discipline (2026-09-25)

System maintains models in parallel:
- M0: random walk baseline (no skill target, just for comparison)
- M2: sparse market-reality (price + volatility + USD + yields + silver) — current champion
- M4-TREND: trend only, no waves
- M4-WAVE: trend + validated adaptive modes (new challenger)
- M4-ABLATION: same as M4-WAVE with phase/frequency/amplitude removed individually

Champion promotion: M_new must beat M_champion on walk-forward with purge, post-cost, multi-regime.


## Lightweight Charts v4.x Deployment Pitfalls (2026-09-25 lesson)

1. **NO native vertical time lines.** `createPriceLine()` only creates HORIZONTAL price-level lines, not vertical time markers. For a vertical forecast-start divider, use HTML/CSS overlay positioned via `chart.timeScale().timeToCoordinate(time)`. Subscribe to `subscribeVisibleTimeRangeChange` to update on zoom.

2. **`setMarkers` markers cluster when chart auto-fits.** When chart contains 200 historical candles + 720 hourly forecast points, the first 24 hours get compressed into <5% of chart width. Markers at hour 24/48/72 appear bunched near origin. Fix options (in order of complexity):
   - Accept cosmetic clustering (markers exist, time-accurate)
   - Stagger vertically with `position: 'aboveBar' | 'inBar' | 'belowBar'`
   - Replace with HTML overlays (more control, can label with formatted text)
   - Change interp to use 12-hour or 6-hour steps for visible spacing

3. **Chart container must have explicit height.** `<div id="tv-chart" style="height: 380px">` — not just `style="width: 100%"`. Chart needs fixed height to render.

4. **Wait for chart.timeScale().fitContent() AFTER setData() + markers.** Calling fitContent before markers are set locks the wrong visible range.

5. **Price-line only supports horizontal lines at a price level.** If you need a vertical line at a specific time, use HTML overlay. Don't keep trying `createPriceLine({time: ...})` — it doesn't accept time as a parameter.

## Live Site Audit Procedure (always-on for any deployed page)

Run after every deployment:

```bash
# 1. HTTP layer
curl -sI https://syedos.arif-fazil.com/emas/ | head -20

# 2. Page integrity
curl -s https://syedos.arif-fazil.com/emas/ > /tmp/page.html
for marker in "UNTUK TRADE" "UNTUK SIMPAN" "SHADOW" "DITEMPA BUKAN DIBERI" "Hari +1"; do
  grep -q "$marker" /tmp/page.html && echo "✓ $marker" || echo "✗ $marker"
done

# 3. API cross-origin (via CORS allowlist on arif-fazil.com)
for ep in ticker apex forecast snapshot macro history calendar; do
  status=$(curl -s -o /dev/null -w "%{http_code}" "https://arif-fazil.com/gold/api/$ep")
  echo "/gold/api/$ep: HTTP $status"
done

# 4. Live state consistency
TICKER_PX=$(curl -s https://arif-fazil.com/gold/api/ticker | python3 -c 'import sys,json;print(json.load(sys.stdin)["price"])')
FC_PX=$(curl -s 'https://arif-fazil.com/gold/api/forecast?horizon=3' | python3 -c 'import sys,json;print(json.load(sys.stdin)["basis"]["close"])')
[ "$TICKER_PX" = "$FC_PX" ] && echo "✓ Consistent: $TICKER_PX" || echo "✗ MISMATCH: ticker=$TICKER_PX forecast=$FC_PX"

# 5. Visual screenshot for vision analysis
google-chrome --headless=new --disable-gpu --no-sandbox \
  --window-size=720,1800 --virtual-time-budget=10000 \
  --screenshot=/tmp/audit.png https://syedos.arif-fazil.com/emas/
```

## References

See `references/deployment-diagnostic.md` for the full audit script + checklist.

DITEMPA BUKAN DIBERI ⚒️


## Session 2026-09-25 — Final Arc (M5+)

By end of session, 4 attempts at adding edge to gold price prediction:
1. Engine modification → failed (modified replica)
2. Wave Forge → failed (M3 -8.39 vs M0)
3. Gravity Field → failed (M4 -3.72 vs M0, gravity NOT TESTED on real data)
4. Perplexity causal replay → confirmed M0 wins

**M5 — Adaptive Distribution Engine** is the right next move:
- Predict distribution QUALITY (volatility + range + asymmetry), NOT direction
- Center path = M0 random walk
- Admission: pinball_loss <= M0 + coverage ~80%/50% + narrower bands + lower QLIKE
- If M5 fails too: gold is noise at 72H horizon for retail-scale analysis

**Key lessons for next session:**
- Multi-source-of-truth problem (3 copies of fetch_gold.py) needs resolution
- Independent audit (IRFANCLAW-style) catches defects internal verification misses
- Adding features without new data source = overfitting risk
- Honest calibration (SHADOW + QUARANTINE) is correct state, not failure
- Trend model (M1) tentatively wins on n=3 sample but too small to promote
- Wave component is decorative — period/amplitude unstable
- Gravity inoperative at 72H horizon — CB demand is quarterly+
- Live engine has 3-route drift; source-of-truth audit pending
- 105 tests passing, 17 receipts in VAULT999, full artifact trail

**For future sessions:**
1. FIRST ACTION: resolve fetch_gold.py multi-source-of-truth (pick canonical path)
2. SECOND: ensure real historical macro data available (FRED DFII10, COT, WGC) for proper gravity tests
3. THIRD: run 30-50 sample non-overlapping walk-forward with proper timestamp guards before any LIVE promotion
4. FOURTH: M5 admission if it improves M0 distribution quality (without direction claim)
5. FIFTH: never claim edge on n<30 samples — statistical honesty
