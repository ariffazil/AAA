---
name: conversation-record-forensics
description: Use when probing what a person said in agent stores.
version: 1.0.0
author: Hermes
license: arifOS
tags: [state-db, attribution, evidence, probe, absence]
metadata:
  hermes:
    category: evidence
    tags: [state-db, attribution, probe, absence]
    related_skills: [telegram-ops, corpus-claim-discipline, local-memory-retrieval]
triggers:
  - what did X actually say, write or ask me
  - probe his chat logs
  - a claim about a person is about to be stated from a partial probe
  - did he ever mention Y, presence or absence
  - answering from one room about a person who writes in several
capability_tier: fed-long-context
ecology_state: WARM
---

# Conversation Record Forensics

Recovering and attributing what a real person actually said inside the agent's own message stores.
This owns the EVIDENCE step: which store, which join, which witness proves who typed a line, and what
counts as proof of ABSENCE. Routing, delivery and lane doctrine live in `telegram-ops`; this skill is
the read side.

## 1. Enumerate every store before answering

The same person can hold parallel threads across one store per profile. Sweep all of them; a
single-DB answer is a partial census presented as a whole one.

```
state.db · shared-state.db · profiles/<name>/state.db
```

Layout differs between hosts — enumerate rather than hardcoding:

```bash
for f in state.db shared-state.db profiles/*/state.db; do
  echo "=== $f"; sqlite3 -readonly "$f" '.tables'
done
```

Open read-only (`sqlite3 -readonly`, or `file:...?mode=ro` in Python). A live gateway writes to these
files while you read; never take a write lock to answer a question.

## 2. Sessions carry the room, messages carry the words

`sessions` holds `id, source, user_id, session_key, chat_id, chat_type, display_name`. `messages`
holds `session_id, role, content, timestamp` — and **no chat_id**. Join through `sessions`.

- **A DM thread** = `sessions.chat_id = <user_id>` with `chat_type = 'dm'`.
- **A group** = one session row per chat, `chat_id` negative, with no per-sender session.

## 3. Who typed it — three candidate witnesses, only two trustworthy

In a shared room the sender is **tagged inline at the head of the content**, `[<display_name>|<user_id>]`.
That tag is the witness to use:

```sql
SELECT s.chat_id, m.role, datetime(m.timestamp,'unixepoch','+8 hours'), m.content
FROM messages m JOIN sessions s ON s.id = m.session_id
WHERE m.role = 'user'
  AND (s.chat_id = '<uid>'                      -- their DM
       OR m.content LIKE '%[%|<uid>]%')          -- their turns in shared rooms
ORDER BY m.timestamp;
```

Traps, each of which silently drops evidence:

- **`session_key` uses two shapes.** Older group sessions carry a per-user suffix
  (`…:group:<chat_id>:<user_id>`); newer ones do not. Filter on `session_key` alone and you lose half
  the person's turns; filter on the in-content tag alone and you lose the older ones. Check both.
- **`messages.display_identity` is a short opaque BLOB, not JSON.** Do not parse or decode it; it
  carries no readable sender identity.
- **A body carries more than the human's words.** Strip before counting or diffing: the gateway
  origin block (`Gateway message origin (JSON …)` and its trailing "Do not guess a reply destination"
  line) is runtime metadata nobody typed; an inline re-quote (`[Replying to: …]`) duplicates an earlier
  message and inflates any word count; a compaction or handoff block pasted into a `user` row is not a
  message the human sent. Keep the origin block only when you need a per-message `user_id`.
- **An attachment line is a pointer, not content.** `<Media omitted>` or "[The user sent an image…]"
  means the artefact is not in the text store at all — say so rather than reasoning as if you read it.

## 4. Absence is a claim and gets the same probe as presence

Before asserting that someone never did something, never wrote, or that no thread or lane exists, run
the count and report it.

```sql
SELECT count(*), min(timestamp), max(timestamp)
FROM sessions WHERE chat_id = '<uid>' OR user_id = '<uid>';
```

Generalising from the room you are standing in to the whole account is how an agent tells a human, to
his face, that a live private thread of hundreds of messages does not exist. **Phantom absence and
ghost capability are the same defect with the sign flipped.** When the count contradicts the claim, say
so in one line and move on — a corrected absence beats a defended one.

## 5. Grade the claim before it becomes a finding

- Separate what the person WROTE from what was INFERRED about it. A message is a datum; its meaning is
  a hypothesis. Label them differently in output and never upgrade one into the other by repetition.
- A person appearing once in a long record is itself a finding — report the single occurrence and the
  surrounding silence as one fact, not as a trend.
- Absence of a record is UNKNOWN, never no. "No entries in that window" is a complete, honest answer;
  inventing a motive to fill the gap is the failure this class exists to prevent.
- Deliver in the register the human asked for and drop the plumbing (table names, SQL, file paths)
  unless he asks how you know.

## Pitfalls

- **Never answer a person question from one room's context.** Probe first, then speak — the correction
  is cheap before the sentence and expensive after it.
- **A partial probe reported as a full one is worse than no probe.** Name which stores you swept and
  which you did not.
- **Do not model the person while you extract.** The read side produces lines and counts; interpretation
  is a separate, clearly-labelled step with its own honesty budget.
