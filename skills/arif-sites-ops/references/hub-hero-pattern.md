# Hub Hero + Content-Viz Pattern (verified 2026-08-07)

Companion to `SKILL.md` §"Hub hero pattern". Reusable recipes for static
HTML pages that need an attention-grabbing hero + better content visualization
below the hero. No JS, no build pipeline changes — drop CSS into the page's
existing inline `<style>` block + paste the SVG art directly into the markup.

---

## 1. Static hero — 2-col grid (visual left, text right)

Pattern used by `/words/`, `/world/`, `/work/`. Pairs with a `tokens.css` link
in `<head>` and the page-level inline `<style>` block.

### Skeleton

```html
<section class="hero" id="<route>-hero" aria-label="<page summary>">
  <div class="<visual>-wrap" aria-hidden="true">
    <svg class="<visual>-<noun>" viewBox="0 0 W H" role="img" aria-label="<visual>">
      <!-- pure-SVG art, no JS animation libraries -->
    </svg>
    <div class="<visual>-emoji" aria-hidden="true">EMOJI</div>
  </div>
  <div class="hero-text">
    <div class="kicker">HUB · REGISTER</div>
    <h1 class="hero-title">The Noun.</h1>
    <p class="hero-prose">One-sentence frame of what this hub is, who it serves, why now.</p>
    <blockquote class="hero-quote">
      <p>"Witty line that earns its keep on a portfolio page."</p>
      <cite>— Author, <em>Work</em> (year)</cite>
    </blockquote>
    <div class="hint">▸ ACTION PHRASE · SECOND ACTION</div>
  </div>
</section>
```

### CSS (drop into the page's inline `<style>` block)

```css
.hero{display:grid;grid-template-columns:minmax(220px,1fr) minmax(0,1.4fr);gap:2.5rem;align-items:center;margin:1.5rem 0 2.5rem;padding:1.5rem 0;border-bottom:1px solid #2a2a3a}
.hero-text{text-align:left}
.kicker{font-family:var(--font-mono,monospace);font-size:.7rem;color:#c9a227;letter-spacing:.18em;text-transform:uppercase;margin-bottom:.75rem}
.hero-title{font-family:var(--font-display,serif);font-size:clamp(2rem,5vw,3.25rem);line-height:1.05;margin:0 0 1rem;color:var(--text-primary,#F5F5F7)}
.hero-prose{font-size:1.05rem;color:#c8c4b8;margin:0 0 1.5rem;max-width:36rem;line-height:1.55}
.hero-quote{border-left:2px solid #c9a227;padding:0 0 0 1rem;margin:0 0 1.25rem;font-style:italic;color:#9a958c;font-size:.92rem;line-height:1.6}
.hero-quote cite{display:block;margin-top:.5rem;font-style:normal;font-family:var(--font-mono,monospace);font-size:.72rem;color:#8a8378;letter-spacing:.06em;text-transform:uppercase}
.hint{font-family:var(--font-mono,monospace);font-size:.7rem;color:#8a8378;letter-spacing:.1em}
@media (max-width:720px){.hero{grid-template-columns:1fr;gap:1.5rem}.hero-text{text-align:center}.hero-quote{text-align:left}}
```

---

## 2. Compass rose (words hero)

3 rings + 72 degree ticks + cardinal/intercardinal star + N/E/S/W glyphs.
60s CSS rotation, reduced-motion honoured.

