# OpenClaw Gateway Immortality Protocol
**Date:** 2026-05-17 | **Executor:** Hermes | **Status:** PARTIAL SUCCESS (WatchdogSec + Timer live; Security hardening deferred)

---

## Context

OpenClaw gateway (port 18789) was in a 7-restart loop due to:
- Orphan PID 944202 holding the port
- systemd service `exit code 78` interpreted as failure
- `systemctl is-enabled` = **disabled** (would NOT survive reboot)
- No WatchdogSec (no alive ping from systemd)
- Telegram 409 Conflict = dual polling (systemd + orphan both running)

---

## Execution Log

### Phase A: Orphan Kill + Systemd Reset

```bash
openclaw gateway stop
# Output: "Gateway service disabled."
# Orphan PID 944202 killed, port 18789 released

ss -tulpn | grep 18789
# Output: (empty — port free)

systemctl reset-failed openclaw-gateway.service
systemctl start openclaw-gateway.service
systemctl enable openclaw-gateway.service  # enabled for boot
```

### Phase B: Apply WatchdogSec

Added to `[Service]` section:
```ini
WatchdogSec=60
```

### Phase C: Health Guardian Timer

Created `/usr/local/bin/openclaw-health-guardian.sh` + systemd timer running every 5 min.

### Phase D: Security Hardening Attempt → FAILED

Applied to service file:
```ini
ProtectSystem=strict
ProtectHome=read-only
ReadOnlyPaths=/
```

Result: `exit code 226/NAMESPACE` — **Node.js cannot read modules under strict ReadOnlyPaths**

Recovery: Restored original service file (without strict hardening), gateway healthy.

---

## Final Working Service File

```
[Unit]
Description=OpenClaw Gateway (Host-based)
After=network.target docker.service
Wants=network.target

[Service]
Type=simple
Restart=always
RestartSec=10
StartLimitInterval=60
StartLimitBurst=3
User=root
WorkingDirectory=/root
Environment="PATH=..."
Environment="HOME=/root"
Environment="NODE_OPTIONS=--max-old-space-size=1024"
Environment="OPENCLAW_GATEWAY_PORT=18789"
ExecStart=/usr/local/bin/openclaw-gateway-secure.sh
TimeoutStopSec=30
KillSignal=SIGTERM
RestartKillSignal=SIGTERM
WatchdogSec=60
LimitNOFILE=65536
LimitNPROC=8192

[Install]
WantedBy=multi-user.target
```

---

## Final State

| Component | Status |
|-----------|--------|
| Service | ✅ `active (running)` PID 54434 |
| Boot enable | ✅ `enabled` |
| WatchdogSec 60s | ✅ Active |
| Health Guardian Timer | ✅ Active, every 5 min |
| Telegram | ✅ Clean polling |
| Port 18789 | ✅ Owned by systemd |
| Security hardening | ❌ Deferred (Node.js namespace issue) |

---

## Key Learnings

1. **`openclaw gateway stop` sometimes leaves orphans** — must verify port is free after running it
2. **`exit code 226/NAMESPACE` = systemd namespace isolation blocking Node.js** — never apply `ProtectSystem=strict + ReadOnlyPaths=/` to Node.js services
3. **`exit code 78` from openclaw-gateway-secure.sh = "gateway already running under systemd; existing gateway is healthy"** — indicates orphan process, not an actual failure
4. **Linger must be enabled** for user-level systemd services on headless VPS: `loginctl show-user root | grep Linger` → `Linger=yes`
5. **WatchdogSec is the single most important immortality feature** — it auto-restarts frozen services without external monitoring

---

## VAULT999 Integration (TODO)

Health guardian script was designed to write audit events to VAULT999 PostgreSQL, but:
- `/root/.vault999-pw` not found
- VAULT999 connection string not available in this context

Future: complete the VAULT999 audit trail for health guardian events (service restart → VAULT999 `vault_seals` or separate `openclaw_health_log` table).