# Live Atlas page pattern (`/world/`) — Palantir-grade signal surface

Arif directive (2026-08-08): *"Can we improve the design of this landing sister for Worlds? We put real ATLAS OF THE WORLDS with dynamics signal palantir level?"*

The `/world/` index page is no longer a static Korzybski wireframe. It is a **live signal surface** with
SVG world map, pulsing hubs, scrolling ticker, dynamics strip, and a sidebar of macro/sovereign threads.
Old version backed up at `/tmp/index-v1.html` (8.5 KB). New version 38 KB single-file HTML.

## Page anatomy (top → bottom)

```
TOPBAR (sticky):    ARIF FAZIL · WORLD / ATLAS  | nav (HOME/EARTH/WORLD/WORDS/WORK) | MYT clock
TICKER BAR:        ▍ LIVE FEED  [BRENT $83.5 +1.4   HH-NAT $2.66 -0.01   GOLD $4339.8 +2.9 ...]  ← scrolls 60s loop
ATLAS STRIP:       "WORLD · WHAT IS HAPPENING · LIVE ATLAS"   "The Atlas of Worlds."  + Korzybski quote
                   ┌─────────────────────────────────────────┬───────────────────┐
ATLAS STAGE:       │                                         │  MACRO STACK      │
                   │         SVG world map (720×360)         │   DXY · US10Y     │
                   │         + 14 hubs (KL, Brent, JKM,      │   VIX · MYR       │
                   │         OPEC, Moscow, NY, Tokyo, …)     │   GSR · KLCI      │
                   │         + 6 trade flow lines            │  SOVEREIGN THERMO │
                   │         + scanline animation            │   RM82.8B · 70.5% │
                   │         + compass reticle               │   CFFO 85.2B      │
                   │         + placecard on hover            │   FCF-Zero $71.60 │
                   │                                         │  SIGNAL THREADS   │
                   ├─────────────────────────────────────────┤   8 rotating      │
                   │ DYNAMICS STRIP: BRENT  GOLD  JKM        │   alerts          │
                   ├─────────────────────────────────────────┤  OTHER WORLDS    │
                   │ COCKPIT CTA  +  /oil /gas /gold /klci /usdmyr                     │
                   │ MAKCIK GPT CTA                          │                   │
                   └─────────────────────────────────────────┴───────────────────┘
FOOTER:            DITEMPA BUKAN DIBERI
```

## Hub color & signal semantics

| Color | Meaning | Hubs |
|---|---|---|
| 🔴 `#ff5d5d` | Supply / OPEC / sanctioned flows | Riyadh, Abu Dhabi, Moscow, Caracas |
| 🟢 `#57d98e` | Oil / demand-side anchor | London (Brent), Shanghai |
| 🟠 `#ffb84d` | Mixed / sovereign / price source | NY (Henry Hub), Beijing, Singapore |
| 🔵 `#6aa8ff` | Capital / DXY | Frankfurt, Washington |
| 🟡 `#e8b64c` | Sovereign anchor (PETRONAS) | **Kuala Lumpur** — main hub, double pulse |
| 🟦 `#4ecdc4` | LNG / gas demand | JKM (Tokyo), Tokyo |

Pulse animation: `.pulse-hot` 2.4s ease-out (red/raw), `.pulse-cold` 3.2s (green/demand).

## Hub coordinates (the X/Y mapping)

These are **schematic** (not Mercator). The schematic trade-off is intentional — Korzybski lens,
not territory. Reuse these exact coordinates for any new hub; deviating breaks visual cohesion.

