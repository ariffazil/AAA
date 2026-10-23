---
name: telegram-gateway-group-debug
description: Diagnose "the bot doesn't reply in my Telegram group" — wiring a NEW group (invite links don't work for bots), the adapter gating chain, the DM-vs-group chat_id tell, the self-echo loop, and the free_response_chats config path. Use when a Telegram bot answers DMs but stays silent in groups, when a user drops a t.me/+ invite link asking to "test the bot", when "send in SADO" actually arrived as a DM, when the gateway log shows "Blocked unauthorized user <bot_id>" floods, or when require_mention/free_response_chats edits "do nothing" despite correct-looking config.
---

# Telegram Gateway — Group Message Debugging

A companion to `hermes-telegram-gateway-ops` (which covers identity, tokens, drop-ins, restart). This skill covers the specific failure class: **DMs work, groups don't.**

## The #1 rule — chat_id is truth

The gateway log line `inbound message: chat=<id> msg='...'` is definitive:

- `chat=267378578` (positive) = **DM** with user 267378578
- `chat=-1003815535761` (negative) = **group** SADO

If every log line for the user's "group test" shows `chat=<positive_user_id>`, they are typing in the bot's DM, not in the group. This is the most common cause of "bot doesn't reply in groups". Even experienced Telegram users confuse the bot's DM chat with the group chat.

**Verify with the user:** "Look at the chat header in Telegram. Does it say `ASI🪽` (bot DM) or `SADO` (group with members)?"

## The adapter gating chain

Inside `adapter.py` `_should_process_message(msg)`, the bypass order is:

```
1. _is_own_message          → drop bot self-echo (line 8341)
2. _is_group_chat?          → DMs return True immediately (line 8357)
3. allowed_topics           → empty = no filtering
4. ignored_threads          → empty = no filtering
5. _telegram_allowed_chats  → empty = passes all chats
6. _telegram_free_response_chats → BYPASS mention for specific chats ★
7. _telegram_require_mention → false = all messages pass
8. _is_reply_to_bot         → always passes
9. _message_mentions_bot    → always passes if @mentioned
```

`★` — the free_response_chats step is the key bypass. If a chat is in this set, mention is not required.

### How `free_response_chats` is read (adapter.py:7581-7587)

```python
raw = self.config.extra.get("free_response_chats")
if raw is None:
    raw = os.getenv("TELEGRAM_FREE_RESPONSE_CHATS", "")
```

Two paths:
1. **Root-level config.yaml** key `free_response_chats: ['-1003815535761']` → `config.extra.get()`
2. **Env var** `TELEGRAM_FREE_RESPONSE_CHATS=-1003815535761` → comma-separated

If it's only nested under the `telegram:` block, it may NOT be in `config.extra` depending on how the profile flattens keys. **Safest path: env var in the systemd drop-in.**

### Required env vars for "all groups reply" (nuclear option)

```ini
TELEGRAM_REQUIRE_MENTION=false
TELEGRAM_FREE_RESPONSE_CHATS=-1003815535761,-1003753855708
TELEGRAM_ALLOWED_CHATS=-1003753855708,-1003815535761,...
TELEGRAM_GROUP_ALLOWED_USERS=267378578,1042200555,...
```

Place in `/etc/systemd/system/hermes-asi-gateway.service.d/<name>.conf` with `chmod 600`, then `systemctl daemon-reload && systemctl restart hermes-asi-gateway`.

## The self-echo loop (auth gate ordering bug)

In `_handle_text_message` (line 8476), `_is_user_authorized_from_message` runs at line 8492 — **before** `_should_process_message` at line 8499. Inside `_should_process_message`, `_is_own_message` runs first at line 8341.

Result for every bot outgoing message:
```
webhook → _handle_text_message → auth check (line 8492) → bot_id NOT in allowlist
→ log "Blocked unauthorized user <bot_id>" → never reaches _is_own_message
```

**Log signature:**
```
WARNING [Telegram] Blocked unauthorized user 8410138119 in chat 8410138119
WARNING [Telegram] Blocked unauthorized user 8410138119 in chat 8410138119
```

**Tell:** `from_user.id == chat.id == bot_id`. Real messages never match this.

**Fix:** add `_is_own_message(msg)` check at the top of `_handle_text_message` (before auth, around line 8485). Bundled adapter — patch needs `cross_profile=True` and a T2 announce.

## Diagnostic commands

```bash
# 1. Did the group message arrive?
grep -E "1003815535761" /usr/local/lib/hermes-agent/profiles/<profile>/logs/gateway.log

# 2. What env vars does the running gateway have?
strings /proc/$(systemctl show -p MainPID hermes-asi-gateway.service | cut -d= -f2)/environ \
  | grep -E "FREE_RESPONSE|REQUIRE_MENTION|ALLOWED_CHATS|GROUP_ALLOWED"

# 2b. Zero entries for a specific user? → Telegram privacy mode suspect
grep -c '<user_id>' /usr/local/lib/hermes-agent/profiles/<profile>/logs/gateway.log
# If 0 across all log files → adapter never receives messages → privacy mode ON
# Fix: @BotFather → /setprivacy → Disable → remove+re-add bot to group

# 2c. Verify env var auth gate — is the user in the process env?
strings /proc/<gateway_pid>/environ | grep 'TELEGRAM_ALLOWED_USERS'
# If user_id is NOT in this list → silent drop at adapter auth gate

# 3. Synthetic webhook probe (bypass Telegram, test directly)
SECRET=$(strings /proc/<PID>/environ | grep '^TELEGRAM_WEBHOOK_SECRET=' | cut -d= -f2)
curl -sS -w "\nHTTP %{http_code}\n" \
  -H "X-Telegram-Bot-Api-Secret-Token: ${SECRET}" \
  -H "Content-Type: application/json" \
  -d '{"update_id":<unique>,"message":{"message_id":<id>,"from":{"id":267378578,"is_bot":false,"first_name":"Arif"},"chat":{"id":-1003815535761,"title":"SADO","type":"supergroup"},"date":<epoch>,"text":"probe"}}' \
  http://127.0.0.1:8444/telegram/webhook

# 4. Verify chat info
curl -s "https://api.telegram.org/bot<TOKEN>/getChat" -d chat_id="-1003815535761" \
  | python3 -c "import json,sys;d=json.load(sys.stdin)['result'];print(f'id={d[\"id\"]} type={d[\"type\"]} title={d[\"title\"]}')"
```

## "Does the bot have access to group X now?" — config truth vs. traffic proof (2026-08-15)

Two different questions hide inside "do we have access": (1) is the allowlist live in the running process, (2) has any message from the group ever actually arrived. Answer BOTH, separately, before reporting.

**Ladder (in order):**

1. **Live process env** — config.yaml and drop-ins can lie; `/proc` can't. Find the gateway PID from its self-report file first:
   ```bash
   PID=$(python3 -c "import json;print(json.load(open('/usr/local/lib/hermes-agent/profiles/aaa-hermes/gateway_state.json'))['pid'])")
   tr '\0' '\n' < /proc/$PID/environ | grep -E 'TELEGRAM_GROUP_ALLOWED_CHATS|TELEGRAM_ALLOWED_CHATS'
   ```
   (`gateway_state.json` in the profile dir carries `{pid, gateway_state, platforms.telegram.state}` — faster than `ps aux` archaeology in multi-bot topology; cross-check `/proc/<pid>` exists since the file survives crashes with a stale PID. Note `tr '\0' '\n'` works; plain `strings` also fine.)
   Chat ID present in BOTH `TELEGRAM_GROUP_ALLOWED_CHATS` (observe gate) and `TELEGRAM_ALLOWED_CHATS` (response gate) = door open.
2. **Webhook health** — `getWebhookInfo` (token read from the same /proc env, never from config): `url` set + `pending_update_count: 0` = Telegram side healthy, queue empty. Proves nothing about past delivery.
3. **Traffic proof** — the ONLY evidence a group message ever arrived:
   ```bash
   grep -a '<group_chat_id>' /usr/local/lib/hermes-agent/profiles/aaa-hermes/logs/gateway.log | tail -5
   ```
   Look for `inbound message: ... chat=<group_chat_id>`. Remember TWO homes exist: `/root/.hermes/logs/` (CLI) and the profile dir — gateway.log lives in the profile dir (fd of the gateway process points there).

**The at-most-once delivery rule:** a message sent while the gateway process was down, or while the chat was not yet in the allowlist env, is consumed and dropped forever — Telegram does NOT redeliver after the config lands later. Signature: everything green (env live, webhook healthy, `pending_update_count: 0`) but ZERO gateway.log lines for the chat_id → the user's earlier test was swallowed during the config window and will never arrive. Do not wait for it or promise redelivery — tell the user to send a NEW message in the group.

**Tells:**
- A test that arrives under the user's DM chat (`chat=<positive_user_id>`) was typed in the bot DM, not the group — the #1 rule above. "Access" can be fully green while the user's test never touched the group.
- Gateway logs are timestamped in the server's local mix (some lines UTC, some +08) — when correlating log time with "when the user sent it", trust the `inbound message:` line content over wall-clock assumptions.

## Agent denies a capability it has on CLI — `platform_toolsets.<platform>` (2026-08-09)

**Symptom:** the agent in a Telegram group says *"aku tak boleh generate gambar/video"* — but the same profile on CLI can. The tools exist (API keys set, FED has the models), the lane card is fine, yet the model in Telegram reports "text-based AI only".

**Root cause:** `platform_toolsets` in config.yaml only had a `cli:` list. Telegram had NO explicit entry, so `_get_platform_tools()` (`hermes_cli/tools_config.py:1646`) fell back to the platform's `default_toolset` (`hermes-telegram`) — which excludes `image_gen` / `video_gen` / `web`. The model literally did not have those function definitions in its tool list, so it honestly reported it couldn't.

**Diagnosis:**
```bash
python3 -c "
import yaml
d = yaml.safe_load(open('/usr/local/lib/hermes-agent/profiles/aaa-hermes/config.yaml'))
pt = d.get('platform_toolsets', {})
print('keys:', list(pt.keys()))          # if 'telegram' missing → default toolset
print('telegram:', pt.get('telegram'))
"
```

**Fix — set the Telegram toolset explicitly:**
```bash
hermes config set platform_toolsets.telegram '["web","image_gen","video_gen","vision","skills","memory","terminal","file","tts","session_search","todo","cronjob","delegation","clarify","code_execution"]'
```

Then restart the gateway. This is separate from the lane CAPABILITY MAP injection (person-lane-operator skill): the map stops the agent *claiming* incapacity; `platform_toolsets.telegram` actually *gives* it the tools. Both are needed — one is context, the other is capability.

**General rule:** when the agent denies a capability on ONE platform but has it on another, check `platform_toolsets.<platform>` resolution before touching lanes, skills, or keys. Tool injection is the last-mile gate.

### Lane `skills: []` = capability blindness (2026-08-09) + the unification ruling

The lane_switch plugin injects each lane's `skills:` list (from `lanes.yaml`) into the LLM context. A lane with `skills: []` (e.g. `izzu-aia` before the fix) means the agent in that group does not KNOW it can generate images/video/PDFs — it answers "tak boleh" from ignorance, even when the tools are present. **Fix: unify** — every warga lane carries the SAME core skill set; lanes differ only in memory/voice/authority, never capability. Guest lane stays `skills: []` (zero-trust).

Sovereign preference (Arif, 2026-08-09): when skills/services misbehave, **fix, never delete** ("jangan buang skills sesuka hati"), and **unify, never fragment** ("penat wei" — no per-user/per-group skill lists). One agent, one skill set, all humans. A broken skill gets patched to reflect reality (e.g. ComfyUI documented as NOT OPERATIONAL on this box) rather than removed.

### Agent claims ≠ agent actions — verify before reporting (2026-08-09)

An agent can claim "dah hantar email" without ever calling the send tool (tool call failed or was skipped). Log signature: the agent's text claims success but `gateway.log`/tool logs show zero send activity. This is F9 fabrication of real-world actions — worse than sending without judgment. **Gate:** before reporting any real-world action as done, require a verifiable handle — Brevo `messageId` (via `python3 /root/scripts/brevo-verify.py --check <id>`), `gateway.log "Sending response"` line, or file existence. The `verify-before-report` skill enforces this discipline; load it whenever delivery is claimed.

## Identifying a bare t.me invite link (no context, don't click) — 2026-08-15

User drops `https://t.me/+<hash>` with no explanation. Before assuming anything, scrape the public preview — Telegram serves group metadata to unauthenticated curl:

```bash
curl -s -m 10 "https://t.me/+hEkd23U7zrBhOGJl" \
  | grep -oE '<meta property="og:title" content="[^"]*"'
# → content="Sin Boy"   (group NAME, revealed WITHOUT joining)
```

`og:title` = group title; works for any `t.me/+hash` / `t.me/joinchat/` link. This answers "what did the user just hand me" without clicking, joining, or burning the one-time flow.

**Then, to check whether anyone actually USED the link** (new member joined a group the bot is already in):

1. `getUpdates` is useless here — webhook active → `409 Conflict` (known pitfall above). Don't burn a call on it.
2. `gateway.log` grep for the group chat_id is the only traffic proof — same rule as the access-verification ladder:
   ```bash
   grep -a '<group_chat_id>' /usr/local/lib/hermes-agent/profiles/aaa-hermes/logs/gateway.log | tail -5
   ```
   Joins surface as `new_chat_members` service messages; if the gateway processed one, it's in the log.

**Token indirection trap (verified 2026-08-15):** `TELEGRAM_BOT_TOKEN` in `kunci-mas.env` is a template string (`"${ASI_BOT_...}"`), NOT a literal token. Grep-finding it and using it → `404 Not Found` from the Bot API. The live token is `ASI_BOT_TOKEN` in the same file:

```bash
source /root/.secrets/kunci-mas.env
curl -s "https://api.telegram.org/bot${ASI_BOT_TOKEN}/getMe"   # → @ASI_arifos_bot, id 8410138119
```

Always `getMe` to confirm which bot a token names before drawing conclusions from API responses — a `404` on `getUpdates` can mean "wrong/templated token", not "no updates". Reading the token from `/proc/<gateway_pid>/environ` (already resolved by the wrapper) avoids the indirection entirely.

## Wiring a NEW group — invite links are for humans, not bots (2026-08-15)

User drops `https://t.me/+<hash>` and asks "test whether the bot replies there" (see the invite-link identification section below for scraping its title first). **The invite link is a dead end for bots**: Telegram invite links join human accounts only — the Bot API has no join-by-link method, and a headless browser click won't work either. Don't burn turns on it. The only path in is a human adding the bot.

**The wiring sequence for a brand-new group (not in any allowlist):**

1. **Human adds the bot** — group → Add members → search the bot username (`@ASI_arifos_bot` for the Hermes seat, `@arifOS_bot` for FORGE). A bot CANNOT be invited via link, and the chat_id CANNOT be derived from the invite-link hash.
2. **Discover the chat_id** — after the first message in the group, grep gateway.log for the new negative `-100…` id. No other source is truth.
3. **Allowlist the chat in BOTH gates** — `TELEGRAM_ALLOWED_CHATS` (response) AND `TELEGRAM_GROUP_ALLOWED_CHATS` (observation) in kunci-mas.env + systemd drop-in → restart gateway.
4. **Privacy mode check** — bot reacts only to /commands and @mentions but ignores normal chat → `@BotFather → /setprivacy → Disable → remove & re-add the bot`.
5. **Ask for a FRESH test AFTER config lands** — the at-most-once rule: any test sent during the config window was consumed and will never redeliver. Never promise redelivery of the old message.

**Outbound probe beats waiting:** the moment the bot is a member, `getChat` + `sendMessage` with the bot token returns `ok:true` + `message_id` (recipe in "Outbound send works; inbound read does NOT" below). Use it to confirm the add succeeded before asking the user to @mention.

## Forum supergroups

Groups with topics enabled (`is_forum=true`) carry `message_thread_id` on every message. The `_allowed_topics` filter (line 8361) checks this:

```python
if allowed_topics:  # non-empty
    topic_id = str(thread_id) if thread_id is not None else self._GENERAL_TOPIC_THREAD_ID
    if topic_id not in allowed_topics:
        return False
```

If `TELEGRAM_ALLOWED_TOPICS` is empty/unset, all topics pass. If set, only listed topics pass.

## The env-var authorization override (2026-08-09)

When `TELEGRAM_ALLOWED_USERS` or `TELEGRAM_GROUP_ALLOWED_USERS` exist in the process environment (typically via `kunci-mas.env` → systemd drop-in → gateway PID), they act as **sole authority** for user-level auth in `_is_user_authorized_from_message`. The adapter's code path:

```python
# adapter.py:_is_user_authorized_from_message
adapter_allow_from = self.config.extra.get("allow_from")
if adapter_allow_from is not None:
    # config.yaml allow_from IS checked first — but...
    allowed = {str(u).strip() for u in adapter_allow_from}
    return user_id in allowed or "*" in allowed
# ...then falls to runner auth → env vars
runner = getattr(getattr(self, "_message_handler", None), "__self__", None)
auth_fn = getattr(runner, "_is_user_authorized", None)
if callable(auth_fn):
    return bool(auth_fn(source))  # ← uses TELEGRAM_ALLOWED_USERS
```

**The trap:** If the runner path is taken (common in production), `TELEGRAM_ALLOWED_USERS` becomes the effective gate — even when `config.yaml` has `allow_from` with the correct IDs. A new person in `config.yaml allow_from` but MISSING from the env var → **zero log entries, zero adapter flush, zero error**. Silent drop.

**Verify with:**
```bash
strings /proc/<gateway_pid>/environ | grep -E 'TELEGRAM_ALLOWED_USERS|TELEGRAM_GROUP_ALLOWED_USERS'
```

**Fix:** Add the new person's ID to BOTH:
1. `kunci-mas.env` → `TELEGRAM_ALLOWED_USERS=...` and `TELEGRAM_GROUP_ALLOWED_USERS=...`
2. `config.yaml` → `telegram.allow_from` and `telegram.group_allow_from`
Then restart the gateway.

## Telegram Privacy Mode — the invisible server-side gate

Even with all env vars and config.yaml correct, if the bot has **privacy mode ON** (the Telegram default for new bots), messages from non-admin, non-mention group members **never reach the bot at all**. Zero log entries — no "Flushing text batch", no "Blocked unauthorized user", no "inbound message". Telegram drops them server-side.

**How to confirm:** Grep the gateway log for the user's ID:
```bash
grep -c '<user_id>' /usr/local/lib/hermes-agent/profiles/<profile>/logs/gateway.log
```
If zero across ALL log files (gateway.log, agent.log, errors.log), the messages never reach the adapter. This rules out all Hermes-side filters.

**The privacy-mode rule:** Bots with privacy mode ON only receive:
- Commands (`/start`, `/help`)
- Messages that @mention the bot
- Replies to the bot's own messages
- Messages from group **administrators**
- Service messages (joins, leaves, pins)

**Fix:** @BotFather → `/setprivacy` → select bot → **Disable** → then **remove and re-add the bot** to the group (Telegram caches the setting per-group; a fresh join forces the new setting to apply).

**Common misdiagnosis:** People fix env vars, config.yaml, and free_response_chats — and it's all correct — but the bot still ignores a specific user. The env var gate AND the adapter gate both pass, but Telegram never delivers the message in the first place. **Always check for zero log entries as the first diagnostic step before diving into adapter code.**

## Lane-switch plugin reads `lanes.yaml`, NOT `lane-*.json`

The lane_switch plugin (`/usr/local/lib/hermes-agent/profiles/aaa-hermes/plugins/lane_switch/__init__.py`) reads its canonical registry from:

```python
LANES_YAML = Path("/root/HERMES/lanes/lanes.yaml")  # ← THIS is the source of truth
```

The `lane-*.json` files in `/root/HERMES/profiles/aaa-hermes/memories/` (e.g. `lane-izzu.json`, `lane-aliff.json`) are **legacy files** from an earlier design. They can have wrong group IDs, stale triggers, or missing lanes — and they are **NOT read by the plugin**. If you find a wrong chat_id in `lane-izzu.json`, that is NOT the cause of the bug. Check `lanes.yaml` instead.

## Pitfalls

- `free_response_chats` under `telegram:` block in config.yaml may not propagate to `config.extra` — root-level or env var is safer.
- A forum topic's `message_thread_id` (e.g. `5999`) is NOT the same as `chat.id`. Don't confuse them when debugging.
- `_is_own_message` runs inside `_should_process_message` (line 8341), NOT before auth. Self-echoes flood the auth gate.
- `pending_update_count: 0` from `getWebhookInfo` does NOT prove recent activity — only that Telegram successfully delivered everything in queue. Check `gateway.log` directly.
- Synthetic webhook probes get HTTP 200 even when the message is silently dropped — always grep the log after the probe, not just check status code.
- Bot sends **anonymously** (`is_anonymous: true`) but `from.id` is still the bot_id in webhook updates — Telegram does not redact sender identity server-side.

## Observed group context NOT injected (agent has no memory of chat history) — 2026-08-12

The hardest class of "agent forgets what was said in this group" symptom. The Telegram adapter has a full observe-then-inject pipeline that **looks wired but silently no-ops** when one gate isn't set.

### Symptom

In a Telegram group (SADO, AIA, etc.), user says something, then later says `"apa hang ingat Syed cakap tadi?"` or `" jawab betul soalan aku tadi"`. Agent: "I don't have visibility into previous messages in this chat." Even though:
- `TELEGRAM_OBSERVE_UNMENTIONED_GROUP_MESSAGES=true` is set
- The agent RESPONDS to @mentions and replies (adapter is not silent)
- The bot is admin of the group (privacy mode off)
- `state.db` has session rows for that chat

### Root cause — three gates, one missing silently

The pipeline (4 files, 8 hops) has THREE gates that must all return truthy for observed context to reach the agent prompt:

```
adapter.py:7512 _observe_unmentioned_group_message
        ↓ appends {observed: True} to state.db
adapter.py:7319 _apply_telegram_group_observe_attribution
        ↓ sets event.channel_prompt with marker
adapter.py:7340 _telegram_observe_allowed_chats()  ← GATE #1 (most common miss)
        ↓ must return non-empty set AND chat_id be in it
gateway/run.py:884  separate_observed_context = _uses_telegram_observed_group_context(channel_prompt)
        ↓ checks for marker string "observed Telegram group context"
gateway/run.py:911  observed_group_context.append(content)
        ↓ separates observed=True rows out of agent_history
gateway/run.py:20553 _wrap_current_message_with_observed_context(_run_message, observed_group_context)
        ↓ prepends [Observed Telegram group context…] block to current turn
```

**GATE #1** is the failure. `_telegram_observe_allowed_chats()` calls `_telegram_group_allowed_chats()` which reads `TELEGRAM_GROUP_ALLOWED_CHATS` env OR `config.extra["group_allowed_chats"]`. If neither is set, it returns `set()` and `_apply_telegram_group_observe_attribution()` short-circuits at line 7322:

```python
allowed = self._telegram_observe_allowed_chats()
if not allowed or chat_id_str not in allowed:
    return event  # ← no channel_prompt marker set → pipeline halts
```

The session transcript still gets the observed message (`observed: True` rows in state.db), but the gateway never separates it from regular history because the channel_prompt marker is missing.

### Verification recipe

Prove the chain works before assuming the config fix landed:

```bash
# 1. Check current env / config — is group_allowed_chats populated?
strings /proc/$(systemctl show -p MainPID hermes-asi-gateway.service | cut -d= -f2)/environ \
  | grep -E "GROUP_ALLOWED_CHATS|group_allowed|observe_unmentioned"
# Expected post-fix: GROUP_ALLOWED_CHATS=-1003815535761 (or comma-separated list)

# 2. Check session transcript for observed=True rows
sqlite3 /usr/local/lib/hermes-agent/profiles/aaa-hermes/state.db \
  "SELECT session_id, role, substr(content,1,80), observed FROM messages
   WHERE observed=1 ORDER BY id DESC LIMIT 10;"
# Expected: rows with observed=1 AND content starts with [sender|user_id]

# 3. Verify the marker gets set — issue a probe and grep log
grep -E "observed Telegram group context|telegram_group_observe" \
  /usr/local/lib/hermes-agent/profiles/aaa-hermes/logs/gateway.log | tail -5
# Expected: lines mentioning the marker when a @mention arrives in a group

# 4. Verify injected context reaches the API call (most authoritative)
# Add a temporary print or inspect last gateway.log line for any MessageEvent that
# contains the [Observed Telegram group context ...] prefix
tail -200 /usr/local/lib/hermes-agent/profiles/aaa-hermes/logs/gateway.log \
  | grep -B1 -A1 "Observed Telegram group context" | tail -10
```

### Fix (config-only, T1 reversible)

Add `group_allowed_chats` to the `telegram:` section of `config.yaml`:

```yaml
telegram:
  group_allowed_chats:
    - '-1003815535761'   # SADO
    - '-1003521544074'   # AIA
  # … existing keys …
```

Or set env var in the systemd drop-in:

```ini
TELEGRAM_GROUP_ALLOWED_CHATS=-1003815535761,-1003521544074
```

Then restart the gateway. No source code change needed — the pipeline is already complete; it was just gated off.

### Why this got missed in earlier debugging

`_telegram_observe_allowed_chats()` silently returns `set()` when its config source is empty — **no log line, no error**. The chat still goes through `require_mention` / `free_response_chats` / `allowed_chats` filtering correctly (those work). The bot replies to @mentions. The user assumes "group works" and doesn't realize the OBSERVE side is dead. The first symptom they get is "agent doesn't remember my previous messages" — which they may diagnose as a memory problem (it isn't).

### Pitfalls (additions from 2026-08-12 find)

- `group_allowed_chats` is a SEPARATE config key from `allowed_chats` — they serve different purposes. `allowed_chats` is the **response gate**; `group_allowed_chats` is the **observation gate**. Don't conflate.
- The path `adapter.py:_telegram_observe_allowed_chats()` reads ONLY this key — it does NOT check `allow_from` or any auth list. Two distinct gates, two distinct config keys.
- The default (no `group_allowed_chats` set) is OBSERVATION OFF, not observation-on. Backward compatibility intent: existing deployments before the feature had observe off, so the default preserves that. New feature: must opt-in explicitly.
- `require_mention=false` does NOT enable observation. They're orthogonal gates (response vs. observation).
- Observed messages stored in state.db with `observed=True` flag do NOT automatically replay into agent history. The injection is per-turn and read-time only — observed messages from past sessions are stale and not loaded.
- `_apply_telegram_group_observe_attribution()` returns the event unchanged if the chat is not in the observation allowlist, even if `observe_unmentioned_group_messages=true` is set globally. Both must agree.

## Companion references

`references/izzu-aia-silence-debug-2026-08-09.md` — full transcript of the Izzu-in-AIA debug session: env-var override + Telegram privacy mode as dual root causes, lane-*.json red herring, zero-log-entry diagnostic path.
`references/group-message-debugging-2026-08-05.md` — full transcript of the SADO debug session, with the chat_id evidence, the gating chain walked through, and the nuclear-option env config.
``references/`` (inline below) — full transcript of the cron bot-self-DM delivery: state.db session showing `chat_id=8410138119`, `_resolve_single_delivery_target` resolver path, the fix (override `deliver=telegram:267378578`), the prior-learnings sibling sessions that pointed at the wrong layer.

### Inline transcript — bot-self-DM delivery (2026-08-06 04:00–04:24 UTC)

Gateway.log showed alternating WARN and ERROR lines around 04:04 UTC:

```
ERROR [Telegram] Failed to send Telegram message: Forbidden: the bot can't send messages to the bot
WARNING [Telegram] Send failed (attempt 1/2, retrying in 4.1s): Forbidden: the bot can't send messages to the bot
ERROR [Telegram] Failed to deliver response after 2 retries: Forbidden: the bot can't send messages to the bot
```

Concurrently inbound prefilter logs: `Blocked unauthorized user 8410138119 in chat 8410138119`. Arif's interpretation (correct): *"bot cuba DM diri sendiri (Chat ID: 8410138119) dan bukannya hantar ke target sebenar (User ID: 267378578). F2 Truth sentiasa menang bila kita gali log."*

`state.db sessions` rows poisoned (verified):
```
20260806_023139_d1507661 | chat_id=8410138119
20260806_032042_0f3a12d7 | chat_id=8410138119
20260806_041033_5081f748 | chat_id=8410138119
```

Sub-agents spawned within these rows inherit `origin.chat_id=8410138119`. `cron/scheduler.py::_resolve_single_delivery_target` line 1108 returns that ID blindly when `deliver="origin"`. Result: `OutboundTarget(telegram, 8410138119)` → `sendMessage(8410138119, …)` → Telegram rejects → 2 retries → final ERROR.

**Siblings that pointed at the wrong layer (all probed, all refuted):**
- Token rotation → getMe confirmed token good, identity `ASI_arifos_bot`
- jobs.json patch → live jobs.json L2 already had `deliver: telegram:267378578`; backups had old 8410138119 entries but they're dead
- Auth/allowlist edit → inbound prefilter already blocks correctly; the bug is outbound
- Health check → gateway healthy
- Resolver trust in `origin.chat_id` is the actual fix point.

**The fix is two-fold:** (1) explicit `deliver: "telegram:267378578"` on cron jobs (already in place for 5 canonical blueprints verified 2026-08-06 04:00 UTC); (2) the sub-agent delivery loop inside sessions must use the same explicit override when `origin` could be poisoned — verify session doesn't carry `chat_id == bot_id` before resolving to `origin`.

**Audit recipe for next occurrence:**
```bash
BOT_ID=$(curl -s "https://api.telegram.org/bot${ASI_BOT_TOKEN}/getMe" | jq -r '.result.id')
sqlite3 /usr/local/lib/hermes-agent/profiles/aaa-hermes/state.db \
  "SELECT id, chat_id FROM sessions WHERE chat_id='$BOT_ID' ORDER BY last_active_at DESC LIMIT 5;"
grep -E "to $BOT_ID" /usr/local/lib/hermes-agent/profiles/aaa-hermes/logs/gateway.log | tail -5
```
Expected post-fix: empty.

## channel_directory.json as the zero-processing witness

Read `/usr/local/lib/hermes-agent/profiles/<profile>/channel_directory.json` (live, no restart needed). If `platforms.telegram` lists only `"type": "dm"` entries and **zero groups**, the bot has **NEVER processed a single group message** in this session. This is the strongest signal that delivery is broken upstream (webhook / Caddy / Cloudflare / Telegram routing), NOT a Hermes filter. Allowlist/mention/free_response edits will NOT fix it — the update never reaches the handler.

Per the hermes-telegram-gateway-ops identity-truth hierarchy: `pending_update_count: 0` from `getWebhookInfo` means "Telegram successfully delivered queued updates", not "updates are flowing now". Combine both:
- `pending_update_count: 0` (Telegram side empty) AND `channel_directory.json` has zero groups (Hermes side has zero group history) → real group delivery gap.
- `pending_update_count: 0` but `channel_directory.json` has groups → historical good, current incident is filter/allowlist.

## "I give up — dispatch Kimi" pattern

When adapter inspection, env tweaks, and synthetic probes converge but the root cause won't yield, **delegate to a peer agent in the federation** (Kimi / OpenCode / Claude Code via `delegate_task` from the dispatcher, or `aaa-dispatch.sh kimi "<prompt>"` from the terminal). Use a focused brief:

1. State the symptom in one line ("SADO group messages silently dropped, HTTP 200, zero log")
2. List the verified facts (env vars in process, bot admin status, synthetic probe results)
3. Point at the exact file + line range to inspect (`adapter.py:8476 _handle_text_message`)
4. Require a **verifiable outcome**: a log line proving inbound fired, OR exact root cause + minimal patch
5. Forbid risky actions: "NEVER call `systemctl restart` from your own session — use `setsid sh -c "sleep 5; systemctl restart ..."` so parent survives"
6. Demand an evidence-based reply shape: FIXED / BLOCKED / ROOT CAUSE, with PID, log line, env var, file path

Self-dispatch pattern saved ~30 min of manual bisection in this session — the subagent reads its own proc env, runs probes, and isolates variables you can't reach from a stuck gateway session.

## OpenClaw trajectory forensics (when the bot IS NOT Hermes)

OpenClaw runs a separate gateway (`openclaw-gateway.service` on `:18789`) with its own agent kernel, journal, and session store. The symptom is the same — "DMs work, groups don't" — but the adapter/gating chain is completely different. The journal signature differs:

```
[turn/kernel] visible channel turn dispatched with no queued reply payloads
```

This line means: the kernel completed a turn, the LLM was called (model fetch 200 OK), but the agent produced **zero outbound messages**. Three causes, all producing the same log line:

| Cause | Log / trajectory evidence | Fix |
|---|---|---|
| **Agent-judgment silence** | `trace.artifacts.assistantTexts: ["No reply needed — ..."]` + `finalStatus: success` | Tighten the agent prompt. T3 doctrine change. |
| **Provider rejection** | `isError=true` + `[model-fallback/decision]` in journal (e.g. `400 'tools' : maximum number of items is 128`) | Trim tool atlas or switch model. |
| **Hooked silent-drop** | `[agents/tool-policy] tool policy removed N tool(s)` in journal around the turn | Inspect `tools.deny` in `openclaw.json` for that sender. |

**Wrong-cause trap:** I once blamed MEMORY.md's `[TO:]` HARAM rule for group silence after grepping the agent's ruleset. The trajectory actually showed `"No reply needed — routine market wrap, no action requested."` — the model was the gate, not the rule. **Always read the trajectory before naming the cause.**

### Trajectory forensics path

Sessions live at:
```
/root/.openclaw/agents/main/sessions/<uuid>[-topic-<topicId>].trajectory.jsonl
```

Group sessions carry the Telegram topic ID in the filename suffix. DM sessions carry the user ID.

**Step 1 — Find the session:**
```bash
# Get topic ID from journal
journalctl -u openclaw-gateway --no-pager -n 200 | grep "topic:" | grep "no queued reply" | tail -1
# Find session file by topic
ls -lat /root/.openclaw/agents/main/sessions/*topic-41564* | head -2
```

**Step 2 — Extract the model's actual text** (or use `scripts/openclaw_silence_probe.sh <topic_id>`):
```bash
tail -3 /root/.openclaw/agents/main/sessions/<sid>.trajectory.jsonl \
  | python3 -c "
import sys, json
for line in sys.stdin:
    d = json.loads(line.strip())
    if d.get('type') == 'trace.artifacts':
        a = d.get('data',{})
        print('finalStatus:', a.get('finalStatus'))
        print('assistantTexts:', a.get('assistantTexts'))
        print('messagingToolSentTexts:', a.get('messagingToolSentTexts'))
        print('didSendViaMessagingTool:', a.get('didSendViaMessagingTool'))
        print('usage:', a.get('usage'))
"
```

**Step 3 — Cross-check journal around the same timestamp:**
```bash
journalctl -u openclaw-gateway --no-pager --since "5 min ago" \
  | grep -iE "inbound|outbound|error|fail|reject|fallback|policy"
```

The truth lives where `assistantTexts[]` + `messagingToolSentTexts[]` agree — not where MEMORY.md rules appear to fit the symptom.

### OpenClaw group config truth

OpenClaw's group behavior is governed by `openclaw.json` → `channels.telegram.groups`:
```json
{
  "groupPolicy": "allowlist",
  "groups": {
    "-1003753855708": {"groupPolicy": "open", "requireMention": false}
  }
}
```

Unlike Hermes (which uses `free_response_chats` + env vars in systemd drop-ins), OpenClaw uses its own JSON config. `groupPolicy: open` + `requireMention: false` means "the channel layer passes everything" — but the agent kernel can still produce zero payloads if it judges the message unworthy.

### MEMORY.md overflow warning

OpenClaw truncates `MEMORY.md` when it exceeds `bootstrapMaxChars` (default 31743):
```
[agent/embedded] workspace bootstrap file MEMORY.md is 35204 chars (limit 31743); truncating
```
This means the agent's memory context is incomplete, which may affect its judgment about whether to reply. If `assistantTexts` shows silence on substantive messages, check for this truncation warning in the journal around the turn timestamp.

## Synthetic probe script (Hermes)

Use `scripts/sado_probe.sh` (template in this skill) to issue a hermetic probe to a running webhook without disturbing live state. Returns the HTTP code + the new gateway.log lines that appeared in the 5-second window — proves whether the handler fired. Default probe targets SADO (`-1003815535761`) and Arif (`267378578`); override via positional args.

```bash
bash scripts/sado_probe.sh                              # default SADO probe
bash scripts/sado_probe.sh -1003753855708 267378578 "hi" # different group
```

## OpenClaw silence probe script

Use `scripts/openclaw_silence_probe.sh <topic_id>` to pull ground-truth from the OpenClaw trajectory when the journal shows `no queued reply payloads` but the cause is unclear. Extracts the four key fields (`assistantTexts`, `messagingToolSentTexts`, `didSendViaMessagingTool`, `finalStatus`) and prints a verdict.

```bash
bash scripts/openclaw_silence_probe.sh 41564   # group topic ID
```

## The bot-self-DM delivery trap (outbound `Forbidden: the bot can't send messages to the bot`) — 2026-08-06

Distinct from the **inbound** `Blocked unauthorized user <bot_id>` flood above. This pattern is **outbound** — a cron sub-agent or sub-session tries to deliver *to* the bot's own chat_id, Telegram rejects with `Forbidden: the bot can't send messages to the bot`, gateway retried twice, then marked the delivery failed.

### Root cause — `deliver="origin"` inherited a bot-self chat_id

```python
# /usr/local/lib/hermes-agent/cron/scheduler.py::_resolve_single_delivery_target
if deliver_value == "origin":
    if origin:
        return {
            "platform": origin["platform"],
            "chat_id": str(origin["chat_id"]),  # ← could be the bot's own ID
            "thread_id": origin.get("thread_id"),
        }
```

When a session is somehow registered against the bot's own chat_id (`8410138119` for @ASI_arifos_bot, see `channel_directory.json` `"ASI🪽" dm 8410138119`):
- An inbound message from `8410138119` is blocked by `_is_user_authorized_from_message` (allowlist gate)
- But the session row may already exist in `state.db` with `chat_id=8410138119`
- A cron job or sub-agent spawned inside that session with `deliver="origin"` then resolves target to the bot's own ID
- Outbound `sendMessage(8410138119, ...)` → Telegram API returns `Forbidden: the bot can't send messages to the bot`
- Gateway retries 2×, then logs `[Telegram] Failed to deliver response after 2 retries`

### Log signature (the 3-line fingerprint)

```
WARNING [Telegram] Blocked unauthorized user 8410138119 in chat 8410138119
ERROR   [Telegram] Failed to send Telegram message: Forbidden: the bot can't send messages to the bot
WARNING [Telegram] Send failed (attempt 1/2, retrying in 2.4s): Forbidden: the bot can't send messages to the bot
```

If you see these three in sequence in the same second window, it is NOT an inbound spam — it's an outbound delivery against a bot-self origin. The inbound-block line is the prior event; the outbound `Forbidden` is the breakage you need to fix.

### Differentiate inbound spam vs outbound self-DM

| Signal | Inbound spam (blocked at gate) | Outbound self-DM |
|---|---|---|
| `Blocked unauthorized user` | many per minute, recursive | one shortly after a blocked inbound |
| `sendMessage` / `Failed to send` | absent | present with `Forbidden: … to the bot` |
| `Failed to deliver response after N retries` | absent | present |
| When does it stop? | when sender stops; or after pairing | when cron job's `deliver` field is fixed |

### Fix recipe

1. **Override the cron `deliver` to the user's actual chat_id** (Arif's: `telegram:267378578`). The bot-self ID is never a valid delivery target — the user's true DM is the only safe default.
2. **For ad-hoc sub-agents spawned from a bot-self session**, pass `deliver="telegram:267378578"` explicitly when calling `cronjob` create/update, never rely on `deliver="origin"` default.
3. **Audit `channel_directory.json`** for any `"type": "dm"` entry whose `id` equals the bot's own `getMe` id. If present, that entry is the poison — find the session that registered it and resolve.
4. **Do NOT retry the same `deliver="origin"`** — the resolver is deterministic; retrying just produces the same `Forbidden`. Edit the job.

