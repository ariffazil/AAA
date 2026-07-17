---
name: FORGE-route-least-power
description: >
  Route every task to the SMALLEST capability that can accomplish it.
  Prevents over-engineering, yak-shaving, and reflexive tool escalation.
  Enforces one-owner-per-task, idempotent actions, and strict queues.
  Ask: "Can a simpler tool do this?" before reaching for the powerful one.
version: 2.0.0
author: FORGE (000Ω) for Arif (F13 SOVEREIGN)
forged: 2026-07-17
tags: [routing, least-power, discipline, anti-yak-shaving, efficiency, entropy]
scope: all_agents
priority: 80
---

# ROUTE LEAST POWER — Lower Machine Entropy

> **"Can a simpler tool do this?"** — Ask this before every tool call.
> **Power is not preference. Power is fitness.**
> **Lower entropy = less chaos = fewer incidents.**

---

## The Ladder (escalate only if current tier fails)

```
TIER 1 — READ (zero side effects)
  read, glob, grep, webfetch
  ↓ insufficient? ↓

TIER 2 — OBSERVE (low cost, no mutation)
  arif_observe, forge_registry_status, forge_probe
  ↓ insufficient? ↓

TIER 3 — REASON (advisory only)
  arif_think, sequential-thinking, forge_evaluate
  ↓ insufficient? ↓

TIER 4 — MUTATE (governed, reversible)
  forge_shell, forge_git, forge_filesystem, edit, write
  ↓ insufficient? ↓

TIER 5 — EXTERNAL (network, API calls)
  forge_search, forge_fetch, brave-search, perplexity
  ↓ insufficient? ↓

TIER 6 — IRREVERSIBLE (requires F13)
  arif_seal, forge_execute_sealed, rm -rf, DROP TABLE
```

## Rules

1. **Always start at Tier 1.** Only escalate when the current tier cannot solve the problem.
2. **State your tier before acting.** "I'm using Tier 2 (observe) to check organ health."
3. **Never skip tiers.** Don't jump from read → irreversible.
4. **If two tools at the same tier work,** prefer the one with fewer side effects.
5. **If you're reaching for Tier 5+ for a simple task,** you're probably over-engineering. Stop.

## Entropy-Reducing Discipline

### One Owner Per Task
- Never let 2 agents edit the same file or service concurrently
- If work overlaps, serialize: agent A finishes fully (including verify) before agent B starts
- When in doubt, use `forge_lock` to claim ownership

### Idempotent Actions
- Every agent command should be safe to rerun
- Before running: "What happens if this runs twice?"
- If the answer is "it breaks," refactor for idempotency first
- Prefer `forge_filesystem_patch` (preview before apply) over blind write

### Strict Queues
- Serialize risky work — don't parallelize mutations on the same substrate
- Each phase completes fully (read → plan → execute → verify) before the next begins
- For parallel safe work (independent OBSERVE calls), use `forge_parallel`

### 3-Agent Routing
```
ARCHITECT decides → Tier 3 (reason)
ENGINEER applies  → Tier 4 (mutate)
AUDITOR verifies  → Tier 1-2 (read/observe)
```
- If you're doing all 3 roles, separate the VERIFY step explicitly
- Never verify with the same tool that mutated

## Anti-Patterns

- ❌ Calling `forge_shell` to read a file (use `read`)
- ❌ Calling `perplexity_research` for a local file search (use `grep`)
- ❌ Calling `arif_seal` before `arif_judge` (judge first, seal after)
- ❌ Reaching for `task()` to spawn a subagent for a single grep
- ❌ Two agents editing the same config file simultaneously
- ❌ A non-idempotent script in a cron job

## Decision Heuristic

```
Is this a question?          → Tier 1-2 (read/observe)
Is this a plan?              → Tier 3 (reason)
Is this an edit?             → Tier 4 (mutate, with F1 AMANAH backup)
Is this external research?   → Tier 5 (fetch/search)
Is this permanent?           → Tier 6 (irreversible, F13 required)
Is there an owner already?   → Wait. Don't race.
Can this run twice safely?   → If no, fix it first.
```

## Seal

This skill prevents tool escalation spirals. It's the agent's cost function.
Every unnecessary Tier 5+ call wastes compute and increases blast radius.
One owner, idempotent actions, strict queues — lower entropy every cycle.

DITEMPA BUKAN DIBERI.
