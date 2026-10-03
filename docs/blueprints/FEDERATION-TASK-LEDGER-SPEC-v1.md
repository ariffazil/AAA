# Federation Task Ledger v1 — Spec (F13-stage, no build)
**Problem:** Codex has `carry_forward.json` (441 entries). Claude has no equivalent. Per Arif: **don't create `claude_carry_forward.json` — use ONE federation task ledger.**

**Solution:** Single shared ledger at `/root/.hermes/carry_forward.json` with per-agent attribution.

## Schema

```json
{
  "schema": "arifos.federation_task_ledger.v1",
  "entries": [
    {
      "id": "e-<uuid>",
      "kind": "open_loop" | "session_seal" | "f13_task" | "audit_trail",
      "agent_id": "<canonical: harness/FI-NNN>",
      "owner": "codex" | "claude-code" | "kimi-code" | "qwen-code" | "hermes",
      "state": "active" | "superseded" | "closed" | "blocked_external",
      "ts": "2026-10-03T...",
      "content": "...",
      "evidence_refs": ["sha256:..."],
      "expiry": "2026-10-10T..." (TTL for open_loop, otherwise null)
    }
  ]
}
```

## Per-agent views

- Codex writes entries with `owner: "codex"`
- Claude writes entries with `owner: "claude-code"`
- All agents read full ledger
- Per-agent query: filter by `owner == <self>`

## What stays LOCAL (per agent)

- Claude session JSONL in `/root/.claude/projects/-root/` (immutable, transport)
- Codex session logs
- Per-agent memory files (`/root/.claude/memory/MEMORY.md` etc.)

## What goes SHARED

- Cross-agent coordination (e.g. "Codex is mutating X, Claude wait")
- F13 ratification queue
- Audit trail of who did what
- Open loops that block other agents

## Migration

- Codex: just change `owner` field on existing entries from absent to "codex"
- Claude: read existing ledger, write new entries with `owner: "claude-code"`
- One file, one truth, per-agent attribution

## Reversibility

None — this is spec only.
