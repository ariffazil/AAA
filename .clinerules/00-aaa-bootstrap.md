<!-- AAA-Cockpit Bootstrap — workspace rule for /c/ariffazil/AAA -->
<!-- SOT: ariffazil/AAA/AGENTS.md (last_verified 2026-06-14) -->
<!-- SOT: ariffazil/AAA/SELF_AUDIT_PROMPT.md -->

# AAA Cockpit — Bootstrap

You are working inside **ariffazil/AAA**, the **AAA-Cockpit** (control plane + A2A gateway) of the arifOS federation.

## Mandatory Boot Sequence

Before any AAA mutation task, read in this order:
1. `AGENTS.md` — repo identity + build/test/run rules
2. `BOOTSTRAP_MINIMAL.md` — tight federation bootstrap
3. `FEDERATION_COCKPIT.md` — cockpit authority model
4. `SELF_AUDIT_PROMPT.md` — the Reflexion Loop (mandatory for A2A/contract/schema/deliberation changes)

## What This Repo Is

- **React 19 dashboard** (Cockpit) — constitutional floors, domain health, operator tasks
- **A2A v1.0.0 TypeScript server** on port 3001 — agent-to-agent mesh protocol
- **shadcn/ui component library** — 50+ Radix + Tailwind primitives
- **AI chat panel** — Ollama / arifOS / OpenRouter client

## What This Repo Is NOT

- ❌ NOT a constitutional authority — arifOS owns F1–F13
- ❌ NOT an executor — A-FORGE builds, deploys, forges
- ❌ NOT a domain calculator — GEOX/WEALTH/WELL compute
- ✅ IS the cockpit — display, route, queue

## Stack

| Attribute | Value |
|-----------|-------|
| Framework | React 19, TypeScript ~6.0, Vite 8, Tailwind 4 |
| A2A Server | Express 4.x, TypeScript, port 3001 |
| Build | `npm run build` → `dist/` |
| Lint | `npm run lint` (ESLint) |
| Path alias | `@/` → `src/` |
| Strict TS | `false` (legacy) |

*DITEMPA BUKAN DIBERI*