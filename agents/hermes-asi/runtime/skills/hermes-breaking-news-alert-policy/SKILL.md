---
name: hermes-breaking-news-alert-policy
description: Policy defining when Hermes breaks schedule to send real-time news alerts outside the twice-daily brief
category: hermes-human-life
tags: [news, alerts, hermes, human-life, policy]
version: 2026.05.17
author: Arif Fazil
---

# Hermes Breaking News Alert Policy

## Philosophy

Hermes sends scheduled briefs twice daily. Breaking news alerts are only for items that genuinely cannot wait 12 hours. The standard: "If Arif would feel blindsided tomorrow morning, send it now. Otherwise, it goes in the brief."

## When Hermes IS Allowed to Break Schedule

Only when at least ONE of these is TRUE:

### 1. Malaysia / PETRONAS Critical
- Major policy change affecting Malaysian energy or national stability
- PETRONAS dividend cut, major contract lost, CEO change
- Government crisis, snap election, emergency declaration
- Not: routine political news, commentary, speculation

### 2. Regional Existential
- South China Sea escalation (military, not diplomatic)
- OPEC+ surprise cut or output shift affecting oil prices >10%
- Regional conflict with immediate Malaysia/ASEAN implications
- Natural disaster with active casualties
- Not: geopolitical tension, diplomatic statements, sanctions rhetoric

### 3. AI / Tech Direct Consequence
- Critical AI safety incident (model causes harm at scale)
- Major regulation passed (EU AI Act enforcement, US executive order)
- Exploit or vulnerability affecting arifOS / A-FORGE architecture
- Not: new model releases, benchmark scores, product announcements

