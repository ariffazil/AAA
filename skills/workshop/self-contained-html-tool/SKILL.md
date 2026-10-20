---
name: self-contained-html-tool
description: "Use when shipping a tool as one HTML file."
version: 1.0.0
author: HERMES
license: proprietary
tags: [html, artifact, delivery, mobile, verification]
risk_tier: low
autonomy_tier: T1
metadata:
  hermes:
    tags: [html, artifact, delivery, mobile, verification]
    related_skills: [visual-artifact-delivery, human-facing-artifact-design]
---

# Self-Contained HTML Tool

One `.html` file, data embedded, no build step, no server, no internet — opens on a phone and
works. For a practitioner on a gym floor, in a shop, or in a car, this beats an app, a dashboard
and a deploy pipeline.

## When to Use

- The human wants "a tool" for someone who is not going to install anything.
- A dataset needs to be browsable/searchable rather than read end to end.
- The artifact has to survive being forwarded on WhatsApp and opened offline.

## Build shape

1. **Gather the data first and cache it to JSON on disk** (`data.json`), then generate the page
   from that file with a small Python script. Never hand-write records into the HTML; the next
   refresh must be a re-run, not an edit.
2. **Embed as `const DATA = <json>`** inside a `<script>` block. `json.dumps(..., ensure_ascii=False)`
   for non-ASCII text — escaping bites hardest on Malay and German.
3. **Translate at build time, not at read time.** Map every source-language label, direction and
   unit to the reader's language in the generator, then grep the built file for source words
   (`täglich`, `positiv`, `Belegt`) to prove nothing leaked through untranslated.
4. **Add the judgment layer yourself.** A score is raw material; the reader needs the decision.
   Classify each row into a handful of named action tiers and put the tiers on the filter chips —
   that is what turns a table into a tool.
5. **Vanilla JS only** — search input, chip filter, render function over `DATA`. No framework, no
   CDN, no fonts from the network.
6. **Carry provenance and the disclaimer in the footer**: source, retrieval date, what the score
   does and does not mean, and what the tool refuses to answer.

## Mobile gate — run before delivering

A CSS grid whose track is `1fr` does not shrink below its content's min-content width, so a card
with long unbreakable strings pushes the page wider than a phone screen.

- Track: `grid-template-columns: minmax(0, 1fr)` (and `repeat(2, minmax(0,1fr))` for the
  two-column breakpoint).
- Card: `min-width: 0; overflow-wrap: anywhere;`.
- Verify, do not eyeball:

```python
cdp('Emulation.setDeviceMetricsOverride', width=390, height=844, deviceScaleFactor=2, mobile=True)
print(js("document.documentElement.scrollWidth"), js("document.documentElement.clientWidth"))
cdp('Emulation.clearDeviceMetricsOverride')
```

Equal numbers = pass. Then on desktop confirm the grid really has two columns
(`getComputedStyle(el).gridTemplateColumns`) and that `document.body.scrollHeight` is sane.

## Functional gate

Open the built file with `file://`, then assert on real DOM output, not on intent:
card count equals the data length, each chip filters to the expected count, a search term returns
its row, and no console error. Print the first card's `innerText` — that catches a card that
rendered with empty fields, which a count check misses.

## Delivery

- Attach the file to the message; never point the human at a path under a temp or cache directory.
- Put the explainer in plain language: what it does, the Tier names, and the honest gap — "I did
  not add regional legality because I had no source I could stand behind, so it says so on the
  page".
- If it belongs on a site, copy it into the site's `public/` tree and say it is staged, not
  deployed, rather than deploying unasked.
