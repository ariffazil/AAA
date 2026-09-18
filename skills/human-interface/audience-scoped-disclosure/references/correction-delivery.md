# Correcting Something Already Said

A sent message has no rollback. Once a wrong claim is in front of humans the only remaining move is
the correction — and its shape decides whether the room keeps the fact or the fumble.

## Decide first: correct, or let it stand

Correct when the claim is one humans may act on — a number, a time, an attribution, a fact about a
person. Let it stand when it was only a matter of tone nobody will reuse.

A correction is owed **to the room the error landed in**, not only to the principal in private.

## Shape

One message, in the plain register used in that room:

1. What was wrong, named specifically — not "an error".
2. That it was yours, with no essay about how it happened.
3. What is true instead — or that the true value is theirs to state, when only they can know it.
4. Stop. No lesson, no adjacent advice, no offer to discuss.

Never bundle the correction with advice about the subject you got wrong.

## Timing

When the timing is his to judge, hand the principal the choice. A correction that costs a night's
sleep or lands mid-crisis is a second injury. Default to the next natural window in that room and
say when it will be, so silence is not read as forgetting.

## Delivery that cannot be mistaken for a live reply

Post it standalone rather than from inside the live agent conversation, so no thread context, no
reply chain, and no pending topic rides along:

```bash
# The token's env var NAME is per-platform: read platforms.telegram.bot_token_env, and load the
# same EnvironmentFile= the gateway unit uses rather than a guessed dotfile.
set -a; . "$(sed -n 's/^EnvironmentFile=//p' /etc/systemd/system/hermes-asi-gateway.service)"; set +a
export TELEGRAM_BOT_TOKEN="$<bot_token_env name>"
hermes send --to telegram:<chat_id> --file /tmp/correction.txt --json
```

`hermes send` reuses the gateway's platform credentials directly — no LLM turn, no agent loop. It
reads `TELEGRAM_BOT_TOKEN`; when the profile stores the bot token under the platform's own name
(`platforms.telegram.bot_token_env` in the active config) that alias must be exported, or it fails
asking for a Botfather token while a valid one sits on disk. Sourcing a dotfile you merely guessed
is unreliable — the gateway's unit defines which environment file actually holds the token. If the
CLI still refuses, post to the Bot API directly and assert the returned `message_id`: full recipe in
`relay-delivery.md`.

Write the body to a file, keep it short, and verify by reading back the returned `message_id` —
`success: true` without an id is a claim, not a delivery. Deleting it again via Bot API
`deleteMessage` is possible, but ask first: the room already read it.

## After the correction

The correction is not the repair. Write the rule that produced the error where the next session will
load it, or the same class returns. Numeric claims: `auditable-numeric-artifacts`. Audience and
register claims: this skill.
