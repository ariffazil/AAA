---
name: curated-recommendation-lists
description: "Use when building a ranked watch/read list for someone."
version: 1.0.0
risk_tier: low
floor_scope: [F2, F9]
autonomy_tier: T1
tags: [curation, artifacts, evidence-basis, posters, html]
---

# Curated Recommendation Lists

> A recommendation list is a claim about a person, not a claim about a catalog. The list is only as
good as the evidence you had about them — so name the evidence before you name the titles.

## When this applies

"What should I watch / read / listen to", "what fits me", "build a list for me and for X", ranking
rails, taste profiles, gift lists, reading paths. One human or a pair. Output is usually an HTML
artifact in chat and, on request, a page on a site.

## Procedure

1. **Collect anchors before you rank.** Two or three titles (or authors, albums, places) the person
   actually chose. Ask for them in one short line if you do not have them; do not substitute
   reasoning about their job, industry, education or personality. One real title outranks a
   paragraph of plausible inference.
2. **Write the basis sentence before the list.** What the list was built from, how many anchors,
   and what it is not (no account data read, no platform telemetry). Put it near the top of the
   artifact, not in a footnote — a disclosure after 33 percentages arrives too late to do its job.
3. **Name the pattern, not the genre.** From the anchors, state the question the person is using
   fiction to ask ("can I understand someone who broke?"), then filter candidates on that. Genre
   labels collapse distinct appetites into one; a question survives.
4. **For a pair, build three rails: A, B, then shared.** The shared rail must pass both filters,
   which drops titles that are strong on one axis only. Expect it to read *better* than either solo
   rail — that is the extra constraint working, and worth saying out loud so it is not read as the
   solver contradicting itself.
5. **Attach one why-line per card.** The reason is what makes a list a recommendation rather than a
   dump. One sentence, with a concrete hook back to the anchor.
6. **Get metadata and posters from a public source, then store them.** TVMaze has a keyless API:
   `https://api.tvmaze.com/singlesearch/shows?q=<title>` returns name, premiered year, network,
   genres and `image.original`. Verify each hit is the right work before using it — the endpoint
   fuzzy-matches and will return a same-named programme from another country, and regional titles
   come back as the localised record instead of the original.
7. **Two asset modes, pick by destination.**
   - *Chat artifact (one file, opens offline):* downscale to ~300x450, JPEG q82 (~20-35 KB each),
     base64-inline into `src`. A few dozen posters lands around 1 MB — acceptable as a file.
   - *Site page:* keep the compressed JPEGs as real files under `public/img/<collection>/` and
     reference them by path. Inline base64 in a bundled SPA inflates the JS chunk for no benefit.
8. **Build the rails with rank numerals beside the poster**, a match badge, a platform badge, and
   the why-line under it. Horizontal scroll per rail; do not paginate.
9. **Verify by rendering, not by reading the code.** Load the artifact, then measure: card count,
   images with `naturalWidth > 0`, `document.body.scrollWidth` versus `innerWidth` (horizontal
   overflow), and the rank numeral's box versus its overflow container. Screenshot and eyeball at
   desktop and phone width.

## Pitfalls

- **Role-based taste inference is a guess wearing evidence's clothes.** "Works in geoscience, so
  likes documentaries" earns the question *based on what* — and once that question is asked, the
  list is already suspect. Label a guess as a guess, or ask for anchors first.
- **A match percentage has no denominator.** It is curator confidence on a scale you invented.
  Render it in a visually distinct language from any platform rating, and state its basis inside
  the artifact. `auditable-numeric-artifacts` carries the general rule on derived figures.
- **Never claim availability.** Label the platform by original network and say once that catalog
  varies by country and month; tell the reader to search the title if it is missing.
- **Rank numerals absolutely positioned inside a scroll container get clipped.** `overflow-x:auto`
  cuts anything placed left of the card; measure the numeral's `getBoundingClientRect()` against
  the rail's before declaring the layout done. Reserve real padding on the card instead.
- **`loading="lazy"` makes the image count lie.** Scroll to the bottom (or the target rail) before
  counting `naturalWidth > 0`, or you will report broken images that were only unrequested.
- **Duplicated data across two artifact formats is a maintenance trap.** When the same list must
  live both as a chat file and as a site page, keep one data module and generate both, rather than
  hand-editing two copies.
- **Do not put the recipient's name on the artifact as author.** A list built for someone is not by
  them; crediting them is an attribution error and it undercuts the "this is about you" framing.

## Delivery

- Chat: the artifact as a file plus one or two preview screenshots, and a short plain-language
  paragraph — the pattern found, the shared-rail explanation, and what you would start with.
  No methodology recital, no contents page.
- Site page: route + nav + static assets + sitemap, then verify live HTTP 200 on the new route and
  404 on a garbage path, and screenshot the live URL. When the page names a real person, their
  review comes before any third-party or public announcement.
