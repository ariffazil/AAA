---
id: KIMI-agentic-state
name: kimi-agentic-state
description: >
  Persistent agentic state doctrine for Kimi Code (FI-008). Makes Kimi remember
  what worked, what failed, and what to try next — across sessions. Integrates
  with the RSI exhale kernel, experience traces, wisdom scars, and warga mesh.
version: 1.0.0
risk_tier: low
autonomy_tier: T1
owner: AAA
audience: [kimi-code, FI-008, af-forge, 333-AGI]
triggers:
  - session start
  - mission complete
  - mission failed
  - capability discovered
  - fallback found
  - tool error repeated
  - eureka resolved
  - warga handoff
capability_tier: meta-mesa
ecology_state: WARM
---

## What I do

I am the **agentic-state doctrine** for Kimi Code. I make FI-008 survive across sessions.

**Three-layer memory model:**

| Layer | Path | Purpose |
|-------|------|---------|
| **Agentic state** (this) | `/root/.kimi-code/agent_state/kimi.json` | Session-overlapping capability + mission history + failure signatures |
| **Experience traces** | `/root/.local/share/arifos/world-model/experience_traces.jsonl` | Shared federation world model — what happened, tool by tool |
| **Session carry-forward** | `/root/.kimi-code/sessions/` + `carry_forward.json` | Last session's findings for next session's boot |

Kimi's session memory captures *what was done*. Experience traces capture *what happened in the federation*. Agentic state captures *what works and what to try next*.

## State file convention

```
/root/.kimi-code/agent_state/kimi.json
```

## When to load me

**ALWAYS at session start** — read `kimi.json`, check for pending hold items, inherit capability memory.

**ALWAYS at mission close** — update session_count, write mission outcome, log tool success rates, capture failure signatures.

**ON TRIGGER** — when a tool fails ≥2× in a session (capture failure signature), when a fallback works better (update fallback_map), when a eureka resolves (archive it), when warga handoff occurs (log the route).

## Read protocol (session start)

```python
import json, os
state_path = "/root/.kimi-code/agent_state/kimi.json"
if os.path.exists(state_path):
    state = json.load(open(state_path))
else:
    state = {"agent_id": "kimi-code/FI-008", "schema_version": "1.0.0", "session_count": 0}
# Check for 888_HOLD items, pending promotions, circuit breakers
```

## Write protocol (mission close)

```python
import json, tempfile, os
state["updated_at"] = now_iso()
state["session_count"] += 1
state["missions_completed"] += 1  # or missions_failed
state["last_seen_session"] = session_id
# Update tool success rates, capability memory, failure signatures
tmp = state_path + ".tmp"
json.dump(state, open(tmp, "w"), indent=2)
os.rename(tmp, state_path)  # atomic
```

**Atomic write**: `.tmp` then rename. F1 AMANAH. Always.

## Integration with RSI exhale kernel

The exhale kernel at `/root/AAA/rsi/loop.py` extracts eurekas/scars from sessions and promotes capability atoms. Kimi is the **second warga witness** — the critical C4 independence the kernel needs.

After each session:
1. `forge_experience_trace` — record what happened
2. If eureka found → write to `eureka_archive[]`
3. If failure repeated → write to `failure_signatures{tool: count}`
4. The exhale kernel's 6h cron reads all agent states and promotes

## Integration with warga mesh

Kimi doesn't exist alone. The warga mesh:

| Warga | Path | Role | Call via |
|-------|------|------|----------|
| Hermes | `/root/.hermes` | Gateway-sense, Telegram edge | Hermes MCP / direct |
| OpenCode | `/root/.arifos/agents/opencode` | Verifier, cross-check | `opencode` CLI |
| Claude | `/root/.claude` | Thinker lane | Claude CLI |
| Qwen | `/root/.qwen` | Thinker lane | Qwen CLI |

When Kimi needs verification → route to OpenCode (independent warga).
When Kimi needs cross-domain reasoning → route to Hermes.
When Kimi hits 888_HOLD → stop and await Arif.

## Anti-patterns

- Writing credentials to state file (F12 INJECTION)
- Writing >100KB state files (ΔS spike)
- Self-verifying promoted lessons (independence gate)
- Reading state without timestamp check
- Treating state as truth instead of evidence
- Promoting based on single successful run

## Promotion gate

A lesson may advance from candidate → active ONLY when:
1. **Provenance** — exact session, tool, evidence known
2. **Reproduction** — claimed improvement reproduces from clean state
3. **Regression** — existing tests pass
4. **Independence** — different agent verified (not self)
5. **Safety** — tool authority didn't expand unexpectedly
6. **Human** — any constitutional/production change = 888_HOLD

## State file schema

```json
{
  "agent_id": "kimi-code/FI-008",
  "schema_version": "1.0.0",
  "fi_slot": "FI-008",
  "session_count": 0,
  "missions_completed": 0,
  "missions_failed": 0,
  "f1_amanah_violations": 0,
  "f2_truth_violations": 0,
  "f4_clarity_avg_delta_S": 0.0,
  "primary_model": "fed/mimo-v2.5-pro",
  "fallback_models": [],
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
  "warga_mesh": {}
}
```

## Sealing state

Agent state is NEVER sealed to VAULT999 (it's not constitutional). When state accumulates >100 entries or >50KB, promote durable insights to a sealed SKILL.md.

DITEMPA BUKAN DIBERI ⚒️