```js
const placePositions = {
  'hub-kl':    { x: 572, y: 208, dx: 14,  dy: -42 }, // Kuala Lumpur — PETRONAS
  'hub-jkm':   { x: 358, y: 98,  dx: 14,  dy: -28 }, // Tokyo — JKM
  'hub-brent': { x: 330, y: 83,  dx: -180, dy: -28 }, // London — Brent
  'hub-hh':    { x: 155, y: 98,  dx: -180, dy: -10 }, // New York — Henry Hub
  'hub-rud':   { x: 438, y: 148, dx: 14,  dy: -30 }, // Riyadh — OPEC+
  'hub-mow':   { x: 402, y: 78,  dx: -180, dy: -28 }, // Moscow
  'hub-chn':   { x: 625, y: 135, dx: 14,  dy: -10 }, // Shanghai
  'hub-jpn':   { x: 675, y: 115, dx: 14,  dy: -10 }, // Tokyo
  'hub-sgp':   { x: 582, y: 215, dx: 14,  dy: -10 }, // Singapore
  'hub-auh':   { x: 446, y: 155, dx: 14,  dy: -10 }, // Abu Dhabi
  'hub-dca':   { x: 148, y: 108, dx: -180, dy: -10 }, // Washington
  'hub-fra':   { x: 358, y: 92,  dx: 14,  dy: -10 }, // Frankfurt
  'hub-ccs':   { x: 178, y: 178, dx: 14,  dy: -10 }, // Caracas
  'hub-bjs':   { x: 600, y: 105, dx: 14,  dy: -10 }, // Beijing
};
```

## Live data wiring (vanilla fetch, no D3, no CDN)

```js
const subs = [
  { elem: 'oil',   url: '/oil/api/ticker',  prefix: 'XBRENT',  sym: 'BRENT',  dec: 1 },
  { elem: 'gas',   url: '/gas/api/ticker',  prefix: 'XNATGAS', sym: 'HH-NAT', dec: 2 },
  { elem: 'gold',  url: '/gold/api/ticker', prefix: 'XAU',     sym: 'GOLD',   dec: 1 },
];

async function sync() {
  const fetched = await Promise.all(subs.map(s => fetchSnapshot(s)));
  // 1. Update ticker tape (3-line scroller, doubled for seamless loop)
  paintTicker(entries);
  // 2. Update dynamics strip (BRENT/GOLD/JKM big numbers + RSI thermostat bars)
  // 3. Update macro stack from gold.macro (dxy, us10y, vix, usmyr, silver → gsr)
}
sync();
setInterval(sync, 30000); // 30s refresh — same cadence as vitals
```

## Placecard (hover any hub)

```js
const placeCard = document.getElementById('placeCard');
const pcMeta = {
  'hub-kl':    { k: 'KUALA LUMPUR · PETRONAS', v: '2.4 Mboe/d', m: 'Net cash RM82.8B · φ 0.9299' },
  'hub-brent': { k: 'LONDON · BRENT', v: '$83.5', m: '+1.8% · master PETRONAS variable' },
  // … 12 more
};
// mouseenter → position absolute card relative to stage rect (which scales SVG to viewport)
el.addEventListener('mouseenter', () => {
  // placeCard.style.left = (pos.x * scaleX + pos.dx) + 'px'
  // placeCard.style.top = (pos.y * scaleY + pos.dy) + 'px'
  placeCard.classList.add('show');
});
```

## Signal threads (alert rotation)

```js
const alertPool = [
  { ts: 'BRENT', lvl: 'md', msg: 'XBRENT +1.8% · 30s lag' },
  { ts: 'GOLD',  lvl: 'lo', msg: 'XAUUSD neutral band · RSI 55.1' },
  { ts: 'DXY',   lvl: 'md', msg: 'DXY 99.60 · soft USD' },
  { ts: 'SEAL',  lvl: 'hi', msg: 'PETRONAS φ 0.9299 · TRIPWIRE' },
  { ts: 'JKM',   lvl: 'lo', msg: 'JKM -0.4% · HH premium soft' },
  { ts: 'FX',    lvl: 'md', msg: 'USD/MYR 4.090 · firmer' },
  { ts: 'GSR',   lvl: 'lo', msg: 'GSR 68.5 · gold/silver ratio' },
  { ts: 'KLCI',  lvl: 'lo', msg: 'KLCI 1,748 · +0.90%' },
  { ts: 'OPEC',  lvl: 'hi', msg: 'OPEC+ watch · Vienna meeting' },
  { ts: 'CFFO',  lvl: 'md', msg: 'CFFO RM85.2B · buffer +RM25.2B' },
];
setInterval(addAlert, 7000); // rotate every 7s, max 8 visible
```

Severity classes: `hi` (red, tripwire), `md` (amber, structural), `lo` (teal, observation).

## CSS design tokens (the dark palette)

