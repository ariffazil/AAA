# HEARTBEAT.md — antigravity Agent

## Health Check Contract

Run every session start and every 30 minutes during active work in the local cockpit.

```
CHECKLIST:
├── Workspace accessible? (c:\ariffazil)
├── Local git clean? (git status check for F1)
├── AppData directory active? (C:\Users\User\.gemini\antigravity)
├── MCP local servers alive? (arifos_local at localhost:8080)
└── Constitutional awareness? (can cite Floors F1–F13)
```

## Escalation Triggers

| Condition | Action |
|-----------|--------|
| Workspace inaccessible | Error block + halt |
| Local git untracked changes | Warn user to commit/stash (F1) |
| Constitutional uncertainty | HOLD + ask Arif |
| MCP offline / timeout | Enter Degraded Mode (F4 Clarity/Anti-Hantu) |

---

*Last updated: 2026-05-22*