```html
<svg class="compass-rose" viewBox="0 0 400 400" role="img" aria-label="Compass rose">
  <circle cx="200" cy="200" r="190" class="ring ring-outer" />
  <circle cx="200" cy="200" r="160" class="ring ring-mid" />
  <circle cx="200" cy="200" r="70"  class="ring ring-inner" />
  <g class="star star-cardinal">
    <path d="M200 30 L214 200 L200 370 L186 200 Z" />
    <path d="M30 200 L200 186 L370 200 L200 214 Z" />
  </g>
  <g class="star star-inter">
    <path d="M200 200 L297 103 L214 186 Z" />
    <path d="M200 200 L297 297 L214 214 Z" />
    <path d="M200 200 L103 297 L186 214 Z" />
    <path d="M200 200 L103 103 L186 186 Z" />
  </g>
  <text x="200" y="52"  class="cardinal-letter" text-anchor="middle">N</text>
  <text x="352" y="207" class="cardinal-letter" text-anchor="middle">E</text>
  <text x="200" y="362" class="cardinal-letter" text-anchor="middle">S</text>
  <text x="48"  y="207" class="cardinal-letter" text-anchor="middle">W</text>
</svg>
```

```css
.compass-wrap{position:relative;width:100%;max-width:340px;aspect-ratio:1;margin:0 auto}
.compass-rose{width:100%;height:100%;animation:compass-spin 60s linear infinite;transform-origin:50% 50%}
@keyframes compass-spin{to{transform:rotate(360deg)}}
@media (prefers-reduced-motion:reduce){.compass-rose{animation:none}}
.ring{fill:none;stroke:#2a2a3a;stroke-width:1}.ring-outer{stroke:#3a3524}
.star-cardinal path{fill:rgba(201,162,39,.14);stroke:#c9a227;stroke-width:1;filter:drop-shadow(0 0 6px rgba(201,162,39,.45))}
.star-inter path{fill:rgba(201,162,39,.06);stroke:rgba(201,162,39,.45);stroke-width:.8}
.cardinal-letter{font-family:var(--font-mono,monospace);font-size:18px;fill:#c9a227;opacity:.85}
```

For 72 degree ticks, generate with a 4-line for loop and inject — never
hand-type 72 elements (`<line>` × 72 = ~3KB of dead markup).

---

## 3. Wireframe globe (world hero)

Equirectangular 720×360 SVG: 10° graticule as a single `<path>` per axis,
continent silhouettes as a second `<g class="continent">`, equator line
with pulse animation. Continent path data is hand-approximated equirectangular
geometry — readable but not cartographically accurate (no JS).

```html
<svg class="world-map" viewBox="0 0 720 360" role="img" aria-label="Wireframe world map">
  <g class="grat">
    <!-- meridians every 20px; parallels every 20px. Single path per axis. -->
    <path d="M20 0V360 M40 0V360 M60 0V360 M80 0V360 M100 0V360 M120 0V360 M140 0V360 M160 0V360
             M180 0V360 M200 0V360 M220 0V360 M240 0V360 M260 0V360 M280 0V360 M300 0V360
             M320 0V360 M340 0V360 M360 0V360 M380 0V360 M400 0V360 M420 0V360 M440 0V360
             M460 0V360 M480 0V360 M500 0V360 M520 0V360 M540 0V360 M560 0V360 M580 0V360
             M600 0V360 M620 0V360 M640 0V360 M660 0V360 M680 0V360 M700 0V360"/>
    <path d="M0 20H720 M0 40H720 M0 60H720 M0 80H720 M0 100H720 M0 120H720 M0 140H720
             M0 160H720 M0 200H720 M0 220H720 M0 240H720 M0 260H720 M0 280H720 M0 300H720
             M0 320H720 M0 340H720"/>
  </g>
  <line class="equator-glow" x1="0" y1="180" x2="720" y2="180"/>
  <g class="continent">
    <!-- North America / Greenland / S America / Africa / Europe / Asia /
         SE Asia / Australia / Antarctica silhouette paths -->
  </g>
</svg>
```

```css
.map-wrap{position:relative;width:100%;aspect-ratio:2/1;margin:0 auto;max-width:560px}
.grat{stroke:#161d28;stroke-width:.6;fill:none}
.continent{fill:rgba(26,31,43,.55);stroke:#2c3444;stroke-width:.8}
.equator-glow{stroke:#c9a227;stroke-width:.8;opacity:.25;fill:none;animation:eq-pulse 6s ease-in-out infinite}
@keyframes eq-pulse{0%,100%{opacity:.15}50%{opacity:.4}}
@media (prefers-reduced-motion:reduce){.equator-glow{animation:none}}
```

