# VPS Map — arifOS Federation

> **DITEMPA BUKAN DIBERI** — Intelligence is forged, not given.
>
> This file is the canonical orientation surface for zero-context agents.
> Last updated: 2026-05-03 by Kimi Code (ARIF-KIMI).

---

## 1. Canonical Roots

| Path | Purpose | Notes |
|------|---------|-------|
| `/root` | Operator home + main repo warehouse | Terminal starts here. Most repos live directly under `/root`. |
| `/root/compose` | Docker Compose stack definition | `docker-compose.yml`, `.env`, Caddyfile copies, secrets. |
| `/root/sites` | **Live web root source** | Bind-mounted into `caddy` container as `/var/www/html`. This is what Caddy actually serves. |
| `/var/www/html` | Web root (host view) | **Same underlying directory as `/root/sites/`**. Changes here are live. |
| `/root/volumes` | Persistent Docker data | postgres, qdrant, caddy, vault999, ollama. |

---

## 2. Git Repositories

| Organ | Repo Path | Branch | Notes |
|-------|-----------|--------|-------|
| arifOS | `/root/arifOS` | `main` | Constitutional kernel. Python 3.12. FastMCP. |
| A-FORGE | `/root/A-FORGE` | `main` | Metabolic shell. Node.js 22 + TypeScript. |
| AAA | `/root/AAA` | unknown | Agent control plane. |
| GEOX | `/root/geox` | `main` | Earth intelligence. Python 3.11. |
| WEALTH | `/root/WEALTH` | `main` | Capital intelligence. Python 3.12. Monolith. |
| arif-sites | `/root/arif-sites` | unknown | Static sites for subdomains. |
| arifos-command-center | `/root/arifos-command-center` | unknown | Operator console. |
| arifos-model-registry | `/root/arifos-model-registry` | n/a | Model artifacts. Mounted read-only into arifosmcp. |
| compose | `/root/compose` | `main` | Deployment manifests. NOT a code repo per se. |

---

## 3. Deployment & Config

### 3.1 Docker Compose
- **File SOT**: `/root/compose/docker-compose.yml`
- **Env SOT**: `/root/compose/.env`
- **Command**: `cd /root/compose && docker compose ...`

### 3.2 Reverse Proxy
- **Caddyfile SOT (LIVE)**: `/root/arifOS/Caddyfile`
  - Mounted into `caddy` container at `/etc/caddy/Caddyfile:ro`.
  - **WARNING**: `/root/compose/Caddyfile` exists but is **NOT mounted**. It is stale (9811 bytes vs live 12356 bytes).
- **Web root SOT (LIVE)**: `/root/sites/`
  - Mounted into `caddy` container at `/var/www/html:ro`.
  - `/var/www/html/` on the host is the **same directory** (bind mount or symlink).

### 3.3 Important Files
| File | Purpose |
|------|---------|
| `/root/compose/.env` | Docker Compose environment variables |
| `/root/compose/secrets/` | Docker secrets mount |
| `/root/compose/dozzle-users.yml` | Dozzle auth config |

---

## 4. Per-Organ Runtime Details

### arifOS Kernel
| Field | Value |
|-------|-------|
| Repo | `/root/arifOS` |
| Compose service | `arifosmcp` |
| Container name | `arifosmcp` |
| Image | `ghcr.io/ariffazil/arifos:latest` |
| Python runtime | 3.12 |
| **Container import path** | `/app/arifosmcp/` (shadows `/usr/src/app/arifosmcp/`) |
| Volume mount (host→container) | `/root/arifOS/arifosmcp/runtime/rest_routes.py` → `/usr/src/app/arifosmcp/runtime/rest_routes.py:ro` |
| **Dual-path bug** | Host file mounted to `/usr/src/app/...` but Python imports from `/app/...`. See `DOCKER_VOLUME_AUDIT.md`. |
| MCP URL | `https://arifos.arif-fazil.com/mcp` |
| Health | `https://arifos.arif-fazil.com/health` |
| Build info | `https://arifos.arif-fazil.com/api/build-info` |
| SOT drift | `https://arifos.arif-fazil.com/inspector/sot` |
| Inspector | `https://arifos.arif-fazil.com/webmcp` |
| Observatory | `https://arifos.arif-fazil.com/` |

