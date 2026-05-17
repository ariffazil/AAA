---
title: "SKILL: arifOS Federation Atlas"
type: skill
version: 2.0.0
category: governance
risk_band: LOW
floors: []
evidence_required: false
sources: [/root/.opencode/skills/arifOS-federation/SKILL.md]
confidence: high
---

# SKILL: arifOS Federation Atlas

> **Source:** `/root/.opencode/skills/arifOS-federation/SKILL.md`
> **Agent:** OpenCode (Ω-FORGE)
> **Forged:** 2026-05-17

---

## Trigger Conditions

- Understanding federation architecture
- Mapping tasks to correct repo
- Identifying which organ owns a concern
- Navigating between 8 sovereign repos
- Keywords: federation, repos, organs, architecture, A-FORGE, GEOX, WEALTH, WELL, AAA, HERMES

---

## The 8 Sovereign Repos

| # | Organ | Role | Repo | Language | Path |
|---|-------|------|------|----------|------|
| 1 | arifOS | Constitutional Kernel | ariffazil/arifOS | Python 3.12+ | /root/arifOS |
| 2 | A-FORGE | Execution / Forge | ariffazil/A-FORGE | TypeScript/Node.js | /root/A-FORGE |
| 3 | GEOX | Earth Intelligence | ariffazil/GEOX | Python 3.11+ | /root/geox |
| 4 | WEALTH | Capital Intelligence | ariffazil/wealth | Python 3.12+ | /root/WEALTH |
| 5 | WELL | Vitality Intelligence | ariffazil/well | Python 3.12+ | /root/WELL |
| 6 | AAA | Control Plane | ariffazil/AAA | TypeScript/React | /root/AAA |
| 7 | HERMES | ASI Deliberative Relay | (local only) | Node.js/Express | /root/HERMES |
| 8 | arif-sites | Static Sites | ariffazil/arif-sites | Shell/HTML | /root/arif-sites |

---

## VPS Stack Ports

| Service | Port |
|---------|------|
| arifOS MCP | 8080 |
| GEOX | 8081 |
| WEALTH | 8082 |
| WELL | 8083 |
| AAA A2A | 3001 |
| HERMES | 3002 |
| A-FORGE Bridge | 7071 |
| Vault999 | 8100 |
| Vault999 Writer | 5001 |
| PostgreSQL | 5432 |
| Redis | 6379 |
| Qdrant | 6333 |
| Caddy | 80/443 |
| Ollama | 11434 |

---

## Constitutional Floors (Quick Ref)

| Floor | Code | Key Rule |
|-------|------|---------|
| F01 | AMANAH | No irreversible ops without human ack |
| F02 | TRUTH | Cite sources, no fabrication |
| F09 | ANTIHANTU | No consciousness claims |
| F13 | SOVEREIGN | Human veto is absolute |

---

## Build & Test Commands

```bash
# arifOS
cd /root/arifOS && pip install -e ".[dev]" && pytest tests/ -q

# A-FORGE
cd /root/A-FORGE && npm install && npm run build && npm test

# GEOX
cd /root/geox && pip install -e ".[dev]" && pytest tests/ -q

# WEALTH
cd /root/WEALTH && pip install -e . && python internal/monolith.py

# WELL
cd /root/WELL && pip install -e . && python server.py && python test_well.py

# AAA
cd /root/AAA && npm install && npm run build && npm run lint

# HERMES
cd /root/HERMES && npm install && npm test && npm start
```

---

## Related Pages

- [[agent-opencode]] — this agent's entity page
- [[federation-entities]] — all nodes, agents, services
- [[intelligence-tree]] — the 7-layer ontology
- [[SCHEMA.md]] — TREE777 governance schema

---

*DITEMPA BUKAN DIBERI — The federation is mapped.*
