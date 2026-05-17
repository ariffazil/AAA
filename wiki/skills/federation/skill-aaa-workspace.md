---
title: "SKILL: AAA Workspace Operations"
type: skill
version: 1.0.0
category: governance
risk_band: MEDIUM
floors: [F1, F11]
evidence_required: true
sources: [/root/.opencode/skills/aaa-workspace/SKILL.md]
confidence: high
---

# SKILL: AAA Workspace Operations

> **Source:** `/root/.opencode/skills/aaa-workspace/SKILL.md`
> **Agent:** OpenCode (Ω-FORGE)
> **Forged:** 2026-05-17

---

## Trigger Conditions

- Managing AAA-specific tasks
- Workspace state, agent lifecycle
- Coordination with other federation organs
- OpenClaw agent management
- Recovery and deployment operations
- Keywords: AAA, workspace, agents, recovery, deployment

---

## Workspace Structure

```
AAA/
├── .opencode/skills/     # Local skills
├── .openclaw/            # OpenClaw agent config
├── api/                  # API endpoints
├── apps/                 # Application layer
└── cancan/               # Capability definitions
```

---

## Common Operations

### Check Workspace Health

```bash
# AAA service status
curl -sf http://localhost:3001/health 2>/dev/null || echo "AAA A2A down"

# OpenClaw agents
ls -la .openclaw/agents/
cat .openclaw/agents/*/state.json 2>/dev/null
```

### Agent Lifecycle

```bash
# List running agents
cat .openclaw/agents/*/state.json | jq '.state'

# Restart agent (depends on OpenClaw CLI)
```

### Sync with arifOS

```bash
# Verify MCP connectivity
curl -sf https://mcp.arif-fazil.com/health

# Check VAULT999 sync
curl -sf http://localhost:5001/health
```

---

## Coordination with Other Organs

| Organ | Role | Coordination |
|-------|------|-------------|
| arifOS MCP | Constitutional decisions | Query before governed actions |
| A-FORGE | Infra deployment | Delegate deployments |
| GEOX/WEALTH/WELL | Domain operations | Cross-repo coordination |
| OpenCode | Meta-orchestration | Via skill-reflector |

---

## Related Pages

- [[federation-entities]] — AAA entity in federation
- [[skill-arifos-operator]] — operating with arifOS
- [[skill-spatial-grounding]] — VPS context grounding
- [[SCHEMA.md]] — TREE777 governance schema

---

*DITEMPA BUKAN DIBERI — AAA is the surface. Govern it well.*
