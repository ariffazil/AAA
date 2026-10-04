# Per-Essay Page Rebuild from .ts Source

**When:** A task asks to rebuild the per-essay pages under `/words/writing/<slug>/index.html`
(14 pages as of 2026-08-07 — listing lives at `index.json`, the per-slug pages are static
HTML siblings of `index.html`). Typically triggered by: "rebuild all writing article pages",
"regenerate essay HTML from source", or "match the EXACT footer block across all essays".

**When NOT:** When you only need to rebuild the LISTING (`/words/writing/index.html`) — use
`writing-index-rebuild-recipe.md` instead. When you are publishing a SINGLE new essay, use
`essay-publish-recipe.md` (which goes through the build pipeline, not a direct Python pass).

## The pattern (verified 2026-08-07)

The 14 per-essay pages are static HTML. The `.ts` files at
`/root/arif-fazil.com/sites/arif-fazil.com/src/data/essays/*.ts` hold:

| Field | Type | Used for |
|---|---|---|
| `title: \`...\`` | backtick string | `<title>`, `<h1>` |
| `date: 'YYYY-MM-DD'` | ISO date | `<time datetime=...>`, formatted display, `read_min` metadata |
| `slug: 'kebab-case'` | string | URL path, `meta description` truncation context |
| `tags: [...]` | array | Tag pills under byline |
| `excerpt: \`...\`` | backtick string | Lede paragraph under `<h1>` |
| `html: \`...\`` | backtick string (multi-line) | Article body — wrapped in `<article class="font-body...">` |
| `isDirectPublication: true` | optional flag | Filter signal — many `.ts` files have it; the rebuild should default to "direct" if missing |

A Python pass that extracts these fields with regex and emits one HTML per slug is the
fastest path for a wholesale rebuild.

## Template anatomy (per page)

```html
<!doctype html>
<html lang="en" data-ring="SOUL">
<head>
  <meta charset="UTF-8" />
  <title>{TITLE} — Arif Fazil | arifOS</title>
  <link href="https://fonts.googleapis.com/css2?family=Fraunces..." rel="stylesheet" />
  <link href="https://api.fontshare.com/v2/css?f[]=cabinet-grotesk..." rel="stylesheet" />
  <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,...Ψ..." />
  <link rel="stylesheet" href="/_shared/design-system/tokens.css" />
  <link rel="stylesheet" href="/assets/index-Dte6gqTG.css" />
  <meta name="description" content="{EXCERPT truncated to 280 chars}" />
  <link rel="canonical" href="https://arif-fazil.com/words/writing/{SLUG}/" />
</head>
<body class="bg-forge-black">
<div class="site-frame">
  <header>ARIF FAZIL | nav: Home Earth Words World Work</header>
  <a href="/words/writing/">← Writing</a>
  <div class="kicker">WORDS · {SERIES} · ENGLISH · SEALED 999</div>
  <h1 class="font-display text-4xl md:text-6xl font-black uppercase ...">{TITLE}</h1>
  <p class="font-body text-lg md:text-xl ...">{EXCERPT}</p>
  <div class="byline-row">
    <span>By Arif Fazil</span> · <span>Sealed 999</span> ·
    <time datetime="{DATE}">{DD Month YYYY}</time> · <span>{N} min read</span>
  </div>
  <div class="tag-pills">{TAG_PILLS}</div>
  <hr />
  <article class="font-body text-lg ...">{HTML_BODY}</article>

  <!-- EXACT footer block — DO NOT MODIFY -->
  <footer class="mt-16 pt-8 border-t border-forge-iron">
    <p><strong>Muhammad Arif bin Fazil</strong></p>
    <p>Geoscientist · Architect, arifOS · Petronas Carigali · UW–Madison '13</p>
    <p>Penang, Malaysia</p>
    <p>Published: {DATE_DISPLAY} · Direct Publication · /words/ context</p>
    <p>Epistemic Tag: INT — {EPISTEMIC_SCOPE}</p>
    <p>Pairs with: <a href="/words/writing/{OTHER_SLUG}/">{OTHER_TITLE}</a></p>
  </footer>
  <footer class="mt-6 pt-6 border-t border-forge-iron font-mono text-[0.6rem] text-forge-dim">
    <p>"Ditempa bukan diberi — Forged, not given."</p>
    <p>Published directly on <a href="/">arif-fazil.com</a> · Constitutional surface: <a href="/words/">/words/</a></p>
    <p><a href="/world/makcikgpt/">MakcikGPT</a> · <a href="/doctrine/">Doctrine</a> · <a href="/feed.xml">/feed.xml</a></p>
    <p>Agents: polite crawl, no mass-email, cite with rsl.xml. Do no harm.</p>
    <p><a href="/llms.txt">llms.txt</a> · <a href="/missions.json">missions.json</a> · <a href="/surfaces.json">surfaces.json</a></p>
  </footer>
</div>
</body>
</html>
```

The EXACT footer block is user-mandated — see the "footer doctrine" pitfall below.

