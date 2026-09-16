# Institutional Contrast Mapping

> Lightweight pattern for mapping structural changes in any GLC, corporate, or government body.
> When you need to know "what changed recently" without a full forensic deep dive.
> Proven: 2026-08-26 — PETRONAS leadership contrast (board refresh, COO creation, CEO extension).

## When to Use

- User asks "what's the latest on [entity] leadership/board/structure?"
- User drops an official leadership page URL and says "map this" or "what changed?"
- Any GLC/corporate/agency query about recent structural reorganisation
- Follow-up to news research — user wants the contrast between reported events and current state

**When NOT to Use:**
- Full financial analysis → `references/institutional-financial-deep-dive-pattern.md`
- Forensic crisis case building → `institutional-forensic-analysis` skill
- Quick fact check → `web_search` alone

## The Three-Layer Method

### Layer 1: News Landscape Scan (events)

Run 3 parallel search queries:
```
web_search: "{entity} leadership news {year}"
web_search: "{entity} CEO/board changes {year}"
web_search: "{entity} {specific person name} {year}"
```

**Goal:** identify the key events — appointments, departures, promotions, new roles, scandals, legal exposure. These are the *triggers*.

### Layer 2: Live Canonical Scrape (current state)

Scrape the entity's official leadership/about page:
```
mcp__firecrawl__firecrawl_scrape(url="{official_leadership_url}", formats=["markdown"], onlyMainContent=true, maxAge=0)
```

**Goal:** the actual current state. Websites update; news may lag or lead.

**Tool fallback chain (if firecrawl unavailable):**
1. `web_extract` — but only if backend is configured to firecrawl/tavily/exa. **SearXNG backend CANNOT extract page content** — it returns `SearXNG is a search-only backend` error. Do not retry; skip to next rung.
2. `browser_exec` headless browser — works but adds latency and may fail on JS-heavy SPAs.
3. `computer_use` capture — last resort, slowest option.

**Pitfall:** `web_extract` with SearXNG is a known failure mode. The error message is cryptic but consistent. Always go directly to firecrawl for page extraction.

### Layer 3: Cross-Reference → Contrast Matrix (signal)

Build a table comparing news events against the live page:

| Signal | News reported | Website confirms | Structural read |
|--------|--------------|------------------|-----------------|
| {Event 1} | {Source, date} | {Current state} | {Why it matters} |
| {Event 2} | {Source, date} | {Current state} | {Why it matters} |

**Columns explained:**
- **Signal:** what to look for (appointment, departure, new role, new title)
- **News reported:** what the media said happened, with source
- **Website confirms:** whether the official page reflects this yet
- **Structural read:** the *interpretation* — what this change signals about the entity's posture

## The Structural Read (Critical Step)

Don't just list names. For each change, answer:

1. **Why this structure now?** (political insurance, operational coverage, compliance response, strategic pivot)
2. **What is unusual?** (new titles created, dual-hatting, unusual board composition, multiple company secretaries)
3. **What does it signal?** (defensive posture, expansion, consolidation, crisis response)

Common patterns:
- **COO created = operational defensive layer.** Entity is splitting political/strategic (CEO) from execution (COO), usually during litigation or multi-front disputes.
- **Dual company secretaries = compliance intensification.** More regulatory burden, more filings, more governance scrutiny.
- **Board refresh during crisis = governance theatre or genuine reform.** Check if departing members were on audit/risk committees — if yes, it's structural; if they were general members, it's rotation.
- **CEO extension despite scandal = political insurance.** The entity is betting continuity matters more than optics. Usually means no internal successor is ready, or the political cost of removal exceeds the reputational cost of keeping.

## Pitfalls

1. **Snippet-only synthesis = T2 violation.** If `web_search` returns only snippets (title + 200 chars) and full articles cannot be extracted via any fallback, DO NOT synthesise from snippets. Report: "I have snippet-level data only. Cannot synthesize beyond these fragments." The SNIPPET SCAR applies here.

2. **News vs website lag.** News may report an appointment before the website updates, or vice versa. When they conflict, the website is the canonical current state; news is the event that caused the change. Note the lag explicitly.

3. **Single-source risk.** One news article + one website scrape = thin evidence. For high-consequence claims (billion-RM exposure, political appointments, state-level disputes), at least two independent news sources should corroborate before the structural read is presented as confident.

4. **Board ≠ Executive.** Board of Directors (governance) and Executive Leadership Team (operations) are different layers. A person can sit on one but not the other. Always map both separately. A CEO who is an Executive Director sits on both; an independent non-exec is board only.

5. **Don't confuse file editing with knowledge.** Reading the current page tells you *who is listed now*. It does not tell you *when they were appointed* or *what they replaced*. You need the news layer for that. The contrast matrix is the value — not either layer alone.

## Worked Example: PETRONAS (2026-08-26)

**Context:** User asked "what are the major news about PETRONAS leadership recently" then dropped `petronas.com/about-us/our-leaders` and said "map the contrast or changes."

**Layer 1 findings (news):**
- Tengku Taufik second contract extension (Bloomberg/FMT, Aug 8 2026)
- Mohd Jukris Abdul Wahab appointed COO (Rigzone/Bloomberg, Jan 19 2026)
- Petrofac-Kingtime scandal — RM1B+ exposure (The Corporate Secret, Aug 10 2026)
- Three board members departed after FY2024 (PETRONAS IFR 2025 chairman message)

**Layer 2 findings (live scrape via firecrawl):**
- 10 board members listed (including 2 company secretaries)
- Jukris listed as COO + EVP Upstream + Exec Director (triple hat)
- Two new independent directors (Shahrazat, Abdul Rasheed)
- Norwankiss added as second company secretary

**Layer 3 contrast matrix:**

| Signal | News | Website | Structural read |
|--------|------|---------|-----------------|
| Taufik extension | 2nd extension, ~2yr | Listed as President & Group CEO | Continuity despite Petrofac exposure — political insurance |
| Jukris COO | New COO role, Jan 2026 | COO + EVP Upstream + Exec Dir | Operational defensive layer — splits political (Taufik) from execution (Jukris) |
| Board refresh | Johan, Ibrahim, KY departed | Shahrazat + Abdul Rasheed new | Governance refresh during crisis — 2 new independent directors |
| Dual secretary | Not in news | Norwankiss new alongside Azizi | Compliance intensification — more governance burden |

**Key insight:** The entire structure is designed to insulate the CEO from operational exposure while concentrating execution authority in Jukris. Classic political insurance for a GLC facing billion-ringgit litigation (Petrofac) and a state-level sovereignty fight (Sarawak gas).