```css
:root {
  --bg-deep:#07090d;   --bg-pane:#0e141d;   --bg-panel:#0b0f16;
  --line:#1c2634;      --line2:#263244;
  --ink:#d7e0ec;       --dim:#7c8b9e;       --faint:#4a586a;
  --gold:#e8b64c;      --gold-soft:#c9a227; --gold-pale:#5a4a1f;
  --green:#57d98e;     --teal:#4ecdc4;       --red:#ff5d5d;
  --amber:#ffb84d;     --blue:#6aa8ff;
  --signal-up:#57d98e; --signal-down:#ff5d5d; --signal-neutral:#7c8b9e;
}
```

Page chrome (topbar, ticker, panels, footer) is self-contained inline — no shared CSS file.
**Design constraint:** dark + gold accent only. If a sibling surface (e.g. `/propa/`, `/vitals/`)
imports this token set, it must match.

## Compass + scanline + corner brackets (chrome polish)

```svg
<g class="compass" transform="translate(660,140)">
  <circle r="22"/>
  <line x1="0" y1="-22" x2="0" y2="22"/>
  <line x1="-22" y1="0" x2="22" y2="0"/>
  <text x="0" y="-26" fill="#c9a227" font-size="9" text-anchor="middle"
        font-family="IBM Plex Mono, monospace">N</text>
</g>

<line class="scanline" x1="0" y1="0" x2="720" y2="0" stroke="#e8b64c" opacity="0.1"/>
<!-- CSS: @keyframes scan { 0% { transform: translateY(-180px) } 100% { transform: translateY(180px) } } -->

<!-- corner brackets via CSS pseudo-elements .atlas-corners::before/::after -->
```

## Multi-copy disk layout (same Rule 0 as `/world/vitals/`)

- Live: `/var/www/html/arif/world/index.html` (~38 KB)
- Old/baseline: `/var/www/html/arif/world/index.html.bak-*` (4 files dated 20260806/07)
- Temp backup during redesign: `/tmp/index-v1.html`
- Sibling copies: `/var/www/html/world/` (may not exist; if it does, `cp` to sync)

## Deploy + verification (same as vitals)

```bash
chown www-data:www-data /var/www/html/arif/world/index.html
chmod 644 /var/www/html/arif/world/index.html
curl -sI "https://arif-fazil.com/world/?cb=$(date +%s)" | head -3
```

Then `browser_navigate` + `browser_console`:
```js
JSON.stringify({
  ticker: document.getElementById('tickerTape')?.textContent?.substring(0, 100),
  dyn_brent: document.getElementById('dyn-brent')?.textContent,
  dyn_gold: document.getElementById('dyn-gold')?.textContent,
  m_dxy: document.getElementById('m-dxy')?.textContent,
  alerts: document.getElementById('alertThread')?.children.length,
  svgs: document.querySelectorAll('svg').length
}, null, 2)
```

Expect: ticker has BRENT + GAS + GOLD, dyn_brent/dyn_gold populated, m_dxy = 99.60,
alerts = 8, svgs = 1 (the map).

## What NOT to add (Pitfalls)

- ❌ **Don't add a build step.** Single-file HTML, inline CSS+JS, vanilla SVG. Any new "atlas-like"
  page on this site must follow the same one-file discipline.
- ❌ **Don't use D3 / Chart.js / any CDN library.** CSP is strict (`script-src 'self' 'unsafe-inline'`).
  Pure SVG only.
- ❌ **Don't add real-geo Mercator.** The schematic continents + abstract hub dots are the design.
  Arif's preferred lens, not territory (Korzybski).
- ❌ **Don't link to `/vitals/`.** Live cockpit is at `/world/vitals/`. The legacy `/vitals/` 308s to
  `/propa/`. Use `href="/world/vitals/"`.
- ❌ **Don't add inline `<style>` for shared chrome.** Keep all tokens/chrome in the same `<style>`
  block at the top of the file.
- ❌ **Don't call `m.macro.dxy` etc. without a null guard.** The snapshot field can be absent on
  first-load before enrichment completes. Always check `if (m.dxy != null)`.
- ❌ **Don't fake the MYT clock with `new Date().getHours()`.** Use the helper `tick()` that
  computes UTC+8 from local TZ.

## Intent signals (when to reuse this pattern)

- Arif asks for "atlas", "live map", "palantir", "world dashboard", "signals"
- /world/ needs a redesign beyond prose cards
- A new arif-fazil.com landing wants hub-style nav (cyber-ops / trading floor aesthetic)