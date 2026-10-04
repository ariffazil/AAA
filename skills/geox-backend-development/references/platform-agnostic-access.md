# Platform-Agnostic GEOX Access Pattern

> Session: 2026-08-10 | Origin: Arif's eureka — "auto-mint ANON-xxx, zero config, works everywhere"

## The Problem

External AI platforms (ChatGPT, Cursor, Claude) can only connect to GEOX MCP — they have no arifOS, no SCT tokens, no session minting. Before this pattern, they got `SESSION_INVALID` and could never call a tool.

## The Solution: Auto-Mint + 3-Tier Classification

### Auto-Mint (GEOX-local, zero arifOS dependency)

When no session_id is present or the session is empty:
1. GEOX generates `ANON-{uuid.uuid4().hex[:16]}`
2. Returns it in the response envelope
3. Caller echoes it back for continuity
4. No cross-server dependency

### 3-Tier Classification (by what the call TOUCHES)

| Tier | What it touches | Tools | Gate |
|------|----------------|-------|------|
| **Anon** | Pure functions, caller inputs | geox_temporal, geox_source, geox_seismic_compute, geox_geomechanics, geox_basin, geox_deep_time, geox_map, geox_spatial, geox_model, geox_prospect | None (rate-limited) |
| **Session** | Server-held artifacts | geox_workspace, geox_well, geox_well_qc, geox_petrophysics, geox_seismic_interpret | Continuity (ANON-xxx) |
| **Verified** | Ingest, mutations, seal | geox_well_ingest, geox_claim (seal), geox_seismic_ingest | SCT required (arifOS) |

### Rate Limiting

| Tier | Max calls/min |
|------|---------------|
| Anon | 30 |
| Session | 100 |
| Verified | unlimited (999) |

### Provenance Stamps

Every guest output must include:
```json
{
  "actor_verified": false,
  "authority": "ADVISORY",
  "guest_output": true,
  "caveat": "Guest output must never be mistaken for evidence"
}
```

## Implementation Files

| File | Purpose |
|------|---------|
| `src/geox_mcp/session_enforcement.py` | PATH 4: auto-mint for empty/ANON-xxx sessions |
| `src/geox_mcp/tool_tiers.py` | 3-tier classification |
| `src/geox_mcp/rate_limiter.py` | Per-session sliding window |
| `src/geox_mcp/geox_middleware.py` | HTTP-level auto-mint injection |

## FastMCP Transport Constraint

FastMCP's HTTP transport resolves `Mcp-Session-Id` **before** the middleware chain runs. A truly headerless `tools/call` gets HTTP 400 from FastMCP before `on_call_tool` fires.

**The MCP protocol requires a session header.** The standard flow (initialize → get SID → use it) is the only supported client path. Auto-mint happens inside the middleware when the SID is present but GEOX doesn't recognize it (e.g., FastMCP raw hex).

## Acceptance Test

```
Call GEOX from a client with ONLY GEOX connected and nothing else.
If a decline curve comes back with no prior handshake, it's agnostic.
That's the acceptance gate.
```

## Arif's Architectural Admissions

1. **Software cannot generate physical authority** — the root of trust is out-of-band
2. **Latency is physical reality** — deferred decisions queue intents, don't fake seals
3. **Lanes process; the kernel routes** — lanes never talk directly, communication goes through arifOS

These admissions mean:
- Anon + Session tiers = GEOX-local (platform-agnostic)
- Verified tier = requires arifOS (federation trust)
- The coupling is intentional and correct
