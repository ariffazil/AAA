# Telegram Bot Contract Matrix — arifOS Federation

> **DITEMPA BUKAN DIBERI** — Forged 2026-08-05 by 333-AGI under F13 SOVEREIGN directive
> **Purpose:** Single source of truth for "who answers what" across 3 bot identities
> **SOT:** This file + live `:port/health` probe. Any other doc is a pointer.

## Bot Identity → Role → Webhook → Agent

| Bot | Telegram Handle | Role | Webhook URL | Caddy Route | Upstream Port | Agent | Protocol |
|-----|----------------|------|-------------|-------------|---------------|-------|----------|
| **Hermes ASI** | `@ASI_arifos_bot` | Human bridge / NL encoder / gateway | `/telegram/webhook` | line 1022 | `:8444` | Hermes gateway (systemd) | Telegram Bot API → MCP |
| **FORGE** | `@arifOS_bot` | Coding execution bridge | `/forge/webhook` | line 1018 | `:7071` | A-FORGE (systemd) | Telegram Bot API → forge_shell |
| **OpenClaw AGI** | `@AGI_ASI_bot` | System ops / metabolizer / flow | `/telegram-webhook*` | line 2178 | `:8787` | OpenClaw gateway (systemd) | Telegram Bot API → A2A/flow |

## A2A Endpoints (Agent-to-Agent, NOT Telegram)

| Endpoint | Port | Protocol | Status | Exposed |
|----------|------|----------|--------|---------|
| **AAA A2A Server** | `:3001` | JSON-RPC 2.0 (A2A v1.0) | ✅ LIVE | Caddy `/a2a/*` + Tailscale |
| **Hermes A2A Listener** | `:18087` | JSON-RPC 2.0 (A2A v1.0) | ❌ DOWN (2026-08-05) | local-only, needs fix |
| **A-FORGE MCP** | `:7072` | MCP Streamable HTTP | ✅ LIVE | Caddy `mcp.arif-fazil.com` |

## Human Interaction Contract

| DM / Group Chat | Who Answers | Use Case |
|-----------------|-------------|----------|
| DM `@ASI_arifos_bot` | Hermes ASI | General intent, research, Q&A, federation queries |
| DM `@arifOS_bot` | FORGE | Code builds, deployments, debugging, git ops |
| DM `@AGI_ASI_bot` | OpenClaw AGI | System status, federation health, flow monitoring |
| Group (all 3) | Hermes is primary responder | Conversational — others react to explicit commands |

## Channel vs Protocol — The Iron Rule

```
TELEGRAM = transport/channel (human ↔ bot, Bot API webhook)
A2A      = protocol/coordination (agent ↔ agent, JSON-RPC sendMessage)
AAA      = control plane (discovery, registration, cockpit — :3001)
```

**Never route Telegram through A2A. Never expose A2A as a Telegram webhook.**
They are orthogonal layers. Telegram is how Arif talks. A2A is how agents talk to each other.
AAA shows both in one cockpit.

## Health Check

```bash
# Telegram endpoints (via Caddy)
curl -sI https://arif-fazil.com/telegram/webhook | head -1
curl -sI https://arif-fazil.com/forge/webhook | head -1
curl -sI https://arif-fazil.com/telegram-webhook | head -1

# A2A endpoints
curl -sf http://127.0.0.1:3001/health        # AAA A2A server
curl -sf http://127.0.0.1:18087/health       # Hermes A2A listener
```

## Port Map — Agent Card vs Runtime Truth

| Agent | Card Says | Runtime Truth | Status |
|-------|-----------|---------------|--------|
| **Hermes ASI** | gateway:18086, a2a:18089 | gateway:8444+8445 (Caddy /telegram/webhook) | Card STALE — gateway port changed |
| **OpenClaw AGI** | gateway:8787 | gateway:8787+18789 (Caddy /telegram-webhook*) | Card ≈ Runtime |
| **FORGE Bot** | exec:7071, mcp:7072 | exec:7071 (Caddy /forge/webhook) | Card ≈ Runtime |
| ~~Hindsight~~ | :18087→8888 | :18087 was Hindsight KB, NOT Hermes A2A | **RETIRED 2026-08-05** |
| Hermes A2A | planned :18089 per card | Never deployed | Service unit doesn't exist |

## Known Issues

| Issue | Severity | Status |
|-------|----------|--------|
| Hindsight KB on :18087 crashed (no API key) — port hijacked from planned Hermes A2A | ✅ RESOLVED | Container stopped+removed. :18087+:18088 freed. |
| Hermes agent card says gateway:18086 but runtime is :8444 | LOW | Card needs sync with live Caddy routes |
| Hermes A2A (:18089) planned but never deployed | MEDIUM | `hermes-a2a.service` unit file doesn't exist |
| 3 Telegram bots' agent cards exist but not visible in AAA directory | LOW | Cards at `/root/AAA/agents/<bot>/agent-card.json`. AAA `card-inventory-loader` scans directory. Discovery gap likely in live-probe filter. |
| FORGE-bot agent card was missing | ✅ RESOLVED | Created at `/root/AAA/agents/forge-bot/agent-card.json` |
| 3 bot identities → user mental model noisy | ✅ RESOLVED | Contract matrix is the answer |
| A2A invisible to operator | ✅ RESOLVED | Surfaced in matrix + documented port plan |

## Probe Results (2026-08-05T06:30Z)

```
/telegram/webhook  → :8444  ✅ Hermes gateway LIVE (pid 315766 on :8444, pid 213210 on :8445)
/forge/webhook     → :7071  ✅ A-FORGE LIVE
/telegram-webhook* → :8787  ✅ OpenClaw gateway LIVE (pid 77179, also :18789)
/a2a/*             → :3001  ✅ AAA A2A server LIVE (Tailscale + localhost)
:18087             →        🗑️  RETIRED (was Hindsight KB, now freed)
:18089             →        ⬜ Hermes A2A PLANNED (not deployed)
AAA agent registry →        7 core organs. Agent cards for Hermes/OpenClaw/FORGE-bot exist.
```

---

*Forged: 2026-08-05. DITEMPA BUKAN DIBERI — the contract is forged, not given.*
