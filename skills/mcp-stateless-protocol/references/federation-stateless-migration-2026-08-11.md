# Federation Stateless Migration State — 2026-08-11 (UPDATED)

> **Last probe:** 2026-08-11T04:50Z
> **Key finding:** arifOS IS on 2026-07-28 spec (older reference file was stale)

## Active MCP Endpoints (live probed)

### Internal (127.0.0.1)

| Port | Server | Proto Version | Tools | Stateless? | Binding |
|------|--------|--------------|-------|-----------|---------|
| :8088 | arifOS MCP | **2026-07-28** ✅ | 8 | ✅ YES | 127.0.0.1 |
| :7071 | A-FORGE Sense | 2024-11-05 | 116 | ❌ | 127.0.0.1 |
| :7072 | A-FORGE MCP | (not declared) | 48 | ⚠️ sessions=active | **100.64.0.2 (Tailscale only)** |
| :8081 | GEOX | (not declared) | 18 | ❌ | 127.0.0.1 |
| :18082 | WEALTH | (not declared) | 11 | ❌ | 127.0.0.1 |
| :18083 | WELL | (not declared) | 10 | ❌ | 127.0.0.1 |

### Public (Caddy → Cloudflare)

| Domain | → Backend | Status | Role |
|--------|-----------|--------|------|
| `mcp.arif-fazil.com/mcp` | :8088 | ✅ 200 | Canonical public door |
| `arifos.arif-fazil.com/mcp` | :8088 | ✅ 200 | Observatory |
| `geox.arif-fazil.com/mcp` | :8081 | ✅ 200 | Direct (drift) |
| `wealth.arif-fazil.com/mcp` | :18082 | ✅ 200 | Direct (drift) |
| `well.arif-fazil.com/mcp` | :18083 | ✅ 200 | Direct (drift) |
| `aaa.arif-fazil.com` | :3001 | ⚠️ 404 | A2A (not MCP) |

**Current state:** 1/5 organs on 2026-07-28 spec (arifOS only). 5 public subdomains exist — architecture drift from the single-door doctrine.

## SDK Versions (live probed via pyproject.toml + venv)

| Organ | Stack | Version | Stateless Capable? |
|-------|-------|---------|-------------------|
| arifOS | fastmcp | 3.4.6 | ✅ Already deployed |
| arifOS | mcp SDK | 1.27.2 | ✅ via FastMCP |
| GEOX | fastmcp | 3.4.5 | ❓ verify upstream |
| WEALTH | fastmcp | 3.4.6 | ❓ verify upstream |
| WELL | fastmcp | 3.4.5 | ❓ verify upstream |
| A-FORGE | @modelcontextprotocol/sdk | ^1.9.0 | ❓ verify npm registry |

**Note:** FastMCP versions upgraded 3.4.2 → 3.4.5/3.4.6 since earlier probes. Always re-probe live.

## A-FORGE Dual-Port Architecture (detailed)

A-FORGE runs **two services in one Node process** (`/usr/bin/node /root/A-FORGE/dist/src/interfaces/server.js`):

```
Process: PID 2131409, user=forge
  :7071 → Express HTTP bridge (116 tools, internal RPC)
  :7072 → MCP Streamable-HTTP (48 stateless tools)
```

### The binding bug

`:7072` binds `100.64.0.2` (Tailscale mesh IP) only, NOT `127.0.0.1`:

```
LISTEN  127.0.0.1:7071    → node (A-FORGE server)    ✅ local reachable
LISTEN  100.64.0.2:7072   → tailscaled proxy          ❌ localhost can't reach
```

Impact:
- Caddy routes `mcp.arif-fazil.com/api/organs/aforge/*` → `127.0.0.1:7072`
- But `:7072` doesn't listen on `127.0.0.1`
- **Result:** Caddy gets connection refused, A-FORGE MCP has no public door

### Architecture source

From `/root/A-FORGE/src/interfaces/server.ts`:
- Imports both Express routes AND `StreamableHTTPServerTransport` from `@modelcontextprotocol/sdk`
- Single Node process serves both ports
- MCP transport uses `StreamableHTTPServerTransport`
- Internal `STATELESS_TOOLS` whitelist in `:7072` — read-only tools bypass session

### Port collapse opportunity

Since both ports run in same process, collapse is feasible:
1. Mount MCP transport as Express routes on `:7071` (path `/mcp`)
2. Fix binding to `127.0.0.1`
3. Update Caddyfile: `reverse_proxy 127.0.0.1:7072` → `127.0.0.1:7071`
4. Kill dual-port complexity, entropy reduced

### Systemd services

```
a-forge.service              → active (main process, both ports)
aforge-heartbeat.service     → active
a-forge-mcp-test.service     → FAILED (dead since Aug 10, disable)
```

## Architectural Decision (F13 ratified 2026-08-11)

**Verdict: Option 3 + Option 5 — Hybrid Federation → APEX Registry**

The 5 options evaluated:

| Option | Pattern | Score |
|--------|---------|-------|
| 1. Multi-Door | Keep subdomains | 60 |
| 2. Single Door | All through arifOS | 60 |
| 3. Hybrid Federation | arifOS=governance, organs=execution | 76 ✅ |
| 4. Service Mesh | Envoy/Istio | 20 |
| 5. APEX Registry | Discovery + direct routing | 80 ✅ |

### Why not single door?

arifOS authority ceiling = `JUDGE_ONLY`, not `ROUTE_EVERYTHING`. Kernel governs, doesn't transport.

### Why hybrid + registry?

- Stateless protocol removes session-management burden
- arifOS already has identity (SCT), authorization, receipts (VAULT999), floor enforcement
- Organs stay autonomous (no bottleneck)
- Registry provides discovery without routing overhead

Key framing: **"Stateless MCP removes transport memory, not institutional memory."**

## Migration Tasks (Phase 0 — common prerequisite)

### 1. Python SDK stateless verification (GEOX/WEALTH/WELL)

Check if FastMCP 3.4.5/3.4.6 supports stateless:
```bash
grep -r "stateless\|Mcp-Session-Id\|session_id" /root/{GEOX,WEALTH,WELL}/src/
```

If upgrade needed: bump pyproject.toml, test locally before deploy.

### 2. A-FORGE port collapse

Read `src/interfaces/server.ts` + `src/interfaces/mcp/`, mount MCP as Express routes on :7071, fix binding, update Caddyfile, remove `a-forge-mcp-test.service`. Estimated: 5-7 days, medium risk.

### 3. Registry manifest creation

Aggregate tool catalogs from arifOS `/tools.json`, GEOX `/tools.json`, WEALTH/WELL `.well-known/mcp/server.json`, A-FORGE `src/interfaces/mcp/forgeTools.ts`. Output: `/root/forge_work/phase0-registry-manifest.yaml`. Estimated: 2-3 days, low risk.

## Pitfalls

- **A-FORGE :7072 binding is the immediate bug.** Fix before any stateless migration.
- **FastMCP version drift** (3.4.2 → 3.4.5/3.4.6) happened silently. Always probe live.
- **Caddy routes to :7072 will fail** until binding fixed.
- **arifOS already stateless** — don't waste time "upgrading" it.
- **5 subdomains = governance surface multiplication.** Stateless MCP makes this WORSE, not better (no protocol session boundary).
