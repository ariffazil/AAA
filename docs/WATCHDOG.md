# WATCHDOG.md — Agent Silent-Death Guard

## Purpose

Watchdog prevents the **Paradox of API Key** — the agent goes silent mid-fix, config left corrupted, system unrecoverable without human intervention.

## Architecture

```
Cron (every 5 min)
    ↓
Isolated agent turn: health_check
    ↓
OpenClaw gateway health API
    ↓
[healthy] → log beat, exit
[silent > 10 min] → restore golden_config → notify
```

## Golden Config

Location: `~/.openclaw/golden/`

```
~/.openclaw/golden/
├── config-backup.json     # last known working config
├── auth-profiles.json      # API keys snapshot
└── checkpoint.lock        # "I am alive" timestamp
```

## Restoration Trigger

- Watchdog checks: if last checkpoint > 10 minutes ago AND gateway silent → restore
- Restoration = copy golden/* → active config path
- Notify via Telegram channel

## Cron Job

```bash
# Created via cron tool
openclaw cron add \
  --name "Watchdog Heartbeat" \
  --every 5m \
  --session isolated \
  --agent-turn "health_check" \
  --delivery announce \
  --channel telegram
```

## Health Check Agent Prompt

```
You are the watchdog. Check OpenClaw gateway health.

1. Run: openclaw health
2. Check: openclaw gateway status
3. Read: ~/.openclaw/golden/checkpoint.lock (last heartbeat timestamp)

If gateway is HEALTHY:
- Update checkpoint.lock with current timestamp
- Exit silently

If gateway is SILENT (>10 min since last beat):
- Restore from ~/.openclaw/golden/config-backup.json
- Run: openclaw gateway restart
- Send alert to configured channel
- Log restoration event to ~/watchdog/log.md
```

## Log

`~/watchdog/log.md` — append-only record:

```
## [YYYY-MM-DD HH:MM] watchdog | RESTORED | reason
## [YYYY-MM-DD HH:MM] watchdog | BEAT | healthy
```
