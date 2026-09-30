---
name: agent-message-store-forensics
description: "Use when asked what someone said to the agent."
version: 1.0.0
owner: curator
triggers:
  - "probe his chat logs"
  - "what did he say to you last night"
  - "did he ever message you privately"
  - "anything emergency in her messages"
  - "what did I miss in that group"
  - "read the last 24h of that chat"
  - "does the record show X"
tags: [telegram, state-db, evidence, provenance, reporting, curator]
---

# Agent Message-Store Forensics

Recover and report **another person's traffic with the agent**, from the agent's own stores, with the
search space named. Fires on:

- "probe his chat logs — anything emergency in his messages?"
- "what did X say to you last night?"
- "did he ever message you privately?"
- "what did I miss in that group?"

The deliverable is a **record-grounded answer**: quotes carrying timestamp and channel, plus an
explicit statement of what the probe could *not* find. Memory is not evidence. What a previous turn
said about the store is not evidence either.

## PROCEDURE

1. **Scope it before querying.** Which person, which window, which question — an emergency scan, a
   topic, or one absence claim. If the question is an absence ("did he ever…"), the deliverable is
   the **search space plus the result**, not a bare yes/no.
2. **Inventory the person's sessions** across every store. Match by `user_id` **and** by the group
   `chat_id` — never by `session_key` alone.
3. **Sweep their own words** for the question's terms, tagging each hit with its channel (DM vs
   group), because *privately* vs *in the room* is usually the real question.
4. **Pull a recency window verbatim** — the last N days of their `role='user'` rows, full text.
   Passes 2–3 locate; this pass produces the quotes.
5. **Read the graded artifacts before composing.** Lane memory for that person, the admitted-facts
   register, and any prior audit or falsification ledger on the subject. A prior audit's negative
   findings are **findings**: do not silently re-derive them, and do not resurrect what it downgraded.
6. **Compose** per the reporting contract below.

## CORE RULES

1. **Match sessions by `session_key` AND `chat_id`.** The live group session is
   `agent:main:telegram:group:<chat_id>` with **no** user suffix; only archived per-sender turns
   carry `…:group:<chat_id>:<user_id>`. A person-scoped filter silently omits everything said in the
   room today, and the omission reads to the human as "he never said it".
2. **`messages` has no `chat_id`.** Sessions carry it; messages carry `session_id`. Querying
   messages by chat_id returns nothing and proves nothing.
3. **Inside a group session the sender is in the body, not the row.** The gateway stamps
   `[DisplayName|<user_id>]` into the content; `display_identity` is a blob, not JSON. Filter on the
   body tag when asking what one person said in a shared room.
4. **Two content classes are envelopes, not speech — never quote them as the person's words.** Rows
   beginning `Gateway message origin (…)` are transport metadata; `[CONTEXT COMPACTION — REFERENCE
   ONLY]` blocks are summaries of earlier turns. Both arrive with `role='user'`.
5. **Filter `role` deliberately and cap output length.** A keyword sweep that includes `role='tool'`
   returns page scrapes and tool payloads, not conversation — an unfiltered multi-store sweep can
   return hundreds of thousands of characters in one call and bury the finding. Person-words queries
   use `role='user'`, drop the envelope prefixes, and print a short per-row window; the full text
   stays in the store and the window is enough to decide what to pull verbatim.
6. **Convert the timestamp in the query.** The store is UTC; convert to the human's zone in SQL so
   quotes carry the time they actually lived.
7. **Never open the live store read-write to answer a question.** The gateway is writing to it. Use
   read-only access (`sqlite3 -readonly`, or a `file:…?mode=ro` URI), one store at a time.
8. **A negative about your own stores needs the same warrant as a positive.** "There is no DM
   between us", "I checked — he never messaged privately", "nothing about that in my files" are
   claims until re-queried across every store. This is the highest-cost failure in this class: a
   false absence hands the human a wrong world to decide in.
9. **Base rate before signal.** Before reading a person's mention of a topic as diagnostic, count
   how often **each party** raises it in the same corpus. In a two-person channel the topic is often
   a shared idiom of the dyad, and the human may raise it more often than the subject. Compute the
   rate, then read *position in the sequence* and *register* — never the bare mention.