### GEOX
| Field | Value |
|-------|-------|
| Repo | `/root/geox` |
| Compose service | `geox` |
| Container name | `geox_eic` |
| Image | `af-forge-geox` (built locally) |
| Python runtime | 3.11 |
| Container import path | `/app` |
| MCP URL | `https://geox.arif-fazil.com/mcp` |
| Health | `https://geox.arif-fazil.com/health` |
| Discovery | `https://geox.arif-fazil.com/.well-known/mcp/server.json` |
| GUI container | `geox_gui` (nginx:alpine) |

### WEALTH
| Field | Value |
|-------|-------|
| Repo | `/root/WEALTH` |
| Compose service | `wealth-organ` |
| Container name | `wealth-organ` |
| Image | `compose-wealth-organ:v1.0.0` |
| Python runtime | 3.12 (in venv at `/app/.venv`) |
| MCP URL | `https://wealth.arif-fazil.com/mcp` |
| Health | `https://wealth.arif-fazil.com/health` |
| Ready | `https://wealth.arif-fazil.com/ready` |

### WELL
| Field | Value |
|-------|-------|
| Python runtime | 3.12 |
| Status | Live in compose, but was previously removed. Now restored. |

### AAA
| Field | Value |
|-------|-------|
| Repo | `/root/AAA` |
| Compose services | `aaa`, `aaa-a2a` |
| Container names | `aaa-a2a`, `hermes-agent` |
| Images | `aaa-a2a:v1.0.0`, `hermes-agent:v1.0.0` |
| Runtime | Node.js |
| A2A URL | `https://aaa.arif-fazil.com/a2a` |
| Health | `https://aaa.arif-fazil.com/health` |

### A-FORGE
| Field | Value |
|-------|-------|
| Repo | `/root/A-FORGE` |
| Compose service | `forge-notifier` |
| Container name | `af-bridge-prod` |
| Image | `a-forge-af-bridge` |
| Runtime | Node.js 22 |
| Bridge URL | `https://arifos.arif-fazil.com` (proxied via Caddy) |
| Health | Not exposed publicly; internal port 7071. |

### Ω-Wiki
| Field | Value |
|-------|-------|
| Source | `/root/arif-sites/sites/wiki.arif-fazil.com/` |
| Deployed | `/root/sites/wiki/` (or `/var/www/html/wiki/`) |
| URL | `https://wiki.arif-fazil.com` |
| Type | Static site. No MCP endpoint. |

---

## 5. Persistent Data Volumes

| Host Path | Container | Purpose |
|-----------|-----------|---------|
| `/root/volumes/postgres` | `postgres:/var/lib/postgresql/data` | VAULT999 + app data |
| `/root/volumes/qdrant` | `qdrant:/qdrant/storage` | Vector memory |
| `/root/volumes/caddy/data` | `caddy:/data` | TLS certs, Caddy state |
| `/root/volumes/caddy/config` | `caddy:/config` | Caddy config |
| `/root/volumes/ollama` | `ollama:/root/.ollama` | Local models |
| `/root/volumes/vault999` | `vault999:/var/lib/arifos/vault` | Vault ledger |
| `telemetry-data` (Docker vol) | `arifosmcp:/app/telemetry` | Telemetry |

---

## 6. Known Chaos / Dual Paths

| Issue | Location | Impact |
|-------|----------|--------|
| **rest_routes.py mount mismatch** | arifosmcp container | Host edits to `/usr/src/app/...` are ignored; runtime uses `/app/...` |
| **Caddyfile duplicate** | `/root/compose/Caddyfile` vs `/root/arifOS/Caddyfile` | Only `/root/arifOS/Caddyfile` is mounted. The compose copy is stale. |
| **Sites dual visibility** | `/root/sites/` vs `/var/www/html/` | Same directory, but agents may be confused which is "canonical". |
| **GEOX container name mismatch** | Compose `geox` → runtime `geox_eic` | `docker compose restart geox` may not match `docker restart geox_eic`. |
| **hermes-agent origin** | Not in main `docker-compose.yml` services | May be from secondary compose or manual run. |

---

## 7. Quick Reference

```bash
# Restart arifOS kernel
cd /root/compose && docker compose restart arifosmcp

# Restart all federation organs
cd /root/compose && docker compose restart geox wealth-organ

# View live Caddyfile
cat /root/arifOS/Caddyfile

# View live web root
ls -la /root/sites/

# Check container import paths
docker exec arifosmcp python3 -c "import arifosmcp.runtime.rest_routes as r; print(r.__file__)"
```
