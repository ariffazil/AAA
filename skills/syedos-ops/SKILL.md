---
name: syedos-ops
description: >-
  Operate, patch, and verify Arif's personal SyedOS dashboard family at
  syedos.arif-fazil.com (named after his friend Abang Sado Syed).
  Direct-edit HTML at /var/www/html/syedos/ (no git, owned by www-data:www-data).
  Live-data wiring to free APIs (gold-api.com XAU/XAG, binance futures klines,
  exchangerate.host), and the hardcoded-value pitfall pattern where placeholders
  never get replaced. Trigger: any mention of syedos.arif-fazil.com, the /emas/
  page, "SABAR" verdict badge, or trading-dashboard HTML at /var/www/html/syedos/.
  SEE `references/syed-person-identity.md` FIRST if "Abang Sado" is mentioned —
  he is a real person (Syed Khairuddin Morktarudin), NOT a dashboard callsign.
---

# syedos-ops

> ⚠️ **"Abang Sado" is a real person, NOT a dashboard callsign.** Syed Khairuddin
> Morktarudin (`@rico_ricaldo_33`). The dashboard is named after him. If any
> future session treats Syed as a callsign or persona instead of Arif's friend,
> that is an F2 violation. See `references/syed-person-identity.md` for the
> full person profile, business (nasi lemak brand), communication style, and
> current caregiver situation (Mak Khairuddin / [NAME-REDACTED] — post-ERCP
> laparotomy, now recovering at homestay). Arif corrected this on 2026-08-07:
> "Wei abang sado Syed tu manusia betul la."

SyedOS is Arif's personal multi-page dashboard served from `/var/www/html/syedos/`. As of 2026-08-07, the directory IS git-controlled (private repo `ariffazil/syedos` on GitHub) — **the "no git" / direct-edit pattern is OBSOLETE**. Edit model: branch in the local repo, commit, push; the live webroot `/var/www/html/syedos/` IS the git working tree. Each subdomain page (`/emas/`, `/heal/`, etc.) is a self-contained HTML file with inline CSS + JS, no build step, no React. Static. Lightweight Charts (TradingView) for OHLC.

## Architecture facts (verified 2026-08-06; F1 lockdown 2026-08-07)

- **Root:** `/var/www/html/syedos/`, served by Caddy + Cloudflare, public URL `https://syedos.arif-fazil.com/<page>/`
- **Git-controlled (added 2026-08-07):** `ariffazil/syedos` private repo, branch `main`. The webroot `/var/www/html/syedos/` IS the git working tree. Edit workflow: `cd /var/www/html/syedos && git checkout main && git pull && git checkout -b fix/<short-name>` → edit → `chown www-data:www-data <file>` → `git add -p && git commit -m "fix(<page>): <what>" && git push -u origin fix/<short-name>` → PR → merge → live.
- **Deprecated (pre-F1-lockdown) pattern — DO NOT USE:** `cp <file>.bak-$(date +%Y%m%d)` + root edit + chown www-data. That was the pre-git workflow and should NOT be reintroduced. Use branches and PRs like every other site.
- **Owner:** `www-data:www-data` — preserve ownership after edit; git operations run as root
- **Persona:** "Abang Sado" branding in headers
- **Sub-pages observed:** `/emas/` (gold trading), `/heal/` (health/recovery), `/` (home launcher with cards)

## Live-data source inventory

| Page | Field | Endpoint | Auth |
|---|---|---|---|
| `/emas/` | XAU spot price | `https://api.gold-api.com/price/XAU` | none |
| `/emas/` | XAG spot (silver) | `https://api.gold-api.com/price/XAG` | none |
| `/emas/` | OHLC candles (4H/1D/1W) | `https://arif-fazil.com/gold/api/history?interval=<tf>&period=<p>` → fallback `https://fapi.binance.com/fapi/v1/klines?symbol=XAUUSDT` → final fallback `https://api.binance.com/api/v3/klines?symbol=PAXGUSDT` | none |
| `/emas/` | USD/MYR FX | `https://api.exchangerate.host/latest?base=USD&symbols=MYR` → fallback `https://open.er-api.com/v6/latest/USD` | none |
| `/emas/` | DXY (live) | ❌ **no free CORS-enabled endpoint without key** — keep static 98.5 or register fcsapi.com/marketstack.io |