10. **A first-person statement upgrades a prior negative — say so.** When the subject's own words
    contradict an earlier "no evidence of X", name the upgrade and its evidence class. A stale
    negative repeated after new first-party evidence is the same defect as fabrication.
11. **Creative artifacts are firewalled.** Persona bibles, synthetic-voice scripts, generated
    imagery, and group banter that an agent later wrote down as a trait are **fiction about a real
    person**. If you cannot say which layer a claim lives in, you cannot use it as evidence.
12. **NOT FOUND must name the search space.** "Scanned the DM, the group, and the lane files; no such
    request appears" is a finding. "I couldn't find it" is not. This matters most when the human
    attributes a fact to the agent with confidence — the human's certainty is not a source.
13. **`ls` can stop short of a nested directory, and dossier trees are often mode-restricted or
    symlinked into another tree.** Follow up with `find`, and check where a path resolves, before
    declaring material missing.

## QUERY SHAPES

Stores: `~/.hermes/state.db` (main), `~/.hermes/profiles/<profile>/state.db` (per profile — a person
may have traffic in more than one). Schema: `sessions(id, user_id, session_key, chat_id, chat_type,
display_name, started_at, last_activity_at, message_count)`; `messages(id, session_id, role, content,
timestamp)`; `timestamp` is a Unix float in UTC.

```sql
-- inventory: who is this person in the store?
SELECT id, chat_type, display_name,
       datetime(last_activity_at,'unixepoch','+8 hours'), message_count
FROM sessions
WHERE user_id = :uid OR chat_id = :dm_chat OR chat_id = :group_chat
   OR session_key LIKE '%' || :uid || '%'
ORDER BY last_activity_at DESC;

-- the person's own words on a topic, channel tagged
SELECT datetime(m.timestamp,'unixepoch','+8 hours'),
       CASE WHEN s.chat_id = :dm_chat THEN 'DM' ELSE 'GROUP' END,
       substr(replace(m.content, char(10), ' '), 1, 300)
FROM messages m JOIN sessions s ON s.id = m.session_id
WHERE m.role = 'user' AND m.content IS NOT NULL
  AND (s.chat_id IN (:dm_chat, :group_chat) OR m.content LIKE '%' || :uid || '%')
  AND (m.content LIKE '%term1%' OR m.content LIKE '%term2%')
  AND m.content NOT LIKE 'Gateway message origin%'
  AND m.content NOT LIKE '%CONTEXT COMPACTION%'
ORDER BY m.timestamp;

-- recency window, verbatim (cutoff stated in LOCAL time)
SELECT datetime(m.timestamp,'unixepoch','+8 hours'), m.role, m.content
FROM messages m
WHERE m.session_id = :sid AND m.role IN ('user','assistant')
  AND m.content IS NOT NULL AND length(m.content) > 60
  AND m.timestamp > strftime('%s', :cutoff) - 8*3600
ORDER BY m.timestamp;
```

The `- 8*3600` converts a locally-stated cutoff into the UTC epoch the column stores. Getting the
sign wrong returns an empty window that then reads as an absence finding.

Sanity-check the inventory against `message_count`: a session with hundreds of messages is the live
room; zero-message rows are provisioned-but-unused stubs.

## REPORTING CONTRACT

- **Lead with the verdict.** For an emergency scan, the first line answers *is there anything that
  crosses the line* — then the detail.
- **If an earlier claim of yours was wrong, the correction leads the answer**, ahead of the content.
  The human is relying on it.
- **Then the items**, each with verbatim text, timestamp, and channel.
- **Then what remains unverified**, named explicitly.
- **Then one action, or silence.** No menus, no offer to go deeper, no method narration. Do not
  narrate the probe — deliver what it found.
- **Do not truncate a finding to fit the reply.** Long is long; the human asked for the record, not a
  summary of the record.
- **If the human says they do not understand the answer, change SHAPE, not volume.** A shorter copy
  of a framing that failed fails again and costs the turn twice. Re-say it as one plain sentence that
  names the thing.

DITEMPA BUKAN DIBERI ⚒️
