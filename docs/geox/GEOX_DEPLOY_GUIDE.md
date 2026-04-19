# GEOX Build & Deploy Guide

**For any agent working on af-forge (VPS: af-forge.tailf6bfb5.ts.net)**
**Last updated: 2026-04-12**

---

## GEOX Stack Overview

```
/opt/arifos/sites/arif-fazil.com/
├── geox/              ← geox-site (git repo)
│   ├── map/
│   │   └── index.html ← MAP PORTAL (Spatial Commons v4)
│   ├── index.html
│   ├── css/
│   ├── js/
│   ├── prospect/
│   ├── wiki/
│   ├── status/
│   ├── tools/
│   ├── skills/
│   └── workspaces/
└── arifosmcp/         ← arifOS MCP server
    └── runtime/
```

**Live URL:** `https://geox.arif-fazil.com/`

---

## Deploying GEOX Map Portal

### Files to edit
- **Live deploy:** `/opt/arifos/sites/arif-fazil.com/geox/map/index.html`
- **Git repo:** `/opt/arifos/sites/arif-fazil.com/geox/` (git repo, branch `main`)
- **Local work copy:** After editing, copy to deploy path:
  ```bash
  cp /your/file.html /opt/arifos/sites/arif-fazil.com/geox/map/index.html
  ```

### Git workflow (arifOS/geox repo)
```bash
cd /opt/arifos/sites/arif-fazil.com/geox

# Stage the file
git add map/index.html

# Commit with SEAL message
git commit -m "map: description of change

SEAL 999"

# Push (requires SSH key for github.com)
git push origin main
```

### Verifying the live site
```bash
# Check HTTP status
curl -sk "https://geox.arif-fazil.com/map/index.html" -o /dev/null -w "HTTP %{http_code}\n"

# Check line count
wc -l /opt/arifos/sites/arif-fazil.com/geox/map/index.html

# Check key features are present
grep -c "layers.bathymetry = L.tileLayer.wms" /opt/arifos/sites/arif-fazil.com/geox/map/index.html
grep -c "probeMacroSTRAT" /opt/arifos/sites/arif-fazil.com/geox/map/index.html
grep -c "layerCatalog" /opt/arifos/sites/arif-fazil.com/geox/map/index.html
```

**Required grep checks (all must pass):**
| Check | Expected | Purpose |
|-------|----------|---------|
| `wc -l` | > 1000 | File is enhanced version |
| `layers.bathymetry = L.tileLayer.wms` | ≥ 1 | GEBCO WMS layer assigned |
| `probeMacroSTRAT` | ≥ 1 | Geology probe function exists |
| `layerCatalog` | ≥ 3 | Layer registry exists |

### Using the browser tool to verify
```bash
# OpenClaw browser tool — screenshot the live page
# Use profile="openclaw" for headless Chromium on the VPS
# profile="user" for the logged-in user browser on the host machine
```

### Mobile responsive check
```bash
# Ensure responsive CSS exists for ≤768px and ≤480px
grep -c "@media (max-width: 768px)" /opt/arifos/sites/arif-fazil.com/geox/map/index.html
```

---

## Deploying arifOS MCP

```bash
cd /opt/arifos/sites/arif-fazil.com/arifosmcp
docker compose build
docker compose up -d
# Or depending on setup:
docker-compose build && docker-compose up -d
```

### Verify MCP is live
```bash
curl -sk https://arifosmcp.arif-fazil.com/health | python3 -m json.tool
curl -sk https://arifosmcp.arif-fazil.com/tools | python3 -m json.tool | head -50
```

---

## Common Tasks

### Restart a service
```bash
# Traefik / gateway
openclaw gateway restart

# Docker containers
docker compose -f /opt/arifos/docker-compose.yml restart <service>
docker compose -f /opt/arifos/sites/arif-fazil.com/docker-compose.site.yml restart
```

### Check logs
```bash
docker compose -f /opt/arifos/docker-compose.yml logs -f --tail=50 <service>
openclaw gateway status
```

### Check what's running
```bash
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
openclaw status
```

---

## Traefik Routing Notes

- `geox.arif-fazil.com` may return 404 via traefik even when direct IP:port works
- Direct access: `http://<host_ip>:8000` range for geox-site
- Traefik config: `/opt/arifos/traefik/`
- Check traefik logs: `docker logs traefik`

---

## Key URLs

| Service | URL |
|---------|-----|
| GEOX Map | `https://geox.arif-fazil.com/map/index.html` |
| arifOS MCP health | `https://arifosmcp.arif-fazil.com/health` |
| arifOS MCP tools | `https://arifosmcp.arif-fazil.com/tools` |
| GEOX Platform | `https://geox.arif-fazil.com/` |
| OpenClaw gateway | `openclaw gateway status` |

---

## For New Agents (BOOTSTRAP Notes)

When starting a session on af-forge:

1. Check temporal state: `/root/.openclaw/temporal-state.json`
2. Read workspace: `SOUL.md`, `USER.md`, `arifos.init`, `AGENTS.md`
3. Check memory: `memory/2026-04-12.md` for recent GEOX work
4. Check `GEOX_ROADMAP.md` and `TODO.md` for current state
5. **This guide:** `GEOX_DEPLOY_GUIDE.md`

---

## Principles

- **DITEMPA BUKAN DIBERI** — forged, not given. Verify before claiming.
- **888 HOLD** — if something says LIVE but isn't confirmed, label it honestly.
- **Provenance always visible** — source, license, status per layer.
- **Federate don't mirror** — prefer BBOX queries, tiles, WMS over local copies.
- **VERDICT before FORCE** — judge every action tendency before execution.

---

**999 SEAL ALIVE**