### Why this is silent (the lesson)

A blocked inbound leaves a `Blocked unauthorized user …` WARNING and exits cleanly — no delivery attempted, no error, no retry. But an outbound against a bot-self chat_id crosses the network and hits Telegram's API, which is the only place the failure surfaces. The gateway then retries twice and surfaces a `Failed to deliver response` ERROR. **The inbound-block log is not the failure; the outbound `Forbidden` is.** Treat any new `Forbidden: bot can't send messages to the bot` as a resolver/destination bug, not a config drift, not a token problem.

## Pitfalls (additions from 2026-08-05 incident)

- `getUpdates` while `getWebhookInfo.pending_update_count: 0` returns `409 Conflict: can't use getUpdates method while webhook is active` — this is **normal Telegram behavior**, not a fault. To poll updates, delete the webhook first (`deleteWebhook`).
- The bot's anonymous admin badge ("HERMES AGENT") is cosmetic — `from.id` on the webhook update is still the bot's numeric id, not the human's. Don't be fooled into thinking a "HERMES AGENT" sender means it's the bot's own message; check `from.id`.
- A synthetic POST with the **same `update_id` twice** is silently deduped by PTB on the second hit (no log entry, HTTP 200). Always use a fresh `update_id` per probe (`$(date +%s%N)` or `$RANDOM$RANDOM`).
- The bot DM chat_id equals the user's numeric id (`chat=267378578` for user 267378578). If your log shows `chat=<your_user_id>`, the message was sent to the bot's DM regardless of what window the user thought they typed in. Verify before debugging adapter code — the bug is usually client-side (wrong chat open), not server-side.
- `systemctl cat <unit>` is the **merged truth** for the unit's environment (vault + flat-env + every drop-in). `config.yaml` is fiction when drop-ins override. `/proc/<pid>/environ` is binary — use `strings /proc/<pid>/environ | grep VAR` (plain grep says "binary file matches").

