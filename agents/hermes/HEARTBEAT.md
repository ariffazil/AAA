# HEARTBEAT.md — hermes Agent

## Health Check Contract

Run every session start and every 15 minutes during active memory operations.

```
CHECKLIST:
├── Memory index accessible? (can read memory/)
├── Daily log exists? (memory/YYYY-MM-DD.md)
├── MEMORY.md valid? (parseable, not corrupted)
├── A2A peers reachable? (openclaw, opencode)
├── Reasoning model available? (ollama ps)
└── Constitutional awareness? (can cite F2, F9)
```

## Escalation Triggers

| Condition | Action |
|-----------|--------|
| Memory not found | Warn + search alternatives |
| Index corruption | HOLD + notify Arif |
| Model unavailable | Degrade to symbolic reasoning |
| Constitutional uncertainty | HOLD + ask Arif |

---

*Last updated: 2026-04-29*
