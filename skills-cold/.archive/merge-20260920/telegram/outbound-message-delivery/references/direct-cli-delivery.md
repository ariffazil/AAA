# Direct CLI delivery — verified mechanics

Sending a specific body of text into a chat **without** routing it through a live agent
turn. Use when the goal is that one body of text and nothing else reaches the room: a
correction to something already said, an announcement, a sentence the human wrote and
handed over, a script or cron result.

A reply routed through the live session arrives wrapped in whatever the session is
carrying — thread context, persona framing, the residue of the last few turns. Direct CLI
delivery is clean by construction.

## Procedure

1. **Resolve the target.** `hermes send --list telegram` lists configured destinations.
   Groups get `telegram:-<id>`; the negative sign is part of the id. Read the chat id out of
   the gateway log (`chat=<id>`) rather than from memory — a person's traffic can appear
   under more than one id, and a DM id is not the group id.
2. **Write the body to a file and pass the file**, never a long inline argument: quoting
   survives intact, and the bytes reviewed are the bytes that land. Re-read the file before
   sending.
3. **Resolve the credential by the name config declares, then send.**
   ```bash
   grep -A20 '^telegram:' /root/.hermes/config.yaml | grep bot_token_env   # the declared name
   hermes send --to telegram:-<group_id> --file /tmp/msg.txt --json
   ```
   See *The credential* below — the name is data read from config, and guessing it is how this
   file was wrong before.
4. **Verify by `message_id`.** The `--json` body returns
   `{"success": true, "platform": "telegram", "chat_id": "…", "message_id": "…", "mirrored": true}`.
   The `message_id` comes back from the platform, not from your intent. A success line
   without one is a claim about delivery, not delivery.
5. **Report the transition, not a Boolean.** "Sent" is not a state. Name it *produced →
   delivered* with the `message_id`, or *blocked at gate* with the exact operation refused.

## The credential — the name is data, not knowledge

The resolution order inside `hermes send` is:

