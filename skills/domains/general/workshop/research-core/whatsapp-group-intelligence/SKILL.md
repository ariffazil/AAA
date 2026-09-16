---
name: whatsapp-group-intelligence
description: "Analyze exported WhatsApp group chats to extract key people, power structures, event details, and social dynamics. Combines structural and emotional"
triggers:
  - "whatsapp chat export"
  - "group chat analysis"
  - "who should I meet"
  - "reunion attendee analysis"
  - "event decision support"
---

# WhatsApp Group Intelligence

Analyze exported WhatsApp group chats to extract actionable social intelligence.

## When to Use

- User shares a WhatsApp chat export (.zip or .txt)
- User asks "who should I meet" at an event
- User is deciding whether to attend a gathering
- User needs a reply drafted for a specific person in the group

## Step-by-Step Protocol

### 1. Extract & Structure

- Unzip if needed. Typical exports: `.txt` chat log + `.vcf` contacts
- Identify group name, creation date, creator
- Count total messages, date range, active participants

### 2. Map the Power Structure

Extract from the chat:
- **Admins/Creators** — who created the group, who has admin
- **AJK/Committee** — formal roles (president, treasurer, logistics, etc.)
- **Connectors** — people who add others, tag people, bridge subgroups
- **Anchors** — most active, highest message count, keep the group alive
- **Lurkers** — added but rarely/never spoke

### 3. Profile Key Individuals

For each named person, extract:
- **Name** (from WhatsApp display name or mentions)
- **Phone** (if visible)
- **Role** in group (admin, AJK, connector, anchor)
- **Profession/industry** (if mentioned in chat)
- **Personality signals** — humor style, leadership energy, warmth
- **Notable quotes** — anything that reveals character

### 4. Match to User's World

Cross-reference identified people against the user's:
- **Industry** (e.g., petroleum engineering, AI, geoscience)
- **Background** (e.g., same university, same hometown)
- **Interests** (e.g., tech, business, creative)
- **Emotional needs** (e.g., needs warmth, needs professional peers, needs someone who remembers the old days)

Produce a ranked list: who to meet first, who to avoid, who's the safe entry point.

### 5. Event Context

From the chat, extract:
- Event date, venue, time
- Attendance numbers (paid/confirmed vs total group)
- Dress code, program flow, special activities
- Last-minute updates or changes

### 6. Emotional Intelligence Layer

Read between the lines:
- **Identity gap** — is the user carrying weight (institutional, personal) that the group doesn't know about?
- **Social anxiety signals** — "I kinda feel not going" = needs permission, not persuasion
- **Institutional pressure** — MSS, rightsizing, career uncertainty = walking into "so kerja mana?" is a minefield
- **Introvert protection** — user may need a safe entry point, not a full social agenda

### 7. Reply Drafting

When asked "what to reply to X":
- Match tone to the person's energy in the chat (casual, warm, formal)
- Keep it short — no over-explaining, no excuses
- Preserve the relationship bridge for future
- Suggest 2-3 options: warm, minimal, and one with light humor

## WhatsApp Screenshot Analysis (multimodal, not export)

When the input is a **screenshot image** of a WhatsApp chat rather than a text export, the group/export protocol does not apply. Full protocol (quote-bar vs new-text separation, left/right speaker attribution, ledger-before-interpretation, the three live-caught failure modes): **`references/whatsapp-screenshot-analysis.md`**. Prime rule: load and ledger the image BEFORE interpreting — never narrate from the user's relayed fragment of a screenshot.

## 1:1 Tenure Exports (relationship ledger, not group chat)

When the import is a single long 1:1 DM export and the user wants to know *what the decade was*, the group protocol doesn't apply. Full protocol (parse regex, initiation attribution, silence-gap ranking, keyword→next-reply windows, final-stretch read, pronoun trap, F5 privacy floor): **`references/1on1-tenure-analysis.md`**.

## Event-Anchored Retrieval & Temporal Anchoring

When the user names an external event ("the Genting concert", "the court date") and asks what the chat said around it, or when any analysis explains behavior by dates/calendars/roles: **`references/event-anchored-retrieval.md`** — exact-date verification, reading the chat window around the anchor, and the two fabrication traps observed in the wild (day-of-week from memory; current job title back-projected onto a past window).

## Cross-Medium Verification (MANDATORY when prior maps exist)

Before building or presenting any relational analysis, check if shadow maps, dossiers, or prior claims exist for the subject. If they do:

1. **Run quantitative probes first.** Parse the export (regex, per-sender counts, initiation attribution, silence gaps, keyword windows, time-of-day). Numbers come before narrative.
2. **Falsify prior claims against the data.** For every claim in an existing map, find at least two data points in the export that support it. If unsupported → flag as UNSUBSTANTIATED.
3. **Compare across communication mediums.** WhatsApp private DM ≠ Telegram group ≠ voice call. Different spaces produce different dynamics. Never merge them into one narrative without noting the medium.
4. **Quantify mundane vs dramatic.** Count logistics messages (location, time, food, parking) vs emotional messages (rindu, sedih, sorry, worship). If 80% is logistics, say so — don't reframe logistics as "confessional disguised as logistics."

**Failure pattern (observed 8/20):** Agent built a 752-line "complete relationship map" from limited sources (one heart-to-heart, one Telegram group, voice notes) and presented it as comprehensive. When confronted with actual 4,300-message WhatsApp export + real-time Telegram gateway logs, almost every dramatic claim was UNSUBSTANTIATED. The map was built from 20% emotional moments amplified into 100% of the relationship. The other 80% — logistics, mundane care, silence — was the actual relationship.

## Output Format

```
## Group Summary
- Group name, date range, message count
- Total participants, active vs lurkers

## Power Structure
- Creator, admins, AJK roles
- Top 5 anchors by activity

## People to Meet (ranked for user)
1. **Name** — role, why they matter for THIS user
2. ...

## People to Skip
- Name — reason

## Event Details
- Date, venue, program

## Emotional Read
- What the user is really feeling
- What they need to hear (honest, not motivational)
- Safe entry strategy
```

## Pitfalls

- **Don't assume professions** from phone numbers. Only label what the chat explicitly states.
- **Don't over-analyze lurkers.** They might just be private, not disinterested.
- **Don't push attendance.** If the user decides not to go, respect it. The analysis still has value for future events.
- **Privacy awareness.** Phone numbers and names are sensitive. Don't store them beyond the session context.
- **Don't web-search participants.** The chat export is the source. External lookup crosses a privacy line.
- **BM/English mix.** Malaysian WhatsApp chats are typically BM-English code-switched. Parse both.
- **Don't amplify 20% into 100%.** Emotional/salient moments are vivid but unrepresentative. If a keyword appears 3 times in 4,300 messages, it's a data point, not a theme. Always present frequency alongside the quote.
- **Never explain past behavior with a CURRENT role/schedule.** Verify the person held the job at that date; if the start date is unknown, leave the hole open. (Live catch 8/20: "cuti cikgu" framing for Aug 2024 — subject only became a teacher Apr 2026.)
- **Weekdays and case statuses are never recalled — they are looked up.** `date -d` for days; source documents for legal/medical/financial status. Stale memory is the #1 fabrication vector in family narratives.
