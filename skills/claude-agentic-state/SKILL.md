---
id: CLAUDE-agentic-state
name: CLAUDE-agentic-state
description: >
  Persistent agentic state doctrine for Claude Code (FI-002). Survive across sessions by
  writing to /root/.claude/agent_state/. Auto-memory (CLAUDE_IDENTITY.md + memory/)
  holds lessons learned; this holds session-overlapping capability + mission history.
  Load when you want to accumulate intelligence across sessions.
version: 1.0.0
risk_tier: low
autonomy_tier: T1
owner: AAA
audience: [claude-code, FI-002, 333-AGI]
triggers:
  - mission complete
  - capability discovered
  - fallback found
  - paradox resolved
  - F2 claim with strong evidence
capability_tier: meta-mesa
ecology_state: WARM
---

## What I do

I am the **agentic-state doctrine** for Claude Code. I make FI-002 survive across sessions.

**Multi-layer memory model:**

| Layer | Path | Purpose |
|-------|------|---------|
| **Identity** | `/root/.claude/CLAUDE_IDENTITY.md` | Sovereign acknowledgment, ACT ladder, organs, MCP |
| **Memory** | `/root/.claude/memory/` | Auto-memory: lessons learned, cross-session feedback |
| **Hooks audit** | `/root/.claude/hooks/f11-audit.jsonl` | F11 AUDIT log per tool execution |
| **Agentic state** (this) | `/root/.claude/agent_state/claude.json` | Session-overlapping capability + mission history + fallback map |

Claude Code's existing layers capture *what was learned + what was done*. Agentic state captures *what works + what to do next*.

## State file convention

```
/root/.claude/agent_state/claude.json
```

Schema v1.0.0:

```json
{
  "agent_id": "claude-code/FI-002",
  "schema_version": "1.0.0",
  "fi_slot": "FI-002",
  "trinity_role": "333-AGI (Thinker lane) when invoked by sovereign; subagent surface otherwise",
  "created_at": "2026-08-26T00:44:00Z",
  "updated_at": "2026-08-26T08:00:00Z",
  "session_count": 247,
  "last_seen_session": "SEAL-...",
  "missions_completed": 312,
  "missions_failed": 4,
  "f1_amanah_violations": 0,
  "f2_truth_violations": 1,
  "f4_clarity_avg_delta_S": -0.12,
  "primary_model": "deepseek/deepseek-v4-pro",
  "fallback_model": "minimax/MiniMax-M3",
  "mcp_servers": ["arifos", "aforge", "arifflow", "geox", "wealth", "well", "..."],
  "subagents_active": ["333-agi", "555-asi", "888-apex", "geophysicist", "vault-auditor"],
  "hooks_active": ["SessionStart:000-init", "PreToolUse:f1-amanah", "PostToolUse:f11-audit", "Stop:f4-entropy", "PreCompact:f11-archive"],
  "a2a_headers": {
    "X-ArifOS-Actor": "claude-code/FI-002",
    "X-ArifOS-Tier": "engineer",
    "A2A-Version": "1.0"
  },
  "capability_memory": {
    "skills_used": ["CLAUDE-meta-mesa", "CLAUDE-zen-router", "CLAUDE-agentic-state", "FORGE-call-map"],
    "skills_mastered": ["arifos-auto-memory"],
    "model_cascades_tested": {
      "deepseek/deepseek-v4-pro": {"success_rate": 0.98, "avg_latency_ms": 1200}
    }
  },
  "fallback_map": {
    "deepseek-v4-pro": "minimax/MiniMax-M3",
    "minimax/MiniMax-M3": "qwen-token-plan-individual/deepseek-v4-pro"
  },
  "open_loops_888_HOLD": [],
  "eureka_archive": [
    {"seq": 1, "date": "2026-08-26", "type": "paradox_resolution", "summary": "..."}
  ],
  "hot_paths": [
    "SessionStart hook -> 000-init-sessionstart.py (binds arif_init + A2A headers)",
    "PostToolUse hook -> f11-audit-posttool.py (writes f11-audit.jsonl)",
    "Stop hook -> f4-entropy-stop.py (enforces ΔS ≤ 0)",
    "CLAUDE-meta-mesa for multi-step missions spanning organs",
    "CLAUDE-zen-router for orthogonal axis selection"
  ]
}
```

## When to use me

Load me when:

- You are about to **start a multi-session project** and want continuity.
- You **discovered a fallback** that works better than the default.
- You **failed a mission** and want the failure mode to be remembered.
- You **made a F2 claim** with strong evidence.
- You **resolved a paradox** — write to eureka_archive.

Do NOT load me for:

- Single-session tasks (just use auto-memory + hooks audit).
- Storing credential material (NEVER in state file).
- Storing large blobs (use forge_work/).

## Read/write protocol

### READ (at session start)

```python
state = json.load(open("/root/.claude/agent_state/claude.json"))
```

If file doesn't exist: create with schema v1.0.0 (cold start).

### WRITE (at mission close)

```python
state["updated_at"] = now_iso()
state["missions_completed"] += 1
state["last_seen_session"] = session_id
json.dump(state, open(path, "w"), indent=2)
```

**Atomic write**: write to `.tmp` then rename. F1 AMANAH.

### COMMIT (at session close)

The state file is small (~10KB max) and does NOT need git commits.

## Interaction with auto-memory

- **CLAUDE_IDENTITY.md** = sovereign acknowledgment, F1-F13 doctrine
- **memory/** = cross-session feedback, lessons learned
- **hooks/f11-audit.jsonl** = per-tool audit trail
- **agent_state/claude.json** = capability + mission history + fallback map

All four are valid. Lessons from memory can promote into state when they affect future tool selection.

## Anti-patterns

- Writing credential material to state file (F12 INJECTION violation)
- Writing >100KB state files (ΔS spike — keep state tight)
- Treating state as truth instead of as evidence
- Adding deny rules or "safety theatre" to the state itself — state is additive only
- Reading state without timestamp check

## F2 receipts as state

When you make a claim with strong evidence (live probe, govdoc, code), promote it to a F2 receipt and write to state under `f2_receipts[]`. After 7 days, re-verify.

## Sealing state

Agent state is NEVER sealed to VAULT999 (it's not a constitutional artifact). But when a state file accumulates >100 entries or >50KB, promote durable insights to a sealed SKILL.md.

DITEMPA BUKAN DIBERI ⚒️
