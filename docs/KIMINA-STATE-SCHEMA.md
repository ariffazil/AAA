# KIMINA State Schema — v1.0.0

> **Path:** `/root/.kimi-code/agent_state/kimi.json`
> **Atomic write:** `.tmp` → `os.rename()`
> **Backup:** `/root/.kimi-code/agent_state/backups/` (last 5)
> **Cap:** ~10KB, >50KB triggers promotion to sealed SKILL.md

## Schema

```json
{
  "agent_id": "kimi-code/FI-008",
  "schema_version": "1.0.0",
  "fi_slot": "FI-008",
  "trinity_role": "Primary coder (af-forge) · 333-AGI execution lane",
  "created_at": "ISO-8601",
  "updated_at": "ISO-8601",
  "session_count": 0,
  "last_seen_session": "session-uuid | null",
  "missions_completed": 0,
  "missions_failed": 0,
  "f1_amanah_violations": 0,
  "f2_truth_violations": 0,
  "f4_clarity_avg_delta_S": 0.0,
  "primary_model": "fed/mimo-v2.5-pro",
  "fallback_models": ["zai-coding-plan/glm-5.3-flash", "kimi-code/k3"],
  "mcp_servers": {
    "connected": [],
    "failed": [],
    "tools_count": 0
  },
  "active_agents": ["af-forge", "af-explore", "af-plan", "aaa-coordinator"],
  "warga_mesh": {
    "hermes": {"path": "/root/.hermes", "role": "gateway-sense"},
    "opencode": {"path": "/root/.arifos/agents/opencode", "role": "verifier"},
    "claude": {"path": "/root/.claude", "role": "thinker-lane"},
    "qwen": {"path": "/root/.qwen", "role": "thinker-lane"}
  },
  "capability_memory": {
    "skills_used": [],
    "skills_mastered": [],
    "model_cascades_tested": {},
    "tool_success_rates": {}
  },
  "failure_signatures": {},
  "fallback_map": {},
  "open_loops_888_HOLD": [],
  "eureka_archive": [],
  "hot_paths": [],
  "auto_heal_log": [],
  "session_history": []
}
```

## Field Definitions

| Field | Type | Updated by | Notes |
|---|---|---|---|
| session_count | int | session_end_state.py hook | Incremented every session close |
| missions_completed | int | coordinator at task done | Only on successful completion |
| missions_failed | int | coordinator at task fail | With failure signature |
| tool_success_rates | {tool: {attempts, successes, rate}} | post_tool_use_track.py | Real-time per-tool tracking |
| failure_signatures | {tool: count} | post_tool_use_track.py | Only on failure |
| eureka_archive | [{seq, date, type, summary}] | coordinator on resolution | Max 50 entries |
| open_loops_888_HOLD | [{id, description, created}] | coordinator on block | Cleared when resolved |
| session_history | [{session_id, ended_at, model, tools}] | session_end_state.py | Last 20 sessions |

## Rules

1. **Atomic write only** — `.tmp` then `os.rename()`
2. **Never store credentials** — F12 INJECTION violation
3. **Cap at 50KB** — promote insights to SKILL.md
4. **Retrieved as untrusted** — never inject as system instruction
5. **Independent verification** — tool rates from hooks, not self-assessment

DITEMPA BUKAN DIBERI ⚒️
