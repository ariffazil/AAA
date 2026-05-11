---
name: openclaw-event-loop-diagnosis
description: Diagnose OpenClaw gateway slowness via event loop log forensics — identifies when Node.js event loop blocking is the root cause of slow Telegram replies or gateway unresponsiveness.
trigger: "OpenClaw bot slow to reply, Telegram polling stalls, liveness warnings in logs, eventLoopDelayP99Ms elevated"
version: 1.0.0
---

# OpenClaw Event Loop Diagnosis

## Key Signal: Liveness Warnings in Logs

The log file is at `/tmp/openclaw/openclaw-YYYY-MM-DD.log` (rotated daily).

The **authoritative diagnostic signal** for gateway slowness is NOT `gateway probe` (it always fails on VPS LAN bind) — it is the `liveness warning` with `eventLoopDelayP99Ms`:

```bash
cat /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log 2>/dev/null | python3 -c "
import sys, json
lines = sys.stdin.readlines()
warnings = [l for l in lines if 'liveness' in l.lower()]
for w in warnings[-10:]:
    try:
        d = json.loads(w)
        print(d.get('time',''), d.get('message','')[:300])
    except:
        print(w[:300])
"
```

## Interpreting the Metrics

| Metric | Meaning | Healthy | Warning | Critical |
|--------|---------|---------|---------|----------|
| `eventLoopDelayP99Ms` | 99th-percentile event loop block | <500ms | 1000-5000ms | >5000ms |
| `eventLoopUtilization` | % time event loop was busy | <0.7 | 0.7-0.95 | >0.95 (=1.0) |
| `active` / `waiting` / `queued` | Tasks in event loop | any | — | queued>0 consistently |

## Root Cause Patterns

### 1. Plugin Warmup Storm (most common after restart)
```
eventLoopDelayP99Ms=12465.5 eventLoopUtilization=1
```
45 heavy plugins (playwright, pdfjs, acpx, etc.) initialize simultaneously on startup, blocking the event loop for 10-15 seconds. **This is transient** — the system recovers as plugins finish loading.

**Diagnosis:** Check the startup timestamp in logs — if liveness warnings cluster within the first 60s after gateway start, it's warmup. Look for `http server listening` as the "warmup done" marker.

### 2. Telegram API Fetch Timeout Chain
```
[fetch-timeout] fetch timeout reached; aborting operation
fetch timeout; url=https://api.telegram.org/bot.../getMe
```
Telegram API calls timeout (2.5s → 10s retry), each blocking the event loop. Often cascades from warmup storm.

**Diagnosis:** Grep logs for `fetch-timeout` and `api.telegram.org`.

### 3. Session Avalanche
```
Sessions: 29 active (or more)
```
29+ stale sessions all trying to process on startup flood the event loop.

**Diagnosis:** `openclaw sessions` shows session count and age.

### 4. Plugin Initialization Freeze (core-plugin-tools blocking)
```
bundle-mcp {"subsystem":"bundle-mcp"} failed to start server "geox" ... Not Found
agent/embedded {...} "core-plugin-tools:10113ms@10116ms"
```
A single plugin (e.g. `core-plugin-tools`) takes 10+ seconds to initialize, blocking the event loop for ALL other operations during that time. This is NOT transient warmup — it is a continuous block on every agent run cycle. The `totalMs` in trace logs shows the full prep stage duration.

**Diagnosis:** Look for `core-plugin-tools:NNNNms` in embedded-run trace logs. If >5000ms, this IS the bottleneck. Also check `bundle-mcp` warnings for MCP servers returning 404 — failing MCP endpoints cause the bundler to retry on every run, compounding the load.

### 5. MCP Endpoint Failure Cascade
When an MCP server (e.g. `geox` at `https://geox.arif-fazil.com/mcp/stream`) returns 404, OpenClaw's tool bundler repeatedly attempts to reconnect. This manifests as:
- `failed to start server "geox" ... Not Found` in logs
- Gateway appears healthy (`reachable`) but Telegram replies are slow
- Tools from that MCP server are silently excluded from the bundle

**Diagnosis:** `curl -s -o /dev/null -w "%{http_code}" https://geox.arif-fazil.com/mcp/stream` — should return 200 or 406, not 404. Also check the Caddyfile routing: container serves at `/mcp` but proxy may route `/mcp/stream` → 404.

### 6. Session Avalanche (40+ sessions)
```
Sessions: 40 active
```
40 accumulated sessions (not cleaned up) each consuming memory and CPU. Combined with plugin initialization blocking, this creates a pile-on effect where the event loop never fully recovers between runs.

**Diagnosis:** `openclaw status --deep` shows exact session count and age. Sessions older than 1h that are still "active" are ghost sessions. The event loop metric `eventLoopUtilization` stays elevated because the session store itself is under pressure.

## Decision Tree

```
Event loop delay > 5000ms?
  ├─ No  → Gateway slowness is NOT event loop. Check: network, Telegram token, MCP tool timeouts
  └─ Yes → Check timestamp: within 60s of gateway restart?
              ├─ Yes  → SABAR. Transient warmup storm. Monitor liveness trend.
              │         If `eventLoopDelayP99Ms` DECREASING over 3+ readings → recovering ✅
              │         If INCREASING or stable → gateway needs restart
              └─ No  → Check for core-plugin-tools freeze?
                        ├─ core-plugin-tools >5000ms in trace → MCP endpoint or init problem
                        │   → Check: curl https://geox.arif-fazil.com/mcp/stream
                        │   → Check: bundle-mcp warnings in logs
                        │   → Check: Caddyfile routing for /mcp vs /mcp/stream
                        └─ No  → Check session count (openclaw status --deep)
                                    ├─ 40+ sessions → restart gateway to clear session store
                                    └─ Normal → Gateway in degraded state → restart
```

## Trend Analysis

Compare 3+ consecutive liveness warnings. Recovery pattern (gateway recovering on its own):
```
14:01:18  eventLoopDelayP99Ms=12465  ← peak
14:02:57  eventLoopDelayP99Ms=11878  ← stable
14:05:05  eventLoopDelayP99Ms=7159   ← improving ✅ → SABAR, don't restart, just monitor
```

Degraded state (needs restart):
```
14:01:18  eventLoopDelayP99Ms=12465
14:02:57  eventLoopDelayP99Ms=12900  ← INCREASING
14:05:05  eventLoopDelayP99Ms=13100  ← still increasing → restart gateway
```

## Recovery Verification

After restart, verify with:
```bash
# Telegram reconnect
openclaw channels status --probe 2>&1
# Should show: running, connected, mode:polling

# HTTP reachability
curl -s --max-time 3 http://127.0.0.1:18789/ | head -3
# Should return HTML

# Event loop trend (wait 60s then check logs)
sleep 60 && cat /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log | python3 -c "..."
# eventLoopDelayP99Ms should be <5000ms and trending down
```

## Key Insight

`gateway probe` is NOT the diagnostic signal for VPS setups. On VPS with `bind: "lan"` (LAN IP 72.62.71.199), the CLI probe always hits `127.0.0.1:18789` and reports "unreachable" even when the gateway is perfectly healthy. The `channels status --probe` command is authoritative for Telegram connectivity. The event loop liveness warnings are the authoritative signal for gateway responsiveness.
