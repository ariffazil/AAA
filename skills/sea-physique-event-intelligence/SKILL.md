---
name: sea-physique-event-intelligence
version: 1.0.1
description: "Research physique events in Malaysia and SEA."
author: hermes
license: MIT
metadata:
  hermes:
    tags: [research, bodybuilding, physique, competition, malaysia, sea, fitness-events]
    related_skills: [AGI-agentic-web, well-bodybuilding-comp-prep]
floor_scope: [F2, F4, F9, F12]
autonomy_tier: T1
---

# SEA Physique Event Intelligence

Research protocol for physique/bodybuilding/fitness competition events in Malaysia and Southeast Asia.

## When to Use

User asks about bodybuilding events, men's physique shows, competition calendars, "any show this weekend", "upcoming competitions", Mr KL, NPC/PCA/INBA/WFF events, or wants to spectate/compete in physique competitions in Malaysia or SEA.

## User Preference: Arif (SOVEREIGN)

- **Primary language**: BM Penang for conversation, EN for structured data/tables
- **Format**: Answer-first, then structured table. No preamble.
- **Depth**: When user says "deep research" hit ALL federations, ALL platforms, ALL timeframes
- **Platforms**: Instagram is the PRIMARY source for Malaysian fitness events. Web search alone misses many. When user says "insta search" use browser or web_extract on IG pages directly.
- **Frustration signals**: "Today", "this weekend" = user narrowing scope fast. Start tight, expand on request.

## Research Protocol

### Phase 1: Quick Scan (what is happening NOW)
1. Web search: "[event type] KL Kuala Lumpur [date range]"
2. Web search: site:instagram.com "[keyword]" [month]
3. Check key Instagram accounts below
4. Return: tight answer, 1-3 events max, dates + venues + links

### Phase 2: Full Calendar (deep research)
1. Hit EVERY federation with Malaysia presence
2. Search each federation Malaysia + SEA calendar
3. Search regional events accessible from KL (SG, Bali, VN, Laos, TH)
4. Search local club shows (KLBBF, state federations)
5. Compile chronological table with Status column
6. Include Mr KL (KLBBF) — often NOT web-indexed

### Phase 3: Instagram Deep Dive (when user explicitly asks)
1. Key hashtags: #mensphysiquekl #malaysiabodybuilding #npcmalaysia #pcamalaysia
2. Many small shows announce LAST MINUTE on IG only

## Key Instagram Accounts

| Account | Federation |
|---|---|
| @ifbbproleague_malaysia | NPC/IFBB Pro League |
| @pcamalaysia | PCA |
| @inbapnbamy | INBA/PNBA |
| @globalclassic_malaysia | NPC/IFBB associated |
| @battleofphysique | Battle of Physique |
| @mbbf.official | MBBF (WBPF/ABBF) |
| @dwows_eventcenter | DWOWS |

## Venue Patterns (Malaysia)

| Venue | Used By | Location |
|---|---|---|
| KLPAC (Pentas 1) | PCA | Sentul |
| Nexus Connexion | NPC/IFBB Pro | Bangsar South |
| Menara KEN TTDI | INBA/PNBA | TTDI |
| MVEC (Mid Valley) | WFF, Battle of Physique | Mid Valley City |
| OCM Indoor Sports Arena | KLBBF / Mr KL | Jalan Hang Jebat |
| Palace Golden Horses | WBPF/ABBF | Mines, Selangor |

## Federation Directory

Full directory with all 9 federations, shows, fees, and pro pathways:
`references/federation-directory-malaysia-2026.md`

## Pitfalls

1. Web search misses IG-only events. Always supplement with IG account checks.
2. Date confusion: some federations list the same event with slightly different dates.
3. Mr KL is invisible online. KLBBF rarely appears on event listing sites. Check Facebook.
4. Natural events (INBA/PNBA, NPC Natural) have strict drug testing. Do not confuse with open shows.
5. Pro card pathways differ: NPC Pro → Olympia. INBA Pro → Natural Olympia. PCA Pro → PCA international. NOT interchangeable.
6. Stale hits: search results surface shows from earlier in the SAME year (Jun/Jul events in an Aug search). Anchor with the current date FIRST and only cite events still ahead. Flag registration deadlines alongside show dates — Arif tracks sponsors/athletes and NPC closes ~5 weeks pre-show.
7. Third-party calendars (kompak.store etc.) list month-less or unverified dates (e.g. "WFF Universe KL 12th"). Confirm on the federation's own page before citing.

## Live Calendar Cache

`references/kl-physique-calendar-2026-H2.md` — web-verified H2 2026 KL/SEA snapshot (2026-08-15). Re-confirm dates before citing; add newer finds there.
