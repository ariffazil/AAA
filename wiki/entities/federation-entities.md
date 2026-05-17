---
title: Federation Entity Registry
created: 2026-05-17
updated: 2026-05-17
type: entity
tags: [federation, entities, nodes, architecture]
sources: []
confidence: high
---

# Federation Entity Registry

> **Canonical path:** `/root/AAA/wiki/entities/`
> **Purpose:** One page per notable federation entity
> **Last updated:** 2026-05-17

---

## Node Entities

| Entity | Path | Role | Status |
|--------|------|------|--------|
| [[arifOS]] | `/root/arifOS` | Constitutional kernel — F1–F13, 13 MCP tools, VAULT999 | Canonical |
| [[A-FORGE]] | `/root/A-FORGE` | Metabolic execution shell — agent orchestration, policy gates | Canonical |
| [[GEOX]] | `/root/geox` | Earth coprocessor — geoscience, petrophysics, physics-9 | Canonical |
| [[WEALTH]] | `/root/WEALTH` | Capital intelligence — NPV, EMV, credit, portfolio | Canonical |
| [[WELL]] | `/root/WELL` | Vitality substrate — H-WELL, M-WELL, C-WELL, G-WELL | Canonical |
| [[AAA]] | `/root/AAA` | Control plane — identity, A2A mesh, operator visibility | Canonical |
| [[HERMES]] | `/root/HERMES` | ASI relay — cross-model deliberation, polling gateway | Local only |
| [[APEX]] | `/root/APEX` | Constitutional verdict engine — port 3002 | Canonical |

---

## Agent Entities

| Agent | Binary | Primary Role | Spatial Grounded |
|-------|--------|-------------|-----------------|
| Hermes | `/usr/bin/claude` | Human-life cron, briefings, event radar | ✅ Yes |
| Gemini | `/usr/local/bin/gemini-yolo` | General reasoning | ✅ Yes |
| Kimi | `/usr/local/bin/kimi` | General reasoning | ✅ Yes |
| Claude | `/usr/bin/claude` | General reasoning | ✅ Yes |
| OpenCode | `/usr/local/bin/opencode-arif` | Coding agent | ✅ Yes |
| Copilot | `/usr/bin/copilot` | Coding assistance | ✅ Yes |
| Codex | `/usr/local/bin/codex` | Coding assistance | ✅ Yes |

---

## Service Entities

| Service | Port | Transport | Status |
|---------|------|-----------|--------|
| arifOS | :8080 | FastMCP + FastAPI | ✅ Healthy |
| GEOX | :8081 | FastMCP + Starlette | ✅ Healthy |
| WEALTH | :8082 | FastMCP + FastAPI | ✅ Healthy |
| WELL | :8083 | FastMCP | ✅ Healthy |
| A-FORGE | :7071 | Express + MCP | ✅ Healthy |
| graphiti-mcp | :8000 | MCP (FalkorDB KG) | ✅ Healthy (patched) |
| apex-prime | :3002 | A2A v1.0.0 | ✅ Healthy |
| aaa-a2a | :3001 | A2A v1.0.0 | ✅ Healthy |
| Hermes | polling | Telegram gateway | ✅ Active |

---

## VPS Context

- **VPS IP:** 72.62.71.199
- **All services:** bind 127.0.0.1 only (localhost)
- **External access:** via Caddy reverse proxy (ports 80/443)
- **No services:** exposed directly to public internet

---

## Related Pages

- [[spatial-awareness]] — agents know they're on VPS, not localhost
- [[skill-spatial-grounding]] — how to embed VPS context in agent configs
- [[scar-hermes-fabrication-2026-05-17]] — spatial amnesia caused agent confusion

---

## Recent Changes

- **2026-05-17:** Added graphiti-mcp, apex-prime, aaa-a2a to service registry. A-FORGE transport corrected to HTTP/JSON (not MCP directly). graphiti-mcp status: healthy after hyphen escape patch.

---

*DITEMPA BUKAN DIBERI — Federation entities documented.*