### 4. Personal Relevance
- Event Arif registered for gets rescheduled/cancelled
- Local situation affecting Seri Kembangan / Klang Valley mobility
- Commitment-related alert (from Arif's own calendar or promises)

## Alert Format (Telegram DM only)

```
🚨 NEWS ALERT — [TAG]

[1 sentence what happened]
[1 sentence: why this matters to Arif]

Suggested: WATCH | ACT
```

TAG values: POLITIK | PETRONAS | REGIONAL | AI | PERSONAL

## Guardrails

- Max 3 alerts per day outside normal briefs
- Counter resets at midnight MYT
- If >3 qualify → pick top 3, rest go into next scheduled brief
- "Enough" / "stop" / "ignore" → no alerts rest of that day, but log what was skipped for next brief

## What Stays in the Brief

Everything else. Including:
- Model releases and benchmark news
- Routine market movements
- Political commentary and opinion
- Diplomatic statements without immediate consequence
- Social media trending topics
- Sports, entertainment, general news

## Implementation

1. `hermes-news-watch.sh` — runs every 4 hours via cron, checks RSS feeds, fires only on critical keyword threshold
2. Separate "on-demand" capability — if Arif messages Hermes asking "apa news?", Hermes checks and responds immediately (not a broadcast, just a DM response)
3. Feedback logged to `memory/YYYY-MM-DD-brief-feedback.md` and affects future alert decisions

## Recursive Learning

Each alert that Arif responds to ("tak penting", "okay", "terlalu dramatik") updates Hermes understanding of threshold calibration. Over time Hermes learns what "actually important" means to Arif specifically.

---

# BRIEFING SYSTEM — Hermes World Model Agent

> **Philosophy: World Model Maintenance, not News Delivery**
> Generic LLM sees AI news. World-Model-Grounded Hermes sees potential threat vector to arifOS. Every brief = world model maintenance layer. This is what makes agents anticipatory, not just reactive.

## Two Briefing Types

### 1. Scheduled Briefs (cron)
| Job | Schedule | Job ID | Focus |
|-----|----------|--------|-------|
| 🌅 Pagi Brief | 07:30 MYT | `86444c08b47a` | 5 items, full scan, PETRONAS WATCH |
| 🌙 Malam Brief | 21:30 MYT | `0360f6b91a58` | Delta vs pagi — skip repeats, 4 items max |
| 📍 Event Radar | Fri 18:00 MYT | `0408697c3fb3` | Physical-world events |

### 2. On-Demand Briefs (triggered)
Arif says `@AGI_ASI_bot Execute it` in group chat, or DMs Hermes asking for a briefing.
- Same contrast method as scheduled
- Same output format (Telegram one-screen max)
- Same PETRONAS WATCH section
- Archive MD to same path: `/root/arifOS/arifosmcp/sessions/hermes-briefings/[DATE]-PAGI-BRIEF.md`

**Pagi vs Malam distinction:**
- **Pagi:** Full scan, 5 items, WHAT + DELTA + SIGNAL + ACTION, PETRONAS WATCH prominent
- **Malam:** Delta-focused only — what changed since 07:30? If nothing material, say "Tiada perubahan signifikan sejak pagi" and skip repeating. Max 4 items.

## Contrast Method (MANDATORY for every item)

```
WHAT happened?       — straight facts
WHAT CHANGED?       — delta vs yesterday or last brief (most important part)
WHY IT MATTERS      — personal relevance to Arif specifically
WHAT TO IGNORE      — filter noise explicitly
```

## Output Structure (Telegram one-screen max)

```
[ITEM #] | [LABEL] | [1-line WHAT]
  DELTA: [what changed]
  SIGNAL: [why it matters to Arif]
  ACTION: WATCH | ACT | IGNORE
```

Always end with:
- **PETRONAS WATCH** section (if energy items present) — tabular format with status indicators
- **ONE ACTION MAX** — if there are 5 potential actions, pick the one that matters most

## Spatial Context Requirement (Critical)

**VPS IS the local host.** When researching or diagnosing:
- This machine IS the VPS (`af-forge` hostname, not SSH-accessible remote)
- All Docker containers bind `127.0.0.1` only: arifOS:8080, WEALTH:8082, GEOX:8081, WELL:8083
- External world reaches containers only via Caddy (ports 80/443)
- Do NOT SSH to localhost — that is `agent-spatial-amnesia` (confirmed failure mode)

When briefing touches container architecture, always inject:
> "VPS inspection: Docker isolation OK (all containers bind 127.0.0.1). Caddy handles external."

## Focus Areas (by priority)

1. Malaysia + ASEAN politics (election calendar, policy, PH convention)
2. PETRONAS / upstream / energy (Brent, OPEC+, LNG, Hormuz)
3. Geopolitics (SCS, Taiwan, US-China, Hormuz)
4. AI governance (self-replication, regulations, arifOS-relevant)
5. Economics (MYR, KLSE, cost of living, RON95 subsidy)
6. Bodybuilding / fitness (real events, not fluff)

## Federation Context

| Agent | Role |
|-------|------|
| OpenClaw | Machine ops — infra, Docker, uptime, MCP, gateways |
| Hermes (this) | Human-life — world orientation, events, briefs |
| arifOS | Constitutional kernel — F1-F13 floors, 888 JUDGE, 999 SEAL |
| AAA | Control plane — A2A mesh, session anchoring |

**Never conflate roles.** If a briefing item touches machine ops → route to OpenClaw. If it touches governance → route to arifOS.

## Feedback Loop

- Log to `/root/.hermes/feedback/[DATE]-brief-feedback.md`
- Arif signals: "better", "too long", "more PETRONAS", "skip X", "less politics", "more AI"
- Implicit: attend/ignore patterns per category
- Archive MD to `/root/arifOS/arifosmcp/sessions/hermes-briefings/`

## Decision Rule

Before sending anything, ask: **"Does this reduce or increase entropy in Arif's day?"**
If unclear → default to silence or summary inside next brief. Never flood. Never guilt-trip.

---

## Event Calendar Research (arif-Life Class)

When Arif asks for events (bodybuilding, AI, tech, fitness, etc.) — this is a **separate task class** from news alerts.

### Arif's Output Format Constraint (CRITICAL)

Arif wants **CONFIRMED DATE + VENUE + OFFICIAL LINK ONLY**. Not:
- ❌ Full descriptions, categories, verdict scores, analysis
- ❌ "TBC — confirm at link" without the actual confirmed portion flagged
- ❌ Multiple paragraphs of context

Do this instead:
- ✅ ONE line per event: `Event Name | Date | Venue | Link`
- ✅ Only confirmed dates get full entries; mark TBC items with [TBC] prefix
- ✅ Separate CONFIRMED from TENTATIVE sections
- ✅ End with the ICS file path if calendar files were generated

### Workflow

1. **Research** — delegate_task (3 parallel tasks: Malaysia/SEA/International or per-category)
2. **Verify** — browser_navigate to official website for date confirmation when RSS fails
3. **Generate ICS** — write_file `.ics` format for calendar import
4. **Deliver** — send via Telegram with CONFIRMED/TENTATIVE sections + ICS file path

### ICS Generation Pattern

```
Location: /root/arifOS/arifosmcp/sessions/hermes-briefings/
Naming: arif-fazil-[category]-events.ics
Format: iCalendar 2.0 (VCALENDAR/VEVENT blocks)
Content: DTSTART, DTEND, SUMMARY, DESCRIPTION, LOCATION, URL, STATUS, CATEGORIES
```

### Key Sources for Event Research

| Category | Sources |
|----------|---------|
| Bodybuilding | npcmalaysia.com, mfbb.com.my, hyrox.com, arnoldsportsfestival.com, borneopost.com |
| AI/Tech | superai.com, gitexasia.com, imda.gov.sg, aisingapore.org, techinasia.com |
| Fitness Race | hyrox.com (HYROX KL December confirmed for Malaysia) |
| Regional | depa.or.th (Thailand), enterprise singapore.gov.sg (SWITCH) |

### Confirmed Events (as of 2026-05-17)

| Event | Date | Venue |
|-------|------|-------|
| SuperAI 2026 | 10-11 June 2026 | Marina Bay Sands, Singapore |
| GITEX AI Asia 2027 | 29-30 April 2027 | Marina Bay Sands, Singapore |
| HYROX Kuala Lumpur | December 2026 | Kuala Lumpur, Malaysia |
| 60th Mr Sarawak | June 2026 | Kuching, Sarawak |
| Mr Olympia 2026 | September 2026 | Las Vegas, USA |
| SEA Games 2027 | Q3 2027 | Kuala Lumpur, Malaysia |

---

*Last updated: 2026-05-17 | Added: Briefing System + World Model Agent philosophy | Event Calendar Research class*
*Policy for Hermes human-life cron stack*