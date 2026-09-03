# OpenClaw Watchdog Session Stall Pattern

## Symptom
- 54+ stalled sessions accumulated over ~7.5 hours
- Every 5-minute cron cycle spawns a new stuck session
- Sessions stall at `model_call` stage
- `openclaw health --json` takes ~2.2s but completes successfully when run directly in a terminal

## Root Cause
`openclaw health --json` is shell-based, but it **spawns an isolated subagent session internally** to probe the event loop. In cron-spawned environments, the subagent session cannot complete LLM API calls (missing credentials in that isolated context), causing it to hang indefinitely at the `model_call` stage.

## The Rule
```
Shell commands that internally invoke LLM model calls
will stall in cron/isolated subagent sessions.
Use direct HTTP curl instead.
```

## The Fix Pattern
```bash
# WRONG (stalls in cron/isolated sessions):
HEALTH_JSON=$(openclaw health --json 2>/dev/null)

# RIGHT (shell-native, no model call):
HEALTH_JSON=$(curl -sf --max-time 8 http://127.0.0.1:18789/health 2>/dev/null)
```

## Which Scripts Were Affected
| Script | Problem | Fix |
|--------|---------|-----|
| `openclaw-watchdog.sh` | 3× `openclaw health --json` | → `curl .../health` |
| `watchdog-heartbeat.sh` | Already correct | No change needed |

## Verification
```bash
# Test the fixed script
bash /root/.openclaw/workspace/scripts/openclaw-watchdog.sh
# Expected: EXIT 0, no stalled sessions

# Check for stalled sessions
grep -c "model_call" /root/.openclaw/logs/commands.log
# Expected after fix: no new entries

# Check watchdog log
tail /var/log/arifOS-watchdog.log
# Expected: GATEWAY_HEALTHY entries
```

## Related Files
- `/root/.openclaw/workspace/scripts/openclaw-watchdog.sh` — patched
- `/root/.openclaw/workspace/scripts/watchdog-heartbeat.sh` — reference correct implementation
- `/root/.openclaw/logs/commands.log` — session stall evidence
- `/var/log/arifOS-watchdog.log` — watchdog run log
