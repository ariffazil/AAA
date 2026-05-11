---
name: openclaw-chaos-recovery
description: Full restart and recovery procedure for OpenClaw gateway when sessions are stuck, Telegram is disconnected, or messages return "Something went wrong". Use when the in-process SIGUSR1 restart doesn't fix it.
tags: [openclaw, telegram, stuck-sessions, gateway, devops]
category: devops
sources:
  - af-forge VPS incident 2026-05-05 (stuck sessions, grammy missing, session store bloat, visibleReplies default change)
  - af-forge VPS incident 2026-05-07 (exit code 78 + StartLimitBurst lockout from stale process holding port 18789)
---

# OpenClaw Chaos Recovery

## OpenClaw Gateway Restart (P99 > 2000ms or stuck)

When event loop P99 exceeds 2000ms, the gateway is choking. SIGUSR1 does NOT fix it — requires a full stop/start cycle.

### CRITICAL: Use `background=true`, NOT shell `&`
The terminal tool rejects shell-level `&` backgrounding. Always use `background=true` for long-lived processes.

**Wrong (fails with "foreground command uses shell-level background wrappers"):**
```bash
cd /tmp && node /usr/lib/node_modules/openclaw/dist/index.js gateway --port 18789 > /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log 2>&1 &
```

**Correct workflow:**
```bash
# Step 1: Kill
pkill -f "openclaw.*gateway" 2>/dev/null; sleep 3

# Step 2: Start in background (background=true, NOT &)
# terminal(command="...gateway --port 18789 > /tmp/openclaw/...", background=true)

# Step 3: Wait for startup, then verify health
sleep 8 && curl -s --max-time 5 http://localhost:18789/health
```

### Post-restart verification
```bash
curl -s --max-time 5 http://localhost:18789/health
# Expected: {"ok":true,"status":"live"}
```

### Confirm fresh process (not stuck in old state)
```bash
# New log file should start ~30s ago
ls -la /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log

# Log should show "gateway ready" (not "starting channels" which was pre-restart)
tail -5 /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log | python3 -c "
import sys,json
for line in sys.stdin:
    try:
        d = json.loads(line)
        if 'gateway ready' in str(d): print('✅ FRESH START - gateway ready')
        elif 'starting channels' in str(d): print('⚠️  OLD LOG before restart')
    except: pass
"
```

## Diagnosis First

```bash
# Quick health check
curl -s --max-time 10 http://127.0.0.1:18789/health
systemctl --user status openclaw-gateway --no-pager | head -12

# What's actually happening
journalctl --user -u openclaw-gateway --since "10 minutes ago" --no-pager \
  | grep -v "Skipping escaped" | tail -30

# Stuck sessions
openclaw sessions --active 10

# Telegram/grammy issues
openclaw doctor --non-interactive 2>&1 | grep -A3 "grammy\|telegram\|channel"
```

## Step 19 — Symlink Traversal Error in exec-approvals Path

**Symptom:** `openclaw exec` fails with:
```
Refusing to traverse symlink in exec approvals path: /root/.openclaw
```

**Root cause:** `/root/.openclaw` is a symlink to a real directory. OpenClaw's exec approval system resolves the actual path and finds a symlink component in the approved path, which it refuses to traverse.

**Diagnosis:**
```bash
# Confirm it's a symlink
ls -la /root/.openclaw
# → lrwxrwxrwx 1 root root 19 May  9 07:05 /root/.openclaw -> /root/AAA/.openclaw

# Confirm exec-approvals.json path
cat /root/.openclaw/exec-approvals.json | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['socket']['path'])"
# → /root/.openclaw/exec-approvals.sock
```

**Fix:** Replace symlink with real directory. Full procedure in `openclaw-workspace-symlink-migration` skill.

**Short version (for reference):**
```bash
# 1. Smart backup (~539MB, skip 4.6GB plugin-runtime-deps)
BACKUP_DIR="/root/AAA/.openclaw.backup-$(date +%Y%m%d-%H%M%S)"
for item in workspace agents credentials audit tasks cron; do
  cp -a /root/AAA/.openclaw/$item "$BACKUP_DIR/$item"
done
for f in exec-approvals.json openclaw.json env.local delta-log.jsonl; do
  cp -a /root/AAA/.openclaw/$f "$BACKUP_DIR/$f"
done

# 2. Migrate
rm /root/.openclaw
mkdir /root/.openclaw
cp -a /root/AAA/.openclaw/workspace /root/.openclaw/
cp -a /root/AAA/.openclaw/agents /root/.openclaw/
cp -a /root/AAA/.openclaw/credentials /root/.openclaw/
cp -a /root/AAA/.openclaw/audit /root/.openclaw/
for f in exec-approvals.json openclaw.json env.local delta-log.jsonl; do
  cp -a /root/AAA/.openclaw/$f /root/.openclaw/$f
done

# 3. Fix permissions
chmod 700 /root/.openclaw
chmod -R 700 /root/.openclaw/workspace
chmod 600 /root/.openclaw/exec-approvals.json

# 4. Verify
stat /root/.openclaw | grep "Directory"  # should return "Directory" not "symbolic link"
```

