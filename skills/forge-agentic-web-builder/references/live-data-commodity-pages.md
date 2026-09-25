# Live-Data Commodity Pages — Recipe

> Class of page: a React component in the arif-fazil.com SPA that displays live API data from WEALTH (or any organ) with a static fallback. Used for the gold/oil/gas/klci/usdmyr terminals and any future "live signal" surface.
>
> Pattern proven on `/world/economics/gold/` patch 2026-09-25 — replaced hardcoded `$2,485.40` / SEAL / SOVEREIGN HEDGE with live ticker + APEX + 6-state regime + forecast cone + decision action guide, auto-refresh 60s.

## When to use

- The page is a SPA route inside `arif-fazil.com` (Caddy `@spa_routes` fallback → `/var/www/html/arif/index.html`).
- A live data feed exists at a documented endpoint (e.g. `/wealth/gold/api/ticker`, `/wealth/gold/api/apex`).
- The current page has hardcoded display values that have drifted out of sync with reality.
- The change is JS-rendered, NOT a new server-routed page. (If you need a new server route, this recipe is wrong — use OP 1 / OP 3 in SKILL.md instead.)

## Anatomy of a commodity page (the 6 mandatory fields)

Every live commodity page must surface, at minimum, these six values from the live ticker:

1. **price** — current spot
2. **change / changePct** — session delta
3. **signal** — short/medium directional bias from the engine
4. **confidence** — model's probability that the signal will resolve in the indicated direction
5. **support[] / resistance[] / pivot** — structural levels (3 of each, live)
6. **ema20 / ema50 / ema200 + emaTrend** — trend context

For non-trading pages (klci/usdmyr) the field set varies but the structure (live ?? static fallback) does not.

## Recipe

### Step 1 — Probe reality (probe-before-write)

Before editing, verify:
- What URL does the user actually hit? `curl -sI` it.
- What file does Caddy serve? `grep -B1 -A8 '<exact-path>\|@spa_routes' /etc/caddy/vhosts/arif-fazil.com.conf`.
- Is the page server-routed (specific Caddy `handle` block with `try_files`) or SPA-routed (`@spa_routes` fallthrough)? The answer determines if your patch is just `.tsx` + JS or requires Caddy too.
- Where is the React source? `find /root/arif-fazil.com -name '*.tsx' -path '*<slug>*'` — there is usually only one, often a generic `<Page>Commodity` rendered with a slug prop.
- What does the live API actually return? `curl -s <endpoint> | head -100`. Type it in TypeScript BEFORE you start writing display code.

**Never guess the live API shape.** The 2026-09-25 patch was rescued at this step — the API returned a much richer JSON than the previous static fields, and typing it first prevented three rounds of "field doesn't exist" errors.

### Step 2 — Backup and edit

```bash
cp -a src/pages/<Page>.tsx src/pages/<Page>.tsx.bak-<reason>
```

Edit patterns:

```tsx
// 1. Type the live response
type TickerLive = { price: number; change: number; changePct: number; ... };
type ApexLive = { state: string; direction: string; verdict: string; ... };

// 2. State with null initial + interval cleanup
const [ticker, setTicker] = useState<TickerLive | null>(null);
const fetchLive = useCallback(async () => { /* fetch + parse + setState */ }, [slug]);
useEffect(() => {
  fetchLive();
  const id = setInterval(fetchLive, 60000);
  return () => clearInterval(id);
}, [fetchLive]);

// 3. Live ?? static fallback at the leaf
const currentPrice = ticker ? `$${ticker.price.toFixed(2)}` : commodity.price;
```

### Step 3 — Build (no deploy)

```bash
cd /root/arif-fazil.com/sites/arif-fazil.com && npm run build
```

Note the new chunk hash from the output (e.g. `CommodityPage-BcuuLmdL.js 27.61 kB`).

Pitfall: `npm run build` runs `prebuild` scripts that regenerate agent shells, nav canon, feed, discovery, etc. These can fail independently and abort the build. If a prebuild fails, fix the failing script or accept the consequence — the SPA build itself is the last step (`tsc -b && vite build`).