## Outbound send works; inbound read does NOT (the asymmetry — 2026-08-08)

A Hermes session can `sendMessage`/`getChat`/`sendDocument` to any supergroup it's a member of — those are stateless outbound API calls. **It cannot read historical group messages from inside the session** unless that session is bound to the gateway's webhook context. The trap: agent assumes `chat_id` discovery implies message surveillance.

**The full capability matrix:**

| Operation | From ad-hoc Hermes session | From gateway-bound Hermes session (webhook owns the chat) |
|---|---|---|
| `sendMessage(chat_id, text)` | ✅ yes (need bot token + group membership) | ✅ yes |
| `getChat(chat_id)` | ✅ yes | ✅ yes |
| `sendDocument(chat_id, file)` | ✅ yes | ✅ yes |
| Read historical messages | ❌ no — no API surface | ✅ yes (gateway streams via webhook) |
| Receive new inbound messages in real-time | ❌ no — webhook goes to gateway's main session, not this one | ✅ yes (this session is the bound handler) |

**Probe recipe (verify before claiming "I sent to the group"):**

```bash
set -a && source /root/.secrets/kunci-mas.env && set +a
curl -sf "https://api.telegram.org/bot${ASI_ARIFOS_BOT_TOKEN}/getChat" \
  -d chat_id="-1003753855708" | jq -c '{ok, title: .result.title, type: .result.type}'
# ✅ ok:true + correct title + type:"supergroup" = bot can SEE the group
# ❌ ok:false + error_code:400 + "chat not found" = bot not in group OR wrong chat_id format

# Send with response evidence
curl -s -X POST "https://api.telegram.org/bot${ASI_ARIFOS_BOT_TOKEN}/sendMessage" \
  -d chat_id="-1003753855708" -d text="..." \
  | jq -c '{ok, message_id: .result.message_id, error: .description}'
# ✅ ok:true + message_id:int = delivered (API confirmation, not self-report)
```

