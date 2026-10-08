# Autoresearch Loop Contract — Keep-or-Revert Governance

> **Verdict:** ADOPT WITH GOVERNANCE
> **Source:** github.com/karpathy/autoresearch (97.5k★ REPO, not gist; Mar 2026) + fork bquast/autoresearch-mesa
> **Compiled:** 2026-10-08 · 333-AGI · session SEAL-b117b112a28d411d

## The contract (7 rules)

1. **Evaluator frozen** — objective metric + comparison live OUTSIDE the agent-editable surface.
2. **Fixed budget** — every trial gets the same wall-clock/compute budget; runs stay comparable.
3. **One hypothesis per iteration** — single bounded change; verdicts stay attributable.
4. **Execute + measure + receipt** — no claim without a measured receipt.
5. **Keep only measured improvement; otherwise revert completely** — failures leave receipts too, not silence.
6. **Stop conditions** — evaluator drift, invalid comparison, unsafe change, budget exhausted → HALT.
7. **Human-authored policy defines the lane** — agents edit the experiment surface only (program.md ↔ AGENTS.md/SOUL.md symmetry).

## Federation alignment (measured)

| Autoresearch element | arifOS SOT already holding it |
|---|---|
| Evaluator outside editable surface | F1-F13 thresholds in /etc/arifos/canon (manifest_hash-verified, chattr +I on canon/) |
| Stop on evaluator drift | JITU (δ ≥ 0.50 → HOLD, out-of-band systemd actuator, F13 SAH 2026-10-07) |
| One-change attribution | Change-packet discipline (F13 2026-10-07): hash-bound packets, exit-code ownership |
| Fixed budget | arif_init work_contract budgets (tools/reasoning/cost) |
| Keep-or-revert receipts | **GAP** — successes seal; failures vanish. This contract closes it. |

## Hardening deltas (the new part)

- **Revert receipts mandatory:** failed experiments append `## [date] experiment | hypothesis | metric | REVERT | receipt` to knowledge log.md — the federation's autoresearch loop becomes auditable in BOTH directions (Phase C falsifier: same_signature + same_selection = ALARM).
- **Forge plan attribution:** plan_review rejects bundles of >1 independent mutation without parent links — one change per iteration, verdicts attributable.
- **GEOX adaptation:** hypothesis → bounded Earth-model change → open metric/falsifier → keep/revert. No geological claim becomes fact solely because a scalar improved.

## Revert receipt template (A2 — KEEP and REVERT are both first-class)

Append to `/root/AAA/knowledge/log.md` after every bounded experiment (forge iteration, engine change, config trial):

```
## [YYYY-MM-DDTHH:MMZ] experiment | <one-line hypothesis> | metric=<name>=<before>→<after> | KEEP|REVERT | budget=<spent/limit> | receipt=<flow/vault id> | falsifier=<what would have made this wrong>
```

Rules: failures append too — silence is the defect this template closes. Three consecutive REVERTs on the same signature = stop + consult (Phase-C alarm: same_signature + same_selection = no adaptation). REVERT receipts feed AT-007 pattern compression when volume justifies it.

