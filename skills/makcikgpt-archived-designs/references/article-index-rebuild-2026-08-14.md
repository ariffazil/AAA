# Rebuilding the Landing ARTICLES array from live article files

Concrete recipe for the "adapt data binding, don't cp" step in the visual-recovery
workflow. When restoring the Primer Dark landing, the archived HTML hardcodes a
22-article `ARTICLES` array. The live site has far more article files — rebuild the
array from the live files instead of pasting the stale 22.

Verified 2026-08-14: 80 article files on disk (the task said "81" but the actual
count is 80 = `ls *.html | grep -v index.html | wc -l`). **Always derive the count,
never trust a stated number.**

## Where files live

- Articles: `/var/www/html/arif/makcikgpt-md/*.html`
- Landing: `/var/www/html/arif/makcikgpt-md/index.html` (exclude from the article list)
- Archived design: `git show 767596c:sites/arif-fazil.com/makcikgpt/index.html`

Article slugs fall into two families:
- **Editorial (civic journalism)** — descriptive slugs: `petronas-dna`, `searah-followup`,
  `anwar-jung-shadow`, `ai-johor-rakyat-2026`, `bangang-*`, etc.
- **arifOS essays** — numbered slugs: `s1-1` … `s9-2`, `m1-1` … `m5-4` (legacy).
  The `s*` files are English arifOS/AI-governance essays → M3. The `m1-*`…`m5-*`
  files are Malay editorial, one series letter per prefix.

## Metadata extraction (slug → title, date)

Titles come in **three formats**, so fall back in order:

1. `<title>X — MakcikGPT</title>` (older s-series) → strip trailing `— MakcikGPT`
2. `<title>MakcikGPT — X</title>` (editorial) → strip leading `MakcikGPT —`
3. Title is just the slug (some editorial files, e.g. `ai-johor-rakyat-2026`) →
   read the real title from `<h1 class="cover-title">` (strip `<br>` → space)
4. Also strip any trailing `| ARIF FAZIL` junk.

Dates come from **two sources**, in order:

1. `<time>YYYY-MM-DD</time>` (s-series files use this)
2. Malay byline text in editorial files: `6 Julai 2026` → map month name to `MM`
   (`Januari`→01 … `Disember`→12) and emit `YYYY-MM-DD`
3. Fallback `2026-01-01` if neither present (3 files this session had no date).

## Series classification (M1–M5)

**Filename prefix wins first** (highest signal), then keyword match, else default M3:

```python
series = 'M3'                                # default = Tech & Sovereignty
if   slug.startswith('m1-'): series = 'M1'   # Energy
elif slug.startswith('m2-'): series = 'M2'   # Governance
elif slug.startswith('m3-'): series = 'M3'
elif slug.startswith('m4-'): series = 'M4'   # Economy
elif slug.startswith('m5-'): series = 'M5'   # Politics
elif slug.startswith(('s1-','s2-',...,'s9-')): series = 'M3'  # arifOS essays
elif keyword match on (slug + title).lower():
    'searah'|'sarawak'|'bernama'|'harakah'  -> M2
    'petronas'|'exxon'|'hormuz'|'iran'|'suriname' -> M1
    'johor'|'harga'|'duit raya'|'salary benchmark' -> M4
    'bangang'|'anwar'|'dap'|'loke'|'chennah'|'syaitan' -> M5
```

Pitfall: keyword matching alone misfiled `m2-5` (Bila Senyum CEO PETRONAS…) as M1 and
`searah-senyum-media-suap` as M1 because "PETRONAS" appears in the title — but they are
SEARAH/governance stories. **Prefix check first** is what fixes this. `m2-*` must stay M2
even when the title mentions PETRONAS.

Resulting distribution (2026-08-14): M1=12, M2=14, M3=41, M4=4, M5=9 = 80.

## Output shape

URLs are `/world/makcikgpt/<slug>` (NOT `/makcikgpt/<slug>` — the archived 22 used the
old short path). BASE = `https://arif-fazil.com`. Emit the `ARTICLES` array as
`{s,d,u,t}` objects, sort by date desc for "Terbaru", and let the page JS compute
series counts + render (the archived JS already does `ARTICLES.filter(a=>a.s===k).length`).

The stats strip count is dynamic — set it to `len(articles)`, not a literal.

## Verification checklist (run after every write)

```bash
# 1. Live URL is served and >15KB
curl -sf -o /dev/null -w "HTTP:%{http_code} SIZE:%{size_download}\n" https://arif-fazil.com/world/makcikgpt/
# 2. Fractal canvas present
grep -c 'hero-canvas' index.html          # >=1
# 3. No forbidden chrome (5 Rein)
grep -c 'WHERE AM I\|WHY CARE\|WHAT NEXT\|Canonical landing:\|Source of truth:' index.html   # 0
# 4. Article count matches files
grep -o 's:"M[1-5]"' index.html | wc -l   # == ls *.html | grep -v index | wc -l
# 5. Stats strip count correct
grep -o '[0-9]*</b><span>Artikel' index.html
```