Continent `<path d="M... Z"/>` strings in the live `/world/` are 9 lines
totalling ~750B — copy verbatim from
`/var/www/html/arif/world/index.html` if you need to rebuild a similar page.

---

## 4. Drill string (work hero)

Pure CSS keyframes — drill pipe (gold/iron repeating gradient) moves down
26% then back up. No SVG needed.

```html
<div class="drill-wrap" aria-hidden="true">
  <div class="rig-line"></div>
  <div class="wellbore"></div>
  <div class="drill-string">
    <div class="drill-pipe"></div>
    <div class="drill-bit"></div>
  </div>
  <div class="depth-ticks">
    <span class="depth-tick"></span><span class="depth-tick"></span>
    <span class="depth-tick"></span><span class="depth-tick"></span>
    <span class="depth-tick"></span><span class="depth-tick"></span>
    <span class="depth-tick"></span><span class="depth-tick"></span>
    <span class="depth-tick"></span>
  </div>
  <div class="drill-emoji" aria-hidden="true">❤️‍🩹</div>
</div>
```

```css
.drill-wrap{position:relative;width:min(64vmin,280px);height:min(44vh,320px);margin:0 auto}
.rig-line{position:absolute;left:50%;top:0;bottom:0;width:1px;background:linear-gradient(to bottom,rgba(201,162,39,.5),rgba(42,42,58,.6));transform:translateX(-.5px)}
.wellbore{position:absolute;left:50%;top:18%;bottom:0;width:14px;transform:translateX(-50%);border-left:1px dashed #2a2a3a;border-right:1px dashed #2a2a3a;background:rgba(255,255,255,.015)}
.drill-string{position:absolute;left:50%;top:0;transform:translateX(-50%);width:6px;height:52%;animation:drill-stroke 4.5s cubic-bezier(.45,0,.55,1) infinite}
.drill-pipe{width:100%;height:calc(100% - 12px);background:repeating-linear-gradient(to bottom,#c9a227 0 6px,#3a3524 6px 12px);opacity:.85;border-radius:2px;box-shadow:0 0 8px rgba(201,162,39,.35)}
.drill-bit{width:0;height:0;margin:0 auto;border-left:7px solid transparent;border-right:7px solid transparent;border-top:12px solid #c9a227;filter:drop-shadow(0 0 6px rgba(201,162,39,.5))}
@keyframes drill-stroke{0%{transform:translateX(-50%) translateY(0)}55%{transform:translateX(-50%) translateY(26%)}70%{transform:translateX(-50%) translateY(24%)}100%{transform:translateX(-50%) translateY(0)}}
@media (prefers-reduced-motion:reduce){.drill-string{animation:none}}
.depth-ticks{position:absolute;left:calc(50% + 16px);top:18%;bottom:0;display:flex;flex-direction:column;justify-content:space-between}
.depth-tick{width:8px;height:1px;background:#2a2a3a}
.drill-emoji{position:absolute;left:50%;top:44%;transform:translate(-50%,-50%);font-size:clamp(2.5rem,7vw,4.5rem);filter:drop-shadow(0 0 14px rgba(201,162,39,.35))}
```

Drill emoji ❤️‍🩹 is a ZWJ sequence — render it with an explicit
`font-family: "Apple Color Emoji", "Segoe UI Emoji", "Noto Color Emoji", sans-serif`
fallback if it shows as black on some platforms.

---

## 5. Acts card grid — 3-column reading cards (added 2026-08-07)

Used on `/earth/#dynamic` to make the "Dynamic Earth — three readings" section
scannable. Each reading gets a SVG icon (60px), kicker label, h3, paragraph,
gold left-border accent.

