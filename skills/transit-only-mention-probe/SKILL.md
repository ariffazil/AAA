---
name: transit-only-mention-probe
description: "Probe session DB before describing a name."
version: 1.0.0
tags: [human-reality, person-intelligence, falsification, held_out]
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# Transit-only Mention Probe

A name can appear hundreds of times across dozens of sessions and still be **transit-only**: the named person never produced a single line in the corpus. The hit count grants visibility, not knowledge. Without this probe, an agent silently upgrades a reflexive corpus (principal talking ABOUT X) into a primary corpus (X talking) and presents X as if X had been interviewed.

## When to use

- A name surfaces that you've never seen as a direct chat participant
- grep across state.db returns high counts for a name
- Principal asks "siapa [name]" and name is not in `people.yaml`
- Before writing any portrait, dossier, or held_out entry

## Probe (run before any descriptive writing)

```
DB=/root/.hermes/state.db

# Total hits
sqlite3 "$DB" "SELECT COUNT(*) FROM messages WHERE LOWER(content) LIKE '%<name>%' COLLATE NOCASE;"

# Role distribution — does the named person ever produce content?
sqlite3 "$DB" "SELECT role, COUNT(*) FROM messages
  WHERE LOWER(content) LIKE '%<name>%' COLLATE NOCASE GROUP BY role;"
# If a foreign telegram_user_id appears in a user-role row, person IS direct participant.
# If every user-role hit is the principal's own sender_id, person is transit-only.

# Date bounds
sqlite3 "$DB" "SELECT datetime(MIN(timestamp),'unixepoch'), datetime(MAX(timestamp),'unixepoch')
  FROM messages WHERE LOWER(content) LIKE '%<name>%' COLLATE NOCASE;"
```

## Three buckets

| Bucket | Signature | Treatment |
|---|---|---|
| `direct_participant` | user-role rows from a foreign sender_id | Normal corpus reading. Full lane card possible after F13 admission. |
| `transit_only` | user-role hits are all principal's own sender_id | Held_out entry in `people.yaml` (scope=dm). Tag every fact `[src: principal relay, conf ≤0.7]`. Never broadcast. Never dossier. Promote only if person themselves contacts the agent. |
| `shadow_only` | name appears only in hermes_rasa / hermes_shadow tool outputs | Do NOT record in `people.yaml`. Shadow organs report classes, not people. |

## Why the count lies

443 mentions over 14 sessions, sorted by session_id, reads as "I know this person." Sorted by **role**, the same 443 reads as "principal mentioned 128, agent echoed 144, tool traces 171, zero utterances from the named person." First framing produces a confident reading; second produces held_out. Same corpus, opposite deliverable.

## Triangle/buffer pattern

When X is mentioned only in the context of A's bond with B (X = B's secret client), resist interviewing X's interior. Read X's structural position in the social graph only — who is the buffer, who protects whom from whom — and hold X's motive and feelings as X's domain. Never promote transit-only to dossier even at high hit counts.

## Single-line test

Before writing a portrait of X, can you point to a single message where X themselves said something? If no → held_out, no portrait. If yes → proceed normally.

## Pitfall — refusing to look

The reflex failure mode is to skip the probe because the name "feels known." That reflex is exactly what this skill counters. The probe is three SQL queries; it costs less than one paragraph of confident wrong prose.
