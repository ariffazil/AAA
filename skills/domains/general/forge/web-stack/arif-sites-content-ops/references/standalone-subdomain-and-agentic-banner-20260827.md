# Standalone Subdomain + Agentic Banner Patterns (2026-08-27)

Two new patterns forged when updating `syedos.arif-fazil.com` with an "Agentic Intelligence" layer.

## 1. Standalone Subdomain Pattern (third-party / persona sites)

For non-Arif persona sites (e.g. `syedos.arif-fazil.com` for Syed), the pattern differs from the React/Vite main site.

- **Tech:** Static HTML, no build step. Chart.js / TradingView / Leaflet from CDN. Inline CSS+JS.
- **Disk root:** `/var/www/html/<subdomain>/` (NOT under arif-fazil.com path).
- **Caddy vhost:** `import tls_origin` + `encode zstd gzip` + `handle /upload* { reverse_proxy localhost:18900 }` + `handle /dashboard/* { try_files /dashboard.html /index.html; file_server }` + catch-all `try_files` + `file_server`.
- **Cloudflare:** A record, proxied=true, TTL 120. Cert via Caddy ACME (auto).
- **F13 ruling:** "Jangan link dengan main site" — no cross-links between subdomain and arif-fazil.com.
- **Multi-surface:** Mission cards on home page linking to `/emas/`, `/nasilemak/`, `/heal/`, `/dashboard/`, `/meal-plan/`. Each subpage is self-contained HTML.
- **`llms.txt` at root** — agent discovery. List every page, every live data endpoint, every cron job, every system service. Update on every site change.
- **Pitfall:** Webroot deletion during federation maintenance (proven 2026-08-03). Recovery: check `/root/backups/www-html-*` tarballs newest first, copy back. Caddy stays configured, 404 until restore.
- **Pitfall:** Frozen-snapshot trap — Caddy serves from disk instantly on file change, no reload needed. But upstream WEALTH API endpoint changes (gold-api vs Binance) need a service restart (`systemctl restart gold-api`) AND cache clear.

## 2. 🧠 Agentic Intelligence Banner — Live Signal UI Pattern

For any site that displays "intelligence" (trading signal, business KPI, monitoring metric), the banner pattern is:

1. **Strip at top of body** (above mission cards / chart). Always visible.
2. **Title row:** "🧠 AGENTIC SIGNAL · HH:MM:SS MYT" — live timestamp.
3. **3-5 rows, each with:** key (left, 50% width), val (right-aligned, 25%), verdict pill (rightmost, 25%, color-coded).
4. **Verdict pills:** `ab-v-green` (positive), `ab-v-red` (negative), `ab-v-gold` (neutral/SABAR).
5. **Data sources:** Live API (gold-api.com, er-api.com, met.gov.my) for spot data + heuristic/locally-computed for derived metrics (verdict, R:R, lot size).
6. **Update cadence:** Live data fetches every 60s; meta tag `temporal:localtime` updates every 1s.
7. **No new external deps.** Computed metrics run in inline JS using the same data the page already fetches — don't fetch from a separate endpoint.
8. **Pattern reuse:** Same DOM structure on `/`, `/emas/`, `/nasilemak/`. Each page computes its own verdict from the data it already has.

**Reference implementation:** `syedos.arif-fazil.com` (3 files patched: `index.html`, `emas/index.html`, `nasilemak/index.html`, plus `llms.txt` updated).

### Banner HTML template

```html
<div class="agentic-banner" id="agenticBanner">
  <div class="ab-title">🧠 AGENTIC SIGNAL · <span id="ab-ts">--:-- MYT</span></div>
  <div class="ab-row">
    <span class="ab-key">Emas (XAUUSD)</span>
    <span class="ab-val" id="ab-emas">$--</span>
    <span class="ab-verdict" id="ab-emas-v">--</span>
  </div>
  <div class="ab-row">
    <span class="ab-key">Berlauk Cap (hari ni)</span>
    <span class="ab-val" id="ab-cap">-- unit</span>
    <span class="ab-verdict ab-v-green">SAVES ~RM45</span>
  </div>
  <div class="ab-row">
    <span class="ab-key">TOD Mix (cuti/hari ni)</span>
    <span class="ab-val" id="ab-tod">--</span>
    <span class="ab-verdict ab-v-gold">+12% MARGIN</span>
  </div>
</div>
```

### Banner CSS

