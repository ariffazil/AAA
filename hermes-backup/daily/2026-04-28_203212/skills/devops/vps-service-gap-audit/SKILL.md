---
name: vps-service-gap-audit
description: Audit what's actually running vs what's defined — catch services built but not deployed.
tags: [docker, compose, audit, devops, vps]
last_updated: 2026-04-28
---

# VPS Service Gap Audit — A-FORGE Pattern

> **When to use:** Suspect a service is "defined but not deployed," or need to audit what's actually running vs. what should be running.

## Audit Layer Order

### Layer 1 — Container reality
```bash
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```
Compare against the compose file's `services:` keys. Mark which are missing.

### Layer 2 — Port listeners
```bash
ss -tlnp | grep -E "7071|3001|8084|8085|8080|8081"
```
If a service is defined in compose but the port is dark, it's not running.

### Layer 3 — Caddy routes
```bash
cat /root/compose/Caddyfile
```
Check each subdomain's `reverse_proxy` directive. Static `file_server` vs live `reverse_proxy` tells you if the route is pointing at a live service or a dead landing.

### Layer 4 — .env presence
```bash
ls /path/to/service/.env
```
Missing `.env` = service can't start even if manually invoked.

## A-FORGE Specific Checklist

| Check | Command | Dead if |
|-------|---------|---------|
| Bridge container | `docker ps \| grep af-bridge` | Not found |
| Port 7071 listener | `ss -tlnp \| grep 7071` | Dark |
| Caddy forge route | `grep forge /root/compose/Caddyfile` | `file_server` instead of `reverse_proxy` |
| .env | `ls /root/A-FORGE/.env` | Not found |
| In main stack | `grep -c A-FORGE /root/compose/docker-compose.yml` | Returns 0 |

## The Key Insight

**A service can be "defined in a docker-compose.yml" but absent from the main stack.** The `A-FORGE/docker-compose.yml` defined `af-bridge-prod`, but it was never added to `/root/compose/docker-compose.yml`. The source code was there. The Dockerfile was there. The compose definition was there. But it wasn't in the *orchestrating* file.

Always check: is the service in the **orchestrating** compose file, not just its own sub-directory compose?

## 3-Compose Architecture (arifOS Federation)

The VPS runs **three separate Docker Compose projects** that interoperate:

| Project | Config Path | Role |
|---------|-------------|------|
| `a-forge` | `/root/A-FORGE/docker-compose.yml` | Metabolic shell — AgentEngine, sense bridge |
| `af-forge` | `/root/arifOS/deployments/af-forge/docker-compose.yml` | Constitutional kernel — arifOS F1–F13, VAULT999 |
| `compose` | `/root/compose/docker-compose.yml` | Shared infrastructure + domain organs |

All three are **intentionally separate** — kernel can be rebuilt without touching infra.

## Systemd Duplicate Process Pattern

When a bare process and a systemd service both try to own the same gateway:

**Symptoms:**
- `ps aux` shows two PIDs for the same binary (e.g., PID 2010856 bare + PID 2011048 systemd child)
- Port is only bound to one PID (the bare one)
- The systemd child logs repeat: `"already running under systemd; waiting 5000ms before retrying startup"` every 10s

**Diagnosis:**
```bash
# Check journal for the retry pattern — THIS IS GROUND TRUTH
journalctl -u openclaw-gateway.service --no-pager -n 20

# Check which PID actually owns the port
ss -ltnp | grep <port>

# Check CPU time — real work vs retry overhead
ps aux | grep openclaw | grep -v grep
# High CPU + high uptime = real worker
# Low CPU + low uptime = retry loop
```

**Fix — Option A (keep bare, disable systemd):**
```bash
sudo systemctl disable <service>
sudo kill <systemd-child-pid>   # systemd won't restart because it's disabled
```

**Fix — Option B (migrate fully to systemd):**
```bash
sudo kill <bare-pid>             # stop bare first
sudo systemctl restart <service>
```

**The hermes-asi-gateway case:** It failed because openclaw-gateway bare was already polling Telegram. hermes exited immediately with "Gateway already running" — correct behavior. The failed state just needed `systemctl reset-failed hermes-asi-gateway.service` to clear journal clutter.

## Deployment Lag Pattern

A commit updates `pyproject.toml` with new dependency versions (e.g., `fastmcp==3.2.4`), but the **container still runs the old version** because the image was never rebuilt.

**Detecting:**
```bash
# Repo says
grep fastmcp /root/arifOS/pyproject.toml

# Container has
docker exec <container> pip show fastmcp | grep Version
```

**Always rebuild + push + redeploy after dependency bumps.** The image SHA must match the git commit SHA for the deployment to be coherent.

## Gotcha

`.agent/` (singular) vs `.agents/` (plural) — some workflow files reference the wrong directory name. MCP Market listed `.agent/workflows/fag.md` but the repo uses `.agents/` (plural). This catches skill installs.