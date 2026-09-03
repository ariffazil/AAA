# Hermes ↔ arifOS Fusion Architecture — Findings Log
**Session:** 2026-05-18 | Hermes Agent + Arif audit session

---

## Key Findings

### 1. Hermes MCP does NOT support server-side tool filtering

Tested: `hermes mcp list` shows `arifos: http://127.0.0.1:8080/mcp — all tools — enabled`

The native-mcp skill config for HTTP transport supports: `command`, `args`, `env`, `url`, `headers`, `timeout`, `connect_timeout`, `sampling`. No `allowedTools` or `tool_filter` key.

**Implication:** Enforcement must be skill-based self-regulation, not server-side config. Hermes has full arifOS MCP tool access at connection time.

---

### 2. arifOS 7 memory layers (corrected from "7 layers" claim)

arifOS has 6 deployable memory layers, not 7:

| Layer | Tech | Access | Hermes use |
|-------|------|--------|------------|
| L0 Ephemeral | RAM | In-process | Tool scratch space |
| L1 Session | SQLite FTS5 | Current session | session_search |
| L2 Working | Hermes memory/*.md | Current+recent | MEMORY.md prompt-injected |
| L3 Semantic | Qdrant vector DB | Cross-agent | arif_memory_recall |
| L4 Structured | PostgreSQL | Cross-agent | arif_memory_recall |
| L5 Knowledge | Graphiti graph DB | Cross-agent | arif_memory_recall |
| L6 VAULT999 | Append-only JSONL | Cross-agent | arif_vault_seal (write-gated) |

---

### 3. Hermes is reactive-agentic, not autonomous-agentic

| Capability | Hermes | Truly Agentic |
|------------|--------|---------------|
| Respond to messages | YES | YES |
| Run scheduled tasks | YES | YES |
| Use tools | YES | YES |
| Set own goals | NO | YES |
| Pursue goals across sessions | NO | YES |
| Detect failures and self-correct | NO | YES |
| Act on events without polling | NO | YES |

Gap is intent and metacognition, not tools. Hermes has 50+ skills, MCP servers, A2A, cron — but no SovereignLoop or self-monitoring layer.

---

### 4. OpenClaw vs Hermes memory — honest comparison

**Hermes memory — strengths:**
- Always-on context: prompt-injected, zero latency
- Curated by necessity: 2,200 char limit forces economy
- Automatic session search: SQLite FTS5
- Simple to debug: open a markdown file

**Hermes memory — weaknesses:**
- Single-agent: no sharing with OpenClaw, A-FORGE, Kimi
- No audit trail: agent can edit its own memory
- Shallow: 1,300 tokens total

**arifOS memory — strengths:**
- 6 layers: ephemeral → session → Qdrant → Postgres → Graphiti → VAULT999
- Cross-agent: any federation node recalls same memory
- Governed: pruning sacred requires 888_HOLD
- Rich retrieval: semantic, entity relationships, constitutional lineage

**arifOS memory — weaknesses:**
- Not prompt-injected: must explicitly call arif_memory_recall
- Higher latency: vector search vs instant file read
- More complex: 3 databases vs 2 markdown files

---

### 5. Correct architecture: Fusion, not replacement

**Wrong:** Replace Hermes memory with arifOS
**Wrong:** Layer arifOS without integration
**Right:** Fusion — both memory systems working in parallel, each doing what it does best

---

## Specs and Skills Created

| File | Purpose |
|------|---------|
| `/root/AAA/wiki/hermes-arifos-integration-spec.md` v1.1 | Full fusion architecture spec |
| `/root/.hermes/skills/arifos-recall/SKILL.md` v1.1 | Skill bridging Hermes L2 ↔ arifOS L3-L6 |

---

## Open Questions

- Phase 2 pending event dir needs OpenClaw cron — not yet implemented
- arifOS MCP tools (888_JUDGE, 999_SEAL) still need OpenClaw as proxy — Hermes can't call them directly
- Phase 3 autonomy upgrade (webhooks, watchdog loops) deferred to after Phase 1 stable

---

**DITEMPA BUKAN DIBERI**