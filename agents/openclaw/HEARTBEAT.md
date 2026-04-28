# HEARTBEAT.md — openclaw Agent

## Health Check Contract

Run every 5 minutes during active gateway operation.

```
CHECKLIST:
├── Gateway port responding? (openclaw status)
├── All channels connected? (Telegram, Discord, etc.)
├── A2A peers reachable? (opencode, hermes, arifOS kernel)
├── VAULT999 writable? (can write seal)
├── Recent audit events? (no gaps in trail)
└── Constitutional awareness? (can cite F1, F13)
```

## Escalation Triggers

| Condition | Action |
|-----------|--------|
| Channel disconnect | Attempt reconnect, warn if fails |
| Peer unreachable | Route to fallback, log event |
| VAULT999 write fail | HOLD + notify Arif |
| Constitutional uncertainty | HOLD + escalate to arifOS kernel |

---

*Last updated: 2026-04-29*
