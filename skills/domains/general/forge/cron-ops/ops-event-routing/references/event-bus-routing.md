# Event-bus routing — mechanism and policy

Topical depth for ops-event-routing. Load when wiring a new producer→bridge pair or
deciding which of an existing fleet's jobs should post.

## Bridge contract

```
event-bridge.sh <source_name> <content_file> [severity]
```

1. Hash the content (`sha256`, truncated) and compare with `<source>.last_hash`.
2. Unchanged → exit 0 with no output. This is the noise floor.
3. Changed → append a structured record to the authoritative event log (`events.jsonl`),
   then project a human-readable message to the channel.
4. Write the new hash only after the projection succeeds, so a failed send retries next run.

The event log is authoritative; the chat channel is a projection of it. Never treat the
channel as the ledger.

## Event envelope

```
FORGE | <severity> | <event_type>
event: evt_<YYYYMMDD>_<HHMM>_<hash8>
scope: node | federation
host: <host_id>
source: <source_name>
dedupe: <sha256_16>
time: <ISO-8601 UTC>
verdict: NEW | ESCALATED | ACTIONED | VERIFIED | RESOLVED | SEALED | HOLD
```

Machine-readable enough to audit, one screen human-readable. Derive the dedupe key from
`hash(rule_id + host_id + resource + normalized condition)` so it is stable across runs.

## State machine — publish on transition, not on repetition

```
OBSERVED → CLASSIFIED → ACTIONED/HOLD → VERIFIED → SEALED
```

Emit only when one of these changes: NEW, ESCALATED, ACTIONED, VERIFIED, HOLD, RESOLVED,
SEALED. A standing condition that never changes becomes an incident with an escalation
policy — not a repeated daily FYI.

## Job inventory policy

Do not ask "which job should post?" Ask which outcome each job maps to:

| Job outcome | Route |
|---|---|
| measure only | structured log + metrics (P3) |
| detect material drift | emit a normalized event (P0/P1) |
| bounded reversible repair under a pre-approved runbook | execute, then emit receipt (P1) |
| needs judgment or has irreversible blast radius | create a HOLD, no autonomous action (P0) |
| strategic intelligence | digest only when materially changed, else weekly roll-up (P2) |
| fails repeatedly | ONE incident with backoff, never repeated raw errors |

Each posting job should declare: `job_id`, `owner_organ`, `host_scope`, `schedule`,
`input_contract`, `expected_state`, `event_rules`, `auto_remediation` (default disabled),
`dedupe_key`, `evidence_sink`, `channel_route`, `severity_policy`. Stored alongside the
inventory, this is a control-plane artifact rather than opaque crontab lines.

## Wiring an existing fleet

1. Enumerate every scheduled surface before changing any of them — crontab, `/etc/cron.d`,
   systemd timers, and the agent's own scheduler are separate registries that do not
   reconcile against each other.
2. Classify each job to a lane. Most jobs are P3 and need no change at all.
3. For the few signal-bearing jobs, add a bridge entry at producer-time + 1 minute.
4. Leave plumbing (backup, prune, cert renewal, reapers, rotation) untouched — it already
   has an accountable result in its log.

Do not route a whole fleet's raw output into a channel to "improve visibility"; that
converts an operations room into a dashboard nobody reads.
