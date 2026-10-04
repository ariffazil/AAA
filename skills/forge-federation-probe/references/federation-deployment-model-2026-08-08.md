# Federation Source ↔ Runtime ↔ Live Deployment Map

> **Forged:** 2026-08-08 after MCP-PROBE-2026-08-08 exposed the per-organ source/runtime paths and the `dist/build-commit.txt` trap.
> **Status:** durable — this map only changes when an organ's systemd unit changes.

## The Iron Rule

> **Edit source in `/root/<organ>/`. For arifOS, also rsync to `/opt/arifos/app/`. Then restart the systemd unit. Never edit `/opt/` directly without a matching `/root/` edit.**

If you patch a runtime file (e.g. `/opt/arifos/app/...`) without editing the source, the next `make deploy-local` (arifOS) or `make deploy` (A-FORGE) will rsync your runtime patch back over — silently destroying your work.

## Per-organ topology

| Organ | Source dir | Runtime dir | Deploy command | Restart | What "deployed" means |
|---|---|---|---|---|---|
| **arifOS** | `/root/arifOS/` | `/opt/arifos/app/` | `make deploy-local` (rsync + restart) | `systemctl restart arifos.service` | `git rev-parse HEAD` written to `/opt/arifos/app/.git_commit` by ExecStartPost |
| **A-FORGE** | `/root/A-FORGE/src/` | `/root/A-FORGE/dist/src/` (tsc compiled) | `make deploy-local` (npm build + write `.git_commit` AND `dist/build-commit.txt` + restart) | `systemctl restart a-forge-mcp.service` AND `a-forge.service` | Two units; bridge reads `dist/build-commit.txt` for BUILD_COMMIT |
| **GEOX** | `/root/GEOX/` | `/root/GEOX/` (runs from source) | Manual `systemctl restart geox-mcp.service` | same | Source IS runtime; restart picks up changes |
| **WEALTH** | `/root/WEALTH/` | `/root/WEALTH/` (runs from source) | `make deploy-local` | `systemctl restart wealth-organ.service` | User `wealth` has /dev/null write issue — write .git_commit in deploy |
| **WELL** | `/root/WELL/` | `/root/WELL/` (runs from source) | `make deploy-local` | `systemctl restart well.service` | Source IS runtime; TWO /health emitters (HTTP + FastMCP tool) |
| **AAA** | `/root/AAA/` | `/root/AAA/a2a-server/` (Node from source) | `make deploy-local` | `systemctl restart aaa-a2a.service` | Computes apex_scalars inline — no delegation |

## systemd unit map

| Organ | Unit | ExecStart | WorkingDirectory |
|---|---|---|---|
| arifOS | `arifos.service` | `python -c "from arifosmcp.runtime.__main__ import main; main()"` | `/opt/arifos/app` |
| A-FORGE | `a-forge-mcp.service` | `node dist/src/interfaces/mcp/serve.js --port=7072` | `/root/A-FORGE` |
| A-FORGE | `a-forge.service` | separate unit for the core organ | varies |
| GEOX | `geox-mcp.service` | `python3 -m geox_mcp.server --port=8081` | `/root/GEOX` |
| WEALTH | `wealth-organ.service` | `python3 server_federated.py` | `/root/WEALTH` |
| WELL | `well.service` | `python3 server.py` | `/root/WELL` |
| AAA | `aaa-a2a.service` | `node a2a-server/server.js` | (default) |

To find which unit owns a port: `ss -tlnp | grep <port>` → find `users:("node",pid=...)` → `systemctl status <unit>`.

## The A-FORGE dist/ trap (the most common pitfall)

A-FORGE has TWO source trees:
- `/root/A-FORGE/src/` — TypeScript source (committed, edited by humans)
- `/root/A-FORGE/dist/` — compiled JavaScript (gitignored, runtime artifact)

The bridge reads `BUILD_COMMIT` from `dist/build-commit.txt` at startup. For a deploy to be visible to the federation probe, three things must happen:

1. `npm run build` → regenerates `dist/src/**/*.js` from `src/**/*.ts`
2. `git rev-parse --short HEAD > dist/build-commit.txt` → updates bridge BUILD_COMMIT
3. `systemctl restart a-forge-mcp.service` → picks up new dist/

`make deploy-local` does all three. `npm run build` alone does only step 1 — the bridge will show a stale commit and Phase 6 drift probe fails.

## The GEOX git_version prefix

GEOX emits `git_version: "geox-<sha>"` (e.g. `geox-112fb70f`). The probe strips `geox-` to get the SHA. If you add a new organ with a prefixed commit format, document it in ORGAN.md so the probe knows to strip it.

## The WEALTH subprocess /dev/null trap

WEALTH runs as user `wealth` and its sandbox lacks `/dev/null` write permission. `subprocess.run(["git", ...])` returns empty stdout even on success. The health endpoint returns `git_commit: UNAVAILABLE` and `git_commit_fallback_trusted: False`. Mitigation: write `/root/WEALTH/.git_commit` from the deploy step (the probe reads `git_commit_fallback` via the fallback chain).

## WELL has two /health emitters

WELL exposes `/health` via both an HTTP endpoint (line ~19077, `_well_health_handler`) and a FastMCP tool `well_health_check` (line ~1984). The federation probe hits the HTTP one. Both need `authority_ceiling` for full coverage. The tool may report a different shape (cached state dict) — it's not the canonical wire surface.

## Makefile deploy contract (template)

Every organ should have these targets:

```makefile
deploy-local: verify
	@GIT_SHA=$$(git rev-parse --short HEAD); \
	echo "$$GIT_SHA" > .git_commit; \
	[ -d dist ] && echo "$$GIT_SHA" > dist/build-commit.txt || true; \
	systemctl restart <unit>.service; \
	sleep 3; \
	curl -sf http://127.0.0.1:<port>/health >/dev/null && echo "✅ healthy" || echo "❌ down"

verify:
	@curl -sf http://127.0.0.1:<port>/health | python3 -c \
	"import json,sys;h=json.load(sys.stdin);assert h.get('authority_ceiling'),'authority_ceiling ABSENT'; \
	print(f'✅ authority_ceiling={h[\"authority_ceiling\"]}')" || echo "❌ verify failed"
```
