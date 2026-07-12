# P2P READINESS — Federation Organs (Audit 2026-07-12)

> **Purpose:** For each organ, evaluate readiness to serve its own `/.well-known/agent-card.json` and accept A2A JSON-RPC calls directly (peer-to-peer), without the AAA gateway as a relay.
>
> **Audit scope:** arifOS, A-FORGE, GEOX, WEALTH, WELL, AAA.
> **Authority:** F8 LAW (system boundary), F13 SOVEREIGN.
> **P2P path:** A2A CIV-33 — sibling P2P uses the same JSON-RPC verbs (`message/send`, `tasks/get`, `tasks/cancel`) that AAA proxies today.

---

## Summary Matrix

| Organ   | Port  | `.well-known/agent-card.json` | A2A verbs (JSON-RPC) | TLS-ready | p2p_ready | Blockers |
|---------|-------|------------------------------|----------------------|-----------|-----------|----------|
| arifOS  | 8088  | ✅ 200                       | ❌ 404               | via Caddy 443 | partial | JSON-RPC verbs not exposed |
| A-FORGE | 7071  | ❌ **404**                   | ❌ 404               | via Caddy 443 | **not p2p** | **No `/.well-known` route; no A2A endpoint** |
| GEOX    | 8081  | ✅ 200                       | ❌ 404               | via Caddy 443 | partial | JSON-RPC verbs not exposed |
| WEALTH  | 18082 | ✅ 200                       | ❌ 404               | via Caddy 443 | partial | JSON-RPC verbs not exposed |
| WELL    | 18083 | ✅ 200                       | ❌ 404               | via Caddy 443 | partial | JSON-RPC verbs not exposed |
| AAA     | 3001  | ✅ 200                       | ✅ 400 (active, expects body) | via Caddy 443 | ✅ p2p-ready | None for A2A; gateway tier |

> **Key finding:** All organs except AAA lack a JSON-RPC endpoint for `tasks/send` / `tasks/get` / `tasks/cancel`. A-FORGE additionally has no static `/.well-known` route. To make every organ a first-class P2P peer, the organs behind Caddy need:
> 1. A `/.well-known/agent-card.json` route (or static file).
> 2. A JSON-RPC endpoint at `/a2a` (or `/rpc`) accepting the A2A verbs.
> 3. Bearer-token / API-key middleware (currently optional since "localhost IS the password" — but required for any external peer).
>
> Until those land, **AAA remains the single P2P ingress** for the federation, and other organs are MCP-only resources reachable through AAA routing.

---

## Per-Organ Detail

