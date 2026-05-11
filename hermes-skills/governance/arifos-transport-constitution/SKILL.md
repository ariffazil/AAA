---
name: arifos-transport-constitution
description: Canonical transport stance for arifOS MCP — ONE public lane, stdio for verification only. Activates when anyone asks about MCP transport, SSE, streamable-http, or local dev surfaces.
category: governance
---

# arifOS Transport Constitution (v2026.05.04)

> DITEMPA BUKAN DIBERI — Forged, Not Given

## Canonical Transport Stance

arifOS has ONE public lane. Everything else is verification.

### Lane 1 — Public Federation (THE ONLY LANE)
- **URL:** `https://arifos.arif-fazil.com/mcp`
- **Transport:** `streamable-http` (FastMCP, stateless HTTP)
- **Auth:** ConstitutionalJWTAuthMiddleware wired (permissive — logs violations, does not block unauthenticated calls yet)
- **Streaming:** HTTP chunked transfer encoding (NOT SSE)
- **This is what you use. Every time.**

### Lane 2 — Stdio Verification (FOR SUBAGENTS / AUTOMATION)
- **Transport:** `stdio`
- **Use:** cold-start health probes, surface drift checks, test harnesses
- **Continuity:** NONE — each run is isolated, stateless
- **For subagents only, not human workflow**

### Lane 3 — SSE (LEGACY / DEPRECATED)
- Only for old MCP clients that can't do streamable-http
- arifOS sovereign `/sse` endpoint reserved for oversight signals, NOT the MCP channel
- Not the canonical channel

### Binding Override Rule
- `ARIFOS_HOST=0.0.0.0` only when Caddy/reverse-proxy is in front
- Production: container behind Caddy, so `0.0.0.0` is fine
- Any future standalone dev: default to `127.0.0.1`

## What arifOS IS NOT
- NOT a local dev server
- NOT something you run on laptop
- NOT a desktop app

arifOS = VPS-hosted constitutional kernel, accessed via web link only.

## Session Behavior
- Current: `stateless_http=True` — no MCP-Session-Id, no session continuity
- Each HTTP request is self-contained
- stdio runs always cold-start, zero continuity

## Re-evaluate If
- MCP spec mandates mandatory session resumption
- arifOS adds stateful session mode
- Federation scale requires HTTP/2+ or QUIC
