# Agent-Zero Status: ARCHIVED

> Agent-Zero is not currently active. No running process; no service file.

## Source snapshots

- `/root/backups/agent-zero/` — prior backup
- `/root/backups/entropy-reduction-2026-06-30/oo0-state/agent-zero/` — full snapshot from entropy-reduction backup
- `/root/oo0-STATE/agent-zero/` — live stale copy pending relocation

## Recommission path

If Agent-Zero is reactivated:
1. Create `/root/AAA/agents/agent-zero/{AGENTS.md,IDENTITY.md,SOUL.md,TOOLS.md,agent-card.json}`
2. Move source to `/root/src/agent-zero/`
3. Add systemd service if needed
4. Update `AAA/agents/AGENT_REGISTRY.md`

## Decision

Archived 2026-06-30 by FORGE (000Ω) because no active process/service and source exists only inside `/root/oo0-STATE/`.
