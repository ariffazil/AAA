# HEARTBEAT.md — opencode Agent

## Health Check Contract

Run every session start and every 30 minutes during active work.

```
CHECKLIST:
├── Context fresh? (AGENTS.md read < 1 hour ago)
├── Project structure unchanged? (git status)
├── Memory available? (can read previous session notes)
├── Tools responding? (basic read/write test)
└── Constitutional awareness? (can cite F1, F9, F13)
```

## Escalation Triggers

| Condition | Action |
|-----------|--------|
| Memory not found | Warn + continue with reduced context |
| Tool failure | Report error + degrade gracefully |
| Constitutional uncertainty | HOLD + ask Arif |
| Auth failure | Log + escalate to arifOS kernel |

---

*Last updated: 2026-04-29*
