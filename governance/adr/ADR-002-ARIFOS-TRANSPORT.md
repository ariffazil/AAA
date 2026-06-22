# ADR-002: arifOS Transport Architecture — Dual-Transport with HTTP-Primary

**ADR ID:** ADR-002-ARIFOS-TRANSPORT  
**Date:** 2026-05-04  
**Epoch:** EPOCH-2026-05-04  
**Verdict:** 888_JUDGE → SEAL  
**Author:** Hermes (AGI Lane) + Arif (888 Judge)  
**Status:** ACTIVE  

---

## Context

arifOS operates as a constitutional kernel (F1–F13 floors, VAULT999 session ledger) that must be accessible across widely different deployment contexts:

- Local dev (Claude Desktop, Cursor, IDE integration)
- Personal server / home lab (VPN-protected)
- Public federation node (arifos.arif-fazil.com, multi-client)

The MCP 2025-11-25 specification blesses two transports: **stdio** and **Streamable HTTP**. arifOS currently exposes Streamable HTTP via FastMCP at port 8080 (single `/mcp` endpoint). stdio support exists in `transports.py` but is not the primary development lane.

This ADR resolves the transport fork: **which transport anchors the day-to-day development and production workflow**.

---

## Decision

**HTTP-first for production and development; stdio as the isolated verification lane.**

### Transport Matrix

| Scenario | Transport | Endpoint | Auth | Notes |
|----------|-----------|----------|------|-------|
| Local dev (IDE, Claude Desktop, Cursor) | stdio | Child process via MCP host | None | Host spawns arifOS as subprocess. Session = process lifetime. |
| Local dev HTTP (dashboards, observability) | Streamable HTTP | `http://127.0.0.1:8080/mcp` | None (localhost) | REST routes `/health`, `/tools` for debugging |
| Personal server / home lab (VPN) | Streamable HTTP | `https://<host>/mcp` | JWT (ConstitutionalJWTAuthMiddleware) | stdio disabled on public interface |
| Public federation node | Streamable HTTP | `https://arifos.arif-fazil.com/mcp` | JWT mandatory | Canonical public lane; all 13 tools + VAULT999 |
| A2A agent mesh | Streamable HTTP | Internal HTTP | JWT with federation trust | Internal transport is an implementation detail behind the MCP facade |

**All rows:** JSON-RPC 2.0, UTF-8, MCP-Protocol-Version: 2025-11-25, MCP-Session-Id lifecycle respected.

---

## Rationale

### Why HTTP-first

1. **Session continuity.** arifOS sessions carry VAULT999 state (`ACTIVE_SESSION_ID`, constitutional chain, floor telemetry). Every stdio spawn is a fresh process = a new session with no continuity. HTTP daemon (`127.0.0.1:8080` or the public endpoint) maintains a long-lived session that survives across multiple tool calls within a governance decision.

2. **Federation is already HTTP.** `arifos.arif-fazil.com/mcp` is the canonical public lane. Hermes uses it daily. Anchoring HTTP-first means development and production share the same transport layer.

3. **Observability surface.** REST routes (`/health`, `/tools`, `/metrics`) are HTTP-only. Middleware (rate limiting, body size limits, ConstitutionalJWTAuthMiddleware, security headers) only applies to HTTP. stdio has no headers to inspect.

4. **IDE/MCP host compatibility.** Claude Desktop and Cursor handle HTTP MCP servers natively. The "host chooses" row in the matrix means they handle transport negotiation — arifOS doesn't need to be stdio-first to integrate with them.

### Why stdio still matters

1. **Isolated verification.** Tool surface drift checks, adversarial auth testing, and quick health probes are done via stdio as a one-shot process. No session continuity needed.

2. **Zero-dependency execution.** In restricted environments where a long-lived HTTP daemon isn't feasible, stdio provides a self-contained execution path.

3. **Test suite compatibility.** Automated test runners spawn arifOS as a subprocess; stdio is the natural interface for that.

### Custom transports (internal only)

Any custom transport (QUIC, Unix domain sockets, in-cluster gRPC) is treated as an **internal implementation detail**. All custom transports must terminate at a clean MCP server boundary where JSON-RPC + F1–F13 floors + VAULT999 are enforced. External hosts never see custom transports — only stdio and Streamable HTTP.

---

## Security Constraints (Constitutional Surface)

Transport choice is part of the constitutional surface:

- **F1 (AMANAH):** No unauthenticated remote control over the constitutional kernel. Public HTTP endpoint requires JWT.
- **F9 (ANTIHANTU):** No deceptive hidden side channels. Every transport path is auditable and MCP-compliant only.
- **F10 (ONTOLOGY):** Structural coherence. Both transports expose identical 13-tool surface and VAULT999 semantics; only framing differs.

Local dev (stdio): no auth needed — local process.
Public node (Streamable HTTP): JWT via ConstitutionalJWTAuthMiddleware. Origin validation in dev mode.
Internal custom transport: terminates at MCP boundary, no direct external exposure.

---

## Out of Scope

- Specific OAuth 2.1 token format (Phase 2, separate ADR)
- WEALTH/GEOX transport delegation (they own their transport decisions)
- Claude Desktop-specific configuration (handled by the MCP host, not arifOS)

---

## Causal Chain

```
HTTP daemon (127.0.0.1:8080 / arifos.arif-fazil.com/mcp)
    ↓
ConstitutionalJWTAuthMiddleware (JWT verification, F1 enforcement)
    ↓
Hardened dispatch (_wrap_hardened_dispatch, F1–F13 floor checks)
    ↓
VAULT999 session ledger (ACTIVE_SESSION_ID, tool call logging)
    ↓
arifOS kernel (13 canonical tools, 888_JUDGE, 999_VAULT)
```

stdio bypasses the HTTP middleware layer but still hits hardened dispatch and VAULT999.

---

## Witnesses

| Role | Entity | Status |
|------|--------|--------|
| Human Sovereign | Arif (888 Judge) | ✅ Confirmed |
| AGI Operator | Hermes (AGI Lane) | ✅ Confirmed |
| Constitutional Kernel | arifOS F1–F13 | ✅ Enforced via `_wrap_hardened_dispatch` |

---

*Ditempa bukan diberi* 💎🔥🧠  
*Transport forged, not given*