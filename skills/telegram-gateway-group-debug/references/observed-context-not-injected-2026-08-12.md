# Observed Group Context NOT Injected — 2026-08-12 Session

## Symptom

Arif asked: *"My agents in other chat group cannot read previous message?? ... In the same group. Why Hermes agents cannot reflect previous message ??"*

Context: Syed had asked a question in SADO group. Agent replied but showed no knowledge of messages Syed (or anyone else) sent earlier in the same group. The agent acted as if each message arrived in isolation — no memory of the conversation thread.

## Investigation path

Eight source files traced end-to-end:

1. `plugins/platforms/telegram/adapter.py` — searched for `message_history`, `group_history`, `reply_context` (zero hits on those exact terms — naming is non-obvious)
2. Found `_observe_unmentioned_group_message()` at line 7512 — **stores** observed messages in transcript with `observed=True`
3. `_should_process_message()` at line 7575 — **gates** which messages the bot processes vs. observes
4. `_apply_telegram_group_observe_attribution()` at line 7319 — **binds** observed context to the current dispatched message
5. `_telegram_observe_allowed_chats()` at line 6945 — **the silent gate** that returns `set()` when `group_allowed_chats` not configured
6. `gateway/run.py:_build_gateway_agent_history()` at line 857 — **separates** observed rows from replay history
7. `gateway/run.py:_wrap_current_message_with_observed_context()` at line 993 — **prepends** observed block to current user turn
8. `gateway/session.py:append_to_transcript()` at line 2395 — **persists** with `observed=True` flag

## Root cause (one missing config key)

`_telegram_observe_allowed_chats()` reads `TELEGRAM_GROUP_ALLOWED_CHATS` env var OR `config.extra["group_allowed_chats"]`. Neither was set:

```bash
$ strings /proc/<PID>/environ | grep GROUP_ALLOWED_CHATS
# (empty)

$ grep group_allowed_chats config.yaml
# (not present)
```

Result: `_apply_telegram_group_observe_attribution()` short-circuits at line 7322:

```python
allowed = self._telegram_observe_allowed_chats()
if not allowed or chat_id_str not in allowed:
    return event  # no channel_prompt marker → pipeline halts
```

The channel_prompt never gets the `_TELEGRAM_OBSERVED_CONTEXT_PROMPT_MARKER` ("observed Telegram group context") string. Without that marker, `_uses_telegram_observed_group_context()` in `gateway/run.py:833` returns False, `separate_observed_context` stays False, and observed rows are never separated from regular history — they're just silently dropped from the agent's view.

## The fix (delegated to OpenCode)

Config-only change — add to `telegram:` section of config.yaml:

```yaml
telegram:
  group_allowed_chats:
    - '-1003815535761'   # SADO
    - '-1003521544074'   # AIA
```

Or env var: `TELEGRAM_GROUP_ALLOWED_CHATS=-1003815535761,-1003521544074`

No Python source changes. The entire pipeline already existed; it was just gated off by a missing config key whose absence produced no error and no log line.

## Why this is hard to find

1. The feature uses non-obvious naming: `observe_unmentioned_group_messages` (storage) vs `group_allowed_chats` (injection gate). They sound unrelated.
2. The silent return is by design (backward compat) — no warning, no debug log.
3. The bot still *responds* to @mentions correctly. The symptom only appears when the user expects the agent to *remember* prior context.
4. The `observed=True` rows ARE in state.db — so a DB inspection shows data is flowing. The break is between DB and agent prompt, not between Telegram and DB.

## Related env state (at time of finding)

```
TELEGRAM_OBSERVE_UNMENTIONED_GROUP_MESSAGES=true   ✅ (storage works)
TELEGRAM_REQUIRE_MENTION=false                     ✅ (bot responds to all)
TELEGRAM_FREE_RESPONSE_CHATS=…SADO,AIA…            ✅ (response gate open)
TELEGRAM_GROUP_ALLOWED_CHATS                       ❌ NOT SET (injection gate closed)
config.yaml telegram.group_allowed_chats           ❌ NOT SET
```

The first three being correct made it look like everything was wired. Only the fourth (a different config key serving a different purpose) was missing.