## Pitfalls (every one fired during 2026-08-07 session)

### 1. The federation sync daemon overwrites your output mid-session

**Verified 2026-08-07 (cost: 30 min confusion).** The arifOS federation has a
`what-to-watch-daemon.py` (systemd) and several `.timer` units
(`federation-watchdog.timer`, `fed-sync.timer`, `arifflow-fq-mirror.timer`) that
**regenerate static HTML in `/var/www/html/arif/words/writing/<slug>/index.html` on a
short schedule**. Files you wrote at 08:29 can be silently overwritten by 08:31 with a
DIFFERENT structure (e.g. `<div class="mt-16 pt-8 border-t border-forge-iron">` instead
of `<footer class="mt-16 pt-8 ...">`, and a single `<footer class="mt-8 pt-6 ...">`
instead of the two-footer pattern).

**Detection:** `ls -la /var/www/html/arif/words/writing/<slug>/index.html` — if the
mtime is LATER than your last write and the content doesn't match your script's output,
the daemon overwrote you. Compare:
```bash
diff <(python3 your_script.py | head -200) /var/www/html/arif/words/writing/<slug>/index.html
```

**Mitigation:**
- Run the rebuild, then immediately run the verification script IN THE SAME TURN.
- If verification fails AFTER a clean run, the daemon is the prime suspect — re-run
  the rebuild + verification as a single chained command.
- For permanent safety, write the rebuild + verification as a single shell pipeline:
  `python3 rebuild.py && python3 verify.py` so they execute before the next timer tick.

### 2. Task spec count vs actual directory count

User said "rebuild ALL 17 writing article pages" on 2026-08-07. Actual count of article
directories under `/var/www/html/arif/words/writing/` was **14** (verified against
`index.json` `"count": 14`).

**Don't:** blindly trust the user's count and try to find 17 slugs.
**Do:** `ls -d /var/www/html/arif/words/writing/*/ | wc -l` and `grep '"count"' index.json`
to reconcile. Report the discrepancy in your summary — the user often knows the count
differently (e.g. including planned-not-yet-published slugs). Rebuild all that EXIST.

### 3. Source `<article>` wrapper stripping — varies per .ts

Source `.ts` files have THREE different outer wrappings around the article body:

| Pattern | Files |
|---|---|
| `<article>` ... `</article>` | 14-the-tool-is-the-thought, 19-the-tool-is-the-thought, 20-survival-of-the-fittest-tools, 21-three-timelines-one-boundary, 22-agentic-intelligence-big-bang, 14-i-hate-ai-i-hate-dsg-and-i-built-both-anyway |
| `<article class="scientific-paper">` ... `</article>` | 11, 12, 13, 18, 23, 24, 25, 26, growing-intelligence-..., contrast-governed-..., contrast-primitive-..., physics-constrained-... |
| Raw body (no wrapper) | 01, 02, 03, 04, 05, 06, 07, 08, 09, 10 (Medium-era `.ts` files) |

The template already wraps the body in `<article class="font-body ...">`. If the source
body ALSO starts with `<article>`, you'll get a nested `<article>` (browsers handle this
gracefully but it's malformed markup).

**Fix:** strip the outer wrapper before injection:
```python
body = re.sub(r'^\s*<article[^>]*>\s*', '', body, flags=re.DOTALL)
body = re.sub(r'\s*</article>\s*$', '', body, flags=re.DOTALL)
```

**Detection after generation:** `<article` count should be 1 (template) OR 2 (template + raw
`<article class="scientific-paper">` that the strip missed). If 3+, you have nested articles.

### 4. The `'13` year marker — Unicode apostrophe, not HTML escape

The byline footer says `UW–Madison '13` where `'` is U+2019 (right single quotation mark,
em-dash style), NOT `&#x27;` or HTML entity. The exact substring is `UW–Madison '13` —
when verifying, match against this literal Unicode form, not against `&#x27;13`.

**Caught this on 2026-08-07:** the first verification script used `&#x27;13` in the
expected-string and failed 14/14 files even though every file was correct. Switching to
the raw U+2019 made it pass instantly.

**General rule:** when writing verification scripts that grep for HTML output, paste
the EXACT byte sequence from the source file (or `od -c | head`) — don't trust your
fingers to remember whether `'` was HTML-escaped or not.

### 5. Kicker series classification is semantic, not mechanical

The kicker row (`WORDS · {SERIES} · ENGLISH · SEALED 999`) varies:
- `S8 · THE FORGE` — the MCP-era field notes (Tool is the Thought, Three Timelines, etc.)
- `SITE ESSAYS · CONSTITUTIONAL` — direct publications outside the Forge series (AGI Paradox, etc.)

There's no field in the `.ts` that tells you which. Build a hand-curated map from slug →
kicker series, defaulting to `SITE ESSAYS · CONSTITUTIONAL` when in doubt. Don't try to
parse `essays.json` series IDs — the static HTML rebuild runs WITHOUT the build pipeline,
so it's read-only on `essays.json`.

