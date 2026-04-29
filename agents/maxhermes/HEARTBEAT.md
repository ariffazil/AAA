# HEARTBEAT.md — maxhermes Agent

## Health Check Contract

```
CHECKLIST:
├── GEOX MCP reachable? (geox-mcp:health)
├── PhysicsGuard active?
├── Memory accessible?
├── self-verify functional?
├── Peer hermes-asi reachable?
└── Constitutional floors loaded?
```

## Escalation Triggers

| Condition | Action |
|-----------|--------|
| GEOX MCP down | HOLD + notify |
| AC_Risk ≥ 0.75 | HOLD + human review |
| PhysicsGuard void | VOID + escalate |
| Non-Earth task | Route to hermes-asi |

---

*Last updated: 2026-04-29*
