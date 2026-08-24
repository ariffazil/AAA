---
id: MY-REALITY-STACK
name: Malaysia Reality Stack — Primary-Source Routing
version: 1.0.0-2026.08.15
description: Route all Malaysia macro/policy/energy/corporate claims through primary government/financial sources using EXISTING federation tools. NO new MCP servers. Hard F2 provenance law for any MY figure.
owner: F13 SOVEREIGN (directive 2026-08-15, external proposal adapted)
risk_tier: low
floor_scope: [F2, F7, F9, F10]
autonomy_tier: T0
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# MY-REALITY-STACK — Malaysia Reality Routing

> **DITEMPA BUKAN DIBERI.** Agents speak of Malaysia only through her own ledgers.
> Public registry: https://arif-fazil.com/world/malaysia/reality-stack/

## THE LAW (non-bypassable)

1. **NO NEW MCP SERVERS.** The external proposal (bnm-mcp, parlimen-mcp) is implemented as THIS SKILL + existing organs, not as new servers. Federation rule: modes on existing tools, not new registrations.
2. **F2 PROVENANCE — THE HARD RULE:** No Malaysia macro figure (OPR, CPI, GDP, FX reserve, energy demand, water level, corporate capex) may be stated without a payload tag from a primary source below, fetched THIS session. Unverifiable → say UNKNOWN, cite nothing.
3. **VECTOR MEMORY:** memory geometry is mathematical — `vector_memory` (embeddings, cosine distance), never biological metaphors. Aligned with F9/F10 anti-anthropomorphism.

## ROUTING TABLE (tool → use)

| Need | Tool (existing) | Pattern |
|---|---|---|
| JSON endpoint pull | `forge_fetch` (mode=json) or `arif_observe(mode=fetch)` | Direct GET, cache TTL default |
| Blocked-from-VPS host (000/403) | SearXNG (`forge_fetch` query=) or browser (`forge_browser_navigate`) | parlimen.gov.my, hanpar, bursa, bernama block DC IPs — route via search cache or browser render |
| Recurring structured pull | `forge_ephemeral` (generate → invoke → retire) | Temporary tool, dissolves after mission — NOT a new server |
| News validation | `hermes_fact_check` / `arif_observe(mode=search)` | Wire claim → primary source cross-check before memory write |
| Figures into reasoning | `arif_think` after payload in context | Hooded-engine rule: no payload in window = no capability |

## PRIMARY SOURCES (probed 2026-08-15, from VPS)

### 1 · Fiscal / Macro / Financial
- **BNM Open API** `https://api.bnm.gov.my` — OPR, base rates, FX, interbank, gov bond, consumer alerts; KijangAPI gold at `/v2/kijang`. Requires registered `app` header token. Domain LIVE but 404s unauthenticated/DC-IP — register token, or route via search.
- **BNM portal** `https://www.bnm.gov.my` — 200 OK. Statements, MCPM minutes, FX policy.
- **OpenDOSM** `https://open.dosm.gov.my` — 200 OK. Official statistics dashboard (CPI, labour force, trade).
- **DOSM data lake** `https://storage.dosm.gov.my` — 200 OK. Dataset JSON/CSV releases.
- **data.gov.my** `https://data.gov.my` — CKAN paths currently 404 (post-migration drift) — use OpenDOSM until stable.

### 2 · Legislative
- **Hansard** `https://hanpar.parlimen.gov.my` + `https://www.parlimen.gov.my` — 000 from VPS (geo-block). Route via SearXNG/browser. Written answers (jawapan bertulis) = minister-level primary record.
- **LOM (AGC)** `https://lom.agc.gov.my` — 200 OK. Acts, amendments. Federal Gazette via AGC portal.

### 3 · Energy / Water / Earth
- **Suruhanjaya Tenaga** `https://www.st.gov.my` — 200 OK. Grid data, MSO (Malaysia Energy Statistics Outlook), coal retirement schedule, commission rulings.
- **JPS/DID flood+river telemetry** `https://publicinfobanjir.water.gov.my` — 200 OK. Live river level/rainfall stations (Johor basin cases).
- **JPS hydrology portal** `https://hydrology.water.gov.my` — 000 from VPS; use publicinfobanjir mirror.
- **PETRONAS/MPM** — NO public API (INT). Production/reserves: PTG annual reports (PDF via st/bnm-style fetch) + EIA international for cross-check. Never fabricate well/block names — GEOX `geox_basin` for geometry ground-truth.
- **GEOX organ** — all geometry claims (basin boundaries, block coords, well inventory) route through GEOX MCP, not memory.

### 4 · Corporate
- **Bursa announcements** `https://www.bursamalaysia.com` — 403 bot-wall from VPS; browser-render or SearXNG cache. Announcements = capex/equity/board primary record.
- **SSM** `https://www.ssm.com.my` — 302 alive; UBO lookups are PAID (e-info account). Flag as gated; never infer ownership without document.

### 5 · News Wires (secondary until primary-anchored)
- The Edge `https://www.theedgemarkets.com` (301→200), Malaysiakini RSS `https://www.malaysikini.com/rss/` (301), Bernama RSS path currently unreachable from VPS — use site search. **Wire text = INT until anchored to a §1–§4 payload.**

## ANTI-HALLUCINATION CONTRACT

- Sandakan-class well-name errors → GEOX ground-truth or UNKNOWN.
- Macro figure without payload → UNKNOWN + "fetch first via MY-REALITY-STACK".
- News claim without wire provenance → not eligible for memory write (any tier).
