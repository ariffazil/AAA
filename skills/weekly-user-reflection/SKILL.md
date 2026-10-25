---
name: weekly-user-reflection
description: "Use when Arif asks for his weekly users reflection."
version: 1.1.0
tags: [hermes, telegram, state-db, reflection, weekly, forensics, arif]
floor_scope: [F2, F4, F9, F12]
autonomy_tier: T1
---

# Weekly User Reflection (state.db deep read)

Recurring sovereign deliverable: every week Arif says *"weekly users reflection with HERMES"* and wants a DEEP read of state.db + the week's Telegram chat logs, detailing insights, meaning interactions, frictions, drifts, shadow bangang, eureka wisdoms, and new skills/capabilities gained. This is a human-meaning task, not an ops report — the output must read like someone who KNOWS him, not a system that ran SQL.

## Procedure (order matters)

1. **Find the LIVE Telegram store.** The DB with `source='telegram'` is the profile store — NOT `/root/HERMES/state.db` (CLI/subagent/cron only). Verify before trusting any number:
   ```
   sqlite3 <db> "SELECT DISTINCT source FROM sessions;"
   ```
   If you don't see `telegram`, you're in the wrong DB. On this host the live one is `/root/.hermes/state.db` (it also holds `cli`/`cron`/`subagent` — filter by source or chat_id, don't blanket-sum).

2. **Per-chat volume for the week.** Timestamp window is epoch SECONDS rendered `+8 hours` (MYT). Group `chat_id` is NEGATIVE (SADO/ALPHA-ZEN/APEX-ZEN = `-1003815535761`, AAA = `-1003753855708`); DMs use the raw user id (Arif = `267378578`).

   The `messages` table has NO `source`/`chat_id`/`display_name` columns — every per-chat query must JOIN `sessions`: `FROM messages m JOIN sessions s ON s.id=m.session_id` then filter `s.source='telegram'`. Page long user-message dumps with `ORDER BY m.timestamp LIMIT n OFFSET k` instead of one giant query — a week is tens of thousands of rows and one shot buries the signal.

3. **Role + per-day breakdown** to see the rhythm (assistant/tool vs user; which days were heavy).

4. **Token burn by chat** via `session_model_usage` — NEVER `messages.token_count` (reads 0 across the board). Cost is unreliable (`cost_status='unknown'` mostly); treat token counts as the signal.

5. **Split the sovereign's messages by length.** `<~500 chars` = his REAL words ("voice"); `>=500` = pasted docs/artifacts/logs. Extract ONLY the short ones chronologically to reconstruct the week's actual emotional + decision arc. Reading the pastes wastes budget and hides the human. (`EXTERNALIZED:` lines and `[The user sent a document...]` lines are pastes — skip.)

6. **Read group chats separately** (SADO/ALPHA-ZEN, AAA) for the relational layer — who else talked, what the sibling agents did in human rooms. In group sessions EVERY inbound arrives as `role='user'` carrying a prefix tag that names the true sender: `[ARIF] [ARIF|267378578]` = Arif relaying through Hermes into the room (much of his real voice lives here, not only in the DM), `[FORGE]`, `[IRFANclaw🦞]`, `[Wawa]`, `[AIA]`, plus `[Replying to: "..."]` quote headers. Group and filter on these prefixes — `role='user'` alone tells you nothing about who spoke.

7. **New skills/capabilities:** `find /root/.hermes/skills /root/AAA/skills -name SKILL.md -newermt '<week-start>' | sort`. Rank by VALUE to him, not count.

8. **Model usage** by input tokens for the week (which model carried the load).

## The deliverable shape Arif wants (write to THIS frame)

- Open with **one line that carries the whole week** — the single question/theme running underneath everything (he answers "am I dijaga?" through Syed, Izzu, Kak Su, Anwar, the whole build).
- **Polarities he oscillates between** (body/affection vs build/sovereignty) — name them without judging; holding both without labeling is the job.
- **Frictions** — where it hurt, each tied to a concrete repeated signal.
- **Shadow bangang** — his agents' errors AND sibling agents' errors (relational leaks, process-narration in human rooms, disclaimers he didn't ask for, calibration misses).
- **Eurekas** — insights HE forged himself (name them as his, not yours).
- **Security & infra signals** — unresolved external disclosures (age them in days), credentials pasted into any chat, and recurring alert spam (count the repeats). These are usually his top action items; name each with the concrete next step only he can take.
- **New skills/capabilities** — value-ranked.
- Close with **the single thing to carry into next week** — usually one of his own invariant phrases, restated as the operating truth.

## Output rules (his standing preferences — non-negotiable)

- BM Penang kampung, `aku`/`hang`, no `saya`. No flattery. No jargon, no doctrine names, no floor/table/state narration in the body.
- No markdown tables. Bullets or short labeled lines.
- Human language, not system language. It is a reflection, not a status report.

## Pitfalls

- **Never surface a third person's content outside its own chat** — state.db holds other humans' private data (Syed's, Izzu's, family). The reflection goes to the sovereign only; keep others' specifics out of any shared room.
- **messages.token_count is 0 — always pivot to session_model_usage** or you'll report "nobody burns anything."
- **Never compare `m.timestamp >= strftime(...)` with a formatted time string** — `strftime` with
  `'+8 hours'` produces text, the comparison silently matches nothing, and you report an empty week.
  Compute the epoch integer in Python (UTC, minus 8h from the MYT wall-clock boundary) and pass the
  bare integer into the SQL. Verify with a `GROUP BY hour` probe before concluding "no messages".
- **Timestamp = epoch seconds, not millis** — dividing by 1000 yields 1970 dates. Render `datetime(x,'unixepoch','+8 hours')`.
- **Short-vs-long split is the whole trick** for finding the human in 12k rows; without it you drown in pasted PDFs and miss his actual words.
- **Don't confuse a sibling agent's process chatter with meaning** — IRFANclaw/ASI "Working… / provider down… / re-sending…" lines in a group are noise that cluttered a human room; flag it as bangang, don't relay it as content.
- **display_name is a label, not identity** — rooms get renamed mid-window (ALPHA-ZEN → APEX-ZEN), so the same chat_id appears under two names. Group by chat_id; grouping by display_name double-counts the room.
- **Substance hides in relay prefixes** — the deepest personal reads of a week often sit inside `[ARIF]`-prefixed group relays and `[Replying to:]` threads, not the DM. Skipping prefixed rows as 'system noise' throws away the human.
- **Fresh rows live in the WAL, not the main DB file** — during/after an active session the newest messages exist only in `state.db-wal`. A plain `sqlite3 /root/.hermes/state.db` query on the main file returns an older snapshot and you conclude "no messages today". Copy BOTH files to /tmp and query the copy:
  ```
  cp /root/.hermes/state.db /tmp/state_copy.db
  cp /root/.hermes/state.db-wal /tmp/state_copy.db-wal
  sqlite3 /tmp/state_copy.db "SELECT MAX(timestamp), datetime(MAX(timestamp),'unixepoch','+8 hours') FROM messages;"
  ```
  Verify the copy's MAX(timestamp) covers the window you need before saying "nothing there".
- **Mirror sessions double-record** — a gateway restart clones the live session into a second session_id holding the SAME conversation. Dedupe by timestamp+role+content-prefix before counting anything.
- **Other profiles' sessions share the DB** — cross-lane claims (ASI lane, other rooms) are readable from the same store; ground a claim in ONE lane before answering cross-lane questions, and never call a record "kosong" without a WAL-aware probe. Arif catches this class of miss every time.
- **Health topics of a third person stay out of shared rooms** — even a well-meant health tip about a named person must not be forwarded to any lane without the sovereign's direct order in THAT turn; the content can be right and the delivery still be a boundary breach. Keep health specifics (ECG results, medications, diagnoses) in the sovereign's lane only.
