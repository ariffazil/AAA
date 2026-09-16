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