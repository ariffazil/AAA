# Typography Unification Session — 2026-08-14

## What was done

Unified all 89 MakcikGPT article HTML files at `/var/www/html/arif/makcikgpt-md/*.html` to a single `<style>` block, stripping Tailwind class overrides.

## Canonical CSS (the one to use)

```html
<style>
:root{--bg:#0a0a0a;--bg-card:#111;--fg:#f0f0f0;--fg-muted:#9a9a9a;--red:#e0301e;--blue:#1f3fd4;--yellow:#f2b705}
body{background:var(--bg);color:var(--fg);font-family:"Newsreader","Georgia",serif;font-size:17px;line-height:1.65;max-width:680px;margin:0 auto;padding:48px 24px}
h1{font-family:"Cabinet Grotesk","Inter",sans-serif;font-size:clamp(24px,4vw,36px);font-weight:800;line-height:1.15;letter-spacing:-0.02em;margin:0 0 12px;color:var(--fg)}
h2{color:var(--yellow);font-size:1.3em;font-weight:700;margin:1.8em 0 0.6em}
h3{color:var(--red);font-size:1.15em;font-weight:700;margin:1.4em 0 0.5em}
p{margin-bottom:1em}
a{color:var(--yellow);text-decoration:underline;text-underline-offset:3px}
a:hover{color:var(--fg)}
blockquote{border-left:3px solid var(--blue);padding:10px 18px;margin:1.2em 0;background:rgba(31,63,212,0.05);border-radius:0 6px 6px 0;font-style:italic;color:var(--fg-muted);font-size:0.95em}
strong{color:var(--yellow);font-weight:700}
em{color:var(--fg-muted)}
hr{border:none;border-top:1px solid #2a2a2a;margin:1.5em 0}
ul,ol{margin-bottom:1em;padding-left:1.5em}
li{margin-bottom:0.3em}
table{width:100%;border-collapse:collapse;margin:1.2em 0;font-size:0.95em}
th{text-align:left;padding:8px 10px;border-bottom:2px solid var(--yellow);color:var(--yellow);font-weight:700;font-size:0.85em;text-transform:uppercase;letter-spacing:0.04em}
td{padding:6px 10px;border-bottom:1px solid #2a2a2a}
.footer-sig{margin-top:3rem;border-top:1px solid #2a2a2a;padding-top:1.2rem;font-family:'JetBrains Mono',monospace;font-size:0.7rem;color:#666;text-align:center;letter-spacing:0.04em}
.footer-sig .kicker{color:var(--yellow);font-weight:600;margin-bottom:0.4rem;display:block}
</style>
```

## Applied values (verified via Playwright getComputedStyle)

| Element | Value |
|---------|-------|
| body font-size | 17px |
| body line-height | 1.65 (28.05px) |
| body max-width | 680px |
| h1 | clamp(24px,4vw,36px) = 36px at 900px viewport |
| h2 | 1.3em = 22.1px, yellow |
| h3 | 1.15em = 19.55px, red |
| p margin-bottom | 1em = 17px |
| blockquote border | 3px solid blue + muted bg |
| table th padding | 8px 10px, yellow, uppercase |
| table td padding | 6px 10px |
| .footer-sig | 0.7rem, JetBrains Mono, centered |

## The Python script

Location: `/tmp/unify-articles.py`

Idempotent. For each `.html` (except index.html):
1. Removes ALL `<style>` blocks
2. Strips class attributes from `<body>`, `<article>`, `<h1>`, `<div class="site-frame...">`, `<header>`, `<nav>`, `<hr>` (Tailwind overrides)
3. Injects the single canonical `<style>` block before `</head>`

Re-run safe: produces identical output on re-run.

## The Tailwind-class override trap (critical pitfall)

85 of 87 articles had `<article class="font-body text-lg leading-relaxed text-forge-white/85 space-y-5 max-w-3xl">` which set `font-size: 1.15rem (18.4px)` via `tokens.css`, completely overriding the `<style>` body rule of `font-size: 17px`. The `<h1>` had `class="font-display text-4xl md:text-6xl font-black..."` which overrode the `<h1>` style rule to `60px` on desktop.

Simply adding a `<style>` block was NOT enough — the Tailwind classes take precedence. The solution was to strip ALL conflicting class attributes.

Detection: rendered `p` computed as 18.4px when it should be 17px, despite "new CSS" grep count being correct.

## Background regenerator trap

A `unify-makcikgpt-v2.cjs` script was running between passes, regenerating articles in the old template. Detected via `stat -c '%y %n' *.html` — files had `.97` second timestamps in bursts, indicating batch node processing.

## Pre-state summary (2026-08-14 16:38)

- h1: clamp(28px,5vw,42px) — too big
- h2: 1.4em (25.2px) — fine
- h3: 1.1em (19.8px) — barely different from 18px body
- body: 18px, line-height 1.7, max-width 720px
- p margin-bottom: 1.2em — too much whitespace

User complaint: articles cause eye strain, inconsistent sizes, text feels disconnected.

## Known follow-ups for future sessions

- The `tokens.css` at `/var/www/html/_shared/design-system/tokens.css` still loads and defines `--text-lg: 1.15rem`. As long as `text-lg` class is stripped from `<article>`, it doesn't interfere. But if a new article is generated without class-stripping, the override returns.
- The `/assets/index-Dte6gqTG.css` link is a dead reference (file doesn't exist) — cosmetic, no functional impact.
- `inject-article-styles.py` in skill `scripts/` directory still has the OLD CSS values (18px body, clamp(28px)). Should be updated to match the canonical values.
