---
name: forge-event-delivery
description: 'Delta-gated cron output delivery. P0-P3 severity routing.'
owner: AAA
---
# FORGE Event Delivery

Governs how federation output reaches human surfaces. Core principle: **state-change events belong in the group; routine telemetry belongs in logs.**

## Standing rules

1. **Every cron that posts to human surfaces MUST go through the event bridge** (`/root/scripts/event-bridge.sh`). Direct posting from cron scripts is forbidden — it bypasses delta gating and produces noise.
2. **Fixed-schedule delivery is noise.** "Post every day at 09:00" = dashboard spam. Event-driven delivery ("post only on state change") = signal.
3. **Every claim must carry host_id and scope.** A finding on one node is not a federation-wide verdict.
4. **Dedupe by content hash, not by timestamp.** Same finding re-detected = no new post.

## Event bridge usage

```bash
/root/scripts/event-bridge.sh <source_name> <content_file> [severity]
# Severity: P0 (interrupt), P1 (execution receipt), P2 (intelligence digest)
# P3 (telemetry) = logs only, never Telegram
```

The event bridge:
- Hashes content with sha256, truncates to 16 chars
- Compares against last posted hash (delta gate)
- Only posts if hash differs (NEW or ESCALATED)
- Appends to `/root/AAA/state/event-bridge/events.jsonl`
- Posts via `forge-notify.sh` to AAA group

## FORGE event format

```
FORGE | <severity> | <event_type>
event: evt_<YYYYMMDD>_<HHMM>_<hash8>
scope: node
host: <host_id>
source: <source_name>
dedupe: <sha256_16>
time: <ISO-8601 UTC>
verdict: NEW|ESCALATED|ACTIONED|VERIFIED|RESOLVED|SEALED|HOLD

<structured_content>
```

### Severity routing

| Level | Name | Posts? | Examples |
|-------|------|--------|----------|
| P0 | interrupt | YES | Security breach, data loss, outage |
| P1 | execution receipt | YES (delta) | Service restarted, scar sealed |
| P2 | intelligence digest | YES (delta) | Mesh fidelity changed |
| P3 | telemetry | NO | Clean scanner, heartbeat |

## What should post

### YES
- Scanner DRIFT DETECTED → host_id + action
- Scar sealed ≥ MEDIUM → receipt
- Persistent service registered/removed → constitution receipt
- Organ DOWN → recovery receipt
- Cross-node change → node-qualified
- Weekly digest → Sunday 22:00 MYT

### NO
- "Working", "Scanner CLEAN", heartbeat pings
- Successful routine backup/prune
- Raw agent deliberation
- Repeated failure for same incident

## Cron wrappers (delta-gated)

| Wrapper | Parent cron | Condition |
|---------|-------------|-----------|
| `scanner-event.sh` | drift_scanner (02:00) | drift found |
| `pulse-event.sh` | federation_pulse (07:47) | mesh changed |
| `triage-event.sh` | triage_digest (09:00) | actionable items |
| `vitality-event.sh` | vitality_pulse (15:00) | vitality dropped |
| `flow-event.sh` | arifflow_digest (22:00) | GOVERNANCE_COLLAPSE |
| `weekly-digest.sh` | Sun 22:00 | always |

## One-off agent relay — the exception, and how to end it cleanly

Rule 1 ("go through the event bridge") governs **scheduled** output. It does not cover a single message an agent is asked to deliver once, on behalf of a human, into a chat. That path skips delta-gating and hash-dedup on purpose — there is no second identical post to suppress — and it needs its own discipline:

- **Send outside the gateway's session.** A long-lived gateway session carries thread context; a relay composed inside it can land anchored to a stale `reply_to`, echo the in-flight conversation, or get swallowed by a delivery retry loop. Post it as a fresh standalone message instead, then report the returned message id.

  ```bash
  # resolve the bot token, then send the file as a standalone post
  set -a; . /root/.hermes/.env >/dev/null 2>&1; set +a
  export TELEGRAM_BOT_TOKEN="${HERMES_TELEGRAM_BOT_TOKEN:-$TELEGRAM_BOT_TOKEN}"
  hermes send --to telegram:<chat_id> --file /tmp/relay.txt --json
  ```

  The CLI reuses the gateway's platform credentials, so no running gateway is required for bot-token platforms; `--list` enumerates valid targets and `-t` accepts `platform`, `platform:chat_id`, or `platform:chat_id:thread_id`.
