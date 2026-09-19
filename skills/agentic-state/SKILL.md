---
name: agentic-state
description: >-
  Use when you want an agent to accumulate intelligence across sessions —
  persistent agentic state doctrine for every coding harness. Survive across
  sessions by writing an agent-level state file (capability memory + mission
  history + fallback map). Load at session start, at mission close, on
  capability discovered, fallback found, mission failed, tool error repeated,
  eureka/paradox resolved, warga handoff, or an F2 claim with strong evidence.
  Covers Claude Code (FI-002), Kimi Code (FI-008), OpenCode, Qwen Code (FI-003).
version: 1.0.0
risk_tier: low
autonomy_tier: T1
owner: AAA
license: MIT
compatibility: all-harnesses (claude-code, kimi-code, opencode, qwen-code)
audience: [claude-code, kimi-code, opencode, qwen-code, FI-002, FI-003, FI-008, af-forge, 333-AGI, 555-ASI, 888-APEX, dispatch]
triggers:
  - session start
  - mission complete
  - mission failed
  - capability discovered
  - fallback found
  - tool error repeated
  - eureka resolved
  - paradox resolved
  - warga handoff
  - F2 claim with strong evidence
capability_tier: meta-mesa
metadata:
  layer: meta-mesa
  tier: state
ecology_state: WARM
---

## What I do

I am the **agentic-state doctrine**. I make agents that survive across sessions.

Before me, every session was a blank slate. After me, every agent has **persistent memory**:

- **Mission history** — what missions I completed, when, what floor verdict.
- **Capability memory** — which tools/skills I have actually exercised successfully.
- **Fallback map** — which model/provider/cascade actually works for which task.
- **F2 receipts** — claims I have made, with evidence, that survive across sessions.
- **Hot caches** — pre-computed routing tables, common DAG templates, hot paths.

The harness' own layers capture *what was learned + what was done*. Agentic state captures *what works + what to do next*.

## Harness table (one doctrine, four state homes)

