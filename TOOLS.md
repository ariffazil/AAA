# TOOLS.md — Local Environment Notes

> **Skills define how tools work. This file is for local specifics — yours alone.**
> **DITEMPA BUKAN DIBERI — Intelligence is forged, not given.**

**Rules:**
- Do not store secrets, credentials, API keys, or tokens here
- Do not duplicate AGENTS.md governance rules here
- Do not store transient state — use HEARTBEAT.md for runtime state

---

## VPS Infrastructure

| Service | Host | Port | Notes |
|---------|------|------|-------|
| arifOS MCP | mcp.arif-fazil.com | 8080 | Constitutional kernel, 13 tools |
| GEOX MCP | geox | 8081 | Earth intelligence |
| WEALTH MCP | wealth-organ | 8082 | Capital intelligence |
| WELL MCP | well | 8083 | Biological substrate |
| A-FORGE | af-bridge-prod | 7071 | Execution bridge |
| AAA A2A | aaa-a2a | 3001 | Federation gateway |
| Caddy | caddy | 80/443 | Reverse proxy |
| Postgres | postgres | 5432 | arifOS + WEALTH |
| Redis | redis | 6379 | arifOS + WEALTH |
| Qdrant | qdrant | 6333 | arifOS vector memory |

---

## MCP Endpoints (Public)

| Domain | Route | Purpose |
|--------|-------|---------|
| mcp.arif-fazil.com | /mcp | arifOS MCP |
| arifos.arif-fazil.com | /mcp | arifOS MCP (alias) |
| geox.arif-fazil.com | /mcp | GEOX MCP |
| well.arif-fazil.com | /mcp | WELL MCP |
| wealth.arif-fazil.com | /mcp | WEALTH MCP |
| forge.arif-fazil.com | / | A-FORGE bridge |
| aaa.arif-fazil.com | /a2a/* | AAA A2A gateway |

---

## GitHub Repos

| Repo | Path |
|------|------|
| arifOS | /root/arifOS |
| A-FORGE | /root/A-FORGE |
| GEOX | /root/geox |
| WEALTH | /root/WEALTH |
| AAA | /root/AAA |
| WELL | /root/well |

---

## Skills Location

- Primary: ~/.hermes/skills/
- Workspace: /root/AAA/skills/

---

## Workspace Paths

| Purpose | Path |
|---------|------|
| AAA workspace (this) | /root/AAA |
| arifOS workspace | /root/arifOS |
| Daily memory | /root/AAA/memory/YYYY-MM-DD.md |
| Skills | ~/.hermes/skills/ |
| Cron output | ~/.hermes/cron/output/ |

---

## TTS Preferences

- Provider: MiniMax (via minimax_bridge)
- Default model: speech-02-hd
- Emotion parameter: available on speech-02-hd only
- Note: speech-02 (non-hd) rejects emotion parameter

---

## Communication

- Primary: Telegram (group: arifOS)
- Home channel ID: 267378578
- All agents post verdicts to Telegram

---

*This file is for environment specifics only. Governance lives in AGENTS.md, LOOP.md, AUTONOMY.md.*
