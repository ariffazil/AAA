---
id: my-local-reality
name: my-local-reality
description: "Use when the sovereign asks about food, events, gyms, local news or neighbourhood reality in Malaysia. The human-life layer under my-reality: three area anchors (Seri Kembangan, KLCC, Penang), verified keyless sources, blocked sources named, freshness gate so gossip never outlives its window."
version: 1.0.0
owner: F13
risk_tier: low
floor_scope: [F2, F4, F6, F11]
autonomy_tier: T1
triggers:
  - "tempat makan"
  - "nak makan mana"
  - "restaurant near"
  - "event this weekend"
  - "event kl"
  - "gym review"
  - "gym dekat sini"
  - "local news"
  - "berita tempatan"
  - "gosip"
  - "kawasan aku"
  - "seri kembangan"
  - "one south"
  - "klcc"
  - "penang"
  - "my-local-reality"
verified_on: 2026-10-23
capability_tier: fed-agent-subagent
ecology_state: WARM
related_skills: [my-reality, web-ops, firecrawl, social-video-intelligence]
---

# my-local-reality — the human-life layer

> **Boundary:** `my-reality` owns *institutional* Malaysia (prayer, weather, flood, FX,
> gold, quake, OPR, base rate). **This skill owns the human-life layer** — where to eat, what
> is happening, what people say about a place. Do not merge them; do not duplicate the
> institutional adapters here.

## USE WHEN

1. He asks where to eat, which gym, what event, what is happening in an area.
2. He asks for news or gossip about somewhere he lives, works, or is from.
3. A brief needs a local pulse (his commute, his neighbourhood, his kampung).
4. An answer needs the *place* dimension that my-reality does not carry.

## DO NOT USE WHEN

1. The question is macro or institutional — use `my-reality` (BNM, MET, JPS, AlAdhan).
2. The question is about a named person's private life — that is a person claim, not local reality; use `governed-uncertainty`.
3. A number is required for a decision with consequence — local sources are REPORTED, not measured.
4. He asks for a review verdict on a business he might invest in — use `online-vendor-legitimacy-check`.

## The three area anchors (his actual geography)

| anchor | why it matters | precision available |
|---|---|---|
| **One South, Seri Kembangan** (43300, Selangor) | where he stays | district weather only; street level needs Places |
| **KLCC, Kuala Lumpur** (50088) | where he works | district weather; mall/office radius needs Places |
| **Penang** (kampung) | where he is from | state level; AlAdhan default already Penang |

**Rule:** every local answer names the anchor it was resolved against. "Near you" is not an
answer; "within 2 km of One South" is. If the anchor is ambiguous (Penang island vs mainland),
say which one you used.

## Verified sources (probed 2026-10-23 from KVM8, keyless)

| Layer | Source | Status | Notes |
|---|---|---|---|
| Weather, district | `api.data.gov.my/weather/forecast` | **200** | 29 districts. **Does not carry Seri Kembangan or KL by name** — nearest district must be resolved and named |
| Weather, warning | `api.data.gov.my/weather/warning` | **200** | storms, rough seas, valid_from/to |
| Transit, live | `api.data.gov.my/gtfs-realtime/vehicle-position/prasarana?category=rapid-bus-kl` | **200** | live RapidKL bus positions, ~10 KB |
| News, national | `thestar.com.my/RSS` , `rss.bernama.com` | **200** | keyless |
| News, independent | `freemalaysiatoday.com` | **200** | keyless |
| Tech/consumer | `soyacincau.com/feed` | **200** | keyless |
| Community forum | `forum.lowyat.net` | **200** | keyless, scraped |
| Places / food / gym | **SerpAPI (already held)** | **key PRESENT** | Google Maps local results through the `serpapi` MCP — no new key needed |
| Places, fallback | Foursquare Places | needs key | 500 free Pro calls/mo, then paid |
| Events | Eventbrite | 405 to plain GET | needs its API token, not a scrape |

## BLOCKED from this host (name it, do not pretend)

| Source | Code | What that means |
|---|---|---|
| `malaymail.com/rss` | **403** | UA/bot wall — use the firecrawl lane, not curl |
| `burpple.com/kl` | **403** | bot wall; Burpple is Singapore-first, KL coverage thin |
| `reddit.com/r/malaysia/.rss` | **403** | needs OAuth or a proxy lane |
| `eventbrite.com/d/...` | **405** | it is a web page, not an API |

A 403 is not "no data exists". It is "this lane is closed". Try firecrawl -> exa -> brave ->
parallel-search before saying a source is unavailable.

## The freshness ladder (this is the whole point)

Gossip rots fastest, then events, then reviews, then news, then geography. Tag every claim:

| class | max age before re-probe | why |
|---|---|---|
| Event | 24 h | an event that passed is misinformation |
| Gossip / forum | 48 h | a thread goes quiet; a claim goes stale in hours |
| Review / rating | 90 d | restaurants change chefs and close |
| News | 7 d for "current", else it is history | a headline is not a state |
| Place exists | 180 d | closures are silent |
| Geography / anchor | static | One South is still One South |

Never present a review as the current state of a business without saying when it was written.

## Hard rules

1. **Reported, not measured.** A Google or forum rating is REPORTED. It never becomes OBS, and it never grounds a decision with money or health consequence without a second source.
2. **No invented places.** If the probe returns nothing, say "no result in this radius". Never construct a plausible restaurant name. Fabricated local detail is the worst class of error because he can check it in ten seconds and lose trust in everything else.
3. **Name the radius and the anchor.** "Best nasi lemak" is not answerable. "Nasi lemak within 3 km of One South, sorted by review count" is.
4. **Gossip is a claim type, not a fact type.** Label it GOSSIP, name the venue, never attribute it to a named person without their own words.
5. **Halal is a certification, not a vibe.** "Muslim-friendly" in a review is not halal status. Authoritative source is JAKIM's directory; if unverified, say HALAL_STATUS_UNKNOWN.
6. **One source is a lead, not a finding.** Two independent sources, or label it single-source.

## What is genuinely missing (built vs needed)

| Need | Have | Missing |
|---|---|---|
| Food discovery | SerpAPI Google Maps lane | scripted adapter + radius/anchor resolver |
| Gym reviews | same | same, plus the 90-day review gate |
| Events | nothing verified | Eventbrite API token, or firecrawl on KL listing pages |
| Local news | 4 working RSS feeds | de-duplicating ingest + freshness tagger |
| Community pulse | Lowyat 200, Reddit 403 | proxy/OAuth lane for Reddit, or accept Lowyat only |
| Transit | GTFS realtime 200 | scripted adapter; trip-updates 404s, only vehicle-position works |
| Area profile | nothing | three anchor files as first-class objects (static facts, not API) |
| Halal | nothing wired | JAKIM directory lookup |

## Falsifier

If `api.data.gov.my/weather/forecast` stops returning 200, or the SerpAPI key is rotated out,
every row above marked verified is stale and must be re-probed before use. If a local answer
names a place without naming the anchor and radius that produced it, the answer is in breach.

## Changelog

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-10-23 | Initial forge. Splits the human-life layer out of `my-reality` (which stays institutional). Nine sources probed live; four named blocked; freshness ladder per class; three area anchors declared. |