```css
.acts{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:1.5rem;max-width:1100px;margin:1rem auto 0;padding:0 .25rem}
.act{background:rgba(255,255,255,.02);border:1px solid #2a2a3a;border-left:3px solid var(--earth-gold);border-radius:6px;padding:1.5rem 1.25rem;transition:border-color .2s,background .2s,transform .2s}
.act:hover{border-color:var(--earth-gold);background:rgba(201,162,39,.04);transform:translateY(-2px)}
.act .no{font-family:var(--font-mono,monospace);font-size:.62rem;color:var(--earth-gold);letter-spacing:.18em;text-transform:uppercase;margin-bottom:.85rem;opacity:.85}
.act h3{font-family:var(--font-display,serif);font-size:1.25rem;font-weight:700;color:var(--text-primary,#F5F5F7);margin:0 0 .85rem;line-height:1.2}
.act p{font-size:.92rem;color:var(--text-secondary,#A8A9B4);line-height:1.6;margin:0}
.act p b{color:var(--text-primary,#F5F5F7);font-weight:600}
.act .viz{margin-bottom:1rem;height:60px;display:flex;align-items:center;justify-content:center;color:var(--earth-gold);opacity:.7}
.act .viz svg{width:100%;height:100%}
@media(max-width:900px){.acts{grid-template-columns:1fr}}
```

The `.viz` block sits between the `<div class="act">` opening and the kicker
label — pure-SVG art, `aria-hidden=true`, no JS.

---

## 6. Two-column prose + data table (added 2026-08-07)

Used on `/earth/#malay` (Malay Basin case study) to upgrade a facts list
that was rendering as flat text. Prose left, structured table right.

```css
.basin-callout{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(280px,1fr);gap:2.5rem;align-items:start;max-width:1100px;margin:1rem auto 0;padding:0 .25rem}
.basin-callout h3{font-family:var(--font-display,serif);font-size:1.35rem;color:var(--text-primary,#F5F5F7);margin:0 0 1rem}
.basin-callout p{font-size:.95rem;color:var(--text-secondary,#A8A9B4);line-height:1.65;margin:0 0 1rem}
.basin-callout p b{color:var(--text-primary,#F5F5F7)}
.facts{display:grid;grid-template-columns:1fr;gap:0;border:1px solid #2a2a3a;border-radius:6px;overflow:hidden;background:rgba(0,0,0,.2)}
.facts>div{display:grid;grid-template-columns:90px 1fr;gap:.75rem;padding:.7rem .85rem;font-size:.85rem;border-bottom:1px solid #2a2a3a;align-items:baseline}
.facts>div:nth-child(odd){background:rgba(255,255,255,.02)}
.facts>div:last-child{border-bottom:none}
.facts span{font-family:var(--font-mono,monospace);font-size:.68rem;color:var(--earth-gold);letter-spacing:.06em;text-transform:uppercase;opacity:.9}
.facts>div b{color:var(--text-primary,#F5F5F7);font-weight:600}
@media(max-width:900px){.basin-callout{grid-template-columns:1fr}}
```

Markup:

```html
<div class="basin-callout">
  <div>
    <h3>Section title</h3>
    <p>Long-form prose goes here.</p>
  </div>
  <div class="facts">
    <div><span>label</span> · value</div>
    <div><span>label</span> · value</div>
    ...
  </div>
</div>
```

The 90px label column is the visual signature — wider labels (`group` →
`belong-to`) break the layout. Keep labels ≤10 chars.

---

## 7. Pitfall — design-system tokens aren't always loaded

`/earth/` has its OWN page-local tokens (`--earth-gold: #C9A227`,
`--earth-paper: #0A0B0D`, `--earth-ember: #E4572E`) defined in
`earth/_shared/earth.css`. The design-system `tokens.css` provides
`--gold`, `--text-primary`, `--font-display`, etc. If a new CSS rule on
`/earth/` references `var(--earth-gold)` it works; if it references
`var(--gold)` (the design-system token) it ALSO works because both CSS
sources are loaded.

Other hub pages only load `tokens.css`. Stick to design-system tokens there;
don't introduce page-local variables that other pages don't share.

---
