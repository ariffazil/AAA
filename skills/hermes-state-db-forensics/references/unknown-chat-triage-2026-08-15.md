# Unknown-Chat Triage — "Koho Pharma" incident (2026-08-15)

Trigger: user says "agent bot tu la" / names a chat with zero known history. Task: identify what the chat is and why the bot never spoke there — WITHOUT guessing identity (never invent who a chat belongs to).

## The probe trail (as run, all live)

1. `channel_directory.json` (profile root) → **HIT**: `{"id": "8003148821", "name": "Koho Pharma", "type": "dm", "thread_id": null}`. The gateway has seen this chat. Also confirmed the roster holds sibling-bot chats (`🔥FORGE🔥`, `AGENT MERDEKA`, `🦞OPENCLAW🦞`, `ASI🪽`) alongside human DMs — directory membership does NOT mean "human".
2. state.db `sessions WHERE chat_id='8003148821'` → **0 rows**. No `gateway_routing` row either. The chat never successfully conversed.
3. `config.yaml` allowlists → `'8003148821'` in NEITHER `allowed_chats` NOR `allow_from` → any inbound was silently dropped.
4. Journal (`journalctl --since 13:40 | grep -i koho/telegram`): two outbound failures from THIS session's own replies —
   - `13:58:12 ERROR hermes_plugins.telegram_platform.adapter: [Telegram] Failed to send Telegram message: Forbidden: bot can't initiate conversation with a user`
   - `13:58:41 ERROR ... Forbidden: the bot can't send messages to the bot`
   → the reply we attempted in-session was blocked BOTH ways: target never started us AND/OR target is itself a bot.

## Interpretation matrix

| Evidence | Reading |
|---|---|
| In directory, 0 sessions, not allowlisted, Forbidden ×2 | Chat contacted the bot but no conversation ever established. Two candidate identities: (a) human business account that never pressed /start or was dropped by allowlist; (b) an agent/bot account — bot↔bot DM impossible by Telegram law. |
| Two Forbidden variants within a minute | The API itself is telling us the target is ambiguous/bot-like: `can't initiate` = no /start from them; `can't send to the bot` = target IS a bot. Either way **config cannot fix outbound** — allowlist only gates inbound. |

## The class lesson (ladder)

`channel_directory.json` (ever seen?) → `state.db sessions` (ever conversed?) → `config.yaml` allowlists (inbound gate) → journal `Forbidden:` (outbound block). Name WHICH rung failed in the answer. If the rung is a Forbidden, the honest answer includes: Telegram Bot API forbids bot↔bot DMs entirely; correct bot-to-bot transport is the A2A lane (`hermes-a2a-listener.service` :18089) or a human relay — then ask the sovereign ONE disambiguating question (human account vs bot) rather than guessing.

## Guard rails observed

- Never guess identity of an unknown chat from its name ("Koho Pharma" could be human or bot).
- Never claim allowlisting will fix delivery — it only fixes inbound; Forbidden is platform law.
- Zero rows in state.db ≠ "user never messaged" — it can equally mean "messaged, inbound dropped, no session persisted". The directory hit is what proves contact happened.
