# HEARTBEAT.md — hermes-asi Agent

## Health Check Contract

```
CHECKLIST:
├── Memory accessible? (MEMORY.md readable)
├── Peers reachable? (maxhermes, hermes-ops)
├── arifOS kernel connected?
├── Delta-logger functional?
└── Constitutional floors active?
```

## Escalation Triggers

| Condition | Action |
|-----------|--------|
| Memory not found | Warn + continue |
| Peer unreachable | Route directly or HOLD |
| Constitutional uncertainty | HOLD + ask Arif |

---

*Last updated: 2026-04-29*
