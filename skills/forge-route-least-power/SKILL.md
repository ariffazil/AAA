---
name: forge-route-least-power
id: forge-route-least-power
owner: A-FORGE
risk_tier: low
floor_scope: [F1, F2, F4, F7]
description: "Use when task may be over-engineered."
version: 2.0.0
author: FORGE (000Ω) for Arif (F13 SOVEREIGN)
forged: 2026-07-17
tags: [routing, least-power, discipline, anti-yak-shaving, efficiency, entropy]
scope: all_agents
priority: 80
autonomy_tier: T1
capability_tier: fed-agent-subagent
ecology_state: WARM
owned_by: A-FORGE
authority_of: A-FORGE
---
# ROUTE LEAST POWER — Lower Machine Entropy

> **"Can a simpler tool do this?"** — Ask this before every tool call.
> **"Is the gate itself the problem?"** — Ask this before designing one.
> **Power is not preference. Power is fitness.**
> **Lower entropy = less chaos = fewer incidents.**

---

## Gate-Design Discipline (entropy that comes from constraining entropy)

A capability gate (mode emit, content filter, capability whitelist) is itself a piece of machinery. It can become the shadow it was meant to prevent. Three rules for designing one:

1. **Gate by mutation class, not by mode class.** Read/think/audit/plan are NEVER gated — cognition is not mutation. Only the irreversible operations (deploy, seal, forge, delegate) carry a gate. A gate that touches reading is attached to the wrong boundary.
2. **TTL must exceed the longest expected audit pass.** A 300s TTL on a mode-emit gate blocks long inventory sweeps, deep audits, and multi-file patches where the same turn legitimately spans 5-10 minutes. Default TTL = max(audit-window) + margin; 30 min is a safe floor for human-paced work.
3. **A gate with no documented failure case is a shadow.** Before shipping a gate, name the failure class it prevents (fabrication? unauthorized mutation? attention theft?). If you cannot name one, the gate is not preventing — it is restricting.

The capability whitelist, TTL, and tier membership of every gate must live in **runtime queryable form** (e.g. an authority_flow_graph node), not in markdown prose. A rule you cannot query is a rule you cannot audit.

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
- ❌ Adding a mode gate, content filter, or capability whitelist without naming the failure class it prevents — gates without a stated purpose are the most common form of accidental shadow

## Shadow Detection (when an existing constraint may itself be the bug)

When a user reports the agent feels **restricted, clipped, bangang, or repeatedly apologetic** — before responding, grep the active constitution (SOUL.md, context-governor.md, lanes.yaml) for:

- character / token caps (e.g. `240`, `200`, `1600`)
- hard-banned phrase regexes (e.g. `\bpergi\s+tido\b`, `\bminum\s+air\b`)
- closing-ritual bans and boot-signature blocks
- mode-based output shaping (witness / light / analyst / coach tables)

Any of these is a candidate **shadow cap**. Present a one-line trace to the user ("the cap lives at X, owned by Y, currently enforced as Z") before suggesting a tweak — the user already knows the symptom; the trace confirms you found the cause. If the cap has no observable failure case, no test, and no owner distinct from the file containing it, it is a **strip candidate**, not a tuning candidate: move it to runtime (a queryable invariants module) or delete it. Cap-shaped complaints are rarely about the number — they are about the lack of explanation.

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
