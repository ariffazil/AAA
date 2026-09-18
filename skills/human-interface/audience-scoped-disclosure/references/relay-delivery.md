# Delivering a Sentence the Principal Wrote for Someone Else

Task class: the principal hands over a sentence addressed to another human and says to post it. He
is delegating **transmission**, not authorship — and asking a member of the household to pass a
message along is ordinary human practice, not a breach.

## The invariant

The gate is **whose sentence it is**, never whether the subject is permitted.

- A line that began in his mouth may leave through you, when he says to send it.
- A line *you* composed — especially about the other person's body, hours, or regimen — may not. It
  reads as monitoring rather than care, and the recipient cannot answer a system back.
- "Assurance stays human-originated" governs origination, not transmission. Citing it to refuse a
  relay he asked for is a misreading of the clause.

## Procedure

1. **Verbatim.** His wording exactly — no shortening, softening, translating, or "warming up". A
   reworded line is no longer what he asked to send, and he will not recognise it.
2. **Credit it in the first line.** `<Name> pesan — word for word:` then the sentence. Every reader
   must know whose words these are: an unattributed post reads as the agent speaking for itself,
   which forfeits the property that made the relay acceptable even though the words were human.
3. **Send once, add nothing.** No preamble, no analysis, no closing commentary, no lecture about why
   he should have sent it himself. Refusing once on doctrinal grounds is a defensible judgement
   call; defending the refusal across turns *after* he restates the request is the error — it turns
   service into obstruction and costs him the turn twice.
4. **Report the witness.** Name the destination and the returned `message_id`. "Sent" without an id
   is a self-report, not a delivery.
5. **Do not re-open it.** No follow-up asking how it landed unless he asks.

## Send mechanics that work

```bash
hermes send --to telegram:<chat_id> --json '<text>'
```

This path looks for the bot token under a generic env name (`TELEGRAM_BOT_TOKEN`). When the profile
keeps it under the platform's own name instead, it fails asking for a Botfather token while a valid
one sits on disk. Resolve the name the gateway itself uses — do not guess a dotfile:

```bash
# 1. the env file the gateway actually loads
sed -n 's/^EnvironmentFile=//p' /etc/systemd/system/hermes-asi-gateway.service
# 2. the platform's own token var name: platforms.telegram.bot_token_env in the active config
#    (/root/.hermes/config.yaml and /usr/local/lib/hermes-agent/profiles/<profile>/config.yaml)
set -a; . <that EnvironmentFile>; set +a
export TELEGRAM_BOT_TOKEN="$<the bot_token_env name>"
```

If the CLI still will not resolve it, post directly — verified to return the id:

```bash
curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN_VAR}/sendMessage" \
  --data-urlencode "chat_id=<chat_id>" --data-urlencode "text=<message>" \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print('ok=',d.get('ok'),'msg_id=',d.get('result',{}).get('message_id'))"
```

- Resolve chat titles to ids with `hermes send --list telegram` instead of reading an id out of a
  transcript.
- Confirm the bot identity behind the token before posting words under his name (`getMe`).
- Never echo, log or file the token value — reference the env var name only.
- **`ok:true` AND a `message_id` are the delivery witness.** `ok:true` alone is not.

## Pitfalls

- **Refusing twice.** The first refusal can be defended; the second converts a service request into
  a doctrinal argument the principal has to win. Take his correction whole and send.
- **Dropping the attribution to keep it short.** Brevity is not worth an unowned sentence in a room
  where people know him.
- **Internal plumbing in a human lane.** Memory-staging notices, self-improvement review lines,
  receipt blocks and tool traces must never appear in a chat a human reads. Before reporting a leak,
  check the actual outbound payload in the gateway log — seeing a notice in your own session
  transcript is not evidence it was posted to the chat.
- **`Forbidden: the bot can't send messages to the bot`.** The target resolved to the bot itself.
  That is a target-resolution error, not an auth failure — fix the chat_id and retry.
- **Sending as the wrong identity.** Several bots share this host. `getMe` on the resolved token is
  the only proof of who the message will appear from.