### arifOS — port 8088
- **HTTP server:** `python` (PID 331701), bound to 127.0.0.1 only.
- **`/.well-known/agent-card.json`:** ✅ 200 — serves the constitutional kernel agent card with `P/T/V/G/E/M` axis skills.
- **A2A-Version header:** server emits A2A-Version-aware responses (A2A/1.0 declared in card).
- **Auth:** JWT bearer (arifOS session token) for irreversible verbs; OPERATOR_API_TOKEN for human-expert endpoints.
- **TLS:** Behind Cloudflare + Caddy (https://arifos.arif-fazil.com). Plain HTTP at 8088.
- **JSON-RPC verbs:** ❌ 404 — no `tasks/send`, `tasks/get`, `tasks/cancel` endpoint at `/a2a/*`. Today, arifOS is reachable via MCP only (8 canonical tools).
- **p2p_ready:** **partial** (card present, but A2A verbs not exposed).
- **Blockers:**
  - [`A-FORGE MEDIUM`] Expose JSON-RPC verbs (`message/send`, `tasks/send`, `tasks/get`, `tasks/cancel`) at `/a2a`. Suggest `/a2a/rpc` or mount A2A-grammar on top of MCP `tools/call` calls with `tool_name=arif_route` etc.
  - Expose `/.well-known/agent-card.json` through the public hostname (Caddy already proxies it).

### A-FORGE — port 7071
- **HTTP server:** `node` (PID 3026438), bound to 127.0.0.1 only.
- **`/.well-known/agent-card.json`:** ❌ **404** — A-FORGE does NOT currently serve a static agent card (this audit created one in `agent-cards/organs/aforge/agent-card.json`, but the live service doesn't expose it).
- **MCP endpoint:** `/mcp` returns 200 with 102 tools. JSON-RPC initialize works.
- **Auth:** `bearer_auth` and `api_key` declared in card. MUTATE verbs require session+lease+seal from arifOS.
- **TLS:** Behind Cloudflare + Caddy (https://a-forge.arif-fazil.com).
- **JSON-RPC verbs:** ❌ 404.
- **p2p_ready:** **false**.
- **Blockers:**
  - [`A-FORGE HIGH`] Add `/.well-known/agent-card.json` route — serve file from `/root/AAA/agent-cards/organs/aforge/agent-card.json`.
  - [`A-FORGE HIGH`] Add JSON-RPC verbs at `/a2a/rpc`.
  - [`A-FORGE MEDIUM`] Document session+lease+seal handshake in `card.security.leaseRequired`.

### GEOX — port 8081
- **HTTP server:** `python3` (PID 3738139), bound to 127.0.0.1 only.
- **`/.well-known/agent-card.json`:** ✅ 200 — the live service returns a slim card with `owned_mcp` array (31 tools). This audit replaces it with the richer skill-clustered `agent-cards/organs/geox/agent-card.json`.
- **MCP endpoint:** `/mcp` returns 200 with 31 tools.
- **Auth:** JWT bearer (arifOS session) declared. allow_anonymous=true today for localhost.
- **TLS:** Behind Cloudflare + Caddy (https://geox.arif-fazil.com).
- **JSON-RPC verbs:** ❌ 404.
- **p2p_ready:** **partial**.
- **Blockers:**
  - [`A-FORGE MEDIUM`] Same as arifOS — expose A2A JSON-RPC at `/a2a`.
  - [`GEOX LOW`] Update live service to serve the newly-aligned `agent-cards/organs/geox/agent-card.json`.

### WEALTH — port 18082
- **HTTP server:** `python3` (PID 3741378), bound to 127.0.0.1 only.
- **`/.well-known/agent-card.json`:** ✅ 200 — live card uses dotted skill ids (`capital.thermodynamics`, `institutional.resilience`, `wisdom.evaluate`). Audit-aligned card uses hyphen-cased skills (`capital-math`, `institutional-resilience`).
- **MCP endpoint:** `/mcp` returns 200 with 12 tools.
- **Auth:** bearer_auth + api_key declared. computeOnly=true — WEALTH cannot authorize execution.
- **TLS:** Behind Cloudflare + Caddy (https://wealth.arif-fazil.com).
- **JSON-RPC verbs:** ❌ 404.
- **p2p_ready:** **partial**.
- **Blockers:**
  - JSON-RPC verbs at `/a2a` (medium priority — same blocker pattern as arifOS/GEOX).
  - Live service should serve the audit-aligned card.

### WELL — port 18083
- **HTTP server:** `python3` (PID 4012645), bound to 127.0.0.1 only.
- **`/.well-known/agent-card.json`:** ✅ 200 — live card uses bare schema (`schema: agent-manifest/v1`), and a non-versioned `owned_mcp.tool_count: 18` (stale — actual count is 29). Audit-aligned card has 4 skill clusters and full tool coverage.
- **MCP endpoint:** `/mcp` returns 200 with 29 tools.
- **Auth:** bearer_auth + api_key declared. reflect_only=true.
- **TLS:** Behind Cloudflare + Caddy (https://well.arif-fazil.com).
- **JSON-RPC verbs:** ❌ 404.
- **p2p_ready:** **partial**.
- **Blockers:**
  - JSON-RPC verbs at `/a2a` (medium).
  - Refresh live `/.well-known` to audit-aligned card (low — informational drift only).
  - Note: WELL is F13 sovereign territory — JSON-RPC verbs should be **read-only**.

### AAA — port 3001
- **HTTP server:** `node` (PID 923358), bound to 127.0.0.1 only.
- **`/.well-known/agent-card.json`:** ✅ 200 — gateway card with `federation_organs[]` aggregator.
- **`/a2a/discover`:** ✅ returns 41 agents in registry (registry is gateway's first-class job).
- **JSON-RPC verbs:** ✅ 400 — endpoint accepts `message/send`, `tasks/send`, `tasks/get`, `tasks/cancel` (4xx indicates body validation, not 404 — endpoint present and active).
- **Auth:** OAuth 2.1 + bearer_auth; SSO via `/oauth/authorize` & `/oauth/token`.
- **TLS:** Behind Cloudflare + Caddy (https://aaa.arif-fazil.com).
- **p2p_ready:** **true** for A2A traffic; tier-1 of the federation.
- **Blockers:** None for A2A. (Gateway tier.)

---

## P2P Requirements Checklist

For each organ to be a first-class A2A peer (CIV-33 P2P path), it must provide:

- [ ] **Static or route `/.well-known/agent-card.json`** (Ed25519-signed card aligned to live MCP surface).
- [ ] **`A2A-Version: 1.0` header handling** in responses.
- [ ] **Bearer token auth** — same JWT scheme issued by `arif_init` (000-SALAM handshake).
- [ ] **JSON-RPC 2.0 endpoint** at `/a2a` or `/a2a/rpc` accepting:
  - `message/send`
  - `tasks/send`
  - `tasks/get`
  - `tasks/cancel`
- [ ] **TLS** (when externally exposed) via Caddy + Cloudflare; localhost can stay plain HTTP per ADR-001.
- [ ] **A2A skill registry** with `id`, `name`, `description`, `tags`, `examples`, `inputModes`, `outputModes` (each skill must include `tools[]` mapping to MCP tool names).

---

## Recommended Roll-Out

1. **Phase A — Static card exposure (low cost):** add `/.well-known/agent-card.json` route on every organ (currently only A-FORGE missing). Mount the JSON file in the running container or proxy it from `/root/AAA/agent-cards/organs/<organ>/agent-card.json`. Already-done at the file level for all 6 organs.
2. **Phase B — JSON-RPC verbs (medium cost):** add A2A verbs at `/a2a` for GEOX, WEALTH, WELL, arifOS. Each verb's transport body maps to internal MCP `tools/call` calls.
3. **Phase C — Auth layering (medium cost):** flip `authRequired: true` on every organ's static card so JSON-RPC rejects unsigned calls; rely on the `bearer_auth` middleware.
4. **Phase D — TLS upgrade (already done at edge):** Caddy + Cloudflare already terminate TLS. Edge plain HTTP behind it is fine per ADR-001 ("localhost IS the password"); only worry if peer is *not* in this federation.

> After Phase A + B + C, every organ is a peer. AAA remains the gateway for **discovery** (`/a2a/discover`), but the verbs themselves can be served by any organ.

---

## Verification

| Check | Status |
|-------|--------|
| All 6 organ `agent-card.json` files written and Ed25519-signed | ✅ |
| All 6 cards `signatures[*].proofValue` is 64-byte Ed25519 round-trip-verifiable | ✅ |
| Card `protocolVersion` is `1.2` for all organs | ✅ |
| Inventory snapshot saved to `agent-cards/organs/_audit_2026_07_12/inventory.json` | ✅ |
| Live MCP `tools/list` matches card `skills[].tools[]` for every organ | ✅ (8, 102, 31, 12, 29, 41) |

---
*Audit by Kimi Code CLI — 2026-07-12 23:24 UTC*
*DITEMPA BUKAN DIBERI — Forged, Not Given.*