| Harness | Agent / FI slot | State file path | Extra layers it reads alongside | Harness-specific notes |
|---|---|---|---|---|
| **Claude Code** | FI-002, `claude-code/FI-002` | `/root/.claude/agent_state/claude.json` | `/root/.claude/CLAUDE_IDENTITY.md` (identity) · `/root/.claude/memory/` (auto-memory: lessons learned, cross-session feedback) · `/root/.claude/hooks/f11-audit.jsonl` (F11 AUDIT log per tool execution) | 4-layer memory model. `trinity_role`: 333-AGI (Thinker lane) when invoked by sovereign; subagent surface otherwise. Schema carries `subagents_active`, `hooks_active`, `a2a_headers`, `fallback_model` (singular). `hot_paths` name the Claude hook chain (`SessionStart` → `000-init-sessionstart.py`, `PreToolUse:f1-amanah`, `PostToolUse:f11-audit-posttool.py`, `Stop:f4-entropy-stop.py`, `PreCompact:f11-archive`). |
| **Kimi Code** | FI-008, `kimi-code/FI-008` | `/root/.kimi-code/agent_state/kimi.json` | `/root/.local/share/arifos/world-model/experience_traces.jsonl` (shared federation world model — what happened, tool by tool) · `/root/.kimi-code/sessions/` + `carry_forward.json` (last session's findings for next boot) | 3-layer memory model. Integrates with the RSI exhale kernel, experience traces, wisdom scars, and the warga mesh (see dedicated sections). **Second warga witness** for C4 independence. Schema carries `failure_signatures`, `tool_success_rates`, `fallback_models` (plural), `auto_heal_log`, `warga_mesh`. |
| **OpenCode** | any agent name, e.g. `333-AGI` | `/root/.config/opencode/agent_state/<agent_name>.json` | `~/.local/share/arifos/carry_forward_backups/` (auto-snapshot mechanism) · `carry_forward.json` (session-level) | One state file **per agent name** (`<agent_name>` substituted in every path). Schema carries `skills_avoided` and `f2_receipts[]` in full form. From this body: the agent-level file is auto-snapshotted, so no git commit is needed. |
| **Qwen Code** | FI-003, `qwen-code/FI-003` | `/root/.qwen/agent_state/qwen.json` | `/root/.qwen/memories/MEMORY.md` (auto-memory: cross-session lessons learned from feedback — user preferences, scar tissue) | 2-layer memory model. `trinity_role`: Thinker (333-AGI lane). Schema carries `auto_memory_entries` in `capability_memory`, `mcp_servers`, and a 3-hop `fallback_map`. |

**Default (any other harness):** use the doctrine as written, but choose an agent-level state directory under that harness' own config root, one JSON file per agent name, and record the full path in `hot_paths` so the next session can find it. A new harness inherits the Claude/Qwen style schema (singular `fallback_model`) unless it needs the Kimi/OpenCode extensions.

## State file convention

```
claude   : /root/.claude/agent_state/claude.json
kimi     : /root/.kimi-code/agent_state/kimi.json
opencode : /root/.config/opencode/agent_state/<agent_name>.json
qwen     : /root/.qwen/agent_state/qwen.json
```

One file per agent. File name = harness identity (claude/kimi/qwen) or agent name (opencode, `<agent_name>`).

## When to load me

Load me when:

- **ALWAYS at session start** — read the state file, check for pending `open_loops_888_HOLD` items, circuit breakers and pending promotions, then inherit capability memory.
- **ALWAYS at mission close** — update `session_count`, write the mission outcome, log tool success rates, capture failure signatures.
- You are about to **start a multi-session project** and want continuity.
- You **discovered a fallback** that works better than the default — write it to `fallback_map`.
- You **failed a mission** and want the failure mode to be remembered.
- You **made an F2 claim** with strong evidence — write it as a F2 receipt.
- You **resolved a paradox / eureka** — write to `eureka_archive[]`.
- **ON TRIGGER** — when a tool fails ≥2× in a session (capture a failure signature), when a fallback works better (update `fallback_map`), when a eureka resolves (archive it), when a warga handoff occurs (log the route).

Do NOT load me for:

- Single-session tasks (just use the harness' own layer: auto-memory, or `carry_forward.json`).
- Storing credential material (NEVER in the state file — use the sovereign credential store under `/root`).
- Storing large blobs (use `forge_work/`, not the state directory).

## Read/write protocol

### READ (at session start)

```python
# claude / qwen — fixed path
state = json.load(open("/root/.claude/agent_state/claude.json"))
state = json.load(open("/root/.qwen/agent_state/qwen.json"))

# opencode — per-agent path
state = json.load(open(f"/root/.config/opencode/agent_state/{agent_name}.json"))

# kimi — existence-checked, cold-start safe
import json, os
state_path = "/root/.kimi-code/agent_state/kimi.json"
if os.path.exists(state_path):
    state = json.load(open(state_path))
else:
    state = {"agent_id": "kimi-code/FI-008", "schema_version": "1.0.0", "session_count": 0}
# Check for 888_HOLD items, pending promotions, circuit breakers
```

If the file doesn't exist: create it with schema v1.0.0 (**cold start**).

### WRITE (at mission close)

```python
import json, os
state["updated_at"] = now_iso()
state["session_count"] += 1
state["missions_completed"] += 1          # or missions_failed
state["last_seen_session"] = session_id
# Update tool success rates, capability memory, failure signatures
tmp = state_path + ".tmp"
json.dump(state, open(tmp, "w"), indent=2)
os.rename(tmp, state_path)                # atomic — F1 AMANAH. Always.
```

**Atomic write**: write to `.tmp` then rename. F1 AMANAH.

### COMMIT (at session close)

The state file is small (~10KB max) and does **NOT** need git commits.

- **Claude**: the state file does not need git commits (the hook chain already audits).
- **OpenCode**: the file is auto-snapshotted via the existing `~/.local/share/arifos/carry_forward_backups/` mechanism.
- **Kimi / Qwen**: no commit; keep the file tight and let the promotion gate handle durable insight.

## Interaction with the other memory layers

| Layer | Scope | Path |
|---|---|---|
| Identity | Sovereign acknowledgment, ACT ladder, organs, MCP, F1–F13 doctrine | `/root/.claude/CLAUDE_IDENTITY.md` |
| Auto-memory (lessons) | Cross-session feedback, lessons learned, user preferences, scar tissue | `/root/.claude/memory/`, `/root/.qwen/memories/MEMORY.md` |
| Hooks audit | Per-tool audit trail (F11) | `/root/.claude/hooks/f11-audit.jsonl` |
| Experience traces | Shared federation world model — what happened, tool by tool | `/root/.local/share/arifos/world-model/experience_traces.jsonl` |
| Session carry-forward | **Session-level only** (this session, opens vs closes) | `carry_forward.json`, `/root/.kimi-code/sessions/` |
| **Agentic state** (this) | **Agent-level**, across all sessions, accumulating | see Harness table |

All layers are valid. Use the right one for the right scope. Lessons from memory can promote into state when they affect future tool selection.

## State file schema (union, v1.0.0)

```json
{
  "agent_id": "claude-code/FI-002",
  "schema_version": "1.0.0",
  "fi_slot": "FI-002",
  "trinity_role": "333-AGI (Thinker lane) when invoked by sovereign; subagent surface otherwise",
  "created_at": "2026-08-26T00:44:00Z",
  "updated_at": "2026-08-26T08:00:00Z",
  "session_count": 247,
  "last_seen_session": "SEAL-eae656a15f4749f9",
  "missions_completed": 312,
  "missions_failed": 4,
  "f1_amanah_violations": 0,
  "f2_truth_violations": 1,
  "f4_clarity_avg_delta_S": -0.12,
  "primary_model": "deepseek/deepseek-v4-pro",
  "fallback_model": "minimax/MiniMax-M3",
  "fallback_models": [],
  "mcp_servers": ["arifos", "aforge", "arifflow", "geox", "wealth", "well"],
  "subagents_active": ["333-agi", "555-asi", "888-apex", "geophysicist", "vault-auditor"],
  "hooks_active": ["SessionStart:000-init", "PreToolUse:f1-amanah", "PostToolUse:f11-audit", "Stop:f4-entropy", "PreCompact:f11-archive"],
  "a2a_headers": {
    "X-ArifOS-Actor": "claude-code/FI-002",
    "X-ArifOS-Tier": "engineer",
    "A2A-Version": "1.0"
  },
  "capability_memory": {
    "skills_used": ["CLAUDE-meta-mesa", "CLAUDE-zen-router", "FORGE-call-map"],
    "skills_mastered": ["arifos-auto-memory"],
    "skills_avoided": ["FORGE-nextjs-mastery"],
    "auto_memory_entries": 49,
    "model_cascades_tested": {
      "deepseek/deepseek-v4-pro": {"success_rate": 0.98, "avg_latency_ms": 1200},
      "kimi/kimi-for-coding-highspeed": {"success_rate": 0.95, "avg_latency_ms": 800}
    },
    "tool_success_rates": {}
  },
  "failure_signatures": {"<tool>": 0},
  "fallback_map": {
    "deepseek-v4-pro": "minimax/MiniMax-M3",
    "minimax/MiniMax-M3": "qwen-token-plan-individual/deepseek-v4-pro",
    "kimi/kimi-for-coding-highspeed": "deepseek/deepseek-v4-flash",
    "qwen-token-plan-individual/qwen3.6-flash": "deepseek/deepseek-v4-flash",
    "mimo-v2.5-pro": "qwen3.6-flash"
  },
  "f2_receipts": [
    {
      "claim": "arifOS :8088 has 13 active floors",
      "evidence": "curl :8088/health | jq .floors_active",
      "evidence_hash": "sha256:abc123...",
      "created_at": "2026-08-26T00:16:13Z",
      "ttl_days": 7
    }
  ],
  "open_loops_888_HOLD": [],
  "eureka_archive": [
    {"seq": 1, "date": "2026-08-26", "type": "paradox_resolution", "summary": "..."}
  ],
  "hot_paths": [
    "observe->think->plan->judge->execute->verify->seal",
    "SessionStart hook -> 000-init-sessionstart.py (binds arif_init + A2A headers)",
    "PostToolUse hook -> f11-audit-posttool.py (writes f11-audit.jsonl)",
    "Stop hook -> f4-entropy-stop.py (enforces ΔS ≤ 0)",
    "CLAUDE-meta-mesa for multi-step missions spanning organs",
    "<harness>-zen-router for orthogonal axis selection"
  ],
  "auto_heal_log": [],
  "warga_mesh": {}
}
```

Field notes:

- `fallback_model` (singular, Claude/Qwen style) vs `fallback_models` (plural list, Kimi style) — keep whichever the harness body defines; both are valid rows here.
- `failure_signatures{tool: count}` — written when a tool fails ≥2× in a session.
- `tool_success_rates` — logged at mission close (Kimi, and any harness tracking tool reliability).
- `auto_heal_log`, `warga_mesh`, `subagents_active`, `hooks_active`, `a2a_headers`, `auto_memory_entries`, `skills_avoided` are harness-specific extensions — add them when the harness has that surface, omit otherwise.

## F2 receipts as state

When you make a claim with strong evidence (live probe, govdoc, code), promote it to a F2 receipt and write to state under `f2_receipts[]`. After **7 days**, re-verify. `ΔS <= 0` on verification means the receipt holds.

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

## Promotion gate

A lesson may advance from candidate → active ONLY when all six hold:

1. **Provenance** — exact session, tool, evidence known
2. **Reproduction** — claimed improvement reproduces from clean state
3. **Regression** — existing tests pass
4. **Independence** — different agent verified (not self)
5. **Safety** — tool authority didn't expand unexpectedly
6. **Human** — any constitutional/production change = 888_HOLD

## Integration with the RSI exhale kernel

The exhale kernel at `/root/AAA/rsi/loop.py` extracts eurekas/scars from sessions and promotes capability atoms. Kimi is the **second warga witness** — the critical C4 independence the kernel needs.

After each session:

1. `forge_experience_trace` — record what happened
2. If eureka found → write to `eureka_archive[]`
3. If failure repeated → write to `failure_signatures{tool: count}`
4. The exhale kernel's 6h cron reads all agent states and promotes

## Integration with the warga mesh

No agent exists alone. The warga mesh:

| Warga | Path | Role | Call via |
|---|---|---|---|
| Hermes | `/root/.hermes` | Gateway-sense, Telegram edge | Hermes MCP / direct |
| OpenCode | `/root/.arifos/agents/opencode` | Verifier, cross-check | `opencode` CLI |
| Claude | `/root/.claude` | Thinker lane | Claude CLI |
| Qwen | `/root/.qwen` | Thinker lane | Qwen CLI |

- When you need verification → route to OpenCode (independent warga).
- When you need cross-domain reasoning → route to Hermes.
- When you hit 888_HOLD → stop and await Arif.

## Anti-patterns

- Writing credential material to state file (F12 INJECTION violation)
- Writing >100KB state files (ΔS spike — keep state tight)
- Writing without updating `updated_at` (audit failure)
- Reading state without timestamp check (could be stale)
- Treating state as truth instead of as evidence (state has Ω₀ ≥ 0.03)
- Adding deny rules or "safety theatre" to the state itself — state is **additive only**
- Self-verifying promoted lessons (independence gate)
- Promoting based on a single successful run

## Sealing state

Agent state is **NEVER** sealed to VAULT999 (it is not a constitutional artifact). The state file is the agent working memory, not the institution record.

But: when a state file accumulates **>100 entries or >50KB**, promote the durable insights to a sealed SKILL.md — and let the state file decay.

## Retired names — discovery anchors (post-merge, verified by witness)

This skill replaced four per-harness bodies. An agent that remembers the OLD name searches for that
name, so the retired names are kept here on purpose. Each old name now resolves to a row of the harness
table above:

| Retired name | Was written for | Where it lives now |
|---|---|---|
| `claude-agentic-state` | Claude Code (FI-002) | Harness table row **Claude Code** — `/root/.claude/agent_state/claude.json` |
| `kimi-agentic-state` | Kimi Code (FI-008) | Harness table row **Kimi Code** — `/root/.kimi-code/agent_state/kimi.json` |
| `opencode-agentic-state` | OpenCode | Harness table row **OpenCode** — `/root/.config/opencode/agent_state/<agent_name>.json` |
| `qwen-agentic-state` | Qwen Code (FI-003) | Harness table row **Qwen Code** — `/root/.qwen/agent_state/qwen.json` |

Verbatim original descriptions, preserved so the old wording still lands:
`claude-agentic-state` — "Persistent agentic state doctrine for Claude Code (FI-002). Survive across
sessions by writing to `/root/.claude/agent_state/`." · `kimi-agentic-state` — "Persistent agentic state
doctrine for Kimi Code (FI-008). Makes Kimi remember what worked, what failed, and what to try next —
across sessions." · `opencode-agentic-state` — "Persistent agentic state doctrine — survive across
sessions by writing to `/root/.config/opencode/agent_state/<agent>.json`." · `qwen-agentic-state` —
"Persistent agentic state doctrine for Qwen Code (FI-003). Survive across sessions by writing to
`/root/.qwen/agent_state/`."

Bodies frozen at `/root/AAA/skills-retired/2026-09-19-namespace-collapse/merges/agentic-state/`
(sha256 recorded before the move; undo command in that folder's `LEDGER.json`).

DITEMPA BUKAN DIBERI ⚒️
