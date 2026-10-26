---
name: rendered-surface-verification
description: "Use when a deployed page must match its template."
triggers:
  - "design aligned"
  - "make it look like the other pages"
  - "article renders differently"
  - "verify the page is live"
  - "published but looks wrong"
  - "stale count on the live page"
  - "bundle hash"
  - "200 but wrong content"
floor_scope: [F2, F4, F9, F12]
autonomy_tier: T1
---

# Rendered Surface Verification

Proving a deployed surface is the one you intended. The failure this skill exists to catch: every
URL answers `200`, the content is real, and the page is still not the thing you built — different
template, different lane, different generation of assets.

## Core law

**A `200` describes the hop that served it, not the document the reader got.**
Status codes answer reachability. Nothing about template, lane, or asset generation. Verification
of a rendered surface means answering three separate questions:

1. **Which file** answered? (same path can serve different documents per request header)
2. **Which lane** did you probe — the human lane or the machine lane?
3. **Is it the same template** as the rest of the surface?

A one-probe check answers none of them.

## Step 1 — establish which file answered

### User-Agent routing

A single path is routinely split by UA: crawlers and CLI agents get markdown/text, browsers get an
HTML shell. Consequences that bite:

- Verifying content with default `curl` measures the machine document and says nothing about the
  human page.
- **Headless browsers are themselves on the bot list** (`HeadlessChrome`). A DOM/screenshot probe
  silently measures the wrong surface and reports success on a page no human ever sees.

Override the UA before probing the human view:

```python
cdp('Network.enable')
cdp('Network.setUserAgentOverride',
    userAgent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36")
```

When a headless probe returns markdown, escaped text, or a document with no site chrome, that is
the tell — you are in the machine lane, not looking at a broken page.

### Duplicate serve roots

The same logical asset (`articles.json`, `llms.txt`, an article body) can exist in two serve roots,
with the routed one chosen per request. `ls` reads one root; `curl` reads the other.

Signature: **disk shows the new value, HTTP shows the old one, and it looks like an edge cache.**
Rule caching out first — grep every serve root for that filename before concluding the CDN is stale.

```bash
find /var/www -name '<asset>' 2>/dev/null | while read f; do stat -c '%y %s %n' "$f"; done
```

## Step 2 — probe the lane the human sees

Fetch twice and assert both are the expected documents: once with a browser UA, once with a
crawler UA. One green probe is not evidence about the other lane. Then confirm the rendered tree
in a real browser with the UA overridden — not just the HTML source.

## Step 3 — verify by computed style against a sibling

"Looks aligned" is not a test. Pick a known-good sibling on the same template and diff the rendered
properties. Relative comparison beats absolute assertions because it stays valid as the design
system evolves.

```js
(() => {
  const h1  = document.querySelector('h1');
  const h2  = document.querySelector('article h2, .article-section h2');
  const art = document.querySelector('article');
  const c = e => e ? getComputedStyle(e) : null;
  return JSON.stringify({
    title: document.title,
    h1: h1 ? [c(h1).textTransform, c(h1).fontSize, c(h1).fontFamily.split(',')[0], c(h1).color] : null,
    h2: h2 ? [c(h2).fontFamily.split(',')[0], c(h2).color, c(h2).borderBottomWidth] : null,
    bg: c(document.body).backgroundColor,
    maxw: art ? c(art).maxWidth : null,
    classes: [...new Set([...document.querySelectorAll('[class]')].flatMap(e => [...e.classList]))].sort()
  });
})()
```

Run it on the new page and on a sibling. Any differing value is drift. The **class vocabulary** is
the sharpest signal: an unfamiliar class name (`cover`, `fact`, `foot`) on a page whose siblings use
a different set means that page was authored outside the template, and no stylesheet defines the
stranger — it renders as flat prose.

## Step 4 — assert uniformity, not reachability

A generator that produces many pages from one template makes per-page `200` the weakest possible
evidence: a partial deploy leaves most pages correct and a few on a previous asset generation, and
every URL still answers `200`.

```bash
# one template must yield one hash across the corpus
for d in <corpus>/*/; do [ -f "$d/index.html" ] && md5sum "$d/index.html"; done \
  | awk '{print $1}' | sort -u | wc -l     # must be 1

# nothing may still name a retired asset
<grep the old hashed asset across live HTML> | wc -l     # must be 0

# every referenced asset must exist
<grep asset refs> | while read f; do test -f "<webroot>/assets/$f" || echo "MISSING $f"; done
```

Two hashes = partial deploy. Any page whose hash, byte size, or class vocabulary differs from the
sibling set was produced by a different path than the build you think you ran.

## Pitfalls

- **Hand-writing the served file instead of generating it.** The page renders, the URL is `200`, and
  it is the only page on the surface with that design. If the content lives in a source module plus
  a generator, edit the module and rebuild — a hand-written file in the webroot diverges at the next
  build and cannot be maintained. Diagnose it by the hash-outlier test above.
- **A build renames the asset hash, so every previously-deployed page now names a dead entry.**
  Shipping only the route you touched leaves the surface running two asset generations at once.
  After every build, sweep live HTML for the retired hash and republish each hit from the fresh
  build, then assert zero remain. Do not use `--delete`; republish in place.
- **Discovery files (`*.json`, `llms.txt`, sitemap, feed) are separate deploy targets from the page.**
  A page can be live and correct while the index that lists it is stale, so nothing finds it. Update
  and deploy discovery artifacts in the same pass, then re-probe the served copy.
- **A generator with a schema gate hard-fails, it does not degrade.** If a registry entry is marked
  sealed/published but lacks its required register or provenance block, the index generator throws
  and nothing downstream runs. Read the error and fill the entry — do not hand-edit the generated
  output to get past it.
- **Pre-existing gaps in unrelated surfaces are not yours to fix mid-task.** An asset-missing check
  will surface old breakage elsewhere on the site. Name it explicitly as pre-existing and out of
  scope; do not widen a content deploy into a repair of someone else's page.
- **Verify before announcing.** "Published" means: both lanes `200`, discovery lists it, the corpus
  is uniform, and the rendered style matches the sibling. Anything less is a draft.

## Close-out checklist

1. Browser-UA probe and crawler-UA probe both return the expected document.
2. Generated corpus is uniform (one template hash, zero retired-asset references).
3. Discovery surfaces list the item; served copy matches disk.
4. Computed-style parity against a known-good sibling, human lane, UA overridden.
5. Pre-existing defects reported as pre-existing, not silently absorbed.
