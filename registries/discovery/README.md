# AAA Registry — Discovery Layer

> **PUBLIC-FACING** artifacts that external agents and scanners read first.
> These mirror (and extend) `AAA/.well-known/` and `AAA/public/.well-known/`.

## Axis purpose

Discovery is the only registry layer visible to:
- External MCP / A2A clients querying `/.well-known/`
- The `isitagentready.com` agent-readiness scanner
- AGNTCY/dir peers that pull our OASF record
- The Linux Foundation AI Catalog (when adopted by A2A/MCP steering)

## What lives here

| File | Standard | Spec URL | Phase 1 status |
|---|---|---|---|
| `ai-catalog.json` | Agent-Card/ai-catalog (LF working group) | https://agent-card.github.io/ai-catalog/ | ✅ Generated 2026-06-22 |
| `mcp-server-card.json` | MCP server card (Level 4 readiness) | https://modelcontextprotocol.io/ | ✅ Generated 2026-06-22 |
| `skills-index.json` | Agent Skills index (Level 4 readiness) | https://agentskills.io/ (proposed) | ✅ Generated 2026-06-22 |
| `oasf-record.json` | AGNTCY OASF record | https://github.com/agntcy/oasf | ✅ Generated 2026-06-22 |
| `agent-card.json` | A2A v1.0.0 spec | https://a2a-protocol.org/ | ✅ Already at `public/.well-known/agent-card.json` |
| `agent.json` | Legacy agent.json | (legacy) | ✅ Already at `.well-known/agent.json` |
| `arifos.json` | Federation manifest | (internal) | ✅ Already at `public/.well-known/arifos.json` |
| `a2a-routing-policy.json` | A2A routing policy | (internal) | ✅ Already at `public/.well-known/a2a-routing-policy.json` |

## The 4 files that reached Level 4 readiness

When these 4 exist at the public surface (`/.well-known/`), `aaa.arif-fazil.com`
reaches **Level 4 (Agent-Integrated)** on the agent-readiness ladder.
Adding a valid A2A agent-card.json already in place → **Level 5 (Agent-Native)**.

## Deployment

Files in this directory are NOT yet served at `/.well-known/`.
Phase 4 (publishing) requires explicit 888 approval.
The files are present as **canonical source-of-truth**; serving them is a
Caddy static-route decision, not a content decision.

## Generator

```
python /root/AAA/registries/external/ai-catalog/scripts/build-ai-catalog.py  # 🆕 planned Phase 4.6
```

For Phase 1 these files are hand-built from live data — see
`/root/forge_work/2026-06-22-phase1-discovery-surface.md` for sha256 receipts.
