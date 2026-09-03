# Hermes ↔ arifOS MCP Integration — Technical Findings
**Session:** 2026-05-18 | Hermes Agent + Arif audit
**Source:** Hermes ↔ arifOS Fusion Architecture Spec v1.1

---

## Finding 1: Hermes MCP does NOT support server-side tool filtering

**Tested:** `hermes mcp list` shows:
```
arifos  http://127.0.0.1:8080/mcp  all  ✓ enabled
```

**Config schema for HTTP transport (native-mcp skill):**
```
command, args, env, url, headers, timeout, connect_timeout, sampling
```

**No `allowedTools` or `tool_filter` key.** The native-mcp skill explicitly does not support tool filtering for HTTP transports. Full tool access is granted at connection time.

**Implication:** Enforcement must be skill-based self-regulation. Hermes has full arifOS MCP tool access — it self-regulates via the `arifos-recall` skill.

---

## Finding 2: arifOS has 6 deployable memory layers, not 7

| Layer | Tech | Access |
|-------|------|--------|
| L0 Ephemeral | RAM | In-process |
| L1 Session | SQLite FTS5 | Current session |
| L2 Working | Hermes memory/*.md | Current+recent |
| L3 Semantic | Qdrant vector DB | Cross-agent |
| L4 Structured | PostgreSQL | Cross-agent |
| L5 Knowledge | Graphiti graph DB | Cross-agent |
| L6 VAULT999 | Append-only JSONL | Cross-agent |

**Correction:** "arifOS 7 layers" claim in earlier memory was wrong. L0 is RAM scratch, not a deployable layer. 6 deployable layers (L1-L6) with L6 (VAULT999) being the constitutional sovereign.

---

## Finding 3: Hermes is reactive-agentic, not autonomous-agentic

| Capability | Hermes | Truly Agentic |
|------------|--------|---------------|
| Respond to messages | YES | YES |
| Run scheduled tasks | YES | YES |
| Use tools | YES | YES |
| Set own goals | NO | YES |
| Pursue goals across sessions | NO | YES |
| Detect failures and self-correct | NO | YES |
| Act on events without polling | NO | YES |

**Gap:** Intent and metacognition. Not tools — Hermes has 50+ skills, MCP, A2A, cron. The gap is the absence of a SovereignLoop or self-monitoring layer.

---

## Correct MCP tool list for arifOS (self-regulated via skill)

**SHOULD call (read-only):**
- `arif_memory_recall(mode=recall, get, list, context)`
- `arif_vault_seal(mode=list, verify, chain)` — read vault history only
- `arif_ops_measure(mode=health, vitals)`
- `arif_sense_observe(mode=search, ingest)`
- `arif_judge_deliberate(mode=history, explain)`

**MUST NOT call (self-regulated):**
- `arif_vault_seal(mode=seal)` — requires OpenClaw witness
- `arif_forge_execute` — sovereign gate
- `arif_judge_deliberate(mode=judge)` — adjudication gate
- `arif_session_init` — session re-init gate

---

## Finding 4: arifOS memory vs Hermes memory — honest comparison

**Hermes L2 (MEMORY.md / USER.md):**
- Zero latency, prompt-injected, always-on
- 2,200 char limit forces curation
- No audit trail — agent edits own memory
- Single-agent only — not shared with OpenClaw/A-FORGE

**arifOS L3-L6:**
- Cross-agent: any federation node reads same
- Governed: pruning sacred requires 888_HOLD
- Rich retrieval: semantic, entity relationships, constitutional lineage
- Not prompt-injected — must explicitly call arif_memory_recall

**Correct architecture:** Fusion — both memory systems working in parallel, each doing what it does best.

---

**DITEMPA BUKAN DIBERI**