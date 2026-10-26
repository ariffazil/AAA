---
name: social-expert-ranking
description: "Use when ranking social-media experts in any field."
version: 1.0.0
forged: 2026-10-21
tags: [expert-finding, osint, social-media, vetting, influencers, misinformation]
capability_tier: fed-agent-subagent
---

## When to Use

- "Sapa pakar paling betul kat TikTok untuk X"
- Ranking fitness/peptide/supplement/health influencers by credibility
- Auditing a claimed expert list from social media
- "Ramai pakar X kat TikTok sekarang" — any request to separate signal from fame

Pairs with `expert-finder-engine` (that skill ranks institutional professionals; this one ranks
voices without a registry).

# Social Expert Ranking — Evidence Filters Over Fame

Social-media "experts" have no registry and no procedure volume. Fame metrics (followers, views)
measure reach, not correctness. Rank with three measurable filters, all checkable from public
content alone:

## The 3 Filters

### 1. Conflict of interest — the sales filter beats the credential filter
Does the voice SELL the thing it praises? Own product sales, affiliate codes, telehealth funnels,
MLM downlines, "DM me for the protocol". A seller's protocol is an advertisement. Credentials can
be worn by a salesperson — the MD/PhD prefix does not neutralize a commission structure.

### 2. Citeability — species check
Do claims point at retrievable studies? Does the content name the species? In peptide/supplement
spaces most cited work is rodent; "clinically proven" on social usually means "tested on rats".
The question "in what species?" collapses most influencer rankings in one move.

### 3. Admits uncertainty — the honesty marker
Does the voice say "this is experimental, the data is in animals"? Honesty signals: names risks,
insists on supervision/bloodwork, cycles off, says what did NOT work. Red flags: dosing protocols
distributed by DM, miracle language, "doctors don't want you to know", selling the compound
directly.

## Verdict Buckets

- **LOLOS** — passes all three; listen
- **TAPIS** — generalist reviewer or carries sponsorships; keep with explicit caveats (name the
  sponsorship)
- **GUGUR** — seller or MLM; discard and warn

Name MLM health funnels explicitly in the warning: they recruit through a doctor persona, and a
doctor persona is not a medical source. Patent-count and "endorsed by N doctors" claims inside an
MLM pitch are classic markers, not evidence.

## Marhaen sources count

Ordinary-community creators count as experts when they pass the same filters. Small accounts that
show their own bloodwork, change one variable at a time, and say what did NOT work are
higher-trust than large accounts that never name a failure.

## Local-language mapping trick

Mine long-form podcast guest rosters in the local language. A serious podcast's guest list is a
better local expert map than any follower-count leaderboard: booking a long-form guest requires
the host to trust the guest under hours of unedited talk. Search YouTube search results directly
(parse `ytInitialData` from the results HTML) — filter by channel + view count to find who is
talking about the topic natively vs just translating English content.

## Global-tier anchor

For regulated/health topics, anchor the global tier first (who holds the field's actual
authority — society founders, handbook authors, licensed clinicians with teaching roles), then
place local voices relative to it. Amplifiers (celebrities who mention the topic occasionally)
are not sources regardless of reach.

DITEMPA BUKAN DIBERI