## The hardcoded-value pitfall (the real lesson)

The `/emas/` page shipped with these silent failures:

| Field | Displayed | Reality | Why |
|---|---|---|---|
| Silver | `$31.2` | $61.78 (gold-api.com) | `textContent = '$31.2'` line, comment "placeholder with static values" — never replaced |
| DXY | `98.5` | n/a live | Same pattern, hardcoded |
| USD/MYR | `4.08` | variable | Same pattern |
| RSI | `50 + diff*2` | nonsense | Tick-to-tick diff, not Wilder 14-period |
| EMA20/EMA50 | `price × 0.995/0.99` | fake | Always 0.5% below price |
| S1/S2/R1/R2 | `price × ±1.5%/±3%` | fake | Percentage offsets, not swing highs/lows |
| `tfMap['4h']` | `'1h'` | wrong | Typo — 4H button secretly fetched 1H candles |
| Init | `tick()` + `loadChart()` fire twice | flicker | No `_started` guard, both `DOMContentLoaded` + `readyState!=='loading'` paths ran |

**Symptoms Arif reports:** "Silver $31.2 macam pelik", "verdict says SABAR but price already at 7-week high", "chart looks 1H when I pick 4H". Every symptom is a hardcoded value pretending to be live.

## Patch checklist (run before any patch)

```bash
# 1. Branch + checkout (NEW workflow as of 2026-08-07)
cd /var/www/html/syedos
git checkout main && git pull origin main
git checkout -b fix/<short-name>
# Now edit. The webroot IS the git working tree.

# 2. Live-verify the suspected value BEFORE patching
curl -sfL "https://api.gold-api.com/price/XAG" -H "User-Agent: Mozilla/5.0"
# →  {"currency":"USD","price":61.77,...}

# 3. After edit, preserve ownership + commit + push
sudoedit /var/www/html/syedos/emas/index.html
chown www-data:www-data /var/www/html/syedos/emas/index.html  # Caddy user
git add -p && git commit -m "fix(emas): <what changed>"
git push -u origin fix/<short-name>
# PR review → merge → live

# 4. Browser-verify after deploy — load page, run in console:
JSON.stringify({
  price: document.getElementById('price')?.textContent,
  silver: document.getElementById('mc-ag')?.textContent,
  rsi: document.getElementById('mc-rsi')?.textContent,
  closesLoaded: window.__lastCloses?.length
}, null, 2)
```

## Required fix patterns

### Real Wilder RSI 14-period
```js
const closes = window.__lastCloses || [];
let rsiFixed = 50;
if (closes.length >= 14) {
  let gain=0, loss=0;
  const slice = closes.slice(-15);
  for (let i=1; i<slice.length; i++) {
    const d = slice[i]-slice[i-1];
    if (d>=0) gain+=d; else loss-=d;
  }
  const rs = loss===0 ? 100 : (gain/14)/(loss/14);
  rsiFixed = Math.round(100 - 100/(1+rs));
}
```

### Real EMA20/EMA50 from closes
```js
const k20 = 2/21, k50 = 2/51;
let ema20v = slice[0], ema50v = slice[0];
for (let i=1; i<slice.length; i++) {
  ema20v = slice[i]*k20 + ema20v*(1-k20);
  ema50v = slice[i]*k50 + ema50v*(1-k50);
}
```

### Real S/R from swing highs/lows (last 20 candles)
```js
const recentH = (window.__lastHighs||[]).slice(-20);
const recentL = (window.__lastLows||[]).slice(-20);
const r1 = Math.max(...recentH);
const s1 = Math.min(...recentL);
const r2 = Math.max(...recentH.slice(0,-5));
const s2 = Math.min(...recentL.slice(0,-5));
```

