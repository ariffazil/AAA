---
name: openclaw-gateway-restart-loop
description: Fix OpenClaw gateway stuck in systemd restart loop — kill stale PID then restart
---

# openclaw-gateway-restart-loop

## Problem
`systemctl restart openclaw-gateway` gets stuck in a restart loop. Systemd detects the old process still alive and refuses to start a fresh one:

```
[gateway] already running under systemd; waiting 5000ms before retrying startup
```

## Root Cause
Old gateway process (previous instance) is still bound to port 18789. Systemd's `Restart=` policy keeps killing the new attempt and re-running.

## Fix — Kill then Start

```bash
# 1. Find the stale PID
ps aux | grep "openclaw/gateway\|node.*gateway --port 18789" | grep -v grep

# 2. Force-kill it
kill -9 <PID>

# 3. Wait for port to clear
sleep 2

# 4. Now restart via systemd
systemctl restart openclaw-gateway

# 5. Verify
sleep 6 && curl -s --max-time 5 http://127.0.0.1:18789/health
# expected: {"ok":true,"status":"live"}
```

## Verification
```bash
curl -s http://127.0.0.1:18789/health
systemctl status openclaw-gateway --no-pager | grep "Active:"
openclaw channels status 2>/dev/null | grep -E "connected|stopped"
```

## Pitfalls
- `systemctl restart` alone won't clear a stuck old PID — systemd keeps it alive
- `pkill -f "openclaw-gateway"` may not catch all node child processes — use `ps aux` to find exact PID
- Wait 2s after kill before restart to allow port release (TIME_WAIT)

## Zombie OpenClaw Processes

When the gateway crashes repeatedly, multiple `openclaw` node processes accumulate. They show as many `openclaw` PIDs with high CPU% but do nothing useful. Find and kill all of them:

```bash
# Find all openclaw processes
ps aux | grep -E "openclaw|node.*gateway" | grep -v grep | awk '{print $1,$2,$3,$11}'

# Kill all stale PIDs (not the current main gateway PID)
kill -9 <pid1> <pid2> <pid3> 2>/dev/null

# Then restart cleanly
systemctl restart openclaw-gateway
```

Symptoms: many `openclaw` processes with high CPU but the actual gateway (node + openclaw-message) are on different PIDs. Check `ps aux | grep openclaw | grep -v grep` regularly during debugging.

## Python TCPServer EADDRINUSE (gateway-relay.py)

If a Python relay script (e.g. `gateway-relay.py`) fails to bind with:
```
OSError: [Errno 98] Address already in use
```
And `ss -tlnp | grep PORT` shows nothing — the socket is in TIME_WAIT from a previous process. Fix by adding `allow_reuse_address` to the HTTPServer:

```python
import socketserver

class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

class Handler(BaseHTTPRequestHandler):
    pass

server = ReusableTCPServer(('0.0.0.0', PORT), Handler)
server.serve_forever()
```

Also check `ss -tan | grep PORT` for TIME_WAIT entries that `ss -tlnp` might miss.
