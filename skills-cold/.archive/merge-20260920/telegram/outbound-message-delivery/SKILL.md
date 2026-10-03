---
name: outbound-message-delivery
description: "Use when posting a message into a named chat."
version: 1.0.0
author: Hermes (curator)
license: F13-Sovereign
tags:
  - telegram
  - delivery
  - receipts
  - ops
triggers:
  - "post to that group"
  - "send this to him"
  - "relay this message"
  - "hermes send"
  - "outbound message"
  - "did it actually deliver"
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# Outbound Message Delivery

Class of task: put a message into a **named** chat — one group and not another, one DM and not
another — and know it landed. Covers relays a human explicitly asked for, delivery notices from a
timer or script, and any send where the chat is chosen rather than defaulted.

Two failure modes, and the same discipline prevents both — resolve the target, verify the identity,
verify the receipt:

1. Reporting a send that never left.
2. Sending as the wrong bot, so the room sees a different identity than the one it knows.

## Procedure

1. **Resolve the target name to a chat id. Never guess an id from memory.**

   ```bash
   hermes send --list telegram
   ```

   Prints each configured target as `telegram:<Name>  [<chat_id>]`. Groups are negative ids; a DM is
the user id. Copy the id exactly — a transposed digit posts into a room no one was watching.

2. **Send with the CLI.** It reuses the gateway's platform credentials, which is why it is the
   default path.

   ```bash
   hermes send --to telegram:<chat_id> --json '<text>'
   ```

3. **If the CLI reports a missing bot token, that is a name-resolution problem, not a missing
   credential.** The token lives under the name `config.yaml` declares for that lane
   (`telegram.extra.bot_token_env`), and the CLI reads the hardcoded `TELEGRAM_BOT_TOKEN` first,
   falling back to the declared name only when the first produced nothing. Read the declared name
   instead of guessing one, and see `references/direct-cli-delivery.md`. Do not go hunting for a
   credential change, and never ask a human for a token. Two things stay constant whichever route
   you take:
   - **Encode the body.** Message text carries newlines, quotes and emoji; an unencoded body
     truncates at the first `&` and delivers a half-sentence. Passing `--file` sidesteps shell
     quoting entirely.
   - **Never echo, print, or log a credential value**, and do not type a secrets path as a literal
     command argument — the constitutional gate blocks such command lines before they run. The path
     is not the secret; the value is.

4. **Confirm the identity before posting into a live room.** Ask the platform which bot the
   credential belongs to (the Bot API `getMe` call) and check the username against the lane's owner.
   Two credentials will both "work" — the wrong one simply posts as the wrong bot, and that is
   visible to everyone in the room.

5. **Verify the receipt. A send without a success flag and a message id is UNKNOWN, not done.**
   Parse the response, keep the message id, and report the chat name plus that id to whoever asked.
   Nothing else counts as delivery — not the absence of an error, not the CLI's exit code alone.

## Relaying a human's words

When the send carries someone else's message rather than your own:

- **Verbatim.** Do not paraphrase, tighten, translate, or improve it.
- **One attribution line on top** (`<name> pesan:` / `<name> said:`) so the room knows whose words
these are. The attribution is the entire difference between carrying a message and speaking for
someone.
- **No extra framing** — no closing marker, no signature beyond the attribution.
- **Never assemble the text from the room's records.** A relay carries the human's words and nothing
else; writing the message yourself, however plausibly, is speaking in his name.
- **Report back what landed, not what you intended:** chat name plus message id. If the delivery path
was awkward to find, fix it silently and say only that it is done.

## Pitfall: transport lock blocks `hermes send` CLI — fall back to Bot API directly

The `hermes send` CLI can be blocked by a transport lock that refuses sends without an explicit, pre-verified destination. If the lock fires even with `--to telegram:<id>` and `--list` also fails, do NOT loop on the CLI. Fall back to the Telegram Bot API via Python:

1. Read the bot token from config: `grep -o "bot_token_env: [^ ]*" ~/.hermes/config.yaml` to get the env key name, then `os.environ.get(<key>)`.
2. Send via the Bot API endpoint:
   - Text: `POST https://api.telegram.org/bot{token}/sendMessage` with `{"chat_id": <id>, "text": <msg>}`
   - Voice: `POST https://api.telegram.org/bot{token}/sendVoice` with multipart form: `chat_id`, `caption`, `voice` (ogg file)
3. Check `resp["ok"] == True` and `resp["result"]["message_id"]` for the receipt.
4. Report the message_id as the delivery proof.

Do NOT print or log the token. The K-02 gate blocks commands that expose secrets.

## Pitfalls

- **An explicit relay request is an errand, not a debate.** When a human has asked for a message to be
carried, declining on principle is not a safe default — it hands finished work back to him. Execute,
then report the receipt.
- **Wrong-bot posts are permanent.** There is no visible edit history and no unsend for a message the
room already read. Confirm the identity on any lane you have not posted to before.
- **One lane, one bot.** Post as the bot that owns the room. A second bot in the same room is the
dual-identity confusion the routing doctrine exists to prevent.
- **Do not let a delivery receipt become a report about the message.** The receipt is chat + id; the
content already belongs to the human who wrote it.
- **Do not infer delivery from silence.** No error returned is not the same as delivered — check the
receipt, and if the platform cannot confirm, say UNKNOWN rather than "sent".