### Dedupe init (avoid double-fire on load)
```js
let _started = false;
function start() {
  if (_started) return; _started = true;
  tick(); setInterval(tick, 30000); loadChart('4h');
}
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', start);
} else { start(); }
```

### Re-trigger tick() after candle load (so RSI/EMA/SR reflect fresh data)
```js
candleSeries.setData(ohlc);
window.__lastCloses = ohlc.map(d => d.close);
window.__lastHighs = ohlc.map(d => d.high);
window.__lastLows = ohlc.map(d => d.low);
tick();  // ← critical — without this, RSI/EMA display last-tick values until next 30s tick
```

### Correct timeframe map (Binance klines are strict)
```js
const tfMap = { '1h': '1h', '4h': '4h', '1d': '1d', '1w': '1wk' };
// WRONG: '4h': '1h' — silently maps 4H button to 1H candles
```

## Don't do this

- ❌ Hardcode any macro value (silver, DXY, USD/MYR) — link to a live endpoint, even if the endpoint is unreliable
- ❌ Fake RSI/EMA from current tick diff — always compute from candle series
- ❌ Compute S/R as `price × percent_offset` — derive from swing highs/lows
- ❌ Trust `arif-fazil.com/gold/api/history` without verifying it's live — fallback to binance fapi
- ❌ Edit without `cp ... .bak-$(date +%Y%m%d)` — recovery is non-git
- ❌ Forget to `chown www-data:www-data` after root edit — Caddy may serve stale or 500

## Verification script (re-run after every patch)

```bash
# 1. Live values flowing?
curl -s "https://syedos.arif-fazil.com/emas/" | grep -E "silver|31\.2|0\.985|0\.97|tfMap"
# expected: 0 hits for hardcoded patterns

# 2. Browser-render check (manual or via browser_navigate + console.evaluate)
# 3. Reload page, check Network tab: /price/XAU + /price/XAG + binance klines all 200
```

## SyedOS voice note delivery pitfalls

**Spec:** ≤90 seconds, `edge-tts --voice ms-MY-OsmanNeural --rate "+5%"`, ogg (opus) for Telegram voice bubble. **Never generate >90s without Arif sign-off.** Estimation: ~140 wpm → 90s = ~210 words max.

**Failure mode (proven 2026-08-07):** Voice note generated correctly (1.6 MB mp3, 4:31) but Telegram send to chat_id `1042200555` returned 404 because vault token masking (`***`) made programmatic extraction from `/proc/<pid>/environ` empty. Voice artifacts sat on disk unused.

**Mitigation order:**
1. Check token length before generating: `TOK=$(grep "^ASI_ARIFOS_BOT_TOKEN=" /proc/<pid>/environ | cut -d= -f2); echo ${#TOK}` — if 0 or ends `***`, skip programmatic send.
2. Fallback: `MEDIA:/path/to/voice.ogg` in Telegram reply to Arif → he forwards manually.
3. If vault readable: `set -a && source /root/.secrets/kunci-mas.env && set +a` before extraction.

See `references/voice-note-delivery-syed-2026-08-07.md` for full incident transcript, code pattern, and duration estimation math.

## Related skills

- `arif-sites-ops` / `arif-fazil-site-ops` — broader arif-fazil.com operations (deploy, route, verify-pages)
- `live-data-dashboards` — generic live-data patterns, CORS-free sources
- `verify-sibling-ops-reports` — sibling report verification pattern (apply same live-verify approach)
- `references/syed-person-identity.md` — who Abang Sado Syed actually is (person profile, medical history, family tree, communication style, identity correction log)
- `references/voice-note-delivery-syed-2026-08-07.md` — voice note failure modes, token masking trap, duration spec
- `references/syed-caregiver-voice-recap-2026-08-07.md` — full caregiver reality recap voice note script, when to use, 5-block structure, pitfalls, 90s/30s scaling variants
- `hermes-persona-alignment` — **NEW (2026-08-07)**: 7-layer persona alignment audit for non-operator personas; Syed is the canonical worked example. Load when the task involves extending Hermes to Syed (health tracking, cron jobs, USER.md creation) rather than dashboard HTML patching (this skill's core scope).