### Step 4 — Surgical sync (no Caddy reload)

```bash
rsync -av --update \
  /root/arif-fazil.com/sites/arif-fazil.com/dist/index.html \
  /var/www/html/arif/index.html

rsync -av --update --delete \
  /root/arif-fazil.com/sites/arif-fazil.com/dist/assets/ \
  /var/www/html/arif/assets/
```

`--update` keeps untouched content alive; `--delete` on `assets/` is safe because that directory is owned by the build.

### Step 5 — Verify by content signature

```bash
curl -s https://arif-fazil.com/assets/<NewChunkHash>.js | grep -c '<distinctive-string-from-new-code>'
```

`grep -c` returning >0 is the deploy succeeded signal. Returning 0 means either:
- The chunk never uploaded (`stat /var/www/html/arif/assets/<NewChunkHash>.js` for mtime).
- Cloudflare is serving a stale chunk from a prior deploy (rare for fresh hashes; common for reused filenames).
- The build never emitted a chunk for your page (check `dist/assets/` directly).

ALSO verify the SPA shell, because updating assets without updating `index.html` leaves the user on a cached shell that never requests the new chunk:

```bash
stat -c '%y %n' /var/www/html/arif/index.html /var/www/html/arif/assets/<NewChunkHash>.js
```

Both mtimes must be in this session.

## Idioms

**Auto-refresh timestamp.** Render a "last updated HH:MM:SS · auto-refresh 60s" badge next to the verdict. The human reader can see freshness at a glance; you can see whether the fetch chain is alive without opening devtools.

**State badge with regime colour.** The badge is a small DOM element with a coloured ring; don't paint a full coloured panel for state. It reads as decoration. A single dot + state name in monospace is enough.

**Verdict pill, not verdict paragraph.** `LONG / SHORT / HOLD` is a single chip, not prose. The Dynamics section can be prose (and is — see below). The State section is a chip. The Action Guide is structured (entry/stop/target/RR/confluence/trigger/invalidation), not narrative.

**Forecast cone = 3 cards, not a chart.** For a 30-day horizon with no neural net, three percentile cards (P25 bearish floor / P50 median / P75 bullish ceiling) communicate the distribution better than a chart at this fidelity. The math: `sigma = ATR * sqrt(days)`; P25 = `price - 0.674*sigma`, P75 = `price + 0.674*sigma`. Honest disclosure: this is statistical sampling, not a trained forecast — say so in a footer line.

