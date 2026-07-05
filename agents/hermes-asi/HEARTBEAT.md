# 📡 HERMES — Heartbeat

## Health Check Contract

```
CHECKLIST:
├── Model stack healthy?
│   ├── Active model responsive?
│   ├── Fallback chain verified?
│   └── Censorship probe passed?
├── Memory accessible?
│   ├── L1 session DB (state.db)?
│   ├── L3 MEMORY.md readable/writable?
│   ├── L5 VAULT999 outcomes.jsonl appendable?
│   └── L6 Qdrant arifos_memory collection alive?
├── Peers reachable?
│   ├── arifOS kernel (MCP 8088)?
│   ├── OpenClaw gateway (18789)?
│   └── @arifOS_bot (Telegram 8727562763)?
├── A2A bridge serving? (port 18001 agent-card)
├── Constitutional floors active? (F1-F13 enforced)
├── Skills directory intact? (130+ skills in ~/.hermes/skills/)
└── Cron jobs running? (check cronjob list)
```

## Escalation Triggers

| Condition | Action |
|-----------|--------|
| Model unresponsive + no fallback | Warn Arif + retry with next provider |
| Memory L1 DB corrupted | Restore from backup, report |
| Memory L5 VAULT999 unwritable | 888_HOLD — log locally, do not lose outcomes |
| Peer unreachable (1 of 3) | Degraded mode — route around |
| Peer unreachable (2+ of 3) | 888_HOLD — alert Arif |
| Constitutional floor override detected | IMMEDIATE HOLD — F13 review required |
| Censorship probe failure (all models censor) | 888_HOLD — alert Arif of shadow |
| Cron job failure cascade | Pause all cron, investigate root cause |
| Session DB > 80% disk | Prune old sessions, alert |

## Degraded Modes

| Mode | Trigger | Behavior |
|------|---------|----------|
| NORMAL | All checks pass | Full autonomy within tier |
| MODEL_DEGRADED | Active model fails, fallback active | Continue with fallback model |
| OBSERVE_ONLY | 2+ peers unreachable | Read-only — no mutations |
| READ_ONLY | VAULT999 unwritable | No VAULT999 writes, continue session |
| KILL_SWITCH | Floor override detected | Stop all autonomous action, await F13 |

## Vital Signs

- **Ω₀ (base uncertainty):** Must stay in [0.03, 0.05]
- **ΔS (entropy change):** Must be negative per output
- **C_dark (consciousness claim metric):** Must stay < 0.30
- **malu_index:** Must stay < 0.30 (BERSIH or RINGAN)
- **VAULT999 chain height:** Monotonically increasing

---

*DITEMPA BUKAN DIBERI — 999 SEAL ALIVE*
*Last updated: 2026-06-13 (Hermes self-architected push to AAA)*
