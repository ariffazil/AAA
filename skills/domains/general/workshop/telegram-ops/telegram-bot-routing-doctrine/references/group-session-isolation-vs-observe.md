# "Bot tak nampak previous message dalam group" — observe vs session isolation

Diagnosed 2026-08-12 (SADO group, Syed's Hooligan V6 question). Reported as "agent can't
read previous message in the same group." The intuitive first fix — "inject observed-group
context" — was WRONG. This is the ground-truth diagnostic path.

## The two mechanisms (only one is usually real)

### 1. `require_mention` and `observe_unmentioned_group_messages` are MUTUALLY EXCLUSIVE

Code path: `adapter.py` → `_should_observe_unmentioned_group_message()`:

```python
if not self._telegram_observe_unmentioned_group_messages():
    return False
...
if not self._telegram_require_mention():
    return False   # require_mention=false KILLS observe entirely
```

- Observe only activates when `require_mention=true` (bot silent unless @'d, stores the rest).
- When `require_mention=false` (the arifOS default on Hermes), EVERY group message is a full
  dispatch turn — there is NO observe path at all.
- A chat in `free_response_chats` is dispatched, never observed (`_should_observe` returns
  False for it).
- Default for `observe_unmentioned_group_messages` = **false** (line 6892). Often never configured.
- **A diagnosis table claiming BOTH `require_mention=false` AND `observe=true` is
  self-contradictory** — verify against live config before trusting it.

### 2. The real cause is usually SESSION ISOLATION, not an observe gap

Groups accumulate MULTIPLE sessions split by idle gaps (session rotation / scale-to-zero).
A new session starts with an EMPTY context — it does not carry the previous session's
history. "Didn't see what Syed said earlier" almost always means "it was in an older
session," not "the observe pipeline dropped it."

Observed SADO group: 4+ separate sessions (271 / 93 / 87 / 136 msgs) split by time gaps.
The Hooligan question lived in an old session; the current session had no memory of it.

## Ground-truth check — the live `state.db` `observed` column

```bash
# NOTE: /usr/local/lib/hermes-agent/sessions.db is EMPTY (0 bytes) — NOT the live store.
# The live store is the profile state.db the running gateway keeps open:
cd /usr/local/lib/hermes-agent/profiles/aaa-hermes   # (or HERMES_HOME/profiles/aaa-hermes)
python3 -c "
import sqlite3; db=sqlite3.connect('state.db')
# find group sessions
for r in db.execute(\"SELECT id, substr(title,1,40), chat_id, message_count FROM sessions \
  WHERE chat_id='-1003815535761' ORDER BY started_at DESC LIMIT 8\"): print(r)
# per-session: are user msgs observed=0 (real turn) or observed=1 (stored-only)?
for r in db.execute(\"SELECT role, observed, substr(content,1,50) FROM messages \
  WHERE session_id='<sid>' AND role='user' ORDER BY id DESC LIMIT 15\"): print(r)
"
```

- All user messages `observed=0` → every message WAS a real turn; observe never ran.
  Fix lies in cross-session continuity (session-linking / lane-memory carry), NOT injecting
  observed context (which would double-process an already free_response chat).
- Any `observed=1` → observe pipeline active; then the inject-gap fix is legitimate.

## Diagnosis discipline (the actual lesson)

Verify the reporter's diagnosis against live code + data BEFORE accepting it. Probe the
adapter source, the live config, and state.db. Agree with truth, not with the person —
even when the person is the sovereign and hands you a labelled evidence table. Show the
evidence for the contradiction (mutual exclusion + observed=0) rather than executing the
suggested (wrong-target) fix.