**Common misformat**: bare `1003753855708` (no `-100` prefix) returns `400 chat not found` even when the bot IS a member. Telegram supergroup IDs always start with `-100`. DM chat_ids for sovereign (Arif = `267378578`) need no prefix.

**Implication for routing decisions**: when an agent is asked to do group-routed work (e.g. "audit the AAA group"), the agent CAN deliver the audit result to the group via `sendMessage` — but it CANNOT consume what the group has been discussing unless the gateway has captured and exposed that context. If the agent needs to *react* to group history, route the request to the **gateway-bound main session** (the one that owns the webhook), not to an ad-hoc session.

## Coding-agent → Telegram delivery chain (forge outputs, audits, PDFs)

Coding harnesses (OpenCode, Codex, Claude Code, Kimi-Code) **cannot** deliver artifacts to Telegram directly. They have no `chat_id` discovery path: bots without a webhook cannot use `getUpdates` (returns 409), and bots with a webhook cannot use `getUpdates`. The harness therefore sees 0 messages and cannot learn the user's chat_id from inbound traffic.

**The correct chain:**

```
Coding agent (forge)
   ↓ produces artifact (PDF, doc, receipt)
   ↓ A2A notifies Hermes
Hermes (Telegram edge)
   ↓ owns chat_id: 267378578 (Arif DM, @ASI_arifos_bot)
   ↓ AND chat_id: -1003753855708 (AAA supergroup, @arifOS)
   ↓ delivers via ASI_ARIFOS_BOT_TOKEN
   ↓ returns message_id as evidence
```

