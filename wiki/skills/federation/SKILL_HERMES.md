---
title: "SKILL: HERMES Operations"
type: skill
version: 1.0.0
category: governance
risk_band: MEDIUM
floors: [F1, F9]
evidence_required: true
sources: [/root/.opencode/skills/hermes-ops/SKILL.md]
confidence: high
---

# SKILL: HERMES Operations

> **Source:** `/root/.opencode/skills/hermes-ops/SKILL.md`
> **Agent:** OpenCode (Ω-FORGE)
> **Forged:** 2026-05-17

---

## Trigger Conditions

- Operating HERMES ASI Deliberative Relay
- 888 JUDGE evaluation, constitutional verdicts
- A2A protocol, agent deliberation
- Agent lifecycle management
- Keywords: HERMES, hermes, ASI, 888, judgment, deliberation, A2A

---

## Role in Federation

| Property | Value |
|----------|-------|
| Organ | HERMES — ASI Deliberative Relay |
| Authority | 888 JUDGE — evaluates, does not execute |
| Port | 3002 (internal), routed via Caddy |
| Protocol | A2A v1.0.0 |
| Repo | /root/HERMES (local only, no public remote) |

---

## Health Check

```bash
# Quick status
curl -s http://localhost:3002/ | python3 -m json.tool

# Agent card (A2A discovery)
curl -s http://localhost:3002/.well-known/agent-card.json | python3 -m json.tool

# Docker health
docker inspect hermes-agent --format '{{.State.Health.Status}}'
```

---

## Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Service identity + health |
| `/.well-known/agent-card.json` | GET | A2A agent discovery |
| `/tasks` | POST | Submit a deliberation task |
| `/tasks/{taskId}` | GET | Check task status |
| `/tasks/{taskId}/stream` | GET | Stream task results |
| `/tasks/{taskId}/cancel` | POST | Cancel a pending task |

---

## Lifecycle Commands

```bash
# Install
cd /root/HERMES && npm install

# Start (dev with watch)
cd /root/HERMES && npm run dev

# Start (production)
cd /root/HERMES && npm start

# Test
cd /root/HERMES && npm test

# Docker restart
docker compose -f /root/compose/docker-compose.yml restart hermes-agent

# View logs
docker logs hermes-agent --tail 100 -f
```

---

## Constitutional Role

HERMES is the 888 JUDGE layer — evaluates actions against all 13 floors but does NOT:
- Modify files
- Deploy
- Seal

Execution authority lives in arifOS (999 SEAL) and A-FORGE (777 FORGE).

---

## Related Pages

- [[federation-entities]] — HERMES entity
- [[concept-tools-and-embodiment]] — HERMES as deliberation organ
- [[skill-arifos-operator]] — operating with arifOS
- [[SCHEMA.md]] — TREE777 governance schema

---

*DITEMPA BUKAN DIBERI — HERMES evaluates. It does not execute.*
