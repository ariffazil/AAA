# GEOX Deployment Reality — systemd Service, Not Docker

> PROVEN 2026-08-26. Deploy scripts are misleading.

## The Misleading Scripts

`/root/GEOX/scripts/deploy-vps.sh` and `deploy-dimension-native.sh` both:
1. Build Docker images locally (`docker build --no-cache`)
2. SSH to `srv1325122.hstgr.cloud` (remote VPS)
3. Push images via `docker save | ssh docker load`
4. Run `docker compose up -d` on the remote

**This is NOT how GEOX actually runs.**

## Actual Deployment Architecture

GEOX runs on the LOCAL VPS (af-forge) as systemd services:

```
geox-mcp.service          → /root/GEOX/.venv/bin/python3 -m geox_mcp.server --host 127.0.0.1 --port 8081
geox-static-server.service → static site for cloudflared
geox-heartbeat.service     → organ heartbeat daemon
```

The MCP server is fronted by Cloudflare → nginx → `127.0.0.1:8081`.

## How to Deploy Changes

```bash
# 1. Edit source files in /root/GEOX/
# 2. Commit and push
git -C /root/GEOX add -A && git -C /root/GEOX commit -m "..." && git -C /root/GEOX push

# 3. Restart the service
systemctl restart geox-mcp.service

# 4. Verify
curl -s http://127.0.0.1:8081/health | python3 -m json.tool
curl -s http://127.0.0.1:8081/.well-known/mcp/server.json | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('version'))"
```

## The discovery_handler Trap

The `.well-known/mcp/server.json` endpoint is served DYNAMICALLY by `discovery_handler()`
in `server.py` (line ~3246). It does NOT serve the static `.well-known/mcp/server.json` file.

To update the live server card:
- Patch the `discovery_handler` function in `/root/GEOX/src/geox_mcp/server.py`
- Update `GEOX_VERSION` (line ~67)
- Update the `description` string (line ~3270)
- Restart `geox-mcp.service`

The static `.well-known/mcp/server.json` file in the repo is NEVER served by the live endpoint.

## Three-Way Path Split

| Layer | Path | Purpose |
|---|---|---|
| Source | `/root/GEOX/` | Git repo, editable |
| Installed | `/root/GEOX/.venv/` | Python venv (editable install) |
| Served | `127.0.0.1:8081` | systemd service reads from source |

Unlike arif-fazil.com (which has repo/deployed/WEALTH three-way), GEOX is simpler:
the service reads directly from the source directory. A restart picks up source changes.

## Pitfalls

- **Docker build timeout**: VTK (146MB) causes `deploy-vps.sh` to timeout at 120s.
  Don't use the Docker deploy scripts — use `systemctl restart` instead.
- **Remote SSH refused**: `srv1325122.hstgr.cloud:22` refuses connections.
  The remote VPS is not the deployment target.
- **Static file ≠ live endpoint**: Editing `.well-known/mcp/server.json` in the repo
  does NOT change what the live server serves. The `discovery_handler` is the source.
- **CI failures are pre-existing**: 7/9 GitHub Actions workflows fail due to
  CLAUDE.md permissions, uv lockfile drift, and test collection errors.
  These are NOT caused by GEOX changes.
