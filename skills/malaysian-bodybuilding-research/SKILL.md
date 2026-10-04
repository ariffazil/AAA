---
name: malaysian-bodybuilding-research
description: Research Malaysian & SEA bodybuilding/physique athletes AND upcoming competition events — athlete results via TegapTV, federation categories, gym affiliations, identity reconciliation, social media discovery via coach tags, plus event calendar research across PCA/NPC/WFF/INBA/WNBF/ABBF federations.
tags:
  - bodybuilding
  - physique
  - malaysia
  - southeast-asia
  - competition-calendar
  - ifbb
  - npc
  - pca
  - research
---

# Malaysian Bodybuilding / Physique Athlete Research

## When to use
- User asks to research a Malaysian bodybuilding, physique, or "Body Smart" competitor
- Identifying an athlete seen in TegapTV footage or event photos (placings, tag numbers)
- Finding competition results, categories, gym affiliation, or social media for a Malaysian physique athlete
- Reconciling two different spellings/names that may be the same competitor
- User asks about Malaysian bodybuilding/physique federations, event calendars, or which shows are coming up
- Building a competition calendar or scouting upcoming Malaysian physique events

## Key sources (in priority order)
1. **TegapTV.com results pages** — tegaptv.com hosts "Full Results <Event> <Year>" posts with complete placings per category plus competitor **tag numbers** (e.g. "Mohd Khairuddin Hadzari (tag.11)"). URL pattern: `tegaptv.com/YYYY/MM/DD/full-results-<event>-<year>`. The homepage aggregates recent results. Search: `"full results" site:tegaptv.com` or `TegapTV <event> <year> results`. Pages are WordPress — web_extract pulls them cleanly.
2. **TegapTV YouTube channel** — prejudging/finals videos, winner announcements, and the **"gym visit" profile series**: titles like "ATHLETE NAME - GYM NAME, City" (e.g. "Syed Khairuddin Morktarudin - D'POPEYE GYM, Kuala Lumpur"). The description names the gym and location — retrievable via web_extract even when the browser hits YouTube's bot-check.
3. **TegapTV Facebook (facebook.com/tegaptv) & Instagram (@tegaptvmalaysia)** — photo sets, lineup announcements, results shares.
4. **Gym Facebook/Instagram pages** — e.g. D'Popeye Gym Sri Rampai (facebook.com/dpopeyegymtamansrirampai). Some gyms are "old school hardcore" places whose founder IS the head coach — that person's IG is a goldmine.
5. **Coach Instagram accounts** — gym founders/head coaches tag their athletes. E.g. Iwan Setiawan (@iwan_setiawan230577, Founder D'Popeye Gym, KLBBF VP/Head Coach) posts "My apprentice @<athlete-handle>…". Searching `"@<suspected-handle>"` or the coach handle surfaces corroboration that official result pages never contain.

## Domain knowledge — Malaysian federation structure
- **"Body Smart"** = the Men's Physique / "Badan Cantik" class. Split by height: **Bawah 170cm** (below 170cm) and **Atas 170cm** (above 170cm). Height classes, NOT weight classes.
- Bodybuilding (bina badan) open classes split by weight: Bawah 70kg, 70–80kg, Atas 80kg; plus "Bakat Baru" (new talent, below/above 70kg), "Best of the Bests" (overall open), "Champ of Champ".
- Recurring events: Mr ACT (late Dec), Mr Isagenix (1 Jan), Mr Enrich (Dec), Mr Body Smart Meru, Mr Puchong, Mr Malaysia, NABBA/WFF shows. NABBA-affiliated circuit covered by TegapTV.
- Bahasa placings: Pertama (1st), Kedua (2nd), Ketiga (3rd), Keempat (4th), Kelima (5th), Juara (champion). "Tag.#" = competitor number on stage.

## Federation directory (for event calendar & category research)
- **IFBB Pro/NPC Malaysia** (ifbbpromalaysia.com, @ifbbproleague_malaysia) — enhanced. 4 shows/year in MY.
- **INBA/PNBA Malaysia** (asianaturalbodybuilding.com, @inbapnbaglobal_official) — **natural** (WADA). Unique: Cosplay Fitness.
- **WFF Malaysia** (wff-international.com, FB: /wffmalaysia) — enhanced. Unique: Denim Jeans Model.
- **PCA Malaysia** (pcaofficial.com, @pcaofficial global) — enhanced. Growing Asia presence.
- **FIF Malaysia** (fifinternational.net) — **natural**. Glute Gauntlet Model category.
- **WNBF Malaysia** (wnbfmys.org, @wnbfmy) — **natural** (drug-tested). Muscle Mash is flagship.
- **MBBF/WBPF** (wbpsf.org) — national federation, enhanced. Runs Mr Malaysia state→national pipeline.
- **NABBA Malaysia** — enhanced. Champion of Champions format.
Full calendar + source URLs: `references/malaysia-federation-calendar-2026.md`

## Workflow
1. Search the exact name + "bodybuilding", the alternate spelling, and combinations: `"<Name>" bodybuilding`, `"<alt spelling>"`, `<name> tegaptv`, `<name> <gym>`.
2. Pull every TegapTV result page found with web_extract. Record: event, venue, date, category, placing (Bahasa), tag number.
3. Cross-reference across events — the same names recur (Faez Nick, Zaid Moheyer, Amirul Firdaus…), so result pages corroborate each other and confirm identity.
4. Gym affiliation: search `TegapTV "<name>" gym`. The YouTube gym-visit series titles name the gym directly.
5. Social media: search `"@<name>" instagram` and `site:instagram.com <name> <gym>`. Prefer coach/team tags over the athlete's own account (usually private). Verify candidate handles against bio/location/content — name collisions are rampant (a "Syed Khairuddin" IG hit may be an engineer, a footballer, or an NUS professor).
6. Age/DOB: almost never published in results pages or captions. Do NOT estimate from photos; report "not publicly documented".
7. Save a markdown dossier: identity table (each spelling + where it appears), per-event results (event/venue/date/placing/tag), category, gym connection with evidence chain, social handles with confidence level, source URLs, open questions.

## Identity reconciliation
Two spellings for one athlete is the NORM in this scene: official results use the formal name ("Mohd Khairuddin Hadzari"), media/gym features use the patronymic/honorific form ("Syed Khairuddin Morktarudin"). Treat as the same person when they share: same media ecosystem (TegapTV), same gym, same competitive timeframe, and/or coach tags. State confidence explicitly (high/medium) — absolute proof is usually unavailable.

## Federation / event calendar research methodology
When building a Malaysia physique event calendar or scouting federations:
1. Start with federation websites (ifbbpromalasia.com, wffasia.jp, pcaofficial.com/international, asianaturalbodybuilding.com, worldnaturalbb.com, fifinternational.net)
2. Search CloudJoi, Eventbrite, HappeningNext, KLEventsCalendar for ticketing/listing data
3. Check `references/malaysia-federation-calendar-2026.md` for pre-built directory and source URLs
4. For Instagram handles: search `site:instagram.com <federation name>` — many Malaysian federations have weak IG presence; Facebook is often stronger (e.g. WFF Malaysia, PCA Malaysia)
5. Natural status: check for "drug-tested", "WADA compliant", or "natural" in federation descriptions; WNBF and INBA/PNBA are confirmed natural; all others are enhanced unless stated

## Pitfalls
- Instagram profile extraction usually fails/blocks — corroborate via search snippets and coach tags instead of the profile itself.
- Don't confuse same-name strangers: cross-check bio, geography, content (e.g. @syedgerrard, Sungai Siput ≠ KL physique athlete).
- YouTube watch page in the browser may show a bot-check; the search snippet + web_extract description suffice.
- A missing name in a Top-5 list ≠ "did not compete": could be a lower placing or non-entry. Flag as an open question.
- Never fabricate age/results. List open questions explicitly at the end of the dossier.

## Event Calendar / Upcoming Competition Research

### When to use
- User asks for upcoming bodybuilding/physique competitions in Malaysia or SEA
- Building a competition calendar for a specific date range
- Finding registration deadlines, fees, or categories for a specific show

### Key sources (in priority order)
1. **Federation websites** — most authoritative for confirmed dates, categories, registration, and fees:
   - **IFBB Pro Malaysia** (ifbbpromalaysia.com) — NPC Regional events in Malaysia. Lists categories, venue, hotel, registration periods, and fee tiers.
   - **NPC Worldwide Schedule** (ifbbpro.com/npc-worldwide/schedule/) — master schedule for all NPC/IFBB Pro League events globally. Filter by country. May be incomplete for some regions (Philippines events sometimes missing).
   - **PCA International** (pcaofficial.com/international) — **most comprehensive single-page listing** of PCA events across all countries. Shows date, city, and links to registration pages with fees. PCA runs 10+ shows in Thailand alone per year.
   - **IFBB Pro League Thailand** (ifbbproleaguethailand.com/events/) — Thailand NPC/IFBB Pro events with registration details.
   - **WFF International** (wff-international.com/events/) — WFF global events calendar with dates and venues.
   - **ABBF** (abbf.asia/Event.html) — Asian continental championships.
   - **INBA/PNBA Asia** (asianaturalbodybuilding.com) — Natural events across Singapore, Malaysia, Philippines, Thailand, Vietnam, China.
   - **WNBF Singapore** (wnbfsingapore.com/event) — Natural events in Singapore.
   - **PABBM / state federations** — Mr Malaysia national championship and state qualifiers (Mr Sabah, Mr Penang, etc.). Dates often announced via news articles, not federation websites.
2. **Event platforms** — for individual event details (fees, venue, registration):
   - **CloudJoi** (cloudjoi.com/shows/) — Malaysian event ticketing, especially PCA events.
   - **Eventbrite** — WFF, NPC, and independent events.
   - **Eventibus** (eventibus.com) — global event aggregator.
   - **HappeningNext** (happeningnext.com) — Malaysian event aggregator.
   - **Active.com** — INBA/PNBA and FM Singapore events with registration.
   - **Muscleware** (muscleware.com) — NPC Worldwide athlete registration portal.
3. **Curated calendars** — cross-reference to catch events missed by individual searches:
   - **CrazyBadman blog** (crazybadman.com/blogs/news/2026-bodybuilding-fitness-competition-calendar) — curated SEA competition calendar with country-by-country listing. Includes dates, organizers, and summaries.
   - **Kompak store blog** (kompak.store/blog/) — international bodybuilding calendar.
4. **News articles** — for state-level events (Mr Sabah, Mr Penang, etc.) often announced via Malaysian news portals (Nabalu News, Daily Express, BorneoPost, Harian Metro, Astro Stadium).

### SEA federation landscape (Aug-Nov 2026 baseline)
| Federation | Presence | Notes |
|---|---|---|
| NPC Worldwide / IFBB Pro League | MY, TH, PH, VN, ID | Pro qualifier pathway. Promoter: Hugo Chan (MY/ID), Moe Elmoussawi (TH), Alex Hong (PH), Tamer El Guindy (PH/MCI) |
| PCA | TH, MY, ID, PH, SG | Largest show volume in Thailand (10+ shows/yr). First-ever PCA Malaysia Pro Qualifier in 2026. Promoter: Nic Edgerton (Asia) |
| INBA/PNBA | SG, MY, PH, TH, VN | Natural/pro-drug-tested. Natural Universe is their biggest Asia event (Singapore). |
| WNBF | SG | Natural-only. Polygraph + WADA urine testing. |
| WFF | TH | SE Asia Championships in Pattaya. Also NABBA-affiliated Malaysian circuit (via TegapTV). |
| ABBF/WBPF | Continental | Asian Bodybuilding & Physique Sports Championships. National team selection event. |
| State federations | MY | Mr Sabah, Mr Penang, Mr Johor → feed into Mr Malaysia national championship. |

### Workflow
1. Search `bodybuilding competition [country] [year] calendar` and `physique competition [country] [year]` for broad discovery.
2. Pull federation websites for confirmed events in the target date range.
3. Pull curated calendars (CrazyBadman, Kompak) as cross-reference.
4. Extract individual event pages for registration details (fees, deadlines, categories, venue).
5. Search news sites for state-level events not listed on federation sites.
6. Compile into structured output with: event name, federation, date, venue/city/country, categories, registration status/deadline, fees, pro_qualifier flag, notes, source_url.

### Pitfalls
- PCA membership (£50+VAT/year) is required BEFORE entering any PCA show — competitors often miss this.
- NPC/IFBB Pro membership required separately for NPC events.
- The NPC Worldwide Schedule may not list all regional events (Philippines events sometimes on ifbbprokorea.com only).
- "Natural" events (WNBF, INBA/PNBA) require drug testing (polygraph + urine) — athletes must check banned substance lists 10 years back.
- State-level Malaysian events (Mr Sabah, Mr Penang) are often only announced via news articles, not federation websites.
- PCA Thailand is very active (10+ shows/year) — search pcaofficial.com/international for the full list.
- Dates and venues are subject to change — always verify against the source URL.
- Eventbrite "no refunds" policy is common for physique events.

## Support files
- `references/tegaptv-event-index-and-khairuddin-dossier.md` — known TegapTV result-page URLs (event index) + full findings on Mohd Khairuddin Hadzari / Syed Khairuddin Morktarudin, so a follow-up session can extend rather than redo.
- `references/hmetro-malaysia-image-extraction.md` — recipe for extracting article images from bot-blocked Harian Metro / HMetro pages. When `browser_navigate` times out and `web_extract` fails, plain `curl` with a browser UA recovers `og:image` + all `assets.hmetro.com.my/images/articles/*` URLs in one shot. Includes AMP fallback for text.
- `references/joe-zack-azizol-dossier.md` — dossier for Mohamad Azizol Zakariya ("Joe Zack"), Bahau NS — WFF Men Athletic Physique competitor and school teacher (Geografi + PJK), HMetro 2026-08-08 feature.
- `references/malaysia-federation-calendar-2026.md` — comprehensive directory of all Malaysian bodybuilding/physique federations (websites, IG handles, natural status, categories) + 2026 event calendar (Aug–Nov focus) with source URLs. Compiled 2026-08-15.
- `references/sea-event-sources-and-url-patterns.md` — comprehensive inventory of SEA bodybuilding event sources with URL patterns, federation mapping, and verified data points from Aug-Nov 2026 research. Use as starting point for any future event calendar task.

## Malaysian media: Harian Metro / HMetro article extraction
HMetro (hmetro.com.my) is a primary Malaysian news source for local human-interest and athlete features. From a datacenter IP both `browser_navigate` and `web_extract` fail (page timeout / "Failed to fetch"). **Plain `curl` with a normal browser UA works** and surfaces everything in one shot:

```bash
curl -sL -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36" \
  "https://www.hmetro.com.my/utama/2026/08/1395281/cikgu-menjadi-sado" -o /tmp/page.html
```

Extract images + metadata:
- `grep -oE 'https://[a-z.]*hmetro[a-z.]*/images/articles/[^"]+\.(jpg|jpeg|png|webp)' /tmp/page.html | sort -u` → all body/featured images
- `<meta property="og:image">` → social-share hero
- `<meta property="article:author">` → reporter byline (e.g. `Redzuan Muharam`)
- `<meta name="article-city">` → city tag (e.g. `Jempol`)
- `<meta name="article-id">` → article ID
- `<meta property="article:published_time">` → ISO timestamp (MYT, `+08:00`)
- `<meta name="keywords">` → keyword tags; the last 2-3 are usually the most specific (athlete name + gym + competition)

**AMP fallback** (`/amp/utama/...`) is a clean static page that **does** go through `web_extract` when the main URL times out. Prefer AMP for text content; use curl-recovered URLs for images.

Same recipe generalizes to other Malaysian news sites (BHarian, Kosmo, Utusan, Sinar Harian). Astro Awani usually works via web_extract directly; Malaysiakini paywalls. Verified 2026-08-08 on the `cikgu-menjadi-sado` feature. Full recipe: `references/hmetro-malaysia-image-extraction.md`.

## Stage-photo analysis pattern (no caption, just the image)
When you have a competition stage photo but no caption, `vision_analyze` with a targeted question recovers structured evidence. Verified 2026-08-08 against a WFF championship podium shot — extracted: competitor tag numbers, prize amount ("CHAMPION RM 1,000"), federation tag (WFF), sponsor logos (KBS), event year (2025), official role (EXCO lanyard). Use this when:

- Caption is missing/cropped on the publisher's IG repost (only the headline image survives)
- You need to corroborate a name against the on-stage tag number
- You want the actual prize value or category code that the prose never states

Combine with the photo's URL provenance (HMetro CDN) for F2 citation. The vision transcript is *evidence* — quote it (e.g. "Backdrop text: `2025 ... KBS ... WFF ... Champion RM 1,000`"), don't paraphrase it as your own observation.
