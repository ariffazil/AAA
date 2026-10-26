# HERMES LOCAL REALITY GAP AUDIT

Date: 2026-10-23
Host: forge (af-forge, 100.64.0.2)
Observer: HERMES KVM8
Question (F13): what tools, plugins, apps or MCPs are needed for my agents, especially
HERMES, to be aligned with my actual reality -- Malaysia, food, events, gym reviews of an
area, local news, gossip -- anchored on One South Seri Kembangan (stay), KLCC (work),
Penang (kampung).

## Headline finding

The gap is not a shortage of tools. HERMES already carries 22 healthy MCP servers and six
independent web lanes (firecrawl, exa, brave-search, parallel-search, serpapi, zai_search),
plus a working key for SerpAPI that serves Google Maps local results.

The gap is two things:

1. NO HUMAN-LIFE LAYER. The existing `my-reality` skill covers institutional Malaysia only:
   prayer, weather, flood, FX, gold, quake, OPR, base rate. Nine adapters, all keyless, all
   verified. Not one of them answers "where do I eat" or "what is happening this weekend".
2. NO ANCHORED GEOGRAPHY. His three areas do not exist as objects anywhere in the system.
   No file says what One South is, what radius is walkable from it, what the commute to
   KLCC looks like, or which district weather reading actually applies.

## What was verified live today (keyless, HTTP 200)

| Source | Endpoint | Bytes | Use |
|---|---|---|---|
| MET district forecast | api.data.gov.my/weather/forecast | 613 for 2 rows | 29 districts |
| MET warning | api.data.gov.my/weather/warning | 15,265 | storms, rough seas |
| GTFS live bus | api.data.gov.my/gtfs-realtime/vehicle-position/prasarana?category=rapid-bus-kl | 10,332 | RapidKL positions |
| The Star | thestar.com.my/RSS | 200 | national news |
| Bernama | rss.bernama.com | 200 | national wire |
| Free Malaysia Today | freemalaysiatoday.com | 200 | independent news |
| SoyaCincau | soyacincau.com/feed | 200 | consumer/tech |
| Lowyat forum | forum.lowyat.net | 200 | community pulse |

Coverage note, and it matters: the MET feed carries 29 district names and does NOT include
Seri Kembangan or Kuala Lumpur by name. Any answer that quotes a district reading must say
which district was borrowed. That is the difference between a fact and a guess dressed as one.

## What is blocked from this host (named, not hidden)

| Source | Code | Meaning |
|---|---|---|
| malaymail.com/rss | 403 | bot wall -- use the firecrawl lane |
| burpple.com/kl | 403 | bot wall; Burpple is Singapore-first anyway |
| reddit.com/r/malaysia/.rss | 403 | needs OAuth or a proxy lane |
| eventbrite.com/d/malaysia--kuala-lumpur/events | 405 | it is a page, not an API |

## What is missing entirely

| Need | Status | What it costs |
|---|---|---|
| Food / gym discovery adapter | SerpAPI key PRESENT, no scripted adapter | one script, no new key |
| Events | nothing verified | Eventbrite API token, or firecrawl on listing pages |
| Local news ingest | 4 feeds reachable, no ingest, no dedupe | one script |
| Community pulse | Lowyat reachable, Reddit blocked | proxy lane, or accept Lowyat only |
| Transit adapter | GTFS reachable, not wired | one script; only vehicle-position works, trip-updates 404s |
| Area anchor files | none exist | three static files -- this is the highest value item |
| Halal status | nothing wired | JAKIM directory lookup |
| Google Places key | absent | not needed if SerpAPI stays funded |

## The freshness ladder (why gossip needs its own law)

Gossip rots in hours. Events rot in a day. Reviews rot in a quarter. News rots in a week.
Geography does not rot. Treating all five with the same "verified" stamp is how a local
system starts confidently telling him about a restaurant that closed in March.

Declared in `my-local-reality`: Event 24h, gossip 48h, review 90d, news 7d, place 180d,
anchor static.

## Forged this session

`my-local-reality` v1.0.0 -- /root/AAA/skills/domains/my-reality/workshop/my-domain-intel/my-local-reality/
7,397 bytes. Splits the human-life layer out of `my-reality` (which stays institutional and
gains a one-line pointer). Declares the three anchors, the verified table, the blocked table,
the freshness ladder, six hard rules, the built-vs-needed table, and a falsifier.

## Recommendation, in priority order

1. Anchor files first. Facts about his three places, written once, probed against maps. Everything else hangs off them. No API needed.
2. Food and gym adapter on the SerpAPI lane already paid for. Radius plus anchor plus review-age, never bare "best".
3. News ingest on the four working feeds, with a 7-day freshness tag and dedupe across the three national sources.
4. Events last, because it needs a token decision from him.
5. Never wire gossip without the 48-hour gate. Ungated gossip is the fastest way to make the whole local layer untrustworthy.

## Falsifier

If api.data.gov.my/weather/forecast or the SerpAPI key stops answering, this audit is stale.
If any local answer names a place without naming the anchor and radius, the answer is in breach.
