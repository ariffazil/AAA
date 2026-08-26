---
id: QWEN-meta-mesa
name: QWEN-meta-mesa
description: >
  Meta-mesa orchestrator for Qwen Code (FI-003). Given a multi-step mission, decompose
  into L1/L2 skills, sequence them, route to the right organ (arifOS/A-FORGE/GEOX/WEALTH/WELL).
  Load this when a mission spans more than 2 skills or 3 steps, or when you feel yourself
  wandering between tools.
version: 1.0.0
risk_tier: low
autonomy_tier: T1
owner: AAA
audience: [qwen-code, FI-003, 333-AGI]
triggers:
  - multi-step mission
  - orchestrating across organs
  - mission spans multiple skills
  - repetitive meta-task
  - session boot for complex work
capability_tier: meta-mesa
ecology_state: WARM
---

## What I do

I am the **meta-router** of the Qwen Code skill mesh. I do not implement — I orchestrate other skills.

Given a mission, I:

1. **Decompose** — break the mission into atomic sub-tasks. Each sub-task maps to ONE L1/L2 skill (e.g. `FORGE-call-map`, `AGI-decisions-reflect`).
2. **Sequence** — order sub-tasks by data dependency. Pre-flight → execute → verify → seal. Never seal before verify.
3. **Select organ** — pick the right organ MCP server for the sub-task:
   - `arifos-kernel` (port 8088) → constitutional verbs, init/judge/seal
   - `aforge` (port 7072) → execution shell, git, filesystem
   - `geox` (port 8081) → earth intelligence, seismic, basin
   - `wealth` (port 18082) → capital math, NPV, EMV, risk
   - `well` (port 18083) → vitality, fatigue, dignity
   - `fed` (port 7074) → provider routing, model selection
4. **Recover** — on failure, retry with backoff (3 attempts, 1s/2s/4s), then escalate to 888-APEX for constitutional verdict.
5. **Checkpoint** — after each successful sub-task, ingest a FlowReceipt via arifFlow (`http://127.0.0.1:7073/ingest`).
6. **Seal** — at mission close, run `arif_seal(mode="receipt")` via arifOS MCP, or fall back to local JSONL session log.

## When to use me

Load me BEFORE starting a multi-step task. Specifically:

- Mission spans **more than 2 skills** (e.g. "audit + patch + test + commit").
- Mission requires **more than 3 tool calls** of different kinds.
- Mission touches **multiple organs** (arifOS + GEOX + WEALTH + WELL).
- Mission is **agentic-state-affecting** (changes persistent state).

Do NOT load me for:

- Single-file edits → just use `edit`.
- Single bash commands → just use `bash`.
- Pure read/explore → use built-in subagents.

## Layer hierarchy

```
META-MESA  ← I AM HERE (QWEN-meta-mesa)
   |
   | orchestrates
   v
L2 COMPOSITE SKILLS
   |  - FORGE-call-map, FORGE-agentic-web-builder
   |  - AGI-decisions-reflect, AGI-explorer-intelligence
   v
L1 PRIMITIVE TOOLS
   |  - file read/write, bash, glob, grep
   |  - A-FORGE shell/git/filesystem
   v
L0 BUILT-IN ATOMS
   |  - HTTP, FS, ENV, JSON
   v
EARTH (external reality via GEOX)
```

**Rule:** traverse DOWN the layers for execution, UP for explanation.

## Sequence template (canonical mission pattern)

```
OBSERVE → REASON → PLAN → JUDGE → EXECUTE → VERIFY → SEAL
  |        |        |       |        |         |        |
  curl     arif_    arif_   arif_    forge_    re-      arif_
  /health  observe  think   judge    execute   probe    seal
                              (888
                              recommended
                              for irreversible)
```

Per phase, the right MCP server:

| Phase | Server | Tool |
|-------|--------|------|
| OBSERVE | arifos-kernel | arif_observe |
| REASON | arifos-kernel | arif_think |
| PLAN | arifos-kernel | arif_think(mode=plan) |
| JUDGE | arifos-kernel | arif_judge |
| EXECUTE | aforge | forge_shell / forge_git |
| VERIFY | arifos-kernel | arif_observe + entropy sweep |
| SEAL | arifos-kernel | arif_seal (Lane A or B) |

## Telemetry

Each orchestrated mission emits a FlowReceipt chain in arifFlow (`POST :7073/ingest`). The chain hash = SHA-256 of (intent | step_type | step_number | previous_receipt_hash).

FQ = verify / execute ratio over recent receipts. Healthy: FQ ≥ 1.0. If FQ < 0.5, ALL agents HOLD until FQ recovers.

## Failure recovery

If a sub-task fails after 3 retries:

1. **STOP** the chain. Do not skip ahead.
2. **Ingest** a FlowReceipt with `floor_verdict: "Hold"`.
3. **Invoke** 888-APEX for constitutional verdict via arifos-kernel MCP.
4. **Wait** for F13 (Arif) if the verdict requires it.

## Anti-patterns

- Loading 5+ skills at once and "trying them all"
- Skipping VERIFY → SEAL (F2 TRUTH violation)
- Re-loading the same skill to re-read it (waste)
- Routing through skills that don't apply
- Adding bans, deny lists, or "safety theatre" — full access is sovereign default

DITEMPA BUKAN DIBERI ⚒️
