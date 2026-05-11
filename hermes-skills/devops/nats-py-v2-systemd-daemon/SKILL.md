---
name: nats-py-v2-systemd-daemon
category: devops
description: Deploy Python NATS listener daemons as systemd services on arifOS VPS. Covers nats-py v2.14.0 API quirks (error classes, connect kwargs), ProtectHome symlink trap, and the Supabase JWKS keepalive pattern.
tags: [nats, systemd, python, daemon, mesh, arifos]
created: 2026-05-07
---

# NATS Python Daemon Deployment (nats-py v2.14.0)

## Trigger
When deploying a NATS-based Python listener/daemon as a systemd service on arifOS VPS, or when debugging `ModuleNotFoundError: No module named 'nats'` / nats-py API errors in a systemd context.

## API Differences (nats-py v2.14.0 vs v1.x)

Most online docs and StackOverflow examples are written for nats-py v1.x. v2.14.0 has breaking changes:

### Error class names
```python
# WRONG (v1.x style — these don't exist in v2.14.0):
from nats.errors import ErrNoServers, ErrTimeout, ErrConnectionClosed

# CORRECT (v2.14.0):
from nats.errors import NoServersError
from nats.errors import ConnectionClosedError as ErrConnectionClosed
from nats.errors import TimeoutError as NatsTimeoutError  # alias to avoid builtin conflict
```

### connect() kwargs
```python
# WRONG - timeout= is NOT a valid kwarg in nats.connect() for v2.14.0:
nc = await nats.connect(url, timeout=10, reconnect_time_wait=2)

# CORRECT - reconnect_time_wait is valid, timeout is NOT:
nc = await nats.connect(url, max_reconnect_attempts=-1, reconnect_time_wait=2)
```

### next_msg() timeout
```python
# Correct (v2.14.0) — timeout= IS valid for next_msg():
msg = await sub.next_msg(timeout=30)

# For subscribe callbacks: no timeout needed, they fire on message arrival
```

## Python Interpreter Selection

systemd's `ProtectHome=true` blocks access to `/root`. If the venv Python is symlinked from `/root`, `ExecStart` will fail with `203/EXEC`.

```bash
# Check where nats-py is installed:
python3 -c "import nats; print(nats.__version__)"
pip3 show nats-py | grep Location

# Two options:
# Option A: System Python + nats-py installed system-wide
sudo pip3 install nats-py --break-system-packages
ExecStart=/usr/bin/python3 /path/to/script.py

# Option B: venv Python with ProtectHome=read-only or Home=tmpfs
# ProtectHome=true blocks /root symlinks → 203/EXEC
```

## Complete systemd Service Template

```ini
[Unit]
Description=ARIF-OS Agent Worker — NATS listener + Firejail executor
After=network.target arifos-nats.service
Wants=arifos-nats.service

[Service]
Type=simple
ExecStart=/usr/bin/python3 /workspace/agent-workspace/listen_and_execute.py
Restart=on-failure
RestartSec=5
StandardOutput=journal
StandardError=journal
SyslogIdentifier=arif-agent-worker
NoNewPrivileges=true
ProtectSystem=strict
ProtectHome=true           # blocks /root symlinks — use system Python or Home=tmpfs
ReadWritePaths=/workspace/agent-workspace
IPAddressDeny=0.0.0.0/0
IPAddressAllow=127.0.0.0/8

[Install]
WantedBy=multi-user.target
```

## Minimal Reconnect Pattern (v2.14.0)

```python
import asyncio, nats
from nats.errors import NoServersError, ConnectionClosedError as ErrConnectionClosed

INITIAL_DELAY = 1.0
MAX_DELAY = 60.0
BACKOFF = 2.0

async def connect_with_reconnect():
    delay = INITIAL_DELAY
    while True:
        try:
            nc = await nats.connect(
                "nats://127.0.0.1:4222",
                max_reconnect_attempts=-1,
                reconnect_time_wait=int(delay),
            )
            delay = INITIAL_DELAY  # reset on success
            return nc
        except (NoServersError, ErrConnectionClosed, OSError):
            await asyncio.sleep(delay)
            delay = min(delay * BACKOFF, MAX_DELAY)
```

## Verification Commands

```bash
# Check service status
sudo systemctl status arif-agent-worker.service

# View real-time logs
sudo journalctl -u arif-agent-worker.service -f

# Check for 203/EXEC (interpreter/symlink issue)
sudo journalctl -u arif-agent-worker.service -n 5 --reverse

# Reset after failed starts (StartLimitBurst counter)
sudo systemctl reset-failed arif-agent-worker.service

# Force a test run
sudo systemctl start arif-agent-worker.service
```

## NATS Topic Naming Convention

| Topic | Purpose |
|-------|---------|
| `system.test` | Mesh validation / firejail execution |
| `system.heartbeat` | Hourly aliveness broadcast |
| `agent.*` | Per-agent routing |
| `federation.*` | Federation-wide events |

## Supabase JWKS Keepalive Pattern

```python
import urllib.request

def ping_supabase_jwks(url: str) -> bool:
    """HTTP GET to Supabase JWKS endpoint — resets 7-day inactivity timer."""
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "arifOS-Heartbeat/1.0"},
            method="GET"
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status == 200
    except Exception:
        return False
```