### 6. Pairs-with mapping is content-derived, not arbitrary

The footer's "Pairs with: <other-slug>" link must point to a SEMANTICALLY related article
in the same series (e.g. the AGI Paradox triptych cross-links each other; the AVO
trilogy cross-links each other). Build a hand-curated dict `slug -> (other_slug, other_title)`
that captures the canonical pairings. Default to a sensible generic (e.g. "The Tool Is
the Thought") if no good pair exists. Wrong pair-with is worse than no pair-with.

### 7. Estimating `read_min`

The task spec says `read_min` in the byline. Derive from word count:
```python
text = re.sub(r'<[^>]+>', ' ', html_body)
words = len(text.split())
minutes = max(1, round(words / 200))   # 200 wpm standard
```
Expect 5-30 min for these essays. Science trilogy hits 18-26 min; site essays 5-12 min.

### 8. Apostrophe / quote-entity cleanliness

The `html.escape()` call in Python uses default `quote=True` which escapes `'` → `&#x27;`.
This produces `Petronas&#x27;s Brazil` instead of `Petronas's Brazil`. For HTML body
content, this is technically correct (browsers render it identically), but the existing
on-site convention (set by `render-words-essays.cjs`) is to NOT escape apostrophes.
**Either way works** — be consistent within the rebuild pass.

## Verification recipe (post-rebuild)

Create a fresh `/tmp/hermes-verify-writing-rebuild.py` each run. The verification should:

1. Check 14 (or actual N) slugs × 2 locations = 28 files exist.
2. For each, grep for:
   - 12 head strings: `fonts.googleapis.com`, `api.fontshare.com`, `tokens.css`,
     `assets/index-Dte6gqTG.css`, `data-ring="SOUL"`, `rel="canonical"`,
     `<meta name="description"`, `ARIF FAZIL`, all 5 nav links
   - 21 body strings: `← Writing`, `SEALED 999`, `By Arif Fazil`, `Sealed 999`,
     `<time datetime=`, `min read`, `<hr class=`, `<article class="font-body`,
     `Muhammad Arif bin Fazil`, `Geoscientist · Architect, arifOS`,
     `Penang, Malaysia`, `Epistemic Tag:`, `<span class="text-forge-red">INT</span>`,
     `Pairs with:`, `Ditempa bukan diberi`, `Published directly on`, `/llms.txt`,
     `/missions.json`, `/surfaces.json`, `Agents: polite crawl`, `MakcikGPT`
   - 2 EXACT footer tags: `<footer class="mt-16 pt-8 border-t border-forge-iron">` AND
     `<footer class="mt-6 pt-6 border-t border-forge-iron font-mono text-[0.6rem] text-forge-dim">`
3. Confirm mirror == public (`diff -q` returns empty for all slugs).
4. Confirm `<article` count is 1-2 per file (template + optional scientific-paper inner).
5. Confirm file ends with `</html>` (clean EOF).

**DO NOT** use exact-string-match on substrings containing HTML-escaped Unicode unless
you've verified the source actually escapes them. Grep for raw U+2019 (apostrophe) or
use byte-level `od -c` to confirm.

## Live mirror vs public mirror (always double-write)

When the user says "mirror to /root/arif-fazil.com/sites/arif-fazil.com/public/...", the
second path is the SOURCE that the next `npm run build` will overwrite. Both paths must
be written in the same pass:

```python
for dest in (PUBLIC_DIR, MIRROR_DIR):
    d = os.path.join(dest, slug)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, 'index.html'), 'w') as f:
        f.write(page)
```

Verify with:
```bash
diff -rq /var/www/html/arif/words/writing /root/arif-fazil.com/sites/arif-fazil.com/public/words/writing
# Must return empty (no output = no differences)
```

If the diff shows drift, the mirror write failed silently (e.g. permission error on
/var/www/html/arif/). Re-write both and re-verify.

## Footer doctrine (user-mandated, do not paraphrase)

Two `<footer>` tags appear in EVERY essay:

1. **Bio footer** — `Muhammad Arif bin Fazil · Geoscientist · Architect, arifOS · Petronas Carigali · UW–Madison '13 · Penang, Malaysia · Published: <date> · Direct Publication · /words/ context · Epistemic Tag: INT — <scope> · Pairs with: <link>`

2. **Site footer** — `"Ditempa bukan diberi — Forged, not given."` + MakcikGPT/Doctrine/feed.xml links + llms.txt/missions.json/surfaces.json + Agents: polite crawl notice

These two footers MUST appear before the closing `</div>` (the `site-frame`). The exact
wording, ordering, and structure are Arif's preference — verified across the existing
essays and reinforced in `essay-publish-workflow.md`.

**Pitfall:** if you paraphrase ("forged not given" instead of "Forged, not given"), or
swap the order, or drop the "Agents: polite crawl" line — Arif will reject the rebuild.
Treat the footer as a literal byte template, not a guideline.
