---
name: aaa-constitution-architecture-audit
description: "Evaluate federation organ placement against constitutional ceilings and financial viability. Produce scoring matrix, verify all organs stay within charter, calculate 3-year NPV/EMV/IRR for alternatives."
tags: [constitution, architecture, governance, cost-benefit, organ-placement]
---

# AAA Constitution Architecture Audit

## Purpose

When user asks "**Why does X belong under AAA?**" or "**Where should organ Y live?**" or any question about **organ placement authority**, run this audit protocol.

## Core Doctrine

> **Separate authority ≠ Separate repo.**
> **Repository boundary ≠ Authority boundary.**

Decision driven by **release cadence** (lifecycle independence), not just organizational chart. One authority can have multiple repos. Multiple authorities can share one repo (low coupling).

## Four Scenario Framework

| Scenario | What It Does | When To Use |
|----------|-------------|-------------|
| **A · Siblings** | Organs remain separate peers, co-located on VPS | Default. All organs healthy, no friction yet |
| **B · Merge Upstream** | One organ becomes gatekeeper over others | Only with F13 amendment; never silent re-role |
| **C · Merge Downstream** | Fold smaller organ into larger one | When both have same ceiling AND release cadence aligned |
| **D · Extract** | Create new dedicated service/repo | When lifecycle independence becomes real (version drift) |

## Scoring Matrix (5-point scale, weighted)

Score each scenario 1-5 on these criteria:

| Criterion | Weight | Meaning |
|-----------|--------|---------|
| **Constitutional Alignment** | 30% | Do ceilings (OBSERVE_ONLY, 777_FORGE, ADVISORY, etc.) stay intact? |
| **Authority Separation** | 20% | Least privilege preserved? No judge/router/executor collapse? |
| **Operational Risk** | 15% | Blast radius of failure? Reversibility if wrong? |
| **Closed-loop Value** | 15% | Can you actually improve self-correction without breaking rules? |
| **Auditability (F11)** | 10% | Is decision provenance clear per change? |
| **Cost/Complexity** | 10% | Developer time/month, CI/CD overhead |
| **Future Extraction** | 10% | Easy to migrate out if needed? |

**Disqualification Rule:** Any scenario violating a constitutional ceiling scores ≤1 and is rejected unless user explicitly amends constitution.

## Financial Model (3-year horizon)

```python
NPV = Σ(Monthly_Cost_t / (1+r)^t) - Initial_Setup_Cost
EMV = NPV × (1 - Risk_Adjustment_Factor)
IRR = Rate where NPV == 0
Payback_Months = Time until cumulative cash flow turns positive

Risk_Adjustment_Factor = weighted average of high-risk scenarios from institutional sink theory
Monthly_Cost = (developer_time_hours × $50/hr) + CI/CD_minutes × $0.05/min + storage × $0.023/GB
```

Where:
- developer_time_hours = estimated maintenance hrs/month × 12 months
- Initial_Setup_Cost = developer_days × $800/day (blended engineering rate)

## Live Probe Checklist (Before Verdict)

Verify current state before recommending change:

```bash
for svc in frame-organ.service litellm-federation.service flame.service; do
  systemctl status $svc 2>/dev/null | head -3
done

curl -sf http://127.0.0.1:7074/health  # FED
curl -sf http://127.0.0.1:18901/health  # FLAME
curl -sf http://127.0.0.1:18085/health  # FRAME

git log --oneline --since='90 days ago' /root/AAA/scripts/fed* | wc -l
git log --oneline --since='90 days ago' /root/FRAME/src/ | wc -l
```

If services running >30 days with zero TODO/FIXME items → **"if it ain't broke, don't fix it"** default applies.

## The "Charter-Safe Upgrade" Pattern

When you want closed-loop improvement but can't break ceilings:

> **Add read-only telemetry taps instead of mutation gates.**

Example: FRAME already probes FED at :7074. Instead of making FRAME mutate FED routing weights, just route those probe results to where Arif reviews drift reports. Insight closure *without mutation*.

## Output Template

```markdown
## Summary

**Verdict:** [Scenario Letter — Name] ✅ RECOMMENDED / ❌ NOT RECOMMENDED

### Scorecard

| Scenario | Constitutional | Separation | Risk | Closed-loop | Audit | Cost | Total |
|----------|---------------|------------|------|-------------|-------|------|-------|
| A · X    | 5             | 5          | 5    | 1           | 4     | 5    | 30    |
| B · Y    | 1             | 2          | 3    | 5           | 4     | 3    | 22    |
| C · Z    | 4             | 3          | 2    | 3           | 4     | 2    | 19    |
| D · W    | 1             | 1          | 2    | 2           | 5     | 3    | 18    |

### Financial Metrics (3-Year Horizon)

| Metric | Status Quo | Alternative | Delta |
|--------|------------|-------------|-------|
| Initial Cost | $0 | $X,XXX | +$X,XXX |
| Monthly Maint | $XX | $XXX | +$XX |
| NPV | -$XXX | -$XXX | +$XX |
| Lock-in Score | 2/10 | 6/10 | +4 |

### Key Constraint

[The governing principle that rules out most alternatives]

Example: "Any scenario improving closed-loop score from 1→5 requires giving FRAME mutation power = OBSERVE_ONLY breach = de facto F13 amendment."

### Recommendation

Keep current structure unless actual operational friction emerges (not theoretical). The architecture is already optimal given constitutional constraints.

Upgrade path: Add [telemetry tap name] for insight closure without mutation.
```

## Pitfalls

- **Never** silently re-role an organ from OBSERVE_ONLY → mutating authority
- **Never** merge lanes that have different ceilings (free-tier vs paid-tier inference)
- **Never** treat repository boundary as authority boundary
- **Never** recommend changes when services have been stable >30 days without friction
- **Always** run live probes first — config files don't tell reality

## References

See also:
- `/root/AAA/governance/FRAME_DESIGN.md` (W-vector measurement doctrine)
- `/root/AAA/docs/MCP-FRAME.md` (MCP capability mapping principles)