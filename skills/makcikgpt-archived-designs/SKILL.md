---
name: makcikgpt-archived-designs
description: Git archive for arif-fazil.com MakcikGPT visual designs — Primer Dark (2026-07-31), original chat-interface (2026-06-30), 75dcd84 minimal essay page. Use when restoring previous visual standards, comparing current vs historical, or learning what good design looks like for this site. Includes the 5 Rein chrome-leak pattern + design-lint enforcement + the canonical visual-recovery workflow playbook.
version: "1.1.0"
tags: [arif-fazil, makcikgpt, archived, primer-dark, design-invariants, chrome-lint, visual-recovery, references]
---
# MakcikGPT Archived Designs — Visual Recovery Canon

Arif's `/world/makcikgpt/` visual standard drifted three times between 2026-06 and
2026-08 because every agent added "helpful" agent-chrome to the page (epistemic tags,
source-of-truth paths, zen-pulse "WHERE AM I?" cards, render-script paths, "Canonical
landing:" lines). Each addition was small. Combined, they turned a journalism brand
into a GitHub repo.

This reference is the recovery canon: **three archived visual states**, the commits
that produced them, and how to extract them when redesigning. The canonical playbook
for the full restore workflow lives in `references/visual-recovery-workflow-2026-08-11.md`.

## The three archived visual states

| State | Date | Commit | File | Visual | Use it for |
|---|---|---|---|---|---|
| **Original Chat Interface** | 2026-06-30 | `696f734` | `sites/arif-fazil.com/makcikgpt/index.html` | Chat UI with Makcik persona (gold/brown, DM Serif Display, `👵` favicon, persona badge, typing indicator, suggestion chips) | Persona-driven homepage (future — MakcikGPT chat product) |
| **Primer Dark Marketing** | 2026-07-31 | `767596c` | `sites/arif-fazil.com/makcikgpt/index.html` | Hero "Makcik Tanya. Kuasa Jawab." + stats strip + pull-quote + 5 series cards + search/filter + footer | **Current target.** Restore this for any redesign. |
| **Minimal Essay Page** | 2026-07-01 | `75dcd84` | `sites/arif-fazil.com/src/pages/EssayPage.tsx` | Simple hero with "Narrative · Ψ SOUL" + title + date/tags + body + Medium/direct badge + "← All Essays" | Restore `/words/writing/` essay page to its simplest form |

## Extracting the archived HTML

```bash
# Primer Dark landing (363 lines, 19.6KB)
git show 767596c:sites/arif-fazil.com/makcikgpt/index.html > /tmp/makcikgpt-primer-dark.html

# Original chat interface (early, ~300 lines, gold/brown palette)
git show 696f734:sites/arif-fazil.com/makcikgpt/index.html > /tmp/makcikgpt-chat.html

# Minimal essay page component (117 lines)
git show 75dcd84:sites/arif-fazil.com/src/pages/EssayPage.tsx > /tmp/essay-page-minimal.tsx

# Archived articles (e.g. PETRONAS DNA — full editorial HTML)
git show 767596c:sites/arif-fazil.com/public/makcikgpt-md/petronas-dna.html > /tmp/article-petronas-dna.html
git show 767596c:sites/arif-fazil.com/public/makcikgpt-md/chennah-bangang.html > /tmp/article-chennah-bangang.html
git show 767596c:sites/arif-fazil.com/public/makcikgpt-md/searah-kekal-milik-penuh.html > /tmp/article-searah.html
```

After extracting, open the file in browser (`file:///tmp/...`) and `browser_vision`
it for visual reference.

## Visual Recovery Workflow — extract, serve, screenshot, compare

**When the user says "current state is ugly" or "find the archive"** (Arif's
verbatim directive: *"Buruk. Aku x mau ni.. deep archive extraction"*), do NOT
redesign from the current state. The archived git version is the visual
contract — extract it, serve it locally, screenshot it, and compare.

### The 6-step workflow

```bash
# 1. Extract archived HTML to a working directory
mkdir -p /tmp/makcikgpt-archive
git show 767596c:sites/arif-fazil.com/makcikgpt/index.html > /tmp/makcikgpt-archive/index.html

# 2. Serve locally on a free port
cd /tmp/makcikgpt-archive && python3 -m http.server 8765 &
sleep 2
curl -sf -o /dev/null -w "HTTP:%{http_code} SIZE:%{size_download}\n" http://127.0.0.1:8765/index.html

# 3. browser_navigate + browser_vision for visual proof
#    → captures screenshot to cache/screenshots/
#    → vision model returns text description of the visual

# 4. Take a screenshot of the CURRENT (broken) state for comparison
#    → load https://arif-fazil.com/world/makcikgpt/ the same way
#    → user can now see BEFORE vs AFTER in their chat

# 5. Wait for explicit approval before mutating any generator or live file
#    → show both screenshots in the reply
#    → ask: "Ini ke yang hang nak restore?" or proceed if directive is clear

# 6. Once approved, swap the generator template (e.g. generate-makcik-index.cjs)
#    → adapt data binding (don't `cp` — data shape may have evolved)
#    → idempotent retrofitter for static HTML files (see inject-article-styles.sh)
#    → add DESIGN_INVARIANTS.md as SOT
#    → add design-lint.sh as auto-block, wired to prebuild
```

### Why this workflow matters

- **Don't redesign from current** — the current state is broken by definition
  if the user is complaining. Trying to "improve" from a broken baseline
  perpetuates the drift. The archived version IS the design contract.
- **Show before mutating** — Arif is visual (`gambar = real generated photo`).
  He decides from screenshots, not from prose descriptions. Always capture
  a screenshot of the archived state AND the current state before patching.
- **Local serve + screenshot > prose** — `git show` returns HTML text but
  rendered visual is what matters. `python3 -m http.server` + `browser_navigate`
  is the cheapest path to a screenshot.
- **Adapt data binding, don't cp** — the archived HTML has hardcoded
  article titles/dates. Copy the CSS/template structure, bind to current
  data source (e.g. `src/data/essays.json` via `getMakcikSource()`).

Full session reference: `references/visual-recovery-workflow-2026-08-11.md`.

## The Primer Dark design tokens (use these)

```css
:root {
  --bg: #0a0a0a;       /* near-black page */
  --bg-alt: #111111;   /* panel surface */
  --bg-card: #1a1a1a;  /* card surface */
  --bg-hover: #242424; /* hover state */
  --border: #2a2a2a;
  --fg: #f0f0f0;        /* primary text */
  --fg-muted: #9a9a9a;
  --fg-subtle: #666666;
  --red: #e0301e;      /* M1, energy, "where I am" badge */
  --blue: #1f3fd4;     /* M2, governance, "what next" */
  --yellow: #f2b705;   /* M3, sovereignty, "why care" */
  --body: 'Inter', sans-serif;
  --mono: 'JetBrains Mono', monospace;
}
```

The hero headline pattern (4-line color flow):
```html
<h1>
  Makcik<br>
  <span class="c-b">Tanya.</span>
  <span class="c-r">Kuasa</span>
  <span class="c-y">Jawab.</span>
</h1>
```

## The 5 Rein — agent-chrome that must NEVER appear in visual HTML

These exact strings, anywhere in a visual HTML file, will fail the build:

| # | Pattern | Why it's chrome |
|---|---|---|
| 1 | `Canonical landing:` | Internal SOT path leak |
| 2 | `WHERE AM I?` | Agent-nav card |
| 3 | `WHY CARE?` | Agent-nav card |
| 4 | `Source of truth:` | SOT leak |
| 5 | `Rendered by` | Ops leak |

Plus the soft-set (warnings, not blockers):
- `999 SEAL ·` repeated more than once per page
- `DITEMPA BUKAN DIBERI` more than once per page (footer only)
- Multiple consecutive breadcrumbs ending with `<strong>...</strong>`

Full rationale + the canonical visual contracts per surface:
`/root/arif-fazil.com/sites/arif-fazil.com/DESIGN_INVARIANTS.md`

## The chrome-lint enforcement

`/root/arif-fazil.com/sites/arif-fazil.com/scripts/design-lint.sh` scans every
`public/**/*.html` and `src/**/*.{tsx,ts,css}` for the 5 Rein + a wider forbidden
patterns list. Exit 1 on any violation. Wire to `npm run build` prebuild hook to
fail closed.

```bash
# Run manually
bash /root/arif-fazil.com/sites/arif-fazil.com/scripts/design-lint.sh

# Expected output
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
design-lint.sh · scanned 247 files
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ PASSED — no agent-chrome detected

# On failure
❌ FORBIDDEN CHROME: 'WHERE AM I?'
   file: public/world/makcikgpt/index.html
   line: 12,45,78
```

If you must add agent-facing metadata, put it in `<link rel="alternate" type="application/json" href="...">` or `<meta name="..." content="...">` — invisible to humans, available to agents. Never visible body text.

## When to use which archived design

| Task | Restore from |
|---|---|
| Landing `/world/makcikgpt/` redesign | `767596c` (Primer Dark) |
| Adding a new chat-like persona page | `696f734` (Chat Interface) |
| Stripping chrome from `/words/writing/` essay page | `75dcd84` (Minimal) |
| Recovering an article that was overwritten | `767596c` `public/makcikgpt-md/*.html` |
| Building a NEW surface with the Primer Dark palette | Use the tokens above |

## The 3-second human test

Every visual page must pass: within 3 seconds of landing, a human reader knows
**what this page is**, **why they should care**, and **what to do next** — without
reading any tag labels, source paths, or federation jargon. If the page fails this,
redesign it. Don't add disclaimers — fix the page.

## Visual contract cheat-sheet

### Landing — `/world/makcikgpt/`

```
[TOPBAR]   ← HOME · /WORLD/     🔴 SEAL 999 · 🟡 BM · 🔵 DATE
[HERO]     Makcik Tanya. Kuasa Jawab. (white→blue→red→yellow)
[STATS]    22 ARTIKEL · 5 SIRI · 999 SEAL · BM BAHASA MAKCIK
[QUOTE]    "Depa kata strategic partnership..."  — MAKCIK · seal 999
[TERBARU]  🔴 ● 5 latest, numbered 01–05
[SIRI]     🔵 ◆ 5 series cards (M1–M5)
[SEMUA]    🟡 ■ full article list with chip + date
[FOOTER]   ●● MAKCIKGPT · ARIF-FAZIL.COM · DITEMPA BUKAN DIBERI 🇲🇾
```

### Article — `/world/makcikgpt/<slug>/`

```
[COVER]    🧬 🇲🇾 🧬
           Cerita untuk Jiran-Jiran (yellow kicker)
           <H1>Title</H1>
           <subtitle>italic muted</subtitle>
           Oleh MakcikGPT, suara yang tanya "..."
           999 Meterai · Versi 1.0 Bahasa Makcik · <date>
[BODY]     Newsreader serif 17px, line-height 1.65, max-width 680px
           h1: clamp(24px,4vw,36px) Cabinet Grotesk sans
           h2: 1.3em (22px) yellow | h3: 1.15em (19.5px) red
           p margin-bottom: 1em (tight spacing)
           blockquote: blue left border 3px, muted bg
           strong: yellow emphasis | a: yellow underline
[FOOTER]   .footer-sig: JetBrains Mono 0.7rem, centered, muted
```

### Essay — `/words/writing/<slug>/`

```
[HERO]     Narrative · Ψ SOUL
           <H1>Title</H1>
           <date> · [tags]
[BODY]     forge-dark prose, max-w-3xl
[FOOTER]   ⚒️ Published directly on arif-fazil.com  ·  ← All Essays
```

## Article chrome — the inject pattern

Static articles in `/var/www/html/arif/makcikgpt-md/*.html` are produced by the
`prerender-articles.cjs` script which does NOT inject CSS. They render as
white-background default-browser HTML unless you inject a `<style>` block.

Use `scripts/inject-article-styles.sh` (in the site repo):

```bash
# Idempotent — only injects if "MAKCIKGPT ARTICLE — Primer Dark reader" sentinel isn't present
bash /root/arif-fazil.com/sites/arif-fazil.com/scripts/inject-article-styles.sh

# Output
✓ injected: petronas-dna.html
✓ injected: chennah-bangang.html
...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
inject-article-styles.sh · injected=82 · skipped=1 · errors=0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

The script injects the dark-mode CSS (Primer Dark palette, Newsreader serif body)
and Google Fonts link (`<link href="...Newsreader...">`) into every article's
`<head>`. The `index.html` is skipped (landing has its own styling).

**Idempotency sentinel:** the script checks for `MAKCIKGPT ARTICLE — Primer Dark
reader` in the file before injecting. Safe to re-run after regenerations.

## Why these archives matter

The 22-article landing had a clear visual identity at one point. Each subsequent
agent change was small ("just add a footer note", "just add a status indicator"),
but each served agents, not humans. The archived Primer Dark landing is the
"good" state. The chrome-leak pattern is what happened since.

Future agents must:
1. Read `DESIGN_INVARIANTS.md` before touching any visual HTML.
2. Run `design-lint.sh` before any commit to a visual surface.
3. If restoring an archived design, extract via `git show <commit>:<path>` and
   adapt the data binding — don't just `cp` (the data shape may have evolved).
4. When the user says "current state is ugly," do NOT redesign from current.
   Extract the archived good state, serve locally, screenshot, compare, then
   proceed with restoration. See `references/visual-recovery-workflow-2026-08-11.md`.
5. When the user shows frustration ("BANGANG", "Fix all", "Aku penat", "Go",
   "Pergi"), **ship action with terse acknowledgment — no philosophical
   preamble.** Show judgment, execute, report. The reflection was already in
   the user's question; he wants the answer, not a meta-analysis. Catch this
   BEFORE the user has to say "BANGANG." If reflection is needed, 1-2
   sentences max. Verified lesson 2026-08-11 (see Pitfalls below).

## MakcikGPT Writing Register — Zero Jargon Rule (F13 SOVEREIGN, 2026-08-14)

Arif explicitly corrected: *"Fail. I don't want any jargons at all. I want full reality human. No ai no arifos."*

**Every MakcikGPT article must pass the "makcik kampung test":** could your makcik
read this at the nasi lemak stall and understand every word? If not, rewrite.

### Forbidden words in article body (auto-fail):
FQ, arifOS, AI (unless natural Malay like "bukan AI"), proxy, KPI, Model
(as tech concept), drift, confident, bullshit, federation, constitutional,
entropy, thermodynamic, capability, agent, token, scalar, vector, metric,
measurement, organ, governance, sovereign, seal, forge, apex, quantum,
architecture, system, layer, framework, pipeline, ontology.

### Allowed register:
- Kampung analogies (nasi lemak, jiran, kebun, ibu, anak)
- Direct human experience (rasa, nampak, dengar, hidup)
- Short sentences. Paragraphs ≤ 3 sentences.
- Tables for comparison (kau bagi / kau dapat)
- Blockquotes for key insight
- No English paragraphs. Malay throughout. Single English words OK if natural.

### The article template pattern:
```html
<!-- Same CSS as article above -->
<h1>Title</h1>
<p style="...">Versi Makcik Kampung · date</p>
<hr>
<h2>Section heading (yellow)</h2>
<p>Content...</p>
<blockquote>"Key insight in one line"</blockquote>
<!-- ... sections ... -->
<div class="footer-sig">MAKCIKGPT · ARIF-FAZIL.COM</div>
```

### Article creation workflow:
1. Write HTML to `/var/www/html/arif/makcikgpt-md/<slug>.html`
2. Include: `<link rel="stylesheet" href="/_shared/design-system/tokens.css">`
3. Include inline `<style>` with Primer Dark CSS (or use inject-article-styles.py)
4. Add article to landing page ARTICLES array (JavaScript in index.html)
5. Run: `python3 /tmp/add_<slug>.py` (write script, run, verify)
6. Verify: `curl -sf -o /dev/null -w "HTTP:%{http_code}" "https://arif-fazil.com/world/makcikgpt/<slug>"`
7. Jargon scan: `grep -oinE '\b(FQ|arifOS|AI|proxy|KPI|...)\\b' <file> | grep -v 'font-family\\|tokens.css'`

## Pitfalls (verified 2026-08-11)

0. **Sacred geometry / hexagram ban (SCAR 2026-08-15).** Commit 12d1861
   ("Antigravity AI" / agy CLI) shipped a "Fractal Tripartite Geometry" SVG —
   two interlocking equilateral triangles in concentric circles = Star of
   David — into the MakcikGPT hero, and SEALED it `8/8 FULLY_ALIGNED · PASS`.
   For a BM civic-journalism brand this is brand-fatal. Rules:
   - No sacred-geometry figures (hexagram, enneagram, mandala rings) in any
     visual surface. "Fractal" is not a MakcikGPT voice.
   - Enforcement is now CANON: `verify-design-canon.cjs` check 7 (commit
     33a07bf) scans public/ + dist/ for >=2 large outlined polygons and fails
     the build. Do not remove that check.
   - When an agent self-reports `SEALED · ALL PASS` on visual work, verify
     with a real render before believing it — this agent's seal was prose,
     not evidence. (Reverted by sibling at 2392048 same day 14:22.)

1. **Philosophizing when the user wants action.** When user asks "What will
   happen if X" or "Fix all" or shows any frustration signal — they want a
   short verdict + action, not a multi-layer philosophical analysis. **The
   reflex to reflect is the most expensive mistake.** Catch it BEFORE the
   user has to say "BANGANG. Fix all." Default rule: state the verdict + the
   action + the result. Stop there. The user can ask for reflection if they
   want it.

2. **Redesigning from current state.** The current state is broken by
   definition if the user is complaining. Trying to "improve" from a broken
   baseline perpetuates the drift. The archived git version IS the design
   contract — extract it first via `git show <commit>:<path>`.

3. **`cp` of archived HTML.** Data shape evolves. Copy the CSS/template
   structure, bind to current data source. Never paste hardcoded values from
   an old commit.

4. **Skipping local serve + screenshot.** Arif is visual. He decides from
   images, not prose. `python3 -m http.server` + `browser_navigate` is the
   cheapest path to a screenshot.

5. **Single-pass restoration without lint.** Without `design-lint.sh` wired
   to prebuild, drift returns within weeks. The 3-layer defense (SOT +
   auto-block + recovery archive) is what locks the visual standard.

6. **Treating `git show` output as final.** It's text. The visual is what
   matters. Render with browser.

7. **Skipping the GitHub-protection pattern.** Before `write_file` to
   `/var/www/html/<site>/`, run `git ls-tree -r HEAD --name-only`. Live
   webroot can DIVERGE from git (verified 2026-08-11 on SyedOS — agent
   bulldozed a 5-card hub + gold chart assuming empty). Recovery:
   `git checkout HEAD -- .` + chown + chmod + probe ALL routes.

## Batch article unification (2026-08-14)

When articles drift from the canonical Primer Dark template (no nav, duplicate h1, old CSS), batch-fix with:

```bash
node /root/arif-fazil.com/sites/arif-fazil.com/scripts/unify-makcikgpt-v2.cjs
```

This script reads each `.html`, extracts body content, strips existing nav/header/metadata, and wraps in the canonical template. Handles: no-nav, no-article-tag, duplicate h1, old inline CSS, metadata paragraphs ("999 Meterai", "MakcikGPT article:") in body.

After running: verify all articles have nav with `grep -c 'header class="flex' /var/www/html/arif/makcikgpt-md/*.html | grep ":0$"` (should return empty).

## Canonical article typography (2026-08-14) — the one style block to use

Body 17px/1.65/max-680px; h1 `clamp(24px,4vw,36px)` Cabinet Grotesk; h2 1.3em+1.3em-yellow; h3 1.15em red; p margin-bottom 1em; blockquote 3px blue left border + muted bg; `.footer-sig` JetBrains Mono. This is the SOT — see the Visual contract cheat-sheet above for the exact blocks.

**Two traps when a `<style>` block exists but is ignored — both bit a 2026-08-14 typography unification run:**

1. **The Tailwind-class source of truth.** Inline Tailwind class attributes on elements override `/tokens.css` AND inline `<style>`. The canonical template (added by `unify-makcikgpt-v2.cjs`, ~85 articles) adds `class="font-body text-lg leading-relaxed text-forge-white/85 space-y-5 max-w-3xl"` to `<article>`, `class="font-display text-4xl md:text-6xl font-black..."` to `<h1>`, `class="bg-forge-black"` to `<body>`. `tokens.css` defines `--text-lg: 1.15rem` (≈18.4px) so body text renders **18.4px/serif/1.311**, completely overriding your `<style>` body rule → a 17px body font rule produces literally nothing. **You must strip the conflicting class attributes too**:
   - `<body class="...">` → `<body>`
   - `<article class="font-body text-lg leading-relaxed ...">` → `<article>`
   - `<h1 class="font-display text-4xl ...">` → `<h1>`
   - `<div class="site-frame max-w-4xl ...">` → `<div>`
   - `<p class="font-body text-lg ...">` (subtitle) → `<p>`
   - `<hr class="border-forge-iron...">` → `<hr>`
   Regex `re.sub(r'<article\b([^>]*?)class="[^"]*"([^>]*?)>', r'<article\1\2>', ...)` per tag. **Verify with a real browser render and `getComputedStyle()`** — `grep` on the class string tells you nothing about what CSS won. A `<style>` block can be present, 1 tag, "with new css" count correct, and STILL render wrong because classes override it.

2. **A background job regenerates the articles in the old template.** The full canonical template is emitted to the live webroot by `unify-makcikgpt-v2.cjs` (sometimes re-run by a parent agent/cron between your passes and mid-edit). Symptom: you fix 10 files, they look fixed, then some revert. Detection: `stat -c '%y %n' *.html` — regeneration timestamps cluster in whole-second bursts (e.g. `.97`, `.97`, `.97`). Mitigation: make the unification script fully idempotent (strip classes + inject style) and run it LAST, right before the render/verify step, then screenshot immediately.

See also:
- `arif-fazil-site-ops` skill — main site operations
- `references/typography-unification-2026-08-14.md` — session log with canonical CSS values, verified computed sizes, Tailwind override pitfall, and regenerator trap
- `/root/arif-fazil.com/sites/arif-fazil.com/DESIGN_INVARIANTS.md` — canonical design SOT
- `/root/arif-fazil.com/sites/arif-fazil.com/scripts/design-lint.sh` — chrome enforcement
- `/root/arif-fazil.com/sites/arif-fazil.com/scripts/inject-article-styles.sh` — article CSS retrofitter
- `/root/arif-fazil.com/sites/arif-fazil.com/scripts/generate-makcik-index.cjs` — landing generator (Primer Dark template)
- `references/visual-recovery-workflow-2026-08-11.md` — canonical playbook (extract → serve → screenshot → compare → restore → lint → wire)
