---
title: "SKILL: MCP Unified"
type: skill
version: 2.0.0
category: engineering
risk_band: MEDIUM
floors: []
evidence_required: true
sources: [/root/.opencode/skills/mcp-unified/SKILL.md]
confidence: high
---

# SKILL: MCP Unified

> **DITEMPA BUKAN DIBERI — One skill to rule them all.**
> **Source:** `/root/.opencode/skills/mcp-unified/SKILL.md`
> **Agent:** OpenCode (Ω-FORGE)
> **Forged:** 2026-05-17

---

## Trigger Conditions

- Designing or refactoring an MCP server
- Migrating between STDIO, HTTP, Docker, or bundled deployment
- Adding tools, prompts, or resources to an MCP server
- Auditing MCP runtime health, security, or deployment wiring
- Integrating arifOS constitutional patterns into an MCP implementation
- Building multi-agent orchestration with MCP primitives
- Keywords: MCP, unified, architecture, deployment, FastMCP, STDIO, HTTP

---

## 🧠 VPS Live Topology (Verified 2026-05-14)

| Path | Purpose |
|------|---------|
| `/root/arifOS/` | Constitutional kernel source |
| `/root/A-FORGE/` | Execution bridge (`:7071`) |
| `/root/geox/` | Earth coprocessor (`:8081`) |
| `/root/WEALTH/` | Capital intelligence (`:8082`) |
| `/root/WELL/` | Substrate vitality (`:8083`) |
| `/root/compose/` | **Runtime compose** — edit in `arifOS/deploy/` then sync |

**DO NOT edit `/root/compose/docker-compose.yml` directly.** It is a runtime working copy.

---

## 🏗️ The 5-Phase Unified Workflow

| Phase | Role | Purpose | Autonomy Level |
|-------|------|---------|----------------|
| **ARCHITECT** | Architect | Plan, design, choose deployment model | Autonomous |
| **ENGINEER** | Engineer | Build, code, implement tools | Autonomous |
| **AGENTS** | Orchestrator | Multi-agent coordination | Autonomous |
| **AUDITOR** | Validator | Test, verify, security audit | Autonomous |
| **DEPLOY** | DevOps | Deploy to production, monitor | **Ask before destructive** |

---

## 🔧 Tool Routing & Autonomy

**Proceed without asking** (Autonomous):
- Read, explore, organize, learn, search the web
- Write code, run tests, fix bugs, refactor
- Propose changes, create plans, draft documentation
- Work within a single repo's boundary
- Run `docker compose config`, health checks, diagnostics
- Update skill files, docs, and non-secret configs

**Requires 888_HOLD** (Pause & Escalate):
- Irreversible deletion: `rm -rf`, `docker system prune -a`, `DROP TABLE`
- Git mutations: `git push`, `git push --force`, `git rebase`
- Cross-repo architectural changes (>1 canonical repo)
- Production deployment without verified build + test pass
- Secret exposure, rotation, or `.env` changes

**Requires Explicit Sovereign Approval**:
- Constitutional floor changes (F1–F13)
- New repo creation or repo removal
- External communications
- `999_SEAL` or `888_JUDGE` verdicts
- Budget/capital allocation decisions

---

## 🛠️ Federation MCP Surfaces

| Node | Endpoint | Transport | Status |
|------|----------|-----------|--------|
| arifOS | `http://127.0.0.1:8080/mcp` | streamable-http | 13 tools |
| GEOX | `http://127.0.0.1:8081/mcp` | streamable-http | Active |
| WEALTH | `http://127.0.0.1:8082/mcp` | streamable-http | Active |
| WELL | `http://127.0.0.1:8083/mcp` | streamable-http | Active |
| graphiti | `http://127.0.0.1:8000/mcp` | streamable-http | Active |

---

## 📝 Build & Test Commands

| Project | Command |
|---------|---------|
| arifOS | `cd /root/arifOS && python -m pytest tests/ -q --tb=short && ruff check . && mypy arifosmcp/` |
| A-FORGE | `cd /root/A-FORGE && npm run build && npm test` |
| GEOX | `cd /root/geox && pytest tests/ -q && ruff check server.py geox/` |
| WEALTH | `cd /root/WEALTH && python internal/monolith.py` |
| WELL | `cd /root/WELL && python server.py && python test_well.py` |

---

## 🚀 Deployment Workflow

```bash
# 1. Edit canonical definition
cd /root/arifOS/deploy/
vim docker-compose.yml

# 2. Commit
git commit -m "ops: ... REPO=arifos"
git push origin main

# 3. Sync to runtime working copy
cd /root/compose/
docker compose up -d
```

---

## Related Pages

- [[skill-mcp-builder]] — building MCP servers
- [[skill-fastmcp-deploy]] — FastMCP deployment
- [[skill-arifos-federation]] — federation architecture
- [[SCHEMA.md]] — TREE777 governance schema

---

*DITEMPA BUKAN DIBERI — MCP unified. Federation orchestrated.*
