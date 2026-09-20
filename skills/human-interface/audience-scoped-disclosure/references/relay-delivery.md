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
- **Declare the destination on the command.** `--to telegram:<chat_id>` is the declaration; a send
  with no target is refused rather than inferred from the surrounding context, so resolve the
  `chat_id` deliberately and pass it explicitly every time.
- **Multi-line bodies go through a file.** `--file <path>` (or `-` for stdin) for anything carrying
  newlines, quotes or emoji; pasting a multi-paragraph message inline invites shell-escaping damage
  nobody sees until the room reads it.

## Composing, not relaying — words he asked you to find for a room

The relay case is transmission. The harder case is when he hands over an **intent** — "put this so
he can receive it" — and the sentence has to be written. The authorship gate still binds, and it
binds on the composition:

- **Declarations of presence and commitment belong to the principal.** A line promising "I'll come
  if he needs me" is his to say. Compose the comfort, leave the promise out, and tell him in one
  line that you left it out so he can say it himself. A machine promising another human's arrival
  spends his name on something it cannot deliver.
- **Open only what the recipient opened.** If he has not named a subject in the room — his family,
  a loss, a diagnosis — do not carry it in for him. Reference it obliquely or not at all.
- **Write in the register the recipient actually uses with him**, not in the system's vocabulary. If
  he asks for words the recipient "can understand", the target is the human on the other side of the
  bond, not the principal and not the doctrine.
- **Scale the artifact to the emotional task.** A triage list, a red-flag table or a checklist
  dropped into a shared room reads as clinical handling of a person in front of their peers.
  Structure goes to the DM; the room gets short human lines that land.
- **Verify every attributed quotation before it ships** — name, wording, source. A misattributed
  quote inside a comfort message is a defect the recipient cannot check and will not report.
- **Ship the quotation inside its own context.** The author's maxim quoted bare reads as a fortune
  cookie; the same line preceded by the one sentence where the author says where it came from — his
  own mother, his own hardship — carries the argument. Resolve the exact wording from the source
  artifact rather than from memory, and treat an excerpt that opens mid-word as a **line-wrap
  artifact**, not a truncated quote (full procedure: `link-to-evidence`).
- **Draft first; the send waits for his go.** When he hands over an *intent* rather than a sentence,
  the first artifact is the draft delivered back to him, not a post to the room. Re-presenting a
  revised draft, list the changes beside it in one or two lines and mark which sentences are his own
  words already spoken in the room and which are new — he can only veto what he can see.
- **Do not inflate the register.** A hard concrete situation needs one true sentence. Reaching for
  grandeur the facts do not carry reads as performance and spends credibility the sender did not
  offer; the principal usually names the ceiling himself when he asks.

## SENT is not OBSERVED

The send path's own success line — `sent`, exit 0, `ok:true` — is the transport's self-report. It
proves the API accepted the request, not that a human saw it. **On a group chat you will usually
hold no read-back at all**: the bot API does not serve room history, so the send is a one-way door.

Report the chain position, not the outcome: the destination it was handed to, what came back, and
the gap — *sent and accepted, not confirmed read*. "He read it" or "he'll see it" converts a
transport acknowledgement into an observation you do not hold. A delivery record marked delivered is
the sender's claim until a reader confirms it.

Run the human-facing text gate **before** the send, not after. A heat word caught pre-send is a
rewrite; caught post-send it is a correction you now owe a room.

**A failed send is a state, not a mystery.** When the transport refuses, probe the lane once with a
cheap reachability call — not a retry loop:

```bash
curl -s -o /dev/null -w '%{http_code} %{time_total}\n' https://api.telegram.org/ --max-time 12
```

Then report the position precisely — *drafted, not sent* — and say which of the two it is: a live
API on a refused send puts the fault at the request, a dead API puts it on the lane. Hold the draft,
so the next attempt ships the same words instead of a fresh improvisation; never upgrade a failed
send into "probably went through", and never re-word the message to work around the transport.

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