**Key insight:** The exec-approvals.json socket path (`/root/.openclaw/exec-approvals.sock`) requires NO config change — it resolves correctly under the real directory.

**Note:** Gateway service may show `state failed` after migration — this predates the migration and is unrelated. Local gateway responds fine.

---

## Known Fixes

### grammy missing → Telegram won't load
Symptom: `failed to load bundled channel telegram: Cannot find module 'grammy'`
```bash
npm install -g grammy
systemctl --user restart openclaw-gateway
```

### WEALTH "Method not found" on MCP initialize (2026-05-05 update)
Symptom: `[bundle-mcp] failed to start server "wealth" ... Method not found"` during session startup, but `curl .../mcp` works fine with `id:0`. OpenClaw 2026.4.29 sends `id:null` in the initialize request — a FastMCP interop quirk. Restarting wealth-organ usually clears it transiently; the error doesn't break functionality.
```bash
docker restart wealth-organ
curl -s http://127.0.0.1:8082/health
```

### Group replies going DM instead of to group (OpenClaw 2026.4.27+)
Symptom: Bot responds in DM instead of in the group, even though group is configured with `requireMention: false`.
Cause: Since 2026.4.27, group replies are "private by default". The config setting `messages.groupChat.visibleReplies` defaults to a DM-only mode.
Fix:
```bash
openclaw config set messages.groupChat.visibleReplies '"automatic"'
systemctl --user restart openclaw-gateway
```
Config change survives restart. Verify: `openclaw channels status` shows Telegram as "running, connected".

### Stale Process Holding Port — systemd Exit Code 78 + StartLimitBurst Lockout
Symptom: Gateway shows `failed (Result: exit-code)` in `systemctl status`, exit code 78. Journal shows `"Gateway failed to start: gateway already running under systemd"` or `"Port 18789 is already in use"`. `systemctl start` fails with `"Start request repeated too quickly"`.

**Root cause:** A stale OpenClaw process (from before the last restart attempt) is holding port 18789. New systemd instance starts, detects port occupied, exits code 78. Three rapid failures within 60s trigger `StartLimitBurst=3` lockout.

**Diagnosis:**
```bash
journalctl -u openclaw-gateway --no-pager -n 30 | grep -E "exit-code|already running|18789"
ss -tlnp | grep 18789   # find stale PID
ps aux | grep openclaw | grep gateway  # confirm stale vs active
```

**Fix — two steps:**
```bash
# Step 1: Kill stale process (use pid from ss output above)
kill -9 <STALE_PID>
sleep 3

# Step 2: Clear systemd lockout and restart
systemctl reset-failed openclaw-gateway
systemctl start openclaw-gateway
sleep 8

# Verify
curl -s http://127.0.0.1:18789/health
ss -tlnp | grep 18789
```

**Prevention:** Ungraceful exits (SIGKILL, OOM, VPS reboot) leave stale processes. Monitor with `systemctl status openclaw-gateway` after any unexpected restart.

---

### Sessions stuck, queue blocking — THE MAIN CHAOS
Symptom: Messages fail with "Something went wrong", old tasks still processing.

**CRITICAL: The in-process restart (`SIGUSR1` or `/restart`) does NOT clear stuck session state.**
You need a full stop/start cycle.

```bash
# Clean stop — wait up to 30s
systemctl --user stop openclaw-gateway
sleep 5
systemctl --user status openclaw-gateway

# If stuck in "deactivating" — find ALL openclaw-related PIDs and hard kill
ps aux | grep -E "openclaw|minimax-coding" | grep -v grep | awk '{print $2}' | xargs -r kill -9
sleep 3
systemctl --user status openclaw-gateway  # should show inactive/failed

# Start fresh
systemctl --user start openclaw-gateway
sleep 8

# Verify
curl -s --max-time 10 http://127.0.0.1:18789/health
openclaw channels status
```

### Session store bloat
Symptom: 400MB+ session store, 1000+ files, gateway memory climbing.
```bash
# Preview
openclaw sessions cleanup --dry-run

# Execute (after confirming dry-run)
openclaw sessions cleanup --enforce
```

## Why SIGUSR1 Restart Doesn't Work for Stuck Sessions
The in-process restart reloads config and re-initializes channels, but the session lane queue remains blocked by whatever task was hanging (usually a timed-out LLM call). The session state persists in memory and in the session store. A full `systemctl stop/start` wipes the in-memory state.

## Verification Checklist
After every recovery:
```bash
curl -s --max-time 10 http://127.0.0.1:18789/health  # should respond in <2s
openclaw channels status  # Telegram: enabled, configured, running, connected
```
