# AAA Copilot Instructions

AAA is the control plane and agent-workspace anchor for this federation. Treat it as the shared workspace abstraction, not just a frontend repo.

This file is the repo-level AAA anchor for Copilot sessions. The redacted snapshot attestation lives in `docs/operations/copilot-snapshot-attestation.md`.

## Global vs repo-local config

- Keep operational Copilot config global in `~/.copilot/`.
- Do not create repo-local `.copilot/` directories here unless there is a deliberate exception.
- This repo-level file is the AAA-specific context layer, not a replacement for global MCP/LSP config.

## Build, test, and run

- Install: `npm install`
- Build: `npm run build`
- Full validation: `npm test`
- Lint: `npm run lint`
- AAA-specific validation: `npm run validate:aaa`
- A2A tests: `npm run a2a:test`
- A2A server: `npm run a2a:server`
- Dev server: `npm run dev`

## High-level architecture

- `src/main.tsx` boots the UI, `src/App.tsx` is the app root, and `src/Cockpit.tsx` is the main operator dashboard.
- `src/gateway/` contains the A2A gateway and agent-card surface.
- `src/adapter/`, `src/hooks/`, and `src/lib/` hold shared app plumbing.
- `agents/` and `workspace/` are the agent-facing work surfaces; keep them aligned with the control plane role of this repo.

## Key conventions

- TypeScript is ESM and uses explicit imports from `@/` for `src/`.
- `npm test` is a composite validation command (`lint` + `build`), not a separate unit-test runner.
- `npm run validate:aaa` is the repo-specific schema/contract gate; use it when touching contracts or exported surfaces.
- `npm run a2a:test` is the targeted check for the gateway surface.
- Keep A2A and control-plane changes in this repo; keep constitutional judgment in `arifOS`.
