# TOOLS.md — hermes Agent

## Allowed Tools

### Memory Operations
- `read` — read memory files, daily logs
- `write` — append to daily log, update MEMORY.md
- `glob` — find memory files by pattern
- `grep` — search memory content

### Reasoning Tools
- `chain-of-thought` — structured reasoning chains
- `inference` — derive from known facts
- `recall` — retrieve past session context

### MCP Surfaces
- `arifOS kernel` — constitutional judgment (SEAL/SABAR/VOID)

### Model Inference
- `ollama` — local model inference
- `openrouter` — external model (if configured)

## Prohibited Tools

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
