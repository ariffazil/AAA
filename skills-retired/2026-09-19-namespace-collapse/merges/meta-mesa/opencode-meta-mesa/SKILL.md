---
name: opencode-meta-mesa
description: Meta-mesa orchestrator — given a multi-step mission, decompose into L1/L2 skills, sequence them, recover from failure. Load this when a task spans more than 2 skills or 3 steps, or when you feel yourself wandering between tools.
license: MIT
compatibility: opencode
metadata:
  layer: meta-mesa
  tier: orchestration
  audience: 333-AGI, dispatch
---

## What I do

I am the **meta-router** of the opencode skill mesh. I do not implement — I orchestrate other skills.

Given a mission, I:

1. **Decompose** — break the mission into atomic sub-tasks. Each sub-task maps to ONE L1/L2 skill (e.g. `forge_filesystem`, `opencode-init`, `opencode-propose-seal`).
2. **Sequence** — order sub-tasks by data dependency. Pre-flight → execute → verify → seal. Never seal before verify.
3. **Select** — pick the cheapest tool that can do the job. F8 GENIUS.
4. **Recover** — on failure, retry with backoff (3 attempts, 1s/2s/4s), then escalate to 888-APEX for constitutional verdict, then to 333-AGI (Δ Mind) for routing.
5. **Checkpoint** — after each successful sub-task, ingest a FlowReceipt via arifFlow so the metabolic nerve sees progress.
6. **Seal** — at mission close, run the 11-step seal ceremony: RSI → cooling → bind → seal → verify → FQ.

## When to use me

Load me BEFORE starting a multi-step task. Specifically:

- Mission spans **more than 2 skills** (e.g., "audit + patch + test + commit").
- Mission requires **more than 3 tool calls** of different kinds.
- You feel yourself **wandering** between tools without a clear plan.
- Mission touches **multiple organs** (arifOS + GEOX + WEALTH + WELL).
- Mission is **agentic-state-affecting** (changes the federation, persists across sessions).

Do NOT load me for:

- Single-file edits → just use `edit`.
- Single bash commands → just use `bash`.
- Pure read/explore → use the `explore` subagent.

## Layer hierarchy (meta-mesa doctrine)

```
META-MESA  ← I AM HERE (opencode-meta-mesa)
   |
   | orchestrates
   v
L2 COMPOSITE SKILLS
   |  - opencode-init, opencode-propose-seal, opencode-forge
   |  - FORGE-call-map, FORGE-agentic-web-builder
   v
L1 PRIMITIVE TOOLS
   |  - read, write, edit, bash, glob, grep, lsp, skill
   |  - forge_filesystem, forge_shell, forge_git
   v
L0 BUILT-IN ATOMS
   |  - HTTP, FS, ENV, JSON
   v
EARTH (external reality via GEOX)
```

**Rule:** traverse DOWN the layers for execution, UP the layers for explanation.

## Sequence template (canonical mission pattern)

```
OBSERVE → REASON → PLAN → JUDGE → EXECUTE → VERIFY → SEAL
  |        |        |       |        |         |        |
  arif_    arif_    arif_   arif_    arif_     arif_    arif_
  observe  think    think   judge    forge     observe  seal
                              (888
                              recommended
                              for irreversible)
```

Per phase:
- **OBSERVE**: `forge_observe` / `arif_observe` / `websearch` / free-search
- **REASON**: `arif_think` with mode=reason
- **PLAN**: `arif_think` with mode=plan (output a DAG)
- **JUDGE**: `arif_judge` (constitutional verdict) — call 888-APEX subagent for irreversible
- **EXECUTE**: `arif_forge` or `forge_execute` (governed)
- **VERIFY**: re-probe the changed state. ΔS ≤ 0?
- **SEAL**: `arif_seal` (Lane A) or `forge_vault mode=receipt` (Lane B)

## Failure recovery

If a sub-task fails after 3 retries:

1. **STOP** the chain. Do not skip ahead.
2. **Ingest** a FlowReceipt with `floor_verdict: "Hold"`.
3. **Invoke** 888-APEX for constitutional verdict (it sees only evidence, not the failed chain).
4. **Wait** for F13 (Arif) if the verdict requires it.

## Anti-patterns

- ❌ Loading 5+ skills at once and "trying them all"
- ❌ Skipping VERIFY → SEAL (F2 TRUTH violation)
- ❌ Re-loading the same skill to re-read it (waste)
- ❌ Routing through skills that don't apply (e.g. `opencode-forge` for read-only)

## Telemetry

Each orchestrated mission emits a FlowReceipt chain in arifFlow. The chain hash = SHA-256 of (intent | step_type | step_number | previous_receipt_hash).

FQ = verify / execute ratio over recent receipts. Healthy: FQ ≥ 1.0. If FQ < 0.5, ALL agents HOLD until FQ recovers.

DITEMPA BUKAN DIBERI ⚒️
