# MakcikGPT reading-flow & dead-stub repair (2026-08-14)

Scripts live in `sites/arif-fazil.com/scripts/` (repo root = /root/arif-fazil.com,
alias /root/arif-sites). All idempotent via HTML markers; re-run safe.

## 1. Article prev/next + related (kill the dead-end)

`node scripts/inject-article-nav.cjs` — injects `<!-- NAV-PREVNEXT v1 -->` block
(prev/next cards in date-desc reading order + up to 3 same-series "Baca juga")
before the footer of every full article. Order/series/titles come from the hub's
embedded `const ARTICLES=[...]` array in `public/makcikgpt-md/index.html`
(fullest ordered corpus; essays.json only holds 23 canonical pieces).

Rules baked in (each was a real bug):
- Hub array contains duplicate slugs AND same-title-under-two-slugs entries.
  Dedupe by slug for ordering, by normalized title for related, and exclude
  prev/next from related so no link ever repeats.
- Legacy essays (no `<footer>`, use `.footer-sig`) fall back to inserting
  before `</body>`. Five philosophical legacy essays are intentionally NOT in
  the hub array — they keep only their "← Semua Artikel" back link; that is
  correct, not a gap.
- Redirect pages (below) must carry NO nav: inject strips any prior block and
  skips files containing `REDIRECT-STUB v1`.

## 2. Dead stubs → redirects

Series-slug pages (m2-4, s3-4, s6-11 …) were placeholder stubs: `<article>` =
date + self-referential "Baca artikel penuh →" (dead loop), yet 200 + in
sitemap. 56 found. Fix pair:
- `node scripts/map-stub-redirects.cjs` — prints `{stubSlug: targetUrl}`.
  Resolution order: onsite non-stub sibling (exact then normalized-title then
  prefix-containment) → essays.json dest (onsite path or medium URL, matched by
  id or title) → SPA essays index (`src/data/essays/index.ts` slug+title,
  normalized) → hub fallback. Result 2026-08-14: 20 onsite, 9 /writing,
  27 medium, 0 fallback.
- `node scripts/fix-stub-redirects.cjs` — rewrites each stub to a
  `<!-- REDIRECT-STUB v1 -->` page: meta-refresh 0 + canonical + visible link.
  No Caddy change needed; humans and crawlers both land on real content.

## 3. Hub-array parsing pitfall (bit us twice)

Titles contain escaped quotes (`t:"\"Kekal Milik Penuh Malaysia\" — ..."`).
Naive `t:"([^"]+)"` silently drops those entries (84→69 parsed; 15 articles
lost their nav). Correct pattern:

  /\{s:"((?:[^"\\]|\\.)*)",d:"((?:[^"\\]|\\.)*)",u:"((?:[^"\\]|\\.)*)",t:"((?:[^"\\]|\\.)*)"\}/g

then unescape `\"` → `"` and `\\` → `\`. Any new script parsing the hub array
MUST use this.

## Verify

After any run: `grep -l "REDIRECT-STUB v1" public/makcikgpt-md/*.html | xargs
grep -l NAV-PREVNEXT | wc -l` must be 0; real-article nav count == full pages
in hub; then `rsync -a public/makcikgpt-md/ /var/www/html/arif/makcikgpt-md/`
and confirm one redirect + one full article in a real-Chrome-UA browser
(meta-refresh is NOT followed by `curl -L` — that is expected, not a bug).
