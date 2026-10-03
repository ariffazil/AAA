# Whole-room onboarding — SEMBANG (2026-09-15)

## Request

"Activate this telegram group id -1003740520259 (SEMBANG) and make sure all users have access to HERMES without @mention needed. The human in that group is the named human member, identity verified via getChatMember before grant (tokenized per privacy discipline; see verification step below)."

## What was true before

The chat_id was absent from every surface. Bot was already **administrator** in the group (`getChatMember` status), so Gate 1 was already satisfied — the failure mode was purely allowlist.

## The change set

| Surface | Keys touched |
|---|---|
| `/root/.hermes/config.yaml` | `telegram.allowed_chats` (+chat), `telegram.free_response_chats` (+chat, YAML list), `telegram.allow_from` + `telegram.group_allow_from` (+user), `telegram.extra.channel_prompts['<chat>']` (new) |
| `/root/.hermes/.env` | `TELEGRAM_ALLOWED_CHATS`, `TELEGRAM_GROUP_ALLOWED_CHATS` (+chat); `TELEGRAM_ALLOWED_USERS`, `TELEGRAM_GROUP_ALLOWED_USERS` (+user) |
| `/root/.secrets/kunci-mas.flat.env` | same four keys (systemd EnvironmentFile) |

`systemctl restart hermes-asi-gateway.service` → `Connected to Telegram (polling mode)`.

## Why one chat_id covers "all users"

`gateway/authz_mixin.py`:

- `_chat_scoped_grant` (line ~474): `if is_group and source.chat_id: ... _allows(_coerce_allow_set(_auth_env('TELEGRAM_GROUP_ALLOWED_CHATS')), source.chat_id) → True` — runs before the `user_id` guard, so it also admits anonymous admins and sender_chat posts.
- `_principal_authorized` (line ~607): `if is_group_or_forum and source.chat_id: if group_chat_allowlist and _allows(..., source.chat_id): return True`.

So the room is a grant unit. Members still get listed in the `_USERS` vars so they work in DMs.

## Removing @mention

`plugins/platforms/telegram/adapter.py::_should_process_message`:

```
allowed = self._telegram_allowed_chats()          # hard gate
if allowed and chat_id_str not in allowed: return guest_mention
if guest_mention or chat_id_str in free_response_chats or is_free_response_topic: return True
...
if not self._telegram_require_mention() or self._is_reply_to_bot(message): return True
```

`telegram.require_mention: false` is global, so every allowlisted chat is already free-response; adding the chat to `free_response_chats` makes the intent explicit and survives a future global flip to `true`.

## Room-scoped persona (privacy)

`SOUL.md` + `memories/MEMORY.md` are global and injected into every room — a PETRONAS colleague room would otherwise inherit Arif's personal-lane memory. `telegram.extra.channel_prompts` keyed by chat id (read by `resolve_channel_prompt`, `gateway/platforms/base.py`) scopes the room: register, the named humans, scope, and an explicit no-private-memory line. Per-room, auto-injected, no memory budget, cannot leak elsewhere.

## Proof run (real execution)

```
env -i HERMES_HOME=/root/.hermes HOME=/root PATH=/usr/bin:/bin ./venv/bin/python
```

- `load_hermes_dotenv(hermes_home="/root/.hermes")` → `[/root/.hermes/.env]`; then `platform_gate_env`: ALLOWED_CHATS n=32 chat=YES, GROUP_ALLOWED_CHATS n=31 chat=YES, ALLOWED_USERS n=20 user=YES, GROUP_ALLOWED_USERS n=19 user=YES.
- `TelegramAdapter` instance built via `object.__new__` with `config.extra` from config.yaml: `_telegram_allowed_chats()` n=32 contains chat, `_telegram_free_response_chats()` n=31 contains chat, `_telegram_require_mention()` False, `_should_process_message(<plain message from the member, no mention>)` → **True**.

## Pitfalls hit

- `load_hermes_dotenv` is keyword-only — a positional arg raises `takes 0 positional arguments but 1 was given`, the load silently no-ops, and the probe then reads the *shell* env and reports wrong counts (looked like "no sembang" while the file was already correct). Always `env -i` + keyword call.
- `hermes config set` writes arrays as YAML-quoted strings; edit `free_response_chats` on disk as a real `- 'id'` list.
- The named human must be verified against Telegram, not trusted from the request: `getChatMember?chat_id=<chat>&user_id=<verified-member-uid>` → `<verified-member-name>`, `status=member`. One API call beats assuming the ID is right.
- Bot-authored test messages cannot prove the inbound path: `_should_process_message` drops `_sender_is_other_bot` unless the chat is `-1003753855708` (A2A). The last-mile proof needs a real human message in the group.
