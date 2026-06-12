# CONTEXT.md — AAA (Control Plane)

> **Organ:** AAA | **Port:** 3001 | **Repo:** `ariffazil/AAA`
> **Kernel SoT:** `ariffazil/arifOS` (FEDERATION_CONTRACT.md + GENESIS/000)
> **Last Updated:** 2026-06-12

## Live State
- **Service:** `aaa-a2a.service` (systemd, enabled)
- **Health:** `http://127.0.0.1:3001/health`
- **Frontend:** React 19 + Vite 8 + Tailwind 4
- **A2A:** Express 4.x TypeScript gateway
- **Role:** Display, route, queue — never adjudicate

## Dependencies
- arifOS MCP kernel (port 8088) — constitutional data
- All organ MCP endpoints for federation display
- PostgreSQL for agent registry

## Current Focus
- Operational. AGI kernel specs committed (2026-06-12). Agent cards live.
- GENESIS/ still missing (pending 011+ allocation)

## Known Issues
- No GENESIS/ — kernel canon unlinked
- APEX reference in FEDERATION_COCKPIT.md fixed (2026-06-12)
