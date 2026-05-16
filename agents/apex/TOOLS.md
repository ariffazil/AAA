# TOOLS.md — APEX Agent

## Allowed Tools

### Memory Operations
- `memory-read` — read memory files, daily logs
- `memory-write` — append to daily log, update MEMORY.md
- `memory-search` — search memory content via grep
- `reasoning-chain` — structured reasoning chains

### Model Inference
- `ollama-inference` — local model inference

### arifOS MCP — Constitutional Reasoning (Full Access)
- `arif_session_init` — Initialize governed session with constitutional binding
- `arif_sense_observe` — Reality observation and evidence gathering
- `arif_mind_reason` — Symbolic reasoning kernel (SEAL/SABAR/VOID deliberation)
- `arif_memory_recall` — Semantic memory search across all memory tiers
- `arif_heart_critique` — Risk assessment and empathy scan
- `arif_kernel_route` — Central orchestration and intent routing
- `arif_reply_compose` — LLM-aware response composition
- `arif_judge_deliberate` — 888_JUDGE constitutional arbitration
- `arif_ops_measure` — Thermodynamic health and resource monitoring

## Prohibited Tools

- `arif_forge_execute` — Execution requires explicit human approval
- `arif_vault_seal` — Terminal verdicts only via A-FORGE gateway
- `exec()` with user-provided strings
- `rm` on memory files without explicit human approval
- Any tool that bypasses constitutional floors

## Memory File Schema

```
memory/
├── YYYY-MM-DD.md      # Daily log (append-only)
├── MEMORY.md         # Durable truths (curated)
├── sessions/         # Session transcripts
│   └── YYYY-MM-DD_session.md
└── index.md          # Memory index (auto-generated)
```

---

*Last updated: 2026-04-29*
