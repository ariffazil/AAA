---
name: ground-relayed-agent-claims
description: Ground another agent's audit claims against live reality.
---

# Ground Relayed Agent Claims

When another agent (external AI, subagent, witness bot, or another lane) relays an audit, verdict, or report, do NOT accept it whole and do NOT reject it whole. Ground it claim-by-claim against live measured reality, then report what survives.

## Steps

1. **Extract the load-bearing claims.** Pick the specific, falsifiable numbers/assertions — not the framing. `F1=0.0`, `13/13 pass`, `22 commit gap`, `drift=false` are claims; "the system is immature" is framing.
2. **Probe the live source, not the relay.** `curl` the health endpoint, `git rev-parse` the SHAs, read the actual file. The relay is a *description* of a measurement, not the measurement.
3. **Classify each claim** as BETUL / SALAH / SEPARUH (half-true, mislabeled, or stale), each with the evidence that decided it. A claim can be directionally right and factually wrong at the same time — say both.
4. **Report the verdict table** (claim → live → verdict), then one line on what actually matters.

## Pitfalls

- **Self-report fields lie; measured truth doesn't.** `drift=false`, `deployment_drift_status:"aligned"`, `"13/13 pass"`, `deployed_commit==source_commit` are the service narrating itself. Verify against `git rev-parse HEAD` on source vs runtime, or against `floors_provenance` — never against the `/health` summary line alone.
- **Surface confusion.** An auditor mixes fields from `/health` with fields from a different MCP surface (arif_init / arif_observe) and labels them all "OBS live /health." Check WHERE each number came from before trusting it.
- **Stale numbers are worse than wrong numbers.** Deploy gaps and floor counts change while an agent drafts its report — the gap read 22, then 88, then 97. Quote the probe time; a moving target makes every fixed number stale.
- **A single snapshot is not a trend.** A reading that flipped (F1 pass↔fail, fq 0.39→0.92) is an oscillation, not a direction. Never read one instant as "worsening."
- **Independent ≠ correct.** ChatGPT trusted the self-report ("converged"); 333-AGI and Claude saw the contradiction but quoted stale/mixed numbers. Strong, honest auditors still fall for the same trap — you still re-probe every claim.
