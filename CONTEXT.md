<!-- SOT-MANIFEST
owner: Arif
last_verified: 2026-06-24
valid_from: 2026-06-24
valid_until: 2026-07-24
confidence: high
scope: /root/AAA
-->

# CONTEXT.md — AAA (Cockpit / Control Plane)

> **Organ:** AAA | **Port:** 3001 | **Repo:** `ariffazil/AAA`
> **Last Updated:** 2026-06-24

## Live State

- **A2A Service:** `aaa-a2a.service` (systemd, port 3001)
- **Cockpit:** React 19 + Vite 8 + Tailwind 4, served by Caddy
- **Health:** `http://127.0.0.1:3001/health`
- **Role:** Control plane / cockpit — A2A gateway, 888 JUDGE deliberation, human interface

## Key Components

- `a2a-server/` — Express A2A v0.3.0 gateway (`server.js`, `deliberation.ts`, `vault.js`)
- `src/` — React cockpit (`Cockpit.tsx`, `ai/`, `gateway/`, `components/ui/`)
- `agents/`, `skills/`, `contracts/`, `registries/` — federation metadata
- `public/` — static assets + `a2a/agent-card.json`

## 888 JUDGE

- Legacy APEX deliberation was absorbed into `a2a-server/deliberation.ts`.
- APEX service (`apex-prime.service`) on port 3002 is **decommissioned**.

## Dependencies

- arifOS kernel (8088) — constitutional floors and final judgment
- A-FORGE (7071/7072) — execution under SEAL
- VAULT999 (8100/5001) — audit ledger

## Known Issues

- Federation Governance Gate previously failed due to missing `FEDERATION_CONTRACT.md` and `CONTEXT.md` — **resolved 2026-06-24**
- Secret-scan false positives may exist in test fixtures; all production secrets are in `/root/.secrets/` only.

---

*DITEMPA BUKAN DIBERI — Judgment is made visible, not invented.*
