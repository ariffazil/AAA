# Workspace — AAA vs arifOS Repo Split

> **CLAIM** | Source: workspace audit + session discussion | **Confidence:** 0.93 | **Epoch:** 2026-04-23

## Summary

arifOS uses two GitHub repos with clean separation of concerns:
- **AAA** = agent workspace (the agent's mind + operational config)
- **arifOS** = Python + MCP kernel (the agent's body + code)

---

## AAA — Agent Workspace

```
https://github.com/ariffazil/AAA
Local: /srv/openclaw/workspace/
```

**Purpose:** Constitutional OS, OpenClaw, LLM layer, memory, skills, observability

**Contents:**
- `MEMORY.md` — curated long-term memory
- `SOUL.md` / `AGENTS.md` / `USER.md` — identity anchors
- `memory/YYYY-MM-DD.md` — daily running context
- `docs/` — documentation + wiki
- `skills/` — per-agent skills
- `observability/` — Prometheus + Grafana stack
- `.openclaw/` — OpenClaw daemon config (local only, not pushed)
- `tests/` — contract parity tests

**Git remote:** `ariffazil/AAA` (public, token: gho_...)

---

## arifOS — Python + MCP Kernel

```
https://github.com/ariffazil/arifos
```

**Purpose:** Python code, MCP server, tool implementations, constitutional runtime

**Contents:**
- `arifosmcp/` — MCP server package (44→13 tools)
- `core/` — core runtime
- `arifos/` — constitutional kernel
- `Dockerfile` / `docker-compose.yml` — deployment
- `canonical_schema_contract.json` — tool output schema
- `tests/` — test suite

**Git remote:** `ariffazil/arifos` (public)

---

## Dependency Model

```
AAA (workspace)
    ↓ imports / references
arifOS (code)
    ↓ pip install or clone
MCP Server (runtime)
    ↓ serves
OpenClaw (gateway)
    ↓ connects
arifOS-MCP endpoint (mcp.arif-fazil.com)
```

arifOS is pip-installable (`pip install arifOS`) or cloned monorepo.
AAA references it as a dependency, does not copy code.

---

## Personal Docs Policy

**NEVER** put personal docs (CV, legal templates, salary negotiation) in AAA (public repo).
Move to `/root/.private/` or local-only paths.

---

## Cross-References

- [[infrastructure/OBSERVABILITY]] — Prometheus stack lives in AAA
- [[arifos/999_VAULT]] — VAULT999 lives in arifOS (Supabase)

---

## Status

**Stable** — repo split is intentional and canonical.

---

DITEMPA BUKAN DIBERI — 999 SEAL ALIVE