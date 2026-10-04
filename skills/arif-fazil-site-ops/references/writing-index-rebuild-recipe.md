# Writing Index Rebuild from .ts Source Data

**When:** The `/words/writing/index.html` listing surface needs a full rebuild — typically
after new essays are published, or when the index has accumulated duplicates/drift.

**When NOT:** When a single essay is being published (use the essay-publish recipe instead).

## Source data locations

| What | Path | Role |
|------|------|------|
| Essay .ts modules | `/root/arif-fazil.com/sites/arif-fazil.com/src/data/essays/*.ts` | Source of truth for direct-publication content |
| Essay catalog | `/root/arif-fazil.com/sites/arif-fazil.com/src/data/essays.json` | Series assignments, Medium URLs, Medium-linked essays |
| Live index | `/var/www/html/arif/words/writing/index.html` | What Caddy serves (backup before overwrite) |
| SPA source | `src/data/essays/index.ts` | React SPA essay registry |

## Step 1: Extract direct-publication essays from .ts files

Filter: `isDirectPublication: true` in the .ts file text body. Deduplicate by slug
(some slugs appear in multiple .ts files — e.g. `11-contrast-detection-...` and
`contrast-governed-...` share the same slug; first by filename wins).

Per .ts file, extract:
- `slug:` field (string literal)
- `title:` field (backtick string)
- `date:` field
- `excerpt:` field (backtick string)
- `tags:` array
- **First `<h2>` inside the HTML body** — this is the kicker text. Some essays use
  `class="paper-section-title"` on h2, some don't — just grab the first h2 regardless.
  Strip HTML tags from the content; collapse whitespace.

