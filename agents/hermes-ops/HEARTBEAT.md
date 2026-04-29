# HEARTBEAT.md — hermes-ops Agent

## Health Check Contract

```
CHECKLIST:
├── docker running?
├── git configured?
├── claude-code functional?
├── github-pro connected?
├── arifos-deploy ready?
├── Recent deployments succeeded?
└── Constitutional floors active?
```

## Escalation Triggers

| Condition | Action |
|-----------|--------|
| Docker down | HOLD + notify |
| Git auth fail | HOLD + fix auth |
| Deploy failure | HOLD + rollback |
| Destructive op | 888_HOLD + human |

---

*Last updated: 2026-04-29*
