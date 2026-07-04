# Sub-Agent Spawn Template — OpenClaw Operational Procedure

**Procedure ID:** `subagent-spawn`  
**Agent:** OpenClaw (AGI — Operational Gateway)  
**Priority:** P1  
**Forged:** 2026-06-14  
**DITEMPA BUKAN DIBERI**

## Purpose

Standard contract for spawning bounded sub-agents. Every spawned agent receives a clear task definition, output schema, time budget, and evidence requirement. Returns structured JSON. Terminates when complete. No long-running daemons.

## Spawn Contract (JSON Schema)

```json
{
  "task_id": "unique-task-id",
  "task_description": "What to do in plain human language",
  "output_schema": {
    "required_fields": ["field1", "field2"],
    "format": "json"
  },
  "time_budget_minutes": 15,
  "evidence_required": true,
  "risk_band": "T0|T1|T2",
  "allowed_tools": ["bash", "read", "web_search"],
  "forbidden_tools": ["rm", "systemctl", "docker"],
  "spawned_at": "ISO8601",
  "deadline": "ISO8601"
}
```

## Spawn Commands

### OpenClaw → OpenCode (coding sub-agent)

```bash
# Via sessions_spawn or A2A
openclaw spawn opencode \
  --task "Audit the last 50 governance events for E7 pattern updates" \
  --time 30m \
  --output-schema '{"patterns": [], "recommendations": []}' \
  --risk T1
```

### OpenClaw → Hermes (deliberation sub-agent)

```bash
openclaw spawn hermes-asi \
  --task "Check epistemic coherence of the following claim: ..." \
  --time 10m \
  --output-schema '{"verdict": "CONFIRMED|REFUTED|MIXED", "confidence": 0.0-1.0, "evidence": []}' \
  --risk T0
```

## Output Contract

Every sub-agent MUST return:

```json
{
  "task_id": "unique-task-id",
  "status": "COMPLETED|TIMED_OUT|FAILED",
  "verdict": "structured per output_schema",
  "evidence": [
    {"type": "url|tool_output|file", "value": "..."}
  ],
  "duration_seconds": 245,
  "notes": "Any caveats or partial results"
}
```

## Time Budget Enforcement

- Agent tracks elapsed time internally
- At 80% of budget: warn and prepare summary
- At 100%: return best-effort result with `status: TIMED_OUT`
- No extensions without explicit human approval

## Governance

- Sub-agents inherit the spawner's lease and risk ceiling
- Sub-agent actions are logged under the spawner's session_id
- All sub-agent outputs are ephemeral unless explicitly sealed to VAULT999
- Sub-agents have NO F13 authority — cannot override sovereign decisions

## Deployment

This template lives at:
- `/root/AAA/agents/openclaw/procedures/SUBAGENT_SPAWN.md` (this file)
- Referenced by OpenClaw's AGENTS.md and TOOLS.md