**Python extraction script pattern:**
```python
import re, glob
files = sorted(glob.glob('*.ts'))
seen = set()
for f in files:
    text = open(f).read()
    if not re.search(r'isDirectPublication:\s*true', text): continue
    slug = re.search(r"slug:\s*'([^']+)'", text).group(1)
    if slug in seen: continue
    seen.add(slug)
    title = re.search(r"title:\s*`([^`]+)`", text).group(1)
    date = re.search(r"date:\s*'([^']+)'", text).group(1)
    excerpt = re.search(r'excerpt:\s*`([^`]+)`', text).group(1)
    # First h2 in body
    m = re.search(r'<h2[^>]*>(.*?)</h2>', text, re.S)
    kicker = re.sub(r'<[^>]+>', '', m.group(1)).strip() if m else ''
    # Tags array
    m = re.search(r"tags:\s*\[(.*?)\]", text, re.S)
    tags = re.findall(r"'([^']+)'", m.group(1)) if m else []
```

## Step 2: Classify into series

Based on essays.json series assignments (not all essays have a series — some are SITE):

| Series | Label | Essays | Border color |
|--------|-------|--------|-------------|
| S4 | GOVERNANCE CANON | Aug 7 triptych (AGI Paradox, Truth Is Not Cheap, Third Axis) | gold |
| S6 | EUREKA TRILOGY | 3 contrast/AVO papers | iron |
| S8 | THE FORGE | MCP-era field notes (Tool, Fittest, Timelines, Big Bang) | iron |
| SITE | SITE ESSAYS | Everything else (i-hate-ai, mind-is-not, brazil, binatang) | iron |

Classification is semantic, not mechanical. The series IDs in essays.json (`S4`, `S6`, `S8`)
assign the direct-publication essays. Everything else goes to SITE.

## Step 3: Extract Medium-linked essays for the archive section

From `essays.json`: filter `dest.type === 'medium'`, deduplicate by title (same essay
appears under multiple series entries — e.g. S5#3 and S7#5 are both "Growing Intelligence
Without Losing Our Soul"). Sort newest-first.

The Medium archive section uses simpler cards (no kicker, no excerpt — just title, date,
series tag, and `↗ Medium` CTA with `target="_blank"`).

## Step 4: Render feed cards

**Direct-publication card pattern:**
```html
<a href="/words/writing/{slug}/" class="block border border-forge-iron hover:border-forge-red bg-forge-steel/20 rounded-sm px-6 py-5 transition-colors mb-3">
  <div class="flex flex-col sm:flex-row sm:items-baseline sm:justify-between gap-1 mb-3">
    <div class="font-mono text-[0.6rem] text-forge-red uppercase tracking-widest">WORDS · {SERIES} · SEALED 999</div>
    <time class="font-mono text-[0.65rem] text-forge-dim whitespace-nowrap">{DATE}</time>
  </div>
  <div class="font-mono text-[0.55rem] text-forge-orange uppercase tracking-widest mb-2">— {KICKER}</div>
  <h2 class="text-xl font-black uppercase tracking-tight text-forge-white leading-tight mb-2">{TITLE}</h2>
  <p class="font-body text-sm text-forge-orange/80 mb-4 leading-relaxed">{EXCERPT}</p>
  <div class="flex flex-wrap items-center gap-1.5">{TAG_PILLS}<span class="font-mono text-[0.65rem] text-forge-red ml-auto">Read article →</span></div>
</a>
```

**Medium archive card pattern:**
```html
<a href="{MEDIUM_URL}" target="_blank" rel="noopener noreferrer" class="block border border-forge-iron hover:border-forge-red bg-forge-steel/10 rounded-sm px-5 py-3 transition-colors mb-2">
  <div class="flex flex-col sm:flex-row sm:items-baseline sm:justify-between gap-1 mb-1">
    <div class="font-mono text-[0.6rem] text-forge-red/80 uppercase tracking-widest">Medium · {SERIES_ID}#{N}</div>
    <time class="font-mono text-[0.6rem] text-forge-dim whitespace-nowrap">{DATE}</time>
  </div>
  <h2 class="text-sm font-bold text-forge-white/90 leading-tight mb-1">{TITLE}</h2>
  <div class="flex flex-wrap items-center gap-1.5">{TAG_PILLS}<span class="font-mono text-[0.6rem] text-forge-red ml-auto">↗ Medium</span></div>
</a>
```

## Step 5: Page structure (9 components)

1. **Top bar**: ARIF FAZIL brand + nav HOME EARTH WORDS WORLD WORK
2. **Breadcrumb**: `/ › words › writing`
3. **Kicker + title**: `CONSTITUTIONAL ESSAYS · Ψ SOUL` + big italic `Writing`
4. **Description**: total essay count across all sections
5. **Stats pills**: count per series + date
6. **Zen pulse**: WHERE AM I? / WHY CARE? / WHAT NEXT?
7. **Filter chips**: 🔺 S4 · 🌊 S6 · 🔨 S8 · 🌍 Site · ↗ Medium Archive (5 chips)
8. **Feed sections**: S4 → S6 → S8 → SITE → Medium Archive
9. **Footer**: DITEMPA quote + byline (Muhammad Arif bin Fazil · Geoscientist · Architect, arifOS · Petronas Carigali · UW–Madison '13 · Penang, Malaysia) + MakcikGPT/Doctrine/feed.xml links + machine catalog

## Step 6: Deploy

The writing index is a **static HTML file** — no build step needed:
```bash
cp index.html /var/www/html/arif/words/writing/index.html
```

Verify: browser_navigate + browser_vision for visual parity, grep for unique markers.

## Pitfalls

- **Duplicate slugs across .ts files**: legacy + new essay files may share a slug. Always dedup.
- **Duplicate titles across series in essays.json**: Medium-linked essays appear under
  multiple series (S2#2 = S3#4 = "Agentic Intelligence Big Bang"). Dedup by title for
  the Medium archive section.
- **Kicker extraction varies**: some essays have `<h2 class="paper-section-title">`, some
  use bare `<h2>`. The regex `<h2[^>]*>(.*?)</h2>` handles both. Some kickers are section
  labels ("Section 1 — Acemoglu's Two Axes"), some are punchy ("The McDonald's Theory of
  Intelligence"). Both are acceptable — the rule is "first h2 inside body."
- **Tags array may be empty** in older .ts files that used a different schema. Don't fail —
  render empty tag row gracefully (no pills).
- **Duplicate cards**: the old index had S6 EUREKA Trilogy with 6 cards (duplicated) instead
  of 3. Rebuild from source to catch this.
- **SPA chrome**: the index MUST use `/_shared/design-system/tokens.css` and
  `/assets/index-Dte6gqTG.css`. These are the canonical design tokens for the SPA.
