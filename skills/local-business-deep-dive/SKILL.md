---
name: local-business-deep-dive
description: 'Comprehensive research of a local business entity (esp. Malaysian): owner identity + namesake disambiguation, founding history, notable members/alumni, equipment/offerings reputation, competition-production record,'
---
# Local Business Deep-Dive Research

## When to use
User asks for a comprehensive profile of a specific local business: owner, history, notable people, reputation, pricing history, competitive position. The D'Popeye Gym Sri Rampai session (2026-08) is the reference case — see `references/dpopeye-gym-case-study.md` for the worked example, source URLs, and what data came from where.

## Workflow

### 1. Core identity & ownership
- Find the business's official **Facebook page handle** and **Instagram handle** first — in Malaysia (and most SEA markets) these are the primary web presence and the page "About" text (address, hours, phone, email, staff posts) is indexed by search engines even when the pages themselves are login-walled.
- Owner identification: search `"<business name>" owner OR founder OR CEO`; then check the owner's personal FB/LinkedIn — **role start dates on FB profiles ("Owner and CEO Oct 23, 2012 – Present") and LinkedIn experience entries give the founding date**.
- IG bio lines carry current roles/federations/credentials (e.g. "Vice President KLBBF | Head Coach KLBBF | Founder..."). Read the full bio text from search snippets.

### 2. Namesake disambiguation (MANDATORY for common names)
Never assume a name match is the same person. The D'Popeye case had **three different Iwan Setiawans**: an Indonesian footballer (b. 1958), an Indonesian model/One Gym owner (b. 1976, Jakarta — Reps-ID profile), and the Malaysian gym owner (b. 23 May 1977 — Wong Hong.net athlete interview). Verify each hit against **DOB + residence + occupation + family names** before using it. A plausible-looking bio article from the wrong country/industry will corrupt the whole dossier.

### 3. History & founding date
Triangulate across: owner's FB/LinkedIn role start dates, anniversary posts, "We're back in business" / relaunch videos, pandemic-era closure posts (e.g. "closed 29-30 June 2023, resume 1 July 2023"), old directory listings. Note **multi-location businesses**: original address vs branch address often have DIFFERENT hours, phone lines, and even price structures — capture each location separately and label the data.

### 4. Notable members / alumni / production record
- Search the business name + contest/event names (`"<gym>" Mr Malaysia OR NABBA OR NPC`).
- For gyms: federation contest-results pages (NPC News Online `contests.npcnewsonline.com`, NABBA, WFF) are extractable and authoritative.
- Industry media (e.g. TegapTV Malaysia for bodybuilding) film prep documentaries at specific gyms — the video title/description names the gym, coach, and athlete.
- Athlete/celebrity testimonials on IG ("This was where I trained for X") are strong reputation evidence — the post text is indexed.

### 5. Reputation & offerings
- Search review content creators (e.g. my.gymie "100 gym challenge" — walk-in fee, hours, décor details are all in the caption).
- Mainstream listings (Time Out KL) give curated descriptions: equipment brands, clientele, on-site sales (e.g. "sells protein at half market price"), registration fees.
- Distinguish "production gym" (produces athletes/competitors) from "promoter" (runs shows) — the user may conflate them.

### 6. Pricing history reconstruction (e.g. 2020–2025)
Assemble a year-by-year table from heterogeneous sources:
- **Current/listed price**: Time Out, directory sites (baydimalaysia.com, gym.my), Google/Waze listings.
- **Promo posts**: holiday promos name the standard rate ("MERDEKA PROMO RM70 for new membership, applicable 31 Aug 2023") — implies standard ≈ RM70.
- **Membership-card posts** on IG: "Registration RM50 only... Men RM70, Ladies RM60".
- **New-rate announcement videos**: FB video titles/descriptions carry the facts ("Here our New Rate for 2025 — Free day pass plus no tax, 500 Founder spots") even when the video is unwatchable.
- **Walk-in / day-pass fees** from reviewer captions (RM8).
- **Service packages** from FB group posts (PT packages RM960/RM1440 with session counts).
- Flag uncertainty: "exact 2025 figure is in a video that isn't indexed — needs the video or a call."

### 7. Scene positioning
Map the segment: premium chains (RM150-250/mo, amenities) vs mid-range independents vs old-school hardcore gyms vs boutique. Position the subject by price band + credibility markers (media features, athlete endorsements, federation ties, "legendary" status). Name 1-2 direct local competitors with their own price points for contrast.

### 8. Deliverable format (matches user expectations)
Write a dossier to a markdown file, structured as:
- Title + compile date + source list note
- Owner/Founder section (roles, bio, credentials, federation roles)
- History (founding date, locations, theme, pandemic/relaunch notes)
- Notable members table (person | connection | achievement)
- Equipment/atmosphere reputation
- Competition production record (year-by-year)
- Pricing table (period | rate | source/notes)
- Operating hours table (location | hours | source)
- Position in scene (segments + direct competitors)
- **Quick Reference fact block** (all contact/address/handle data in one place)
- Source URL list
- Limitations/uncertainties at the end (login-walled items, video-only content)

## Malaysian data-source bank
- **Directories**: Time Out KL, baydimalaysia.com, gym.my, Waze live-map (place IDs), iRumah (property context for the neighbourhood).
- **Social**: FB page handle + owner's personal FB (role dates), IG location pages (`instagram.com/explore/locations/<id>/`) leak owner handle + post count + hours logged-out, IG bios via search snippets.
- **Federation/contest records**: NPC News Online (`contests.npcnewsonline.com/contests/<year>/...`), NABBA, WFF.
- **Industry media**: TegapTV (Malaysian bodybuilding), YouTube titles.
- **People databases**: LinkedIn, personal athlete-profile sites (e.g. wonghong.net athlete interviews — goldmine for full bios).

## Pitfalls
- **FB + IG login walls**: web_extract returns empty/failed; browser hits a login dialog on www AND m. variants. Do NOT burn turns clicking dialog buttons. Use search-snippet mining + IG location pages — full mechanics in `anti-bot-web-extraction`.
- **Search results polluted by namesakes**: the Wikipedia hit for a common name (footballer) will rank above the actual subject. Disambiguate first, filter after.
- **Hours/price differ per location**: label which location each fact belongs to.
- **Video-only content**: prices/announcements often live only in FB video titles — the indexed title is the fact, the exact figure may need the video.
- **Registration fee vs monthly fee confusion**: Time Out listed RM170 "upfront upon registration" while IG card posts said RM50 registration — report both with dates.
- Don't fabricate missing figures; say "not in indexed text — needs the video/phone call."

## Routing notes (moved from description 2026-10-23)

pricing history across years (e.g. 2020-2025), and scene positioning vs competitors. Produces a structured dossier (quick-reference fact table, per-dimension sections, pricing/people tables, source URL list, limitations note). Trigger: 'research <business> comprehensively', 'owner/history/pricing of X', any deep-dive on a local gym, restaurant, clinic, studio, shop. Pairs with anti-bot-web-extraction for FB/IG login-wall bypass.
