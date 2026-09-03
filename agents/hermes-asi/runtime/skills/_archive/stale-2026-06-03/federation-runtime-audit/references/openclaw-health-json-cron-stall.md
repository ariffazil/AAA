# openclaw health --json Session Stall in Cron Environments

## Context
Session: 2026-05-18, OpenClaw watchdog debugging.

## Symptom
- 54 stalled sessions accumulated over ~7.5 hours
- Sessions stall at `model_call` stage
- Every 5-minute cron cycle spawns a new stuck session
- `openclaw health --json` itself completes in ~2.2s when run directly in terminal

## Root Cause
`openclaw health --json` is a shell command, but it **internally spawns an isolated subagent session** to probe the event loop. In cron/isolated environments:
- The subagent session cannot complete LLM API calls
- Missing credentials in that isolated context → stall at `model_call` stage
- This happens silently — no error logged, just indefinite hang

## The Pattern
```
Shell command that internally uses LLM model calls
= WILL stall in cron/isolated subagent sessions
```

## The Fix
Replace `openclaw health --json` with direct `curl` to the gateway health endpoint.

```bash
# WRONG (spawns subagent session, stalls in cron):
HEALTH_JSON=$(openclaw health --json 2>/dev/null)

# RIGHT (shell-native, no model call):
HEALTH_JSON=$(curl -sf --max-time 8 http://127.0.0.1:18789/health 2>/dev/null)
```

## Scripts Fixed
| Script | Instances Fixed |
|--------|----------------|
| `openclaw-watchdog.sh` | 3× `openclaw health --json` → `curl .../health` |
| `watchdog-heartbeat.sh` | Already correct — uses `curl` directly |

## Correct Reference: watchdog-heartbeat.sh
```bash
# This is the right pattern (42 lines, running correctly since before the incident)
HEALTH_JSON=$(curl -sf --max-time 8 http://127.0.0.1:18789/health 2>/dev/null)
```

## Verification
```bash
# Test fixed script
bash /root/.openclaw/workspace/scripts/openclaw-watchdog.sh
# Expected: EXIT 0, GATEWAY_HEALTHY in log

# Confirm stalled sessions stop spawning
# (sessions self-expire; no new ones after fix)
```

## Related Files
- `/root/.openclaw/workspace/scripts/openclaw-watchdog.sh` — fixed
- `/root/.openclaw/workspace/scripts/watchdog-heartbeat.sh` — correct reference
- `/root/.openclaw/logs/commands.log` — stalled session evidence