- **Resolve the token lookup before blaming the credential.** `hermes send` reads `TELEGRAM_BOT_TOKEN`, while the env file may export only the alias `HERMES_TELEGRAM_BOT_TOKEN` (declared there as an alias for the bot token). Without the explicit export the send fails with "You must pass the token you received from t.me/Botfather" *while the credential is present on disk* — that error means the lookup missed, not that the token is missing. Confirm names only, never values: `sed 's/=.*/=<set>/' /root/.hermes/.env | grep -i telegram`.
- **Write the body to a file and pass the file**, not an inline shell argument — multi-line text and quotes survive intact and the exact bytes stay auditable.
- **Never read the delivery verdict through a pipe.** `hermes send … --json 2>&1 | tail -20; echo $?` prints the status of `tail`, so a failed send looks like a clean one. Branch on the parsed JSON instead: `success: true` plus a `message_id` is DELIVERED, an `error` key is a failed send regardless of shell status. If you need the code itself, capture it without piping.
- **`message_id` is the delivery proof.** Report the state you actually reached ("posted, id N"), never "sent" or "done". No id back = PRODUCED, not DELIVERED.
- **Attribute relayed words to their human.** When the sentence belongs to a person who asked you to deliver it, put their name in the message's first line. The channel is the agent's; the sentence is theirs. Unattributed, a relayed sentence reads as the agent's own opinion, which changes what it means to the person receiving it — and to anyone else in the chat who later reads it as the record.
- **Never author the sentence.** Carrying a human's words is fine; composing words and putting them in their mouth is not. Verbatim, attributed, nothing added.
- **If the content corrects an error you made, say so in the same message shape** — the correction belongs to the agent, the reassurance belongs to the human, and they should not be blended into one voice.

## State machine

OBSERVED → CLASSIFIED → ACTIONED/HOLD → VERIFIED → SEALED

Only publish on transitions: NEW, ESCALATED, ACTIONED, VERIFIED, HOLD, RESOLVED, SEALED.
No repeat unless state changes.

## Pitfalls

1. **Node qualifier is mandatory.** Observation on srv1946043 ≠ statement about KVM8. Every event must carry `host: <host_id>` and `scope: node`.
2. **Fixed-schedule = noise fatigue.** Week 1 gets read. Week 2 ignored. Delta gating prevents this.
3. **Telegram is projection, not source of truth.** Authoritative log: `/root/AAA/state/event-bridge/events.jsonl`. Design for log first, project to Telegram second.
4. **Content hash dedup needs stable output.** Timestamps/UUIDs in output = hash changes every run = delta gate broken.
6. **Gate on SUBSTANCE, not on the message text.** The bridge hashes the whole body, so
   any volatile field in it — run counts, per-item frequency, durations, a run timestamp —
   makes two identical outcomes hash differently and post twice. The fix is at the emitter:
   compute a digest over the *decision content only* (which items changed state, and to
   what), compare it against a stored marker, and keep volatile counts OUT of the body.
   Otherwise a loop that runs on a schedule posts on every tick while looking delta-gated.
7. **Write the dedupe marker only AFTER the bridge accepts.** If the marker is written
   before the post, a delivery failure is recorded as delivered and the event is lost
   silently. Ordering: post → confirm → record.
8. **The stability rule applies to your own emitter first.** Rule 4 is easy to satisfy for
   a scanner reading a file and easy to violate for a producer that composes its own
   message. If your source text is generated, the delta gate is only as stable as your
   generator.
5. **Severity auto-classification is heuristic.** Override with explicit severity when keywords are wrong.

## Files

- Bridge: `/root/scripts/event-bridge.sh`
- Log: `/root/AAA/state/event-bridge/events.jsonl`
- State: `/root/AAA/state/event-bridge/<source>.last_hash`
- Inventory: `/root/AAA/state/event-bridge/CRON-INVENTORY.md`

---
*DITEMPA BUKAN DIBERI ⚒️ · arifOS F1-F13*