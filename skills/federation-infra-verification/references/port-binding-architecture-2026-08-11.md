# Federation Port Binding Architecture (2026-08-11)

## arifOS — Single-Port Elegance (:8088)

arifOS uses **one port for everything**: internal REST + MCP Streamable-HTTP.
One Python process (`arifosmcp.runtime`) serves both interfaces simultaneously.

```
                    ┌──────────────────────────────┐
                    │     arifOS KERNEL (:8088)    │
                    │     binds 127.0.0.1:8088     │
                    └──────────┬───────────────────┘
                               │
              ┌────────────────┼────────────────────┐
              │                │                    │
     LOCAL (organs)    arifos.arif-fazil    mcp.arif-fazil
     127.0.0.1:8088    .com (observatory)   .com (MCP door)
     GEOX, WEALTH,     Caddy → 8088         Caddy → 8088
     WELL, arifFlow
     Hermes, OpenClaw
```

**Why single-port works:** MCP protocol and internal REST share the same Python
process. The `/mcp*` route handles Streamable-HTTP; everything else is REST/JSON.
Caddy handles TLS termination and domain routing — the kernel doesn't care which
domain arrived, it just serves.

## A-FORGE — Dual-Port Legacy (:7071 + :7072)

| Port | Role | Binding | Protocol | Status |
|------|------|---------|----------|--------|
| 7071 | Internal RPC (forge_shell, forge_fetch) | `127.0.0.1` ✅ | REST/JSON (Node.js) | Healthy |
| 7072 | MCP Streamable-HTTP (tool discovery) | `100.64.0.2` (Tailscale ONLY) ❌ | MCP | Unreachable from localhost |

**The bug:** `:7072` only binds Tailscale IP `100.64.0.2`, not `127.0.0.1`.
Caddy routes that need `reverse_proxy 127.0.0.1:7072` silently fail. Health
probes on `localhost:7072` also fail. This is why `doctor.sh` shows A-FORGE as
❌ even though the `:7071` service is healthy and `:7072` node process is running.

**Why two ports exist:**
- MCP protocol has sentinel gate, content boundaries, two-context defense — layers not present in internal RPC
- Internal RPC can call `forge_execute` direct without MCP overhead
- External agents shouldn't see internal surface — only MCP-governed tools
- **Entropy cost:** two ports = two health probes, two binding configs, two places to fail

**Possible fixes (ranked by reversibility):**
1. Bind `:7072` to `127.0.0.1` in addition to Tailscale (T1, config change + restart)
2. Consolidate to single-port like arifOS (T2, architectural change)
3. Route Caddy through Tailscale IP instead of localhost (T1, Caddy config change — but leaks Tailscale dependency into public routing)

## Complete Organ Port Table

| Organ | Port | Binding | systemd unit | Notes |
|-------|------|---------|-------------|-------|
| arifOS | 8088 | 127.0.0.1 | arifos.service | Single-port: REST + MCP |
| A-FORGE sense | 7071 | 127.0.0.1 | a-forge.service | Internal RPC only |
| A-FORGE MCP | 7072 | 100.64.0.2 | a-forge.service | ⚠️ Tailscale-only bind |
| GEOX | 8081 | 127.0.0.1 | geox-mcp.service | Single-port |
| WEALTH | 18082 | 127.0.0.1 | wealth-organ.service | Single-port |
| WELL | 18083 | 127.0.0.1 | well.service | Single-port (MOCK mode) |
| AAA | 3001 | 127.0.0.1 | aaa-a2a.service | A2A gateway |
| arifFlow | 7073 | 127.0.0.1 | arifflow.service | FQ metabolism |
| FED | 7074 | 127.0.0.1 | (Python process) | Model router advisor |
| FLAME | 18901 | 127.0.0.1 | (Python process) | Free inference mesh |

## Caddy Routing Map (from /etc/caddy/Caddyfile)

```
mcp.arif-fazil.com/mcp                    → 127.0.0.1:8088  (arifOS kernel MCP)
mcp.arif-fazil.com/health                 → 127.0.0.1:8088
mcp.arif-fazil.com/tools                  → 127.0.0.1:8088
mcp.arif-fazil.com/api/organs/geox/*      → 127.0.0.1:8081
mcp.arif-fazil.com/api/organs/wealth/*    → 127.0.0.1:18082
mcp.arif-fazil.com/api/organs/well/*      → 127.0.0.1:18083
mcp.arif-fazil.com/api/organs/aforge/*    → 127.0.0.1:7072  ⚠️ BROKEN (Tailscale bind)
mcp.arif-fazil.com/api/organs/forge/*     → 127.0.0.1:7072  ⚠️ BROKEN (same)
arifos.arif-fazil.com/*                   → 127.0.0.1:8088
arif-fazil.com/health                     → 127.0.0.1:8088
```

**All reverse_proxy directives point to 127.0.0.1** — so any organ that doesn't
bind localhost is unreachable through Caddy regardless of its actual health.

## Diagnostic: "Service healthy but doctor.sh says FAIL"

When a service appears healthy in `systemctl status` and `curl :port/health`
returns OK on one interface but doctor.sh or federation probes show FAIL:

1. `curl -sf http://127.0.0.1:PORT/health` — does localhost reach it?
2. `ss -tlnp | grep :PORT` — what IP is it bound to?
3. Check the binding:
   - `127.0.0.1` → should work from localhost + Caddy ✅
   - `100.64.0.2` → Tailscale-only, localhost unreachable ❌
   - `0.0.0.0` → reachable everywhere (security concern for internal-only)
   - `[::1]` or `[::] ` — IPv6 only, may not match Caddy's `127.0.0.1`
4. If bound correctly but still failing → check if process is actually listening:
   `ss -tlnp | grep :PORT` should show the process name

## The "single-port vs dual-port" consolidation question

arifOS proves single-port works. A-FORGE's dual-port adds:
- 2× health probe complexity
- 2× binding failure modes
- Tailscale dependency leaking into Caddy routing
- Confusion about "is A-FORGE up?" (yes on :7071, broken on :7072)

**Consolidation argument:** federation is mature enough that A-FORGE could adopt
the arifOS pattern — single Node process serving both internal RPC and MCP on
one port, with Caddy handling public/private routing.

**Counter-argument:** MCP sentinel gate and two-context defense are load-bearing
security layers. Merging them onto the same port may weaken the boundary if the
process doesn't enforce it internally.

**Verdict:** fix the Tailscale-only binding first (low-risk T1). Consolidate to
single-port as a planned T2 when there's bandwidth to test MCP sentinel gate on
a unified port.
