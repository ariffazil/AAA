---
id: QWEN-zen-router
name: QWEN-zen-router
description: >
  Orthogonal axis routing for Qwen Code (FI-003). Given an intent, classify it across 9
  orthogonal axes (organ, action, mode, tier, layer, surface, scope, time, reversibility)
  and route to the right organ MCP server. Load when you must pick between equally-valid
  tools.
version: 1.0.0
risk_tier: low
autonomy_tier: T1
owner: AAA
audience: [qwen-code, FI-003, 333-AGI]
triggers:
  - which organ
  - which tool
  - routing decision
  - tool selection
  - branching decision
capability_tier: meta-mesa
ecology_state: WARM
---

## What I do

I am the **zen router**. I do not orchestrate (that's `QWEN-meta-mesa`). I **classify and select**.

Given an intent, I evaluate it against **9 orthogonal axes** and produce a routing decision:

| Axis | Question | Options |
|------|----------|---------|
| 1. **organ** | Which federation organ owns this? | arifos, aforge, geox, wealth, well, fed, none |
| 2. **action** | What kind of work? | observe, reason, plan, judge, execute, verify, seal, route, memory |
| 3. **mode** | Read or write? | read, write, mutate, irreversible |
| 4. **tier** | How expensive? | free (FLAME), cheap (token-plan), medium (direct), heavy (apex), forbidden |
| 5. **layer** | What layer of the stack? | earth, governed, free, constitutional, kernel |
| 6. **surface** | Which tool surface? | filesystem, shell, MCP, plugin, federation, web, native |
| 7. **scope** | Federation or local? | local, project, federation, sovereign |
| 8. **time** | Latency tolerance? | realtime, batch, async, anytime |
| 9. **reversibility** | Can this be undone? | reversible, soft-irreversible, irreversible |

**Rule:** the answer to all 9 axes defines the tool. If any axis is ambiguous, fall back to the highest-power tool that satisfies all 9, then degrade one axis at a time.

## When to use me

Load me when:

- You have **two or more equally-valid tools** and need to pick.
- You want to **route by intent**, not by tool name.
- You're at a **branching decision** and want to make the call explicit.
- You want to **document your reasoning** for an audit trail.

Do NOT load me for:

- Trivial choices (one obvious tool).
- Missions (use `QWEN-meta-mesa` instead).

## Decision table (excerpt for Qwen Code)

| Intent | organ | action | tier | layer | surface | reversible |
|--------|-------|--------|------|-------|---------|------------|
| "Read VAULT999 seal chain" | arifos | observe | free | constitutional | mcp | yes |
| "Run pytest on /root/A-FORGE" | aforge | execute | medium | governed | mcp | yes |
| "Add memory of fact X" | arifos | memory | free | constitutional | mcp | yes |
| "Build new MCP server" | aforge | execute | heavy | governed | mcp | yes |
| "Drop Postgres table" | aforge | execute | forbidden | governed | mcp | NO → 888_HOLD |
| "Search the web" | hermes | observe | free | free | mcp | yes |
| "Draft new SKILL.md" | aforge | execute | medium | governed | filesystem | yes |
| "Seal a verdict" | arifos | seal | heavy | constitutional | mcp | NO (Lane A) |

## Routing examples

```yaml
intent: "Audit drift in geox-basin skill"
axes:
  organ: geox          # domain tool
  action: observe      # reading, not writing
  tier: cheap          # qwen-token-plan
  layer: governed
  surface: mcp
  scope: project
  reversibility: full
tool: geox_geox_basin(mode="profile", basin_name="...")
```

```yaml
intent: "Mutate forge_work/2026-08-26-x.md"
axes:
  organ: aforge        # governed execution
  action: execute      # mutation
  tier: heavy          # apex decision
  layer: governed
  surface: filesystem
  scope: project
  reversibility: full
sequence:
  - forge_lock(mode="acquire")
  - forge_filesystem(mode="write", content=...)
  - forge_entropy_sweep(path="forge_work/")
  - forge_lock(mode="release")
  - arif_seal(mode="receipt")  # Lane B
```

## Anti-patterns

- Asking "which tool should I use?" without answering the 9 axes
- Routing everything to the apex (heavy) when free suffices
- Skipping reversibility check before mutation
- Adding deny rules, MCP gating, or "safety theatre" — full access is sovereign default
- Routing through a layer you don't understand

## Routing theorem

> **The cheapest tool that satisfies all 9 axes is the right tool.**

If two tools satisfy all 9, pick the one with the lower tier.
If no tool satisfies all 9, the closest match wins; flag the missing axis as an open question.

DITEMPA BUKAN DIBERI ⚒️
