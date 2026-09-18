# Router Regret Metric — FED Routing Feedback Signal

> **Status:** F13_OBSERVED (2026-09-18) — forged from ChatGPT Deep Research contrast.
> **Binding:** FED routing decisions, AAA capability matching.
> **Grounding:** FED `fed_route` · `fed_report_latency` · capability-gate.md · EUREKA-08 (aggregate is for dashboard).

## The Metric

```
Regret(t) = Utility(best_possible_agent, t) - Utility(routed_agent, t)
```

Where `best_possible_agent` is determined retrospectively from outcome quality.

## Why It Matters

FED routes by model/cost/latency but has **no feedback signal from outcomes**. Without regret measurement:
- "Codex solved 78%" is meaningless without knowing which alternatives would have done better
- Router cannot learn from its mistakes
- Cost optimization is blind — an inexpensive model that causes repeated retries may cost more than a frontier model that resolves once

## Companion Metrics

```
CostPerSuccess = total_cost / accepted_tasks

RouterAccuracy = 1 - (sum(Regret) / sum(BestPossible))

EnsembleLift = multi_agent_quality - best_single_agent_quality
```

## Implementation

1. **After each federation task:** Record agent chosen, alternatives available, outcome quality, cost, latency
2. **Retrospectively:** Compute regret when ground truth is available (test pass/fail, human acceptance)
3. **Feed into FED:** Adjust routing weights based on accumulated regret per (agent_profile, task_class) pair
4. **Monitor:** Track p50/p95 regret — high median regret = router learning wrong patterns

## What Regret Reveals

| Regret pattern | Diagnosis | Fix |
|---|---|---|
| Consistently near 0 | Router is well-calibrated | Maintain |
| High for specific task class | Wrong agent for that class | Adjust routing weights |
| High for specific agent | Agent underperforming expectations | Review agent config/profile |
| High when multi-agent used | Coordination overhead > benefit | Reduce ensemble usage |
| High when single-agent used | Should have used ensemble | Increase ensemble triggers |

## EUREKA-08 Grounding

"Aggregate is for dashboard. Per-spawn = audit. Aggregate = visualization. Never audit from aggregate."

Regret must be computed **per task**, then aggregated for routing optimization. Aggregate regret without per-task attribution is meaningless.

DITEMPA BUKAN DIBERI ⚒️
