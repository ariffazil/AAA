# Watchdog — Golden Config Restore

> **CLAIM** | Source: `~/.openclaw/cron/jobs.json` + workspace audit | **Confidence:** 0.95 | **Epoch:** 2026-04-23

## Summary

The watchdog cron ensures arifOS remains operational by monitoring OpenClaw gateway health and restoring from a golden config if the agent goes silent.

---

## Watchdog Cron Job

```json
{
  "id": "171913a8-1e89-4b2d-ae82-04bcaecfac20",
  "name": "Watchdog Heartbeat",
  "schedule": { "kind": "every", "everyMs": 300000 },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "Check OpenClaw gateway health..."
  }
}
```

- **Interval:** Every 5 minutes (300,000ms)
- **Mode:** Isolated agent session (separate from main agent)
- **Channel:** Telegram (announce mode)

---

## Checkpoints

| File | Purpose | Last updated |
|------|---------|-------------|
| `~/.openclaw/golden/checkpoint.lock` | Heartbeat timestamp | `1776942080` (2026-04-23 11:01 UTC) |
| `~/.openclaw/golden/config-backup.json` | Golden config snapshot | `2026-04-23 11:04 UTC` |

---

## Restore Logic

```
IF gateway unhealthy OR silent > threshold:
  → cp ~/.openclaw/golden/config-backup.json ~/.openclaw/openclaw.json
  → openclaw gateway restart
  → WATCHDOG_RESTORE_TRIGGERED + reason
ELSE:
  → Update checkpoint.lock
  → WATCHDOG_BEAT_OK
```

---

## Pre-Requisites (Now Fixed ✅)

| Requirement | Status | Fixed |
|-------------|--------|-------|
| `config-backup.json` exists | ✅ Fixed 2026-04-23 | Now in `~/.openclaw/golden/` |
| `checkpoint.lock` writable | ✅ Active | Heartbeat running |
| Isolated cron session | ✅ Active | Every 5 min |
| Telegram announce | ✅ Configured | Sends to main session |

---

## Cross-References

- [[arifos/888_JUDGE]] — SEAL authority that watchdog protects
- [[infrastructure/OBSERVABILITY]] — Prometheus monitoring alongside watchdog

---

## Status

**Stable** — Watchdog infrastructure active and self-maintaining.

---

DITEMPA BUKAN DIBERI — 999 SEAL ALIVE