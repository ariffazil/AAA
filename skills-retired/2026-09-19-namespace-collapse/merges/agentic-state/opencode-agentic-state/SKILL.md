---
name: opencode-agentic-state
description: Persistent agentic state doctrine — survive across sessions by writing to /root/.config/opencode/agent_state/<agent>.json. Load this when you want to accumulate capability memory, mission history, and federation learnings across sessions.
license: MIT
compatibility: opencode
metadata:
  layer: meta-mesa
  tier: state
  audience: 333-AGI, 555-ASI, 888-APEX, dispatch
---

## What I do

I am the **agentic-state doctrine**. I make agents that survive across sessions.

Before me, every session was a blank slate. After me, every agent has **persistent memory**:

- **Mission history** — what missions I completed, when, what floor verdict.
- **Capability memory** — which tools/skills I have actually exercised successfully.
- **Fallback map** — which model/provider/cascade actually works for which task.
- **F2 receipts** — claims I have made, with evidence, that survive across sessions.
- **Hot caches** — pre-computed routing tables, common DAG templates, hot paths.

## State file convention

```
/root/.config/opencode/agent_state/<agent_name>.json
```

Each agent file:

```json
{
  "agent_id": "333-AGI",
  "schema_version": "1.0.0",
  "created_at": "2026-08-26T00:15:00Z",
  "updated_at": "2026-08-26T08:00:00Z",
  "session_count": 47,
  "last_seen_session": "SEAL-eae656a15f4749f9",
  "missions_completed": 312,
  "missions_failed": 4,
  "f1_amanah_violations": 0,
  "f2_truth_violations": 1,
  "f4_clarity_avg_delta_S": -0.12,
  "capability_memory": {
    "skills_used": ["opencode-meta-mesa", "opencode-zen-router", "FORGE-call-map"],
    "skills_mastered": ["opencode-init", "opencode-propose-seal"],
    "skills_avoided": ["FORGE-nextjs-mastery"],
    "model_cascades_tested": {
      "deepseek-v4-pro": {"success_rate": 0.98, "avg_latency_ms": 1200},
      "kimi/kimi-for-coding-highspeed": {"success_rate": 0.95, "avg_latency_ms": 800}
    }
  },
  "fallback_map": {
    "deepseek-v4-pro": "minimax/MiniMax-M3",
    "kimi/kimi-for-coding-highspeed": "deepseek/deepseek-v4-flash",
    "qwen-token-plan-individual/qwen3.6-flash": "deepseek/deepseek-v4-flash"
  },
  "open_loops_888_HOLD": [],
  "eureka_archive": [
    {"seq": 1, "date": "2026-08-26", "type": "paradox_resolution", "summary": "..."}
  ],
  "hot_paths": [
    "observe->think->plan->judge->execute->verify->seal",
    "opencode-meta-mesa for multi-step missions"
  ]
}
```

## When to use me

Load me when:

- You are about to **start a multi-session project** and want continuity.
- You **discovered a fallback** that works better than the default — write it.
- You **failed a mission** and want the failure mode to be remembered.
- You **made a F2 claim** with strong evidence — write it as a F2 receipt.
- You **resolved a paradox** — write to eureka_archive.

Do NOT load me for:

- Single-session tasks (just use carry-forward.json).
- Storing credential material (NEVER in state file — use the sovereign credential store under /root).
- Storing large blobs (use forge_work/, not state/).

## Read/write protocol

### READ (at session start)

```python
state = json.load(open(f"/root/.config/opencode/agent_state/{agent_name}.json"))
```

If file does not exist: create with schema v1.0.0 (cold start).

### WRITE (at mission close)

```python
state["updated_at"] = now_iso()
state["missions_completed"] += 1
state["last_seen_session"] = session_id
json.dump(state, open(path, "w"), indent=2)
```

**Atomic write**: write to `.tmp` then rename. F1 AMANAH.

### COMMIT (at session close)

The state file is small enough (~10KB max) that it does NOT need git commits. It is auto-snapshot via the existing `~/.local/share/arifos/carry_forward_backups/` mechanism.

## Interaction with carry-forward.json

- **carry-forward.json** = session-level (this session only, opens vs closes)
- **agent_state/<name>.json** = agent-level (across all sessions, accumulates)

Both are valid. Use the right one for the right scope.

## Anti-patterns

- Writing credential material to state file (F12 INJECTION violation)
- Writing >100KB state files (ΔS spike — keep state tight)
- Writing without updating updated_at (audit failure)
- Reading state without timestamp check (could be stale)
- Treating state as truth instead of as evidence (state has Ω₀ ≥ 0.03)

## F2 receipts as state

When you make a claim with strong evidence (live probe, govdoc, code), promote it to a F2 receipt and write to state under `f2_receipts[]`:

```json
"f2_receipts": [
  {
    "claim": "arifOS :8088 has 13 active floors",
    "evidence": "curl :8088/health | jq .floors_active",
    "evidence_hash": "sha256:abc123...",
    "created_at": "2026-08-26T00:16:13Z",
    "ttl_days": 7
  }
]
```

After 7 days, re-verify. ΔS <= 0 on verification means receipt holds.

## Sealing state

Agent state is NEVER sealed to VAULT999 (it is not a constitutional artifact). The state file is the agent working memory, not the institution record.

But: when a state file accumulates >100 entries or >50KB, **promote the durable insights** to a sealed SKILL.md and let the state file decay.

DITEMPA BUKAN DIBERI ⚒️