**Forecast contract — emit quantile horizons, NEVER fake future OHLC candles (2026-09-25, Syed's emas upgrade).** The 72-hour prediction request turned into the cleanest forecast contract: 3 horizons (+24h / +48h / +72h), each with P10/P25/P50/P75/P90 quantiles of the future CLOSE distribution, NOT 72 projected OHLC bars. A model cannot know future open/high/low/close of each hour — emitting fake candles presents false precision. The cone (quantile distribution of future close) is what statistical sampling can actually produce. The shape: `sigma_h = ATR_1h * sqrt(h)`; P25/P75 anchor at `price ± 0.674 * sigma_h`. **For any forecast page, the contract is always: N horizons × quantile bands, never N OHLC bars.** Also gate with `forecast_status: SHADOW` until walk-forward validation proves the model beats baseline (pinball loss / coverage / Brier skill). A `LIVE` label without calibration proof is the most common false-authority failure.

**Two output rails for mixed audiences — NEVER auto-translate (2026-09-25, Syed's emas directive).** When one surface serves both margin technical traders and physical-saver laypeople, do NOT funnel them through one stance. Emit two rails with separate vocabularies:

- **Trade rail** (margin technical): `LONG BIAS` / `SHORT BIAS` / `NO TRADE` / `EVENT RISK`. Entry zones, stops, RR. Defaults to `NO TRADE` when calibration is SHADOW.
- **Simpan rail** (physical saver / store-of-value): `SABAR` / `TUNGGU` / `JAGA` / `TAMBAH BERPERINGKAT`. Plain-language guidance, no entry/exit. Defaults to `SABAR` on regime uncertainty.

`LONG BIAS` does NOT translate to `TAMBAH BERPERINGKAT`. `SHORT BIAS` does NOT translate to "sell your physical gold". The horizon, the spread (broker vs physical dealer), the purpose (speculative vs store-of-value), and the XAU/MYR translation are all different. **Explicit `auto_translate_disabled: true` in any forecast config that serves both audiences.** A human-veto footer line ("Default sentiasa SABAR / NO TRADE melainkan calibration LIVE. Anda yang putuskan.") reinforces that stance is output, not instruction.

**Cross-origin when target vhost has no `/api/*` route (2026-09-25, Syed's emas).** The Syed vhost (`/etc/caddy/vhosts/syedos.arif-fazil.com.conf`) only handles `/upload*`, `/dashboard*`, and a catch-all `try_files` — there is NO `/api/*` reverse_proxy. Trying to call `/gold/api/ticker` from a page served at `syedos.arif-fazil.com` 404s because the catch-all falls through to nothing. The fix is **not** to add a Caddy route (T3 HOLD without Arif's explicit go signal); the fix is to **point the page at the canonical `https://arif-fazil.com/gold/api/*` instead.** Cross-origin works because the target already serves `Access-Control-Allow-Origin: *` and the source page's CSP `connect-src` includes `https://arif-fazil.com`. Build the page with a configurable `DATA_BASE` constant; when probing deployment, check both: (1) does the target vhost have an `/api/*` reverse_proxy? (2) does the source CSP allow `connect-src` to the alternative origin? If both yes → use the alternative origin. If the alternative origin isn't allowed in CSP, that's a separate site-deploy fix, not a page-build fix.

**Dynamics = 5 short bullets, not paragraphs.** Each bullet one observation + one implication. EMA distance. RSI state. Vol regime. Volume confirmation. APEX state. Five lines that an experienced trader reads in five seconds.

**Decision Action Guide = entry / stop / target / RR / confluence / trigger / invalidation.** Not "buy" or "sell". The guide describes the trade setup that WOULD be valid given the current state; the human decides whether to take it. If confluence < 0.3, the action column says `SABAR · HOLD` and the rest is `—`.

**Footer disclaimer (always).** "※ Not trading advice. Forecast is statistical ensemble from live ATR · confluence < 0.3 = no edge." One line, monospace, dim. Protects the page from being read as a trade recommendation.

## Pitfalls

- **Updating only `assets/` and forgetting `index.html`.** Browsers cache the SPA shell; without a shell mtime bump, the new chunk is never requested. Always sync both; verify both mtimes.
- **Live values bleeding into the static fallback.** If your static fallback is "BULLISH MANDATE" but live data could resolve to "HOLD", the visual jump on first fetch is jarring. Either make the static fallback say "LOADING" or render the verdict pill conditionally (`apexVerdict === 'LOADING'` until live arrives). Choose one; don't mix.
- **Ticker timestamp older than 5 min = stale.** Some live feeds return data minutes old under backpressure. Surface the timestamp; if it's stale, render a `STALE · last verified HH:MM` chip.
- **`fetch` CORS errors silently `.catch(() => {})`.** Convenient but hides real failures. Add a fallback log so the deployment can be diagnosed if a feed goes down: `console.warn('[gold] ticker fetch failed', err)`.
- **Live-data refresh creating render thrash.** `setInterval(fetchLive, 60000)` triggers a full re-render every minute. For dense pages this is fine; for pages with expensive children, wrap the live values in `React.memo` and pass only the changed fields.

## Anti-patterns

- ❌ Polling every 1 second — wastes network, doesn't add information, hammers the upstream API. 60s is the floor for retail-grade pages.
- ❌ Polling-based "live" with no `setInterval` cleanup — memory leak on SPA route change. Always `clearInterval` in the effect cleanup.
- ❌ Hiding the static fallback behind the live values — if the live API is down, the page should still render something sensible, not "undefined".
- ❌ Live values rendered without a timestamp — readers cannot tell whether the page is fresh or cached.
- ❌ Verdict pill that flashes between values on every refresh — gate the pill behind a debounce or only flip on regime change, not on every price tick.