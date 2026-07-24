# Agent Card Version Policy

> SOT: This file. Forged 2026-07-24 by FORGE under APEX refactor.

## Rule

1. **One SOT per agent.** Each agent has exactly one canonical `agent-card.json`.
2. **Version in card must match version in registry.** `agents.yaml` is canonical registry. Card `version` field must agree.
3. **Duplicate detection.** If two cards claim the same `agent_id` at different versions, the higher version in the canonical location wins. Archive the lower.
4. **Canonical locations:**
   - AAA warga: `/agents/agent_cards/<name>.json`
   - External runtimes: `/agents/_external/<runtime>/agent-card.json`
   - Gateway card: `/a2a/agent-card.json`
5. **Retired agents** must have `status: retired` in `agents.yaml`. Their card may remain in `_archive/`.
6. **No duplicate agent cards in `dist/`.** `dist/` is a build artifact. Only `a2a/agent-card.json` is SOT.
7. **Version check on CI.** `validate-root-agent-config.mjs` must verify card versions match registry.

## Anti-patterns

- ❌ Same agent card at v1.0.0 and v4.1.0 in different directories
- ❌ `agent-cards.json` as a separate registry (use `agents.yaml` only)
- ❌ dist/ copies diverging from SOT
- ❌ Retired agents without `status: retired` field
