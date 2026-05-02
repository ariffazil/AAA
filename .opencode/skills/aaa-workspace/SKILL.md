---
name: aaa-workspace
description: AAA (Agents, API, Apps) workspace operations within the arifOS federation. Canonical workspace for governed agent operations, recovery, and deployment. Use for managing AAA-specific tasks, workspace state, agent lifecycle, and coordination with other federation organs.
version: 1.0.0
author: arif
tags: aaa, workspace, agents, recovery, deployment
---

# AAA Workspace Protocol

## AAA Role in Federation
AAA is the surface layer of arifOS: Agents, API, AI, Apps. Canonical workspace for governed agent operations, recovery, and deployment.

## Workspace Structure
```
AAA/
├── .opencode/skills/     # Local skills
├── .openclaw/            # OpenClaw agent config
├── api/                  # API endpoints
├── apps/                 # Application layer
└── cancan/               # Capability definitions
```

## Common Operations

### Check Workspace Health
```bash
# AAA service status
curl -sf http://localhost:8084/health 2>/dev/null || echo "AAA down"

# OpenClaw agents
ls -la .openclaw/agents/
cat .openclaw/agents/*/state.json 2>/dev/null
```

### Agent Lifecycle
```bash
# List running agents
cat .openclaw/agents/*/state.json | jq '.state'

# Restart agent
# (具体取决于OpenClaw CLI)
```

### Sync with arifOS
```bash
# Verify MCP connectivity
curl -sf https://mcp.arif-fazil.com/health

# Check VAULT999 sync
curl -sf http://localhost:5001/health
```

## Coordination with Other Organs
- arifOS MCP: constitutional decisions
- A-FORGE: infra deployment
- GEOX/WEALTH/WELL: domain operations
- OpenCode: meta-orchestration via skill-reflector

---

*Last updated: 2026-05-02*