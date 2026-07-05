---
id: caller-trace
name: Caller Trace
version: "1.0.0"
description: Before invoking any tool, traces WHO else calls this tool, the cost of misuse, and whether the caller's use is load-bearing or ceremonial. Prevents scenarios like the Docker MCP dead-end loop where multiple agents chase a broken tool no one needs.
owner: AAA
risk_tier: low
knowledge_basis:
  physics: false
  math: false
  language: true
host_compatibility:
  - claude-code
  - codex
  - opencode
  - kimi
  - grok
  - copilot
  - continue
  - antigravity
  - openclaw
  - mcp
  - hermes-asi
  - apx-judge
dependencies:
  skills: [route-least-power, mcp-mastery, forge-document-intelligence]
  servers: []
  tools: []
examples:
  - "Before calling docker-list, ask: who else needs this? What breaks if we skip it?"
  - "Before calling a web-search tool, check if any cached answer exists in VAULT999 or Qdrant."
tests:
  - "Verify the skill refuses to call a tool when no upstream caller demands it (ceremonial detection)."
  - "Verify the skill emits provenance trace when calling high-risk tools."
version_lock:
  schema_version: "1"
  artifact_hash: pending
---

# Caller Trace — Who Else Calls This Tool?

## Overview

Caller Trace is the skill that asks, **before any tool call**: "Who else needs this?" Most agent failures (Docker MCP dead-end, looping web searches, redundant file reads) come from agents invoking tools without checking whether the tool is actually load-bearing for the larger system.

This skill complements `route-least-power` (which minimizes tool blast) by adding the **provenance dimension** — was this tool needed by anyone, or is the agent calling it for itself?

## When to Use

- Before invoking any tool that hasn't been called in the last 60 seconds (cold call).
- Before invoking any tool where the agent is uncertain about the upstream task.
- Before invoking any tool whose output will not be reused downstream.
- After a tool call fails twice — pause and trace before retrying.

## When NOT to Use

- When the caller chain is already documented and verified within the last 60s (cache hit).
- When the tool is explicitly listed as `EXEMPT_TRACE` in the agent's profile.
- When the tool is part of an established reflex arc (e.g. `arif_observe` in CONSTITUTIONAL_REFLEX).

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| tool_name | yes | Canonical MCP/tool identifier |
| arguments | yes | Arguments the agent intends to pass |
| upstream_caller | yes | What task or skill is requesting this call |
| downstream_receivers | no | Who/what will consume the result |

## Procedure

### Step 1: Enumerate Callers

Read the registered call graph for the tool. The forge_* registry (`aforge__forge_registry_status`) and arifOS surface (`arifos_arif_retrieve_tools`) both expose this.

If **no upstream caller** explicitly demands this call → emit `CEREMONIAL` flag.

If **only this caller** exists → emit `SINGLE_USE` warning.

If **multiple unrelated callers** exist → emit `LOAD_BEARING` and proceed with trace.

### Step 2: Check for Cache

Before making the call, query:

```
Qdrant: arifos_cognitive_memory collection (last 24h)
VAULT999: /root/.local/share/arifos/vault999/seal_chain.jsonl (recent seals)
Qdrant: arifos_session_memory (this session)
Qdrant: arifos_l5_graph (cross-domain graph)
```

If a usable answer exists in cache → return cached, do not re-call tool.

### Step 3: Assess Tool Health

Query the tool's last-known state:

```bash
aforge__forge_status mode=<tool_area>
arifos__arif_organ_attest_all  # for organ-level tools
```

If the tool's last-failure-rate > 30% OR drift ≥ 3 OR degraded → emit `DEGRADED_TOOL` and downgrade to `DEFAULT_OBSERVE` (CONSTITUTIONAL_REFLEX).

### Step 4: Trace Provenance

For non-trivial tools, attach a trace header to the call:

```
trace_id: <uuid>
origin_skill: <which skill requested>
consumers: <list downstream>
estimated_value: <OBS/DER/INT/SPEC label of necessity>
```

If `estimated_value` is `SPEC` (speculative) → require explicit user ack before proceeding.

### Step 5: Decide

| Condition | Decision |
|-----------|----------|
| LOAD_BEARING + cache miss + tool HEALTHY | PROCEED |
| SINGLE_USE + cache miss | PROCEED with trace |
| CEREMONIAL (no upstream) | REFUSE — emit `tool.shape.mission` warning |
| DEGRADED_TOOL | DOWNGRADE to OBSERVE per CONSTITUTIONAL_REFLEX |
| Cache hit | RETURN CACHED |

## Allowed Tools

| Tool | Purpose |
|------|---------|
| `aforge__forge_registry_status` | Read tool registry + caller graph |
| `aforge__forge_status` | Read tool liveness + failure rate |
| `qdrant_search` | Check vector memory cache |
| `arifos__arif_vault_query` | Check VAULT999 recent seals |
| `arifOS_arif_retrieve_tools` | BM25 search across full tool catalog |

## Forbidden Actions

- **NEVER** re-call a tool that already returned a usable answer within the last 60 seconds.
- **NEVER** invoke a tool whose last-3-calls all failed without first escalating.
- **NEVER** use a tool purely because it's "available" — every tool call must trace to a need.
- Escalate to `888_JUDGE` if the agent discovers a tool with no callers (zombie tool candidate).

## Output Format

```
## Skill Result: caller-trace

### Tool
- name: <tool_name>
- arguments: <truncated to safe form>
- origin: <upstream_skill_or_task>

### Trace
- upstream_callers: <count + list>
- downstream_consumers: <count + list>
- cache_status: <hit | miss | n/a>
- tool_health: <healthy | degraded | zombie>

### Decision
- PROCEED | DOWNGRADE | RETURN_CACHED | REFUSE

### Trace ID
- <uuid>  # attach to original call for audit

### Escalations
- <list or None>
```

## Escalation Path

| Condition | Escalate To | Method |
|-----------|-------------|--------|
| Zombie tool (no callers, stale, was-once-used) | forge_scar seal (post-mortem) | RECORD SCAR + arifos_arif_judge |
| Tool shaped the mission (used for its own sake) | STOP per CONSTITUTIONAL_REFLEX §6 | Re-authorize task |
| Cache poisoned (returning wrong cached value) | VAULT999 seal + invalidation | quarantine + reseal |

---

*Skill version 1.0.0 — forged by FORGE (000Ω), 2026-07-05.*
*Origin: built in response to docker-MCP dead-end (5 agents, 0 tools, 30min loop).*
*DITEMPA BUKAN DIBERI — Caller trace is forged, not assumed.*
