---
name: aaa-event-bridge
description: "Use when a cron report did/didn't reach the AAA group."
owner: Hermes
---
# AAA Event Bridge

Cron output reaches the AAA group through a **delta-gated event bridge**, not by
crons posting directly. If a report is missing, or arrives every day regardless of
change, the bridge is the thing to inspect.

## Law

AAA group is an **execution/event ledger**, not a notification channel.

- Post only on **state change** (NEW / ESCALATED / ACTIONED / VERIFIED / RESOLVED / SEALED)
- **Silent when clean** — a clean day produces zero messages
- Severity: P0 interrupt · P1 execution receipt · P2 digest · **P3 telemetry = logs only, never Telegram**

## Files

| Path | Role |
|---|---|
| `/root/scripts/event-bridge.sh` | core adapter — hash, delta-gate, post, log |
| `/root/scripts/{scanner,pulse,triage,vitality,flow}-event.sh` | per-source wrappers |
| `/root/scripts/weekly-digest.sh` | Sunday roll-up |
| `/root/A-FORGE/duties/forge-notify.sh` | delivery primitive (bot `@arifOS_bot` → `-1003753855708`) |
| `/root/AAA/state/event-bridge/events.jsonl` | **authoritative** append-only event log |
| `/root/AAA/state/event-bridge/<source>.last_hash` | delta gate |
| `/root/AAA/state/event-bridge/CRON-INVENTORY.md` | per-job declaration |

Telegram is a **projection** of `events.jsonl`, never the source of truth.

## Message contract

```
FORGE | <severity> | <event_type>
event: evt_<YYYYMMDD>_<HHMM>_<hash8>
scope: node
host: <host_id>
source: <source>
dedupe: <sha256_16>
verdict: <state>
```

`scope` + `host` are **mandatory**. An unqualified claim read across nodes is a rumor,
not a finding.

## Debugging a missing post

1. Did the parent cron produce output? Check its log.
2. Is the content hash unchanged? → bridge correctly skipped (check `*.last_hash`).
3. Did the wrapper's own condition gate it? (e.g. `triage-event.sh` only fires on aged/blocking items)
4. Check `events.jsonl` for the `event_id` — posted but delivery failed shows there.

## Wiring rules

- Bridge crons run **1 minute after** their parent cron.
- Direct `forge-notify.sh` calls from scanners are **removed** — all posts go through the bridge.
- Do not add fixed-schedule posts; gate on delta or the channel becomes noise.

## Rollback

```bash
crontab -l | grep -v "event-bridge\|event\.sh\|weekly-digest" | crontab -
```

---
*Built 2026-09-14. Replaced a fixed-schedule design that would have posted daily
regardless of change. DITEMPA BUKAN DIBERI*
