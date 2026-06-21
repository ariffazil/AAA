# CONTEXT.md — AAA (Control Plane)

> **Organ:** AAA | **Port:** 3001 | **Repo:** `ariffazil/AAA`
> **Last Updated:** 2026-06-21

## Live State
- **Service:** `aaa-a2a.service` (systemd, enabled)
- **Health:** `http://127.0.0.1:3001/health`
- **Frontend:** React 19 + Vite 8 + Tailwind 4
- **A2A:** Express 4.x TypeScript gateway
- **Role:** Display, route, queue — never adjudicate
- **Warga agents:** 333-AGI, 555-ASI, 888-APEX, A-AUDIT, A-ARCHIVE
- **Agent dirs:** `/root/AAA/agents/{333-AGI,555-ASI,888-APEX,A-AUDIT,A-ARCHIVE}`

## Key Updates (2026-06-21)
- **Hermes ASI consolidated** — runtime proxy + 5 warga identities (commit `5ecd8c27`)
- **7-organ topology** — AAA federation upgrade with 333/555/666/777 agent routes (commit `1408e0d1`)
- **GENESIS/ populated** — 3 files (013-015) for AAA-specific doctrine
- **Entropy cleaned** — Hermes backup (~700MB), 28 empty dirs, 6 broken symlinks removed

## Dependencies
- arifOS MCP kernel (port 8088) — constitutional data
- All organ MCP endpoints for federation display
- PostgreSQL for agent registry

## Known Issues
- None open. Hermes ASI backup purge complete.
