---
name: verified-portrait-sourcing
description: "Use when real photos of named people must be verified."
version: 1.0.0
author: arifOS federation (curator)
tags: [media, provenance, verification, portraits, dossier]
metadata:
  hermes:
    tags: [media, provenance, verification, portraits]
    related_skills: [sourced-media-delivery, person-dossier-from-public-sources, typst-pdf-report, visual-artifact-delivery]
---

# Verified Portrait Sourcing

Putting a face beside a name is a **factual claim of identity**, held to the same standard as a
biographical sentence. One wrong face under the right name is a defamation-class error, not a
cosmetic one — it cannot be un-sent and it destroys the credibility of every other fact in the
document.

Companion skills (externally owned, read them, do not edit): `person-dossier-from-public-sources`
for the roster/biography method, `sourced-media-delivery` for photo albums and outbound credit
rules, `typst-pdf-report` for PDF construction.

## When to use

- A dossier, brief, deck, or directory is requested "with their pictures".
- Several named people must appear in one document with consistent framing.
- Any time an image will be printed beside a person's name rather than sent on its own.

## Procedure

### 1. Build the roster first, with URLs

A portrait task starts as a roster task. Extract every name with its own profile URL and the
department/category it belongs to, then keep only the tiers that matter (senior/consultant/head).
Parse the listing as repeated cards, not via the site's global nav: split the HTML on the card
container, then pull name, position, credentials and href per card.

### 2. Climb the source ladder — institution's own pages before image search

1. **Leadership / management page.** Usually the only place with real headshots for office-holders,
   and the markup is clean: `<img src="..." alt="FULL NAME">`. Filter alt text against the roster
   and you get verified pairs for free. It covers the heads, not the whole senior list.
2. **News / media-centre page.** Filenames often carry the name (`Dr-<Name>-MM.webp`). Usable, but
   credit it as an event photo, not a portrait.
3. **The site's find-a-doctor / people listing page.** Distinct from individual profile pages; the
   listing sometimes serves a real per-card portrait with `alt` = the person's name. Check it before
   concluding a site publishes no photos.
4. **Specialist news outlets with structured metadata.** WordPress sites expose the media without
   scraping HTML:
   ```
   /wp-json/wp/v2/posts?search=<name>&per_page=10&_embed=1
   ```
   Read `_embedded['wp:featuredmedia'][0].source_url` and `.caption.rendered`. A caption that names
   the person and their role *is* the attribution — stronger evidence than a matching filename.

Image search engines are the weakest rung, not the first: the hit arrives with no caption, no date,
no identity guarantee, and the API may be quota-gated. Site-native structured data first.

### 3. Defeat the placeholder trap

Individual profile pages frequently serve a **shared placeholder** for everyone
(`COPYRIGHT-LOGO-*.png`, `DR-IMAGE-COPYRIGHT-LOGO-*`, `male.png`, `female.webp`). Every profile then
looks like it has a photo and a naive scrape reports "49 portraits found". Filter by filename and
count reuse: a file shared across N people is a placeholder, never a portrait. Report the real number.

### 4. Match captions on two name tokens, never the surname

Strip honorifics first (`DATO`, `DATUK`, `PROF`, `DR`, `SRI`, `SERI`, `HAJI`, `A/L`, `A/P`), then
require **at least two** remaining tokens in caption + url-decoded filename combined. A Malay
surname is often a patronymic shared by thousands; single-token matching pulls in a different,
better-known person and the article about *that* doctor looks exactly like a hit.

### 5. Verify visually, batched

```
montage -label '%f' *.png *.jpg *.webp -tile 4x3 -geometry 380x380+6+6 \
        -background white -fill black -pointsize 22 sheet.jpg
```

Read the sheet in one `vision_analyze` pass: per tile — how many people, portrait vs event vs group
vs text graphic, head-and-shoulders of one identifiable person (yes/no). Ask for any badge, masthead
or clothing text. Drop every tile that fails even when the filename or caption matched; the two
failures that survive filename matching are the **magazine/press cover** (right name printed on the
cover, still not a portrait) and the **podium or group shot**.

### 6. Render the gap honestly

No verified portrait → initials tile, and say so in the document's limits section. Never a stand-in
face, never a stock face, never a silent omission. "Six portraits were verifiable, the rest are
initials because the site hides every consultant photo behind a placeholder" reads as rigour; a
silent downgrade reads as an omission.

## Layout conventions (Typst)

- Uniform column regardless of source aspect ratio:
  `#image("ph_x.jpg", width: 30mm, height: 38mm, fit: "cover")`.
- Per-photo credit line under the image, ~6.4pt, not once in a colophon:
  `#text(size: 6.4pt, fill: rgb("#8c98a4"))[Foto: IJN]`.
- Initials fallback in the same slot:
  `#align(center + horizon)[#text(size: 19pt, weight: "bold", fill: rgb("#b9c3cc"))[AB]]`.
- Wrap each person's block in `#block(breakable: false)[...]` so a portrait is never stranded at
the foot of a page away from the paragraph it belongs to.
- Credit style: institution name for staff headshots, outlet + year for press photos.

## Rules that are not optional

- **No unverified face beside a real name.** The initials tile is the only acceptable stand-in.
- **Credit every photo individually.** No credit, no print. Unknown photographer → say unknown.
- **Never merge identities across sources.** Same role, same department, similar name is not the
  same person; two different people can share a patronymic.
- **Do not claim a photo exists because a page renders an `<img>`.** Read the src.
- **State the count.** In the artifact's limits section, name how many portraits were verifiable
  and why the rest are initials.

## Pitfalls

- Scraping a listing by splitting on the card class fails silently when the site changes the wrapper:
  assert the expected card count before trusting the parse, and fall back to a regex on the profile
  URL pattern (`/doctor/<slug>/`) when the count comes back zero.
- Vision descriptions of a face are not identity proof — they confirm *composition* (one person,
  portrait framing, no masthead text). Identity comes from the pairing on the page; the vision pass
  exists to reject the group/event/cover cases the pairing could not distinguish.
- A vision pass will sometimes "correct" a name it read off a magazine cover. Treat any name it reads
  as evidence about the *source image*, never as a reason to relabel your roster entry.
- Mixed extensions from one host (`.png` headshots, `.webp` press photos, `.jpeg` event shots):
  detect the real type from downloaded magic bytes rather than trusting the URL suffix.
- If the request says "one PDF with their pictures", the pictures are part of the deliverable, not a
  nice-to-have — deliver the verified subset inside the artifact and explain the remainder, rather
  than shipping the document and mentioning afterwards that photos were unavailable.
