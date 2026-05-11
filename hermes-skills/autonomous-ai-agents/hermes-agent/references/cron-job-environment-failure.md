# Hermes Cron Job Environment Failure — Recovery Pattern

## The Pattern

Cron job triggers (via `hermes cron`) run in a **container/CI environment** where `execute_code` and `terminal` tools may be completely non-functional:
- `execute_code` → `FileNotFoundError: [Errno 2] No such file or directory`
- `terminal` → `not_found` for all session IDs

This is environment-specific, not a script or code issue. The script is fine. The runner's tool infrastructure is broken.

## Symptoms

Cron job delivery report shows:
```
| Step | Status | Error |
| python3 scripts/wealth_daily_briefing.py | ❌ | execute_code and terminal tools non-functional |
| npm run build | ❌ | No shell execution available |
```

## Recovery — Run from Current Session

Since the current session's tools ARE working, run the script directly:

```bash
# Run from this session (tools working)
python3 /root/.local/bin/wealth_daily_briefing.py
```

## Key Fixes for Cron Job Scripts

### 1. Use absolute paths in cron prompts
```
# Wrong (relative path, breaks in cron)
python3 scripts/wealth_daily_briefing.py

# Right (absolute path, works in any environment)
python3 /root/.local/bin/wealth_daily_briefing.py
```

### 2. Output paths must match the public arif-sites path
The script outputs to `.local/arif-sites/...` but public path is `/root/arif-sites/...`. Manually sync after running:
```bash
cp /root/.local/arif-sites/sites/arif-fazil.com/public/data/wealth/latest.json \
   /root/arif-sites/sites/arif-fazil.com/public/data/wealth/latest.json
cp /root/.local/arif-sites/sites/arif-fazil.com/public/data/wealth/archive/YYYY-MM-DD.json \
   /root/arif-sites/sites/arif-fazil.com/public/data/wealth/archive/
```

### 3. Always commit after sync
```bash
cd /root/arif-sites && git add -A && git commit -m "WEALTH briefing $(date +%Y-%m-%d)"
```

## Diagnostic When Cron Fails

```bash
# Test if tools work in this session
python3 -c "print('execute_code OK')"  # or
timeout 5 echo "terminal OK"

# Test actual script
python3 /root/.local/bin/wealth_daily_briefing.py

# Check latest output
ls -la /root/arif-sites/sites/arif-fazil.com/public/data/wealth/
```

## Prevention

When creating a new cron job via `hermes cron create`, use:
- **Absolute script paths** (not relative)
- **No shell command dependencies** that require `terminal` tool
- **Explicit output sync** step if script writes to non-public paths

## Related
- `hermes-agent` → `references/hermes-docker-compose-wiring.md` — env_file config for hermes-agent container
- Cron job creation: `hermes cron create SCHED` then `hermes cron list` to verify