1. the platform's **hardcoded** name, `TELEGRAM_BOT_TOKEN` (`gateway.config.
   PLATFORM_TOKEN_ENV_NAMES` / `gateway.config_env._ENV_STEPS`, both are that one string);
2. **only if that produced nothing**, the name the platform block itself declares at
   `config.yaml` → `telegram.extra.bot_token_env`.

Measured 2026-09-17: `config.yaml:100` carries `bot_token_env: ASI_ARIFOS_BOT_TOKEN`. The field
exists because `PlatformConfig.from_dict` promotes that non-typed key into `extra`, and — until
the same day — **no code read it back**. The source note in `tools/send_message_tool.py`
(lines 283–313) records the root cause in its own words: a deployment injecting the token *only*
under the declared name (systemd `EnvironmentFile=`) reached the sender with an empty token, and
python-telegram-bot raised *"You must pass the token you received from https://t.me/Botfather!"*.
The gateway stayed up only because a systemd drop-in happens to hardcode `TELEGRAM_BOT_TOKEN` —
so the lane broke for every **standalone caller** (CLI, cron, script) while the bot kept
answering in chat. The fix honours the declaration, and only after the hardcoded name, so nothing
that already worked changed.

Three consequences, and the third is the one that bites:

- **Read the declared name; never hardcode an alias in a skill.** An earlier version of this file
  prescribed `HERMES_TELEGRAM_BOT_TOKEN`. The code never reads that name. It happened to work —
  because the variable exists in the shell *and* holds the same bot's credential — so the
  prescription tested green while teaching a false mechanism. **A test that passes for the wrong
  reason is how a superstition gets sealed as procedure.**
- **That error message does not mean the credential is missing.** It means the token was *empty at
  the sender* — a name-resolution problem. The credential can be present and visible under the
  declared name while the path that failed saw nothing. Do not go hunting for a credential
  change, and never ask the principal for a token.
- **Do not try to clear it by exporting a guessed name.** Exporting `TELEGRAM_BOT_TOKEN` does
  satisfy path 1, so it appears to be the fix. It also means the next lane you touch resolves to
  whatever that alias points at — and if the alias holds a *different* bot, you have posted as the
  wrong bot in a live room. `bot_token_env` is the supported surface; use it.

## More than one bot token lives in this environment

Six credential names resolve in this environment, and they are **three different bots**. Measured
2026-09-17 by reading each name's public bot-id prefix (the digits before the `:` — `getMe` returns
them, and they are safe to compare; never print the token itself):

| name | bot id | which bot |
|---|---|---|
| `ASI_ARIFOS_BOT_TOKEN` — **the declared one** | 8410138119 | `@ASI_arifos_bot` |
| `ASI_BOT_TOKEN` | 8410138119 | same bot |
| `HERMES_TELEGRAM_BOT_TOKEN` | 8410138119 | same bot |
| `AGI_ASI_BOT_TOKEN` | 8149595687 | a different bot (OpenClaw family) |
| `FORGE_BOT_TOKEN` | 8727562763 | a different bot (`@hermesarifos_bot`, Gateway 4) |
| `TELEGRAM_BOT_TOKEN` — the **hardcoded** name | *(unset)* | — |

That last row is the whole story. The name the code looks for **first** is unset here, so the
resolution falls through to the declared `bot_token_env` and the send path depends on the
declaration. A skill that says "never rely on `bot_token_env`" is not being cautious — it is
describing the pre-2026-09-17 code, and the declaration is now the only thing that works.

Before posting into a lane you have not posted to before, compare the resolving name's bot id
against the lane's declared owner. **Same-bot aliases are interchangeable; a different bot's token
is a wrong-identity post**, and the room sees it.

The **existing antibody** for "which bot is this token" is `telegram-bot-identity-and-group-routing`
§1 — a `getMe` loop that prints the resolved username for every candidate variable at once. Use it
rather than re-deriving identity; this file owns only *which name the CLI reads*, not *which bot
each name belongs to*.

## Pitfalls

- **Inline bodies get mangled or refused.** Long text as a positional argument hits shell
  quoting and the command-size parser. Write to a file and pass `--file`.
- **Exit code 0 is not delivery.** An error object can print on stdout with exit 0 — always
  read the `--json` body and require `message_id`. Exit codes are documented as 0 ok, 1
  delivery/backend error, 2 usage error; the contract you act on is the body.
- **`--json` is a flag, not the body.** It takes no argument. `hermes send --to X --json '<text>'`
  parses `<text>` as the positional message and happens to work — but read it as `--json` +
  positional and the next edit is safe; read it as "`--json` carries the text" and
  `hermes send --to X --json` silently reads **stdin** instead.
- **A CLI delivery does not appear in the live session's outbound log.** That is expected,
  not a failure. Verify against the returned `message_id`, not the session.
- **Sending at the wrong hour.** When the recipient is on a short sleep window or the send
  will wake someone, raise the timing once as a question — then send what the human decided.
  The timing call is theirs.

## Attribution — whose sentence is it

- **Words the human wrote and handed to you:** keep verbatim, put their name in the first line
  ("<Name> suruh aku sampaikan: …"), add nothing of your own below it. The bot's name is on
  the envelope; the human's name must be on the sentence, or the reader cannot tell whose
  words these are.
- **Words you composed:** never put them in a human's mouth. A machine-written line forwarded
  under someone's name is not them and they will not recognise it. Attribute it to yourself
  as the agent, or don't send it.
- **When the human asks you to relay, the relaying is the request.** Refusing because "it
  should come from them" mistakes authorship for channel — asking a member of the household
  to pass a message is ordinary human practice. Carrying their own already-spoken sentence is
  not the same act as inventing one for them; do not refuse the second while guarding against
  the first.
- **Own the error in the same room.** If a line you sent was wrong, the correction goes where
  the wrong line went: one line, plain, no lesson attached.

## Source

`hermes send --help` (flags, exit codes) · `/root/.hermes/config.yaml:100` (`bot_token_env`) ·
`tools/send_message_tool.py:283–313` (root-cause note + `_token_from_declared_env`) ·
`venv/.../telegram/_bot.py:337` (the error string's origin) · `config.yaml` target list for the
bot ids. Live sends into a group returning `message_id` were observed 2026-09-17; the credential
name in this file was corrected the same day against the source, because the earlier explanation
was a coincidence, not a mechanism.
