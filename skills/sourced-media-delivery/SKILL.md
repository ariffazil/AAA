---
name: sourced-media-delivery
description: "Use when real web photos must be found, checked, sent."
version: 1.0.0
author: arifOS federation (curator)
license: private-sovereign
tags: [media, provenance, verification, delivery, image-search]
metadata:
  hermes:
    tags: [media, provenance, verification, delivery]
    related_skills: [refusal-sink-audit, shadow-mode, visual-artifact-delivery]
---

# Sourced Media Delivery

## When to Use

- He asks for *real* pictures from the web — not generated ones — of a subject, event, or type.
- Any time a discovered image will be shown, filed, or forwarded: the failure mode is not "couldn't
  find it", it is **claiming things about a photo you never actually read**.

## Procedure

1. **Discover with a real search API, not an eyeballed guess.** `EXA_API_KEY` (env or
   `/root/.secrets/kunci-root.env`); one natural-language query, ask for pages rather than raw CDN
   image URLs. Tier every hit by *domain* before by content: official federation / contest /
   organiser sites first, unknown blogs second (queue for review), explicit-adult domains never.
2. **Go one level deeper for real content.** Search hits are landing pages; the images live in the
   gallery. On contest and roster sites the event page lists each person as a profile link and each
   profile carries its own photo — that is how a *named* roster is built without guessing. Parse the
   event page for profile hrefs (`/<slug>/<id>/<person_slug>`), then pull each profile's own image.
3. **Probe that it is live.** A search result is a claim; an HTTP status is a measurement. Record
   status, final URL, `og:title`, `og:site_name`, author, published time. Only the measured status
   gets written down as "live".
4. **Read every candidate before sending it.** One `vision_analyze` call per image asking for the
   facts you need (how many people, sex, setting, attire, definition, quality). Drop anything the
   module refuses to describe, anything that is the wrong subject, anything blurry or a distant
   lineup. Sending a photo you could not read means vouching for pixels you never saw — and if he
   opens it and it is not what you said, the whole set loses credibility.
5. **Credit in the caption, on the first photo of the album.** Event, source, photographer. No
   credit, no send. If the photographer is unknown, say unknown rather than implying the site made it.
6. **Deliver as one album** with the bytes attached in the same request: multipart fields
   `chat_id`, a `media` JSON array where each item is `{"type":"photo","media":"attach://f1"}`
   (caption on the first item only), plus one `f1=@path.jpg` part per file. The bot credential lives
   in `/root/.secrets/hermes-telegram.env` and is read into the request by the script, never echoed.
   Keep the returned `message_id`s so a later retract has a handle, and say what you dropped and why
   — "aku buang enam, satu vision sendiri tolak" is a receipt, not a confession.

## Rules that are not optional

- **No hotness ranking of named real people.** "Siapa paling hot" gets a roster with what the
  physique/build actually reads as (division, frame, conditioning, symmetry) and which two stand
  out on craft criteria — the choosing stays with him. A ranking puts a verdict on a real body.
- **No body described from a headline.** A news article gives a name, not a physique. Say "name
  only, no photo verified" instead of inventing mass, height, or condition.
- **Never merge identities across sources.** Same face, different person is a real failure class
  (lighting, tan, dehydration, stage vs off-season).
- **Login-walled platforms are not sources.** Instagram/X/Facebook answer with walls from this host;
  ask for a screenshot instead of pretending a fetch worked.
- **Skip the aggregator blog.** Copy that writes desire onto uncredited photos of real people fails
  the credit rule twice: no photographer, and a third party's appetite attached to a named body.
  Use the gallery that names the shooter, and say why you skipped in one line — an editorial rule,
  not a moral one.

## Pitfalls

- Portfolio/photographer sites on the same template return wildly different image counts — one
  gallery yields fifteen images, the next yields zero. Count image URLs before promising a gallery,
  and fall back to the section index page when a named gallery is empty.
- Contest comps are often 600×900, not originals. If print quality is asked for, say so; never
  upscale silently and call it native.
- `publishedDate` from search APIs is frequently null even for dated galleries. Fill the date from
  the page probe, not from the search hit.
- Search-page HTML for login-walled sites is a consent interstitial, not the gallery. If the parsed
  image list contains only logos and sponsor banners, the scrape failed — say that, do not ship it.
- Repo-summary services (DeepWiki and kin) describe APIs plausibly and incompletely. For any
  integration, read the OpenAPI JSON or the source tree — never a summary.
