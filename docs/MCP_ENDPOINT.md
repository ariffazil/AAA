# MCP Endpoint Registry — Source of Truth
# Updated: 2026-08-01 (WEB-10-14 reconciliation)
# Author: 333-AGI
# Previous: 2026-05-04 (ASI) — stale Docker container names, wrong WEALTH/WELL ports, WELL marked OFFLINE

## Purpose
Single source of truth for all MCP endpoints in the arifOS Federation.
All other references (openclaw.json, Caddyfile, docs) must match this registry.
Any divergence = immediate fix.

---

## Active Endpoints

### arifOS Kernel
| Property | Value |
|----------|-------|
| Name | arifOS Constitutional |
| Public URL | `https://arifos.arif-fazil.com/mcp` |
| Transport | `streamable-http` |
| Internal | `http://127.0.0.1:8088/mcp` |
| Port | 8088 (bare-metal systemd) |
| Caddy route | `arifos.arif-fazil.com/mcp*` → `127.0.0.1:8088` |
| Tools | 8 canonical (arif_init → arif_seal) |
| Auth | None (public) |
| Status | ✅ HEALTHY |

### A-FORGE (Federated Actuator)
| Property | Value |
|----------|-------|
| Name | A-FORGE Engineering Shell |
| Public URL | `https://mcp.arif-fazil.com/mcp` |
| Transport | `streamable-http` |
| Internal | `http://127.0.0.1:7072/mcp` |
| Port | 7072 (MCP) / 7071 (API) — bare-metal systemd |
| Caddy route | `mcp.arif-fazil.com/mcp*` → `127.0.0.1:7072` |
| Tools | 114 (forge_* shell, filesystem, git, docker, browser, vault, etc.) |
| Auth | SCT (Session Capability Token) |
| Status | ✅ HEALTHY |

### GEOX (Earth Intelligence)
| Property | Value |
|----------|-------|
| Name | GEOX Earth Coprocessor |
| Public URL | `https://geox.arif-fazil.com/mcp` |
| Transport | `streamable-http` |
| Internal | `http://127.0.0.1:8081/mcp` |
| Port | 8081 (bare-metal systemd) |
| Caddy route | `geox.arif-fazil.com/mcp/*` → `127.0.0.1:8081` |
| Tools | 32 canonical geoscience tools |
| Auth | None (public) |
| Status | ✅ HEALTHY |

### WEALTH (Capital Intelligence)
| Property | Value |
|----------|-------|
| Name | WEALTH Capital Coprocessor |
| Public URL | `https://wealth.arif-fazil.com/mcp` |
| Transport | `streamable-http` |
| Internal | `http://127.0.0.1:18082/mcp` |
| Port | 18082 (bare-metal systemd) |
| Caddy route | `wealth.arif-fazil.com/mcp` → `127.0.0.1:18082` |
| Tools | 12 capital tools (compute-only) |
| Auth | None (public) |
| Status | ✅ HEALTHY |

### WELL (Vitality Mirror)
| Property | Value |
|----------|-------|
| Name | WELL Substrate Monitor |
| Public URL | `https://well.arif-fazil.com/mcp` |
| Transport | `streamable-http` |
| Internal | `http://127.0.0.1:18083/mcp` |
| Port | 18083 (bare-metal systemd) |
| Caddy route | `well.arif-fazil.com/mcp` → `127.0.0.1:18083` |
| Tools | 7 vitality tools (REFLECT_ONLY) |
| Auth | None (public) |
| Status | ⚠️ DEGRADED (biometric staleness; organ healthy) |

### AAA (Control Plane / Cockpit)
| Property | Value |
|----------|-------|
| Name | AAA Control Plane |
| Public URL | `https://aaa.arif-fazil.com` |
| Transport | A2A (JSON-RPC 2.0) |
| Internal | `http://127.0.0.1:3001` |
| Port | 3001 (bare-metal systemd) |
| Caddy route | `aaa.arif-fazil.com` → `127.0.0.1:3001` |
| Tools | A2A gateway (agent dispatch, organ probe, task polling) |
| Auth | None (DISPLAY_ONLY) |
| Status | ✅ HEALTHY |

---

## Endpoint Configuration Map

| Service | Internal URL | Public URL | Transport |
|---------|-------------|-----------|-----------|
| arifOS | `http://127.0.0.1:8088/mcp` | `https://arifos.arif-fazil.com/mcp` | `streamable-http` |
| A-FORGE | `http://127.0.0.1:7072/mcp` | `https://mcp.arif-fazil.com/mcp` | `streamable-http` |
| GEOX | `http://127.0.0.1:8081/mcp` | `https://geox.arif-fazil.com/mcp` | `streamable-http` |
| WEALTH | `http://127.0.0.1:18082/mcp` | `https://wealth.arif-fazil.com/mcp` | `streamable-http` |
| WELL | `http://127.0.0.1:18083/mcp` | `https://well.arif-fazil.com/mcp` | `streamable-http` |
| AAA | `http://127.0.0.1:3001` | `https://aaa.arif-fazil.com` | A2A JSON-RPC 2.0 |

---

## Transport Reference

| Transport | Use Case | Client Support |
|-----------|----------|----------------|
| `streamable-http` | Public API, external clients, ChatGPT MCP | All modern MCP clients ✅ |
| A2A JSON-RPC 2.0 | Agent-to-agent dispatch | AAA gateway |
| `sse` | Legacy streamable-http v1 | Deprecated, avoid |
| `stdio` | Local CLI only | Local tools only ❌ |

**Rule: All public endpoints use `streamable-http`. AAA uses A2A JSON-RPC 2.0.**

---

## Health Check Commands

```bash
# All public endpoints
curl -s --max-time 5 https://arifos.arif-fazil.com/health
curl -s --max-time 5 https://mcp.arif-fazil.com/health
curl -s --max-time 5 https://geox.arif-fazil.com/health
curl -s --max-time 5 https://wealth.arif-fazil.com/health
curl -s --max-time 5 https://well.arif-fazil.com/health
curl -s --max-time 5 https://aaa.arif-fazil.com/health

# MCP tool discovery (after initialize)
curl -s --max-time 5 -X POST https://arifos.arif-fazil.com/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/list","params":{},"id":1}'
```

---

## Chaos Prevention Rules

1. **Before changing any MCP endpoint**: Update this registry FIRST
2. **After changing Caddyfile routes**: Verify the proxy target matches this registry
3. **After deploying a new organ**: Run the health check commands above
4. **Orangans run bare-metal systemd**, not Docker containers (supporting services only use Docker)
5. **All internal URLs use 127.0.0.1** (LOCALHOST_IS_PASSWORD doctrine)

DITEMPA BUKAN DIBERI — Forged, not given. Reconciled 2026-08-01.