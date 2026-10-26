---
name: telegram-chat-resolution
description: "Use when a Telegram link or id must resolve first."
version: 1.0.0
risk_tier: low
autonomy_tier: T1
triggers:
  - "a t.me/+ invite link is pasted with no instruction"
  - "a bare numeric chat id is pasted with no instruction"
  - "is this a group or a DM"
  - "baca chat id ni"
  - "chat_id ni apa"
  - "resolve this chat before reading it"
floor_scope: [F2, F4, F9, F12]
autonomy_tier: T1
---

# telegram-chat-resolution — id → type → name, before any read

Companion to `telegram-ops` (externally owned, read-only). That door covers operating, repairing and
extracting; this one covers the step that must happen first when the target itself is unidentified:
a link or a number arrives and nobody has said what it is.

Do not extract, summarise, or send until `type` is known. "A group" may be a DM, and a DM may belong
to a third party.

## Procedure

1. **Numeric id in hand → `getChat` first. One call, no guessing.**
   ```bash
   curl -s "https://api.telegram.org/bot$TOK/getChat?chat_id=<id>"
   ```
   Returns `type` (`private` / `group` / `supergroup` / `channel`) plus `first_name`+`username` or
   `title`. Cheapest disambiguation that exists — beats every file or DB probe.

2. **Read the SIGN of the number.** Positive = a user/DM (`383454779` → `type: private`). Groups and
   supergroups are negative (`-<id>`, `-100<id>`). A bare positive number can never be a group, so
   when the human calls it a group, report the mismatch — do not hunt for a group that would fit.

3. **`t.me/+<hash>` invite link → you cannot resolve it.** No Bot-API method trades a hash for an
   id, and a bot cannot join from an invite hash. The public preview page returns `og:title`
   "Join group chat on Telegram" with an **empty** `og:description` for private links, so scraping it
   yields nothing but the word "Telegram". There is no third route; do not loop on curl.

4. **Name which of three doors unlocks it, in one line, then stop:** the numeric id (negative for a
   group), or add the bot to the group (needs admin on that side), or forward / export the messages.

5. **Only then read.** Group history: `telegram-conversation-history-extraction` (gateway log, `-a`
   mandatory). A chat already in the store: `hermes-state-db-forensics` (`sessions.chat_id`, never
   `messages` — messages carry `session_id` only).

## Pitfalls

- **`chat_id` is the ROOM, `sender`/`user_id` is the PERSON.** A turn header like
  `Active room chat_id=383454779 | sender=267378578` means the principal is speaking inside a *third
  party's* DM. Never read that `chat_id` as the human's own identity, and never carry that room's
  content into another chat.
- **Do not open with a userbot hunt.** MTProto-as-the-human is a separate, authorization-gated
  branch (`telegram-ops` C2) requiring explicit consent before a session is even looked for. The
  default answer to an invite hash is "here is what unlocks it", not "let me build an account
  client".
- **A resolution failure is a finding, not a licence to improvise.** "That id is a DM, not a group"
  and "I cannot read an invite hash" are complete answers. Fabricating a chat_id, or summarising a
  chat you never opened, is the one unrecoverable move here.
- **Scope filesystem sweeps.** A recursive `grep -r` over `/root` plus `/opt` exceeds the tool
  timeout and returns nothing; the answer sits in two files (`channel_directory.json`,
  `state.db`). Probe the specific store, not the filesystem.

## Related

- `telegram-ops` — umbrella (external/read-only): branch A operate, B incident, C observe.
- `hermes-state-db-forensics` — schema, SQL, unknown-chat ladder.
- `arif-digest-group-chat` — the read-and-summarise pipeline once the chat is confirmed.