```css
.agentic-banner {
  background: linear-gradient(135deg, rgba(240,165,0,0.08), rgba(240,165,0,0.02));
  border: 1px solid rgba(240,165,0,0.25);
  border-radius: 12px; padding: 14px 16px; margin-bottom: 18px;
}
.ab-title { font-size: 11px; font-weight: 700; color: #f0a500; letter-spacing: 1.5px; margin-bottom: 10px; }
.ab-row { display: flex; align-items: center; padding: 5px 0; font-size: 12px; border-bottom: 1px solid rgba(240,165,0,0.08); }
.ab-row:last-child { border-bottom: none; }
.ab-key { flex: 0 0 50%; color: #6b7280; }
.ab-val { flex: 0 0 25%; color: #fff; font-weight: 600; text-align: right; padding-right: 8px; }
.ab-verdict { flex: 0 0 25%; font-size: 9px; padding: 2px 6px; border-radius: 10px; text-align: center; font-weight: 700; }
.ab-v-green { background: rgba(34,197,94,.15); color: #22c55e; }
.ab-v-red { background: rgba(239,68,68,.15); color: #ef4444; }
.ab-v-gold { background: rgba(240,165,0,.15); color: #f0a500; }
```

### Verdict Card pattern (full-card version for /emas/)

```html
<div class="verdict-card" id="verdictCard">
  <div class="vc-head">
    <span class="vc-title">🧠 AGENTIC VERDICT</span>
    <span class="vc-confidence" id="vcConf">—</span>
  </div>
  <div class="vc-row">
    <span class="vc-label">Setup Quality</span>
    <span class="vc-val" id="vcSetup">—</span>
  </div>
  <div class="vc-row">
    <span class="vc-label">Risk:Reward</span>
    <span class="vc-val" id="vcRR">—</span>
  </div>
  <div class="vc-row">
    <span class="vc-label">Lot (1% risk)</span>
    <span class="vc-val" id="vcLot">—</span>
  </div>
  <div class="vc-row">
    <span class="vc-label">Worst-case</span>
    <span class="vc-val" id="wcRM">—</span>
  </div>
  <div class="vc-foot" id="vcFoot">Memuat turun...</div>
</div>
```

### Lot/position-size math (XAUUSD example)

```
acctRM = 10000
maxLossRM = acctRM * 0.01   // 1% rule → RM100
slDistPips = |p - sl| * 10  // $1 = 10 pips (2-decimal broker)
slDistRM_per001 = slDistPips * myrRateNum
lotSize = (maxLossRM / slDistRM_per001) * 0.01
```

Setup Quality heuristic: A+ = price within $5 of EMA20 and $10 of EMA50; A = EMA20 > EMA50 with 50 < RSI < 65; B- = RSI > 65 or < 35; B = otherwise.

## 3. Incremental Site Update Discipline

When asked to "update" an existing site:

1. **Read existing files first** with `read_file(limit=80)` then offset — never overwrite from scratch.
2. **Patch with `patch()` tool** using unique `old_string` + `new_string`. Do NOT use `write_file` to rewrite.
3. **CSS additions** go immediately before existing component CSS (e.g. `/* Verdict card — agentic */` block before `/* Quick stats */`).
4. **JS additions** go at end of `<script>` block, just before closing `</script>`. Wrap in IIFE if state is local.
5. **Verify all routes after** with `curl -sk -o /dev/null -w "%{http_code} %{size_download}b\n" <each_route>` — expected 200 for all.
6. **Update `llms.txt`** if the agent surface changed.
7. **Don't re-render from scratch** — the user already verified the existing layout. Only ADD intelligence, don't reorganize.

## 4. Site Classification (load-bearing decision)

Before editing a site, confirm classification:

- **Main site (arif-fazil.com):** React 19 + Vite, essays in `src/essays/`, build pipeline. Use `arif-sites-content-ops` original flow.
- **Standalone subdomain (syedos.*, wawabot.*, etc.):** Static HTML, no build, inline CSS/JS. Use this pattern.
- **Organ site (geox.*, wealth.*, well.*, aaa.*):** Substrate-anchored MCP-backed, edit via `arifos-organ-forging`. Do NOT touch via content-ops.

Mixing these flows (e.g. running `npm build` on syedos/, or editing arifos.* as if it's React) breaks the build/deploy and consumes cycles. Always identify the site class first.

## 5. Free Live APIs (verified working 2026-08-27)

For agentic banner data, no API key needed:

| Data | Endpoint | CORS |
|------|----------|------|
| XAUUSD spot | `https://api.gold-api.com/price/XAU` | * |
| XAG silver | `https://api.gold-api.com/price/XAG` | * |
| USDMYR FX | `https://open.er-api.com/v6/latest/USD` | * |
| Sovereign history | `https://arif-fazil.com/gold/api/history` (own domain) | needs auth |

Failed (rate-limited or JS-gated 2026-08-27):
- stooq.com — requires JS, no JSON API
- alphavantage — `demo` key throttled
- yfinance Python lib — not installed
- Yahoo Finance v7 quote — Too Many Requests

For Brent oil / DXY / US10Y: use TradingView widget cross-reference (free, no key) or note as "via TV widget" placeholder.
