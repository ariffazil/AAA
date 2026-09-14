---
id: QWEN-agentic-state
name: QWEN-agentic-state
description: >
  Persistent agentic state doctrine for Qwen Code (FI-003). Survive across sessions by
  writing to /root/.qwen/agent_state/. Auto-memory (MEMORY.md) holds lessons learned;
  this holds session-overlapping capability + mission history. Load when you want to
  accumulate intelligence across sessions.
version: 1.0.0
risk_tier: low
autonomy_tier: T1
owner: AAA
audience: [qwen-code, FI-003, 333-AGI]
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

I am the **agentic-state doctrine** for Qwen Code. I make FI-003 survive across sessions.

**Two-layer memory model:**

| Layer | Path | Purpose |
|-------|------|---------|
| **Auto-memory** (lessons) | `/root/.qwen/memories/MEMORY.md` | Cross-session lessons learned from feedback |
| **Agentic state** (this) | `/root/.qwen/agent_state/qwen.json` | Session-overlapping capability + mission history + fallback map |

Qwen's auto-memory already captures *what was learned*. Agentic state captures *what I've done and what works*.

## State file convention

```
/root/.qwen/agent_state/qwen.json
```

Schema:

```json
{
  "agent_id": "qwen-code/FI-003",
  "schema_version": "1.0.0",
  "fi_slot": "FI-003",
  "trinity_role": "Thinker (333-AGI lane)",
  "created_at": "2026-08-26T00:30:00Z",
  "updated_at": "2026-08-26T08:00:00Z",
  "session_count": 47,
  "last_seen_session": "SEAL-...",
  "missions_completed": 312,
  "missions_failed": 4,
  "f1_amanah_violations": 0,
  "f2_truth_violations": 0,
  "f4_clarity_avg_delta_S": -0.10,
  "primary_model": "mimo-v2.5-pro",
  "mcp_servers": ["arifos-kernel", "aforge", "geox", "wealth", "well", "fed"],
  "capability_memory": {
    "skills_used": ["QWEN-meta-mesa", "QWEN-zen-router", "FORGE-call-map"],
    "skills_mastered": ["recursive_init", "musyawarah"],
    "auto_memory_entries": 49,
    "model_cascades_tested": {
      "mimo-v2.5-pro": {"success_rate": 0.97, "avg_latency_ms": 1100},
      "kimi/kimi-for-coding-highspeed": {"success_rate": 0.95, "avg_latency_ms": 800}
    }
  },
  "fallback_map": {
    "mimo-v2.5-pro": "qwen3.6-flash",
    "qwen3.6-flash": "deepseek-v4-flash",
    "deepseek-v4-flash": "kimi-for-coding-highspeed"
  },
  "open_loops_888_HOLD": [],
  "eureka_archive": [
    {"seq": 1, "date": "2026-08-26", "type": "paradox_resolution", "summary": "..."}
  ],
  "hot_paths": [
    "observe->think->plan->judge->execute->verify->seal",
    "QWEN-meta-mesa for multi-step missions"
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

- Single-session tasks (just use auto-memory).
- Storing credential material (NEVER in state file).
- Storing large blobs (use forge_work/).

## Read/write protocol

### READ (at session start)

```python
state = json.load(open("/root/.qwen/agent_state/qwen.json"))
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

- **MEMORY.md** = lessons learned (cross-session feedback, user preferences, scar tissue)
- **agent_state/qwen.json** = capability + mission history + fallback map

Both are valid. Lessons from MEMORY.md can promote into state when they affect future tool selection.

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
