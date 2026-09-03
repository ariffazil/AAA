# agent.json Evolution Proposal — DRAFT

> **STATUS:** DRAFT — proposal only. NOT deployed.
> **DRAFTED:** 2026-08-20
> **REFERENCES:** `/root/AAA/.well-known/agent.json` (existing, SEAL-signed v2026.06.30)

---

## Existing State (read, do not modify)

The current `agent.json` describes the **arifOS Kernel** as a single agent with 7 supported actions (`arif_init`, `arif_observe`, `arif_think`, `arif_route`, `arif_judge`, `arif_act`, `arif_seal`). It is SEAL-signed (Ed25519) and registered at `https://arifos.arif-fazil.com/.well-known/agent.json`.

This file is **already Phase 1 DISCOVERY-compliant**. It exposes:
- Federation peers (GEOX, WEALTH, WELL, A-FORGE, A-FORGE MCP, AAA)
- Capability envelope (can_do / cannot_do)
- Escalation tiers (T1/T2/T3/F13)
- Authentication mechanism
- A2A `supported_interfaces`

**Verdict: do NOT overwrite.** Phase 1 work for the kernel card is **complete**.

---

## What Is Net-New (Phase 1)

| Artifact | Status | Location |
|---|---|---|
| `/.well-known/agent.json` (kernel card) | **EXISTS, SEALED** | `/root/AAA/.well-known/agent.json` |
| `/.well-known/agent-card.json` (gateway card) | **EXISTS, SEALED** | `/root/AAA/.well-known/agent-card.json` |
| `/.well-known/mcp/server.json` | **EXISTS, DRAFT** | `/root/AAA/.well-known/mcp/server.json` |
| `/.well-known/arifos.json` (federation manifest) | **DRAFT — net new** | `/root/AAA/forge_work/2026-08-20/ecosystem-expansion/drafts/arifos.json` |
| `/.well-known/did.json` (DID document) | **EXISTS, SEALED** | referenced in `agent-card.json` sovereign extension |

---

## Recommended Path Forward

### Option A — Add `arifos.json` only (RECOMMENDED)
- Deploy the drafted `/root/AAA/forge_work/2026-08-20/ecosystem-expansion/drafts/arifos.json` to `https://arif-fazil.com/.well-known/arifos.json`
- Leave existing SEAL-signed cards unchanged
- arifos.json becomes the **federation manifest** (organs, expansion organs, governance, trust model, memory policy)
- agent.json + agent-card.json remain the **kernel + gateway discovery surfaces**
- Separation: kernel card = who I am; gateway card = how to reach the federation; arifos.json = what the federation contains

**Blast radius:** New file on public surface. Low risk — purely additive.
**Authority required:** Phase 1 SEAL (Arif + Hermes).
**Hermes handoff:** Copy file to `/var/www/arif-fazil.com/.well-known/`, set CORS, no service restart.

### Option B — Extend existing cards with ecosystem fields (NOT RECOMMENDED)
- Adding fields to SEAL-signed cards invalidates their signatures
- Would require re-signing the entire card with Ed25519 sovereign key
- Adds Phase 1 work to a T3 (irreversible signature mutation) envelope
- Higher blast radius for marginal gain

### Option C — Federation manifest embedded in agent-card.json extension (FUTURE)
- Could add `arifos.json` content as another extension under `extensions[]` in agent-card.json
- Requires re-sealing agent-card.json
- Couples discovery to gateway — better as standalone for cleaner separation

---

## Phase 1 Acceptance Criteria

When Phase 1 is sealed and deployed:

- [ ] `https://arif-fazil.com/.well-known/agent.json` returns 200 with valid A2A card
- [ ] `https://aaa.arif-fazil.com/.well-known/agent-card.json` returns 200 with valid A2A gateway card
- [ ] `https://arif-fazil.com/.well-known/arifos.json` returns 200 with the drafted federation manifest
- [ ] All 5 organ-specific agent cards resolve (`/root/AAA/.well-known/` per-organ layout OR per-organ `.well-known/` on subdomain)
- [ ] `https://arif-fazil.com/.well-known/did.json` resolves for F13 sovereign signature verification
- [ ] Caddy/Cloudflare headers allow public GET on all `.well-known/*` paths
- [ ] No Caddy/Cloudflare headers block well-known agents (cf. `MCP initialize Caddy fix 2026-06-29`)

---

## Phase 1 SEAL Checklist (Hermes handoff)

1. Pull the draft: `cp /root/AAA/forge_work/2026-08-20/ecosystem-expansion/drafts/arifos.json /var/www/arif-fazil.com/.well-known/arifos.json`
2. Set permissions: `chmod 644` (public read)
3. Verify: `curl -I https://arif-fazil.com/.well-known/arifos.json`
4. Validate JSON: `jq . /var/www/arif-fazil.com/.well-known/arifos.json | head`
5. Update Caddy if needed (verify no auth-gate on `/.well-known/*`)
6. Receipt: log deploy to VAULT999 via arif_seal (action_hash = sha256 of deployed file)
7. Notify federation: NATS subject `arifos.federation.discovery.sealed`

---

## What This Proposal Does NOT Touch

- Existing SEAL-signed agent.json (kernel card)
- Existing SEAL-signed agent-card.json (gateway card)
- DID document
- VAULT999
- A-FORGE lease / forge_* tools
- arifFLOW
- Any disabled MCP server (per `Disabled MCP Audit 2026-08-04`)
- arifOS kernel internals
- Port bindings
- Caddy config (unless Caddy currently blocks `.well-known/`)
- DNS

---

*Drafted by 333-PROPOSAL. Awaiting 888-JUDGE verdict and Arif + Hermes SEAL.*