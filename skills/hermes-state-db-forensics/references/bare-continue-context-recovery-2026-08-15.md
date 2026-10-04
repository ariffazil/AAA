# Bare-"Continue" context recovery (2026-08-15, SADO group)

Situation: session starts with a single word like "Continue" and zero prior
turns in the agent's context (group chat, session rotation, post-restart).
Never guess what to continue — reconstruct it from the store.

## The ladder that worked (in order)

1. `session_search()` — may hard-fail with the FTS5 shadow-table error
   (already a SKILL.md pitfall). Don't debug it; pivot immediately.
2. Open the profile store read-only and **discover schema before querying**:
   ```sql
   sqlite3 "file:/usr/local/lib/hermes-agent/profiles/aaa-hermes/state.db?mode=ro" \
     "SELECT name FROM pragma_table_info('sessions');"
   ```
   Guessing column names fails: `created_at`, `updated_at`, `m.created_at`
   do NOT exist. Real columns (verified this session):
   - `sessions`: `started_at`, `ended_at`, `last_activity_at`, `title`,
     `chat_id`, `chat_type`, `display_name`, `user_id`
   - `messages`: `timestamp` (epoch seconds), `role`, `content`, `token_count`
3. Find the live session for the chat: `WHERE chat_id='<group id>' ORDER BY
   last_activity_at DESC` — one group accrues MANY session rows over days
   (SADO had 6); the newest by `last_activity_at` is the live one.
4. Read the tail of that session (both `user` and `assistant` roles) to see
   the last exchange — that is what "Continue" refers to.
5. Cross-check the sender's OTHER recent sessions (DM rows for the same
   `user_id` / `display_name`) — "Continue" may point at work done in a DM,
   not the group. Compare `last_activity_at` across both.
6. If the tail references artifacts (videos, reports), verify them on disk
   (`ls -lt /root/HERMES/.out/`, `/root/forge_work/`) to know what actually
   exists before replying.

## Gotchas observed

- The incoming "Continue" message itself was NOT yet in `messages` at query
  time — the DB tail ends at the previous turn. Expected; the gateway
  persists asynchronously. Don't loop waiting for it.
- Reply register follows the recovered tail, not the task framing: the last
  SADO exchange was 1-2 line banter about generated videos "burning the
  server", so the correct "Continue" reply is one more line of that banter —
  not a status report.
- `datetime(timestamp,'unixepoch','localtime')` renders MYT correctly on
  this box; compare against `date` output to anchor "now" before deciding
  which session is live.
