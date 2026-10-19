---
name: weekly-user-reflection
description: "Use when Arif asks for his weekly users reflection."
version: 1.0.0
tags: [hermes, telegram, state-db, reflection, weekly, forensics, arif]
---

# Weekly User Reflection (state.db deep read)

Recurring sovereign deliverable: every week Arif says *"weekly users reflection with HERMES"* and wants a DEEP read of state.db + the week's Telegram chat logs, detailing insights, meaning interactions, frictions, drifts, shadow bangang, eureka wisdoms, and new skills/capabilities gained. This is a human-meaning task, not an ops report — the output must read like someone who KNOWS him, not a system that ran SQL.

## Procedure (order matters)

1. **Find the LIVE Telegram store.** The DB with `source='telegram'` is the profile store — NOT `/root/HERMES/state.db` (CLI/subagent/cron only). Verify before trusting any number:
   ```
   sqlite3 <db> "SELECT DISTINCT source FROM sessions;"
   ```
   If you don't see `telegram`, you're in the wrong DB. On this host the live one is `/root/.hermes/state.db` (it also holds `cli`/`cron`/`subagent` — filter by source or chat_id, don't blanket-sum).

2. **Per-chat volume for the week.** Timestamp window is epoch SECONDS rendered `+8 hours` (MYT). Group `chat_id` is NEGATIVE (SADO/ALPHA-ZEN = `-1003815535761`, AAA = `-1003753855708`); DMs use the raw user id (Arif = `267378578`).

3. **Role + per-day breakdown** to see the rhythm (assistant/tool vs user; which days were heavy).

4. **Token burn by chat** via `session_model_usage` — NEVER `messages.token_count` (reads 0 across the board). Cost is unreliable (`cost_status='unknown'` mostly); treat token counts as the signal.

5. **Split the sovereign's messages by length.** `<~500 chars` = his REAL words ("voice"); `>=500` = pasted docs/artifacts/logs. Extract ONLY the short ones chronologically to reconstruct the week's actual emotional + decision arc. Reading the pastes wastes budget and hides the human. (`EXTERNALIZED:` lines and `[The user sent a document...]` lines are pastes — skip.)

6. **Read group chats separately** (SADO/ALPHA-ZEN, AAA) for the relational layer — who else talked, what the sibling agents did in human rooms.

7. **New skills/capabilities:** `find /root/.hermes/skills /root/AAA/skills -name SKILL.md -newermt '<week-start>' | sort`. Rank by VALUE to him, not count.

8. **Model usage** by input tokens for the week (which model carried the load).

## The deliverable shape Arif wants (write to THIS frame)

- Open with **one line that carries the whole week** — the single question/theme running underneath everything (he answers "am I dijaga?" through Syed, Izzu, Kak Su, Anwar, the whole build).
- **Polarities he oscillates between** (body/affection vs build/sovereignty) — name them without judging; holding both without labeling is the job.
- **Frictions** — where it hurt, each tied to a concrete repeated signal.
- **Shadow bangang** — his agents' errors AND sibling agents' errors (relational leaks, process-narration in human rooms, disclaimers he didn't ask for, calibration misses).
- **Eurekas** — insights HE forged himself (name them as his, not yours).
- **New skills/capabilities** — value-ranked.
- Close with **the single thing to carry into next week** — usually one of his own invariant phrases, restated as the operating truth.

## Output rules (his standing preferences — non-negotiable)

- BM Penang kampung, `aku`/`hang`, no `saya`. No flattery. No jargon, no doctrine names, no floor/table/state narration in the body.
- No markdown tables. Bullets or short labeled lines.
- Human language, not system language. It is a reflection, not a status report.

## Pitfalls

- **Never surface a third person's content outside its own chat** — state.db holds other humans' private data (Syed's, Izzu's, family). The reflection goes to the sovereign only; keep others' specifics out of any shared room.
- **messages.token_count is 0 — always pivot to session_model_usage** or you'll report "nobody burns anything."
- **Timestamp = epoch seconds, not millis** — dividing by 1000 yields 1970 dates. Render `datetime(x,'unixepoch','+8 hours')`.
- **Short-vs-long split is the whole trick** for finding the human in 12k rows; without it you drown in pasted PDFs and miss his actual words.
- **Don't confuse a sibling agent's process chatter with meaning** — IRFANclaw/ASI "Working… / provider down… / re-sending…" lines in a group are noise that cluttered a human room; flag it as bangang, don't relay it as content.