**Direct-API fallback when Hermes is unavailable** — Hermes (the agent running in this session) can deliver directly using `ASI_ARIFOS_BOT_TOKEN` from `/root/.secrets/kunci-mas.env`. The pattern:

```bash
set -a && source /root/.secrets/kunci-mas.env && set +a
curl -s -X POST "https://api.telegram.org/bot${ASI_ARIFOS_BOT_TOKEN}/sendMessage" \
  -d chat_id=-1003753855708 -d text="summary" | jq -c '{ok, message_id}'
```

`ok:true` + `message_id` = delivered (API response, not self-report). For files, use `sendDocument` with a `file://` path or multipart upload.

**The forge-bots-vs-Hermes-bots distinction:**
- `@arifOS_bot` (FORGE) and `@ASI_arifos_bot` (Hermes) — both members of AAA supergroup (`-1003753855708`)
- Coding harnesses produce, Hermes delivers — never ask the harness to deliver
- The harness's complaint "I can't find chat_id" is **correct by design** — that's not their surface

**Verified AAA supergroup** (2026-08-08, via `getChat` with `ASI_ARIFOS_BOT_TOKEN`):
- chat_id: `-1003753855708`
- title: `AAA`
- type: `supergroup`
- username: `arifOS`
- bot membership: `@ASI_arifos_bot` and `@arifOS_bot` both have send permissions

**The user's DM chat_id is 267378578** — found in this profile's `MEMORY.md` lane notes (SADO-group user) and in `channel_directory.json` for the bot DM entry.

<!-- dead-pointer sweep 2026-10-23: artifacts that could not be located were replaced with the references/ directory; see audit JSON for the missing basenames. -->
