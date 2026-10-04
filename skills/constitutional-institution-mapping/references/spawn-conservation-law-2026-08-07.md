# Spawn Conservation Law — Reference (2026-08-07, DRAFT)

## The Law

```
Agent Spawn Conservation Law:

Every spawn must transfer burden to one of four buckets:
  compute | coordination | judgment | provenance

No spawn is free. Only the bucket changes.

Swarm architecture:     coordination debt ↑
Star architecture:      judgment debt ↑
Star + judge-gate:      provenance debt ↑
```

This is **DRAFT**, pending sovereign ratification. Formal statement lives in the main SKILL.md §3.3.

## Why this matters

Swarm labs that add agents to fix coordination problems are moving burden from coordination bucket to judgment bucket (which they don't even know exists). The mature federation does the inverse: explicit judge-gate moves burden from judgment to provenance (audit trail).

**Spent correctly.**

## The T1-T5 Risk Classifier (the gate that implements this law)

Every `delegate_task` invocation must pre-classify:

| Tier | Description | Examples | Gate |
|---|---|---|---|
| T1 | Read-only analysis | grep, search, fetch, observe | Spawn freely |
| T2 | Recommendation / proposal | plan, score, propose | Spawn freely, report back |
| T3 | Code mutation | edit, write, patch, create | **Judge path required** |
| T4 | Infrastructure change | deploy, restart, migrate, configure | **Judge path required** |
| T5 | Identity / governance mutation | vault seal, key rotation, ACL, F1-F13 | **Judge path required** |

```python
if risk_class >= T3:
    seal = call_arif_judge(action=goal, action_class=...)
    if seal.verdict == 'SEAL':
        spawn(goal)  # proceed under judge's lease
    else:
        return seal  # HOLD/VOID — do not spawn
else:
    spawn(goal)  # T1/T2: safe, no judge call
```

## The four-debt timing hierarchy

| Debt | Failure cadence | Detection latency | Floor that closes it |
|---|---|---|---|
| Coordination debt | today (immediate) | milliseconds | F1 AMANAH (reversible-first) |
| Verification debt | this week (next agent cycle) | seconds-minutes | F2 TRUTH + F11 AUDITABILITY |
| Judgment debt | this month (cumulative drift) | days-weeks | F13 SOVEREIGN (judge path) |
| Provenance debt | years later (courtroom maturity) | years | F11 AUDITABILITY (VAULT999 hash chain) |

Each debt has a different cadence. Each needs different instrumentation. `judgment_coverage = apex_verdicts / risky_actions` measures only the middle one. We need four metrics, one per debt.

## Star vs Mesh Topology Math (live-verified 2026-08-07)

| n | Mesh n(n-1)/2 | Star n-1 | Savings |
|---|---|---|---|
| 6 agents (OpenCode) | 15 | 5 | 67% |
| 7 nodes (Hermes delegation) | 21 | 6 | 71% |
| 19 nodes (one nesting level) | 171 | 38+ | 78% |

Star topology is implicit Dunbar management. **"No nesting" is not anti-loop technique — it is constitutional budget against topology growth.**

If children could spawn children (depth=2), even with star topology, edge count jumps from 6 to 38+. The "no nesting" constraint at harness level is what keeps it linear.

## Three-harness comparison (the Diseconomy Boundary in practice)

| Harness | Delegation surface | In-built judge gate | Status |
|---|---|---|---|
| OpenCode | 6 named subagents (333-AGI primary) | Yes: `arifos-judge-gate.ts` plugin | Gated ✅ |
| Kimi Code | `af-*` subagents (af-forge primary) | Via `arif-do` federation plugin | Gated ✅ |
| Hermes | 6 ephemeral `delegate_task` children | **None** | **Gap** ❌ |

The gap is constitutional — every other harness routes T2+ through judgment. Hermes currently does not. **The fix is the T1-T5 classifier above.**

## Why this lives in `constitutional-institution-mapping`

This isn't pure operations — it's the institutional-economics mapping that explains **why** the floors must exist. Without it, the F1-F13 floors look arbitrary (imposed by an architect). With it, the floors are the **minimum viable geometry** for an agent to exist without the void eating everything.

Cross-reference: `constitutional-institution-mapping` SKILL.md §3.3 (the patch added in this session).

## Cross-reference

- `a2a-gateway-protocol` skill → `references/a2a-five-gate-sequence-2026-08-07.md` (the five A2A gates — operational side)
- `arifos-prompt-doctrine` skill → invariant-vs-dynamics classification (where to put the T1-T5 classifier — SOUL.md patch candidate)
- `arifos-federation-ops` skill → Lane A vs Lane B sealing (destination of SEAL-grade judgments from the classifier)
- `agent-config-validation` skill → JSON schema validation (where the Diseconomy Boundary doctrine could become a federation doc section)