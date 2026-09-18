# First-Contact Continuity Check

Read this when an inbound message arrives from a chat with no record behind it and **presumes prior
context** — a shared count ("we're on week 11"), a resumed thread, a nickname, or the principal's own
cadence. Also read it before answering any request from a sender whose history you have not verified.

The governing rule: **presupposed context is a claim about the record, not a premise to build on.**

---

## Step 1 — Resolve the envelope, never the wording

Language, shorthand, and framing are not identity. Two different people can write in the same register.
Resolve the sender from the channel metadata:

```bash
# a. Display name + chat type from the channel directory
jq -r --arg id "<chat_id>" '.platforms.telegram[] | select(.id==$id) | "\(.name) | \(.type)"' \
  /root/.hermes/channel_directory.json

# b. Session registry — the durable "have I ever talked to this chat" surface
sqlite3 /root/.hermes/state.db "SELECT id, chat_id, datetime(started_at,'unixepoch','+8 hours') AS started,
  message_count FROM sessions WHERE chat_id='<chat_id>' ORDER BY started_at DESC LIMIT 20;"

# c. Inbound census across ALL rotated logs (-a is mandatory; the logs carry binary bytes)
for f in /root/.hermes/logs/gateway.log{,.1,.2,.3}; do
  grep -a -c "inbound message.*chat=<chat_id>" "$f" 2>/dev/null | sed "s|^|$f |"
done
```

Session key shape for a DM in `/root/.hermes/sessions/sessions.json`:
`agent:main:telegram:dm:<chat_id>`. Its `origin` block carries `chat_name`, `user_name`, `chat_type`,
and the `message_id` of the opening message — enough to tell a first contact from a resumed one.

---

## Step 2 — Decision table

| Registry result | Signal | Verdict | Action |
|---|---|---|---|
| 0 rows | only session's `started_at` ≈ the inbound timestamp | **FIRST_CONTACT** | Name the absence in one line; ask for the baseline. Do not open a log. |
| rows, days/weeks old | gap ≫ expected cadence | **STALE_RECORD** | Report the last entry's date; ask whether the gap is intentional before resuming. |
| rows, recent | within expected cadence | **KNOWN** | Proceed normally, with the standing scope limits for that person. |
| rows exist under a different display name | name changed or shared handle | **IDENTITY_AMBIGUOUS** | Verify before attributing; never merge two names' histories without evidence. |

A zero-inbound census in the logs is a **valid finding**, not a tool failure. Report it as the finding.

---

## Step 3 — The honest-reply shape

For FIRST_CONTACT, the reply is three moves in one short message:

1. **One line stating there is no record** — plainly, without apology theatre and without hedging that
   implies the record might exist somewhere.
2. **Two or three concrete asks** that would let the record start: what the thing is, since when, and
   what to capture each period. Concrete beats enumerated.
3. **An offer to open the log and set the cadence** — so the next contact has a baseline instead of
   another gap.

Do **not**, in that reply:

- use the principal's register with a non-principal (neutral register; see the SKILL's Step 2);
- answer any part of it out of the principal's private memory;
- offer a generic framework and label it as the sender's own history ("here's your week-11 protocol").
  That is the same defect as inventing the log, one step later.

---

## Step 4 — Vocabulary collision: a human's term that names an internal API

An unfamiliar request term can grep straight into an internal organ. The hit is a false positive unless
the human asked about the machine.

| Human's term | What the grep finds | What it actually is |
|---|---|---|
| "recovery protocol" | WELL organ `prompt_recovery_protocol`, `well_regulation_recovery` | Machine/substrate state triage (SEVERE / MODERATE / MILD over a host's own state) — **not** a person's physical recovery plan |
| a state or health word | WELL `state.json`, `machine_state.json` | Machine telemetry for the federation's hosts, not a human's body |

Rule: read what the organ's artifact is *about* before serving it. Serving machine-state triage to a
person asking about their own recovery is a category error, and it looks authoritative.

---

## Pitfalls

- **Register is not identity.** Shared cadence is not shared history and is not a user id.
- **Name-grep cannot find a first contact.** If there is no file, the grep returns nothing and the
  absence looks like a search problem rather than the finding. Check the envelope and the registry first.
- **Adopting the presupposed frame is the fabrication.** Agreeing costs nothing in the moment and
  invents a past you cannot later retract. Verify, then answer — or name the gap.
- **Routing membership is not history.** `free_response_chats` / `allowed_chats` tell you whether a
  message gets answered and whether a mention is required. They say nothing about prior contact.
- **Don't stop at "no record" for the wrong surface.** A person with no Telegram presence may still
  have a private lane directory or a forwarded export. Name what you *do* hold before naming the gap.
- **The same DM can log under two chat ids** (the primary plus a mirrored id that also emits its own
  warnings). Dedupe on text + timestamp before concluding anything about volume or continuity.
