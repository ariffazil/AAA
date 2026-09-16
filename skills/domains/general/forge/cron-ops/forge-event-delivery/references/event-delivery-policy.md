# Event Delivery Policy — Full Reference

## Cron inventory policy

Each job should declare:

```yaml
job_id:
owner_organ:
host_scope:
schedule:
input_contract:
expected_state:
event_rules:
auto_remediation:
  enabled: false
  runbook_id:
  reversibility:
  authority:
dedupe_key:
evidence_sink:
telegram_route:
severity_policy:
```

### Routing decision tree

1. **Measure only** → structured log + metrics (P3, never Telegram)
2. **Detect material drift** → emit normalized event via event bridge (P1/P2)
3. **Can make bounded reversible repair** → execute under pre-approved runbook, emit receipt (P1)
4. **Needs judgment or irreversible blast radius** → 888 HOLD, no autonomous action (P0)
5. **Produces strategic intelligence** → digest only when changed materially; weekly roll-up (P2)
6. **Fails repeatedly** → one incident event with backoff/escalation, never repeated raw errors

## Event state machine

```
OBSERVED → CLASSIFIED → ACTIONED/HOLD → VERIFIED → SEALED
```

### Transition triggers

| Transition | When | Post? |
|------------|------|-------|
| NEW | Condition first crosses materiality threshold | YES |
| ESCALATED | Severity, blast radius, or duration increases | YES |
| ACTIONED | Pre-authorized automated action ran | YES |
| VERIFIED | Health/state demonstrably restored | YES |
| HOLD | Human authorization required | YES |
| RESOLVED | Condition cleared (include duration + evidence) | YES |
| SEALED | Scar or constitution update committed | YES |

### Dedup

Event ID = `hash(rule_id + host_id + resource + normalized_condition)`
Content hash = `sha256(content)` truncated to 16 chars
Delta gate: posts only when content hash differs from last posted hash.

## Message contract examples

### P1 — Verified remediation
```
FORGE | P1 | VERIFIED_REMEDIATION
event: evt_20260914_01H00_a1b2c3d4
scope: node
host: srv1946043.hstgr.cloud
rule: public_bind.wan_shim
observed: 0.0.0.0:4020
action: bind changed to 100.64.0.5; systemd restarted
verified: pid=453132 | listener=100.64.0.5:4020 | health=PASS
evidence: scar/2026-09-13/wan-shim-bind-public-2026-09-13.md
dedupe: 0e21e19e...
verdict: CLOSED
```

### P0 — Hold for human
```
FORGE | P0 | 888_HOLD
event: evt_...
scope: node
host: <host_id>
rule: unknown_public_listener
observed: tcp/15021 bound 0.0.0.0 by <process>
risk: external exposure; ownership unresolved
proposed: quarantine service and apply allow-list policy
required_auth: human approval
evidence: <path/hash>
verdict: HOLD
```

## What NOT to post

- "Working" / timer progress / terminal completion
- Clean scanner results
- Successful routine backup/prune/cert renewal
- Heartbeat/liveness pings
- "Health=green" after every scheduled run
- Raw agent deliberation
- "⏳ Working" progress messages
- Repeated failure notifications for same incident

## Rollback

Disable all event bridges:
```bash
crontab -l | grep -v 'event-bridge\|event\.sh\|weekly-digest' | crontab -
```

Individual bridge disable: remove the wrapper cron entry.
Event log persists at `/root/AAA/state/event-bridge/events.jsonl`.
