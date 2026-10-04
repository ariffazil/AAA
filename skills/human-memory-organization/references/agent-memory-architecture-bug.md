# Agent Memory Architecture Bug (2026-08-08)

`skill_view(name='agent-memory-architecture')` fails with:
```
Object of type date is not JSON serializable
```
The skill itself is at `/usr/local/lib/hermes-agent/profiles/aaa-hermes/skills/mlops/agent-memory-architecture/SKILL.md`.

**Cause:** unquoted date in YAML frontmatter — the parser tries to serialize a Python datetime object.

**Workaround:** `read_file(path='/usr/local/lib/hermes-agent/profiles/aaa-hermes/skills/mlops/agent-memory-architecture/SKILL.md')` to load content directly; ignore the `skill_view` failure.

**Fix needed:** patch frontmatter to quote date values (or remove date field). Not applied here — hub-protected skill, flagged for curator attention.

## L1–L6 Federation Memory Map (verified live 2026-08-08)

| Layer | Substrate | Collections / Paths |
|---|---|---|
| L1 | Redis ephemeral (ping = PONG) | 127.0.0.1:6379 |
| L2 | Redis session thread | 127.0.0.1:6379 |
| L3 | Qdrant vectors (14 collections) | `arif_evidence`, `arifos_constitution`, `arifos_memory`, `arifos_precedent`, `arifos_session_memory`, `arifos_vault_canon`, `arifos_vault_ephemeral`, `arifos_vault_quarantine`, `arifos_vault_sacred`, `arifos_vault_working`, `atlas333_eureka`, `federation_shared`, `openclaw_memory`, `petronas_knowledge` |
| L4 | Supabase (54 domain tables) | postgres://127.0.0.1:5432 |
| L5 | Graphiti / FalkorDB (relationships) | 127.0.0.1:6380 |
| L6 | VAULT999 append-only | `/root/arifOS/VAULT999/outcomes.jsonl` (41,391 receipts as of 2026-08-08 23:43 UTC) |

Human memory (separate from L1-L6, see `human-memory-organization` skill):
- `/root/memory/` — dated seal files 2026-07-03 → 2026-08-03, plus `overnight-*.md`, `rsi/`, `sessions/`, `ratifications/`
- `/root/.private/` — CV docs, salary-negotiation drafts, `petronas-memory/`
- No Obsidian vault (OBSIDIAN_VAULT_PATH unset)
